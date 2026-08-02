# 临高启明同人写作 Skill — 实施方案 v3（审计双轮修订版）

> 基于 [AUDIT_REPORT.md](E:\AI_project\lgqm_roles\AUDIT_REPORT.md)（12 项）与 [AUDIT_REPORT_v2.md](E:\AI_project\lgqm_roles\AUDIT_REPORT_v2.md)（7 项）全量修订
> v3 新增修复：depth=0 平铺布局 Bug、fallback 提取算法具体化、领域重叠说明、install.py 校验、黑名单净化、平铺布局专项测试

---

## Context

`E:\AI_project\lgqm_roles\` 下有 81 个角色蒸馏 skill，用户写作同人时需手动判断调用哪个。目标：开发 `lgqm-writing` meta-skill，自动识别场景、匹配并调用角色 skill。

三个核心需求：
1. 角色 skill 作为"子文件"组织，保持 `.claude/skills/` 目录整洁
2. 支持未来持续新增角色（目前 81，目标无上限）
3. 零修改即可移植到其他电脑

## 审计发现的关键风险（已在本版方案中全部解决）

| # | 风险 | 等级 | 解决方案 |
|---|------|------|----------|
| 1 | 7 个 SKILL.md 缺失 `triggers` 字段 | 🔴 | 统一补齐 + build_catalog.py fallback |
| 2 | `find_perspective_dirs()` 路径不安全 | 🔴 | 安全校验 + 黑名单过滤 |
| 3 | scenario-mapping 是手动单点瓶颈 | 🔴 | 改为领域标签引用，运行时动态解析 |
| 4 | 路由器无 fallback 策略 | 🟡 | 定义无匹配/过多匹配/Skill 失败三种回退 |
| 5 | PowerShell 安装命令不可移植 | 🟡 | 用 install.py 脚本替代 |
| 6 | 领域标签推断算法未定义 | 🟡 | 定义 28 领域 × 关键词映射表 |
| 7 | workflow 文件格式不明确 | 🟡 | 明确为 Markdown 指令文件，由 SKILL.md 按需加载 |
| 8 | 无增量构建机制 | 🟢 | catalog 头部加时间戳 + hash |
| 9 | 测试策略过薄（5 个用例） | 🟢 | 扩展为 6 类 × 5+ 用例 = 30+ |
| 10 | 行数估算偏低 | 🟢 | 按实际预估调整 |
| 11 | **[v2] depth 遍历遗漏平铺布局（致命）** | 🔴 | `for depth in [1,2]` 改为显式三 pattern，含 depth=0 平铺 |
| 12 | **[v2] fallback 提取算法未具体化** | 🟡 | 定义 `extract_keywords_from_description()` 三条规则 |
| 13 | **[v2] 领域关键词重叠歧义** | 🟡 | 文档化"多领域归属合理"原则 |
| 14 | **[v2] install.py source_root 可能指向错误** | 🟡 | 增加源仓库根校验，失败时清晰报错 |
| 15 | **[v2] 黑名单含 `.claude` 不合理** | 🟢 | 移除 `.claude`，黑名单仅含 .git/batches/lgqm-writing/__pycache__ |
| 16 | **[v2] 平铺布局无专项测试** | 🟢 | 验证标准新增模拟平铺布局测试 |

---

## 1. 架构设计

### 1.1 双布局策略

**源仓库**（开发/管理）：角色按 3 个分类目录组织 → 便于人类管理和蒸馏流程
**安装后**（使用）：全部 `*-perspective/` + `lgqm-writing/` 平铺在 `.claude/skills/` → Claude Code 自动发现

```
.claude/skills/                    # 安装后（任意机器）
├── lgqm-writing/                  # 路由器（复制整个目录即可）
│   ├── SKILL.md                   # 入口 + 路由协议（~450 行）
│   ├── references/
│   │   ├── character-catalog.md   # 自动生成：全角色速查表
│   │   ├── domain-index.md        # 自动生成：领域→角色映射
│   │   ├── scenario-mapping.md    # 手动：场景→领域标签（非硬编码角色名）
│   │   └── writing-principles.md  # 手动：同人写作方法论
│   ├── scripts/
│   │   ├── build_catalog.py       # 扫描 SKILL.md → 生成 catalog
│   │   ├── validate_catalog.py    # 校验 + --test 测试矩阵
│   │   └── install.py             # 跨平台安装脚本
│   └── workflows/                 # Markdown 指令文件（被 SKILL.md 按需加载）
│       ├── single-character.md
│       ├── multi-character.md
│       ├── scenario-recommend.md
│       └── fallback.md            # 🆕 审计新增：回退策略
│
├── beiwei-perspective/            # 平铺！不在子目录中
├── changshide-perspective/
├── ... (全部 *-perspective/，平铺)
└── chongzhen-perspective/
```

### 1.2 路由工作流

```
用户输入 → Phase 1: 意图分类 → Phase 2: 角色匹配 → Phase 3: Skill 调用 → Phase 4: 合成输出
              │                      │                    │
              ├─ 直接角色名?         ├─ catalog 精确匹配   ├─ 成功 → 输出
              ├─ 场景描述?           ├─ domain-index 模糊   ├─ 失败 → workflows/fallback.md
              ├─ 多角色?             ├─ scenario-mapping    └─ 部分失败 → 标注缺失
              └─ 设定问题?           └─ 无匹配 → fallback
```

### 1.3 回退策略（🆕 审计 #4）

| 情况 | 行为 |
|------|------|
| **无匹配** | 不直接拒绝。从 `character-catalog.md` 输出分类摘要，引导用户缩小范围。提示"你可以用以下关键词重新描述场景：雷州/广州/山东/江南/军事/政治/商业/..." |
| **匹配过多**（>5 个） | 按优先级排序（scenario-mapping 推荐 > domain-index 匹配 > 纯关键词），展示 top-5，告知"还有 N 个可选角色，是否需要更精确的筛选？" |
| **Skill 调用失败** | 返回部分结果 + 标注"以下角色未能加载：[name]" + 提示用户检查 `*-perspective/` 目录是否已安装 |
| **格式 B 角色**（无 triggers） | 对 description 做关键词提取作为 fallback，`validate_catalog.py --test` 输出 warning 列出缺失项 |

---

## 2. 🔴 关键修复：Frontmatter 格式统一

### 2.1 问题

7 个 SKILL.md 缺失独立 `triggers` 字段，触发词嵌入在 `description` 散文中：

| 文件 | 当前格式 |
|------|----------|
| `chentong-perspective/SKILL.md` | description 含 `当用户要求"以陈同视角/口吻"时使用` |
| `dongmingdang-perspective/SKILL.md` | description 含 `当用户要求"用董明珰/董明铛视角或口吻"时使用` |
| `gaoju-perspective/SKILL.md` | （同上模式） |
| `liluoyou-perspective/SKILL.md` | （同上模式） |
| `limo-perspective/SKILL.md` | （同上模式） |
| `mapeng-perspective/SKILL.md` | （同上模式） |
| `wangzhaomin-perspective/SKILL.md` | description 含 `Use when the user explicitly asks for 王兆敏...` |

### 2.2 修复方案（双轨）

**轨道 A**：手动补齐这 7 个文件的 `triggers` YAML list，从 description 中提取角色名、别名、关键词。

**轨道 B**：`build_catalog.py` 增加 fallback 逻辑：
```python
import re

def extract_keywords_from_description(desc):
    """从 description 散文中提取触发关键词（fallback 策略）。
    覆盖三种模式：中文引号内角色名/别名、"用于..."列举、"Use when"从句。"""
    keywords = []
    # 规则 1: 中文引号内的角色名/别名（如 "以陈同视角/口吻" → 陈同, 陈同视角）
    for match in re.findall(r'[""]([^""]{2,20})[""]', desc):
        keywords.extend(re.split(r'[/、，,,]', match))
    # 规则 2: "用于..." 后的逗号分隔词（如 "用于广州商绅、髡货代理..."）
    m = re.search(r'用于([^。；]+)', desc)
    if m:
        keywords.extend(re.split(r'[、，,,]', m.group(1)))
    # 规则 3: "Use when" / "当用户要求" 从句中的中文词
    for pat in [r'[Uu]se\s+when\s+(.+?)(?:[.]|\s+不在)', r'当用户要求[“"](.+?)[”"]']:
        for m in re.finditer(pat, desc):
            keywords.extend(re.findall(r'[一-鿿]{2,10}', m.group(1)))
    return list(dict.fromkeys([k.strip() for k in keywords if k.strip()]))  # 去重保序

def extract_triggers(frontmatter):
    triggers = frontmatter.get('triggers', [])
    if not triggers:
        desc = frontmatter.get('description', '')
        triggers = extract_keywords_from_description(desc)
    return triggers
```

`validate_catalog.py` 必须检查每个 entry 是否有非空 triggers，输出 warning 并列出缺失项。

---

## 3. 🔴 关键修复：路径安全

### 3.1 问题

`Path(__file__).resolve().parent.parent.parent` 在脚本被移动/软链接/`python -m` 调用时出错。

### 3.2 修复

```python
def get_skills_root():
    """从当前脚本位置向上找到 SKILLS_ROOT。
    
    安全校验：skills_root 下必须能找到至少一个 *-perspective/ 目录。
    黑名单：跳过 .git/、batches/、lgqm-writing/、__pycache__/。
    """
    script_dir = Path(__file__).resolve().parent  # scripts/
    lgqm_writing = script_dir.parent              # lgqm-writing/
    skills_root = lgqm_writing.parent             # 源仓库或 .claude/skills/
    
    BLACKLIST = {'.git', 'batches', 'lgqm-writing', '__pycache__'}
    
    found = []
    # 三种布局：平铺(安装后) / 分类一级(源仓库) / 分类二级(容错)
    patterns = [
        '*-perspective/SKILL.md',       # depth=0: .claude/skills/beiwei-perspective/SKILL.md
        '*/*-perspective/SKILL.md',     # depth=1: lgqm_roles/元老角色蒸馏/beiwei-perspective/SKILL.md
        '*/*/*-perspective/SKILL.md',   # depth=2: 容错（不推荐但兼容）
    ]
    for pattern in patterns:
        for skill_md in skills_root.glob(pattern):
            parts = set(skill_md.relative_to(skills_root).parts)
            if not parts & BLACKLIST:
                found.append(skill_md.parent)
    
    if not found:
        raise RuntimeError(
            f"Cannot find any *-perspective/ under {skills_root}. "
            f"Place lgqm-writing/ alongside all *-perspective/ directories."
        )
    return skills_root, sorted(set(found))
```

---

## 4. 🔴 关键修复：scenario-mapping 改为领域驱动

### 4.1 问题

`scenario-mapping.md` 硬编码角色名（如 `liuxiang-perspective`），新角色加入后容易遗漏。

### 4.2 修复

`scenario-mapping.md` 不存角色名，**存领域标签**。路由器在运行时通过 `domain-index.md` 动态解析：

```markdown
## 广州治理线
- 领域标签: 广州治理, 警务, 商业, 士绅
- 推荐视角组合: 主视角=广州治理, 次级=警务+商业, 对立面=士绅
- 写作提示: 焦点在城市管理的新旧碰撞

## 雷州糖业线
- 领域标签: 雷州, 工业, 情报, 特种作战
- 推荐视角组合: 主视角=雷州+工业, 暗线=情报+特种作战
```

路由器读取时：`广州治理 → domain-index → [liuxiang, mumin, zhangyunmi, guoyi, gaodi]`。

### 4.3 交叉校验

`build_catalog.py` 生成 catalog 后，对比 `scenario-mapping.md` 引用的领域标签和 `domain-index.md` 中实际存在的标签：
- `[WARNING] scenario-mapping.md references domain 'X' which has no characters`
- `[INFO] New characters not covered by any scenario: aaa, bbb`

---

## 5. 🟡 领域标签推断算法

### 5.1 28 领域 × 关键词映射表

```python
DOMAIN_PATTERNS = {
    "军事": ["特侦", "海军", "步兵", "作战", "登陆", "治安战", "战役", "反游击", "枪械", "船", "舰队", "伏波军", "国民军"],
    "特种作战": ["特侦", "参谋旅行", "行动", "侦察", "菊花屿", "邹和尚庙"],
    "情报": ["情报", "侦查", "渗透", "外情局", "眼线", "线人", "敌工", "广州站", "特务"],
    "政保": ["政保", "政治保卫", "侦查网", "内务安全", "黑色行动"],
    "政治/人事": ["办公厅", "组织部", "人事", "政治", "元老团结", "程序", "计委", "企划院"],
    "广州治理": ["广州", "拆违", "城市治理", "琼山", "佛山", "特别市"],
    "雷州": ["雷州", "糖", "海义堂", "海安街", "徐闻", "华南糖厂"],
    "工业": ["工业化", "蒸汽", "化工", "制糖", "火工", "技改", "计划", "机械"],
    "化工": ["化工", "雷汞", "硝化甘油", "苦味酸", "青蒿素", "药品", "火工", "燃烧瓶"],
    "医疗": ["医院", "防疫", "鼠疫", "外科", "药品", "检疫", "卫生", "百仞总医院"],
    "农业": ["农业", "农庄", "种子", "粮食", "南海", "农林水产", "天地会", "经营地主"],
    "商业": ["商业", "合作社", "百货", "招商", "丝业", "贸易", "糖行", "共同基金", "镖局"],
    "宗教": ["教会", "修道院", "道教", "云笈观", "慈济堂", "新道教", "临高教会"],
    "女性权利": ["女权", "妇联", "女性权利", "女仆"],
    "大明朝廷": ["崇祯", "大明", "皇帝", "朝廷", "阁臣", "首辅", "兵部", "乾清宫"],
    "士绅": ["士绅", "缙绅", "进士", "咨议局", "宗法", "名教", "岭南三忠"],
    "满清": ["后金", "满清", "皇太极", "东虏", "八旗", "辽东"],
    "海军": ["海军", "舰队", "大洋舰队", "伏波军海军", "第一舰队"],
    "山东": ["山东", "据点", "难民", "经略", "发动机行动"],
    "江南": ["江南", "丝业", "凤凰山庄", "招商局", "缙绅"],
    "警务": ["警察", "警务", "治安", "审讯", "户籍", "刑事科", "派出所"],
    "教育": ["芳草地", "教育", "干部学校", "社学", "学习班"],
    "流寇/民变": ["流寇", "闯王", "民变", "不纳粮", "荥阳"],
    "防疫": ["防疫", "鼠疫", "检疫", "隔离", "接触史", "防疫所"],
    "火工/装备": ["雷汞", "硝化甘油", "苦味酸", "特战装备", "燃烧瓶"],
    "难民/收容": ["难民", "收容", "转运", "发动机行动"],
    "海盗/海上": ["海盗", "招抚", "莲花号", "杭州号", "澳门"],
    "宣传/传媒": ["临高时报", "灯塔", "宣传", "新闻", "舆论"],
}
```

### 5.2 领域重叠说明

部分关键词在多个领域间共享（如 `特侦` 同时出现在"军事"和"特种作战"中，`防疫` 同时出现在"医疗"和"防疫"中）。这是**有意为之**——领域标签用于辅助匹配而非精确分类，一个角色属于多个领域是合理的。`validate_catalog.py --test` 的用例包含人工抽查"领域归属合理性"。

### 5.3 匹配逻辑

```python
def infer_domains(frontmatter):
    triggers = extract_triggers(frontmatter)  # 包含 fallback
    description = frontmatter.get('description', '')
    text = ' '.join(triggers + [description])
    domains = []
    for domain, keywords in DOMAIN_PATTERNS.items():
        if any(kw in text for kw in keywords):
            domains.append(domain)
    return domains
```

---

## 6. 🟡 安装流程：install.py

替代原方案中的手写 PowerShell 命令。跨平台（Windows/macOS/Linux），处理编码和路径问题。

```python
#!/usr/bin/env python3
"""install.py — 将 lgqm_roles 安装到 Claude Code skills 目录。"""
import os, sys, shutil
from pathlib import Path

def get_claude_skills_dir():
    home = Path.home()
    return home / '.claude' / 'skills'

def install():
    source_root = Path(__file__).resolve().parent.parent  # 期望是 lgqm_roles/
    target_root = get_claude_skills_dir()
    
    # 校验 source_root 是源仓库根（而非被单独复制到 .claude/skills/ 的 lgqm-writing/）
    category_dirs = ['元老角色蒸馏', '规划民-土著角色蒸馏', '明朝真实历史人物蒸馏']
    if not any((source_root / cat).exists() for cat in category_dirs):
        print(f"ERROR: {source_root} 不是 lgqm_roles 源仓库根目录。", file=sys.stderr)
        print("install.py 必须从 lgqm_roles/lgqm-writing/scripts/ 运行，", file=sys.stderr)
        print("或 lgqm-writing/ 必须位于 lgqm_roles/ 内、与三个分类目录同级。", file=sys.stderr)
        sys.exit(1)
    
    target_root.mkdir(parents=True, exist_ok=True)
    
    # 1. 复制 lgqm-writing/
    shutil.copytree(source_root / 'lgqm-writing', target_root / 'lgqm-writing', dirs_exist_ok=True)
    
    # 2. 平铺复制全部 *-perspective/
    category_dirs = ['元老角色蒸馏', '规划民-土著角色蒸馏', '明朝真实历史人物蒸馏']
    for cat in category_dirs:
        cat_path = source_root / cat
        if cat_path.exists():
            for skill_dir in cat_path.iterdir():
                if skill_dir.is_dir() and skill_dir.name.endswith('-perspective'):
                    shutil.copytree(skill_dir, target_root / skill_dir.name, dirs_exist_ok=True)
    
    print(f"Installed to {target_root}")
    print("Run: python lgqm-writing/scripts/build_catalog.py")
```

---

## 7. 🟡 Workflow 文件格式定义

四个 workflow 文件是 **Markdown 指令文件**，由 `SKILL.md` 通过 `Read` 工具按需加载。格式：

```markdown
# Workflow: [名称]

## Trigger
当路由器分类为 [DIRECT_CHARACTER / SCENARIO_WRITING / MULTI_CHARACTER / LORE_CHECK] 时加载本文件。

## Protocol
1. ...
2. ...

## Output Format
...
```

`SKILL.md` 中的引用方式：
> 如果分类为 SCENARIO_WRITING，**Read [workflows/scenario-recommend.md](workflows/scenario-recommend.md) 并严格按其 Protocol 执行。**

---

## 8. 🟢 增量构建 + 测试矩阵

### 8.1 元数据头

`character-catalog.md` 头部：
```markdown
<!-- GENERATED: 2026-08-02T17:30:00 | files:81 | hash:a1b2c3d4 -->
```

`validate_catalog.py --check` 快速比对 hash，不一致时触发重建。

### 8.2 测试矩阵（`validate_catalog.py --test`）

| 测试类型 | 数量 | 示例 |
|----------|------|------|
| 精确人物名匹配 | 8 | "用北炜的视角" "萧子山会怎么处理" |
| 别名/外号匹配 | 5 | "督公怎么看" "杜女王" "石翁" "江局" |
| 领域/地点匹配 | 8 | "雷州糖厂" "广州站" "临高教会" "山东基地" |
| 事件/情节匹配 | 6 | "女仆案" "唐僧计划" "发动机行动" |
| 模糊/多义输入 | 5 | "写一场战斗" "商业谈判" "防疫" |
| 无匹配输入 | 3 | "架空兵器" "外星人" "无关话题" |

---

## 9. 调整后的文件估算

| 文件 | 估算 | 说明 |
|------|------|------|
| `SKILL.md` | ~450 行 | 4 phase 路由协议 + fallback 策略 + 调用协议 |
| `build_catalog.py` | ~300 行 | 双格式兼容 + 领域推断 + 交叉校验 + 增量构建 |
| `validate_catalog.py` | ~150 行 | completeness check + triggers 非空 + --test 矩阵 |
| `install.py` | ~60 行 | 跨平台安装 |
| `character-catalog.md` | ~500 行 | 自动生成 |
| `domain-index.md` | ~80 行 | 自动生成 |
| `scenario-mapping.md` | ~150 行 | 领域标签驱动 |
| `writing-principles.md` | ~80 行 | 手动 |
| `workflows/*.md` × 5 | ~50 行/个 | 含新增 fallback.md |

---

## 10. 实现步骤（修订）

| Step | 内容 | 审计关联 |
|------|------|----------|
| **0** | **补齐 7 个缺失 triggers 的 SKILL.md** | 🔴 #1 |
| 1 | 创建 `lgqm-writing/{references,scripts,workflows}/` | — |
| 2 | 编写 `build_catalog.py`（含 fallback + 安全路径 + 领域推断 + 交叉校验 + 增量元数据） | 🔴 #1 #2 #6, 🟡 #6, 🟢 #8 |
| 3 | 运行 `build_catalog.py`，生成 `character-catalog.md` + `domain-index.md` | — |
| 4 | 编写 `scenario-mapping.md`（领域标签驱动，非硬编码角色名） | 🔴 #3 |
| 5 | 编写 `writing-principles.md` | — |
| 6 | 编写 `SKILL.md`（含完整 fallback 策略） | 🟡 #4 |
| 7 | 编写 5 个 workflow 文件（含 fallback.md） | 🟡 #7 |
| 8 | 编写 `validate_catalog.py`（含 --test 30+ 用例） | 🟡 #9 |
| 9 | 编写 `install.py` | 🟡 #5 |
| 10 | 运行 `validate_catalog.py --test`，验证匹配准确率 ≥ 90% | 🟡 #9 |
| 11 | 编写 README 安装说明 | — |

---

## 11. 需要修改的现有文件

| 文件 | 修改内容 |
|------|----------|
| `规划民-土著角色蒸馏/chentong-perspective/SKILL.md` | 补齐 `triggers` YAML list |
| `规划民-土著角色蒸馏/dongmingdang-perspective/SKILL.md` | 补齐 `triggers` |
| `规划民-土著角色蒸馏/gaoju-perspective/SKILL.md` | 补齐 `triggers` |
| `规划民-土著角色蒸馏/liluoyou-perspective/SKILL.md` | 补齐 `triggers` |
| `规划民-土著角色蒸馏/limo-perspective/SKILL.md` | 补齐 `triggers` |
| `规划民-土著角色蒸馏/mapeng-perspective/SKILL.md` | 补齐 `triggers` |
| `规划民-土著角色蒸馏/wangzhaomin-perspective/SKILL.md` | 补齐 `triggers` |
| `README.md` | 添加 lgqm-writing 安装说明 |

## 12. 验证标准

1. `build_catalog.py` 在源仓库（分类布局）下正确发现全部 81 个 *-perspective/
2. **平铺布局专项测试**：模拟安装后布局（全部 `*-perspective/` 平铺在 skills_root 下，无分类目录），`build_catalog.py` 必须返回全部 81 个角色，且角色名**不包含**分类目录名作为前缀（如 `元老角色蒸馏/beiwei-perspective` 这类路径在平铺布局下不应再出现）
3. `validate_catalog.py --check` 全部通过（triggers 非空、目录完整）
4. `validate_catalog.py --test` 通过率 ≥ 90%（30+ 用例）
5. `install.py` 在新机器上成功安装并运行 `build_catalog.py`；在非源仓库位置运行时输出清晰的错误信息而非静默失败
6. 路由器对 5 个手工测试 prompt 返回正确的 top-3 推荐

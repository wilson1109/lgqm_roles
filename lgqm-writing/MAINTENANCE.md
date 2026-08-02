# lgqm-writing 维护手册

> 版本：2026-08-02 | 适用 skill：`lgqm-writing/`
> 本手册说明如何**新增、更新、移除角色 skill**，以及常见问题的排查方法。

---

## 0. 架构速览：哪些自动、哪些手动

| 组件 | 生成方式 | 何时需要动它 |
|------|----------|--------------|
| `references/character-catalog.md` | 自动（build_catalog.py） | 永远**不要**手改，重跑脚本即更新 |
| `references/domain-index.md` | 自动（build_catalog.py） | 永远**不要**手改 |
| `references/scenario-mapping.md` | 手动 | 新增角色涉及**新场景/新领域**时才改 |
| `references/writing-principles.md` | 手动 | 写作规范有变化时 |
| `SKILL.md` | 手动 | 路由协议变化时（新增角色**通常不需要**动） |
| `scripts/*.py` | 手动 | 脚本本身 bug 或功能增强时 |
| `workflows/*.md` | 手动 | 处理流程变化时 |

**核心结论**：新增角色时，唯一可能的手动工作是改 `scenario-mapping.md`，其余全部由 `build_catalog.py` 自动完成。

---

## 1. 新增角色完整流程

### Step 1: 准备角色 skill 目录

复制 `*-perspective/` 目录到对应的分类目录：

```text
lgqm_roles/
├── 元老角色蒸馏/           # ← 元老角色
├── 规划民-土著角色蒸馏/      # ← 归化民/土著
└── 明朝真实历史人物蒸馏/      # ← 明朝历史人物
```

> 也可以直接用 nuwa-skill 蒸馏生成，再放到分类目录。

### Step 2: 检查 SKILL.md frontmatter

`SKILL.md` 的 YAML frontmatter **必须**包含三项（`triggers` 尤其重要）：

```yaml
---
name: new-character-perspective
description: 角色简介 + 触发说明。基于《临高启明》第X卷原文蒸馏，含7个心智模型、8条决策启发式。
triggers:
  - 新角色名
  - 别名
  - 组织名
  - 标志性概念
---
```

**frontmatter 规范：**

| 字段 | 要求 | 说明 |
|------|------|------|
| `name` | 必填 | 与目录名一致（`xxx-perspective`） |
| `description` | 必填 | 角色简介 + 触发语；建议标注"基于…蒸馏，含X个心智模型" |
| `triggers` | **必填** | YAML list。缺失时脚本会 fallback 从 description 提取，但匹配质量会下降 |

**triggers 应该包含哪几类关键词？**

| 类型 | 示例 |
|------|------|
| 角色名/别名/外号 | 北炜、杜女王、督公、石翁 |
| 官职/身份 | 海军部长、临高县令、特侦队长 |
| 组织名 | 广州站、临高教会、起威镖局 |
| 标志性概念/方法 | 工分、十面张网、共同基金、天书 |
| 主题领域 | 鼠疫、西法火器、女权、镖局 |
| 关联人物 | 徐光启（孙元化的触发器）、李丝雅（李默的触发器） |
| 拼音/英文 | beiwei、guoyi、chongzhen |

**反面示例（会降低匹配质量）：**
```yaml
triggers:
  - 角色          # ❌ 太泛，"角色"会误触发
  - 写作          # ❌ 不属于本角色专属
  - 工业          # ❌ 太泛，多个工业角色共享
```

### Step 3: 正文 `# 标题` 必须可提取角色名

> **这一步只需编辑角色的 SKILL.md 文件，不需要运行任何命令。** 运行脚本是 Step 4 的事。

角色 SKILL.md 正文的第一行 `# 标题` 会被 `build_catalog.py` 用来提取角色中文名（写入 catalog 并参与匹配），所以格式必须能从中识别出角色名：

```markdown
# 张三丰 · 思维操作系统    ← ✅ 会提取出"张三丰"
# 张三丰 Perspective        ← ✅ 会提取出"张三丰"
# 张三丰（张真人）· 思维操作系统  ← ✅ 会提取出"张三丰"（忽略括号）
# 武当山 视角              ← ❌ 没有角色名，提取会失败
```

> 标题建议格式：`# 角色名 · 可选说明`（`·` 前后用空格）。编辑完保存即可，无需运行命令。

### Step 4: 重建 catalog

**PowerShell**
```powershell
Set-Location "E:\AI_project\lgqm_roles"
python lgqm-writing\scripts\build_catalog.py
```

**Bash**
```bash
cd lgqm_roles
python lgqm-writing/scripts/build_catalog.py
```

预期输出：
```text
Wrote: lgqm-writing/references/character-catalog.md (82 characters)   ← 比之前 +1
Wrote: lgqm-writing/references/domain-index.md (28 domains)
Done: 82 characters from E:\AI_project\lgqm_roles
```

**如果总数没变**，说明新角色没被扫描到——见第 5 节「常见问题」。

### Step 5: 验证

**PowerShell**
```powershell
python lgqm-writing\scripts\validate_catalog.py --check
# CHECK: 82 skills, 0 errors, 0 warnings   ← 期望 0 errors

python lgqm-writing\scripts\validate_catalog.py --test
# TEST: 35/35 passed (100%)                ← 期望通过率不下降
```

**Bash**
```bash
python lgqm-writing/scripts/validate_catalog.py --check
# CHECK: 82 skills, 0 errors, 0 warnings   ← 期望 0 errors

python lgqm-writing/scripts/validate_catalog.py --test
# TEST: 35/35 passed (100%)                ← 期望通过率不下降
```

### Step 6: 更新 scenario-mapping（仅当涉及新场景/新领域）

如果新角色带来了**新的故事线类型**（如新加入一个"台湾线"角色，而 scenario-mapping 没有"台湾"场景），则：

1. 打开 `lgqm-writing/references/scenario-mapping.md`
2. 确认新角色的领域标签是否已有对应场景；没有则新增：

```markdown
### 台湾线（示例）
- 领域标签: 大明朝廷, 军事, 商业
- 推荐视角组合: 主视角=大明朝廷, 次级=商业, 对立面=军事
- 写作提示: ...
```

> `build_catalog.py` 运行时会自动交叉校验 scenario-mapping 引用的领域，输出 `[WARNING]` 提示缺失。**如果 warning 里出现你新角色的领域但没写场景**，说明该补 scenario 了。

### Step 7: 打包发布

**PowerShell**
```powershell
# 重新打包分发包（如有 zip 约定）
Set-Location "E:\AI_project\lgqm_roles"
python -m zipfile -c "新角色-perspective.zip" "分类目录\新角色-perspective\"
```

**Bash**
```bash
# 重新打包分发包（如有 zip 约定）
cd lgqm_roles
python -m zipfile -c "新角色-perspective.zip" "分类目录/新角色-perspective/"
```

---

## 2. 批量新增角色

一次加入多个角色时，把全部目录放进分类目录后**只跑一次** `build_catalog.py`：

**PowerShell**
```powershell
python lgqm-writing\scripts\build_catalog.py
```

**Bash**
```bash
python lgqm-writing/scripts/build_catalog.py
```

脚本自动扫描全部，无需逐个处理。批量后检查 catalog 数量是否等于「原有 + 新增」。

---

## 3. 更新已有角色

修改角色的 `SKILL.md`（触发词、描述、正文）后：

**PowerShell**
```powershell
python lgqm-writing\scripts\build_catalog.py   # 重新生成 catalog
python lgqm-writing\scripts\validate_catalog.py --check   # 确认无回归
```

**Bash**
```bash
python lgqm-writing/scripts/build_catalog.py   # 重新生成 catalog
python lgqm-writing/scripts/validate_catalog.py --check   # 确认无回归
```

如果修改了 `triggers`，建议补一条匹配测试用例（见第 4 节）。

---

## 4. 维护测试用例

测试用例在 `lgqm-writing/scripts/validate_catalog.py` 的 `TEST_CASES` 列表中。新增/修改角色后，为它补充 1-2 条用例：

```python
TEST_CASES = [
    # ... 现有用例 ...
    ("用张三丰视角看武当山建设", {'张三丰'}, "新角色点名"),
    ("写武当山道观经营", {'张三丰', '吴石芒'}, "新角色+宗教"),
]
```

测试逻辑：对每条用例，把用户输入与全部角色匹配，要求**期望角色至少命中 top-3**。

- `expected_names` 填角色的中文名（就是 `# 标题` 提取的那个名字）
- 无匹配用例填 `None`（用于验证"不该误触发"的情况）

---

## 5. 常见问题排查

### Q1: build_catalog.py 扫描不到新角色

**现象**：跑完脚本角色总数没变。

**排查**（先切到 lgqm_roles 目录）：

**PowerShell**
```powershell
Set-Location "E:\AI_project\lgqm_roles"
$env:PYTHONIOENCODING = "utf-8"
python -c "import sys; sys.path.insert(0, 'lgqm-writing/scripts'); import build_catalog as bc; _, found = bc.get_skills_root(); print(f'扫描到 {len(found)} 个目录'); print([str(p) for p in found if '新角色' in str(p)])"
# 检查完恢复环境变量
Remove-Item Env:PYTHONIOENCODING
```

**Bash**
```bash
cd lgqm_roles
PYTHONIOENCODING=utf-8 python -c "
import sys; sys.path.insert(0, 'lgqm-writing/scripts')
import build_catalog as bc
_, found = bc.get_skills_root()
print(f'扫描到 {len(found)} 个目录')
print([str(p) for p in found if '新角色' in str(p)])  # 检查新角色是否在列
"
```

**可能原因**：
- 目录名不以 `-perspective` 结尾 → 改目录名
- 缺少 `SKILL.md` 或 frontmatter 解析失败 → 检查 YAML 语法
- 目录在 `_BLACKLIST` 里（`.git`/`batches`/`lgqm-writing`/`__pycache__`）→ 移出这些目录
- `lgqm-writing/` 不在三个分类目录的**同级** → 检查目录布局

### Q2: catalog 中角色名是"未知"或提取错误

**原因**：`# 标题` 里没有可提取的角色名。

**修复**：把正文标题改成 `# 角色名 · 说明` 格式，重跑 `build_catalog.py`。

### Q3: 领域标签不合理（太多/太少/错误）

**原因**：领域由 `build_catalog.py` 里 `DOMAIN_PATTERNS` 关键词表推断，靠 triggers + description 匹配。

**排查**：

**PowerShell**
```powershell
$env:PYTHONIOENCODING = "utf-8"
python -c "import sys; sys.path.insert(0, 'lgqm-writing/scripts'); import build_catalog as bc; _, all_chars, _ = bc.scan_all(); print(all_chars['新角色-perspective']['domains'])"
Remove-Item Env:PYTHONIOENCODING
```

**Bash**
```bash
PYTHONIOENCODING=utf-8 python -c "
import sys; sys.path.insert(0, 'lgqm-writing/scripts')
import build_catalog as bc
_, all_chars, _ = bc.scan_all()
print(all_chars['新角色-perspective']['domains'])
"
```

**修复**：
- 在 `triggers` 里加入该领域的关键词（推荐）
- 或调整 `DOMAIN_PATTERNS`（但会影响所有角色，慎改）

### Q4: validate --test 通过率下降

**原因**：新增角色带走了某测试用例的期望命中，或触发了误匹配。

**修复**：

**PowerShell**
```powershell
$env:PYTHONIOENCODING = "utf-8"
python lgqm-writing\scripts\validate_catalog.py --test
Remove-Item Env:PYTHONIOENCODING
```

**Bash**
```bash
PYTHONIOENCODING=utf-8 python lgqm-writing/scripts/validate_catalog.py --test
```
看输出中失败的用例，在 `TEST_CASES` 里补充/调整期望。

### Q5: install.py 报"不是源仓库根目录"

**原因**：`lgqm-writing/` 被单独复制走了，不在 `lgqm_roles/` 内。

**修复**：把 `lgqm-writing/` 放回 `lgqm_roles/` 内（与三个分类目录同级）再运行。

### Q6: 新角色 skill 被 Claude 触发但路由器没调用它

**现象**：直接说角色名能触发角色 skill，但 `lgqm-writing` 路由没匹配到。

**原因**：路由器匹配依赖 `character-catalog.md`，该文件是**快照**。新角色加入后未重跑 `build_catalog.py`。

**修复**：重跑 `python lgqm-writing/scripts/build_catalog.py`。

---

## 6. 命令速查

**PowerShell**（在 lgqm_roles 目录下）

```powershell
# 重建 catalog（新增/更新角色后必跑）
python lgqm-writing\scripts\build_catalog.py

# 只校验不写文件（CI 用）
python lgqm-writing\scripts\build_catalog.py --check

# 完整性校验
python lgqm-writing\scripts\validate_catalog.py --check

# 匹配测试矩阵
python lgqm-writing\scripts\validate_catalog.py --test

# 一键安装到 $HOME\.claude\skills\
python lgqm-writing\scripts\install.py

# 安装到自定义目录
python lgqm-writing\scripts\install.py --dir "C:\path\to\skills"
```

**Bash**（在 lgqm_roles 目录下）

```bash
# 重建 catalog（新增/更新角色后必跑）
python lgqm-writing/scripts/build_catalog.py

# 只校验不写文件（CI 用）
python lgqm-writing/scripts/build_catalog.py --check

# 完整性校验
python lgqm-writing/scripts/validate_catalog.py --check

# 匹配测试矩阵
python lgqm-writing/scripts/validate_catalog.py --test

# 一键安装到 ~/.claude/skills/
python lgqm-writing/scripts/install.py

# 安装到自定义目录
python lgqm-writing/scripts/install.py --dir PATH
```

---

## 7. 新增角色 Checklist

```markdown
- [ ] SKILL.md frontmatter 含 name/description/triggers
- [ ] triggers 包含角色名、别名、组织、概念、主题、关联人物
- [ ] 正文 # 标题格式为「角色名 · 说明」
- [ ] 目录放入正确的分类目录
- [ ] 目录名以 -perspective 结尾
- [ ] 运行 build_catalog.py，确认 catalog 数量 +1
- [ ] 运行 validate_catalog.py --check，0 errors
- [ ] 运行 validate_catalog.py --test，通过率不下降
- [ ] （如需）更新 scenario-mapping.md 补场景
- [ ] （建议）在 TEST_CASES 补 1-2 条用例
- [ ] （发布时）重新打包 zip
```

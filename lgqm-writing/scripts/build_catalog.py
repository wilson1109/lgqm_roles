#!/usr/bin/env python3
"""build_catalog.py — 自动生成 character-catalog.md 和 domain-index.md。

扫描所有 *-perspective/SKILL.md 的 frontmatter，提取角色名、触发词、领域标签，
生成路由器所需的两个索引文件。

用法:
    python build_catalog.py            # 构建（默认）
    python build_catalog.py --check     # 校验模式，不写文件

可移植性:
    - 零绝对路径：基于 __file__ 计算 skills_root
    - 兼容两种布局：平铺（安装后）与分类目录（源仓库）
    - 兼容两种 frontmatter：独立 triggers 字段 或 嵌入 description
"""
import re
import sys
import yaml
import hashlib
import datetime
from pathlib import Path
from collections import defaultdict

# 领域关键词映射表（辅助匹配，允许一个角色多领域）
DOMAIN_PATTERNS = {
    "军事": ["特侦", "海军", "步兵", "作战", "战斗", "攻略", "登陆", "治安战", "战役", "反游击", "枪械", "船", "舰队", "伏波军", "国民军"],
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

# 跳过非角色目录
BLACKLIST = {'.git', 'batches', 'lgqm-writing', '__pycache__'}


def get_skills_root():
    """从当前脚本位置向上找到 SKILLS_ROOT。

    安全校验：skills_root 下必须能找到至少一个 *-perspective/ 目录。
    黑名单：跳过 .git/、batches/、lgqm-writing/、__pycache__/。
    """
    script_dir = Path(__file__).resolve().parent       # scripts/
    lgqm_writing = script_dir.parent                    # lgqm-writing/
    skills_root = lgqm_writing.parent                   # 源仓库或 .claude/skills/

    found = find_perspective_dirs(skills_root)
    if not found:
        raise RuntimeError(
            f"Cannot find any *-perspective/ under {skills_root}. "
            f"Place lgqm-writing/ alongside all *-perspective/ directories."
        )
    return skills_root, found


def find_perspective_dirs(skills_root):
    """发现所有 *-perspective/ 目录，兼容平铺与分类布局。"""
    found = []
    patterns = [
        '*-perspective/SKILL.md',       # depth=0: 平铺（安装后布局）
        '*/*-perspective/SKILL.md',     # depth=1: 分类目录（源仓库布局）
        '*/*/*-perspective/SKILL.md',   # depth=2: 容错
    ]
    for pattern in patterns:
        for skill_md in skills_root.glob(pattern):
            parts = set(skill_md.relative_to(skills_root).parts)
            if not parts & BLACKLIST:
                found.append(skill_md.parent)
    return sorted(set(found))


def parse_frontmatter(filepath):
    """从 SKILL.md 提取 YAML frontmatter。"""
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        content = filepath.read_text(encoding='gbk', errors='replace')
    if not content.startswith('---'):
        return {}
    end = content.find('\n---', 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[3:end]) or {}
    except yaml.YAMLError:
        return {}


def extract_keywords_from_description(desc):
    """从 description 散文中提取触发关键词（fallback 策略）。

    覆盖三种模式：中文引号内角色名/别名、"用于..."列举、"Use when"从句。
    """
    keywords = []
    # 规则 1: 中文引号内的角色名/别名
    for match in re.findall(r'["“”]([^"“”]{2,20})["“”]', desc):
        keywords.extend(re.split(r'[/、，,，]', match))
    # 规则 2: "用于..." 后的分隔词
    m = re.search(r'用于([^。；]+)', desc)
    if m:
        keywords.extend(re.split(r'[、，,，]', m.group(1)))
    # 规则 3: "Use when"/"当用户要求" 从句中的中文词
    for pat in [r'[Uu]se\s+when\s+(.+?)(?:[.]|\s+不在)', r'当用户要求["“”](.+?)["“”]']:
        for m in re.finditer(pat, desc):
            keywords.extend(re.findall(r'[一-鿿]{2,10}', m.group(1)))
    return list(dict.fromkeys(k.strip() for k in keywords if k.strip()))


def extract_triggers(frontmatter):
    """提取触发词，triggers 字段缺失时从 description fallback。"""
    triggers = frontmatter.get('triggers', []) or []
    if not triggers:
        desc = frontmatter.get('description', '')
        triggers = extract_keywords_from_description(desc)
    return triggers


def infer_domains(frontmatter, triggers):
    """从 triggers + description 推断领域标签。"""
    text = ' '.join(triggers + [frontmatter.get('description', '')])
    domains = []
    for domain, keywords in DOMAIN_PATTERNS.items():
        if any(kw in text for kw in keywords):
            domains.append(domain)
    return domains


def extract_character_name(skill_md_path, description):
    """从 SKILL.md 正文 # 标题提取角色中文名。

    标题格式多样，按优先级处理：
      1. # 陈同 · 思维操作系统        → 陈同
      2. # 崇祯皇帝 · 思维操作系统      → 崇祯皇帝
      3. # 北炜 Perspective            → 北炜
      4. # 刘大霖（孟良） · 思维操作系统 → 刘大霖
      5. # 朱鸣夏 · 训练政工与治安战 Perspective → 朱鸣夏
    """
    try:
        content = skill_md_path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError):
        content = skill_md_path.read_text(encoding='gbk', errors='replace')
    for line in content.splitlines():
        if line.startswith('# '):
            title = line[2:].strip()
            # 去括号注记：刘大霖（孟良）→ 刘大霖
            title = re.sub(r'[（(].*?[）)]', '', title)
            # 按 ·、|、｜ 截断，取第一段
            title = re.split(r'[·|｜]', title)[0].strip()
            # 去掉英文/视角后缀
            title = re.sub(r'\s*(Perspective|perspective|视角)$', '', title).strip()
            if title and len(title) <= 8:
                return title
            break
    # fallback: description 开头处的角色名
    m = re.search(r'[一-鿿]{2,6}', description or '')
    if m:
        return m.group(0)
    return '未知'


def compute_hash(all_chars):
    """计算 catalog 的稳定 hash，用于增量校验。"""
    h = hashlib.md5()
    for key in sorted(all_chars):
        h.update(key.encode('utf-8'))
        h.update(str(all_chars[key]).encode('utf-8'))
    return h.hexdigest()[:8]


def scan_all():
    """扫描全部角色，返回 skills_root + 角色数据。"""
    skills_root, skill_dirs = get_skills_root()
    all_chars = {}
    warnings = []
    for skill_dir in skill_dirs:
        skill_md = skill_dir / 'SKILL.md'
        if not skill_md.exists():
            warnings.append(f"[WARNING] 缺少 SKILL.md: {skill_dir}")
            continue
        fm = parse_frontmatter(skill_md)
        if not fm:
            warnings.append(f"[WARNING] 无法解析 frontmatter: {skill_dir}")
            continue
        skill_name = skill_dir.name
        triggers = extract_triggers(fm)
        if not triggers:
            warnings.append(f"[WARNING] 无触发词: {skill_name}")
        desc = fm.get('description', '')
        all_chars[skill_name] = {
            'name': skill_name.replace('-perspective', ''),
            'character_name': extract_character_name(skill_md, desc),
            'description': desc,
            'triggers': triggers,
            'domains': infer_domains(fm, triggers),
            'path': str(skill_dir),
        }
    return skills_root, all_chars, warnings


def generate_catalog_md(all_chars, out_path):
    """生成 character-catalog.md。"""
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    h = compute_hash(all_chars)
    lines = [
        '# 临高启明角色目录 (Character Catalog)',
        '',
        f'> 自动生成于 {now} | 共 {len(all_chars)} 角色 | hash: {h}',
        f'> 生成命令: python lgqm-writing/scripts/build_catalog.py',
        '',
        '## 目录索引',
        '',
    ]
    # 按领域聚类快速索引
    domain_chars = defaultdict(list)
    for skill_name, data in all_chars.items():
        for d in data['domains']:
            domain_chars[d].append(data['name'])
    for d in sorted(domain_chars):
        lines.append(f"- **{d}**: {', '.join(sorted(set(domain_chars[d])))}")
    lines.append('')
    lines.append('---')
    lines.append('')
    # 按 skill 名排序逐条列出
    for skill_name in sorted(all_chars):
        data = all_chars[skill_name]
        lines.append(f"## {skill_name}")
        lines.append(f"- **角色名**: {data['character_name']}")
        lines.append(f"- **Skill 名**: {data['name']}")
        if data['triggers']:
            trig_show = data['triggers'][:20]
            lines.append(f"- **触发词** ({len(data['triggers'])}): {', '.join(trig_show)}")
        if data['domains']:
            lines.append(f"- **领域**: {', '.join(data['domains'])}")
        lines.append(f"- **路径**: {data['path']}")
        lines.append('')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Wrote: {out_path} ({len(all_chars)} characters)")


def generate_domain_index(all_chars, out_path):
    """生成 domain-index.md。"""
    domain_chars = defaultdict(list)
    for skill_name, data in all_chars.items():
        for d in data['domains']:
            domain_chars[d].append(data['name'])
    lines = [
        '# 领域索引 (Domain Index)',
        '',
        f'> 自动生成 | {len(domain_chars)} 个领域',
        '',
        '| 领域 | 关联角色技能 |',
        '|---|---|',
    ]
    for domain in sorted(domain_chars):
        chars = ', '.join(sorted(set(domain_chars[domain])))
        lines.append(f"| {domain} | {chars} |")
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Wrote: {out_path} ({len(domain_chars)} domains)")


def cross_check_scenario_mapping(all_chars, scenario_path):
    """交叉校验 scenario-mapping.md 引用的领域 vs 实际领域。"""
    if not scenario_path.exists():
        print("[INFO] scenario-mapping.md 不存在，跳过交叉校验")
        return
    text = scenario_path.read_text(encoding='utf-8')
    domains_in_scenario = set()
    for line in text.splitlines():
        if '领域' in line and ':' in line:
            parts = line.split(':', 1)[1]
            for d in parts.replace('，', ',').replace('、', ',').split(','):
                d = d.strip()
                if d:
                    domains_in_scenario.add(d)
    actual_domains = set()
    for data in all_chars.values():
        actual_domains.update(data['domains'])
    missing = domains_in_scenario - actual_domains
    for d in sorted(missing):
        print(f"[WARNING] scenario-mapping.md 引用领域 '{d}'，但无角色匹配该领域")
    uncovered = actual_domains - domains_in_scenario
    for d in sorted(uncovered):
        print(f"[INFO] 领域 '{d}' 暂无对应场景条目")


def main():
    check_only = '--check' in sys.argv
    skills_root, all_chars, warnings = scan_all()

    for w in warnings:
        print(w)

    if check_only:
        n_ok = sum(1 for d in all_chars.values() if d['triggers'])
        print(f"CHECK: {n_ok}/{len(all_chars)} skills have triggers")
        sys.exit(0 if n_ok == len(all_chars) else 1)

    ref_dir = Path(__file__).resolve().parent.parent / 'references'
    ref_dir.mkdir(parents=True, exist_ok=True)

    generate_catalog_md(all_chars, ref_dir / 'character-catalog.md')
    generate_domain_index(all_chars, ref_dir / 'domain-index.md')
    cross_check_scenario_mapping(all_chars, ref_dir / 'scenario-mapping.md')

    print(f"Done: {len(all_chars)} characters from {skills_root}")


if __name__ == '__main__':
    main()

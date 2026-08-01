#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
required = [
    "SKILL.md",
    "references/research/01-writings.md",
    "references/research/02-conversations.md",
    "references/research/03-expression-dna.md",
    "references/research/04-external-views.md",
    "references/research/05-decisions.md",
    "references/research/06-timeline.md",
    "references/sources/SOURCE_INDEX.md",
]

errors = []
for rel in required:
    path = root / rel
    if not path.exists():
        errors.append(f"missing {rel}")
        continue
    minimum = 8000 if rel == "SKILL.md" else 1500 if rel.endswith("SOURCE_INDEX.md") else 900
    if path.stat().st_size < minimum:
        errors.append(f"{rel} too small: {path.stat().st_size} < {minimum}")

if errors:
    print("FAIL")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

skill = (root / "SKILL.md").read_text(encoding="utf-8")
source = (root / "references/sources/SOURCE_INDEX.md").read_text(encoding="utf-8")
research = "\n".join(
    (root / f"references/research/0{i}-{name}.md").read_text(encoding="utf-8")
    for i, name in [
        (1, "writings"),
        (2, "conversations"),
        (3, "expression-dna"),
        (4, "external-views"),
        (5, "decisions"),
        (6, "timeline"),
    ]
)

skill_needles = [
    "name: lucheng-perspective",
    "# 陆橙 · 思维操作系统",
    "陆澄（常见误写）",
    "角色扮演规则",
    "回答工作流（Agentic Protocol）",
    "证据分级纪律",
    "核心心智模型",
    "决策启发式",
    "表达 DNA",
    "人物时间线",
    "价值观与反模式",
    "诚实边界",
    "Smoke Prompts",
    "陆小娘",
    "姚玉兰",
    "柯云",
    "黄安德",
    "财税",
    "琼山县",
    "刘翔",
    "广州市妇联主任",
    "济良所",
    "卞翠宝",
    "杜易斌",
    "张允幂",
    "广州风俗业情况初步调查报告",
    "袁舒知",
    "郑逍余",
    "郑明姜",
    "万春全",
    "聚宝堂",
    "假币",
    "会道门",
    "不完美的结局",
    "偏见并未消失",
    "不能把政治案件当作纪律工具",
]
errors += [f"SKILL.md missing {needle}" for needle in skill_needles if needle not in skill]

if skill.count("### 模型") < 7:
    errors.append("SKILL.md has fewer than 7 mental models")
if len(re.findall(r"^\d+\. \*\*", skill, re.M)) < 8:
    errors.append("SKILL.md has fewer than 8 decision heuristics")
if skill.startswith("---") is False:
    errors.append("SKILL.md missing YAML frontmatter")
if "# 陆澄 ·" in skill:
    errors.append("陆澄 must not replace the canonical title 陆橙")

source_needles = [
    "原著规范名",
    "陆橙",
    "陆澄",
    "来源纪律",
    "第三卷 新社会.md",
    "第五卷 进入.md",
    "第七卷 大陆-广州治理篇.md",
    "第八卷 深耕经营(上).md",
    "济良所",
    "聚宝堂",
    "不完美的结局",
]
errors += [f"SOURCE_INDEX.md missing {needle}" for needle in source_needles if needle not in source]
if source.count("| 第") < 22:
    errors.append("SOURCE_INDEX.md has fewer than 22 original-text anchors")

research_needles = [
    "本轮按崇祯范本重修",
    "原著规范名为“陆橙”",
    "妇联",
    "济良所",
    "卞翠宝",
    "袁舒知",
    "聚宝堂",
    "偏见",
    "边界",
]
errors += [f"research missing {needle}" for needle in research_needles if needle not in research]

banned = [
    "袁淑芝",
    "郑小玉",
    "TODO",
    "TBD",
]
full_text = skill + "\n" + source + "\n" + research
errors += [f"banned artifact remains: {item}" for item in banned if item in full_text]

if errors:
    print("FAIL")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("PASS", root.name)

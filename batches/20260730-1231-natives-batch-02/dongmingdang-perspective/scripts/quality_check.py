#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
required_files = [
    "SKILL.md",
    "references/research/01-writings.md",
    "references/research/02-conversations.md",
    "references/research/03-expression-dna.md",
    "references/research/04-external-views.md",
    "references/research/05-decisions.md",
    "references/research/06-timeline.md",
    "references/sources/SOURCE_INDEX.md",
]

failures = []


def read(rel: str) -> str:
    path = root / rel
    if not path.exists():
        failures.append(f"missing file: {rel}")
        return ""
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 500:
        failures.append(f"file too small: {rel}")
    return text


texts = {rel: read(rel) for rel in required_files}
skill = texts["SKILL.md"]
source = texts["references/sources/SOURCE_INDEX.md"]

# Frontmatter must stay compact and predictable for discovery.
if not skill.startswith("---\n"):
    failures.append("SKILL.md missing YAML frontmatter")
else:
    try:
        _, fm, _body = skill.split("---\n", 2)
    except ValueError:
        failures.append("SKILL.md malformed YAML frontmatter")
    else:
        keys = []
        for line in fm.splitlines():
            if line.strip() and not line.startswith(" ") and ":" in line:
                keys.append(line.split(":", 1)[0].strip())
        if set(keys) != {"name", "description"}:
            failures.append(f"frontmatter keys must be name/description only, got {keys}")
        if "name: dongmingdang-perspective" not in fm:
            failures.append("frontmatter name must be dongmingdang-perspective")
        desc = " ".join(
            line for line in fm.splitlines()
            if line.startswith("description:") or line.startswith("  ")
        )
        if len(desc) > 1024:
            failures.append("frontmatter description exceeds 1024 chars")

required_sections = [
    "角色扮演规则",
    "回答工作流",
    "身份卡",
    "核心心智模型",
    "决策启发式",
    "表达 DNA",
    "人物时间线",
    "价值观与内部张力",
    "诚实边界",
    "来源附录",
    "Smoke Prompts",
]
for section in required_sections:
    if section not in skill:
        failures.append(f"SKILL.md missing section: {section}")

# Seven models, each with evidence, application and failure boundary.
model_blocks = re.findall(
    r"^### 模型\d：.*?(?=^### 模型\d：|^---\n|\Z)",
    skill,
    flags=re.M | re.S,
)
if len(model_blocks) != 7:
    failures.append(f"expected 7 mental models, got {len(model_blocks)}")
for i, block in enumerate(model_blocks, 1):
    for field in ["**一句话：**", "**来源证据：**", "**应用方式：**", "**局限性：**"]:
        if field not in block:
            failures.append(f"model {i} missing field {field}")

required_phrases = [
    "原文明示",
    "可证推断",
    "未知",
    "广州治理篇 135 次、两广攻略篇 2 次、第八卷 1 次，共 138 次",
    "“董明铛”仅作异名/误写入口",
    "原著正文主名为“董明珰”",
    "十五六岁",
    "白色贴纸",
    "2 级以上",
    "蓝色贴纸",
    "董家铺子当时不具备德隆贷款申请门槛",
    "流言带来客流是旁白与他者判断",
    "郑尚洁仅由他人转述提及",
    "原文没有写实际发文过程",
    "第八卷",
]
for phrase in required_phrases:
    if phrase not in skill:
        failures.append(f"SKILL.md missing required phrase: {phrase}")

for forbidden in [
    "正名用“董明珰”",
    "刘翔给她文书与生计边界",
    "把“犯官小姐”的危险名声改造成能招徕客流的招牌",
    "裴丽秀、郑尚洁、张筱奇把她看作“可造之才”",
    "她与李子玉的关系停留在暧昧、互相利用",
    "卫生许可证、营业执照",
]:
    if forbidden in skill:
        failures.append(f"unsafe wording remains in SKILL.md: {forbidden}")

# Research files must preserve evidence levels rather than flattening inference into fact.
for rel in required_files[1:-1]:
    text = texts[rel]
    for phrase in ["证据等级", "原文明示", "可证推断", "未知"]:
        if phrase not in text:
            failures.append(f"{rel} missing evidence marker: {phrase}")

# Source index: canonical corpus, exact counts, typo handling, twenty anchors and exclusions.
source_needles = [
    "/Users/gao/Library/Mobile Documents/com~apple~CloudDocs/旅顺口写作计划/原著/md",
    "第七卷 大陆-广州治理篇.md | 94 | 37 | 4 | 135",
    "第七卷 大陆-两广攻略篇.md | 1 | 1 | 0 | 2",
    "第八卷 深耕经营(上).md | 0 | 1 | 0 | 1",
    "| **总计** | **95** | **39** | **4** | **138** |",
    "“董明铛” | 0",
    "两处截断笔误“董明”",
    "20 个核心证据锚点",
    "临高启明全本.md",
    "临高启明全本.md.bak",
    "董家铺子当时是 1 级白贴",
    "2 级以上且连续一年照章纳税",
]
for needle in source_needles:
    if needle not in source:
        failures.append(f"SOURCE_INDEX missing: {needle}")
anchor_rows = re.findall(r"^\|\s*\d+\s*\|", source, flags=re.M)
if len(anchor_rows) != 20:
    failures.append(f"expected 20 source anchor rows, got {len(anchor_rows)}")

if failures:
    print("FAIL", root.name)
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS", root.name)

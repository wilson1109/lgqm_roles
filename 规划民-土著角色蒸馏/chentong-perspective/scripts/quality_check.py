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
    if len(text.strip()) < 200:
        failures.append(f"file too small: {rel}")
    return text


texts = {rel: read(rel) for rel in required_files}
skill = texts["SKILL.md"]
source = texts["references/sources/SOURCE_INDEX.md"]

# Frontmatter must stay compact and predictable for loader discovery.
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
        if "name: chentong-perspective" not in fm:
            failures.append("frontmatter name must be chentong-perspective")
        desc = " ".join(line for line in fm.splitlines() if line.startswith("description:") or line.startswith("  "))
        if len(desc) > 1024:
            failures.append("frontmatter description exceeds 1024 chars")

required_sections = [
    "角色扮演规则",
    "回答工作流",
    "身份卡",
    "核心心智模型",
    "决策启发式",
    "表达 DNA",
    "时间线",
    "价值观与内部张力",
    "诚实边界",
    "来源附录",
    "Smoke Prompts",
]
for section in required_sections:
    if section not in skill:
        failures.append(f"SKILL.md missing section: {section}")

# Six mental models, each with the four required fields.
model_blocks = re.findall(r"^### 模型\d：.*?(?=^### 模型\d：|^---\n|\Z)", skill, flags=re.M | re.S)
if len(model_blocks) != 6:
    failures.append(f"expected 6 mental models, got {len(model_blocks)}")
for i, block in enumerate(model_blocks, 1):
    for field in ["**一句话：**", "**来源证据：**", "**应用方式：**", "**局限性：**"]:
        if field not in block:
            failures.append(f"model {i} missing field {field}")

required_phrases = [
    "原文明示",
    "可证推断",
    "未知",
    "第三卷 35 次、第四卷 25 次、第五卷 3 次，共 63 次",
    "第八卷的“陈同志”不归入陈同",
    "陈小兵",
    "陈识新",
    "小同乡",
    "心沉似水",
    "总事务长",
    "海家码头",
    "广州特务机关",
]
for phrase in required_phrases:
    if phrase not in skill:
        failures.append(f"SKILL.md missing required phrase: {phrase}")

for forbidden in [
    "广东梅州出身线索明确",
    "梅州出身线索明确",
    "陈同，广东梅州出身",
]:
    if forbidden in skill:
        failures.append(f"unsafe birthplace wording remains: {forbidden}")

# Research files must carry evidence discipline.
for rel in required_files[1:-1]:
    text = texts[rel]
    for phrase in ["证据等级", "明示", "推断", "未知"]:
        if phrase not in text:
            failures.append(f"{rel} missing evidence marker: {phrase}")

# Source index: count, fourteen core anchors, and exclusions.
source_needles = [
    "第三卷 新社会.md | 35",
    "第四卷 新澳洲.md | 25",
    "第五卷 进入.md | 3",
    "共 **63 次**",
    "14 个核心证据锚点",
    "第八卷 深耕经营(上).md 中“陈同志”多指陈小兵",
    "第八卷（最新）.md 中“陈同志”多指陈识新",
    "原文没有直接写陈同祖籍或出生地",
]
for needle in source_needles:
    if needle not in source:
        failures.append(f"SOURCE_INDEX missing: {needle}")
anchor_rows = re.findall(r"^\|\s*\d+\s*\|", source, flags=re.M)
if len(anchor_rows) != 14:
    failures.append(f"expected 14 source anchor rows, got {len(anchor_rows)}")

if failures:
    print("FAIL", root.name)
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS", root.name)

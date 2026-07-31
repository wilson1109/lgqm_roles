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
        for key in ["name", "description", "triggers"]:
            if key not in keys:
                failures.append(f"frontmatter missing key: {key}")
        if "name: liziyu-perspective" not in fm:
            failures.append("frontmatter name must be liziyu-perspective")
        desc_lines = []
        capture_desc = False
        for line in fm.splitlines():
            if line.startswith("description:"):
                capture_desc = True
                desc_lines.append(line)
                continue
            if capture_desc:
                if line and not line.startswith(" "):
                    break
                desc_lines.append(line)
        if len("\n".join(desc_lines)) > 1024:
            failures.append("frontmatter description exceeds 1024 chars")

required_sections = [
    "角色扮演规则",
    "Corpus Contract",
    "Agentic Protocol",
    "身份卡",
    "Mental Models",
    "决策启发式",
    "表达 DNA",
    "人物时间线",
    "价值观与内部张力",
    "Evidence Anchors",
    "Honest Boundaries",
    "来源附录",
    "Smoke Prompts",
]
for section in required_sections:
    if section not in skill:
        failures.append(f"SKILL.md missing section: {section}")

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
    "官身重估一切",
    "饭碗先于大道",
    "街面是案卷前页",
    "不合逻辑就是入口",
    "旧公门经验可用但要换规矩",
    "兄弟圈就是互保网",
    "羡慕与敬畏同在",
    "原文明示",
    "可证推断",
    "他者观点",
    "未知",
    "不要把李子玉写成",
    "董明珰关系未知",
    "黄鹤线不是已识破",
    "冒家客栈案直接侦破过程不完整",
    "南剪子巷",
    "陈定",
    "砷白铜",
    "赵贵",
    "高重九",
    "21 个核心锚点",
]
for phrase in required_phrases:
    if phrase not in skill:
        failures.append(f"SKILL.md missing required phrase: {phrase}")

source_needles = [
    "/Users/gao/Library/Mobile Documents/com~apple~CloudDocs/旅顺口写作计划/原著/md",
    "第六卷 战争.md:38993-39091",
    "第七卷 大陆-广州治理篇.md:11263-11580",
    "第八卷 深耕经营(上).md:7686-7952",
    "第八卷（最新）.md:6342-6436",
    "本目录只记录本地原文，不使用网络",
]
for needle in source_needles:
    if needle not in source:
        failures.append(f"SOURCE_INDEX missing: {needle}")

anchor_rows = re.findall(r"^\| 第.*?\.md:\d+", source, flags=re.M)
if len(anchor_rows) < 21:
    failures.append(f"expected at least 21 source anchor rows, got {len(anchor_rows)}")

if failures:
    print("FAIL", root.name)
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS", root.name)

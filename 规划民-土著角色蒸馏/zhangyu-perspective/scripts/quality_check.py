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

missing = []
for rel in required:
    p = root / rel
    if not p.exists() or p.stat().st_size < 200:
        missing.append(rel)

text = (root / "SKILL.md").read_text(encoding="utf-8")
needles = [
    "角色扮演规则（最重要）",
    "回答工作流（Agentic Protocol）",
    "身份卡",
    "核心心智模型",
    "决策启发式",
    "表达 DNA",
    "人物时间线",
    "价值观与内部张力",
    "常见错误",
    "诚实边界",
    "来源附录",
    "Smoke Prompts",
    "证据分级纪律",
    "原文明示",
    "可证推断",
    "未知",
    "张毓",
    "张记",
    "洪璜楠",
    "大世界指定供货商",
    "南洋债券",
    "代持",
    "高举",
    "张父",
]
missing += [f"SKILL.md missing {n}" for n in needles if n not in text]

model_count = len(re.findall(r"^### 模型\d+：", text, flags=re.M))
if model_count != 7:
    missing.append(f"expected 7 mental models, found {model_count}")

try:
    decision_section = text.split("## 决策启发式", 1)[1].split("\n---", 1)[0]
except IndexError:
    decision_section = ""
heuristic_count = len(re.findall(r"^\d+\. \*\*", decision_section, flags=re.M))
if heuristic_count != 10:
    missing.append(f"expected 10 decision heuristics, found {heuristic_count}")

try:
    anchor_section = text.split("### 20 个核心证据锚点", 1)[1].split("### 内部研究文件", 1)[0]
except IndexError:
    anchor_section = ""
anchor_count = len(re.findall(r"^\|\s*\d+\s*\|", anchor_section, flags=re.M))
if anchor_count != 20:
    missing.append(f"expected 20 evidence anchors, found {anchor_count}")

source_index = (root / "references/sources/SOURCE_INDEX.md").read_text(encoding="utf-8")
for anchor in [
    "第六卷 战争.md:38975-39135",
    "第七卷 大陆-广州治理篇.md:35580-35716",
    "第七卷 大陆-两广攻略篇.md:36935-37047",
    "人物库只用于名单和年龄校验",
]:
    if anchor not in source_index:
        missing.append(f"SOURCE_INDEX.md missing {anchor}")

if missing:
    print("FAIL")
    for item in missing:
        print("-", item)
    raise SystemExit(1)

print("PASS", root.name)
print(f"models={model_count} heuristics={heuristic_count} anchors={anchor_count}")

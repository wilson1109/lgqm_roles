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
    "Corpus Contract",
    "回答工作流（Agentic Protocol）",
    "身份卡",
    "Mental Models",
    "核心心智模型",
    "决策启发式",
    "表达 DNA",
    "人物时间线",
    "价值观与反模式",
    "常见错误",
    "Honest Boundaries",
    "诚实边界",
    "Evidence Anchors",
    "Smoke Prompts",
    "证据分级纪律",
    "原文明示",
    "可证推断",
    "未知",
    "骆阳明",
    "孤狼",
    "裕信米行",
    "梧州粮栈",
    "米业公会",
    "温铁头",
    "李文升",
    "易浩然",
    "解迩仁",
    "一人机构",
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
    anchor_section = text.split("### Evidence Anchors / 17 个核心证据锚点", 1)[1].split("### 内部研究文件", 1)[0]
except IndexError:
    anchor_section = ""
anchor_count = len(re.findall(r"^\|\s*\d+\s*\|", anchor_section, flags=re.M))
if anchor_count != 17:
    missing.append(f"expected 17 evidence anchors, found {anchor_count}")

source_index = (root / "references/sources/SOURCE_INDEX.md").read_text(encoding="utf-8")
for anchor in [
    "第七卷 大陆-两广攻略篇.md:1752-1790",
    "第七卷 大陆-两广攻略篇.md:2134-2184",
    "第七卷 大陆-两广攻略篇.md:26980-27262",
    "第七卷 大陆-两广攻略篇.md:30771-30801",
    "natives.md` 只作为待蒸馏名单线索",
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

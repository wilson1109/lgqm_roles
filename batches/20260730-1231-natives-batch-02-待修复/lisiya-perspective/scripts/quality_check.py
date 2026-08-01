#!/usr/bin/env python3
from pathlib import Path

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
    "思维操作系统",
    "角色扮演规则",
    "Corpus Contract",
    "Mental Models",
    "Agentic Protocol",
    "决策启发式",
    "Honest Boundaries",
    "Evidence Anchors",
    "李华梅",
    "李淳",
    "李醇",
    "李默",
    "七海霸者之证",
    "安达曼女仆",
    "兰度",
    "苟循礼",
    "李思雅集团",
    "真情与心计",
    "人物时间线",
]
missing += [f"SKILL.md missing {n}" for n in needles if n not in text]

if missing:
    print("FAIL")
    for item in missing:
        print("-", item)
    raise SystemExit(1)

print("PASS", root.name)

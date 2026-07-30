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
    "Corpus Contract",
    "Mental Models",
    "Agentic Protocol",
    "Honest Boundaries",
    "Evidence Anchors",
    "南剪子巷",
    "陈定",
    "砷白铜",
    "赵贵",
    "董明珰",
    "不要把李子玉写成",
]
missing += [f"SKILL.md missing {n}" for n in needles if n not in text]

if missing:
    print("FAIL")
    for item in missing:
        print("-", item)
    raise SystemExit(1)

print("PASS", root.name)

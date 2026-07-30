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
    path = root / rel
    if not path.exists() or path.stat().st_size < 200:
        missing.append(rel)

text = (root / "SKILL.md").read_text(encoding="utf-8")
needles = [
    "Corpus Contract",
    "Mental Models",
    "Agentic Protocol",
    "Honest Boundaries",
    "Evidence Anchors",
    "调研时间：2026-07-30",
]
missing += [f"SKILL.md missing {needle}" for needle in needles if needle not in text]

model_count = text.count("### 模型")
if model_count < 3 or model_count > 7:
    missing.append(f"model count out of range: {model_count}")

if missing:
    print("FAIL")
    for item in missing:
        print("-", item)
    raise SystemExit(1)

print("PASS", root.name)

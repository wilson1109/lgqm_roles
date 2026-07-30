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
    "熊文灿 · 思维操作系统",
    "角色扮演规则（最重要）",
    "回答工作流（Agentic Protocol）",
    "身份卡",
    "核心心智模型",
    "决策启发式",
    "表达DNA",
    "人物时间线（关键节点）",
    "价值观与反模式",
    "智识谱系",
    "诚实边界",
    "附录：调研来源",
    "郑芝龙",
    "常青云",
    "常浦",
    "火烧梧州",
    "羚羊峡",
    "招抚",
    "戴罪立功",
]
missing += [f"SKILL.md missing {n}" for n in needles if n not in text]

model_count = text.count("### 模型")
if model_count != 7:
    missing.append(f"expected 7 mental models, found {model_count}")

heuristic_lines = [
    line for line in text.splitlines()
    if line[:3] in {f"{i}. " for i in range(1, 9)}
]
if len(heuristic_lines) < 8:
    missing.append(f"expected at least 8 decision heuristics, found {len(heuristic_lines)}")

if missing:
    print("FAIL")
    for item in missing:
        print("-", item)
    raise SystemExit(1)

print("PASS", root.name)

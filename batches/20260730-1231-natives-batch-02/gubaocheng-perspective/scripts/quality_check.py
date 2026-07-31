#!/usr/bin/env python3
import re
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
    "回答工作流",
    "Corpus Contract",
    "核心心智模型",
    "Mental Models",
    "Agentic Protocol",
    "证据锚点",
    "Evidence Anchors",
    "决策启发式",
    "表达 DNA",
    "人物时间线",
    "价值观与内部张力",
    "诚实边界",
    "来源附录",
    "Smoke Prompts",
    "顾葆成",
    "顾少掌柜",
    "李洛由妻侄",
    "琼海号",
    "天宝号",
    "辽海行临高分号",
    "夏茅冈煤矿",
    "黄县煤矿",
    "殖民贸易部",
    "德隆贷款",
    "髡化",
    "不是李洛由第二",
    "证据不足",
]
missing += [f"SKILL.md missing {n}" for n in needles if n not in text]

model_blocks = re.findall(
    r"^### 模型\d：.*?(?=^### 模型\d：|^## 证据锚点|^---\n|\Z)",
    text,
    flags=re.M | re.S,
)
if len(model_blocks) != 7:
    missing.append(f"expected 7 mental models, got {len(model_blocks)}")
for i, block in enumerate(model_blocks, 1):
    for field in ["**一句话：**", "**来源证据：**", "**应用方式：**", "**局限性：**"]:
        if field not in block:
            missing.append(f"model {i} missing field {field}")

heuristics = re.findall(r"^\d+\. \*\*", text, flags=re.M)
if len(heuristics) < 8:
    missing.append(f"expected at least 8 decision heuristics, got {len(heuristics)}")

anchor_rows = re.findall(r"^\| 第[三四五七八]卷", text, flags=re.M)
if len(anchor_rows) < 13:
    missing.append(f"expected at least 13 evidence anchor rows, got {len(anchor_rows)}")

if missing:
    print("FAIL")
    for item in missing:
        print("-", item)
    raise SystemExit(1)

print("PASS", root.name)

#!/usr/bin/env python3
from pathlib import Path

SOURCE_ROOT = Path("/Users/gao/Library/Mobile Documents/com~apple~CloudDocs/旅顺口写作计划/原著/md")
SOURCES = [
    "第五卷 进入.md",
    "第八卷 深耕经营(上).md",
    "第八卷（最新）.md",
]
NEEDLES = ("温体仁", "溫體仁")

root = Path(__file__).resolve().parents[1]
out = root / "references" / "sources" / "raw-mentions-local.md"

total = 0
lines = ["# 温体仁：本地原文命中\n", "\n"]
lines.append(f"源根目录：{SOURCE_ROOT}\n\n")

for name in SOURCES:
    path = SOURCE_ROOT / name
    matches = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if any(needle in line for needle in NEEDLES):
            matches.append((lineno, line.strip()))
    total += len(matches)
    lines.append(f"## {name}（{len(matches)}行）\n\n")
    for lineno, line in matches:
        lines.append(f"- {name}:{lineno}: {line}\n")
    lines.append("\n")

lines.insert(2, f"拆卷去重匹配行：{total}行；全本及备份存在重复命中，未纳入本文件。\n\n")
out.write_text("".join(lines), encoding="utf-8")
print(out)

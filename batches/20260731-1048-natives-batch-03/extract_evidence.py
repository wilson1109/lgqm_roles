#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract exact novel evidence for selected batch-03 characters.

This script is intentionally dumb: it searches configured aliases, slices
sentences/paragraphs directly from the local novel text, and writes JSONL.
No interpretations, models, or draft prose belong here.
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
from pathlib import Path


NOVEL = Path(
    "/Users/gao/Library/Mobile Documents/com~apple~CloudDocs/"
    "旅顺口写作计划/原著/md/临高启明全本.md"
)

TARGETS: dict[str, dict[str, object]] = {
    "changqingyun": {
        "dir": "changqingyun-perspective",
        "aliases": ["常青云"],
    },
    "fubuer": {
        "dir": "fubuer-perspective",
        "aliases": ["符不二"],
    },
    "huangxiong": {
        "dir": "huangxiong-perspective",
        "aliases": ["黄熊"],
    },
    "yangshixiang": {
        "dir": "yangshixiang-perspective",
        "aliases": ["杨世祥"],
    },
    "zengjuan": {
        "dir": "zengjuan-perspective",
        "aliases": ["曾卷"],
    },
    "zhaofengtian": {
        "dir": "zhaofengtian-perspective",
        "aliases": ["赵丰田"],
    },
}

SENTENCE_END = "。！？!?；;\n"
HEADING_RE = re.compile(r"^(#{1,6}\s+.+)$", re.M)


def line_starts(text: str) -> list[int]:
    starts = [0]
    starts.extend(match.end() for match in re.finditer(r"\n", text))
    return starts


def line_no(starts: list[int], offset: int) -> int:
    return bisect.bisect_right(starts, offset)


def chapter_index(text: str) -> list[tuple[int, str]]:
    chapters: list[tuple[int, str]] = []
    for match in HEADING_RE.finditer(text):
        heading = match.group(1).strip()
        if "临高启明" in heading and len(heading) < 20:
            continue
        chapters.append((match.start(), heading))
    return chapters


def chapter_at(chapters: list[tuple[int, str]], offset: int) -> str:
    idx = bisect.bisect_right(chapters, (offset, chr(0x10FFFF))) - 1
    if idx < 0:
        return "UNKNOWN"
    return chapters[idx][1]


def slice_sentence(text: str, offset: int) -> tuple[int, str]:
    start = offset
    while start > 0 and text[start - 1] not in SENTENCE_END:
        start -= 1
    while start < len(text) and text[start] in "\n\r\t ":
        start += 1

    end = offset
    while end < len(text) and text[end] not in SENTENCE_END:
        end += 1
    if end < len(text):
        end += 1

    quote = text[start:end].strip()
    if len(quote) < 18:
        p_start = text.rfind("\n", 0, offset)
        p_end = text.find("\n", offset)
        start = 0 if p_start == -1 else p_start + 1
        end = len(text) if p_end == -1 else p_end
        quote = text[start:end].strip()
    return start, quote


def context_slice(text: str, start: int, width: int = 220) -> str:
    left = max(0, start - width)
    right = min(len(text), start + width)
    return text[left:right].strip()


def collect(text: str, target: dict[str, object]) -> list[dict[str, object]]:
    aliases = [re.escape(alias) for alias in target["aliases"]]  # type: ignore[index]
    pattern = re.compile("|".join(aliases))
    starts = line_starts(text)
    chapters = chapter_index(text)
    seen: set[tuple[int, str]] = set()
    rows: list[dict[str, object]] = []

    for match in pattern.finditer(text):
        start, quote = slice_sentence(text, match.start())
        key = (start, quote)
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "id": len(rows) + 1,
                "quote": quote,
                "offset": start,
                "line": line_no(starts, start),
                "chapter": chapter_at(chapters, start),
                "aliases": sorted(set(pattern.findall(quote))),
                "context": context_slice(text, start),
            }
        )
    return rows


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "targets",
        nargs="*",
        help="Target ids to extract. Omit to extract all configured targets.",
    )
    args = parser.parse_args()

    unknown = sorted(set(args.targets) - set(TARGETS))
    if unknown:
        parser.error(
            "unknown target(s): "
            + ", ".join(unknown)
            + "; choose from "
            + ", ".join(sorted(TARGETS))
        )

    text = NOVEL.read_text(encoding="utf-8")
    root = Path(__file__).resolve().parent
    target_ids = args.targets or sorted(TARGETS)

    for target_id in target_ids:
        target = TARGETS[target_id]
        rows = collect(text, target)
        out = root / str(target["dir"]) / "references" / "sources" / "EVIDENCE.jsonl"
        write_jsonl(out, rows)
        print(f"{target_id}: wrote {len(rows)} evidence rows -> {out}")
        if len(rows) < 30:
            print(f"WARNING: {target_id} has fewer than 30 evidence rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import os
import json
import pathlib
import re
import subprocess
import sys
import tempfile


MIN_EVIDENCE_ROWS = 30
FULL_COORD_RE = re.compile(r"EVIDENCE\.jsonl\s+#(\d+),\s*offset\s+(\d+)")
PARTIAL_COORD_RE = re.compile(r"EVIDENCE\.jsonl\s+#\d+(?!\d)(?!,\s*offset)")
SHORT_REF_RE = re.compile(r"(?<!EVIDENCE\.jsonl\s)#\d+(?!\d)")


def find_repo_root(start: pathlib.Path) -> pathlib.Path:
    for parent in [start, *start.parents]:
        if (parent / "verify_batch.py").exists():
            return parent
    raise SystemExit("[ABORT] verify_batch.py not found")


def main() -> int:
    skill_dir = pathlib.Path(__file__).resolve().parents[1]
    repo_root = find_repo_root(skill_dir)
    evidence = skill_dir / "references" / "sources" / "EVIDENCE.jsonl"

    if not evidence.exists():
        print(f"[FAIL] {skill_dir.name}: EVIDENCE.jsonl missing")
        return 1

    with evidence.open(encoding="utf-8") as f:
        rows = sum(1 for line in f if line.strip())
    if rows < MIN_EVIDENCE_ROWS:
        print(f"[FAIL] {skill_dir.name}: only {rows} evidence rows")
        return 1

    evidence_by_id = {}
    with evidence.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            evidence_by_id[int(row["id"])] = int(row["offset"])

    content_paths = [skill_dir / "SKILL.md"]
    content_paths.extend(sorted((skill_dir / "references" / "research").glob("*.md")))
    errors = []
    for path in content_paths:
        with path.open(encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if SHORT_REF_RE.search(line):
                    errors.append(
                        f"{path.relative_to(skill_dir)}:{lineno}: short evidence ref"
                    )
                if PARTIAL_COORD_RE.search(line):
                    errors.append(
                        f"{path.relative_to(skill_dir)}:{lineno}: incomplete evidence coordinate"
                    )
                for match in FULL_COORD_RE.finditer(line):
                    evidence_id = int(match.group(1))
                    offset = int(match.group(2))
                    if evidence_by_id.get(evidence_id) != offset:
                        errors.append(
                            f"{path.relative_to(skill_dir)}:{lineno}: "
                            f"EVIDENCE #{evidence_id} offset {offset} mismatch"
                        )
    if errors:
        print(f"[FAIL] {skill_dir.name}: strict evidence coordinate errors")
        for error in errors[:40]:
            print(f"  - {error}")
        if len(errors) > 40:
            print(f"  - ... {len(errors) - 40} more")
        return 1

    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"{skill_dir.name}-verify-"))
    os.symlink(skill_dir, tmp / skill_dir.name)
    return subprocess.run(
        [sys.executable, str(repo_root / "verify_batch.py"), str(tmp)]
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())

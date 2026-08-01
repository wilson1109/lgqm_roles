#!/usr/bin/env python3
import os
import pathlib
import subprocess
import sys
import tempfile


MIN_EVIDENCE_ROWS = 30


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

    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"{skill_dir.name}-verify-"))
    os.symlink(skill_dir, tmp / skill_dir.name)
    return subprocess.run(
        [sys.executable, str(repo_root / "verify_batch.py"), str(tmp)]
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())

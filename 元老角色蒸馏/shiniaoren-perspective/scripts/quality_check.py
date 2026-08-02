#!/usr/bin/env python3
import os
import pathlib
import subprocess
import sys
import tempfile


MIN_EVIDENCE_ROWS = 30
GENERIC_STEP1_TYPES = ["原文考据", "角色判断", "制度分析", "伦理风险"]
FORBIDDEN_SKILL_FRAGMENTS = [
    "先给结论，再说明模型依据",
    "事实约束 -> 权力/资源 -> 人心/伦理 -> 可执行动作",
    "EVIDENCE #",
    "offset ",
]


def find_repo_root(start: pathlib.Path) -> pathlib.Path:
    for parent in [start, *start.parents]:
        if (parent / "verify_batch.py").exists():
            return parent
    raise SystemExit("[ABORT] verify_batch.py not found")


def main() -> int:
    skill_dir = pathlib.Path(__file__).resolve().parents[1]
    repo_root = find_repo_root(skill_dir)
    evidence = skill_dir / "references" / "sources" / "EVIDENCE.jsonl"
    skill_md = skill_dir / "SKILL.md"

    if not evidence.exists():
        print(f"[FAIL] {skill_dir.name}: EVIDENCE.jsonl missing")
        return 1
    if not skill_md.exists():
        print(f"[FAIL] {skill_dir.name}: SKILL.md missing")
        return 1

    with evidence.open(encoding="utf-8") as f:
        rows = sum(1 for line in f if line.strip())
    if rows < MIN_EVIDENCE_ROWS:
        print(f"[FAIL] {skill_dir.name}: only {rows} evidence rows")
        return 1

    content = skill_md.read_text(encoding="utf-8")
    for fragment in FORBIDDEN_SKILL_FRAGMENTS:
        if fragment in content:
            print(f"[FAIL] {skill_dir.name}: forbidden template/evidence fragment in SKILL.md: {fragment}")
            return 1
    for generic_type in GENERIC_STEP1_TYPES:
        if f"**{generic_type}**" in content:
            print(f"[FAIL] {skill_dir.name}: generic Step 1 type in SKILL.md: {generic_type}")
            return 1
    for heading in ("### 思想来源", "### 在元老院的位置"):
        if heading not in content:
            print(f"[FAIL] {skill_dir.name}: missing genealogy heading: {heading}")
            return 1
    step3 = content.split("### Step 3:", 1)
    if len(step3) != 2 or step3[1].split("---", 1)[0].count("\n- ") < 4:
        print(f"[FAIL] {skill_dir.name}: Step 3 is missing substantial character-specific bullets")
        return 1

    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"{skill_dir.name}-verify-"))
    os.symlink(skill_dir, tmp / skill_dir.name)
    return subprocess.run(
        [sys.executable, str(repo_root / "verify_batch.py"), str(tmp)]
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())

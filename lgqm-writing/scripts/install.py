#!/usr/bin/env python3
"""install.py — 将 lgqm_roles 安装到 Claude Code skills 目录。

跨平台（Windows / macOS / Linux）。从 lgqm_roles/ 源仓库将 lgqm-writing/
和全部 *-perspective/ 平铺复制到 ~/.claude/skills/。

用法:
    python install.py             # 默认安装到 ~/.claude/skills/
    python install.py --dir PATH  # 安装到指定目录

注意:
    - 本脚本必须从 lgqm_roles/lgqm-writing/scripts/ 运行，
      或 lgqm-writing/ 必须位于 lgqm_roles/ 内、与三个分类目录同级。
    - 安装后运行: python ~/.claude/skills/lgqm-writing/scripts/build_catalog.py
"""
import os
import sys
import shutil
import argparse
from pathlib import Path

CATEGORY_DIRS = ['元老角色蒸馏', '规划民-土著角色蒸馏', '明朝真实历史人物蒸馏']


def get_skills_root():
    """定位 lgqm_roles/ 源仓库根目录（lgqm-writing/ 的父目录）。"""
    script_dir = Path(__file__).resolve().parent   # scripts/
    lgqm_writing = script_dir.parent              # lgqm-writing/
    skills_root = lgqm_writing.parent             # 期望是 lgqm_roles/
    return skills_root, lgqm_writing


def validate_source_root(source_root, lgqm_writing):
    """校验 source_root 是源仓库根（含分类目录 + lgqm-writing/）。"""
    ok = (lgqm_writing / 'SKILL.md').exists()
    for cat in CATEGORY_DIRS:
        if (source_root / cat).exists():
            ok = True
    if not ok:
        print(f"ERROR: {source_root} 不是 lgqm_roles 源仓库根目录。", file=sys.stderr)
        print("install.py 必须从 lgqm_roles/lgqm-writing/scripts/ 运行，", file=sys.stderr)
        print("或 lgqm-writing/ 必须位于 lgqm_roles/ 内、与三个分类目录同级。", file=sys.stderr)
        sys.exit(1)


def install(target_root):
    source_root, lgqm_writing = get_skills_root()
    validate_source_root(source_root, lgqm_writing)
    target_root.mkdir(parents=True, exist_ok=True)

    # 1. 复制 lgqm-writing/
    dest = target_root / 'lgqm-writing'
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(lgqm_writing, dest)
    print(f"  Copied: lgqm-writing/ -> {dest}")

    # 2. 平铺复制全部 *-perspective/
    count = 0
    for cat in CATEGORY_DIRS:
        cat_path = source_root / cat
        if not cat_path.exists():
            print(f"  [SKIP] 目录不存在: {cat}")
            continue
        for skill_dir in cat_path.iterdir():
            if not skill_dir.is_dir() or not skill_dir.name.endswith('-perspective'):
                continue
            dst = target_root / skill_dir.name
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(skill_dir, dst)
            count += 1
    print(f"  Copied: {count} *-perspective/ directories")

    print(f"\n安装完成: {target_root}")
    print("下一步: python \"{}/lgqm-writing/scripts/build_catalog.py\"".format(target_root))


def main():
    parser = argparse.ArgumentParser(description='Install lgqm_roles to Claude Code skills directory')
    parser.add_argument('--dir', type=str, default=None, help='目标目录（默认 ~/.claude/skills/）')
    args = parser.parse_args()

    if args.dir:
        target_root = Path(args.dir).resolve()
    else:
        target_root = Path.home() / '.claude' / 'skills'

    install(target_root)


if __name__ == '__main__':
    main()

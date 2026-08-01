#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parents[1]
required = [
    'SKILL.md',
    'references/research/01-writings.md',
    'references/research/02-conversations.md',
    'references/research/03-expression-dna.md',
    'references/research/04-external-views.md',
    'references/research/05-decisions.md',
    'references/research/06-timeline.md',
    'references/sources/SOURCE_INDEX.md',
]
missing = []
for rel in required:
    p = root / rel
    if not p.exists() or p.stat().st_size < 200:
        missing.append(rel)
text = (root / 'SKILL.md').read_text(encoding='utf-8')
needles = [
    'triggers:',
    '思维操作系统',
    '角色扮演规则',
    '语料契约',
    '回答工作流',
    '核心心智模型',
    '决策启发式',
    '表达 DNA',
    '人物时间线',
    '价值观与反模式',
    '智识谱系',
    '诚实边界',
    '附录：调研来源',
    'Evidence Anchors',
]
missing += [f'SKILL.md missing {n}' for n in needles if n not in text]
facts = ['天情广闻录', '琼崖败略十一疏', '老泥鳅', '知髡以制髡', '王朝可更易', '道统不能绝', '文底', '武底']
missing += [f'SKILL.md missing corrected fact {n}' for n in facts if n not in text]
reference_needles = {
    'references/research/01-writings.md': ['天情广闻录', '琼崖败略十一疏', '道统不能绝'],
    'references/research/02-conversations.md': ['月婉', '公开财报', '系统'],
    'references/research/03-expression-dna.md': ['王朝可更易', '公开财报', '专业'],
    'references/research/04-external-views.md': ['直接自述补强', '守道与制髡'],
    'references/research/05-decisions.md': ['解释髡人“系统”', '临败守道'],
    'references/research/06-timeline.md': ['髡情自述', '临败守道'],
    'references/sources/SOURCE_INDEX.md': ['8669-8681', '9007-9029'],
}
for rel, terms in reference_needles.items():
    body = (root / rel).read_text(encoding='utf-8')
    missing += [f'{rel} missing {term}' for term in terms if term not in body]
if missing:
    print('FAIL')
    for item in missing:
        print('-', item)
    raise SystemExit(1)
print('PASS', root.name)

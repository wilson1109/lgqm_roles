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
facts = ['黄秉坤', '黄炳坤', '助学贷款', '财税职校', '二爷', '女人缘', '情场高手']
missing += [f'SKILL.md missing corrected fact {n}' for n in facts if n not in text]
reference_needles = {
    'references/research/01-writings.md': ['旧主不是清零项', '笨拙的身份自救', '女人缘打开，手脚仍笨'],
    'references/research/02-conversations.md': ['先喊旧称', '有女人缘'],
    'references/research/03-expression-dna.md': ['黄秉坤书童', '黄炳坤书童', '助学贷款'],
    'references/research/05-decisions.md': ['先脱口喊“二爷”', '有女人缘不等于会处理女人缘'],
    'references/research/06-timeline.md': ['举债续学', '财税职校'],
    'references/sources/SOURCE_INDEX.md': ['被女同学拥抱', '退学、贷款、职校'],
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

import re, sys, pathlib
rows = [l for l in pathlib.Path('rows.md').read_text().splitlines() if l.startswith('| `')]
assert len(rows) == 5, len(rows)
for r in rows:
    cells = [c.strip() for c in r.strip().strip('|').split('|')]
    assert len(cells) == 8, (len(cells), cells[0])
    assert all(cells), cells[0]
skill = pathlib.Path('lane/SKILL.md')
text = skill.read_text()
head = '## Gate/probe registry'
i = text.find(head)
j = text.find('\n## ', i + 1)
block = text[i:j]
lines = block.splitlines()
last = max(k for k, l in enumerate(lines) if l.startswith('| `'))
new = lines[:last + 1] + rows + lines[last + 1:]
skill.write_text(text[:i] + '\n'.join(new) + text[j:])
print('inserted', len(rows), 'rows after line', last)

"""Apply R34ReadmePatch/patch.md blocks (a)-(d) + knowledge entries to the mirror only."""
import re
import shutil
import sys
from pathlib import Path

W = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/build/R34MutReadme-work')
B = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/build')

patch = (B / 'R34ReadmePatch/patch.md').read_text(encoding='utf-8')
afters = re.findall(r'After:\n```text\n(.*?)```', patch, re.S)
assert len(afters) == 4, f"expected 4 After blocks, got {len(afters)}"
row_a = afters[0].strip('\n')
row_b = afters[1].strip('\n')
assert row_a.count('\n') == 0 and row_b.count('\n') == 0
bullet = afters[2].strip('\n')
assert bullet.count('\n') == 0
new_d = afters[3].strip('\n').splitlines()
assert len(new_d) == 2
before_d = re.findall(r'Before \(line 279\):\n```text\n(.*?)```', patch, re.S)
assert len(before_d) == 1
old_d = before_d[0].strip('\n')

readme = W / 'corpus/README.md'
lines = readme.read_text(encoding='utf-8').splitlines()

# (a)+(b): insert the two index rows immediately before the lessons/round-1.md row
anchors1 = [i for i, l in enumerate(lines) if l.startswith('| `lessons/round-1.md`')]
assert len(anchors1) == 1, anchors1
lines[anchors1[0]:anchors1[0]] = [row_a, row_b]

# (c): insert discharge bullet immediately before '## Open gaps'
anchors2 = [i for i, l in enumerate(lines) if l.startswith('## Open gaps')]
assert len(anchors2) == 1, anchors2
lines.insert(anchors2[0], bullet)

# (d): replace the round-33 partly-discharged line with the new two-line text
anchors3 = [i for i, l in enumerate(lines) if l == old_d]
assert len(anchors3) == 1, anchors3
lines[anchors3[0]:anchors3[0] + 1] = new_d

readme.write_text('\n'.join(lines) + '\n', encoding='utf-8')

# entries: copy draft entry files into the mirror knowledge dir
shutil.copyfile(B / 'R34EntryTB2/entry.md', W / 'corpus/knowledge/terminal-bench-task-grader.md')
shutil.copyfile(B / 'R34EntryProvider/entry.md', W / 'corpus/knowledge/provider-selfreport-eval-limits.md')
print('patch applied: 2 index rows, coverage bullet, frontier bullet pair, 2 entries')

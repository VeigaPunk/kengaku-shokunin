import re
import subprocess

LANE = '/home/vgpnk/Projects/shokunin/kengaku-shokunin'
REV = '43255758'

def git(*args):
    p = subprocess.run(['git', '-C', LANE, *args], capture_output=True, text=True, check=True)
    return p.stdout

text = git('show', REV + ':corpus/README.md')
text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
text = re.sub(r'^\s*```.*?^\s*```', '', text, flags=re.S | re.M)
rows = {'knowledge': set(), 'lessons': set()}
for line in text.splitlines():
    if not line.startswith('|'):
        continue
    cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
    if len(cells) < 2 or not all(cells):
        continue
    match = re.fullmatch(r'`(knowledge|lessons)/([^`]+)`', cells[0])
    if match:
        rows[match[1]].add(match[2])
tree = git('ls-tree', '-r', '--name-only', REV, 'corpus').splitlines()
counts = []
for kind in ('knowledge', 'lessons'):
    files = {p.rsplit('/', 1)[1] for p in tree if p.startswith('corpus/' + kind + '/') and p.count('/') == 2 and p.endswith('.md')}
    missing = files - rows[kind]
    orphan = rows[kind] - files
    counts.append(len(missing))
    print(f'UNIVERSE {kind} files={len(files)} indexed={len(files)-len(missing)} missing={len(missing)} orphan={len(orphan)}')
dirs = {p.split('/')[2] for p in tree if p.startswith('corpus/evidence/') and p.count('/') >= 3}
mentioned = set(re.findall(r'corpus/evidence/([A-Za-z0-9_.-]+)/', text))
counts.append(len(dirs - mentioned))
print(f'UNIVERSE evidence dirs={len(dirs)} indexed={len(dirs & mentioned)} missing={len(dirs-mentioned)} orphan={len(mentioned-dirs)}')
print(f'FINAL_RULE rev={REV} total={sum(counts)} split=' + '/'.join(map(str, counts)))

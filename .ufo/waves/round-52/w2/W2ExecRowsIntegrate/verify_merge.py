import subprocess,re,shutil,sys
from pathlib import Path
L=Path('lane'); 
base=subprocess.check_output(['git','-C','lane','show','30801b4:SKILL.md'],text=True)
rows=[l for l in Path('registry-rows.md').read_text().splitlines() if l.startswith('| `')]
lines=base.split('\n')
# find end of registry table: last line starting with '| `' after heading
h=next(i for i,l in enumerate(lines) if l.startswith('## Gate/probe registry'))
last=max(i for i,l in enumerate(lines[h:h+120],start=h) if l.startswith('| `'))
def run(skill,tag):
    (L/'SKILL.md').write_text(skill)
    p=subprocess.run(['python3','plans/round52_c2_registry.py','--lane','.'],cwd=L,capture_output=True,text=True)
    print('==',tag,'rc',p.returncode); print('\n'.join(p.stdout.splitlines()[:6]+[x for x in p.stdout.splitlines() if x.startswith(('PREDICATE','  '))][:4]))
new=lines[:last+1]+rows+lines[last+1:]
run('\n'.join(new),'merged-28+2')
# control: drop one row
d=[r for r in rows if 'round33-defects' not in r]
run('\n'.join(lines[:last+1]+d+lines[last+1:]),'drop-row')
# control: blank cells in every new row's verdict
e=[re.sub(r"^(\| `[^`]+` \| \w+ \| .*?\| )", r"\1", r) for r in rows]
blank=[ '|'.join(r.split('|')[:4])+'|  |'+'|'.join(r.split('|')[5:]) for r in rows]
run('\n'.join(lines[:last+1]+blank+lines[last+1:]),'blank-verdict')
# control: false selftest
fs=[r.replace('`python3 plans/catalog_probe.py --selftest`','`python3 plans/catalog_probe.py --nope`') for r in rows]
run('\n'.join(lines[:last+1]+fs+lines[last+1:]),'false-selftest')
subprocess.run(['git','-C','lane','checkout','-q','SKILL.md'])

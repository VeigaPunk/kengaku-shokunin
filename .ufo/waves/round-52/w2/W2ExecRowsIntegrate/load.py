import re,sys,json
from pathlib import Path
W=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1')
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
files={'A':'C2ScribeRowsA/rows.md','B':'C2ScribeRowsB/rows.md','C':'C2ScribeRowsC/rows.md','D':'C2ScribeRowsD/artifacts/rows.md','E':'C2ScribeRowsE/rows.md','F':'C2ScribeRowsF/rows.md'}
CMD=re.compile(r"python3 ((?:plans/[A-Za-z0-9_]+\.py|corpus/evidence/[A-Za-z0-9_]+/[A-Za-z0-9_]+\.py|grader\.py))")
def parse(text):
    out=[]
    for line in text.splitlines():
        if not line.startswith('|'): continue
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells)!=8 or set(cells[0])<=set('-: ') or cells[0]=='name': 
            if len(cells)!=8 and not set(cells[0])<=set('-: '): print('BAD CELLCOUNT',len(cells),line[:60])
            continue
        out.append(cells)
    return out
rows={}
for k,f in files.items():
    for r in parse((W/f).read_text()):
        m=CMD.search(r[2]); 
        # uv run form
        rows[r[0]]=(k,m.group(1) if m else None,r)
if __name__=='__main__':
    print(len(rows))
    for n,(k,s,r) in rows.items(): print(k,n,s,[len(c) for c in r])

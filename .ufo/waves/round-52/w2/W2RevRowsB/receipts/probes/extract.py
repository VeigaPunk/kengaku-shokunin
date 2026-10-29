import json,sys
from pathlib import Path
lane=Path(sys.argv[1]); out=sys.argv[2]
names={'order-check','round35-c1-coverage','round35-hardening','round36-c2','round45-c1','round45-c2','round46-c1','round46-c2','round46-c3','round50-c1','round50-c2','round51-routing','round51-surfaces','routed-findings','tb2-grader-probe'}
rows=[]
for ln,line in enumerate((lane/'SKILL.md').read_text().splitlines(),1):
    if not line.startswith('|'): continue
    cells=[c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells)!=8 or cells[0].strip('`') not in names: continue
    rows.append({'line':ln,'name':cells[0].strip('`'),'cells':cells})
json.dump(rows,open(out,'w'),indent=1,ensure_ascii=False)
print(len(rows))

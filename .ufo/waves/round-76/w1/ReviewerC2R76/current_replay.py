import importlib.util,json,contextlib,io,hashlib
from pathlib import Path
S=Path('/fast/scratch/hyaku/kengaku-r76/ReviewerC2R76')
L=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
p=L/'plans/round76_c2_defect_discharge.py'
spec=importlib.util.spec_from_file_location('current_c2',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print('GATE_SHA256',hashlib.sha256(p.read_bytes()).hexdigest())
rows=[json.loads(x) for x in (L/m.LEDGER).read_text().splitlines() if x.strip()]
rows=[x for x in rows if x.get('id','').startswith('R75-D')]
for name in ['e1','e2','e4','e5']:
 root=S/'fix'/name
 r=[dict(x) for x in rows]
 if name=='e1':
  for x in r:x['check']="grep -q 'the' SCORECARD.md"
 if name in ['e4','e5']:r=[]
 (root/m.LEDGER).write_text(''.join(json.dumps(x)+'\n' for x in r))
 out=S/'work'/('current-'+name+'.txt')
 print('=== CURRENT',name)
 rc=m.emit(root,'worktree',out,probe=L,work=S/'work/current')
 print('RC',rc)
print('=== CURRENT REV MASTER')
rc=m.emit(L,'master',S/'work/current-rev.txt',probe=L,work=S/'work/current')
print('RC',rc)

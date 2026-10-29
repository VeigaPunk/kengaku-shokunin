import json,sys,re
sys.path.insert(0,'/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans')
import round52_c1_grader_audit as A
from pathlib import Path
lane=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
G=lane/'corpus/evidence/round52/graders'
rows=json.load(open('ast_all.json'))
pop,records,*_=A.collect(lane)
tot=sum(r.get('test_count',0) for r in records.values()); print('counter test_count total',tot, 'features test_functions total', sum(r['features'].get('test_functions',0) for r in records.values() if r.get('features')))
out=[]
for t,n,c,a,s,e in rows:
    if (c=='P1')!=(a=='P1'):
        body=(G/records[t]['grader']).read_text(errors='replace')
        blk=dict(A.split_tests(body))[n]
        stripped=A.PRESENCE.sub(' ',blk)
        m1=A.BEHAV_T.search(stripped); m2=A.VALUE.search(stripped)
        def ctx(m): 
            return None if not m else stripped[max(0,m.start()-40):m.end()+40].replace('\n','\\n')
        print(t,n,'counter',c,'ast',a,'| BEHAV:',m1.group(0) if m1 else None,'|VALUE:',m2.group(0) if m2 else None)
        print('    ',ctx(m1) or ctx(m2))

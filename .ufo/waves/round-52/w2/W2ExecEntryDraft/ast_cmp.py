import ast,json,sys
sys.path.insert(0,'/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans')
import round52_c1_grader_audit as A
from pathlib import Path
lane=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
G=lane/'corpus/evidence/round52/graders'
pop,records,exp,pres,mm,cands,sums=A.collect(lane)
PRES={'exists','is_file','is_dir','isfile','isdir'}
SAFE={'Path','join','str'}
def callname(c):
    f=c.func
    return f.id if isinstance(f,ast.Name) else f.attr if isinstance(f,ast.Attribute) else '?'
def is_pres_assert(n):
    if not isinstance(n,ast.Assert): return False
    calls=[c for c in ast.walk(n.test) if isinstance(c,ast.Call)]
    if not calls: return False
    if not all(callname(c) in PRES|SAFE for c in calls): return False
    # no comparisons
    if any(isinstance(x,(ast.Compare,)) for x in ast.walk(n.test)): return False
    return any(callname(c) in PRES for c in calls)
def ast_class(fn):
    body=fn.body
    if body and isinstance(body[0],ast.Expr) and isinstance(getattr(body[0],'value',None),ast.Constant): body=body[1:]
    asserts=[b for b in body if isinstance(b,ast.Assert)]
    if not asserts: return 'NA'
    # every statement either simple assign w/ safe calls, setup() call, or pres-assert
    for b in body:
        if isinstance(b,ast.Assert):
            if not is_pres_assert(b): return 'nonP1'
        elif isinstance(b,ast.Assign):
            calls=[c for c in ast.walk(b.value) if isinstance(c,ast.Call)]
            if any(callname(c) not in SAFE for c in calls): return 'nonP1'
        elif isinstance(b,ast.Expr) and isinstance(b.value,ast.Call) and callname(b.value) in ('setup',):
            continue
        else: return 'nonP1'
    return 'P1'
res={}
allrows=[]
for t,r in sorted(records.items()):
    if 'grader' not in r: continue
    body=(G/r['grader']).read_text(errors='replace')
    tree=ast.parse(body)
    amap={n.name:(ast_class(n),n.lineno,n.end_lineno) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
    cmap={x['test']:x['class'] for x in r['tests']}
    for n,(c,s,e) in amap.items():
        allrows.append((t,n,cmap.get(n),c,s,e))
dis=[x for x in allrows if (x[2]=='P1')!=(x[3]=='P1')]
print('total tests',len(allrows),'counter P1',sum(x[2]=='P1' for x in allrows),'ast P1',sum(x[3]=='P1' for x in allrows))
for x in dis: print(x)
json.dump(allrows,open('ast_all.json','w'))

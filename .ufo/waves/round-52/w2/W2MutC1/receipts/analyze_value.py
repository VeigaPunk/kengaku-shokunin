import ast, importlib.util, json, re
from pathlib import Path
S=Path('/fast/scratch/hyaku/kengaku-r52/w2-W2MutC1'); L=S/'lane-base'
def load(p,n):
    sp=importlib.util.spec_from_file_location(n,str(p)); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B=load(S/'mut/base.py','b'); M3=load(S/'mut/M03.py','m3')
pop=json.loads((L/'plans/round52-tasks.json').read_text())
G=L/'corpus/evidence/round52/graders'
rows=[]; flips=[]; total_base={}
for task,files in sorted(pop['tasks'].items()):
    pg=B.primary_grader(files)
    if not pg or not (G/pg).exists(): continue
    body=(G/pg).read_text(errors='replace')
    base_cls=B.classify_tests(body)
    m3_cls=M3.classify_tests(body)
    # AST view: drop comments (not in AST) and docstrings
    try: tree=ast.parse(body)
    except SyntaxError as e: print('SYNTAX',task,e); continue
    fn={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
    for t in base_cls:
        name=t['test']; cls=t['class']
        node=fn.get(name)
        ast_cls=None
        if node is not None:
            import copy; n2=copy.deepcopy(node)
            if n2.body and isinstance(n2.body[0],ast.Expr) and isinstance(getattr(n2.body[0],'value',None),ast.Constant) and isinstance(n2.body[0].value.value,str):
                n2.body=n2.body[1:] or [ast.Pass()]
            block=ast.unparse(n2)
            ast_cls=B.classify_test(block)
        m3c=[x['class'] for x in m3_cls if x['test']==name]
        rows.append((task,name,cls,m3c[0] if m3c else None,ast_cls))
        if cls!='P1' and ast_cls=='P1': flips.append((task,name,cls,ast_cls))
    total_base[task]=len(base_cls)
print('tests scanned',len(rows))
from collections import Counter
print('base classes',Counter(r[2] for r in rows))
print('M03 classes',Counter(r[3] for r in rows))
print('AST(no docstring, no comment) classes',Counter(r[4] for r in rows))
print('P1 in base:',sum(1 for r in rows if r[2]=='P1'),' P1 in AST-view:',sum(1 for r in rows if r[4]=='P1'))
print('tests P3(base) that become P1 once docstrings removed (AST view):')
for f in flips: print('  ',f)
for n in ['test_model_file_exists','test_parallel_linear_exists','test_bn_sample_exists']:
    print(n,[r for r in rows if r[1]==n])

print('--- transition matrix base -> AST-view (all tests)')
print(Counter((r[2],r[4]) for r in rows))
print('--- base != M03 transitions', Counter((r[2],r[3]) for r in rows if r[2]!=r[3]))
# contamination: block of each test extends to next test_ def, so it can swallow helper defs
contam=[]
for task,files in sorted(pop['tasks'].items()):
    pg=B.primary_grader(files)
    if not pg or not (G/pg).exists(): continue
    body=(G/pg).read_text(errors='replace')
    for name,block in B.split_tests(body):
        helpers=[l for l in block.splitlines()[1:] if re.match(r'^(def |class |import |from |[A-Za-z_]+ *=)',l)]
        if helpers: contam.append((task,name,len(helpers),helpers[:2]))
print('tests whose base block swallows non-test top-level code:',len(contam))
for c in contam[:40]: print('  ',c[0],c[1],c[2],c[3])

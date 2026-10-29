import importlib.util, json, re, collections
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c1',LANE/'plans/round52_c1_grader_audit.py')
c1=importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
root=LANE/'corpus/evidence/round52/graders'
pop=json.load(open(LANE/'plans/round52-tasks.json'))
def body_of(t):
    pg=c1.primary_grader(pop['tasks'][t]); return (root/pg).read_text(errors='replace'), pg
# triggers for the two A1-named tests
for t,name in [('pytorch-model-recovery','test_model_file_exists'),('torch-tensor-parallelism','test_parallel_linear_exists'),('pytorch-model-recovery','test_weights_file_unchanged')]:
    b,pg=body_of(t)
    blk=dict(c1.split_tests(b))[name]
    st=c1.PRESENCE.sub(' ',blk)
    print('=====',t,name,'stripped-hits VALUE:',[(m.group(0), st[max(0,m.start()-30):m.end()+20].replace('\n','\\n')) for m in c1.VALUE.finditer(st)][:6])
    print('   BEHAV_T:',[(m.group(0), st[max(0,m.start()-30):m.end()+20].replace('\n','\\n')) for m in c1.BEHAV_T.finditer(st)][:4])
    print(blk[:900])
# population-wide sensitivity
stats=collections.Counter()
examples=collections.defaultdict(list)
for t in sorted(pop['tasks']):
    pg=c1.primary_grader(pop['tasks'][t])
    if not pg or not (root/pg).exists(): continue
    b=(root/pg).read_text(errors='replace')
    if re.search(r'^def\s+test_\w+\s*\([^)]*\)\s*->',b,re.M): stats['return-annotated test defs']+=1; examples['ann'].append(t)
    if re.search(r'^class\s+\w+',b,re.M): stats['files with class defs']+=1; examples['cls'].append(t)
    if re.search(r'^(async\s+)?def\s+test_',b,re.M) is None: stats['files with no top-level def test_']+=1; examples['notop'].append(t)
    if re.search(r'^\s+def\s+test_',b,re.M): stats['files with INDENTED def test_']+=1
    if re.search(r'^async\s+def\s+test_',b,re.M): stats['async test defs']+=1; examples['async'].append(t)
    if re.search(r'^(?!def test_)def\s+\w+',b,re.M): pass
    # helper defs after a test: non-test top-level def after first test def
    defs=[m for m in re.finditer(r'^def\s+(\w+)\s*\(',b,re.M)]
    tfirst=[i for i,m in enumerate(defs) if m.group(1).startswith('test_')]
    if tfirst:
        after=[m.group(1) for m in defs[tfirst[0]:] if not m.group(1).startswith('test_')]
        if after: stats['files with helper def AFTER a test (absorbed into prior test block)']+=1; examples['helperafter'].append((t,after))
    # 'in' tokens in docstrings / comments in test blocks
    for name,blk in c1.split_tests(b):
        code=re.sub(r'"""[\s\S]*?"""','',blk); code=re.sub(r'#[^\n]*','',code)
        if c1.classify_test(blk)!=c1.classify_test(code) and c1.classify_test(blk)=='P3' : stats['tests P3 only because of docstring/comment']+=1; examples['docP3'].append((t,name))
        if c1.classify_test(blk)=='P1' : stats['P1 tests']+=1
        if c1.classify_test(blk)!='P1' and c1.classify_test(code)=='P1': stats['P1 if docstrings+comments removed (gained)']+=1; examples['gainP1'].append((t,name))
        if c1.classify_test(blk)=='P1' and c1.classify_test(code)!='P1': stats['P1 lost if docstrings+comments removed']+=1
for k,v in stats.items(): print(k,v)
for k,v in examples.items(): print(k, v[:12], len(v))

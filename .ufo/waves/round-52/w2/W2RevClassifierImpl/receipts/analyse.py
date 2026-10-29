import importlib.util, json, re, sys, collections
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c1',LANE/'plans/round52_c1_grader_audit.py')
c1=importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
root=LANE/'corpus/evidence/round52/graders'
pop=json.load(open(LANE/'plans/round52-tasks.json'))
tasks=pop['tasks']; cp=pop['capture_population']
# 1 tasks vs capture_population per-task difference
for t in sorted(tasks):
    if sorted(tasks[t])!=sorted(cp[t]):
        print('DIFF',t,'tasks=',tasks[t],'cp=',cp[t])
print('sample tasks value type',type(tasks['adaptive-rejection-sampler']), tasks['adaptive-rejection-sampler'])
print('grader_files field', pop['grader_files'])
# 2 per-test token report
rows=[]
for t,files in sorted(tasks.items()):
    pg=c1.primary_grader(files)
    if not pg or not (root/pg).exists(): continue
    body=(root/pg).read_bytes().decode('utf-8',errors='replace')
    fcls,feats=c1.classify(body)
    for name,block in c1.split_tests(body):
        stripped=c1.PRESENCE.sub(' ',block)
        cls=c1.classify_test(block)
        v=[m.group(0) for m in c1.VALUE.finditer(stripped)]
        b=[m.group(0) for m in c1.BEHAV_T.finditer(stripped)]
        rows.append((t,name,cls,fcls,v[:4],b[:3]))
cnt=collections.Counter(r[2] for r in rows)
print('per-test counts',dict(cnt),'total tests',len(rows))
for r in rows:
    if r[2] in ('P1','P2') or r[0] in ('pytorch-model-recovery','torch-tensor-parallelism'):
        print(r)

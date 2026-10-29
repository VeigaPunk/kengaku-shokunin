import importlib.util, json, re
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c1',LANE/'plans/round52_c1_grader_audit.py')
c1=importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
G=LANE/'corpus/evidence/round52/graders'
pop=json.load(open(LANE/'plans/round52-tasks.json'))
def strip(b): b=re.sub(r'"""[\s\S]*?"""','',b); return re.sub(r'(?m)#[^\n]*','',b)
def split_any_def(body):
    ms=list(re.finditer(r'^def\s+(\w+)\s*\(',body,re.M)); out=[]
    for i,m in enumerate(ms):
        end=ms[i+1].start() if i+1<len(ms) else len(body)
        out.append((m.group(1),body[m.start():end]))
    return out
for t,n in [('pytorch-model-recovery','test_model_file_exists'),('torch-tensor-parallelism','test_parallel_linear_exists'),('torch-tensor-parallelism','test_column_parallel_linear')]:
    pg=c1.primary_grader(pop['tasks'][t]); body=(G/pg).read_text(errors='replace')
    impl=dict(c1.split_tests(body))[n]
    fixed=dict(split_any_def(body))[n]
    print(f'{t}::{n}')
    print('   impl split                 ->',c1.classify_test(impl))
    print('   impl split, no docs/comments->',c1.classify_test(strip(impl)))
    print('   any-def split, no docs/comments->',c1.classify_test(strip(fixed)))
# count tests whose block contains a non-test top-level def (absorbed helpers) and class flips when split fixed
absorbed=[]
for t in sorted(pop['tasks']):
    pg=c1.primary_grader(pop['tasks'][t])
    if not pg or not (G/pg).exists(): continue
    body=(G/pg).read_text(errors='replace')
    a=dict(c1.split_tests(body)); b=dict(split_any_def(body))
    for n in a:
        if a[n]!=b[n]:
            absorbed.append((t,n,c1.classify_test(a[n]),c1.classify_test(b[n])))
print('tests whose block absorbs a helper def:',len(absorbed))
for x in absorbed: print('  ',x)
# distribution-search file-level presence token
body=(G/c1.primary_grader(pop['tasks']['distribution-search'])).read_text(errors='replace')
print('distribution-search presence-ish tokens:',re.findall(r'.{0,25}(?:exists|is_file|is_dir)\(.{0,10}',body)[:6])

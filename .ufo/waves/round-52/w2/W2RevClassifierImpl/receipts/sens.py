import importlib.util, json, re, collections
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c1',LANE/'plans/round52_c1_grader_audit.py')
c1=importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
root=LANE/'corpus/evidence/round52/graders'
pop=json.load(open(LANE/'plans/round52-tasks.json'))
# FROZEN file-level vocabulary (claims §C1 text)
F_PRES=re.compile(r"(exists\(|is_file\(|is_dir\(|os\.path\.exists)")
F_CONT=re.compile(r"(read_text|read_bytes|open\(|json\.load|re\.(search|match|findall|finditer)|\.decode\(|\.strip\(\)|\.splitlines\()")
F_BEH=re.compile(r"(subprocess|os\.system|os\.popen|Popen|socket|requests|urllib|http\.client|docker|bwrap|curl)")
def f_classify(body):
    p=bool(F_PRES.search(body)); c=bool(F_CONT.search(body)); b=bool(F_BEH.search(body))
    n=len(re.findall(r'^\s*def\s+test_',body,re.M))
    if p and not c and not b: return 'V1'
    if b: return 'V2'
    if c: return 'V3'
    if n<=2: return 'V4'
    return 'V0'
rows=[]
for t in sorted(pop['tasks']):
    pg=c1.primary_grader(pop['tasks'][t])
    if not pg or not (root/pg).exists(): continue
    body=(root/pg).read_bytes().decode('utf-8',errors='replace')
    impl,_=c1.classify(body); strict=f_classify(body)
    rows.append((t,pg,body,impl,strict))
print('file-level impl vs frozen-vocab class differences:')
diff=[(t,i,s) for t,_,_,i,s in rows if i!=s]
print(len(diff), diff)
# per-test variants
def p1_tasks(variant):
    tasks=set(); ntests=0
    for t,pg,body,_,_ in rows:
        for name,blk in c1.split_tests(body):
            if variant=='impl': cls=c1.classify_test(blk)
            elif variant=='no_comments_docstrings':
                code=re.sub(r'"""[\s\S]*?"""','',blk); code=re.sub(r'(?m)#[^\n]*','',code); cls=c1.classify_test(code)
            elif variant=='frozen_behav_only':
                st=c1.PRESENCE.sub(' ',blk)
                if 'assert' not in blk: cls='P0'
                elif re.search(r'(subprocess|os\.system|os\.popen|Popen|socket|requests|urllib|http\.client|docker|bwrap|curl)',st): cls='P2'
                elif c1.VALUE.search(st): cls='P3'
                elif c1.PRESENCE.search(blk): cls='P1'
                else: cls='P0'
            elif variant=='extended_presence':
                ext=re.compile(r'\b(os\.path\.isdir\(|os\.path\.isfile\(|glob\(|listdir\(|os\.access\(|os\.stat\(|getsize\()')
                st=c1.PRESENCE.sub(' ',blk); st=ext.sub(' ',st)
                cls=c1.classify_test(blk)
                if cls in('P0','P3') and 'assert' in blk and ext.search(blk) and not c1.BEHAV_T.search(st) and not re.search(r'(==|!=|<=|>=|allclose|len\()', st): cls='P1'
            if cls=='P1': tasks.add(t); ntests+=1
    return len(tasks), ntests, sorted(tasks)
for v in ['impl','no_comments_docstrings','frozen_behav_only','extended_presence']:
    n,k,ts=p1_tasks(v); print(v,'tasks_with_P1=',n,'P1_tests=',k)
    if v in('impl','no_comments_docstrings'): print('   ',ts)
# misses: assert-bearing tests with presence-like calls outside PRESENCE
miss=[]
for t,pg,body,_,_ in rows:
    for name,blk in c1.split_tests(body):
        if 'assert' in blk and re.search(r'(os\.path\.isdir\(|glob\(|listdir\(|os\.access\(|os\.stat\(|getsize\()',blk) and c1.classify_test(blk) not in ('P1',):
            miss.append((t,name,c1.classify_test(blk)))
print('presence-like calls outside frozen PRESENCE in non-P1 tests:',len(miss),miss[:10])
# curl trailing-space gap
cur=[(t) for t,pg,body,_,_ in rows if re.search(r"curl(?! )",body)]
print('files with bare curl token not followed by space:',cur)
# assert.*in marker effect file level
assertin=[t for t,pg,body,i,s in rows if re.search(r'assert.*\bin\b',body) and c1.CONTENT.search(body) and not re.search(r'(read_text|read_bytes|open\(|json\.load|re\.(search|match|findall|finditer)|\.decode\(|\.strip\(\)|\.splitlines\()',body)]
print('files whose CONTENT is ONLY the undisclosed assert-in marker:',assertin)
print('os.path.isfile occurrences files:',[t for t,pg,body,_,_ in rows if 'os.path.isfile' in body])
print('tasks sum of tasks lists:',sum(len(v) for v in pop['tasks'].values()),'capture_population sum:',sum(len(v) for v in pop['capture_population'].values()))

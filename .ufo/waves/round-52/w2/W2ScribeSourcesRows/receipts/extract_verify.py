# Deterministic rendering + quote check for the S179-S193 draft rows (2026-10-28 fetches).
import re, html, json, subprocess, os, sys
from html.parser import HTMLParser
BASE='/fast/scratch/hyaku/kengaku-r52/w2-W2ScribeSourcesRows'
os.chdir(BASE)
class T(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in ('script','style','noscript'): s.skip+=1
        if t in ('br','p','div','li','tr','h1','h2','h3','h4','h5','h6','section','blockquote','pre','td','th','dt','dd','figcaption'): s.out.append('\n')
    def handle_endtag(s,t):
        if t in ('script','style','noscript'): s.skip-=1
        if t in ('p','div','li','tr','h1','h2','h3','h4','h5','h6','section','blockquote','pre','td','th'): s.out.append('\n')
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
def render(p):
    t=T(); t.feed(open(p,encoding='utf-8',errors='replace').read())
    out=[]
    for l in ''.join(t.out).split('\n'):
        l=re.sub(r'\s+',' ',l).strip()
        if l: out.append(l)
    return out
os.makedirs('txt',exist_ok=True)
docs={}
docs['tbench21']=render('pa/tbench21.html')
docs['hf-zai']=render('pa/hf-zai.html')
docs['arxiv-2605-26079-html']=render('pa/arxiv-2605-26079-html.html')
docs['arxiv-2601-11868-html']=render('pa/arxiv-2601-11868-html.html')
docs['arxiv-2503-15223-abs']=render('pa/arxiv-2503-15223-abs.html')
docs['june']=render('pa/june.html')
docs['snorkel']=render('pa/snorkel.html')
docs['gh-issue-1387']=render('pa/gh-issue-1387.html')
docs['readme']=open('fetch/README.md',encoding='utf-8').read().split('\n')
docs['pr53-body']=open('txt/pr53-body.txt',encoding='utf-8').read().split('\n')
for k,v in docs.items():
    open(f'txt/{k}.lines.txt','w').write('\n'.join(f'{i+1}\t{l}' for i,l in enumerate(v))+'\n')
pdf=subprocess.run(['pdftotext','-f','3','-l','3','-layout','pa/tsdetect.pdf','-'],capture_output=True,text=True).stdout.split('\n')
docs['tsdetect-p3']=pdf
docs['bn']=open('fetch/bn-fit-modify_tests_test_outputs.py',encoding='utf-8').read().split('\n')
docs['pmr']=open('fetch/pytorch-model-recovery_tests_test_outputs.py',encoding='utf-8').read().split('\n')
docs['tp']=open('fetch/torch-tensor-parallelism_tests_test_outputs.py',encoding='utf-8').read().split('\n')
Q=[
 ('S179','tree-2fd12b88.json','"sha":"2fd12b88aafdd04a52c298e3940bcb189f9766d6"',None),
 ('S180','readme','Each task in TB2.0 has received several hours of human and LM-assisted validation',None),
 ('S181','bn','Test that the sampled data from the fitted BN exists',None),
 ('S182','pmr','Checks if the model file exists',None),
 ('S183','tp','Checks that the agent creates a file named parallel_linear.py',"in the expected directory."),
 ('S184','pr53-body','Tests were updated when they over-specified or let any solution pass.',None),
 ('S185','tbench21','Some tasks had instructions that were not aligned to their tests.',None),
 ('S186','hf-zai','the test logic itself misjudged valid submissions or let non-compliant outputs through',None),
 ('S187','arxiv-2605-26079-html','Our trajectory audit independently recovered 14 of these 21 issues under strict matching',None),
 ('S188','arxiv-2503-15223-abs',"a patch may pass the tests but nevertheless fail to match the developers' expectations.",None),
 ('S189','tsdetect-p3','A test method that does not contain a single assertion statement and @Test(expected) annotation parameter',None),
 ('S190','arxiv-2601-11868-html','A terminal bench task is considered well-specified if the unit tests will pass if and only if the container ends in an acceptable state.',None),
 ('S191','june','On Terminal-Bench 2.1, 40 of 83 gold-passing tasks (48%) certify success after a careless deletion',None),
 ('S192','gh-issue-1387','Verifiers that grade against a golden artifact instead of solution properties',None),
 ('S193','snorkel','A revision of Terminal-Bench 2.0 that fixes 28 of 89 tasks and introduces continuous validation for agentic benchmarks.',None),
]
ok=True
for sid,key,q,nxt in Q:
    if key.startswith('tree'):
        lines=open('pa/'+key,encoding='utf-8').read().split('\n')
    else:
        lines=docs[key]
    hits=[i+1 for i,l in enumerate(lines) if q in l]
    extra=''
    if nxt:
        h2=[i+1 for i,l in enumerate(lines) if nxt in l]
        extra=f' next-line-hits={[h+1 for h in hits if h+1 in h2]}'
    nw=len(q.split())
    if not hits: ok=False
    print(f'{sid} key={key} hits={hits} words={nw}{extra}')
print('ALL-FOUND' if ok else 'SOME-MISSING')

import importlib.util, json, re, sys, io, tokenize
L='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
sp=importlib.util.spec_from_file_location('c1',L+'/plans/round52_c1_grader_audit.py');c1=importlib.util.module_from_spec(sp);sp.loader.exec_module(c1)
pop=json.load(open(L+'/plans/round52-tasks.json'))['tasks']
def tight_blocks(body):
    """function body only (def line through the last indented line), comments dropped"""
    lines=body.split('\n'); out=[]; i=0
    while i<len(lines):
        m=re.match(r'^def\s+(test_\w+)\s*\(',lines[i])
        if m:
            j=i+1
            while j<len(lines) and (lines[j].strip()=='' or lines[j][:1] in (' ','\t')): j+=1
            blk='\n'.join(l for l in lines[i:j] if not l.lstrip().startswith('#'))
            out.append((m.group(1),blk)); i=j
        else: i+=1
    return out
loose=tight=0; ntests=0; flips=[]; ltasks=set(); ttasks=set()
for t,files in sorted(pop.items()):
    g=c1.primary_grader(files); p=L+'/corpus/evidence/round52/graders/'+g
    try: body=open(p,errors='replace').read()
    except FileNotFoundError: continue
    A={n:c1.classify_test(b) for n,b in c1.split_tests(body)}
    B={n:c1.classify_test(b) for n,b in tight_blocks(body)}
    ntests+=len(A)
    for n in A:
        if A[n]=='P1': loose+=1; ltasks.add(t)
        if B.get(n)=='P1': tight+=1; ttasks.add(t)
        if A[n]!=B.get(n): flips.append((t,n,A[n],B.get(n)))
print('tests',ntests,'P1 as-committed',loose,'tasks',len(ltasks),'| P1 tight(body-only, no comment lines)',tight,'tasks',len(ttasks))
print('class changes',len(flips)); 
for f in flips: print(' ',f)
print('newly P1 tasks',sorted(ttasks-ltasks)); print('lost P1 tasks',sorted(ltasks-ttasks))

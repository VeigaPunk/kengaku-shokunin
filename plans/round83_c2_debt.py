#!/usr/bin/env python3
"""R83-C2: eight frozen outside debts, actual source/repair/check bindings.

Axes: coverage and calibration. --rev reads revision evidence, never a current
ledger fallback. The current checks remain the instrument in all modes.
"""
from __future__ import annotations
import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

BASE='614f00559c75155ec100e945b3e8257b14fb7496'
SPOT='corpus/lessons/round-82-verifier-spotcheck.md'
LESSON='corpus/lessons/round-83.md'
LEDGER='corpus/routed-findings.jsonl'
CHECK='plans/round83_c2_checks.py'
INSTRUMENT=Path(__file__).with_name('round83_c2_checks.py')


def git(root,*args,binary=False):
    p=subprocess.run(['git','-C',str(root.resolve()),*args],capture_output=True,text=not binary)
    if p.returncode: raise ValueError('git failed: '+' '.join(args))
    return p.stdout


def universe(origin):
    body=git(origin,'show',BASE+':'+SPOT)
    section=re.search(r'^## 6\. Routed defects.*?(?=^## 7\.|\Z)',body,re.S|re.M)
    if not section: raise ValueError('frozen section 6 absent')
    result={}
    for line_no,line in enumerate(body.splitlines(),1):
        m=re.match(r'^- \*\*V([1-8]) · ',line)
        if m and line in section.group(0): result['R82-V'+m.group(1)]=line_no
    if len(result)!=8: raise ValueError('frozen universe is not eight ids')
    return result


def materialise(origin,rev,work):
    dst=Path(tempfile.mkdtemp(prefix='tree-',dir=work))
    archive=git(origin,'archive',rev,binary=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
        tf.extractall(dst,filter='data')
    return dst


def read(root,path):
    p=root/path
    return p.read_text() if p.is_file() else ''


def rows(root):
    out={}; duplicates=[]
    for number,line in enumerate(read(root,LEDGER).splitlines(),1):
        if not line.strip(): continue
        try: r=json.loads(line)
        except json.JSONDecodeError as e: raise ValueError('malformed ledger line %d'%number) from e
        if not isinstance(r,dict) or not isinstance(r.get('id'),str): raise ValueError('ledger row lacks id')
        if r['id'] in out: duplicates.append(r['id'])
        out[r['id']]=r
    return out,duplicates


def run_check(root,n,origin):
    env=os.environ.copy()
    env['R83_ORIGIN_REPO']=str(origin.resolve())
    env['R83_FLEET_REPO']=str(Path(os.environ.get('R83_FLEET_REPO',str(origin.resolve().parent))).resolve())
    env['PYTHONDONTWRITEBYTECODE']='1'
    p=subprocess.run([sys.executable,str(INSTRUMENT),'v'+str(n)],cwd=root,env=env,capture_output=True,text=True,timeout=60)
    print(p.stdout,end='')
    if p.stderr: print('CHECK-STDERR '+p.stderr.strip())
    return p.returncode


def evaluate(root,origin,tracked):
    ids=universe(origin); data,dups=rows(root); defects=[]
    for rid in dups: defects.append(('DUPLICATE-ROW',rid))
    print('UNIVERSE spotcheck=%s ids=8 %s'%(SPOT,','.join(ids)))
    source_lines=read(root,SPOT).splitlines()
    if read(root,SPOT)!=git(origin,'show',BASE+':'+SPOT): defects.append(('SOURCE-CHANGED',SPOT))
    closed=passed=0
    for rid,line in ids.items():
        r=data.get(rid)
        if r is None:
            defects.append(('DEBT-UNREGISTERED',rid)); continue
        n=int(rid[-1]); check=r.get('check',''); literal=r.get('evidence_literal','')
        if not isinstance(check,str): check=''
        print('DEBT %s status=%s close=%s'%(rid,r.get('status'),r.get('close')))
        if r.get('status')!='closed': defects.append(('NOT-CLOSED',rid))
        else: closed+=1
        if r.get('source')!=SPOT+':'+str(line) or SPOT not in tracked or len(source_lines)<line or not source_lines[line-1].startswith('- **V%d · '%n):
            defects.append(('SOURCE-LINE',rid))
        close_value=r.get('close','')
        close=close_value.split('#',1)[0].split(' ',1)[0] if isinstance(close_value,str) else ''
        if close!=LESSON or close not in tracked: defects.append(('CLOSE-UNRESOLVED',rid))
        body=read(root,LESSON)
        paragraphs=re.split(r'\n\s*\n|\n(?=###? |- \*\*R82-V\d)',body)
        repair='\n'.join(p for p in paragraphs if re.search(r'\b'+rid+r'\b',p))
        if not repair: defects.append(('CLOSE-NO-ID',rid))
        if not isinstance(literal,str) or not literal.strip() or literal not in repair: defects.append(('CLOSE-NO-EVIDENCE',rid))
        evidence=[]
        if n==2: evidence=['corpus/evidence/round83/r82-census-after.txt']
        if n==3: evidence=['.ufo/waves/round-82/w1/w1-results.json','corpus/evidence/round83/r82-seat-census.json' if 'r82-seat-census.json' in repair else 'corpus/evidence/round83/r82-seat-counts.json']
        for path in evidence:
            if path not in tracked: defects.append(('EVIDENCE-UNTRACKED',rid+' '+path))
        if check!='python3 '+CHECK+' v'+str(n):
            defects.append(('CHECK-TRIVIAL' if check.strip() in ('true',':','exit 0','') else 'CHECK-BINDING',rid)); continue
        rc=run_check(root,n,origin)
        if rc==0: passed+=1
        else: defects.append(('CHECK-FAIL',rid+' rc='+str(rc)))
    index_rows=[line for line in read(root,'corpus/README.md').splitlines() if line.lstrip().startswith('|')]
    indexed=any('lessons/round-82-verifier-spotcheck.md' in l and len(l.strip().strip('|').split('|'))==3 for l in index_rows)
    if not indexed: defects.append(('INDEX-MISSING',SPOT))
    for code,detail in defects: print('DEFECT %s %s'%(code,detail))
    print('DEFECTS n=%d'%len(defects))
    print('TARGET ids=8 closed=%d checks_passed=%d indexed=%s defects=%d'%(closed,passed,'yes' if indexed else 'no',len(defects)))
    print('PREDICATE R83-C2 '+('fail' if defects else 'pass'))
    return int(bool(defects))


def proposed_rows(origin):
    literals=['S262=4 S263=2','W04=27','affected=6 unrecovered=2 recovered=4','82fe89d5','three-cell README rows','S265 and S266','seven of ten new registry rows declare selftests','07:24-03:00=10:24Z']
    return [dict(id=rid,status='closed',source=SPOT+':'+str(line),close=LESSON,evidence_literal=literals[int(rid[-1])-1],check='python3 '+CHECK+' v'+rid[-1]) for rid,line in universe(origin).items()]


def write(root,path,body):
    p=root/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(body)


def fixture(origin,work):
    """Base evidence plus real byte repairs; no injected checker or fake git facts."""
    root=materialise(origin,BASE,work)
    source=read(root,'corpus/SOURCES.md')
    lines=source.splitlines()
    for old,new,old_count,new_count in [('S262','S268','(6 words','(4 words'),('S263','S269','(1 word','(2 words')]:
        original=next(l for l in lines if l.startswith('| '+old+' |'))
        c=[v.strip() for v in original.strip('|').split('|')]
        c[0]=new; c[5]=c[5].replace(old_count,new_count); c[6]='supersedes '+old+' — '+c[6]
        lines.append('| '+' | '.join(c)+' |')
    c=[v.strip() for v in next(l for l in lines if l.startswith('| S264 |')).strip('|').split('|')]
    c[0]='S270'; c[6]='supersedes S264 — REJECTED: missing locator; flip: pinned file appears'; lines.append('| '+' | '.join(c)+' |')
    write(root,'corpus/SOURCES.md','\n'.join(lines)+'\n')
    p=['R82-V1 S262=4 S263=2 corrects round-82 Gate and report annotations.',
       'R82-V2 W04=27 supersedes reported 26 after-count.',
       'R82-V3 affected=6 unrecovered=2 recovered=4 '+', '.join(['SweepGateR82','SweepHarvestR82','ReviewerR82','CriticR82','MutationR82','RegistryCounterR82'])+'; final outputs are separate from provider interruptions.',
       'R82-V4 82fe89d5 added plans/round82_c2_closure_debt.py and plans/round82_c2_checks.py; not c804dd41.',
       'R82-V5 three-cell README rows.',
       'R82-V6 S265 and S266 correct the Gate omission.',
       'R82-V7 seven of ten new registry rows declare selftests; round37-c1-attribution, round80-c1-remint, round82-c2-checks are none declared.',
       'R82-V8 07:24-03:00=10:24Z; local -03:00, not Z. This round uses UTC.']
    gate='## Gate\n\nS265 2026-11-04 corpus/evidence/round81/log-summary-date-ranges-probe.txt:1 “# tb2 log-summary-date-ranges grader probe (round 81)”\n\nS266 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/instruction.md 2026-11-04 :9 “Write a CSV file /app/summary.csv with the following structure (including the header):”\n\n## Corrections\n\n'
    write(root,LESSON,gate+'\n\n'.join(p)+'\n')
    readme=read(root,'corpus/README.md')
    paths=['lessons/round-82.md','lessons/round-81-verifier-spotcheck.md','lessons/round-82-verifier-spotcheck.md']
    readme='\n'.join(l for l in readme.splitlines() if not any(path in l for path in paths))
    write(root,'corpus/README.md',readme+'\n'+'\n'.join('| `'+path+'` | lesson | correction |' for path in paths)+'\n')
    before=read(root,'corpus/evidence/round82/census-before.txt')
    output='\n'.join(l.replace('kengaku\t','file\t',1) for l in before.splitlines() if '\tW04\t' in l)+'\n'
    output+='file\tW04\tS266 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/instruction.md across scopes\n'
    measured=str(root/'corpus/SOURCES.md')
    output+='file\tok\t'+measured+'\n'
    write(root,'corpus/evidence/round83/r82-census-after.txt','COMMAND /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file '+measured+'\nREV a44b2f083ee8b4115aea64598646f4bd9e3c1470\nEXIT 0\nSTDOUT_BEGIN\n'+output+'STDOUT_END\nSTDERR_BEGIN\nSTDERR_END\n')
    import hashlib
    raw=read(root,'.ufo/waves/round-82/w1/w1-results.json')
    receipt=dict(source='.ufo/waves/round-82/w1/w1-results.json',source_sha256=hashlib.sha256(raw.encode()).hexdigest(),seats=12,final_terminal=10,final_empty=1,final_unstructured=1,affected=['SweepGateR82','SweepHarvestR82','ReviewerR82','CriticR82','MutationR82','RegistryCounterR82'],unrecovered=['SweepGateR82','RegistryCounterR82'],recovered=['SweepHarvestR82','ReviewerR82','CriticR82','MutationR82'])
    write(root,'corpus/evidence/round83/r82-seat-counts.json',json.dumps(receipt))
    write(root,LEDGER,read(root,LEDGER)+'\n'+'\n'.join(json.dumps(r) for r in proposed_rows(origin))+'\n')
    tracked=set(git(origin,'ls-tree','-r','--name-only',BASE).splitlines())|{LESSON,'corpus/evidence/round83/r82-census-after.txt','corpus/evidence/round83/r82-seat-counts.json'}
    return root,tracked


def battery(origin,work,mode):
    mutations=[('source','SOURCE-LINE'),('literal','CLOSE-NO-EVIDENCE'),('trivial','CHECK-TRIVIAL'),('missing-row','DEBT-UNREGISTERED'),('index','INDEX-MISSING'),('nonclosed','NOT-CLOSED'),('duplicate','DUPLICATE-ROW'),('contradiction-v3','CHECK-FAIL R82-V3'),('contradiction-v7','CHECK-FAIL R82-V7'),('forged-v2','CHECK-FAIL R82-V2'),('forged-v6','CHECK-FAIL R82-V6')]+[('repair-v'+str(n),'CHECK-FAIL R82-V'+str(n)) for n in range(1,9)]
    cases=[('green','')]+mutations if mode=='selftest' else mutations
    failures=0; red=0
    for name,want in cases:
        root,tracked=fixture(origin,work)
        try:
            data=[json.loads(l) for l in read(root,LEDGER).splitlines() if l.strip()]
            first=next(r for r in data if r['id']=='R82-V1')
            if name=='source': first['source']=SPOT+':1'
            elif name=='literal': first['evidence_literal']='absent literal'
            elif name=='trivial': first['check']='true'
            elif name=='missing-row': data=[r for r in data if r['id']!='R82-V1']
            elif name=='nonclosed': first['status']='open'
            elif name=='duplicate': data.append(first.copy())
            elif name=='index': write(root,'corpus/README.md','')
            elif name=='contradiction-v3': write(root,LESSON,read(root,LESSON).replace('R82-V3 ','R82-V3 The corrected affected count is five, not six. Historical claim: '))
            elif name=='contradiction-v7': write(root,LESSON,read(root,LESSON).replace('R82-V7 ','R82-V7 All ten now declare selftests. Historical claim: '))
            elif name=='forged-v2':
                body=read(root,'corpus/evidence/round83/r82-census-after.txt')
                write(root,'corpus/evidence/round83/r82-census-after.txt',re.sub(r'duplicate url [^\n]+','fabricated warning',body))
            elif name=='forged-v6':
                lesson=read(root,LESSON)
                write(root,LESSON,re.sub(r'## Gate.*?## Corrections','## Gate\n\nS265 S266 https://example.invalid/unrelated 2026-11-04 :1 “unrelated invented quote”\n\n## Corrections',lesson,flags=re.S))
            elif name.startswith('repair-v'):
                n=int(name[-1]); paths={1:'corpus/SOURCES.md',2:'corpus/evidence/round83/r82-census-after.txt',3:'corpus/evidence/round83/r82-seat-counts.json',4:LESSON,5:'corpus/README.md',6:'corpus/SOURCES.md',7:'SKILL.md',8:LESSON}
                path=paths[n]
                if n in (4,8): write(root,path,read(root,path).replace('R82-V'+str(n),'REMOVED-ID'))
                elif n==7: write(root,path,read(root,path).replace('none declared','selftest now'))
                else: write(root,path,'corrupted actual repair data\n')
            write(root,LEDGER,'\n'.join(json.dumps(r) for r in data)+'\n')
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf): rc=evaluate(root,origin,tracked)
            print(buf.getvalue(),end='')
            caught=rc==0 if name=='green' else rc==1 and ('DEFECT '+want) in buf.getvalue()
            red+=rc==1; failures+=not caught
            print(('CASE' if mode=='selftest' else 'MUTANT')+' '+name+' '+('ok' if caught else 'FAIL'))
        finally: shutil.rmtree(root)
    if mode=='selftest': print('SELFTEST cases=%d red=%d failures=%d'%(len(cases),red,failures))
    else: print('MUTANTS real=%d killed=%d survived=%d'%(len(cases),len(cases)-failures,failures))
    return int(bool(failures))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lane',default='.')
    ap.add_argument('--rev')
    ap.add_argument('--work',required=True)
    modes=ap.add_mutually_exclusive_group()
    modes.add_argument('--selftest',action='store_true')
    modes.add_argument('--mutants',action='store_true')
    modes.add_argument('--control-presence',action='store_true')
    modes.add_argument('--sensitivity',action='store_true')
    a=ap.parse_args(); origin=Path(a.lane).resolve(); work=Path(a.work).resolve(); work.mkdir(parents=True,exist_ok=True)
    os.environ['TMPDIR']=str(work); tempfile.tempdir=str(work)
    try:
        if a.selftest or a.mutants: return battery(origin,work,'selftest' if a.selftest else 'mutants')
        if a.sensitivity:
            root=materialise(origin,BASE,work)
            try:
                failed=sum(run_check(root,n,origin)!=0 for n in range(1,9))
                print('SENSITIVITY n=8 failed_at_base=%d'%failed)
                return 0 if failed==8 else 1
            finally: shutil.rmtree(root)
        if a.control_presence:
            root=materialise(origin,BASE,work)
            try:
                write(root,LEDGER,read(root,LEDGER)+'\n'+'\n'.join(json.dumps(r) for r in proposed_rows(origin)))
                tracked=set(git(origin,'ls-tree','-r','--name-only',BASE).splitlines())
                rc=evaluate(root,origin,tracked)
                print('CONTROL presence target_reached=%s'%str(rc==0))
                return 0 if rc==1 else 1
            finally: shutil.rmtree(root)
        if a.rev:
            root=materialise(origin,a.rev,work)
            try: return evaluate(root,origin,set(git(origin,'ls-tree','-r','--name-only',a.rev).splitlines()))
            finally: shutil.rmtree(root)
        return evaluate(origin,origin,set(git(origin,'ls-files').splitlines()))
    except (ValueError,OSError,subprocess.TimeoutExpired,tarfile.TarError) as e:
        print('SETUP '+str(e)); return 2

if __name__=='__main__': sys.exit(main())

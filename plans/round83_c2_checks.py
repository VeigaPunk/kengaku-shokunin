#!/usr/bin/env python3
"""R83-C2 independent evidence checks; current instrument, measured-tree evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

BASE = '614f00559c75155ec100e945b3e8257b14fb7496'
TIP82 = 'a44b2f083ee8b4115aea64598646f4bd9e3c1470'
LESSON = 'corpus/lessons/round-83.md'
RESULTS = '.ufo/waves/round-82/w1/w1-results.json'
REPORT = '.ufo/reports/round-82/kengaku.md'
TOOLS = ['plans/round82_c2_closure_debt.py', 'plans/round82_c2_checks.py']
NAMES = ['SweepGateR82','SweepHarvestR82','ReviewerR82','CriticR82','MutationR82','RegistryCounterR82']
EXCEPTIONS = ['round37-c1-attribution','round80-c1-remint','round82-c2-checks']
REGISTRY = ['log-appendonly','round37-c1-attribution','round66-registry-check','round80-c1-remint','round81-log-summary-probe','round81-vulnerable-secret-probe','round82-c3-sweep','round82-c1-plans-registry','round82-c2-closure-debt','round82-c2-checks']
ROOT = Path.cwd()

def text(path):
    p = ROOT / path
    return p.read_text() if p.is_file() else ''

def git(*args):
    origin = Path(os.environ.get('R83_ORIGIN_REPO', str(ROOT))).resolve()
    p = subprocess.run(['git','-C',str(origin),*args],capture_output=True,text=True)
    if p.returncode:
        raise ValueError('git evidence unavailable: '+ ' '.join(args))
    return p.stdout

def frozen(path):
    return git('show', BASE+':'+path)

def cells(line):
    return [x.strip() for x in line.strip().strip('|').split('|')]

def source_rows(body):
    out={}
    for line in body.splitlines():
        if not line.startswith('| S'): continue
        c=cells(line)
        if len(c)!=11: raise ValueError('malformed SOURCES row')
        if c[0] in out: raise ValueError('duplicate SOURCES id '+c[0])
        out[c[0]]=c
    return out

def paragraph(n):
    body = text(LESSON)
    # Corrections are paragraph-bound: an id elsewhere cannot license unrelated data.
    parts = re.split(r'\n\s*\n|\n(?=###? |- \*\*R82-V\d)',body)
    return '\n'.join(p for p in parts if re.search(r'\bR82-V'+str(n)+r'\b',p))

def immutable_sources(ids):
    old,new = source_rows(frozen('corpus/SOURCES.md')),source_rows(text('corpus/SOURCES.md'))
    return all(i in new and new[i] == old[i] for i in ids)

def v1(p):
    rows=source_rows(text('corpus/SOURCES.md'))
    if not immutable_sources(['S262','S263']): return False
    for new,old,quote,want,path in [('S268','S262','echo 1 > /logs/verifier/reward.txt',4,'corpus/evidence/round82/fetch/log-summary-date-ranges_tests_test.sh'),('S269','S263','-w requests==2.32.4',2,'corpus/evidence/round82/fetch/nginx-request-logging_tests_test.sh')]:
        r=rows.get(new)
        if not r or ('supersedes '+old) not in r[6]: return False
        pairs=re.findall(r'[“\"]([^”\"]+)[”\"]\s*\((\d+) words?\b',r[5])
        if not pairs or any(len(q.split()) != int(n) for q,n in pairs): return False
        if (quote,str(want)) not in pairs or quote not in frozen(path) or text(path)!=frozen(path): return False
        if quote not in p and not ('S262=4 S263=2' in p): return False
    return (all(s in p for s in ['round82','Gate','report']) or all(s in p for s in ['round-82','Gate','report']))

def v2(p):
    t=text('corpus/evidence/round83/r82-census-after.txt')
    command=re.search(r'^COMMAND (.+)$',t,re.M)
    if not command: return False
    cmd=re.fullmatch(r'(\S*/scripts/sources-census\.sh) validate --file (/\S+/corpus/SOURCES\.md)',command.group(1))
    if not cmd: return False
    block=re.search(r'^STDOUT_BEGIN\n(.*?)^STDOUT_END$',t,re.S|re.M)
    if not block: return False
    expected=[l.replace('kengaku\t','file\t',1) for l in frozen('corpus/evidence/round82/census-before.txt').splitlines() if '\tW04\t' in l]
    expected.append('file\tW04\tS266 duplicate url raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/instruction.md across scopes')
    expected.append('file\tok\t'+cmd.group(2))
    return (block.group(1).splitlines()==expected and len(expected)==28 and
            re.search(r'^REV '+TIP82+r'$',t,re.M) is not None and
            re.search(r'^EXIT 0$',t,re.M) is not None and
            '26' in p and '27' in p and 'supersed' in p.lower())

def seat_counts(raw):
    rows=json.loads(raw)['results']
    terminal=empty=unstructured=0
    for r in rows:
        output=r.get('output') or ''
        if not output.strip(): empty+=1; continue
        try: parsed=json.loads(output)
        except json.JSONDecodeError: parsed=None
        if isinstance(parsed,dict): terminal+=1
        else: unstructured+=1
    return dict(seats=len(rows),final_terminal=terminal,final_empty=empty,final_unstructured=unstructured)

def v3(p):
    raw=text(RESULTS)
    path='corpus/evidence/round83/r82-seat-census.json' if 'r82-seat-census.json' in p else 'corpus/evidence/round83/r82-seat-counts.json'
    receipt=json.loads(text(path))
    counts=seat_counts(raw)
    normalized=p.lower().replace('`','')
    numeric={'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}
    assertions=re.findall(r'\b(affected|unrecovered|recovered)(?: count)?\s*(?:is|=)\s*(\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten)\b',normalized)
    if any((int(v) if v.isdigit() else numeric[v]) != {'affected':6,'unrecovered':2,'recovered':4}[k] for k,v in assertions): return False
    return (raw==frozen(RESULTS) and counts==dict(seats=12,final_terminal=10,final_empty=1,final_unstructured=1) and
            all(receipt.get(k)==v for k,v in counts.items()) and receipt.get('source')==RESULTS and
            receipt.get('source_sha256')==hashlib.sha256(raw.encode()).hexdigest() and
            set(receipt.get('affected',[]))==set(NAMES) and
            set(receipt.get('unrecovered',[]))=={'SweepGateR82','RegistryCounterR82'} and
            set(receipt.get('recovered',[]))==set(NAMES)-{'SweepGateR82','RegistryCounterR82'} and
            all(n in p for n in NAMES) and 'final' in p.lower() and 'provider' in p.lower() and
            all(re.search(r'\b'+k+r'\s*=\s*'+str(v)+r'\b',p) for k,v in [('affected',6),('unrecovered',2),('recovered',4)]))

def v4(p):
    additions=git('diff-tree','--root','--no-commit-id','--name-only','--diff-filter=A','-r','82fe89d5').splitlines()
    return '82fe89d5' in p and all(t in additions and t in p for t in TOOLS) and 'c804dd41' in p

def v5(p):
    rows=[cells(l) for l in text('corpus/README.md').splitlines() if l.lstrip().startswith('|')]
    for path in ['lessons/round-82.md','lessons/round-81-verifier-spotcheck.md','lessons/round-82-verifier-spotcheck.md']:
        matching=[r for r in rows if any(re.search(r'(?<![\w/-])'+re.escape(path)+r'(?![\w.-])',c) for c in r)]
        if len(matching)!=1 or len(matching[0])!=3 or not all(matching[0]): return False
    return True

def v6(p):
    rows=source_rows(text('corpus/SOURCES.md'))
    r=rows.get('S270')
    if not immutable_sources(['S264','S265','S266']) or not r: return False
    if not re.match(r'^supersedes S264 — REJECTED: .+; flip: .+',r[6]) or r[7]!='rejected': return False
    body=text(LESSON)
    match=re.search(r'^## Gate\b(.*?)(?=^## |\Z)',body,re.S|re.M)
    if not match: return False
    gate=match.group(1)
    pin='https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/'
    requirements=[
        ('S265','corpus/evidence/round81/log-summary-date-ranges-probe.txt',1,'# tb2 log-summary-date-ranges grader probe (round 81)'),
        ('S266',pin+'log-summary-date-ranges/instruction.md',9,'Write a CSV file /app/summary.csv with the following structure (including the header):')]
    for ident,location,line,quote in requirements:
        entries=[b for b in gate.splitlines() if re.search(r'\b'+ident+r'\b',b) and location in b]
        if not any('2026-11-04' in b and re.search(r':'+str(line)+r'\b',b) and '“'+quote+'”' in b for b in entries): return False
        if not 0<len(quote.split())<=25: return False
    receipt=text('corpus/evidence/round81/log-summary-date-ranges-probe.txt').splitlines()
    if not receipt or receipt[0]!=requirements[0][3]: return False
    return all(x in p for x in ['S265','S266']) and ('Gate' in p)

def v7(p):
    selected={}
    for line in text('SKILL.md').splitlines():
        if not line.lstrip().startswith('|'): continue
        c=cells(line)
        if len(c)==8 and c[0].strip('`') in REGISTRY:
            name=c[0].strip('`')
            if name in selected: return False
            selected[name]=c[4]
    missing=sorted(k for k,v in selected.items() if v.strip('`')=='none declared')
    declared= 'seven of ten' in p.lower() or re.search(r'selftest_declared\s*=\s*7 of 10',p)
    if re.search(r'\b(?:all|each of the) (?:ten|10)\b.{0,40}\b(?:declare|carry|have)\b.{0,20}\bselftests?\b',p,re.I): return False
    declared_rows=[v for v in selected.values() if v.strip('`')!='none declared']
    return bool(declared) and len(selected)==10 and missing==sorted(EXCEPTIONS) and all(n in p for n in EXCEPTIONS) and len(declared_rows)==7 and all('python3 ' in v for v in declared_rows)

def v8(p):
    # round-92 M6: the fleet repo resolves from SHOKUNIN_ROOT (or R83_FLEET_REPO) first;
    # origin.parent stays only as the last fallback so the check is not clone-path dependent.
    explicit=os.environ.get('R83_FLEET_REPO') or os.environ.get('SHOKUNIN_ROOT')
    origin=Path(os.environ.get('R83_ORIGIN_REPO',str(ROOT))).resolve()
    fleet=Path(explicit if explicit else str(origin.parent)).resolve()
    old=subprocess.run(['git','-C',str(fleet),'show','c839b658102dbcc401c78bbb7ea3bb47f11a333d:'+REPORT],capture_output=True)
    current=fleet/REPORT
    preserved=old.returncode==0 and current.is_file() and current.read_bytes()==old.stdout
    return (preserved and all(s in p for s in ['07:24','-03:00','10:24Z','UTC']) and
            ('not Z' in p or 'not UTC' in p or 'incorrect' in p.lower() or 'label correction' in p.lower()))

CHECKS=[v1,v2,v3,v4,v5,v6,v7,v8]

def check(n):
    p=paragraph(n)
    try:
        ok=bool(p) and CHECKS[n-1](p)
    except (ValueError,KeyError,TypeError,OSError,IndexError) as e:
        print('CHECK v%d fail: %s'%(n,e)); return 1
    print('CHECK v%d %s'%(n,'ok' if ok else 'fail'))
    return 0 if ok else 1

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('check',nargs='?',choices=['v'+str(n) for n in range(1,9)])
    ap.add_argument('--all',action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--work', type=Path)
    a=ap.parse_args()
    if a.selftest:
        if not a.work:
            ap.error('--selftest requires --work DIR')
        origin = Path(os.environ.get('R83_ORIGIN_REPO', str(ROOT))).resolve()
        # Reuse the real-byte fixtures; the debt driver invokes this CLI per id.
        driver = Path(__file__).with_name('round83_c2_debt.py')
        return subprocess.run(
            [sys.executable, str(driver), '--lane', str(origin), '--selftest',
             '--work', str(a.work.resolve())], check=False).returncode
    if a.all: return max(check(n) for n in range(1,9))
    if not a.check: ap.error('check or --all required')
    return check(int(a.check[1:]))

if __name__=='__main__': sys.exit(main())

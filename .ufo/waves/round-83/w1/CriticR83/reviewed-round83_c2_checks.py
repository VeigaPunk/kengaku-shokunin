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
SPOT = 'corpus/lessons/round-82-verifier-spotcheck.md'
LESSON = 'corpus/lessons/round-83.md'
RESULTS = '.ufo/waves/round-82/w1/w1-results.json'
REPORT = '.ufo/reports/round-82/kengaku.md'
TOOLS = ['plans/round82_c2_closure_debt.py', 'plans/round82_c2_checks.py']
NAMES = ['SweepGateR82','SweepHarvestR82','ReviewerR82','CriticR82','MutationR82','RegistryCounterR82']
EXCEPTIONS = ['round37-c1-attribution','round80-c1-remint','round82-c2-checks']
REGISTRY = ['log-appendonly','round37-c1-attribution','round66-registry-check','round80-c1-remint','round81-log-summary-probe','round81-vulnerable-secret-probe','round82-c3-sweep','round82-c1-plans-registry','round82-c2-closure-debt','round82-c2-checks']
LITERALS = ['S262=4 S263=2','W04=27','affected=6 unrecovered=2 recovered=4','82fe89d5','three-cell README rows','S265 and S266','seven of ten new registry rows declare selftests','07:24-03:00=10:24Z']
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
    return {c[0]:c for line in body.splitlines() if line.startswith('| S') and len(c:=cells(line)) == 11}

def paragraph(n):
    body = text(LESSON)
    # Corrections are paragraph-bound: an id elsewhere cannot license unrelated data.
    parts = re.split(r'\n\s*\n|\n(?=###? )',body)
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
        if (quote,str(want)) not in pairs or quote not in text(path): return False
    return all(s in p for s in ['round82','Gate','report']) or all(s in p for s in ['round-82','Gate','report'])

def v2(p):
    t=text('corpus/evidence/round83/r82-census-after.txt')
    warnings=[l for l in t.splitlines() if re.match(r'^kengaku\s+W04\s+',l)]
    ids=[re.search(r'W04\s+(S\d+)',l).group(1) for l in warnings]
    before=re.findall(r'^kengaku\s+W04\s+(S\d+)',frozen('corpus/evidence/round82/census-before.txt'),re.M)
    return (len(warnings)==27 and len(set(ids))==27 and set(ids)==set(before)|{'S266'} and
            re.search(r'^COMMAND .+sources-census',t,re.M) is not None and
            re.search(r'^REV '+TIP82+r'$',t,re.M) is not None and
            re.search(r'^EXIT 0$',t,re.M) is not None and
            re.search(r'^kengaku\s+ok\b',t,re.M) is not None and '26' in p and 'supersed' in p.lower())

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
    receipt=json.loads(text('corpus/evidence/round83/r82-seat-counts.json'))
    counts=seat_counts(raw)
    return (counts==dict(seats=12,final_terminal=10,final_empty=1,final_unstructured=1) and
            all(receipt.get(k)==v for k,v in counts.items()) and receipt.get('source')==RESULTS and
            receipt.get('source_sha256')==hashlib.sha256(raw.encode()).hexdigest() and
            set(receipt.get('affected',[]))==set(NAMES) and
            set(receipt.get('unrecovered',[]))=={'SweepGateR82','RegistryCounterR82'} and
            set(receipt.get('recovered',[]))==set(NAMES)-{'SweepGateR82','RegistryCounterR82'} and
            all(n in p for n in NAMES) and 'final' in p.lower() and 'provider' in p.lower())

def v4(p):
    additions=git('diff-tree','--root','--no-commit-id','--name-only','--diff-filter=A','-r','82fe89d5').splitlines()
    return all(t in additions and t in p for t in TOOLS) and 'c804dd41' in p

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
    for ident in ['S265','S266']:
        blocks=[b for b in re.split(r'\n\s*\n',gate) if ident in b]
        if not blocks: return False
        b='\n'.join(blocks)
        if not re.search(r'https?://\S+',b) or not re.search(r'2026-11-04',b): return False
        quotes=re.findall(r'[“\"]([^”\"\n]+)[”\"]',b)
        if not any(0<len(q.split())<=25 for q in quotes) or not re.search(r':\d+',b): return False
    return 'omission' in p.lower() or 'omitt' in p.lower()

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
    return len(selected)==10 and missing==sorted(EXCEPTIONS) and all(n in p for n in EXCEPTIONS)

def v8(p):
    origin=Path(os.environ.get('R83_ORIGIN_REPO',str(ROOT))).resolve()
    fleet=Path(os.environ.get('R83_FLEET_REPO',str(origin.parent))).resolve()
    old=subprocess.run(['git','-C',str(fleet),'show','c839b658102dbcc401c78bbb7ea3bb47f11a333d:'+REPORT],capture_output=True)
    current=fleet/REPORT
    preserved=old.returncode==0 and current.is_file() and current.read_bytes()==old.stdout
    return (preserved and all(s in p for s in ['-03:00','10:24Z','UTC']) and
            ('not Z' in p or 'not UTC' in p or 'incorrect' in p.lower()))

CHECKS=[v1,v2,v3,v4,v5,v6,v7,v8]

def check(n):
    p=paragraph(n)
    try:
        ok=bool(p) and LITERALS[n-1] in p and CHECKS[n-1](p)
    except (ValueError,KeyError,TypeError,OSError,IndexError) as e:
        print('CHECK v%d fail: %s'%(n,e)); return 1
    print('CHECK v%d %s'%(n,'ok' if ok else 'fail'))
    return 0 if ok else 1

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('check',nargs='?',choices=['v'+str(n) for n in range(1,9)])
    ap.add_argument('--all',action='store_true')
    a=ap.parse_args()
    if a.all: return max(check(n) for n in range(1,9))
    if not a.check: ap.error('check or --all required')
    return check(int(a.check[1:]))

if __name__=='__main__': sys.exit(main())

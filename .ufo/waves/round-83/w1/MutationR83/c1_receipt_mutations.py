#!/usr/bin/env python3
"""PROPOSED C1 actual-data battery; requires an already-green private fixture.

Never makes a receipt or implements a grader. Call with --fixture ABS --out ABS
--detector ARGV... . Detector argv must already point at the private fixture.
Only use below /fast/scratch/hyaku/kengaku-r83/MutationR83/. No git writes.
Runs the same detector pristine, mutated, restored; archives full stdout/stderr,
exit codes and file hashes. Non-green pristine/restored is inconclusive.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path


def sha(b): return hashlib.sha256(b).hexdigest() if b is not None else None

def main():
    p=argparse.ArgumentParser(); p.add_argument('--fixture',required=True);p.add_argument('--out',required=True)
    p.add_argument('--detector',nargs=argparse.REMAINDER,required=True);a=p.parse_args()
    root=Path(a.fixture).resolve();out=Path(a.out).resolve()
    assert str(root).startswith('/fast/scratch/hyaku/kengaku-r83/MutationR83/')
    receipt=root/'corpus/evidence/round83/code-from-image-probe.txt'
    ledger=root/'plans/grader-population-ledger.json'
    before={receipt:receipt.read_bytes(),ledger:ledger.read_bytes()}
    def run():
        r=subprocess.run(a.detector,cwd=root,capture_output=True,text=True,timeout=180)
        return dict(exit=r.returncode,stdout=r.stdout,stderr=r.stderr)
    def stamp(t,key):
        s,n=re.subn(r'(?m)^'+key+r'(?::|\s)\s*.*$',key+' '+('0'*40 if key=='LANE_TIP' else '0'*64),t)
        assert n==1,(key,n);return s
    def wrong_ledger():
        d=json.loads(before[ledger]);d['members']['code-from-image']['status']='unexecuted';ledger.write_text(json.dumps(d))
    def mutate(name):
        t=before[receipt].decode()
        if name in ('SUBJECT_SHA','TOOL_SHA','CASE_TABLE_SHA','LANE_TIP'): receipt.write_text(stamp(t,name))
        elif name=='omit-case':
            t,n=re.subn(r'(?m)^CASE whitespace .*\n','',t);assert n==1;receipt.write_text(t)
        elif name=='rewrite-vector':
            old='CASE prefix-only predicted=P/F observed=P/F';assert old in t;receipt.write_text(t.replace(old,old[:-3]+'P/P',1))
        elif name=='ledger-only': receipt.unlink()
        elif name=='wrong-ledger': wrong_ledger()
    records=[]
    out.mkdir(parents=True,exist_ok=True)
    for name in ('SUBJECT_SHA','TOOL_SHA','CASE_TABLE_SHA','omit-case','rewrite-vector','ledger-only','LANE_TIP','wrong-ledger'):
        pristine=run(); observed=None; error=None
        try:
            mutate(name)
            changed={str(f.relative_to(root)):dict(before=sha(b),after=sha(f.read_bytes() if f.exists() else None)) for f,b in before.items()}
            observed=run()
        except Exception as e: error=repr(e);changed={}
        finally:
            for f,b in before.items():f.write_bytes(b)
        restored=run()
        exact=all(f.read_bytes()==b for f,b in before.items())
        verdict='inconclusive' if error or pristine['exit']!=0 or restored['exit']!=0 or not exact else ('survived' if observed['exit']==0 else 'rejected-unattributed')
        # A rejection is NOT an attributed kill: operator must inspect its finding.
        records.append(dict(mutant=name,pristine=pristine,mutated=observed,restored=restored,hashes=changed,restored_exact=exact,error=error,verdict=verdict))
    (out/'c1-receipts.json').write_text(json.dumps(records,indent=2))

if __name__=='__main__':main()

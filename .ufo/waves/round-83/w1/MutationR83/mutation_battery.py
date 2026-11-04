#!/usr/bin/env python3
"""Actual R83 draft mutations; no replacement predicate or toy reference gate.

--origin is read-only. All fixture files and TMPDIR live beneath --scratch.
Runs the copied DebtR83 evaluate detector pristine/mutated/restored for each
mutation. Uses its real fixture builder, checks instrument and frozen universe.
A failed pristine baseline is INCONCLUSIVE, never a killed mutant.
"""
import argparse, contextlib, hashlib, importlib.util, io, json, os, shutil
from pathlib import Path


def digest(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None


def load(path):
    spec=importlib.util.spec_from_file_location('actual_debt',path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--origin',required=True)
    ap.add_argument('--scratch',required=True); ap.add_argument('--out',required=True)
    a=ap.parse_args(); scratch=Path(a.scratch).resolve(); out=Path(a.out).resolve()
    assert str(scratch).startswith('/fast/scratch/hyaku/kengaku-r83/MutationR83/')
    scratch.mkdir(parents=True,exist_ok=True); out.mkdir(parents=True,exist_ok=True)
    os.environ['TMPDIR']=str(scratch); os.environ['PYTHONDONTWRITEBYTECODE']='1'
    os.environ['R83_FLEET_REPO']='/home/vgpnk/Projects/shokunin'
    m=load(Path(__file__).parent/'instruments/round83_c2_debt.py')
    origin=Path(a.origin).resolve(); root,tracked=m.fixture(origin,scratch)
    paths=[m.LEDGER,m.LESSON,'corpus/SOURCES.md','corpus/README.md','SKILL.md',
           'corpus/evidence/round83/r82-census-after.txt','corpus/evidence/round83/r82-seat-counts.json']
    pristine={p:(root/p).read_bytes() if (root/p).exists() else None for p in paths}
    def restore():
        for p,b in pristine.items():
            f=root/p
            if b is None: f.unlink(missing_ok=True)
            else: f.write_bytes(b)
    def run():
        s=io.StringIO()
        try:
            with contextlib.redirect_stdout(s): rc=m.evaluate(root,origin,tracked)
            return dict(exit=rc,stdout=s.getvalue())
        except Exception as e:
            return dict(exit=2,stdout=s.getvalue(),exception=repr(e))
    def ledger(edit):
        rs=[json.loads(x) for x in (root/m.LEDGER).read_text().splitlines() if x.strip()]
        edit(rs); (root/m.LEDGER).write_text('\n'.join(json.dumps(r) for r in rs)+'\n')
    def row(rs,n): return next(r for r in rs if r['id']=='R82-V'+str(n))
    def change(p,old,new):
        f=root/p; t=f.read_text(); assert old in t,(p,old); f.write_text(t.replace(old,new,1))
    def wrong_source(): ledger(lambda rs: row(rs,1).__setitem__('source',m.SPOT+':162'))
    def false_count(): change('corpus/SOURCES.md','| S268 |','| X268 |')
    def five_seats():
        p='corpus/evidence/round83/r82-seat-counts.json'; d=json.loads((root/p).read_text());d['affected']=d['affected'][:-1];(root/p).write_text(json.dumps(d))
    def bad_census(): change('corpus/evidence/round83/r82-census-after.txt','REV a44b2f083ee8b4115aea64598646f4bd9e3c1470','REV '+('0'*40))
    def count26():
        p='corpus/evidence/round83/r82-census-after.txt';f=root/p;ls=f.read_text().splitlines(); ix=next(i for i,l in enumerate(ls) if 'W04' in l);del ls[ix];f.write_text('\n'.join(ls)+'\n')
    def malformed(): change('corpus/README.md','| `lessons/round-81-verifier-spotcheck.md` | lesson | correction |','| `lessons/round-81-verifier-spotcheck.md` | correction |')
    def selected_exception():
        f=root/'SKILL.md'; lines=f.read_text().splitlines()
        ix=next(i for i,l in enumerate(lines) if l.lstrip().startswith('|') and 'round37-c1-attribution' in l and 'none declared' in l)
        lines[ix]=lines[ix].replace('none declared','selftest now')
        f.write_text('\n'.join(lines)+'\n')
    def contradictory_seats():
        change(m.LESSON,'R82-V3 affected=6','R82-V3 The corrected affected count is five, not six. Historical claim affected=6')
    def contradictory_selftests():
        change(m.LESSON,'R82-V7 seven of ten','R82-V7 All ten now declare selftests. Historical claim: seven of ten')
    def exceptions(): change('SKILL.md','none declared','selftest now')
    def literal(): ledger(lambda rs: row(rs,3).__setitem__('evidence_literal','affected=5 unrecovered=2 recovered=3'))
    def duplicate(): ledger(lambda rs: rs.append(row(rs,2).copy()))
    def trivial(): ledger(lambda rs: row(rs,4).__setitem__('check','true'))
    mutations=[('C2-wrong-source-line','SOURCE-LINE',wrong_source),
      ('C2-unchanged-correction-false-new-source','CHECK-FAIL',false_count),
      ('C2-six-versus-five','CHECK-FAIL',five_seats),('C2-bad-historical-W04-revision','CHECK-FAIL',bad_census),
      ('C2-W04-count-26','CHECK-FAIL',count26),('C2-malformed-index','CHECK-FAIL',malformed),
      ('C2-unselected-selftest-control','CHECK-FAIL',exceptions),('C2-false-count-binding','CLOSE-NO-EVIDENCE',literal),
      ('C2-duplicate','DUPLICATE-ROW',duplicate),('C2-trivial-check','CHECK-TRIVIAL',trivial),
      ('C2-selected-selftest-exception','CHECK-FAIL',selected_exception),
      ('C2-contradictory-five-seat-correction','CHECK-FAIL',contradictory_seats),
      ('C2-contradictory-ten-selftests','CHECK-FAIL',contradictory_selftests)]
    if os.environ.get('R83_NEW_PROBES_ONLY'):
        mutations=mutations[-3:]
    baseline=run(); (out/'baseline.json').write_text(json.dumps(baseline,indent=2))
    records=[]
    try:
        for name,token,mutate in mutations:
            restore(); before=run(); mutation_error=None
            try: mutate()
            except Exception as e: mutation_error=repr(e)
            changed={p:dict(before=digest(pristine[p]),after=digest((root/p).read_bytes() if (root/p).exists() else None)) for p in paths if pristine[p] != ((root/p).read_bytes() if (root/p).exists() else None)}
            observed=run(); restore(); restored=run()
            restored_hashes=all(pristine[p]==((root/p).read_bytes() if (root/p).exists() else None) for p in paths)
            verdict=('inconclusive' if before['exit']!=0 or restored['exit']!=0 or mutation_error or not changed else
                     'killed' if observed['exit']==1 and ('DEFECT '+token) in observed['stdout'] else
                     'survived' if observed['exit']==0 else 'inconclusive')
            rec=dict(mutant=name,detector='DebtR83 evaluate; actual copied draft',expected='exit 1 DEFECT '+token,
                     pristine=before,mutated=observed,restored=restored,hashes=changed,
                     restored_exact=restored_hashes,mutation_error=mutation_error,verdict=verdict)
            records.append(rec); print(name,verdict,flush=True)
        (out/'mutations.json').write_text(json.dumps(records,indent=2))
        (out/'summary.json').write_text(json.dumps(dict(baseline_exit=baseline['exit'],
            counts={k:sum(r['verdict']==k for r in records) for k in ['killed','survived','inconclusive']},
            restored_exact=all(r['restored_exact'] for r in records)),indent=2))
    finally:
        restore(); shutil.rmtree(root)
    return 0

if __name__=='__main__': raise SystemExit(main())

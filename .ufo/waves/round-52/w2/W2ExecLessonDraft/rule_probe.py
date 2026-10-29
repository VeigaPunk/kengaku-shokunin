#!/usr/bin/env python3
"""Freeze-checklist rule-behaviour probe (draft; scratch).  Imports the lane counter read-only,
applies the file-level rule AND the per-test rule to every captured primary grader, and reports
every file whose file-level label contradicts its own per-test classes.
  contradiction(V1): file class V1 ('satisfiable by mere presence') but >=1 test is P2/P3.
  contradiction(V4): file class V4 but >=1 test is P1/P2/P3 (V4 means no marker applies).
Exit 1 when any contradiction exists (the probe 'fails' = the rule misdescribes the sample)."""
import importlib.util, json, sys
from pathlib import Path
lane = Path(sys.argv[1]); mod = Path(sys.argv[2]) if len(sys.argv) > 2 else lane/'plans/round52_c1_grader_audit.py'
sp = importlib.util.spec_from_file_location('c1', mod); c1 = importlib.util.module_from_spec(sp); sp.loader.exec_module(c1)
pop = json.loads((lane/'plans/round52-tasks.json').read_text())
tasks = pop['tasks']; bad = []; n = 0; cls = {}
for t, rec in sorted(tasks.items()):
    files = rec['grader_files'] if isinstance(rec, dict) and 'grader_files' in rec else rec
    g = c1.primary_grader(files)
    if not g: continue
    p = lane/'corpus/evidence/round52/graders'/g
    if not p.exists(): continue
    body = p.read_text(errors='replace'); n += 1
    fc, _ = c1.classify(body); tcs = [x['class'] for x in c1.classify_tests(body)]
    cls[t] = (fc, tcs)
    if fc == 'V1' and any(c in ('P2', 'P3') for c in tcs): bad.append((t, fc, tcs))
    if fc == 'V4' and any(c != 'P0' for c in tcs): bad.append((t, fc, tcs))
print(f'PROBE graders={n} contradictions={len(bad)}')
for t, fc, tcs in bad: print(f'  CONTRADICTION {t} file={fc} tests={"".join(c[1] for c in tcs)}')
# file-level coverage of the per-test queue
q = [t for t, (fc, tcs) in cls.items() if 'P1' in tcs]
print(f'P1-bearing tasks={len(q)} of which file-level V1/V4={sum(1 for t in q if cls[t][0] in ("V1","V4"))}')
sys.exit(1 if bad else 0)

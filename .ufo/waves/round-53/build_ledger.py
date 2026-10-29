#!/usr/bin/env python3
"""Merge the nine C2ExecRows*/ledger-part.json seat outputs into plans/round53-tipstate.json (L1 integration step).

Usage: build_ledger.py <wave dir> <out ledger> [--override overrides.json]
An override file maps row name -> partial entry (merged over the seat's entry) so the L1's re-measurement can update
exit/state/evidence/reason without editing seat files.  Seat-only fields (tip_dependent, seconds, argv_source) are
dropped; the counter's schema is {argv, exit, state, kind, reason?, evidence?, timeout_s?}.
"""
import glob
import json
import sys
from pathlib import Path

wave, out = Path(sys.argv[1]), Path(sys.argv[2])
over = {}
if "--override" in sys.argv:
    over = json.loads(Path(sys.argv[sys.argv.index("--override") + 1]).read_text())
rows = {}
for f in sorted(glob.glob(str(wave / "C2ExecRows*/ledger-part.json"))):
    for k, v in json.loads(Path(f).read_text()).items():
        assert k not in rows, f"duplicate row {k}"
        rows[k] = v
for k, v in over.items():
    rows.setdefault(k, {}).update(v)
keep = ("argv", "exit", "state", "kind", "reason", "evidence", "timeout_s")
led = {"schema": "r53-tipstate-v1", "base": "see SKILL.md registry at the measured tip", "rows": {}}
for k in sorted(rows):
    e = {a: rows[k][a] for a in keep if a in rows[k]}
    if e.get("state") == "green":
        e.pop("reason", None)
        e.pop("evidence", None)
    led["rows"][k] = e
out.write_text(json.dumps(led, indent=1, sort_keys=True) + "\n")
print(f"rows={len(led['rows'])} red={sum(1 for e in led['rows'].values() if e['state']=='red')}")

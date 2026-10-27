#!/usr/bin/env python3
"""Renders .ufo/waves/round-45/a3w1-spec.json — attempt-3 re-dispatch of the wave-2 (falsify) items that the
orchestrator session exit (2026-10-26 23:57:36 -03) killed before they left a report. L1 KengakuR45a3.

Source of truth: w2-spec.json (rendered by make_wave2_spec.py, dispatched as w2 by attempt 2). Items are copied
unchanged except: wave/reportDir/report paths point at a3w1, the context names attempt 3 and the salvage tip, and
each seat is told that the killed w2 seat's partial files are unverified leads, never evidence. Items whose w2
seat left a report file (5) are NOT re-dispatched; the L1 re-verifies those reports itself."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
W = f"{L}/.ufo/waves/round-45"
OLD, NEW = f"{W}/w2", f"{W}/a3w1"
SETTLED = {"R45RevC1Receipt", "R45LabratRefetch", "R45CritAssimilation", "R45ExecCensusPost", "R45ExecNoHarm"}
TIP = "fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc"
ATTACK = {"reviewer", "critic", "mutation-tester", "labrat"}

w2 = json.loads(pathlib.Path(f"{W}/w2-spec.json").read_text())

NOTE = f"""
# Attempt 3 (binding addendum to the context above)
This is wave `a3w1` of round 45 attempt 3 (L1 `KengakuR45a3`): a re-dispatch of wave-2 items whose seats were killed
when the orchestrator session exited (2026-10-26 23:57:36 -03). Everything above that says "wave 2" means this wave;
every path above under {OLD}/ is replaced by {NEW}/ — your report is {NEW}/<YourSeatName>.md and your files go under
{NEW}/<YourSeatName>/. The lane tip you measure is `master` = `{TIP}` (or later; record the hash you measured):
the only change since the w2 dispatch is an orchestrator salvage commit of wave-evidence files.
A killed w2 seat of your name may have left partial files under {OLD}/<YourSeatName>/: they are UNVERIFIED leads from a
seat that never finished. You may read them; you may never cite them as evidence or copy a number from them — re-run
anything you rely on and write your own receipts under {NEW}/<YourSeatName>/. Never edit or delete anything under {OLD}/.
Five w2 reports exist ({", ".join(sorted(SETTLED))}); read them in {OLD}/ if useful, attack them if your item covers them.
"""


def fix(s):
    return s.replace(OLD, NEW).replace(".ufo/waves/round-45/w2/", ".ufo/waves/round-45/a3w1/")


items = []
for it in w2["items"]:
    if it["name"] in SETTLED:
        continue
    p = fix(it["prompt"]).replace(" wave-2 item ", " wave a3w1 (attempt-3 re-dispatch of wave 2) item ")
    items.append({**it, "prompt": p, "milestone": "kengaku r45 wave a3w1 (falsify re-dispatch, v1)"})

assert len(items) == len(w2["items"]) - len(SETTLED) == 34, len(items)
c = Counter(i["role"] for i in items)
attack = sum(n for r, n in c.items() if r in ATTACK)
assert 32 <= len(items) <= 64 and attack * 4 >= len(items), (len(items), attack)
spec = {"wave": "kengaku-r45-a3w1",
        "milestone": "kengaku round 45 attempt 3 wave a3w1 (falsify): re-dispatch of the 34 killed wave-2 items",
        "reportDir": ".ufo/waves/round-45/a3w1", "context": fix(w2["context"]) + NOTE, "items": items}
pathlib.Path(f"{W}/a3w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(items), dict(c), f"attack={attack}/{len(items)}")

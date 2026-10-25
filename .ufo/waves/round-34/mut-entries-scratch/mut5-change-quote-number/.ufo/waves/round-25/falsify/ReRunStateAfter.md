ATTACKS: C2 `state-check-after.txt` reproduction at pristine tip 8ea41f9ed.

Axes: receipt fidelity; selftest result.

- Extracted `git archive 8ea41f9ed` to `/tmp/k25w2-ReRunStateAfter` (no live-lane mutation).
- `cd /tmp/k25w2-ReRunStateAfter && python3 plans/state_check.py --summary`: exit 0; output reports `assertions=236 match=232 mismatch=0 superseded=1 offline_unverifiable=3` and the receipt's same remaining lines. Plain stdout differs from `corpus/evidence/round25-calibration/state-check-after.txt` only because the receipt appends `exit=0` (the script itself does not print this shell status; see `plans/state_check.py:1263-1268`).
- Re-ran with the status trailer (`printf 'exit=%s\n' "$rc"`); `diff -u` against `corpus/evidence/round25-calibration/state-check-after.txt` produced no diff (`receipt_diff_exit=0`).
- `cd /tmp/k25w2-ReRunStateAfter && python3 plans/state_check.py --selftest`: `[selftest] ALL PASS (canonical seed, pointers, out-of-population box, pointer-only, sources supersession, ABSENT rule)` (`plans/state_check.py:1116-1224`).

Installs: none.
VERDICT: SURVIVES — both requested checks pass, and the after receipt is reproduced exactly when its recorded exit-status trailer is included.
# MutTesterR91 — mutation battery over the round-91 instruments (scratch clones only)

Tip: `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0`. Table: `.ufo/waves/round-91/w1/MutTesterR91/mutants.md`.
Scratch clones under `/fast/scratch/hyaku/kengaku-r91/MutTesterR91/`, removed on exit. Lane not written; no
commits, no pushes, no installs (none needed, none made).

## Coverage (attack axis)

14 rows: C3 gate 5 (a, b, c1, c2, d), C2 checker 4 (e, f, g, k), C1 counter 2 (h, i), F1 counter 3 (j, j+reg, reg).
Each mutant ran in a working copy restored from git and sha-verified. C1 controls ran in three committed scratch
clones (forged TOOL_SHA, decorative HOST_PYTHON, tampered observation line).

Killed by a named case or leg: a, c1, c2, e, f, g, k, reg, plus h and i via controls.
Survived: b (equivalent), d (verdict line), j (tip), j+reg (pair), and h and i at tip.

## Verdicts by battery (exact commands, rc)

- `python3 -B plans/round91_counter_pin.py --lane <lane> --rev HEAD --work <w>` — rc 0 at tip. `PINS checked=16 matched=16 mismatched=0`, `SELFTEST cases=8 red-green-ok=8`, `PREDICATE R91-C2 pass`.
- `python3 -B plans/round91_counter_pin.py --lane <lane> --rev HEAD --work <w> --selftest` — rc 0 at tip; rc 1 under each of e, f, g, k.
- `python3 -B plans/round91_burndown.py --lane <lane> --rev HEAD --work <w> --selftest` — rc 0 at tip (13/13); rc 1 under a, c1, c2; rc 0 under b and d (survivors).
- `python3 -B plans/round91_burndown.py --lane <lane> --rev HEAD --work <w> --freeze-round 92` — rc 1 at tip, `freeze=refused`.
- `python3 -B plans/round91_c1_replay.py --lane <lane> --rev HEAD --work <w>` — rc 1 at tip; see defect below.
- `python3 -B plans/round91_f1_counter.py --lane <lane> --work <w>` — rc 0 at tip (`PREDICATE R91-F1 pass`, `live=0`, all four blind-spot rows parse).

## Measured tip versus frozen predictions (mispredicts recorded, not repaired)

1. **R91-C1 fails at tip (predicted pass, exit 0).** Cause: `parse_receipt` in `plans/round91_c1_replay.py` reads
   case ids from `id=` tokens, but `corpus/evidence/round91/modernize-probe.txt` writes `CASE <id> predicted=… observed=…`
   positionally. Every case parses to `?`, so L5 fails for all ten cases (`DEFECT L5 receipt names unknown case ?` ×10).
   Measured: `TARGET executed_rows=35 … executed=0 cases=10 legs=20 mismatches=10 defects=10`, rc 1. L1–L4 and L6–L9 pass
   at tip. This is a frozen-counter defect; reported, not repaired.
2. **R91-C3 freeze refused at tip (predicted `freeze=admitted`, exit 0).** Measured at `--freeze-round 92`:
   `freeze=refused oldest_pending_round=82 pending=30 parked=7 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=34 checks_run=114 overrides=3`.
   Defects: `override-unjustified R42-R2`, `override-unjustified R42-R3-33`, `override-unjustified R42-R3-37` (superseding rows
   carry a `check` that differs from the base check, with no `override_reason`), and `check-failed R82-V8 rc=1`.
   Predicted counts also off: `resolutions>=35` (measured 34), `checks_run>=117` (measured 114), `SELFTEST cases=9` (measured 13).
3. **R82-V8 check is location-dependent.** `python3 plans/round83_c2_checks.py v8` from my scratch clone prints `CHECK v8 fail`.
   The script sets `fleet = origin.parent` (line 168) and runs `git show c839b658…:REPORT` there. From a clone under
   `/fast/scratch/...` that commit is absent, so the check fails. The claim's "passes from a clone cwd" was not observed
   from a clone whose parent is not the fleet root. Not verified from inside the fleet root (no write to the lane).
4. **R91-C2 predicted C=6 selftest cases; measured 8.** K=16 matches. `RED_CASES` (line 148) lists seven names and is
   never read; the battery has eight cases including `clean-green`.
5. **R91-F1 matches prediction** (`PARSED` 1/2/1/2, `WRONG-LINE-CAUGHT True`, `live=0`).

## Survivors and the real input that exposes each

- **M-C3b (equivalent).** The `unowned` refusal can never fire: `validate()` rejects blocked rows without an owner first.
  `unowned_blocked=` is structurally zero. No real input reaches it.
- **M-C3d (verdict line unguarded by check failures).** Real input: six `refused` seeds opened 88 plus a closed row `CK-1`
  with `check: exit 4`. Pristine: `freeze=refused`, rc 1. Mutant: `freeze=admitted` beside `DEFECT check-failed CK-1 rc=4`,
  rc still 1 via `not defects`. The selftest checks only rc and the defect substring, so it cannot see the verdict line.
- **M-C1h (L9 stamp leg always true; tip survives).** Killed only by the committed control receipts (forged TOOL_SHA
  and decorative HOST_PYTHON both print `DEFECT L9` under pristine and not under the mutant). A real forged or
  mismatched receipt stamp is what exposes it.
- **M-C1i (L6 rerun leg always true; tip survives).** Killed only by the observation-tamper control. A receipt observation
  block that differs from a fresh probe re-run is what exposes it.
- **M-F1j (wrong-line assertion removed; tip survives).** The tip registry has no line-cited defect, so nothing reaches the
  assertion at tip. Real input: a regression in line-kind detection in `plans/anchor_line_check.py:137`. Combined with j the
  pair is green (`WRONG-LINE-CAUGHT False`, `PREDICATE R91-F1 pass`, rc 0); the pristine counter alone exits 1 with
  `DEFECT WRONG-LINE not caught`. The assertion is the only guard against that regression.

## Calibration and operability notes

- C1 predicate rc cannot discriminate leg mutants while L5 is red at tip: every C1 mutant prints rc 1. Leg kills come from
  `DEFECT` line presence on controls. The frozen claim's control outputs are not committed under `.ufo/waves/round-91/`
  (checked: no C1 control file exists in that directory). My control outputs stay in scratch.
- C2 mutants are caught by the in-path selftest. The only default-path guard on the checker's own bytes is the SELF-PIN
  leg (M-C2g); removing it leaves the default run red only through the selftest.
- C3 selftest kills `c1`/`c2` through the same `seed-starved-refuses` case (no pending rows there, since the base row is
  superseded). The verdict-line gap (M-C3d) and the dead owner-count clause (M-C3b) are not covered by any case.

## Dispositions

No repairs to frozen elements. Findings 1–4 above are routed to the planner (L1 KengakuR91), not patched here. No tools
installed or upgraded. Scratch removed on exit (`rm -rf -- /fast/scratch/hyaku/kengaku-r91/MutTesterR91`).

# MutTesterR91 — mutants (round 91, scratch clones only)

Tip under test: `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0` (clone detached at that revision; lane untouched).
Per-mutant clone: `$M` = scratch clone of the lane (one clone per instrument, file restored from git
between mutants, restored sha256 verified equal to pristine). Work dirs `$W` are scratch-only.
Pristine sha256 (prefix 16): round91_burndown.py `666f5b3770…`, round91_counter_pin.py `4e2361668…`,
round91_c1_replay.py `19600cabc…`, round91_f1_counter.py `e86121a2…`, anchor_line_check.py `814a091e…`.

Unmutated baselines at the tip (command → rc):
- `python3 -B plans/round91_counter_pin.py --lane $M --rev HEAD --work $W` → rc 0; `PINS checked=16 matched=16 mismatched=0`; `SELFTEST cases=8 red-green-ok=8`; `PREDICATE R91-C2 pass`.
- `python3 -B plans/round91_counter_pin.py --lane $M --rev HEAD --work $W --selftest` → rc 0 (8/8).
- `python3 -B plans/round91_burndown.py --lane $M --rev HEAD --work $W --selftest` → rc 0 (13/13).
- `python3 -B plans/round91_burndown.py --lane $M --rev HEAD --work $W --freeze-round 92` → rc 1; `freeze=refused oldest_pending_round=82 pending=30 parked=7 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=34 checks_run=114 overrides=3`; DEFECTs `override-unjustified R42-R2`, `override-unjustified R42-R3-33`, `override-unjustified R42-R3-37`, `check-failed R82-V8 rc=1`; `PREDICATE R91-C3 fail`.
- `python3 -B plans/round91_c1_replay.py --lane $M --rev HEAD --work $W` → rc 1; `TARGET executed_rows=35 … executed=0 cases=10 legs=20 mismatches=10 defects=10`; ten `DEFECT L5 receipt names unknown case ?`; `PREDICATE R91-C1 fail`. (L1–L4, L6–L9 pass.)
- `python3 -B plans/round91_f1_counter.py --lane $M --work $W` → rc 0; `PARSED S260=1,S261=2,S265=1,S266=2`; `ANCHORLINE … live=0 rc=0`; `WRONG-LINE-CAUGHT True`; `PREDICATE R91-F1 pass`.

Columns: `rc` = exit code of the battery under the mutant (baseline in brackets). `killed` = the
battery's output changed on a named case/leg (rc flip or a named red line disappears/appears).

| id | file | mutation | command | rc (base) | expected | observed | killed\|survived | killed_by |
|---|---|---|---|---|---|---|---|---|
| M-C3a | plans/round91_burndown.py:242 | override_reason check skipped (`if False and not (...)`) | `python3 -B plans/round91_burndown.py --lane $M --rev HEAD --work $W --selftest` | 1 (0) | a red case for override-unjustified | `SELFTEST override-unjustified-refuses rc=0 want=1 substring-ok=False ok=False`; `red-green-ok=12` of 13. Tip (`--freeze-round 92`): rc 1 unchanged; the three `override-unjustified` DEFECTs vanish | killed | selftest case `override-unjustified-refuses` |
| M-C3b | plans/round91_burndown.py:281 | unowned-blocked refusal made a no-op (`or bool(unowned)` → `or False`) | `… --selftest` | 0 (0) | a red case for the unowned refusal | 13/13 green. Tip rc 1 unchanged. Equivalent mutant: `unowned` is always empty because `validate()` already rejects a blocked row without a non-empty owner (that is what `blocked-unowned-refuses` exercises) | survived | none — equivalent; the `unowned_blocked=` count is structurally 0 |
| M-C3c1 | plans/round91_burndown.py:301 | seed clause always true in the printed SEEDS value (`seeds_ok = True or …`) | `… --selftest` | 1 (0) | seed-starved case red, SEEDS line `ok=False` | `SELFTEST seed-starved-refuses rc=0 want=1 ok=False`; `red-green-ok=12` | killed | selftest case `seed-starved-refuses` |
| M-C3c2 | plans/round91_burndown.py:305 | seed clause dropped from the PREDICATE conjunction (`… and seeds_ok` removed) | `… --selftest`; plus fixture `--file fixture-c2.jsonl --freeze-round 92` (one closed row opened 89, no open rows) | 1 (0) | seed-starved case refuses | `seed-starved-refuses rc=0 want=1` (`red-green-ok=12`). Fixture: `freeze=admitted … seeds_83_91=1`, `SEEDS … ok=False`, `PREDICATE R91-C3 pass` (pristine: rc 1 `PREDICATE R91-C3 fail`) | killed | selftest case `seed-starved-refuses`; real-input fixture exposes the same clause |
| M-C3d | plans/round91_burndown.py:278 | `check_failed` dropped from the refusal (`or check_failed` → `or False`) | `… --selftest`; plus fixture `--file fixture-d.jsonl --freeze-round 92` (six refused seeds opened 88 + closed row CK-1 with `check: exit 4`) | 0 (0) | a red case printing `freeze=refused` | 13/13 green (`failing-check-refuses-freeze` checks only rc and the `check-failed CK-1 rc=4` substring). Fixture under mutant: `DEFECT check-failed CK-1 rc=4`, `freeze=admitted`, `PREDICATE R91-C3 fail` (rc still 1 via `not defects`). Pristine fixture: `freeze=refused` | survived | none in selftest; the verdict line is exposed only by the fixture |
| M-C2e | plans/round91_counter_pin.py:80-81 | absent pinned path becomes a silent skip (`checked -= 1; continue`) | `python3 -B plans/round91_counter_pin.py --lane $M --rev HEAD --work $W --selftest` | 1 (0) | `path-absent` red with `PIN-MISMATCH absent` | `SELFTEST path-absent rc=0 want=1 defect-ok=False`; child prints `PINS checked=0 matched=0` `PREDICATE R91-C2 pass`; `red-green-ok=7`. Default tip run rc 1 via `SELF-PIN-MISMATCH` (checker bytes changed) | killed | selftest case `path-absent` |
| M-C2f | plans/round91_counter_pin.py:104 | blob anchor check always passes (`elif False and anchored != pin`) | `… --selftest` | 1 (0) | `blob-anchor-missing` red with `RECORD-TABLE anchor` | `SELFTEST blob-anchor-missing rc=0 want=1 ok=False`; `red-green-ok=7` | killed | selftest case `blob-anchor-missing` |
| M-C2g | plans/round91_counter_pin.py:85-92 | SELF-PIN leg removed (block cut) | `… --selftest`; and default tip run | 1 (0) | `self-pin-mismatch` red | `SELFTEST self-pin-mismatch rc=0 want=1 ok=False`; `red-green-ok=7`. Default tip run rc 1 only because the in-path selftest is red; `PINS checked=16 matched=16` (checker's own bytes no longer verified) | killed | selftest case `self-pin-mismatch` (default run catches it only through the in-path selftest) |
| M-C2k | plans/round91_counter_pin.py:82 | pinned-bytes sha compare disabled (`if False and sha(data) != pin`) | `… --selftest`; and default tip run | 1 (0) | `counter-byte-mutated` and `tampered-pin` red | `SELFTEST counter-byte-mutated rc=0 want=1`, `SELFTEST tampered-pin rc=0 want=1`; `red-green-ok=6`. Default tip run rc 1 via `SELF-PIN-MISMATCH` | killed | selftest cases `counter-byte-mutated`, `tampered-pin` |
| M-C1h | plans/round91_c1_replay.py:254 | L9 stamp leg always passes (`l9 = True or stamp_ok`) | tip: `python3 -B plans/round91_c1_replay.py --lane $M --rev HEAD --work $W`; controls in clones with a committed forged receipt | tip 1 (1); controls 1 (1) | a `DEFECT L9 stamp fields mismatch` line present under pristine and absent under the mutant, on forged-stamp and decorative-stamp controls | Tip: no change (L5 red dominates, rc 1, no L9 line either way). Forged-stamp control (TOOL_SHA = 64×0): pristine prints `DEFECT L9 … tool=0000…`; mutant prints no L9 line. Decorative control (HOST_PYTHON `Python 9.9.9`): pristine prints `DEFECT L9 … python=Python 9.9.9`; mutant prints no L9 line | killed by controls; tip survived | forged-stamp control and decorative-stamp control (DEFECT L9 presence) |
| M-C1i | plans/round91_c1_replay.py:202 | L6 rerun leg always passes (`l6 = True or (…)`) | tip run (rc 1 unchanged); control: receipt `CASE full-pass … ok=False` committed in a clone | tip 1 (1); control 1 (1) | `DEFECT L6 rerun rc=0 obs=10 want=10` under pristine, absent under mutant | Tip: no change. Observation-tamper control: pristine prints `DEFECT L6 rerun rc=0 obs=10 want=10`; mutant prints no L6 line, rc 1 only from L5 | killed by control; tip survived | observation-tamper control (DEFECT L6 presence) |
| M-F1j | plans/round91_f1_counter.py:97-98 and :102 | wrong-line assertion removed (defect block cut; `and caught` dropped from PREDICATE) | `python3 -B plans/round91_f1_counter.py --lane $M --work $W` | 0 (0) | none expected at tip (tip is green) | tip rc 0, `PREDICATE R91-F1 pass`; no change | survived | none at tip — see M-F1j+reg |
| M-F1j+reg | plans/round91_f1_counter.py (as M-F1j) plus plans/anchor_line_check.py:137 line-kind check disabled (`if False and (…)`) | assertion removed AND line-defect detection regressed | same F1 command | 0 (expected 1) | WRONG-LINE-CAUGHT False should fail the predicate | `WRONG-LINE-CAUGHT False`; `PREDICATE R91-F1 pass`; rc 0 | survived | none — the pair is green |
| M-F1reg | plans/anchor_line_check.py:137 (pristine F1 counter) | line-kind detection regressed (`if False and (…)`) | same F1 command | 1 (0) | `WRONG-LINE not caught` defect | `WRONG-LINE-CAUGHT False`; `DEFECT WRONG-LINE not caught (the repair broke the true positive)`; `PREDICATE R91-F1 fail`; rc 1. Registry-wide `ANCHORLINE … live=0` unchanged (no line-cited defect in the real registry to see) | killed | F1 wrong-line assertion (fixture `wrong-line`) |

Restoration: every mutated file was restored with `git -C $clone checkout -- <file>` and the sha256 was
rechecked equal to the pristine value (burndown `666f5b37…`, counter_pin `4e236166…`, c1_replay `19600cab…`,
f1_counter `e86121a2…`, anchor_line_check `814a091e…`). Control clones carried one committed forged receipt
each (scratch only, never pushed; lane untouched).

## Survivors and the real input that would expose each

1. **M-C3b (equivalent, dead clause).** No reachable input. `validate()` rejects `status=blocked` without a
   non-empty owner before `unowned` is built, so `unowned_blocked=` is structurally 0. The owner rule is
   enforced once (in `validate`), not twice; the `unowned` refusal is dead code. Tip rc is unaffected.
2. **M-C3d (freeze verdict unguarded by check failures).** Exposed by a ledger in which every effectively
   open row is fresh, all seeds are present, and one effectively-closed row's check exits non-zero. Fixture:
   six `refused` rows with `opened_round` 88 plus `CK-1` (`status: closed`, `check: exit 4`). Pristine:
   `freeze=refused`, rc 1. Mutant: `freeze=admitted` printed beside `DEFECT check-failed CK-1 rc=4`, rc still 1
   through `not defects`. A consumer that greps `freeze=admitted` is misled. The selftest does not assert the
   verdict line.
3. **M-C1h (L9 stamp leg).** Tip survives (L5 red dominates). Exposed by any receipt whose `TOOL_SHA`,
   `CASE_TABLE_SHA`, `HOST_PYTHON`, `HOST_OPENSSL` or `HOST_USERNS` disagrees with the tree or host. Killed
   only by the control commits (forged-stamp, decorative-stamp).
4. **M-C1i (L6 rerun leg).** Tip survives (rerun matches). Exposed by a receipt observation block that differs
   from a fresh probe re-run (edited or stale receipt). Killed only by the observation-tamper control.
5. **M-F1j (wrong-line assertion removed).** Tip survives (no line-cited defect in the registry, so nothing to
   assert). Exposed by a regression of the line-kind check in `plans/anchor_line_check.py`: the assertion is the
   only thing that turns that regression red (M-F1reg), and with M-F1j the pair is green (M-F1j+reg).

## Calibration notes

- C1 predicate rc cannot discriminate leg mutants while L5 is red at the tip: every C1 mutant prints rc 1. Leg
  kills are read from DEFECT-line presence on controls only. This is the reason the controls must be committed
  (claim requires `.ufo/waves/round-91/` control outputs before scoring; not verified here).
- C2 checker mutants are killed by the in-path selftest, not by the default pin pass; the self-pin leg (M-C2g)
  is the only default-path guard against a checker edit, and it is removed by M-C2g with no default-run signal
  beyond the selftest.
- C2 selftest declares `RED_CASES` with seven names while `selftest()` runs eight cases (the `clean-green` case is
  the eighth); the tuple is unused and drifts from the battery.

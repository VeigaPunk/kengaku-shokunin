# CriticFalsify — scoped findings (round 91, w1, read-only)

Full evidence with commands and outputs: `.ufo/waves/round-91/w1/CriticFalsify/critique.md` (16 findings). Tip `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0`, BASE `59764383d4dd33d58faa50daad4c06d0cde410aa`.

## Verdicts

- **C1 — NOT MET at tip.** `python3 plans/round91_c1_replay.py --lane <lane> --rev a8de3e69… --work <w>` → rc 1, `TARGET executed_rows=35 member=modernize-scientific-stack located=1 executed=0 cases=10 legs=20 mismatches=10 defects=10`, ten `DEFECT L5 receipt names unknown case ?`, `PREDICATE R91-C1 fail`. Cause: `parse_receipt` reads CASE ids from `key=value` tokens; the id is positional, so every id is `?`. The receipt vectors match the frozen table 10/10 when compared directly. Legs L1–L4, L6–L9 emit no defect at tip.
- **C1 — BASE control:** rc 1, `PREDICATE R91-C1 fail`, defects=9. Agrees.
- **C2 — MET at tip:** rc 0, `PINS checked=16 matched=16 mismatched=0`, `SELFTEST cases=8 red-green-ok=8`, `PREDICATE R91-C2 pass`. BASE: rc 2, `DEFECT SETUP unreadable plans/counter-pins-r91.json`, could-not-evaluate. Agrees.
- **C2 — frozen rule violated literally:** `git diff --stat 386184a6 a8de3e69 -- <pinned paths>` lists `plans/counter-pins-r91.json` and `plans/round91_counter_pin.py`; empty against B2 `b836a862`. The B→B2 edit is disclosed (M3).
- **C2 — B selftest (386184a6):** 4 of 8 red for named reason. Agrees with M3's count. Clean-green's rc 2 comes from `rev=""` in the fixture, not from PATH-only env (PATH-only with `rev HEAD` passes rc 0). B2 selftest: 8/8, rc 0.
- **C3 — NOT MET at tip.** `python3 plans/round91_burndown.py --lane <lane> --rev a8de3e69… --work <w> --freeze-round 92` → rc 1, `freeze=refused oldest_pending_round=82 pending=30 parked=7 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=34 checks_run=114 overrides=3`, `DEFECT override-unjustified` for R42-R2, R42-R3-33, R42-R3-37, `PREDICATE R91-C3 fail`. Predicted `freeze=admitted`, `resolutions>=35`, `checks_run>=117`.
- **C3 — triage absent from the committed tip:** `corpus/routed-findings.jsonl` is byte-identical BASE→tip (blob `830c0dae…`; empty `git diff --stat`), and equal to the lane working-tree copy. All 30 open rows were opened in rounds 82–89; none in round 91.
- **C3 — BASE control:** rc 1, `freeze=refused`, same numbers as tip (`malformed_unresolved=0`, so the predicted `>=1` is not met). Agrees on refusal.
- **C3 selftest:** `SELFTEST cases=13 red-green-ok=13`, rc 0 (predicted 9).
- **C3 R82-V8 check:** `python3 plans/round83_c2_checks.py v8` → `CHECK v8 fail` rc 1 from a clone under `$S`; passes from the real lane path. The claim's "passes from a clone cwd" is false. `round83_c2_checks.py` is unchanged B→tip.
- **F1 counter (R82-F1 repair):** tip rc 0, `PARSED S260=1,S261=2,S265=1,S266=2`, `ANCHORLINE … cited=84 … live=0`, `WRONG-LINE-CAUGHT True`, `PREDICATE R91-F1 pass`. Agrees. At BASE the counter crashes (`AttributeError: … no attribute 'anchor_quotes'`, rc 1), not `PARSE-ABSENT` as M4 states; the counter lacks a could-not-evaluate guard.

## Numbers that agree

- Ledger BASE: 88 members, 34 executed; file-artifact 25, filesystem-metadata 2, numeric-band 3, stdout-inspection 10, subprocess-exec 12.
- Ledger tip: 88 members, 35 executed; file-artifact 26, filesystem-metadata 3, numeric-band 4, stdout-inspection 11, subprocess-exec 13.
- Routed tip (213 rows, 0 malformed): effective open 30, blocked 7 (R51-R3 owner is the placeholder `unowned:integrator`, which the gate accepts).
- SOURCES rows: BASE 272, tip 274.
- Census: `cd /home/vgpnk/Projects/shokunin && scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku; echo rc=$?` → `kengaku ok`, rc 0. From the lane root it is not found (rc 127): the script lives in the fleet root.
- Stamp: `TOOL_SHA` d70210cb… (= sha256 of the probe at B2 and tip), `CASE_TABLE_SHA` 89fab14b… (tip and A), `SUBJECT_SHA` 0c24195f…, `HOST_PYTHON` Python 3.14.8, `HOST_OPENSSL` OpenSSL 3.6.5, `HOST_USERNS` 122865, `LANE_TIP` B2 is an ancestor of tip (rc 0).

## Mispredicts recorded (not repaired)

C2 selftest cases 6 predicted, 8 measured; C3 selftest cases 9 predicted, 13 measured; C3 `malformed_or_invalid_unresolved>=1` predicted at BASE, measured 0; C3 `checks_run>=117` and `resolutions>=35` predicted, measured 114 and 34.

## Installs / updates

None. Scratch `$S=/fast/scratch/hyaku/kengaku-r91/CriticFalsify` removed on exit. No lane git mutation; no subagent spawned; no fleet-root write.

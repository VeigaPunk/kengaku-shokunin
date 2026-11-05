# R92 CriticFalsify — independent re-derivation and attacks

Seat: CriticFalsify (leaf, no subagents, no commits, no lane git mutation). Own clone under
`/fast/scratch/hyaku/kengaku-r92/CriticFalsify/` (removed before yield). Receipts copied to
`.ufo/waves/round-92/w1/CriticFalsify/receipts/` (names below refer to that directory).

Measured revisions: BASE `4ba56182`, freeze A `96f249e0`, instruments B `4f6b3c52`, B2 `f0018773`
(clone, the round-92 pin-ledger refresh), and the lane HEAD observed at check time, `288511d8`
(tip, after the official receipt `42bd5104` and repair commits `d1ccf56d`..`288511d8`).
Tip numbers below are measured from the tip worktree's own counter bytes (not the B2 clone's).

## Per-number verdicts

Section A: claim numbers at BASE and B2 (the state the seat was assigned to measure).

| # | Number / claim | Verdict | Evidence |
|---|---|---|---|
| 1 | C1 BASE `round92_c1_replay` rc 1, `executed_rows=35` | AGREE | c1-base.out: `TARGET executed_rows=35 ... executed=0`, rc 1 (located=0, defects=9) |
| 2 | C2 BASE: M7, M12, M9 all red, rc 1 | AGREE | c2-base.out: M7 `base-rc=1 base-L5=10`; M12 base unguarded; M9 `base-flag-present=True base-table-absent=True`. Caveat: run with BASE as both rev and tip, so tip legs are red by construction |
| 3 | C2 do-nothing: r91 counter default run green at BASE | AGREE | c2-base.out: `default-run-rc=0` on the BASE pin checker |
| 4 | C3 BASE `freeze=refused oldest_pending_round=82 pending=1` + three `override-unjustified` | DISAGREE | At B2 code: `oldest_pending_round=10000 pending=1 overrides=3 malformed_unresolved=1`, zero `override-unjustified`, extra `DEFECT line 125` and `DEFECT check-failed R82-V8` (gate-core-base.out). At tip code (tip-c3-base.out): `freeze=refused oldest_pending_round=- pending=0`, zero `override-unjustified`, only `DEFECT check-failed R82-V8`. The "pending=1" at B2 is the invalid row R82-F1 (state open, opened=10000), not an ordinary open row |
| 5 | C3 pre-audit: chain-aware BASE resolves pending to 0 | PARTIAL | AGREE at tip code (pending=0); DISAGREE at B2 code (pending=1, invalid row counted as open) |
| 6 | C3 default run completes with a verdict (B2) | DISAGREE | burn-base2.out: CHECK lines, then `TimeoutExpired` traceback at 603 s, rc 1, no `freeze=`/`PREDICATE` line. Bounded 25 s run: 221 nested selftest markers, depth 14 (recursion, finding G1) |
| 7 | Ledger BASE executed 35 of 88 | AGREE | ledger-base.json (4ba56182): 88 members, 35 `executed`, 53 `unexecuted` |
| 8 | Ledger BASE cells: filesystem-metadata 3/10, crypto-credential 3/12, serialization-schema 4/10, file-artifact 26/76 | AGREE | Recomputed from ledger-base.json (class counts over all members, executed subset) |
| 9 | Tip cells 4/10, 4/12, 5/10, 27/76 | AGREE | Arithmetic (+1 each; member carries exactly those four classes); tip-c1.out `PREDICATE R92-C1 pass` (L7 cells_ok) |
| 10 | C1 tip `TARGET executed_rows=36 ... cases=10 legs=60 mismatches=0 defects=0`, rc 0 | AGREE | tip-c1.out (measured with tip counter bytes at 288511d8) |
| 11 | Probe B2 rc 0, `mismatches=0`, PREDICATE pass | AGREE | probe1.out, probe2.out (two independent B2 runs), committed bs-probe.txt |
| 12 | Probe determinism: CASE lines byte-identical across runs | AGREE | my two runs and the committed receipt: CASE lines identical 10/10; TOOL_SHA `13e41e91...` identical in all three. No float or timing sensitivity observed (grader performance leg reads computed `sequential_timecost`, not wall-clock) |
| 13 | TOOL_SHA `db02dd47...` (pre-freeze dry run) | UNVERIFIABLE | Dry-run bytes are not committed. Shipped TOOL_SHA is `13e41e91...`. CASE_TABLE_SHA `2249d5c0...` matches |
| 14 | Probe stamp reads clean worktree | DISAGREE | Clone `git status --porcelain` is empty, but probe1, probe2 and the committed bs-probe.txt all print `WORKTREE dirty` (finding Q3) |
| 15 | legs = 60 (10 cases x 6 functions) | AGREE | round92-cases.json: 10 cases, `leg_order` length 6; probe prints `CASES 10 LEGS 60` |
| 16 | F2 predicted `captured>=74` as "71 before + 3 pins" | PARTIAL | 71 before: AGREE (BASE and B2 both `captured=71 uncaptured=13`). "+3" arithmetic: DISAGREE. Tip shows `captured=78` = 71 + seven new captured rows (S283–S289). Threshold 74 is met |
| 17 | anchor counts at BASE/B2: rows=274 cited=84 captured=71 uncaptured=13 defective=10 repaired=10 live=0 | AGREE | anchor-base.out, anchor-b2.out (10 ROW lines, 13 UNCAPTURED) |
| 18 | C2 M7 tip green (`PREDICATE R91-C1 pass` on same receipt bytes, mismatches=0) | AGREE, with predicate caveat | tip-c2.out: `M7 pass base-rc=1 base-L5=10 tip-rc=0`. The green leg now runs on a ledger-rewound clone (finding P1/C2) |
| 19 | C2 M12: masked BASE dies unguarded (rc 1, no PREDICATE line); tip closes (rc 2, DEFECT SETUP) | AGREE | m12-base-masked-stderr.txt: `FileNotFoundError: 'openssl'`; m12tip.out: `DEFECT SETUP host probe absent (... openssl=absent ...)`, rc 2 |
| 20 | C2 M9 tip green: flags absent, table pinned, PINS checked=17 matched=17, SELFTEST 9/9 | DISAGREE at B2, AGREE at tip | At B2: `tip-flag-absent=False` (c2-b2.out); literal `--skip-selftest` remains on round91_counter_pin.py lines 16, 211. PINS 17/17, SELFTEST 9/9 at B2 (pin-b2.out) are AGREE. At tip `tip-flag-absent=True` and `M9 pass`, but the M9 green predicate was edited after freeze (P1) |
| 21 | C3 tip `freeze=admitted pending=0 malformed_unresolved=0`, SELFTEST red-green-ok, PREDICATE pass, rc 0 | AGREE | tip-c3.out: `SELFTEST-DETAIL cases=10 red-green-ok=10`, `freeze=admitted ... pending=0`, `PREDICATE R92-C3 pass`, rc 0 |
| 22 | F2 tip `CAPTURE-PINNED S287=1,S288=1,S289=1`, live=0, `WRONG-LINE-CAUGHT True`, PREDICATE pass | AGREE | tip-f2.out, rc 0 |
| 23 | Committed probe receipt matches B2 probe | AGREE | committed-bs-probe.txt: CASE lines identical to probe2.out, `mismatches=0`, PREDICATE pass |

Section B: ledger and attack results not covered by the table above.

- Ledger arithmetic (BASE): recomputed independently, all four cells and 35/88 AGREE.
- Attack on C2 "trivial pass": no trivially green sub-check at BASE. M7 red by 10 `L5` lines; M12 red by an openssl traceback; M9 red by both flag-present and table-absent. The r91 default run is green at BASE, but M9 conjunction requires the flags, so it does not pass trivially.
- Attack on C3 override branch: see finding G4. It is a real hole.

## FINDINGS

Severity: MAJOR = claim-blocking, a frozen predicate is wrong, or a frozen rule was breached.
MINOR = weakens the claim or the instrument; does not change a current verdict.
Status: FIXED-AT-TIP = verified defective at B2, passes at 288511d8; OPEN = still defective at 288511d8.

P1 MAJOR, frozen-rule breach, OPEN. Frozen predicates were edited after freeze A and after the B2 measurement. The claims doc (`plans/round-92-claims.md`, frozen at A) states predicates do not change after A. Changes after B2: `1d5634e3` replaces M9's green leg `PINS checked=17 matched=17` with an any-N/N regex; `6a51ff0e` removes docstring literals and adds the R91_C2_CHILD_MODE selftest mechanism; `round92_c2_conformance.py` M7 green leg now clones the lane, rewinds the ledger, and runs the counter there; `a0c7438a`, `b72c83e9`, `dd48027f` change the gate (child-proof, SHOKUNIN_ROOT export, invalid-row chain walk). Commit messages state these were caught by the "tip run". Evidence: `git log f0018773..288511d8`; `git diff f0018773 288511d8 -- plans/round92_c2_conformance.py plans/round91_counter_pin.py plans/round92_burndown.py`. The claims doc needs a disclosed re-freeze or the edits need reverting.

G1 MAJOR, FIXED-AT-TIP. Gate v3 default path never completes at B2. `in_child_mode` (B2 round92_burndown.py:553-567) requires `--selftest` in the parent argv, but `gate()` (:447-450) spawns selftest children without it, so every child reruns the battery. Evidence: burn-base2.out (603 s `TimeoutExpired`, rc 1, no verdict); bounded repro: 221 markers, depth 14. Tip: `a0c7438a` broadens the child-proof; tip-c3.out completes. Residual MINOR: any process whose cmdline contains `round92_burndown.py` is now accepted as a child when a matching marker exists.

G2 MAJOR, FIXED-AT-TIP. SHOKUNIN_ROOT scrubbed from closing checks. `run_check` env (B2 :155-158) passes only PATH/HOME/LANE. R82-V8 then falls back to `origin.parent` and fails. Evidence: gate-core-base.out `DEFECT check-failed R82-V8`; r82v8-b2-scrubbed.out `CHECK v8 fail` versus r82v8-b2-with-shokunin-root.out `CHECK v8 ok`. Tip: `dd48027f` and `b72c83e9` export SHOKUNIN_ROOT; tip-c3.out passes.

G3 MAJOR, FIXED-AT-TIP. Invalid base rows cannot be resolved by a superseding row. B2 :262-270 uses `chain_end_cache.get(sid, sid)`, which never walks invalid rows, so `by_id.get(sid)` is None. Evidence: fixture-invalid-base-resolved.out (B2): closed `BAD-1-R` supersedes invalid `BAD-1`, still `freeze=refused malformed_unresolved=1`. Live row R82-F1 (corpus/routed-findings.jsonl line 125) is invalid and was unresolvable at B2. Tip: `b72c83e9` calls `chain_end(sid)`; tipcode-fixture-invalid-base-resolved.out admitted; tip-c3.out `malformed_unresolved=0`.

G4 MAJOR, OPEN at tip. Override branch admits vacuous closing checks (claim M10(b) violated). In the override branch (B2 :306-322), `vacuous_check` is never called (only at :328 for non-override rows). The path-token test is skipped when the override check has no path token (`if ovr_tokens and ...`). `base_rc` is printed but never gated. Evidence: fixture-override-true.out and fixture-override-colon.out at B2: `freeze=admitted ... overrides=1`, `PREDICATE R92-C3 pass`; the same at tip (tipcode-fixture-override-true.out, tipcode-fixture-override-colon.out, tip code unchanged, `vacuous_check(` still only at tip line 329). Claim text: "an override row's check must share at least one path token with the row's close, source, or base check." Smallest correction: apply `vacuous_check` to override checks and reject an empty path-token set.

G5 MINOR, OPEN at tip. `freeze=admitted pending=0` is not enforced. The refusal on pending only applies when `oldest < freeze-2` (B2 :357-363). Evidence: fixture-pending91.out (B2 and tip code): open row opened in round 91 gives `freeze=admitted ... pending=1`, `PREDICATE R92-C3 pass`. The printed predicate says pending=0, so the code can pass a state the predicate forbids. Smallest correction: refuse when `pending>0` under `--freeze-round`.

G6 MAJOR, claim mispredict, recorded (see table rows 4-5). The BASE expectation (oldest 82, three `override-unjustified`) is not reproduced at B2 or at tip. The predicted DEFECTs come from a one-level resolver; the shipped chain-aware resolver names the R91 rows (which carry reasons). Recorded, not repaired.

G7 MINOR, OPEN. Shokunin.conf lookup is clone-path dependent: `SHOKUNIN_ROOT or lane.root.parent` (B2 :277; tip same). In a scratch clone without SHOKUNIN_ROOT the run exits `DEFECT SETUP shokunin.conf unreadable` rc 2. The M6 fix covers only the round83 check, not the gate's own conf lookup.

G8 MINOR, OPEN. The gate runs mutating git in its `--lane` (`git worktree prune/add/remove`, B2 :290-291, :371). Running the frozen predicate in the lane writes that repo's worktree registry. Any seat or lead run must disclose it.

C1 MINOR, OPEN. L9 host-state dependence: `round92_c1_replay.py` :270-274 compares receipt HOST_USERNS, HOST_OPENSSL and HOST_PYTHON to the live host. The pass depends on the current sysctl, and a changed sysctl flips pass to fail rather than could-not-evaluate.

C2 MINOR, OPEN. Dead code: `round92_c1_replay.py:261` computes `guarded_run(...)` and discards it, then `:263` overwrites.

Q3 MINOR, OPEN, committed in the receipt. Probe stamp `WORKTREE dirty` on a clean tree: `round92_bs_probe.py` :167 `sh()` returns the string "absent" on empty output, so `dirty == ""` (:170, :193) is never true. The committed bs-probe.txt carries the bug. Not in the L9 leg, so the predicate is unchanged. Smallest correction: return "" for empty output.

Q4 MINOR, OPEN. Probe sandbox binds host root read-write: `round92_bs_probe.py` :253-254 `--dev-bind / /`. The docstring's "fresh bubblewrap namespace" overstates the isolation. No write was observed in these runs. Smallest correction: `--ro-bind / /` with the case dir already bound at /app.

Q5 MINOR, OPEN. The M12 check (`round92_c2_conformance.py`) accepts any rc-1 run without a PREDICATE line, so any crash satisfies it. The BASE red is in fact the openssl traceback (m12-base-masked-stderr.txt), so no current false pass, but the check is not tied to openssl.

C-4 MINOR, OPEN. `round91_counter_pin.py --selftest` mode reads the expectations table from the working tree (`Path(__file__).with_name`), not the pinned rev; the default path is rev-pinned.

F-1 MINOR, arithmetic. F2 "71 + 3 = 74": tip captured is 78 (= 71 + S283–S289). Threshold met (F2 PASS at tip).

L-1 INFO. `git worktree list` in the lane reports HEAD detached at `288511d8`, not master as the spec names. I did not touch the lane.

Attacks run without a defect found: C1 L5/L4 (predicted vectors match the 10 observed); C2 M7 and M12 non-triviality (red at BASE for the stated reasons); probe determinism (committed and independent CASE lines identical); F2 threshold (met at tip).

Install or upgrade record: none. No sysctl, pacman, fleet-root, or lane-git mutation. The lane's `.ufo/waves/round-92/w1/CriticFalsify/` directory (report and receipts) is the only write into the lane.

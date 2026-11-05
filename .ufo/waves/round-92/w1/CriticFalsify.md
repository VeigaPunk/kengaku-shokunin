# R92 CriticFalsify — scoped findings

Full per-number table and evidence: `.ufo/waves/round-92/w1/CriticFalsify/report.md`
(receipts under `.ufo/waves/round-92/w1/CriticFalsify/receipts/`).

Measured: BASE `4ba56182`, B2 `f0018773`, lane HEAD at check time `288511d8` (tip).

## Headline

- Coverage (C1): AGREE. At tip, `executed_rows=36`, 10 cases, 60 legs, mismatches 0, rc 0.
- Calibration (C2): green at tip, but the tip passes only after predicate edits made after freeze A (P1). At B2 the M9 literal sub-check was red.
- Operability (C3): green at tip (`freeze=admitted pending=0 malformed_unresolved=0`, SELFTEST 10/10, rc 0). The BASE expectation in the claim is wrong. The override hole (G4) is still open at tip.

## FINDINGS

| ID | Sev | Status | Finding | Evidence |
|---|---|---|---|---|
| P1 | MAJOR | OPEN | Frozen predicates edited after freeze A and after the B2 measurement: M9 green leg (17 literal to any N/N), C2 M7 green leg (ledger-rewind clone), gate child-proof, SHOKUNIN_ROOT export, invalid-row chain walk. Needs disclosed re-freeze or revert. | `git log f0018773..288511d8`; `git diff f0018773 288511d8 -- plans/round92_c2_conformance.py plans/round91_counter_pin.py plans/round92_burndown.py` |
| G1 | MAJOR | FIXED-AT-TIP | Gate default path recursed; never returned a verdict at B2 (603 s TimeoutExpired, rc 1). Child-mode required `--selftest` in parent argv. Tip completes. Residual MINOR: child-proof is broader. | `receipts/burn-base2.out`; B2 round92_burndown.py:553-567, :447-450; tip `receipts/tip-c3.out` |
| G2 | MAJOR | FIXED-AT-TIP | `run_check` scrubbed env, so SHOKUNIN_ROOT never reached R82-V8 and the M6 fix was unreachable from the gate. | `receipts/gate-core-base.out`; `receipts/r82v8-b2-scrubbed.out` (fail) vs `receipts/r82v8-b2-with-shokunin-root.out` (ok) |
| G3 | MAJOR | FIXED-AT-TIP | Invalid base rows could not be resolved by a superseding row; live R82-F1 (ledger line 125) unresolvable at B2. | `receipts/fixture-invalid-base-resolved.out` (B2 refused); `receipts/tipcode-fixture-invalid-base-resolved.out` (admitted) |
| G4 | MAJOR | OPEN | Override branch admits vacuous closing checks: `vacuous_check` never runs on overrides, empty path-token set is not flagged, base_rc not gated. Claim M10(b) violated. | `receipts/fixture-override-true.out`, `fixture-override-colon.out` (B2); `receipts/tipcode-fixture-override-*.out` (tip, admitted); round92_burndown.py:306-322, :329 |
| G5 | MINOR | OPEN | `freeze=admitted pending=0` not enforced: open round-91 row admitted with pending=1. | `receipts/fixture-pending91.out`; `receipts/tipcode-fixture-pending91.out` |
| G6 | MAJOR | recorded | C3 BASE expectation wrong: no `override-unjustified` (claim 3), oldest 10000 at B2 / none at tip (claim 82); the "pending=1" at B2 is the invalid row. | `receipts/gate-core-base.out`; `receipts/tip-c3-base.out` |
| G7 | MINOR | OPEN | shokunin.conf path is clone-path dependent (`SHOKUNIN_ROOT or lane.root.parent`); M6 fixes only round83. | round92_burndown.py:277 (B2) |
| G8 | MINOR | OPEN | Gate runs `git worktree prune/add/remove` in its `--lane`; mutating git in the repo under test. | round92_burndown.py:290-291, :371 |
| C-1 | MAJOR | FIXED-AT-TIP (post-freeze edit) | M9 literal `--skip-selftest` remained in B2 pin checker docstrings (lines 16, 211), so `tip-flag-absent=False` and C2 red at B2. Tip cleaned it by a post-freeze edit (P1). | `receipts/c2-b2.out`; B2 round91_counter_pin.py:16,211 |
| C-2 | MINOR | OPEN | `round91_counter_pin.py --selftest` reads expectations from working tree, not the pinned rev. | round91_counter_pin.py (`Path(__file__).with_name`) |
| C-3 | MINOR | OPEN | M12 check accepts any rc-1 run without a PREDICATE line. BASE red is in fact the openssl traceback, so no current false pass. | `receipts/m12-base-masked-stderr.txt` |
| Q1 | MINOR | OPEN | C1 L9 pass depends on live sysctl and host versions (`HOST_USERNS`, `HOST_OPENSSL`, `HOST_PYTHON`). | round92_c1_replay.py:270-274 |
| Q2 | MINOR | OPEN | Dead `guarded_run` computation overwritten. | round92_c1_replay.py:261 vs :263 |
| Q3 | MINOR | OPEN, in committed receipt | Probe stamp reports `WORKTREE dirty` on a clean tree (committed bs-probe.txt). Not in L9, so no predicate change. | round92_bs_probe.py:167, :170, :193; `receipts/committed-bs-probe.txt` |
| Q4 | MINOR | OPEN | Probe binds host root read-write (`--dev-bind / /`); "fresh namespace" overstates isolation. | round92_bs_probe.py:253-254 |
| Q5 | MINOR | UNVERIFIABLE | TOOL_SHA dry-run prediction `db02dd47...` cannot be checked; shipped is `13e41e91...`; dry-run bytes not committed. | claims doc; `receipts/probe1.out`, `probe2.out` |
| F-1 | MINOR | arithmetic | F2 "71 + 3 = 74" wrong; tip captured is 78 (71 + S283–S289). Threshold 74 met, F2 PASS. | `receipts/anchor-b2.out`, `receipts/tip-f2.out` |
| L-1 | INFO | observed | Lane `git worktree list` shows HEAD detached at `288511d8`, not master. Not touched. | lane `git worktree list` (read-only) |

## Agreed

- C1 BASE rc 1 `executed_rows=35`; tip `executed_rows=36`, legs 60, mismatches 0, rc 0.
- C2 BASE all three red (M7 10 L5 lines; M12 openssl traceback; M9 flag present, table absent); M12 tip closed; M7 tip green.
- Ledger 35/88; cells 3/10, 3/12, 4/10, 26/76 at BASE; tip cells 4/10, 4/12, 5/10, 27/76.
- Probe: rc 0, mismatches 0; CASE lines identical across my two runs and the committed receipt (10/10).
- Anchor at BASE/B2: captured 71, uncaptured 13, defective 10, repaired 10, live 0. Tip captured 78, F2 PASS.

## Smallest correction suggestions (not applied)

- G4: run `vacuous_check` on override checks; require a non-empty path-token overlap.
- G5: under `--freeze-round`, refuse when `pending>0`.
- C-2 / P1: re-freeze or revert the post-freeze edits; if kept, disclose the M9 and M7 predicate changes in the claims doc.
- Q3: `sh()` returns "" on empty output; the committed receipt needs a re-stamp only if L1 wants it accurate.
- Q4: `--ro-bind / /` plus the writable case dir.

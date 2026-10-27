# R44RoutedObserve — routed-findings burn-down (considerthese/2026-10-26.md proposal 1)

Lane tip read: `5e3d3aa06c6b7000929ac3e62563a39159c4501f` (`git clone -q --shared`; clone top-level verified equal to `$S/lane`; ledger last touched by `8adf76c`, so the ledger at the tip is the round-43 closure state). Every counter run went through `claims/envelope.sh`; ENVELOPE lines in `R44RoutedObserve/{list,observe,replacement_checks.out,patched-observe.out}.txt` (all four: `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`, exit 0). No lane file was written; the clone was not mutated (`git status --short` empty).

## 1. Observed (verbatim tail lines)

`python3 plans/routed_open.py --lane "$S/lane" --list` → `ROWS total=60 open=38 blocked=1 closed=21 refused=0` / `routed_open=39 oldest_round=39` (receipt `R44RoutedObserve/list.txt`).
`… --observe` → `OBSERVE rows=60 mismatched=0` / same two summary lines (`observe.txt`). `mismatched=0` is trivially true for the open rows: **no open/blocked row's own `check` passes** (observed=pass appears only on the 21 closed rows; 30 open/blocked rows observe=fail, 9 are `n/a` = no check).

## 2. Disposition of the 39 open/blocked rows

Classes: PASS = check exits 0 (closable by the ledger's own rule); NULL = no `check`; STALE = the check cannot pass although the routed work is recorded (the check greps for an in-place edit, but round-43 R1 makes fixes appended errata and "nothing above is edited"); REFUTED = the finding is false at the tip; OPEN = check fails for real; UNPASSABLE = check cannot pass for any state of the repo.

| class | n | rows |
|---|---|---|
| PASS | **0** | — |
| STALE, substance recorded → closable with a replacement check | 10 | R42-R3-11, -12, -13, -15 (lesson errata E2/E3/`:57`/E5, `corpus/lessons/round-42.md:160-215`); R42-R3-38, -39, -40 (entry `## Errata (round 43` E1/E2/E3 cite `:296-298`, `:309-312`, `:430-432` — the old checks grep the single tokens `:297`/`:311`/`:431`, absent by design, `grep -cF` = 0/0/0); R42-R3-20, -23 (`corpus/QUALITY.md` C3 `:846-851`, C6 `:865-868`); R42-R3-31 (`SCORECARD.md:1829-1834` S1; check wants the phrase "counter that invokes", which the correction rewrote) |
| NULL, closable now | 3 | R42-R3-17 (lesson E6 records it); R42-R2 (children R42-R2.1/.2 closed, observe=pass; its own note says "landed work is closed in R42-R2.1"); R40-R1 (F1-F4 closed by R40-R1.1, observe=pass; residual carried by R42-R1) |
| REFUTED → `refused` | 2 | R42-R3-14 (`plans/round42_c2_verify.py:327` IS the `("V7"…),("V8"…),("V9"…)` line, `:328` is `defects = 0`; the lesson cite `:327` is exact — `round-42.md:198`); R42-R3-16 (`Dockerfile` capture: `:8` comment, `:9` `COPY tests/sim.c`, `:10` `COPY gates.txt`; cite `Dockerfile:9-10` is exact) |
| UNPASSABLE check | 2 | R39-R4 and R42-R5: both run `mutant_direction_check.py --counter plans/round3{9,42}_c1_verify.py`, which prints `SETUP counter … is not a round-38-list counter` and exits 2 for any counter but round 38 (re-run just now, both). The residual they stand for is real; the check is not |
| OPEN (fails for a real reason) | 16 | R39-R2 (absent `--work` still dies in `git_leak_probe.py`); R39-R3 (blocked, `defects.jsonl` pinned); R42-R1 (clause 5: `battery42` has 5 files, no `command -v uv`/`/usr/local/bin/uv`; clauses 1-4 pass — tail uv-pin residual); R42-R3 (tier-B PR-state reader absent); R42-R6, R42-R3-26, R42-R3-27 (`scratch_guard.py --selftest` still `ok=36/36`, unreadable-sentinel exit unfixed); R42-R3-02 (SKILL.md cites no `:238`); R42-R3-05 (entry still cites `:26-52`; no erratum names `:26-53`); R42-R3-06 (README `S128` label); R42-R3-07 (`SKILL.md:699` still "equal to the receipt row"); R42-R3-08 (`pkg_gate.py:276` biopython — and `pkg_gate.py` is FROZEN this round, so it is blocked, not merely open); R42-R3-18, -19 (`plans/carried_direction_diff.py`, `plans/sources_appendonly.py` still absent); R42-R3-32 (envelope-drift record not appended to `round-42.md`; it exists only in the verifier lesson `round-42-verifier-spotcheck.md:46`); R42-R3-36 (`ls corpus/evidence/round43 | grep prior-art` → none) |
| NULL, genuinely open | 6 | R40-R5 (bundle), R42-R3-09 (nit), -33, -34, -35, -37 (each says "never claimed closed"/"no check: unrun image") |

Sum: 0+10+3+2+2+16+6 = 39 ✓ (10+3 closable, 2 refusable = 15 leave `routed_open`; 24 stay).

**Stale-check test (answered from receipts, not argued):** `R44RoutedObserve/replacement_checks.sh` holds one replacement `check` per closable/refusable row; `replacement_checks.out`: 15/15 `pass`. `closures-patch.jsonl` (15 lines: 13 `closed`, 2 `refused`) applied to a scratch copy of the ledger and observed with `routed_open.py --file`: `OBSERVE rows=60 mismatched=0` / `ROWS total=60 open=23 blocked=1 closed=34 refused=2` / `routed_open=24 oldest_round=39` (`patched-observe.out`). **39 → 24**, oldest unchanged (R39-R2/R3/R4).

Structural findings the observe pass exposes:
1. **Triple-counted residual.** R39-R4, R40-R5 and R42-R5 all carry the same set (F39OrderGateMut fail-open in `order_check.py`, F39LedgerTip D1, F39MutDirection, order-class row). The 39 therefore counts one bundle three times; distinct open items ≈ 37. A bundle should be one row with children, as R40-R1/R40-R1.1 did.
2. **Round-43's own routed items are not in the ledger.** `grep -c 'round-43-verifier-spotcheck' corpus/routed-findings.jsonl` → 0; `corpus/lessons/round-43-verifier-spotcheck.md:154-` routes R1-R5 "(round 44)" and the max `opened_round` in the ledger is 42 (`{39:5, 40:6, 42:49}`). The summary line `routed_open=39` is short by up to 5 (`unfiled=5` below). Nothing reads lessons to compare.
3. **Not wired into the close path.** `grep -n 'routed_open' plans/round_close.py` → no hit; the number is quoted by hand.
4. **Age rule.** The proposal's freeze rule ("refuse a new coverage claim while the oldest open finding is more than two rounds old"): oldest is round 39, age 5 at round 44 → would already refuse this round's C2. The three oldest rows are R39-R2 (real defect, small fix), R39-R3 (blocked by a frozen pin) and R39-R4 (unpassable check; real residual = `order_check.py` fail-open, frozen this round, C1 mutant U14c is the only order mutant in scope).
5. **Edits in place.** The ledger is not append-only in practice: `8adf76c` rewrote 13 rows' status in place (`routed_open.py` docstring says a second row per id is a defect). Burn-down needs git history because the file keeps no `closed_round`.

## 3. Burn-down line

Proposed, one per round, printed beside `routed_open=<n> oldest_round=<r>`:

`routed_burn round=<r> opened=<a> born_closed=<b> closed=<c> refused=<f> open=<n> oldest=<o> age=<r-o> unfiled=<u>`

- `opened`: ids first seen that round with status open|blocked; `born_closed`: ids first seen already closed|refused (back-filled history); `closed`/`refused`: ids open|blocked at any point up to the round's last ledger commit that end it closed/refused (carried in or opened and closed in-round); `unfiled`: routed items in that round's closure lesson `§Routed` not present as ledger rows (this needs a lesson reader; 0 until built; hand-count now: round 43 → 5).
- Round attribution = `round-N:` in the commit subject; no schema change. Optional follow-up if rows keep being edited in place: a `closed_round` field.
- Script: `R44RoutedObserve/routed_burn.py --lane DIR [--round-now N]`, stdlib, read-only on git (`git show <rev>:corpus/routed-findings.jsonl`). Computed from `git log --reverse -- corpus/routed-findings.jsonl` (4 commits: `74513c0`, `ff14d76`, `77ea425`, `8adf76c`; receipt `routed_burn.out`):

```
routed_burn round=41 opened=5  born_closed=5 closed=0  refused=0 open=5  oldest=39 age=2
routed_burn round=42 opened=5  born_closed=1 closed=0  refused=0 open=10 oldest=39 age=3
routed_burn round=43 opened=43 born_closed=1 closed=14 refused=0 open=39 oldest=39 age=4   (commits 77ea425,8adf76c)
routed_burn round=44 (tip, no ledger commit yet) open=39 oldest=39 age=5
open by opened_round: {39: 3, 40: 2, 42: 34}
```
Reconciles: 5 → 5+5−0 = 10 → 10+43−14 = 39 ✓ (matches `--list`). Reading: 53 rows opened in 3 rounds, 14 closed (26%); round 42 closed nothing; round 43 opened 43 (the wave-2 falsify back-load R42-R3-01…41) and closed 14; the oldest open item has not moved in 3 rounds. Round 41 back-loaded the ledger (rows opened in rounds 39-40 first appear in round 41), so `age` is measured from `opened_round`, not first-commit round. With the closures in §4 applied, the round-44 line would read `opened=0 closed=13 refused=2 open=24 oldest=39 age=5` (before any new round-44 routed items).

## 4. Paste-ready closure field values

Full JSONL (id + the fields to overwrite: `status`, `close` or `blocker`, `check`; every `check` is run from the lane root and exited 0 at `5e3d3aa`): `R44RoutedObserve/closures-patch.jsonl`. Summary (check strings are in the file; the `(77ea425)` pin is the commit that appended each erratum):

| id | status | close / blocker (abridged) |
|---|---|---|
| R42-R3-11 | closed | lesson `round-42.md` Errata E2: F39 trio "not named carried again in the freeze" |
| R42-R3-12 | closed | `round-42.md` E3: ratios are one generator run's stdout |
| R42-R3-13 | closed | `round-42.md` `### Errata (round 43, closure R1 — receipt pointer)`: `:6` → `:11` |
| R42-R3-15 | closed | `round-42.md` E5: census needs `-E` |
| R42-R3-17 | closed | `round-42.md` E6: no persisted failing receipt |
| R42-R3-20 | closed | `QUALITY.md` C3 (D3) `:846-851` |
| R42-R3-23 | closed | `QUALITY.md` C6 (D6) `:865-868` |
| R42-R3-31 | closed | `SCORECARD.md` S1 `:1829-1834` |
| R42-R3-38 / -39 / -40 | closed | entry `## Errata (round 43` E1 `:296-298` / E2 `:309-312` / E3 `:430-432` |
| R42-R2 | closed | children R42-R2.1 + R42-R2.2 closed, observe=pass; SCORECARD S3 |
| R40-R1 | closed | F1-F4 closed by R40-R1.1; residual carried by R42-R1 |
| R42-R3-14 | refused | refuted: `round42_c2_verify.py:327` is the V9 line; `round-42.md:198` |
| R42-R3-16 | refused | refuted: `Dockerfile:9-10` are the two `COPY` lines |

Judgement calls the L1 must own: (a) R42-R3-20/-23/-31 and -38/-39/-40 are closed by *appended correction*, not by fixing the original sentence — consistent with the round-43 append-only rule but the criteria text itself still reads as originally written; if the L1 wants the original fixed, leave them open. (b) Replacing a row's `check` follows the precedent in R42-R2's note ("Stale-check correction 2026-10-26"). (c) The 2 `refused` rows use `blocker` for the refutation text, as `routed_open.py` requires.

## 5. Not done / limits
- I did not read each row's `source` lesson line to re-judge whether the *finding* was right, except for the two refuted ones; the rest is "check result + whether the errata the lesson/entry/QUALITY/SCORECARD carries covers it", read in the files cited.
- `unfiled=5` for round 43 is a hand count from `round-43-verifier-spotcheck.md:154-175`; no tool computes it.
- The round-43 closure R1-R5 routed items were not filed (finding 2); the L1 may file them as `R43-R1…R43-R5` — out of this seat's write scope.

Files: `R44RoutedObserve/{list.txt,observe.txt,routed_burn.py,routed_burn.out,replacement_checks.sh,replacement_checks.out,closures-patch.jsonl,patched-observe.out}`.

VERDICT: routed-open-39-closable-now-13

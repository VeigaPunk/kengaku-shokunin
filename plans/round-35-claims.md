# Round 35 — frozen claims (kengaku, hyaku run 7, 2026-10-25)

Baseline lane tip: `58a19f37312e1b22fd2a7957bdfc6bb7832aadd0`. Frozen before any grader run, any
repair, and any seat dispatch. A rule changed after a seat has scored is not the claim's rule.

Axis selection: SCORECARD scores coverage 7, novelty 7 (tied lowest non-retired), calibration 8,
depth 9, operability 8, freshness 8, adjacency 8. No stagnation waiver (novelty is below the
saturation line). Tie-break: coverage — a pinned local source and a runnable instrument exist; a
novelty move needs a phenomenon claim with no opened source this round. Coverage stays capped at
7 by the open round-25/round-33 L0 question (`.ufo/l0-questions.md:163`); C1 is judged on its
counter, not on a score move.

## C1 — coverage (lowest, tied): pinned Terminal-Bench 2.0 `protein-assembly` grader, admitted with an executed probe

Surface moved: frontier → core for one TB2 task's own scoring code (corpus/README.md §Frontier
round-33 clause "the clause stays open for the other benchmarks' scoring code (Terminal-Bench
2.0's …)"), plus a new instrument — an offline probe that executes the pinned grader on synthetic
outputs mapped to `instruction.md` requirements. Round 34 captured the bytes but admitted nothing.

- Sources (opened this round, 2026-10-25, byte-identical to the round-34 captures):
  S105 `tests/test_outputs.py`, S106 `tests/test.sh`, S107 `instruction.md`, at
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/`.
- Entry: `corpus/knowledge/tb2-protein-assembly-grader.md`; probe `plans/tb2_grader_probe.py`
  (18 frozen cases, predictions written from static reading before the first run); receipt
  `corpus/evidence/round35/tb2-grader-probe.txt`.
- **Predicate (frozen):** C1 passes iff `python3 plans/round35_c1_verify.py --lane .` prints
  `checks=6 defects=0` and `PREDICATE C1 pass`, exit 0. Checks V1–V6 are defined in the counter's
  docstring (capture manifest at pinned digests; S105–S107 rows; entry triad, falsifier and ≥8
  located quotes verified against capture lines; index + coverage row and 42/42 files/index rows;
  probe receipt byte-equal to a fresh run with `mismatches=0`, carried verbatim by the entry;
  census exit 0).
- Before (freeze): `checks=6 defects=5`, exit 1 (`.ufo/waves/round-35/claims/control-c1-nothing.txt`).
- Kill rule: any V red at the landing tip → C1 not admitted; a probe case whose observation
  differs from its frozen prediction is reported as a mismatch, never re-predicted.
- Cheapest skip-control (round-34 draft re-dressed at the C1 path, rows from its source lines, an
  index row and coverage bullet, no manifest/probe/quote table): `checks=6 defects=5`, exit 1
  (`claims/control-c1-skip.txt`). The control cannot reach the target.

## C2 — calibration: persistent routed-defect ledger; round-34 self-assessment mismatches D1–D5 closed

Mines `considerthese/2026-10-25.md` proposal 2 (one persistent ledger instead of a new
`plans/roundNN_defects.py` per round). `corpus/defects.jsonl` holds the five defects the round-34
non-author spot-check routed (`corpus/lessons/round-34-verifier-spotcheck.md:75-79`); each row's
check in `plans/defect_ledger.py` compares the lane's self-assessment with an observation computed
from repo bytes, and re-runs at every tip.

- **Predicate (frozen):** C2 passes iff `python3 plans/defect_ledger.py --lane .` prints
  `rows=5 closed=5 observed_pass=5 mismatches=0` and `PREDICATE C2 pass`, exit 0.
- Before (freeze): `rows=5 closed=0 observed_pass=0 mismatches=0`, `PREDICATE C2 fail`, exit 1
  (`claims/control-c2-nothing.txt`). Every check is red at freeze, which is the demonstration that
  each can fail.
- Kill rule: any row open, any observed fail, or any mismatch at the landing tip → not admitted.
- Cheapest skip-control (flip every row to `closed`, repair nothing; shared clone):
  `rows=5 closed=5 observed_pass=1 mismatches=4`, exit 1 (`claims/control-c2-flip.txt`; D1 passes
  only because a fresh clone has no untracked files — D1 is a working-tree check by design).

## Separability

C1 touches `corpus/knowledge/tb2-protein-assembly-grader.md`, `corpus/SOURCES.md` rows
S105–S107, `corpus/README.md`, `corpus/evidence/round35/`. C2 touches `corpus/defects.jsonl`, round-34
scratch/manifest/lesson erratum, a SCORECARD correction line and a round-35 lesson Mistakes row.
Neither counter reads the other's surfaces (C2's D5 reads `corpus/lessons/round-35.md` §Mistakes,
which C1 does not check).

## Frontier step

Census before: `.ufo/waves/round-35/claims/census-before.txt` (exit 0, 15 W04). Sourced claim: C1
(S105–S107 opened this round). Mistake to mine: round-34's S091 false refusal and committed scratch
bloat (C2 D5/D2). Assimilation: considerthese proposal 2 (C2); `merge/kengaku/` re-screen for one
theme fitting C1; no package row is appended unless an admitted entry cites it.

## Planner seat

The L1 holds the canonical planner seat; the validator rejects `planner` as a swarm role.

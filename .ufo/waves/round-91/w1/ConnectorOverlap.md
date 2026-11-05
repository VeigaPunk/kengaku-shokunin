# ConnectorOverlap — round 91 scoped findings (read-only)

Full scan, per-lane counts, and every hit with path:line: `.ufo/waves/round-91/w1/ConnectorOverlap/overlap.md`.

## Verdicts

- **(a) Freeze refusal keyed on routed-finding age:** no sibling implements it. Nearest: kaidoku `tools/round-30/prefreeze-gate.py:28` (pin refusal), kaidoku `tools/round-84/freeze-precheck.py:9` (claim-metadata refusal), souji `tools/souji-freeze-check.py:301` (receipt-age refusal), tabi `scripts/check-frontier-admission.mjs:38` (row-opened admission). None gates a freeze on open-finding age. Owners: kaidoku, souji, tabi lanes.
- **(b) Checker self-pin:** siblings do self-pin. Exact match: kaidoku `tools/round-34/version-needs-counter.py:177` (running bytes compared to the self-entry in the frozen instrument ledger, raised inside the predicate path). Also kotodama `tools/assemble-culture-d4.py:35` and `tools/gates/typed-pipeline-gate.py:455`. Kumitate's `scripts/counter-pins.mjs` is a sha pin ledger over counters, but its registry does not contain the checker itself. Owners: kaidoku, kotodama, kumitate lanes.
- **(c) Offline replay of a pinned TB2 grader in bubblewrap:** no sibling overlap. Zero files match both bwrap and a Terminal-Bench/test_outputs token.

## Counts (files matching, per lane)

| lane | (a) freeze∧refus/admit | (a) age tokens | (b) pin tokens | (b) self-byte read | (c) bwrap | (c) TB2 |
|---|---|---|---|---|---|---|
| kaidoku | 20 | 0 | 43 | 118 | 4 | 0 |
| kotoba | 4 | 0 | 0 | 0 | 1 | 0 |
| souji | 2 | 0 | 4 | 31 | 4 | 0 |
| tabi | 1 | 0 | 5 | 0 | 0 | 0 |
| tameshi | 0 | 2 | 6 | 27 | 1 | 0 |
| kotodama | 0 | 0 | 11 | 38 | 0 | 0 |
| kumitate-shokunin | 0 | 0 | 5 | 0 | 4 | 0 |
| mori | 0 | 0 | 4 | 26 | 0 | 0 |
| kake | 0 | 0 | 3 | 10 | 0 | 0 |
| tsukuroi | 0 | 0 | 1 | 75 | 0 | 0 |
| chousa | 0 | 0 | 1 | 7 | 0 | 0 |
| kama | 0 | 0 | 0 | 30 | 1 | 0 |
| mado | 0 | 0 | 0 | 5 | 1 | 0 |
| kagi | 0 | 0 | 0 | 1 | 0 | 0 |
| kasegi | 0 | 0 | 0 | 0 | 0 | 0 |

Lanes with no plans/tools/scripts/tests to scan: kumitate-shokinin, audio-shokunin, game-dev-2d-shokunin, game-dev-3d-shokunin, lore-shokunin, revenger-shokunin. Not lanes: exp-full, history-recheck, research (empty).

## Owners and absorption

Nothing absorbed. Every overlap is named for its owning sibling lane. The R91-C2 combination (a pin ledger covering the checker, a blob entry for a case table, and a selftest inside the predicate path) is not implemented by any sibling in the form scanned.

## Environment

Read-only. Counts used `grep -rIliE` over sibling `plans/ tools/ scripts/ tests/`. Scratch `/fast/scratch/hyaku/kengaku-r91/ConnectorOverlap` removed after the scan. No install or upgrade. No sibling file opened for write.

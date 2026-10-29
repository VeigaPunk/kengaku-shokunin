# C2ExecRowsF — tip-state of 8 registry rows (round 53 wave 1)

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2ExecRowsF/ledger-part.json` (8 rows; raw outputs `out-<row>-<run>.txt` beside it).

## Method
Clean shared clone `C=/fast/scratch/hyaku/kengaku-r53/C2ExecRowsF/tmp.7ZBjcweJfH` (`git clone -q --shared` of the lane; `rev-parse --show-toplevel` printed `$C/lane`; HEAD `1373b6c`, i.e. base tip 536925b + claims commit a34838f + wave-1 spec commit; `git status --porcelain` empty after both batches). Each argv ran from `$C/lane`, `TMPDIR` a per-row dir under `$C`, 900 s timeout, twice (driver `drv.py`, 8 rows concurrent). Both exit codes agreed on every row (not flaky). Seconds are the mean of the two runs under 8-way concurrent load.

## Rows
| row | argv (all `python3 plans/<script> --lane .` unless noted) | exit x2 | s (run1/run2) | state | kind |
|---|---|---|---|---|---|
| catalog-probe | `catalog_probe.py --verify --lane .` | 0,0 | 0.1/0.1 | green | entry |
| fibsqrt-probe | `fibsqrt_probe.py --lane .` | 0,0 | 76.6/69.5 | green | entry |
| mutant-direction-check | `mutant_direction_check.py --lane .` | 1,1 | 211.0/107.4 | red | entry |
| round30-defects | `round30_defects.py --lane .` | 0,0 | 0.3/0.4 | green | entry |
| round37-c1-mutants | `round37_c1_verify.py --lane .` | 1,1 | 244.9/141.7 | red | entry |
| round41-c1-mutants | `round41_c1_verify.py --lane .` | 0,0 | 15.3/9.6 | green | entry |
| round45-c2 | `round45_c2_verify.py --lane .` | 1,1 | 5.6/4.4 | red | entry |
| round52-c2 | `round52_c2_registry.py --lane .` | 0,0 | 0.1/0.4 | green | entry |

All argv source: the row's own entry cell with `--lane .` (no placeholders; optional selectors omitted; no `--work`). No selftest/help kinds needed (0 help rows).

## Red causes
- **mutant-direction-check** (tip-independent): the default counter is the frozen round-38 list; mutant N21 (`sums.splitlines()[:1]`, declared `silence`) can only mirror, so the check prints `DIR N21 D5 declared=silence observed=mirror MISLABELLED`, `DIRECTIONS total=22 mislabelled=1`. Identical to the round-38 receipt `.ufo/waves/round-38/integrate/direction-check.txt`. Will persist whatever this round commits.
- **round37-c1-mutants** (tip-dependent): the embedded `plans/pkg_gate.py` P8 fails on the lane — `corpus/knowledge/fixture-honest-geometry.md` (56 files) has no `corpus/README.md` index row (55) — so `BATTERY fixtures=64 wrong=35`, `MUTANTS total=55 killed=52 survived=3` (M35, M36, M37 are P8 mutants), `PREDICATE C1 fail`. Output byte-identical across runs. Re-measure after the L1 lands `corpus/README.md` / `corpus/knowledge/*.md`: indexing the missing file (and the new round-53 entry) makes it green.
- **round45-c2** (tip-dependent): V2 `gate_exit=1` from the same P8 (`gate: P8 DEFECT index_rows=55 knowledge_files=56 bad=1`), `checks=11 defects=1`; all other V legs ok. Same re-measure trigger as round37-c1-mutants (`corpus/README.md` index vs `corpus/knowledge/`).

## Green rows' tip sensitivity (for L1 re-measure)
- round52-c2: reads SCORECARD/SKILL/LOG/README/knowledge for advertised `plans/*.py`; the round-53 scripts (`round53_*`) need registry rows or it goes `MISSING>0`. Re-measure after SKILL.md/LOG.md/SCORECARD.md land.
- round30-defects: D2 recounts `kappa` lines in `corpus/knowledge/*.md` against a lesson sentence; a new knowledge entry containing `kappa` would flip it.
- catalog-probe, fibsqrt-probe, round41-c1-mutants: no dependence on files this round changes (pinned captures/tool digests).

## Registry cells that disagree with observation (<=25 words quoted)
- round37-c1-mutants: cell `0` "predicate holds … `MUTANTS total=55 killed=55 survived=0`" — observed killed=52 survived=3, exit 1 (P8 drift; no tip stated in the cell).
- round45-c2: cell measured `index_rows=54 knowledge_files=55` at `30801b4`; observed 55/56 — same defect, drifted count; exit 1 agrees with the cell's own measurement.
- mutant-direction-check: cell declares exits `0` and `1` only; the script docstring also defines exit 2 (setup) and 3 (`LEGS-DISAGREE`/INVALID). Exit 1 observed agrees with the cell.
- round52-c2 observed `REGISTERED total=74 rows=76` as the cell says; no disagreement. catalog-probe, fibsqrt-probe, round30-defects, round41-c1-mutants: no disagreement.

No tools installed. Scratch dir removed at exit. No tool inconsistencies noted.

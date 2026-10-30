# R54-C2 migration audit

REDECLARED 4

| Row | R53 declaration (kind / argv) | Entry-truth argv → exit | Red reason |
|---|---|---|---|
| `round53-c2` | selftest: `python3 plans/round53_c2_tipstate.py --selftest` | `python3 plans/round53_c2_tipstate.py --lane .` → 2 | The tip-state counter has no argument-free entry mode: bare invocation prints usage and exits 2; its entry contract requires `--source` and `--work` scratch arguments which the registry cell does not name. |
| `scratch-root-guard` | selftest: `python3 plans/scratch_guard.py --selftest` | `python3 plans/scratch_guard.py check .` → 2 | The gate's check entry requires the round sentinel file which exists only in an active round tree, so on a bare clean checkout it reports `sentinel-missing` and exits 1. |
| `sources-adopt` | selftest: `python3 plans/sources_adopt.py --selftest` | `python3 plans/sources_adopt.py --lane .` → 2 | The adoption gate has no argument-free entry mode: bare invocation prints its usage and exits 2; its entry contract requires an adoption task (package and admit ids) which the registry cell does not name. |
| `stage-scan` | selftest: `python3 plans/stage_scan.py --selftest` | `python3 plans/stage_scan.py --lane .` → 2 | The stage scanner has no argument-free entry mode: bare invocation rejects the registry cell's `--lane` flag and exits 2; its entry contract takes positional stage inputs which the cell does not name. |

## Counts and regression check

- R53 declarations considered: 78.
- REDECLARED: 4 (green R53 declarations of kind `selftest` or `help`, with R54 entry-truth red).
- Regression candidates: 0 (green R53 `kind=entry` declarations with R54 entry-truth red). Empty as required.

## Live registry cross-check (5 sampled rows)

Compared registry cell name and script path in live `SKILL.md` §Gate/probe registry against row/script identity. All five match; no mismatch finding.

| Name | Expected script path | Live registry cell | Result |
|---|---|---|---|
| `round53-c2` | `plans/round53_c2_tipstate.py` | `python3 plans/round53_c2_tipstate.py ...` | match |
| `scratch-root-guard` | `plans/scratch_guard.py` | `python3 plans/scratch_guard.py ...` | match |
| `sources-adopt` | `plans/sources_adopt.py` | `python3 plans/sources_adopt.py ...` | match |
| `stage-scan` | `plans/stage_scan.py` | `python3 plans/stage_scan.py ...` | match |
| `state-assertion-check` | `plans/state_check.py` | `python3 plans/state_check.py --summary` | match |

Evidence inputs: `plans/round53-tipstate.json` and `plans/round54-entrytruth.json` rows; live registry cells in `SKILL.md` lines 567, 573, 608, 640 and 641. This is a data comparison, not a rerun of gates.

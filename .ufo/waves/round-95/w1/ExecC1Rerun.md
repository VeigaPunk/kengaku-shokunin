# ExecC1Rerun — scoped findings (R95-C1 re-measurement)

Full report: `.ufo/waves/round-95/w1/ExecC1Rerun/report.md`. Receipts beside it (`c1-rerun.txt`, `c1-base.txt`, `c1-f.txt`, `probe-run2.txt`, `probe-run3.txt`, `*.obs`, `*.stamps`, `py311-run.txt`, `origsuite-*.txt`, `origsuite-summary.txt`, drivers in `drivers/`).

## Measured
- Counter `plans/round95_c1_replay.py --rev afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`: rc 0, `LEGS` all pass, `TARGET executed_rows=39 … mismatches=0 defects=0`, `PREDICATE R95-C1 pass`. Matches the frozen predicate.
- Counter at BASE `4524072d…`: rc 1, all nine legs fail. Counter at F `d9cd18a7…`: rc 1 (expected).
- Probe ×3: OBSERVATIONS blocks byte-identical; VULNERABLE_BOTTLE_SHA `761756ce…`, TOOL_SHA and CASE_TABLE_SHA identical to the frozen table.
- Python 3.11.17 (bound into bwrap): 15 of 15 vectors equal predicted; no divergence from 3.14.8.
- Upstream suite at `0207a34f` (sha-verified against the capture's upstream pin), pytest 8.4.1:

| variant | result |
|---|---|
| oracle | 357 passed |
| vulnerable | 1 failed (`test_prevent_control_characters_in_headers`) |
| solve | 357 passed |
| hkey-only (C11) | 1 failed, same test |
| package-shadow (C15) | rc 2, 25 collection errors (`ImportError: tob`) |

## Verdicts
- **C1 holds on re-measurement.** No defect, no mismatch, no verdict-flipping finding.
- **C11 is a whole-harness reject, not only a test_outputs.py gap.** The first half of `tests/test.sh` (upstream suite) fails the half fix. The replay's `test_outputs.py`-only scoring passes it, so the replay alone understates the reject. Routed to round 96 as info, not a flip.
- **C15 is rejected by the whole harness only via a collection crash.** The probe's shadow package is incomplete (exports only `_hkey`). A complete shadow was not measured, so the C15 whole-harness verdict is conditional on the shadow's incompleteness. Routed to round 96 as minor.

## Tool installs (recorded)
- `uv venv --python 3.11 $S/venv311` (uv-managed CPython 3.11.17, already present) and `uv pip install pytest==8.4.1` (iniconfig 2.3.1, packaging 26.3, pluggy 1.7.0, pygments 2.21.0), scratch-only. Reason: TB2-pinned grader pytest for portability probe (b). No pacman, no PATH writes, no sysctl changes.

## Scratch
- Lane clone and all `--work` dirs under `/fast/scratch/hyaku/kengaku-r95/ExecC1Rerun/`, removed after the receipts were copied into this wave dir.

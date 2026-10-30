# R2C2Counter

Recommendation: frozen C2 closure is not established. This review does not admit or score the claim.

## BLOCKER findings (pasted)

1. **Argparse abbreviation laundering:** `plans/round54_c2_entrytruth.py:146-159` rejects exact forbidden flags only. One-row scratch registry entry `python3 plans/gate.py` exits **1**, but a ledger declaring `python3 plans/gate.py --selft` green passes the unchanged full counter, exit **0**, `laundered=0`. Argparse resolves `--selft` to `--selftest`. Evidence: `R2C2Counter/laundering-probes.txt`, case `abbreviated-selftest`.
2. **uv decoy script laundering:** `plans/round54_c2_entrytruth.py:160-164` searches for a matching interpreter/script pair anywhere in argv. `["uv", "run", "--no-project", "--offline", "python3", "-cprint('wrapper green')", "python3", "plans/gate.py"]` passes validation and the unchanged full counter, exit **0**, while the real registry entry exits **1**. The script pair is only inline Python's trailing arguments; the gate never executes. Evidence: same receipt, case `uv-decoy-script`.

Both are observed instances of the frozen Claim 2 kill rule, claims lines 176-178. L1 disposition is required; no frozen artifact changed.

## Additional findings

- **MAJOR:** ENV control is not executed or gated by `evaluate` (`255-361`); standalone `round54_c2_controls.py:160-174` leaves its positive branch unpoisoned and passes even when supplied a helper that merely returns inherited `os.environ`. Receipt: `R2C2Counter/env-control-false-positive.txt`.
- **MINOR:** builder outcome-dependent selection and winner-only `chosen` lack candidate receipts; current `chosen: bare` entries contain `--lane .`, inconsistent with the builder tag rule.
- **MINOR:** required `REDECLARED <n>` diagnostic is replaced by `MIGRATION redeclared=<n>`.

Full REGISTRY / LEDGER / EXEC / MIGRATION / ENV mapping, builder and flag analysis, residual risks: [review.md](R2C2Counter/review.md).

## Required receipts

- [selftest.txt](R2C2Counter/selftest.txt): **7/7 PASS**, exit **0**; unchanged imported main, guarded scratch fixture commits.
- [dry.txt](R2C2Counter/dry.txt): **78 registry / 78 ledger**, zero static defects, exit **0**; correctly reports static legs only, no predicate.

Actual Git-variable scrubbing passed its direct probe, including indexed/count-underscore variables; TIMEOUT independently forces predicate failure. No summary-mode defect asserted where the registry explicitly names `--summary`. No full 78-row execution performed. LSP unavailable (`xd://lsp`: no such tool); text fallback was not treated as semantic proof. No tools installed/updated or production edits. Scratch removed before handoff.

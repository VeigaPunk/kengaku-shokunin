# E6RowAudit08 — R54-C2 independent re-execution

Three assigned ledger rows were re-executed in a shared clone at `62e9bba5e4a0bed376890299aa6a09039db7e68e`, using the counter's `hermetic_env` and per-row 600-second cap. All three argv are entry mode and their scripts exist in the clone.

Verdicts:
- `interval-reverdict`: declared 0, observed 0, fragment match N/A — **CONFIRMED**.
- `ledger-tip`: declared 0, observed 0, fragment match N/A — **CONFIRMED**.
- `mutant-direction-check`: declared 1, observed 1, fragment match true — **CONFIRMED**.

Evidence: `interval-reverdict` ended `mismatches=0`; `ledger-tip` ended `rows=9 closed=9 observed_pass=9 mismatches=0`; `mutant-direction-check` included declared fragment `DIR N01 P1 declared=silence observed=silence ok`, and the output tail reported `DIRECTIONS total=22 mislabelled=1` (consistent with declared exit 1). Detailed commands and tails are in `w1/E6RowAudit08/audit.md`; machine-readable verdicts in `w1/E6RowAudit08/audit.json`.

Scratch clone/environment removed. Tool installs: none. Checks/tests/builds intentionally not run.

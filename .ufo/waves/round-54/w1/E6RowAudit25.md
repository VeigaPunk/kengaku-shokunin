# E6RowAudit25 — R54-C2 entry re-execution

Evidence: `audit.json` and `audit.md` under `.ufo/waves/round-54/w1/E6RowAudit25/`. The shared clone was made from the lane at current tip; runs used counter `hermetic_env`, isolated scratch TMPDIRs, combined stdout/stderr, and 600s per-row timeout. All three argv are entry mode under the frozen forbidden-option definition, and all three referenced script paths exist in the clone.

Verdicts:
- `scratch-root-guard`: declared 2, observed 1, evidence fragment matches — **MISMATCH**.
- `sources-adopt`: declared 2, observed 2, evidence fragment matches — **CONFIRMED**.
- `stage-scan`: declared 2, observed 2, evidence fragment matches — **CONFIRMED**.

Exact mismatch output tail: `CHECK red reason=sentinel-missing`. The observed behavior agrees with the row's evidence fragment and reason, but contradicts its declared exit value. The ledger reason also describes exit 1, matching this execution rather than declared 2.

No tools installed. No checks beyond the assigned executions were run.
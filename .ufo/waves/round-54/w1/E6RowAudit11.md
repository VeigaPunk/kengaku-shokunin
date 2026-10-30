# E6RowAudit11 — independent R54-C2 row re-execution

Audit artifacts: `.ufo/waves/round-54/w1/E6RowAudit11/audit.json` and `audit.md`.

Re-ran all three ledger `entry_argv`s against shared clone tip `62e9bba5e4a0bed376890299aa6a09039db7e68` using the counter's imported `hermetic_env`, scratch TMPDIRs, and 600-second per-row caps. All three argv values were entry-mode (no `--selftest`, `--help`, `--dry`, or `--version`), and their referenced script paths exist in the clone.

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| round-close-check | 0 | 0 | n/a | CONFIRMED |
| round28-census | 1 | 1 | false | MISMATCH |
| round30-defects | 0 | 0 | n/a | CONFIRMED |

`round28-census` exit agrees, but its declared fragment `"c1": { "exit": 0, "findings": [], "metrics":` does not appear verbatim. Observed JSON uses multiline formatting (`"c1": {` then separate lines for `"exit": 0`, `"findings": []`, and `"metrics": {`), so this row is not confirmed under the specified two-part rule. Exact commands, evidence/output tails, and all row metadata are in `audit.md` and `audit.json`.

No tools installed or updated. Scratch clone and driver removed before handoff. No blockers.
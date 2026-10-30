# E6RowAudit05 — R54-C2 independent re-execution

Three entry argv runs were independently executed in a shared clone of the current lane tip under imported `round54_c2_entrytruth.hermetic_env`, with each run limited to 600 seconds and TMPDIR inside seat scratch. All argv passed `entry_mode_ok`; all corresponding script paths existed in the clone. Detailed commands and exact captured output tails are in `E6RowAudit05/audit.md`; machine-readable verdicts are in `E6RowAudit05/audit.json`.

Verdicts (name, declared, observed, fragment-match, verdict):
- feal-linear-probe, 0, 0, null, CONFIRMED
- feal-probe, 0, 0, null, CONFIRMED
- fibsqrt-probe, 0, 0, null, CONFIRMED

Declared evidence field is absent for these green rows, so fragment-match is null/not applicable.

Evidence basis: ledger rows and registry cells from the frozen lane; executed commands and outputs captured by the driver in scratch and retained as tails in audit.md.

Files changed: `.ufo/waves/round-54/w1/E6RowAudit05/audit.json`, `.ufo/waves/round-54/w1/E6RowAudit05/audit.md`, this report. No production files changed. No tools installed. Risks/blockers: none observed; full output retained in scratch only.

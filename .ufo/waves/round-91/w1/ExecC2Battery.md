# ExecC2Battery — R91-C2 control battery (summary)

Full table with commands, rc and first defect lines: `.ufo/waves/round-91/w1/ExecC2Battery/controls.txt`.
Narrative: `.ufo/waves/round-91/w1/ExecC2Battery/report.md`.
Subject: `plans/round91_counter_pin.py` + `plans/counter-pins-r91.json` at tip C `a8de3e69`. Scratch clone only; lane not modified; no installs.

| Control | Expected rc | Observed rc | First defect |
|---|---|---|---|
| 1 positive (no skip) at a8de3e69 | 0 | 0 | none; PINS 16/16, SELFTEST 8/8, PREDICATE pass |
| DN do-nothing at BASE 59764383 | 2 | 2 | DEFECT SETUP unreadable plans/counter-pins-r91.json |
| 2 one-space append, round88_claim_figures.py | 1 | 1 | DEFECT PIN-MISMATCH bytes plans/round88_claim_figures.py |
| 3 delete round91_burndown.py | 1 | 1 | DEFECT PIN-MISMATCH absent plans/round91_burndown.py |
| 4 one-byte round89-q66-records.json | 1 | 1 | DEFECT RECORD-TABLE mismatch plans/round89-q66-records.json |
| 5 checker self-leg forced green, committed, ledger untouched | 1 | 1 | DEFECT PIN-MISMATCH bytes plans/round91_counter_pin.py (self-pin leg not reached) |
| 6 checker + ledger regenerated in one commit, `--skip-selftest` | residual (pass expected) | 0 | PREDICATE R91-C2 pass (residual observed) |
| 7 weakened blob-anchor-missing expectation, pin not regenerated | 1 | 1 | DEFECT PIN-MISMATCH bytes plans/round91_counter_pin.py; weakened case stays green |
| 8 delete counter-pins-r91.json | 2 | 2 | DEFECT SETUP unreadable plans/counter-pins-r91.json |

Extra findings:
- 5b: uncommitted self-leg disable at the clean tip with `--skip-selftest` exits 0 (self-pin bypassed); without skip it exits 1 via the in-path selftest (`SELFTEST self-pin-mismatch rc=0 want=1`).
- 7b: weakened selftest expectation plus regenerated pin in one commit exits 0 (`SELFTEST 8/8`) — a second undisclosed residual.
- 7c: a red case with a wrong expected rc, pin regenerated, exits 1 via `SELFTEST-CHILD` (selftest leg is in the predicate path).
- Cosmetic: the summary line prints `red-green-ok=0` while `SELFTEST-DETAIL` says 7.
- Mispredict: SELFTEST cases predicted 6, measured 8. PINS 16 matched.

Installs: none.

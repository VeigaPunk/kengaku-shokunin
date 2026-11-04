# ReviewerR83 — R83-C1

Axes: coverage, calibration. Recommendation only; frozen contract unchanged.

## Findings

**Medium — actual negative-control evidence remains mandatory.** `plans/round83_freeze_controls.py:12-14` hardcodes `target_reached=False`; it neither calls the counter nor constructs ledger-only/fabricated receipt fixtures. Its `FREEZE-CONTROLS pass` is pre-data anti-vacuity evidence, not executed gate rejection. L1 must retain actual counter stdout/exit for do-nothing, ledger-only and fabricated observations before scoring. This does not establish an implementation bug in the unavailable counter.

## Empirical results

Independent real bubblewrap replay of BASE's unmodified captured grader: **8 cases, 16 legs, zero mismatches**, function order preserved, separate process/sandbox per leg, scratch UTF-8 files read at real `/app/output.txt`. No mocked file APIs; host `/app` absent before/after. Prefix and equality red witnesses hit subject lines 25 and 29 respectively.

Two extra scratch-only falsifiers: directory `output.txt` produces P/defect (`IsADirectoryError`, exit 2); import-time `FileNotFoundError` is setup exit 2, not graded F. These establish classification requirements, not observed ReplayR83 bugs.

## Residual risk and gaps

ReplayR83 and CounterR83 drafts absent at direct read; no claim either implementation reviewed or C1 passed. Exact proposed stamp/argv/digest/ledger/vector/revision corruption recipes in `ReviewerR83/attack-spec.json` remain unexecuted against the unavailable gate. LSP device unavailable (`No such tool`), so no semantic caller/diagnostic evidence. No resume path in scope. No tool installations, production changes, git mutations or general tests.

Full scoped report: [ReviewerR83/report.txt](ReviewerR83/report.txt).
Raw receipts and reproducible independent driver: [ReviewerR83/independent-falsifiers.json](ReviewerR83/independent-falsifiers.json), [ReviewerR83/falsifier.py](ReviewerR83/falsifier.py).

# ExecC2Battery-3 — scoped findings (R92-C2 conformance battery)

Full table, raw outputs and scratch commit ids: `.ufo/waves/round-92/w1/ExecC2Battery/report.md` and `controls.txt`.

Clone at B2 f0018773f507f363854123856990f8ff8a87eb8c (scratch only; removed before yield).

- Controls 1, 3, 4 match the expected outcome.
- F1 (control 2): at B2 `plans/round92_c2_conformance.py` returns rc 1, not rc 0. M7 and M12 pass; M9 fails on `tip-flag-absent=False`. The `--skip-selftest` flag is removed from argparse (`--skip-selftest` is rejected, rc 2), but the literal string remains in `plans/round91_counter_pin.py` at lines 16 and 211. The frozen M9 predicate ("checker bytes contain no --skip-selftest") is therefore false at B2. The default counter run at B2 is rc 0 (PINS 17/17, SELFTEST 9/9). Not repaired.
- F2 (control 5): `git grep -c 'skip-selftest' f0018773 -- plans/round91_counter_pin.py` prints `:2` (exit 0), same cause as F1. `CHILD_ENV` count is 3 (green).
- F3 (control 6): the table-pin rewrite as specified (flip clean-green rc, re-pin the ledger) is rejected by the selftest (rc 1, `clean-green rc=0 want=1`), not passed. Leg 1 (no re-pin) is rc 2 as expected. The known residual reproduces with a consistent rewrite (weakened defect text, re-pinned, rc 0) — disclosed, not a control-6 pass; the L0 kengaku round-91 in-tree-pin question owns it.
- Observations O1–O4 (table-source mismatch between --rev and working tree in the selftest fixtures; text-vs-byte hash in M9 `tip-table-pinned-match`; BASE-valued "tip" fields in control 1; a racy first launch re-run cleanly) are in report.md.
- Tool installs: none. Host sysctls untouched.

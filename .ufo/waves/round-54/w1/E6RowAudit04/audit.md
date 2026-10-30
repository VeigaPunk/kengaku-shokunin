# R54-C2 independent entry-row audit

Re-executed in a shared clone of the current lane tip via the counter's `hermetic_env` helper. For each command, a distinct temporary directory below `/fast/scratch/hyaku/kengaku-r54/E6RowAudit04/` provided `TMPDIR`, HOME, and XDG config; timeout was 600 seconds per row. All three script paths exist in the clone; all argv pass entry-mode inspection (no `--selftest`, `--help`, `-h`, `--dry`, or `--version`). Ledger evidence field is empty for each row, so fragment-match is `null`/not applicable.

Driver command: `python3 /fast/scratch/hyaku/kengaku-r54/E6RowAudit04/tmp.oVUWwQkRub/audit_driver.py`

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| db-wal-probe | 0 | 0 | null (empty evidence field) | CONFIRMED |
| defect-ledger | 0 | 0 | null (empty evidence field) | CONFIRMED |
| extraction-policy-compare | 0 | 0 | null (empty evidence field) | CONFIRMED |

Exact entry commands (run with cwd equal to the clone root):

```sh
python3 plans/db_wal_probe.py --lane .
python3 plans/defect_ledger.py --lane .
python3 plans/parser_policy_compare.py --summary
```

Output tails:

- `db-wal-probe`: `regrade cases=28 differ=0\ncases=28 observed_pass=8 observed_fail=20 mismatches=0\n`
- `defect-ledger`: `R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True\nrows=5 closed=5 observed_pass=5 mismatches=0\nPREDICATE C2 pass\n`
- `extraction-policy-compare`: `MATRIX row E8 0 17 0 17 1012 26 0 17 0\nTOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5\n`

The driver captured complete combined stdout/stderr in its execution result; these tails preserve each summary. No timeout or mismatch occurred. No tools installed/updated.

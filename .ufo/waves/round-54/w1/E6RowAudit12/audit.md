# R54-C2 assigned-row independent audit

Executed in a shared clone of the lane at its then-current tip, with `hermetic_env(tmp)` imported from the frozen `plans/round54_c2_entrytruth.py`. Each row had a dedicated TMPDIR under `/fast/scratch/hyaku/kengaku-r54/E6RowAudit12/tmp/`; timeout was 600 seconds per row. Each script path exists, and each argv is entry mode (none of `--selftest`, `--help`, `-h`, `--dry`, `--version` occurs).

The selected ledger rows are green (`entry_state=green`), and contain no `evidence` field (`null`), so fragment-match is not applicable; exit agreement suffices for these green rows.

| name | declared | observed | fragment-match | verdict | output |
|---|---:|---:|---|---|---|
| round31-c1-literals | 0 | 0 | n/a | CONFIRMED | `checks=6 defects=0` |
| round31-defects | 0 | 0 | n/a | CONFIRMED | `checks=10 defects=0` |
| round33-c1-literals | 0 | 0 | n/a | CONFIRMED | `checks=8 defects=0` |

Exact commands (run from clone root):

```sh
python3 plans/round31_c1_verify.py --lane .
# exit 0; stdout: checks=6 defects=0
python3 plans/round31_defects.py --lane .
# exit 0; stdout: checks=10 defects=0
python3 plans/round33_c1_verify.py --lane .
# exit 0; stdout: checks=8 defects=0
```

All observed output is in `audit.json`; no rows were unrun and no mismatches were found.

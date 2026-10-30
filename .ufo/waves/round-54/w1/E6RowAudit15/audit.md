# Round 54 entrytruth row audit

Source: current shared clone at `62e9bba5e4a0bed376890299aa6a09039db7e68e`. Executed with `hermetic_env()` imported from the frozen lane counter; clone was CWD, `TMPDIR=/fast/scratch/hyaku/kengaku-r54/E6RowAudit15/tmp`, timeout 600 seconds per row. The reported argv is exactly the ledger's `entry_argv`; all scripts exist in the clone and all argv are entry mode (none contains `--selftest`, `--help`, `-h`, `--dry`, `--version`).

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| round37-c2 | 0 | 0 | n/a (green row has no evidence fragment) | CONFIRMED |
| round38-c1-mutants | 1 | 1 | true | CONFIRMED |
| round38-c2 | 0 | 0 | n/a (green row has no evidence fragment) | CONFIRMED |

## Exact commands

```sh
python3 plans/round37_c2_verify.py --lane .
python3 plans/round38_c1_verify.py --lane .
python3 plans/round38_c2_verify.py --lane .
```

## Observed evidence

- `round37-c2`: `checks=7 defects=0` and `PREDICATE C2 pass`; exit 0.
- `round38-c1-mutants`: `PINS total=14 mismatched=0` occurs verbatim; exit 1. This matches the declared red exit and declared evidence fragment.
- `round38-c2`: output includes `checks=7 defects=0`; exit 0.

No mismatches or unrun rows. No tools installed or updated.

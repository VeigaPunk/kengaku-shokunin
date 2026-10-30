# Round 54 entrytruth row re-execution

Clone: shared clone of current lane repository at `/fast/scratch/hyaku/kengaku-r54/E6RowAudit19/clone` (top-level assertion passed). For each row, the runner imported `hermetic_env` from lane `plans/round54_c2_entrytruth.py`, set per-row `TMPDIR` below seat scratch, and ran with a 600-second subprocess timeout. No `--selftest`, `--help`, `-h`, `--dry`, or `--version` argument was present; script exists in clone in each case. These are green rows, so no evidence fragment is declared (`fragment_match: null`).

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| round43-c1-mutants | 0 | 0 | n/a | CONFIRMED |
| round43-c2 | 0 | 0 | n/a | CONFIRMED |
| round44-c1-mutants | 0 | 0 | n/a | CONFIRMED |

Exact entry commands:

```text
python3 plans/round43_c1_verify.py --lane .
python3 plans/round43_c2_verify.py --lane .
python3 plans/round44_c1_verify.py --lane .
```

Output evidence captured by the driver (stdout+stderr; relevant tails):

- `round43-c1-mutants`: `PINS total=2 mismatched=0`; successive `FIXTURE ... ok` results (tail recorded by driver; no declared fragment).
- `round43-c2`: `V1 ok listed=12 bad=0 extra=0`; `V1 ...` through subsequent checks included in output (no declared fragment).
- `round44-c1-mutants`: `PINS total=2 mismatched=0`; successive `FIXTURE ... ok` results (no declared fragment).

Registry-cell agreement checked against `SKILL.md` rows 602, 603, and 605: each registry entry command matches its ledger `entry_argv` script and `--lane .` arguments. No mismatches or unrun rows. No tools installed/updated.

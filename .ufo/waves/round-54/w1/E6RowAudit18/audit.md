# R54-C2 independent entry-row audit

Clone tip: `62e9bba5e4a0bed376890299aa6a09039db7e68e`.

Each run used the frozen ledger argv from the clone, with `plans/round54_c2_entrytruth.py::hermetic_env(tmp)` and `TMPDIR=/fast/scratch/hyaku/kengaku-r54/E6RowAudit18/tmp.Ely7NhsAiZ/tmp`. Per-row timeout: 600 seconds. Each argv is entry mode (no `--selftest`, `--help`, `--dry`, or `--version`) and its script exists in the clone. The ledger records all three rows green and has no `reason`/`evidence` fragment for them; evidence fragment match is therefore N/A, not a failed comparison.

| row | declared | observed | fragment match | verdict |
|---|---:|---:|---|---|
| round41-c2 | 0 | 0 | N/A (no declared fragment; green row) | CONFIRMED |
| round42-c1-mutants | 0 | 0 | N/A (no declared fragment; green row) | CONFIRMED |
| round42-c2 | 0 | 0 | N/A (no declared fragment; green row) | CONFIRMED |

Commands (cwd is clone root; all three received the hermetic environment described above):

```sh
python3 plans/round41_c2_verify.py --lane .
python3 plans/round42_c1_verify.py --lane .
python3 plans/round42_c2_verify.py --lane .
```

Observed output tails:

```text
round41-c2:
checks=8 defects=0
PREDICATE C2 pass

round42-c1-mutants:
MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=9/9 order=5/5
ADVERTISED direct=13 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass

round42-c2:
checks=9 defects=0
PREDICATE C2 pass
```

No mismatch or timeout. The full observed output was retained in the executor tool result; the tails above are literal excerpts.

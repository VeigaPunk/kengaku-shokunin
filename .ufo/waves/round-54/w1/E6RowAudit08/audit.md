# R54-C2 assigned-row independent audit

Shared clone: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit08/clone`, current tip `62e9bba5e4a0bed376890299aa6a09039db7e68e`.
Each command ran with `round54_c2_entrytruth.hermetic_env(tmp)` (isolated HOME/XDG, empty global git config, system config disabled, GIT_* scrubbed) and `TMPDIR` below the seat scratch. Per-row timeout: 600 seconds. Each argv is entry mode (no forbidden --selftest/--help/--dry/--version option), and its script exists in clone.

| Row | Declared | Observed | Evidence fragment | Verdict |
|---|---:|---:|---|---|
| interval-reverdict | 0 | 0 | none declared | CONFIRMED |
| ledger-tip | 0 | 0 | none declared | CONFIRMED |
| mutant-direction-check | 1 | 1 | `DIR N01 P1 declared=silence observed=silence ok` — found | CONFIRMED |

Commands (run from clone):

```sh
python3 plans/attrib_calibration.py --summary
python3 plans/ledger_tip.py --lane .
python3 plans/mutant_direction_check.py --lane .
```

Observed output tails:

- `interval-reverdict`: `TOTAL files=9 scored_files=5 trial_only=4 blocks=10 superseded=5 unique_samples=4 duplicates=1 scored_trials=92 correct=92 incorrect=0 estimates=35 PASS=7 FAIL=0 INDETERMINATE=11 UNTESTED=12 shares=12 n_ge_17=12 stored_verdicts=7 transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 stored_checks=119 mismatches=0 dup=[corpus/evidence/attrib-r22-legs.log:312-362=corpus/evidence/attrib-r22-opencode-trials.log:204-254]`
- `ledger-tip`: `TIP commit=62e9bba5e4a0bed376890299aa6a09039db7e68e control=/fast/scratch/hyaku/kengaku-r54/E6RowAudit08/clone dirty=0`; `rows=9 closed=9 observed_pass=9 mismatches=0`
- `mutant-direction-check`: `DIR N21 D5 declared=silence observed=mirror MISLABELLED`; `LEGS mutants=22 disagree=0 invalid=0`; `DIRECTIONS total=22 mislabelled=1`

No mismatches or unrun rows. The two green rows have no declared evidence fragment; fragment match is not applicable.

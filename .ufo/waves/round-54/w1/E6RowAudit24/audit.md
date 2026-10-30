# R54-C2 assigned-row re-execution

Clone revision: `62e9bba5e4a0bed376890299aa6a09039db7e68e`. Each command was invoked in that clone's root using `round54_c2_entrytruth.py:hermetic_env` and a distinct `$TMPDIR` beneath `/fast/scratch/hyaku/kengaku-r54/E6RowAudit24/`; timeout was 600 seconds per row. All three argv passed `entry_mode_ok`, contained none of `--selftest`, `--help`, `-h`, `--dry`, `--version`, and named a script present in the clone.

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| round53-c1 | 0 | 0 | n/a (no evidence fragment declared) | CONFIRMED |
| round53-c2 | 2 | 2 | true | CONFIRMED |
| routed-findings | 0 | 0 | n/a (no evidence fragment declared) | CONFIRMED |

## Commands and captured output tails

### round53-c1
`python3 plans/round53_c1_triage.py --lane .`

Observed output tail:
```text
PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok r52_audit_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184
FREEZE clean=yes classifier_and_freeze_one_commit=yes classifier_sha=ok label_files_pinned=ok shards_pinned=ok labels_after_freeze_and_untouched=yes authors=4
ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52 unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)
ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes
CONFIRM candidates_never_read=28 new_confirmed=20 rejected=0 target>=3
PRIOR-ART rows=20 tasks_covered=20/20 known=7 new=13 urls=13 rejected=0 target: urls>=3 new>=1
PREDICATE R53-C1 pass
```

### round53-c2
`python3 plans/round53_c2_tipstate.py --lane .`

Declared evidence fragment: `SETUP --source and --work are required unless --dry`

Observed output tail:
```text
SETUP --source and --work are required unless --dry
```

### routed-findings
`python3 plans/routed_open.py --lane .`

Observed output tail:
```text
ROWS total=75 open=31 blocked=1 closed=41 refused=2
routed_open=32 oldest_round=39
```

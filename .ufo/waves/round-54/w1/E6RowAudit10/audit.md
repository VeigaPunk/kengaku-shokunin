# Round 54 C2 entry-truth independent re-execution

Shared clone: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit10/clone`, HEAD `62e9bba5e4a0bed376890299aa6a09039db7e68e`. Each command ran from that clone with `plans/round54_c2_entrytruth.py`'s imported `hermetic_env()` and a unique TMPDIR under the seat scratch directory; timeout 600 seconds per row. All scripts existed, all invocations were entry mode (no forbidden flags), and all completed before timeout.

| Row | Declared exit/state | Observed exit | Evidence fragment | Fragment match | Verdict |
|---|---:|---:|---|---|---|
| polyglot-c-py-probe | 0 / green | 0 | none declared (green row) | n/a | CONFIRMED |
| regex-log-probe | 0 / green | 0 | none declared (green row) | n/a | CONFIRMED |
| registry-reference-check | 0 / green | 0 | none declared (green row) | n/a | CONFIRMED |

## Exact argv and terminal output tails

### polyglot-c-py-probe

```text
python3 plans/polyglot_c_py_probe.py --lane .
```

```text
regrade cases=18 differ=7
cases=18 observed_pass=7 observed_fail=11 mismatches=0
```

### regex-log-probe

```text
python3 plans/regex_log_probe.py --lane .
```

```text
case=feb-29-rejected predicted=pass observed=pass match=yes assertion='-' requirement='February can have up to 29 days (the permitting side is unobserved)'
cases=24 observed_pass=8 observed_fail=16 mismatches=0
```

### registry-reference-check

```text
python3 plans/registry_check.py --summary
```

```text
SCOPE frozen13 source rows / baseline35 knowledge files; literal mentions, not source truth; new files excluded
TOTAL source_rows_checked=13 knowledge_files_expected=35 reference_links=12 mismatch_sources=0 finding_count=0 exit=0
```

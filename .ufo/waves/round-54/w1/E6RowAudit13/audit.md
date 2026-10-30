# R54-C2 assigned-row re-execution

Source: shared clone of current lane tip `62e9bba5e4a0bed376890299aa6a09039db7e68e` at `/fast/scratch/hyaku/kengaku-r54/E6RowAudit13/tmp.1kISC5Pdz3/clone`. Each command ran with counter `hermetic_env` imported from `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round54_c2_entrytruth.py`, TMPDIR `/fast/scratch/hyaku/kengaku-r54/E6RowAudit13/tmp.1kISC5Pdz3/tmp`, and a 600-second per-row timeout. All scripts exist and all argv are entry mode (no forbidden selftest/help/dry/version token).

## Results

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| round33-defects | 0 | 0 | N/A (green) | CONFIRMED |
| round35-c1-coverage | 1 | 1 | true | CONFIRMED |
| round35-hardening | 0 | 0 | N/A (green) | CONFIRMED |

## Exact commands and output tails

`python3 plans/round33_defects.py --lane .` (timeout 600)

```text
checks=6 defects=0
```

`python3 plans/round35_c1_verify.py --lane .` (timeout 600)

```text
V1 ok
V2 ok
V3 ok
V4 DEFECT knowledge files=57 index rows=57 (want 42/42)
V5 ok
V6 ok
checks=6 defects=1
PREDICATE C1 fail
```
The declared red fragment occurs verbatim.

`python3 plans/round35_hardening.py --lane .` (timeout 600)

```text
H1 ok changed_since_freeze=0
H2 ok rows=22 unparsed=0 distinct_quotes=22 distinct_lines=22
H3 ok short_teaches=0
H4 ok draft_clause=True harness_clause=True green_word=True
H5 ok directional=True capture_pinned=True
H6 ok untracked_anywhere=0
hardening run=6 failed=0
```

No installs or updates. No build, lint, test, formatter, or verification suite run; this was the assigned row re-execution audit only.

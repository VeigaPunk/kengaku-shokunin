# FxAdoptionAfter — C1 draft counter reachability

## Scope and result

Tested the uncommitted C1 draft state only; no files were modified.

Command run from lane root:

```text
$ python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
EXIT_CODE=0
```

**VERDICT: predicate-reachable**

The expected frozen after-line is printed from the existing drafts with no further edit. The command exited 0.

## Checks

- **S093 used-by:** `corpus/SOURCES.md` line 112 parses as an 11-cell row; the `used-by` cell is `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md`. It contains the new entry path.
- **Index row regex:** applying the counter's anchored index-row regex (`^\| `knowledge/benchmark-grader-semantics.md` \|`) to `corpus/README.md` matched exactly one row (`index_row_match_count=1`); it is line 67.
- **Draft sources/date:** the entry's `source:` lines yield exactly `S093`, `S094`, `S097`; its `verified-at:` line is `2026-10-25`.
- **Registry rows:** the counter-compatible row regex found S093 at line 112, S094 at line 114, and S097 at line 115. Each parsed row has 11 cells, `status=mined`, and `opened=2026-10-25`; S094 and S097 used-by name the entry.

The counter implementation at `plans/adoption_check.py:119-124` counts index-row regex matches and requires exactly one; lines 132-142 run the census and map its return code to `ok`/`fail`; lines 149-164 gate exit 0 on the expected counts and all frozen checks.

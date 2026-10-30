# R54-C2 independent row re-execution

Clone: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit20/clone` (current lane tip). Each command ran from that clone with `env=hermetic_env(/fast/scratch/hyaku/kengaku-r54/E6RowAudit20/tmp/<row>)`, imported from `plans/round54_c2_entrytruth.py`; each had a 600-second timeout. All scripts existed and argv were entry mode (no selftest/help/dry/version switches). No ledger evidence fragment applies: these three rows are green and carry no `evidence` field.

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| round44-c2 | 0 | 0 | n/a | CONFIRMED |
| round45-c1 | 0 | 0 | n/a | CONFIRMED |
| round45-c2 | 0 | 0 | n/a | CONFIRMED |

## Commands and output tails

### round44-c2

`python3 plans/round44_c2_verify.py --lane .`

Exit 0. Tail:
```
V1 ok listed=11 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
    gate: P4 ok checked=22 bad=0 first=0
    gate: P5 ok manifest_entries=11 bad=0 first=0
    gate: P6 ok rows=9 bad=0 first=0
    gate: P7 ok source_lines=9 bad=0 first=0
    gate: P8 ok index_rows=57 knowledge_files=57 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=3630
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=9 bad=0
V4 ok cases=14 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=14/14 bad=0
V10 ok mechanism_rows=14/14 bad=0
V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0
checks=11 defects=0
PREDICATE C2 pass
```

### round45-c1

`python3 plans/round45_c1_verify.py --lane .`

Exit 0. Tail:
```
FENCE-RUN honest battery44/u9_worktree_b.py u9_worktree_b-erratum-completed-in-place ADMIT opens=0
REFUSAL f10_laneinclude.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f1_gitfile.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f2_deep.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f3_abbrev.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f4_fifo.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f5_alternates.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f6_above.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f7_commondir.py clean fixtures=3 admitted=0 hung=0 opens=0
REFUSAL f8_worktreecfg.py clean fixtures=2 admitted=0 hung=0 opens=0
REFUSAL f9_nodescribe.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
```

### round45-c2

`python3 plans/round45_c2_verify.py --lane .`

Exit 0. Tail:
```
V1 ok listed=9 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=19 distinct_quotes=19 distinct_lines=19 out_of_word_range=0
    gate: P4 ok checked=19 bad=0 first=0
    gate: P5 ok manifest_entries=9 bad=0 first=0
    gate: P6 ok rows=8 bad=0 first=0
    gate: P7 ok source_lines=8 bad=0 first=0
    gate: P8 ok index_rows=57 knowledge_files=57 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=4659
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=8 bad=0
V4 ok cases=16 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=9 tags=9 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=16/16 bad=0
V10 ok mechanism_rows=16/16 bad=0
V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0
checks=11 defects=0
PREDICATE C2 pass
```

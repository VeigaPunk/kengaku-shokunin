# R54-C2 independent row audit

Clone HEAD: `62e9bba5e4a0bed376890299aa6a09039db7e68e`
Hermetic environment: imported `hermetic_env` from frozen `plans/round54_c2_entrytruth.py`; each run used its row-specific `$TMPDIR` under this seat scratch directory. Timeout: 600 seconds per row.

| Row | Declared | Observed | Fragment match | Entry mode / script exists | Verdict |
|---|---:|---:|---|---|---|
| round46-c1 | 0 | 0 | None | True / True | **CONFIRMED** |

## Commands and observed output tails

| round46-c2 | 0 | 0 | None | True / True | **CONFIRMED** |

## Commands and observed output tails

| round46-c3 | 1 | 1 | True | True / True | **CONFIRMED** |

## Commands and observed output tails

### round46-c1

`python3 plans/round46_c1_verify.py --lane .` (cwd: clone root; 600s cap)

```text
SEALED s_refs_link.py clean fixtures=1 admitted=0 hung=0 touches=0
SEALED p_pack_redirect.py clean fixtures=1 admitted=0 hung=0 touches=0
SEALED p_info_redirect.py clean fixtures=1 admitted=0 hung=0 touches=0
SEALED s_packed_refs.py clean fixtures=1 admitted=0 hung=0 touches=0
SEALED c_excludes_file.py clean fixtures=1 admitted=0 hung=0 touches=0
SEALED p_refs_redirect.py clean fixtures=1 admitted=0 hung=0 touches=0
SEALED c_core_attributes_path.py clean fixtures=1 admitted=0 hung=0 touches=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=32 contradicted=0
REASON -
PREDICATE C1 pass
```

### round46-c2

`python3 plans/round46_c2_verify.py --lane .` (cwd: clone root; 600s cap)

```text
PINS total=3 mismatched=0
A anchorline live=0 repaired=8 base_rows=149 base_missing=0 base_changed=0 ok
B predictor states=16 grader_pass=10 grader_fail=6 disagree=0 ok
C entry source_ranges=9 source_ranges_bad=0 errata_marks=5/5 ok
D selftest exit=0 ok
checks=4 defects=0
PREDICATE C2 pass
```

### round46-c3

`python3 plans/round46_c3_verify.py --lane .` (cwd: clone root; 600s cap)

```text
V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
checks=13 defects=2
PREDICATE C3 fail
```

Declared evidence fragment `V1 ok listed=8 wrong=0 extra=0` appears in the observed output: **True**.


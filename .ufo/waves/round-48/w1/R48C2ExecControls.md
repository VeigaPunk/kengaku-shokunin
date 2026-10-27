# R48C2ExecControls — C2 pre-receipt controls, P10 disabled (executor)

Axes named: **coverage** (R48-C2 only). No other axis assessed; no admission claimed for R48-C1 or R48-C2.

## Freeze gate (checked before the first measurement)

The stage-1 freeze exists in the committed lane tree and predates every measurement below.

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %cI %s' a543d92083557dd9b33ee674e9b99b03411f80af
a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27T06:53:29-03:00 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims
$ git -C ... merge-base --is-ancestor a543d92083557dd9b33ee674e9b99b03411f80af HEAD   -> exit 0
$ git -C ... rev-parse HEAD
bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767
```

Freeze instant `2026-10-27T06:53:29-03:00` = `09:53:29Z`; the three control runs carry `run_utc=2026-10-27T11:37:09Z`, `…11:37:12Z`, `…11:37:15Z`. Freeze precedes measurement by ~1h44m.

No stage-2 instrument exists yet, so **no scored counter or probe execution was made on claimed work**:

```
$ git ls-tree -r --name-only a543d92 | grep -E 'round48_c2|polyglot|order_check|round48_c1'
(no plans/round48_c2_verify.py, no plans/round48_c1_verify.py; plans/polyglot_c_py_probe.py and plans/order_check.py present)
```

Named fact measured, not inferred: claim §C2 describes the hardened probe (`sha256 22b7779e…`) as "integrated verbatim to `plans/polyglot_c_py_probe.py`". At the frozen base that is not yet true —

```
67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26  base/plans/polyglot_c_py_probe.py
22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d  base/.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  base/plans/pkg_gate.py
a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4  base/plans/round46_c3_verify.py
99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536  base/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt
dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277  base/corpus/evidence/round46/polyglot-c-py-probe.txt
```

The base carries the round-46 probe (`67a8f4a6…`); the `22b7779e…` integration is a wave-1 task (seat `R48C2ExecProbe`). The base control below is therefore exactly what its name says: the frozen tree **with `plans/polyglot_c_py_probe.py` removed**.

## Instruments (both scratch-only; neither is the stage-2 pin)

| instrument | sha256 | role |
|---|---|---|
| `cand/round48_c2_verify.py` (mine) | `e0ddd97e33a0444c928f6b2feba9e85f625f8b1832c8c7d5efcb039058c30397` | imports `plans/round46_c3_verify.py` pinned at `a971c24d…`; frozen deltas: `V7P` (delta a, tag coverage from the frozen tables alone), `--no-p10` gate path (delta b), `V15` (delta c, precondition dry-run), `V14` defect-with-reason while `<N>` is unpinned (delta d) |
| `cand/run_controls.py` | `0171be3368df813b5edd8af55b297ba0657ecbe0aedff1d3d5ff36ccde5140d5` | builds each control tree as a `git clone --shared` of the lane at `a543d92`, commits the counter and the transform, runs the counter, writes the receipt |
| `…/R48C2ExecCounter/candidate/round48_c2_verify.py` (sibling seat, read-only) | `2c574c84dcbf3b16b9254d07fd16d5cfd3ffa540b991cd1f37b931db681ef236` | cross-run with `--control base|filler|echo` |

Structural fence in my candidate: without `--no-p10` it refuses to run, so this wave-1 file cannot be pointed at the claimed work.

```
$ python3 cand/round48_c2_verify.py --lane control-r48-c2-base/lane --work $PWD/smoke
REV 787691a96b41dc147d0c8f3fc518c1330f4bf8db
REV_DIRTY 0
SETUP wave-1 control instrument: scored mode (P10 enabled) refused; pass --no-p10
checks=0 defects=0
PREDICATE R48-C2 not-run
EXIT=2
```

## Control transforms and measured revisions

Each receipt's `REV` is a real commit id inside the seat scratch: `a543d92` → `9a739c3` (candidate counter committed) → transform commit. The transform commit message, diffstat and the counter digest are printed in each receipt header. All trees report `REV_DIRTY 0`, so the gate's `P9` clean-tree clause is meaningful rather than a dirt artefact.

| control | transform | REV | checks | defects | content defects | predicate |
|---|---|---|---|---|---|---|
| base | `plans/polyglot_c_py_probe.py` deleted (526 deletions) | `787691a96b41dc147d0c8f3fc518c1330f4bf8db` | 16 | 7 | 5 (`V2,V5,V7,V7P,V8`) | **fail** |
| filler | none (`plans/filler46/` scored via `--filler`) | `ecf768d0dd364a5789816c93d7f4cb77090e7e0e` | 11 | 8 | 7 (`V4,V6,V7,V7P,V9,V10,V12`) | **fail** |
| echo | dry table copied over `corpus/evidence/round46/polyglot-c-py-probe.txt` | `4ffb15d00b2d5be3830446d8c35e4fdd18ae9b12` | 16 | 6 | 5 (`V4,V7,V7P,V8,V9`) | **fail** |

Receipt digests: base `20d3339d6cb8b7afcd153d64ae94da3d9de0d4c6f69411b9e60f957430a8f2de`, filler `1092fb5df5a84fde95672a4e2529965b310c15ce66d693bb2b92a490440413b5`, echo `2fccabc88089853c822f059e34f59f0f06c8c76acae49513fd6858f6053eb600`.

## Degradation is not the verdict's source

`V14` is a defect by the counter's own rule ("a leg that cannot run is a defect, never a pass") because `<N>` and the floor are stage-2 literals and the wave-1 mutant payloads are not present; `V15` is a real precondition leg. The fail verdict does **not** rest on either: each control has ≥5 **content** defects, printed as a `content_defects=` line. A stage-2 counter that runs `V14` for real cannot flip any of the three.

## Verbatim control receipts

### control-r48-c2-base — REV 787691a96b41dc147d0c8f3fc518c1330f4bf8db

```
REV 787691a96b41dc147d0c8f3fc518c1330f4bf8db
# control control-r48-c2-base: base tree: plans/polyglot_c_py_probe.py deleted; gate run with P10 disabled
# measured tree: clone of lane a543d92083557dd9b33ee674e9b99b03411f80af + committed transforms, run at /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/control-r48-c2-base/lane
# candidate counter plans/round48_c2_verify.py sha256=e0ddd97e33a0444c928f6b2feba9e85f625f8b1832c8c7d5efcb039058c30397
# transform: 787691a96b41dc147d0c8f3fc518c1330f4bf8db control transform: plans/polyglot_c_py_probe.py deleted (base tree, no probe)
# transform: 
# transform:  plans/polyglot_c_py_probe.py | 526 -------------------------------------------
# transform:  1 file changed, 526 deletions(-)
# freeze a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27T06:53:29-03:00 (stage-1, plans/round-48-claims.md)
ORDER reason=ORDER FAIL freeze-contains-receipt a543d92083557dd9b33ee674e9b99b03411f80af already has corpus/evidence/round46/polyglot-c-py-probe.txt | ORDER FAIL receipt-before-claims 8d7f74ce63c25ad200c69fe0d90158cc7099def6 is an ancestor of a543d92083557dd9b33ee674e9b99b03411f80af
ORDER receipt=corpus/evidence/round46/polyglot-c-py-probe.txt in_HEAD=yes order_check_exit=1 ORDER RESULT FAIL
ORDER reason=ORDER ERROR receipt not committed in HEAD: corpus/evidence/round48/polyglot-c-py-probe.txt
ORDER receipt=corpus/evidence/round48/polyglot-c-py-probe.txt in_HEAD=absent order_check_exit=2 ORDER RESULT ERROR
ORDER run_utc=2026-10-27T11:37:09Z receipt_files_under_corpus/evidence/round48=0
REV 787691a96b41dc147d0c8f3fc518c1330f4bf8db
REV_DIRTY 0
MODE control --no-p10 (gate P10/fresh-probe leg disabled, frozen V8 fix)
V1 ok listed=8 wrong=0 extra=0
    gate: P1 DEFECT pinned=2 mismatched=['plans/polyglot_c_py_probe.py']
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
    gate: P4 ok checked=20 bad=0 first=0
    gate: P5 ok manifest_entries=8 bad=0 first=0
    gate: P6 ok rows=7 bad=0 first=0
    gate: P7 ok source_lines=7 bad=0 first=0
    gate: P8 ok index_rows=53 knowledge_files=53 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: defects=1
V2 DEFECT spec=frozen gate=frozen p10=disabled gate_exit=1
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V5 DEFECT probe or dry table not at its freeze digest
V6 ok census_exit=0 registry=corpus/SOURCES.md
V7 DEFECT rows=5 tags=7 bad=["unparsed row '| instruction.md:7 | both-print | not exercised | '", "unparsed row '| instruction.md:9 | toolchain | not exercised | n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]
V7P DEFECT tags=7 parsed_cases=18 map_rows=5 cited=5/7 bad=['both-print: no committed case violates it', 'toolchain: no committed case violates it', 'both-print: round-46 V7 offender still uncovered', 'toolchain: round-46 V7 offender still uncovered', "unparsed requirement-map rows=['| instruction.md:7 | both-print | not exercised | no frozen ', '| instruction.md:9 | toolchain | not exercised | no frozen c']", 'requirement-map rows=5 frozen tags=7', "map tags differ from frozen tags (missing=['both-print', 'toolchain'] extra=[])"]
V8 DEFECT order_exit=1 result=not-PASS
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
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
V14 DEFECT mutation floor <N> unpinned (stage-2 literal); wave-1 mutants absent
V15 DEFECT inputs=4 unresolved=['probe'] tables_parsed=2 tags=7
content_defects=5 (V2,V5,V7,V7P,V8)
checks=16 defects=7
PREDICATE R48-C2 fail
# exit=1
```

### control-r48-c2-filler — REV ecf768d0dd364a5789816c93d7f4cb77090e7e0e

```
REV ecf768d0dd364a5789816c93d7f4cb77090e7e0e
# control control-r48-c2-filler: the committed filler package plans/filler46/ scored as the package (--filler)
# measured tree: clone of lane a543d92083557dd9b33ee674e9b99b03411f80af + committed transforms, run at /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/control-r48-c2-filler/lane
# candidate counter plans/round48_c2_verify.py sha256=e0ddd97e33a0444c928f6b2feba9e85f625f8b1832c8c7d5efcb039058c30397
# transform: ecf768d0dd364a5789816c93d7f4cb77090e7e0e control transform: none (filler package scored via --filler)
# freeze a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27T06:53:29-03:00 (stage-1, plans/round-48-claims.md)
ORDER reason=ORDER FAIL freeze-contains-receipt a543d92083557dd9b33ee674e9b99b03411f80af already has corpus/evidence/round46/polyglot-c-py-probe.txt | ORDER FAIL receipt-before-claims 8d7f74ce63c25ad200c69fe0d90158cc7099def6 is an ancestor of a543d92083557dd9b33ee674e9b99b03411f80af
ORDER receipt=corpus/evidence/round46/polyglot-c-py-probe.txt in_HEAD=yes order_check_exit=1 ORDER RESULT FAIL
ORDER reason=ORDER ERROR receipt not committed in HEAD: corpus/evidence/round48/polyglot-c-py-probe.txt
ORDER receipt=corpus/evidence/round48/polyglot-c-py-probe.txt in_HEAD=absent order_check_exit=2 ORDER RESULT ERROR
ORDER run_utc=2026-10-27T11:37:12Z receipt_files_under_corpus/evidence/round48=0
REV ecf768d0dd364a5789816c93d7f4cb77090e7e0e
REV_DIRTY 0
MODE control --no-p10 (gate P10/fresh-probe leg disabled, frozen V8 fix)
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
V7P DEFECT tags=4 parsed_cases=16 map_rows=4 cited=0/4 bad=['single-file: no committed case violates it', 'python-run: no committed case violates it', 'c-run: no committed case violates it', 'fib: no committed case violates it']
V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V14 DEFECT mutation floor <N> unpinned (stage-2 literal); wave-1 mutants absent
V15 ok inputs=8 unresolved=0 tables_parsed=2 tags=4
content_defects=7 (V4,V6,V7,V7P,V9,V10,V12)
checks=11 defects=8
PREDICATE R48-C2 fail
# exit=1
```

### control-r48-c2-echo — REV 4ffb15d00b2d5be3830446d8c35e4fdd18ae9b12

```
REV 4ffb15d00b2d5be3830446d8c35e4fdd18ae9b12
# control control-r48-c2-echo: the frozen dry table copied as the receipt (echo); gate run with P10 disabled
# measured tree: clone of lane a543d92083557dd9b33ee674e9b99b03411f80af + committed transforms, run at /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/control-r48-c2-echo/lane
# candidate counter plans/round48_c2_verify.py sha256=e0ddd97e33a0444c928f6b2feba9e85f625f8b1832c8c7d5efcb039058c30397
# transform: 4ffb15d00b2d5be3830446d8c35e4fdd18ae9b12 control transform: frozen dry table copied over the probe receipt path (echo)
# transform: 
# transform:  corpus/evidence/round46/polyglot-c-py-probe.txt | 54 ++++++++++++-------------
# transform:  1 file changed, 26 insertions(+), 28 deletions(-)
# freeze a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27T06:53:29-03:00 (stage-1, plans/round-48-claims.md)
ORDER reason=ORDER FAIL freeze-contains-receipt a543d92083557dd9b33ee674e9b99b03411f80af already has corpus/evidence/round46/polyglot-c-py-probe.txt | ORDER FAIL receipt-before-claims 8d7f74ce63c25ad200c69fe0d90158cc7099def6 is an ancestor of a543d92083557dd9b33ee674e9b99b03411f80af
ORDER receipt=corpus/evidence/round46/polyglot-c-py-probe.txt in_HEAD=yes order_check_exit=1 ORDER RESULT FAIL
ORDER reason=ORDER ERROR receipt not committed in HEAD: corpus/evidence/round48/polyglot-c-py-probe.txt
ORDER receipt=corpus/evidence/round48/polyglot-c-py-probe.txt in_HEAD=absent order_check_exit=2 ORDER RESULT ERROR
ORDER run_utc=2026-10-27T11:37:15Z receipt_files_under_corpus/evidence/round48=0
REV 4ffb15d00b2d5be3830446d8c35e4fdd18ae9b12
REV_DIRTY 0
MODE control --no-p10 (gate P10/fresh-probe leg disabled, frozen V8 fix)
V1 ok listed=8 wrong=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
    gate: P4 ok checked=20 bad=0 first=0
    gate: P5 ok manifest_entries=8 bad=0 first=0
    gate: P6 ok rows=7 bad=0 first=0
    gate: P7 ok source_lines=7 bad=0 first=0
    gate: P8 ok index_rows=53 knowledge_files=53 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: defects=0
V2 ok spec=frozen gate=frozen p10=disabled gate_exit=0
V3 ok rows=7 bad=0
V4 DEFECT cases=18 mismatches_named=0/0 bad=['case ids differ from the frozen table', 'summary line count != 1']
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0 registry=corpus/SOURCES.md
V7 DEFECT rows=5 tags=7 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-build: no receipt case violates it', "unparsed row '| instruction.md:7 | both-print | not exercised | '", 'fib-kth: no receipt case violates it', 'stdout-only: no receipt case violates it', "unparsed row '| instruction.md:9 | toolchain | not exercised | n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]
V7P DEFECT tags=7 parsed_cases=0 map_rows=5 cited=0/7 bad=['single-file: no committed case violates it', 'python-run: no committed case violates it', 'c-build: no committed case violates it', 'both-print: no committed case violates it', 'fib-kth: no committed case violates it', 'stdout-only: no committed case violates it', 'toolchain: no committed case violates it', 'both-print: round-46 V7 offender still uncovered', 'toolchain: round-46 V7 offender still uncovered', "unparsed requirement-map rows=['| instruction.md:7 | both-print | not exercised | no frozen ', '| instruction.md:9 | toolchain | not exercised | no frozen c']", 'requirement-map rows=5 frozen tags=7', "map tags differ from frozen tags (missing=['both-print', 'toolchain'] extra=[])"]
V8 DEFECT order_exit=1 result=not-PASS
V9 DEFECT case_rows=18/0 bad=['case table rows=18 receipt cases=0 equal=False']
V10 ok mechanism_rows=18/18 bad=0
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
V14 DEFECT mutation floor <N> unpinned (stage-2 literal); wave-1 mutants absent
V15 ok inputs=4 unresolved=0 tables_parsed=2 tags=7
content_defects=5 (V4,V7,V7P,V8,V9)
checks=16 defects=6
PREDICATE R48-C2 fail
# exit=1
```

## Frozen V8 outcome, measured

1. **base** — the gate refused the tree with P10 absent: `gate: P1 DEFECT pinned=2 mismatched=['plans/polyglot_c_py_probe.py']`, `gate: defects=1`, `V2 DEFECT spec=frozen gate=frozen p10=disabled gate_exit=1`. No `P10` leg line was printed.
2. **echo** — the gate **accepted** the echo tree with P10 absent: `gate: defects=0`, `V2 ok … p10=disabled gate_exit=0`. That is a real, reportable property: with `--rerun` omitted, `P10` is the only gate clause that compares receipt *content* against a fresh probe, so a dry-table receipt passes `P1–P9`. The echo control is still refused, by the counter's own content legs: `V4 DEFECT … bad=['case ids differ from the frozen table', 'summary line count != 1']`, `V9 DEFECT case_rows=18/0`, `V7P DEFECT … parsed_cases=0`, `V7 DEFECT … 5 tags: no receipt case violates it`. Recorded as observed; nothing was re-frozen, weakened or re-labelled.
3. **filler** — `--filler` mode does not run the package gate (round-46 contract); refusal comes from `V4,V6,V7,V7P,V9,V10,V12`.

## Frozen delta (a), observed on the frozen base

`V7P DEFECT tags=7 parsed_cases=18 map_rows=5 cited=5/7` with `bad=['both-print: no committed case violates it', 'toolchain: no committed case violates it', … "unparsed requirement-map rows=['| instruction.md:7 | both-print | not exercised | no frozen ', '| instruction.md:9 | toolchain | not exercised | no frozen c']", 'requirement-map rows=5 frozen tags=7']`.

The round-46 V7 shape is present verbatim in the committed bytes: the two rows exist but carry the label `not exercised`, which does not parse as `enforced|unenforced|partly`, and neither tag has a violating committed case. Delta (a) therefore catches, on the frozen tree, exactly the defect the round-46 spot-check named.

## No-P10 discipline (checked mechanically)

`plans/order_check.py` regexes (`GATE_P10`, `CASE … observed=`) applied to all three receipts:

```
gate_p10_lines= 0   executed_case_lines= 0        (base)
gate_p10_lines= 0   executed_case_lines= 0        (echo)
gate_p10_lines= 0   executed_case_lines= 0        (filler)
```

The only `P10` strings are the `MODE control --no-p10` line, `p10=disabled` inside `V2`'s detail, and the receipt header. No control executed the probe: the frozen probe ran `--dry` only (`V5 ok probe=frozen dry_byte_equal=True`), and the full 18-case table never ran.

## Ordering receipts pinned

Every receipt carries the same pin block (per-tree, verbatim):

```
# freeze a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27T06:53:29-03:00 (stage-1, plans/round-48-claims.md)
ORDER reason=ORDER FAIL freeze-contains-receipt … already has corpus/evidence/round46/polyglot-c-py-probe.txt | ORDER FAIL receipt-before-claims 8d7f74ce63c25ad200c69fe0d90158cc7099def6 is an ancestor of a543d92…
ORDER receipt=corpus/evidence/round46/polyglot-c-py-probe.txt in_HEAD=yes order_check_exit=1 ORDER RESULT FAIL
ORDER reason=ORDER ERROR receipt not committed in HEAD: corpus/evidence/round48/polyglot-c-py-probe.txt
ORDER receipt=corpus/evidence/round48/polyglot-c-py-probe.txt in_HEAD=absent order_check_exit=2 ORDER RESULT ERROR
ORDER run_utc=2026-10-27T11:37:09Z receipt_files_under_corpus/evidence/round48=0
```

Direct re-run of the ordering gate on a control tree, outside the harness:

```
$ python3 plans/order_check.py --lane . --claims plans/round-48-claims.md --receipt corpus/evidence/round46/polyglot-c-py-probe.txt
ORDER RESULT FAIL
EXIT=1
$ python3 plans/order_check.py --lane . --claims plans/round-48-claims.md --receipt corpus/evidence/round48/polyglot-c-py-probe.txt
ORDER ERROR receipt not committed in HEAD: corpus/evidence/round48/polyglot-c-py-probe.txt
ORDER RESULT ERROR
EXIT=2
```

Read as evidence: (i) the round-46 receipt cannot serve as the round-48 receipt — it is already inside the freeze commit, so `order_check` fails `freeze-contains-receipt` and `receipt-before-claims`; (ii) **no round-48 probe receipt exists in HEAD at all** (`in_HEAD=absent`, `receipt_files_under_corpus/evidence/round48=0`), which is the ordering property these controls must hold: they ran before any receipt could exist. Stage 2 must name the round-48 receipt path; the `corpus/evidence/round48/…` path used above is this seat's probe of the ordering gate, not a frozen literal.

## Cross-run with the sibling canonical candidate (independent instrument)

Command, three times (`base`, `filler`, `echo`):

```
python3 /fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py \
    --lane /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/base --control <name> --work <scratch>/w-canon-<name>
```

`--control` excludes the `V2` probe leg by construction. Exit 1 on all three.

### cross-canon-base — REV a543d92083557dd9b33ee674e9b99b03411f80af
```
REV a543d92083557dd9b33ee674e9b99b03411f80af
# cross-run: canonical wave-1 candidate counter (seat R48C2ExecCounter) by seat R48C2ExecControls
# counter sha256=3de23dafd2b5abb43c31d31f2beb1cc3f34e5b1607951a7698ec57f11eaba43d path=/fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py
# lane tree: /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/base (clone of lane a543d920, unmodified)
# command: python3 /fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py --lane /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/base --control base --work /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-base
CONTROL base tree=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-base/k48-c2-lqgti7rr/ctl-base p10=disabled
V15 DEFECT inputs=11 tables=6 blocked=2
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V5 DEFECT probe or dry table not at its freeze digest
V6 ok census_exit=0 registry=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-base/k48-c2-lqgti7rr/ctl-base/corpus/SOURCES.md
V7 DEFECT rows=7 tags=7 violated=5/7 bad=7 first=both-print:no committed case carries violates=both-print
V8 DEFECT controls=3 package_order=fail bad=4 first=package order exit=1
V9 DEFECT precondition: the case table is absent
V10 DEFECT precondition: the mechanism section is absent
V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-base/k48-c2-lqgti7rr/ctl-base/plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
V14 DEFECT mutation literals pending (stage-2 pins MUT_N and MUT_FLOOR)
checks=14 defects=7
PREDICATE R48-C2 fail
```

### cross-canon-filler
```
REV a543d92083557dd9b33ee674e9b99b03411f80af
# cross-run: canonical wave-1 candidate counter (seat R48C2ExecCounter) by seat R48C2ExecControls
# counter sha256=3de23dafd2b5abb43c31d31f2beb1cc3f34e5b1607951a7698ec57f11eaba43d path=/fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py
# lane tree: /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/base (clone of lane a543d920, unmodified)
# command: python3 /fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py --lane /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/base --control filler --work /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-filler
CONTROL filler tree=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-filler/k48-c2-9fn9ebi3/ctl-filler p10=disabled
V15 DEFECT inputs=11 tables=6 blocked=7
V1 DEFECT precondition: a capture does not resolve to its frozen digest
V3 ok rows=7 bad=0
V4 DEFECT precondition: the dry table is absent or not at its frozen digest
V5 DEFECT precondition: the dry table is absent or not at its frozen digest
V6 DEFECT census_exit=1 registry=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-filler/k48-c2-9fn9ebi3/ctl-filler/plans/filler46/SOURCES-filler.md
V7 DEFECT precondition: the dry table is absent or not at its frozen digest
V8 DEFECT controls=3 package_order=fail bad=4 first=package order exit=1
V9 DEFECT precondition: the case table is absent
V10 DEFECT precondition: a capture does not resolve to its frozen digest
V11 DEFECT grader capture not at its frozen digest
V12 DEFECT precondition: a capture does not resolve to its frozen digest
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-filler/k48-c2-9fn9ebi3/ctl-filler/plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
V14 DEFECT mutation literals pending (stage-2 pins MUT_N and MUT_FLOOR)
checks=14 defects=12
PREDICATE R48-C2 fail
```

### cross-canon-echo
```
REV a543d92083557dd9b33ee674e9b99b03411f80af
# cross-run: canonical wave-1 candidate counter (seat R48C2ExecCounter) by seat R48C2ExecControls
# counter sha256=3de23dafd2b5abb43c31d31f2beb1cc3f34e5b1607951a7698ec57f11eaba43d path=/fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py
# lane tree: /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/base (clone of lane a543d920, unmodified)
# command: python3 /fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py --lane /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/base --control echo --work /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-echo
CONTROL echo tree=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-echo/k48-c2-7nq0tggo/ctl-echo p10=disabled
V15 DEFECT inputs=11 tables=6 blocked=4
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 DEFECT precondition: the receipt parses to zero CASE lines
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0 registry=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-echo/k48-c2-7nq0tggo/ctl-echo/corpus/SOURCES.md
V7 DEFECT precondition: the receipt parses to zero CASE lines
V8 DEFECT controls=3 package_order=fail bad=4 first=package order exit=1
V9 DEFECT precondition: the receipt parses to zero CASE lines
V10 DEFECT precondition: the receipt parses to zero CASE lines
V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/w-canon-echo/k48-c2-7nq0tggo/ctl-echo/plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
V14 DEFECT mutation literals pending (stage-2 pins MUT_N and MUT_FLOOR)
checks=14 defects=7
PREDICATE R48-C2 fail
```

Two independently written instruments, on the same frozen base, agree: `checks=16 defects=7`, `checks=11 defects=8`, `checks=16 defects=6` (mine) versus `checks=14 defects=7`, `checks=14 defects=12`, `checks=14 defects=7` (sibling) — **all six runs print `PREDICATE R48-C2 fail`**.

Divergences worth the L1's attention when pinning (reported, not re-frozen):

- **Echo gate acceptance.** The sibling `V8` demands each control be *refused by the gate* (`exit 1`). With `--rerun` omitted the gate accepts the echo tree (`gate_exit=0`, `gate: defects=0`), so that clause cannot hold for the echo control at this base. The echo is caught by `V4/V7/V9`, not by the gate.
- **Filler pin set.** The sibling `V15` applies the real package's `CAPTURES` digests to the filler control package, whose captures are deliberately different bytes, so its filler legs report `precondition: a capture does not resolve to its frozen digest` instead of the content defects `V4/V7/V9/V10/V12`. My `V15` checks the filler's own `SHA256SUMS` and lets the content legs speak. Both reject the filler; only the second yields a per-leg content record.
- **`V15` blocking.** The sibling `V15` blocks the legs that read stage-2-pending inputs (`blocked=2/7/4`), faithful to delta (c), which means its control receipts defect partly on absent stage-2 material. Mine runs the legs and lets them defect individually.

## Commands run (exact)

```
git -C <lane> log -1 --format='%H %cI %s' a543d92083557dd9b33ee674e9b99b03411f80af
git -C <lane> merge-base --is-ancestor a543d92083557dd9b33ee674e9b99b03411f80af HEAD
git -C <lane> ls-tree -r --name-only a543d92083557dd9b33ee674e9b99b03411f80af | grep -E 'round48_c2|polyglot|order_check|round48_c1'
git clone -q --shared <lane> /fast/scratch/hyaku/kengaku-r48/R48C2ExecControls/base
git -C base checkout -q a543d92083557dd9b33ee674e9b99b03411f80af ; git -C base rev-parse --show-toplevel
sha256sum base/plans/polyglot_c_py_probe.py base/.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py base/plans/pkg_gate.py base/plans/round46_c3_verify.py base/corpus/evidence/round46/polyglot-c-py-probe.txt base/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt base/plans/order_check.py
TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls python3 cand/run_controls.py
python3 cand/round48_c2_verify.py --lane control-r48-c2-base/lane --work $PWD/smoke          # scored-mode refusal, exit 2
python3 /fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py --lane <scratch>/base --control base|filler|echo --work <scratch>/w-canon-<name>
python3 plans/order_check.py --lane <control tree> --claims plans/round-48-claims.md --receipt corpus/evidence/round46/polyglot-c-py-probe.txt
python3 plans/order_check.py --lane <control tree> --claims plans/round-48-claims.md --receipt corpus/evidence/round48/polyglot-c-py-probe.txt
```

Every fixture git call ran as `git -C "$D" …` with `D` inside `/fast/scratch/hyaku/kengaku-r48/R48C2ExecControls`, and each run asserts `git rev-parse --show-toplevel` equals `$D` before any write. No write touched the lane: the lane's `git status --porcelain` shows only the L1's own untracked `.ufo/waves/round-48/` dispatch material and `corpus/lessons/round-48.md`.

## Limits

1. **No stage-2 pin exists** (`plans/round48_c2_verify.py`, `<V>`, `<N>`, mutant plan, control-receipt paths are all absent). These receipts come from two *wave-1 candidates*, not the pinned counter; stage 2 must re-run the committed counter to make the pinnable receipts. `V14` is therefore a defect-by-rule here.
2. **`V11` executes the captured grader on 60 counter-generated states**, never the frozen 18-case probe table (`states=60 grader_pass=15 grader_fail=45 disagree=0`). The frozen probe ran `--dry` only; no full probe run, no `--rerun`, no `P10` line anywhere.
3. **Host divergence**: host `python3 3.14.8` and `gcc 16.2.1` stand in for the image's runtimes, as the round-46 probe already records.
4. **Receipts live in this report, not as loose files**: my write scope is this one report path, so each receipt is embedded verbatim above with its digest. The scratch tree, including all three control clones and both receipt sets, was removed before this report was finalised; the digests above are the only handle on them.
5. The `corpus/evidence/round48/polyglot-c-py-probe.txt` path is this seat's ordering probe, not a frozen literal; stage 2 must name the real receipt path.
6. No tool was installed or upgraded; nothing in `~/.local/bin` or any PATH directory was touched.

## Sources opened (all accessed 2026-10-27)

| URL | located quote (≤25 words) |
|---|---|
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` | “Pre-receipt controls run the C2 gate with its P10 (fresh probe re-run) leg disabled — that is the V8 fix, frozen here” |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` | “V7 lacks violating cases for `both-print` and `toolchain`; V8 finds the pre-receipt P10 execution” |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c3_verify.py` | “a leg that cannot run is a defect, never a pass” |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg_gate.py` | “("P9", c_clean_tree), ("P10", c_rerun)” |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/polyglot_c_py_probe.py` | “Before the stage-2 freeze only `--dry` and `--stage-check` are run” |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/order_check.py` | “FAIL  when the freeze commit (the first commit adding <claims>) already contains <receipt>” |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg-spec-r46.json` | “"receipt": "corpus/evidence/round46/polyglot-c-py-probe.txt"” |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/stage2_controls.py` (blob at `a543d92`) | “Each control runs on a fresh `git clone --shared` of the lane at REV” |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/control-c3-echo.txt` (blob at `a543d92`) | “gate: P10 DEFECT fresh probe output is not byte-equal to the receipt” |
| `file:///fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py` | “the gate's `P10` (fresh probe re-run) clause does not exist in the run” |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C2Echo.md` | “the required round-48 P10-disabled control execution is unverified and must be recorded after stage 2” |
| `file:///home/vgpnk/.omp/agent/RULES.md` | “never pipe an unverified remote script into a shell” |

## VERDICT

**PASS for this item, nothing admitted.** All three frozen C2 controls print `PREDICATE R48-C2 fail`, with `REV`-prefixed receipts, P10 disabled, and order pins proving no round-48 probe receipt exists:

```
control-r48-c2-base   REV 787691a96b41dc147d0c8f3fc518c1330f4bf8db  checks=16 defects=7  PREDICATE R48-C2 fail
control-r48-c2-filler REV ecf768d0dd364a5789816c93d7f4cb77090e7e0e  checks=11 defects=8  PREDICATE R48-C2 fail
control-r48-c2-echo   REV 4ffb15d00b2d5be3830446d8c35e4fdd18ae9b12  checks=16 defects=6  PREDICATE R48-C2 fail
```

A second, independently written counter agrees on all three. No scored counter or probe execution was made on the claimed work; no predicate, kill rule, control or literal was changed. Two findings are routed to the L1 for stage 2: the echo control is **accepted** by the package gate when P10 is disabled (it is caught by the counter's content legs, not the gate), and the frozen base's `both-print`/`toolchain` requirement rows are committed with the unparseable label `not exercised` — the exact V7 class that round-48 delta (a) is frozen to catch.

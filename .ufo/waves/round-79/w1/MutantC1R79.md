# MutantC1R79 — R79-C1 additional mutation probe

Freeze: `5d6843134017780c045e92eed4e83264188a7d47`. Axes: coverage (additional defect classes) and calibration (survivors retained rather than counted as kills).

## Result

**12 new mutations: 10 killed, 2 survived, 0 inconclusive.** These are additional to the counter’s six `MUTANTS` entries; the denominator attack changes n, not the existing off-by-one k attack. Every case ran the identical bounded CLI on pristine, mutated, and exactly restored bytes. All 12 pristine runs and all 12 restored runs exited 0 with identical output. No lane implementation was modified.

## Method

Committed inputs were fetched with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 5d6843134017780c045e92eed4e83264188a7d47:<path>`. The scratch fixture contained all 122 files the counter needs: counter, census, ledger, SKILL, 88 grader test bodies, and named receipts/instruments. Fixtures retained the freeze Git index and master ref, using the lane object database read-only as an alternate; this preserves actual tracking checks, unlike fixture_tree’s existence-only approximation. No counter module was imported. Mutation facts came from committed JSON/receipt/test bytes.

Four independent fixtures ran concurrently. Each subprocess had a 60-second timeout. Every case used:

```sh
python3 "$CASE/plans/round79_c1_population_ledger.py" --lane "$CASE" --work "$CASE/work" --quiet
```

`$CASE` was `/fast/scratch/hyaku/kengaku-r79/MutantC1R79/M01` through `M12`. The original extraction fixture was `.../aZNB`. No commit was created. Each original fixture file was restored in a finally block; introduced files were removed. Scratch is deleted after report persistence.

### Shared pristine/restored actual output (rc 0)

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECTS n=0
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 pass
```

## Mutation table

| ID | Mutation | Expected detector | Mutant rc | Observed defects | Verdict |
|---|---|---|---:|---|---|
| M01 | omit-one-class | PAIR-MISMATCH | 1 | PAIR-MISMATCH | killed |
| M02 | foreign-blocker-evidence | EVIDENCE-MISMATCH | 0 | none; DEFECTS n=0 | survived |
| M03 | unlocated-has-subject | UNLOCATED-SUBJECT-PRESENT | 1 | UNLOCATED-SUBJECT-PRESENT | killed |
| M04 | correct-k-wrong-n | CLASS-K-MISMATCH | 1 | CLASS-K-MISMATCH | killed |
| M05 | byte-identical-untracked-receipt | RECEIPT-UNTRACKED | 1 | RECEIPT-UNTRACKED | killed |
| M06 | duplicate-json-member | LEDGER-SHAPE | 0 | none; DEFECTS n=0 | survived |
| M07 | near-miss-member | MEMBER-UNACCOUNTED and MEMBER-EXTRA | 1 | MEMBER-EXTRA, MEMBER-UNACCOUNTED | killed |
| M08 | wrong-verdict | VERDICT-MISMATCH | 1 | VERDICT-MISMATCH | killed |
| M09 | wrong-subject-shape | SUBJECT-MISMATCH | 1 | SUBJECT-MISMATCH | killed |
| M10 | unlocated-debt-erased | DEBT-UNNAMED | 1 | DEBT-UNNAMED | killed |
| M11 | wrong-task-receipt-with-added-subject | RECEIPT-POPULATION | 1 | RECEIPT-POPULATION | killed |
| M12 | unlocated-wrong-round | ROUND-MISMATCH | 1 | ROUND-MISMATCH, UNLOCATED-RECEIPT-OUTSIDE-ROUND | killed |

## Survivors

### M02 — foreign blocker evidence accepted

`break-filter-js-from-html.evidence` was replaced verbatim with `filter-js-from-html.evidence`. The replacement is not present in the target grader after whitespace normalization (observed `False`), but both excerpts contain `selenium`, so the check at counter lines 305–307 accepts the foreign excerpt.

Original: `ys import tempfile from pathlib import Path from selenium import webdriver from selenium.common.exceptions`

Replacement: `b import Path from bs4 import BeautifulSoup from selenium import webdriver from selenium.common.exceptions`

Expected detector: `EVIDENCE-MISMATCH` for evidence borrowed from a different member (the assignment’s evidence-provenance attack). Observed: rc 0, `DEFECTS n=0`, `PREDICATE R79-C1 pass`. Calibration caveat: the frozen core blocker condition still holds, because the target’s own detector really fires; this establishes an evidence-provenance coverage gap, not a demonstrated false blocker classification. The frozen text does not explicitly require the entire evidence excerpt to occur in the grader; do not silently strengthen it.

### M06 — duplicate raw JSON member accepted

A second, byte-equivalent `build-pmars` member entry was inserted before the existing entry. Raw JSON therefore accounts for that member twice while Python json.loads silently collapses duplicate names. Expected rule: “every member accounted exactly once”; expected reporting point `LEDGER-SHAPE` (or a duplicate-member defect). Observed: rc 0, `LEDGER rows=88`, `DEFECTS n=0`. This is a duplicate-key ambiguity the gate does not detect, not a missing population member after JSON decoding. No contract or implementation was changed.

## Exact mutations, outputs, and hashes

Notation: `d` is a fresh JSON decode of the frozen ledger; `files` maps paths to frozen bytes; `ledger` is `plans/grader-population-ledger.json`. Unless `raw_ledger=True`, serialize d with `json.dumps(d, indent=1) + "\n"`. The raw duplicate-key case bypasses serialization. This formatting-only serialization also occurs in the other ledger cases; it does not alter decoded facts.

### M01 — omit-one-class

```python
d['members']['build-pmars']['classes'].remove('subprocess-exec')
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT PAIR-MISMATCH build-pmars ledger=['file-artifact'] census=['subprocess-exec', 'file-artifact']
DEFECTS n=1
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `d30c51815a088dbdf5ec443c09d854dab12f2cd2f113106f350489b1e0ef0ba4`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

### M02 — foreign-blocker-evidence

```python
d['members']['break-filter-js-from-html']['evidence']=d['members']['filter-js-from-html']['evidence']
```

Actual rc: pristine=0, mutant=0, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECTS n=0
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 pass
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `cbba26a3fddd29b54a33bf3c992e9fef44df28c9a6552294d98fe2179ae245b8`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

### M03 — unlocated-has-subject

```python
p=d['members']['cancel-async-tasks']['receipt']; files[p]+=b'\nTASK-UNDER-TEST cancel-async-tasks\n'
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT UNLOCATED-SUBJECT-PRESENT cancel-async-tasks corpus/evidence/round61/cancel-async-probe.txt
DEFECTS n=1
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `corpus/evidence/round61/cancel-async-probe.txt`
  - before: `3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a`
  - mutated: `d315c2ab165cea91880f3ac5a17f7010dae40b869a32af49a6bcb969af330a62`
  - restored: `3a69fddb8ab817bf78dad57b4d28e1c964b288c433901560fa98f59ff306922a`
- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `21053c83dbeb46a19690436b95a960fde90a156d46c122b73d11c7e7a26a5392`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

### M04 — correct-k-wrong-n

```python
files['SKILL.md']=files['SKILL.md'].replace(b'executed 10 of 45',b'executed 10 of 46',1)
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT CLASS-K-MISMATCH subprocess-exec cell=10 of 46 ledger=10 of 45
DEFECTS n=1
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `SKILL.md`
  - before: `f4f74deace12539de6aa378078a461c3cdc515e11a57896050d109f61288aaa8`
  - mutated: `8dad4fa31f3308bef0cc8201bb10bb982e1bb61110077a402f9334edaf468091`
  - restored: `f4f74deace12539de6aa378078a461c3cdc515e11a57896050d109f61288aaa8`
- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `21053c83dbeb46a19690436b95a960fde90a156d46c122b73d11c7e7a26a5392`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

### M05 — byte-identical-untracked-receipt

```python
r=d['members']['build-pmars']; p=r['receipt']; r['receipt']='corpus/evidence/round38/untracked-identical.txt'; files[r['receipt']]=files[p]
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT RECEIPT-UNTRACKED build-pmars corpus/evidence/round38/untracked-identical.txt
DEFECTS n=1
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `e5f1ecb8bb23f191595284140aefa03ca9c4c19336dfc108122ca5781f9f98dc`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
- `corpus/evidence/round38/untracked-identical.txt`
  - before: `None`
  - mutated: `2408b477b0299e1339064b4b3df968a00174b3a5999016073b5fe4fd8cbb4ef9`
  - restored: `None`

### M06 — duplicate-json-member

```python
raw=files[ledger].decode(); q=chr(34); row=json.dumps(d['members']['build-pmars']); key=q+'members'+q+': {'; files[ledger]=raw.replace(key,key+'\n'+q+'build-pmars'+q+': '+row+',',1).encode(); raw_ledger=True
```

Actual rc: pristine=0, mutant=0, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECTS n=0
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 pass
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `914f17b2c0fdbb0b64a3e739758ff4c0ff699ca9b72fc48ab0605acbcf134358`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

### M07 — near-miss-member

```python
d['members']['fix-gitt']=d['members'].pop('fix-git')
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT MEMBER-EXTRA fix-gitt
DEFECT MEMBER-UNACCOUNTED fix-git
DEFECTS n=2
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=63 unaccounted=1 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `3f49feb2142edd7b9f81d556ac2b465cf80b8f4b9088a95551b1ce8889eed406`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

### M08 — wrong-verdict

```python
d['members']['build-pmars']['verdict']='vectors'
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT VERDICT-MISMATCH build-pmars ledger=vectors receipt=cases
DEFECTS n=1
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `5ea9118cea4f7e6435ac814300dee0dddcb5cc6242082307f7ae4216612b9f88`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

### M09 — wrong-subject-shape

```python
d['members']['build-pmars']['subject']='task-under-test'
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT SUBJECT-MISMATCH build-pmars ledger=task-under-test receipt=tb2-header
DEFECTS n=1
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `73c0804f470dd5d9e8ba8e4dbe11c0ebb0b06732d127e9bf970e82f6b392f0b4`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

### M10 — unlocated-debt-erased

```python
d['members']['cancel-async-tasks']['debt']='none'
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT DEBT-UNNAMED cancel-async-tasks 'none'
DEFECTS n=1
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `912cbc89ace9c6e9f22859a6f378cefbb713ae7342db418e1a76bcce19d28ac9`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

### M11 — wrong-task-receipt-with-added-subject

```python
r=d['members']['build-pmars']; r['receipt']=d['members']['circuit-fibsqrt']['receipt']; files[r['receipt']]+=b'\nTASK-UNDER-TEST build-pmars\n'; r['subject']='task-under-test'
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT RECEIPT-POPULATION build-pmars corpus/evidence/round42/fibsqrt-probe.txt names 2 members
DEFECT RECEIPT-POPULATION circuit-fibsqrt corpus/evidence/round42/fibsqrt-probe.txt names 2 members
DEFECTS n=2
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `f055d3d41c1f15e4463bd475e1b1ccef307407d8f7354cea92df674eaa2a7b55`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
- `corpus/evidence/round42/fibsqrt-probe.txt`
  - before: `2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a`
  - mutated: `d85688e7593966a09c62c6a1d14eaa56acb0b311d51f02237281c882550e67b7`
  - restored: `2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a`

### M12 — unlocated-wrong-round

```python
d['members']['cancel-async-tasks']['round']=62
```

Actual rc: pristine=0, mutant=1, restored=0. All stderr empty.

```text
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT ROUND-MISMATCH cancel-async-tasks instrument=r61 ledger=r62
DEFECT UNLOCATED-RECEIPT-OUTSIDE-ROUND cancel-async-tasks corpus/evidence/round61/cancel-async-probe.txt
DEFECTS n=2
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
```

SHA-256 (absent means no file):

- `plans/grader-population-ledger.json`
  - before: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`
  - mutated: `13fe15637389de2d9ef0ca0b369247357a1262539cbd5a74c5d2f63eaf98f819`
  - restored: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`

## Restoration evidence

All 122 original input files were reread after restoration for every case. Aggregate SHA-256 before and after each of the 12 cases: `b959c6157acf55bb58a695f8174e7c3a4c7c9edea9990c9f2e06367f4faf93ec`.

Aggregate algorithm: iterate paths in sorted order; SHA-256 update with UTF-8 path, NUL byte, and the raw SHA-256 digest of its bytes. All 12 before/after aggregates matched; all restored outputs exactly matched their respective pristine outputs. The M05 introduced receipt was absent again after restoration.

Frozen ledger SHA-256: `d71fa08cc9b61501151ab9f4fe0f89fbc71fa0e0beeb2e00f78da1c0fcf8acc5`.
Frozen counter SHA-256: `648ff9fa786631203ee2c663a397c97252dc7c0e4f77c28e692dfe40e2aeb962`.

## Boundaries and tooling

No installs or upgrades. Used existing Python 3 and Git; no grader, browser, VM, or other domain runtime was invoked. Only the assigned report and owned scratch were written. No claim, control, kill rule, counter, or lane artifact was repaired.

## Self-evaluation

Accuracy 4/5: actual CLI outputs and hashes retained; M02 is explicitly distinguished from a false core blocker classification. Completeness 5/5: 12 new cases, survivor list, pristine/mutated/restored runs, and exact-byte restoration. Clarity 4/5: full transcripts make this longer than the result table. Actionability 4/5: exact mutations and CLI retained, but scratch is intentionally disposable. Conciseness 4/5: repeated output preserves evidence at the cost of length. Overall 4.2/5. Highest-impact next consideration is duplicate-key rejection if raw JSON uniqueness is intended; no repair is made here. The user should agree the evidence-provenance survivor has been qualified rather than overstated.

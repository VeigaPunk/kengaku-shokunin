# BatteriesR79 — C1BatteriesR79

Axes: coverage and calibration. Frozen predicates, targets, controls, and kill rules unchanged.

## Provenance and result

Source: shared clone of the lane, checked out detached at `5d6843134017780c045e92eed4e83264188a7d47`. Clone root equality was asserted before checkout. No counter was imported; all battery runs invoked the pinned executable as a subprocess. Independent manual mutation used a separate complete copy of that pinned tree (including Git metadata), not the battery mutation helpers.

All requested batteries reproduced. No implementation repair was made. All six primary invocations returned rc 0 with empty stderr; the independent mutation returned rc 1 with empty stderr. No tools installed or upgraded.

Scratch root (`S`): `/fast/scratch/hyaku/kengaku-r79/C1BatteriesR79`.

## Five requested tallies

1. `DEFECTS n=0`, rc 0.
2. `SELFTEST cases=13 red=12 failures=0`, rc 0.
3. `MUTANTS real=6 killed=6 survived=0`, rc 0.
4. All controls printed `target_reached=False`, rc 0 each:
   - namegrep: 102 defects = `RECEIPT-POPULATION` ×88 + `CLASS-K-MISMATCH` ×14.
   - default-reason: 7 defects = `REASON-UNDERSTATED` ×7.
   - all-blocked: 62 defects = `REASON-UNBACKED` ×62.
5. Independent drop-a-row: `DEFECTS n=1`; exact line `DEFECT MEMBER-UNACCOUNTED adaptive-rejection-sampler`; rc 1.

## Mutant table

| Mutant | Observed defect codes | Outcome |
|---|---|---|
| flip-executed-to-unattempted | CLASS-K-MISMATCH | killed |
| swap-blocker-reason | REASON-UNBACKED | killed |
| drop-a-row | MEMBER-UNACCOUNTED | killed |
| fake-executed-row | CLASS-K-MISMATCH,RECEIPT-POPULATION | killed |
| census-as-receipt | RECEIPT-POPULATION | killed |
| class-cell-off-by-one | CLASS-K-MISMATCH | killed |

## Exact primary command/output evidence

### quiet

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone/plans/round79_c1_population_ledger.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone --quiet
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=88 executed=18 unlocated=6 unexecuted=64
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECTS n=0
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=64 unaccounted=0 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 pass
rc=0
stderr=''
```

### selftest

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone/plans/round79_c1_population_ledger.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone --selftest --work /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/work
CASE clean expect=pass observed=- ok
CASE member-missing expect=MEMBER-UNACCOUNTED observed=CLASS-K-MISMATCH,MEMBER-UNACCOUNTED ok
CASE member-extra expect=MEMBER-EXTRA observed=MEMBER-EXTRA ok
CASE receipt-untracked expect=RECEIPT-UNTRACKED observed=RECEIPT-UNTRACKED ok
CASE receipt-no-obs expect=RECEIPT-NO-OBS observed=RECEIPT-NO-OBS ok
CASE subject-absent expect=SUBJECT-ABSENT observed=SUBJECT-ABSENT ok
CASE receipt-population expect=RECEIPT-POPULATION observed=RECEIPT-POPULATION ok
CASE reason-unbacked expect=REASON-UNBACKED observed=REASON-UNBACKED ok
CASE reason-understated expect=REASON-UNDERSTATED observed=REASON-UNDERSTATED ok
CASE unlocated-subject-present expect=UNLOCATED-SUBJECT-PRESENT observed=UNLOCATED-SUBJECT-PRESENT ok
CASE class-k-mismatch expect=CLASS-K-MISMATCH observed=CLASS-K-MISMATCH ok
CASE class-row-unquantified expect=CLASS-ROW-UNQUANTIFIED observed=CLASS-ROW-UNQUANTIFIED ok
CASE pair-mismatch expect=PAIR-MISMATCH observed=PAIR-MISMATCH ok
SELFTEST cases=13 red=12 failures=0
rc=0
stderr=''
```

### mutants

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone/plans/round79_c1_population_ledger.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone --mutants --work /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/work
MUTANT flip-executed-to-unattempted expect=CLASS-K-MISMATCH observed=CLASS-K-MISMATCH killed
MUTANT swap-blocker-reason expect=REASON-UNBACKED observed=REASON-UNBACKED killed
MUTANT drop-a-row expect=MEMBER-UNACCOUNTED observed=MEMBER-UNACCOUNTED killed
MUTANT fake-executed-row expect=RECEIPT-POPULATION|SUBJECT-ABSENT|RECEIPT-NO-OBS|RECEIPT-UNTRACKED observed=CLASS-K-MISMATCH,RECEIPT-POPULATION killed
MUTANT census-as-receipt expect=RECEIPT-POPULATION observed=RECEIPT-POPULATION killed
MUTANT class-cell-off-by-one expect=CLASS-K-MISMATCH observed=CLASS-K-MISMATCH killed
MUTANTS real=6 killed=6 survived=0
rc=0
stderr=''
```

### namegrep

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone/plans/round79_c1_population_ledger.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone --control-namegrep --work /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/work
CONTROL namegrep executed=88 unexecuted=0 defects=102 codes=CLASS-K-MISMATCH,RECEIPT-POPULATION
CONTROL namegrep target_reached=False
rc=0
stderr=''
```

### default-reason

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone/plans/round79_c1_population_ledger.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone --control-default-reason --work /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/work
CONTROL default-reason executed=18 unexecuted=64 defects=7 codes=REASON-UNDERSTATED
CONTROL default-reason target_reached=False
rc=0
stderr=''
```

### all-blocked

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone/plans/round79_c1_population_ledger.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone --control-all-blocked --work /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/work
CONTROL all-blocked executed=18 unexecuted=64 defects=62 codes=REASON-UNBACKED
CONTROL all-blocked target_reached=False
rc=0
stderr=''
```

## Independent hand recreation

Copied the complete pinned clone to `$S/manual` with `shutil.copytree`, without invoking/importing counter helpers. Used a surgical file edit to delete original lines 4–14 of `manual/plans/grader-population-ledger.json`: the entire `adaptive-rejection-sampler` member entry, including its trailing comma. This is the battery's `drop-a-row` mutation independently recreated; no other member or class cell changed. Ran the original, unmodified pinned executable over this copy:

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone/plans/round79_c1_population_ledger.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/manual --quiet --work /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/work
UNIVERSE classes=16 members=88 pairs=230 census_executed=17 census_covered=12
LEDGER rows=87 executed=18 unlocated=6 unexecuted=63
COVERAGE replayed=24 covered=15 uncovered=container-image census_covered=12
DEFECT MEMBER-UNACCOUNTED adaptive-rejection-sampler
DEFECTS n=1
TARGET classes=16 members=88 pairs=230 replayed=24 located=18 unlocated=6 unexecuted=63 unaccounted=1 unbacked=0 understated=0 covered=15
PREDICATE R79-C1 fail
rc=1
stderr=''
```

## Control per-code counts

Primary control output reports totals and unique codes, not multiplicities. To expose multiplicities, copied the pinned executable to `$S/control-detail.py` and added only these output statements immediately after its existing control defect collection (original line 695):

```python
    for code in sorted({code for code, _ in defects}):
        print(f"CONTROL-DETAIL {kind} code={code} count={sum(1 for actual, _ in defects if actual == code)}")
```

No predicate, fixture, mutation, or control generation logic changed. This supplementary output instrumentation is distinct from the unmodified primary batteries above and does not import the counter to derive facts.

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/control-detail.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone --control-namegrep --work /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/detail-work
CONTROL-DETAIL namegrep code=CLASS-K-MISMATCH count=14
CONTROL-DETAIL namegrep code=RECEIPT-POPULATION count=88
CONTROL namegrep executed=88 unexecuted=0 defects=102 codes=CLASS-K-MISMATCH,RECEIPT-POPULATION
CONTROL namegrep target_reached=False
rc=0
stderr=''
```

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/control-detail.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone --control-default-reason --work /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/detail-work
CONTROL-DETAIL default-reason code=REASON-UNDERSTATED count=7
CONTROL default-reason executed=18 unexecuted=64 defects=7 codes=REASON-UNDERSTATED
CONTROL default-reason target_reached=False
rc=0
stderr=''
```

```text
$ python3 /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/control-detail.py --lane /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/clone --control-all-blocked --work /fast/scratch/hyaku/kengaku-r79/C1BatteriesR79/detail-work
CONTROL-DETAIL all-blocked code=REASON-UNBACKED count=62
CONTROL all-blocked executed=18 unexecuted=64 defects=62 codes=REASON-UNBACKED
CONTROL all-blocked target_reached=False
rc=0
stderr=''
```

## Scope, risks, and blockers

- Only permanent file written: this report. All copies and diagnostic edits were under the seat scratch root; scratch is removed before yield.
- Baseline used the exact requested `--quiet` command without `--work`. The pinned CLI unconditionally calls `mkdir(exist_ok=True)` on its default `/fast/scratch/hyaku/kengaku-r79/counter` work path even in read-only measurement mode (lines 720–721). Whether that directory preexisted was not observed. No fixture operations were requested there; every subsequent invocation explicitly used seat-owned scratch work paths.
- No failing battery, surviving mutant, target-reaching control, or missing prerequisite observed. The aggregate battery's printed `red=12` is retained verbatim, not independently reinterpreted.
- No supported LSP tool was exposed; no symbol refactor was needed. No lane implementation, global configuration, credentials, or external substrate was edited.
- These results are scoped to the freeze revision, not any later lane tip. No additional build/lint/format suite was run.

## Deliverable self-check

Accuracy 5: raw outputs and return codes retained. Completeness 5: all five items, six mutant outcomes, three per-code control counts, and the manual kill retained. Clarity 4: long command paths make the evidence verbose; the five-tally summary precedes it. Actionability 5: the pinned revision, commands, edit range, and exact defect are reproducible. Conciseness 4: raw and summary evidence intentionally repeat; retaining both satisfies the verbatim evidence request. Overall 4.6/5. Highest-impact improvement would be a shorter command-prefix convention, omitted here to preserve directly executable commands. User agreement is expected on coverage; verbosity preference remains subjective.

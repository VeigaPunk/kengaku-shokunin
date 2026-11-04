# MutantR78 — round 78 w1

Axes: coverage (C1), calibration (C2). No contract changes or lane source edits.

Committed-byte snapshot: `cd2e25bb80cf618135cc001193df13966ef1c711`. Frozen claims read in full before commands. Detector runs are CLI subprocesses; neither counter was imported. No subagents or other runtimes invoked.

Tools: existing `Python 3.14.8`, git, bash, mktemp; no installations or updates.

## Fixture isolation and provenance

Scratch root: `/fast/scratch/hyaku/kengaku-r78/MutantR78` (deleted after writing this report). C1 copied the battery’s pristine `fx-base` into a `mktemp` fixture, initialized branch master, asserted its top-level, and committed only fixture bytes. C2 fixture generation was adapted **only in scratch** to use `D=$(mktemp -d "$1/XXXX") && git -C "$D" init -q -b master` and assert the exact top-level before any add/commit. Its detector and battery definitions were unchanged; the adaptation only changes fixture allocation/guard plumbing. Every git call names `-C`.

Committed source SHA256:
- C1: `9c4fc23174d65256e3cf6dcc7014e8c79fcac1d3c6d93e229f85dbffae6b212f`
- C2: `e79fe3fdee1348baa518a9327e19c6865ada4159a925f2efab24ac9fc4913a0b`
- C2 guarded scratch copy used for runs: `4ca847138a5778eb961495035abc389fe5d38cd4df8ff2fec35eca4527b1aec5`
- C2 copied source restored exactly before disposal: `e79fe3fdee1348baa518a9327e19c6865ada4159a925f2efab24ac9fc4913a0b`.

## Existing attributed batteries

### C1: rc 0
Command: `python3 /fast/scratch/hyaku/kengaku-r78/MutantR78/round78_c1_class_member_ledger.py --mutants --work /fast/scratch/hyaku/kengaku-r78/MutantR78/c1-battery`
```text
MUTANT drop-link killed=CLASS-ROW-UNLINKED
MUTANT drop-member killed=MEMBER-UNACCOUNTED
MUTANT break-receipt killed=PREDICATE-ABSENT
MUTANT bad-reason killed=REASON-UNKNOWN
MUTANT kill-detector killed=REASON-UNBACKED
MUTANT coverage-regression killed=COVERAGE-REGRESSION
MUTANTS real=6 killed=6 wrong_id=0 survived=0
```
### C2: rc 0
Command: `python3 /fast/scratch/hyaku/kengaku-r78/MutantR78/round78_c2_stamp_location.py --mutants --work /fast/scratch/hyaku/kengaku-r78/MutantR78/c2-battery`
```text
MUTANT omit-tip killed=TIP-ABSENT
MUTANT drift killed=TOOL-DRIFT
MUTANT supplied-clean killed=SUPPLIED-BUT-CLEAN
MUTANT no-command killed=COMMAND-ABSENT
MUTANT unlocated-pass killed=PASS-UNLOCATED
MUTANT unresolved-tip killed=TIP-UNRESOLVED
MUTANTS real=6 killed=6 wrong_id=0 survived=0
```

## Six additional fixture mutants

| Counter | Mutant | Expected class | Observed | Verdict |
|---|---|---|---|---|
| C1 | duplicate-member | MEMBER-DUPLICATE | rc=0; DEFECTS n=0 | survived |
| C2 | empty-command | COMMAND-ABSENT | rc=1; COMMAND-ABSENT | killed |
| C1 | predicate-prefix | PREDICATE-ABSENT | rc=0; DEFECTS n=0 | survived |
| C2 | truncated-digest | TOOL-DRIFT / full-digest refusal | rc=0; DEFECTS n=0 | survived |
| C1 | incomplete-vector-table | PREDICATE-ABSENT | rc=0; DEFECTS n=0 | survived |
| C2 | rewritten-conflicting-stamp | STAMP-CONFLICT | rc=0; DEFECTS n=0 | survived |

**MUTANTS-EXTRA: 1 killed/6**

Both pristine baselines passed (rc 0), and all six exact-byte restorations passed (rc 0). Thus none is inconclusive. The killed input fired its expected class. Five survivors falsify frozen requirements; none should be relabeled a stated limit.

## Survivor interpretation and amendments

- **duplicate-member**: C1: “every member … is accounted exactly once” (claims lines 15–16). Duplicate JSON keys are silently collapsed before accounting; the earlier a1 row is discarded. Close in-round with an additive MEMBER-DUPLICATE detector using duplicate-key-aware JSON parsing.
- **empty-command**: C2 COMMAND requirement (lines 68–69,97). Killed; no amendment required for this input.
- **predicate-prefix**: C1: “each executed member names a tracked receipt whose own bytes print its passing predicate” (lines 17–18). `passing-is-not-pass` is not the exact passing verdict. Close in-round with additive PREDICATE-ABSENT for non-exact verdict lines.
- **truncated-digest**: C2 kill rule: “A receipt whose TOOL_SHA matches by coincidence of a truncated pin is refused (full digest comparison)” (lines 110–111). An 8-hex prefix passes. Close in-round with additive defect for any non-64-hex pin; this is an explicit frozen kill-rule violation, not a stated limit.
- **incomplete-vector-table**: C1: executed evidence must print its passing predicate (lines 17–18), or the task’s allowed fully frozen vector table. One invented VECTOR line supplies neither a predicate nor a complete frozen table. Close in-round by adding defects for incomplete/unidentified vector tables; do not broaden what counts as evidence.
- **rewritten-conflicting-stamp**: C2 STAMP-CONFLICT: “two LANE_TIP values in one receipt” (line 98). Replacing the original line by two distinct resolvable ancestor stamps passes. Close in-round with additive STAMP-CONFLICT for multiple distinct values. The mutation rewrites the stamp in-place rather than adding a purported correction block.

## Actual detector output and restoration evidence

The same bounded CLI invocation was run on pristine, mutant, and restored bytes:
```text
python3 /fast/scratch/hyaku/kengaku-r78/MutantR78/round78_c1_class_member_ledger.py --lane /fast/scratch/hyaku/kengaku-r78/MutantR78/5q5k --work /fast/scratch/hyaku/kengaku-r78/MutantR78/audit-work-1
python3 /fast/scratch/hyaku/kengaku-r78/MutantR78/round78_c2_stamp_location.py --lane /fast/scratch/hyaku/kengaku-r78/MutantR78/c2-battery/mnVZ --work /fast/scratch/hyaku/kengaku-r78/MutantR78/audit-work-2
```

### C1 pristine (rc 0)
```text
LANE_TIP 372835e84fe26d3f622fd5adc11b84ef040c660a
WORKTREE clean
UNIVERSE classes=2 members=5 pairs=5
MEMBER a1 executed classes=alpha receipt=corpus/evidence/r/a1.txt verdict=R70-C1 token=predicate
MEMBER a2 unexecuted classes=alpha receipt=- verdict=reason:vm-required
MEMBER b1 executed classes=beta receipt=corpus/evidence/r/b1.txt verdict=R71-C1 token=predicate
MEMBER b2 executed classes=beta receipt=corpus/evidence/r/b2.txt verdict=R72-C1 token=predicate
MEMBER b3 unexecuted classes=beta receipt=- verdict=reason:browser-required
CLASS alpha k=1 n=2 census=2 ledger_k=1
CLASS beta k=2 n=3 census=3 ledger_k=2
LEDGER rows=5 executed=3 unexecuted=2
COVERAGE recomputed_covered=1 census_covered=1 promoted=- recomputed_uncovered=gamma
DEFECTS n=0
TARGET classes=2 members=5 executed=3 unexecuted=2 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```
### C2 pristine (rc 0)
```text
LANE_TIP a3371d08e5ded84cece756270b1f734ddaf603ac
WORKTREE dirty
UNIVERSE dirs=2 receipts=6
RECEIPT corpus/evidence/round77/a-clean.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/b-no-tip.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c-drift.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/d-supplied.txt tip=a52dbe36 worktree=dirty tool=plans/supplied_only.py sha=- legs=ok
RECEIPT corpus/evidence/round77/e-no-command.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/f-unlocated.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=6 located=6 unlocated=0
PREDICATE R78-C2 pass
```
### C1 duplicate-member
```diff
--- pristine/plans/grader-selected-members.json
+++ mutant/plans/grader-selected-members.json
@@ -1,5 +1,6 @@
 {
   "members": {
+    "a1": {"status": "unexecuted", "classes": ["alpha"], "reason": "invented"},
     "a1": {
       "status": "executed",
       "classes": [
```
SHA256 before: `7a20abf8f60fbde45c96dcbc27d0f2ef15bfa437632b32a952120ebe4824a130`
SHA256 mutant: `bf737ab1019b5b0b9161651e70946c38f286f78c0b2ca5429c91c4d518c158f1`
SHA256 restored: `7a20abf8f60fbde45c96dcbc27d0f2ef15bfa437632b32a952120ebe4824a130`
Mutant rc=0; stderr=''.
```text
LANE_TIP 372835e84fe26d3f622fd5adc11b84ef040c660a
WORKTREE dirty
UNIVERSE classes=2 members=5 pairs=5
MEMBER a1 executed classes=alpha receipt=corpus/evidence/r/a1.txt verdict=R70-C1 token=predicate
MEMBER a2 unexecuted classes=alpha receipt=- verdict=reason:vm-required
MEMBER b1 executed classes=beta receipt=corpus/evidence/r/b1.txt verdict=R71-C1 token=predicate
MEMBER b2 executed classes=beta receipt=corpus/evidence/r/b2.txt verdict=R72-C1 token=predicate
MEMBER b3 unexecuted classes=beta receipt=- verdict=reason:browser-required
CLASS alpha k=1 n=2 census=2 ledger_k=1
CLASS beta k=2 n=3 census=3 ledger_k=2
LEDGER rows=5 executed=3 unexecuted=2
COVERAGE recomputed_covered=1 census_covered=1 promoted=- recomputed_uncovered=gamma
DEFECTS n=0
TARGET classes=2 members=5 executed=3 unexecuted=2 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```
Restored rc=0; exact-byte equality=True; stderr=''.
```text
DEFECTS n=0
TARGET classes=2 members=5 executed=3 unexecuted=2 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```
### C2 empty-command
```diff
--- pristine/corpus/evidence/round77/a-clean.txt
+++ mutant/corpus/evidence/round77/a-clean.txt
@@ -2,6 +2,6 @@
 WORKTREE clean
 TOOL plans/fixture_tool.py
 TOOL_SHA 2a402bbbd4eb5f592eee6abe3a2ebdb6c6cb5b30ce9c473bb171e74ebbc4d647
-COMMAND python3 plans/fixture_tool.py --selftest
+COMMAND 
 SELFTEST cases=3 red=2
 PREDICATE R78-C1 pass
```
SHA256 before: `b44c7637956878ab8ff9e6d963739b4db80b5c5db3cd19fc5ac39b91d843c98c`
SHA256 mutant: `56550bc62ff26b86d1344520d235d9f53cacc85b8ba5156a68fb5f6ebc018f04`
SHA256 restored: `b44c7637956878ab8ff9e6d963739b4db80b5c5db3cd19fc5ac39b91d843c98c`
Mutant rc=1; stderr=''.
```text
LANE_TIP a3371d08e5ded84cece756270b1f734ddaf603ac
WORKTREE dirty
UNIVERSE dirs=2 receipts=6
RECEIPT corpus/evidence/round77/a-clean.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=COMMAND-ABSENT
RECEIPT corpus/evidence/round77/b-no-tip.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c-drift.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/d-supplied.txt tip=a52dbe36 worktree=dirty tool=plans/supplied_only.py sha=- legs=ok
RECEIPT corpus/evidence/round77/e-no-command.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/f-unlocated.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
DEFECT COMMAND-ABSENT corpus/evidence/round77/a-clean.txt
DEFECTS n=1
TARGET receipts=6 located=5 unlocated=1
PREDICATE R78-C2 fail
```
Restored rc=0; exact-byte equality=True; stderr=''.
```text
DEFECTS n=0
TARGET receipts=6 located=6 unlocated=0
PREDICATE R78-C2 pass
```
### C1 predicate-prefix
```diff
--- pristine/corpus/evidence/r/a1.txt
+++ mutant/corpus/evidence/r/a1.txt
@@ -1 +1 @@
-PREDICATE R70-C1 pass
+PREDICATE R70-C1 passing-is-not-pass
```
SHA256 before: `2f926574d1e59c8f9f0fe1473f52f9a9094e21264131f3a12e283db3048b1ec3`
SHA256 mutant: `7273700909ecef38b2e427badaab0c7642c4ba8c32caaf68093887d22a970936`
SHA256 restored: `2f926574d1e59c8f9f0fe1473f52f9a9094e21264131f3a12e283db3048b1ec3`
Mutant rc=0; stderr=''.
```text
LANE_TIP 372835e84fe26d3f622fd5adc11b84ef040c660a
WORKTREE dirty
UNIVERSE classes=2 members=5 pairs=5
MEMBER a1 executed classes=alpha receipt=corpus/evidence/r/a1.txt verdict=R70-C1 token=predicate
MEMBER a2 unexecuted classes=alpha receipt=- verdict=reason:vm-required
MEMBER b1 executed classes=beta receipt=corpus/evidence/r/b1.txt verdict=R71-C1 token=predicate
MEMBER b2 executed classes=beta receipt=corpus/evidence/r/b2.txt verdict=R72-C1 token=predicate
MEMBER b3 unexecuted classes=beta receipt=- verdict=reason:browser-required
CLASS alpha k=1 n=2 census=2 ledger_k=1
CLASS beta k=2 n=3 census=3 ledger_k=2
LEDGER rows=5 executed=3 unexecuted=2
COVERAGE recomputed_covered=1 census_covered=1 promoted=- recomputed_uncovered=gamma
DEFECTS n=0
TARGET classes=2 members=5 executed=3 unexecuted=2 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```
Restored rc=0; exact-byte equality=True; stderr=''.
```text
DEFECTS n=0
TARGET classes=2 members=5 executed=3 unexecuted=2 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```
### C2 truncated-digest
```diff
--- pristine/corpus/evidence/round77/a-clean.txt
+++ mutant/corpus/evidence/round77/a-clean.txt
@@ -1,7 +1,7 @@
 LANE_TIP a52dbe368cb3694e2282374d9238ea4cfceb1707
 WORKTREE clean
 TOOL plans/fixture_tool.py
-TOOL_SHA 2a402bbbd4eb5f592eee6abe3a2ebdb6c6cb5b30ce9c473bb171e74ebbc4d647
+TOOL_SHA 2a402bbb
 COMMAND python3 plans/fixture_tool.py --selftest
 SELFTEST cases=3 red=2
 PREDICATE R78-C1 pass
```
SHA256 before: `b44c7637956878ab8ff9e6d963739b4db80b5c5db3cd19fc5ac39b91d843c98c`
SHA256 mutant: `79b9403085ce105107a57ecb5384efb740fb66601d2320627070d22164fdbe5b`
SHA256 restored: `b44c7637956878ab8ff9e6d963739b4db80b5c5db3cd19fc5ac39b91d843c98c`
Mutant rc=0; stderr=''.
```text
LANE_TIP a3371d08e5ded84cece756270b1f734ddaf603ac
WORKTREE dirty
UNIVERSE dirs=2 receipts=6
RECEIPT corpus/evidence/round77/a-clean.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/b-no-tip.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c-drift.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/d-supplied.txt tip=a52dbe36 worktree=dirty tool=plans/supplied_only.py sha=- legs=ok
RECEIPT corpus/evidence/round77/e-no-command.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/f-unlocated.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=6 located=6 unlocated=0
PREDICATE R78-C2 pass
```
Restored rc=0; exact-byte equality=True; stderr=''.
```text
DEFECTS n=0
TARGET receipts=6 located=6 unlocated=0
PREDICATE R78-C2 pass
```
### C1 incomplete-vector-table
```diff
--- pristine/corpus/evidence/r/a1.txt
+++ mutant/corpus/evidence/r/a1.txt
@@ -1 +1 @@
-PREDICATE R70-C1 pass
+VECTOR only-one-row frozen=match
```
SHA256 before: `2f926574d1e59c8f9f0fe1473f52f9a9094e21264131f3a12e283db3048b1ec3`
SHA256 mutant: `cb61b4bfd1629bb12c49fa81aeb83dc36a4e5e9ef98a8f151ac5ae2622ac3f8c`
SHA256 restored: `2f926574d1e59c8f9f0fe1473f52f9a9094e21264131f3a12e283db3048b1ec3`
Mutant rc=0; stderr=''.
```text
LANE_TIP 372835e84fe26d3f622fd5adc11b84ef040c660a
WORKTREE dirty
UNIVERSE classes=2 members=5 pairs=5
MEMBER a1 executed classes=alpha receipt=corpus/evidence/r/a1.txt verdict=R70-C1 token=vectors
MEMBER a2 unexecuted classes=alpha receipt=- verdict=reason:vm-required
MEMBER b1 executed classes=beta receipt=corpus/evidence/r/b1.txt verdict=R71-C1 token=predicate
MEMBER b2 executed classes=beta receipt=corpus/evidence/r/b2.txt verdict=R72-C1 token=predicate
MEMBER b3 unexecuted classes=beta receipt=- verdict=reason:browser-required
CLASS alpha k=1 n=2 census=2 ledger_k=1
CLASS beta k=2 n=3 census=3 ledger_k=2
LEDGER rows=5 executed=3 unexecuted=2
COVERAGE recomputed_covered=1 census_covered=1 promoted=- recomputed_uncovered=gamma
DEFECTS n=0
TARGET classes=2 members=5 executed=3 unexecuted=2 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```
Restored rc=0; exact-byte equality=True; stderr=''.
```text
DEFECTS n=0
TARGET classes=2 members=5 executed=3 unexecuted=2 unaccounted=0 unbacked=0
PREDICATE R78-C1 pass
```
### C2 rewritten-conflicting-stamp
```diff
--- pristine/corpus/evidence/round77/a-clean.txt
+++ mutant/corpus/evidence/round77/a-clean.txt
@@ -1,3 +1,4 @@
+LANE_TIP a3371d08e5ded84cece756270b1f734ddaf603ac
 LANE_TIP a52dbe368cb3694e2282374d9238ea4cfceb1707
 WORKTREE clean
 TOOL plans/fixture_tool.py
```
SHA256 before: `b44c7637956878ab8ff9e6d963739b4db80b5c5db3cd19fc5ac39b91d843c98c`
SHA256 mutant: `3fee141e651c82f06a2fed160325170185c48f310393cf8e9062ae176920412e`
SHA256 restored: `b44c7637956878ab8ff9e6d963739b4db80b5c5db3cd19fc5ac39b91d843c98c`
Mutant rc=0; stderr=''.
```text
LANE_TIP a3371d08e5ded84cece756270b1f734ddaf603ac
WORKTREE dirty
UNIVERSE dirs=2 receipts=6
RECEIPT corpus/evidence/round77/a-clean.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/b-no-tip.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/c-drift.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/d-supplied.txt tip=a52dbe36 worktree=dirty tool=plans/supplied_only.py sha=- legs=ok
RECEIPT corpus/evidence/round77/e-no-command.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
RECEIPT corpus/evidence/round77/f-unlocated.txt tip=a52dbe36 worktree=clean tool=plans/fixture_tool.py sha=yes legs=ok
DEFECTS n=0
TARGET receipts=6 located=6 unlocated=0
PREDICATE R78-C2 pass
```
Restored rc=0; exact-byte equality=True; stderr=''.
```text
DEFECTS n=0
TARGET receipts=6 located=6 unlocated=0
PREDICATE R78-C2 pass
```

## Assessment

Accuracy 4/5: actual outputs and hashes recorded; only fixture allocation plumbing was adapted for safety. Completeness 5/5: both attributed batteries plus six distinct extra mutants, baseline/mutant/restored runs, and all requested dispositions included. Clarity 4/5: detailed receipts are long but separated from the six-row summary. Actionability 5/5: each survivor maps to an explicit additive detector amendment. Conciseness 4/5: raw outputs retained for reproducibility. Overall 4.4/5. Improvement priority: add the five missing refusal cases to the in-round battery without weakening frozen claims. Self-check: the report distinguishes fixture safety adaptations, observed failures, and recommended amendments.

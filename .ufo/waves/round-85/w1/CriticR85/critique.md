# CriticR85 — adversarial review of frozen R85-C1 and R85-C2

Axes: coverage, calibration. This is a leaf review, not an admission or canonical judgment. No production files were edited, no subagents were dispatched, no network was used, and no tools were installed.

## Scope and revision authority

Read the entire frozen claims document first, then the case table, defect list, all three instruments, the captured subject, QUALITY Q1–Q24/Q60/Q61, the round-84 outside routed-defect definitions and relevant round-85 lesson/checker sections. Frozen claims revision: `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`; BASE: `0de45354d7aff18e4a23a348ec13de3a1f707a44`.

The lane advanced repeatedly during review. Final pinned measurement was `def5d0ea5fbf49389400663d30c5a2c8820e56a5`. Earlier measurements explicitly named below belong to their named revisions, not an unspecified final state. Counter scripts were executed from archived commit trees against explicit revision arguments where supported. Transient failures while the working-copy counter and master changed concurrently are NOT counted as findings.

The frozen claims file remained unchanged in the observed freeze-to-tip diff. No frozen predicate, target, case table, control set, kill rule or defect list was edited by this seat. Corrections below are recommendations to L1, not applied changes.

## Observed results

At `def5d0ea`:

```
C1 target:
TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0
PREDICATE R85-C1 pass

C1 mutants:
MUTANT no-ledger fixture=ledger-bad unmutated_defect=True mutant_reaches_target=False
MUTANTS real=5 necessary=4 redundant=1

C1 selftest:
SELFTEST cases=10 red=10 failures=0

C2 target:
CHECK v3 ok code-leg=True behavioural=True rc=0
TARGET ids=8 closed=8 checks_passed=8 indexed=yes defects=0
PREDICATE R85-C2 pass

C2 sensitivity:
SENSITIVITY n=8 failed_at_base=8

C2 default invocation, without --rev:
CHECK v1 DEFECT missing=<all four R84 paths>
TARGET ids=8 closed=7 checks_passed=7 indexed=yes defects=1
PREDICATE R85-C2 fail
```

At `b1e57097`, C1 against BASE returned exit 1, cases/legs/located/executed all zero, eight named defects. Its four frozen controls each returned `target_reached=False`: do-nothing; ledger-only; fabricated observations (`VECTOR-MISMATCH,REPRODUCE-MISMATCH`); forged receipt (`REPRODUCE-MISMATCH` alone). C2 target and sensitivity also passed there. C2 selftest gave `cases=6 red=6 failures=0`, its mutants gave `real=3 necessary=3 redundant=0`, and its presence-only-Q61 control remained red.

Additional isolated attacks: changing only a case-table `why` field caused `RECEIPT-TABLE-SHA` plus `REPRODUCE-MISMATCH rc=2`; removing the defects input caused `DEFECT SETUP frozen-input-missing`, exit 2. Those attacks did not turn the target green.

## Findings (11)

### F1 — MAJOR: the C1 mutant battery is red after the ledger-verdict change

Counterexample: at `def5d0ea`, `--mutants` reports only four necessary mutants of five; the `no-ledger` mutant cannot reach target. The function returns exit 1 when `necessary != len(MUTANTS)`.

Evidence: commit `35b1e4e0` changed both the real ledger verdict and `check()`'s required value from `predicate` to `cases`, but `flip_ledger()` still writes `verdict="predicate"`. Thus the ledger-bad fixture retains an unrelated `LEDGER-VERDICT` failure after disabling the status check. The ledger-only control also now has two defects, `LEDGER-VERDICT,RECEIPT-MISSING`, rather than only missing receipt.

Causality experiment: changing ONLY the scratch counter copy's `flip_ledger()` value to `cases` yielded all five `mutant_reaches_target=True`, `MUTANTS real=5 necessary=5 redundant=0`. Production remained untouched.

Impact: coverage control evidence and calibration of the C1 counter; Q22 requires current-tip re-derivation, not an older green mutant receipt. This is a fixable fixture defect, not grounds to declare the replay itself unexecuted. Smallest safe correction: update the fixture helper to the current ledger schema and rerun the frozen mutant battery, retaining the losing receipt. Falsifier: the pinned counter writes `cases` in its helper, or its unmodified battery demonstrates five necessary mutants.

### F2 — MAJOR: false class denominator, false before/after, and contradictory authorities

Counterexample: the ledger at BASE contains TEN `serialization-schema` members, including already-executed `db-wal-recovery` (round 40, receipt `corpus/evidence/round40/db-wal-probe.txt`). BASE is 1/10 executed; the measured round-85 tree is 2/10. The global 28→29 / 60→59 counts are correct.

Evidence: `corpus/evidence/round62/class-survey.txt` says `CLASS serialization-schema count=10`, listing both members. Reading the ledger at BASE, freeze, receipt commit and master produced respectively 1/10, 1/10, 2/10, 2/10. SKILL's updated class row explicitly says `executed 2 of 10 (round 85 adds sqlite-db-truncate to round 40's db-wal-recovery)`.

Yet the frozen heading says first `serialization-schema` member, and both frozen claims and `corpus/lessons/round-85.md` say 0/9→1/9. The lesson and SKILL therefore disagree in the same tree. The narrow member-level predicate remains true: sqlite-db-truncate itself was base-unexecuted. Calling it a new class or a first executed class member is not supported.

Impact: coverage sizing, Q10's exact-number requirement, R12's current-state authority, and append-only correction discipline (Q6/R1/Q60). Smallest safe correction: append a dated recomputation/corrigendum in the lesson/report: class 1/10→2/10; preserve frozen text and explicitly supersede its mistaken cells. Falsifier: an explicit frozen population exclusion that removes db-wal-recovery and another member from this class; none was located.

### F3 — MAJOR: the score leg does not observe the grader's internal score; int/float discrimination is overstated

Counterexample: a scratch subject variant tags `(word,value,type(value).__name__)` in the grader's two tuple sets, so integer values no longer match the solution's floats. Using the probe's actual HARNESS with only filesystem-path substitutions, this wrong-typing grader produced the ENTIRE frozen vector unchanged:

```
exact8 8/P; seven 7/P; six 6/F; empty 0/F;
extras 8/P; duplicates 8/P; string-values 0/F; int-values 6/F
```

The harness still reports six matches for int-values because it independently recomputes ordinary Python set equality. The strict-typing grader internally has zero matches and returns F. Both internal 0/F and 6/F are observed as harness-score 6/F. The original subject also reproduced every frozen vector in this experiment. A separate `>= 6` threshold mutant changed six and int-values to 6/P and WAS detected: the threshold leg is genuinely useful.

The same limitation applies analytically to the duplicates claim: a row-counting score of 16 still passes `>6`, while the separate harness reports eight; duplicates alone cannot distinguish those internal scores. This latter alternative is an inference, not a claimed executed row-counting mutation. The tested Counter-intersection variant also survived, but its min-count intersection does NOT establish a score-16 counterexample.

Impact: coverage evidence sizing. `duplicates=8` and `int-values=6` are correct predictions under the shipped source's Python set semantics. What is false is that the replay independently distinguishes every claimed semantic alternative. `legs=16` is also assigned as `2*len(cases)`, not sixteen independent observations. The verdict leg is not wholly vacuous: it observes the real test and detects threshold disagreement. Smallest safe correction: append a limitation to the lesson/report; do not retune the frozen table. A future prospective experiment can observe grader-internal score or choose an int-heavy case crossing the verdict boundary. Falsifier: show that this frozen vector rejects the demonstrated strict-type subject under its unchanged harness measurement, apart from rejecting its deliberately changed subject digest (which proves byte identity, not case discrimination).

### F4 — MAJOR: optional --rev is effectively required by C2

Counterexample: the documented default `round85_c2_debt.py --lane <lane> --work <scratch>` reports closed=7/defects=1, whereas the explicit `--rev def5d0ea...` form passes.

Evidence: default main constructs `Tree(lane,"worktree","worktree")`; v1 calls `git cat-file -e worktree:<path>`. Git returns `fatal: invalid object name 'worktree'`. All four actually tracked paths are then reported missing. This is not missing R84 evidence.

Impact: calibration counter's advertised CLI contract, Q22 reproduction. Smallest safe correction: resolve an actual revision for the tracked-path leg in default mode, or make --rev explicitly required with an honest documented contract. Falsifier: default mode resolves a real tree tip and reaches the same eight-check target with the same tracked paths.

### F5 — MAJOR: C2 v2 omits the frozen SETUP-fixture half

Counterexample by code: v2 only loops TABLE/DEFECTS/CLAIMS, reads FREEZE_REV bytes and compares measured-tree bytes. It never invokes the C1 fail-closed SETUP fixture.

The frozen table explicitly promises `freeze-tree presence + a SETUP fixture run`. That fixture does exist and passes in C1 `--selftest` (`freeze-anchor-fails-closed`); it is not executed by the named C2 check. Thus a green v2 alone does not establish the full frozen check. Its BASE red is an absence before the freeze, labelled `drifted-since-freeze`, not an exercised late-freeze-anchor failure.

Impact: calibration, Q24's failure-capable instrumentation. Smallest safe correction: execute the promised fixture as part of v2 and preserve its setup exit evidence, without changing the frozen predicate. Falsifier: identify the fixture subprocess in this v2 execution path, not merely in another tool's selftest.

### F6 — MINOR: frozen V3 exit convention contradicts the executable control

Evidence: the frozen R84-V3 check column says `--control-forged-receipt` prints `target_reached=False`, exit 1. Actual rejected-forgery control exits 0; C1 `control()` returns zero when target is NOT reached. C2 now explicitly accepts rc=0 (commit `217910c5` and the later code/behaviour split).

Impact: calibration acceptance instructions. The executable convention is sensible, but it is not the frozen text's stated convention. Smallest safe correction: append an explicit corrigendum distinguishing a rejected fixture's underlying predicate exit 1 from the successful control runner's exit 0. Do not silently replace the frozen wording. Falsifier: a frozen text interpretation explicitly making that distinction, or the actual control returning exit 1 while rejection is counted successful.

### F7 — MINOR: green Q13 selftest does not exercise the line-start anchor

Counterexample: in an isolated copy of `gate_timing_check.py`, removing `^` and MULTILINE from `REPORT_AUTHOR_RE` left `--selftest` exit 0 with the same final output. The real selftest tests line-start writer/author conflicts, but has no contrasting mid-line declaration that must not count.

Impact: the V6 repair's claimed anchor exercise, not the separately observed writer rename. Smallest safe correction: add the contrasting mid-line selftest/anchor mutant through the authorized owner; this seat did not change the operator-owned checker. Alternatively acknowledge the narrower evidence in the report. Falsifier: an existing selftest that fails on this exact de-anchored regex. Scratch baseline and mutant outputs both ended `ALL PASS`.

### F8 — MAJOR: v7 does not test the full frozen repair and v9 tests a declaration

Evidence: the frozen V7 repair requires the round-85 lesson AND report to carry the corrected trend plus a dated correction. v7 reads two substrings from round-84.md and `expansion: unchanged` from round-85.md; it checks neither a date nor the round report. A false or undated statement containing the two tokens passes that part. v9 checks only the strings `Definition horizon`, full BASE sha, and `future file`; it does not interpret whether the future-file condition is actually priced.

The actual lesson prose is notably more honest than these checks: its horizon section explicitly says V3/V5/V7/V9 reds at BASE mean absent, not measured-and-wrong. That disclosure should be credited; an eight-red transcript is not eight independent causal demonstrations. The kill-rule phrase `a repair that is prose only` needs interpretation because V7/V9 are prose repairs by design.

Impact: calibration, Q23's rejection of correctly labelled but false statements. Smallest safe correction: check the frozen repair's named artifacts/date and use content-specific conditions rather than token co-presence; keep the existing horizon disclosure and carry the report obligation until the report exists. Falsifier: demonstrate these checks reject an undated/false-token-only correction and a report missing the promised line.

### F9 — MAJOR: the two claims are not artifact-independent under R13

Counterexample by dependency: C2 v2 directly counts C1's frozen case table; v3 reads C1's counter and invokes its forged-receipt control. Reverting C1's instrument paths makes v3 `instrument-absent`, changing C2's count. Both frozen claims also explicitly reference those dependencies.

QUALITY R13 says no claim's counting command counts another claim's created artifact and requires the other-claim-paths-reverted count not to move. The frozen heading nevertheless calls these claims causally separable. Different axes do not satisfy that mechanical independence rule. The newer code-only v3 path without a receipt reduces one dependency but not the shared-counter/table dependency.

Impact: coverage/calibration claim sizing; canonical judge must decide whether both credits are compatible, rather than this leaf admitting a waiver. Smallest safe correction: report the shared artifacts and the failed independence condition honestly; do not silently narrow or rename a frozen claim. Future claims can separate instrument repair from its coverage use prospectively. Falsifier: a documented authorized partition plus a revert test leaving both claim counts unchanged.

### F10 — MINOR: host/revision stamp fields are present but not bound

Counterexample: in a complete isolated tip fixture, changed receipt LANE_TIP to forty zeros and HOST_PYTHON from Python 3.14.8 to Python 3.9.1, leaving the block intact. C1 still printed its exact green target with defects=0.

Evidence: the counter requires presence of HOST_PYTHON/HOST_OPENSSL/LANE_TIP but does not validate their values; reproduction compares only observation blocks. A reproducible block cannot authenticate the original host/revision stamp. This does not imply the real receipt's host fields are false.

Impact: provenance wording in the coverage claim (`host-pinned`). Smallest safe correction: distinguish recorded host metadata from mechanically verified host/revision binding in the lesson/report, or validate the promised binding using independent retained evidence. Falsifier: reject the demonstrated false-stamp fixture with a field-specific defect while keeping its authentic block reproducible.

### F11 — MAJOR: current v3 can close V3 without executing the frozen forged-receipt check

Evidence at `def5d0ea`: after substring-based `code_leg` checks, v3 does `if not tree.has(RECEIPT): return code_leg, ... receipt-absent(no behavioural leg)`. Thus deleting the receipt can leave V3 closed based on source-token presence alone. The frozen V3 check requires the forged-receipt control's measured rejection, not an optional behavioural leg. Source text containing the guard/default/call substrings also does not prove they lie on the executed path.

Impact: calibration discharge, Q24's distinction between an unevaluated run and a rejection. Smallest safe correction: keep the behavioural obligation unsatisfied until an independently built forged fixture is actually checked, or construct a fixture without relying on the production receipt. Do not count an unrun behavioural check as closed. Falsifier: v3 refuses the no-receipt case or still executes a real forged-control run there. This finding is grounded in the branch, not a claimed executed deletion experiment.

## Per-defect causal assessment

- V1: faithful tracked-tree check with a relevant BASE red. Default CLI bug is F4.
- V2: real freeze presence and byte binding; fail-closed behaviour exists in C1 selftest, but the named C2 check omits it (F5). BASE absence is not the original late-freeze mechanism.
- V3: real unconditional reproduction rejected the tested forged block. BASE red is instrument absence; the current optional behavioural path is weaker than the frozen check (F6/F11).
- V5: Q61 landed, has the required citation, and its placeholder-row control was measurably refused. v5 itself is a three-token check; this does not prove an entry-admission counter rejects informed filler. Q61 explicitly discloses the standing-counter limit. Do not inflate this to completion of that standing system.
- V6: writer rename is substantive and observed; the checker stays unchanged from BASE. Its selftest does not discriminate the anchor (F7).
- V7: a real dated append-only correction exists. The check is weaker than the frozen repair and omits the report (F8).
- V8: strongest mechanical before/after: literal flags 0/4 at BASE, 4/4 at tip. This is not a missing-future-file red.
- V9: honest horizon prose is present, with the existing full BASE revision. Its check reads a compliance declaration, not causal accounting (F8). The disclosure landed after the freeze in the successor lesson, so it must not be described as pricing already present in the frozen claims text.

V4 exclusion is honest: `round85-defects.json` explicitly routes it to operator, the counter prints ROUTED and counts eight other ids, `gate_timing_check.py` had no BASE-to-tip diff in the observed tree, and no round-85 falsify/wave2 directory was found. Do not quietly call V4 discharged.

## Admission/claim-sizing interpretation

This is a genuine narrow member execution, not a solved-task/model result or a newly covered class. The captured subject digest matches the pin. The eight frozen numerical predictions are correct; duplicates collapse to eight and six integer pairs equal the six float pairs in Python. Ledger-only and wrong/self-consistent forged-block controls did not go green. Table drift and a missing frozen input failed closed.

Q1–Q10 and Q21 primarily govern knowledge admission; this round asserts no new knowledge entry admission, so their entire checklist is not an invented extra C1 predicate. Their source-scope, exact-number, retained-evidence and correction principles do apply to the lesson's factual sentences. Q11/Q12 are not a demand for confidence intervals on eight deterministic fixtures. Q13–Q16 apply to the held-entry identity repair without waiving operator-owned V4. Q18/Q20/Q22/Q24 prohibit substituting later declarations, unrelated green checks, or unexecuted controls for frozen evidence. Q60 requires byte-derived corrections, not repeating a mistaken class cell. Q61's demonstrated placeholder refusal is bounded, not an informed-forger or standing-admission result.

The same claim sentence must survive from plan to counter to label: current green target lines do not erase the wrong class label, omitted check halves, default-mode failure, or the losing mutant receipt. Do-nothing is demonstrably red. One-artifact-one-claim is not demonstrated (F9). Corrections must preserve the frozen table and declare limitations rather than silently narrowing it after landing. These are issues for the canonical judge; this seat neither integrates nor admits either claim.

## Review limits and self-check

Executed review experiments used scratch-only subject/checker variants and path substitutions, not alternate production receipts. They test discrimination, not the byte-identity gate; changed subjects correctly fail the real subject pin. One initial path-substitution experiment mistakenly left the subject reading /app and produced FileNotFoundError; it was corrected before drawing the F3 conclusion. A tested Counter-intersection mutant was not misreported as a score-16 model.

Self-check: accuracy 4/5 (pinned measurements and explicit inference labels; moving tip limits finality); completeness 4/5 (both claims and all eight ids covered; report not yet filed cannot be audited); clarity 4/5 (separate target passes from control/check defects); actionability 4/5 (each finding has correction and falsifier, integration deliberately remains with L1); conciseness 3/5 (eleven independent defects require a long report). Mean 3.8/5. Highest-impact actions: fix the stale mutant fixture; append the exact class-count correction; restore the frozen behavioural/check obligations without changing their predicates.

SEAT CriticR85 VERDICT FINDINGS findings=11

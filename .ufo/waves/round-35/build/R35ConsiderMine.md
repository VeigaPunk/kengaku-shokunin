# R35ConsiderMine — considerthese 2026-10-25 mining (proposal 2 + sibling proposals)

Seat: scribe (leaf). Scope: mine `considerthese/2026-10-25.md` §Self-improvement suggestions 2 against
what round 35 actually implements (`plans/defect_ledger.py` + `corpus/defects.jsonl`), cross-check the
r30–r33 defect counters for class recurrence into round 34's D1–D5, draft the Round35 QUALITY criterion,
and note what of proposals 1 and 3 round 35 leaves unimplemented.

## 1. What proposal 2 asked for

Source: `considerthese/2026-10-25.md:39-45` (quote):

> 2. **One persistent routed-defect ledger instead of a new `plans/roundNN_defects.py` per round.** … Proposal:
> `corpus/defects.jsonl` (id, class, opened_round, closing_commit, recurrence) with one checker that
> (a) re-runs every closed defect's check at tip forever, (b) blocks pre-registration when a class
> recurs twice, and (c) includes a tip-receipt validator (every `corpus/evidence/**` receipt re-run and
> byte-compared), which would have caught D3 mechanically.

## 2. What round 35 implements (matrix)

Implementation evidence: `plans/defect_ledger.py` (committed at freeze `11d6453`; `git status` shows it
unmodified), `corpus/defects.jsonl` (five rows R34-D1…D5), frozen predicate in `plans/round-35-claims.md:47-55`.

| Proposal part | Implemented? | Evidence |
|---|---|---|
| Persistent `corpus/defects.jsonl` + one checker instead of a new `roundNN_defects.py` per round | **Yes** | `corpus/defects.jsonl` rows carry `id, class, opened_round, source, check, status, closed_round, recurrence_of`; single checker `plans/defect_ledger.py` with `CHECKS` = the five `r34_d*` functions. Schema deviates from the proposal: `closing_commit` → `closed_round` (round number, not commit); `recurrence` → `recurrence_of`; adds `source` and `check` fields. |
| (a) re-run every closed defect's check at tip forever | **Yes** | `defect_ledger.py` docstring: "re-runs EVERY row's check at the current tip, forever" (lines 7-9). `main()` (lines 120-137) runs every row's check on every invocation, and counts a calibration mismatch both ways: `closed` whose check fails AND `open` whose check passes (`agree = (is_closed and ok) or (st == "open" and not ok)`, line 132). PREDICATE requires all rows closed, all observed pass, zero mismatches (lines 138-139). The "forever" is a standing bar because C2's frozen predicate (`round-35-claims.md:47`) and Q23 both bind future tips to this command. |
| (b) block pre-registration when a class recurs twice | **No** | `recurrence_of` is recorded, never read: `grep -n recurrence_of plans/defect_ledger.py` → no hits; `main()` consumes only `check`, `status`, `id`. No pre-registration gate exists anywhere in the checker. Q23 (worktree) already names this: "`recurrence_of` is recorded, not enforced" (`corpus/QUALITY.md` ~line 291). |
| (c) tip-receipt validator (every `corpus/evidence/**` receipt re-run and byte-compared) | **No** | `CHECKS` = only `r34_d1…d5`. No scan over `corpus/evidence/**` exists. Narrowest analogue: `r34_d3` (lines 55-66) verifies the single `tb2-eval/SHA256SUMS` manifest's listed digests against file bytes — one specific receipt, not the general evidence-wide re-run+byte-compare the proposal describes. Q22 (`corpus/QUALITY.md:255-271`) remains the "cheap half" (receipts must re-run at tip by report close); the general validator is still unimplemented debt. |

Run at tip (2026-10-25, lane worktree; `python3 plans/defect_ledger.py --lane .`):

```
R34-D1 status=open observed=fail agree=yes untracked=5
R34-D2 status=open observed=fail agree=yes committed_mirror_paths=109413
R34-D3 status=open observed=pass agree=NO listed=6 evaluator_listed=True bad=0
R34-D4 status=open observed=pass agree=NO correction_lines=1
R34-D5 status=open observed=fail agree=yes erratum_lines=1 r35_mistake_row=False
rows=5 closed=0 observed_pass=2 mismatches=2
PREDICATE C2 fail
exit=1
```

Freeze control `claims/control-c2-nothing.txt` (committed at `11d6453`) matches the frozen claim:
`rows=5 closed=0 observed_pass=0 mismatches=0`, `PREDICATE C2 fail`, exit 1. The two rows that flipped
green in the worktree since freeze are the *observed*=pass/`agree=NO` rows: D3 (`listed=6
evaluator_listed=True` — the tb2-eval manifest now lists the evaluator files) and D4 (`correction_lines=1`
— the SCORECARD D4 correction line exists). D5 is half-done (`erratum_lines=1`, but `r35_mistake_row=False`:
`corpus/lessons/round-35.md` has no `## Mistakes` table with an S091 row; the lesson file is currently 15
lines, WIP). D1 still has 5 untracked paths under the round-34 wave/plan paths. `control-c2-flip.txt`
(shared clone, all rows flipped `closed`, nothing repaired) scores `rows=5 closed=5 observed_pass=1
mismatches=4` — demonstrating the status-only flip cannot satisfy the predicate.

## 3. Class recurrence across r30–r33 counters into round 34 D1–D5

Counter classes read from `plans/round30_defects.py` (D1–D5), `plans/round31_defects.py` (R1–R10),
`plans/round32_defects.py` (R1–R7), `plans/round33_defects.py` (N1–N6) — each counter's frozen labels
in `CHECKS`/`FROZEN`.

Round-34 defects and their recurrences:

- **D1 `uncommitted-round-work`** (ledger `recurrence_of` = `R33-N1 (round-32 wave paths untracked at
  tip; plans/round-33-claims.md:87)`). Class history: R30-D4 `uncommitted-wave-evidence`
  (`.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md` uncommitted) → R31-R9
  `round30-seat-reports-committed` (five wave seat reports modified/uncommitted) → R33-N1
  `round32-wave-tree-committed` (ten round-32 wave paths untracked at a pushed tip) → R34-D1.
  **Direct class recurrence.** ⚠ Note: the task brief's example says "round-32 N2"; per `round33_defects.py`
  and `plans/round-33-claims.md:87`, the untracked-wave-tree defect is **N1** (N2 = SCORECARD section).
  The freeze commit's `defects.jsonl` row actually carried the wrong pointer `R32-N2 (…; SCORECARD.md
  round-32 section)`; the current worktree delta corrects it to `R33-N1` (`git diff corpus/defects.jsonl`).
- **D2 `committed-scratch-bloat`** — no antecedent class in r30–r33 counters (committed recursive mirror
  blobs; 109,413 mirror paths at tip as of the run above). New.
- **D3 `receipt-claims-unbacked-manifest`** — family-level repeat of receipt/evidence integrity class:
  R32-R3 `round31-cli-receipt-regenerated` (receipt rewritten with a wrong relative path; every line
  `can't open file`/`exit=2`) is the closest prior; D3 is a different sub-class (manifest omission vs
  path corruption). Both are exactly what proposal-2 part (c) was designed to catch mechanically.
- **D4 `scorecard-misattribution`** — sibling of R33-N2 `scorecard-round32-section` (missing SCORECARD
  round-32 section): both are SCORECARD-layer recording defects; D4 is a wrong attribution, N2 a missing
  section. Different defect, same surface.
- **D5 `false-refusal-reason`** — new class (reviewer/refusal reasoning error). No r30–r33 antecedent.

Also notable: round 33's own N3/N4/N5/N6 are direct recurrences of round 32's R1/R2/R6/R7 classes
(phantom hash `a44b5a8`; report-before-final-commits; stale lesson locators; lesson-vs-registry fact) —
i.e. the per-round counter pattern already tolerated within-window recurrence, which is the motivation
for proposal-2 part (b).

## 4. QUALITY.md criterion draft

Worktree `corpus/QUALITY.md` already carries an uncommitted 24-line addition
(`git diff corpus/QUALITY.md`; not in freeze commit `11d6453`) titled
`## Round35 criterion — a routed defect lives in one ledger and re-runs forever` → Q23, lesson pointer
`corpus/lessons/round-35.md` §Mistakes. It matches the requested style (lines 255+), the frozen claim,
and the D1↔R33-N1 recurrence. Verified gaps against the assignment's spec (supply to L1):

1. Title differs from the requested `## Round35 criterion — routed defects live in one ledger` (semantic
   match; keep either, but the assignment names the latter).
2. Its Limits note part (b) (not implemented) but does **not** record that part (c) — the tip-receipt
   validator — is also unimplemented. Add it (see §2).
3. It says D1 "recurs round 33's N1" — correct, and now consistent with the corrected jsonl row (the
   freeze-committed row said R32-N2).

Draft for the L1 (Q23 replacement/addition, style-matched):

```
## Round35 criterion — routed defects live in one ledger

- **Q23 — every defect a non-author closure routes to this lane enters `corpus/defects.jsonl` with a
  check in `plans/defect_ledger.py` that is red when the row is written; a row says `closed` only
  while its check passes at the tip.** A defect closed in prose and checked by a one-round counter
  (`plans/round30_defects.py` … `round33_defects.py`) is checked once and then forgotten: round 34's
  D1 (round-34 work left untracked) recurs round 33's N1 (round-32 wave paths untracked at the tip,
  `plans/round-33-claims.md:87`), and nothing re-ran N1's check after round 33 closed it. The ledger
  checker re-runs every row at every tip and counts a calibration mismatch for a `closed` row whose
  check fails and for an `open` row whose check passes. Executable check: `python3
  plans/defect_ledger.py --lane .` — any `agree=NO` line, or a nonzero exit while a round report says
  its defects are closed, is a failure. Each check compares the lane's self-assessment with an
  observation computed from repo bytes (a manifest digest, a tag-stripped capture, the branch tree), so
  a correctly labelled but false sentence does not pass. Shown able to fail: all five round-34 rows red
  at the round-35 freeze (`.ufo/waves/round-35/claims/control-c2-nothing.txt`) and a status-only flip
  scores `mismatches=4` (`control-c2-flip.txt`). The proposal and its date are
  `considerthese/2026-10-25.md` §Self-improvement suggestions 2 ("one persistent routed-defect ledger
  instead of a new `plans/roundNN_defects.py` per round", 2026-10-25); this discharges the debt Q22
  named. Limits: parts (b) and (c) of that proposal are not implemented — `recurrence_of` is recorded,
  not enforced (no pre-registration block on a class recursing twice), and there is no general
  tip-receipt validator over `corpus/evidence/**` (only D3's tb2-eval manifest check); checks are
  per-defect functions, so a new routed defect still needs code. Mutation scratch runs in a `mktemp`
  clone outside the lane and commits only receipts (round-34 D2: 109,413 committed mirror paths at the
  round-35 freeze). Lesson: `corpus/lessons/round-35.md` §Mistakes.
```

## 5. Proposals 1 and 3 — what round 35 should note as not-implemented

- **Proposal 1 (model-diverse verification)** — not implemented. `considerthese/2026-10-25.md:34-38`
  notes all 18 roles route to `@m_flash` and the non-author integrator is the same model; no second-model
  discernment sample or disagreement log appears in the round-35 claims, controls, or the Q23 delta. The
  round's calibration remains single-checker, single-model. (No round-35 prompt file found under
  `/.ufo/prompts/` to inspect further; conclusion rests on claims/controls/QUALITY delta.)
- **Proposal 3 (decision packet for the round-25 L0 coverage cap)** — not implemented, and the claims
  file owns the gap: `plans/round-35-claims.md:10-11` "Coverage stays capped at 7 by the open
  round-25/round-33 L0 question (`.ufo/l0-questions.md:163`); C1 is judged on its counter, not on a
  score move." The L0 question at `.ufo/l0-questions.md:163` (kengaku | round-33, "decision packet: what
  committed evidence lifts the round-25 L0 coverage cap") is still open and unanswered. Round 35
  correctly declines to spend on it; note it as carried debt.

## 6. Out-of-scope / limits

- No installs made (no tooling channel records).
- Observations are of the worktree at 2026-10-25 (mid-round; rows still `open`): the D3/D4 green
  observations above reflect repairs landed since freeze — final landing state is the L1's to verify.
- Round-35 prompt file not locatable (searched `/.ufo/prompts/` and lane); no impact on the matrix.

VERDICT: considerthese-mined-1/3

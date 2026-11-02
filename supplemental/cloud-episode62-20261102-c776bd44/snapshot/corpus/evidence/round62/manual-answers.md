# Round62 manual answer freeze

Author: kengaku-shokunin-round62. Date: 2026-11-02.
Challenge: parent's independent reviewer `judge_kengaku_round62`, public
`audit/kengaku62-independent/manual-challenge.md`. Neither sealed oracle read.
All fractions below derived by hand; no metric script, upstream function,
benchmark, model/provider, or alternate sandbox route executed. The original
283-case machine oracle is excluded; this answers only the revised manual set.

Notation: A=finite-panel pass@k; R=finite-panel pass^k; bounds [lower,upper].
D=C(n,k). Counts in the derivations are subset counts, not empirical model
performance. Each task status measured means all outcomes observed; bounded
means unresolved outcomes remain even if one interval collapses.

| case | per-task result and derivation | fixed-task suite result |
|---|---|---|
| 1 PPFF, k2 | n4,c2,D6. One all-fail pair, one all-pass pair. A=[5/6,5/6], R=[1/6,1/6], measured | same; measured |
| 2 PPFF, k1 | D4; two passing singleton slots. A=[1/2,1/2], R=[1/2,1/2], measured | same; measured |
| 3 PPP, k3 | D1; sole subset all-pass. A=[1/1,1/1], R=[1/1,1/1], measured | same; measured |
| 4 FFF, k3 | D1; sole subset all-fail. A=[0/1,0/1], R=[0/1,0/1], measured | same; measured |
| 5 PPFFF, k5 | D1; sole subset contains successes and failures. A=[1/1,1/1], R=[0/1,0/1], measured | same; measured |
| 6 PF; PPPFF, k2 | PF: D1, A=[1/1,1/1], R=[0/1,0/1]. PPPFF: D10, one all-fail pair, three all-pass pairs, A=[9/10,9/10], R=[3/10,3/10]. Both measured | equal-task mean A=[19/20,19/20], R=[3/20,3/20], measured |
| 7 PFEM, k2 | n4,c1,u2,D6. All unresolved fail: three all-fail pairs, zero all-pass pairs. All unresolved pass: zero all-fail pairs, three all-pass pairs. A=[1/2,1/1], R=[0/1,1/2], bounded | same; bounded |
| 8 PPE, k2 | n3,c2,u1,D3. Regardless of E, every pair contains a pass. All-pass pairs range from one to three. A=[1/1,1/1], R=[1/3,1/1], bounded | same; bounded (the exact A does not make E observed) |
| 9 P; PPF, k2 | P: n1<k2, no subset, A=null,R=null,ineligible. PPF: D3,no all-fail pair,one all-pass pair,A=[1/1,1/1],R=[1/3,1/3],measured | macro=null; ineligible/could-not-evaluate, not the second task's score alone |
| 10 PEF; MPPFF, k2 | PEF: n3,c1,u1,D3; all-fail pairs range1→0, all-pass pairs0→1. A=[2/3,1/1],R=[0/1,1/3],bounded. MPPFF: n5,c2,u1,D10; all-fail pairs3→1, all-pass pairs1→3. A=[7/10,9/10],R=[1/10,3/10],bounded | A=[41/60,19/20], R=[1/20,19/60], bounded; average each endpoint over two tasks |

## Distinct wrong interpretations rejected

- Case1 rejects swapping discovery and consistency: five of six pairs discover
  a success but only one pair is all-success. It also rejects plug-in powers:
  empirical p=1/2 would give discovery3/4 and consistency1/4, not5/6 and1/6.
  Those plug-in numbers answer a with-replacement empirical resampling question.
- Case6 rejects pooling: four successes among seven slots yields D21,
  discovery18/21=6/7 and consistency6/21=2/7, unlike the macro results19/20
  and3/20. Pooled pairs span tasks and change the event, not merely precision.
- Case7 rejects dropping unresolved slots: surviving PF at k2 would give
  discovery1 and consistency0 as points. It discards the two planned slots and
  conceals both intervals. Counting E/M as observed F instead selects the lower
  endpoints without the declared operational-failure estimand that could justify it.
- Case9 rejects assigning zero or perfect success to n<k, and rejects silently
  reporting only the eligible task. The fixed planned task population remains.
- Case8 rejects “equal numeric endpoints imply complete observations”: discovery
  is already saturated, but E remains unresolved and reliability is not identified.

These are manual logical counterexamples, not executed mutants or runtime tests.
A reviewer may falsify an arithmetic answer independently; matching this set is
not proof of an implementation, model intelligence, IID trials, or a 95% CI.

## Input/estimand discipline

Absent task/slot records cannot be inferred from the surviving panel; a separate
planned manifest is needed to detect omission. An explicit M contributes to n
and u. Reject duplicate task IDs and duplicate slot IDs within a task (otherwise
one observation can be counted repeatedly); duplicate JSON keys (ambiguous
interpretation); unknown fields/statuses (unannounced semantics); boolean,
floating/nonpositive k (not a positive integer subset size); empty task/trial
lists (undefined population); and the proposal's resource overages (>100 tasks,
>1000 slots/task, >1MiB input, k>1000). These are declared input rules, NOT a
claim a validator has been implemented or run. A finite-panel formula needs no
IID assumption. The future-draw unbiased interpretation needs iid binary trials
with stable per-task p and fixed sampling/stopping design. Missing-outcome
bounds describe identification, not sampling uncertainty; repeated correlated
runs or adaptively selected observations cannot supply a future-trial guarantee.

## Source analysis, no upstream execution

HumanEval capture `humaneval-evaluation.py` at
b9453e8f1865df0a0057a1383767caa400acfbcf: `estimate_pass_at_k` lines13–36
implements per-task estimates; `evaluate_functional_correctness` lines88–91
filters k with `(total >= k).all()` and takes the task mean. The outer guard,
not the helper's early return, establishes the caller's sample-size domain.

Tau capture `tau-run.py` at59a200c6d575d595120f1cb70fea53cef0632f6b:
line184 defines n as count of globally unique trial IDs, lines188–199 count
success per represented task then macro-average C(c,k)/C(n,k). Complete balanced
panels with aligned trial IDs justify that common denominator; arbitrary
incomplete/misaligned panels do not. Lines90–99 catch an exception and construct
reward0, rather than an unresolved-success interval. No claim here establishes
how any actual published result was computed or its error frequency.

## C2 historical precision answers

Read-only evidence: `.ufo/waves/round-62/recon/precision-before.txt`.

- D1: `.ufo/waves/round-61/recon/table-identity.txt` records THREE differing
  lines: separator row, sequential-sync, no-max-enforcement. Thus TWO data
  rows differ; “one row”/“other eleven identical” was inaccurate. The amended
  embedded table was the corrected one; historical first-failure bytes stay.
- D2: fresh WHATWG capture line105 is pointer98, codepoint0x00E2. In this index,
  byte=pointer+0x80, so byte0xE2 (226 decimal) is pointer98, not pointer226.
  The original S225 row remains and a successor source row must correct it.
- D3: base f97e5b7b81d02084b63042631e0f3a1897af25c7 has272 LF,0 CR;
  freeze215a70291349abfbfaba8de9dd8d3d1f330a0002 has274 LF,274 CR
  (274 CRLF); repairb99205767bac69358bc827a2da9da783d707125b has274 LF,0 CR.
  Local `git diff --numstat f97e5b7b 215a7029 -- corpus/SOURCES.md` reports
  +274/-272, total546; base→repair+2/-0. Therefore the author's273 was wrong,
  but546 matches this measured command. The old review's +274/-237=511 does
  NOT reproduce; no cause established. Correct both author and reviewer prose
  append-only rather than substituting the old review's incorrect figure.

No claim that Q23's perpetual executable defect check has run or been extended.
Precision correction can be independently reviewed; automation remains a named
conformance limitation under the host restriction.

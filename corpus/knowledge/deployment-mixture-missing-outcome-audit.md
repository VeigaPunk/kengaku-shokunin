source: S231 — https://arxiv.org/html/2404.16966v1 §3.3; S232 — https://arxiv.org/pdf/2205.07388v1 §1 p1 and §3.1 p7 Eq(1)–(2)
verified-at: 2026-11-02
recheck: 2027-05-01 (180d) — reopen pinned sources; reassess use-case weights, missingness semantics and transport before applying to any real decision

# Release-audit memo: mixture, missing outcomes and a fixed deadline

Manual design knowledge only. This is not a running evaluation harness, an
empirical model result, a statistical population PASS, or deployment authority.
It extends paired-eval-uncertainty-reporting.md and the historical task27 timeout
analysis; pairing/clustering/multiplicity are existing knowledge, not this round's
novelty. See the committed independent brief and first author memo for the worked
case once admitted.

## Read the record before ranking

Fix the decision object: system revision, scaffold, grader, task strata, deadline,
retry allowance, target mixture and cost accounting. Maintain an assigned-attempt
ledger with success, observed failure, truly unknown result, and provenance.
A known deadline miss is failure for success-by-deadline even if the eventual
answer might be correct. A lost outcome log is not necessarily failure: call it
unknown unless independent evidence establishes the endpoint. This distinction
is a property of the declared endpoint, not the vendor's preferred exclusion.

S231 (original 2024 study, not independent replication) §3.3 states “there is no
universally correct distribution of interest”. Its model-ranking sensitivity
motivates choosing weights from the application rather than convenient benchmark
counts. It does not identify a user's deployment distribution. Reweighting cannot
repair absent coverage, within-stratum shift or invalid graders.

S232 (Manski's 2022 methodological argument) §1 p1 considers “all logically
possible distributions of the missing data”. Its point is that missing-data
inference needs credible assumptions; it does not ban valid model-based
imputation. The binary finite-record specialization below is derived here.

## Exact finite-panel audit (not confidence intervals)

For stratum h and system m, let assigned n=s+f+u>0, with successes s, failures f,
unknowns u. Lower l=s/n, upper r=(s+u)/n. With common target weights w summing1:
L_m=sum(w_h*l_mh), U_m=sum(w_h*r_mh). Contrast A-B lies in
[L_A-U_B,U_A-L_B]. Proof: each unknown binary outcome contributes between0 and1;
choose all unknown A outcomes0 and B outcomes1 for the contrast minimum, reverse
for its maximum. Without additional joint restrictions those endpoint choices
are feasible even for paired tasks. Marginal totals alone do not supply a paired
standard error. A positive interval lower endpoint is robust to these missing
outcomes on this panel; it is not a confidence statement about future requests.

For two strata with w in[a,b], evaluate both endpoints of each affine contrast
bound. If delta is a required margin, solve lower_bound(w)>=delta, honoring the
policy's strict/inclusive comparison. Unknown weights are not permission to
choose whichever favors A. If a positive-weight stratum is entirely unmeasured,
its binary rate remains[0,1]; do not omit it and renormalize the rest.

## Decision before more measurement

Report four distinct objects: observed-data statistic, finite-panel identified
set, weight sensitivity, and uncertainty about deployment. Costs are billed
attempt totals divided by assigned counts, then weighted by the same target
mixture. Cost per success answers a different question. Missing outcomes do not
make spent compute free. If cost is itself missing, bound it using justified
limits or mark feasibility unresolved; outcome bounds do not bound costs.

A fictional finite-panel screen can require worst-case improvement >=delta AND
cost<=ceiling. State eligibility only for that screen. A real release also needs
representative within-stratum sampling, outcome/identity integrity, design-valid
uncertainty and authority. Q11 remains binding for any population binary-rate
PASS. Identification bounds and sampling uncertainty must both be addressed;
no arithmetic combination here claims valid confidence coverage.

Recovery priority is an information question as well as a budget question:
recover original logs before buying replacement runs when they resolve unknown
original outcomes. Preserve unsuccessful attempts. Any rerun uses a prospectively
symmetric outcome-independent rule and retains both records; changing timeout,
prompt, exclusions or retry count changes the evaluated system/estimand. Random
new samples may reduce sampling uncertainty but need not identify lost outcomes.

## Reject and flip conditions

- Completed-only ranking: reject as assigned-panel evidence; flip only with a
  justified missingness model for the desired estimand or recovered outcomes.
- Favorable benchmark mixture: reject for target ranking; flip when independent
  target-distribution evidence supports those weights and transport assumptions.
- Longer timeout only for A: reject as same-protocol repair; it is a new system
  comparison requiring equal policy specification and separate reporting.
- Identification interval called95% CI: reject; flip requires an actual valid
  inferential procedure with the real sampling/cluster design and assumptions.
- Cheap average price from successful runs: reject as total-attempt cost; flip
  requires complete assigned cost accounting or an explicitly different objective.

Falsifier: a counterexample to the endpoint construction under the stated binary,
fixed-denominator/no-cross-outcome-restriction model, or a memo that recommends
population release from these bounds alone. Additional constraints can tighten
the interval, but must be stated rather than smuggled into its interpretation.

## Worked audit and tradeoff

First manual answer: corpus/evidence/round64/first-audit-memo.md, frozen at
6576c75f6661ce25ce054345f4555c0c286a54dc before oracle release. It diagnoses
completed-record composition reversal, derives sharp missing-outcome bounds,
and distinguishes ranking from margin-and-cost eligibility. After authentic
recovery, the supplied candidate has advantage D(w)=1/5-13w/25 and cost6-3w:
more Easy reduces cost but also advantage. The fictional policy's joint feasible
weights are[1/5,15/52], not the whole supplied[1/5,3/10]. This is a case-specific
manual calculation, not a population confidence claim or a model-quality result.

Source S232 §3.1 printed p7 Eq(1)–(2) directly gives the conditional-mean
decomposition and bounded-support region; the finite-panel binary proof above
specializes that algebra, not its sampling interpretation. Novelty is the
integrated decision memo and repairs, not either established formula.

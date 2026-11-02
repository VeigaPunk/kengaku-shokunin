# Round64 proposal — deployment-mixture and missing-outcome release audit

2026-11-02; baseline fb8f996e4b05ee46e8977c91726ca23f74f5e0fe.
One exploratory claim C1, coverage (lowest axis; scalar7 held). Before:
paired-eval-uncertainty-reporting.md addresses pairing, clustering, resolution and
multiplicity; agent-time-horizon-and-task-validity.md addresses timeout design.
Neither supplies the joint mixture/missing-outcome decision audit below. Targeted
gap sweep .ufo/waves/round-64/recon/gap-sweep.txt is empty (exit1); this establishes
absence of these terms, not proof of global novelty. Those existing skills are
inputs, not new credit. After: a reusable end-to-end audit memo connecting
weighted estimand, missingness bounds, deadline scoring, cost feasibility and a
conditional fictional release decision. New synthesis, not new mathematics.

## Model frozen before independent task

Two pinned systems A and B, two or three mutually exclusive exhaustive task
strata. For each system and stratum: assigned count n>0, observed binary successes
s, observed failures f (including deadline failures under the stated policy),
and truly unobserved outcomes u with s+f+u=n. Input may give costs including all
assigned attempts. Structural missingness and absent strata must be refused or
bounded, never silently renormalized. Target stratum weights w>=0 sum1, given
prospectively or an interval for the first weight in a two-stratum problem.

Derivation (manual arithmetic, not statistical execution): stratum success lies
in [s/n,(s+u)/n]. Target mean lies in sums of weighted endpoints. Contrast A-B
lies in [L_A-U_B,U_A-L_B]; endpoints achievable without cross-system restrictions
on unobserved binary outcomes. These are finite-record identification bounds,
NOT sampling confidence intervals. Paired design alone does not force missing
A and missing B to agree. Observed-complete s/(n-u) is descriptive only unless
its missingness assumptions are justified. Expected cost uses total assigned
attempts and target weights, not success-only or completed-only denominators.
For uncertain two-stratum weights the linear bounds attain extrema at the two
allowed endpoints; display crossing threshold if rankings reverse.

Policy is part of the fictional case: target improvement margin delta, inclusive
or strict comparison, cost ceiling and whether uncertainty must be resolved.
We may certify a finite-record robust condition if its lower contrast bound
meets the supplied threshold and costs meet the ceiling. This is NOT a binary
population-rate PASS or deployment authorization. Q11 statistical rate admission
still requires its interval gate; no point table is granted population validity.
If sample-to-deployment transport, within-stratum representativeness, uncertainty,
or outcome integrity is unresolved, explicitly HOLD population release despite
any favorable finite-table calculation. Distinguish identification uncertainty,
sampling uncertainty, weight uncertainty and decision preference. Reruns/recovery
must preserve original attempts and specify symmetric, outcome-independent retry
rules; retrospective omission or tuning timeout changes the estimand.

## Source model (opened, source-only, never executed)

S231 proposed: Ailem et al., arXiv2404.16966v1 (25 Apr2024), §§1,3.3.
https://arxiv.org/html/2404.16966v1. Exact §3.3 quote: “there is no universally
correct distribution of interest”. Supports application-specific weighting and
rank sensitivity, not identification of actual deployment weights. Capture
corpus/evidence/round64/sources/ailem2024.html sha256
cc6b44ca618b56ee671cec0c65bf942a4fe334cff0083de8954c54a2421929a5.
S232 proposed: Manski, Inference with Imputed Data (May2022), §1 p1.
https://arxiv.org/pdf/2205.07388v1. Quote: “all logically possible distributions
of the missing data”. Supports identification-region reasoning, not a claim
that all imputation is invalid. Binary formulas above are explicit elementary
specializations derived here, not quoted paper formulas. Capture
corpus/evidence/round64/sources/manski2022.pdf sha256
ba25c02dcd2c0358a1012a3eaf19c504b28524dbcac2882fcd965a91b0faed5e.
Both older original research/preprints, not claims of 2026 frontier novelty.

## Independent challenge and gate

Parent-appointed /root/judge_kengaku_round64 creates ONE difficult integrated
fictional release brief with interacting constraints, plus counterfactual changes
that discriminate (i) mixture reversal, (ii) asymmetric missingness, (iii) timeout
versus unknown, (iv) cost denominator, (v) interval vs confidence, (vi) repair
versus post-hoc selection. Reviewer freezes private hand oracle before exposing
questions. Author commits first audit answer before oracle release. No scripts,
calculators, fixture/counter or generator execution by either seat. Metadata and
source-read operations are not semantics tests.

Exact arithmetic errors, missing assumptions, unsupported recommendations and
tradeoffs must be preserved, not rerolled. Arithmetic agreement is diagnostic
only: the single claim needs named non-author unprovable-but-better judgment
on new end-to-end operational utility, and no axis harm. Reject an answer that
gets numbers right but makes a population-release claim without valid uncertainty
or transport. Reviewer spot-checks an admit AND reject and source locations.

## Standing constraints

Strict Q32 envelope unavailable; no alternate execution. No provider calls,
credentials, purchases, security changes or scope expansion. TB2 stays17/89,
coverage cap7. Q23 literal defect-ledger discrepancy stays open; canonical62
maintenance/R61 repairs are not new credit. Cloud duplicate62 only supplement.
Sequential passes plus independent review use approved OPERATOR-ADAPTATION.
No64 closure self-attestation, no65 before parent closure. General methodology
stays chousa-owned; this is scoped to LLM evaluation decisions.

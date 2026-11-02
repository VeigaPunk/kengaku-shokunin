source: S228 — R4.5.1 p.adjust.R :41–45,70–81; S229 — R4.5.1 p.adjust.Rd Details; S230 — Benjamini & Yekutieli (2001), DOI10.1214/aos/1013699998, §1.2 and Theorems1.2/1.3 pp1167–1169. Captures: corpus/evidence/round63/sources/; pins: plans/round-63-proposal.md.
verified-at: 2026-11-02 (source reading and manual derivation only; independent admission pending)
recheck: 180d; reopen pinned sources and check fixed-family formulas, dependence and error-target limits; runtime equivalence requires a separately authorized sandboxed trial

# Multiplicity-aware model comparisons — fixed complete families

Candidate, not admitted until parent-appointed review. This develops the generic
family/multiplicity warning in paired-eval-uncertainty-reporting.md into exact
procedures. It does not replace paired/cluster-aware input tests: the correction
receives valid p-values; it cannot fix pseudoreplication, optional stopping,
contaminated evaluation data, or a wrong null hypothesis.

## Start with the decision, not the smallest p-value

A fixed family might be five predeclared model-vs-baseline contrasts on the same
benchmark. If all pairwise contrasts among those models were inspected, that is
not automatically the same family. Declare eligible contrasts, sidedness, task
population, estimand, error target and method before outcomes. The number of
models is not always the number of hypotheses. Repeated looks and metric/slice
search require their own design; no correction here licenses unlimited searching.

Let V be false rejections and R all rejections. FWER=Pr(V>=1); FDR=E[V/max(R,1)].
Both are repeated-sampling properties, not probabilities that a particular null
is true. FDR control does not bound every realized V/R or generally control FWER.
When all nulls are true, V=R and FDP is1 iff R>0, so FDR=FWER in that special case.
Corrected significance still does not establish practical importance: report
paired effect size and design-appropriate uncertainty, not only a reject label.

## Exact hand algorithm

Assume complete family m>=1, p_i in[0,1], and valid super-uniform null marginals
Pr(p_i<=t)<=t. Sort p_(1)<=...<=p_(m), keeping original hypothesis IDs. For the
small panels in the manual challenge use exact fractions, not rounded decimals.
Let a denote the chosen alpha (FWER) or q (FDR), depending on method.

| Method | Adjusted value at rank i | Reject rule | Guarantee conditions |
|---|---|---|---|
| Holm | min(1, max over j<=i of (m-j+1)p_(j)) | adjusted<=alpha; equivalently stop at first p_(i)>alpha/(m-i+1) | strong FWER<=alpha; arbitrary dependence, valid null marginals |
| BH | min(1, min over j>=i of mp_(j)/j) | largest k with p_(k)<=kq/m, reject ranks1..k; none if no k | FDR<=q under independence or the paper's PRDS-on-true-nulls condition |
| BY | min(1, min over j>=i of mH_m p_(j)/j), H_m=sum(1/j) | same BH step-up rule with q/H_m | FDR<=q under arbitrary dependence, valid null marginals |

Return adjusted values/reject decisions to original ID order. Ties get equal
adjusted values. Equality at the threshold rejects under this frozen convention.
Holm needs a PREFIX maximum; BH/BY need a SUFFIX minimum. A small p-value can
fail the first BH threshold yet be rejected because a larger rank meets its own
threshold. Applying Holm's first-failure rule to BH therefore loses discoveries.
The correction formula is inspected in S228; no R runtime parity was measured.
S229's phrase about arbitrary assumptions for Holm does NOT remove marginal
p-value validity or license arbitrary data-dependent hypothesis selection.

Why Holm survives arbitrary dependence (manual proof): let m0 true nulls exist.
If any true null is rejected, the first true null in ascending order has rank r
with m-r+1>=m0 and p_(r)<=alpha/(m-r+1)<=alpha/m0. The probability any true null
falls below alpha/m0 is at most sum over the m0 nulls of alpha/m0=alpha by the
union bound; independence is unnecessary. If m0=0, V=0 trivially. This proof
explains the assumptions; it does not prove any model evaluation supplied valid
marginal p-values. BH/BY guarantees are attributed to S230, not newly proved here.

## Domain judgment and explicit refusals

| Situation | Decision | Reason |
|---|---|---|
| Confirmatory claim that any selected model improves baseline | predeclare family; Holm if FWER is required | FDR is a different risk budget |
| Exploratory set of promising contrasts, justified independence/PRDS | BH may match the declared FDR goal | do not infer PRDS from shared questions or positive correlations alone |
| Exploratory family with unknown dependence | BY if its conservatism is acceptable, or redesign | arithmetic BH values can be computed but their nominal guarantee is not licensed |
| Pick minimum p after inspecting m candidates | retain full intended family or use independent validation/design-valid selective inference | singleton adjustment launders selection; family scope is substantive |
| No rejection | report insufficient evidence under this test/design | not equivalence, equality or no useful effect |
| Invalid per-contrast tests | repair design/inference upstream | multiplicity cannot repair bad p-values |

Missing tests, API NA/n semantics, hierarchical families, online/anytime testing,
selective intervals and power planning are not held by this entry. The source's
PRDS condition is stronger than a casual claim that all tests are correlated in
one direction; no custom benchmark is certified PRDS here. No empirical claim
about a model, leaderboard or future task population is made.

## Falsifiability and evidence boundary

The independent frozen challenge and committed answers must expose order,
monotonicity, step direction, family-size and interpretation errors. Any exact
value or guarantee failing independent source/derivation review defeats admission.
Source-code reading is not execution, and successful manual examples do not
validate an implementation, stochastic coverage or resistance to all misuse.
The generic preexisting multiplicity guidance stays intact; the gain is the
worked decision layer, not discovery of multiplicity itself.

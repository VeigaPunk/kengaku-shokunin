source: S243, Geifman & El-Yaniv2017 §§2–3, https://papers.nips.cc/paper_files/paper/2017/file/4a8423d5e91fda00bb7e46540e2b0cf1-Paper.pdf; S244, Kamath/Jia/Liang2020 §§2.3,3, https://aclanthology.org/2020.acl-main.503.pdf; original case work .ufo/waves/round-69/author/first-answers.md
verified-at: 2026-11-03
recheck: 180d; reread definitions and any guarantee assumptions before reusing them for a new evaluation

# Selective answering: count the people you do not answer

This extends the evaluation frontier with an abstention contract. It complements
`candidate-success-deployable-selection.md` and judge calibration, rather than
substituting for either. Canonical older papers define the setting, not current
LLM capability. This is manual evaluation judgment, not a live abstention system.

## Start with the ledger, not the headline

For each item retain identity, split, domain/group, frozen policy and threshold,
answer/abstain decision, correctness and any stipulated cost. Make three totals
visible: correct answers C, wrong answers W and abstentions A; N=C+W+A.
Show coverage(C+W)/N, retained error W/(C+W) when the denominator is positive,
and correctly served fraction C/N. Never interchange these denominators.
A report saying90% correct on400 answered requests out of1,000 means360 correct
answers, not900. The600 absent answers contain no measured counterfactual accuracy.
These definitions follow S243; all numerical examples here are original case work.

## Choose the comparison before choosing the winner

- At unequal coverage, lower retained error alone is not system superiority.
  A risk2% at coverage20% and B risk5% at80% trade off error against service.
- Compare a specified operating point. In caseB, at40% coverage A has5% error and
  B3%; this is B's empirical advantage there, not complete-curve dominance.
- Equal accepted counts need not mean equal accepted items. Preserve paired item
  decisions and outcomes for uncertainty analysis; do not infer paired discordances
  from marginal totals.
- If costs are meaningful, calculate across all requests. CaseC with correct+1,
  wrong-4, refusal-.1 gives A utility.240/request and B.380. Changing only wrong
  cost to-10 gives A.120 and B-.100. State the cost choice rather than declaring
  the lower-risk model universally preferable.
- A0-answer policy has undefined retained error0/0, although zero realized wrong
  answers. Label it NA/no accepted observations, not a perfect-risk champion.
  No universal minimum coverage or cost preference is implied.

## Keep fitting and certification apart

A threshold selected from evaluation labels makes that dataset selection data.
Keep its descriptive curve, but do not rename it untouched test evidence. Freeze
the chosen mapping/ties/threshold and evaluate a fresh representative set. Use a
prespecified bound/decision; if it fails, preserve the failure rather than tune
on those labels and rebrand them untouched. S243's algorithm supplies its own
sampling/search conditions; merely thresholding does not inherit its theorem.

Original caseF derives the fixed-threshold iid Bernoulli zero-error upper limit:
(1-u)^n=.05, hence u=1-.05^(1/n). With20 retained correct items, u≈.1391, not.02.
With zero errors149 retained iid items suffice for this one-sided95% limit≤.02.
This is not a two-sided95% interval, a posterior probability, or observed evidence
that149 future answers will be correct. Label-based selection and distribution
shift invalidate a naive transfer of that fixed-policy calculation.

## Equal retained accuracy can hide unequal service

CaseE: X answers810/900 and Y10/100, both with10% observed retained error.
Coverage is90% versus10%; correctly served fractions81% versus9%. Aggregate90%
retained accuracy does not erase those disparities. Nor do these tables establish
causes, error severity, counterfactual outcomes or a universal fairness decision.
Report subgroup denominators and uncertainty before drawing stronger conclusions.
This is original evaluation reasoning, not a claim either cited paper proves a
particular fairness criterion.

## Know what transports

S244 distinguishes absolute calibration from selective ranking and studies
extractive QA under source/unknown-domain mixtures. Its setup motivates checking
shift; it does not guarantee the same threshold's retained error in arbitrary
future generative tasks. Neither known-OOD training nor source calibration alone
certifies that transfer. Seek target-relevant labeled checks and explicit assumptions.
A bounded descriptive memo can still be correct: caseH's fixed policies show8%
versus12% retained error at50% empirical coverage. Accept this observation while
withholding population superiority and deployment guarantees.

## Boundary and falsification

Check the source definitions, immutable A–H answers and independent terminal
review. A denominator error, unsupported finite-sample promise or blanket refusal
of a valid bounded comparison would falsify this card's operational usefulness.
No pre-study matched baseline exists; case adequacy is not causal learning gain
or an estimated general reliability rate. Statistical-method invention belongs
to chousa; serving/deployment changes are outside Kengaku. No new TB2 coverage,
score change, Q23/Q32/Q38 closure or runtime parity claim.

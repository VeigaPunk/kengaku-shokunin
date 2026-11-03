# Round69 immutable first answers

Written after freeze fcb25f3b51cf2564856aada7bb37e40fb816235d and primary study,
before reading reviewer expectations. Manual original analysis; no model inference.

## A

Retained accuracy360/400=.90; selective error40/400=.10; coverage400/1000=.40.
Correct service fraction360/1000=.36, wrong service40/1000=.04, abstention600/1000=.60.
The last statement switches denominator from answered requests to all requests and
is false. Nothing identifies what the model would have answered on the600 abstentions,
or their correctness. Report90% correct among answered items,36% of all items answered
correctly on this fixed set. Incoming-population extrapolation requires representative
sampling and uncertainty assessment; neither is supplied.

## B

Original A point: coverage.20, risk4/200=.02; B:.80 and40/800=.05.
Neither dominates both dimensions: A lowers retained error while answering fewer.
A better-system conclusion requires the objective (risk constraint/coverage target or
costs) and adequate evidence, not minimum risk alone. At matched empirical coverage.40,
A risk20/400=.05 versus B12/400=.03: B is better on this operating point by2 percentage
points retained error, and8 fewer wrong answers. That supports neither full-curve
nor population dominance. Same number accepted does not prove same items accepted;
preserve identities, paired labels/acceptance and threshold provenance, then use
appropriate uncertainty analysis and report other operating points if relevant.

## C

A risk20/400=.05, coverage.40; utility380-4(20)-.1(600)=240, or.240/request.
B risk80/800=.10, coverage.80; utility720-4(80)-.1(200)=380, or.380/request.
Under these stated utilities choose B despite higher conditional risk. The retained
error metric alone omits costs of refusal and the additional correct service.
With wrong penalty-10: A380-200-60=120 (.120/request), B720-800-20=-100
(-.100/request); choose A instead. These are exact descriptive utilities on the
supplied set, not estimated deployment economic returns. Utility preferences and
realistic target-population frequencies must be specified prospectively.

## D

The1,000 labels were used to choose among50 thresholds: this is selection data,
not untouched test proof. Observed<=2% is not a population upper confidence bound,
and threshold selection adds optimism. Retain the table as honest descriptive
threshold fitting/exploration; the colleague's discard-all claim is too broad.
Freeze chosen policy, score mapping, threshold/tie handling, error labels and target
population now; evaluate once on a fresh independent representative labeled test set.
Report accepted count/total, errors/accepted and a prespecified confidence bound and
coverage. Determine sample needs from the2% target before collecting labels. If the
bound misses the target, record non-certification rather than tune on that test and
reuse it as untouched. Alternatively a prospectively justified uniform risk-control
procedure could account for selection, but this memo did not implement one and cannot
retroactively inherit the2017 SGR theorem merely by using thresholds. No demand to
throw away valid data, and no claim50 tests automatically create an exact correction
without assumptions.

## E

X coverage810/900=.90, risk81/810=.10, retained accuracy.90; correctly served729/900=.81.
Y coverage10/100=.10, risk1/10=.10, retained accuracy.90; correctly served9/100=.09.
Overall answered820/1000=.82, errors82/820=.10, correct738/820=.90; all-item
correct service738/1000=.738. Equal observed conditional accuracy hides an80-point
coverage gap and a72-point correct-service gap. It does not prove equal access,
safety or lack of disadvantage. Y has only10 answered cases, so equal point error
rates also do not imply equal population risks/precision. These tables do not tell
why coverage differs, counterfactual outcomes on refusals, error severity, causal
discrimination or which fairness rule should govern. Collect subgroup identities,
sample uncertainty, request/case mix, refusal consequences and relevant costs; avoid
turning descriptive disparity into a proved causal allegation.

## F

For fixed independently selected threshold and iid retained Bernoulli errors of
risk p, probability of observing zero errors in n=20 is(1-p)^20. Exact one-sided95%
upper limit solves(1-u)^20=.05, so u=1-.05^(1/20)=.13910834066826516, about13.91%.
Zero empirical error therefore certifies neither zero true error nor a2% risk target.
For the same zero-error design, at least ceil(log(.05)/log(.98))=149 accepted iid
items are needed for that upper limit to be<=.02. This is a planning calculation,
not an observed future result. An upper bound is a repeated-sampling coverage
statement, not a95% posterior probability that this particular p lies below it.
If the threshold was chosen on these labels, the fixed-threshold argument no longer
suffices; use independent testing or a justified selection-adjusted procedure. If
deployment shifts, the retained population changes, so the same bound does not transfer
without support. Explicitly one-sided95%, not the lane's distinct two-sided95% rule.

## G

All-abstain: coverage0/100=0; retained error0/0 is undefined, not empirical proof of
perfect conditional reliability. A software convention displaying0 must flag its
undefined/no-data meaning and not win a risk-only ranking. Other policy: coverage.50,
retained error5/50=.10, correct service45/100=.45. This is not enough for an absolute
best-policy choice: refusal and wrong-answer costs/constraints may differ. Report
counts, coverage, retained risk as NA when denominator0, correct/wrong service and
uncertainty as applicable. Let the user specify a risk/coverage constraint or utility;
do not invent a universal coverage minimum or refusal cost. Zero realized wrong
answers for all-abstain is true but distinct from zero conditional error risk.

## H

Accept the first memo as written. Coverage100/200=.50 for each, risks8/100=.08
versus12/100=.12, a4-point observed advantage for A at that coverage on the supplied
set. It explicitly avoids the unsupported inference. Equal counts do not imply
identical answered subsets; require per-item acceptance, correctness and sampling
structure (including clustering) for a dependence-aware comparison, and representative
sampling/uncertainty before population inference. Marginal counts alone do not identify
paired discordances or the exact paired uncertainty. More independent evaluation
would improve precision, but does not erase this descriptive result.
Reject second memo: source calibration alone does not ensure destination retained
risk at the same threshold. Unknown domains can shift correctness, confidence and
which requests are retained. Need target-relevant labeled validation or justified
transport assumptions, report shift and subgroup behavior; no known-OOD training
procedure establishes arbitrary future-domain guarantees by itself.

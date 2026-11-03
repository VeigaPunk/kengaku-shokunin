# FIRST ANSWER — binary-judge incident memo

Author /root/train_kengaku_round65; 2026-11-02. Manual reasoning only, before
private oracle release. Challenge SHA256
6cd43cfc7024a950f37cbf31490b7548f38530948437e27fc6d08eb65deb0064.
No calculator, code, analytical counter or model call.

## Decision

HOLD the announcement that A is better. Historic calibration conditionally
favors A, but B's current pilot changes the plug-in ranking. Neither calculation
establishes population superiority, drift, or a release margin. Same judge,
version and prompt are not evidence of equal conditional errors for differently
styled answers. Spend the offered budget on human adjudications, not another
100000 machine judgments: the named unknown is calibration/transport, which
more unlabeled verdicts cannot resolve. No real release is authorized here.

## Arithmetic and what it means

Let s=sensitivity, c=specificity, d=s+c-1, r=judge-positive frequency. From
total probability r=d theta+1-c. Thus theta=(r+c-1)/d for nonzero d.

Historic calibration: s=80/100=4/5, c=70/100=7/10, d=1/2.
A raw r=600/1000=3/5 gives (3/5-3/10)/(1/2)=3/5.
B raw r=450/1000=9/20 gives (9/20-3/10)/(1/2)=3/10.
Conditional plug-in contrast A-B=3/10. These are NOT human success counts
600 and300 out of1000, and are not exact population rates. Interpretation
requires historic class-conditional rates to apply to each system now.

Current B pilot: s=12/20=3/5, c=18/20=9/10, d=1/2.
Using B's r=9/20 gives (9/20-1/10)/(1/2)=7/10.
With A still conditionally at3/5, the contrast becomes -1/10. This exposes
sensitivity to calibration; it does not prove B wins or that conditional drift
has occurred. The B pilot has only20 observations in each human class, and A's
historic transport is itself unverified. Same1000 prompts establishes a matched
opportunity, not known outcome covariance. The briefing lacks joint labels and
paired judge overlap; do not invent a paired interval or treat systems as
independent merely because overlap is unavailable.

Possible-world demonstration, distinctly NOT pilot inference: suppose exact
current population rates were A(s,c)=(4/5,7/10), B(s,c)=(3/5,9/10), with true
prevalences A3/5, B7/10. Then A judge rate=(1/2)(3/5)+3/10=3/5, and B judge
rate=(1/2)(7/10)+1/10=9/20. A has higher raw score but lower human prevalence.
These exact values provide a counterexample to ranking solely by raw score when
conditional errors differ; finite pilot fractions do not establish this world.

The second inspection reverses the conditioning:18/20=P(Y=1|J=1) estimated
on inspected judge-positive B outputs (PPV), and8/10=P(Y=0|J=0) on inspected
judge-negative outputs (NPV). Neither is s nor c. The selection mechanism and
inclusion fractions are unavailable; do not pool its30 cases with the
human-class-stratified pilot to invent ordinary confusion denominators. These
inspection fractions are descriptive for those cases, not automatically
representative even within judge strata. Representative random sampling within
judge strata plus known target stratum masses could support an appropriate
weighted design, but the briefing does not give that selection guarantee.

## Diagnostic cards

**S — singular, not unbiased.** s=7/10,c=3/10,d=0; predicted r=7/10 for every
theta. For example theta=1/5 and theta=4/5 both fit the same exact r=7/10.
Raw bias r-theta is respectively1/2 and-1/10. It vanishes only at theta=7/10,
not for every prevalence. More judge-only outcomes cannot identify theta under
this model. Representative human labels of target outputs can estimate theta
directly; alternatively a demonstrably informative, recalibrated judge under a
valid transport design can change the measurement model. Extra calibration of
this already-known singular matrix does not restore its information.

**N — ill-conditioning plus compatibility.** s=51/100,c=1/2,d=1/100.
The population feasibility interval is[1/2,51/100]. Exact r=.505=101/200 gives
theta=(1/200)/(1/100)=1/2. Exact r=.515=103/200 gives theta=3/2, outside[0,1],
so that exact population rate is incompatible with the specified exact matrix.
But103/200 as a SAMPLE judge frequency can occur with a feasible population
rate; it is not algebraic disproof of that population model. Report the
out-of-range plug-in3/2 and assess the sampling design/uncertainty, not clip to1
and call it validated. Clipping is a transformation, not evidence. Sensitivity
to r is1/d=100: a .005 change changes the inverse by .5. Operationally require
much stronger precision/transport evidence or use direct human assessment; do
not claim a tiny raw-score difference is a stable corrected ranking. No precision
target or required sample size can be invented from this briefing.

**R — negative does not mean singular.** s=1/5,c=3/10,d=-1/2.
For exact r=3/5, theta=(3/5+3/10-1)/(-1/2)=1/5, feasible. The compatibility
interval is[1/5,7/10]. With this SAME fixed matrix across populations, higher
raw r means lower theta; if matrices differ this simple ranking rule fails.
For prospectively reversing J to1-J, new s'=4/5,c'=7/10,d'=1/2,r'=2/5;
new inverse=(2/5+7/10-1)/(1/2)=1/5. Preserve both original and reversed coding,
recalibrate and freeze coding before comparisons; do not select the coding that
flatters a system. This is elementary algebra. Lee §5 explicitly assumes
q0+q1>1 for its stated inversion analysis; the negative-d extension is not
misattributed to that theorem or its finite-sample uncertainty claims.

## Bounded repair and announcement conditions

Use60 human adjudications as follows: draw30 prompt IDs uniformly without
replacement from the complete original1000-prompt roster; adjudicate BOTH saved
system outputs for each selected prompt (30 pairs,60 output judgments). Preserve
existing machine verdicts and exact prompt/output identities. Blind human
reviewers to system IDs and judge verdicts where feasible, use the same frozen
binary rubric and a predefined disagreement/adjudication protocol, and retain
all results. Interpret60 as output adjudications, not a guarantee that unresolved
cases need no further person-time. If that budget cannot implement the protocol,
record unresolved labels and HOLD rather than inventing truth or silently
substituting easy examples. Recover full original paired machine verdicts from
logs if available; do not regenerate answers or discard failures.

This is a concrete representative paired audit, not an optimal allocation or
power guarantee. Human-positive/negative class counts will be random, not
assumed30/30; if a class is absent or scarce, record that limitation and request
a separate authorized continuation rather than manufacture a sensitivity or
specificity. Diagnose B's long-answer error behavior and verify A's transport;
retain style attributes for analysis but do not post-hoc tune a favorable subset.
Keep historic and pilot calibration results separately labeled. If the first1000
prompts themselves are nonrepresentative or family-clustered, the audit does not
remove that defect.

After the bounded audit, report paired human outcomes, supported conditional
error estimates with their denominators and design-aware uncertainty, and the
unresolved transport/coverage questions. Do not automatically pool calibration
and evaluation samples or use an independence formula when the audit overlaps
the evaluated set. Separate finite1000-prompt inference from target-population
transport. Freeze an actual practical margin/error policy before any new
confirmatory assessment; none is supplied here. An announcement needs valid
comparison uncertainty and target relevance, not just an inverse inside[0,1].
If the available sample cannot meet the later justified decision requirements,
report inconclusive and retain HOLD. Never present corrected fractions as
binomial data for an ordinary exact CP test. Q11 is not discharged by this memo.

## Reusable checklist

Freeze target/rubric and human adjudication; retain2x2 tables with human-class
denominators and selection design; inspect d and population-vs-sample
compatibility; distinguish prior shift from conditional drift; avoid PPV/NPV
substitution; preserve pairs and test/calibration dependence; choose repair that
addresses the actual unknown; include both uncertainty sources; retain old
results and preregister the new decision; HOLD unsupported rankings.

## Dated correction to append, preserving old digest

2026-11-02 round65: supersedes the old `llm-judge-calibration.md` falsifier
claim that sens+spec=1 makes the bias term zero and reduces the problem to
ordinary binomial uncertainty. At that sum, the judge-positive population rate
is1-specificity regardless of human prevalence: prevalence is unidentifiable
from judge frequency. Raw bias can be zero at one coincidental prevalence, not
generally. Only sensitivity=specificity=1 gives raw unbiasedness for every
prevalence. Also narrow the digest's distribution-shift sentence to stable
class-conditional judge errors (§8); estimated calibration rates do not confer
exact finite-sample unbiasedness (§5). The original wording remains for audit.

## Primary support and source authority

Lee et al., ICML2026/PMLR306, retained original
corpus/evidence/round65/sources/lee2026.pdf: §3 p3 defines human-reference and
class-conditional rates, footnote2 requires resolved human disagreement;
§4.1 p4 eq4 known-rate inverse and eq5 plug-in; §4.2 p4 both uncertainty
sources; §5 p5 eq9 total-probability identity and positive-d condition, followed
by explicit finite-calibration bias; §8 p8 states stable P(J|Y) across test and
calibration, Table2 p9 distinguishes conditionals and priors. Card deductions,
compatibility interval and bounded audit design are reasoning from that model,
not source-reported experiments or optimal-allocation claims. Primary paper
self-reports its empirical results; none is independently replicated here.

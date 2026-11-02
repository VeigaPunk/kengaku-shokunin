# Round63 manual answers — before oracle release

Author /root/train_kengaku_round63; 2026-11-02. Questions sha256
 a314f97aaeb99008c8bc9d52be9763fd5dff5638c7f786330cd27c05bc175863.
All arithmetic below hand-derived. No script, R execution, calculator, fixtures,
or private oracle consulted. Threshold1/20 inclusive. Vectors in original order.
H3=11/6; H4=25/12; H5=137/60. Source/formula freeze3bfa5bd97fc64227201264f328373a934c72deb6.

| Case | Holm adjusted | Holm rejects | BH adjusted | BH rejects | BY adjusted | BY rejects |
|---|---|---|---|---|---|---|
| C1 | (3/100,2/25,2/25) | A | (3/100,41/1000,41/1000) | A,B,C | (11/200,451/6000,451/6000) | none |
| C2 | (9/100,9/100,9/100) | none | (49/1000,49/1000,49/1000) | A,B,C | (539/6000,539/6000,539/6000) | none |
| C3 | (3/25,1/250,3/25,1/5) | B | (4/75,1/250,4/75,1/5) | B | (1/9,1/120,1/9,5/12) | B |
| C4 | (1/20,3/40,3/40,3/40) | A | (1/20,1/20,1/20,1/20) | A,B,C,D | (5/48,5/48,5/48,5/48) | none |
| C5 | (3/200,1/25,1/25) | A,B,C | (3/200,3/100,1/25) | A,B,C | (11/400,11/200,11/150) | A |
| C6 | (3/50,4/5,9/10,9/10,9/10) | none | (3/50,1/2,1/2,1/2,1/2) | none | (137/1000,1,1,1,1) | none |

## Arithmetic working and decisive distinctions

C1: sorted input already. Holm rank products .03,.08,.041 become .03,.08,.08
by prefix maxima. BH products .03,.06,.041 become .03,.041,.041 by suffix minima.
Raw products violate adjusted-p monotonicity and lose the step procedure's logic;
particularly raw Holm .041 at rank3 would falsely reject C after rank2 fails.
Multiply BH adjusted values by11/6 (no clipping here) for BY.

C2: Holm raw products .09,.08,.049; prefix maxima all .09. Rank1 fails .05/3,
so Holm rejects none. BH raw products .09,.06,.049; suffix minima all .049.
Rank3 .049<=.05 qualifies, so BH rejects all3 despite rank1 .03>.05/3.
Stopping BH at the first missed local threshold is wrong. BY multiplies .049
by11/6 ->539/6000>.05, rejects none.

C3: sorted B,A,C,D (A/C tied, interchangeable within their block). Holm products
.004,.12,.08,.2 ->.004,.12,.12,.2. BH products .004,.08,4/75,.2
->.004,4/75,4/75,.2. BY multiply by25/12 ->1/120,1/9,1/9,5/12.
Restore A,B,C,D as table; ties receive same values, not different significance.

C4: Holm raw products1/20,3/40,3/40,1/20, so last inherits3/40.
A exactly meets alpha/4=1/80; B fails alpha/3=1/60. Only A rejected.
BH all raw products equal1/20 and rank4 exactly meets q, so all reject.
BY each becomes(1/20)(25/12)=5/48. Equality counted as reject, no rounding.

C5: Holm products .015,.04,.04, already monotone. BH products .015,.03,.04,
already monotone. BY multiply by11/6, yielding the table. Holm strong FWER and
BY FDR guarantees are licensed for stipulated valid null marginals and arbitrary
dependence. BH arithmetic is valid as arithmetic, but nominal FDR control is
NOT established by shared tasks; independence/PRDS cannot be inferred. Rejection
labels in its column describe its mechanical decisions only, not justified claims.

C6: Holm products .06,.8,.9,.8,.5 ->prefix .06,.8,.9,.9,.9.
BH products .06,.5,.5,.5,.5 ->unchanged. H5=(60+30+20+15+12)/60=137/60;
BY first=.06*137/60=137/1000; others137/120>1 clipped to1. No rejection.
False singleton uses m=1,H1=1: all methods give A=3/250<1/20 and reject A.
Selection does not license that smaller family: A was chosen as the best of5,
not independently prespecified as the sole contrast. The input null p-value's
validity for a fixed contrast is not a guarantee for the selected minimum.

## C7 — error targets

V counts false null rejections, R all null rejections. FDP=V/R if R>0, and0
when R=0. FDR=E[FDP]; FWER=Pr(V>=1). Neither assertion follows. A bound on an
expectation of a proportion is not a bound on the chance of any error or every
realized proportion, nor a posterior probability conditioned on these four
rejections. For illustration, a hypothetical procedure has R=4 always and V=1
with probability1/5, V=0 otherwise: FDR=(1/5)(1/4)=.05 but FWER=.20 and the
bad realizations have FDP=.25. This is a logical counterexample about error
metrics, not an empirical experiment or claim that a specific procedure realizes
it. If all nulls were true, FDP=1 on any rejection, giving FDR=FWER specially;
that condition was not supplied.

## C8 — lack of rejection is not equivalence

Adjusted p=.30 does not reject the specified difference null at .05. The interval
[-.20,.30] is compatible with harms/improvements much larger than .05 and zero;
it is not contained within [-.05,.05]. Neither equivalence nor absence of a
meaningful improvement is established. Need a prospectively justified margin,
explicit equivalence (or noninferiority, if that is the actual goal) hypotheses,
appropriate paired/cluster-aware design, sufficient precision/power, correct
one-/two-sided confidence level and multiplicity handling. A suitable equivalence
procedure could establish equivalence when its compatible interval lies wholly
within the margins. Do not attach posterior probabilities to p=.30 or decide
which side/design retrospectively to obtain a desired answer.

## C9 — pseudoreplication is upstream of multiplicity

BY cannot repair invalid marginal p-values caused by pretending500 generations
are500 independent tasks. Define the estimand first: equal-weight performance
difference across these five fixed tasks differs from performance on a broader
task population. For the latter, task is a primary sampling/cluster unit; repeats
within task estimate generation randomness and are nested observations, with
matched outcomes retained where actually paired. Need task sampling justification,
valid task/cluster-aware inference (only five clusters is a severe precision and
method-validity limitation), and honest assumptions about dependence within/across
runs. For the fixed suite, one can analyze conditional generation variability
with its actual dependence design, but cannot infer all-task transport from that.
BY controls multiplicity only once individual null p-values satisfy validity; it
changes neither the target population nor representativeness of these five tasks.

## C10 — selected reports do not reset the family

Declaring the three selected values a new confirmatory family is insufficient;
selection occurred after the six-hypothesis family was inspected. Without the
full vector, exact Holm/BH/BY adjusted vectors and rejection sets generally cannot
be reconstructed: omitted values can alter ranks, prefix maxima, suffix minima
and the selected cutoff. Special trivial cases can be decidable, but no general
unique reconstruction follows. With known original m=6 and valid original
marginals, conservative Bonferroni adjusted values min(1,6*p) for each reported
contrast are computable without missing values; this is a different, explicitly
labelled procedure, not reconstruction of Holm/BH/BY or the full rejection set.
Defensible path: recover/disclose all six original p-values, hypotheses and search
history, apply the prespecified full-family rule and label selected narrative as
exploratory. If unavailable, retain m=6, disclose missingness and limits rather
than invent exact results. Genuine prospective confirmation requires a frozen
new family/design, error target/method and independent untouched evaluation data
(or another inference design explicitly valid for reuse/selection), adequate
power and valid tests. Merely rerunning the correction on the same selected values
is not independent validation.

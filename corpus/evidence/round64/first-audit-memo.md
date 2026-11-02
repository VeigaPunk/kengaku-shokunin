# First audit memo — frozen fictional panel

Author /root/train_kengaku_round64, 2026-11-02. Manual derivation only, before
private-oracle release. Brief SHA256
cf62c6600c2f988f129aa8cac3d735b87daaccb69c61994ec78d1675d6608c45.
B is candidate, A incumbent: all improvements below are B-A, not proposal's
illustrative A-B orientation. No API calls or numerical execution.

## Recommendation

HOLD any population release: no transport or sampling-uncertainty evidence exists.
For the original finite panel, HOLD robust GO: costs qualify, but admissible
missing-outcome completions include both substantial harm and benefit. Recover
authenticated original logs first. In the specified all-logs-recovered scenario,
GO is justified ONLY for the fictional finite-panel screen at the original
Easy1/4 mixture: improvement7/100 exceeds1/20 and cost21/4 is below27/5.
This does not authorize deployment or satisfy Q11 population-rate admission.

## 1. The two manager arguments change denominators

A completed successes=(72+18)=90, completed attempts80+60=140:9/14.
B completed successes=38+42=80, completed attempts40+90=130:8/13.
9/14>8/13 since117>112 after multiplying by182. Pooled completed records favor
A, descriptively. But A's completed sample contains Easy share4/7, B's4/13.
Those are neither the common assigned distribution nor the target1/4.

Within families: A Easy72/80=9/10; A Hard18/60=3/10.
B Easy38/40=19/20; B Hard42/90=7/15. B is descriptively higher in both.
Common target complete-case A=(1/4)(9/10)+(3/4)(3/10)=9/20.
B=(1/4)(19/20)+(3/4)(7/15)=19/80+28/80=47/80.
B-A=47/80-36/80=11/80. The pooled-vs-family reversal is a Simpson-type
composition reversal; it is not an arithmetic inconsistency. Common weights
remove that composition difference but not selection within each family. Neither
“reject B” nor “ship B” follows for assigned outcomes or deployment: differential
unknowns have no justified missingness mechanism. Complete-case rates describe
the outcomes we happened to observe, not the unknown outcomes.

## 2. Sharp finite-panel bounds and policy

For n100, bounds are successes/100 through(successes+unknown)/100:
A Easy[72/100,92/100], Hard[18/100,58/100].
B Easy[38/100,98/100], Hard[42/100,52/100].
A target lower=72/400+54/400=126/400=63/200;
upper=92/400+174/400=266/400=133/200.
B target lower=38/400+126/400=164/400=41/100;
upper=98/400+156/400=254/400=127/200.
B-A lower=82/200-133/200=-51/200;
upper=127/200-63/200=64/200=8/25.

These bounds are sharp: for minimum contrast, every unknown B outcome is0 and
every unknown A outcome1; for maximum reverse those assignments. Each satisfies
the supplied counts. Shared prompt IDs do not require the systems' successes
to match. No joint constraints on unknown outcomes were given. The lower bound
is below1/20, so robust finite-panel GO is not established. This is not proof B
fails every completion; the upper bound allows success. No confidence level is
attached. Sampling uncertainty about new requests is an additional problem.

Known deadlines remain observed failures, including A's3+12 and B's1+20 deadline
subsets. Later correctness does not make success-by60seconds unknown. Lost logs
are genuinely unknown under this brief. Their compute costs nevertheless count.
A cost per assigned Easy=200/100=2, Hard=400/100=4;
target=(1/4)2+(3/4)4=7/2.
B cost per assigned Easy=3, Hard=6;
target=(1/4)3+(3/4)6=21/4=5.25<=27/5=5.4.
Use total attempts, not completions or successes, as the cost denominator.

## 3. Authentic original-log recovery

Recovered successes A Easy72+10=82, Hard18+12=30;
B Easy38+12=50, Hard42+8=50; all denominators remain100.
A target82/400+90/400=172/400=43/100.
B target50/400+150/400=200/400=1/2.
Improvement=1/2-43/100=7/100>=1/20. Original costs unchanged, so finite-panel
GO at w1/4. Recovery collapses identification uncertainty for this fixed panel;
it neither creates random sampling nor proves within-family transport. Population
HOLD remains. No90-second responses have been rescored as60-second successes.

## 4. Alternative-use-case weight sensitivity, after recovery

A(w)=(82/100)w+(30/100)(1-w)=3/10+(13/25)w.
B(w)=1/2. Difference D(w)=1/5-(13/25)w.
Ranking equality D=0 occurs at w=5/13; B ranks above A below5/13.
The entire stated range[1/5,3/10] is below5/13: ranking never reverses inside it.
But the policy asks for a minimum margin, not mere positive ranking.
D>=1/20 gives(13/25)w<=3/20, hence w<=15/52.
B cost C(w)=3w+6(1-w)=6-3w.
C<=27/5 gives w>=1/5. Intersection with the given range:
**w in[1/5,15/52]**, inclusive because both policy comparisons are inclusive.
At w1/5, D=12/125 and cost27/5: eligible exactly at cost boundary.
At w3/10, D=11/250<1/20 while cost51/10<27/5: not eligible because margin
fails, despite positive ranking and lower cost. Thus GO is not robust across the
entire alternative-use-case interval. The original w1/4 is in the eligible set.

With ceiling5.0, C<=5 gives w>=1/3. That is outside[1/5,3/10], so no supplied
mixture is feasible. Indeed even without restricting to the stated interval,
w>=1/3 and w<=15/52 have empty intersection. More Easy lowers cost but erodes
B's improvement because A is much stronger on Easy after recovery. This is an
explicit quality/cost tradeoff, not a license to choose favorable weights.
An alternative use case may legitimately have different prospectively grounded
weights; selecting weights after these results to justify the preferred model
invalidates the claimed target decision and must be labeled exploratory.

## 5. Smallest defensible repair and stopping conditions

First recover original outcome evidence, preserving attempt IDs, timestamps,
deadline, system/grader pins and all cost records. The counterfactual supplies
exactly that repair; no extra generation is necessary to decide its finite panel.
Before recovery, prioritize evidence that can shrink the decision-relevant
identified set, but do not promise that an unspecified subset of logs suffices.
Original logs are preferable to replacement samples when the question is the
original missing outcomes. If logs cannot be recovered, retain the bounds or
state a substantively justified sensitivity model, never pretend missing-at-random.

Reject converting known late-correct failures into unknown: it changes the endpoint
and widens a bound by discarding known information. A longer deadline can define a
new, prospectively specified evaluation, applied symmetrically and reported apart.
Reject dropping unknowns: it conditions on selected observed records. Reject
rerunning only B's failures until pass: it changes attempt budget and selection,
loses original failures, and makes comparison unfair. A valid new retry-policy
evaluation fixes retry/timeout rules prospectively for both systems, retains every
attempt and cost, and measures the revised system separately.

Conditional GO: recovered panel at w1/4 under ceiling5.4, only fictional panel
eligibility. It flips to HOLD if authenticated recovery is not established, if
true policy/weight differs, or if the declared bound/ceiling condition fails.
HOLD: original robust panel; it can flip after authentic recovery that establishes
both criteria (the supplied recovery does). Another HOLD: recovered alternative
range robust GO, because w3/10 violates margin; a legitimately narrowed target
range contained in[1/5,15/52] or new policy authority could change that panel
screen, but selecting such range after results does not validate prior release.
Population HOLD flips only with appropriate transport/representativeness,
valid outcome and identity audit, design-matched uncertainty meeting the stated
risk criterion (including Q11 where applicable), and authorized decision-making.
No blind sample-size guarantee is possible without variance/design/target data.

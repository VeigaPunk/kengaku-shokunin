source: S037 — `python3 plans/attrib_calibration.py --summary` (own-work, offline gate output over the nine committed r21–r23 receipts); S030 — https://jhanley.biostat.mcgill.ca/c607/ch08/zero_numerator.pdf — p.1 "Making Inferences: The Rule of Three"; S027 — https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html — Parameters → method → 'exact'; S028 — https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html — Notes ¶1–2; S029 — https://doi.org/10.1214/ss/1009213286 — Abstract p.101; S011 — https://proceedings.mlr.press/v306/lee26bl.html — §4.1 eq. (4), §4.2 eq. (5)–(8), §5.2; S033 — https://doi.org/10.1093/oxfordjournals.aje.a112510 — Abstract; S034 — https://doi.org/10.1016/j.prevetmed.2013.09.015 — Abstract; S036 — corpus/evidence/attrib-r23-stream.log:239
verified-at: 2026-10-20
recheck: 90d — re-run `python3 plans/attrib_calibration.py --summary` and `--selftest` (exit 0), `sh plans/fixtures/r25/attrib_oracle.sh --intervals` (exit 0, same verdicts), and re-open S027/S028 on-release; recheck immediately when a new attribution receipt lands (it is outside the frozen P1 manifest and the instrument will flag it)

# Attribution-instrument interval calibration (round 25)

## Claim

Every stored verdict of the lane's blind route-leg attribution instrument
(`plans/attrib_probe.py`, rounds 21–23) is a point fraction against bar 0.80
with a min-n rule. Re-derived offline with exact two-sided 95% Clopper–Pearson
intervals and the pre-registered rule (PASS iff lower ≥ bar, FAIL iff
upper < bar, INDETERMINATE otherwise, UNTESTED iff n = 0;
`plans/round-25-claims.md`), the four unique scored samples (92 trials, 92
correct) keep their overall-accuracy PASS, but one stored PASS does not
survive and two stored FAILs were never tests:

| receipt (authoritative block) | stored line | stored | interval (CP95) | re-verdict |
|---|---|---|---|---|
| `attrib-r21-impl-ds-trials.log:268-312` | ACCURACY 20/20 | PASS | [0.831567, 1] | PASS |
| `attrib-r21-impl-glm-trials.log:142-188` | ACCURACY 22/22 | PASS | [0.845627, 1] | PASS |
| `attrib-r22-opencode-trials.log:204-254` | ACCURACY 20/20 | PASS | [0.831567, 1] | PASS |
| `attrib-r22-opencode-trials.log:204-254` | TARGET hyper 10/10 | PASS | [0.691503, 1] | **INDETERMINATE** (needs n ≥ 17 at zero errors) |
| `attrib-r22-opencode-trials.log:204-254` | TARGET opencode-go 0/0 | FAIL | — | **UNTESTED** |
| `attrib-r23-stream.log:258-320` | ACCURACY 30/30 | PASS | [0.884297, 1] | PASS |
| `attrib-r23-stream.log:258-320` | STREAM TARGET opencode-go 0/0 | FAIL | — | **UNTESTED** |

`attrib-r22-legs.log:312-362` has a trial table identical to the r22-opencode
block and is counted once under the frozen rule; its request windows and
pins differ, so the instrument prints a pooled-if-distinct sensitivity line
(40/40, CP95 [0.911903, 1]) with no verdict credit. Per-leg: of 12 recall
estimates, 2 PASS (r21 alibaba 20/20, r23 hyper 24/24), 5 INDETERMINATE
(devin 9/9, zai 13/13, r22 alibaba 10/10, r22 hyper 10/10, r23 alibaba 6/6),
5 UNTESTED (0 GT trials). A leg never observed in GT has an
unidentified share bound: the Rogan–Gladen bound is [0, 1] for every
opencode-go share although its observed share is 0/20 and 0/30.

Counting command: `python3 plans/attrib_calibration.py --summary` →
`TOTAL … unique_samples=4 duplicates=1 scored_trials=92 correct=92 incorrect=0
estimates=35 PASS=12 FAIL=0 INDETERMINATE=11 UNTESTED=12 … stored_verdicts=7
transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 stored_checks=119
mismatches=0` (2026-10-20). A second parser written independently in POSIX
sh+awk (`plans/fixtures/r25/attrib_oracle.sh --intervals`) reproduces the
same samples, duplicate, and transitions.

## Evidence

- Zero numerators are not zero rates. S030, p.1 "The Rule of Three": "we can
  be 95% confident that the chance of this event is at most three in n (ie,
  3/n)". Read at this bar: 10/10 correct bounds the error rate near 0.30 —
  the exact two-sided bound is 1 − 0.691503 = 0.308497.
- The exact interval is the documented reference. S027, `proportion_ci`
  Parameters → method: "'exact' : Use the Clopper-Pearson exact method [1]."
  S028, Notes ¶1: "Beta, the Clopper-Pearson exact interval has coverage at
  least 1-alpha, but is in general conservative."
- At a boundary the central interval is one-sided in effect. S028, Notes ¶2:
  "the coverage will be only 1 - alpha/2 in the case of “beta”" when count is
  zero or equals nobs — every stored verdict here sits on that boundary.
- Point and Wald readings mislead at small n. S029, Abstract ¶1: "chaotic
  coverage properties of the Wald interval are far more persistent than is
  appreciated"; Abstract ¶2 recommends Wilson or Jeffreys for small n — so
  the Wilson column is printed as a sensitivity check, never as the verdict.
- Observed positive shares are biased when the test is imperfect. S033,
  Abstract: the "frequency of positive tests is shown to be a bad estimate,
  and the necessary adjustmants are given." The adjustment used is S011's
  form: §4.2, eq. (5): "Substituting estimates q̂1 and q̂0 into (4) gives the
  bias-corrected estimator (Rogan & Gladen, 1978; Lang & Reiczigel, 2014)."
- S011's own interval is not exact. §5.2: it constructs "a confidence interval
  for θ using the "add two successes and two failures" adjusted Wald approach".
  S034, Abstract, proposes approximate limits "when sensitivity and specificity
  are estimated from independent samples". The lane's bound instead takes the
  worst corner of the CP-lower-bound box (conservative, not coverage-exact).
- Own-work: the stored `STREAM TARGET opencode-go … -> FAIL` at n = 0 (S036,
  `attrib-r23-stream.log:239`) is a coverage refusal, not an accuracy test;
  under the interval rule it is UNTESTED.

## What this does not establish

- **Trials are not independent bodies.** Each block's n is repeated sends of
  1–3 prompt bodies (`bodies=1..3` in the instrument output, flagged
  `iid-fragile`). The CP interval is trial-level; at cluster level (m ≤ 3) no
  block could PASS. The overall PASSes are PASSes for this protocol's repeated
  bodies, not for a population of prompts (S015's clustered-error warning,
  `corpus/knowledge/paired-eval-uncertainty-reporting.md`).
- **GT is a journal join, not human labels.** S011's guarantee assumes a
  human-labelled calibration set; here GT comes from shim journal windows that
  also carried other traffic (request lines 37–160 for 20–30 trials). Any GT
  join error is invisible to the interval.
- **One-vs-rest specificity is derived**, marginal per leg, not simultaneous;
  a single misattribution would move two legs' denominators.
- **The r22 dedup may undercount.** The frozen row-equality rule merged two
  executions with disjoint request windows; the pooled 40/40 line shows what
  counting them separately would give. No verdict rests on that line.
- Rogan–Gladen full text and Clopper & Pearson (1934) were not openable this
  round (publisher 403); the formula is grounded on S011 eq. (4)–(5) only.
- Falsifier: any scored trial marked `NO` in a future receipt, or a receipt
  showing within-body YES/NO heterogeneity, changes the zero-error reading;
  the instrument's `--selftest` R1/R1b fixtures show it then exits 1 or moves
  the verdict.

## Extends

Extends `corpus/knowledge/attrib-r21.md` (its descriptive Wilson intervals at
`:139,154,156` carried no verdict and no per-leg bound) and
`corpus/knowledge/llm-judge-calibration.md` (the S011 correction applied to the
lane's own instrument rather than a judge). New coverage-map row:
`Instrument interval calibration`.

## How kengaku applies it

| Situation | Do | Don't |
|---|---|---|
| A pass bar on a binary accuracy | PASS only if the exact CP95 lower bound ≥ bar; print n needed (17 / 26 / 34 for 0 / 1 / 2 errors at 0.80, `plans/fixtures/r25/power_table.tsv`) | Accept a point fraction plus a min-n gate (10/10 at min-n 10 is INDETERMINATE) |
| A leg or target with 0 GT trials | Report UNTESTED | Report FAIL (a refusal is not a measurement) |
| Reporting a leg share | Report the Rogan–Gladen bound with its Youden lower bound; [0, 1] when unidentified | Report the observed share as the true share |
| Repeated sends of a few prompt bodies | Print `bodies=m`, call the PASS protocol-level | Read trial-level n as prompt-population n |

## Rejected

- **Rule of three as the verdict rule.** Rejected: it approximates a one-sided
  95% bound and would PASS 15/15 and 16/16 at bar 0.80 where the frozen
  two-sided CP rule is INDETERMINATE (`plans/fixtures/r25/power_table.tsv`).
  Flip: an operator ruling that one-sided bounds suffice for lane gates.
- **Prediction-powered inference (S035) as the correction.** Rejected for this
  entry: its scope is means, quantiles and regression coefficients, not
  classifier sensitivity/specificity. Flip: a PPI variant for misclassified
  multiclass labels.

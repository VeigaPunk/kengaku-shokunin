# ExecKS — KS-band edge and forgery pass rates (round 99, C1/R99-C1 mechanism)

Seat: ExecKS. Hypothesis: 'the grader's KS rule (scipy.stats.kstest, p >= 0.001, n = 10000)
passes a normal quantile grid shifted by up to about 0.048 sd and fails above it, and a
seeded random draw from the exact target normal (the C03 marginal-only forgery) passes
in >= 99.8% of seeds'.

Axes: (1) determinism — seeded masks sampling noise for the gap cases; (2) tightness —
the KS verdict band on a mean-shifted marginal; (3) honest pass rates — the counter's
single-seed cases (C03 seed 3, C11/C12 grids) stated relative to the seed population.

## Method (grader-faithful, in the grader venv)

Venv: `uv venv -p 3.13 G && uv pip install --python G/bin/python pytest==8.4.1 pandas==2.3.2
scipy==1.16.1` → python 3.13.16, pandas 2.3.2, scipy 1.16.1, pytest 8.4.1, numpy 2.5.4
(the C1 probe's pins). Grader rule reproduced exactly as `test_sampled_data`:
`kstest(D, "norm", args=(true_mean, true_std))`, `p >= 0.001`, true_mean =
-12.2965135 + 0.5495886 * 50.47989 = 15.446658573253998, true_std =
((0.5495886**2) * 10.68515**2 + 14.0916**2)**0.5 = 15.266260266516712, n = 10_000.
Grid: `norm.ppf((arange(10000)+0.5)/10000) + k` (the builder's construction at T).
Random draws: `numpy.random.default_rng(seed)`. Maintainer process: the fitted Gaussian
CPDs recovered by OLS on the committed `bn_sample_10k.csv` (U: 50.47989/10.68515; D:
-12.2965135/0.5495886/resid-sd 14.09165 — matching the grader constants to ~1e-5),
intervened exactly as `modify_bn.R` (drop U->Y, do(Y=0), Y~N(0,1e-9) ≈ 0). Script =
`.ufo/waves/round-99/w1/ExecKS/ex.py`, output `out.txt`. C1/C2 frozen counters re-run
at T from a `git clone --shared` checkout detached at
f72a8bc710b12473b5c768004e2581f980d924f4 (top-level verified): both `pass`, receipts in
`c1-receipt.txt` / `c2-receipt.txt`.

## Results

### 1. Quantile-grid pass/fail edge (bisection, p >= 0.001 rule)

Bisection on k over [0.045, 0.050] to 4e-5 sd:

| k (sd) | KS p | verdict |
|---|---|---|
| 0.0450 | 0.003028 | pass (C11 ✓) |
| 0.0480 | 0.001242 | pass |
| 0.048672 | 0.001010 | pass |
| 0.048691 | 0.001003 | pass |
| 0.048711 | 0.000997 | fail |
| 0.0500 | 0.000664 | fail (C12 ✓) |

**Edge = 0.04869 sd** (passes ≤ 0.048672, fails ≥ 0.048711, bracket width 3.9e-5 sd),
where Φ(edge) − 0.5 = 0.019417. Consistent with the builder's statistic
Φ(k) − 1/2 (+1/2n) and with scipy's asymptotic p-value at the 0.001 threshold for
n = 10 000. For context, a *random* draw at the same shifts passes only 30.5% of seeds
at 0.045 sd and 21.5% at 0.050 sd (200 seeds) — the deterministic grid is what makes
C11/C12 reproducible; at 0.03 sd a random draw passes 75.5% (151/200, consistent with
the builder comment's 49/200 fail).

### 2. C03 marginal-only forgery pass rate (seeded, 2000 seeds)

D ~ `default_rng(seed).normal(true_mean, true_std, 10000)` — exactly the C03 case shape
(U,R,Y,M = 0.0): **1998/2000 = 99.900%** pass. Failing seeds: 752, 1837 (both p < 0.001).
Seed 3 (the replay's frozen seed) passes, reproducing the C03 `...,P,1` leg. The
residual 0.1% is the KS test's own type-I rate at α=0.001 — a correct-marginal draw
fails ~1/1000 seeds by construction of the test, independent of the forgery.

### 3. Maintainer-solution process pass rate (seeded, 2000 seeds)

Hierarchical intervened draw (U → R,M / Y=0 → D): **2000/2000 = 100.000%** pass. The
committed maintainer sample at T also passes (p = 0.2907, `fails.txt`). Note this is
structurally higher than the marginal-only rate: the exact marginal is a true-Normal
mixture in both constructions, but the hierarchical draw's empirical KS statistic
fluctuates less here — empirically 0/2000 failures vs 2/2000 for the i.i.d. marginal.
(One reading: both are the same marginal law; two Bernoulli trials at p≈0.001 with
2000 draws is weak evidence, not a mechanism difference. The 100% is "no observed
failure", not a proof of immunity.)

## Verdicts

| id | verdict | evidence |
|---|---|---|
| H-EDGE (grid shift edge ≈ 0.048 sd) | **holds** — measured edge 0.04869 ± 0.00004 sd, bracketed by C11 (+0.045 pass) and C12 (+0.050 fail) | `.ufo/waves/round-99/w1/ExecKS/out.txt`, `ex.py` |
| H-MARGINAL (C03 forgery pass rate ≥ 99.8%) | **holds** — 1998/2000 = 99.900%; only the KS test's intrinsic α=0.001 type-I rate keeps it from 100% | `.ufo/waves/round-99/w1/ExecKS/out.txt`, `fails.txt` |
| H-MAINTAINER (solution process pass rate) | measured **2000/2000 = 100%**; committed sample p=0.2907 passes | `.ufo/waves/round-99/w1/ExecKS/out.txt`, `fails.txt` |
| R99-C1 frozen predicate @ T | **pass** (11/11 legs, 13×10 legs, 0 mismatches, executed 43, file-artifact 34) — re-run, not re-asserted | `.ufo/waves/round-99/w1/ExecKS/c1-receipt.txt` |
| R99-C2 frozen predicate @ T | **pass** (K1=pass…K7=pass, pop=12 cleared=12, GATE 45→33) — re-run, not re-asserted | `.ufo/waves/round-99/w1/ExecKS/c2-receipt.txt` |

Scoping notes: the checklist rows above are re-executions of the frozen counters at T
for falsification only — predicates, counters and kill rules were not edited (no
production edits; detached clone). C01's positive control passing in the replay
(maintainer sample p = 0.2907 ≥ 0.001) agrees with the 100% maintainer-process rate.
No tools installed beyond the spec'd venv (uv-provided 3.13.16, pytest 8.4.1,
pandas 2.3.2, scipy 1.16.1, numpy 2.5.4). Scratch removed after receipts copied;
clone detached at f72a8bc710b12473b5c768004e2581f980d924f4, probe sha afacbf81… and
solution sample sha 982a7441… verified against the frozen table.

Report: .ufo/waves/round-99/w1/ExecKS.md

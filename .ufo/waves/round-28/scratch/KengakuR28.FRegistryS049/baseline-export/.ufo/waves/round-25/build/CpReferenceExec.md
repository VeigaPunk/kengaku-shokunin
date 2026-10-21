# R25 CpReferenceExec: independent exact Clopper–Pearson reference (C1 novelty)
Seat KengakuR25.CpReferenceExec (writer, leaf). Clone `/tmp/kengaku-r25-CpReferenceExec`, branch `r25-CpReferenceExec`, observed base `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`. Nothing is committed (`git status --short` shows `?? plans/fixtures/`). In the live lane tree, only this report was written.
## Files (in the clone)
- `plans/fixtures/r25/cp_reference.py` (388 lines, sha256 `f6cdf70f…bbd857`, stdlib only). Each bound comes from bisection on the grid i/10^D of the exact tail `P(X>=j|n,p)`, computed in `fractions.Fraction` (no beta or F quantile, no float on the path). One exact evaluation at the midpoint then fixes the half-up rounding, so every printed digit is proven. Ties are reported; none occurred. Semantics follow R `binom.test` (`binom.test.R:65-87`). Modes: emit; `--verify PATH`, which checks per bound that the tail at v±½·10^-D brackets α/2 (or 1−α/2), plus grid completeness, the k=0/k=n endpoints, lo(k,n)=1−hi(n−k,n) and monotonicity in k; `--point K N`; `--published`. Exit codes: 0 ok, 1 mismatch or failed proof, 2 usage.
- `plans/fixtures/r25/cp_reference.tsv`: 862 lines (header plus 861 rows for 0<=k<=n<=40, ordered by n then k), sha256 `2b7c4898…07bdd`. The n=0 row is the empty-information interval [0,1]; R rejects n=0.
## Evidence (commands run in the clone)
- `python3 plans/fixtures/r25/cp_reference.py --out plans/fixtures/r25/cp_reference.tsv` printed `rows=861 nmax=40 alpha=1/20 decimals=12 ties=0` in 0.76 s. Two regenerations were byte-identical (same sha256).
- `--verify plans/fixtures/r25/cp_reference.tsv` exited 0 with `certified=1640 endpoints=82 symmetric=861 monotone=1640 failures=0`.
- Three corrupted scratch copies each exited 1:
  - +1e-12 on lo(1,2): `FAIL line 6 k=1 n=2: lo=0.012579117094 is not the correctly rounded root`, plus a symmetry FAIL.
  - A deleted row: `missing row k=17 n=40`.
  - The dispatch value: `FAIL line 57 k=0 n=10: hi=0.308498000000 …`.
- `--published` exited 0: `values=14 match=11 mismatch=3 unexpected=0 | closed_form: values=80 match=80 mismatch=0 max_abs_diff=7.4e-17 tol=1e-15`. Bad arguments exit 2.
## TSV head
```
k	n	lo	hi
0	0	0.000000000000	1.000000000000
0	1	0.000000000000	0.975000000000
1	1	0.025000000000	1.000000000000
0	2	0.000000000000	0.841886116992
1	2	0.012579117093	0.987420882907
2	2	0.158113883008	1.000000000000
0	3	0.000000000000	0.707598226179
1	3	0.008403758660	0.905700675950
2	3	0.094299324050	0.991596241340
3	3	0.292401773821	1.000000000000
```
## Cross-check
Match rules, fixed in code before the run: a `dec` value must equal the exact bound rounded to the printed places; an `f64` value must satisfy |Δ| ≤ 5e-13, and its ulp error is shown.
| # | source @ location | k/n conf | printed lo · hi | exact lo · hi | verdict lo · hi |
|---|---|---|---|---|---|
| 1-2 | Stata [R] ci PDF p.9 Ex.6 | 2/20 .95 | .0123485 · .3169827 | 0.0123485272 · 0.3169827140 | MATCH · MATCH |
| 3 | Stata PDF p.10 Technical note | 0/20 .95 | — · .1684335 | 0 · 0.1684334710 | — · MATCH |
| 4-5 | Stata PDF p.14 Ex.13 | 1/10 .99 | .0005011 · .5442871 | 0.0005011286 · 0.5442870569 | MATCH · MATCH |
| 6 | SciPy binomtest Examples (one-sided .95) | 3/15 .90 | 0.05684686759024681 · — | 0.05684686759024680044 | MATCH (+1.68 ulp) |
| 7-8 | SciPy proportion_ci Examples | 7/50 .95 | 0.05819170033997342 · 0.26739600249700846 | 0.05819170034037208486 · 0.26739600249700843716 | MATCH (Δ 4.0e-13 = −57,453 ulp) · MATCH (+0.34 ulp) |
| 9-10 | NIST 7.2.4.1 page (Dataplot) | 4/20 .90 | 0.071354 · 0.401029 | 0.0713538843 · 0.4010281173 | MATCH · **MISMATCH** (6dp 0.401028) |
| 11-12 | NIST prc241.r (uniroot) | 4/20 .90 | 0.07134838 · 0.4010294 | 0.0713538843 · 0.4010281173 | **MISMATCH** (Δ 5.5e-6) · **MISMATCH** (Δ 1.3e-6) |
| 13-14 | NCSS Ch.510 p.510-5 Ex.1 | 55/100 .95 | 0.4472802 · 0.6496798 | 0.4472801888 · 0.6496797708 | MATCH · MATCH |
| D | dispatch example vs Wikipedia closed form | 10/10 lo · 0/10 hi | 0.691503 · 0.308498 | 0.6915028922 · 0.3084971078 | MATCH · **MISMATCH** (6dp 0.308497) |
Closed-form sweep, 1−(α/2)^(1/n) and (α/2)^(1/n) for n=1..40 in float64: 80/80 MATCH, max |Δ| 7.4e-17.
## Findings
1. The dispatch value "k=0,n=10 upper 0.308498" is wrong. The exact value is 0.30849710781876082… (TSV:57 `0.308497107819`; a 60-digit Decimal closed form agrees), which rounds to **0.308497**. The k=n=10 lower bound 0.691503 is correct (TSV:67).
2. NIST prints pu=0.401029 (prc241.htm:444), but the exact 6dp value is 0.401028. Independent 60-digit check: P(X≤4|20,0.4010285)−0.05 = −3.516e-7. Its R code returns 0.4010294 and 0.07134838 with no `tol` argument, consistent with uniroot's default `tol = .Machine$double.eps^0.25` (nlm.R:60). The page's own prose interval "(0.071, 0.400)" (prc241.htm:451) contradicts its pu. These three rows are pinned `expect=MISMATCH`.
3. SciPy's documented lo(7,50) is 4.0e-13 below the root (60-digit tail residual −8.2e-13). It passes the 12-dp rule with only 1e-13 to spare. The code solves `find_root(… sf(k-1) - alpha …)` (_binomtest.py:137); that solver tolerance causes the gap is [INFERENCE]. Any consumer comparing against this value needs a tolerance of at least 5e-13.
4. Power ask (`plans/round-25-claims.md:43`): the TSV confirms n=17. lo(16,16)=0.794092785792 (TSV:154) and lo(17,17)=0.804935677031 (TSV:172). The stated "n=16 → 0.7940" is truncated; correctly rounded it is 0.7941. The verdict does not change.
5. Support for prediction P1: lo(10,10)=0.691502892181 < 0.80 ≤ hi=1, so 10/10 is INDETERMINATE under the frozen rule.
6. R is not installed (no `R`/`Rscript`) and pacman is paused, so the binom.test semantics come from its source (`binom.test.R:65-87`), not from running it.
## Sources opened (local date 2026-10-20; curl fetches 2026-10-21T00:22:50Z to 00:29:44Z UTC; every quote found in the raw bytes)
- https://www.stata.com/manuals/rci.pdf `f8f23751…`: "The exact binomial, also known as the Clopper–Pearson (1934) interval, is computed by default." @ PDF p.9 Ex.6 (values on PDF pp.9, 10, 14)
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html `0f161b5a…`: "ConfidenceInterval(low=0.05684686759024681, high=1.0)" @ Examples, last block (raw l.659)
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html `f814ec0f…`: "‘exact’ : Use the Clopper-Pearson exact method [1]." @ Parameters→method; values @ Examples (raw l.596)
- https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm `20994b4a…`: "Whether or not the interval is truly "exact" depends on the software." @ binomial example (raw l.451-452). Also prc241.r `e381daab…` ("> [1] 0.4010294") and prc241.dp `f3bdb589…` ("PU = 0.401029")
- https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/NCSS/One_Proportion.pdf `7ea7ddf7…`: "Exact Confidence Interval for P … 55 100 0.55 1.95996 0.4472802 0.6496798" @ p.510-5 Ex.1
- https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval `4466eb89…`: "closed-form expressions for the interval bounds are available" @ § Clopper–Pearson interval (raw l.5982)
- https://raw.githubusercontent.com/wch/r-source/trunk/src/library/stats/R/binom.test.R `385ee83d…`: "## Determine p s.t. Prob(B(n,p) >= x) = alpha." @ l.65. Also nlm.R in the same directory, `256be4ad…`: "tol = .Machine$double.eps^0.25" @ l.60
- https://raw.githubusercontent.com/scipy/scipy/v1.18.0/scipy/stats/_binomtest.py `df89f663…`: "find_root(lambda p, k, n: _SimpleBinomial(n, p).sf(k-1) - alpha," @ l.137
Checks for L1: run `--verify plans/fixtures/r25/cp_reference.tsv` and `--published` (both should exit 0), then regenerate with `--out` and `cmp`.
VERDICT: The exact rational-bisection CP reference and its 861-row TSV are built in the clone. All 1640 bounds certified and every corruption test exited 1. Of 14 published values, 11 match; NIST's three and the dispatch's 0.308498 are wrong (exact 0.308497).
Installs: none (python3.14 stdlib; curl and pdftotext were already installed).

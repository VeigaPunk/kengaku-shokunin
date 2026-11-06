source: S334–S339, https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/bn-fit-modify/tests/test_outputs.py:150; companion files and quotes in corpus/lessons/round-99.md §Gate
verified-at: 2026-11-06 (round 99; measured T f72a8bc710b12473b5c768004e2581f980d924f4)
recheck: on-release

# A one-column distribution test grades a whole causal pipeline

The captured `bn-fit-modify` grader asks for three files: the learned DAG, the DAG after an intervention
on Y, and 10 000 samples from the intervened network. Seven of its nine tests check that files exist,
that columns are present, and that each DAG's set of `(from, to)` pairs equals a hard-coded edge set.
Only `test_sampled_data` looks at the sample's values. It checks the row count (10 000), the column count
(5), and a one-sample Kolmogorov–Smirnov test of **column D alone**. The reference normal for that test
uses the maintainer's fitted constants: mean −12.2965135 + 0.5495886·50.47989, sd
√(0.5495886²·10.68515² + 14.0916²). The test accepts when p ≥ 0.001.

The replay runs the captured file unchanged under real `pytest.main`, with an observe-only hook that
records each test's outcome and exception type. The environment is python 3.13 / pandas 2.3.2 /
scipy 1.16.1 / pytest 8.4.1 (the `test.sh` pins), plus numpy 2.5.4 for the seeded case builder. The run is
offline in bubblewrap. Thirteen cases × ten legs reproduce their mechanism predictions
(`plans/round99-cases.json`, `corpus/evidence/round99/bnfit-probe.txt`). Legs are the nine tests in file
order, then the reward: `bn_exists, ldag_exists, ldag_cols, ldag_struct, idag_exists, idag_cols,
idag_struct, sample_cols, sample_data, reward`.

| intervention | observed | interpretation |
|---|---|---|
| C01 maintainer solution outputs (R/bnlearn, one offline run) | P×9, 1 | positive control. The fit printed by the solution equals the grader's constants: D = −12.2965135 + 0.5495886·U + 0.4485709·Y, sd 14.09165; the grader rounds the sd to 14.0916 (`corpus/evidence/round99/bn-fit-modify-solution/run.log`). ReviewC1 re-ran the script offline and got byte-identical DAG files and the same fit |
| C02 no output files | F,F,E,E,F,E,E,E,E, 0 (E = FileNotFoundError) | no work is rejected |
| C03 U,R,Y,M all 0.0; D drawn from the target normal (seeded draw, `default_rng(3)`) | P×9, 1 | **gap**: no structure learning, no fit and no intervention, yet the sample passes, because only D is tested. Flip rate: 1998/2000 seeds pass (99.9 %, the KS α; ExecKS) |
| C04 sample from the fitted BN without the Y intervention (seeded draw, `default_rng(4)`, OLS refit on the dataset) | sample_data F, 0 | mechanism negative for C03: the KS test sees D's mean shift, +0.449·E[Y] = +22.59 (about 1.48 sd; KS D 0.516). Flip rate: 0/200 seeds pass (ScribeLesson) |
| C05 solution sample written with R's default row-names column | sample_data F, 0 | the names test only checks inclusion (passes); the 5-column assert fails. This is a realistic R slip: `write.csv` defaults to `row.names = TRUE`, and the maintainer's script passes `row.names = FALSE` explicitly to avoid it |
| C06 both DAG files with header `to,from` and swapped columns | P×9, 1 | the grader reads by column name. The instruction's literal header `to,from` over `A,B` example rows is ambiguous, and the grader tolerates either column order as long as the names match |
| C07 learned DAG with every edge twice plus a `weight` column | P×9, 1 | **gap**: the grader compares a set, so duplicates and extra columns pass |
| C08 R→M written M→R | ldag_struct F, 0 | set equality catches a reversed edge |
| C09 intervened DAG keeps U→Y | idag_struct F, 0 | the intervention's graph surgery is checked |
| C10 9 999 sample rows | sample_data F, 0 | exact row count |
| C11 D = normal quantile grid shifted +0.045 sd | P×9, 1 | **gap (tolerance band)**: KS D = 0.0180, p = 0.0030 ≥ 0.001 |
| C12 the same grid shifted +0.050 sd | sample_data F, 0 | KS D = 0.0200, p = 0.00066: the pass/fail edge is a mean shift of 0.0487 sd (bisected: ExecKS 0.04869, ScribeLesson 0.048702) |
| C13 D = deterministic normal quantile grid (no sampling) | P×9, 1 | **gap**: any array with the right marginal passes, so nothing requires a sample |

## What this teaches about grading

- **A marginal test of one variable does not certify the joint distribution that produced it.** The task's
  substance — structure learning, parameter fitting, and the do-intervention on Y — reaches the grader
  only through D's mean and spread. Two different causal pipelines that produce the same D marginal score
  the same. Y is never required to be 0 after the intervention, and U, R and M are never read (C03).
- **A distribution test with a fixed threshold sets a tolerance band, not a correctness check.** With
  n = 10 000 and p ≥ 0.001 the band is about ±0.0487 sd on the mean (C11/C12). Random draws near the edge
  pass or fail by chance: a seeded random draw at +0.03 sd failed in dry run 1, and 49 of 200 seeds fail at
  that shift (`.ufo/waves/round-99/L1/predictions-amendment-1.txt`). A prediction about a stochastic
  verdict must state its seed noise, or the case must be deterministic.
- **Set-based structure checks are blind to multiplicity and extra fields** (C07), as in round 98's
  per-line membership check (`knowledge/tb2-regex-chess-grader.md`), which a duplicate also fools.
- **The task's input is not pinned by the task commit.** The Dockerfile fetches the dataset from the
  unpinned `main` branch of a personal repository (S338). On 2026-11-06 those bytes equalled commit
  `62ce2364` (S339). The grader's constants were computed from those bytes, so a changed dataset would
  fail a correct solution.

## Limits

- The positive control is one run of the maintainer's R script, with conda-forge r-bnlearn 5.2.1 instead
  of the CRAN 4.9 that `solve.sh` installs. `rbn()` is unseeded, so the probe stages that run's committed
  outputs and does not re-run R. The fit equal to the grader constants is the evidence that the fixture is
  faithful.
- The replay does not run the harness image (`alexgshaw/bn-fit-modify:20251031`, S340). It makes no claim
  about any submitted agent solution.

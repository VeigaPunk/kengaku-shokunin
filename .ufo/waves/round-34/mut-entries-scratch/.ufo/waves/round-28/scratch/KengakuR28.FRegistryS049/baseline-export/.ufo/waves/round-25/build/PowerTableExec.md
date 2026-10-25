# PowerTableExec — r25 C1 power table (writer, private clone; axis: novelty)
Clone `/tmp/kengaku-r25-PowerTableExec`, branch `r25-PowerTableExec`, observed base `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`. Uncommitted; L1 integrates.
New `plans/fixtures/r25/power_table.py` (415 lines, mode 100755, sha256 `405d049ae5e5e92af81d52505013671d742007bbb8d7339d35b16ff0a684b3f7`)
New `plans/fixtures/r25/power_table.tsv` (75 lines, sha256 `840fec51c99e934bb57607b93d3ce463b09174df39797c41a3093d533d62ca0d`)

## Behavior
- Stdlib-only and offline. Every decision is the exact integer test `P(X>=k | n, bar) <= 1/40`, which is equivalent to "CP95 lower >= bar" because the tail strictly increases in p. No float or Beta quantile enters a verdict.
- Bounds come from a 64-step integer bisection bracket (width 2^-64) and are printed only when both ends round half-even to the same 6 dp (certified). Tails are exact, printed to 8 dp. The rule3 and Wilson columns are approximations, never verdicts.
- CLI: no args prints; `--write`; `--check` (byte drift exits 1); `--summary`; `--selftest`. Exit codes 0/1/2 follow the shared interface. Blocks are `min_n`, `zero_error`, `derived` and `check`, each with its own `table` header row.

## Table: min n with two-sided CP95 lower >= bar, k = n − e (`power_table.tsv:7-16`)
```
bar  e min_n counts  lower@min  lower@min-1 tail@min   tail@min-1 r3 wil
0.80 0    17   17/17 0.804936 0.794093    0.02251800 0.02814750 15  16
0.80 1    26   25/26 0.803630 0.796483    0.02266736 0.02738973 NA  25
0.80 2    34   32/34 0.803227 0.797736    0.02259587 0.02677912 NA  33
0.90 0    36   36/36 0.902606 0.899968    0.02252840 0.02503156 30  35
0.90 1    54   53/54 0.901085 0.899298    0.02366974 0.02588226 NA  53
0.90 2    70   68/70 0.900571 0.899185    0.02418130 0.02619770 NA  69
0.95 0    72   72/72 0.950056 0.949371    0.02489428 0.02620451 60  73
0.95 1   110 109/110 0.950389 0.949943    0.02406759 0.02513792 NA 110
0.95 2   142 140/142 0.950049 0.949702    0.02486110 0.02584922 NA 142
```
Zero-error rows for n=1..40, shown as `n cp_lower 1-3/n` (`power_table.tsv:18-58`; the TSV adds rule3−cp, 0.05^(1/n) and PASS-at columns):
```
 1 0.025000 -2.000000 |  2 0.158114 -0.500000 |  3 0.292402  0.000000 |  4 0.397635  0.250000 |  5 0.478176  0.400000
 6 0.540742  0.500000 |  7 0.590384  0.571429 |  8 0.630583  0.625000 |  9 0.663733  0.666667 | 10 0.691503  0.700000
11 0.715086  0.727273 | 12 0.735352  0.750000 | 13 0.752947  0.769231 | 14 0.768364  0.785714 | 15 0.781981  0.800000
16 0.794093  0.812500 | 17 0.804936  0.823529 | 18 0.814698  0.833333 | 19 0.823533  0.842105 | 20 0.831567  0.850000
21 0.838902  0.857143 | 22 0.845627  0.863636 | 23 0.851815  0.869565 | 24 0.857526  0.875000 | 25 0.862815  0.880000
26 0.867725  0.884615 | 27 0.872297  0.888889 | 28 0.876564  0.892857 | 29 0.880555  0.896552 | 30 0.884297  0.900000
31 0.887811  0.903226 | 32 0.891119  0.906250 | 33 0.894237  0.909091 | 34 0.897182  0.911765 | 35 0.899968  0.914286
36 0.902606  0.916667 | 37 0.905109  0.918919 | 38 0.907487  0.921053 | 39 0.909749  0.923077 | 40 0.911903  0.925000
```

## Findings
F1 **n=17 verified.** `python3 plans/fixtures/r25/power_table.py --summary` prints `min_n_rows=9 zero_error_rows=40 checks=6 pass=6 fail=0 power_ask_min_n=17` and exits 0. `power_table.tsv:70` reads `power_ask_n17 PASS`: 0.8^17=0.02251800 <= 0.025 < 0.8^16=0.02814750.
F2 `round-25-claims.md:43` gives n=16 → 0.7940. The exact value is 0.794093, which is 0.7941 at 4 dp (`tsv:61`): the pre-registration truncated it. The verdict is unaffected, and `ConnKotoba.md:43` already noted this. The truncation spread to CalibSelftestExec `EXPECTED.tsv:3-4` (messaged; they acked a fix). `SkillRuleScout.md:40` calls it a "match".
F3 The tightened ask N(0..5)={17,26,34,41,48,55} (`CritPowerAsk.md:8`) reproduces exactly (`tsv:62`). Its boundary values 0.8036/0.8032/0.7965/0.7977 match `tsv:9-10`.
F4 The rule of three is anti-conservative under the frozen rule from n=9 (`tsv:27,64`). It would PASS n=15-16 at 0.80 and n=30-35 at 0.90 where CP gives INDETERMINATE (`tsv:65`). It sits below 0.05^(1/n) for every n in 1-40 (`tsv:66`), so it approximates the one-sided 95% (two-sided 90%) bound, not α/2=0.025.
F5 Wilson is not uniformly looser than CP. With zero errors, Wilson > CP for n=1-45 and Wilson < CP for n=46-400 (`tsv:67`). Wilson minima are 16/35/73 against CP 17/36/72 (`tsv:8,11,14`). A Wilson PASS at n=16 is not a frozen-rule PASS, yet at bar 0.95 Wilson needs one more trial than CP.
F6 Tightest crossing: bar 0.90, e=0, lower(35/35)=0.899968, which is 3.2e-5 below the bar (`tsv:63`). The exact tail is 0.9^35=0.02503156 (`tsv:11`).
F7 Independent oracle: `uv run --no-project --python 3.14 --with scipy --with statsmodels python /tmp/r25-powertable-oracle/oracle.py <tsv>` → `scipy=1.18.1 statsmodels=0.15.0 compared=143 mismatches=0`. It compared beta.ppf bounds, binom.sf tails, and the CP and Wilson min-n scans. Against CpReferenceExec `cp_reference.tsv` (n<=40): 48 overlapping (k,n), 0 mismatches at 6 dp.
F8 `--selftest` → `selftest_total=13 pass=13 fail=0`. Positive controls: the exact rule, the closed form, R binom.test(9,10)=[0.5549839,0.9974714] and (10,10)=[0.6915029,1]. Red mutants caught: one-sided α→14, rule3→15, Wilson→16, scan ±1→18/16, a perturbed reference, an uncertified 8-bit bracket, a non-monotone decision, and an edited cell (drift at line 8).
F9 Other runs: `--write` exit 0 (75 lines); `--check` → `no drift`, exit 0; `--bogus` → usage, exit 2; `--check /tmp/nonexistent-r25.tsv` exits 1.

## Risks
- This is iid binomial math only; correlation between trials (cluster effects) is not modelled.
- The no-reversal check is finite (n<=400); monotonicity in n and k is argued analytically in the script docstring.
- The write tool set mode 100755, while `plans/attrib_probe.py` is 100644; L1 may normalize.

VERDICT: n=17 confirmed as the exact zero-error CP95 minimum at bar 0.80 (0.8^16 > 0.025 >= 0.8^17); power table certified, 143/143 oracle-matched, selftest 13/13.
Installs: nothing persistent. Ephemeral `uv run --with scipy --with statsmodels` (scipy 1.18.1, statsmodels 0.15.0, plus numpy/pandas; 13 pkgs; PyPI → uv cache) for the independent oracle; uv 0.13.0 was already installed. No pacman.

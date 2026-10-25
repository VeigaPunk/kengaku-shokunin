# Round-11 power analysis — emission-granularity severity dose (filed before any request)

## Effect-size source (committed r9 bytes only, re-derivable)

Command (repo root; reads only `corpus/evidence/round9-replication/results-r9.jsonl`):

```python
import json, collections, statistics
recs = [json.loads(l) for l in open('corpus/evidence/round9-replication/results-r9.jsonl')]
d = collections.defaultdict(dict)
for r in recs:
    if r['cell'] in ('A-CKPT4710', 'A-CKPT710') and 'nwrong' in r:
        d[r['pid']].setdefault(r['cell'], {})[r['turn']] = r['nwrong']
diffs = []
for pid in sorted(d):
    a, b = d[pid]['A-CKPT4710'], d[pid]['A-CKPT710']
    diffs.append(((b[7] + b[10]) / 2) - ((a[7] + a[10]) / 2))
statistics.mean(diffs), statistics.stdev(diffs), len(diffs)
```

Result (ran 2026-09-28, round 11 design phase): per-pid paired difference of
mean `nwrong` at the **shared checkpoints {7,10}** (710 minus 4710):

| pid | 101 | 102 | 103 | 104 | 105 | 106 | 107 | 108 |
|---|---|---|---|---|---|---|---|---|
| diff | +2.5 | 0.0 | +1.0 | −0.5 | +1.0 | 0.0 | 0.0 | 0.0 |

- mean diff = **+0.500**, sample sd = **0.9636**, n = 8
- Cohen d = 0.500 / 0.9636 = **0.519**
- sign test: 3 wins (710 worse) / 1 loss / 4 ties — r9's own report calls the
  paired tests "underpowered and not conventionally significant at this n"
  (`replication.md` §Dose-response reading).

## Why the shared-checkpoint paired mean is the primary endpoint

Turns 7 and 10 are graded under **both** schedules on the **same** problem, so
the per-pid difference removes problem difficulty entirely; the r9 headline
"0.875 → 1.375" mixes denominators (final-turn means over different cells)
and is descriptive only. The paired difference at {7,10} has mean +0.500 —
the same signal, cleaner unit. (Final-turn-only diffs give the identical mean
+0.500 on these 8 pids.)

## Sample size

Primary test (preregistered in `probe_plan_r11.md` §Analysis): two-sided
paired t-test, α = 0.05, on the 64 per-pid differences. Normal-approximation
sample size: n = (z₀.₉₇₅ + z₀.₈₀)² / d² = (1.9600 + 0.8416)² / d² = 7.849 / d².

| planning d | required n (80% power) |
|---:|---:|
| 0.519 (r9 point estimate) | 30 |
| 0.50 | 32 |
| 0.40 | 50 |
| **0.35 (chosen MDE)** | **64** |
| 0.30 | 88 |

**Chosen n = 64 pairs (pids 201–264).** Rationale: the r9 d = 0.519 is
estimated from 8 pairs (sd itself uncertain; the effect was selected *because*
it showed, so it is upward-biased — regression to the mean). Planning at
d = 0.35 ≈ ⅔ of the point estimate makes the run adequately powered for any
true effect ≥ 0.35 sd; at the r9 point estimate the power is
Φ(√64·0.519 − 1.960) = Φ(2.191) ≈ **0.986**. At n = 64 the MDE (80% power,
α = 0.05 two-sided) is d = √(7.849/64) = **0.350**.

## Cost feasibility (why not n = 88)

r9's 276 requests took mean wall_s 0.215 s (median 0.26, max 0.62;
`sum(wall_s)` ≈ 60 s). r11 at n = 64 issues 1 (descriptors) + 64 × 22 =
**1409 requests** ≈ 5–8 min serial. n = 88 (d = 0.30) would cost ~1857
requests; the marginal power gain over a shrinkage-adjusted MDE of 0.35 does
not justify doubling burst exposure. If the observed d lands below 0.35 the
honest outcome is the preregistered DIRECTIONAL verdict, not a silent n
extension (post-hoc power grabs are anti-pattern territory per `SKILL.md`).

## Residual threats (priced, not hidden)

1. **Non-iid draws** (round-7 finding: lag-1 autocorrelation, shared decode
   state under `--cont-batching --parallel 2`): pairing is within-pid and
   adjacent in time, cell order counterbalanced by pid parity, one filler
   request before each cell — these bound, not eliminate, the threat. The
   t-test assumes iid differences across pids; cross-pid contamination would
   inflate type-I error, so the sign test is preregistered as robustness.
2. **d estimated from n = 8**: handled by the 0.35 shrinkage above.
3. **Serving stack** (q4_0 KV cache, `--kv-unified`, custom chat template,
   IQ2_XXS quant): pinned as experimental-unit descriptors at run time and
   cited in every derived claim; no cross-model generalization is claimed.
4. **Multiplicity**: one primary endpoint (paired severity diff). Pass rates
   and McNemar are preregistered as descriptive/robustness — a significant
   McNemar is reported as a new pass-rate finding, never folded into the
   primary claim.

#!/usr/bin/env python3
"""Round-12 power analysis — deterministic, stdlib-only, offline.

Every input number is read from COMMITTED bytes (no hand-typed effect sizes):

  * r11 paired severity dose at shared checkpoints {7,10}
        corpus/evidence/round11-power/results-r11.jsonl  -> mean diff, sd of diffs
  * r8 paired gap A-CKPT(4710) - A-INC at {4,7,10} and the final-turn level step
        corpus/evidence/round8-horizon/results.jsonl
  * the per-problem difficulty distribution used to build the Page-test
    alternative is bootstrapped from r11's committed per-pid values

Outputs (printed, and pasted verbatim into power_analysis_r12.md):
  1. paired-t power by Monte Carlo (fixed seed) for dz in {0.35, r11-observed}
     at n in {44, 48, 56, 64};
  2. the minimum n reaching 80% power for each dz (integer search, MC);
  3. Page's ordered-trend power at n in {44, 48, 56, 64} under the anchored
     4-arm alternative (counts simulated as integers, so ties are realistic);
  4. the transport arm's power at n=48 for the r11 dz and for a halved dz.

Monte Carlo seeds are fixed; PYTHONHASHSEED is irrelevant (no dict iteration
over hash-ordered keys in any statistic). Re-run:
    python3 corpus/evidence/round12-ladder/power_r12.py
"""
import json
import math
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
R11 = os.path.join(ROOT, "corpus/evidence/round11-power/results-r11.jsonl")
R8 = os.path.join(ROOT, "corpus/evidence/round8-horizon/results.jsonl")
SEED = 20260929
NSIM = 20000


def load(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


# ---------- 1. committed effect sizes ----------
def per_pid_mean(recs, cell, turns):
    out = {}
    for r in recs:
        if r.get("cell") == cell and r.get("turn") in turns and "nwrong" in r:
            out.setdefault(r["pid"], []).append(r["nwrong"])
    return {k: statistics.fmean(v) for k, v in out.items()}


def paired(a, b):
    pids = sorted(set(a) & set(b))
    d = [b[p] - a[p] for p in pids]
    return statistics.fmean(d), statistics.stdev(d), len(d), pids


def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def paired_t_p(diffs):
    n = len(diffs)
    m = statistics.fmean(diffs)
    sd = statistics.stdev(diffs) if n > 1 else 0.0
    if sd == 0.0:
        return 1.0
    t = m / (sd / math.sqrt(n))
    # two-sided p from the normal approximation to the t distribution; the MC
    # below is a POWER estimate, and the t/normal difference at df>=43 is
    # <0.02 in p (stated as an approximation in power_analysis_r12.md).
    return 2.0 * (1.0 - norm_cdf(abs(t)))


def mc_paired_power(dz, n, sims=NSIM, seed=SEED):
    rng = random.Random(seed)
    hits = 0
    for _ in range(sims):
        d = [rng.gauss(dz, 1.0) for _ in range(n)]
        if paired_t_p(d) < 0.05 and statistics.fmean(d) > 0:
            hits += 1
    return hits / sims


def min_n_for_power(dz, target=0.80, lo=8, hi=400):
    for n in range(lo, hi + 1):
        if mc_paired_power(dz, n, sims=4000, seed=SEED + n) >= target:
            return n, mc_paired_power(dz, n, sims=NSIM, seed=SEED)
    return None, None


# ---------- 2. Page's ordered-trend test (k=4, blocks = problems) ----------
def page_L(blocks):
    """blocks: list of 4 values ordered dense->sparse. Returns (L, E_L, var_L, z).
    Midranks within block; Var per block = [sum j^2 - (sum j)^2/k] * S^2 with
    S^2 the block's midrank sample variance (exact conditional null variance
    for a random permutation of the observed midrank multiset)."""
    k = 4
    Rj = [0.0] * k
    var = 0.0
    for b in blocks:
        order = sorted(range(k), key=lambda i: b[i])
        ranks = [0.0] * k
        i = 0
        while i < k:
            j = i
            while j + 1 < k and b[order[j + 1]] == b[order[i]]:
                j += 1
            mid = (i + j) / 2.0 + 1.0
            for t in range(i, j + 1):
                ranks[order[t]] = mid
            i = j + 1
        for t in range(k):
            Rj[t] += ranks[t]
        mbar = sum(ranks) / k
        s2 = sum((r - mbar) ** 2 for r in ranks) / (k - 1)
        coef = sum((t + 1) ** 2 for t in range(k)) - (sum(range(1, k + 1)) ** 2) / k
        var += coef * s2
    L = sum((t + 1) * Rj[t] for t in range(k))
    n = len(blocks)
    E_L = n * k * (k + 1) ** 2 / 4.0
    if var <= 0:
        return L, E_L, var, 0.0
    return L, E_L, var, (L - E_L) / math.sqrt(var)


def mc_page_power(means, diff_sd, n, sims=4000, seed=SEED, difficulty=None):
    """means: 4 arm offsets (dense->sparse); diff_sd: sd of a paired diff, so
    per-observation noise sd = diff_sd/sqrt(2). Integer counts (ties realistic).
    difficulty: list of per-problem offsets to bootstrap from (committed r11)."""
    rng = random.Random(seed)
    noise = diff_sd / math.sqrt(2.0)
    hits = 0
    for _ in range(sims):
        blocks = []
        for _ in range(n):
            d = rng.choice(difficulty) if difficulty else 0.0
            vals = [max(0, int(round(m + d + rng.gauss(0.0, noise)))) for m in means]
            blocks.append(vals)
        _, E_L, _, z = page_L(blocks)
        if z > 0 and 2.0 * (1.0 - norm_cdf(abs(z))) < 0.05:
            hits += 1
    return hits / sims


def main():
    r11 = load(R11)
    r8 = load(R8)
    a4710 = per_pid_mean(r11, "A-CKPT4710", {7, 10})
    a710 = per_pid_mean(r11, "A-CKPT710", {7, 10})
    m_r11, sd_r11, n_r11, pids = paired(a4710, a710)
    dz_r11 = m_r11 / sd_r11
    print(f"## committed inputs")
    print(f"r11 paired dose {{7,10}}: mean={m_r11:+.4f} sd={sd_r11:.4f} n={n_r11} dz={dz_r11:.4f}")

    inc8 = per_pid_mean(r8, "A-INC", {4, 7, 10})
    ck8 = per_pid_mean(r8, "A-CKPT", {4, 7, 10})
    m8, sd8, n8, _ = paired(inc8, ck8)
    print(f"r8 paired gap (A-CKPT - A-INC) {{4,7,10}}: mean={m8:+.4f} sd={sd8:.4f} n={n8} dz={m8/sd8:.4f}")
    fin8 = {c: per_pid_mean(r8, c, {10}) for c in ("A-INC", "A-CKPT")}
    fin8_mono = per_pid_mean(r8, "A-MONO", {1})
    step8 = statistics.fmean(fin8["A-CKPT"].values()) - statistics.fmean(fin8["A-INC"].values())
    fin11 = {c: per_pid_mean(r11, c, {10}) for c in ("A-CKPT4710", "A-CKPT710")}
    step11 = statistics.fmean(fin11["A-CKPT710"].values()) - statistics.fmean(fin11["A-CKPT4710"].values())
    mono8 = statistics.fmean(fin8_mono.values())
    ck4710_8 = statistics.fmean(fin8["A-CKPT"].values())
    print(f"r8 final-turn levels: INC={statistics.fmean(fin8['A-INC'].values()):.4f} "
          f"CKPT={ck4710_8:.4f} (step {step8:+.4f}) MONO={mono8:.4f}")
    print(f"r11 final-turn levels: 4710={statistics.fmean(fin11['A-CKPT4710'].values()):.4f} "
          f"710={statistics.fmean(fin11['A-CKPT710'].values()):.4f} (step {step11:+.4f})")
    print(f"r8 MONO - CKPT4710 (final, paired): "
          f"{statistics.fmean([fin8_mono[p]-fin8['A-CKPT'][p] for p in sorted(set(fin8_mono)&set(fin8['A-CKPT']))]):+.4f}")

    print(f"\n## 1. paired-t power (Monte Carlo, sims={NSIM}, seed={SEED})")
    for dz in (0.35, round(dz_r11, 4)):
        row = []
        for n in (44, 48, 56, 64):
            row.append(f"n={n}: {mc_paired_power(dz, n):.3f}")
        print(f"dz={dz}: " + "  ".join(row))
    print(f"normal-approx reference at dz={dz_r11:.4f}: " +
          "  ".join(f"n={n}: {norm_cdf(dz_r11*math.sqrt(n)-1.959964):.3f}" for n in (44, 48, 56, 64)))

    print(f"\n## 2. minimum n for 80% power (paired t, MC search)")
    for dz in (0.35, round(dz_r11, 4)):
        n_min, pw = min_n_for_power(dz)
        print(f"dz={dz}: n_min={n_min} (power at n_min = {pw:.3f})")

    print(f"\n## 3. Page's ordered-trend power (k=4, MC sims=4000, seed={SEED})")
    difficulty = [a4710[p] for p in pids]
    difficulty = [d - statistics.fmean(difficulty) for d in difficulty]
    means = [0.0, m8, m8 + m_r11, m8 + m_r11 + step11]
    print(f"anchored arm offsets (dense->sparse): " + " ".join(f"{m:+.4f}" for m in means))
    print(f"difficulty offsets bootstrapped from r11 per-pid A-CKPT4710 {{7,10}} means (n={len(difficulty)}); "
          f"noise sd = {sd_r11:.4f}/sqrt(2) = {sd_r11/math.sqrt(2):.4f}; counts integer-rounded")
    for n in (44, 48, 56, 64):
        print(f"n={n}: power={mc_page_power(means, sd_r11, n, difficulty=difficulty):.3f}")
    half = [m / 2.0 for m in means]
    print(f"halved alternative {[round(m,4) for m in half]}: " +
          "  ".join(f"n={n}: {mc_page_power(half, sd_r11, n, difficulty=difficulty):.3f}" for n in (48, 64)))
    n_min_page = None
    for n in range(12, 200):
        if mc_page_power(means, sd_r11, n, sims=2000, seed=SEED + n, difficulty=difficulty) >= 0.80:
            n_min_page = n
            break
    print(f"minimum n for 80% Page power at the anchored alternative: {n_min_page}")

    print(f"\n## 4. transport arm (family 2, paired t)")
    for dz in (round(dz_r11, 4), round(dz_r11 / 2, 4)):
        print(f"dz={dz}: n=48 power={mc_paired_power(dz, 48):.3f}  n=44 power={mc_paired_power(dz, 44):.3f}  "
              f"n=32 power={mc_paired_power(dz, 32):.3f}")
    n_t, pw_t = min_n_for_power(round(dz_r11 / 2, 4))
    print(f"minimum n for 80% power at a HALVED transported effect (dz={dz_r11/2:.4f}): {n_t} (power {pw_t:.3f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

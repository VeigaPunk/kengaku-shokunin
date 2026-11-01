# distribution-search oracle note (round 58, C3)

Task: terminal-bench-2 `distribution-search` @ pin `2fd12b88` (full sha
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`). Graded property: build a length-150000
probability vector P with |KL(P||U) − 10.0| ≤ 1e-3 AND |KL(U||P) − 10.0| ≤ 1e-3, where
U is uniform. Sources: S209 (task.toml), S210 (tests/test_outputs.py), S211
(solution/solve.sh — the oracle), S212 (instruction.md). Capture bytes committed at
`corpus/evidence/round58/tb2-distribution-search/` (sha256s below).

## The oracle read (S211)

The maintainer's `solution/solve.sh` embeds `search_distributions.py`: a **three-level
Newton solve over integer atom counts**. For candidate counts (A, B, C) of
heavy/middle/light atoms it solves for (log p_h, log p_m, log p_l):

    E1: A*ph + B*pm + C*pl = 1                          (simplex)
    E2: A*lh + B*lm + C*ll = -V*(ln V + 10)             (KL(U||P) = 10)
    E3: A*ph*lh + B*pm*lm + C*pl*ll = 10 - ln V         (KL(P||U) = 10)

(damped Newton with line search, logs clamped <= 0), scanning A over a ±1175 grid around
f = 0.05·V and B over a geometric ladder, accepting the first point with
max(|KLf − 10|, |KLb − 10|) ≤ 1e-3, then `P /= P.sum()`.

Authoring-time run of the extracted solver (this round, WSL python 3.12.3 / numpy 2.5.4,
the r56 A3.4 canonical environment) accepted:

    A=2, B=6325, C=143673
    ph = 0.4453992881456182
    pm = 1.7260803274269405e-05
    pl = 1.8683398418359735e-10

Elementwise verification of the built array (the grader's own reduction path,
`np.sum(P*np.log(P)) + np.log(P.size)` / `-np.log(P.size) - (1/P.size)*np.sum(np.log(P))`):
kf = 10.0 (error 0.0), kb = 9.999999999999995 (error 5.3e-15), sum−1 = +2.2e-16,
min = 1.87e-10 > 0, max = 0.4454 ≤ 1. These six literals are frozen into
`plans/round58_c2_kl_probe.py` and `plans/round-58-claims.md`.

## Capture identity (all fetched 2026-11-01 at the pin, bytes hashed on arrival)

| file | sha256 |
|---|---|
| task.toml (S209) | `70c8e73cafd0a75306375bec2c2e1e4d82e0cb969fd7e38a63e7c344de43b681` |
| tests/test_outputs.py (S210) | `02bca54db4849b7c911253fb92f941e21db8b1eea13261a7e5a9871fca68b4ed` |
| solution/solve.sh (S211) | `19daaee18d534f36679854b0ba5727290df389ee023ebb67846cb89579d38bbe` |
| instruction.md (S212) | `aba2e1835b2f827686402c3d3ff9b309aab8c9cbac26e23fc46aaeb34e958915` |

Probe receipt: `corpus/evidence/round58/kl-probe.txt` (written by
`plans/round58_c2_kl_probe.py --lane . --work <scratch> --receipt …`; its sha256 is pinned
in the probe's registry row and the round-58 SCORECARD section). Recheck command (180d):

    python3 plans/round58_c2_kl_probe.py --lane . --work <scratch> \
        --receipt corpus/evidence/round58/kl-probe.txt

## Static grader readings the freeze records

1. `test_kl_divergences` **renormalizes before measuring** (`P = P / P.sum()`): leg 4 is
   blind to overall scale — a raw-counts integer array and a ×1.001-scaled simplex both
   pass it while failing the validity leg.
2. `test_distribution_validity` runs on the RAW array; its `P.min() > 0` check is
   load-bearing for leg 4 (a nonpositive atom sends `np.log` to nan/−inf and both KLs out
   of band). Leg order (validity before kl) is file order, not declared dependency.
3. The shape constraint (1-D, exactly 150000) is leg-2-only: `P.size` and the `np.sum`
   reductions are shape-agnostic, so a (2, 75000) reshape passes validity and both KL legs.
4. The band accepts a neighbourhood: the solution with the middle level raised by a
   relative 5.2e-4 (a DIFFERENT distribution) still passes both legs (kf err ~5.1e-4,
   kb err ~3.5e-5) — the gate underdetermines the answer, exactly as the oracle's
   count-scanning search implies.
5. Determinism contrast (r57): no wall-clock leg, no U marks — a full-commitment 48-leg
   prediction table.

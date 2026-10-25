# Round-12 power analysis (filed pre-request; bundle member)

Generated inputs and every number below come from
`corpus/evidence/round12-ladder/power_r12.py` — stdlib only, offline, seeded
Monte Carlo, reading **committed** r8/r11 bytes for its effect sizes (no
hand-typed effects). Re-run verbatim:

```
python3 corpus/evidence/round12-ladder/power_r12.py
```

(`sims=20000` for the paired-t curves, `4000` for the Page curves, seed
`20260929`; the integer `n_min` search uses `4000` sims per candidate and
re-measures the winner at `20000`.)

## Filed design parameters

| parameter | value | source |
|---|---|---|
| primary confirmatory test (family 1) | Page's ordered-trend test, k=4 arms × n=64 blocks | `probe_plan_r12.md` §2.3 E1 |
| primary paired contrast (family 1) | `A-CKPT710 − A-CKPT4710` at {7,10}, n=64 | §2.3 E2 |
| transport contrast (family 2) | `T-SPARSE − T-DENSE` at {7,10}, n=48 | §2.3 E5 |
| two-sided α | 0.05 | all rules |
| target power | 0.80 | floors below |
| expected effect size | dz = 0.4288 (r11 paired: mean +0.3516, sd 0.8198, n=64) | `power_r12.py` §committed inputs |
| conservative MDE | dz = 0.35 (r11's filed MDE) | `round11-power/power_analysis_r11.md` |
| **power floors (error contingency)** | **family 1 n ≥ 44, family 2 n ≥ 44** | derived below |

## 1. Paired-t power at the planned n

Monte Carlo, 20 000 sims per cell, seed 20260929:

| dz | n=44 | n=48 | n=56 | n=64 |
|---|---:|---:|---:|---:|
| 0.35 (conservative MDE) | 0.644 | 0.682 | 0.739 | **0.798** |
| 0.4288 (r11 observed) | **0.810** | **0.842** | 0.891 | **0.928** |

Normal-approximation reference at dz=0.4288 (agrees with the MC to ±0.002):
n=44 → 0.812, n=48 → 0.844, n=56 → 0.894, n=64 → 0.929.

Readings, stated honestly:

- family 1 at n=64 has **0.928** power at the r11-observed effect and **0.798**
  at the conservative MDE dz=0.35 — i.e. r11's own "n=64 for MDE 0.35 at 80%"
  filing was right to within 0.002 of power, and r12 keeps it.
- family 2 at n=48 has **0.842** power at dz=0.4288, but only **0.682** at
  dz=0.35 and (below) **0.327** at a halved transported effect. The transport
  arm is powered for *the effect family 1 actually showed*, not for an
  attenuated one; a null there is weak evidence against transport.

## 2. Minimum n reaching 80% power (paired t, integer search)

| dz | n_min | power at n_min (20 000 sims) |
|---|---:|---:|
| 0.35 | 63 | 0.790 |
| 0.4288 | 42 | 0.791 |

The search returns the first n whose 4 000-sim estimate clears 0.80, then
re-measures at 20 000 sims; MC noise puts the re-measured value slightly under
0.80 in both cases. The **filed floors are therefore set one step above the
search result**: at n=44 the 20 000-sim power is **0.810** (n=42 → 0.791,
n=43 not on the grid). Hence `probe_plan_r12.md` §2.3's contingency floors are
**44 for both families**, replacing the asserted 56/42 that the design critic
falsified (D3: 42 pairs do not reach 80% power at dz=0.4288).

## 3. Page's ordered-trend power (the primary confirmatory test)

Alternative anchored on committed bytes: arm offsets dense→sparse
`[+0.0000, +0.6667, +1.0182, +1.3464]`, built as

- `+0.6667` — r8's paired per-pid gap `A-CKPT − A-INC` at {4,7,10}, n=10
  (the only committed measurement of that leg);
- `+1.0182` = 0.6667 + r11's paired dose at {7,10} (+0.3516);
- `+1.3464` = 1.0182 + r11's final-turn step `A-CKPT710 − A-CKPT4710`
  (+0.3281), used as the one-step extrapolation to a single-checkpoint arm.

Per-problem difficulty offsets are bootstrapped from r11's committed per-pid
`A-CKPT4710` {7,10} means (n=64, mean-centred); per-observation noise
sd = 0.8198/√2 = 0.5797; simulated values are integer-rounded and floored at 0,
so tie structure is realistic (integer `nwrong` in 0..8).

| n | Page power (4 000 sims) |
|---:|---:|
| 44 | 1.000 |
| 48 | 1.000 |
| 56 | 1.000 |
| 64 | 1.000 |
| 48, halved alternative `[0, +0.3333, +0.5091, +0.6732]` | 0.989 |
| 64, halved alternative | 0.997 |

Minimum n for 80% Page power at the anchored alternative: **12**.

**Interpretation (this is the honest part):** the ordered-trend test is
massively over-powered at n=64 for any alternative near the anchored one, so
E1's binding risk is **anchor validity, not power**. The INC leg of the anchor
comes from r8 at n=10 in a different batch, and this lane's own measurement
rule 10 (`SKILL.md`) forbids comparing raw levels across batches — the anchor
is used only as a *power* input, never as a predicted level. If the true INC
arm is much closer to 4710 than r8's n=10 gap suggests, the trend weakens
toward the three adjacent contrasts, which is exactly what R1's
`LADDER DIRECTIONAL` branch is for.

## 4. Transport arm (family 2)

| dz | n=48 | n=44 | n=32 |
|---|---:|---:|---:|
| 0.4288 (family-1 effect, unattenuated) | 0.842 | 0.810 | 0.681 |
| 0.2144 (halved — the attenuation prior in `predict_r12.py`) | 0.327 | 0.303 | 0.244 |

Minimum n for 80% power at a halved transported effect: **169** (power 0.796).
n=48 was chosen because 169 problems × 2 arms ≈ 3 700 further requests would
double the run for an arm whose purpose is a *directional* transport check;
the resulting 0.327 power at the attenuated alternative is filed here rather
than hidden, and `predictions-r12.md` RL6 (P(TRANSPORTS) = 0.45) is set
consistent with it.

## 5. What is NOT powered

- No cross-model or cross-stack claim: one served unit, pinned in-band.
- The batching dissociation (E4) has no prior paired measurement at n≥44; its
  point prediction (+0.0437) is essentially null, so E4 is powered for a
  large effect only (0.928 at dz=0.4288, far less at the predicted magnitude).
  RL5 = 0.20 reflects that.
- Calibration slope precision: Van Calster's ≥200-events-and-≥200-non-events
  guidance is met by the 416 pass events only if the observed pass count lands
  ≥200 and the failures ≥200 — predicted passes sum to 150.8 across all arms
  (`predictions-r12.md` §2), so **the non-event side clears 200 and the event
  side does not**; the slope is reported with that shortfall named, not as a
  precision claim.

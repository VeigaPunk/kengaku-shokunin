# Round 11 preregistered predictions

Scope: 64 fresh problems, pids 201–264, seeds `3000 + pid*41`, cells
`A-CKPT4710` (checkpoints {4,7,10}) vs `A-CKPT710` (checkpoints {7,10}),
endpoint/settings/descriptors per `probe_plan_r11.md`. Filed and hashed before
the first endpoint request (see `ordering.log`).

## Point predictions (scored `|predicted − observed| / 64`)

| Quantity | Predicted | Basis | Falsifier |
|---|---:|---|---|
| A-CKPT4710 final (turn-10) passes | 15/64 | r9 2/8 = 25%, r8 A-CKPT 1/10 = 10%; shrunk toward the r8–r9 pooled ~20% | — (descriptive; no directional claim preregistered on passes) |
| A-CKPT710 final (turn-10) passes | 13/64 | r9 2/8 = 25% but the severity differential predicts slightly worse exactness | — |
| Paired severity diff (710 − 4710, mean nwrong at shared {7,10}) | **+0.350** | r9 point estimate +0.500 shrunk by ~30% for selection bias | diff ≤ 0 kills the granularity–severity claim at the powered n |

## Probabilistic predictions (scored with Brier, mean over the three)

| # | Event | P |
|---|---|---:|
| 1 | mean paired diff > 0 | 0.78 |
| 2 | two-sided paired t-test p < 0.05 AND diff > 0 | 0.50 |
| 3 | \|passes(4710) − passes(710)\| ≤ 8 | 0.60 |

Brier = (1/3) Σ (P − outcome)², outcome ∈ {0,1}. Filed as probabilities
because they are feasible here — the round-10 calibration rubric caps
"point forecasts where probabilities are feasible".

## Preregistered verdict rule (exclusive, mechanical)

Let `diff` = mean paired severity difference, `p` = two-sided paired t p-value:

1. `diff > 0` AND `p < 0.05` → **ESTABLISHED**: granularity–severity dose
   demonstrated at the preregistered power (n=64, MDE d=0.35).
2. `diff > 0` AND `p ≥ 0.05` → **DIRECTIONAL**: indeterminate; per the
   calibration rubric this MUST NOT be reported as established or replicated.
3. `diff ≤ 0` → **FALSIFIED** at n=64: the r9 severity reading does not
   survive a powered rerun; record as a refutation of the lane's own r9
   interpretation.

## Secondary preregistered tests (robustness / new-findings only)

- Exact sign test on the 64 per-pid diffs (ties omitted, exact binomial):
  must agree in direction with the t-test, else the verdict downgrades to
  DIRECTIONAL regardless of the t p-value.
- McNemar exact test on final passes (b = 4710-pass/710-fail, c = converse):
  descriptive. If p < 0.05 it is reported as a **new** pass-rate dose
  finding (r9's tie dead) with its own prior-art pricing — never folded into
  the severity claim.

## What would falsify the design itself (pre-run checks)

- Any of the 64 seeds fails `gen_problem` or duplicates an r8/r9 problem →
  run is void, re-seed and re-hash before any request.
- `ordering.log` hash time not ≤ first `request_ts` → calibration breach,
  round self-reports it (r8 precedent).
- Descriptors record cannot pin the served model id → run continues but
  claims lose their experimental-unit descriptor and are downgraded.

#!/usr/bin/env python3
"""ExecKS: KS-rule edge + marginal-only pass rate + maintainer-process pass rate."""
import numpy as np, pandas as pd
from scipy.stats import kstest, norm

TM = -12.2965135 + 0.5495886 * 50.47989
TS = ((0.5495886**2) * 10.68515**2 + 14.0916**2) ** 0.5
N = 10_000
P_TH = 0.001
print(f"TM={TM!r} TS={TS!r}")

def ks_p(x):
    return kstest(x, "norm", args=(TM, TS)).pvalue

def passes(x):
    return ks_p(x) >= P_TH

# ---- 1. bisection on quantile-grid shift (sd units) ----
q = norm.ppf((np.arange(N) + 0.5) / N)
def grid_pass(k):
    return ks_p(TM + TS * (q + k)) >= P_TH
for k in (0.0, 0.01, 0.03, 0.045, 0.048, 0.05, 0.06):
    print(f"grid k={k:+.4f} p={ks_p(TM + TS * (q + k)):.6g} pass={grid_pass(k)}")

lo, hi = 0.045, 0.050   # lo passes (C11), hi fails (C12)
assert grid_pass(lo) and not grid_pass(hi), "bracket violated"
for _ in range(60):
    mid = (lo + hi) / 2
    if hi - lo < 5e-5:
        break
    if grid_pass(mid):
        lo = mid
    else:
        hi = mid
print(f"EDGE lo={lo:.6f} hi={hi:.6f} width={hi-lo:.2e}  edge~{(lo+hi)/2:.6f} sd")
for k in (lo, (lo+hi)/2, hi):
    print(f"  grid k={k:.6f} p={ks_p(TM + TS * (q + k)):.6g} pass={grid_pass(k)}")
# theoretical: D_stat = Phi(k)-0.5 (+0.5/n grid coarseness)
print(f"Phi(edge)-0.5 = {norm.cdf((lo+hi)/2)-0.5:.6f}")

# random-draw comparison at same shifts (cross-check builder comment: 49/200 fail at 0.03)
for k in (0.0, 0.03, 0.045, (lo+hi)/2, 0.05):
    s = 0
    for seed in range(200):
        rng = np.random.default_rng(seed)
        s += passes(TM + TS * (rng.standard_normal(N) + k))
    print(f"random-draw k={k:.4f} pass-rate over 200 seeds = {s/2:.1f}% ({s}/200)")

# ---- 2a. marginal-only forgery: D ~ N(TM,TS) exactly, 2000 seeds ----
S = 2000
cnt = 0
for seed in range(S):
    rng = np.random.default_rng(seed)
    if passes(rng.normal(TM, TS, N)):
        cnt += 1
print(f"MARGINAL-ONLY (C03 forgery) pass {cnt}/{S} = {cnt/S*100:.3f}%")

# ---- 2b. maintainer process: hierarchical intervened draw ----
# fit bnlearn-equivalent Gaussian CPDs by OLS on the committed 10k data
data = pd.read_csv("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round99/tb2-bn-fit-modify/bn_sample_10k.csv")
def ols(y, xs):
    X = np.column_stack([np.ones(len(data))] + [data[x].to_numpy() for x in xs])
    beta, *_ = np.linalg.lstsq(X, data[y].to_numpy(), rcond=None)
    resid = data[y].to_numpy() - X @ beta
    return beta, float(np.sqrt(resid @ resid / (len(data) - X.shape[1])))
print("U fit mean=%.5f sd=%.5f (grader E[U]=50.47989, sd_u=10.68515)" % (data["U"].mean(), data["U"].std(ddof=1)))
bD, sD = ols("D", ["U", "Y"])
print(f"D fit intercept={bD[0]:.7f} b_U={bD[1]:.7f} b_Y={bD[2]:.7f} sd={sD:.5f} (grader -12.2965135/0.5495886/14.0916)")
bR, sR = ols("R", ["U"]); bM, sM = ols("M", ["U", "R"])
cnt2 = 0
for seed in range(S):
    rng = np.random.default_rng(seed)
    U = rng.normal(data["U"].mean(), data["U"].std(ddof=1), N)
    Y = np.zeros(N)                                   # intervention do(Y=0)
    R = bR[0] + bR[1] * U + rng.normal(0, sR, N)
    M = bM[0] + bM[1] * U + bM[2] * R + rng.normal(0, sM, N)
    D = bD[0] + bD[1] * U + bD[2] * Y + rng.normal(0, sD, N)
    if passes(D):
        cnt2 += 1
print(f"MAINTAINER-PROCESS (hierarchical intervened) pass {cnt2}/{S} = {cnt2/S*100:.3f}%")

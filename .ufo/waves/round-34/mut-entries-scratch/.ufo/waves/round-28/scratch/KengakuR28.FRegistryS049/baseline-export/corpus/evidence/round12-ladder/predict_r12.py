#!/usr/bin/env python3
"""Round-12 prediction generator — writes the preregistered forecast bundle.

This script is part of the hashed preregistration bundle: it is run BEFORE any
round-12 endpoint request and reads ONLY committed prior-round bytes
(r8 `corpus/evidence/round8-horizon/results.jsonl`, r11
`corpus/evidence/round11-power/results-r11.jsonl`). It cannot see r12 outcomes.

It emits three files next to itself:
  predictions-r12.md              (bundle member; human-readable, hashed)
  predictions-r12-perproblem.jsonl (416 pass events, one per (arm,pid))
  predictions-r12-signevents.jsonl (304 per-problem sign events)

Every number in the .md is derived by a rule stated IN this file. The three
judgement inputs — the shrinkage pseudo-count, the checkpoint-count
extrapolation, the transport attenuation factor, and the seven run-level event
probabilities — are literals below with their justification in a comment; they
are frozen by the bundle hash, which is the point of preregistering them.

Re-run:  python3 corpus/evidence/round12-ladder/predict_r12.py
Determinism: stdlib only, no dict-order dependence, no network, no clock in any
output (the UTC date line is read from SOURCE_DATE_EPOCH if set, else omitted).
"""
import hashlib
import json
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
R11 = os.path.join(ROOT, "corpus/evidence/round11-power/results-r11.jsonl")
R8 = os.path.join(ROOT, "corpus/evidence/round8-horizon/results.jsonl")

N1, N2 = 64, 48
PIDS = list(range(201, 201 + N1))
PIDS2 = list(range(401, 401 + N2))
ARMS1 = ["A-INC", "A-CKPT4710", "A-CKPT710", "A-CKPT10", "A-MONO"]
ARMS2 = ["T-DENSE", "T-SPARSE"]
CLIP = (0.02, 0.98)          # prediction clip, keeps Brier/logit finite
LOGIT_CLIP = 1e-6            # recalibration clip (design critic D5)

# ---------- judgement inputs (frozen by the bundle hash) ----------
K_SHRINK = 4                 # pseudo-observations toward 0.5 for arms whose prior
                             # evidence has n < 20 (r8 arms only, n=10)
ATTENUATE = 0.5              # stated prior: a dose transported to a structurally
                             # different task family is expected at half
                             # magnitude. NOT a measurement; labelled as a prior
                             # wherever it is used.
RUNLEVEL_EVENTS = [
    # (id, event text, probability, justification)
    ("RL1", "E1 Page p < 0.05 AND direction increasing (LADDER ESTABLISHED)", 0.55,
     "power_analysis_r12.md gives >=0.98 power at the anchored alternative, but the "
     "anchor's INC leg comes from r8 at n=10 in a different batch; the binding risk is "
     "anchor validity, not power, so 0.55 not 0.9"),
    ("RL2", "E2 verdict = REPEATS-r11 (diff>0, p<0.05, sign agrees)", 0.70,
     "r11 fired the same rule at p=0.0011 on these exact problems; batch variability "
     "(r8 1/10, r9 2/8+2/8, r11 29/64+21/64) is the residual risk"),
    ("RL3", "E2 additionally POINT-MATCHES-r11 (|diff - 0.352| <= 0.15)", 0.45,
     "the r11 point estimate has a 95% CI half-width of 0.205, wider than the 0.15 window"),
    ("RL4", "all three adjacent diffs (E3) > 0", 0.50,
     "the INC leg is the only one never measured at n>=44; sign agreement across three "
     "gaps is a conjunction"),
    ("RL5", "E4 verdict = DISSOCIATION ESTABLISHED", 0.20,
     "the mechanical point prediction below is +0.044, i.e. essentially null: r8's "
     "MONO-CKPT4710 gap (+0.700) is almost exactly consumed by two extrapolated "
     "final-turn steps (2 x +0.328)"),
    ("RL6", "E5 verdict = TRANSPORTS (family-2 dose diff>0, p<0.05)", 0.45,
     "attenuation prior 0.5 x dz=0.4288 -> dz=0.214, at which n=48 has 0.327 power "
     "(power_r12.py §4); unattenuated it has 0.842"),
    ("RL7", "E6 verdict = FORECAST SKILLED (BSS>0 AND slope in [0.5,2.0])", 0.50,
     "the persistence predictor should beat arm climatology on family-1 replicate arms "
     "but is constant-per-arm on family 2, where BSS is ~0 by construction"),
]


def load(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def sigmoid(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def logit(p):
    p = min(1.0 - LOGIT_CLIP, max(LOGIT_CLIP, p))
    return math.log(p / (1.0 - p))


def fit_logistic(X, y, iters=200, tol=1e-12):
    """Newton–Raphson with a ridge of 1e-8 for numerical stability. X rows are
    [1, f1, f2, ...]. Deterministic; no external dependency."""
    k = len(X[0])
    b = [0.0] * k
    for _ in range(iters):
        g = [0.0] * k
        H = [[0.0] * k for _ in range(k)]
        for x, yi in zip(X, y):
            p = sigmoid(sum(bj * xj for bj, xj in zip(b, x)))
            w = p * (1.0 - p)
            r = yi - p
            for a in range(k):
                g[a] += r * x[a] - 1e-8 * b[a]
                for c in range(k):
                    H[a][c] += w * x[a] * x[c] + (1e-8 if a == c else 0.0)
        # solve H delta = g (Gaussian elimination, partial pivoting)
        M = [row[:] + [g[i]] for i, row in enumerate(H)]
        for col in range(k):
            piv = max(range(col, k), key=lambda r: abs(M[r][col]))
            if abs(M[piv][col]) < 1e-14:
                return b, False
            M[col], M[piv] = M[piv], M[col]
            for r in range(k):
                if r != col:
                    f = M[r][col] / M[col][col]
                    for c in range(col, k + 1):
                        M[r][c] -= f * M[col][c]
        delta = [M[i][k] / M[i][i] for i in range(k)]
        b = [bj + dj for bj, dj in zip(b, delta)]
        if max(abs(d) for d in delta) < tol:
            return b, True
    return b, False


def per_pid_mean(recs, cell, turns, pid_filter=None):
    out = {}
    for r in recs:
        if r.get("cell") == cell and r.get("turn") in turns and "nwrong" in r:
            if pid_filter is not None and r["pid"] not in pid_filter:
                continue
            out.setdefault(r["pid"], []).append(r["nwrong"])
    return {k: statistics.fmean(v) for k, v in out.items()}


def final_pass(recs, cell, turn):
    return {r["pid"]: bool(r["ok"]) for r in recs
            if r.get("cell") == cell and r.get("turn") == turn and "ok" in r}


def shrunk(successes, n, k=K_SHRINK):
    return (successes + k * 0.5) / (n + k)


def main():
    r11 = load(R11)
    r8 = load(R8)

    # ---- r11 committed quantities (the predictor's only per-problem features) ----
    a4710 = per_pid_mean(r11, "A-CKPT4710", {7, 10}, set(PIDS))
    a710 = per_pid_mean(r11, "A-CKPT710", {7, 10}, set(PIDS))
    assert len(a4710) == N1 == len(a710), (len(a4710), len(a710))
    x = {p: (a4710[p] + a710[p]) / 2.0 for p in PIDS}
    xbar = statistics.fmean(x.values())
    diff_r11 = statistics.fmean([a710[p] - a4710[p] for p in PIDS])
    sd_r11 = statistics.stdev([a710[p] - a4710[p] for p in PIDS])
    wins = sum(1 for p in PIDS if a710[p] - a4710[p] > 0)

    p4710 = final_pass(r11, "A-CKPT4710", 10)
    p710 = final_pass(r11, "A-CKPT710", 10)
    rate4710 = sum(p4710[p] for p in PIDS) / N1
    rate710 = sum(p710[p] for p in PIDS) / N1

    # difficulty slope c: logistic fit on r11's 128 (pid,arm) final-pass outcomes
    X, y = [], []
    for p in PIDS:
        for arm, ok in (("A-CKPT4710", p4710[p]), ("A-CKPT710", p710[p])):
            X.append([1.0, 1.0 if arm == "A-CKPT710" else 0.0, x[p] - xbar])
            y.append(1.0 if ok else 0.0)
    coef, conv = fit_logistic(X, y)
    assert conv, "logistic fit did not converge"
    a_int, b_arm, c_diff = coef

    # ---- r8 committed quantities (INC / MONO anchors) ----
    inc8 = final_pass(r8, "A-INC", 10)
    mono8 = final_pass(r8, "A-MONO", 1)
    ck8 = final_pass(r8, "A-CKPT", 10)
    n8 = len(inc8)
    gap8 = statistics.fmean([per_pid_mean(r8, "A-CKPT", {4, 7, 10}, {p})[p]
                             - per_pid_mean(r8, "A-INC", {4, 7, 10}, {p})[p] for p in sorted(inc8)])
    step8_final = (statistics.fmean(per_pid_mean(r8, "A-CKPT", {10}, set(inc8)).values())
                   - statistics.fmean(per_pid_mean(r8, "A-INC", {10}, set(inc8)).values()))
    mono_minus_ck8 = statistics.fmean([
        per_pid_mean(r8, "A-MONO", {1}, {p})[p] - per_pid_mean(r8, "A-CKPT", {10}, {p})[p]
        for p in sorted(inc8)])
    step11_final = (statistics.fmean(per_pid_mean(r11, "A-CKPT710", {10}, set(PIDS)).values())
                    - statistics.fmean(per_pid_mean(r11, "A-CKPT4710", {10}, set(PIDS)).values()))

    # ---- arm base rates (rule: raw rate if prior n>=20; shrunk if n<20;
    #      checkpoint-count extrapolation if no direct observation) ----
    base = {
        "A-INC": shrunk(sum(inc8.values()), n8),
        "A-CKPT4710": rate4710,
        "A-CKPT710": rate710,
        "A-CKPT10": rate710 - (rate4710 - rate710),   # linear in checkpoint count 3->2->1
        "A-MONO": shrunk(sum(mono8.values()), n8),
        "T-DENSE": rate4710,                            # transport-of-base-rate null
        "T-SPARSE": rate710,
    }
    base_rule = {
        "A-INC": f"r8 {sum(inc8.values())}/{n8} shrunk with k={K_SHRINK} toward 0.5",
        "A-CKPT4710": f"r11 {sum(p4710[p] for p in PIDS)}/{N1} raw (n>=20)",
        "A-CKPT710": f"r11 {sum(p710[p] for p in PIDS)}/{N1} raw (n>=20)",
        "A-CKPT10": "linear extrapolation in checkpoint count from the r11 pair "
                    f"(3 ckpts {rate4710:.4f}, 2 ckpts {rate710:.4f} -> 1 ckpt)",
        "A-MONO": f"r8 {sum(mono8.values())}/{n8} shrunk with k={K_SHRINK} toward 0.5",
        "T-DENSE": "family-1 dense arm rate (transport-of-base-rate null)",
        "T-SPARSE": "family-1 sparse arm rate (transport-of-base-rate null)",
    }

    # ---- per-problem pass probabilities (mean-preserving in the arm marginal) ----
    # The fitted difficulty slope is steep, so a raw tilt
    # sigmoid(logit(base) + c*z) saturates and its arm mean drifts far from the
    # §1 base rate (measured before this fix: A-MONO mean p 0.372 vs base 0.143).
    # A per-arm logit offset delta_arm is therefore solved by bisection so that
    # mean(clip(sigmoid(logit(base) + c*z + delta))) == base_arm to 1e-12: the
    # tilt redistributes probability ACROSS problems while preserving the
    # arm-level marginal, so each arm's predicted pass count equals
    # base_arm * n by construction. Clipping is inside the bisection target so
    # saturation cannot re-break the marginal.
    def arm_probs(zvals):
        """zvals: per-problem difficulty offsets (x_pid - xbar); empty -> constant."""
        return [c_diff * z for z in zvals] if zvals else []

    def solve_delta(tilt, base_arm):
        lo, hi = -40.0, 40.0
        for _ in range(200):
            mid = (lo + hi) / 2.0
            m = statistics.fmean([min(CLIP[1], max(CLIP[0], sigmoid(logit(base_arm) + t + mid)))
                                  for t in tilt])
            if m > base_arm:
                hi = mid
            else:
                lo = mid
            if hi - lo < 1e-12:
                break
        return (lo + hi) / 2.0

    rows, deltas = [], {}
    for arm in ARMS1:
        tilt = arm_probs([x[p] - xbar for p in PIDS])
        d = solve_delta(tilt, base[arm])
        deltas[arm] = d
        for p, t in zip(PIDS, tilt):
            pr = min(CLIP[1], max(CLIP[0], sigmoid(logit(base[arm]) + t + d)))
            rows.append({"arm": arm, "family": 1, "pid": p, "p_pass": round(pr, 6),
                         "base_arm": round(base[arm], 6), "x_pid": round(x[p], 6),
                         "delta_arm": round(d, 6)})
    for arm in ARMS2:
        # no family-2 prior data: constant per arm by design (no-information
        # forecast); the marginal is the base rate exactly, delta = 0.
        deltas[arm] = 0.0
        pr = min(CLIP[1], max(CLIP[0], base[arm]))
        for p in PIDS2:
            rows.append({"arm": arm, "family": 2, "pid": p, "p_pass": round(pr, 6),
                         "base_arm": round(base[arm], 6), "x_pid": None,
                         "delta_arm": 0.0})

    # ---- per-problem sign events: P(sparser nwrong > denser nwrong) ----
    # E2's contrast has r11 per-problem evidence -> unconditional win rate wins/N1.
    # Every other contrast gets the uninformative 0.50: no committed per-problem
    # sign distribution exists for it (family-2 tie rates are unknown, and the
    # INC/CKPT10/MONO arms were never run at n>=44).
    p_e2 = wins / N1
    contrasts = [("E3a", "A-CKPT4710 - A-INC", "{4,7,10}", 1, 0.50),
                 ("E3b", "A-CKPT710 - A-CKPT4710", "{7,10}", 1, round(p_e2, 6)),
                 ("E3c", "A-CKPT10 - A-CKPT710", "{10}", 1, 0.50),
                 ("E4", "A-MONO - A-CKPT10", "final", 1, 0.50),
                 ("E5", "T-SPARSE - T-DENSE", "{7,10}", 2, 0.50)]
    srows = []
    for cid, label, turns, fam, prob in contrasts:
        for p in (PIDS if fam == 1 else PIDS2):
            srows.append({"contrast": cid, "label": label, "turns": turns,
                          "family": fam, "pid": p, "p_diffpos": prob})

    # ---- point predictions (each with its mechanical derivation) ----
    pred_E3a = gap8
    pred_E2 = round(diff_r11, 3)
    pred_E3c = step11_final
    pred_E4 = mono_minus_ck8 - 2 * step11_final
    pred_E5 = ATTENUATE * diff_r11
    points = [
        ("E3a 4710-INC at {4,7,10}", pred_E3a,
         f"r8 paired per-pid mean at {{4,7,10}}, n={n8} (committed bytes)"),
        ("E2/E3b 710-4710 at {7,10}", pred_E2,
         f"r11 paired per-pid mean, n={N1} (recomputed {diff_r11:+.4f}, published +0.352)"),
        ("E3c 10-710 at {10}", pred_E3c,
         f"one-step linear extrapolation in removed checkpoints using r11's final-turn "
         f"step ({step11_final:+.4f})"),
        ("E4 MONO-CKPT10 final", pred_E4,
         f"r8 paired MONO-CKPT4710 final gap ({mono_minus_ck8:+.4f}) minus two "
         f"extrapolated final-turn steps (2 x {step11_final:+.4f})"),
        ("E5 SPARSE-DENSE at {7,10} (family 2)", pred_E5,
         f"r11 dose x ATTENUATE={ATTENUATE} (stated prior, not a measurement)"),
    ]
    pred_passes = {}
    for arm in ARMS1 + ARMS2:
        pred_passes[arm] = sum(r["p_pass"] for r in rows if r["arm"] == arm)

    # ---- write artifacts ----
    pj = os.path.join(HERE, "predictions-r12-perproblem.jsonl")
    sj = os.path.join(HERE, "predictions-r12-signevents.jsonl")
    with open(pj, "w") as f:
        for r in rows:
            f.write(json.dumps(r, separators=(",", ":"), sort_keys=True) + "\n")
    with open(sj, "w") as f:
        for r in srows:
            f.write(json.dumps(r, separators=(",", ":"), sort_keys=True) + "\n")

    def sha(path):
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    n_pass = len(rows)
    n_sign = len(srows)
    n_rl = len(RUNLEVEL_EVENTS)
    lines = []
    A = lines.append
    A("# Round-12 filed predictions (generated by `predict_r12.py`; hashed pre-request)")
    A("")
    A("Generated from COMMITTED prior-round bytes only — r8")
    A("`corpus/evidence/round8-horizon/results.jsonl`) and r11")
    A("`corpus/evidence/round11-power/results-r11.jsonl`). No round-12 request had")
    A("been made when this file was written; `ordering.log` pins the ordering. Rules")
    A("and every judgement literal live in `predict_r12.py` (also hashed).")
    A("")
    A("## Event sets scored at close (design critic D6: reported separately, never")
    A("## pooled into one 'forecast skill' number without these splits)")
    A("")
    A(f"| set | N | what it tests |")
    A(f"|---|---:|---|")
    A(f"| pass events | {n_pass} | 5 family-1 arms x {N1} problems + 2 family-2 arms x {N2} |")
    A(f"| per-problem sign events | {n_sign} | E3a/E3b/E3c/E4 x {N1} + E5 x {N2} |")
    A(f"| run-level events | {n_rl} | RL1-RL7 below |")
    A(f"| **total scored events** | **{n_pass + n_sign + n_rl}** | |")
    A("")
    A("Brier = mean (p - outcome)^2 per set. BSS = 1 - Brier/Brier_climatology, where")
    A("the climatological forecast is each event's own group base rate: per-arm")
    A("observed pass rate for pass events, per-contrast observed win rate for sign")
    A("events, per-event observed rate for run-level events. **The pooled pass-event")
    A("BSS is labelled `persistence + arm-rate transport`, not generic forecast")
    A("skill**: family-1 predictions reuse r11 outcomes on the SAME problems, and")
    A("family-2 predictions are constant per arm by design. Reported splits: (i)")
    A("family-1 replicate arms (`A-CKPT4710`, `A-CKPT710` — the arms with r11")
    A("per-problem evidence), (ii) family-1 novel arms (`A-INC`, `A-CKPT10`,")
    A("`A-MONO` — base rate + transported difficulty slope only), (iii) family 2")
    A("(constant per arm). Excluded pids (error records) are dropped from BOTH the")
    A("score and its climatology, never scored as failures.")
    A("")
    A("Calibration: slope + intercept from a logistic recalibration of outcome on")
    A(f"logit(p), probabilities clipped to [{LOGIT_CLIP}, 1-{LOGIT_CLIP}] before the")
    A("logit (critic D5), damped Newton, <=50 iterations, tol 1e-10; reported for the")
    A(f"{n_pass} pass events (primary) and for all {n_pass + n_sign + n_rl} events")
    A("(secondary). Reliability: 5 equal-width bins on p; an empty bin prints")
    A("`pred=n/a obs=n/a n=0` (critic D8).")
    A("")
    A("## 1. Arm base rates and their derivation rule")
    A("")
    A("| arm | base rate | rule |")
    A("|---|---:|---|")
    for arm in ARMS1 + ARMS2:
        A(f"| `{arm}` | {base[arm]:.4f} | {base_rule[arm]} |")
    A("")
    A(f"Shrinkage rule: raw rate when the prior evidence has n>=20; otherwise")
    A(f"(successes + {K_SHRINK}*0.5)/(n + {K_SHRINK}). `A-CKPT10` has no direct")
    A("observation, so it is linearly extrapolated in checkpoint count from the r11")
    A("pair. Family-2 arms inherit the family-1 dense/sparse rates as an explicit")
    A("transport-of-base-rate null.")
    A("")
    A("## 2. Difficulty tilt (fitted on r11's committed per-problem bytes)")
    A("")
    A(f"Logistic fit on {len(y)} r11 (pid,arm) final-pass outcomes, features")
    A(f"[1, I(arm=A-CKPT710), x_pid - xbar] where x_pid = mean of that pid's r11")
    A(f"mean `nwrong` at {{7,10}} over both arms, xbar = {xbar:.6f}:")
    A("")
    A(f"    intercept a = {a_int:+.6f}")
    A(f"    arm(710) b  = {b_arm:+.6f}")
    A(f"    difficulty c = {c_diff:+.6f}   (per unit of x_pid - xbar)")
    A("")
    A("r12 per-problem probability:")
    A("")
    A("    p = clip( sigmoid( logit(base_arm) + c*(x_pid - xbar) + delta_arm ) )")
    A("")
    A(f"clipped to [{CLIP[0]}, {CLIP[1]}]. `delta_arm` is a mean-preserving offset")
    A("solved by bisection per arm so that the arm's mean predicted probability")
    A("equals its §1 base rate exactly (the fitted slope is steep; without the")
    A("offset the sigmoid saturates and the arm marginal drifts — measured before")
    A("the fix: A-MONO mean p 0.372 against a 0.143 base rate). Consequence: each")
    A("arm's predicted pass count equals base_arm x n by construction, and the tilt")
    A("only redistributes probability ACROSS problems.")
    A("")
    A("| arm | delta_arm | mean p | min p | max p |")
    A("|---|---:|---:|---:|---:|")
    for arm in ARMS1 + ARMS2:
        ps = [r["p_pass"] for r in rows if r["arm"] == arm]
        A(f"| `{arm}` | {deltas[arm]:+.4f} | {statistics.fmean(ps):.4f} | "
          f"{min(ps):.4f} | {max(ps):.4f} |")
    A("")
    A("The fitted arm intercepts are NOT reused for arms other than the two r11")
    A("arms; those take the §1 base rates. Family-2 problems have no prior x_pid,")
    A("so they get the constant base rate (no tilt, delta = 0).")
    A("")
    A("**Persistence-skill caveat (design critic D6).** `x_pid` is the mean of that")
    A("pid's r11 mean `nwrong` at {7,10} over both arms, so it includes r11's")
    A("turn-10 value — the same turn whose r12 pass is the prediction target. This")
    A("is not within-run circularity (different run, different day, a fresh context")
    A("per ladder, no cross-run state on the served unit), but the fitted slope is")
    A("therefore a *persistence-of-difficulty* coefficient and C5's skill claim may")
    A("only be read as persistence skill against arm climatology, never as cold")
    A("forecasting.")
    A("")
    A("Per-problem values: `predictions-r12-perproblem.jsonl` "
      f"({n_pass} lines, sha256 `{sha(pj)}`)")
    A("")
    A("Predicted pass counts implied by §1+§2 (the point predictions for the")
    A("SUMMARY lines; observed counts are compared against these at close):")
    A("")
    A("| arm | predicted passes | of n |")
    A("|---|---:|---:|")
    for arm in ARMS1:
        A(f"| `{arm}` | {pred_passes[arm]:.1f} | {N1} |")
    for arm in ARMS2:
        A(f"| `{arm}` | {pred_passes[arm]:.1f} | {N2} |")
    A("")
    A("## 3. Per-problem sign events")
    A("")
    A("| contrast | label | turns | P(diff>0) per problem | source of the probability |")
    A("|---|---|---|---:|---|")
    srcs = {"E3a": "uninformative 0.50 — no committed per-problem sign distribution",
            "E3b": f"r11 unconditional per-problem win rate {wins}/{N1}",
            "E3c": "uninformative 0.50 — `A-CKPT10` never run",
            "E4": "uninformative 0.50 — `A-MONO` never paired at n>=44",
            "E5": "uninformative 0.50 — family-2 tie rate unknown"}
    for cid, label, turns, fam, prob in contrasts:
        A(f"| {cid} | `{label}` | {turns} | {prob:.4f} | {srcs[cid]} |")
    A("")
    A(f"Per-event values: `predictions-r12-signevents.jsonl` ({n_sign} lines, "
      f"sha256 `{sha(sj)}`)")
    A("")
    A("## 4. Point predictions (mechanical derivations from committed bytes)")
    A("")
    A("| quantity | predicted | derivation |")
    A("|---|---:|---|")
    for name, val, why in points:
        A(f"| {name} | {val:+.4f} | {why} |")
    A("")
    A(f"Committed inputs: r11 paired dose {{7,10}} {diff_r11:+.4f} (sd {sd_r11:.4f}, "
      f"n={N1}, dz={diff_r11/sd_r11:.4f}); r11 per-problem wins {wins}/{N1}; "
      f"r8 paired gap {{4,7,10}} {gap8:+.4f} (n={n8}); r8 paired MONO-CKPT4710 final "
      f"{mono_minus_ck8:+.4f}; r11 final-turn step {step11_final:+.4f}; r8 final-turn "
      f"step {step8_final:+.4f}.")
    A("")
    A("## 5. Run-level probabilistic predictions (judgement, frozen by the hash)")
    A("")
    A("| id | event | P | justification |")
    A("|---|---|---:|---|")
    for rid, text, prob, why in RUNLEVEL_EVENTS:
        A(f"| {rid} | {text} | {prob:.2f} | {why} |")
    A("")
    A("Brier over these seven events is reported separately (r11's 3-event Brier of")
    A("0.153 is the comparator; 7 events is still small and is labelled as such).")
    A("")
    A("## 6. Preregistered verdict rule")
    A("")
    A("Applied verbatim from `probe_plan_r12.md` §2.3 (R1-R5), including the neutral-")
    A("sign downgrade (wins == losses counts as DISAGREEMENT), the degenerate-input")
    A("conventions (sd=0 -> t=0.000, p=1.0000; var_L=0 -> z=0.000, p=1.0000), and the")
    A("`UNDERPOWERED-INDETERMINATE` override when a family's analysed n falls below")
    A("the filed power floor (`power_analysis_r12.md`).")
    A("")
    md = os.path.join(HERE, "predictions-r12.md")
    with open(md, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"wrote {os.path.relpath(md, ROOT)} ({len(lines)} lines, sha256 {sha(md)})")
    print(f"wrote {os.path.relpath(pj, ROOT)} ({n_pass} pass events)")
    print(f"wrote {os.path.relpath(sj, ROOT)} ({n_sign} sign events)")
    print(f"total scored events at close: {n_pass + n_sign + n_rl}")
    print(f"fitted difficulty slope c = {c_diff:+.6f} (converged={conv})")
    for arm in ARMS1 + ARMS2:
        print(f"  base[{arm}] = {base[arm]:.4f}  predicted passes = {pred_passes[arm]:.1f}")
    for name, val, _ in points:
        print(f"  point[{name}] = {val:+.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

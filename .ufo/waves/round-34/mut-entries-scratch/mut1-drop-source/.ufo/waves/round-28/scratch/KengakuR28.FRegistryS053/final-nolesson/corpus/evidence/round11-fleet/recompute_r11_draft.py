#!/usr/bin/env python3
"""Round-11 deterministic analysis engine — emission-granularity severity dose.

DRAFT (L1 integration owner promotes it).
-----------------------------------------
This file lives at `corpus/evidence/round11-fleet/recompute_r11_draft.py`.
PROMOTION (mechanical, no source edits required — the module resolves its
default paths from its own location, so a verbatim copy works from either
directory):

    cp corpus/evidence/round11-fleet/recompute_r11_draft.py \
       corpus/evidence/round11-power/recompute_r11.py

Run (after the main run has landed `results-r11.jsonl` in round11-power):

    python3 corpus/evidence/round11-power/recompute_r11.py            # writes analysis_r11.md
    python3 corpus/evidence/round11-power/recompute_r11.py --results P --out Q
    python3 corpus/evidence/round11-power/recompute_r11.py --selftest # no endpoint, no results file needed

Never contacts the endpoint: this module performs no network I/O at all
(neither `/v1/chat/completions` nor `/v1/models`).

Frozen predictions
------------------
The point/probabilistic predictions and the verdict rule are baked in below as
`PRED` / `VERDICT_RULE_NOTE`, transcribed from
`corpus/evidence/round11-power/predictions-r11.md`:

    sha256(predictions-r11.md) = e912085ce0283dd4a0cd5c2de31dde937f69d38e12e9e4970a3470d23c46a902

as recorded in `corpus/evidence/round11-power/prereg-bundle.sha256` (v1). The
engine re-checks that frozen hash against the bundle file at analysis time and
records the result in `analysis_r11.md` (mismatch is reported, never fatal —
the deviation discipline is the grader's call).

Stored-line contract
--------------------
Every aggregate line emitted into `analysis_r11.md` uses the EXACT format
pinned in `probe_plan_r11.md` §5 (the gate re-derives those regexes from
committed bytes). Stats are stdlib-only: paired t via mean/sample-sd plus a
two-sided p from the incomplete-beta continued fraction (df = n-1); exact
binomials via `math.comb`.

Determinism: no set iteration reaches output; all pid/turn traversal is
sorted; floats are formatted with fixed precision. Independent of
PYTHONHASHSEED.
"""

import argparse
import json
import math
import os
import re
import sys
import tempfile

# --------------------------------------------------------------------------
# paths (resolved from this file so the draft and its promoted copy behave
# identically)
# --------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATE_DIRS = [HERE, os.path.join(os.path.dirname(HERE), "round11-power")]
POWER_DIR = next(
    (d for d in _CANDIDATE_DIRS if os.path.exists(os.path.join(d, "probe_plan_r11.md"))),
    _CANDIDATE_DIRS[-1],
)
DEF_RESULTS = os.path.join(POWER_DIR, "results-r11.jsonl")
DEF_OUT = os.path.join(POWER_DIR, "analysis_r11.md")
DEF_BUNDLE = os.path.join(POWER_DIR, "prereg-bundle.sha256")
DEF_ORDERING = os.path.join(POWER_DIR, "ordering.log")

GRADED_CELLS = ("A-CKPT4710", "A-CKPT710")
ACK_CELLS = ("A-CKPT4710-ack", "A-CKPT710-ack")
SHARED_TURNS = (7, 10)          # checkpoints graded under BOTH schedules
FINAL_TURN = 10

# --------------------------------------------------------------------------
# frozen predictions (predictions-r11.md, sha256 above)
# --------------------------------------------------------------------------
PREDICTIONS_SHA256 = "e912085ce0283dd4a0cd5c2de31dde937f69d38e12e9e4970a3470d23c46a902"
PRED = {
    # point predictions
    "passes_4710": 15,          # A-CKPT4710 final (turn-10) passes, of 64
    "passes_710": 13,           # A-CKPT710 final (turn-10) passes, of 64
    "severity_diff": 0.350,     # paired severity diff (710 - 4710), shared {7,10}
    # probabilistic predictions (Brier)
    "p_diff_gt_0": 0.78,        # mean paired diff > 0
    "p_sig_and_pos": 0.50,      # two-sided paired t p < 0.05 AND diff > 0
    "p_pass_gap_le_8": 0.60,    # |passes(4710) - passes(710)| <= 8
}
PASS_DENOM = 64                 # preregistered per-cell denominator (n=64 pids)
VERDICT_RULE_NOTE = (
    "predictions-r11.md §Preregistered verdict rule (exclusive, mechanical): "
    "(1) diff>0 and p<0.05 -> ESTABLISHED; (2) diff>0 and p>=0.05 -> DIRECTIONAL; "
    "(3) diff<=0 -> FALSIFIED. Secondary: the exact sign test must agree in "
    "direction with the t-test, else the verdict downgrades to DIRECTIONAL "
    "regardless of the t p-value."
)

# --------------------------------------------------------------------------
# ports (byte-faithful with grader.py / round9 graders)
# --------------------------------------------------------------------------
def extract_json_block(text):
    """Parse the last fenced JSON block, else the last brace/bracket span."""
    blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", text, re.S)
    if blocks:
        try:
            return json.loads(blocks[-1])
        except Exception:
            pass
    m = re.findall(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]",
                   text, re.S)
    for cand in reversed(m):
        try:
            return json.loads(cand)
        except Exception:
            continue
    return None


# --------------------------------------------------------------------------
# statistics (stdlib only)
# --------------------------------------------------------------------------
def mean(xs):
    return sum(xs) / len(xs)


def sample_sd(xs):
    """Sample standard deviation, denominator n-1 (matches statistics.stdev)."""
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def _betacf(a, b, x):
    """Continued fraction for the incomplete beta function (NR 6.4)."""
    MAXIT, EPS, FPMIN = 300, 3.0e-16, 1.0e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < EPS:
            break
    return h


def betai(a, b, x):
    """Regularized incomplete beta I_x(a, b) (NR 6.4)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t, df):
    """Two-sided Student-t tail P(|T| >= |t|) = I_{df/(df+t^2)}(df/2, 1/2)."""
    if df <= 0:
        raise ValueError("df must be positive")
    x = df / (df + t * t)
    return betai(df / 2.0, 0.5, x)


# t critical value, two-sided alpha=0.05, via bisection on the betai tail.
# df=63 -> 1.9983405425. Cross-checked by independent Simpson integration of
# the Student-t density (see SELFTEST_ANCHORS) and against the §5 constant
# 1.9983; the engine uses the computed value, the constant is asserted only.
T_CRIT_DF63_DOC = 1.9983  # probe_plan_r11.md §5 (scipy t.ppf(0.975, 63))


def t_crit(df, alpha=0.05):
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if t_two_sided_p(mid, df) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


# ---- selftest-only independent reference: adaptive Simpson quadrature of the
# Student-t density. Deliberately a different algorithm from the betai
# continued fraction, so it catches branch/convergence defects in `betai`.
def _t_pdf(t, df):
    return (math.exp(math.lgamma((df + 1) / 2.0) - math.lgamma(df / 2.0))
            / math.sqrt(df * math.pi) * (1.0 + t * t / df) ** (-(df + 1) / 2.0))


def _ada_simpson(f, a, b, tol=1e-11, maxdepth=50):
    def rec(a, b, fa, fb, fc, whole, depth):
        c = (a + b) / 2.0
        lm, rm = (a + c) / 2.0, (c + b) / 2.0
        flm, frm = f(lm), f(rm)
        left = (c - a) / 6.0 * (fa + 4.0 * flm + fc)
        right = (b - c) / 6.0 * (fc + 4.0 * frm + fb)
        if depth <= 0 or abs(left + right - whole) < 15.0 * tol:
            return left + right + (left + right - whole) / 15.0
        return (rec(a, c, fa, fc, flm, left, depth - 1)
                + rec(c, b, fc, fb, frm, right, depth - 1))
    fa, fb = f(a), f(b)
    c = (a + b) / 2.0
    return rec(a, b, fa, fb, f(c), (b - a) / 6.0 * (fa + 4.0 * f(c) + fb), maxdepth)


def ref_t_two_sided_p(t, df):
    """Selftest reference: 2 * integral_t^{t+60} of the t density."""
    t = abs(t)
    return 2.0 * _ada_simpson(lambda x: _t_pdf(x, df), t, t + 60.0)


def binom_two_sided(k, n):
    """Exact two-sided sign-test p: 2*min(P[X<=k], P[X>=k]), X~Bin(n,1/2),
    capped at 1.0 (the convention r9 used, replication.md §Paired exact sign
    tests)."""
    if n <= 0:
        return 1.0
    pl = sum(math.comb(n, i) for i in range(0, k + 1)) / 2.0 ** n
    pr = sum(math.comb(n, i) for i in range(k, n + 1)) / 2.0 ** n
    return min(1.0, 2.0 * min(pl, pr))


def mcnemar_exact(b, c):
    """Exact two-sided McNemar p: sum of Bin(b+c, 1/2) point probabilities that
    are <= P(min(b,c)) — the standard exact conditional form.

    Note: for the symmetric p=1/2 binomial this is provably identical to the
    2*P[X<=min(b,c)] two-tailed form (the <= threshold selects {0..k} and its
    mirror {n-k..n}, which carry equal mass), so the two readings of the test
    cannot disagree on any input — the choice here is a documentation matter,
    not a behavioural one.
    """
    n = b + c
    if n <= 0:
        return 1.0
    probs = [math.comb(n, i) / 2.0 ** n for i in range(n + 1)]
    thr = probs[min(b, c)]
    return min(1.0, sum(p for p in probs if p <= thr + 1e-15))


# --------------------------------------------------------------------------
# analysis
# --------------------------------------------------------------------------
def _read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _parse_bundle(text):
    """prereg-bundle.sha256 -> list of (hash, path) in file order."""
    entries = []
    for line in text.splitlines():
        m = re.match(r"^([0-9a-f]{64})\s+(\S+)$", line.strip())
        if m:
            entries.append((m.group(1), m.group(2)))
    return entries


def _parse_version(text):
    """ordering.log carries the `bundle sha256 file <path> (vN)` provenance line."""
    for line in text.splitlines():
        m = re.match(r"^bundle sha256 file (\S+) \((v\d+)\)$", line.strip())
        if m:
            return m.group(2)
    return None


def _parse_ordering(text):
    times = {}
    for line in text.splitlines():
        m = re.match(r"^(pre-hash|post-hash)\s+(\S+)$", line.strip())
        if m:
            times[m.group(1)] = m.group(2)
    return times


def analyze(recs, bundle_text, ordering_text, results_name):
    """Return the full analysis_r11.md text. Pure function of its arguments."""
    L = []

    descriptors = [r for r in recs if r.get("cell") == "descriptors"]
    meta = [r for r in recs if r.get("cell") == "meta"]
    graded = [r for r in recs if r.get("cell") in GRADED_CELLS and "nwrong" in r]
    acks = [r for r in recs if str(r.get("cell", "")).endswith("-ack")]
    fillers = [r for r in recs if r.get("cell") == "filler"]
    errors = [r for r in recs if r.get("cell") == "error"]

    # ---- per-cell tables --------------------------------------------------
    nwrong_by = {c: {} for c in GRADED_CELLS}   # cell -> pid -> turn -> nwrong
    for r in graded:
        nwrong_by[r["cell"]].setdefault(r["pid"], {})[r["turn"]] = r["nwrong"]

    def final_rows(cell):
        return [r for r in graded if r["cell"] == cell and r["turn"] == FINAL_TURN]

    def cell_stats(cell):
        fr = sorted(final_rows(cell), key=lambda r: r["pid"])
        allr = [r for r in graded if r["cell"] == cell]
        passes = sum(1 for r in fr if r["ok"])
        mean_final = mean([r["nwrong"] for r in fr]) if fr else float("nan")
        mean_all = mean([r["nwrong"] for r in allr]) if allr else float("nan")
        return passes, len(fr), mean_final, mean_all

    stats = {c: cell_stats(c) for c in GRADED_CELLS}   # 4710, 710

    # ---- primary endpoint: paired diff at shared checkpoints --------------
    pids = sorted(set(nwrong_by["A-CKPT4710"]) & set(nwrong_by["A-CKPT710"]))
    diff_pids, diffs = [], []
    for pid in pids:
        a, b = nwrong_by["A-CKPT4710"][pid], nwrong_by["A-CKPT710"][pid]
        if all(t in a for t in SHARED_TURNS) and all(t in b for t in SHARED_TURNS):
            diff_pids.append(pid)
            diffs.append(mean([b[t] for t in SHARED_TURNS])
                         - mean([a[t] for t in SHARED_TURNS]))
    n = len(diffs)
    d_mean = mean(diffs) if diffs else float("nan")
    d_sd = sample_sd(diffs) if n > 1 else float("nan")
    df = n - 1
    d_se = d_sd / math.sqrt(n) if n else float("nan")
    t_stat = d_mean / d_se if d_se else float("nan")
    p_val = t_two_sided_p(t_stat, df) if df > 0 else float("nan")
    crit = t_crit(df) if df > 0 else float("nan")
    ci_lo, ci_hi = d_mean - crit * d_se, d_mean + crit * d_se

    # ---- exact sign test (ties omitted) -----------------------------------
    wins = sum(1 for d in diffs if d > 0)
    losses = sum(1 for d in diffs if d < 0)
    ties = n - wins - losses
    sign_p = binom_two_sided(wins, wins + losses)
    sign_dir = 0 if wins == losses else (1 if wins > losses else -1)
    t_dir = 0 if d_mean == 0 else (1 if d_mean > 0 else -1)

    # ---- McNemar on final passes -----------------------------------------
    ok_final = {}
    for cell, turn in ((c, FINAL_TURN) for c in GRADED_CELLS):
        ok_final[cell] = {r["pid"]: bool(r["ok"])
                          for r in graded if r["cell"] == cell and r["turn"] == turn}
    common = sorted(set(ok_final["A-CKPT4710"]) & set(ok_final["A-CKPT710"]))
    b_cnt = sum(1 for pid in common if ok_final["A-CKPT4710"][pid] and not ok_final["A-CKPT710"][pid])
    c_cnt = sum(1 for pid in common if not ok_final["A-CKPT4710"][pid] and ok_final["A-CKPT710"][pid])
    mcn_p = mcnemar_exact(b_cnt, c_cnt)

    # ---- audits -----------------------------------------------------------
    len_fin = sum(1 for r in graded if r.get("finish") == "length")
    parse_fail = sum(1 for r in graded if extract_json_block(r.get("raw", "")) is None)
    ack_audit = []
    for cell in ACK_CELLS:
        rows = [r for r in acks if r.get("cell") == cell]
        okc = sum(1 for r in rows if r.get("raw", "").strip().lower().startswith("ok"))
        ack_audit.append((cell, okc, len(rows)))

    # ---- verdict (mechanical) --------------------------------------------
    if not (d_mean > 0):
        branch, verdict = 3, "FALSIFIED"
        why = "diff <= 0 -> branch 3"
    elif p_val < 0.05:
        branch, verdict = 1, "ESTABLISHED"
        why = "diff > 0 and p < 0.05 -> branch 1"
    else:
        branch, verdict = 2, "DIRECTIONAL"
        why = "diff > 0 but p >= 0.05 -> branch 2"
    downgraded = False
    if d_mean > 0 and sign_dir != t_dir:
        downgraded, verdict = True, "DIRECTIONAL"
    verdict_comment = (
        "<!-- verdict rule (mechanical, no judgment): diff=%+.3f (>0: %s), "
        "p=%.4f (<0.05: %s) -> %s; sign-test direction=%+d (wins=%d losses=%d "
        "ties=%d) vs t direction=%+d -> %s -->"
        % (d_mean, "yes" if d_mean > 0 else "no", p_val,
           "yes" if p_val < 0.05 else "no", why, sign_dir, wins, losses, ties,
           t_dir, ("DOWNGRADE to DIRECTIONAL (sign disagreement)" if downgraded
                   else "no downgrade"))
    )

    # ---- Brier ------------------------------------------------------------
    outcomes = [
        (1 if d_mean > 0 else 0,
         "mean paired diff > 0", PRED["p_diff_gt_0"]),
        (1 if (d_mean > 0 and p_val < 0.05) else 0,
         "two-sided paired t p < 0.05 AND diff > 0", PRED["p_sig_and_pos"]),
        (1 if abs(stats["A-CKPT4710"][0] - stats["A-CKPT710"][0]) <= 8 else 0,
         "abs(passes(4710) - passes(710)) <= 8", PRED["p_pass_gap_le_8"]),
    ]
    brier = mean([(p - o) ** 2 for o, _, p in outcomes])

    # ---- ordering / registration -----------------------------------------
    bundle_entries = _parse_bundle(bundle_text)
    bundle_version = _parse_version(bundle_text) or _parse_version(ordering_text) or "?"
    hash_by_file = {os.path.basename(p): h for h, p in bundle_entries}
    times = _parse_ordering(ordering_text)
    req_ts = [r["request_ts"] for r in recs
              if "request_ts" in r and r.get("cell") != "meta"]
    first_ts = min(req_ts) if req_ts else "unavailable"
    hash_names = ", ".join("%s %s" % (os.path.basename(p), h) for h, p in bundle_entries)
    sha_ok = hash_by_file.get("predictions-r11.md") == PREDICTIONS_SHA256

    # ======================= document =====================================
    L.append("# Round 11 analysis — emission-granularity severity dose (powered rerun)")
    L.append("")
    L.append("Generated by `corpus/evidence/round11-power/recompute_r11.py` (stdlib only, "
             "deterministic) from `%s`. Primary endpoint: paired per-pid mean `nwrong` "
             "at the shared checkpoints {7,10}, cells `A-CKPT710` − `A-CKPT4710`. "
             "Single served unit — Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS under the "
             "stack pinned in the `descriptors` record; no cross-model generalization." % results_name)
    L.append("")
    L.append("## Observed results")
    L.append("")
    L.append("Final graded turn is turn %d." % FINAL_TURN)
    L.append("")
    L.append("| Cell | Final passes / %d | Mean final nwrong | Mean nwrong (all graded) |" % PASS_DENOM)
    L.append("|---|---:|---:|---:|")
    for cell in GRADED_CELLS:
        passes, den, mfinal, mall = stats[cell]
        L.append("| %s | %d/%d | %.3f | %.3f |" % (cell, passes, den, mfinal, mall))
    L.append("")
    L.append("%s contains %d descriptors, %d meta, %d graded, %d ack, %d fillers, %d error records"
             % (results_name, len(descriptors), len(meta), len(graded), len(acks),
                len(fillers), len(errors)))
    L.append("")
    L.append("## Primary endpoint — paired severity difference")
    L.append("")
    L.append("Paired mean difference (710 − 4710, shared checkpoints {7,10}): %+.3f sd %.3f n=%d"
             % (d_mean, d_sd, n))
    L.append("Paired t-test: t=%+.3f, df=%d, two-sided p=%.4f" % (t_stat, df, p_val))
    L.append("95%% CI of mean difference: [%+.3f, %+.3f]" % (ci_lo, ci_hi))
    L.append("Exact sign test: wins=%d losses=%d ties=%d two-sided p=%.4f"
             % (wins, losses, ties, sign_p))
    L.append("")
    L.append(verdict_comment)
    L.append("PREREGISTERED VERDICT: %s" % verdict)
    L.append("")
    L.append("## Secondary tests and audits")
    L.append("")
    L.append("McNemar exact test on final passes: b=%d c=%d two-sided p=%.4f"
             % (b_cnt, c_cnt, mcn_p))
    L.append("Finish audit at graded turns: finish=length %d/%d, parse fail %d/%d"
             % (len_fin, len(graded), parse_fail, len(graded)))
    L.append("Ack compliance (raw lowercased startswith ok): A-CKPT4710 %d/%d = %.1f%%; "
             "A-CKPT710 %d/%d = %.1f%%"
             % (ack_audit[0][1], ack_audit[0][2], 100.0 * ack_audit[0][1] / ack_audit[0][2],
                ack_audit[1][1], ack_audit[1][2], 100.0 * ack_audit[1][1] / ack_audit[1][2]))
    L.append("")
    L.append("## Prediction scoring")
    L.append("")
    L.append("| Quantity | Predicted | Observed | Abs error /64 |")
    L.append("|---|---:|---:|---:|")
    L.append("| A-CKPT4710 final passes | %d/64 | %d/64 | %.3f |"
             % (PRED["passes_4710"], stats["A-CKPT4710"][0],
                abs(PRED["passes_4710"] - stats["A-CKPT4710"][0]) / PASS_DENOM))
    L.append("| A-CKPT710 final passes | %d/64 | %d/64 | %.3f |"
             % (PRED["passes_710"], stats["A-CKPT710"][0],
                abs(PRED["passes_710"] - stats["A-CKPT710"][0]) / PASS_DENOM))
    L.append("| Paired severity diff | %+.3f | %+.3f | %.3f |"
             % (PRED["severity_diff"], d_mean, abs(PRED["severity_diff"] - d_mean)))
    L.append("")
    L.append("(Last row's error is in `nwrong` units — the /64 column applies to the "
             "count predictions only.)")
    L.append("Paired severity diff prediction: +0.350 predicted, %+.3f observed, abs error %.3f"
             % (d_mean, abs(PRED["severity_diff"] - d_mean)))
    L.append("Brier score (3 probabilistic predictions): %.3f" % brier)
    L.append("")
    L.append("| # | Event | P | Outcome | (P − outcome)² |")
    L.append("|---|---|---:|---:|---:|")
    for i, (o, label, p) in enumerate(outcomes, 1):
        L.append("| %d | %s | %.2f | %d | %.4f |" % (i, label, p, o, (p - o) ** 2))
    L.append("")
    L.append("## Registration and ordering")
    L.append("")
    L.append("Ordering proof: prereg-bundle.sha256 (%s) — %s; ordering.log pre-hash %s / "
             "post-hash %s; first request_ts %s."
             % (bundle_version, hash_names or "unavailable",
                times.get("pre-hash", "unavailable"), times.get("post-hash", "unavailable"),
                first_ts))
    L.append("Predictions hash check: embedded predictions-r11.md sha256 %s vs "
             "prereg-bundle.sha256 entry %s — %s"
             % (PREDICTIONS_SHA256, hash_by_file.get("predictions-r11.md", "unavailable"),
                "OK" if sha_ok else "MISMATCH"))
    L.append("")
    L.append("Verdict rule applied verbatim: %s" % VERDICT_RULE_NOTE)
    L.append("")
    return "\n".join(L)


# --------------------------------------------------------------------------
# selftest fixtures
# --------------------------------------------------------------------------
TS0 = "2026-09-28T23:10:30Z"
TS1 = "2026-09-28T23:10:31Z"

ACK_TURNS = {
    "A-CKPT4710": [1, 2, 3, 5, 6, 8, 9],       # graded turns {4,7,10} are not acks
    "A-CKPT710": [1, 2, 3, 4, 5, 6, 8, 9],     # graded turns {7,10} are not acks
}


def fixture_records(specs, ack_ok=True, bad_raw=(), nfill=2, ack_raws=None):
    """specs: list of (pid, {"A-CKPT4710": {turn: nwrong}, "A-CKPT710": {...}}).

    ok is derived mechanically: ok == (nwrong == 0). bad_raw lists
    (pid, cell, turn) whose `raw` is unparseable (parse-fail audit).
    ack_ok: bool for both cells, or {cell: bool} per cell.
    ack_raws: {(pid, cell): raw} overrides for ack turns (case/whitespace tests).
    """
    ack_raws = ack_raws or {}
    recs = [{"cell": "descriptors", "request_ts": TS0, "endpoint": "local",
             "models_json": {}, "server": {}, "temp": 0.2, "maxtok": 8192,
             "system_prompt": "x", "seed_scheme": "3000+pid*41",
             "pids": [p for p, _ in specs], "n": len(specs),
             "counterbalance": "pid parity", "machinery_sha256": "0" * 64,
             "probe_lineage": "probe_r11.py"}]
    for pid, nw in sorted(specs, key=lambda x: x[0]):
        recs.append({"cell": "meta", "pid": pid, "init": {}, "ops": [],
                     "truth": {}, "tail_touched": []})
        for cell in GRADED_CELLS:
            for turn in sorted(nw.get(cell, {})):
                v = nw[cell][turn]
                raw = "" if (pid, cell, turn) in bad_raw else "```json\n{}\n```"
                recs.append({"cell": cell, "pid": pid, "turn": turn,
                             "ok": v == 0, "nwrong": v, "got": {}, "want": {},
                             "finish": "stop", "usage": {}, "wall_s": 0.1,
                             "raw": raw, "request_ts": TS1})
        for cell in GRADED_CELLS:
            ok_here = ack_ok.get(cell, True) if isinstance(ack_ok, dict) else ack_ok
            for turn in ACK_TURNS[cell]:
                recs.append({"cell": cell + "-ack", "pid": pid, "turn": turn,
                             "raw": ack_raws.get((pid, cell), "ok" if ok_here else "Done."),
                             "finish": "stop",
                             "usage": {}, "wall_s": 0.1, "request_ts": TS1})
        for _ in range(nfill):
            recs.append({"cell": "filler", "finish": "stop", "usage": {},
                         "wall_s": 0.1, "raw": "ready", "request_ts": TS1})
    return recs


def _line(md, prefix):
    for ln in md.splitlines():
        if ln.startswith(prefix):
            return ln
    raise AssertionError("no line with prefix %r" % prefix)


def _contains(md, needle):
    return any(needle in ln for ln in md.splitlines())


def _expect(cond, msg, failures):
    if not cond:
        failures.append(msg)


def _fixture_md(recs, bundle=DEF_BUNDLE, ordering=DEF_ORDERING):
    """Write the fixture JSONL to a tempfile, run the real file->md path, return text."""
    with tempfile.TemporaryDirectory() as td:
        rp = os.path.join(td, "results-r11.jsonl")
        with open(rp, "w", encoding="utf-8") as fh:
            for r in recs:
                fh.write(json.dumps(r, separators=(",", ":")) + "\n")
        out = os.path.join(td, "analysis_r11.md")
        return run_analysis(rp, bundle, ordering, out)


# independently computed two-sided t tails. No scipy in this environment, so:
#  * df=63/7/10 anchors come from adaptive Simpson quadrature of the Student-t
#    density (tolerance 1e-13, upper limit t+60) in a scratch kernel: it
#    agrees with `betai` to 1.3e-13 (df=63), 7.5e-11 (df=7), 9.9e-14 (df=10).
#  * df=1/2/3 anchors come from the closed forms, checked directly in the
#    selftest (below), which agree with `betai` to ~1e-15.
#  * t crit two-sided 95%: df=63 -> 1.9983405425 (matches the §5 constant
#    1.9983 and the published t-table value), df=3 -> 3.1824463053.
SELFTEST_ANCHORS = [
    ("betai anchor t=2.0 df=63 -> p~0.0500", t_two_sided_p(2.0, 63), 0.049815763699, 1e-9),
    ("betai t=0.7745966692 df=3", t_two_sided_p(0.7745966692414834, 3), 0.495025346060, 1e-9),
    ("betai t=1.9855802013 df=7", t_two_sided_p(1.9855802012591142, 7), 0.087459342600, 1e-8),
    ("betai t=2.3094010768 df=10", t_two_sided_p(2.3094010767585034, 10), 0.043551787774, 1e-9),
    ("t_crit df=63", t_crit(63), 1.9983405425, 1e-6),
    ("t_crit df=63 vs §5 constant", t_crit(63), T_CRIT_DF63_DOC, 1e-3),
    ("t_crit df=3", t_crit(3), 3.1824463053, 1e-6),
]


def selftest():
    failures = []
    checks = []

    # 1) numeric anchors ---------------------------------------------------
    for label, got, want, tol in SELFTEST_ANCHORS:
        checks.append(label)
        _expect(abs(got - want) <= tol, "%s: got %.10f want %.10f (tol %g)" % (label, got, want, tol), failures)

    # independent closed-form t tails (df=1,2,3) cross-checking `betai`
    def _cf_df1(t):
        return 1.0 - (2.0 / math.pi) * math.atan(t)
    def _cf_df2(t):
        return 1.0 - t / math.sqrt(2.0 + t * t)
    def _cf_df3(t):
        th = math.atan(t / math.sqrt(3.0))
        return 1.0 - (2.0 / math.pi) * (th + math.sin(th) * math.cos(th))
    for label, fn, df in (("df=1", _cf_df1, 1), ("df=2", _cf_df2, 2), ("df=3", _cf_df3, 3)):
        for t in (0.25, 0.7745966692414834, 2.0, 4.0):
            checks.append("closed-form %s t=%.2f" % (label, t))
            _expect(abs(t_two_sided_p(t, df) - fn(t)) < 1e-12,
                    "%s t=%.4f: betai %.15f vs closed %.15f" % (label, t, t_two_sided_p(t, df), fn(t)),
                    failures)

    # quadrature reference (different algorithm) + betai symmetry identity
    for df, t in ((63, 2.0), (63, 0.2), (10, 2.3094010767585034), (7, 1.9855802012591142)):
        checks.append("quad reference df=%d t=%.4f" % (df, t))
        got, want = t_two_sided_p(t, df), ref_t_two_sided_p(t, df)
        _expect(abs(got - want) < 1e-8,
                "quad ref df=%d t=%.4f: betai %.12f vs quad %.12f" % (df, t, got, want), failures)
    checks.append("betai symmetry identity I_x(a,b)+I_{1-x}(b,a)=1")
    worst = 0.0
    for df in (1, 2, 3, 7, 10, 63):
        for t in (0.01, 0.05, 0.5, 2.0, 10.0, 25.0):
            x = df / (df + t * t)
            a, b = df / 2.0, 0.5
            worst = max(worst, abs(betai(a, b, x) + betai(b, a, 1.0 - x) - 1.0))
    _expect(worst < 1e-12, "symmetry identity worst deviation %g" % worst, failures)

    # exact-binomial anchors (hand-computed)
    checks.append("binom_two_sided(2,3)==1.0")
    _expect(binom_two_sided(2, 3) == 1.0, "binom_two_sided(2,3) = %r" % binom_two_sided(2, 3), failures)
    checks.append("mcnemar_exact(5,0)==0.0625")
    _expect(abs(mcnemar_exact(5, 0) - 0.0625) < 1e-15, "mcnemar_exact(5,0) = %r" % mcnemar_exact(5, 0), failures)
    checks.append("mcnemar_exact(1,1)==1.0")
    _expect(mcnemar_exact(1, 1) == 1.0, "mcnemar_exact(1,1) = %r" % mcnemar_exact(1, 1), failures)

    # 2) FIX_MIN: n=4, diffs [+1.0, 0.0, +0.5, -0.5] ----------------------
    #    mean +0.25, sample sd 0.645497.. ("0.645" at 3 dp), t=+0.7745966..
    #    -> p 0.4950, CI [-0.777, +1.277], sign wins=2 losses=1 ties=1 -> 1.0000
    #    final passes 4710 3/4, 710 3/4; McNemar b=1 c=1 -> 1.0000
    fx = [
        (201, {"A-CKPT4710": {4: 0, 7: 1, 10: 0}, "A-CKPT710": {7: 2, 10: 1}}),
        (202, {"A-CKPT4710": {4: 0, 7: 0, 10: 0}, "A-CKPT710": {7: 0, 10: 0}}),
        (203, {"A-CKPT4710": {4: 0, 7: 1, 10: 2}, "A-CKPT710": {7: 4, 10: 0}}),
        (204, {"A-CKPT4710": {4: 0, 7: 2, 10: 0}, "A-CKPT710": {7: 1, 10: 0}}),
    ]
    recs = fixture_records(fx, ack_ok={"A-CKPT4710": True, "A-CKPT710": False},
                           bad_raw={(203, "A-CKPT4710", 10)},
                           ack_raws={(201, "A-CKPT4710"): "  OK  \n",
                                     (203, "A-CKPT4710"): "Ok",
                                     (204, "A-CKPT4710"): "OK"})
    md = _fixture_md(recs)

    # independent recomputation of the same quantities from the fixture spec
    iv = [1.0, 0.0, 0.5, -0.5]
    import statistics
    exp_mean = statistics.mean(iv)          # +0.25
    exp_sd = statistics.stdev(iv)           # 0.6454972243679028
    exp_t = exp_mean / (exp_sd / math.sqrt(4))   # 0.7745966692414834

    expected = {
        "results-r11.jsonl contains 1 descriptors, 4 meta, 20 graded, 60 ack, 8 fillers, 0 error records":
            "counts line",
        "Paired mean difference (710 − 4710, shared checkpoints {7,10}): +0.250 sd 0.645 n=4":
            "paired diff line",
        "Paired t-test: t=+0.775, df=3, two-sided p=0.4950":
            "t line",
        "95% CI of mean difference: [-0.777, +1.277]":
            "CI line",
        "Exact sign test: wins=2 losses=1 ties=1 two-sided p=1.0000":
            "sign-test line",
        "McNemar exact test on final passes: b=1 c=1 two-sided p=1.0000":
            "McNemar line",
        "Finish audit at graded turns: finish=length 0/20, parse fail 1/20":
            "finish-audit line",
        "Ack compliance (raw lowercased startswith ok): A-CKPT4710 28/28 = 100.0%; A-CKPT710 0/32 = 0.0%":
            "ack line",
        "PREREGISTERED VERDICT: DIRECTIONAL":
            "verdict line",
        "| A-CKPT4710 | 3/4 | 0.500 | 0.500 |":
            "observed table row 4710",
        "| A-CKPT710 | 3/4 | 0.250 | 1.000 |":
            "observed table row 710",
        "Brier score (3 probabilistic predictions): 0.153":
            "Brier line",
        "Paired severity diff prediction: +0.350 predicted, +0.250 observed, abs error 0.100":
            "severity-diff prediction line",
        "| A-CKPT4710 final passes | 15/64 | 3/64 | 0.188 |":
            "point table row 4710",
        "| A-CKPT710 final passes | 13/64 | 3/64 | 0.156 |":
            "point table row 710",
        "| Paired severity diff | +0.350 | +0.250 | 0.100 |":
            "point table row diff",
        "| 1 | mean paired diff > 0 | 0.78 | 1 | 0.0484 |":
            "Brier outcome row 1",
        "| 2 | two-sided paired t p < 0.05 AND diff > 0 | 0.50 | 0 | 0.2500 |":
            "Brier outcome row 2",
        "| 3 | abs(passes(4710) - passes(710)) <= 8 | 0.60 | 1 | 0.1600 |":
            "Brier outcome row 3",
    }
    for want_line, label in expected.items():
        checks.append("FIX_MIN " + label)
        _expect(_contains(md, want_line), "FIX_MIN %s missing: %r" % (label, want_line), failures)

    # the fixture's own statistics (independent of the engine's formatting)
    checks.append("FIX_MIN independent mean/sd/t")
    _expect(abs(exp_mean - 0.25) < 1e-12 and abs(exp_sd - 0.6454972243679028) < 1e-12
            and abs(exp_t - 0.7745966692414834) < 1e-12,
            "fixture arithmetic drifted: mean=%r sd=%r t=%r" % (exp_mean, exp_sd, exp_t), failures)
    checks.append("FIX_MIN verdict branch comment (DIRECTIONAL, no downgrade)")
    _expect(_contains(md, "diff=+0.250 (>0: yes), p=0.4950 (<0.05: no) -> diff > 0 but p >= 0.05 -> branch 2")
            and _contains(md, "no downgrade"),
            "FIX_MIN verdict comment did not report branch 2 / no downgrade", failures)

    # 3) FIX_DIRECTIONAL: n=8, diffs [+1,+1,+1,+1,-0.5,0,0,0] -------------
    #    mean +0.4375, sd 0.62321, t=1.9855802013 df=7 -> p=0.0875 (>=0.05),
    #    wins=4 losses=1 ties=3 -> sign direction agrees -> branch 2.
    fxd = [
        (301, {"A-CKPT4710": {7: 0, 10: 0}, "A-CKPT710": {7: 1, 10: 1}}),
        (302, {"A-CKPT4710": {7: 0, 10: 0}, "A-CKPT710": {7: 1, 10: 1}}),
        (303, {"A-CKPT4710": {7: 0, 10: 0}, "A-CKPT710": {7: 1, 10: 1}}),
        (304, {"A-CKPT4710": {7: 0, 10: 0}, "A-CKPT710": {7: 1, 10: 1}}),
        (305, {"A-CKPT4710": {7: 1, 10: 1}, "A-CKPT710": {7: 1, 10: 0}}),
        (306, {"A-CKPT4710": {7: 2, 10: 2}, "A-CKPT710": {7: 2, 10: 2}}),
        (307, {"A-CKPT4710": {7: 3, 10: 3}, "A-CKPT710": {7: 3, 10: 3}}),
        (308, {"A-CKPT4710": {7: 4, 10: 4}, "A-CKPT710": {7: 4, 10: 4}}),
    ]
    mdd = _fixture_md(fixture_records(fxd))
    checks.append("FIX_DIRECTIONAL line values")
    _expect(_contains(mdd, "Paired mean difference (710 − 4710, shared checkpoints {7,10}): +0.438 sd 0.623 n=8"),
            "FIX_DIRECTIONAL diff line: %r" % _line(mdd, "Paired mean difference"), failures)
    _expect(_contains(mdd, "Paired t-test: t=+1.986, df=7, two-sided p=0.0875"),
            "FIX_DIRECTIONAL t line: %r" % _line(mdd, "Paired t-test"), failures)
    _expect(_contains(mdd, "Exact sign test: wins=4 losses=1 ties=3 two-sided p=0.3750"),
            "FIX_DIRECTIONAL sign line: %r" % _line(mdd, "Exact sign test"), failures)
    checks.append("FIX_DIRECTIONAL branch 2, no downgrade")
    _expect(_line(mdd, "PREREGISTERED VERDICT: ") == "PREREGISTERED VERDICT: DIRECTIONAL"
            and _contains(mdd, "-> branch 2") and _contains(mdd, "no downgrade"),
            "FIX_DIRECTIONAL did not take branch 2 without downgrade", failures)

    # 4) FIX_DOWNGRADE: n=11, 5 x +5.0 wins and 6 x -0.5 losses -----------
    #    mean=+2.0, sd=2.8722813, t=2.3094010768 df=10 -> p=0.0436 (<0.05):
    #    branch 1 would be ESTABLISHED, but wins=5 < losses=6 -> sign
    #    direction is negative -> downgrade to DIRECTIONAL.
    fxdg = []
    for i, pid in enumerate(range(401, 407)):        # six losses of -0.5
        fxdg.append((pid, {"A-CKPT4710": {7: 1, 10: 1}, "A-CKPT710": {7: 1, 10: 0}}))
    for pid in range(407, 412):                      # five wins of +5.0
        fxdg.append((pid, {"A-CKPT4710": {7: 0, 10: 0}, "A-CKPT710": {7: 5, 10: 5}}))
    mddg = _fixture_md(fixture_records(fxdg))
    checks.append("FIX_DOWNGRADE line values")
    _expect(_contains(mddg, "Paired mean difference (710 − 4710, shared checkpoints {7,10}): +2.000 sd 2.872 n=11"),
            "FIX_DOWNGRADE diff line: %r" % _line(mddg, "Paired mean difference"), failures)
    _expect(_contains(mddg, "Paired t-test: t=+2.309, df=10, two-sided p=0.0436"),
            "FIX_DOWNGRADE t line: %r" % _line(mddg, "Paired t-test"), failures)
    _expect(_contains(mddg, "Exact sign test: wins=5 losses=6 ties=0 two-sided p=1.0000"),
            "FIX_DOWNGRADE sign line: %r" % _line(mddg, "Exact sign test"), failures)
    checks.append("FIX_DOWNGRADE branch 1 downgraded to DIRECTIONAL")
    _expect(_line(mddg, "PREREGISTERED VERDICT: ") == "PREREGISTERED VERDICT: DIRECTIONAL"
            and _contains(mddg, "-> branch 1") and _contains(mddg, "DOWNGRADE to DIRECTIONAL (sign disagreement)"),
            "FIX_DOWNGRADE did not report the sign-disagreement downgrade", failures)

    # 5) FIX_FALSIFIED: diff <= 0 -> FALSIFIED (branch 3) ------------------
    fxf = [
        (501, {"A-CKPT4710": {7: 1, 10: 1}, "A-CKPT710": {7: 0, 10: 0}}),
        (502, {"A-CKPT4710": {7: 1, 10: 1}, "A-CKPT710": {7: 0, 10: 0}}),
    ]
    mdf = _fixture_md(fixture_records(fxf))
    checks.append("FIX_FALSIFIED branch 3")
    _expect(_line(mdf, "PREREGISTERED VERDICT: ") == "PREREGISTERED VERDICT: FALSIFIED"
            and _contains(mdf, "-> branch 3"),
            "FIX_FALSIFIED did not take branch 3: %r" % _line(mdf, "PREREGISTERED VERDICT: "), failures)

    # 6) FIX_FULL: n=64-shaped fixture reproduces the §5 census literal ----
    full = []
    for pid in range(201, 265):
        full.append((pid, {"A-CKPT4710": {4: 0, 7: pid % 3, 10: pid % 2},
                           "A-CKPT710": {7: (pid + 1) % 3, 10: (pid + 1) % 2}}))
    mdfull = _fixture_md(fixture_records(full))
    checks.append("FIX_FULL §5 census literal")
    _expect(_contains(mdfull, "results-r11.jsonl contains 1 descriptors, 64 meta, 320 graded, "
                              "960 ack, 128 fillers, 0 error records"),
            "FIX_FULL census line: %r" % _line(mdfull, "results-r11.jsonl contains"), failures)
    checks.append("FIX_FULL n=64 pairing")
    _expect(_contains(mdfull, "Paired mean difference (710 − 4710, shared checkpoints {7,10}):")
            and _line(mdfull, "Paired mean difference").endswith(" n=64"),
            "FIX_FULL pairing line: %r" % _line(mdfull, "Paired mean difference"), failures)
    checks.append("FIX_FULL df=63")
    _expect(_contains(mdfull, "df=63, two-sided p="), "FIX_FULL t line: %r" % _line(mdfull, "Paired t-test"), failures)

    # 7) real preregistration files (if present) ---------------------------
    if os.path.exists(DEF_BUNDLE):
        checks.append("real bundle: predictions-r11.md sha matches frozen constant")
        entries = _parse_bundle(_read_text(DEF_BUNDLE))
        by_file = {os.path.basename(p): h for h, p in entries}
        _expect(len(entries) == 3 and by_file.get("predictions-r11.md") == PREDICTIONS_SHA256,
                "bundle entries=%r" % (entries,), failures)
    if os.path.exists(DEF_ORDERING):
        checks.append("real ordering.log parses times + bundle version")
        otxt = _read_text(DEF_ORDERING)
        times = _parse_ordering(otxt)
        _expect("pre-hash" in times and "post-hash" in times and _parse_version(otxt) == "v1",
                "ordering times=%r version=%r" % (times, _parse_version(otxt)), failures)

    print("selftest: %d checks, %d failures" % (len(checks), len(failures)))
    for f in failures:
        print("FAIL: " + f)
    return 1 if failures else 0


# --------------------------------------------------------------------------
def load_records(path):
    recs = []
    with open(path, "r", encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                recs.append(json.loads(ln))
    return recs


def run_analysis(results_path, bundle_path, ordering_path, out_path):
    """Read results + registration files, write out_path, return the md text."""
    recs = load_records(results_path)
    bundle_text = _read_text(bundle_path) if os.path.exists(bundle_path) else ""
    ordering_text = _read_text(ordering_path) if os.path.exists(ordering_path) else ""
    md = analyze(recs, bundle_text, ordering_text, os.path.basename(results_path))
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(md)
    return md


def main(argv=None):
    ap = argparse.ArgumentParser(description="Round-11 analysis engine (stdlib only).")
    ap.add_argument("--results", default=DEF_RESULTS, help="results-r11.jsonl path")
    ap.add_argument("--out", default=DEF_OUT, help="analysis_r11.md output path")
    ap.add_argument("--bundle", default=DEF_BUNDLE, help="prereg-bundle.sha256 path")
    ap.add_argument("--ordering", default=DEF_ORDERING, help="ordering.log path")
    ap.add_argument("--selftest", action="store_true",
                    help="run synthetic-fixture assertions (no results file needed)")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if not os.path.exists(args.results):
        sys.stderr.write("recompute_r11: missing results file: %s\n" % args.results)
        return 2
    md = run_analysis(args.results, args.bundle, args.ordering, args.out)
    sys.stdout.write("recompute_r11: wrote %s from %d records\n"
                     % (args.out, len(load_records(args.results))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
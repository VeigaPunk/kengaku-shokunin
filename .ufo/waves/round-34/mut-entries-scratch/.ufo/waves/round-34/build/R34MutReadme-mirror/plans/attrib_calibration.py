#!/usr/bin/env python3
"""Interval-calibrated verdicts for the lane's blind attribution instrument
(kengaku round 25, claim C1 — plans/round-25-claims.md:21-66).

Re-derives OFFLINE, from committed receipt bytes only, how accurate
plans/attrib_probe.py's blind leg attribution is, as exact intervals, and
re-verdicts every stored point verdict. Receipts are read, never written; no
journal, endpoint or network is touched.

Population P1 (claims:28-33): corpus/evidence/attrib-r2[123]-*.log under
--root. Per file the scored block is the LAST "## GT + scoring at close" block
(the receipts' own AUTHORITATIVE SCORING SECTION rule,
attrib-r21-impl-ds-trials.log:316); a file without one is trial-only and
reports accuracy 0/0 -> UNTESTED. Authoritative blocks whose trial tables are
identical (same trial ids, predictions, GT, chains) are one sample: the
earliest-scored block is kept and every later one is named as its duplicate
and not counted. When --root has no corpus/evidence directory, every *.log
directly under it is read instead (fixture trees).

Estimates per kept block: overall accuracy; per-leg recall (GT == leg);
per-leg specificity, one-vs-rest (GT != leg and prediction != leg); every
stored TARGET / STREAM TARGET clause; and per leg the predicted share q with
its Rogan-Gladen true-share bound. Legs = the keys of the receipt's blind
`scores={...}` lines plus every leg named in the table.

Frozen rule (claims:35-40): two-sided 95% Clopper-Pearson; PASS iff lower >=
bar, FAIL iff upper < bar, INDETERMINATE otherwise, UNTESTED iff n == 0; bar =
the line's own stated bar (0.80). The receipts' min-n (20 overall, 10 per
target) belongs to the stored point rule: it is re-applied when stored verdicts
are re-derived and reported in --json, never used by the interval rule. Wilson
95% is a sensitivity column, never a verdict. Leg-share bound: min/max of
(q + sp - 1) / (se + sp - 1) over se in [se_L, 1], sp in [sp_L, 1] (CP lower
bounds of recall / specificity), clipped to [0, 1]. The function is monotone in
each coordinate wherever se + sp > 1, so the four corners give the extremes;
when se_L + sp_L - 1 <= 0 the box reaches the pole se + sp = 1 and the bound is
the vacuous [0, 1]. Same plug-in sensitivity/specificity correction as the
judge-bias accounting of S011 (corpus/SOURCES.md:33).

Stored-line re-derivation covers every block, superseded ones included: each
row's `correct` cell, `GT counts`, `ACCURACY`, `TARGET`, `BODY`, `STREAM TARGET`
and the `score_summary` record are recomputed from the block's own rows with
attrib_probe.py cmd_score's arithmetic (plans/attrib_probe.py:965-1106).

Usage:  python3 plans/attrib_calibration.py [--root DIR] [--summary|--json] [--selftest]
Exit:   0 ran and every stored line re-derives from its own rows;
        1 parse/recompute inconsistency or selftest failure;
        2 usage (bad --root, no receipts). INDETERMINATE is a finding, not an error.

Numerics: CP bounds are Beta quantiles — lower = Beta(k, n-k+1) at alpha/2,
upper = Beta(k+1, n-k) at 1-alpha/2 — found by bisection on grader.py's
continued-fraction `betai` (grader.py:879-925, Numerical Recipes 6.4), loaded
from this checkout without running grader's CLI and without writing bytecode.
Sources: Clopper & Pearson 1934, Biometrika 26(4):404-413,
doi:10.1093/biomet/26.4.404; SciPy 1.18.0 BinomTestResult.proportion_ci
("'exact' : Use the Clopper-Pearson exact method") and its binomtest(k=7, n=50)
example, used as a selftest anchor; Wilson 1927, JASA 22(158):209-212; Rogan &
Gladen 1978, Am J Epidemiol 107(1):71-76.
"""
import argparse
import ast
import functools
import glob
import importlib.util
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ALPHA = 0.05
Z95 = 1.959963984540054
VERDICTS = ("PASS", "FAIL", "INDETERMINATE", "UNTESTED")
HEADER = "## GT + scoring at close"
SUMMARY_PREFIX = '{"kind": "score_summary"'
RECORD_PREFIX = '{"kind": "record"'
EXCL = "EXCLUDED:"
DASH = "\u2014"

ROW_RE = re.compile(r"^\|\s*T\d+\s*\|")
SCORES_RE = re.compile(r"\bprediction=\S+ confidence=\S+ scores=(\{.*\})\s*$")
STAMP_RE = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)")
JOURNAL_RE = re.compile(r"--since @(\d+) --until @(\d+)")
GTC_RE = re.compile(r"^GT counts: (\{.*\})$")
ACC_RE = re.compile(r"^ACCURACY: (\d+)/(\d+) = (\d+\.\d{3}) \(bar (\d+\.\d+), "
                    r"min scored n (\d+)\) -> (PASS|FAIL)$")
TGT_RE = re.compile(r"^TARGET (\S+): on-target GT n=(\d+), correct (\d+)/(\d+) = (\d+\.\d{3}) "
                    r"\(bar (\d+\.\d+), min on-target n (\d+)\) -> (PASS|FAIL) \| "
                    r"class GT dist (\{.*\})$")
BODY_RE = re.compile(r"^BODY (\S+): scored n=(\d+), on-target\((\S+)\) n=(\d+), "
                     r"correct (\d+)/(\d+) = (\d+\.\d{3}) \| GT dist (\{.*\})$")
STGT_RE = re.compile(r"^STREAM TARGET (\S+): on-target GT n=(\d+), correct (\d+)/(\d+) = "
                     r"(\d+\.\d{3}) \(bar (\d+\.\d+), min on-target n (\d+)\) -> (PASS|FAIL)$")
# (stored-line key, line prefix, pattern); a prefixed line that fails its
# pattern is a parse inconsistency, never skipped.
STORED = (("stream-target", "STREAM TARGET ", STGT_RE), ("target", "TARGET ", TGT_RE),
          ("body", "BODY ", BODY_RE), ("accuracy", "ACCURACY:", ACC_RE),
          ("gt_counts", "GT counts:", GTC_RE))


# ---------- interval arithmetic ----------
def _load_betai():
    path = os.path.join(REPO, "grader.py")
    spec = importlib.util.spec_from_file_location("_kengaku_grader", path)
    mod = importlib.util.module_from_spec(spec)
    prev = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = prev
    return mod.betai


_BETAI = []


def _betai(a, b, x):
    if not _BETAI:
        _BETAI.append(_load_betai())
    return _BETAI[0](a, b, x)


def _beta_quantile(p, a, b):
    """x with I_x(a, b) = p, by bisection until the bracket is two adjacent floats."""
    lo, hi = 0.0, 1.0
    for _ in range(1100):
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        if _betai(a, b, mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


@functools.lru_cache(maxsize=None)
def clopper_pearson(k, n, alpha=ALPHA):
    """Exact two-sided (1-alpha) Clopper-Pearson interval for k successes in n."""
    if not (isinstance(k, int) and isinstance(n, int) and 0 <= k <= n and 0.0 < alpha < 1.0):
        raise ValueError("clopper_pearson needs integers 0 <= k <= n and 0 < alpha < 1")
    if n == 0:
        return (0.0, 1.0)
    lo = 0.0 if k == 0 else _beta_quantile(alpha / 2.0, k, n - k + 1)
    hi = 1.0 if k == n else _beta_quantile(1.0 - alpha / 2.0, k + 1, n - k)
    return (lo, hi)


def wilson(k, n, z=Z95):
    """Wilson score interval (sensitivity column only)."""
    if n == 0:
        return (0.0, 1.0)
    p, z2 = k / n, z * z
    den = 1.0 + z2 / n
    centre = (p + z2 / (2.0 * n)) / den
    half = z * math.sqrt(p * (1.0 - p) / n + z2 / (4.0 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


def verdict(k, n, bar):
    """The frozen interval rule (claims:35-36)."""
    if n == 0:
        return "UNTESTED"
    lo, hi = clopper_pearson(k, n)
    if lo >= bar:
        return "PASS"
    if hi < bar:
        return "FAIL"
    return "INDETERMINATE"


def rg_bound3(q_lo, q_hi, se_lo, sp_lo):
    """Rogan-Gladen bound with the observed-share arm too (round-25 falsify CritRgBound).

    (q + sp - 1)/(se + sp - 1) is increasing in q, so the extremes sit at the corners of
    [q_lo, q_hi] x [se_lo, 1] x [sp_lo, 1]. With q from the two-sided CP95 interval and se_lo,
    sp_lo one-sided 97.5% CP lower bounds, a union bound gives >= 90% coverage under any
    dependence between the arms (same rows feed all three)."""
    if se_lo + sp_lo - 1.0 <= 0.0:
        return (0.0, 1.0)
    lo = min(rg_bound(q_lo, se_lo, sp_lo)[0], rg_bound(q_hi, se_lo, sp_lo)[0])
    hi = max(rg_bound(q_lo, se_lo, sp_lo)[1], rg_bound(q_hi, se_lo, sp_lo)[1])
    return (lo, hi)


def rg_bound(q, se_lo, sp_lo):
    """Rogan-Gladen true-share bound over se in [se_lo, 1], sp in [sp_lo, 1]."""
    if se_lo + sp_lo - 1.0 <= 0.0:
        return (0.0, 1.0)
    vals = [(q + sp - 1.0) / (se + sp - 1.0) for se in (se_lo, 1.0) for sp in (sp_lo, 1.0)]
    return (min(1.0, max(0.0, min(vals))), min(1.0, max(0.0, max(vals))))


# ---------- receipt parsing ----------
def parse_receipt(path):
    """Every '## GT + scoring at close' block of one receipt, in file order.

    A block runs from its header to its score_summary record (inclusive), else
    to the line before the next '## ' heading / EOF. Row = (trial, cls,
    prediction, gt, gt_class, chain, correct) exactly as printed."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    blocks = []
    for s, head in enumerate(lines):
        if not head.startswith(HEADER):
            continue
        end, j = None, s + 1
        while j < len(lines):
            if lines[j].startswith("## "):
                break
            if lines[j].startswith(SUMMARY_PREFIX):
                end = j
                break
            j += 1
        if end is None:
            end = j - 1
            while end > s and not lines[end].strip():
                end -= 1
        m = STAMP_RE.search(head)
        blk = {"start_line": s + 1, "end_line": end + 1, "rows": [], "row_lines": [],
               "stored_lines": {}, "errors": [], "stamp": m.group(1) if m else None,
               "journal": None, "frozen_sha256": None, "instrument_sha256": None}
        for i in range(s + 1, end + 1):
            raw, ln = lines[i].rstrip(), i + 1
            if ROW_RE.match(raw):
                cells = [c.strip() for c in raw.strip("|").split("|")]
                if len(cells) == 7:
                    blk["rows"].append(tuple(cells))
                    blk["row_lines"].append(ln)
                else:
                    blk["errors"].append("%d: table row has %d cells, want 7" % (ln, len(cells)))
                continue
            if raw.startswith("# journal command:"):
                mj = JOURNAL_RE.search(raw)
                blk["journal"] = "@%s..@%s" % mj.groups() if mj else raw[len("# journal command:"):].strip()
            elif raw.startswith("# frozen table re-verified at scoring:"):
                blk["frozen_sha256"] = raw.split()[-1]
            elif raw.startswith("# instrument sha256 at scoring:"):
                blk["instrument_sha256"] = raw.split()[-1]
            key = None
            if raw.startswith(SUMMARY_PREFIX):
                key = "score_summary"
            else:
                for name, prefix, rx in STORED:
                    if raw.startswith(prefix):
                        mm = rx.match(raw)
                        if mm is None:
                            blk["errors"].append("%d: unparsed stored line %r" % (ln, raw[:60]))
                        else:
                            key = name if name in ("accuracy", "gt_counts") else "%s:%s" % (name, mm.group(1))
                        break
            if key:
                if key in blk["stored_lines"]:
                    blk["errors"].append("%d: second %s line in one block" % (ln, key))
                blk["stored_lines"][key] = {"line": ln, "text": raw}
        blocks.append(blk)
    return blocks


def _file_facts(path):
    """Leg roster from the blind `scores={...}` lines, and the trial-record count."""
    roster, records, errors = set(), 0, []
    with open(path, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            if line.startswith(RECORD_PREFIX):
                records += 1
            m = SCORES_RE.search(line)
            if m:
                try:
                    roster.update(json.loads(m.group(1)))
                except ValueError:
                    errors.append("%d: unparsable scores={...}" % ln)
    return roster, records, errors


# ---------- stored-line re-derivation (attrib_probe.py cmd_score arithmetic) ----------
def _scored(rows):
    return [r for r in rows if not r[3].startswith(EXCL)]


def _counts(values):
    out = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return out


def _point_verdict(n, acc, bar, min_n):
    return "PASS" if (n >= min_n and acc >= bar) else "FAIL"


def _clause(rows, target, cls=None):
    """(on-target n, correct, accuracy, class GT dist) as cmd_score computes them."""
    sub = rows if cls is None else [r for r in rows if r[1] == cls]
    hit = [r for r in sub if r[3] == target]
    ok = sum(1 for r in hit if r[2] == r[3])
    return len(hit), ok, (ok / len(hit) if hit else 0.0), _counts(r[3] for r in sub), len(sub)


def rederive(block):
    """Recompute every stored line of one block from its own rows -> checks."""
    rows, st = block["rows"], block["stored_lines"]
    scored = _scored(rows)
    checks = []

    def chk(key, line, stored, recomputed):
        checks.append({"key": key, "line": line, "stored": stored,
                       "recomputed": recomputed, "ok": stored == recomputed})

    bad = []  # (trial, line) of rows whose correct / excluded cells disagree with their own GT
    for r, ln in zip(rows, block["row_lines"]):
        want = (DASH, DASH, DASH) if r[3].startswith(EXCL) else ("YES" if r[2] == r[3] else "NO",)
        got = (r[4], r[5], r[6]) if r[3].startswith(EXCL) else (r[6],)
        if got != want:
            bad.append((r[0], ln))
    first = bad[0][1] if bad else (block["row_lines"][0] if rows else block["start_line"])
    chk("rows:correct", first, ("inconsistent " + ",".join("%s@%d" % b for b in bad)) if bad else "consistent",
        "consistent")

    gtc = _counts(r[3] for r in scored)
    k, n = sum(1 for r in scored if r[2] == r[3]), len(scored)
    acc = k / n if n else 0.0
    if "gt_counts" in st:
        try:
            stored_gtc = json.loads(GTC_RE.match(st["gt_counts"]["text"]).group(1))
        except ValueError:
            stored_gtc = "unparsable"
        chk("gt_counts", st["gt_counts"]["line"], stored_gtc, gtc)
    acc_v, bars = None, {}
    if "accuracy" in st:
        m = ACC_RE.match(st["accuracy"]["text"])
        acc_v = _point_verdict(n, acc, float(m.group(4)), int(m.group(5)))
        chk("accuracy", st["accuracy"]["line"],
            [int(m.group(1)), int(m.group(2)), m.group(3), m.group(6)], [k, n, "%.3f" % acc, acc_v])
    else:
        chk("accuracy", block["start_line"], "missing", "ACCURACY line")

    for key in sorted(st):
        kind, _, leg = key.partition(":")
        line, text = st[key]["line"], st[key]["text"]
        if kind == "target":
            m = TGT_RE.match(text)
            bar, min_n = float(m.group(6)), int(m.group(7))
            hn, ok, a, dist, _ = _clause(scored, leg, "force-" + leg)
            v = _point_verdict(hn, a, bar, min_n)
            bars[key] = (bar, min_n, v)
            chk(key, line, [int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5), m.group(8),
                            _literal(m.group(9))], [hn, ok, hn, "%.3f" % a, v, dist])
        elif kind == "body":
            m = BODY_RE.match(text)
            hn, ok, a, dist, ns = _clause(scored, m.group(3), "stream-" + leg)
            chk(key, line, [int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5)),
                            int(m.group(6)), m.group(7), _literal(m.group(8))],
                [ns, m.group(3), hn, ok, hn, "%.3f" % a, dist])
        elif kind == "stream-target":
            m = STGT_RE.match(text)
            bar, min_n = float(m.group(6)), int(m.group(7))
            hn, ok, a, _, _ = _clause(scored, leg)
            v = _point_verdict(hn, a, bar, min_n)
            bars[key] = (bar, min_n, v)
            chk(key, line, [int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5), m.group(8)],
                [hn, ok, hn, "%.3f" % a, v])

    if "score_summary" in st:
        _rederive_summary(st["score_summary"], rows, scored, k, n, acc, gtc, acc_v, bars, chk)
    return checks


def _literal(text):
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return "unparsable"


def _rederive_summary(rec, rows, scored, k, n, acc, gtc, acc_v, bars, chk):
    line = rec["line"]
    try:
        summ = json.loads(rec["text"])
    except ValueError:
        chk("score_summary", line, "unparsable", "JSON object")
        return
    excluded = [[int(r[0][1:]), r[3][len(EXCL):]] for r in rows if r[3].startswith(EXCL)]
    chk("score_summary.scored", line, summ.get("scored"), n)
    chk("score_summary.correct", line, summ.get("correct"), k)
    chk("score_summary.accuracy", line, summ.get("accuracy"), acc)
    chk("score_summary.gt_counts", line, summ.get("gt_counts"), gtc)
    chk("score_summary.excluded", line, summ.get("excluded"), excluded)
    # cmd_score's process verdict is the stream clause only from the instrument
    # that also writes shim_level_verdict (attrib-r23-stream.log:339-348);
    # every other summary carries the shim-level ACCURACY verdict.
    if summ.get("mode") == "stream-trials" and "shim_level_verdict" in summ:
        chk("score_summary.shim_level_verdict", line, summ["shim_level_verdict"], acc_v)
        want = bars.get("stream-target:%s" % summ.get("stream_target"), (None, None, "missing STREAM TARGET"))[2]
        chk("score_summary.verdict", line, summ.get("verdict"), want)
    else:
        chk("score_summary.verdict", line, summ.get("verdict"), acc_v)
    for tgt, stats in sorted((summ.get("target_stats") or {}).items()):
        bar, min_n, _ = bars.get("target:" + tgt, (None, None, None))
        hn, ok, a, dist, ns = _clause(scored, tgt, "force-" + tgt)
        want = {"gt_on_target": hn, "correct": ok, "accuracy": round(a, 3),
                "verdict": _point_verdict(hn, a, bar, min_n) if bar is not None else "missing TARGET line",
                "class_scored": ns, "gt_distribution": dist}
        chk("score_summary.target_stats:" + tgt, line, stats, want)
    if "stream_on_target" in summ:
        chk("score_summary.stream_on_target", line, summ["stream_on_target"],
            _clause(scored, summ.get("stream_target"))[0])
    for name, stats in sorted((summ.get("stream_body_stats") or {}).items()):
        hn, ok, a, dist, ns = _clause(scored, summ.get("stream_target"), "stream-" + name)
        chk("score_summary.stream_body_stats:" + name, line, stats,
            {"scored": ns, "gt_on_target": hn, "correct": ok, "accuracy": round(a, 3),
             "gt_distribution": dist})


# ---------- estimates ----------
def need_n(e, bar, alpha=ALPHA, cap=400):
    """Smallest n with e errors whose CP lower bound reaches bar (Amendment 1 item 3)."""
    for n in range(max(e, 1), cap + 1):
        if n - e >= 0 and clopper_pearson(n - e, n, alpha)[0] >= bar:
            return n
    return None


def _estimate(name, k, n, bar, stored=None, min_n=None):
    """One estimate; bar None = no bar (shares), so no verdict unless n == 0."""
    lo, hi = clopper_pearson(k, n)
    wl, wh = wilson(k, n)
    est = {"estimate": name, "k": k, "n": n, "point": (k / n if n else None),
           "cp95": [lo, hi], "wilson": [wl, wh], "bar": bar, "min_n": min_n,
           "stored": stored, "interval": verdict(k, n, bar) if (n == 0 or bar is not None) else None}
    if est["interval"] == "INDETERMINATE":
        est["need_n"] = need_n(n - k, bar)
    return est


def block_estimates(block, roster):
    """Verdict-bearing estimates and leg-share bounds of one authoritative block."""
    st, scored = block["stored_lines"], _scored(block["rows"])
    m = ACC_RE.match(st["accuracy"]["text"])
    bar = float(m.group(4))
    n = len(scored)
    ests = [_estimate("accuracy", sum(1 for r in scored if r[2] == r[3]), n, bar, m.group(6), int(m.group(5)))]
    legs = sorted(set(roster) | {r[2] for r in scored} | {r[3] for r in scored})
    rec, spec = {}, {}
    for leg in legs:
        pos = [r for r in scored if r[3] == leg]
        rec[leg] = _estimate("recall:" + leg, sum(1 for r in pos if r[2] == leg), len(pos), bar)
    for leg in legs:
        neg = [r for r in scored if r[3] != leg]
        spec[leg] = _estimate("specificity:" + leg, sum(1 for r in neg if r[2] != leg), len(neg), bar)
        if not any(r[2] == leg for r in scored):
            # Amendment 2 (round-25 falsify, CritSpecificity): a leg the instrument never predicted
            # has specificity n/n by construction (the complement of its 0 share) - no verdict.
            spec[leg]["interval"] = None
            spec[leg]["non_firing"] = True
            spec[leg].pop("need_n", None)
    ests += [rec[leg] for leg in legs] + [spec[leg] for leg in legs]
    # bodies = distinct request-body classes behind each estimate (round-25 falsify CritBodiesFlag):
    # a PASS is iid-fragile when fewer distinct bodies than need_n(errors) stand behind it.
    def _mark(est, rows):
        est["bodies"] = len({r[1] for r in rows})
        est["iid_fragile"] = (est["interval"] == "PASS"
                              and est["bodies"] < (need_n(est["n"] - est["k"], bar) or 10 ** 9))
    _mark(ests[0], scored)
    for leg in legs:
        _mark(rec[leg], [r for r in scored if r[3] == leg])
        _mark(spec[leg], [r for r in scored if r[3] != leg])
    for key in sorted(st):
        kind, _, leg = key.partition(":")
        if kind == "target":
            t = TGT_RE.match(st[key]["text"])
            hn, ok, _, _, _ = _clause(scored, leg, "force-" + leg)
            ests.append(_estimate(key, ok, hn, float(t.group(6)), t.group(8), int(t.group(7))))
        elif kind == "stream-target":
            t = STGT_RE.match(st[key]["text"])
            hn, ok, _, _, _ = _clause(scored, leg)
            ests.append(_estimate(key, ok, hn, float(t.group(6)), t.group(8), int(t.group(7))))
    shares = []
    for leg in legs if n else ():
        kq = sum(1 for r in scored if r[2] == leg)
        se_lo, sp_lo = rec[leg]["cp95"][0], spec[leg]["cp95"][0]
        sh = _estimate("share:" + leg, kq, n, None)
        sh.update({"se_lo": se_lo, "sp_lo": sp_lo, "youden_lo": se_lo + sp_lo - 1.0,
                   "rg_cond": list(rg_bound(kq / n, se_lo, sp_lo)),
                   "rg90": list(rg_bound3(sh["cp95"][0], sh["cp95"][1], se_lo, sp_lo))})
        shares.append(sh)
    return ests, shares


# ---------- population analysis ----------
# P1 frozen manifest (plans/round-25-claims.md §C1): the nine committed receipts and
# their sha256 at base 6180e4f. A changed or extra receipt is a mismatch, not new data.
P1_SHA256 = {
    "attrib-r21-ds-trials.log": "7e6102461583c749ff370b5685a8f106da41db2bb1a46e0baf9b4d7384d52ecd",
    "attrib-r21-glm-trials.log": "aa6956065b58ba61a4fdce9c1e47e4bce13b1eeb280cf4c37f29f29e54cc08bb",
    "attrib-r21-impl-ds-trials.log": "1dddb3d62eb3edecddbd469279b2310772a1217fc02a4dc08c32512e2b03daf1",
    "attrib-r21-impl-glm-trials.log": "04c505e4d384ce345ec4ac23462c6392428b0493aaba5c3213a6ce45d2556744",
    "attrib-r22-legs-hyper.log": "f2978c2f0925de915b669fc67ff8eea21f901a531d257f5e04571cead35a7c6d",
    "attrib-r22-legs.log": "fbef90b5ebba327752f040ae0490610cd9b026e52bdbf6f149521ab30764a735",
    "attrib-r22-opencode-trials.log": "179c4e9abea8797e76021c457c3e40e14f196fbb055a45c3a5731bc03e3d7230",
    "attrib-r23-stream-trials.log": "5ce762aa27fc42489510b2d6cc4aaef184dcb0ba6df1a0e4329e7d75ce2112fb",
    "attrib-r23-stream.log": "afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131",
}


def population(root):
    ev = os.path.join(root, "corpus", "evidence")
    if os.path.isdir(ev):
        # any attribution receipt, so a later one (r24+) is flagged by the frozen manifest
        # (round-25 falsify SimplifyCalib F1), not silently ignored
        return sorted(glob.glob(os.path.join(ev, "attrib-r[0-9]*.log")))
    return sorted(glob.glob(os.path.join(root, "*.log")))


def manifest_mismatches(root, paths):
    """Lane mode only: the P1 file set and bytes must equal the frozen manifest."""
    if not os.path.isdir(os.path.join(root, "corpus", "evidence")):
        return []
    out, names = [], {os.path.basename(p): p for p in paths}
    if not set(names) & set(P1_SHA256):
        return []  # fixture trees (selftest) carry no P1 receipt names
    for name in sorted(set(names) | set(P1_SHA256)):
        if name not in P1_SHA256:
            out.append("%s: receipt outside the frozen P1 manifest" % name)
        elif name not in names:
            out.append("%s: frozen P1 receipt missing" % name)
        else:
            with open(names[name], "rb") as fh:
                digest = hashlib.sha256(fh.read()).hexdigest()
            if digest != P1_SHA256[name]:
                out.append("%s: sha256 %s != frozen %s" % (name, digest[:16], P1_SHA256[name][:16]))
    return out


def _table_key(block):
    return tuple(sorted((r[0], r[2], r[3], r[5]) for r in block["rows"]))


def _span(block):
    return "%d-%d" % (block["start_line"], block["end_line"])


def analyze(root, dedup=True):
    """Parse P1 under root, re-derive every stored line, re-verdict, total."""
    out = {"root": root, "rule": {"alpha": ALPHA, "interval": "clopper-pearson", "sensitivity": "wilson",
                                  "z": Z95, "verdict": "PASS iff lo>=bar; FAIL iff hi<bar; "
                                  "INDETERMINATE otherwise; UNTESTED iff n==0"},
           "files": [], "blocks": [], "duplicates": [], "estimates": [], "shares": [],
           "mismatches": [], "totals": {}}
    auth, n_checks = [], 0
    out["mismatches"] += manifest_mismatches(root, population(root))
    for path in population(root):
        rel = os.path.relpath(path, root)
        blocks = parse_receipt(path)
        roster, records, ferr = _file_facts(path)
        out["mismatches"] += ["%s:%s" % (rel, e) for e in ferr]
        out["files"].append({"file": rel, "status": "scored" if blocks else "trial-only",
                             "blocks": len(blocks), "trial_records": records, "roster": sorted(roster),
                             "authoritative": _span(blocks[-1]) if blocks else None})
        for i, b in enumerate(blocks):
            checks = rederive(b)
            n_checks += len(checks)
            failed = [c for c in checks if not c["ok"]]
            scored = _scored(b["rows"])
            out["blocks"].append({
                "file": rel, "lines": _span(b), "role": "P1" if i == len(blocks) - 1 else "superseded",
                "stamp": b["stamp"], "journal": b["journal"], "frozen_sha256": b["frozen_sha256"],
                "instrument_sha256": b["instrument_sha256"], "rows": len(b["rows"]),
                "scored": len(scored), "correct": sum(1 for r in scored if r[2] == r[3]),
                "checks": len(checks), "failed_checks": failed, "errors": b["errors"]})
            out["mismatches"] += ["%s:%s %s: stored=%r recomputed=%r" % (rel, c["line"], c["key"], c["stored"],
                                                                         c["recomputed"]) for c in failed]
            out["mismatches"] += ["%s:%s" % (rel, e) for e in b["errors"]]
        if blocks:
            auth.append((rel, blocks[-1], roster))
        else:
            e = _estimate("accuracy", 0, 0, None)
            e.update({"file": rel, "lines": "-"})
            out["estimates"].append(e)

    groups = {}
    for rel, b, _ in auth:
        groups.setdefault(_table_key(b), []).append((rel, b))
    for rel, b, roster in auth:
        first_rel, first = sorted(groups[_table_key(b)],
                                  key=lambda t: (t[1]["stamp"] or "~", t[0], t[1]["start_line"]))[0]
        if dedup and first is not b:
            differ = [f for f in ("stamp", "journal", "frozen_sha256", "instrument_sha256") if b[f] != first[f]]
            out["duplicates"].append({"duplicate": "%s:%s" % (rel, _span(b)),
                                      "of": "%s:%s" % (first_rel, _span(first)), "header_fields_differ": differ})
            if differ and "accuracy" in b["stored_lines"]:
                # Amendment 1 item 4: the frozen rule counts the identical table once. If the two blocks are
                # distinct executions, the pooled estimates would be these (sensitivity only, no verdict
                # credit). Round-25 falsify (RevDedupSensitivity): print every verdict-bearing estimate.
                pooled = dict(b, rows=list(b["rows"]) + [(r[0] + "b",) + tuple(r[1:]) for r in b["rows"]])
                for e in block_estimates(pooled, roster)[0]:
                    if e["estimate"] == "accuracy" or e["estimate"].startswith(("target:", "recall:")):
                        sens = _estimate("sensitivity:pooled-if-distinct:" + e["estimate"], e["k"], e["n"],
                                         e["bar"])
                        sens["interval_if_pooled"] = sens.pop("interval")
                        sens["interval"] = None
                        sens.pop("need_n", None)
                        sens.update({"file": rel, "lines": _span(b)})
                        out["shares"].append(sens)
            continue
        if "accuracy" not in b["stored_lines"]:
            continue  # already a mismatch (rederive): no stated bar to verdict against
        ests, shares = block_estimates(b, roster)
        for e in ests + shares:
            e.update({"file": rel, "lines": _span(b)})
        out["estimates"].extend(ests)
        out["shares"].extend(shares)
    order = {f["file"]: i for i, f in enumerate(out["files"])}
    out["estimates"].sort(key=lambda e: order[e["file"]])
    out["shares"].sort(key=lambda e: order[e["file"]])

    ests = out["estimates"]
    acc = [e for e in ests if e["estimate"] == "accuracy" and e["lines"] != "-"]
    stored = [e for e in ests if e["stored"]]
    trans = {}  # stored point verdict -> interval verdict
    for e in stored:
        move = "%s>%s" % (e["stored"], e["interval"])
        trans[move] = trans.get(move, 0) + 1
    t = {"files": len(out["files"]),
         "scored_files": sum(1 for f in out["files"] if f["status"] == "scored"),
         "trial_only": sum(1 for f in out["files"] if f["status"] == "trial-only"),
         "blocks": len(out["blocks"]),
         "superseded": sum(1 for b in out["blocks"] if b["role"] == "superseded"),
         "unique_samples": len(acc), "duplicates": len(out["duplicates"]),
         "scored_trials": sum(e["n"] for e in acc), "correct": sum(e["k"] for e in acc),
         "incorrect": sum(e["n"] - e["k"] for e in acc), "estimates": len(ests)}
    t.update({v: sum(1 for e in ests if e["interval"] == v) for v in VERDICTS})
    t.update({"shares": sum(1 for e in out["shares"] if e["estimate"].startswith("share:")),
              "sensitivity_lines": sum(1 for e in out["shares"] if e["estimate"].startswith("sensitivity:")), "n_ge_17": sum(1 for e in ests if e["n"] >= 17),
              "stored_verdicts": len(stored), "transitions": dict(sorted(trans.items())),
              "stored_checks": n_checks, "mismatches": len(out["mismatches"]),
              "unscored_trial_records": sum(f["trial_records"] for f in out["files"]
                                            if f["status"] == "trial-only")})
    out["totals"] = t
    return out


# ---------- rendering ----------
def _f(x):
    return "%.6f" % x


def estimate_line(e):
    line = "%s %s %s %d/%d point=%s cp95=[%s,%s] wilson=[%s,%s] stored=%s interval=%s" % (
        e["file"], e["lines"], e["estimate"], e["k"], e["n"],
        "-" if e["point"] is None else _f(e["point"]), _f(e["cp95"][0]), _f(e["cp95"][1]),
        _f(e["wilson"][0]), _f(e["wilson"][1]), e["stored"] or "-", e["interval"] or "-")
    if "rg_cond" in e:
        # rg_cond: given the observed share (no sampling arm) - a sensitivity bound, not an interval;
        # rg90: with the observed-share CP95 arm, >= 90% by union bound.
        line += " rg_cond=[%s,%s] rg90=[%s,%s] J_lo=%+.6f" % (
            _f(e["rg_cond"][0]), _f(e["rg_cond"][1]), _f(e["rg90"][0]), _f(e["rg90"][1]), e["youden_lo"])
    if e.get("need_n") is not None:
        line += " need_n=%d" % e["need_n"]
    if e.get("interval_if_pooled"):
        line += " if_pooled=%s" % e["interval_if_pooled"]
    if e.get("non_firing"):
        line += " non-firing"
    if "bodies" in e:
        line += " bodies=%d%s" % (e["bodies"], " iid-fragile" if e["iid_fragile"] else "")
    return line


def ordered_lines(res):
    """Estimates then share bounds of each file, in P1 file order (stable sort)."""
    order = {f["file"]: i for i, f in enumerate(res["files"])}
    return sorted(res["estimates"] + res["shares"], key=lambda e: order[e["file"]])


def totals_line(res):
    t = res["totals"]
    keys = ("files", "scored_files", "trial_only", "blocks", "superseded", "unique_samples", "duplicates",
            "scored_trials", "correct", "incorrect", "estimates") + VERDICTS + (
            "shares", "n_ge_17", "stored_verdicts")
    parts = ["%s=%s" % (k, t[k]) for k in keys]
    parts.append("transitions=" + (",".join("%s:%d" % kv for kv in t["transitions"].items()) or "-"))
    parts += ["stored_checks=%d" % t["stored_checks"], "mismatches=%d" % t["mismatches"]]
    parts.append("dup=[" + ",".join("%s=%s" % (d["duplicate"], d["of"]) for d in res["duplicates"]) + "]")
    return "TOTAL " + " ".join(parts)


def render_report(res):
    out = ["attrib_calibration: root %s, P1 = %d file(s)" % (res["root"], len(res["files"]))]
    for f in res["files"]:
        if f["status"] == "trial-only":
            out.append("file %s: trial-only (%d trial records, no '%s' block)" % (f["file"], f["trial_records"], HEADER))
            continue
        out.append("file %s: %d block(s); authoritative = last %s" % (f["file"], f["blocks"], f["authoritative"]))
        for b in res["blocks"]:
            if b["file"] == f["file"]:
                out.append("  block %s [%s] stamp=%s rows=%d scored=%d correct=%d checks %d/%d ok" % (
                    b["lines"], b["role"], b["stamp"], b["rows"], b["scored"], b["correct"],
                    b["checks"] - len(b["failed_checks"]), b["checks"]))
    for d in res["duplicates"]:
        out.append("duplicate: %s == %s (counted once; header fields differ: %s)" % (
            d["duplicate"], d["of"], ",".join(d["header_fields_differ"]) or "none"))
    out += ["MISMATCH " + m for m in res["mismatches"]]
    out += [estimate_line(e) for e in ordered_lines(res)]
    out.append(totals_line(res))
    return "\n".join(out)


# ---------- selftest ----------
def _tail_ge(k, n, p):
    return sum(math.comb(n, j) * p ** j * (1.0 - p) ** (n - j) for j in range(k, n + 1))


def _tail_le(k, n, p):
    return sum(math.comb(n, j) * p ** j * (1.0 - p) ** (n - j) for j in range(0, k + 1))


# (name, function, argument, want, tolerance). Closed forms: k=n lower =
# (alpha/2)^(1/n), k=0 upper = 1-(alpha/2)^(1/n). Power ask, claims:43: the
# printed 0.7940 (n=16) / 0.8049 (n=17) are 4-dp truncations (n=16 is
# 0.794092..., rounding gives 0.7941), so the anchor truncates.
# SciPy 1.18.0 binomtest docs example: binomtest(k=7, n=50, p=0.1).proportion_ci()
# = (0.05819170033997342, 0.26739600249700846), method='exact' (Clopper-Pearson).
# Wilson at k=n: lower = n/(n+z^2); corpus/knowledge/attrib-r21.md:139-140,154
# prints [0.839, 1.000] for 20/20 and [0.851, 1.000] for 22/22.
CP_ANCHORS = [("cp lo 7/50 scipy", "cp_lo", (7, 50), 0.05819170033997342, 1e-9),
              ("cp hi 7/50 scipy", "cp_hi", (7, 50), 0.26739600249700846, 1e-9),
              ("cp lo 16/16 power ask", "cp_lo_trunc4", (16, 16), 0.7940, 1e-12),
              ("cp lo 17/17 power ask", "cp_lo_trunc4", (17, 17), 0.8049, 1e-12),
              ("wilson lo 20/20 knowledge", "wilson_lo3", (20, 20), 0.839, 1e-12),
              ("wilson lo 22/22 knowledge", "wilson_lo3", (22, 22), 0.851, 1e-12)]
for _n in range(1, 41):
    CP_ANCHORS.append(("cp lo %d/%d closed form" % (_n, _n), "cp_lo", (_n, _n), (ALPHA / 2) ** (1.0 / _n), 1e-12))
    CP_ANCHORS.append(("cp hi 0/%d closed form" % _n, "cp_hi", (0, _n), 1.0 - (ALPHA / 2) ** (1.0 / _n), 1e-12))
    CP_ANCHORS.append(("wilson lo %d/%d closed form" % (_n, _n), "wilson_lo", (_n, _n), _n / (_n + Z95 * Z95), 1e-12))

_ANCHOR_FN = {"cp_lo": lambda k, n: clopper_pearson(k, n)[0], "cp_hi": lambda k, n: clopper_pearson(k, n)[1],
              "cp_lo_trunc4": lambda k, n: math.floor(clopper_pearson(k, n)[0] * 1e4) / 1e4,
              "wilson_lo": lambda k, n: wilson(k, n)[0], "wilson_lo3": lambda k, n: round(wilson(k, n)[0], 3)}


def anchor_failures(anchors):
    return ["%s: got %.15g want %.15g" % (name, _ANCHOR_FN[fn](*arg), want)
            for name, fn, arg, want, tol in anchors if abs(_ANCHOR_FN[fn](*arg) - want) > tol]


def _fx_file(legs, blocks):
    head = ["# fixture receipt (attrib_calibration selftest; syntax of attrib-r23-stream.log:194-256)",
            '{"kind": "record", "trial_id": 1, "class": "std", "prediction": "%s"}' % legs[0],
            "    prediction=%s confidence=0.500 scores=%s" % (legs[0], json.dumps({l: 1.0 for l in legs}))]
    return "\n".join(head + [""] + blocks) + "\n"


def _fx_block(stamp, rows, tail, journal="@1..@2"):
    since, until = journal.replace("@", "").split("..")
    out = ["## GT + scoring at close (journal read AFTER all trials %s %s)" % (DASH, stamp),
           "# journal command: journalctl --user -u fx-shim --since @%s --until @%s --no-pager" % (since, until),
           "# frozen table re-verified at scoring: sha256 " + "0" * 64, "",
           "| trial | class | prediction | GT | gt_class | chain | correct |", "|---|---|---|---|---|---|---|"]
    for tid, cls, pred, gt, correct in rows:
        if gt.startswith(EXCL):
            out.append("| T%02d | %s | %s | %s | %s | %s | %s |" % (tid, cls, pred, gt, DASH, DASH, DASH))
        else:
            out.append("| T%02d | %s | %s | %s | served | 1/%s OK 200 | %s |" % (tid, cls, pred, gt, gt, correct))
    return "\n".join(out + [""] + tail)


def _fixture_tree(d):
    """Hand-written receipts; every stored line below is typed, not computed."""
    ev = os.path.join(d, "corpus", "evidence")
    os.makedirs(ev)
    force_rows = [(i, "force-b", "b", "b", "YES") if i % 2 else (i, "force-c", "a", "a", "YES")
                  for i in range(1, 21)]
    force_tail = ['GT counts: {"b": 10, "a": 10}',
                  "ACCURACY: 20/20 = 1.000 (bar 0.80, min scored n 20) -> PASS",
                  "TARGET b: on-target GT n=10, correct 10/10 = 1.000 (bar 0.80, min on-target n 10) -> PASS"
                  " | class GT dist {'b': 10}",
                  "TARGET c: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL"
                  " | class GT dist {'a': 10}",
                  '{"kind": "score_summary", "shim": "fx", "accuracy": 1.0, "scored": 20, "correct": 20, '
                  '"verdict": "PASS", "gt_counts": {"b": 10, "a": 10}, "excluded": [], "mode": "force-trials", '
                  '"target_stats": {"b": {"gt_on_target": 10, "correct": 10, "accuracy": 1.0, "verdict": "PASS", '
                  '"class_scored": 10, "gt_distribution": {"b": 10}}, "c": {"gt_on_target": 0, "correct": 0, '
                  '"accuracy": 0.0, "verdict": "FAIL", "class_scored": 10, "gt_distribution": {"a": 10}}}}']
    files = {
        "attrib-r21-fx-n17.log": _fx_file(["a", "b"], [_fx_block(
            "2026-01-01T00:00:17Z", [(i, "std", "a", "a", "YES") for i in range(1, 18)],
            ['GT counts: {"a": 17}', "ACCURACY: 17/17 = 1.000 (bar 0.80, min scored n 17) -> PASS",
             '{"kind": "score_summary", "shim": "fx", "accuracy": 1.0, "scored": 17, "correct": 17, '
             '"verdict": "PASS", "gt_counts": {"a": 17}, "excluded": []}'])]),
        "attrib-r21-fx-n16.log": _fx_file(["a", "b"], [_fx_block(
            "2026-01-01T00:00:16Z", [(i, "std", "a", "a", "YES") for i in range(1, 17)],
            ['GT counts: {"a": 16}', "ACCURACY: 16/16 = 1.000 (bar 0.80, min scored n 16) -> PASS"])]),
        "attrib-r21-fx-n0.log": _fx_file(["a", "b"], [_fx_block(
            "2026-01-01T00:00:00Z", [(i, "std", "a", "EXCLUDED:UNMATCHED", "") for i in range(1, 4)],
            ["GT counts: {}", "ACCURACY: 0/0 = 0.000 (bar 0.80, min scored n 20) -> FAIL",
             '{"kind": "score_summary", "shim": "fx", "accuracy": 0.0, "scored": 0, "correct": 0, '
             '"verdict": "FAIL", "gt_counts": {}, "excluded": [[1, "UNMATCHED"], [2, "UNMATCHED"], '
             '[3, "UNMATCHED"]]}'])]),
        "attrib-r22-fx-force.log": _fx_file(["a", "b", "c"], [
            _fx_block("2026-01-01T00:01:00Z",
                      [(1, "force-b", "b", "b", "YES"), (2, "force-c", "b", "a", "NO"),
                       (3, "force-b", "b", "b", "YES"), (4, "force-c", "a", "a", "YES")],
                      ['GT counts: {"b": 2, "a": 2}', "ACCURACY: 3/4 = 0.750 (bar 0.80, min scored n 20) -> FAIL"]),
            "", _fx_block("2026-01-01T00:02:00Z", force_rows, force_tail, "@10..@20")]),
        "attrib-r22-fx-dup.log": _fx_file(["a", "b", "c"], [
            _fx_block("2026-01-01T00:03:00Z", force_rows, force_tail, "@30..@40")]),
        "attrib-r23-fx-fail.log": _fx_file(["a", "b"], [_fx_block(
            "2026-01-01T00:04:00Z",
            [(i, "std", "a", "a", "YES") if i <= 10 else (i, "std", "b", "a", "NO") for i in range(1, 21)],
            ['GT counts: {"a": 20}', "ACCURACY: 10/20 = 0.500 (bar 0.80, min scored n 20) -> FAIL"])]),
        "attrib-r23-fx-stream.log": _fx_file(["a", "b", "c"], [_fx_block(
            "2026-01-01T00:05:00Z",
            [(1, "stream-h", "a", "a", "YES"), (2, "stream-h", "a", "a", "YES")]
            + [(i, "stream-i", "b", "b", "YES") for i in range(3, 7)],
            ['GT counts: {"a": 2, "b": 4}', "ACCURACY: 6/6 = 1.000 (bar 0.80, min scored n 20) -> FAIL",
             "BODY h: scored n=2, on-target(c) n=0, correct 0/0 = 0.000 | GT dist {'a': 2}",
             "BODY i: scored n=4, on-target(c) n=0, correct 0/0 = 0.000 | GT dist {'b': 4}",
             "STREAM TARGET c: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL",
             '{"kind": "score_summary", "shim": "fx", "accuracy": 1.0, "scored": 6, "correct": 6, '
             '"verdict": "FAIL", "gt_counts": {"a": 2, "b": 4}, "excluded": [], "mode": "stream-trials", '
             '"stream_target": "c", "stream_on_target": 0, "stream_body_stats": {"h": {"scored": 2, '
             '"gt_on_target": 0, "correct": 0, "accuracy": 0.0, "gt_distribution": {"a": 2}}, "i": '
             '{"scored": 4, "gt_on_target": 0, "correct": 0, "accuracy": 0.0, "gt_distribution": '
             '{"b": 4}}}, "shim_level_verdict": "FAIL"}'])]),
        "attrib-r23-fx-trialonly.log": _fx_file(["a", "b"], []),
    }
    for name, text in files.items():
        with open(os.path.join(ev, name), "w", encoding="utf-8") as f:
            f.write(text)
    return ev


# hand-derived expectations for _fixture_tree: (file, estimate) -> (k, n, stored, interval)
FX_EXPECT = {
    ("attrib-r21-fx-n0.log", "accuracy"): (0, 0, "FAIL", "UNTESTED"),
    ("attrib-r21-fx-n16.log", "accuracy"): (16, 16, "PASS", "INDETERMINATE"),
    ("attrib-r21-fx-n17.log", "accuracy"): (17, 17, "PASS", "PASS"),
    ("attrib-r21-fx-n17.log", "recall:b"): (0, 0, None, "UNTESTED"),
    ("attrib-r21-fx-n17.log", "specificity:b"): (17, 17, None, None),  # non-firing leg (Amendment 2)
    ("attrib-r22-fx-force.log", "accuracy"): (20, 20, "PASS", "PASS"),
    ("attrib-r22-fx-force.log", "target:b"): (10, 10, "PASS", "INDETERMINATE"),
    ("attrib-r22-fx-force.log", "target:c"): (0, 0, "FAIL", "UNTESTED"),
    ("attrib-r23-fx-fail.log", "accuracy"): (10, 20, "FAIL", "FAIL"),
    ("attrib-r23-fx-fail.log", "specificity:b"): (10, 20, None, "FAIL"),
    ("attrib-r23-fx-stream.log", "accuracy"): (6, 6, "FAIL", "INDETERMINATE"),
    ("attrib-r23-fx-stream.log", "stream-target:c"): (0, 0, "FAIL", "UNTESTED"),
    ("attrib-r23-fx-trialonly.log", "accuracy"): (0, 0, None, "UNTESTED"),
}
FX_TOTALS = {"files": 8, "trial_only": 1, "blocks": 8, "superseded": 1, "unique_samples": 6,
             "duplicates": 1, "scored_trials": 79, "correct": 69, "incorrect": 10, "mismatches": 0}


def _fixture_failures(res):
    got = {(os.path.basename(e["file"]), e["estimate"]): (e["k"], e["n"], e["stored"], e["interval"])
           for e in res["estimates"]}
    bad = ["%s %s: got %r want %r" % (f, est, got.get((f, est)), want)
           for (f, est), want in sorted(FX_EXPECT.items()) if got.get((f, est)) != want]
    bad += ["totals.%s: got %r want %r" % (k, res["totals"][k], v)
            for k, v in sorted(FX_TOTALS.items()) if res["totals"][k] != v]
    return bad


def _cli(root):
    p = subprocess.run([sys.executable, os.path.abspath(__file__), "--root", root, "--summary"],
                       capture_output=True, text=True)
    return p.returncode, (p.stderr.strip().splitlines() or [""])[0]


def _mutate(path, old, new):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if text.count(old) != 1:
        raise AssertionError("mutation anchor %r occurs %d times in %s" % (old, text.count(old), path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new))


def selftest():
    results = []

    def record(cid, ok, desc, detail=""):
        results.append(ok)
        print("selftest %s %s: %s%s" % ("ok  " if ok else "FAIL", cid, desc, (" -- " + detail) if detail else ""))

    fails = anchor_failures(CP_ANCHORS)
    record("A1", not fails, "%d known-value anchors (closed forms, SciPy 7/50, power ask, Wilson)"
           % len(CP_ANCHORS), "; ".join(fails[:3]))
    worst = 0.0
    for n in range(0, 41):
        for k in range(0, n + 1):
            lo, hi = clopper_pearson(k, n)
            if k > 0:
                worst = max(worst, abs(_tail_ge(k, n, lo) - ALPHA / 2))
            if 0 < n and k < n:
                worst = max(worst, abs(_tail_le(k, n, hi) - ALPHA / 2))
    record("A2", worst < 1e-9, "betai-inverted CP bounds vs direct binomial tail sums, all 0<=k<=n<=40",
           "worst |tail-0.025| = %.2e" % worst)
    vr = [verdict(0, 0, 0.8), verdict(16, 16, 0.8), verdict(17, 17, 0.8), verdict(10, 20, 0.8),
          # equality boundaries (round-25 falsify MutVerdictBoundary): lo == bar is PASS, hi == bar is not FAIL
          verdict(17, 17, clopper_pearson(17, 17)[0]), verdict(0, 17, clopper_pearson(0, 17)[1])]
    record("A3", vr == ["UNTESTED", "INDETERMINATE", "PASS", "FAIL", "PASS", "INDETERMINATE"],
           "verdict rule anchors incl. lo==bar and hi==bar", repr(vr))
    rg = [rg_bound(0.3, 1.0, 1.0), rg_bound(0.5, 0.9, 0.9), rg_bound(0.5, 0.4, 0.5), rg_bound(0.0, 0.9, 0.9)]
    want_rg = [(0.3, 0.3), (0.4 / 0.9, 0.5 / 0.9), (0.0, 1.0), (0.0, 0.0)]
    record("A4", all(abs(a - b) < 1e-12 for g, w in zip(rg, want_rg) for a, b in zip(g, w)),
           "Rogan-Gladen bound anchors (exact se/sp, interior box, vacuous J<=0, clip)", repr(rg))

    # Round-25 falsify survivors (MutRgBound, MutDedupManifest): pin each branch they bent.
    rg2 = [rg_bound(0.3, 0.8, 0.9), rg_bound(0.95, 0.9, 0.9), rg_bound(0.5, 0.5, 0.5)]
    want2 = [(2.0 / 9.0, 0.375), (17.0 / 18.0, 1.0), (0.0, 1.0)]
    record("A5", all(abs(a - b) < 1e-12 for g, w in zip(rg2, want2) for a, b in zip(g, w)),
           "Rogan-Gladen asymmetric box, upper clip, pole se_lo+sp_lo==1", repr(rg2))
    wl = wilson(7, 50)
    record("A6", abs(wl[0] - 0.06950833427016294) < 1e-12 and abs(wl[1] - 0.2618619371058554) < 1e-12,
           "Wilson 7/50 both endpoints (closed form)", repr(wl))
    ref = os.path.join(HERE, "fixtures", "r25", "cp_reference.tsv")
    worst_ref, rows_ref = 0.0, 0
    with open(ref, encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if not parts or parts[0] == "k":
                continue
            k_, n_, lo_, hi_ = int(parts[0]), int(parts[1]), float(parts[2]), float(parts[3])
            lo, hi = clopper_pearson(k_, n_)
            worst_ref = max(worst_ref, abs(lo - lo_), abs(hi - hi_))
            rows_ref += 1
    record("A7", rows_ref == 861 and worst_ref < 1e-11,
           "CP vs exact-rational cp_reference.tsv, all 861 rows within 1e-11",
           "rows %d worst %.2e" % (rows_ref, worst_ref))
    row = lambda t, p, g: (t, "std", p, g, "served", "1/%s OK 200" % g, "YES" if p == g else "NO")
    b1 = {"rows": [row("T01", "a", "a"), row("T02", "b", "b")]}
    b2 = {"rows": [row("T01", "a", "a"), row("T02", "a", "b")]}
    record("A8", _table_key(b1) != _table_key(b2), "dedup key separates tables that differ only in a prediction")

    with tempfile.TemporaryDirectory(prefix="attrib-cal-selftest-") as tmp:
        green = os.path.join(tmp, "green")
        ev = _fixture_tree(green)
        res = analyze(green)
        fx = _fixture_failures(res)
        record("F1", not fx, "fixture tree: hand-derived verdicts, dedup once, trial-only, last-block rule",
               "; ".join(fx[:3]))
        code, _ = _cli(green)
        record("F2", code == 0, "CLI exit on the consistent fixture tree", "exit %d" % code)

        # red (i): one GT cell flipped -> its stored lines no longer re-derive
        red1 = os.path.join(tmp, "red-flip-gt")
        shutil.copytree(green, red1)
        _mutate(os.path.join(red1, "corpus", "evidence", "attrib-r21-fx-n17.log"),
                "| T05 | std | a | a |", "| T05 | std | a | b |")
        code, first = _cli(red1)
        record("R1", code == 1, "red: flipped GT cell -> exit 1", "exit %d, %s" % (code, first))
        # red (i-b): GT and correct flipped together -> ACCURACY / GT counts no longer re-derive
        red1b = os.path.join(tmp, "red-flip-gt-correct")
        shutil.copytree(green, red1b)
        _mutate(os.path.join(red1b, "corpus", "evidence", "attrib-r21-fx-n17.log"),
                "| T05 | std | a | a | served | 1/a OK 200 | YES |", "| T05 | std | a | b | served | 1/b OK 200 | NO |")
        code, first = _cli(red1b)
        record("R1b", code == 1, "red: GT+correct cell flipped, stored ACCURACY kept -> exit 1",
               "exit %d, %s" % (code, first))
        # red (iv): a stored point verdict word flipped
        red4 = os.path.join(tmp, "red-verdict")
        shutil.copytree(green, red4)
        _mutate(os.path.join(red4, "corpus", "evidence", "attrib-r23-fx-fail.log"),
                "min scored n 20) -> FAIL", "min scored n 20) -> PASS")
        code, first = _cli(red4)
        record("R4", code == 1, "red: stored verdict FAIL->PASS -> exit 1", "exit %d, %s" % (code, first))
        # red (iii): the duplicate block counted twice must break the totals
        dup_fx = _fixture_failures(analyze(green, dedup=False))
        record("R3", bool(dup_fx), "red: duplicate block counted twice -> totals mismatch",
               "; ".join(dup_fx[:2]))
        # red (v): one byte of a frozen P1 receipt changed (lane copy) -> manifest mismatch, exit 1
        lane = os.path.join(tmp, "lane-copy")
        shutil.copytree(os.path.join(REPO, "corpus", "evidence"), os.path.join(lane, "corpus", "evidence"),
                        ignore=shutil.ignore_patterns("round*", "probe-*"))
        code, _ = _cli(lane)
        record("G1", code == 0, "green: unmodified lane copy of P1 passes the frozen manifest", "exit %d" % code)
        with open(os.path.join(lane, "corpus", "evidence", "attrib-r23-stream.log"), "a", encoding="utf-8") as fh:
            fh.write("\n")
        code, first = _cli(lane)
        record("R5", code == 1 and "sha256" in first, "red: one byte added to a frozen P1 receipt -> exit 1",
               "exit %d, %s" % (code, first))
        # red (vi): empty population -> exit 2 (never a vacuous PASS)
        empty = os.path.join(tmp, "empty")
        os.makedirs(os.path.join(empty, "corpus", "evidence"))
        code, _ = _cli(empty)
        record("R6", code == 2, "red: empty population -> exit 2 (no vacuous PASS)", "exit %d" % code)
    # red (ii): a known CP value perturbed must be caught by the anchor check
    perturbed = [(a[0], a[1], a[2], a[3] + 1e-6, a[4]) if a[0] == "cp lo 7/50 scipy" else a for a in CP_ANCHORS]
    new = [f for f in anchor_failures(perturbed) if f not in fails]
    record("R2", len(new) == 1 and new[0].startswith("cp lo 7/50 scipy"),
           "red: known CP value perturbed by 1e-6 -> anchor check fails", "; ".join(new))
    failed = results.count(False)
    print("selftest: %d checks, %d failed" % (len(results), failed))
    return 1 if failed else 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="attrib_calibration.py",
                                 description="Interval-calibrated re-verdict of the attribution receipts (P1).")
    ap.add_argument("--root", default=REPO, help="lane root holding corpus/evidence/ (default: this checkout)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--summary", action="store_true", help="one line per estimate, then a TOTAL line")
    mode.add_argument("--json", action="store_true", help="full machine-readable result")
    ap.add_argument("--selftest", action="store_true", help="known values + fixture red runs")
    args = ap.parse_args(argv)
    try:
        _betai(0.5, 0.5, 0.5)
    except (OSError, ImportError, AttributeError) as exc:
        print("attrib_calibration: cannot load betai from %s: %s" % (os.path.join(REPO, "grader.py"), exc),
              file=sys.stderr)
        return 1
    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("attrib_calibration: --root %s is not a directory" % root, file=sys.stderr)
        return 2
    if not population(root):
        print("attrib_calibration: SETUP: no receipts under %s (corpus/evidence/attrib-r2[123]-*.log, or *.log "
              "when it has no corpus/evidence)" % root, file=sys.stderr)
        return 2
    try:
        res = analyze(root)
    except (OSError, UnicodeError) as exc:
        print("attrib_calibration: SETUP: unreadable receipt: %s" % exc, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(res, indent=1))
    elif args.summary:
        for m in res["mismatches"]:
            print("MISMATCH " + m, file=sys.stderr)
        print("\n".join([estimate_line(e) for e in ordered_lines(res)] + [totals_line(res)]))
    else:
        print(render_report(res))
    return 1 if res["mismatches"] else 0


if __name__ == "__main__":
    sys.exit(main())

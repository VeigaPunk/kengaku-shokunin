#!/usr/bin/env python3
"""kengaku round-11 hermetic replay extension — DRAFT (integration owner: L1).

Drop-in extension of `grader.py` (round-10 gate, repo root). It replays the
round-11 evidence OFFLINE (no endpoint, no network) and re-derives every stored
number from committed bytes. L1 integrates it into grader.py; this file edits
nothing else.

    python3 corpus/evidence/round11-fleet/grader_r11_draft.py   # fixture selftest

What `grade_r11` verifies (given `recs`, `md_text`, `runlog_text`, `rep`):
  META     every meta record regenerates exactly from `gen_problem(3000+pid*41)`
           for pids 201-264, and stored truth/tail_touched re-derive from
           init+ops (ported gen_problem / states_along / tail_touched).
  REPLAY   every graded record's stored got/want/ok/nwrong re-derives from its
           stored `raw` (extract_json_block) graded against meta truth, with
           want == truth[turn-1]; per-cell turn sets equal the checkpoint sets.
  CENSUS   the record census equals probe_plan_r11.md §4 (1 descriptors, 64
           meta, 192/128 graded, 448/512 ack, 128 fillers, 0 error, 1473 total,
           128 jobs, 1409 requests). A census mismatch is a MISMATCH, never a
           die, so a partial run still grades.
  SUMMARY  the two `run.log` `=== SUMMARY ===` cell lines re-derive from the
           turn-10 graded records.
  ANALYSIS every analysis_r11.md §5 stored line re-derives: observed table
           (passes + both means), census sentence, paired diff mean/sd/n, t/df/p,
           95% CI, exact sign test, McNemar, finish audit, ack compliance,
           PREREGISTERED VERDICT (mechanical rule + sign-agreement downgrade),
           Brier, severity-diff prediction line, point-prediction scoring table.

`check_r11_ordering(rep)` verifies the preregistration discipline:
  HASHES   every line of prereg-bundle.sha256 matches a recomputed sha256 of the
           named repo-relative bundle file (hermetic: no sha256sum subprocess);
           the three bundle paths are exactly probe_plan_r11.md /
           power_analysis_r11.md / predictions-r11.md, all under
           corpus/evidence/round11-power/.
  TIMES    ordering.log post-hash time <= the first request_ts in
           results-r11.jsonl (plain string compare on the Z-timestamps), and the
           record carrying that first request_ts is the descriptors record.

Lineage / textual copies (say so explicitly, per brief): KEYS, extract_json_block,
sim_apply, tail_touched, gen_problem, states_along, grade_state, Report, die,
read_text, load_jsonl and parse_runlog_summary are copied verbatim from
grader.py (its own header notes those are ports of horizon.py/analyze.py).
probe_r11.py is a byte-identical copy of round9-replication/replicate.py, so its
gen_problem semantics are grader.py's.

Stats: stdlib only and deterministic. Paired t p-value via an incomplete-beta
continued fraction (betacf/betai, Numerical-Recipes style) with df = n-1;
exact sign test and McNemar via math.comb; t-quantile for the CI via bisection
on the two-sided p (documented pin C1 below).

Ambiguity pins (the §5 templates leave these under-specified; recorded so L1 and
recompute_r11.py agree):
  A1  decimal-valued stored fields are compared NUMERICALLY at the template's
      precision (3 or 4 dp); U+2212 MINUS and U+00B1 PLUS-MINUS are normalised.
      Fraction-valued fields ("X/64") are compared as exact strings.
  B1  `Paired t-test` df is n-1 (63 for n=64); the t quantile used for the CI is
      found by bisection on the same two-sided p to 1e-10 (df=63 -> 1.9983405).
      recompute_r11.py MUST use the same (or a table value accurate to >1e-6).
  C1  scoring-table rows are matched positionally to the three point predictions
      in predictions-r11.md order (4710 passes, 710 passes, severity diff).
  D1  "Paired severity diff prediction" observed value is pinned as the signed
      3-dp mean diff; abs error = |predicted - observed| (predicted read from
      predictions-r11.md).
  E1  Brier P-values are parsed from predictions-r11.md rows 1..3 by label.

-----------------------------------------------------------------------------
INTEGRATION STEPS FOR L1 (exact)
-----------------------------------------------------------------------------
 1. Paste the module body (everything below the `DRAFT-CODE` marker, minus the
    `-- selftest --` fixture block) into grader.py, after `grade_r9`. Keep the
    ports (`KEYS`, `extract_json_block`, `sim_apply`, `tail_touched`,
    `gen_problem`, `states_along`, `grade_state`) OUT — grader.py already has
    them; delete this file's copies to avoid a second definition.
 2. DEFAULTS: add
        "r11_jsonl":  os.path.join(HERE, "corpus/evidence/round11-power/results-r11.jsonl"),
        "r11_md":     os.path.join(HERE, "corpus/evidence/round11-power/analysis_r11.md"),
        "r11_runlog": os.path.join(HERE, "corpus/evidence/round11-power/run.log"),
    and sidecar constants (mirroring R9_PRED/R9_PRED_SHA/R9_ORDERING):
        R11_PRED     = os.path.join(HERE, "corpus/evidence/round11-power/predictions-r11.md"),
        R11_SHA      = os.path.join(HERE, "corpus/evidence/round11-power/prereg-bundle.sha256"),
        R11_ORDERING = os.path.join(HERE, "corpus/evidence/round11-power/ordering.log"),
    then set REPO_ROOT = HERE and R11_* to those DEFAULTS paths (drop the
    _find_repo_root probe; it exists only because this draft lives one dir down).
 3. PINS: add entries AFTER the run lands, md5 taken from the LOG.md landing
    entry (landing convention: byte-identical copy of the /tmp run, md5 recorded
    in LOG.md). Placeholders to fill, do NOT ship them unresolved:
        "r11_jsonl":  ("md5", "<md5 of landed results-r11.jsonl>"),
        "r11_runlog": ("md5", "<md5 of landed run.log>"),
        "r11_md":     ("md5", "<md5 of landed analysis_r11.md>"),
    `check_pins` keys off `paths[key]`, so add all three to the `paths` dict in
    `main` (step 4) for pins to be enforced instead of skipped.
 4. main(): add argparse options `--r11-jsonl/--r11-md/--r11-runlog` defaulting to
    the DEFAULTS entries; add the three to the `paths` dict; add
        for p in (R11_PRED, R11_SHA, R11_ORDERING):
            if not os.path.isfile(p): die(f"missing sidecar file: {p}")
    and after `grade_r9(...)`:
        grade_r11(r11_recs, read_text(paths["r11_md"]),
                  read_text(paths["r11_runlog"]), rep)
        check_r11_ordering(rep)
    with `r11_recs = load_jsonl(paths["r11_jsonl"])`. `check_r11_ordering` reads
    the bundle/sha/ordering/jsonl through the module-level R11_* paths, so it
    needs no arguments beyond `rep`.
 5. Selftest: add S4/S5 (and optionally S6):
        S4  flip one stored `ok` in the first r11 A-CKPT4710 graded record;
            require exit 1 + "MISMATCH r11.replay.A-CKPT4710.ok".
        S5  bump the numerator of the first r11 run.log SUMMARY cell line
            (e.g. "A-CKPT4710: 15/64" -> "A-CKPT4710: 16/64"; use the actual
            landed denominator, do not hardcode the fixture's "2/2");
            require exit 1 + "MISMATCH r11.summary.A-CKPT4710".
        S6  (optional) set ordering.log `post-hash` after the first request_ts;
            require exit 1 + "MISMATCH r11.ordering.hash_precedes_first_request".
 6. CRITICAL selftest-copy fix (basename collision): the r11 runlog lands as
    corpus/evidence/round11-power/run.log, whose basename `run.log` COLLIDES
    with the r8 runlog (round8-horizon/run.log). `run_selftest` currently copies
    DEFAULTS files to `os.path.join(tmp, os.path.basename(DEFAULTS[key]))`, so
    the later copy overwrites the earlier and the S0 control breaks once
    r11_runlog is in DEFAULTS. Change the copy loop to a per-key unique name:
        clean[key] = os.path.join(tmp, key + "__" + os.path.basename(DEFAULTS[key]))
    and pass the same `clean[...]` paths to every `run(...)` call (S0..S6).
    The on-disk filename `run.log` inside round11-power/ is fixed by the hashed
    probe_plan_r11.md §4 — do NOT rename it; fix only the tmp copy names.
 7. Fixture coverage: this draft's `__main__` selftest (temp tree, n=2 pids)
    exercises every check id incl. the census/ordering paths, so L1 can drop the
    fixture block after a green run; keep the betai known-value assertions in the
    module-level `selftest_stats()` so the analytic t-table is re-proved on every
    `--selftest`.

NEVER issues a request to 127.0.0.1:34113 — hermetic, offline, stdlib only.
"""
import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
import tempfile

# ======================= DRAFT-CODE =======================
# (L1: everything from here down, minus the fixture block at the end, is pasted
#  after grade_r9 in grader.py; the ports below are dropped — grader.py has them.)

_HERE = os.path.dirname(os.path.abspath(__file__))


def _find_repo_root():
    """Repo root = nearest ancestor holding corpus/evidence/round11-power/.
    After integration into repo-root grader.py, `HERE` itself qualifies; the
    draft lives in corpus/evidence/round11-fleet/ so it needs three hops up."""
    for cand in (_HERE,
                 os.path.dirname(_HERE),
                 os.path.dirname(os.path.dirname(_HERE)),
                 os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))):
        if os.path.isdir(os.path.join(cand, "corpus", "evidence", "round11-power")):
            return cand
    return _HERE


REPO_ROOT = _find_repo_root()
R11_DIR = os.path.join(REPO_ROOT, "corpus/evidence/round11-power")
R11_JSONL = os.path.join(R11_DIR, "results-r11.jsonl")
R11_ORDERING = os.path.join(R11_DIR, "ordering.log")
R11_SHA = os.path.join(R11_DIR, "prereg-bundle.sha256")
R11_PRED = os.path.join(R11_DIR, "predictions-r11.md")
R11_BUNDLE_FILES = ("probe_plan_r11.md", "power_analysis_r11.md", "predictions-r11.md")

R11_N_PIDS = 64
R11_PIDS = list(range(201, 201 + R11_N_PIDS))
R11_SEED_SCHEME = "3000+pid*41"


def r11_seed(pid):
    return 3000 + pid * 41


CKPT4710 = "A-CKPT4710"
CKPT710 = "A-CKPT710"
CELL_CHECKPOINTS = {CKPT4710: (4, 7, 10), CKPT710: (7, 10)}
SHARED_CHECKPOINTS = (7, 10)
GRADED_TURN = 10
MINUS = "\u2212"
_SIGN_GLYPHS = {"\u2212": "-", "\u2013": "-", "\u2014": "-", "\u00b1": ""}

# §4 census at n=64 (derived checks in _check_census reproduce these).
SECTION4_CENSUS = {
    "descriptors": 1, "meta": 64, "graded": 320, "graded_cells": (192, 128),
    "ack": 960, "ack_cells": (448, 512), "fillers": 128, "errors": 0,
    "total": 1473, "jobs": 128,
}

# ---------- ports (verbatim from grader.py; L1 drops these) ----------
KEYS = ["nails", "bolts", "screws", "washers", "hinges"]


def extract_json_block(text):
    blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", text, re.S)
    if blocks:
        try:
            return json.loads(blocks[-1])
        except Exception:
            pass
    m = re.findall(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]", text, re.S)
    for cand in reversed(m):
        try:
            return json.loads(cand)
        except Exception:
            continue
    return None


def sim_apply(state, op):
    s = dict(state)
    kind = op[0]
    if kind == "SET":
        s[op[1]] = op[2]
    elif kind == "ADD":
        s[op[1]] += op[2]
    elif kind == "SUB":
        s[op[1]] -= op[2]
    elif kind == "MOV":
        s[op[2]] += s[op[1]]
        s[op[1]] = 0
    elif kind == "DEL":
        del s[op[1]]
    elif kind == "NEW":
        s[op[1]] = op[2]
    return s


def tail_touched(ops, mid=7):
    t = {o[1] for o in ops[mid:]}
    t |= {o[2] for o in ops[mid:] if o[0] == "MOV"}
    return t


def gen_problem(seed):
    """Iterative form of horizon.py gen_problem (seed += 977 on rejection),
    identical to analyze.py's gen_problem_exact which matched all r8 metas."""
    retries = 0
    while True:
        rng = random.Random(seed)
        init = {k: rng.randint(3, 30) for k in KEYS}
        extra = ["brackets", "rivets", "gaskets"]
        state, ops = dict(init), []
        while len(ops) < 10:
            live = list(state)
            roll = rng.random()
            if roll < 0.18:
                op = ("SET", rng.choice(live), rng.randint(0, 30))
            elif roll < 0.45:
                op = ("ADD", rng.choice(live), rng.randint(1, 9))
            elif roll < 0.65:
                c = [k for k in live if state[k] > 0]
                if not c:
                    continue
                k = rng.choice(c)
                op = ("SUB", k, rng.randint(1, min(9, state[k])))
            elif roll < 0.80:
                if len(live) < 2:
                    continue
                a, b = rng.sample(live, 2)
                if state[a] == 0:
                    continue
                op = ("MOV", a, b)
            elif roll < 0.90:
                if len(live) < 4:
                    continue
                op = ("DEL", rng.choice(live))
            else:
                if not extra:
                    continue
                op = ("NEW", extra.pop(0), rng.randint(2, 9))
            if op[0] in ("SET", "ADD", "SUB", "DEL") and op[1] not in state:
                continue
            if op[0] == "NEW" and op[1] in state:
                continue
            state = sim_apply(state, op)
            ops.append(op)
        kinds = {o[0] for o in ops}
        if "DEL" not in kinds or "MOV" not in kinds or len(tail_touched(ops)) < 2:
            seed += 977
            retries += 1
            continue
        return init, [list(o) for o in ops], retries


def states_along(init, ops, n=None):
    s, out = dict(init), []
    for op in (ops if n is None else ops[:n]):
        s = sim_apply(s, op)
        out.append(s)
    return out


def grade_state(got, want):
    if not isinstance(got, dict):
        return False, len(want)
    wrong = sum(1 for k in set(got) | set(want) if got.get(k) != want.get(k))
    return got == want, wrong


# ---------- check engine (Report verbatim, erratum not needed for r11) ----------
class Report:
    def __init__(self):
        self.checks = 0
        self.mismatches = []

    def eq(self, cid, stored, recomp):
        self.checks += 1
        if stored != recomp:
            self.mismatches.append(f"MISMATCH {cid}: stored={stored!r} recomputed={recomp!r}")

    def ok(self, cid, condition, detail):
        self.checks += 1
        if not condition:
            self.mismatches.append(f"MISMATCH {cid}: {detail}")


def die(msg):
    print(f"grader: INPUT ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def read_text(path):
    if not os.path.isfile(path):
        die(f"missing file: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        die(f"unreadable file {path}: {e}")


def load_jsonl(path):
    recs = []
    for i, line in enumerate(read_text(path).splitlines(), 1):
        if not line.strip():
            continue
        try:
            recs.append(json.loads(line))
        except json.JSONDecodeError as e:
            die(f"{path}:{i}: invalid JSON: {e}")
    return recs


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_runlog_summary(text):
    if "=== SUMMARY ===" not in text:
        die("run.log has no '=== SUMMARY ===' block")
    block = text.split("=== SUMMARY ===", 1)[1]
    out = {}
    for line in block.splitlines():
        m = re.match(r"^(\S+): (\d+)/(\d+)$", line.strip())
        if m:
            out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    if not out:
        die("run.log SUMMARY block parsed to 0 cells")
    return out


# ---------- stats (stdlib, deterministic) ----------
def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _sd_sample(xs):
    n = len(xs)
    if n < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def _betacf(a, b, x):
    """Continued fraction for the incomplete beta (Numerical Recipes)."""
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
    """Regularised incomplete beta I_x(a,b)."""
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
    """Two-sided Student-t tail probability: I_{df/(df+t^2)}(df/2, 1/2)."""
    return betai(df / 2.0, 0.5, df / (df + t * t))


def t_crit(df, alpha=0.05):
    """Positive t quantile with two-sided tail alpha, by bisection on p."""
    lo, hi = 0.0, 1.0e4
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_two_sided_p(mid, df) > alpha:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _binom_cdf_le(n, k):
    return sum(math.comb(n, j) for j in range(0, k + 1)) / 2.0 ** n


def exact_sign_p(wins, losses):
    n = wins + losses
    if n == 0:
        return 1.0
    le = _binom_cdf_le(n, wins)
    ge = sum(math.comb(n, j) for j in range(wins, n + 1)) / 2.0 ** n
    return min(1.0, 2.0 * min(le, ge))


def exact_mcnemar_p(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2.0 * _binom_cdf_le(n, min(b, c)))


def _num(s):
    t = s.strip()
    for k, v in _SIGN_GLYPHS.items():
        t = t.replace(k, v)
    return float(t)


def recompute_final_ok(r):
    return grade_state(extract_json_block(r.get("raw", "")), r.get("want"))[0] \
        if r.get("want") is not None else False


# ---------- r11 meta / replay ----------
def _build_meta(recs, rep, pids, seed_fn):
    metas = [r for r in recs if r.get("cell") == "meta"]
    rep.eq("r11.meta.count", len(metas), len(pids))
    seen = {}
    for m in metas:
        seen.setdefault(m["pid"], []).append(m)
    rep.ok("r11.meta.unique_pids", all(len(v) == 1 for v in seen.values()),
           f"duplicate meta pids: {[p for p, v in seen.items() if len(v) > 1]}")
    rep.eq("r11.meta.pid_set", sorted(seen), sorted(pids))
    truth_by_pid = {}
    diffs = {"init": [], "ops": [], "truth": [], "tail": [], "seed": []}
    for pid in sorted(pids):
        if pid not in seen:
            continue
        m = seen[pid][0]
        init2, ops2, _ = gen_problem(seed_fn(pid))
        if init2 != m.get("init"):
            diffs["init"].append(pid)
        if ops2 != m.get("ops"):
            diffs["ops"].append(pid)
        truth = states_along(m["init"], [tuple(o) for o in m["ops"]])
        if truth != m.get("truth"):
            diffs["truth"].append(pid)
        if sorted(tail_touched([tuple(o) for o in m["ops"]])) != m.get("tail_touched"):
            diffs["tail"].append(pid)
        truth_by_pid[pid] = truth
    for field in diffs:
        rep.ok(f"r11.meta.regenerate.{field}", not diffs[field],
               f"{len(diffs[field])}/{len(pids)} pids differ: {diffs[field][:4]}")
    return truth_by_pid


def _replay_graded(recs, rep, truth_by_pid):
    cells = {}
    for r in recs:
        c = r.get("cell", "")
        if c in (CKPT4710, CKPT710) and "ok" in r:
            cells.setdefault(c, []).append(r)
    for cell in (CKPT4710, CKPT710):
        rows = cells.get(cell, [])
        rep.eq(f"r11.replay.{cell}.turn_set",
               sorted({r["turn"] for r in rows}), list(CELL_CHECKPOINTS[cell]))
        diffs = {"got": 0, "want": 0, "ok": 0, "nwrong": 0}
        first = None
        for r in rows:
            pid, turn = r["pid"], r["turn"]
            truth = truth_by_pid.get(pid)
            if truth is None or not (1 <= turn <= len(truth)):
                diffs["want"] += 1
                first = first or (pid, turn, "no meta/turn")
                continue
            want_re = truth[turn - 1]
            got_re = extract_json_block(r.get("raw", ""))
            ok_re, nw_re = grade_state(got_re, want_re)
            for field, recomp, stored in (("got", got_re, r.get("got")),
                                          ("want", want_re, r.get("want")),
                                          ("ok", ok_re, r.get("ok")),
                                          ("nwrong", nw_re, r.get("nwrong"))):
                if recomp != stored:
                    diffs[field] += 1
                    first = first or (pid, turn, field)
        for field in ("got", "want", "ok", "nwrong"):
            rep.ok(f"r11.replay.{cell}.{field}", diffs[field] == 0,
                   f"{diffs[field]}/{len(rows)} records differ (first: {first})")
    return cells


def _turn10_recs(cells, cell):
    return [r for r in cells.get(cell, []) if r.get("turn") == GRADED_TURN]


def _check_census(recs, rep, n):
    g4710 = sum(1 for r in recs if r.get("cell") == CKPT4710 and "ok" in r)
    g710 = sum(1 for r in recs if r.get("cell") == CKPT710 and "ok" in r)
    a4710 = sum(1 for r in recs if r.get("cell") == CKPT4710 + "-ack")
    a710 = sum(1 for r in recs if r.get("cell") == CKPT710 + "-ack")
    desc = sum(1 for r in recs if r.get("cell") == "descriptors")
    metas = sum(1 for r in recs if r.get("cell") == "meta")
    fillers = sum(1 for r in recs if r.get("cell") == "filler")
    errors = sum(1 for r in recs if r.get("cell") == "error")
    rep.eq("r11.census.descriptors", desc, 1)
    rep.eq("r11.census.meta", metas, n)
    rep.eq(f"r11.census.graded.{CKPT4710}", g4710, 3 * n)
    rep.eq(f"r11.census.graded.{CKPT710}", g710, 2 * n)
    rep.eq(f"r11.census.ack.{CKPT4710}-ack", a4710, 7 * n)
    rep.eq(f"r11.census.ack.{CKPT710}-ack", a710, 8 * n)
    rep.eq("r11.census.fillers", fillers, 2 * n)
    rep.eq("r11.census.errors", errors, 0)
    rep.eq("r11.census.total_records", len(recs), 1 + 23 * n)
    # §4 counts 1409 endpoint requests = 1 descriptors /v1/models + n*(3+2+7+8+2)
    rep.eq("r11.census.requests", (g4710 + g710) + (a4710 + a710) + fillers + 1, 22 * n + 1)
    rep.eq("r11.census.graded_missing_ok",
           sum(1 for r in recs if r.get("cell") in (CKPT4710, CKPT710) and "ok" not in r), 0)
    rep.eq("r11.census.ack_has_ok",
           sum(1 for r in recs if str(r.get("cell", "")).endswith("-ack") and "ok" in r), 0)
    if n == R11_N_PIDS:
        rep.eq("r11.census.section4",
               (desc, metas, g4710 + g710, a4710 + a710, fillers, errors),
               (SECTION4_CENSUS["descriptors"], SECTION4_CENSUS["meta"],
                SECTION4_CENSUS["graded"], SECTION4_CENSUS["ack"],
                SECTION4_CENSUS["fillers"], SECTION4_CENSUS["errors"]))
        rep.eq("r11.census.section4_total", len(recs), SECTION4_CENSUS["total"])
        rep.eq("r11.census.section4_graded_cells", (g4710, g710), SECTION4_CENSUS["graded_cells"])
        rep.eq("r11.census.section4_ack_cells", (a4710, a710), SECTION4_CENSUS["ack_cells"])
        rep.eq("r11.census.section4_requests", (g4710 + g710) + (a4710 + a710) + fillers + 1, 1409)
    return {"graded": g4710 + g710, "ack": a4710 + a710}


def _check_descriptors(recs, rep, n, pids):
    """§3/§4 experimental-unit descriptor: first record, pins pids + seed scheme."""
    desc = [r for r in recs if r.get("cell") == "descriptors"]
    rep.eq("r11.descriptors.count", len(desc), 1)
    if len(desc) != 1:
        return
    d = desc[0]
    rep.ok("r11.descriptors.request_ts", "request_ts" in d, "descriptors record carries no request_ts")
    rep.eq("r11.descriptors.pids", d.get("pids"), list(pids))
    rep.eq("r11.descriptors.n", d.get("n"), n)
    rep.eq("r11.descriptors.seed_scheme", d.get("seed_scheme"), R11_SEED_SCHEME)
    for field in ("endpoint", "models_json", "server", "temp", "maxtok", "system_prompt",
                  "counterbalance", "machinery_sha256", "probe_lineage"):
        rep.ok(f"r11.descriptors.field.{field}", field in d,
               f"descriptors record missing field {field!r}")


def _check_summary(recs, runlog_text, rep, n):
    stored = parse_runlog_summary(runlog_text)
    rep.eq("r11.summary.cell_set", sorted(stored), sorted([CKPT4710, CKPT710]))
    for cell in (CKPT4710, CKPT710):
        rows = _turn10_recs({cell: [r for r in recs if r.get("cell") == cell and "ok" in r]}, cell)
        passes = sum(1 for r in rows if recompute_final_ok(r))
        rep.eq(f"r11.summary.{cell}", stored.get(cell), (passes, len(rows)))
    jobs = re.findall(r"^\[(\d+)/(\d+)\]", runlog_text, re.M)
    rep.eq("r11.counts.jobs_logged", len(jobs), 2 * n)
    rep.ok("r11.counts.jobs_denominator", all(int(j[1]) == 2 * n for j in jobs),
           f"progress denominators {sorted({j[1] for j in jobs})} != {2 * n}")
    if n == R11_N_PIDS:
        rep.eq("r11.counts.section4_jobs", len(jobs), SECTION4_CENSUS["jobs"])


# ---------- analysis_r11.md ----------
_STORED = {
    "counts": r"results-r11\.jsonl contains (\d+) descriptors, (\d+) meta, (\d+) graded, "
              r"(\d+) ack, (\d+) fillers, (\d+) error records",
    "diff": r"Paired mean difference \(710 [-\u2212\u2013] 4710, shared checkpoints \{7,10\}\): "
            r"([+\-\u2212]?\d+\.\d+) sd (\d+\.\d+) n=(\d+)",
    "t": r"Paired t-test: t=([+\-\u2212\u00b1]?\d+\.\d+), df=(\d+), two-sided p=(\d+\.\d+)",
    "ci": r"95% CI of mean difference: \[([+\-\u2212]?\d+\.\d+), ([+\-\u2212]?\d+\.\d+)\]",
    "sign": r"Exact sign test: wins=(\d+) losses=(\d+) ties=(\d+) two-sided p=(\d+\.\d+)",
    "mcnemar": r"McNemar exact test on final passes: b=(\d+) c=(\d+) two-sided p=(\d+\.\d+)",
    "finish": r"Finish audit at graded turns: finish=length (\d+)/(\d+), parse fail (\d+)/(\d+)",
    "ack": r"Ack compliance \(raw lowercased startswith ok\): "
           r"A-CKPT4710 (\d+)/(\d+) = (\d+\.\d)%; A-CKPT710 (\d+)/(\d+) = (\d+\.\d)%",
    "verdict": r"PREREGISTERED VERDICT: (ESTABLISHED|DIRECTIONAL|FALSIFIED)",
    "brier": r"Brier score \(3 probabilistic predictions\): (\d+\.\d+)",
    "sev": r"Paired severity diff prediction: ([+\-\u2212]?\d+\.\d+) predicted, "
           r"([+\-\u2212\u00b1]?\d+\.\d+) observed, abs error (\d+\.\d+)",
    "obs_header": r"^\| Cell \| Final passes / (\d+) \| Mean final nwrong \| "
                  r"Mean nwrong \(all graded\) \|$",
    "score_header": r"^\| Quantity \| Predicted \| Observed \| Abs error /(\d+) \|$",
    "score_row": r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
    "pred_p4710": r"^\| A-CKPT4710 final \(turn-10\) passes \| (\d+)/(\d+) \|",
    "pred_p710": r"^\| A-CKPT710 final \(turn-10\) passes \| (\d+)/(\d+) \|",
    "pred_pdiff": r"^\| Paired severity diff \(710 [-\u2212\u2013] 4710, mean nwrong at shared "
                  r"\{7,10\}\) \| \*\*\+?(\d+\.\d+)\*\* \|",
    "pred_p1": r"^\| 1 \| mean paired diff > 0 \| (\d+\.\d+) \|$",
    "pred_p2": r"^\| 2 \| two-sided paired t-test p < 0\.05 AND diff > 0 \| (\d+\.\d+) \|$",
    "pred_p3": r"^\| 3 \| (.*) \| (\d+\.\d+) \|$",
}


def _grab(rep, key, text, pattern=None):
    m = re.search(pattern or _STORED[key], text, re.M)
    if m is None:
        rep.ok(f"r11.analysis.{key}.present", False, f"stored line not found: {key}")
    return m


def parse_r11_predictions(ptxt, rep, n):
    """Point + probabilistic predictions from predictions-r11.md (§5 anchors)."""
    out = {}
    for key, field in (("pred_p4710", "p4710"), ("pred_p710", "p710")):
        m = _grab(rep, key, ptxt)
        if m:
            out[field] = int(m.group(1))
            rep.eq(f"r11.predictions.{field}.denominator", int(m.group(2)), n)
    m = _grab(rep, "pred_pdiff", ptxt)
    if m:
        out["pdiff"] = float(m.group(1))
    for key, field in (("pred_p1", "P1"), ("pred_p2", "P2"), ("pred_p3", "P3")):
        m = _grab(rep, key, ptxt)
        if m:
            out[field] = float(m.group(m.lastindex))
    rep.ok("r11.predictions.points_present",
           all(k in out for k in ("p4710", "p710", "pdiff")),
           f"parsed point predictions: {sorted(out)}")
    return out


def _cell_stats(cell_recs, truth_by_pid):
    finals = [r for r in cell_recs if r.get("turn") == GRADED_TURN]
    passes = 0
    fin_nw = []
    for r in finals:
        want = truth_by_pid[r["pid"]][r["turn"] - 1]
        ok_re, nw_re = grade_state(extract_json_block(r.get("raw", "")), want)
        passes += 1 if ok_re else 0
        fin_nw.append(nw_re)
    all_nw = []
    for r in cell_recs:
        want = truth_by_pid[r["pid"]][r["turn"] - 1]
        all_nw.append(grade_state(extract_json_block(r.get("raw", "")), want)[1])
    return passes, _mean(fin_nw), _mean(all_nw)


def _check_analysis(recs, cells, truth_by_pid, md_text, rep, n, pids):
    preg = parse_r11_predictions(read_text(R11_PRED), rep, n)

    # ---- census sentence ----
    m = _grab(rep, "counts", md_text)
    if m:
        stored = tuple(int(m.group(i)) for i in range(1, 7))
        comp = (sum(1 for r in recs if r.get("cell") == "descriptors"),
                sum(1 for r in recs if r.get("cell") == "meta"),
                sum(1 for r in recs if r.get("cell") in (CKPT4710, CKPT710) and "ok" in r),
                sum(1 for r in recs if str(r.get("cell", "")).endswith("-ack")),
                sum(1 for r in recs if r.get("cell") == "filler"),
                sum(1 for r in recs if r.get("cell") == "error"))
        for i, name in enumerate(("descriptors", "meta", "graded", "ack", "fillers", "errors")):
            rep.eq(f"r11.analysis.counts.{name}", stored[i], comp[i])

    # ---- observed table ----
    mh = _grab(rep, "obs_header", md_text)
    if mh:
        rep.eq("r11.analysis.obs.denominator", int(mh.group(1)), n)
    cells_stats = {}
    for cell in (CKPT4710, CKPT710):
        cell_recs = sorted(cells.get(cell, []), key=lambda r: (r["pid"], r["turn"]))
        if not cell_recs:
            continue
        p, mean_final, mean_all = _cell_stats(cell_recs, truth_by_pid)
        cells_stats[cell] = (p, mean_final, mean_all)
        row = re.search(r"^\| " + re.escape(cell) + r" \| (\d+)/(\d+) \| (\d+\.\d{3}) \| (\d+\.\d{3}) \|$",
                        md_text, re.M)
        if not row:
            rep.ok(f"r11.analysis.obs.{cell}.row_present", False, "observed row not found")
            continue
        rep.eq(f"r11.analysis.obs.{cell}.passes", row.group(1), str(p))
        rep.eq(f"r11.analysis.obs.{cell}.denominator", row.group(2), str(n))
        rep.eq(f"r11.analysis.obs.{cell}.mean_final_nwrong", round(_num(row.group(3)), 3),
               round(mean_final, 3))
        rep.eq(f"r11.analysis.obs.{cell}.mean_all_nwrong", round(_num(row.group(4)), 3),
               round(mean_all, 3))
    rep.eq("r11.analysis.obs.cell_set", sorted(cells_stats), sorted([CKPT4710, CKPT710]))

    # ---- per-pid paired diffs at shared checkpoints ----
    nw = {}
    for cell in (CKPT4710, CKPT710):
        nw[cell] = {}
        for r in cells.get(cell, []):
            if r.get("turn") in SHARED_CHECKPOINTS:
                want = truth_by_pid[r["pid"]][r["turn"] - 1]
                nw[cell].setdefault(r["pid"], {})[r["turn"]] = \
                    grade_state(extract_json_block(r.get("raw", "")), want)[1]
    diffs, missing = [], []
    for pid in sorted(pids):
        try:
            d = _mean([nw[CKPT710][pid][t] for t in SHARED_CHECKPOINTS]) \
                - _mean([nw[CKPT4710][pid][t] for t in SHARED_CHECKPOINTS])
        except KeyError:
            missing.append(pid)
            continue
        diffs.append(d)
    rep.eq("r11.paired.pids_missing", missing, [])
    rep.eq("r11.paired.n", len(diffs), len(pids))
    mean_d = _mean(diffs)
    sd_d = _sd_sample(diffs)
    n_d = len(diffs)
    sem = sd_d / math.sqrt(n_d) if n_d else 0.0
    t_stat = mean_d / sem if sem > 0 else 0.0
    p_val = t_two_sided_p(t_stat, n_d - 1) if n_d > 1 else 1.0
    tc = t_crit(n_d - 1, 0.05) if n_d > 1 else 0.0
    lo, hi = mean_d - tc * sem, mean_d + tc * sem

    m = _grab(rep, "diff", md_text)
    if m:
        rep.eq("r11.analysis.diff.mean", round(_num(m.group(1)), 3), round(mean_d, 3))
        rep.eq("r11.analysis.diff.sd", round(_num(m.group(2)), 3), round(sd_d, 3))
        rep.eq("r11.analysis.diff.n", int(m.group(3)), n_d)
    m = _grab(rep, "t", md_text)
    if m:
        rep.eq("r11.analysis.t.t", round(_num(m.group(1)), 3), round(t_stat, 3))
        rep.eq("r11.analysis.t.df", int(m.group(2)), n_d - 1)
        rep.eq("r11.analysis.t.p", round(_num(m.group(3)), 4), round(p_val, 4))
    m = _grab(rep, "ci", md_text)
    if m:
        rep.eq("r11.analysis.ci.lo", round(_num(m.group(1)), 3), round(lo, 3))
        rep.eq("r11.analysis.ci.hi", round(_num(m.group(2)), 3), round(hi, 3))

    # ---- sign test on the per-pid diffs ----
    wins = sum(1 for d in diffs if d > 0)
    losses = sum(1 for d in diffs if d < 0)
    ties = sum(1 for d in diffs if d == 0)
    p_sign = exact_sign_p(wins, losses)
    m = _grab(rep, "sign", md_text)
    if m:
        rep.eq("r11.analysis.sign.wins", int(m.group(1)), wins)
        rep.eq("r11.analysis.sign.losses", int(m.group(2)), losses)
        rep.eq("r11.analysis.sign.ties", int(m.group(3)), ties)
        rep.eq("r11.analysis.sign.p", round(_num(m.group(4)), 4), round(p_sign, 4))

    # ---- McNemar on final passes ----
    fin_ok = {}
    for cell in (CKPT4710, CKPT710):
        fin_ok[cell] = {r["pid"]: recompute_final_ok(r) for r in _turn10_recs(cells, cell)}
    b = sum(1 for pid in fin_ok[CKPT4710] if fin_ok[CKPT4710].get(pid)
            and pid in fin_ok[CKPT710] and not fin_ok[CKPT710][pid])
    c = sum(1 for pid in fin_ok[CKPT710] if fin_ok[CKPT710].get(pid)
            and pid in fin_ok[CKPT4710] and not fin_ok[CKPT4710][pid])
    p_mc = exact_mcnemar_p(b, c)
    m = _grab(rep, "mcnemar", md_text)
    if m:
        rep.eq("r11.analysis.mcnemar.b", int(m.group(1)), b)
        rep.eq("r11.analysis.mcnemar.c", int(m.group(2)), c)
        rep.eq("r11.analysis.mcnemar.p", round(_num(m.group(3)), 4), round(p_mc, 4))

    # ---- finish audit over all graded turns ----
    graded = [r for r in recs if r.get("cell") in (CKPT4710, CKPT710) and "ok" in r]
    n_len = sum(1 for r in graded if r.get("finish") == "length")
    n_parse = sum(1 for r in graded if extract_json_block(r.get("raw", "")) is None)
    m = _grab(rep, "finish", md_text)
    if m:
        rep.eq("r11.analysis.finish.length", (int(m.group(1)), int(m.group(2))),
               (n_len, len(graded)))
        rep.eq("r11.analysis.finish.parse_fail", (int(m.group(3)), int(m.group(4))),
               (n_parse, len(graded)))

    # ---- ack compliance ----
    m = _grab(rep, "ack", md_text)
    if m:
        idx = 1
        for cell in (CKPT4710, CKPT710):
            rows = [r for r in recs if r.get("cell") == cell + "-ack"]
            okc = sum(1 for r in rows if r.get("raw", "").strip().lower().startswith("ok"))
            rep.eq(f"r11.analysis.ack.{cell}.count", (int(m.group(idx)), int(m.group(idx + 1))),
                   (okc, len(rows)))
            rep.eq(f"r11.analysis.ack.{cell}.pct", round(_num(m.group(idx + 2)), 1),
                   round(100.0 * okc / len(rows), 1) if rows else 0.0)
            idx += 3

    # ---- verdict (mechanical rule + sign-agreement downgrade) ----
    verdict = r11_verdict(mean_d, p_val, wins, losses)
    m = _grab(rep, "verdict", md_text)
    if m:
        rep.eq("r11.analysis.verdict", m.group(1), verdict)

    # ---- Brier over the three probabilistic predictions ----
    if all(k in preg for k in ("P1", "P2", "P3")):
        o1 = 1.0 if mean_d > 0 else 0.0
        o2 = 1.0 if (p_val < 0.05 and mean_d > 0) else 0.0
        p4710 = cells_stats.get(CKPT4710, (0,))[0]
        p710 = cells_stats.get(CKPT710, (0,))[0]
        o3 = 1.0 if abs(p4710 - p710) <= 8 else 0.0
        brier = ((preg["P1"] - o1) ** 2 + (preg["P2"] - o2) ** 2 + (preg["P3"] - o3) ** 2) / 3.0
        m = _grab(rep, "brier", md_text)
        if m:
            rep.eq("r11.analysis.brier", round(_num(m.group(1)), 3), round(brier, 3))

    # ---- severity-diff prediction line ----
    m = _grab(rep, "sev", md_text)
    if m and "pdiff" in preg:
        rep.eq("r11.analysis.sev.predicted", round(_num(m.group(1)), 3), round(preg["pdiff"], 3))
        rep.eq("r11.analysis.sev.observed", round(_num(m.group(2)), 3), round(mean_d, 3))
        rep.eq("r11.analysis.sev.abs_error", round(_num(m.group(3)), 3),
               round(abs(preg["pdiff"] - mean_d), 3))

    # ---- point-prediction scoring table (positional: 4710, 710, diff) ----
    _check_score_table(md_text, rep, n, preg, cells_stats, mean_d)


def r11_verdict(mean_d, p_val, wins, losses):
    """predictions-r11.md §Preregistered verdict rule (exclusive, mechanical)."""
    if mean_d <= 0:
        return "FALSIFIED"
    base = "ESTABLISHED" if p_val < 0.05 else "DIRECTIONAL"
    if base == "ESTABLISHED" and wins <= losses:
        return "DIRECTIONAL"  # sign-agreement downgrade clause
    return base


def _check_score_table(md_text, rep, n, preg, cells_stats, mean_d):
    mh = _grab(rep, "score_header", md_text)
    if mh:
        rep.eq("r11.analysis.score.denominator", int(mh.group(1)), n)
    if not mh:
        return
    rows = []
    for line in md_text[mh.end():].splitlines():
        line = line.strip()
        if not line or re.fullmatch(r"\|[-:| ]+\|", line):
            continue
        m = re.match(_STORED["score_row"], line)
        if not m:
            break
        rows.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()))
        if len(rows) == 3:
            break
    rep.eq("r11.analysis.score.row_count", len(rows), 3)
    if len(rows) != 3:
        return
    p4710 = cells_stats.get(CKPT4710, (0, 0.0, 0.0))[0]
    p710 = cells_stats.get(CKPT710, (0, 0.0, 0.0))[0]
    expect = []
    if "p4710" in preg:
        expect.append((f"{preg['p4710']}/{n}", f"{p4710}/{n}", f"{abs(preg['p4710'] - p4710) / n:.3f}"))
    if "p710" in preg:
        expect.append((f"{preg['p710']}/{n}", f"{p710}/{n}", f"{abs(preg['p710'] - p710) / n:.3f}"))
    if "pdiff" in preg:
        expect.append((f"{preg['pdiff']:+.3f}", f"{mean_d:+.3f}", f"{abs(preg['pdiff'] - mean_d):.3f}"))
    rep.eq("r11.analysis.score.expect_rows", len(expect), 3)
    for i, (label, pred_s, obs_s, err_s) in enumerate(rows):
        if i >= len(expect):
            break
        pred_exp, obs_exp, err_exp = expect[i]
        rep.ok(f"r11.analysis.score.row{i}.predicted_matches_prereg",
               abs(_num(pred_s.replace("/" + str(n), "")) - _num(pred_exp.replace("/" + str(n), ""))) < 1e-9
               if i < 2 else round(_num(pred_s), 3) == round(_num(pred_exp), 3),
               f"row {i} predicted {pred_s!r} != prereg {pred_exp!r}")
        rep.ok(f"r11.analysis.score.row{i}.observed",
               (obs_s == obs_exp) if i < 2 else round(_num(obs_s), 3) == round(_num(obs_exp), 3),
               f"row {i} observed {obs_s!r} != recomputed {obs_exp!r}")
        rep.ok(f"r11.analysis.score.row{i}.abs_error",
               round(_num(err_s), 3) == round(_num(err_exp), 3),
               f"row {i} abs error {err_s!r} != recomputed {err_exp!r}")


# ---------- entry points ----------
def grade_r11(recs, md_text, runlog_text, rep, pids=None, seed_fn=None):
    """Re-derive every stored round-11 number from committed bytes.

    `pids`/`seed_fn` default to the preregistered n=64 (pids 201-264,
    seed 3000+pid*41); the fixture selftest passes a smaller pair set.
    """
    pids = list(R11_PIDS if pids is None else pids)
    seed_fn = r11_seed if seed_fn is None else seed_fn
    n = len(pids)

    truth_by_pid = _build_meta(recs, rep, pids, seed_fn)
    cells = _replay_graded(recs, rep, truth_by_pid)
    _check_descriptors(recs, rep, n, pids)
    _check_census(recs, rep, n)
    _check_summary(recs, runlog_text, rep, n)
    _check_analysis(recs, cells, truth_by_pid, md_text, rep, n, pids)
    return cells


def check_r11_ordering(rep, jsonl_path=None):
    """Preregistration discipline: bundle hashes + hash-before-first-request.

    Hermetic: relative paths from REPO_ROOT, sha256 recomputed in-process (no
    sha256sum subprocess). The jsonl is read (not passed) because the check's
    only consumer of it is the first-request_ts comparison.
    """
    lines = [l for l in read_text(R11_SHA).splitlines() if l.strip()]
    rep.eq("r11.ordering.sha_line_count", len(lines), len(R11_BUNDLE_FILES))
    seen = {}
    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            rep.ok("r11.ordering.sha_line_parse", False, f"unparseable sha line: {line!r}")
            continue
        digest, rel = parts[0], parts[1]
        base = os.path.basename(rel)
        rep.ok(f"r11.ordering.sha_repo_relative.{base}",
               not os.path.isabs(rel) and rel.startswith("corpus/evidence/round11-power/"),
               f"sha line path {rel!r} is not repo-relative under round11-power/")
        full = os.path.join(REPO_ROOT, rel)
        if not os.path.isfile(full):
            rep.ok(f"r11.ordering.sha_file_present.{base}", False, f"missing bundle file {rel}")
            continue
        rep.eq(f"r11.ordering.sha256.{base}", digest, file_sha256(full))
        seen[base] = True
    rep.eq("r11.ordering.sha_file_set", sorted(seen), sorted(R11_BUNDLE_FILES))

    ord_text = read_text(R11_ORDERING)
    pre = re.search(r"^pre-hash\s+(\S+)\s*$", ord_text, re.M)
    post = re.search(r"^post-hash\s+(\S+)\s*$", ord_text, re.M)
    rep.ok("r11.ordering.pre_hash_present", pre is not None, "ordering.log has no 'pre-hash' line")
    rep.ok("r11.ordering.post_hash_present", post is not None, "ordering.log has no 'post-hash' line")

    path = jsonl_path or R11_JSONL
    recs = load_jsonl(path)
    stamped = [r for r in recs if "request_ts" in r and r.get("request_ts")]
    rep.ok("r11.ordering.requests_present", bool(stamped), "no records carry request_ts")
    if not stamped:
        return
    first_ts = min(r["request_ts"] for r in stamped)
    first_recs = [r for r in stamped if r["request_ts"] == first_ts]
    rep.ok("r11.ordering.first_request_is_descriptors",
           all(r.get("cell") == "descriptors" for r in first_recs),
           f"record(s) at first request_ts {first_ts}: {sorted({r.get('cell') for r in first_recs})}")
    if post:
        rep.ok("r11.ordering.hash_precedes_first_request", post.group(1) <= first_ts,
               f"post-hash {post.group(1)} > first request_ts {first_ts}")
    if pre and post:
        rep.ok("r11.ordering.pre_le_post", pre.group(1) <= post.group(1),
               f"pre-hash {pre.group(1)} > post-hash {post.group(1)}")


def selftest_stats():
    """Re-prove the analytic t-table on known values (embedded assertions)."""
    checks = [
        ("t=2.0 df=63", 2.0, 63, 0.0500, 5e-4),
        ("t=1.999 df=60", 1.999, 60, 0.0502, 5e-4),
        ("t=0 df=63", 0.0, 63, 1.0, 1e-12),
    ]
    bad = []
    for name, t, df, want, tol in checks:
        got = t_two_sided_p(t, df)
        if abs(got - want) > tol:
            bad.append(f"{name}: p={got!r}, want {want} +/- {tol}")
    tc = t_crit(63, 0.05)
    if abs(tc - 1.9983405) > 1e-5:
        bad.append(f"t_crit(63,0.05)={tc!r}, want 1.9983405")
    for name, got, want in (("betai(0.5,0.5,0.5)", betai(0.5, 0.5, 0.5), 0.5),
                            ("betai(1,1,0.25)", betai(1.0, 1.0, 0.25), 0.25)):
        if abs(got - want) > 1e-12:
            bad.append(f"{name}={got!r}, want {want}")
    return bad


# ======================= -- selftest (fixture) =======================
# Synthetic fixture: temp tree, n=2 pids, hand-computable diffs. Runs every
# check id through a fresh Report, asserts 0 mismatches, then 3 mutations each
# assert their EXPECTED mismatch id fires. Not pasted into grader.py.

FIX_PIDS = [201, 202]
# per-pid recomputed nwrong at graded turns (hand-computed):
#   pid 201: 4710 {4,7,10}=(0,0,0)  710 {7,10}=(1,1)  -> diff +1.00
#   pid 202: 4710 {4,7,10}=(?,-,0)  710 {7,10}=(1,0)  -> diff -0.50
#   (pid 202 turn 4 is the parse-fail/length record, excluded from the diff)
FIX_NWRONG = {
    201: {CKPT4710: {4: 0, 7: 0, 10: 0}, CKPT710: {7: 1, 10: 1}},
    202: {CKPT4710: {4: None, 7: 2, 10: 0}, CKPT710: {7: 1, 10: 0}},
}


def _fix_ts(i):
    return f"2026-09-28T23:30:{i:02d}Z"


def _raw_of(got):
    if got is None:
        return "no json here at all"
    return "```json\n" + json.dumps(got, separators=(",", ":"), sort_keys=True) + "\n```"


def _perturb(want, k):
    """A dict differing from `want` in exactly k keys (k = recomputed nwrong)."""
    got = dict(want)
    keys = sorted(want)
    for j in range(k):
        got[keys[j % len(keys)]] = want[keys[j % len(keys)]] + 100 + j
    return got


def _build_fixture_tree(tmp):
    d = os.path.join(tmp, "corpus/evidence/round11-power")
    os.makedirs(d, exist_ok=True)
    for name in R11_BUNDLE_FILES:
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(f"# fixture bundle file {name}\n")
    with open(os.path.join(d, "ordering.log"), "w", encoding="utf-8") as f:
        f.write("pre-hash 2026-09-28T23:20:00Z\n"
                "post-hash 2026-09-28T23:20:01Z\n"
                "bundle sha256 file prereg-bundle.sha256 (v1)\n")

    recs = []
    nrec = 0

    def stamp(rec, explicit=None):
        nonlocal nrec
        rec = dict(rec)
        rec["request_ts"] = explicit or _fix_ts(nrec)
        nrec += 1
        return rec

    recs.append(stamp({"cell": "descriptors", "endpoint": "http://127.0.0.1:34113",
                       "models_json": {"data": [{"id": "fixture"}]}, "server": {"pid": 1},
                       "temp": 0.2, "maxtok": 8192, "system_prompt": "fixture",
                       "seed_scheme": R11_SEED_SCHEME, "pids": FIX_PIDS, "n": len(FIX_PIDS),
                       "counterbalance": "even pid: 4710 first; odd pid: 710 first",
                       "machinery_sha256": "0" * 64, "probe_lineage": "fixture"},
                      explicit=_fix_ts(0)))
    nrec = 1

    truth_by_pid = {}
    for pid in FIX_PIDS:
        init, ops, _ = gen_problem(r11_seed(pid))
        truth = states_along(init, [tuple(o) for o in ops])
        truth_by_pid[pid] = truth
        recs.append({"cell": "meta", "pid": pid, "init": init, "ops": ops, "truth": truth,
                     "tail_touched": sorted(tail_touched([tuple(o) for o in ops]))})

    ack_seen = {CKPT4710: 0, CKPT710: 0}
    for pid in FIX_PIDS:
        truth = truth_by_pid[pid]
        order = [CKPT4710, CKPT710] if pid % 2 == 0 else [CKPT710, CKPT4710]
        for cell in order:
            recs.append(stamp({"cell": "filler", "finish": "stop",
                               "usage": {"total_tokens": 3}, "wall_s": 0.01, "raw": "ready"}))
            ck = set(CELL_CHECKPOINTS[cell])
            for turn in range(1, 11):
                want = truth[turn - 1]
                if turn in ck:
                    nw = FIX_NWRONG[pid][cell][turn]
                    if nw is None:
                        got, raw, finish = None, "no json here at all", "length"
                        nwrong_re = len(want)
                        ok = False
                    else:
                        got = want if nw == 0 else _perturb(want, nw)
                        raw, finish = _raw_of(got), "stop"
                        ok, nwrong_re = grade_state(got, want)
                    recs.append(stamp({"cell": cell, "pid": pid, "turn": turn, "ok": ok,
                                       "nwrong": nwrong_re, "got": got, "want": want,
                                       "finish": finish, "usage": {"total_tokens": 5},
                                       "wall_s": 0.02, "raw": raw}))
                else:
                    ack_seen[cell] += 1
                    raw = "ok" if ack_seen[cell] <= (12 if cell == CKPT4710 else 10) else "sure"
                    recs.append(stamp({"cell": cell + "-ack", "pid": pid, "turn": turn,
                                       "raw": raw[:80], "finish": "stop",
                                       "usage": {"total_tokens": 2}, "wall_s": 0.01}))

    with open(os.path.join(d, "results-r11.jsonl"), "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")

    jobs = []
    for pid in FIX_PIDS:
        order = [CKPT4710, CKPT710] if pid % 2 == 0 else [CKPT710, CKPT4710]
        jobs += [(c, pid) for c in order]
    log = []
    for i, (cell, pid) in enumerate(jobs, 1):
        log.append(f"[{i}/{len(jobs)}] ({cell!r}, {pid})")
    passes = {c: sum(1 for r in recs if r.get("cell") == c and r.get("turn") == 10
                     and recompute_final_ok(r)) for c in (CKPT4710, CKPT710)}
    den = {c: sum(1 for r in recs if r.get("cell") == c and r.get("turn") == 10)
           for c in (CKPT4710, CKPT710)}
    log += ["", "=== SUMMARY ===",
            f"{CKPT4710}: {passes[CKPT4710]}/{den[CKPT4710]}",
            f"{CKPT710}: {passes[CKPT710]}/{den[CKPT710]}",
            "wall_total_s: 1.0", ""]
    with open(os.path.join(d, "run.log"), "w", encoding="utf-8") as f:
        f.write("\n".join(log))

    # ---- predictions fixture ----
    ptxt = f"""# fixture predictions
| Quantity | Predicted | Basis | Falsifier |
|---|---:|---|---|
| A-CKPT4710 final (turn-10) passes | 1/{len(FIX_PIDS)} | fixture | — |
| A-CKPT710 final (turn-10) passes | 1/{len(FIX_PIDS)} | fixture | — |
| Paired severity diff (710 {MINUS} 4710, mean nwrong at shared {{7,10}}) | **+0.350** | fixture | — |

| # | Event | P |
|---|---|---:|
| 1 | mean paired diff > 0 | 0.50 |
| 2 | two-sided paired t-test p < 0.05 AND diff > 0 | 0.50 |
| 3 | \\|passes(4710) {MINUS} passes(710)\\| ≤ 8 | 0.50 |
"""
    with open(os.path.join(d, "predictions-r11.md"), "w", encoding="utf-8") as f:
        f.write(ptxt)

    # ---- analysis md fixture (values computed with the module's own stats) ----
    cells = {c: [r for r in recs if r.get("cell") == c and "ok" in r] for c in (CKPT4710, CKPT710)}
    n = len(FIX_PIDS)
    stats = {c: _cell_stats(cells[c], truth_by_pid) for c in (CKPT4710, CKPT710)}
    diffs = []
    for pid in FIX_PIDS:
        d710 = _mean([FIX_NWRONG[pid][CKPT710][t] for t in SHARED_CHECKPOINTS])
        d4710 = _mean([FIX_NWRONG[pid][CKPT4710][t] for t in SHARED_CHECKPOINTS])
        diffs.append(d710 - d4710)
    mean_d, sd_d = _mean(diffs), _sd_sample(diffs)
    sem = sd_d / math.sqrt(len(diffs))
    t_stat = mean_d / sem
    p_val = t_two_sided_p(t_stat, len(diffs) - 1)
    tc = t_crit(len(diffs) - 1, 0.05)
    lo, hi = mean_d - tc * sem, mean_d + tc * sem
    wins = sum(1 for d in diffs if d > 0)
    losses = sum(1 for d in diffs if d < 0)
    ties = sum(1 for d in diffs if d == 0)
    p_sign = exact_sign_p(wins, losses)
    fin = {c: {r["pid"]: recompute_final_ok(r) for r in cells[c] if r["turn"] == 10}
           for c in (CKPT4710, CKPT710)}
    b = sum(1 for pid in fin[CKPT4710] if fin[CKPT4710][pid] and not fin[CKPT710].get(pid, True))
    cc = sum(1 for pid in fin[CKPT710] if fin[CKPT710][pid] and not fin[CKPT4710].get(pid, True))
    p_mc = exact_mcnemar_p(b, cc)
    graded = [r for r in recs if r.get("cell") in (CKPT4710, CKPT710) and "ok" in r]
    n_len = sum(1 for r in graded if r.get("finish") == "length")
    n_parse = sum(1 for r in graded if extract_json_block(r.get("raw", "")) is None)
    ack_rows = {c: [r for r in recs if r.get("cell") == c + "-ack"] for c in (CKPT4710, CKPT710)}
    okc = {c: sum(1 for r in ack_rows[c] if r["raw"].strip().lower().startswith("ok"))
           for c in (CKPT4710, CKPT710)}
    p4710, p710 = stats[CKPT4710][0], stats[CKPT710][0]
    o1 = 1.0 if mean_d > 0 else 0.0
    o2 = 1.0 if (p_val < 0.05 and mean_d > 0) else 0.0
    o3 = 1.0 if abs(p4710 - p710) <= 8 else 0.0
    brier = ((0.5 - o1) ** 2 + (0.5 - o2) ** 2 + (0.5 - o3) ** 2) / 3.0
    verdict = r11_verdict(mean_d, p_val, wins, losses)
    md = f"""# fixture analysis_r11.md
| Cell | Final passes / {n} | Mean final nwrong | Mean nwrong (all graded) |
|---|---:|---:|---:|
| A-CKPT4710 | {p4710}/{n} | {stats[CKPT4710][1]:.3f} | {stats[CKPT4710][2]:.3f} |
| A-CKPT710 | {p710}/{n} | {stats[CKPT710][1]:.3f} | {stats[CKPT710][2]:.3f} |

results-r11.jsonl contains 1 descriptors, {n} meta, {len(graded)} graded, {sum(len(v) for v in ack_rows.values())} ack, 4 fillers, 0 error records
Paired mean difference (710 {MINUS} 4710, shared checkpoints {{7,10}}): {mean_d:+.3f} sd {sd_d:.3f} n={len(diffs)}
Paired t-test: t={t_stat:.3f}, df={len(diffs) - 1}, two-sided p={p_val:.4f}
95% CI of mean difference: [{lo:.3f}, {hi:.3f}]
Exact sign test: wins={wins} losses={losses} ties={ties} two-sided p={p_sign:.4f}
McNemar exact test on final passes: b={b} c={cc} two-sided p={p_mc:.4f}
Finish audit at graded turns: finish=length {n_len}/{len(graded)}, parse fail {n_parse}/{len(graded)}
Ack compliance (raw lowercased startswith ok): A-CKPT4710 {okc[CKPT4710]}/{len(ack_rows[CKPT4710])} = {100.0 * okc[CKPT4710] / len(ack_rows[CKPT4710]):.1f}%; A-CKPT710 {okc[CKPT710]}/{len(ack_rows[CKPT710])} = {100.0 * okc[CKPT710] / len(ack_rows[CKPT710]):.1f}%
PREREGISTERED VERDICT: {verdict}
Brier score (3 probabilistic predictions): {brier:.3f}
Paired severity diff prediction: +0.350 predicted, {mean_d:+.3f} observed, abs error {abs(0.350 - mean_d):.3f}

| Quantity | Predicted | Observed | Abs error /{n} |
|---|---:|---:|---:|
| A-CKPT4710 final passes | 1/{n} | {p4710}/{n} | {abs(1 - p4710) / n:.3f} |
| A-CKPT710 final passes | 1/{n} | {p710}/{n} | {abs(1 - p710) / n:.3f} |
| Paired severity diff | +0.350 | {mean_d:+.3f} | {abs(0.350 - mean_d):.3f} |
"""
    with open(os.path.join(d, "analysis_r11.md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(d, "prereg-bundle.sha256"), "w", encoding="utf-8") as f:
        for name in R11_BUNDLE_FILES:
            f.write(f"{file_sha256(os.path.join(d, name))}  corpus/evidence/round11-power/{name}\n")
    return recs


def _run_fixture():
    global REPO_ROOT, R11_DIR, R11_JSONL, R11_ORDERING, R11_SHA, R11_PRED
    tmp = tempfile.mkdtemp(prefix="kengaku-r11-fixture-")
    saved = (REPO_ROOT, R11_DIR, R11_JSONL, R11_ORDERING, R11_SHA, R11_PRED)
    results = []
    try:
        _build_fixture_tree(tmp)
        REPO_ROOT = tmp
        R11_DIR = os.path.join(tmp, "corpus/evidence/round11-power")
        R11_JSONL = os.path.join(R11_DIR, "results-r11.jsonl")
        R11_ORDERING = os.path.join(R11_DIR, "ordering.log")
        R11_SHA = os.path.join(R11_DIR, "prereg-bundle.sha256")
        R11_PRED = os.path.join(R11_DIR, "predictions-r11.md")

        def run_all(recs=None, runlog_path=None, order_path=None):
            r = Report()
            rs = load_jsonl(R11_JSONL) if recs is None else recs
            grade_r11(rs, read_text(os.path.join(R11_DIR, "analysis_r11.md")),
                      read_text(runlog_path or os.path.join(R11_DIR, "run.log")),
                      r, pids=FIX_PIDS, seed_fn=r11_seed)
            old_ord = R11_ORDERING
            if order_path:
                globals()["R11_ORDERING"] = order_path
            try:
                check_r11_ordering(r, jsonl_path=R11_JSONL)
            finally:
                globals()["R11_ORDERING"] = old_ord
            return r

        rep = run_all()
        results.append(("S0 control (clean fixture)", not rep.mismatches,
                        f"checks={rep.checks} mismatches={len(rep.mismatches)}"
                        + ("" if not rep.mismatches else f" :: {rep.mismatches[:4]}")))

        # M1: flip one stored ok in the first A-CKPT4710 graded record.
        recs1 = json.loads(json.dumps(load_jsonl(R11_JSONL)))
        flipped = False
        for r in recs1:
            if r.get("cell") == CKPT4710 and "ok" in r:
                r["ok"] = not r["ok"]
                flipped = True
                break
        rep1 = run_all(recs=recs1)
        results.append(("M1 stored-ok flip -> r11.replay.A-CKPT4710.ok",
                        flipped and "r11.replay.A-CKPT4710.ok"
                        in "\n".join(rep1.mismatches),
                        f"flip={flipped} mismatches={rep1.mismatches[:3]}"))

        # M2: edit the first SUMMARY cell line.
        log2 = os.path.join(tmp, "run_m2.log")
        txt = read_text(os.path.join(R11_DIR, "run.log"))
        assert f"{CKPT4710}: 2/2" in txt, "fixture SUMMARY control assumption failed"
        with open(log2, "w", encoding="utf-8") as f:
            f.write(txt.replace(f"{CKPT4710}: 2/2", f"{CKPT4710}: 1/2", 1))
        rep2 = run_all(runlog_path=log2)
        results.append(("M2 SUMMARY edit -> r11.summary.A-CKPT4710",
                        "r11.summary.A-CKPT4710" in "\n".join(rep2.mismatches),
                        f"mismatches={rep2.mismatches[:3]}"))

        # M3: push ordering.log post-hash past the first request_ts.
        log3 = os.path.join(tmp, "ordering_m3.log")
        otxt = read_text(os.path.join(R11_DIR, "ordering.log"))
        with open(log3, "w", encoding="utf-8") as f:
            f.write(otxt.replace("post-hash 2026-09-28T23:20:01Z",
                                 "post-hash 2026-09-28T23:59:59Z", 1))
        rep3 = run_all(order_path=log3)
        results.append(("M3 broken ordering timestamp -> r11.ordering.hash_precedes_first_request",
                        "r11.ordering.hash_precedes_first_request" in "\n".join(rep3.mismatches),
                        f"mismatches={rep3.mismatches[:3]}"))
    finally:
        REPO_ROOT, R11_DIR, R11_JSONL, R11_ORDERING, R11_SHA, R11_PRED = saved
        shutil.rmtree(tmp, ignore_errors=True)

    all_ok = True
    for name, passed, detail in results:
        print(f"[fixture] {'PASS' if passed else 'FAIL'} {name}: {detail}")
        all_ok = all_ok and passed
    print(f"[fixture] {'ALL PASS' if all_ok else 'FAILURES PRESENT'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    stat_bad = selftest_stats()
    if stat_bad:
        for b in stat_bad:
            print(f"[fixture] FAIL stats: {b}")
        print("[fixture] FAILURES PRESENT")
        sys.exit(1)
    print("[fixture] PASS stats: betai/betai known values + t_crit(63)=1.9983405")
    sys.exit(_run_fixture())
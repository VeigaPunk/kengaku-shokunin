#!/usr/bin/env python3
"""kengaku hermetic evidence-replay grader — the operability gate (round 10).

Replays the committed probe evidence OFFLINE (no endpoint, no network) and
exits with a verdict a stranger can run:

    python3 grader.py            # grade the committed evidence
    python3 grader.py --selftest # corrupt temp copies; all must be caught

Exit codes (kagi drift-pins convention):
    0  every recomputed value matches the stored one
    1  at least one mismatch; each printed as `MISMATCH <check-id>: ...`
    2  missing/unreadable input, or unparseable evidence

What it verifies, layer by layer:
  PIN     evidence bytes == the hashes recorded when they landed (pins are
          checked only when the DEFAULT in-repo paths are graded; overridden
          paths are by definition mutated copies).
  META    every meta record regenerates exactly from its seed through the
          ported gen_problem (r8: 700+pid*13, pids 1-10; r9: 2000+pid*29,
          pids 101-108), and stored truth/tail_touched re-derive from
          init+ops through sim_apply.
  REPLAY  every graded record's stored got/want/ok/nwrong equals a fresh
          re-parse of its stored `raw` (extract_json_block ported verbatim
          from horizon.py) re-graded against the meta-derived truth;
          B-records also re-derive corrupt_from/outcome/healed; C-records
          re-run grade_c / valid_latin.
  SUMMARY every stored aggregate re-derives from the replayed records:
          r8 run.log `=== SUMMARY ===` (11 cells) + job/record counts;
          r9 replication.md observed table (passes + mean final nwrong),
          record counts, sign tests, onset ladder, failure classes, ack
          compliance, finish-reason claim, cross-round table, prediction
          scoring table vs predictions-r9.md, prediction-hash chain and
          the ordering proof (hash time <= first request_ts).
  ERRATA  adjudicated corrections are pinned in ERRATA below: a check whose
          stored value was ruled defective in a later round passes iff the
          recomputation equals the ADJUDICATED value and the stored text
          still shows the original (the erratum chain stays visible).

Lineage: promotes corpus/evidence/round9-fleet/analyze.py (exact
gen_problem regeneration) and the graders of corpus/evidence/round8-horizon/
horizon.py (extract_json_block / sim_apply / grade_state / grade_c) into a
committed gate. Stdlib only. Deterministic: never orders results by set
iteration (PYTHONHASHSEED-independent).
"""
import argparse
import hashlib
import itertools
import json
import math
import os
import random
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = {
    "r8_jsonl": os.path.join(HERE, "corpus/evidence/round8-horizon/results.jsonl"),
    "r8_runlog": os.path.join(HERE, "corpus/evidence/round8-horizon/run.log"),
    "r9_jsonl": os.path.join(HERE, "corpus/evidence/round9-replication/results-r9.jsonl"),
    "r9_md": os.path.join(HERE, "corpus/evidence/round9-replication/replication.md"),
}
R9_PRED = os.path.join(HERE, "corpus/evidence/round9-replication/predictions-r9.md")
R9_PRED_SHA = os.path.join(HERE, "corpus/evidence/round9-replication/predictions-r9.sha256.repo")
R9_ORDERING = os.path.join(HERE, "corpus/evidence/round9-replication/ordering.log")

# Hashes recorded when the artifacts landed (LOG.md round-8/round-9 entries;
# r9 files pinned as of round 10 from HEAD 1bd17ec bytes — no earlier record).
# r9_md re-pinned in round 10: pre-errata md5 a70980a5f465da1bedd0ffa474a0c032
# → post-errata d9235e41f3ebfdcabd368c71cde878a1 (the only change is the
# appended "## Errata (round 10)" section; recorded in LOG.md round-10 entry).
PINS = {
    "r8_jsonl": ("md5", "df154cb524bf210782fb0f4a46fd1bdc"),
    "r8_runlog": ("md5", "fc3b232ffc532717e50c1d06e0549acc"),
    "r9_jsonl": ("md5", "f3c58218da27cc6b05dca5a4e10d7f52"),
    "r9_md": ("md5", "d9235e41f3ebfdcabd368c71cde878a1"),
}

# Adjudicated errata: check-id -> (stored_defective_value, corrected_value, ruling)
# The check passes iff stored text still shows the defective value AND the
# recomputation equals the corrected value. Ruling text must cite LOG.md.
ERRATA = {
    "r9.failure_classes.state_error": (
        "12/32", "24/32",
        "round-10 grader recomputation from committed results-r9.jsonl: final "
        "graded-turn passes are INC 4/8 + CKPT4710 2/8 + CKPT710 2/8 + MONO "
        "0/8 = 8/32, parse failures 0/32, so state errors = 24/32; the stored "
        "12/32 equals the two checkpoint cells' final failures (6+6) over the "
        "all-cells denominator (that provenance is conjectural; the corrected "
        "value is arithmetic on committed bytes). See LOG.md round-10 entry "
        "and replication.md §Errata."),
}

KEYS = ["nails", "bolts", "screws", "washers", "hinges"]
CONFLICT_ROWS = [["A", "B", "C", "D"], ["B", "C", "D", "A"], ["A", "B", "D", "C"]]
BENIGN_ROWS = [["A", "B", "C", "D"], ["B", "A", "D", "C"], ["C", "D", "A", "B"]]


# ---------- ports from horizon.py (byte-faithful semantics) ----------
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


def col_conflict_free(rows):
    return all(len(set(r[c] for r in rows)) == len(rows) for c in range(4))


def valid_latin(sq):
    if not isinstance(sq, list) or len(sq) != 4:
        return False
    sym = {"A", "B", "C", "D"}
    if not all(isinstance(r, list) and len(r) == 4 and set(r) == sym for r in sq):
        return False
    return all(set(sq[r][c] for r in range(4)) == sym for c in range(4))


def rows_perm_only(sq):
    sym = {"A", "B", "C", "D"}
    return (isinstance(sq, list) and len(sq) == 4
            and all(isinstance(r, list) and set(r) == sym for r in sq))


def grade_c(got, prior_rows, with_rule):
    out = {"ok": False, "viol_ok": False, "square_valid": False,
           "preserved": False, "over_repair": False, "parse": got is not None}
    if not isinstance(got, dict):
        return out
    viol, sq = got.get("violations"), got.get("square")
    if not isinstance(viol, list) or not isinstance(sq, list):
        return out
    out["square_valid"] = valid_latin(sq) if with_rule else rows_perm_only(sq)
    changed = set(viol)
    kept_ok = all(sq[i] == prior_rows[i] for i in range(3) if (i + 1) not in changed)
    out["preserved"] = kept_ok
    remaining = [prior_rows[i] for i in range(3) if (i + 1) not in changed]
    feasible = col_conflict_free(remaining) if with_rule else True
    out["viol_ok"] = feasible and kept_ok
    if with_rule and out["viol_ok"]:
        minimal_sz = next((sz for sz in range(4)
                           if any(col_conflict_free([prior_rows[i] for i in range(3) if i not in c])
                                  for c in itertools.combinations(range(3), sz))), None)
        out["over_repair"] = minimal_sz is not None and len(changed) > minimal_sz
    out["ok"] = out["square_valid"] and out["viol_ok"] and out["preserved"]
    return out


# ---------- check engine ----------
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

    def erratum(self, cid, stored_text_value, recomp_str):
        """Adjudicated-erratum check: stored text must still show the defective
        value (chain visible) and the recomputation must equal the ruling."""
        defective, corrected, ruling = ERRATA[cid]
        self.checks += 1
        if stored_text_value != defective or recomp_str != corrected:
            self.mismatches.append(
                f"MISMATCH {cid}: stored={stored_text_value!r} (expected defective "
                f"{defective!r} to remain visible) recomputed={recomp_str!r} "
                f"(expected adjudicated {corrected!r}) ruling={ruling}")


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


def file_md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- shared replay helpers ----------
def build_meta(recs, rep, tag, pids, seed_fn):
    metas = [r for r in recs if r.get("cell") == "meta"]
    rep.eq(f"{tag}.meta.count", len(metas), len(pids))
    seen = {}
    for m in metas:
        seen.setdefault(m["pid"], []).append(m)
    rep.ok(f"{tag}.meta.unique_pids", all(len(v) == 1 for v in seen.values()),
           f"duplicate meta pids: {[p for p, v in seen.items() if len(v) > 1]}")
    rep.eq(f"{tag}.meta.pid_set", sorted(seen), sorted(pids))
    truth_by_pid = {}
    diffs = {"init": [], "ops": [], "truth": [], "tail": []}
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
        rep.ok(f"{tag}.meta.regenerate.{field}", not diffs[field],
               f"{len(diffs[field])}/{len(pids)} pids differ: {diffs[field][:4]}")
    return truth_by_pid


def replay_a_records(recs, rep, tag, truth_by_pid, mono_cell="A-MONO"):
    """Re-parse raw and re-grade every graded A record; aggregate per cell/field."""
    cells = {}
    for r in recs:
        c = r.get("cell", "")
        if c.startswith("A-") and not c.endswith("-ack") and "ok" in r:
            cells.setdefault(c, []).append(r)
    for cell in sorted(cells):
        rows = cells[cell]
        diffs = {"got": 0, "want": 0, "ok": 0, "nwrong": 0}
        first = None
        for r in rows:
            pid, turn = r["pid"], r["turn"]
            truth = truth_by_pid.get(pid)
            if truth is None:
                diffs["want"] += 1
                first = first or (pid, turn, "no meta")
                continue
            want_re = truth[-1] if cell == mono_cell else truth[turn - 1]
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
            rep.ok(f"{tag}.replay.{cell}.{field}", diffs[field] == 0,
                   f"{diffs[field]}/{len(rows)} records differ (first: {first})")
    return cells


def final_passes(cells, cell, ok_field="ok"):
    """Per-pid ok at max turn -> (passes, n_pids, {pid: record})."""
    rows = cells.get(cell, [])
    by_pid = {}
    for r in rows:
        p = r["pid"]
        if p not in by_pid or r["turn"] > by_pid[p]["turn"]:
            by_pid[p] = r
    return by_pid


# ---------- round 8 ----------
def grade_r8(recs, runlog_text, rep):
    truth_by_pid = build_meta(recs, rep, "r8", range(1, 11), lambda pid: 700 + pid * 13)
    cells = replay_a_records(recs, rep, "r8", truth_by_pid)

    # ---- B records: corrupt-field membership, corrupt_from rule, outcome, healed ----
    b_by_cell = {}
    for r in recs:
        if r.get("cell", "").startswith("B-"):
            b_by_cell.setdefault(r["cell"], []).append(r)
    b_diffs = {"field": 0, "from": 0, "got": 0, "want": 0, "ok": 0, "outcome": 0, "healed": 0}
    b_n = 0
    b_first = None
    for cell in sorted(b_by_cell):
        _, mode, cond = cell.split("-", 2)  # B-{corrupt|clean}-{plain|hint}
        for r in b_by_cell[cell]:
            b_n += 1
            pid = r["pid"]
            truth = truth_by_pid[pid]
            m = recs_meta_lookup(recs, pid)
            ops = [tuple(o) for o in m["ops"]]
            correct7 = states_along(m["init"], ops, 7)
            state_mid = dict(correct7[-1])
            want = truth[-1]
            got_re = extract_json_block(r.get("raw", ""))
            if got_re != r.get("got"):
                b_diffs["got"] += 1
                b_first = b_first or (cell, pid, "got")
            if want != r.get("want"):
                b_diffs["want"] += 1
                b_first = b_first or (cell, pid, "want")
            sim_corrupt = None
            if mode == "corrupt":
                cand = {k for k in tail_touched(ops, 7) if k in state_mid}
                field = r.get("corrupt_field")
                allowed = cand if cand else set(state_mid)
                if field not in allowed:
                    b_diffs["field"] += 1
                    b_first = b_first or (cell, pid, "corrupt_field")
                hv = None
                for j in range(5, -1, -1):
                    v = correct7[j].get(field)
                    if v is not None and v != state_mid.get(field):
                        hv = v
                        break
                expected_from = hv if hv is not None else state_mid.get(field, 0) + 5
                if r.get("corrupt_from") != expected_from:
                    b_diffs["from"] += 1
                    b_first = b_first or (cell, pid, "corrupt_from")
                sm = dict(state_mid)
                sm[field] = r.get("corrupt_from")
                sim_corrupt = states_along(sm, ops[7:])[-1]
            else:
                if r.get("corrupt_field") is not None or r.get("corrupt_from") is not None:
                    b_diffs["field"] += 1
                    b_first = b_first or (cell, pid, "clean-corrupt_field-not-null")
            exact_re = got_re == want
            outcome_re = "corrected" if exact_re else ("propagated" if got_re == sim_corrupt else "other")
            healed_re = mode == "clean" or (isinstance(got_re, dict)
                                            and got_re.get(r.get("corrupt_field")) == want.get(r.get("corrupt_field")))
            for field, recomp, stored in (("ok", exact_re, r.get("ok")),
                                          ("outcome", outcome_re, r.get("outcome")),
                                          ("healed", healed_re, r.get("healed"))):
                if recomp != stored:
                    b_diffs[field] += 1
                    b_first = b_first or (cell, pid, field)
    for field in b_diffs:
        rep.ok(f"r8.replay.B.{field}", b_diffs[field] == 0,
               f"{b_diffs[field]}/{b_n} B records differ (first: {b_first})")

    # ---- C records: full grade_c replay ----
    c_specs = {"C-conflict": (CONFLICT_ROWS, True), "C-benign": (BENIGN_ROWS, True),
               "C-norule": (BENIGN_ROWS, False)}
    c_diffs = {}
    c_n = 0
    for r in recs:
        cell = r.get("cell", "")
        if cell in c_specs:
            c_n += 1
            rows, with_rule = c_specs[cell]
            g = grade_c(extract_json_block(r.get("raw", "")), rows, with_rule)
            for field, recomp in g.items():
                if recomp != r.get(field):
                    c_diffs.setdefault(field, []).append((cell, r.get("rep")))
            if extract_json_block(r.get("raw", "")) != r.get("got"):
                c_diffs.setdefault("got", []).append((cell, r.get("rep")))
        elif cell == "C-MONO":
            c_n += 1
            got_re = extract_json_block(r.get("raw", ""))
            ok_re = valid_latin(got_re)
            for field, recomp in (("ok", ok_re), ("square_valid", ok_re), ("got", got_re)):
                if recomp != r.get(field):
                    c_diffs.setdefault(field, []).append((cell, r.get("rep")))
    rep.eq("r8.replay.C.count", c_n, 16)
    rep.ok("r8.replay.C.fields", not c_diffs,
           f"{sum(len(v) for v in c_diffs.values())} field diffs: "
           f"{ {k: v[:2] for k, v in c_diffs.items()} }")

    # ---- recompute SUMMARY (from recomputed oks, not stored) ----
    summ = {}
    for cell in ("A-INC", "A-CKPT"):
        fp = final_passes(cells, cell)
        got_re_final = [recompute_final_ok(r) for r in fp.values()]
        summ[cell] = (sum(1 for x in got_re_final if x), len(fp))
    fp = final_passes(cells, "A-MONO")
    mono_oks = [grade_state(extract_json_block(r.get("raw", "")), truth_by_pid[r["pid"]][-1])[0]
                for r in fp.values()]
    summ["A-MONO"] = (sum(1 for x in mono_oks if x), len(fp))
    for cell in sorted(b_by_cell):
        oks = []
        for r in b_by_cell[cell]:
            m = recs_meta_lookup(recs, r["pid"])
            ops = [tuple(o) for o in m["ops"]]
            want = states_along(m["init"], ops)[-1]
            oks.append(extract_json_block(r.get("raw", "")) == want)
        summ[cell] = (sum(1 for x in oks if x), len(oks))
    for cell in ("C-conflict", "C-benign", "C-norule"):
        rows, with_rule = c_specs[cell]
        rs = [r for r in recs if r.get("cell") == cell]
        oks = [grade_c(extract_json_block(r.get("raw", "")), rows, with_rule)["ok"] for r in rs]
        summ[cell] = (sum(1 for x in oks if x), len(oks))
    rs = [r for r in recs if r.get("cell") == "C-MONO"]
    oks = [valid_latin(extract_json_block(r.get("raw", ""))) for r in rs]
    summ["C-MONO"] = (sum(1 for x in oks if x), len(oks))

    stored_summ = parse_runlog_summary(runlog_text)
    rep.eq("r8.summary.cell_set", sorted(stored_summ), sorted(summ))
    for cell in sorted(set(stored_summ) | set(summ)):
        s = stored_summ.get(cell)
        r_ = summ.get(cell)
        rep.eq(f"r8.summary.{cell}", s, r_)

    # ---- counts ----
    jobs = len(re.findall(r"^\[\d+/78\]", runlog_text, re.M))
    rep.eq("r8.counts.jobs_logged", jobs, 78)
    rep.eq("r8.counts.records", len(recs), 268)
    rep.eq("r8.counts.non_meta", sum(1 for r in recs if r.get("cell") != "meta"), 258)
    return summ, stored_summ


_META_INDEX = {}


def recs_meta_lookup(recs, pid):
    key = id(recs)
    idx = _META_INDEX.get(key)
    if idx is None:
        idx = {r["pid"]: r for r in recs if r.get("cell") == "meta"}
        _META_INDEX[key] = idx
    return idx[pid]


def recompute_final_ok(r):
    return grade_state(extract_json_block(r.get("raw", "")), r.get("want"))[0] \
        if r.get("want") is not None else False


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


# ---------- round 9 ----------
def grade_r9(recs, md_text, rep, r8_summ_recomp, r8_summ_stored):
    truth_by_pid = build_meta(recs, rep, "r9", range(101, 109), lambda pid: 2000 + pid * 29)
    cells = replay_a_records(recs, rep, "r9", truth_by_pid)

    graded = [r for r in recs if r.get("cell", "").startswith("A-")
              and not r.get("cell", "").endswith("-ack") and "ok" in r]
    acks = [r for r in recs if r.get("cell", "").endswith("-ack")]
    fillers = [r for r in recs if r.get("cell") == "filler"]

    # recomputed final-pass table
    recomp_table = {}
    for cell in ("A-INC", "A-CKPT4710", "A-CKPT710", "A-MONO"):
        fp = final_passes(cells, cell)
        oks, nws = [], []
        for pid in sorted(fp):
            r = fp[pid]
            ok_re, nw_re = grade_state(extract_json_block(r.get("raw", "")),
                                       truth_by_pid[pid][-1] if cell == "A-MONO"
                                       else truth_by_pid[pid][r["turn"] - 1])
            oks.append(ok_re)
            nws.append(nw_re)
        recomp_table[cell] = (sum(1 for x in oks if x), len(oks), sum(nws) / len(nws))

    # ---- observed-results table in replication.md ----
    obs = {}
    for m in re.finditer(r"^\| (A-(?:INC|CKPT4710|CKPT710|MONO)) \| (\d+)/8 \| (\d+\.\d{3}) \|$",
                         md_text, re.M):
        obs[m.group(1)] = (int(m.group(2)), float(m.group(3)))
    rep.eq("r9.observed.cell_set", sorted(obs), sorted(recomp_table))
    for cell in sorted(recomp_table):
        passes, n, mean_nw = recomp_table[cell]
        if cell in obs:
            rep.eq(f"r9.observed.{cell}.passes", obs[cell][0], passes)
            rep.eq(f"r9.observed.{cell}.mean_nwrong", f"{obs[cell][1]:.3f}", f"{mean_nw:.3f}")
        rep.eq(f"r9.observed.{cell}.denominator", n, 8)

    # ---- record counts sentence ----
    m = re.search(r"contains (\d+) meta, (\d+) scored records, (\d+) fillers, no error records",
                  md_text)
    if not m:
        rep.ok("r9.counts.sentence_present", False, "counts sentence not found in replication.md")
    else:
        rep.eq("r9.counts.meta", int(m.group(1)), sum(1 for r in recs if r.get("cell") == "meta"))
        rep.eq("r9.counts.scored", int(m.group(2)), len(graded) + len(acks))
        rep.eq("r9.counts.fillers", int(m.group(3)), len(fillers))
        rep.eq("r9.counts.errors", 0, sum(1 for r in recs if r.get("cell") == "error"))
    rep.eq("r9.counts.total_records", len(recs), 284)

    # ---- sign tests ----
    fp_ok = {}
    for cell in ("A-INC", "A-CKPT4710", "A-CKPT710", "A-MONO"):
        f = final_passes(cells, cell)
        fp_ok[cell] = {pid: recompute_final_ok(f[pid]) for pid in f}
    pairs = [("INC vs CKPT4710", "A-INC", "A-CKPT4710"),
             ("CKPT4710 vs CKPT710", "A-CKPT4710", "A-CKPT710"),
             ("CKPT710 vs MONO", "A-CKPT710", "A-MONO"),
             ("INC vs MONO", "A-INC", "A-MONO")]
    for label, c1, c2 in pairs:
        wins = losses = ties = 0
        for pid in sorted(fp_ok[c1]):
            a, b = fp_ok[c1][pid], fp_ok[c2][pid]
            if a and not b:
                wins += 1
            elif b and not a:
                losses += 1
            else:
                ties += 1
        n = wins + losses
        if n == 0:
            p_str = "1.000 (undefined direction; all ties)"
        else:
            cdf_le = sum(math.comb(n, k) for k in range(0, wins + 1)) / 2 ** n
            cdf_ge = sum(math.comb(n, k) for k in range(wins, n + 1)) / 2 ** n
            p_str = f"{2 * min(cdf_le, cdf_ge):.3f}"
        row = re.search(r"^\| " + re.escape(label) + r" \| (\d+) \| (\d+) \| (\d+) \| ([^|]+) \|$",
                        md_text, re.M)
        if not row:
            rep.ok(f"r9.signtest.{label}.row_present", False, "row not found in replication.md")
            continue
        rep.eq(f"r9.signtest.{label}.wins", int(row.group(1)), wins)
        rep.eq(f"r9.signtest.{label}.losses", int(row.group(2)), losses)
        rep.eq(f"r9.signtest.{label}.ties", int(row.group(3)), ties)
        rep.eq(f"r9.signtest.{label}.p", row.group(4).strip(), p_str)

    # ---- onset ladder ----
    m = re.search(r"INC first-error turns by pid 101\u2013108: `([^`]+)`; mean among the (\d+) "
                  r"non-perfect trajectories = \*\*([\d.]+)\*\*", md_text)
    if not m:
        rep.ok("r9.onset.line_present", False, "onset line not found in replication.md")
    else:
        onset_re = []
        for pid in range(101, 109):
            rows = sorted([r for r in cells.get("A-INC", []) if r["pid"] == pid],
                          key=lambda r: r["turn"])
            first_err = None
            for r in rows:
                if not recompute_final_ok(r):
                    first_err = r["turn"]
                    break
            onset_re.append(first_err)
        stored_list = [None if x.strip() == "None" else int(x) for x in m.group(1).split(",")]
        rep.eq("r9.onset.per_pid", stored_list, onset_re)
        nonperfect = [x for x in onset_re if x is not None]
        rep.eq("r9.onset.n_nonperfect", int(m.group(2)), len(nonperfect))
        rep.eq("r9.onset.mean", m.group(3), f"{sum(nonperfect) / len(nonperfect):.1f}")
    # predicted onset from predictions-r9.md (preregistration anchor; the
    # observed mean is checked against replication.md above)
    pred_txt = read_text(R9_PRED)
    mp = re.search(r"Predicted INC mean onset turn: ([\d.]+)", pred_txt)
    rep.ok("r9.onset.prediction_preregistered", mp is not None,
           "predictions-r9.md carries no 'Predicted INC mean onset turn' value")

    # ---- failure classes at final graded turn ----
    final_recs = []
    for cell in ("A-INC", "A-CKPT4710", "A-CKPT710", "A-MONO"):
        f = final_passes(cells, cell)
        final_recs += [f[pid] for pid in sorted(f)]
    parse_fail = sum(1 for r in final_recs if extract_json_block(r.get("raw", "")) is None)
    length_fin = sum(1 for r in final_recs if r.get("finish") == "length")
    state_err = sum(1 for r in final_recs
                    if extract_json_block(r.get("raw", "")) is not None and not recompute_final_ok(r))
    mf = re.search(r"parse fail (\d+)/(\d+); finish=length (\d+)/(\d+); state error "
                   r"\(parsed but not exact\) (\d+)/(\d+)", md_text)
    if not mf:
        rep.ok("r9.failure_classes.line_present", False, "failure-class line not found")
    else:
        rep.eq("r9.failure_classes.parse_fail", f"{mf.group(1)}/{mf.group(2)}",
               f"{parse_fail}/{len(final_recs)}")
        rep.eq("r9.failure_classes.finish_length", f"{mf.group(3)}/{mf.group(4)}",
               f"{length_fin}/{len(final_recs)}")
        # stored state-error figure is under an adjudicated erratum (see ERRATA)
        rep.erratum("r9.failure_classes.state_error",
                    f"{mf.group(5)}/{mf.group(6)}", f"{state_err}/{len(final_recs)}")
    mono_final = final_passes(cells, "A-MONO")
    mm = re.search(r"audit on MONO is parse (\d+)/(\d+), finish=length (\d+)/(\d+), state error (\d+)/(\d+)",
                   md_text)
    if not mm:
        rep.ok("r9.failure_classes.mono_line_present", False, "MONO audit line not found")
    else:
        mrecs = [mono_final[p] for p in sorted(mono_final)]
        mpf = sum(1 for r in mrecs if extract_json_block(r.get("raw", "")) is None)
        mlen = sum(1 for r in mrecs if r.get("finish") == "length")
        mse = sum(1 for r in mrecs if extract_json_block(r.get("raw", "")) is not None
                  and not recompute_final_ok(r))
        rep.eq("r9.failure_classes.mono.parse", f"{mm.group(1)}/{mm.group(2)}", f"{mpf}/{len(mrecs)}")
        rep.eq("r9.failure_classes.mono.length", f"{mm.group(3)}/{mm.group(4)}", f"{mlen}/{len(mrecs)}")
        rep.eq("r9.failure_classes.mono.state_error", f"{mm.group(5)}/{mm.group(6)}", f"{mse}/{len(mrecs)}")

    # ---- ack compliance ----
    ma = re.search(r"CKPT4710 (\d+)/(\d+) = ([\d.]+)%; CKPT710 (\d+)/(\d+) = ([\d.]+)%", md_text)
    if not ma:
        rep.ok("r9.ack.line_present", False, "ack-compliance line not found")
    else:
        for cell, num, den, pct in (("A-CKPT4710-ack", ma.group(1), ma.group(2), ma.group(3)),
                                    ("A-CKPT710-ack", ma.group(4), ma.group(5), ma.group(6))):
            rows = [r for r in acks if r.get("cell") == cell]
            okc = sum(1 for r in rows if r.get("raw", "").strip().lower().startswith("ok"))
            rep.eq(f"r9.ack.{cell}.count", f"{num}/{den}", f"{okc}/{len(rows)}")
            rep.eq(f"r9.ack.{cell}.pct", pct, f"{100.0 * okc / len(rows):.1f}" if rows else "n/a")

    # ---- finish-reason claim ----
    stop_finals = sum(1 for r in final_recs if r.get("finish") == "stop")
    rep.ok("r9.finish.all_finals_stop", stop_finals == len(final_recs),
           f"{stop_finals}/{len(final_recs)} final graded records have finish=='stop'")

    # ---- cross-round table (r8 columns must equal the r8 replay) ----
    xmap = [("A-INC", "A-INC"), ("A-CKPT (4,7,10) / CKPT4710", "A-CKPT"), ("A-MONO", "A-MONO")]
    for label, r8cell in xmap:
        row = re.search(r"^\| " + re.escape(label) + r" \| (\d+)/10 \| (\d+)/8 \|$", md_text, re.M)
        if not row:
            rep.ok(f"r9.crossround.{r8cell}.row_present", False, "row not found")
            continue
        s8 = r8_summ_stored.get(r8cell)
        rep.eq(f"r9.crossround.{r8cell}.r8_col", f"{row.group(1)}/10",
               f"{s8[0]}/10" if s8 else "MISSING")
        rep.eq(f"r9.crossround.{r8cell}.r8_col_vs_replay", row.group(1), str(s8[0]) if s8 else "?")
        r9cell = "A-CKPT4710" if r8cell == "A-CKPT" else r8cell
        rep.eq(f"r9.crossround.{r8cell}.r9_col", f"{row.group(2)}/8",
               f"{recomp_table[r9cell][0]}/8")
    row = re.search(r"^\| A-CKPT710 \| not run \| (\d+)/8 \|$", md_text, re.M)
    if not row:
        rep.ok("r9.crossround.A-CKPT710.row_present", False, "row not found")
    else:
        rep.eq("r9.crossround.A-CKPT710.r9_col", f"{row.group(1)}/8",
               f"{recomp_table['A-CKPT710'][0]}/8")

    # ---- prediction scoring table vs predictions-r9.md and replay ----
    pred = {}
    for m2 in re.finditer(r"^\| (A-(?:INC|CKPT4710|CKPT710|MONO)) \| (\d+)/8 \|", pred_txt, re.M):
        pred[m2.group(1)] = int(m2.group(2))
    rep.eq("r9.predictions.preregistered_cells", sorted(pred),
           ["A-CKPT4710", "A-CKPT710", "A-INC", "A-MONO"])
    for m2 in re.finditer(r"^\| (A-(?:INC|CKPT4710|CKPT710|MONO)) \| (\d+)/8 \| (\d+)/8 \| "
                          r"(hit|miss) \| (\d+\.\d{3}) \|$", md_text, re.M):
        cell = m2.group(1)
        obs_passes = recomp_table[cell][0]
        rep.eq(f"r9.predscore.{cell}.predicted_col", int(m2.group(2)), pred.get(cell))
        rep.eq(f"r9.predscore.{cell}.observed_col", int(m2.group(3)), obs_passes)
        rep.eq(f"r9.predscore.{cell}.hit_col", m2.group(4),
               "hit" if pred.get(cell) == obs_passes else "miss")
        rep.eq(f"r9.predscore.{cell}.abs_err_col", m2.group(5),
               f"{abs(pred.get(cell, 0) - obs_passes) / 8:.3f}")

    # ---- prediction hash chain + ordering proof ----
    sha_line = read_text(R9_PRED_SHA).split()
    if len(sha_line) < 1:
        die("predictions-r9.sha256.repo empty")
    actual = hashlib.sha256(read_text(R9_PRED).encode("utf-8")).hexdigest()
    rep.eq("r9.ordering.prediction_sha256", sha_line[0], actual)
    ord_lines = [l.strip() for l in read_text(R9_ORDERING).splitlines() if l.strip()]
    rep.eq("r9.ordering.hash_before_after_equal", len(set(ord_lines)), 1)
    req_ts = [r["request_ts"] for r in recs if "request_ts" in r and r.get("cell") != "meta"]
    rep.ok("r9.ordering.hash_precedes_first_request", bool(req_ts) and ord_lines
           and max(ord_lines) <= min(req_ts),
           f"hash time {max(ord_lines) if ord_lines else '?'} vs first request "
           f"{min(req_ts) if req_ts else '?'}")

    return recomp_table


# ---------- pins ----------
def check_pins(paths, rep):
    for key, (algo, expected) in PINS.items():
        p = paths[key]
        if os.path.abspath(p) != os.path.abspath(DEFAULTS[key]):
            print(f"[pin] {key}: SKIPPED (overridden path, treated as mutated copy)")
            continue
        h = hashlib.new(algo)
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        rep.eq(f"pin.{key}.{algo}", expected, h.hexdigest())


# ---------- selftest ----------
def run_selftest():
    """Corrupt temp copies three ways; the grader must catch all three."""
    results = []
    tmp = tempfile.mkdtemp(prefix="kengaku-grader-selftest-")
    try:
        clean = {}
        for key in DEFAULTS:
            clean[key] = os.path.join(tmp, os.path.basename(DEFAULTS[key]))
            with open(DEFAULTS[key], "rb") as src, open(clean[key], "wb") as dst:
                dst.write(src.read())
        import subprocess

        def run(*argv):
            p = subprocess.run([sys.executable, os.path.abspath(__file__), *argv],
                               capture_output=True, text=True)
            return p.returncode, p.stdout

        rc, out = run("--r8-jsonl", clean["r8_jsonl"], "--r8-runlog", clean["r8_runlog"],
                      "--r9-jsonl", clean["r9_jsonl"], "--r9-md", clean["r9_md"])
        results.append(("S0 control (clean copies)", rc == 0 and "VERDICT: PASS" in out,
                        f"exit {rc}, expected 0"))

        # S1: flip one stored ok in the first r8 A-INC record with ok==true
        p1 = os.path.join(tmp, "m1.jsonl")
        flipped = False
        with open(clean["r8_jsonl"]) as f, open(p1, "w") as out:
            for line in f:
                r = json.loads(line)
                if not flipped and r.get("cell") == "A-INC" and r.get("ok") is True:
                    r["ok"] = False
                    line = json.dumps(r, separators=(",", ":")) + "\n"
                    flipped = True
                out.write(line)
        rc, out = run("--r8-jsonl", p1, "--r8-runlog", clean["r8_runlog"],
                      "--r9-jsonl", clean["r9_jsonl"], "--r9-md", clean["r9_md"])
        results.append(("S1 stored-ok flip (record layer)",
                        rc == 1 and flipped and "MISMATCH r8.replay.A-INC.ok" in out,
                        f"exit {rc}, expected 1 + check-id r8.replay.A-INC.ok "
                        f"(flip applied: {flipped}, id fired: {'r8.replay.A-INC.ok' in out})"))

        # S2: edit one stored SUMMARY number in run.log
        p2 = os.path.join(tmp, "m2.log")
        txt = open(clean["r8_runlog"]).read()
        assert "A-INC: 7/10" in txt
        open(p2, "w").write(txt.replace("A-INC: 7/10", "A-INC: 8/10", 1))
        rc, out = run("--r8-jsonl", clean["r8_jsonl"], "--r8-runlog", p2,
                      "--r9-jsonl", clean["r9_jsonl"], "--r9-md", clean["r9_md"])
        results.append(("S2 run.log SUMMARY edit (summary layer)",
                        rc == 1 and "MISMATCH r8.summary.A-INC" in out,
                        f"exit {rc}, expected 1 + check-id r8.summary.A-INC "
                        f"(id fired: {'r8.summary.A-INC' in out})"))

        # S3: bump the first digit inside the last fenced JSON block of the
        #     first r9 A-MONO record's raw (re-parse layer)
        p3 = os.path.join(tmp, "m3.jsonl")
        done = False
        with open(clean["r9_jsonl"]) as f, open(p3, "w") as out:
            for line in f:
                r = json.loads(line)
                if not done and r.get("cell") == "A-MONO":
                    raw = r["raw"]
                    blocks = list(re.finditer(r"```(?:json)?\s*\n(.*?)```", raw, re.S))
                    if blocks:
                        b = blocks[-1]
                        inner = b.group(1)
                        dm = re.search(r"\d", inner)
                        if dm:
                            newdigit = str((int(dm.group(0)) + 1) % 10)
                            newinner = inner[:dm.start()] + newdigit + inner[dm.end():]
                            raw = raw[:b.start(1)] + newinner + raw[b.end(1):]
                            r["raw"] = raw
                            line = json.dumps(r, separators=(",", ":")) + "\n"
                            done = True
                out.write(line)
        rc, out = run("--r8-jsonl", clean["r8_jsonl"], "--r8-runlog", clean["r8_runlog"],
                      "--r9-jsonl", p3, "--r9-md", clean["r9_md"])
        results.append(("S3 raw-digit bump (re-parse layer)",
                        rc == 1 and done and "MISMATCH r9.replay.A-MONO.got" in out,
                        f"exit {rc}, expected 1 + check-id r9.replay.A-MONO.got "
                        f"(mutation applied: {done}, id fired: {'r9.replay.A-MONO.got' in out})"))
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    all_ok = True
    for name, passed, detail in results:
        print(f"[selftest] {'PASS' if passed else 'FAIL'} {name}: {detail}")
        all_ok = all_ok and passed
    print(f"[selftest] {'ALL PASS' if all_ok else 'FAILURES PRESENT'}")
    return 0 if all_ok else 1


# ---------- main ----------
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true",
                    help="corrupt temp copies; exit 0 only if every corruption is caught")
    ap.add_argument("--r8-jsonl", default=DEFAULTS["r8_jsonl"])
    ap.add_argument("--r8-runlog", default=DEFAULTS["r8_runlog"])
    ap.add_argument("--r9-jsonl", default=DEFAULTS["r9_jsonl"])
    ap.add_argument("--r9-md", default=DEFAULTS["r9_md"])
    args = ap.parse_args(argv)

    if args.selftest:
        sys.exit(run_selftest())

    paths = {"r8_jsonl": args.r8_jsonl, "r8_runlog": args.r8_runlog,
             "r9_jsonl": args.r9_jsonl, "r9_md": args.r9_md}
    for key, p in paths.items():
        if not os.path.isfile(p):
            die(f"{key}: no such file: {p}")
    for p in (R9_PRED, R9_PRED_SHA, R9_ORDERING):
        if not os.path.isfile(p):
            die(f"missing sidecar file: {p}")

    rep = Report()
    check_pins(paths, rep)
    r8_recs = load_jsonl(paths["r8_jsonl"])
    r9_recs = load_jsonl(paths["r9_jsonl"])
    r8_summ_recomp, r8_summ_stored = grade_r8(r8_recs, read_text(paths["r8_runlog"]), rep)
    grade_r9(r9_recs, read_text(paths["r9_md"]), rep, r8_summ_recomp, r8_summ_stored)

    for line in rep.mismatches:
        print(line)
    print(f"CHECKS n={rep.checks} mismatches={len(rep.mismatches)} "
          f"errata_pinned={len(ERRATA)}")
    print("VERDICT: " + ("PASS — stored evidence fully re-derives offline"
                         if not rep.mismatches else "FAIL"))
    return 0 if not rep.mismatches else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:  # any unexpected crash is an input/env problem
        print(f"grader: INPUT ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)

#!/usr/bin/env python3
"""kengaku round-12 hermetic replay extension — DRAFT (integration owner: L1).

Drop-in extension of `grader.py` (round-11 gate, repo root). It replays the
round-12 evidence OFFLINE (no endpoint, no network, no /proc, stdlib only) and
re-derives every stored number from committed bytes. L1 integrates it into
`grader.py`; this file edits nothing else.

    python3 corpus/evidence/round12-fleet/grader_r12_draft.py --selftest-r12

What `grade_r12` verifies (given `recs`, `md_text`, `runlog_text`, `rep`):
  META     every family-1 meta regenerates exactly from `gen_problem(3000+pid*41)`
           for pids 201-264 (retry chain `+977` — 31/64 of the design seeds are
           rejected at least once, max 5 steps), stored `truth`/`tail_touched`
           re-derive from init+ops, and the family-1 problems are IDENTICAL to
           r11's committed metas (cross-tree check against
           `corpus/evidence/round11-power/results-r11.jsonl`).
  META2    every family-2 meta regenerates from the hash-pinned
           `probe_r12.py:gen_seq_problem(5000+pid*37)` (pids 401-448), with the
           plan §2.2 invariants (op-kind set ⊇ {DEL,MOV,REV}; last 3 ops touch
           >= 2 distinct positions) and no duplicate (init,ops).
  REPLAY   every graded record's stored got/want/ok/nwrong re-derives from its
           stored `raw` via the shipped `extract_json_block` (fenced block,
           bare-bracket fallback, parse-failure path), on family-1 key-map
           semantics and family-2 list semantics (length error + positional
           mismatches; parse failure -> nwrong = len(want)).
  CENSUS   per-cell record counts equal plan §4's formulas and the pinned totals
           (4 114 records, 4 002 HTTP calls at n1=64/n2=48); `descriptors` and
           `descriptors_end` both present, model ids equal (mid-run drift),
           `machinery_sha256` == sha256 of the committed `probe_r12.py`.
  SUMMARY  all seven `run.log` SUMMARY cell lines re-derive from the JSONL,
           `wall_total_s` present and > 0, progress-line count == the job count,
           and the per-pid arm order equals the §2.1 rotation / §2.2 parity rule.
  ANALYSIS every analysis_r12.md §5 stored line re-derives (arm table, E1 Page
           trend, E2-E5 paired stats, E6 Brier/BSS/calibration/reliability, finish
           audit, ack compliance, excluded pids, scoring table, ordering +
           descriptor sentences) and all five VERDICT lines are re-obtained by
           applying R1-R5 to the recomputed numbers (incl. POINT-MATCHES-r11 and
           the UNDERPOWERED-INDETERMINATE override).
  PRED     the per-problem probability file is located inside the prereg bundle,
           its sha256 equals the bundle-pinned digest, and the analysis' Brier/BSS
           is recomputed FROM THOSE COMMITTED PROBABILITIES and the observed
           outcomes (never from re-derived probabilities).
  ORDERING prereg-bundle.sha256 verifies from the repo root for every bundled
           file; ordering.log pre/post-hash <= run-script-hash <= first
           `request_ts` (plain `<=` string compare — r11 anti-pattern 15: never
           demand sub-second gaps at 1 s resolution), and the first stamped
           record in file order is the `descriptors` GET.
  VERDICT  R1-R5 re-derived from the recomputed statistics by the plan §2.3
           rules, including the R2 point-match clause and the n<56 / n<42
           underpowered override.

Lineage / textual copies (say so explicitly, per brief): the block between the
`verbatim copies from grader.py` markers — KEYS, MINUS, _SIGN_GLYPHS, Report,
extract_json_block, sim_apply, tail_touched, gen_problem, states_along,
grade_state, die, read_text, load_jsonl, file_sha256, parse_runlog_summary,
_mean, _sd_sample, _betacf, betai, t_two_sided_p, t_crit, _binom_cdf_le,
exact_sign_p, exact_mcnemar_p, _num — is copied byte-exact by
`ast.get_source_segment` from grader.py (line spans in the block header and in
corpus/evidence/round12-fleet/r12-grader-notes.md). Everything below the
`END verbatim copies` marker is new in round 12.

New machinery (see r12-grader-notes.md for the check inventory):
  * `_load_machinery` — loads `gen_seq_problem` (and only literal module-level
    constants / imports it needs) from the hash-pinned `probe_r12.py` WITHOUT
    executing import-time side effects (ast-scoped exec, not `import`), so the
    gate grades family 2 against the exact bytes that ran.
  * `sim_seq_apply` / `seq_states_along` / `grade_seq` — family-2 semantics
    transcribed from probe_plan_r12.md §2.2 (the op table and the nwrong metric
    are fully specified there), validated against every stored meta2 `truth`.
  * `page_l_trend` — Page's L for ordered treatments in randomized blocks with
    within-block midranks and the tie-corrected per-block variance (derivation
    documented in the function docstring).
  * `logistic_fit` / `logit_calibration` — damped Newton on logit(p) (max 50
    iterations, tol 1e-10) plus an optimizer-independent stationarity check at
    the STORED parameters.
  * `brier_scores` / `reliability_bins` — E6 scoring from the committed
    probabilities and the recomputed outcomes.

Statistics are stdlib-only and deterministic (`PYTHONHASHSEED`-independent: no
set-iteration order feeds any comparison; every iteration is over a sorted list
or an explicit order).

--------------------------------------------------------------------------------
PROMOTION PLAN FOR L1 (exact; this file is never edited at promotion)
--------------------------------------------------------------------------------
 1. Delete this file's `verbatim copies` block (grader.py defines all of it).
 2. Paste everything from the `R12-CODE` marker to the `fixture selftest` marker
    into grader.py after `check_r11_ordering`; keep `_find_repo_root` for the
    draft's benefit only if you also keep REPO_ROOT = HERE (grader.py already has
    REPO_ROOT via _find_repo_root from the r11 section — reuse it, drop this
    file's copy).
 3. DEFAULTS/PINS: add `r12_jsonl` / `r12_md` / `r12_runlog` (md5s taken from
    LOG.md at landing) and the R12_* sidecar constants already defined here.
 4. main(): add `--r12-jsonl/--r12-md/--r12-runlog`, add the three keys to
    `paths`, call `grade_r12(...)` + `check_r12_ordering(rep)` +
    `check_r12_pins(paths, rep, R12_PINS)`; fill R12_PINS at landing.
 5. Selftest: expose `--selftest-r12` (this file's fixture) and fold
    `selftest_stats_r12()` into `--selftest`.
Never issues a request to 127.0.0.1:34113 — hermetic, offline.
"""
import argparse
import ast
import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))


def _find_repo_root():
    """Repo root = nearest ancestor holding corpus/evidence/round12-ladder/.
    After integration into repo-root grader.py, `HERE` itself qualifies; the
    draft lives in corpus/evidence/round12-fleet/ so it needs three hops up."""
    for cand in (_HERE,
                 os.path.dirname(_HERE),
                 os.path.dirname(os.path.dirname(_HERE)),
                 os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))):
        if os.path.isdir(os.path.join(cand, "corpus", "evidence", "round12-ladder")):
            return cand
    return _HERE


REPO_ROOT = _find_repo_root()
R12_DIR = os.path.join(REPO_ROOT, "corpus/evidence/round12-ladder")
R12_JSONL = os.path.join(R12_DIR, "results-r12.jsonl")
R12_MD = os.path.join(R12_DIR, "analysis_r12.md")
R12_RUNLOG = os.path.join(R12_DIR, "run.log")
R12_ORDERING = os.path.join(R12_DIR, "ordering.log")
R12_SHA = os.path.join(R12_DIR, "prereg-bundle.sha256")
R12_PRED = os.path.join(R12_DIR, "predictions-r12.md")
R12_MACHINERY = os.path.join(R12_DIR, "probe_r12.py")
R11_DIR = os.path.join(REPO_ROOT, "corpus/evidence/round11-power")
R11_JSONL = os.path.join(R11_DIR, "results-r11.jsonl")
R11_MD = os.path.join(R11_DIR, "analysis_r11.md")

# Files that must be hash-pinned in prereg-bundle.sha256 BEFORE the run
# (plan §6.1: probe_plan_r12.md, power_analysis_r12.md, predictions-r12.md,
# predict_r12.py). The per-problem probability file is located STRUCTURALLY
# among the bundle's lines (it must be pre-hash-pinned to count as preregistered).
R12_REQUIRED_BUNDLE = ("probe_plan_r12.md", "power_analysis_r12.md",
                       "predictions-r12.md", "predict_r12.py",
                       "predictions-r12-perproblem.jsonl",
                       "predictions-r12-signevents.jsonl")
# Scripts whose post-fix hashes are appended to ordering.log (plan §6.5).
# The landed v1 ordering.log carries exactly two (probe_r12.py, run_r12.py);
# predict_r12.py is hash-pinned inside the bundle instead, so it is verified
# when a line exists but is not required.
R12_SCRIPT_HASH_REQUIRED = ("probe_r12.py", "run_r12.py")
R12_SCRIPT_FILES = ("probe_r12.py", "run_r12.py", "predict_r12.py")

# Pins for the landed bytes (LOG.md landing entry, r9/r11 convention). L1 fills
# this at promotion; empty means "no pin checks" (the fixture passes its own).
R12_PINS = {}

# ---------- design constants (probe_plan_r12.md §2) ----------
R12_N_PIDS_1 = 64
R12_PIDS_1 = list(range(201, 201 + R12_N_PIDS_1))
R12_SEED_SCHEME_1 = "3000+pid*41"
R12_N_PIDS_2 = 48
R12_PIDS_2 = list(range(401, 401 + R12_N_PIDS_2))
R12_SEED_SCHEME_2 = "5000+pid*37"
RETRY_STEP = 977


def r12_seed1(pid):
    return 3000 + pid * 41


def r12_seed2(pid):
    return 5000 + pid * 37


# §2.1 family-1 arms and the rotation Latin square.
F1_ARMS = ["A-INC", "A-CKPT4710", "A-CKPT710", "A-CKPT10", "A-MONO"]
LADDER_ARMS = ["A-INC", "A-CKPT4710", "A-CKPT710", "A-CKPT10"]   # E1 order INC < 4710 < 710 < 10
MONO_CELL = "A-MONO"
F2_ARMS = ["T-DENSE", "T-SPARSE"]

F1_CHECKPOINTS = {"A-INC": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                  "A-CKPT4710": (4, 7, 10), "A-CKPT710": (7, 10),
                  "A-CKPT10": (10,), "A-MONO": (1,)}
F2_CHECKPOINTS = {"T-DENSE": (4, 7, 10), "T-SPARSE": (7, 10)}
GRADED_CELLS = F1_ARMS + F2_ARMS
FINAL_TURN = {c: max(t) for c, t in F1_CHECKPOINTS.items()}
FINAL_TURN.update({c: max(t) for c, t in F2_CHECKPOINTS.items()})
ACK_CELLS = ["A-CKPT4710-ack", "A-CKPT710-ack", "A-CKPT10-ack",
             "T-DENSE-ack", "T-SPARSE-ack"]
# Ack turn sets: every turn of the cell that is NOT a graded checkpoint.
ACK_TURNS = {"A-CKPT4710-ack": tuple(t for t in range(1, 11) if t not in (4, 7, 10)),
             "A-CKPT710-ack": tuple(t for t in range(1, 11) if t not in (7, 10)),
             "A-CKPT10-ack": tuple(t for t in range(1, 11) if t not in (10,)),
             "T-DENSE-ack": tuple(t for t in range(1, 11) if t not in (4, 7, 10)),
             "T-SPARSE-ack": tuple(t for t in range(1, 11) if t not in (7, 10))}

# §2.3 verdict thresholds: the filed power floors (L1 delta 3 / D3: MC exact-t
# at dz=0.4288 gives 0.810 at n=44 and 0.791 at n=42, so BOTH floors are 44).
MIN_N_FAMILY_1 = 44
MIN_N_FAMILY_2 = 44
R2_POINT_TOL = 0.15
# §2.3/§5 say "448 pass events"; recomputation from §2/§4 gives 416 = 5*64 +
# 2*48 (448 = 7*64 is an arithmetic slip in the plan prose — flagged in
# r12-grader-notes.md). The gate pins the RECOMPUTED count and, at the filed
# n, additionally pins it to this constant.
E6_EVENTS_EXPECTED = {"n1": 64, "n2": 48, "events": 416, "sign": 304,
                      "runlevel": 7, "total": 727}


def census_expected(n1, n2):
    """Plan §4 per-cell counts and the two pinned totals, as functions of n."""
    graded = {"A-INC": 10 * n1, "A-CKPT4710": 3 * n1, "A-CKPT710": 2 * n1,
              "A-CKPT10": n1, "A-MONO": n1, "T-DENSE": 3 * n2, "T-SPARSE": 2 * n2}
    ack = {"A-CKPT4710-ack": 7 * n1, "A-CKPT710-ack": 8 * n1, "A-CKPT10-ack": 9 * n1,
           "T-DENSE-ack": 7 * n2, "T-SPARSE-ack": 8 * n2}
    return {"descriptors": 1, "descriptors_end": 1, "meta": n1, "meta2": n2,
            "graded": graded, "ack": ack, "fillers": 5 * n1 + 2 * n2,
            "errors": 0,
            "graded_total": sum(graded.values()), "ack_total": sum(ack.values()),
            "records": 2 + 47 * n1 + 23 * n2,
            "calls": 46 * n1 + 22 * n2 + 2,
            "stamped": 46 * n1 + 22 * n2 + 2,
            "unstamped": n1 + n2,
            "jobs": 5 * n1 + 2 * n2,
            "chat_calls": 46 * n1 + 22 * n2}


SECTION4_TOTALS = (4114, 4002, 416)   # records, HTTP calls, progress lines


def arm_order(pid):
    """§2.1 rotation: ARMS[(pid-201) % 5:] + ARMS[:(pid-201) % 5]."""
    r = (pid - 201) % 5
    return F1_ARMS[r:] + F1_ARMS[:r]


def arm_order_counts(pids):
    """{arm: [count at position 0..4]} realized by the rotation over `pids`."""
    out = {a: [0, 0, 0, 0, 0] for a in F1_ARMS}
    for pid in pids:
        for pos, arm in enumerate(arm_order(pid)):
            out[arm][pos] += 1
    return out


def f2_order(pid):
    """§2.2 counterbalance: even pid runs T-DENSE first."""
    return list(F2_ARMS) if pid % 2 == 0 else list(reversed(F2_ARMS))


# ---------- §5 stored-line templates (analysis_r12.md) ----------
_SIGNS = "[+\\-\u2212\u00b1]?"
_NUMF = r"\d+\.\d+"
_R12_STORED = {
    "counts": (r"results-r12\.jsonl contains (\d+) descriptors, (\d+) meta, "
               r"(\d+) meta2, (\d+) graded, (\d+) ack, (\d+) fillers, "
               r"(\d+) error records"),
    "arm_row": (r"^\| (A-INC|A-CKPT4710|A-CKPT710|A-CKPT10|A-MONO|T-DENSE|T-SPARSE) "
                r"\| (\d+)/(\d+) \| (" + _SIGNS + _NUMF + r") \| ("
                + _SIGNS + _NUMF + r") \|$"),
    "page": (r"E1 Page trend: L=(" + _SIGNS + r"\d+(?:\.\d+)?) E_L=(" + _SIGNS
             + r"\d+(?:\.\d+)?) var_L=(" + _SIGNS + r"\d+(?:\.\d+)?) z=(" + _SIGNS
             + _NUMF + r") two-sided p=(" + _NUMF
             + r") direction=(increasing|decreasing|neutral)"),
    "e2_diff": (r"E2 paired diff \(710 [\-\u2212\u2013] 4710, \{7,10\}\): ("
                + _SIGNS + _NUMF + r") sd (" + _NUMF + r") n=(\d+)"),
    "e2_p_fix": (r"E2 paired t: t=([+\-\u2212\u00b1]?\d+\.\d+), df=(\d+), "
                 r"two-sided p=(\d+\.\d+)"),
    "e2_t": (r"E2 paired t: t=(" + _SIGNS + _NUMF + r"), df=(\d+), two-sided p=("
             + _NUMF + r")"),
    "e2_ci": (r"E2 95% CI: \[(" + _SIGNS + _NUMF + r"), (" + _SIGNS + _NUMF + r")\]"),
    "e2_sign": (r"E2 exact sign: wins=(\d+) losses=(\d+) ties=(\d+) two-sided p=("
                + _NUMF + r")(?: direction=(\+1|-1|NEUTRAL))?"),
    "e2_mcnemar": r"E2 McNemar final passes: b=(\d+) c=(\d+) two-sided p=(" + _NUMF + r")",
    "e3": (r"E3 adjacent gaps: 4710-INC \{4,7,10\} (" + _SIGNS + _NUMF + r") p=("
           + _NUMF + r"); 710-4710 \{7,10\} (" + _SIGNS + _NUMF + r") p=(" + _NUMF
           + r"); 10-710 \{10\} (" + _SIGNS + _NUMF + r") p=(" + _NUMF + r")"),
    "e4": (r"E4 batching diff \(MONO [\-\u2212\u2013] CKPT10, final\): (" + _SIGNS
           + _NUMF + r") sd (" + _NUMF + r") n=(\d+) t=(" + _SIGNS + _NUMF
           + r") p=(" + _NUMF + r") sign W/L/T=(\d+)/(\d+)/(\d+)"),
    "e5": (r"E5 transport diff \(SPARSE [\-\u2212\u2013] DENSE, \{7,10\}\): ("
           + _SIGNS + _NUMF + r") sd (" + _NUMF + r") n=(\d+) t=(" + _SIGNS
           + _NUMF + r") p=(" + _NUMF + r") sign W/L/T=(\d+)/(\d+)/(\d+)"),
    "e6_events": (r"E6 events: pass=(\d+) sign=(\d+) runlevel=(\d+) total=(\d+)"),
    "e6_events_alt": (r"E6 event sets: pass (\d+)/(\d+) scored; sign (\d+)/(\d+) scored; "
                      r"run-level (\d+)/(\d+) scored; all scored events (\d+)/(\d+)"),
    "e6_brier_sign": (r"E6 Brier sign: pooled=(" + _NUMF + r") \(N=(\d+)\); "
                      r"(?:per-contrast )?((?:[A-Za-z0-9\-]+=" + _NUMF
                      + r")(?: [A-Za-z0-9\-]+=" + _NUMF + r")*)"),
    "e6_brier_sign_alt": (r"E6 Brier sign events: pooled=(" + _NUMF + r") \(N=(\d+)\); "
                          r"(?:per-contrast )?((?:[A-Za-z0-9\-]+=" + _NUMF
                          + r")(?: [A-Za-z0-9\-]+=" + _NUMF + r")*)"),
    "e6_brier_runlevel": (r"E6 Brier runlevel: pooled=(" + _NUMF + r") \(N=(\d+)\)"),
    "e6_brier_runlevel_alt": (r"E6 Brier run-level events: pooled=(" + _NUMF
                              + r") \(N=(\d+)\)"),
    "e6_brier_all": (r"E6 (?:Brier all(?: scored events)?|Brier pooled all): pooled=("
                     + _NUMF + r") \(N=(\d+)\)"),
    "e6_bss_groups": (r"E6 BSS sign=(n/a|" + _SIGNS + _NUMF + r") runlevel=(n/a|"
                      + _SIGNS + _NUMF + r") pooled-all-727=(n/a|" + _SIGNS + _NUMF + r")"),
    "e6_bss_groups_alt": (r"E6 BSS per group climatology: pass=(n/a|" + _SIGNS
                          + _NUMF + r") sign=(n/a|" + _SIGNS + _NUMF + r") run-level=(n/a|"
                          + _SIGNS + _NUMF + r") pooled=(n/a|" + _SIGNS + _NUMF + r")"),
    "e6_cal_all": (r"E6 calibration (?:secondary )?\(all (?:scored )?events\): slope=("
                   + _SIGNS + _NUMF + r") intercept=(" + _SIGNS + _NUMF
                   + r") \([^)]*?(\d+) events\)"),
    "e6_brier": (r"E6 Brier (?:pass: |pass |: )?pooled=(" + _NUMF + r") \(N=(\d+)\); (?:per-arm )?((?:"
                 r"[A-Za-z0-9\-]+=" + _NUMF + r")(?: [A-Za-z0-9\-]+=" + _NUMF + r")*)"),
    "e6_bss": (r"E6 BSS (?:pass )?vs arm climatology: (?:pooled=)?(n/a|" + _SIGNS
               + _NUMF + r")"),
    "e6_cal": (r"E6 calibration(?: \(pass events\))?: slope=(" + _SIGNS
               + _NUMF + r") intercept=(" + _SIGNS + _NUMF
               + r") \((?:damped )?Newton on logit\(p\)[^)]*?, (\d+) events\)"),
    "e6_rel": (r"^E6 reliability \(5 bins(?:, pass events)?\): ([\d.]+)-([\d.]+): "
               r"pred=(n/a|" + _NUMF + r") obs=(n/a|" + _NUMF + r") n=(\d+)$"),
    "finish": (r"Finish audit at graded turns: finish=length (\d+)/(\d+), parse fail "
               r"(\d+)/(\d+)"),
    "ack": (r"(A-CKPT4710|A-CKPT710|A-CKPT10|T-DENSE|T-SPARSE)(?:-ack)? (\d+)/(\d+) = ("
            + _NUMF + r")%"),
    "excluded": r"Excluded pids: family1 (\S+) family2 (\S+)",
    "verdict_r1": r"VERDICT R1 ladder: (.+)$",
    "verdict_r2": r"VERDICT R2 (?:repeat|replication): (.+)$",
    "verdict_r3": r"VERDICT R3 batching: (.+)$",
    "verdict_r4": r"VERDICT R4 transport: (.+)$",
    "verdict_r5": r"VERDICT R5 forecast: (.+)$",
    "score_header": r"^\| Quantity \| Predicted \| Observed \| Abs error(?: /[^|]*)? \|$",
    "score_row": r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
    "r11_diff": (r"Paired mean difference \(710 [\-\u2212\u2013] 4710, shared "
                 r"checkpoints \{7,10\}\): (" + _SIGNS + _NUMF + r")"),
}
DESCRIPTOR_SENTENCE_TOKENS = ("single served unit", "Qwen3-Coder-30B-A3B-Instruct",
                              "q4_0", "--kv-unified", "--parallel 2",
                              "no cross-model generalization")


# ---------- verbatim copies from grader.py (L1: DELETE this whole block at
#            promotion — grader.py already defines every one of these) ----------
# Line spans taken mechanically from grader.py by ast.get_source_segment
# (see corpus/evidence/round12-fleet/r12-grader-notes.md, "verbatim copies");
# only Report.erratum (which needs grader.py's module-level ERRATA) is dropped.
KEYS = ["nails", "bolts", "screws", "washers", "hinges"]


MINUS = "\u2212"


_SIGN_GLYPHS = {"\u2212": "-", "\u2013": "-", "\u2014": "-", "\u00b1": ""}


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
# ======================= R12-CODE =======================
# (L1: paste from here to the `fixture selftest` marker into grader.py after
#  check_r11_ordering; REPO_ROOT/RES packaging per the header promotion plan.)

# ---------- round-12 statistics (stdlib, deterministic) ----------
def _midranks(vals):
    """Within-block midranks 1..k for `vals` (ties share the average rank)."""
    k = len(vals)
    order = sorted(range(k), key=lambda i: vals[i])
    ranks = [0.0] * k
    i = 0
    while i < k:
        j = i
        while j + 1 < k and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for t in range(i, j + 1):
            ranks[order[t]] = avg
        i = j + 1
    return ranks


def page_l_trend(blocks):
    """Page's L ordered-trend test for randomized blocks (one row per pid).

    blocks[i][j] = value of treatment j (j = 1..k in the preregistered order
    INC < 4710 < 710 < 10) for block i. Ties take midranks; the variance is
    accumulated block-by-block, which handles ties exactly:

        S_i     = sum_j j * r_ij            (r_ij = within-block midranks)
        E[S_i]  = k (k+1)^2 / 4
        Var(S_i)= sigma2_pop(r_i) * k^2 (k+1) / 12
        sigma2_pop(r_i) = (1/k) sum_j (r_ij - (k+1)/2)^2

    (valid because a block's ranks always sum to k(k+1)/2; for untied ranks
    sigma2_pop = (k+1)(k-1)/12 and Var(L) = b k^2 (k+1)^2 (k-1)/144, the
    textbook value). z is the normal approximation; p is two-sided
    (erfc(|z|/sqrt(2))); `direction` is "increasing" iff L > E[L] (severity
    rising as forced-emission density falls), else "decreasing" (the L == E[L]
    degenerate case falls to "decreasing" — pinned here, probability-zero in
    practice).
    """
    b = len(blocks)
    k = len(blocks[0]) if b else 0
    L = 0.0
    var = 0.0
    for row in blocks:
        r = _midranks(row)
        L += sum((j + 1) * r[j] for j in range(k))
        mean_r = (k + 1) / 2.0
        s2 = sum((x - mean_r) ** 2 for x in r) / k
        var += s2 * k * k * (k + 1) / 12.0
    e_l = b * k * (k + 1) ** 2 / 4.0
    if var > 0:
        z = (L - e_l) / math.sqrt(var)
    else:                                  # D9: fully tied blocks -> z=+0.000, p=1.0000
        z = 0.0
    p = min(1.0, math.erfc(abs(z) / math.sqrt(2.0)))
    direction = ("increasing" if L > e_l else
                 ("decreasing" if L < e_l else "neutral"))
    return {"L": L, "E_L": e_l, "var_L": var, "z": z, "p": p, "direction": direction}


def paired_stats(diffs):
    """Paired mean/sd/t/p/CI + exact-sign counts over a list of per-pid diffs."""
    n = len(diffs)
    m = _mean(diffs)
    sd = _sd_sample(diffs)
    sem = sd / math.sqrt(n) if n else 0.0
    t = m / sem if sem > 0 else 0.0
    p = t_two_sided_p(t, n - 1) if n > 1 else 1.0
    tc = t_crit(n - 1, 0.05) if n > 1 else 0.0
    return {"n": n, "diff": m, "sd": sd, "t": t, "p": p,
            "ci_lo": m - tc * sem, "ci_hi": m + tc * sem,
            "wins": sum(1 for d in diffs if d > 0),
            "losses": sum(1 for d in diffs if d < 0),
            "ties": sum(1 for d in diffs if d == 0)}


def mcnemar_pairs(ok_a, ok_b):
    """b = a-pass/b-fail, c = converse, over the shared (sorted) pid set."""
    b = c = 0
    for pid in sorted(set(ok_a) & set(ok_b)):
        if ok_a[pid] and not ok_b[pid]:
            b += 1
        elif ok_b[pid] and not ok_a[pid]:
            c += 1
    return b, c, exact_mcnemar_p(b, c)


_LOGIT_EPS = 1e-6


def _logit(p):
    q = min(1.0 - _LOGIT_EPS, max(_LOGIT_EPS, p))
    return math.log(q / (1.0 - q))


def _sigmoid(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    z = math.exp(x)
    return z / (1.0 + z)


def _loglik(xs, ys, a, b):
    ll = 0.0
    for x, y in zip(xs, ys):
        p = _sigmoid(a + b * x)
        ll += y * math.log(max(p, 1e-300)) + (1.0 - y) * math.log(max(1.0 - p, 1e-300))
    return ll


def calibration_gradient(xs, ys, a, b):
    """[g_a, g_b] = gradient of the log-likelihood at (a, b); the MLE is 0."""
    ga = gb = 0.0
    for x, y in zip(xs, ys):
        r = y - _sigmoid(a + b * x)
        ga += r
        gb += r * x
    return ga, gb


def logistic_fit(xs, ys, max_iter=50, tol=1e-10):
    """Damped Newton on logit(p_cal) = a + b*logit(p_pred) (plan §5).

    Deterministic: fixed iteration cap, deterministic step-halving on the
    log-likelihood. Non-separable data only; a separation or a singular
    Hessian stops the loop early (and the caller's stationarity check then
    decides, so the gate never depends on a single optimizer path).
    """
    a, b = 0.0, 0.0
    for _ in range(max_iter):
        ga = gb = h11 = h12 = h22 = 0.0
        for x, y in zip(xs, ys):
            p = _sigmoid(a + b * x)
            w = p * (1.0 - p)
            ga += y - p
            gb += (y - p) * x
            h11 += w
            h12 += w * x
            h22 += w * x * x
        det = h11 * h22 - h12 * h12
        if det <= 0:
            break
        da = (h22 * ga - h12 * gb) / det
        db = (h11 * gb - h12 * ga) / det
        ll0 = _loglik(xs, ys, a, b)
        scale, ok = 1.0, False
        for _ in range(60):
            if _loglik(xs, ys, a + scale * da, b + scale * db) >= ll0 - 1e-15:
                ok = True
                break
            scale *= 0.5
        if not ok:
            break
        a += scale * da
        b += scale * db
        if abs(scale * da) < tol and abs(scale * db) < tol:
            break
    return a, b


def logistic_calibration(probs, outcomes):
    """slope/intercept of the logistic recalibration + |grad| at that point."""
    xs = [_logit(p) for p in probs]
    a, b = logistic_fit(xs, outcomes)
    ga, gb = calibration_gradient(xs, outcomes, a, b)
    return {"slope": b, "intercept": a, "grad_norm": math.hypot(ga, gb),
            "n": len(xs)}


def brier_scores(events, probs, outcomes):
    """Pooled + per-arm Brier and BSS vs the run's own per-arm climatology.

    events is a deterministic (sorted) list of (cell, pid) keys; probs/outcomes
    are dicts keyed by those events.
    """
    per_arm = {}
    for e in events:
        per_arm.setdefault(e[0], []).append((probs[e], outcomes[e]))
    pooled = _mean([(probs[e] - outcomes[e]) ** 2 for e in events])
    arm_brier = {c: _mean([(p - o) ** 2 for p, o in v]) for c, v in sorted(per_arm.items())}
    climat = {c: _mean([o for _p, o in v]) for c, v in sorted(per_arm.items())}
    ref = _mean([(climat[e[0]] - outcomes[e]) ** 2 for e in events])
    return {"pooled": pooled, "per_arm": arm_brier, "climatology": climat,
            "ref": ref, "bss": (1.0 - pooled / ref) if ref > 0 else 0.0,
            "n": len(events)}


REL_EDGES = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)


def reliability_bins(events, probs, outcomes, edges=REL_EDGES):
    """5 fixed-width reliability bins; the top bin is closed at 1.0.

    Returns [(lo, hi, mean_pred, mean_obs, n)] with empty bins reported as
    (lo, hi, 0.0, 0.0, 0) — plan §5 lists 5 bins per run.
    """
    out = []
    last = len(edges) - 2
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        sel = [e for e in events
               if (lo <= probs[e] < hi) or (i == last and probs[e] == hi)]
        out.append((lo, hi, _mean([probs[e] for e in sel]),
                    _mean([outcomes[e] for e in sel]), len(sel)))
    return out


# ---------- E6 event sets (amended §2.3/§5: three scored sets) ----------
SIGN_CONTRASTS = [("E3a", "A-CKPT4710", "A-INC", (4, 7, 10)),
                  ("E3b", "A-CKPT710", "A-CKPT4710", (7, 10)),
                  ("E3c", "A-CKPT10", "A-CKPT710", (10,)),
                  ("E4", MONO_CELL, "A-CKPT10", None),   # None: final-state pairing
                  ("E5", "T-SPARSE", "T-DENSE", (7, 10))]
RL_IDS = ["RL1", "RL2", "RL3", "RL4", "RL5", "RL6", "RL7"]
BSS_SPLITS = [("family1-replicate", ["A-CKPT4710", "A-CKPT710"]),
              ("family1-novel", ["A-INC", "A-CKPT10", "A-MONO"]),
              ("family2", ["T-DENSE", "T-SPARSE"])]


def _bss(ps, ys, clim):
    """1 - BS/BS_clim; None (rendered n/a) when the climatology is degenerate.

    Mirrors recompute_r12_draft.py:bss (NaN -> the analysis prints `n/a`), so a
    stored `n/a` is accepted exactly when bs_ref == 0.
    """
    if not ps:
        return None
    bs = _mean([(p - y) ** 2 for p, y in zip(ps, ys)])
    bs_ref = _mean([(c - y) ** 2 for c, y in zip(clim, ys)])
    if bs_ref <= 0.0:
        return None
    return 1.0 - bs / bs_ref


def _score_set(events, probs, group_fn):
    """Score one event set: pooled + per-group Brier, BSS vs own-group climatology.

    `events` is a deterministic list of ((key), y) with y in {0,1}; `probs` maps
    key -> filed probability (None drops the event from BOTH score and
    climatology, never scored as a failure).
    """
    keys, ps, ys, groups, unmapped = [], [], [], [], []
    for key, y in events:
        p = probs.get(key) if probs else None
        if p is None or not (0.0 <= p <= 1.0):
            unmapped.append(key)
            continue
        keys.append(key)
        ps.append(p)
        ys.append(y)
        groups.append(group_fn(key))
    gsum, gcnt = {}, {}
    for g, y in zip(groups, ys):
        gsum[g] = gsum.get(g, 0) + y
        gcnt[g] = gcnt.get(g, 0) + 1
    clim = [gsum[g] / gcnt[g] for g in groups]
    per_group = {}
    for g in sorted(set(groups)):
        idx = [k for k, gg in enumerate(groups) if gg == g]
        per_group[g] = _mean([(ps[k] - ys[k]) ** 2 for k in idx])
    return {"keys": keys, "ps": ps, "ys": ys, "groups": groups, "clim": clim,
            "n": len(ps), "events": len(events), "unmapped": unmapped,
            "brier": _mean([(p - y) ** 2 for p, y in zip(ps, ys)]) if ps else None,
            "bss": _bss(ps, ys, clim), "per_group": per_group,
            "group_rate": {g: gsum[g] / gcnt[g] for g in sorted(gcnt)}}


def _paired_pairs_turns(nw, cell_a, turns_a, cell_b, turns_b, pids):
    """[(pid, mean_A, mean_B)] for the pids that carry every needed turn."""
    out = []
    for pid in sorted(pids):
        try:
            a = _mean([nw[cell_a][pid][t] for t in turns_a])
            b = _mean([nw[cell_b][pid][t] for t in turns_b])
        except KeyError:
            continue
        out.append((pid, a, b))
    return out


def sign_event_pairs(nw, cid, cell_a, cell_b, turns, pids):
    """Sign-event pairs for one contrast (E4 = final-state pairing, turns None)."""
    if turns is None:
        return _paired_pairs_turns(nw, cell_a, (FINAL_TURN[cell_a],),
                                  cell_b, (FINAL_TURN[cell_b],), pids)
    return _paired_pairs_turns(nw, cell_a, turns, cell_b, turns, pids)


def _close_dp(s, value):
    """Compare a stored decimal string at its own printed precision (half ulp).

    §5 pins the decimals (e.g. `L=<f.1>`, `var_L=<f.3>`, `p=<f.pppp>`), so a
    stored value is correct iff it equals the recomputation rounded to that many
    decimals; `n/a` never matches a number.
    """
    v = _safe_num(s)
    if v is None or value is None:
        return False
    t = s.strip()
    dp = len(t.split(".")[1]) if "." in t else 0
    return abs(v - value) <= 0.5 * (10.0 ** -dp) + 1e-9


def _retry_depth(gen, scheme, init, ops, cap=40):
    """Smallest k with gen(scheme + k*977) reproducing (init, ops); None if none.

    The round-12 family-2 generator is RECURSIVE (`gen_seq_problem(seed+977)`),
    so the +977 chain is not reported by the callable: the chain is re-derived
    by reproduction, which also works for the iterative family-1 port.
    """
    for k in range(cap + 1):
        try:
            out = _unpack_gen(gen(scheme + RETRY_STEP * k))
        except Exception:  # noqa: BLE001 - a generator failure is a mismatch
            return None
        i2, o2 = out[0], [list(o) for o in out[1]]
        if i2 == init and o2 == ops:
            return k
    return None


def _parse_realized_positions(line):
    """{arm: [count per position 1..5]} from either §5 rendering, or None.

    Handles the plan form (`Realized arm positions after deletion: A-INC:13 12
    13 13 13 ...`) and the recompute_r12_draft form (`Realized arm-position
    counts (family 1, post-deletion): pos1 A-INC=13 A-CKPT4710=... ; pos2 ...`).
    """
    if not line:
        return None
    if re.search(r"pos\d", line):
        mat = {}
        for seg in re.split(r"pos(\d)", line):
            pass
        parts = re.split(r"pos(\d)", line)
        for i in range(1, len(parts) - 1, 2):
            pos = int(parts[i])
            for arm, cnt in re.findall(r"(A-INC|A-CKPT4710|A-CKPT710|A-CKPT10|A-MONO)\s*=\s*(\d+)",
                                       parts[i + 1]):
                mat.setdefault(arm, {})[pos] = int(cnt)
        if mat:
            return {a: [mat.get(a, {}).get(p, None) for p in range(1, 6)] for a in F1_ARMS}
    mat = {}
    toks = re.split(r"(?=A-INC|A-CKPT4710|A-CKPT710|A-CKPT10|A-MONO)", line)
    for tok in toks:
        m = re.match(r"(A-INC|A-CKPT4710|A-CKPT710|A-CKPT10|A-MONO)\b(.*)$", tok)
        if not m:
            continue
        nums = [int(x) for x in re.findall(r"\d+", m.group(2))][:5]
        if len(nums) == 5:
            mat[m.group(1)] = nums
    return mat if len(mat) == len(F1_ARMS) else None


# ---------- family-2 semantics (probe_plan_r12.md §2.2, transcribed) ----------
def sim_seq_apply(state, op):
    """Positional token-list op semantics (0-based indices, operand in range)."""
    s = list(state)
    kind = op[0]
    if kind == "APP":
        s.append(op[1])
    elif kind == "INS":
        s.insert(op[1], op[2])
    elif kind == "DEL":
        del s[op[1]]
    elif kind == "SET":
        s[op[1]] = op[2]
    elif kind == "MOV":
        t = s.pop(op[1])
        s.insert(op[2], t)
    elif kind == "SWP":
        s[op[1]], s[op[2]] = s[op[2]], s[op[1]]
    elif kind == "REV":
        i, j = op[1], op[2]
        s[i:j + 1] = list(reversed(s[i:j + 1]))
    return s


def seq_states_along(init, ops):
    s, out = list(init), []
    for op in ops:
        s = sim_seq_apply(s, op)
        out.append(s)
    return out


def grade_seq(got, want):
    """§2.2 metric: |len differ| + positional mismatches; non-list -> len(want)."""
    if not isinstance(got, list):
        return False, len(want)
    n = min(len(got), len(want))
    wrong = abs(len(got) - len(want)) + sum(1 for i in range(n) if got[i] != want[i])
    return got == want, wrong


# ---------- machinery loader (hash-pinned probe_r12.py, side-effect free) ----
def _literal_ast(node):
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return all(_literal_ast(e) for e in node.elts)
    if isinstance(node, ast.Dict):
        return (all(_literal_ast(k) for k in node.keys if k is not None)
                and all(_literal_ast(v) for v in node.values))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        return _literal_ast(node.operand)
    return False


def _load_machinery(path, names):
    """Load `names` from a committed probe script WITHOUT running side effects.

    Only module-level imports, function/class defs and literal-only assignments
    are compiled and exec'd; an import-time `open(...)`/`LOGF = f(...)`/
    `sys.exit()` is deliberately skipped (r11 INTEGRATOR-NOTES MINOR (e): a
    plain `import probe_r11` creates a stray results.jsonl in OUT). Contract on
    probe_r12.py: `gen_seq_problem` and every helper it calls must be reachable
    from module-level defs + literal constants.
    Returns (namespace, missing_names); namespace is None on a hard failure.
    """
    if not os.path.isfile(path):
        return None, [f"missing machinery file {path}"]
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src)
    except (OSError, SyntaxError) as e:
        return None, [f"{path}: {type(e).__name__}: {e}"]
    keep = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef,
                             ast.AsyncFunctionDef, ast.ClassDef)):
            keep.append(node)
        elif (isinstance(node, ast.Assign) and len(node.targets) == 1
              and isinstance(node.targets[0], ast.Name) and _literal_ast(node.value)):
            keep.append(node)
    ns = {"__name__": "kengaku_r12_machinery", "__file__": path}
    try:
        exec(compile(ast.Module(body=keep, type_ignores=[]), path, "exec"), ns)
    except Exception as e:  # a broken probe script is a mismatch, not a crash
        return None, [f"{path}: exec {type(e).__name__}: {e}"]
    return ns, [n for n in names if n not in ns]


def _unpack_gen(out):
    """gen_seq_problem may return (init, ops) or (init, ops, retries)."""
    if isinstance(out, (tuple, list)) and len(out) >= 2:
        retries = int(out[2]) if len(out) > 2 else 0
        return out[0], out[1], retries
    raise ValueError(f"unexpected generator return: {type(out).__name__}")


def _tail_positions(ops, count=3):
    """Distinct integer position operands touched by the last `count` ops."""
    pos = set()
    for op in ops[-count:]:
        for operand in op[1:]:
            if isinstance(operand, int):
                pos.add(operand)
    return pos


def f2_invariants(ops):
    """Plan §2.2 pre-hash invariants: op kinds ⊇ {DEL,MOV,REV} and the last 3
    ops touch >= 2 distinct positions. Returns (ok, sorted_kinds, sorted_pos)."""
    kinds = sorted({o[0] for o in ops})
    pos = sorted(_tail_positions(ops))
    ok = {"DEL", "MOV", "REV"} <= set(kinds) and len(pos) >= 2
    return ok, kinds, pos


# ---------- tolerant record introspection ----------
def _walk(obj):
    """Deterministic walk of every (key, value) pair in a nested record."""
    if isinstance(obj, dict):
        for k in sorted(obj, key=str):
            yield k, obj[k]
            for sub in _walk(obj[k]):
                yield sub
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield i, v
            for sub in _walk(v):
                yield sub


def _hex_set(obj):
    return {v for _k, v in _walk(obj)
            if isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v)}


def _model_ids(models_json):
    """Model-id-ish strings under id/name/model keys (sorted, de-duplicated)."""
    ids = set()
    for k, v in _walk(models_json):
        if isinstance(v, str) and isinstance(k, str) and \
                k.lower() in ("id", "name", "model", "model_id", "served_model"):
            ids.add(v)
    return sorted(ids)


def _int_values(obj):
    return {v for _k, v in _walk(obj) if isinstance(v, int) and not isinstance(v, bool)}


def _list_values(obj):
    return [v for _k, v in _walk(obj) if isinstance(v, list)]


def _string_values(obj):
    return [v for _k, v in _walk(obj) if isinstance(v, str)]


def _get_key(obj, *needles):
    """First (key, value) whose lowercased key contains any needle."""
    for k, v in _walk(obj):
        if isinstance(k, str):
            kl = k.lower()
            if any(nd in kl for nd in needles):
                return k, v
    return None, None


def _hash_file(algo, path):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- round-12 meta / meta2 ----------
def _meta_index(recs, cell):
    out = {}
    for r in recs:
        if r.get("cell") == cell:
            out.setdefault(r.get("pid"), []).append(r)
    return out


def _want_for(cell, pid, turn, truth):
    tr = truth.get(pid)
    if not tr:
        return None
    if cell == MONO_CELL:
        return tr[-1]
    return tr[turn - 1] if 1 <= turn <= len(tr) else None


def _check_meta_f1(recs, rep, pids, r11_path=None):
    """Family-1 metas: scheme seed, +977 retry chain, regeneration, r11 identity."""
    seen = _meta_index(recs, "meta")
    rep.eq("r12.meta.count", sum(len(v) for v in seen.values()), len(pids))
    rep.ok("r12.meta.unique_pids", all(len(v) == 1 for v in seen.values()),
           f"duplicate meta pids: {sorted(p for p, v in seen.items() if len(v) > 1)}")
    rep.eq("r12.meta.pid_set", sorted(seen), sorted(pids))
    diffs = {k: [] for k in ("init", "ops", "truth", "tail", "seed", "chain", "retries")}
    conventions = set()
    n_retried = 0
    truth_by_pid = {}
    for pid in sorted(pids):
        if pid not in seen:
            continue
        m = seen[pid][0]
        scheme = r12_seed1(pid)
        init2, ops2, retries = gen_problem(scheme)
        if retries:
            n_retried += 1
        if init2 != m.get("init"):
            diffs["init"].append(pid)
        if ops2 != m.get("ops"):
            diffs["ops"].append(pid)
        truth = states_along(m["init"], [tuple(o) for o in m["ops"]])
        if truth != m.get("truth"):
            diffs["truth"].append(pid)
        if sorted(tail_touched([tuple(o) for o in m["ops"]])) != m.get("tail_touched"):
            diffs["tail"].append(pid)
        ss = m.get("seed")
        accepted = scheme + RETRY_STEP * retries
        if not isinstance(ss, int):
            diffs["seed"].append(pid)
        elif ss == scheme:
            conventions.add("scheme-seed")
        elif ss == accepted:
            conventions.add("accepted-seed")
        else:
            diffs["seed"].append(pid)
        if isinstance(ss, int) and (ss - scheme) % RETRY_STEP == 0 and ss >= scheme:
            i3, o3, _ = gen_problem(ss)
            if i3 != m.get("init") or o3 != m.get("ops"):
                diffs["chain"].append(pid)
        elif isinstance(ss, int):
            diffs["chain"].append(pid)
        if "retries" in m and m["retries"] != retries:
            diffs["retries"].append(pid)
        truth_by_pid[pid] = truth
    for field, cid in (("init", "regenerate.init"), ("ops", "regenerate.ops"),
                       ("truth", "regenerate.truth"), ("tail", "regenerate.tail_touched"),
                       ("seed", "seed"), ("chain", "retry_chain"), ("retries", "retries_field")):
        ids = diffs[field]
        rep.ok(f"r12.meta.{cid}", not ids,
               f"{len(ids)}/{len(pids)} pids differ: {ids[:4]}")
    rep.ok("r12.meta.seed_convention_consistent", len(conventions) == 1,
           f"mixed stored-seed conventions across pids: {sorted(conventions)}")
    rep.ok("r12.meta.retry_chain_exercised", n_retried > 0,
           f"{n_retried}/{len(pids)} design seeds are rejected at least once under "
           f"gen_problem (+977 chain) — a run whose metas show 0 rejects does not "
           f"regenerate through the documented chain")
    if r11_path is None or not os.path.isfile(r11_path):
        rep.ok("r12.meta.r11_identity.source_present", False,
               f"missing committed r11 jsonl: {r11_path}")
    else:
        r11 = {r["pid"]: r for r in load_jsonl(r11_path) if r.get("cell") == "meta"}
        covered = [p for p in sorted(pids) if p in r11 and p in seen]
        rep.eq("r12.meta.r11_identity.pids_covered", covered, sorted(pids))
        for field in ("init", "ops", "truth", "tail_touched"):
            bad = [p for p in covered
                   if seen[p][0].get(field) != r11[p].get(field)]
            rep.ok(f"r12.meta.r11_identity.{field}", not bad,
                   f"{len(bad)} pids differ from r11's committed meta {field}: {bad[:4]}")
    return truth_by_pid


def _feat_eq(key, stored, feat):
    kl = key.lower()
    if any(t in kl for t in ("kind", "pos")):
        if isinstance(stored, list) and isinstance(feat.get(key), list):
            return sorted(stored) == sorted(feat[key])
        if isinstance(stored, list) and isinstance(feat.get(key), list) is False:
            return False
    return stored == feat.get(key)


def _check_meta_f2(recs, rep, pids, machinery_path):
    """Family-2 metas regenerate through the hash-pinned probe_r12.py generator."""
    seen = _meta_index(recs, "meta2")
    rep.eq("r12.meta2.count", sum(len(v) for v in seen.values()), len(pids))
    rep.ok("r12.meta2.unique_pids", all(len(v) == 1 for v in seen.values()),
           f"duplicate meta2 pids: {sorted(p for p, v in seen.items() if len(v) > 1)}")
    rep.eq("r12.meta2.pid_set", sorted(seen), sorted(pids))
    ns, missing = _load_machinery(machinery_path, ["gen_seq_problem"])
    rep.ok("r12.meta2.machinery.gen_seq_problem", ns is not None and not missing,
           f"cannot load gen_seq_problem from {machinery_path}: {missing} "
           f"(contract: module-level def + literal constants only)")
    if ns is None or missing:
        return {}
    gen = ns["gen_seq_problem"]
    diffs = {k: [] for k in ("generate", "init", "ops", "truth", "seed", "chain",
                             "features", "invariants")}
    pairs = []
    depths = []
    truth_by_pid = {}
    for pid in sorted(pids):
        if pid not in seen:
            continue
        m = seen[pid][0]
        scheme = r12_seed2(pid)
        try:
            init2, ops2, retries = _unpack_gen(gen(scheme))
        except Exception as e:  # noqa: BLE001 - any generator failure is a mismatch
            diffs["generate"].append(f"{pid}:{type(e).__name__}")
            continue
        # probe_r12.py's family-2 generator RECURSES on seed+977 and returns a
        # 2-tuple, so the chain depth is re-derived by reproduction instead
        depth = _retry_depth(gen, scheme, m.get("init"),
                             [list(o) for o in m.get("ops", [])])
        if init2 != m.get("init"):
            diffs["init"].append(pid)
        if ops2 != [list(o) for o in m.get("ops", [])]:
            diffs["ops"].append(pid)
        truth = seq_states_along(m["init"], m.get("ops", []))
        if truth != m.get("truth"):
            diffs["truth"].append(pid)
        kinds = sorted({o[0] for o in m.get("ops", [])})
        pos = sorted(_tail_positions(m.get("ops", [])))
        inv_ok, _k2, _p2 = f2_invariants(m.get("ops", []))
        if not inv_ok:
            diffs["invariants"].append(pid)
        feat = {"kinds": kinds, "op_kinds": kinds, "kinds_present": kinds,
                "tail_positions": pos, "positions": pos,
                "n_ops": len(m.get("ops", [])), "len_init": len(m.get("init", [])),
                "n_tokens": len(m.get("init", [])), "n_truth": len(truth)}
        f = m.get("features")
        if not isinstance(f, dict) or not f:
            diffs["features"].append(f"{pid}:no-dict")
        else:
            recognized = [k for k in sorted(f) if k in feat]
            if not recognized:
                diffs["features"].append(f"{pid}:no-recognized-key")
            for k in recognized:
                if not _feat_eq(k, f[k], feat):
                    diffs["features"].append(f"{pid}:{k}")
        ss = m.get("seed")
        if not isinstance(ss, int) or (ss - scheme) % RETRY_STEP != 0 or ss < scheme:
            diffs["seed"].append(pid)
        elif depth is None or ss not in (scheme, scheme + RETRY_STEP * depth):
            diffs["seed"].append(f"{pid}:seed-not-on-chain")
        else:
            try:
                i3, o3, _ = _unpack_gen(gen(ss))
                if i3 != m.get("init") or o3 != [list(o) for o in m.get("ops", [])]:
                    diffs["chain"].append(pid)
            except Exception:  # noqa: BLE001
                diffs["chain"].append(pid)
        if "retries" in m and m["retries"] != retries:
            diffs["chain"].append(f"{pid}:retries")
        if depth is None:
            diffs["chain"].append(f"{pid}:depth-unrecoverable")
        depths.append(depth)
        pairs.append(json.dumps([m.get("init"), m.get("ops")], sort_keys=True))
        truth_by_pid[pid] = truth
    for field, cid in (("generate", "generate"), ("init", "regenerate.init"),
                       ("ops", "regenerate.ops"), ("truth", "regenerate.truth"),
                       ("seed", "seed"), ("chain", "retry_chain"),
                       ("features", "features"), ("invariants", "plan_invariants")):
        ids = list(dict.fromkeys(diffs[field]))
        rep.ok(f"r12.meta2.{cid}", not ids, f"{len(ids)}/{len(pids)} pids differ: {ids[:4]}")
    rep.ok("r12.meta2.unique_problems", len(set(pairs)) == len(pairs),
           f"{len(pairs) - len(set(pairs))} duplicate (init,ops) within family 2")
    rep.ok("r12.meta2.retry_chain_reproduction", not diffs["chain"],
           f"{len(diffs['chain'])}/{len(pids)} pids whose +977 depth is not recoverable "
           f"by reproduction; depths {depths}")
    f1 = {json.dumps([m.get("init"), m.get("ops")], sort_keys=True)
          for m in [v[0] for v in _meta_index(recs, "meta").values()]}
    rep.ok("r12.meta2.disjoint_from_family1", not (set(pairs) & f1),
           f"{len(set(pairs) & f1)} family-2 problems duplicate a family-1 problem")
    return truth_by_pid


# ---------- round-12 raw re-parse / re-grade ----------
_FENCE_RE = re.compile(r"```")
_BARE_RE = re.compile(r"\[[^\[\]]*\]")


def _check_replay(recs, rep, truth1, truth2):
    """Every graded record's stored got/want/ok/nwrong vs a fresh re-parse."""
    by_cell = {}
    for r in recs:
        c = r.get("cell", "")
        if c in GRADED_CELLS and "ok" in r:
            by_cell.setdefault(c, []).append(r)
    truth_of = {c: (truth1, 1, F1_CHECKPOINTS[c]) for c in F1_ARMS}
    truth_of.update({c: (truth2, 2, F2_CHECKPOINTS[c]) for c in F2_ARMS})
    for cell in GRADED_CELLS:
        rows = by_cell.get(cell, [])
        truth, fam, turns = truth_of[cell]
        rep.eq(f"r12.replay.{cell}.turn_set", sorted({r["turn"] for r in rows}),
               sorted(turns))
        diffs = {"got": 0, "want": 0, "ok": 0, "nwrong": 0}
        first = None
        parse_bad = []
        bare_bad = []
        for r in rows:
            pid, turn = r["pid"], r["turn"]
            want = _want_for(cell, pid, turn, truth)
            if want is None:
                diffs["want"] += 1
                first = first or (pid, turn, "no meta/turn")
                continue
            got = extract_json_block(r.get("raw", ""))
            ok_re, nw_re = (grade_state(got, want) if fam == 1 else grade_seq(got, want))
            if got is None and (r.get("ok") is not False or r.get("nwrong") != len(want)):
                parse_bad.append((pid, turn))
            raw = r.get("raw", "")
            if (not _FENCE_RE.search(raw) and _BARE_RE.search(raw)
                    and got is None and r.get("got") is not None):
                bare_bad.append((pid, turn))
            for field, recomp, stored in (("got", got, r.get("got")),
                                          ("want", want, r.get("want")),
                                          ("ok", ok_re, r.get("ok")),
                                          ("nwrong", nw_re, r.get("nwrong"))):
                if recomp != stored:
                    diffs[field] += 1
                    first = first or (pid, turn, field)
        for field in ("got", "want", "ok", "nwrong"):
            rep.ok(f"r12.replay.{cell}.{field}", diffs[field] == 0,
                   f"{diffs[field]}/{len(rows)} records differ (first: {first})")
        rep.ok(f"r12.replay.{cell}.parse_fail_path", not parse_bad,
               f"{len(parse_bad)} unparseable raws whose stored ok/nwrong break the "
               f"§2.2 convention (ok=False, nwrong=len(want)): {parse_bad[:3]}")
        rep.ok(f"r12.replay.{cell}.bare_bracket_path", not bare_bad,
               f"{len(bare_bad)} unfenced bare-array raws the shipped parser cannot "
               f"recover while `got` is stored non-null: {bare_bad[:3]}")
    # ack + filler structure
    for cell in ACK_CELLS:
        rows = [r for r in recs if r.get("cell") == cell]
        rep.eq(f"r12.replay.{cell}.turn_set", sorted({r["turn"] for r in rows}),
               list(ACK_TURNS[cell]))
        rep.ok(f"r12.replay.{cell}.raw_truncated",
               all(len(str(r.get("raw", ""))) <= 80 for r in rows),
               f"{sum(1 for r in rows if len(str(r.get('raw', ''))) > 80)} acks exceed 80 chars")
    fillers = [r for r in recs if r.get("cell") == "filler"]
    rep.ok("r12.replay.filler.fields",
           all(all(k in r for k in ("finish", "usage", "wall_s", "raw", "request_ts"))
               for r in fillers),
           f"{sum(1 for r in fillers if not all(k in r for k in ('finish','usage','wall_s','raw','request_ts')))}"
           f"/{len(fillers)} filler records lack a required field")


# ---------- round-12 census ----------
def _check_census(recs, rep, n1, n2):
    exp = census_expected(n1, n2)
    rep.eq("r12.census.descriptors", sum(1 for r in recs if r.get("cell") == "descriptors"), 1)
    rep.eq("r12.census.descriptors_end", sum(1 for r in recs if r.get("cell") == "descriptors_end"), 1)
    rep.eq("r12.census.meta", sum(1 for r in recs if r.get("cell") == "meta"), n1)
    rep.eq("r12.census.meta2", sum(1 for r in recs if r.get("cell") == "meta2"), n2)
    for cell in GRADED_CELLS:
        rep.eq(f"r12.census.graded.{cell}",
               sum(1 for r in recs if r.get("cell") == cell and "ok" in r),
               exp["graded"][cell])
    for cell in ACK_CELLS:
        rep.eq(f"r12.census.ack.{cell}", sum(1 for r in recs if r.get("cell") == cell),
               exp["ack"][cell])
    fillers = sum(1 for r in recs if r.get("cell") == "filler")
    errors = sum(1 for r in recs if r.get("cell") == "error")
    rep.eq("r12.census.fillers", fillers, exp["fillers"])
    rep.eq("r12.census.errors", errors, exp["errors"])
    rep.eq("r12.census.graded_total",
           sum(1 for r in recs if r.get("cell") in GRADED_CELLS and "ok" in r),
           exp["graded_total"])
    rep.eq("r12.census.ack_total", sum(1 for r in recs if r.get("cell") in ACK_CELLS),
           exp["ack_total"])
    rep.eq("r12.census.graded_missing_ok",
           sum(1 for r in recs if r.get("cell") in GRADED_CELLS and "ok" not in r), 0)
    rep.eq("r12.census.ack_has_ok",
           sum(1 for r in recs if str(r.get("cell", "")).endswith("-ack") and "ok" in r), 0)
    # §4 pins cell:"A-INC-ack" = 0 (INC grades every turn, so it emits no acks)
    rep.eq("r12.census.no_inc_acks",
           sum(1 for r in recs if r.get("cell") == "A-INC-ack"), 0)
    rep.eq("r12.census.total_records", len(recs), exp["records"])
    stamped = sum(1 for r in recs if r.get("request_ts"))
    rep.eq("r12.census.stamped_records", stamped, exp["stamped"])
    rep.eq("r12.census.unstamped_records", len(recs) - stamped, exp["unstamped"])
    # every request-bearing record is exactly one chat call; +2 /v1/models GETs
    chat = sum(1 for r in recs if r.get("cell") in GRADED_CELLS + ACK_CELLS + ["filler"])
    rep.eq("r12.census.chat_calls", chat, exp["chat_calls"])
    rep.eq("r12.census.http_calls", chat + 2, exp["calls"])
    if (n1, n2) == (R12_N_PIDS_1, R12_N_PIDS_2):
        rep.eq("r12.census.section4_records_calls",
               (len(recs), chat + 2), SECTION4_TOTALS[:2])


# ---------- round-12 descriptors ----------
def _norm_counts(v):
    """Normalise an arm/position count structure to {arm: [count]*5}, or None."""
    if not isinstance(v, dict) or set(v) != set(F1_ARMS):
        return None
    out = {}
    for arm in F1_ARMS:
        c = v[arm]
        if isinstance(c, dict):
            try:
                out[arm] = [int(c[k]) if k in c else int(c[str(k)]) for k in range(5)]
            except (KeyError, TypeError, ValueError):
                return None
        elif isinstance(c, list) and len(c) == 5 and all(isinstance(x, int) for x in c):
            out[arm] = list(c)
        else:
            return None
    return out


def _check_descriptors(recs, rep, n1, n2, pids1, pids2, machinery_path,
                       bundle_path=None, ordering_path=None):
    desc = [r for r in recs if r.get("cell") == "descriptors"]
    rep.eq("r12.descriptors.count", len(desc), 1)
    if len(desc) != 1:
        return
    d = desc[0]
    rep.ok("r12.descriptors.request_ts", bool(d.get("request_ts")),
           "descriptors record carries no request_ts")
    ids = _model_ids(d.get("models_json")) if d.get("models_json") is not None else []
    rep.ok("r12.descriptors.models_json_ids", bool(ids),
           f"no model id under id/name/model keys in models_json: {str(d.get('models_json'))[:120]}")
    lv = _list_values(d)
    rep.ok("r12.descriptors.pids1", any(v == pids1 for v in lv),
           "no list-valued field equals the family-1 pid list")
    rep.ok("r12.descriptors.pids2", any(v == pids2 for v in lv),
           "no list-valued field equals the family-2 pid list")
    iv = _int_values(d)
    rep.ok("r12.descriptors.n_consistent", n1 in iv and n2 in iv,
           f"int values {sorted(iv)[:8]} lack n1={n1}/n2={n2}")
    sv = _string_values(d)
    rep.ok("r12.descriptors.seed_schemes",
           R12_SEED_SCHEME_1 in sv and R12_SEED_SCHEME_2 in sv,
           f"both seed schemes must appear as strings: have {sorted(set(sv))[:6]}")
    _k, temp = _get_key(d, "temp")
    _k, maxtok = _get_key(d, "maxtok", "max_tokens")
    rep.ok("r12.descriptors.temp", temp == 0.2, f"temp field {temp!r} != 0.2 (plan §2.1)")
    rep.ok("r12.descriptors.maxtok", maxtok == 8192, f"maxtok field {maxtok!r} != 8192")
    _k, sp = _get_key(d, "system_prompt", "system")
    rep.ok("r12.descriptors.system_prompt", isinstance(sp, str) and bool(sp.strip()),
           f"system prompt missing/empty: {sp!r}")
    ns, missing = _load_machinery(machinery_path, ["SYSTEM"])
    if ns is not None and "SYSTEM" in ns:
        rep.eq("r12.descriptors.system_prompt_matches_machinery", sp, ns["SYSTEM"])
    else:
        rep.ok("r12.descriptors.system_prompt_matches_machinery", False,
               f"probe_r12.py exposes no SYSTEM to compare against ({missing})")
    _k, ep = _get_key(d, "endpoint")
    rep.ok("r12.descriptors.endpoint", isinstance(ep, str) and bool(ep),
           f"endpoint field missing/empty: {ep!r}")
    _k, srv = _get_key(d, "server", "argv", "pid")
    rep.ok("r12.descriptors.server_info", srv is not None,
           "no server/argv/pid field (plan §3: best effort, but it must be recorded)")
    mach = d.get("machinery_sha256")
    ok_mach = (isinstance(mach, str) and os.path.isfile(machinery_path)
               and mach == file_sha256(machinery_path))
    rep.ok("r12.descriptors.machinery_sha256", ok_mach,
           f"machinery_sha256 {mach!r} != sha256({machinery_path})")
    dir_path = os.path.dirname(machinery_path)
    want_hashes = {}
    for name in R12_SCRIPT_FILES:
        p = os.path.join(dir_path, name)
        if os.path.isfile(p):
            want_hashes[name] = file_sha256(p)
    if bundle_path and os.path.isfile(bundle_path):
        want_hashes["prereg-bundle.sha256"] = file_sha256(bundle_path)
    have = _hex_set(d)
    miss_h = sorted(k for k, v in want_hashes.items() if v not in have)
    rep.ok("r12.descriptors.script_hashes_present", not miss_h,
           f"descriptors record does not pin the sha256 of: {miss_h}")
    bk, bv = _get_key(d, "bundle")
    if bk is not None:
        rep.eq("r12.descriptors.bundle_sha256_key", bv,
               want_hashes.get("prereg-bundle.sha256"))
    exp_counts = arm_order_counts(pids1)
    match = None
    for v in [x for _k2, x in _walk(d) if isinstance(x, dict)]:
        norm = _norm_counts(v)
        if norm is not None:
            match = norm
            break
    rep.ok("r12.descriptors.arm_order_counts", match == exp_counts,
           f"realized arm/position counts {match!r} != §2.1 rotation {exp_counts!r}")
    cb = [s for s in sv if "DENSE" in s and any(t in s.lower() for t in ("even", "odd", "parity"))]
    rep.ok("r12.descriptors.f2_counterbalance", bool(cb),
           "no string field states the family-2 parity counterbalance (DENSE first on even pids)")
    _k, njobs = _get_key(d, "n_jobs")
    rep.eq("r12.descriptors.n_jobs", njobs, census_expected(n1, n2)["jobs"])
    for key, name in (("machinery_sha256", "probe_r12.py"),
                      ("runner_sha256", "run_r12.py"),
                      ("predictor_sha256", "predict_r12.py"),
                      ("prereg_bundle_sha256", "prereg-bundle.sha256")):
        f = os.path.join(dir_path, name)
        want = file_sha256(f) if os.path.isfile(f) else None
        rep.eq(f"r12.descriptors.sha_key.{key}", d.get(key), want)
    if match is not None:
        rep.eq("r12.descriptors.arm_order_counts_sum",
               [sum(match[a]) for a in sorted(match)], [n1] * len(F1_ARMS))
    lk, lv = _get_key(d, "lineage")
    rep.ok("r12.descriptors.probe_lineage", isinstance(lv, str) and bool(lv.strip()),
           f"probe lineage string missing/empty: {lv!r}")
    if ordering_path and os.path.isfile(ordering_path):
        m = re.search(r"^run-script-hash\s+\S+\s+([0-9a-f]{64})\s+probe_r12\.py", read_text(ordering_path), re.M)
        rep.eq("r12.descriptors.machinery_sha256_vs_ordering",
               mach, m.group(1) if m else None)


def _check_descriptors_end(recs, rep):
    """§8 mid-run-drift mitigation: descriptors_end must re-read the same unit.

    Pinned by L1: exactly one `descriptors_end`, the LAST record in the file,
    with the same model id and the same `server.pid` as the start record, and
    `n_records` equal to the file's line count minus 1.
    """
    end = [r for r in recs if r.get("cell") == "descriptors_end"]
    if len(end) != 1:
        rep.ok("r12.descriptors.end_present", False,
               f"{len(end)} descriptors_end records (plan §4 pins exactly 1)")
        return
    e = end[0]
    rep.ok("r12.descriptors.end_present", True, "")
    d = next((r for r in recs if r.get("cell") == "descriptors"), None)
    ids_e = _model_ids(e.get("models_json")) if e.get("models_json") is not None else []
    ids_d = _model_ids(d.get("models_json")) if (d and d.get("models_json") is not None) else []
    rep.ok("r12.descriptors.end_models_json", bool(ids_e),
           "descriptors_end carries no models_json model id")
    rep.ok("r12.descriptors.end_models_match", bool(ids_e) and ids_e == ids_d,
           f"mid-run drift: descriptors ids {ids_d} vs descriptors_end ids {ids_e}")
    _k, srv = _get_key(e, "server", "argv", "pid")
    _k2, note = _get_key(e, "error", "note", "failure", "unavailable")
    rep.ok("r12.descriptors.end_server_info", srv is not None or note is not None,
           "descriptors_end carries neither a server/argv re-read nor a recorded failure note")
    rep.ok("r12.descriptors.end_request_ts", bool(e.get("request_ts")),
           "descriptors_end carries no request_ts")
    rep.ok("r12.descriptors.end_is_last", recs[-1] is e,
           f"descriptors_end is not the last record (index "
           f"{recs.index(e)} of {len(recs) - 1})")
    n_rec = e.get("n_records")
    rep.eq("r12.descriptors.end_n_records", n_rec, len(recs) - 1)
    _k1, srv_d = _get_key(d or {}, "server")
    _k2, srv_e = _get_key(e, "server")
    pid_d = srv_d.get("pid") if isinstance(srv_d, dict) else None
    pid_e = srv_e.get("pid") if isinstance(srv_e, dict) else None
    rep.eq("r12.descriptors.end_server_pid", pid_e, pid_d)


# ---------- round-12 run.log ----------
def _check_summary(recs, runlog_text, rep, truth1, truth2, n1, n2, pids1, pids2):
    stored = parse_runlog_summary(runlog_text)
    rep.eq("r12.runlog.cell_set", sorted(stored), sorted(GRADED_CELLS))
    truth_of = {c: (truth1, F1_CHECKPOINTS[c]) for c in F1_ARMS}
    truth_of.update({c: (truth2, F2_CHECKPOINTS[c]) for c in F2_ARMS})
    for cell in GRADED_CELLS:
        truth, _turns = truth_of[cell]
        rows = [r for r in recs
                if r.get("cell") == cell and r.get("turn") == FINAL_TURN[cell]]
        passes = 0
        for r in rows:
            want = _want_for(cell, r["pid"], r["turn"], truth)
            if want is None:
                continue
            got = extract_json_block(r.get("raw", ""))
            ok_re = (grade_state(got, want) if cell in F1_ARMS else grade_seq(got, want))[0]
            passes += 1 if ok_re else 0
        rep.eq(f"r12.runlog.{cell}", stored.get(cell), (passes, len(rows)))
    m = re.search(r"^wall_total_s:\s*([\d.]+)\s*$", runlog_text, re.M)
    rep.ok("r12.runlog.wall_total_s", m is not None and float(m.group(1)) > 0,
           f"wall_total_s line {'missing' if not m else m.group(1)!r} (must be present and > 0)")
    exp = census_expected(n1, n2)
    jobs = re.findall(r"^\[(\d+)/(\d+)\] \('([^']+)', (\d+)\)$", runlog_text, re.M)
    rep.eq("r12.runlog.jobs", len(jobs), exp["jobs"])
    rep.ok("r12.runlog.jobs_denominator",
           bool(jobs) and all(int(j[1]) == exp["jobs"] for j in jobs),
           f"progress denominators {sorted({j[1] for j in jobs})} != {exp['jobs']}")
    rep.ok("r12.runlog.job_cells", all(j[2] in GRADED_CELLS for j in jobs),
           f"unknown job cells: {sorted({j[2] for j in jobs} - set(GRADED_CELLS))}")
    f1, f2 = {}, {}
    for _num, _den, cell, pid in jobs:
        (f1 if cell in F1_ARMS else f2).setdefault(int(pid), []).append(cell)
    bad1 = [p for p in sorted(f1) if f1[p] != arm_order(p)]
    rep.ok("r12.runlog.arm_order_f1", not bad1,
           f"{len(bad1)} pids deviate from the §2.1 rotation: {bad1[:3]}")
    bad2 = [p for p in sorted(f2) if f2[p] != f2_order(p)]
    rep.ok("r12.runlog.arm_order_f2", not bad2,
           f"{len(bad2)} pids deviate from the §2.2 parity counterbalance: {bad2[:3]}")
    rep.ok("r12.runlog.job_pids_known",
           set(f1) <= set(pids1) and set(f2) <= set(pids2),
           f"unknown pids: {sorted((set(f1) - set(pids1)) | (set(f2) - set(pids2)))[:4]}")
    if (n1, n2) == (R12_N_PIDS_1, R12_N_PIDS_2):
        rep.eq("r12.runlog.section4_jobs", len(jobs), SECTION4_TOTALS[2])


_PROB_KEYS = ("p", "prob", "probability", "p_pass", "phat")
_SIGN_KEYS = ("p_diffpos", "p", "prob", "probability")


def _load_probs(path, keys=_PROB_KEYS, group_keys=("cell", "arm"),
                pid_keys=("pid", "problem")):
    """Parse a per-event probability file -> ({(group,pid): p}, problems, notes).

    Handles the pinned round-12 JSONL schema (`predictions-r12-perproblem.jsonl`:
    arm/pid/p_pass; `predictions-r12-signevents.jsonl`: contrast/pid/p_diffpos)
    and a markdown table with group/pid/p columns.
    """
    if path is None or not os.path.isfile(path):
        return None, [f"missing probability file {path}"], []
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
    except OSError as e:
        return None, [f"unreadable: {e}"], []
    out, problems, notes = {}, [], []
    if path.endswith(".jsonl") or path.endswith(".json"):
        objs = []
        for i, line in enumerate(txt.splitlines(), 1):
            if not line.strip():
                continue
            try:
                objs.append(json.loads(line))
            except json.JSONDecodeError as e:
                return None, [f"{path}:{i}: invalid JSON: {e}"], []
        if len(objs) == 1 and isinstance(objs[0], dict) and "events" in objs[0]:
            objs = objs[0]["events"]
        for o in objs:
            if not isinstance(o, dict):
                problems.append(f"non-object entry {o!r}")
                continue
            g = next((o[k] for k in group_keys if k in o), None)
            pid = next((o[k] for k in pid_keys if k in o), None)
            p = next((o[k] for k in keys if k in o), None)
            if g is None or pid is None or p is None:
                problems.append(f"entry lacks group/pid/p: {json.dumps(o)[:80]}")
                continue
            try:
                out[(str(g), int(pid))] = float(p)
            except (TypeError, ValueError):
                problems.append(f"unparseable p/pid: {json.dumps(o)[:80]}")
        if not out and not problems:
            notes.append(f"{os.path.basename(path)}: no records")
        return out, problems, notes
    lines = txt.splitlines()
    hdr = None
    for i, line in enumerate(lines):
        low = line.lower()
        if (line.strip().startswith("|") and "pid" in low
                and any(k in low for k in ("cell", "arm", "contrast"))
                and re.search(r"\bp\b|prob", low)):
            hdr = i
            break
    if hdr is None:
        return None, ["no probability table header with pid + group + p columns"], []
    cols = [c.strip().lower() for c in lines[hdr].strip().strip("|").split("|")]
    gi = next((j for j, c in enumerate(cols)
               if c in ("cell", "arm", "contrast")), None)
    pi = next((j for j, c in enumerate(cols) if c in ("pid", "problem")), None)
    pp = next((j for j, c in enumerate(cols)
               if c in ("p", "prob", "probability", "p_pass", "p_diffpos")), None)
    if gi is None or pi is None or pp is None:
        return None, [f"table header {cols} lacks group/pid/p columns"], []
    for line in lines[hdr + 1:]:
        s = line.strip()
        if not s.startswith("|") or re.fullmatch(r"\|[-:| ]+\|", s):
            continue
        cells_row = [c.strip() for c in s.strip("|").split("|")]
        if len(cells_row) <= max(gi, pi, pp):
            continue
        try:
            out[(cells_row[gi], int(cells_row[pi]))] = float(cells_row[pp])
        except ValueError:
            problems.append(f"unparseable row {s[:80]}")
    return out, problems, notes


def _resolve_prob_sources(bundle_path, dir_path):
    """Locate the FILED probability files among the PRE-HASHED bundle members.

    Returns ((pass_src, sign_src), notes) where each src is
    (basename, path, bundle_digest, probs) or None. A file is classified by its
    event key space: arm/pid records are the pass-event source, contrast/pid
    records the sign-event source; other bundled files are reported as notes.
    """
    if not bundle_path or not os.path.isfile(bundle_path):
        return (None, None), [f"missing prereg bundle: {bundle_path}"]
    notes = []
    hits_pass, hits_sign = [], []
    for line in read_text(bundle_path).splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 2:
            notes.append(f"unparseable bundle line {line!r}")
            continue
        digest, rel = parts[0], parts[1]
        base = os.path.basename(rel)
        full = os.path.join(dir_path, base)
        if not os.path.isfile(full):
            notes.append(f"{base}: bundled but missing from {dir_path}")
            continue
        probs, problems, _n = _load_probs(full)
        if probs and len(probs) >= 2:
            hits_pass.append((base, full, digest, probs))
            continue
        sprobs, sproblems, _sn = _load_probs(full, keys=_SIGN_KEYS,
                                            group_keys=("contrast", "cell", "arm"))
        if sprobs and len(sprobs) >= 2:
            hits_sign.append((base, full, digest, sprobs))
            continue
        notes.append(f"{base}: not a probability table "
                     f"({(problems or sproblems or ['no records'])[0]})")
    if len(hits_pass) != 1:
        notes.append(f"{len(hits_pass)} bundled pass-event probability files: "
                     f"{[h[0] for h in hits_pass]}")
        hits_pass = []
    if len(hits_sign) != 1:
        notes.append(f"{len(hits_sign)} bundled sign-event probability files: "
                     f"{[h[0] for h in hits_sign]}")
        hits_sign = []
    return ((hits_pass[0] if hits_pass else None),
            (hits_sign[0] if hits_sign else None)), notes


def _read_runlevel_probs(pred_text):
    """RL1-RL7 probabilities from the `predictions-r12.md` §5 table.

    Row shape: `| RL1 | <event text> | 0.55 | <justification> |` — the
    probability is the first cell that is a bare float.
    """
    out = {}
    if not pred_text:
        return out
    for line in pred_text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells_row = [c.strip() for c in s.strip("|").split("|")]
        if not cells_row or cells_row[0] not in RL_IDS:
            continue
        for c in cells_row[1:]:
            if re.fullmatch(r"\d+(?:\.\d+)?", c):
                out[cells_row[0]] = float(c)
                break
    return out


def _check_prob_sources(rep, sources, notes, R, pred_text, pids1, pids2):
    """Probability-file provenance, sha pins, coverage and scoring-source rules.

    The scored Brier/BSS is recomputed FROM THESE COMMITTED PROBABILITIES and
    the observed outcomes — never from re-derived probabilities.
    """
    pass_src, sign_src = sources
    rep.ok("r12.pred.probs_source_unique", pass_src is not None,
           f"no unique pre-hashed pass-event probability file: {notes}")
    rep.ok("r12.pred.sign_prob_source_unique", sign_src is not None,
           f"no unique pre-hashed sign-event probability file: {notes}")
    if pass_src:
        base, path, digest, probs = pass_src
        rep.eq("r12.pred.probs_sha256", digest,
               file_sha256(path) if os.path.isfile(path) else None)
        expected = sorted([(c, p) for c in F1_ARMS for p in pids1]
                          + [(c, p) for c in F2_ARMS for p in pids2])
        rep.eq("r12.pred.probs_event_set", sorted(probs), expected)
        rep.ok("r12.pred.probs_range",
               all(0.0 <= v <= 1.0 for v in probs.values()),
               f"{sum(1 for v in probs.values() if not 0.0 <= v <= 1.0)} out of [0,1]")
        f2_const = all(len({probs.get((c, p)) for p in pids2}) == 1 for c in F2_ARMS)
        rep.ok("r12.pred.probs_f2_constant", f2_const,
               "family-2 probabilities are not constant per arm (§8 comparator)")
        rep.ok("r12.pred.scoring_source", R["e6"]["probs_sha256"] == digest,
               f"scored Brier was not built from the committed pass file {base}")
        m = re.search(r"perproblem[^\n]*sha256\s*`?([0-9a-f]{64})", pred_text or "")
        rep.eq("r12.pred.probs_sha256_stated", m.group(1) if m else None,
               file_sha256(path) if os.path.isfile(path) else None)
    if sign_src:
        base, path, digest, probs = sign_src
        rep.eq("r12.pred.sign_probs_sha256", digest,
               file_sha256(path) if os.path.isfile(path) else None)
        expected = sorted([(cid, p) for cid, ca, _cb, _t in SIGN_CONTRASTS
                           for p in (pids1 if ca in F1_ARMS else pids2)])
        rep.eq("r12.pred.sign_probs_event_set", sorted(probs), expected)
        rep.ok("r12.pred.sign_probs_range",
               all(0.0 <= v <= 1.0 for v in probs.values()),
               f"{sum(1 for v in probs.values() if not 0.0 <= v <= 1.0)} out of [0,1]")
        rep.ok("r12.pred.sign_scoring_source", R["e6"]["sign_digest"] == digest,
               f"scored sign Brier was not built from the committed file {base}")
        m = re.search(r"signevents[^\n]*sha256\s*`?([0-9a-f]{64})", pred_text or "")
        rep.eq("r12.pred.sign_probs_sha256_stated", m.group(1) if m else None,
               file_sha256(path) if os.path.isfile(path) else None)
    rep.eq("r12.pred.scored_unmapped",
           [f"pass:{k}" for k in R["e6"]["pass"]["unmapped"]]
           + [f"sign:{k}" for k in R["e6"]["sign"]["unmapped"]]
           + [f"run:{k}" for k in R["e6"]["runlevel"]["unmapped"]], [])


# ---------- round-12 analysis recomputation (analysis_r12.md §5) ----------
def _nw_maps(recs, truth1, truth2):
    """{cell: {pid: {turn: nwrong}}} and {cell: {pid: {turn: ok}}} from raws."""
    nw = {c: {} for c in GRADED_CELLS}
    okk = {c: {} for c in GRADED_CELLS}
    for r in recs:
        cell = r.get("cell", "")
        if cell not in GRADED_CELLS or "ok" not in r:
            continue
        pid, turn = r.get("pid"), r.get("turn")
        want = _want_for(cell, pid, turn, truth1 if cell in F1_ARMS else truth2)
        if want is None:
            continue
        got = extract_json_block(r.get("raw", ""))
        ok_re, nw_re = (grade_state(got, want) if cell in F1_ARMS else grade_seq(got, want))
        nw[cell].setdefault(pid, {})[turn] = nw_re
        okk[cell].setdefault(pid, {})[turn] = ok_re
    return nw, okk


def _error_pids(recs, pids1, pids2):
    """Listwise deletion: an error record removes its pid from its family."""
    e1, e2 = set(), set()
    for r in recs:
        if r.get("cell") != "error":
            continue
        pid = r.get("pid")
        if pid is None:
            job = r.get("job")
            nums = re.findall(r"\d+", job if isinstance(job, str) else json.dumps(job))
            pid = int(nums[-1]) if nums else None
        if pid is None:
            continue
        if pid in pids1:
            e1.add(pid)
        elif pid in pids2:
            e2.add(pid)
    return sorted(e1), sorted(e2)


def r11_e2_point(md_path):
    """The r11 observed paired diff, read from the committed r11 analysis."""
    if not md_path or not os.path.isfile(md_path):
        return None
    m = re.search(_R12_STORED["r11_diff"], read_text(md_path), re.M)
    return _num(m.group(1)) if m else None


def r12_verdicts(R, min_n1=MIN_N_FAMILY_1, min_n2=MIN_N_FAMILY_2):
    """Apply the amended plan §2.3 rules R1-R5 verbatim.

    Returns ({R1..R5}, underpowered). The override fires when a family's
    listwise-deleted n OR its paired contrast n falls below the filed floor
    (both floors 44); the paired-n clause is the recompute engine's reading of
    "family-1 n < 44 or family-2 n < 44" — recorded in r12-grader-notes.md.
    """
    n1e, n2e = R["n_eff"]
    under = (n1e < min_n1 or n2e < min_n2
             or R["e2"]["n"] < min_n1 or R["e5"]["n"] < min_n2)
    if under:
        return {k: "UNDERPOWERED-INDETERMINATE" for k in
                ("R1", "R2", "R3", "R4", "R5")}, True
    pg = R["page"]
    e3 = R["e3"]
    if pg["p"] < 0.05 and pg["direction"] == "increasing":
        r1 = "LADDER ESTABLISHED"
    elif pg["p"] >= 0.05 and all(g[2] > 0 for g in e3):
        r1 = "LADDER DIRECTIONAL"
    else:
        r1 = "LADDER NOT SUPPORTED"
    e2 = R["e2"]
    if e2["diff"] > 0 and e2["p"] < 0.05 and e2["wins"] > e2["losses"]:
        r2 = "REPEATS-r11"
    elif e2["diff"] > 0 and e2["p"] < 0.05:
        r2 = "REPEATS-DOWNGRADED"      # neutral sign (wins == losses) is DISAGREEMENT
    elif e2["diff"] > 0:
        r2 = "DIRECTIONAL"
    else:
        r2 = "DOES-NOT-REPEAT"
    e4 = R["e4"]
    if e4["diff"] > 0 and e4["p"] < 0.05:
        r3 = "DISSOCIATION ESTABLISHED"
    elif e4["diff"] > 0:
        r3 = "DISSOCIATION DIRECTIONAL"
    else:
        r3 = "DISSOCIATION FALSIFIED"
    e5 = R["e5"]
    if e5["diff"] > 0 and e5["p"] < 0.05:
        r4 = "TRANSPORTS"
    elif e5["diff"] > 0:
        r4 = "TRANSPORT DIRECTIONAL"
    else:
        r4 = "TRANSPORT NOT SUPPORTED"
    bss = R["e6"]["pass"]["bss"]
    slope = (R["e6"]["calib_pass"] or {}).get("slope")
    if bss is None or slope is None:
        r5 = "FORECAST UNSKILLED"
    elif bss > 0 and 0.5 <= slope <= 2.0:
        r5 = "FORECAST SKILLED"
    elif bss > 0:
        r5 = "FORECAST SKILLED-MISCALIBRATED"
    else:
        r5 = "FORECAST UNSKILLED"
    return {"R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5}, False


def _recompute_r12(recs, truth1, truth2, pids1, pids2, err_pids, probs,
                   probs_digest, min_n1=MIN_N_FAMILY_1, min_n2=MIN_N_FAMILY_2,
                   r11_point=None, md_path=None, probs_sign=None,
                   sign_digest=None, probs_run=None):
    """Every §5 quantity, re-derived from committed bytes (never from stored fields).

    `probs`/`probs_sign`/`probs_run` are the FILED probabilities (416 pass
    events, 304 sign events, 7 run-level events); scoring never re-derives a
    probability. `err_pids` is the listwise-deletion pair (family 1, family 2).
    """
    nw, okk = _nw_maps(recs, truth1, truth2)
    e1_pids, e2_pids = err_pids
    eff1 = [p for p in pids1 if p not in set(e1_pids)]
    eff2 = [p for p in pids2 if p not in set(e2_pids)]
    R = {"n_eff": (len(eff1), len(eff2)), "excluded": {"family1": list(e1_pids),
                                                      "family2": list(e2_pids)}}
    arms = {}
    for cell in GRADED_CELLS:
        pids = eff1 if cell in F1_ARMS else eff2
        turns = F1_CHECKPOINTS[cell] if cell in F1_ARMS else F2_CHECKPOINTS[cell]
        ft = FINAL_TURN[cell]
        have = [p for p in sorted(pids) if ft in okk[cell].get(p, {})]
        passes = sum(1 for p in have if okk[cell][p][ft])
        mean_final = _mean([nw[cell][p][ft] for p in have])
        allnw = [nw[cell][p][t] for p in sorted(pids) for t in turns
                 if t in nw[cell].get(p, {})]
        arms[cell] = (passes, len(have), mean_final, _mean(allnw))
    R["arms"] = arms
    blocks, page_missing = [], []
    for pid in sorted(eff1):
        try:
            blocks.append([nw[c][pid][FINAL_TURN[c]] for c in LADDER_ARMS])
        except KeyError:
            page_missing.append(pid)
    R["page_missing"] = page_missing
    R["page"] = page_l_trend(blocks)
    R["page_n"] = len(blocks)
    # E2 is (sparser - denser) = A-CKPT710 - A-CKPT4710 at the shared turns
    e2_pairs = _paired_pairs_turns(nw, "A-CKPT710", (7, 10), "A-CKPT4710", (7, 10), eff1)
    d2 = [a - b for _p, a, b in e2_pairs]
    R["e2"] = paired_stats(d2) if d2 else {"n": 0, "diff": 0.0, "sd": 0.0, "t": 0.0,
                                           "p": 1.0, "ci_lo": 0.0, "ci_hi": 0.0,
                                           "wins": 0, "losses": 0, "ties": 0}
    R["e2"]["missing"] = [p for p in eff1 if p not in {x[0] for x in e2_pairs}]
    fin = {c: {p: okk[c][p].get(FINAL_TURN[c]) for p in sorted(eff1)
               if FINAL_TURN[c] in okk[c].get(p, {})} for c in ("A-CKPT4710", "A-CKPT710")}
    b, cc, p_mc = mcnemar_pairs(fin["A-CKPT4710"], fin["A-CKPT710"])
    R["e2"]["mcnemar"] = (b, cc, p_mc)
    R["sign_direction"] = ("+1" if R["e2"]["wins"] > R["e2"]["losses"]
                           else ("-1" if R["e2"]["wins"] < R["e2"]["losses"] else "NEUTRAL"))
    e3 = []
    for label, ca, cb, turns in (("4710-INC", "A-CKPT4710", "A-INC", (4, 7, 10)),
                                 ("710-4710", "A-CKPT710", "A-CKPT4710", (7, 10)),
                                 ("10-710", "A-CKPT10", "A-CKPT710", (10,))):
        pairs = _paired_pairs_turns(nw, ca, turns, cb, turns, eff1)
        dd = [a - b for _p, a, b in pairs]
        st = paired_stats(dd) if dd else {"diff": 0.0, "p": 1.0, "n": 0, "sd": 0.0,
                                          "t": 0.0, "ci_lo": 0.0, "ci_hi": 0.0,
                                          "wins": 0, "losses": 0, "ties": 0}
        e3.append((label, turns, st["diff"], st["p"], st))
    R["e3"] = e3
    e4_pairs = sign_event_pairs(nw, "E4", MONO_CELL, "A-CKPT10", None, eff1)
    d4 = [a - b for _p, a, b in e4_pairs]
    R["e4"] = paired_stats(d4) if d4 else {"n": 0, "diff": 0.0, "sd": 0.0, "t": 0.0,
                                           "p": 1.0, "wins": 0, "losses": 0, "ties": 0,
                                           "ci_lo": 0.0, "ci_hi": 0.0}
    R["e4"]["missing"] = [p for p in eff1 if p not in {x[0] for x in e4_pairs}]
    e5_pairs = _paired_pairs_turns(nw, "T-SPARSE", (7, 10), "T-DENSE", (7, 10), eff2)
    d5 = [a - b for _p, a, b in e5_pairs]
    R["e5"] = paired_stats(d5) if d5 else {"n": 0, "diff": 0.0, "sd": 0.0, "t": 0.0,
                                           "p": 1.0, "wins": 0, "losses": 0, "ties": 0,
                                           "ci_lo": 0.0, "ci_hi": 0.0}
    R["e5"]["missing"] = [p for p in eff2 if p not in {x[0] for x in e5_pairs}]
    # ---- E6 (1) pass events ----
    pass_events = []
    for cell in GRADED_CELLS:
        pids = eff1 if cell in F1_ARMS else eff2
        for pid in sorted(pids):
            t = FINAL_TURN[cell]
            if t in okk[cell].get(pid, {}):
                pass_events.append(((cell, pid), 1 if okk[cell][pid][t] else 0))
    pass_set = _score_set(pass_events, probs, lambda k: k[0])
    rel_keys = pass_set["keys"]
    rel_probs = {k: p for k, p in zip(pass_set["keys"], pass_set["ps"])}
    rel_out = {k: y for k, y in zip(pass_set["keys"], pass_set["ys"])}
    calib_pass = (logistic_calibration(pass_set["ps"], pass_set["ys"])
                  if pass_set["ps"] else None)
    R["e6"] = {"pass": pass_set, "events_pass": len(pass_events),
               "probs_sha256": probs_digest, "sign_digest": sign_digest,
               "reliability": reliability_bins(rel_keys, rel_probs, rel_out),
               "calib_pass": calib_pass,
               "missing_probs": [k for k in pass_set["unmapped"]]}
    # ---- E6 (2) sign events ----
    sign_events = []
    for cid, ca, cb, turns in SIGN_CONTRASTS:
        pids = eff1 if ca in F1_ARMS else eff2
        for pid, a, bb in sign_event_pairs(nw, cid, ca, cb, turns, pids):
            sign_events.append(((cid, pid), 1 if (a - bb) > 0 else 0))
    R["e6"]["sign"] = _score_set(sign_events, probs_sign, lambda k: k[0])
    R["e6"]["events_sign"] = len(sign_events)
    # ---- verdicts (needed for the run-level outcomes) ----
    R["r11_point"] = r11_point
    R["r2_point_clause"] = (r11_point is not None
                            and abs(R["e2"]["diff"] - r11_point) <= R2_POINT_TOL)
    R["verdicts"], R["underpowered"] = r12_verdicts(R, min_n1, min_n2)
    # ---- E6 (3) run-level events (RL1-RL7; outcomes from the reported verdicts) ----
    vtext = R["verdicts"]
    rl_out = {
        "RL1": 1 if vtext["R1"] == "LADDER ESTABLISHED" else 0,
        "RL2": 1 if vtext["R2"].startswith("REPEATS-r11") else 0,
        "RL3": 1 if R["r2_point_clause"] else 0,
        "RL4": 1 if all(g[2] > 0 for g in R["e3"]) else 0,
        "RL5": 1 if vtext["R3"] == "DISSOCIATION ESTABLISHED" else 0,
        "RL6": 1 if vtext["R4"] == "TRANSPORTS" else 0,
        "RL7": 1 if vtext["R5"] == "FORECAST SKILLED" else 0,
    }
    R["e6"]["rl_outcomes"] = rl_out
    R["e6"]["runlevel"] = _score_set([(rid, rl_out[rid]) for rid in RL_IDS],
                                     probs_run, lambda k: "RL")
    # per-event Brier for the run-level set = that single event's squared error
    R["e6"]["runlevel"]["per_event"] = {
        rid: ((probs_run or {}).get(rid) - rl_out[rid]) ** 2
        for rid in RL_IDS if (probs_run or {}).get(rid) is not None}
    R["e6"]["events_runlevel"] = len(RL_IDS)
    # ---- pooled aggregates ----
    all_ps = pass_set["ps"] + R["e6"]["sign"]["ps"] + R["e6"]["runlevel"]["ps"]
    all_ys = pass_set["ys"] + R["e6"]["sign"]["ys"] + R["e6"]["runlevel"]["ys"]
    all_clim = pass_set["clim"] + R["e6"]["sign"]["clim"] + R["e6"]["runlevel"]["clim"]
    R["e6"]["all"] = {"n": len(all_ps),
                      "brier": _mean([(p - y) ** 2 for p, y in zip(all_ps, all_ys)])
                      if all_ps else None,
                      "bss": _bss(all_ps, all_ys, all_clim)}
    R["e6"]["calib_all"] = (logistic_calibration(all_ps, all_ys) if all_ps else None)
    R["e6"]["total_events"] = (len(pass_events) + len(sign_events) + len(RL_IDS))
    R["e6"]["splits"] = {}
    for name, spl_arms in BSS_SPLITS:
        idx = [k for k, g in enumerate(pass_set["groups"]) if g in spl_arms]
        R["e6"]["splits"][name] = (
            {"n": len(idx), "bss": _bss([pass_set["ps"][k] for k in idx],
                                        [pass_set["ys"][k] for k in idx],
                                        [pass_set["clim"][k] for k in idx])}
            if idx else {"n": 0, "bss": None})
    # ---- degenerate-input flags (D9) ----
    R["degenerate"] = {"page": R["page"]["var_L"] == 0.0}
    for name, st in (("E2", R["e2"]), ("E4", R["e4"]), ("E5", R["e5"])):
        R["degenerate"][name] = st.get("sd") == 0.0
    for label, _t, _d, _p, st in R["e3"]:
        R["degenerate"]["E3 " + label] = st.get("sd") == 0.0
    # ---- realized arm positions from the JSONL file order (post-deletion) ----
    first_idx = {}
    for i, r in enumerate(recs):
        c, pid = r.get("cell"), r.get("pid")
        if c in F1_ARMS and pid is not None and (pid, c) not in first_idx:
            first_idx[(pid, c)] = i
    pos_mat = {a: [0] * 5 for a in F1_ARMS}
    for pid in eff1:
        have = [(first_idx[(pid, c)], c) for c in F1_ARMS if (pid, c) in first_idx]
        for pos, (_i, c) in enumerate(sorted(have), 1):
            pos_mat[c][pos - 1] += 1
    R["realized_positions"] = pos_mat
    graded = [r for r in recs if r.get("cell") in GRADED_CELLS and "ok" in r]
    R["finish"] = (sum(1 for r in graded if r.get("finish") == "length"),
                   sum(1 for r in graded if extract_json_block(r.get("raw", "")) is None),
                   len(graded))
    ack = {}
    for cell in ACK_CELLS:
        rows = [r for r in recs if r.get("cell") == cell]
        okc = sum(1 for r in rows if str(r.get("raw", "")).strip().lower().startswith("ok"))
        ack[cell] = (okc, len(rows), (100.0 * okc / len(rows)) if rows else 0.0)
    R["ack"] = ack
    return R


# ---------- analysis_r12.md line checks ----------
def _grab12(rep, key, text, pattern=None):
    m = re.search(pattern or _R12_STORED[key], text, re.M)
    if m is None:
        rep.ok(f"r12.analysis.{key}.present", False, f"stored line not found: {key}")
    return m


def _safe_num(s):
    try:
        return _num(s)
    except (ValueError, AttributeError, TypeError):
        return None


def _close(s, value, tol):
    v = _safe_num(s)
    if v is None or value is None:
        return False
    return abs(v - value) <= tol + 1e-12


def _close_na(s, value):
    """`n/a` matches exactly when the recomputation is undefined (None)."""
    if value is None:
        return s.strip() == "n/a"
    return _close_dp(s, value)


def _verdict_line(rep, cid, line, branch, clause_expected, clause_text="POINT-MATCHES-r11"):
    """Stored verdict line == branch text, with the R2 clause iff expected."""
    s = (line or "").strip()
    if not s.startswith(branch):
        rep.ok(cid, False, f"stored verdict {s!r} does not start with {branch!r}")
        return
    rest = s[len(branch):]
    has_clause = clause_text in rest
    residue = rest.replace(clause_text, "").replace("additionally", "")
    residue = residue.strip(" \t\u2014\u2013-(),;:.")
    rep.ok(cid, residue == "" and has_clause == clause_expected,
           f"stored verdict {s!r}: trailing text {residue!r}, clause present "
           f"{has_clause} (expected {clause_expected})")


def _pred_lookup(pred_text, kind, arms):
    """First filed prediction for a scoring-table row (label-driven)."""
    if not pred_text:
        return None
    lines = [l.strip() for l in pred_text.splitlines()]
    for line in lines:
        low = line.lower()
        if kind == "final_passes":
            if arms and arms[0].lower() in low:
                m = re.search(r"(\d+)/(\d+)", line)
                if m:
                    return ("frac", int(m.group(1)), int(m.group(2)))
        elif kind == "paired_diff":
            if all(a.lower() in low for a in arms) and ("diff" in low or "severity" in low):
                m = re.search(_SIGNS + r"\d+\.\d+", line)
                if m:
                    return ("num", _num(m.group(0)))
        elif kind == "page_L":
            if "page" in low or "trend" in low:
                m = re.search(_SIGNS + r"\d+\.\d+", line)
                if m:
                    return ("num", _num(m.group(0)))
        else:
            token = {"brier": "brier", "bss": "bss", "slope": "slope",
                     "intercept": "intercept"}.get(kind)
            if token and token in low:
                m = re.search(_SIGNS + r"\d+\.\d+", line)
                if m:
                    return ("num", _num(m.group(0)))
    return None


def _identify_score_row(label):
    lab = label.upper()
    arms = [a for a in GRADED_CELLS if a.upper() in lab]
    if len(arms) >= 2 and ("DIFF" in lab or "GAP" in lab):
        return "paired_diff", arms
    if len(arms) == 1 and ("FINAL" in lab or "PASS" in lab):
        return "final_passes", arms
    if "PAGE" in lab or "TREND" in lab:
        return "page_L", []
    low = label.lower()
    if "brier" in low and "bss" not in low:
        return "brier", []
    if "bss" in low or "skill" in low:
        return "bss", []
    if "slope" in low:
        return "slope", []
    if "intercept" in low:
        return "intercept", []
    return None, []


def _paired_pair_value(R, arms):
    if set(arms) >= {"A-CKPT710", "A-CKPT4710"} and len(arms) == 2:
        return R["e2"]["diff"]
    for label, _turns, diff, _p, _st in R["e3"]:
        toks = label.split("-")
        if len(toks) == 2 and {toks[0], toks[1]} <= {a.replace("A-CKPT", "").replace("A-", "")
                                                    for a in arms}:
            return diff
    return None


def _check_analysis(R, ctx, rep, pred_text):
    """Compare every analysis_r12.md §5 line with the recomputed quantity."""
    md = ctx["md"]
    # ---- census sentence ----
    m = _grab12(rep, "counts", md)
    if m:
        # amended §5 counts BOTH descriptor records ("2 descriptors"); the
        # numbers must also account for the pinned 4 114-record total
        # (1+1+64+48+1328+2256+416). r12-grader-notes.md flags that a producer
        # counting only the start record prints 1 and cannot sum to 4114.
        comp = (sum(1 for r in ctx["recs"] if r.get("cell") in
                    ("descriptors", "descriptors_end")),
                sum(1 for r in ctx["recs"] if r.get("cell") == "meta"),
                sum(1 for r in ctx["recs"] if r.get("cell") == "meta2"),
                sum(1 for r in ctx["recs"] if r.get("cell") in GRADED_CELLS and "ok" in r),
                sum(1 for r in ctx["recs"] if r.get("cell") in ACK_CELLS),
                sum(1 for r in ctx["recs"] if r.get("cell") == "filler"),
                sum(1 for r in ctx["recs"] if r.get("cell") == "error"))
        for i, name in enumerate(("descriptors", "meta", "meta2", "graded", "ack",
                                  "fillers", "errors")):
            rep.eq(f"r12.analysis.counts.{name}", int(m.group(i + 1)), comp[i])
    # ---- arm table ----
    seen_arm_rows = []
    for mm in re.finditer(_R12_STORED["arm_row"], md, re.M):
        cell = mm.group(1)
        seen_arm_rows.append(cell)
        passes, n, mean_final, mean_all = R["arms"][cell]
        rep.eq(f"r12.analysis.arm.{cell}.passes", int(mm.group(2)), passes)
        rep.eq(f"r12.analysis.arm.{cell}.n", int(mm.group(3)), n)
        rep.ok(f"r12.analysis.arm.{cell}.mean_final", _close(mm.group(4), mean_final, 5e-4),
               f"stored {mm.group(4)!r} vs recomputed {mean_final:.6f}")
        rep.ok(f"r12.analysis.arm.{cell}.mean_shared", _close(mm.group(5), mean_all, 5e-4),
               f"stored {mm.group(5)!r} vs recomputed {mean_all:.6f}")
    rep.eq("r12.analysis.arm.row_set", sorted(seen_arm_rows), sorted(GRADED_CELLS))
    # ---- E1 Page ----
    m = _grab12(rep, "page", md)
    if m:
        pg = R["page"]
        rep.ok("r12.analysis.e1.L", _close_dp(m.group(1), pg["L"]),
               f"stored {m.group(1)!r} vs recomputed {pg['L']!r}")
        rep.ok("r12.analysis.e1.E_L", _close_dp(m.group(2), pg["E_L"]),
               f"stored {m.group(2)!r} vs recomputed {pg['E_L']!r}")
        rep.ok("r12.analysis.e1.var_L", _close_dp(m.group(3), pg["var_L"]),
               f"stored {m.group(3)!r} vs recomputed {pg['var_L']!r}")
        rep.ok("r12.analysis.e1.z", _close_dp(m.group(4), pg["z"]),
               f"stored {m.group(4)!r} vs recomputed {pg['z']!r}")
        rep.ok("r12.analysis.e1.p", _close_dp(m.group(5), pg["p"]),
               f"stored {m.group(5)!r} vs recomputed {pg['p']!r}")
        rep.eq("r12.analysis.e1.direction", m.group(6), pg["direction"])
    rep.eq("r12.analysis.e1.pids_missing", R["page_missing"], [])
    rep.eq("r12.analysis.e1.n_blocks", R["page_n"], R["n_eff"][0])
    # ---- E2 ----
    e2 = R["e2"]
    m = _grab12(rep, "e2_diff", md)
    if m:
        rep.ok("r12.analysis.e2.diff", _close(m.group(1), e2["diff"], 5e-4),
               f"stored {m.group(1)!r} vs recomputed {e2['diff']:.6f}")
        rep.ok("r12.analysis.e2.sd", _close(m.group(2), e2["sd"], 5e-4),
               f"stored {m.group(2)!r} vs recomputed {e2['sd']:.6f}")
        rep.eq("r12.analysis.e2.n", int(m.group(3)), e2["n"])
    rep.eq("r12.analysis.e2.pids_missing", e2["missing"], [])
    m = _grab12(rep, "e2_t", md)
    if m:
        rep.ok("r12.analysis.e2.t", _close(m.group(1), e2["t"], 5e-4),
               f"stored {m.group(1)!r} vs recomputed {e2['t']:.6f}")
        rep.eq("r12.analysis.e2.df", int(m.group(2)), max(e2["n"] - 1, 0))
        rep.ok("r12.analysis.e2.p", _close(m.group(3), e2["p"], 5e-5),
               f"stored {m.group(3)!r} vs recomputed {e2['p']:.6f}")
    m = _grab12(rep, "e2_ci", md)
    if m:
        rep.ok("r12.analysis.e2.ci_lo", _close(m.group(1), e2["ci_lo"], 5e-4),
               f"stored {m.group(1)!r} vs recomputed {e2['ci_lo']:.6f}")
        rep.ok("r12.analysis.e2.ci_hi", _close(m.group(2), e2["ci_hi"], 5e-4),
               f"stored {m.group(2)!r} vs recomputed {e2['ci_hi']:.6f}")
    m = _grab12(rep, "e2_sign", md)
    if m:
        rep.eq("r12.analysis.e2.sign_wins", int(m.group(1)), e2["wins"])
        rep.eq("r12.analysis.e2.sign_losses", int(m.group(2)), e2["losses"])
        rep.eq("r12.analysis.e2.sign_ties", int(m.group(3)), e2["ties"])
        rep.ok("r12.analysis.e2.sign_p",
               _close(m.group(4), exact_sign_p(e2["wins"], e2["losses"]), 5e-5),
               f"stored {m.group(4)!r}")
        rep.eq("r12.analysis.e2.sign_direction", m.group(5), R["sign_direction"])
    m = _grab12(rep, "e2_mcnemar", md)
    if m:
        rep.eq("r12.analysis.e2.mcnemar_b", int(m.group(1)), e2["mcnemar"][0])
        rep.eq("r12.analysis.e2.mcnemar_c", int(m.group(2)), e2["mcnemar"][1])
        rep.ok("r12.analysis.e2.mcnemar_p", _close(m.group(3), e2["mcnemar"][2], 5e-5),
               f"stored {m.group(3)!r} vs recomputed {e2['mcnemar'][2]:.6f}")
    # ---- E3 adjacent gaps ----
    m = _grab12(rep, "e3", md)
    if m:
        for i, (label, _turns, diff, p, _st) in enumerate(R["e3"]):
            rep.ok(f"r12.analysis.e3.g{i + 1}.diff", _close(m.group(1 + 2 * i), diff, 5e-4),
                   f"{label}: stored {m.group(1 + 2 * i)!r} vs recomputed {diff:.6f}")
            rep.ok(f"r12.analysis.e3.g{i + 1}.p", _close(m.group(2 + 2 * i), p, 5e-5),
                   f"{label}: stored {m.group(2 + 2 * i)!r} vs recomputed {p:.6f}")
    # ---- E4 / E5 ----
    for key, stat in (("e4", R["e4"]), ("e5", R["e5"])):
        m = _grab12(rep, key, md)
        if not m:
            continue
        rep.ok(f"r12.analysis.{key}.diff", _close(m.group(1), stat["diff"], 5e-4),
               f"stored {m.group(1)!r} vs recomputed {stat['diff']:.6f}")
        rep.ok(f"r12.analysis.{key}.sd", _close(m.group(2), stat["sd"], 5e-4),
               f"stored {m.group(2)!r} vs recomputed {stat['sd']:.6f}")
        rep.eq(f"r12.analysis.{key}.n", int(m.group(3)), stat["n"])
        rep.ok(f"r12.analysis.{key}.t", _close(m.group(4), stat["t"], 5e-4),
               f"stored {m.group(4)!r} vs recomputed {stat['t']:.6f}")
        rep.ok(f"r12.analysis.{key}.p", _close(m.group(5), stat["p"], 5e-5),
               f"stored {m.group(5)!r} vs recomputed {stat['p']:.6f}")
        rep.eq(f"r12.analysis.{key}.sign", (int(m.group(6)), int(m.group(7)), int(m.group(8))),
               (stat["wins"], stat["losses"], stat["ties"]))
        rep.eq(f"r12.analysis.{key}.pids_missing", stat.get("missing", []), [])
        rep.eq(f"r12.analysis.{key}.n_panel", stat["n"] + len(stat.get("missing", [])),
               R["n_eff"][0 if key == "e4" else 1])
    # ---- E6: three scored event sets (amended §2.3/§5) ----
    e6 = R["e6"]
    pset, sset, rset, aset = e6["pass"], e6["sign"], e6["runlevel"], e6["all"]
    rep.eq("r12.analysis.e6.unmapped_events",
           ([f"pass:{k}" for k in pset["unmapped"]]
            + [f"sign:{k}" for k in sset["unmapped"]]
            + [f"run:{k}" for k in rset["unmapped"]]), [])
    # event counts: scored pass/sign/run-level + the scored total (727 at full n)
    m = _grab12(rep, "e6_events", md) or _grab12(
        rep, "e6_events_alt", md, _R12_STORED["e6_events_alt"])
    if m:
        rep.eq("r12.analysis.e6.counts_pass", int(m.group(1)), pset["n"])
        rep.eq("r12.analysis.e6.counts_sign", int(m.group(2)), sset["n"])
        rep.eq("r12.analysis.e6.counts_runlevel", int(m.group(3)), rset["n"])
        rep.eq("r12.analysis.e6.counts_total", int(m.group(4)), aset["n"])
    if (R["n_eff"][0], R["n_eff"][1]) == (E6_EVENTS_EXPECTED["n1"], E6_EVENTS_EXPECTED["n2"]):
        rep.eq("r12.analysis.e6.counts_design",
               (pset["n"], sset["n"], rset["n"], aset["n"]),
               (E6_EVENTS_EXPECTED["events"], E6_EVENTS_EXPECTED["sign"],
                E6_EVENTS_EXPECTED["runlevel"], E6_EVENTS_EXPECTED["total"]))
    # pass-event Brier: pooled + N + per-arm
    m = _grab12(rep, "e6_brier", md)
    if m:
        rep.ok("r12.analysis.e6.brier_pass_pooled", _close_na(m.group(1), pset["brier"]),
               f"stored {m.group(1)!r} vs recomputed {pset['brier']!r}")
        rep.eq("r12.analysis.e6.brier_pass_n", int(m.group(2)), pset["n"])
        pairs_stored = dict(re.findall(r"([A-Za-z0-9\-]+)=(" + _NUMF + r")", m.group(3)))
        rep.eq("r12.analysis.e6.brier_arm_set", sorted(pairs_stored), sorted(GRADED_CELLS))
        for cell in sorted(pairs_stored):
            rep.ok(f"r12.analysis.e6.brier.{cell}",
                   _close_dp(pairs_stored[cell], pset["per_group"].get(cell)),
                   f"stored {pairs_stored[cell]!r} vs recomputed "
                   f"{pset['per_group'].get(cell)!r}")
    # sign-event Brier: pooled + N + per-contrast
    m = _grab12(rep, "e6_brier_sign", md) or _grab12(
        rep, "e6_brier_sign_alt", md, _R12_STORED["e6_brier_sign_alt"])
    if m:
        rep.ok("r12.analysis.e6.brier_sign_pooled", _close_na(m.group(1), sset["brier"]),
               f"stored {m.group(1)!r} vs recomputed {sset['brier']!r}")
        rep.eq("r12.analysis.e6.brier_sign_n", int(m.group(2)), sset["n"])
        pairs_stored = dict(re.findall(r"([A-Za-z0-9\-]+)=(" + _NUMF + r")", m.group(3)))
        rep.eq("r12.analysis.e6.brier_contrast_set", sorted(pairs_stored),
               sorted(cid for cid, _a, _b, _t in SIGN_CONTRASTS))
        for cid in sorted(pairs_stored):
            rep.ok(f"r12.analysis.e6.brier_sign.{cid}",
                   _close_dp(pairs_stored[cid], sset["per_group"].get(cid)),
                   f"stored {pairs_stored[cid]!r} vs recomputed "
                   f"{sset['per_group'].get(cid)!r}")
    # run-level Brier: pooled + N=7 + per-event
    m = _grab12(rep, "e6_brier_runlevel", md) or _grab12(
        rep, "e6_brier_runlevel_alt", md, _R12_STORED["e6_brier_runlevel_alt"])
    if m:
        rep.ok("r12.analysis.e6.brier_runlevel_pooled", _close_na(m.group(1), rset["brier"]),
               f"stored {m.group(1)!r} vs recomputed {rset['brier']!r}")
        rep.eq("r12.analysis.e6.brier_runlevel_n", int(m.group(2)), rset["n"])
        per_event = {k: v for k, v in re.findall(r"(RL[1-7])=(" + _NUMF + r")", md)}
        if per_event:
            rep.eq("r12.analysis.e6.brier_runlevel_set", sorted(per_event), sorted(RL_IDS))
            for rid in sorted(per_event):
                rep.ok(f"r12.analysis.e6.brier_runlevel.{rid}",
                       _close_dp(per_event[rid], rset["per_event"].get(rid)),
                       f"stored {per_event[rid]!r} vs recomputed "
                       f"{rset['per_event'].get(rid)!r}")
    # pooled over all scored events
    m = _grab12(rep, "e6_brier_all", md)
    if m:
        rep.ok("r12.analysis.e6.brier_all_pooled", _close_na(m.group(1), aset["brier"]),
               f"stored {m.group(1)!r} vs recomputed {aset['brier']!r}")
        rep.eq("r12.analysis.e6.brier_all_n", int(m.group(2)), aset["n"])
    # BSS: pooled pass + the three splits, and sign/runlevel/all
    m = _grab12(rep, "e6_bss", md)
    if m:
        rep.ok("r12.analysis.e6.bss_pass_pooled", _close_na(m.group(1), pset["bss"]),
               f"stored {m.group(1)!r} vs recomputed {pset['bss']!r}")
    for name, _arms in BSS_SPLITS:
        m = re.search(re.escape(name) + r"(?:-arms)?=(n/a|" + _SIGNS + _NUMF + r")", md)
        if m:
            rep.ok(f"r12.analysis.e6.bss_split.{name}",
                   _close_na(m.group(1), e6["splits"][name]["bss"]),
                   f"stored {m.group(1)!r} vs recomputed {e6['splits'][name]['bss']!r}")
        else:
            rep.ok(f"r12.analysis.e6.bss_split.{name}.present", False,
                   f"no stored BSS split for {name}")
    m = (_grab12(rep, "e6_bss_groups", md)
         or _grab12(rep, "e6_bss_groups_alt", md, _R12_STORED["e6_bss_groups_alt"]))
    if m:
        # the sibling rendering carries `pass=` first; the plan's §5 line does not
        off = 1 if len(m.groups()) == 4 else 0
        if off:
            rep.ok("r12.analysis.e6.bss_pass_redundant",
                   _close_na(m.group(1), pset["bss"]),
                   f"stored {m.group(1)!r} vs recomputed {pset['bss']!r}")
        rep.ok("r12.analysis.e6.bss_sign", _close_na(m.group(1 + off), sset["bss"]),
               f"stored {m.group(1 + off)!r} vs recomputed {sset['bss']!r}")
        rep.ok("r12.analysis.e6.bss_runlevel", _close_na(m.group(2 + off), rset["bss"]),
               f"stored {m.group(2 + off)!r} vs recomputed {rset['bss']!r}")
        rep.ok("r12.analysis.e6.bss_pooled_all", _close_na(m.group(3 + off), aset["bss"]),
               f"stored {m.group(3 + off)!r} vs recomputed {aset['bss']!r}")
    # calibration: primary (pass events) + secondary (all scored events)
    m = _grab12(rep, "e6_cal", md)
    if m:
        cp = R["e6"]["calib_pass"] or {}
        rep.ok("r12.analysis.e6.cal_slope", _close_dp(m.group(1), cp.get("slope")),
               f"stored {m.group(1)!r} vs recomputed {cp.get('slope')!r}")
        rep.ok("r12.analysis.e6.cal_intercept", _close_dp(m.group(2), cp.get("intercept")),
               f"stored {m.group(2)!r} vs recomputed {cp.get('intercept')!r}")
        rep.eq("r12.analysis.e6.cal_n", int(m.group(3)), cp.get("n"))
        rep.ok("r12.analysis.e6.cal_stationary",
               cp.get("grad_norm") is not None and cp["grad_norm"] < 0.05,
               f"|grad| at the fitted point = {(cp.get('grad_norm') or float('nan')):.4f}")
    m = _grab12(rep, "e6_cal_all", md)
    if m:
        ca = R["e6"]["calib_all"] or {}
        rep.ok("r12.analysis.e6.cal_all_slope", _close_dp(m.group(1), ca.get("slope")),
               f"stored {m.group(1)!r} vs recomputed {ca.get('slope')!r}")
        rep.ok("r12.analysis.e6.cal_all_intercept", _close_dp(m.group(2), ca.get("intercept")),
               f"stored {m.group(2)!r} vs recomputed {ca.get('intercept')!r}")
        rep.eq("r12.analysis.e6.cal_all_n", int(m.group(3)), ca.get("n"))
    # reliability over the pass events (empty bins print n/a)
    rel = re.findall(_R12_STORED["e6_rel"], md, re.M)
    rep.eq("r12.analysis.e6.reliability_bins", len(rel), len(REL_EDGES) - 1)
    if len(rel) == len(REL_EDGES) - 1:
        for i, (lo_s, hi_s, pred_s, obs_s, n_s) in enumerate(rel):
            lo, hi, pred, obs, cnt = R["e6"]["reliability"][i]
            rep.ok(f"r12.analysis.e6.reliability.{i}.edges",
                   _close_dp(lo_s, lo) and _close_dp(hi_s, hi),
                   f"bin {i} edges {lo_s}-{hi_s} != {lo}-{hi} (pinned {REL_EDGES})")
            rep.eq(f"r12.analysis.e6.reliability.{i}.n", int(n_s), cnt)
            if cnt == 0:
                rep.ok(f"r12.analysis.e6.reliability.{i}.empty_is_na",
                       pred_s.strip() == "n/a" and obs_s.strip() == "n/a",
                       f"empty bin {i} stored pred={pred_s!r} obs={obs_s!r} (D8: n/a)")
            else:
                rep.ok(f"r12.analysis.e6.reliability.{i}.pred", _close_dp(pred_s, pred),
                       f"stored {pred_s!r} vs recomputed {pred!r}")
                rep.ok(f"r12.analysis.e6.reliability.{i}.obs", _close_dp(obs_s, obs),
                       f"stored {obs_s!r} vs recomputed {obs!r}")
    # ---- finish audit ----
    m = _grab12(rep, "finish", md)
    if m:
        length, parse, total = R["finish"]
        rep.eq("r12.analysis.finish.length", (int(m.group(1)), int(m.group(2))), (length, total))
        rep.eq("r12.analysis.finish.parse_fail", (int(m.group(3)), int(m.group(4))), (parse, total))
    # ---- ack compliance ----
    seen_ack = {}
    for mm in re.finditer(_R12_STORED["ack"], md, re.M):
        seen_ack.setdefault(mm.group(1) + "-ack", mm)
    rep.eq("r12.analysis.ack.cell_set", sorted(seen_ack), sorted(ACK_CELLS))
    for cell, mm in sorted(seen_ack.items()):
        if cell not in R["ack"]:
            rep.ok(f"r12.analysis.ack.{cell}.known", False, f"unknown ack cell {cell}")
            continue
        okc, n, pct = R["ack"][cell]
        rep.eq(f"r12.analysis.ack.{cell}.count", (int(mm.group(2)), int(mm.group(3))), (okc, n))
        rep.ok(f"r12.analysis.ack.{cell}.pct", _close(mm.group(4), pct, 5e-2),
               f"stored {mm.group(4)!r} vs recomputed {pct:.4f}")
    # ---- excluded pids ----
    m = _grab12(rep, "excluded", md)
    if m:
        for i, key in enumerate(("family1", "family2")):
            stored = [int(x) for x in re.findall(r"\d+", m.group(i + 1))]
            rep.eq(f"r12.analysis.excluded.{key}", stored, R["excluded"][key])
    # ---- verdict lines ----
    r2_clause = R["r2_point_clause"] if not R["underpowered"] else R["r2_point_clause"]
    for k in ("R1", "R2", "R3", "R4", "R5"):
        m = _grab12(rep, "verdict_" + k.lower(), md)
        if not m:
            continue
        _verdict_line(rep, f"r12.analysis.verdict_{k.lower()}", m.group(1),
                      R["verdicts"][k], r2_clause if k == "R2" else False)
    rep.ok("r12.analysis.verdict_r2.r11_reference", R["r11_point"] is not None,
           "r11's committed observed paired diff could not be read (R2 point clause)")
    rep.ok("r12.analysis.verdicts_override_consistent",
           R["underpowered"] == any(str(v).startswith("UNDERPOWERED-INDETERMINATE")
                                    for v in R["verdicts"].values()
                                    if isinstance(v, str)),
           f"override flag {R['underpowered']} (n_eff={R['n_eff']}) inconsistent with "
           f"the verdict texts")
    # ---- realized arm positions after listwise deletion (amended §5) ----
    m = re.search(r"Realized arm positions?[^\n]*", md)
    if m:
        stored = _parse_realized_positions(m.group(0))
        rep.ok("r12.analysis.realized_positions", stored == R["realized_positions"],
               f"stored {stored!r} vs recomputed {R['realized_positions']!r}")
    else:
        rep.ok("r12.analysis.realized_positions.present", False,
               "no 'Realized arm position' line in analysis_r12.md")
    # ---- degenerate-input notes (D9): present iff a convention fired ----
    deg = [k for k, v in sorted(R["degenerate"].items()) if v]
    notes = re.findall(r"NOTE degenerate:[^\n]*", md)
    rep.ok("r12.analysis.degenerate_note_present", bool(notes) == bool(deg),
           f"{len(notes)} NOTE degenerate lines for {len(deg)} degenerate inputs "
           f"({deg})")
    for token in ("var_L", "zero-variance"):
        if any(("var_L" in k) or ("zero-variance" in token) for k in deg) and token == "var_L" \
                and R["degenerate"].get("page"):
            rep.ok("r12.analysis.degenerate_note_page",
                   any("var_L" in n or "Page" in n for n in notes),
                   f"var_L == 0 but no NOTE line mentions the Page/variance case: {notes}")
            break

    # ---- ordering + descriptor sentences ----
    aim = ctx.get("analysis_inputs") or {}
    need = []
    for d in aim.get("bundle_digests", []):
        need.append(d)
    need += [t for t in (aim.get("pre_hash"), aim.get("post_hash"), aim.get("first_request_ts"))
             if t]
    missing_toks = [t for t in need if t not in md]
    rep.ok("r12.analysis.ordering_sentence", not missing_toks,
           f"analysis_r12.md is missing ordering-proof tokens: {missing_toks}")
    miss_d = [t for t in DESCRIPTOR_SENTENCE_TOKENS if t.lower() not in md.lower()]
    rep.ok("r12.analysis.descriptor_sentence", not miss_d,
           f"analysis_r12.md is missing §1 descriptor tokens: {miss_d}")
    # ---- point-prediction scoring table ----
    mh = _grab12(rep, "score_header", md)
    if not mh:
        return
    rows = []
    for line in md[mh.end():].splitlines():
        s = line.strip()
        if not s or re.fullmatch(r"\|[-:| ]+\|", s):
            continue
        mm = re.match(_R12_STORED["score_row"], s)
        if not mm:
            break
        rows.append(tuple(mm.group(i).strip() for i in (1, 2, 3, 4)))
    rep.ok("r12.analysis.score.row_count", len(rows) >= len(GRADED_CELLS),
           f"{len(rows)} scoring-table rows for {len(GRADED_CELLS)} arms")
    arm_rows = []
    for label, _p, _o, _e in rows:
        kind, arms = _identify_score_row(label)
        if kind == "final_passes":
            arm_rows.append(arms[0])
    rep.eq("r12.analysis.score.arm_rows", sorted(arm_rows), sorted(GRADED_CELLS))
    for i, (label, pred_s, obs_s, err_s) in enumerate(rows):
        kind, arms = _identify_score_row(label)
        rep.ok(f"r12.analysis.score.row{i}.identifiable", kind is not None,
               f"row {i} label {label!r} matches no re-derivable quantity")
        if kind is None:
            continue
        if kind == "final_passes":
            passes, n = R["arms"][arms[0]][0], R["arms"][arms[0]][1]
            obs_val = passes / n if n else 0.0
            obs_frac = (passes, n)
        elif kind == "paired_diff":
            obs_val = _paired_pair_value(R, arms)
            obs_frac = None
        elif kind == "page_L":
            obs_val, obs_frac = R["page"]["L"], None
        elif kind == "brier":
            obs_val, obs_frac = e6.get("brier_pooled"), None
        elif kind == "bss":
            obs_val, obs_frac = e6.get("bss"), None
        elif kind == "slope":
            obs_val, obs_frac = e6.get("slope"), None
        else:
            obs_val, obs_frac = e6.get("intercept"), None
        if obs_val is None:
            rep.ok(f"r12.analysis.score.row{i}.observed", False,
                   f"row {i} ({label!r}) has no recomputed value")
            continue
        if obs_frac is not None:
            mfrac = re.match(r"^(\d+)/(\d+)$", obs_s.replace(" ", ""))
            ok_obs = (mfrac is not None
                      and (int(mfrac.group(1)), int(mfrac.group(2))) == obs_frac) \
                or (mfrac is None and _close(obs_s, obs_val, 5e-4))
        else:
            ok_obs = _close(obs_s, obs_val, 5e-4)
        rep.ok(f"r12.analysis.score.row{i}.observed", ok_obs,
               f"row {i} ({label!r}) stored {obs_s!r} vs recomputed {obs_val!r}")
        pred = _pred_lookup(pred_text, kind, arms)
        if pred is None:
            rep.ok(f"r12.analysis.score.row{i}.predicted_prereg", False,
                   f"row {i} ({label!r}) prediction not found in predictions-r12.md")
        elif pred[0] == "frac":
            mfrac = re.match(r"^(\d+)/(\d+)$", pred_s.replace(" ", ""))
            rep.ok(f"r12.analysis.score.row{i}.predicted_prereg",
                   mfrac is not None
                   and (int(mfrac.group(1)), int(mfrac.group(2))) == (pred[1], pred[2]),
                   f"row {i} predicted {pred_s!r} != prereg {pred[1]}/{pred[2]}")
            frac_err = abs(pred[1] / pred[2] - obs_val)
            count_err = abs(pred[1] - obs_frac[0]) if obs_frac else None
            rep.ok(f"r12.analysis.score.row{i}.abs_error",
                   _close(err_s, frac_err, 5e-4)
                   or (count_err is not None and _close(err_s, count_err, 5e-4)),
                   f"row {i} abs error {err_s!r} vs |{pred[1]}/{pred[2]} - {obs_val!r}|"
                   f" ({frac_err:.6f})")
        else:
            rep.ok(f"r12.analysis.score.row{i}.predicted_prereg",
                   _close(pred_s, pred[1], 5e-4),
                   f"row {i} predicted {pred_s!r} != prereg {pred[1]!r}")
            rep.ok(f"r12.analysis.score.row{i}.abs_error",
                   _close(err_s, abs(pred[1] - obs_val), 5e-4),
                   f"row {i} abs error {err_s!r} vs {abs(pred[1] - obs_val):.6f}")


# ---------- round-12 ordering + pins ----------
_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def check_r12_ordering(rep, jsonl_path=None, sha_path=None, ordering_path=None,
                       dir_path=None, script_files=None, bundle_required=None,
                       recs=None, repo_root=None):
    """Preregistration discipline: bundle hashes + the ordering chain.

    r11 anti-pattern 15: `request_ts` has 1 s resolution and the run issues
    several requests per second, so every comparison here is `<=` (or `>=`)
    between Z-timestamp strings — never a strictly-greater sub-second test.
    `repo_root` defaults to the repository root; the fixture passes its tmp tree.
    """
    root = REPO_ROOT if repo_root is None else repo_root
    sha_path = sha_path or R12_SHA
    ordering_path = ordering_path or R12_ORDERING
    dir_path = dir_path or R12_DIR
    jsonl_path = jsonl_path or R12_JSONL
    script_files = tuple(R12_SCRIPT_HASH_REQUIRED if script_files is None
                         else script_files)
    required = tuple(R12_REQUIRED_BUNDLE if bundle_required is None else bundle_required)
    lines = [l for l in read_text(sha_path).splitlines() if l.strip()]
    rep.ok("r12.ordering.sha_line_count", len(lines) >= len(required),
           f"{len(lines)} bundle lines for {len(required)} required members")
    seen = {}
    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            rep.ok("r12.ordering.sha_line_parse", False, f"unparseable sha line: {line!r}")
            continue
        digest, rel = parts[0], parts[1]
        base = os.path.basename(rel)
        rep.ok(f"r12.ordering.sha_repo_relative.{base}",
               (not os.path.isabs(rel)
                and rel.startswith("corpus/evidence/round12-ladder/")),
               f"sha line path {rel!r} is not repo-relative under round12-ladder/")
        full = rel if os.path.isabs(rel) else os.path.join(root, rel)
        if not os.path.isfile(full):
            rep.ok(f"r12.ordering.sha_file_present.{base}", False, f"missing bundle file {rel}")
            continue
        rep.eq(f"r12.ordering.sha256.{base}", digest, file_sha256(full))
        seen[base] = True
    rep.ok("r12.ordering.sha_required_present", set(required) <= set(seen),
           f"bundle missing required members: {sorted(set(required) - set(seen))}")
    ord_text = read_text(ordering_path)
    pre = re.search(r"^pre-hash\s+(\S+)\s*$", ord_text, re.M)
    post = re.search(r"^post-hash\s+(\S+)\s*$", ord_text, re.M)
    scripts = re.findall(r"^run-script-hash\s+(\S+)\s+([0-9a-f]{64})\s+([^\s(]+)"
                         r"(?:\s+\([^)]*\))?\s*$", ord_text, re.M)
    rep.ok("r12.ordering.pre_hash_present", pre is not None, "ordering.log has no 'pre-hash' line")
    rep.ok("r12.ordering.post_hash_present", post is not None, "ordering.log has no 'post-hash' line")
    stamps = ([pre.group(1)] if pre else []) + ([post.group(1)] if post else []) \
        + [s[0] for s in scripts]
    rep.ok("r12.ordering.hash_ts_format", bool(stamps) and all(_TS_RE.match(t) for t in stamps),
           f"non-Z timestamps in ordering.log: {[t for t in stamps if not _TS_RE.match(t)]}")
    if pre and post:
        rep.ok("r12.ordering.pre_le_post", pre.group(1) <= post.group(1),
               f"pre-hash {pre.group(1)} > post-hash {post.group(1)}")
    names = [s[2] for s in scripts]
    rep.ok("r12.ordering.script_hash_lines",
           set(script_files) <= set(names) and len(names) >= len(script_files),
           f"run-script-hash lines cover {sorted(set(names))}, need {sorted(script_files)}")
    for _ts, digest, name in scripts:
        if name not in script_files:
            continue
        p = os.path.join(dir_path, name)
        if not os.path.isfile(p):
            rep.ok(f"r12.ordering.script_hash_file_present.{name}", False, f"missing {p}")
        else:
            rep.eq(f"r12.ordering.script_hash_matches_file.{name}", digest, file_sha256(p))
    script_ts = sorted(s[0] for s in scripts)
    if post and script_ts:
        rep.ok("r12.ordering.post_le_script_hash", post.group(1) <= script_ts[0],
               f"post-hash {post.group(1)} > first run-script-hash {script_ts[0]}")
    recs = load_jsonl(jsonl_path) if recs is None else recs
    stamped = [r for r in recs if r.get("request_ts")]
    rep.ok("r12.ordering.requests_present", bool(stamped), "no records carry request_ts")
    if not stamped:
        return
    first_ts = min(r["request_ts"] for r in stamped)
    rep.ok("r12.ordering.hash_precedes_first_request", max(stamps) <= first_ts,
           f"last hash-line time {max(stamps)} > first request_ts {first_ts}")
    if script_ts:
        rep.ok("r12.ordering.script_hash_le_first_request", script_ts[-1] <= first_ts,
               f"last run-script-hash {script_ts[-1]} > first request_ts {first_ts}")
    rep.ok("r12.ordering.first_request_is_descriptors",
           stamped[0].get("cell") == "descriptors" and stamped[0]["request_ts"] == first_ts,
           f"first stamped record in file order: {stamped[0].get('cell')} @ "
           f"{stamped[0]['request_ts']}; min request_ts {first_ts}")


def check_r12_pins(paths, rep, pins=None, defaults=None):
    """Landed-byte pins (md5/sha256 of the committed artifacts), r11 convention."""
    pins = R12_PINS if pins is None else pins
    defaults = defaults or {}
    for key in sorted(pins):
        algo, expected = pins[key]
        p = paths.get(key)
        if p is None or not os.path.isfile(p):
            rep.ok(f"pin.{key}.path", False, f"no readable path for pin key {key}: {p}")
            continue
        if defaults.get(key) and os.path.abspath(p) != os.path.abspath(defaults[key]):
            print(f"[pin] {key}: SKIPPED (overridden path, treated as mutated copy)")
            continue
        rep.eq(f"pin.{key}.{algo}", expected, _hash_file(algo, p))


# ---------- round-12 entry point ----------
def _analysis_inputs(bundle_path, ordering_path, recs):
    """Tokens the analysis' ordering sentence must carry (plan §5)."""
    out = {"bundle_digests": [], "pre_hash": None, "post_hash": None,
           "first_request_ts": None}
    if bundle_path and os.path.isfile(bundle_path):
        out["bundle_digests"] = [l.split()[0] for l in read_text(bundle_path).splitlines()
                                 if l.strip() and len(l.split()) >= 2]
    if ordering_path and os.path.isfile(ordering_path):
        t = read_text(ordering_path)
        m = re.search(r"^pre-hash\s+(\S+)\s*$", t, re.M)
        out["pre_hash"] = m.group(1) if m else None
        m = re.search(r"^post-hash\s+(\S+)\s*$", t, re.M)
        out["post_hash"] = m.group(1) if m else None
    stamped = [r["request_ts"] for r in recs if r.get("request_ts")]
    out["first_request_ts"] = min(stamped) if stamped else None
    return out


def grade_r12(recs, md_text, runlog_text, rep, pids1=None, pids2=None,
              machinery_path=None, r11_jsonl=None, r11_md=None, pred_path=None,
              bundle_path=None, ordering_path=None, dir_path=None,
              min_n1=None, min_n2=None):
    """Re-derive every stored round-12 number from committed bytes.

    `pids1`/`pids2` default to the preregistered n=64 / n=48; the fixture passes
    smaller pid sets (census/total checks then follow `census_expected`). The
    three filed probability sources (416 pass events, 304 sign events, 7
    run-level events) are located among the PRE-HASHED bundle members: the
    scored Brier/BSS is always computed from those committed bytes.
    """
    pids1 = list(R12_PIDS_1 if pids1 is None else pids1)
    pids2 = list(R12_PIDS_2 if pids2 is None else pids2)
    n1, n2 = len(pids1), len(pids2)
    machinery_path = machinery_path or R12_MACHINERY
    dir_path = dir_path or R12_DIR
    bundle_path = bundle_path or R12_SHA
    ordering_path = ordering_path or R12_ORDERING
    pred_path = pred_path or R12_PRED
    min_n1 = MIN_N_FAMILY_1 if min_n1 is None else min_n1
    min_n2 = MIN_N_FAMILY_2 if min_n2 is None else min_n2

    truth1 = _check_meta_f1(recs, rep, pids1, r11_jsonl or R11_JSONL)
    truth2 = _check_meta_f2(recs, rep, pids2, machinery_path)
    _check_replay(recs, rep, truth1, truth2)
    _check_census(recs, rep, n1, n2)
    _check_descriptors(recs, rep, n1, n2, pids1, pids2, machinery_path,
                       bundle_path, ordering_path)
    _check_descriptors_end(recs, rep)
    _check_summary(recs, runlog_text, rep, truth1, truth2, n1, n2, pids1, pids2)

    pred_text = None
    if os.path.isfile(pred_path):
        pred_text = read_text(pred_path)
    else:
        rep.ok("r12.pred.pred_file_present", False, f"missing predictions file {pred_path}")
    sources, notes = _resolve_prob_sources(bundle_path, dir_path)
    pass_src, sign_src = sources
    run_probs = _read_runlevel_probs(pred_text) or {}
    rep.eq("r12.pred.run_probs_present", sorted(run_probs), sorted(RL_IDS))
    r11_point = r11_e2_point(r11_md or R11_MD)
    err = _error_pids(recs, pids1, pids2)
    R = _recompute_r12(recs, truth1, truth2, pids1, pids2, err,
                       pass_src[3] if pass_src else None,
                       pass_src[2] if pass_src else None, min_n1, min_n2, r11_point,
                       probs_sign=sign_src[3] if sign_src else None,
                       sign_digest=sign_src[2] if sign_src else None,
                       probs_run=run_probs)
    ctx = {"recs": recs, "md": md_text,
           "analysis_inputs": _analysis_inputs(bundle_path, ordering_path, recs)}
    _check_analysis(R, ctx, rep, pred_text)
    _check_prob_sources(rep, sources, notes, R, pred_text, pids1, pids2)
    return R


# ======================= fixture selftest (S7) =======================
# Builds a synthetic round-12 tree (no real run needed), proves the clean tree
# passes every check, then runs a mutation battery: each corruption must be
# killed by the specific check id named in the battery.
FIX1 = [201, 202, 203]
FIX2 = [401, 402, 403]
FIX_PRED_PASSES = {"A-INC": 1, "A-CKPT4710": 1, "A-CKPT710": 2, "A-CKPT10": 2,
                   "A-MONO": 0, "T-DENSE": 1, "T-SPARSE": 1}
FIX_PRED_DIFF = 0.500
FIX_PRED_PAGE_L = 20.0
FIX_RL_P = {"RL1": 0.55, "RL2": 0.70, "RL3": 0.45, "RL4": 0.50,
            "RL5": 0.20, "RL6": 0.45, "RL7": 0.50}


def _fix_sign_p(cid):
    """Per-contrast P(diff > 0) (spread so the sign BSS is defined)."""
    return {"E3a": 0.50, "E3b": 0.41, "E3c": 0.50, "E4": 0.50, "E5": 0.50}[cid]


def selftest_stats_r12():
    """Known-value anchors for the NEW statistics (independent of the fixture)."""
    bad = []
    # Page's L: 3 untied blocks 1..4 -> L=90, E=75, Var=25, z=3, p=0.0026998
    pg = page_l_trend([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])
    for got, want, tol, name in ((pg["L"], 90.0, 1e-9, "page.L"),
                                 (pg["E_L"], 75.0, 1e-9, "page.E_L"),
                                 (pg["var_L"], 25.0, 1e-9, "page.var_L"),
                                 (pg["z"], 3.0, 1e-9, "page.z"),
                                 (pg["p"], 0.002699796, 1e-8, "page.p")):
        if abs(got - want) > tol:
            bad.append(f"{name}={got!r}, want {want} +/- {tol}")
    if pg["direction"] != "increasing":
        bad.append(f"page.direction={pg['direction']!r}, want 'increasing'")
    # tied block [1,1,2,3]: midranks 1.5,1.5,3,4 -> L=29.5, E=25, Var=7.5
    pt = page_l_trend([[1, 1, 2, 3]])
    for got, want, name in ((pt["L"], 29.5, "page.tie.L"), (pt["E_L"], 25.0, "page.tie.E_L"),
                            (pt["var_L"], 7.5, "page.tie.var_L")):
        if abs(got - want) > 1e-9:
            bad.append(f"{name}={got!r}, want {want}")
    # family-2 op semantics, hand-evaluated
    init = ["a", "b", "c"]
    ops = [["APP", "d"], ["INS", 1, "x"], ["DEL", 0], ["SET", 1, "z"],
           ["MOV", 0, 3], ["SWP", 0, 1], ["REV", 1, 3]]
    want_states = [["a", "b", "c", "d"], ["a", "x", "b", "c", "d"], ["x", "b", "c", "d"],
                   ["x", "z", "c", "d"], ["z", "c", "d", "x"], ["c", "z", "d", "x"],
                   ["c", "x", "d", "z"]]
    got_states = seq_states_along(init, ops)
    if got_states != want_states:
        bad.append(f"seq_states_along={got_states!r}, want {want_states!r}")
    for got, want, name in ((grade_seq([1, 2], [1, 2, 3]), (False, 1), "grade_seq.short"),
                            (grade_seq(None, [1, 2, 3]), (False, 3), "grade_seq.none"),
                            (grade_seq([1, 9, 3], [1, 2, 3]), (False, 1), "grade_seq.mismatch"),
                            (grade_seq([1, 2, 3], [1, 2, 3]), (True, 0), "grade_seq.exact")):
        if got != want:
            bad.append(f"{name}={got!r}, want {want!r}")
    # family-2 plan §2.2 invariants (the tree-level check is also unit-anchored,
    # because a *stored* op list can only violate them if the generator did)
    good_ops = [["APP", "d"], ["DEL", 0], ["MOV", 1, 3], ["REV", 0, 2], ["SWP", 0, 1]]
    bad_kinds = [["APP", "d"], ["DEL", 0], ["MOV", 1, 3], ["SWP", 0, 1], ["SWP", 0, 1]]
    bad_tail = [["REV", 0, 1], ["DEL", 3], ["APP", "a"], ["APP", "b"], ["DEL", 1]]
    for ops, want, name in ((good_ops, True, "invariants.good"),
                            (bad_kinds, False, "invariants.missing-kind"),
                            (bad_tail, False, "invariants.short-tail")):
        got = f2_invariants(ops)[0]
        if got != want:
            bad.append(f"f2_invariants({name})={got!r}, want {want!r}")
    if sorted(_tail_positions(bad_tail)) != [1]:
        bad.append(f"_tail_positions(bad_tail)={sorted(_tail_positions(bad_tail))!r}, want [1]")
    # census formulas reproduce the committed smoke evidence (L1: the n=2/n2=2
    # mock smoke produced exactly 142 records and the n=1/n2=1 real smoke 72)
    for (a1, a2, recs_n) in ((2, 2, 142), (1, 1, 72), (64, 48, 4114)):
        exp = census_expected(a1, a2)
        if exp["records"] != recs_n:
            bad.append(f"census_expected({a1},{a2})[records]={exp['records']}, want {recs_n}")
    if census_expected(64, 48)["calls"] != 4002 or census_expected(64, 48)["jobs"] != 416:
        bad.append("census_expected(64,48) calls/jobs != 4002/416")
    # Brier/BSS anchors
    ev = [("T-DENSE", 1), ("T-DENSE", 2)]
    pr = {ev[0]: 0.5, ev[1]: 0.5}
    oc = {ev[0]: 1.0, ev[1]: 0.0}
    bs = brier_scores(ev, pr, oc)
    if abs(bs["pooled"] - 0.25) > 1e-12 or abs(bs["bss"]) > 1e-12:
        bad.append(f"brier constant-0.5 pooled={bs['pooled']!r} bss={bs['bss']!r}, want 0.25/0.0")
    pr2 = {ev[0]: 1.0, ev[1]: 0.0}
    bs2 = brier_scores(ev, pr2, oc)
    if abs(bs2["pooled"]) > 1e-12 or abs(bs2["bss"] - 1.0) > 1e-12:
        bad.append(f"brier perfect pooled={bs2['pooled']!r} bss={bs2['bss']!r}, want 0/1")
    # reliability bins anchor
    ev3 = [("T-DENSE", 1), ("T-DENSE", 2), ("T-DENSE", 3), ("T-DENSE", 4)]
    pr3 = dict(zip(ev3, [0.1, 0.3, 0.7, 0.9]))
    oc3 = dict(zip(ev3, [0.0, 1.0, 1.0, 1.0]))
    rel = reliability_bins(ev3, pr3, oc3)
    want_rel = [(0.1, 0.0, 1), (0.3, 1.0, 1), (0.0, 0.0, 0), (0.7, 1.0, 1), (0.9, 1.0, 1)]
    got_rel = [(round(p, 6), round(o, 6), n) for _lo, _hi, p, o, n in rel]
    if got_rel != want_rel:
        bad.append(f"reliability_bins={got_rel!r}, want {want_rel!r}")
    # logistic calibration: Newton vs an independent profile-likelihood grid
    xs = [-1.6 + 0.04 * i for i in range(80)]
    ys = [1.0 if (i * 7) % 10 < 3 + (1 if i > 40 else 0) else 0.0 for i in range(80)]
    cal = logistic_calibration([_sigmoid(x) for x in xs], ys)
    ga, gb = calibration_gradient([_logit(_sigmoid(x)) for x in xs], ys,
                                  cal["intercept"], cal["slope"])
    if math.hypot(ga, gb) > 1e-6:
        bad.append(f"calibration gradient at the fitted point = {math.hypot(ga, gb):.3e}, want <1e-6")
    ag, bg = _profile_grid_fit([_logit(_sigmoid(x)) for x in xs], ys)
    if abs(ag - cal["intercept"]) > 1e-4 or abs(bg - cal["slope"]) > 1e-4:
        bad.append(f"logistic_fit ({cal['intercept']:.6f},{cal['slope']:.6f}) != profile grid "
                   f"({ag:.6f},{bg:.6f})")
    return bad


def _profile_grid_fit(xs, ys, lo=-3.0, hi=3.0, steps=400):
    """Independent 1-D profile-likelihood maximisation (grid + golden section).

    Used only by the selftest as a cross-check on `logistic_fit`'s Newton path:
    for a fixed slope b the intercept a is chosen by bisection on the gradient
    (the profile likelihood in a is concave), then b is maximised by a coarse
    grid followed by a golden-section refinement.
    """
    def best_a(b):
        a_lo, a_hi = -30.0, 30.0
        for _ in range(120):
            mid = 0.5 * (a_lo + a_hi)
            g, _ = calibration_gradient(xs, ys, mid, b)
            if g > 0:
                a_lo = mid
            else:
                a_hi = mid
        return 0.5 * (a_lo + a_hi)

    def prof(b):
        return _loglik(xs, ys, best_a(b), b)

    best_b, best_ll = None, None
    for i in range(steps + 1):
        b = lo + (hi - lo) * i / steps
        ll = prof(b)
        if best_ll is None or ll > best_ll:
            best_b, best_ll = b, ll
    step = (hi - lo) / steps
    a_, b_ = best_b - step, best_b + step
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = b_ - gr * (b_ - a_), a_ + gr * (b_ - a_)
    fc, fd = prof(c), prof(d)
    for _ in range(200):
        if fc > fd:
            b_, d, fd = d, c, fc
            c = b_ - gr * (b_ - a_)
            fc = prof(c)
        else:
            a_, c, fc = c, d, fd
            d = a_ + gr * (b_ - a_)
            fd = prof(d)
        if abs(b_ - a_) < 1e-12:
            break
    b = 0.5 * (a_ + b_)
    return best_a(b), b


# ---------- fixture: synthetic round-12 tree + mutation battery ----------
SYNTH_PROBE_SRC = '''#!/usr/bin/env python3
"""fixture stand-in for probe_r12.py (synthetic tree only; never committed)."""
import os
import random

TOKENS = ["alpha", "beta", "gamma", "delta", "eps", "zeta", "kappa", "lambda"]
SYSTEM = "fixture system prompt (round-12 synthetic tree)"
N_OPS = 10

# deliberate import-time side effect: the gate's machinery loader must NOT run it
SIDE_EFFECT = open(os.path.join(os.path.dirname(__file__), "IMPORT-SIDE-EFFECT.txt"), "w").write("boom")


def sim_seq_op(state, op):
    s = list(state)
    kind = op[0]
    if kind == "APP":
        s.append(op[1])
    elif kind == "INS":
        s.insert(op[1], op[2])
    elif kind == "DEL":
        del s[op[1]]
    elif kind == "SET":
        s[op[1]] = op[2]
    elif kind == "MOV":
        t = s.pop(op[1])
        s.insert(op[2], t)
    elif kind == "SWP":
        s[op[1]], s[op[2]] = s[op[2]], s[op[1]]
    elif kind == "REV":
        i, j = op[1], op[2]
        s[i:j + 1] = list(reversed(s[i:j + 1]))
    return s


def gen_seq_problem(seed):
    retries = 0
    while True:
        rng = random.Random(seed)
        init = rng.sample(TOKENS, 6)
        state = list(init)
        ops = []
        while len(ops) < N_OPS:
            n = len(state)
            roll = rng.random()
            if roll < 0.15:
                op = ("APP", rng.choice(TOKENS))
            elif roll < 0.30:
                op = ("INS", rng.randrange(0, n + 1), rng.choice(TOKENS))
            elif roll < 0.50:
                op = ("DEL", rng.randrange(0, n))
            elif roll < 0.65:
                op = ("SET", rng.randrange(0, n), rng.choice(TOKENS))
            elif roll < 0.80:
                op = ("MOV", rng.randrange(0, n), rng.randrange(0, max(n - 1, 1)))
            elif roll < 0.90 and n >= 2:
                i = rng.randrange(0, n)
                j = rng.randrange(0, n)
                if i == j:
                    j = (j + 1) % n
                op = ("SWP", i, j)
            elif n >= 2:
                i = rng.randrange(0, n - 1)
                j = rng.randrange(i + 1, n)
                op = ("REV", i, j)
            else:
                op = ("APP", rng.choice(TOKENS))
            state = sim_seq_op(state, op)
            ops.append(op)
        kinds = {o[0] for o in ops}
        pos = set()
        for o in ops[-3:]:
            for operand in o[1:]:
                if isinstance(operand, int):
                    pos.add(operand)
        if {"DEL", "MOV", "REV"} - kinds or len(pos) < 2:
            seed += 977
            retries += 1
            continue
        return init, [list(o) for o in ops], retries
'''
SYNTH_RUN_SRC = "#!/usr/bin/env python3\n# fixture stand-in for run_r12.py (synthetic tree only)\n"
SYNTH_PREDICT_SRC = "#!/usr/bin/env python3\n# fixture stand-in for predict_r12.py (synthetic tree only)\n"


def _fix_ts(i):
    """Fixture request_ts, all AFTER the ordering.log hash + launch times
    (2026-09-29T01:16:08Z / 01:19:59Z) — the ordering chain is `<=`, never >."""
    secs = 20 * 60 + i                      # 01:20:00Z + i seconds
    return "2026-09-29T01:%02d:%02dZ" % (secs // 60, secs % 60)


def _fence(obj):
    return "```json\n" + json.dumps(obj) + "\n```"


def _perturb_dict(want, k):
    got = dict(want)
    for j, key in enumerate(sorted(want)[:k]):
        got[key] = want[key] + 100 + j
    return got


def _perturb_list(want, k):
    got = list(want)
    for j in range(min(k, len(got))):
        got[j] = str(got[j]) + "*"
    return got


# deterministic nwrong patterns: family 1 gives a ladder where the r11-matched
# pair (710 - 4710 over {7,10}) lands at 1/3 = 0.333 (|0.333-0.352| <= 0.15, so
# the R2 POINT-MATCHES-r11 clause is exercised); family 2 gives SPARSE > DENSE.
def _fix_nw1(pid, cell, turn):
    if cell == "A-CKPT4710":
        return 1
    if cell == "A-CKPT710":
        if pid == FIX1[0]:
            return 1
        return 2 if turn == 7 else 1
    base = {"A-INC": 0, "A-CKPT10": 2, "A-MONO": 3}[cell]
    return max(0, base + ((pid + turn) % 3) - 1)


def _fix_nw2(pid, cell, turn):
    base = {"T-DENSE": 1, "T-SPARSE": 3}[cell]
    extra = 0 if cell == "T-DENSE" else (pid % 4)
    return max(0, base + ((pid + turn) % 2) + extra)


def _fix_p1(pid, cell):
    """Family-1 per-problem probability (spread, so the calibration fit is well posed)."""
    return round(0.1 + 0.1 * ((pid + F1_ARMS.index(cell) * 3) % 8), 2)


def _fix_p2(cell):
    return {"T-DENSE": 0.6, "T-SPARSE": 0.4}[cell]


def _fmtp(x, spec):
    """Format a number or the literal n/a (mirrors recompute_r12_draft._fmt)."""
    if x is None:
        return "n/a"
    return format(x, spec)


def _build_r12_fixture(tmp, degenerate=False):
    """Synthetic round-12 tree using the REAL artifact schemas (no run needed).

    `degenerate=True` builds the D9 variant: every ladder arm carries the same
    final-turn severity for every pid, so sd(diffs) == 0 and Var_L == 0 and the
    §2.3 degenerate conventions apply (t=+0.000/p=1.0000, z=+0.000/p=1.0000,
    plus `NOTE degenerate:` lines).
    """
    d = os.path.join(tmp, "corpus/evidence/round12-ladder")
    os.makedirs(d, exist_ok=True)

    def wp(name, text):
        p = os.path.join(d, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        return p

    probe = wp("probe_r12.py", SYNTH_PROBE_SRC)
    wp("run_r12.py", SYNTH_RUN_SRC)
    wp("predict_r12.py", SYNTH_PREDICT_SRC)
    wp("probe_plan_r12.md", "# fixture probe plan (synthetic tree)\n")
    wp("power_analysis_r12.md", "# fixture power analysis (synthetic tree)\n")
    wp("power_r12.py", "# fixture power script\n")
    wp("precheck_r12.py", "# fixture precheck\n")

    recs = []
    nrec = [0]

    def stamp(rec, explicit=None):
        rec = dict(rec)
        rec["request_ts"] = explicit or _fix_ts(nrec[0])
        nrec[0] += 1
        return rec

    truth1 = {}
    for pid in FIX1:
        init, ops, _r = gen_problem(r12_seed1(pid))
        truth = states_along(init, [tuple(o) for o in ops])
        truth1[pid] = truth
        recs.append({"cell": "meta", "pid": pid, "seed": r12_seed1(pid), "init": init,
                     "ops": ops, "truth": truth,
                     "tail_touched": sorted(tail_touched([tuple(o) for o in ops]))})
    ns_probe, _missing = _load_machinery(probe, ["gen_seq_problem", "SYSTEM"])
    gen2 = ns_probe["gen_seq_problem"]
    truth2 = {}
    for pid in FIX2:
        scheme = r12_seed2(pid)
        init, ops, _ret = _unpack_gen(gen2(scheme))
        ops = [list(o) for o in ops]
        truth = seq_states_along(init, ops)
        truth2[pid] = truth
        k = _retry_depth(gen2, scheme, init, ops)
        recs.append({"cell": "meta2", "pid": pid, "seed": scheme + RETRY_STEP * (k or 0),
                     "init": init, "ops": ops, "truth": truth,
                     "features": {"kinds": sorted({o[0] for o in ops}), "n_ops": len(ops),
                                  "tail_positions": sorted(_tail_positions(ops))}})

    def nw1(pid, cell, turn):
        if degenerate:
            return 1
        return _fix_nw1(pid, cell, turn)

    def nw2(pid, cell, turn):
        if degenerate:
            return 1
        return _fix_nw2(pid, cell, turn)

    def graded(cell, pid, turn, fam, truth):
        want = _want_for(cell, pid, turn, truth)
        if (not degenerate) and cell == "T-SPARSE" and pid == FIX2[-1] \
                and turn == FINAL_TURN[cell]:
            return stamp({"cell": cell, "pid": pid, "turn": turn, "ok": False,
                          "nwrong": len(want), "got": None, "want": want,
                          "finish": "length", "usage": {"total_tokens": 5},
                          "wall_s": 0.02, "raw": "no json here at all"})
        k = nw1(pid, cell, turn) if fam == 1 else nw2(pid, cell, turn)
        got = _perturb_dict(want, k) if fam == 1 else _perturb_list(want, k)
        if fam == 1 and cell == "A-INC" and pid == FIX1[0] and turn == 1:
            raw = json.dumps(got)          # bare-brace fallback (no fences)
        elif fam == 2 and cell == "T-DENSE" and pid == FIX2[0] and turn == 4:
            raw = json.dumps(got)          # bare-array fallback (no fences)
        else:
            raw = _fence(got)
        return stamp({"cell": cell, "pid": pid, "turn": turn, "ok": got == want,
                      "nwrong": (grade_state(got, want) if fam == 1
                                 else grade_seq(got, want))[1],
                      "got": got, "want": want, "finish": "stop",
                      "usage": {"total_tokens": 7}, "wall_s": 0.05, "raw": raw})

    ack_seen = [0]
    for pid in FIX1:
        for cell in arm_order(pid):
            recs.append(stamp({"cell": "filler", "finish": "stop",
                               "usage": {"total_tokens": 3}, "wall_s": 0.01,
                               "raw": "ready"}))
            if cell == MONO_CELL:
                recs.append(graded(cell, pid, 1, 1, truth1))
                continue
            for turn in range(1, 11):
                if turn in F1_CHECKPOINTS[cell]:
                    recs.append(graded(cell, pid, turn, 1, truth1))
                else:
                    ack_seen[0] += 1
                    raw = "ok" if ack_seen[0] % 5 else "sure"
                    recs.append(stamp({"cell": cell + "-ack", "pid": pid, "turn": turn,
                                       "raw": raw, "finish": "stop",
                                       "usage": {"total_tokens": 2}, "wall_s": 0.01}))
    for pid in FIX2:
        for cell in f2_order(pid):
            recs.append(stamp({"cell": "filler", "finish": "stop",
                               "usage": {"total_tokens": 3}, "wall_s": 0.01,
                               "raw": "ready"}))
            for turn in range(1, 11):
                if turn in F2_CHECKPOINTS[cell]:
                    recs.append(graded(cell, pid, turn, 2, truth2))
                else:
                    ack_seen[0] += 1
                    recs.append(stamp({"cell": cell + "-ack", "pid": pid, "turn": turn,
                                       "raw": "ok", "finish": "stop",
                                       "usage": {"total_tokens": 2}, "wall_s": 0.01}))

    # ---- filed probabilities (pinned schemas: arm/p_p_pass and contrast/p_diffpos)
    prob_lines = []
    for cell in F1_ARMS:
        for pid in FIX1:
            prob_lines.append(json.dumps(
                {"arm": cell, "base_arm": 0.5, "delta_arm": 0.0, "family": 1,
                 "p_pass": _fix_p1(pid, cell), "pid": pid, "x_pid": 1.0},
                separators=(",", ":")))
    for cell in F2_ARMS:
        for pid in FIX2:
            prob_lines.append(json.dumps(
                {"arm": cell, "base_arm": _fix_p2(cell), "delta_arm": 0.0, "family": 2,
                 "p_pass": _fix_p2(cell), "pid": pid, "x_pid": 0.0},
                separators=(",", ":")))
    probs_path = wp("predictions-r12-perproblem.jsonl", "\n".join(prob_lines) + "\n")
    sign_lines = []
    for cid, ca, cb, turns in SIGN_CONTRASTS:
        fam = 1 if ca in F1_ARMS else 2
        for pid in (FIX1 if fam == 1 else FIX2):
            sign_lines.append(json.dumps(
                {"contrast": cid, "family": fam, "label": f"{ca} - {cb}",
                 "p_diffpos": _fix_sign_p(cid), "pid": pid,
                 "turns": str(turns) if turns else "final"}, separators=(",", ":")))
    sign_path = wp("predictions-r12-signevents.jsonl", "\n".join(sign_lines) + "\n")

    # ---- predictions-r12.md (arm point rows + RL1-RL7 + internal sha pins)
    pred_lines = ["# Round-12 filed predictions (fixture)", "",
                  "| Quantity | Predicted | Basis |", "|---|---:|---|"]
    for cell in GRADED_CELLS:
        pred_lines.append(f"| {cell} final (turn-10) passes | {FIX_PRED_PASSES[cell]}/"
                          f"{len(FIX1)} | fixture |")
    pred_lines.append("| Paired severity diff (A-CKPT710 - A-CKPT4710, mean nwrong at "
                      f"shared {{7,10}}) | {FIX_PRED_DIFF:+.3f} | fixture |")
    pred_lines.append(f"| E1 Page trend L | {FIX_PRED_PAGE_L:.1f} | fixture |")
    pred_lines.append("")
    pred_lines.append("Per-problem values: `predictions-r12-perproblem.jsonl` "
                      f"({len(prob_lines)} lines, sha256 `{file_sha256(probs_path)}`)")
    pred_lines.append("Per-event values: `predictions-r12-signevents.jsonl` "
                      f"({len(sign_lines)} lines, sha256 `{file_sha256(sign_path)}`)")
    pred_lines.append("")
    pred_lines.append("## 5. Run-level probabilistic predictions")
    pred_lines.append("")
    pred_lines.append("| id | event | P | justification |")
    pred_lines.append("|---|---|---:|---|")
    for rid, p in ((r, FIX_RL_P[r]) for r in RL_IDS):
        pred_lines.append(f"| {rid} | fixture event {rid} | {p:.2f} | fixture |")
    pred = wp("predictions-r12.md", "\n".join(pred_lines) + "\n")

    bundle_files = list(R12_REQUIRED_BUNDLE)
    sha_text = "".join(f"{file_sha256(os.path.join(d, n))}  "
                       f"corpus/evidence/round12-ladder/{n}\n" for n in bundle_files)
    sha_path = wp("prereg-bundle.sha256", sha_text)

    desc = {"cell": "descriptors", "endpoint": "http://127.0.0.1:34113",
            "models_json": {"data": [{"id": "fixture-qwen3-coder-30b"}]},
            "server": {"pid": 4242, "argv": ["llama-server", "--parallel", "2"]},
            "temp": 0.2, "maxtok": 8192, "system_prompt": ns_probe["SYSTEM"],
            "seed_scheme": R12_SEED_SCHEME_1, "seed_scheme_f2": R12_SEED_SCHEME_2,
            "pids": list(FIX1), "pids_f2": list(FIX2), "n": len(FIX1), "n2": len(FIX2),
            "arm_order_counts": arm_order_counts(FIX1),
            "counterbalance": "family 2: even pid -> T-DENSE first, odd pid -> T-SPARSE first",
            "schedule": "families interleaved pid-block-by-pid-block",
            "n_jobs": census_expected(len(FIX1), len(FIX2))["jobs"],
            "machinery_sha256": file_sha256(probe),
            "runner_sha256": file_sha256(os.path.join(d, "run_r12.py")),
            "predictor_sha256": file_sha256(os.path.join(d, "predict_r12.py")),
            "prereg_bundle_sha256": file_sha256(sha_path),
            "probe_lineage": "fixture lineage"}
    recs.insert(0, stamp(desc, explicit=_fix_ts(0)))
    jsonl = os.path.join(d, "results-r12.jsonl")
    with open(jsonl, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")
    # descriptors_end last, with n_records = lines - 1 (L1 pin)
    with open(jsonl, "a", encoding="utf-8") as f:
        f.write(json.dumps(stamp({"cell": "descriptors_end",
                                  "models_json": {"data": [{"id": "fixture-qwen3-coder-30b"}]},
                                  "server": {"pid": 4242, "argv": ["llama-server"]},
                                  "wall_total_s": 212.5,
                                  "n_records": len(recs)},
                                 ), separators=(",", ":")) + "\n")
    recs.append(json.loads(open(jsonl, encoding="utf-8").read().splitlines()[-1]))

    # ---- run.log
    jobs = [(c, p) for p in FIX1 for c in arm_order(p)] + \
           [(c, p) for p in FIX2 for c in f2_order(p)]
    log = [f"[{i}/{len(jobs)}] ('{c}', {p})" for i, (c, p) in enumerate(jobs, 1)]
    summary = []
    for cell in GRADED_CELLS:
        truth = truth1 if cell in F1_ARMS else truth2
        rows = [r for r in recs if r.get("cell") == cell and r.get("turn") == FINAL_TURN[cell]]
        passes = 0
        for r in rows:
            got = extract_json_block(r.get("raw", ""))
            want = _want_for(cell, r["pid"], r["turn"], truth)
            ok_re = (grade_state(got, want) if cell in F1_ARMS else grade_seq(got, want))[0]
            passes += 1 if ok_re else 0
        summary.append((cell, passes, len(rows)))
    log += ["", "=== SUMMARY ==="]
    log += [f"{c}: {p}/{n}" for c, p, n in summary]
    log += ["wall_total_s: 212.5", ""]
    runlog = wp("run.log", "\n".join(log) + "\n")

    ordering_text = ("pre-hash 2026-09-29T01:16:08Z\n"
                     "post-hash 2026-09-29T01:16:08Z\n"
                     "bundle sha256 file prereg-bundle.sha256 (v1: fixture)\n")
    for name in R12_SCRIPT_HASH_REQUIRED:
        ordering_text += (f"run-script-hash 2026-09-29T01:16:08Z "
                          f"{file_sha256(os.path.join(d, name))} {name} (fixture)\n")
    ordering_text += "main-run-launch 2026-09-29T01:19:59Z\n"
    ordering_path = wp("ordering.log", ordering_text)

    probs = {}
    for line in prob_lines:
        o = json.loads(line)
        probs[(o["arm"], o["pid"])] = o["p_pass"]
    sign_probs = {}
    for line in sign_lines:
        o = json.loads(line)
        sign_probs[(o["contrast"], o["pid"])] = o["p_diffpos"]
    err = _error_pids(recs, FIX1, FIX2)
    aim = _analysis_inputs(sha_path, ordering_path, recs)
    R = _recompute_r12(recs, truth1, truth2, FIX1, FIX2, err, probs,
                       file_sha256(probs_path), 1, 1, r11_e2_point(R11_MD),
                       probs_sign=sign_probs, sign_digest=file_sha256(sign_path),
                       probs_run=dict(FIX_RL_P))
    R_over = _recompute_r12(recs, truth1, truth2, FIX1, FIX2, err, probs,
                            file_sha256(probs_path), MIN_N_FAMILY_1, MIN_N_FAMILY_2,
                            r11_e2_point(R11_MD), probs_sign=sign_probs,
                            sign_digest=file_sha256(sign_path), probs_run=dict(FIX_RL_P))
    md_path = wp("analysis_r12.md", _fixture_analysis_md(R, aim, recs))
    md_over = wp("analysis_r12_override.md", _fixture_analysis_md(R_over, aim, recs))
    return {"dir": d, "probe": probe, "jsonl": jsonl, "runlog": runlog, "root": tmp,
            "ordering": ordering_path, "sha": sha_path, "md": md_path,
            "md_override": md_over, "pred": pred, "probs_path": probs_path,
            "sign_path": sign_path, "recs": recs,
            "md_text": read_text(md_path), "md_override_text": read_text(md_over),
            "runlog_text": read_text(runlog), "ordering_text": ordering_text,
            "sha_text": sha_text, "R": R, "R_override": R_over,
            "truth1": truth1, "truth2": truth2, "probs_map": probs, "aim": aim,
            "sign_map": sign_probs, "first_ts": _fix_ts(0), "degenerate": degenerate,
            "probs_digest": file_sha256(probs_path),
            "pred_text": read_text(pred),
            "clean_files": {n: read_text(os.path.join(d, n)) for n in
                            ("predictions-r12.md", "predictions-r12-perproblem.jsonl",
                             "predictions-r12-signevents.jsonl", "prereg-bundle.sha256")},
            "pins": {"r12_jsonl": ("md5", _hash_file("md5", jsonl)), "r12_md": ("md5", _hash_file("md5", md_path))}}


def _fixture_analysis_md(R, aim, recs):
    """The amended §5 document, written from the recomputed quantities."""
    a, pg, e2, e6 = R["arms"], R["page"], R["e2"], R["e6"]
    pset, sset, rset, aset = e6["pass"], e6["sign"], e6["runlevel"], e6["all"]
    n = R["n_eff"][0]
    L = []
    L.append("results-r12.jsonl contains %d descriptors, %d meta, %d meta2, %d graded, "
             "%d ack, %d fillers, %d error records"
             % (sum(1 for r in recs if r.get("cell") in ("descriptors", "descriptors_end")),
                sum(1 for r in recs if r.get("cell") == "meta"),
                sum(1 for r in recs if r.get("cell") == "meta2"),
                sum(1 for r in recs if r.get("cell") in GRADED_CELLS and "ok" in r),
                sum(1 for r in recs if r.get("cell") in ACK_CELLS),
                sum(1 for r in recs if r.get("cell") == "filler"),
                sum(1 for r in recs if r.get("cell") == "error")))
    L.append("")
    L.append("| Arm | Final passes / n | Mean final nwrong | Mean nwrong (shared turns) |")
    L.append("|---|---:|---:|---:|")
    for cell in GRADED_CELLS:
        p, nn, mf, ma = a[cell]
        L.append(f"| {cell} | {p}/{nn} | {mf:.3f} | {ma:.3f} |")
    L.append("")
    L.append(f"E1 Page trend: L={pg['L']:.1f} E_L={pg['E_L']:.1f} var_L={pg['var_L']:.3f} "
             f"z={pg['z']:+.3f} two-sided p={pg['p']:.4f} direction={pg['direction']}")
    L.append(f"E2 paired diff (710 - 4710, {{7,10}}): {e2['diff']:+.3f} sd {e2['sd']:.3f} "
             f"n={e2['n']}")
    L.append(f"E2 paired t: t={e2['t']:+.3f}, df={max(e2['n'] - 1, 0)}, "
             f"two-sided p={e2['p']:.4f}")
    L.append(f"E2 95% CI: [{e2['ci_lo']:+.3f}, {e2['ci_hi']:+.3f}]")
    L.append(f"E2 exact sign: wins={e2['wins']} losses={e2['losses']} ties={e2['ties']} "
             f"two-sided p={exact_sign_p(e2['wins'], e2['losses']):.4f} "
             f"direction={R['sign_direction']}")
    L.append(f"E2 McNemar final passes: b={e2['mcnemar'][0]} c={e2['mcnemar'][1]} "
             f"two-sided p={e2['mcnemar'][2]:.4f}")
    g = R["e3"]
    L.append(f"E3 adjacent gaps: 4710-INC {{4,7,10}} {g[0][2]:+.3f} p={g[0][3]:.4f}; "
             f"710-4710 {{7,10}} {g[1][2]:+.3f} p={g[1][3]:.4f}; "
             f"10-710 {{10}} {g[2][2]:+.3f} p={g[2][3]:.4f}")
    e4, e5 = R["e4"], R["e5"]
    L.append(f"E4 batching diff (MONO - CKPT10, final): {e4['diff']:+.3f} sd {e4['sd']:.3f} "
             f"n={e4['n']} t={e4['t']:+.3f} p={e4['p']:.4f} "
             f"sign W/L/T={e4['wins']}/{e4['losses']}/{e4['ties']}")
    L.append(f"E5 transport diff (SPARSE - DENSE, {{7,10}}): {e5['diff']:+.3f} "
             f"sd {e5['sd']:.3f} n={e5['n']} t={e5['t']:+.3f} p={e5['p']:.4f} "
             f"sign W/L/T={e5['wins']}/{e5['losses']}/{e5['ties']}")
    L.append(f"E6 events: pass={pset['n']} sign={sset['n']} runlevel={rset['n']} "
             f"total={aset['n']} (excluded pids dropped from score and climatology)")
    L.append("E6 Brier pass: pooled=%s (N=%d); per-arm %s"
             % (_fmtp(pset["brier"], ".4f"), pset["n"],
                " ".join("%s=%s" % (c, _fmtp(pset["per_group"].get(c), ".4f"))
                         for c in GRADED_CELLS)))
    L.append("E6 Brier sign: pooled=%s (N=%d); per-contrast %s"
             % (_fmtp(sset["brier"], ".4f"), sset["n"],
                " ".join("%s=%s" % (cid, _fmtp(sset["per_group"].get(cid), ".4f"))
                         for cid, _a, _b, _t in SIGN_CONTRASTS)))
    L.append("E6 Brier runlevel: pooled=%s (N=%d); per-event %s"
             % (_fmtp(rset["brier"], ".4f"), rset["n"],
                " ".join("%s=%s" % (rid, _fmtp(rset["per_event"].get(rid), ".4f"))
                         for rid in RL_IDS)))
    L.append("E6 Brier all: pooled=%s (N=%d)"
             % (_fmtp(aset["brier"], ".4f"), aset["n"]))
    L.append("E6 BSS pass vs arm climatology: pooled=%s [persistence + arm-rate "
             "transport]; family1-replicate=%s (N=%d); family1-novel=%s (N=%d); "
             "family2=%s (N=%d)"
             % (_fmtp(pset["bss"], "+.4f"), _fmtp(e6["splits"]["family1-replicate"]["bss"], "+.4f"),
                e6["splits"]["family1-replicate"]["n"],
                _fmtp(e6["splits"]["family1-novel"]["bss"], "+.4f"),
                e6["splits"]["family1-novel"]["n"],
                _fmtp(e6["splits"]["family2"]["bss"], "+.4f"),
                e6["splits"]["family2"]["n"]))
    L.append(f"E6 BSS sign={_fmtp(sset['bss'], '+.4f')} "
             f"runlevel={_fmtp(rset['bss'], '+.4f')} "
             f"pooled-all-727={_fmtp(aset['bss'], '+.4f')}")
    cp, ca = e6["calib_pass"] or {}, e6["calib_all"] or {}
    L.append("E6 calibration (pass events): slope=%s intercept=%s "
             "(damped Newton on logit(p) clipped to [1e-06, 0.999999], %s events)"
             % (_fmtp(cp.get("slope"), "+.4f"), _fmtp(cp.get("intercept"), "+.4f"),
                cp.get("n")))
    L.append("E6 calibration (all events): slope=%s intercept=%s (%s events)"
             % (_fmtp(ca.get("slope"), "+.4f"), _fmtp(ca.get("intercept"), "+.4f"),
                ca.get("n")))
    for lo, hi, pred, obs, cnt in e6["reliability"]:
        L.append("E6 reliability (5 bins, pass events): %.1f-%.1f: pred=%s obs=%s n=%d"
                 % (lo, hi, _fmtp(pred, ".3f"), _fmtp(obs, ".3f"), cnt))
    length, parse, total = R["finish"]
    L.append(f"Finish audit at graded turns: finish=length {length}/{total}, "
             f"parse fail {parse}/{total}")
    ack = " ".join(f"{c} {R['ack'][c][0]}/{R['ack'][c][1]} = {R['ack'][c][2]:.1f}%"
                   for c in ACK_CELLS)
    L.append(f"Ack compliance (raw lowercased startswith ok): {ack}")
    fam = R["excluded"]
    L.append("Excluded pids: family1 %s family2 %s"
             % (",".join(str(x) for x in fam["family1"]) or "none",
                ",".join(str(x) for x in fam["family2"]) or "none"))
    L.append("Realized arm positions after deletion: "
             + "; ".join(f"{cell}:{' '.join(str(x) for x in R['realized_positions'][cell])}"
                         for cell in F1_ARMS))
    if R["degenerate"]["page"]:
        L.append("NOTE degenerate: zero-variance Page (var_L=0)")
    for name in ("E2", "E4", "E5"):
        if R["degenerate"][name]:
            L.append(f"NOTE degenerate: zero-variance diffs ({name})")
    for label, _t, _d, _p, _st in R["e3"]:
        if R["degenerate"]["E3 " + label]:
            L.append(f"NOTE degenerate: zero-variance diffs (E3 {label})")
    L.append("")
    vlabels = {"R1": "ladder", "R2": "repeat", "R3": "batching",
               "R4": "transport", "R5": "forecast"}
    for k in ("R1", "R2", "R3", "R4", "R5"):
        text = R["verdicts"][k]
        if k == "R2" and R["r2_point_clause"]:
            text += " — additionally POINT-MATCHES-r11"
        L.append(f"VERDICT {k} {vlabels[k]}: {text}")
    L.append("")
    L.append("| Quantity | Predicted | Observed | Abs error |")
    L.append("|---|---:|---:|---:|")
    for cell in GRADED_CELLS:
        p, nn, _mf, _ma = a[cell]
        pred = FIX_PRED_PASSES[cell]
        L.append(f"| {cell} final passes | {pred}/{n} | {p}/{nn} | "
                 f"{abs(pred / n - p / nn):.3f} |")
    L.append(f"| Paired diff (A-CKPT710 - A-CKPT4710) | {FIX_PRED_DIFF:+.3f} | "
             f"{e2['diff']:+.3f} | {abs(FIX_PRED_DIFF - e2['diff']):.3f} |")
    L.append(f"| E1 Page trend L | {FIX_PRED_PAGE_L:.1f} | {pg['L']:g} | "
             f"{abs(FIX_PRED_PAGE_L - pg['L']):.3f} |")
    L.append("")
    L.append("Ordering proof: prereg-bundle.sha256 v1 — " + ", ".join(aim["bundle_digests"]))
    L.append(f"ordering.log pre-hash {aim['pre_hash']} / post-hash {aim['post_hash']}; "
             f"first request_ts {aim['first_request_ts']}.")
    L.append("Single served unit — Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS under the stack "
             "pinned in the `descriptors` record (q4_0 KV cache, `--kv-unified`, "
             "`--parallel 2`, custom non-upstream chat template); no cross-model "
             "generalization.")
    return "\n".join(L) + "\n"


def _md_set(md, key, group, new_text):
    m = re.search(_R12_STORED[key], md, re.M)
    if not m:
        raise SystemExit(f"fixture: stored pattern {key!r} not found in the analysis md")
    return md[:m.start(group)] + new_text + md[m.end(group):]


def _md_bump(md, key, group, delta, prec="+.3f"):
    m = re.search(_R12_STORED[key], md, re.M)
    if not m:
        raise SystemExit(f"fixture: stored pattern {key!r} not found in the analysis md")
    return _md_set(md, key, group, format(_num(m.group(group)) + delta, prec))


def _md_set_score_obs(md, arm, new_text):
    for line in md.splitlines():
        if arm in line and "final passes" in line and line.strip().startswith("|"):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) == 4 and parts[0].startswith(arm):
                parts[2] = new_text
                old = line
                new = "| " + " | ".join(parts) + " |"
                return md.replace(old, new, 1)
    raise SystemExit(f"fixture: no scoring row for {arm}")


def _deep(x):
    return json.loads(json.dumps(x))


_VERDICT_BRANCHES = {
    "R1": ["LADDER ESTABLISHED", "LADDER DIRECTIONAL", "LADDER NOT SUPPORTED"],
    "R2": ["REPEATS-r11", "REPEATS-DOWNGRADED", "DIRECTIONAL", "DOES-NOT-REPEAT"],
    "R3": ["DISSOCIATION ESTABLISHED", "DISSOCIATION DIRECTIONAL",
           "DISSOCIATION FALSIFIED"],
    "R4": ["TRANSPORTS", "TRANSPORT DIRECTIONAL", "TRANSPORT NOT SUPPORTED"],
    "R5": ["FORECAST SKILLED", "FORECAST SKILLED-MISCALIBRATED", "FORECAST UNSKILLED"],
}


def _other_branch(state, key):
    """A branch of the same verdict rule that differs from the recomputed one."""
    cur = state["R"]["verdicts"][key]
    return next(b for b in _VERDICT_BRANCHES[key] if b != cur)


def _run(state, **ov):
    """One gate pass over the fixture tree with optional input overrides."""
    rep = Report()
    recs = ov.get("recs", state["recs"])
    md = ov.get("md", state["md_text"])
    if ov.get("md_from_R") is not None:
        md = _fixture_analysis_md(ov["md_from_R"], state["aim"], recs)
    pred = state["pred"]
    if ov.get("md_pred") is not None:
        pred = os.path.join(state["dir"], "predictions-r12.mutated.md")
        with open(pred, "w", encoding="utf-8") as f:
            f.write(ov["md_pred"])
    grade_r12(recs, md, ov.get("runlog", state["runlog_text"]), rep,
              pids1=FIX1, pids2=FIX2,
              machinery_path=ov.get("machinery", state["probe"]),
              r11_jsonl=ov.get("r11_jsonl", R11_JSONL), r11_md=R11_MD,
              pred_path=pred, bundle_path=ov.get("bundle", state["sha"]),
              ordering_path=ov.get("ordering", state["ordering"]),
              dir_path=state["dir"],
              min_n1=ov.get("min_n1", 1), min_n2=ov.get("min_n2", 1))
    check_r12_ordering(rep, jsonl_path=state["jsonl"],
                       sha_path=ov.get("sha_path", state["sha"]),
                       ordering_path=ov.get("ordering", state["ordering"]),
                       dir_path=state["dir"], recs=recs, repo_root=state["root"])
    check_r12_pins({"r12_jsonl": state["jsonl"], "r12_md": state["md"]}, rep,
                   ov.get("pins", state["pins"]))
    return rep


def _battery():
    """(name, expected check id, mutation) for the S7 mutation battery.

    Every check family is killed by at least one entry (see r12-grader-notes.md
    for the family -> mutation map).
    """

    def first(recs, pred):
        for r in recs:
            if pred(r):
                return r
        raise SystemExit("fixture: mutation target not found")

    def m_nw(cell):
        def fn(s, _t):
            recs = _deep(s["recs"])
            r = first(recs, lambda x: x.get("cell") == cell and "ok" in x)
            r["nwrong"] = (r["nwrong"] or 0) + 1
            return {"recs": recs}
        return fn

    def m_ok(cell):
        def fn(s, _t):
            recs = _deep(s["recs"])
            r = first(recs, lambda x: x.get("cell") == cell and "ok" in x)
            r["ok"] = not r["ok"]
            return {"recs": recs}
        return fn

    def m_got_digit(cell):
        def fn(s, _t):
            recs = _deep(s["recs"])
            r = first(recs, lambda x: x.get("cell") == cell and "ok" in x)
            raw = r["raw"]
            blocks = list(re.finditer(r"```(?:json)?\s*\n(.*?)```", raw, re.S))
            b = blocks[-1]
            inner = b.group(1)
            dm = re.search(r"\d", inner)
            newdigit = str((int(dm.group(0)) + 1) % 10)
            r["raw"] = (raw[:b.start(1)] + inner[:dm.start()] + newdigit
                        + inner[dm.end():] + raw[b.end(1):])
            return {"recs": recs}
        return fn

    def m_raw_unparseable(cell):
        def fn(s, _t):
            recs = _deep(s["recs"])
            r = first(recs, lambda x: x.get("cell") == cell and "ok" in x)
            r["raw"] = "no json here at all"
            return {"recs": recs}
        return fn

    def m_meta_field(field, v):
        def fn(s, _t):
            recs = _deep(s["recs"])
            r = first(recs, lambda x: x.get("cell") == "meta")
            r[field] = v(r[field])
            return {"recs": recs}
        return fn

    def m_meta2_field(field, v):
        def fn(s, _t):
            recs = _deep(s["recs"])
            r = first(recs, lambda x: x.get("cell") == "meta2")
            r[field] = v(r[field])
            return {"recs": recs}
        return fn

    def m_drop(cell, n=1):
        def fn(s, _t):
            recs = _deep(s["recs"])
            out, dropped = [], 0
            for r in recs:
                if r.get("cell") == cell and dropped < n:
                    dropped += 1
                    continue
                out.append(r)
            return {"recs": out}
        return fn

    def m_rec(cell, mutate):
        def fn(s, _t):
            recs = _deep(s["recs"])
            for r in recs:
                if r.get("cell") == cell:
                    mutate(r)
                    break
            return {"recs": recs}
        return fn

    def m_desc(field, v):
        def fn(s, _t):
            recs = _deep(s["recs"])
            r = first(recs, lambda x: x.get("cell") == "descriptors")
            if callable(v):
                v(r)
            else:
                r[field] = v
            return {"recs": recs}
        return fn

    def m_runlog(old, new):
        def fn(s, _t):
            return {"runlog": s["runlog_text"].replace(old, new, 1)}
        return fn

    def m_runlog_drop_line():
        def fn(s, _t):
            lines = s["runlog_text"].splitlines()
            for i, l in enumerate(lines):
                if l.startswith("[3/"):
                    del lines[i]
                    break
            return {"runlog": "\n".join(lines) + "\n"}
        return fn

    def m_runlog_swap_jobs():
        def fn(s, _t):
            lines = s["runlog_text"].splitlines()
            idx = [i for i, l in enumerate(lines) if l.endswith(", 201)")][:2]
            lines[idx[0]], lines[idx[1]] = lines[idx[1]], lines[idx[0]]
            return {"runlog": "\n".join(lines) + "\n"}
        return fn

    def m_ordering(new_text):
        def fn(s, tmp):
            path = os.path.join(tmp, "ordering_mutated.log")
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text(s["ordering_text"]))
            return {"ordering": path}
        return fn

    def m_md_set(key, group, new_text):
        def fn(s, _t):
            return {"md": _md_set(s["md_text"], key, group, new_text)}
        return fn

    def m_md_bump(key, group, delta, prec="+.3f"):
        def fn(s, _t):
            return {"md": _md_bump(s["md_text"], key, group, delta, prec)}
        return fn

    def m_md_replace(old, new):
        def fn(s, _t):
            assert old in s["md_text"], f"fixture: {old!r} not in the analysis md"
            return {"md": s["md_text"].replace(old, new, 1)}
        return fn

    def m_r11_synth(s, tmp):
        recs = _deep(s["recs"])
        path = os.path.join(tmp, "r11-synth.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for r in recs:
                if r.get("cell") != "meta":
                    continue
                r2 = {k: v for k, v in r.items() if k != "seed"}
                if r2["pid"] == FIX1[1]:
                    k0 = sorted(r2["init"])[0]
                    r2["init"][k0] += 1
                f.write(json.dumps(r2, separators=(",", ":")) + "\n")
        return {"r11_jsonl": path}

    battery = [
        # ---- replay layer ----
        ("M01 flip a stored nwrong (A-CKPT4710)", "r12.replay.A-CKPT4710.nwrong",
         m_nw("A-CKPT4710")),
        ("M02 flip a stored ok (A-INC)", "r12.replay.A-INC.ok", m_ok("A-INC")),
        ("M03 digit-bump inside the first A-CKPT10 fenced block", "r12.replay.A-CKPT10.got",
         m_got_digit("A-CKPT10")),
        ("M04 flip a stored nwrong (T-DENSE, list metric)", "r12.replay.T-DENSE.nwrong",
         m_nw("T-DENSE")),
        ("M05 unparseable T-SPARSE raw (parse-fail convention)", "r12.replay.T-SPARSE.nwrong",
         m_raw_unparseable("T-SPARSE")),
        ("M06 unparseable A-INC raw", "r12.replay.A-INC.ok", m_raw_unparseable("A-INC")),
        # ---- meta / meta2 ----
        ("M07 corrupt a family-1 meta seed (+1)", "r12.meta.seed",
         m_meta_field("seed", lambda v: v + 1)),
        ("M08 corrupt a family-1 meta init", "r12.meta.regenerate.init",
         m_meta_field("init", lambda v: {**v, sorted(v)[0]: v[sorted(v)[0]] + 1})),
        ("M09 corrupt a family-1 meta truth", "r12.meta.regenerate.truth",
         m_meta_field("truth", lambda v: v[:-1] + [{**v[-1], sorted(v[-1])[0]: 999}])),
        ("M10 corrupt a family-1 meta tail_touched", "r12.meta.regenerate.tail_touched",
         m_meta_field("tail_touched", lambda v: [])),
        ("M11 delete a family-1 meta record", "r12.meta.count", m_drop("meta")),
        ("M12 corrupted r11-side meta (cross-tree identity)", "r12.meta.r11_identity.init",
         m_r11_synth),
        ("M13 corrupt a family-2 meta seed (+1)", "r12.meta2.seed",
         m_meta2_field("seed", lambda v: v + 1)),
        ("M14 swap two family-2 ops", "r12.meta2.regenerate.ops",
         m_meta2_field("ops", lambda v: [v[1], v[0]] + v[2:])),
        ("M15 corrupt a family-2 meta truth", "r12.meta2.regenerate.truth",
         m_meta2_field("truth", lambda v: v[:-1] + [list(reversed(v[-1]))])),
        ("M16 corrupt a family-2 features value", "r12.meta2.features",
         m_meta2_field("features", lambda v: {**v, "n_ops": v["n_ops"] + 1})),
        ("M17 break the machinery load (syntax-broken probe_r12.py)",
         "r12.meta2.machinery.gen_seq_problem",
         (lambda s, _t: {"machinery": os.path.join(s["dir"], "probe_broken.py")})),
        # ---- descriptors ----
        ("M18 drift descriptors_end models_json id", "r12.descriptors.end_models_match",
         (lambda s, _t: {"recs": [
             {**r, "models_json": {"data": [{"id": "drifted-model"}]}}
             if r.get("cell") == "descriptors_end" else r for r in _deep(s["recs"])]})),
        ("M19 corrupt descriptors machinery_sha256", "r12.descriptors.machinery_sha256",
         m_desc("machinery_sha256", "0" * 64)),
        ("M20 corrupt descriptors arm_order_counts", "r12.descriptors.arm_order_counts",
         m_desc(None, lambda r: r["arm_order_counts"].update({"A-INC": [1, 1, 1, 1, 1]}))),
        ("M21 drop the runner hash from descriptors",
         "r12.descriptors.sha_key.runner_sha256",
         m_desc(None, lambda r: r.pop("runner_sha256", None))),
        ("M22 corrupt descriptors system_prompt",
         "r12.descriptors.system_prompt_matches_machinery",
         m_desc("system_prompt", "not the machinery system prompt")),
        ("M23 remove the family-2 counterbalance string", "r12.descriptors.f2_counterbalance",
         m_desc("counterbalance", "family2 order by pid")),
        ("M24 corrupt descriptors n_jobs", "r12.descriptors.n_jobs",
         m_desc("n_jobs", 999)),
        ("M25 corrupt descriptors_end n_records", "r12.descriptors.end_n_records",
         m_rec("descriptors_end", lambda r: r.update({"n_records": 12345}))),
        ("M26 change the descriptors_end server pid", "r12.descriptors.end_server_pid",
         m_rec("descriptors_end", lambda r: r.update({"server": {"pid": 9999}}))),
        # ---- census ----
        ("M27 delete one graded record", "r12.census.graded.A-CKPT10", m_drop("A-CKPT10")),
        ("M28 delete one ack record", "r12.census.ack.A-CKPT4710-ack",
         m_drop("A-CKPT4710-ack")),
        ("M29 delete one filler record", "r12.census.fillers", m_drop("filler")),
        ("M30 delete the descriptors_end record", "r12.census.descriptors_end",
         m_drop("descriptors_end")),
        ("M31 strip request_ts from a filler", "r12.census.stamped_records",
         m_rec("filler", lambda r: r.update({"request_ts": ""}))),
        ("M32 add an off-design A-INC-ack record", "r12.census.no_inc_acks",
         (lambda s, _t: {"recs": _deep(s["recs"]) + [
             {"cell": "A-INC-ack", "pid": FIX1[0], "turn": 2, "raw": "ok",
              "finish": "stop", "usage": {}, "wall_s": 0.0,
              "request_ts": _fix_ts(0)}]})),
        ("M33 drop the usage field from a filler", "r12.replay.filler.fields",
         m_rec("filler", lambda r: r.pop("usage", None))),
        ("M34 pad an ack raw past 80 chars", "r12.replay.A-CKPT4710-ack.raw_truncated",
         m_rec("A-CKPT4710-ack", lambda r: r.update({"raw": "x" * 90}))),
        ("M35 change an ack turn", "r12.replay.A-CKPT4710-ack.turn_set",
         m_rec("A-CKPT4710-ack", lambda r: r.update({"turn": 99}))),
        # ---- run.log ----
        ("M36 edit the A-INC SUMMARY numerator", "r12.runlog.A-INC",
         (lambda s, _t: {"runlog": _bump_summary(s["runlog_text"], "A-INC")})),
        ("M37 zero out wall_total_s", "r12.runlog.wall_total_s",
         m_runlog("wall_total_s: 212.5", "wall_total_s: 0.0")),
        ("M38 delete a progress line", "r12.runlog.jobs", m_runlog_drop_line()),
        ("M39 swap two family-1 job lines", "r12.runlog.arm_order_f1", m_runlog_swap_jobs()),
        # ---- analysis: E1/E2/E3/E4/E5 ----
        ("M40 perturb the stored E2 diff", "r12.analysis.e2.diff",
         m_md_bump("e2_diff", 1, 0.5)),
        ("M41 perturb the stored E1 Page p", "r12.analysis.e1.p",
         m_md_set("page", 5, "0.0499")),
        ("M42 perturb the Page L", "r12.analysis.e1.L",
         m_md_set("page", 1, "999.0")),
        ("M43 perturb var_L", "r12.analysis.e1.var_L",
         m_md_set("page", 3, "999.000")),
        ("M44 flip the stored E1 direction", "r12.analysis.e1.direction",
         (lambda s, _t: {"md": _md_set(
             s["md_text"], "page", 6,
             "decreasing" if s["R"]["page"]["direction"] == "increasing" else "increasing")})),
        ("M45 perturb the E2 sign direction", "r12.analysis.e2.sign_direction",
         (lambda s, _t: {"md": _md_set(
             s["md_text"], "e2_sign", 5,
             "NEUTRAL" if s["R"]["sign_direction"] != "NEUTRAL" else "+1")})),
        ("M46 perturb a stored E3 gap", "r12.analysis.e3.g1.diff",
         m_md_bump("e3", 1, 0.4)),
        ("M47 perturb the E4 batching diff", "r12.analysis.e4.diff",
         m_md_bump("e4", 1, -0.75)),
        ("M48 perturb the E5 transport diff", "r12.analysis.e5.diff",
         m_md_bump("e5", 1, -0.75)),
        # ---- analysis: E6 (three event sets) ----
        ("M49 perturb the E6 pass-event count", "r12.analysis.e6.counts_pass",
         m_md_set("e6_events", 1, "999")),
        ("M50 perturb the E6 sign-event count", "r12.analysis.e6.counts_sign",
         m_md_set("e6_events", 2, "999")),
        ("M51 perturb the pooled pass Brier", "r12.analysis.e6.brier_pass_pooled",
         m_md_bump("e6_brier", 1, 0.05, ".4f")),
        ("M52 corrupt a per-arm Brier (T-SPARSE)", "r12.analysis.e6.brier.T-SPARSE",
         (lambda s, _t: {"md": s["md_text"].replace(
             "T-SPARSE=%.4f" % s["R"]["e6"]["pass"]["per_group"]["T-SPARSE"],
             "T-SPARSE=0.9999", 1)})),
        ("M53 corrupt a per-contrast sign Brier (E3a)", "r12.analysis.e6.brier_sign.E3a",
         (lambda s, _t: {"md": s["md_text"].replace(
             "E3a=%.4f" % s["R"]["e6"]["sign"]["per_group"]["E3a"], "E3a=0.9999", 1)})),
        ("M54 corrupt a run-level Brier (RL3)", "r12.analysis.e6.brier_runlevel.RL3",
         (lambda s, _t: {"md": s["md_text"].replace(
             "RL3=%.4f" % s["R"]["e6"]["runlevel"]["per_event"]["RL3"], "RL3=0.9999", 1)})),
        ("M55 corrupt the all-events pooled Brier", "r12.analysis.e6.brier_all_pooled",
         m_md_bump("e6_brier_all", 1, 0.05, ".4f")),
        ("M56 corrupt the BSS pooled pass value", "r12.analysis.e6.bss_pass_pooled",
         m_md_bump("e6_bss", 1, 0.1, "+.4f")),
        ("M57 corrupt a BSS split", "r12.analysis.e6.bss_split.family1-novel",
         (lambda s, _t: {"md": _md_split(s["md_text"], "family1-novel", "+0.9999")})),
        ("M58 corrupt the BSS sign value", "r12.analysis.e6.bss_sign",
         (lambda s, _t: {"md": _md_set(s["md_text"], "e6_bss_groups", 1, "+0.9999")})),
        ("M59 corrupt the BSS pooled-all value", "r12.analysis.e6.bss_pooled_all",
         (lambda s, _t: {"md": _md_set(s["md_text"], "e6_bss_groups", 3, "+0.9999")})),
        ("M60 perturb the calibration slope", "r12.analysis.e6.cal_slope",
         m_md_bump("e6_cal", 1, 0.07, "+.4f")),
        ("M61 change the calibration event count", "r12.analysis.e6.cal_n",
         (lambda s, _t: {"md": _md_set(s["md_text"], "e6_cal", 3,
                                       str(s["R"]["e6"]["calib_pass"]["n"] + 1))})),
        ("M62 corrupt the all-events calibration intercept",
         "r12.analysis.e6.cal_all_intercept",
         m_md_bump("e6_cal_all", 2, 0.1, "+.4f")),
        ("M63 perturb a reliability bin", "r12.analysis.e6.reliability.0.pred",
         m_md_set("e6_rel", 3, "0.777")),
        ("M64 flip a reliability bin's n to zero", "r12.analysis.e6.reliability.0.n",
         m_md_set("e6_rel", 5, "0")),
        # ---- analysis: census sentence, arm table, audits, verdicts ----
        ("M65 perturb the census sentence (meta2)", "r12.analysis.counts.meta2",
         m_md_set("counts", 3, "999")),
        ("M66 perturb the census descriptors count", "r12.analysis.counts.descriptors",
         m_md_set("counts", 1, "1")),
        ("M67 perturb the arm table (first row passes)", "r12.analysis.arm.A-INC.passes",
         m_md_set("arm_row", 2, "9")),
        ("M68 perturb the finish-audit parse count", "r12.analysis.finish.parse_fail",
         m_md_set("finish", 3, "7")),
        ("M69 perturb an ack-compliance count", "r12.analysis.ack.A-CKPT4710-ack.count",
         m_md_set("ack", 2, "0")),
        ("M70 perturb the excluded-pids line", "r12.analysis.excluded.family1",
         m_md_set("excluded", 1, "201,202")),
        ("M71 corrupt the realized-position counts", "r12.analysis.realized_positions",
         (lambda s, _t: {"md": re.sub(
             r"(Realized arm positions after deletion: A-INC:)([\d ]+)",
             lambda mm: mm.group(1) + "9 9 9 9 9", s["md_text"], count=1)})),
        ("M72 flip the stored R1 verdict", "r12.analysis.verdict_r1",
         (lambda s, _t: {"md": _md_set(s["md_text"], "verdict_r1", 1,
                                       _other_branch(s, "R1"))})),
        ("M73 append junk after the R2 point clause", "r12.analysis.verdict_r2",
         (lambda s, _t: {"md": _md_set(
             s["md_text"], "verdict_r2", 1,
             s["R"]["verdicts"]["R2"] + " — additionally POINT-MATCHES-r11 UNEXPECTED")})),
        ("M74 drop the R2 point clause", "r12.analysis.verdict_r2",
         (lambda s, _t: {"md": s["md_text"].replace(
             " — additionally POINT-MATCHES-r11", "", 1)})),
        ("M75 flip the stored R3 verdict", "r12.analysis.verdict_r3",
         (lambda s, _t: {"md": _md_set(s["md_text"], "verdict_r3", 1,
                                       _other_branch(s, "R3"))})),
        ("M76 break the descriptor sentence", "r12.analysis.descriptor_sentence",
         (lambda s, _t: {"md": s["md_text"].replace(
             "no cross-model generalization", "x", 1)})),
        ("M77 break the ordering sentence", "r12.analysis.ordering_sentence",
         (lambda s, _t: {"md": s["md_text"].replace(s["first_ts"], "nope", 1)})),
        ("M78 perturb a scoring-table Observed value", "r12.analysis.score.row1.observed",
         (lambda s, _t: {"md": _md_set_score_obs(s["md_text"], "A-CKPT4710", "9/9")})),
        ("M79 corrupt the stored E2 t statistic", "r12.analysis.e2.t",
         m_md_bump("e2_t", 1, 1.0)),
        ("M80 corrupt the analysis' E2 CI lower bound", "r12.analysis.e2.ci_lo",
         m_md_bump("e2_ci", 1, -0.5)),
        ("M81 corrupt a stored E2 sign count", "r12.analysis.e2.sign_wins",
         m_md_set("e2_sign", 1, "99")),
        ("M82 corrupt a McNemar cell", "r12.analysis.e2.mcnemar_b",
         m_md_set("e2_mcnemar", 1, "99")),
        ("M83 drop the NOTE degenerate lines (a degenerate input still holds)",
         "r12.analysis.degenerate_note_present",
         (lambda s, _t: {"md": chr(10).join(
             [l for l in s["md_text"].splitlines()
              if not l.startswith("NOTE degenerate")]) + chr(10)})),
        # ---- probability sources ----
        ("M84 swap two pass probabilities (bundle sha unchanged)", "r12.pred.probs_sha256",
         (lambda s, _t: {"file_mut": "swap_pass"})),
        ("M85 swap two pass probabilities + re-pin the bundle",
         "r12.analysis.e6.brier_pass_pooled",
         (lambda s, _t: {"file_mut": "swap_pass", "rehash_bundle": True})),
        ("M86 make the family-2 probabilities non-constant", "r12.pred.probs_f2_constant",
         (lambda s, _t: {"file_mut": "vary_f2", "rehash_bundle": True})),
        ("M87 delete the pass probability file", "r12.pred.probs_source_unique",
         (lambda s, _t: {"file_mut": "drop_pass", "rehash_bundle": True})),
        ("M88 swap two sign probabilities (bundle sha unchanged)",
         "r12.pred.sign_probs_sha256",
         (lambda s, _t: {"file_mut": "swap_sign"})),
        ("M89 delete the sign probability file", "r12.pred.sign_prob_source_unique",
         (lambda s, _t: {"file_mut": "drop_sign", "rehash_bundle": True})),
        ("M90 corrupt the stated perproblem sha256 in predictions-r12.md",
         "r12.pred.probs_sha256_stated",
         (lambda s, _t: {"md_pred": s["pred_text"].replace(
             file_sha256(s["probs_path"]), "0" * 64, 1)})),
        # ---- ordering + pins ----
        ("M91 reorder ordering.log (post-hash after the script hashes)",
         "r12.ordering.post_le_script_hash",
         m_ordering(lambda t: t.replace("post-hash 2026-09-29T01:16:08Z",
                                        "post-hash 2026-09-29T01:16:30Z", 1))),
        ("M92 push post-hash past the first request_ts",
         "r12.ordering.hash_precedes_first_request",
         m_ordering(lambda t: t.replace("post-hash 2026-09-29T01:16:08Z",
                                        "post-hash 2026-09-29T23:59:59Z", 1))),
        ("M93 corrupt a run-script-hash digest",
         "r12.ordering.script_hash_matches_file.probe_r12.py",
         m_ordering(lambda t: re.sub(
             r"(run-script-hash \S+ )([0-9a-f]{64})( probe_r12\.py)",
             r"\g<1>" + "0" * 64 + r"\g<3>", t))),
        ("M94 delete a run-script-hash line", "r12.ordering.script_hash_lines",
         m_ordering(lambda t: "\n".join(l for l in t.splitlines()
                                        if "run_r12.py" not in l) + "\n")),
        ("M95 corrupt a bundled file's bytes", "r12.ordering.sha256.predictions-r12.md",
         (lambda s, _t: {"file_mut": "write_bundle"})),
        ("M96 pin mismatch on the landed jsonl", "pin.r12_jsonl.md5",
         (lambda s, _t: {"pins": {"r12_jsonl": ("md5", "0" * 32),
                                  "r12_md": s["pins"]["r12_md"]}})),
        # ---- minima / override ----
        ("M97 run the override analysis with powered minima", "r12.analysis.verdict_r1",
         (lambda s, _t: {"md": s["md_override_text"], "min_n1": 1, "min_n2": 1})),
        ("M98 run the powered analysis with the filed minima", "r12.analysis.verdict_r1",
         (lambda s, _t: {"md": s["md_text"], "min_n1": MIN_N_FAMILY_1,
                         "min_n2": MIN_N_FAMILY_2})),
    ]
    return battery


def _md_split(md, name, new_value):
    """Rewrite one `familyX=<value>` BSS-split token in the analysis md."""
    m = re.search(re.escape(name) + r"(?:-arms)?=(n/a|" + _SIGNS + _NUMF + r")", md)
    if not m:
        raise SystemExit(f"fixture: BSS split {name} not found")
    return md[:m.start(1)] + new_value + md[m.end(1):]


def _bump_summary(runlog_text, cell):
    """numerator+1 on a SUMMARY cell line (the fixture's own arithmetic)."""
    return re.sub(r"^" + re.escape(cell) + r": (\d+)/(\d+)$",
                  lambda m: f"{cell}: {int(m.group(1)) + 1}/{m.group(2)}",
                  runlog_text, count=1, flags=re.M)


def _run_r12_fixture():
    if not (os.path.isfile(R11_JSONL) and os.path.isfile(R11_MD)):
        print("[selftest-r12] SKIP: the fixture needs the committed r11 bytes for the "
              "cross-tree identity check and the R2 point clause")
        return 0
    results = []
    tmp = tempfile.mkdtemp(prefix="kengaku-r12-fixture-")
    try:
        state = _build_r12_fixture(tmp)
        # broken probe variant for the machinery-load mutation
        with open(os.path.join(state["dir"], "probe_broken.py"), "w", encoding="utf-8") as f:
            f.write("def gen_seq_problem(seed)\n    return [], [], 0\n")
        # the clean control
        rep = _run(state)
        results.append(("S0 control (clean synthetic tree)", not rep.mismatches,
                        f"checks={rep.checks} mismatches={len(rep.mismatches)}"
                        + ("" if not rep.mismatches else f" :: {rep.mismatches[:4]}")))
        if rep.mismatches:
            for line in rep.mismatches[:40]:
                print(f"[selftest-r12] CONTROL MISMATCH {line}")
        # S0e: the machinery loader must not execute import-time statements
        # (the synthetic probe_r12.py writes a marker file at import if it does)
        marker = os.path.join(state["dir"], "IMPORT-SIDE-EFFECT.txt")
        results.append(("S0e control (machinery loader is side-effect free)",
                        not os.path.exists(marker),
                        f"marker {'present (!)' if os.path.exists(marker) else 'absent'}: {marker}"))
        # S0c: the exact call shape grader.py will use — every path resolved from the
        # module constants, probabilities located STRUCTURALLY inside the prereg
        # bundle (no fixture-supplied probs map).
        saved_globals = {k: globals()[k] for k in
                         ("REPO_ROOT", "R12_DIR", "R12_JSONL", "R12_MD", "R12_RUNLOG",
                          "R12_ORDERING", "R12_SHA", "R12_PRED", "R12_MACHINERY")}
        try:
            globals().update({"REPO_ROOT": state["root"], "R12_DIR": state["dir"],
                              "R12_JSONL": state["jsonl"], "R12_MD": state["md"],
                              "R12_RUNLOG": state["runlog"],
                              "R12_ORDERING": state["ordering"], "R12_SHA": state["sha"],
                              "R12_PRED": state["pred"], "R12_MACHINERY": state["probe"]})
            rep3 = Report()
            grade_r12(load_jsonl(R12_JSONL), read_text(R12_MD), read_text(R12_RUNLOG),
                      rep3, pids1=FIX1, pids2=FIX2, min_n1=1, min_n2=1)
            check_r12_ordering(rep3)
            results.append(("S0c control (default paths, structural probs lookup, no "
                            "explicit probs map)", not rep3.mismatches,
                            f"checks={rep3.checks} mismatches={len(rep3.mismatches)}"
                            + ("" if not rep3.mismatches else f" :: {rep3.mismatches[:4]}")))
        finally:
            globals().update(saved_globals)
        # the override-mode control (filed minima, UNDERPOWERED-INDETERMINATE texts)
        rep_ov = _run(state, md=state["md_override_text"],
                      min_n1=MIN_N_FAMILY_1, min_n2=MIN_N_FAMILY_2)
        results.append(("S0b control (override mode, n_eff < minima)",
                        not rep_ov.mismatches,
                        f"checks={rep_ov.checks} mismatches={len(rep_ov.mismatches)}"
                        + ("" if not rep_ov.mismatches else f" :: {rep_ov.mismatches[:4]}")))
        # S0d: the D9 degenerate tree — pinned degenerate lines, never NaN/inf
        deg_root = tempfile.mkdtemp(prefix="kengaku-r12-degenerate-")
        try:
            dst = _build_r12_fixture(deg_root, degenerate=True)
            repd = _run(dst)
            bad_tok = [t for t in ("nan", "inf") if t in dst["md_text"].lower()]
            results.append(("S0d control (degenerate tree: D9 pinned lines, no NaN/inf)",
                            not repd.mismatches and not bad_tok,
                            f"checks={repd.checks} mismatches={len(repd.mismatches)} "
                            f"bad_tokens={bad_tok}"
                            + ("" if not repd.mismatches else f" :: {repd.mismatches[:4]}")))
            for name, cid, fn in (
                    ("M99 degenerate tree: stored E2 p is not the pinned 1.0000",
                     "r12.analysis.e2.p",
                     (lambda dd: {"md": _md_set(dd["md_text"], "e2_p_fix", 3, "0.5000")})),
                    ("M100 degenerate tree: all NOTE degenerate lines removed",
                     "r12.analysis.degenerate_note_present",
                     (lambda dd: {"md": chr(10).join([
                         l for l in dd["md_text"].splitlines()
                         if not l.startswith("NOTE degenerate")]) + chr(10)})),
                    ("M101 degenerate tree: z forced off the pinned +0.000",
                     "r12.analysis.e1.z",
                     (lambda dd: {"md": _md_set(dd["md_text"], "page", 4, "+2.000")})),
            ):
                try:
                    r = _run(dst, **fn(dst))
                    killed = cid in chr(10).join(r.mismatches)
                    results.append((name + f" -> {cid}", killed,
                                    f"checks={r.checks} mismatches={len(r.mismatches)}"
                                    + ("" if killed else f" :: NOT KILLED; got {r.mismatches[:3]}")))
                except SystemExit as e:
                    results.append((name + f" -> {cid}", False, f"fixture error: {e}"))
        finally:
            shutil.rmtree(deg_root, ignore_errors=True)
        for name, cid, fn in _battery():
            try:
                ov = fn(state, tmp) or {}
                ov = _apply_file_mutations(state, ov)
                r = _run(state, **ov)
                killed = cid in "\n".join(r.mismatches)
                results.append((name + f" -> {cid}", killed,
                                f"checks={r.checks} mismatches={len(r.mismatches)}"
                                + ("" if killed else f" :: NOT KILLED; got {r.mismatches[:3]}")))
            except SystemExit as e:
                results.append((name + f" -> {cid}", False, f"fixture error: {e}"))
            finally:
                # every mutated file is restored before the next scenario
                _restore_fixture(state)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    all_ok = True
    for name, passed, detail in results:
        print(f"[selftest-r12] {'PASS' if passed else 'FAIL'} {name}: {detail}")
        all_ok = all_ok and passed
    print(f"[selftest-r12] {'ALL PASS' if all_ok else 'FAILURES PRESENT'} "
          f"({len(results)} scenarios)")
    return 0 if all_ok else 1


def _apply_file_mutations(state, ov):
    """File-level mutations; returns the override dict for one gate pass.

    A probability swap without re-hashing the bundle must fail the sha256 pin; a
    swap WITH a re-hash must fail the analysis' Brier (the stored score no
    longer matches the committed probabilities). Every mutated file is restored
    by `_restore_fixture` before the next scenario.
    """
    kind = ov.get("file_mut")
    if kind in ("swap_pass", "vary_f2"):
        path = state["probs_path"]
        objs = [json.loads(l) for l in read_text(path).splitlines() if l.strip()]
        if kind == "swap_pass":
            objs[0]["p_pass"], objs[1]["p_pass"] = objs[1]["p_pass"], objs[0]["p_pass"]
        else:
            for o in objs:
                if o["arm"] == "T-DENSE" and o["pid"] == FIX2[1]:
                    o["p_pass"] = 0.99
        with open(path, "w", encoding="utf-8") as f:
            f.write(chr(10).join(json.dumps(o, separators=(",", ":")) for o in objs)
                    + chr(10))
    elif kind == "swap_sign":
        path = state["sign_path"]
        objs = [json.loads(l) for l in read_text(path).splitlines() if l.strip()]
        j = next((i for i, o in enumerate(objs)
                  if o["p_diffpos"] != objs[0]["p_diffpos"]), None)
        if j is None:
            raise SystemExit("fixture: sign-event probabilities are all identical")
        objs[0]["p_diffpos"], objs[j]["p_diffpos"] = (objs[j]["p_diffpos"],
                                                     objs[0]["p_diffpos"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(chr(10).join(json.dumps(o, separators=(",", ":")) for o in objs)
                    + chr(10))
    elif kind == "drop_pass":
        os.remove(state["probs_path"])
    elif kind == "drop_sign":
        os.remove(state["sign_path"])
    elif kind == "write_bundle":
        with open(os.path.join(state["dir"], "predictions-r12.md"), "a",
                  encoding="utf-8") as f:
            f.write(chr(10) + "corrupted after hashing" + chr(10))
    if ov.get("rehash_bundle"):
        rows = []
        for n in R12_REQUIRED_BUNDLE:
            full = os.path.join(state["dir"], n)
            if not os.path.isfile(full):
                continue
            rows.append(file_sha256(full) + "  corpus/evidence/round12-ladder/" + n)
        with open(state["sha"], "w", encoding="utf-8") as f:
            f.write(chr(10).join(rows) + chr(10))
    return ov


def _restore_fixture(state):
    """Reset every file the battery mutates back to the clean fixture bytes."""
    for name, text in state["clean_files"].items():
        with open(os.path.join(state["dir"], name), "w", encoding="utf-8") as f:
            f.write(text)
    stray = os.path.join(state["dir"], "predictions-r12.mutated.md")
    if os.path.isfile(stray):
        os.remove(stray)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest-r12", action="store_true",
                    help="build a synthetic round-12 tree; every mutation must be killed")
    ap.add_argument("--r12-jsonl", default=R12_JSONL)
    ap.add_argument("--r12-md", default=R12_MD)
    ap.add_argument("--r12-runlog", default=R12_RUNLOG)
    args = ap.parse_args(argv)
    if args.selftest_r12:
        bad = selftest_stats_r12()
        for b in bad:
            print(f"[selftest-r12] FAIL stats: {b}")
        print(f"[selftest-r12] {'PASS' if not bad else 'FAIL'} stats anchors "
              f"(Page's L / seq semantics / Brier-BSS / reliability / logistic Newton)")
        rc_stats = 1 if bad else 0
        return max(rc_stats, _run_r12_fixture())
    if not os.path.isfile(args.r12_jsonl):
        die(f"no round-12 evidence at {args.r12_jsonl} — run --selftest-r12 on a synthetic "
            f"tree, or grade after the landing")
    rep = Report()
    paths = {"r12_jsonl": args.r12_jsonl, "r12_md": args.r12_md,
             "r12_runlog": args.r12_runlog}
    check_r12_pins(paths, rep)
    recs = load_jsonl(args.r12_jsonl)
    grade_r12(recs, read_text(args.r12_md), read_text(args.r12_runlog), rep)
    check_r12_ordering(rep)
    for line in rep.mismatches:
        print(line)
    print(f"CHECKS n={rep.checks} mismatches={len(rep.mismatches)}")
    print("VERDICT: " + ("PASS — round-12 evidence fully re-derives offline"
                         if not rep.mismatches else "FAIL"))
    return 0 if not rep.mismatches else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:  # any unexpected crash is an input/env problem
        print(f"grader_r12_draft: INPUT ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
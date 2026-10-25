#!/usr/bin/env python3
"""Round-12 deterministic analysis engine — emission-granularity LADDER + transport.

Engine of record for round 12.  Promoted by L1 from
`corpus/evidence/round12-fleet/recompute_r12_draft.py` (draft by
ExecutorRecompute) with every binding adjudication of
`corpus/evidence/round12-fleet/INTEGRATOR-NOTES.md` §1 applied:

    cp corpus/evidence/round12-fleet/recompute_r12_draft.py \
       corpus/evidence/round12-ladder/recompute_r12.py

The module resolves its default paths from its own location *and* searches the
sibling `round12-ladder/` directory, so the promoted copy works unchanged.

Usage
-----
    python3 recompute_r12.py --selftest          # synthetic fixtures only
    python3 recompute_r12.py                     # results-r12.jsonl -> analysis_r12.md
    python3 recompute_r12.py --results P --out Q
    python3 recompute_r12.py P                   # positional results path

No network I/O of any kind, no `/proc`, no endpoint.  Deterministic: same input
bytes -> byte-identical output, independent of PYTHONHASHSEED (verified in
`--selftest` by re-running the file->md path under PYTHONHASHSEED unset, =1 and
=99 and comparing the bytes).

Promotion notes (INTEGRATOR-NOTES.md §1 rows applied at promotion)
------------------------------------------------------------------
 * 1a/1b/1c  Page's L kept in the sum-of-ranks form with per-block conditional
   null variance `5·S²_block` (k=4); ties use 1-based midranks; a pid enters E1
   only with final-turn records in all four ladder arms.  A selftest asserts
   the tied block `(1,2.5,2.5,4)` gives per-block variance 8.333… and that the
   no-tie form reduces to `n·k²(k+1)(k²-1)/144`.
 * 4c        ack compliance prints exactly FIVE lines, in §4 order; the empty
   `A-INC-ack` cell is not printed (critic D7).
 * 4d/§5      the three filed prediction artifacts are read by their PINNED
   names/schemas only (`predictions-r12-perproblem.jsonl` keys
   arm/family/pid/p_pass/base_arm/x_pid/delta_arm,
   `predictions-r12-signevents.jsonl` keys contrast/label/turns/family/pid/
   p_diffpos, run-level RL1-RL7 parsed from `predictions-r12.md` §5).  Absence,
   a sha256 disagreement with `prereg-bundle.sha256`, or a coverage shortfall
   fails hard with exit 2 — `UNDERPOWERED-INDETERMINATE` is reserved for the
   44/44 error-deletion floors.  There is no candidate-name search and no
   markdown-embedded fallback.
 * 4e/4f     `L=<f.1>` and `E_L=<f.1>` always one decimal, `var_L=<f.3>`.
 * 4h        the census line folds `descriptors_end` in and reads
   `2 descriptors`; a separate audit line names both record kinds.
 * 4i/4l     R2 branch labels are `REPEATS-r11` / `REPEATS-DOWNGRADED` /
   `DIRECTIONAL` / `DOES-NOT-REPEAT`, with a same-line `POINT-MATCHES-r11`
   suffix when `|diff-0.352| <= 0.15`; the point-prediction table gains one row
   per arm's predicted pass count from `predictions-r12.md` §2 and compares
   counts with r11's proportion convention.
 * 4j        both power floors are 44/44; error records are attributed through
   the runner's `job = [cell, fam, pid]` shape; unattributable records print
   `ERROR RECORD UNATTRIBUTED …`.
 * 4k        the ordering sentence also carries the two `run-script-hash` lines
   and the `main-run-launch` line.
 * §1 end    three event sets scored separately (416 pass / 304 sign / 7
   run-level = 727), BSS per set and pooled with the pooled pass BSS labelled
   `persistence + arm-rate transport`, calibration on pass events (primary) and
   all events (secondary), the degenerate conventions (`sd=0 -> t=+0.000
   p=1.0000` + `NOTE degenerate:`; `Var_L=0 -> z=+0.000 p=1.0000`; `b=c=0 ->
   p=1.0000`), the neutral-sign downgrade, `direction=<+1|-1|NEUTRAL>` on the
   E2 sign line, and the `Realized arm positions after deletion:` block.

Independent truth re-derivation (task item 4)
---------------------------------------------
`analyze` regenerates every family-1 problem from `seed = 3000 + pid*41` and
every family-2 problem from `seed = 5000 + pid*37`, compares `init`/`ops`/
`truth`/`tail_touched` against each `meta`/`meta2` record and every stored
graded `want` against the regenerated state at that turn, then re-parses every
graded record's `raw` through `extract_json_block` and re-grades it (`ok`,
`nwrong`; family 2 = |len diff| + positional mismatches, non-list ->
`len(want)`).  Any disagreement prints `TRUTH MISMATCH familyN …` or
`REGRADE MISMATCH …`.

Promotion verification (draft hand-off vs promoted engine)
---------------------------------------------------------
The promoted engine is exercised two ways: `--selftest` on synthetic fixtures
(statistics anchors, generator ports vs `probe_r12.py`, census arithmetic,
verdict branches, degenerate conventions, determinism) and a full run over the
committed `results-r12.jsonl` (4 114 records, 0 error records), whose output is
`analysis_r12.md` and whose stdout+stderr is `recompute-run.log`.  Every §5
stored line is emitted in the pinned byte format; the recomputed numbers live
in `analysis_r12.md`, not here.

Specification of record (never edited by this file)
---------------------------------------------------
`corpus/evidence/round12-ladder/probe_plan_r12.md`: §2.1/§2.2 arms and turn
sets, §2.3 endpoints E1-E6, §4 record schema + pinned totals, §5 stored-line
formats, the R1-R5 verdict rules, and the error-record contingency.

Statistics: stdlib only.  `_mean`, `_sd_sample`, `_betacf`, `betai`,
`t_two_sided_p`, `t_crit` are reused verbatim from
`corpus/evidence/round11-power/recompute_r11.py`; exact sign/McNemar come from
`math.comb`.  New: the tie-corrected Page statistic, the normal tail via
`math.erfc`, Brier/BSS/reliability, and damped-Newton logistic recalibration
(<=50 iterations, tol 1e-10).
"""

import argparse
import ast
import hashlib
import json
import math
import os
import re
import sys
import tempfile

# --------------------------------------------------------------------------
# paths (resolved from this file so the draft and its promoted copy behave
# identically; both the fleet draft dir and the ladder dir are searched)
# --------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(HERE)
_CANDIDATE_DIRS = [
    HERE,
    os.path.join(_PARENT, "round12-ladder"),
    os.path.join(_PARENT, "round12-fleet"),
]
LADDER_DIR = next(
    (d for d in _CANDIDATE_DIRS if os.path.exists(os.path.join(d, "probe_plan_r12.md"))),
    os.path.join(_PARENT, "round12-ladder"),
)

DEF_RESULTS = os.path.join(LADDER_DIR, "results-r12.jsonl")
DEF_OUT = os.path.join(LADDER_DIR, "analysis_r12.md")
DEF_PRED = os.path.join(LADDER_DIR, "predictions-r12.md")
DEF_BUNDLE = os.path.join(LADDER_DIR, "prereg-bundle.sha256")
DEF_ORDERING = os.path.join(LADDER_DIR, "ordering.log")
PROBE_R12 = os.path.join(LADDER_DIR, "probe_r12.py")
PREDICT_R12 = os.path.join(LADDER_DIR, "predict_r12.py")

# Pinned prediction-file paths (L1 §1 row "§5 probability-file interface":
# exact names, exact schemas, hard failure if absent; all three are inside the
# hashed bundle).  There is no candidate-name search and no markdown-embedded
# fallback any more.
DEF_PERPROB = os.path.join(LADDER_DIR, "predictions-r12-perproblem.jsonl")
DEF_SIGNEV = os.path.join(LADDER_DIR, "predictions-r12-signevents.jsonl")
PINNED_PRED_FILES = ("predictions-r12-perproblem.jsonl",
                     "predictions-r12-signevents.jsonl",
                     "predictions-r12.md")


class PredictionError(Exception):
    """Hard failure of the pinned prediction-file interface (exit 2).

    Raised on absence, a sha256 disagreement with `prereg-bundle.sha256`, or a
    coverage shortfall over the scored events.  `UNDERPOWERED-INDETERMINATE` is
    reserved for the 44/44 error-deletion floors (§2.3), never for a corrupted
    bundle.
    """

# --------------------------------------------------------------------------
# design constants (§2.1, §2.2, §4)
# --------------------------------------------------------------------------
F1_ARMS = ["A-INC", "A-CKPT4710", "A-CKPT710", "A-CKPT10", "A-MONO"]
LADDER_ARMS = F1_ARMS[:4]              # INC < 4710 < 710 < 10 (E1 order)
F2_ARMS = ["T-DENSE", "T-SPARSE"]
ALL_ARMS = F1_ARMS + F2_ARMS

FINAL_TURN = 10                        # every arm but the single-shot one
ARM_FINAL_TURN = {"A-MONO": 1}         # §2.1: the single shot is logged as turn 1

ARM_TURNS = {
    "A-INC": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "A-CKPT4710": [4, 7, 10],
    "A-CKPT710": [7, 10],
    "A-CKPT10": [10],
    "A-MONO": [1],
    "T-DENSE": [4, 7, 10],
    "T-SPARSE": [7, 10],
}
# ack turns (graded turns excluded); used by the synthetic fixture builder only
ACK_TURNS = {
    "A-CKPT4710": [1, 2, 3, 5, 6, 8, 9],
    "A-CKPT710": [1, 2, 3, 4, 5, 6, 8, 9],
    "A-CKPT10": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "T-DENSE": [1, 2, 3, 5, 6, 8, 9],
    "T-SPARSE": [1, 2, 3, 4, 5, 6, 8, 9],
}
# Ack-compliance audit cells: the FIVE cells that can carry records, in §4
# order.  `A-INC-ack` is empty by construction (§4: "INC grades every turn, so
# it emits no ack records") and is deliberately not printed -- L1 delta 2 pins
# exactly five lines.
ACK_CELLS = [
    "A-CKPT4710-ack", "A-CKPT710-ack", "A-CKPT10-ack",
    "T-DENSE-ack", "T-SPARSE-ack",
]
F1_ACK_BASE = ["A-CKPT4710", "A-CKPT710", "A-CKPT10"]      # §4: A-INC-ack is empty by construction
F2_ACK_BASE = ["T-DENSE", "T-SPARSE"]

# E3 adjacent gaps, in §5 print order: (label, A, B, turns) with diff = A - B
E3_GAPS = [("4710-INC", "A-CKPT4710", "A-INC", (4, 7, 10)),
           ("710-4710", "A-CKPT710", "A-CKPT4710", (7, 10)),
           ("10-710", "A-CKPT10", "A-CKPT710", (10,))]

def _shared_turns_table():
    """Per-arm "Mean nwrong (shared turns)" column of the §5 arm table.

    Definition used by this engine: the graded turns that participate in the
    arm's paired contrasts — E3's adjacent gaps (family-1 ladder, which
    includes E2's 710-4710 at {7,10}), E4 for the single-shot `A-MONO` (whose
    logged turn 1 IS its final state, §2.1), E5 for both family-2 arms.  It is
    derived from the contrast definitions, not from whichever bytes happen to
    be present, so the column is well defined even on a partial run.
    (probe_plan_r12.md §5 does not define this column; see the notes.)
    """
    table = {c: set() for c in ALL_ARMS}
    for _label, a_cell, b_cell, turns in E3_GAPS:
        table[a_cell] |= set(turns)
        table[b_cell] |= set(turns)
    table["A-MONO"] |= {ARM_FINAL_TURN["A-MONO"]}
    table["A-CKPT10"] |= {FINAL_TURN}
    table["T-DENSE"] |= {7, 10}
    table["T-SPARSE"] |= {7, 10}
    return {c: sorted(table[c]) for c in ALL_ARMS}


SHARED_TURNS = _shared_turns_table()

# The five per-problem sign-event contrasts of predictions-r12-signevents.jsonl
# (L1 delta 4): (contrast id, A, B, turns) with y = 1 iff mean(A) - mean(B) > 0
# and the filed probability P(diff > 0).  `turns=None` means the E4 final-turn
# pairing (A-MONO's logged turn 1 against A-CKPT10's turn 10).
SIGN_CONTRASTS = [
    ("E3a", "A-CKPT4710", "A-INC", (4, 7, 10)),
    ("E3b", "A-CKPT710", "A-CKPT4710", (7, 10)),
    ("E3c", "A-CKPT10", "A-CKPT710", (10,)),
    ("E4", "A-MONO", "A-CKPT10", None),
    ("E5", "T-SPARSE", "T-DENSE", (7, 10)),
]
RL_IDS = ["RL1", "RL2", "RL3", "RL4", "RL5", "RL6", "RL7"]
# Reported BSS splits (predictions-r12.md §"Event sets scored at close")
BSS_SPLITS = [("family1-replicate", ["A-CKPT4710", "A-CKPT710"]),
              ("family1-novel", ["A-INC", "A-CKPT10", "A-MONO"]),
              ("family2", ["T-DENSE", "T-SPARSE"])]

SEED_F1 = "3000+pid*41"
SEED_F2 = "5000+pid*37"

# Filed power floors -- L1 delta 3: MC exact-t power at dz=0.4288 gives
# 0.810 at n=44 and 0.791 at n=42 (power_r12.py output, pasted into
# power_analysis_r12.md), so BOTH families floor at 44.
F1_MIN_N = 44
F2_MIN_N = 44
R11_DIFF_REF = 0.352                   # plan R2: r11's measured diff
R11_DIFF_TOL = 0.15
ALPHA = 0.05

# descriptor sentence, verbatim from probe_plan_r12.md §1 (carried by every
# derived claim)
DESCRIPTOR_SENTENCE = (
    "*single served unit — Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS under the "
    "stack pinned in the run's `descriptors` record (q4_0 KV cache, "
    "`--kv-unified`, `--parallel 2`, custom non-upstream chat template); no "
    "cross-model generalization.*"
)

REL_BIN_EDGES = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
CALIB_MAX_ITER = 50
CALIB_TOL = 1e-10
LOGIT_EPS = 1e-6                       # p is clipped to [eps, 1-eps] before logit

# --------------------------------------------------------------------------
# generators: family 1 (verbatim r11 port) and family 2 (§2.2 port)
# --------------------------------------------------------------------------
import random  # noqa: E402  (kept next to the ports it serves)

KEYS = ["nails", "bolts", "screws", "washers", "hinges"]


def sim_apply(state, op):
    """Verbatim probe_r11.py / grader.py family-1 op semantics."""
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


def op_str(op):
    if op[0] in ("SET", "ADD", "SUB", "NEW"):
        return "%s %s %s" % (op[0], op[1], op[2])
    if op[0] == "MOV":
        return "MOV %s %s" % (op[1], op[2])
    return "DEL %s" % op[1]


def tail_touched(ops, mid=7):
    t = {o[1] for o in ops[mid:]}
    t |= {o[2] for o in ops[mid:] if o[0] == "MOV"}
    return t


def gen_problem(seed, _depth=0):
    """Iterative port of probe_r11.py:gen_problem (reject -> seed + 977).

    Byte-identical semantics to the recursive r11 form and to grader.py's
    iterative port ('identical to analyze.py's gen_problem_exact which matched
    all r8 metas').  The recursion is unrolled so a pathological seed cannot
    blow the interpreter stack; the retry bound is reported, never silent.
    """
    depth = _depth
    while depth <= 4096:
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
            depth += 1
            continue
        return init, ops, depth
    raise RuntimeError("gen_problem: retry bound exceeded for seed %d" % seed)


def states_along(init, ops, n=None):
    """Verbatim probe_r11.py:states_along."""
    s, out = dict(init), []
    for op in (ops if n is None else ops[:n]):
        s = sim_apply(s, op)
        out.append(s)
    return out


def grade_state(got, want):
    """Verbatim probe_r11.py/grader.py family-1 grading: (exact, n_wrong_keys)."""
    if not isinstance(got, dict):
        return False, len(want)
    wrong = sum(1 for k in set(got) | set(want) if got.get(k) != want.get(k))
    return got == want, wrong


# ---- family 2 ------------------------------------------------------------
SEQ_TOKENS = ["alpha", "beta", "gamma", "delta", "eps", "zeta", "kappa", "lambda"]
# probe_r12.py:TOKVOCAB — identical 8-token vocabulary


def seq_apply(state, op):
    """§2.2 op semantics on an ordered token list (0-based indices); verbatim
    port of probe_r12.py:sim_apply2 (MOV/INS insert at index j of the
    SHORTENED list, clamped)."""
    s = list(state)
    k = op[0]
    if k == "APP":
        s.append(op[1])
    elif k == "INS":
        s.insert(min(op[1], len(s)), op[2])
    elif k == "DEL":
        del s[op[1]]
    elif k == "SET":
        s[op[1]] = op[2]
    elif k == "MOV":
        t = s.pop(op[1])
        s.insert(min(op[2], len(s)), t)
    elif k == "SWP":
        i, j = op[1], op[2]
        s[i], s[j] = s[j], s[i]
    elif k == "REV":
        i, j = op[1], op[2]
        s[i:j + 1] = list(reversed(s[i:j + 1]))
    return s


def tail_positions(ops, mid=7):
    """Positions (int operands) named by ops[mid:] — verbatim port of
    probe_r12.py:tail_positions; §2.2 requires the last 3 ops to name >= 2
    distinct positions."""
    t = set()
    for o in ops[mid:]:
        for x in o[1:]:
            if isinstance(x, int):
                t.add(x)
    return t


def gen_seq_problem(seed, _depth=0):
    """Family-2 generator — byte-exact PORT of probe_r12.py:gen_seq_problem
    (sha256 1871697f5c3410adf3c17297138e76416cdeb63194038324eec067abe6b90662),
    used only when the shipped module cannot be loaded.  `--selftest` asserts
    that this port reproduces the shipped generator's (init, ops) for all 48
    family-2 seeds whenever `probe_r12.py` is present.

    rng consumption, op distribution (roll thresholds 0.16/0.32/0.48/0.62/
    0.76/0.88), the `n < 4` guards, the MOV i != j resample, the REV gap >= 2
    rule and the accept condition ({DEL,MOV,REV} present and tail_positions
    >= 2) all mirror the shipped source exactly.  The recursion is unrolled
    (seed += 977) to a bounded loop; returns (init, ops, retries).
    """
    depth = _depth
    while depth <= 4096:
        rng = random.Random(seed)
        init = rng.sample(SEQ_TOKENS, 6)
        seq, ops = list(init), []
        while len(ops) < 10:
            n = len(seq)
            roll = rng.random()
            if roll < 0.16:
                op = ("APP", rng.choice(SEQ_TOKENS))
            elif roll < 0.32:
                op = ("INS", rng.randrange(n + 1), rng.choice(SEQ_TOKENS))
            elif roll < 0.48:
                if n < 4:
                    continue
                op = ("DEL", rng.randrange(n))
            elif roll < 0.62:
                op = ("SET", rng.randrange(n), rng.choice(SEQ_TOKENS))
            elif roll < 0.76:
                if n < 4:
                    continue
                i = rng.randrange(n)
                j = rng.randrange(n)
                if i == j:
                    continue
                op = ("MOV", i, j)
            elif roll < 0.88:
                if n < 4:
                    continue
                i, j = rng.sample(range(n), 2)
                op = ("SWP", i, j)
            else:
                if n < 4:
                    continue
                i, j = sorted(rng.sample(range(n), 2))
                if j - i < 2:
                    continue
                op = ("REV", i, j)
            seq = seq_apply(seq, op)
            ops.append(op)
        kinds = {o[0] for o in ops}
        if not {"DEL", "MOV", "REV"} <= kinds or len(tail_positions(ops)) < 2:
            seed += 977
            depth += 1
            continue
        return init, ops, depth
    raise RuntimeError("gen_seq_problem: retry bound exceeded for seed %d" % seed)


def seq_states(init, ops, n=None):
    s, out = list(init), []
    for op in (ops if n is None else ops[:n]):
        s = seq_apply(s, op)
        out.append(s)
    return out


def grade_seq(got, want):
    """§2.2 family-2 grading; the non-list/parse-failure convention is
    `ok=False, nwrong=len(want)` (mirrors grade_state's non-dict branch)."""
    if not isinstance(got, list):
        return False, len(want)
    if got == want:
        return True, 0
    m = min(len(got), len(want))
    mism = sum(1 for i in range(m) if got[i] != want[i])
    return False, abs(len(got) - len(want)) + mism


def family_of_pid(pid):
    """Design pid ranges (§2.1/§2.2) — a fallback only; meta/meta2 decide."""
    if 201 <= pid <= 264:
        return 1
    if 401 <= pid <= 448:
        return 2
    return 0


def _want_state(cell, turn, ops, states):
    """The state a graded record's `want` should hold.

    `A-MONO` is the single-shot arm: its logged `turn` is 1 but the emitted
    state is the FINAL state (all ops applied, §2.1).  Every other arm's `turn`
    is the 1-based op index.  `None` means the record is out of range.
    """
    if cell == "A-MONO":
        return states[-1] if states else None
    if turn is None or turn < 1 or turn > len(ops):
        return None
    return states[turn - 1]


# --------------------------------------------------------------------------
# sandboxed import of the shipped generators
# --------------------------------------------------------------------------
def _sandboxed_probe_namespace(path):
    """Execute only the side-effect-free top level of `probe_r12.py`.

    The shipped probe module opens its own results log at import time
    (`LOGF = open(...)`) and `os.makedirs(OUT)`; a plain import would touch the
    filesystem.  This keeps FunctionDef/ClassDef/Import/ImportFrom plus
    constant-valued assignments (function bodies need e.g. `KEYS`, `SYSTEM`,
    `RULES`) and drops any assignment whose value calls something.
    """
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src)
    keep = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                             ast.Import, ast.ImportFrom)):
            keep.append(node)
        elif isinstance(node, ast.Assign):
            if not any(isinstance(n, ast.Call) for n in ast.walk(node.value)):
                keep.append(node)
    mod = ast.Module(body=keep, type_ignores=[])
    ns = {"__name__": "probe_r12_sandboxed"}
    exec(compile(mod, path, "exec"), ns)
    return ns


def load_generators():
    """-> (dict with 'gen_problem'/'gen_seq_problem'/'gen_seq_problem_source'
    , provenance string).  Falls back to this file's ports on any failure."""
    info = {"gen_problem": gen_problem, "gen_seq_problem": gen_seq_problem,
            "gen_seq_problem_source": "port(recompute_r12_draft.py)",
            "gen_problem_source": "port(recompute_r12_draft.py)",
            "sha256": None, "path": PROBE_R12, "error": None}
    if not os.path.exists(PROBE_R12):
        info["error"] = "probe_r12.py absent"
        return info
    try:
        with open(PROBE_R12, "rb") as fh:
            info["sha256"] = hashlib.sha256(fh.read()).hexdigest()
        ns = _sandboxed_probe_namespace(PROBE_R12)
    except Exception as exc:  # never fatal: the audit reports, the run proceeds
        info["error"] = "%s: %s" % (type(exc).__name__, exc)
        return info
    gp = ns.get("gen_problem")
    if callable(gp):
        info["gen_problem"] = gp
        info["gen_problem_source"] = "probe_r12.py"
    gs = ns.get("gen_seq_problem")
    if callable(gs):
        info["gen_seq_problem"] = gs
        info["gen_seq_problem_source"] = "probe_r12.py"
    return info


def call_gen(fn, seed):
    """Normalise a generator's return: (init, ops).  Tolerates an extra
    retry-count/exactness element."""
    out = fn(seed)
    if not isinstance(out, tuple) or len(out) < 2:
        raise ValueError("generator returned %r" % (out,))
    return out[0], [list(o) for o in out[1]]


# --------------------------------------------------------------------------
# ports of the r11 parse helper (byte-faithful with grader.py / probe_r11.py)
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
# statistics (stdlib only; r11 helpers verbatim, new helpers below them)
# --------------------------------------------------------------------------
def _mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def _sd_sample(xs):
    """Sample standard deviation, denominator n-1 (r11 verbatim)."""
    n = len(xs)
    if n < 2:
        return float("nan")
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


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
    if not math.isfinite(t):
        return float("nan")
    return betai(df / 2.0, 0.5, df / (df + t * t))


def t_crit(df, alpha=ALPHA):
    """Positive t quantile, two-sided tail alpha, by bisection on the betai
    tail (r11 verbatim)."""
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if t_two_sided_p(mid, df) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def normal_two_sided_p(z):
    """Two-sided standard-normal tail 2*(1-Phi(|z|)) = erfc(|z|/sqrt(2))."""
    return math.erfc(abs(z) / math.sqrt(2.0))


def binom_two_sided(k, n):
    """Exact two-sided sign-test p: 2*min(P[X<=k], P[X>=k]), X~Bin(n,1/2),
    capped at 1.0 (r11 verbatim, `math.comb` only)."""
    if n <= 0:
        return 1.0
    pl = sum(math.comb(n, i) for i in range(0, k + 1)) / 2.0 ** n
    pr = sum(math.comb(n, i) for i in range(k, n + 1)) / 2.0 ** n
    return min(1.0, 2.0 * min(pl, pr))


def exact_sign_p(wins, losses):
    """Sign test over the discordant pairs only (ties omitted, r9/r11 rule)."""
    return binom_two_sided(wins, wins + losses)


def mcnemar_exact(b, c):
    """Exact two-sided McNemar p (r11 verbatim; `math.comb` only)."""
    n = b + c
    if n <= 0:
        return 1.0
    probs = [math.comb(n, i) / 2.0 ** n for i in range(n + 1)]
    thr = probs[min(b, c)]
    return min(1.0, sum(p for p in probs if p <= thr + 1e-15))


# ---- new: Page's ordered-trend test (tie-corrected) ----------------------
def midranks(vals):
    """1-based midranks: equal values share the average of their ranks."""
    n = len(vals)
    order = sorted(range(n), key=lambda i: vals[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + 1 + j + 1) / 2.0
        for t in range(i, j + 1):
            ranks[order[t]] = avg
        i = j + 1
    return ranks


def page_test(blocks):
    """Page's L for ordered treatments in n randomized blocks (k arms).

    L = sum_j j * R_j with R_j the SUM of within-block ranks (midranks for
    ties) of arm j over the n blocks; E_L = n*k*(k+1)^2/4.

    Tie-corrected variance, derived per block: for a uniformly random
    permutation of the block's fixed midrank multiset onto the fixed
    coefficients c_j = j,

        Var(sum_j c_j r_j) = SS_c * SS_r / (k-1),
        SS_c = sum_j (j - (k+1)/2)^2,  SS_r = sum_j (r_j - (k+1)/2)^2

    (the standard random-permutation variance identity).  Summing over the
    independent blocks gives var_L; with no ties SS_r = k(k^2-1)/12 and this
    reduces exactly to the classical n*k^2*(k+1)*(k^2-1)/144.  Ties shrink
    SS_r and therefore the variance; E_L is unchanged (midranks preserve the
    block rank sum).

    Returns dict(L, E_L, var_L, z, p, direction, n, blocks_used, L_mean_rank).
    z and p are invariant under the alternative mean-rank scaling
    (L' = L/n, E_L' = k(k+1)^2/4, var_L' = var_L/n^2) that §2.3's `R-bar`
    notation suggests — so R1 cannot depend on that reading.
    """
    n = len(blocks)
    k = len(blocks[0]) if n else 0
    out = {"n": n, "k": k, "L": float("nan"), "E_L": float("nan"),
           "var_L": float("nan"), "z": float("nan"), "p": float("nan"),
           "direction": "n/a", "L_mean_rank": float("nan"), "blocks_used": n}
    if n == 0 or k < 2:
        return out
    ss_c = sum((j - (k + 1) / 2.0) ** 2 for j in range(1, k + 1))
    L = 0.0
    var = 0.0
    for vals in blocks:
        r = midranks(vals)
        L += sum(j * r[j - 1] for j in range(1, k + 1))
        ss_r = sum((x - (k + 1) / 2.0) ** 2 for x in r)
        var += ss_c * ss_r / (k - 1)
    e_l = n * k * (k + 1) ** 2 / 4.0
    # Degenerate convention (L1 delta 7): var_L = 0 -> z = +0.000, p = 1.0000;
    # NaN is never printed for a degenerate but well-formed block matrix.
    degenerate = var <= 0.0
    if degenerate:
        z, p = 0.0, 1.0
    else:
        z = (L - e_l) / math.sqrt(var)
        p = normal_two_sided_p(z)
    out.update({
        "L": L, "E_L": e_l, "var_L": var, "z": z, "p": p,
        # L1 §1 row 4e/§2.3: direction is defined by `L > E_L` (z > 0) ->
        # increasing severity with decreasing density; `L < E_L` -> decreasing;
        # exact equality (z == 0) -> neutral.  §5 stores
        # `direction=<increasing|decreasing|neutral>`.
        "direction": ("neutral" if L == e_l
                      else ("increasing" if L > e_l else "decreasing")),
        "L_mean_rank": L / n, "degenerate": degenerate,
    })
    return out


def paired_contrast(pairs):
    """pairs: list of (pid, a_value, b_value) -> paired stats on diffs a - b.

    Returns dict(n, mean, sd, se, t, df, p, ci_lo, ci_hi, wins, losses, ties,
    sign_p, sign_dir, t_dir, pids).
    """
    diffs = [a - b for _, a, b in pairs]
    n = len(diffs)
    wins = sum(1 for d in diffs if d > 0)
    losses = sum(1 for d in diffs if d < 0)
    ties = n - wins - losses
    res = {"n": n, "pids": [p for p, _, _ in pairs], "mean": float("nan"),
           "sd": float("nan"), "se": float("nan"), "t": float("nan"),
           "df": n - 1, "p": float("nan"), "ci_lo": float("nan"),
           "ci_hi": float("nan"), "wins": wins, "losses": losses,
           "ties": ties, "sign_p": exact_sign_p(wins, losses),
           "degenerate": False,
           # wins == losses -> NEUTRAL (0); R2 counts 0 as DISAGREEMENT
           # (L1 delta 7 / predictions-r12.md §6)
           "sign_dir": 0 if wins == losses else (1 if wins > losses else -1)}
    if n == 0:
        res["t_dir"] = 0
        return res
    res["mean"] = _mean(diffs)
    res["t_dir"] = 0 if res["mean"] == 0 else (1 if res["mean"] > 0 else -1)
    if n > 1:
        res["sd"] = _sd_sample(diffs)
        res["se"] = res["sd"] / math.sqrt(n)
        if res["se"] > 0:
            res["t"] = res["mean"] / res["se"]
            res["p"] = t_two_sided_p(res["t"], n - 1)
        else:
            # Degenerate convention (L1 delta 7): zero-variance diffs print
            # t=+0.000 and p=1.0000, never NaN.
            res["t"] = 0.0
            res["p"] = 1.0
            res["degenerate"] = True
        crit = t_crit(n - 1)
        res["ci_lo"] = res["mean"] - crit * res["se"]
        res["ci_hi"] = res["mean"] + crit * res["se"]
    return res


def mcnemar_from_pairs(pairs):
    """pairs: (pid, a_ok, b_ok) -> (b, c, p) with b = a pass & b fail."""
    b = sum(1 for _, x, y in pairs if x and not y)
    c = sum(1 for _, x, y in pairs if (not x) and y)
    return b, c, mcnemar_exact(b, c)


# ---- new: forecast scoring ----------------------------------------------
def brier(ps, ys):
    if not ps:
        return float("nan")
    return _mean([(p - y) ** 2 for p, y in zip(ps, ys)])


def bss(ps, ys, clim):
    """1 - BS / BS_clim; clim is the per-event climatology probability."""
    bs = brier(ps, ys)
    bs_ref = brier(clim, ys)
    if not math.isfinite(bs) or not math.isfinite(bs_ref) or bs_ref <= 0.0:
        return float("nan")
    return 1.0 - bs / bs_ref


def _clip_p(p):
    return min(1.0 - LOGIT_EPS, max(LOGIT_EPS, p))


def logit(p):
    q = _clip_p(p)
    return math.log(q / (1.0 - q))


def _loglik(a, b, xs, ys):
    ll = 0.0
    for x, y in zip(xs, ys):
        eta = a + b * x
        ll += y * eta - math.log1p(math.exp(-abs(eta))) - max(0.0, eta) - min(0.0, eta)
    return ll


def calibrate(ps, ys):
    """Logistic recalibration logit(p_hat) = a + b*logit(p) by damped Newton.

    Start (a, b) = (0, 1) (the identity-calibration prior).  Each iteration
    solves the 2x2 Newton system on the log-likelihood, then halves the step
    until the log-likelihood does not decrease (damping; the objective is
    strictly concave so this always progresses).  Stop when the *undamped*
    Newton step satisfies max(|da|, |db|) < 1e-10, or after 50 iterations
    (plan §5: "damped Newton, max 50 iterations, tol 1e-10, deterministic").

    Returns dict(slope, intercept, iters, converged, n, note).
    """
    xs = [logit(p) for p in ps]
    out = {"slope": float("nan"), "intercept": float("nan"), "iters": 0,
           "converged": False, "n": len(ps), "note": ""}
    if len(ps) < 3 or len(set(ys)) < 2 or len(set(xs)) < 2:
        out["note"] = "insufficient variation"
        return out
    a, b = 0.0, 1.0
    ll = _loglik(a, b, xs, ys)
    for it in range(1, CALIB_MAX_ITER + 1):
        out["iters"] = it
        g_a = g_b = 0.0
        h_aa = h_ab = h_bb = 0.0
        for x, y in zip(xs, ys):
            phat = 1.0 / (1.0 + math.exp(-(a + b * x)))
            r = y - phat
            w = phat * (1.0 - phat)
            g_a += r
            g_b += x * r
            h_aa += w
            h_ab += w * x
            h_bb += w * x * x
        det = h_aa * h_bb - h_ab * h_ab
        if det == 0.0 or not math.isfinite(det):
            out["note"] = "singular Hessian"
            break
        # Newton step on the (concave) log-likelihood: delta = H^{-1} g
        da = (h_bb * g_a - h_ab * g_b) / det
        db = (-h_ab * g_a + h_aa * g_b) / det
        if not (math.isfinite(da) and math.isfinite(db)):
            out["note"] = "non-finite step"
            break
        step = 1.0
        while step > 1e-12:
            a2, b2 = a + step * da, b + step * db
            ll2 = _loglik(a2, b2, xs, ys)
            if ll2 >= ll:
                break
            step /= 2.0
        a, b = a + step * da, b + step * db
        ll = _loglik(a, b, xs, ys)
        if max(abs(da), abs(db)) < CALIB_TOL:
            out["converged"] = True
            break
    out["slope"], out["intercept"] = b, a
    return out


def reliability(ps, ys, edges=None):
    """5-bin reliability table: inclusive lower / exclusive upper edges, last
    bin closed.  Empty bins keep their edges with n=0 and n/a statistics."""
    edges = edges or REL_BIN_EDGES
    rows = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        idx = [k for k, p in enumerate(ps)
               if (p >= lo and (p < hi or (i == len(edges) - 2 and p <= hi)))]
        sel = [ps[k] for k in idx]
        ys_sel = [ys[k] for k in idx]
        rows.append({"lo": lo, "hi": hi, "n": len(sel),
                     "pred": _mean(sel) if sel else float("nan"),
                     "obs": _mean(ys_sel) if sel else float("nan")})
    return rows


# --------------------------------------------------------------------------
# formatting helpers — unavailable numerics render the literal `n/a`
# --------------------------------------------------------------------------
def _fmt(x, spec):
    if x is None:
        return "n/a"
    try:
        if not math.isfinite(x):
            return "n/a"
    except TypeError:
        return "n/a"
    return spec % x


def _fmt_int(x):
    if x is None:
        return "n/a"
    try:
        if not math.isfinite(x):
            return "n/a"
    except TypeError:
        return "n/a"
    if abs(x - round(x)) < 1e-9:
        return "%d" % int(round(x))
    return "%.1f" % x


def _sign_dir_literal(d):
    """§5 E2 sign line: `direction=<+1|-1|NEUTRAL>` (critic D4)."""
    return "+1" if d > 0 else ("-1" if d < 0 else "NEUTRAL")


# --------------------------------------------------------------------------
# registration files (r11 verbatim)
# --------------------------------------------------------------------------
def _read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _parse_bundle(text):
    entries = []
    for line in text.splitlines():
        m = re.match(r"^([0-9a-f]{64})\s+(\S+)$", line.strip())
        if m:
            entries.append((m.group(1), m.group(2)))
    return entries


def _parse_version(text):
    for line in text.splitlines():
        m = re.match(r"^bundle sha256 file (\S+) \((v\d+)", line.strip())
        if m:
            return m.group(2)
    return None


def _parse_ordering(text):
    """ordering.log: pre/post-hash timestamps, the launch line, and the
    run-script-hash lines (L1 §1 row 4k)."""
    times = {}
    for line in text.splitlines():
        m = re.match(r"^(pre-hash|post-hash)\s+(\S+)$", line.strip())
        if m:
            times[m.group(1)] = m.group(2)
            continue
        m = re.match(r"^main-run-launch\s+(\S+)$", line.strip())
        if m:
            times["main-run-launch"] = m.group(1)
    return times


def _parse_run_script_hashes(text):
    """ordering.log `run-script-hash <ts> <sha256> <name> (note)` -> list."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^run-script-hash\s+(\S+)\s+([0-9a-f]{64})\s+(\S+)", line.strip())
        if m:
            out.append((m.group(1), m.group(3), m.group(2)))
    return out


# --------------------------------------------------------------------------
# input parsers for the filed predictions / probabilities
# --------------------------------------------------------------------------
def read_perproblem(path):
    """`predictions-r12-perproblem.jsonl` (pinned schema, L1 delta 5).

    One JSON object per (arm, pid) final-turn pass event with keys
    `arm` (string, e.g. "A-CKPT10" -- NOT `cell`), `family` (1|2), `pid` (int),
    `p_pass` (float), `base_arm`, `x_pid` (float or null for family 2).
    Returns ({(arm, pid): p_pass}, notes, error).
    """
    probs, notes = {}, []
    if not path or not os.path.exists(path):
        return probs, notes, "absent: %s" % path
    with open(path, "r", encoding="utf-8") as fh:
        for i, ln in enumerate(fh, 1):
            ln = ln.strip()
            if not ln:
                continue
            try:
                rec = json.loads(ln)
            except Exception as exc:
                notes.append("line %d: unparsed JSON (%s)" % (i, type(exc).__name__))
                continue
            if not isinstance(rec, dict):
                notes.append("line %d: not an object" % i)
                continue
            arm, pid, p = rec.get("arm"), rec.get("pid"), rec.get("p_pass")
            if arm is None or pid is None or p is None:
                notes.append("line %d: missing arm/pid/p_pass" % i)
                continue
            try:
                probs[(str(arm), int(pid))] = float(p)
            except Exception:
                notes.append("line %d: non-numeric p_pass %r" % (i, p))
    if not probs and not notes:
        return probs, notes, "no records in %s" % path
    return probs, notes, None


def read_signevents(path):
    """`predictions-r12-signevents.jsonl` (pinned schema, L1 delta 5).

    Keys `contrast` ("E3a"|"E3b"|"E3c"|"E4"|"E5"), `label`, `turns`, `family`,
    `pid` (int), `p_diffpos` (float).  Returns
    ({(contrast, pid): p_diffpos}, notes, error).
    """
    probs, notes = {}, []
    if not path or not os.path.exists(path):
        return probs, notes, "absent: %s" % path
    with open(path, "r", encoding="utf-8") as fh:
        for i, ln in enumerate(fh, 1):
            ln = ln.strip()
            if not ln:
                continue
            try:
                rec = json.loads(ln)
            except Exception as exc:
                notes.append("line %d: unparsed JSON (%s)" % (i, type(exc).__name__))
                continue
            if not isinstance(rec, dict):
                notes.append("line %d: not an object" % i)
                continue
            cid, pid, p = rec.get("contrast"), rec.get("pid"), rec.get("p_diffpos")
            if cid is None or pid is None or p is None:
                notes.append("line %d: missing contrast/pid/p_diffpos" % i)
                continue
            try:
                probs[(str(cid), int(pid))] = float(p)
            except Exception:
                notes.append("line %d: non-numeric p_diffpos %r" % (i, p))
    if not probs and not notes:
        return probs, notes, "no records in %s" % path
    return probs, notes, None


def _md_cells(line):
    """Split a markdown table row on UNESCAPED `|` (predictions-r12.md §5 has
    `\\|diff - 0.352\\|` inside a cell), dropping the outer bars and unescaping."""
    st = line.strip()
    if st.startswith("|"):
        st = st[1:]
    if st.endswith("|") and not st.endswith("\\|"):
        st = st[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", st)]


_P_CELL_RE = re.compile(r"^(?:0|1|0?\.\d+|1\.0+)$")


def read_runlevel(pred_text):
    """Run-level probabilities RL1-RL7 from the `predictions-r12.md` §5 table.

    The md's sha256 is in the bundle, so this parse is pinned.  The RL3 event
    cell itself embeds raw `|` characters (`(|diff - 0.352| <= 0.15)`), so the
    row is split on unescaped pipes and the probability is taken as the UNIQUE
    cell that looks like a bare probability, scanning from the right and
    skipping the trailing justification cell.  Zero or two-or-more candidates
    is a hard failure (`PredictionError` -> exit 2) with the row printed --
    the engine never guesses.  Returns ([(id, label, p)], notes).
    """
    rows, notes = [], []
    if not pred_text:
        return rows, ["predictions-r12.md absent"]
    for ln in pred_text.splitlines():
        st = ln.strip()
        if not st.startswith("|"):
            continue
        cells = [c.replace("**", "") for c in _md_cells(st)]
        if not cells or cells[0] not in RL_IDS:
            continue
        cands = [i for i in range(1, len(cells) - 1) if _P_CELL_RE.match(cells[i])]
        if len(cands) != 1:
            raise PredictionError(
                "run-level row %s: %d probability cells (want exactly 1) in %r"
                % (cells[0], len(cands), st))
        p_idx = cands[0]
        rows.append((cells[0], " ".join(cells[1:p_idx]).strip(),
                     float(cells[p_idx])))
    seen = {r[0] for r in rows}
    for rid in RL_IDS:
        if rid not in seen:
            notes.append("run-level row %s missing" % rid)
    return rows, notes


def read_predictor_runlevel(path):
    """`predict_r12.py:RUNLEVEL_EVENTS` literals (id -> P), read-only, by AST.

    The predictor is inside the hashed bundle; this cross-checks the parsed
    `predictions-r12.md` §5 values against the script that wrote them.
    Returns (dict, error-or-None).
    """
    if not path or not os.path.exists(path):
        return {}, "predict_r12.py absent"
    try:
        tree = ast.parse(_read_text(path))
    except SyntaxError as exc:
        return {}, "predict_r12.py unparsable: %s" % exc
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "RUNLEVEL_EVENTS":
                    try:
                        val = ast.literal_eval(node.value)
                    except Exception as exc:
                        return {}, "RUNLEVEL_EVENTS is not a literal: %s" % exc
                    out = {}
                    for item in val:
                        if isinstance(item, (list, tuple)) and len(item) >= 3:
                            try:
                                out[str(item[0])] = float(item[2])
                            except Exception:
                                pass
                    return out, None
    return {}, "RUNLEVEL_EVENTS not found"


_NUM_CELL_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?$")
_INT_CELL_RE = re.compile(r"^\d+$")
_TURNS_CELL_RE = re.compile(r"^\{[\d,\s]+\}$")
_E_LABEL_RE = re.compile(r"^(?:E3a|E3b|E3c|E2|E4|E5)\b")


def parse_point_predictions(text):
    """Point predictions from `predictions-r12.md`.

    Two pinned tables are read (§2 `| arm | predicted passes | of n |` ->
    kind "passcount"; §4 `| quantity | predicted | derivation |` -> kind
    "contrast") and every other table is rejected by shape:

      * the predicted value is located as the FIRST numeric cell, not by a
        fixed column index, so a label that itself carries raw `|` characters
        (the §5 RL3 hazard) still parses; everything before it is the label;
      * §3's per-problem sign-event rows are rejected because they carry a
        standalone `{turns}` cell and their P column is not a point value;
      * a passcount row additionally needs an integer `of n` cell.

    Returns a list of dicts {kind, label, raw, pred, denom}.
    """
    rows = []
    if not text:
        return rows
    for ln in text.splitlines():
        st = ln.strip()
        if not st.startswith("|"):
            continue
        cells = [c.replace("**", "").replace("`", "").strip() for c in _md_cells(st)]
        if len(cells) < 2:
            continue
        # §3's per-problem sign-event table is `| contrast | label | turns | P |
        # source |`: its turns column is a standalone `{...}` spec or the
        # literal `final`, and its P column is not a point value -- reject the
        # shape so only §2's pass-count and §4's point tables survive.
        if len(cells) >= 5 and (_TURNS_CELL_RE.match(cells[2] or "")
                                or cells[2] == "final"):
            continue
        if any(_TURNS_CELL_RE.match(c) for c in cells[1:]):
            continue
        k = next((i for i in range(1, len(cells)) if _NUM_CELL_RE.match(cells[i])), None)
        if k is None:
            continue
        label = " ".join(c for c in cells[:k] if c).strip()
        pred = float(cells[k])
        if label in ALL_ARMS:
            denom = next((int(c) for c in cells[k + 1:] if _INT_CELL_RE.match(c)), None)
            if denom:
                rows.append({"kind": "passcount", "label": label,
                             "raw": cells[k], "pred": pred, "denom": denom})
            continue
        if _E_LABEL_RE.match(label):
            rows.append({"kind": "contrast", "label": label,
                         "raw": cells[k], "pred": pred, "denom": None})
    return rows


def score_row(label, raw, val, obs):
    """Map one filed point prediction to the observed quantity it forecasts.

    Returns (predicted_used, observed_used, predicted_display,
    observed_display, quantity_name) or None when the label matches nothing the
    engine measures (such a row renders `n/a` — the engine never guesses).

    Two row kinds (predictions-r12.md §2 and §4):
      * an arm's predicted pass count (label = the arm name, `of n` column) is
        compared as a PROPORTION — r11's convention — against that arm's
        observed `<passes>/<n>`;
      * a §4 contrast row (`E3a`/`E2`/`E3b`/`E3c`/`E4`/`E5`) is compared in
        `nwrong` units against the recomputed endpoint.
    `Abs error` is the absolute difference of the two values actually compared.
    """
    low = label.lower()

    def count_row(arm):
        denom = obs.get("passes_denom", {}).get(arm)
        passes = obs.get("passes_final", {}).get(arm)
        if not denom or passes is None:
            return None
        if "/" in raw:
            num, den = raw.split("/", 1)
            pred_prop = float(num) / float(den)
        else:
            pred_prop = val / denom if val > 1.0 else val
        return (pred_prop, passes / denom, raw, "%d/%d" % (passes, denom),
                "final passes %s" % arm)

    if low in [a.lower() for a in ALL_ARMS]:
        return count_row(label)
    for key, qname, needles in (
            ("e3a_diff", "E3a gap (4710 - INC, {4,7,10})", ("e3a",)),
            ("e3c_diff", "E3c gap (10 - 710, {10})", ("e3c",)),
            ("e2_diff", "E2/E3b gap (710 - 4710, {7,10})",
             ("e2", "e3b", "severity")),
            ("e4_diff", "E4 diff (MONO - CKPT10, final)", ("e4", "mono")),
            ("e5_diff", "E5 diff (SPARSE - DENSE, {7,10})",
             ("e5", "sparse", "dense", "transport"))):
        if any(n in low for n in needles) and obs.get(key) is not None:
            return (val, obs[key], raw, "%+.3f" % obs[key], qname)
    if ("page" in low or "trend" in low) and obs.get("e1_p") is not None:
        return (val, obs["e1_p"], raw, "%.4f" % obs["e1_p"], "E1 Page two-sided p")
    return None


# --------------------------------------------------------------------------
# analysis
# --------------------------------------------------------------------------
def analyze(recs, bundle_text, ordering_text, results_name, pred_text="",
            pred_name="predictions-r12.md", perprob=None, signprob=None,
            runprob_rows=None, probmeta=None, gens=None, probs_notes=None,
            probs_error=None, strict=False):
    """Return the full analysis_r12.md text.  Pure function of its arguments.

    `perprob` maps (arm, pid) -> filed P(pass); `signprob` maps
    (contrast, pid) -> filed P(diff > 0); `runprob_rows` is [(id, label, p)]
    for RL1-RL7; `probmeta` carries the three pinned files' names/sha256s.

    `strict=True` (the real run, when `prereg-bundle.sha256` pins the three
    artifacts) turns a probability coverage shortfall into `PredictionError`
    -> exit 2 instead of a silent partial score.
    """
    gens = gens or {"gen_problem": gen_problem, "gen_seq_problem": gen_seq_problem,
                    "gen_problem_source": "port", "gen_seq_problem_source": "port",
                    "sha256": None, "path": PROBE_R12, "error": "not supplied"}
    L = []

    # ---------------- census ------------------------------------------------
    by_cell = {}
    for r in recs:
        c = r.get("cell")
        if c is not None:
            by_cell[c] = by_cell.get(c, 0) + 1
    descriptors = by_cell.get("descriptors", 0)
    descriptors_end = by_cell.get("descriptors_end", 0)
    metas_1 = [r for r in recs if r.get("cell") == "meta"]
    metas_2 = [r for r in recs if r.get("cell") == "meta2"]
    graded = [r for r in recs if r.get("cell") in ALL_ARMS and "nwrong" in r]
    acks = [r for r in recs if str(r.get("cell", "")).endswith("-ack")]
    fillers = [r for r in recs if r.get("cell") == "filler"]
    errors = [r for r in recs if r.get("cell") == "error"]
    census_cells = {c: by_cell.get(c, 0) for c in ALL_ARMS}

    # graded records per cell (raw re-parse / re-grade audit)
    graded_by_cell = {c: sorted([r for r in graded if r.get("cell") == c],
                                key=lambda r: (r.get("pid", -1), r.get("turn", -1)))
                      for c in ALL_ARMS}

    # ---------------- truth rebuild (independent of the stored `truth`) ----
    truth_audit = {"f1": [], "f2": [], "f1_ok": 0, "f2_ok": 0, "unchecked": []}

    def _cmp_meta(rec, fam, gen, states_fn, grade_note):
        pid = rec.get("pid")
        seed = rec.get("seed")
        if pid is None or seed is None:
            truth_audit["unchecked"].append("family%d pid=%r seed=%r" % (fam, pid, seed))
            return
        try:
            init, ops = call_gen(gen, seed)
            states = states_fn(init, ops)
        except Exception as exc:
            truth_audit["unchecked"].append(
                "family%d pid=%s: generator raised %s: %s" % (fam, pid, type(exc).__name__, exc))
            return
        bad = []
        if rec.get("init") != init:
            bad.append("init")
        if rec.get("ops") != ops:
            bad.append("ops")
        # `meta.truth` / `meta2.truth` store the FULL state sequence (one state
        # per op), not just the final state.
        if rec.get("truth") != states:
            bad.append("truth")
        if fam == 1 and "tail_touched" in rec:
            if sorted(rec["tail_touched"]) != sorted(tail_touched(ops)):
                bad.append("tail_touched")
        if bad:
            truth_audit["f%d" % fam].append("pid %s: %s mismatch" % (pid, "+".join(bad)))
        else:
            truth_audit["f%d_ok" % fam] += 1
        # graded `want` integrity for this pid
        for cell in (F1_ARMS if fam == 1 else F2_ARMS):
            for r in graded_by_cell.get(cell, []):
                if r.get("pid") != pid:
                    continue
                t = r.get("turn")
                want_expected = _want_state(cell, t, ops, states)
                if want_expected is None:
                    continue
                if r.get("want") != want_expected:
                    truth_audit["f%d" % fam].append(
                        "pid %s %s turn %s: stored want != regenerated state" % (pid, cell, t))
        return

    for rec in sorted(metas_1, key=lambda r: r.get("pid", -1)):
        _cmp_meta(rec, 1, gens["gen_problem"], states_along, "f1")
    for rec in sorted(metas_2, key=lambda r: r.get("pid", -1)):
        _cmp_meta(rec, 2, gens["gen_seq_problem"], seq_states, "f2")

    # ---------------- re-parse + re-grade every graded record --------------
    regrade = {"checked": 0, "mismatch": [], "parse_fail": 0, "finish_length": 0}
    ok_by = {}
    for r in sorted(graded, key=lambda r: (r.get("cell", ""), r.get("pid", -1),
                                           r.get("turn", -1))):
        cell = r.get("cell")
        regrade["checked"] += 1
        if r.get("finish") == "length":
            regrade["finish_length"] += 1
        got = extract_json_block(r.get("raw", "") or "")
        if got is None:
            regrade["parse_fail"] += 1
        if cell in F2_ARMS:
            ok2, nwrong2 = grade_seq(got, r.get("want"))
        else:
            ok2, nwrong2 = grade_state(got, r.get("want"))
        ok_by[(cell, r.get("pid"), r.get("turn"))] = (ok2, nwrong2)
        if ok2 != bool(r.get("ok")) or nwrong2 != r.get("nwrong"):
            regrade["mismatch"].append(
                "%s pid=%s turn=%s raw=(ok=%s,nwrong=%s) rebuilt=(ok=%s,nwrong=%s)"
                % (cell, r.get("pid"), r.get("turn"), r.get("ok"), r.get("nwrong"),
                   ok2, nwrong2))

    # ---------------- error-record contingency ----------------------------
    excluded = {1: [], 2: []}
    err_unattributed = []
    for e in errors:
        pid = e.get("pid")
        fam = e.get("family")
        if pid is None:
            blob = " ".join(str(e.get(k, "")) for k in ("job", "err", "error", "msg"))
            for m in re.finditer(r"\b(\d{2,4})\b", blob):
                cand = int(m.group(1))
                f = family_of_pid(cand)
                if f:
                    pid, fam = cand, f
                    break
        if pid is not None:
            fam = fam or family_of_pid(pid)
        if pid is None or not fam:
            err_unattributed.append(json.dumps(e, sort_keys=True)[:200])
            continue
        if pid not in excluded[fam]:
            excluded[fam].append(pid)
    for fam in (1, 2):
        excluded[fam] = sorted(excluded[fam])

    f1_pids_all = sorted({r.get("pid") for r in metas_1 if r.get("pid") is not None})
    f2_pids_all = sorted({r.get("pid") for r in metas_2 if r.get("pid") is not None})
    if not f1_pids_all:
        f1_pids_all = sorted({r.get("pid") for r in graded if r.get("cell") in F1_ARMS
                              and r.get("pid") is not None})
    if not f2_pids_all:
        f2_pids_all = sorted({r.get("pid") for r in graded if r.get("cell") in F2_ARMS
                              and r.get("pid") is not None})
    f1_pids = [p for p in f1_pids_all if p not in excluded[1]]
    f2_pids = [p for p in f2_pids_all if p not in excluded[2]]

    # ---------------- per-cell nwrong index -------------------------------
    nwrong_by = {}
    ok_by_stored = {}
    for r in graded:
        cell, pid, turn = r.get("cell"), r.get("pid"), r.get("turn")
        nwrong_by.setdefault((cell, pid), {})[turn] = r.get("nwrong")
        ok_by_stored.setdefault((cell, pid), {})[turn] = bool(r.get("ok"))

    def final_turn(cell):
        return ARM_FINAL_TURN.get(cell, FINAL_TURN)

    def cell_pids(cell):
        return f2_pids if cell in F2_ARMS else f1_pids

    def final_recs(cell):
        t = final_turn(cell)
        return [r for r in graded_by_cell.get(cell, [])
                if r.get("turn") == t and r.get("pid") in set(cell_pids(cell))]

    shared_turns = SHARED_TURNS   # from the contrast definitions (see above)

    # ---------------- per-arm table ---------------------------------------
    arm_stats = {}
    for cell in ALL_ARMS:
        fr = final_recs(cell)
        passes = sum(1 for r in fr if r.get("ok"))
        mean_final = _mean([r.get("nwrong") for r in fr])
        vals = []
        for pid in cell_pids(cell):
            pid_vals = nwrong_by.get((cell, pid))
            if not pid_vals:
                continue
            turns = shared_turns[cell]
            if all(t in pid_vals for t in turns):
                vals.append(_mean([pid_vals[t] for t in turns]))
        arm_stats[cell] = {"passes": passes, "n": len(fr), "mean_final": mean_final,
                           "mean_shared": _mean(vals), "shared_n": len(vals)}

    # ---------------- E1: Page's ordered-trend test -----------------------
    blocks = []
    for pid in f1_pids:
        vals = []
        for arm in LADDER_ARMS:
            d = nwrong_by.get((arm, pid))
            if not d or final_turn(arm) not in d:
                vals = []
                break
            vals.append(d[final_turn(arm)])
        if len(vals) == len(LADDER_ARMS):
            blocks.append(vals)
    page = page_test(blocks)

    # ---------------- E2 / E3: paired ladder contrasts --------------------
    def gap_pairs(a_cell, b_cell, turns):
        pairs = []
        for pid in f1_pids:
            da = nwrong_by.get((a_cell, pid))
            db = nwrong_by.get((b_cell, pid))
            if not da or not db:
                continue
            if all(t in da for t in turns) and all(t in db for t in turns):
                pairs.append((pid, _mean([da[t] for t in turns]),
                              _mean([db[t] for t in turns])))
        return pairs

    e2 = paired_contrast(gap_pairs("A-CKPT710", "A-CKPT4710", (7, 10)))
    mcn_pairs = []
    for pid in f1_pids:
        oa = ok_by_stored.get(("A-CKPT4710", pid))
        ob = ok_by_stored.get(("A-CKPT710", pid))
        ta, tb = final_turn("A-CKPT4710"), final_turn("A-CKPT710")
        if oa and ob and ta in oa and tb in ob:
            mcn_pairs.append((pid, oa[ta], ob[tb]))
    mcn_b, mcn_c, mcn_p = mcnemar_from_pairs(mcn_pairs)

    e3 = []
    for label, a_cell, b_cell, turns in E3_GAPS:
        st = paired_contrast(gap_pairs(a_cell, b_cell, turns))
        e3.append((label, turns, st))

    # ---------------- E4: batching dissociation ---------------------------
    e4_pairs = []
    for pid in f1_pids:
        dm = nwrong_by.get(("A-MONO", pid))
        dc = nwrong_by.get(("A-CKPT10", pid))
        if not dm or not dc:
            continue
        tm, tc = final_turn("A-MONO"), final_turn("A-CKPT10")
        if tm in dm and tc in dc:
            e4_pairs.append((pid, dm[tm], dc[tc]))
    e4 = paired_contrast(e4_pairs)
    e4_mcn_pairs = []
    for pid in f1_pids:
        om = ok_by_stored.get(("A-MONO", pid))
        oc = ok_by_stored.get(("A-CKPT10", pid))
        tm, tc = final_turn("A-MONO"), final_turn("A-CKPT10")
        if om and oc and tm in om and tc in oc:
            e4_mcn_pairs.append((pid, om[tm], oc[tc]))
    e4_b, e4_c, e4_mcn_p = mcnemar_from_pairs(e4_mcn_pairs)

    # ---------------- E5: transport ---------------------------------------
    e5_pairs = []
    for pid in f2_pids:
        ds = nwrong_by.get(("T-SPARSE", pid))
        dd = nwrong_by.get(("T-DENSE", pid))
        if not ds or not dd:
            continue
        if all(t in ds for t in (7, 10)) and all(t in dd for t in (7, 10)):
            e5_pairs.append((pid, _mean([ds[7], ds[10]]), _mean([dd[7], dd[10]])))
    e5 = paired_contrast(e5_pairs)

    # ---------------- E6: three scored event sets (L1 delta 4) ------------
    # (1) pass events: one per (arm, pid) final-turn graded record (416 at full n)
    pass_events = []
    for cell in ALL_ARMS:
        for r in final_recs(cell):
            pass_events.append(((cell, r.get("pid")), 1 if r.get("ok") else 0))

    # (2) per-problem sign events: one per (contrast, pid), y = 1 iff diff > 0
    sign_pairs = {}
    for cid, a_cell, b_cell, turns in SIGN_CONTRASTS:
        if cid == "E4":
            sign_pairs[cid] = e4_pairs
        elif cid == "E5":
            sign_pairs[cid] = e5_pairs
        else:
            sign_pairs[cid] = gap_pairs(a_cell, b_cell, turns)
    sign_events = []
    for cid, _a, _b, _t in SIGN_CONTRASTS:
        for pid, a, b in sign_pairs[cid]:
            sign_events.append(((cid, pid), 1 if (a - b) > 0 else 0))

    perprob = perprob or {}
    signprob = signprob or {}
    runprob_rows = runprob_rows or []

    def _score(events, probs_map, group_fn):
        """Score one event set.

        The climatological forecast is each event's own group base rate
        (per-arm rate for pass events, per-contrast observed win rate for sign
        events, the set's observed rate for the run-level set), computed over
        the SAME events -- excluded pids never enter either the score or its
        climatology.
        """
        ps, ys, groups, unmapped = [], [], [], []
        for key, y in events:
            if key not in probs_map:
                unmapped.append(str(key))
                continue
            p = probs_map[key]
            if not (0.0 <= p <= 1.0):
                unmapped.append("%s (p=%r out of range)" % (key, p))
                continue
            ps.append(p)
            ys.append(y)
            groups.append(group_fn(key))
        gsum, gcnt = {}, {}
        for g, y in zip(groups, ys):
            gsum[g] = gsum.get(g, 0) + y
            gcnt[g] = gcnt.get(g, 0) + 1
        clim = [gsum[g] / gcnt[g] for g in groups]
        per_group = {}
        group_n = {}
        group_rate = {}
        for g in sorted(gcnt):
            idx = [k for k, gg in enumerate(groups) if gg == g]
            per_group[g] = brier([ps[k] for k in idx], [ys[k] for k in idx])
            group_n[g] = gcnt[g]
            group_rate[g] = gsum[g] / gcnt[g]
        return {"n": len(ps), "events": len(events), "ps": ps, "ys": ys,
                "groups": groups, "clim": clim, "unmapped": unmapped,
                "brier": brier(ps, ys) if ps else None,
                "bss": bss(ps, ys, clim) if ps else None,
                "per_group": per_group, "group_n": group_n,
                "group_rate": group_rate}

    pass_set = _score(pass_events, perprob, lambda k: k[0])
    sign_set = _score(sign_events, signprob, lambda k: k[0])
    calib = calibrate(pass_set["ps"], pass_set["ys"]) if pass_set["ps"] else {
        "slope": None, "intercept": None, "iters": 0, "converged": False,
        "n": 0, "note": "no probabilities"}
    # the 5-bin table is always emitted (empty bins render n/a) so that §5's
    # "(x5)" shape holds even when no probability was filed
    rel = reliability(pass_set["ps"], pass_set["ys"])

    # ---------------- audits ----------------------------------------------
    G = len(graded)
    ack_audit = []
    for cell in ACK_CELLS:
        rows = [r for r in acks if r.get("cell") == cell]
        okc = sum(1 for r in rows if str(r.get("raw", "")).strip().lower().startswith("ok"))
        ack_audit.append((cell, okc, len(rows)))

    # realized arm-position counts, post-deletion, derived from the file order
    # (the order each pid's cells first appear in the append-only jsonl)
    first_idx = {}
    for i, r in enumerate(recs):
        c, pid = r.get("cell"), r.get("pid")
        if c in F1_ARMS and pid is not None and (pid, c) not in first_idx:
            first_idx[(pid, c)] = i
    pos_counts = {}
    for pid in f1_pids:
        have = [(first_idx[(pid, c)], c) for c in F1_ARMS if (pid, c) in first_idx]
        for pos, (_i, c) in enumerate(sorted(have), 1):
            pos_counts.setdefault(pos, {})
            pos_counts[pos][c] = pos_counts[pos].get(c, 0) + 1
    desc_order_counts = None
    for d in recs:
        if d.get("cell") == "descriptors":
            for k in sorted(d):
                if "arm_order" in k and isinstance(d[k], dict):
                    desc_order_counts = (k, d[k])
            break

    # ---------------- verdicts --------------------------------------------
    n1, n2 = len(f1_pids), len(f2_pids)
    under_n = (n1 < F1_MIN_N) or (n2 < F2_MIN_N)
    under_ep = (e2["n"] < F1_MIN_N) or (e5["n"] < F2_MIN_N)
    underpowered = under_n or under_ep
    under_why = []
    if n1 < F1_MIN_N:
        under_why.append("family1 n=%d < %d" % (n1, F1_MIN_N))
    if n2 < F2_MIN_N:
        under_why.append("family2 n=%d < %d" % (n2, F2_MIN_N))
    if e2["n"] < F1_MIN_N:
        under_why.append("E2 paired n=%d < %d" % (e2["n"], F1_MIN_N))
    if e5["n"] < F2_MIN_N:
        under_why.append("E5 paired n=%d < %d" % (e5["n"], F2_MIN_N))
    under_text = "UNDERPOWERED-INDETERMINATE"

    # R1 ladder
    p_ok = page["p"] is not None and math.isfinite(page["p"]) and page["p"] < ALPHA
    inc = page["direction"] == "increasing"
    all_gaps_pos = len(e3) == 3 and all(st["mean"] is not None and st["mean"] > 0
                                        for _, _, st in e3)
    if p_ok and inc:
        r1 = "LADDER ESTABLISHED"
        r1_why = ("Page p=%.4f (<0.05: yes) AND direction=%s -> LADDER ESTABLISHED"
                  % (page["p"], page["direction"]))
    elif (not p_ok) and all_gaps_pos:
        r1 = "LADDER DIRECTIONAL"
        r1_why = ("Page p=%s (>=0.05: yes) AND all three E3 gaps > 0 -> LADDER DIRECTIONAL"
                  % _fmt(page["p"], "%.4f"))
    else:
        r1 = "LADDER NOT SUPPORTED"
        r1_why = ("Page p=%s (>=0.05: %s), direction=%s, all E3 gaps > 0: %s -> LADDER NOT SUPPORTED"
                  % (_fmt(page["p"], "%.4f"), "yes" if not p_ok else "no",
                     page["direction"], "yes" if all_gaps_pos else "no"))

    # R2 repeatability (L1 delta 9: renamed -- identical problems and seeds plus
    # llama.cpp multi-slot non-determinism mean this is a REPEAT, not an
    # independent replication).  wins == losses is NEUTRAL and counts as
    # DISAGREEMENT, so it downgrades.
    d2, p2v = e2["mean"], e2["p"]
    sig_ok2 = e2["sign_dir"] != 0 and e2["sign_dir"] == e2["t_dir"]
    if d2 > 0 and p2v is not None and math.isfinite(p2v) and p2v < ALPHA and sig_ok2:
        r2 = "REPEATS-r11"
        r2_why = ("diff=%+.3f (>0: yes), p=%s (<0.05: yes), sign dir=%+d == t dir=%+d -> REPEATS-r11"
                  % (d2, _fmt(p2v, "%.4f"), e2["sign_dir"], e2["t_dir"]))
    elif d2 > 0 and p2v is not None and math.isfinite(p2v) and p2v < ALPHA:
        r2 = "REPEATS-DOWNGRADED"
        r2_why = ("diff=%+.3f (>0: yes), p=%s (<0.05: yes), sign dir=%+d (%s) != t dir=%+d -> REPEATS-DOWNGRADED"
                  % (d2, _fmt(p2v, "%.4f"), e2["sign_dir"],
                     "NEUTRAL" if e2["sign_dir"] == 0 else "opposite", e2["t_dir"]))
    elif d2 > 0:
        r2 = "DIRECTIONAL"
        r2_why = ("diff=%+.3f (>0: yes), p=%s (>=0.05: yes) -> DIRECTIONAL"
                  % (d2, _fmt(p2v, "%.4f")))
    else:
        r2 = "DOES-NOT-REPEAT"
        r2_why = "diff=%+.3f (<=0) -> DOES-NOT-REPEAT" % d2
    point_match = d2 is not None and math.isfinite(d2) and abs(d2 - R11_DIFF_REF) <= R11_DIFF_TOL
    if point_match:
        r2 = "%s; additionally POINT-MATCHES-r11 (|diff - %.3f| = %.3f <= %.2f)" % (
            r2, R11_DIFF_REF, abs(d2 - R11_DIFF_REF), R11_DIFF_TOL)
        r2_why += "; |diff - %.3f| = %.3f <= %.2f -> additionally POINT-MATCHES-r11" % (
            R11_DIFF_REF, abs(d2 - R11_DIFF_REF), R11_DIFF_TOL)

    # R3 batching
    d4, p4 = e4["mean"], e4["p"]
    if d4 > 0 and p4 is not None and math.isfinite(p4) and p4 < ALPHA:
        r3 = "DISSOCIATION ESTABLISHED"
        r3_why = "diff=%+.3f (>0: yes), p=%s (<0.05: yes) -> DISSOCIATION ESTABLISHED" % (d4, _fmt(p4, "%.4f"))
    elif d4 > 0:
        r3 = "DISSOCIATION DIRECTIONAL"
        r3_why = "diff=%+.3f (>0: yes), p=%s (>=0.05: yes) -> DISSOCIATION DIRECTIONAL" % (d4, _fmt(p4, "%.4f"))
    else:
        r3 = "DISSOCIATION FALSIFIED"
        r3_why = "diff=%+.3f (<=0) -> DISSOCIATION FALSIFIED" % d4

    # R4 transport
    d5, p5 = e5["mean"], e5["p"]
    if d5 > 0 and p5 is not None and math.isfinite(p5) and p5 < ALPHA:
        r4 = "TRANSPORTS"
        r4_why = "diff=%+.3f (>0: yes), p=%s (<0.05: yes) -> TRANSPORTS" % (d5, _fmt(p5, "%.4f"))
    elif d5 > 0:
        r4 = "TRANSPORT DIRECTIONAL"
        r4_why = "diff=%+.3f (>0: yes), p=%s (>=0.05: yes) -> TRANSPORT DIRECTIONAL" % (d5, _fmt(p5, "%.4f"))
    else:
        r4 = "TRANSPORT NOT SUPPORTED"
        r4_why = "diff=%+.3f (<=0) -> TRANSPORT NOT SUPPORTED" % d5

    # R5 forecast: the pinned §5 `E6 BSS vs arm climatology` value (pass-event
    # arm climatology) plus the PRIMARY calibration slope on the 416 pass events
    bss_pass = pass_set["bss"]
    bss_ok = bss_pass is not None and math.isfinite(bss_pass) and bss_pass > 0
    sl = calib["slope"]
    sl_ok = sl is not None and math.isfinite(sl) and 0.5 <= sl <= 2.0
    if not pass_set["ps"]:
        r5 = "FORECAST UNSCORED"
        r5_why = ("no pass event carried a filed probability (coverage 0/%d) -> R5 not scoreable"
                  % len(pass_events))
    elif bss_ok and sl_ok:
        r5 = "FORECAST SKILLED"
        r5_why = ("BSS=%s (>0: yes), calibration slope=%s in [0.5, 2.0]: yes -> FORECAST SKILLED"
                  % (_fmt(bss_pass, "%+.4f"), _fmt(sl, "%+.4f")))
    elif bss_ok:
        r5 = "FORECAST SKILLED-MISCALIBRATED"
        r5_why = ("BSS=%s (>0: yes), calibration slope=%s in [0.5, 2.0]: no -> FORECAST SKILLED-MISCALIBRATED"
                  % (_fmt(bss_pass, "%+.4f"), _fmt(sl, "%+.4f")))
    else:
        r5 = "FORECAST UNSKILLED"
        r5_why = "BSS=%s (<=0) -> FORECAST UNSKILLED" % _fmt(bss_pass, "%+.4f")
    # (§5 probability-file interface, L1 §1: a coverage shortfall fails hard
    # with exit 2 -- raised where the three event sets are built -- it never
    # downgrades to `UNDERPOWERED-INDETERMINATE`, which is reserved for the
    # 44/44 error-deletion floors.)

    verdicts = [("R1 ladder", r1, r1_why), ("R2 repeat", r2, r2_why),
                ("R3 batching", r3, r3_why), ("R4 transport", r4, r4_why),
                ("R5 forecast", r5, r5_why)]
    if underpowered:
        verdicts = [(name, under_text,
                     "%s; %s" % (why, "underpowered: " + "; ".join(under_why)))
                    for name, _, why in verdicts]
        under_note = "underpowered: " + "; ".join(under_why)
    else:
        under_note = ""

    # ---------------- run-level events (RL1-RL7) --------------------------
    # Outcomes are taken from the REPORTED (post-contingency) verdicts plus the
    # three numeric clauses; see the notes for this reading.
    vtext = {name: text for name, text, _why in verdicts}
    rl_out = {
        "RL1": 1 if vtext.get("R1 ladder") == "LADDER ESTABLISHED" else 0,
        "RL2": 1 if vtext.get("R2 repeat", "").startswith("REPEATS-r11") else 0,
        "RL3": 1 if (d2 is not None and math.isfinite(d2)
                     and abs(d2 - R11_DIFF_REF) <= R11_DIFF_TOL) else 0,
        "RL4": 1 if all_gaps_pos else 0,
        "RL5": 1 if vtext.get("R3 batching") == "DISSOCIATION ESTABLISHED" else 0,
        "RL6": 1 if vtext.get("R4 transport") == "TRANSPORTS" else 0,
        "RL7": 1 if vtext.get("R5 forecast") == "FORECAST SKILLED" else 0,
    }
    run_events = [(rid, rl_out[rid]) for rid in RL_IDS]
    run_probs = {rid: p for rid, _lab, p in runprob_rows}
    run_set = _score(run_events, run_probs, lambda k: "RL")

    # Hard failure (exit 2) on a coverage shortfall over the scored events:
    # the three prediction artifacts are inside the hashed bundle, so a
    # shortfall means a corrupted tree, not a small sample.
    if strict:
        short = []
        for label, st, total in (("pass", pass_set, len(pass_events)),
                                 ("sign", sign_set, len(sign_events)),
                                 ("runlevel", run_set, len(run_events))):
            if st["n"] != total:
                short.append("%s %d/%d" % (label, st["n"], total))
        if short:
            raise PredictionError(
                "probability coverage shortfall: %s (events with no filed probability)"
                % "; ".join(short))

    # ---------------- pooled aggregates over the three sets ---------------
    all_ps = pass_set["ps"] + sign_set["ps"] + run_set["ps"]
    all_ys = pass_set["ys"] + sign_set["ys"] + run_set["ys"]
    all_clim = pass_set["clim"] + sign_set["clim"] + run_set["clim"]
    pooled_n = len(all_ps)
    total_events = len(pass_events) + len(sign_events) + len(run_events)
    pooled_brier = brier(all_ps, all_ys) if all_ps else None
    pooled_bss = bss(all_ps, all_ys, all_clim) if all_ps else None
    calib_all = calibrate(all_ps, all_ys) if all_ps else {
        "slope": None, "intercept": None, "iters": 0, "converged": False,
        "n": 0, "note": "no probabilities"}
    split_bss = {}
    split_n = {}
    for name, arms in BSS_SPLITS:
        idx = [k for k, g in enumerate(pass_set["groups"]) if g in arms]
        split_n[name] = len(idx)
        if idx:
            split_bss[name] = bss([pass_set["ps"][k] for k in idx],
                                  [pass_set["ys"][k] for k in idx],
                                  [pass_set["clim"][k] for k in idx])
        else:
            split_bss[name] = None
    unmapped = (["pass:" + m for m in pass_set["unmapped"]]
                + ["sign:" + m for m in sign_set["unmapped"]]
                + ["run:" + m for m in run_set["unmapped"]])

    # ---------------- point-prediction scoring ----------------------------
    e3_by_label = {label: st for label, _turns, st in e3}
    obs = {
        "e1_p": page["p"], "e2_diff": e2["mean"], "e4_diff": e4["mean"],
        "e5_diff": e5["mean"],
        "e3a_diff": e3_by_label["4710-INC"]["mean"],
        "e3c_diff": e3_by_label["10-710"]["mean"],
        "passes_final": {c: arm_stats[c]["passes"] for c in ALL_ARMS},
        "passes_denom": {c: arm_stats[c]["n"] for c in ALL_ARMS},
    }
    pred_rows = parse_point_predictions(pred_text)
    probmeta = probmeta or {}

    # ======================= document =====================================
    L.append("# Round 12 analysis — powered emission-granularity ladder + transport")
    L.append("")
    L.append("Generated by `corpus/evidence/round12-ladder/recompute_r12.py` "
             "— stdlib only, deterministic, no network I/O — from `%s`. Primary endpoint: "
             "Page's ordered-trend test over the four-arm family-1 density ladder "
             "`A-INC` (10 checkpoints) > `A-CKPT4710` (3) > `A-CKPT710` (2) > `A-CKPT10` (1)."
             % results_name)
    L.append("")
    L.append(DESCRIPTOR_SENTENCE)
    L.append("")
    L.append("## Census and per-arm totals")
    L.append("")
    L.append("%s contains %d descriptors, %d meta, %d meta2, %d graded, %d ack, "
             "%d fillers, %d error records"
             % (results_name, descriptors + descriptors_end, len(metas_1), len(metas_2), G,
                len(acks), len(fillers), len(errors)))
    L.append("")
    L.append("| Arm | Final passes / n | Mean final nwrong | Mean nwrong (shared turns) |")
    L.append("|---|---:|---:|---:|")
    for cell in ALL_ARMS:
        st = arm_stats[cell]
        L.append("| %s | %d/%d | %s | %s |"
                 % (cell, st["passes"], st["n"], _fmt(st["mean_final"], "%.3f"),
                    _fmt(st["mean_shared"], "%.3f")))
    L.append("")
    # L and E_L print one decimal (L is half-integral under ties), var_L three
    # (L1 delta 6)
    L.append("E1 Page trend: L=%s E_L=%s var_L=%s z=%s two-sided p=%s direction=%s"
             % (_fmt(page["L"], "%.1f"), _fmt(page["E_L"], "%.1f"),
                _fmt(page["var_L"], "%.3f"), _fmt(page["z"], "%+.3f"),
                _fmt(page["p"], "%.4f"), page["direction"]))
    L.append("E2 paired diff (710 - 4710, {7,10}): %s sd %s n=%d"
             % (_fmt(e2["mean"], "%+.3f"), _fmt(e2["sd"], "%.3f"), e2["n"]))
    L.append("E2 paired t: t=%s, df=%d, two-sided p=%s"
             % (_fmt(e2["t"], "%+.3f"), e2["df"], _fmt(e2["p"], "%.4f")))
    L.append("E2 95%% CI: [%s, %s]"
             % (_fmt(e2["ci_lo"], "%.3f"), _fmt(e2["ci_hi"], "%.3f")))
    L.append("E2 exact sign: wins=%d losses=%d ties=%d two-sided p=%s direction=%s"
             % (e2["wins"], e2["losses"], e2["ties"], _fmt(e2["sign_p"], "%.4f"),
                _sign_dir_literal(e2["sign_dir"])))
    L.append("E2 McNemar final passes: b=%d c=%d two-sided p=%s"
             % (mcn_b, mcn_c, _fmt(mcn_p, "%.4f")))
    L.append("E3 adjacent gaps: " + "; ".join(
        "%s {%s} %s p=%s" % (label, ",".join(str(t) for t in turns),
                             _fmt(st["mean"], "%+.3f"), _fmt(st["p"], "%.4f"))
        for label, turns, st in e3))
    L.append("E4 batching diff (MONO - CKPT10, final): %s sd %s n=%d t=%s p=%s sign W/L/T=%d/%d/%d"
             % (_fmt(e4["mean"], "%+.3f"), _fmt(e4["sd"], "%.3f"), e4["n"],
                _fmt(e4["t"], "%+.3f"), _fmt(e4["p"], "%.4f"),
                e4["wins"], e4["losses"], e4["ties"]))
    L.append("E5 transport diff (SPARSE - DENSE, {7,10}): %s sd %s n=%d t=%s p=%s sign W/L/T=%d/%d/%d"
             % (_fmt(e5["mean"], "%+.3f"), _fmt(e5["sd"], "%.3f"), e5["n"],
                _fmt(e5["t"], "%+.3f"), _fmt(e5["p"], "%.4f"),
                e5["wins"], e5["losses"], e5["ties"]))
    L.append("E6 events: pass=%d sign=%d runlevel=%d total=%d "
             "(excluded pids dropped from score and climatology)"
             % (len(pass_events), len(sign_events), len(run_events),
                len(pass_events) + len(sign_events) + len(run_events)))
    L.append("E6 Brier pass: pooled=%s (N=%d); per-arm %s"
             % (_fmt(pass_set["brier"], "%.4f"), pass_set["n"],
                " ".join("%s=%s" % (c, _fmt(pass_set["per_group"].get(c), "%.4f"))
                         for c in ALL_ARMS)))
    L.append("E6 Brier sign: pooled=%s (N=%d); per-contrast %s"
             % (_fmt(sign_set["brier"], "%.4f"), sign_set["n"],
                " ".join("%s=%s" % (cid, _fmt(sign_set["per_group"].get(cid), "%.4f"))
                         for cid, _a, _b, _t in SIGN_CONTRASTS)))
    L.append("E6 Brier runlevel: pooled=%s (N=%d)"
             % (_fmt(run_set["brier"], "%.4f"), run_set["n"]))
    # §2.3 requires "Brier per set + pooled"; §5's line list names only the three
    # per-set lines, so the pooled-over-all-727 line is an addition the gate pins
    # (INTEGRATOR-NOTES.md §1). analysis_r12.md is NOT a bundle member, so adding
    # a line post-run breaks no hash.
    L.append("E6 Brier all scored events: pooled=%s (N=%d)"
             % (_fmt(pooled_brier, "%.4f"), pooled_n))
    L.append("E6 BSS pass vs arm climatology: pooled=%s [persistence + arm-rate transport]; "
             "family1-replicate=%s (N=%d); family1-novel=%s (N=%d); family2=%s (N=%d)"
             % (_fmt(bss_pass, "%+.4f"),
                _fmt(split_bss.get("family1-replicate"), "%+.4f"),
                split_n.get("family1-replicate", 0),
                _fmt(split_bss.get("family1-novel"), "%+.4f"),
                split_n.get("family1-novel", 0),
                _fmt(split_bss.get("family2"), "%+.4f"),
                split_n.get("family2", 0)))
    L.append("E6 BSS sign=%s runlevel=%s pooled-all-727=%s"
             % (_fmt(sign_set["bss"], "%+.4f"), _fmt(run_set["bss"], "%+.4f"),
                _fmt(pooled_bss, "%+.4f")))
    L.append("E6 calibration (pass events): slope=%s intercept=%s "
             "(damped Newton on logit(p) clipped to [1e-06, 0.999999], %d events)"
             % (_fmt(calib["slope"], "%+.4f"), _fmt(calib["intercept"], "%+.4f"),
                calib["n"]))
    L.append("E6 calibration (all events): slope=%s intercept=%s (%d events)"
             % (_fmt(calib_all["slope"], "%+.4f"), _fmt(calib_all["intercept"], "%+.4f"),
                calib_all["n"]))
    for row in rel:
        L.append("E6 reliability (5 bins, pass events): %.1f-%.1f: pred=%s obs=%s n=%d"
                 % (row["lo"], row["hi"], _fmt(row["pred"], "%.3f"),
                    _fmt(row["obs"], "%.3f"), row["n"]))
    if not pass_set["ps"]:
        L.append("E6 reliability note: no pass event carried a filed probability; all five bins are empty")
    L.append("Finish audit at graded turns: finish=length %d/%d, parse fail %d/%d"
             % (regrade["finish_length"], G, regrade["parse_fail"], G))
    for cell, okc, tot in ack_audit:
        L.append("Ack compliance (raw lowercased startswith ok): %s %d/%d = %s"
                 % (cell, okc, tot,
                    "%.1f%%" % (100.0 * okc / tot) if tot else "n/a"))
    L.append("Excluded pids: family1 %s family2 %s"
             % ("none" if not excluded[1] else ",".join(str(p) for p in excluded[1]),
                "none" if not excluded[2] else ",".join(str(p) for p in excluded[2])))
    L.append("")
    for name, text, why in verdicts:
        L.append("<!-- VERDICT %s rule (mechanical, no judgment): %s -->" % (name, why))
        L.append("VERDICT %s: %s" % (name, text))
    L.append("")
    L.append("## Audit (regeneration, re-parse, re-grade)")
    L.append("")
    L.append("Truth rebuild: family1 %d/%d verified (%s), family2 %d/%d verified (%s)%s"
             % (truth_audit["f1_ok"], len(metas_1), gens["gen_problem_source"],
                truth_audit["f2_ok"], len(metas_2), gens["gen_seq_problem_source"],
                "" if gens.get("sha256") else " [probe_r12.py absent or unreadable]"))
    if gens.get("error"):
        L.append("Generator import note: %s" % gens["error"])
    L.append("Generator source: %s sha256=%s"
             % (gens.get("path", "n/a"), gens.get("sha256") or "n/a"))
    for fam in (1, 2):
        for msg in truth_audit["f%d" % fam]:
            L.append("TRUTH MISMATCH family%d %s" % (fam, msg))
    for msg in truth_audit["unchecked"]:
        L.append("TRUTH UNCHECKED %s" % msg)
    L.append("Re-grade audit: %d graded records re-parsed and re-graded; %d stored-field mismatch(es)"
             % (regrade["checked"], len(regrade["mismatch"])))
    for msg in regrade["mismatch"]:
        L.append("REGRADE MISMATCH %s" % msg)
    if err_unattributed:
        for msg in err_unattributed:
            L.append("ERROR RECORD UNATTRIBUTED %s" % msg)
    L.append("Shared-turn sets used: %s"
             % "; ".join("%s [%s]" % (c, ",".join(str(t) for t in shared_turns[c]))
                         for c in ALL_ARMS))
    L.append("Page scaling note: sum-of-ranks L=%s E_L=%s var_L=%s; mean-rank scaling "
             "L=%s E_L=%.3f var_L=%s (identical z=%s p=%s — R1 is scaling-invariant)"
             % (_fmt(page["L"], "%.4f"), _fmt(page["E_L"], "%.4f"),
                _fmt(page["var_L"], "%.4f"), _fmt(page["L_mean_rank"], "%.4f"),
                page["k"] * (page["k"] + 1) ** 2 / 4.0 if page["k"] else float("nan"),
                _fmt(page["var_L"] / page["n"] ** 2 if page["n"] else float("nan"), "%.6f"),
                _fmt(page["z"], "%+.3f"), _fmt(page["p"], "%.4f")))
    L.append("E6 scored-event tally: pass %d/%d scored; sign %d/%d scored; run-level %d/%d scored; "
             "all scored events %d/%d"
             % (pass_set["n"], len(pass_events), sign_set["n"], len(sign_events),
                run_set["n"], len(run_events), pooled_n, total_events))
    L.append("E6 coverage audit: %d final-turn graded events; %d carried a filed probability; unmapped %d"
             % (len(pass_events), pass_set["n"], len(unmapped)))
    L.append("E6 run-level outcomes: %s"
             % " ".join("%s=%d" % (rid, rl_out[rid]) for rid in RL_IDS))
    L.append("E6 run-level filed probabilities: %s"
             % " ".join("%s=%s" % (rid, ("%.4f" % run_probs[rid]) if rid in run_probs else "n/a")
                        for rid in RL_IDS))
    if probmeta.get("runlevel_check"):
        L.append("Run-level probability cross-check: %s" % probmeta["runlevel_check"])
    if probs_error:
        L.append("Prediction-file note: %s" % probs_error)
    for msg in (probs_notes or [])[:30]:
        L.append("PREDICTION RECORD UNMAPPED %s" % msg)
    for key, fname in (("perproblem", "%s" % probmeta.get("perproblem_name", "predictions-r12-perproblem.jsonl")),
                       ("signevents", "%s" % probmeta.get("signevents_name", "predictions-r12-signevents.jsonl")),
                       ("runlevel", pred_name)):
        L.append("Prediction file %s: %s sha256=%s"
                 % (key, fname, probmeta.get("%s_sha256" % key) or "n/a"))
    L.append("Calibration solver (primary, pass events): iters=%d converged=%s%s"
             % (calib["iters"], calib["converged"],
                (" note=%s" % calib["note"]) if calib["note"] else ""))
    L.append("Calibration solver (secondary, all scored events): iters=%d converged=%s%s"
             % (calib_all["iters"], calib_all["converged"],
                (" note=%s" % calib_all["note"]) if calib_all["note"] else ""))
    if page.get("degenerate"):
        L.append("NOTE degenerate: zero-variance Page (var_L=0)")
    for name, st in (("E2", e2), ("E4", e4), ("E5", e5)):
        if st.get("degenerate"):
            L.append("NOTE degenerate: zero-variance diffs (%s)" % name)
    for label, _turns, st in e3:
        if st.get("degenerate"):
            L.append("NOTE degenerate: zero-variance diffs (E3 %s)" % label)
    for arm in F1_ARMS:
        L.append("Realized arm positions after deletion: %s:%s"
                 % (arm, ",".join(str(pos_counts.get(pos, {}).get(arm, 0))
                                  for pos in range(1, 6))))
    if not pos_counts:
        L.append("Realized arm positions after deletion: n/a (no family-1 graded bytes)")
    L.append("Realized arm-position counts (descriptors record): %s"
             % ("%s=%s" % (desc_order_counts[0], json.dumps(desc_order_counts[1], sort_keys=True))
                if desc_order_counts else "not present in descriptors"))
    if descriptors_end != 1:
        L.append("Descriptor note: %d `descriptors` and %d `descriptors_end` records present"
                 % (descriptors, descriptors_end))
    L.append("Graded records per cell: %s"
             % ", ".join("%s %d" % (c, len(graded_by_cell[c])) for c in ALL_ARMS))
    L.append("E2 McNemar b/c recomputed from stored `ok` at the final turns; "
             "E4 McNemar b=%d c=%d two-sided p=%s" % (e4_b, e4_c, _fmt(e4_mcn_p, "%.4f")))
    if under_note:
        L.append("Contingency: %s" % under_note)
    L.append("")
    L.append("## Prediction scoring")
    L.append("")
    if not pred_text:
        L.append("`%s` not present at analysis time — point-prediction scoring unavailable."
                 % pred_name)
    L.append("| Quantity | Predicted | Observed | Abs error |")
    L.append("|---|---:|---:|---:|")
    matched_rows = 0
    for item in pred_rows:
        sr = score_row(item["label"], item["raw"], item["pred"], obs)
        if sr is None:
            L.append("| %s | %s | n/a | n/a |" % (item["label"], item["raw"]))
            continue
        pred_used, obs_used, p_disp, o_disp, qname = sr
        matched_rows += 1
        L.append("| %s | %s | %s | %s |"
                 % (item["label"], p_disp, o_disp,
                    _fmt(abs(pred_used - obs_used), "%.3f")))
    if not pred_rows:
        L.append("| (no point-prediction rows parsed) | n/a | n/a | n/a |")
    L.append("")
    L.append("Forecast scoring uses the filed per-event probabilities only (never recomputed "
             "post hoc): Brier %s (pass, N=%d), %s (sign, N=%d), %s (run-level, N=%d), "
             "%s (all %d); BSS vs own-group climatology %s (pass) / %s (sign) / %s "
             "(run-level) / %s (pooled); calibration slope %s / intercept %s (primary, "
             "%d pass events), %s / %s (secondary, %d events)."
             % (_fmt(pass_set["brier"], "%.4f"), pass_set["n"],
                _fmt(sign_set["brier"], "%.4f"), sign_set["n"],
                _fmt(run_set["brier"], "%.4f"), run_set["n"],
                _fmt(pooled_brier, "%.4f"), pooled_n,
                _fmt(bss_pass, "%+.4f"), _fmt(sign_set["bss"], "%+.4f"),
                _fmt(run_set["bss"], "%+.4f"), _fmt(pooled_bss, "%+.4f"),
                _fmt(calib["slope"], "%+.4f"), _fmt(calib["intercept"], "%+.4f"),
                calib["n"], _fmt(calib_all["slope"], "%+.4f"),
                _fmt(calib_all["intercept"], "%+.4f"), calib_all["n"]))
    if pred_rows:
        L.append("Point-prediction rows parsed: %d (%d matched to an observed quantity)"
                 % (len(pred_rows), matched_rows))
    L.append("")
    L.append("## Ordering and registration")
    L.append("")
    bundle_entries = _parse_bundle(bundle_text)
    bundle_version = _parse_version(bundle_text) or _parse_version(ordering_text) or "?"
    hash_by_file = {os.path.basename(p): h for h, p in bundle_entries}
    times = _parse_ordering(ordering_text)
    ts = [r.get("request_ts") for r in recs if r.get("request_ts")]
    first_ts = min(ts) if ts else "unavailable"
    L.append("Ordering proof: prereg-bundle.sha256 (%s) — %s; ordering.log pre-hash %s / "
             "post-hash %s; first request_ts %s."
             % (bundle_version,
                ", ".join("%s %s" % (os.path.basename(p), h) for h, p in bundle_entries)
                or "unavailable",
                times.get("pre-hash", "unavailable"), times.get("post-hash", "unavailable"),
                first_ts))
    run_hashes = _parse_run_script_hashes(ordering_text)
    L.append("Run-script hashes (ordering.log): %s"
             % ("; ".join("%s %s %s" % (ts, name, sha) for ts, name, sha in run_hashes)
                or "unavailable"))
    L.append("Main run launched: %s (ordering.log `main-run-launch`)."
             % times.get("main-run-launch", "unavailable"))
    pred_hash = hash_by_file.get(os.path.basename(pred_name), "unavailable")
    L.append("Predictions file: %s (bundle sha256 entry %s)." % (pred_name, pred_hash))
    L.append("")
    L.append("Verdict rules applied verbatim from `probe_plan_r12.md` §2.3 (R1-R5), with the "
             "error-record contingency: any `cell:\"error\"` record listwise-deletes that pid "
             "from its family, and family-1 n < 44 or family-2 n < 44 (the filed power "
             "floors, `power_analysis_r12.md`) reports every verdict "
             "`UNDERPOWERED-INDETERMINATE` regardless of its p-value.")
    L.append("")
    return "\n".join(L)


# --------------------------------------------------------------------------
# file plumbing
# --------------------------------------------------------------------------
def load_records(path):
    recs = []
    with open(path, "r", encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                recs.append(json.loads(ln))
    return recs


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def verify_pinned_file(path, bundle_entries, bundle_path):
    """Pinned-name/schema hard failure (L1 §1, §5 probability-file interface).

    Absent -> PredictionError.  When the bundle pins the file's basename, its
    sha256 must agree with `prereg-bundle.sha256`.
    """
    if not os.path.exists(path):
        raise PredictionError("pinned prediction file absent: %s" % path)
    base = os.path.basename(path)
    if base not in PINNED_PRED_FILES:
        return
    want = bundle_entries.get(base)
    if not want:
        raise PredictionError("%s is not pinned in %s" % (base, bundle_path))
    got = sha256_file(path)
    if got != want:
        raise PredictionError("sha256 mismatch for %s: bundle %s != file %s"
                              % (base, want, got))


def run_analysis(results_path, out_path, bundle_path=DEF_BUNDLE, ordering_path=DEF_ORDERING,
                 pred_path=None, perprob_path=None, signev_path=None, gens=None):
    """Read the run bytes + the pinned registration/prediction files, write
    out_path, return the md.

    The three prediction artifacts are read by their pinned names/schemas only
    (no candidate search, no markdown fallback) and their sha256 is checked
    against `prereg-bundle.sha256`.  Raises `PredictionError` -> exit 2 on
    absence, sha mismatch, or a coverage shortfall.
    """
    recs = load_records(results_path)
    bundle_text = _read_text(bundle_path) if os.path.exists(bundle_path) else ""
    ordering_text = _read_text(ordering_path) if os.path.exists(ordering_path) else ""
    pred_path = pred_path if pred_path is not None else DEF_PRED
    perprob_path = perprob_path if perprob_path is not None else DEF_PERPROB
    signev_path = signev_path if signev_path is not None else DEF_SIGNEV

    bundle_entries = {os.path.basename(p): h for h, p in _parse_bundle(bundle_text)}
    strict = bool(bundle_entries)
    if strict:
        verify_pinned_file(DEF_PERPROB if perprob_path == DEF_PERPROB else perprob_path,
                           bundle_entries, bundle_path)
        verify_pinned_file(DEF_SIGNEV if signev_path == DEF_SIGNEV else signev_path,
                           bundle_entries, bundle_path)
        verify_pinned_file(DEF_PRED if pred_path == DEF_PRED else pred_path,
                           bundle_entries, bundle_path)
    else:
        for path in (pred_path, perprob_path, signev_path):
            if not os.path.exists(path):
                raise PredictionError("prediction file absent: %s" % path)

    pred_text = _read_text(pred_path)
    perprob, pp_notes, pp_err = read_perproblem(perprob_path)
    if pp_err:
        raise PredictionError("perproblem reader: %s" % pp_err)
    signprob, sp_notes, sp_err = read_signevents(signev_path)
    if sp_err:
        raise PredictionError("signevents reader: %s" % sp_err)
    runprob_rows, rl_notes = read_runlevel(pred_text)
    if [r[0] for r in runprob_rows] != RL_IDS:
        raise PredictionError("run-level RL1-RL7 not parsed from %s (%s)"
                              % (pred_path, "; ".join(rl_notes) or "no rows"))
    expected_rl, rl_src_err = read_predictor_runlevel(PREDICT_R12)
    if expected_rl:
        bad_rl = ["%s %s!=%s" % (rid, p, expected_rl[rid])
                  for rid, _lab, p in runprob_rows
                  if rid in expected_rl and abs(p - expected_rl[rid]) > 1e-12]
        miss_rl = [rid for rid in RL_IDS if rid not in expected_rl]
        if bad_rl or miss_rl:
            raise PredictionError(
                "run-level probabilities disagree with predict_r12.py "
                "RUNLEVEL_EVENTS: %s%s"
                % ("; ".join(bad_rl), ("; missing " + ",".join(miss_rl)) if miss_rl else ""))
    gens = gens or load_generators()
    probmeta = {
        "perproblem_name": os.path.basename(perprob_path),
        "perproblem_sha256": sha256_file(perprob_path),
        "signevents_name": os.path.basename(signev_path),
        "signevents_sha256": sha256_file(signev_path),
        "runlevel_name": os.path.basename(pred_path),
        "runlevel_sha256": sha256_file(pred_path),
        "runlevel_check": ("verified against predict_r12.py RUNLEVEL_EVENTS"
                           if expected_rl else (rl_src_err or "not cross-checked")),
    }
    md = analyze(recs, bundle_text, ordering_text, os.path.basename(results_path),
                 pred_text=pred_text, pred_name=os.path.basename(pred_path),
                 perprob=perprob, signprob=signprob, runprob_rows=runprob_rows,
                 probmeta=probmeta, gens=gens,
                 probs_notes=pp_notes + sp_notes, probs_error=None, strict=strict)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(md)
    return md


# --------------------------------------------------------------------------
# selftest fixtures
# --------------------------------------------------------------------------
TS0 = "2026-09-28T23:10:30Z"
TS1 = "2026-09-28T23:10:31Z"
TS2 = "2026-09-28T23:40:31Z"


def _want_with_errors(want, k):
    """Family-1 got: `want` with exactly k deliberately wrong keys (k clamped
    to the key count).  grade_state then returns (k == 0, k)."""
    keys = sorted(want)
    k_eff = min(k, len(keys))
    got = dict(want)
    for key in keys[:k_eff]:
        got[key] = want[key] + 100
    return got, k_eff


def _want_seq_with_errors(want, k, length_mismatch=False):
    """Family-2 got: `want` with exactly k positional mismatches, optionally
    one token short (the length error counts once)."""
    got = list(want)
    k_eff = min(k, len(want))
    for i in range(k_eff):
        got[i] = "___wrong___"
    if length_mismatch:
        got = got[:-1]
    return got, k_eff


def fixture_records(n1=4, n2=3, nw_spec=None, parse_fail=None, seq_len_mismatch=None,
                    error_pids=(), tamper=None, f1_pids=None, f2_pids=None):
    """Build a synthetic `results-r12.jsonl` body (list of records).

    n1/n2   number of family-1 / family-2 pids (default small: underpowered).
    nw_spec dict {(pid, cell, turn): nwrong} overriding the default pattern.
    parse_fail list of (pid, cell, turn) whose `raw` carries no JSON at all.
    seq_len_mismatch (pid, cell, turn) whose family-2 answer is one token short.
    error_pids list of (family, pid) -> `cell:"error"` records (attributed
            through the `job` string, exercising §4's pid-less schema).
    tamper   {(pid, cell, turn): value} overwriting the stored `nwrong` field
            on an otherwise correct record (the re-grade audit must catch it).
    """
    nw_spec = nw_spec or {}
    parse_fail = set(parse_fail or ())
    tamper = tamper or {}
    f1_pids = f1_pids if f1_pids is not None else list(range(201, 201 + n1))
    f2_pids = f2_pids if f2_pids is not None else list(range(401, 401 + n2))
    recs = []
    recs.append({"cell": "descriptors", "request_ts": TS0, "endpoint": "local",
                 "models_json": {}, "server": {}, "temp": 0.2, "maxtok": 8192,
                 "system_prompt": "x", "seed_scheme": SEED_F1, "seed_scheme2": SEED_F2,
                 "pids": list(f1_pids), "pids2": list(f2_pids), "n": len(f1_pids),
                 "n2": len(f2_pids), "counterbalance": "5-rotation / pid parity",
                 "machinery_sha256": "0" * 64, "probe_lineage": "probe_r12.py"})

    def default_nw(pid, cell, turn):
        idx = {"A-INC": 10, "A-CKPT4710": 3, "A-CKPT710": 2, "A-CKPT10": 1,
               "A-MONO": 1, "T-DENSE": 3, "T-SPARSE": 2}[cell]
        base = (pid * 7 + turn * 3) % (idx + 1)
        return base

    def emit_graded(pid, cell, turn, want, k, length_mismatch=False, family=1):
        if (pid, cell, turn) in parse_fail:
            raw = "I am unable to comply with that request."
            got, k_eff = None, (len(want) if family == 1 or not isinstance(want, list)
                                else len(want))
            ok = False
        elif family == 1:
            got, k_eff = _want_with_errors(want, k)
            raw = "```json\n%s\n```" % json.dumps(got, separators=(",", ":"))
            ok = (k_eff == 0)
        else:
            got, k_eff = _want_seq_with_errors(want, k, length_mismatch=length_mismatch)
            raw = "```json\n%s\n```" % json.dumps(got, separators=(",", ":"))
            ok, k_eff = grade_seq(got, want)
        stored_nw = k_eff
        if family == 1 and got is not None:
            ok, stored_nw = grade_state(got, want)
        elif family == 2 and got is not None:
            ok, stored_nw = grade_seq(got, want)
        if (pid, cell, turn) in tamper:
            stored_nw = tamper[(pid, cell, turn)]
            ok = (stored_nw == 0)
        recs.append({"cell": cell, "pid": pid, "turn": turn, "ok": ok,
                     "nwrong": stored_nw, "got": got if got is not None else {},
                     "want": want, "finish": "length" if (pid, cell, turn) in parse_fail else "stop",
                     "usage": {}, "wall_s": 0.1, "raw": raw, "request_ts": TS1})

    # family 1
    for pid in f1_pids:
        seed = 3000 + pid * 41
        init, ops = call_gen(gen_problem, seed)
        states = states_along(init, ops)
        recs.append({"cell": "meta", "pid": pid, "seed": seed, "init": init,
                     "ops": ops, "truth": states,
                     "tail_touched": sorted(tail_touched(ops))})
        for cell in F1_ARMS:
            for turn in ARM_TURNS[cell]:
                want = _want_state(cell, turn, ops, states)
                k = nw_spec.get((pid, cell, turn), default_nw(pid, cell, turn))
                emit_graded(pid, cell, turn, want, k, family=1)
        for cell in F1_ACK_BASE:
            for turn in ACK_TURNS[cell]:
                recs.append({"cell": cell + "-ack", "pid": pid, "turn": turn,
                             "raw": "ok", "finish": "stop", "usage": {}, "wall_s": 0.1,
                             "request_ts": TS1})
        for _ in range(5):
            recs.append({"cell": "filler", "finish": "stop", "usage": {},
                         "wall_s": 0.1, "raw": "ready", "request_ts": TS1})

    # family 2
    for pid in f2_pids:
        seed = 5000 + pid * 37
        init, ops = call_gen(gen_seq_problem, seed)
        states = seq_states(init, ops)
        recs.append({"cell": "meta2", "pid": pid, "seed": seed, "init": init,
                     "ops": ops, "truth": states, "features": {}})
        for cell in F2_ARMS:
            for turn in ARM_TURNS[cell]:
                want = _want_state(cell, turn, ops, states)
                k = nw_spec.get((pid, cell, turn),
                                {"T-DENSE": 5, "T-SPARSE": 3}[cell])
                lm = (seq_len_mismatch is not None
                      and (pid, cell, turn) == tuple(seq_len_mismatch))
                emit_graded(pid, cell, turn, want, k, length_mismatch=lm, family=2)
        for cell in F2_ACK_BASE:
            for turn in ACK_TURNS[cell]:
                recs.append({"cell": cell + "-ack", "pid": pid, "turn": turn,
                             "raw": "ok", "finish": "stop", "usage": {}, "wall_s": 0.1,
                             "request_ts": TS1})
        for _ in range(2):
            recs.append({"cell": "filler", "finish": "stop", "usage": {},
                         "wall_s": 0.1, "raw": "ready", "request_ts": TS1})

    for fam, pid in error_pids:
        name = "A-CKPT710" if fam == 1 else "T-SPARSE"
        recs.append({"cell": "error", "job": "(%s, %d)" % (name, pid),
                     "err": "connection reset by peer", "request_ts": TS2})
    recs.append({"cell": "descriptors_end", "request_ts": TS2, "models_json": {},
                 "server": {}, "pid": 4242, "argv": []})
    return recs


def _fixture_md(recs, pred_text="", probs=None, signprob=None, runprob_rows=None,
                out_name="analysis_r12.md", pred_name="predictions-r12.md",
                perprob_name="predictions-r12-perproblem.jsonl",
                signev_name="predictions-r12-signevents.jsonl"):
    """Render the fixture record list through the real `analyze` path."""
    gens = {"gen_problem": gen_problem, "gen_seq_problem": gen_seq_problem,
            "gen_problem_source": "port(selftest)", "gen_seq_problem_source": "port(selftest)",
            "sha256": None, "path": PROBE_R12, "error": "selftest fixture"}
    md = analyze(recs, "", "", "results-r12.jsonl", pred_text=pred_text,
                 pred_name=pred_name, perprob=probs or {}, signprob=signprob or {},
                 runprob_rows=runprob_rows or [], probmeta={}, gens=gens,
                 strict=False)
    if out_name:
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, out_name), "w", encoding="utf-8") as fh:
                fh.write(md)
    return md


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


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------
def selftest():
    failures = []
    checks = []

    def chk(label, cond, msg):
        checks.append(label)
        _expect(cond, "%s: %s" % (label, msg), failures)

    # 1) r11 statistics anchors -------------------------------------------
    chk("betai t=2.0 df=63 -> p 0.0498158",
        abs(t_two_sided_p(2.0, 63) - 0.049815763699) < 1e-9,
        "got %.12f" % t_two_sided_p(2.0, 63))
    chk("t_crit(63) == 1.9983405425", abs(t_crit(63) - 1.9983405425) < 1e-6,
        "got %.10f" % t_crit(63))
    chk("t_crit(3) == 3.1824463053", abs(t_crit(3) - 3.1824463053) < 1e-6,
        "got %.10f" % t_crit(3))
    chk("t_two_sided_p(0.7745966692414834, 3) == 0.495025346060",
        abs(t_two_sided_p(0.7745966692414834, 3) - 0.495025346060) < 1e-9,
        "got %.12f" % t_two_sided_p(0.7745966692414834, 3))
    chk("exact_sign_p(2,1) == 1.0", exact_sign_p(2, 1) == 1.0,
        "got %r" % exact_sign_p(2, 1))
    chk("exact_sign_p(5,0) == 0.0625", abs(exact_sign_p(5, 0) - 0.0625) < 1e-15,
        "got %r" % exact_sign_p(5, 0))
    chk("mcnemar_exact(1,1) == 1.0", mcnemar_exact(1, 1) == 1.0,
        "got %r" % mcnemar_exact(1, 1))
    chk("normal_two_sided_p(1.959963985) ~ 0.05",
        abs(normal_two_sided_p(1.959963984540054) - 0.05) < 1e-12,
        "got %.15f" % normal_two_sided_p(1.959963984540054))

    # 2) Page's L, hand-computed 3-block toy (no ties) ---------------------
    #    blocks (arm order INC, 4710, 710, 10); within-block ranks 4..1 for the
    #    largest..smallest value, so a block contributes s = sum_j j*r_j:
    #      b1 [3,2,1,0] -> ranks (4,3,2,1) -> s = 1*4+2*3+3*2+4*1 = 20
    #      b2 [0,1,2,3] -> ranks (1,2,3,4) -> s = 1+4+9+16          = 30
    #      b3 [2,3,1,0] -> ranks (3,4,2,1) -> s = 3+8+6+4           = 21
    #    L = 20+30+21 = 71;  E_L = n*k*(k+1)^2/4 = 3*4*25/4 = 75
    #    var per block (no ties) = SS_c*SS_r/(k-1) = 5*5/3 = 25/3;
    #    var_L = 3*25/3 = 25;  z = (71-75)/5 = -0.8
    #    p = 2*(1-Phi(0.8)) = erfc(0.8/sqrt(2)) = 0.4237107971667933
    toy = [[3, 2, 1, 0], [0, 1, 2, 3], [2, 3, 1, 0]]
    pt = page_test(toy)
    chk("Page toy L == 71", pt["L"] == 71.0, "got %r" % pt["L"])
    chk("Page toy E_L == 75", pt["E_L"] == 75.0, "got %r" % pt["E_L"])
    chk("Page toy var_L == 25", abs(pt["var_L"] - 25.0) < 1e-12, "got %r" % pt["var_L"])
    chk("Page toy z == -0.8", abs(pt["z"] + 0.8) < 1e-12, "got %r" % pt["z"])
    chk("Page toy p == 0.4237107971667933",
        abs(pt["p"] - 0.4237107971667933) < 1e-12, "got %.15f" % pt["p"])
    chk("Page toy direction == decreasing", pt["direction"] == "decreasing",
        "got %r" % pt["direction"])

    # 3) Page's L with ties, hand-computed 2-block toy --------------------
    #    b1 [1,1,2,0] -> midranks (2.5,2.5,4,1) -> s = 2.5+5+12+4 = 23.5
    #       SS_r = 0+0+(4-2.5)^2+(1-2.5)^2 = 4.5 -> var = 5*4.5/3 = 7.5
    #    b2 [0,2,2,2] -> midranks (1,3,3,3) -> s = 1+6+9+12 = 28
    #       SS_r = (1-2.5)^2+3*(0.5)^2 = 3.0 -> var = 5*3.0/3 = 5.0
    #    L = 51.5, E_L = 2*25 = 50, var_L = 12.5, z = 1.5/sqrt(12.5) = 0.4242640
    #    p = 2*(1-Phi(0.4242640)) = 0.671494...
    toyt = [[1, 1, 2, 0], [0, 2, 2, 2]]
    ptt = page_test(toyt)
    chk("Page tie toy L == 51.5", abs(ptt["L"] - 51.5) < 1e-12, "got %r" % ptt["L"])
    chk("Page tie toy E_L == 50", ptt["E_L"] == 50.0, "got %r" % ptt["E_L"])
    chk("Page tie toy var_L == 12.5", abs(ptt["var_L"] - 12.5) < 1e-12,
        "got %r" % ptt["var_L"])
    chk("Page tie toy z ~ 0.4242640",
        abs(ptt["z"] - 1.5 / math.sqrt(12.5)) < 1e-12, "got %r" % ptt["z"])
    chk("Page tie toy direction == increasing", ptt["direction"] == "increasing",
        "got %r" % ptt["direction"])
    # no-tie variance must reduce to the classical k^2(k+1)(k^2-1)/144 formula
    classic1 = 4 ** 2 * 5 * (4 ** 2 - 1) / 144.0        # k^2(k+1)(k^2-1)/144 = 25/3
    chk("Page var reduces to the classical no-tie formula n*k^2(k+1)(k^2-1)/144",
        abs(classic1 - 25.0 / 3.0) < 1e-12
        and abs(page_test([[1, 2, 3, 4]] * 4)["var_L"] - 4 * classic1) < 1e-12,
        "got %r want %r (classic1=%r)" % (page_test([[1, 2, 3, 4]] * 4)["var_L"],
                                          4 * classic1, classic1))
    # midranks check
    chk("midranks([1,1,2,0]) == [2.5,2.5,4.0,1.0]",
        midranks([1, 1, 2, 0]) == [2.5, 2.5, 4.0, 1.0],
        "got %r" % midranks([1, 1, 2, 0]))

    # 4) paired contrast, hand-computed (r11's FIX_MIN diff vector) --------
    #    diffs [+1.0, 0.0, +0.5, -0.5] -> mean +0.25, sd 0.6454972243679028,
    #    se 0.3227486, t 0.7745966692414834, p 0.495025346060,
    #    CI = 0.25 +/- t_crit(3)*se = 0.25 +/- 3.1824463053*0.3227486121839514
    #       = [-0.7771301284, +1.2771301284]
    pst = paired_contrast([(201, 1.0, 0.0), (202, 0.0, 0.0), (203, 0.5, 0.0), (204, 0.0, 0.5)])
    chk("paired mean == +0.25", abs(pst["mean"] - 0.25) < 1e-15, "got %r" % pst["mean"])
    chk("paired sd == 0.6454972243679028",
        abs(pst["sd"] - 0.6454972243679028) < 1e-12, "got %r" % pst["sd"])
    chk("paired t == 0.7745966692414834",
        abs(pst["t"] - 0.7745966692414834) < 1e-12, "got %r" % pst["t"])
    chk("paired p == 0.495025346060", abs(pst["p"] - 0.495025346060) < 1e-9,
        "got %.12f" % pst["p"])
    chk("paired df == 3", pst["df"] == 3, "got %r" % pst["df"])
    chk("paired CI == [-0.7771301284, +1.2771301284]",
        abs(pst["ci_lo"] + 0.7771301283855188) < 1e-9
        and abs(pst["ci_hi"] - 1.2771301283855188) < 1e-9,
        "got [%r, %r]" % (pst["ci_lo"], pst["ci_hi"]))
    chk("paired sign W/L/T == 2/1/1",
        (pst["wins"], pst["losses"], pst["ties"]) == (2, 1, 1),
        "got %r" % ((pst["wins"], pst["losses"], pst["ties"]),))
    chk("paired sign p == 1.0", pst["sign_p"] == 1.0, "got %r" % pst["sign_p"])
    chk("paired n==1 -> n/a sd/t (no crash)",
        not math.isfinite(paired_contrast([(1, 1.0, 0.0)])["sd"]),
        "sd finite")

    # 5) Brier / BSS, hand-computed ---------------------------------------
    #    p = [0.8, 0.3, 0.5], y = [1, 0, 1] -> (0.04+0.09+0.25)/3 = 0.126666...
    chk("brier == 0.1266666...", abs(brier([0.8, 0.3, 0.5], [1, 0, 1]) - 0.38 / 3) < 1e-15,
        "got %r" % brier([0.8, 0.3, 0.5], [1, 0, 1]))
    chk("brier perfect forecast == 0",
        brier([1.0, 0.0, 1.0], [1, 0, 1]) == 0.0, "got %r" % brier([1.0, 0.0, 1.0], [1, 0, 1]))
    # BSS sign behaviour: a perfect forecast gives BSS -> 1 (BS = 0)
    chk("bss perfect forecast == 1.0",
        abs(bss([1.0, 0.0, 1.0, 0.0], [1, 0, 1, 0], [0.5, 0.5, 0.5, 0.5]) - 1.0) < 1e-15,
        "got %r" % bss([1.0, 0.0, 1.0, 0.0], [1, 0, 1, 0], [0.5, 0.5, 0.5, 0.5]))
    # an uninformative forecast equal to climatology gives BSS == 0
    chk("bss climatology == 0.0",
        abs(bss([0.5, 0.5, 0.5, 0.5], [1, 0, 1, 0], [0.5] * 4)) < 1e-15,
        "got %r" % bss([0.5] * 4, [1, 0, 1, 0], [0.5] * 4))
    # a worse-than-climatology forecast gives BSS < 0
    chk("bss worse-than-climatology < 0",
        bss([0.9, 0.9, 0.1, 0.1], [1, 0, 1, 0], [0.5] * 4) < 0,
        "got %r" % bss([0.9, 0.9, 0.1, 0.1], [1, 0, 1, 0], [0.5] * 4))

    # 6) calibration: exactly-calibrated synthetic probabilities -> slope 1 --
    #    For 9 probability levels p_j = 0.1..0.9 with n_j = 100 replicates each
    #    and k_j = 100*p_j exact successes, BOTH score equations vanish at
    #    (a, b) = (0, 1): sum(y - p) = 0 and sum(x*(y - p)) = 0 with
    #    x_j = logit(p_j).  The logistic MLE is unique (no separation, full
    #    rank), so the fitted slope is exactly 1 and the intercept exactly 0.
    cps, cys = [], []
    for j in range(1, 10):
        p_lvl = j / 10.0
        k_lvl = int(round(100 * p_lvl))
        cps.extend([p_lvl] * 100)
        cys.extend([1] * k_lvl + [0] * (100 - k_lvl))
    cal = calibrate(cps, cys)
    chk("calibration slope == 1.0 on exactly-calibrated synthetic p",
        abs(cal["slope"] - 1.0) < 1e-6, "got %.12f (iters %d, %s)"
        % (cal["slope"], cal["iters"], cal["converged"]))
    chk("calibration intercept == 0.0 on exactly-calibrated synthetic p",
        abs(cal["intercept"]) < 1e-6, "got %.12f" % cal["intercept"])
    chk("calibration converged within 50 iters", cal["converged"] and cal["iters"] <= 50,
        "iters=%d converged=%s" % (cal["iters"], cal["converged"]))
    chk("calibration deterministic (repeat run identical)",
        calibrate(cps, cys)["slope"] == cal["slope"], "slope drift")
    # an over-confident forecast must give slope < 1: double the log-odds
    ops2 = [_clip_p(1.0 / (1.0 + math.exp(-2.0 * logit(p)))) for p in cps]
    chk("calibration slope < 1 for over-confident forecasts",
        calibrate(ops2, cys)["slope"] < 1.0, "got %r" % calibrate(ops2, cys)["slope"])
    # reliability bins: 5 rows, counts sum to N
    rel = reliability(cps, cys)
    chk("reliability has 5 bins", len(rel) == 5, "got %d" % len(rel))
    chk("reliability n sums to N", sum(r["n"] for r in rel) == len(cps),
        "got %d want %d" % (sum(r["n"] for r in rel), len(cps)))
    chk("reliability bin 0.8-1.0 holds both p=0.8 and p=0.9 (n=200, pred=obs=0.85)",
        rel[4]["n"] == 200 and abs(rel[4]["pred"] - 0.85) < 1e-12
        and abs(rel[4]["obs"] - 0.85) < 1e-12, "got %r" % rel[4])
    chk("reliability bin 0.0-0.2 holds p=0.1 only (n=100, obs=0.1)",
        rel[0]["n"] == 100 and abs(rel[0]["obs"] - 0.1) < 1e-12, "got %r" % rel[0])
    chk("calibration unavailable on constant p (no crash)",
        not math.isfinite(calibrate([0.5] * 10, [1, 0] * 5)["slope"]), "slope finite")

    # 7) family-2 grading conventions -------------------------------------
    w = ["alpha", "beta", "gamma"]
    chk("grade_seq exact match", grade_seq(list(w), w) == (True, 0),
        "got %r" % (grade_seq(list(w), w),))
    chk("grade_seq length mismatch counts once",
        grade_seq(["alpha", "beta"], w) == (False, 1), "got %r" % (grade_seq(["alpha", "beta"], w),))
    chk("grade_seq positional + length errors add",
        grade_seq(["zeta", "beta"], w) == (False, 2),
        "got %r" % (grade_seq(["zeta", "beta"], w),))
    chk("grade_seq non-list -> nwrong=len(want)",
        grade_seq(None, w) == (False, 3), "got %r" % (grade_seq(None, w),))
    chk("grade_state non-dict -> nwrong=len(want)",
        grade_state(None, {"a": 1}) == (False, 1), "got %r" % (grade_state(None, {"a": 1}),))

    # 8) family-1 generator port matches the r11 seeds byte-for-byte -------
    #    (r11 ran pids 201-264 with seed 3000+pid*41 and landed results-r11.jsonl)
    okgen = True
    for pid in (201, 232, 264):
        init, ops, _d = gen_problem(3000 + pid * 41)
        if len(ops) != 10 or not isinstance(init, dict):
            okgen = False
    chk("gen_problem port generates 10 ops for r11's seeds", okgen, "port broke")
    gs = gen_seq_problem(5000 + 401 * 37)
    kinds = {o[0] for o in gs[1]}
    chk("gen_seq_problem port satisfies §2.2 accept condition",
        {"DEL", "MOV", "REV"} <= kinds and len(tail_positions(gs[1])) >= 2
        and len(gs[1]) == 10 and len(gs[0]) == 6,
        "got kinds=%r ops=%d init=%r" % (sorted(kinds), len(gs[1]), gs[0]))
    # every family-2 seed of the design must generate (48/48, §6.2 precheck)
    gen_fail = []
    for pid in range(401, 449):
        try:
            i2, o2, _d2 = gen_seq_problem(5000 + pid * 37)
            if len(o2) != 10 or len(i2) != 6:
                gen_fail.append(pid)
        except Exception as exc:
            gen_fail.append("%d:%s" % (pid, type(exc).__name__))
    chk("gen_seq_problem port generates all 48 family-2 seeds (401-448)",
        not gen_fail, "failed: %r" % gen_fail)

    # 9) end-to-end fixture: census + audit + contingency ------------------
    #    n1=4 / n2=3 (below the 56/42 minima) with one error record per family;
    #    one parse failure, one family-2 length mismatch, one tampered stored
    #    `nwrong` (which the re-grade audit must catch).
    f1 = list(range(201, 205))
    f2 = list(range(401, 404))
    nw_spec = {(201, "A-CKPT4710", 7): 2, (201, "A-CKPT4710", 10): 0,
               (201, "A-CKPT710", 7): 4, (201, "A-CKPT710", 10): 1,
               (202, "A-CKPT4710", 7): 0, (202, "A-CKPT4710", 10): 0,
               (202, "A-CKPT710", 7): 0, (202, "A-CKPT710", 10): 0,
               (203, "A-CKPT4710", 7): 1, (203, "A-CKPT4710", 10): 1,
               (203, "A-CKPT710", 7): 2, (203, "A-CKPT710", 10): 0,
               (204, "A-CKPT4710", 7): 1, (204, "A-CKPT4710", 10): 0,
               (204, "A-CKPT710", 7): 1, (204, "A-CKPT710", 10): 0}
    recs = fixture_records(n1=4, n2=3, nw_spec=nw_spec,
                           parse_fail=[(203, "A-INC", 5)],
                           seq_len_mismatch=(401, "T-DENSE", 10),
                           error_pids=[(1, 204), (2, 403)],
                           tamper={(202, "A-MONO", 1): 7},
                           f1_pids=f1, f2_pids=f2)
    probs = {}
    for pid in f1:
        if pid == 204:
            continue
        for arm in F1_ARMS:
            probs[(arm, pid)] = 0.25 + 0.1 * ((pid + len(arm)) % 5)
    for pid in f2:
        if pid == 403:
            continue
        probs[("T-DENSE", pid)] = 0.30
        probs[("T-SPARSE", pid)] = 0.25
    pred_md = ("# Round 12 preregistered predictions (synthetic)\n\n"
               "## 2. Predicted pass counts\n\n"
               "| arm | predicted passes | of n |\n|---|---:|---:|\n"
               "| `A-CKPT4710` | 29.0 | 64 |\n\n"
               "## 4. Point predictions\n\n"
               "| quantity | predicted | derivation |\n|---|---:|---|\n"
               "| E2/E3b 710-4710 at {7,10} | +0.3520 | r11 |\n")
    md = _fixture_md(recs, pred_text=pred_md, probs=probs)

    # census arithmetic, recomputed independently from the record list
    n_graded = sum(1 for r in recs if r.get("cell") in ALL_ARMS and "nwrong" in r)
    n_ack = sum(1 for r in recs if str(r.get("cell", "")).endswith("-ack"))
    n_fill = sum(1 for r in recs if r.get("cell") == "filler")
    n_err = sum(1 for r in recs if r.get("cell") == "error")
    n_desc = sum(1 for r in recs if r.get("cell") in ("descriptors", "descriptors_end"))
    n_meta = sum(1 for r in recs if r.get("cell") == "meta")
    n_meta2 = sum(1 for r in recs if r.get("cell") == "meta2")
    chk("census line matches independent arithmetic",
        _line(md, "results-r12.jsonl contains") ==
        "results-r12.jsonl contains %d descriptors, %d meta, %d meta2, %d graded, "
        "%d ack, %d fillers, %d error records"
        % (n_desc, n_meta, n_meta2, n_graded, n_ack, n_fill, n_err),
        "got %r" % _line(md, "results-r12.jsonl contains"))
    chk("census fixture shape (4 f1 pids x 5 arms + 3 f2 pids x 2 arms)",
        n_graded == 4 * (10 + 3 + 2 + 1 + 1) + 3 * (3 + 2),
        "got %d" % n_graded)
    arm_row_re = r"^\| (A-INC|A-CKPT4710|A-CKPT710|A-CKPT10|A-MONO|T-DENSE|T-SPARSE) \| \d+/\d+ \|"
    chk("seven arm rows emitted",
        sum(1 for ln in md.splitlines() if re.match(arm_row_re, ln)) == 7,
        "got %d: %r" % (sum(1 for ln in md.splitlines() if re.match(arm_row_re, ln)),
                        [ln for ln in md.splitlines() if re.match(arm_row_re, ln)]))
    chk("arm table header exact",
        _contains(md, "| Arm | Final passes / n | Mean final nwrong | Mean nwrong (shared turns) |"),
        "header missing")

    # truth audit must be clean on a fixture built from the same generators
    chk("truth rebuild family1 4/4 verified",
        _contains(md, "family1 4/4 verified"), _line(md, "Truth rebuild:"))
    chk("truth rebuild family2 3/3 verified",
        _contains(md, "family2 3/3 verified"), _line(md, "Truth rebuild:"))
    chk("re-grade audit: 1 parse failure detected",
        _contains(md, "parse fail 1/%d" % n_graded), _line(md, "Finish audit"))
    chk("re-grade audit: 2 stored-field mismatches detected (parse fail has none; tamper caught)",
        _contains(md, "1 stored-field mismatch(es)"),
        _line(md, "Re-grade audit:"))
    chk("tampered stored nwrong reported as REGRADE MISMATCH",
        _contains(md, "REGRADE MISMATCH A-MONO pid=202 turn=1"), "tamper not caught")
    chk("no TRUTH MISMATCH lines on a faithful fixture",
        not _contains(md, "TRUTH MISMATCH"), "spurious truth mismatch")

    # contingency
    chk("excluded pids line lists both families",
        _line(md, "Excluded pids:") == "Excluded pids: family1 204 family2 403",
        "got %r" % _line(md, "Excluded pids:"))
    chk("underpowered branch fires on all five verdicts",
        all(_line(md, "VERDICT %s" % n).endswith("UNDERPOWERED-INDETERMINATE")
            for n in ("R1 ladder", "R2 repeat", "R3 batching", "R4 transport", "R5 forecast")),
        "got %r" % [_line(md, "VERDICT %s" % n) for n in
                    ("R1 ladder", "R2 repeat", "R3 batching", "R4 transport", "R5 forecast")])
    chk("underpowered comment names the minima",
        _contains(md, "family1 n=3 < 44") and _contains(md, "family2 n=2 < 44"),
        "comment lacks the arithmetic")
    lines_fx = md.splitlines()
    chk("every VERDICT line is immediately preceded by its rule comment",
        all(lines_fx[lines_fx.index(_line(md, "VERDICT %s" % n)) - 1].startswith("<!-- VERDICT %s" % n)
            for n in ("R1 ladder", "R2 repeat", "R3 batching", "R4 transport", "R5 forecast")),
        "comment placement broke: %r" % [lines_fx[lines_fx.index(_line(md, "VERDICT %s" % n)) - 1]
                                         for n in ("R1 ladder", "R2 repeat")])

    # E6 pipeline: pooled Brier must equal the value recomputed from probs
    ys_by = {}
    for r in recs:
        if r.get("cell") in ALL_ARMS and "nwrong" in r and r.get("turn") == ARM_FINAL_TURN.get(r["cell"], FINAL_TURN):
            ys_by[(r["cell"], r["pid"])] = 1 if r.get("ok") else 0
    exp_ps = [probs[k] for k in sorted(ys_by) if k in probs]
    exp_ys = [ys_by[k] for k in sorted(ys_by) if k in probs]
    exp_pooled = sum((p - y) ** 2 for p, y in zip(exp_ps, exp_ys)) / len(exp_ps)
    chk("E6 pooled Brier equals the independent recomputation from the filed probabilities",
        _line(md, "E6 Brier pass:").startswith("E6 Brier pass: pooled=%.4f (N=%d);"
                                              % (exp_pooled, len(exp_ps))),
        "got %r want pooled=%.4f N=%d" % (_line(md, "E6 Brier pass:"), exp_pooled, len(exp_ps)))
    chk("E6 Brier pass line carries all seven per-arm values in §5 order",
        all(("%s=" % c) in _line(md, "E6 Brier pass:") for c in ALL_ARMS)
        and _line(md, "E6 Brier pass:").index("A-INC=") < _line(md, "E6 Brier pass:").index("T-SPARSE="),
        _line(md, "E6 Brier pass:"))
    chk("E6 reliability has exactly 5 lines (with probabilities)",
        sum(1 for ln in md.splitlines()
            if ln.startswith("E6 reliability (5 bins, pass events):")) == 5,
        "got %d" % sum(1 for ln in md.splitlines()
                       if ln.startswith("E6 reliability (5 bins, pass events):")))
    md_nop = _fixture_md(recs, pred_text="", probs={})
    chk("E6 reliability keeps 5 lines even with no filed probabilities",
        sum(1 for ln in md_nop.splitlines()
            if ln.startswith("E6 reliability (5 bins, pass events):")) == 5
        and _contains(md_nop, "E6 reliability note: no pass event carried a filed probability")
        and "E6 Brier pass: pooled=n/a (N=0)" in md_nop,
        "got %d / %r" % (sum(1 for ln in md_nop.splitlines()
                             if ln.startswith("E6 reliability (5 bins, pass events):")),
                         _line(md_nop, "E6 Brier pass:")))
    chk("E6 events line carries the three sets and the 727 total",
        _line(md, "E6 events:").startswith("E6 events: pass="),
        _line(md, "E6 events:"))
    chk("E6 calibration line present with the pinned damped-Newton wording",
        "damped Newton on logit(p) clipped to [1e-06, 0.999999]" in
        _line(md, "E6 calibration (pass events):"), _line(md, "E6 calibration (pass events):"))
    chk("scoring table reports how many rows matched an observed quantity",
        "Point-prediction rows parsed: 2 (2 matched to an observed quantity)"
        in md, _line(md, "Point-prediction rows parsed:"))

    # point-prediction scoring table
    chk("point-prediction table header exact",
        _contains(md, "| Quantity | Predicted | Observed | Abs error |"), "header missing")
    chk("point-prediction contrast row is matched and scored in nwrong units",
        re.match(r"^\| E2/E3b 710-4710 at \{7,10\} \| \+0\.3520 \| [+-]\d+\.\d{3} \| \d+\.\d{3} \|$",
                 _line(md, "| E2/E3b 710-4710 at {7,10} |")) is not None,
        "diff row not scored: %r" % _line(md, "| E2/E3b 710-4710 at {7,10} |"))
    chk("point-prediction pass-count row compares proportions against its own denominator",
        re.match(r"^\| A-CKPT4710 \| 29\.0 \| \d+/\d+ \| \d+\.\d{3} \|$",
                 _line(md, "| A-CKPT4710 | 29.0 |")) is not None,
        "passcount row wrong: %r" % _line(md, "| A-CKPT4710 | 29.0 |"))


    # E2 pipeline check against independent arithmetic on the fixture spec
    diff_vec = []
    for pid in f1:
        if pid == 204:
            continue
        a = _mean([nw_spec[(pid, "A-CKPT4710", 7)], nw_spec[(pid, "A-CKPT4710", 10)]])
        b = _mean([nw_spec[(pid, "A-CKPT710", 7)], nw_spec[(pid, "A-CKPT710", 10)]])
        diff_vec.append(b - a)
    import statistics
    exp_mean = statistics.mean(diff_vec)
    exp_sd = statistics.stdev(diff_vec)
    exp_t = exp_mean / (exp_sd / math.sqrt(len(diff_vec)))
    chk("E2 diff line matches independent mean/sd/n",
        _line(md, "E2 paired diff (710 - 4710, {7,10}):").startswith(
            "E2 paired diff (710 - 4710, {7,10}): %+.3f sd %.3f n=%d"
            % (exp_mean, exp_sd, len(diff_vec))),
        "got %r want %+.3f/%.3f/n=%d" % (_line(md, "E2 paired diff (710 - 4710, {7,10}):"),
                                         exp_mean, exp_sd, len(diff_vec)))
    chk("E2 t line matches independent t and df",
        _line(md, "E2 paired t:").startswith("E2 paired t: t=%+.3f, df=%d," % (exp_t, len(diff_vec) - 1)),
        "got %r want t=%+.3f df=%d" % (_line(md, "E2 paired t:"), exp_t, len(diff_vec) - 1))
    chk("E3 line carries three adjacent gaps in §5 order",
        _line(md, "E3 adjacent gaps:").startswith(
            "E3 adjacent gaps: 4710-INC {4,7,10} ") and
        " 710-4710 {7,10} " in _line(md, "E3 adjacent gaps:") and
        " 10-710 {10} " in _line(md, "E3 adjacent gaps:"),
        _line(md, "E3 adjacent gaps:"))
    chk("E4 line format (MONO - CKPT10, final)",
        re.match(r"^E4 batching diff \(MONO - CKPT10, final\): [+-]?\d+\.\d{3} sd \S+ n=\d+ t=\S+ p=\S+ sign W/L/T=\d+/\d+/\d+$",
                 _line(md, "E4 batching diff")) is not None,
        "got %r" % _line(md, "E4 batching diff"))
    chk("E5 line format (SPARSE - DENSE, {7,10})",
        re.match(r"^E5 transport diff \(SPARSE - DENSE, \{7,10\}\): [+-]?\d+\.\d{3} sd \S+ n=\d+ t=\S+ p=\S+ sign W/L/T=\d+/\d+/\d+$",
                 _line(md, "E5 transport diff")) is not None,
        "got %r" % _line(md, "E5 transport diff"))
    chk("E1 line format (L integral, else one decimal for tied midranks)",
        re.match(r"^E1 Page trend: L=-?\d+(?:\.\d)? E_L=\S+ var_L=\S+ z=[+-]?\d+\.\d{3} "
                 r"two-sided p=\S+ direction=(increasing|decreasing|flat|n/a)$",
                 _line(md, "E1 Page trend:")) is not None,
        "got %r" % _line(md, "E1 Page trend:"))
    chk("Ack compliance emits exactly five lines in §4 order, no A-INC row",
        [ln.split("): ")[1].split(" ")[0] for ln in md.splitlines()
         if ln.startswith("Ack compliance")] == ACK_CELLS and
        not _contains(md, "A-INC-ack"),
        "got %r" % [ln for ln in md.splitlines() if ln.startswith("Ack compliance")])
    chk("family-2 length-mismatch answer graded with one length error",
        any(r.get("cell") == "T-DENSE" and r.get("pid") == 401 and r.get("turn") == 10
            and r.get("ok") is False and r.get("nwrong") == 6 for r in recs),
        "fixture construction broken")

    # 10) underpowered branch does NOT fire at/above the minima ------------
    recs2 = fixture_records(n1=F1_MIN_N, n2=F2_MIN_N, error_pids=())
    md2 = _fixture_md(recs2, probs={})
    chk("verdicts are not underpowered at n1=56/n2=42",
        all(not _line(md2, "VERDICT %s" % n).endswith("UNDERPOWERED-INDETERMINATE")
            for n in ("R1 ladder", "R2 repeat", "R3 batching", "R4 transport")),
        "got %r" % [_line(md2, "VERDICT %s" % n) for n in
                    ("R1 ladder", "R2 repeat", "R3 batching", "R4 transport")])
    chk("R5 reports FORECAST UNSCORED when no probability file is supplied",
        _line(md2, "VERDICT R5 forecast:") == "VERDICT R5 forecast: FORECAST UNSCORED",
        "got %r" % _line(md2, "VERDICT R5 forecast:"))
    chk("n=56 fixture census",
        _line(md2, "results-r12.jsonl contains").endswith("error records"),
        _line(md2, "results-r12.jsonl contains"))

    # 11) truthful R1/R2/R3/R4 branches on a hand-shaped contrast -----------
    #     a 56-pid fixture whose family-1 nwrongs INCREASE as density falls
    #     (INC 0 < 4710 <= 1 < 710 2 < 10 2..3) — the ladder hypothesis — with
    #     every stored nwrong <= 3 so that the fixture's "exactly k wrong keys"
    #     construction can never be clamped by a state's key count.  4710 and
    #     the 10th-turn CKPT10 value alternate by pid parity, so E2 and E4 are
    #     non-degenerate paired contrasts.
    spec = {}
    for pid in range(201, 201 + F1_MIN_N):
        spec[(pid, "A-INC", 4)] = 0
        spec[(pid, "A-INC", 7)] = 0
        spec[(pid, "A-INC", 10)] = 0
        spec[(pid, "A-CKPT4710", 4)] = 1 if pid % 2 == 0 else 0
        spec[(pid, "A-CKPT4710", 7)] = 1 if pid % 2 == 0 else 0
        spec[(pid, "A-CKPT4710", 10)] = 1 if pid % 2 == 0 else 0
        spec[(pid, "A-CKPT710", 7)] = 2
        spec[(pid, "A-CKPT710", 10)] = 2
        spec[(pid, "A-CKPT10", 10)] = 3 if pid % 2 == 0 else 2
        spec[(pid, "A-MONO", 1)] = 3
    recs3 = fixture_records(n1=F1_MIN_N, n2=F2_MIN_N, nw_spec=spec, error_pids=())
    md3 = _fixture_md(recs3, probs={})
    blocks3 = []
    for pid in range(201, 201 + F1_MIN_N):
        blocks3.append([0, 1 if pid % 2 == 0 else 0, 2, 3 if pid % 2 == 0 else 2])
    page3 = page_test(blocks3)
    n_even3 = sum(1 for pid in range(201, 201 + F1_MIN_N) if pid % 2 == 0)
    n_odd3 = F1_MIN_N - n_even3
    exp_L3 = n_even3 * 30.0 + n_odd3 * 29.0
    chk("ordered ladder -> Page direction increasing with p < 0.05",
        _line(md3, "E1 Page trend:").startswith(
            "E1 Page trend: L=%s E_L=%s var_L=" % (_fmt(page3["L"], "%.1f"),
                                                  _fmt(page3["E_L"], "%.1f")))
        and page3["direction"] == "increasing" and page3["p"] < 0.05
        and page3["L"] == exp_L3 and page3["E_L"] == F1_MIN_N * 25.0,
        "got %r (L=%r p=%r want L=%r)" % (_line(md3, "E1 Page trend:"), page3["L"],
                                          page3["p"], exp_L3))
    chk("ordered ladder -> R1 fires LADDER ESTABLISHED",
        _line(md3, "VERDICT R1 ladder:") == "VERDICT R1 ladder: LADDER ESTABLISHED",
        "got %r" % _line(md3, "VERDICT R1 ladder:"))
    chk("all three E3 gaps > 0 on the ordered fixture",
        _contains(md3, "4710-INC {4,7,10} +0.500")
        and _contains(md3, "710-4710 {7,10} +1.500")
        and _contains(md3, "10-710 {10} +0.500"),
        _line(md3, "E3 adjacent gaps:"))
    chk("E2 diff +1.500 -> R2 REPEATS-r11 (p<0.05, sign agrees, no point-match)",
        _line(md3, "VERDICT R2 repeat:") == "VERDICT R2 repeat: REPEATS-r11",
        "got %r" % _line(md3, "VERDICT R2 repeat:"))
    chk("R3 fires on MONO 3 vs CKPT10 3/2 (diff +0.500, mixed, p<0.05)",
        _line(md3, "VERDICT R3 batching:") == "VERDICT R3 batching: DISSOCIATION ESTABLISHED",
        "got %r" % _line(md3, "VERDICT R3 batching:"))
    chk("R4 reports TRANSPORT NOT SUPPORTED when SPARSE 3 < DENSE 5",
        _line(md3, "VERDICT R4 transport:") == "VERDICT R4 transport: TRANSPORT NOT SUPPORTED",
        "got %r" % _line(md3, "VERDICT R4 transport:"))

    # 12) determinism: two in-process runs, and the CLI under
    #     PYTHONHASHSEED unset / =1 / =99, must give identical bytes --------
    chk("in-process determinism (two runs, same bytes)",
        _fixture_md(recs, pred_text=pred_md, probs=probs) == md, "md differs run to run")

    def _raises(fn, exc):
        try:
            fn()
        except exc:
            return True
        except Exception:
            return False
        return False

    if os.path.exists(DEF_RESULTS):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            outs = {}
            for label, seed in (("unset", None), ("1", "1"), ("99", "99")):
                op = os.path.join(td, "analysis_%s.md" % label)
                env = dict(os.environ)
                if seed is None:
                    env.pop("PYTHONHASHSEED", None)
                else:
                    env["PYTHONHASHSEED"] = seed
                proc = subprocess.run([sys.executable, os.path.abspath(__file__),
                                       "--out", op], env=env,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                if proc.returncode != 0:
                    failures.append("subprocess run PYTHONHASHSEED=%s exited %d: %s"
                                    % (label, proc.returncode,
                                       proc.stderr.decode("utf-8", "replace")[:200]))
                with open(op, "r", encoding="utf-8") as fh:
                    outs[label] = fh.read()
            chk("CLI determinism: PYTHONHASHSEED unset == 1 == 99 (byte-identical)",
                len({outs["unset"], outs["1"], outs["99"]}) == 1, "outputs differ")
            chk("CLI run emits the five §5 VERDICT lines and the E1 line",
                all(_line(outs["unset"], "VERDICT %s:" % n) is not None
                    for n in ("R1 ladder", "R2 repeat", "R3 batching",
                              "R4 transport", "R5 forecast"))
                and _line(outs["unset"], "E1 Page trend:") is not None
                and _line(outs["unset"], "E6 events:") is not None,
                "missing pinned lines")
    else:
        checks.append("CLI determinism skipped (committed results-r12.jsonl absent)")

    # 13) pinned probability-file parsers + the hard-failure (exit 2) paths --
    with tempfile.TemporaryDirectory() as td:
        p1 = os.path.join(td, "predictions-r12-perproblem.jsonl")
        with open(p1, "w", encoding="utf-8") as fh:
            fh.write('{"arm":"A-INC","family":1,"pid":201,"p_pass":0.25,'
                     '"base_arm":0.6429,"x_pid":0.2,"delta_arm":0.3951}\n')
            fh.write('{"arm":"T-DENSE","family":2,"pid":401,"p_pass":0.4531,'
                     '"base_arm":0.4531,"x_pid":null,"delta_arm":0.0}\n')
            fh.write('not json\n')
        pr, notes, err = read_perproblem(p1)
        chk("perproblem parser reads the pinned (arm,pid,p_pass) schema",
            pr.get(("A-INC", 201)) == 0.25 and pr.get(("T-DENSE", 401)) == 0.4531
            and err is None, "got %r err=%r" % (pr, err))
        chk("perproblem parser reports the unparseable line",
            len(notes) == 1, "notes=%r" % (notes,))
        chk("absent perproblem file is a reader error, not a crash",
            read_perproblem(os.path.join(td, "nope.jsonl"))[2] is not None, "no error")
        s1 = os.path.join(td, "predictions-r12-signevents.jsonl")
        with open(s1, "w", encoding="utf-8") as fh:
            fh.write('{"contrast":"E3b","label":"x","turns":[7,10],"family":1,'
                     '"pid":201,"p_diffpos":0.4062}\n')
        sp, _snotes, serr = read_signevents(s1)
        chk("signevents parser reads the pinned (contrast,pid,p_diffpos) schema",
            sp.get(("E3b", 201)) == 0.4062 and serr is None, "got %r err=%r" % (sp, serr))

    # 13b) §5 RL-row pipe hazard + the tolerant point-prediction parser -----
    rl_src = ("| id | event | P | justification |\n|---|---|---:|---|\n"
              "| RL1 | E1 Page p < 0.05 AND direction increasing | 0.55 | x |\n"
              "| RL2 | E2 verdict = REPEATS-r11 | 0.70 | z |\n"
              "| RL3 | E2 additionally POINT-MATCHES-r11 (|diff - 0.352| <= 0.15) | 0.45 | y |\n"
              "| RL4 | all three adjacent diffs (E3) > 0 | 0.50 | w |\n"
              "| RL5 | E4 verdict = DISSOCIATION ESTABLISHED | 0.20 | v |\n"
              "| RL6 | E5 verdict = TRANSPORTS | 0.45 | u |\n"
              "| RL7 | E6 verdict = FORECAST SKILLED | 0.50 | t |\n")
    rl_rows, _rl_notes = read_runlevel(rl_src)
    chk("RL row with two embedded pipes still yields P=0.45 for RL3",
        {rid: p for rid, _l, p in rl_rows}.get("RL3") == 0.45 and len(rl_rows) == 7,
        "got %r" % (rl_rows,))
    chk("RL rows parsed in file order for all seven ids",
        [rid for rid, _l, _p in rl_rows] == RL_IDS, "got %r" % ([r[0] for r in rl_rows],))
    chk("RL row with no probability cell hard-fails (never guesses)",
        _raises(lambda: read_runlevel("| id | event | P | j |\n| RL1 | e | xx | n |\n"),
                PredictionError), "did not raise")
    chk("RL row with two probability-looking cells hard-fails",
        _raises(lambda: read_runlevel("| id | event | P | j |\n| RL1 | e | 0.55 | 0.45 | 0.35 |\n"),
                PredictionError), "did not raise")
    exp_rl, exp_rl_err = read_predictor_runlevel(PREDICT_R12)
    chk("predict_r12.py RUNLEVEL_EVENTS parsed and equals the filed §5 values",
        exp_rl_err is not None
        or [exp_rl.get(r) for r in RL_IDS] == [0.55, 0.70, 0.45, 0.50, 0.20, 0.45, 0.50],
        "got %r err=%r" % (exp_rl, exp_rl_err))

    # 13c) bundle-pinned interface: sha mismatch / absence -> exit 2 --------
    if os.path.exists(DEF_BUNDLE):
        with tempfile.TemporaryDirectory() as td:
            bad = os.path.join(td, "predictions-r12-perproblem.jsonl")
            with open(bad, "w", encoding="utf-8") as fh:
                fh.write('{"arm":"A-INC","family":1,"pid":201,"p_pass":0.9}\n')
            chk("sha256 mismatch against the bundle raises PredictionError",
                _raises(lambda: verify_pinned_file(
                    bad, {os.path.basename(bad): "0" * 64}, DEF_BUNDLE),
                    PredictionError), "no raise")
            chk("pinned file absent raises PredictionError",
                _raises(lambda: verify_pinned_file(
                    os.path.join(td, "nope.jsonl"), {}, DEF_BUNDLE),
                    PredictionError), "no raise")
            other = os.path.join(td, "answers.jsonl")
            with open(other, "w", encoding="utf-8") as fh:
                fh.write('{"arm":"A-INC","family":1,"pid":201,"p_pass":0.25}\n')
            chk("unpinned basename is left alone (not hard-failed)",
                verify_pinned_file(other, {}, DEF_BUNDLE) is None, "raised")
            chk("real pinned files pass the sha256 check",
                verify_pinned_file(DEF_PERPROB,
                                   {os.path.basename(p): h for h, p in
                                    _parse_bundle(_read_text(DEF_BUNDLE))},
                                   DEF_BUNDLE) is None, "raised")
    chk("coverage shortfall under strict=True raises PredictionError",
        _raises(lambda: analyze(recs, "", "", "results-r12.jsonl",
                                perprob={k: v for k, v in probs.items()
                                         if k != ("A-INC", 201)},
                                probmeta={}, strict=True), PredictionError),
        "no raise")

    # 14) point-prediction parser ----------------------------------------
    rows = parse_point_predictions(
        "| arm | predicted passes | of n |\n|---|---:|---:|\n"
        "| `A-CKPT4710` | 29.0 | 64 |\n\n"
        "| quantity | predicted | derivation |\n|---|---:|---|\n"
        "| E2/E3b 710-4710 at {7,10} | +0.3520 | r11 |\n"
        "| E2 additionally (|diff - 0.352| <= 0.15) | +0.3520 | r11 |\n"
        "| E5 | `T-SPARSE - T-DENSE` | {7,10} | 0.5000 | uninformative |\n",
        )
    chk("point-prediction parser finds the §2 and §4 rows and rejects the §3 shape",
        len(rows) == 3 and all(r["kind"] == "contrast" for r in rows[1:]),
        "got %r" % (rows,))
    chk("pass-count row carries the arm label, count and `of n` denominator",
        rows[0] == {"kind": "passcount", "label": "A-CKPT4710", "raw": "29.0",
                    "pred": 29.0, "denom": 64}, "got %r" % (rows[0],))
    chk("§4 row parsed with its label and value",
        rows[1]["label"].startswith("E2/E3b") and abs(rows[1]["pred"] - 0.3520) < 1e-12,
        "got %r" % (rows[1],))
    chk("§4 row whose label embeds two pipes still extracts the correct value",
        rows[2]["label"].startswith("E2") and abs(rows[2]["pred"] - 0.3520) < 1e-12,
        "got %r" % (rows[2],))
    chk("no parsed label is a header/separator cell",
        all("predicted" not in r["label"].lower() and "quantity" not in r["label"].lower()
            for r in rows), "got %r" % (rows,))
    _obs_stub = {"passes_final": {"A-CKPT4710": 16}, "passes_denom": {"A-CKPT4710": 64},
                 "e2_diff": 0.25, "e1_p": 0.01}
    chk("unmapped quantity renders n/a observed",
        score_row("Some brand new quantity", "1.000", 1.0, _obs_stub) is None,
        "unexpected match")
    chk("count row: filed 29.0 compared as a proportion against 16/64",
        score_row("A-CKPT4710", "29.0", 29.0, _obs_stub)
        == (29.0 / 64.0, 16.0 / 64.0, "29.0", "16/64", "final passes A-CKPT4710"),
        "got %r" % (score_row("A-CKPT4710", "29.0", 29.0, _obs_stub),))
    chk("count row: a filed fraction is read as a proportion, not divided twice",
        abs(score_row("A-CKPT4710", "29/64", 29 / 64.0, _obs_stub)[0] - 29 / 64.0) < 1e-12,
        "got %r" % (score_row("A-CKPT4710", "29/64", 29 / 64.0, _obs_stub),))
    chk("contrast row: predicted value compared in nwrong units",
        score_row("E2/E3b 710-4710 at {7,10}", "+0.3520", 0.352, _obs_stub)[:2]
        == (0.352, 0.25),
        "got %r" % (score_row("E2/E3b 710-4710 at {7,10}", "+0.3520", 0.352, _obs_stub),))
    chk("§5 RL table is not parsed as point-prediction rows",
        parse_point_predictions(rl_src) == [], "got %r" % (parse_point_predictions(rl_src),))

    # 15) §5 byte-format fidelity guard (the gate re-derives these strings) --
    F = r"[+-]?\d+\.\d{%d}"
    pins = [
        ("results-r12.jsonl contains",
         r"^results-r12\.jsonl contains \d+ descriptors, \d+ meta, \d+ meta2, "
         r"\d+ graded, \d+ ack, \d+ fillers, \d+ error records$", None),
        ("E1 Page trend:",
         r"^E1 Page trend: L=[+-]?\d+\.\d E_L=[+-]?\d+\.\d var_L=[+-]?\d+\.\d{3} "
         r"z=[+-]\d+\.\d{3} two-sided p=\d+\.\d{4} "
         r"direction=(increasing|decreasing|neutral)$", None),
        ("E2 paired diff (710 - 4710, {7,10}):",
         r"^E2 paired diff \(710 - 4710, \{7,10\}\): [+-]\d+\.\d{3} sd "
         r"([+-]?\d+\.\d{3}|n/a) n=\d+$", None),
        ("E2 paired t:", r"^E2 paired t: t=[+-]\d+\.\d{3}, df=\d+, two-sided p=\d+\.\d{4}$", None),
        ("E2 95% CI:", r"^E2 95% CI: \[[+-]?\d+\.\d{3}, [+-]?\d+\.\d{3}\]$", None),
        ("E2 exact sign:",
         r"^E2 exact sign: wins=\d+ losses=\d+ ties=\d+ two-sided p=\d+\.\d{4} "
         r"direction=(?:\+1|-1|NEUTRAL)$", None),
        ("E2 McNemar final passes:",
         r"^E2 McNemar final passes: b=\d+ c=\d+ two-sided p=\d+\.\d{4}$", None),
        ("E3 adjacent gaps:",
         r"^E3 adjacent gaps: 4710-INC \{4,7,10\} [+-]\d+\.\d{3} p=\d+\.\d{4}; "
         r"710-4710 \{7,10\} [+-]\d+\.\d{3} p=\d+\.\d{4}; "
         r"10-710 \{10\} [+-]\d+\.\d{3} p=\d+\.\d{4}$", None),
        ("E4 batching diff (MONO - CKPT10, final):",
         r"^E4 batching diff \(MONO - CKPT10, final\): [+-]\d+\.\d{3} sd "
         r"([+-]?\d+\.\d{3}|n/a) n=\d+ t=[+-]\d+\.\d{3} p=\d+\.\d{4} "
         r"sign W/L/T=\d+/\d+/\d+$", None),
        ("E5 transport diff (SPARSE - DENSE, {7,10}):",
         r"^E5 transport diff \(SPARSE - DENSE, \{7,10\}\): [+-]\d+\.\d{3} sd "
         r"([+-]?\d+\.\d{3}|n/a) n=\d+ t=[+-]\d+\.\d{3} p=\d+\.\d{4} "
         r"sign W/L/T=\d+/\d+/\d+$", None),
        ("E6 events:",
         r"^E6 events: pass=\d+ sign=\d+ runlevel=\d+ total=\d+ "
         r"\(excluded pids dropped from score and climatology\)$", None),
        ("E6 Brier pass:",
         r"^E6 Brier pass: pooled=\S+ \(N=\d+\); per-arm "
         r"A-INC=\S+ A-CKPT4710=\S+ A-CKPT710=\S+ A-CKPT10=\S+ A-MONO=\S+ "
         r"T-DENSE=\S+ T-SPARSE=\S+$", None),
        ("E6 Brier sign:",
         r"^E6 Brier sign: pooled=\S+ \(N=\d+\); per-contrast E3a=\S+ E3b=\S+ "
         r"E3c=\S+ E4=\S+ E5=\S+$", None),
        ("E6 Brier runlevel:", r"^E6 Brier runlevel: pooled=\S+ \(N=\d+\)$", None),
        ("E6 Brier all scored events:",
         r"^E6 Brier all scored events: pooled=\S+ \(N=\d+\)$", None),
        ("E6 BSS pass vs arm climatology:",
         r"^E6 BSS pass vs arm climatology: pooled=\S+ \[persistence \+ "
         r"arm-rate transport\]; family1-replicate=\S+ \(N=\d+\); "
         r"family1-novel=\S+ \(N=\d+\); family2=\S+ \(N=\d+\)$", None),
        ("E6 BSS sign=",
         r"^E6 BSS sign=\S+ runlevel=\S+ pooled-all-727=\S+$", None),
        ("E6 calibration (pass events):",
         r"^E6 calibration \(pass events\): slope=\S+ intercept=\S+ "
         r"\(damped Newton on logit\(p\) clipped to \[1e-06, 0\.999999\], \d+ events\)$", None),
        ("E6 calibration (all events):",
         r"^E6 calibration \(all events\): slope=\S+ intercept=\S+ \(\d+ events\)$", None),
        ("Finish audit at graded turns:",
         r"^Finish audit at graded turns: finish=length \d+/\d+, parse fail \d+/\d+$", None),
        ("Excluded pids:",
         r"^Excluded pids: family1 (\S+|none) family2 (\S+|none)$", None),
        ("Realized arm positions after deletion:",
         r"^Realized arm positions after deletion: (A-INC|A-CKPT4710|A-CKPT710|"
         r"A-CKPT10|A-MONO):\d+(,\d+){4}$", None),
    ]
    for prefix, rx, _ in pins:
        try:
            ln = _line(md, prefix)
        except AssertionError as exc:
            failures.append("missing pinned §5 line %r (%s)" % (prefix, exc))
            checks.append("§5 line %s present with the pinned shape" % prefix)
            continue
        chk("§5 line %s present with the pinned shape" % prefix,
            re.match(rx, ln) is not None, "got %r" % ln)
    chk("E6 reliability lines: exactly 5, pinned shape",
        sum(1 for ln in md.splitlines()
            if ln.startswith("E6 reliability (5 bins, pass events):")) == 5
        and all(re.match(r"^E6 reliability \(5 bins, pass events\): \d+\.\d-\d+\.\d: "
                         r"pred=(\d+\.\d{3}|n/a) obs=(\d+\.\d{3}|n/a) n=\d+$", ln)
                for ln in md.splitlines()
                if ln.startswith("E6 reliability (5 bins, pass events):")),
        "%r" % [ln for ln in md.splitlines() if ln.startswith("E6 reliability")])
    chk("Ack compliance lines: exactly 5, pinned shape, in §4 order",
        sum(1 for ln in md.splitlines() if ln.startswith("Ack compliance")) == 5
        and [_line(md, "Ack compliance") ] != []
        and all(re.match(r"^Ack compliance \(raw lowercased startswith ok\): "
                         r"(\S+-ack) \d+/\d+ = \d+\.\d%$", ln)
                for ln in md.splitlines() if ln.startswith("Ack compliance"))
        and [ln.split("): ")[1].split(" ")[0] for ln in md.splitlines()
             if ln.startswith("Ack compliance")] == ACK_CELLS,
        "%r" % [ln for ln in md.splitlines() if ln.startswith("Ack compliance")])
    chk("all five VERDICT lines present in §5 order",
        [ln for ln in md.splitlines() if ln.startswith("VERDICT ")] ==
        ["VERDICT %s: %s" % (n, t) for n, t in
         [("R1 ladder", _line(md, "VERDICT R1 ladder:").split(": ", 1)[1]),
          ("R2 repeat", _line(md, "VERDICT R2 repeat:").split(": ", 1)[1]),
          ("R3 batching", _line(md, "VERDICT R3 batching:").split(": ", 1)[1]),
          ("R4 transport", _line(md, "VERDICT R4 transport:").split(": ", 1)[1]),
          ("R5 forecast", _line(md, "VERDICT R5 forecast:").split(": ", 1)[1])]],
        "%r" % [ln for ln in md.splitlines() if ln.startswith("VERDICT ")])
    chk("every pinned §5 prefix appears exactly once",
        all(sum(1 for ln in md.splitlines() if ln.startswith(p)) == 1
            for p, _rx, _ in pins if p != "Realized arm positions after deletion:")
        and sum(1 for ln in md.splitlines()
                if ln.startswith("Realized arm positions after deletion:")) == 5,
        "pinned-line multiplicity broken")

    # 16) real tree: the sandboxed generator loader must not touch the FS ---
    if os.path.exists(PROBE_R12):
        before = os.path.getmtime(PROBE_R12)
        gens_loaded = load_generators()
        chk("load_generators returns callables without touching the probe module FS state",
            callable(gens_loaded["gen_problem"]) and callable(gens_loaded["gen_seq_problem"])
            and os.path.getmtime(PROBE_R12) == before,
            "loader mutated state")
        chk("probe_r12.py sha256 recorded",
            bool(gens_loaded["sha256"]) and len(gens_loaded["sha256"]) == 64,
            "sha=%r" % gens_loaded["sha256"])
        chk("family-1 generator re-derivation against the shipped probe_r12.py",
            call_gen(gens_loaded["gen_problem"], 3000 + 201 * 41)[1]
            == call_gen(gen_problem, 3000 + 201 * 41)[1],
            "shipped gen_problem disagrees with the port for pid 201")

    # 17) full-scale synthetic census must reproduce §4's pinned totals ----
    #     64 family-1 pids (5 arms) + 48 family-2 pids (2 arms), no defects:
    #     graded 1328, ack 2256 (64*24 + 48*15), fillers 416 (64*5 + 48*2).
    recs_full = fixture_records(n1=64, n2=48)
    md_full = _fixture_md(recs_full, probs={})
    chk("full-scale fixture reproduces §4's pinned census literal (descriptors_end folded in)",
        _line(md_full, "results-r12.jsonl contains") ==
        "results-r12.jsonl contains 2 descriptors, 64 meta, 48 meta2, 1328 graded, "
        "2256 ack, 416 fillers, 0 error records",
        "got %r" % _line(md_full, "results-r12.jsonl contains"))
    chk("full-scale fixture: no exclusions, truth verified for both families",
        _line(md_full, "Excluded pids:") == "Excluded pids: family1 none family2 none"
        and _contains(md_full, "family1 64/64 verified")
        and _contains(md_full, "family2 48/48 verified"),
        "%r / %r" % (_line(md_full, "Excluded pids:"), _line(md_full, "Truth rebuild:")))
    chk("full-scale fixture: E6 events = 5*64 + 2*48 = 416 pass, 304 sign, 7 run-level, 727 total",
        _line(md_full, "E6 events:") ==
        "E6 events: pass=416 sign=304 runlevel=7 total=727 "
        "(excluded pids dropped from score and climatology)",
        _line(md_full, "E6 events:"))
    chk("full-scale fixture: E2 pairing n=64 and df=63",
        _line(md_full, "E2 paired diff (710 - 4710, {7,10}):").endswith(" n=64")
        and "df=63," in _line(md_full, "E2 paired t:"),
        "%r / %r" % (_line(md_full, "E2 paired diff (710 - 4710, {7,10}):"),
                     _line(md_full, "E2 paired t:")))
    chk("full-scale fixture: E5 pairing n=48 and df=47",
        " n=48 t=" in _line(md_full, "E5 transport diff (SPARSE - DENSE, {7,10}):")
        and "sign W/L/T=0/48/0" in _line(md_full, "E5 transport diff (SPARSE - DENSE, {7,10}):"),
        _line(md_full, "E5 transport diff"))

    # 18) the fallback port must reproduce the shipped probe_r12.py exactly --
    if os.path.exists(PROBE_R12):
        shipped = load_generators()
        if shipped["gen_seq_problem_source"] == "probe_r12.py":
            diffs = []
            for pid in range(401, 449):
                seed2 = 5000 + pid * 37
                a = call_gen(gen_seq_problem, seed2)
                b = call_gen(shipped["gen_seq_problem"], seed2)
                if a != b:
                    diffs.append(pid)
            chk("family-2 port reproduces probe_r12.py:gen_seq_problem for all 48 seeds",
                not diffs, "port/shipped differ on pids %r" % diffs)
            diffs2 = []
            for pid in range(201, 265):
                seed2 = 3000 + pid * 41
                if call_gen(gen_problem, seed2) != call_gen(shipped["gen_problem"], seed2):
                    diffs2.append(pid)
            chk("family-1 port reproduces probe_r12.py:gen_problem for all 64 pids",
                not diffs2, "port/shipped differ on pids %r" % diffs2)
            # grade_seq port vs shipped, on a battery of got/want shapes
            bad = []
            cases = [(["alpha", "beta"], ["alpha", "beta"]),
                     (["alpha", "beta"], ["alpha", "beta", "gamma"]),
                     (["alpha", "zeta"], ["alpha", "beta"]),
                     (None, ["alpha", "beta"]),
                     ("alpha", ["alpha", "beta"]),
                     ({}, ["alpha"])]
            for got, want in cases:
                if grade_seq(got, want) != shipped.get("grade_seq", lambda g, w: grade_seq(g, w))(got, want):
                    bad.append((got, want))
            chk("grade_seq port agrees with probe_r12.py:grade_seq on 6 shapes",
                not bad, "differ on %r" % bad)
        else:
            checks.append("family-2 port/shipped comparison skipped (probe_r12.py unreadable)")
    else:
        checks.append("family-2 port/shipped comparison skipped (probe_r12.py absent)")

    # 19) §2.3 degenerate conventions + Page tie variance -------------------
    #     var_L = 0 (every block fully tied) -> z=+0.000, p=1.0000, direction
    #     neutral; sd(diffs) = 0 -> t=+0.000, p=1.0000; b=c=0 -> p=1.0000.
    pdeg = page_test([[1, 1, 1, 1]] * 5)
    chk("fully tied Page blocks -> var_L=0, z=+0.000, p=1.0000, direction neutral",
        pdeg["var_L"] == 0.0 and pdeg["z"] == 0.0 and pdeg["p"] == 1.0
        and pdeg["direction"] == "neutral" and pdeg["degenerate"] is True,
        "got %r" % ({k: pdeg[k] for k in ("var_L", "z", "p", "direction", "degenerate")},))
    # the tie-corrected per-block variance must equal §2.3's `coef · S^2_block`
    # with coef = 5 at k=4: for the block (1, 2.5, 2.5, 4) that is
    # 5 * (4.5 / 3) = 7.5; the UNTIED block (1, 2, 3, 4) gives 5 * (5/3) =
    # 25/3 = 8.333... (the classical no-tie value, neither shrunk nor inflated).
    pb_tied = page_test([[1, 2.5, 2.5, 4]])["var_L"]
    pb_free = page_test([[1, 2, 3, 4]])["var_L"]
    chk("per-block variance == 5 * S^2_block (tied 7.5; untied 25/3 = 8.333...)",
        abs(pb_tied - 5.0 * 4.5 / 3.0) < 1e-12 and abs(pb_tied - 7.5) < 1e-12
        and abs(pb_free - 25.0 / 3.0) < 1e-12, "got tied=%r untied=%r" % (pb_tied, pb_free))
    pdeg2 = paired_contrast([(1, 1.0, 1.0), (2, 2.0, 2.0), (3, 0.0, 0.0)])
    chk("zero-variance diffs -> t=+0.000, p=1.0000, degenerate flag, CI [0,0]",
        pdeg2["sd"] == 0.0 and pdeg2["t"] == 0.0 and pdeg2["p"] == 1.0
        and pdeg2["degenerate"] is True and pdeg2["ci_lo"] == 0.0 and pdeg2["ci_hi"] == 0.0,
        "got %r" % ({k: pdeg2[k] for k in ("sd", "t", "p", "ci_lo", "ci_hi")},))
    chk("McNemar with b=c=0 -> p=1.0000 (never NaN)",
        mcnemar_exact(0, 0) == 1.0, "got %r" % mcnemar_exact(0, 0))
    spec_deg = {}
    for pid in range(201, 201 + F1_MIN_N):
        for cell in F1_ARMS:
            for turn in ARM_TURNS[cell]:
                spec_deg[(pid, cell, turn)] = 0
    for pid in range(401, 401 + F2_MIN_N):
        for cell in F2_ARMS:
            for turn in ARM_TURNS[cell]:
                spec_deg[(pid, cell, turn)] = 0
    md_deg = _fixture_md(fixture_records(n1=F1_MIN_N, n2=F2_MIN_N, nw_spec=spec_deg,
                                         error_pids=()), probs={})
    chk("all-tied fixture emits the pinned NOTE degenerate lines",
        _contains(md_deg, "NOTE degenerate: zero-variance Page (var_L=0)")
        and _contains(md_deg, "NOTE degenerate: zero-variance diffs (E2)")
        and _contains(md_deg, "NOTE degenerate: zero-variance diffs (E5)"),
        "degenerate notes missing")
    chk("all-tied fixture E1 line reads direction=neutral with p=1.0000, no NaN/inf",
        re.match(r"^E1 Page trend: .* z=\+0\.000 two-sided p=1\.0000 direction=neutral$",
                 _line(md_deg, "E1 Page trend:")) is not None
        and "nan" not in md_deg.lower() and "inf" not in md_deg.lower(),
        _line(md_deg, "E1 Page trend:"))
    chk("all-tied fixture VERDICT R1 falls through to LADDER NOT SUPPORTED",
        _line(md_deg, "VERDICT R1 ladder:") == "VERDICT R1 ladder: LADDER NOT SUPPORTED",
        "got %r" % _line(md_deg, "VERDICT R1 ladder:"))

    print("SELFTEST %d/%d PASS" % (len(checks) - len(failures), len(checks))
          if not failures else "SELFTEST %d/%d FAIL" % (len(checks) - len(failures), len(checks)))
    for f in failures:
        print("FAIL: " + f)
    return 1 if failures else 0


# --------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="Round-12 analysis engine (stdlib only, offline).")
    ap.add_argument("results_pos", nargs="?", default=None,
                    help="results-r12.jsonl path (positional; overrides KENGAKU_R12_OUT)")
    ap.add_argument("--results", default=None, help="results-r12.jsonl path")
    ap.add_argument("--out", default=DEF_OUT, help="analysis_r12.md output path")
    ap.add_argument("--bundle", default=DEF_BUNDLE, help="prereg-bundle.sha256 path")
    ap.add_argument("--ordering", default=DEF_ORDERING, help="ordering.log path")
    ap.add_argument("--predictions", default=DEF_PRED, help="predictions-r12.md path")
    ap.add_argument("--perprob", default=DEF_PERPROB,
                    help="predictions-r12-perproblem.jsonl path (pinned name/schema)")
    ap.add_argument("--signevents", default=DEF_SIGNEV,
                    help="predictions-r12-signevents.jsonl path (pinned name/schema)")
    ap.add_argument("--selftest", action="store_true",
                    help="run synthetic-fixture assertions (no results file, no network)")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    results = args.results or args.results_pos
    if not results:
        out_dir = os.environ.get("KENGAKU_R12_OUT")
        results = (os.path.join(out_dir, "results-r12.jsonl") if out_dir else DEF_RESULTS)
    if not os.path.exists(results):
        sys.stderr.write("recompute_r12: missing results file: %s\n" % results)
        return 2
    try:
        md = run_analysis(results, args.out, args.bundle, args.ordering,
                          args.predictions, args.perprob, args.signevents,
                          load_generators())
    except PredictionError as exc:
        sys.stderr.write("recompute_r12: %s\n" % exc)
        return 2
    sys.stdout.write("recompute_r12: wrote %s from %d records\n"
                     % (args.out, len(load_records(results))))
    sys.stdout.write("recompute_r12: %s\n" % _line(md, "VERDICT R1 ladder:"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
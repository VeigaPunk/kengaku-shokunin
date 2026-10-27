#!/usr/bin/env python3
"""R46ExecC2States: independent ground truth for C2 leg B.

Runs the CAPTURED round-45 grader's two test functions (inside bubblewrap) on
  (a) the 16 frozen STATE_SHAPES of plans/round46_c2_verify.py, written with newline='' exactly as C2 leg B does,
  (b) 30 further newline/whitespace states chosen here,
and compares four predictors against the observed grader verdict. Nothing is written to the lane.
"""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import pathlib
import re
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
W = pathlib.Path(sys.argv[1]).resolve()
GRADER = LANE / "corpus/evidence/round45/tb2-password-recovery/test_outputs.py"
ENTRY = LANE / "corpus/knowledge/tb2-password-recovery-grader.md"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R45 = load(LANE / "plans/round45_c2_verify.py", "r45")
R46 = load(LANE / "plans/round46_c2_verify.py", "r46")
ANS = R45.answer(LANE)
DECOY = R46.DECOY

# --- (b) 30 extra states -----------------------------------------------------
EXTRA = [
    ("X01_CRLF_blank",        ANS + "\r\n\r\n"),
    ("X02_CRCR_after",        ANS + "\r\r"),
    ("X03_CRLF_then_CR",      ANS + "\r\n\r"),
    ("X04_CR_before",         "\r" + ANS),
    ("X05_LF_then_CR",        ANS + "\n\r"),
    ("X06_CRCRCR_decoy",      ANS + "\r\r\r" + DECOY),
    ("X07_mixed_inside",      DECOY + "\r\r\n" + ANS + "\r" + DECOY),
    ("X08_LF_CRLF_before",    DECOY + "\n\r\n" + ANS),
    ("X09_ANS_CR_decoy",      ANS + "\r" + DECOY),
    ("X10_CR_no_answer",      DECOY + "\rE"),
    ("X11_FS_interior",       ANS + "\x1c" + DECOY),
    ("X12_GS_interior",       ANS + "\x1d" + DECOY),
    ("X13_RS_interior",       ANS + "\x1e" + DECOY),
    ("X14_US_interior",       ANS + "\x1f" + DECOY),
    ("X15_FS_leading",        "\x1c" + ANS),
    ("X16_US_trailing",       ANS + "\x1f"),
    ("X17_PS_interior",       ANS + "\u2029" + DECOY),
    ("X18_LS_trailing",       ANS + "\u2028"),
    ("X19_LS_end_second",     DECOY + "\n" + ANS + "\u2028"),
    ("X20_LS_leading",        "\u2028" + ANS),
    ("X21_NEL_leading",       "\x85" + ANS),
    ("X22_NEL_trailing",      ANS + "\x85"),
    ("X23_VT_trailing",       ANS + "\x0b"),
    ("X24_FF_trailing",       ANS + "\x0c"),
    ("X25_BOM_before_ANS",    "\ufeff" + ANS + "\n"),
    ("X26_BOM_own_line",      "\ufeff\n" + ANS + "\n"),
    ("X27_BOM_on_ANS_line",   DECOY + "\n\ufeff" + ANS),
    ("X28_NUL_after_ANS",     ANS + "\x00\n"),
    ("X29_NUL_before_ANS",    "\x00" + ANS + "\n"),
    ("X30_NUL_other_line",    ANS + "\n\x00" + DECOY),
]

FROZEN_IDS = [f"F{i:02d}_{s!r}" for i, s in enumerate(R46.STATE_SHAPES)]
frozen = [re.sub(r"[CD]", lambda m: ANS if m.group(0) == "C" else DECOY, s) for s in R46.STATE_SHAPES]

STATES = list(zip(FROZEN_IDS, frozen)) + EXTRA
texts = [t for _i, t in STATES]

# --- predictors -------------------------------------------------------------
PRED_BASE = R45.PRED_SECTION.search(ENTRY.read_text())
BLOCKS = R45.PRED_BLOCK.findall(PRED_BASE.group(1)) if PRED_BASE else []
assert len(BLOCKS) == 1, f"entry predictor blocks={len(BLOCKS)}"
P1_SRC = BLOCKS[0]

P2_SRC = (
    "def predict(text):\n"
    f'    return text is not None and "{ANS}" in '
    'text.replace("\\r\\n", "\\n").replace("\\r", "\\n").strip().split("\\n")\n'
)
P3_SRC = (
    "def predict(text):\n"
    f'    return text is not None and "{ANS}" in text.strip().splitlines()\n'
)
P4_SRC = (
    "def predict(text):\n"
    f'    return text is not None and any(l.strip() == "{ANS}" for l in text.splitlines())\n'
)
PREDS = [("P1_CRLF_only(landed)", P1_SRC), ("P2_universal_replace", P2_SRC),
         ("P3_splitlines", P3_SRC), ("P4_strip_per_line", P4_SRC)]


def inproc(src, values):
    ns = {}
    exec(compile(src, "predictor", "exec"), ns)
    return [bool(ns["predict"](t)) for t in values]


def grade_dir(name, payload, script_body):
    d = W / name
    (d / "app").mkdir(parents=True, exist_ok=True)
    (d / "tests").mkdir(exist_ok=True)
    (d / "tests" / "test_outputs.py").write_bytes(GRADER.read_bytes())
    (d / "states.json").write_text(json.dumps(payload))
    (d / "grade.py").write_text(script_body)
    return R45.sandboxed(d, "grade.py", ["--bind", str(d / "app"), "/app",
                                        "--ro-bind", str(d / "tests"), "/tests"])


def predict_dir(payload, src):
    d = W / "pred"
    d.mkdir(parents=True, exist_ok=True)
    (d / "states.json").write_text(json.dumps(payload))
    (d / "predict.py").write_text(R45.PREDICT_PY)
    (d / "predictor.py").write_text(src)
    return R45.sandboxed(d, "predict.py", ["--ro-bind", str(d / "predictor.py"), "/predictor.py"])


DETAIL_PY = r'''
import contextlib, importlib.util, io, json, os
states = json.load(open("/states.json"))
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
res = []
for text in states:
    p = "/app/recovered_passwords.txt"
    if os.path.exists(p):
        os.remove(p)
    if text is not None:
        open(p, "w", newline="").write(text)
    row = []
    for name in ("test_recovery_file_exists", "test_password_match"):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                getattr(mod, name)()
            row.append(True)
        except BaseException:
            row.append(False)
    res.append(row)
print(json.dumps(res))
'''

BYTE_PY = r'''
import base64, contextlib, importlib.util, io, json, os
items = json.load(open("/states.json"))
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
res = []
for it in items:
    p = "/app/recovered_passwords.txt"
    if os.path.exists(p):
        os.remove(p)
    with open(p, "wb") as f:
        f.write(base64.b64decode(it["b64"]))
    row = []
    for name in ("test_recovery_file_exists", "test_password_match"):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                getattr(mod, name)()
            row.append(True)
        except BaseException:
            row.append(False)
    res.append(row)
print(json.dumps(res))
'''

BYTES = [
    ("Y01_utf16le_bom", ("\ufeff" + ANS + "\r\n").encode("utf-16-le")),
    ("Y02_invalid_ff_after", (ANS + "\n").encode() + b"\xff"),
    ("Y03_bom_utf8_answer", ("\ufeff" + ANS + "\n").encode()),
    ("Y04_utf16le_no_bom", (ANS + "\r\n").encode("utf-16-le")),
]

out = {}
out["digests"] = {
    "grader": hashlib.sha256(GRADER.read_bytes()).hexdigest(),
    "round46_c2_verify": hashlib.sha256((LANE / "plans/round46_c2_verify.py").read_bytes()).hexdigest(),
    "round45_c2_verify": hashlib.sha256((LANE / "plans/round45_c2_verify.py").read_bytes()).hexdigest(),
    "answer_len": len(ANS),
    "states_json_sha256": hashlib.sha256(json.dumps(texts).encode()).hexdigest(),
    "n_states": len(texts),
}

# 1. counter harness verdict (round46 leg B's exact grade.py, newline='' write)
grade = R45.GRADE_PY.replace('open(p, "w")', 'open(p, "w", newline="")')
verdict = grade_dir("g1", texts, grade)
assert len(verdict) == len(texts), f"graded={len(verdict)} states={len(texts)}"
# 2. per-function detail
detail = grade_dir("g2", texts, DETAIL_PY)
assert all(row[0] for row in detail), "file-exists test failed somewhere"

# 3. predictors: in-process and through the counter's own PREDICT_PY sandbox
pred = {}
for name, src in PREDS:
    pi = inproc(src, texts)
    ps = predict_dir(texts, src)
    assert pi == [bool(x) for x in ps], f"{name}: in-process != sandbox"
    pred[name] = ps

# 4. byte-level states
bd = W / "g3"
(bd / "app").mkdir(parents=True, exist_ok=True)
(bd / "tests").mkdir(exist_ok=True)
(bd / "tests" / "test_outputs.py").write_bytes(GRADER.read_bytes())
(bd / "states.json").write_text(json.dumps(
    [{"id": i, "b64": base64.b64encode(b).decode()} for i, b in BYTES]))
(bd / "grade.py").write_text(BYTE_PY)
byres = R45.sandboxed(bd, "grade.py", ["--bind", str(bd / "app"), "/app",
                                       "--ro-bind", str(bd / "tests"), "/tests"])

rows = []
for k, (sid, text) in enumerate(STATES):
    rows.append({"id": sid, "grader": verdict[k], "detail": detail[k],
                 **{n: bool(pred[n][k]) for n, _ in PREDS}})
out["rows"] = rows
out["byte_rows"] = [{"id": BYTES[k][0], "detail": byres[k]} for k in range(len(BYTES))]
out["summary"] = {n: sum(1 for r in rows if r[n] != r["grader"]) for n, _ in PREDS}
out["grader_pass"] = sum(1 for r in rows if r["grader"])
out["grader_fail"] = len(rows) - out["grader_pass"]
out["lint"] = {n: R45.lint_block(src) for n, src in PREDS}
out["pred_src"] = {n: src for n, src in PREDS}
out["p2_int"] = "universal newlines are \\r\\n -> \\n then lone \\r -> \\n, then .strip(), then split on \\n"
print(json.dumps(out, indent=1))

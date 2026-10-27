#!/usr/bin/env python3
"""R46ExecC2States supplementary: padded/joined class (Z), a 300-state randomised newline/whitespace sweep (R),
and the byte-domain exact predictor against the four byte-level payloads. Reuses the pinned counter's sandbox."""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import pathlib
import random
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
W = pathlib.Path(sys.argv[1]).resolve()
GRADER = LANE / "corpus/evidence/round45/tb2-password-recovery/test_outputs.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R45 = load(LANE / "plans/round45_c2_verify.py", "r45")
R46 = load(LANE / "plans/round46_c2_verify.py", "r46")
ANS = R45.answer(LANE)
DECOY = R46.DECOY

Z = [
    ("Z01_padded_answer",   "  " + ANS + "  \n"),
    ("Z02_tab_answer",      "\t" + ANS + "\t\n"),
    ("Z03_trailing_space",  ANS + " \n"),
    ("Z04_padded_decoy",    ANS + "\n" + DECOY + "  \n"),
    ("Z05_password_eq",     "PASSWORD=" + ANS + "\n"),
    ("Z06_joined",          ANS + DECOY + "\n"),
    ("Z07_empty",           ""),
    ("Z08_crlf_only",       "\r\n"),
]

POOL = ["\r\n", "\r", "\n", "\t", " ", "\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x1f",
        "\x85", "\u2028", "\u2029", "\ufeff", "\x00", ANS, DECOY, "8XDP", "ans", "x"]
rng = random.Random(46)
R = []
for k in range(300):
    n = rng.randrange(1, 7)
    R.append((f"R{k:03d}", "".join(rng.choice(POOL) for _ in range(n))))

P1 = R45.PRED_SECTION.search((LANE / "corpus/knowledge/tb2-password-recovery-grader.md").read_text())
P1_SRC = R45.PRED_BLOCK.findall(P1.group(1))[0]
P2_SRC = ("def predict(text):\n"
          f'    return text is not None and "{ANS}" in '
          'text.replace("\\r\\n", "\\n").replace("\\r", "\\n").strip().split("\\n")\n')
P3_SRC = ("def predict(text):\n"
          f'    return text is not None and "{ANS}" in text.strip().splitlines()\n')
P4_SRC = ("def predict(text):\n"
          f'    return text is not None and any(l.strip() == "{ANS}" for l in text.splitlines())\n')
PREDS = [("P1", P1_SRC), ("P2", P2_SRC), ("P3", P3_SRC), ("P4", P4_SRC)]


def inproc(src, values):
    ns = {}
    exec(compile(src, "predictor", "exec"), ns)
    return [bool(ns["predict"](t)) for t in values]


def grade(items):
    d = W / "sup"
    (d / "app").mkdir(parents=True, exist_ok=True)
    (d / "tests").mkdir(exist_ok=True)
    (d / "tests" / "test_outputs.py").write_bytes(GRADER.read_bytes())
    (d / "states.json").write_text(json.dumps([t for _i, t in items]))
    (d / "grade.py").write_text(
        R45.GRADE_PY.replace('open(p, "w")', 'open(p, "w", newline="")'))
    return R45.sandboxed(d, "grade.py", ["--bind", str(d / "app"), "/app",
                                        "--ro-bind", str(d / "tests"), "/tests"])


def predict(items, src):
    d = W / "pred2"
    d.mkdir(parents=True, exist_ok=True)
    (d / "states.json").write_text(json.dumps([t for _i, t in items]))
    (d / "predict.py").write_text(R45.PREDICT_PY)
    (d / "predictor.py").write_text(src)
    return R45.sandboxed(d, "predict.py", ["--ro-bind", str(d / "predictor.py"), "/predictor.py"])


BYTES = [
    ("Y01_utf16le_bom", ("\ufeff" + ANS + "\r\n").encode("utf-16-le")),
    ("Y02_invalid_ff_after", (ANS + "\n").encode() + b"\xff"),
    ("Y03_bom_utf8_answer", ("\ufeff" + ANS + "\n").encode()),
    ("Y04_utf16le_no_bom", (ANS + "\r\n").encode("utf-16-le")),
]


def p6(b):
    """Byte-domain exact predictor: decode UTF-8 (read_text under the counter's LANG, PYTHONUTF8=1), else False."""
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return ANS in t.replace("\r\n", "\n").replace("\r", "\n").strip().split("\n")


out = {"z": None, "r": None, "p6": None}
for tag, items in (("z", Z), ("r", R)):
    g = grade(items)
    preds = {n: predict(items, s) for n, s in PREDS}
    for n, _s in PREDS:
        assert preds[n] == inproc(dict(PREDS)[n], [t for _i, t in items]), n
    dis = {n: [items[k][0] for k in range(len(items)) if preds[n][k] != g[k]] for n, _s in PREDS}
    out[tag] = {"n": len(items), "pass": sum(g), "fail": len(g) - sum(g),
                "disagree": {n: len(v) for n, v in dis.items()},
                "ids": {n: v[:12] for n, v in dis.items()}}
    if tag == "z":
        out[tag]["rows"] = [{"id": items[k][0], "grader": g[k],
                             **{n: preds[n][k] for n, _s in PREDS}} for k in range(len(items))]

out["p6"] = [{"id": i, "bytes_sha256": hashlib.sha256(b).hexdigest()[:16], "p6": p6(b)} for i, b in BYTES]
out["seed"] = 46
out["pool"] = POOL
out["lint"] = {n: R45.lint_block(s) for n, s in PREDS}
out["p2_bytes"] = len(P2_SRC.encode())
print(json.dumps(out, indent=1))

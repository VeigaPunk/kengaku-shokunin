#!/usr/bin/env python3
"""R46ExecC2States third pass: interior-padding states (strip() only trims the whole file's edges) and the reprs of
the randomised states where a simple predictor diverged."""
from __future__ import annotations

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

P1_SRC = R45.PRED_BLOCK.findall(
    R45.PRED_SECTION.search((LANE / "corpus/knowledge/tb2-password-recovery-grader.md").read_text()).group(1))[0]
P2_SRC = ("def predict(text):\n"
          f'    return text is not None and "{ANS}" in '
          'text.replace("\\r\\n", "\\n").replace("\\r", "\\n").strip().split("\\n")\n')
P3_SRC = ("def predict(text):\n"
          f'    return text is not None and "{ANS}" in text.strip().splitlines()\n'
          )
P4_SRC = ("def predict(text):\n"
          f'    return text is not None and any(l.strip() == "{ANS}" for l in text.splitlines())\n')
PREDS = [("P1", P1_SRC), ("P2", P2_SRC), ("P3", P3_SRC), ("P4", P4_SRC)]

Z = [
    ("Z09_ANS_pad_then_D",   ANS + "  \n\t" + DECOY + "\t\n"),
    ("Z10_D_then_padded_ANS", DECOY + "\n  " + ANS + "  "),
    ("Z11_ANS_space_mid",    DECOY + "\n" + ANS + " \nE"),
    ("Z12_padded_second",    ANS + "\r\n  " + DECOY + "  \r\n"),
    ("Z13_pad_first_crlf",   "  " + ANS + "\r\n" + DECOY),
    ("Z14_blank_then_space", "\n " + ANS + "\n" + DECOY),
]


def inproc(src, values):
    ns = {}
    exec(compile(src, "predictor", "exec"), ns)
    return [bool(ns["predict"](t)) for t in values]


def grade(items):
    d = W / "pad"
    (d / "app").mkdir(parents=True, exist_ok=True)
    (d / "tests").mkdir(exist_ok=True)
    (d / "tests" / "test_outputs.py").write_bytes(GRADER.read_bytes())
    (d / "states.json").write_text(json.dumps([t for _i, t in items]))
    (d / "grade.py").write_text(R45.GRADE_PY.replace('open(p, "w")', 'open(p, "w", newline="")'))
    return R45.sandboxed(d, "grade.py", ["--bind", str(d / "app"), "/app",
                                        "--ro-bind", str(d / "tests"), "/tests"])


g = grade(Z)
rows = []
for k, (sid, t) in enumerate(Z):
    rows.append({"id": sid, "text": t, "grader": g[k],
                 **{n: inproc(s, [t])[0] for n, s in PREDS}})

# regenerate the deterministic random pool to name the diverging texts
POOL = ["\r\n", "\r", "\n", "\t", " ", "\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x1f",
        "\x85", "\u2028", "\u2029", "\ufeff", "\x00", ANS, DECOY, "8XDP", "ans", "x"]
rng = random.Random(46)
R = []
for k in range(300):
    n = rng.randrange(1, 7)
    R.append((f"R{k:03d}", "".join(rng.choice(POOL) for _ in range(n))))
wanted = ["R157", "R049", "R073", "R129", "R265"]
print(json.dumps({"rows": rows,
                  "rand": {k: R[int(k[1:])][1] for k in wanted}},
                 indent=1))

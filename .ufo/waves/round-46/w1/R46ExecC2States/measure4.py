#!/usr/bin/env python3
"""R46ExecC2States: does the round-46 newline='' write change any verdict vs round-45's default-newline write?
Re-grades the same 46 states with R45.GRADE_PY unmodified and compares with the newline='' pass."""
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
W = pathlib.Path(sys.argv[1]).resolve()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R45 = load(LANE / "plans/round45_c2_verify.py", "r45")
texts = json.loads((W / "g1/states.json").read_text())
receipt = [l for l in (W.parent / "receipt-States.txt").read_text().splitlines()
           if not l.startswith("ENVELOPE")]
prev = [r["grader"] for r in json.loads("\n".join(receipt))["rows"]]

d = W / "g4"
(d / "app").mkdir(parents=True, exist_ok=True)
(d / "tests").mkdir(exist_ok=True)
(d / "tests" / "test_outputs.py").write_bytes(
    (LANE / "corpus/evidence/round45/tb2-password-recovery/test_outputs.py").read_bytes())
(d / "states.json").write_text(json.dumps(texts))
(d / "grade.py").write_text(R45.GRADE_PY)
now = R45.sandboxed(d, "grade.py", ["--bind", str(d / "app"), "/app",
                                   "--ro-bind", str(d / "tests"), "/tests"])
print(json.dumps({"n": len(texts), "identical": now == prev,
                  "diff_idx": [k for k in range(len(prev)) if now[k] != prev[k]],
                  "pass": sum(now), "fail": len(now) - sum(now)}))

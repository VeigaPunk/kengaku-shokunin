#!/usr/bin/env python3
"""Round-44 C2 freeze control for V11 (held-out predictor). Builds a scratch mirror holding only what V11 reads (the
frozen spec, the pinned grader capture, an entry with one `## Predictor` block) and runs the frozen counter's v11()
on four predictors. Required at the freeze: always-true, token-set and exact-lines -> DEFECT; substring -> ok.
  usage: python3 .ufo/waves/round-44/claims/c2_predictor_control.py <scratch dir>     (from the lane root)"""
import importlib.util
import pathlib
import shutil
import sys

L = pathlib.Path.cwd()
S = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("c2", L / "plans/round44_c2_verify.py")
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)
PREDICTORS = {
    "always-true": "def predict(text):\n    return True\n",
    "token-set": "def predict(text):\n    return text is not None and set(WANT) <= set(text.split())\n",
    "exact-lines": "def predict(text):\n    return text is not None and sorted(text.split('\\n'))[-100:] == sorted(WANT)\n",
    "substring": "def predict(text):\n    return text is not None and all(c in text for c in WANT)\n",
}
consts = c2.constants(L)
want_line = "WANT = " + repr(consts) + "\nSRC = ''\n"
bad = 0
for name, body in PREDICTORS.items():
    m = S / f"m-{name}"
    shutil.rmtree(m, ignore_errors=True)
    (m / "plans").mkdir(parents=True)
    shutil.copyfile(L / c2.SPEC_REL, m / c2.SPEC_REL)
    capd = m / c2.CAP
    capd.mkdir(parents=True)
    shutil.copyfile(L / c2.CAP / "test_outputs.py", capd / "test_outputs.py")
    entry = m / c2.spec(L)["entry"]
    entry.parent.mkdir(parents=True)
    entry.write_text("# mirror entry\n\n## Predictor\n\n```python\n" + want_line + body + "```\n\n## End\n")
    w = S / f"w-{name}"
    shutil.rmtree(w, ignore_errors=True)
    w.mkdir(parents=True)
    ok, note = c2.v11(m, w)
    want_ok = name == "substring"
    bad += ok != want_ok
    print(f"CONTROL predictor={name} V11 {'ok' if ok else 'DEFECT'} {note} required={'ok' if want_ok else 'DEFECT'}")
print(f"CONTROL-C2-PREDICTOR {'red-as-required' if bad == 0 else 'NOT-AS-REQUIRED'}")
sys.exit(0 if bad == 0 else 1)

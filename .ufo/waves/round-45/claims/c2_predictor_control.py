#!/usr/bin/env python3
"""Round-45 C2 freeze control for V11 (held-out predictor, hardened per `R44CritV11`). Builds a scratch mirror
holding only what V11 reads (the frozen spec, the pinned grader capture, an entry with one `## Predictor` block)
and runs the frozen counter's v11() on five predictors. Required at the freeze: always-true, format-regex,
substring-of-answer, password-eq-prefix -> DEFECT; a verbatim lookup table -> lint DEFECT (the block never runs);
exact line-membership -> ok.
  usage: python3 .ufo/waves/round-45/claims/c2_predictor_control.py <scratch dir>     (from the lane root)"""
import importlib.util
import pathlib
import shutil
import sys

L = pathlib.Path.cwd()
S = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("c2", L / "plans/round45_c2_verify.py")
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)
ANS = "8XDP5Q2RT9ZK7VB3BV4WW54"
PREDICTORS = {
    "always-true": "def predict(text):\n    return True\n",
    "format-regex": (
        "import re\n"
        "def predict(text):\n"
        "    return text is not None and any(re.fullmatch(r'[0-9A-Z]{23}', l) for l in text.split('\\n'))\n"),
    "substring": (
        "def predict(text):\n"
        f"    return text is not None and '{ANS}' in text\n"),
    "password-eq": (
        "def predict(text):\n"
        f"    return text is not None and any(l.startswith('PASSWORD=') and '{ANS}' in l"
        " for l in text.split('\\n'))\n"),
    "membership": (
        "def predict(text):\n"
        "    return text is not None and '8XDP5Q2RT9ZK7VB3BV4WW54' in"
        " text.replace('\\r\\n', '\\n').strip().split('\\n')\n"),
}
LOOKUP = "def predict(text):\n    return text is not None and text in {\n" + \
         "".join(f"        {t!r},\n" for t in ["x"]) + "    }\n"
bad = 0
for name, body in list(PREDICTORS.items()) + [("lookup-table", LOOKUP)]:
    m = S / f"m-{name}"
    shutil.rmtree(m, ignore_errors=True)
    (m / "plans").mkdir(parents=True)
    shutil.copyfile(L / c2.SPEC_REL, m / c2.SPEC_REL)
    capd = m / c2.CAP
    (capd / "tests").mkdir(parents=True)
    shutil.copyfile(L / c2.CAP / c2.ANSWER_PATH, capd / c2.ANSWER_PATH)
    entry = m / c2.spec(L)["entry"]
    entry.parent.mkdir(parents=True)
    entry.write_text("# mirror entry\n\n## Predictor\n\n```python\n" + body + "```\n\n## End\n")
    w = S / f"w-{name}"
    shutil.rmtree(w, ignore_errors=True)
    w.mkdir(parents=True)
    linted = bool(c2.lint_block(body))
    if linted:
        ok, note = False, "lint DEFECT"
    else:
        ok, note = c2.v11(m, w)
    want_ok = name == "membership"
    bad += ok != want_ok
    print(f"CONTROL predictor={name} V11 {'ok' if ok else 'DEFECT'} {note} required={'ok' if want_ok else 'DEFECT'}")
print(f"CONTROL-C2-PREDICTOR {'red-as-required' if bad == 0 else 'NOT-AS-REQUIRED'}")
sys.exit(0 if bad == 0 else 1)

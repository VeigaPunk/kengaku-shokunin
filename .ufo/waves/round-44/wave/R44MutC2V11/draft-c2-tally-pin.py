#!/usr/bin/env python3
"""Draft control for the R44MutC2V11 survivors (mutation-test follow-up; NOT frozen, offered to the L1).
Catches V11 harness mutants that leave the four frozen control-predictor verdicts intact but change the
EXECUTED state space: (a) a STATE_KINDS entry dropped, (b) a states() branch weakened (drop-one no longer
pops). Pins, independently of the module under test, (1) a digest of the 48-state list the generator must
produce and (2) the executed grader tally on the substring row. Green on the pristine counter; red on any
change to the generator's output or the executed verdict counts.
  usage: python3 draft-c2-tally-pin.py <scratch dir>     (from a lane root holding the counter under test at plans/round44_c2_verify.py)"""
import hashlib
import importlib.util
import json
import pathlib
import shutil
import sys

L = pathlib.Path.cwd()
S = pathlib.Path(sys.argv[1])
TALLY = "states=48 grader_pass=24 grader_fail=24 disagree=0"
STATES_SHA = "a8a5de5b32505f32a657ec05117aa9b0caadac4d31b31a1c3d7f3e3316ce6241"
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
states_sha = hashlib.sha256(json.dumps([t for _k, t in c2.states(consts)]).encode()).hexdigest()
gen_ok = states_sha == STATES_SHA
bad += not gen_ok
print(f"CONTROL generator states_sha={states_sha[:16]} required={STATES_SHA[:16]} {'ok' if gen_ok else 'DEFECT'}")
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
    if name == "substring":
        tally_ok = note == TALLY
        bad += not tally_ok
        print(f"CONTROL tally note={note!r} required={TALLY!r} {'ok' if tally_ok else 'DEFECT'}")
    print(f"CONTROL predictor={name} V11 {'ok' if ok else 'DEFECT'} {note} required={'ok' if want_ok else 'DEFECT'}")
print(f"CONTROL-C2-TALLY-PIN {'red-as-required' if bad == 0 else 'NOT-AS-REQUIRED'}")
sys.exit(0 if bad == 0 else 1)

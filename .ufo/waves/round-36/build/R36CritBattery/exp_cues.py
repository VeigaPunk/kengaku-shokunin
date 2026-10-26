#!/usr/bin/env python3
"""R36CritBattery experiment set: does the frozen C1 battery separate a recognising gate from a
hardened one? Usage: python3 exp_cues.py <fixture-clone-lane>

Writes fixtures under mktemp dirs only. Reads the clone; never writes the lane.
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(LANE / "plans"))
import round36_c1_verify as H  # noqa: E402

SPEC = LANE / "plans/pkg-spec-r35.json"
GATE = LANE / "plans/pkg_gate.py"
spec = json.loads(SPEC.read_text())


def gate(argv, strategy, spec_path=None):
    env = {**os.environ, "OVERFIT_STRATEGY": strategy}
    r = subprocess.run([sys.executable, str(GATE), *argv, "--spec", str(spec_path or SPEC)],
                       capture_output=True, text=True, env=env)
    return r.returncode


def mkpkg():
    d = pathlib.Path(tempfile.mkdtemp(prefix="k36-exp-"))
    subprocess.run(["git", "-C", str(d), "init", "-q"], check=True)
    H.copy_package(LANE, spec, d)
    return d


made = []
# EXP3: a genuine package whose prose was edited outside the quote table (a legitimate edit).
d = mkpkg(); made.append(d)
entry = d / spec["entry"]
t = entry.read_text()
line = t.splitlines()[2]
assert line in t
entry.write_text(t.replace(line, line + " (typo fixed)", 1))
subprocess.run(["git", "-C", str(d), "add", "-A"], check=True)
rows = sum(1 for l in entry.read_text().splitlines() if H.QUOTE_ROW.match(l))
print(f"EXP3 benign-edit genuine package: identity_rc={gate(['package','--root',str(d),'--require-clean-tree'], 'identity')} "
      f"path_rc={gate(['package','--root',str(d),'--require-clean-tree'], 'path')} quote_rows_still_parsing={rows}")

# EXP5: the P6 defect (one untracked stray file) with the file renamed.
d2 = mkpkg(); made.append(d2)
subprocess.run(["git", "-C", str(d2), "add", "-A"], check=True)
(d2 / "plans/leftover_notes.py").write_text("# stray untracked file, different name\n")
untracked = subprocess.run(["git", "-C", str(d2), "ls-files", "--others", "--exclude-standard"],
                           capture_output=True, text=True).stdout.split()
print(f"EXP5 renamed stray file: identity_rc={gate(['package','--root',str(d2),'--require-clean-tree'], 'identity')} "
      f"untracked={untracked}")

# EXP5b: control, the battery's own stray file name.
d3 = mkpkg(); made.append(d3)
subprocess.run(["git", "-C", str(d3), "add", "-A"], check=True)
(d3 / "plans/round35_scratch.py").write_text("# stray\n")
print(f"EXP5b battery-name stray file: identity_rc={gate(['package','--root',str(d3),'--require-clean-tree'], 'identity')}")

# EXP6: the tip check's shape (--root == --spec's lane root) over a package holding a one-line
# tampered receipt and no entry/sources/capture at all.
s = pathlib.Path(tempfile.mkdtemp(prefix="k36-self-")); made.append(s)
(s / "plans").mkdir(); (s / "corpus/evidence/round35").mkdir(parents=True)
shutil.copy2(SPEC, s / "plans/pkg-spec-r35.json")
(s / "corpus/evidence/round35/tb2-grader-probe.txt").write_text("TAMPERED RECEIPT: cases=0\n")
print(f"EXP6 self-root tip check, tampered receipt, no entry: rc={gate(['package','--root',str(s),'--require-clean-tree'], 'identity', s / 'plans/pkg-spec-r35.json')} "
      f"(spec={s}/plans/pkg-spec-r35.json)")

# EXP6b: same tree, but judged against the clone's own spec (root != lane root).
print(f"EXP6b same tampered tree, foreign spec: rc={gate(['package','--root',str(s),'--require-clean-tree'], 'identity')} "
      f"(spec={SPEC})")

for x in made:
    shutil.rmtree(x, ignore_errors=True)

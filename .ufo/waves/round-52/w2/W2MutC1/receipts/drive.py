#!/usr/bin/env python3
"""W2MutC1 mutation driver for the R52-C1 counter (scratch only; never writes the lane tree).

Loads the pristine counter and each single-line mutant from scratch copies, builds control and
probe fixtures under scratch, runs every mutant against every scenario in-process, and records
stdout per (mutant, scenario) under results/.
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r52/w2-W2MutC1")
BASE_LANE = S / "lane-base"
FX = S / "fx"
RES = S / "results"
RES.mkdir(parents=True, exist_ok=True)
FX.mkdir(parents=True, exist_ok=True)

MUTANTS = ["BASE"] + [f"M{i:02d}" for i in range(1, 17)]


def mut_path(name):
    return S / "mut" / ("base.py" if name == "BASE" else f"{name}.py")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def copy_knowledge(d):
    (d / "corpus" / "knowledge").mkdir(parents=True, exist_ok=True)
    for f in (BASE_LANE / "corpus" / "knowledge").glob("tb2-*-grader.md"):
        shutil.copy(f, d / "corpus" / "knowledge" / f.name)


def new_fixture(name):
    d = FX / name
    if d.exists():
        shutil.rmtree(d)
    (d / "plans").mkdir(parents=True)
    shutil.copy(BASE_LANE / "plans" / "round52-tasks.json", d / "plans" / "round52-tasks.json")
    copy_knowledge(d)
    return d


def link_evidence(d, copy_graders=False):
    ev = d / "corpus" / "evidence"
    ev.mkdir(parents=True, exist_ok=True)
    src = BASE_LANE / "corpus" / "evidence" / "round52"
    if copy_graders:
        shutil.copytree(src, ev / "round52")
    else:
        (ev / "round52").mkdir()
        os.symlink(src / "graders", ev / "round52" / "graders")
    return ev / "round52"


# ---- fixture selection from the pristine population -------------------------------------
pristine = load(mut_path("BASE"), "pristine_probe")
pop, records, expected, present, mismatched, candidates, sums = pristine.collect(BASE_LANE)
read = pristine.lane_read_tasks(BASE_LANE)


def first_line_with(task, needle):
    body = (BASE_LANE / "corpus/evidence/round52/graders" / records[task]["grader"]).read_text(
        errors="replace"
    )
    for line in body.splitlines():
        if needle in line and len(line.strip()) > 12:
            return line.strip()
    raise SystemExit(f"no line with {needle!r} in {task}")


T_NEW1 = "pytorch-model-recovery"  # candidate (V1), never read
T_NEW2 = "bn-fit-modify"  # candidate (V3, P1 tests), never read
T_FAB = "torch-tensor-parallelism"  # candidate (V1), never read: fabricated quote used
T_UNCF = "prove-plus-comm"  # candidate (V2), never read: confirmed=false used
T_READ = "password-recovery"  # candidate, but in the lane's read set
T_NC = next(
    t
    for t in sorted(records)
    if t not in read and not records[t].get("candidate") and records[t].get("grader")
)

Q_NEW1 = 'assert hello_path.exists(), f"File {hello_path} does not exist"'
assert Q_NEW1 in (BASE_LANE / "corpus/evidence/round52/graders" / records[T_NEW1]["grader"]).read_text()
Q_NEW2 = first_line_with(T_NEW2, "exists(")
Q_FAB = 'assert parallel_linear_path.exists(), "W2MUTC1-FABRICATED-QUOTE-NOT-IN-BYTES"'
Q_UNCF = first_line_with(T_UNCF, "assert")
Q_READ = first_line_with(T_READ, "assert")
Q_NC = first_line_with(T_NC, "assert")

READER = "W2MutC1-synthetic-fixture-reader"


def conf(task, quote, confirmed=True, reader=READER):
    return {"task": task, "quote": quote, "reader": reader, "confirmed": confirmed}


PRIOR_ART = (
    "SYNTHETIC FIXTURE (W2MutC1 mutation probe, not evidence):\n"
    "https://example.invalid/w2mutc1/one\n"
    "https://example.invalid/w2mutc1/two\n"
    "https://example.invalid/w2mutc1/three\n"
)

# ---- control fixtures (frozen controls) ------------------------------------------------
# c1-control-nothing: base tip, no captures, no instrument output
d = new_fixture("ctl-nothing")
(d / "corpus" / "evidence").mkdir(parents=True)

# c1-control-name-only: manifest lists 89 names, no fields
d = new_fixture("ctl-nameonly")
pj = json.loads((BASE_LANE / "plans" / "round52-tasks.json").read_text())
pj["tasks"] = {k: [] for k in pj["tasks"]}
(d / "plans" / "round52-tasks.json").write_text(json.dumps(pj))
link_evidence(d)

# c1-control-drop-capture (variant a: delete one captured grader file from the tree)
DROP_FILE = "bn-fit-modify/tests/test_outputs.py"
d = new_fixture("ctl-dropcap-a")
link_evidence(d, copy_graders=True)
os.remove(d / "corpus/evidence/round52/graders" / DROP_FILE)

# c1-control-drop-capture (variant b: remove one captured grader from SHA256SUMS manifest)
d = new_fixture("ctl-dropcap-b")
link_evidence(d, copy_graders=True)
sp = d / "corpus/evidence/round52/graders/SHA256SUMS"
kept = [ln for ln in sp.read_text(errors="replace").splitlines() if DROP_FILE not in ln]
sp.write_text("\n".join(kept) + "\n")

# ---- proposed probes (NOT frozen controls) for the confirmation leg -------------------
def conf_fixture(name, items, prior=True):
    d = new_fixture(name)
    ev = link_evidence(d)
    (ev / "confirmations.json").write_text(json.dumps(items))
    if prior:
        (ev / "prior-art.md").write_text(PRIOR_ART)
    return d


conf_fixture("conf-quote", [conf(T_NEW1, Q_NEW1), conf(T_FAB, Q_FAB)])
conf_fixture("conf-member", [conf(T_NC, Q_NC)])
conf_fixture("conf-read", [conf(T_READ, Q_READ)])
conf_fixture("conf-unconf", [conf(T_UNCF, Q_UNCF, confirmed=False)])
conf_fixture("conf-thr1", [conf(T_NEW1, Q_NEW1)])
conf_fixture("conf-thr2", [conf(T_NEW1, Q_NEW1), conf(T_NEW2, Q_NEW2)])

# ---- scenarios -------------------------------------------------------------------------
# name -> (lane dir or None, mode, patch)
SCEN = {
    "SELFTEST": (BASE_LANE, "selftest", None),
    "PRISTINE": (BASE_LANE, "verdict", None),
    "F-nothing": (FX / "ctl-nothing", "verdict", None),
    "F-nameonly": (FX / "ctl-nameonly", "verdict", None),
    "F-blind-file": (BASE_LANE, "verdict", "blind_file"),
    "F-blind-full": (BASE_LANE, "verdict", "blind_full"),
    "F-dropcap-a": (FX / "ctl-dropcap-a", "verdict", None),
    "F-dropcap-b": (FX / "ctl-dropcap-b", "verdict", None),
    "P-quote": (FX / "conf-quote", "verdict", None),
    "P-member": (FX / "conf-member", "verdict", None),
    "P-read": (FX / "conf-read", "verdict", None),
    "P-unconf": (FX / "conf-unconf", "verdict", None),
    "P-thr1": (FX / "conf-thr1", "verdict", None),
    "P-thr2": (FX / "conf-thr2", "verdict", None),
}


def run(mname, sname):
    lane, mode, patch = SCEN[sname]
    mod = load(mut_path(mname), f"{mname}_{sname}".replace("-", "_"))
    if patch == "blind_file":
        mod.classify = lambda body: ("V0", {"forced": True, "test_functions": 0})
    if patch == "blind_full":
        mod.classify = lambda body: ("V0", {"forced": True, "test_functions": 0})
        mod.classify_test = lambda block: "P0"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            if mode == "selftest":
                rc = mod.selftest(lane)
            else:
                rc = mod.verdict(lane)
        except Exception as exc:  # a crash is a finding, record it
            print(f"CRASH {type(exc).__name__}: {exc}")
            rc = 99
    out = buf.getvalue() + f"[exit={rc}]\n"
    return out


def main():
    matrix = {}
    for m in MUTANTS:
        for s in SCEN:
            out = run(m, s)
            matrix[f"{m}|{s}"] = out
            (RES / f"{m}__{s}.txt").write_text(out)
    (RES / "matrix.json").write_text(json.dumps(matrix, indent=1))
    print("runs", len(matrix))
    # per-mutant population stats (not frozen predicate output)
    stats = {}
    for m in MUTANTS:
        mod = load(mut_path(m), f"stat_{m}")
        tot = 0
        p1 = 0
        for task, files in pop["tasks"].items():
            pg = mod.primary_grader(files)
            if not pg or not (BASE_LANE / "corpus/evidence/round52/graders" / pg).exists():
                continue
            body = (BASE_LANE / "corpus/evidence/round52/graders" / pg).read_text(errors="replace")
            tests = mod.classify_tests(body)
            tot += len(tests)
            p1 += sum(1 for t in tests if t["class"] == "P1")
        stats[m] = {"test_functions_split": tot, "P1_tests": p1}
    (RES / "stats.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats))
    print("T_NC", T_NC, "| Q_NC", Q_NC)
    print("Q_NEW2", Q_NEW2)
    print("Q_UNCF", Q_UNCF)
    print("Q_READ", Q_READ)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Round-53 frozen controls on the REAL landed tree (C1 and C2), run on scratch clones.

    python3 controls.py --src <lane or clone of the integration commit> --out <receipt dir> --scratch <scratch root> [--which c1|c2|all]

Every control is a scratch shared clone of --src with ONE forged-but-complete (or do-nothing) change, committed inside the
scratch clone only (explicit `git -C <clone>`, top-level verified first), then scored by the frozen counter at --src.  A control
passes iff the counter exits non-zero AND prints the named leg marker.  Receipts: <out>/c1-control-*.txt, c2-control-*.txt.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ID = ["-c", "user.name=r53-control", "-c", "user.email=control@r53.invalid"]


def sh(*a, cwd=None, check=True, **kw):
    return subprocess.run(a, cwd=cwd, check=check, capture_output=True, text=True, **kw)


def clone(src: Path, dst: Path) -> Path:
    sh("git", "clone", "-q", "--shared", str(src), str(dst))
    top = sh("git", "-C", str(dst), "rev-parse", "--show-toplevel").stdout.strip()
    assert Path(top).resolve() == dst.resolve(), (top, dst)
    return dst


def commit(c: Path, msg: str):
    sh("git", "-C", str(c), "add", "-A")
    sh("git", "-C", str(c), *ID, "commit", "-q", "--allow-empty", "-m", msg)


def run_counter(c: Path, script: str, *args, timeout=1800):
    p = subprocess.run(["python3", script, "--lane", str(c), *args], cwd=c, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr


def check(label, rc, out, marker, outdir: Path, extra=""):
    ok = rc != 0 and marker in out
    (outdir / f"{label}.txt").write_text(f"# {label}\n# expect: exit != 0 and marker {marker!r}\n# observed exit={rc}\n{out}\n{extra}")
    print(f"CONTROL {label} exit={rc} marker={'present' if marker in out else 'ABSENT'} -> {'ok' if ok else 'FAIL'}")
    return ok


def c1(src: Path, outdir: Path, scratch: Path) -> int:
    bad = 0
    script = "plans/round53_c1_triage.py"
    L = "corpus/evidence/round53"

    def mk(name):
        d = scratch / f"c1-{name}"
        shutil.rmtree(d, ignore_errors=True)
        return clone(src, d)

    # 0. the unmodified tree (reported, not a control)
    c = mk("baseline")
    rc, out = run_counter(c, script)
    (outdir / "c1-baseline.txt").write_text(f"# unmodified clone of --src, exit={rc}\n{out}")
    print(f"BASELINE c1 exit={rc}")
    # 1. nothing: no labels, no freeze
    c = mk("nothing")
    for rel in (f"{L}/oracle-labels.json", "plans/round53-c1-freeze.json"):
        (c / rel).unlink(missing_ok=True)
    commit(c, "nothing")
    rc, out = run_counter(c, script)
    bad += not check("c1-control-nothing", rc, out, "FREEZE absent", outdir)
    # 2. names-only population (tasks with empty file lists)
    c = mk("names-only")
    p = c / "plans/round52-tasks.json"
    d = json.loads(p.read_text())
    d["capture_population"] = {k: [] for k in d["capture_population"]}
    p.write_text(json.dumps(d))
    commit(c, "names-only")
    rc, out = run_counter(c, script)
    bad += not check("c1-control-names-only", rc, out, "population_sha=BAD", outdir)
    # 3. forged stub capture (bytes replaced, any digest file re-pinned)
    c = mk("forged-stub")
    stub = next(p for p in sorted((c / "corpus/evidence/round52/graders").glob("*/tests/test_outputs.py")))
    stub.write_text("def test_x():\n    assert True\n")
    for sums in (c / "corpus/evidence/round52/graders").glob("SHA256SUMS"):
        pass
    commit(c, "forged-stub")
    rc, out = run_counter(c, script)
    bad += not check("c1-control-forged-stub", rc, out, "blob_bad=1", outdir)
    # 4. do-nothing classifier: every test P0, freeze re-pinned to the new bytes (forged-complete)
    c = mk("all-p0")
    clf = c / "plans/round53_c1_classify.py"
    clf.write_text("def classify_source(src):\n    import ast\n    out = {}\n    for n in ast.walk(ast.parse(src)):\n"
                   "        if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'):\n            out[n.name] = 'P0'\n"
                   "    return out\n")
    fz = c / "plans/round53-c1-freeze.json"
    d = json.loads(fz.read_text())
    import hashlib
    d["classifier_sha256"] = hashlib.sha256(clf.read_bytes()).hexdigest()
    fz.write_text(json.dumps(d))
    commit(c, "all-p0")
    rc, out = run_counter(c, script)
    bad += not check("c1-control-all-p0", rc, out, "PREDICATE R53-C1 fail", outdir)
    # 5. the round-52 classifier substituted for v2 (freeze re-pinned)
    c = mk("r52-classifier")
    clf = c / "plans/round53_c1_classify.py"
    clf.write_text("import importlib.util, sys\nfrom pathlib import Path\n_p = Path(__file__).with_name('round52_c1_grader_audit.py')\n"
                   "_s = importlib.util.spec_from_file_location('r52a', _p)\n_m = importlib.util.module_from_spec(_s)\nsys.modules['r52a'] = _m\n_s.loader.exec_module(_m)\n\n"
                   "def classify_source(src):\n    return {x['test']: ('P1' if x['class'] == 'P1' else 'P0') for x in _m.classify_tests(src)}\n")
    d = json.loads(fz.read_text()) if (fz := c / "plans/round53-c1-freeze.json").exists() else {}
    d["classifier_sha256"] = hashlib.sha256(clf.read_bytes()).hexdigest()
    fz.write_text(json.dumps(d))
    commit(c, "r52-classifier")
    rc, out = run_counter(c, script)
    bad += not check("c1-control-r52-classifier", rc, out, "control_ok=NO", outdir)
    # 6. labels written in the SAME commit as the freeze (order unprovable): rebuild history in the scratch clone
    c = mk("same-commit")
    sh("git", "-C", str(c), *ID, "checkout", "-q", "--orphan", "r53same")
    commit(c, "same-commit: everything in one root commit")
    rc, out = run_counter(c, script)
    bad += not check("c1-control-same-commit", rc, out, "order=UNPROVEN", outdir)
    return bad


def c2(src: Path, outdir: Path, scratch: Path) -> int:
    bad = 0
    script = "plans/round53_c2_tipstate.py"
    led = "plans/round53-tipstate.json"
    d = json.loads((src / led).read_text())
    rows = d["rows"]
    red = next(n for n in sorted(rows) if rows[n]["state"] == "red")
    green = next(n for n in sorted(rows) if rows[n]["state"] == "green" and rows[n]["kind"] != "help")
    only = f"{red},{green}"

    def mk(name):
        dd = scratch / f"c2-{name}"
        shutil.rmtree(dd, ignore_errors=True)
        return clone(src, dd)

    def run(c, *extra):
        w = scratch / f"w-{c.name}"
        shutil.rmtree(w, ignore_errors=True)
        p = subprocess.run(["python3", script, "--lane", str(c), "--source", str(c), "--work", str(w), "--jobs", "2", "--timeout", "900", *extra],
                           cwd=c, capture_output=True, text=True, timeout=3600)
        shutil.rmtree(w, ignore_errors=True)
        return p.returncode, p.stdout + p.stderr

    c = mk("nothing")
    (c / led).unlink()
    commit(c, "nothing")
    rc, out = run(c, "--dry")
    bad += not check("c2-control-nothing", rc, out, "LEDGER ledger absent", outdir)

    def forge(label, marker, mutate):
        nonlocal bad
        c = mk(label)
        dd = json.loads((c / led).read_text())
        mutate(dd["rows"])
        (c / led).write_text(json.dumps(dd, indent=1))
        commit(c, label)
        rc, out = run(c, "--only", only)
        bad += not check(f"c2-control-{label}", rc, out, marker, outdir, f"# rows run: {only}\n")

    def all_green(r):
        for e in r.values():
            e["exit"], e["state"] = 0, "green"
            e.pop("evidence", None)
            e.pop("reason", None)

    def all_red(r):
        for e in r.values():
            e["exit"], e["state"], e["kind"] = 1, "red", "entry"
            e["evidence"] = "forged fragment that no run prints"
            e["reason"] = "a forged declaration that claims every instrument is red without having observed any output"

    def bad_evidence(r):
        r[red]["evidence"] = "text the observed output never contains"

    forge("all-green", f"MISMATCH {red} declared exit=0", all_green)
    forge("all-red", f"MISMATCH {green} declared exit=1", all_red)
    forge("evidence-altered", f"EVIDENCE-MISSING {red}", bad_evidence)
    return bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--which", default="all")
    a = ap.parse_args()
    src, out, scratch = Path(a.src).resolve(), Path(a.out).resolve(), Path(a.scratch).resolve()
    out.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    bad = 0
    if a.which in ("c1", "all"):
        bad += c1(src, out, scratch)
    if a.which in ("c2", "all"):
        bad += c2(src, out, scratch)
    print(f"CONTROLS failed={bad}")
    sys.exit(1 if bad else 0)

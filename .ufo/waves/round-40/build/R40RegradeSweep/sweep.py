#!/usr/bin/env python3
"""R40RegradeSweep: grade-twice stability across the lane's five admitted TB2 graders.

For each earlier probe (protein-assembly, regex-log, configure-git-webserver, build-pmars,
git-leak-recovery) take the oracle case and two failing cases, build the end state ONCE in that
probe's own sandbox, then run the grader twice on the unchanged state (fresh process / fresh
module import each time) and compare the per-test letters.

Reads the lane read-only (--lane), writes only under --work.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import traceback

# ---- selection: per task, the oracle case + two failing cases (cid, expected overall verdict) ----
SELECT = {
    "protein": [("valid-balanced", "pass"), ("stop-codon-appended", "fail"),
                ("donor-one-substitution", "fail")],
    "regex": [("reference-month-aware", "pass"), ("first-date-only", "fail"),
              ("extra-capture-group", "fail")],
    "cgw": [("static-file-no-git", "pass"), ("no-server", "fail"), ("capitalised", "fail")],
    "bpm": [("canned-shape", "pass"), ("canned-script", "fail"), ("nonexec-binary", "fail")],
    "glr": [("oracle-solve-sh", "pass"), ("untouched", "fail"), ("dangling-secret-blob", "fail")],
}

GRADE_HARNESS_GLR = r'''
import importlib.util, sys
spec = importlib.util.spec_from_file_location("tb2_git_leak_grader", "/cap/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in %r:
    try:
        getattr(mod, name)()
        print("TEST " + name + " P")
    except AssertionError:
        print("TEST " + name + " F")
    except Exception as e:
        print("TEST " + name + " F error=" + type(e).__name__)
'''


def load_probe(probe_dir, name):
    path = probe_dir / (name + ".py")
    spec = importlib.util.spec_from_file_location("probe_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # dataclasses under `from __future__ import annotations` needs it
    spec.loader.exec_module(mod)
    return mod


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def manifest(root):
    out = {}
    root = pathlib.Path(root)
    for p in sorted(root.rglob("*")):
        rel = str(p.relative_to(root))
        st = p.lstat()
        entry = {"kind": "dir" if p.is_dir() else "link" if p.is_symlink() else "file",
                 "mode": oct(st.st_mode & 0o7777), "mtime": st.st_mtime_ns}
        if p.is_symlink():
            entry["target"] = os.readlink(p)
        elif p.is_file():
            entry["size"] = st.st_size
            entry["sha256"] = sha256(p)
        out[rel] = entry
    return out


def content_key(e):
    return (e["kind"], e["mode"], e.get("size"), e.get("sha256"), e.get("target"))


def state_delta(before, after):
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(k for k in set(before) & set(after)
                     if content_key(before[k]) != content_key(after[k]))
    touched = sorted(k for k in set(before) & set(after)
                     if content_key(before[k]) == content_key(after[k])
                     and before[k]["mtime"] != after[k]["mtime"])
    return added, removed, changed, touched


def delta_str(d):
    added, removed, changed, touched = d
    if not (added or removed or changed):
        return "unchanged" if not touched else "TOUCH:" + ",".join(touched[:6])
    parts = []
    if changed:
        parts.append("changed=" + ",".join(changed[:6]))
    if added:
        parts.append("added=" + ",".join(added[:6]))
    if removed:
        parts.append("removed=" + ",".join(removed[:6]))
    return "MUT:" + ";".join(parts)


# ---------------------------------------------------------------- in-process graders
def grade_static(grader, state_path, test_name, label, tmpdir):
    spec = importlib.util.spec_from_file_location(label, grader)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    real = pathlib.Path
    mod.Path = lambda _arg: real(state_path)  # the grader hard-codes /app/<file>
    try:
        getattr(mod, test_name)()
        return 0, "pass", "-"
    except AssertionError as e:
        first = (str(e).splitlines() or ["AssertionError"])[0]
        return 0, "fail", first
    except Exception as e:  # noqa: BLE001
        return 1, "error", type(e).__name__


def run_static(task, probe, cap, work, grader_rel, test_name, label, builder):
    rows = []
    for cid, expected in SELECT[task]:
        state = work / (task + "-" + cid)
        state.mkdir(parents=True)
        content = builder(probe, cap, cid)
        p = state / ("gblock.txt" if task == "protein" else "regex.txt")
        p.write_text(content)
        grades = []
        deltas = []
        m = manifest(state)
        for _ in range(2):
            rc, obs, msg = grade_static(cap / grader_rel, p, test_name, label, state)
            m2 = manifest(state)
            deltas.append(state_delta(m, m2))
            m = m2
            grades.append((rc, obs, msg))
        rows.append(dict(task=task, cid=cid, expected=expected, grades=grades, deltas=deltas))
    return rows





# ---------------------------------------------------------------- sandbox helpers
def run_bwrap(argv, env, timeout=300):
    r = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def parse_letters(out, tests):
    got = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0] == "TEST" and parts[1] in tests:
            got[parts[1]] = parts[2] + (":" + parts[3] if len(parts) > 3 else "")
    return "".join(got[t][0] if t in got else "?" for t in tests), got


def run_bpm(probe, cap, work):
    rows = []
    for cid, expected in SELECT["bpm"]:
        case = next(c for c in probe.CASES if c.cid == cid)
        w = work / ("bpm-" + cid)
        (w / "ulb").mkdir(parents=True)
        (w / "ulsb").mkdir()
        (w / "build").mkdir()
        probe.build_art(case.art, w / "ulb" / "pmars", w / "build")
        probe.build_art(case.sbin, w / "ulsb" / "pmars", w / "build")
        probe.stage_app(case.app, w / "app")
        (w / "harness.py").write_text(probe.HARNESS_PY)
        env = {"PATH": probe.PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        argv = probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py"]
        grades, deltas = [], []
        m = manifest(w)
        for _ in range(2):
            rc, out, err = run_bwrap(argv, env)
            m2 = manifest(w)
            deltas.append(state_delta(m, m2))
            m = m2
            letters, got = parse_letters(out, probe.TESTS)
            grades.append((rc, letters, got, out, err))
        rows.append(dict(task="bpm", cid=cid, expected=expected, grades=grades, deltas=deltas))
    return rows


def run_cgw(probe, cap, work):
    rows = []
    for cid, expected in SELECT["cgw"]:
        case = next(c for c in probe.CASES if c.cid == cid)
        w = work / ("cgw-" + cid)
        probe.prepare(w, case.tools, case.server, probe.HARNESS_PY)
        env = {"PATH": "/work/bin", "HOME": "/work/home", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        argv = probe.sandbox_argv(cap, w) + ["/usr/bin/bash", "/work/run.sh"]
        grades, deltas = [], []
        m = manifest(w)
        for _ in range(2):
            ready = w / "ready"
            if ready.exists():
                ready.unlink()  # runtime handshake written by the server, not graded state
            rc, out, err = run_bwrap(argv, env)
            m2 = manifest(w)
            deltas.append(state_delta(m, m2))
            m = m2
            verdict = [l for l in out.splitlines() if l.startswith("VERDICT ")]
            obs = verdict[0].split()[1] if len(verdict) == 1 else "ERR"
            extra = verdict[0].split()[2] if verdict and len(verdict[0].split()) > 2 else ""
            grades.append((rc, obs, extra, out, err))
        rows.append(dict(task="cgw", cid=cid, expected=expected, grades=grades, deltas=deltas))
    return rows


def run_glr(probe, cap, work):
    rows = []
    for cid, expected in SELECT["glr"]:
        case = next(c for c in probe.CASES if c.cid == cid)
        w = work / ("glr-" + cid)
        (w / "app").mkdir(parents=True)
        (w / "recipe.sh").write_text(case.recipe)
        (w / "harness.py").write_text(probe.HARNESS_PY)
        env = {"PATH": probe.PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
               "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
        # stage once
        rc, out, err = run_bwrap(probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py",
                                                              "stage", "1" if case.setup else "0"], env)
        if rc != 0:
            rows.append(dict(task="glr", cid=cid, expected=expected, stage=(rc, out, err),
                             grades=[], deltas=[]))
            continue
        # grade twice: same /app, fresh process, no setup/recipe re-run
        (w / "harness.py").write_text(GRADE_HARNESS_GLR % (probe.TESTS,))
        argv = probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py"]
        grades, deltas = [], []
        m = manifest(w / "app")
        for _ in range(2):
            rc, out, err = run_bwrap(argv, env)
            m2 = manifest(w / "app")
            deltas.append(state_delta(m, m2))
            m = m2
            letters, got = parse_letters(out, probe.TESTS)
            grades.append((rc, letters, got, out, err))
        rows.append(dict(task="glr", cid=cid, expected=expected, stage=(0, out, err),
                         grades=grades, deltas=deltas))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--probes", required=True, help="dir holding copies of the five probe modules")
    ap.add_argument("--only", default=None, help="comma list of tasks: protein,regex,cgw,bpm,glr")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    probe_dir = pathlib.Path(a.probes).resolve()
    tasks = a.only.split(",") if a.only else ["protein", "regex", "cgw", "bpm", "glr"]
    work.mkdir(parents=True, exist_ok=True)
    rows = []

    probes = {}
    for t, mod in (("protein", "tb2_grader_probe"), ("regex", "regex_log_probe"),
                   ("cgw", "git_webserver_probe"), ("bpm", "build_pmars_probe"),
                   ("glr", "git_leak_probe")):
        if t in tasks:
            probes[t] = load_probe(probe_dir, mod)

    if "protein" in tasks:
        p = probes["protein"]
        cap = lane / "corpus/evidence/round35/tb2-eval"

        def build(probe, cap, cid, _p=p):
            src = (cap / "test_outputs.py").read_bytes()
            parts = _p.components(src.decode())
            cases = dict((c[0], c[1]) for c in _p.build_cases(parts))
            return cases[cid]
        rows += run_static("protein", p, cap, work, pathlib.Path("test_outputs.py"),
                           "test_gblock", "tb2_protein_assembly_grader", build)

    if "regex" in tasks:
        p = probes["regex"]
        cap = lane / "corpus/evidence/round36/tb2-regex-log"

        def build_r(probe, cap, cid, _p=p):
            cases = dict((c[0], c[1]) for c in _p.build_cases())
            return cases[cid]
        rows += run_static("regex", p, cap, work, pathlib.Path("test_outputs.py"),
                           "test_regex_matches_dates", "tb2_regex_log_grader", build_r)

    if "cgw" in tasks:
        rows += run_cgw(probes["cgw"], lane / "corpus/evidence/round37/tb2-git-webserver", work / "x")
    if "bpm" in tasks:
        rows += run_bpm(probes["bpm"], lane / "corpus/evidence/round38/tb2-build-pmars", work / "x")
    if "glr" in tasks:
        rows += run_glr(probes["glr"], lane / "corpus/evidence/round39/tb2-git-leak-recovery", work / "x")

    # ---- report ----
    diffs = 0
    print(f"# sweep lane={lane}")
    for r in rows:
        task, cid, expected = r["task"], r["cid"], r["expected"]
        if len(r["grades"]) != 2:
            print(f"CASE {task}/{cid} expected={expected} STAGE-FAILED")
            continue
        g1, g2 = r["grades"]
        if task in ("protein", "regex"):
            sig1 = (g1[1], g1[2])
            sig2 = (g2[1], g2[2])
            obs1, obs2 = g1[1], g2[1]
            detail1 = f"{g1[1]}:{g1[2][:60]!r}"
            detail2 = f"{g2[1]}:{g2[2][:60]!r}"
        elif task == "cgw":
            sig1 = (g1[1], g1[2])
            sig2 = (g2[1], g2[2])
            obs1, obs2 = g1[1], g2[1]
            detail1 = obs1 + ((" " + g1[2]) if g1[2] else "")
            detail2 = obs2 + ((" " + g2[2]) if g2[2] else "")
        else:
            sig1 = g1[1]
            sig2 = g2[1]
            obs1, obs2 = ("pass" if set(g1[1]) == {"P"} else "fail"), ("pass" if set(g2[1]) == {"P"} else "fail")
            detail1, detail2 = g1[1], g2[1]
        same = sig1 == sig2
        r["same"] = same
        diffs += not same
        d1, d2 = r["deltas"]
        print(f"CASE {task}/{cid} expected={expected} grade1={detail1} grade2={detail2}"
              f" regrade={'same' if same else 'DIFF'}"
              f" rc1={g1[0]} rc2={g2[0]} state_after_1={delta_str(d1)} state_after_2={delta_str(d2)}")
        for i, g in enumerate((g1, g2), 1):
            if g[0] != 0 and task in ("bpm", "glr", "cgw"):
                print(f"  grade{i}-rc={g[0]} stderr_tail={(g[4] or '')[-300:]!r}")
    by_task = {}
    for r in rows:
        by_task.setdefault(r["task"], []).append(r)
    print()
    for t in ["protein", "regex", "cgw", "bpm", "glr"]:
        if t not in by_task:
            continue
        rs = by_task[t]
        d = sum(1 for r in rs if not r.get("same", True))
        mut = any(dd[0] or dd[1] or dd[2] for r in rs for dd in r["deltas"])
        touch = any(dd[3] for r in rs for dd in r["deltas"])
        print(f"TASK {t} cases={len(rs)} regrade_diff={d} mutating={'yes' if mut else 'no'}"
              f" touched_only={'yes' if touch and not mut else 'no'}")
    print(f"TOTAL cases={len(rows)} regrade_diff={diffs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

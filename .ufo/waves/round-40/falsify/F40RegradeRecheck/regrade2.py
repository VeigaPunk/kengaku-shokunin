#!/usr/bin/env python3
"""F40RegradeRecheck: independent re-run of R40RegradeSweep's table on cgw and glr.

For each selected case: build the end state ONCE with the lane probe's own builders, then invoke
the pinned grader TWICE in two fresh processes, no rebuild and no state reset between gradings
(the one disclosed exception, cgw's probe-harness `ready` handshake, is reported separately in the
--no-clear-ready variant). Files the grader wrote are reported by GNU `find <root> -newer <marker>`.

Writes only under --work. Reads the lane clone read-only.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import time

S = pathlib.Path(__file__).resolve().parent
LANE = S / "lane"
PROBES = S / "probes"
WORK = S / "work"
MARKS = S / "marks"

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

# the grader's own checksum command (test_outputs.py:101) and the same command without the dot-path skip
CHK_HARNESS = r'''
import subprocess
BS = chr(92)
SKIP = "*/" + BS + ".*"
def sh(cmd):
    return subprocess.run(["sh", "-c", cmd], capture_output=True, text=True)
def chk(cmd):
    r = sh(cmd)
    return (r.stdout.split()[0] if r.returncode == 0 and r.stdout.strip() else "ERR")
print("CHK skip=" + chk("find /app/repo -type f -not -path '%s' -exec sha256sum {} + | sort | sha256sum" % SKIP))
print("CHK full=" + chk("find /app/repo -type f -exec sha256sum {} + | sort | sha256sum"))
print("CHK skipfiles=" + str(len(sh("find /app/repo -type f -not -path '%s'" % SKIP).stdout.splitlines())))
print("CHK allfiles=" + str(len(sh("find /app/repo -type f").stdout.splitlines())))
'''


def load_probe(name):
    spec = importlib.util.spec_from_file_location("probe_" + name, PROBES / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
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
        e = {"kind": "dir" if p.is_dir() else "link" if p.is_symlink() else "file",
             "mode": oct(st.st_mode & 0o7777), "mtime": st.st_mtime_ns}
        if p.is_symlink():
            e["target"] = os.readlink(p)
        elif p.is_file():
            e["size"] = st.st_size
            e["sha256"] = sha256(p)
        out[rel] = e
    return out


def ckey(e):
    return (e["kind"], e["mode"], e.get("size"), e.get("sha256"), e.get("target"))


def delta(before, after):
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(k for k in set(before) & set(after) if ckey(before[k]) != ckey(after[k]))
    touched = sorted(k for k in set(before) & set(after)
                     if ckey(before[k]) == ckey(after[k]) and before[k]["mtime"] != after[k]["mtime"])
    return added, removed, changed, touched


def dstr(d):
    added, removed, changed, touched = d
    if not (added or removed or changed):
        return "unchanged" if not touched else "TOUCH:" + ",".join(touched)
    parts = []
    for label, xs in (("added", added), ("removed", removed), ("changed", changed)):
        if xs:
            parts.append(label + "=" + ",".join(xs))
    return "MUT:" + ";".join(parts)


def bump(marker):
    time.sleep(0.05)
    marker.write_text("mark\n")
    os.utime(marker, None)


def find_newer(root, marker):
    r = subprocess.run(["find", str(root), "-newer", str(marker)], capture_output=True, text=True)
    root = pathlib.Path(root)
    out = []
    for line in r.stdout.splitlines():
        p = pathlib.Path(line)
        out.append(str(p.relative_to(root)) if str(p).startswith(str(root)) else line)
    return sorted(out)


def run(argv, env, timeout):
    return subprocess.run(argv, env=env, capture_output=True, text=True, timeout=timeout)


# ------------------------------------------------------------------ configure-git-webserver
def cgw(probe, cap, cid, clear_ready=True, force_curl=None):
    case = next(c for c in probe.CASES if c.cid == cid)
    w = WORK / ("cgw-" + cid + ("" if clear_ready else "-noclear"))
    if w.exists():
        import shutil
        shutil.rmtree(w)
    tag = cid + ("" if clear_ready else "-noclear")
    marker = MARKS / ("cgw-" + tag)
    tools = force_curl if force_curl else case.tools
    probe.prepare(w, tools, case.server, probe.HARNESS_PY)
    env = {"PATH": "/work/bin", "HOME": "/work/home", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    argv = probe.sandbox_argv(cap, w) + ["/usr/bin/bash", "/work/run.sh"]
    m = manifest(w)
    print(f"BUILD cgw/{tag} tools={tools} server={'yes' if case.server else 'no'} predicted={case.predicted}"
          f" files={len(m)}")
    grades = []
    for i in (1, 2):
        cleared = "no"
        if clear_ready and (w / "ready").exists():
            (w / "ready").unlink()
            cleared = "yes"
        bump(marker)
        r = run(argv, env, 180)
        newer = find_newer(w, marker)
        m2 = manifest(w)
        d = delta(m, m2)
        m = m2
        verdict = [l for l in r.stdout.splitlines() if l.startswith("VERDICT ")]
        obs = verdict[0].split()[1] if len(verdict) == 1 else "ERR"
        extra = verdict[0].split()[2] if verdict and len(verdict[0].split()) > 2 else ""
        out_lines = [l for l in r.stdout.splitlines() if l.startswith("STDOUT ")]
        print(f"GRADE cgw/{tag} n={i} rc={r.returncode} verdict={obs}{(' ' + extra) if extra else ''}"
              f" harness_cleared_ready={cleared} state_after={dstr(d)}")
        print(f"  find-newer cgw/{tag} n={i} ({len(newer)}): {json.dumps(newer)}")
        for l in out_lines:
            print("  " + l)
        if r.returncode != 0:
            print("  stderr_tail=" + repr((r.stderr or "")[-300:]))
        grades.append((obs, extra))
    same = grades[0] == grades[1]
    print(f"CASE cgw/{tag} grade1={grades[0][0]} grade2={grades[1][0]} regrade={'same' if same else 'DIFF'}")
    return same


# ------------------------------------------------------------------ git-leak-recovery
def glr(probe, cap, cid):
    case = next(c for c in probe.CASES if c.cid == cid)
    w = WORK / ("glr-" + cid)
    if w.exists():
        import shutil
        shutil.rmtree(w)
    (w / "app").mkdir(parents=True)
    (w / "recipe.sh").write_text(case.recipe)
    (w / "harness.py").write_text(probe.HARNESS_PY)
    marker = MARKS / ("glr-" + cid)
    env = {"PATH": probe.PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
    stage = run(probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py", "stage",
                                             "1" if case.setup else "0"], env, 300)
    stages = [l for l in stage.stdout.splitlines() if l.startswith("STAGE ")]
    print(f"BUILD glr/{cid} predicted={case.predicted} stage_rc={stage.returncode} {' '.join(stages)}")
    if stage.returncode != 0:
        print("  stage stderr=" + repr((stage.stderr or "")[-400:]))
        return None
    # what the staged state already holds inside the graded repository
    lf = subprocess.run(["find", str(w / "app/repo/.git/lost-found"), "-type", "f"],
                        capture_output=True, text=True)
    pre_lf = sorted(str(pathlib.Path(x).relative_to(w / "app")) for x in lf.stdout.splitlines())
    print(f"PRESTAGE glr/{cid} lost-found files={json.dumps(pre_lf)}")

    root = w / "app"
    # the grader's checksum command, and the same command without the dot-path skip
    def chk():
        (w / "harness.py").write_text(CHK_HARNESS)
        r = run(probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py"], env, 300)
        return [l for l in r.stdout.splitlines() if l.startswith("CHK ")]

    m = manifest(root)
    print(f"BUILD glr/{cid} files_in_app={len(m)}")
    for l in chk():
        print(f"CHECKSUM glr/{cid} before_grade1 {l}")
    (w / "harness.py").write_text(GRADE_HARNESS_GLR % (probe.TESTS,))
    argv = probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py"]
    grades = []
    for i in (1, 2):
        (w / "harness.py").write_text(GRADE_HARNESS_GLR % (probe.TESTS,))  # chk() overwrites the bind target
        bump(marker)
        r = run(argv, env, 300)
        newer = find_newer(root, marker)
        m2 = manifest(root)
        d = delta(m, m2)
        m = m2
        got = {}
        for line in r.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 3 and parts[0] == "TEST" and parts[1] in probe.TESTS:
                got[parts[1]] = (parts[2], parts[3] if len(parts) > 3 else "")
        letters = "".join(got.get(t, ("?",))[0] for t in probe.TESTS)
        errs = ",".join(f"{t}:{got[t][1]}" for t in probe.TESTS if t in got and got[t][1])
        print(f"GRADE glr/{cid} n={i} rc={r.returncode} tests={letters} state_after={dstr(d)}"
              f"{(' ' + errs) if errs else ''}")
        print(f"  find-newer glr/{cid} n={i} ({len(newer)}): {json.dumps(newer)}")
        for l in chk():
            print(f"CHECKSUM glr/{cid} after_grade{i} {l}")
        if r.returncode != 0:
            print("  stderr_tail=" + repr((r.stderr or "")[-300:]))
        grades.append(letters)
    same = grades[0] == grades[1]
    print(f"CASE glr/{cid} grade1={grades[0]} grade2={grades[1]} regrade={'same' if same else 'DIFF'}"
          f" predicted={case.predicted} match={'yes' if grades == [case.predicted] * 2 else 'NO'}")
    return same


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    MARKS.mkdir(parents=True, exist_ok=True)
    cgw_probe = load_probe("git_webserver_probe")
    glr_probe = load_probe("git_leak_probe")
    cap_cgw = LANE / cgw_probe.CAP
    cap_glr = LANE / glr_probe.CAP
    for name, digest in cgw_probe.PINS.items():
        got = sha256(cap_cgw / name)
        print(f"PIN cgw {name} pinned={digest[:12]} got={got[:12]} ok={'yes' if got == digest else 'NO'}")
    for name, digest in glr_probe.PINS.items():
        got = sha256(cap_glr / name)
        print(f"PIN glr {name} pinned={digest[:12]} got={got[:12]} ok={'yes' if got == digest else 'NO'}")

    print()
    print("=== selected cgw cases: sweep protocol (clear probe `ready` between gradings) ===")
    for cid in ("static-file-no-git", "no-server", "capitalised"):
        cgw(cgw_probe, cap_cgw, cid)
    print()
    print("=== cgw: un-exercised wget branch of verify.sh (no curl on PATH) ===")
    cgw(cgw_probe, cap_cgw, "wget-static-file")
    print()
    print("=== cgw: same case with the probe handshake NOT cleared between gradings ===")
    cgw(cgw_probe, cap_cgw, "static-file-no-git", clear_ready=False)
    print()
    print("=== selected glr cases ===")
    for cid in ("oracle-solve-sh", "untouched", "dangling-secret-blob"):
        glr(glr_probe, cap_glr, cid)
    print()
    print("DONE")


if __name__ == "__main__":
    sys.exit(main())

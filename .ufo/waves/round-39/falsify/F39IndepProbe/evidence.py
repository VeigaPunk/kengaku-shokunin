#!/usr/bin/env python3
"""F39IndepProbe evidence pass: for each of the six extra states, run the same setup+recipe through the
frozen probe's sandbox and print the mechanism behind each test's letter (which query fired, what fsck
listed, whether the secret is still in the object store or on disk). The grader is NOT imported here; the
letters come from the sibling run (`run-final.txt`), this file explains them.

Usage: evidence.py <lane-at-tip> <work-parent>
"""
from __future__ import annotations

import importlib.util
import pathlib
import shutil
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
WORK = pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
src = pathlib.Path(__file__).resolve().parent / "probe_extra.py"

spec = importlib.util.spec_from_file_location("probe_extra", src)
pe = importlib.util.module_from_spec(spec)
sys.modules["probe_extra"] = pe
spec.loader.exec_module(pe)
m = pe.m
CASES = pe.CASES

m.HARNESS_PY = r'''
import importlib.util, subprocess, sys
setup = sys.argv[2] == "1"
REPO = "/app/repo"


def stage(argv):
    return subprocess.run(argv, cwd="/app", stdin=subprocess.DEVNULL,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def g(argv):
    try:
        return subprocess.run(["git", "-C", REPO] + argv, cwd="/app", stdin=subprocess.DEVNULL,
                              capture_output=True)
    except OSError:
        return None


def ev(k, v):
    print("EV " + k + "=" + str(v))


if setup and stage(["bash", "/cap/challenge-setup.sh"]):
    sys.exit(3)
if stage(["bash", "-euo", "pipefail", "/recipe.sh"]):
    sys.exit(3)


def lines(argv):
    r = g(argv)
    if r is None or r.returncode != 0:
        return -1
    return len([l for l in r.stdout.decode(errors="replace").splitlines() if l.strip()])


ev("grep_lines", lines(["log", "--all", "--grep", "secret\\[", "--regexp-ignore-case"]))
ev("pickaxe_lines", lines(["log", "--all", "-p", "-S", "secret["]))
ev("oneline_lines", lines(["log", "--oneline", "--all"]))
r = g(["for-each-ref", "--format=%(refname)"])
ev("refs", ",".join(sorted(r.stdout.decode(errors="replace").split()))
   if r is not None and r.returncode == 0 and r.stdout.strip() else "-")
r = g(["fsck", "--lost-found"])
if r is not None and r.returncode == 0:
    dl = [l for l in r.stdout.decode(errors="replace").splitlines() if "dangling" in l]
    ev("fsck_dangling", len(dl))
    ev("fsck_objtypes", ",".join(sorted({l.split()[1] for l in dl})) if dl else "-")
else:
    ev("fsck_dangling", "-")
    ev("fsck_objtypes", "-")
ev("reflog_lines", lines(["log", "--reflog", "-p", "-S", "secret["]))
r = g(["cat-file", "--batch-all-objects", "--batch"])
_hits = 0
if r is not None and r.returncode == 0:
    b = r.stdout
    i = 0
    while i < len(b):
        nl = b.find(b"\n", i)
        if nl < 0:
            break
        h = b[i:nl].split()
        if len(h) != 3 or h[1] not in (b"blob", b"commit", b"tree"):
            break
        size = int(h[2])
        if b"secret[" in b[nl + 1:nl + 1 + size]:
            _hits += 1
        i = nl + 1 + size + 1
ev("objects_secret", _hits)
_names = []
r = g(["cat-file", "--batch-all-objects", "--batch-check=%(objectname) %(objecttype)"])
if r is not None and r.returncode == 0:
    for l in r.stdout.decode(errors="replace").splitlines():
        f = l.split()
        if len(f) == 2 and f[1] == "tree":
            t = g(["cat-file", "-p", f[0]])
            if t is not None and t.returncode == 0:
                for e in t.stdout.decode(errors="replace").splitlines():
                    sp = e.split("\t", 1)
                    if len(sp) == 2 and "secret[" in sp[1]:
                        _names.append(sp[1])
ev("tree_names", ",".join(sorted(_names)) if _names else "-")
import os
paths = []
for root, dirs, files in os.walk("/app"):
    for f in files:
        fp = os.path.join(root, f)
        if fp == "/app/secret.txt":
            continue
        try:
            with open(fp, "rb") as fh:
                if b"secret[" in fh.read():
                    paths.append(fp)
        except OSError:
            pass
ev("work", ",".join(sorted(paths)) if paths else "-")
try:
    ev("flag", open("/app/secret.txt").read().strip())
except OSError as e:
    ev("flag", "MISSING/" + type(e).__name__)
'''


def main():
    cap = LANE / m.CAP
    for name, digest in m.PINS.items():
        if m.sha256(cap / name) != digest:
            print(f"SETUP capture {name} not pinned", file=sys.stderr)
            return 2
    root = pathlib.Path(tempfile.mkdtemp(prefix="k39ev-", dir=WORK))
    try:
        for c in CASES:
            rc, out = m.run_case(cap, root, c, "evidence")
            ev = {}
            for l in out.splitlines():
                if l.startswith("EV ") and "=" in l:
                    k, v = l[3:].split("=", 1)
                    ev[k] = v
            if rc != 0 or "flag" not in ev:
                print(f"SETUP case {c.cid} rc={rc}", file=sys.stderr)
                return 2
            print(f"CASE {c.cid} predicted_tests={c.predicted}"
                  f" flag={ev['flag']} grep_lines={ev['grep_lines']} pickaxe_lines={ev['pickaxe_lines']}"
                  f" oneline_lines={ev['oneline_lines']} refs={ev['refs']}"
                  f" fsck_dangling={ev['fsck_dangling']} fsck_objtypes={ev['fsck_objtypes']}"
                  f" reflog_lines={ev['reflog_lines']} objects_secret={ev['objects_secret']}"
                  f" tree_names={ev['tree_names']} work={ev['work']}")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

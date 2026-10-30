#!/usr/bin/env python3
"""C2CritPredicate2 attack harness: build fixture trees (stubbed scripts, real pinned row
names) under the seat scratch dir and run the real counter against them.

Every fixture repo is created with `git -C "$D" init -q` under a mktemp dir inside the seat
scratch; every later git call names `-C "$D"`.  The lane tree is only ever READ.
"""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys, tarfile, tempfile
from pathlib import Path

SEAT = Path("/fast/scratch/hyaku/kengaku-r53/C2CritPredicate2")
LANE = SEAT / "lane"
SCRIPT = re.compile(r"python3\s+((?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py|grader\.py)")
COUNTER = "plans/round53_c2_tipstate.py"

results = []


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, **kw)


def git(d, *a):
    return subprocess.run(["git", "-C", str(d), *a], capture_output=True, text=True)


def lane_tree():
    """Committed lane tree (read-only export)."""
    out = subprocess.run(["git", "-C", str(LANE), "archive", "HEAD"], capture_output=True)
    return out.stdout


def make_fixture(label, mutate, stub=True, extra=None):
    """Create a fixture repo D (git init) holding the lane tree, apply `mutate(D)`, commit."""
    D = Path(tempfile.mkdtemp(prefix=f"fx-{label}-", dir=str(SEAT / "fix")))
    tar = tarfile.open(fileobj=__import__("io").BytesIO(lane_tree()))
    tar.extractall(D)
    git(D, "init", "-q")
    git(D, "config", "user.email", "fixture@invalid")
    git(D, "config", "user.name", "fixture")
    if stub:
        stub_all(D)
    if mutate:
        mutate(D)
    git(D, "add", "-A")
    git(D, "commit", "-q", "--allow-empty", "-m", f"fixture {label}")
    return D


def registry(D):
    t = (D / "SKILL.md").read_text()
    m = list(re.finditer(r"(?m)^## Gate/probe registry(?: \([^\n]*\))?[ \t]*$", t))
    i = m[0].start(); j = t.find("\n## ", m[0].end())
    rows = {}
    for l in t[i:j].splitlines():
        mm = re.match(r"^\|\s*`([^`]+)`\s*\|", l)
        if mm:
            rows[mm.group(1)] = l
    return t, rows


def row_scripts(D):
    """name -> script path named in the row's entry cell."""
    _, rows = registry(D)
    out = {}
    for n, l in rows.items():
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", l.strip().strip("|"))]
        mm = SCRIPT.search(cells[2])
        out[n] = mm.group(1) if mm else None
    return out


NEVER_STUB = {"plans/round53_c2_tipstate.py"}   # the counter under test must stay real


def stub_all(D):
    """Replace every registry row's script with a trivial exit-0 stub (keeps the pin)."""
    for n, s in row_scripts(D).items():
        if not s or s in NEVER_STUB:
            continue
        p = D / s
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("import sys\nprint('stub ok')\nsys.exit(0)\n")


def load_ledger(D):
    return json.loads((D / "plans/round53-tipstate.json").read_text())


def save_ledger(D, led):
    (D / "plans/round53-tipstate.json").write_text(json.dumps(led, indent=1) + "\n")


def green_ledger(D):
    """Every row green/exit 0, kinds kept consistent with argv."""
    led = load_ledger(D)
    for n, e in led["rows"].items():
        e["exit"] = 0; e["state"] = "green"
        e.pop("evidence", None); e.pop("reason", None)
    save_ledger(D, led)


def clone_source(D, tag):
    """Clean shared clone of the fixture = the 'source' the counter measures."""
    S = Path(tempfile.mkdtemp(prefix=f"src-{tag}-", dir=str(SEAT / "fix"))) / "src"
    subprocess.run(["git", "clone", "-q", "--shared", str(D), str(S)], check=True)
    return S


def run_counter(D, S, tag, jobs=4, timeout=600, extra_args=(), counter=None):
    w = SEAT / "work" / tag
    if w.exists():
        shutil.rmtree(w, ignore_errors=True)
    cmd = ["python3", str(counter or (D / COUNTER)), "--lane", str(D), "--source", str(S),
           "--work", str(w), "--jobs", str(jobs), "--timeout", str(timeout), *extra_args]
    env = dict(os.environ)
    env["TMPDIR"] = str(SEAT / "tmp")
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(D))
    out = p.stdout + p.stderr
    (SEAT / "out" / f"{tag}.txt").write_text(f"$ {' '.join(cmd)}\nrc={p.returncode}\n{out}")
    return p.returncode, out


def report(label, expect, rc, out, notes=""):
    line = next((l.strip() for l in out.splitlines()
                 if l.strip().startswith(expect) or expect in l), None)
    verdict = "CAUGHT" if rc != 0 else "LANDED(pass)"
    results.append(dict(label=label, expected=expect, rc=rc, verdict=verdict, seen=line, notes=notes))
    print(f"[{verdict}] {label}: rc={rc} expect~ {expect!r} seen={line!r} {notes}")
    return line

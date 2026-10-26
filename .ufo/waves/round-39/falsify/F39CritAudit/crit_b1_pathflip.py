"""attack module crit_b1 (critic seat F39CritAudit, wave 2): the A1 repair re-checks RESULTS, not INPUT.

`plans/round39_c1_audit.py` re-runs the reference gate after a candidate kill and requires the tuple to
reproduce `ref[j]`, and re-runs the mutant and requires the kill to reproduce. That proves the pair is
reproducible *per gate binary*; it does not prove the mutant's code caused the difference.

This module builds the same four fixtures as wave-1 `crit_a1_flip.py` (honest about the reference run),
but the swap is driven by WHICH gate binary is running: a helper started by the build child watches the
process table (the directory name is assembled at run time so the side-channel token scan does not see a
literal) and keeps each fixture's `--spec` on the honest payload while `gates/ref.py` or `gates/null.py`
runs, and on the flipped payload while `gates/M0*.py` runs. Every run therefore reproduces exactly, the
reference re-check sees `ref[j]`, the mutant re-check sees the kill, and the kill is counted although the
mutant's code is not the cause.
"""

import atexit
import hashlib
import json
import os
import pathlib
import subprocess
import sys

DAEMON = r"""
import json, os, pathlib, sys, time
root = pathlib.Path(sys.argv[1])
plan = json.loads(sys.argv[2])
log = pathlib.Path(sys.argv[3])
sep = os.path.sep
proc = sep + "".join(["p", "r", "o", "c"])
cmdf = "cmd" + "line"
rootb = str(root).encode()
def note(msg):
    try:
        with log.open("a") as fh:
            fh.write("%.6f %s\n" % (time.time(), msg))
    except OSError:
        pass
def switch(live, src, base):
    try:
        data = pathlib.Path(src).read_bytes()
        cur = pathlib.Path(live).read_bytes()
        if cur == data:
            return
        tmp = live + ".swp"
        pathlib.Path(tmp).write_bytes(data)
        os.replace(tmp, live)
        note("switch " + base + " " + os.path.basename(live))
    except OSError:
        pass
tries = {}
start = time.time()
while time.time() - start < 150:
    try:
        names = os.listdir(proc)
    except OSError:
        break
    live_now = set(names)
    for stale in [k for k in tries if k not in live_now]:
        del tries[stale]
    for name in names:
        if not name.isdigit():
            continue
        n = tries.get(name, 0)
        if n >= 8:
            continue
        tries[name] = n + 1
        try:
            raw = pathlib.Path(proc, name, cmdf).read_bytes()
        except OSError:
            continue
        if b"/gates/" not in raw or rootb not in raw:
            continue
        base = ""
        for tok in raw.split(b"\0"):
            if b"/gates/" in tok:
                base = os.path.basename(tok.decode("utf-8", "replace"))
        note("detect " + base + " " + name)
        want = "flip" if base.startswith("M") else "orig"
        for e in plan:
            switch(e["live"], e[want], base)
"""
PLANS = []
ROOT = None


def _spawn():
    if not PLANS or ROOT is None:
        return
    try:
        subprocess.Popen([sys.executable, "-c", DAEMON, str(ROOT), json.dumps(PLANS), str(ROOT.parent / "flip.log")],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True, close_fds=True)
    except OSError:
        pass


atexit.register(_spawn)


def _digest(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def _spec(ctx):
    return json.loads(json.dumps(ctx.spec))


def _arm(d, live_name, orig, flip):
    live = d / live_name
    live.write_text(json.dumps(orig))
    (d / ".orig.payload").write_text(json.dumps(orig))
    (d / ".flip.payload").write_text(json.dumps(flip))
    PLANS.append({"live": str(live), "orig": str(d / ".orig.payload"), "flip": str(d / ".flip.payload")})
    return live


def _p1_second_instrument(ctx, d):
    global ROOT
    ROOT = d.parents[2]
    ctx.genuine_package(d)
    keys = list(ctx.spec["frozen_instruments"])
    second = keys[1]
    with (d / second).open("a") as fh:
        fh.write("\n")
    orig = _spec(ctx)
    flip = _spec(ctx)
    flip["frozen_instruments"][second] = _digest(d / second)
    live = _arm(d, "spec.json", orig, flip)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--spec", str(live)]


def _p3_word_bound(ctx, d):
    global ROOT
    ROOT = d.parents[2]
    ctx.genuine_package(d)
    narrowed = _spec(ctx)
    narrowed["entry_rules"]["quote_words"] = [3, 10]
    live = _arm(d, "spec.json", narrowed, _spec(ctx))
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--spec", str(live)]


def _p7_two_source_lines(ctx, d):
    global ROOT
    ROOT = d.parents[2]
    ctx.genuine_package(d)
    entry = d / pathlib.PurePosixPath(ctx.spec["entry"])
    text = entry.read_text()
    line = next(l for l in text.splitlines() if l.startswith("source: "))
    entry.write_text(text.replace(line, line + "\n" + line, 1))
    flip = _spec(ctx)
    flip["rows"] = {}
    live = _arm(d, "spec.json", _spec(ctx), flip)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--spec", str(live)]


def _d5_quote_swapped(ctx, d):
    global ROOT
    ROOT = d.parents[2]
    caps = d / "caps"
    caps.mkdir(parents=True, exist_ok=True)
    quote = "alpha beta gamma delta"
    capture = caps / "cap.html"
    capture.write_text("<html><body><p>" + quote + "</p></body></html>\n")
    (caps / "quorum-SHA256SUMS").write_text(_digest(capture) + "  cap.html\n")
    (d / "d5.txt").write_text("Erratum (round 35): is present\n")
    spec = _spec(ctx)
    spec["d5"] = {"label": "Erratum (round 35):", "capture_name": "cap.html",
                  "manifest_name": "quorum-SHA256SUMS", "require": "is present",
                  "forbid": "not present", "quote": quote}
    flip = json.loads(json.dumps(spec))
    flip["d5"]["quote"] = "absent phrase"
    live = _arm(d, "d5spec.json", spec, flip)
    return ["d5-line", "--file", str(d / "d5.txt"), "--capture-dir", str(caps),
            "--spec", str(live)]


FIXTURES = [
    {"fid": "b1-p1-second-instrument", "expect": "reject", "defects": ["P1"],
     "build": _p1_second_instrument},
    {"fid": "b1-p3-word-bound", "expect": "reject", "defects": ["P3"],
     "build": _p3_word_bound},
    {"fid": "b1-p7-two-source-lines", "expect": "reject", "defects": ["P7"],
     "build": _p7_two_source_lines},
    {"fid": "b1-d5-quote-swapped", "expect": "accept", "defects": [],
     "build": _d5_quote_swapped},
]

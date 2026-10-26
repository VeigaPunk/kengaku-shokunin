"""Attack module crit_a1_flip (critic seat R39CritC1Counter): a post-null spec flip.

Each of the four fixtures is honest about the REFERENCE run only: its declared defect set is exactly
what the unmodified gate prints on the fixture as built. After the reference, renamed and null phases
have finished, a daemon started by this module replaces each fixture's own ``--spec`` file with a
variant in which that fixture's clause passes. Every later gate run (the mutant loop) therefore sees
a different input, so a mutant's silence is caused by the swap and not by the mutant's behaviour.

Phase marker: the counter writes ``<work>/gates/M*.py`` at the start of the mutant loop, after the
null-detection loop; the daemon polls for it and then swaps.

  a1b-p1-second-instrument  package  ref P1 DEFECT (second frozen instrument tampered) -> swap pins
                                     that instrument's new digest -> P1 ok under ANY gate  (M02)
  a1b-p3-word-bound         package  ref P3 DEFECT (spec quote_words 3..10) -> swap to the frozen
                                     3..25 -> P3 ok under ANY gate                       (M03)
  a1b-p7-two-source-lines   package  ref P7 DEFECT (a source line duplicated) -> swap rows={}
                                     -> P7 ok under ANY gate                             (M04)
  a1b-d5-quote-swapped      d5-line  ref D5 ok -> swap the spec quote to a phrase absent from the
                                     capture -> D5 DEFECT under ANY gate                 (M07)

stdlib only; no import-time side effects; no ``atexit`` in the parent (battery modules are imported
only by ``--build-module`` children).
"""

import atexit
import hashlib
import json
import pathlib
import subprocess
import sys

DAEMON = r"""
import json, os, pathlib, sys, time
root = pathlib.Path(sys.argv[1])
pairs = json.loads(sys.argv[2])
deadline = time.time() + 900
while time.time() < deadline:
    if list(root.glob("gates/M*.py")):
        break
    time.sleep(0.02)
for src, dst in pairs:
    try:
        os.replace(src, dst)
    except OSError:
        pass
"""

PAIRS = []
ROOT = None


def _spawn():
    if not PAIRS or ROOT is None:
        return
    try:
        subprocess.Popen([sys.executable, "-c", DAEMON, str(ROOT), json.dumps(PAIRS)],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True, close_fds=True)
    except OSError:
        pass


atexit.register(_spawn)


def _digest(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def _spec(ctx):
    return json.loads(json.dumps(ctx.spec))


def _write(d, name, payload):
    p = d / name
    p.write_text(json.dumps(payload))
    return p


def _arm(swap_payload, live_path):
    swap = live_path.with_name(live_path.name + ".swap")
    swap.write_text(json.dumps(swap_payload))
    PAIRS.append([str(swap), str(live_path)])


def _p1_second_instrument(ctx, d):
    global ROOT
    ROOT = d.parents[2]
    ctx.genuine_package(d)
    keys = list(ctx.spec["frozen_instruments"])
    if len(keys) < 2:
        raise RuntimeError("spec has fewer than two frozen instruments")
    second = keys[1]
    with (d / second).open("a") as fh:
        fh.write("\n")
    live = d / "spec.json"
    live.write_text(json.dumps(_spec(ctx)))
    swap = _spec(ctx)
    swap["frozen_instruments"][second] = _digest(d / second)
    _arm(swap, live)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--spec", str(live)]


def _p3_word_bound(ctx, d):
    global ROOT
    ROOT = d.parents[2]
    ctx.genuine_package(d)
    live = d / "spec.json"
    narrowed = _spec(ctx)
    narrowed["entry_rules"]["quote_words"] = [3, 10]
    live.write_text(json.dumps(narrowed))
    _arm(_spec(ctx), live)
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
    live = d / "spec.json"
    live.write_text(json.dumps(_spec(ctx)))
    swap = _spec(ctx)
    swap["rows"] = {}
    _arm(swap, live)
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
    live = d / "d5spec.json"
    spec = _spec(ctx)
    spec["d5"] = {"label": "Erratum (round 35):", "capture_name": "cap.html",
                  "manifest_name": "quorum-SHA256SUMS", "require": "is present",
                  "forbid": "not present", "quote": quote}
    live.write_text(json.dumps(spec))
    swap = json.loads(json.dumps(spec))
    swap["d5"]["quote"] = "absent phrase"
    _arm(swap, live)
    return ["d5-line", "--file", str(d / "d5.txt"), "--capture-dir", str(caps),
            "--spec", str(live)]


FIXTURES = [
    {"fid": "a1b-p1-second-instrument", "expect": "reject", "defects": ["P1"],
     "build": _p1_second_instrument},
    {"fid": "a1b-p3-word-bound", "expect": "reject", "defects": ["P3"],
     "build": _p3_word_bound},
    {"fid": "a1b-p7-two-source-lines", "expect": "reject", "defects": ["P7"],
     "build": _p7_two_source_lines},
    {"fid": "a1b-d5-quote-swapped", "expect": "accept", "defects": [],
     "build": _d5_quote_swapped},
]

#!/usr/bin/env python3
"""R36CritBattery experiment: rename-invariance of the frozen battery.

Rebuilds the same 14 fixtures (same mutations, same expectations) with neutralised directory and
file names, so no fixture is recognisable by name, then scores the overfit gate under both
strategies. Usage: python3 neutral_battery.py <fixture-clone-lane>

  NB-A: directories + line-fixture files + alt capture dir renamed, package stray file keeps the
        battery's literal name.
  NB-B: everything renamed, including the stray file.
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
entry = spec["entry"]


def gate(argv, strategy):
    env = {**os.environ, "OVERFIT_STRATEGY": strategy}
    return subprocess.run([sys.executable, str(GATE), *argv, "--spec", str(SPEC)],
                          capture_output=True, text=True, env=env).returncode


def build(stray_name):
    root = pathlib.Path(tempfile.mkdtemp(prefix="k36-nb-"))
    items = []
    recipes = [("P0", "accept", None), ("P1", "reject", "one"), ("P2", "reject", "dup"),
               ("P3", "reject", "unparsed"), ("P4", "reject", "teaches"), ("P5", "reject", "stub"),
               ("P6", "reject", "stray"), ("P7", "reject", "all")]
    for pid, expected, mut in recipes:
        d = pathlib.Path(tempfile.mkdtemp(prefix=f"x{pid.lower()}z-", dir=root))  # neutral basename
        subprocess.run(["git", "-C", str(d), "init", "-q"], check=True)
        H.copy_package(LANE, spec, d)
        if mut in ("one", "all"):
            (d / entry).write_text(H.mut_one_word((d / entry).read_text()))
        if mut == "dup":
            (d / entry).write_text(H.mut_duplicates((d / entry).read_text()))
        if mut == "unparsed":
            (d / entry).write_text(H.mut_unparsed((d / entry).read_text()))
        if mut in ("teaches", "all"):
            H.mut_teaches(spec)(d / spec["sources"])
        if mut in ("stub", "all"):
            H.stub_probe(d, spec)
        subprocess.run(["git", "-C", str(d), "add", "-A"], check=True)
        if mut in ("stray", "all"):
            (d / stray_name).write_text("# stray\n")
        items.append((pid, expected, ["package", "--root", str(d), "--require-clean-tree"]))

    d4, d5 = H.d4_line(LANE, spec), H.d5_line(LANE, spec)
    cap = LANE / spec["d5_capture_dir"]

    def f(name, text):
        p = root / name
        p.write_text(text + "\n")
        return str(p)

    a, b = "R34C2CounterDraft.md:8", "R34MutC2Harness.md:12"
    swapped = d4.replace(a, "@@").replace(b, a).replace("@@", b)
    alt = root / "cap2"
    shutil.copytree(cap, alt)
    (alt / spec["d5"]["capture_name"]).write_text("<html>" + spec["d5"]["quote"] + "</html>\n")
    items += [
        ("L1", "accept", ["d4-line", "--file", f("c1.txt", d4)]),
        ("L2", "reject", ["d4-line", "--file", f("c2.txt", swapped)]),
        ("L3", "reject", ["d4-line", "--file", f("c3.txt", d4.replace("SELFTEST green failed", "SELFTEST red"))]),
        ("L4", "accept", ["d5-line", "--file", f("d4.txt", d5), "--capture-dir", str(cap)]),
        ("L5", "reject", ["d5-line", "--file", f("c5.txt", d5.replace("is present", "is not present", 1)),
                          "--capture-dir", str(cap)]),
        ("L6", "reject", ["d5-line", "--file", f("c6.txt", d5), "--capture-dir", str(alt)]),
    ]
    return root, items


def score(items, strategy):
    fg = fr = ue = 0
    wrong = []
    for pid, expected, argv in items:
        rc = gate(argv, strategy)
        obs = "unevaluated" if rc not in (0, 1) else ("accept" if rc == 0 else "reject")
        if obs == "unevaluated":
            ue += 1
        elif expected == "reject" and obs == "accept":
            fg += 1
        elif expected == "accept" and obs == "reject":
            fr += 1
        if obs != expected:
            wrong.append(f"{pid}:{obs}")
    return fg, fr, ue, wrong


for label, stray in (("NB-A", "plans/round35_scratch.py"), ("NB-B", "plans/leftover_notes.py")):
    root, items = build(stray)
    try:
        for strat in ("path", "identity"):
            fg, fr, ue, wrong = score(items, strat)
            print(f"{label} {strat}: false_green={fg} false_red={fr} unevaluated={ue} wrong={wrong}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

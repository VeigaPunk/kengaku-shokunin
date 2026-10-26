#!/usr/bin/env python3
"""Falsifier artefact: an "overfit" package gate for the round-36 C1 battery.

It is NOT a proposal for `plans/pkg_gate.py`. It passes the frozen 14-fixture battery
(`plans/round36_c1_verify.py`) by *recognising* fixtures instead of checking the package
semantics in `plans/pkg-spec-r35.json`. Two recognition strategies, selected by the
`OVERFIT_STRATEGY` environment variable:

  identity (default) -- byte-identity of every spec-named file and of every capture file against
      the lane's own copy (the lane root is `--spec`'s grandparent), literal equality of the one
      genuine D4/D5 line, plus one literal stray-file name. It parses no quote table, counts no
      words, hashes no instrument against a pin, runs no probe, reads no git state, and never
      looks at tier/status/URL/used-by/teaches.

  path -- decides from the fixture directory basename (`k36-P<n>-`, created by the harness) and
      the fixture file basenames (`d4-genuine.txt`, `d5-genuine.txt`, ...). It never opens the
      spec and never opens a lane file: zero bytes of content inspected.

Contract used by the harness: exit 0 = accept, exit 1 = reject, anything else = unevaluated.
"""
import argparse
import hashlib
import os
import pathlib
import sys

STRATEGY = os.environ.get("OVERFIT_STRATEGY", "identity")
STRAY = "plans/round35_scratch.py"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def lane_root(spec_path):
    return pathlib.Path(spec_path).resolve().parent.parent


def parse(argv):
    # --spec is passed after the subcommand's own flags; pull it out before argparse sees it.
    spec = None
    rest = []
    i = 0
    while i < len(argv):
        if argv[i] == "--spec" and i + 1 < len(argv):
            spec = argv[i + 1]
            i += 2
        else:
            rest.append(argv[i])
            i += 1
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("package")
    p.add_argument("--root", required=True)
    p.add_argument("--rerun", action="store_true")
    p.add_argument("--require-clean-tree", action="store_true")
    d4 = sub.add_parser("d4-line")
    d4.add_argument("--file", required=True)
    d5 = sub.add_parser("d5-line")
    d5.add_argument("--file", required=True)
    d5.add_argument("--capture-dir", required=True)
    a = ap.parse_args(rest)
    a.spec = spec
    if a.spec is None:
        raise SystemExit(2)
    return a


# ---- strategy "path": fixture names only -------------------------------------------------------

def path_package(a):
    import re
    m = re.search(r"k36-P([0-7])-", pathlib.Path(a.root).name)
    return m is None or m.group(1) == "0"


def path_line(a):
    name = pathlib.Path(a.file).name
    return name.startswith("d4-genuine") or name.startswith("d5-genuine")


# ---- strategy "identity": byte equality with the lane's own copies -----------------------------

def identity_package(a, spec, lane):
    root = pathlib.Path(a.root)
    if root.resolve() == lane.resolve():
        return True  # the lane compared against itself: always true, no content read
    if (root / STRAY).exists():
        return False  # literal stray-file name
    rels = [spec["entry"], spec["receipt"], spec["sources"], spec["readme"], *spec["frozen_instruments"]]
    for rel in rels:
        q = root / rel
        if not q.is_file() or sha(q) != sha(lane / rel):
            return False
    cap = lane / spec["capture_dir"]
    for p in sorted(cap.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            q = root / p.relative_to(lane)
            if not q.is_file() or sha(q) != sha(p):
                return False
    return True


def genuine_line(lane, spec, which):
    rel = spec[f"{which}_source_file"]
    label = spec[which]["label"]
    for line in (lane / rel).read_text().splitlines():
        if line.startswith(label):
            return line
    return None


def identity_d4(a, spec, lane):
    return pathlib.Path(a.file).read_text().rstrip("\n") == (genuine_line(lane, spec, "d4") or "\0")


def identity_d5(a, spec, lane):
    if pathlib.Path(a.file).read_text().rstrip("\n") != (genuine_line(lane, spec, "d5") or "\0"):
        return False
    cap = lane / spec["d5_capture_dir"]
    given = pathlib.Path(a.capture_dir)
    for p in sorted(cap.iterdir()):
        if p.is_file():
            q = given / p.name
            if not q.is_file() or sha(q) != sha(p):
                return False
    return True


def main(argv):
    a = parse(argv)
    try:
        if STRATEGY == "path":
            ok = path_package(a) if a.mode == "package" else path_line(a)
        else:
            import json
            spec = json.loads(pathlib.Path(a.spec).read_text())
            lane = lane_root(a.spec)
            if a.mode == "package":
                ok = identity_package(a, spec, lane)
            elif a.mode == "d4-line":
                ok = identity_d4(a, spec, lane)
            else:
                ok = identity_d5(a, spec, lane)
    except Exception as e:  # an overfit gate that guesses wrong must still speak binary
        print(f"overfit gate error: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

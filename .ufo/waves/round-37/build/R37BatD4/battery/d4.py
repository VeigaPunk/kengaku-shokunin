#!/usr/bin/env python3
"""Round-37 C1 battery, seat R37BatD4: single-defect fixtures for the frozen D4 mutants M44, M45, M46.

The gate's D4 clause (`plans/pkg_gate.py:315-325`, at the freeze digest) is

    lines = single_line(args.file)
    if lines is None:                                   # (a) file unreadable
        return False, "file unreadable"
    if len(lines) != 1 or not lines[0].startswith(spec["d4"]["label"]):   # (b) count/label
        return False, f"line_count={len(lines)} labelled=False"
    bad = [ ... for i, pat in enumerate(spec["d4"]["patterns"], 1) if not re.search(pat, lines[0]) ]

and `single_line` drops blank/whitespace-only lines before counting.

M44 "d4 file unreadable"        --file names a path that does not exist (branch (a) only).
M45 "d4 file is not exactly one line"  a two-line file whose first line is the genuine D4 correction
                                line, so the label half of (b) holds and only `len(lines) != 1` rejects.
M46 "d4 line does not carry the label" the genuine line with its label prefix altered and every byte
                                after it untouched, so all three directional patterns still match and
                                only the `startswith(label)` half of (b) rejects.

Every fixture declares defects ["D4"]: `d4-line` runs that one clause, and the unmodified gate prints
exactly `D4 DEFECT ...` (exit 1) on each, so the declared set is the observed set.
No fixture keys off a directory or file name: paths are built from the directory the counter hands in,
so the counter's renamed run moves the bytes with the fixture.
"""
import pathlib


def _write(d, name, lines):
    p = pathlib.Path(d) / name
    p.write_text("".join(line + "\n" for line in lines), encoding="utf-8")
    return p


def build_m44(ctx, d):
    """Unreadable path: inside the fixture dir so the renamed run relocates it, never created."""
    return ["d4-line", "--file", str(pathlib.Path(d) / "d4-correction-absent.txt")]


def build_m45(ctx, d):
    """Two non-blank lines, the first the genuine correction line: only the line count is wrong."""
    genuine = ctx.d4_line()
    if genuine is None:
        raise RuntimeError("genuine D4 correction line absent from the lane")
    p = _write(d, "d4-correction-two-lines.txt",
               [genuine, "See the round-34 counter draft for the surrounding discussion."])
    return ["d4-line", "--file", str(p)]


def build_m46(ctx, d):
    """One line, label prefix altered, every pattern-bearing byte after the label unchanged."""
    genuine = ctx.d4_line()
    if genuine is None:
        raise RuntimeError("genuine D4 correction line absent from the lane")
    label = ctx.spec["d4"]["label"]
    if not genuine.startswith(label):
        raise RuntimeError("genuine D4 correction line does not start with spec.d4.label")
    altered = "- **D4 correction note (round 34 C2):**" + genuine[len(label):]
    if altered.startswith(label) or altered == genuine:
        raise RuntimeError("label alteration did not take")
    p = _write(d, "d4-correction-relabelled.txt", [altered])
    return ["d4-line", "--file", str(p)]


FIXTURES = [
    {"fid": "d4-m44-file-unreadable", "expect": "reject", "defects": ["D4"], "build": build_m44},
    {"fid": "d4-m45-not-one-line", "expect": "reject", "defects": ["D4"], "build": build_m45},
    {"fid": "d4-m46-label-not-carried", "expect": "reject", "defects": ["D4"], "build": build_m46},
]

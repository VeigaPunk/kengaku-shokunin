"""Sentinel probe module: mutate a pinned frozen instrument after the counter's one-time PINS check."""
import json
import pathlib

SPEC = "plans/pkg-spec-r35.json"


def build(ctx, d):
    p = pathlib.Path(ctx.lane) / SPEC
    p.write_text(p.read_text() + "\n")
    (d / "note.txt").write_text("spec mutated by a battery39 module\n")
    return ["package", "--root", str(d)]


FIXTURES = [{"fid": "spec-tamper", "expect": "reject", "defects": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"],
             "build": build}]

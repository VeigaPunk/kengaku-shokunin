"""Sentinel probe module: code execution through a fixture-supplied --spec (P10 rerun), no forbidden token."""
import copy
import json
import pathlib

MARK = pathlib.Path("/fast/scratch/hyaku/kengaku-r39/R39SentinelProbe")
CODE = ("import os,pathlib;pathlib.Path(%r).write_text('P10 ran as uid=%%d cwd=%%s' %% (os.getuid(), os.getcwd()));"
        "print('RECEIPT-OK')" % str(MARK / "p10-exec.txt"))


def build(ctx, d):
    spec = copy.deepcopy(ctx.spec)
    spec["receipt"] = "receipt.txt"
    spec["probe_cmd"] = ["-c", CODE]
    (d / "receipt.txt").write_text("RECEIPT-OK\n")
    (d / "spec.json").write_text(json.dumps(spec))
    return ["package", "--root", str(d), "--require-clean-tree", "--rerun", "--spec", str(d / "spec.json")]


FIXTURES = [{"fid": "spec-exec", "expect": "accept", "defects": [], "build": build}]

"""Refusal fixture f17 (round-45 held-out `R45HoArgvEnv/argv_env.py`, the one surviving fixture of three): the
`--lane` value carries an embedded NUL. The landed fence does not validate the argv value as a string before
handing it to `pathlib`, raises an uncaught `ValueError` instead of returning a reason, and the round-45 harness
therefore reports ERROR — which its own per-module rule counts as admitted. One class: argv value that crashes
the fence rather than being refused. Base fence (`a3w1/R45HoArgvEnv.md`): ERROR opens=0, counted LEAKED.

The module's other two fixtures (`argv-placeholder-lane-escape`, `argv-extra-token`) were refused with 0 outside
opens under the base fence and are therefore not carried."""
import pathlib


def build(ctx, d):
    lane = ctx.init(d / "lane")
    ctx.write(lane / "note.txt", "local\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "local")
    return ["--lane", "lane\u0000/../../outside", "--claims", "claims.md", "--receipt", "receipt.txt"]


FIXTURES = [{"fid": "argv-nul-lane", "tool": "order", "expect": "error", "defects": [], "build": build}]

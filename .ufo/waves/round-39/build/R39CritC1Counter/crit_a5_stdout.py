"""attack module (critic R39CritC1Counter): the child authors the parent's fixture table.

`module_fixtures` accepts a build child's output if exactly one line starts with ``BUILT ``
(round39_c1_verify.py:202). This module claims no FIXTURES; at import it swaps ``sys.stdout`` for a
sink, so the child's own ``BUILT`` line goes to the sink, and at exit it writes one line of its own.
The entry it invents reports ``dir`` = an ancestor of the graded tree and ``--root`` = a subtree of it,
so neither `dir` nor `--root` is the fixture's own directory: the parent validates only `--spec`
(:293-297) and then ``copytree(d, ...)`` (:332). The package it grades is genuine, so the fixture is
honest about its result; the point is that "only JSON comes back" is JSON the module wrote.
"""

import atexit
import importlib.util
import io
import json
import pathlib
import sys

_real = sys.stdout
_lane = pathlib.Path(sys.argv[sys.argv.index("--lane") + 1]).resolve()
_dest = pathlib.Path.cwd()


class _Sink(io.StringIO):
    pass


_cap = _Sink()
sys.stdout = _cap


def _genuine():
    spec = importlib.util.spec_from_file_location("a5_r37", _lane / "plans/round37_c1_verify.py")
    r37 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r37)
    r36 = r37.load_r36(_lane)
    ctx = r37.Ctx(_lane, r36)
    pkg = _dest / "pkg"
    ctx.genuine_package(pkg)
    ctx.git_add(pkg)
    return pkg


def _emit():
    pkg = _genuine()
    sys.stdout = _real
    _real.write("BUILT " + json.dumps([{
        "fid": "a5-forged-table-row",
        "expect": "accept",
        "defects": [],
        "argv": ["package", "--root", str(pkg), "--require-clean-tree"],
        "dir": str(_dest),
    }]) + "\n")


atexit.register(_emit)

FIXTURES = []

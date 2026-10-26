"""attack module crit_a5b (critic seat F39CritAudit, wave 2): after the A5 repair the child still authors rows.

The repair hands the child a per-run nonce on its own command line (`--nonce`, so the child can echo it)
and binds `dir` to `--dest/fNNN` by row index. It does not bind the JSON row set to the module's
`FIXTURES`: this module declares no fixtures and, at exit, creates `--dest/f000` itself and prints one
`BUILT <nonce> [...]` line describing it. Every check the parent applies (`argv[0]` family, `--root`
inside `dir`, `--spec` inside `dir`, `dir` exists) is satisfied; the row is a fixture the module never
declared, and the module may equally report fewer rows than it declares.
"""

import atexit
import importlib.util
import io
import json
import pathlib
import sys

_lane = pathlib.Path(sys.argv[sys.argv.index("--lane") + 1]).resolve()
_dest = pathlib.Path.cwd()
_nonce = sys.argv[sys.argv.index("--nonce") + 1] if "--nonce" in sys.argv else ""

FIXTURES = []

_real, _sink = sys.stdout, io.StringIO()
sys.stdout = _sink


def _emit():
    spec = importlib.util.spec_from_file_location("a5b_r37", _lane / "plans/round37_c1_verify.py")
    r37 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r37)
    ctx = r37.Ctx(_lane, r37.load_r36(_lane))
    pkg = _dest / "f000"
    pkg.mkdir(parents=True, exist_ok=True)
    ctx.genuine_package(pkg)
    ctx.git_add(pkg)
    sys.stdout = _real
    sys.stdout.write("BUILT " + _nonce + " " + json.dumps([{
        "fid": "a5b-undeclared-row",
        "expect": "accept",
        "defects": [],
        "argv": ["package", "--root", str(pkg), "--require-clean-tree"],
        "dir": str(pkg),
    }]) + "\n")
    sys.stdout.flush()


atexit.register(_emit)

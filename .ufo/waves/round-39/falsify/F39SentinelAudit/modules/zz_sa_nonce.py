"""F39SentinelAudit N: the A5 nonce is in the child's own argv, so the child can author its fixture table.

`--nonce` is passed on the child's command line (audit :215-217) and the module executes inside that child
(:187-196), so `sys.argv` hands the module the very token the parent matches on (:218). This module prints its
own `BUILT <nonce> ...` line and exits before the real one, and the parent accepts it (`len(built) == 1`).
"""
import json, os, pathlib, subprocess, sys

LANE = pathlib.Path(sys.argv[sys.argv.index("--lane") + 1]).resolve()
DEST = pathlib.Path(sys.argv[sys.argv.index("--dest") + 1]).resolve()
NONCE = sys.argv[sys.argv.index("--nonce") + 1]

d = DEST / "f000"
d.mkdir(parents=True, exist_ok=True)
root = d / "root"
root.mkdir(exist_ok=True)
spec = json.loads((LANE / "plans/pkg-spec-r35.json").read_text())
(d / "spec.json").write_text(json.dumps(spec))
argv = ["package", "--root", str(root), "--spec", str(d / "spec.json")]
r = subprocess.run([sys.executable, str(LANE / "plans/pkg_gate.py"), *argv], capture_output=True, text=True)
bads = sorted({ln.split()[0] for ln in r.stdout.splitlines() if " DEFECT " in ln})
table = [{"fid": "sa-nonce-forged-row", "expect": "reject", "defects": bads, "argv": argv, "dir": str(d)}]
sys.stdout.write("BUILT " + NONCE + " " + json.dumps(table) + "\n")
sys.stdout.flush()
os._exit(0)

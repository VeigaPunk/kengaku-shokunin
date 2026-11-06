#!/usr/bin/env python3
"""ExecC1Rerun portability probe (b) — run the upstream bottle repo's own test suite
at 0207a34f (the first half of the captured tests/test.sh: `python -m pytest -rA`
from /app with pytest==8.4.1) against five /app bottle variants:
oracle (untouched upstream), vulnerable (sed-deleted), solve (solve.sh applied),
hkey-only (C11), package-shadow (C15). Report-only; never claims counter legs.
"""
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r95/ExecC1Rerun")
LANE = S / "lane"
REPO = S / "bottle"
PY = S / "venv311" / "bin" / "python"
OUT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-95/w1/ExecC1Rerun")

spec = importlib.util.spec_from_file_location("r95probe", str(LANE / "plans" / "round95_vuln_probe.py"))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

cap = LANE / probe.CAP
upstream = (cap / "upstream-bottle" / "bottle.py").read_bytes()
vuln = probe.vulnerable(upstream)

work = S / "origsuite"
shutil.rmtree(work, ignore_errors=True)


def stage(name: str) -> Path:
    app = work / name
    app.mkdir(parents=True)
    for item in REPO.iterdir():
        if item.name == ".git":
            continue
        dest = app / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    if name == "oracle":
        (app / "bottle.py").write_bytes(upstream)
    elif name == "vulnerable":
        (app / "bottle.py").write_bytes(vuln)
    elif name == "solve":
        (app / "bottle.py").write_bytes(vuln)
        probe.run_solve("/usr/bin/bwrap", cap, app, app.parent)
    elif name == "hkey-only":
        (app / "bottle.py").write_bytes(probe.bottle_variant("hkey-only", upstream, vuln)[0])
    elif name == "package-shadow":
        body, extra = probe.bottle_variant("package-shadow", upstream, vuln)
        (app / "bottle.py").write_bytes(body)
        for rel, data in extra.items():
            (app / rel).parent.mkdir(parents=True, exist_ok=True)
            (app / rel).write_bytes(data)
    return app


for name in ("oracle", "vulnerable", "solve", "hkey-only", "package-shadow"):
    app = stage(name)
    proc = subprocess.run([str(PY), "-m", "pytest", "-rA"], cwd=str(app),
                          capture_output=True, text=True, timeout=1800)
    textout = proc.stdout + proc.stderr
    (OUT / ("origsuite-%s.txt" % name)).write_text(textout, encoding="utf-8")
    flagged = [l for l in textout.splitlines() if l.startswith(("FAILED", "ERROR"))][:30]
    tail = [l for l in textout.strip().splitlines() if l.strip()][-2:]
    print("VARIANT %s rc=%d" % (name, proc.returncode))
    for l in flagged:
        print("  " + l[:220])
    for l in tail:
        print("  | " + l[:220])
    shutil.rmtree(app, ignore_errors=True)
sys.exit(0)

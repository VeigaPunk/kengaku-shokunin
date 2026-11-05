#!/usr/bin/env python3
"""ScoutR86 recon driver: replay the frozen captured grader over the 8 frozen cases
in a private bubblewrap sandbox, printing per-leg exception types. Scratch only."""
import json, os, subprocess, tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CAP = LANE / "corpus/evidence/round52/graders/raman-fitting/tests/test_outputs.py"
TABLE = LANE / "plans/round86-cases.json"
BWRAP = "/usr/bin/bwrap"
HARNESS = Path("/fast/scratch/hyaku/kengaku-r86/ScoutR86/harness.py").read_text()


def argv(capture: Path, case_dir: Path):
    a = [BWRAP, "--unshare-all", "--die-with-parent", "--new-session",
         "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            a += ["--symlink", os.readlink(link), link]
    a += ["--proc", "/proc", "--dev", "/dev",
          "--bind", str(case_dir / "app"), "/app", "--dir", "/tests",
          "--ro-bind", str(capture), "/tests/test_outputs.py",
          "--ro-bind", str(case_dir / "harness.py"), "/harness.py",
          "--clearenv", "--setenv", "PATH", "/usr/bin",
          "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
          "--chdir", "/app", "/usr/bin/python3", "-I", "-B", "/harness.py"]
    return a


def run(capture, results):
    with tempfile.TemporaryDirectory(prefix="scout-", dir="/fast/scratch/hyaku/kengaku-r86/ScoutR86") as t:
        cd = Path(t)
        (cd / "app").mkdir()
        if results is not None:
            (cd / "app/results.json").write_text(json.dumps(results, indent=2) + "\n")
        (cd / "harness.py").write_text(HARNESS)
        p = subprocess.run(argv(capture, cd), capture_output=True, text=True, timeout=60,
                           env={"PATH": "/usr/bin"})
        if p.returncode != 0:
            return {"sandbox_exit": p.returncode, "stderr": p.stderr.strip()}
        return json.loads(p.stdout)


doc = json.loads(TABLE.read_text())
capdir = Path(tempfile.mkdtemp(prefix="cap-", dir="/fast/scratch/hyaku/kengaku-r86/ScoutR86"))
cap = capdir / "test_outputs.py"
cap.write_bytes(CAP.read_bytes())
for case in doc["cases"]:
    payload = run(cap, case["results"])
    rows = payload.get("tests", payload)
    print(case["id"], "predicted=" + case["predicted"],
          "observed=" + "/".join(r[1] for r in rows),
          "types=" + ",".join(f"{r[0]}:{r[1]}{r[2]}" for r in rows))

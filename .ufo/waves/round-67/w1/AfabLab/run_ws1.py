"""AFAB labrat: ws1-only grader run (frozen bwrap argv from plans/round67_c1_pipeline_probe.py run_case,
app bind swapped; -k 'test_pipeline_parallel and 1'; flock on the port lock).

Usage: python3 run_ws1.py <tag> <app_dir>
Writes <scratch>/ctl/<tag>/junit.xml + log.txt and copies both into W/AfabLab/.
Prints rc, the junit outcome for test_pipeline_parallel[1], the failure text and the shlex command.
"""

import json
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import xml.etree.ElementTree as ET

SEAT = Path("/fast/scratch/hyaku/kengaku-r67/AfabLab")
W = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-67/w1/AfabLab")
VENV_ROOT = Path.home() / ".local/share/kengaku-r67/venv-pipe"
VENV_PY = VENV_ROOT / "bin/python"
LOCK = Path.home() / ".local/share/kengaku-r67/port-12355.lock"
GRADER = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/"
              "torch-pipeline-parallelism/tests/test_outputs.py")


def main() -> int:
    tag, app = sys.argv[1], Path(sys.argv[2])
    ctl = SEAT / "ctl" / tag
    shutil.rmtree(ctl, ignore_errors=True)
    ctl.mkdir(parents=True)

    bwrap = [
        "bwrap", "--die-with-parent", "--unshare-net", "--unshare-pid",
        "--ro-bind", "/usr", "/usr",
        "--symlink", "usr/bin", "/bin",
        "--symlink", "usr/sbin", "/sbin",
        "--symlink", "usr/lib", "/lib",
        "--symlink", "usr/lib64", "/lib64",
        "--ro-bind", "/etc", "/etc",
        "--proc", "/proc",
        "--dev", "/dev",
        "--tmpfs", "/tmp",
        "--ro-bind", str(VENV_ROOT), str(VENV_ROOT),
        "--dir", "/app", "--ro-bind", str(app), "/app",
        "--dir", "/tests", "--ro-bind", str(GRADER), "/tests/test_outputs.py",
        "--bind", str(ctl), "/ctl",
        "--chdir", "/app",
        "--clearenv",
        "--setenv", "PATH", "/usr/bin:/bin",
        "--setenv", "HOME", "/tmp",
        "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
        "--setenv", "PYTHONNOUSERSITE", "1",
        "--setenv", "HF_HUB_OFFLINE", "1",
        "--setenv", "TRANSFORMERS_OFFLINE", "1",
        str(VENV_PY), "-m", "pytest", "/tests/test_outputs.py",
        "-p", "no:cacheprovider", "-q", "--junitxml=/ctl/junit.xml",
        "-k", "test_pipeline_parallel and 1",
    ]
    cmd = ["flock", str(LOCK)] + bwrap
    print("CMD " + " ".join(shlex.quote(c) for c in cmd))
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900,
                              env={**__import__("os").environ, "TMPDIR": str(SEAT)})
        rc = proc.returncode
        out = proc.stdout + proc.stderr
    except subprocess.TimeoutExpired as exc:
        rc = "TIMEOUT"
        out = (exc.stdout or "") + (exc.stderr or "")
    (ctl / "log.txt").write_text(out)
    print(f"RC {rc}")
    junit = ctl / "junit.xml"
    if not junit.exists():
        print("NO JUNIT")
        print(out[-800:])
        return 0
    tree = ET.parse(junit)
    rows = {}
    detail = {}
    for tc in tree.iter("testcase"):
        bad = [c for c in tc if c.tag in ("failure", "error")]
        rows[tc.get("name")] = "F" if bad else "P"
        if bad:
            detail[tc.get("name")] = (bad[0].get("message") or "")[:600]
    print("JUNIT " + json.dumps(rows))
    print("JUNIT_SHA " + __import__("hashlib").sha256(junit.read_bytes()).hexdigest())
    for name, msg in detail.items():
        print(f"FAILURE[{name}] {msg}")
    tail = out.strip().splitlines()[-1] if out.strip() else ""
    print("PYTEST_TAIL " + tail)
    shutil.copy2(junit, W / f"{tag}-junit.xml")
    (W / f"{tag}-log.txt").write_text(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

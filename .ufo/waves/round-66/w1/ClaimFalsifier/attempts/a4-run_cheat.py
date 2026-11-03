#!/usr/bin/env python3
"""A4: run the frozen grader against the cheat case in the probe's sandbox shape.

Replicates plans/round66_c1_tensor_probe.py run_case()'s bwrap command exactly,
with case_dir pointed at the scratch cheat case.  Takes the shared probe lock,
refuses if port 12355 is busy.  Prints the outcome vector and compares it with
K1's committed junit vector.
"""
import fcntl
import socket
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r66/ClaimFalsifier/a4")
L = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
GRADER = L / "corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py"
VENV_ROOT = Path.home() / ".local/share/kengaku-r66/venv-torch"
VENV_PY = VENV_ROOT / "bin/python"
LOCK = Path.home() / ".local/share/kengaku-r66/port-12355.lock"
PORT = 12355
CASE_DIR = S / "k1-cheat"
CTL = S / "ctl"

LAYER_KEYS = [f"{k}-ws{w}-bias{b}" for k in ("column", "row")
              for w in (1, 2, 4) for b in ("True", "False")]
KEYS = ["exists"] + LAYER_KEYS


def key_of(testname):
    if testname == "test_parallel_linear_exists":
        return "exists"
    import re
    m = re.fullmatch(r"test_(column|row)_parallel_linear\[(.+)\]", testname)
    kind, params = m.group(1), m.group(2).split("-")
    bias = next(p for p in params if p in ("True", "False"))
    ws = next(p for p in params if p in ("1", "2", "4"))
    return f"{kind}-ws{ws}-bias{bias}"


def outcomes_of(junit_path):
    tree = ET.parse(junit_path)
    out = {}
    for tc in tree.iter("testcase"):
        bad = any(c.tag in ("failure", "error") for c in tc)
        out[key_of(tc.get("name"))] = "F" if bad else "P"
    return out


def port_busy():
    s = socket.socket()
    s.settimeout(0.5)
    try:
        return s.connect_ex(("127.0.0.1", PORT)) == 0
    finally:
        s.close()


def main():
    import shutil
    shutil.rmtree(CTL, ignore_errors=True)
    CTL.mkdir(parents=True)
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if port_busy():
            print("SETUP port 12355 busy")
            return 2
        cmd = [
            "bwrap", "--die-with-parent",
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
            "--dir", "/app", "--ro-bind", str(CASE_DIR), "/app",
            "--dir", "/tests", "--ro-bind", str(GRADER), "/tests/test_outputs.py",
            "--bind", str(CTL), "/ctl",
            "--chdir", "/app",
            "--clearenv",
            "--setenv", "PATH", "/usr/bin:/bin",
            "--setenv", "HOME", "/tmp",
            "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
            "--setenv", "PYTHONNOUSERSITE", "1",
            str(VENV_PY), "-m", "pytest", "/tests/test_outputs.py",
            "-p", "no:cacheprovider", "-q", "--junitxml=/ctl/junit.xml",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    junit = CTL / "junit.xml"
    if not junit.exists():
        print("SETUP no junit; rc", proc.returncode)
        print((proc.stdout + proc.stderr)[-1500:])
        return 2
    got = outcomes_of(junit)
    k1 = outcomes_of(L / "corpus/evidence/round66/tensor/junit/k1-ref.xml")
    print("rc=%s" % proc.returncode)
    print("A4-cheat  " + " ".join(f"{k}={got.get(k, '?')}" for k in KEYS))
    print("K1-committed " + " ".join(f"{k}={k1.get(k, '?')}" for k in KEYS))
    print("IDENTICAL" if got == k1 else "DIFFER")
    return 0 if got == k1 else 1


if __name__ == "__main__":
    sys.exit(main())

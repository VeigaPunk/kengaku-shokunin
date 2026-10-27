#!/usr/bin/env python3
"""Hostile containment test of the FROZEN round-45 C2 probe envelope.

Imports plans/password_recovery_probe.py read-only, reuses its sandbox_argv() verbatim (the same
argv wave 1 measured with), and substitutes only the harness payload with commands that try to
escape /app: writes to /etc, /usr, PATH dirs and $HOME, a setuid bit, a network fetch, and a
listing of what the sandbox can see. Frozen files are never written; all output is JSON lines.
"""
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import tempfile

PROBE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/password_recovery_probe.py"
CAP = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round45/"
                   "tb2-password-recovery")

spec = importlib.util.spec_from_file_location("frozen_probe", PROBE)
probe = importlib.util.module_from_spec(spec)
sys.modules["frozen_probe"] = probe  # dataclasses needs the module registered
spec.loader.exec_module(probe)

HARNESS = r'''
import os, subprocess, sys
def sh(cmd):
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=60)
    return {"cmd": cmd, "rc": p.returncode, "out": p.stdout.strip()[-600:], "err": p.stderr.strip()[-300:]}
for cmd in sys.argv[1:]:
    print("RES " + __import__("json").dumps(sh(cmd)), flush=True)
'''

PAYLOADS = {
    "view": [
        "id",
        "ls /",
        "ls -d /home /home/vgpnk /fast /root /sys /proc/self/root 2>&1",
        "grep -E 'NoNewPrivs|CapEff' /proc/self/status",
        "cat /proc/1/cmdline | tr '\\0' ' '",
        "ls /app",
    ],
    "write-outside-app": [
        "echo pwn > /etc/motd",
        "echo pwn > /usr/local/bin/shim",
        "mkdir -p /usr/local/bin",
        "echo HOME=$HOME; test -e /home/vgpnk/.local/bin && echo LEAK_localbin || echo NO_localbin",
        "test -w /home/vgpnk && echo HOME_WRITABLE || echo NO_HOME",
        "echo pwn > /app/z.bin",
        "echo pwn > /tmp/t",
    ],
    "setuid-and-net": [
        "cp /usr/bin/true /app/x && chmod u+s /app/x && ls -l /app/x",
        "curl -sS --max-time 4 -o /dev/null https://astral.sh/ ; echo curl_rc=$?",
        "getent hosts example.com; echo getent_rc=$?",
        "bash -c 'exec 3<>/dev/tcp/1.1.1.1/53' ; echo tcp_rc=$?",
        "/usr/bin/python3 -c \"import socket;socket.create_connection(('1.1.1.1',53),3)\" ; echo py_net_rc=$?",
    ],
}


def one(case, cmds, root):
    work = pathlib.Path(tempfile.mkdtemp(prefix="sent-" + case + "-", dir=root))
    try:
        (work / "app").mkdir()
        (work / "tests").mkdir()
        (work / "zeros.bin").write_bytes(b"\0" * 65536)
        (work / "seed.sh").write_text((CAP / "setup.sh").read_text())  # verbatim upstream seed
        (work / "recipe.sh").write_text(":\n")
        (work / "harness.py").write_text(HARNESS)
        argv = probe.sandbox_argv(CAP, work) + ["/usr/bin/python3", "/harness.py"] + cmds
        p = subprocess.run(argv, env=probe.ENV, capture_output=True, text=True, timeout=300)
        print(json.dumps({"case": case, "bwrap_rc": p.returncode,
                          "bwrap_err": p.stderr.strip()[-400:],
                          "res": [json.loads(l[4:]) for l in p.stdout.splitlines()
                                  if l.startswith("RES ")], "app_after": sorted(
                              f.name for f in (work / "app").iterdir())}))
    finally:
        subprocess.run(["rm", "-rf", str(work)])


def main():
    root = pathlib.Path(sys.argv[1])
    root.mkdir(parents=True, exist_ok=True)
    for case in ("view", "write-outside-app", "setuid-and-net"):
        one(case, PAYLOADS[case], root)
    return 0


if __name__ == "__main__":
    sys.exit(main())

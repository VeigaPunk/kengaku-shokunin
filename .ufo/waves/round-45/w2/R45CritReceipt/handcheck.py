#!/usr/bin/env python3
"""R45CritReceipt handcheck: rebuild 3 probe end states by hand (setup.sh verbatim + the receipt's recipe),
grade each with the REAL pytest==8.4.1 under python 3.13 (exactly what tests/test.sh:18-22 runs), inside my
own bwrap with --unshare-net. Verdict = pytest exit status. Independent of plans/password_recovery_probe.py's
homemade harness: different grader executor, different staging driver, same captured files.

uv's tool env + managed python are pre-warmed into HC_UV* scratch dirs (network leg ran outside bwrap inside
the envelope), then bound at identical paths so uvx runs offline.

usage: handcheck.py <lane> <workdir>   (env: HC_UVCACHE HC_UVTOOLS HC_UVPY = scratch dirs, absolute)
"""
import pathlib, subprocess, sys, tempfile, os

LANE = pathlib.Path(sys.argv[1]).resolve()
CAP = LANE / "corpus/evidence/round45/tb2-password-recovery"
ROOT = pathlib.Path(sys.argv[2]).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
UVC, UVT, UVP = os.environ["HC_UVCACHE"], os.environ["HC_UVTOOLS"], os.environ["HC_UVPY"]

PW = "PW=$(grep -ao '8XD[A-Z0-9]*' /pub/test_outputs.py | head -n1)\n"
# recipes taken verbatim from plans/password_recovery_probe.py CASES (lines 117, 125, 133-134)
CASES = {
    "oracle-solve-sh": "bash /pub/solve.sh >/dev/null 2>&1 || true\n",
    "dir-state": "mkdir -p /app/recovered_passwords.txt\n" + PW
                 + "printf '%s\\n' \"$PW\" > /app/recovered_passwords.txt/x\n",
    "constant-crlf": PW + "printf '%s\\r\\n' \"$PW\" > /app/recovered_passwords.txt\n",
}
PUBLIC = ("instruction.md", "test_outputs.py", "solve.sh")

def bwrap(work, argv):
    a = ["/usr/bin/bwrap", "--unshare-net", "--unshare-pid", "--unshare-ipc",
         "--die-with-parent", "--new-session", "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            a += ["--symlink", os.readlink(link), link]
    a += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
          "--ro-bind", str(work / "zeros.bin"), "/dev/urandom",
          "--bind", str(work / "app"), "/app",
          "--ro-bind", str(work / "tests"), "/tests", "--dir", "/pub",
          "--ro-bind", "/home/vgpnk/.local/bin", "/home/vgpnk/.local/bin",
          "--ro-bind", "/home/vgpnk/.local/share/uv/python", "/home/vgpnk/.local/share/uv/python",
          "--bind", UVC, UVC, "--bind", UVT, UVT, "--bind", UVP, UVP]
    for name in PUBLIC:
        a += ["--ro-bind", str(CAP / name), "/pub/" + name]
    a += ["--ro-bind", str(work / "seed.sh"), "/seed.sh",
          "--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
          "--chdir", "/app"]
    return a + argv

ENV = {"PATH": "/home/vgpnk/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
       "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "XDG_CACHE_HOME": UVC, "UV_TOOL_DIR": UVT, "UV_PYTHON_INSTALL_DIR": UVP}

def run(a):
    return subprocess.run(a, env=ENV, capture_output=True, text=True, timeout=1800)

for cid, recipe in CASES.items():
    work = pathlib.Path(tempfile.mkdtemp(prefix="hc-", dir=ROOT))
    (work / "app").mkdir(); (work / "tests").mkdir()
    (work / "zeros.bin").write_bytes(b"\0" * 65536)
    (work / "tests/test_outputs.py").write_bytes((CAP / "test_outputs.py").read_bytes())
    (work / "seed.sh").write_bytes((CAP / "setup.sh").read_bytes())
    (work / "recipe.sh").write_text(recipe)

    # STAGE: bash -euo pipefail the verbatim seed, then the recipe (probe staging semantics)
    for step in ("seed", "recipe"):
        p = run(bwrap(work, ["bash", "-euo", "pipefail", f"/{step}.sh"]))
        print(f"{cid} STAGE {step} rc={p.returncode} stderr={p.stderr.strip()[-200:]!r}")
        if p.returncode:
            print(f"{cid} SETUP-FAIL")
            break
    else:
        # GRADE: test.sh's uvx+pytest command line (ctrf plugin dropped - it only writes a report)
        p = run(bwrap(work, ["uvx", "-p", "3.13", "-w", "pytest==8.4.1",
                             "pytest", "/tests/test_outputs.py", "-rA"]))
        lines = [l for l in p.stdout.splitlines()
                 if l.startswith(("PASSED", "FAILED", "ERROR")) or "passed" in l or "failed" in l]
        print(f"{cid} GRADE pytest-rc={p.returncode} verdict={'pass' if p.returncode == 0 else 'fail'}")
        for l in lines:
            print(f"  {cid} {l.rstrip()}")
        if p.stderr.strip():
            print(f"  {cid} stderr: {p.stderr.strip()[-300:]!r}")

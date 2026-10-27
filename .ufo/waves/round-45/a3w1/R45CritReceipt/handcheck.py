#!/usr/bin/env python3
"""R45CritReceipt handcheck (attempt 3): rebuild 3 probe end states by hand and grade each with the REAL
pytest==8.4.1 under `uvx -p 3.13` - the exact executor tests/test.sh:18-22 runs (ctrf plugin dropped: it only
writes the report file). Independent of plans/password_recovery_probe.py's homemade two-function harness.

Cases chosen to cover all three letter shapes in the landed receipt:
  under-varsea  F-  (oracle solve.sh run from /app/varsea - recipe fidelity + cwd dependence)
  dir-state     PF  (directory at the graded path - the error=IsADirectoryError annotation)
  crlf-line     PP  (universal-newline \r\n -> \n is load-bearing here, unlike constant-crlf where .strip()
                     alone would suffice)

Recipes are pulled BYTE-VERBATIM out of the frozen probe module (imported read-only from the clone), never
retyped. Staging: plain `bash /seed.sh` then `bash /recipe.sh` (the image runs `RUN bash /app/setup.sh`).
uv's tool env is pre-warmed into XDG_CACHE_HOME (bound at the same path) and the managed cpython-3.13 is
bound read-only from ~/.local/share/uv, so `uvx -p 3.13` works under --unshare-net.

usage: handcheck.py <lane> <workdir>   (env: HC_UVCACHE = scratch cache dir, absolute)
"""
import hashlib
import importlib.util
import os
import pathlib
import subprocess
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
CAP = LANE / "corpus/evidence/round45/tb2-password-recovery"
ROOT = pathlib.Path(sys.argv[2]).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
UVC = os.environ["HC_UVCACHE"]

# pull the frozen case table verbatim out of the clone's probe module (registered in sys.modules first:
# py3.14's dataclass decorator looks the module up there)
spec = importlib.util.spec_from_file_location("prp", str(LANE / "plans/password_recovery_probe.py"))
prp = importlib.util.module_from_spec(spec)
sys.modules["prp"] = prp
spec.loader.exec_module(prp)
WANT = ("under-varsea", "dir-state", "crlf-line")
CASES = {c.cid: c.recipe for c in prp.CASES if c.cid in WANT}
assert set(CASES) == set(WANT), CASES.keys()
for cid in WANT:
    print(f"recipe {cid} sha256={hashlib.sha256(CASES[cid].encode()).hexdigest()[:16]}"
          f" bytes={len(CASES[cid])}")

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
          "--ro-bind", "/home/vgpnk/.local/share/uv", "/home/vgpnk/.local/share/uv",
          "--bind", UVC, UVC]
    for name in PUBLIC:
        a += ["--ro-bind", str(CAP / name), "/pub/" + name]
    a += ["--ro-bind", str(work / "seed.sh"), "/seed.sh",
          "--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
          "--chdir", "/app"]
    return a + argv


ENV = {"PATH": "/home/vgpnk/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
       "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "XDG_CACHE_HOME": UVC, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}


def run(a):
    return subprocess.run(a, env=ENV, capture_output=True, text=True, timeout=1800)


EXPECTED = {"under-varsea": ("fail", "F-"), "dir-state": ("fail", "PF"), "crlf-line": ("pass", "PP")}
results = {}
for cid in WANT:
    work = pathlib.Path(tempfile.mkdtemp(prefix="hc-", dir=ROOT))
    (work / "app").mkdir()
    (work / "tests").mkdir()
    (work / "zeros.bin").write_bytes(b"\0" * 65536)
    (work / "tests/test_outputs.py").write_bytes((CAP / "test_outputs.py").read_bytes())
    (work / "seed.sh").write_bytes((CAP / "setup.sh").read_bytes())
    (work / "recipe.sh").write_text(CASES[cid])

    ok = True
    for step in ("seed", "recipe"):
        p = run(bwrap(work, ["bash", f"/{step}.sh"]))
        print(f"{cid} STAGE {step} rc={p.returncode} stderr={p.stderr.strip()[-200:]!r}")
        if p.returncode:
            ok = False
            print(f"{cid} SETUP-FAIL")
            break
    if not ok:
        results[cid] = "setup-fail"
        continue
    # end-state evidence before grading
    p = run(bwrap(work, ["bash", "-c",
                         "stat -c '%F %s %n' /app/recovered_passwords.txt 2>&1; "
                         "stat -c '%F %s %n' /app/varsea/recovered_passwords.txt 2>&1; "
                         "printf 'FILE<<'; od -An -c /app/recovered_passwords.txt 2>/dev/null | head -4; "
                         "printf '>>'"]))
    print(f"{cid} ENDSTATE {p.stdout.strip()!r}")
    for attempt in (1, 2):
        p = run(bwrap(work, ["uvx", "-p", "3.13", "-w", "pytest==8.4.1",
                             "pytest", "/tests/test_outputs.py", "-rA"]))
        lines = [l for l in p.stdout.splitlines()
                 if l.startswith(("PASSED", "FAILED", "ERROR")) or "passed" in l or "failed" in l]
        print(f"{cid} GRADE[{attempt}] pytest-rc={p.returncode} "
              f"verdict={'pass' if p.returncode == 0 else 'fail'}")
        for l in lines:
            print(f"  {cid} {l.rstrip()}")
        if p.stderr.strip():
            print(f"  {cid} stderr: {p.stderr.strip()[-300:]!r}")
        results[cid] = "pass" if p.returncode == 0 else "fail"

print("== handcheck summary ==")
ok = 0
for cid in WANT:
    want, _letters = EXPECTED[cid]
    got = results.get(cid)
    mark = "MATCH" if got == want else "MISMATCH"
    ok += got == want
    print(f"HANDCHECK {cid} receipt_observed={want} my_pytest={got} {mark}")
print(f"handcheck matched={ok}/{len(WANT)}")

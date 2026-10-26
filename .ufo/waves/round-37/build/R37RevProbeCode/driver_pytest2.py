"""R37RevProbeCode: pytest-equivalence, variant 2 — stderr visible, uv-python bound at its absolute path."""
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
spec = importlib.util.spec_from_file_location("probe", LANE + "/plans/git_webserver_probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules["probe"] = probe
spec.loader.exec_module(probe)
cap = pathlib.Path(LANE) / probe.CAP
root = pathlib.Path(sys.argv[1])
VENV = sys.argv[2]
UVPY = sys.argv[3]

PYTEST_HARNESS = r'''
import subprocess
r = subprocess.run(["/work/venv/bin/python", "-m", "pytest", "/tests/test_outputs.py",
                    "-q", "-p", "no:cacheprovider", "--no-header"],
                   capture_output=True, text=True)
print("PYTEST rc=%d" % r.returncode)
for line in r.stdout.splitlines():
    print("PYTEST-OUT " + line)
for line in r.stderr.splitlines()[:8]:
    print("PYTEST-ERR " + line)
'''


def run_case_err(case, script):
    work = pathlib.Path(tempfile.mkdtemp(prefix="cgw-", dir=root))
    try:
        probe.prepare(work, case.tools, case.server, script)
        env = {"PATH": "/work/bin", "HOME": "/work/home", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        argv = probe.sandbox_argv(cap, work)
        uvroot = str(pathlib.Path(UVPY).parent)
        for d in ["/home", "/home/vgpnk", "/home/vgpnk/.local", "/home/vgpnk/.local/share",
                  "/home/vgpnk/.local/share/uv", uvroot]:
            argv += ["--dir", d]
        argv += ["--ro-bind", uvroot, uvroot, "--ro-bind", VENV, "/work/venv"]
        r = subprocess.run(argv + ["/usr/bin/bash", "/work/run.sh"], env=env,
                           capture_output=True, text=True, timeout=180)
        return r.returncode, r.stdout, r.stderr
    finally:
        shutil.rmtree(work, ignore_errors=True)


for cid in sys.argv[4].split(","):
    case = next(c for c in probe.CASES if c.cid == cid)
    rc, out, err = run_case_err(case, PYTEST_HARNESS)
    prc = [l for l in out.splitlines() if l.startswith("PYTEST rc")]
    verdict = "pass" if (prc and prc[0] == "PYTEST rc=0") else "fail"
    print(f"CASE {cid} predicted={case.predicted} pytest_verdict={verdict} {prc[0] if prc else 'NO-RC harness_rc=%d' % rc}")
    for l in out.splitlines():
        if l.startswith(("PYTEST-OUT", "PYTEST-ERR")):
            print("  " + l)
    if not prc:
        print("  STDERR-TAIL: " + err.strip()[-500:].replace("\n", " | "))

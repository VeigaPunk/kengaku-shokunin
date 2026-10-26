"""R42PlanNext control: TB2 feal-differential-cryptanalysis grader (pin 2fd12b88) driven offline in bwrap --unshare-net.
Cases are constructed attack.py files, not agents. Host python/gcc stand in for the image. Not a frozen probe."""
import os, pathlib, shutil, subprocess, sys, tempfile, time, re
TB2 = pathlib.Path(sys.argv[1]); ROOT = pathlib.Path(sys.argv[2]); REPS = int(sys.argv[3]) if len(sys.argv) > 3 else 1
T = TB2 / "feal-differential-cryptanalysis"
HARNESS = '''import sys, time, traceback
sys.path.insert(0, "/tests")
import test_outputs
t0 = time.time()
try:
    test_outputs.test_feal_differential_cryptanalysis_attack()
    print("RESULT PASS %.1fs" % (time.time() - t0))
except BaseException as e:
    print("RESULT FAIL %.1fs %s: %s" % (time.time() - t0, type(e).__name__, str(e)[:120].replace("\\n", " ")))
'''
ORACLE = None
def oracle_attack():
    s = (T / "solution/solve.sh").read_text()
    m = re.search(r"cat <<'EOF' > /app/attack.py\n(.*?)\nEOF\n", s, re.S)
    body = m.group(1)
    # the oracle's own __main__ block imports feal (host demo) - harmless; keep bytes
    return body
CASES = {
    "nop": None,
    "oracle-solve-sh": oracle_attack,
    "cheat-import-get_keys": lambda: "def attack(encrypt_fn):\n    import feal_in_c\n    return feal_in_c.get_keys()[5]\n",
    "cheat-clock-seed": lambda: '''import ctypes, time, sys
sys.path.insert(0, "/app")
def attack(encrypt_fn):
    import feal as F
    libc = ctypes.CDLL("libc.so.6")
    now = int(time.time())
    for dt in range(0, -6, -1):
        libc.srand(now + dt)
        ks = [((libc.rand() & 0xFFFF) * 1234567) & 0xFFFFFFFF for _ in range(6)]
        F.key[:] = ks
        if all(F.encrypt(p) == encrypt_fn(p) for p in (0x0123456789ABCDEF, 0, 0xFFFFFFFFFFFFFFFF)):
            return ks[5]
    return 0
''',
    "slow-oracle-45s": lambda: "import time\n" + oracle_attack() + "\n_orig = attack\ndef attack(e):\n    r = _orig(e)\n    time.sleep(45)\n    return r\n",
    "wrong-key": lambda: "def attack(encrypt_fn):\n    return 0\n",
    "sleep-then-cheat": lambda: "import time\ndef attack(e):\n    time.sleep(35)\n    import feal_in_c\n    return feal_in_c.get_keys()[5]\n",
}
def run(name, rep):
    w = pathlib.Path(tempfile.mkdtemp(prefix="feal-", dir=ROOT))
    (w / "app").mkdir(); (w / "tests").mkdir()
    shutil.copy(T / "environment/feal.py", w / "app/feal.py")
    for f in (T / "tests").iterdir(): shutil.copy(f, w / "tests" / f.name)
    shutil.rmtree(w / "tests/build", ignore_errors=True)
    mk = CASES[name]
    if mk: (w / "app/attack.py").write_text(mk())
    (w / "harness.py").write_text(HARNESS)
    argv = ["/usr/bin/bwrap", "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session", "--ro-bind", "/usr", "/usr"]
    for l in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(l): argv += ["--symlink", os.readlink(l), l]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--bind", str(w / "app"), "/app",
             "--bind", str(w / "tests"), "/tests", "--ro-bind", str(w / "harness.py"), "/harness.py", "--chdir", "/app",
             "/usr/bin/env", "-i", "PATH=/usr/bin:/bin", "HOME=/tmp", "PYTHONDONTWRITEBYTECODE=1", "/usr/bin/python3", "/harness.py"]
    t0 = time.time()
    p = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    last = [l for l in p.stdout.splitlines() if l.startswith("RESULT")] or ["RESULT NONE rc=%s %s" % (p.returncode, p.stderr.strip()[-200:])]
    shutil.rmtree(w, ignore_errors=True)
    return last[-1], time.time() - t0
for name in CASES:
    reps = REPS if name in ("oracle-solve-sh", "cheat-clock-seed") else 1
    for r in range(reps):
        res, el = run(name, r)
        print(f"CASE {name} rep={r+1} {res} wall={el:.1f}s", flush=True)

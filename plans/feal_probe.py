#!/usr/bin/env python3
"""Round-43 C2 probe: the pinned Terminal-Bench 2.0 `feal-differential-cryptanalysis` grader, executed offline.

  python3 plans/feal_probe.py --lane .                run every frozen case, print the receipt
  python3 plans/feal_probe.py --lane . --dry          print the frozen case table only (no sandbox)
  python3 plans/feal_probe.py --lane . --stage-check  build every case's end state in the sandbox and byte-compile
                                                      its /app/attack.py; the grader is never imported

What runs: the captured grader `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88, digest checked before any
case) inside a bubblewrap sandbox per case: private network/pid/ipc namespaces, /usr and /etc read-only, /tmp
private, /app a fresh writable directory seeded as the task Dockerfile seeds it (`COPY feal.py ./`), /tests a
fresh writable directory holding the five captured grader files (`test_outputs.py`, `setup.py`, `feal_module.c`,
`feal.c`, `feal.h`: the grader compiles the `feal_in_c` extension into /tests with `python setup.py build_ext
--inplace`), /cap holding `solve.sh`, cwd /app (Dockerfile `WORKDIR /app`). Per case the probe writes the case's
`/app/attack.py` (or none), the sandbox runs the case recipe under `bash -euo pipefail` (only the oracle case has
one: the task's solve.sh, which writes /app/attack.py), then a harness process imports the grader and calls its one
test function. The verdict is the harness process's exit status, which is what tests/test.sh rewards: pytest exits
0 iff no test fails, and test.sh writes reward 1 iff `$? -eq 0`. The harness exits 0 when the test returns and 1
when it raises (an AssertionError is `F`, any other exception is `F` with its class named); a process that leaves
with status 0 without the harness printing a verdict line is still `P` (tagged `exit=no-verdict-line`), because
pytest would also have exited 0. A recipe that exits non-zero is a probe error (exit 2), never a verdict. The SAME
end state is then graded by a second, fresh harness process without rebuilding it; the CASE line carries
`regrade=same` or `regrade=DIFF:<letter>` (reported, never used for the verdict).

The grader's facts this probe exercises (captured `test_outputs.py`, `feal.c`, `feal_module.c`, `test.sh`): the
test appends `/app` and then `/tests` to `sys.path`, imports the agent's module `attack` and then the reference
extension `feal_in_c` into the SAME interpreter, calls `feal_in_c.create_random_keys()` (C `srand(time(NULL))`
once per process, then six `rand() & 0xFFFF` seeds times 1234567), calls `attack.attack(feal_in_c.encrypt)` and
asserts `feal_in_c.get_keys()[5] == stolen`. Nothing times the call; `feal_in_c.get_keys` is a public function of
a module the agent's code can import.

Cases are constructed attack modules, not agents. Predictions were written before the first recorded run of this
probe and frozen with it; the dry table is the freeze receipt. `R42PlanNext` (round-42 wave 1, raw data
`.ufo/waves/round-42/build/R42PlanNext/feal/feal_run1.txt`) graded nop, the oracle, `cheat-import-get_keys`,
`cheat-clock-seed`, `wrong-key` and two slow shapes on this host before this freeze, with an unfrozen harness that
called the test function in-process; the cases `nop`, `oracle-solve-sh`, `wrong-key`, `cheat-import-get_keys`,
`cheat-clock-seed` and `slow-oracle-45s` re-observe those shapes. The other six were never graded before the
freeze.

Each case names the instruction requirements it violates (`violates=` tags, see TAGS). An empty `violates=` on a
failing case is a grader stricter than the instruction; tags on a passing case name a requirement the grader does
not see. `cheat-clock-seed` depends on the C library's `rand()` sequence (host glibc here; the image is Debian
bookworm glibc), so its verdict is a host fact, flagged `host=libc-rand`.

Limits, stated before the first run: host python3 (3.14) and host gcc stand in for the image's python 3.13 under
`uvx -p 3.13` and Debian gcc (test.sh installs gcc and uv over the network); setuptools is the host's, not
80.9.0; the task image is never pulled; pytest is not run (the harness calls the one test function and maps its
outcome onto pytest's exit status); recipes run as the probing user, not root. Deterministic receipt: no temp
path, timing or host version is printed. Scratch lives under --work (created if absent), else $TMPDIR (tempfile
default), and is removed on exit.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round43/tb2-feal-differential-cryptanalysis"
PINS = {
    "test_outputs.py": "585780e76d98094ad118d096f8c78f2281352dc9826e3687c4de152659631a3d",
    "setup.py": "d1d8f08966670ac8bfc1a9cfa8c16a6915eef2153a44ad6502daec2da83e08aa",
    "feal_module.c": "1ae1c8a31b099b5742b35a3d6b1b70a2509d8d13d79ab74535e038e9a3379363",
    "feal.c": "bd4e9fb31e38073414d8a1930b2e67bc59eaee17e52f58133f781d297073e885",
    "feal.h": "d3ebd83bfbdb86f3543bda72a0693aabe478c6880ef78cb4a8e6c2e5a779759e",
    "feal.py": "23cc077b9dce176a3aa3078681d1c8dff8c1b7959556c9457db57036d2885dfe",
    "solve.sh": "6846dd2877aac95bc0b35a65c3b522403d21491407e02f07b7060ab4071a9620",
    "instruction.md": "b4093780b283e5c9838997769fb7bca090e3f4cbbd2d7cb275ba60cdfd722572",
}
GRADER_FILES = ("test_outputs.py", "setup.py", "feal_module.c", "feal.c", "feal.h")
BWRAP = "/usr/bin/bwrap"
TOOLS = ("/usr/bin/python3", "/usr/bin/python", "/usr/bin/bash", "/usr/bin/gcc")
TESTS = ("test_feal_differential_cryptanalysis_attack",)
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# tag -> the instruction line that states the requirement (instruction.md as captured)
TAGS = {
    "chosen-plaintext": "instruction.md:1",
    "recover-key5": "instruction.md:1",
    "attack-file": "instruction.md:3",
    "return-uint32": "instruction.md:3",
    "time-30s": "instruction.md:3",
}

ORACLE = "bash /cap/solve.sh >/dev/null 2>&1\n"
CHEAT = ("chosen-plaintext",)

IMPORT_GET_KEYS = '''def attack(encrypt_fn):
    import feal_in_c
    return feal_in_c.get_keys()[5]
'''
ALWAYS_EQUAL = '''class Anything:
    def __eq__(self, other):
        return True

    __hash__ = object.__hash__


def attack(encrypt_fn):
    return Anything()
'''
SYSMODULES_SHADOW = '''import sys
import types

_fake = types.ModuleType("feal_in_c")
_fake.create_random_keys = lambda: None
_fake.encrypt = lambda p: 0
_fake.get_keys = lambda: [0, 0, 0, 0, 0, 0]
sys.modules["feal_in_c"] = _fake


def attack(encrypt_fn):
    return 0
'''
PATCH_GET_KEYS = '''def attack(encrypt_fn):
    import feal_in_c
    feal_in_c.get_keys = lambda: [0, 0, 0, 0, 0, 7]
    return 7
'''
EXIT_ZERO = '''import os


def attack(encrypt_fn):
    os._exit(0)
'''
CLOCK_SEED = '''import ctypes
import sys
import time

sys.path.insert(0, "/app")


def attack(encrypt_fn):
    import feal as F
    libc = ctypes.CDLL("libc.so.6")
    now = int(time.time())
    for dt in range(0, -10, -1):
        libc.srand(now + dt)
        ks = [((libc.rand() & 0xFFFF) * 1234567) & 0xFFFFFFFF for _ in range(6)]
        F.key[:] = ks
        if all(F.encrypt(p) == encrypt_fn(p) for p in (0x0123456789ABCDEF, 0, 0xFFFFFFFFFFFFFFFF)):
            return ks[5]
    return 0
'''
WRAP_ORACLE = '''
import importlib.util as _u
_s = _u.spec_from_file_location("oracle_attack", "/app/oracle_attack.py")
_m = _u.module_from_spec(_s)
_s.loader.exec_module(_m)
'''


@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    predicted: str          # one letter per TESTS entry
    violates: tuple
    requirement: str
    attack: str | None = None   # content of /app/attack.py written before the recipe; None = no file
    recipe: str = ""            # bash run inside the sandbox before grading
    host: str = ""              # a host fact the verdict depends on


CASES = [
    Case("nop", "F", ("attack-file", "recover-key5"), "no /app/attack.py (the shipped feal.py only)"),
    Case("oracle-solve-sh", "P", (), "the task's solve.sh writes the reference differential attack", recipe=ORACLE),
    Case("wrong-key", "F", ("recover-key5",), "attack() returns 0", attack="def attack(encrypt_fn):\n    return 0\n"),
    Case("oracle-off-by-one", "F", ("recover-key5",), "the reference attack's result plus one",
         recipe=ORACLE + "mv /app/attack.py /app/oracle_attack.py\n"
         + "cat > /app/attack.py <<'EOF'\n" + WRAP_ORACLE
         + "def attack(encrypt_fn):\n    return (_m.attack(encrypt_fn) + 1) & 0xFFFFFFFF\nEOF\n"),
    Case("return-str", "F", ("return-uint32",), "the reference attack's result returned as a decimal string",
         recipe=ORACLE + "mv /app/attack.py /app/oracle_attack.py\n"
         + "cat > /app/attack.py <<'EOF'\n" + WRAP_ORACLE
         + "def attack(encrypt_fn):\n    return str(_m.attack(encrypt_fn))\nEOF\n"),
    Case("cheat-import-get_keys", "P", CHEAT, "attack() imports the reference module and returns get_keys()[5]",
         attack=IMPORT_GET_KEYS),
    Case("cheat-always-equal", "P", CHEAT + ("recover-key5", "return-uint32"),
         "attack() returns an object whose __eq__ is always True (no key, no int)", attack=ALWAYS_EQUAL),
    Case("cheat-sysmodules-shadow", "P", CHEAT + ("recover-key5",),
         "importing attack installs a fake feal_in_c in sys.modules; attack() returns 0", attack=SYSMODULES_SHADOW),
    Case("cheat-patch-get_keys", "P", CHEAT + ("recover-key5",),
         "attack() rebinds feal_in_c.get_keys to return a constant and returns that constant", attack=PATCH_GET_KEYS),
    Case("cheat-exit-zero", "P", CHEAT + ("recover-key5",),
         "attack() ends the grader process with os._exit(0) before the assert", attack=EXIT_ZERO),
    Case("cheat-clock-seed", "P", CHEAT,
         "attack() replays the C srand(time(NULL)) key schedule through libc and checks it against encrypt_fn",
         attack=CLOCK_SEED, host="libc-rand"),
    Case("slow-oracle-45s", "P", ("time-30s",), "the reference attack followed by a 45 s sleep",
         recipe=ORACLE + "mv /app/attack.py /app/oracle_attack.py\n"
         + "cat > /app/attack.py <<'EOF'\nimport time\n" + WRAP_ORACLE
         + "def attack(encrypt_fn):\n    r = _m.attack(encrypt_fn)\n    time.sleep(45)\n    return r\nEOF\n"),
]

HARNESS_PY = r'''
import contextlib, importlib.util, io, os, subprocess, sys
mode = sys.argv[1]
if mode in ("stage", "recipe"):
    rc = subprocess.run(["bash", "-euo", "pipefail", "/recipe.sh"], cwd="/app", stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
    print("STAGE recipe rc=" + str(rc), flush=True)
    if rc:
        sys.exit(3)
    if mode == "stage":
        import py_compile
        if os.path.exists("/app/attack.py"):
            try:
                py_compile.compile("/app/attack.py", cfile="/tmp/attack.pyc", doraise=True)
                print("STAGE attack compiles=yes", flush=True)
            except py_compile.PyCompileError:
                print("STAGE attack compiles=NO", flush=True)
                sys.exit(4)
        else:
            print("STAGE attack absent", flush=True)
        b = subprocess.run("cd /tests && python setup.py build_ext --inplace", shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        ok = b == 0 and subprocess.run(["python3", "-c", "import sys; sys.path.append('/tests'); "
                                        "import feal_in_c; feal_in_c.get_keys"], cwd="/tmp",
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        print("STAGE extension builds=" + ("yes" if ok else "NO"), flush=True)
        if not ok:
            sys.exit(5)
    sys.exit(0)
spec = importlib.util.spec_from_file_location("tb2_feal_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in %r:
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            getattr(mod, name)()
        sys.stdout.write("TEST " + name + " P\n")
        sys.stdout.flush()
    except AssertionError:
        print("TEST " + name + " F", flush=True)
        sys.exit(1)
    except BaseException as e:
        print("TEST " + name + " F error=" + type(e).__name__, flush=True)
        sys.exit(1)
sys.exit(0)
''' % (TESTS,)


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sandbox_argv(cap, work):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--bind", str(work / "app"), "/app", "--bind", str(work / "tests"), "/tests", "--dir", "/cap",
             "--ro-bind", str(cap / "solve.sh"), "/cap/solve.sh",
             "--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
             "--ro-bind", str(work / "harness.py"), "/harness.py", "--chdir", "/app"]
    return argv


ENV = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
       "PYTHONDONTWRITEBYTECODE": "1"}


def harness(cap, work, mode):
    p = subprocess.run(sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py", mode],
                       env=ENV, capture_output=True, text=True, timeout=1800)
    return p.returncode, p.stdout


def run_case(cap, root, case, mode):
    """mode 'stage' -> (rc, out); mode 'grade' -> (recipe_rc, [(rc, out), (rc, out)])."""
    work = pathlib.Path(tempfile.mkdtemp(prefix="kfp-", dir=root))
    try:
        app, tests = work / "app", work / "tests"
        app.mkdir()
        tests.mkdir()
        shutil.copyfile(cap / "feal.py", app / "feal.py")
        for name in GRADER_FILES:
            shutil.copyfile(cap / name, tests / name)
        if case.attack is not None:
            (app / "attack.py").write_text(case.attack)
        (work / "recipe.sh").write_text(case.recipe or ":\n")
        (work / "harness.py").write_text(HARNESS_PY)
        if mode == "stage":
            return harness(cap, work, "stage")
        rc, out = harness(cap, work, "recipe")
        if rc != 0:
            return rc, out
        return 0, [harness(cap, work, "grade"), harness(cap, work, "grade")]
    finally:
        shutil.rmtree(work, ignore_errors=True)


def letter(rc, out):
    """pytest's exit status decides (tests/test.sh:25); the verdict line only names the failure."""
    line = [l for l in out.splitlines() if l.startswith("TEST ")]
    note = ""
    if line:
        parts = line[-1].split()
        if len(parts) > 3:
            note = parts[3]
    elif rc == 0:
        note = "exit=no-verdict-line"
    else:
        note = f"exit={rc}-no-verdict-line"
    return ("P" if rc == 0 else "F"), note


def overall(letters):
    return "pass" if letters == "P" * len(TESTS) else "fail"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    mx = ap.add_mutually_exclusive_group()
    mx.add_argument("--dry", action="store_true")
    mx.add_argument("--stage-check", action="store_true")
    ap.add_argument("--work", default=None, help="scratch parent, created if absent (default: $TMPDIR)")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    cap = lane / CAP
    ids = [c.cid for c in CASES]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"[a-z0-9_-]+", i) for i in ids) \
            or any(t not in TAGS for c in CASES for t in c.violates) \
            or any(len(c.predicted) != len(TESTS) or set(c.predicted) - {"P", "F"} for c in CASES):
        print("SETUP duplicate or malformed case id, unknown tag or malformed prediction", file=sys.stderr)
        return 2
    if a.dry:
        for t, loc in TAGS.items():
            print(f"TAG {t} {loc}")
        for c in CASES:
            shape = "recipe" if c.recipe else ("absent" if c.attack is None else
                                               f"{c.attack.count(chr(10))}-lines")
            print(f"CASE {c.cid} predicted={overall(c.predicted)} tests={c.predicted}"
                  f" violates={','.join(c.violates)} attack={shape}"
                  f"{' host=' + c.host if c.host else ''} -- {c.requirement}")
        print(f"cases={len(CASES)} predicted_pass={sum(overall(c.predicted) == 'pass' for c in CASES)}"
              f" predicted_fail={sum(overall(c.predicted) == 'fail' for c in CASES)}")
        return 0
    for name, digest in PINS.items():
        if not (cap / name).is_file() or sha256(cap / name) != digest:
            print(f"SETUP capture {name} missing or not at its pinned digest", file=sys.stderr)
            return 2
    for tool in (BWRAP,) + TOOLS:
        if not os.access(tool, os.X_OK):
            print(f"SETUP {tool} is required", file=sys.stderr)
            return 2
    if a.work:
        try:
            pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"SETUP --work {a.work} cannot be created: {e.strerror}", file=sys.stderr)
            return 2
    root = pathlib.Path(tempfile.mkdtemp(prefix="k43-fp-", dir=a.work))
    try:
        if a.stage_check:
            bad = 0
            for c in CASES:
                rc, out = run_case(cap, root, c, "stage")
                stages = " ".join(l.split(" ", 1)[1] for l in out.splitlines() if l.startswith("STAGE "))
                bad += rc != 0
                print(f"STAGECHECK {c.cid} rc={rc} {stages}")
            print(f"stagecheck cases={len(CASES)} failed={bad}")
            return 0 if bad == 0 else 1
        print("# tb2 feal-differential-cryptanalysis grader probe (kengaku round 43) @ terminal-bench-2 2fd12b88")
        for name in sorted(PINS):
            print(f"# capture {name} sha256={PINS[name]}")
        npass = nfail = mism = rediff = 0
        for c in CASES:
            rc, res = run_case(cap, root, c, "grade")
            if rc != 0:
                print(f"SETUP case {c.cid} recipe failed (rc={rc})", file=sys.stderr)
                print(res, file=sys.stderr)
                return 2
            (l1, n1), (l2, _n2) = letter(*res[0]), letter(*res[1])
            obs = overall(l1)
            npass += obs == "pass"
            nfail += obs == "fail"
            match = l1 == c.predicted
            mism += not match
            rediff += l2 != l1
            print(f"CASE {c.cid} predicted={overall(c.predicted)} observed={obs} tests={l1}"
                  f" predicted_tests={c.predicted} match={'yes' if match else 'NO'}"
                  f" regrade={'same' if l2 == l1 else 'DIFF:' + l2}"
                  f" violates={','.join(c.violates)}{' ' + n1 if n1 else ''}"
                  f"{' host=' + c.host if c.host else ''} -- {c.requirement}")
        print(f"regrade cases={len(CASES)} differ={rediff}")
        print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

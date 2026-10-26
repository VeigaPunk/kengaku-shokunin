#!/usr/bin/env python3
"""Round-44 C2 probe: the pinned Terminal-Bench 2.0 `feal-linear-cryptanalysis` grader, executed offline.

  python3 plans/feal_linear_probe.py --lane .                run every frozen case, print the receipt
  python3 plans/feal_linear_probe.py --lane . --dry          print the frozen case table only (no sandbox)
  python3 plans/feal_linear_probe.py --lane . --stage-check  build every case's end state in the sandbox and report
                                                             whether /app/plaintexts.txt exists; never grades

What runs: the captured grader `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88, digest checked before any
case) inside a bubblewrap sandbox per case: private network/pid/ipc namespaces, /usr and /etc read-only, /tmp
private, cwd /app (Dockerfile `WORKDIR /app`). /app is a fresh writable directory seeded the way the task
Dockerfile seeds it (`COPY task-deps/ /app/`, `gcc -O3 -o feal feal.c`, `gcc -O3 -o decrypt decrypt.c`,
`python3 gen.py`, `rm orig_plaintexts.txt`, `rm gen.py`), so the image state the agent starts from is rebuilt
per case. /tests holds the captured `test_outputs.py` only. /pub holds read-only copies of three PUBLIC files at
the pin (`gen.py`, `test_outputs.py`, `solve.sh`): the image deletes gen.py and never ships the tests, but both
are published in the benchmark repository, and a case that reads /pub models an agent that read the public
task source. Per case the sandbox runs the case recipe under `bash -euo pipefail` in /app (the recipe writes
/app/plaintexts.txt or nothing), then a harness process imports the grader and calls its one test function
`test_attack`. The verdict is the harness exit status, which is what tests/test.sh rewards (pytest exits 0 iff no
test fails; test.sh writes reward 1 iff `$? -eq 0`): exit 0 when the test returns, 1 when it raises (an
AssertionError is `F`, any other exception is `F` with its class named). A recipe that exits non-zero is a probe
error (exit 2), never a verdict. The SAME end state is then graded by a second, fresh harness process; the CASE
line carries `regrade=same` or `regrade=DIFF:<letter>` (reported, never used for the verdict).

The grader's facts this probe exercises (captured `test_outputs.py`): 100 decimal constants in a triple-quoted
string (`:4-103`); `test_attack` reads `/app/plaintexts.txt` (`:120`) and asserts `c in data` for each constant
(`:121-122`): a substring test on the whole file text, with no count, order, format or exactness check.

Cases are constructed end states, not agents. Predictions were written before the first recorded run of this
probe and frozen with it; the dry table is the freeze receipt. `R43PlanNext` (round-43 wave 1,
`.ufo/waves/round-43/build/R43PlanNext/feal_linear_run_oracle.sh`) ran the oracle and a substring check (not the
grader's test function) on this host before this freeze: `CONSTANTS 100 ALL_IN_DATA True LINES 928`. No other
case shape was graded before the freeze.

Each case names the instruction requirements it violates (`violates=` tags, see TAGS). An empty `violates=` on a
failing case is a grader stricter than the instruction; tags on a passing case name a requirement the grader does
not see.

Limits, stated before the first run: host python3 and host gcc stand in for the image's python 3.13 under
`uvx -p 3.13` and Debian bookworm gcc; the task image is never pulled; pytest is not run (the harness calls the one
test function and maps its outcome onto pytest's exit status); recipes run as the probing user, not root; the
image's `pip install setuptools==80.9.0` is not replayed (nothing in this task imports it). Deterministic
receipt: no temp path, timing or host version is printed. Scratch lives under --work (created if absent), else
$TMPDIR (tempfile default), and is removed on exit.
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

CAP = "corpus/evidence/round44/tb2-feal-linear-cryptanalysis"
PINS = {
    "test_outputs.py": "f59ebc7218a648582483cee02556c3bc1235e186301376bc3be066ed106ed9f9",
    "feal.c": "bbd38d19f976b27e5a5aff23e21ba5f0164335397928ca05220379552dea08da",
    "decrypt.c": "4c6864e0d3a76626f1a7af1383e6826a85bdd1e7e373215741ece4f50a94ebd2",
    "gen.py": "3a71f0b5d9095440bea31bced5ea4fc8dd4cff0ae4226ea0400a3bfa7c452c63",
    "solve.sh": "be50ae01a3ea850a6dc4bc99dc130d0b7ad37963c85544a02b03a4f5da29cb77",
    "instruction.md": "a2f1669d4067af6c7b8ac05ff7d5849ca5df68397c94701645c4b9a3b6f71b03",
    "Dockerfile": "ef521cded1b5e0e9a11a6aa9c758e4474f2160e641fb9a177a20cdc728bfff1d",
}
TASK_DEPS = ("feal.c", "decrypt.c", "gen.py")
PUBLIC = ("gen.py", "test_outputs.py", "solve.sh")
BWRAP = "/usr/bin/bwrap"
TOOLS = ("/usr/bin/python3", "/usr/bin/bash", "/usr/bin/gcc")
TESTS = ("test_attack",)
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# tag -> the instruction line that states the requirement (instruction.md as captured)
TAGS = {
    "known-plaintext-attack": "instruction.md:7",
    "recover-key": "instruction.md:7",
    "decrypt-all": "instruction.md:8",
    "plaintexts-file": "instruction.md:10",
}
ATTACKLESS = ("known-plaintext-attack", "recover-key")

# Dockerfile:6-11 replayed in /app (COPY already done by the probe).
SEED = ("gcc -O3 -o feal feal.c\ngcc -O3 -o decrypt decrypt.c\npython3 gen.py >/dev/null\n"
        "rm orig_plaintexts.txt\nrm gen.py\n")
# solve.sh as published: writes attack.c, compiles it, runs it into /app/plaintexts.txt.
ORACLE = "bash /pub/solve.sh >/dev/null 2>&1\n"
# The four 20-bit round keys printed in the public gen.py (gen.py:12).
KEYS_FROM_GEN = ("python3 - <<'EOF' > /tmp/keys\nimport re\n"
                 "print(' '.join(re.findall(r'\"(0x[0-9a-f]+)\"', open('/pub/gen.py').read().split('keys = ')[1]"
                 ".split(']')[0])))\nEOF\n")
GEN_REPLAY = '''python3 - <<'EOF' > /app/plaintexts.txt
import hashlib, struct
keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]
src = open("/pub/gen.py").read()
assert 'keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]' in src
seed = hashlib.sha256("".join(keys).encode()).digest()
for i in range(100):
    print(int.from_bytes(hashlib.sha256(seed + struct.pack(">Q", 32 + i)).digest()[:8], "big"))
EOF
'''
COPY_CONSTANTS = '''python3 - <<'EOF' > /app/plaintexts.txt
import re
src = open("/pub/test_outputs.py").read()
print(re.search(r'soln = """(.*?)"""', src, re.S).group(1))
EOF
'''


@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    predicted: str          # one letter per TESTS entry
    violates: tuple
    requirement: str
    recipe: str = ""        # bash run in /app after the image seed, before grading


CASES = [
    Case("nop", "F", ("decrypt-all", "plaintexts-file") + ATTACKLESS, "no /app/plaintexts.txt (the image state only)"),
    Case("oracle-solve-sh", "P", (), "the task's solve.sh: linear attack in C, then ./decrypt with the recovered keys",
         recipe=ORACLE),
    Case("decrypt-public-keys", "P", ATTACKLESS,
         "./decrypt ciphertexts.txt with the four round keys printed in the public gen.py:12 (no attack)",
         recipe=KEYS_FROM_GEN + "./decrypt ciphertexts.txt $(cat /tmp/keys) > /app/plaintexts.txt\n"),
    Case("replay-public-gen", "P", ATTACKLESS + ("decrypt-all",),
         "recompute the 100 plaintexts from the public gen.py hash chain (counters 32-131); no key, no decryption",
         recipe=GEN_REPLAY),
    Case("copy-public-constants", "P", ATTACKLESS + ("decrypt-all",),
         "copy the 100 expected constants out of the public tests/test_outputs.py", recipe=COPY_CONSTANTS),
    Case("oracle-concatenated", "P", (), "the oracle's numbers joined into one line with no separator",
         recipe=ORACLE + "tr -d ' \\n\\t' < /app/plaintexts.txt > /tmp/p && cp /tmp/p /app/plaintexts.txt\n"),
    Case("oracle-plus-decoys", "P", (),
         "the oracle's output followed by 100 decryptions under a wrong key (two answers per ciphertext)",
         recipe=ORACLE + KEYS_FROM_GEN
         + "set -- $(cat /tmp/keys); ./decrypt ciphertexts.txt 0x00001 $2 $3 $4 >> /app/plaintexts.txt\n"),
    Case("oracle-reversed", "P", (), "the oracle's lines in reverse order", recipe=ORACLE
         + "tac /app/plaintexts.txt > /tmp/p && cp /tmp/p /app/plaintexts.txt\n"),
    Case("oracle-zero-padded", "P", (), "the correct plaintexts printed as 20-digit zero-padded decimals",
         recipe=KEYS_FROM_GEN + "./decrypt ciphertexts.txt $(cat /tmp/keys) | python3 -c 'import sys\n"
         "for l in sys.stdin: print(\"%020d\" % int(l))' > /app/plaintexts.txt\n"),
    Case("one-missing", "F", ("decrypt-all",), "the correct 100 plaintexts with the last one dropped",
         recipe=KEYS_FROM_GEN + "./decrypt ciphertexts.txt $(cat /tmp/keys) | head -n 99 > /app/plaintexts.txt\n"),
    Case("hex-output", "F", (), "the correct plaintexts printed in hexadecimal (instruction.md names no format)",
         recipe=KEYS_FROM_GEN + "./decrypt ciphertexts.txt $(cat /tmp/keys) | python3 -c 'import sys\n"
         "for l in sys.stdin: print(hex(int(l)))' > /app/plaintexts.txt\n"),
    Case("wrong-key-decrypt", "F", ("recover-key", "decrypt-all"), "decrypt with round key 0 off by one bit",
         recipe=KEYS_FROM_GEN + "set -- $(cat /tmp/keys); ./decrypt ciphertexts.txt $(printf '0x%x' $(( $1 ^ 1 ))) $2 $3 $4"
         " > /app/plaintexts.txt\n"),
    Case("pairs-plaintexts", "F", ("decrypt-all",) + ATTACKLESS, "the 32 known plaintexts from pairs.txt",
         recipe="cut -d' ' -f1 pairs.txt > /app/plaintexts.txt\n"),
    Case("ciphertexts-copied", "F", ("decrypt-all",) + ATTACKLESS, "ciphertexts.txt copied unchanged",
         recipe="cp ciphertexts.txt /app/plaintexts.txt\n"),
]

HARNESS_PY = r'''
import contextlib, importlib.util, io, os, subprocess, sys
mode = sys.argv[1]
if mode in ("stage", "recipe"):
    for step, script in (("seed", "/seed.sh"), ("recipe", "/recipe.sh")):
        rc = subprocess.run(["bash", "-euo", "pipefail", script], cwd="/app", stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        print("STAGE " + step + " rc=" + str(rc), flush=True)
        if rc:
            sys.exit(3)
    if mode == "stage":
        p = "/app/plaintexts.txt"
        print("STAGE plaintexts " + (("bytes=" + str(os.path.getsize(p))) if os.path.exists(p) else "absent"),
              flush=True)
    sys.exit(0)
spec = importlib.util.spec_from_file_location("tb2_feal_linear_grader", "/tests/test_outputs.py")
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
             "--bind", str(work / "app"), "/app", "--ro-bind", str(work / "tests"), "/tests", "--dir", "/pub"]
    for name in PUBLIC:
        argv += ["--ro-bind", str(cap / name), "/pub/" + name]
    argv += ["--ro-bind", str(work / "seed.sh"), "/seed.sh", "--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
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
    work = pathlib.Path(tempfile.mkdtemp(prefix="kflp-", dir=root))
    try:
        app, tests = work / "app", work / "tests"
        app.mkdir()
        tests.mkdir()
        for name in TASK_DEPS:
            shutil.copyfile(cap / name, app / name)
        shutil.copyfile(cap / "test_outputs.py", tests / "test_outputs.py")
        (work / "seed.sh").write_text(SEED)
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
            shape = "recipe" if c.recipe else "absent"
            print(f"CASE {c.cid} predicted={overall(c.predicted)} tests={c.predicted}"
                  f" violates={','.join(c.violates)} end={shape} -- {c.requirement}")
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
    root = pathlib.Path(tempfile.mkdtemp(prefix="k44-flp-", dir=a.work))
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
        print("# tb2 feal-linear-cryptanalysis grader probe (kengaku round 44) @ terminal-bench-2 2fd12b88")
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
                  f" violates={','.join(c.violates)}{' ' + n1 if n1 else ''} -- {c.requirement}")
        print(f"regrade cases={len(CASES)} differ={rediff}")
        print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

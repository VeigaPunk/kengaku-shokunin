#!/usr/bin/env python3
"""Round-42 C2 probe: the pinned Terminal-Bench 2.0 `circuit-fibsqrt` grader, executed offline.

  python3 plans/fibsqrt_probe.py --lane .                run every frozen case, print the receipt
  python3 plans/fibsqrt_probe.py --lane . --dry          print the frozen case table only (no sandbox)
  python3 plans/fibsqrt_probe.py --lane . --stage-check  build every case's end state in the sandbox and print
                                                         only the stage exit codes; the grader is never imported

What runs: the captured grader `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88, digest checked before any
case) inside a bubblewrap sandbox per case: private network/pid/ipc namespaces, /usr and /etc read-only, /tmp
private, /app a fresh writable directory, /tests holding only `test_outputs.py` and `sim.c` (the grader
compiles `/tests/sim.c`), /cap holding `solve.sh`, cwd /app (the task Dockerfile's `WORKDIR /app`; tests/test.sh
refuses to run from `/`). Per case the probe seeds /app as the Dockerfile does (`COPY tests/sim.c /app`, `COPY
gates.txt /app`: the captured example circuit), then applies the case's host-side end state (a replacement
`gates.txt`, its removal, a directory in its place, or an extra executable `/app/sim`), the sandbox runs the case
recipe under `bash -euo pipefail` (only the oracle case has one: the task's solve.sh), then imports the grader
and calls its three test functions in file order: an AssertionError is `F`, any other exception is `F` with its
class named, a return is `P`. A case's verdict is `pass` iff all three are `P` (pytest exits 0 iff no test fails;
tests/test.sh writes reward 1 iff pytest exits 0). A recipe that exits non-zero is a probe error (exit 2), never a
verdict. After the first grading the harness grades the SAME end state again without rebuilding it; the CASE
line carries `regrade=same` or `regrade=DIFF:<letters>` (reported, never used for the verdict).

The grader's facts this probe exercises (captured `test_outputs.py`, `sim.c`): test 1 checks `/app/gates.txt`
exists; test 2 counts every line of it (`< 32000`); test 3 compiles `/tests/sim.c` to `./sim` in the cwd and runs
`/app/sim N` for 28 fixed N (`1,4,8,12,41,42,107,220,209,366` and `x*x`, `x*x-1`, `x*x+1` for x in
`12,41,42,107,220,209`; the largest is 48401), comparing stdout with `fib(isqrt(N)) % 2**32`. `sim.c` reads
`gates.txt` relative to its cwd, skips every line that does not scan as `out%d = <op>`, sets signals 0-31 from
argv[1] (not stdin), and prints the 32 HIGHEST-INDEXED signals, not the file's last 32 lines.

Lookup circuits (built by this probe, deterministic): `lookup(values)` holds the 32 input signals, negates them,
builds one 32-input AND equality chain per value and one OR tree per output bit over the values whose answer has
that bit set; it equals the answer on exactly the listed values and prints 0 on every other input.

Predictions: written before the first recorded run of this probe and frozen with it; the dry table is the
freeze receipt. `R41PlanNext` (round-41 wave 1) graded three shapes on this host before this freeze (nop 2/3
tests, oracle 3/3, a 28-value lookup 3/3): the cases `nop`, `oracle-solve-sh` and `lookup-28` re-observe them;
every other case was never graded before the freeze.

Each case names the instruction requirements it violates (`violates=` tags, see TAGS). An empty `violates=` on
a failing case is a grader stricter than the instruction; tags on a passing case name a requirement the grader
does not see.

Limits, stated before the first run: host python3 and host gcc stand in for the image's Debian bookworm
python 3.13 and gcc (test.sh runs pytest under `uvx -p 3.13`, which needs the network); the task image is never
pulled; recipes run as the probing user, not root. This probes the grader on constructed end states, not any
agent. Deterministic receipt: no temp path, timing or host version is printed. Scratch lives under --work
(created if absent), else $TMPDIR (tempfile default), and is removed on exit.
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

CAP = "corpus/evidence/round42/tb2-circuit-fibsqrt"
PINS = {
    "test_outputs.py": "6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438",
    "sim.c": "700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173",
    "gates.txt": "032786f94f16605767c62bb61ce4dbba7ab7d3f1046712c975f01c9a04b6ad29",
    "solve.sh": "a4ffab4183815a0eb7646abc1de1fc67695014c060d7ff16e8bca9ec94385d0b",
    "instruction.md": "a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea",
}
BWRAP = "/usr/bin/bwrap"
TOOLS = ("/usr/bin/python3", "/usr/bin/bash", "/usr/bin/gcc")
TESTS = ("test_gates_file_exists", "test_gates_file_size", "test_sqrt_fib")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# tag -> the instruction line that states the requirement (instruction.md as captured)
TAGS = {
    "line-form": "instruction.md:1",
    "last-32-lines": "instruction.md:9",
    "gates-file": "instruction.md:11",
    "line-limit": "instruction.md:11",
    "output-function": "instruction.md:11",
    "example-208": "instruction.md:12",
    "example-20000": "instruction.md:13",
}

GRADED = [1, 4, 8, 12, 41, 42, 107, 220, 209, 366]
for _x in (12, 41, 42, 107, 220, 209):
    GRADED += [_x * _x]
for _x in (12, 41, 42, 107, 220, 209):
    GRADED += [_x * _x - 1]
for _x in (12, 41, 42, 107, 220, 209):
    GRADED += [_x * _x + 1]


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def answer(n):
    import math
    return fib(math.isqrt(n)) % (2 ** 32)


def lookup(values, flip=None):
    """Gate lines (no trailing newline) equal to the answer on `values`; flip=(value, bit) corrupts one bit."""
    lines = []

    def new(expr):
        lines.append(f"out{len(lines)} = {expr}")
        return len(lines) - 1

    for i in range(32):
        new(f"out{i}")
    neg = [new(f"~out{i}") for i in range(32)]
    eqs = []
    for v in sorted(set(values)):
        lit = [i if (v >> i) & 1 else neg[i] for i in range(32)]
        acc = lit[0]
        for x in lit[1:]:
            acc = new(f"out{acc} & out{x}")
        eqs.append((v, acc))
    outs = []
    for j in range(32):
        sel = [acc for v, acc in eqs if ((answer(v) ^ (1 << flip[1] if flip and flip[0] == v else 0)) >> j) & 1]
        if not sel:
            outs.append(new("0"))
            continue
        acc = sel[0]
        for s in sel[1:]:
            acc = new(f"out{acc} | out{s}")
        outs.append(acc)
    for j in range(32):
        new(f"out{outs[j]}")
    return lines


def text(lines, eol="\n"):
    return eol.join(lines) + eol


L28 = lookup(GRADED)
L27 = lookup([v for v in GRADED if v != 48401])
L30 = lookup(GRADED + [208, 20000])
FAKE_SIM = ("#!/bin/sh\nexec /usr/bin/python3 -c 'import math,sys\n"
            "n=math.isqrt(int(sys.argv[1]));a,b=0,1\nfor _ in range(n): a,b=b,a+b\nprint(a%2**32)' \"$1\"\n")


@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    predicted: str          # letters for TESTS in file order
    violates: tuple
    requirement: str
    gates: str | None = ""   # "" keep the seeded example; None remove; "<dir>" a directory; "<empty>" empty; else content
    sim: str | None = None   # content of an executable /app/sim written before grading
    recipe: str = ""         # bash run inside the sandbox before grading


EX = ("output-function", "example-208", "example-20000")
ORACLE = "bash /cap/solve.sh >/dev/null 2>&1\n"
CASES = [
    Case("nop", "PPF", EX, "the shipped example circuit (prints N/2) left in place"),
    Case("oracle-solve-sh", "PPP", (), "the task's solve.sh generates the reference circuit", recipe=ORACLE),
    Case("no-gates-file", "FFF", ("gates-file",) + EX, "/app/gates.txt removed", gates=None),
    Case("empty-gates-file", "PPF", EX, "an empty /app/gates.txt (sim prints nothing)", gates="<empty>"),
    Case("lookup-28", "PPP", EX, "a lookup circuit for exactly the 28 graded inputs (0 elsewhere)",
         gates=text(L28)),
    Case("lookup-27-drop-48401", "PPF", EX, "the lookup circuit without the largest graded input 48401",
         gates=text(L27)),
    Case("lookup-28-plus-examples", "PPP", ("output-function",),
         "the lookup circuit plus the instruction's two examples 208 and 20000", gates=text(L30)),
    Case("lookup-28-bitflip-41", "PPF", EX, "the lookup circuit with bit 0 of the answer for N=41 flipped",
         gates=text(lookup(GRADED, flip=(41, 0)))),
    Case("lookup-28-padded-31999", "PPP", EX, "the lookup circuit padded with blank lines to 31999 lines",
         gates=text(L28 + [""] * (31999 - len(L28)))),
    Case("lookup-28-padded-32000", "PFP", ("line-limit",) + EX,
         "the lookup circuit padded with blank lines to 32000 lines (sim ignores blanks; the size test counts them)",
         gates=text(L28 + [""] * (32000 - len(L28)))),
    Case("lookup-28-comment-lines", "PPP", ("line-form",) + EX,
         "every gate line of the lookup circuit preceded by a `# note` line",
         gates=text([y for x in L28 for y in ("# note", x)])),
    Case("lookup-28-reversed-lines", "PPP", ("last-32-lines",) + EX,
         "the lookup circuit's lines in reverse order: the file's last 32 lines are the input copies",
         gates=text(list(reversed(L28)))),
    Case("lookup-28-crlf", "PPP", EX, "the lookup circuit with CRLF line ends", gates=text(L28, "\r\n")),
    Case("lookup-28-trailing-space", "PPF", EX,
         "every line of the lookup circuit ends in one space (copy lines no longer scan as copies)",
         gates=text([x + " " for x in L28])),
    Case("fake-sim-script", "PPF", EX,
         "the shipped example circuit plus an executable /app/sim script printing the right answers",
         sim=FAKE_SIM),
    Case("gates-is-directory", "PFF", ("gates-file",) + EX, "/app/gates.txt is a directory", gates="<dir>"),
]

HARNESS_PY = r'''
import importlib.util, subprocess, sys
mode = sys.argv[1]
rc = subprocess.run(["bash", "-euo", "pipefail", "/recipe.sh"], cwd="/app", stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
print("STAGE recipe rc=" + str(rc))
if rc or mode == "stage":
    sys.exit(3 if rc else 0)
spec = importlib.util.spec_from_file_location("tb2_fibsqrt_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
import contextlib, io
for tag in ("TEST", "REGRADE"):
    for name in %r:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                getattr(mod, name)()
            print(tag + " " + name + " P")
        except AssertionError:
            print(tag + " " + name + " F")
        except Exception as e:
            print(tag + " " + name + " F error=" + type(e).__name__)
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
             "--bind", str(work / "app"), "/app", "--dir", "/tests", "--dir", "/cap"]
    for name in ("test_outputs.py", "sim.c"):
        argv += ["--ro-bind", str(cap / name), f"/tests/{name}"]
    argv += ["--ro-bind", str(cap / "solve.sh"), "/cap/solve.sh",
             "--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
             "--ro-bind", str(work / "harness.py"), "/harness.py", "--chdir", "/app"]
    return argv


def run_case(cap, root, case, mode):
    work = pathlib.Path(tempfile.mkdtemp(prefix="fsp-", dir=root))
    try:
        app = work / "app"
        app.mkdir()
        shutil.copyfile(cap / "sim.c", app / "sim.c")
        shutil.copyfile(cap / "gates.txt", app / "gates.txt")
        if case.gates is None:
            (app / "gates.txt").unlink()
        elif case.gates == "<dir>":
            (app / "gates.txt").unlink()
            (app / "gates.txt").mkdir()
        elif case.gates == "<empty>":
            (app / "gates.txt").write_bytes(b"")
        elif case.gates:
            (app / "gates.txt").write_bytes(case.gates.encode())
        if case.sim is not None:
            (app / "sim").write_text(case.sim)
            (app / "sim").chmod(0o755)
        (work / "recipe.sh").write_text(case.recipe or ":\n")
        (work / "harness.py").write_text(HARNESS_PY)
        env = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
               "PYTHONDONTWRITEBYTECODE": "1"}
        p = subprocess.run(sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py", mode],
                           env=env, capture_output=True, text=True, timeout=1800)
        return p.returncode, p.stdout
    finally:
        shutil.rmtree(work, ignore_errors=True)


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
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"[a-z0-9-]+", i) for i in ids) \
            or any(t not in TAGS for c in CASES for t in c.violates) \
            or any(len(c.predicted) != len(TESTS) or set(c.predicted) - {"P", "F"} for c in CASES) \
            or len(GRADED) != 28:
        print("SETUP duplicate or malformed case id, unknown tag, malformed prediction or graded list", file=sys.stderr)
        return 2
    if a.dry:
        for t, loc in TAGS.items():
            print(f"TAG {t} {loc}")
        for c in CASES:
            lines = ("removed" if c.gates is None else "seeded" if c.gates == "" else c.gates
                     if c.gates.startswith("<") else c.gates.count("\n"))
            print(f"CASE {c.cid} predicted={overall(c.predicted)} tests={c.predicted}"
                  f" violates={','.join(c.violates)} gates_lines={lines} -- {c.requirement}")
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
    root = pathlib.Path(tempfile.mkdtemp(prefix="k42-fsp-", dir=a.work))
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
        print("# tb2 circuit-fibsqrt grader probe (kengaku round 42) @ terminal-bench-2 2fd12b88")
        for name in sorted(PINS):
            print(f"# capture {name} sha256={PINS[name]}")
        npass = nfail = mism = rediff = 0
        for c in CASES:
            rc, out = run_case(cap, root, c, "grade")
            got, again = {}, {}
            for l in out.splitlines():
                parts = l.split()
                if len(parts) >= 3 and parts[0] in ("TEST", "REGRADE") and parts[1] in TESTS:
                    (got if parts[0] == "TEST" else again)[parts[1]] = (parts[2], parts[3] if len(parts) > 3 else "")
            if rc != 0 or set(got) != set(TESTS) or set(again) != set(TESTS):
                print(f"SETUP case {c.cid} did not yield three test verdicts twice (rc={rc})", file=sys.stderr)
                print(out, file=sys.stderr)
                return 2
            letters = "".join(got[t][0] for t in TESTS)
            letters2 = "".join(again[t][0] for t in TESTS)
            errs = ",".join(f"{t}:{got[t][1]}" for t in TESTS if got[t][1])
            obs = overall(letters)
            npass += obs == "pass"
            nfail += obs == "fail"
            match = letters == c.predicted
            mism += not match
            rediff += letters2 != letters
            print(f"CASE {c.cid} predicted={overall(c.predicted)} observed={obs} tests={letters}"
                  f" predicted_tests={c.predicted} match={'yes' if match else 'NO'}"
                  f" regrade={'same' if letters2 == letters else 'DIFF:' + letters2}"
                  f" violates={','.join(c.violates)}{' ' + errs if errs else ''} -- {c.requirement}")
        print(f"regrade cases={len(CASES)} differ={rediff}")
        print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

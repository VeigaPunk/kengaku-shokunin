#!/usr/bin/env python3
"""Round-46 C3 probe: the pinned Terminal-Bench 2.0 `polyglot-c-py` grader, executed offline.

  python3 plans/polyglot_c_py_probe.py --lane .                run every frozen case, print the receipt
  python3 plans/polyglot_c_py_probe.py --lane . --dry          print the frozen case table only (no sandbox)
  python3 plans/polyglot_c_py_probe.py --lane . --stage-check  build every case's end state in the sandbox and
                                                               report its shape plus a parse-only check of the two
                                                               languages; never imports or calls the grader

ORDER RULE (qualifying claim C3, QUALITY Q30). Before the stage-2 freeze only `--dry` and `--stage-check` are run:
stage-check builds end states and parses them, it does not import `test_outputs.py`, does not call
`test_fibonacci_polyglot`, and does not compile-and-run the candidate file. The first recorded full run follows the
stage-2 commit and its receipt is `corpus/evidence/round46/polyglot-c-py-probe.txt`. The predictions in CASES were
written from the captured grader text before any case of this table ran; the `--dry` output is the freeze receipt.
Disclosed prior grading, carried from the claims file: round-45 seat `w1/R45PlanNext.md` §2 ran this grader twice on
the host (the published oracle, then an extra-file re-grade) while ranking coverage candidates. That is not a case
table; no case below has run.

Round-49 v2 repairs (the two grade-path defects measured in round 48, seat `w1/R48C2ExecProbe.md` §3; every other
bound below is carried over unchanged):
(a) the grade path now runs the image seed and the case recipe. Mode `all` fell outside the harness guard
`mode in ("stage", "recipe")`, so each graded end state was an empty /app: measured `mode=all grader sees
/app/polyglot: exists=False`, all seven predicted passes flipping to fail. The guard now covers `all`, the seed and
recipe still exit 3 (a setup error, surfaced as `SETUP case … sandbox failed (rc=3)`) before any grading, and the
`STAGE` lines stay on stdout as the receipt's own evidence that both steps ran.
(b) the `prlimit --nproc` ceiling is measured per run instead of frozen at 48. `RLIMIT_NPROC` is compared against
every thread of the real uid host-wide, not against the sandbox's own processes, so 48 refused to create the
namespace under a wave-loaded host (`bwrap: Creating new namespace failed: Resource temporarily unavailable`;
measured uid 1000 at 1106-1146 threads in round 48, 3076 in round 49). The ceiling is now the uid's live thread
count plus `NPROC_HEADROOM` spare slots (with `NPROC_FALLBACK` when /proc is unreadable), so the *fork budget* stays
bounded at the headroom while the value tracks host load; one retry at double headroom covers a thread count that
grows between the measurement and the fork.

What runs: the captured grader `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88, digest checked before any
case) inside ONE bubblewrap sandbox per case: an unshared user/pid/ipc/net/uts/cgroup set, a fixed hostname, a
cleared environment passed on the argv, /usr and /etc read-only, `/` remounted read-only last, a 32 MiB /tmp and a
64 MiB /app tmpfs, cwd /app, and `prlimit --nproc=<uid threads + NPROC_HEADROOM> --cpu=5 --fsize=1M --core=0
--as=512M --nofile=512` around the sandbox (see the v2 repair (b) below: the ceiling tracks the uid's live thread
count, the HEADROOM is the recipe's fork budget), so a recipe cannot fork, spin, fill a file or allocate without
bound; sandbox stdout is read through a 1 MiB cap and the sandbox is killed at 60 s. Those are sandbox-side bounds
only: the captured grader still runs its own subprocesses with `capture_output=True` and no timeout (`:30-42`). /app
is a fresh empty tmpfs: the task image has `WORKDIR /app` and `apt install gcc`
(`environment/Dockerfile` at the pin) and creates nothing else, so no `/app/polyglot` exists at the start - `nop`
is that state. /tests holds the captured test_outputs.py only. /pub holds read-only copies of three PUBLIC files at
the pin (instruction.md, test_outputs.py, solve.sh) standing in for what an agent could see; /tpl holds the
polyglot skeleton this probe's recipes instantiate, so no expected value is written into this file. Each case runs
a recipe that writes (or does not write) `/app/polyglot/main.py.c`, and the one captured test function then runs
against that end state in a pytest-free harness; its exit status is the verdict (pytest is not invoked; `tests/test.sh`
only wraps pytest and writes the reward file, so the verdict is the same). Tests are one function, so a case's
letters are one character: `P` when it returns, `F` when it raises (`AssertionError` from the three asserts or from
`os.listdir`'s precondition, `CalledProcessError` from `check=True` on gcc or on either runtime, `FileNotFoundError`
when `/app/polyglot` does not exist). The SAME end state is then graded again by a second leg inside that same
sandbox, with a freshly imported grader module over the same /app tmpfs: the CASE line carries `regrade=same` or
`regrade=DIFF:<letters>` (reported, never used for the verdict).

The grader's facts this probe exercises (captured `test_outputs.py:16-46`): `os.listdir("/app/polyglot")` must equal
`["main.py.c"]` exactly (`:17-20`) - a list compare, so any second entry fails and the order of a single entry is
irrelevant; `gcc /app/polyglot/main.py.c -o /app/polyglot/cmain` runs with `check=True` (`:23-25`), which WRITES a
second file into the directory the listing just checked; then for `(42, "267914296"), (10, "55"), (0, "0")` (`:27`)
both `python3 main.py.c N` and `./cmain N` run with `check=True` and their `stdout.strip()` (`:36`, `:43`) must equal
the expected value (`:29-46`). No other N is graded, the source is never inspected, no timing or file-size bound applies. Two
consequences the table makes explicit: (a) the grader is not idempotent - grading one end state twice fails the
second time on the listing the first grade's own gcc broke (the `regrade` column, and the `leftover-cmain` case,
which is exactly the state instruction.md:5 tells the agent to produce); (b) `.strip()` erases leading/trailing
whitespace on both sides but not extra lines.

Each case names the instruction requirements it violates (`violates=` tags, see TAGS). An empty `violates=` on a
failing case is a grader stricter than the instruction; tags on a passing case name a requirement the grader does
not see (a lookup table satisfies the graded fixed points without computing Fibonacci).

Limits, stated before the first run: host gcc and host python3 stand in for the image's gcc 13.2.0 / python 3.12.3
(named divergence: this host runs a newer gcc, which warns where the image's would; warnings do not decide the
verdict); the task image is never pulled and its `apt install gcc` is not replayed (the sandbox binds host /usr; gcc
and python3 are checked before any case); pytest is not run; recipes run as the probing user, not root; no network;
`tests/test.sh`'s uv/pytest bootstrap is not replayed. `--stage-check`'s `pycheck` is `compile()` of the file text
(parse only, nothing executed) and `ccheck` is `gcc -fsyntax-only` (parse only, no link, no run) - so `empty-file`'s
link failure and every run-time outcome stay predictions read off the source, not observations.

Three consequences of the one-sandbox design, measured and disclosed rather than implied:
(a) phases share a namespace. seed.sh, recipe.sh and both grade legs run in the same pid namespace, so an orphan a
recipe leaves behind is still alive at grading (bounded by the measured `--nproc` ceiling and `--die-with-parent`;
every recipe here is frozen text, so exposure is small - a future per-case agent-authored recipe would need a pid
namespace per phase).
(b) one 60 s budget covers all four phases: if leg 1 is killed, leg 2 never runs and the receipt's `regrade=` shows
`DIFF:-` (a `-` letter from `letters()`), which counts as a mismatch rather than as a verdict.
(c) the fd-1 redirect does not bound the payload: the grader's own `capture_output=True` pipe (`:30-42`, frozen) still
holds the payload's bytes in the sandbox python, so a megabyte emitter meets `--as=536870912` as a `MemoryError`
inside the harness - no verdict line, so the CASE line says `exit=...-no-verdict-line`. That is the chosen trade: the
host cannot be pressured, the verdict becomes ambiguous. The host-pressure limit became a measurement, not a claim.

Deterministic receipt: no temp path, timing or host version is printed. Scratch lives under --work (created if
absent), else $TMPDIR (tempfile default), and is removed on exit; the host side of a case is four small scripts -
/app and /tmp are the sandbox's own tmpfs, so no case writes into the host tree.
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
import threading

CAP = "corpus/evidence/round46/tb2-polyglot-c-py"
PINS = {
    "test_outputs.py": "b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec",
    "instruction.md": "a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96",
    "solve.sh": "e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0",
    "README.md": "591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881",
    "test.sh": "4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334",
    "Dockerfile": "2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a",
    "task.toml": "d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea",
}
PUBLIC = {"instruction.md": "instruction.md", "test_outputs.py": "test_outputs.py",
          "solve.sh": "solve.sh"}
BWRAP = "/usr/bin/bwrap"
PRLIMIT = "/usr/bin/prlimit"
# prlimit takes bare byte counts, not M/K suffixes (measured: --fsize=1M -> "failed to parse FSIZE limit")
LIMITS = ("--cpu=5", "--fsize=1048576", "--core=0", "--as=536870912", "--nofile=512")
# NPROC is built per run, not frozen here: RLIMIT_NPROC is compared against every thread of the real uid host-wide,
# so a small absolute ceiling cannot create a namespace at all on a wave-loaded host (measured: uid 1000 at
# 1106-1146 threads in round 48, 3076 in round 49 -> "bwrap: Creating new namespace failed"). What is bounded is the
# spare budget a recipe may fork into, so the ceiling is the live uid thread count plus this headroom.
NPROC_HEADROOM = 256
NPROC_FALLBACK = 8192    # /proc unreadable: above every observed uid thread count, still a bounded header
TOOLS = ("/usr/bin/python3", "/usr/bin/bash", "/usr/bin/gcc", "/usr/bin/prlimit")
TESTS = ("test_fibonacci_polyglot",)
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
CAP_BYTES = 1 << 20      # sandbox stdout kept; the reader keeps draining so a chatty payload cannot deadlock
TIMEOUT = 60             # wall clock per sandbox invocation, then the sandbox is killed
SBOX_ENV = (("PATH", PATH), ("HOME", "/tmp"), ("TMPDIR", "/tmp"), ("LANG", "C.UTF-8"),
            ("LC_ALL", "C.UTF-8"), ("PYTHONUTF8", "1"), ("PYTHONDONTWRITEBYTECODE", "1"))

# tag -> the instruction.md line that states the requirement (instruction.md as captured)
TAGS = {
    "single-file": "instruction.md:1",    # a single file in /app/polyglot/main.py.c
    "python-run": "instruction.md:3",     # `python3 /app/polyglot/main.py.c N`
    "c-build": "instruction.md:5",        # `gcc ... -o /app/polyglot/cmain && /app/polyglot/cmain N`
    "both-print": "instruction.md:7",     # both of these should print to stdout ...
    "fib-kth": "instruction.md:7",        # the kth Fibonacci number, f(0) = 0, f(1) = 1, etc.
    "stdout-only": "instruction.md:7",    # print to stdout (stderr is never read by the grader)
    "toolchain": "instruction.md:9",      # python3 3.12.3 and gcc 13.2.0
}
DIRP = "/app/polyglot"
SRC = "/app/polyglot/main.py.c"

# The polyglot skeleton, bound read-only at /tpl/polyglot-template.txt: the C comment opened on line 1 and closed
# after the Python block makes the Python source a C comment and the C source a Python string, the same overlap the
# published solution/solve.sh uses. Placeholders: @@WARN@@ (a line that is a C directive and a Python comment),
# @@NPARSE@@ (how the C side reads N), @@LOOP@@ (the C Fibonacci loop), @@PY@@, @@C@@, @@RET@@.
TEMPLATE = r'''@@WARN@@#define pgopen b /*
import sys

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

_k = int(sys.argv[1])
@@PY@@
"""
#define pgclose b */
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    unsigned long long a = 0, b = 1, t;
@@NPARSE@@
@@LOOP@@
@@C@@
    return @@RET@@;
}
#define pgtail """
'''

NPARSE_OK = "    unsigned int n = (unsigned int)strtoul(argv[1], NULL, 10);"
LOOP_OK = "    for (unsigned int i = 0; i < n; ++i) { t = a + b; a = b; b = t; }"


def poly(*, warn="", py='print(fib(_k))', c='    printf("%llu\\n", a);', nparse=NPARSE_OK,
         loop=LOOP_OK, ret="0"):
    return (TEMPLATE.replace("@@WARN@@", warn).replace("@@NPARSE@@", nparse).replace("@@LOOP@@", loop)
            .replace("@@PY@@", py).replace("@@C@@", c).replace("@@RET@@", ret))


def emit(text):
    """bash that creates /app/polyglot/main.py.c with exactly this text."""
    return ("mkdir -p " + DIRP + "\ncat > " + SRC + " <<'POLYGLOT_EOF'\n" + text + "POLYGLOT_EOF\n")


ORACLE = "bash /pub/solve.sh >/dev/null 2>&1\n"

# the leak channel these cases exercise: the three graded values are read out of the PUBLIC grader copy inside the
# sandbox and turned into a print table - no expected value is written into this probe
LOOKUP = r'''mkdir -p /app/polyglot
python3 - <<'TABLE_EOF'
import ast, pathlib
src = pathlib.Path("/pub/test_outputs.py").read_text()
cases = None
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "test_cases":
        cases = ast.literal_eval(node.value)
if not cases:
    raise SystemExit("no test_cases literal in the public grader")
py = ("TABLE = {%s}\nprint(TABLE[int(sys.argv[1])])"
      % ", ".join("%d: %r" % (int(n), v) for n, v in cases))
cw = "\n".join('        case %d: puts("%s"); break;' % (int(n), v) for n, v in cases)
c = "    switch (strtoul(argv[1], NULL, 10)) {\n" + cw + "\n        default: return 1;\n    }"
tpl = pathlib.Path("/tpl/polyglot-template.txt").read_text()
pathlib.Path("/app/polyglot/main.py.c").write_text(
    tpl.replace("@@WARN@@", "").replace("@@NPARSE@@", "").replace("@@LOOP@@", "")
       .replace("@@PY@@", py).replace("@@C@@", c).replace("@@RET@@", "0"))
TABLE_EOF
'''

@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    predicted: str          # one letter per TESTS entry: P pass, F fail
    regrade: str            # the same end state graded a second time
    violates: tuple
    requirement: str
    recipe: str = ""        # bash run in /app after the image seed, before grading
    expect: str = "src"     # what the end state must look like to --stage-check: src | dir | absent


CASES = [
    Case("nop", "F", "F", ("single-file",),
         "the image seed only: WORKDIR /app exists, /app/polyglot does not - os.listdir raises FileNotFoundError "
         "before any assert",
         expect="absent"),
    Case("oracle-solve-sh", "P", "F", (),
         "the task's published solution/solve.sh run verbatim with cwd /app (it creates polyglot/ relatively): a "
         "real polyglot whose Fibonacci loop both runtimes run",
         recipe=ORACLE),
    Case("lookup-table", "P", "F", ("fib-kth",),
         "a polyglot that hardcodes the three graded outputs, read out of the PUBLIC tests/test_outputs.py at recipe "
         "time and turned into a print table: the grader has exactly three fixed points and never inspects the "
         "source, so a lookup table is indistinguishable from computing",
         recipe=LOOKUP),
    Case("python-only", "F", "F", ("c-build",),
         "valid Python that is not C (a plain import/def/raise program): python3 runs it, gcc fails with a parse "
         "error and check=True raises CalledProcessError",
         recipe=emit(r'''import sys

def main() -> int:
    if len(sys.argv) != 2:
        return 2
    a, b = 0, 1
    for _ in range(int(sys.argv[1])):
        a, b = b, a + b
    print(a)
    return 0

raise SystemExit(main())
''')),
    Case("c-only", "F", "F", ("python-run",),
         "valid C that is not Python (no # comment line, no Python expression): gcc builds it and it prints the "
         "right value, python3 aborts with a SyntaxError before the first expected value is compared",
         recipe=emit(r'''#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    unsigned long long a = 0, b = 1, t;
    unsigned int n = (unsigned int)strtoul(argv[1], NULL, 10);
    for (unsigned int i = 0; i < n; ++i) { t = a + b; a = b; b = t; }
    printf("%llu\n", a);
    return 0;
}
''')),
    Case("extra-file", "F", "F", ("single-file",),
         "the oracle polyglot plus one unrelated file (NOTES.md) in /app/polyglot: the listing assert compares the "
         "whole list to [\"main.py.c\"], so a harmless extra file fails before gcc runs",
         recipe=ORACLE + "printf 'notes\\n' > /app/polyglot/NOTES.md\n"),
    Case("leftover-cmain", "F", "F", ("single-file",),
         "the oracle polyglot plus the binary that instruction.md:5 itself tells the agent to build "
         "(`gcc ... -o /app/polyglot/cmain && ./cmain N`): following the instruction leaves the second entry the "
         "grader's listing forbids - instruction and grader contradict each other",
         recipe=ORACLE + "gcc /app/polyglot/main.py.c -o /app/polyglot/cmain 2>/dev/null || true\n"),
    Case("wrong-value", "F", "F", ("fib-kth",),
         "a real polyglot whose f(42) is off by one (both runtimes print fib(n)+1 when N is 42): the value, not the "
         "shape, decides; the C loop also writes cmain, so the re-grade is what the listing sees",
         recipe=emit(poly(py="v = fib(_k)\nprint(v + 1 if _k == 42 else v)",
                          c='    printf("%llu\\n", n == 42 ? a + 1 : a);'))),
    Case("trailing-ws", "P", "F", (),
         "a correct polyglot that pads its output with leading and trailing spaces and blank lines in both "
         "runtimes: the grader compares stdout.strip(), which erases whitespace on both ends",
         recipe=emit(poly(py='print("   %d   \\n\\n" % fib(_k))',
                          c='    printf("  %llu  \\n\\n", a);'))),
    Case("nonzero-exit", "F", "F", (),
         "a correct polyglot that prints the right value and then exits non-zero (python sys.exit(3) / C return 3): "
         "the grader runs both runtimes with check=True, so a non-zero status fails a run whose stdout matched - "
         "the instruction never says the exit status must be 0",
         recipe=emit(poly(py="print(fib(_k))\nsys.exit(3)", ret="3"))),
    Case("stderr-noise", "P", "F", (),
         "a correct polyglot that also writes to stderr in both runtimes (python print(..., file=sys.stderr), C "
         "fprintf(stderr, ...)): the grader captures stderr and compares only stdout, so noise is invisible",
         recipe=emit(poly(py='print("noise", file=sys.stderr)\nprint(fib(_k))',
                          c='    fprintf(stderr, "noise\\n");\n    printf("%llu\\n", a);'))),
    Case("n-parsed-differently", "F", "F", ("fib-kth",),
         "a polyglot whose two sides read N differently - Python int(argv[1]), C the first digit only "
         "(argv[1][0]-'0') - so 42 and 10 disagree while 0 happens to match; no case proves both runtimes parsed N",
         recipe=emit(poly(nparse="    unsigned int n = (unsigned int)(argv[1][0] - '0');"))),
    Case("compile-warning", "P", "F", (),
         "a correct polyglot carrying an explicit `#warning` line (a Python comment, a C preprocessing warning): "
         "gcc exits 0 with a diagnostic on stderr, and check=True only reads the exit status",
         recipe=emit(poly(warn="#warning polyglot-fallback-path\n"))),
    Case("regrade-same-state", "P", "F", ("single-file",),
         "the oracle's end state, graded and then graded again: the first grade's own gcc writes "
         "/app/polyglot/cmain, so the same untouched state fails the second time - the grader is not idempotent "
         "(this row is the deliberate re-grade of oracle-solve-sh's state; the per-case `regrade` column is its "
         "measurement)",
         recipe=ORACLE),
    Case("empty-file", "F", "F", ("fib-kth",),
         "a zero-byte /app/polyglot/main.py.c: the listing passes, python3 prints nothing, and gcc links nothing "
         "with a main - both runtimes are wrong before any value is compared",
         recipe="mkdir -p " + DIRP + "\n: > " + SRC + "\n"),
    Case("dir-in-place", "F", "F", ("c-build",),
         "a DIRECTORY at /app/polyglot/main.py.c: the listing is exactly [\"main.py.c\"] so the precondition passes, "
         "then gcc is handed a directory and check=True raises CalledProcessError",
         recipe="mkdir -p " + DIRP + "\nmkdir -p " + SRC + "\n",
         expect="dir"),
    Case("crlf-source", "P", "F", (),
         "a correct polyglot whose whole source uses CRLF line endings: CPython's tokenizer and gcc both accept "
         "CRLF, so the newline style of the source is invisible to this grader",
         recipe="mkdir -p " + DIRP + "\ncat > /tmp/plain.py.c <<'POLYGLOT_EOF'\n" + poly() + "POLYGLOT_EOF\n"
         + "python3 -c \"d=open('/tmp/plain.py.c','rb').read(); "
           "open('/app/polyglot/main.py.c','wb').write(d.replace(b'\\n', b'\\r\\n'))\"\n"),
    Case("value-plus-line", "F", "F", ("stdout-only",),
         "a polyglot that prints the right value followed by a second line of output in both runtimes: "
         "strip() trims only the ends, so the compared string is two lines and no case fires the equality",
         recipe=emit(poly(py='print(fib(_k))\nprint("decoy")',
                          c='    printf("%llu\\n", a);\n    puts("decoy");'))),
]

HARNESS_PY = r'''
import contextlib, importlib.util, io, os, subprocess, sys
mode = sys.argv[1]
if mode in ("stage", "recipe", "all"):
    for step, script in (("seed", "/seed.sh"), ("recipe", "/recipe.sh")):
        rc = subprocess.run(["bash", "-euo", "pipefail", script], cwd="/app", stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        print("STAGE " + step + " rc=" + str(rc), flush=True)
        if rc:
            sys.exit(3)
    names = sorted(os.listdir("/app/polyglot")) if os.path.isdir("/app/polyglot") else None
    print("STAGE dir=" + ("absent" if names is None else (",".join(names) or "empty")), flush=True)
    p = "/app/polyglot/main.py.c"
    if os.path.isdir(p):
        state = "dir"
    elif os.path.exists(p):
        state = "bytes=" + str(os.path.getsize(p))
    else:
        state = "absent"
    print("STAGE file=" + state, flush=True)
    if mode == "stage":
        if os.path.isfile(p):
            try:
                compile(open(p, encoding="utf-8", errors="replace").read(), p, "exec")
                print("STAGE pycheck=ok", flush=True)
            except SyntaxError as e:
                print("STAGE pycheck=fail line=" + str(e.lineno), flush=True)
            r = subprocess.run(["gcc", "-fsyntax-only", p], capture_output=True, text=True)
            warn = sum(1 for l in r.stderr.splitlines() if ": warning:" in l)
            print("STAGE ccheck=" + ("ok" if r.returncode == 0 else "fail") + " cwarn=" + str(warn),
                  flush=True)
        else:
            print("STAGE pycheck=n/a ccheck=n/a", flush=True)
    if mode != "all":              # mode all continues into the two grade legs over the same /app tmpfs
        sys.exit(0)
con = os.dup(1)                    # verdict lines only: anything a child writes to fd 1 is discarded
null = os.open(os.devnull, os.O_WRONLY)
for leg in (1, 2):
    spec = importlib.util.spec_from_file_location("tb2_polyglot_c_py_grader", "/tests/test_outputs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    os.dup2(null, 1)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            getattr(mod, %r)()
        res = "P"
    except AssertionError:
        res = "F"
    except BaseException as e:
        res = "F error=" + type(e).__name__
    finally:
        os.dup2(con, 1)
    print("TEST leg" + str(leg) + " " + res, flush=True)
sys.exit(0)
''' % (TESTS[0],)


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def nproc_ceiling():
    """RLIMIT_NPROC is counted against every thread of this real uid host-wide, so the ceiling has to clear the
    live thread count before the sandbox can be created at all; what stays bounded is the headroom above it."""
    uid = os.getuid()
    total = 0
    try:
        entries = os.listdir("/proc")
    except OSError:
        return NPROC_FALLBACK
    for entry in entries:
        if not entry.isdigit():
            continue
        try:
            with open("/proc/" + entry + "/status", encoding="utf-8", errors="replace") as fh:
                real = None
                for line in fh:
                    if line.startswith("Uid:"):
                        real = int(line.split()[1])
                    elif line.startswith("Threads:"):
                        if real == uid:
                            total += int(line.split()[1])
                        break
        except (OSError, ValueError, IndexError):
            continue
    return total + NPROC_HEADROOM if total else NPROC_FALLBACK


def sandbox_argv(cap, work, nproc):
    """argv for one case. Binds come before `--remount-ro /` (a bind after it fails); `--remount-ro /dev` follows
    the /dev tmpfs mount, and /app plus /tmp are the sandbox's own sized tmpfs - the host tree is never bound."""
    argv = [PRLIMIT, "--nproc=" + str(nproc), *LIMITS, "--", BWRAP, "--unshare-all", "--die-with-parent",
            "--new-session", "--hostname", "polyglot-sandbox", "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev",
             "--size", "8388608", "--tmpfs", "/dev/shm", "--remount-ro", "/dev",
             "--size", "33554432", "--tmpfs", "/tmp", "--size", "67108864", "--tmpfs", "/app",
             "--ro-bind", str(work / "tests"), "/tests", "--dir", "/pub", "--dir", "/tpl"]
    for name, src in PUBLIC.items():
        argv += ["--ro-bind", str(cap / src), "/pub/" + name]
    argv += ["--ro-bind", str(work / "template.txt"), "/tpl/polyglot-template.txt",
             "--ro-bind", str(work / "seed.sh"), "/seed.sh", "--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
             "--ro-bind", str(work / "harness.py"), "/harness.py", "--clearenv"]
    for k, v in SBOX_ENV:
        argv += ["--setenv", k, v]
    argv += ["--chdir", "/app", "--remount-ro", "/"]
    return argv


def harness(cap, work, mode, nproc):
    """One sandbox invocation, with one retry at double headroom when the namespace itself could not be created
    (the uid thread count can grow between the measurement and the fork; a sandbox that never started produces no
    output at all and must not be read as a case verdict)."""
    rc, out = invoke(cap, work, mode, nproc)
    if rc == 1 and not out.strip():
        rc, out = invoke(cap, work, mode, nproc * 2)
    return rc, out


def invoke(cap, work, mode, nproc):
    """One sandbox invocation: stdout read through a CAP_BYTES store, killed at TIMEOUT seconds."""
    p = subprocess.Popen(sandbox_argv(cap, work, nproc) + ["/usr/bin/python3", "/harness.py", mode],
                         stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    buf = bytearray()

    def drain(fd):
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            if len(buf) < CAP_BYTES:
                buf.extend(chunk[:CAP_BYTES - len(buf)])

    reader = threading.Thread(target=drain, args=(p.stdout.fileno(),), daemon=True)
    reader.start()
    try:
        p.wait(timeout=TIMEOUT)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        p.kill()
        p.wait()
        rc = 124
    reader.join(5)
    p.stdout.close()
    return rc, bytes(buf).decode("utf-8", "replace")


def run_case(cap, root, case, mode, nproc):
    """One sandbox per case ('stage' -> stage legs; 'grade' -> seed, recipe and both grade legs on one /app
    tmpfs, which is what lets the re-grade see the cmain the first grade's gcc wrote)."""
    work = pathlib.Path(tempfile.mkdtemp(prefix="k46-pgp-", dir=root))
    try:
        tests = work / "tests"
        tests.mkdir()
        shutil.copyfile(cap / "test_outputs.py", tests / "test_outputs.py")
        (work / "template.txt").write_text(TEMPLATE)
        (work / "seed.sh").write_text("mkdir -p /app\n")
        (work / "recipe.sh").write_text(case.recipe or ":\n")
        (work / "harness.py").write_text(HARNESS_PY)
        return harness(cap, work, "stage" if mode == "stage" else "all", nproc)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def letters(out, leg):
    """(letters, note) for one grade leg; '-' when the leg printed no verdict line."""
    for l in out.splitlines():
        p = l.split(None, 3)
        if len(p) >= 3 and p[0] == "TEST" and p[1] == "leg" + str(leg):
            return "".join("P" if p[2] == "P" else "F" for _ in TESTS), (p[3] if len(p) > 3 else "")
    return "-" * len(TESTS), "no-verdict-line"


def overall(letters_):
    return "pass" if letters_ == "P" * len(TESTS) else "fail"


def regrade_tag(predicted, regrade):
    return "same" if regrade == predicted else "DIFF:" + regrade


def stage_line(out, key):
    for l in out.splitlines():
        if not l.startswith("STAGE "):
            continue
        for tok in l.split()[1:]:
            k, _, v = tok.partition("=")
            if k == key:
                return v
    return ""


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
            or any(len(c.predicted) != len(TESTS) or set(c.predicted) - {"P", "F", "-"} for c in CASES) \
            or any(len(c.regrade) != len(TESTS) or set(c.regrade) - {"P", "F", "-"} for c in CASES) \
            or any(c.expect not in ("src", "dir", "absent") for c in CASES):
        print("SETUP duplicate or malformed case id, unknown tag or malformed prediction", file=sys.stderr)
        return 2
    if a.dry:
        for t, loc in TAGS.items():
            print(f"TAG {t} {loc}")
        for c in CASES:
            shape = "recipe" if c.recipe else "absent"
            print(f"CASE {c.cid} predicted={overall(c.predicted)} tests={c.predicted}"
                  f" regrade={regrade_tag(c.predicted, c.regrade)}"
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
    root = pathlib.Path(tempfile.mkdtemp(prefix="k46-pgp-", dir=a.work))
    nproc = nproc_ceiling()
    try:
        if a.stage_check:
            bad = 0
            for c in CASES:
                rc, out = run_case(cap, root, c, "stage", nproc)
                dirv = stage_line(out, "dir")
                filev = stage_line(out, "file")
                seen = ("dir" if filev == "dir" else
                        "absent" if filev == "absent" else
                        "src" if filev.startswith("bytes=") else "?")
                ok = rc == 0 and seen == c.expect
                bad += not ok
                rest = " ".join(tok for l in out.splitlines() if l.startswith("STAGE ")
                                for tok in l.split()[1:]
                                if tok.split("=")[0] in ("pycheck", "ccheck", "cwarn"))
                print(f"STAGECHECK {c.cid} rc={rc} expect={c.expect} file={filev} dir={dirv}"
                      f" {rest} match={'yes' if ok else 'NO'}")
            print(f"stagecheck cases={len(CASES)} failed={bad}")
            return 0 if bad == 0 else 1
        print("# tb2 polyglot-c-py grader probe (kengaku round 46) @ terminal-bench-2 2fd12b88")
        for name in sorted(PINS):
            print(f"# capture {name} sha256={PINS[name]}")
        npass = nfail = mism = rediff = 0
        for c in CASES:
            rc, out = run_case(cap, root, c, "grade", nproc)
            if rc != 0:
                print(f"SETUP case {c.cid} sandbox failed (rc={rc})", file=sys.stderr)
                print(out, file=sys.stderr)
                return 2
            l1, n1 = letters(out, 1)
            l2, _n2 = letters(out, 2)
            obs = overall(l1)
            npass += obs == "pass"
            nfail += obs == "fail"
            match = l1 == c.predicted and (l2 == c.regrade)
            rmatch = regrade_tag(c.predicted, c.regrade) == ("same" if l2 == l1 else "DIFF:" + l2)
            mism += not (match and rmatch)
            rediff += l2 != l1
            print(f"CASE {c.cid} predicted={overall(c.predicted)} observed={obs} tests={l1}"
                  f" predicted_tests={c.predicted} match={'yes' if match and rmatch else 'NO'}"
                  f" regrade={'same' if l2 == l1 else 'DIFF:' + l2}"
                  f" violates={','.join(c.violates)}{' ' + n1 if n1 else ''} -- {c.requirement}")
        print(f"regrade cases={len(CASES)} differ={rediff}")
        print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

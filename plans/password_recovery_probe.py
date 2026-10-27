#!/usr/bin/env python3
"""Round-45 C2 probe: the pinned Terminal-Bench 2.0 `password-recovery` grader, executed offline.

  python3 plans/password_recovery_probe.py --lane .                run every frozen case, print the receipt
  python3 plans/password_recovery_probe.py --lane . --dry          print the frozen case table only (no sandbox)
  python3 plans/password_recovery_probe.py --lane . --stage-check  build every case's end state in the sandbox and
                                                                   report whether /app/recovered_passwords.txt
                                                                   exists; never grades

What runs: the captured grader `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88, digest checked before any
case) inside a bubblewrap sandbox per case: private network/pid/ipc namespaces, /usr and /etc read-only, /tmp
private, cwd /app (Dockerfile `WORKDIR /app`). /app is a fresh writable directory seeded the way the task image
seeds it: `environment/setup.sh` runs VERBATIM (it creates /app/varsea, a 4MB disk image at
/app/varsea/disks/sub1/subA/subAlpha/ae3f4c.dat, zips launchcode.txt, splits the zip into two fragments at
`offset+20`, and dd's them at the 1MB and 3MB offsets with a noise log at 2MB). One substitution, stated before
the first run: `/dev/urandom` is bound to a 64KB zeros file inside the sandbox, so the image's random fill and
the varsea noise become zeros while the fragment layout is reproduced byte-for-byte; `grep -aob` therefore
cannot find a stray '8XD' or 'W54' outside the fragments (the varsea file names carry `date +%s%N` timestamps
and stay non-deterministic, but nothing the grader or this probe reads depends on them). /tests holds the
captured test_outputs.py only. /pub holds read-only copies of three PUBLIC files at the pin (instruction.md,
test_outputs.py, solve.sh) standing in for what an agent could see. Each case then runs a recipe that writes
(or does not write) /app/recovered_passwords.txt, and the two captured test functions are executed one by one
against that end state by a tiny pytest-free harness (a case that fails the first test leaves the second a
skip: its result letter is recorded `-`; pytest itself would run every test and its exit status is identical,
which is the only thing tests/test.sh rewards). The verdict is the harness exit status: exit 0 when every
test returns, 1 when one raises (an AssertionError is `F`, any other exception is `F` with its class named).
A recipe that exits non-zero is a probe error (exit 2), never a verdict. The SAME end state is then graded by
a second, fresh harness process; the CASE line carries `regrade=same` or `regrade=DIFF:<letters>` (reported,
never used for the verdict).

The grader's facts this probe exercises (captured `test_outputs.py`): `test_recovery_file_exists` asserts
`Path("/app/recovered_passwords.txt").exists()` (`:8-10`); `test_password_match` reads that file,
`.strip().split("\\n")` it into `guesses` (`:14`), asserts `len(guesses) > 0` (`:16`, dead code - the split of
any string is non-empty, so no end state can fire it) and asserts the exact constant
`"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses` (`:18`): exact line membership of one hard-coded 23-character answer,
with no format, case, order, count or uniqueness check.

Cases are constructed end states, not agents. Predictions were written before the first recorded run of this
probe and frozen with it; the dry table is the freeze receipt. No case of this task was executed on this host
before the freeze (the round-44 probe covered a different task, `feal-linear-cryptanalysis`).

Each case names the instruction requirements it violates (`violates=` tags, see TAGS). An empty `violates=` on a
failing case is a grader stricter than the instruction; tags on a passing case name a requirement the grader
does not see.

Limits, stated before the first run: host python3 (the grader's imports are `pathlib` only) stands in for the
image's python 3.13 under `uvx -p 3.13`; the task image is never pulled; pytest is not run (the harness calls
the test functions and maps their outcome onto pytest's exit status); recipes run as the probing user, not
root; the `apt` tool installs in the Dockerfile are not replayed (the sandbox binds host /usr; `zip`, `dd`,
`strings`, `grep`, `od`, `tr`, `date`, `find`, `awk`, `sort`, `cut`, `head` are present on the host and checked
before any case); `tests/test.sh`'s uv/pytest bootstrap is not replayed - it only wraps pytest and writes the
reward file. Deterministic receipt: no temp path, timing or host version is printed. Scratch lives under --work
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

CAP = "corpus/evidence/round45/tb2-password-recovery"
PINS = {
    "setup.sh": "9fdde5d9cd74ae0d633bdd59e7249cc6d7385d27a98b1e2dbbeb11b05a6f2af8",
    "solve.sh": "c5f9fc70b6bae40befdd0088dde1a3bc6e909852c9fbb36a617c627b7b8d804f",
    "instruction.md": "bc4f501148805bbccdb94a5c5b745f1ce9564f04ef0fe36bc37c3ca20b7810a5",
    "test_outputs.py": "2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e",
}
PUBLIC = {"instruction.md": "instruction.md", "test_outputs.py": "tests/test_outputs.py",
          "solve.sh": "solution/solve.sh"}
BWRAP = "/usr/bin/bwrap"
TOOLS = ("/usr/bin/python3", "/usr/bin/bash", "/usr/bin/zip", "/usr/bin/dd", "/usr/bin/strings")
TESTS = ("test_recovery_file_exists", "test_password_match")
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# tag -> the instruction.md line that states the requirement (instruction.md as captured)
TAGS = {
    "forensic": "instruction.md:1",       # recover the PASSWORD from the deleted file
    "write-file": "instruction.md:9",     # write ... to the file: /app/recovered_passwords.txt
    "one-per-line": "instruction.md:9",   # one per line
    "one-guess": "instruction.md:9",      # make multiple guesses (grader: at least one line)
    "recover": "instruction.md:2",        # the recovered password is among the guesses
    "len23": "instruction.md:5",          # exactly 23 characters
    "prefix": "instruction.md:6",         # starts with "8XD"
    "suffix": "instruction.md:6",         # ends with "W54"
    "charset": "instruction.md:7",        # uppercase letters and digits only
}
OUT = "/app/recovered_passwords.txt"

# The answer read back from the PUBLIC grader copy (the leak channel these cases exercise): no constant is
# written into this probe - `PW` pulls it out of /pub/test_outputs.py inside the sandbox.
PW = "PW=$(grep -ao '8XD[A-Z0-9]*' /pub/test_outputs.py | head -n1)\n"
SEED = None  # filled at build time from the verbatim capture


@dataclasses.dataclass(frozen=True)
class Case:
    cid: str
    predicted: str          # one letter per TESTS entry; '-' = earlier test already failed
    violates: tuple
    requirement: str
    recipe: str = ""        # bash run in /app after the image seed, before grading


CASES = [
    Case("nop", "F-", ("write-file", "one-guess", "recover", "forensic"),
         "the seeded image state only - no recovered_passwords.txt"),
    Case("oracle-solve-sh", "PP", (),
         "the task's published solve.sh: recover the two zip fragments from the disk image, emit candidate "
         "passwords one per line (the oracle writes a handful of guesses, the true one among them)",
         recipe="bash /pub/solve.sh >/dev/null 2>&1 || true\n"),
    Case("constant", "PP", ("forensic",),
         "the 23-char answer read out of the public tests/test_outputs.py, written as one line - the grader "
         "cannot tell recovery from reading the public answer",
         recipe=PW + "printf '%s\\n' \"$PW\" > /app/recovered_passwords.txt\n"),
    Case("constant-crlf", "PP", ("forensic",),
         "the public answer on one CRLF-terminated line; read_text()'s universal-newline mode eats the "
         "carriage return",
         recipe=PW + "printf '%s\\r\\n' \"$PW\" > /app/recovered_passwords.txt\n"),
    Case("constant-joined", "PF", ("one-per-line", "forensic"),
         "the public answer concatenated with two decoys on ONE line - the line itself is not the answer",
         recipe=PW + "printf '%s\\n' \"${PW}8XDP5Q2RT9ZK7VB3BV4WW54Q2RT9ZK7VB3BV4WW54ZZ\" "
         "> /app/recovered_passwords.txt\n"),
    Case("dir-state", "PF", ("write-file", "one-guess", "recover"),
         "a DIRECTORY at /app/recovered_passwords.txt (plus the recovered password inside it): exists() is "
         "true, read_text() raises IsADirectoryError - the second test dies on a non-assert exception",
         recipe="mkdir -p /app/recovered_passwords.txt\n" + PW
         + "printf '%s\\n' \"$PW\" > /app/recovered_passwords.txt/x\n"),
    Case("empty-file", "PF", ("one-guess", "recover", "forensic"),
         "a zero-byte recovered_passwords.txt: the len(guesses)>0 assert at :16 cannot fire "
         "(split of '' is ['']), the membership assert at :18 decides",
         recipe=": > /app/recovered_passwords.txt\n"),
    Case("wrong-23", "PF", ("prefix", "suffix", "recover", "forensic"),
         "one 23-char uppercase/digit guess, format-conforming, wrong content",
         recipe="printf '%s\\n' 'ZZZZZZZZZZZZZZZZZZZZZZZ' > /app/recovered_passwords.txt\n"),
    Case("prefix-decoy", "PF", ("recover", "forensic"),
         "a guess that satisfies every published format constraint (23 chars, 8XD..W54, [A-Z0-9]) and is not "
         "the password - a partially recovered guess the grader cannot reward",
         recipe="printf '%s\\n' '8XDZZZZZZZZZZZZZZZZZW54' > /app/recovered_passwords.txt\n"),
    Case("sub-first", "PF", ("len23", "suffix", "recover", "forensic"),
         "the first 20 chars of the public answer - a truncated read",
         recipe=PW + "printf '%s\\n' \"${PW:0:20}\" > /app/recovered_passwords.txt\n"),
    Case("sub-last", "PF", ("len23", "prefix", "recover", "forensic"),
         "the last 20 chars of the public answer - the tail fragment only, missing the 8XD prefix",
         recipe=PW + "printf '%s\\n' \"${PW:3}\" > /app/recovered_passwords.txt\n"),
    Case("lower23", "PF", ("charset", "prefix", "suffix", "recover", "forensic"),
         "the public answer lowercased - case is part of the answer",
         recipe=PW + "printf '%s\\n' \"$(printf '%s' \"$PW\" | tr 'A-Z' 'a-z')\" "
         "> /app/recovered_passwords.txt\n"),
    Case("decoys-1000", "PP", ("forensic",),
         "the public answer plus 1000 wrong guesses, shuffled: the membership test has no count or "
         "uniqueness check",
         recipe=PW + "{ printf '%s\\n' \"$PW\"; seq 1 1000 | sed 's/^/WRONGGUESS/'; } "
         "> /app/recovered_passwords.txt\n"),
    Case("password-eq", "PF", ("recover", "forensic"),
         "the recovered password written in the file's OWN format 'PASSWORD=8XDP5...' (what launchcode.txt "
         "contained, instruction.md:4): the grader wants the bare value among the guesses, not the assignment",
         recipe=PW + "printf 'PASSWORD=%s\\n' \"$PW\" > /app/recovered_passwords.txt\n"),
    Case("crlf-line", "PP", ("forensic",),
         "the public answer on a CRLF-terminated line followed by a second guess: read_text()'s "
         "universal-newline mode translates \\r\\n to \\n before split, so a CRLF guess file still matches",
         recipe=PW + "printf '%s\\r\\nWRONGDECOY0\\n' \"$PW\" > /app/recovered_passwords.txt\n"),
    Case("under-varsea", "F-", ("write-file", "one-guess", "recover"),
         "the oracle's recovery work done from inside /app/varsea (the solver's cwd elsewhere): the guesses "
         "land at /app/varsea/recovered_passwords.txt, never at the graded path",
         recipe="cd /app/varsea && bash /pub/solve.sh >/dev/null 2>&1 || true\n"),
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
        p = "/app/recovered_passwords.txt"
        print("STAGE recovered " + (("bytes=" + str(os.path.getsize(p))) if os.path.exists(p) else "absent"),
              flush=True)
    sys.exit(0)
spec = importlib.util.spec_from_file_location("tb2_password_recovery_grader", "/tests/test_outputs.py")
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
             "--ro-bind", str(work / "zeros.bin"), "/dev/urandom",
             "--bind", str(work / "app"), "/app", "--ro-bind", str(work / "tests"), "/tests", "--dir", "/pub"]
    for name, src in PUBLIC.items():
        argv += ["--ro-bind", str(cap / src), "/pub/" + name]
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
    work = pathlib.Path(tempfile.mkdtemp(prefix="kprp-", dir=root))
    try:
        app, tests = work / "app", work / "tests"
        app.mkdir()
        tests.mkdir()
        (work / "zeros.bin").write_bytes(b"\0" * 65536)
        shutil.copyfile(cap / "tests/test_outputs.py", tests / "test_outputs.py")
        (work / "seed.sh").write_text((cap / "environment/setup.sh").read_text())
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


def letters(rc, out):
    """(letters, note): one letter per TESTS entry in run order; '-' for tests never reached.

    pytest's exit status decides (tests/test.sh:45-48); the TEST lines only name which test failed."""
    got = {}
    note = ""
    for l in out.splitlines():
        if l.startswith("TEST "):
            p = l.split(None, 3)
            got[p[1]] = p[2]
            if len(p) > 3:
                note = p[3]
    res = "".join(got.get(t, "-") for t in TESTS)
    if not got:
        note = f"exit={rc}-no-verdict-line" if rc else "exit=no-verdict-line"
    return res, note


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
            or any(len(c.predicted) != len(TESTS) or set(c.predicted) - {"P", "F", "-"} for c in CASES):
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
        src = {"setup.sh": "environment/setup.sh", "solve.sh": "solution/solve.sh",
               "instruction.md": "instruction.md", "test_outputs.py": "tests/test_outputs.py"}[name]
        if not (cap / src).is_file() or sha256(cap / src) != digest:
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
    root = pathlib.Path(tempfile.mkdtemp(prefix="k45-prp-", dir=a.work))
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
        print("# tb2 password-recovery grader probe (kengaku round 45) @ terminal-bench-2 2fd12b88")
        for name in sorted(PINS):
            print(f"# capture {name} sha256={PINS[name]}")
        npass = nfail = mism = rediff = 0
        for c in CASES:
            rc, res = run_case(cap, root, c, "grade")
            if rc != 0:
                print(f"SETUP case {c.cid} recipe failed (rc={rc})", file=sys.stderr)
                print(res, file=sys.stderr)
                return 2
            (l1, n1), (l2, _n2) = letters(*res[0]), letters(*res[1])
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

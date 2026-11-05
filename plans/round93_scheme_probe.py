#!/usr/bin/env python3
"""Replay the captured `schemelike-metacircular-eval` grader with its own test function
(round 93, R93-C1).

Each case stages a declarative /app tree (the captured `interp.py`, plus one eval.scm
variant derived deterministically from the captured reference solution, or none) and a
/tests tree (the captured grader plus all, one or none of its .scm test directories),
then imports the captured `tests/test_outputs.py` unmodified and calls `test_interp()`
inside a fresh bubblewrap namespace: tmpfs root, host /usr and /etc read-only, the case
/app bound read-write, the case /tests bound read-only, no network. The grader's own
subprocess calls (`python3 interp.py ...`, its 10 s / 60 s timeouts) run unpatched.

Observed vector per case, in this order (the case table's `leg_order`):

    outcome   P = test_interp() returned, F = it raised AssertionError, E = anything else
    passed    the N of the grader's own "Summary: N passed, M failed out of T tests" line
    failed    M of that line
    total     T of that line (`-` when the grader printed no Summary line)
    timeouts  count of the grader's own "FAILED: Timeout" lines

No assertion is reimplemented. The host /app and /tests are never touched: every bind
source lives under --work. The bwrap path is injectable (`--bwrap`) so a sandbox-outage
control can be run on any host (round-92 M13).

Usage:  python3 plans/round93_scheme_probe.py --lane <repo> --work <scratch dir> [--bwrap PATH]
Writes the receipt (stamp block plus observation block) to stdout.
Exit:   0 every case observed == predicted, 1 a case differed, 2 setup defect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CAP = "corpus/evidence/round93/graders/schemelike-metacircular-eval"
TABLE = "plans/round93-cases.json"
TOOL = "plans/round93_scheme_probe.py"
MEMBER = "schemelike-metacircular-eval"
HEADER = "# tb2 schemelike-metacircular-eval grader probe (round 93)"
SUBJECT_SHA = "fbb84e3c0c2f72ed7de90f54380f860052c16155e7d0c9076cd57c966e9be7ed"
INTERP_SHA = "efb8b5cdcf78b73afcf39d59600a1f355ca89b7bac9854bb01f110cc77bea2c1"
SOLVE_SHA = "e2c5b0ac2bef4801a1891e13c108813381877426c1a7f01bab86b4fc1f712510"
DEFAULT_BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 1200
MUL_FROM = "(define-var! '* (make-primitive (lambda (args) (* (car args) (cadr args)))) initial-env)"
MUL_TO = "(define-var! '* (make-primitive (lambda (args) (+ (car args) (cadr args)))) initial-env)"
FIB = "(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))\n(display (fib 35))\n(newline)\n"

HARNESS = r"""
import contextlib, importlib.util, io, re, sys
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
buf = io.StringIO()
outcome = "P"
try:
    with contextlib.redirect_stdout(buf):
        mod.test_interp()
except AssertionError:
    outcome = "F"
except BaseException as error:
    outcome = "E"
    print("ERROR " + type(error).__name__, file=sys.stderr)
text = buf.getvalue()
m = re.search(r"^Summary: (\d+) passed, (\d+) failed out of (\d+) tests$", text, re.M)
passed, failed, total = (m.group(1), m.group(2), m.group(3)) if m else ("-", "-", "-")
timeouts = len(re.findall(r"^FAILED: Timeout$", text, re.M))
print("PAYLOAD outcome=%s passed=%s failed=%s total=%s timeouts=%d" % (outcome, passed, failed, total, timeouts))
"""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def guarded(args: list[str]) -> str:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return "absent"
    text = (proc.stdout or proc.stderr).strip()
    return text.splitlines()[0] if text else "absent"


def reference_eval(solve: str) -> str:
    """The captured solution's heredoc body: lines between `cat <<'EOF' > eval.scm` and `EOF`."""
    lines = solve.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.startswith("cat <<'EOF' > eval.scm"))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].rstrip("\n") == "EOF")
    return "".join(lines[start + 1:end])


def eval_variant(kind: str, ref: str) -> str | None:
    if kind == "absent":
        return None
    if kind == "reference":
        return ref
    if kind == "mutant-mul":
        if ref.count(MUL_FROM) != 1:
            raise SystemExit("SETUP mutant-mul anchor count %d" % ref.count(MUL_FROM))
        return ref.replace(MUL_FROM, MUL_TO)
    if kind == "true-suffix-newline":
        return ref + "\n(newline)\n(display \"True\")\n"
    if kind == "true-suffix-bare":
        return ref + "\n(display \"True\")\n"
    if kind == "echo-filename":
        return "(display (read))\n(newline)\n"
    if kind == "fib-heavy":
        return FIB
    raise SystemExit("SETUP unknown eval kind %s" % kind)


def stage(case: dict, cap: Path, ref: str, root: Path) -> tuple[Path, Path]:
    app = root / "app"
    tests = root / "tests"
    if root.exists():
        shutil.rmtree(root)
    app.mkdir(parents=True)
    tests.mkdir(parents=True)
    shutil.copy2(cap / "tests" / "interp.py", app / "interp.py")
    shutil.copy2(cap / "tests" / "test_outputs.py", tests / "test_outputs.py")
    shutil.copy2(cap / "tests" / "interp.py", tests / "interp.py")
    body = eval_variant(case["eval"], ref)
    if body is not None:
        (app / "eval.scm").write_text(body, encoding="utf-8")
    sel = case["tests"]
    if sel == "full":
        shutil.copytree(cap / "tests" / "test", tests / "test")
        shutil.copytree(cap / "tests" / "shadow_test", tests / "shadow_test")
    elif sel.startswith("single:"):
        rel = sel.split(":", 1)[1]
        (tests / Path(rel).parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(cap / "tests" / rel, tests / rel)
    elif sel != "none":
        raise SystemExit("SETUP unknown tests selector %s" % sel)
    return app, tests


def run_case(bwrap: str, app: Path, tests: Path, harness: Path) -> str:
    cmd = [bwrap, "--die-with-parent", "--unshare-all",
           "--tmpfs", "/", "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc",
           "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
           "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",
           "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
           "--bind", str(app), "/app", "--ro-bind", str(tests), "/tests",
           "--ro-bind", str(harness), "/harness.py",
           "--setenv", "PATH", "/usr/bin", "--chdir", "/app",
           "/usr/bin/python3", "-I", "-B", "/harness.py"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=CASE_TIMEOUT)
    for line in proc.stdout.splitlines():
        if line.startswith("PAYLOAD "):
            fields = dict(tok.split("=", 1) for tok in line.split()[1:])
            return "%s,%s,%s,%s,%s" % (fields["outcome"], fields["passed"], fields["failed"],
                                       fields["total"], fields["timeouts"])
    return "NOPAYLOAD(rc=%d)" % proc.returncode


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    parser.add_argument("--bwrap", default=DEFAULT_BWRAP)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    cap = lane / CAP
    if not Path(args.bwrap).is_file() or not os.access(args.bwrap, os.X_OK):
        print("DEFECT SETUP sandbox-unavailable %s" % args.bwrap)
        return 2
    try:
        userns = Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    except OSError:
        userns = "absent"
    if not userns.isdigit() or int(userns) <= 0:
        print("DEFECT SETUP user namespaces unavailable (%s)" % userns)
        return 2
    subject = (cap / "tests" / "test_outputs.py").read_bytes()
    interp = (cap / "tests" / "interp.py").read_bytes()
    solve = (cap / "solution" / "solve.sh").read_bytes()
    if sha(subject) != SUBJECT_SHA or sha(interp) != INTERP_SHA or sha(solve) != SOLVE_SHA:
        print("DEFECT SETUP capture sha mismatch")
        return 2
    table_bytes = (lane / TABLE).read_bytes()
    table = json.loads(table_bytes.decode())
    ref = reference_eval(solve.decode())
    harness = work / "harness.py"
    harness.write_text(HARNESS, encoding="utf-8")
    tip = guarded(["git", "-C", str(lane), "rev-parse", "HEAD"])
    print(HEADER)
    print("MEMBER %s" % MEMBER)
    print("SUBJECT_SHA %s" % SUBJECT_SHA)
    print("INTERP_SHA %s" % INTERP_SHA)
    print("REFERENCE_EVAL_SHA %s" % sha(ref.encode()))
    print("TOOL_SHA %s" % sha((lane / TOOL).read_bytes()))
    print("CASE_TABLE_SHA %s" % sha(table_bytes))
    print("LANE_TIP %s" % tip)
    print("HOST_PYTHON %s" % guarded(["/usr/bin/python3", "-V"]))
    print("HOST_USERNS %s" % userns)
    print("LEG_ORDER %s" % ",".join(table["leg_order"]))
    print("OBSERVATIONS_BEGIN")
    mismatches = 0
    for case in table["cases"]:
        app, tests = stage(case, cap, ref, work / "cases" / case["id"])
        observed = run_case(args.bwrap, app, tests, harness)
        ok = observed == case["predicted"]
        mismatches += 0 if ok else 1
        print("CASE %s predicted=%s observed=%s ok=%s" % (case["id"], case["predicted"], observed, ok))
    print("OBSERVATIONS_END")
    print("mismatches %d" % mismatches)
    shutil.rmtree(work / "cases", ignore_errors=True)
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

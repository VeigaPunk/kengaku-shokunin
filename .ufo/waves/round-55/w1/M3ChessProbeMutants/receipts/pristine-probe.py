#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `chess-best-move` grader (round 55, C3).

Materializes the lane's committed capture
`corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` (terminal-bench-2 @
2fd12b88) as a byte-copy bound read-only at /tests inside a bubblewrap sandbox, and runs its
`test_move_correct()` against a frozen table of 12 synthetic /app/move.txt artefacts. The
grader judges an agent-written token file by order-insensitive full-multiset equality over
whitespace-split tokens: `assert sorted(move) == sorted(["g2g4", "e2e4"])`.

Each case carries a prediction (P/F) written from a static reading of the grader BEFORE the
first run (frozen with the round-55 claims, commit 80afa613). Observed verdicts: exit 0 = P;
nonzero exit with AssertionError in output = F; anything else (bwrap error, missing file,
OSError) = SETUP for that case -> whole run exits 2. The predicate line prints pass iff every
case's observed verdict equals its frozen prediction.

This executes scoring code on synthetic inputs only: no network, no model, no container, no
task certification.

Run as:
  python3 plans/round55_c3_chess_probe.py --lane . \
      --work /fast/scratch/hyaku/kengaku-r55/E5ChessProbe/work \
      --receipt corpus/evidence/round55/chess-best-move-probe.txt
Plumbing check without touching the TB2 capture:
  python3 plans/round55_c3_chess_probe.py --selftest --work <scratch>
"""
import argparse
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

TB2_PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py"
GRADER_SHA256 = "a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286"
BWRAP = "/usr/bin/bwrap"

PROG = ("import sys; sys.path.insert(0, '/tests'); "
        "import test_outputs as t; t.test_move_correct()")

ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
       "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}

# Frozen case table (round-55 claims, commit 80afa613): name | move.txt bytes | prediction.
# Predictions derive only from the captured grader's own assertion:
#   move = Path("/app/move.txt").read_text().strip().split()
#   assert sorted(move) == sorted(["g2g4", "e2e4"])
# i.e. order-insensitive full-multiset equality over whitespace-split tokens, no case or
# digit-width normalization.
CASES = [
    # both winning moves, one per line, lowercase ASCII: exact multiset -> pass
    ("both-lowercase-two-lines", "g2g4\ne2e4\n", "P"),
    # whitespace-separated on one line: split() is whitespace-agnostic -> pass
    ("both-space-separated", "g2g4 e2e4", "P"),
    # order is free (sorted() on both sides) -> pass
    ("reversed-order", "e2e4 g2g4", "P"),
    # only one of the two required moves -> fail
    ("single-move-only", "g2g4\n", "F"),
    # str.upper is never applied; sorted(["G2G4", ...]) != sorted(["g2g4", ...]) -> fail
    ("uppercase-white", "G2G4\ne2e4\n", "F"),
    # full-multiset equality: a third token breaks the cardinality -> fail
    ("extra-decoy-move", "g2g4\ne2e4\na2a3\n", "F"),
    # duplicate token leaves the multiset short of "g2g4" -> fail
    ("duplicate-move", "g2g4\ne2e4\ne2e4\n", "F"),
    # strip() + split() collapse leading/trailing/interior runs and blank lines -> pass
    ("whitespace-padded", "  g2g4   e2e4  \n\n", "P"),
    # empty file: split of '' is [], not the two-move multiset -> fail
    ("empty-file", "", "F"),
    # split() treats \r\n as whitespace; strip() eats the trailing run -> pass
    ("crlf-line-endings", "g2g4\r\ne2e4\r\n", "P"),
    # a legal-looking but wrong move from the instruction's example -> fail
    ("instruction-example-h1h8", "h1h8\ne2e4\n", "F"),
    # FULLWIDTH DIGIT TWO (\uFF12) is not ASCII '2'; no width normalization -> fail
    ("fullwidth-unicode-digit", "g\uFF12g4\ne2e4\n", "F"),
]

SELFTEST_CASES = [
    ("toy-pass", "ok\n", "P"),
    ("toy-fail", "bad\n", "F"),
]

TOY_TEST = '''"""Toy grader for --selftest plumbing checks (not the TB2 capture)."""
from pathlib import Path


def test_toy_correct():
    value = Path("/app/toy.txt").read_text().strip()
    assert value == "ok", "toy mismatch"
'''

TOY_PROG = ("import sys; sys.path.insert(0, '/tests'); "
            "import test_toy_probe as t; t.test_toy_correct()")


def sandbox_argv(tests_dir, app_dir):
    argv = [BWRAP, "--unshare-all", "--die-with-parent", "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
        elif os.path.isdir(link):
            argv += ["--ro-bind", link, link]
    argv += ["--ro-bind", "/etc", "/etc",
             "--proc", "/proc", "--dev", "/dev",
             "--tmpfs", "/tmp", "--tmpfs", "/home",
             "--ro-bind", str(tests_dir), "/tests",
             "--bind", str(app_dir), "/app",
             "--chdir", "/app"]
    return argv


def run_in_sandbox(tests_dir, app_dir, prog, timeout=120):
    """Returns (verdict, rc, combined_output); verdict in {"P", "F", "SETUP"}."""
    argv = sandbox_argv(tests_dir, app_dir) + ["/usr/bin/python3", "-c", prog]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, env=ENV,
                              timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return "SETUP", -1, f"timeout after {timeout}s: {exc}"
    except OSError as exc:
        return "SETUP", -1, f"failed to exec bwrap: {exc}"
    out = proc.stdout + proc.stderr
    if proc.returncode == 0:
        return "P", proc.returncode, out
    if "AssertionError" in out:
        return "F", proc.returncode, out
    return "SETUP", proc.returncode, out


def materialize_grader(lane, tests_dir):
    """Byte-copy the captured grader into tests_dir, refusing on any byte drift."""
    cap = pathlib.Path(lane) / GRADER_REL
    if not cap.is_file():
        raise SetupError(f"captured grader missing: {cap}")
    data = cap.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != GRADER_SHA256:
        raise SetupError(f"grader sha256 {digest} != frozen pin {GRADER_SHA256}")
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "test_outputs.py").write_bytes(data)


class SetupError(Exception):
    pass


def run_battery(lane, work, lines):
    tests_dir = work / "tests"
    materialize_grader(lane, tests_dir)
    cases_dir = work / "cases"
    observed_pass = observed_fail = mismatches = 0
    setup_names = []
    for name, content, predicted in CASES:
        casedir = cases_dir / name
        casedir.mkdir(parents=True, exist_ok=True)
        (casedir / "move.txt").write_bytes(content.encode("utf-8"))
        observed, rc, raw = run_in_sandbox(tests_dir, casedir, PROG)
        if observed == "SETUP":
            lines.append(f"CASE {name} predicted={predicted} observed=SETUP rc={rc}")
            setup_names.append(name)
            detail = " | ".join(raw.splitlines()[:3])[:300]
            print(f"SETUP-ERROR {name} rc={rc}: {detail}", file=sys.stderr)
            continue
        if observed == "P":
            observed_pass += 1
        else:
            observed_fail += 1
        if observed != predicted:
            mismatches += 1
        lines.append(f"CASE {name} predicted={predicted} observed={observed} rc={rc}")
    lines.append(f"cases={len(CASES)} observed_pass={observed_pass} "
                 f"observed_fail={observed_fail} mismatches={mismatches}")
    if setup_names:
        lines.append(f"SETUP cases={' '.join(setup_names)}")
        return 2
    if mismatches == 0:
        lines.append("PREDICATE R55-C3 pass")
        return 0
    lines.append("PREDICATE R55-C3 fail")
    return 1


def run_selftest(work, lines):
    """Run the same bwrap pipeline against a toy grader and toy artefacts only."""
    tests_dir = work / "selftests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "test_toy_probe.py").write_text(TOY_TEST, encoding="utf-8")
    failures = 0
    setup_hit = False
    for name, content, predicted in SELFTEST_CASES:
        casedir = work / "selfcases" / name
        casedir.mkdir(parents=True, exist_ok=True)
        (casedir / "toy.txt").write_bytes(content.encode("utf-8"))
        observed, rc, raw = run_in_sandbox(tests_dir, casedir, TOY_PROG)
        if observed == "SETUP":
            setup_hit = True
            detail = " | ".join(raw.splitlines()[:3])[:300]
            lines.append(f"SELFTEST CASE {name} observed=SETUP rc={rc}: {detail}")
            print(f"SETUP-ERROR selftest {name} rc={rc}: {detail}", file=sys.stderr)
            continue
        if observed != predicted:
            failures += 1
        lines.append(f"SELFTEST CASE {name} predicted={predicted} "
                     f"observed={observed} rc={rc}")
    lines.append(f"SELFTEST cases={len(SELFTEST_CASES)} failures={failures}")
    if setup_hit:
        return 2
    return 0 if failures == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=".",
                    help="lane repo root holding the captured grader (default: .)")
    ap.add_argument("--work", default=None,
                    help="scratch dir for case materialization (default: fresh dir under "
                         "TMPDIR); always removed on exit")
    ap.add_argument("--receipt", default=None,
                    help="path to tee the full output to")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the sandbox plumbing against a toy grader; does not touch "
                         "the TB2 capture")
    args = ap.parse_args(argv)

    work = pathlib.Path(args.work) if args.work else pathlib.Path(
        tempfile.mkdtemp(prefix="r55-c3-chess-probe-", dir=os.environ.get("TMPDIR") or None))
    lines = []
    code = 2
    try:
        if args.selftest:
            code = run_selftest(work, lines)
        else:
            try:
                code = run_battery(pathlib.Path(args.lane), work, lines)
            except SetupError as exc:
                print(f"SETUP {exc}", file=sys.stderr)
                lines.append(f"SETUP {exc}")
                code = 2
    finally:
        shutil.rmtree(work, ignore_errors=True)

    text = "\n".join(lines) + "\n"
    sys.stdout.write(text)
    if args.receipt:
        receipt = pathlib.Path(args.receipt)
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(text, encoding="utf-8")
    return code


if __name__ == "__main__":
    sys.exit(main())

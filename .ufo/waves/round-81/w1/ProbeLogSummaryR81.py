#!/usr/bin/env python3
"""Offline replay instrument for the pinned Terminal-Bench 2.0 `log-summary-date-ranges`
grader (kengaku round 81, R81-C1, seat ProbeLogSummaryR81).

What runs: the committed round-52 capture
`corpus/evidence/round52/graders/log-summary-date-ranges/tests/test_outputs.py`
(terminal-bench-2 @ 2fd12b88, sha256 pinned below) inside a bubblewrap sandbox per
case: private net/pid/ipc namespaces, /usr and /etc read-only, /tmp private, /app a
fresh writable directory, /tests holding only the capture the probe executes, cwd
/app.  The probe stages the case's end state at /app/summary.csv, then imports the
capture and calls its two test functions in file order -- no pytest runner.  A normal
return is `P`, an AssertionError is `F`, any other escaping exception is `F` with its
class named.  A case's verdict is `P` iff both functions return (pytest exits 0 iff no
test fails; tests/test.sh writes reward 1 iff pytest exits 0).

Predictions are DERIVED, never retyped: every case declares the grader requirements it
violates (`violates=` tags) and the predicted verdict is `P` iff that set is empty.
The tag -> leg map is the capture's own structure: `file-missing`
(test_summary_file_exists), `header` (`header == ["period","severity","count"]`),
`row-count` (`len(reader) - 1 == 15`), `content` (the 15-row zip equality).  The
exact-15 fixture table is parsed out of the capture's own `EXPECTED_ROWS` at run time,
so a mistyped fixture cannot masquerade as the expected end state.

Note on the frozen seat table: the seat spec annotates `extra trailing blank line (P)`,
but csv.reader yields an empty row for the blank line (16 data rows), so the case
violates `row-count` and derives F -- the same verdict the committed frozen instrument
`plans/round81_log_summary_probe.py` records for it.  The spec's own rule
("predictions are DERIVED from the case definitions in code, never retyped") wins over
the annotation; the two extra exact-variant cases (no trailing newline, quoted fields)
keep the table at the frozen >=4 P / >=4 F balance.

The graded artifact is a lane-authored end state, not an agent's output: this records
how the captured grader answers constructed CSVs, and nothing about any model or
agent.  The task image is never pulled and no network is used.

Run as:
  python3 ProbeLogSummaryR81.py --lane <lane> --work <scratch>
  python3 ProbeLogSummaryR81.py --lane <lane> --work <scratch> --receipt <path>
  python3 ProbeLogSummaryR81.py --lane <lane> --work <scratch> --selftest
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round52/graders/log-summary-date-ranges/tests/test_outputs.py"
PIN = "2fc06a6ce1944ad82f84fb437395fa75ed8c0eadd385b92e375c27e5bc9cb2b4"
BWRAP = "/usr/bin/bwrap"
SANDBOX_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
TESTS = ("test_summary_file_exists", "test_summary_structure_and_counts")

HEADER = "period,severity,count"
TAGS = {
    "file-missing": "output file absent",
    "header": "header is not exactly period,severity,count",
    "row-count": "data row count is not 15",
    "content": "one or more rows differ from the expected table",
}


def expected_rows(cap_text: str) -> list[list[str]]:
    """Parse EXPECTED_ROWS out of the capture -- the fixture table is the grader's own."""
    tree = ast.parse(cap_text)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "EXPECTED_ROWS":
                    return [list(r) for r in ast.literal_eval(node.value)]
    raise ValueError("EXPECTED_ROWS not found in capture")


def csv_text(rows, header=HEADER, eol="\n", trailing=True, quote=False):
    def cell(v):
        return f'"{v}"' if quote else v

    body = [",".join(cell(c) for c in header.split(","))]
    body += [",".join(cell(c) for c in r) for r in rows]
    text = eol.join(body)
    return text + (eol if trailing else "")


def build_cases(rows: list[list[str]]) -> list[tuple]:
    swapped = [rows[0], rows[2], rows[1]] + rows[3:]
    changed = [r if not (r[0] == "total" and r[1] == "INFO") else [r[0], r[1], "56622"]
               for r in rows]
    return [
        ("exact-15-rows", frozenset(), csv_text(rows)),
        ("exact-no-trailing-newline", frozenset(), csv_text(rows, trailing=False)),
        ("exact-crlf", frozenset(), csv_text(rows, eol="\r\n")),
        ("exact-quoted-fields", frozenset(), csv_text(rows, quote=True)),
        ("missing-file", frozenset({"file-missing"}), None),
        ("empty-file", frozenset({"header", "row-count"}), ""),
        ("wrong-header", frozenset({"header"}), csv_text(rows, header="date,level,total")),
        ("fourteen-rows", frozenset({"row-count"}), csv_text(rows[:14])),
        ("sixteen-rows", frozenset({"row-count"}), csv_text(rows + [["today", "DEBUG", "1"]])),
        ("one-count-changed", frozenset({"content"}), csv_text(changed)),
        ("two-rows-swapped", frozenset({"content"}), csv_text(swapped)),
        ("extra-blank-row", frozenset({"row-count"}), csv_text(rows) + "\n"),
    ]


CASES: list[tuple] = []  # populated in main() from the capture's own EXPECTED_ROWS


def predict_legs(case) -> tuple[str, str]:
    """Derive a case's per-leg prediction from its violated requirements (file order)."""
    tags = case[1]
    leg1 = "F" if "file-missing" in tags else "P"
    leg2 = "F" if tags - {"file-missing"} else "P"
    return leg1, leg2


def predicted(case) -> str:
    return "P" if predict_legs(case) == ("P", "P") else "F"


def harness_prog(tests) -> str:
    return r'''
import importlib.util
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for name in %r:
    try:
        getattr(mod, name)()
        print("LEG " + name + " P")
    except AssertionError:
        print("LEG " + name + " F")
    except Exception as e:
        print("LEG " + name + " F error=" + type(e).__name__)
''' % (tests,)


def sandbox_argv(grader_file: pathlib.Path, work: pathlib.Path):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent",
            "--new-session", "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev",
             "--tmpfs", "/tmp", "--bind", str(work / "app"), "/app", "--dir", "/tests",
             "--ro-bind", str(grader_file), "/tests/test_outputs.py",
             "--ro-bind", str(work / "harness.py"), "/harness.py", "--chdir", "/app"]
    return argv


def run_case(grader_file: pathlib.Path, root: pathlib.Path, content, tests):
    """Returns (verdict, letters) or (None, note) when the harness itself fails."""
    work = pathlib.Path(tempfile.mkdtemp(prefix="r81ls-", dir=root))
    try:
        app = work / "app"
        app.mkdir()
        if content is not None:
            (app / "summary.csv").write_bytes(content.encode())
        (work / "harness.py").write_text(harness_prog(tests))
        env = {"PATH": SANDBOX_PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        p = subprocess.run(sandbox_argv(grader_file, work) + ["/usr/bin/python3", "/harness.py"],
                           env=env, capture_output=True, text=True, timeout=180)
        legs = [ln.split()[1:] for ln in p.stdout.splitlines() if ln.startswith("LEG ")]
        if len(legs) != len(tests):
            return None, f"HARNESS rc={p.returncode} out={p.stdout.strip()[-160:]}"
        letters = "".join(leg[1] for leg in legs)
        return ("P" if letters == "P" * len(tests) else "F"), letters
    finally:
        shutil.rmtree(work, ignore_errors=True)


def run_battery(lane: pathlib.Path, work: pathlib.Path, lines: list[str]) -> int:
    cap = lane / CAP
    if not cap.is_file():
        lines.append(f"SETUP capture absent {CAP}")
        return 2
    got = hashlib.sha256(cap.read_bytes()).hexdigest()
    if got != PIN:
        lines.append(f"SETUP capture digest != pin {PIN}")
        return 2
    try:
        rows = expected_rows(cap.read_text())
    except Exception as e:
        lines.append(f"SETUP EXPECTED_ROWS unparseable: {e}")
        return 2
    global CASES
    CASES = build_cases(rows)
    if not pathlib.Path(BWRAP).exists():
        lines.append(f"SETUP bwrap absent at {BWRAP}")
        return 2
    work.mkdir(parents=True, exist_ok=True)
    mism = seen_p = seen_f = 0
    for case in CASES:
        obs, letters = run_case(cap, work, case[2], TESTS)
        pred = predicted(case)
        if obs is None:
            lines.append(f"SETUP harness failure {case[0]}: {letters}")
            return 2
        if obs == "P":
            seen_p += 1
        else:
            seen_f += 1
        if obs != pred:
            mism += 1
        lines.append(f"CASE {case[0]} predicted={pred} observed={obs} rc={0 if obs == 'P' else 1}")
    lines.append(f"cases={len(CASES)} observed_pass={seen_p} observed_fail={seen_f} "
                 f"mismatches={mism}")
    lines.append(f"PREDICATE R81-C1 {'pass' if mism == 0 else 'fail'}")
    return 0 if mism == 0 else 1


TOY_FAIL = "def toy_ok():\n    pass\n\n\ndef toy_assert():\n    raise AssertionError('toy')\n\n\ndef toy_escape():\n    raise RuntimeError('toy')\n"
TOY_PASS = "def toy_ok():\n    pass\n\n\ndef toy_fine():\n    pass\n"


def selftest(lane: pathlib.Path, work: pathlib.Path, lines: list[str]) -> int:
    """Two falsifier directions, no capture bytes needed for the pipeline half:
    (A) the tag map must predict F for every tagged case and P for every untagged one,
    and a single added tag must flip a case; (B) the same sandbox/harness path must
    return P for a returning toy function, F for an AssertionError and F error=...
    for any other escaping exception, and P for an all-pass toy grader."""
    rows = expected_rows((lane / CAP).read_text()) if (lane / CAP).is_file() else None
    if rows is None:
        lines.append("SETUP capture absent for derivation half")
        return 2
    bad = 0
    cases = build_cases(rows)
    for case in cases:
        want = "P" if not case[1] else "F"
        if predicted(case) != want:
            bad += 1
            lines.append(f"SELFTEST-FAIL derivation {case[0]}")
    flipped = ("flip-probe", frozenset({"content"}), None)
    if predicted(flipped) != "F":
        bad += 1
        lines.append("SELFTEST-FAIL flip")
    if not pathlib.Path(BWRAP).exists():
        lines.append(f"SETUP bwrap absent at {BWRAP}")
        return 2
    work.mkdir(parents=True, exist_ok=True)
    toy_fail = work / "toy_fail.py"
    toy_pass = work / "toy_pass.py"
    toy_fail.write_text(TOY_FAIL)
    toy_pass.write_text(TOY_PASS)
    checks = [
        (toy_fail, ("toy_ok", "toy_assert", "toy_escape"), "PFF", "F"),
        (toy_pass, ("toy_ok", "toy_fine"), "PP", "P"),
    ]
    for path, tests, want_letters, want_verdict in checks:
        obs, letters = run_case(path, work, "", tests)
        if obs is None or letters != want_letters or obs != want_verdict:
            bad += 1
            lines.append(f"SELFTEST-FAIL pipeline {path.name}: got={letters!r} verdict={obs!r}")
    checks_n = len(cases) + 1 + len(checks)
    lines.append(f"SELFTEST checks={checks_n} failures={bad}")
    return 0 if bad == 0 else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    lines: list[str] = []
    rev = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    if not rev:
        lines.append("SETUP git rev-parse failed")
        print("\n".join(lines) + "\n", end="")
        return 2
    lines.append(f"REV {rev}")
    if a.selftest:
        work = pathlib.Path(a.work or tempfile.mkdtemp(prefix="r81ls-"))
        if a.work:
            work.mkdir(parents=True, exist_ok=True)
        rc = selftest(lane, work, lines)
    else:
        work = pathlib.Path(a.work or tempfile.mkdtemp(prefix="r81ls-"))
        work.mkdir(parents=True, exist_ok=True)
        rc = run_battery(lane, work, lines)
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if a.receipt:
        out = pathlib.Path(a.receipt)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

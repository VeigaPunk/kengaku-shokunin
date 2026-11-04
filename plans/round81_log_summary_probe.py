#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `log-summary-date-ranges` grader (round 81, R81-C1).

What runs: the committed capture `corpus/evidence/round52/graders/log-summary-date-ranges/tests/
test_outputs.py` (terminal-bench-2 @ 2fd12b88, byte-identical to the pinned-tree remote file,
sha256 pinned below) inside a bubblewrap sandbox per case: private net/pid/ipc namespaces, /usr and
/etc read-only, /tmp private, /app a fresh writable directory, /cap holding only the capture the
probe executes, cwd /app. The probe stages the case's end state at /app/summary.csv, then imports
the capture and calls its two test functions in file order: an AssertionError is `F`, any other
exception is `F` with its class named, a return is `P`. A case's verdict is `P` iff both functions
return (pytest exits 0 iff no test fails; tests/test.sh writes reward 1 iff pytest exits 0).

Predictions are DERIVED, not retyped: each case declares the instruction/grader requirements it
violates (`violates=` tags) and the predicted verdict is `P` iff that set is empty. The tag → leg map
is the capture's own structure: `file-missing` (test_summary_file_exists), `header`
(`header == ["period","severity","count"]`), `row-count` (`len(reader)-1 == 15`), `content`
(the 15-row zip equality).

The graded artifact is a lane-authored end state, not an agent's output: this records how the
captured grader answers constructed CSVs, and nothing about any model or agent. The task image is
never pulled and no network is used.

Run as:
  python3 plans/round81_log_summary_probe.py --lane . --work <scratch> [--receipt <path>]
  python3 plans/round81_log_summary_probe.py --lane . --render-table
  python3 plans/round81_log_summary_probe.py --lane . --selftest --work <scratch>
"""
from __future__ import annotations

import argparse
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
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
TESTS = ("test_summary_file_exists", "test_summary_structure_and_counts")

HEADER = "period,severity,count"
ROWS = [
    ("today", "ERROR", "370"), ("today", "WARNING", "463"), ("today", "INFO", "1433"),
    ("last_7_days", "ERROR", "2969"), ("last_7_days", "WARNING", "4020"),
    ("last_7_days", "INFO", "12203"),
    ("last_30_days", "ERROR", "9594"), ("last_30_days", "WARNING", "12847"),
    ("last_30_days", "INFO", "38702"),
    ("month_to_date", "ERROR", "4682"), ("month_to_date", "WARNING", "6327"),
    ("month_to_date", "INFO", "19420"),
    ("total", "ERROR", "14160"), ("total", "WARNING", "18772"), ("total", "INFO", "56621"),
]
TAGS = {
    "file-missing": "output file absent",
    "header": "header is not exactly period,severity,count",
    "row-count": "data row count is not 15",
    "content": "one or more rows differ from the expected table",
}


def csv_text(rows, header=HEADER, eol="\n", trailing=True, quote=False):
    def cell(v):
        return f'"{v}"' if quote else v
    body = [",".join(cell(c) for c in header.split(","))]
    body += [",".join(cell(c) for c in r) for r in rows]
    text = eol.join(body)
    return text + (eol if trailing else "")


def base(**kw):
    return [list(r) for r in ROWS]


CASES = [
    ("exact-15-rows", [], csv_text(base())),
    ("exact-no-trailing-newline", [], csv_text(base(), trailing=False)),
    ("exact-crlf", [], csv_text(base(), eol="\r\n")),
    ("exact-quoted-fields", [], csv_text(base(), quote=True)),
    ("missing-file", ["file-missing"], None),
    ("empty-file", ["header", "row-count"], ""),
    ("wrong-header", ["header"],
     csv_text(base(), header="date,level,total")),
    ("fourteen-rows", ["row-count"], csv_text(base()[:14])),
    ("sixteen-rows", ["row-count"], csv_text(base() + [["today", "DEBUG", "1"]])),
    ("one-count-changed", ["content"],
     csv_text([r if r[0] != "total" or r[1] != "INFO" else [r[0], r[1], "56622"] for r in base()])),
    ("two-rows-swapped", ["content"],
     csv_text([base()[0], base()[2], base()[1]] + base()[3:])),
    ("extra-blank-row", ["row-count"], csv_text(base()) + "\n"),
]

HARNESS_PY = r'''
import importlib.util, sys
spec = importlib.util.spec_from_file_location("tb2_log_summary", "/cap/test_outputs.py")
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
''' % (TESTS,)


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def predicted(case) -> str:
    return "P" if not case[1] else "F"


def sandbox_argv(cap: pathlib.Path, work: pathlib.Path):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent",
            "--new-session", "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--bind", str(work / "app"), "/app", "--dir", "/cap",
             "--ro-bind", str(cap), "/cap/test_outputs.py",
             "--ro-bind", str(work / "harness.py"), "/harness.py", "--chdir", "/app"]
    return argv


def run_case(cap: pathlib.Path, root: pathlib.Path, case) -> tuple[str, str]:
    name, _tags, content = case
    work = pathlib.Path(tempfile.mkdtemp(prefix="r81ls-", dir=root))
    try:
        app = work / "app"
        app.mkdir()
        if content is not None:
            (app / "summary.csv").write_bytes(content.encode())
        (work / "harness.py").write_text(HARNESS_PY)
        env = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        p = subprocess.run(sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py"],
                           env=env, capture_output=True, text=True, timeout=180)
        legs = [ln.split()[1:] for ln in p.stdout.splitlines() if ln.startswith("LEG ")]
        if len(legs) != len(TESTS):
            return "?", f"HARNESS rc={p.returncode} out={p.stdout.strip()[-160:]}"
        letters = "".join(leg[1] for leg in legs)
        return ("P" if letters == "P" * len(TESTS) else "F"), letters
    finally:
        shutil.rmtree(work, ignore_errors=True)


def render_table(lines: list[str]) -> None:
    for name, tags, _content in CASES:
        lines.append(f"TABLE {name} predicted={predicted((name, tags, None))} "
                     f"violates={','.join(tags) or '-'}")
    lines.append(f"CASES n={len(CASES)} predicted_pass="
                 f"{sum(1 for c in CASES if predicted(c) == 'P')} predicted_fail="
                 f"{sum(1 for c in CASES if predicted(c) == 'F')}")


def run_battery(lane: pathlib.Path, work: pathlib.Path, lines: list[str]) -> int:
    cap = lane / CAP
    if not cap.is_file():
        lines.append(f"SETUP capture absent {CAP}")
        return 2
    got = sha256(cap)
    if got != PIN:
        lines.append(f"SETUP capture digest != pin {PIN}")
        return 2
    if not pathlib.Path(BWRAP).exists():
        lines.append(f"SETUP bwrap absent at {BWRAP}")
        return 2
    work.mkdir(parents=True, exist_ok=True)
    mism = 0
    seen_p = seen_f = 0
    for case in CASES:
        obs, letters = run_case(cap, work, case)
        pred = predicted(case)
        if obs == "P":
            seen_p += 1
        elif obs == "F":
            seen_f += 1
        if obs != pred:
            mism += 1
        lines.append(f"CASE {case[0]} predicted={pred} observed={obs} rc={0 if obs == 'P' else 1}"
                     f" legs={letters} violates={','.join(case[1]) or '-'}")
    lines.append(f"cases={len(CASES)} observed_pass={seen_p} observed_fail={seen_f} mismatches={mism}")
    lines.append(f"PREDICATE R81-C1 {'pass' if mism == 0 else 'fail'}")
    return 0 if mism == 0 else 1


def selftest(lane: pathlib.Path, work: pathlib.Path, lines: list[str]) -> int:
    """Predictions against the tag map without a sandbox: every tagged case must predict F and every
    untagged case P; a case whose tags are cleared must flip its prediction."""
    bad = 0
    for name, tags, _c in CASES:
        want = "P" if not tags else "F"
        if predicted((name, tags, None)) != want:
            bad += 1
            lines.append(f"SELFTEST-FAIL {name}")
    flipped = ("exact-15-rows", ["content"], None)
    if predicted(flipped) != "F":
        bad += 1
        lines.append("SELFTEST-FAIL flip")
    lines.append(f"SELFTEST cases={len(CASES) + 1} failures={bad}")
    return 0 if bad == 0 else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--render-table", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    lines: list[str] = []
    rev = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    lines.append(f"REV {rev}")
    if a.render_table:
        render_table(lines)
        rc = 0
    elif a.selftest:
        work = pathlib.Path(a.work or tempfile.mkdtemp(prefix="k81ls-"))
        if a.work:
            work.mkdir(parents=True, exist_ok=True)
        rc = selftest(lane, work, lines)
    else:
        base_work = a.work or tempfile.mkdtemp(prefix="k81ls-")
        work = pathlib.Path(base_work)
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

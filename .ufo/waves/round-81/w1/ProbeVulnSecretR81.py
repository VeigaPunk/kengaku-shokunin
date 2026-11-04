#!/usr/bin/env python3
"""Offline replay instrument for the Terminal-Bench 2.0 `vulnerable-secret` grader (R81-C1).

Replays the committed round-52 capture
`corpus/evidence/round52/graders/vulnerable-secret/tests/test_outputs.py`
(39 lines, three test functions, five asserts: existence, exact stripped
equality with `FLAG{...}`, prefix/suffix/length) against staged
`/app/results.txt` artifacts, inside a bubblewrap sandbox. Same bwrap recipe
and leg rule as `plans/db_wal_probe.py` / `plans/round59_c1_openssl_probe.py`:
capture bound read-only at `/tests`, staged writable `/app`, the capture's own
test functions called in file order (`test_results_file_exists`,
`test_results_file_contains_secret_flag`, `test_results_file_format`); a case
observes P iff all three legs pass, rc=0 iff all legs pass.

Frozen case table (10 cases, 4 P / 6 F; each stages `/app/results.txt`):
  exact flag (P); exact flag with a trailing newline and surrounding spaces
  (P -- the grader strips); trailing newline only (P); surrounding spaces only
  (P); missing file (F); wrong flag (F); `FLAG{` only (F: endswith); `FLAG{x}`
  (F: len>10); flag plus a trailing second line (F: stripped equality);
  truncated flag (F). The enumerated table floors at 2 P, so the two
  newline-only / spaces-only strip variants are carried to satisfy the frozen
  ">= 8 cases with at least 4 P and 4 F" shape.

Predictions are DERIVED in code from the case definitions (never retyped): a
static model of the capture evaluates the five asserts on each case's staged
content (`leg_truth`), and the case predicts P iff every predicate holds.
`--selftest` cross-checks that derived model against an independently declared
violated-assert tag set per case, plus point flips and the frozen shape floors.

Battery stdout (the receiptable stream; the OBSERVATIONS block of a minted
receipt equals this stdout under the counter's projection):
  REV <hex commit>
  CASE <id> predicted=<P|F> observed=<P|F> rc=<0|1>
  cases=<n> observed_pass=<n> observed_fail=<n> mismatches=<n>
  PREDICATE R81-C1 pass|fail
Exit 0 iff mismatches=0; exit 2 on setup failure (bwrap absent, capture drift,
harness failure) -- a setup failure is never faked into an observation.
Per-leg detail (`LEG <case> <test> P|F`) goes to stderr only.

Run as:
  python3 ProbeVulnSecretR81.py --lane <lane> --work <scratch> [--receipt <path>]
  python3 ProbeVulnSecretR81.py --lane <lane> --selftest
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

CAP = "corpus/evidence/round52/graders/vulnerable-secret/tests/test_outputs.py"
PIN = "f2b65f63ac81acd1e80e1ad4c59c1022131a0f9eb20f8ab3212c4ef8d8f0c753"
BWRAP = "/usr/bin/bwrap"
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
TESTS = ("test_results_file_exists", "test_results_file_contains_secret_flag",
         "test_results_file_format")
FLAG = "FLAG{b4ff3r_0v3rfl0w_m4st3r_k3y_2024}"

# Case = (id, staged content for /app/results.txt (None: stage nothing),
#         declared violated-assert tags -- an INDEPENDENT cross-model used by
#         --selftest only; battery predictions come from leg_truth(), never
#         from these tags). Tag names name the capture's own asserts.
CASES = [
    ("exact-flag", FLAG, ()),
    ("exact-flag-newline-spaces", "  " + FLAG + "\n  ", ()),
    ("exact-flag-newline", FLAG + "\n", ()),
    ("exact-flag-spaces", "  " + FLAG + "  ", ()),
    # A missing file violates existence; the static model evaluates the other
    # four asserts on the would-be stripped content (empty), so all five fail.
    ("missing-file", None, ("exists", "equality", "prefix", "suffix", "length")),
    ("wrong-flag", "FLAG{wrong_key_0000}", ("equality",)),
    # "FLAG{": does not end with "}" and is not longer than 10 characters.
    ("prefix-only", "FLAG{", ("equality", "suffix", "length")),
    # "FLAG{x}": strips to itself, so equality and the >10 length both fail.
    ("short-flag", "FLAG{x}", ("equality", "length")),
    # An inner newline survives .strip(), so suffix fails alongside equality.
    ("flag-plus-second-line", FLAG + "\nsecond line", ("equality", "suffix")),
    # FLAG[:-1] ends in "2", not "}"; 37 chars still clear the length tooth.
    ("truncated-flag", FLAG[:-1], ("equality", "suffix")),
]

HARNESS_PY = r'''
import importlib.util, sys
spec = importlib.util.spec_from_file_location("tb2_vulnerable_secret", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rc = 0
for name in %r:
    try:
        getattr(mod, name)()
        print("LEG " + name + " P")
    except Exception as exc:
        rc = 1
        print("LEG " + name + " F error=" + type(exc).__name__)
sys.exit(rc)
''' % (TESTS,)


def leg_truth(content: str | None) -> dict[str, bool]:
    """Static model of the capture's five asserts, evaluated on staged content.

    Grounded line-by-line in the capture: exists (test 1), stripped equality
    with the flag (test 2), startswith FLAG{ / endswith } / len > 10 (test 3).
    """
    exists = content is not None
    stripped = (content or "").strip()
    return {
        "exists": exists,
        "equality": stripped == FLAG,
        "prefix": stripped.startswith("FLAG{"),
        "suffix": stripped.endswith("}"),
        "length": len(stripped) > 10,
    }


def violated(content: str | None) -> tuple[str, ...]:
    return tuple(name for name, ok in leg_truth(content).items() if not ok)


def predicted(content: str | None) -> str:
    return "P" if not violated(content) else "F"


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sandbox_argv(tests_dir: pathlib.Path, app_dir: pathlib.Path,
                 harness: pathlib.Path) -> list[str]:
    """The db_wal_probe/round59 recipe: ro /usr and /etc, proc/dev/tmpfs,
    writable staged /app, capture ro at /tests, harness ro, chdir /app."""
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc",
            "--die-with-parent", "--new-session", "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
        elif os.path.isdir(link):
            argv += ["--ro-bind", link, link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev",
             "--tmpfs", "/tmp", "--tmpfs", "/home",
             "--ro-bind", str(tests_dir), "/tests",
             "--bind", str(app_dir), "/app",
             "--ro-bind", str(harness), "/harness.py", "--chdir", "/app"]
    return argv


def run_case(cap: pathlib.Path, work: pathlib.Path, case) -> tuple[str, int, str]:
    """Returns (observed P|F, harness rc, per-leg letters). Never fakes:
    a sandbox or harness failure raises SetupError."""
    name, content, _tags = case
    cdir = pathlib.Path(tempfile.mkdtemp(prefix="r81vs-", dir=work))
    try:
        app = cdir / "app"
        app.mkdir()
        tests_dir = cdir / "tests"
        tests_dir.mkdir()
        shutil.copyfile(cap, tests_dir / "test_outputs.py")
        if content is not None:
            (app / "results.txt").write_bytes(content.encode())
        harness = cdir / "harness.py"
        harness.write_text(HARNESS_PY)
        env = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
               "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        argv = sandbox_argv(tests_dir, app, harness) + ["/usr/bin/python3", "/harness.py"]
        try:
            p = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired as exc:
            raise SetupError(f"{name} timeout after 120s: {exc}") from exc
        except OSError as exc:
            raise SetupError(f"{name} failed to exec bwrap: {exc}") from exc
        letters = [ln.split()[2] for ln in p.stdout.splitlines() if ln.startswith("LEG ")]
        if len(letters) != len(TESTS):
            raise SetupError(f"{name} harness rc={p.returncode} "
                             f"out={(p.stdout + p.stderr).strip()[-160:]}")
        marks = "".join(letters)
        ok = marks == "P" * len(TESTS)
        return ("P" if ok else "F"), (0 if ok else 1), marks
    finally:
        shutil.rmtree(cdir, ignore_errors=True)


class SetupError(Exception):
    pass


def run_battery(lane: pathlib.Path, work: pathlib.Path, lines: list[str]) -> int:
    cap = lane / CAP
    if not cap.is_file():
        raise SetupError(f"capture absent {CAP}")
    digest = sha256(cap)
    if digest != PIN:
        raise SetupError(f"capture sha256 {digest} != frozen pin {PIN}")
    if not pathlib.Path(BWRAP).exists():
        raise SetupError(f"bwrap absent at {BWRAP}")
    work.mkdir(parents=True, exist_ok=True)
    mism = seen_p = seen_f = 0
    for case in CASES:
        obs, rc, letters = run_case(cap, work, case)
        pred = predicted(case[1])
        if obs == "P":
            seen_p += 1
        else:
            seen_f += 1
        if obs != pred:
            mism += 1
        print(f"LEG {case[0]} {'/'.join(TESTS)} {letters}", file=sys.stderr)
        lines.append(f"CASE {case[0]} predicted={pred} observed={obs} rc={rc}")
    lines.append(f"cases={len(CASES)} observed_pass={seen_p} "
                 f"observed_fail={seen_f} mismatches={mism}")
    lines.append(f"PREDICATE R81-C1 {'pass' if mism == 0 else 'fail'}")
    return 0 if mism == 0 else 1


def selftest(lines: list[str]) -> int:
    """Prediction-only checks (no sandbox): the derived model must agree with
    every case's independently declared violated-assert tag set, a tampered
    exact flag must flip P->F, and the frozen shape floors must hold."""
    bad = checks = 0

    def fail(msg: str) -> None:
        nonlocal bad
        bad += 1
        lines.append(f"SELFTEST-FAIL {msg}")

    for name, content, tags in CASES:
        checks += 1
        if violated(content) != tuple(tags):
            fail(f"{name} violated={','.join(violated(content)) or '-'} "
                 f"declared={','.join(tags) or '-'}")
        checks += 1
        if predicted(content) != ("P" if not tags else "F"):
            fail(f"{name} predicted={predicted(content)} tags={','.join(tags) or '-'}")
    checks += 1
    if predicted(FLAG[:-3]) != "F" or predicted(FLAG[:-3] + "}") != "F":
        fail("tampered exact flag did not flip to F")
    checks += 1
    if predicted(FLAG.strip()) != "P" or predicted(FLAG + "\n\n") != "P":
        fail("strip semantics broke the exact flag's P")
    checks += 1
    n, np_, nf = len(CASES), sum(1 for c in CASES if predicted(c[1]) == "P"), \
        sum(1 for c in CASES if predicted(c[1]) == "F")
    if not (n >= 8 and np_ >= 4 and nf >= 4):
        fail(f"shape floors: cases={n} P={np_} F={nf} (need >=8/>=4/>=4)")
    checks += 1
    if TESTS != ("test_results_file_exists", "test_results_file_contains_secret_flag",
                 "test_results_file_format"):
        fail("leg order is not the capture's file order")
    lines.append(f"SELFTEST cases={n} checks={checks} failures={bad}")
    return 0 if bad == 0 else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None,
                    help="scratch parent for per-case sandboxes (default: mkdtemp)")
    ap.add_argument("--receipt", default=None,
                    help="also write the stdout stream to this path")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    lines: list[str] = []
    try:
        rev = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        if not rev:
            raise SetupError(f"unresolved HEAD at {lane}")
        lines.append(f"REV {rev}")
        if a.selftest:
            rc = selftest(lines)
        else:
            work = pathlib.Path(a.work) if a.work else \
                pathlib.Path(tempfile.mkdtemp(prefix="k81vs-"))
            rc = run_battery(lane, work, lines)
    except SetupError as exc:
        print(f"SETUP {exc}", file=sys.stderr)
        return 2
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if a.receipt:
        out = pathlib.Path(a.receipt)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

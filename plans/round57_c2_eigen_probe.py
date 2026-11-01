#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `largest-eigenval` grader (round 57, C2).

Materializes the lane's committed capture
`corpus/evidence/round57/tb2-eigenval/tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88)
as a byte-copy bound read-only at /tests inside a bubblewrap sandbox, and runs its three
test functions -- test_eigen_pair, test_dominance_eigenvalue, test_speedup -- directly
(no pytest runner) against a frozen table of lane-written synthetic /app/eigen.py
candidates. The grader is the corpus's first wall-clock-performance gate: two correctness
legs (eigen-pair residual, dominance vs np.linalg.eigvals) plus a timing leg that rewards
the candidate whose MEDIAN call time over N=100 seeded matrices is strictly below the
in-grader reference (np.linalg.eig itself), timed in an isolated process.

The capture imports `pytest` at module level; the probe stubs that module (no-op
`pytest.mark.parametrize` decorator) so the assertions execute without a pytest install.
The capture bytes are never modified and are sha256-pinned; the stub is probe-owned and
bound at /stub. numpy is the system WSL package.

Each case carries a prediction written from a static reading of the capture BEFORE the
first capture run (frozen with the round-57 claims; the plumbing was proven with a toy
grader only). Predictions are P (assertions pass), F (AssertionError) or U -- U marks a
case whose outcome is NOT derivable from the grader's static semantics (here: a candidate
identical to the reference algorithm, whose timing comparison is decided by host noise);
U cases are executed and reported observed-only and never count toward mismatches.
Observed verdicts: exit 0 = P; nonzero exit with AssertionError in output = F; anything
else (bwrap error, missing module, timeout) = SETUP for that case -> whole run exits 2.
The predicate line prints pass iff every P/F prediction equals its observed verdict.

This executes scoring code on synthetic lane-written inputs only: no network, no model,
no container image, no task certification, no agent run. Sampling note: the probe runs
sizes {2, 5, 10} for the correctness legs and {2, 10} for the timing leg -- a sample of
the grader's 2..10 grid, not the full pytest run.

Run as:
  python3 plans/round57_c2_eigen_probe.py --lane . --work <scratch> \
      --receipt corpus/evidence/round57/eigen-probe.txt
Plumbing check without touching the TB2 capture:
  python3 plans/round57_c2_eigen_probe.py --selftest --work <scratch>
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
GRADER_REL = "corpus/evidence/round57/tb2-eigenval/tests/test_outputs.py"
GRADER_SHA256 = "cdc58e3aa0960dac2e12a12b1cfa4131237d697762a6a78ebf33f80d2eb168ce"
BWRAP = "/usr/bin/bwrap"

PYTEST_STUB = '''def parametrize(*a, **k):
    def d(f):
        return f
    return d


class _Mark:
    parametrize = staticmethod(parametrize)


mark = _Mark()
'''

# Lane-written synthetic candidates; one is materialized as /app/eigen.py per case.
CANDIDATES = {
    # exact values/vectors from the same LAPACK call the grader's reference uses, plus a
    # fixed 200k-iteration Python loop per call (>=10 ms) that dwarfs the ~microsecond
    # reference median: mathematically exact, statically slower.
    "eig-sleep": (
        "import numpy as np\n"
        "\n"
        "\n"
        "def find_dominant_eigenvalue_and_eigenvector(A):\n"
        "    values, vectors = np.linalg.eig(np.asarray(A, dtype=np.float64))\n"
        "    idx = int(np.argmax(np.abs(values)))\n"
        "    for _ in range(200000):\n"
        "        pass\n"
        "    return values[idx], vectors[:, idx]\n"
    ),
    # identical to the grader's reference algorithm and cost: the timing comparison is
    # decided by host noise, not by the answer (the U cases).
    "eig-bare": (
        "import numpy as np\n"
        "\n"
        "\n"
        "def find_dominant_eigenvalue_and_eigenvector(A):\n"
        "    values, vectors = np.linalg.eig(np.asarray(A, dtype=np.float64))\n"
        "    idx = int(np.argmax(np.abs(values)))\n"
        "    return values[idx], vectors[:, idx]\n"
    ),
    # maximally wrong answer (eigenvalue 0, unit first column) that does no eigensolve:
    # the statically fastest possible candidate.
    "zero-e1": (
        "import numpy as np\n"
        "\n"
        "\n"
        "def find_dominant_eigenvalue_and_eigenvector(A):\n"
        "    v = np.zeros(A.shape[0], dtype=np.float64)\n"
        "    v[0] = 1.0\n"
        "    return 0.0, v\n"
    ),
}

PAIR_SIZES = (2, 5, 10)
SPEED_SIZES = (2, 10)


def _prog(leg, size):
    fn = {"pair": "test_eigen_pair", "dom": "test_dominance_eigenvalue",
          "speed": "test_speedup"}[leg]
    return (
        "import sys\n"
        "sys.path.insert(0, '/stub')\n"   # probe-owned pytest stub + this prog
        "sys.path.insert(0, '/app')\n"    # candidate module namespace (grader chdirs here)
        "sys.path.insert(0, '/tests')\n"  # the byte-pinned capture
        "import test_outputs as t\n"
        f"t.{fn}({size})\n"
    )


# Frozen case table (round-57 claims freeze; predictions from static reading only):
# (name, candidate, leg, size, prediction) -- prediction in {"P", "F", "U"}.
# Static readings, per capture function:
#   test_eigen_pair: np.linalg.eig's (value, vector) pairs satisfy
#     np.allclose(A @ v, value * v) for dense non-defective matrices (defectiveness has
#     probability zero under normal(0,1) entries); a zero vector is refused earlier;
#     (0.0, e1) fails because A @ e1 is the matrix's first column, nonzero w.p. 1.
#   test_dominance_eigenvalue: np.isclose(|cand|, |ref_max|) with the SAME values array
#     (eig-sleep/eig-bare) is a comparison of identical floats -> P; |0| against the
#     largest |eigenvalue| of a dense normal(0,1) matrix (order sqrt(n) sigma, w.p. 1
#     far above the 1e-8 default tolerance) -> F.
#   test_speedup: median of 100 per-call times in an isolated process; ref is
#     np.linalg.eig itself (~microseconds at these sizes). eig-sleep adds a fixed
#     200k-iteration loop (milliseconds) -> F w.p. 1. eig-bare IS the reference
#     algorithm: the dt < ref_dt comparison between two medians of identical code is
#     host-noise -> U. zero-e1 builds one vector and returns -- strictly less work than
#     a LAPACK eigensolve -> P w.p. 1.
CASES = []
for _s in PAIR_SIZES:
    CASES.append((f"eig-sleep-pair-s{_s}", "eig-sleep", "pair", _s, "P"))
    CASES.append((f"eig-bare-pair-s{_s}", "eig-bare", "pair", _s, "P"))
    CASES.append((f"zero-e1-pair-s{_s}", "zero-e1", "pair", _s, "F"))
for _s in PAIR_SIZES:
    CASES.append((f"eig-sleep-dom-s{_s}", "eig-sleep", "dom", _s, "P"))
    CASES.append((f"eig-bare-dom-s{_s}", "eig-bare", "dom", _s, "P"))
    CASES.append((f"zero-e1-dom-s{_s}", "zero-e1", "dom", _s, "F"))
for _s in SPEED_SIZES:
    CASES.append((f"eig-sleep-speed-s{_s}", "eig-sleep", "speed", _s, "F"))
    CASES.append((f"eig-bare-speed-s{_s}", "eig-bare", "speed", _s, "U"))
    CASES.append((f"zero-e1-speed-s{_s}", "zero-e1", "speed", _s, "P"))

ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
       "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}

# Toy grader + toy candidates for --selftest plumbing only (never the TB2 capture).
TOY_GRADER = (
    "import os\n"
    "import numpy as np\n"
    "import pytest\n"
    "from concurrent.futures import ProcessPoolExecutor\n"
    "\n"
    "os.chdir(\"/app\")\n"
    "import toy_cand as C\n"
    "\n"
    "\n"
    "def _ref(A):\n"
    "    return float(np.linalg.eigvalsh(A).max())\n"
    "\n"
    "\n"
    "def _time(func, mats):\n"
    "    import time\n"
    "    out = []\n"
    "    for A in mats:\n"
    "        t0 = time.perf_counter()\n"
    "        func(A)\n"
    "        t1 = time.perf_counter()\n"
    "        out.append(t1 - t0)\n"
    "    return out\n"
    "\n"
    "\n"
    "@pytest.mark.parametrize(\"size\", [2, 4])\n"
    "def test_pair(size):\n"
    "    val, vec = C.answer(np.eye(size))\n"
    "    assert not np.allclose(vec, 0)\n"
    "    assert np.allclose(np.eye(size) @ vec, val * vec)\n"
    "\n"
    "\n"
    "def test_speed():\n"
    "    mats = [np.eye(4) for _ in range(10)]\n"
    "    with ProcessPoolExecutor(max_workers=1) as ex:\n"
    "        ref = ex.submit(_time, _ref, mats).result(timeout=30)\n"
    "        cand = ex.submit(_time, C.answer, mats).result(timeout=30)\n"
    "    assert np.median(cand) < np.median(ref)\n"
)
TOY_CAND_OK = (
    "import numpy as np\n"
    "\n"
    "\n"
    "def answer(A):\n"
    "    return 1.0, np.ones(A.shape[0])\n"
)
TOY_CAND_BAD = (
    "import numpy as np\n"
    "\n"
    "\n"
    "def answer(A):\n"
    "    return 1.0, np.zeros(A.shape[0])\n"
)
TOY_PROG_OK = (
    "import sys\n"
    "sys.path.insert(0, '/stub')\n"
    "sys.path.insert(0, '/app')\n"
    "sys.path.insert(0, '/tests')\n"
    "import toy_grader as t\n"
    "t.test_pair(2)\n"
    "t.test_pair(4)\n"
    "t.test_speed()\n"
)
TOY_PROG_BAD = (
    "import sys\n"
    "sys.path.insert(0, '/stub')\n"
    "sys.path.insert(0, '/app')\n"
    "sys.path.insert(0, '/tests')\n"
    "import toy_grader as t\n"
    "t.test_pair(2)\n"
)


class SetupError(Exception):
    pass


def sandbox_argv(tests_dir, app_dir, stub_dir):
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
             "--ro-bind", str(stub_dir), "/stub",
             "--bind", str(app_dir), "/app",
             "--chdir", "/app"]
    return argv


def run_in_sandbox(tests_dir, app_dir, stub_dir, prog, timeout=120):
    """Returns (verdict, rc, combined_output); verdict in {"P", "F", "SETUP"}."""
    argv = sandbox_argv(tests_dir, app_dir, stub_dir) + ["/usr/bin/python3", "-I", "-c", prog]
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


def materialize(lane, tests_dir):
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


def make_stub_dir(work):
    stub = work / "stub"
    stub.mkdir(parents=True, exist_ok=True)
    (stub / "pytest.py").write_text(PYTEST_STUB, encoding="utf-8")
    return stub


def run_battery(lane, work, lines):
    tests_dir = work / "tests"
    materialize(lane, tests_dir)
    stub_dir = make_stub_dir(work)
    cases_dir = work / "cases"
    observed_pass = observed_fail = mismatches = setup_cases = 0
    observed_u = []
    for name, cand, leg, size, predicted in CASES:
        casedir = cases_dir / name
        casedir.mkdir(parents=True, exist_ok=True)
        (casedir / "eigen.py").write_text(CANDIDATES[cand], encoding="utf-8")
        observed, rc, raw = run_in_sandbox(tests_dir, casedir, stub_dir, _prog(leg, size))
        if observed == "SETUP":
            setup_cases += 1
            detail = " | ".join(raw.splitlines()[:3])[:300]
            print(f"SETUP-ERROR {name} rc={rc}: {detail}", file=sys.stderr)
            lines.append(f"CASE {name} predicted={predicted} observed=SETUP rc={rc}")
            continue
        if observed == "P":
            observed_pass += 1
        else:
            observed_fail += 1
        if predicted == "U":
            observed_u.append(f"{name}={observed}")
            lines.append(f"CASE {name} predicted=U observed={observed} rc={rc} (observed-only)")
            continue
        if observed != predicted:
            mismatches += 1
        lines.append(f"CASE {name} predicted={predicted} observed={observed} rc={rc}")
    lines.append(f"cases={len(CASES)} observed_pass={observed_pass} "
                 f"observed_fail={observed_fail} mismatches={mismatches} setup={setup_cases}")
    if observed_u:
        lines.append("OBSERVED-U " + " ".join(observed_u))
    if setup_cases:
        lines.append("PREDICATE R57-C2 fail")
        return 2
    if mismatches == 0:
        lines.append("PREDICATE R57-C2 pass")
        return 0
    lines.append("PREDICATE R57-C2 fail")
    return 1


def run_selftest(work, lines):
    """Run the same bwrap pipeline against a toy grader and toy candidates only."""
    tests_dir = work / "selftests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "toy_grader.py").write_text(TOY_GRADER, encoding="utf-8")
    stub_dir = make_stub_dir(work)
    ok_dir = work / "selfok"
    bad_dir = work / "selfbad"
    ok_dir.mkdir(parents=True, exist_ok=True)
    bad_dir.mkdir(parents=True, exist_ok=True)
    (ok_dir / "toy_cand.py").write_text(TOY_CAND_OK, encoding="utf-8")
    (bad_dir / "toy_cand.py").write_text(TOY_CAND_BAD, encoding="utf-8")
    failures = 0
    setup_hit = False
    for name, app_dir, prog, predicted in (
        ("toy-ok", ok_dir, TOY_PROG_OK, "P"),
        ("toy-bad", bad_dir, TOY_PROG_BAD, "F"),
    ):
        observed, rc, raw = run_in_sandbox(tests_dir, app_dir, stub_dir, prog)
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
    lines.append(f"SELFTEST cases=2 failures={failures}")
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
        tempfile.mkdtemp(prefix="r57-c2-eigen-probe-", dir=os.environ.get("TMPDIR") or None))
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

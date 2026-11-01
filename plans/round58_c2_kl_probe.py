#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `distribution-search` grader (round 58, C3).

Materializes the lane's committed capture
`corpus/evidence/round58/tb2-distribution-search/tests/test_outputs.py` (terminal-bench-2 @
2fd12b88) as a byte-copy bound read-only at /tests inside a bubblewrap sandbox, and runs its
four test functions -- test_distribution_file_exists, test_distribution_shape,
test_distribution_validity, test_kl_divergences -- directly (no pytest runner) against a
frozen table of lane-written synthetic /app/dist.npy candidates. The grader is the corpus's
first numeric-TOLERANCE gate: the decisive leg asserts BOTH KL(P||U) and KL(U||P) within
1e-3 of 10.0 over a 150,000-atom simplex, after an in-leg renormalization; the validity leg
(finite, strictly positive, <= 1, sum 1 within 1e-5) runs on the RAW array and its
strict-positivity check guards the backward-KL log domain.

The capture imports `pytest` at module level; the probe stubs that module (`pytest.fail`
raises AssertionError, `pytest.mark` is a no-op) so the assertions execute without a pytest
install. The capture bytes are never modified and are sha256-pinned; the stub is
probe-owned and bound at /stub. numpy is the system WSL package (the r56 A3.4 canonical
environment; uv/pytest absent).

Unlike the round-57 timing gate, this grader is DETERMINISTIC: every case's outcome follows
from float64 arithmetic on the constructed array, so the freeze carries zero U marks -- a
full-commitment prediction table (the r57 contrast is recorded in the knowledge entry).

Each candidate is built INSIDE the sandbox by probe-owned builder code from frozen literal
constants (the round-58 claims freeze carries the same constants; the `sol` constants come
from a round-58 authoring-time run of the maintainer's own three-level solver, capture
S211). No network, no model, no container image, no agent run: synthetic lane-written
arrays only.

Run as:
  python3 plans/round58_c2_kl_probe.py --lane . --work <scratch> \
      --receipt corpus/evidence/round58/kl-probe.txt
Plumbing check without touching the TB2 capture:
  python3 plans/round58_c2_kl_probe.py --selftest --work <scratch>
"""
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile

TB2_PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round58/tb2-distribution-search/tests/test_outputs.py"
GRADER_SHA256 = "02bca54db4849b7c911253fb92f941e21db8b1eea13261a7e5a9871fca68b4ed"
BWRAP = "/usr/bin/bwrap"

PYTEST_STUB = '''def fail(*a, **k):
    raise AssertionError(a[0] if a else "pytest.fail")


def parametrize(*a, **k):
    def d(f):
        return f
    return d


class _Mark:
    parametrize = staticmethod(parametrize)


mark = _Mark()
'''

# Frozen construction constants (round-58 claims freeze).
SOL_A = 2
SOL_B = 6325
SOL_PH = 0.4453992881456182
SOL_PM = 1.7260803274269405e-05
SOL_PL = 1.8683398418359735e-10
KLV = 150_000
KLT = 10.0

# Lane-written synthetic candidates; each is materialized as /app/dist.npy per case.
CANDIDATES = {
    # the authoring-time solution of the grader's own constraint system: 2 heavy atoms,
    # 6325 middle, 143673 light (the maintainer three-level solver's accepted point,
    # capture S211); both KLs land on 10.0 to float64 round-off.
    "sol": f'''
import numpy as np
V = {KLV}
def build():
    P = np.empty(V, dtype=np.float64)
    P[:{SOL_A}] = {SOL_PH!r}
    P[{SOL_A}:{SOL_A}+{SOL_B}] = {SOL_PM!r}
    P[{SOL_A}+{SOL_B}:] = {SOL_PL!r}
    P /= P.sum()
    return P
''',
    # uniform: the exact center of the simplex; both KLs are 0, far outside the band.
    "uniform": f'''
import numpy as np
V = {KLV}
def build():
    return np.full(V, 1.0 / V, dtype=np.float64)
''',
    # two-level with 7 heavy atoms solving only the backward constraint: kb = 10 exact,
    # kf = 9.9715 -- outside the band. The one-legged case.
    "kb-only-m7": f'''
import math
import numpy as np
V = {KLV}
T = {KLT!r}
def build():
    m = 7
    def g(x):
        return math.log1p((m / V) * math.expm1(x)) - (m / V) * x - T
    lo, hi = -50.0, 700.0
    for _ in range(300):
        mid = (lo + hi) / 2
        if g(lo) * g(mid) <= 0:
            hi = mid
        else:
            lo = mid
    x = (lo + hi) / 2
    b = 1.0 / (V - m + m * math.exp(x))
    a = math.exp(x) * b
    P = np.full(V, b, dtype=np.float64)
    P[:m] = a
    return P
''',
    # the solution with atom 0 set to exactly 0 (mass folded into atom 1): the validity
    # leg's strict-positivity check fails, and the backward KL's log domain breaks
    # (kb -> +inf, kf -> nan) -- the validity leg is load-bearing for leg 4.
    "minzero": f'''
import numpy as np
def build():
    P = np.empty({KLV}, dtype=np.float64)
    P[:{SOL_A}] = {SOL_PH!r}
    P[{SOL_A}:{SOL_A}+{SOL_B}] = {SOL_PM!r}
    P[{SOL_A}+{SOL_B}:] = {SOL_PL!r}
    P /= P.sum()
    P[0] = 0.0
    P[1] += {SOL_PH!r}
    return P
''',
    # a negative atom (mass folded into atom 1): validity fails on min > 0 and max > 1;
    # log of a negative value makes both KLs nan.
    "negatom": f'''
import numpy as np
def build():
    P = np.empty({KLV}, dtype=np.float64)
    P[:{SOL_A}] = {SOL_PH!r}
    P[{SOL_A}:{SOL_A}+{SOL_B}] = {SOL_PM!r}
    P[{SOL_A}+{SOL_B}:] = {SOL_PL!r}
    P /= P.sum()
    P[0] = -{SOL_PH!r} / 2.0
    P[1] += 1.5 * {SOL_PH!r}
    return P
''',
    # a nan atom: isfinite fails validity; nan propagates through both KLs.
    "nanatom": f'''
import numpy as np
def build():
    P = np.empty({KLV}, dtype=np.float64)
    P[:{SOL_A}] = {SOL_PH!r}
    P[{SOL_A}:{SOL_A}+{SOL_B}] = {SOL_PM!r}
    P[{SOL_A}+{SOL_B}:] = {SOL_PL!r}
    P /= P.sum()
    P[0] = np.nan
    return P
''',
    # the solution scaled by 1.001: the RAW sum moves 1e-3 away from 1 (validity fails at
    # its 1e-5 band), but the KL leg renormalizes first -- scale drift is invisible to it.
    "sumdrift": f'''
import numpy as np
def build():
    P = np.empty({KLV}, dtype=np.float64)
    P[:{SOL_A}] = {SOL_PH!r}
    P[{SOL_A}:{SOL_A}+{SOL_B}] = {SOL_PM!r}
    P[{SOL_A}+{SOL_B}:] = {SOL_PL!r}
    P /= P.sum()
    return P * 1.001
''',
    # the same two-level family at a 100,000-atom vocabulary (m=5, backward-solved):
    # wrong size (shape fails), still a valid simplex, kf outside the band.
    "wrongvocab-m5": f'''
import math
import numpy as np
V = 100000
T = {KLT!r}
def build():
    m = 5
    def g(x):
        return math.log1p((m / V) * math.expm1(x)) - (m / V) * x - T
    lo, hi = -50.0, 700.0
    for _ in range(300):
        mid = (lo + hi) / 2
        if g(lo) * g(mid) <= 0:
            hi = mid
        else:
            lo = mid
    x = (lo + hi) / 2
    b = 1.0 / (V - m + m * math.exp(x))
    a = math.exp(x) * b
    P = np.full(V, b, dtype=np.float64)
    P[:m] = a
    return P
''',
    # the solution reshaped (2, 75000): ndim fails the shape leg, but P.size and the
    # np.sum reductions are shape-agnostic -- validity and both KLs still pass.
    "twod": f'''
import numpy as np
def build():
    P = np.empty({KLV}, dtype=np.float64)
    P[:{SOL_A}] = {SOL_PH!r}
    P[{SOL_A}:{SOL_A}+{SOL_B}] = {SOL_PM!r}
    P[{SOL_A}+{SOL_B}:] = {SOL_PL!r}
    P /= P.sum()
    return P.reshape(2, 75000)
''',
    # atom 0 pushed to 1.2 with the rest scaled negative to keep the sum: validity fails
    # three ways (min < 0, max > 1), nan propagates through both KLs.
    "maxover": f'''
import numpy as np
def build():
    P = np.empty({KLV}, dtype=np.float64)
    P[:{SOL_A}] = {SOL_PH!r}
    P[{SOL_A}:{SOL_A}+{SOL_B}] = {SOL_PM!r}
    P[{SOL_A}+{SOL_B}:] = {SOL_PL!r}
    P /= P.sum()
    rest = P[1:].copy()
    P[0] = 1.2
    P[1:] = rest * (-0.2 / rest.sum())
    return P
''',
    # the solution with the middle level raised by a relative 5.2e-4 and renormalized: a
    # DIFFERENT distribution whose both KL errors stay inside the 1e-3 band
    # (kf err ~5.1e-4, kb err ~3.5e-5) -- the band accepts a neighbourhood, not a point.
    "tolbnd": f'''
import numpy as np
def build():
    P = np.empty({KLV}, dtype=np.float64)
    P[:{SOL_A}] = {SOL_PH!r}
    P[{SOL_A}:{SOL_A}+{SOL_B}] = {SOL_PM!r} * (1.0 + 5.2e-4)
    P[{SOL_A}+{SOL_B}:] = {SOL_PL!r}
    P /= P.sum()
    return P
''',
    # the solution as raw integer counts (x 1e12, rounded): the RAW array fails validity
    # (max ~4.5e11 > 1, sum ~1e12), but the KL leg renormalizes and is scale-invariant --
    # it passes. Leg 4 is blind to normalization.
    "intcounts": f'''
import numpy as np
def build():
    P = np.empty({KLV}, dtype=np.float64)
    P[:{SOL_A}] = {SOL_PH!r}
    P[{SOL_A}:{SOL_A}+{SOL_B}] = {SOL_PM!r}
    P[{SOL_A}+{SOL_B}:] = {SOL_PL!r}
    P /= P.sum()
    return np.round(P * 1e12).astype(np.int64)
''',
}

# Frozen case table (round-58 claims freeze; predictions from static reading + the same
# float64 construction math run at authoring time -- zero U marks, the r57 contrast).
# (name, candidate, (exists, shape, validity, kl)) -- each prediction in {"P", "F"}.
CASES = [
    ("sol", "sol", ("P", "P", "P", "P")),
    ("uniform", "uniform", ("P", "P", "P", "F")),
    ("kb-only-m7", "kb-only-m7", ("P", "P", "P", "F")),
    ("minzero", "minzero", ("P", "P", "F", "F")),
    ("negatom", "negatom", ("P", "P", "F", "F")),
    ("nanatom", "nanatom", ("P", "P", "F", "F")),
    ("sumdrift", "sumdrift", ("P", "P", "F", "P")),
    ("wrongvocab-m5", "wrongvocab-m5", ("P", "F", "P", "F")),
    ("twod", "twod", ("P", "F", "P", "P")),
    ("maxover", "maxover", ("P", "P", "F", "F")),
    ("tolbnd", "tolbnd", ("P", "P", "P", "P")),
    ("intcounts", "intcounts", ("P", "P", "F", "P")),
]

TEST_NAMES = ("test_distribution_file_exists", "test_distribution_shape",
              "test_distribution_validity", "test_kl_divergences")

ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
       "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}


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


def driver_prog(candidate_src):
    return (
        "import sys\n"
        "sys.path.insert(0, '/stub')\n"   # probe-owned pytest stub
        "sys.path.insert(0, '/tests')\n"  # the byte-pinned capture
        "import json\n"
        + candidate_src +
        "import numpy as np\n"
        "np.save('/app/dist.npy', build())\n"
        "import test_outputs as t\n"
        "res = {}\n"
        "setup_leg = None\n"
        "for name in " + repr(TEST_NAMES) + ":\n"
        "    try:\n"
        "        getattr(t, name)()\n"
        "        res[name] = 'P'\n"
        "    except AssertionError:\n"
        "        res[name] = 'F'\n"
        "    except Exception as e:\n"
        "        res[name] = 'SETUP'\n"
        "        setup_leg = name + ':' + type(e).__name__\n"
        "print('LEGS ' + json.dumps(res))\n"
        "if setup_leg:\n"
        "    print('LEG-SETUP ' + setup_leg)\n"
        "    sys.exit(3)\n"
        "sys.exit(0)\n"
    )


def run_in_sandbox(tests_dir, app_dir, stub_dir, prog, timeout=120):
    """Returns (per-leg dict or None, rc, combined_output)."""
    argv = sandbox_argv(tests_dir, app_dir, stub_dir) + ["/usr/bin/python3", "-I", "-c", prog]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, env=ENV,
                              timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return None, -1, f"timeout after {timeout}s: {exc}"
    except OSError as exc:
        return None, -1, f"failed to exec bwrap: {exc}"
    out = proc.stdout + proc.stderr
    legs = None
    for line in proc.stdout.splitlines():
        if line.startswith("LEGS "):
            legs = json.loads(line[5:])
    if legs is None:
        return None, proc.returncode, out
    if proc.returncode != 0 or any(v == "SETUP" for v in legs.values()):
        return legs, proc.returncode, out
    return legs, proc.returncode, out


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
    mismatches = setup_cases = 0
    for name, cand, predicted in CASES:
        casedir = cases_dir / name
        (casedir / "app").mkdir(parents=True)
        legs, rc, out = run_in_sandbox(tests_dir, casedir / "app", stub_dir,
                                       driver_prog(CANDIDATES[cand]))
        if legs is None or any(v == "SETUP" for v in legs.values()):
            setup_cases += 1
            lines.append(f"SETUP {name} rc={rc} :: {out.strip()[-200:]}")
            continue
        observed = tuple(legs[n] for n in TEST_NAMES)
        bad = [f"{n}:predicted-{p}-observed-{o}"
               for n, p, o in zip(TEST_NAMES, predicted, observed) if p != o]
        if bad:
            mismatches += 1
            lines.append(f"MISMATCH {name} " + "; ".join(bad))
        lines.append(f"CASE {name} predicted={'/'.join(predicted)} "
                     f"observed={'/'.join(observed)} " + ("ok" if not bad else "FAIL"))
    lines.append(f"cases={len(CASES)} legs={len(CASES) * len(TEST_NAMES)} "
                 f"mismatches={mismatches} setup={setup_cases} predicted_u=0")
    ok = mismatches == 0 and setup_cases == 0
    lines.append(f"PREDICATE R58-C3 {'pass' if ok else 'fail'}")
    return (0 if ok else 1)


TOY_GRADER = (
    "import numpy as np\n"
    "import pytest\n"
    "\n"
    "\n"
    "def test_loads():\n"
    "    try:\n"
    "        np.load('/app/dist.npy')\n"
    "    except FileNotFoundError:\n"
    "        pytest.fail('missing')\n"
    "\n"
    "\n"
    "def test_band():\n"
    "    P = np.load('/app/dist.npy')\n"
    "    v = float(P.sum())\n"
    "    assert abs(v - 1.0) <= 1e-3, f'sum {{v}} off band'\n"
)


def run_selftest(work, lines):
    """Run the same bwrap pipeline against a toy grader and toy candidates only."""
    tests_dir = work / "toytests"
    tests_dir.mkdir(parents=True)
    (tests_dir / "toy_grader.py").write_text(TOY_GRADER, encoding="utf-8")
    stub_dir = make_stub_dir(work / "toystub")
    ok_all = True
    for name, arr_src, want in (
        ("toy-ok", "import numpy as np\ndef build():\n    return np.array([0.5, 0.5])", ("P", "P")),
        ("toy-off", "import numpy as np\ndef build():\n    return np.array([0.9, 0.2])", ("P", "F")),
    ):
        casedir = work / "toy" / name
        (casedir / "app").mkdir(parents=True)
        prog = (
            "import sys\n"
            "sys.path.insert(0, '/stub')\n"
            "sys.path.insert(0, '/tests')\n"
            "import json\n"
            f"exec({str(arr_src)!r})\n"
            "import numpy as np\n"
            "np.save('/app/dist.npy', build())\n"
            "import toy_grader as t\n"
            "res = {}\n"
            "for name in ('test_loads', 'test_band'):\n"
            "    try:\n"
            "        getattr(t, name)()\n"
            "        res[name] = 'P'\n"
            "    except AssertionError:\n"
            "        res[name] = 'F'\n"
            "    except Exception as e:\n"
            "        res[name] = 'SETUP'\n"
            "print('LEGS ' + json.dumps(res))\n"
        )
        argv = sandbox_argv(tests_dir, casedir / "app", stub_dir) + [
            "/usr/bin/python3", "-I", "-c", prog]
        proc = subprocess.run(argv, capture_output=True, text=True, env=ENV, timeout=120)
        legs = None
        for line in proc.stdout.splitlines():
            if line.startswith("LEGS "):
                legs = json.loads(line[5:])
        got = tuple(legs.values()) if legs else ("NONE",)
        ok = got == want
        ok_all &= ok
        lines.append(f"SELFTEST {name} got={'/'.join(got)} want={'/'.join(want)} "
                     f"{'ok' if ok else 'FAIL'}")
    lines.append(f"SELFTEST {'pass' if ok_all else 'fail'}")
    return 0 if ok_all else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--receipt", default=None,
                    help="write the final text here as well as stdout")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    lines = []
    rev = subprocess.run(["git", "-C", str(a.lane), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    lines.append(f"REV {rev}")
    with tempfile.TemporaryDirectory(prefix="k58-c3-", dir=a.work) as work:
        if a.selftest:
            rc = run_selftest(pathlib.Path(work), lines)
        else:
            rc = run_battery(pathlib.Path(a.lane), pathlib.Path(work), lines)
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if a.receipt:
        receipt = pathlib.Path(a.receipt)
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(text, encoding="utf-8")
    return rc


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Round-44 R44PytestParity: rebuild the 14 probe case end states and grade them with real pytest.

The end state is built by the frozen probe's own code path (`pr.harness(cap, work, "recipe")`), so the
`/app` tree is byte-identical to `plans/feal_linear_probe.py`'s grade runs. Grading differs only in the
harness: `uvx -p 3.13 -w pytest==8.4.1 pytest /tests/test_outputs.py -v -rA` (captured tests/test.sh,
minus `--ctrf` and with UV_OFFLINE=1 because the sandbox has no network) instead of importing
test_attack. Pytest's process exit status is compared with the receipt's verdict per case.
"""
from __future__ import annotations

import importlib.util
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r44/R44PytestParity")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
RECEIPT = LANE / "corpus/evidence/round44/feal-linear-probe.txt"

spec = importlib.util.spec_from_file_location("probe_ref", S / "probe_ref.py")
pr = importlib.util.module_from_spec(spec)
sys.modules["probe_ref"] = pr
spec.loader.exec_module(pr)

CAP = LANE / pr.CAP
WORK = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else S / "w"

PYTEST_ENV = {
    "PATH": "/home/vgpnk/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "HOME": str(S / "home"),
    "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
    "TMPDIR": "/tmp",
    "UV_CACHE_DIR": str(S / "uvcache"),
    "UV_TOOL_DIR": str(S / "uvtools"),
    "UV_TOOL_BIN_DIR": str(S / "uvbin"),
    "UV_OFFLINE": "1",
}
if os.environ.get("PARITY_CACHE_ONLY_NO_FLAG"):
    PYTEST_ENV.pop("UV_OFFLINE")
UVX = "/home/vgpnk/.local/bin/uvx"
PYTEST_ARGV = ["-p", "3.13", "-w", "pytest==8.4.1", "pytest", "/tests/test_outputs.py", "-v", "-rA"]


def pytest_sandbox(cap, work):
    """The probe's sandbox (same /app, /tests, /pub binds) plus read-only $HOME and scratch for uv."""
    argv = pr.sandbox_argv(cap, work)
    assert argv[-2:] == ["--chdir", "/app"], argv[-2:]
    return argv[:-2] + ["--ro-bind", "/home/vgpnk", "/home/vgpnk", "--bind", str(S), str(S),
                        "--chdir", "/app"]


def build(cap, root, case):
    """The probe's `run_case` build half, verbatim (seed + recipe through /harness.py, no import)."""
    work = pathlib.Path(tempfile.mkdtemp(prefix="kpar-", dir=root))
    app, tests = work / "app", work / "tests"
    app.mkdir()
    tests.mkdir()
    for name in pr.TASK_DEPS:
        shutil.copyfile(cap / name, app / name)
    shutil.copyfile(cap / "test_outputs.py", tests / "test_outputs.py")
    (work / "seed.sh").write_text(pr.SEED)
    (work / "recipe.sh").write_text(case.recipe or ":\n")
    (work / "harness.py").write_text(pr.HARNESS_PY)
    rc, out = pr.harness(cap, work, "recipe")
    return work, rc, out


def grade(cap, work):
    p = subprocess.run(pytest_sandbox(cap, work) + [UVX] + PYTEST_ARGV,
                       env=PYTEST_ENV, capture_output=True, text=True, timeout=1800)
    return p.returncode, p.stdout + p.stderr


def collected(out):
    m = re.search(r"collected (\d+) items?", out)
    return int(m.group(1)) if m else None


def reason(rc, out):
    if rc == 0:
        m = re.search(r"^=+ (.*passed.*) =+$", out, re.M)
        return (m.group(1) if m else "rc=0").replace(" ", "_")
    m = re.search(r"^E\s+([A-Za-z_.]*Error[^ \n]*)", out, re.M)
    if m:
        return m.group(1)
    m = re.search(r"^FAILED \S+ - (.*)$", out, re.M)
    if m:
        return m.group(1)[:60].replace(" ", "_")
    return f"rc={rc}"


def receipt_verdicts():
    rows = {}
    for line in RECEIPT.read_text().splitlines():
        m = re.match(r"CASE (\S+) predicted=(\S+) observed=(\S+) tests=(\S+) .*regrade=(\S+)", line)
        if m:
            rows[m.group(1)] = (m.group(3), m.group(4), m.group(5))
    return rows


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    for name, digest in pr.PINS.items():
        got = pr.sha256(CAP / name)
        if got != digest:
            print(f"SETUP capture {name} sha256={got} != pinned {digest}", file=sys.stderr)
            return 2
    rows = receipt_verdicts()
    if len(rows) != len(pr.CASES):
        print(f"SETUP receipt rows={len(rows)} cases={len(pr.CASES)}", file=sys.stderr)
        return 2
    print(f"# pytest-parity harness: {UVX} {' '.join(PYTEST_ARGV)} (cwd=/app, bwrap --unshare-net)")
    print(f"# env UV_OFFLINE={PYTEST_ENV.get('UV_OFFLINE', 'unset')} UV_CACHE_DIR={S / 'uvcache'}"
          f" (no network in the sandbox)")
    root = pathlib.Path(tempfile.mkdtemp(prefix="k44-par-", dir=WORK))
    matched = mismatched = 0
    try:
        for case in pr.CASES:
            work, rc, out = build(CAP, root, case)
            try:
                if rc != 0:
                    print(f"SETUP case {case.cid} recipe failed rc={rc}", file=sys.stderr)
                    print(out, file=sys.stderr)
                    return 2
                rc1, out1 = grade(CAP, work)
                rc2, out2 = grade(CAP, work)
                v = "pass" if rc1 == 0 else "fail"
                v2 = "pass" if rc2 == 0 else "fail"
                obs, tests_letter, regrade = rows[case.cid]
                ok = v == obs and v2 == obs
                matched += ok
                mismatched += not ok
                n = collected(out1)
                print(f"PYTESTCASE {case.cid} receipt={obs}/{tests_letter}/regrade={regrade}"
                      f" pytest1={v}(rc={rc1}) pytest2={v2}(rc={rc2}) collected={n}"
                      f" parity={'yes' if ok else 'NO'} reason={reason(rc1, out1)}"
                      f" reason2={reason(rc2, out2)}")
            finally:
                shutil.rmtree(work, ignore_errors=True)
        print(f"pytest-parity rows={len(pr.CASES)} matched={matched} mismatched={mismatched}")
        return 0 if mismatched == 0 else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Replay the captured `fix-code-vulnerability` grader with its own six test functions
(round 95, R95-C1).

The task image (captured `environment/Dockerfile`) clones bottlepy/bottle at 0207a34f and then
removes the oracle with two sed deletions (`1562,1563d`, then `1567,1568d` on the result). This
probe rebuilds that /app/bottle.py offline from the captured upstream `bottle.py`, applying the
same two deletions, and checks the result hashes the same every run. Each case then stages a
declarative /app tree (one bottle variant plus one report variant, see the case table) and a
read-only /tests tree holding the captured `test_outputs.py`, imports the captured grader
unmodified and calls its six test functions in file order inside a fresh bubblewrap namespace:
tmpfs root, host /usr and /etc read-only, the case /app bound read-write, /tests read-only, no
network. The `solve` variant runs the captured `solution/solve.sh` itself, unmodified, with
/usr/bin/bash and host GNU sed in the same kind of namespace (cwd /app).

Import path. The harness (`tests/test.sh`) runs `python -m pytest ... /tests/test_outputs.py`
from WORKDIR /app: `-m` puts the cwd on sys.path and pytest's default prepend mode puts the
test file's directory in front of it. The harness here models exactly that order
(`sys.path[:0] = ["/tests", "/app"]`); the grader then inserts `/tests/bottle` (absent) itself.
The `imported` leg records which file the grader's `from bottle import _hkey` resolved to.

Observed vector per case, in the case table's `leg_order`:

    exists      test_report_file_exists_example    P returned, F AssertionError,
    vul_file    test_vul_file                      E:<exception type name> anything else
    cwe_id      test_cwe_id
    hkey_basic  test_hkey_basic_cases
    hkey_error  test_hkey_error_cases
    hkey_real   test_hkey_real_world_examples
    imported    sys.modules['bottle'].__file__ after the six calls (`-` if never imported)

No assertion is reimplemented. Every bind source lives under --work. The bwrap path is
injectable (`--bwrap`) so a sandbox-outage control runs on any host.

Usage:  python3 plans/round95_vuln_probe.py --lane <repo> --work <scratch dir> [--bwrap PATH]
Writes the receipt (stamp block plus observation block) to stdout.
Exit:   0 every case observed == predicted, 1 a case differed, 2 setup defect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CAP = "corpus/evidence/round95/graders/fix-code-vulnerability"
TABLE = "plans/round95-cases.json"
TOOL = "plans/round95_vuln_probe.py"
MEMBER = "fix-code-vulnerability"
HEADER = "# tb2 fix-code-vulnerability grader probe (round 95)"
PINS = {
    "tests/test_outputs.py": "c006a5de95b69bd78055aa26cc055734dbd50718ede25d331f767bfee4ef7f26",
    "solution/solve.sh": "7a0131b369d83ae8546ecc3f9b4e23d38240f1bd1f0941e4430fa85b5182ee03",
    "environment/Dockerfile": "0917470986224df4daf4854a71302ae81c73ba5dd6e25be1232d29b758a5b3ab",
    "upstream-bottle/bottle.py": "abf643683b4870e07500f8a035d1a076d4bf0bbf98eb2fb5180fbc3ef8fad802",
}
SUBJECT_SHA = PINS["tests/test_outputs.py"]
DEFAULT_BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 300
DELETIONS = [(1562, 1563), (1567, 1568)]  # the Dockerfile's two `sed -i -e 'a,bd'` lines, in order
HKEY_ANCHOR = "def _hkey(key):\n    key = touni(key)\n"
HVAL_ANCHOR = "def _hval(value):\n    value = touni(value)\n"
RAISE_KEY = ("    if '\\n' in key or '\\r' in key or '\\0' in key:\n"
             "        raise ValueError(\"Header names must not contain control characters: %r\" % key)\n")

REPORTS = {
    "upper-cwe": '{"file_path": "/app/bottle.py", "cwe_id": ["CWE-93"]}\n',
    "relative-path": '{"file_path": "bottle.py", "cwe_id": ["cwe-93"]}\n',
    "string-cwe": '{"file_path": "/app/bottle.py", "cwe_id": "cwe-93"}\n',
    "split-lines": ('{"file_path": "/app/bottle.py", "cwe_id": ["cwe-79"]}\n'
                    '{"file_path": "/app/bottle.py", "cwe_id": ["cwe-93"]}\n'),
    "trailing-blank-line": '{"file_path": "/app/bottle.py", "cwe_id": ["cwe-93"]}\n\n',
    "int-cwe": '{"file_path": "/app/bottle.py", "cwe_id": [93]}\n',
}

HARNESS = r"""
import importlib.util, os, sys
os.chdir("/app")
sys.path[:0] = ["/tests", "/app"]
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
out = []
for name in ("test_report_file_exists_example", "test_vul_file", "test_cwe_id",
             "test_hkey_basic_cases", "test_hkey_error_cases", "test_hkey_real_world_examples"):
    try:
        getattr(mod, name)()
        out.append("P")
    except AssertionError:
        out.append("F")
    except BaseException as error:
        out.append("E:" + type(error).__name__)
m = sys.modules.get("bottle")
out.append(getattr(m, "__file__", None) or "-" if m is not None else "-")
print("PAYLOAD " + ",".join(out))
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


def sandbox(bwrap: str, binds: list[tuple[str, str, str]], chdir: str, argv: list[str]) -> list[str]:
    cmd = [bwrap, "--die-with-parent", "--unshare-all",
           "--tmpfs", "/", "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc",
           "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
           "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",
           "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
    for kind, src, dst in binds:
        cmd += [kind, src, dst]
    return cmd + ["--setenv", "PATH", "/usr/bin", "--setenv", "HOME", "/tmp",
                  "--setenv", "LANG", "C.UTF-8", "--chdir", chdir, *argv]


def vulnerable(upstream: bytes) -> bytes:
    lines = upstream.decode().splitlines(keepends=True)
    for a, b in DELETIONS:
        del lines[a - 1:b]
    return "".join(lines).encode()


def insert_after(src: str, anchor: str, text: str) -> str:
    if src.count(anchor) != 1:
        raise SystemExit("SETUP anchor count %d for %r" % (src.count(anchor), anchor[:30]))
    return src.replace(anchor, anchor + text)


def bottle_variant(kind: str, upstream: bytes, vuln: bytes) -> tuple[bytes, dict[str, bytes]]:
    """Return (/app/bottle.py bytes, extra files) for a non-solve variant."""
    src = vuln.decode()
    if kind == "vulnerable":
        return vuln, {}
    if kind == "oracle":
        return upstream, {}
    if kind == "hkey-only":
        return insert_after(src, HKEY_ANCHOR, RAISE_KEY).encode(), {}
    if kind == "strip":
        return insert_after(src, HKEY_ANCHOR,
                            "    key = key.replace('\\n', '').replace('\\r', '').replace('\\0', '')\n").encode(), {}
    if kind == "over-strict":
        return insert_after(src, HKEY_ANCHOR,
                            "    if '_' in key or '\\n' in key or '\\r' in key or '\\0' in key:\n"
                            "        raise ValueError(\"bad header name: %r\" % key)\n").encode(), {}
    if kind == "package-shadow":
        shadow = ("def _hkey(key):\n" + RAISE_KEY.replace("    if", "    if", 1)
                  + "    return key.title().replace('_', '-')\n")
        return vuln, {"bottle/__init__.py": shadow.encode()}
    raise SystemExit("SETUP unknown bottle kind %s" % kind)


def run_solve(bwrap: str, cap: Path, app: Path, work: Path) -> None:
    script = work / "solve.sh"
    shutil.copy2(cap / "solution" / "solve.sh", script)
    cmd = sandbox(bwrap, [("--bind", str(app), "/app"), ("--ro-bind", str(script), "/solution/solve.sh")], "/app",
                  ["/usr/bin/bash", "/solution/solve.sh"])
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=CASE_TIMEOUT)
    if not (app / "report.jsonl").is_file():
        raise SystemExit("SETUP solve.sh wrote no report rc=%d %s" % (proc.returncode, proc.stderr.strip()[-200:]))


def stage(bwrap: str, case: dict, cap: Path, upstream: bytes, vuln: bytes, root: Path) -> tuple[Path, Path]:
    app = root / "app"
    tests = root / "tests"
    if root.exists():
        shutil.rmtree(root)
    app.mkdir(parents=True)
    tests.mkdir(parents=True)
    shutil.copy2(cap / "tests" / "test_outputs.py", tests / "test_outputs.py")
    report = case["report"]
    if case["bottle"] == "solve":
        (app / "bottle.py").write_bytes(vuln)
        run_solve(bwrap, cap, app, root)
        if report == "absent":
            (app / "report.jsonl").unlink()
    else:
        body, extra = bottle_variant(case["bottle"], upstream, vuln)
        (app / "bottle.py").write_bytes(body)
        for rel, data in extra.items():
            (app / rel).parent.mkdir(parents=True, exist_ok=True)
            (app / rel).write_bytes(data)
        if report == "solve":
            sol = (cap / "solution" / "solve.sh").read_text()
            start = sol.index("cat > /app/report.jsonl <<EOF\n") + len("cat > /app/report.jsonl <<EOF\n")
            (app / "report.jsonl").write_text(sol[start:sol.index("\nEOF\n", start) + 1])
    if report not in ("solve", "absent"):
        if report not in REPORTS:
            raise SystemExit("SETUP unknown report kind %s" % report)
        (app / "report.jsonl").write_text(REPORTS[report])
    return app, tests


def run_case(bwrap: str, app: Path, tests: Path, harness: Path) -> str:
    cmd = sandbox(bwrap, [("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests"),
                          ("--ro-bind", str(harness), "/harness.py")], "/app",
                  ["/usr/bin/python3", "-I", "-B", "/harness.py"])
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=CASE_TIMEOUT)
    for line in proc.stdout.splitlines():
        if line.startswith("PAYLOAD "):
            return line.split(" ", 1)[1]
    return "NOPAYLOAD(rc=%d)" % proc.returncode


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    parser.add_argument("--bwrap", default=DEFAULT_BWRAP)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    if work == lane or lane in work.parents:
        print("DEFECT SETUP --work inside the lane %s" % work)
        return 2
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
    for rel, want in PINS.items():
        p = cap / rel
        if not p.is_file() or sha(p.read_bytes()) != want:
            print("DEFECT SETUP capture sha mismatch %s" % rel)
            return 2
    table_bytes = (lane / TABLE).read_bytes()
    table = json.loads(table_bytes.decode())
    upstream = (cap / "upstream-bottle" / "bottle.py").read_bytes()
    vuln = vulnerable(upstream)
    harness = work / "harness.py"
    harness.write_text(HARNESS, encoding="utf-8")
    print(HEADER)
    print("MEMBER %s" % MEMBER)
    print("SUBJECT_SHA %s" % SUBJECT_SHA)
    print("SOLVE_SHA %s" % PINS["solution/solve.sh"])
    print("UPSTREAM_BOTTLE_SHA %s" % PINS["upstream-bottle/bottle.py"])
    print("VULNERABLE_BOTTLE_SHA %s" % sha(vuln))
    print("TOOL_SHA %s" % sha((lane / TOOL).read_bytes()))
    print("CASE_TABLE_SHA %s" % sha(table_bytes))
    print("LANE_TIP %s" % guarded(["git", "-C", str(lane), "rev-parse", "HEAD"]))
    print("HOST_PYTHON %s" % guarded(["/usr/bin/python3", "-V"]))
    print("HOST_BASH %s" % guarded(["/usr/bin/bash", "--version"]))
    print("HOST_SED %s" % guarded(["/usr/bin/sed", "--version"]))
    print("HOST_USERNS %s" % userns)
    print("LEG_ORDER %s" % ",".join(table["leg_order"]))
    print("OBSERVATIONS_BEGIN")
    mismatches = 0
    for case in table["cases"]:
        app, tests = stage(args.bwrap, case, cap, upstream, vuln, work / "cases" / case["id"])
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

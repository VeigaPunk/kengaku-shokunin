#!/usr/bin/env python3
"""Replay the captured `write-compressor` grader with its own three test functions
(round 94, R94-C1).

The reference artifact is rebuilt every run, offline, from the captured bytes: the
`main.rs` heredoc of the captured `solution/solve.sh` is compiled with the host `rustc` and
fed the captured `environment/data.txt`, exactly as solve.sh does (`cat data.txt | ./main >
data.comp`), inside a bubblewrap namespace with no network. Each case then stages a
declarative /app tree (the captured environment `decomp.c` and `data.txt`, plus one
`data.comp` variant derived deterministically from the reference artifact, or none, or the
tamper overrides) and a read-only /tests tree (the captured `test_outputs.py`,
`original-decomp.c`, `original-data.txt`), imports the captured grader unmodified and calls
its three test functions in file order with cwd /app inside a fresh namespace: tmpfs root,
host /usr and /etc read-only, the case /app bound read-write, /tests read-only, no network.
The grader's own `setup()` (copies over /app/decomp.c and /app/data.txt, runs `gcc -o
decomp2 decomp.c`) and its `cat data.comp | /app/decomp2` pipeline run unpatched.

Observed vector per case, in this order (the case table's `leg_order`):

    exists     test_compressed_file_exists:            P returned, F AssertionError,
                                                       E:<exception type name> anything else
    roundtrip  test_decompression_produces_original:   same
    size       test_compression_size:                  same
    bytes      size of /app/data.comp before grading   (`-` when absent)

No assertion is reimplemented. Every bind source lives under --work. The bwrap path is
injectable (`--bwrap`) so a sandbox-outage control runs on any host (round-92 M13).

Usage:  python3 plans/round94_compressor_probe.py --lane <repo> --work <scratch dir> [--bwrap PATH]
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

CAP = "corpus/evidence/round94/graders/write-compressor"
TABLE = "plans/round94-cases.json"
TOOL = "plans/round94_compressor_probe.py"
MEMBER = "write-compressor"
HEADER = "# tb2 write-compressor grader probe (round 94)"
PINS = {
    "tests/test_outputs.py": "809f486053e3ffbce852111dee1f63d80ab31297bd33172389e50278bed384e2",
    "tests/original-decomp.c": "7f8d9ef66943f912a217aa48f4ef5efc967b44c2b21d0f56df029b5ab413f62a",
    "tests/original-data.txt": "0fc483d0fb31128dfa41ed11adca56c88688888189826ef9daeafd7559b4fa4e",
    "solution/solve.sh": "01550b7de7ab1320b1898eae055226bb7c73bee259c75102d2240c974a730409",
    "environment/decomp.c": "7f8d9ef66943f912a217aa48f4ef5efc967b44c2b21d0f56df029b5ab413f62a",
    "environment/data.txt": "0fc483d0fb31128dfa41ed11adca56c88688888189826ef9daeafd7559b4fa4e",
}
SUBJECT_SHA = PINS["tests/test_outputs.py"]
DEFAULT_BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 600
CAT_DECOMP = "#include <stdio.h>\nint main(){int c;while((c=getchar())!=EOF)putchar(c);return 0;}\n"

HARNESS = r"""
import importlib.util, os
os.chdir("/app")
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
out = []
for name in ("test_compressed_file_exists", "test_decompression_produces_original", "test_compression_size"):
    try:
        getattr(mod, name)()
        out.append("P")
    except AssertionError:
        out.append("F")
    except BaseException as error:
        out.append("E:" + type(error).__name__)
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


def heredoc(solve: str, opener: str) -> str:
    lines = solve.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.startswith(opener))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].rstrip("\n") == "EOF")
    return "".join(lines[start + 1:end])


def sandbox(bwrap: str, binds: list[tuple[str, str, str]], chdir: str, argv: list[str]) -> list[str]:
    cmd = [bwrap, "--die-with-parent", "--unshare-all",
           "--tmpfs", "/", "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc",
           "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
           "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",
           "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
    for kind, src, dst in binds:
        cmd += [kind, src, dst]
    return cmd + ["--setenv", "PATH", "/usr/bin", "--setenv", "HOME", "/tmp", "--chdir", chdir, *argv]


def build_reference(bwrap: str, cap: Path, work: Path) -> bytes:
    ref = work / "ref"
    if ref.exists():
        shutil.rmtree(ref)
    ref.mkdir(parents=True)
    solve = (cap / "solution" / "solve.sh").read_text()
    (ref / "main.rs").write_text(heredoc(solve, "cat <<'EOF' > main.rs"))
    shutil.copy2(cap / "environment" / "data.txt", ref / "data.txt")
    script = "rustc main.rs -o main && cat data.txt | ./main > data.comp"
    proc = subprocess.run(sandbox(bwrap, [("--bind", str(ref), "/work")], "/work", ["/usr/bin/sh", "-c", script]),
                          capture_output=True, text=True, timeout=CASE_TIMEOUT)
    comp = ref / "data.comp"
    if proc.returncode != 0 or not comp.is_file():
        raise SystemExit("SETUP reference build failed rc=%d %s" % (proc.returncode, proc.stderr.strip()[-200:]))
    return comp.read_bytes()


def comp_variant(kind: str, ref: bytes, raw: bytes) -> bytes | None:
    if kind == "absent":
        return None
    if kind == "reference":
        return ref
    if kind == "raw-data":
        return raw
    if kind == "truncate-2000":
        return ref[:2000]
    if kind == "pad-300-zero":
        return ref + b"\0" * 300
    if kind == "empty":
        return b""
    if kind == "flip-byte-1000":
        return ref[:1000] + bytes([ref[1000] ^ 0xFF]) + ref[1001:]
    raise SystemExit("SETUP unknown comp kind %s" % kind)


def stage(case: dict, cap: Path, ref: bytes, root: Path) -> tuple[Path, Path, str]:
    app = root / "app"
    tests = root / "tests"
    if root.exists():
        shutil.rmtree(root)
    app.mkdir(parents=True)
    tests.mkdir(parents=True)
    for name in ("test_outputs.py", "original-decomp.c", "original-data.txt"):
        shutil.copy2(cap / "tests" / name, tests / name)
    shutil.copy2(cap / "environment" / "decomp.c", app / "decomp.c")
    shutil.copy2(cap / "environment" / "data.txt", app / "data.txt")
    tamper = case.get("tamper", "none")
    if tamper == "data-and-decomp":
        (app / "data.txt").write_text("x\n")
        (app / "decomp.c").write_text(CAT_DECOMP)
    elif tamper != "none":
        raise SystemExit("SETUP unknown tamper %s" % tamper)
    body = comp_variant(case["comp"], ref, (cap / "environment" / "data.txt").read_bytes())
    size = "-"
    if body is not None:
        (app / "data.comp").write_bytes(body)
        size = str(len(body))
    return app, tests, size


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
    ref = build_reference(args.bwrap, cap, work)
    harness = work / "harness.py"
    harness.write_text(HARNESS, encoding="utf-8")
    print(HEADER)
    print("MEMBER %s" % MEMBER)
    print("SUBJECT_SHA %s" % SUBJECT_SHA)
    print("SOLVE_SHA %s" % PINS["solution/solve.sh"])
    print("REFERENCE_COMP_SHA %s" % sha(ref))
    print("REFERENCE_COMP_BYTES %d" % len(ref))
    print("TOOL_SHA %s" % sha((lane / TOOL).read_bytes()))
    print("CASE_TABLE_SHA %s" % sha(table_bytes))
    print("LANE_TIP %s" % guarded(["git", "-C", str(lane), "rev-parse", "HEAD"]))
    print("HOST_PYTHON %s" % guarded(["/usr/bin/python3", "-V"]))
    print("HOST_GCC %s" % guarded(["/usr/bin/gcc", "--version"]))
    print("HOST_RUSTC %s" % guarded(["/usr/bin/rustc", "--version"]))
    print("HOST_USERNS %s" % userns)
    print("LEG_ORDER %s" % ",".join(table["leg_order"]))
    print("OBSERVATIONS_BEGIN")
    mismatches = 0
    for case in table["cases"]:
        app, tests, size = stage(case, cap, ref, work / "cases" / case["id"])
        observed = "%s,%s" % (run_case(args.bwrap, app, tests, harness), size)
        ok = observed == case["predicted"]
        mismatches += 0 if ok else 1
        print("CASE %s predicted=%s observed=%s ok=%s" % (case["id"], case["predicted"], observed, ok))
    print("OBSERVATIONS_END")
    print("mismatches %d" % mismatches)
    shutil.rmtree(work / "cases", ignore_errors=True)
    shutil.rmtree(work / "ref", ignore_errors=True)
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Replay the captured `financial-document-processor` grader with its own seven test functions and its
own pytest reward rule (round 100, R100-C1).

The task image (captured `Dockerfile`) is ubuntu:24.04 + uv; `/app/documents/` holds 17 JPG/PDF files
whose names `randomize_filenames.py` replaces with `secrets.token_urlsafe(9)` at build. The grader
identifies every file by sha512, so the probe stages the 17 captured documents under their captured
names. The verifier (`test.sh`) runs `/tests/test_outputs.py` under
`uvx -p 3.13 -w pytest==8.4.1 -w pandas==2.3.2 -w pytest-json-ctrf==0.3.5` and writes reward 1 iff
pytest exits 0. This probe models the verifier side with one pre-staged virtual environment:

    --grader-venv  python 3.13.x, pytest 8.4.1, pandas 2.3.2, pytest-json-ctrf 0.3.5

numpy arrives unpinned with pandas; its version is printed (GRADER_UNPINNED), not refused.

Positive control: the maintainer's `solve.sh` (a pytesseract/PyMuPDF classifier) was run once at P0
(2026-11-06, host tesseract 5.5.3 in place of apt's 5.3.4, the solve.sh PEP 723 pins, offline
bubblewrap). Its placement (`placement.tsv`: directory, name, sha256 per document), its summary.csv
and its per-invoice JSON sidecars are committed under `corpus/evidence/round100/fdp-solution/` with
SHA256SUMS; the probe stages those bytes.

Every sandboxed step runs in a fresh bubblewrap namespace with --unshare-all (no network) and
--clearenv, tmpfs root, host /usr read-only, the venv and its interpreter read-only, the case /app
read-write, the captured test file read-only at /tests and the fixture read-only at /fixture. The
sandbox binary is fixed at /usr/bin/bwrap.

Each case's /app starts as the image state (the 17 documents in /app/documents) and is then edited
inside the sandbox by BUILDER for the case kind (deterministic, no randomness). The grader runs ONCE
per case as real pytest (`pytest.main`) over the unmodified captured file; an observe-only plugin
records each test's outcome and `call.excinfo.typename`:

    P passed, F AssertionError, E:<exception type name> any other failure; reward 1 iff pytest rc 0

No assertion is reimplemented. Output order is the case table order.

Usage:  python3 plans/round100_fdp_probe.py --lane <repo> --work <scratch dir> --grader-venv <dir> [--jobs N]
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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CAP = "corpus/evidence/round100/tb2-financial-document-processor"
FIX = "corpus/evidence/round100/fdp-solution"
TABLE = "plans/round100-cases.json"
TOOL = "plans/round100_fdp_probe.py"
MEMBER = "financial-document-processor"
HEADER = "# tb2 financial-document-processor grader probe (round 100)"
PINS = {
    "test_outputs.py": "978f506ad5c1bfaf28f9bc774dfe4347d33d046ca009b8496eb513956b7f5a9a",
    "test.sh": "48abbda713ace5cee00dd28c7398959f28280062350eb88206a6697a28c72790",
    "solve.sh": "90861b79c4bd7733909616ffa058151847eb67a4d43395a964c449cf7e24c4fb",
    "Dockerfile": "2ea485aead008998d7a551e8c80b6bd354a74cbffc310a1f4b88d0b7c53d23ff",
    "task.toml": "163ee252895c05d36ca37137dba4d6c24b46be28d56ce84ef8bb35bb5b894bda",
    "instruction.md": "b21cf2af1891922732327bf586d14b250d36d96de7867479c15bd1c58ef0db58",
    "README.md": "32438e7780d235dd609f4740e36512c4cd2f34ef26842ea52c5bbde46fcf5e86",
    "randomize_filenames.py": "09828ee53e8f2165a9888c5de84e40fcb057bb889d93bfc90d9aeca8c4e23be4",
    "SHA256SUMS": "0a137bdb179c5d4e9056565e8fa18725bf94f56b43fa78547db888bb1cb46fa3",
}
FIX_PINS = {
    "placement.tsv": "32518f87d43be98e862086e6dd847538b3d2800ad9f083ff3994826a1fb48209",
    "summary.csv": "08724ad988ea1fe13804ddaf85da9b3731289ac5b9a9e730117b9134c3e977b2",
    "document_processor.py": "db4f841e7dc0b3c846fc1e37f37ee3a0e28f3601b055afa1fec00b269e8d937a",
    "SHA256SUMS": "97fbf7930b838bc28556a67ba296b131660b8d1e18272b288c169e9a5183ed6f",
}
SUBJECT_SHA = PINS["test_outputs.py"]
BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 1800
GRADER_WANT = ("3.13", "8.4.1", "2.3.2", "0.3.5")   # test.sh uvx pins: -p 3.13, pytest, pandas, pytest-json-ctrf
TESTS = ("test_directories_created", "test_invoices_moved_correctly", "test_other_documents_moved_correctly",
         "test_summary_csv_exists", "test_summary_csv_structure", "test_summary_csv_content",
         "test_original_documents_dir_empty")
KINDS = ("solution", "absent", "all-total-rows", "one-invoice-repeated", "json-in-invoices",
         "txt-in-invoices", "documents-subdir", "duplicate-copy", "misclassified-one", "vat-zero",
         "total-plus-0.009", "total-plus-0.01", "no-summary", "headers-reordered", "bom-header")

BUILDER = r"""
import csv, io, os, shutil, sys
kind = sys.argv[1]
fx = "/fixture/solution/"
DOCS = "/app/documents/"
rows = list(csv.reader(open(fx + "summary.csv", newline="")))
header, body = rows[0], rows[1:]
placement = [l.rstrip("\n").split("\t") for l in open(fx + "placement.tsv") if l.strip()]
first_invoice = sorted(name for d, name, _ in placement if d == "invoices")[0]

def place(skip=None, to_other=None):
    os.makedirs("/app/invoices", exist_ok=True)
    os.makedirs("/app/other", exist_ok=True)
    for d, name, _ in placement:
        if name == skip:
            continue
        dest = "other" if name == to_other else d
        shutil.move(DOCS + name, "/app/%s/%s" % (dest, name))
    for j in sorted(os.listdir(fx + "invoices-json")):
        if to_other and j == to_other.rsplit(".", 1)[0] + ".json":
            continue
        shutil.copyfile(fx + "invoices-json/" + j, "/app/invoices/" + j)

def write_summary(table, prefix=""):
    buf = io.StringIO()
    csv.writer(buf).writerows(table)
    with open("/app/invoices/summary.csv", "w", newline="", encoding="utf-8") as f:
        f.write(prefix + buf.getvalue())

if kind == "absent":
    pass
elif kind == "solution":
    place()
    shutil.copyfile(fx + "summary.csv", "/app/invoices/summary.csv")
elif kind == "all-total-rows":
    place()
    total = [r for r in body if r[0] == "total"]
    assert len(total) == 1
    write_summary([header] + total * 11)
elif kind == "one-invoice-repeated":
    place()
    inv = [r for r in body if r[0] == first_invoice]
    total = [r for r in body if r[0] == "total"]
    assert len(inv) == 1 and len(total) == 1
    write_summary([header] + inv * 10 + total)
elif kind == "json-in-invoices":
    place()
    shutil.copyfile(fx + "summary.csv", "/app/invoices/summary.csv")
    open("/app/invoices/notes.json", "w").write("{}\n")
elif kind == "txt-in-invoices":
    place()
    shutil.copyfile(fx + "summary.csv", "/app/invoices/summary.csv")
    open("/app/invoices/notes.txt", "w").write("notes\n")
elif kind == "documents-subdir":
    os.makedirs(DOCS + "keep")
    for d, name, _ in placement:
        shutil.copyfile(DOCS + name, DOCS + "keep/" + name)
    place()
    shutil.copyfile(fx + "summary.csv", "/app/invoices/summary.csv")
elif kind == "duplicate-copy":
    place()
    shutil.copyfile(fx + "summary.csv", "/app/invoices/summary.csv")
    shutil.copyfile("/app/invoices/" + first_invoice, "/app/invoices/copy-" + first_invoice)
elif kind == "misclassified-one":
    place(to_other=first_invoice)
    kept = [r for r in body if r[0] not in (first_invoice, "total")]
    total = [r for r in body if r[0] == "total"]
    assert len(kept) == 9 and len(total) == 1
    write_summary([header] + kept + total)
elif kind == "vat-zero":
    place()
    write_summary([header] + [[r[0], r[1], r[2] if r[2] != "" else "0"] for r in body])
elif kind in ("total-plus-0.009", "total-plus-0.01"):
    place()
    new = "6204.199" if kind == "total-plus-0.009" else "6204.2"
    hit = [r for r in body if r[1] == "6204.19"]
    assert len(hit) == 1
    write_summary([header] + [[r[0], new if r[1] == "6204.19" else r[1], r[2]] for r in body])
elif kind == "no-summary":
    place()
elif kind == "headers-reordered":
    place()
    write_summary([[header[0], header[2], header[1]]] + [[r[0], r[2], r[1]] for r in body])
elif kind == "bom-header":
    place()
    write_summary([header] + body, prefix="\ufeff")
else:
    raise SystemExit("unknown kind " + kind)
print("BUILT", kind)
"""

VERSIONS = ("import sys, importlib.metadata as m\n"
            "print('VERSIONS', sys.version.split()[0], m.version('pytest'), m.version('pandas'), "
            "m.version('pytest-json-ctrf'), m.version('numpy'))\n")
RUNNER = r"""
import sys
import pytest
verdict = {}
class Observe:
    # observes only: records each test's outcome and exception type name
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        rep = outcome.get_result()
        if rep.when == "call" or (rep.when != "call" and rep.failed):
            if rep.passed:
                verdict[item.name] = "P"
            elif call.excinfo is not None:
                name = call.excinfo.typename
                verdict[item.name] = "F" if name == "AssertionError" else "E:" + name
            else:
                verdict[item.name] = "E:" + rep.outcome
rc = int(pytest.main(["-q", "-p", "no:cacheprovider", "/tests/test_outputs.py"], plugins=[Observe()]))
for name in %r:
    print("VERDICT", name, verdict.get(name, "MISSING"))
print("RC", rc)
sys.exit(rc)
""" % (TESTS,)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def guarded(args: list[str]) -> str:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return "absent"
    text = (proc.stdout or proc.stderr).strip()
    return text.splitlines()[0] if text else "absent"


class Box:
    """One sandbox recipe: the read-only interpreter/venv binds shared by every run."""

    def __init__(self, ro_trees: list[str]):
        self.ro_trees = ro_trees

    def cmd(self, binds: list[tuple[str, str, str]], chdir: str, path: str, argv: list[str]) -> list[str]:
        cmd = [BWRAP, "--die-with-parent", "--unshare-all", "--clearenv",
               "--tmpfs", "/", "--ro-bind", "/usr", "/usr",
               "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
               "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",
               "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
        for tree in self.ro_trees:
            cmd += ["--ro-bind", tree, tree]
        for kind, src, dst in binds:
            cmd += [kind, src, dst]
        return cmd + ["--setenv", "PATH", path, "--setenv", "HOME", "/tmp",
                      "--setenv", "LANG", "C.UTF-8", "--setenv", "OMP_NUM_THREADS", "1",
                      "--chdir", chdir, *argv]

    def run(self, binds, chdir, path, argv) -> subprocess.CompletedProcess:
        return subprocess.run(self.cmd(binds, chdir, path, argv), capture_output=True, text=True,
                              timeout=CASE_TIMEOUT)


def venv_python(venv: Path) -> Path:
    return venv / "bin" / "python"


def interpreter_root(venv: Path) -> str:
    real = venv_python(venv).resolve()
    return str(real.parent.parent.parent)


def check_venv(box: Box, venv: Path, scratch: Path) -> tuple[str, str]:
    probe = scratch / "versions.py"
    probe.write_text(VERSIONS, encoding="utf-8")
    proc = box.run([("--ro-bind", str(probe), "/versions.py")], "/tmp", "%s/bin:/usr/bin" % venv,
                   [str(venv_python(venv)), "-I", "-B", "/versions.py"])
    line = next((x for x in proc.stdout.splitlines() if x.startswith("VERSIONS ")), "")
    parts = line.split()
    if (len(parts) != 6 or ".".join(parts[1].split(".")[:2]) != GRADER_WANT[0]
            or tuple(parts[2:5]) != GRADER_WANT[1:]):
        raise SystemExit("SETUP venv %s versions %r rc=%d %s" % (venv, line, proc.returncode,
                                                                   proc.stderr.strip()[-200:]))
    return "%s %s %s %s" % GRADER_WANT, "python %s numpy %s" % (parts[1], parts[5])


def verify_sums(base: Path) -> bool:
    """Every SHA256SUMS line hashes to its file, and every regular file except SHA256SUMS is listed."""
    listed = {}
    for line in (base / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, _, rel = line.partition("  ")
        listed[rel[2:] if rel.startswith("./") else rel] = digest
    present = {str(p.relative_to(base)) for p in base.rglob("*") if p.is_file() and p.name != "SHA256SUMS"}
    return set(listed) == present and all(sha((base / r).read_bytes()) == d for r, d in listed.items())


def stage(box: Box, case: dict, root: Path, venv: Path, fixture: Path, builder: Path) -> Path:
    kind = case["app"]
    if kind not in KINDS:
        raise SystemExit("SETUP unknown app kind %s" % kind)
    if root.exists():
        shutil.rmtree(root)
    app = root / "app"
    (app / "documents").mkdir(parents=True)
    for doc in sorted((fixture / "documents").iterdir()):   # the image state: 17 documents
        shutil.copyfile(doc, app / "documents" / doc.name)
    proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(fixture), "/fixture"),
                    ("--ro-bind", str(builder), "/builder.py")], "/app", "%s/bin:/usr/bin" % venv,
                   [str(venv_python(venv)), "-I", "-B", "/builder.py", kind])
    if proc.returncode != 0 or ("BUILT %s" % kind) not in proc.stdout:
        raise SystemExit("SETUP builder %s rc=%d %s" % (kind, proc.returncode, proc.stderr.strip()[-300:]))
    return app


def run_case(box: Box, app: Path, tests: Path, venv: Path, runner: Path) -> str:
    proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests"),
                    ("--ro-bind", str(runner), "/runner.py")], "/app",
                   "%s/bin:/usr/bin" % venv, [str(venv_python(venv)), "-I", "-B", "/runner.py"])
    verdict: dict[str, str] = {}
    rc = None
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[0] == "VERDICT":
            verdict[parts[1]] = parts[2]
        elif len(parts) == 2 and parts[0] == "RC" and parts[1].lstrip("-").isdigit():
            rc = int(parts[1])
    out = [verdict.get(name, "MISSING") for name in TESTS]
    out.append("1" if rc == 0 and proc.returncode == 0 else "0" if rc is not None else "NORC(%d)" % proc.returncode)
    return ",".join(out)


def detail(app: Path) -> str:
    """Directory census of the graded /app: file counts and the summary's sha256 prefix."""
    parts = []
    for name in ("documents", "invoices", "other"):
        d = app / name
        if d.is_dir():
            files = sum(1 for p in d.rglob("*") if p.is_file())
            parts.append("%s=%d" % (name, files))
        else:
            parts.append("%s=absent" % name)
    s = app / "invoices" / "summary.csv"
    parts.append("summary=%s" % (sha(s.read_bytes())[:16] if s.is_file() else "absent"))
    return " ".join(parts)


def one(box, case, work, venv, fixture, tests, builder, runner) -> tuple[str, str]:
    root = work / "cases" / case["id"]
    try:
        app = stage(box, case, root, venv, fixture, builder)
        observed = run_case(box, app, tests, venv, runner)
        info = detail(app)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return observed, info


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    parser.add_argument("--grader-venv", required=True)
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    grader_venv = Path(args.grader_venv).resolve()
    for p in (work, grader_venv):
        if p == lane or lane in p.parents:
            print("DEFECT SETUP path inside the lane %s" % p)
            return 2
    if args.jobs < 1:
        print("DEFECT SETUP --jobs must be >= 1")
        return 2
    work.mkdir(parents=True, exist_ok=True)
    cap = lane / CAP
    fixture = lane / FIX
    if not Path(BWRAP).is_file() or not os.access(BWRAP, os.X_OK):
        print("DEFECT SETUP sandbox-unavailable %s" % BWRAP)
        return 2
    try:
        userns = Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    except OSError:
        userns = "absent"
    if not userns.isdigit() or int(userns) <= 0:
        print("DEFECT SETUP user namespaces unavailable (%s)" % userns)
        return 2
    for base, pins in ((cap, PINS), (fixture, FIX_PINS)):
        for rel, want in pins.items():
            p = base / rel
            if not p.is_file() or sha(p.read_bytes()) != want:
                print("DEFECT SETUP capture sha mismatch %s/%s" % (base.name, rel))
                return 2
        if not verify_sums(base):
            print("DEFECT SETUP SHA256SUMS does not cover %s exactly" % base.name)
            return 2
    if not venv_python(grader_venv).exists():
        print("DEFECT SETUP venv python absent %s" % grader_venv)
        return 2
    table_bytes = (lane / TABLE).read_bytes()
    table = json.loads(table_bytes.decode())
    box = Box(sorted({str(grader_venv), interpreter_root(grader_venv)}))
    try:
        pinned, unpinned = check_venv(box, grader_venv, work)
    except SystemExit as error:
        print("DEFECT %s" % error)
        return 2
    builder = work / "builder.py"
    builder.write_text(BUILDER, encoding="utf-8")
    runner = work / "runner.py"
    runner.write_text(RUNNER, encoding="utf-8")
    tests = work / "tests"
    if tests.exists():
        shutil.rmtree(tests)
    tests.mkdir()
    shutil.copyfile(cap / "test_outputs.py", tests / "test_outputs.py")
    fix = work / "fixture"
    if fix.exists():
        shutil.rmtree(fix)
    shutil.copytree(cap / "documents", fix / "documents")
    shutil.copytree(fixture, fix / "solution")
    print(HEADER)
    print("MEMBER %s" % MEMBER)
    print("SUBJECT_SHA %s" % SUBJECT_SHA)
    print("TEST_SH_SHA %s" % PINS["test.sh"])
    print("SOLVE_SHA %s" % PINS["solve.sh"])
    print("CAPTURE_SUMS_SHA %s" % PINS["SHA256SUMS"])
    print("FIXTURE_SUMS_SHA %s" % FIX_PINS["SHA256SUMS"])
    print("TOOL_SHA %s" % sha((lane / TOOL).read_bytes()))
    print("CASE_TABLE_SHA %s" % sha(table_bytes))
    print("LANE_TIP %s" % guarded(["git", "-C", str(lane), "rev-parse", "HEAD"]))
    print("GRADER_SIDE python,pytest,pandas,pytest-json-ctrf %s" % pinned)
    print("GRADER_UNPINNED %s" % unpinned)
    print("HOST_BASH %s" % guarded(["/usr/bin/bash", "--version"]))
    print("HOST_USERNS %s" % userns)
    print("SANDBOX clearenv=1 unshare-all=1 etc-bound=0 bwrap=%s" % BWRAP)
    print("LEG_ORDER %s" % ",".join(table["leg_order"]))
    sys.stdout.flush()
    cases = table["cases"]
    try:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(one, box, c, work, grader_venv, fix, tests, builder, runner) for c in cases]
            results = [f.result() for f in futures]
    except SystemExit as error:
        print("DEFECT %s" % error)
        return 2
    finally:
        shutil.rmtree(work / "cases", ignore_errors=True)
        shutil.rmtree(fix, ignore_errors=True)
    print("OBSERVATIONS_BEGIN")
    mismatches = 0
    for case, (observed, info) in zip(cases, results):
        ok = observed == case["predicted"]
        mismatches += 0 if ok else 1
        print("CASE %s predicted=%s observed=%s ok=%s" % (case["id"], case["predicted"], observed, ok))
        print("DETAIL %s %s %s" % (case["id"], info, case["app"]))
    print("OBSERVATIONS_END")
    print("mismatches %d" % mismatches)
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

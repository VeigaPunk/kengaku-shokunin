#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `torch-pipeline-parallelism` grader (round 67, R67-C1).

Runs the grader's own pytest module -- never a copy, never a rewrite -- once per frozen case inside a
bubblewrap sandbox: /app is the case directory (its `pipeline_parallel.py`, or an empty directory for
q2-none), /tests/test_outputs.py is the byte-pinned grader, and the network namespace and PID namespace
are unshared. Each case yields four outcomes, in KEYS order:

    exists     test_pipeline_parallel_exists
    no_hooks   test_no_hooks_in_pipeline_parallel
    ws1        test_pipeline_parallel[1]   (world size 1, gloo on 127.0.0.1:12355)
    ws2        test_pipeline_parallel[2]   (world size 2, gloo on 127.0.0.1:12355)

Leg rule (frozen): P iff the junit testcase has no failure/error child; F otherwise.

Grader under execution (lane capture, byte-verified at run time and at every check):
    corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py
    sha256 23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f
    (corpus/evidence/round52/graders/SHA256SUMS line 169)

Frozen table (plans/round-67-claims.md, R67-C1), vector order exists/no_hooks/ws1/ws2:

    q1-ref            PPPP   reference AFAB implementation
    q2-none           FFFF   do-nothing control (no /app/pipeline_parallel.py)
    q3-stub           PPFF   stub that raises NotImplementedError in train_step_pipeline_afab
    q4-hooks-noop     PFPP   correct numerics plus a no-op forward hook (the literal is in the code)
    q5-full-model     PPPF   no partition: every rank runs all layers (layer-count assertion fails at ws2)
    q6-unscaled-loss  PPFF   correct schedule, loss not divided by the microbatch count

Amendment A1 (plans/round-67-claims.md, dated 2026-11-03): the counter now enforces the frozen predicate
sentence as written -- exactly one CASE and one VECTOR line per frozen case, no duplicate, unknown or
malformed line, a VECTOR line before its CASE line is bound the same way, the frozen label must agree with
the vector, the CASE rc must equal pytest's exit status for the junit outcomes (0 iff all four legs P), the
GRADER line is matched whole, and an unreadable junit is a named finding. The run refuses to overwrite an
existing receipt. The frozen table, cases and kill rules are unchanged.

Setup failures (grader sha drift, missing venv, port 12355 busy, bwrap refusal, missing junit, timeout)
are SETUP, exit 2 (could-not-evaluate), never a verdict.

The junit bytes of a receipt live beside it at <receipt-stem>.junit/<case>.xml, so a later run never
overwrites an earlier receipt's bytes.

Usage:
    python3 plans/round67_c1_pipeline_probe.py --run --receipt <path> --work <scratch>
    python3 plans/round67_c1_pipeline_probe.py --check-receipt <receipt>
    python3 plans/round67_c1_pipeline_probe.py --selftest --work <scratch>

Exit: 0 pass, 1 predicate failed, 2 could-not-evaluate. Scratch is taken from --work only; nothing is
written under /tmp by this file.
"""

import argparse
import fcntl
import hashlib
import re
import shutil
import socket
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PROBE_VERSION = "r67-c1/1"
LANE = Path(__file__).resolve().parents[1]
GRADER_REL = "corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py"
GRADER = LANE / GRADER_REL
GRADER_SHA256 = "23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f"
CASES_DIR = LANE / "corpus/evidence/round67/pipe/cases"
RECORD_RECEIPT = LANE / "corpus/evidence/round67/pipe/receipt.txt"
VENV_ROOT = Path.home() / ".local/share/kengaku-r67/venv-pipe"
VENV_PY = VENV_ROOT / "bin/python"
LOCK = Path.home() / ".local/share/kengaku-r67/port-12355.lock"
PORT = 12355
CASE_FILE = "pipeline_parallel.py"

CASES = ["q1-ref", "q2-none", "q3-stub", "q4-hooks-noop", "q5-full-model", "q6-unscaled-loss"]
KEYS = ["exists", "no_hooks", "ws1", "ws2"]
FROZEN_TABLE = {
    "q1-ref": "PPPP",
    "q2-none": "FFFF",
    "q3-stub": "PPFF",
    "q4-hooks-noop": "PFPP",
    "q5-full-model": "PPPF",
    "q6-unscaled-loss": "PPFF",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_sha() -> str:
    return sha256(Path(__file__).resolve())


def junit_dir_for(receipt: Path) -> Path:
    return receipt.parent / (receipt.stem + ".junit")


def key_of(testname: str) -> str:
    if testname == "test_pipeline_parallel_exists":
        return "exists"
    if testname == "test_no_hooks_in_pipeline_parallel":
        return "no_hooks"
    m = re.fullmatch(r"test_pipeline_parallel\[(\d+)\]", testname or "")
    if not m or m.group(1) not in ("1", "2"):
        raise ValueError(f"unexpected testcase name: {testname}")
    return f"ws{m.group(1)}"


def junit_outcomes(junit: Path) -> dict:
    """Return {key: P|F} from a junit file; raises ValueError or ET.ParseError on unreadable input."""
    tree = ET.parse(junit)
    outcomes = {}
    for tc in tree.iter("testcase"):
        k = key_of(tc.get("name"))
        bad = [c for c in tc if c.tag in ("failure", "error")]
        outcomes[k] = "F" if bad else "P"
    return outcomes


def vector_of(outcomes: dict) -> str:
    return "".join(outcomes.get(k, "?") for k in KEYS)


def port_busy() -> bool:
    s = socket.socket()
    s.settimeout(0.5)
    try:
        return s.connect_ex(("127.0.0.1", PORT)) == 0
    finally:
        s.close()


def setup_error(msg: str) -> int:
    print(f"SETUP {msg}")
    print("PREDICATE R67-C1 could-not-evaluate")
    return 2


def case_app_dir(case: str, work: Path) -> Path:
    d = CASES_DIR / case
    if d.is_dir():
        return d
    empty = work / "empty-app" / case
    shutil.rmtree(empty, ignore_errors=True)
    empty.mkdir(parents=True)
    return empty


def run_case(case: str, work: Path) -> dict:
    app = case_app_dir(case, work)
    ctl = work / "ctl" / case
    shutil.rmtree(ctl, ignore_errors=True)
    ctl.mkdir(parents=True)
    cmd = [
        "bwrap", "--die-with-parent", "--unshare-net", "--unshare-pid",
        "--ro-bind", "/usr", "/usr",
        "--symlink", "usr/bin", "/bin",
        "--symlink", "usr/sbin", "/sbin",
        "--symlink", "usr/lib", "/lib",
        "--symlink", "usr/lib64", "/lib64",
        "--ro-bind", "/etc", "/etc",
        "--proc", "/proc",
        "--dev", "/dev",
        "--tmpfs", "/tmp",
        "--ro-bind", str(VENV_ROOT), str(VENV_ROOT),
        "--dir", "/app", "--ro-bind", str(app), "/app",
        "--dir", "/tests", "--ro-bind", str(GRADER), "/tests/test_outputs.py",
        "--bind", str(ctl), "/ctl",
        "--chdir", "/app",
        "--clearenv",
        "--setenv", "PATH", "/usr/bin:/bin",
        "--setenv", "HOME", "/tmp",
        "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
        "--setenv", "PYTHONNOUSERSITE", "1",
        "--setenv", "HF_HUB_OFFLINE", "1",
        "--setenv", "TRANSFORMERS_OFFLINE", "1",
        str(VENV_PY), "-m", "pytest", "/tests/test_outputs.py",
        "-p", "no:cacheprovider", "-q", "--junitxml=/ctl/junit.xml",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return {"case": case, "error": "timeout"}
    junit = ctl / "junit.xml"
    if not junit.exists():
        return {"case": case, "error": "no junit", "rc": proc.returncode,
                "tail": (proc.stdout + proc.stderr)[-600:]}
    try:
        outcomes = junit_outcomes(junit)
    except (ValueError, ET.ParseError) as e:
        return {"case": case, "error": f"junit unreadable: {e}"}
    return {
        "case": case,
        "rc": proc.returncode,
        "outcomes": outcomes,
        "junit": junit,
        "case_sha": sha256(app / CASE_FILE) if (app / CASE_FILE).exists() else "none",
        "junit_sha": sha256(junit),
    }


def run(receipt: Path, work: Path) -> int:
    if receipt.exists():
        return setup_error(f"receipt exists, refusing to overwrite: {receipt}")
    if not GRADER.exists() or sha256(GRADER) != GRADER_SHA256:
        return setup_error("grader sha drift or missing grader")
    if not VENV_PY.exists():
        return setup_error(f"missing venv {VENV_PY}")
    if not Path("/usr/bin/bwrap").exists():
        return setup_error("missing bwrap")
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    results = []
    with open(LOCK, "w") as lockf:
        fcntl.flock(lockf, fcntl.LOCK_EX)
        if port_busy():
            return setup_error(f"port {PORT} busy")
        for c in CASES:
            r = run_case(c, work)
            if "error" in r:
                return setup_error(f"case {r['case']}: {r['error']}")
            results.append(r)
    jdir = junit_dir_for(receipt)
    shutil.rmtree(jdir, ignore_errors=True)
    jdir.mkdir(parents=True)
    lines = [
        "# R67-C1 receipt -- TB2 torch-pipeline-parallelism grader offline under bwrap",
        f"# instrument plans/round67_c1_pipeline_probe.py version={PROBE_VERSION}",
        f"PROBE sha256={probe_sha()} version={PROBE_VERSION}",
        f"GRADER sha256={GRADER_SHA256} path={GRADER_REL}",
        "VENV torch=2.15.0+cpu transformers=5.22.1 pytest=9.2.0 python=3.14.8 install=uv-pip-pypi+pytorch-cpu",
    ]
    for r in results:
        dst = jdir / f"{r['case']}.xml"
        shutil.copyfile(r["junit"], dst)
        lines.append(
            f"CASE {r['case']} case_sha256={r['case_sha']} junit_sha256={sha256(dst)} rc={r['rc']}"
        )
        vec = vector_of(r["outcomes"])
        frozen = FROZEN_TABLE[r["case"]]
        lines.append(
            f"VECTOR {r['case']} " + " ".join(f"{k}={v}" for k, v in zip(KEYS, vec))
            + f" frozen={'match' if vec == frozen else 'mismatch'}"
        )
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text("\n".join(lines) + "\n")
    return check_receipt(receipt)


def check_receipt(path: Path) -> int:
    """Re-derive every checkable field of a receipt from committed bytes; return 0/1/2."""
    findings = []
    try:
        text = path.read_text()
    except OSError as e:
        return setup_error(f"cannot read receipt: {e}")
    lines = text.splitlines()
    jdir = junit_dir_for(path)
    probe_line = [l for l in lines if l.startswith("PROBE ")]
    if len(probe_line) != 1:
        findings.append("defect: PROBE line count != 1")
    else:
        m = re.fullmatch(r"PROBE sha256=([0-9a-f]{64}) version=(\S+)", probe_line[0])
        if not m:
            findings.append("defect: malformed PROBE line")
        else:
            if m.group(1) != probe_sha():
                findings.append("defect: PROBE sha does not match committed probe bytes")
            if m.group(2) != PROBE_VERSION:
                findings.append("defect: PROBE version does not match the probe")
    grader_line = [l for l in lines if l.startswith("GRADER ")]
    gm = re.fullmatch(r"GRADER sha256=([0-9a-f]{64}) path=(\S+)", grader_line[0]) if len(grader_line) == 1 else None
    if gm is None or gm.group(1) != GRADER_SHA256 or gm.group(2) != GRADER_REL:
        findings.append("defect: GRADER line missing, malformed or not the pinned sha/path")
    if not GRADER.exists() or sha256(GRADER) != GRADER_SHA256:
        findings.append("defect: committed grader bytes do not match the pinned sha")

    case_lines = {}
    for l in lines:
        if not l.startswith("CASE "):
            continue
        m = re.fullmatch(r"CASE (\S+) case_sha256=(\S+) junit_sha256=([0-9a-f]{64}) rc=(-?\d+)", l)
        if not m:
            findings.append(f"defect: malformed CASE line: {l[:80]}")
            continue
        case = m.group(1)
        if case not in FROZEN_TABLE:
            findings.append(f"defect: unknown case {case} in CASE line")
            continue
        if case in case_lines:
            findings.append(f"defect: duplicate CASE line for {case}")
            continue
        case_lines[case] = (m.group(2), m.group(3), int(m.group(4)))

    vector_lines = {}
    for l in lines:
        if not l.startswith("VECTOR "):
            continue
        m = re.fullmatch(r"VECTOR (\S+) " + " ".join(f"{k}=([PF])" for k in KEYS) + r" frozen=(match|mismatch)", l)
        if not m:
            findings.append(f"defect: malformed VECTOR line: {l[:80]}")
            continue
        case = m.group(1)
        if case not in FROZEN_TABLE:
            findings.append(f"defect: unknown case {case} in VECTOR line")
            continue
        if case in vector_lines:
            findings.append(f"defect: duplicate VECTOR line for {case}")
            continue
        vec = "".join(m.group(i + 2) for i in range(len(KEYS)))
        vector_lines[case] = (vec, m.group(len(KEYS) + 2))

    for case in CASES:
        if case not in case_lines or case not in vector_lines:
            findings.append(f"defect: missing CASE or VECTOR line for {case}")
            continue
        vec, label = vector_lines[case]
        case_sha, junit_sha, rc = case_lines[case]
        if vec != FROZEN_TABLE[case]:
            findings.append(f"defect: {case} vector {vec} != frozen {FROZEN_TABLE[case]}")
        if (label == "match") != (vec == FROZEN_TABLE[case]):
            findings.append(f"defect: {case} frozen label {label} contradicts vector {vec}")
        want_rc = 0 if vec == "PPPP" else 1
        if rc != want_rc:
            findings.append(f"defect: {case} rc={rc} is not the pytest status for vector {vec} (want {want_rc})")
        jx = jdir / f"{case}.xml"
        if not jx.exists():
            findings.append(f"defect: junit missing for {case}")
            continue
        if sha256(jx) != junit_sha:
            findings.append(f"defect: junit sha mismatch for {case}")
        try:
            derived = vector_of(junit_outcomes(jx))
        except (ValueError, ET.ParseError) as e:
            findings.append(f"defect: junit unreadable for {case}: {e}")
        else:
            if derived != vec:
                findings.append(f"defect: VECTOR {case} {vec} disagrees with its junit {derived}")
        app = CASES_DIR / case / CASE_FILE
        want = sha256(app) if app.exists() else "none"
        if case_sha != want:
            findings.append(f"defect: case_sha mismatch for {case}")

    for f in findings:
        print(f"CHECK {f}")
    ok = not findings
    print(f"CHECK ok cases={len(case_lines)}" if ok else f"CHECK findings={len(findings)}")
    print(f"PREDICATE R67-C1 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def selftest(work: Path) -> int:
    base = RECORD_RECEIPT
    if not base.exists():
        return setup_error("no committed receipt for selftest")
    red = work / "selftest" / "receipt.txt"
    shutil.rmtree(red.parent, ignore_errors=True)
    red.parent.mkdir(parents=True)
    shutil.copytree(junit_dir_for(base), red.parent / "receipt.junit")
    text = base.read_text()
    flipped = re.sub(r"VECTOR q1-ref exists=P", "VECTOR q1-ref exists=F", text, count=1)
    red.write_text(flipped)
    rc_green = check_receipt(base)
    rc_red = check_receipt(red)
    ok = rc_green == 0 and rc_red == 1
    print(f"SELFTEST green_rc={rc_green} red_rc={rc_red} {'ok' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--receipt", type=Path, default=RECORD_RECEIPT)
    ap.add_argument("--check-receipt", type=Path)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", type=Path)
    args = ap.parse_args(argv)
    if args.check_receipt:
        return check_receipt(args.check_receipt)
    if args.work is None and (args.run or args.selftest):
        print("usage: --work <scratch dir> is required (scratch is never /tmp)")
        return 2
    if args.run:
        return run(args.receipt, args.work)
    if args.selftest:
        return selftest(args.work)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

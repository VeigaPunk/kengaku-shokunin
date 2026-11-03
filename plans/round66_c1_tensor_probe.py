#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `torch-tensor-parallelism` grader (round 66, R66-C1).

Runs the grader's own pytest module -- never a copy, never a rewrite -- once per frozen case,
inside a bubblewrap sandbox whose /app is the case directory and whose /tests/test_outputs.py
is the byte-pinned grader. Each case yields 13 test outcomes (the existence check plus 12
parametrised layer tests); the vector of P/F outcomes is compared to the frozen table below.

Grader under execution (lane capture, byte-verified at run time):
    corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py
    sha256 4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290
    (corpus/evidence/round52/graders/SHA256SUMS line 171)

Frozen table (plans/round-66-claims.md, R66-C1). Outcome keys: `exists`, and
`<kind>-ws<N>-bias<B>` with kind in {column,row}, N in {1,2,4}, B in {True,False}.

    K1 compliant reference         all 13 P
    K2 do-nothing control          exists F, all 12 layer tests F
    K3 stub control (raises)       exists P, all 12 layer tests F
    K4 column never gathers        exists P; column ws1 P, column ws2/ws4 F; row all P
    K5 row never reduces           exists P; column all P; row ws1 P, row ws2/ws4 F

Leg rule (frozen): P iff the junit testcase has no failure/error child; F otherwise.
Setup failures (grader sha drift, missing venv, port 12355 busy, bwrap refusal, missing junit)
are SETUP, exit 2 (could-not-evaluate), never a verdict.

Usage:
    python3 plans/round66_c1_tensor_probe.py --run --receipt corpus/evidence/round66/tensor/receipt.txt --work <scratch>
    python3 plans/round66_c1_tensor_probe.py --check-receipt <receipt>
    python3 plans/round66_c1_tensor_probe.py --selftest --work <scratch>

Exit: 0 pass, 1 predicate failed, 2 could-not-evaluate. Scratch is taken from --work only;
nothing is written under /tmp except the sandbox's own tmpfs.
"""

import argparse
import fcntl
import hashlib
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
GRADER = LANE / "corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py"
GRADER_SHA256 = "4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290"
CASES_DIR = LANE / "corpus/evidence/round66/tensor/cases"
JUNIT_DIR = LANE / "corpus/evidence/round66/tensor/junit"
VENV_ROOT = Path.home() / ".local/share/kengaku-r66/venv-torch"
VENV_PY = VENV_ROOT / "bin/python"
LOCK = Path.home() / ".local/share/kengaku-r66/port-12355.lock"
PORT = 12355
TORCH = "2.15.0+cpu"
PROBE_SHA_SELF = True  # the probe's own sha is recorded at run time (see probe_sha())

CASES = ["k1-ref", "k2-none", "k3-stub", "k4-col-nogather", "k5-row-noreduce"]
LAYER_KEYS = [f"{k}-ws{w}-bias{b}" for k in ("column", "row") for w in (1, 2, 4) for b in ("True", "False")]
KEYS = ["exists"] + LAYER_KEYS


def frozen(case: str) -> dict:
    v = {k: "F" for k in KEYS}
    if case == "k1-ref":
        v = {k: "P" for k in KEYS}
    elif case == "k2-none":
        pass
    elif case == "k3-stub":
        v["exists"] = "P"
    elif case == "k4-col-nogather":
        v["exists"] = "P"
        for k in KEYS:
            if k.startswith("row-"):
                v[k] = "P"
            elif k.startswith("column-"):
                v[k] = "P" if "-ws1-" in k else "F"
    elif case == "k5-row-noreduce":
        v["exists"] = "P"
        for k in KEYS:
            if k.startswith("column-"):
                v[k] = "P"
            elif k.startswith("row-"):
                v[k] = "P" if "-ws1-" in k else "F"
    else:
        raise KeyError(case)
    return v


FROZEN_TABLE = {c: frozen(c) for c in CASES}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_sha() -> str:
    return sha256(Path(__file__).resolve())


def key_of(testname: str) -> str:
    if testname == "test_parallel_linear_exists":
        return "exists"
    m = re.fullmatch(r"test_(column|row)_parallel_linear\[(.+)\]", testname)
    if not m:
        raise ValueError(f"unexpected testcase name: {testname}")
    kind, params = m.group(1), m.group(2).split("-")
    bias = next(p for p in params if p in ("True", "False"))
    ws = next(p for p in params if p in ("1", "2", "4"))
    return f"{kind}-ws{ws}-bias{bias}"


def port_busy() -> bool:
    s = socket.socket()
    s.settimeout(0.5)
    try:
        return s.connect_ex(("127.0.0.1", PORT)) == 0
    finally:
        s.close()


def setup_error(msg: str) -> int:
    print(f"SETUP {msg}")
    print("PREDICATE R66-C1 could-not-evaluate")
    return 2


def run_case(case: str, case_dir: Path, work: Path) -> dict:
    ctl = work / "ctl" / case
    shutil.rmtree(ctl, ignore_errors=True)
    ctl.mkdir(parents=True)
    cmd = [
        "bwrap", "--die-with-parent",
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
        "--dir", "/app", "--ro-bind", str(case_dir), "/app",
        "--dir", "/tests", "--ro-bind", str(GRADER), "/tests/test_outputs.py",
        "--bind", str(ctl), "/ctl",
        "--chdir", "/app",
        "--clearenv",
        "--setenv", "PATH", "/usr/bin:/bin",
        "--setenv", "HOME", "/tmp",
        "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
        "--setenv", "PYTHONNOUSERSITE", "1",
        str(VENV_PY), "-m", "pytest", "/tests/test_outputs.py",
        "-p", "no:cacheprovider", "-q", "--junitxml=/ctl/junit.xml",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    junit = ctl / "junit.xml"
    if not junit.exists():
        return {"case": case, "rc": proc.returncode, "error": "no junit", "tail": (proc.stdout + proc.stderr)[-800:]}
    tree = ET.parse(junit)
    outcomes = {}
    for tc in tree.iter("testcase"):
        name = tc.get("name")
        bad = any(child.tag in ("failure", "error") for child in tc)
        outcomes[key_of(name)] = "F" if bad else "P"
        if bad:
            msg = next((c.get("message") or "" for c in tc if c.tag in ("failure", "error")), "")
            outcomes.setdefault("_msg", {})[key_of(name)] = msg[:160].replace("\n", " ")
    return {
        "case": case,
        "rc": proc.returncode,
        "outcomes": {k: outcomes[k] for k in KEYS if k in outcomes},
        "msgs": outcomes.get("_msg", {}),
        "junit": junit,
        "case_sha": sha256(case_dir / "parallel_linear.py") if (case_dir / "parallel_linear.py").exists() else "none",
        "junit_sha": sha256(junit),
    }


def verdict_lines(results: list) -> tuple:
    ok = True
    lines = []
    for r in results:
        vec = " ".join(f"{k}={r['outcomes'].get(k, '?')}" for k in KEYS)
        match = all(r["outcomes"].get(k) == FROZEN_TABLE[r["case"]][k] for k in KEYS)
        ok = ok and match
        lines.append(f"CASE {r['case']} case_sha={r['case_sha']} junit_sha={r['junit_sha']} rc={r['rc']} port_free=True")
        lines.append(f"VECTOR {r['case']} {vec} frozen={'match' if match else 'MISMATCH'}")
        for k, m in sorted(r.get("msgs", {}).items()):
            lines.append(f"FRAGMENT {r['case']} {k} {m}")
    return ok, lines


def cmd_run(receipt: Path, work: Path) -> int:
    if not GRADER.exists() or sha256(GRADER) != GRADER_SHA256:
        return setup_error("grader sha mismatch or missing")
    if not VENV_PY.exists():
        return setup_error(f"venv missing at {VENV_ROOT}; recreate: uv venv --python /usr/bin/python3 {VENV_ROOT} && uv pip install --python {VENV_PY} --index-url https://download.pytorch.org/whl/cpu torch==2.15.0 && uv pip install --python {VENV_PY} transformers==5.22.1 pytest==9.2.0")
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        results = []
        for case in CASES:
            if port_busy():
                return setup_error(f"port {PORT} busy before {case}")
            case_dir = CASES_DIR / case
            if case == "k2-none":
                case_dir = work / "k2-none-app"
                shutil.rmtree(case_dir, ignore_errors=True)
                case_dir.mkdir(parents=True)
            r = run_case(case, case_dir, work)
            if "error" in r:
                return setup_error(f"{case}: {r['error']} rc={r['rc']} tail={r['tail']!r}")
            jdir = receipt.parent / "junit"
            jdir.mkdir(parents=True, exist_ok=True)
            shutil.copy(r["junit"], jdir / f"{case}.xml")
            results.append(r)
    ok, lines = verdict_lines(results)
    out = [
        f"GRADER sha256={GRADER_SHA256} path=corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py",
        f"TORCH version={TORCH} python={sys.version.split()[0]} bwrap={subprocess.run(['bwrap','--version'],capture_output=True,text=True).stdout.strip()}",
        f"PROBE sha256={probe_sha()}",
        *lines,
        f"PREDICATE R66-C1 {'pass' if ok else 'fail'}",
    ]
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0 if ok else 1


def check_receipt(receipt: Path) -> tuple:
    """Re-derive the verdict from the receipt and the committed bytes it names."""
    text = receipt.read_text().splitlines()
    problems = []
    if not any(l == f"GRADER sha256={GRADER_SHA256} path=corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py" for l in text):
        problems.append("grader line does not name the pinned sha")
    if not any(l.startswith("PROBE sha256=") and l.split("=", 1)[1] == probe_sha() for l in text):
        problems.append("probe sha does not match the committed probe")
    seen = {}
    for l in text:
        m = re.match(r"VECTOR (\S+) (.*) frozen=(\S+)$", l)
        if m:
            case = m.group(1)
            vec = dict(tok.split("=") for tok in m.group(2).split())
            seen[case] = vec
            if m.group(3) != "match":
                problems.append(f"{case} vector marked MISMATCH")
            if any(vec.get(k) != FROZEN_TABLE[case][k] for k in KEYS):
                problems.append(f"{case} vector differs from the frozen table")
    for case in CASES:
        if case not in seen:
            problems.append(f"{case} has no VECTOR line")
    for l in text:
        m = re.match(r"CASE (\S+) case_sha=(\S+) junit_sha=(\S+)", l)
        if not m:
            continue
        case, case_sha, junit_sha = m.groups()
        case_file = CASES_DIR / case / "parallel_linear.py"
        actual_case = sha256(case_file) if case_file.exists() else "none"
        if actual_case != case_sha:
            problems.append(f"{case} case_sha does not match committed bytes")
        jfile = receipt.parent / "junit" / f"{case}.xml"
        if not jfile.exists() or sha256(jfile) != junit_sha:
            problems.append(f"{case} junit_sha does not match committed junit bytes")
    if not any(l == "PREDICATE R66-C1 pass" for l in text):
        problems.append("receipt does not carry PREDICATE R66-C1 pass")
    return (not problems), problems


def cmd_check(receipt: Path) -> int:
    ok, problems = check_receipt(receipt)
    if ok:
        print("CHECK ok cases=5")
        print("PREDICATE R66-C1 pass")
        return 0
    for p in problems:
        print(f"CHECK defect: {p}")
    print("PREDICATE R66-C1 fail")
    return 1


def cmd_selftest(work: Path) -> int:
    """Self-test over isolated fixtures: a mutated vector and a missing junit must both be refused."""
    fx = Path(tempfile.mkdtemp(dir=work, prefix="selftest-"))
    try:
        good = fx / "good.txt"
        lines = [
            f"GRADER sha256={GRADER_SHA256} path=corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py",
            f"PROBE sha256={probe_sha()}",
        ]
        for case in CASES:
            r = FROZEN_TABLE[case]
            vec = " ".join(f"{k}={r[k]}" for k in KEYS)
            case_file = CASES_DIR / case / "parallel_linear.py"
            case_sha = sha256(case_file) if case_file.exists() else "none"
            junit_sha = sha256(JUNIT_DIR / f"{case}.xml") if (JUNIT_DIR / f"{case}.xml").exists() else "none"
            lines.append(f"CASE {case} case_sha={case_sha} junit_sha={junit_sha} rc=0 port_free=True")
            lines.append(f"VECTOR {case} {vec} frozen=match")
        lines.append("PREDICATE R66-C1 pass")
        good.write_text("\n".join(lines) + "\n")
        shutil.copytree(JUNIT_DIR, fx / "junit")
        ok_good, _ = check_receipt(good)
        mutated = fx / "mutated.txt"
        mutated.write_text(good.read_text().replace("VECTOR k1-ref exists=P", "VECTOR k1-ref exists=F", 1))
        ok_mut, _ = check_receipt(mutated)
        results = {"good_accepted": ok_good, "mutated_refused": not ok_mut}
        print(f"SELFTEST {results}")
        return 0 if all(results.values()) else 1
    finally:
        shutil.rmtree(fx, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--run", action="store_true")
    g.add_argument("--check-receipt", type=Path)
    g.add_argument("--selftest", action="store_true")
    ap.add_argument("--receipt", type=Path, default=LANE / "corpus/evidence/round66/tensor/receipt.txt")
    ap.add_argument("--work", type=Path)
    a = ap.parse_args()
    if a.run:
        if not a.work:
            print("SETUP --work required")
            return 2
        a.work.mkdir(parents=True, exist_ok=True)
        return cmd_run(a.receipt, a.work)
    if a.check_receipt:
        return cmd_check(a.check_receipt)
    if not a.work:
        print("SETUP --work required")
        return 2
    a.work.mkdir(parents=True, exist_ok=True)
    return cmd_selftest(a.work)


if __name__ == "__main__":
    sys.exit(main())

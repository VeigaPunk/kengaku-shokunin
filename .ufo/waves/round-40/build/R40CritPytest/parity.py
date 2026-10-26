#!/usr/bin/env python3
"""Round-40 R40CritPytest parity driver (final form).

Runs the REAL pytest 8.4.1 (uv venv -p 3.13 -> CPython 3.13.16, PyPI via uv) over the
pinned capture tests/test_outputs.py on each of the 28 frozen case end states of
plans/db_wal_probe.py, inside the probe's own bwrap sandbox (same seeds, same recipes,
same binds), with the venv bound read-only at /venv, and compares the per-test letters
with the committed receipt corpus/evidence/round40/db-wal-probe.txt.

Three pytest invocations per case, from the SAME end state:
  PT    -- minimal deterministic invocation (-q -rA --no-header -p no:cacheprovider)
  REPT  -- byte-identical repeat of PT (stability column)
  CTRF  -- test.sh verbatim (captured verifier recipe): pytest --ctrf /tmp/... /cap/test_outputs.py -rA
           (pytest 8.4.1 + pytest-json-ctrf 0.3.5, cwd /app, no extra flags)

Reuses the copied probe verbatim: P.CASES, P.TESTS, P.PINS, P.run_case; only HARNESS_PY and
sandbox_argv (extra read-only binds) are replaced. End states are therefore byte-identical
to the reference probe's; only the grading engine differs.
"""
from __future__ import annotations

import importlib.util
import pathlib
import re
import shutil
import sys
import tempfile

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r40/R40CritPytest")
LANE = S / "lane"
VENV = S / "venv"
UVPY = pathlib.Path("/home/vgpnk/.local/share/uv/python")
RECEIPT = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round40/db-wal-probe.txt")

spec = importlib.util.spec_from_file_location("p40", S / "db_wal_probe_pytest.py")
P = importlib.util.module_from_spec(spec)
sys.modules["p40"] = P          # dataclasses needs the module registered (__future__ annotations)
spec.loader.exec_module(P)

HARNESS = r'''
import json, os, re, subprocess, sys
mode = sys.argv[1]
rc = subprocess.run(["bash", "-euo", "pipefail", "/recipe.sh"], cwd="/app", stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
print("STAGE|recipe|" + str(rc))
if rc or mode == "stage":
    sys.exit(3 if rc else 0)
names = __NAMES__
v = subprocess.run(["/venv/bin/python", "-c",
                    "import importlib.metadata as m;print(m.version('pytest'), m.version('pytest-json-ctrf'), __import__('sys').version.split()[0])"],
                   capture_output=True, text=True)
print("PV|" + v.stdout.strip())
RUNS = (
    ("PT", ["-q", "-rA", "--no-header", "-p", "no:cacheprovider"], {"COLUMNS": "1000"}),
    ("REPT", ["-q", "-rA", "--no-header", "-p", "no:cacheprovider"], {"COLUMNS": "1000"}),
    ("CTRF", ["--ctrf", "/tmp/verifier-ctrf.json", "-rA"], {}),
)
for tag, flags, extra in RUNS:
    p = subprocess.run(["/venv/bin/python", "-m", "pytest"] + flags + ["/cap/test_outputs.py"],
                       cwd="/app", capture_output=True, text=True, stdin=subprocess.DEVNULL,
                       env=dict(os.environ, **extra))
    print("PRC|" + tag + "|" + str(p.returncode))
    got = {}
    for line in p.stdout.splitlines():
        if tag == "PT":
            print("RAW|" + line)
        m = re.match(r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s+\S*::(\w+)", line.strip())
        if m:
            rest = line.strip()[m.end():]
            em = re.search(r"([A-Za-z_][A-Za-z0-9_.]*(?:Error|Exception))\b", rest)
            got[m.group(2)] = (m.group(1), em.group(1).split(".")[-1] if em else "")
    print("PCOUNT|" + tag + "|" + str(len(got)))
    for name in names:
        status, err = got.get(name, ("MISSING", ""))
        print(tag + "|" + name + "|" + ("P" if status == "PASSED" else "F") + "|" + status + "|" + err)
try:
    c = json.load(open("/tmp/verifier-ctrf.json"))
    t = c["results"]["tests"]
    print("CTRFJSON|tests=" + str(len(t)) + "|statuses=" + ",".join(sorted(x["status"] for x in t)))
except Exception as e:
    print("CTRFJSON|FAIL|" + type(e).__name__)
'''.replace("__NAMES__", repr(P.TESTS))

P.HARNESS_PY = HARNESS
_orig_sandbox = P.sandbox_argv


def sandbox_argv(cap, work):
    return _orig_sandbox(cap, work) + [
        "--ro-bind", str(VENV), "/venv",
        "--ro-bind", str(UVPY), str(UVPY),
    ]


P.sandbox_argv = sandbox_argv


def receipt():
    cases = {}
    for line in RECEIPT.read_text().splitlines():
        if not line.startswith("CASE "):
            continue
        cid = line.split()[1]
        m = re.search(r" tests=([PF]+) ", line)
        errs = {k: v for k, v in re.findall(r"(test_[a-z_]+):error=([A-Za-z0-9_]+)", line)}
        cases[cid] = (m.group(1), errs)
    return cases


def parse(out, tag):
    got, status, errs = {}, {}, {}
    rc = None
    for line in out.splitlines():
        parts = line.split("|")
        if parts[0] == tag and len(parts) >= 5:
            _, name, letter, st, err = parts[:5]
            got[name] = letter
            status[name] = st
            if err:
                errs[name] = err
        elif parts[0] == "PRC" and len(parts) == 3 and parts[1] == tag:
            rc = int(parts[2])
    return got, status, errs, rc


def letters_of(got):
    return "".join(got.get(t, "?") for t in P.TESTS)


def main():
    only = set(sys.argv[1:])
    ref = receipt()
    root = pathlib.Path(tempfile.mkdtemp(prefix="pytest-parity-", dir=S))
    outdir = S / "out"
    agree = disagree = c_agree = c_disagree = 0
    pypass = cpass = 0
    try:
        print("# pytest parity @ pytest 8.4.1 / CPython 3.13 in the db_wal_probe.py sandbox")
        print(f"# venv={VENV} ro-bound at /venv; managed python {UVPY} ro-bound in place")
        for case in P.CASES:
            if only and case.cid not in only:
                continue
            rc, out = P.run_case(LANE / P.CAP, root, case, "grade")
            (outdir / (case.cid + ".txt")).write_text(out)
            got, status, errs, prc = parse(out, "PT")
            again, _, _, re_rc = parse(out, "REPT")
            cgot, _, _, crc = parse(out, "CTRF")
            ctrf = next((l for l in out.splitlines() if l.startswith("CTRFJSON|")), "CTRFJSON|MISSING")
            ref_letters, ref_errs = ref[case.cid]
            letters, letters2, cletters = letters_of(got), letters_of(again), letters_of(cgot)
            errgot = {k: v for k, v in errs.items() if v != "AssertionError"}
            match = letters == ref_letters
            cmatch = cletters == ref_letters
            errs_match = errgot == ref_errs
            agree += match
            disagree += not match
            c_agree += cmatch
            c_disagree += not cmatch
            npass = letters == "P" * len(P.TESTS)
            pypass += npass
            cpass += cletters == "P" * len(P.TESTS)
            print(f"PYCASE {case.cid} rc={rc} pytest_rc={prc} pytest={letters} probe={ref_letters}"
                  f" match={'yes' if match else 'NO'}"
                  f" ctrf={cletters} ctrf_match={'yes' if cmatch else 'NO'} ctrf_rc={crc}"
                  f" pytest_overall={'pass' if npass else 'fail'}"
                  f" probe_overall={'pass' if ref_letters == 'P' * len(P.TESTS) else 'fail'}"
                  f" errs={'same' if errs_match else 'DIFF'}"
                  f" regrade={'same' if letters2 == letters else 'DIFF:' + letters2} re_rc={re_rc}"
                  f" {ctrf}")
        n = agree + disagree
        print(f"parity cases={n} agree={agree} disagree={disagree} pytest_pass={pypass}")
        print(f"parity-ctrf cases={c_agree + c_disagree} agree={c_agree} disagree={c_disagree}"
              f" ctrf_pass={cpass}")
        return 0 if disagree == 0 and c_disagree == 0 else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

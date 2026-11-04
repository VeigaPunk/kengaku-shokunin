#!/usr/bin/env python3
"""Independent bubblewrap re-execution of the gcode-to-text grader, 8 frozen cases.

Staging is derived from the frozen table in plans/round-84-claims.md, not from
plans/round84-cases.json or plans/round84_gcode_probe.py.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

FLAG = "flag{gc0d3_iz_ch4LLenGiNg}"

# (id, bytes or None for absent)
CASES = [
    ("missing", None),
    ("empty", b""),
    ("exact", FLAG.encode()),
    ("padded", (" \n" + FLAG + "\t\n").encode()),
    ("uppercase", b"FLAG{GC0D3_IZ_CH4LLENGING}"),
    ("suffix", (FLAG + "x").encode()),
    ("prefix-only", b"flag{gc0d3_iz_"),
    ("wrong-flag", b"flag{gc0d3_iz_ch4LLenGiNx}"),
]

FROZEN = {
    "missing": ["F", "F"],
    "empty": ["P", "F"],
    "exact": ["P", "P"],
    "padded": ["P", "P"],
    "uppercase": ["P", "F"],
    "suffix": ["P", "F"],
    "prefix-only": ["P", "F"],
    "wrong-flag": ["P", "F"],
}

EXTRA = [
    ("x-empty-bytes", b""),
    ("x-nonutf8", b"\xff\xfe"),
    ("x-dir", "DIR"),
]


def build(root, cid, payload):
    d = os.path.join(root, cid, "app")
    os.makedirs(d)
    if payload is None:
        return d
    target = os.path.join(d, "out.txt")
    if payload == "DIR":
        os.makedirs(target)
    else:
        with open(target, "wb") as fh:
            fh.write(payload)
    return d


def run_case(appdir, grader_dir, driver_dir):
    argv = [
        "bwrap",
        "--unshare-all",
        "--ro-bind", "/usr", "/usr",
        "--ro-bind", "/etc", "/etc",
        "--symlink", "usr/lib", "/lib",
        "--symlink", "usr/lib", "/lib64",
        "--proc", "/proc",
        "--dev", "/dev",
        "--bind", appdir, "/app",
        "--ro-bind", grader_dir, "/tests",
        "--ro-bind", driver_dir, "/driver",
        "--chdir", "/",
        "/usr/bin/python3", "/driver/two_leg.py",
    ]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=120)
    return p, argv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--grader", required=True, help="grader dir containing tests/test_outputs.py")
    ap.add_argument("--driver", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = os.path.join(args.work, "cases")
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)

    grader_dir = os.path.abspath(args.grader)
    lines = []
    mismatches = 0
    defects = 0
    observed_vectors = {}

    def emit(s):
        lines.append(s)
        print(s)

    emit("HARNESS reviewer-independent bwrap re-execution")
    emit("grader_dir=%s" % grader_dir)
    emit("driver=%s" % os.path.abspath(os.path.join(args.driver, "two_leg.py")))
    emit("python=%s" % subprocess.run(["/usr/bin/python3", "-c", "import sys;print(sys.version.split()[0])"],
                                      capture_output=True, text=True).stdout.strip())
    emit("")

    for cid, payload in CASES:
        appdir = build(root, cid, payload)
        p, _ = run_case(appdir, grader_dir, args.driver)
        rec = None
        try:
            rec = json.loads(p.stdout.strip().splitlines()[-1])
        except Exception:
            rec = None
        if rec is None:
            observed_vectors[cid] = None
            emit("CASE %-11s predicted=%s observed=ERR(sandbox) rc=%d stderr=%r"
                 % (cid, "/".join(FROZEN[cid]), p.returncode, p.stderr[-300:]))
            defects += 1
            continue
        order = rec["functions"]
        vals = [leg[1] for leg in rec["legs"]]
        observed_vectors[cid] = vals
        detail = "; ".join("%s=%s(%s)" % (leg[0], leg[1], leg[2]) for leg in rec["legs"])
        mismatch = vals != FROZEN[cid]
        if mismatch:
            mismatches += 1
        if "SETUP" in vals:
            defects += 1
        emit("CASE %-11s predicted=%s observed=%s %s  [%s] rc=%d"
             % (cid, "/".join(FROZEN[cid]), "/".join(vals),
                "MISMATCH" if mismatch else "match", detail, p.returncode))

    emit("")
    emit("EXTRA probes (not part of the frozen 8; attack evidence only)")
    for cid, payload in EXTRA:
        appdir = build(root, cid, payload)
        p, argv = run_case(appdir, grader_dir, args.driver)
        try:
            rec = json.loads(p.stdout.strip().splitlines()[-1])
            detail = "; ".join("%s=%s(%s)" % (leg[0], leg[1], leg[2]) for leg in rec["legs"])
            vals = "/".join(leg[1] for leg in rec["legs"])
        except Exception:
            detail = "sandbox-error rc=%d stderr=%r" % (p.returncode, p.stderr[-300:])
            vals = "ERR"
        emit("EXTRA %-15s observed=%s  [%s] rc=%d" % (cid, vals, detail, p.returncode))

    emit("")
    emit("cases=%d mismatches=%d setup_defects=%d" % (len(CASES), mismatches, defects))
    emit("observed_vectors=%s" % json.dumps(observed_vectors, sort_keys=True))
    emit("PREDICATE R84-PROBE %s" % ("pass" if mismatches == 0 and defects == 0 else "fail"))

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return 0 if mismatches == 0 and defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

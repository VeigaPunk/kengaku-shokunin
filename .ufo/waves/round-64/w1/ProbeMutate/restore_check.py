#!/usr/bin/env python3
"""Restoration leg: originals untouched, preserved copies reproduce the baseline.

Writes W/receipts/restoration.txt. Reads the lane originals read-only.
"""

import hashlib
import pathlib
import shutil
import subprocess
import sys
import time

W = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/ProbeMutate")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
ORIG = {
    "probe": LANE / ".ufo/waves/round-64/w1/ProbeBuild/round64_c1_kvstore_probe.py",
    "sweep": LANE / ".ufo/waves/round-64/w1/SweepBuild/round64_trio_sweep.py",
    "gate": LANE / "plans/round63_gate_checks.py",
}
COPY = {
    "probe": W / "pristine/round64_c1_kvstore_probe.py",
    "sweep": W / "pristine/round64_trio_sweep.py",
    "gate": W / "pristine/round63_gate_checks.py",
}
BATTERY = {"probe": "9f56d25ddb33e14474c6439c16f25dd5545da99e542a051d342113a88b306843",
           "sweep": "56638ea1dfc0ca47ee91dfc0afec9c9fcbbefa9b15d3e163ad423b7f8dbf8bb0",
           "gate": "797085c242a63d0b38f875b6f67550848ddac34dd7f5dbd20861ad3849e7a18a"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd, cwd):
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=300)
    return proc.returncode, proc.stdout, proc.stderr


def main():
    work = W / "work"
    if work.exists():
        shutil.rmtree(work)
    (work / "st-probe").mkdir(parents=True)
    (work / "st-sweep").mkdir(parents=True)

    lines = ["# restoration leg — originals untouched; preserved copies re-detected",
             f"ts={time.strftime('%Y-%m-%dT%H:%M:%S')}", ""]
    ok = True
    for name, orig in ORIG.items():
        copy = COPY[name]
        o, c = sha256(orig), sha256(copy)
        same = o == c == BATTERY[name]
        ok = ok and same
        lines += [f"original_{name}={orig}",
                  f"original_sha256_now={o}",
                  f"battery_sha256={BATTERY[name]}",
                  f"preserved_copy={copy}",
                  f"preserved_sha256={c}",
                  f"byte_identical_to_battery_source={same}", ""]

    cases = [
        ("probe-check-receipt", [sys.executable, str(COPY["probe"]), "--check-receipt",
                                 str(W / "fixtures/probe/good-receipt.txt")], 0),
        ("probe-selftest", [sys.executable, str(COPY["probe"]), "--selftest",
                            "--work", str(work / "st-probe")], 0),
        ("sweep-m5-lane", [sys.executable, str(COPY["sweep"]), "--sweep", "--lane",
                           str(W / "fixtures/sweep/lane-m5"), "--frozen-list",
                           str(W / "fixtures/sweep/lane-m5/frozen.txt")], 1),
        ("sweep-selftest", [sys.executable, str(COPY["sweep"]), "--selftest",
                            "--work", str(work / "st-sweep")], 0),
    ]
    for label, cmd, expect in cases:
        rc, out, err = run(cmd, W)
        verdict = "ok" if rc == expect else "MISMATCH"
        ok = ok and rc == expect
        lines += [f"## {label}", f"cmd={' '.join(cmd)}", f"rc={rc} expect={expect} {verdict}",
                  "--- stdout ---", out.rstrip() or "(empty)",
                  "--- stderr ---", err.rstrip() or "(empty)", ""]
    lines.append(f"RESTORATION {'pass' if ok else 'fail'}")
    (W / "receipts/restoration.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

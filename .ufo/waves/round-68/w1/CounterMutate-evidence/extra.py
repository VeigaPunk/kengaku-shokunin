#!/usr/bin/env python3
"""Two extra probes:

(a) BASE-PROBE committed-bytes branch (deleted with the receipt-sha check in m2):
    load the probe with a valid adjacent base probe, then swap the bytes, then check.
    The frozen checker must emit base-probe-bytes; m2 must accept.

(b) the load-time path when the adjacent base probe is already drifted: what the
    instrument prints and returns (robustness observation, outside --check-receipt).
"""
import importlib.util
import pathlib
import shutil
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r68/CounterMutate")
L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FROZEN = "4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc"
RECORD = L / "corpus/evidence/round68/pypi/receipt.txt"
BASE_NAME = "round63_c1_pypi_probe.py"


def stage(tag, probe_src):
    d = S / "fix" / tag / "plans"
    if d.exists():
        shutil.rmtree(d.parent)
    d.mkdir(parents=True)
    shutil.copy2(probe_src, d / "round68_c1_pypi_finish.py")
    shutil.copy2(L / "plans" / BASE_NAME, d / BASE_NAME)
    return d / "round68_c1_pypi_finish.py", d / BASE_NAME


def load(mod_path):
    spec = importlib.util.spec_from_file_location("probe_x", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def swap_branch():
    out = {}
    for tag, src in (("base-swap-m00", L / "plans/round68_c1_pypi_finish.py"),
                     ("base-swap-m2",
                      S / "mut/m2/plans/round68_c1_pypi_finish.py")):
        probe, base = stage(tag, src)
        mod = load(probe)                       # valid bytes at load time
        mod._BASE = mod.load_base_probe()       # succeeds
        base.write_bytes(base.read_bytes() + b"\n# drift\n")   # swap after load
        mod.own_sha256 = lambda: FROZEN
        mod.lane_root = lambda: L
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = mod.check_receipt(RECORD)
        defects = [ln.split("CHECK defect ", 1)[1] for ln in buf.getvalue().splitlines()
                   if ln.startswith("CHECK defect ")]
        out[tag] = {"rc": rc, "defects": defects}
    return out


def load_time_drift():
    out = {}
    for tag, src in (("base-drift-load-m00", L / "plans/round68_c1_pypi_finish.py"),
                     ("base-drift-load-m2",
                      S / "mut/m2/plans/round68_c1_pypi_finish.py")):
        probe, base = stage(tag, src)
        base.write_bytes(base.read_bytes() + b"\n# drift\n")
        p = subprocess.run([sys.executable, str(probe), "--check-receipt", str(RECORD)],
                           capture_output=True, text=True, timeout=120)
        erred = "Traceback (most recent call last)" in p.stderr
        out[tag] = {"rc": p.returncode,
                    "stdout": p.stdout.strip().splitlines()[:2],
                    "stderr_last": p.stderr.strip().splitlines()[-1:] if p.stderr else [],
                    "traceback": erred}
    return out


def main():
    swap = swap_branch()
    drift = load_time_drift()
    print("(a) BASE-PROBE committed-bytes branch (post-load byte swap)")
    for k, v in swap.items():
        print(f"  {k:<16} rc={v['rc']} defects={v['defects']}")
    print("(b) adjacent base probe already drifted at load time")
    for k, v in drift.items():
        print(f"  {k:<20} rc={v['rc']} traceback={v['traceback']} "
              f"stdout={v['stdout']} stderr_last={v['stderr_last']}")
    ok = (swap["base-swap-m00"]["rc"] == 1
          and any(d.startswith("base-probe-bytes") for d in swap["base-swap-m00"]["defects"])
          and swap["base-swap-m2"]["rc"] == 0)
    print(f"EXTRA ok={ok}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

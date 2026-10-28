#!/usr/bin/env python3
"""R50C1CritBlind8 probe: build candidate blind hostile modules and decide each fixture with the lane's own
harness contract (separate process, verdict in the exit status), against the lane's fence at its tip.

Verdicts are the counter's (`plans/round50_c1_verify.py` HARNESS): 10 BREACH (refused) · 11 ADMIT · other ERROR.
Read-only against the lane clone; every fixture is built into an opaque, decoy-padded parent inside --work.
"""
import argparse
import importlib.util
import json
import pathlib
import secrets
import subprocess
import sys

PAD = 8


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--mods", required=True, help="directory of candidate modules")
    ap.add_argument("--fence", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    counter = load(lane / "plans/round50_c1_verify.py", "k50_counter")
    hb = load(lane / "plans/honest50/build_honest_population.py", "k50_honest")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "k50_k44")

    harness = work / "harness.py"
    harness.write_text(counter.HARNESS)
    fence = pathlib.Path(a.fence).resolve() if a.fence else lane / "plans/fixture_fence.py"
    print(f"LANE {lane}")
    print(f"FENCE {fence} sha256={counter.sha256_file(fence)}")
    print(f"GIT {subprocess.run(['git', '--version'], capture_output=True, text=True).stdout.strip()}")

    mods = sorted(pathlib.Path(a.mods).glob("*.py"))
    env = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"}
    bad = 0
    for path in mods:
        gen = work / secrets.token_hex(8)
        gen.mkdir(parents=True, exist_ok=True)
        for _k in range(PAD):
            (gen / secrets.token_hex(4)).mkdir()
        try:
            built = hb.build_once(k44, path, gen)
        except Exception as e:                                        # a build failure is a receipt
            print(f"{path.name}: BUILD-ERROR {type(e).__name__}: {e}")
            bad += 1
            continue
        for fid, tool, expect, _defects, argv, d, _b in built:
            p = subprocess.run([sys.executable, "-I", str(harness), str(fence), str(d), tool,
                                json.dumps(argv)], cwd=str(d), env=env, capture_output=True, text=True,
                               timeout=120)
            v = "BREACH" if p.returncode == 10 else ("ADMIT" if p.returncode == 11 else "ERROR")
            why = (p.stderr.strip().splitlines() or [""])[-1][:300]
            print(f"{fid} expect={expect} rc={p.returncode} verdict={v} why={why}")
            if v != "BREACH":
                bad += 1
    print(f"PROBE fixtures={sum(1 for _ in mods)} unclean={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

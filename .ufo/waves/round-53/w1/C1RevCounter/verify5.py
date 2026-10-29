#!/usr/bin/env python3
"""Final batch on the FROZEN counter (a34838f):
  Z1  scratch clone -> --selftest -> cases=22 failures=0 (the task's required run)
  Z2  leg_pins forced False  -> which selftest cases still pass?  (battery discrimination)
  Z3  leg_confirm forced False -> which cases still pass?
  Z4  'not uncl' conjunct neutralised -> is the unclassified=0 rule covered?
  Z5  'not bad' conjunct neutralised  -> is the bad-label-row rule covered?
  Z6  'not extra' conjunct neutralised-> is the extra-label-row rule covered?
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C1RevCounter")
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin").resolve()
FROZEN = SCRATCH / "FROZEN_counter.py"
BASE = FROZEN.read_text()


def run_selftest(src_text, tag):
    d = Path(tempfile.mkdtemp(prefix=f"z-{tag}-", dir=str(SCRATCH)))
    (d / "round53_c1_triage.py").write_text(src_text)
    shutil.copy(SCRATCH / "round53_c1_extract.py", d / "round53_c1_extract.py")
    env = dict(os.environ, TMPDIR=str(SCRATCH))
    p = subprocess.run([sys.executable, str(d / "round53_c1_triage.py"), "--selftest"],
                       capture_output=True, text=True, env=env, timeout=900)
    shutil.rmtree(d, ignore_errors=True)
    fails = [l.split()[1] for l in p.stdout.splitlines()
             if l.startswith("SELFTEST ") and l.rstrip().endswith("FAIL")]
    tail = [l for l in p.stdout.splitlines() if l.startswith("SELFTEST cases=")]
    return {"tag": tag, "rc": p.returncode, "failed_cases": fails, "summary": tail[-1] if tail else ""}


def main():
    # ---- Z1: scratch clone of the lane, run the FROZEN counter's --selftest there ----
    clone = SCRATCH / "clone"
    if clone.exists():
        shutil.rmtree(clone)
    clone.mkdir(parents=True)
    # copy the repo state (tracked files only) without touching the lane
    subprocess.run(["git", "-C", str(LANE), "archive", "a34838f"], capture_output=True, check=True)
    tar = subprocess.run(["git", "-C", str(LANE), "archive", "a34838f"], capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", str(clone)], input=tar.stdout, check=True)
    print("=== Z1: --selftest in a scratch clone of the claims commit a34838f ===")
    p = subprocess.run([sys.executable, "plans/round53_c1_triage.py", "--selftest"], cwd=str(clone),
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=str(SCRATCH)))
    for l in p.stdout.splitlines():
        print("   ", l)
    print("    exit:", p.returncode)

    print()
    print("=== Z2..Z6: leg/conjunct discrimination over the 22 cases ===")
    MUTS = {
        "Z2_leg_pins_always_false": [("    ok = (pop_ok and pin_ok and idx_ok and match == cfg[\"CAPTURES_EXPECTED\"]",
                                       "    ok = False and (pop_ok and pin_ok and idx_ok and match == cfg[\"CAPTURES_EXPECTED\"]")],
        "Z3_leg_confirm_always_false": [("    ok = len(good) >= cfg[\"CONFIRM_MIN\"]",
                                         "    ok = False and len(good) >= cfg[\"CONFIRM_MIN\"]")],
        "Z4_not_uncl": [("and not bad and not extra and not uncl and", "and not bad and not extra and True and")],
        "Z5_not_bad": [("and not bad and not extra and not uncl and", "and True and not extra and not uncl and")],
        "Z6_not_extra": [("and not bad and not extra and not uncl and", "and not bad and True and not uncl and")],
        "Z7_no_sweep_len_check": [("if not isinstance(sw, list) or len(sw) < 2:", "if not isinstance(sw, list):")],
        "Z8_absent_never_counted": [("absent += 1", "absent += 0")],
        "Z9_contested_budget_off": [("and len(contested) <= ORACLE_MAX_CONTESTED * n", "and True")],
    }
    for tag, subs in MUTS.items():
        src = BASE
        ok = True
        for old, new in subs:
            if old not in src:
                ok = False
                break
            src = src.replace(old, new, 1)
        if not ok:
            print(f"   {tag}: PATTERN NOT FOUND")
            continue
        r = run_selftest(src, tag)
        print(f"   {tag}: rc={r['rc']} {r['summary']}")
        print(f"      failing cases: {r['failed_cases']}")

    shutil.rmtree(clone, ignore_errors=True)


if __name__ == "__main__":
    main()

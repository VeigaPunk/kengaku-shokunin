#!/usr/bin/env python3
"""Seat R50C1CritBlind7 driver: build the two blind hostile modules through the lane's own builder and ask the
tip fence for one decision per fixture, out of process, exactly as `plans/round50_c1_verify.py` does."""
import argparse
import importlib.util
import json
import os
import pathlib
import secrets
import subprocess
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fence", default=None)
    ap.add_argument("--modules", nargs="+", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    fence = pathlib.Path(a.fence).resolve() if a.fence else lane / "plans/fixture_fence.py"
    work = pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)

    counter = load(lane / "plans/round50_c1_verify.py", "k50_counter")
    hb = load(lane / "plans/honest50/build_honest_population.py", "k50_honest")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "k50_k44")
    harness = work / "harness.py"
    harness.write_text(counter.HARNESS)
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": "/nonexistent", "LANG": "C.UTF-8",
           "LC_ALL": "C.UTF-8", "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"}
    print(f"FENCE {fence} sha256={counter.sha256_file(fence)}")
    for mod_path in (pathlib.Path(m).resolve() for m in a.modules):
        gen = work / secrets.token_hex(8)
        gen.mkdir(parents=True)
        for _ in range(counter.PAD):
            (gen / secrets.token_hex(4)).mkdir()
        print(f"MODULE {mod_path.name} sha256={counter.sha256_file(mod_path)}")
        try:
            built = hb.build_once(k44, mod_path, gen)
        except Exception as e:                                     # a build failure is a receipt
            print(f"BUILD-ERROR {mod_path.name}: {type(e).__name__}: {e}")
            continue
        for fid, tool, expect, _defects, argv, d, _b in built:
            audit = hb.structural_audit(d)
            ident = hb.tree_identity(d)
            p = subprocess.run([sys.executable, "-I", str(harness), str(fence), str(d), tool,
                                json.dumps(argv)], cwd=str(d), env=env, capture_output=True, text=True,
                               timeout=120)
            verdict = "BREACH" if p.returncode == 10 else ("ADMIT" if p.returncode == 11 else "ERROR")
            why = (p.stderr.strip().splitlines() or [""])[-1][:300]
            lane_rel = argv[argv.index("--lane") + 1] if "--lane" in argv else "."
            repo = d / lane_rel
            gd = subprocess.run(["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
                                capture_output=True, text=True)
            gdraw = gd.stdout.strip()
            gdres = str(pathlib.Path(gdraw).resolve()) if gd.returncode == 0 else None
            head = subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "HEAD"],
                                  capture_output=True, text=True)
            print(json.dumps({
                "fid": fid, "tool": tool, "expect": expect, "argv": argv, "dir": str(d), "repo": str(repo),
                "fence_rc": p.returncode, "fence_verdict": verdict, "fence_reason": why,
                "symlinks": audit["symlinks"], "specials": audit["specials"], "hardlinks": audit["hardlinks"],
                "tree_sha": ident[0], "n_files": ident[1], "n_dirs": ident[2],
                "gitdir_raw": gdraw, "gitdir_resolved": gdres,
                "gitdir_inside_d": bool(gdres) and pathlib.Path(gdres).is_relative_to(d.resolve()),
                "head_rc": head.returncode, "head": head.stdout.strip(),
            }, sort_keys=True))
        print(f"GEN {gen}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

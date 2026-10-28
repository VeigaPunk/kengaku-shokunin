#!/usr/bin/env python3
"""Seat R50C1CritBlind5 — composed-indirection probe (critique, NOT a deliverable).

Escalation of the two blind modules: keep every single indirection inside `d`, and let the outside read need
TWO kinds of indirection in sequence:

    wt/.git --gitfile--> wtadmin (inside d)
    wtadmin/commondir --commondir--> shared/.git (inside d)
    shared/.git/objects/info/alternates --alternates--> comp-out/.git/objects (OUTSIDE d)
    refs/heads/feature = <a commit that exists only in comp-out>

A fence that resolves each indirection kind but does not carry the classification across kinds admits this and
still lets a git child read outside `d`. Prints the verdict of the fence under test and the real-git witness.

This file is BOTH the fixture module (top-level `build`/`FIXTURES`, round-44 contract) and its driver; it runs
main() only when executed directly.
Usage: python3 probe_compose.py --lane CLONE [--fence FENCE] --work DIR
"""
import argparse
import importlib.util
import pathlib
import shutil
import subprocess
import sys


def build(ctx, d):
    out = ctx.init(d.parent / "comp-out")
    ctx.write(out / "b-only.txt", "outside bytes\n")
    ctx.git(out, "add", "-A")
    ctx.git(out, "commit", "-qm", "out")
    o_sha = ctx.sh("git", "-C", str(out), "rev-parse", "HEAD").stdout.strip()
    shared = d / "shared"                      # a BARE store: no `.git` dir, so a tree walk never collects it
    shared.mkdir()
    ctx.sh("git", "init", "-q", "--bare", str(shared))
    ctx.write(shared / "objects/info/alternates", "../../../comp-out/.git/objects\n")
    ctx.write(shared / "refs/heads/feature", o_sha + "\n")
    adm = d / "wtadmin"
    adm.mkdir()
    (adm / "HEAD").write_text("ref: refs/heads/feature\n")
    (adm / "commondir").write_text("../shared\n")
    (adm / "gitdir").write_text("../wt/.git\n")
    (d / "wt").mkdir()
    (d / "wt" / ".git").write_text("gitdir: ../wtadmin\n")
    return ["--lane", "wt"]


FIXTURES = [{"fid": "bl5-compose-cd-then-alternates", "tool": "anchor", "expect": "breach", "defects": [],
             "build": build}]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(*argv):
    return subprocess.run([str(a) for a in argv], capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fence", default=None)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    hb = load(lane / "plans/honest50/build_honest_population.py", "cp_hb")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "cp_k44")
    fence_path = pathlib.Path(a.fence).resolve() if a.fence else lane / "plans/fixture_fence.py"
    fence = load(fence_path, "cp_fence")
    print(f"FENCE {fence_path} sha256={hb.sha256_file(fence_path)}")
    gen = work / "build"
    gen.mkdir()
    for fid, tool, _e, _df, argv, d, _b in hb.build_once(k44, pathlib.Path(__file__).resolve(), gen):
        why = fence.breach(d, argv, tool)
        print(f"FIXTURE {fid} argv={argv}")
        print(f"VERDICT {'ADMIT' if why is None else 'BREACH'} {why or ''}")
        r = git("git", "-C", d / "wt", "log", "--oneline")
        print(f"REALGIT log rc={r.returncode} out={r.stdout.strip()!r} err={r.stderr.strip().splitlines()[:1]}")
        r = git("git", "-C", d / "wt", "rev-parse", "--show-toplevel")
        print(f"REALGIT toplevel rc={r.returncode} out={r.stdout.strip()}")
        print(f"REALGIT objects-dirs-under-d={[str(p.relative_to(d)) for p in d.rglob('objects') if p.is_dir()]}")
        print(f"REALGIT commondir-files={[str(p.relative_to(d)) for p in d.rglob('commondir')]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

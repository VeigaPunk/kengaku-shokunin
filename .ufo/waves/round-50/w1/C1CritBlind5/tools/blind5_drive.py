#!/usr/bin/env python3
"""Seat R50C1CritBlind5 driver: build the two blind hostile modules through the lane's own builder contract,
measure the base fence on them, and witness with real git that each one makes a git child read outside `d`.

Read-only against the lane: builds into DIR/<module>/f000, writes nothing into the lane tree.
Usage: python3 blind5_drive.py --lane CLONE --module-dir DIR [--work DIR]
"""
import argparse
import importlib.util
import os
import pathlib
import shutil
import stat
import subprocess
import sys

ENV = None  # inert; every fixture git call goes through the lane's Ctx


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tree_scan(d):
    """Symlinks, special files and multi-link regular files anywhere in the fixture (the base fence's own
    blanket refusals). A module that trips one of these is refused for the wrong reason."""
    bad = []
    for top, dirs, files in os.walk(str(d)):
        for name in dirs + files:
            p = pathlib.Path(top) / name
            st = os.lstat(p)
            if stat.S_ISLNK(st.st_mode):
                bad.append(("symlink", str(p.relative_to(d))))
            elif not (stat.S_ISDIR(st.st_mode) or stat.S_ISREG(st.st_mode)):
                bad.append(("special", str(p.relative_to(d))))
            elif stat.S_ISREG(st.st_mode) and st.st_nlink > 1:
                bad.append(("nlink>1", str(p.relative_to(d))))
    return bad


def git(*argv):
    return subprocess.run([str(a) for a in argv], capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--module-dir", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--fence", default=None, help="fence under test (default plans/fixture_fence.py of --lane)")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)

    hb = load(lane / "plans/honest50/build_honest_population.py", "bl5_hb")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "bl5_k44")
    fence = load(pathlib.Path(a.fence).resolve() if a.fence else lane / "plans/fixture_fence.py", "bl5_fence")

    for mod_path in sorted(pathlib.Path(a.module_dir).glob("*.py")):
        gen = work / mod_path.stem
        gen.mkdir(parents=True)
        print(f"=== MODULE {mod_path.name} sha256={hb.sha256_file(mod_path)}")
        built = hb.build_once(k44, mod_path, gen)
        for fid, tool, expect, _defects, argv, d, _b in built:
            print(f"BUILT fid={fid} tool={tool} argv={argv} d={d.relative_to(work)}")
            scan = tree_scan(d)
            print(f"TREE anomalies={len(scan)} {scan[:5]}")
            why = fence.breach(d, argv, tool)
            print(f"FENCE fid={fid} verdict={'ADMIT' if why is None else 'BREACH'} why={why!r}")
            print(f"OUTSIDE-ENTRIES {sorted(p.name for p in d.parent.iterdir() if p != d)}")
            for rel in sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()):
                print(f"  FILE {rel}")
            yield_witness(d, fid, work)
    return 0


def yield_witness(d, fid, work):
    """Real-git witnesses for one fixture; each is printed as `WITNESS <fid> <name> rc=<n> <text>`."""
    d = pathlib.Path(d)
    if fid == "bl5-alternates-chain-out":
        out = d.parent / "chain-out"
        sha = git("git", "-C", out, "rev-parse", "HEAD").stdout.strip()
        print(f"WITNESS {fid} outside-commit={sha}")
        print(f"WITNESS {fid} lane-rev-parse rc=0 exists={git('git','-C',d/'lane','cat-file','-e',sha).returncode == 0}")
        r = git("git", "-C", d / "lane", "cat-file", "-p", f"{sha}:b-only.txt")
        print(f"WITNESS {fid} read-outside-object rc={r.returncode} stdout={r.stdout.strip()!r}")
        under_d = [str(p.relative_to(d)) for p in (d).rglob(sha[:2] + "/*") if p.is_file()]
        outside = [str(p.relative_to(d.parent)) for p in out.rglob(sha[:2] + "/*") if p.is_file()]
        print(f"WITNESS {fid} object-under-d={under_d} object-outside-d={outside}")
        cp = work / "moveaway" / "chain"
        shutil.rmtree(cp.parent, ignore_errors=True)
        shutil.copytree(d.parent, cp, symlinks=True)
        shutil.move(str(cp / "chain-out"), str(cp / "chain-out.gone"))
        r = git("git", "-C", cp / "f000" / "lane", "cat-file", "-p", f"{sha}:b-only.txt")
        print(f"WITNESS {fid} outside-moved-away rc={r.returncode} err={r.stderr.strip().splitlines()[:1]}")
    elif fid == "bl5-wt-commondir-out":
        wt = d / "wt"
        for name, args in (("toplevel", ("rev-parse", "--show-toplevel")),
                           ("absolute-git-dir", ("rev-parse", "--absolute-git-dir")),
                           ("git-common-dir", ("rev-parse", "--git-common-dir")),
                           ("log", ("log", "--oneline", "--all"))):
            r = git("git", "-C", wt, *args)
            print(f"WITNESS {fid} {name} rc={r.returncode} out={r.stdout.strip().splitlines()[:2]}")
        body = git("git", "-C", wt, "cat-file", "-p", "HEAD:seed.txt")
        print(f"WITNESS {fid} read-object rc={body.returncode} stdout={body.stdout.strip()!r}")
        under = [str(p.relative_to(d)) for p in d.rglob("objects") if p.is_dir()]
        print(f"WITNESS {fid} objects-dirs-under-d={under}")
        cp = work / "moveaway" / "wt"
        shutil.rmtree(cp.parent, ignore_errors=True)
        shutil.copytree(d.parent, cp, symlinks=True)
        shutil.move(str(cp / "wt-common"), str(cp / "wt-common.gone"))
        r = git("git", "-C", cp / "f000" / "wt", "log", "--oneline", "--all")
        print(f"WITNESS {fid} outside-moved-away rc={r.returncode} err={r.stderr.strip().splitlines()[:1]}")


if __name__ == "__main__":
    sys.exit(main())

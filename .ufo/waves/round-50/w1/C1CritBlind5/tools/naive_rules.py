#!/usr/bin/env python3
"""Seat R50C1CritBlind5 — narrow-widening vs correct-widening probe.

The round-50 repair must relax `plans/fixture_fence.py` so the honest in-`d` indirection classes are admitted
(n20 linked worktree, n21 separate gitdir, n22 alternates-in-d). For each fixture this probe prints, side by
side, whether a NARROW (tempting) widening admits it and whether the CORRECT (resolving) widening refuses it,
next to what real git actually does. A fixture that every narrow widening admits, and that real git uses to read
outside `d`, is the counterexample: the repair must resolve, not pattern-match.

Rules (all read-only; all operate on the fixture dir `d` and the lane the argv names):
  R1a alternates, ONE HOP from the lane's own store only      (target inside d -> admit)
  R1b alternates, TRANSITIVE from the lane's store            (every hop inside d -> admit)
  R2a gitfile, ONE HOP                                        (gitdir target inside d -> admit)
  R2b gitfile one hop + commondir of that gitdir resolved      (both inside d -> admit)
  R3a commondir TEXT is a relative path                        (no leading '/' -> admit)
  R3b commondir RESOLVED against its gitdir                    (inside d -> admit)

Read-only against the lane; builds into --work.
"""
import argparse
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(p):
    return pathlib.Path(os.path.normpath(str(p)))


def inside(p, d):
    p, d = str(norm(p)), str(norm(d))
    return p == d or p.startswith(d + os.sep)


def resolve(base, text):
    text = text.strip()
    return norm(text if text.startswith("/") else pathlib.Path(base) / text)


def gitdir_of(dot_git):
    """Resolve a `.git` entry (dir or file) to the git directory it names, or None."""
    if dot_git.is_dir():
        return dot_git
    if not dot_git.is_file():
        return None
    for line in dot_git.read_text(errors="replace").splitlines():
        if line.strip().startswith("gitdir:"):
            return resolve(dot_git.parent, line.split(":", 1)[1])
    return None


def common_of(gitdir):
    """The common directory of a git dir (its own commondir, resolved against itself, else itself)."""
    cdf = pathlib.Path(gitdir) / "commondir"
    if not cdf.is_file():
        return pathlib.Path(gitdir)
    return resolve(gitdir, cdf.read_text(errors="replace"))


def lane_dirs(d, argv):
    tok = None
    for i, a in enumerate(argv):
        if a == "--lane" and i + 1 < len(argv):
            tok = argv[i + 1]
    if tok is None:
        return None, None
    lane = resolve(d, tok)
    gd = gitdir_of(lane / ".git")
    if gd is None:
        return None, None
    return gd, common_of(gd)


def alternates_lines(objects_dir):
    f = pathlib.Path(objects_dir) / "info" / "alternates"
    if not f.is_file():
        return []
    return [ln.strip() for ln in f.read_text(errors="replace").splitlines() if ln.strip()]


def r1a(d, argv):
    gd, common = lane_dirs(d, argv)
    if common is None:
        return "n/a", "lane has no gitdir"
    lines = alternates_lines(common / "objects")
    if not lines:
        return "n/a", "lane store has no alternates"
    for ln in lines:
        t = resolve(common / "objects", ln)
        if not inside(t, d):
            return "REFUSE", f"direct target {t} outside d"
    return "ADMIT", f"{len(lines)} direct line(s) inside d (does not read the target's own alternates)"


def r1b(d, argv):
    gd, common = lane_dirs(d, argv)
    if common is None:
        return "n/a", "lane has no gitdir"
    seen, todo, hops = set(), [common / "objects"], 0
    while todo and hops < 6:
        cur = todo.pop(0)
        if str(cur) in seen:
            continue
        seen.add(str(cur))
        for ln in alternates_lines(cur):
            t = resolve(cur, ln)
            hops += 1
            if not inside(t, d):
                return "REFUSE", f"hop {hops}: {cur} -> {t} outside d"
            todo.append(t)
    return "ADMIT", f"{len(seen)} store(s), every hop inside d"


def all_gitfiles(d):
    return [p for p in d.rglob(".git") if p.is_file()]


def r2a(d, argv):
    files = all_gitfiles(d)
    if not files:
        return "n/a", "no .git file"
    for p in files:
        t = gitdir_of(p)
        if t is None or not inside(t, d):
            return "REFUSE", f"{p.relative_to(d)} -> {t} outside/undecipherable"
    return "ADMIT", f"{len(files)} gitfile(s), targets inside d (target classified as a store, bytes unread)"


def r2b(d, argv):
    files = all_gitfiles(d)
    if not files:
        return "n/a", "no .git file"
    for p in files:
        t = gitdir_of(p)
        if t is None or not inside(t, d):
            return "REFUSE", f"{p.relative_to(d)} -> {t} outside/undecipherable"
        cdf = pathlib.Path(t) / "commondir"
        if cdf.is_file():
            c = resolve(t, cdf.read_text(errors="replace"))
            if not inside(c, d):
                return "REFUSE", f"{p.relative_to(d)} gitdir {t.relative_to(d)} commondir -> {c} outside d"
    return "ADMIT", f"{len(files)} gitfile(s) and their commondir(s) inside d"


def all_commondirs(d):
    return [p for p in d.rglob("commondir") if p.is_file()]


def r3a(d, argv):
    files = all_commondirs(d)
    if not files:
        return "n/a", "no commondir"
    for p in files:
        if p.read_text(errors="replace").strip().startswith("/"):
            return "REFUSE", f"{p.relative_to(d)} is absolute"
    return "ADMIT", f"{len(files)} commondir(s) hold a relative path (target never resolved)"


def r3b(d, argv):
    files = all_commondirs(d)
    if not files:
        return "n/a", "no commondir"
    for p in files:
        c = resolve(p.parent, p.read_text(errors="replace"))
        if not inside(c, d):
            return "REFUSE", f"{p.relative_to(d)} -> {c} outside d"
    return "ADMIT", f"{len(files)} commondir(s) resolve inside d"


RULES = (("R1a alternates one-hop ", r1a), ("R1b alternates transitive", r1b),
         ("R2a gitfile one-hop   ", r2a), ("R2b gitfile+commondir  ", r2b),
         ("R3a commondir text    ", r3a), ("R3b commondir resolved ", r3b))


def git(*argv):
    return subprocess.run([str(a) for a in argv], capture_output=True, text=True)


def realgit(d, fid):
    if fid == "bl5-alternates-chain-out":
        out = d.parent / "chain-out"
        sha = git("git", "-C", out, "rev-parse", "HEAD").stdout.strip()
        r = git("git", "-C", d / "lane", "cat-file", "-p", f"{sha}:b-only.txt")
        return rc(r), f"lane reads {sha[:12]} only present outside d -> {r.stdout.strip()!r}"
    if fid == "bl5-wt-commondir-out":
        common = git("git", "-C", d / "wt", "rev-parse", "--git-common-dir").stdout.strip()
        r = git("git", "-C", d / "wt", "log", "--oneline", "--all")
        return rc(r), f"common-dir={common} log={r.stdout.strip()!r} (no objects dir under d)"
    return None, "honest class: outside read not required"


def rc(r):
    return f"rc={r.returncode}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--module-dir", required=True)
    ap.add_argument("--extra-module", action="append", default=[])
    ap.add_argument("--fence", default=None)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    hb = load(lane / "plans/honest50/build_honest_population.py", "nw_hb")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "nw_k44")
    fence = load(pathlib.Path(a.fence).resolve() if a.fence else lane / "plans/fixture_fence.py", "nw_fence")
    mods = sorted(pathlib.Path(a.module_dir).glob("*.py")) + [pathlib.Path(p) for p in a.extra_module]
    for mod_path in mods:
        gen = work / mod_path.stem
        gen.mkdir(parents=True)
        for fid, tool, _e, _df, argv, d, _b in hb.build_once(k44, mod_path, gen):
            why = fence.breach(d, argv, tool)
            print(f"FIXTURE {fid} module={mod_path.name}")
            print(f"  FENCE       {'ADMIT' if why is None else 'BREACH'} {why or ''}")
            for name, fn in RULES:
                v, note = fn(d, argv)
                print(f"  {name} {v:6s} {note}")
            r, text = realgit(d, fid)
            print(f"  REALGIT     {r or '-':8s} {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

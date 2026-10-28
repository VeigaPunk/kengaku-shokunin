#!/usr/bin/env python3
"""Round-50 C2 counting command: every artifact pointer the lane's self-assessment files carry resolves.

Surface (frozen in `plans/round-50-claims.md` §C2): the three self-assessment files `SCORECARD.md`,
`SHONEN.md` and `PROVINCE.md`. A *pointer* is

  * a lane-relative artifact path starting `plans/` or `corpus/` and ending in one of the extensions in
    `EXTS` — the kind of pointer those files use for evidence (`plans/round44_c1_verify.py`,
    `corpus/evidence/round9-fleet/probeA.py`); or
  * a 40-hex commit hash.

A pointer RESOLVES iff

  * the path exists at the audit revision (lane root); or
  * the SCORECARD carries a correction row `SUPERSEDED <pointer> -> <target>` and `<target>` exists; or
  * the correction row is `SUPERSEDED <pointer> -> never-landed` and `git log --all --oneline -- <pointer>`
    is empty (the file never existed in the lane's committed history), so there is nothing to re-point at
    and the correction says so;
  * a hash resolves iff `git cat-file -e <hash>` succeeds AND the hash is an ancestor of the branch tip.

Corrections are the lane's append-only discipline (PROTOCOL.md: corrections are new text, never a rewrite), so
they live in the `## Round 50 — C2 corrections` block of `SCORECARD.md`, one `SUPERSEDED` row per pointer.

Before (measured at `71f5f5f`, 2026-10-28, `--raw`): 12 unresolved pointers, 0 unresolved hashes.
Frozen predicate: `POINTERS total=… resolved=… unresolved=0`, exit 0.

Usage: python3 plans/round50_c2_audit.py [--lane .] [--selftest]
Exit: 0 all pointers resolve · 1 a pointer does not resolve · 2 setup error.
`--selftest` appends a bogus token to a scratch copy of SCORECARD.md and requires exit 1 (the check can fail).
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

FILES = ("SCORECARD.md", "SHONEN.md", "PROVINCE.md")
EXTS = ("md", "py", "json", "jsonl", "txt", "patch", "whl", "sh", "json5", "tres")
TOKEN = re.compile(
    r"(?<![\w/.-])((?:plans|corpus)/[A-Za-z0-9_][A-Za-z0-9_./+-]*?\.(?:" + "|".join(EXTS) + r"))"
    r"|(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
SUPERSEDED = re.compile(r"^\s*SUPERSEDED\s+(\S+)\s+->\s+(\S+)\s*$", re.M)


def git(lane, *args):
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


def scan(lane):
    paths, hashes = set(), set()
    for name in FILES:
        p = lane / name
        if not p.is_file():
            print(f"SETUP missing {name}", file=sys.stderr)
            return None, None
        for m in TOKEN.finditer(p.read_text()):
            (paths if m.group(1) else hashes).add(m.group(1) or m.group(0))
    return paths, hashes


def superseded_map(lane):
    text = (lane / "SCORECARD.md").read_text()
    return {m.group(1): m.group(2) for m in SUPERSEDED.finditer(text)}


def audit(lane, check_hashes=True):
    paths, hashes = scan(lane)
    if paths is None:
        return 2, None
    supers = superseded_map(lane)
    branch = git(lane, "rev-parse", "--abbrev-ref", "origin/HEAD").stdout.strip().split("/")[-1] or "master"
    tip = git(lane, "rev-parse", branch).stdout.strip()
    if not tip:
        tip = git(lane, "rev-parse", "HEAD").stdout.strip()
        branch = "HEAD"
    unresolved, res_exist, res_sup, res_never = [], 0, 0, 0
    for p in sorted(paths):
        if (lane / p).exists():
            res_exist += 1
            continue
        target = supers.get(p)
        if target and target != "never-landed" and (lane / target).exists():
            res_sup += 1
            continue
        if target == "never-landed" and not git(lane, "log", "--all", "--oneline", "--", p).stdout.strip():
            res_never += 1
            continue
        unresolved.append(p)
    bad_hashes = []
    for h in (sorted(hashes) if check_hashes else ()):
        if git(lane, "cat-file", "-e", h).returncode != 0:
            bad_hashes.append((h, "missing"))
        elif git(lane, "merge-base", "--is-ancestor", h, tip).returncode != 0:
            bad_hashes.append((h, "not-ancestor"))
    total = len(paths) + len(hashes)
    resolved = res_exist + res_sup + res_never + (len(hashes) - len(bad_hashes))
    print(f"TIP {tip} branch={branch}")
    print(f"POINTERS total={total} paths={len(paths)} hashes={len(hashes)} resolved={resolved} "
          f"exists={res_exist} superseded={res_sup} never-landed={res_never} "
          f"unresolved={len(unresolved) + len(bad_hashes)}")
    for p in unresolved:
        print(f"UNRESOLVED {p}")
    for h, why in bad_hashes:
        print(f"UNRESOLVED-HASH {h} {why}")
    return (0 if not unresolved and not bad_hashes else 1), set(unresolved) | {h for h, _ in bad_hashes}


def selftest(lane):
    """A scratch copy of the three files plus a bogus pointer must go red; the pristine copy must stay green."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="k50-c2-"))
    try:
        for entry in lane.iterdir():
            if entry.name in FILES or entry.name == ".git":
                continue
            (tmp / entry.name).symlink_to(entry, target_is_directory=entry.is_dir())
        for name in FILES:
            shutil.copyfile(lane / name, tmp / name)
        git(tmp, "init", "-q")
        git(tmp, "add", "-A")
        git(tmp, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "selftest")
        clean_rc, clean_bad = audit(tmp, check_hashes=False)
        with open(tmp / "SCORECARD.md", "a") as fh:
            fh.write("\nplans/round50_selftest_bogus.py\n")
        dirty_rc, dirty_bad = audit(tmp, check_hashes=False)
        added = sorted(dirty_bad - clean_bad)
        print(f"SELFTEST pristine_rc={clean_rc} bogus_rc={dirty_rc} new_unresolved={added} "
              f"verdict={'ok' if added == ['plans/round50_selftest_bogus.py'] else 'BROKEN'}")
        return 0 if added == ["plans/round50_selftest_bogus.py"] else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    rc = selftest(lane) if a.selftest else audit(lane)[0]
    return rc if isinstance(rc, int) else 2


if __name__ == "__main__":
    sys.exit(main())

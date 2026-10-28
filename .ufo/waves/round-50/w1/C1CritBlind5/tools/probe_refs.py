#!/usr/bin/env python3
"""Seat R50C1CritBlind5 — refs-body probe (cross-check raised by seat R50C1ExecRepair, critique only).

Their candidate had a transient defect: a dropped `_refs` call let `n17-replace-ref` pass by *absence* of the
check rather than by the allowlist. The frozen 32 hostile modules do not cover that regression, because the
honest population is what forces `refs/replace` and `refs/notes` to be admitted — nothing forces their *bodies*
to be validated. This probe supplies that pair: the honest classes stay honest (40-hex body) and the matching
hostile fixtures carry a body git would never write.

  bl5-ref-junk-replace   `.git/refs/replace/<40 hex>` whose body is `junk`
  bl5-ref-junk-notes     `.git/refs/notes/commits` whose body is `junk`

A fence that admits refs by name/shape only admits both; a fence that validates the 40-hex body refuses both and
still admits the honest `n16`/`n17` classes.

Usage: python3 probe_refs.py --lane CLONE --fence FENCE --work DIR [--honest]   (--honest also builds n16/n17)
"""
import argparse
import importlib.util
import pathlib
import shutil
import sys

HEX40 = "a" * 40


def _repo(ctx, d, name):
    r = ctx.init(d / name)
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    return r


def build_junk_replace(ctx, d):
    r = _repo(ctx, d, "repo")
    ctx.write(r / ".git/refs/replace" / HEX40, "junk\n")
    return ["--lane", "repo"]


def build_junk_notes(ctx, d):
    r = _repo(ctx, d, "repo")
    ctx.write(r / ".git/refs/notes/commits", "junk\n")
    return ["--lane", "repo"]


FIXTURES = [
    {"fid": "bl5-ref-junk-replace", "tool": "anchor", "expect": "breach", "defects": [], "build": build_junk_replace},
    {"fid": "bl5-ref-junk-notes", "tool": "anchor", "expect": "breach", "defects": [], "build": build_junk_notes},
]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fence", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--honest", action="append", default=[])
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    hb = load(lane / "plans/honest50/build_honest_population.py", "pr_hb")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "pr_k44")
    fp = pathlib.Path(a.fence).resolve()
    fence = load(fp, "pr_fence")
    print(f"FENCE {fp} sha256={hb.sha256_file(fp)}")
    gens = [("hostile", pathlib.Path(__file__).resolve())] + [("honest", pathlib.Path(p)) for p in a.honest]
    for tag, mp in gens:
        gen = work / tag / mp.stem
        gen.mkdir(parents=True)
        for fid, tool, _e, _df, argv, d, _b in hb.build_once(k44, mp, gen):
            why = fence.breach(d, argv, tool)
            print(f"FIXTURE {fid} source={tag} verdict={'ADMIT' if why is None else 'BREACH'} why={why or ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

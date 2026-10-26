#!/usr/bin/env python3
"""R43CritValueLeg measurement harness (critic seat).

Imports the FROZEN round-43 C1 counter (plans/round43_c1_verify.py) read-only and drives its
Runner/build_battery to measure the new value-attribution leg g:

  stable   - reference double-trace record stability under jobs/seed/scratch-root variation
  spans    - per-mutant raw site records (with a RAW-dumping tracer copy) for NA18/NO7
  effect   - traced vs untraced rc/classes on every witness fixture, reference and all 9 mutants
  repro    - prepare the forced-equal SITE_EQUAL mirror for control-c1-value reproduction
"""
from __future__ import annotations

import argparse
import concurrent.futures
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
WITNESS = LANE / ".ufo/waves/round-43/claims/witness"


def load_counter():
    spec = importlib.util.spec_from_file_location("k43_c1", LANE / "plans/round43_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class SeedRunner:
    """Like mod.Runner but with a configurable PYTHONHASHSEED inside tool runs."""

    def __init__(self, mod, root, jobs, lane, seed=0):
        self._mod = mod
        self._inner = mod.Runner(root, jobs, lane)
        self._seed = seed

    def __getattr__(self, name):
        return getattr(self._inner, name)

    def env(self, tmp, span=None):
        e = self._inner.env(tmp, span)
        e["PYTHONHASHSEED"] = str(self._seed)
        return e

    def run(self, tool, variant, fx, trace=False, span=None):
        return self._inner.run(tool, variant, fx, trace=trace, span=span)

    def run_all(self, tool, variant, fixtures, trace=False, span=None):
        with concurrent.futures.ThreadPoolExecutor(self._inner.jobs) as ex:
            return list(ex.map(lambda fx: self._inner.run(tool, variant, fx, trace=trace, span=span),
                               fixtures))


def build_fixtures(mod, root, lane, bdir=WITNESS):
    fixtures, side = mod.build_battery(pathlib.Path(bdir), root, lane)
    if side != 0:
        raise SystemExit(f"sidechannel tokens found: {side}")
    (root / "fixtures.json").write_text(json.dumps(
        [{**fx, "dir": str(fx["dir"])} for fx in fixtures]))
    return fixtures


def fixtures_of(runner, tool):
    root = runner._inner.root
    data = json.loads((root / "fixtures.json").read_text())
    return [{**fx, "dir": pathlib.Path(fx["dir"])} for fx in data if fx["tool"] == tool]


def write_variants(mod, root):
    vdir = root / "variants"
    vdir.mkdir(exist_ok=True)
    refs, mutants = {}, {}
    for tool in mod.TOOLS:
        src = (LANE / mod.TOOLS[tool]).read_text()
        p = vdir / f"ref-{tool}.py"
        p.write_text(src)
        refs[tool] = p
    for row in mod.MUTANTS:
        mid, tool, _cls, _dir, _advk, _label, _wit, old, new = row
        src = (LANE / mod.TOOLS[tool]).read_text()
        if src.count(old) != 1:
            raise SystemExit(f"mutant {mid}: old not unique in {tool}")
        p = vdir / f"{mid}.py"
        p.write_text(src.replace(old, new, 1))
        start = src[: src.index(old)].count("\n") + 1
        span = set(range(start, start + new.count("\n") + 1))
        mutants[mid] = (p, span)
    return refs, mutants


def tool_of(mid):
    return "anchor" if mid.startswith("NA") else "order"


def union_spans(mod, tool):
    src = (LANE / mod.TOOLS[tool]).read_text()
    sp = set()
    for _mid, ttool, _c, _d, _k, _l, _w, old, new in mod.MUTANTS:
        if ttool == tool:
            start = src[: src.index(old)].count("\n") + 1
            sp |= set(range(start, start + new.count("\n") + 1))
    return sp


def cmd_stable(mod, args):
    # Every arm gets its own root (a fresh Runner each), so the within-arm double-trace compare is the
    # primary stability signal; a second root with the same config isolates the scratch-root axis.
    base = pathlib.Path(args.rootbase)
    arms = [
        ("j1-s0", 1, 0, "r1"),
        ("j8-s0", 8, 0, "r1"),
        ("j1-s12345", 1, 12345, "r1"),
        ("j1-s0-r2", 1, 0, "r2"),
    ]
    out = {}
    for tag, jobs, seed, rid in arms:
        root = base / rid / tag
        root.mkdir(parents=True, exist_ok=True)
        build_fixtures(mod, root, LANE)
        refs, _ = write_variants(mod, root)
        runner = SeedRunner(mod, root, jobs, LANE, seed)
        rec = {}
        for tool in mod.TOOLS:
            fxs = fixtures_of(runner, tool)
            sp = union_spans(mod, tool)
            r1a = runner.run_all(tool, refs[tool], fxs, trace=True, span=sp)
            r1b = runner.run_all(tool, refs[tool], fxs, trace=True, span=sp)
            for fx, ra, rb in zip(fxs, r1a, r1b):
                rec[fx["fid"]] = (ra, rb)
        out[tag] = rec
        for fid, (ra, rb) in rec.items():
            same = (ra[0], tuple(sorted(ra[1]))) == (rb[0], tuple(sorted(rb[1])))
            ok = same and ra[2] == rb[2] and ra[3] == rb[3]
            print(f"STABLE {tag} {fid} rc_cls_eq={same} lines_eq={ra[2]==rb[2]} sites_eq={ra[3]==rb[3]} n_sites={len(ra[3])} all_same={ok}")
            if not ok:
                print(f"  r1 rc={ra[0]} cls={sorted(ra[1])} lines={sorted(ra[2])} sites={ra[3]}")
                print(f"  r2 rc={rb[0]} cls={sorted(rb[1])} lines={sorted(rb[2])} sites={rb[3]}")
    for fid in out["j1-s0"]:
        a = out["j1-s0"][fid][0][3]
        b = out["j1-s0-r2"][fid][0][3]
        print(f"CROSSROOT {fid} sites_eq={a==b} n_a={len(a)} n_b={len(b)}")
        if a != b:
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    print(f"  first diff at {i}: a={x!r} b={y!r}")
                    break


def run_raw(runner, tool, variant, fx, span, tag):
    """Like Runner.run(trace=True) but preserves the raw tracer dump (hits / sites / RAW texts)
    before the work dirs are removed."""
    mod = runner._mod
    inner = runner._inner
    n = next(inner.seq)
    work = inner.root / "work" / f"w{n:06d}"
    tmp = inner.root / "rtmp" / f"t{n:06d}"
    work.mkdir()
    tmp.mkdir()
    src = open(variant, "rb")
    tsrc = open(inner.tracer, "rb")
    try:
        data = ((src.fileno(), mod.SLOT), (tsrc.fileno(), mod.TRACER_SLOT))
        cmd = mod.ro_sandbox(writable=(work, tmp),
                             hide=[p for p in inner.hidden() if p.exists()],
                             ro_data=data, empty=inner.empty) + [mod.PY, mod.TRACER_SLOT, mod.SLOT] + fx["argv"]
        r = subprocess.run(cmd, cwd=str(fx["dir"]), env=runner.env(tmp, span),
                           capture_output=True, text=True, timeout=600,
                           pass_fds=tuple(fd for fd, _dst in data))
        trace_path = tmp / "k43-trace.txt"
        raw = trace_path.read_text().split("\n") if trace_path.exists() else []
        outdir = inner.root / "rawdump"
        outdir.mkdir(exist_ok=True)
        (outdir / f"{tag}.txt").write_text("\n".join(raw))
        return r.returncode, mod.classes(tool, r.stdout), raw
    finally:
        src.close()
        tsrc.close()
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)


def cmd_spans(mod, args):
    tracer = mod.TRACER
    for a, b in (
        ("text = RUN.sub(\"/RUN\", ADDR.sub(\"0x\", text))",
         "text = RUN.sub(\"/RUN\", ADDR.sub(\"0x\", text))\n    RAW.append(text)"),
        ("import hashlib, os, re, runpy, sys\n",
         "import hashlib, os, re, runpy, sys\nRAW = []\n"),
        ("fh.write(\" \".join(str(n) for n in sorted(hit)) + \"\\n\" + \" \".join(sites) + \"\\n\")",
         "fh.write(\" \".join(str(n) for n in sorted(hit)) + \"\\n\" + \" \".join(sites) + \"\\n\"\n        + \"\\n\" + \"\\n\".join(RAW) + \"\\n\")"),
    ):
        if a not in tracer:
            raise SystemExit(f"tracer patch target missing: {a[:60]!r}")
        tracer = tracer.replace(a, b)

    for mid in args.mutants:
        row = next(m for m in mod.MUTANTS if m[0] == mid)
        tool = row[1]
        src = (LANE / mod.TOOLS[tool]).read_text()
        old, new = row[7], row[8]
        start = src[: src.index(old)].count("\n") + 1
        span = set(range(start, start + new.count("\n") + 1))
        root = pathlib.Path(args.rootbase) / f"span-{mid}"
        root.mkdir(parents=True, exist_ok=True)
        build_fixtures(mod, root, LANE)
        refs, mutants = write_variants(mod, root)
        runner = SeedRunner(mod, root, 1, LANE, 0)
        runner._inner.tracer.write_text(tracer)
        for k, fx in enumerate(fixtures_of(runner, tool)):
            rr1 = run_raw(runner, tool, refs[tool], fx, span, f"{mid}-{k}-ref1")
            rr2 = run_raw(runner, tool, refs[tool], fx, span, f"{mid}-{k}-ref2")
            mr = run_raw(runner, tool, mutants[mid][0], fx, span, f"{mid}-{k}-mut")
            sites1 = tuple(rr1[2][1].split()) if len(rr1[2]) > 1 else ()
            sites2 = tuple(rr2[2][1].split()) if len(rr2[2]) > 1 else ()
            sitesm = tuple(mr[2][1].split()) if len(mr[2]) > 1 else ()
            print(f"SPAN {mid} {fx['fid']} hits_ref={rr1[2][0]!r} hits_mut={mr[2][0]!r}")
            print(f"SPAN {mid} {fx['fid']} ref_sites={sites1}")
            print(f"SPAN {mid} {fx['fid']} ref2_sites={sites2} stable={sites1==sites2}")
            print(f"SPAN {mid} {fx['fid']} mut_sites={sitesm} refmut_eq={sites1==sitesm}")
            for i, (x, y) in enumerate(zip(sites1, sitesm)):
                if x != y:
                    rx = rr1[2][2 + i] if len(rr1[2]) > 2 + i else "?"
                    mx = mr[2][2 + i] if len(mr[2]) > 2 + i else "?"
                    print(f"  RAW DIFF {mid} {fx['fid']} site#{i}:")
                    print(f"    ref={rx}")
                    print(f"    mut={mx}")
                    break
            else:
                if sites1 == sitesm:
                    print(f"  RAW EQUAL {mid} {fx['fid']} (no site differs)")

def cmd_effect(mod, args):
    root = pathlib.Path(args.rootbase) / "effect"
    root.mkdir(parents=True, exist_ok=True)
    build_fixtures(mod, root, LANE)
    refs, mutants = write_variants(mod, root)
    runner = SeedRunner(mod, root, args.jobs, LANE, 0)
    for tool in mod.TOOLS:
        sp = union_spans(mod, tool)
        for fx in fixtures_of(runner, tool):
            u = runner.run(tool, refs[tool], fx, trace=False)
            t = runner.run(tool, refs[tool], fx, trace=True, span=sp)
            same = (u[0], tuple(sorted(u[1]))) == (t[0], tuple(sorted(t[1])))
            print(f"EFFECT ref {tool} {fx['fid']} untraced=({u[0]},{sorted(u[1])}) traced=({t[0]},{sorted(t[1])}) same={same}")
    for mid, (p, span) in mutants.items():
        tool = tool_of(mid)
        for fx in fixtures_of(runner, tool):
            u = runner.run(tool, p, fx, trace=False)
            t1 = runner.run(tool, p, fx, trace=True, span=span)
            t2 = runner.run(tool, p, fx, trace=True, span=span)
            same = (u[0], tuple(sorted(u[1]))) == (t1[0], tuple(sorted(t1[1])))
            stable = (t1[2], t1[3]) == (t2[2], t2[3])
            print(f"EFFECT {mid} {tool} {fx['fid']} untraced=({u[0]},{sorted(u[1])}) traced=({t1[0]},{sorted(t1[1])}) same={same} trace_stable={stable}")
            if not same:
                print(f"  DIVERGES: {u} vs {t1}")

def cmd_repro(mod, args):
    mirror = pathlib.Path(args.rootbase) / "m-value"
    (mirror / "plans/battery43").mkdir(parents=True, exist_ok=True)
    for name in ("anchor_digest_check.py", "order_check.py", "round43_c1_verify.py"):
        shutil.copy(LANE / "plans" / name, mirror / "plans" / name)
    for w in WITNESS.glob("*.py"):
        shutil.copy(w, mirror / "plans/battery43" / w.name)
    ctr = mirror / "plans/round43_c1_verify.py"
    text = ctr.read_text()
    if "return tuple(mut_sites) == tuple(ref_sites)" not in text:
        raise SystemExit("SITE_EQUAL line missing")
    text = text.replace("return tuple(mut_sites) == tuple(ref_sites)", "return True")
    ctr.write_text(text)
    print(f"MIRROR_READY {mirror}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("stable", "spans", "effect", "repro"):
        p = sub.add_parser(name)
        p.add_argument("--rootbase", default="/fast/scratch/hyaku/kengaku-r43/R43CritValueLeg/w")
        p.add_argument("--jobs", type=int, default=1)
    sub.choices["spans"].add_argument("--mutants", nargs="+", default=["NA18", "NO7"])
    a = ap.parse_args()
    mod = load_counter()
    {"stable": cmd_stable, "spans": cmd_spans, "effect": cmd_effect, "repro": cmd_repro}[a.cmd](mod, a)
    return 0


if __name__ == "__main__":
    sys.exit(main())

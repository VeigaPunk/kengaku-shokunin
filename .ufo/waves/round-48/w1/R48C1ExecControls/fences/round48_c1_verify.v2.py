#!/usr/bin/env python3
"""Round-48 C1 counter (calibration, v3): the fixture fence is admitted only when it admits every fixture of a
frozen honest population without touching a byte outside `d`, refuses every frozen hostile module without
touching a byte outside `d`, and every admission that touched nothing outside `d` is reported as BENIGN-ADMIT
instead of being counted as a leak.

Contract. `plans/round-48-claims.md` §C1 (stage-1 commit a543d920) freezes this counter as
`plans/round46_c1_verify.py` (digest-pinned below, imported unchanged) plus five deltas, restated here with the
code that implements each:

  (a) HONEST POPULATION frozen at stage 2 = the 104 fixtures of `plans/battery42`, `plans/battery43`,
      `plans/battery44` plus the 16 novel honest modules committed at stage 2 under `plans/honest48/` and pinned
      below by digest: the nine round-46 novel classes rebuilt from their `w2` report description (`n01`-`n09`,
      authored against the *base* fence description, never against a repaired fence) and the seven classes
      authored in round 48 (`n10`-`n16`). `HONEST_TOTAL` is the stage-2 literal <H> and
      `HONEST_NOVEL_EXPECTED` the literal number of novel fixtures, so a population that loses or mixes its
      novel half cannot pass on the 104 battery fixtures alone.
  (b) BEHAVIOURAL CLASSIFICATION. Per fixture: `LEAK` = admitted AND traced opens/reads outside `d` observed;
      `BENIGN-ADMIT` = admitted with zero traced outside access; `READ` = refused but traced outside access
      observed; `HUNG`; `ERROR` = the harness exit status carried neither decision. Only LEAK counts as `leaked`;
      BENIGN-ADMIT is counted on its own `BENIGN` line and is never a leak. The kill rule keys on hostile
      behaviour: a hostile fixture admitted with outside access is a LEAK. A module is `clean` only when every
      fixture it builds was refused with zero outside access, so a BENIGN-ADMIT in a hostile leg leaves
      `clean<total` and the frozen line below cannot print (this counter is stricter than the kill rule, which
      names only outside-access admissions; it is never looser). An ERROR module is never clean: it is reported
      on `ERRORS` and keeps the frozen line from printing, with LEAK/READ keeping their strict meanings.
  (c) NAME HIDING (Q39) retained: fixture dirs, build dirs, fixture parents and module copies are named by a
      per-run `secrets` token, every parent is padded to `PAD` decoy children, and build and fence order are
      shuffled — all of it inherited from the round-46 counter's `build_module`/main ordering, which this file
      calls rather than copies.
  (d) STRACE ENVELOPE B1/B3/B4/B5/B6 retained by importing the round-46 counter's `run_fence`/`analyse`
      unchanged: the log lives outside the read-only sandbox, the whole scratch root is in scope, the
      stat/access/exec/write families count, `<unfinished ...>`/`<... resumed>` are decoded, and the verdict
      travels as the harness exit status (10 BREACH, 11 ADMIT, 12 error), never as parsed stdout.
  (e) REFUSALS = the 20 frozen `plans/refusals46/` modules; SEALED = the 12 frozen `plans/sealed46/` modules
      plus the wave-1 held-out hostile modules authored against the *landed* fence, committed at stage 2 under
      `plans/sealed48/` and pinned by digest. `SEALED_FLOOR` is the stage-2 literal <S>.

Frozen predicate (same lines as `plans/round-48-claims.md` §C1; the L1 fills `<P>`, `<S>`, `<H>` at the stage-2
amendment, together with the pins of `plans/sealed48/` and the 16 novel honest modules under `plans/honest48/`):
  C1 passes iff `python3 plans/round48_c1_verify.py --lane .` prints `PINS total=<P> mismatched=0`, then
  `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, then
  `SEALED total=<S> clean=<S> leaked=0 read=0 hung=0 build_errors=0`, then
  `HONEST fixtures=<H> admitted=<H> refused=0 read=0 hung=0 build_errors=0`, then `BENIGN total=<B>`, then
  `CALIBRATION advertised=<20+S> contradicted=0`, then `PREDICATE R48-C1 pass`, exit 0, on a clean clone of the
  landing tip.

Receipts (Q22): the first line this counter prints is `REV <40-hex>` of the tree it measured; a dirty tree is
reported as `TREE dirty=<n>` and fails the predicate in the frozen (default) mode, because the predicate is
bound to a clean clone.

ORDERING (Q30). This counter scores the *landed* fence. It must not be run as a pass/fail receipt on any tree
before the stage-2 amendment commit exists: wave-1 candidates are only selftested, with `--fence`, on scratch
clones of the base, and the predicate they print is the predicate of the whole lane that happens to be checked
out, never an admission of R48-C1.

Limits, named: io_uring SQE opens/reads emit no traced syscall (B7, not exploited; `io_uring_*` is not blocked);
host paths outside the scratch root are not counted, so a fence may still read `/etc`, `/proc` and `/sys` while
deciding; a directory stat's `st_nlink` channel is nulled by padding, not measured; a module that fails to
build contributes no fixtures and is reported per leg; `BENIGN total=` counts fixtures (not modules) across all
three legs, and per-leg module counts are printed on `BENIGN-MODULES`; the novel honest population is lane
files pinned in `PINS_EXTRA`, so a missing, extra or edited novel module is a `PINS` mismatch rather than a
silent narrowing of the honest leg, and `HONEST_NOVEL_EXPECTED` binds the novel count from the other side;
`--refusals`, `--sealed`, `--honest`, `--fence` and `--seed` are testing overrides, and the predicate they print
is the predicate of the inputs they name (never a receipt for the frozen run).

  --lane DIR       lane (or clone) to measure; default `.`
  --work DIR       scratch parent (must lie outside the lane; default $TMPDIR)
  --jobs N         parallel fence runs (default 8)
  --refusals DIR   testing only: refusal modules from DIR
  --sealed DIR     testing only: sealed modules from DIR
  --honest DIR     testing only: extra honest modules from DIR
  --fence PATH     testing only: run the fence at PATH instead of plans/fixture_fence.py
  --seed HEX       testing only: fix the per-run token seed (names stay opaque; receipts reproduce)
  --literals       print the measured population counts and the PIN lines a stage-2 amendment must paste
                   in; build and trace nothing; exit 0

Exit 0 pass, 1 fail, 2 setup error.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import pathlib
import random
import secrets
import shutil
import subprocess
import sys
import tempfile

K44_REL = "plans/round44_c1_verify.py"
R46_REL = "plans/round46_c1_verify.py"
R46_PIN = "ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508"   # plans/round46_c1_verify.py @ a543d920
FENCE_REL = "plans/fixture_fence.py"
REFUSAL_REL = "plans/refusals46"
SEALED_REL = "plans/sealed46"
REFUSAL_SOURCE_REL = "plans/refusals45"
HONEST_RELS = ("plans/battery42", "plans/battery43", "plans/battery44")
HONEST_EXTRA_REL = "plans/honest48"     # stage 2: the 16 novel honest modules, pinned below
SEALED_EXTRA_REL = "plans/sealed48"     # stage 2: wave-1 held-out hostile modules, pinned below
# STAGE-2 LITERALS. `--literals` measures the population the committed tree actually holds; the amendment
# copies the numbers and the PIN lines back into this block. Nothing else in this file may change at stage 2.
REFUSAL_FLOOR = 20                       # <R>, frozen exact
SEALED_FLOOR = 12                        # <S>: 12 + len(plans/sealed48/*.py)
HONEST_BATTERY = 104                     # the standing batteries, pinned by the round-46 table
HONEST_NOVEL_EXPECTED = 16               # novel fixtures: 9 r46novel (n01-n09) + 7 novel48 (n10-n16)
HONEST_TOTAL = 120                       # <H>: HONEST_BATTERY + HONEST_NOVEL_EXPECTED
# The 16 novel honest modules exactly as delivered by `.ufo/waves/round-48/w1/R48C1ExecHonest/modules/`
# (verified against that seat's `modules.sha256`); the stage-2 amendment commits them under `plans/honest48/`
# at these digests. A file there that is not listed, or a listed file whose bytes moved, is a PINS mismatch.
PINS_EXTRA: dict[str, str] = {
    "plans/honest48/n10_empty_repo.py": "04919778ef5f75a081517149d8bc84582622971a9a1e24da7df883446e737e3f",
    "plans/honest48/n11_multibranch.py": "72c2433ec8bb4898b7e7949a443f6fdc3c69aa9f1b3496366de50eba98116bb0",
    "plans/honest48/n12_local_config_user.py": "6c501b23fed7a8e3b1f9c20e3e45bc8707a087938c79ad9cdb78df8b425af952",
    "plans/honest48/n13_remote_origin.py": "34b2ca158cf3ce4d82484db06a065d88458064ae29fb4321e039d8a54e835d9d",
    "plans/honest48/n14_stash_entry.py": "3e288c6d5786520a101313e19f148bf79c6130470f753b911c6ba83409d3db92",
    "plans/honest48/n15_commit_graph.py": "4f34a149fa7e4018727cea5c1f421107dd1fda747b0c4de2cead45723be3f4c0",
    "plans/honest48/n16_notes_ref.py": "fabcc598e6117e469532e3f6bb1b297468eb27c3878f6f7faa5668a98a2a4ae6",
    "plans/honest48/n01_packed_refs.py": "9e1a2058e326781e0fb7007f041c2f13caa21b93fbd9cea6f668eb3765dac853",
    "plans/honest48/n02_annotated_tag.py": "9eda83c41d1442e14a25b48e17aa2024981d8d4b127d1507f714b911ecc10c16",
    "plans/honest48/n03_detached_head.py": "e9bd62d3341d645f34c2372b9076b92dfdefd5a3caf7d669119426edaae71e7a",
    "plans/honest48/n04_merge_commit.py": "ae6eed2fc058ebc9602b43daa9b04655bdc327d6d6d4f769adc22f3f56386daf",
    "plans/honest48/n05_gitignore.py": "59de03481bee3763087e2f2b2a92c64966952e9cdba8b11c1ed579f40cce8d24",
    "plans/honest48/n06_linear_30.py": "98035b8f551bc1818be09e3a987ef1fcf46356d90135ed3724e23b3879bad011",
    "plans/honest48/n07_reflog_gc.py": "8afa31c42b5075ea64cb53b18fc1d17af0dcb98330f521989fbb61e659c16f51",
    "plans/honest48/n08_tag_detached.py": "66eacd43caa995748677687ad4218ce1049ebc114a087e8405bec8f3c53c0f98",
    "plans/honest48/n09_ignored_untracked.py": "94fe3220722e18b02354e505ff4f7f51c4f3c2214fc9f91b81094150f8214c1b",
}

KINDS = ("clean", "benign", "leak", "read", "hung", "error")


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_r46(lane):
    """Import the round-46 counter only when its bytes match the stage-1 pin."""
    got = sha256(lane / R46_REL)
    if got != R46_PIN:
        print(f"SETUP {R46_REL} sha256={got} is not the pinned {R46_PIN}", file=sys.stderr)
        return None
    return load(lane / R46_REL, "kengaku_r46_counter")


def rev(lane):
    """(40-hex HEAD or 40 zeros, dirty count or -1). `--no-optional-locks` keeps the measurement read-only."""
    head = subprocess.run(["git", "--no-optional-locks", "-C", str(lane), "rev-parse", "HEAD"],
                          capture_output=True, text=True)
    st = subprocess.run(["git", "--no-optional-locks", "-C", str(lane), "status", "--porcelain"],
                        capture_output=True, text=True)
    if head.returncode != 0 or st.returncode != 0:
        return "0" * 40, -1
    return head.stdout.strip() or "0" * 40, len([l for l in st.stdout.splitlines() if l.strip()])


def kind_of(verdict, hits):
    """Delta (b): the four hostile buckets, BENIGN-ADMIT, and ERROR kept out of both leak and read."""
    if verdict == "HUNG":
        return "hung"
    if verdict == "ERROR":
        return "error"
    if verdict == "ADMIT":
        return "leak" if hits else "benign"
    return "read" if hits else "clean"


def module_rollup(rows):
    """One hostile module -> one of the frozen buckets. Not clean unless every fixture it claims was refused
    untouched; a module that built no fixture at all did not produce the module it claims, so it is a build
    error and never clean."""
    if not rows:
        return "build_errors"
    kinds = {r["kind"] for r in rows}
    for k in ("leak", "error", "hung", "benign", "read"):
        if k in kinds:
            return k
    return "clean"


def pin_issues(lane, k46, extra_dirs, default_mode):
    """Every pinned file at its digest, and (default mode) every file of a frozen population pinned — an
    unpinned input cannot print `mismatched=0`."""
    pins = dict(k46.PINS)
    pins[R46_REL] = R46_PIN
    issues = [rel for rel, dig in pins.items() if sha256(lane / rel) != dig]
    if default_mode:
        for d in extra_dirs:
            if not d.is_dir():
                continue
            for f in sorted(d.glob("*.py")):
                rel = f.relative_to(lane).as_posix()
                if rel not in PINS_EXTRA:
                    issues.append(rel + ":unpinned")
        for rel, dig in PINS_EXTRA.items():
            if sha256(lane / rel) != dig:
                issues.append(rel)
    return pins, issues


def module_files(d):
    return sorted(d.glob("*.py")) if d.is_dir() else []


def literal_report(lane, refdir, sealdir, honest_extra, sealed_extra):
    """Measure the population the tree holds and print what the stage-2 amendment must paste."""
    refusal = module_files(refdir)
    sealed_frozen = module_files(sealdir)
    sealed_extra_files = module_files(sealed_extra)
    honest_battery = [f for rel in HONEST_RELS for f in module_files(lane / rel)]
    honest_novel = module_files(honest_extra)
    print(f"LITERALS refusals={len(refusal)} sealed_frozen={len(sealed_frozen)}"
          f" sealed_extra={len(sealed_extra_files)} honest_battery_modules={len(honest_battery)}"
          f" honest_battery_fixtures={HONEST_BATTERY} honest_novel_modules={len(honest_novel)}"
          f" pins_extra={len(PINS_EXTRA)}")
    print(f'LITERALS-TO-PASTE REFUSAL_FLOOR={len(refusal)}'
          f" SEALED_FLOOR={len(sealed_frozen) + len(sealed_extra_files)}"
          f" HONEST_TOTAL={HONEST_BATTERY + len(honest_novel)}")
    for f in sealed_extra_files + honest_novel:
        print(f'PIN "{f.relative_to(lane).as_posix()}" "{sha256(f)}"')
    print("REV " + rev(lane)[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--refusals", default=None, help="testing only: refusal module dir")
    ap.add_argument("--sealed", default=None, help="testing only: sealed module dir")
    ap.add_argument("--honest", default=None, help="testing only: extra honest module dir")
    ap.add_argument("--fence", default=None, help="testing only: fence file under test")
    ap.add_argument("--seed", default=None, help="testing only: fixed token seed")
    ap.add_argument("--literals", action="store_true", help="print the stage-2 literals and pins; run nothing")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    rng = secrets.SystemRandom() if a.seed is None else random.Random(int(a.seed, 16))
    default_mode = (a.refusals is None and a.sealed is None and a.honest is None and a.fence is None
                    and a.seed is None and not a.literals)
    refdir = pathlib.Path(a.refusals).resolve() if a.refusals else lane / REFUSAL_REL
    sealdir = pathlib.Path(a.sealed).resolve() if a.sealed else lane / SEALED_REL
    hon_dir = pathlib.Path(a.honest).resolve() if a.honest else lane / HONEST_EXTRA_REL
    seal_extra = lane / SEALED_EXTRA_REL
    fence_src = pathlib.Path(a.fence).resolve() if a.fence else lane / FENCE_REL
    head, dirty = rev(lane)
    print(f"REV {head}")
    print("TREE clean" if dirty == 0 else f"TREE dirty={dirty}" + ("" if default_mode else " (override)"))
    k46 = load_r46(lane)
    if k46 is None:
        return 2
    pins, issues = pin_issues(lane, k46, (hon_dir, seal_extra), default_mode)
    print(f"PINS total={len(pins) + len(PINS_EXTRA)} mismatched={len(issues)}"
          + (f" first={issues[0]}" if issues else ""))
    for rel in issues[1:]:
        print(f"PIN-MISMATCH {rel}")
    if a.literals:
        literal_report(lane, refdir, sealdir, hon_dir, seal_extra)
        return 0
    if R46_REL in issues:
        print("SETUP the round-46 counter (contract) is not at its pinned digest", file=sys.stderr)
        return 2
    for exe in ("/usr/bin/bwrap", "/usr/bin/python3", k46.STRACE):
        if not os.access(exe, os.X_OK):
            print(f"SETUP {exe} is required", file=sys.stderr)
            return 2
    k44 = load(lane / K44_REL, "kengaku_r44_counter")

    if a.work:
        if pathlib.Path(a.work).resolve().is_relative_to(lane):
            print("SETUP --work must not lie inside the lane", file=sys.stderr)
            return 2
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k48-c1-", dir=a.work)).resolve()
    if root.is_relative_to(lane):
        print("SETUP scratch root lies inside the lane; pass --work", file=sys.stderr)
        shutil.rmtree(root, ignore_errors=True)
        return 2
    empty = pathlib.Path(tempfile.mkdtemp(prefix=root.name + "-empty-", dir=root.parent))
    try:
        ctl = root / "ctl"
        ctl.mkdir()
        (ctl / "harness.py").write_text(k46.HARNESS)
        fence_copy = ctl / "fence.py"
        if not fence_src.is_file():
            print(f"FENCE {fence_src} absent")
            fence_copy.write_text("def breach(d, argv, tool):\n    raise RuntimeError('fence absent')\n")
        else:
            fence_copy.write_bytes(fence_src.read_bytes())
            print(f"FENCE source={fence_src} sha256={sha256(fence_copy)}")
        honest_battery = [f for rel in HONEST_RELS for f in module_files(lane / rel)]
        honest_novel = module_files(hon_dir)
        groups = {
            "refusal": module_files(refdir),
            "sealed": module_files(sealdir) + (module_files(seal_extra) if sealdir == lane / SEALED_REL else []),
            "honest": honest_battery + honest_novel,
        }
        # (a): the honest leg's two halves are counted apart, so `HONEST_NOVEL_EXPECTED` can bind the novel
        # half on its own and a battery-only population cannot print the frozen line.
        pop = {("honest", f): "battery" for f in honest_battery}
        pop.update({("honest", f): "novel" for f in honest_novel})
        print(f"LITERALS refusals={REFUSAL_FLOOR} sealed={SEALED_FLOOR} honest={HONEST_TOTAL}")
        print(f"LAYOUT refusals={refdir} sealed={sealdir} honest_extra={hon_dir} sealed_extra={seal_extra}"
              f" novel={len(honest_novel)} pad={k46.PAD} jobs={a.jobs}")
        if default_mode:
            cp_bad = k46.copy_rows(refdir, lane) if refdir.is_dir() else []
        else:
            cp_bad = []
            print("COPY-CHECK skipped (refusals dir overridden for testing)")
        for g in ("refusal", "sealed", "honest"):
            print(f"MODULES {g} total={len(groups[g])}"
                  + ("" if groups[g] else " (directory absent or empty)"))
        built: dict[str, list] = {g: [] for g in groups}
        build_errors = {g: 0 for g in groups}
        order = [(g, f) for g in groups for f in groups[g]]
        rng.shuffle(order)                                 # (c): build order carries no signal
        for g, f in order:
            try:
                built[g].append((f, k46.build_module(k44, lane, root, empty, f, rng, ctl)))
            except (RuntimeError, ValueError, KeyError, TypeError, json.JSONDecodeError,
                    subprocess.TimeoutExpired) as e:
                build_errors[g] += 1
                print(f"BUILD-ERROR {g} {f.name} {str(e)[:160]}")
        jobs = [(g, f, fx) for g in built for f, fxs in built[g] for fx in fxs]
        rng.shuffle(jobs)                                  # (c): run order carries no signal
        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as ex:
            res = list(ex.map(lambda t: k46.run_fence(k44, lane, root, ctl, empty, fence_copy, t[1][2], t[0]),
                              enumerate(jobs)))
        per: dict[tuple[str, pathlib.Path], list] = {}
        for (g, f, fx), (verdict, why, hits, calls) in zip(jobs, res):
            kind = kind_of(verdict, len(hits))
            per.setdefault((g, f), []).append({"fx": fx, "verdict": verdict, "why": why, "hits": hits,
                                               "calls": calls, "kind": kind})
            head_hit = f"{hits[0][0]}:{hits[0][1]}" if hits else ""
            print(f"FENCE-RUN {g} {fx['module']} {fx['fid']} {verdict} {kind} touches={len(hits)}"
                  f" calls={calls}" + (f" first={head_hit}" if head_hit else "")
                  + (f" -- {why}" if why else ""))

        def hostile_leg(g):
            tally = {k: 0 for k in ("clean", "leak", "read", "hung", "build_errors", "benign", "error")}
            for f, fxs in built[g]:
                rows = per.get((g, f), [])
                bucket = module_rollup(rows)
                tally[bucket] += 1
                print(f"{g.upper()} {f.name} {bucket.upper()} fixtures={len(rows)}"
                      f" admitted={sum(r['verdict'] == 'ADMIT' for r in rows)}"
                      f" hung={sum(r['verdict'] == 'HUNG' for r in rows)}"
                      f" touches={sum(len(r['hits']) for r in rows)}")
            tally["build_errors"] += build_errors[g] + (len(cp_bad) if g == "refusal" else 0)
            return tally, len(groups[g])

        rt, rtotal = hostile_leg("refusal")
        print(f"REFUSALS total={rtotal} clean={rt['clean']} leaked={rt['leak']} read={rt['read']}"
              f" hung={rt['hung']} build_errors={rt['build_errors']}")
        st, stotal = hostile_leg("sealed")
        print(f"SEALED total={stotal} clean={st['clean']} leaked={st['leak']} read={st['read']}"
              f" hung={st['hung']} build_errors={st['build_errors']}")
        hrows = [r for (g, _f), rows in per.items() if g == "honest" for r in rows]
        h_adm = sum(r["kind"] == "benign" for r in hrows)
        h_ref = sum(r["kind"] in ("clean", "read") for r in hrows)
        h_read = sum(bool(r["hits"]) for r in hrows)
        h_hung = sum(r["kind"] == "hung" for r in hrows)
        hbuild = build_errors["honest"]
        print(f"HONEST fixtures={len(hrows)} admitted={h_adm} refused={h_ref} read={h_read} hung={h_hung}"
              f" build_errors={hbuild}")
        novel_rows = [r for (g, f), rows in per.items() if pop.get((g, f)) == "novel" for r in rows]
        print(f"HONEST-POP battery={sum(len(r) for (g, f), r in per.items() if pop.get((g, f)) == 'battery')}"
              f" novel={len(novel_rows)} expected_novel={HONEST_NOVEL_EXPECTED}"
              f" novel_modules={len(honest_novel)}")
        benign = {g: 0 for g in groups}
        for (g, _f), rows in per.items():
            benign[g] += sum(r["kind"] == "benign" for r in rows)
        benign_fx = sum(benign.values())
        print(f"BENIGN total={benign_fx}")
        print(f"BENIGN-MODULES refusals={benign['refusal']} sealed={benign['sealed']} honest={benign['honest']}")
        errors = rt["error"] + st["error"] + sum(r["kind"] == "error" for r in hrows)
        if errors:
            print(f"ERRORS total={errors}")
        contradicted = rt["leak"] + rt["read"] + rt["hung"] + st["leak"] + st["read"] + st["hung"]
        print(f"CALIBRATION advertised={rtotal + stotal} contradicted={contradicted}")
        after = [rel for rel, dig in pins.items() if sha256(lane / rel) != dig]
        fails = []
        if issues:
            fails.append(f"pins={len(issues)}")
        if after:
            fails.append(f"pins-after={len(after)}")
        if default_mode and dirty != 0:
            fails.append(f"tree-dirty={dirty}")
        if rtotal != REFUSAL_FLOOR:
            fails.append(f"refusals-total={rtotal}!={REFUSAL_FLOOR}")
        if (rt["clean"] != rtotal or rt["leak"] or rt["read"] or rt["hung"] or rt["build_errors"]
                or rt["benign"] or rt["error"]):
            fails.append("refusals-not-clean")
        if stotal != SEALED_FLOOR:
            fails.append(f"sealed-total={stotal}!={SEALED_FLOOR}")
        if (st["clean"] != stotal or st["leak"] or st["read"] or st["hung"] or st["build_errors"]
                or st["benign"] or st["error"]):
            fails.append("sealed-not-clean")
        if len(novel_rows) != HONEST_NOVEL_EXPECTED:
            fails.append(f"honest-novel={len(novel_rows)}!={HONEST_NOVEL_EXPECTED}")
        if len(hrows) != HONEST_TOTAL:
            fails.append(f"honest-fixtures={len(hrows)}!={HONEST_TOTAL}")
        if h_adm != HONEST_TOTAL or h_ref or h_read or h_hung or hbuild:
            fails.append("honest-not-admitted")
        if errors:
            fails.append(f"errors={errors}")
        if contradicted:
            fails.append(f"contradicted={contradicted}")
        good = not fails
        print("REASON " + (",".join(fails) if fails else "-"))
        print(f"PREDICATE R48-C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(empty, ignore_errors=True)
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

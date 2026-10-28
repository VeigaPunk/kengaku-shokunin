#!/usr/bin/env python3
"""Round-49 C1 counter (calibration, v3): the fixture fence is admitted only when it admits every fixture of a
frozen honest population without touching a byte outside `d`, refuses every frozen hostile module without
touching a byte outside `d`, survives the frozen mutant battery, and every admission that touched nothing
outside `d` is reported as BENIGN-ADMIT instead of being counted as a leak.

Contract. `plans/round-49-claims.md` §C1 (stage-1 commit 9d2900a) freezes this counter as
`plans/round46_c1_verify.py` (digest-pinned below, imported unchanged) plus six deltas, restated here with the
code that implements each:

  (a) HONEST POPULATION frozen at stage 2 = the 104 fixtures of `plans/battery42`, `plans/battery43`,
      `plans/battery44` plus the novel honest classes authored by wave-1 seats against the *base* fence
      description, committed at stage 2 under `plans/honest49/` and pinned below by digest.
      `HONEST_NOVEL_EXPECTED` is the stage-2 literal number of novel fixtures and `HONEST_TOTAL` the literal
      <H>, so a population that loses or mixes its novel half cannot pass on the 104 battery fixtures alone.
  (b) BEHAVIOURAL CLASSIFICATION. Per fixture: `LEAK` = admitted AND traced opens/reads outside `d` observed;
      `BENIGN-ADMIT` = admitted with zero traced outside access; `READ` = refused but traced outside access
      observed; `HUNG`; `ERROR` = the harness exit status carried neither decision. Only LEAK counts as
      `leaked`; BENIGN-ADMIT is counted on its own `BENIGN` line and is never a leak. The kill rule keys on
      hostile behaviour: a hostile fixture admitted with outside access is a LEAK. A module is `clean` only
      when every fixture it builds was refused with zero outside access, so a BENIGN-ADMIT in a hostile leg
      leaves `clean<total` and the frozen line below cannot print (this counter is stricter than the kill
      rule, which names only outside-access admissions; it is never looser). An ERROR module is never clean: it
      is reported on `ERRORS` and keeps the frozen line from printing, with LEAK/READ keeping their strict
      meanings.
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
      `plans/sealed49/` and pinned by digest. `SEALED_TOTAL` is the stage-2 literal <S>.
  (f) MUTANTS leg (new; the round-48 routed gap). `<M>` fence mutants are declared in
      `plans/mutants49/c1-mutants.json` — one object per mutant with `id`, the `payload` path of a mutated copy
      of the landed fence (lane-relative or absolute), the payload's sha256 `digest`, and a `description`;
      either `{"mutants": [...]}` or a bare list. The counter verifies each payload's digest, applies it by
      replacing the fence copy the harness loads, and re-measures all three legs on that copy: a mutant is
      *caught* iff the mutated fence no longer prints the clean signature (any new hostile leak/read/hang, any
      hostile module no longer refused, any honest refusal, or any harness error). A payload that does not
      parse, does not define `breach`, or does not match its digest is reported `broken` — never counted as
      caught, and the predicate fails with `mutants-broken`. Fewer than `<M>/2` caught prints
      `MUTANTS total=<M> caught=<k> floor=<M>/2 verdict=unmet` and fails the predicate; `<M>` below the
      frozen `MUTANT_MIN=12` also fails it. The harness for every variant is the round-46 `HARNESS` text, and
      the fixtures are built once and re-used, so one battery costs one build and `<M>+1` fence passes.

Frozen predicate (same lines as `plans/round-49-claims.md` §C1; the L1 fills `<P>`, `<S>`, `<H>`, `<M>` at the
stage-2 amendment, together with the pins of `plans/sealed49/`, `plans/honest49/` and the mutant payloads):
  C1 passes iff `python3 plans/round49_c1_verify.py --lane .` prints `PINS total=<P> mismatched=0`, then
  `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, then
  `SEALED total=<S> clean=<S> leaked=0 read=0 hung=0 build_errors=0`, then
  `HONEST fixtures=<H> admitted=<H> refused=0 read=0 hung=0 build_errors=0`, then `BENIGN total=<B>`, then
  `MUTANTS total=<M> caught=<k> floor=<M>/2 verdict=met`, then
  `CALIBRATION advertised=<20+S> contradicted=0`, then `PREDICATE R49-C1 pass`, exit 0, on a clean clone of the
  landing tip.

Receipts (Q22): the first line this counter prints is `REV <40-hex>` of the tree it measured; a dirty tree is
reported as `TREE dirty=<n>` and fails the predicate in the frozen (default) mode, because the predicate is
bound to a clean clone.

ORDERING (Q30). This counter scores the *landed* fence. It must not be run as a pass/fail receipt on any tree
before the stage-2 amendment commit exists: wave-1 candidates are only selftested, with `--fence` and/or
`--mutants`, on scratch clones of the base, and the predicate they print is the predicate of the whole lane that
happens to be checked out, never an admission of R49-C1.

Limits, named: io_uring SQE opens/reads emit no traced syscall (B7, not exploited; `io_uring_*` is not blocked);
host paths outside the scratch root are not counted, so a fence may still read `/etc`, `/proc` and `/sys` while
deciding; a directory stat's `st_nlink` channel is nulled by padding, not measured; a module that fails to
build contributes no fixtures and is reported per leg; `BENIGN total=` counts fixtures (not modules) across all
three legs, and per-leg module counts are printed on `BENIGN-MODULES`; the novel honest population is lane files
pinned in `PINS_EXTRA`, so a missing, extra or edited novel module is a `PINS` mismatch rather than a silent
narrowing of the honest leg; a mutant payload is trusted exactly as far as its pinned digest, and a mutant that
changes only bytes no leg observes *survives* by design (the floor, not any single mutant, is the claim); the
mutant battery re-uses one build, so a mutant cannot be caught merely by perturbing fixture construction;
`--refusals`, `--sealed`, `--honest`, `--fence`, `--mutants` and `--seed` are testing overrides, and the
predicate they print is the predicate of the inputs they name (never a receipt for the frozen run).

  --lane DIR       lane (or clone) to measure; default `.`
  --work DIR       scratch parent (must lie outside the lane; default $TMPDIR)
  --jobs N         parallel fence runs (default 8)
  --refusals DIR   testing only: refusal modules from DIR
  --sealed DIR     testing only: sealed modules from DIR
  --honest DIR     testing only: extra honest modules from DIR
  --fence PATH     testing only: run the fence at PATH instead of plans/fixture_fence.py
  --mutants PATH   testing only: mutant declarations from PATH instead of plans/mutants49/c1-mutants.json
  --seed HEX       testing only: fix the per-run token seed (names stay opaque; receipts reproduce)
  --literals       print the measured population counts and the PIN lines a stage-2 amendment must paste in;
                   build and trace nothing; exit 0

Exit 0 pass, 1 fail, 2 setup error.
"""
from __future__ import annotations

import argparse
import ast
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import pathlib
import random
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

K44_REL = "plans/round44_c1_verify.py"
R46_REL = "plans/round46_c1_verify.py"
R46_PIN = "ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508"   # plans/round46_c1_verify.py @ 3a548330
FENCE_REL = "plans/fixture_fence.py"
REFUSAL_REL = "plans/refusals46"
SEALED_REL = "plans/sealed46"
HONEST_RELS = ("plans/battery42", "plans/battery43", "plans/battery44")
HONEST_EXTRA_REL = "plans/honest49"     # stage 2: novel honest modules, pinned below
SEALED_EXTRA_REL = "plans/sealed49"     # stage 2: wave-1 held-out hostile modules, pinned below
MUTANTS_REL = "plans/mutants49/c1-mutants.json"
# STAGE-2 LITERALS. `--literals` measures the population the committed tree actually holds; the amendment
# copies the numbers and the PIN lines back into this block. Nothing else in this file may change at stage 2.
REFUSAL_FLOOR = 20                       # <R>, frozen exact
SEALED_FROZEN = 12                       # plans/sealed46, exact
SEALED_TOTAL = 12                        # <S>: SEALED_FROZEN + the plans/sealed49 modules, filled at stage 2
HONEST_BATTERY = 104                     # fixtures of battery42|43|44, pinned by the round-46 table
HONEST_NOVEL_EXPECTED = 0                # novel fixtures under plans/honest49, filled at stage 2
HONEST_TOTAL = 104                       # <H>: HONEST_BATTERY + HONEST_NOVEL_EXPECTED
MUTANT_MIN = 12                          # frozen predicate: <M> >= 12
MUTANT_FLOOR = 0                         # <M>: 0 = unfilled, measured from the JSON (must be >= MUTANT_MIN)
# The novel honest modules as delivered by the wave-1 honest seats and the held-out hostile modules as
# delivered by the wave-1 fence seats; the stage-2 amendment commits them under `plans/honest49/` and
# `plans/sealed49/` at these digests. A file there that is not listed, or a listed file whose bytes moved, is a
# PINS mismatch. Empty here on purpose: wave 1 pins nothing, so `--literals` is what fills this block.
PINS_EXTRA: dict[str, str] = {}


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


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


def load_mutants(path):
    """Delta (f): [[{id, description, payload, digest}]], issues. Accepts {"mutants": [...]} or a bare list;
    every row needs an id/`payload` path and a 64-hex sha256 `digest`."""
    p = pathlib.Path(path)
    if not p.is_file():
        return [], [f"{p}:absent"]
    try:
        raw = json.loads(p.read_text())
    except (OSError, json.JSONDecodeError) as e:
        return [], [f"{p}:unreadable {type(e).__name__}"]
    rows = raw.get("mutants") if isinstance(raw, dict) else raw
    if not isinstance(rows, list):
        return [], [f"{p}:no-mutants-list"]
    out, issues = [], []
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            issues.append(f"row{i}:not-an-object")
            continue
        mid = str(r.get("id") or f"m{i + 1:02d}")
        rel = r.get("payload") or r.get("path")
        dig = r.get("digest") or r.get("sha256")
        desc = str(r.get("description") or r.get("desc") or "")
        if not isinstance(rel, str) or not rel:
            issues.append(f"{mid}:no-payload")
            continue
        if not isinstance(dig, str) or not re.fullmatch(r"[0-9a-f]{64}", dig):
            issues.append(f"{mid}:no-digest")
            continue
        out.append({"id": mid, "description": desc, "payload": rel, "digest": dig})
    if isinstance(raw, dict) and isinstance(raw.get("total"), int) and raw["total"] != len(out):
        issues.append(f"declared-total={raw['total']}!=rows={len(out)}")
    return out, issues


def mutant_bytes(lane, e):
    """Delta (f): the payload is a full mutated copy of the landed fence. Apply = load it in place of the fence
    copy the harness imports. Returns (bytes, why); a payload that cannot be applied is `broken`, never caught."""
    p = pathlib.Path(e["payload"])
    if not p.is_absolute():
        p = lane / p
    try:
        b = p.read_bytes()
    except OSError as x:
        return None, f"unreadable {type(x).__name__}"
    got = sha256_bytes(b)
    if got != e["digest"]:
        return None, f"digest {got[:12]}!={e['digest'][:12]}"
    try:
        tree = ast.parse(b.decode("utf-8"))
    except (UnicodeDecodeError, SyntaxError) as x:
        return None, f"unparseable {type(x).__name__}"
    if not any(isinstance(n, ast.FunctionDef) and n.name == "breach" for n in tree.body):
        return None, "no top-level breach()"
    return b, ""


def literal_report(lane, refdir, sealdir, honest_extra, sealed_extra, mut_entries, mut_issues):
    """Measure the population the tree holds and print what the stage-2 amendment must paste."""
    refusal = module_files(refdir)
    sealed_frozen = module_files(sealdir)
    sealed_extra_files = module_files(sealed_extra)
    honest_battery = [f for rel in HONEST_RELS for f in module_files(lane / rel)]
    honest_novel = module_files(honest_extra)
    print(f"LITERALS refusals={len(refusal)} sealed_frozen={len(sealed_frozen)}"
          f" sealed_extra={len(sealed_extra_files)} honest_battery_modules={len(honest_battery)}"
          f" honest_battery_fixtures={HONEST_BATTERY} honest_novel_modules={len(honest_novel)}"
          f" mutants={len(mut_entries)} pins_extra={len(PINS_EXTRA)}")
    print(f'LITERALS-TO-PASTE REFUSAL_FLOOR={len(refusal)}'
          f" SEALED_EXTRA_EXPECTED={len(sealed_extra_files)}"
          f" SEALED_TOTAL={len(sealed_frozen) + len(sealed_extra_files)}"
          f" HONEST_NOVEL_EXPECTED={len(honest_novel)} MUTANT_FLOOR={len(mut_entries)}")
    for i in mut_issues:
        print(f"MUTANT-ISSUE {i}")
    for f in sealed_extra_files + honest_novel:
        print(f'PIN "{f.relative_to(lane).as_posix()}" "{sha256(f)}"')
    print("REV " + rev(lane)[0])


def build_all(k46, k44, lane, root, empty, groups, rng, ctl):
    """Delta (c): one shuffled build of every module, fence-independent — the mutant battery re-uses it."""
    built: dict[str, list] = {g: [] for g in groups}
    build_errors = {g: 0 for g in groups}
    order = [(g, f) for g in groups for f in groups[g]]
    rng.shuffle(order)
    for g, f in order:
        try:
            built[g].append((f, k46.build_module(k44, lane, root, empty, f, rng, ctl)))
        except (RuntimeError, ValueError, KeyError, TypeError, json.JSONDecodeError,
                subprocess.TimeoutExpired) as e:
            build_errors[g] += 1
            print(f"BUILD-ERROR {g} {f.name} {str(e)[:160]}")
    return built, build_errors


def measure(k46, k44, lane, root, ctl, empty, built, build_errors, cp_bad, fence_path, jobs, rng, verbose,
            novel_mods=frozenset()):
    """Delta (d): run every built fixture through one fence copy and roll the three legs up. With
    `verbose=False` (mutant passes) only the leg tallies and the breaching rows are printed."""
    runs = [(g, f, fx) for g in built for f, fxs in built[g] for fx in fxs]
    rng.shuffle(runs)                                      # (c): run order carries no signal
    with concurrent.futures.ThreadPoolExecutor(max(1, jobs)) as ex:
        res = list(ex.map(lambda t: k46.run_fence(k44, lane, root, ctl, empty, fence_path, t[1][2], t[0]),
                          enumerate(runs)))
    per: dict[tuple[str, pathlib.Path], list] = {}
    for (g, f, fx), (verdict, why, hits, calls) in zip(runs, res):
        kind = kind_of(verdict, len(hits))
        per.setdefault((g, f), []).append({"fx": fx, "verdict": verdict, "why": why, "hits": hits,
                                           "calls": calls, "kind": kind})
        head_hit = f"{hits[0][0]}:{hits[0][1]}" if hits else ""
        if verbose or kind in ("leak", "read", "hung", "error"):
            print(f"FENCE-RUN {g} {fx['module']} {fx['fid']} {verdict} {kind} touches={len(hits)}"
                  f" calls={calls}" + (f" first={head_hit}" if head_hit else "")
                  + (f" -- {why}" if why else ""))

    def leg(g, total):
        tally = {k: 0 for k in ("clean", "leak", "read", "hung", "build_errors", "benign", "error")}
        for f, _fxs in built[g]:
            rows = per.get((g, f), [])
            bucket = module_rollup(rows)
            tally[bucket] += 1
            if verbose:
                print(f"{g.upper()} {f.name} {bucket.upper()} fixtures={len(rows)}"
                      f" admitted={sum(r['verdict'] == 'ADMIT' for r in rows)}"
                      f" hung={sum(r['verdict'] == 'HUNG' for r in rows)}"
                      f" touches={sum(len(r['hits']) for r in rows)}")
        tally["build_errors"] += build_errors[g] + (len(cp_bad) if g == "refusal" else 0)
        return tally, total

    rt, rtotal = leg("refusal", len(built["refusal"]) + build_errors["refusal"])
    st, stotal = leg("sealed", len(built["sealed"]) + build_errors["sealed"])
    hrows = [r for (g, _f), rows in per.items() if g == "honest" for r in rows]
    novel_fx = sum(len(per.get(("honest", f), [])) for f, _fx in built["honest"] if f in novel_mods)
    benign = {g: 0 for g in built}
    for (g, _f), rows in per.items():
        benign[g] += sum(r["kind"] == "benign" for r in rows)
    return {"rt": rt, "rtotal": rtotal, "st": st, "stotal": stotal, "hrows": hrows,
            "novel_fx": novel_fx,
            "h_adm": sum(r["kind"] == "benign" for r in hrows),
            "h_ref": sum(r["kind"] in ("clean", "read") for r in hrows),
            "h_read": sum(bool(r["hits"]) for r in hrows),
            "h_hung": sum(r["kind"] == "hung" for r in hrows),
            "hbuild": build_errors["honest"],
            "benign": benign,
            "benign_fx": sum(benign.values()),
            "contradicted": rt["leak"] + rt["read"] + rt["hung"] + st["leak"] + st["read"] + st["hung"],
            "errors": rt["error"] + st["error"] + sum(r["kind"] == "error" for r in hrows)}


def regressions(base, cur):
    """Delta (f) catch rule. The clean signature is `every hostile module refused untouched, every honest
    fixture admitted untouched, no harness error`; a mutant is caught iff its pass prints something strictly
    worse than the landed fence's own pass on the same built fixtures (a new leak/read/hang/benign admission,
    a hostile module no longer refused, an honest refusal, or a harness error). Comparing against the landed
    fence's measured pass — not an idealised all-clean line — keeps the battery honest when the landed fence is
    already failing, and a mutant that only changes bytes no leg observes survives, as the floor intends."""
    b = []
    for leg_name, key in (("refusals", "rt"), ("sealed", "st")):
        if cur[key]["clean"] < base[key]["clean"]:
            b.append(f"{leg_name}-clean={cur[key]['clean']}<{base[key]['clean']}")
        for k in ("leak", "read", "hung", "benign", "error", "build_errors"):
            if cur[key][k] > base[key][k]:
                b.append(f"{leg_name}-{k}={cur[key][k]}>{base[key][k]}")
    if cur["h_adm"] < base["h_adm"]:
        b.append(f"honest-admitted={cur['h_adm']}<{base['h_adm']}")
    if cur["h_ref"] > base["h_ref"]:
        b.append(f"honest-refused={cur['h_ref']}>{base['h_ref']}")
    if cur["h_read"] > base["h_read"]:
        b.append(f"honest-read={cur['h_read']}>{base['h_read']}")
    if cur["h_hung"] > base["h_hung"]:
        b.append(f"honest-hung={cur['h_hung']}>{base['h_hung']}")
    if cur["hbuild"] > base["hbuild"]:
        b.append(f"honest-build-errors={cur['hbuild']}>{base['hbuild']}")
    return b


def run_mutants(k46, k44, lane, root, ctl, empty, built, build_errors, cp_bad, entries, base, novel_mods,
                jobs, rng, mut_issues):
    """Delta (f): one fence pass per mutant over the same built fixtures; caught iff the clean signature breaks."""
    caught, broken = 0, 0
    for e in entries:
        payload, why = mutant_bytes(lane, e)
        if payload is None:
            broken += 1
            print(f"MUTANT {e['id']} broken {why} desc={e['description'][:100]}")
            mut_issues.append(f"{e['id']}:{why}")
            continue
        # The mutant fence must sit in a `ctl` directory of its own pass: the round-46 analyser excludes the
        # ctl directory from outside-`d` hits, so loading the fence under test is never itself a touch (the
        # clean pass relies on the same rule). Sharing a ctl would make every mutant look like a leak.
        vctl = root / "variants" / re.sub(r"[^A-Za-z0-9_.-]", "_", e["id"])[:40]
        vctl.mkdir(parents=True, exist_ok=True)
        (vctl / "harness.py").write_text(k46.HARNESS)
        fpath = vctl / f"fence-{secrets.token_hex(4)}.py"
        fpath.write_bytes(payload)
        cur = measure(k46, k44, lane, root, vctl, empty, built, build_errors, cp_bad, fpath, jobs, rng,
                      verbose=False, novel_mods=novel_mods)
        breaks = regressions(base, cur)
        if breaks:
            caught += 1
            print(f"MUTANT {e['id']} caught breaks={','.join(breaks[:5])} desc={e['description'][:100]}")
        else:
            print(f"MUTANT {e['id']} survived desc={e['description'][:100]}")
    return caught, broken


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--refusals", default=None, help="testing only: refusal module dir")
    ap.add_argument("--sealed", default=None, help="testing only: sealed module dir")
    ap.add_argument("--honest", default=None, help="testing only: extra honest module dir")
    ap.add_argument("--fence", default=None, help="testing only: fence file under test")
    ap.add_argument("--mutants", default=None, help="testing only: mutant declarations file")
    ap.add_argument("--seed", default=None, help="testing only: fixed token seed")
    ap.add_argument("--literals", action="store_true", help="print the stage-2 literals and pins; run nothing")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    rng = secrets.SystemRandom() if a.seed is None else random.Random(int(a.seed, 16))
    default_mode = (a.refusals is None and a.sealed is None and a.honest is None and a.fence is None
                    and a.mutants is None and a.seed is None and not a.literals)
    refdir = pathlib.Path(a.refusals).resolve() if a.refusals else lane / REFUSAL_REL
    sealdir = pathlib.Path(a.sealed).resolve() if a.sealed else lane / SEALED_REL
    hon_dir = pathlib.Path(a.honest).resolve() if a.honest else lane / HONEST_EXTRA_REL
    seal_extra = lane / SEALED_EXTRA_REL
    fence_src = pathlib.Path(a.fence).resolve() if a.fence else lane / FENCE_REL
    mut_path = pathlib.Path(a.mutants).resolve() if a.mutants else lane / MUTANTS_REL
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
    mut_entries, mut_issues = load_mutants(mut_path)
    if a.literals:
        literal_report(lane, refdir, sealdir, hon_dir, seal_extra, mut_entries, mut_issues)
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
    root = pathlib.Path(tempfile.mkdtemp(prefix="k49-c1-", dir=a.work)).resolve()
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
            fence_copy.write_bytes(b"def breach(d, argv, tool):\n    raise RuntimeError('fence absent')\n")
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
        print(f"LITERALS refusals={REFUSAL_FLOOR} sealed={SEALED_TOTAL} honest={HONEST_TOTAL}"
              f" mutants={len(mut_entries)}")
        print(f"LAYOUT refusals={refdir} sealed={sealdir} honest_extra={hon_dir} sealed_extra={seal_extra}"
              f" mutants={mut_path} novel={len(honest_novel)} pad={k46.PAD} jobs={a.jobs}")
        if default_mode:
            cp_bad = k46.copy_rows(refdir, lane) if refdir.is_dir() else []
        else:
            cp_bad = []
            print("COPY-CHECK skipped (refusals dir overridden for testing)")
        for g in ("refusal", "sealed", "honest"):
            print(f"MODULES {g} total={len(groups[g])}"
                  + ("" if groups[g] else " (directory absent or empty)"))
        built, build_errors = build_all(k46, k44, lane, root, empty, groups, rng, ctl)
        novel_mods = frozenset(honest_novel)
        r = measure(k46, k44, lane, root, ctl, empty, built, build_errors, cp_bad, fence_copy, a.jobs, rng,
                    verbose=True, novel_mods=novel_mods)
        rt, rtotal, st, stotal, hrows = r["rt"], r["rtotal"], r["st"], r["stotal"], r["hrows"]
        print(f"REFUSALS total={rtotal} clean={rt['clean']} leaked={rt['leak']} read={rt['read']}"
              f" hung={rt['hung']} build_errors={rt['build_errors']}")
        print(f"SEALED total={stotal} clean={st['clean']} leaked={st['leak']} read={st['read']}"
              f" hung={st['hung']} build_errors={st['build_errors']}")
        print(f"HONEST fixtures={len(hrows)} admitted={r['h_adm']} refused={r['h_ref']} read={r['h_read']}"
              f" hung={r['h_hung']} build_errors={r['hbuild']}")
        print(f"HONEST-POP battery={len(hrows) - r['novel_fx']} novel={r['novel_fx']}"
              f" expected_novel={HONEST_NOVEL_EXPECTED} novel_modules={len(honest_novel)}")
        print(f"BENIGN total={r['benign_fx']}")
        print(f"BENIGN-MODULES refusals={r['benign']['refusal']} sealed={r['benign']['sealed']}"
              f" honest={r['benign']['honest']}")
        if r["errors"]:
            print(f"ERRORS total={r['errors']}")
        m_total = len(mut_entries)
        caught, broken = run_mutants(k46, k44, lane, root, ctl, empty, built, build_errors, cp_bad,
                                     mut_entries, r, novel_mods, a.jobs, rng, mut_issues)
        verdict = "met" if m_total and caught * 2 >= m_total else "unmet"
        print(f"MUTANTS total={m_total} caught={caught} floor={m_total}/2 verdict={verdict}")
        for i in mut_issues:
            print(f"MUTANT-ISSUE {i}")
        print(f"CALIBRATION advertised={rtotal + stotal} contradicted={r['contradicted']}")
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
        if stotal != SEALED_TOTAL:
            fails.append(f"sealed-total={stotal}!={SEALED_TOTAL}")
        if st["clean"] != stotal or st["leak"] or st["read"] or st["hung"] or st["build_errors"] \
                or st["benign"] or st["error"]:
            fails.append("sealed-not-clean")
        if len(hrows) != HONEST_TOTAL:
            fails.append(f"honest-fixtures={len(hrows)}!={HONEST_TOTAL}")
        if r["h_adm"] != len(hrows) or r["h_ref"] or r["h_read"] or r["h_hung"] or r["hbuild"]:
            fails.append("honest-not-admitted")
        if m_total < MUTANT_MIN:
            fails.append(f"mutants-total={m_total}<{MUTANT_MIN}")
        if MUTANT_FLOOR and m_total != MUTANT_FLOOR:
            fails.append(f"mutants-total={m_total}!={MUTANT_FLOOR}")
        if caught * 2 < m_total:
            fails.append(f"mutants-caught={caught}<{m_total}/2")
        if broken:
            fails.append(f"mutants-broken={broken}")
        if mut_issues:
            fails.append(f"mutants-declared={len(mut_issues)}")
        if r["errors"]:
            fails.append(f"errors={r['errors']}")
        if r["contradicted"]:
            fails.append(f"contradicted={r['contradicted']}")
        good = not fails
        print("REASON " + (",".join(fails) if fails else "-"))
        print(f"PREDICATE R49-C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(empty, ignore_errors=True)
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:          # a receipt pipeline (`| head`) closing early is not a counter verdict
        os._exit(1)

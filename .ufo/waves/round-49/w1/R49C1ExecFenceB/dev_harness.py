#!/usr/bin/env python3
"""Dev harness for the round-49 C1 fence repair (seat R49C1ExecFenceB, variant B).

Reuses the round-46 counter's bwrap sandbox, round-44 builder, strace analyser and verdict table (imported
unchanged from the lane at the frozen base) and extends its legs for round 49: the 16 novel honest fixtures of
round 48 (`.ufo/waves/round-48/w1/R48C1ExecHonest/modules/{r46novel,novel48}`) join the 104 battery fixtures, so
the HONEST leg measures the frozen 120-fixture population, and every leg prints its own receipt. A MUTANTS leg
applies each mutant fence named in `--mutant-index` and reports whether the mutant is caught on its named
targets. The harness never writes inside the lane.

Usage:
  python3 dev_harness.py --lane DIR --fence FILE [--groups refusals,sealed,honest] [--jobs N]
                         [--mutant-index FILE] [--only REGEX] [--out FILE] [--rev HEX]
Exit 0 all measured legs clean, 1 a leg is not clean, 2 setup error.
"""
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

K46_REL = "plans/round46_c1_verify.py"
K44_REL = "plans/round44_c1_verify.py"
REFUSAL_REL = "plans/refusals46"
SEALED_REL = "plans/sealed46"
BATTERY_DIRS = ("plans/battery42", "plans/battery43", "plans/battery44")
HONEST_DIRS = (".ufo/waves/round-48/w1/R48C1ExecHonest/modules/r46novel",
               ".ufo/waves/round-48/w1/R48C1ExecHonest/modules/novel48")
HONEST_TOTAL = 120
MUTANT_FLOOR_NUM = 1          # caught must be >= floor/2 (frozen predicate shape); floor set by --mutant-floor
LOG = []


def say(msg):
    LOG.append(str(msg))
    print(msg, flush=True)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def tree_bytes(lane):
    n = 0
    for p in lane.rglob("*"):
        try:
            if p.is_file() and p.suffix not in (".pyc",):
                n += p.stat().st_size
        except OSError:
            pass
    return n


def pick_modules(lane, group, only):
    if group == "refusals":
        mods = sorted((lane / REFUSAL_REL).glob("*.py"))
    elif group == "sealed":
        mods = sorted((lane / SEALED_REL).glob("*.py"))
    else:
        mods = [f for rel in BATTERY_DIRS for f in sorted((lane / rel).glob("*.py"))]
        mods += [f for rel in HONEST_DIRS for f in sorted((lane / rel).glob("*.py"))]
    if only:
        import re
        rx = re.compile(only)
        mods = [f for f in mods if rx.search(f.as_posix())]
    return mods


def run_pass(k46, k44, lane, fence, groups, jobs, only, seed, tag):
    rng = random.Random(seed)
    root = pathlib.Path(tempfile.mkdtemp(prefix=f"devk49-{tag}-", dir=os.environ.get("TMPDIR")))
    empty = pathlib.Path(tempfile.mkdtemp(prefix=root.name + "-empty-", dir=root.parent))
    ctl = root / "ctl"
    ctl.mkdir()
    (ctl / "harness.py").write_text(k46.HARNESS)
    fence_copy = ctl / "fence.py"
    fence_copy.write_bytes(pathlib.Path(fence).read_bytes())
    pins = {}
    for rel in [K46_REL, K44_REL, str(fence)]:
        path = pathlib.Path(rel) if os.path.isabs(rel) else lane / rel
        pins[rel] = (path, sha256(path))
    mods = {g: pick_modules(lane, g, only) for g in groups}
    built, berr = {g: [] for g in groups}, {g: 0 for g in groups}
    order = [(g, f) for g in groups for f in mods[g]]
    rng.shuffle(order)
    try:
        for g, f in order:
            try:
                built[g].append((f, k46.build_module(k44, lane, root, empty, f, rng, ctl)))
            except (RuntimeError, ValueError, KeyError, TypeError, json.JSONDecodeError,
                    subprocess.TimeoutExpired) as e:
                berr[g] += 1
                say(f"BUILD-ERROR {g} {f.parent.name}/{f.name} {str(e)[:160]}")
        jobs_list = [(g, f, fx) for g in built for f, fxs in built[g] for fx in fxs]
        rng.shuffle(jobs_list)
        with concurrent.futures.ThreadPoolExecutor(max(1, jobs)) as ex:
            res = list(ex.map(lambda t: k46.run_fence(k44, lane, root, ctl, empty, fence_copy, t[1][2], t[0]),
                              enumerate(jobs_list)))
        per = {}
        for (g, f, fx), (v, why, hits, calls) in zip(jobs_list, res):
            per.setdefault((g, f), []).append((fx, v, why, hits, calls))
            head = f"{hits[0][0]}:{hits[0][1]}" if hits else ""
            say(f"FENCE-RUN {g} {fx['module']} {fx['fid']} {v} touches={len(hits)} calls={calls}"
                + (f" first={head}" if head else "") + (f" -- {why}" if why else ""))
        summary = {}
        for g in groups:
            clean = leaked = read = hung = benign = 0
            for f, fxs in built[g]:
                rows = per.get((g, f), [])
                n_admit = sum(v in ("ADMIT", "ERROR") for _fx, v, _w, _o, _c in rows)
                n_hung = sum(v == "HUNG" for _fx, v, _w, _o, _c in rows)
                n_hit = sum(len(o) for _fx, _v, _w, o, _c in rows)
                admit_all = bool(rows) and n_admit == len(rows)
                if not rows or (admit_all and n_hit):
                    verdict = "LEAKED"
                    leaked += 1
                elif admit_all and not n_hit:
                    verdict = "BENIGN-ADMIT"
                    benign += 1
                elif n_hung:
                    verdict = "HUNG"
                    hung += 1
                elif n_hit:
                    verdict = "READ"
                    read += 1
                else:
                    verdict = "clean"
                    clean += 1
                say(f"{g.upper()} {f.name} {verdict} fixtures={len(rows)} admitted={n_admit} hung={n_hung}"
                    f" touches={n_hit}")
            rows = [row for (gg, _f), rs in per.items() if gg == g for row in rs]
            s = {"total": len(mods[g]), "clean": clean, "leaked": leaked, "read": read, "hung": hung,
                 "benign": benign, "build_errors": berr[g], "fixtures": len(rows),
                 "admitted": sum(v == "ADMIT" for _fx, v, _w, _o, _c in rows),
                 "admitted_clean": sum(v == "ADMIT" and not o for _fx, v, _w, o, _c in rows),
                 "refused": sum(v in ("BREACH", "ERROR") for _fx, v, _w, _o, _c in rows),
                 "read_fixtures": sum(bool(o) for _fx, _v, _w, o, _c in rows),
                 "hung_fixtures": sum(v == "HUNG" for _fx, v, _w, _o, _c in rows)}
            summary[g] = s
            if g in ("refusals", "sealed"):
                say(f"{g.upper()} total={s['total']} clean={clean} leaked={leaked} read={read} hung={hung}"
                    f" benign_admit={benign} build_errors={berr[g]}")
            else:
                say(f"HONEST fixtures={s['fixtures']} admitted={s['admitted_clean']} refused={s['refused']}"
                    f" read={s['read_fixtures']} hung={s['hung_fixtures']} build_errors={berr[g]}"
                    f" modules={s['total']}")
        mism = [k for k, (path, dig) in pins.items() if sha256(path) != dig]
        say(f"PINS total={len(pins)} mismatched={len(mism)}" + (f" first={mism[0]}" if mism else ""))
        return summary, mism
    finally:
        shutil.rmtree(root, ignore_errors=True)
        shutil.rmtree(empty, ignore_errors=True)


def mutant_pass(k46, k44, lane, index, jobs, seed, out):
    rows = []
    for entry in json.loads(pathlib.Path(index).read_text()):
        name = entry["file"]
        targets = entry.get("targets", [])
        fence = pathlib.Path(entry["path"] if "path" in entry else name)
        # build a REGEX that selects the named modules across every group
        only = "|".join(targets) if targets else None
        seed2 = hashlib.sha256((name + str(seed)).encode()).hexdigest()[:16]
        say(f"MUTANT-RUN {name} targets={targets}")
        summary, mism = run_pass(k46, k44, lane, fence, ("refusals", "sealed", "honest"), jobs, only,
                                 int(seed2, 16), "mut")
        flipped = []
        for g, s in summary.items():
            if g in ("refusals", "sealed"):
                if s["leaked"] or s["clean"] < s["total"]:
                    flipped.append(f"{g}:clean={s['clean']}/{s['total']} leaked={s['leaked']}")
            else:
                if s["refused"] or s["read_fixtures"] or s["hung_fixtures"] or \
                        s["admitted_clean"] < s["fixtures"] or mism:
                    flipped.append(f"honest:admitted={s['admitted_clean']}/{s['fixtures']}"
                                   f" refused={s['refused']}")
        caught = bool(flipped)
        rows.append({"mutant": name, "caught": caught, "flips": flipped, "note": entry.get("note", "")})
        say(f"MUTANT {name} caught={'yes' if caught else 'no'}" + (f" {' '.join(flipped)}" if flipped else ""))
    caught = sum(1 for r in rows if r["caught"])
    say(f"MUTANTS total={len(rows)} caught={caught} floor={len(rows) // 2}")
    if out:
        pathlib.Path(out).write_text(json.dumps(rows, indent=1) + "\n")
    return caught, len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fence", required=True)
    ap.add_argument("--groups", default="refusals,sealed,honest")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", default=None)
    ap.add_argument("--seed", default="49c1fenceb")
    ap.add_argument("--out", default=None)
    ap.add_argument("--mutant-index", default=None)
    ap.add_argument("--mutant-out", default=None)
    ap.add_argument("--label", default="")
    ap.add_argument("--rev", default="")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    groups = tuple(g.strip() for g in a.groups.split(",") if g.strip())
    for rel in (K46_REL, K44_REL):
        if not (lane / rel).is_file():
            say(f"SETUP {rel} absent from {lane}")
            return 2
    k46 = load(lane / K46_REL, "k46_counter")
    k44 = load(lane / K44_REL, "k44_counter")
    head = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    say(f"REV {a.rev or head}")
    say(f"TREE {lane}")
    say(f"LABEL {a.label or pathlib.Path(a.fence).name}")
    say(f"FENCE source={a.fence} sha256={sha256(a.fence)}")
    seed = int(hashlib.sha256(a.seed.encode()).hexdigest()[:16], 16)
    summary, mism = run_pass(k46, k44, lane, a.fence, groups, a.jobs, a.only, seed, "main")
    clean = not mism
    for g, s in summary.items():
        if g in ("refusals", "sealed"):
            clean = clean and s["leaked"] == 0 and s["read"] == 0 and s["hung"] == 0 and \
                s["build_errors"] == 0 and s["clean"] == s["total"]
        else:
            clean = clean and s["admitted_clean"] == s["fixtures"] and s["refused"] == 0 and \
                s["read_fixtures"] == 0 and s["hung_fixtures"] == 0 and s["build_errors"] == 0 and \
                s["fixtures"] == HONEST_TOTAL
    if "refusals" in summary and "sealed" in summary:
        contradicted = sum(s["leaked"] + s["read"] + s["hung"] + s["build_errors"]
                           for g, s in summary.items() if g in ("refusals", "sealed"))
        advertised = sum(s["total"] for g, s in summary.items() if g in ("refusals", "sealed"))
        say(f"CALIBRATION advertised={advertised} contradicted={contradicted}")
        clean = clean and contradicted == 0
    if a.mutant_index:
        caught, total = mutant_pass(k46, k44, lane, a.mutant_index, a.jobs, seed, a.mutant_out)
        say(f"MUTANTS total={total} caught={caught} floor={total // 2} verdict="
            f"{'met' if caught >= total // 2 else 'unmet'}")
        clean = clean and caught >= total // 2
    say(f"PREDICATE R49-C1 {'pass' if clean else 'fail'}")
    if a.out:
        pathlib.Path(a.out).write_text("\n".join(LOG) + "\n")
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())

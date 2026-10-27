#!/usr/bin/env python3
"""Round-48 C1 — build the frozen HONEST fixture population and its identity receipts.

Seat `R48C1ExecHonest` (executor), wave `round-48/w1`. Not a counter and not a probe: this tool builds
fixtures and digests them. It executes no fence, no gate and no gated tool, so it produces no scored
measurement of claimed work. The stage-2 counter pins the population file this tool prints (`population.txt`
+ `population.sha256`); scoring happens later, against a committed stage-2 freeze.

Population (round-48 claims §C1 (a), `plans/round-48-claims.md`):
  battery42/43/44  the 104 fixtures of the standing batteries, built through the round-44 builder contract
                   (`Ctx`/`build(ctx, d)`), with every module digest checked against the round-46 counter's
                   `PINS` table so the 104 are provably the same 104 the round-46 counter measured.
  r46novel         the 9 round-46 novel honest classes, rebuilt from their wave-2 report descriptions
                   (`.ufo/waves/round-46/w2/R46W2C1HoHonest.md`).
  novel48          NEW honest classes authored by this seat: ordinary `git init` repository states the
                   round-46 set does not cover.

Authoring guard (`--assert-base`, default on): the builder refuses to run unless `plans/fixture_fence.py` is
the round-48 stage-1 BASE fence (`05d5fe03…`) and `plans/round44_c1_verify.py` is the round-46-pinned builder
(`6cf05323…`). The novel classes were authored against the base fence *description* only; a repaired fence in
the tree would make the authoring provenance unprovable, so the builder refuses instead of guessing.

Identity: per fixture, a canonical digest of the built tree — every directory and regular file by relative
path, permission bits and content sha256, sorted — with the volatile set `MASK` excluded. `.git/index` is
masked because it caches inode/mtime stat data that no two builds reproduce; masking it is the round-44
counter's own choice (`fingerprint()` skips `.git/index`). Every fixture is built `--repeats` times (default
2) into separate parents, and the fixture is `deterministic` only when the normalized identities are equal —
so a receipt's digest is a reproducible statement, not a one-shot sample. `argv` is normalized to `{WORK}`,
so no absolute scratch path enters the receipt.

Usage:
  python3 build_honest_population.py --lane DIR --modules DIR --out DIR [--work DIR] [--jobs N] [--repeats N]

Exit: 0 population frozen and every assertion held · 2 setup/guard error · 1 a fixture or an assertion failed.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import pathlib
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time

BASE_REV = "a543d92083557dd9b33ee674e9b99b03411f80af"
BASE_FENCE_SHA = "05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e"
K44_REL = "plans/round44_c1_verify.py"
K44_SHA = "6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad"
K46_REL = "plans/round46_c1_verify.py"
FENCE_REL = "plans/fixture_fence.py"
BATTERY_RELS = ("plans/battery42", "plans/battery43", "plans/battery44")
BATTERY_TOTAL = 104          # frozen pre-existing count (round-46 counter HONEST_TOTAL)
R46NOVEL_TOTAL = 9           # frozen in the claims: the nine round-46 novel honest classes
NOVEL48_FLOOR = 6            # frozen in the claims: "6+ NEW novel honest classes"
MASK = (".git/index",)       # git's stat cache: the one non-reproducible byte set (measured, see receipt)


def masked(rel):
    """`.git/index` at any depth: a battery fixture keeps its repository below the fixture dir."""
    return rel == ".git/index" or rel.endswith("/.git/index")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while chunk := fh.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def load(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------- identity ----------


def tree_identity(root):
    """Canonical digest of one built fixture: sorted (kind, relpath, mode, content) lines, MASK excluded."""
    lines, n_files, n_dirs = [], 0, 0
    for top, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        t = pathlib.Path(top)
        for name in dirs:
            rel = (t / name).relative_to(root).as_posix()
            if masked(rel):
                continue
            n_dirs += 1
            lines.append(f"D {rel} {stat.S_IMODE(os.lstat(t / name).st_mode):04o}")
        for name in sorted(files):
            p = t / name
            rel = p.relative_to(root).as_posix()
            if masked(rel):
                continue
            st = os.lstat(p)
            if stat.S_ISLNK(st.st_mode):
                body = "symlink:" + os.readlink(p)
            elif stat.S_ISREG(st.st_mode):
                body = "sha256:" + sha256_file(p)
            else:
                body = f"special:{st.st_mode:o}"
            n_files += 1
            lines.append(f"F {rel} {stat.S_IMODE(st.st_mode):04o} {body}")
    lines.sort()
    h = hashlib.sha256()
    for line in lines:
        h.update(line.encode() + b"\n")
    return h.hexdigest(), n_files, n_dirs


def structural_audit(root):
    """Prove the honesty claim structurally: no symlink, no special file, no hard link, gitdir inside `root`.

    An honest fixture cannot read outside `d` by construction when its tree holds no indirection at all, so this
    is measured per fixture rather than asserted in prose. Measured, not fenced: no fence is run here.
    """
    symlinks, specials, hardlinks = [], [], []
    for top, dirs, files in os.walk(root):
        t = pathlib.Path(top)
        for name in list(dirs) + list(files):
            p = t / name
            st = os.lstat(p)
            rel = p.relative_to(root).as_posix()
            if stat.S_ISLNK(st.st_mode):
                symlinks.append(rel)
                dirs[:] = [d for d in dirs if d != name]
            elif not (stat.S_ISDIR(st.st_mode) or stat.S_ISREG(st.st_mode)):
                specials.append(rel)
            elif stat.S_ISREG(st.st_mode) and st.st_nlink > 1:
                hardlinks.append(rel)
    return {"symlinks": sorted(symlinks), "specials": sorted(specials), "hardlinks": sorted(hardlinks)}


def gitdir_inside(ctx, repos, root):
    out = []
    for repo in repos:
        r = ctx.sh("git", "-C", str(repo), "rev-parse", "--absolute-git-dir", check=False)
        gd = pathlib.Path(r.stdout.strip()).resolve() if r.returncode == 0 else None
        out.append(bool(gd) and gd.is_relative_to(root))
    return out


def git_state(ctx, repos):
    """Read-only repository facts per discovered repo: toplevel, HEAD, every ref, fsck."""
    out = []
    for repo in repos:
        top = ctx.sh("git", "-C", str(repo), "rev-parse", "--show-toplevel", check=False)
        head = ctx.sh("git", "-C", str(repo), "rev-parse", "--verify", "HEAD", check=False)
        refs = ctx.sh("git", "-C", str(repo), "for-each-ref", "--format=%(refname) %(objectname)", check=False)
        fsck = ctx.sh("git", "-C", str(repo), "fsck", "--strict", "--no-progress", check=False)
        out.append({
            "dir": repo.name,
            "toplevel_ok": top.returncode == 0 and pathlib.Path(top.stdout.strip()).resolve() == repo,
            "head": head.stdout.strip() if head.returncode == 0 else None,
            "refs": sorted(l for l in refs.stdout.splitlines() if l.strip()) if refs.returncode == 0 else [],
            "fsck_rc": fsck.returncode,
        })
    return out


def normalize_argv(argv, d):
    out = []
    prefix = str(d)
    for tok in argv:
        if tok == prefix:
            out.append("{WORK}")
        elif tok.startswith(prefix + "/"):
            out.append("{WORK}/" + tok[len(prefix) + 1:])
        else:
            out.append(tok)
    return out


def discover_repos(root):
    """Every work-tree directory holding a real `.git` directory (the repo, not its gitdir)."""
    return sorted(pathlib.Path(top) for top, dirs, _f in os.walk(root) if ".git" in dirs)


def build_once(k44, module_path, gen):
    """Build every fixture of one module into gen/fNNN; return [(fid, tool, expect, defects, argv, dir, build)]."""
    mod = load(module_path, f"k48_honest_{module_path.stem}_{hash(str(gen)) & 0xffff:x}")
    ctx = k44.Ctx(gen)
    out = []
    fixtures = getattr(mod, "FIXTURES", None)
    if not isinstance(fixtures, list) or not fixtures:
        raise ValueError(f"{module_path.name}: no FIXTURES list")
    for k, fx in enumerate(fixtures):
        d = gen / f"f{k:03d}"
        d.mkdir(parents=True)
        argv = fx["build"](ctx, d)
        if not isinstance(argv, list) or not all(type(t) is str for t in argv):
            raise TypeError(f"{module_path.name}/{fx.get('fid')!r}: build() must return a list of str")
        if not d.is_dir():
            raise RuntimeError(f"{module_path.name}/{fx.get('fid')!r}: fixture dir vanished")
        if not (d / ".git").exists() and not any((p / ".git").is_dir() for p in d.iterdir() if p.is_dir()):
            raise RuntimeError(f"{module_path.name}/{fx.get('fid')!r}: no repository under the fixture dir")
        out.append((fx.get("fid"), fx.get("tool"), fx.get("expect"), fx.get("defects"), argv, d,
                    getattr(fx.get("build"), "__name__", "?")))
    return out


def identify_one(k44, module_path, fx, repeats, work, rng_tag):
    """Build one fixture `repeats` times, compare identities, return its receipt."""
    fid, tool, expect, defects, _argv0, _d0, build = fx
    ids, states = [], []
    for r in range(repeats):
        gen = work / f"r{r}" / rng_tag
        shutil.rmtree(gen, ignore_errors=True)
        gen.mkdir(parents=True)
        built = build_once(k44, module_path, gen)
        hit = [b for b in built if b[0] == fid]
        if len(hit) != 1:
            raise RuntimeError(f"fixture {fid!r} not found exactly once in its module build")
        _f, tool, expect, defects, argv, d, build = hit[0]
        digest, n_files, n_dirs = tree_identity(d)
        repos = discover_repos(d)
        ctx = k44.Ctx(d)
        st = git_state(ctx, repos)
        audit = structural_audit(d)
        audit["gitdir_inside"] = gitdir_inside(ctx, repos, d)
        ids.append(digest)
        states.append({"files": n_files, "dirs": n_dirs, "repos": st, "audit": audit,
                       "argv": normalize_argv(argv, d)})
        shutil.rmtree(gen)
    deterministic = len(set(ids)) == 1
    return {
        "fid": fid, "tool": tool, "expect": expect, "defects": defects, "build": build,
        "argv": states[0]["argv"], "tree_sha256": ids[0],
        "files": states[0]["files"], "dirs": states[0]["dirs"],
        "repos": states[0]["repos"],
        "audit": states[0]["audit"],
        "repeats": repeats, "deterministic": deterministic,
        "all_ids_equal": len(set(ids)) == 1,
    }


# ---------- populations ----------


def population_modules(lane, modules_dir):
    pops = [("battery42", lane / "plans/battery42"), ("battery43", lane / "plans/battery43"),
            ("battery44", lane / "plans/battery44"),
            ("r46novel", modules_dir / "r46novel"), ("novel48", modules_dir / "novel48")]
    out = []
    for name, d in pops:
        files = sorted(pathlib.Path(d).glob("*.py"))
        if not files:
            raise SystemExit(f"SETUP population {name}: no modules under {d}")
        out.append((name, files))
    return out


def build_symbols(module_path):
    text = module_path.read_text()
    return re.findall(r"^def (\w+)\(ctx, d\):", text, re.M)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True, help="lane tree at the round-48 stage-1 freeze")
    ap.add_argument("--modules", required=True, help="dir holding r46novel/ and novel48/")
    ap.add_argument("--out", required=True, help="receipt output dir (wave artifact dir)")
    ap.add_argument("--work", default=None, help="scratch parent (must lie outside the lane)")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--repeats", type=int, default=2)
    ap.add_argument("--assert-base", dest="assert_base", action="store_true", default=True)
    ap.add_argument("--no-assert-base", dest="assert_base", action="store_false")
    a = ap.parse_args()

    lane = pathlib.Path(a.lane).resolve()
    out = pathlib.Path(a.out).resolve()
    if not (lane / K44_REL).is_file():
        print(f"SETUP {lane} is not a lane tree ({K44_REL} absent)", file=sys.stderr)
        return 2
    if a.work and pathlib.Path(a.work).resolve().is_relative_to(lane):
        print("SETUP --work must not lie inside the lane", file=sys.stderr)
        return 2

    rev = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True)
    rev = rev.stdout.strip()
    guard = []
    fence_sha = sha256_file(lane / FENCE_REL)
    k44_sha = sha256_file(lane / K44_REL)
    if a.assert_base:
        if rev != BASE_REV:
            print(f"SETUP lane HEAD {rev} is not the stage-1 freeze {BASE_REV}", file=sys.stderr)
            return 2
        if fence_sha != BASE_FENCE_SHA:
            print(f"SETUP {FENCE_REL} sha256 {fence_sha} is not the base fence {BASE_FENCE_SHA}: the novel "
                  "classes were authored against the base description, so a repaired fence is not a valid "
                  "authoring tree", file=sys.stderr)
            return 2
        if k44_sha != K44_SHA:
            print(f"SETUP {K44_REL} sha256 {k44_sha} is not the pinned builder {K44_SHA}", file=sys.stderr)
            return 2
        guard.append(f"GUARD base-fence-ok {FENCE_REL} sha256={fence_sha}")
        guard.append(f"GUARD builder-ok {K44_REL} sha256={k44_sha}")
        guard.append(f"GUARD lane-rev-ok {rev}")

    k44 = load(lane / K44_REL, "kengaku_r44_builder")
    k46 = load(lane / K46_REL, "kengaku_r46_pins")
    pin_rows, pin_bad = [], []
    for rel in BATTERY_RELS:
        for f in sorted((lane / rel).glob("*.py")):
            key = f.relative_to(lane).as_posix()
            want = k46.PINS.get(key)
            got = sha256_file(f)
            ok = got == want
            if not ok:
                pin_bad.append(key)
            pin_rows.append({"module": key, "sha256": got, "pinned": want, "ok": ok})

    pops = population_modules(lane, pathlib.Path(a.modules).resolve())
    work_parent = pathlib.Path(tempfile.mkdtemp(prefix="k48-honest-", dir=a.work)).resolve()
    if work_parent.is_relative_to(lane):
        print("SETUP scratch root lies inside the lane; pass --work", file=sys.stderr)
        return 2
    started = time.time()
    receipts, failures = [], []
    try:
        def run(pop, f):
            gen_tag = hashlib.sha256(f"{pop}/{f.name}".encode()).hexdigest()[:12]
            work = work_parent / "gen"
            work.mkdir(exist_ok=True)
            fixtures = build_once(k44, f, work / ("probe-" + gen_tag))  # contract/arity check, then discarded
            shutil.rmtree(work / ("probe-" + gen_tag), ignore_errors=True)
            rows = []
            for fx in fixtures:
                r = identify_one(k44, f, fx, a.repeats, work, gen_tag)
                r.update({"population": pop, "module": f.relative_to(lane).as_posix()
                          if f.is_relative_to(lane) else f.relative_to(pathlib.Path(a.modules).resolve()).as_posix(),
                          "module_sha256": sha256_file(f)})
                rows.append(r)
            return pop, f, rows

        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as ex:
            futs = [ex.submit(run, pop, f) for pop, files in pops for f in files]
            for fut in concurrent.futures.as_completed(futs):
                try:
                    pop, f, rows = fut.result()
                except Exception as e:                       # a build failure is a receipt, never silence
                    failures.append(f"{type(e).__name__}: {e}")
                    print(f"BUILD-FAIL {e}", file=sys.stderr)
                    continue
                receipts.extend(rows)
                print(f"MODULE {pop} {f.name} fixtures={len(rows)} "
                      f"deterministic={sum(r['deterministic'] for r in rows)}")
    finally:
        shutil.rmtree(work_parent, ignore_errors=True)

    receipts.sort(key=lambda r: (r["population"], r["module"], r["fid"]))
    out.mkdir(parents=True, exist_ok=True)
    recdir = out / "receipts"
    shutil.rmtree(recdir, ignore_errors=True)
    for r in receipts:
        p = recdir / r["population"] / f"{pathlib.Path(r['module']).stem}--{r['fid']}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n")
    (out / "identity.jsonl").write_text(
        "".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts))

    counts = {}
    for r in receipts:
        counts[r["population"]] = counts.get(r["population"], 0) + 1
    fids = [r["fid"] for r in receipts]
    dupes = sorted({f for f in fids if fids.count(f) > 1}) if len(set(fids)) != len(fids) else []

    pop_lines = ["# HONEST POPULATION round-48 C1 v1",
                 f"# lane={rev} builder_sha256={sha256_file(pathlib.Path(__file__).resolve())} "
                 f"base_fence_sha256={fence_sha} builder_tree=plans/round44_c1_verify.py@{k44_sha}",
                 "# columns: HONEST <tree_sha256> <population> <module>#<build> <fid> <tool>",
                 f"# mask={' '.join(MASK)} (volatile; git stat cache)"]
    for r in receipts:
        pop_lines.append(f"HONEST {r['tree_sha256']} {r['population']} {r['module']}#{r['build']} "
                         f"{r['fid']} {r['tool']}")
    population_text = "\n".join(pop_lines) + "\n"
    (out / "population.txt").write_text(population_text)
    pop_sha = hashlib.sha256(population_text.encode()).hexdigest()
    (out / "population.sha256").write_text(f"{pop_sha}  population.txt\n")
    mod_rows = []
    for _pop, files in pops:
        for f in files:
            rel = f.relative_to(lane).as_posix() if f.is_relative_to(lane) else \
                f.relative_to(pathlib.Path(a.modules).resolve()).as_posix()
            mod_rows.append(f"{sha256_file(f)}  {rel}")
    mod_text = "\n".join(sorted(mod_rows)) + "\n"
    (out / "modules.sha256").write_text(mod_text)
    mod_sha = hashlib.sha256(mod_text.encode()).hexdigest()

    checks = []
    if guard:
        pass
    for row in pin_rows:
        if not row["ok"]:
            checks.append(f"battery-module-pin-mismatch {row['module']}")
    if counts.get("battery42", 0) + counts.get("battery43", 0) + counts.get("battery44", 0) != BATTERY_TOTAL:
        checks.append("battery-total")
    if counts.get("r46novel", 0) != R46NOVEL_TOTAL:
        checks.append("r46novel-total")
    if counts.get("novel48", 0) < NOVEL48_FLOOR:
        checks.append("novel48-floor")
    if dupes:
        checks.append("fid-duplicates:" + ",".join(dupes))
    if failures:
        checks.append(f"build-failures={len(failures)}")
    bad_det = [r["fid"] for r in receipts if not r["deterministic"]]
    if bad_det:
        checks.append("nondeterministic:" + ",".join(bad_det))
    bad_top = [f"{r['fid']}" for r in receipts for s in r["repos"] if not s["toplevel_ok"]]
    if bad_top:
        checks.append("toplevel:" + ",".join(bad_top))
    bad_fsck = [r["fid"] for r in receipts for s in r["repos"] if s["fsck_rc"] != 0]
    if bad_fsck:
        checks.append("fsck:" + ",".join(bad_fsck))
    norepo = [r["fid"] for r in receipts if not r["repos"]]
    if norepo:
        checks.append("no-repository:" + ",".join(norepo))
    for key in ("symlinks", "specials", "hardlinks"):
        bad = [r["fid"] for r in receipts if r["audit"][key]]
        if bad:
            checks.append(f"{key}:" + ",".join(bad))
    outside = [r["fid"] for r in receipts if not all(r["audit"]["gitdir_inside"])]
    if outside:
        checks.append("gitdir-outside:" + ",".join(outside))

    receipt_line = ["REV " + rev,
                    f"POPULATION population.txt sha256={pop_sha} fixtures={len(receipts)}",
                    f"MODULE-MANIFEST modules.sha256 sha256={mod_sha} modules={len(mod_rows)}",
                    f"BUILDER build_honest_population.py sha256={sha256_file(pathlib.Path(__file__).resolve())}",
                    f"MODULES dir={pathlib.Path(a.modules).resolve()} repeats={a.repeats} jobs={a.jobs}",
                    "MASK " + " ".join(MASK),
                    f"COUNTS " + " ".join(f"{k}={counts.get(k, 0)}" for k in
                                          ("battery42", "battery43", "battery44", "r46novel", "novel48"))]
    receipt_line += guard
    receipt_line += [f"BATTERY-MODULE-PIN {r['module']} sha256={r['sha256']} ok={int(r['ok'])}"
                     for r in pin_rows]
    receipt_line += [f"IDENTITY {r['population']} {r['fid']} tree_sha256={r['tree_sha256']} "
                     f"files={r['files']} dirs={r['dirs']} deterministic={int(r['deterministic'])} "
                     f"head={r['repos'][0]['head'] if r['repos'] else '-'} "
                     f"fsck={','.join(str(s['fsck_rc']) for s in r['repos']) or '-'} "
                     f"symlinks={len(r['audit']['symlinks'])} specials={len(r['audit']['specials'])} "
                     f"hardlinks={len(r['audit']['hardlinks'])} "
                     f"gitdir_inside={int(all(r['audit']['gitdir_inside']))}"
                     for r in receipts]
    receipt_line += [f"HOST git={subprocess.run(['git', '--version'], capture_output=True, text=True).stdout.strip()} "
                     f"python={platform.python_version()} platform={platform.platform()}",
                     f"SCORED none (no fence, gate or counter executed; stage-2 freeze absent at {rev})",
                     f"DURATION seconds={time.time() - started:.1f}",
                     "CHECKS " + (" ".join(checks) if checks else "all-ok")]
    (out / "builder-receipt.txt").write_text("\n".join(receipt_line) + "\n")
    print("\n".join(receipt_line))
    print(f"PREDICATE POPULATION {'fail' if checks else 'ok'}")
    return 1 if checks else 0


if __name__ == "__main__":
    sys.exit(main())

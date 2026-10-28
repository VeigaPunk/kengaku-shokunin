#!/usr/bin/env python3
"""Round-50 seat R50C1ExecSealedAssemble: assemble the plans/sealed50 candidate.

Candidate sources: the blind critic modules authored in wave 1 (wave directories) and the hostile
variants (`plans/sealed50` at the lane tip, carried here as candidates). Gates, in order:

  FIXTURES   module imports; `FIXTURES` is a non-empty list of dicts carrying fid/tool/expect/defects/build
             (build callable); build(ctx, d) returns list[str]; the fixture dir survives; fids unique in module.
  DETERM.    every fixture is built twice at the SAME absolute root and once at a DIFFERENT absolute root,
             through the lane's own harness (`plans/honest50/build_honest_population.py`, which imports the
             round-44 `Ctx`). Canonical identity = the population builder's `tree_identity`.
  BASE       the BASE fence (freeze clone, sha256 05d5fe03…) must REFUSE (breach() truthy) every fixture.
             Verdict travels in a child process exit code (10 BREACH, 11 ADMIT, 12 ERROR), as the counter does.

De-duplication is by fixture identity: `fid` across modules (the counter's per-module attribution is keyed on
fids), plus byte-identical build identity (tree_sha256, tool, normalised argv). One survivor per identity; the
variant with the better contract/portability tuple wins, ties by source order (lane variant first).

Usage: assemble.py --lane CLONE --work DIR --candidates DIR --out DIR
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys

ABSLIT = re.compile(r"""["'](/[A-Za-z0-9_.][^"'\n]*)["']""")

HARNESS = r'''
import importlib.util, json, os, pathlib, sys
spec = importlib.util.spec_from_file_location("fence_under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
os.closerange(3, 1024)
try:
    r = m.breach(pathlib.Path(sys.argv[2]), json.loads(sys.argv[4]), sys.argv[3])
except Exception as e:
    sys.stderr.write(f"HARNESS-ERROR {type(e).__name__}: {e}\n")
    sys.exit(12)
sys.stderr.write(("BREACH " + " ".join(str(r).split()))[:300] + "\n" if r else "ADMIT\n")
sys.exit(10 if r else 11)
'''


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while chunk := fh.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def contract_problems(mod, path):
    problems = []
    fx = getattr(mod, "FIXTURES", None)
    if not isinstance(fx, list) or not fx:
        return ["FIXTURES is not a non-empty list"]
    fids = set()
    for k, row in enumerate(fx):
        if not isinstance(row, dict):
            problems.append(f"FIXTURES[{k}] is not a dict")
            continue
        for key in ("fid", "tool", "expect", "defects", "build"):
            if key not in row:
                problems.append(f"FIXTURES[{k}] missing {key}")
        if not isinstance(row.get("fid"), str) or not row.get("fid"):
            problems.append(f"FIXTURES[{k}] fid is not a non-empty str")
        if not isinstance(row.get("tool"), str) or not row.get("tool"):
            problems.append(f"FIXTURES[{k}] tool is not a non-empty str")
        if not isinstance(row.get("expect"), str) or not row.get("expect"):
            problems.append(f"FIXTURES[{k}] expect is not a non-empty str")
        if not isinstance(row.get("defects"), list):
            problems.append(f"FIXTURES[{k}] defects is not a list")
        if not callable(row.get("build")):
            problems.append(f"FIXTURES[{k}] build is not callable")
        fid = row.get("fid")
        if isinstance(fid, str):
            if fid in fids:
                problems.append(f"duplicate fid inside module: {fid}")
            fids.add(fid)
    return problems


def build_rep(hb, k44, mod, row, root, tag):
    """Build one fixture into root/tag/f000; return a receipt dict or raise."""
    gen = root / tag
    shutil.rmtree(gen, ignore_errors=True)
    gen.mkdir(parents=True)
    for _k in range(4):                       # opaque decoys, as the counter does (Q39)
        (gen / os.urandom(3).hex()).mkdir()
    d = gen / "f000"
    d.mkdir()
    ctx = hb.quiet_ctx(k44, gen)
    argv = row["build"](ctx, d)
    if not isinstance(argv, list) or not all(type(t) is str for t in argv):
        raise TypeError(f"{row.get('fid')!r}: build() must return a list of str")
    if not d.is_dir():
        raise RuntimeError(f"{row.get('fid')!r}: fixture dir vanished")
    return {"dir": d, "argv": hb.normalize_argv(argv, d), "argv_raw": argv}


def canonical(hb, d):
    return hb.retry_read(hb.tree_identity, d)


def safe_gitfile_index_paths(root):
    """Canonical extras, but a gitfile whose target carries a NUL is skipped (that pointer is not a path)."""
    out = set()
    root = pathlib.Path(root)
    for p in root.rglob(".git"):
        if not p.is_file():
            continue
        try:
            m = hb_matcher.match(p.read_text(errors="replace"))
        except (OSError, ValueError):
            continue
        if not m:
            continue
        try:
            target = (p.parent / m.group(1)).resolve()
        except (OSError, ValueError):
            continue
        if target.is_relative_to(root.resolve()):
            out.add((target / "index").relative_to(root.resolve()).as_posix())
    return out


def verdict(fence, fixture_dir, tool, argv, work, idx):
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": "/nonexistent",
           "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONHASHSEED": "0",
           "PYTHONDONTWRITEBYTECODE": "1"}
    log = work / "harness" / f"{idx:04d}.err"
    log.parent.mkdir(parents=True, exist_ok=True)
    try:
        p = subprocess.run([sys.executable, "-I", str(work / "harness.py"), str(fence),
                            str(fixture_dir), tool, json.dumps(argv)], cwd=str(fixture_dir),
                           env=env, capture_output=True, text=True, timeout=120)
        rc = p.returncode
        why = (p.stderr.strip().splitlines() or [""])[-1][:240]
    except subprocess.TimeoutExpired:
        rc, why = 12, "HUNG"
    return {"v": "BREACH" if rc == 10 else ("ADMIT" if rc == 11 else "ERROR"), "why": why}


hb_matcher = None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    cands = pathlib.Path(a.candidates).resolve()
    out = pathlib.Path(a.out).resolve()
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    (work / "harness.py").write_text(HARNESS)

    global hb_matcher
    hb = load(lane / "plans/honest50/build_honest_population.py", "as_hb")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "as_k44")
    hb_matcher = hb.GITFILE
    fence = lane / "plans/fixture_fence.py"

    modules = []
    for src in ("blind", "lane50"):
        base = cands / src
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.py")):
            modules.append({"path": p, "source": src, "origin": p.parent.name if src == "blind" else "lane50",
                            "name": p.name})

    results = []
    idx = 0
    for m in modules:
        rec = {"file": m["name"], "source": m["source"], "origin": m["origin"],
               "src_path": str(m["path"]), "sha256": sha256_file(m["path"]),
               "fixtures": [], "contract": None, "problems": []}
        try:
            mod = load(m["path"], f"cand_{idx}_{m['path'].stem}")
        except Exception as e:                                  # import failure is a contract failure
            rec["contract"] = False
            rec["problems"].append(f"import: {type(e).__name__}: {e}")
            results.append(rec)
            idx += 1
            continue
        problems = contract_problems(mod, m["path"])
        rec["problems"] += problems
        rec["contract"] = not problems
        src_text = m["path"].read_text()
        rec["abs_literals"] = sorted(set(ABSLIT.findall(src_text)))
        root_a = work / "rootA" / f"m{idx:02d}"
        root_b = work / "rootB" / f"m{idx:02d}"
        for k, row in enumerate(getattr(mod, "FIXTURES", []) or []):
            fx = {"fid": row.get("fid"), "tool": row.get("tool"), "expect": row.get("expect"),
                  "defects": row.get("defects")}
            if not callable(row.get("build")):
                fx["status"] = "contract-fail"
                rec["fixtures"].append(fx)
                continue
            reps = []
            # two builds at the SAME absolute fixture path (destroyed and rebuilt in between) is the
            # determinism definition the population builder uses; a third root measures portability only.
            for tag, root in (("r0", root_a), ("r1", root_a), ("r2", root_b)):
                try:
                    br = build_rep(hb, k44, mod, row, root, f"f{k:02d}")
                    ident = canonical(hb, br["dir"])
                    reps.append({"tag": tag, "dir": br["dir"], "argv": br["argv"],
                                 "argv_raw": br["argv_raw"],
                                 "tree_sha256": ident[0], "files": ident[1], "dirs": ident[2],
                                 "masked": ident[3], "error": None})
                except ValueError as e:
                    if "null character" not in str(e):
                        reps.append({"tag": tag, "error": f"{type(e).__name__}: {e}"})
                        continue
                    # canonical digest itself cannot resolve a NUL gitfile target: identity is defined
                    # instead by the same walk with NUL-carrying gitfile targets skipped (named limit).
                    try:
                        br = build_rep(hb, k44, mod, row, root, f"f{k:02d}")
                        saved = hb.gitfile_index_paths
                        hb.gitfile_index_paths = safe_gitfile_index_paths
                        try:
                            ident = canonical(hb, br["dir"])
                        finally:
                            hb.gitfile_index_paths = saved
                        reps.append({"tag": tag, "dir": br["dir"], "argv": br["argv"],
                                     "argv_raw": br["argv_raw"],
                                     "tree_sha256": ident[0], "files": ident[1], "dirs": ident[2],
                                     "masked": ident[3], "error": None,
                                     "identity_instrument": "canonical+NUL-gitfile-skip"})
                    except Exception as e2:
                        reps.append({"tag": tag, "error": f"{type(e2).__name__}: {e2}"})
                except Exception as e:
                    reps.append({"tag": tag, "error": f"{type(e).__name__}: {e}"})
            ok_build = all(r.get("error") is None for r in reps) and len(reps) == 3
            if ok_build:
                fx["tree_sha256"] = reps[0]["tree_sha256"]
                fx["tree_sha256_rep1"] = reps[1]["tree_sha256"]
                fx["tree_sha256_cross"] = reps[2]["tree_sha256"]
                fx["argv"] = reps[0]["argv"]
                fx["deterministic"] = reps[0]["tree_sha256"] == reps[1]["tree_sha256"] and reps[0]["argv"] == reps[1]["argv"]
                fx["root_independent"] = reps[0]["tree_sha256"] == reps[2]["tree_sha256"]
                instr = {r.get("identity_instrument") for r in reps if r.get("error") is None}
                if instr - {None}:
                    fx["identity_instrument"] = ",".join(sorted(x for x in instr if x))
                if len(instr) > 1:
                    fx["deterministic"] = False   # mixed identity instrument: not a verified two-build identity
                v = verdict(fence, reps[0]["dir"], fx["tool"], reps[0]["argv_raw"], work, idx * 10 + k)
                fx.update({"base": v["v"], "base_why": v["why"]})
            else:
                fx["deterministic"] = None
                fx["root_independent"] = None
                fx["base"] = None
                fx["errors"] = [r.get("error") for r in reps if r.get("error")]
            fx["status"] = ("ok" if ok_build and fx.get("deterministic") and fx.get("base") == "BREACH"
                            else "reject")
            rec["fixtures"].append(fx)
        results.append(rec)
        idx += 1

    # ---- de-duplicate by fixture identity: fid across modules, then byte-identical build identity ----
    def quality(r):
        fx = r["fixtures"]
        return (r["contract"] is True,
                bool(fx) and all(f.get("deterministic") for f in fx),
                bool(fx) and all(f.get("root_independent") for f in fx),
                not r.get("abs_literals"))

    ranked = sorted(results, key=lambda r: (tuple(not x for x in quality(r)),
                                            0 if r["source"] == "lane50" else 1,
                                            r["file"], r["sha256"]))
    kept, dropped = [], []
    seen_fid, seen_shape = {}, {}
    for r in ranked:
        fids = [f["fid"] for f in r["fixtures"] if f.get("fid")]
        dup = [f for f in fids if f in seen_fid]
        shapes = [(f.get("tree_sha256"), tuple(f.get("argv") or ()), f.get("tool"))
                  for f in r["fixtures"] if f.get("tree_sha256")]
        dup_shape = [s for s in shapes if s in seen_shape]
        if dup:
            dropped.append({"file": r["file"], "sha256": r["sha256"], "reason": f"duplicate fid(s) {dup} kept in {seen_fid[dup[0]]}"})
            continue
        if dup_shape:
            dropped.append({"file": r["file"], "sha256": r["sha256"],
                            "reason": f"duplicate build identity kept in {seen_shape[dup_shape[0]]}"})
            continue
        if any(f.get("status") != "ok" for f in r["fixtures"]) or not r["fixtures"]:
            dropped.append({"file": r["file"], "sha256": r["sha256"],
                            "reason": "gate: " + "; ".join(
                                f"{f['fid']}:{f.get('status')} base={f.get('base')} det={f.get('deterministic')}"
                                for f in r["fixtures"]) + ("; " + "; ".join(r["problems"]) if r["problems"] else "")})
            continue
        kept.append(r)
        for f in fids:
            seen_fid[f] = r["file"]
        for s in shapes:
            seen_shape[s] = r["file"]

    # ---- emit ----
    sealed = out / "sealed50"
    shutil.rmtree(sealed, ignore_errors=True)
    sealed.mkdir(parents=True)
    manifest = []
    for r in sorted(kept, key=lambda r: r["file"]):
        shutil.copyfile(r["src_path"], sealed / r["file"])
        for f in r["fixtures"]:
            manifest.append({"file": r["file"], "sha256": r["sha256"], "fixture": f["fid"],
                             "tool": f["tool"], "expected": f["expect"],
                             "base_verdict": f["base"], "base_why": f["base_why"],
                             "tree_sha256": f["tree_sha256"],
                             "tree_sha256_rep1": f.get("tree_sha256_rep1"),
                             "tree_sha256_cross": f.get("tree_sha256_cross"),
                             "argv": f["argv"],
                             "deterministic": f["deterministic"],
                             "root_independent": f["root_independent"],
                             "identity_instrument": f.get("identity_instrument", "canonical"),
                             "source": f"{r['source']}:{r['origin']}"})
    (out / "manifest.json").write_text(json.dumps({
        "rev": subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "fence": {"path": "plans/fixture_fence.py", "sha256": sha256_file(fence)},
        "candidates": len(results), "modules_kept": len(kept), "modules_dropped": len(dropped),
        "rows": manifest, "dropped": sorted(dropped, key=lambda d: d["file"]),
        "module_notes": [{"file": r["file"], "sha256": r["sha256"], "abs_literals": r.get("abs_literals", [])}
                         for r in sorted(kept, key=lambda r: r["file"])],
    }, indent=1) + "\n")
    with open(out / "manifest.tsv", "w") as fh:
        fh.write("file\tsha256\tfixture\ttool\texpected\tbase_verdict\tdeterministic\troot_independent\t"
                 "tree_sha256\ttree_sha256_rebuild\ttree_sha256_crossroot\n")
        for row in manifest:
            fh.write("\t".join(str(row[k]) for k in ("file", "sha256", "fixture", "tool", "expected",
                                                     "base_verdict", "deterministic", "root_independent",
                                                     "tree_sha256", "tree_sha256_rep1",
                                                     "tree_sha256_cross")) + "\n")
    with open(out / "modules.tsv", "w") as fh:
        fh.write("file\tsha256\tfixtures\texpected\tbase_verdicts\tdeterministic\troot_independent\tsource\n")
        for r in sorted(kept, key=lambda r: r["file"]):
            rows = [row for row in manifest if row["file"] == r["file"]]
            fh.write("\t".join([r["file"], r["sha256"],
                                ",".join(x["fixture"] for x in rows),
                                ",".join(x["expected"] for x in rows),
                                ",".join(x["base_verdict"] for x in rows),
                                ",".join(str(x["deterministic"]) for x in rows),
                                ",".join(str(x["root_independent"]) for x in rows),
                                f"{r['source']}:{r['origin']}"]) + "\n")
    print(f"CANDIDATES modules={len(results)} fixtures={sum(len(r['fixtures']) for r in results)}")
    print(f"KEPT modules={len(kept)} fixtures={len(manifest)}")
    print(f"DROPPED modules={len(dropped)}")
    for d in sorted(dropped, key=lambda d: d["file"]):
        print(f"DROP {d['file']} {d['sha256'][:12]} {d['reason']}")
    for r in sorted(kept, key=lambda r: r["file"]):
        print(f"KEEP {r['file']} {r['sha256']} fixtures={len(r['fixtures'])} source={r['source']}:{r['origin']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

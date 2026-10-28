#!/usr/bin/env python3
"""Round-50 C1 sealed-module contract audit (seat R50C1ExecSealedAudit, read-only).

Audits every module in the given directories against the FIXTURES contract the round-50 counter
(`plans/round50_c1_verify.py`) consumes:

  contract      module imports; `FIXTURES` is a non-empty list; each row is a dict carrying
                fid/tool/expect/defects/build; build(ctx, d) returns a list[str]; the fixture dir
                survives; every fid is unique inside its module.
  determinism   each fixture is built twice at the SAME absolute root (`.git/index` masked by the
                population builder's own `tree_identity`); the two canonical digests must be equal.
  root-indep.   a third build at a DIFFERENT absolute root; a digest that moves means the fixture
                embeds its absolute build root (an absolute build path), reported separately.
  abs-path      module source carries no bare absolute path literal, and no built fixture file
                contains a host path (the scratch root, /home/vgpnk, /tmp) instead of a path
                derived from its own build root.
  dup-fid       fid is unique across all audited modules and against the frozen r46 populations.
  leak          module stem / fid / marker string must not appear in fence-writer reports.

Supplementary (not part of the audit verdict): the BASE fence's verdict per fixture; the assemble
gate requires REFUSED.

Usage: audit_sealed.py --lane DIR --work DIR --modules DIR_OR_GLOB [...] [--json OUT]
Nothing is written to --lane.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

HOST_MARKERS = (b"/home/vgpnk", b"/fast/scratch", b"/tmp/")
FENCE_WRITERS = {
    "C1ExecRepair", "C1ExecRepairB", "C1ExecRepairDiff", "C1MutRepairB", "C1MutHostile",
    "C1CritRepairWeaker", "C1CritHygiene", "C1CritIdent", "C1CritPredicate",
    "C1ExecCleanRun", "C1ExecParity", "C1ExecCounterHygiene", "C1ExecCounterSelftest",
}
REQUIRED = ("fid", "tool", "expect", "defects", "build")
ABS_LITERAL = re.compile(r"""["'](/[A-Za-z0-9_.][^"'\n]*)["']""")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def walk_content(root):
    """Every (relpath, bytes) of a built fixture: regular file bodies and symlink targets."""
    out = []
    root = pathlib.Path(root)
    for top, dirs, files in os.walk(root):
        dirs[:] = sorted(dirs)
        t = pathlib.Path(top)
        for name in sorted(files + dirs):
            p = t / name
            try:
                st = os.lstat(p)
            except FileNotFoundError:
                continue
            rel = p.relative_to(root).as_posix()
            if os.path.islink(p):
                out.append((rel, os.readlink(p).encode()))
            elif os.path.isfile(p):
                try:
                    out.append((rel, p.read_bytes()))
                except (FileNotFoundError, PermissionError, IsADirectoryError):
                    pass
    return out



def build_each(hb, k44, mod, root, rec):
    """Per-fixture fallback: build one fixture at a time, catching per-fixture failures.

    Used when the module-level build raises (one bad fixture must not hide the others). Two builds at the
    same absolute root give the determinism comparison; each fixture also reports its own error.
    """
    fx = getattr(mod, "FIXTURES", []) or []
    out1, out2, out3 = [], [], []
    for k, row in enumerate(fx):
        if not isinstance(row, dict) or not callable(row.get("build")):
            continue
        attempts = []
        for rep in range(3):
            gen = root / f"x{k:03d}" / f"r{rep}"
            shutil.rmtree(gen, ignore_errors=True)
            gen.mkdir(parents=True)
            d = gen / "f000"
            d.mkdir(parents=True)
            try:
                argv = row["build"](hb.quiet_ctx(k44, gen), d)
                digest = hb.retry_read(hb.tree_identity, d)
                attempts.append({"fid": row.get("fid"), "tool": row.get("tool"),
                                 "expect": row.get("expect"), "defects": row.get("defects"),
                                 "argv": hb.normalize_argv(argv, d) if isinstance(argv, list) else argv,
                                 "dir": d, "tree_sha256": digest[0], "files": digest[1],
                                 "dirs": digest[2], "masked": digest[3]})
            except Exception as e:
                rec["problems"].append(f"fixture {row.get('fid')}: {type(e).__name__}: {e}")
                attempts.append(None)
        out1.append(attempts[0])
        out2.append(attempts[1])
        if len(attempts) > 2:
            out3.append(attempts[2])
    b1 = [x for x in out1 if x]
    b2 = [x for x in out2 if x]
    # determinism for the fallback path is judged on fixtures that digested in both builds
    good = [(a["fid"], a["tree_sha256"], b["tree_sha256"], c["tree_sha256"])
            for a, b, c in zip(out1, out2, out3) if a and b and c]
    rec["fallback_pairs"] = good
    return b1, b2


def build_at(hb, k44, module, gen):
    """Build every fixture of `module` into `gen` (fresh) and return per-fid receipts."""
    shutil.rmtree(gen, ignore_errors=True)
    gen.mkdir(parents=True)
    rows = []
    for fid, tool, expect, defects, argv, d, _b in hb.build_once(k44, module, gen):
        digest, n_files, n_dirs, masked = hb.retry_read(hb.tree_identity, d)
        rows.append({"fid": fid, "tool": tool, "expect": expect, "defects": defects,
                     "argv": hb.normalize_argv(argv, d), "dir": d, "tree_sha256": digest,
                     "files": n_files, "dirs": n_dirs, "masked": masked})
    return rows


def contract_problems(module, src):
    """Static + build-time contract checks that need only the module object."""
    problems = []
    fx = getattr(module, "FIXTURES", None)
    if not isinstance(fx, list) or not fx:
        problems.append("no FIXTURES list")
        return problems, []
    seen = set()
    for k, row in enumerate(fx):
        if not isinstance(row, dict):
            problems.append(f"FIXTURES[{k}] not a dict")
            continue
        missing = [key for key in REQUIRED if key not in row]
        if missing:
            problems.append(f"FIXTURES[{k}] missing {','.join(missing)}")
            continue
        if not isinstance(row["fid"], str) or not row["fid"].strip():
            problems.append(f"FIXTURES[{k}].fid not a non-empty str")
        if not isinstance(row["tool"], str) or not row["tool"]:
            problems.append(f"FIXTURES[{k}].tool not a non-empty str")
        if not isinstance(row["expect"], str) or not row["expect"]:
            problems.append(f"FIXTURES[{k}].expect not a non-empty str")
        if not isinstance(row["defects"], list):
            problems.append(f"FIXTURES[{k}].defects not a list")
        if not callable(row["build"]):
            problems.append(f"FIXTURES[{k}].build not callable")
            continue
        try:
            import inspect
            sig = inspect.signature(row["build"])
            if list(sig.parameters) != ["ctx", "d"] and len(sig.parameters) != 2:
                problems.append(f"FIXTURES[{k}].build signature {sig} != (ctx, d)")
        except (TypeError, ValueError):
            pass
        if row["fid"] in seen:
            problems.append(f"duplicate fid inside module: {row['fid']}")
        seen.add(row["fid"])
    for m in ABS_LITERAL.finditer(src):
        lit = m.group(1)
        if lit.rstrip("/") in ("/",):
            continue
        problems.append(f"absolute path literal in source: {lit}")
    return problems, [r["fid"] for r in fx if isinstance(r, dict) and isinstance(r.get("fid"), str)]


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _same_seat(seat, module_path):
    """True when a leaked name lands in the blind module's OWN seat report/dir (expected, not a leak)."""
    if not seat:
        return False
    owner = None
    parts = module_path.parts
    if "w1" in parts:
        idx = parts.index("w1")
        if idx + 1 < len(parts):
            owner = parts[idx + 1]
    if owner is None:
        return False
    o, s2 = _norm(owner), _norm(seat)
    return bool(o) and (o in s2 or s2 in o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--modules", nargs="+", required=True)
    ap.add_argument("--json", default=None)
    ap.add_argument("--leak-scan", nargs="*", default=[])
    ap.add_argument("--skip-base-fence", action="store_true")
    a = ap.parse_args()

    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    hb = load(lane / "plans/honest50/build_honest_population.py", "audit_hb")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "audit_k44")
    fence = None
    if not a.skip_base_fence:
        fence = load(lane / "plans/fixture_fence.py", "audit_fence")

    files = []
    for spec in a.modules:
        p = pathlib.Path(spec)
        if p.is_dir():
            files.extend(sorted(p.glob("*.py")))
        else:
            files.extend(sorted(pathlib.Path().glob(spec)) if not p.is_absolute() else [p])
    files = [f.resolve() for f in files]

    # frozen r46 fids: a sealed50 fid that collides with a frozen row hides which leg caught what
    frozen_fids = {}
    for rel in ("plans/sealed46", "plans/refusals46"):
        d = lane / rel
        if d.is_dir():
            for f in sorted(d.glob("*.py")):
                frozen_fids.setdefault(f.stem, set()).update(contract_problems(load(f, "fz_" + f.stem), f.read_text())[1])

    leak_blob = {}
    for spec in a.leak_scan:
        import glob as _glob
        for p in sorted(pathlib.Path(g) for g in _glob.glob(spec)) if "*" in spec else [pathlib.Path(spec)]:
            if p.is_file():
                try:
                    leak_blob[p.resolve()] = p.read_text(errors="replace")
                except OSError:
                    pass

    results = []
    all_fids = {}
    for i, path in enumerate(files):
        name = path.stem
        src = path.read_text()
        rec = {"module": str(path), "name": path.name, "stem": name, "problems": [],
               "fixtures": [], "deterministic": None, "root_independent": None,
               "host_paths": [], "abs_root_in_fixture": [], "base": {}, "build_error": None,
               "duplicate_fid": [], "leaks": []}
        try:
            mod = load(path, f"audit_mod_{i}_{re.sub(r'W', '_', name)}")
        except Exception as e:
            rec["problems"].append(f"import: {type(e).__name__}: {e}")
            results.append(rec)
            continue
        problems, fids = contract_problems(mod, src)
        rec["problems"] += problems
        gen = work / f"m{i:03d}"
        cross = work / "cross" / f"m{i:03d}"
        try:
            b1 = build_at(hb, k44, path, gen)
            b2 = build_at(hb, k44, path, gen)
            b2b = build_at(hb, k44, path, gen)
        except Exception as e:
            # a module whose build/digest raises still gets a per-fixture row where the fixture alone can run
            rec["build_error"] = f"{type(e).__name__}: {e}"
            rec["problems"].append("build: " + rec["build_error"])
            b1, b2 = build_each(hb, k44, mod, work / f"each{i:03d}", rec)
            if not b1:
                results.append(rec)
                continue
        try:
            b3 = build_at(hb, k44, path, cross)
        except Exception as e:
            b3 = None
            rec["problems"].append(f"cross-root build: {type(e).__name__}: {e}")

        d1 = {r["fid"]: r["tree_sha256"] for r in b1}
        d2 = {r["fid"]: r["tree_sha256"] for r in b2}
        d2b = {r["fid"]: r["tree_sha256"] for r in b2b}
        av1 = {r["fid"]: r["argv"] for r in b1}
        av2 = {r["fid"]: r["argv"] for r in b2}
        rec["deterministic"] = (d1 == d2 == d2b and av1 == av2 and len(b1) == len(b2) == len(b2b))
        rec["triple"] = {"a": d1, "b": d2, "c": d2b}
        if rec.get("fallback_pairs") and any(not (a == b == c) for _f, a, b, c in rec["fallback_pairs"]):
            rec["deterministic"] = False
        if b3 is not None:
            d3 = {r["fid"]: r["tree_sha256"] for r in b3}
            rec["root_independent"] = d1 == d3
            for fid in d1:
                if d1.get(fid) != d3.get(fid):
                    rec["abs_root_in_fixture"].append(fid)
        for r in b1:
            bodies = walk_content(r["dir"])
            for rel, body in bodies:
                for marker in HOST_MARKERS:
                    if marker in body:
                        rec["host_paths"].append(f"{r['fid']}:{rel}:{marker.decode()}")
                if str(gen).encode() in body:
                    rec["abs_root_in_fixture"].append(f"{r['fid']}:{rel}")
            v = None
            if fence is not None:
                try:
                    v = "BREACH" if fence.breach(str(r["dir"]), r["argv"], r["tool"]) else "ADMIT"
                except Exception as e:
                    v = f"ERROR {type(e).__name__}: {e}"
            rec["base"][r["fid"]] = v
            rec["fixtures"].append({"fid": r["fid"], "tool": r["tool"], "expect": r["expect"],
                                    "defects": r["defects"], "argv": r["argv"],
                                    "tree_sha256": r["tree_sha256"], "masked": r["masked"],
                                    "base": v})
            all_fids.setdefault(r["fid"], []).append(str(path))
        if path.parent.name not in ("sealed46", "refusals46"):
            for stem_set in frozen_fids.values():
                for fid in d1:
                    if fid in stem_set:
                        rec["duplicate_fid"].append(f"collides with frozen r46 fid {fid}")
        # name cross-check: stem, fids and the module's own docstring markers
        needles = {name, f'"{name}"'}
        needles.update(d1)
        markers = set(re.findall(r"\bfid\"?:\s*\"([a-z0-9][a-z0-9.-]{6,})\"", src))
        needles.update(markers)
        for p, body in leak_blob.items():
            for needle in needles:
                if needle and needle in body:
                    seat = p.parts[p.parts.index("w1") + 1] if "w1" in p.parts else None
                    rec["leaks"].append({"where": str(p), "seat": seat, "needle": needle,
                                         "self": _same_seat(seat, path)})
        results.append(rec)

    for fid, mods in all_fids.items():
        if len(set(mods)) > 1:
            for rec in results:
                if rec["module"] in mods:
                    rec["duplicate_fid"].append(f"fid {fid} in {len(set(mods))} modules")

    confirmed = []
    for rec in results:
        ok = (not rec["problems"] and rec["deterministic"] and not rec["duplicate_fid"]
              and not [l for l in rec["leaks"] if not l["self"]])
        rec["contract_ok"] = not rec["problems"]
        rec["eligible"] = bool(ok)
        if ok:
            confirmed.append(rec["name"])
        print(f"MODULE {rec['name']} contract={'ok' if rec['contract_ok'] else 'FAIL'} "
              f"deterministic={'yes' if rec['deterministic'] else 'no'} "
              f"root_independent={rec['root_independent']} "
              f"host_paths={len(rec['host_paths'])} abs_root_in_fixture={len(rec['abs_root_in_fixture'])} "
              f"dup_fid={len(rec['duplicate_fid'])} leaks={len([l for l in rec['leaks'] if not l['self']])}")
        for p in rec["problems"]:
            print(f"  CONTRACT-FAIL {rec['name']} {p}")
        if rec["build_error"]:
            print(f"  BUILD-ERROR {rec['name']} {rec['build_error']}")
        if rec["deterministic"] is False:
            ids1 = {r['fid']: r['tree_sha256'] for r in rec["fixtures"]}
            print(f"  NONDETERMINISTIC {rec['name']} fids={','.join(ids1)}")
        if rec["abs_root_in_fixture"]:
            print(f"  ABS-BUILD-ROOT {rec['name']} {','.join(rec['abs_root_in_fixture'][:6])}")
        for row in rec["host_paths"][:6]:
            print(f"  HOST-PATH {rec['name']} {row}")
        for row in rec["duplicate_fid"]:
            print(f"  DUPLICATE-FID {rec['name']} {row}")
        for row in rec["leaks"]:
            kind = "NAME-LEAK" if not row["self"] else "SELF-NAMED"
            print(f"  {kind} {rec['name']} {row['where']} seat={row['seat']} needle={row['needle']}")
        for fid, v in rec["base"].items():
            print(f"  BASE {rec['name']} {fid} {v}")
    # the four named row sets (item R50C1ExecSealedAudit) + the admissible count
    print("")
    print("== CONTRACT-OK ==")
    for rec in results:
        print(f"contract-ok {rec['name']} {'yes' if rec['contract_ok'] else 'NO'}")
    print("== NONDETERMINISTIC ==")
    for rec in results:
        if rec["deterministic"] is False:
            print(f"nondeterministic {rec['name']}")
    if not any(r["deterministic"] is False for r in results):
        print("nondeterministic none")
    print("== IDENTITY-ROOT-DEPENDENT ==")
    for rec in results:
        if rec["root_independent"] is False:
            print(f"root-dependent {rec['name']} fids={','.join(rec['abs_root_in_fixture'][:4])}")
    if not any(r["root_independent"] is False for r in results):
        print("root-dependent none")
    print("== DUPLICATE-FID ==")
    for rec in results:
        for row in rec["duplicate_fid"]:
            print(f"duplicate-fid {rec['name']} {row}")
    if not any(r["duplicate_fid"] for r in results):
        print("duplicate-fid none")
    print("== NAME-LEAKS ==")
    for rec in results:
        for row in rec["leaks"]:
            if not row["self"]:
                print(f"name-leaks {rec['name']} {row['where']} seat={row['seat']} needle={row['needle']}")
    if not any([l for l in r["leaks"] if not l["self"]] for r in results):
        print("name-leaks none")
    print(f"SEALED50-CANDIDATES {len(confirmed)}/{len(results)} {' '.join(confirmed)}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps({"lane": str(lane), "modules": results,
                                                    "eligible": confirmed}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

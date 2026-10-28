#!/usr/bin/env python3
"""Author mutant rows as exact-substring transforms of a fence, generate the inline unified diff, and witness
the kill against the counter's own predicate (verdict vector over HONEST + REFUSALS + SEALED).

A row is kept only when its payload applies (patch rc=0, module imports) AND the verdict vector changes.
`find` must occur exactly once in the fence; a row whose `find` is absent is reported, not silently dropped.

Usage: author_and_witness.py --lane CLONE --fence FENCE --transforms T.json --out rows.json [--work DIR]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_payload(src: str, new: str, tmp: pathlib.Path, tag: str) -> str:
    a = tmp / f"{tag}.a.py"
    b = tmp / f"{tag}.b.py"
    a.write_text(src)
    b.write_text(new)
    p = subprocess.run(["diff", "-u", "--label", "a/plans/fixture_fence.py",
                        "--label", "b/plans/fixture_fence.py", str(a), str(b)],
                       capture_output=True, text=True)
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fence", required=True)
    ap.add_argument("--transforms", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    fence_path = pathlib.Path(a.fence).resolve()
    work = pathlib.Path(tempfile.mkdtemp(prefix="k50-auth-", dir=a.work))
    tf = pathlib.Path(a.transforms)
    if tf.suffix == ".py":
        tx = load(tf, "k50_transforms").TX
    else:
        tx = json.loads(tf.read_text())
    src = fence_path.read_text()

    try:
        verify = load(lane / "plans/round50_c1_verify.py", "k50_verify")
        hb = load(lane / "plans/honest50/build_honest_population.py", "k50_hb")
        hb.ALLOW_NO_REPO = True
        k44 = load(lane / "plans/round44_c1_verify.py", "k50_k44")
        rows = verify.parse_population(lane / "plans/honest50/population.txt")
        modules, seen = [], set()
        for r in rows:
            if r["module"] in seen:
                continue
            seen.add(r["module"])
            modules.append((lane / r["module"], r["module"].replace("/", "-")[:-3]))
        honest, failures = verify.build_all(hb, k44, modules, work / "honest")
        hostile_built = []
        for rel in ("plans/refusals46", "plans/sealed46", "plans/sealed50"):
            d = lane / rel
            if not d.is_dir():
                continue
            files = sorted(d.glob("*.py"))
            fixtures, _x = verify.build_all(
                hb, k44, [(f, f"{rel.split('/')[-1]}-{f.stem}") for f in files],
                work / rel.replace("/", "-"))
            hostile_built.append((rel, files, fixtures))
        allfx = list(honest)
        for _rel, _f, fixtures in hostile_built:
            allfx += fixtures
        module_of = {f["fid"]: f["module"] for f in allfx}

        fence = load(fence_path, "k50_candidate")
        ref = verify.verdicts(fence, allfx)
        print(f"FENCE {fence_path} sha256={verify.sha256_file(fence_path)}")
        print(f"FIXTURES honest={len(honest)} total={len(allfx)} build_errors={len(failures)}")

        kept, dropped = [], []
        for t in tx:
            tid = t["id"]
            t.setdefault("class", t.get("cls", ""))
            n = src.count(t["find"])
            if n != 1:
                dropped.append({"id": tid, "class": t["class"], "why": f"find occurs {n}x (needs exactly 1)"})
                print(f"ROW {tid} DROP find-occurrences={n}")
                continue
            new = src.replace(t["find"], t["repl"], 1)
            if new == src:
                dropped.append({"id": tid, "class": t["class"], "why": "transform is a no-op on this fence"})
                print(f"ROW {tid} DROP no-op")
                continue
            payload = make_payload(src, new, work, tid)
            dest = work / "mutants" / f"{tid}.py"
            path, why = verify.apply_mutant(fence_path, payload, dest)
            if path is None:
                dropped.append({"id": tid, "class": t["class"], "why": f"payload does not apply: {why}"})
                print(f"ROW {tid} DROP not-applicable {why[:100]}")
                continue
            mod = load(path, f"k50_mut_{tid.replace('-', '_')}")
            try:
                mv = verify.verdicts(mod, allfx)
            except Exception as e:
                dropped.append({"id": tid, "class": t["class"], "why": f"fence raises: {e}"})
                print(f"ROW {tid} DROP raises {e}")
                continue
            diffs = []
            for old, nv in zip(ref, mv):
                if old["v"] != nv["v"]:
                    diffs.append({"fid": nv["fid"], "module": module_of.get(nv["fid"], ""),
                                  "old": old["v"], "new": nv["v"],
                                  "old_why": old["why"][:160], "new_why": nv["why"][:160]})
            rec = {"id": tid, "class": t["class"], "payload": payload,
                   "payload_sha256": hashlib.sha256(payload.encode()).hexdigest(),
                   "description": t["description"], "expected_effect": t["effect"],
                   "payload_kind": "unified-diff",
                   "digest": verify.sha256_file(path)}
            if diffs:
                rec["diffs"] = diffs
                kept.append(rec)
                d0 = diffs[0]
                print(f"ROW {tid} CAUGHT n={len(diffs)} first={d0['fid']} {d0['old']}->{d0['new']}")
            else:
                shadow = [(a["fid"], a["why"], b["why"]) for a, b in zip(ref, mv) if a["why"] != b["why"]]
                dropped.append({"id": tid, "class": t["class"],
                                "why": "not caught: verdict vector unchanged",
                                "reason_changes": len(shadow),
                                "example_new_reason": (shadow[0][2][:150] if shadow else ""),
                                "payload": payload,
                                "payload_sha256": hashlib.sha256(payload.encode()).hexdigest(),
                                "digest": verify.sha256_file(path)})
                print(f"ROW {tid} DROP survived (vector unchanged) reason_changes={len(shadow)}")

        pathlib.Path(a.out).write_text(json.dumps({"fence_sha256": verify.sha256_file(fence_path),
                                                   "kept": kept, "dropped": dropped}, indent=1) + "\n")
        print(f"SUMMARY kept={len(kept)} dropped={len(dropped)}")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

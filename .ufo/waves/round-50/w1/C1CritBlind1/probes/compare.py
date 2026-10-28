"""Scratch discriminator for seat R50C1CritBlind1: build the two blind fixtures and the honest in-`d`
indirection classes they must not be confused with (`n20`/`n21` gitfile, `n22` alternates), then score all of
them through three fences: the frozen base fence, a naive pointer-resolution repair, and the same repair with
realpath containment. A blind module is discriminating iff naive ADMITs it and correct REFUSEs it.
"""
import argparse
import importlib.util
import json
import pathlib
import sys

BLIND = ["s50_gitfile_symlink_chain", "s50_alternates_dotdot_abs"]
HONEST = ["n20_linked_worktree", "n21_separate_gitdir", "n22_alternates_in_d"]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def verdict(fence, d, argv, tool):
    try:
        why = fence.breach(d, argv, tool)
    except Exception as e:                                            # noqa: BLE001
        return "ERROR", f"{type(e).__name__}: {e}"
    return ("BREACH", why) if why else ("ADMIT", None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--blind", required=True)
    ap.add_argument("--honest", required=True, nargs="+")
    ap.add_argument("--naive", required=True)
    a = ap.parse_args()
    lane, work = pathlib.Path(a.lane).resolve(), pathlib.Path(a.work).resolve()
    k44 = load(lane / "plans/round44_c1_verify.py", "d_k44")
    base = load(lane / "plans/fixture_fence.py", "d_base")
    nv = load(a.naive, "d_naive")

    jobs = [("blind", [work / a.blind], BLIND), ("honest", [lane / h for h in a.honest], HONEST)]
    rows = []
    for kind, roots, names in jobs:
        for name in names:
            path = next((r / f"{name}.py" for r in roots if (r / f"{name}.py").is_file()), None)
            if path is None:
                rows.append({"kind": kind, "module": name, "error": f"missing {name}.py under {[str(r) for r in roots]}"})
                continue
            mod = load(path, f"d_{name}")
            for fx in mod.FIXTURES:
                dest = work / name / fx["fid"]
                d = dest / "f000"
                d.mkdir(parents=True, exist_ok=True)
                ctx = k44.Ctx(dest)
                try:
                    argv = fx["build"](ctx, d)
                except Exception as e:                                # noqa: BLE001
                    rows.append({"kind": kind, "module": name, "fid": fx["fid"],
                                 "error": f"build: {type(e).__name__}: {e}"})
                    continue
                del ctx
                row = {"kind": kind, "module": name, "fid": fx["fid"], "tool": fx["tool"]}
                for label, f in (("base", base), ("naive", nv), ("correct", nv)):
                    fn = f.breach if label != "naive" else f.naive_breach
                    v, why = verdict(_Fn(fn), d, argv, fx["tool"])
                    row[label] = v
                    row[f"{label}_why"] = why
                rows.append(row)
    print(json.dumps(rows, indent=2))
    disc = [r for r in rows if r.get("kind") == "blind" and r.get("naive") == "ADMIT" and r.get("correct") == "BREACH"]
    print(f"DISCRIMINATING blinds={len(disc)}/{sum(1 for r in rows if r.get('kind') == 'blind')}")
    return 0


class _Fn:
    def __init__(self, fn):
        self.breach = fn


if __name__ == "__main__":
    sys.exit(main())

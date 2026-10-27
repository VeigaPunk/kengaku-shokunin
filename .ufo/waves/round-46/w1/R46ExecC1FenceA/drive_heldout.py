#!/usr/bin/env python3
"""Held-out driver for seat R46ExecC1FenceA: run every round-45 held-out module through the round-45 counter's
own builder and fence runner against the repaired fence in this clone. Read-only; writes only under --work."""
import argparse
import importlib.util
import pathlib
import sys

A3 = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/a3w1")
MODULES = [
    ("ho", A3 / "R45HoIncludeIf/h1_cr_include.py"),
    ("ho", A3 / "R45HoIncludeIf/h2_includeif_cond.py"),
    ("ho", A3 / "R45HoIncludeIf/h3_bom_symlink.py"),
    ("control", A3 / "R45HoIncludeIf/h4_controls.py"),
    ("ho", A3 / "R45HoSymlinks/link_hostiles.py"),
    ("ho", A3 / "R45HoArgvEnv/argv_env.py"),
    ("ho", A3 / "R45HoCommondir2/modules/g1_cdrel.py"),
    ("ho", A3 / "R45HoCommondir2/modules/g2_gitfile.py"),
    ("ho", A3 / "R45HoCommondir2/modules/g3_wtmeta.py"),
    ("ho", A3 / "R45HoCommondir2/modules/g4_cdrel_hidden.py"),
    ("ho", A3 / "R45HoConfigKeys/configkeys.py"),
]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    root = pathlib.Path(a.work).resolve()
    root.mkdir(parents=True, exist_ok=True)
    k45 = load(lane / "plans/round45_c1_verify.py", "k45")
    k44 = k45.load(lane / "plans/round44_c1_verify.py", "k44")
    (root / "harness.py").write_text(k45.HARNESS)
    (root / "fence").mkdir(exist_ok=True)
    fence_copy = root / "fence/fixture_fence.py"
    fence_copy.write_bytes((lane / "plans/fixture_fence.py").read_bytes())
    print(f"FENCE-COPY sha256={k45.sha256(fence_copy)}")
    rows, n, fails = [], 0, 0
    for kind, mod in MODULES:
        try:
            fxs = k45.build_module(k44, lane, root, mod)
        except Exception as e:  # a build failure is a driver failure, not a fence verdict
            print(f"BUILD-ERROR {mod.name} {type(e).__name__}: {str(e)[:160]}")
            fails += 1
            continue
        res = []
        for fx in fxs:
            n += 1
            verdict, why, opens = k45.run_fence(k44, lane, root, fence_copy, fx, n)
            res.append((fx, verdict, why, opens))
            print(f"FENCE-RUN {mod.name} {fx['fid']} {verdict} opens={opens}" + (f" -- {why}" if why else ""))
        admitted = sum(v in ("ADMIT", "ERROR") for _f, v, _w, _o in res)
        hung = sum(v == "HUNG" for _f, v, _w, _o in res)
        read = sum(o > 0 for _f, _v, _w, o in res)
        opens = sum(o for _f, _v, _w, o in res)
        verdict = "LEAKED" if admitted else ("HUNG" if hung else ("READ" if read else "clean"))
        rows.append((kind, mod.name, len(res), admitted, read, hung, opens, verdict))
        print(f"MODULE {mod.name} fixtures={len(res)} admitted={admitted} read_fixtures={read} hung={hung}"
              f" outside_opens={opens} verdict={verdict}")
    print("\n| module | fixtures | admitted | read | hung | outside opens | verdict |")
    print("|---|---|---|---|---|---|---|")
    for kind, name, fx, adm, rd, hg, op, vd in rows:
        print(f"| {name} ({kind}) | {fx} | {adm} | {rd} | {hg} | {op} | {vd} |")
    hostile = [r for r in rows if r[0] == "ho"]
    clean = sum(r[7] == "clean" for r in hostile)
    print(f"HELDOUT modules={len(hostile)} clean={clean} leaked={sum(r[7]=='LEAKED' for r in hostile)}"
          f" read={sum(r[7]=='READ' for r in hostile)} hung={sum(r[7]=='HUNG' for r in hostile)}")
    print(f"CONTROLS modules={len(rows)-len(hostile)} verdicts={[r[7] for r in rows if r[0] == 'control']}")
    return 0 if clean == len(hostile) and not fails else 1


if __name__ == "__main__":
    sys.exit(main())

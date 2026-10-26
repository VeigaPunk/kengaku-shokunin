#!/usr/bin/env python3
"""F37XMutP6 probe — legitimacy of the two P6 survivors.

X1 (teaches threshold lowered by one) and X4 (url compare blind to scheme/host) survive the frozen
battery. For each, build one single-row registry tree that the FROZEN gate must reject and the mutant
must accept: if it does, the survivor is a real weakened check the battery simply never exercises
(a battery limit), not an equivalent mutant. Also prints the P6 clause line of every p6.py fixture so
the per-fixture bad count can be read against the docstrings.
"""
import argparse
import hashlib
import importlib.util
import pathlib
import subprocess
import sys

MUTANTS = {
    "X1": ('if len(cells[6].split()) < rules["min_teaches_words"]:',
           'if len(cells[6].split()) < rules["min_teaches_words"] - 1:'),
    "X4": ('url.group(0) != p.spec["raw_base"] + row["upstream"]',
           'url.group(0).split("://", 1)[-1] != (p.spec["raw_base"] + row["upstream"]).split("://", 1)[-1]'),
}


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
    root = pathlib.Path(a.work).resolve() / "probe"
    root.mkdir(parents=True, exist_ok=True)
    r37 = load(lane / "plans/round37_c1_verify.py", "k37c")
    p6 = load(lane / "plans/battery37/p6.py", "k37p6")
    r36 = r37.load_r36(lane)
    ctx = r37.Ctx(lane, r36)
    gates = {}
    gdir = root / "gates"
    gdir.mkdir(exist_ok=True)
    src = (lane / "plans/pkg_gate.py").read_text()
    (gdir / "ref.py").write_text(src)
    gates["ref"] = gdir / "ref.py"
    for mid, (old, new) in MUTANTS.items():
        assert src.count(old) == 1, (mid, src.count(old))
        (gdir / f"{mid}.py").write_text(src.replace(old, new, 1))
        gates[mid] = gdir / f"{mid}.py"

    def run(gate, d):
        r = subprocess.run([sys.executable, str(gate), "package", "--root", str(d),
                            "--require-clean-tree", "--spec", str(ctx.spec_path)],
                           capture_output=True, text=True, timeout=900)
        p6line = next((l for l in r.stdout.splitlines() if l.startswith("P6 ")), "-")
        defects = sorted({m.group(1) for m in map(r37.CLAUSE_LINE.match, r.stdout.splitlines())
                          if m and m.group(2) == "DEFECT"})
        return r.returncode, defects, p6line

    # --- p6.py fixtures: the P6 line must report exactly one bad entry ---------------------------
    print("SECTION p6-fixture-detail")
    for i, fx in enumerate(p6.FIXTURES):
        d = root / "fx" / f"p{i:02d}"
        d.mkdir(parents=True)
        argv = fx["build"](ctx, d)
        rc, defects, p6line = run(gates["ref"], d)
        print(f"FIXTURE {fx['fid']} rc={rc} defects={','.join(defects)} {p6line}")

    # --- survivor legitimacy probes: frozen gate rejects, survivor accepts -----------------------
    probes = []
    d = ctx.genuine_package(root / "limit-x1")
    p6._set_cell(d, "S105", 6, "alpha beta gamma delta epsilon zeta eta")
    ctx.git_add(d)
    probes.append(("X1", d, "S105 teaches cell = 7 words (min_teaches_words=8)"))
    d = ctx.genuine_package(root / "limit-x4")
    path = d / "corpus/SOURCES.md"
    lines = path.read_text().splitlines()
    hit = 0
    for j, line in enumerate(lines):
        m = p6.SOURCE_ROW.match(line)
        if m and m.group(1) == "S107":
            lines[j] = line.replace("https://raw.githubusercontent.com/", "http://raw.githubusercontent.com/")
            hit += 1
    assert hit == 1, hit
    path.write_text("\n".join(lines) + "\n")
    ctx.git_add(d)
    probes.append(("X4", d, "S107 pinned raw url scheme swapped https -> http"))

    print("SECTION survivor-legitimacy")
    for mid, d, label in probes:
        results = {name: run(gate, d) for name, gate in gates.items()}
        ref_rc, ref_def, _ = results["ref"]
        m_rc, m_def, _ = results[mid]
        print(f"PROBE {mid} {label} | frozen_rc={ref_rc} frozen_defects={','.join(ref_def) or '-'} "
              f"| {mid}_rc={m_rc} {mid}_defects={','.join(m_def) or '-'} "
              f"| survivor_is_real_defect={'yes' if ref_rc == 1 and m_rc == 0 else 'NO'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

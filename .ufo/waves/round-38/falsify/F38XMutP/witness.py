#!/usr/bin/env python3
"""F38XMutP survivor witnesses (round-38 wave 2, falsify seat F38XMutP).

For each SURVIVING extra mutant (X01, X05, X15 — no battery fixture kills it) this builds one
concrete package on which the reference gate and the mutant gate disagree at the clause level,
proving each survivor is a real behavioural difference (non-equivalent), not a battery artefact.

  W-X01: genuine package with the SECOND pinned instrument corrupted -> ref P1 DEFECT, X01 P1 ok
         (X01 checks only the first pin; the battery's only instrument fixture corrupts the first).
  W-X05: genuine package with one quote row rewritten to 26 words (hi=25) -> ref P3 DEFECT, X05 P3 ok
         (X05 loosens the upper word bound by one; no battery quote sits above the range).
  W-X15: genuine package with a DUPLICATE `source: S106 ...` line appended -> ref P7 DEFECT, X15 P7 ok
         (X15 compares only the first collected url; no battery row carries two source lines).

Usage: witness.py LANE WORK   (LANE = clean clone of the landing tip; WORK = scratch parent)
"""
import hashlib
import importlib.util
import pathlib
import shutil
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
WORK = pathlib.Path(sys.argv[2]).resolve()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MUT = {
    "X01": (r'bad = [rel for rel, dig in pins.items() if sha256(p.root / rel) != dig]',
            r'bad = [rel for rel, dig in list(pins.items())[:1] if sha256(p.root / rel) != dig]'),
    "X05": (r'short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]',
            r'short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi + 1]'),
    "X15": (r'if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:',
            r'if (prov.get(sid) or [""])[0] != p.spec["raw_base"] + row["upstream"]:'),
}


def main():
    m = load(LANE / "plans" / "round38_c1_verify.py", "kengaku_r38_c1")
    r37 = load(LANE / m.R37_REL, "kengaku_r37_c1")
    r36 = r37.load_r36(LANE)
    ctx = r37.Ctx(LANE, r36)
    gate_src = (LANE / r37.GATE_REL).read_text()
    root = pathlib.Path(tempfile.mkdtemp(prefix="f38xmutp-w-", dir=WORK))
    gdir = root / "gates"
    gdir.mkdir()
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)
    mut_gates = {}
    for mid, (old, new) in MUT.items():
        assert gate_src.count(old) == 1, mid
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        mut_gates[mid] = mg

    def run(gate, d):
        return m.run_gate(gate, ctx.spec_path, ["package", "--root", str(d), "--require-clean-tree"])

    def witness(name, mid, prepare, want_ref, want_mut):
        d = root / name
        prepare(d)
        ref = run(ref_gate, d)
        mut = run(mut_gates[mid], d)
        ok = want_ref in ref[1] and want_ref not in mut[1]
        print(f"WITNESS {name} mutant={mid} ref_rc={ref[0]} ref_defects={','.join(sorted(ref[1])) or '-'}"
              f" mut_rc={mut[0]} mut_defects={','.join(sorted(mut[1])) or '-'}"
              f" flip={want_ref}->{want_mut} {'ok' if ok else 'FAIL'}")
        return ok

    def prep_x01(d):
        ctx.genuine_package(d)
        rel2 = list(ctx.spec["frozen_instruments"])[1]
        f = d / rel2
        f.write_text(f.read_text() + "\n# off-pin witness byte\n")

    def prep_x05(d):
        ctx.genuine_package(d)
        entry = d / pathlib.PurePosixPath(ctx.spec["entry"])
        text = entry.read_text()

        def fn(data):
            mm = r36.QUOTE_ROW.match(data[0])
            t26 = " ".join(f"w{i}" for i in range(1, 27))
            row = f'| {mm.group(0).split("|")[1].strip()} | “{t26}” | `{mm.group(2)}:{mm.group(3)}` |'
            return [row] + data[1:]

        entry.write_text(r36.rewrite_quotes(text, fn))

    def prep_x15(d):
        ctx.genuine_package(d)
        entry = d / pathlib.PurePosixPath(ctx.spec["entry"])
        text = entry.read_text()
        line = next(l for l in text.splitlines() if l.startswith("source: S106"))
        entry.write_text(text + "\n" + line + "\n")

    oks = [witness("wx01", "X01", prep_x01, "P1", "P1-ok"),
           witness("wx05", "X05", prep_x05, "P3", "P3-ok"),
           witness("wx15", "X15", prep_x15, "P7", "P7-ok")]
    print(f"WITNESSES total=3 ok={sum(oks)}")
    shutil.rmtree(root, ignore_errors=True)
    return 0 if all(oks) else 1


if __name__ == "__main__":
    sys.exit(main())

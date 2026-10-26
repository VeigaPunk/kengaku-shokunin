#!/usr/bin/env python3
"""R39CritC1Equiv witness ladder: rebuild each frozen mutant's declared direction from inputs I construct,
sweep the mutation-relevant parameter across its boundary, and classify every observed (rc, DEFECT set,
ok set) difference with the frozen counter's own exhibits() predicate.

Usage: witness_ladder.py LANE
Everything is written under a scratch root given by $R39W (default: alongside this script).
"""
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

LANE = pathlib.Path(sys.argv[1]).resolve()
ROOT = pathlib.Path(os.environ.get("R39W", pathlib.Path(__file__).resolve().parent / "wladder")).resolve()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


c39 = load(LANE / "plans/round39_c1_verify.py", "c39")
r37 = load(LANE / c39.R37_REL, "r37")
r36 = r37.load_r36(LANE)
ctx = r37.Ctx(LANE, r36)
GATE_SRC = (LANE / "plans/pkg_gate.py").read_text()

ROOT.mkdir(parents=True, exist_ok=True)
GDIR = ROOT / "gates"
GDIR.mkdir(exist_ok=True)
REF = GDIR / "ref.py"
REF.write_text(GATE_SRC)
MUT = {}
for mid, clause, direction, label, wit, old, new in c39.MUTANTS:
    assert GATE_SRC.count(old) == 1, mid
    mg = GDIR / f"{mid}.py"
    mg.write_text(GATE_SRC.replace(old, new, 1))
    compile(mg.read_text(), str(mg), "exec")
    MUT[mid] = (clause, direction, mg)

PKG = ["package", "--require-clean-tree"]
results = []
n = 0


def run(gate, argv):
    return c39.run_gate(gate, ctx.spec_path, argv)


def probe(name, mid, argv, expect, defects, d):
    global n
    n += 1
    clause, direction, mg = MUT[mid]
    fx = {"fid": name, "expect": expect, "defects": defects, "argv": argv}
    fam = c39.family_ok(clause, argv)
    ref = run(REF, argv)
    mut = run(mg, argv)
    hits = [x for x in c39.DIRECTIONS if fam and c39.exhibits(clause, x, fx, ref, mut)] if ref != mut else []
    rec = {"probe": name, "mutant": mid, "clause": clause, "declared": direction, "family": fam,
           "expect": expect, "defects": defects,
           "ref": [ref[0], sorted(ref[1]), sorted(ref[2])], "mut": [mut[0], sorted(mut[1]), sorted(mut[2])],
           "directions": hits}
    results.append(rec)
    tag = "EXHIBIT" if direction in hits else ("SAME" if ref == mut else f"ONLY-{hits or 'UNCLASSIFIED'}")
    print(f"PROBE {name} {mid} {clause}/{direction} ref={ref[0]}:{','.join(sorted(ref[1])) or '-'}"
          f" mut={mut[0]}:{','.join(sorted(mut[1])) or '-'} {tag}")
    return tag


def genuine(d):
    d = pathlib.Path(d)
    ctx.genuine_package(d)
    return d


def main():
    # ---------- M06 / M05: exit-code legs ----------
    d = genuine(ROOT / "p-genuine")
    ctx.git_add(d)
    probe("accept-genuine", "M06", PKG + ["--root", str(d)], "accept", [], d)
    probe("accept-genuine", "M05", PKG + ["--root", str(d)], "accept", [], d)
    rd = ROOT / "p-empty"
    rd.mkdir(exist_ok=True)
    (rd / "README.md").write_text("x\n")
    subprocess_argv = PKG + ["--root", str(rd)]
    probe("reject-emptydir", "M05", subprocess_argv, "reject", sorted(run(REF, subprocess_argv)[1]), rd)
    probe("reject-emptydir", "M06", subprocess_argv, "reject", sorted(run(REF, subprocess_argv)[1]), rd)
    badroot = ROOT / "p-notadir.txt"
    badroot.write_text("x\n")
    probe("setup-notadir", "M06", PKG + ["--root", str(badroot)], "error", [], badroot)
    gline = ROOT / "erratum-genuine.md"
    gline.write_text(ctx.d5_line() + "\n")
    probe("d5-genuine", "M06", ["d5-line", "--file", str(gline),
                                "--capture-dir", str(ctx.d5_capture_dir())], "accept", [], ROOT)
    probe("d5-genuine", "M05", ["d5-line", "--file", str(gline),
                                "--capture-dir", str(ctx.d5_capture_dir())], "accept", [], ROOT)

    # ---------- M02 (P1 silence): which pin index is checked ----------
    pins = list(ctx.spec["frozen_instruments"])
    for k, rel in enumerate(pins):
        dd = genuine(ROOT / f"p-pin{k}")
        f = dd / rel
        f.write_text(f.read_text() + "\n# off-pin witness byte\n")
        ctx.git_add(dd)
        argv = PKG + ["--root", str(dd)]
        probe(f"pin-index{k}", "M02", argv, "reject", sorted(run(REF, argv)[1]), dd)
    # control: no corrupted pin, but the first pin *file* deleted
    dd = genuine(ROOT / "p-pin0-deleted")
    (dd / pins[0]).unlink()
    ctx.git_add(dd)
    argv = PKG + ["--root", str(dd)]
    probe("pin0-deleted", "M02", argv, "reject", sorted(run(REF, argv)[1]), dd)

    # ---------- M03 (P3 silence): word count at the upper bound ----------
    lo, hi = ctx.spec["entry_rules"]["quote_words"]
    for want in (hi, hi + 1, hi + 2):
        dd = genuine(ROOT / f"p-words{want}")
        entry = dd / pathlib.PurePosixPath(ctx.spec["entry"])
        text = entry.read_text()

        def fn(rows, want=want):
            out = []
            for row in rows:
                m = r36.QUOTE_ROW.match(row)
                if m and len(out) == 0:
                    cells = row.split("|")
                    t = " ".join(f"w{i}" for i in range(1, want + 1))
                    out.append(f'| {cells[1].strip()} | “{t}” | `{m.group(2)}:{m.group(3)}` |')
                else:
                    out.append(row)
            return out

        entry.write_text(r36.rewrite_quotes(text, fn))
        ctx.git_add(dd)
        argv = PKG + ["--root", str(dd)]
        probe(f"words-{want}", "M03", argv, "reject", sorted(run(REF, argv)[1]), dd)

    # ---------- M04 (P7 silence): source-line multiplicity ----------
    entry_rel = ctx.spec["entry"]
    first_sid = sorted(ctx.spec["rows"])[0]
    for k, correct in ((1, False), (1, True), (2, False)):
        dd = genuine(ROOT / f"p-srcline{k}{'ok' if correct else 'bad'}")
        entry = dd / pathlib.PurePosixPath(entry_rel)
        text = entry.read_text()
        gen = next(l for l in text.splitlines() if l.startswith(f"source: {first_sid}"))
        url = re.search(r"https?://\S+", gen).group(0)
        extra = gen if correct else gen.replace(url, url + "-stale")
        entry.write_text(text + "\n" + "\n".join([extra] * k) + "\n")
        ctx.git_add(dd)
        argv = PKG + ["--root", str(dd)]
        probe(f"srcline-{k}-{'same' if correct else 'stale'}", "M04", argv, "reject", sorted(run(REF, argv)[1]), dd)
    dd = genuine(ROOT / "p-srcline-first-stale")
    entry = dd / pathlib.PurePosixPath(entry_rel)
    text = entry.read_text()
    gen = next(l for l in text.splitlines() if l.startswith(f"source: {first_sid}"))
    url = re.search(r"https?://\S+", gen).group(0)
    entry.write_text(text.replace(gen, gen.replace(url, url + "-stale")))
    ctx.git_add(dd)
    argv = PKG + ["--root", str(dd)]
    probe("srcline-first-stale", "M04", argv, "reject", sorted(run(REF, argv)[1]), dd)

    # ---------- M01 (D5 mirror): manifest row position ----------
    capdir0 = ctx.d5_capture_dir()
    mname = ctx.spec["d5"]["manifest_name"]
    cname = ctx.spec["d5"]["capture_name"]
    rows0 = [l for l in (capdir0 / mname).read_text().splitlines() if l.strip()]
    caprow = next(l for l in rows0 if l.split()[-1].endswith(cname))
    others = [l for l in rows0 if l is not caprow and not l.split()[-1].endswith(cname)]
    for k in (1, 2, len(others) + 1):
        dd = ROOT / f"p-d5row{k}"
        dd.mkdir(exist_ok=True)
        cd = dd / "captures"
        if not cd.exists():
            shutil.copytree(capdir0, cd)
        placed = others[:k - 1] + [caprow] + others[k - 1:]
        (cd / mname).write_text("\n".join(placed) + "\n")
        line = dd / "erratum.md"
        line.write_text(ctx.d5_line() + "\n")
        argv = ["d5-line", "--file", str(line), "--capture-dir", str(cd)]
        probe(f"d5row-{k}of{len(others)+1}", "M01", argv, "accept", [], dd)

    # ---------- M07 (D5 mirror): markup inside the captured quote ----------
    quote = ctx.spec["d5"]["quote"]
    raw = (capdir0 / cname).read_text()
    hits = [(j, quote[j:j + 10]) for j in range(max(0, len(quote) - 10))
            if quote[j:j + 10] in raw]
    assert hits, "quote window not found verbatim in the capture"
    j, window = hits[0]
    at = raw.index(window)
    for mode in ("inside", "outside"):
        dd = ROOT / f"p-d5tag-{mode}"
        dd.mkdir(exist_ok=True)
        cd = dd / "captures"
        if not cd.exists():
            shutil.copytree(capdir0, cd)
        target = cd / cname
        if mode == "inside":
            new = raw[:at + 3] + "<b></b>" + raw[at + 3:]
        else:
            new = "<b></b>" + raw
        target.write_text(new)
        newdig = sha256(target)
        text = (cd / mname).read_text().splitlines()
        text = [f"{newdig}  {cname}" if l.split() and l.split()[-1].endswith(cname) else l for l in text]
        (cd / mname).write_text("\n".join(text) + "\n")
        line = dd / "erratum.md"
        line.write_text(ctx.d5_line() + "\n")
        argv = ["d5-line", "--file", str(line), "--capture-dir", str(cd)]
        probe(f"d5tag-{mode}", "M07", argv, "accept", [], dd)

    (ROOT / "ladder.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    ex = [r for r in results if r["declared"] in r["directions"]]
    same = [r for r in results if r["ref"] == r["mut"]]
    other = [r for r in results if r["ref"] != r["mut"] and r["declared"] not in r["directions"]]
    print(f"LADDER probes={len(results)} exhibit={len(ex)} same={len(same)} other={len(other)}")
    for r in other:
        print("  OTHER", r["probe"], r["mutant"], r["directions"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

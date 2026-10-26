#!/usr/bin/env python3
"""Differential fuzz over the mutant-relevant surface: does any frozen mutant ever flip out of its
declared direction?  Random perturbations of the genuine round-35 package (package family) and of the
D5 capture/manifest (d5-line family); every observed difference is classified by the frozen counter's
exhibits() for all four directions.

Usage: fuzz.py LANE [N_PKG] [N_D5]
"""
import hashlib
import importlib.util
import json
import os
import pathlib
import random
import re
import shutil
import sys

LANE = pathlib.Path(sys.argv[1]).resolve()
NPKG = int(sys.argv[2]) if len(sys.argv) > 2 else 40
ND5 = int(sys.argv[3]) if len(sys.argv) > 3 else 24
ROOT = pathlib.Path(os.environ.get("R39W", pathlib.Path(__file__).resolve().parent / "fuzz")).resolve()


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
MUT, CLAUSE, DIRECTION = {}, {}, {}
for mid, clause, direction, label, wit, old, new in c39.MUTANTS:
    mg = GDIR / f"{mid}.py"
    mg.write_text(GATE_SRC.replace(old, new, 1))
    MUT[mid], CLAUSE[mid], DIRECTION[mid] = mg, clause, direction

ENTRY = ctx.spec["entry"]
PINS = list(ctx.spec["frozen_instruments"])
LO, HI = ctx.spec["entry_rules"]["quote_words"]
rows_sorted = sorted(ctx.spec["rows"])
CAP0 = ctx.d5_capture_dir()
MAN, CAPNAME = ctx.spec["d5"]["manifest_name"], ctx.spec["d5"]["capture_name"]
QUOTE = ctx.spec["d5"]["quote"]


def classify(mid, ref, mut, expect, declared, argv):
    fx = {"fid": "fuzz", "expect": expect, "defects": declared, "argv": argv}
    if ref == mut or not c39.family_ok(CLAUSE[mid], argv):
        return [] if ref == mut else ["family-skip"]
    return [d for d in c39.DIRECTIONS if c39.exhibits(CLAUSE[mid], d, fx, ref, mut)]


def pkg_edit(rng, d):
    """One random perturbation of a genuine package; returns a label."""
    kinds = ["dup-source", "dup-source-stale", "pin", "words", "del-quote", "untracked", "capture-byte", "receipt"]
    kind = rng.choice(kinds)
    entry = d / pathlib.PurePosixPath(ENTRY)
    text = entry.read_text()
    if kind.startswith("dup-source"):
        sid = rng.choice(rows_sorted)
        gen = next(l for l in text.splitlines() if l.startswith(f"source: {sid}"))
        if kind.endswith("stale"):
            gen = re.sub(r"(https?://\S+)", r"\1-stale", gen, count=1)
        entry.write_text(text + "\n" + "\n".join([gen] * rng.randint(1, 3)) + "\n")
    elif kind == "pin":
        f = d / rng.choice(PINS)
        f.write_text(f.read_text() + "".join(rng.choice("#\n x") for _ in range(rng.randint(1, 8))))
    elif kind == "words":
        n = rng.randint(max(1, LO - 2), HI + 3)

        def fn(rows):
            out = []
            for i, row in enumerate(rows):
                m = r36.QUOTE_ROW.match(row)
                if m and i == 0:
                    cells = row.split("|")
                    t = " ".join(f"z{j}" for j in range(n))
                    out.append(f'| {cells[1].strip()} | “{t}” | `{m.group(2)}:{m.group(3)}` |')
                else:
                    out.append(row)
            return out

        entry.write_text(r36.rewrite_quotes(text, fn))
    elif kind == "del-quote":
        def fn(rows):
            return rows[1:] if len(rows) > 1 else rows
        entry.write_text(r36.rewrite_quotes(text, fn))
    elif kind == "untracked":
        (d / "plans" / f"fuzz-stray-{rng.randint(0, 999)}.py").write_text("# stray\n")
    elif kind == "capture-byte":
        caps = sorted((d / ctx.spec["capture_dir"]).iterdir())
        cap = rng.choice([c for c in caps if c.is_file() and c.name != "SHA256SUMS"]) if caps else None
        if cap is not None:
            cap.write_text(cap.read_text() + "\n<!-- fuzz -->\n")
    else:
        rec = d / ctx.spec["receipt"]
        if rec.is_file():
            rec.write_text(rec.read_text() + "x")
    return kind


def d5_edit(rng, d):
    """Random D5 perturbation (manifest permutation and/or a tag inside a random capture window)."""
    cd = d / "captures"
    shutil.copytree(CAP0, cd)
    kinds = ["permute", "tag-inside", "tag-outside", "digest-stale", "tag-many"]
    kind = rng.choice(kinds)
    cap = cd / CAPNAME
    raw = cap.read_text()
    if kind == "permute":
        rows = [l for l in (cd / MAN).read_text().splitlines() if l.strip()]
        rng.shuffle(rows)
        (cd / MAN).write_text("\n".join(rows) + "\n")
    elif kind == "digest-stale":
        rows = (cd / MAN).read_text().splitlines()
        rows = [("0" * 64 + "  " + CAPNAME) if l.split() and l.split()[-1].endswith(CAPNAME) else l for l in rows]
        (cd / MAN).write_text("\n".join(rows) + "\n")
    elif kind in ("tag-inside", "tag-many"):
        n = 1 if kind == "tag-inside" else 3
        new = raw
        for _ in range(n):
            at = rng.randrange(0, max(1, len(new) - 1))
            new = new[:at] + "<i></i>" + new[at:]
        cap.write_text(new)
        dig = sha256(cap)
        rows = (cd / MAN).read_text().splitlines()
        rows = [f"{dig}  {CAPNAME}" if l.split() and l.split()[-1].endswith(CAPNAME) else l for l in rows]
        (cd / MAN).write_text("\n".join(rows) + "\n")
    else:
        cap.write_text("<i></i>" + raw)
        dig = sha256(cap)
        rows = (cd / MAN).read_text().splitlines()
        rows = [f"{dig}  {CAPNAME}" if l.split() and l.split()[-1].endswith(CAPNAME) else l for l in rows]
        (cd / MAN).write_text("\n".join(rows) + "\n")
    line = d / "erratum.md"
    line.write_text(ctx.d5_line() + "\n")
    return kind, ["d5-line", "--file", str(line), "--capture-dir", str(cd)]


def main():
    rng = random.Random(3919)
    stats = {}
    bad = []
    for i in range(NPKG):
        d = ROOT / f"pkg{i:03d}"
        d.mkdir()
        ctx.genuine_package(d)
        kinds = [pkg_edit(rng, d) for _ in range(rng.randint(1, 2))]
        ctx.git_add(d)
        argv = ["package", "--require-clean-tree", "--root", str(d)]
        ref = c39.run_gate(REF, ctx.spec_path, argv)
        exp = {0: "accept", 1: "reject", 2: "error"}.get(ref[0], "error")
        decl = sorted(ref[1])
        for mid in ("M01", "M02", "M03", "M04", "M05", "M06"):
            mut = c39.run_gate(MUT[mid], ctx.spec_path, argv)
            hits = classify(mid, ref, mut, exp, decl, argv)
            stats.setdefault(mid, {}).setdefault("diffs", 0)
            if ref != mut:
                stats[mid]["diffs"] += 1
                for h in hits:
                    stats[mid][h] = stats[mid].get(h, 0) + 1
                if DIRECTION[mid] not in hits:
                    bad.append((mid, kinds, ref, mut, hits))
        stats.setdefault("pkg-variants", {})["n"] = i + 1
    for i in range(ND5):
        d = ROOT / f"d5_{i:03d}"
        d.mkdir()
        kind, argv = d5_edit(rng, d)
        ref = c39.run_gate(REF, ctx.spec_path, argv)
        for mid in ("M01", "M07"):
            mut = c39.run_gate(MUT[mid], ctx.spec_path, argv)
            hits = classify(mid, ref, mut, {0: "accept", 1: "reject", 2: "error"}.get(ref[0], "error"),
                            sorted(ref[1]), argv)
            if ref != mut:
                stats.setdefault(mid, {}).setdefault("diffs", 0)
                stats[mid]["diffs"] += 1
                for h in hits:
                    stats[mid][h] = stats[mid].get(h, 0) + 1
                if DIRECTION[mid] not in hits:
                    bad.append((mid, [kind], ref, mut, hits))
        stats.setdefault("d5-variants", {})["n"] = i + 1
    def clean(x):
        if isinstance(x, dict):
            return {str(k): clean(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [clean(v) for v in x]
        if isinstance(x, (set, frozenset)):
            return sorted(x)
        return x
    print("FUZZ", json.dumps(stats, sort_keys=True))
    print(f"OUT-OF-DIRECTION {len(bad)}")
    for b in bad[:12]:
        print("  ", clean(b))
    (ROOT / "fuzz.json").write_text(json.dumps(clean({"stats": stats, "out_of_direction": bad}), indent=1))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())

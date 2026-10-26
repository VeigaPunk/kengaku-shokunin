#!/usr/bin/env python3
"""N21 attack: is a SILENCE kill impossible and a MIRROR kill real?

Enumerates manifest shapes over the genuine capture + erratum line (the only two inputs N21 can change are
the manifest rows) and reports ref-vs-mutant D5 status, the subset relation, and each direction witness.
"""
import importlib.util, itertools, pathlib, re, shutil, subprocess, sys

S = pathlib.Path(sys.argv[1]).resolve()
LANE = S / "lane"
W = S / "attack" / "n21"
if W.exists():
    shutil.rmtree(W)
W.mkdir(parents=True)


def load(p, n):
    sp = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


c = load(LANE / "plans/round38_c1_verify.py", "k38")
r37 = load(LANE / c.R37_REL, "k37")
gate_src = (LANE / r37.GATE_REL).read_text()
r36 = r37.load_r36(LANE)
ctx = r37.Ctx(LANE, r36)
d5m = load(LANE / "plans/battery38/d5m.py", "d5m")
FX = [f for f in d5m.FIXTURES if f["fid"] == "d5m-n21-manifest-row-2"][0]
base = W / "base"
base.mkdir()
argv = list(FX["build"](ctx, base))

mut = gate_src.replace("for parts in (row.split() for row in sums.splitlines()))",
                       "for parts in (row.split() for row in sums.splitlines()[:1]))", 1)
assert mut != gate_src
(W / "ref.py").write_text(gate_src)
(W / "n21.py").write_text(mut)


def d5_of(gate, d, argv):
    a = [t.replace(str(base), str(d)) for t in argv]
    full = [sys.executable, str(gate), *a] + ([] if "--spec" in a else ["--spec", str(ctx.spec_path)])
    r = subprocess.run(full, capture_output=True, text=True)
    line = [l for l in r.stdout.splitlines() if l.startswith("D5 ")]
    return r.returncode, (line[0] if line else ""), r.stderr


def sha(p):
    import hashlib
    return hashlib.sha256(p.read_bytes()).hexdigest()


capdir = base / "captures"
capture = capdir / "geniac-s105-reopen.html"
digest = sha(capture)
# keep the builder's own manifest layout so "genuine" means byte-identical to what the accept fixture used
orig = (capdir / "quarantine-SHA256SUMS").read_text()
genuine_row = [l for l in orig.splitlines() if l.strip() and l.split()[0] == digest]
if not genuine_row:
    genuine_row = [l for l in orig.splitlines() if l.strip()]
genuine_row = genuine_row[-1]
decoy_row = "0" * 64 + "  geniac-s105-reopen.html"
wrongsuffix_row = digest + "  geniac-other.html"
blank = ""
junk = "not a manifest row"
rows = {"G": genuine_row, "D": decoy_row, "W": wrongsuffix_row, "B": blank, "J": junk}

print(f"genuine_row: {genuine_row!r}")
print(f"capture digest: {digest}")
print("shape      ref_rc ref_D5                 mut_rc mut_D5                 subset silence mirror")
silence_witness = mirror_witness = 0
violations = []
for n in range(0, 4):
    for combo in itertools.product(rows, repeat=n):
        shape = "".join(combo) or "-"
        d = W / "shapes" / shape.replace("-", "empty")
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(base, d, symlinks=True)
        text = "".join(rows[k] + "\n" for k in combo)
        (d / "captures" / "quarantine-SHA256SUMS").write_text(text)
        rrc, rline, _ = d5_of(W / "ref.py", d, argv)
        mrc, mline, merr = d5_of(W / "n21.py", d, argv)
        rbad = "DEFECT" in rline
        mbad = "DEFECT" in mline
        subset = (not rbad) or mbad  # mutant DEFECT => reference DEFECT (mutant stricter)
        sil = rbad and not mbad
        mir = (not rbad) and mbad
        silence_witness += sil
        mirror_witness += mir
        if not subset:
            violations.append(shape)
        if sil or mir or n < 2:
            print(f"{shape:10s} {rrc} {rline[:24]:24s} {mrc} {mline[:24]:24s} {subset} {sil} {mir}")
print(f"shapes={sum(len(list(itertools.product(rows, repeat=n))) for n in range(4))} "
      f"subset_violations={len(violations)} silence_witnesses={silence_witness} "
      f"mirror_witnesses={mirror_witness}")

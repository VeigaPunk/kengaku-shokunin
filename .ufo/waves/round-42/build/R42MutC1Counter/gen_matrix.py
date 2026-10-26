#!/usr/bin/env python3
"""Regenerate the R42MutC1Counter mutant matrix (counter variants + control base blocks).

Usage: python3 gen_matrix.py <scratch S> <lane clone>
Writes <S>/c/{pristine,attr,nomut,dir}.py, <S>/v/<MID>_<SETUP>.py, <S>/base/<SETUP>.block, <S>/mutants.json.
Setups: N=clean clone, W=witness-as-battery mirror, A=attribution-patched counter, M=no-mutants-patched
counter, T=tool-edited mirror, H=hostile-escape mirror, D=direction-mislabel-patched counter.
"""
import hashlib, json, pathlib, sys

S = pathlib.Path(sys.argv[1]); LANE = pathlib.Path(sys.argv[2])
CL = LANE / ".ufo/waves/round-42/claims"
C = S / "c"; V = S / "v"; B = S / "base"
for p in (C, V, B): p.mkdir(parents=True, exist_ok=True)

pristine = (LANE / "plans/round42_c1_verify.py").read_text()
assert hashlib.sha256(pristine.encode()).hexdigest() == \
    "559fca0c9254e4c09f2406f75ba9559e370012ccb1ecdc91c9a944abbe0c6649", "pristine counter digest mismatch"

attr = pristine.replace(
    '            span = set(range(start, start + new.count("\\n") + 1))',
    '            span = {1}  # CONTROL: a span no line event can reach', 1)
i = pristine.index("MUTANTS = ["); j = pristine.index("\n]\n", i)
nomut = pristine[:i] + "MUTANTS = []" + pristine[j+3:]
dirm = pristine.replace(
    "('XO5', 'order', '-', 'rc-mirror', 'direct',", "('XO5', 'order', '-', 'rc-silence', 'direct',", 1).replace(
    "('XO6', 'order', '-', 'rc-mirror', 'indirect',", "('XO6', 'order', '-', 'rc-silence', 'indirect',", 1)
for name, text in (("pristine", pristine), ("attr", attr), ("nomut", nomut), ("dir", dirm)):
    (C / f"{name}.py").write_text(text)

G = [
 ("CM01", '    return want == a and ref[0] == a and mut[0] == b',
          '    return ref[0] == a and mut[0] == b'),
 ("CM02", '    return fx["expect"] == "reject" and ref[0] == 1 and mut[0] == 0',
          '    return ref[0] == 1 and mut[0] == 0'),
 ("CM03", '    return fx["expect"] == "accept" and ref[0] == 0 and mut[0] == 1',
          '    return ref[0] == 0 and mut[0] == 1'),
 ("CM04", '    return fx["expect"] == "error" and ref[0] == 2 and mut[0] in (0, 1)',
          '    return fx["expect"] == "error" and ref[0] == 2 and mut[0] in (0, 1, 2)'),
 ("CM05", '    return cls in ref[1] and cls in set(fx["defects"]) and cls not in mut[1]  # silence',
          '    return cls in ref[1] and cls not in mut[1]  # silence'),
 ("CM06", '        return ".." not in tok', '        return True'),
 ("CM07", '        if not base.resolve().is_relative_to(d):\n            return False',
          '        if not base.resolve().is_relative_to(d):\n            return True'),
 ("CM08", '        floors_ok = (TOTAL >= 1 and all(FLOORS.get(t, 0) >= 1 for t in TOOLS) and sum(FLOORS.values()) == TOTAL',
          '        floors_ok = (TOTAL >= 1 and all(FLOORS.get(t, 0) >= 1 for t in TOOLS)'),
 ("CM08b",'                     and all(per_tool.get(t, [0, 0]) == [FLOORS[t], FLOORS[t]] for t in TOOLS))',
          '                     and True)'),
 ("CM09", '    good = (not mism and not after and len(MUTANTS) == TOTAL and floors_ok and wrong == 0 and tampered == 0',
          '    good = (not mism and not after and floors_ok and wrong == 0 and tampered == 0'),
 ("CM10", '                if (t_rc, t_cls) == res and span & t_lines:',
          '                if (t_rc, t_cls) == res:'),
 ("CM11", '                if (t_rc, t_cls) == res and span & t_lines:',
          '                if span & t_lines:'),
 ("CM12", '                unattributed += 1', '                unattributed += 0'),
 ("CM13", '                content = file_sha256(p)', '                content = ""'),
 ("CM14", '        hits = [t for t in SIDECHANNEL if t in text]', '        hits = []'),
 ("CM15", '        if not isinstance(argv, list) or not all(type(t) is str for t in argv):', '        if False:'),
 ("CM16", '                  and isinstance(argv, list) and all(isinstance(t, str) and path_ok(t, d) for t in argv)',
          '                  and isinstance(argv, list) and all(isinstance(t, str) for t in argv)'),
 ("CM17", '    mism = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]', '    mism = []'),
 ("CM18", '    after = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]', '    after = []'),
 ("CM19a",'                if res != ref[fx["fid"]]:', '                if False:'),
 ("CM19b",'                if res != ref[fx["fid"]]:', '                if True:'),
 ("CM20", '    dev = a.battery_dir is not None or a.only is not None', '    dev = False'),
]
bases = {"N": pristine, "W": pristine, "A": attr, "M": nomut, "T": pristine, "H": pristine, "D": dirm}
meta = {}
for mid, old, new in G:
    assert pristine.count(old) == 1, (mid, pristine.count(old))
    meta[mid] = {"old": old, "new": new, "sha": {}}
    for setup, base in bases.items():
        assert base.count(old) == 1, (mid, setup, base.count(old))
        vtxt = base.replace(old, new, 1)
        compile(vtxt, f"{mid}_{setup}", "exec")
        (V / f"{mid}_{setup}.py").write_text(vtxt)
        meta[mid]["sha"][setup] = hashlib.sha256(vtxt.encode()).hexdigest()[:16]

controls = {"N": "control-c1-nothing.txt", "W": "control-c1-witness-as-battery.txt",
            "A": "control-c1-attribution.txt", "M": "control-c1-no-mutants.txt",
            "T": "control-c1-tool-edited.txt", "H": "control-c1-hostile-escape.txt",
            "D": "control-c1-direction-mislabel.txt"}
for setup, fname in controls.items():
    lines = [l for l in (CL / fname).read_text().splitlines() if not l.startswith("ENVELOPE")]
    (B / f"{setup}.block").write_text("\n".join(lines) + "\n")
    meta.setdefault("control_sha", {})[setup] = hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()[:16]

(S / "mutants.json").write_text(json.dumps(meta, indent=1))
print(f"gen_matrix: {len(G)} mutants x {len(bases)} setups -> {len(list(V.glob('*.py')))} variants; bases ok")

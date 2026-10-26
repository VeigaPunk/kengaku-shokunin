#!/usr/bin/env python3
"""Round-38 C1 counter (calibration): the gate behaviours the lane advertises that the round-37 battery does
not demonstrate — the mutants the round-37 freeze excluded or wave 2 found surviving — killed only by an
ATTRIBUTED kill.

Frozen predicate (same sentence in plans/round-38-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round38_c1_verify.py --lane .` prints `PINS total=14 mismatched=0`, then
  `BATTERY fixtures=<n> wrong=0 renamed_disagree=0 sidechannel=0`, then
  `MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0`, then `PREDICATE C1 pass`, exit 0,
  measured on a clean clone of the landing tip.

Self-assessment under test: `plans/pkg_gate.py`'s docstring, `corpus/QUALITY.md` Q24/Q27 and the SCORECARD
capability rows `package-gate` / `gate-mutation-harness` advertise behaviours (every quote verbatim on its
cited line; a receipt a fresh run does not reproduce is a defect; an unexpected crash never maps onto 0 or 1;
the genuine package is accepted ...). Each mutant below is one byte-level `old -> new` replacement of the
frozen gate that breaks one advertised behaviour (the `adv` cell names the sentence). A survivor is an
advertised-but-undemonstrated behaviour: the mismatch count between what the lane says its gate does and
what its battery shows.

Sources of the list: the 13 non-equivalent survivors of the round-37 wave-2 extra-mutant seats
(`.ufo/waves/round-37/falsify/F37XMut*.md`), one diagnostic survivor (F37XMutP7 D1, generalised to "first
row skipped"), and the round-37 freeze's excluded / unexecuted shapes measured by R37PlanNext §3.2 (B1 empty
pins, B2 blank manifest line, B5 P10 pass side, B6 clause-crash handler, B7 root-not-a-directory, B8 crash
exit). Excluded, with reason: F37XMutP4 X3, F37XMutP5 X4, F37XMutP8 S1 (observationally equivalent at
(exit code, DEFECT set) granularity, argued in their reports); B3 `import Bio` arm and B4 `OSError` arm
(reachable only through the gate's interpreter/environment, which the counter fixes); B7's spec-not-found
arm (equivalent: its silence still exits 2 via the crash handler).

Kill rule (ATTRIBUTED — the round-37 counter's "any result differs" rule was shown gameable,
`.ufo/waves/round-37/build/R37CritC1Battery.md`): mutant N is killed by fixture f iff the reference and the
mutant both exit 0/1 (or, for MAIN, the reference exits 2) and
  * silence (`dir=silence`, clause C): the reference prints C `DEFECT`, f declares C in its `defects`, the
    mutant run does not print C `DEFECT`;
  * mirror (`dir=mirror`, clause C): the reference prints C `ok`, the mutant run prints C `DEFECT`;
  * RUN (the run_checks crash handler): some clause f declares and the reference prints `DEFECT` is not
    `DEFECT` in the mutant run;
  * MAIN (main's exits): f declares `expect=error`, the reference exits 2, the mutant exits 0 or 1;
and f's subcommand matches the clause family (P*/RUN: package; D4: d4-line; D5: d5-line; MAIN: any).

Battery = the round-36 battery + plans/battery37/*.py (both read through the frozen round-37 counter, pinned
below) + plans/battery38/*.py. A battery38 module exports FIXTURES = [{"fid", "expect": accept|reject|error,
"defects": [exact clause ids printing DEFECT; [] for accept/error], "build": build}]; build(ctx, d) fills the
EMPTY directory d and returns the gate argv tail. Unlike battery37 a battery38 fixture MAY pass its own
`--spec <file inside d>` (shapes B1/B6/B8 need a spec the counter does not own); otherwise the counter
appends the frozen round-35 spec. `sidechannel` counts battery38 module sources that contain any of
`/proc`, `ppid`, `cmdline`, `psutil`, `environ` (a fixture that inspects which gate copy runs is the
round-37 hostile battery's mechanism); a heuristic, not a proof.

Pins (`PINS total=14`): the gate, the round-37 counter, the round-36 counter, the round-35 spec, the nine
battery37 modules and the round-37 attribution audit — every input of this counter that exists at the freeze.

  --battery r37       round-36 + battery37 only (the do-nothing control)
  --battery-dir DIR   load battery38 modules from DIR (development; predicate n/a)
  --only N01,N02      restrict mutants (development; predicate n/a)
  --work DIR          scratch parent (default: $TMPDIR via tempfile)
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pathlib
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile

R37_REL = "plans/round37_c1_verify.py"
BATTERY38_REL = "plans/battery38"
PINS = {
    "plans/pkg_gate.py": "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41",
    "plans/round37_c1_verify.py": "dbc9f7199381f5bbd708458bedc45cd199cee38a6440a2968a886229173413cc",
    "plans/round36_c1_verify.py": "d7c3687c09ed4c8a09a9d7c63efa9232c2b1aff8ffb229fb8a0505578317df73",
    "plans/pkg-spec-r35.json": "e085b43505c9848c8d19eb52c52fec1a3282dac3c5b436f59320e95e5c299fc4",
    "plans/round37_c1_attribution.py": "7064cf1a2ef8e6ef26224b17d7da13a6b9aa6630fd83c13110d9474bbd7db147",
    "plans/battery37/d4.py": "6c08d5391f4c9f461bb0b07d9de720bf0cc167a3a558c86f6fef5d0dad171c64",
    "plans/battery37/d5.py": "c3579f175cfe6b2fdba16a80847f88d04831e5b561df4db4af5898cc9aad75ee",
    "plans/battery37/p23.py": "518340e4d6403b396abd6d871722f6cfa76001a77c5b033bd5702a0bbd399990",
    "plans/battery37/p4.py": "3e506c65098a84d154a37e411f65b32c1bed9439b10e0ea2d8dcff8fa8e7fccf",
    "plans/battery37/p5.py": "a9d721ac23d097354630a8ac069a0b00d3a8d447f795534db4711e8b74c02e72",
    "plans/battery37/p6.py": "b81746fd6342227917a5c4a32a00235babec4860a07fe7811dcd7f171dc55e46",
    "plans/battery37/p7.py": "5245533a336761f7a161395c77b0b9b2ed23609c6426edcfa762135515ae0f39",
    "plans/battery37/p8.py": "cfbe5cf93d46ee30f90e4603367c39bf793aad7f205367182388bd224a7e76ff",
    "plans/battery37/p910.py": "6d2779adcca9ed08afa83bc7e2575a69d76da19a27eb27b640b561005dab20bb",
}
CLAUSE_LINE = re.compile(r"^(P\d+|D4|D5) (ok|DEFECT) ")
SIDECHANNEL = ("/proc", "ppid", "cmdline", "psutil", "environ")
FAMILY = {"D4": "d4-line", "D5": "d5-line"}

# (id, clause, dir, advertised behaviour [source], old, new) — frozen at the gate digest above.
MUTANTS = [
    ("N01", "P1", "silence", "an empty frozen_instruments pin set is not an accept [capability row: 'against a spec of pinned digests'; R37PlanNext B1]",
     'return bool(pins) and not bad, f"pinned=', 'return not bad, f"pinned='),
    ("N02", "P3", "mirror", "a package with exactly min_distinct_locations quote lines is accepted [Q24 'the genuine package must be accepted'; F37XMutP23 X2]",
     'len(locs) >= rules["min_distinct_locations"]', 'len(locs) > rules["min_distinct_locations"]'),
    ("N03", "P4", "silence", "every quote is checked, not only the first [docstring 'a quote not verbatim on its cited line'; F37XMutP4 X2]",
     "    for q in p.quotes:\n        lines = p.capture(q.capture)", "    for q in p.quotes[:1]:\n        lines = p.capture(q.capture)"),
    ("N04", "P4", "silence", "verbatim on the CITED lines, not anywhere in the capture [capability row 'verbatim on its cited capture line'; F37XMutP4 X4]",
     'elif q.text not in "\\n".join(lines[q.start - 1:q.end]):', 'elif q.text not in "\\n".join(lines):'),
    ("N05", "P4", "silence", "verbatim is case-sensitive [docstring 'a quote not verbatim'; F37XMutP4 X5]",
     'elif q.text not in "\\n".join(lines[q.start - 1:q.end]):',
     'elif q.text.lower() not in "\\n".join(lines[q.start - 1:q.end]).lower():'),
    ("N06", "P4", "silence", "a cited range past the capture's last line is a defect [F37XMutP4 X6]",
     "q.end > len(lines):", "q.end > len(lines) + 1:"),
    ("N07", "P5", "silence", "every registry row's capture is pinned in the manifest, not only the first [F37XMutP5 X1]",
     '    for sid, row in p.spec["rows"].items():\n        name = row["capture"]',
     '    for sid, row in list(p.spec["rows"].items())[:1]:\n        name = row["capture"]'),
    ("N08", "P5", "mirror", "a blank manifest line is tolerated, not an unparsed line [Q24 genuine accepted; R37PlanNext B2]",
     "        if not line.strip():\n            continue\n        m = MANIFEST_LINE",
     "        if False:\n            continue\n        m = MANIFEST_LINE"),
    ("N09", "P6", "silence", "a teaches cell below min_teaches_words is a defect [capability row 'teaches cells carry >=8 distinct words'; F37XMutP6 X1]",
     'if len(cells[6].split()) < rules["min_teaches_words"]:', 'if len(cells[6].split()) < rules["min_teaches_words"] - 1:'),
    ("N10", "P6", "silence", "the row URL is the pinned raw URL including its scheme [F37XMutP6 X4]",
     'url.group(0) != p.spec["raw_base"] + row["upstream"]',
     'url.group(0).split("://", 1)[-1] != (p.spec["raw_base"] + row["upstream"]).split("://", 1)[-1]'),
    ("N11", "P7", "silence", "a recheck line must carry a value [F37XMutP7 X4]",
     'if not re.search(r"^recheck:\\s*\\S", p.entry, re.M):', 'if not re.search(r"^recheck:", p.entry, re.M):'),
    ("N12", "P7", "silence", "the first registry row's source line is checked too [F37XMutP7 D1]",
     '    for sid, row in p.spec["rows"].items():\n        if prov.get(sid)',
     '    for sid, row in list(p.spec["rows"].items())[1:]:\n        if prov.get(sid)'),
    ("N13", "P10", "silence", "a receipt differing only in trailing whitespace is not reproduced [docstring 'a receipt a fresh run does not reproduce'; F37XMutP910 L1]",
     "    if r.stdout != want:\n", "    if r.stdout.rstrip() != want.rstrip():\n"),
    ("N14", "P10", "silence", "the receipt is compared beyond its first line [capability row '--rerun byte-compares the receipt'; F37XMutP910 L3]",
     "    if r.stdout != want:\n", "    if r.stdout.splitlines()[:1] != want.splitlines()[:1]:\n"),
    ("N15", "P10", "mirror", "a byte-equal fresh run passes P10 [Q24 genuine accepted; F37XMutP910 L2; R37PlanNext B5]",
     'return True, f"probe_rerun=byte-equal', 'return False, f"probe_rerun=byte-equal'),
    ("N16", "RUN", "silence", "a clause that cannot run is a defect, never a pass [gate run_checks comment; R37PlanNext B6]",
     "ok, note = False, f\"clause error", "ok, note = True, f\"clause error"),
    ("N17", "MAIN", "silence", "a --root that is not a directory is a setup error, exit 2 [docstring 'exit ... 2 = usage/setup'; R37PlanNext B7]",
     "            if not args.root.is_dir():", "            if False:"),
    ("N18", "MAIN", "silence", "an unexpected crash never maps onto 0 or 1 [docstring; R37PlanNext B8]",
     '        print(f"setup: {type(e).__name__}: {e}", file=sys.stderr)\n        return 2',
     '        print(f"setup: {type(e).__name__}: {e}", file=sys.stderr)\n        return 0'),
    ("N19", "D4", "silence", "every directional pattern is checked, the last included [F37XMutD4 X3]",
     'enumerate(spec["d4"]["patterns"], 1)', 'enumerate(spec["d4"]["patterns"][:-1], 1)'),
    ("N20", "D4", "silence", "directional patterns match case-sensitively [F37XMutD4 X4]",
     "if not re.search(pat, lines[0])]", "if not re.search(pat, lines[0], re.IGNORECASE)]"),
    ("N21", "D5", "mirror", "the capture digest is looked up in every manifest row, not only the first [F37XMutD5 X3]",
     "for parts in (row.split() for row in sums.splitlines()))", "for parts in (row.split() for row in sums.splitlines()[:1]))"),
    ("N22", "D5", "silence", "the whole quote must be present, not a 20-character prefix [F37XMutD5 X4]",
     'if re.sub(r"\\s+", "", d5["quote"]) not in flat:', 'if re.sub(r"\\s+", "", d5["quote"])[:20] not in flat:'),
]
TOTAL = 22


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def battery38_fixtures(bdir):
    out, side = [], 0
    if not bdir.is_dir():
        return out, side
    for f in sorted(bdir.glob("*.py")):
        text = f.read_text()
        hits = [t for t in SIDECHANNEL if t in text]
        if hits:
            side += 1
            print(f"SIDECHANNEL {f.name} tokens={','.join(hits)}")
        mod = load(f, f"kengaku_b38_{f.stem}")
        out.extend({**fx, "r36": False, "b38": True} for fx in getattr(mod, "FIXTURES", []))
    return out, side


def run_gate(gate, default_spec, argv):
    """(rc, DEFECT set, ok set); a fixture argv that carries --spec keeps it, else the frozen spec is appended."""
    full = [sys.executable, str(gate), *argv] + ([] if "--spec" in argv else ["--spec", str(default_spec)])
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return ("timeout", frozenset(), frozenset())
    bad, ok = set(), set()
    for m in map(CLAUSE_LINE.match, r.stdout.splitlines()):
        if m:
            (bad if m.group(2) == "DEFECT" else ok).add(m.group(1))
    return (r.returncode, frozenset(bad), frozenset(ok))


def attributed(clause, direction, fx, argv, ref, mut):
    fam = FAMILY.get(clause, "package")
    if clause != "MAIN" and argv[0] != fam:
        return False
    if clause == "MAIN":
        return fx.get("expect") == "error" and ref[0] == 2 and mut[0] in (0, 1)
    if ref[0] not in (0, 1) or mut[0] not in (0, 1):
        return False
    declared = set(fx["defects"]) if fx.get("defects") is not None else set(ref[1])
    if clause == "RUN":
        return any(c in ref[1] and c not in mut[1] for c in declared)
    if direction == "silence":
        return clause in ref[1] and clause in declared and clause not in mut[1]
    return clause in ref[2] and clause in mut[1]  # mirror


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--battery", choices=("full", "r37"), default="full")
    ap.add_argument("--battery-dir", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    dev = a.battery_dir is not None or a.only is not None or a.battery != "full"
    mism = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
    print(f"PINS total={len(PINS)} mismatched={len(mism)}" + (f" first={mism[0]}" if mism else ""))
    r37 = load(lane / R37_REL, "kengaku_r37_c1")
    gate_src = (lane / r37.GATE_REL).read_text() if (lane / r37.GATE_REL).is_file() else ""
    gate_ok = "plans/pkg_gate.py" not in mism
    r36 = r37.load_r36(lane)
    ctx = r37.Ctx(lane, r36)
    fixtures = r37.r36_fixtures(r36) + r37.battery37_fixtures(lane / r37.BATTERY_REL)
    side = 0
    if a.battery == "full":
        bdir = pathlib.Path(a.battery_dir).resolve() if a.battery_dir else lane / BATTERY38_REL
        more, side = battery38_fixtures(bdir)
        fixtures += more
    root = pathlib.Path(tempfile.mkdtemp(prefix="k38-c1-", dir=a.work))
    try:
        ids = [f["fid"] for f in fixtures]
        if len(set(ids)) != len(ids):
            print("SETUP duplicate fixture id", file=sys.stderr)
            return 2
        built, wrong = [], 0
        for i, fx in enumerate(fixtures):
            d = root / "fx" / f"f{i:03d}"
            d.mkdir(parents=True)
            argv = list(fx["build"](ctx, d))
            ok_argv = bool(argv) and argv[0] in ("package", "d4-line", "d5-line")
            if "--spec" in argv:
                k = argv.index("--spec")
                ok_argv = ok_argv and fx.get("b38", False) and k + 1 < len(argv) \
                    and pathlib.Path(argv[k + 1]).resolve().is_relative_to(d.resolve())
            if not ok_argv:
                print(f"SETUP fixture {fx['fid']} returned a forbidden argv", file=sys.stderr)
                return 2
            built.append((fx, d, argv))
        gdir = root / "gates"
        gdir.mkdir()
        ref_gate = gdir / "ref.py"
        ref_gate.write_text(gate_src)
        ref = []
        for fx, d, argv in built:
            res = run_gate(ref_gate, ctx.spec_path, argv)
            ref.append(res)
            exp = fx.get("expect")
            want_rc = {"accept": 0, "reject": 1, "error": 2}.get(exp)
            declared = fx.get("defects")
            if not fx.get("r36") and (declared is None or want_rc is None):
                ok = False
            else:
                ok = res[0] == want_rc and (declared is None or res[1] == frozenset(declared))
            if exp in ("accept", "error"):
                ok = ok and not res[1]
            wrong += not ok
            print(f"FIXTURE {fx['fid']} expect={exp} declared={','.join(sorted(declared)) if declared else '-'}"
                  f" observed_rc={res[0]} observed_defects={','.join(sorted(res[1])) or '-'} {'ok' if ok else 'WRONG'}")
        ren_root = root / "renamed"
        ren_root.mkdir()
        disagree = 0
        for i, (fx, d, argv) in enumerate(built):
            nd = ren_root / f"x{(len(built) - i) * 7919 % 100003:05d}q"
            shutil.copytree(d, nd, symlinks=True)
            nargv = [t.replace(str(d), str(nd)) for t in argv]
            if run_gate(ref_gate, ctx.spec_path, nargv)[:2] != ref[i][:2]:
                disagree += 1
                print(f"RENAMED {fx['fid']} DISAGREES")
        print(f"BATTERY fixtures={len(built)} wrong={wrong} renamed_disagree={disagree} sidechannel={side}")
        null_gate = gdir / "null.py"
        null_gate.write_text(gate_src)
        null_detected = sum(1 for j, (fx, d, argv) in enumerate(built)
                            if run_gate(null_gate, ctx.spec_path, argv) != ref[j])
        only = set(a.only.split(",")) if a.only else None
        killed = survived = invalid = 0
        for mid, clause, direction, label, old, new in MUTANTS:
            if only and mid not in only:
                continue
            if not gate_ok or gate_src.count(old) != 1:
                invalid += 1
                print(f"MUTANT {mid} {clause} {direction} invalid -- {label}")
                continue
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            try:
                py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
            except py_compile.PyCompileError:
                invalid += 1
                print(f"MUTANT {mid} {clause} {direction} invalid(compile) -- {label}")
                continue
            digest = sha256(mg)
            by = None
            for j, (fx, d, argv) in enumerate(built):
                fam = FAMILY.get(clause, "package")
                if clause != "MAIN" and argv[0] != fam:
                    continue
                mut = run_gate(mg, ctx.spec_path, argv)
                if attributed(clause, direction, fx, argv, ref[j], mut):
                    by = fx["fid"]
                    break
            if sha256(mg) != digest:
                invalid += 1
                print(f"MUTANT {mid} {clause} {direction} invalid(mutant file changed during the run) -- {label}")
                continue
            if by:
                killed += 1
                print(f"MUTANT {mid} {clause} {direction} killed by={by} -- {label}")
            else:
                survived += 1
                print(f"MUTANT {mid} {clause} {direction} SURVIVED -- {label}")
        total = len(MUTANTS) if not only else len([m for m in MUTANTS if m[0] in only])
        print(f"MUTANTS total={total} killed={killed} survived={survived} invalid={invalid} null_detected={null_detected}")
        if dev:
            print("PREDICATE C1 n/a (non-default battery or mutant subset)")
            return 0 if (wrong == 0 and disagree == 0 and side == 0 and survived == 0 and invalid == 0
                         and null_detected == 0) else 1
        good = (not mism and len(MUTANTS) == TOTAL and wrong == 0 and disagree == 0 and side == 0
                and killed == TOTAL and survived == 0 and invalid == 0 and null_detected == 0)
        print(f"PREDICATE C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

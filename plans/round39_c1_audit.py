#!/usr/bin/env python3
"""Round-39 C1 AUDIT (post-hoc, NOT the frozen rule): `plans/round39_c1_verify.py` re-run with the four soundness
repairs wave-1 critic R39CritC1Counter asked for (.ufo/waves/round-39/build/R39CritC1Counter.md §2-§5), so a landed
battery can be shown not to depend on the holes the frozen counter leaves open:
  A1  every kill is re-checked: the reference gate is re-run on the killing fixture AFTER the mutant run and must
      reproduce its first result, and the mutant re-run must reproduce the kill (a fixture whose input changes
      between phases is `invalid(nondeterministic fixture)`, not a kill);
  A3  the battery37 and battery38 directories must hold exactly the pinned module names (an added file is a pin
      mismatch, and it is never imported);
  A4  every pin is re-hashed after the mutant loop (`PINS final ...`);
  A5  the fixture directory is the one the parent created, never the child's reported path; a package argv's
      `--root` must lie inside it; the child's JSON line must carry a per-run nonce.
The predicate below keeps the frozen counter's numbers; the audit adds `AUDIT C1 clean|dirty`. Everything else is
the frozen counter's text, kept for reference:

Round-39 C1 counter (calibration): the gate behaviours the lane advertises that its batteries still do not
demonstrate after round 38 — the round-38 freeze's one mislabelled mutant (N21) carried with its reachable
direction, and the non-equivalent survivors round-38 wave 2 found — killed only by an ATTRIBUTED kill, with
every battery38/battery39 module executed OUT OF PROCESS.

Frozen predicate (same sentence in plans/round-39-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round39_c1_verify.py --lane .` prints `PINS total=26 mismatched=0`, then
  `BATTERY fixtures=<n> wrong=0 renamed_disagree=0 sidechannel=0`, then
  `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, then `PREDICATE C1 pass`, exit 0,
  measured on a clean clone of the landing tip.

Self-assessment under test: `plans/pkg_gate.py`'s docstring, `corpus/QUALITY.md` Q24/Q27 and the SCORECARD
capability row `package-gate` (`SCORECARD.md:564`). Each mutant is one byte-level `old -> new` replacement of
the frozen gate; its `adv` cell names the advertising sentence and says when the sentence covers the
behaviour only indirectly. A survivor is an advertised-but-undemonstrated behaviour.

Direction (QUALITY Q29): every mutant's direction is declared here AND has a pre-freeze witness on record —
a committed run in which the reference and the mutant differ in exactly the declared direction on some input
(the `witness` cell). A witness is not a battery fixture: the counter never reads it.
  silence     the reference prints clause C `DEFECT`, the fixture declares C, the mutant does not print C `DEFECT`
              (the mutant is LAXER on C)
  mirror      the reference prints C `ok`, the mutant prints C `DEFECT` (the mutant is STRICTER on C)
  rc-silence  the fixture declares `expect=reject` with a non-empty `defects`, the reference exits 1, the
              mutant exits 0 (LAXER exit code; round-38 wave 2 F38XMutRerunMain finding 2: the round-38 rule
              could not see an exit-code flip with an unchanged DEFECT set)
  rc-mirror   the fixture declares `expect=accept`, the reference exits 0, the mutant exits 1 (STRICTER exit code)
  error       (MAIN, round-38 rule, unused by this list) the fixture declares `expect=error`, the reference
              exits 2, the mutant exits 0 or 1
Kill rule: mutant M is killed by fixture f iff f's subcommand matches M's clause family (P*/RUN: package;
D4: d4-line; D5: d5-line; MAIN: any) and the pair (reference result, mutant result) on f satisfies M's
declared direction; for silence/mirror both runs must exit 0/1. A survivor prints the directions it did
exhibit on any fixture (`exhibits=`), so a mislabelled direction is visible in the receipt (Q29).

Battery = the round-36 battery + plans/battery37/*.py (read in-process through the frozen round-37 counter;
both pinned) + plans/battery38/*.py (pinned) + plans/battery39/*.py. battery38/battery39 modules follow the
battery38 contract — FIXTURES = [{"fid", "expect": accept|reject|error, "defects": [...], "build": build}],
build(ctx, d) fills the EMPTY dir d and returns the gate argv tail, a `--spec` it passes must lie inside d —
but each module is imported and built in a CHILD process (`--build-module`, this file), which hands back only
JSON (fid, expect, defects, argv). A module therefore cannot patch this counter's `run_gate` (round-38
`R38CritClaims` §2: an in-process junk module reached `killed=20`). Gate copies are written only after every
child has exited and are digest-checked after every run. `sidechannel` counts battery38/battery39 sources
carrying `/proc`, `ppid`, `cmdline`, `psutil` or `environ` — a heuristic; non-author code review stays in
admission.

Pins (`PINS total=26`): the gate, the round-37 and round-36 counters, the round-35 spec, the round-37
attribution audit, the nine battery37 modules and the twelve battery38 modules.

  --battery r38       round-36 + battery37 + battery38 only (the do-nothing control)
  --battery-dir DIR   load battery39 modules from DIR (development; predicate n/a)
  --only M01,M02      restrict mutants (development; predicate n/a)
  --work DIR          scratch parent (default: $TMPDIR via tempfile)
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import py_compile
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

R37_REL = "plans/round37_c1_verify.py"
BATTERY38_REL = "plans/battery38"
BATTERY39_REL = "plans/battery39"
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
    "plans/battery38/b1run.py": "95a094976b9c5b79be10d06651419806be75555b09e9b4b03118a43a10b15e8d",
    "plans/battery38/d4m.py": "4fd34339ab32627b65b2fd7ff11f0d1b99c45b02598c8591468b2badbc0d4488",
    "plans/battery38/d5m.py": "5af18f40f7543fd60c8f4926b8f73553804fd428e91d3700a40f351d3d4ddbd7",
    "plans/battery38/mainx.py": "e066e19d499c04e12c37275fb45738306cb4e7c38b4af616140cadc5887e3561",
    "plans/battery38/p10a.py": "e65f7a542ee08d00bce3d67cedc03cd87197ebe7f86fdc3017745b0cb4f5cc2a",
    "plans/battery38/p10b.py": "cb5df72a5c2faf44916b0b23d5ffe2ac64398515d1bb3080d838c7d7ab90c004",
    "plans/battery38/p3m.py": "851d4e82829b9b8fa688180bcba6295e531267d58b05e32af0b088d6d95c57d8",
    "plans/battery38/p4a.py": "60f34aa2ed1fac71be6d8e4af2dfb8c2a09e4322578f643517cdbad0f1fbffbf",
    "plans/battery38/p4b.py": "31d591f6a790ab8d429750791de50f88964a608f2504e8d1fb0e849ba2edd332",
    "plans/battery38/p5m.py": "db9627e8cf3834202057e575416dc454c6c42b9ec9d136bf287ceadb7940803b",
    "plans/battery38/p6m.py": "3a42982e54ddcf9af47bbad1df05a55987c6cfbcb697612553373c888c8b2e97",
    "plans/battery38/p7m.py": "5e6f943f15ec65b278649bbbd25fb975cd6339603c923f9b893c6f2db241dbf5",
}
CLAUSE_LINE = re.compile(r"^(P\d+|D4|D5) (ok|DEFECT) ")
SIDECHANNEL = ("/proc", "ppid", "cmdline", "psutil", "environ")
FAMILY = {"D4": "d4-line", "D5": "d5-line"}
DIRECTIONS = ("silence", "mirror", "rc-silence", "rc-mirror")
F38 = ".ufo/waves/round-38/falsify"

# (id, clause, dir, advertised behaviour [source], witness [pre-freeze, committed], old, new) — frozen at the
# gate digest above.
MUTANTS = [
    ("M01", "D5", "mirror",
     "a D5 capture whose digest sits on a non-first manifest row is accepted [Q24 'the genuine package must be "
     "accepted' (indirect: D5 is a correction line, not the package); round-38 N21 relabelled from its "
     "unreachable 'silence']",
     "plans/battery38/d5m.py fixture d5m-n21-manifest-row-2 (reference D5 ok, mutant D5 DEFECT); "
     ".ufo/waves/round-38/integrate/n21-mirror-diagnostic.txt",
     "for parts in (row.split() for row in sums.splitlines()))",
     "for parts in (row.split() for row in sums.splitlines()[:1]))"),
    ("M02", "P1", "silence",
     "every frozen instrument is checked against its pin, not only the first [package-gate row 'against a spec "
     "of pinned digests ... a stub probe dies on its digest pin']",
     f"{F38}/F38XMutP/witness-run.txt W-X01 (ref P1,P9 -> mutant P9)",
     "bad = [rel for rel, dig in pins.items() if sha256(p.root / rel) != dig]",
     "bad = [rel for rel, dig in list(pins.items())[:1] if sha256(p.root / rel) != dig]"),
    ("M03", "P3", "silence",
     "a quote one word above the spec's upper word bound is a defect [gate docstring 'quote bounds ... come "
     "from --spec']",
     f"{F38}/F38XMutP/witness-run.txt W-X05 (ref P3,P4,P9 -> mutant P4,P9)",
     "short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]",
     "short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi + 1]"),
    ("M04", "P7", "silence",
     "a registry row carries exactly one source line, the pinned URL [package-gate row 'SOURCES rows ... "
     "against a spec of pinned digests' (indirect: the row names the source, the gate pins its URL)]",
     f"{F38}/F38XMutP/witness-run.txt W-X15 (ref P7,P9 -> mutant P9)",
     'if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:',
     'if (prov.get(sid) or [""])[0] != p.spec["raw_base"] + row["upstream"]:'),
    ("M05", "RUN", "rc-silence",
     "a package with a DEFECT clause exits 1, not 0 [gate docstring 'exit 0 = accept, 1 = reject'; "
     "package-gate row 'Exit 0 accept / 1 reject / 2 setup']",
     f"{F38}/F38XMutRerunMain/survivor-probes.txt probe A2 (ref rc=1 defects=8 -> mutant rc=0, same 8 DEFECT lines)",
     "        defects += not ok",
     "        defects += 0"),
    ("M06", "MAIN", "rc-mirror",
     "the genuine package exits 0, not 1 [gate docstring 'exit 0 = accept, 1 = reject'; Q24 'the genuine "
     "package must be accepted']",
     f"{F38}/F38XMutRerunMain/survivor-probes.txt probe A1 (ref rc=0 -> mutant rc=1, clause lines identical)",
     "        return 0 if cmd_package(args, spec) == 0 else 1",
     "        return 1 if cmd_package(args, spec) == 0 else 1"),
    ("M07", "D5", "mirror",
     "a D5 quote is found in a capture whose quote span carries markup [Q24 'the genuine package must be "
     "accepted' (indirect, as M01); the gate strips tags before the flat compare]",
     f"{F38}/F38XMutRerunMain/survivor-probeB.txt (ref D5 ok rc=0 -> mutant D5 DEFECT rc=1)",
     '        flat = re.sub(r"\\s+", "", re.sub(r"<[^>]+>", "", read(capture) or ""))',
     '        flat = re.sub(r"\\s+", "", read(capture) or "")'),
]
TOTAL = 7


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


def build_module_child(lane, module, dest, nonce=""):
    """Child-process entry: build every fixture of one battery module into dest/fNNN, print JSON only."""
    r37 = load(lane / R37_REL, "kengaku_r37_c1")
    ctx = r37.Ctx(lane, r37.load_r36(lane))
    mod = load(module, f"kengaku_b_{module.stem}")
    out = []
    for k, fx in enumerate(getattr(mod, "FIXTURES", [])):
        d = dest / f"f{k:03d}"
        d.mkdir(parents=True)
        argv = [str(t) for t in fx["build"](ctx, d)]
        out.append({"fid": fx["fid"], "expect": fx.get("expect"), "defects": fx.get("defects"),
                    "argv": argv, "dir": str(d)})
    sys.stdout.write("BUILT " + nonce + " " + json.dumps(out) + "\n")
    return 0


def module_fixtures(bdir, root, tag, lane):
    """Build each module of bdir out of process; returns (fixtures, sidechannel count) or raises."""
    out, side = [], 0
    if not bdir.is_dir():
        return out, side
    for f in sorted(bdir.glob("*.py")):
        text = f.read_text()
        hits = [t for t in SIDECHANNEL if t in text]
        if hits:
            side += 1
            print(f"SIDECHANNEL {tag}/{f.name} tokens={','.join(hits)}")
        dest = root / "fx" / f"{tag}-{f.stem}"
        dest.mkdir(parents=True)
        nonce = secrets.token_hex(16)
        r = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve()), "--build-module", str(f),
                            "--dest", str(dest), "--lane", str(lane), "--nonce", nonce],
                           cwd=str(dest), capture_output=True, text=True, timeout=900)
        built = [l for l in r.stdout.splitlines() if l.startswith("BUILT " + nonce + " ")]
        if r.returncode != 0 or len(built) != 1:
            raise RuntimeError(f"module {tag}/{f.name} failed to build (rc={r.returncode}): {r.stderr.strip()[-300:]}")
        for k, fx in enumerate(json.loads(built[0][len("BUILT " + nonce + " "):])):
            fx["dir"] = str(dest / f"f{k:03d}")  # A5: the parent's own directory, never the child's report
            out.append({**fx, "r36": False, "own_spec_ok": True, "module": f"{tag}/{f.name}"})
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


def family_ok(clause, argv):
    if clause == "MAIN":
        return True
    return argv[0] == FAMILY.get(clause, "package")


def exhibits(clause, direction, fx, ref, mut):
    """True iff (ref, mut) on fixture fx satisfies `direction` for `clause` (family already checked)."""
    if direction == "rc-silence":
        declared = fx.get("defects")
        return fx.get("expect") == "reject" and bool(declared) and ref[0] == 1 and mut[0] == 0
    if direction == "rc-mirror":
        return fx.get("expect") == "accept" and ref[0] == 0 and mut[0] == 1
    if direction == "error":
        return fx.get("expect") == "error" and ref[0] == 2 and mut[0] in (0, 1)
    if ref[0] not in (0, 1) or mut[0] not in (0, 1) or clause in ("RUN", "MAIN"):
        return False
    declared = set(fx["defects"]) if fx.get("defects") is not None else set(ref[1])
    if direction == "silence":
        return clause in ref[1] and clause in declared and clause not in mut[1]
    return clause in ref[2] and clause in mut[1]  # mirror


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--battery", choices=("full", "r38"), default="full")
    ap.add_argument("--battery-dir", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--build-module", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--dest", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--nonce", default="", help=argparse.SUPPRESS)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if a.build_module:
        return build_module_child(lane, pathlib.Path(a.build_module).resolve(), pathlib.Path(a.dest).resolve(), a.nonce)
    dev = a.battery_dir is not None or a.only is not None or a.battery != "full"
    mism = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
    for bd in ("plans/battery37", "plans/battery38"):
        have = {f"{bd}/{p.name}" for p in (lane / bd).glob("*.py")}
        want = {rel for rel in PINS if rel.startswith(bd + "/")}
        mism += sorted(have - want)
    print(f"PINS total={len(PINS)} mismatched={len(mism)}" + (f" first={mism[0]}" if mism else ""))
    if any(m.startswith(("plans/battery37/", "plans/battery38/")) and m not in PINS for m in mism):
        print("AUDIT unpinned battery module present; refusing to import it", file=sys.stderr)
        return 2
    r37 = load(lane / R37_REL, "kengaku_r37_c1")
    gate_src = (lane / r37.GATE_REL).read_text() if (lane / r37.GATE_REL).is_file() else ""
    gate_ok = "plans/pkg_gate.py" not in mism
    r36 = r37.load_r36(lane)
    ctx = r37.Ctx(lane, r36)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k39-c1a-", dir=a.work))
    try:
        inproc = r37.r36_fixtures(r36) + r37.battery37_fixtures(lane / r37.BATTERY_REL)
        built, side = [], 0
        for i, fx in enumerate(inproc):
            d = root / "fx" / "inproc" / f"f{i:03d}"
            d.mkdir(parents=True)
            argv = list(fx["build"](ctx, d))
            if not argv or argv[0] not in ("package", "d4-line", "d5-line") or "--spec" in argv:
                print(f"SETUP fixture {fx['fid']} returned a forbidden argv", file=sys.stderr)
                return 2
            built.append((fx, d, argv))
        try:
            more, s38 = module_fixtures(lane / BATTERY38_REL, root, "battery38", lane)
            side += s38
            if a.battery == "full":
                bdir = pathlib.Path(a.battery_dir).resolve() if a.battery_dir else lane / BATTERY39_REL
                m39, s39 = module_fixtures(bdir, root, "battery39", lane)
                more += m39
                side += s39
        except (RuntimeError, subprocess.TimeoutExpired, ValueError, KeyError) as e:
            print(f"SETUP {e}", file=sys.stderr)
            return 2
        for fx in more:
            d, argv = pathlib.Path(fx["dir"]), list(fx["argv"])
            ok_argv = bool(argv) and argv[0] in ("package", "d4-line", "d5-line") and d.is_dir()
            if "--root" in argv:
                k = argv.index("--root")
                ok_argv = ok_argv and k + 1 < len(argv) and pathlib.Path(argv[k + 1]).resolve().is_relative_to(d.resolve())
            if "--spec" in argv:
                k = argv.index("--spec")
                ok_argv = ok_argv and k + 1 < len(argv) \
                    and pathlib.Path(argv[k + 1]).resolve().is_relative_to(d.resolve())
            if not ok_argv:
                print(f"SETUP fixture {fx['fid']} returned a forbidden argv", file=sys.stderr)
                return 2
            built.append((fx, d, argv))
        ids = [fx["fid"] for fx, _d, _a in built]
        if len(set(ids)) != len(ids):
            print("SETUP duplicate fixture id", file=sys.stderr)
            return 2
        gdir = root / "gates"
        gdir.mkdir()
        ref_gate = gdir / "ref.py"
        ref_gate.write_text(gate_src)
        ref_digest = sha256(ref_gate)
        ref, wrong = [], 0
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
        nondet = []
        for mid, clause, direction, label, _witness, old, new in MUTANTS:
            if only and mid not in only:
                continue
            if not gate_ok or gate_src.count(old) != 1 or direction not in DIRECTIONS:
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
            by, seen = None, set()
            for j, (fx, d, argv) in enumerate(built):
                if not family_ok(clause, argv):
                    continue
                mut = run_gate(mg, ctx.spec_path, argv)
                if exhibits(clause, direction, fx, ref[j], mut):
                    again_ref = run_gate(ref_gate, ctx.spec_path, argv)
                    again_mut = run_gate(mg, ctx.spec_path, argv)
                    if again_ref != ref[j] or again_mut != mut:
                        nondet.append(f"{mid}:{fx['fid']}")
                        continue
                    by = fx["fid"]
                    break
                seen.update(x for x in DIRECTIONS if x != direction and exhibits(clause, x, fx, ref[j], mut))
            if sha256(mg) != digest or sha256(ref_gate) != ref_digest:
                invalid += 1
                print(f"MUTANT {mid} {clause} {direction} invalid(gate file changed during the run) -- {label}")
                continue
            if by:
                killed += 1
                print(f"MUTANT {mid} {clause} {direction} killed by={by} -- {label}")
            else:
                survived += 1
                print(f"MUTANT {mid} {clause} {direction} SURVIVED exhibits={','.join(sorted(seen)) or 'none'}"
                      f" -- {label}")
        total = len(MUTANTS) if not only else len([m for m in MUTANTS if m[0] in only])
        print(f"MUTANTS total={total} killed={killed} survived={survived} invalid={invalid} null_detected={null_detected}")
        final = [rel for rel, dig in PINS.items() if sha256(lane / rel) != dig]
        print(f"PINS final total={len(PINS)} mismatched={len(final)}" + (f" first={final[0]}" if final else ""))
        print(f"AUDIT nondeterministic_kills={len(nondet)}" + (f" first={nondet[0]}" if nondet else ""))
        audit_clean = not final and not nondet and not mism
        print(f"AUDIT C1 {'clean' if audit_clean else 'dirty'}")
        if dev:
            print("PREDICATE C1 n/a (non-default battery or mutant subset)")
            return 0 if (wrong == 0 and disagree == 0 and side == 0 and survived == 0 and invalid == 0
                         and null_detected == 0) else 1
        good = (not mism and len(PINS) == 26 and len(MUTANTS) == TOTAL and wrong == 0 and disagree == 0
                and side == 0 and killed == TOTAL and survived == 0 and invalid == 0 and null_detected == 0)
        print(f"PREDICATE C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

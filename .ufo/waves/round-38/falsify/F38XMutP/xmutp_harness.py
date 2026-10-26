#!/usr/bin/env python3
"""F38XMutP extra-mutant harness (round-38 wave 2, falsify seat F38XMutP).

Runs EXTRA (non-frozen) mutants of plans/pkg_gate.py clauses P1-P8 — byte-level old->new shapes
beyond the frozen N01-N22 list (plans/round38_c1_verify.py) and the frozen M01-M55 list
(plans/round37_c1_verify.py) — over the FULL landed battery (round-36 + plans/battery37 +
plans/battery38) with the round-38 ATTRIBUTED kill rule. Reuses the frozen counter's own functions
by importing plans/round38_c1_verify.py from the lane clone under test; the lane itself is never
written (mutant gate copies live under WORK).

Usage: xmutp_harness.py LANE WORK OUT
  LANE  clean clone of the landing tip 8c7422d7a646515d80af44844e8ecc8a1fc1d30a (read-only input)
  WORK  scratch parent for fixture dirs and mutant gate copies (caller deletes)
  OUT   receipt path; every line printed is also appended here

Per mutant the harness scans every family-matching fixture and records an attributed kill under
EITHER direction (silence or mirror), so a mislabelled direction cannot hide a kill (the N21 lesson,
plans/mutant_direction_check.py). Survivors record how many fixtures differed at all and the first
differing (fid, ref, mut) triple, to separate "undemonstrated" from "differs-but-unattributed".
"""
import hashlib
import importlib.util
import pathlib
import py_compile
import shutil
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
WORK = pathlib.Path(sys.argv[2]).resolve()
OUT = pathlib.Path(sys.argv[3]).resolve()
OUTF = open(OUT, "w")


def out(*a):
    s = " ".join(map(str, a))
    print(s, flush=True)
    OUTF.write(s + "\n")
    OUTF.flush()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# (id, clause, shape, label, old, new) — extra mutants, frozen lists excluded. old must occur once.
MUTANTS = [
    ("X01", "P1", "first-item-only", "every pinned instrument is checked, not only the first",
     r'bad = [rel for rel, dig in pins.items() if sha256(p.root / rel) != dig]',
     r'bad = [rel for rel, dig in list(pins.items())[:1] if sha256(p.root / rel) != dig]'),
    ("X02", "P1", "mirror", "an instrument set matching its pins is accepted (P1 false-red)",
     r'for rel, dig in pins.items() if sha256(p.root / rel) != dig]',
     r'for rel, dig in pins.items() if sha256(p.root / rel) == dig]'),
    ("X03", "P2", "mirror", "a receipt matching its pin is accepted (P2 false-red)",
     r'''return got == want, f"receipt_sha256={'pinned' if got == want else got}"''',
     r'''return got != want, f"receipt_sha256={'pinned' if got == want else got}"'''),
    ("X04", "P3", "off-by-one", "a package with exactly min_quotes distinct quotes is accepted (N02's min_quotes twin)",
     r'ok = len(texts) >= rules["min_quotes"] and',
     r'ok = len(texts) > rules["min_quotes"] and'),
    ("X05", "P3", "off-by-one", "a quote one word above the range is still outside it",
     r'short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]',
     r'short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi + 1]'),
    ("X21", "P7", "reordered-branch", "the per-row source compare runs against the collected prov, not an empty one",
     r'''    rules, bad, prov = p.spec["entry_rules"], [], {}
    for line in p.entry.splitlines():''',
     r'''    rules, bad, prov = p.spec["entry_rules"], [], {}
    for sid, row in p.spec["rows"].items():
        if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:
            bad.append(f"{sid}: source line {'absent' if sid not in prov else 'not the pinned url'}")
    for line in p.entry.splitlines():'''),
    ("X07", "P4", "off-by-one", "verbatim starts on the cited line, not one below it",
     r'''elif q.text not in "\n".join(lines[q.start - 1:q.end]):''',
     r'''elif q.text not in "\n".join(lines[q.start:q.end]):'''),
    ("X08", "P4", "mirror", "a readable capture is not reported unreadable (P4 false-red)",
     r'''if lines is None:
            bad.append(f"{q.capture}: unreadable capture")''',
     r'''if lines is not None:
            bad.append(f"{q.capture}: unreadable capture")'''),
    ("X09", "P5", "mirror", "a manifest matching the capture bytes is accepted (P5 false-red)",
     r'if sha256(capdir / name) != digest:',
     r'if sha256(capdir / name) == digest:'),
    ("X10", "P5", "first-item-only", "every quote's capture is pinned in the manifest, not only the first alphabetically",
     r'for name in {q.capture for q in p.quotes}:',
     r'for name in sorted({q.capture for q in p.quotes})[:1]:'),
    ("X11", "P6", "loosened-compare", "a row with more than 11 cells is a defect too",
     r'if len(cells) != 11:',
     r'if len(cells) < 11:'),
    ("X12", "P6", "loosened-compare", "a duplicated registry row is a defect, not only an absent one",
     r'if len(found) != 1:',
     r'if len(found) < 1:'),
    ("X13", "P6", "mirror", "distinct teaches cells are accepted (P6 false-red)",
     r'if len(set(teaches)) != len(teaches):',
     r'if len(set(teaches)) == len(teaches):'),
    ("X14", "P7", "first-item-only", "source lines are collected from the whole entry, not its first line",
     r'for line in p.entry.splitlines():',
     r'for line in p.entry.splitlines()[:1]:'),
    ("X15", "P7", "loosened-compare", "exactly one pinned source line per row, not merely a first one",
     r'if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:',
     r'if (prov.get(sid) or [""])[0] != p.spec["raw_base"] + row["upstream"]:'),
    ("X16", "P7", "mirror", "a present verified-at line is accepted (P7 false-red)",
     r'''if f"verified-at: {rules['verified_at']}" not in p.entry:''',
     r'''if f"verified-at: {rules['verified_at']}" in p.entry:'''),
    ("X17", "P8", "first-item-only", "the index is read from the whole README, not its first line",
     r'for line in p.readme.splitlines():',
     r'for line in p.readme.splitlines()[:1]:'),
    ("X18", "P8", "first-item-only", "the index row must cite every registry row, the later included",
     r'elif not all(sid in rows[0] for sid in p.spec["rows"]):',
     r'elif not all(sid in rows[0] for sid in list(p.spec["rows"])[:1]):'),
    ("X19", "P8", "mirror", "a present coverage bullet is accepted (P8 false-red)",
     r'if not bullet:',
     r'if bullet:'),
    ("X20", "P5", "reordered-branch", "the uncovered-file check runs against the parsed manifest, not an empty one",
     r'''    pinned, bad = {}, []
    for line in text.splitlines():''',
     r'''    pinned, bad = {}, []
    for f in sorted(capdir.iterdir()):
        if f.is_file() and not f.name.startswith(".") and f.name != "SHA256SUMS" \
                and f.name not in pinned:
            bad.append(f"{f.name}: capture file not covered by the manifest")
    for line in text.splitlines():'''),
]


def main():
    m = load(LANE / "plans" / "round38_c1_verify.py", "kengaku_r38_c1")
    r37 = load(LANE / m.R37_REL, "kengaku_r37_c1")
    gate_path = LANE / r37.GATE_REL
    gate_src = gate_path.read_text()
    gate_digest = hashlib.sha256(gate_path.read_bytes()).hexdigest()
    frozen_digest = m.PINS["plans/pkg_gate.py"]
    out(f"GATE plans/pkg_gate.py sha256={'frozen' if gate_digest == frozen_digest else 'MISMATCH ' + gate_digest}")
    out(f"LANE {LANE}")

    frozen_pairs = {(x[4], x[5]) for x in m.MUTANTS} | {(x[3], x[4]) for x in r37.MUTANTS}
    hygiene = []
    for mid, clause, shape, label, old, new in MUTANTS:
        n = gate_src.count(old)
        if n != 1:
            hygiene.append(f"{mid} old-count={n}")
        if (old, new) in frozen_pairs:
            hygiene.append(f"{mid} duplicates a frozen (old,new) pair")
    if hygiene:
        for h in hygiene:
            out("HYGIENE FAIL", h)
        return 2
    out(f"HYGIENE mutants={len(MUTANTS)} old-unique=yes frozen-pair-overlap=no")

    r36 = r37.load_r36(LANE)
    ctx = r37.Ctx(LANE, r36)
    fixtures = r37.r36_fixtures(r36) + r37.battery37_fixtures(LANE / r37.BATTERY_REL)
    more, side = m.battery38_fixtures(LANE / m.BATTERY38_REL)
    fixtures += more

    root = pathlib.Path(tempfile.mkdtemp(prefix="f38xmutp-", dir=WORK))
    try:
        built = []
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
                out(f"SETUP fixture {fx['fid']} returned a forbidden argv")
                return 2
            built.append((fx, d, argv))
        gdir = root / "gates"
        gdir.mkdir()
        ref_gate = gdir / "ref.py"
        ref_gate.write_text(gate_src)
        ref = [m.run_gate(ref_gate, ctx.spec_path, argv) for fx, d, argv in built]
        wrong = 0
        for (fx, d, argv), res in zip(built, ref):
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
            if not ok:
                out(f"FIXTURE {fx['fid']} expect={exp} declared={','.join(sorted(declared)) if declared else '-'}"
                    f" observed_rc={res[0]} observed_defects={','.join(sorted(res[1])) or '-'} WRONG")
        null_gate = gdir / "null.py"
        null_gate.write_text(gate_src)
        null_detected = sum(1 for j, (fx, d, argv) in enumerate(built)
                            if m.run_gate(null_gate, ctx.spec_path, argv) != ref[j])
        out(f"BATTERY fixtures={len(built)} wrong={wrong} null_detected={null_detected} sidechannel={side}")
        if wrong or null_detected:
            out("BATTERY UNSANE -- kills inconclusive")
            return 2

        killed = survived = invalid = 0
        for mid, clause, shape, label, old, new in MUTANTS:
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            try:
                py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
            except py_compile.PyCompileError:
                invalid += 1
                out(f"MUTANT {mid} {clause} {shape} invalid(compile) -- {label}")
                continue
            digest = hashlib.sha256(mg.read_bytes()).hexdigest()
            fam = m.FAMILY.get(clause, "package")
            by = dir_seen = None
            diffs = 0
            first_diff = None
            for j, (fx, d, argv) in enumerate(built):
                if argv[0] != fam:
                    continue
                mut = m.run_gate(mg, ctx.spec_path, argv)
                if mut != ref[j]:
                    diffs += 1
                    if first_diff is None:
                        first_diff = (fx["fid"], ref[j], mut)
                if m.attributed(clause, "silence", fx, argv, ref[j], mut):
                    by, dir_seen = fx["fid"], "silence"
                    break
                if m.attributed(clause, "mirror", fx, argv, ref[j], mut):
                    by, dir_seen = fx["fid"], "mirror"
                    break
            if hashlib.sha256(mg.read_bytes()).hexdigest() != digest:
                invalid += 1
                out(f"MUTANT {mid} {clause} {shape} invalid(file changed during run) -- {label}")
                continue
            if by:
                killed += 1
                out(f"MUTANT {mid} {clause} {shape} killed by={by} dir={dir_seen} sha256={digest[:16]} -- {label}")
            else:
                survived += 1
                extra = f" diffs={diffs} first_diff={first_diff}" if first_diff else " no-fixture-differs"
                out(f"MUTANT {mid} {clause} {shape} SURVIVED{extra} sha256={digest[:16]} -- {label}")
        out(f"MUTANTS total={len(MUTANTS)} killed={killed} survived={survived} invalid={invalid}")
        out(f"VERDICT-COUNTER xmut-p-killed-{killed}/{len(MUTANTS)}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)
        OUTF.close()


if __name__ == "__main__":
    sys.exit(main())

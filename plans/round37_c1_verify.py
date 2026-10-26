#!/usr/bin/env python3
"""Round-37 C1 counter (calibration): which advertised defect clauses of the round-36 package gate does a
fixture battery actually demonstrate? Frozen gate mutants against `plans/pkg_gate.py`.

Frozen predicate (same sentence in plans/round-37-claims.md and in the receipt label):
  C1 passes iff `python3 plans/round37_c1_verify.py --lane .` prints
  `BATTERY fixtures=<n> wrong=0 renamed_disagree=0`, then
  `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, then `PREDICATE C1 pass`, exit 0,
  measured on a clean clone of the landing tip, with `plans/pkg_gate.py` at its freeze digest.

Self-assessment under test: the gate's docstring, `corpus/QUALITY.md` Q24 and the SCORECARD capability row
`package-gate` (round 36) advertise that the gate rejects each defect class below. A class counts as
demonstrated only when silencing that one branch of the gate (one frozen byte-level mutant) changes the
gate's observable result on at least one battery fixture. Survivors are advertised-but-undemonstrated
clauses: the mismatch count between what the lane says its gate does and what its tests show.

Observable result of one gate run = (exit code, set of clause ids printed `DEFECT`). Exit codes other than
0/1 are kept as they are, so a mutant that makes the gate crash on a fixture differs from the null gate.

  * reference: the unmodified gate (copied outside the lane) over every fixture.
  * null mutant: a second copy of the unmodified gate; any fixture whose result differs from the
    reference is `null_detected` (non-determinism in the battery or harness).
  * mutant Mxx: the gate with exactly one frozen `old -> new` replacement; `old` must occur exactly once
    and the result must compile, else the mutant is `invalid`. killed iff some fixture's result differs
    from the reference.
  * battery check: every fixture declares `expect` (accept/reject) and, for rejects, the exact set of
    clause ids that must print `DEFECT`; the reference must match each declaration (`wrong` counts misses).
  * renamed run: the reference re-run over copies of every fixture under different directory names;
    any result change is `renamed_disagree` (a gate must never key on what a fixture is called).

Battery = the round-36 battery (14 fixtures, built by `plans/round36_c1_verify.py` from committed
round-35 bytes, declarations derived from its own accept/reject labels) plus every fixture in
`plans/battery37/*.py` (each module exports FIXTURES, a list of dicts: fid, expect, defects, build;
build(ctx, d) fills the empty directory d and returns the gate argv tail, never `--spec`).

  --battery r36        round-36 battery only (the do-nothing control: what the frozen battery kills)
  --battery-dir DIR    load battery37 modules from DIR (development; the predicate prints n/a)
  --only M01,M02       restrict mutants (development; the predicate prints n/a)
  --work DIR           scratch parent (default: $TMPDIR via tempfile)
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

GATE_REL = "plans/pkg_gate.py"
SPEC_REL = "plans/pkg-spec-r35.json"
R36_REL = "plans/round36_c1_verify.py"
BATTERY_REL = "plans/battery37"
GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"
CLAUSE_LINE = re.compile(r"^(P\d+|D4|D5) (ok|DEFECT) ")

# (id, clause, advertised defect class, old, new) — frozen at the gate digest above.
MUTANTS = [
    ("M01", "P1", "frozen instrument digest mismatch",
     'return bool(pins) and not bad, f"pinned=', 'return bool(pins), f"pinned='),
    ("M02", "P2", "receipt unreadable",
     "return False, f\"receipt unreadable: {p.spec['receipt']}\"", "return True, f\"receipt unreadable: {p.spec['receipt']}\""),
    ("M03", "P2", "receipt digest differs from the pin",
     'return got == want, f"receipt_sha256=', 'return True, f"receipt_sha256='),
    ("M04", "P3", "no Located quotes section",
     "return False, \"no '## Located quotes' section\"", "return True, \"no '## Located quotes' section\""),
    ("M05", "P3", "an unparsed quote row",
     "if p.bad_rows:", "if False:"),
    ("M06", "P3", "fewer distinct quotes than min_quotes",
     'ok = len(texts) >= rules["min_quotes"] and', "ok = True and"),
    ("M07", "P3", "fewer distinct located lines than min_distinct_locations",
     'len(locs) >= rules["min_distinct_locations"]', "True"),
    ("M08", "P3", "a quote outside the word range",
     "and not short", "and True"),
    ("M09", "P4", "no parsed quote",
     'return False, "no parsed quote"', 'return True, "no parsed quote"'),
    ("M10", "P4", "quote cites an unreadable capture",
     'bad.append(f"{q.capture}: unreadable capture")', "pass"),
    ("M11", "P4", "quote line range outside the capture",
     'bad.append(f"{q.capture}:{q.start}-{q.end}: line range outside the capture")', "pass"),
    ("M12", "P4", "quote not verbatim on its cited line",
     'bad.append(f"{q.capture}:{q.start}: quote not verbatim there")', "pass"),
    ("M13", "P5", "capture manifest absent",
     'return False, f"capture manifest absent:', 'return True, f"capture manifest absent:'),
    ("M14", "P5", "unparsed manifest line",
     'bad.append(f"unparsed manifest line {line.strip()[:50]!r}")', "pass"),
    ("M15", "P5", "manifest digest does not match the capture bytes",
     'bad.append(f"{name}: manifest digest does not match the bytes")', "pass"),
    ("M16", "P5", "row capture not pinned in the manifest",
     'bad.append(f"{sid}: capture {name} is not pinned in the manifest")', "pass"),
    ("M17", "P5", "manifest digest differs from the spec pin",
     'bad.append(f"{sid}: manifest digest differs from the spec pin")', "pass"),
    ("M18", "P5", "quoted capture not pinned in the manifest",
     'bad.append(f"quote capture {name} is not pinned in the manifest")', "pass"),
    ("M19", "P5", "capture file not covered by the manifest",
     'bad.append(f"{f.name}: capture file not covered by the manifest")', "pass"),
    ("M20", "P6", "registry row missing or duplicated",
     'bad.append(f"{sid}: rows={len(found)}")', "pass"),
    ("M21", "P6", "registry row without 11 cells",
     'bad.append(f"{sid}: cells={len(cells)}")', "pass"),
    ("M22", "P6", "row url not the pinned raw path",
     'bad.append(f"{sid}: url not the pinned raw path")', "pass"),
    ("M23", "P6", "row tier wrong",
     'bad.append(f"{sid}: tier={cells[3]!r}")', "pass"),
    ("M24", "P6", "row status wrong",
     'bad.append(f"{sid}: status={cells[7]!r}")', "pass"),
    ("M25", "P6", "row used-by is not the entry",
     'bad.append(f"{sid}: used-by is not the entry")', "pass"),
    ("M26", "P6", "teaches cell under min_teaches_words",
     'bad.append(f"{sid}: teaches words={len(cells[6].split())}")', "pass"),
    ("M27", "P6", "teaches cells not pairwise distinct",
     'bad.append("teaches cells are not pairwise distinct")', "pass"),
    ("M28", "P7", "entry unreadable",
     'return False, "entry unreadable"', 'return True, "entry unreadable"'),
    ("M29", "P7", "source line absent or not the pinned url",
     "bad.append(f\"{sid}: source line {'absent' if sid not in prov else 'not the pinned url'}\")", "pass"),
    ("M30", "P7", "verified-at absent or not the frozen date",
     'bad.append("verified-at line absent or not the frozen date")', "pass"),
    ("M31", "P7", "recheck line absent",
     'bad.append("recheck line absent")', "pass"),
    ("M32", "P7", "no Negative space section",
     "bad.append(\"no '## Negative space' section\")", "pass"),
    ("M33", "P7", "Negative space carries no falsifier",
     "bad.append(\"'## Negative space' carries no falsifier\")", "pass"),
    ("M34", "P8", "README unreadable",
     'return False, "README unreadable"', 'return True, "README unreadable"'),
    ("M35", "P8", "index rows for the entry not exactly one",
     'bad.append(f"index rows for knowledge/{entry_name}={len(rows)}")', "pass"),
    ("M36", "P8", "index row does not cite every registry row",
     'bad.append("index row does not cite every registry row")', "pass"),
    ("M37", "P8", "no coverage bullet naming entry and receipt",
     'bad.append("no coverage bullet naming the entry and its receipt")', "pass"),
    ("M38", "P8", "knowledge files differ from index rows",
     'bad.append(f"knowledge files={len(files)} index rows={len(indexed)}")', "pass"),
    ("M39", "P9", "root is not a git worktree",
     'return False, "root is not a readable git worktree"', 'return True, "root is not a readable git worktree"'),
    ("M40", "P9", "untracked file present",
     'return not left, f"untracked=', 'return True, f"untracked='),
    ("M41", "P10", "receipt unreadable at re-run",
     'return False, "receipt unreadable"', 'return True, "receipt unreadable"'),
    ("M42", "P10", "fresh probe exits nonzero",
     'return False, f"fresh probe exit=', 'return True, f"fresh probe exit='),
    ("M43", "P10", "fresh probe output not byte-equal to the receipt",
     'return False, "fresh probe output is not byte-equal to the receipt"',
     'return True, "fresh probe output is not byte-equal to the receipt"'),
    ("M44", "D4", "d4 file unreadable",
     'return False, "file unreadable"\n        if len(lines) != 1 or not lines[0].startswith(spec["d4"]["label"]):',
     'return True, "file unreadable"\n        if len(lines) != 1 or not lines[0].startswith(spec["d4"]["label"]):'),
    ("M45", "D4", "d4 file is not exactly one line",
     'if len(lines) != 1 or not lines[0].startswith(spec["d4"]["label"]):',
     'if not lines[0].startswith(spec["d4"]["label"]):'),
    ("M46", "D4", "d4 line does not carry the label",
     'if len(lines) != 1 or not lines[0].startswith(spec["d4"]["label"]):', "if len(lines) != 1:"),
    ("M47", "D4", "d4 directional pattern absent",
     "if not re.search(pat, lines[0])]", "if False]"),
    ("M48", "D5", "d5 file unreadable",
     'return False, "file unreadable"\n        if len(lines) != 1 or not lines[0].startswith(d5["label"]):',
     'return True, "file unreadable"\n        if len(lines) != 1 or not lines[0].startswith(d5["label"]):'),
    ("M49", "D5", "d5 file is not exactly one line",
     'if len(lines) != 1 or not lines[0].startswith(d5["label"]):', 'if not lines[0].startswith(d5["label"]):'),
    ("M50", "D5", "d5 line does not carry the label",
     'if len(lines) != 1 or not lines[0].startswith(d5["label"]):', "if len(lines) != 1:"),
    ("M51", "D5", "d5 required token missing",
     "bad.append(f\"missing {d5['require']!r}\")", "pass"),
    ("M52", "D5", "d5 forbidden token present",
     "bad.append(f\"carries {d5['forbid']!r}\")", "pass"),
    ("M53", "D5", "d5 capture unreadable",
     'return False, "capture unreadable"', 'return True, "capture unreadable"'),
    ("M54", "D5", "d5 capture digest not in the manifest",
     'bad.append("capture digest is not the one in the manifest")', "pass"),
    ("M55", "D5", "d5 quote absent from the capture",
     'bad.append("quote absent from the capture")', "pass"),
]
TOTAL = 55


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def git(d, *args):
    return subprocess.run(["git", "-C", str(d), *args], capture_output=True, text=True, check=True).stdout


class Ctx:
    """Helpers a battery37 fixture builder may use; everything reads committed-in-tree lane bytes."""

    def __init__(self, lane, r36):
        self.lane = lane
        self.r36 = r36
        self.spec = r36.load_spec(lane)
        self.spec_path = lane / SPEC_REL

    def genuine_package(self, d):
        """git-init d (verified top-level) and copy the genuine round-35 package into it; index not updated."""
        d.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "-C", str(d), "init", "-q"], check=True)
        if pathlib.Path(git(d, "rev-parse", "--show-toplevel").strip()).resolve() != d.resolve():
            raise RuntimeError(f"fixture repo top-level is not {d}")
        self.r36.copy_package(self.lane, self.spec, d)
        return d

    def git_add(self, d):
        git(d, "add", "-A")  # index only: no commit, no identity

    def d4_line(self):
        return self.r36.d4_line(self.lane, self.spec)

    def d5_line(self):
        return self.r36.d5_line(self.lane, self.spec)

    def d5_capture_dir(self):
        return self.lane / self.spec["d5_capture_dir"]


def load_r36(lane):
    spec = importlib.util.spec_from_file_location("kengaku_r36_c1", lane / R36_REL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def r36_fixtures(r36):
    """The frozen round-36 battery as fixture dicts (its builders make their own dirs; we move them into d)."""
    out = []

    def pkg(pid, expect):
        def build(ctx, d):
            tmp = pathlib.Path(tempfile.mkdtemp(dir=d.parent))
            for fid, _label, _exp, src in r36.build_package_fixtures(ctx.lane, ctx.spec, tmp):
                if fid == pid:
                    shutil.rmtree(d)
                    shutil.move(str(src), str(d))
            shutil.rmtree(tmp, ignore_errors=True)
            return ["package", "--root", str(d), "--require-clean-tree"]
        return {"fid": f"r36-{pid}", "expect": expect, "defects": None, "r36": True, "build": build}

    def line(lid, expect):
        def build(ctx, d):
            for fid, _label, _exp, argv in r36.build_line_fixtures(ctx.lane, ctx.spec, d):
                if fid == lid:
                    return argv
            raise RuntimeError(f"round-36 line fixture {lid} absent")
        return {"fid": f"r36-{lid}", "expect": expect, "defects": None, "r36": True, "build": build}

    for pid in ("P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"):
        out.append(pkg(pid, "accept" if pid == "P0" else "reject"))
    for lid, exp in (("L1", "accept"), ("L2", "reject"), ("L3", "reject"),
                     ("L4", "accept"), ("L5", "reject"), ("L6", "reject")):
        out.append(line(lid, exp))
    return out


def battery37_fixtures(bdir):
    out = []
    if not bdir.is_dir():
        return out
    for f in sorted(bdir.glob("*.py")):
        spec = importlib.util.spec_from_file_location(f"kengaku_b37_{f.stem}", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        out.extend({**fx, "r36": False} for fx in getattr(mod, "FIXTURES", []))
    return out


def run_gate(gate, spec_path, argv):
    try:
        r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(spec_path)],
                           capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return ("timeout", frozenset())
    bad = frozenset(m.group(1) for m in map(CLAUSE_LINE.match, r.stdout.splitlines()) if m and m.group(2) == "DEFECT")
    return (r.returncode, bad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--battery", choices=("full", "r36"), default="full")
    ap.add_argument("--battery-dir", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    dev = a.battery_dir is not None or a.only is not None or a.battery != "full"
    gate_src = (lane / GATE_REL).read_text() if (lane / GATE_REL).is_file() else None
    gate_ok = gate_src is not None and sha256(lane / GATE_REL) == GATE_SHA256
    print(f"GATE {GATE_REL} sha256={'frozen' if gate_ok else 'NOT-AT-FREEZE-DIGEST'}")
    r36 = load_r36(lane)
    ctx = Ctx(lane, r36)
    fixtures = r36_fixtures(r36)
    if a.battery == "full":
        bdir = pathlib.Path(a.battery_dir).resolve() if a.battery_dir else lane / BATTERY_REL
        fixtures += battery37_fixtures(bdir)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k37-c1-", dir=a.work))
    try:
        built, wrong = [], 0
        ids = [f["fid"] for f in fixtures]
        if len(set(ids)) != len(ids):
            print("SETUP duplicate fixture id", file=sys.stderr)
            return 2
        for i, fx in enumerate(fixtures):
            d = root / "fx" / f"f{i:03d}"
            d.mkdir(parents=True)
            argv = list(fx["build"](ctx, d))
            if "--spec" in argv or not argv or argv[0] not in ("package", "d4-line", "d5-line"):
                print(f"SETUP fixture {fx['fid']} returned a forbidden argv", file=sys.stderr)
                return 2
            built.append((fx, d, argv))
        # reference + battery declarations
        gdir = root / "gates"
        gdir.mkdir()
        ref_gate = gdir / "ref.py"
        ref_gate.write_text(gate_src or "")
        ref = []
        for fx, d, argv in built:
            res = run_gate(ref_gate, ctx.spec_path, argv)
            ref.append(res)
            want_rc = 0 if fx["expect"] == "accept" else 1
            declared = fx.get("defects")
            if not fx.get("r36") and (declared is None or fx.get("expect") not in ("accept", "reject")):
                ok = False  # a battery37 fixture must declare expect and its exact DEFECT clause set
            else:
                ok = res[0] == want_rc and (declared is None or res[1] == frozenset(declared))
            if fx["expect"] == "accept":
                ok = ok and not res[1]
            wrong += not ok
            print(f"FIXTURE {fx['fid']} expect={fx['expect']} declared={','.join(sorted(fx['defects'])) if fx['defects'] else '-'}"
                  f" observed_rc={res[0]} observed_defects={','.join(sorted(res[1])) or '-'} {'ok' if ok else 'WRONG'}")
        # renamed run: same bytes under different directory names
        ren_root = root / "renamed"
        ren_root.mkdir()
        disagree = 0
        for i, (fx, d, argv) in enumerate(built):
            nd = ren_root / f"x{(len(built) - i) * 7919 % 100003:05d}q"
            shutil.copytree(d, nd, symlinks=True)
            nargv = [t.replace(str(d), str(nd)) for t in argv]
            if run_gate(ref_gate, ctx.spec_path, nargv) != ref[i]:
                disagree += 1
                print(f"RENAMED {fx['fid']} DISAGREES")
        print(f"BATTERY fixtures={len(built)} wrong={wrong} renamed_disagree={disagree}")

        def differs(gate):
            for j, (fx, d, argv) in enumerate(built):
                if run_gate(gate, ctx.spec_path, argv) != ref[j]:
                    return fx["fid"]
            return None

        null_gate = gdir / "null.py"
        null_gate.write_text(gate_src or "")
        null_detected = sum(1 for j, (fx, d, argv) in enumerate(built) if run_gate(null_gate, ctx.spec_path, argv) != ref[j])
        only = set(a.only.split(",")) if a.only else None
        killed = survived = invalid = 0
        for mid, clause, label, old, new in MUTANTS:
            if only and mid not in only:
                continue
            if not gate_ok or gate_src.count(old) != 1:
                invalid += 1
                print(f"MUTANT {mid} {clause} invalid -- {label}")
                continue
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            try:
                py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
            except py_compile.PyCompileError:
                invalid += 1
                print(f"MUTANT {mid} {clause} invalid(compile) -- {label}")
                continue
            digest = sha256(mg)
            by = differs(mg)
            if sha256(mg) != digest:
                invalid += 1
                print(f"MUTANT {mid} {clause} invalid(mutant file changed during the run) -- {label}")
                continue
            if by:
                killed += 1
                print(f"MUTANT {mid} {clause} killed by={by} -- {label}")
            else:
                survived += 1
                print(f"MUTANT {mid} {clause} SURVIVED -- {label}")
        total = len(MUTANTS) if not only else len([m for m in MUTANTS if m[0] in only])
        print(f"MUTANTS total={total} killed={killed} survived={survived} invalid={invalid} null_detected={null_detected}")
        good = (not dev and gate_ok and len(MUTANTS) == TOTAL and wrong == 0 and disagree == 0
                and killed == TOTAL and survived == 0 and invalid == 0 and null_detected == 0)
        if dev:
            print("PREDICATE C1 n/a (non-default battery or mutant subset)")
            return 0 if (wrong == 0 and disagree == 0 and survived == 0 and invalid == 0 and null_detected == 0) else 1
        print(f"PREDICATE C1 {'pass' if good else 'fail'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

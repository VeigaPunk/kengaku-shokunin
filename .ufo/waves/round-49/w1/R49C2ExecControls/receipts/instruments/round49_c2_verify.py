#!/usr/bin/env python3
"""Round-49 C2 counter candidate (coverage): the round-46 TB2 `polyglot-c-py` package under a Q40
re-frozen counter.

Wave-1 control instrument, NOT the stage-2 pin. Contract = `plans/round46_c3_verify.py`
(digest-pinned, imported) plus the four frozen deltas of `plans/round-49-claims.md` §C2:

  (a) V7P — positive tag coverage from the frozen tables alone: every frozen tag is cited by at least
      one committed receipt case `violates=` token, every requirement-map row parses to the header's
      column count, and violating cases exist for `both-print` and `toolchain`;
  (b) --no-p10 — the package gate runs with P10 (fresh probe re-run) disabled. This is the V8 fix and
      it is structural: without --no-p10 this file refuses to run at all, so no wave-1 seat can point
      it at the claimed work or execute the frozen probe through it;
  (c) V15 — precondition dry-run: every frozen input digest resolves and every frozen table parses
      before any leg scores; a missing or tamper-pinned input is a DEFECT of that leg, never a crash;
  (d) V14 — mutation battery over `plans/mutants49/plan.json`; an absent plan or an unmet floor is a
      DEFECT with a reason (the wave-1 instrument reports the unpinned floor as a defect, exactly as
      the frozen claim requires).

Receipt discipline (Q22): the first line is `REV <40-hex>` of the tree measured, followed by
`REV_DIRTY <n>` when the clone is uncommitted-safe (0 expected).

Named limits of this candidate, for the L1's stage-2 decision:
  * V10's DECISIVE map and V12's row rule are the imported round-46 ones; a stage-2 case-table
    amendment re-keys V10's map, which this file does not do.
  * V14 fixes a mutant-plan schema (`{"N": int, "mutants":[{"id","file","find","replace"}]}`) because
    no plan exists yet; the stage-2 counter owns the authoritative schema.
  * `plans/pkg-spec-r49.json` is read when present (spec/probe/dry pins); otherwise the round-46 spec
    and its pins are used, which is what the pre-receipt controls measure.
Exit 0 pass, 1 fail, 2 setup/refusal.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

R46_REL = "plans/round46_c3_verify.py"
R46_SHA256 = "a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4"
SPEC49_REL = "plans/pkg-spec-r49.json"
MUTANTS49_REL = "plans/mutants49/plan.json"
GATE_REL = "plans/pkg_gate.py"
GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"
ORDER_REL = "plans/order_check.py"
PROBE_REL = "plans/polyglot_c_py_probe.py"

SUBSTANTIVE = ("V3", "V4", "V7", "V7P", "V9", "V10", "V12")
FILLER_LEGS = ("V1", "V3", "V4", "V6", "V7", "V7P", "V9", "V10", "V12", "V14", "V15")
PACKAGE_LEGS = ("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V7P", "V8", "V9", "V10", "V11", "V12",
                "V13", "V14", "V15")

MAP_ANY = re.compile(r"^\|\s*`?instruction\.md:(\d+)`?\s*\|\s*`?([a-z0-9-]+)`?\s*\|")
MAP_SEC = re.compile(r"^## Requirement map\n(.*?)(?=^## |\Z)", re.S | re.M)


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def load_r46(lane):
    path = pathlib.Path(lane) / R46_REL
    got = sha256(path)
    if got != R46_SHA256:
        raise ValueError(f"{R46_REL} is not at its freeze digest (got {got})")
    spec = importlib.util.spec_from_file_location("r46_c3_verify", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_pkg(lane, m):
    """The package under test: the stage-2 r49 spec when present, else the frozen r46 spec."""
    p49 = pathlib.Path(lane) / SPEC49_REL
    if p49.is_file():
        s = json.loads(p49.read_text())
        pkg = m.Pkg(pathlib.Path(lane), s, p49, pathlib.Path(lane) / s["entry"],
                    pathlib.Path(lane) / s["receipt"], pathlib.Path(lane) / s.get("dry", m.DRY_REL),
                    pathlib.Path(lane) / s.get("capture_dir", m.CAP),
                    pathlib.Path(lane) / s.get("sources", "corpus/SOURCES.md"),
                    pathlib.Path(lane) / s["readme"], pins=m.CAPTURES, pinned=True,
                    probe=pathlib.Path(lane) / PROBE_REL,
                    claims=s.get("claims", m.CLAIMS_REL), name="package")
        return pkg, (s.get("probe_sha256", m.PROBE_SHA256), s.get("dry_sha256", m.DRY_SHA256)), "r49-spec"
    return m.real_pkg(pathlib.Path(lane)), (m.PROBE_SHA256, m.DRY_SHA256), "r46-spec"


# ---- (a) V7P: positive tag coverage from the frozen tables ---------------------------------------

def v7p(pkg, m):
    try:
        tags, _ids = m.dry_table(pkg)
        parsed = m.receipt_cases(pkg.receipt.read_text())
        entry = pkg.entry.read_text()
    except (OSError, ValueError) as e:
        return False, f"frozen tables unreadable: {e}"
    cited = set()
    for _obs, viol in parsed.values():
        cited |= viol
    bad = []
    uncited = [t for t in tags if t not in cited]
    if uncited:
        bad.append(f"frozen tags with no violating case: {uncited}")
    for t in ("both-print", "toolchain"):
        if t in tags and t not in cited:
            bad.append(f"{t}: round-46 V7 offender still uncovered")
    if not parsed:
        bad.append("receipt carries no parsable CASE ... observed= line")
    nrows = 0
    sec = MAP_SEC.search(entry)
    if not sec:
        bad.append("no '## Requirement map' section")
    else:
        rows = [l for l in sec.group(1).splitlines() if l.startswith("|")]
        header = rows[0] if rows else ""
        width = len(header.strip().strip("|").split("|")) if header else 0
        body = rows[2:] if len(rows) >= 2 else []
        nrows = len(body)
        if width < 4:
            bad.append(f"requirement map header has {width} cells")
        off = [r.strip()[:60] for r in body if len(r.strip().strip("|").split("|")) != width]
        if off:
            bad.append(f"rows not {width} cells: {off[:2]}")
        miss = [r.strip()[:60] for r in body if not MAP_ANY.match(r)]
        if miss:
            bad.append(f"unparsed rows {miss[:2]}")
        mapped = {MAP_ANY.match(r).group(2) for r in body if MAP_ANY.match(r)}
        if mapped != set(tags):
            bad.append(f"map tags differ from frozen tags (missing={sorted(set(tags) - mapped)} "
                       f"extra={sorted(mapped - set(tags))})")
        if body and len(body) < len(tags):
            bad.append(f"requirement-map rows={len(body)} frozen tags={len(tags)}")
    return not bad, (f"tags={len(tags)} parsed_cases={len(parsed)} map_rows={nrows} "
                     f"cited={len(set(tags) & cited)}/{len(tags)} bad={bad or 0}")


# ---- (c) V15: preconditions resolve and frozen tables parse ---------------------------------------

def v15(lane, pkg, m):
    lane = pathlib.Path(lane)
    unresolved, bad = [], []
    files = {"spec": pkg.spec_path, "entry": pkg.entry, "receipt": pkg.receipt, "dry": pkg.dry,
             "registry": pkg.registry, "readme": pkg.readme,
             "manifest": pathlib.Path(pkg.capdir) / "SHA256SUMS"}
    if pkg.pinned:
        files.update({"probe": lane / PROBE_REL, "gate": lane / GATE_REL, "order_check": lane / ORDER_REL})
    for name, p in files.items():
        if not pathlib.Path(p).is_file():
            unresolved.append(name)
    for sid, row in pkg.spec["rows"].items():
        cap = pathlib.Path(pkg.capdir) / row["capture"]
        if not cap.is_file() or sha256(cap) != row["sha256"]:
            unresolved.append(f"{sid}:{row['capture']}")
    tables, tags = 0, 0
    try:
        tags_map, ids = m.dry_table(pkg)
        tables += 1
        tags = len(tags_map)
        if not tags_map or not ids:
            bad.append("dry table has no TAG/CASE lines")
    except (OSError, ValueError) as e:
        bad.append(f"dry table unparsable: {e}")
    try:
        parsed = m.receipt_cases(pkg.receipt.read_text())
        tables += 1
        if not parsed:
            bad.append("receipt has no parsable CASE lines")
    except OSError as e:
        bad.append(f"receipt unreadable: {e}")
    entry = None
    try:
        entry = pkg.entry.read_text()
    except OSError:
        pass
    if entry is not None:
        sec = MAP_SEC.search(entry)
        if not sec:
            bad.append("requirement map section absent")
        else:
            rows = [l for l in sec.group(1).splitlines() if l.startswith("|")]
            if len(rows) < 2:
                bad.append("requirement map has no header + body")
            else:
                width = len(rows[0].strip().strip("|").split("|"))
                if any(len(r.strip().strip("|").split("|")) != width for r in rows[2:]):
                    bad.append("requirement map rows do not parse to the header's column count")
    ok = not unresolved and not bad
    return ok, (f"inputs={len(files) + len(pkg.spec['rows'])} unresolved={unresolved or 0} "
                f"tables_parsed={tables} tags={tags} bad={bad or 0}")


# ---- (d) V14: mutation battery -------------------------------------------------------------------

def v14(lane, pkg, work, m):
    plan_path = pathlib.Path(lane) / MUTANTS49_REL
    if not plan_path.is_file():
        return False, ("mutation floor <N> unpinned (stage-2 plan plans/mutants49/plan.json absent); "
                       "wave-1 mutants absent")
    try:
        plan = json.loads(plan_path.read_text())
    except json.JSONDecodeError as e:
        return False, f"mutant plan unparsable: {e}"
    n = plan.get("N")
    mutants = plan.get("mutants")
    if not isinstance(n, int) or n < 1 or not isinstance(mutants, list) or len(mutants) != n:
        return False, (f"mutant plan malformed N={n!r} "
                       f"mutants={len(mutants) if isinstance(mutants, list) else 'absent'}")
    # A mutant is caught only when it flips a leg that the UNMUTATED package prints ok for: a leg that
    # already defects at baseline cannot be "flipped", and a battery over such a tree would count every
    # mutant as caught for free. A baseline with no clean substantive leg makes the battery vacuous.
    base_res = {n: ok for n, ok, _note in run_legs(lane, pkg, work, SUBSTANTIVE, m, quiet=True)}
    clean = [n for n in SUBSTANTIVE if base_res.get(n)]
    if not clean:
        return False, ("MUTATION DEFECT vacuous battery: no substantive leg ("
                       + ", ".join(SUBSTANTIVE) + ") is clean at baseline, so no mutant can be caught")
    caught, missed = [], []
    for mut in mutants:
        mid = str(mut.get("id") or f"m{len(caught) + len(missed)}")
        target, find = mut.get("file"), mut.get("find", "")
        if not target or not find:
            missed.append(f"{mid}:malformed")
            continue
        dst = pathlib.Path(work) / f"mut-{mid}"
        shutil.copytree(lane, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        f = dst / target
        body = f.read_text() if f.is_file() else None
        if body is None or find not in body:
            missed.append(f"{mid}:target")
            shutil.rmtree(dst, ignore_errors=True)
            continue
        f.write_text(body.replace(find, str(mut.get("replace", "")), 1))
        try:
            mp = m.real_pkg(dst)
        except Exception:
            caught.append(mid)  # a mutant that stops the package parsing is caught
            shutil.rmtree(dst, ignore_errors=True)
            continue
        res = run_legs(dst, mp, dst, SUBSTANTIVE, m, quiet=True)
        flipped = [n for n, ok, _note in res if not ok and base_res.get(n)]
        (caught if flipped else missed).append(mid)
        shutil.rmtree(dst, ignore_errors=True)
    floor = n / 2
    ok = len(caught) >= floor
    note = (f"total={n} caught={len(caught)} floor={floor:g} verdict={'met' if ok else 'unmet'} "
            f"baseline_clean={clean}")
    if missed:
        note += f" missed={missed[:4]}"
    if not ok:
        note = "MUTATION DEFECT " + note
    return ok, note


# ---- legs that keep the imported semantics -------------------------------------------------------

def v2(lane, pkg, work, p10):
    if not pkg.pinned:
        return False, "filler mode: the gate is not run on the control package"
    if sha256(pathlib.Path(lane) / GATE_REL) != GATE_SHA256:
        return False, "gate not at its round-45 freeze digest"
    s = dict(pkg.spec)
    s["receipt_sha256"] = sha256(pkg.receipt) or "absent"
    eff = pathlib.Path(work) / "pkg-spec-r49-effective.json"
    eff.write_text(json.dumps(s))
    argv = [sys.executable, str(pathlib.Path(lane) / GATE_REL), "package", "--root", str(lane),
            "--spec", str(eff), "--require-clean-tree"]
    if p10:
        argv.append("--rerun")
    r = subprocess.run(argv, capture_output=True, text=True, timeout=1800)
    for line in r.stdout.splitlines():
        print("    gate: " + line)
    return r.returncode == 0, (f"spec=frozen gate=frozen p10={'enabled' if p10 else 'disabled'} "
                               f"gate_exit={r.returncode}")


def v5(lane, pkg, pins):
    if not pkg.pinned:
        return False, "filler mode: no probe is pinned for the control package"
    probe_pin, dry_pin = pins
    if not probe_pin or not dry_pin or str(probe_pin).startswith("<"):
        return False, "probe/dry pins pending (stage-2 placeholders)"
    if sha256(pathlib.Path(lane) / PROBE_REL) != probe_pin or sha256(pkg.dry) != dry_pin:
        return False, "probe or dry table not at its freeze digest"
    r = subprocess.run([sys.executable, str(pathlib.Path(lane) / PROBE_REL), "--lane", str(lane), "--dry"],
                       capture_output=True, text=True, timeout=120)
    same = r.returncode == 0 and r.stdout == pkg.dry.read_text()
    return same, f"probe=frozen dry_byte_equal={same}"


def v13(lane, work, m):
    try:
        f = m.filler_pkg(pathlib.Path(lane))
    except (ValueError, OSError) as e:
        return False, f"filler package unusable: {e}"
    res = run_legs(lane, f, work, FILLER_LEGS, m, prefix="    filler: ")
    defects = [n for n, ok, _ in res if not ok]
    sub = [n for n in defects if n in SUBSTANTIVE]
    ok = len(sub) >= 3
    return ok, f"filler_checks={len(res)} defects={len(defects)} substantive={','.join(sub) or 0}"


def run_legs(lane, pkg, work, which, m, pins=None, prefix="", quiet=False):
    table = {
        "V1": lambda: m.v1(pkg),
        "V2": lambda: v2(lane, pkg, work, p10=False),
        "V3": lambda: m.v3(pkg),
        "V4": lambda: m.v4(pkg),
        "V5": lambda: v5(lane, pkg, pins),
        "V6": lambda: m.v6(pkg),
        "V7": lambda: m.v7(pkg),
        "V7P": lambda: v7p(pkg, m),
        "V8": lambda: m.v8(pathlib.Path(lane), pkg),
        "V9": lambda: m.v9(pkg),
        "V10": lambda: m.v10(pkg),
        "V11": lambda: m.v11(pkg, work),
        "V12": lambda: m.v12(pkg),
        "V13": lambda: v13(lane, work, m),
        "V14": lambda: v14(lane, pkg, work, m),
        "V15": lambda: v15(lane, pkg, m),
    }
    out = []
    for name in which:
        try:
            ok, note = table[name]()
        except Exception as e:  # a check that cannot run is a defect, never a pass
            ok, note = False, f"error {type(e).__name__}: {e}"
        if not quiet:
            print(f"{prefix}{name} {'ok' if ok else 'DEFECT'} {note}")
        out.append((name, ok, note))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="round-49 C2 counter candidate (TB2 polyglot-c-py)")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--filler", action="store_true",
                    help="measure the plans/filler46/ control package instead of the package under test")
    ap.add_argument("--no-p10", action="store_true", dest="no_p10",
                    help="control mode: run the gate with P10 (fresh probe re-run) disabled")
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    head = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True)
    print(f"REV {head.stdout.strip() if head.returncode == 0 else 'not-a-git-worktree'}")
    dirty = subprocess.run(["git", "-C", str(lane), "status", "--porcelain"], capture_output=True, text=True)
    print(f"REV_DIRTY {len([l for l in dirty.stdout.splitlines() if l])}")
    if not a.no_p10:
        print("SETUP wave-1 control instrument: scored mode (P10 enabled) refused; pass --no-p10")
        print("checks=0 defects=0")
        print("PREDICATE R49-C2 not-run")
        return 2
    print("MODE control --no-p10 (gate P10/fresh-probe leg disabled, frozen V8 fix)")
    try:
        m = load_r46(lane)
    except (ValueError, OSError) as e:
        print(f"SETUP {e}")
        print("checks=0 defects=0")
        print("PREDICATE R49-C2 fail")
        return 2
    print(f"COUNTER imports {R46_REL} sha256={R46_SHA256} (pinned)")
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    with __import__("tempfile").TemporaryDirectory(prefix="k49-c2-", dir=a.work) as work:
        if a.filler:
            which = FILLER_LEGS
            try:
                pkg = m.filler_pkg(lane)
                pins = None
            except (ValueError, OSError) as e:
                print(f"FILLER unusable: {e}")
                print(f"checks={len(which)} defects={len(which)}")
                print("PREDICATE R49-C2 fail")
                return 1
            print("PINS spec=filler46 (control package)")
        else:
            which = PACKAGE_LEGS
            try:
                pkg, pins, src = load_pkg(lane, m)
            except (ValueError, OSError, KeyError, json.JSONDecodeError) as e:
                print(f"PACKAGE unreadable: {e}")
                defects = 0
                for name in which:
                    print(f"{name} DEFECT package unreadable: {e}")
                    defects += 1
                print(f"checks={len(which)} defects={defects}")
                print("PREDICATE R49-C2 fail")
                return 1
            print(f"PINS spec={src} probe={str(pins[0])[:8]} dry={str(pins[1])[:8]}")
        res = run_legs(lane, pkg, work, which, m, pins=pins)
        defects = sum(1 for _n, ok, _note in res if not ok)
        content = [n for n, ok, _note in res if not ok and n in SUBSTANTIVE]
        print(f"content_defects={len(content)} ({','.join(content) or 0})")
        print(f"checks={len(res)} defects={defects}")
        print(f"PREDICATE R49-C2 {'pass' if defects == 0 else 'fail'}")
        return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

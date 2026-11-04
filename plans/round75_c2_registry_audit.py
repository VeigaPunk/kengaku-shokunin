#!/usr/bin/env python3
"""R75-C2 counter — registry audit whose self-evidence is derived, attributed and revision-stamped.

Frozen before data on 2026-11-04 (L1 KengakuR75); see plans/round-75-claims.md §R75-C2.
Supersedes `plans/round74_c2_registry_audit.py` (which stays committed and re-derivable); this
counter imports its parsers and fixture builders and prices three things round 74 could not.

    python3 plans/round75_c2_registry_audit.py --lane . --mutants --check-stamps corpus/evidence/round75
    python3 plans/round75_c2_registry_audit.py --control-attribute --work DIR
    python3 plans/round75_c2_registry_audit.py --selftest --work DIR

Why this counter exists (round-74 verifier spot-check R74-D4 and R74-D1):
(a) R74-D4 — `--mutants` counted a mutant killed on *any* defect (`killed += int(sum(len(x) …) > 0)`)
    and printed hard-coded `invalid=0 null_detected=1`; no null arm ran, so a mutant killed by the
    wrong finding was indistinguishable from a correct kill. This counter prices every mutant against
    its **expected finding id**, runs a null arm that must survive, and derives every tally.
(b) R74-D1 — receipts carried no measured-revision line and one was produced over a pre-commit
    worktree. This counter stamps `LANE_TIP <commit>` + `WORKTREE clean|dirty` on its own output and
    `--check-stamps` refuses a receipt whose stamp is absent, unresolvable or not an ancestor of the
    measured branch tip (`git rev-parse --verify <rev>^{commit}`, S251).
(c) S250's reject-flip (round 74 lesson) — a flag string in a script body does not prove `argparse`
    acceptance. When a script declares its CLI through `add_argument`, a flag now counts only if an
    `add_argument` call declares it; string presence elsewhere is a named defect
    (`:entry:flag-not-declared:`), not a pass. Scripts with no `add_argument` call keep round 74's
    text-presence rule and are counted in `TEXT-FALLBACK n=` so the weaker evidence is visible.

Predicate (one command, `--lane . --mutants --check-stamps corpus/evidence/round75`):
  INSTRUMENTS/PARSED/D1–D4/MALFORMED  round-74 legs, 0 defects
  MUTANTS total=9 killed=8 expected_matched=8 wrong_id=0 survived=0 null_arms=1 null_survived=1
  STAMPS files=N stamped=N unstamped=0 unresolved=0 not_ancestor=0
  PREDICATE R75-C2 pass
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load_r74():
    spec = importlib.util.spec_from_file_location("r74audit", HERE / "round74_c2_registry_audit.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("round74_c2_registry_audit.py not found beside this file")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R74 = _load_r74()
HEX40 = re.compile(r"^[0-9a-f]{40}$")
STAMP = re.compile(r"^LANE_TIP (\S+)$", re.M)


# --------------------------------------------------------------------------- S250 flip

def cli_declarations(script_text: str) -> tuple[bool, set[str], set[str]]:
    """(declares argparse CLI, flags declared by add_argument, all string literals)."""
    try:
        tree = ast.parse(script_text)
    except SyntaxError:
        return False, set(), set()
    declared: set[str] = set()
    literals: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            literals.add(node.value)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument":
            for arg in list(node.args) + [kw.value for kw in node.keywords]:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    declared.update(re.findall(r"--[a-z][a-z0-9-]*", arg.value))
    return bool(declared), declared, literals


def flag_legs(lane: Path, rows: list[list[str]]) -> tuple[list[str], int]:
    """Defects (new class only) and the count of flags accepted on text presence alone."""
    defects: list[str] = []
    fallback = 0
    for row in rows:
        name, entry = (row[0] if row else "<empty>"), (row[2] if len(row) > 2 else "")
        script = R74.entry_script(entry)
        if not script or not (lane / script).exists():
            continue  # D1 / script-absent already priced by the round-74 legs
        text = (lane / script).read_text(errors="replace")
        has_cli, declared, literals = cli_declarations(text)
        if not has_cli:
            continue
        for flag in R74.command_flags(entry):
            if flag in declared:
                continue
            if any(flag in literal for literal in literals):
                defects.append(f"{name}:entry:flag-not-declared:{flag}")
            elif flag in text:
                defects.append(f"{name}:entry:flag-comment-only:{flag}")
            # absent entirely -> the round-74 `unbacked-flag` leg owns it
    return defects, fallback


def text_fallback_count(lane: Path, rows: list[list[str]]) -> int:
    """Rows whose declared entry flags were accepted only because no add_argument call exists."""
    n = 0
    for row in rows:
        entry = row[2] if len(row) > 2 else ""
        script = R74.entry_script(entry)
        if not script or not (lane / script).exists():
            continue
        has_cli, _, _ = cli_declarations((lane / script).read_text(errors="replace"))
        if not has_cli and R74.command_flags(entry):
            n += 1
    return n


# --------------------------------------------------------------------------- revisions

def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


def lane_tip(lane: Path, rev: str) -> tuple[str, bool]:
    tip = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    resolved = tip.stdout.strip() if tip.returncode == 0 and tip.stdout.strip() else "unknown"
    dirty = bool(git(lane, "status", "--porcelain", "--untracked-files=no").stdout.strip())
    return resolved, dirty


def check_stamps(lane: Path, evidence: Path, rev: str) -> tuple[list[str], str]:
    files = sorted(evidence.glob("*.txt")) if evidence.is_dir() else []
    defects: list[str] = []
    stamped = unresolved = not_ancestor = unstamped = 0
    tip, _ = lane_tip(lane, rev)
    for path in files:
        m = STAMP.search(path.read_text(errors="replace"))
        if not m or m.group(1) == "unknown":
            defects.append(f"UNSTAMPED {path.name}")
            unstamped += 1
            continue
        rev_id = m.group(1)
        if not HEX40.match(rev_id):
            defects.append(f"STAMP-MALFORMED {path.name} {rev_id[:12]}")
            unresolved += 1
            continue
        if git(lane, "rev-parse", "--verify", "--quiet", f"{rev_id}^{{commit}}").returncode != 0:
            defects.append(f"REVISION:unresolvable {path.name} {rev_id[:12]}")
            unresolved += 1
            continue
        if tip != "unknown" and git(lane, "merge-base", "--is-ancestor", rev_id, tip).returncode != 0:
            defects.append(f"REVISION:not-ancestor {path.name} {rev_id[:12]}")
            not_ancestor += 1
            continue
        stamped += 1
    line = (
        f"STAMPS files={len(files)} stamped={stamped} unstamped={unstamped} "
        f"unresolved={unresolved} not_ancestor={not_ancestor}"
    )
    return defects, line


# --------------------------------------------------------------------------- mutants

def mutate(lane: Path, work: Path) -> tuple[list[tuple[str, str, list[str]]], list[str], tuple[str, str, list[str]]]:
    """(mutants, null-arm defects, off-target arm) — every fixture built under `work`."""
    child = work / "mutants_r75"
    if child.exists():
        shutil.rmtree(child)
    child.mkdir(parents=True)

    def defects_of(root: Path) -> list[str]:
        checks, _, _, _ = R74.run_checks(root)
        out = [d for _, dl in checks for d in dl]
        out += flag_legs(root, R74.parse_rows(R74.registry_block((root / R74.SKILL_REL).read_text()))[0])[0]
        return out

    # (name, expected finding id, fixture kwargs or extra script)
    specs: list[tuple[str, str, dict]] = [
        ("M1-entry-absent", ":entry:script-absent:", {"extra_row": R74.row_text("tool-m", "plans/nonexistent.py")}),
        ("M2-selftest-absent", ":self-test:script-absent:",
         {"extra_row": R74.row_text("tool-m", "plans/tool_b.py", selftest="`python3 plans/ghost.py --selftest`")}),
        ("M3-nine-cells", "MALFORMED-ROW columns=9", {"malformed_line": "| a | b | c | d | e | f | g | h | i |"}),
        ("M4-seven-cells", "MALFORMED-ROW columns=7", {"malformed_line": "| a | b | c | d | e | f | g |"}),
        ("M5-duplicate", "DUPLICATE-ROW", {"second_row": R74.row_text("tool-a", "plans/tool_b.py")}),
        ("M6-flag-absent", ":entry:unbacked-flag:", {"extra_row": R74.row_text("tool-m", "plans/tool_b.py --ghostflag")}),
        ("M7-errata-contradiction", "contradictory-revision", {"errata": "contradictory"}),
        ("M8-flag-literal-not-declared", ":entry:flag-not-declared:", {"extra_script": True}),
        ("M9-empty-owner-cell", ":owner:empty",
         {"extra_row": "| `tool-m` | gate | `python3 plans/tool_b.py` | `0` ok · `1` failed | `python3 plans/tool_b.py --selftest` | pinned | read-only | |\n"}),
    ]
    results: list[tuple[str, str, list[str]]] = []
    for name, expected, kwargs in specs:
        root = child / name
        script = kwargs.pop("extra_script", False)
        R74.build_fixture(root, **kwargs)
        if script:
            # argparse script whose docstring names a flag it never registers: round 74 passes it
            # (substring present), round 75 must refuse it (S250 flip).
            (root / "plans" / "tool_doc.py").write_text(
                '"""Tool that accepts --strict according to this sentence."""\n'
                "import argparse\np = argparse.ArgumentParser()\np.add_argument('--lane')\n"
            )
            block = (root / R74.SKILL_REL).read_text()
            block += R74.row_text("tool-doc", "plans/tool_doc.py --strict")
            (root / R74.SKILL_REL).write_text(block)
        results.append((name, expected, defects_of(root)))

    null_dir = child / "N-null-arm"
    R74.build_fixture(null_dir, extra_row=R74.row_text("tool-n", "plans/tool_b.py", pinned="pinned bytes  "))
    null_text = (null_dir / R74.SKILL_REL).read_text() + "\n"
    (null_dir / R74.SKILL_REL).write_text(null_text)
    null_defects = defects_of(null_dir)

    # Off-target arm (the R74-D4 control): the M3 fixture bytes are re-labelled as if the mutation
    # under test were an unhooked entry flag. Round 74's any-defect metric calls that a kill; the
    # attributed metric must call it a wrong-id kill on the *same* bytes.
    off_dir = child / "X-off-target"
    R74.build_fixture(off_dir, malformed_line="| a | b | c | d | e | f | g | h | i |")
    off_target = ("X-off-target", ":entry:unbacked-flag:", defects_of(off_dir))
    shutil.rmtree(child, ignore_errors=True)
    return results, null_defects, off_target


# --------------------------------------------------------------------------- verdicts

def audit_verdict(lane: Path) -> tuple[list[str], int, int, int]:
    checks, rows, scripts, parsed = R74.run_checks(lane)
    block = R74.registry_block((lane / R74.SKILL_REL).read_text(errors="replace"))
    parsed_rows, _ = R74.parse_rows(block)
    extra, _ = flag_legs(lane, parsed_rows)
    defects = [d for _, dl in checks for d in dl] + extra
    for leg, dl in checks:
        print(f"{leg} {'ok' if not dl else 'defect'} n={len(dl)}")
        for d in dl:
            print(f"  DEFECT {d}")
    print(f"FLAGS {'ok' if not extra else 'defect'} n={len(extra)}")
    for d in extra:
        print(f"  DEFECT {d}")
    print(f"TEXT-FALLBACK n={text_fallback_count(lane, parsed_rows)}")
    print(f"INSTRUMENTS total={scripts} rows={rows}")
    print(f"PARSED scripts={scripts} failed={scripts - parsed}")
    print(f"MISMATCH {len(defects)}")
    print(f"DEFECTS n={len(defects)}")
    return defects, rows, scripts, parsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lane", type=Path, default=Path("."), help="Lane root directory")
    parser.add_argument("--rev", default="master", help="Branch whose tip is the measured revision")
    parser.add_argument("--mutants", action="store_true", help="Run the attributed mutant matrix")
    parser.add_argument("--check-stamps", type=Path, default=None, metavar="DIR", help="Audit receipt stamps")
    parser.add_argument("--control-attribute", action="store_true", help="Run the off-target-kill control")
    parser.add_argument("--selftest", action="store_true", help="Run the fixture battery")
    parser.add_argument("--work", type=Path, default=Path("/fast/scratch/hyaku/kengaku-r75/c2"), help="Scratch directory")
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    tip, dirty = lane_tip(args.lane, args.rev)
    print(f"LANE_TIP {tip}")
    print(f"WORKTREE {'dirty' if dirty else 'clean'}")

    if args.selftest:
        fails = 0
        # arm 1: the off-target fixture must be a wrong-id kill, not a kill
        results, null_defects, off = mutate(args.lane, args.work)
        ok = off[1] not in " ".join(off[2]) and bool(off[2])
        print(f"SELFTEST {'ok' if ok else 'FAIL'} off-target: expected {off[1]} absent, other defects {len(off[2])}")
        fails += 0 if ok else 1
        # arm 2: the null arm must survive
        ok = not null_defects
        print(f"SELFTEST {'ok' if ok else 'FAIL'} null-arm: defects={len(null_defects)}")
        fails += 0 if ok else 1
        # arm 3: every real mutant must be caught on its expected id
        mismatched = [n for n, exp, defs in results if exp not in " ".join(defs)]
        ok = not mismatched
        print(f"SELFTEST {'ok' if ok else 'FAIL'} expected-id: mismatched={len(mismatched)}")
        fails += 0 if ok else 1
        # arm 4: stamps — unstamped receipt refused, stamped+ancestor accepted
        stamp_dir = args.work / "stamps_r75"
        if stamp_dir.exists():
            shutil.rmtree(stamp_dir)
        stamp_dir.mkdir(parents=True)
        (stamp_dir / "unstamped.txt").write_text("VERDICT ok\n")
        tip, _ = lane_tip(args.lane, args.rev)
        (stamp_dir / "stamped.txt").write_text(f"LANE_TIP {tip}\nVERDICT ok\n")
        defects, line = check_stamps(args.lane, stamp_dir, args.rev)
        ok = len(defects) == 1 and defects[0].startswith("UNSTAMPED unstamped.txt") and "stamped=1" in line
        print(f"SELFTEST {'ok' if ok else 'FAIL'} stamps: {line} defects={len(defects)}")
        fails += 0 if ok else 1
        print(f"SELFTEST arms=4 failures={fails} ok={fails == 0}")
        shutil.rmtree(args.work / "stamps_r75", ignore_errors=True)
        return 0 if fails == 0 else 1

    if args.control_attribute:
        results, null_defects, off = mutate(args.lane, args.work)
        # Round 74's metric: any defect kills. Round 75's: only the expected id kills.
        r74_killed = sum(1 for _, _, defs in results if defs) + int(bool(off[2]))
        r75_matched = sum(1 for _, exp, defs in results if exp in " ".join(defs)) + int(off[1] in " ".join(off[2]))
        print(f"R74-METRIC killed={r74_killed}/{len(results) + 1} (any-defect counting)")
        print(f"R75-METRIC expected_matched={r75_matched}/{len(results) + 1} wrong_id={len(results) + 1 - r75_matched}")
        print(f"OFF-TARGET {off[0]} expected={off[1]} defects={len(off[2])} matched={off[1] in ' '.join(off[2])}")
        print(f"NULL-ARM defects={len(null_defects)}")
        discriminated = r75_matched < r74_killed and not null_defects
        print(f"PREDICATE R75-C2-control {'pass' if discriminated else 'fail'}")
        return 0 if discriminated else 1

    if not (args.lane / R74.SKILL_REL).exists():
        print(f"SETUP ERROR: {R74.SKILL_REL} absent under {args.lane}", file=sys.stderr)
        return 2

    defects, rows, scripts, parsed = audit_verdict(args.lane)
    failures = len(defects)
    if args.mutants:
        results, null_defects, _ = mutate(args.lane, args.work)
        matched = [n for n, exp, defs in results if exp in " ".join(defs)]
        print(
            f"MUTANTS real={len(results)} expected_matched={len(matched)} "
            f"wrong_id={len(results) - len(matched)} survived={len(results) - len(matched)} "
            f"null_arms=1 null_survived={0 if null_defects else 1} total={len(results) + 1}"
        )
        failures += (len(results) - len(matched)) + (1 if null_defects else 0)
    if args.check_stamps is not None:
        sdefects, line = check_stamps(args.lane, args.check_stamps, args.rev)
        print(line)
        for d in sdefects:
            print(f"  DEFECT {d}")
        failures += len(sdefects)
    print(f"PREDICATE R75-C2 {'pass' if failures == 0 else 'fail'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

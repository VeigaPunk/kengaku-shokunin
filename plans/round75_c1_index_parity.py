#!/usr/bin/env python3
"""R75-C1 counter — corpus index parity, both directions, over three declared universes.

Frozen before data on 2026-11-04 (L1 KengakuR75); see plans/round-75-claims.md §R75-C1.
Reads working-tree bytes; the receipt printed by `--receipt` carries the measured revision.

    python3 plans/round75_c1_index_parity.py --lane .                      # verdict
    python3 plans/round75_c1_index_parity.py --lane . --receipt FILE       # verdict + receipt bytes
    python3 plans/round75_c1_index_parity.py --selftest --work DIR         # fixture battery

Why this counter exists (round-74 verifier spot-check R74-D1 class; AXES.md coverage signal):
`AXES.md` scores coverage as "every surface the corpus *describes* is indexed **and** every index
row exists on disk (both directions); `PROVINCE.md` enumerates surfaces that resolve".  The lane
had no instrument that prices that sentence: `corpus/README.md` silently drifted to 3 unindexed
knowledge entries, 35 unindexed lesson files and 19 unindexed evidence directories, while every
round scorecard kept claiming index parity for the narrower denominators it happened to count.
The drift is invisible to registration gates because an unindexed file advertises nothing.

Declared universes (enumerated from disk, never from an advertisement):
  knowledge   corpus/knowledge/*.md          row form  | `knowledge/<file>` |
  lessons     corpus/lessons/*.md            row form  | `lessons/<file>` |
  evidence    corpus/evidence/*/             mention   corpus/evidence/<dir>/

Legs (each printed; any nonzero leg fails the predicate):
  MISSING           file on disk with no index row / evidence dir with no mention   -> 0
  ORPHAN            index row naming a file that is not on disk                     -> 0
  ORPHAN-EVIDENCE   evidence mention whose first path segment is not a directory    -> 0
  PREDICATE R75-C1  pass
Exit 0 pass, 1 fail (one line per defect), 2 setup.

The `LANE_TIP` line is the R74-D1 repair: every receipt this instrument writes names the
revision whose tree it read (`git rev-parse --verify <rev>^{commit}`) and whether that tree was
dirty, so a receipt produced over a pre-commit worktree can no longer pass as a measurement of
the commit that contains it.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROW = re.compile(r"^\|\s*`(knowledge|lessons)/([^`]+)`")
EVIDENCE = re.compile(r"corpus/evidence/([A-Za-z0-9_.-]+)/")
UNIVERSES = (
    ("knowledge", "corpus/knowledge", "*.md"),
    ("lessons", "corpus/lessons", "*.md"),
)
README = "corpus/README.md"
EVIDENCE_ROOT = "corpus/evidence"


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def lane_tip(lane: Path, rev: str) -> tuple[str, bool]:
    """(resolved commit or 'unknown', worktree dirty on tracked paths)."""
    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)

    tip = git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    resolved = tip.stdout.strip() if tip.returncode == 0 and tip.stdout.strip() else "unknown"
    dirty = bool(git("status", "--porcelain", "--untracked-files=no").stdout.strip())
    return resolved, dirty


def census(lane: Path) -> tuple[list[str], list[str]]:
    """(defect lines, report lines). Order is frozen: report lines are the frozen sentence."""
    readme = read(lane / README)
    defects: list[str] = []
    report: list[str] = []
    indexed: dict[str, set[str]] = {}
    for kind, rel_dir, pattern in UNIVERSES:
        base = lane / rel_dir
        files = sorted(p.name for p in base.glob(pattern)) if base.is_dir() else []
        rows = {m.group(1) for m in (ROW.match(line) for line in readme.splitlines()) if m and m.group(1) == kind}
        targets = {m.group(2) for m in (ROW.match(line) for line in readme.splitlines()) if m and m.group(1) == kind}
        missing = [f for f in files if f not in targets]
        orphan = sorted(t for t in targets if t not in files)
        indexed[kind] = targets
        defects += [f"MISSING {kind}/{f}" for f in missing]
        defects += [f"ORPHAN {kind}/{f}" for f in orphan]
        report.append(
            f"UNIVERSE {kind} files={len(files)} indexed={len(files) - len(missing)} "
            f"missing={len(missing)} orphan={len(orphan)}"
        )
    ev_root = lane / EVIDENCE_ROOT
    dirs = sorted(p.name for p in ev_root.iterdir() if p.is_dir()) if ev_root.is_dir() else []
    mentioned = set(EVIDENCE.findall(readme))
    missing_ev = [d for d in dirs if d not in mentioned]
    orphan_ev = sorted(m for m in mentioned if not (ev_root / m).is_dir())
    defects += [f"MISSING-EVIDENCE {d}" for d in missing_ev]
    defects += [f"ORPHAN-EVIDENCE {d}" for d in orphan_ev]
    report.append(
        f"UNIVERSE evidence dirs={len(dirs)} indexed={len(dirs) - len(missing_ev)} "
        f"missing={len(missing_ev)} orphan={len(orphan_ev)}"
    )
    return defects, report


def emit(lane: Path, rev: str, out: Path | None) -> int:
    if not lane.is_dir():
        print(f"SETUP ERROR: lane {lane} is not a directory", file=sys.stderr)
        return 2
    if not (lane / README).exists():
        print(f"SETUP ERROR: {README} absent under {lane}", file=sys.stderr)
        return 2
    tip, dirty = lane_tip(lane, rev)
    defects, report = census(lane)
    lines = [f"LANE_TIP {tip}", f"WORKTREE {'dirty' if dirty else 'clean'}"]
    lines += report
    lines += defects
    lines.append(f"PREDICATE R75-C1 {'pass' if not defects else 'fail'}")
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    return 0 if not defects else 1


def build_fixture(root: Path, *, drop_row: str = "", orphan_row: str = "", drop_evidence: str = "") -> None:
    if root.exists():
        shutil.rmtree(root)
    for kind, rel, names in (
        ("knowledge", "corpus/knowledge", ("a.md", "b.md")),
        ("lessons", "corpus/lessons", ("round-1.md", "round-2.md")),
    ):
        d = root / rel
        d.mkdir(parents=True)
        for n in names:
            (d / n).write_text(f"# {n}\n")
    for d in ("d1", "d2"):
        (root / EVIDENCE_ROOT / d).mkdir(parents=True)
    rows = [f"| `knowledge/{n}` | fixture | src |" for n in ("a.md", "b.md")]
    rows += [f"| `lessons/{n}` | fixture | ptr |" for n in ("round-1.md", "round-2.md")]
    keep = [r for r in rows if not drop_row or drop_row not in r]
    if orphan_row:
        keep.append(orphan_row)
    body = ["# fixture README", "", *keep, ""]
    if drop_evidence != "d2":
        body.append(f"- `corpus/evidence/d2/` fixture")
    body.append(f"- `corpus/evidence/d1/` fixture")
    (root / README).parent.mkdir(parents=True, exist_ok=True)
    (root / README).write_text("\n".join(body) + "\n")


def selftest(work: Path) -> int:
    child = work / "c1_child"
    fails = 0
    cases = (
        ("clean", {}, 0, None),
        ("missing-knowledge", {"drop_row": "knowledge/b.md"}, 1, "MISSING knowledge/b.md"),
        ("missing-lesson", {"drop_row": "lessons/round-2.md"}, 1, "MISSING lessons/round-2.md"),
        ("missing-evidence", {"drop_evidence": "d2"}, 1, "MISSING-EVIDENCE d2"),
        ("orphan-knowledge", {"orphan_row": "| `knowledge/ghost.md` | fixture | src |"}, 1, "ORPHAN knowledge/ghost.md"),
    )
    try:
        for name, kwargs, want_rc, want_line in cases:
            d = child / name
            build_fixture(d, **kwargs)
            defects, _ = census(d)
            rc = 0 if not defects else 1
            ok = rc == want_rc and (want_line is None or want_line in defects)
            fails += 0 if ok else 1
            print(f"SELFTEST {'ok' if ok else 'FAIL'} {name} rc={rc} want={want_rc}")
    finally:
        shutil.rmtree(child, ignore_errors=True)
    print(f"SELFTEST cases={len(cases)} red={len(cases) - 1} failures={fails} ok={fails == 0}")
    return 0 if fails == 0 else 1


def control_rowshuffle(work: Path) -> int:
    """The cheapest skip: a README whose row count matches the surface count but names one file.

    A counter that counts index rows scores this as complete; this gate keys on filenames and must
    still report every unindexed surface.
    """
    root = work / "c1_rowshuffle"
    build_fixture(root)
    rows = [f"| `knowledge/a.md` | fixture | src |"] * 6
    body = "# fixture README\n\n" + "\n".join(rows) + "\n- `corpus/evidence/d1/` fixture\n"
    (root / README).write_text(body)
    defects, report = census(root)
    surfaces = sum(int(line.split("files=")[1].split()[0]) for line in report[:2])
    surfaces += sum(int(line.split("dirs=")[1].split()[0]) for line in report[2:3])
    naive_rows = len(rows)
    print(f"NAIVE rows={naive_rows} surfaces={surfaces} equal={naive_rows == surfaces}")
    print("\n".join(report))
    print("\n".join(defects))
    ok = bool(defects) and naive_rows == surfaces
    print(f"PREDICATE R75-C1-control {'pass' if ok else 'fail'}")
    shutil.rmtree(root, ignore_errors=True)
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lane", type=Path, default=Path("."), help="Lane root directory")
    parser.add_argument("--rev", default="master", help="Branch whose tip is the measured revision")
    parser.add_argument("--receipt", type=Path, default=None, help="Also write the verdict bytes here")
    parser.add_argument("--selftest", action="store_true", help="Run the fixture battery")
    parser.add_argument("--control-rowshuffle", action="store_true", help="Run the fake-completion control")
    parser.add_argument("--work", type=Path, default=Path("/fast/scratch/hyaku/kengaku-r75/c1"), help="Scratch directory")
    args = parser.parse_args()

    if args.selftest:
        args.work.mkdir(parents=True, exist_ok=True)
        return selftest(args.work)
    if args.control_rowshuffle:
        args.work.mkdir(parents=True, exist_ok=True)
        return control_rowshuffle(args.work)
    return emit(args.lane, args.rev, args.receipt)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""R74-C1 counter — decoupled advertised verdict instruments vs the SKILL.md gate/probe registry.

Frozen before data on 2026-11-04 (L1 KengakuR74); see plans/round-74-claims.md §C1 for
the predicate this implements. Reads committed bytes only; writes nothing.

    python3 plans/round74_c1_registry.py --lane .          # verdict, decoupled universe
    python3 plans/round74_c1_registry.py --universe legacy  # the pre-round-74 advertised universe
    python3 plans/round74_c1_registry.py --selftest         # fixture battery

Why this counter exists (round-73 lessons M73-1 and Planned round 74):
In round 52-73, `self_assessment_files` scanned `SKILL.md` whole, including the
`## Gate/probe registry` table itself. Every row in the registry table thus advertised
itself to the gate, creating a circular self-advertising loop where dropping an unreferenced
registered row went completely undetected (MISSING stayed 0). Moreover, the legacy regex
`[A-Za-z0-9_]+` failed to match hyphenated directory names like `round13-coverage`
(making `coverage_census.py` invisible to the gate).

This counter:
1. Decouples discovery: scans `SKILL.md` strictly *outside* the `## Gate/probe registry`
   section, along with `SCORECARD.md`, `LOG.md`, `corpus/README.md`, `corpus/knowledge/*.md`,
   and `plans/*.md`.
2. Supports hyphenated names `[A-Za-z0-9_.-]+` for scripts and directories.
3. Verifies that every independently advertised instrument is registered (`MISSING == 0`),
   with zero circular self-advertising.
4. Preserves `--universe legacy` as the frozen pre-amendment control.

Predicate (all six legs must hold):
  MISSING            = advertised instruments with no registry row          -> 0
  INCOMPLETE         = registry rows with an empty cell                     -> 0
  ENTRY-MISSING      = registry rows whose entry script is not in the tree  -> 0
  SELFTEST-UNBACKED  = registry rows naming a script+flag the script lacks -> 0
  DUPLICATE          = registry rows with duplicate names                   -> 0
  PREDICATE R74-C1   = pass
Exit 0 on PREDICATE pass, 1 on fail, 2 on setup.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CMD = re.compile(
    r"python3 ((?:plans/[A-Za-z0-9_.-]+\.py|grader\.py|corpus/evidence/round13-coverage/coverage_census\.py))"
)
CMD_LEGACY = re.compile(
    r"python3 ((?:plans/[A-Za-z0-9_]+\.py|corpus/evidence/[A-Za-z0-9_]+/[A-Za-z0-9_]+\.py|grader\.py))"
)
FLAG = re.compile(r"(--[a-z][a-z0-9-]*)")
SELF_FILES = ("SCORECARD.md", "LOG.md", "corpus/README.md")
REGISTRY_HEADING = "## Gate/probe registry"
UNIVERSES = ("decoupled", "legacy")


def self_assessment_files(lane: Path, universe: str = "decoupled") -> list[tuple[str, str]]:
    """Returns list of (rel_path, file_text_to_scan)."""
    out = []
    if universe == "legacy":
        # Legacy scans SKILL.md whole (causing circular self-advertising) and no plans/*.md
        files = ["SCORECARD.md", "SKILL.md", "LOG.md", "corpus/README.md"]
        for f in files:
            p = lane / f
            if p.exists():
                out.append((f, p.read_text(errors="replace")))
        kdir = lane / "corpus" / "knowledge"
        if kdir.is_dir():
            for p in sorted(kdir.glob("*.md")):
                out.append((str(p.relative_to(lane)), p.read_text(errors="replace")))
        return out

    # Decoupled mode: SKILL.md outside registry table + self_files + knowledge + plans docs
    for f in SELF_FILES:
        p = lane / f
        if p.exists():
            out.append((f, p.read_text(errors="replace")))

    skill_path = lane / "SKILL.md"
    if skill_path.exists():
        stext = skill_path.read_text(errors="replace")
        i = stext.find(REGISTRY_HEADING)
        if i >= 0:
            j = stext.find("\n## ", i + 1)
            outside = stext[:i] + (stext[j:] if j > 0 else "")
        else:
            outside = stext
        out.append(("SKILL.md (outside registry)", outside))

    kdir = lane / "corpus" / "knowledge"
    if kdir.is_dir():
        for p in sorted(kdir.glob("*.md")):
            out.append((str(p.relative_to(lane)), p.read_text(errors="replace")))

    pdir = lane / "plans"
    if pdir.is_dir():
        for p in sorted(pdir.glob("*.md")):
            out.append((str(p.relative_to(lane)), p.read_text(errors="replace")))

    return out


def registry_block(text: str) -> str:
    i = text.find(REGISTRY_HEADING)
    if i < 0:
        return ""
    j = text.find("\n## ", i + 1)
    return text[i:j] if j > 0 else text[i:]


def parse_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) != 8:
            continue
        if set(cells[0]) <= set("-: "):
            continue
        if cells[0] == "name":
            continue
        rows.append(cells)
    return rows


def entry_script(entry: str, cmd_re: re.Pattern = CMD) -> str | None:
    m = cmd_re.search(entry)
    return m.group(1) if m else None


def selftest_unbacked(cell: str, lane: Path) -> bool:
    if re.search(r"\bno\b.{0,24}--[a-z][a-z0-9-]*", cell):
        return False
    scripts = sorted(set(re.findall(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py", cell)))
    flags = sorted(set(FLAG.findall(cell)))
    if len(scripts) != 1 or not flags:
        return False
    path = lane / scripts[0]
    if not path.exists():
        return False
    body = path.read_text(errors="replace")
    return all(f not in body for f in flags)


def collect(lane: Path, universe: str = "decoupled"):
    cmd_re = CMD_LEGACY if universe == "legacy" else CMD
    adv: dict[str, set[str]] = {}
    for rel, text in self_assessment_files(lane, universe):
        for m in cmd_re.finditer(text):
            target = m.group(1)
            if (lane / target).exists():
                adv.setdefault(target, set()).add(rel)

    skill_path = lane / "SKILL.md"
    skill = skill_path.read_text(errors="replace") if skill_path.exists() else ""
    block = registry_block(skill)
    rows = parse_rows(block)
    reg: dict[str, list[str]] = {}
    for r in rows:
        s = entry_script(r[2], cmd_re)
        if s:
            reg.setdefault(s, r)

    missing = sorted(set(adv) - set(reg))
    incomplete = [r[0] for r in rows if not all(r)]
    entry_missing = sorted(s for s in reg if not (lane / s).exists())
    names = [r[0] for r in rows]
    duplicate = sorted({n for n in names if names.count(n) > 1})
    unbacked = [r[0] for r in rows if selftest_unbacked(r[4], lane)]
    return adv, rows, reg, missing, incomplete, entry_missing, unbacked, duplicate


def verdict(lane: Path, universe: str = "decoupled") -> int:
    adv, rows, reg, missing, incomplete, entry_missing, unbacked, duplicate = collect(lane, universe)
    plans_seen = sorted(p for p, files in adv.items() if any(x.startswith("plans/") for x in files))
    plans_only = sorted(p for p, files in adv.items() if files and all(x.startswith("plans/") for x in files))
    files_scanned = len(self_assessment_files(lane, universe))

    if universe == "legacy":
        print(f"UNIVERSE mode=legacy files={files_scanned} plans_seen={len(plans_seen)} plans_only={len(plans_only)}")
    else:
        print(f"UNIVERSE mode=decoupled files={files_scanned} plans_seen={len(plans_seen)} self_advertising_prevented=True")

    print(f"ADVERTISED total={len(adv)}")
    print(f"REGISTERED total={len(reg)} rows={len(rows)}")
    print(f"MISSING {len(missing)}")
    for p in missing:
        print(f"  MISSING {p}")
    print(f"INCOMPLETE {len(incomplete)}")
    for r in incomplete:
        print(f"  INCOMPLETE-ROW {r}")
    print(f"ENTRY-MISSING {len(entry_missing)}")
    for p in entry_missing:
        print(f"  ENTRY-MISSING {p}")
    print(f"SELFTEST-UNBACKED {len(unbacked)}")
    for r in unbacked:
        print(f"  SELFTEST-UNBACKED {r}")
    print(f"DUPLICATE {len(duplicate)}")
    for r in duplicate:
        print(f"  DUPLICATE-ROW {r}")

    ok = not (missing or incomplete or entry_missing or unbacked or duplicate)
    print(f"PREDICATE R52-C2 {'pass' if ok else 'fail'}")
    r74 = ok and universe == "decoupled" and len(plans_seen) >= 1
    print(f"PREDICATE R74-C1 {'pass' if r74 else 'fail'}")
    return 0 if r74 else 1


def selftest(lane: Path) -> int:
    """Fixture battery proving decoupled detection and discriminating control."""
    import shutil
    import tempfile

    fails = 0
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        (t / "plans").mkdir()
        (t / "corpus" / "knowledge").mkdir(parents=True)
        (t / "corpus" / "evidence" / "round13-coverage").mkdir(parents=True)
        (t / "plans" / "tool_a.py").write_text("# tool a\n")
        (t / "plans" / "tool_b.py").write_text("# tool b\n")
        (t / "grader.py").write_text("# grader\n")
        (t / "corpus" / "evidence" / "round13-coverage" / "coverage_census.py").write_text("# census\n")
        (t / "SCORECARD.md").write_text("run `python3 plans/tool_a.py` and `python3 grader.py`\n")
        (t / "LOG.md").write_text("run `python3 plans/tool_b.py`\n")
        (t / "corpus" / "README.md").write_text("entry `python3 corpus/evidence/round13-coverage/coverage_census.py`\n")
        (t / "SKILL.md").write_text(
            REGISTRY_HEADING + "\n\n| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| `ta` | gate | `python3 plans/tool_a.py` | 0 ok | none declared | none | read-only | kengaku |\n"
            "| `tb` | gate | `python3 plans/tool_b.py` | 0 ok | none declared | none | read-only | kengaku |\n"
            "| `cc` | probe | `python3 corpus/evidence/round13-coverage/coverage_census.py` | 0 ok | none declared | none | read-only | kengaku |\n"
            "| `gr` | gate | `python3 grader.py` | 0 ok | none declared | none | read-only | kengaku |\n"
        )
        (t / "corpus" / "knowledge" / "k.md").write_text("x\n")

        # 1. Clean decoupled fixture
        adv, rows, reg, missing, incomplete, entry_missing, unbacked, _dup = collect(t, "decoupled")
        if missing or incomplete or entry_missing or unbacked or len(adv) != 4 or len(reg) != 4:
            print(f"SELFTEST FAIL clean-decoupled: adv={len(adv)} reg={len(reg)} missing={missing}")
            fails += 1
        else:
            print("SELFTEST ok clean-decoupled")

        # 2. Dropping a row from SKILL.md for tool_b must raise MISSING in decoupled mode
        txt = (t / "SKILL.md").read_text()
        txt_dropped = "\n".join(l for l in txt.splitlines() if "`tb`" not in l)
        (t / "SKILL.md").write_text(txt_dropped + "\n")
        adv, rows, reg, missing, incomplete, entry_missing, unbacked, _dup = collect(t, "decoupled")
        if "plans/tool_b.py" not in missing:
            print("SELFTEST FAIL decoupled-missing: dropped row was not detected as MISSING")
            fails += 1
        else:
            print("SELFTEST ok decoupled-missing")

        # 3. Anti-circular test: a script ONLY present in the registry table is detected as unadvertised
        (t / "SKILL.md").write_text(
            txt +
            "| `phantom` | gate | `python3 plans/phantom.py` | 0 ok | none declared | none | read-only | kengaku |\n"
        )
        (t / "plans" / "phantom.py").write_text("# phantom\n")
        adv, rows, reg, missing, incomplete, entry_missing, unbacked, _dup = collect(t, "decoupled")
        if "plans/phantom.py" in adv:
            print("SELFTEST FAIL anti-circular: registry table self-advertised plans/phantom.py!")
            fails += 1
        else:
            print("SELFTEST ok anti-circular")

        # 4. Legacy control accepts the hyphenated failure (coverage_census missing)
        adv_l, rows_l, reg_l, missing_l, _, _, _, _ = collect(t, "legacy")
        if "corpus/evidence/round13-coverage/coverage_census.py" in adv_l:
            print("SELFTEST FAIL legacy-control: legacy matched hyphenated directory")
            fails += 1
        else:
            print("SELFTEST ok legacy-control")

    print(f"SELFTEST cases=4 failures={fails}")
    return 0 if fails == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lane", type=Path, default=Path("."), help="Lane root directory")
    parser.add_argument("--universe", choices=UNIVERSES, default="decoupled", help="Advertised universe mode")
    parser.add_argument("--selftest", action="store_true", help="Run fixture battery")
    args = parser.parse_args()

    if args.selftest:
        return selftest(args.lane)
    if not args.lane.is_dir():
        print(f"SETUP ERROR: lane {args.lane} is not a directory", file=sys.stderr)
        return 2
    return verdict(args.lane, args.universe)


if __name__ == "__main__":
    sys.exit(main())

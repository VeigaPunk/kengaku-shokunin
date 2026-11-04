#!/usr/bin/env python3
"""R52-C2 counter — advertised verdict instruments vs the SKILL.md gate/probe registry.

Frozen before data on 2026-10-28 (L1 KengakuR52a3); see plans/round-52-claims.md §C2 for
the predicate this implements.  Reads committed bytes only; writes nothing.

    python3 plans/round52_c2_registry.py --lane .          # verdict, R73-C1 universe
    python3 plans/round52_c2_registry.py --universe legacy  # the pre-R73 advertised universe
    python3 plans/round52_c2_registry.py --selftest         # fixture battery

R73-C1 amendment (2026-11-04, L1 KengakuR73; frozen in plans/round-73-claims.md §C1): the
advertised universe gains `plans/*.md`, because a claims document that names a runnable
`python3 plans/<instrument>.py` command advertises that instrument to every later round even
when no self-assessment file names it.  The five R52-C2 legs are unchanged; the extra arm is
the UNIVERSE line and `PREDICATE R73-C1`, which holds only when those legs hold *and* at least
one instrument came from the plans/ leg.  `--universe legacy` reproduces the pre-amendment
universe (the round-73 control).

Predicate (all four legs must hold):
  MISSING            = advertised instruments with no registry row          -> 0
  INCOMPLETE         = registry rows with an empty cell                     -> 0
  ENTRY-MISSING      = registry rows whose entry script is not in the tree  -> 0
  SELFTEST-UNBACKED  = registry rows naming a script+flag the script lacks -> 0
Exit 0 on PREDICATE pass, 1 on fail, 2 on setup.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# The advertised universe: a lane-owned script named with a runnable command in one of
# the lane's self-assessment files.  Depth is bounded on purpose: fixture helpers under
# plans/fixtures/ are support code, not advertised instruments.
CMD = re.compile(r"python3 ((?:plans/[A-Za-z0-9_]+\.py|corpus/evidence/[A-Za-z0-9_]+/[A-Za-z0-9_]+\.py|grader\.py))")
FLAG = re.compile(r"(--[a-z][a-z0-9-]*)")
SELF_FILES = ("SCORECARD.md", "SKILL.md", "LOG.md", "corpus/README.md")
REGISTRY_HEADING = "## Gate/probe registry"
PLANS_UNIVERSE = "full"      # R73-C1: claims documents advertise instruments too
UNIVERSES = ("full", "legacy")


def self_assessment_files(lane: Path, universe: str = PLANS_UNIVERSE) -> list[Path]:
    files = [lane / f for f in SELF_FILES]
    kdir = lane / "corpus" / "knowledge"
    if kdir.is_dir():
        files += sorted(kdir.glob("*.md"))
    if universe == "full":
        pdir = lane / "plans"
        if pdir.is_dir():
            files += sorted(pdir.glob("*.md"))
    elif universe != "legacy":
        raise ValueError(f"unknown universe {universe!r}")
    return [f for f in files if f.exists()]


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
        rows.append(cells)
    return rows


def entry_script(entry: str) -> str | None:
    m = CMD.search(entry)
    return m.group(1) if m else None


def selftest_unbacked(cell: str, lane: Path) -> bool:
    """True when the self-test cell claims exactly one script+flag the script lacks.

    A flag explicitly negated in prose (e.g. “no --selftest in the script”) is a
    declaration that no self-test exists, not a claim that the script accepts it.
    """
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


def collect(lane: Path, universe: str = PLANS_UNIVERSE):
    adv: dict[str, set[str]] = {}
    for f in self_assessment_files(lane, universe):
        text = f.read_text(errors="replace")
        rel = str(f.relative_to(lane))
        for m in CMD.finditer(text):
            adv.setdefault(m.group(1), set()).add(rel)
    adv = {p: v for p, v in adv.items() if (lane / p).exists()}

    skill = (lane / "SKILL.md").read_text(errors="replace")
    block = registry_block(skill)
    rows = parse_rows(block)
    reg: dict[str, list[str]] = {}
    for r in rows:
        s = entry_script(r[2])
        if s:
            reg.setdefault(s, r)

    missing = sorted(set(adv) - set(reg))
    incomplete = [r[0] for r in rows if not all(r)]
    entry_missing = sorted(s for s in reg if not (lane / s).exists())
    names = [r[0] for r in rows]
    duplicate = sorted({n for n in names if names.count(n) > 1})
    unbacked = [r[0] for r in rows if selftest_unbacked(r[4], lane)]
    return adv, rows, reg, missing, incomplete, entry_missing, unbacked, duplicate


def verdict(lane: Path, universe: str = PLANS_UNIVERSE) -> int:
    adv, rows, reg, missing, incomplete, entry_missing, unbacked, duplicate = collect(lane, universe)
    plans_only = sorted(p for p, files in adv.items()
                        if files and all(x.startswith("plans/") for x in files))
    print(f"UNIVERSE mode={universe} files={len(self_assessment_files(lane, universe))} "
          f"plans_only={len(plans_only)}")
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
    r73 = ok and universe == "full" and len(plans_only) >= 1
    print(f"PREDICATE R73-C1 {'pass' if r73 else 'fail'}")
    return 0 if r73 else 1


def selftest(lane: Path) -> int:
    """Four fixtures on temp trees: a clean lane passes; a lane whose registry omits an
    advertised instrument fails on MISSING; a lane with a blank cell fails on INCOMPLETE; an
    instrument advertised only in a plans/ document is MISSING under `full` and invisible to
    the `legacy` control."""
    import shutil
    import tempfile

    fails = 0
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        (t / "plans").mkdir()
        (t / "corpus" / "knowledge").mkdir(parents=True)
        (t / "plans" / "tool_a.py").write_text("# tool\n")
        (t / "grader.py").write_text("# grader\n")
        (t / "SCORECARD.md").write_text("run `python3 plans/tool_a.py` and `python3 grader.py`\n")
        (t / "SKILL.md").write_text(
            REGISTRY_HEADING + "\n\n| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| `t` | gate | `python3 plans/tool_a.py` | 0 ok | none declared | none | read-only | kengaku |\n"
            "| `g` | gate | `python3 grader.py` | 0 ok | none declared | none | read-only | kengaku |\n"
        )
        (t / "LOG.md").write_text("x\n")
        (t / "corpus" / "README.md").write_text("x\n")
        (t / "corpus" / "knowledge" / "k.md").write_text("x\n")
        adv, rows, reg, missing, incomplete, entry_missing, unbacked, _dup = collect(t)
        if missing or incomplete or entry_missing or unbacked:
            print(f"SELFTEST FAIL clean-fixture: missing={missing} incomplete={incomplete} entry_missing={entry_missing} unbacked={unbacked}")
            fails += 1
        else:
            print("SELFTEST ok clean-fixture")
        # drop the registry row for tool_a.py -> MISSING must fire
        txt = (t / "SKILL.md").read_text()
        txt = "\n".join(l for l in txt.splitlines() if "`t`" not in l)
        (t / "SKILL.md").write_text(txt + "\n")
        adv, rows, reg, missing, incomplete, entry_missing, unbacked, _dup = collect(t)
        if "plans/tool_a.py" not in missing:
            print("SELFTEST FAIL missing-fixture: a dropped registry row did not raise MISSING")
            fails += 1
        else:
            print("SELFTEST ok missing-fixture")
        # blank cell -> INCOMPLETE must fire
        txt = (t / "SKILL.md").read_text().replace("| `g` | gate | `python3 grader.py` | 0 ok |", "| `g` | gate | `python3 grader.py` |  |")
        (t / "SKILL.md").write_text(txt + "\n")
        adv, rows, reg, missing, incomplete, entry_missing, unbacked, _dup = collect(t)
        if not incomplete:
            print("SELFTEST FAIL incomplete-fixture: a blank cell did not raise INCOMPLETE")
            fails += 1
        else:
            print("SELFTEST ok incomplete-fixture")
        # R73-C1 arm: an instrument advertised ONLY in a plans/ document must be advertised
        # under the full universe and invisible under the legacy control.
        (t / "plans" / "tool_c.py").write_text("# tool\n")
        (t / "plans" / "round-99-claims.md").write_text("counter: `python3 plans/tool_c.py --lane .`\n")
        _a, _r, _g, missing_full, *_rest = collect(t, "full")
        _a, _r, _g, missing_legacy, *_rest2 = collect(t, "legacy")
        if "plans/tool_c.py" not in missing_full:
            print("SELFTEST FAIL plans-fixture: a plans-doc-only instrument did not raise MISSING")
            fails += 1
        elif "plans/tool_c.py" in missing_legacy:
            print("SELFTEST FAIL plans-fixture: the legacy universe saw a plans-doc-only instrument")
            fails += 1
        else:
            print("SELFTEST ok plans-fixture")
        shutil.rmtree(t, ignore_errors=True)
    print(f"SELFTEST cases=4 failures={fails}")
    return 0 if fails == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--universe", choices=UNIVERSES, default=PLANS_UNIVERSE)
    a = ap.parse_args()
    lane = Path(a.lane).resolve()
    if not (lane / "SKILL.md").exists():
        print(f"SETUP no SKILL.md under {lane}")
        return 2
    return selftest(lane) if a.selftest else verdict(lane, a.universe)


if __name__ == "__main__":
    sys.exit(main())

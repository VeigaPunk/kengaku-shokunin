#!/usr/bin/env python3
"""R52-C2 counter — advertised verdict instruments vs the SKILL.md gate/probe registry.

Frozen before data on 2026-10-28 (L1 KengakuR52a3); see plans/round-52-claims.md §C2 for
the predicate this implements.  Reads committed bytes only; writes nothing.

    python3 plans/round52_c2_registry.py --lane .          # verdict
    python3 plans/round52_c2_registry.py --selftest         # fixture battery

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


def self_assessment_files(lane: Path) -> list[Path]:
    files = [lane / f for f in SELF_FILES]
    kdir = lane / "corpus" / "knowledge"
    if kdir.is_dir():
        files += sorted(kdir.glob("*.md"))
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
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
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


def collect(lane: Path):
    adv: dict[str, set[str]] = {}
    for f in self_assessment_files(lane):
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
    unbacked = [r[0] for r in rows if selftest_unbacked(r[4], lane)]
    return adv, rows, reg, missing, incomplete, entry_missing, unbacked


def verdict(lane: Path) -> int:
    adv, rows, reg, missing, incomplete, entry_missing, unbacked = collect(lane)
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
    ok = not (missing or incomplete or entry_missing or unbacked)
    print(f"PREDICATE R52-C2 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def selftest(lane: Path) -> int:
    """Three fixtures on temp trees: a clean lane passes; a lane whose registry omits an
    advertised instrument fails on MISSING; a lane with a blank cell fails on INCOMPLETE."""
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
        adv, rows, reg, missing, incomplete, entry_missing, unbacked = collect(t)
        if missing or incomplete or entry_missing or unbacked:
            print(f"SELFTEST FAIL clean-fixture: missing={missing} incomplete={incomplete} entry_missing={entry_missing} unbacked={unbacked}")
            fails += 1
        else:
            print("SELFTEST ok clean-fixture")
        # drop the registry row for tool_a.py -> MISSING must fire
        txt = (t / "SKILL.md").read_text()
        txt = "\n".join(l for l in txt.splitlines() if "`t`" not in l)
        (t / "SKILL.md").write_text(txt + "\n")
        adv, rows, reg, missing, incomplete, entry_missing, unbacked = collect(t)
        if "plans/tool_a.py" not in missing:
            print("SELFTEST FAIL missing-fixture: a dropped registry row did not raise MISSING")
            fails += 1
        else:
            print("SELFTEST ok missing-fixture")
        # blank cell -> INCOMPLETE must fire
        txt = (t / "SKILL.md").read_text().replace("| `g` | gate | `python3 grader.py` | 0 ok |", "| `g` | gate | `python3 grader.py` |  |")
        (t / "SKILL.md").write_text(txt + "\n")
        adv, rows, reg, missing, incomplete, entry_missing, unbacked = collect(t)
        if not incomplete:
            print("SELFTEST FAIL incomplete-fixture: a blank cell did not raise INCOMPLETE")
            fails += 1
        else:
            print("SELFTEST ok incomplete-fixture")
        shutil.rmtree(t, ignore_errors=True)
    print(f"SELFTEST cases=3 failures={fails}")
    return 0 if fails == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    lane = Path(a.lane).resolve()
    if not (lane / "SKILL.md").exists():
        print(f"SETUP no SKILL.md under {lane}")
        return 2
    return selftest(lane) if a.selftest else verdict(lane)


if __name__ == "__main__":
    sys.exit(main())

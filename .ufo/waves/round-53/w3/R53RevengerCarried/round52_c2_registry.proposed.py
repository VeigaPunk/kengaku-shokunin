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
import contextlib
import io
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
CLAUSE_BREAK = re.compile(r"[;,()\n]|\.(?=\s)")
SCRIPT_REF = re.compile(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py")


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


def negated_flag(clause: str, flag: str) -> bool:
    """True when a negation word precedes `flag` inside the same clause."""
    m = re.search(re.escape(flag) + r"(?![a-z0-9-])", clause)
    return bool(m) and re.search(r"\b(?:no|not|without)\b", clause[: m.start()]) is not None


def selftest_unbacked(cell: str, lane: Path) -> bool:
    """True when a clause names exactly one script and an un-negated flag that script lacks.
    Negation and script association are both scoped to the clause (span), not the whole cell."""
    for clause in CLAUSE_BREAK.split(cell):
        scripts = sorted(set(SCRIPT_REF.findall(clause)))
        if len(scripts) != 1 or not (lane / scripts[0]).exists():
            continue
        body = (lane / scripts[0]).read_text(errors="replace")
        for f in sorted(set(FLAG.findall(clause))):
            if not negated_flag(clause, f) and f not in body:
                return True
    return False


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
    names = [r[0] for r in rows]
    duplicate = sorted({n for n in names if names.count(n) > 1})
    unbacked = [r[0] for r in rows if selftest_unbacked(r[4], lane)]
    return adv, rows, reg, missing, incomplete, entry_missing, unbacked, duplicate


def verdict(lane: Path) -> int:
    adv, rows, reg, missing, incomplete, entry_missing, unbacked, duplicate = collect(lane)
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
    return 0 if ok else 1


T_OK = "| `t` | gate | `python3 plans/tool_a.py` | 0 ok | none declared | none | read-only | kengaku |\n"
G_OK = "| `g` | gate | `python3 grader.py` | 0 ok | none declared | none | read-only | kengaku |\n"


def _row(name: str, selftest_cell: str, entry: str = "`python3 plans/tool_a.py`") -> str:
    return f"| `{name}` | gate | {entry} | 0 ok | {selftest_cell} | none | read-only | kengaku |\n"


def _build(t: Path, rows: str, decoy: str = "") -> None:
    (t / "plans").mkdir(exist_ok=True)
    (t / "corpus" / "knowledge").mkdir(parents=True, exist_ok=True)
    (t / "plans" / "tool_a.py").write_text("# tool\n")
    (t / "grader.py").write_text("# grader\n")
    (t / "SCORECARD.md").write_text("run `python3 plans/tool_a.py` and `python3 grader.py`\n")
    (t / "SKILL.md").write_text(REGISTRY_HEADING + "\n\n| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n"
                                "|---|---|---|---|---|---|---|---|\n" + rows + "\n" + decoy)
    (t / "LOG.md").write_text("x\n")
    (t / "corpus" / "README.md").write_text("x\n")
    (t / "corpus" / "knowledge" / "k.md").write_text("x\n")


def selftest(lane: Path) -> int:
    """Ten fixtures on temp trees; each asserts the predicate's exit code and the leg it must raise.
    Covers the three original legs, the entry-missing control (K7), the decoy-table control (K5),
    span-scoped negation (honest / masking) and cross-clause flag attribution."""
    import tempfile

    cases = [
        ("clean", T_OK + G_OK, "", 0, "PREDICATE R52-C2 pass"),
        ("missing", G_OK, "", 1, "MISSING 1"),
        ("incomplete", T_OK + G_OK.replace("| 0 ok |", "|  |"), "", 1, "INCOMPLETE 1"),
        ("K7 entry-missing", T_OK + G_OK + _row("x", "none declared", "`python3 plans/gone.py`"), "", 1, "ENTRY-MISSING 1"),
        ("K5 decoy-table", G_OK, "## Decoy notes\n\n" + T_OK, 1, "MISSING 1"),
        ("false-selftest-claim", _row("t", "`python3 plans/tool_a.py --selftest` (3 fixtures)") + G_OK, "", 1, "SELFTEST-UNBACKED 1"),
        ("negated-flag-honest", _row("t", "`python3 plans/tool_a.py`: no `--selftest` in the script") + G_OK, "", 0, "PREDICATE R52-C2 pass"),
        ("negated-flag-masks-claim", _row("t", "`python3 plans/tool_a.py --selftest`, no `--ghost`") + G_OK, "", 1, "SELFTEST-UNBACKED 1"),
        ("cross-clause-flag-not-claimed", _row("t", "`python3 plans/tool_a.py` runs; `--claims plans/round-99.md` errors") + G_OK, "", 0, "PREDICATE R52-C2 pass"),
        ("negation-in-other-clause-not-masking", _row("t", "no `--ghost` here; `python3 plans/tool_a.py --selftest`") + G_OK, "", 1, "SELFTEST-UNBACKED 1"),
    ]
    fails = 0
    for name, rows, decoy, want_rc, want_text in cases:
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            _build(t, rows, decoy)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = verdict(t)
            out = buf.getvalue()
            ok = rc == want_rc and want_text in out
            print(f"SELFTEST {'ok' if ok else 'FAIL'} {name} rc={rc} want={want_rc} '{want_text}'")
            fails += 0 if ok else 1
    print(f"SELFTEST cases={len(cases)} failures={fails}")
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

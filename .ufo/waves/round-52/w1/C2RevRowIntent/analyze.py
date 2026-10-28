#!/usr/bin/env python3
"""Read-only analysis for seat C2RevRowIntent (kengaku r52 w1).

Replicates plans/round52_c2_registry.py's extraction rules against the lane tree to
answer, mechanically:
  A) which self-assessment file advertises each of the 28 MISSING instruments;
  B) why a registry row exists / does not exist for each instrument (row parsed? cells?);
  C) the exact flags each of the 28 scripts accepts (for the registry self-test cell);
  D) the raw self-test cell of the one row the counter calls SELFTEST-UNBACKED.
Writes nothing inside the lane.
"""
import re
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CMD = re.compile(r"python3 ((?:plans/[A-Za-z0-9_]+\.py|corpus/evidence/[A-Za-z0-9_]+/[A-Za-z0-9_]+\.py|grader\.py))")
FLAG = re.compile(r"(--[a-z][a-z0-9-]*)")
SELF_FILES = ("SCORECARD.md", "SKILL.md", "LOG.md", "corpus/README.md")
REGISTRY_HEADING = "## Gate/probe registry"

MISSING = """plans/adoption_check.py
plans/attrib_probe.py
plans/catalog_probe.py
plans/defect_ledger.py
plans/gate_flip_check.py
plans/parser_policy_compare.py
plans/password_recovery_probe.py
plans/polyglot_c_py_probe.py
plans/round28_census.py
plans/round30_defects.py
plans/round31_c1_verify.py
plans/round31_defects.py
plans/round33_c1_verify.py
plans/round33_defects.py
plans/round35_c1_verify.py
plans/round35_hardening.py
plans/round36_c2_verify.py
plans/round45_c1_verify.py
plans/round45_c2_verify.py
plans/round46_c1_verify.py
plans/round46_c2_verify.py
plans/round46_c3_verify.py
plans/round50_c1_verify.py
plans/round50_c2_audit.py
plans/round51_routing.py
plans/round51_surfaces.py
plans/routed_open.py
plans/tb2_grader_probe.py""".split()


def self_assessment_files():
    files = [LANE / f for f in SELF_FILES]
    kdir = LANE / "corpus" / "knowledge"
    if kdir.is_dir():
        files += sorted(kdir.glob("*.md"))
    return [f for f in files if f.exists()]


def registry_block(text):
    i = text.find(REGISTRY_HEADING)
    if i < 0:
        return ""
    j = text.find("\n## ", i + 1)
    return text[i:j] if j > 0 else text[i:]


def parse_rows(block):
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


def main():
    # A) advertisers
    adv = {}
    for f in self_assessment_files():
        text = f.read_text(errors="replace")
        rel = str(f.relative_to(LANE))
        for m in CMD.finditer(text):
            adv.setdefault(m.group(1), set()).add(rel)
    adv = {p: v for p, v in adv.items() if (LANE / p).exists()}

    skill = (LANE / "SKILL.md").read_text(errors="replace")
    block = registry_block(skill)
    rows = parse_rows(block)
    reg = {}
    for r in rows:
        m = CMD.search(r[2])
        if m:
            reg.setdefault(m.group(1), r)

    print("== A/B) per missing instrument ==")
    for p in MISSING:
        advertisers = sorted(adv.get(p, ()))
        r = reg.get(p)
        print(f"{p}\n  advertised_in={advertisers}")
        if r:
            print(f"  registry_row=YES name={r[0]!r} kind={r[1]!r}")
        else:
            print("  registry_row=NO")

    print("\n== B2) registry table lines dropped by the row parser ==")
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 8 and not set(cells[0]) <= set("-: "):
            continue
        head = cells[0][:60]
        name = re.search(r"`([^`]+)`", line)
        print(f"  cells={len(cells)} name={name.group(1) if name else head!r}")
        if name:
            for m in re.finditer(r"\\?\|", line):
                pass
        # locate the offending pipes
        idx = [i for i, c in enumerate(line.strip().strip("|").split("|"))]
        print(f"     raw_len={len(line)}")

    print("\n== C) flags accepted by each of the 28 scripts ==")
    for p in MISSING:
        s = LANE / p
        body = s.read_text(errors="replace")
        # argparse option strings
        opts = sorted(set(re.findall(r"add_argument\(\s*[\"'](--[a-z0-9-]+)[\"']", body)))
        has_selftest = "--selftest" in body
        sub = sorted(set(re.findall(r"add_subparsers\([^)]*\)", body)))
        print(f"{p}\n  argparse_flags={opts} selftest_string_present={has_selftest}")

    print("\n== D) raw self-test cell of the order-check row ==")
    for line in block.splitlines():
        if line.startswith("| `order-check`"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            print(f"  cells={len(cells)}")
            print(f"  self_test_cell={cells[4] if len(cells) > 4 else 'N/A'!r}")
            scripts = sorted(set(re.findall(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py", cells[4] if len(cells) > 4 else "")))
            flags = sorted(set(FLAG.findall(cells[4] if len(cells) > 4 else "")))
            print(f"  scripts={scripts} flags={flags}")
            for sc in scripts:
                path = LANE / sc
                if path.exists():
                    b = path.read_text(errors="replace")
                    print(f"  {sc}: exists=True flags_present={{{', '.join(f + '=' + str(f in b) for f in flags)}}}")
                else:
                    print(f"  {sc}: exists=False")
            break


if __name__ == "__main__":
    sys.exit(main())

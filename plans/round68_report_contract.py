#!/usr/bin/env python3
"""Round 68, A2: the round-report contract gate.

Frozen predicate (plans/round-68-claims.md, Amendment A2 item 3):

  `python3 plans/round68_report_contract.py <report> --shonen SHONEN.md` exits 0
  and prints `PREDICATE R68-A2 pass` with `DEFECTS n=0` iff S1-S6 hold.

S1 headings        each of the six required `##` headings appears exactly once, in order
S2 SHONEN boxes    `## SHONEN` occurs once and carries exactly one checklist line per
                   SHONEN.md box, matched by the box's first five normalized words
S3 trend verdicts  `expansion:`, `quality:`, `discernment:` each with a verdict word
S4 evidence        the measurements section carries >=2 table rows, each with a
                   backticked token or a 7+-hex commit hash
S5 placeholders    no TODO / TBD / FIXME / lorem ipsum / <placeholder>
S6 driver parity   >= 400 bytes and >= 3 `##` sections

`--selftest` builds five fixtures under --work and proves every check can fail:
r1 the attempt-1 report (missing SHONEN and Trend verdicts), r2 three box lines,
r3 no `discernment:`, r4 a `TODO`, r5 the compliant skeleton.

Exit 0 = pass; 1 = defects; 2 = could-not-evaluate (missing input).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

HEADINGS = [
    "## Work performed",
    "## Landed changes",
    "## Before → after measurements",
    "## Sources & frontier",
    "## Trend verdicts",
    "## SHONEN",
]
VERDICTS = ("improved", "harmed", "unchanged", "unprovable-but-better")
EXPECTED_BOXES = 4  # SHONEN.md carries four boxes (frozen A2 S2 sentence)
BOX_RE = re.compile(r"^- \[[x~ ]\]\s+(.*)$")
CHECK_RE = re.compile(r"^\s*- \[[x~ ]\]\s+(.*)$")
HEX_RE = re.compile(r"\b[0-9a-f]{7,}\b")
H2_RE = re.compile(r"^#{2}\s")
PLACEHOLDERS = ("TODO", "TBD", "FIXME", "lorem ipsum", "<placeholder>")
MAX_INPUT_BYTES = 2 * 1024 * 1024


def norm(text: str) -> str:
    return " ".join(text.split())


def box_keys(shonen_text: str) -> list[str]:
    keys = []
    for line in shonen_text.splitlines():
        m = BOX_RE.match(line.strip())
        if not m:
            continue
        keys.append(" ".join(norm(m.group(1)).split()[:5]))
    return keys


def section(report: str, heading: str) -> str | None:
    lines = report.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if norm(line) == norm(heading))
    except StopIteration:
        return None
    out = []
    for line in lines[start + 1:]:
        if H2_RE.match(line):
            break
        out.append(line)
    return "\n".join(out)


def check(report: str, shonen: str) -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    lines = report.splitlines()

    # S1 — headings, exactly once each, in order.
    positions = []
    missing = []
    dup = []
    for heading in HEADINGS:
        hits = [i for i, line in enumerate(lines) if norm(line) == norm(heading)]
        if not hits:
            missing.append(heading)
        if len(hits) > 1:
            dup.append(f"{heading} x{len(hits)}")
        if hits:
            positions.append(hits[0])
    ordered = positions == sorted(positions) and len(positions) == len(HEADINGS)
    ok = not missing and not dup and ordered
    results.append(("S1", ok, f"headings={len(positions)}/6 missing={missing} dup={dup} ordered={ordered}"))

    # S2 — one checklist line per SHONEN.md box, matched by first five words.
    keys = box_keys(shonen)
    sec = section(report, "## SHONEN")
    if sec is None:
        results.append(("S2", False, f"no ## SHONEN section (boxes={len(keys)})"))
    else:
        got = [norm(m.group(1)) for m in (CHECK_RE.match(line) for line in sec.splitlines()) if m]
        matched = sum(1 for key in keys if any(g.startswith(key) for g in got))
        ok = len(keys) == EXPECTED_BOXES and len(got) == len(keys) and matched == len(keys)
        results.append(("S2", ok, f"box-lines={len(got)} want={len(keys)} (SHONEN.md boxes={EXPECTED_BOXES}) matched={matched}"))

    # S3 — the three trend verdicts.
    sec = section(report, "## Trend verdicts") or ""
    found = {}
    for trend in ("expansion", "quality", "discernment"):
        m = re.search(rf"{trend}\s*:\s*\**\s*({'|'.join(VERDICTS)})", sec)
        found[trend] = m.group(1) if m else None
    ok = all(found.values())
    results.append(("S3", ok, " ".join(f"{k}={v}" for k, v in found.items())))

    # S4 — evidence rows in the measurements table.
    sec = section(report, "## Before → after measurements") or ""
    rows = []
    for line in sec.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if cells and cells[0].lower().startswith(("claim", "claim / axis")):
            continue
        rows.append(stripped)
    pointed = sum(1 for row in rows if "`" in row or HEX_RE.search(row))
    ok = len(rows) >= 2 and pointed == len(rows)
    results.append(("S4", ok, f"rows={len(rows)} pointed={pointed}"))

    # S5 — placeholders.
    lowered = report.lower()
    hits = [p for p in PLACEHOLDERS if p.lower() in lowered]
    results.append(("S5", not hits, f"placeholders={hits}"))

    # S6 — driver parity.
    size = len(report.encode("utf-8"))
    sections = sum(1 for line in lines if H2_RE.match(line))
    ok = size >= 400 and sections >= 3
    results.append(("S6", ok, f"bytes={size} sections={sections}"))
    return results


def skeleton(shonen: str) -> str:
    boxes = [norm(m.group(1)) for m in (BOX_RE.match(line.strip()) for line in shonen.splitlines()) if m]
    shonen_lines = "\n".join(f"- [~] {box} — evidence: `corpus/lessons/round-68.md`" for box in boxes)
    return (
        "# fixture report\n\n"
        "## Work performed\n\nClaim R68-C1 re-derived (`plans/round68_c1_pypi_finish.py`).\n\n"
        "## Landed changes\n\n| change | commit |\n|---|---|\n| gate | `0e52fb5d` |\n\n"
        "## Before → after measurements\n\n"
        "| claim | before | after | command | verdict |\n|---|---|---|---|---|\n"
        "| R68-C1 | absent `0e52fb5d` | pass `a8883187` | `python3 plans/round68_c1_pypi_finish.py --check-receipt r` | pass |\n"
        "| R68-C2 | `DEFECTS n=5` `a8883187` | `DEFECTS n=0` `0e52fb5d` | `python3 plans/round68_c2_correction_gate.py` | pass |\n\n"
        "## Sources & frontier\n\nS240 row present `corpus/SOURCES.md`.\n\n"
        "## Trend verdicts\n\n- expansion: improved (`corpus/SOURCES.md`)\n"
        "- quality: improved (`plans/round68_report_contract.py`)\n"
        "- discernment: unchanged (`corpus/lessons/round-68.md`)\n\n"
        "## SHONEN\n\n" + shonen_lines + "\n"
    )


def _mutate(text: str, old: str, new: str) -> str:
    if old not in text:
        raise SystemExit(f"selftest fixture construction failed: {old!r} absent")
    return text.replace(old, new, 1)


def selftest(lane: Path, work: Path) -> int:
    work.mkdir(parents=True, exist_ok=True)
    shonen = (lane / "SHONEN.md").read_text(encoding="utf-8")
    attempt1 = lane / ".ufo/waves/round-68/w2/report-fixtures/attempt1-report.md"
    if not attempt1.is_file():
        print(f"SELFTEST r1-attempt1 missing fixture {attempt1}")
        return 2
    good = skeleton(shonen)
    boxes = [ln for ln in good.splitlines() if ln.strip().startswith("- [") and "round-68.md" in ln]
    three = good.replace("\n".join(boxes), "\n".join(boxes[:3]))
    wrong_labels = good.replace("- [~] SKILL.md contains", "- [~] The skill contains", 1)
    swapped = _mutate(good, "## Work performed", "## TEMP")
    swapped = _mutate(swapped, "## Landed changes", "## Work performed")
    swapped = _mutate(swapped, "## TEMP", "## Landed changes")
    duplicated = good + "\n## Landed changes\n\nduplicate section\n"
    rows_start = good.index("| R68-C1 |")
    rows_end = good.index("\n\n## Sources", rows_start)
    unpointed_rows = good[:rows_start] + "| R68-C1 | absent | pass | none | pass |\n| R68-C2 | n=5 | n=0 | none | pass |" + good[rows_end:]
    minimal = "## Work performed\n\nx\n"
    five_boxes = good + "- [~] An extra checklist line no SHONEN.md box matches — evidence: `corpus/lessons/round-68.md`\n"
    spaced_dup = good + "\n##  SHONEN\n\n- [~] duplicate section\n"

    fixtures: list[tuple[str, str, set[str]]] = [
        ("r1-attempt1", attempt1.read_text(encoding="utf-8"), {"S1", "S2", "S3"}),
        ("r2-three-boxes", three, {"S2"}),
        ("r3-no-discernment", good.replace("- discernment:", "- judgement:"), {"S3"}),
        ("r4-placeholder", good.replace("Claim R68-C1", "TODO Claim R68-C1"), {"S5"}),
        ("r6-wrong-labels", wrong_labels, {"S2"}),
        ("r7-order-swapped", swapped, {"S1"}),
        ("r8-duplicate-heading", duplicated, {"S1"}),
        ("r9-unpointed-rows", unpointed_rows, {"S4"}),
        ("r10-minimal", minimal, {"S1", "S2", "S3", "S4", "S6"}),
        ("r11-five-boxes", five_boxes, {"S2"}),
        ("r12-spaced-dup-heading", spaced_dup, {"S1"}),
        ("r5-green", good, set()),
    ]
    refused = 0
    green_ok = 0
    total = len(fixtures)
    for name, text, expected in fixtures:
        path = work / f"{name}.md"
        path.write_text(text, encoding="utf-8")
        results = check(text, shonen)
        got = {code for code, ok, _ in results if not ok}
        ok = got == expected
        print(f"SELFTEST {name} want={sorted(expected) or 'pass'} got={sorted(got) or 'pass'} {'ok' if ok else 'MISMATCH'}")
        if expected and ok:
            refused += 1
        if not expected and ok:
            green_ok += 1
    zero_codes = {code for code, ok_, _ in check(good, "") if not ok_}
    zero_ok = zero_codes == {"S2"}
    print(f"SELFTEST r13-zero-box-shonen want=['S2'] got={sorted(zero_codes) or 'pass'} {'ok' if zero_ok else 'MISMATCH'}")
    total += 1
    refused += 1 if zero_ok else 0
    empty_shonen_report = good.split("## SHONEN")[0] + "## SHONEN\n\n"
    vacuous_codes = {code for code, ok_, _ in check(empty_shonen_report, "") if not ok_}
    vacuous_ok = vacuous_codes == {"S2"}
    print(f"SELFTEST r14-empty-shonen-empty-report want=['S2'] got={sorted(vacuous_codes) or 'pass'} {'ok' if vacuous_ok else 'MISMATCH'}")
    total += 1
    refused += 1 if vacuous_ok else 0
    ok = refused == total - 1 and green_ok == 1
    print(f"SELFTEST n={total} red-refused={refused} green-ok={green_ok}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Round 68, A2: the round-report contract gate.")
    ap.add_argument("report", nargs="?", help="report markdown to check")
    ap.add_argument("--lane", default=os.environ.get("UFO_LANE_ROOT", str(Path(__file__).resolve().parent.parent)))
    ap.add_argument("--shonen", default=None, help="SHONEN.md path (default <lane>/SHONEN.md)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", default=None, help="scratch dir for --selftest fixtures")
    args = ap.parse_args(argv)

    lane = Path(args.lane).resolve()
    shonen_path = Path(args.shonen) if args.shonen else lane / "SHONEN.md"
    if args.selftest:
        if args.work:
            work = Path(args.work)
        else:
            import tempfile
            work = Path(tempfile.mkdtemp(prefix="r68-a2-selftest-"))
        try:
            return selftest(lane, work)
        except OSError as exc:
            print(f"SELFTEST could-not-evaluate {exc}")
            return 2
    if not args.report:
        print("usage: round68_report_contract.py <report> [--shonen SHONEN.md] [--selftest]", file=sys.stderr)
        return 2
    report_path = Path(args.report)
    resolved_shonen = shonen_path.resolve()
    print(f"SHONEN {resolved_shonen}")
    for path in (report_path, resolved_shonen):
        if not path.is_file():
            print(f"SETUP could-not-evaluate {path} is not a regular file")
            return 2
        if path.stat().st_size > MAX_INPUT_BYTES:
            print(f"SETUP could-not-evaluate {path} exceeds {MAX_INPUT_BYTES} bytes")
            return 2
    try:
        report = report_path.read_bytes().decode("utf-8")
        shonen = resolved_shonen.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"SETUP could-not-evaluate {exc}")
        return 2
    results = check(report, shonen)
    defects = 0
    for code, ok, detail in results:
        print(f"{code} {'ok' if ok else 'defect'} {detail}")
        if not ok:
            defects += 1
    print(f"DEFECTS n={defects}")
    print(f"PREDICATE R68-A2 {'pass' if defects == 0 else 'fail'}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

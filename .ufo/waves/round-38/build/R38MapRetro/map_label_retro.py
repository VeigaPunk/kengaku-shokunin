#!/usr/bin/env python3
"""R38MapRetro: apply round-38 C2 V7's derived-label rule to the ROUND-37 `## Requirement map`.

Round 37's V7 (plans/round37_c2_verify.py) only asked whether an `enforced` row cites some case
observed `fail`, an `unenforced` row some case observed `pass`, a `partly` row one of each. Round 38's
V7 (plans/round38_c2_verify.py:207-213, :216-256) keys on the receipt's `violates=` tag instead:

    enforced    iff every receipt case whose violates-set carries the line is observed `fail`
    unenforced  iff every such case is observed `pass`
    partly      otherwise,
and every case a row cites must be one of those violating cases.

The round-37 receipt predates `violates=` (its CASE lines carry `-- <requirement>` prose, no tag) and
its map rows label whole line ranges (`instruction.md:1-6`). So the per-case violates-set is read from
an external table (`violates-r37.tsv`: case id -> instruction.md lines, one justification per case) and
a row's label is derived over the union of cases violating any line in the row's range.

  --rule violating   round-38 V7 (default): derive from every violating case, check citations.
  --rule cited       round-37 V7 (ablation): derive from the row's cited cases only, no membership
                     check -- the blind spot that let `instruction.md:9 | enforced` stand beside an
                     observed-pass violating case.

Exit 0 iff no row disagrees and no structural problem was found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CASE = re.compile(r"^CASE (\S+) .*?\bobserved=(pass|fail)\b")
SUMMARY = re.compile(r"^cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)$")
SECTION = re.compile(r"^## Requirement map\n(.*?)(?=^## |\Z)", re.S | re.M)
ROW = re.compile(r"^\|\s*`instruction\.md:(\d+)(?:-(\d+))?`\s*\|\s*`?(enforced|unenforced|partly)`?\s*\|(.*)\|\s*$")
CITED = re.compile(r"`([a-z0-9][a-z0-9-]*)`")


def lines_of(field):
    """'1-6,9' -> {1,2,3,4,5,6,9}; '-' -> set(). Raises ValueError on an unparsable item."""
    out = set()
    for item in field.split(","):
        item = item.strip()
        if not item or item == "-":
            continue
        m = re.match(r"^(\d+)(?:-(\d+))?$", item)
        if not m:
            raise ValueError(f"bad line item {item!r}")
        lo = int(m.group(1))
        hi = int(m.group(2) or lo)
        if hi < lo:
            raise ValueError(f"reversed range {item!r}")
        out.update(range(lo, hi + 1))
    return out


def derive(verdicts):
    if verdicts == {"fail"}:
        return "enforced"
    if verdicts == {"pass"}:
        return "unenforced"
    return "partly"


def read_receipt(path):
    """-> (observed {case: pass|fail}, (n, pass, fail, mismatches) | None, [problems])"""
    text = path.read_text()
    observed, problems = {}, []
    for l in text.splitlines():
        m = CASE.match(l)
        if m:
            if m.group(1) in observed:
                problems.append(f"duplicate receipt case {m.group(1)}")
            observed[m.group(1)] = m.group(2)
    summ = [m for m in (SUMMARY.match(l) for l in text.splitlines()) if m]
    if len(summ) != 1:
        problems.append(f"summary line count {len(summ)} != 1")
        return observed, None, problems
    n, p, f, m = map(int, summ[0].groups())
    cp = sum(1 for o in observed.values() if o == "pass")
    cf = sum(1 for o in observed.values() if o == "fail")
    if not (n == len(observed) and p == cp and f == cf and p + f == n):
        problems.append(f"summary cases={n} pass={p} fail={f} disagrees with CASE lines ({len(observed)})")
    return observed, (n, p, f, m), problems


def read_violates(path):
    """-> ({case: (lineset, why)}, {case: lineno}, [problems])"""
    table, where, problems = {}, {}, []
    for i, raw in enumerate(path.read_text().splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 3:
            problems.append(f"{path.name}:{i}: expected 3 tab-separated fields, got {len(parts)}")
            continue
        case, field, why = (p.strip() for p in parts)
        if case in table:
            problems.append(f"{path.name}:{i}: duplicate case {case}")
            continue
        try:
            lines = lines_of(field)
        except ValueError as e:
            problems.append(f"{path.name}:{i}: {e}")
            continue
        if not why:
            problems.append(f"{path.name}:{i}: {case} carries no justification")
        table[case], where[case] = (lines, why), i
    return table, where, problems


def read_rows(path):
    """-> ([(lo, hi, label, [cited])], [problems])"""
    text = path.read_text()
    sec = SECTION.search(text)
    if not sec:
        return [], [f"{path}: no '## Requirement map' section"]
    rows, problems = [], []
    for l in sec.group(1).splitlines():
        m = ROW.match(l)
        if not m:
            if l.startswith("|") and "instruction.md:" in l:
                problems.append(f"unparsed row {l[:60]!r}")
            continue
        lo = int(m.group(1))
        hi = int(m.group(2) or lo)
        if hi < lo:
            problems.append(f"reversed row range {lo}-{hi}")
        rows.append((lo, hi, m.group(3), CITED.findall(m.group(4))))
    rows.sort()
    covered, dup = set(), []
    for lo, hi, _label, _cited in rows:
        for n in range(lo, hi + 1):
            if n in covered:
                dup.append(n)
            covered.add(n)
    if dup:
        problems.append(f"lines mapped twice={sorted(set(dup))}")
    if rows:
        missing = [n for n in range(1, max(hi for _lo, hi, _l, _c in rows) + 1) if n not in covered]
        if missing:
            problems.append(f"lines unmapped={missing}")
    return rows, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--entry", default="corpus/knowledge/tb2-git-webserver-grader.md")
    ap.add_argument("--receipt", default="corpus/evidence/round37/git-webserver-probe.txt")
    ap.add_argument("--violates", default=None, help="case id -> instruction.md lines (TSV)")
    ap.add_argument("--map-file", default=None,
                    help="file holding a '## Requirement map' section to check instead of the entry's")
    ap.add_argument("--instruction", default="corpus/evidence/round37/tb2-git-webserver/instruction.md")
    ap.add_argument("--rule", choices=("violating", "cited"), default="violating")
    a = ap.parse_args()

    here = Path(__file__).resolve().parent
    entry = Path(a.entry)
    mappath = Path(a.map_file) if a.map_file else entry
    viol = Path(a.violates) if a.violates else here / "violates-r37.tsv"

    observed, summary, problems = read_receipt(Path(a.receipt))
    table, _where, vproblems = read_violates(viol)
    problems += vproblems
    rows, rproblems = read_rows(mappath)
    problems += rproblems

    extra = sorted(set(table) - set(observed))
    absent = sorted(set(observed) - set(table))
    if extra:
        problems.append(f"violates table names cases not in the receipt: {extra}")
    if absent:
        problems.append(f"receipt cases missing from the violates table: {absent}")

    n_inst = None
    ipath = Path(a.instruction)
    if ipath.is_file():
        n_inst = len([l for l in ipath.read_text().splitlines() if l.strip()])

    print(f"# entry={mappath} receipt={a.receipt} violates={viol} rule={a.rule}")
    if summary:
        print(f"# receipt cases={summary[0]} observed_pass={summary[1]} observed_fail={summary[2]} "
              f"mismatches={summary[3]}")
    if n_inst:
        mapped = sorted({n for lines, _w in table.values() for n in lines})
        print(f"# instruction lines={n_inst} violates-table lines={mapped} "
              f"unmapped={sorted(set(range(1, n_inst + 1)) - set(mapped))}")
    print("# case\toverall")

    disagree = 0
    for lo, hi, label, cited in rows:
        tag = f"instruction.md:{lo}" if lo == hi else f"instruction.md:{lo}-{hi}"
        rng = set(range(lo, hi + 1))
        violating = {c: o for c, o in observed.items() if table.get(c, (set(), ""))[0] & rng}
        if a.rule == "cited":
            pool = {c: observed[c] for c in cited if c in observed}
            if pool == {}:
                problems.append(f"{tag}: cites no case known to the receipt")
                derived = None
            else:
                derived = derive(set(pool.values()))
        elif not violating:
            problems.append(f"{tag}: no receipt case violates it")
            derived = None
        else:
            derived = derive(set(violating.values()))
        if not cited:
            cited_bad = ["<none>"]
        elif a.rule == "violating":
            cited_bad = [c for c in cited if c not in violating]
        else:
            cited_bad = [c for c in cited if c not in observed]
        rows_ok = derived is not None and derived == label and not cited_bad
        if not rows_ok:
            disagree += 1
        print(f"\nROW {tag} labelled={label} derived={derived} agree={'yes' if rows_ok else 'NO'}")
        if a.rule == "violating":
            print(f"  violators={len(violating)} "
                  + " ".join(f"{c}={o}" for c, o in sorted(violating.items())))
            free = sorted(c for c, o in violating.items() if o == "pass")
            print(f"  violating-but-passing={free or 'none'}")
        else:
            print("  cited-verdicts=" + " ".join(f"{c}={observed.get(c, 'ABSENT')}" for c in cited))
        print("  cited=" + (" ".join(f"{c}={'ok' if c not in cited_bad else 'NOT-A-VIOLATOR'}"
                                     for c in cited) if cited else "<none>"))
    print()

    for n in sorted({n for lines, _w in table.values() for n in lines}):
        pool = {c: o for c, o in observed.items() if n in table.get(c, (set(), ""))[0]}
        if pool:
            print(f"LINE {n} derived={derive(set(pool.values()))} cases={len(pool)} "
                  f"pass={sum(1 for o in pool.values() if o == 'pass')} "
                  f"fail={sum(1 for o in pool.values() if o == 'fail')}")

    for p in problems:
        print(f"PROBLEM {p}")
    print(f"rows={len(rows)} disagree={disagree} problems={len(problems)}")
    print(f"MAP-RETRO disagree={disagree} rule={a.rule} "
          f"{'pass' if disagree == 0 and not problems else 'fail'}")
    return 0 if disagree == 0 and not problems else 1


if __name__ == "__main__":
    sys.exit(main())

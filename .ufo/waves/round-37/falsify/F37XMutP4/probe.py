#!/usr/bin/env python3
"""F37XMutP4 counterexample probe: for each surviving new P4 mutant, build the minimal fixture that
WOULD kill it (a row the battery never builds) and show reference-reject vs mutant-accept. Proves the
survivors are coverage gaps of plans/battery37/*.py, not equivalent mutants.

Fixtures are built from the genuine round-35 package with the counter's own helpers, into --work
(scratch), never the lane.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import subprocess
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--harness", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    h = load(pathlib.Path(a.harness), "f37_harness")
    k = h.load_counter(lane)
    r36 = k.load_r36(lane)
    ctx = k.Ctx(lane, r36)
    gate_src = (lane / k.GATE_REL).read_text()
    gdir = work / "gates"
    gdir.mkdir(parents=True, exist_ok=True)
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)
    mgates = {}
    for mid, label, old, new in h.NEW_MUTANTS:
        assert gate_src.count(old) == 1, mid
        p = gdir / f"{mid}.py"
        p.write_text(gate_src.replace(old, new, 1))
        mgates[mid] = p

    def entry_text_split(text):
        m, lines, rows = r36.quote_table(text)
        return lines[rows[1]:rows[-1] + 1]

    def make(name, fn):
        d = work / "probe" / name
        if d.exists():
            import shutil
            shutil.rmtree(d)
        ctx.genuine_package(d)
        entry = d / ctx.spec["entry"]
        entry.write_text(r36.rewrite_quotes(entry.read_text(), fn))
        ctx.git_add(d)
        return d

    def rebuild(row, span, repl):
        return row[:span[0]] + repl + row[span[1]:]

    cap_name = r36.QUOTE_ROW.match(entry_text_split((pathlib.Path(lane) / ctx.spec["entry"]).read_text())[0]).group(2)
    cap_lines = (lane / ctx.spec["capture_dir"] / cap_name).read_text().splitlines()

    def second_row_outside(rows):
        rows = list(rows)
        m = r36.QUOTE_ROW.match(rows[1])
        rows[1] = rebuild(rows[1], m.span(3), "9999")
        return rows

    def first_row_wrong_lines(rows):
        rows = list(rows)
        m = r36.QUOTE_ROW.match(rows[0])
        return [rebuild(rows[0], (m.start(3), m.end(4) if m.group(4) else m.end(3)), "1-2")] + list(rows[1:])

    def first_row_case_only(rows):
        rows = list(rows)
        m = r36.QUOTE_ROW.match(rows[0])
        up = m.group(1).upper()
        if up == m.group(1):
            raise RuntimeError("quote has no letters to upper-case")
        return [rebuild(rows[0], (m.start(1), m.end(1)), up)] + list(rows[1:])

    def first_row_one_past_end(rows):
        rows = list(rows)
        m = r36.QUOTE_ROW.match(rows[0])
        span = (m.start(3), m.end(3))
        return [rebuild(rows[0], span, f"{m.group(3)}-{len(cap_lines) + 1}")] + list(rows[1:])

    cases = [
        ("probe-second-row-outside", "X2", second_row_outside),
        ("probe-first-row-off-line", "X4", first_row_wrong_lines),
        ("probe-first-row-case-only", "X5", first_row_case_only),
        ("probe-first-row-one-past-end", "X6", first_row_one_past_end),
    ]
    out = {"capture": cap_name, "capture_lines": len(cap_lines), "rows": [], "note": "fixtures live only in scratch"}
    for name, mid, fn in cases:
        d = make(name, fn)
        argv = ["package", "--root", str(d), "--require-clean-tree"]
        ref = k.run_gate(ref_gate, ctx.spec_path, argv)
        got = k.run_gate(mgates[mid], ctx.spec_path, argv)
        out["rows"].append({"fixture": name, "mutant": mid,
                            "ref": [ref[0], sorted(ref[1])], "mut": [got[0], sorted(got[1])],
                            "same": ref == got})
        print(f"PROBE {name} {mid} ref=rc{ref[0]}/{{{','.join(sorted(ref[1]))}}} "
              f"mut=rc{got[0]}/{{{','.join(sorted(got[1]))}}} {'SAME' if ref == got else 'DIFFERS'}")
    pathlib.Path(a.out).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Round 54: build the entrytruth ledger draft (C2 data sweep, post-freeze).

For every row of SKILL.md's *## Gate/probe registry* this builder determines the ENTRY argv,
executes it hermetically (round54_c2_entrytruth.hermetic_env) in a scratch clone of --source,
and emits ``plans/round54-entrytruth.json`` (schema r54-entrytruth-v1) declaring exactly what it
observed: green rows carry the observed exit 0; red rows carry the observed exit, a verbatim
output fragment and a truthful reason.  The predicate this ledger is later scored against was
frozen in plans/round-54-claims.md BEFORE this sweep ran.

Candidate selection (deterministic): if the round-53 ledger declares a ``kind == entry`` argv for
the row, that argv is candidate A; otherwise A = ``python3 <script> --lane .``; candidate B =
``python3 <script>``.  Both run (cap: the smaller of --timeout and 900 s); the candidate with the
lowest exit wins, ties going to A.  The ledger records which candidates ran via the ``chosen``
field.

Exit codes: 0 ledger written · 1 nothing written (setup).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("r54entry", LANE / "plans" / "round54_c2_entrytruth.py")
r54 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r54)


def r53_entry_argv(lane: Path) -> dict[str, list[str]]:
    p = lane / "plans" / "round53-tipstate.json"
    if not p.is_file():
        return {}
    try:
        d = json.loads(p.read_text())
    except Exception:
        return {}
    out = {}
    for name, spec in (d.get("rows") or {}).items():
        if isinstance(spec, dict) and spec.get("kind") == "entry" and isinstance(spec.get("argv"), list):
            out[name] = spec["argv"]
    return out


def run_one(worker, argv, timeout, row_tmp_root):
    # row_tmp_root is unique per row; run_row creates tmp-<name> beneath it, so parallel rows
    # never share a TMPDIR
    spec = {"entry_argv": argv, "timeout_s": timeout}
    return r54.run_row(worker, "builder", spec, timeout, row_tmp_root)


def _sanitize(n: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", n)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", required=True, help="clean clone of the tree under test")
    ap.add_argument("--out", default=str(LANE / "plans" / "round54-entrytruth.json"))
    ap.add_argument("--work", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--only", default="", help="comma-separated row names to rebuild")
    args = ap.parse_args()

    source = Path(args.source)
    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    rows, dups, badname, nh = r54.registry_rows((source / "SKILL.md").read_text())
    if nh != 1 or dups or badname:
        print(f"SETUP registry broken headings={nh} dups={dups[:3]} bad={badname[:3]}", file=sys.stderr)
        return 1
    script_of = {n: r54.row_script(line) for n, line in rows.items()}
    r53 = r53_entry_argv(source)
    only = {s for s in args.only.split(",") if s}
    names = sorted(rows)
    if only:
        names = [n for n in names if n in only]
    workers = [r54.Worker(source, work, i) for i in range(max(1, args.jobs))]
    free = list(range(len(workers)))
    import threading
    lock = threading.Lock()

    out_rows: dict[str, dict] = {}

    def build(n: str) -> None:
        script = script_of[n]
        cand_a = r53.get(n) if n in r53 else (["python3", script, "--lane", "."] if script else None)
        cand_b = ["python3", script] if script else None
        with lock:
            i = free.pop()
        try:
            w = workers[i]
            results = []
            seen = []
            for c in (cand_a, cand_b):
                if c is None or json.dumps(c) in seen:
                    continue
                seen.append(json.dumps(c))
                row_tmp = work / f"row-{_sanitize(n)}"
                row_tmp.mkdir(parents=True, exist_ok=True)
                r = run_one(w, c, min(args.timeout, 900), row_tmp)
                results.append((c, r))
            def score(r):
                return r["rc"] if isinstance(r["rc"], int) else 999
            best = None
            for c, r in results:
                if best is None or score(r) < score(best[1]):
                    best = (c, r)
            if best is None:
                return
            c, r = best
            frag = ""
            if isinstance(r["rc"], int) and r["rc"] != 0:
                out_line = next((ln for ln in r["out"].splitlines() if ln.strip()), "")
                frag = out_line[:160]
            entry = {
                "entry_argv": c,
                "entry_exit": r["rc"] if isinstance(r["rc"], int) else 1,
                "entry_state": "green" if r["rc"] == 0 else "red",
                "chosen": "r53-entry" if c == r53.get(n) else ("lane-dot" if "--lane" in c else "bare"),
                "sec": r["sec"],
            }
            if entry["entry_state"] == "red":
                entry["reason"] = (f"the instrument exits {entry['entry_exit']} on the clean tree at this "
                                   f"tip; the evidence fragment is verbatim from its own output")
                entry["evidence"] = frag or "(no output captured)"
            with lock:
                out_rows[n] = entry
        finally:
            with lock:
                free.append(i)

    with ThreadPoolExecutor(max(1, args.jobs)) as ex:
        list(ex.map(build, names))
    ledger = {"schema": r54.SCHEMA, "rows": out_rows}
    Path(args.out).write_text(json.dumps(ledger, indent=1, sort_keys=True) + "\n")
    greens = sum(1 for v in out_rows.values() if v["entry_state"] == "green")
    print(f"BUILD rows={len(out_rows)} green={greens} red={len(out_rows) - greens} out={args.out}")
    for n, v in sorted(out_rows.items()):
        if v["entry_state"] == "red":
            print(f"  RED {n} exit={v['entry_exit']} frag={v['evidence'][:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

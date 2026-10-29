#!/usr/bin/env python3
"""Seat-local coverage check for the round-53 classifier (C1ExecClassifier).

Runs classify_source() over every captured grader file named by
corpus/evidence/round53/tests-index.json, keys the results the way the counter's
v2_classes does (<task>::<name> or <task>::<Class>.<name>) and reports:
  * ids covered / unclassified / extra keys,
  * the histogram over the 305 ids,
  * the delta against the previous run's classes-305.json (before the fix round).
"""
from __future__ import annotations

import collections
import importlib.util
import json
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CLASSIFIER = LANE / ".ufo/waves/round-53/w1/C1ExecClassifier/round53_c1_classify.py"
INDEX = LANE / "corpus/evidence/round53/tests-index.json"
CAPTURES = LANE / "corpus/evidence/round52/graders"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("classifier_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    mod = load_module(CLASSIFIER)
    idx = json.loads(INDEX.read_text())
    tests = idx["tests"]
    by_file: dict[str, list] = collections.defaultdict(list)
    for t in tests:
        by_file[t["file"]].append(t)

    got: dict[str, str] = {}
    extra: dict[str, list] = {}
    for rel, rows in sorted(by_file.items()):
        f = CAPTURES / rel
        if not f.exists():
            print(f"MISSING CAPTURE {rel}")
            continue
        src = f.read_text(encoding="utf-8", errors="replace")
        det = mod.classify_detail(src)
        for t in rows:
            key = t["id"]
            name = t["name"] if not t.get("class") else f"{t['class']}.{t['name']}"
            if name in det:
                got[key] = det[name][0]
            else:
                got[key] = "MISSING"
        for k in det:
            if k not in {r["name"] if not r.get("class") else f"{r['class']}.{r['name']}" for r in rows}:
                extra.setdefault(rel, []).append(k)

    covered = sum(1 for v in got.values() if v in ("P1", "P0"))
    unclassified = [k for k, v in got.items() if v not in ("P1", "P0")]
    hist = collections.Counter(got.values())
    print(f"IDS total={len(tests)} covered={covered} unclassified={len(unclassified)}")
    if unclassified:
        print("UNCLASSIFIED", unclassified[:10])
    print("EXTRA KEYS", sum(len(v) for v in extra.values()), {k: v for k, v in list(extra.items())[:5]})
    print("HISTOGRAM " + " ".join(f"{k}={hist[k]}" for k in ("P1", "P0")))
    tasks = collections.defaultdict(collections.Counter)
    for k, v in got.items():
        tasks[k.split("::", 1)[0]][v] += 1
    p1_tasks = sum(1 for t, c in tasks.items() if c["P1"])
    print(f"P1 TASKS {p1_tasks} of {len(tasks)}")

    out = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if out:
        out.write_text(json.dumps(got, indent=1, sort_keys=True) + "\n")
        print("WROTE", out)

    prev_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if prev_path and prev_path.exists():
        prev = json.loads(prev_path.read_text())
        prev_hist = collections.Counter(prev.values())
        print("PREV " + " ".join(f"{k}={prev_hist[k]}" for k in ("P1", "P0")))
        changed = {k: (prev.get(k), v) for k, v in got.items() if k in prev and prev[k] != v}
        print(f"CHANGED {len(changed)}")
        for k, (a, b) in sorted(changed.items()):
            print(f"  {k}: {a} -> {b}")
        print("ONLY-NEW", sorted(set(got) - set(prev))[:10], "ONLY-OLD", sorted(set(prev) - set(got))[:10])
    return 0


if __name__ == "__main__":
    sys.exit(main())

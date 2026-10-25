#!/usr/bin/env python3
"""Independent string-schema census over pinned test.raw.json; imports no production/oracle code."""
import collections
import hashlib
import json
from pathlib import Path

RAW = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json")
data = RAW.read_bytes()
print("raw_sha256", hashlib.sha256(data).hexdigest(), "bytes", len(data))

dup_keys = []
def hook(pairs):
    seen = collections.Counter(k for k, _ in pairs)
    for k, n in seen.items():
        if n > 1:
            dup_keys.append(k)
    return dict(pairs)

nonfinite = []
tasks = json.loads(data, object_pairs_hook=hook, parse_constant=lambda c: nonfinite.append(c) or c)
print("tasks", len(tasks), "duplicate_object_keys", dup_keys, "nonfinite_constants", nonfinite)

c = collections.Counter()
ops = collections.Counter()
optuple = collections.Counter()
value_shapes = collections.Counter()
na_tasks, na_combo, empty_hits, dormant = [], [], [], []
evtypes_issue = []
for t in tasks:
    ev = t.get("eval")
    kinds = ev.get("eval_types")
    if not isinstance(kinds, list) or not kinds or not all(isinstance(k, str) for k in kinds):
        evtypes_issue.append((t["task_id"], "invalid", kinds))
    elif len(set(kinds)) != len(kinds):
        evtypes_issue.append((t["task_id"], "dup", kinds))
    elif set(kinds) - {"string_match", "url_match", "program_html"}:
        evtypes_issue.append((t["task_id"], "unknown", kinds))
    has = "reference_answers" in ev
    refs = ev.get("reference_answers")
    active = "string_match" in kinds
    c[("active" if active else "nonactive", "absent" if not has else type(refs).__name__)] += 1
    if not active and refs is not None:
        dormant.append((t["task_id"], refs))
    if "string_note" in ev:
        c[("string_note_key", "active" if active else "nonactive", type(ev["string_note"]).__name__, "empty" if ev["string_note"] == "" else "nonempty")] += 1
    if active and isinstance(refs, dict):
        optuple[tuple(refs)] += 1
        for op, v in refs.items():
            ops[op] += 1
            shape = type(v).__name__
            if isinstance(v, list):
                shape += "[" + ",".join(sorted({type(x).__name__ for x in v})) + "]" + ("EMPTY" if not v else "")
                if any(isinstance(x, str) and not x.strip() for x in v):
                    empty_hits.append((t["task_id"], op, v))
            elif isinstance(v, str) and not v.strip():
                empty_hits.append((t["task_id"], op, v))
            value_shapes[(op, shape if op != "fuzzy_match" or v != "N/A" else "N/A")] += 1
        if refs.get("fuzzy_match") == "N/A":
            na_tasks.append(t["task_id"])
            note = ev.get("string_note")
            if len(refs) > 1:
                na_combo.append((t["task_id"], list(refs)))
            c[("na_note", type(note).__name__, "empty" if note == "" else "nonempty")] += 1
print("eval_types issues", evtypes_issue)
for k, v in sorted(c.items(), key=str):
    print("count", k, v)
print("operator occurrences (active)", dict(ops))
print("operator tuples (ordered)", {",".join(k): v for k, v in optuple.items()})
print("value shapes", {f"{a}:{b}": n for (a, b), n in sorted(value_shapes.items())})
print("NA tasks", len(na_tasks), na_tasks)
print("NA combined with other operators", na_combo)
print("empty/whitespace string references", empty_hits)
print("dormant nonactive non-null reference_answers", len(dormant), dormant[:5])

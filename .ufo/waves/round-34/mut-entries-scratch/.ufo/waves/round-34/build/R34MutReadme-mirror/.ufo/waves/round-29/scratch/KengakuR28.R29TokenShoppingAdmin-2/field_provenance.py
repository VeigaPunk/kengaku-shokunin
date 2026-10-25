#!/usr/bin/env python3
"""Field provenance census for __SHOPPING_ADMIN__: owning task, JSON path, value class.

Read-only. No production imports. Prints per-field counts and the non-URL
metadata sweep over named top-level fields.
"""
import json
import re
from collections import Counter, defaultdict

RAW = "plans/fixtures/r28/webarena/config_files/test.raw.json"
TOK = "__SHOPPING_ADMIN__"

text = open(RAW, "rb").read().decode("utf-8")
data = json.loads(text)


def walk(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + (i,))
    elif isinstance(o, str):
        yield path, o


records = []
for i, t in enumerate(data):
    for p, v in walk(t):
        for _ in range(v.count(TOK)):
            records.append({"task": i, "task_id": t["task_id"], "path": p, "value": v})

print(f"tasks={len(data)} token_tasks={len({r['task'] for r in records})} leaves={len(records)}")
print(f"index_eq_task_id={sum(1 for i,t in enumerate(data) if t['task_id']==i)}/{len(data)}")
print(f"ids_unique={len({t['task_id'] for t in data})}")
print(f"task_sites_token_only_shopping_admin="
      f"{ {tuple(t['sites']) for t in data if TOK in json.dumps(t)} }")

by = defaultdict(list)
for r in records:
    p = r["path"]
    if len(p) == 1:
        f = p[0]
    elif p[0] == "eval" and len(p) == 2:
        f = "eval." + p[1]
    else:
        f = "eval.program_html[*].url"
    by[f].append(r)
for f, rs in sorted(by.items()):
    print(f"field={f} occurrences={len(rs)} tasks={len({r['task'] for r in rs})} "
          f"distinct_values={len({r['value'] for r in rs})} "
          f"exact_token={sum(1 for r in rs if r['value']==TOK)} "
          f"suffixed={sum(1 for r in rs if r['value']!=TOK)}")

for f in ("intent", "intent_template", "instantiation_dict", "storage_state",
          "require_login", "geolocation"):
    print(f"nonurl_field={f} tasks_with_token={sum(1 for t in data if TOK in json.dumps(t.get(f)))}")
print(f"key_literals_with_token={sum(1 for k in re.findall(r'\"([^\"]+)\":', text) if TOK in k)}")
print(f"values_scheme_prefixed={sum(1 for r in records if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*://', r['value']))}")
print(f"values_starting_with_token={sum(1 for r in records if r['value'].startswith(TOK))}")
print(f"occurrences_per_task={sorted(Counter(r['task'] for r in records).values())}")
print(f"eval_types_token_tasks={Counter(tuple(data[i]['eval']['eval_types']) for i in sorted({r['task'] for r in records})).most_common()}")

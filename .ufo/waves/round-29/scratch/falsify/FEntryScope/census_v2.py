"""v2 re-check census: new candidate numbers (L48, L49, L54) and prior counterexamples. Own code."""
import collections
import json
import re

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
raw = open(ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json", encoding="utf-8").read()
prof = json.load(open(ROOT + "plans/fixtures/r29/profiles.json"))
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = [f"__{n}__" for n in ORDER]
data = json.loads(raw)

per_task = [sum(1 for t in TOK if t in json.dumps(task)) for task in data]
print("tasks_by_distinct_token_count", dict(collections.Counter(per_task)), "rows", sum(per_task))


def leaves(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from leaves(v)
    elif isinstance(o, list):
        for v in o:
            yield from leaves(v)
    elif isinstance(o, str):
        yield o


multi = [s for task in data for s in leaves(task) if sum(s.count(t) for t in TOK) > 1]
print("multi_occurrence_leaves", len(multi), "their_occurrences", sum(sum(s.count(t) for t in TOK) for s in multi))

slash_tasks = 0
slash_occ = 0
for task in data:
    s = json.dumps(task)
    n = sum(len(re.findall(re.escape(t) + "/", s)) for t in TOK)
    slash_occ += n
    slash_tasks += n > 0
print("token_then_slash_occ", slash_occ, "tasks", slash_tasks)
print("http_scheme_all_profiles", all(v.startswith("http://") for p in prof.values() for v in p["values"].values()))

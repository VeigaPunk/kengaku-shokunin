"""FEntryQuality-2 re-check of v2's new numbers and its quote-injection sentence."""
import json
from collections import Counter

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
raw = open(ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json", encoding="utf-8").read()
tasks = json.loads(raw)
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = [f"__{n}__" for n in ORDER]


def leaves(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from leaves(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from leaves(v)
    elif isinstance(obj, str):
        yield obj


per_task_kinds = Counter(sum(any(t in s for s in leaves(task)) for t in TOK) for task in tasks)
print("tasks_by_distinct_token_count", dict(per_task_kinds))
multi = [s for task in tasks for s in leaves(task) if sum(s.count(t) for t in TOK) > 1]
print("multi_leaves", len(multi), "their_occurrences", sum(sum(s.count(t) for t in TOK) for s in multi))
for m in ["__last_url__", "__page__"]:
    print("marker", m, "occ", raw.count(m), "tasks", sum(m in json.dumps(task) for task in tasks))
print("slash_junction_tasks", sum(any(t + "/" in s for t in TOK for s in leaves(task)) for task in tasks),
      "occ", sum(raw.count(t + "/") for t in TOK))
print("HOMEPAGE_token_in_raw", raw.count("__HOMEPAGE__"))

values = {n: f"http://{n.lower()}.invalid" for n in ORDER}
values["MAP"] = 'http://map.invalid","task_id":999999,"zz":"x'
text = raw
for n in ORDER:
    text = text.replace(f"__{n}__", values[n])
data = json.loads(text)
print("dup_task_id_valid_json", len(data), "tasks_overridden_to_999999", sum(t["task_id"] == 999999 for t in data),
      "distinct_ids_after", len({t["task_id"] for t in data}))

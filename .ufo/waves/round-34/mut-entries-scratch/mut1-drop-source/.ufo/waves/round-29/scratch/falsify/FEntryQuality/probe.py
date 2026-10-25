"""FEntryQuality-2 probes: sites/wikipedia reach, literal hosts, quote-injection outcome class."""
import json
import re
from collections import Counter

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
raw = open(ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json", encoding="utf-8").read()
tasks = json.loads(raw)
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]


def leaves(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for v in obj:
            yield from leaves(v, path + "[]")
    elif isinstance(obj, str):
        yield path, obj


wiki = [t for t in tasks if "wikipedia" in t.get("sites", [])]
print("sites_wikipedia_tasks", len(wiki), "ids", [t["task_id"] for t in wiki])
print("their_start_url_prefixes", dict(Counter(t["start_url"].split("/")[0] for t in wiki)))
print("their_sites_sets", dict(Counter(tuple(sorted(t["sites"])) for t in wiki)))
print("leaves_mentioning_wiki", sum("wiki" in s.lower() for t in wiki for _, s in leaves(t)))

lit = Counter()
for t in tasks:
    for p, s in leaves(t):
        for h in re.findall(r"https?://([^/\"\s]+)", s):
            lit[(p, h)] += 1
print("literal_host_paths", dict(lit))

# Outcome class of a value carrying '"': entry claims invalid JSON or escape decoding only.
values = {n: f"http://{n.lower()}.invalid" for n in ORDER}
values["GITLAB"] = 'http://gitlab.invalid","intent":"INJECTED'
text = raw
for n in ORDER:
    text = text.replace(f"__{n}__", values[n])
try:
    data = json.loads(text)
    t0 = next(t for t in data if t["start_url"].startswith("http://gitlab.invalid"))
    print("quote_value_json_valid True tasks", len(data), "task", t0["task_id"],
          "start_url", repr(t0["start_url"]), "intent", repr(t0["intent"][:40]))
except json.JSONDecodeError as e:
    print("quote_value_json_valid False", e.msg)

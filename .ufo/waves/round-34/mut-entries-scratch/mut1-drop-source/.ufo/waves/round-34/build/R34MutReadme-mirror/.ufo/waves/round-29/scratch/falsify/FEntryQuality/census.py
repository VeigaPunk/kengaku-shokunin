"""Independent census for FEntryQuality-2; derived from generator text + pinned data only."""
import hashlib
import json
import re
from collections import Counter

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
RAW = ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT + "plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {n: f"__{n}__" for n in ORDER}

raw_b = open(RAW, "rb").read()
raw = raw_b.decode("utf-8")
profiles = json.load(open(PROF))
tasks = json.loads(raw)
print("sha_raw", hashlib.sha256(raw_b).hexdigest(), "ascii", raw_b.isascii(), "CR", b"\r" in raw_b)
print("tasks", len(tasks), "distinct_ids", len({t["task_id"] for t in tasks}))
print("index_eq_task_id", sum(i == t["task_id"] for i, t in enumerate(tasks)))

occ = {n: raw.count(TOK[n]) for n in ORDER}
print("occurrences", occ, "total", sum(occ.values()))


def leaves(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for v in obj:
            yield from leaves(v, path + "[]")
    elif isinstance(obj, str):
        yield path, obj


def keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from keys(v)


key_hits = sum(TOK[n] in k for k in keys(tasks) for n in ORDER)
leaf_occ = Counter()
for t in tasks:
    for _, s in leaves(t):
        for n in ORDER:
            leaf_occ[n] += s.count(TOK[n])
print("key_token_hits", key_hits, "leaf_occurrences_equal_text", dict(leaf_occ) == occ)

tasks_with = {n: sum(any(TOK[n] in s for _, s in leaves(t)) for t in tasks) for n in ORDER}
print("tasks_with_token", tasks_with, "sum", sum(tasks_with.values()),
      "any", sum(any(any(TOK[n] in s for n in ORDER) for _, s in leaves(t)) for t in tasks))
all_leaves = [(p, s) for t in tasks for p, s in leaves(t)]
print("string_leaves", len(all_leaves))
changed = [(p, s) for p, s in all_leaves if any(TOK[n] in s for n in ORDER)]
multi = [s for _, s in changed if sum(s.count(TOK[n]) for n in ORDER) > 1]
print("changed_leaves", len(changed), "multi_occ_leaves", len(multi))
print("by_path", dict(Counter(p for p, _ in changed)))
url_paths = {"start_url", "eval.reference_url", "eval.program_html[].url"}
print("url_field", sum(p in url_paths for p, _ in changed), "non_url", sum(p not in url_paths for p, _ in changed))
print("markers", {m: raw.count(m) for m in ["__last_url__", "__page__"]},
      "all_dunder", dict(Counter(re.findall(r"__[A-Za-z_]+?__", raw))))
print("token_then_slash", sum(raw.count(TOK[n] + "/") for n in ORDER))
sites_wiki = sum("wikipedia" in t.get("sites", []) for t in tasks)
print("tasks_sites_wikipedia", sites_wiki)


def project(text, values, order):
    for n in order:
        text = text.replace(TOK[n], values[n])
    return text


for name, prof in profiles.items():
    v = prof["values"]
    fwd = project(raw, v, ORDER)
    rev = project(raw, v, list(reversed(ORDER)))
    parsed = json.loads(fwd)
    remaining = sum(fwd.count(TOK[n]) for n in ORDER)
    print("profile", name, "sha", hashlib.sha256(fwd.encode()).hexdigest()[:16],
          "reverse_identical", fwd == rev, "parsed", len(parsed), "remaining", remaining,
          "double_slash_new", fwd.count("//") - raw.count("//") - 0)

# hard-coded hosts that the six-token replacement never touches
hosts = Counter(re.findall(r"https?://([^/\"\s]+)", raw))
print("literal_url_hosts_in_raw", dict(hosts.most_common(15)))

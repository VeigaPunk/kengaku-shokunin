#!/usr/bin/env python3
"""Upstream-output digest witnesses + structural outlier (review seat R29ReviewLeafIdentity)."""
import hashlib
import json
import os

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(ROOT, "plans/fixtures/r28/webarena/config_files/test.raw.json")
PROF = os.path.join(ROOT, "plans/fixtures/r29/profiles.json")
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {t: "__%s__" % t for t in ORDER}
raw_bytes = open(RAW, "rb").read()
raw_text = raw_bytes.decode("utf-8")
data = json.loads(raw_text)
prof = json.load(open(PROF))

def project(text, values):
    for t in ORDER:
        text = text.replace(TOK[t], values[t])
    return text

print("RAW sha256:", hashlib.sha256(raw_bytes).hexdigest())
for name, spec in prof.items():
    pt = project(raw_text, spec["values"])
    pb = pt.encode("utf-8")
    print("PROFILE", name, "test.json-equivalent bytes:", len(pb),
          "sha256:", hashlib.sha256(pb).hexdigest())

print()
print("=== per-task upstream file digests (json.dumps(item, indent=2), no trailing newline) ===")
for t in [0, 66, 259, 431, 682, 487]:
    for name, spec in prof.items():
        pdata = json.loads(project(json.dumps(data[t]), spec["values"]))
        blob = json.dumps(pdata, indent=2).encode("utf-8")
        print("task", t, name, "bytes", len(blob), "sha256", hashlib.sha256(blob).hexdigest())

print()
print("=== structural outlier: item with extra top-level string_note ===")
for idx, it in enumerate(data):
    if "string_note" in it:
        print("index", idx, "task_id", it["task_id"], "keys", sorted(it.keys()))
        print("  eval keys", sorted(it["eval"].keys()))
        print("  token-bearing?", any(isinstance(v, str) and any(t in v for t in TOK.values())
                                      for v in it.values()))
        print("  start_url", repr(it["start_url"]))
        print("  eval.reference_url", repr(it["eval"]["reference_url"])[:200])
        print("  eval.url_note", repr(it["eval"].get("url_note"))[:200])
        print("  eval.annotation_note", repr(it["eval"].get("annotation_note"))[:200])
        print("  top string_note", repr(it.get("string_note"))[:200])

print()
print("=== geolocation / require_login / require_reset distributions ===")
from collections import Counter
print("geolocation:", Counter(json.dumps(it["geolocation"]) for it in data))
print("require_login:", Counter(it["require_login"] for it in data))
print("require_reset:", Counter(it["require_reset"] for it in data))
print("storage_state distinct:", len({it["storage_state"] for it in data}),
      sorted({it["storage_state"] for it in data}))
print("sites distinct:", sorted({tuple(it["sites"]) for it in data}))
print("intent_template_id distinct:", len({it["intent_template_id"] for it in data}),
      "min", min(it["intent_template_id"] for it in data),
      "max", max(it["intent_template_id"] for it in data))
print("task_id == intent_template_id for how many:", sum(1 for it in data if it["task_id"] == it["intent_template_id"]))
print("geolocation non-null count:", sum(1 for it in data if it["geolocation"] is not None))

print()
print("=== does any non-token leaf differ between profiles? (profiles only touch tokens) ===")
a = json.loads(project(raw_text, prof["distinct_origins"]["values"]))
b = json.loads(project(raw_text, prof["path_prefix"]["values"]))
def leaves(o, p="$", acc=None):
    if acc is None:
        acc = []
    if isinstance(o, dict):
        for k, v in o.items():
            leaves(v, p + "." + k, acc)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            leaves(v, "%s[%d]" % (p, i), acc)
    else:
        acc.append((p, v))
    return acc
la, lb = leaves(a), leaves(b)
print("leaf counts equal:", len(la) == len(lb))
diff = [(p, x, y) for (p, x), (_, y) in zip(la, lb) if x != y]
print("leaves differing between distinct_origins and path_prefix:", len(diff))
print("sample:", [(p, str(x)[:40], str(y)[:40]) for p, x, y in diff[:3]])

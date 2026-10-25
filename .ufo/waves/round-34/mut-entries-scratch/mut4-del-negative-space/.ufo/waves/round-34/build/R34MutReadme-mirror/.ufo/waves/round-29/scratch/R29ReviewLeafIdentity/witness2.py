#!/usr/bin/env python3
"""Witness detail census #2 (review seat R29ReviewLeafIdentity). Read-only."""
import json
import os
import re

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(ROOT, "plans/fixtures/r28/webarena/config_files/test.raw.json")
PROF = os.path.join(ROOT, "plans/fixtures/r29/profiles.json")
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {t: "__%s__" % t for t in ORDER}
raw_text = open(RAW, "rb").read().decode("utf-8")
data = json.loads(raw_text)
prof = json.load(open(PROF))

def leaves(obj, path="$", acc=None):
    if acc is None:
        acc = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            leaves(v, path + "." + k, acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            leaves(v, "%s[%d]" % (path, i), acc)
    else:
        acc.append((path, obj))
    return acc

L = leaves(data)
tok_leaves = [(p, v) for p, v in L if isinstance(v, str) and any(t in v for t in TOK.values())]
print("token_bearing_leaves:", len(tok_leaves))
bare = [p for p, v in tok_leaves if v in TOK.values()]
print("leaves_equal_to_a_bare_token:", len(bare))
print("  bare token distribution:", json.dumps({t: sum(1 for p in bare if data and True) for t in []} ))
from collections import Counter
print("  bare by token:", dict(Counter(v for p, v in tok_leaves if v in TOK.values())))
embedded = [(p, v) for p, v in tok_leaves if v not in TOK.values()]
print("leaves_with_embedded_token:", len(embedded))
print("  embedded with |AND|:", sum(1 for p, v in embedded if "|AND|" in v))
print("  embedded with |OR|:", sum(1 for p, v in embedded if "|OR|" in v))
print("  embedded sample:", [(p, v[:80]) for p, v in embedded[:6]])
print("  all token leaves containing a space:", sum(1 for p, v in tok_leaves if " " in v))
print("  token leaves containing backslash:", sum(1 for p, v in tok_leaves if "\\" in v))
print("  token leaves containing a double quote:", sum(1 for p, v in tok_leaves if '"' in v))

print()
print("raw_text contains '|AND|':", raw_text.count("|AND|"), " '|OR|':", raw_text.count("|OR|"))
print("raw_text contains backslash-u escapes:", raw_text.count("\\u"))
print("raw_text contains literal backslash-n:", raw_text.count("\\n"))
print("raw_text has CRLF:", "\r\n" in raw_text, "ends with newline:", raw_text.endswith("\n"))
print("raw_text first 120 chars:", repr(raw_text[:120]))
print("raw_text last 60 chars:", repr(raw_text[-60:]))

# per-profile witness values for selected tasks
def project(text, values):
    for t in ORDER:
        text = text.replace(TOK[t], values[t])
    return text

print()
print("=== per-profile projected values for witness tasks ===")
for t in [0, 66, 431, 682, 487, 259]:
    item = data[t]
    print("task", t, "task_id", item["task_id"], "sites", item.get("sites"),
          "storage_state", item.get("storage_state"))
    for name, spec in prof.items():
        p = json.loads(project(json.dumps(item), spec["values"]))
        print("   ", name)
        print("      start_url:", repr(p["start_url"])[:150])
        for k in ("reference_url", "reference_answer_raw_annotation"):
            if p["eval"].get(k):
                print("      eval.%s:" % k, repr(p["eval"][k])[:170])
        ph = p["eval"].get("program_html") or []
        for i, prog in enumerate(ph):
            if prog.get("url"):
                print("      eval.program_html[%d].url:" % i, repr(prog["url"])[:150])
            rc = (prog.get("required_contents") or {}).get("must_include") or []
            for j, m in enumerate(rc):
                if "__" in m:
                    print("      eval.program_html[%d].required_contents.must_include[%d]:" % (i, j), repr(m)[:150])

print()
print("=== eval_types distribution over tasks (structural, not consumption claim) ===")
print(dict(Counter(tuple(it["eval"]["eval_types"]) for it in data)))
print("=== top-level keys across all 812 items (union / per-item key set) ===")
keysets = Counter(tuple(sorted(it.keys())) for it in data)
for k, v in keysets.items():
    print("  ", v, k)
print("=== eval key sets ===")
ek = Counter(tuple(sorted(it["eval"].keys())) for it in data)
for k, v in ek.items():
    print("  ", v, k)
print("=== program_html entry key sets ===")
pk = Counter()
for it in data:
    for prog in it["eval"].get("program_html") or []:
        pk[tuple(sorted(prog.keys()))] += 1
for k, v in pk.items():
    print("  ", v, k)

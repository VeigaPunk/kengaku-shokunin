#!/usr/bin/env python3
"""Verify reference_url provenance offsets and sample per-profile leaves."""
import json
import hashlib

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
INST = "/tmp/r29_fpathrefurl_2.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__",
          "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]

raw_text = open(RAW, encoding="utf-8").read()
raw = json.loads(raw_text)
inst = json.load(open(INST))

# 1. all token occurrences live in string values, not keys
def walk(o, p=""):
    if isinstance(o, str):
        yield p, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, p + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, p + "/" + str(i))

value_occ = {t: 0 for t in TOKENS}
for t in raw:
    for p, v in walk(t):
        for tok in TOKENS:
            value_occ[tok] += v.count(tok)
print("string_value_occurrences", json.dumps(value_occ, sort_keys=True),
      "sum", sum(value_occ.values()), "raw_text_sum",
      sum(raw_text.count(t) for t in TOKENS))

# 2. provenance offsets: slice check + containment in the task's reference_url literal
op = inst["occurrence_provenance"]
ref_entries = [e for e in op if e["path_template"] == "eval.reference_url"]
print("ref_entries", len(ref_entries),
      "pointer_ok", all(e["json_pointer"] == "/%d/eval/reference_url" % e["task_index"] for e in ref_entries),
      "role", sorted({e["string_role"] for e in ref_entries}))
bad_slice = [e for e in op if raw_text[e["original_input_codepoint_offset"]:
                                    e["original_input_codepoint_offset"] + len(e["token"])] != e["token"]]
print("bad_slice_all", len(bad_slice))
# containment in reference_url leaf literal
seen = {}
contain_bad = []
for e in ref_entries:
    idx = e["task_index"]
    v = raw[idx]["eval"]["reference_url"]
    tok = e["token"]
    k = seen.get((idx, tok), 0)
    seen[(idx, tok)] = k + 1
    pos = -1
    for _ in range(k + 1):
        pos = v.find(tok, pos + 1)
    if pos < 0:
        contain_bad.append((idx, tok, "no_occurrence_index"))
        continue
    start = e["original_input_codepoint_offset"] - pos
    if raw_text[start:start + len(v)] != v:
        contain_bad.append((idx, tok, start, raw_text[start:start + len(v)][:60]))
    elif raw_text[start - 1] != '"':
        contain_bad.append((idx, tok, "not_value_start", raw_text[start - 1:start + 10]))
print("ref_containment_bad", len(contain_bad), contain_bad[:3])
print("ref_offsets_sorted", [e["original_input_codepoint_offset"] for e in ref_entries] ==
      sorted(e["original_input_codepoint_offset"] for e in ref_entries))

# 3. five samples per profile spanning tokens (incl. a multi-occurrence leaf)
# pick task indices: multi-occ REDDIT leaf, GITLAB, SHOPPING, SHOPPING_ADMIN, MAP
ref_by_task = {}
for idx, t in enumerate(raw):
    v = t["eval"]["reference_url"]
    if isinstance(v, str) and any(tok in v for tok in TOKENS):
        ref_by_task[idx] = v
multi = [(idx, v) for idx, v in ref_by_task.items()
         if sum(v.count(tok) for tok in TOKENS) > 1]
print("multi_occ_ref_tasks", [(i, v.count("__REDDIT__")) for i, v in multi])
picks = [multi[0][0]]
for tok in ["__GITLAB__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__MAP__"]:
    for idx, v in ref_by_task.items():
        if tok in v and idx not in picks:
            picks.append(idx)
            break
print("picks", picks)

for pname, prof in inst["profiles"].items():
    values = prof["values"]
    recs = {}
    for t in prof["tasks"]:
        for cl in t["changed_leaves"]:
            if cl["path_template"] == "eval.reference_url":
                recs[t["output_index"]] = cl
    print("PROFILE", pname, "ref_records", len(recs))
    for idx in picks:
        cl = recs[idx]
        ov, pv = cl["original"], cl["projected"]
        # hand derivation: sequential replacement on the decoded original leaf
        hand = ov
        steps = []
        for name in ORDER:
            tok = "__" + name + "__"
            if tok in hand:
                steps.append((tok, hand.count(tok), values[name]))
                hand = hand.replace(tok, values[name])
        print(json.dumps({
            "task": idx, "pointer": cl["json_pointer"], "category": cl["category"],
            "original": ov, "instrument_projected": pv, "hand_projected": hand,
            "hand_steps": steps, "equal": hand == pv,
            "raw_has_token_literal": ("\"" + ov + "\"") in raw_text,
            "tokens_field": cl["tokens"],
        }, ensure_ascii=False))

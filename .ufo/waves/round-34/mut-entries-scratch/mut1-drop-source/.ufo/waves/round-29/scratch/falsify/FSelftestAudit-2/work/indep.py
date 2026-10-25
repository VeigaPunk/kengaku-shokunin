#!/usr/bin/env python3
"""Independent checks (no production import):
 A) Does any selftest case exercise >1 distinct URL-field template, or program_html nesting?
 B) Are the three hand fixtures' expected values independently derivable?
 C) Does the real frozen input contain overlapping URL/non-URL contexts under program_html[]?
"""
import json, re
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
HAND = LANE / "plans/fixtures/r29/hand"
ORDER = ("GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP")

# ---------- A) selftest case inputs: which URL templates appear? ----------
URL_T = {"start_url","eval.reference_url","eval.program_html[].url"}
inputs = {
 "six_tokens": json.dumps([{"task_id":0,"start_url":"__X__/p","intent":"see __X__"}]),
 "units_not_pooled": '[{"task_id": 0, "start_url": "__GITLAB__/a |OR| __GITLAB__/b", "x": ["__REDDIT__"]}]',
 "codepoint": '[{"intent": "\u00e9\u00e9 __MAP__", "__GITLAB__": 1}]',
 "escaped": '[{"intent": "\\u005f\\u005fGITLAB__ and __GITLAB__"}]',
 "quote_backslash": '[{"start_url": "__GITLAB__"}]',
 "url_only_fixture": json.loads((HAND/"url-only.fixture.json").read_text())["raw_text"],
 "index_fixture": json.loads((HAND/"index-shuffled-ids.fixture.json").read_text())["input_raw_text"],
 "cascade_fixture": json.loads((HAND/"cascade-order.case.json").read_text())["raw_serialized_text"],
}
def templates(text):
    out=set()
    for m in re.finditer(r'"([A-Za-z0-9_\[\]]+)"\s*:', text):
        out.add(m.group(1))
    return out
print("== A) selftest case inputs: JSON keys present")
for k,v in inputs.items():
    print("   %-20s keys=%s" % (k, sorted(templates(v))))
print("   url-only fixture evaluated program_html/reference_url values:")
uo_raw = json.loads((HAND/"url-only.fixture.json").read_text())["raw_text"]
uo_obj = json.loads(uo_raw)[0]
print("     eval.reference_url=%r  eval.program_html=%r" % (
    uo_obj["eval"]["reference_url"], uo_obj["eval"]["program_html"]))
print("   => selftest input with NON-EMPTY eval.reference_url or eval.program_html? ",
      bool(uo_obj["eval"]["reference_url"]) or bool(uo_obj["eval"]["program_html"]))

# ---------- B) independent re-derivation of the three hand fixtures ----------
print()
print("== B) independent re-derivation of hand-fixture expected values")

def project(text, values):
    for n in ORDER:
        text = text.replace("__%s__" % n, values[n])
    return text

# B1 cascade
c = json.loads((HAND/"cascade-order.case.json").read_text())
mine = project(c["raw_serialized_text"], c["values"])
print("   cascade expected_projected_text == independently derived:",
      mine == c["expected_projected_text"])
steps=[]
t=c["raw_serialized_text"]
for n in ORDER:
    steps.append(t.count("__%s__"%n)); t=t.replace("__%s__"%n, c["values"][n])
print("   cascade expected_dynamic_replacement_hits_by_source_step == derived:",
      steps == c["expected_dynamic_replacement_hits_by_source_step"], steps)
print("   cascade expected_after_each_source_step == derived:",
      [s["text"] for s in c["expected_after_each_source_step"]] ==
      [x for x in _derive_steps(c["raw_serialized_text"], c["values"])] if False else "checked below")

def derive_steps(text, values):
    out=[]
    for n in ORDER:
        text = text.replace("__%s__" % n, values[n])
        out.append(text)
    return out
ds = derive_steps(c["raw_serialized_text"], c["values"])
print("      derived steps == fixture expected_after_each_source_step:",
      ds == [s["text"] for s in c["expected_after_each_source_step"]])

# B2 url-only
u = json.loads((HAND/"url-only.fixture.json").read_text())
ue = json.loads((HAND/"url-only.expected.json").read_text())
mine_txt = project(u["raw_text"], u["values"])
mine_obj = json.loads(mine_txt)
print("   url-only projection == independently derived:",
      mine_obj == ue["projection"])
occ = {("__%s__"%n): u["raw_text"].count("__%s__"%n) for n in ORDER}
print("   url-only occurrences == independently derived:",
      occ == ue["raw_replacement_occurrences_by_token"])
# expected_mutant: a URL-only substitution leaves non-URL leaves unchanged
uo_only = json.loads(u["raw_text"])
def url_only(node):
    if isinstance(node, dict):
        for k2,v2 in list(node.items()):
            if k2 in ("start_url","reference_url","url") and isinstance(v2,str):
                for n in ORDER: v2 = v2.replace("__%s__"%n, u["values"][n])
                node[k2]=v2
            elif isinstance(v2,(dict,list)): url_only(v2)
    elif isinstance(node,list):
        for i in node: url_only(i)
url_only(uo_only)
def leaf_paths(o, p=()):
    out={}
    if isinstance(o,dict):
        for k,v in o.items(): out.update(leaf_paths(v,p+(k,)))
    elif isinstance(o,list):
        for i,v in enumerate(o): out.update(leaf_paths(v,p+(i,)))
    elif isinstance(o,str): out[p]=o
    return out
a=leaf_paths(json.loads(u["raw_text"])); b=leaf_paths(uo_only)
mut_changed=[list(k) for k in a if a[k]!=b[k]]
print("   url-only mutant changed paths == expected_mutant.changed_string_leaf_paths:",
      sorted(mut_changed)==sorted(ue["expected_mutant"]["changed_string_leaf_paths"]), sorted(mut_changed))
rem = sum(v.count("__GITLAB__")+v.count("__REDDIT__")+v.count("__SHOPPING__")+v.count("__SHOPPING_ADMIN__")+v.count("__WIKIPEDIA__")+v.count("__MAP__") for v in b.values())
print("   url-only mutant remaining token occurrences == expected_mutant.remaining:",
      rem == ue["expected_mutant"]["remaining_known_environment_token_occurrences"], rem)
print("   => expected_mutant IS asserted by selftest? ", '"expected_mutant"' in (LANE/"plans/config_projection.py").read_text())

# B3 index
i = json.loads((HAND/"index-shuffled-ids.fixture.json").read_text())
mine_i = json.loads(project(i["input_raw_text"], i["profile_values"]))
recs = [{"task_id": t.get("task_id"), "output_ordinal": n, "output_filename": "config_files/%d.json"%n,
         "projected_task": t} for n,t in enumerate(mine_i)]
print("   index expected_records == independently derived:", recs == i["expected_records"])
print("   index expected_index_equals_task_id == derived:",
      [t.get("task_id")==n for n,t in enumerate(mine_i)] == i["expected_index_equals_task_id"])
print("   index expected_filename_to_task_id == derived:",
      {"config_files/%d.json"%n: t.get("task_id") for n,t in enumerate(mine_i)} == i["expected_filename_to_task_id"])
print("   index expected_projected_raw_text == derived:",
      project(i["input_raw_text"], i["profile_values"]) == i["expected_projected_raw_text"])

# ---------- C) real input overlapping contexts ----------
print()
print("== C) frozen real input: overlapping URL / non-URL leaf contexts")
raw = json.loads((LANE/"plans/fixtures/r28/webarena/config_files/test.raw.json").read_text())
ph_overlap = 0
for t in raw:
    ev = t.get("eval") or {}
    for ph in (ev.get("program_html") or []):
        if "url" in ph and "required_contents" in ph:
            ph_overlap += 1
print("   program_html[] entries with BOTH url and required_contents:", ph_overlap)
print("   (=> nested overlapping field contexts exist in the frozen input but in NO selftest case)")

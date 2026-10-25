#!/usr/bin/env python3
"""Summary-vs-JSON internal consistency + exact set/template equality for the target token."""
import json
import os
import re
from collections import Counter, defaultdict

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
S = os.path.join(LANE, ".ufo/waves/round-29/scratch/falsify/FTokenShopping")
RAW = os.path.join(LANE, "plans/fixtures/r28/webarena/config_files/test.raw.json")
PROF = os.path.join(LANE, "plans/fixtures/r29/profiles.json")
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
          "__WIKIPEDIA__", "__MAP__"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TARGET = "__SHOPPING__"

raw = open(RAW, "rb").read().decode("utf-8")
prof = json.load(open(PROF, "r", encoding="utf-8"))
inst = json.load(open(os.path.join(S, "instrument.json"), "r", encoding="utf-8"))
summ = open(os.path.join(S, "s1.txt"), "r", encoding="utf-8").read().splitlines()


def walk(node, ptr="", tptr="", root=True):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, ptr + "/" + k, (tptr + "." + k) if tptr else k, False)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, ptr + "/" + str(i), tptr if root else tptr + "[]", False)
    elif isinstance(node, str):
        yield ptr, tptr, node


data = json.loads(raw)
leaves = list(walk(data))
tpl = {p: t for p, t, s in leaves}
leaf_s = {p: s for p, t, s in leaves}

# ---------- A. summary text -> numbers ----------
kv = {}
for line in summ:
    m = re.match(r"^([A-Z_]+) (\{.*\}|[^\s].*)$", line)
    if m:
        kv.setdefault(m.group(1), []).append(m.group(2))
print("=== A. SUMMARY LINES SEEN ===")
for k, v in kv.items():
    print(k, len(v))

def jload(s):
    return json.loads(s)

con = 0
def chk(name, a, b):
    global con
    ok = a == b
    if not ok:
        con += 1
    print(("MATCH   " if ok else "MISMATCH"), name, "summary", a, "json", b)

chk("POPULATION", jload(kv["POPULATION"][0]), inst["population"] and {
    k: inst["population"][k] for k in
    ["distinct_task_ids", "input_task_count", "profile_count",
     "task_profile_projections", "tasks_with_any_token"]})
chk("ORIGINAL_OCCURRENCES_BY_TOKEN", jload(kv["ORIGINAL_OCCURRENCES_BY_TOKEN"][0]),
    inst["population"]["original_occurrences_by_token"])
chk("TASKS_WITH_TOKEN", jload(kv["TASKS_WITH_TOKEN"][0]),
    inst["population"]["tasks_with_token"])
chk("OCCURRENCE_ROLES", jload(kv["OCCURRENCE_ROLES"][0]),
    inst["population"]["occurrence_roles"])
chk("OTHER_MARKERS", jload(kv["OTHER_MARKERS_NOT_ENV_TOKENS"][0]),
    inst["population"]["other_double_underscore_markers"])
chk("INDEX", jload(kv["INDEX"][0]), inst["index_mapping"])
# per-profile
plines = defaultdict(lambda: defaultdict(list))
for line in summ:
    m = re.match(r'^PROFILE (\S+) (\w+)=(.*)$', line)
    if m:
        plines[m.group(1)][m.group(2)].append(m.group(3))
for pname in prof:
    ip = inst["profiles"][pname]
    d = plines[pname]
    chk(pname + ".applied", jload(d["applied_replacements"][0]),
        {s["token"].strip("_") if s["token"].startswith("__") else s["token"]: s["applied_replacements"] for s in ip["steps"]})
    chk(pname + ".changed_leaves_by_token", jload(d["changed_leaves_by_token"][0]),
        ip["changed_leaves_by_token"])
    chk(pname + ".changed_tasks_by_token", jload(d["changed_tasks_by_token"][0]),
        ip["changed_tasks_by_token"])
    chk(pname + ".by_category", jload(d["changed_leaves_by_category"][0]),
        ip["changed_leaves_by_category"])
    chk(pname + ".by_path_template", jload(d["changed_leaves_by_path_template"][0]),
        ip["changed_leaves_by_path_template"])
    chk(pname + ".remaining_text", jload(d["remaining_known_tokens_text"][0]),
        ip["remaining_known_tokens_text"])
    chk(pname + ".remaining_decoded", jload(d["remaining_known_tokens_decoded"][0]),
        ip["remaining_known_tokens_decoded"])
    chk(pname + ".stimulus", jload(d["stimulus_observations"][0]),
        ip["stimulus_observations"])
    scalar = {}
    for line2 in summ:
        if line2.startswith("PROFILE %s " % pname):
            for m2 in re.finditer(r'(\w+)=(\S+)', line2):
                if m2.group(1) not in scalar:
                    scalar[m2.group(1)] = m2.group(2)
    chk(pname + ".parsed_task_count", int(scalar["parsed_task_count"]), ip["parsed_task_count"])
    chk(pname + ".string_leaf_count", int(scalar["string_leaf_count"]), ip["string_leaf_count"])
    chk(pname + ".changed_leaf_count", int(scalar["changed_leaf_count"]), ip["changed_leaf_count"])
    chk(pname + ".changed_task_count", int(scalar["changed_task_count"]), ip["changed_task_count"])
    chk(pname + ".digest", scalar["projected_text_sha256"], ip["projected_text_sha256"])

print("summary_vs_json_mismatches", con)

# ---------- B. exact sets from JSON per-task changed_leaves ----------
print("\n=== B. EXACT TASK/LEAF SETS FOR TARGET FROM JSON ===")
ip = inst["profiles"]["distinct_origins"]
tasks_with_mine = {int(p.split("/")[1]) for p, s in leaf_s.items() if TARGET in s}
json_tok_tasks = set()
json_tok_ptr = Counter()
for t in ip["tasks"]:
    for c in t["changed_leaves"]:
        if TARGET in c["tokens"]:
            json_tok_tasks.add(t["output_index"])
            json_tok_ptr[c["json_pointer"]] += 1
mine_ptr = Counter(p for p, s in leaf_s.items() if TARGET in s)
print("task set equal", tasks_with_mine == json_tok_tasks,
      "mine", len(tasks_with_mine), "json", len(json_tok_tasks),
      "symdiff", sorted(tasks_with_mine ^ json_tok_tasks)[:10])
print("leaf pointer set equal", set(mine_ptr) == set(json_tok_ptr),
      "symdiff", sorted(set(mine_ptr) ^ set(json_tok_ptr))[:10])
print("per-task leaf count equal", all(
    Counter(c["json_pointer"] for c in t["changed_leaves"] if TARGET in c["tokens"]) ==
    Counter(p for p in mine_ptr if int(p.split("/")[1]) == t["output_index"])
    for t in ip["tasks"]))
# ADMIN vs SHOPPING confusion: any JSON leaf whose tokens contain ADMIN but whose original lacks ADMIN?
bad = [(t["output_index"], c["json_pointer"]) for t in ip["tasks"] for c in t["changed_leaves"]
       if "__SHOPPING_ADMIN__" in c["tokens"] and "__SHOPPING_ADMIN__" not in c["original"]]
print("admin-token attribution errors", len(bad), bad[:5])
bad2 = [(t["output_index"], c["json_pointer"]) for t in ip["tasks"] for c in t["changed_leaves"]
        if TARGET in c["tokens"] and TARGET not in c["original"]]
print("target-token attribution errors", len(bad2), bad2[:5])
# every changed leaf's projected == original.replace for each token present
bad3 = 0
for pname, pdef in prof.items():
    for t in inst["profiles"][pname]["tasks"]:
        for c in t["changed_leaves"]:
            exp = c["original"]
            for tok in c["tokens"]:
                exp = exp.replace(tok, pdef["values"][tok.strip("_")])
            if exp != c["projected"]:
                bad3 += 1
print("changed-leaf projected != per-token replace", bad3)

# ---------- C. templates ----------
print("\n=== C. TEMPLATE CENSUS EXACT ===")
tcnt = Counter(tpl[p] for p, s in leaf_s.items() if TARGET in s)
print("TARGET templates", dict(sorted(tcnt.items())))
vals = prof["distinct_origins"]["values"]
text = raw
for name in ORDER:
    text = text.replace("__%s__" % name, vals[name])
proj = json.loads(text)
pwalk = {p: s for p, t, s in walk(proj)}
allchg = Counter(tpl[p] for p, s in leaf_s.items() if pwalk.get(p) != s)
print("all changed templates mine", dict(sorted(allchg.items())))
print("instrument", dict(sorted(ip["changed_leaves_by_path_template"].items())))
print("template_match_exact", dict(allchg) == ip["changed_leaves_by_path_template"])
print("target template sum", sum(tcnt.values()), "target leaves", len(mine_ptr))

# ---------- D. offsets ----------
print("\n=== D. OFFSET ORDERING ===")
rows = [r for r in inst["occurrence_provenance"] if r["token"] == TARGET]
offs = [r["original_input_codepoint_offset"] for r in rows]
print("sorted_ascending", offs == sorted(offs), "unique", len(set(offs)) == len(offs),
      "min", min(offs), "max", max(offs), "in_bounds", max(offs) + len(TARGET) <= len(raw))
# each offset's pointer: the token must lie within that leaf's raw occurrence; check by
# counting how many rows per pointer and compare to leaf census (already done)
print("rows_per_pointer == leaf_occurrence_census",
      Counter(r["json_pointer"] for r in rows) == Counter({p: s.count(TARGET) for p, s in leaf_s.items() if TARGET in s}))
# raw text between consecutive offsets distance
gaps = [offs[i + 1] - offs[i] for i in range(len(offs) - 1)]
print("min_gap", min(gaps), "max_gap", max(gaps))

# ---------- E. per-task target occurrence distribution ----------
print("\n=== E. PER-TASK TARGET OCCURRENCE DISTRIBUTION ===")
per_task_occ = Counter()
for p, s in leaf_s.items():
    n = s.count(TARGET)
    if n:
        per_task_occ[int(p.split("/")[1])] += n
print("dist", dict(sorted(Counter(per_task_occ.values()).items())),
      "total_tasks", len(per_task_occ), "total_occ", sum(per_task_occ.values()))
print("tasks with >1 target occurrence", sorted(k for k, v in per_task_occ.items() if v > 1))
print("max per task", max(per_task_occ.values()))
# index==task_id for target tasks
print("target tasks index==task_id all",
      all(data[i]["task_id"] == i for i in tasks_with_mine))
print("output filenames sample", [t["output_filename"] for t in ip["tasks"]
                                  if t["output_index"] in sorted(tasks_with_mine)[:3]])

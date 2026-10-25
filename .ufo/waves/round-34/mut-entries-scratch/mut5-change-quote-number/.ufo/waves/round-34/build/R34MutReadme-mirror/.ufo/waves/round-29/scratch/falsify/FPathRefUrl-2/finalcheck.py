#!/usr/bin/env python3
"""Final consistency attack: summary text vs JSON records; provenance multisets."""
import json
import re
import subprocess
import collections

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
INST = "/tmp/r29_fpathrefurl_2.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__",
          "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
URL_TEMPLATES = {"start_url", "eval.reference_url", "eval.program_html[].url"}

raw_text = open(RAW, encoding="utf-8").read()
raw = json.loads(raw_text)
inst = json.load(open(INST))
summary = subprocess.run(
    ["python3", LANE + "/plans/config_projection.py", "--summary"],
    capture_output=True, text=True).stdout

# parse summary PROFILE lines
lines = collections.defaultdict(dict)
cur = None
for ln in summary.splitlines():
    m = re.match(r"PROFILE (\S+) (.*)", ln)
    if not m:
        continue
    cur = m.group(1)
    for km in re.finditer(r"(\w+)=(.*?)(?= \b\w+\b=|$)", m.group(2)):
        lines[cur][km.group(1)] = km.group(2)

problems = []
for name, prof in inst["profiles"].items():
    recs = []
    for t in prof["tasks"]:
        for cl in t["changed_leaves"]:
            recs.append((t["output_index"], cl))
    by_tmpl = collections.Counter(cl["path_template"] for _, cl in recs)
    by_cat = collections.Counter(cl["category"] for _, cl in recs)
    by_tok = collections.Counter(tok for _, cl in recs for tok in set(cl["tokens"]))
    multi = sum(1 for _, cl in recs
                if sum(cl["original"].count(t) for t in TOKENS) > 1)
    tasks = len({i for i, _ in recs})
    s = lines[name]
    checks = {
        "changed_leaf_count": (len(recs), int(s["changed_leaf_count"])),
        "changed_task_count": (tasks, int(s["changed_task_count"])),
        "string_leaf_count": (prof["string_leaf_count"], int(s["string_leaf_count"])),
        "parsed_task_count": (prof["parsed_task_count"], int(s["parsed_task_count"])),
        "changed_leaves_with_multiple_occurrences": (multi, int(s["changed_leaves_with_multiple_occurrences"])),
    }
    for k, (a, b) in checks.items():
        if a != b:
            problems.append((name, k, a, b))
    s_tmpl = json.loads(s["changed_leaves_by_path_template"].replace("'", '"').replace("must_include[]", "must_include"))
    s_cat = json.loads(s["changed_leaves_by_category"].replace("'", '"'))
    s_tok_changed = json.loads(s["changed_leaves_by_token"].replace("'", '"'))
    print(name, "summary_vs_json",
          "tmpl", dict(by_tmpl) == s_tmpl,
          "cat", dict(by_cat) == s_cat,
          "tok", dict(by_tok) == s_tok_changed,
          "tmpl_json", dict(by_tmpl), "cat_json", dict(by_cat))
    if dict(by_tmpl) != s_tmpl:
        problems.append((name, "summary_tmpl", dict(by_tmpl), s_tmpl))
    if dict(by_cat) != s_cat:
        problems.append((name, "summary_cat", dict(by_cat), s_cat))
    if dict(by_tok) != s_tok_changed:
        problems.append((name, "summary_tok", dict(by_tok), s_tok_changed))

# reference_url provenance multiset vs leaf census occurrences
op = inst["occurrence_provenance"]
prov = collections.Counter((e["task_index"], e["token"]) for e in op
                           if e["path_template"] == "eval.reference_url")
census = collections.Counter()
for idx, t in enumerate(raw):
    v = t["eval"]["reference_url"]
    if isinstance(v, str):
        for tok in TOKENS:
            census[(idx, tok)] += v.count(tok)
print("ref_provenance_multiset_equal", prov == census,
      "prov_total", sum(prov.values()), "census_total", sum(census.values()))
if prov != census:
    problems.append(("ref_prov_multiset", prov, census))
print("ref_prov_by_token", {t: sum(n for (i, tk), n in prov.items() if tk == t) for t in TOKENS})

# annotation leaf (2 occurrences, 1 changed leaf, non_url category)
ann = [(idx, t["eval"]["reference_answer_raw_annotation"])
       for idx, t in enumerate(raw)
       if any(tok in str(t["eval"]["reference_answer_raw_annotation"]) for tok in TOKENS)]
print("annotation_leaves_with_token", ann)
for idx, v in ann:
    print("annotation_counts", idx, {t: v.count(t) for t in TOKENS if t in v})

# reference_url key occurrences at other JSON paths
counts = collections.Counter()
def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "reference_url":
                counts[p] += 1
            walk(v, p + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, p + "/" + str(i))
for t in raw:
    walk(t)
print("reference_url_key_paths", dict(counts))

# sample equality table + raw span evidence
ref_by_task = {i: t["eval"]["reference_url"] for i, t in enumerate(raw)
               if isinstance(t["eval"]["reference_url"], str)
               and any(tok in t["eval"]["reference_url"] for tok in TOKENS)}
picks = [604, 44, 158, 157, 377]
for pname, prof in inst["profiles"].items():
    recs = {t["output_index"]: cl for t in prof["tasks"] for cl in t["changed_leaves"]
            if cl["path_template"] == "eval.reference_url"}
    for idx in picks:
        cl = recs[idx]
        print("SAMPLE", pname, idx, cl["category"],
              "equal=%s" % (cl["projected"] == ref_by_task[idx].replace(
                  "__GITLAB__", prof["values"]["GITLAB"]).replace(
                  "__REDDIT__", prof["values"]["REDDIT"]).replace(
                  "__SHOPPING__", prof["values"]["SHOPPING"]).replace(
                  "__SHOPPING_ADMIN__", prof["values"]["SHOPPING_ADMIN"]).replace(
                  "__WIKIPEDIA__", prof["values"]["WIKIPEDIA"]).replace(
                  "__MAP__", prof["values"]["MAP"])))
print("PROBLEMS", len(problems))
for p in problems:
    print("PROBLEM", p)

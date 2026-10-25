#!/usr/bin/env python3
"""FHistIdentity independent census of pinned WebArena test.raw.json.

Reads ONLY the raw JSON via stdlib. Does NOT import benchmark_spec_audit.py
or plans/fixtures/r28/benchmark_oracle.py. Every number derived here is an
author-side independent reimplementation.
"""
import collections
import json
import sys

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"

tasks = json.load(open(RAW))
assert isinstance(tasks, list), type(tasks)

out = {"task_count": len(tasks)}
positions_of = {}
ids = []
non_int_ids = []
for pos, task in enumerate(tasks):
    tid = task.get("task_id") if isinstance(task, dict) else None
    if type(tid) is int:
        ids.append(tid)
        positions_of.setdefault(tid, []).append(pos)
    else:
        non_int_ids.append((pos, repr(tid)))

counter = collections.Counter(ids)
dup_ids = sorted(t for t, c in counter.items() if c > 1)
expected = set(range(812))
missing = sorted(expected - set(ids))
unexpected = sorted(set(ids) - expected)
out["id_rows"] = len(ids)
out["non_int_task_id_positions"] = non_int_ids
out["distinct_task_ids"] = len(set(ids))
out["id_min"] = min(ids)
out["id_max"] = max(ids)
out["duplicate_task_ids"] = dup_ids
out["duplicate_occurrences"] = {str(t): counter[t] for t in dup_ids}
out["missing_task_ids"] = missing
out["unexpected_task_ids"] = unexpected
out["ids_are_exactly_0_811"] = (set(ids) == expected and len(ids) == 812 and not dup_ids)

# eval-type set/order histograms (sorted-set labels like the audit groups them)
set_hist = collections.Counter()
order_hist = collections.Counter()
nonlist_eval = []
for pos, task in enumerate(tasks):
    kinds = task.get("eval", {}).get("eval_types")
    if isinstance(kinds, list) and kinds:
        set_hist[",".join(sorted(kinds))] += 1
        order_hist[",".join(kinds)] += 1
    else:
        nonlist_eval.append(pos)
out["eval_type_sets"] = dict(sorted(set_hist.items()))
out["eval_type_set_kinds"] = len(set_hist)
out["eval_type_orders"] = dict(sorted(order_hist.items()))
out["nonlist_eval_types_positions"] = nonlist_eval

# site sets
site_hist = collections.Counter()
for task in tasks:
    sites = task.get("sites")
    site_hist[",".join(sorted(sites)) if isinstance(sites, list) else "<invalid>"] += 1
out["site_sets"] = dict(sorted(site_hist.items()))
out["site_set_kinds"] = len(site_hist)

# strata: (sorted sites, sorted eval types) -> min task_id; first16 lexicographic
strata = collections.defaultdict(list)
for task in tasks:
    tid, sites = task.get("task_id"), task.get("sites")
    kinds = task.get("eval", {}).get("eval_types")
    if type(tid) is int and isinstance(sites, list) and sites and all(isinstance(s, str) and s for s in sites) \
            and isinstance(kinds, list) and kinds and all(isinstance(k, str) for k in kinds):
        strata[(tuple(sorted(sites)), tuple(sorted(kinds)))].append(tid)
out["site_eval_strata"] = len(strata)
out["selected_task_ids"] = [min(v) for k, v in sorted(strata.items())][:16]
out["strata_listing"] = ["|".join(k[0]) + " // " + "|".join(k[1]) + " -> " + ",".join(map(str, sorted(v))) for k, v in sorted(strata.items())]

# flags
out["login_flags"] = dict(sorted(collections.Counter(str(t.get("require_login")).lower() for t in tasks).items()))
out["reset_flags"] = dict(sorted(collections.Counter(str(t.get("require_reset")).lower() for t in tasks).items()))

# string_match operators (operator keys per task; operators may coexist)
str_hist = collections.Counter()
na_without_note = 0
for task in tasks:
    if "string_match" in task.get("eval", {}).get("eval_types", []):
        refs = task["eval"].get("reference_answers", {})
        for op in refs:
            str_hist[op] += 1
        if refs.get("fuzzy_match") == "N/A" and not isinstance(task["eval"].get("string_note"), str):
            na_without_note += 1
out["string_operators"] = dict(sorted(str_hist.items()))
out["na_fuzzy_without_string_note"] = na_without_note

# url_match rules / reference_url
url_rules = collections.Counter()
empty_alt = []
for pos, task in enumerate(tasks):
    ev = task.get("eval", {})
    if "url_match" in ev.get("eval_types", []):
        rule = ev.get("url_note", "GOLD in PRED")
        url_rules[str(rule)] += 1
        ref = ev.get("reference_url")
        if isinstance(ref, str) and any(not a for a in ref.split(" |OR| ")):
            empty_alt.append(pos)
out["url_rules"] = dict(sorted(url_rules.items()))
out["empty_url_alternative_positions"] = empty_alt

# program_html targets
def classify_locator(value):
    if not value.strip():
        return "full_page"
    if value.startswith("document.") or value.startswith("[...document."):
        return "javascript"
    if value.startswith("func:"):
        return "helper"
    return "unsupported"

targets = 0
html_ops = collections.Counter()
loc_classes = collections.Counter()
url_classes = collections.Counter()
both_ops = []
unsupported_loc = []
malformed_func_url = []
for pos, task in enumerate(tasks):
    ev = task.get("eval", {})
    if "program_html" in ev.get("eval_types", []):
        tl = ev.get("program_html", [])
        targets += len(tl)
        for i, tgt in enumerate(tl):
            if not isinstance(tgt, dict):
                continue
            url = tgt.get("url")
            if isinstance(url, str) and url:
                url_classes["last" if url == "last" else "helper" if url.startswith("func") else "navigation"] += 1
                if url.startswith("func") and not url.startswith("func:"):
                    malformed_func_url.append((pos, i))
            loc = tgt.get("locator")
            if isinstance(loc, str):
                c = classify_locator(loc)
                loc_classes[c] += 1
                if c == "unsupported":
                    unsupported_loc.append((pos, i, loc[:60]))
            req = tgt.get("required_contents")
            if isinstance(req, dict):
                if "exact_match" in req and "must_include" in req:
                    both_ops.append((pos, i))
                op = "exact_match" if "exact_match" in req else "must_include" if "must_include" in req else None
                if op:
                    html_ops[op] += 1
out["program_html_targets"] = targets
out["html_operators"] = dict(sorted(html_ops.items()))
out["locator_classes"] = dict(sorted(loc_classes.items()))
out["target_url_classes"] = dict(sorted(url_classes.items()))
out["targets_with_both_ops"] = both_ops
out["unsupported_locators"] = unsupported_loc
out["malformed_func_urls"] = malformed_func_url

json.dump(out, open(sys.argv[1], "w"), indent=2, sort_keys=True)
print("WROTE", sys.argv[1])
print("task_count=%d distinct=%d min=%d max=%d dup=%d missing=%d unexpected=%d exact0811=%s" % (
    out["task_count"], out["distinct_task_ids"], out["id_min"], out["id_max"],
    len(dup_ids), len(missing), len(unexpected), out["ids_are_exactly_0_811"]))
print("eval_type_sets=%s" % out["eval_type_sets"])
print("strata=%d selected=%s" % (out["site_eval_strata"], out["selected_task_ids"]))
print("string_ops=%s targets=%d html_ops=%s locators=%s url_classes=%s" % (
    out["string_operators"], targets, out["html_operators"], out["locator_classes"], out["target_url_classes"]))
print("login=%s reset=%s url_rules=%s" % (out["login_flags"], out["reset_flags"], out["url_rules"]))

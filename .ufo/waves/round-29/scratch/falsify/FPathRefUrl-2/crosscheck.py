#!/usr/bin/env python3
"""Cross-check instrument --json/--summary output against independent census."""
import json
import sys

CENSUS = "/tmp/r29_fpathrefurl_2_census.json"
INST = "/tmp/r29_fpathrefurl_2.json"
RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__",
          "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
URL_TEMPLATES = {"start_url", "eval.reference_url", "eval.program_html[].url"}

census = json.load(open(CENSUS))
inst = json.load(open(INST))
raw = json.load(open(RAW))

mismatches = []
print("instrument findings", len(inst["findings"]))
for name, prof in inst["profiles"].items():
    c = census[name]
    canon = {
        "eval.program_html.required_contents.must_include.[]": "eval.program_html[].required_contents.must_include[]",
        "eval.program_html.url": "eval.program_html[].url",
    }
    my_tmpl = {canon.get(k, k): v for k, v in c["by_template"].items()}
    my_cat = {"url_field": 0, "non_url_field": 0}
    for t, n in my_tmpl.items():
        my_cat["url_field" if t in URL_TEMPLATES else "non_url_field"] += n
    if my_tmpl != prof["changed_leaves_by_path_template"]:
        mismatches.append((name, "by_template", my_tmpl, prof["changed_leaves_by_path_template"]))
    if my_cat != prof["changed_leaves_by_category"]:
        mismatches.append((name, "by_category", my_cat, prof["changed_leaves_by_category"]))
    if c["changed_leaf_count"] != prof["changed_leaf_count"]:
        mismatches.append((name, "changed_leaf_count", c["changed_leaf_count"], prof["changed_leaf_count"]))

    # record-level: flatten instrument changed leaves
    irec = []
    for t in prof["tasks"]:
        for cl in t["changed_leaves"]:
            irec.append((t["output_index"], cl["json_pointer"], cl["path_template"],
                         cl["category"], cl["original"], cl["projected"],
                         tuple(cl["tokens"])))
    # rebuild my records with pointers
    myrec = []
    for (idx, ptr, tmpl, cat, ov, pv, toks) in []:
        pass
    # reuse census: it stored only ref rows; recompute full set for this profile is
    # already reflected in counts, but for record equality re-run leaf diff here cheaply
    profile_values = prof["values"]
    raw_text = open(RAW, encoding="utf-8").read()
    text = raw_text
    for n in ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]:
        text = text.replace("__" + n + "__", profile_values[n])
    pt = json.loads(text)

    def walk(o, p=""):
        if isinstance(o, str):
            yield p, o
        elif isinstance(o, dict):
            for k, v in o.items():
                yield from walk(v, p + "/" + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                yield from walk(v, p + "/" + str(i))

    for idx, (to, tp) in enumerate(zip(raw, pt)):
        po = dict(walk(to, "/" + str(idx)))
        pp = dict(walk(tp, "/" + str(idx)))
        for ptr, ov in po.items():
            pv = pp[ptr]
            if ov == pv:
                continue
            parts = ptr.lstrip("/").split("/")[1:]
            tm = []
            for x in parts:
                if x.isdigit() and tm and tm[-1] == "program_html":
                    continue
                tm.append("[]" if x.isdigit() else x)
            tmpl = ".".join(tm)
            canon_t = {"eval.program_html.[].required_contents.must_include.[]":
                       "eval.program_html[].required_contents.must_include[]",
                       "eval.program_html.[].url": "eval.program_html[].url",
                       "eval.program_html.required_contents.must_include.[]":
                       "eval.program_html[].required_contents.must_include[]",
                       "eval.program_html.url": "eval.program_html[].url"}.get(tmpl, tmpl)
            cat = "url_field" if canon_t in URL_TEMPLATES else "non_url_field"
            toks = tuple(t for t in TOKENS if t in ov)
            myrec.append((idx, ptr, canon_t, cat, ov, pv, toks))
    if sorted(irec) != sorted(myrec):
        only_i = [r for r in irec if r not in myrec]
        only_m = [r for r in myrec if r not in irec]
        mismatches.append((name, "record_diff", only_i[:5], only_m[:5],
                           len(only_i), len(only_m)))
    # reference_url focused
    ref_i = [r for r in irec if r[2] == "eval.reference_url"]
    ref_m = [r for r in myrec if r[2] == "eval.reference_url"]
    bad_ptr = [r for r in ref_i if not all(
        seg == "eval" or seg == "reference_url" or seg.isdigit()
        for seg in r[1].lstrip("/").split("/")) or r[1].split("/")[-1] != "reference_url"]
    print(name, "inst_records", len(irec), "my_records", len(myrec),
          "ref_inst", len(ref_i), "ref_my", len(ref_m),
          "ref_record_equal", sorted(ref_i) == sorted(ref_m),
          "ref_bad_pointer", len(bad_ptr),
          "ref_categories", sorted({r[3] for r in ref_i}),
          "ref_templates", sorted({r[2] for r in ref_i}))
    # tokens multiplicity in reference_url records
    multi = [r for r in ref_i if len(r[6]) != len(set(r[6])) or len(r[6]) > 1]
    print(name, "ref_records_tokens_len>1", len(multi),
          "sample", multi[:3])

    # global changed leaves by token (leaf counts)
    bytok = {t: sum(1 for r in myrec if t in r[6]) for t in TOKENS}
    if bytok != prof["changed_leaves_by_token"]:
        mismatches.append((name, "by_token", bytok, prof["changed_leaves_by_token"]))
    multi_leaves = sum(1 for r in myrec
                       if sum(r[4].count(t) for t in TOKENS) > 1)
    if multi_leaves != prof["changed_leaves_with_multiple_occurrences"]:
        mismatches.append((name, "multi_occ", multi_leaves,
                           prof["changed_leaves_with_multiple_occurrences"]))
    print(name, "my_multi_occ_leaves", multi_leaves,
          "inst", prof["changed_leaves_with_multiple_occurrences"])

print("MISMATCHES", len(mismatches))
for m in mismatches:
    print("MISMATCH", m)

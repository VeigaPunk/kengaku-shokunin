#!/usr/bin/env python3
"""Parse instrument --summary text and compare start_url/category numbers to oracle."""
import json
import re
import sys

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FPathStartUrl")
import oracle_v2 as O

S = O.SCRATCH
raw = open(O.RAW, encoding="utf-8").read()
prof = json.load(open(O.PROF, encoding="utf-8"))
base = json.loads(raw)
base_map = {p: (t, v) for t, p, v in O.walk_doc(base)}
lines = open(S + "/summary.txt", encoding="utf-8").read().splitlines()

pat = re.compile(r"^PROFILE (\S+) changed_leaves_(by_path_template|by_category)=(\{.*\})$")
seen = {}
for n, line in enumerate(lines, 1):
    m = pat.match(line)
    if m:
        pname, kind, payload = m.groups()
        seen.setdefault(pname, {})[kind] = (n, json.loads(payload))

bad = 0
for pname, pobj in prof.items():
    vals = pobj["values"]
    text = raw
    for tok in O.ORDER:
        text = text.replace(tok, vals[tok.strip("_")])
    proj = json.loads(text)
    pm = {p: (t, v) for t, p, v in O.walk_doc(proj)}
    changed = [p for p in base_map if base_map[p][1] != pm[p][1]]
    o_tpl = {}
    o_cat = {"url_field": 0, "non_url_field": 0}
    for p in changed:
        tpl = base_map[p][0]
        o_tpl[tpl] = o_tpl.get(tpl, 0) + 1
        o_cat["url_field" if tpl in O.URL_TEMPLATES else "non_url_field"] += 1
    su_tpl = o_tpl.get("start_url", 0)
    for kind, want in (("by_path_template", o_tpl), ("by_category", o_cat)):
        ln, got = seen[pname][kind]
        status = "OK" if got == want else "MISMATCH"
        if status != "OK":
            bad += 1
        print(f"{pname} {kind} summary_line={ln} {status} "
              f"start_url={got.get('start_url')} oracle_start_url={su_tpl} "
              f"sum={sum(got.values())} oracle_changed={len(changed)}")
        if status != "OK":
            print("  got", got, "want", want)
print("SUMMARY_START_URL_MISMATCHES", bad)

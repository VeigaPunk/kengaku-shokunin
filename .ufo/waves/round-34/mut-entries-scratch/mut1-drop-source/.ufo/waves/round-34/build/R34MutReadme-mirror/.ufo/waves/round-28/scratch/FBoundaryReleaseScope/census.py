import json, sys
from collections import Counter

PIN = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
VERS = {"release_b454f2dc": "b454f2dc.test.raw.json", "v0.2.0_e32b71e3": "e32b71e3.test.raw.json", "pin_dce04686": PIN}


BROKEN = '"string_match"\n        "string_match"'


def load(p):
    with open(p) as fh:
        text = fh.read()
    n = text.count(BROKEN)
    if n:
        sys.stderr.write(f"{p}: in-memory comma repair at {n} sites (scratch only)\n")
        text = text.replace(BROKEN, '"string_match",\n        "string_match"')
    return {t["task_id"]: t for t in json.loads(text)}


def profile(tasks):
    ets = Counter("+".join(sorted(set(t["eval"]["eval_types"]))) for t in tasks.values())
    ops = Counter()
    na = 0
    for t in tasks.values():
        ra = t["eval"].get("reference_answers") or {}
        for k in ra:
            ops[k] += 1
        if ra.get("fuzzy_match") == "N/A":
            na += 1
        if ra.get("exact_match") == "N/A":
            ops["exact_N/A"] += 1
    strata = {}
    for tid, t in tasks.items():
        key = (tuple(sorted(t["sites"])), tuple(sorted(set(t["eval"]["eval_types"]))))
        strata.setdefault(key, []).append(tid)
    order = sorted(strata)
    sel = [min(strata[k]) for k in order[:16]]
    shop = [k for k in order[:16] if "shopping" in k[0]]
    return {"n": len(tasks), "ids": sorted(tasks) == list(range(812)), "evaltype_sets": dict(ets),
            "string_ops": dict(ops), "fuzzy_NA": na, "strata": len(strata), "selected": sel,
            "selected_strata_with_shopping": shop}


SUB = ("eval_types", "reference_answers", "reference_url", "program_html")


def diff(a, b):
    ev = sub = 0
    fields = Counter()
    changed = []
    for tid in a:
        if a[tid]["eval"] != b[tid]["eval"]:
            ev += 1
        s = False
        for f in set(a[tid]["eval"]) | set(b[tid]["eval"]):
            if a[tid]["eval"].get(f) != b[tid]["eval"].get(f):
                fields[f] += 1
                if f in SUB:
                    s = True
        if a[tid].get("intent") != b[tid].get("intent"):
            fields["intent"] += 1
        if s:
            sub += 1
            changed.append(tid)
    return ev, sub, dict(fields), changed


data = {k: load(v) for k, v in VERS.items()}
out = {k: profile(v) for k, v in data.items()}
sample = out["pin_dce04686"]["selected"]
for a, b in (("release_b454f2dc", "pin_dce04686"), ("v0.2.0_e32b71e3", "pin_dce04686"), ("release_b454f2dc", "v0.2.0_e32b71e3")):
    ev, sub, fields, changed = diff(data[a], data[b])
    out[f"{a}->{b}"] = {"eval_block_changed": ev, "substantive": sub, "fields": fields,
                        "sample_substantive": [t for t in sample if t in changed]}
json.dump(out, sys.stdout, indent=1, default=list)

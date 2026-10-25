"""Independent HTML-target census of pinned test.raw.json; derives from data only, imports no production code."""
import collections
import json
import sys

path = sys.argv[1]
tasks = json.load(open(path))
c = collections.Counter()
target_keys = collections.Counter()
rc_keys = collections.Counter()
value_types = collections.Counter()
prep = collections.Counter()
locator_of_prep = collections.Counter()
empty_alt = []
empty_list = []
empty_exact = []
both = []
html_without_kind = []
kind_without_html = []
for t in tasks:
    ev = t["eval"]
    kinds = ev["eval_types"]
    has = "program_html" in ev
    if "program_html" in kinds and not has:
        kind_without_html.append(t["task_id"])
    if has and "program_html" not in kinds:
        html_without_kind.append((t["task_id"], len(ev["program_html"]) if isinstance(ev["program_html"], list) else type(ev["program_html"]).__name__))
    if "program_html" not in kinds:
        continue
    targets = ev["program_html"]
    if not targets:
        c["empty_target_list"] += 1
    for i, tg in enumerate(targets):
        c["targets"] += 1
        target_keys[tuple(sorted(tg))] += 1
        rc = tg["required_contents"]
        rc_keys[tuple(sorted(rc))] += 1
        if "exact_match" in rc and "must_include" in rc:
            both.append((t["task_id"], i))
        op = "exact_match" if "exact_match" in rc else "must_include" if "must_include" in rc else None
        c["op_" + str(op)] += 1
        v = rc.get(op)
        value_types[(op, type(v).__name__, tuple(sorted({type(x).__name__ for x in v})) if isinstance(v, list) else None)] += 1
        if op == "must_include":
            if not v:
                empty_list.append((t["task_id"], i))
            for s in v:
                if isinstance(s, str) and any(not a.strip() for a in s.split(" |OR| ")):
                    empty_alt.append((t["task_id"], i, s))
                if isinstance(s, str) and " |OR| " in s:
                    c["or_items"] += 1
        if op == "exact_match" and isinstance(v, str) and not v.strip():
            empty_exact.append((t["task_id"], i, v))
        loc = tg["locator"]
        cls = "full_page" if not loc.strip() else "javascript" if loc.startswith("document.") or loc.startswith("[...document.") else "helper" if loc.startswith("func:") else "unsupported"
        c["loc_" + cls] += 1
        if "prep_actions" in tg:
            pa = tg["prep_actions"]
            prep[(type(pa).__name__, tuple(sorted({type(x).__name__ for x in pa})) if isinstance(pa, list) else None, len(pa) if hasattr(pa, "__len__") else None)] += 1
            locator_of_prep[cls] += 1
print(json.dumps({
    "counts": dict(sorted(c.items())),
    "target_key_sets": {"|".join(k): n for k, n in target_keys.items()},
    "required_contents_key_sets": {"|".join(k): n for k, n in rc_keys.items()},
    "value_types": {repr(k): n for k, n in value_types.items()},
    "prep_actions": {repr(k): n for k, n in prep.items()},
    "prep_actions_by_locator_class": dict(locator_of_prep),
    "both_operators": both,
    "must_include_empty_list": empty_list,
    "must_include_empty_or_blank_alternative": empty_alt,
    "exact_match_blank": empty_exact,
    "program_html_without_kind": html_without_kind,
    "kind_without_program_html": kind_without_html,
}, indent=1))

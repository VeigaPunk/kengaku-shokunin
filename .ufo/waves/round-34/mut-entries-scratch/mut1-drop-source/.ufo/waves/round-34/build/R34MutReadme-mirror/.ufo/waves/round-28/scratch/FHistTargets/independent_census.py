#!/usr/bin/env python3
"""FHistTargets independent census of pinned WebArena test.raw.json.

Stdlib-only re-derivation of every program_html target/task metric.
Does NOT import plans/benchmark_spec_audit.py or plans/fixtures/r28/benchmark_oracle.py.
Operator/locator/url-class semantics re-derived from the pinned upstream source
plans/fixtures/r28/webarena/evaluation_harness/evaluators.py HTMLContentEvaluator:244-333,
read as data: targets ANDed (score *= per target, :261,:310,:327);
required_contents if/elif gives exact_match precedence over must_include (:305/:312);
each must_include element ANDed across the list, " |OR| " alternatives ORed (:315-327);
target url "last" skips navigation (:271), startswith("func") is eval'd helper (:263-266);
locator "" -> full page (:276), document./[...document. -> JS (:279-280), func: -> helper (:296).
"""
import collections
import functools
import json
import sys

RAW = "plans/fixtures/r28/webarena/config_files/test.raw.json"
SEL = "plans/fixtures/r28/webarena/selected-task-ids.json"
EXPECT_N = 812


def cmp_tuples(a, b):
    """Hand-rolled lexicographic compare over (sites_tuple, kinds_tuple),
    element-wise string compare; an independent implementation of tuple sort."""
    for x, y in zip(a[0], b[0]):
        if x != y:
            return -1 if x < y else 1
    if len(a[0]) != len(b[0]):
        return -1 if len(a[0]) < len(b[0]) else 1
    for x, y in zip(a[1], b[1]):
        if x != y:
            return -1 if x < y else 1
    if len(a[1]) != len(b[1]):
        return -1 if len(a[1]) < len(b[1]) else 1
    return 0


def main():
    tasks = json.load(open(RAW))
    out = {"task_count": len(tasks), "anomalies": []}
    tid = [t["task_id"] for t in tasks]
    out["distinct_task_ids"] = len(set(tid))
    out["id_min"], out["id_max"] = min(tid), max(tid)
    out["duplicate_ids"] = sorted(k for k, v in collections.Counter(tid).items() if v > 1)
    out["missing_ids"] = sorted(set(range(EXPECT_N)) - set(tid))
    out["unexpected_ids"] = sorted(set(tid) - set(range(EXPECT_N)))

    eval_sets = collections.Counter()
    eval_orders = collections.Counter()
    site_sets = collections.Counter()
    login = collections.Counter()
    reset = collections.Counter()
    strata = collections.defaultdict(list)  # (tuple(sorted sites), tuple(sorted kinds)) -> ids

    ph_tasks = 0                      # tasks declaring program_html eval type
    ph_targets_total = 0              # targets counted only inside program_html tasks
    targets_per_task = collections.Counter()
    nonph_nonempty_list = []          # tasks NOT declaring program_html but list non-empty
    url_class = collections.Counter()
    malformed_func_url = 0
    locator_class = collections.Counter()
    eff_operator = collections.Counter()
    both_keys = neither_keys = non_dict_required = 0
    non_dict_target = 0
    missing_url = missing_locator = 0
    mi_elem_total = 0                 # must_include list elements across targets
    mi_elem_or = 0                    # elements containing " |OR| "
    mi_or_alternatives = 0            # total OR alternatives across those elements
    prep_actions_targets = 0
    string_ops = collections.Counter()
    url_rules = collections.Counter()
    ref_url_empty_alt = 0

    for t in tasks:
        ev = t.get("eval", {})
        kinds = ev.get("eval_types", [])
        sk, ss = sorted(kinds), sorted(t.get("sites", []))
        eval_sets[",".join(sk)] += 1
        eval_orders[",".join(kinds)] += 1
        site_sets[",".join(ss)] += 1
        login[str(t.get("require_login")).lower()] += 1
        reset[str(t.get("require_reset")).lower()] += 1
        strata[(tuple(ss), tuple(sk))].append(t["task_id"])

        if "string_match" in kinds:
            for op in ev.get("reference_answers", {}):
                string_ops[op] += 1
        if "url_match" in kinds:
            rule = ev.get("url_note", "GOLD in PRED")
            url_rules[str(rule)] += 1
            ru = ev.get("reference_url", "")
            if any(not a for a in ru.split(" |OR| ")):
                ref_url_empty_alt += 1

        raw_list = ev.get("program_html", [])
        if "program_html" not in kinds:
            if isinstance(raw_list, list) and raw_list:
                nonph_nonempty_list.append(t["task_id"])
            continue
        ph_tasks += 1
        if not isinstance(raw_list, list) or not raw_list:
            out["anomalies"].append({"task_id": t["task_id"], "issue": "program_html_list_empty_or_nonlist"})
            continue
        ph_targets_total += len(raw_list)
        targets_per_task[len(raw_list)] += 1
        for tgt in raw_list:
            if not isinstance(tgt, dict):
                non_dict_target += 1
                continue
            u = tgt.get("url")
            if not isinstance(u, str) or not u:
                missing_url += 1
            else:
                # upstream: startswith("func") -> helper eval branch; == "last" -> no nav; else goto
                cls = "last" if u == "last" else "helper" if u.startswith("func") else "navigation"
                url_class[cls] += 1
                if u.startswith("func") and not u.startswith("func:"):
                    malformed_func_url += 1
            loc = tgt.get("locator")
            if not isinstance(loc, str):
                missing_locator += 1
            else:
                l = loc.strip()
                if not l:
                    locator_class["full_page"] += 1
                elif loc.startswith("document.") or loc.startswith("[...document."):
                    locator_class["javascript"] += 1
                elif loc.startswith("func:"):
                    locator_class["helper"] += 1
                else:
                    locator_class["unsupported"] += 1
            req = tgt.get("required_contents")
            if not isinstance(req, dict):
                non_dict_required += 1
                continue
            has_ex, has_mi = "exact_match" in req, "must_include" in req
            if has_ex and has_mi:
                both_keys += 1
            if has_ex:
                eff_operator["exact_match"] += 1   # upstream if-branch precedence
            elif has_mi:
                eff_operator["must_include"] += 1  # elif-branch
            else:
                neither_keys += 1
            if has_mi and isinstance(req.get("must_include"), list):
                for elem in req["must_include"]:
                    if isinstance(elem, str):
                        mi_elem_total += 1
                        alts = elem.split(" |OR| ")
                        if len(alts) > 1:
                            mi_elem_or += 1
                            mi_or_alternatives += len(alts)
            if "prep_actions" in tgt:
                prep_actions_targets += 1

    # selection: lexicographic strata order via hand-rolled comparator, min id each, first 16
    ordered = sorted(strata.keys(), key=functools.cmp_to_key(cmp_tuples))
    out["strata_count"] = len(strata)
    selection = [min(strata[k]) for k in ordered[:16]]
    out["selection_first16"] = selection
    out["selection_file"] = json.load(open(SEL))
    out["selection_match_file"] = selection == out["selection_file"]

    out["eval_type_sets"] = dict(sorted(eval_sets.items()))
    out["eval_type_orders"] = dict(sorted(eval_orders.items()))
    out["site_sets"] = dict(sorted(site_sets.items()))
    out["login_flags"] = dict(login)
    out["reset_flags"] = dict(reset)
    out["string_operators"] = dict(sorted(string_ops.items()))
    out["url_rules"] = dict(sorted(url_rules.items()))
    out["reference_url_empty_alternative_tasks"] = ref_url_empty_alt

    out["program_html"] = {
        "tasks_declaring_type": ph_tasks,
        "targets_total": ph_targets_total,
        "targets_per_task_hist": {str(k): targets_per_task[k] for k in sorted(targets_per_task)},
        "targets_per_task_min": min(targets_per_task) if targets_per_task else None,
        "targets_per_task_max": max(targets_per_task) if targets_per_task else None,
        "tasks_without_type_but_nonempty_list": nonph_nonempty_list,
        "target_url_classes": dict(sorted(url_class.items())),
        "malformed_func_url_targets": malformed_func_url,
        "locator_classes": dict(sorted(locator_class.items())),
        "effective_operators": dict(sorted(eff_operator.items())),
        "both_exact_and_must_include_targets": both_keys,
        "neither_operator_targets": neither_keys,
        "non_dict_required_contents": non_dict_required,
        "non_dict_targets": non_dict_target,
        "missing_url_targets": missing_url,
        "missing_locator_targets": missing_locator,
        "must_include_elements": mi_elem_total,
        "must_include_elements_with_OR": mi_elem_or,
        "must_include_OR_alternatives": mi_or_alternatives,
        "prep_actions_targets": prep_actions_targets,
    }
    json.dump(out, sys.stdout, indent=2, sort_keys=True)
    print()


main()

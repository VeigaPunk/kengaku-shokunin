#!/usr/bin/env python3
"""Independent author-side census for FHistSelection (falsification, round 28).

Derives the stratum key / selection vector and metric counters directly from the
pinned raw JSON using only the standard library. This file shares NO code with
plans/benchmark_spec_audit.py or plans/fixtures/r28/benchmark_oracle.py; the
selection rule was re-implemented from the claims prose:

    form (sorted site set, sorted evaluator-type set), sort the tuples
    lexicographically, take minimum task_id from each, retain first16 groups.
"""
import json
import sys
from collections import Counter

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
KNOWN_TYPES = {"string_match", "url_match", "program_html"}


def stratum_key(task):
    """Return the grouping tuple, or None when the raw fields cannot form one.

    A task can only be stratified when it carries an integer task_id (bool is
    rejected as a distinct type), a non-empty list of non-empty strings for
    sites, and a non-empty list of strings for eval.eval_types.
    """
    tid = task.get("task_id")
    if type(tid) is not int:
        return None
    sites = task.get("sites")
    if not isinstance(sites, list) or not sites:
        return None
    if not all(isinstance(s, str) and s for s in sites):
        return None
    ev = task.get("eval")
    if not isinstance(ev, dict):
        return None
    kinds = ev.get("eval_types")
    if not isinstance(kinds, list) or not kinds:
        return None
    if not all(isinstance(k, str) for k in kinds):
        return None
    return (tuple(sorted(sites)), tuple(sorted(kinds)))


def locator_kind(locator):
    if not isinstance(locator, str):
        return None
    if not locator.strip():
        return "full_page"
    if locator.startswith("document.") or locator.startswith("[...document."):
        return "javascript"
    if locator.startswith("func:"):
        return "helper"
    return "unsupported"


def url_kind(url):
    if url == "last":
        return "last"
    if isinstance(url, str) and url.startswith("func"):
        return "helper"
    return "navigation"


def main():
    tasks = json.loads(open(RAW).read())
    out = {}
    out["task_count"] = len(tasks)
    ids = [t["task_id"] for t in tasks if type(t.get("task_id")) is int]
    out["distinct_task_ids"] = len(set(ids))
    out["id_min"], out["id_max"] = min(ids), max(ids)
    out["missing_ids"] = sorted(set(range(812)) - set(ids))
    out["duplicate_ids"] = sorted(t for t, c in Counter(ids).items() if c > 1)
    out["unexpected_ids"] = sorted(set(ids) - set(range(812)))

    # --- the selection vector itself ---
    strata = {}
    for task in tasks:
        key = stratum_key(task)
        if key is None:
            continue
        strata.setdefault(key, []).append(task["task_id"])
    ordered = sorted(strata.items())          # tuple sort == lexicographic order
    out["site_eval_strata"] = len(ordered)
    out["strata_keys_ordered"] = [list(k) for k, _ in ordered]
    out["strata_min_ids_ordered"] = [min(v) for _, v in ordered]
    out["selected_task_ids_first16"] = out["strata_min_ids_ordered"][:16]

    # --- metric counters used by the candidate table ---
    eval_sets, eval_orders, site_sets = Counter(), Counter(), Counter()
    str_ops, url_rules, html_ops, loc_classes, url_classes = Counter(), Counter(), Counter(), Counter(), Counter()
    login_flags, reset_flags = Counter(), Counter()
    target_total = 0
    for task in tasks:
        ev = task.get("eval") if isinstance(task.get("eval"), dict) else {}
        kinds = ev.get("eval_types") if isinstance(ev.get("eval_types"), list) else []
        sites = task.get("sites") if isinstance(task.get("sites"), list) else []
        eval_sets[",".join(sorted(kinds))] += 1
        eval_orders[",".join(kinds)] += 1
        if sites:
            site_sets[",".join(sorted(sites))] += 1
        login_flags[str(task.get("require_login")).lower()] += 1
        reset_flags[str(task.get("require_reset")).lower()] += 1
        refs = ev.get("reference_answers")
        if "string_match" in kinds and isinstance(refs, dict):
            for op in refs:
                str_ops[op] += 1
        if "url_match" in kinds:
            url_rules[str(ev.get("url_note", "GOLD in PRED"))] += 1
        if "program_html" in kinds:
            targets = ev.get("program_html")
            if isinstance(targets, list):
                target_total += len(targets)
                for tg in targets:
                    if not isinstance(tg, dict):
                        continue
                    lk = locator_kind(tg.get("locator"))
                    if lk:
                        loc_classes[lk] += 1
                    url = tg.get("url")
                    if isinstance(url, str) and url:
                        url_classes[url_kind(url)] += 1
                    req = tg.get("required_contents")
                    if isinstance(req, dict):
                        op = "exact_match" if "exact_match" in req else "must_include" if "must_include" in req else None
                        if op:
                            html_ops[op] += 1
    out["program_html_targets"] = target_total
    out["eval_type_sets"] = dict(sorted(eval_sets.items()))
    out["eval_type_orders"] = dict(sorted(eval_orders.items()))
    out["site_sets"] = dict(sorted(site_sets.items()))
    out["login_flags"] = dict(sorted(login_flags.items()))
    out["reset_flags"] = dict(sorted(reset_flags.items()))
    out["string_operators"] = dict(sorted(str_ops.items()))
    out["url_rules"] = dict(sorted(url_rules.items()))
    out["html_operators"] = dict(sorted(html_ops.items()))
    out["locator_classes"] = dict(sorted(loc_classes.items()))
    out["target_url_classes"] = dict(sorted(url_classes.items()))

    # tasks per stratum-size detail for the first16 strata
    out["first16_strata_size"] = [len(v) for _, v in ordered[:16]]
    json.dump(out, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()

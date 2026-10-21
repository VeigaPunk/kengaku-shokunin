"""FContractEntry independent re-derivation for Q10 second-seat re-read.
Reads ONLY the pinned fixture bytes; imports no production/oracle code.
Run: python3 -B census.py
"""
import json, collections

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena"
tasks = json.load(open(f"{ROOT}/config_files/test.raw.json"))

# 1. population
ids = [t["task_id"] for t in tasks]
print("tasks", len(tasks), "distinct", len(set(ids)),
      "min", min(ids), "max", max(ids),
      "missing", [i for i in range(812) if i not in set(ids)],
      "dups", [i for i, c in collections.Counter(ids).items() if c > 1])

# 2. evaluator-type SET histogram
ets = collections.Counter(tuple(sorted(t["eval"]["eval_types"])) for t in tasks)
print("eval-type sets", len(ets), dict(ets))

# 3. strata + selection replay
strata = collections.defaultdict(list)
for t in tasks:
    strata[(tuple(sorted(t["sites"])),
            tuple(sorted(t["eval"]["eval_types"])))].append(t["task_id"])
sel = [min(strata[k]) for k in sorted(strata)][:16]
print("strata", len(strata), "selected16", sel)

# 4. string operators (task-level key presence) + N/A population
ops = collections.Counter()
na = []
for t in tasks:
    ra = t["eval"].get("reference_answers") or {}
    for o in ("exact_match", "must_include", "fuzzy_match"):
        if o in ra:
            ops[o] += 1
    if ra.get("fuzzy_match") == "N/A":
        na.append(t)
print("string operators", dict(ops))
print("N/A tasks", len(na),
      "non-single-approach", [t["task_id"] for t in na
                              if list(t["eval"]["reference_answers"]) != ["fuzzy_match"]],
      "no-string_note", [t["task_id"] for t in na if not t["eval"].get("string_note")])

# 5. program_html targets
tg = [(t["task_id"], x) for t in tasks for x in t["eval"].get("program_html", [])]
loc = collections.Counter()
url = collections.Counter()
eff = collections.Counter()
for tid, x in tg:
    l = x["locator"]
    loc["full-page" if not l.strip()
        else "js" if l.startswith(("document.", "[...document."))
        else "helper" if l.startswith("func:") else "OTHER"] += 1
    u = x["url"]
    url["last" if u == "last" else "func" if u.startswith("func") else "nav"] += 1
    rc = x["required_contents"]
    eff["exact_match" if "exact_match" in rc
        else "must_include" if "must_include" in rc else "OTHER"] += 1
print("targets", len(tg), "locators", dict(loc), "urls", dict(url), "eff", dict(eff))

# 6. selected-case coverage gaps + shopping omission
selT = {t["task_id"]: t for t in tasks if t["task_id"] in sel}
for tid in sel:
    gs = selT[tid]["eval"].get("program_html", [])
    print(tid, "sites", sorted(selT[tid]["sites"]),
          "func-url", any(x["url"].startswith("func") for x in gs),
          "func-loc", any(x["locator"].startswith("func:") for x in gs),
          "prep", any("prep_actions" in x for x in gs),
          "OR", any(" |OR| " in c for x in gs
                    for c in x["required_contents"].get("must_include", [])))

# 7. ordering facts
print("ordered combos", collections.Counter(
    tuple(t["eval"]["eval_types"]) for t in tasks if len(t["eval"]["eval_types"]) > 1))
print("non-default url_note", [t["task_id"] for t in tasks
                               if t["eval"].get("url_note") not in (None, "GOLD in PRED")])
print("func-without-colon urls",
      [(tid, x["url"]) for tid, x in tg
       if x["url"].startswith("func") and not x["url"].startswith("func:")])

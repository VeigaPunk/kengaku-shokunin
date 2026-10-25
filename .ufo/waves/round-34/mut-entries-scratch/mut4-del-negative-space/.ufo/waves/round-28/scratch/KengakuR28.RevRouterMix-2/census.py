#!/usr/bin/env python3
"""KengakuR28.RevRouterMix-2 scratch census — read-only parse of the frozen snapshot.

Never imports/executes upstream code; JSON parsing only. Run from any cwd with
  python3 census.py
Snapshots verified against manifest.json before these counts (sha256sum, 2026-10-21):
  test.raw.json 7b50386f…537652  evaluators.py e23edb39…e00c22
  helper_functions.py ec758da4…97e275  LICENSE c71d239d…35d0ab4
  manifest.json c78b1478…23a6dd  selected-task-ids.json 5f7eea2e…f3ed17a
"""
import json, collections, sys, os

root = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..",
                    "plans", "fixtures", "r28", "webarena")
tasks = json.load(open(os.path.join(root, "config_files", "test.raw.json")))
E = lambda t: t["eval"]

print("total", len(tasks))
print("task_id types:", collections.Counter(type(t["task_id"]).__name__ for t in tasks))
print("dup task_ids:", len(tasks) - len({t["task_id"] for t in tasks}),
      "min/max:", min(t["task_id"] for t in tasks), max(t["task_id"] for t in tasks))
combo = collections.Counter(tuple(E(t)["eval_types"]) for t in tasks)
print("eval_type chains:", dict(combo))
print("ordered uniformity (url,html):",
      all(E(t)["eval_types"] == ["url_match", "program_html"] for t in tasks
          if set(E(t)["eval_types"]) == {"url_match", "program_html"}),
      "(string,url):",
      collections.Counter(tuple(E(t)["eval_types"]) for t in tasks
                          if set(E(t)["eval_types"]) == {"string_match", "url_match"}))
print("empty eval_types:", sum(1 for t in tasks if not E(t)["eval_types"]),
      "dup within task:", sum(1 for t in tasks if len(E(t)["eval_types"]) != len(set(E(t)["eval_types"]))))
print("eval null fields:", dict(collections.Counter(
    k for t in tasks for k, v in E(t).items() if v is None)))
print("null reference_url ids:", [(t["task_id"], E(t)["eval_types"]) for t in tasks
                                  if E(t).get("reference_url") is None])
print("dead reference_url (non-empty, url not dispatched):",
      [(t["task_id"], E(t)["eval_types"], E(t)["reference_url"][:60]) for t in tasks
       if isinstance(E(t).get("reference_url"), str) and E(t)["reference_url"]
       and "url_match" not in E(t)["eval_types"]])
sm = [t for t in tasks if "string_match" in E(t)["eval_types"]]
print("string tasks:", len(sm),
      "reference_answers non-dict:", [t["task_id"] for t in sm
                                      if not isinstance(E(t).get("reference_answers"), dict)])
mi = [(t["task_id"], v) for t in sm for k, v in E(t).get("reference_answers", {}).items()
      if k == "must_include" and isinstance(v, list)]
print("must_include single-elem lists:", sum(1 for _, v in mi if len(v) == 1),
      "single-elem AND single-char ref (token path):",
      sum(1 for _, v in mi if len(v) == 1 and len(v[0].strip().strip("'\"").lower()) == 1))
fz = [(t["task_id"], v) for t in sm for k, v in E(t).get("reference_answers", {}).items()
      if k == "fuzzy_match"]
fzna = [(i, v) for i, v in fz if v == "N/A"]
byid = {t["task_id"]: t for t in tasks}
print("fuzzy:", len(fz), "N/A:", len(fzna),
      "N/A single-key string-only:",
      all(byid[i]["eval"]["reference_answers"] == {"fuzzy_match": "N/A"}
          and byid[i]["eval"]["eval_types"] == ["string_match"] for i, _ in fzna),
      "N/A with eval.string_note:",
      all(isinstance(byid[i]["eval"].get("string_note"), str) for i, _ in fzna))
print("eval.string_note present:", sum(1 for t in tasks if "string_note" in E(t)),
      "non-empty:", sum(1 for t in tasks if E(t).get("string_note")))
um = [t for t in tasks if "url_match" in E(t)["eval_types"]]
print("url tasks:", len(um), "reference_url missing:",
      [t["task_id"] for t in um if "reference_url" not in E(t)],
      "empty:", sum(1 for t in um if not E(t).get("reference_url")),
      "with OR:", sum(1 for t in um if " |OR| " in E(t).get("reference_url", "")),
      "non-default url_note:",
      {E(t).get("url_note") for t in um
       if E(t).get("url_note", "GOLD in PRED") != "GOLD in PRED"})
for t in tasks:
    ru = E(t).get("reference_url", "")
    if " |OR| " in ru:
        parts = ru.split(" |OR| ")
        print("  OR url", t["task_id"], "empty parts:",
              [i for i, p in enumerate(parts) if not p.strip()])
print("total program_html targets:",
      sum(len(E(t).get("program_html") or []) for t in tasks))
for t in tasks:
    for tg in E(t).get("program_html", []):
        for it in tg.get("required_contents", {}).get("must_include", []):
            if " |OR| " in it:
                parts = it.split(" |OR| ")
                print("  OR html", t["task_id"], "empty parts:",
                      [i for i, p in enumerate(parts) if not p.strip()])
both = [t["task_id"] for t in tasks for tg in E(t).get("program_html", [])
        if {"exact_match", "must_include"} <= set(tg.get("required_contents", {}))]
neither = [t["task_id"] for t in tasks for tg in E(t).get("program_html", [])
           if isinstance(tg.get("required_contents"), dict)
           and not {"exact_match", "must_include"} & set(tg["required_contents"])]
print("targets BOTH keys:", both, "NEITHER:", neither,
      "empty exact_match '':", sum(1 for t in tasks for tg in E(t).get("program_html", [])
                                   if tg.get("required_contents", {}).get("exact_match") == ""),
      "must_include '' items:", sum(1 for t in tasks for tg in E(t).get("program_html", [])
                                    for it in tg.get("required_contents", {}).get("must_include", [])
                                    if it == ""))
sel = [389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]
print("selected present:", all(i in byid for i in sel))
for i in sel:
    t = byid[i]
    print("  ", i, E(t)["eval_types"], sorted(E(t).get("reference_answers") or {}),
          len(E(t).get("program_html") or []), E(t).get("url_note", "-"), t.get("sites"))

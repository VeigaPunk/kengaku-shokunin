"""Full independent census vs instrument --json, derived from prereg TEXT + pinned bytes.

No import of plans/config_projection.py.
"""
import hashlib
import json
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = LANE + "/plans/fixtures/r29/profiles.json"
MANIFEST = LANE + "/plans/fixtures/r29/manifest.json"
INST = sys.argv[1]

raw_text = open(RAW, "rb").read().decode("utf-8")
profiles = json.load(open(PROFILES))
order = json.load(open(MANIFEST))["replacement_order"]
tokens = {n: "__" + n + "__" for n in order}
instrument = json.load(open(INST))
original = json.loads(raw_text)


def is_url_field(key):
    return key == "start_url" or key == "url" or key.endswith("_url")


def walk_leaves(obj, path="", tmpl="", key=""):
    """Yield dict(pointer, template, key, value) for every scalar leaf."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_leaves(v, path + "/" + k, (tmpl + "." + k) if tmpl else k, k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_leaves(v, path + "/" + str(i), tmpl + "[]", key)
    else:
        yield dict(pointer=path, template=tmpl, key=key, value=obj)


def leaves_by_pointer(obj):
    return {d["pointer"]: d for d in walk_leaves(obj)}


def token_occurrences(s):
    return sum(s.count(t) for t in tokens.values())


summary = {}
problems = []
for name in profiles:
    values = profiles[name]["values"]
    text = raw_text
    applied = {}
    for tn in order:
        applied[tn] = text.count(tokens[tn])
        text = text.replace(tokens[tn], values[tn])
    projected = json.loads(text)

    inst_p = instrument["profiles"][name]
    agg = dict(
        projected_text_sha256=hashlib.sha256(text.encode()).hexdigest(),
        changed_leaf_count=0,
        changed_task_count=0,
        changed_leaves_by_category={},
        changed_leaves_by_path_template={},
        changed_leaves_by_token={},
        changed_tasks_by_token={},
        changed_leaves_with_multiple_occurrences=0,
        string_leaf_count=0,
        remaining_known_tokens_text={t: text.count(t) for t in tokens.values()},
    )
    for t in tokens.values():
        agg["changed_leaves_by_category"].setdefault("url_field", 0)
        agg["changed_leaves_by_category"].setdefault("non_url_field", 0)
        agg["changed_leaves_by_token"].setdefault(t, 0)
        agg["changed_tasks_by_token"].setdefault(t, 0)

    inst_tasks = {r["output_index"]: r for r in inst_p["tasks"]}
    for idx, proj_task in enumerate(projected):
        orig_task = original[idx]
        o = leaves_by_pointer(orig_task)
        p = leaves_by_pointer(proj_task)
        n_string = sum(1 for d in o.values() if isinstance(d["value"], str))
        agg["string_leaf_count"] += n_string
        changed = []
        for ptr, od in o.items():
            pd = p.get(ptr)
            if pd is None:
                problems.append((name, idx, ptr, "leaf disappeared"))
                continue
            if od["value"] != pd["value"]:
                if not isinstance(od["value"], str) or not isinstance(pd["value"], str):
                    problems.append((name, idx, ptr, "non-string change", od["value"], pd["value"]))
                tokens_in = [t for t in tokens.values() if t in od["value"]]
                cat = "url_field" if is_url_field(od["key"]) else "non_url_field"
                changed.append(dict(pointer="/" + str(idx) + ptr,
                                    template=od["template"], key=od["key"], cat=cat,
                                    original=od["value"], projected=pd["value"],
                                    tokens=tokens_in,
                                    occ=token_occurrences(od["value"])))
        # structural additions?
        extra = [ptr for ptr in p if ptr not in o]
        if extra:
            problems.append((name, idx, "extra leaves", extra[:3]))
        agg["changed_leaf_count"] += len(changed)
        if changed:
            agg["changed_task_count"] += 1
        for c in changed:
            agg["changed_leaves_by_category"][c["cat"]] += 1
            agg["changed_leaves_by_path_template"][c["template"]] = \
                agg["changed_leaves_by_path_template"].get(c["template"], 0) + 1
            # attribution: first token in replacement order present in original leaf
            first = next(t for t in tokens.values() if t in c["original"])
            agg["changed_leaves_by_token"][first] += 1
            agg["changed_tasks_by_token"][first] += 0
            if c["occ"] > 1:
                agg["changed_leaves_with_multiple_occurrences"] += 1
        for t in tokens.values():
            if any(t in c["original"] for c in changed):
                pass
        # changed_tasks_by_token: task counts once per token appearing in any changed leaf
        for t in tokens.values():
            if any(t in c["original"] for c in changed):
                agg["changed_tasks_by_token"][t] += 1

        # per-record compare
        rec = inst_tasks.get(idx)
        if rec is None:
            problems.append((name, idx, "record missing"))
            continue
        if rec["task_id"] != orig_task.get("task_id"):
            problems.append((name, idx, "task_id", rec["task_id"], orig_task.get("task_id")))
        if rec["output_index"] != idx:
            problems.append((name, idx, "output_index", rec["output_index"]))
        if rec["index_equals_task_id"] != (idx == orig_task.get("task_id")):
            problems.append((name, idx, "index_equals_task_id", rec["index_equals_task_id"]))
        if rec["output_filename"] != "config_files/%d.json" % idx:
            problems.append((name, idx, "output_filename", rec["output_filename"]))
        want_sha = hashlib.sha256(json.dumps(proj_task, indent=2).encode()).hexdigest()
        if rec["would_be_file_sha256"] != want_sha:
            problems.append((name, idx, "would_be_file_sha256", rec["would_be_file_sha256"], want_sha))
        if rec["projected_task"] != proj_task:
            problems.append((name, idx, "projected_task differs"))
        got = rec["changed_leaves"]
        if len(got) != len(changed):
            problems.append((name, idx, "changed_leaves count", len(got), len(changed)))
        else:
            for g, c in zip(got, changed):
                for f in ("json_pointer", "original", "projected"):
                    if g.get(f) != c["pointer" if f == "json_pointer" else f]:
                        problems.append((name, idx, "leaf " + f, g.get(f), c["pointer" if f == "json_pointer" else f]))
                if g.get("path_template") != c["template"]:
                    problems.append((name, idx, "leaf path_template", g.get("path_template"), c["template"]))
                if g.get("category") != c["cat"]:
                    problems.append((name, idx, "leaf category", g.get("category"), c["cat"]))
                if g.get("tokens") != c["tokens"]:
                    problems.append((name, idx, "leaf tokens", g.get("tokens"), c["tokens"]))
    summary[name] = agg

# compare aggregates against instrument
for name in profiles:
    mine, theirs = summary[name], instrument["profiles"][name]
    print("=== " + name)
    for k in ("projected_text_sha256", "changed_leaf_count", "changed_task_count",
              "string_leaf_count", "changed_leaves_with_multiple_occurrences",
              "remaining_known_tokens_text"):
        print("  %-40s mine=%r theirs=%r %s" % (k, mine[k], theirs.get(k), "OK" if mine[k] == theirs.get(k) else "DIFF"))
    for k in ("changed_leaves_by_category", "changed_leaves_by_path_template",
              "changed_leaves_by_token", "changed_tasks_by_token"):
        same = mine[k] == theirs.get(k)
        print("  %-40s %s" % (k, "OK" if same else "DIFF"))
        if not same:
            print("    mine  =", json.dumps(mine[k], sort_keys=True))
            print("    theirs=", json.dumps(theirs.get(k), sort_keys=True))
print("PROBLEMS", len(problems))
for p in problems[:40]:
    print("  ", p)

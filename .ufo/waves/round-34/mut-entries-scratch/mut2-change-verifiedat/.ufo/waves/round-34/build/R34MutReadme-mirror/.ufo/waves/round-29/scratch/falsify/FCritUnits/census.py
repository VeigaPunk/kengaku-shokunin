"""Independent unit census for round-29 C1. Does not read or import plans/config_projection.py."""
import collections, json, pathlib, sys

ROOT = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
RAW = (ROOT / "plans/fixtures/r28/webarena/config_files/test.raw.json").read_bytes().decode("utf-8")
PROFILES = json.loads((ROOT / "plans/fixtures/r29/profiles.json").read_text("utf-8"))
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {n: f"__{n}__" for n in ORDER}


def leaves(node, path):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from leaves(v, path + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaves(v, path + (i,))


def keys(node):
    if isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from keys(v)
    elif isinstance(node, list):
        for v in node:
            yield from keys(v)


def tmpl(path):
    return ".".join("[]" if isinstance(p, int) else p for p in path).replace(".[]", "[]")


data = json.loads(RAW)
out = {}
out["tasks"] = len(data)
out["distinct_ids"] = len({t["task_id"] for t in data})
out["text_occ"] = {n: RAW.count(TOK[n]) for n in ORDER}
out["text_occ_total"] = sum(out["text_occ"].values())
out["key_occ"] = sum(k.count(TOK[n]) for t in data for k in keys(t) for n in ORDER)

leaf_occ = collections.Counter()
leaf_by_tok = collections.Counter()
task_by_tok = collections.Counter()
multi_occ_leaves = []
multi_tok_leaves = []
tasks_any = 0
tasks_k = collections.Counter()
per_task_leaves = []
all_leaves = 0
tmpl_leaves = collections.Counter()
tmpl_occ = collections.Counter()
for idx, t in enumerate(data):
    toks_here = set()
    nleaf = 0
    for p, s in leaves(t, ()):
        if idx == 0 or True:
            all_leaves += 1
        c = {n: s.count(TOK[n]) for n in ORDER}
        tot = sum(c.values())
        if not tot:
            continue
        nleaf += 1
        tmpl_leaves[tmpl(p)] += 1
        tmpl_occ[tmpl(p)] += tot
        for n in ORDER:
            leaf_occ[n] += c[n]
            if c[n]:
                leaf_by_tok[n] += 1
                toks_here.add(n)
        if tot > 1:
            multi_occ_leaves.append((t["task_id"], tmpl(p), {n: v for n, v in c.items() if v}))
        if sum(1 for v in c.values() if v) > 1:
            multi_tok_leaves.append((t["task_id"], tmpl(p), {n: v for n, v in c.items() if v}))
    for n in toks_here:
        task_by_tok[n] += 1
    if toks_here:
        tasks_any += 1
    tasks_k[len(toks_here)] += 1
    per_task_leaves.append(nleaf)

out["all_string_leaves"] = all_leaves
out["leaf_occ_total"] = sum(leaf_occ.values())
out["changed_leaves"] = sum(per_task_leaves)
out["leaf_by_tok"] = {n: leaf_by_tok[n] for n in ORDER}
out["leaf_by_tok_sum"] = sum(leaf_by_tok.values())
out["task_by_tok"] = {n: task_by_tok[n] for n in ORDER}
out["task_by_tok_sum"] = sum(task_by_tok.values())
out["tasks_any"] = tasks_any
out["tasks_by_distinct_token_count"] = dict(sorted(tasks_k.items()))
out["multi_occ_leaf_count"] = len(multi_occ_leaves)
out["multi_occ_surplus"] = sum(sum(c.values()) - 1 for _, _, c in multi_occ_leaves)
out["multi_occ_leaf_occ"] = sum(sum(c.values()) for _, _, c in multi_occ_leaves)
out["multi_occ_leaves"] = multi_occ_leaves
out["multi_tok_leaf_count"] = len(multi_tok_leaves)
out["multi_tok_leaves"] = multi_tok_leaves
out["tmpl_leaves"] = dict(tmpl_leaves)
out["tmpl_occ"] = dict(tmpl_occ)
out["per_task_leaves_min_max"] = [min(per_task_leaves), max(per_task_leaves)]

prof = {}
for name, spec in PROFILES.items():
    txt = RAW
    applied = {}
    for n in ORDER:
        applied[n] = txt.count(TOK[n])
        txt = txt.replace(TOK[n], spec["values"][n])
    pdata = json.loads(txt)
    ch_leaves = 0
    ch_tasks = 0
    nleaves = 0
    for a, b in zip(data, pdata):
        la = list(leaves(a, ()))
        lb = list(leaves(b, ()))
        assert [p for p, _ in la] == [p for p, _ in lb]
        nleaves += len(la)
        d = sum(1 for (_, x), (_, y) in zip(la, lb) if x != y)
        ch_leaves += d
        ch_tasks += bool(d)
    prof[name] = {"applied": applied, "applied_total": sum(applied.values()), "parsed": len(pdata),
                  "string_leaves": nleaves, "changed_leaves": ch_leaves, "changed_tasks": ch_tasks,
                  "dslash": txt.count("//") - RAW.count("//") - sum(applied.values())}
out["profiles"] = prof
out["projections"] = sum(p["parsed"] for p in prof.values())
out["writes_per_run"] = 1 + len(data)
out["write_events_3_runs"] = 3 * (1 + len(data))
out["distinct_paths_3_runs_same_dir"] = len({"config_files/test.json"} | {f"config_files/{i}.json" for i in range(len(data))})
json.dump(out, sys.stdout, indent=1, sort_keys=False)
print()

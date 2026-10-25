#!/usr/bin/env python3
"""Randomised differential probe of the instrument's diff()/leaf accounting vs an independent walker.

Scope: diff() structure-change detection, changed-leaf enumeration, per-token/per-task leaf
census, carrier invariant, and the decoded remaining-token census (keys included).
"""
import importlib.util
import json
import random
import sys
import traceback

spec = importlib.util.spec_from_file_location("cp", "/tmp/fr29d/cp.py")
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

ORDER = cp.ORDER
TOKENS = ["__%s__" % n for n in ORDER]
VALUES = {n: "http://%s.invalid:1" % n.lower().replace("_", "-") for n in ORDER}


def ptr(path):
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in path)


def walk(original, projected, path, changed, problems):
    if type(original) is not type(projected):
        problems.append(ptr(path))
    elif isinstance(original, dict):
        if list(original) != list(projected):
            problems.append(ptr(path))
        else:
            for key in original:
                walk(original[key], projected[key], path + (key,), changed, problems)
    elif isinstance(original, list):
        if len(original) != len(projected):
            problems.append(ptr(path))
        else:
            for i, item in enumerate(original):
                walk(item, projected[i], path + (i,), changed, problems)
    elif isinstance(original, str):
        if original != projected:
            changed.append((path, original, projected))
    elif original != projected:
        problems.append(ptr(path))


def leaves(node, keys=False):
    if isinstance(node, dict):
        for k, v in node.items():
            if keys:
                yield k
            yield from leaves(v, keys)
    elif isinstance(node, list):
        for v in node:
            yield from leaves(v, keys)
    elif isinstance(node, str):
        yield node


def rand_scalar(rng, depth):
    kind = rng.choice(["s", "s", "s", "i", "b", "n", "f"])
    if kind == "s":
        bits = []
        for _ in range(rng.randint(0, 3)):
            bits.append(rng.choice([
                rng.choice(TOKENS),
                rng.choice(TOKENS).replace("_", "\\u005f"),
                "x", "a/b", "é", "", "__other__", "a\\nb",
            ]))
        return "".join(bits)
    if kind == "i":
        return rng.randint(-5, 5)
    if kind == "b":
        return rng.choice([True, False])
    if kind == "n":
        return None
    return rng.choice([0.5, 1.0, 2])


def rand_node(rng, depth=0):
    if depth > 2:
        return rand_scalar(rng, depth)
    kind = rng.choice(["s", "i", "b", "n", "d", "l", "d", "l"])
    if kind == "d":
        keys = rng.sample(["a", "b", "c", "__GITLAB__", "0", "x/y"], rng.randint(1, 3))
        return {k: rand_node(rng, depth + 1) for k in keys}
    if kind == "l":
        return [rand_node(rng, depth + 1) for _ in range(rng.randint(0, 3))]
    return rand_scalar(rng, depth)


def main():
    rng = random.Random(20261021)
    stats = {"cases": 0, "exceptions": 0, "unexplained_gt0": 0, "count_mismatch": 0, "pointer_mismatch": 0,
             "census_mismatch": 0, "structural_mismatch": 0, "finding_unexpected": 0}
    examples = []
    for case in range(4000):
        n = rng.randint(1, 3)
        raw_obj = [{"task_id": i} for i in range(n)]
        for t in raw_obj:
            node = rand_node(rng, 1)
            t.update(node if isinstance(node, dict) else {"k": node})
        raw = json.dumps(raw_obj, ensure_ascii=rng.choice([True, False]))
        try:
            result, findings = cp.audit_text(raw, {"distinct_origins": {"purpose": "fuzz", "values": VALUES}})
        except Exception as error:
            stats["exceptions"] += 1
            if len(examples) < 8:
                examples.append(("EXC", raw, type(error).__name__, str(error)))
            continue
        stats["cases"] += 1
        rec = result["profiles"]["distinct_origins"]
        try:
            original = json.loads(raw)
        except ValueError:
            continue
        projected_text = raw
        for name in ORDER:
            projected_text = projected_text.replace("__%s__" % name, VALUES[name])
        try:
            projected = json.loads(projected_text)
        except ValueError:
            continue
        changed, problems = [], []
        walk(original, projected, (), changed, problems)
        if len(changed) != rec["changed_leaf_count"]:
            stats["count_mismatch"] += 1
            if len(examples) < 8:
                examples.append(("COUNT", raw, len(changed), rec["changed_leaf_count"]))
        inst_ptrs = sorted(l["json_pointer"] for t in rec["tasks"] for l in t["changed_leaves"])
        orc_ptrs = sorted(ptr(p) for p, _, _ in changed)
        if inst_ptrs != orc_ptrs:
            stats["pointer_mismatch"] += 1
            if len(examples) < 8:
                examples.append(("PTR", raw, orc_ptrs, inst_ptrs))
        # per-token leaf census: instrument vs independent
        mine = {t: 0 for t in TOKENS}
        for _, before, _ in changed:
            for tok in TOKENS:
                if tok in before:
                    mine[tok] += 1
        if mine != rec["changed_leaves_by_token"]:
            stats["census_mismatch"] += 1
            if len(examples) < 8:
                examples.append(("CENSUS", raw, mine, rec["changed_leaves_by_token"]))
        # structural problems: independent vs instrument finding
        inst_struct = [f for f in findings if f["id"] == "projection_structure_changed"]
        if bool(problems) != bool(inst_struct):
            stats["structural_mismatch"] += 1
            if len(examples) < 8:
                examples.append(("STRUCT", raw, problems, inst_struct))
        # carrier invariant reachability: unexplained > 0 ?
        unexplained = sum(1 for _, before, _ in changed if not [t for t in TOKENS if t in before])
        if unexplained:
            stats["unexplained_gt0"] += 1
            if len(examples) < 8:
                examples.append(("UNEXPL", raw, unexplained, None))
        # decoded census: independent
        dec = {t: sum(s.count(t) for s in leaves(projected, True)) for t in TOKENS}
        if dec != rec["remaining_known_tokens_decoded"]:
            stats["census_mismatch"] += 1
            if len(examples) < 8:
                examples.append(("DECODED", raw, dec, rec["remaining_known_tokens_decoded"]))
    print(json.dumps(stats, indent=1))
    for e in examples:
        print(e)
    print("sys.exit", sys.exit(0))


main()

#!/usr/bin/env python3
"""Independent re-derivation of the pinned generator's projection (path_prefix focus).

Derived ONLY from:
  - plans/fixtures/r29/generate_test_data.py bytes (read via cat earlier; semantics re-implemented here)
  - plans/fixtures/r28/webarena/config_files/test.raw.json bytes
  - plans/fixtures/r29/profiles.json
Does not read or import plans/config_projection.py.
"""
import hashlib
import json
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW_P = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF_P = ROOT + "/plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOKENS = {n: "__%s__" % n for n in ORDER}


def leaves(obj, path="$"):
    """Yield (path, value) for every leaf; strings counted separately."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, path + "." + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, path + "[%d]" % i)
    else:
        yield path, obj


def string_leaves(obj):
    out = []
    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, p + "." + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, p + "[%d]" % i)
        elif isinstance(o, str):
            out.append((p, o))
    walk(obj, "$")
    return out


def main():
    raw_bytes = open(RAW_P, "rb").read()
    prof = json.loads(open(PROF_P, "rb").read())

    # generator: text-mode read, locale encoding = UTF-8 here, universal newlines
    raw = raw_bytes.decode("utf-8")
    assert "\r" not in raw, "raw has CR; universal-newline handling would matter"

    print("raw_bytes", len(raw_bytes))
    print("raw_text_sha256", hashlib.sha256(raw_bytes).hexdigest())
    print("raw_chars", len(raw))

    raw_occ = {}
    for n in ORDER:
        raw_occ[n] = raw.count(TOKENS[n])
    print("raw_occurrences", json.dumps(raw_occ, sort_keys=True),
          "sum", sum(raw_occ.values()))

    # raw-following-char per token occurrence, and per-occurrence records
    occ_records = []
    for n in ORDER:
        tok = TOKENS[n]
        start = 0
        while True:
            i = raw.find(tok, start)
            if i < 0:
                break
            nxt = raw[i + len(tok)] if i + len(tok) < len(raw) else ""
            occ_records.append((i, n, nxt))
            start = i + len(tok)
    occ_records.sort()
    print("occurrence_records", len(occ_records))
    assert len(occ_records) == sum(raw_occ.values())

    raw_obj = json.loads(raw)
    print("raw_parsed_tasks", len(raw_obj), "distinct_task_ids",
          len({it["task_id"] for it in raw_obj}),
          "task_id_types", sorted({type(it["task_id"]).__name__ for it in raw_obj}))

    profiles = {}
    for pname in ["distinct_origins", "path_prefix", "trailing_slash_sensitivity"]:
        vals = prof[pname]["values"]
        assert set(vals) == set(ORDER), (pname, sorted(vals))
        text = raw
        applied = {}
        for n in ORDER:
            tok = TOKENS[n]
            applied[n] = text.count(tok)
            text = text.replace(tok, vals[n])

        data = json.loads(text)
        sl_raw = string_leaves(raw_obj)
        sl_proj = string_leaves(data)
        assert len(sl_raw) == len(sl_proj)

        # changed leaves: same path, different string value
        changed = []
        for (pa, va), (pb, vb) in zip(sl_raw, sl_proj):
            assert pa == pb
            if va != vb:
                changed.append((pa, va, vb))

        # changed leaves per token (leaf-level, not occurrence-level)
        per_tok_leaves = {n: 0 for n in ORDER}
        multi = 0
        for pa, va, vb in changed:
            toks_in = [n for n in ORDER if TOKENS[n] in va]
            if len(toks_in) > 1:
                multi += 1
            for n in toks_in:
                per_tok_leaves[n] += 1
        # leaves with multiple occurrences of the same token
        multi_occ = 0
        for pa, va, vb in changed:
            if any(va.count(TOKENS[n]) > 1 for n in ORDER):
                multi_occ += 1

        # per-token raw occurrences that changed at least one leaf
        tasks_with_token = {n: 0 for n in ORDER}
        for idx, item in enumerate(data):
            # original counterpart by identity of position (structure identical)
            oi = raw_obj[idx]
            blob_raw = json.dumps(oi, ensure_ascii=False)
            for n in ORDER:
                if TOKENS[n] in blob_raw:
                    tasks_with_token[n] += 1

        # junction: replacement value ends with '/' and raw next char is '/'
        junctions = {n: 0 for n in ORDER}
        jtotal = 0
        for i, n, nxt in occ_records:
            if vals[n].endswith("/") and nxt == "/":
                junctions[n] += 1
                jtotal += 1

        # internal '//' in projected values (naive-count control)
        naive_dd = text.count("//")

        rem_text = {n: text.count(TOKENS[n]) for n in ORDER}

        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        print("\n=== PROFILE", pname, "===")
        print("values", json.dumps(vals, sort_keys=True))
        print("applied_replacements", json.dumps(applied, sort_keys=True))
        print("projected_text_utf8_bytes", len(text.encode("utf-8")))
        print("projected_text_sha256", sha)
        print("parsed_task_count", len(data))
        print("string_leaf_count", len(sl_proj))
        print("changed_leaf_count", len(changed))
        print("changed_leaves_by_token", json.dumps(per_tok_leaves, sort_keys=True))
        print("changed_tasks_by_token", json.dumps(tasks_with_token, sort_keys=True))
        print("changed_leaves_multi_token", multi,
              "changed_leaves_same_token_multi_occurrence", multi_occ)
        print("junction_by_token", json.dumps(junctions, sort_keys=True),
              "junction_total", jtotal)
        print("naive_double_slash_in_text", naive_dd)
        print("remaining_known_tokens_text", json.dumps(rem_text, sort_keys=True))
        profiles[pname] = {
            "sha": sha, "applied": applied, "junctions": jtotal,
            "junction_by_token": junctions, "string_leaves": len(sl_proj),
            "changed": len(changed),
            "per_tok_leaves": per_tok_leaves,
            "tasks_with_token": tasks_with_token,
            "multi_token": multi, "multi_occ": multi_occ,
            "naive_dd": naive_dd,
        }

    # write compact oracle result for later comparison
    with open(ROOT + "/.ufo/waves/round-29/scratch/falsify/FProfilePathPrefix-2/oracle.json", "w") as f:
        json.dump({"raw_sha": hashlib.sha256(raw_bytes).hexdigest(),
                   "raw_occ": raw_occ, "profiles": profiles}, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()

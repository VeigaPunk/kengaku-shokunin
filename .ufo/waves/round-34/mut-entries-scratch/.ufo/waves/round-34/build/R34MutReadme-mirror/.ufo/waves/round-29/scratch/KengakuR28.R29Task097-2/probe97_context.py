"""Round29 C1 independent case for raw task_id 97: context census + witnesses.

Reads only pinned bytes. No production projection code, no upstream execution.
Outputs: field-path token census (sentinel-attributed leaves), task-97 raw
context, per-task re-serialization bytes, placeholder remnants, shuffled-ID
witness, unit separation (occurrences vs leaves vs tasks).
"""
import hashlib
import json

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = ROOT + "/plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TARGET_ID = "97"


def leaves(obj, path=""):
    if isinstance(obj, dict):
        for k in obj:
            yield from leaves(obj[k], path + "." + k if path else k)
    elif isinstance(obj, list):
        for j, v in enumerate(obj):
            yield from leaves(v, path + "[" + str(j) + "]")
    else:
        yield path, obj


def project(text, values):
    s = text
    for tok in ORDER:
        s = s.replace("__" + tok + "__", values[tok])
    return s


def main():
    text = open(RAW, "rb").read().decode("utf-8")
    data = json.loads(text)
    idx = next(i for i, it in enumerate(data) if str(it["task_id"]) == TARGET_ID)
    print("target index", idx)

    # 1. exact raw context around the single __MAP__ occurrence
    pos = text.find("__MAP__", 89414, 90252)
    print("cp_offset_abs", pos, "cp_offset_in_item", pos - 89414)
    print("context", repr(text[pos - 90:pos + 40]))
    print("raw_line_of_offset", text.count("\n", 0, pos) + 1,
          "col_cp", pos - text.rfind("\n", 0, pos))

    # 2. field-path census by sentinel attribution (context, whole population)
    sent = {t: "SENTINEL_" + t + "_X" for t in ORDER}
    proj = project(text, sent)
    after = json.loads(proj)
    print("\nprojected_tasks", len(after))
    for t in ORDER:
        print("sentinel_count_in_projection", t, proj.count(sent[t]))
    unchanged = sum(1 for a, b in zip(data, after) if a == b)
    print("items_byte_equal_after", unchanged, "items_changed", len(data) - unchanged)
    path_hist = {}
    tok_hist = {}
    tasks_touched = set()
    for i, (a, b) in enumerate(zip(data, after)):
        la, lb = dict(leaves(a)), dict(leaves(b))
        for p in la:
            if la[p] != lb[p]:
                path_hist[p] = path_hist.get(p, 0) + 1
                tasks_touched.add(i)
                for t in ORDER:
                    if "__" + t + "__" in (la[p] if isinstance(la[p], str) else ""):
                        tok_hist[t] = tok_hist.get(t, 0) + str(la[p]).count("__" + t + "__")
    print("changed_leaf_paths_global", dict(sorted(path_hist.items())))
    print("occurrences_by_token_in_changed_leaves", dict(sorted(tok_hist.items())))
    print("occurrence_sum", sum(tok_hist.values()))
    print("tasks_with_any_change", len(tasks_touched))
    print("changed_leaves_total", sum(path_hist.values()))

    # 3. non-URL-valued changed leaves (F3): field names other than start_url/reference_url
    nonurl = {p: n for p, n in path_hist.items() if not (p.endswith("start_url") or p.endswith("reference_url"))}
    print("non_url_shaped_changed_paths", nonurl)

    # 4. item97 leaf-by-leaf categories and token presence
    print("\nitem97_keys", list(data[idx].keys()))
    for k, v in data[idx].items():
        tok = [t for t in ORDER if isinstance(v, str) and "__" + t + "__" in v]
        print(" field=%-20s type=%-6s token=%s value=%r" % (k, type(v).__name__, tok, v))

    # 5. per-profile start_url values + verbatim containment + per-task artifact bytes
    profiles = json.load(open(PROFILES))
    for pn in profiles:
        vals = profiles[pn]["values"]
        p = project(text, vals)
        item = json.loads(p)[idx]
        art = json.dumps(item, indent=2)
        print("\nprofile", pn)
        print(" start_url", repr(item["start_url"]))
        print(" profile_value_occurrences_in_projection", p.count(vals["MAP"]))
        print(" task97_artifact_sha256", hashlib.sha256(art.encode()).hexdigest(),
              "bytes", len(art.encode()))
        print(" artifact_roundtrip_ok", json.loads(art) == item)
        # test.json slice: raw post-replacement text (not re-serialized)
        slice_ok = ('"start_url": "%s"' % vals["MAP"]) in p
        print(" testjson_has_literal_start_url", slice_ok)
        print(" tokens_remaining", {t: p.count("__" + t + "__") for t in ORDER})

    # 6. placeholder remnants in item 97 (all dunder patterns, incl runtime markers)
    import re
    item_text = json.dumps(data[idx])
    print("\ndunder_patterns_item97", sorted(set(re.findall(r"__[A-Za-z0-9_]+__", item_text))))
    print("dunder_patterns_raw_all", sorted(set(re.findall(r"__[A-Za-z0-9_]+__", text))))

    # 7. order/cascade properties on the frozen strings
    print("\nshopping_vs_admin_prefix_collision",
          "__SHOPPING_ADMIN__".count("__SHOPPING__"),
          "__SHOPPING__".count("__SHOPPING_ADMIN__"))
    wrong = text.replace("__MAP__", "http://map.invalid:10106")  # hypothetical wrong order: MAP first
    print("map_first_equals_contract_order", wrong == project(text, profiles["distinct_origins"]["values"]))

    # 8. shuffled-ID witness: enumerate() names by position, not task_id
    w_items = [data[97], data[5], data[811]]
    w_names = ["%d.json" % i for i, _ in enumerate(w_items)]
    print("\nshuffled_witness_filenames", w_names)
    print("shuffled_witness_task_ids", [it["task_id"] for it in w_items])
    print("shuffled_index_eq_id", [n.split(".")[0] == str(it["task_id"]) for n, it in zip(w_names, w_items)])

    # 9. id domain check
    ids = [it["task_id"] for it in data]
    print("\nid_min_max", min(map(int, ids)), max(map(int, ids)),
          "ids_equal_index_order", all(str(i) == ids[i] for i in range(len(ids))))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent re-derivation for raw task_id 811.

Derived ONLY from: round-29 prereg TEXT, pinned generator bytes, pinned raw
file bytes, pinned profiles.json.  Does not read or import
plans/config_projection.py.
"""
import hashlib
import json
import re
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = ROOT + "/plans/fixtures/r29/profiles.json"
MANIFEST = ROOT + "/plans/fixtures/r29/manifest.json"
INSTRUMENT_JSON = "/tmp/r29_fcase811_json.json"
TARGET = 811

# Replacement order transcribed from the pinned generator bytes (lines 11-16).
ORDER = [("GITLAB", "__GITLAB__"), ("REDDIT", "__REDDIT__"),
         ("SHOPPING", "__SHOPPING__"), ("SHOPPING_ADMIN", "__SHOPPING_ADMIN__"),
         ("WIKIPEDIA", "__WIKIPEDIA__"), ("MAP", "__MAP__")]


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def project(text, values):
    out = text
    per = {}
    for name, tok in ORDER:
        n = out.count(tok)
        per[name] = n  # occurrences present when this step runs
        out = out.replace(tok, values[name])
    return out, per


def walk_changed(orig, proj, path="", leaves=None):
    """Yield changed string leaves with pointer, path template, tokens, counts."""
    if leaves is None:
        leaves = []
    if isinstance(orig, dict) and isinstance(proj, dict):
        assert list(orig.keys()) == list(proj.keys()), (path, "key drift")
        for k in orig:
            walk_changed(orig[k], proj[k], path + "/" + k, leaves)
    elif isinstance(orig, list) and isinstance(proj, list):
        assert len(orig) == len(proj), (path, "length drift")
        for i, (a, b) in enumerate(zip(orig, proj)):
            walk_changed(a, b, path + "/" + str(i), leaves)
    else:
        if orig != proj:
            assert isinstance(orig, str) and isinstance(proj, str), (path, "type drift")
            toks, counts = [], {}
            for name, tok in ORDER:
                c = orig.count(tok)
                if c:
                    toks.append(tok)
                    counts[tok] = c
            leaves.append({
                "path": path,
                "path_template": re.sub(r"/\d+", "[]", path)
                                 .lstrip("/").replace("/", "."),
                "original": orig,
                "projected": proj,
                "tokens": toks,
                "token_occurrences": counts,
                "total_occurrences": sum(counts.values()),
            })
    return leaves


def url_category(value, toks):
    """URL-valued iff the value's leading component is a scheme/host shape or a
    bare placeholder resolved to one.  Order-insensitive: replace tokens with a
    stand-in and test for an absolute URL at string start."""
    v = value
    for _, tok in ORDER:
        v = v.replace(tok, "http://H.invalid")
    return bool(re.match(r"^https?://[^/\s]+(?:[/?#]|$)", v))


def main():
    raw_bytes = open(RAW, "rb").read()
    text = raw_bytes.decode("utf-8")
    manifest = json.load(open(MANIFEST))
    profiles = json.load(open(PROFILES))
    inst = json.load(open(INSTRUMENT_JSON))

    print("raw_bytes=%d text_codepoints=%d ascii=%s cr=%d raw_sha256=%s"
          % (len(raw_bytes), len(text), text.isascii(), text.count("\r"),
             sha256(raw_bytes)))
    print("manifest_replacement_order=%s" % manifest["replacement_order"])
    print("manifest_sha256=%s instrument_manifest=%s"
          % (sha256(open(MANIFEST, "rb").read()), inst["manifest_sha256"]))
    if sha256(open(MANIFEST, "rb").read()) != inst["manifest_sha256"]:
        print("MANIFEST_MISMATCH")

    orig_tasks = json.loads(text)
    print("orig_parsed=%d task_ids_ordered_0_811=%s"
          % (len(orig_tasks),
             [t.get("task_id") for t in orig_tasks] == list(range(812))))
    orig_item = orig_tasks[TARGET]

    # token census on the raw text and inside the target item's string leaves
    census = {tok: text.count(tok) for _, tok in ORDER}
    print("raw_token_census=%s total=%d" % (census, sum(census.values())))
    target_census = {tok: 0 for _, tok in ORDER}
    def count_all(o):
        if isinstance(o, dict):
            for v in o.values():
                count_all(v)
        elif isinstance(o, list):
            for v in o:
                count_all(v)
        elif isinstance(o, str):
            for _, tok in ORDER:
                target_census[tok] += o.count(tok)
    count_all(orig_item)
    print("target_item_token_census=%s" % target_census)

    results = {}
    for pname in profiles:
        values = profiles[pname]["values"]
        proj_text, steps = project(text, values)
        proj_tasks = json.loads(proj_text)
        if len(proj_tasks) != 812:
            print("PARSE_COUNT_MISMATCH", pname, len(proj_tasks))
        proj_item = proj_tasks[TARGET]
        leaves = walk_changed(orig_item, proj_item)
        cats = {}
        for lf in leaves:
            lf["category"] = "url_field" if url_category(lf["original"],
                                                         lf["tokens"]) else "non_url_field"
            cats[lf["category"]] = cats.get(lf["category"], 0) + 1

        dumps = json.dumps(proj_item, indent=2)
        value = {
            "projected_text_sha256": sha256(proj_text.encode("utf-8")),
            "steps": {k: steps[k] for k, _ in ORDER},
            "parsed_task_count": len(proj_tasks),
            "item_task_id": proj_item.get("task_id"),
            "index_equals_task_id": proj_item.get("task_id") == TARGET,
            "output_filename": "config_files/%d.json" % TARGET,
            "changed_leaves": leaves,
            "changed_category_counts": cats,
            "would_be_file_sha256_ensure_ascii_true": sha256(dumps.encode("utf-8")),
            "would_be_file_sha256_ensure_ascii_false": sha256(
                json.dumps(proj_item, indent=2, ensure_ascii=False).encode("utf-8")),
            "would_be_bytes_len": len(dumps.encode("utf-8")),
            "projected_item": proj_item,
        }
        results[pname] = value

    # global multi-occurrence census from the raw text, independent of instrument
    multi = []
    base_proj = json.loads(project(text, profiles["distinct_origins"]["values"])[0])
    for ti, item in enumerate(orig_tasks):
        for lf in walk_changed(item, base_proj[ti]):
            if lf["total_occurrences"] > 1:
                multi.append((ti, lf["path"], lf["token_occurrences"]))
    print("global_multi_occurrence_leaves=%d" % len(multi))
    for m in multi:
        print("  multi task=%d path=%s counts=%s" % m)
    print("multi_in_target=%s"
          % [m for m in multi if m[0] == TARGET])

    print("\n=== PER-PROFILE INDEPENDENT RESULT vs INSTRUMENT RECORD ===")
    mismatches = []
    for pname, mine in results.items():
        ip = inst["profiles"][pname]
        it = ip["tasks"][TARGET]
        print("\n--- profile %s" % pname)
        checks = [
            ("projected_text_sha256", mine["projected_text_sha256"], ip["projected_text_sha256"]),
            ("parsed_task_count", mine["parsed_task_count"], ip["parsed_task_count"]),
            ("output_index", TARGET, it["output_index"]),
            ("item_task_id", mine["item_task_id"], it["task_id"]),
            ("index_equals_task_id", mine["index_equals_task_id"], it["index_equals_task_id"]),
            ("output_filename", mine["output_filename"], it["output_filename"]),
            ("projected_task", mine["projected_item"], it["projected_task"]),
            ("would_be_file_sha256", mine["would_be_file_sha256_ensure_ascii_true"],
             it["would_be_file_sha256"]),
        ]
        for label, a, b in checks:
            ok = a == b
            print("%-24s %s" % (label, "MATCH" if ok else "MISMATCH"))
            if not ok:
                mismatches.append((pname, label, a, b))
        # steps
        for k, v in mine["steps"].items():
            if v != ip["steps"][[s["name"] for s in ip["steps"]].index(k)]["applied_replacements"]:
                mismatches.append((pname, "step_" + k, v, None))
        # changed leaves, field by field
        il = it["changed_leaves"]
        print("leaf_count mine=%d instrument=%d" % (len(mine["changed_leaves"]), len(il)))
        if len(mine["changed_leaves"]) != len(il):
            mismatches.append((pname, "leaf_count", len(mine["changed_leaves"]), len(il)))
        for i in range(max(len(mine["changed_leaves"]), len(il))):
            a = mine["changed_leaves"][i] if i < len(mine["changed_leaves"]) else None
            b = il[i] if i < len(il) else None
            if a is None or b is None:
                mismatches.append((pname, "leaf_presence_%d" % i, a, b))
                continue
            for f in ("json_pointer", "path_template", "category", "original",
                      "projected", "tokens"):
                key = "path" if f == "json_pointer" else f
                av = a[key]
                if f == "json_pointer":
                    av = "/811" + a["path"]
                if av != b[f]:
                    mismatches.append((pname, "leaf%d.%s" % (i, f), av, b[f]))
            print("  leaf[%d] %s cat=%s tokens=%s occ=%d" %
                  (i, b["json_pointer"], b["category"], b["tokens"],
                   a["total_occurrences"]))
            if a["token_occurrences"] and b["tokens"] != list(a["token_occurrences"]):
                print("    tokens-list-shape mine(occ)=%s instrument=%s"
                      % (a["token_occurrences"], b["tokens"]))
        print("would_be_bytes_len=%d" % mine["would_be_bytes_len"])
        print("ensure_ascii_false_sha=%s" % mine["would_be_file_sha256_ensure_ascii_false"])

    # occurrence provenance offsets claimed for task 811
    print("\n=== OCCURRENCE PROVENANCE (instrument) ===")
    for o in inst["occurrence_provenance"]:
        if o["task_index"] != TARGET:
            continue
        off = o["original_input_codepoint_offset"]
        at = text[off:off + len(o["token"])]
        print("pointer=%s offset=%d text_at_offset=%r match=%s"
              % (o["json_pointer"], off, at, at == o["token"]))
        # independent offset: locate within the task segment boundaries
        start = text.find('"task_id": %d' % TARGET)
        seg = text[start:start + 2000]
        rel = seg.find(o["token"])
        print("  segment_start=%d rel_in_segment=%d implied=%d agree=%s"
              % (start, rel, start + rel, start + rel == off))

    print("\n=== MISMATCHES: %d ===" % len(mismatches))
    for m in mismatches:
        print("MISMATCH %s %s mine=%r instrument=%r" % m)
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())

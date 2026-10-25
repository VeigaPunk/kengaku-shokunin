"""Independent re-derivation of the pinned generator projection for output index 66.

Authority: prereg TEXT + generator bytes as read by this seat + pinned raw file + profiles.
Does NOT read or import plans/config_projection.py; compares against its --json OUTPUT only.
"""
import json, hashlib, sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = LANE + "/plans/fixtures/r29/profiles.json"
INSTR = LANE + "/.ufo/waves/round-29/scratch/falsify/FCase066/instrument.json"
IDX = 66

# generator lines 11-16 order, transcribed from pinned bytes
ORDER = [("GITLAB", "__GITLAB__"), ("REDDIT", "__REDDIT__"),
         ("SHOPPING", "__SHOPPING__"), ("SHOPPING_ADMIN", "__SHOPPING_ADMIN__"),
         ("WIKIPEDIA", "__WIKIPEDIA__"), ("MAP", "__MAP__")]

raw_bytes = open(RAW, "rb").read()
raw_text = raw_bytes.decode("utf-8")  # pinned file is ASCII; locale-independent here
orig_data = json.loads(raw_text)
profiles_doc = json.load(open(PROF))


def leaves(o, ptr=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, ptr + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, ptr + "/[" + str(i) + "]")
    else:
        yield ptr, o


def leaf_diff(a, b):
    out = []
    la = dict(leaves(a)); lb = dict(leaves(b))
    assert set(la) == set(lb), (set(la) ^ set(lb))
    for p in la:
        if la[p] != lb[p]:
            out.append((p, la[p], lb[p]))
    return out


def occ(leaf_value, token):
    if not isinstance(leaf_value, str):
        return 0
    n, i = 0, 0
    while True:
        i = leaf_value.find(token, i)
        if i < 0:
            return n
        n += 1
        i += len(token)


report = {"index": IDX, "orig_task_id": orig_data[IDX]["task_id"], "profiles": {}}
inst = json.load(open(INSTR))

for pname, prof in profiles_doc.items():
    vals = prof["values"]
    text = raw_text
    applied = {}
    for name, tok in ORDER:
        applied[name] = text.count(tok)
        text = text.replace(tok, vals[name])
    data = json.loads(text)
    item = data[IDX]
    dumped = json.dumps(item, indent=2)            # generator line 23: json.dump(item, f, indent=2)
    h = hashlib.sha256(dumped.encode("utf-8")).hexdigest()
    h_sorted = hashlib.sha256(json.dumps(item, indent=2, sort_keys=True).encode()).hexdigest()
    diffs = leaf_diff(orig_data[IDX], item)
    # token occurrence census on the ORIGINAL leaf values of this task
    orig_leaves = dict(leaves(orig_data[IDX]))
    changed = []
    for p, o, n in diffs:
        toks = []
        cnt = {}
        for name, tok in ORDER:
            c = occ(o, tok)
            if c:
                toks.append(name); cnt[tok] = c
        changed.append({
            "pointer": "/%d%s" % (IDX, p),
            "original": o,
            "projected": n,
            "tokens": toks,
            "occurrences": cnt,
            "projected_has_any_token": any(t in str(n) for _, t in ORDER),
        })
    # every occurrence position of every token inside task 66's original serialized slice
    # (slice bounds recovered from the parsed doc is not needed; use offsets in whole text via json walk)
    rec = {
        "projected_dump_sha256": h,
        "sorted_keys_sha256": h_sorted,
        "projected_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "task_id": item["task_id"],
        "index_equals_task_id": item["task_id"] == IDX,
        "output_filename": "config_files/%d.json" % IDX,
        "changed_leaves": changed,
        "n_changed_leaves": len(changed),
        "applied_replacements": applied,
        "projected_task": item,
    }
    # oracle comparison against instrument OUTPUT
    irec = inst["profiles"][pname]["tasks"][IDX]
    cmp = {
        "projected_task_equal": irec["projected_task"] == item,
        "would_be_file_sha256_match": irec["would_be_file_sha256"] == h,
        "index_equals_task_id_match": irec["index_equals_task_id"] == rec["index_equals_task_id"],
        "output_filename_match": irec["output_filename"] == rec["output_filename"],
        "task_id_match": irec["task_id"] == rec["task_id"],
        "instrument_changed_leaf_count": len(irec["changed_leaves"]),
        "derived_changed_leaf_count": len(changed),
    }
    # field-by-field changed-leaf comparison
    by_ptr = {c["pointer"]: c for c in changed}
    icmp = []
    for e in irec["changed_leaves"]:
        d = by_ptr.get(e["json_pointer"])
        icmp.append({
            "have_derived": d is not None,
            "pointer": e["json_pointer"],
            "original_match": d is not None and e["original"] == d["original"],
            "projected_match": d is not None and e["projected"] == d["projected"],
            "tokens_match": d is not None and e["tokens"] == d["tokens"],
            "instrument_category": e["category"],
            "instrument_path_template": e["path_template"],
            "derived_occurrences": None if d is None else d["occurrences"],
        })
    missing = sorted(set(by_ptr) - {e["json_pointer"] for e in irec["changed_leaves"]})
    rec["oracle_cmp"] = cmp
    rec["changed_leaf_field_cmp"] = icmp
    rec["derived_pointers_missing_from_instrument"] = missing
    rec["profile_text_sha256_match"] = inst["profiles"][pname]["projected_text_sha256"] == rec["projected_text_sha256"]
    report["profiles"][pname] = rec

# provenance cross-check for task 66
prov66 = [e for e in inst["occurrence_provenance"] if e.get("task_index") == IDX]
pv = []
for e in prov66:
    start = e["original_input_codepoint_offset"]
    tok = e["token"]
    pv.append({
        "pointer": e["json_pointer"],
        "token": tok,
        "offset": start,
        "slice_matches_token": raw_text[start:start + len(tok)] == tok,
        "path_template": e["path_template"],
        "string_role": e["string_role"],
    })
report["provenance66"] = pv
report["provenance66_count"] = len(prov66)
report["raw_text_sha256"] = hashlib.sha256(raw_bytes).hexdigest()
report["instrument_raw_text_sha256"] = inst["raw_text_sha256"]

json.dump(report, open(LANE + "/.ufo/waves/round-29/scratch/falsify/FCase066/derived66.json", "w"), indent=2)
print("WROTE derived66.json")
for pname, r in report["profiles"].items():
    print("==", pname)
    print(" task_id", r["task_id"], "index_eq", r["index_equals_task_id"], "nchanged", r["n_changed_leaves"])
    print(" dump_sha", r["projected_dump_sha256"], "sorted_sha", r["sorted_keys_sha256"])
    print(" cmp", json.dumps(r["oracle_cmp"]))
    print(" text_sha_match", r["profile_text_sha256_match"], r["projected_text_sha256"])
    for c in r["changed_leaf_field_cmp"]:
        print("  leaf", json.dumps(c))
    print("  missing", r["derived_pointers_missing_from_instrument"])
print("prov66", json.dumps(report["provenance66"], indent=1))
print("raw_sha_match", report["raw_text_sha256"] == report["instrument_raw_text_sha256"])

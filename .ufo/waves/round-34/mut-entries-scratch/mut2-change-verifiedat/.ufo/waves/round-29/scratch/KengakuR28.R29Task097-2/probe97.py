"""Independent projection probe for raw task_id 97 (round29 C1, seat KengakuR28.R29Task097-2).

Reads ONLY pinned bytes: r29 manifest, r29 profiles, r28 raw test.raw.json.
Never imports/reads production plans/config_projection.py or upstream code.
Replacement semantics are copied from the inert upstream text contract:
six global str.replace calls in manifest order, then json.loads, then
enumerate() for output filenames.
"""
import hashlib
import json
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = ROOT + "/plans/fixtures/r29/profiles.json"
MANIFEST = ROOT + "/plans/fixtures/r29/manifest.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TARGET_ID = "97"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def spans(text):
    """Top-level array element (codepoint) spans using raw_decode."""
    dec = json.JSONDecoder()
    i = text.index("[") + 1
    out = []
    n = len(text)
    while True:
        while i < n and text[i] in " \t\r\n,":
            i += 1
        if i >= n or text[i] == "]":
            return out
        obj, end = dec.raw_decode(text, i)
        out.append((i, end, obj))
        i = end


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
    counts = {}
    for tok in ORDER:
        n = s.count("__" + tok + "__")
        counts[tok] = n
        s = s.replace("__" + tok + "__", values[tok])
    return s, counts


def main():
    print("sha.raw", sha(RAW))
    print("sha.profiles", sha(PROFILES))
    print("sha.manifest", sha(MANIFEST))
    text = open(RAW, "rb").read().decode("utf-8")
    before = json.loads(text)
    sp = spans(text)
    print("tasks", len(before), "spans", len(sp))
    ids = [it["task_id"] for it in before]
    print("distinct_ids", len(set(ids)))
    eq = [i for i, it in enumerate(before) if str(it["task_id"]) == str(i)]
    print("index_eq_taskid", len(eq), "of", len(before))
    print("target_index", [i for i, it in enumerate(before) if str(it["task_id"]) == TARGET_ID])
    idx = next(i for i, it in enumerate(before) if str(it["task_id"]) == TARGET_ID)
    a, b = sp[idx][0], sp[idx][1]
    print("target_span_codepoints", a, b, "len", b - a)
    print("target_text_head", text[a:a + 60].replace("\n", "\\n"))
    print("target_text_tail", text[b - 60:b].replace("\n", "\\n"))

    profiles = json.load(open(PROFILES))
    print("profiles", sorted(profiles), [sorted(profiles[k]["values"]) for k in profiles])

    for pname in profiles:
        values = profiles[pname]["values"]
        proj, counts = project(text, values)
        after = json.loads(proj)  # must parse: no quote/backslash values
        pa, pb = spans(proj)[idx][0], spans(proj)[idx][1]
        item_before, item_after = before[idx], after[idx]
        lb = dict(leaves(item_before))
        la = dict(leaves(item_after))
        assert set(lb) == set(la), "leaf path set changed"
        changed = [p for p in lb if lb[p] != la[p]]
        print("\n== profile", pname)
        print("replace_counts", counts, "sum", sum(counts.values()))
        print("projection_sha256", hashlib.sha256(proj.encode()).hexdigest())
        print("parsed_tasks", len(after), "target_ordinal", idx)
        print("changed_leaf_paths", changed)
        for p in changed:
            print("  %s: %r -> %r" % (p, lb[p], la[p]))
        print("changed_leaf_count", len(changed))
        # ordinal/filename for target
        filename = "%d.json" % idx
        out_item = json.loads(proj)[idx]
        print("output_filename", filename, "out_task_id", out_item["task_id"],
              "index_eq_id", filename == str(out_item["task_id"]) + ".json")
        # per-item token occurrences within the codepoint span
        for tok in ORDER:
            t = "__" + tok + "__"
            local = []
            j = text.find(t, a, b)
            while j != -1 and j < b:
                local.append(j)
                j = text.find(t, j + 1, b)
            if local or counts[tok]:
                print("  token", tok, "item_occ", len(local),
                      "global_occ", counts[tok],
                      "item_cp_offsets", local[:12])
        # non-string leaves touched? report all changed paths types
        print("changed_value_types", sorted({type(la[p]).__name__ for p in changed}))


if __name__ == "__main__":
    main()

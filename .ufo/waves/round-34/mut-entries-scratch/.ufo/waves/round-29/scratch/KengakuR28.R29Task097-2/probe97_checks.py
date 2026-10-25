"""Round29 C1 case97: corrections + completeness witnesses.

Fixes probe2's str-vs-int comparison, proves per-item occurrence attribution is
complete, checks key-name stability, artifact diffs, and order semantics.
Reads only pinned bytes; no production projection code.
"""
import hashlib
import json

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = ROOT + "/plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TARGET_ID = 97


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


def spans(text):
    dec = json.JSONDecoder()
    i = text.index("[") + 1
    out = []
    while True:
        while i < len(text) and text[i] in " \t\r\n,":
            i += 1
        if i >= len(text) or text[i] == "]":
            return out
        obj, end = dec.raw_decode(text, i)
        out.append((i, end, obj))
        i = end


def main():
    text = open(RAW, "rb").read().decode("utf-8")
    data = json.loads(text)
    sp = spans(text)
    ids = [it["task_id"] for it in data]
    print("task_id_types", sorted({type(x).__name__ for x in ids}))
    print("ids_equal_range", ids == list(range(812)))
    print("index_str_eq_task_id", all(str(i) == str(ids[i]) for i in range(812)))
    print("index_int_eq_task_id", sum(1 for i in range(812) if i == ids[i]))

    # per-token: occurrences inside item spans vs whole text
    for tok in ORDER:
        t = "__" + tok + "__"
        per_item = 0
        for a, b, _ in sp:
            j = text.find(t, a, b)
            while j != -1 and j < b:
                per_item += 1
                j = text.find(t, j + 1, b)
        print("token", tok, "in_item_spans", per_item, "whole_text", text.count(t),
              "equal", per_item == text.count(t))
    between = 0
    for i in range(len(sp) - 1):
        seg = text[sp[i][1]:sp[i + 1][0]]
        for tok in ORDER:
            between += seg.count("__" + tok + "__")
    print("occurrences_between_item_spans", between)

    # pairwise substring check (order/cascade semantics on frozen tokens)
    pairs = []
    for a in ORDER:
        for b in ORDER:
            if a != b:
                pairs.append((a, b, ("__" + a + "__") in ("__" + b + "__")))
    print("token_containment_pairs", [(a, b) for a, b, c in pairs if c] or "none")

    # profile values contain no token
    profiles = json.load(open(PROFILES))
    for pn in profiles:
        vals = profiles[pn]["values"]
        hits = [[t for t in ORDER if "__" + t + "__" in v] for v in vals.values()]
        print("profile", pn, "value_contains_token", [h for h in hits if h] or "none")

    # key/path-set stability and occurrence-vs-leaf units per profile
    allpaths = None
    for pn in profiles:
        p = project(text, profiles[pn]["values"])
        after = json.loads(p)
        assert len(after) == 812
        assert [it["task_id"] for it in after] == ids
        paths = set()
        occ = 0
        changed = 0
        for a, b in zip(data, after):
            la, lb = dict(leaves(a)), dict(leaves(b))
            assert set(la) == set(lb), pn
            paths |= set(la)
            for k in la:
                if la[k] != lb[k]:
                    changed += 1
                    occ += str(la[k]).count("__")
        print("profile", pn, "changed_leaves", changed, "changed_task_objects",
              sum(1 for a, b in zip(data, after) if a != b), "pathset_stable", True)
        if allpaths is None:
            allpaths = paths
        else:
            assert paths == allpaths

    # item97 exact line/col of the token, and artifact diffs across profiles
    pos = 89560
    ls = text.rfind("\n", 0, pos) + 1
    le = text.find("\n", pos)
    print("line", text.count("\n", 0, pos) + 1, "col0", pos - ls, "line_text", repr(text[ls:le]))
    arts = {}
    for pn in profiles:
        item = json.loads(project(text, profiles[pn]["values"]))[TARGET_ID]
        art = json.dumps(item, indent=2)
        arts[pn] = art
        print("artifact", pn, len(art.encode()), hashlib.sha256(art.encode()).hexdigest(),
              "ends", repr(art[-12:]))
    base = json.loads(arts["distinct_origins"])
    for pn in ("path_prefix", "trailing_slash_sensitivity"):
        d = json.loads(arts[pn])
        diff = [k for k in base if base[k] != d[k]]
        print("artifact_diff_vs_distinct", pn, diff,
              [(base[k], d[k]) for k in diff])

    # hand witness: order matters only when a profile value contains a later token
    t2 = "A__GITLAB__B"
    contract = t2.replace("__GITLAB__", "__MAP__").replace("__MAP__", "X")
    reverse = t2.replace("__MAP__", "X").replace("__GITLAB__", "__MAP__")
    print("order_witness contract", contract, "reverse", reverse,
          "differ", contract != reverse)

    # shuffled witness: filename is enumerate index, code never reads task_id
    w = [data[97], data[5], data[811]]
    print("shuffled", [(i, it["task_id"], "%d.json" % i) for i, it in enumerate(w)])


if __name__ == "__main__":
    main()

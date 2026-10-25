#!/usr/bin/env python3
"""Independent oracle for r29 start_url leaf census.

Derived only from the prereg TEXT, pinned generator bytes, manifest, profiles and
the raw pinned task file.  Does NOT read/import plans/config_projection.py.
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT + "/plans/fixtures/r29/profiles.json"

ORDER = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
         "__WIKIPEDIA__", "__MAP__"]
URL_TEMPLATES = {"start_url", "eval.reference_url", "eval.program_html[].url"}


def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None


def walk_leaf(obj, path, out):
    """Yield (path_template, json_pointer, value) for every leaf."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                walk_leaf(v, path + (k,), out)
            else:
                out.append((_tpl(path, k, None), "/" + "/".join([p for p in path] + [k]), v))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, (dict, list)):
                walk_leaf(v, path + ("[]", str(i)), out)
            else:
                out.append((_tpl(path, None, True), "/" + "/".join([p for p in path] + [str(i)]), v))
    else:
        raise TypeError("top-level scalar")


def _tpl(path, key, arr):
    parts = list(path)
    t = ".".join(parts)
    if key is not None:
        t = (t + "." if t else "") + key
    if arr:
        t += "[]"
    return t


def leaves(doc):
    out = []
    for i, item in enumerate(doc):
        walk_leaf(item, ("[]",), out)
        # rename: top-level array element marker -> drop leading "[]" for templates and
        # prefix pointer index for uniqueness
    return out


def walk_doc(doc):
    """(template, pointer, value) for the whole top-level task array."""
    out = []
    for i, item in enumerate(doc):
        _walk(item, [], i, out)
    return out


def _walk(obj, path, idx, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            _walk(v, path + [k], idx, out)
    elif isinstance(obj, list):
        for j, v in enumerate(obj):
            _walk(v, path + ["[]"], idx, out)
    else:
        tpl = ".".join(path)
        ptr = "/" + str(idx) + "".join("/" + p for p in path)
        out.append((tpl, ptr, obj))


def tok_in(v):
    if not isinstance(v, str):
        return []
    return [t for t in ORDER if t in v]


def main():
    raw = open(RAW, "r", encoding="utf-8").read()
    profiles = json.load(open(PROF, encoding="utf-8"))
    base = json.loads(raw)
    base_leaves = walk_doc(base)
    print("raw_chars", len(raw), "raw_bytes", len(raw.encode("utf-8")))
    print("raw_sha256", hashlib.sha256(raw.encode("utf-8")).hexdigest())
    print("input_tasks", len(base))

    # duplicate-key detection inside task objects
    dup_flag = []

    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                dup_flag.append(k)
            seen.add(k)
        return dict(pairs)

    json.loads(raw, object_pairs_hook=hook)
    print("raw_duplicate_keys", len(dup_flag))

    print("total_leaves", len(base_leaves))
    print("string_leaves", sum(1 for _, _, v in base_leaves if isinstance(v, str)))
    print("leaf_type_counts", dict(Counter(type(v).__name__ for _, _, v in base_leaves)))
    print("leaf_templates", len(set(t for t, _, _ in base_leaves)))
    print("start_url_leaves", sum(1 for t, _, _ in base_leaves if t == "start_url"))
    print("start_url_nonstr", sum(1 for t, _, v in base_leaves
                                   if t == "start_url" and not isinstance(v, str)))
    print("start_url_with_token", sum(1 for t, _, v in base_leaves
                                     if t == "start_url" and tok_in(v)))
    print("start_url_by_token",
          dict(Counter(tok for t, _, v in base_leaves if t == "start_url"
                       for tok in tok_in(v))))
    # tokens occurring in any leaf outside start_url but whose template ends with start_url
    print("starturl_named_templates",
          sorted(set(t for t, _, _ in base_leaves if t.split(".")[-1] == "start_url")))

    base_byleaf = {ptr: (tpl, v) for tpl, ptr, v in base_leaves}

    all_prof = {}
    for pname, pobj in profiles.items():
        vals = pobj["values"]
        text = raw
        applied = {}
        for tok in ORDER:
            name = tok.strip("_")
            n = text.count(tok)
            applied[tok] = n
            text = text.replace(tok, vals[name])
        proj = json.loads(text)
        proj_leaves = walk_doc(proj)
        proj_byptr = {ptr: (tpl, v) for tpl, ptr, v in proj_leaves}
        assert list(base_byleaf) == list(proj_byptr), "leaf pointer set changed"
        changed = []
        for ptr, (tpl, v0) in base_byleaf.items():
            v1 = proj_byptr[ptr][1]
            if type(v0) is not type(v1):
                raise SystemExit("type change at " + ptr)
            if v0 != v1:
                changed.append((tpl, ptr, v0, v1))
        c_by_tpl = Counter(t for t, _, _, _ in changed)
        c_by_tok = Counter()
        multi = 0
        per_leaf_tokens = {}
        for tpl, ptr, v0, v1 in changed:
            ts = []
            for tok in ORDER:
                name = tok.strip("_")
                if tok in v0 and tok not in v1:
                    ts.append(tok)
            per_leaf_tokens[ptr] = ts
            if len(ts) > 1:
                multi += 1
            for tok in ts:
                c_by_tok[tok] += 1
        changed_tasks = set(ptr.split("/")[1] for _, ptr, _, _ in changed)
        cat = Counter("url_field" if tpl in URL_TEMPLATES else "non_url_field"
                      for tpl, _, _, _ in changed)
        prof_rec = {
            "applied": applied,
            "projected_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "parsed_task_count": len(proj),
            "string_leaf_count": sum(1 for _, _, v in proj_leaves if isinstance(v, str)),
            "changed_leaf_count": len(changed),
            "changed_leaves_by_path_template": dict(c_by_tpl),
            "changed_leaves_by_category": dict(cat),
            "changed_leaves_by_token": dict(c_by_tok),
            "changed_leaves_with_multiple_occurrences": multi,
            "changed_task_count": len(changed_tasks),
            "start_url_changed": c_by_tpl.get("start_url", 0),
            "start_url_changed_by_token": dict(Counter(
                tok for tpl, ptr, v0, v1 in changed if tpl == "start_url"
                for tok in per_leaf_tokens[ptr])),
            "url_field_templates": sorted(set(t for t, _, _, _ in changed
                                              if t in URL_TEMPLATES)),
            "per_leaf_tokens": per_leaf_tokens,
            "changed": changed,
        }
        # every changed start_url leaf really contains a token on one side
        bad_su = [c for c in changed if c[0] == "start_url" and not per_leaf_tokens[c[1]]]
        prof_rec["start_url_changed_without_token"] = len(bad_su)
        all_prof[pname] = prof_rec
        print("\nPROFILE", pname)
        print(" applied", applied)
        print(" projected_text_sha256", prof_rec["projected_text_sha256"])
        print(" parsed_task_count", prof_rec["parsed_task_count"],
              "string_leaf_count", prof_rec["string_leaf_count"])
        print(" changed_leaf_count", prof_rec["changed_leaf_count"],
              "changed_task_count", prof_rec["changed_task_count"])
        print(" changed_leaves_by_path_template", dict(sorted(c_by_tpl.items())))
        print(" changed_leaves_by_category", dict(sorted(cat.items())))
        print(" changed_leaves_by_token", dict(c_by_tok))
        print(" changed_leaves_with_multiple_occurrences", multi)
        print(" start_url_changed", prof_rec["start_url_changed"],
              "by_token", prof_rec["start_url_changed_by_token"],
              "without_token", prof_rec["start_url_changed_without_token"])

    # start_url task-index sets per profile and token composition
    su_changed_idx = {}
    for pname, rec in all_prof.items():
        su_changed_idx[pname] = sorted({int(ptr.split("/")[1]) for tpl, ptr, _, _ in rec["changed"]
                                        if tpl == "start_url"})
        print("\nSTART_URL", pname, "changed_indices", len(su_changed_idx[pname]),
              "first", su_changed_idx[pname][:5], "last", su_changed_idx[pname][-3:])
    print("start_url_index_set_identical_across_profiles",
          len({tuple(v) for v in su_changed_idx.values()}) == 1)

    # token composition of the 812 start_url leaves (from raw)
    su_tokens = Counter()
    for tpl, ptr, v in base_leaves:
        if tpl == "start_url":
            ts = tok_in(v)
            su_tokens[tuple(ts)] += 1
    print("start_url_token_multisets", {str(k): n for k, n in su_tokens.items()})

    out = {"profiles": {k: {kk: vv for kk, vv in v.items() if kk != "changed"}
                        for k, v in all_prof.items()},
           "start_url_indices": su_changed_idx,
           "start_url_token_multisets": {str(k): n for k, n in su_tokens.items()}}
    open(ROOT + "/.ufo/waves/round-29/scratch/falsify/FPathStartUrl/oracle_result.json",
         "w", encoding="utf-8").write(json.dumps(out, indent=1, sort_keys=True))
    # dump sampled changed start_url leaves for hand re-derivation
    sample = {}
    for pname, rec in all_prof.items():
        su = [c for c in rec["changed"] if c[0] == "start_url"]
        picks = [su[0], su[1], su[len(su) // 2], su[-2], su[-1]]
        sample[pname] = [{"json_pointer": p, "original": a, "projected": b}
                         for _, p, a, b in picks]
    open(ROOT + "/.ufo/waves/round-29/scratch/falsify/FPathStartUrl/oracle_sample.json",
         "w", encoding="utf-8").write(json.dumps(sample, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()

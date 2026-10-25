#!/usr/bin/env python3
"""Oracle v2: independent leaf census of the pinned raw task array.

Derived only from the prereg TEXT, generator bytes, manifest/profiles and raw data.
Does NOT read/import plans/config_projection.py.
"""
import hashlib
import json
from collections import Counter

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT + "/plans/fixtures/r29/profiles.json"
SCRATCH = ROOT + "/.ufo/waves/round-29/scratch/falsify/FPathStartUrl"

ORDER = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
         "__WIKIPEDIA__", "__MAP__"]
URL_TEMPLATES = {"start_url", "eval.reference_url", "eval.program_html[].url"}


def occ(v, tok):
    if not isinstance(v, str):
        return 0
    return v.count(tok)


def walk(obj, path, tpl, out, idx):
    """Emit (template, pointer, value). path = pointer segments; tpl = template string."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            sub_tpl = (tpl + "." if tpl else "") + k
            walk(v, path + [k], sub_tpl, out, idx)
    elif isinstance(obj, list):
        for j, v in enumerate(obj):
            walk(v, path + [str(j)], tpl + "[]", out, idx)
    else:
        out.append((tpl, "/" + str(idx) + "/" + "/".join(path), obj))


def walk_doc(doc):
    out = []
    for i, item in enumerate(doc):
        walk(item, [], "", out, i)
    return out


def main():
    raw = open(RAW, "r", encoding="utf-8").read()
    profiles = json.load(open(PROF, encoding="utf-8"))
    base = json.loads(raw)
    base_leaves = walk_doc(base)
    print("raw_chars", len(raw), "raw_sha256", hashlib.sha256(raw.encode()).hexdigest())
    print("input_tasks", len(base), "total_leaves", len(base_leaves),
          "string_leaves", sum(1 for _, _, v in base_leaves if isinstance(v, str)))
    dups = [p for p, n in Counter(ptr for _, ptr, _ in base_leaves).items() if n > 1]
    print("duplicate_leaf_pointers", len(dups), dups[:5])

    su = [(t, p, v) for t, p, v in base_leaves if t == "start_url"]
    print("start_url_leaves", len(su),
          "all_str", all(isinstance(v, str) for _, _, v in su))
    print("start_url_leaf_indices_unique",
          len({p.split('/')[1] for _, p, _ in su}) == len(su))
    tokcount = Counter()
    multisets = Counter()
    for _, _, v in su:
        ts = tuple(t for t in ORDER if t in v)
        multisets[ts] += 1
        for t in ts:
            tokcount[t] += v.count(t)
    print("start_url_occurrences_by_token", dict(tokcount))
    print("start_url_token_multisets", {str(k): n for k, n in multisets.items()})
    print("start_url_tasks_per_token",
          dict(Counter(t for _, _, v in su for t in ORDER if t in v)))

    base_map = {ptr: (tpl, v) for tpl, ptr, v in base_leaves}
    out = {"start_url": {"leaves": len(su),
                         "occurrences_by_token": dict(tokcount),
                         "tasks_per_token": dict(Counter(
                             t for _, _, v in su for t in ORDER if t in v)),
                         "multisets": {str(k): n for k, n in multisets.items()}},
           "profiles": {}}

    for pname, pobj in profiles.items():
        vals = pobj["values"]
        names = {t: t.strip("_") for t in ORDER}
        applied = {}
        text = raw
        for tok in ORDER:
            applied[tok] = text.count(tok)
            text = text.replace(tok, vals[names[tok]])
        proj = json.loads(text)
        proj_leaves = walk_doc(proj)
        proj_map = {ptr: (tpl, v) for tpl, ptr, v in proj_leaves}
        assert set(base_map) == set(proj_map), "leaf pointer mismatch"
        changed = []
        for ptr, (tpl, v0) in base_map.items():
            v1 = proj_map[ptr][1]
            if v0 != v1:
                changed.append((tpl, ptr, v0, v1))
        c_tpl = Counter(t for t, _, _, _ in changed)
        cats = Counter()
        for tpl, _, _, _ in changed:
            if tpl in URL_TEMPLATES:
                cats["url_field"] += 1
            else:
                cats["non_url_field"] += 1
        # per-token leaf attribution by occurrence on the original side
        by_tok = Counter()
        multi = 0
        for tpl, ptr, v0, v1 in changed:
            occs = {tok: occ(v0, tok) for tok in ORDER}
            occs = {k: n for k, n in occs.items() if n}
            if not occs:
                print("!! changed leaf without token occurrence", pname, ptr, repr(v0)[:80],
                      "->", repr(v1)[:80])
            total = sum(occs.values())
            if total > 1:
                multi += 1
            for tok in occs:
                by_tok[tok] += 1
        # start_url-specific change windows
        su_changed = [(p, a, b) for t, p, a, b in changed if t == "start_url"]
        su_same = [p for p, a, b in su_changed if (a.count("__") != b.count("http"))]
        rec = {
            "applied": applied,
            "projected_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "parsed_task_count": len(proj),
            "string_leaf_count": sum(1 for _, _, v in proj_leaves if isinstance(v, str)),
            "changed_leaf_count": len(changed),
            "changed_leaves_by_path_template": dict(c_tpl),
            "changed_leaves_by_category": dict(cats),
            "changed_leaves_by_token": dict(by_tok),
            "changed_leaves_with_multiple_occurrences": multi,
            "changed_task_count": len({p.split('/')[1] for _, p, _, _ in changed}),
            "start_url_changed": len(su_changed),
            "start_url_changed_indices": sorted(int(p.split('/')[1]) for p, _, _ in su_changed),
            "start_url_by_token": dict(Counter(
                t for tpl, p, v0, v1 in changed if tpl == "start_url"
                for t in ORDER if t in v0)),
            "changed": changed,
        }
        out["profiles"][pname] = rec
        print("\nPROFILE", pname)
        for k in ("applied", "projected_text_sha256", "parsed_task_count",
                  "string_leaf_count", "changed_leaf_count", "changed_task_count"):
            print(" ", k, rec[k])
        print("  changed_leaves_by_path_template", dict(sorted(c_tpl.items())))
        print("  changed_leaves_by_category", dict(sorted(cats.items())))
        print("  changed_leaves_by_token", dict(by_tok))
        print("  changed_leaves_with_multiple_occurrences", multi)
        print("  start_url_changed", len(su_changed),
              "by_token", rec["start_url_by_token"])

    (open(SCRATCH + "/oracle_v2.json", "w").write(json.dumps(out, indent=1, sort_keys=True)))
    # samples: 5 changed start_url leaves per profile
    sample = {}
    for pname, rec in out["profiles"].items():
        su = [(p, a, b) for t, p, a, b in rec["changed"] if t == "start_url"]
        picks = [su[0], su[1], su[len(su) // 2], su[-2], su[-1]]
        sample[pname] = [{"json_pointer": p, "original": a, "projected": b}
                         for p, a, b in picks]
    (open(SCRATCH + "/oracle_sample.json", "w").write(json.dumps(sample, indent=1, sort_keys=True)))
    print("\nsample written")


if __name__ == "__main__":
    main()

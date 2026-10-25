"""R29Task356 independent projection case, v2 (corrected field-role classifier).

Reads pinned inputs once, retains bytes, reproduces the six ordered global
serialized-text replacements in memory, and reports leaf-level effects.
Never imports/executes upstream code; writes nothing outside scratch.
"""
import collections
import hashlib
import json
import os

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(ROOT, "plans/fixtures/r28/webarena/config_files/test.raw.json")
PROF = os.path.join(ROOT, "plans/fixtures/r29/profiles.json")
MAN = os.path.join(ROOT, "plans/fixtures/r29/manifest.json")

ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {k: "__%s__" % k for k in ORDER}
PINS = {
    RAW: "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652",
    PROF: "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018",
    MAN: "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87",
}


def read_once(p):
    with open(p, "rb") as f:
        b = f.read()
    return b, hashlib.sha256(b).hexdigest()


def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, p + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, p + "/" + str(i))
    else:
        yield p, o


def role(ptr):
    parts = [x for x in ptr.split("/") if x]
    if len(parts) < 2:
        return "TOP"
    field = parts[1]
    if field == "start_url":
        return "URL:start_url"
    if field == "eval":
        sub = parts[2] if len(parts) > 2 else "eval"
        if sub == "reference_url":
            return "URL:eval.reference_url"
        if sub == "program_html" and parts[-1] == "url":
            return "URL:eval.program_html.url"
        if sub == "program_html" and "must_include" in parts:
            return "CONTENT:eval.program_html.must_include"
        if sub == "program_html" and parts[-1] == "locator":
            return "LOCATOR:eval.program_html.locator"
        if sub == "reference_answer_raw_annotation":
            return "CONTENT:eval.reference_answer_raw_annotation"
        return "OTHER:eval." + sub
    return "METADATA:" + field


def project(text, vals):
    for k in ORDER:
        text = text.replace(TOK[k], vals[k])
    return text


def main():
    rep = {"pins": {}, "raw": {}, "profiles": {}, "markers": {}}
    bufs = {}
    for p, want in PINS.items():
        b, got = read_once(p)
        bufs[p] = b
        rep["pins"][os.path.relpath(p, ROOT)] = {"bytes": len(b), "sha256": got,
                                                 "pinned": want, "match": got == want}
    assert all(v["match"] for v in rep["pins"].values()), "PIN MISMATCH"

    raw = bufs[RAW].decode("utf-8")            # strict
    original = json.loads(raw)
    orig_leaves = dict(leaves(original, ""))
    rep["raw"] = {
        "bytes": len(bufs[RAW]), "codepoints": len(raw),
        "task_count": len(original),
        "distinct_task_ids": len({d["task_id"] for d in original}),
        "index_equals_task_id": all(d["task_id"] == i for i, d in enumerate(original)),
        "occurrences_by_token": {k: raw.count(TOK[k]) for k in ORDER},
        "occurrence_total": sum(raw.count(TOK[k]) for k in ORDER),
        "runtime_markers": {"__last_url__": raw.count("__last_url__"),
                            "__page__": raw.count("__page__")},
        "all_double_underscore_tokens": sorted(set(
            __import__("re").findall(r"__[A-Za-z0-9_]+__", raw))),
    }

    # role census over the whole parsed document
    rc = collections.Counter()
    for p, v in orig_leaves.items():
        rc[role(p)] += 1
    rep["raw"]["leaf_roles"] = dict(rc)

    profiles = json.loads(bufs[PROF].decode("utf-8"))
    path_sets = []
    for pn, body in profiles.items():
        vals = body["values"]
        per_tok = {}
        for k in ORDER:
            before = raw.count(TOK[k])
            after = project(raw, vals).count(TOK[k])
            per_tok[k] = {"occ_replaced": before, "residual_projected": after}
        text = project(raw, vals)
        proj = json.loads(text)                 # decode failure would raise, not repair
        proj_leaves = dict(leaves(proj, ""))
        changed = []
        by_role = collections.Counter()
        for p, a in orig_leaves.items():
            b = proj_leaves.get(p)
            if isinstance(a, str) and a != b:
                by_role[role(p)] += 1
                changed.append({"path": p, "role": role(p), "old": a, "new": b})
        path_sets.append(frozenset(c["path"] for c in changed))
        seam = text.count("//") - text.count("://")
        rep["profiles"][pn] = {
            "declared_purpose": body.get("purpose"),
            "per_token": per_tok,
            "projection_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "projection_bytes": len(text.encode("utf-8")),
            "parsed_tasks": len(proj),
            "leaf_shape_identical": set(proj_leaves) == set(orig_leaves),
            "changed_leaf_count": len(changed),
            "changed_leaves_by_role": dict(by_role),
            "changed_task_count": len({c["path"].split("/")[1] for c in changed}),
            "seam_double_slashes": seam,
            "runtime_markers_after": {"__last_url__": text.count("__last_url__"),
                                      "__page__": text.count("__page__")},
            "residual_known_tokens": {k: text.count(TOK[k]) for k in ORDER},
            "ordinal_task_id_mismatches": sum(
                1 for i, it in enumerate(proj) if it["task_id"] != i),
            "sample_transforms": {
                "start_url": [{"path": c["path"], "old": c["old"], "new": c["new"]}
                              for c in changed if c["role"] == "URL:start_url"][:1],
                "reference_url": [{"path": c["path"], "old": c["old"], "new": c["new"]}
                                  for c in changed
                                  if c["role"] == "URL:eval.reference_url"][:1],
                "program_html_url": [{"path": c["path"], "old": c["old"], "new": c["new"]}
                                     for c in changed
                                     if c["role"] == "URL:eval.program_html.url"][:1],
                "must_include": [{"path": c["path"], "old": c["old"], "new": c["new"]}
                                 for c in changed
                                 if c["role"] == "CONTENT:eval.program_html.must_include"][:1],
                "annotation": [{"path": c["path"], "old": c["old"], "new": c["new"]}
                               for c in changed
                               if c["role"] == "CONTENT:eval.reference_answer_raw_annotation"][:1],
            },
            "multi_occurrence_leaves": [
                {"path": c["path"], "occurrences": sum(c["old"].count(t) for t in TOK.values())}
                for c in changed if sum(c["old"].count(t) for t in TOK.values()) > 1],
            "compound_separator_leaves": [c["path"] for c in changed
                                          if " |AND| " in c["old"] or " |OR| " in c["old"]],
        }
    rep["cross_profile"] = {
        "changed_path_sets_identical": len(set(path_sets)) == 1,
        "changed_path_count": len(path_sets[0]),
        "task_profile_projections": len(profiles) * len(original),
        "profiles": len(profiles),
    }

    # ordinal-vs-id witness on a shuffled ordering (in memory only)
    sh = list(reversed(original))
    rep["shuffled_witness"] = {
        "construction": "reversed(original), in-memory only, no files written",
        "rows": [{"ordinal": i, "filename": "%d.json" % i, "task_id": it["task_id"]}
                 for i, it in enumerate(sh[:3])],
    }
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()

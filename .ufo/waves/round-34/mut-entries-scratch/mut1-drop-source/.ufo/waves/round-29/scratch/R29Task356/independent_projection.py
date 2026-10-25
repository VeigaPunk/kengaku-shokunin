"""R29Task356 independent projection case.

Reads pinned inputs ONCE, retains bytes, and reproduces the upstream generator's
serialized-text replacement contract in memory. Never imports/executes upstream
code, never writes config_files/, never touches network or environment.

Units are labelled explicitly:
  OCC  = textual occurrences of a token in serialized text
  LEAF = changed string leaves in parsed JSON (path-addressed)
  TASK = tasks in the parsed list
"""
import collections
import hashlib
import json
import os
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(ROOT, "plans/fixtures/r28/webarena/config_files/test.raw.json")
PROFILES = os.path.join(ROOT, "plans/fixtures/r29/profiles.json")
MANIFEST = os.path.join(ROOT, "plans/fixtures/r29/manifest.json")

ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {k: "__%s__" % k for k in ORDER}

PINS = {
    RAW: "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652",
    PROFILES: "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018",
    MANIFEST: "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87",
}


def read_once(path):
    with open(path, "rb") as f:
        b = f.read()
    return b, hashlib.sha256(b).hexdigest()


def leaves(obj, path=""):
    """Yield (json_pointer, leaf_value) for every scalar leaf."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, "%s/%s" % (path, k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, "%s/%d" % (path, i))
    else:
        yield path, obj


def classify(pointer):
    """Return (category, rationale). Categories separate consumed-vs-metadata
    by field role in the WebArena config schema; this is a schema reading, not
    a runtime-scoring claim."""
    parts = [p for p in pointer.split("/") if p]
    # strip leading item index
    field = parts[1] if len(parts) > 1 else ""
    if field == "start_url":
        return "URL:start_url", "navigation starting URL"
    if "/eval/" in pointer:
        leaf = parts[-1]
        if leaf == "reference_url" or leaf.endswith("url"):
            return "URL:eval.reference_url", "answer-check reference URL"
        if leaf in ("url",):
            return "URL:eval.program_html.locator", "program-html target URL locator"
        if leaf in ("locator", "required_contents"):
            return "CONTENT:eval.program_html", "content assertion target/text"
        if leaf in ("must_include", "fuzzy_match", "exact_match", "string_note",
                    "reference_answer_raw_annotation", "reference_answers"):
            return "CONTENT:eval.answer", "human/answer text compared after render"
        return "OTHER:eval.%s" % leaf, "eval subfield, role unverified"
    return "METADATA:%s" % field, "config metadata not asserted as consumed"


def main():
    out = {"pins": {}, "profiles": {}, "checked": {}}
    bytes_ = {}
    for p, want in PINS.items():
        b, got = read_once(p)
        bytes_[p] = b
        out["pins"][os.path.relpath(p, ROOT)] = {
            "bytes": len(b), "sha256_observed": got, "sha256_pinned": want,
            "match": got == want,
        }
    if not all(v["match"] for v in out["pins"].values()):
        out["checked"]["status"] = "pin_mismatch"
        print(json.dumps(out, indent=2))
        return 2

    raw_bytes = bytes_[RAW]
    raw_text = raw_bytes.decode("utf-8")  # strict; surrogate/encoding error is fatal
    out["checked"]["raw_bytes"] = len(raw_bytes)
    out["checked"]["raw_unicode_codepoints"] = len(raw_text)
    out["checked"]["bytes_equal_codepoints"] = len(raw_bytes) == len(raw_text)

    original = json.loads(raw_text)
    out["checked"]["original_task_count"] = len(original)
    out["checked"]["original_distinct_task_ids"] = len({d["task_id"] for d in original})

    # --- raw occurrence census with codepoint provenance -------------------
    occ = {}
    for k in ORDER:
        tok = TOK[k]
        positions = []
        start = 0
        while True:
            i = raw_text.find(tok, start)
            if i < 0:
                break
            positions.append(i)
            start = i + len(tok)
        occ[k] = {"token": tok, "occurrences": len(positions),
                  "first_codepoint_offsets": positions[:3],
                  "last_codepoint_offset": positions[-1] if positions else None}
    out["raw_occurrences"] = occ
    out["raw_occurrence_total"] = sum(v["occurrences"] for v in occ.values())

    # overlap witness: does the SHOPPING token match inside SHOPPING_ADMIN text?
    out["checked"]["shopping_token_matches_admin_token_text"] = (
        TOK["SHOPPING"] in TOK["SHOPPING_ADMIN"])

    # which top-level field hosts each occurrence (post-parse, semantic)
    host = collections.Counter()
    for item in original:
        for ptr, val in leaves(item, ""):
            if isinstance(val, str):
                for k in ORDER:
                    n = val.count(TOK[k])
                    if n:
                        host[(ptr.split("/")[1], k)] += n
    out["token_host_fields"] = {"%s|%s" % k: v for k, v in sorted(host.items())}

    profiles = json.loads(bytes_[PROFILES].decode("utf-8"))
    orig_leaves = dict(leaves(original, ""))

    for pname in profiles:
        vals = profiles[pname]["values"]
        text = raw_text
        per_token = {}
        cascade = {}
        for k in ORDER:
            tok = TOK[k]
            before = text.count(tok)
            text = text.replace(tok, vals[k])
            after = text.count(tok)
            per_token[k] = {"occurrences_replaced": before,
                            "residual_after_own_pass": after}
            # cascade: did an earlier value introduce a later token?
            for later in ORDER:
                if later == k:
                    continue
                if TOK[later] in vals[k]:
                    cascade["%s->%s" % (k, later)] = True
        projected = json.loads(text)  # failure here is a finding, not a repair
        proj_leaves = {}
        shapes_ok = True
        for i, item in enumerate(projected):
            for ptr, val in leaves(item, "/%d" % i):
                proj_leaves[ptr] = val
        if set(proj_leaves) != set(orig_leaves):
            shapes_ok = False
        changed = []
        by_cat = collections.Counter()
        for ptr in orig_leaves:
            a, b = orig_leaves[ptr], proj_leaves.get(ptr)
            if isinstance(a, str) and a != b:
                cat, why = classify(ptr)
                by_cat[cat] += 1
                changed.append({"path": ptr, "category": cat,
                                "rationale": why, "old": a, "new": b})
        residual = {k: text.count(TOK[k]) for k in ORDER}
        # ordinal vs task_id
        idx_mismatch = [{"ordinal": i, "task_id": it.get("task_id"),
                         "filename": "%d.json" % i}
                        for i, it in enumerate(projected)
                        if it.get("task_id") != i]
        out["profiles"][pname] = {
            "purpose_declared": profiles[pname].get("purpose"),
            "per_token_occurrences": per_token,
            "cascade_hits": cascade,
            "projection_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "projection_bytes": len(text.encode("utf-8")),
            "projection_codepoints": len(text),
            "parsed_task_count": len(projected),
            "parsed_shape_identical_to_original": shapes_ok,
            "changed_leaf_count": len(changed),
            "changed_leaves_by_category": dict(by_cat),
            "changed_task_count": len({c["path"].split("/")[1] for c in changed}),
            "residual_known_tokens": residual,
            "ordinal_task_id_mismatches": idx_mismatch[:5],
            "ordinal_task_id_mismatch_count": len(idx_mismatch),
            "changed_leaves": changed,
            "changed_leaf_paths_unique": sorted({c["path"] for c in changed}),
        }

    # shuffled-ID witness: generator enumerates by position, not task_id
    shuffled = list(reversed(original))
    witness = [{"ordinal": i, "filename": "%d.json" % i,
                "task_id": it["task_id"]}
               for i, it in enumerate(shuffled[:3])]
    out["shuffled_witness"] = {
        "construction": "reversed(original) in memory only",
        "first_three": witness,
        "index_equals_task_id": all(w["ordinal"] == w["task_id"] for w in witness),
    }
    out["checked"]["status"] = "ok"
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

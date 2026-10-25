#!/usr/bin/env python3
"""Independent __REDDIT__ token census (round29 claim C1, seat R29TokenReddit-2).

Reads the pinned r28 raw JSON bytes ONCE (sha256 verified against the r29 manifest
pin), parses only those retained bytes, and performs an in-memory-only projection
under the three frozen synthetic profiles for length/span derivation.
No project imports, no network, no config_files output is written.
Stdlib only.

Provenance model: raw serialized JSON text is scanned for exact string-literal
spans; each literal is decoded and paired positionally with the decoded document
walk. Token offsets are reported as Unicode-codepoint offsets in the serialized
text AND as offsets inside the decoded leaf, with an explicit per-occurrence map.
"""
import hashlib
import json
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
RAW_PIN = "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"
PROFILES = LANE + "/plans/fixtures/r29/profiles.json"
PROFILES_PIN = "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOKENS = {t: "__%s__" % t for t in ORDER}
TOK = TOKENS["REDDIT"]
TOKLEN = len(TOK)

# ---- read pinned inputs exactly once; retain bytes, verify before parse ----
raw_bytes = open(RAW, "rb").read()
raw_sha = hashlib.sha256(raw_bytes).hexdigest()
assert raw_sha == RAW_PIN, "raw pin mismatch: %s" % raw_sha
prof_bytes = open(PROFILES, "rb").read()
prof_sha = hashlib.sha256(prof_bytes).hexdigest()
assert prof_sha == PROFILES_PIN, "profiles pin mismatch: %s" % prof_sha

text = raw_bytes.decode("utf-8")          # strict; failure raises
doc = json.loads(text)                   # parse only retained bytes
n_tasks = len(doc)
task_ids = [t.get("task_id") for t in doc]

# ---- string-literal scanner with decoded-offset -> raw-offset mapping ----
def scan_literals(s):
    out, i, n = [], 0, len(s)
    while i < n:
        if s[i] == '"':
            j = i + 1
            while j < n:
                if s[j] == "\\":
                    j += 2
                    continue
                if s[j] == '"':
                    break
                j += 1
            out.append((i, j + 1, s[i:j + 1]))   # [quote .. quote+1)
            i = j + 1
        else:
            i += 1
    return out

def decoded_index_map(inner):
    """For each decoded char index, the raw index within the literal body."""
    mapping, ri = [], 0
    while ri < len(inner):
        mapping.append(ri)
        if inner[ri] == "\\":
            if ri + 1 < len(inner) and inner[ri + 1] == "u":
                ri += 6
            else:
                ri += 2
        else:
            ri += 1
    return mapping

lits = scan_literals(text)
decoded_lits = [json.loads(lit) for _, _, lit in lits]

# decoded document walk in serialization order: dict key string, then value
walked = []
def walk(node, path, root_index):
    if isinstance(node, dict):
        for k, v in node.items():
            walked.append(("key", root_index, path + [k], k))
            walk(v, path + [k], root_index)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + ["[%d]" % i], root_index)
    elif isinstance(node, str):
        walked.append(("value", root_index, path, node))

for idx, item in enumerate(doc):
    walk(item, ["[%d]" % idx], idx)

assert len(walked) == len(lits), (len(walked), len(lits))
lit_pair_mismatch = []
for i, ((kind, root, path, val), dec) in enumerate(zip(walked, decoded_lits)):
    if kind == "key":
        if val != dec:
            lit_pair_mismatch.append({"i": i, "kind": kind, "path": path})
        continue
    if val != dec:
        lit_pair_mismatch.append({"i": i, "kind": kind, "path": ".".join(path)})

# per-literal decoded->raw map (computed once per literal)
maps = [decoded_index_map(lit[1:-1]) for _, _, lit in lits]
assert all(len(m) == len(d) for m, d in zip(maps, decoded_lits)), "offset map mismatch"

# ---- raw serialized census for every token (order/overlap context) ----
def find_all(hay, needle):
    out, i = [], hay.find(needle)
    while i != -1:
        out.append(i)
        i = hay.find(needle, i + 1)
    return out

raw_counts = {t: text.count(TOKENS[t]) for t in ORDER}
raw_offsets = {t: find_all(text, TOKENS[t]) for t in ORDER}
reddit_spans = [(o, o + TOKLEN) for o in raw_offsets["REDDIT"]]
overlaps = []
for t in ORDER:
    if t == "REDDIT":
        continue
    for o in raw_offsets[t]:
        s, e = o, o + len(TOKENS[t])
        for rs, re_ in reddit_spans:
            if s < re_ and rs < e:
                overlaps.append({"token": t, "offset": o, "reddit_span": [rs, re_]})

# ---- escape census ----
esc = {}
for m in re.finditer(r"\\u([0-9a-fA-F]{4})", text):
    ch = chr(int(m.group(1), 16))
    esc[ch] = esc.get(ch, 0) + 1

# ---- occurrence table: exact literal span, path, task, field ----
occ = []
for li, (kind, root, path, val) in enumerate(walked):
    if kind != "value" or TOK not in val:
        continue
    start, end, lit = lits[li]
    inner = lit[1:-1]
    m = maps[li]
    for off in find_all(val, TOK):
        raw_off = start + 1 + m[off]
        assert text[raw_off:raw_off + TOKLEN] == TOK, (li, off, raw_off)
        occ.append({
            "raw_offset_codepoint": raw_off,
            "raw_offset_byte": len(text[:raw_off].encode("utf-8")),
            "decoded_leaf_offset": off,
            "decoded_to_raw_skew": raw_off - (start + 1 + off),
            "literal_span": [start, end],
            "root_index": root,
            "task_id": doc[root].get("task_id"),
            "kind": kind,
            "path": ".".join(path),
            "leaf_key": path[-1] if path else "",
            "leaf": val,
        })

# ---- classification ----
URL_FIELD_KEYS = {"url", "start_url", "reference_url"}
def classify(o):
    leaf, off = o["leaf"], o["decoded_leaf_offset"]
    end = off + TOKLEN
    in_scheme = any(m.start() <= off and end <= m.end()
                    for m in re.finditer(r"[A-Za-z][A-Za-z0-9+.\-]*://[^\s\"'<>]*", leaf))
    whole_leaf = leaf == TOK
    followed_by_path = end < len(leaf) and leaf[end] in "/?#"
    preceded_by_scheme = leaf[max(0, off - 3):off] == "://"
    key = o["leaf_key"]
    field_url_typed = key in URL_FIELD_KEYS or key.lower().endswith("_url")
    url_shaped = in_scheme or whole_leaf or followed_by_path or preceded_by_scheme
    if field_url_typed:
        cat = "A_url_typed_field"
    elif url_shaped:
        cat = "B_non_url_field_url_shaped"
    else:
        cat = "C_non_url_plain"
    return {
        "field_url_typed": field_url_typed, "url_shaped": url_shaped,
        "whole_leaf": whole_leaf, "followed_by_path_sep": followed_by_path,
        "in_scheme_lexeme": in_scheme, "category": cat,
    }

for o in occ:
    o.update(classify(o))

# groups by path / by field key / by category, per task
by_path = {}
for o in occ:
    g = by_path.setdefault(o["path"], {"path": o["path"], "count": 0, "roots": [],
                                       "category": o["category"], "leaf_key": o["leaf_key"],
                                       "samples": []})
    g["count"] += 1
    if o["root_index"] not in g["roots"]:
        g["roots"].append(o["root_index"])
    if len(g["samples"]) < 3:
        s = o["decoded_leaf_offset"]
        g["samples"].append(o["leaf"][max(0, s - 45): s + 60])
by_path_list = sorted(by_path.values(), key=lambda g: (-g["count"], g["path"]))

by_key = {}
for o in occ:
    k = by_key.setdefault(o["leaf_key"], {"leaf_key": o["leaf_key"], "count": 0,
                                          "paths": set(), "tasks": set()})
    k["count"] += 1
    k["paths"].add(o["path"])
    k["tasks"].add(o["root_index"])
by_key_list = []
for k in by_key.values():
    by_key_list.append({"leaf_key": k["leaf_key"], "count": k["count"],
                        "distinct_paths": len(k["paths"]),
                        "distinct_tasks": len(k["tasks"])})
by_key_list.sort(key=lambda k: -k["count"])

by_cat = {}
for o in occ:
    by_cat[o["category"]] = by_cat.get(o["category"], 0) + 1

per_task = {}
for o in occ:
    t = per_task.setdefault(o["root_index"], {"root_index": o["root_index"],
                                              "task_id": o["task_id"], "count": 0,
                                              "paths": []})
    t["count"] += 1
    t["paths"].append(o["path"])
per_task_list = [per_task[k] for k in sorted(per_task)]

# ---- per-profile in-memory projection ----
profiles = json.loads(prof_bytes.decode("utf-8"))
profile_results = {}
for pname, pbody in profiles.items():
    values = pbody["values"]
    assert set(values) == set(ORDER)
    cascade = {t: [u for u in ORDER if TOKENS[u] in values[t]] for t in ORDER}
    # JSON-safety of each substituted value
    unsafe = {}
    for t in ORDER:
        enc = json.dumps(values[t])[1:-1]
        if '"' in enc or "\\" in enc:
            unsafe[t] = enc
    post_gitlab = text.replace(TOKENS["GITLAB"], values["GITLAB"])
    gitlab_value_len = len(values["GITLAB"])
    gitlab_delta = gitlab_value_len - len(TOKENS["GITLAB"])
    gitlab_offsets = raw_offsets["GITLAB"]
    spans_pg = find_all(post_gitlab, TOK)
    assert len(spans_pg) == len(occ)
    reddit_value = values["REDDIT"]
    delta = len(reddit_value) - TOKLEN
    # observed shift in the text REDDIT actually acts on, vs original offsets
    shift_checks = []
    for o, s_pg in zip(occ, spans_pg):
        expected = sum(1 for g in gitlab_offsets if g < o["raw_offset_codepoint"]) * gitlab_delta
        shift_checks.append({
            "orig": o["raw_offset_codepoint"], "post_gitlab": s_pg,
            "observed_shift": s_pg - o["raw_offset_codepoint"],
            "expected_gitlab_shift": expected,
            "match": (s_pg - o["raw_offset_codepoint"]) == expected,
        })
    final_starts = [s + j * delta for j, s in enumerate(spans_pg)]
    post_reddit = post_gitlab.replace(TOK, reddit_value)
    span_ok = all(post_reddit[s:s + len(reddit_value)] == reddit_value for s in final_starts)
    value_occ = post_reddit.count(reddit_value)
    cur = post_reddit
    for t in ORDER[2:]:
        cur = cur.replace(TOKENS[t], values[t])
    proj_doc = json.loads(cur)
    leftover = {t: cur.count(TOKENS[t]) for t in ORDER}
    # leaf-level length impact distribution
    leaf_deltas = {}
    for o in occ:
        leaf_deltas[o["path"]] = leaf_deltas.get(o["path"], 0) + delta
    profile_results[pname] = {
        "purpose": pbody["purpose"],
        "reddit_value": reddit_value,
        "reddit_value_codepoints": len(reddit_value),
        "delta_per_occurrence": delta,
        "gitlab_value": values["GITLAB"],
        "gitlab_value_codepoints": gitlab_value_len,
        "gitlab_count": raw_counts["GITLAB"],
        "gitlab_delta_per_occurrence": gitlab_delta,
        "reddit_spans_post_gitlab_codepoints": [[s, s + TOKLEN] for s in spans_pg],
        "shift_checks_all_match": all(c["match"] for c in shift_checks),
        "shift_checks_sample": shift_checks[:5],
        "reddit_final_starts_codepoints": final_starts,
        "replacement_spans_verified": span_ok,
        "reddit_value_occurrences_in_post_reddit_text": value_occ,
        "total_text_delta_from_reddit": len(occ) * delta,
        "final_text_codepoints": len(cur),
        "final_text_bytes": len(cur.encode("utf-8")),
        "parsed_tasks": len(proj_doc),
        "distinct_task_ids": len({t.get("task_id") for t in proj_doc}),
        "index_equals_task_id_all": all(i == t.get("task_id") for i, t in enumerate(proj_doc)),
        "leftover_token_counts": leftover,
        "cascade_token_in_value": cascade,
        "json_unsafe_values": unsafe,
        "task_profile_projections": len(proj_doc),
    }

report = {
    "scope": "single token __REDDIT__; round29 frozen inputs; read-only census",
    "inputs": {
        "raw_path": RAW, "raw_sha256": raw_sha, "raw_bytes": len(raw_bytes),
        "raw_codepoints": len(text),
        "non_ascii_codepoints": sum(1 for c in text if ord(c) > 127),
        "profiles_sha256": prof_sha,
        "parsed_top_level_items": n_tasks,
        "distinct_task_ids": len(set(task_ids)),
        "index_equals_task_id_all": all(i == tid for i, tid in enumerate(task_ids)),
    },
    "raw_serialized_counts_all_tokens": raw_counts,
    "raw_token_lengths": {t: len(TOKENS[t]) for t in ORDER},
    "raw_occurrence_offsets_codepoints": {
        "REDDIT": raw_offsets["REDDIT"], "GITLAB": raw_offsets["GITLAB"]},
    "reddit_overlapping_other_token_occurrences": overlaps,
    "raw_escape_census": {
        "backslash_u_escapes_total": sum(esc.values()),
        "decoded_chars_histogram": {repr(k): v for k, v in sorted(esc.items())},
        "backslash_slash_escapes": text.count("\\/"),
        "escapes_decoding_to_token_chars": {repr(ch): esc.get(ch, 0) for ch in "_REDDIT"},
    },
    "literal_pairing": {
        "string_literals": len(lits), "walked_strings": len(walked),
        "decoded_pair_mismatches": lit_pair_mismatch,
        "all_decoded_pairings_equal": not lit_pair_mismatch,
    },
    "decoded_counts": {
        "occurrences_in_string_values": sum(1 for o in occ if o["kind"] == "value"),
        "occurrences_in_string_keys": sum(1 for o in occ if o["kind"] == "key"),
        "decoded_total": len(occ),
        "raw_literal_count": raw_counts["REDDIT"],
        "equals_raw_literal_count": len(occ) == raw_counts["REDDIT"],
        "escape_split_occurrences": 0 if len(occ) == raw_counts["REDDIT"] else None,
    },
    "distinct_leaves_with_occurrence": len({(o["path"], o["root_index"]) for o in occ}),
    "distinct_tasks_with_occurrence": len({o["root_index"] for o in occ}),
    "task_ids_with_occurrence": sorted({o["task_id"] for o in occ}),
    "category_counts": by_cat,
    "by_leaf_key": by_key_list,
    "by_path": by_path_list,
    "per_task": per_task_list,
    "occurrences": occ,
    "profiles": profile_results,
    "expected_vs_observed": {
        "spec_expected_812x3": 812 * 3,
        "observed_tasks": n_tasks, "observed_profiles": len(profiles),
        "observed_product": n_tasks * len(profiles),
    },
}

out_path = (LANE + "/.ufo/waves/round-29/scratch/"
            "KengakuR28.R29TokenReddit-2/reddit-census.json")
json.dump(report, open(out_path, "w"), indent=2, default=str)

# ---- concise stdout ----
print("raw sha", raw_sha, "bytes", len(raw_bytes), "codepoints", len(text),
      "non_ascii", report["inputs"]["non_ascii_codepoints"])
print("tasks", n_tasks, "distinct", report["inputs"]["distinct_task_ids"],
      "index==task_id", report["inputs"]["index_equals_task_id_all"])
print("counts", raw_counts)
print("REDDIT raw count", raw_counts["REDDIT"], "decoded", len(occ),
      "keys", report["decoded_counts"]["occurrences_in_string_keys"],
      "leaves", report["distinct_leaves_with_occurrence"],
      "tasks", report["distinct_tasks_with_occurrence"])
print("literal pairing all equal", report["literal_pairing"]["all_decoded_pairings_equal"],
      "literals", len(lits))
print("escapes", report["raw_escape_census"])
print("categories", by_cat)
print("by key", by_key_list)
print("skew nonzero occurrences",
      sum(1 for o in occ if o["decoded_to_raw_skew"] != 0),
      "max skew", max((o["decoded_to_raw_skew"] for o in occ), default=0))
for pname, r in profile_results.items():
    print("PROFILE %-28s value=%-34s len=%2d delta/occ=%2d total=%5d final_cp=%d parsed=%d ids=%d leftover=%s spans_ok=%s shift_ok=%s"
          % (pname, r["reddit_value"], r["reddit_value_codepoints"],
             r["delta_per_occurrence"], r["total_text_delta_from_reddit"],
             r["final_text_codepoints"], r["parsed_tasks"], r["distinct_task_ids"],
             r["leftover_token_counts"], r["replacement_spans_verified"],
             r["shift_checks_all_match"]))
print("spec expected", 812 * 3, "observed", n_tasks * len(profiles))
print("FIRST/LAST occurrence",
      {k: occ[0][k] for k in ("raw_offset_codepoint", "path", "task_id", "category")},
      {k: occ[-1][k] for k in ("raw_offset_codepoint", "path", "task_id", "category")})

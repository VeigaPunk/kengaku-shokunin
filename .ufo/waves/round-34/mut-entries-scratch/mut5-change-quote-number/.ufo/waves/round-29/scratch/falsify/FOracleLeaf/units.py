#!/usr/bin/env python3
"""FOracleLeaf-2 retained evidence: unit discrimination + H2 divergence detail
+ programmatic quote word-count. Imports the sibling oracle.py (own module,
never plans/config_projection.py)."""
import collections
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oracle as O  # noqa: E402

raw_bytes, man, pins, pf = O.load_pinned_inputs()
raw = raw_bytes.decode()
doc = json.loads(raw)

vals_h2 = {"GITLAB": "http://gitlab.invalid:10101", "REDDIT": "http://reddit.invalid:10102\\nfast",
           "SHOPPING": "s", "SHOPPING_ADMIN": "sa", "WIKIPEDIA": "w", "MAP": "m"}
mini = '{"task_id": 1, "start_url": "__REDDIT__"}'
leaf_doc = O.leaf_project(json.loads(mini), vals_h2)
_, text_doc = O.text_project(mini, vals_h2)
lv, tv = leaf_doc["start_url"], text_doc["start_url"]
k = next(i for i, (a, b) in enumerate(zip(lv, tv)) if a != b)
lines = [
    f"H2 first divergence at codepoint index {k} of start_url value: leaf U+{ord(lv[k]):04X} text U+{ord(tv[k]):04X}",
    f"H2 leaf value repr {lv!r} len {len(lv)} | text value repr {tv!r} len {len(tv)}",
    "H2 would-be file sha256 leaf : " + hashlib.sha256(json.dumps(leaf_doc, indent=2).encode()).hexdigest(),
    "H2 would-be file sha256 text : " + hashlib.sha256(json.dumps(text_doc, indent=2).encode()).hexdigest(),
]

per_tok_leaves = collections.Counter()
multi_occ = multi_distinct = 0
for item in doc:
    for _ptr, s, is_key in O.walk_strings_decoded(item):
        if is_key:
            continue
        toks, n, start = set(), 0, 0
        while True:
            j = s.find("__", start)
            if j < 0:
                break
            m = O._LEAF_RE.match(s, j)
            if m:
                toks.add(m.group(0))
                n += 1
                start = m.end()
            else:
                start = j + 2
        for t in toks:
            per_tok_leaves[t] += 1
        multi_occ += n >= 2
        multi_distinct += len(toks) >= 2
lines.append("per-token changed leaves (mine): " + json.dumps(dict(sorted(per_tok_leaves.items()))))
lines.append(f"leaves with >=2 token occurrences: {multi_occ} | leaves with >=2 distinct tokens: {multi_distinct}")
lines.append(f"total token occurrences (leaves, counting repeats): {sum(raw.count(t) for t in O.TOKENS)} (raw text)")
lines.append(f"changed leaves total (distinct leaf slots): {sum(per_tok_leaves.values())}")

quote = ("SELFTEST clean cases=20 six_tokens_and_non_url_field,units_not_pooled,"
         "codepoint_offsets_and_key_token,escaped_token_not_replaced,"
         "quote_backslash_decode_failure_and_escape_semantics,profile_map_errors,"
         "hand_cascade_order_R29_ORDER_CASCADE_01,hand_url_only_R29-URL-ONLY-UNREAD-METADATA-01,"
         "hand_index_r29_index_shuffled_ids_1_0,source_order_swap,source_literal_rhs,"
         "source_extra_step,source_id_filename,cli_snapshot_tampered,cli_input_missing,"
         "cli_coherent_rebinding,post_read_replacement_test.raw.json,"
         "post_read_replacement_generate_test_data.py,post_read_replacement_profiles.json,"
         "cli_manifest_tampered")
lines.append(f"selftest quote word count (whitespace-split): {len(quote.split())}")
lines.append(f"python: {sys.version.split()[0]}")
out = "\n".join(lines)
(HERE / "units.out").write_text(out + "\n")
print(out)

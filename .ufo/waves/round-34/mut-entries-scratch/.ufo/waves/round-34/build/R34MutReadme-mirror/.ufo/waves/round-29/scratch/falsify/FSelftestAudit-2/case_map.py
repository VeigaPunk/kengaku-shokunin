#!/usr/bin/env python3
"""Produce the 20-case -> assertion map with exact HEAD line numbers."""
import re
from pathlib import Path
HEAD = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FSelftestAudit-2/head/config_projection.py")
lines = HEAD.read_text().splitlines()

# Locate the selftest function body
start = next(i for i, l in enumerate(lines) if l.startswith("def selftest("))
end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("def "))
body = lines[start:end]

# Walk the body, collecting assert statements grouped by the case they precede.
cur = []
groups = []
for i, l in enumerate(body):
    s = l.strip()
    if s.startswith("assert ") or s.startswith("assert("):
        cur.append((start + i + 1, s))
    m = re.search(r'cases\.append\((.*)\)', s)
    if m:
        groups.append((m.group(1), cur[:]))
        cur = []

print("HEAD file: plans/config_projection.py @ 56fd949a  (548 lines, sha256 5673405e...)")
print("selftest def at line %d" % (start + 1))
print()
order = [
 "six_tokens_and_non_url_field", "units_not_pooled", "codepoint_offsets_and_key_token",
 "escaped_token_not_replaced", "quote_backslash_decode_failure_and_escape_semantics",
 "profile_map_errors", "hand_cascade_order_R29_ORDER_CASCADE_01",
 "hand_url_only_R29-URL-ONLY-UNREAD-METADATA-01", "hand_index_r29_index_shuffled_ids_1_0",
 "source_order_swap", "source_literal_rhs", "source_extra_step", "source_id_filename",
 "cli_snapshot_tampered", "cli_input_missing", "cli_coherent_rebinding",
 "post_read_replacement_test.raw.json", "post_read_replacement_generate_test_data.py",
 "post_read_replacement_profiles.json", "cli_manifest_tampered",
]
for expr, asserts in groups:
    label = expr
    for o in order:
        if o in expr:
            label = o
            break
    print("CASE %-52s" % label)
    for ln, a in asserts:
        print("    L%-4d %s" % (ln, a[:150]))
    if not asserts:
        print("    (no inline assert; assertion inside helper)")
    print()

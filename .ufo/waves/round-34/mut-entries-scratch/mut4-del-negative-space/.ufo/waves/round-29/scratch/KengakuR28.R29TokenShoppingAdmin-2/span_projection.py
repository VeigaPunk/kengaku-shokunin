#!/usr/bin/env python3
"""Own-token-only span projection for __SHOPPING_ADMIN__ across the 3 frozen profiles.

Read-only. No production imports. Prints a table plus per-occurrence offset
prediction checks. Does NOT claim full six-token projection validity.
"""
import json
import re

RAW = "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = "plans/fixtures/r29/profiles.json"
TOK = "__SHOPPING_ADMIN__"

text = open(RAW, "rb").read().decode("utf-8")
profiles = json.load(open(PROFILES))
data = json.loads(text)
occ = [m.start() for m in re.finditer(re.escape(TOK), text)]

print(f"token={TOK} len={len(TOK)} raw_occurrences={len(occ)}")
print(f"raw_codepoints={len(text)} raw_bytes={len(text.encode())} non_ascii={sum(ord(c)>127 for c in text)}")
for name in profiles:
    val = profiles[name]["values"]["SHOPPING_ADMIN"]
    proj = text.replace(TOK, val)
    cum = 0
    ok = 0
    for o in occ:
        if proj.find(val, o + cum) == o + cum:
            ok += 1
        cum += len(val) - len(TOK)
    d = json.loads(proj)
    dbl = sum(1 for o in occ if text[o + 18:o + 19] == "/" and val.endswith("/"))
    print(
        f"profile={name} repl_len={len(val)} delta={len(val)-len(TOK)} "
        f"total_own_delta={len(occ)*(len(val)-len(TOK))} projected_len={len(proj)} "
        f"offset_predictions={ok}/{len(occ)} parses_tasks={len(d)} "
        f"token_remaining={proj.count(TOK)} repl_occurrences={proj.count(val)} "
        f"double_slash_after_authority={dbl}"
    )
print("distinct_leaf_values=" + str(len({v for v in re.findall(r'"[^"]*' + re.escape(TOK) + r'[^"]*"', text)})))

#!/usr/bin/env python3
"""Corrected independent check of url-only expected_mutant (same path notation)."""
import json
from pathlib import Path
HAND = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/hand")
ORDER = ("GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP")
u = json.loads((HAND/"url-only.fixture.json").read_text())
ue = json.loads((HAND/"url-only.expected.json").read_text())

orig = json.loads(u["raw_text"])
mut = json.loads(u["raw_text"])
def url_only(node, path=()):
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if k in ("start_url","reference_url","url") and isinstance(v,str):
                for n in ORDER: v = v.replace("__%s__"%n, u["values"][n])
                node[k] = v
            elif isinstance(v,(dict,list)): url_only(v, path+(k,))
    elif isinstance(node,list):
        for i,v in enumerate(node): url_only(v, path+(i,))
url_only(mut)

def leaves(o, p=()):
    out={}
    if isinstance(o,dict):
        for k,v in o.items(): out.update(leaves(v,p+(k,)))
    elif isinstance(o,list):
        for i,v in enumerate(o): out.update(leaves(v,p+(i,)))
    elif isinstance(o,str): out[p]=o
    return out
def fmt(p): return "$[" + str(p[0]) + "]" + "".join("."+str(x) for x in p[1:])

a = leaves(orig); b = leaves(mut)
changed = sorted(fmt(p) for p in a if a[p]!=b[p])
print("derived url-only mutant changed leaf paths:", changed)
print("fixture expected_mutant.changed_string_leaf_paths:", ue["expected_mutant"]["changed_string_leaf_paths"])
print("MATCH:", changed == sorted(ue["expected_mutant"]["changed_string_leaf_paths"]))
rem = sum(v.count("__%s__"%n) for v in b.values() for n in ORDER)
print("derived remaining token occurrences:", rem, "fixture:", ue["expected_mutant"]["remaining_known_environment_token_occurrences"], "MATCH:", rem==ue["expected_mutant"]["remaining_known_environment_token_occurrences"])
print("fixture expected_mutant.mismatch_paths:", ue["expected_mutant"]["mismatch_paths"])
print("fixture expected_mutant.detector_exit:", ue["expected_mutant"]["detector_exit"])
print()
print("=> expected_mutant is CORRECT but the selftest never references it:")
sel = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FSelftestAudit-2/head/config_projection.py").read_text()
print("   'expected_mutant' in selftest source:", "expected_mutant" in sel)

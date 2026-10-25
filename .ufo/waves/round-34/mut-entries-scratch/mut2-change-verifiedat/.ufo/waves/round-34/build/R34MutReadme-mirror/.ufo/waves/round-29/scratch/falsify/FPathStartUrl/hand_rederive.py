#!/usr/bin/env python3
"""Hand re-derivation: five changed start_url leaves per profile from raw task slices."""
import json
import sys

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FPathStartUrl")
import oracle_v2 as O

SAMPLE = [0, 7, 27, 44, 431]
raw = open(O.RAW, encoding="utf-8").read()
prof = json.load(open(O.PROF, encoding="utf-8"))
inst = json.load(open(O.SCRATCH + "/projection.json", encoding="utf-8"))
base = json.loads(raw)
dec = json.JSONDecoder()
slices = []
i = raw.index("[") + 1
for _ in range(len(base)):
    while raw[i] in " \n\r\t,":
        i += 1
    obj, end = dec.raw_decode(raw, i)
    slices.append((i, end))
    i = end

bad = 0
for pname, pobj in prof.items():
    vals = pobj["values"]
    names = {t: t.strip("_") for t in O.ORDER}
    ip = inst["profiles"][pname]
    print("## PROFILE", pname)
    for idx in SAMPLE:
        a, b = slices[idx]
        chunk = raw[a:b]
        hand = chunk
        counts = {}
        for tok in O.ORDER:
            counts[tok] = hand.count(tok)
            hand = hand.replace(tok, vals[names[tok]])
        obj = json.loads(hand)
        rec = ip["tasks"][idx]
        entries = [cl for cl in rec["changed_leaves"] if cl["path_template"] == "start_url"]
        cl = entries[0]
        checks = {
            "one_entry": len(entries) == 1,
            "orig_eq_raw": cl["original"] == base[idx]["start_url"],
            "hand_eq_proj": obj["start_url"] == cl["projected"],
            "proj_task_eq": rec["projected_task"]["start_url"] == obj["start_url"],
            "category_url": cl["category"] == "url_field",
            "index_eq": rec["output_index"] == idx and rec["task_id"] == base[idx]["task_id"],
            "filename": rec["output_filename"] == f"config_files/{idx}.json",
        }
        ok = all(checks.values())
        if not ok:
            bad += 1
        print(f" idx={idx} tokens_in_task_slice="
              f"{ {k: v for k, v in counts.items() if v} } "
              f"orig_len={len(cl['original'])} proj_len={len(cl['projected'])} ok={ok}")
        print("   ORIG:", cl["original"] if len(cl["original"]) < 120 else cl["original"][:117] + "...")
        print("   PROJ:", cl["projected"] if len(cl["projected"]) < 120 else cl["projected"][:117] + "...")
        print("   checks:", checks)
print("HAND_SAMPLE_FAILURES", bad, "of", len(SAMPLE) * len(prof))

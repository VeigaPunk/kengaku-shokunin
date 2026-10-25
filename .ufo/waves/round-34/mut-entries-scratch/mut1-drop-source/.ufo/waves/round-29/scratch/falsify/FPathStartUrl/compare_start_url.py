#!/usr/bin/env python3
"""Compare instrument --json against oracle v2 census, focused on start_url.

Reads instrument OUTPUT only (scratch/projection.json), never production source.
"""
import json
import sys

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FPathStartUrl")
import oracle_v2 as O  # independent oracle authored in scratch

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
SCRATCH = ROOT + "/.ufo/waves/round-29/scratch/falsify/FPathStartUrl"
ORDER = O.ORDER
URL_TEMPLATES = O.URL_TEMPLATES


def main():
    raw = open(O.RAW, "r", encoding="utf-8").read()
    profiles = json.load(open(O.PROF, encoding="utf-8"))
    inst = json.load(open(SCRATCH + "/projection.json", encoding="utf-8"))
    base = json.loads(raw)
    base_leaves = O.walk_doc(base)
    base_map = {p: (t, v) for t, p, v in base_leaves}
    mismatches = []

    def note(tag, detail):
        mismatches.append((tag, detail))

    # ---- 0. raw occurrence total vs leaf-walk occurrence total
    leaf_occ = {t: 0 for t in ORDER}
    for _, _, v in base_leaves:
        if isinstance(v, str):
            for t in ORDER:
                leaf_occ[t] += v.count(t)
    print("leaf_walk_occurrences", leaf_occ, "sum", sum(leaf_occ.values()))
    print("instrument_original_occurrences", inst["population"]["original_occurrences_by_token"])

    # ---- 1. occurrence provenance: every entry points at its token in raw text
    prov = inst["occurrence_provenance"]
    print("provenance_entries", len(prov))
    prov_bad = 0
    prov_su = 0
    prov_su_by_tok = {}
    for rec in prov:
        off = rec["original_input_codepoint_offset"]
        tok = rec["token"]
        if raw[off:off + len(tok)] != tok:
            prov_bad += 1
            if prov_bad < 6:
                print("  BAD OFFSET", rec, repr(raw[off - 5:off + len(tok) + 5]))
        if rec["path_template"] == "start_url":
            prov_su += 1
            prov_su_by_tok[tok] = prov_su_by_tok.get(tok, 0) + 1
            ptr = rec["json_pointer"]
            idx = int(ptr.split("/")[1])
            # token occurrence must really sit inside that task's start_url raw leaf
            # check via the projected mapping: locate raw task slice boundaries
    print("provenance_offsets_not_matching_token", prov_bad)
    print("provenance_start_url_entries", prov_su, "by_token", prov_su_by_tok)

    # task slice boundaries in raw text (top-level JSON array elements)
    dec = json.JSONDecoder()
    slices = []
    i = raw.index("[") + 1
    for _ in range(len(base)):
        while raw[i] in " \n\r\t,":
            i += 1
        obj, end = dec.raw_decode(raw, i)
        slices.append((i, end))
        i = end
    print("task_slices", len(slices))

    # ---- 2. per-profile compare
    for pname, pobj in profiles.items():
        vals = pobj["values"]
        text = raw
        for tok in ORDER:
            text = text.replace(tok, vals[tok.strip("_")])
        proj = json.loads(text)
        proj_leaves = O.walk_doc(proj)
        proj_map = {p: (t, v) for t, p, v in proj_leaves}
        changed = []
        for ptr, (tpl, v0) in base_map.items():
            if v0 != proj_map[ptr][1]:
                changed.append((tpl, ptr, v0, proj_map[ptr][1]))
        oracle = {ptr: (tpl, v0, v1) for tpl, ptr, v0, v1 in changed}
        print("\n=== PROFILE", pname)
        print(" oracle changed_leaf_count", len(oracle))

        ip = inst["profiles"][pname]
        # summary cross-check
        checks = [
            ("changed_leaf_count", ip["changed_leaf_count"], len(oracle)),
            ("changed_task_count", ip["changed_task_count"],
             len({p.split('/')[1] for p in oracle})),
            ("parsed_task_count", ip["parsed_task_count"], len(proj)),
            ("string_leaf_count", ip["string_leaf_count"],
             sum(1 for _, _, v in proj_leaves if isinstance(v, str))),
            ("projected_text_sha256", ip["projected_text_sha256"],
             O.hashlib.sha256(text.encode()).hexdigest()),
        ]
        o_tpl = O.Counter(t for t, _, _ in oracle.values())
        for tpl, n in o_tpl.items():
            checks.append(("tpl:" + tpl, ip["changed_leaves_by_path_template"].get(tpl), n))
        checks.append(("tpl:extra_keys", sorted(set(ip["changed_leaves_by_path_template"]) - set(o_tpl)), []))
        o_cat = O.Counter("url_field" if t in URL_TEMPLATES else "non_url_field"
                          for t, _, _ in oracle.values())
        for c, n in o_cat.items():
            checks.append(("cat:" + c, ip["changed_leaves_by_category"].get(c), n))
        checks.append(("cat:extra_keys",
                       sorted(set(ip["changed_leaves_by_category"]) - set(o_cat)), []))
        # multi-occurrence: leaves whose original side carries >1 token occurrence
        o_multi = sum(1 for tpl, v0, v1 in oracle.values()
                      if sum(v0.count(tok) for tok in ORDER) > 1)
        checks.append(("multi_occ", ip["changed_leaves_with_multiple_occurrences"], o_multi))
        for tag, got, want in checks:
            if got != want:
                note("summary:" + pname + ":" + tag, {"instrument": got, "oracle": want})
                print("  MISMATCH", tag, "instrument", got, "oracle", want)

        # per-task changed_leaves
        inst_leaves = {}
        task_dups = 0
        for t in ip["tasks"]:
            for cl in t["changed_leaves"]:
                ptr = cl["json_pointer"]
                if ptr in inst_leaves:
                    task_dups += 1
                inst_leaves[ptr] = cl
        print(" instrument per-task leaf entries", len(inst_leaves),
              "duplicate pointers", task_dups)
        only_inst = set(inst_leaves) - set(oracle)
        only_orac = set(oracle) - set(inst_leaves)
        print(" only_instrument", len(only_inst), "only_oracle", len(only_orac))
        if only_inst:
            print("  sample only_instrument", sorted(only_inst)[:5])
            note("only_instrument:" + pname, sorted(only_inst)[:10])
        if only_orac:
            print("  sample only_oracle", sorted(only_orac)[:5])
            note("only_oracle:" + pname, sorted(only_orac)[:10])
        value_bad = 0
        tpl_bad = 0
        cat_bad = 0
        tok_bad = 0
        su_values = []
        for ptr, (tpl, v0, v1) in oracle.items():
            cl = inst_leaves.get(ptr)
            if cl is None:
                continue
            if cl.get("original") != v0 or cl.get("projected") != v1:
                value_bad += 1
                if value_bad < 4:
                    print("  VALUE BAD", ptr, cl, "oracle", repr(v0), repr(v1))
            if cl.get("path_template") != tpl:
                tpl_bad += 1
                if tpl_bad < 4:
                    print("  TPL BAD", ptr, cl.get("path_template"), tpl)
            want_cat = "url_field" if tpl in URL_TEMPLATES else "non_url_field"
            if cl.get("category") != want_cat:
                cat_bad += 1
                if cat_bad < 4:
                    print("  CAT BAD", ptr, cl.get("category"), "want", want_cat)
            want_toks = [t for t in ORDER if t in v0]
            if sorted(cl.get("tokens", [])) != sorted(want_toks):
                tok_bad += 1
                if tok_bad < 4:
                    print("  TOKENS BAD", ptr, cl.get("tokens"), want_toks)
            if tpl == "start_url":
                su_values.append((ptr, v0, v1, cl))
        print(" value_bad", value_bad, "tpl_bad", tpl_bad, "cat_bad", cat_bad,
              "tokens_bad", tok_bad, "start_url_entries", len(su_values))
        for tag, n in (("value", value_bad), ("tpl", tpl_bad), ("cat", cat_bad),
                       ("tokens", tok_bad)):
            if n:
                note(tag + ":" + pname, n)

        # start_url-specific: every changed start_url leaf present, category url_field
        su_oracle = {p: (a, b) for p, (t, a, b) in oracle.items() if t == "start_url"}
        su_inst = {p: cl for p, cl in inst_leaves.items() if cl["path_template"] == "start_url"}
        print(" start_url oracle", len(su_oracle), "instrument", len(su_inst))
        if set(su_oracle) != set(su_inst):
            note("su_ptr:" + pname, {"only_inst": sorted(set(su_inst) - set(su_oracle))[:5],
                                     "only_oracle": sorted(set(su_oracle) - set(su_inst))[:5]})
        su_cat = O.Counter(cl["category"] for cl in su_inst.values())
        print(" start_url categories in instrument", dict(su_cat))
        if set(su_cat) != {"url_field"}:
            note("su_cat:" + pname, dict(su_cat))

        # tokens on start_url
        su_tok = O.Counter()
        for cl in su_inst.values():
            for t in cl.get("tokens", []):
                su_tok[t] += 1
        print(" instrument start_url leaf token attribution", dict(su_tok))
        o_su_tok = O.Counter(t for p, (tpl, v0, v1) in oracle.items() if tpl == "start_url"
                             for t in ORDER if t in v0)
        if O.Counter(dict(su_tok)) != o_su_tok:
            note("su_tok:" + pname, {"instrument": dict(su_tok), "oracle": dict(o_su_tok)})

        # profile-invariance of start_url leaf identities
        # ---- 3. samples
        sample = json.load(open(SCRATCH + "/oracle_sample.json", encoding="utf-8"))[pname]
        print(" SAMPLES")
        for s in sample:
            ptr = s["json_pointer"]
            cl = inst_leaves.get(ptr)
            ok = cl is not None and cl["original"] == s["original"] and cl["projected"] == s["projected"]
            # hand derivation: sequential replacement over the original leaf value
            hand = s["original"]
            steps = []
            for tok in ORDER:
                n = hand.count(tok)
                if n:
                    steps.append((tok, n))
                hand = hand.replace(tok, vals[tok.strip("_")])
            ok_hand = hand == s["projected"]
            idx = int(ptr.split("/")[1])
            # projected_task start_url must equal projected leaf
            pt = ip["tasks"][idx]["projected_task"]["start_url"]
            print("  ", ptr, "len(orig)", len(s["original"]), "tokens", steps,
                  "instrument_match", ok, "hand_match", ok_hand,
                  "projected_task_start_url_match", pt == s["projected"])
            print("     orig:", s["original"])
            print("     proj:", s["projected"])
            if not (ok and ok_hand and pt == s["projected"]):
                note("sample:" + pname, s)
        # output index mapping for samples
        for s in sample:
            idx = int(s["json_pointer"].split("/")[1])
            t = ip["tasks"][idx]
            if t["output_index"] != idx or t["task_id"] != base[idx]["task_id"]:
                note("index:" + pname, {"idx": idx, "rec": {"output_index": t["output_index"],
                                                            "task_id": t["task_id"]}})
        # output filename rule
        print(" sample output_filename", ip["tasks"][0]["output_filename"],
              "index_equals_task_id", ip["tasks"][0]["index_equals_task_id"])

        # ---- 4. category semantics caveat: non_url_field values that look like URLs
        url_like = [(p, oracle[p][0], oracle[p][1]) for p in oracle
                    if oracle[p][0] not in URL_TEMPLATES and isinstance(oracle[p][1], str)
                    and ("http://" in oracle[p][2] or "https://" in oracle[p][2])]
        print(" non_url changed leaves holding http(s) projected values", len(url_like))
        for item in url_like[:3]:
            print("   ", item[0], item[1], repr(item[2])[:100])

    print("\nTOTAL MISMATCH GROUPS", len(mismatches))
    for tag, d in mismatches:
        print(" ", tag, d if not isinstance(d, (list, dict)) else json.dumps(d)[:300])


if __name__ == "__main__":
    main()

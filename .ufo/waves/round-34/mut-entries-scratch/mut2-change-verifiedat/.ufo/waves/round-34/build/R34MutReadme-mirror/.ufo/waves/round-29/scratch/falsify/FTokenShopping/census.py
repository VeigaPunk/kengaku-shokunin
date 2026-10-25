#!/usr/bin/env python3
"""Independent __SHOPPING__ census. Authored from the prereg TEXT, generator bytes and
pinned data. Does NOT read or import plans/config_projection.py."""
import hashlib
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(LANE, "plans/fixtures/r28/webarena/config_files/test.raw.json")
PROF = os.path.join(LANE, "plans/fixtures/r29/profiles.json")
GEN = os.path.join(LANE, "plans/fixtures/r29/generate_test_data.py")
MANIFEST = os.path.join(LANE, "plans/fixtures/r29/manifest.json")
INST = os.path.join(
    LANE, ".ufo/waves/round-29/scratch/falsify/FTokenShopping/instrument.json"
)

TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
          "__WIKIPEDIA__", "__MAP__"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TARGET = "__SHOPPING__"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def walk(node, ptr=""):
    """Yield (json_pointer, string) for every string leaf, in document order."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, ptr + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, ptr + "/" + str(i))
    elif isinstance(node, str):
        yield ptr, node


def path_template(ptr):
    # /0/eval/program_html/3/url -> eval.program_html[].url ; /0/start_url -> start_url
    parts = ptr.split("/")[1:]
    out = []
    for i, p in enumerate(parts):
        if p.isdigit() and i > 0:
            continue
        if p.isdigit() and i == 0:
            continue
        out.append(p)
    if not out:
        return ptr
    if len(out) >= 2 and parts[-2].isdigit():
        return ".".join(out[:-1]) + "[]." + out[-1]
    return ".".join(out)


def main():
    raw_b = open(RAW, "rb").read()
    raw = raw_b.decode("utf-8")
    prof = json.load(open(PROF, "r", encoding="utf-8"))
    gen_src = open(GEN, "r", encoding="utf-8").read()
    manifest = json.load(open(MANIFEST, "r", encoding="utf-8"))
    inst = json.load(open(INST, "r", encoding="utf-8"))

    print("=== INPUT AUTHENTICATION ===")
    print("raw_sha256", sha(raw_b), "bytes", len(raw_b), "chars", len(raw))
    print("manifest_sha256_file", sha(open(MANIFEST, "rb").read()),
          "instrument", inst["manifest_sha256"])
    print("gen_sha256", sha(open(GEN, "rb").read()),
          "pinned", manifest["files"]["plans/fixtures/r29/generate_test_data.py"]["sha256"])
    print("prof_sha256", sha(open(PROF, "rb").read()),
          "pinned", manifest["files"]["plans/fixtures/r29/profiles.json"]["sha256"])
    print("raw_pinned", manifest["files"]["plans/fixtures/r28/webarena/config_files/test.raw.json"]["sha256"])
    print("raw_equals_instrument", inst["raw_text_sha256"] == sha(raw_b))

    print("\n=== GENERATOR REPLACEMENT ORDER (source bytes) ===")
    gen_lines = gen_src.splitlines()
    seen = []
    for n, line in enumerate(gen_lines, 1):
        if ".replace(" in line:
            seen.append((n, line.strip()))
            print(n, line.strip())
    src_order = [s.split('"')[1] for _, s in seen]
    src_short = [t.strip("_") if False else t[2:-2] for t in src_order]
    print("parsed_order", src_order)
    print("parsed_order_short", src_short)
    print("order_matches_manifest", src_short == manifest["replacement_order"])

    # ---------- 1. RAW LITERAL OCCURRENCES ----------
    print("\n=== RAW LITERAL OCCURRENCES (str.count on original text) ===")
    raw_counts = {t: raw.count(t) for t in TOKENS}
    print("raw_counts", raw_counts)
    print("sum", sum(raw_counts.values()))
    print("instrument_original", inst["population"]["original_occurrences_by_token"])
    for t in TOKENS:
        a, b = raw_counts[t], inst["population"]["original_occurrences_by_token"][t]
        print("MATCH" if a == b else "MISMATCH", t, "mine", a, "instrument", b)

    # independent regex-free rescan via find loop to cross-check str.count
    def find_count(s, sub):
        c, i = 0, 0
        while True:
            i = s.find(sub, i)
            if i < 0:
                return c
            c += 1
            i += 1
    alt = {t: find_count(raw, t) for t in TOKENS}
    print("find_loop_counts", alt, "agree_with_str_count", alt == raw_counts)

    # ---------- 2. SUBSTRING / OVERLAP LOGIC ----------
    print("\n=== SUBSTRING OVERLAP BETWEEN TOKENS ===")
    for a in TOKENS:
        for b in TOKENS:
            if a != b and a in b:
                print("SUBSTRING", a, "inside", b, "count", b.count(a))
    print("token substrings of TARGET:",
          {t: (t in TARGET) for t in TOKENS if t != TARGET})
    # does any token contain a shorter token as a prefix that naive replace would hit?
    for a in TOKENS:
        for b in TOKENS:
            if a != b and b in a:
                print("WARN naive order would double-hit:", b, "->", a)
    # explicit check: TARGET as substring of SHOPPING_ADMIN occurrences
    print("TARGET in '__SHOPPING_ADMIN__':", TARGET in "__SHOPPING_ADMIN__")
    # Count what a naive *prefix* regex like __SHOPPING(?:__|_) would pick up
    import re
    naive = re.findall(r"__SHOPPING\w*__", raw)
    from collections import Counter
    c = Counter(naive)
    print("regex __SHOPPING\\\\w*__ families:", dict(c))

    # ---------- 3. DECODED LEAF CENSUS ----------
    data = json.loads(raw)
    leaves = list(walk(data))
    print("\n=== DECODED LEAVES ===")
    print("tasks", len(data), "string_leaves", len(leaves),
          "instrument_string_leaf_count", inst["profiles"]["distinct_origins"]["string_leaf_count"])

    leaf_counts = {}          # token -> leaf count
    leaf_occ = {}             # token -> total occurrences inside leaves
    multi = {}                # token -> leaves with >=2 occurrences
    tasks_with = {t: set() for t in TOKENS}
    leaf_tokens = {}          # ptr -> set(tokens present)
    ptr_index = {}            # ptr -> (task_index, task_id)
    for ptr, s in leaves:
        idx = int(ptr.split("/")[1])
        temps = set()
        for t in TOKENS:
            n = s.count(t)
            if n:
                leaf_counts[t] = leaf_counts.get(t, 0) + 1
                leaf_occ[t] = leaf_occ.get(t, 0) + n
                tasks_with[t].add(idx)
                temps.add(t)
                if n >= 2:
                    multi[t] = multi.get(t, 0) + 1
        leaf_tokens[ptr] = temps
        ptr_index[ptr] = (idx, data[idx]["task_id"])

    print("leaf_counts", {t: leaf_counts.get(t,0) for t in TOKENS})
    print("leaf_occurrences", {t: leaf_occ.get(t,0) for t in TOKENS})
    print("leaves_with_multiple_occurrences", multi)
    print("extra_occurrences(occ-leafcount)", {t: leaf_occ.get(t,0) - leaf_counts.get(t,0) for t in TOKENS})
    print("tasks_with_token", {t: len(tasks_with[t]) for t in TOKENS})
    print("sum_of_leaf_counts", sum(leaf_counts.values()), "changed_leaves_with_multi", sum(multi.values()))
    print("instrument_tasks_with", inst["population"]["tasks_with_token"])
    for t in TOKENS:
        a, b = len(tasks_with[t]), inst["population"]["tasks_with_token"][t]
        print("MATCH" if a == b else "MISMATCH", "TASKS_WITH_TOKEN", t, "mine", a, "instrument", b)

    # mixed-token leaves would make changed_leaves_by_token sum exceed changed_leaf_count
    mixed = {p: sorted(v) for p, v in leaf_tokens.items() if len(v) > 1}
    print("mixed_token_leaves", len(mixed), list(mixed.items())[:5])
    print("sum_leafcounts", sum(leaf_counts.values()),
          "distinct_changed_leaves", len([p for p, v in leaf_tokens.items() if v]))

    # escaped-token probe: decoded occurrences not visible as raw literal text
    dec_occ = {t: sum(s.count(t) for _, s in leaves) for t in TOKENS}
    print("decoded_occurrences", dec_occ,
          "raw_minus_decoded", {t: raw_counts[t] - dec_occ[t] for t in TOKENS})

    # roles: token inside a JSON key?
    roles = Counter()
    for t in TOKENS:
        i = 0
        while True:
            i = raw.find(t, i)
            if i < 0:
                break
            # a token is in a key if an even number of unescaped quotes precedes it
            prefix = raw[:i]
            roles["value"] += 1
            i += 1
    print("instrument_occurrence_roles", inst["population"]["occurrence_roles"])
    # precise key/value determination by parsing object keys
    key_tokens = 0
    def scan_keys(node):
        nonlocal key_tokens
        if isinstance(node, dict):
            for k, v in node.items():
                if any(t in k for t in TOKENS):
                    key_tokens += 1
                scan_keys(v)
        elif isinstance(node, list):
            for v in node:
                scan_keys(v)
    scan_keys(data)
    print("decoded_dict_keys_containing_token", key_tokens)

    # ---------- 4. PER-PROFILE PROJECTION ----------
    print("\n=== PER-PROFILE SEQUENTIAL PROJECTION (own implementation) ===")
    prof_results = {}
    for pname, pdef in prof.items():
        vals = pdef["values"]
        steps = []
        text = raw
        for name in ORDER:
            tok = "__%s__" % name
            before_tokens = {t: text.count(t) for t in TOKENS}
            n = text.count(tok)
            text = text.replace(tok, vals[name])
            after_tokens = {t: text.count(t) for t in TOKENS}
            steps.append({
                "token": tok, "applied": n,
                "cascade_effect": {t: after_tokens[t] - before_tokens[t]
                                   for t in TOKENS if after_tokens[t] != before_tokens[t]},
                "value_contains_token": any(t in vals[name] for t in TOKENS),
            })
        proj = json.loads(text)
        proj_leaves = dict(walk(proj))
        changed = {}
        changed_by_tok = {}
        changed_tasks_by_tok = {}
        for ptr, s in leaves:
            ns = proj_leaves.get(ptr)
            if ns != s:
                changed[ptr] = (s, ns)
                idx = int(ptr.split("/")[1])
                for t in leaf_tokens[ptr]:
                    changed_by_tok.setdefault(t, set()).add(ptr)
                    changed_tasks_by_tok.setdefault(t, set()).add(idx)
        cats = Counter()
        for ptr, (s, ns) in changed.items():
            cats["non_url_field" if "url" not in path_template(ptr) else "url_field"] += 1
        prof_results[pname] = {
            "steps": steps,
            "parsed": len(proj),
            "changed_leaf_count": len(changed),
            "changed_leaves_by_token": {t: len(v) for t, v in changed_by_tok.items()},
            "changed_tasks_by_token": {t: len(v) for t, v in changed_tasks_by_tok.items()},
            "categories": dict(cats),
            "text_sha256": sha(text.encode("utf-8")),
            "changed": changed,
            "proj": proj,
        }
        print("PROFILE", pname)
        print("  applied", [(s["token"], s["applied"]) for s in steps])
        print("  cascade", [s["cascade_effect"] for s in steps])
        print("  parsed", len(proj), "changed", len(changed), "cats", dict(cats))
        print("  changed_leaves_by_token", prof_results[pname]["changed_leaves_by_token"])
        print("  changed_tasks_by_token", prof_results[pname]["changed_tasks_by_token"])
        print("  text_sha256", prof_results[pname]["text_sha256"])
        print("  remaining_text", {t: text.count(t) for t in TOKENS})
        print("  remaining_decoded", {t: sum(1 for s in proj_leaves.values() if t in s) for t in TOKENS})

    # ---------- 5. COMPARE WITH INSTRUMENT ----------
    print("\n=== COMPARE WITH INSTRUMENT (--json / --summary) ===")
    bad = 0
    for pname, mine in prof_results.items():
        ip = inst["profiles"][pname]
        isteps = [s["applied_replacements"] for s in ip["steps"]]
        msteps = [s["applied"] for s in mine["steps"]]
        print("PROFILE", pname, "applied mine", msteps, "instrument", isteps,
              "MATCH" if msteps == isteps else "MISMATCH")
        if msteps != isteps:
            bad += 1
        for key, ik in (("changed_leaves_by_token", "changed_leaves_by_token"),
                        ("changed_tasks_by_token", "changed_tasks_by_token")):
            a, b = mine[key], ip[ik]
            same = a == {k: v for k, v in b.items() if v or k in a}
            print("  ", key, "mine", a, "instrument", b, "MATCH" if a == b else "MISMATCH")
            if a != b:
                bad += 1
        print("  changed_leaf_count mine", mine["changed_leaf_count"],
              "instrument", ip["changed_leaf_count"],
              "MATCH" if mine["changed_leaf_count"] == ip["changed_leaf_count"] else "MISMATCH")
        print("  changed_task_count mine", len({int(p.split('/')[1]) for p in mine["changed"]}),
              "instrument", ip["changed_task_count"])
        print("  text_sha256 MATCH" if mine["text_sha256"] == ip["projected_text_sha256"] else
              "  text_sha256 MISMATCH mine %s inst %s" % (mine["text_sha256"], ip["projected_text_sha256"]))
        print("  categories mine", mine["categories"], "instrument", ip["changed_leaves_by_category"])
        print("  parsed mine", mine["parsed"], "instrument", ip["parsed_task_count"])
        print("  string_leaf_count mine", len(leaves), "instrument", ip["string_leaf_count"])

    # ---------- 6. PER-TASK / PER-LEAF DIFF VS INSTRUMENT FOR TARGET ----------
    print("\n=== TARGET TOKEN PER-TASK DETAIL (distinct_origins) ===")
    ip = inst["profiles"]["distinct_origins"]
    mine = prof_results["distinct_origins"]
    tgt_orig = [r for r in inst["occurrence_provenance"] if r["token"] == TARGET]
    print("provenance_rows_target", len(tgt_orig))
    if tgt_orig:
        print("first", json.dumps(tgt_orig[0]))
        print("keys", sorted(tgt_orig[0].keys()))
    # offset check for every target occurrence
    offs = []
    bad_off = 0
    for r in tgt_orig:
        o = r.get("original_input_codepoint_offset")
        if raw[o:o + len(TARGET)] != TARGET:
            bad_off += 1
        offs.append(o)
    print("provenance_offset_verified", len(tgt_orig) - bad_off, "bad", bad_off,
          "unique_offsets", len(set(offs)))
    # per-task instrument changed leaves vs mine
    inst_tasks = {t["output_index"]: t for t in ip["tasks"]}
    mism_task = 0
    tgt_leaves_inst = 0
    for idx, t in inst_tasks.items():
        cl = [c for c in t["changed_leaves"] if TARGET in c["tokens"]]
        tgt_leaves_inst += len(cl)
        mine_cl = sorted(p for p, (s, ns) in mine["changed"].items()
                         if int(p.split("/")[1]) == idx and TARGET in leaf_tokens[p])
        got = sorted(c["json_pointer"] for c in cl)
        if got != mine_cl:
            mism_task += 1
            if mism_task <= 3:
                print("TASK MISMATCH", idx, "instrument", got[:6], "mine", mine_cl[:6])
        # values must match too
        for c in cl:
            if mine["changed"].get(c["json_pointer"], (None, None))[1] != c["projected"]:
                print("VALUE MISMATCH", idx, c["json_pointer"], c["projected"][:40],
                      mine["changed"].get(c["json_pointer"], (None, None))[1])
                mism_task += 1
    print("target_leaves_in_instrument_per_task_sum", tgt_leaves_inst,
          "mine", len(mine["changed"] and [p for p, v in leaf_tokens.items() if TARGET in v]))
    print("task_level_mismatches", mism_task)
    print("instrument changed_leaves_by_token target", ip["changed_leaves_by_token"][TARGET],
          "mine", len([p for p, v in leaf_tokens.items() if TARGET in v]))

    # tasks carrying target vs changed tasks carrying target
    print("target_tasks_carrying", len(tasks_with[TARGET]),
          "target_tasks_changed_instrument", ip["changed_tasks_by_token"][TARGET])
    # per-leaf original text for multi-occurrence SHOPPING leaves
    print("\n=== TARGET MULTI-OCCURRENCE LEAVES ===")
    for ptr, s in leaves:
        n = s.count(TARGET)
        if n >= 2:
            print(ptr, "task", ptr_index[ptr], "n", n, "len", len(s), "snippet", s[:120].replace("\n", " "))
    print("\n=== TARGET LEAVES BY PATH TEMPLATE ===")
    tmpl = Counter()
    for ptr, s in leaves:
        if TARGET in s:
            tmpl[path_template(ptr)] += 1
    print(dict(tmpl))
    print("instrument path templates for target-containing leaves: see per-profile by_path_template")
    print("\n=== FULL PROJECTED OBJECT COMPARISON (all 2436 task/profile) ===")
    for pname, mine in prof_results.items():
        ip = inst["profiles"][pname]
        inst_objs = [t["projected_task"] for t in sorted(ip["tasks"], key=lambda x: x["output_index"])]
        mine_objs = mine["proj"]
        print(pname, "objects", len(mine_objs), len(inst_objs),
              "IDENTICAL" if mine_objs == inst_objs else "DIFFER")
        if mine_objs != inst_objs:
            for i, (a, b) in enumerate(zip(mine_objs, inst_objs)):
                if a != b:
                    print("  first differing index", i)
                    break
        # per-path-template independent census
        tmpl = Counter()
        for ptr, (s, ns) in mine["changed"].items():
            tmpl[path_template(ptr)] += 1
        print("  by_path_template mine", dict(sorted(tmpl.items())))
        print("  by_path_template inst", dict(sorted(ip["changed_leaves_by_path_template"].items())))
        print("  template_match", dict(tmpl) == ip["changed_leaves_by_path_template"])
        # per-token per-template for target
        tgt = Counter()
        for ptr, s_ in leaves:
            if TARGET in s_:
                tgt[path_template(ptr)] += 1
        print("  TARGET leaves by template", dict(sorted(tgt.items())))

    print("\nBAD_CATEGORY_COUNTS", bad)
    print("DONE")


if __name__ == "__main__":
    main()

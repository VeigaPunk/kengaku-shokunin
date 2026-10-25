#!/usr/bin/env python3
"""Discriminating power of oracle agreement on the frozen population (FCritOracleIndependence).

Derived from plans/round-29-claims.md TEXT and the pinned generator bytes only; it does not import
plans/config_projection.py. It reads the instrument's --json OUTPUT from argv[1].

Builds seven oracle variants (one faithful, six deliberately wrong semantics) and asks: how many of
the 2436 task/profile records does each variant agree with exactly? A variant with a wrong semantics
that still agrees everywhere shows that population agreement cannot certify that semantic axis.
Then runs every variant on the adopted hand fixtures and one own quote/backslash case to show which
witness, if any, separates it.
"""
import hashlib
import json
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = LANE + "/plans/fixtures/r29/profiles.json"
HAND = LANE + "/plans/fixtures/r29/hand/"
PINS = {RAW: "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652",
        PROFILES: "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018"}
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
URL_KEYS = {"start_url", "reference_url", "url"}


def pinned(path):
    b = open(path, "rb").read()
    assert hashlib.sha256(b).hexdigest() == PINS[path], path
    return b.decode("utf-8")


def text_seq(raw, values, order):
    for name in order:
        raw = raw.replace("__%s__" % name, values[name])
    return json.loads(raw)


def text_simultaneous(raw, values, order):
    names = sorted(order, key=len, reverse=True)
    rx = re.compile("|".join(re.escape("__%s__" % n) for n in names))
    return json.loads(rx.sub(lambda m: values[m.group(0)[2:-2]], raw))


def leaf_sub(node, values, order, url_only=False, key=None):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            nk = k if url_only else sub_str(k, values, order)
            out[nk] = leaf_sub(v, values, order, url_only, k)
        return out
    if isinstance(node, list):
        return [leaf_sub(v, values, order, url_only, key) for v in node]
    if isinstance(node, str):
        if url_only and key not in URL_KEYS:
            return node
        return sub_str(node, values, order)
    return node


def sub_str(s, values, order):
    for name in order:
        s = s.replace("__%s__" % name, values[name])
    return s


VARIANTS = {
    "V0_faithful_text_source_order": lambda raw, v: (text_seq(raw, v, ORDER), "index"),
    "V1_text_reversed_order": lambda raw, v: (text_seq(raw, v, ORDER[::-1]), "index"),
    "V2_text_simultaneous_single_pass": lambda raw, v: (text_simultaneous(raw, v, ORDER), "index"),
    "V3_decoded_leaf_keys_and_values": lambda raw, v: (leaf_sub(json.loads(raw), v, ORDER), "index"),
    "V4_decoded_leaf_reversed_order": lambda raw, v: (leaf_sub(json.loads(raw), v, ORDER[::-1]), "index"),
    "V5_filename_by_task_id": lambda raw, v: (text_seq(raw, v, ORDER), "task_id"),
    "V6_url_fields_only": lambda raw, v: (leaf_sub(json.loads(raw), v, ORDER, url_only=True), "index"),
}


def ptr(parts):
    return "".join("/" + str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def changed(orig, proj, path, out):
    if isinstance(orig, dict) and isinstance(proj, dict):
        ok, pk = list(orig), list(proj)
        if ok != pk:
            out.append((ptr(path), "KEYS", json.dumps(ok), json.dumps(pk)))
        for a, b in zip(ok, pk):
            changed(orig[a], proj[b], path + [a], out)
    elif isinstance(orig, list) and isinstance(proj, list):
        for i, (a, b) in enumerate(zip(orig, proj)):
            changed(a, b, path + [i], out)
    elif isinstance(orig, str) and orig != proj:
        out.append((ptr(path), orig, proj))


def records(raw, values, variant):
    data, naming = VARIANTS[variant](raw, values)
    orig = json.loads(raw)
    recs = []
    for idx, item in enumerate(data):
        diff = []
        changed(orig[idx], item, [idx], diff)
        name = "config_files/%s.json" % (idx if naming == "index" else item["task_id"])
        recs.append({"output_filename": name, "projected_task": item,
                     "would_be_file_sha256": hashlib.sha256(json.dumps(item, indent=2).encode()).hexdigest(),
                     "changed": sorted(diff)})
    return recs


def main():
    prod = json.load(open(sys.argv[1]))
    raw = pinned(RAW)
    profiles = json.loads(pinned(PROFILES))
    print("POPULATION_AGREEMENT unit=task/profile records (of 2436)")
    for variant in VARIANTS:
        tally = {"projected_task": 0, "output_filename": 0, "would_be_file_sha256": 0, "changed_leaves": 0, "all_four": 0}
        first_mismatch = None
        total = 0
        for pname, prof in profiles.items():
            ours = records(raw, prof["values"], variant)
            theirs = prod["profiles"][pname]["tasks"]
            assert len(ours) == len(theirs) == 812
            for o, t in zip(ours, theirs):
                total += 1
                tc = sorted((l["json_pointer"], l["original"], l["projected"]) for l in t["changed_leaves"])
                eq = {"projected_task": o["projected_task"] == t["projected_task"],
                      "output_filename": o["output_filename"] == t["output_filename"],
                      "would_be_file_sha256": o["would_be_file_sha256"] == t["would_be_file_sha256"],
                      "changed_leaves": o["changed"] == tc}
                for k, v in eq.items():
                    tally[k] += v
                tally["all_four"] += all(eq.values())
                if not all(eq.values()) and first_mismatch is None:
                    bad = [k for k, v in eq.items() if not v]
                    first_mismatch = "%s output_index=%d task_id=%s fields=%s" % (pname, t["output_index"], t["task_id"], bad)
        print("%-36s total=%d %s first_mismatch=%s" % (variant, total, json.dumps(tally), first_mismatch))

    print("HAND_WITNESS_SEPARATION (does the witness's expected value reject the variant?)")
    order_case = json.load(open(HAND + "cascade-order.case.json"))
    url_case = json.load(open(HAND + "url-only.fixture.json"))
    url_exp = json.load(open(HAND + "url-only.expected.json"))
    idx_case = json.load(open(HAND + "index-shuffled-ids.fixture.json"))
    quote_values = dict(zip(ORDER, ['http://g.invalid/a"b', "http://r.invalid/a\\nb", "http://s.invalid", "http://sa.invalid", "http://w.invalid", "http://m.invalid"]))
    quote_raw = '[{"task_id":0,"start_url":"__GITLAB__","intent":"x"},{"task_id":1,"start_url":"__REDDIT__/p"}]'
    for variant in VARIANTS:
        row = {}
        try:
            data, _ = VARIANTS[variant](order_case["raw_serialized_text"], order_case["values"])
            row["cascade_order"] = "agrees" if data == order_case["expected_parsed_value"] else "REJECTS"
        except ValueError as e:
            row["cascade_order"] = "REJECTS(%s)" % type(e).__name__
        data, _ = VARIANTS[variant](url_case["raw_text"], url_case["values"])
        row["url_only"] = "agrees" if data == url_exp["projection"] else "REJECTS"
        recs = records(idx_case["input_raw_text"], idx_case["profile_values"], variant)
        got = [{"task_id": r["projected_task"]["task_id"], "output_filename": r["output_filename"], "projected_task": r["projected_task"]} for r in recs]
        exp = [{"task_id": e["task_id"], "output_filename": e["output_filename"], "projected_task": e["projected_task"]} for e in idx_case["expected_records"]]
        row["index_shuffled"] = "agrees" if got == exp else "REJECTS"
        try:
            data, _ = VARIANTS[variant](quote_raw, quote_values)
            row["own_quote_backslash_case"] = "parses:start_url[1]=%r" % data[1]["start_url"]
        except ValueError as e:
            row["own_quote_backslash_case"] = "decode_error(%s)" % type(e).__name__
        print("%-36s %s" % (variant, json.dumps(row)))


if __name__ == "__main__":
    main()

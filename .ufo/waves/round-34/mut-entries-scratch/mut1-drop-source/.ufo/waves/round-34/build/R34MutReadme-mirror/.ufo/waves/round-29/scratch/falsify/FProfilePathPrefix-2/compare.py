#!/usr/bin/env python3
"""Independent full comparison for path_prefix against instrument --json OUTPUT only."""
import hashlib
import json

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
SCR = ROOT + "/.ufo/waves/round-29/scratch/falsify/FProfilePathPrefix-2"
RAW_P = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF_P = ROOT + "/plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {n: "__%s__" % n for n in ORDER}
PNAME = "path_prefix"


def json_string_spans(text):
    """Yield (path_tuple, role, decoded, raw_start, raw_content) for every string literal.

    Minimal recursive-descent JSON scanner over the raw serialized text.
    """
    out = []
    n = len(text)

    def skip_ws(i):
        while i < n and text[i] in " \t\r\n":
            i += 1
        return i

    def parse_string(i):
        assert text[i] == '"'
        j = i + 1
        buf = []
        while True:
            c = text[j]
            if c == "\\":
                e = text[j + 1]
                mapping = {'"': '"', "\\": "\\", "/": "/", "b": "\b",
                           "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
                if e in mapping:
                    buf.append(mapping[e]); j += 2
                elif e == "u":
                    buf.append(chr(int(text[j + 2:j + 6], 16))); j += 6
                else:
                    raise ValueError("bad escape at %d" % j)
            elif c == '"':
                j += 1
                break
            else:
                buf.append(c); j += 1
        return j, "".join(buf), j

    def parse_value(i, path):
        i = skip_ws(i)
        c = text[i]
        if c == "{":
            i = skip_ws(i + 1)
            if text[i] == "}":
                return i + 1
            while True:
                i = skip_ws(i)
                assert text[i] == '"'
                j, key, _ = parse_string(i)
                out.append((path + (("@key", key),), "key", key, i + 1, text[i + 1:j - 1]))
                i = skip_ws(j)
                assert text[i] == ":"
                i = parse_value(i + 1, path + (key,))
                i = skip_ws(i)
                if text[i] == ",":
                    i += 1
                    continue
                assert text[i] == "}"
                return i + 1
        if c == "[":
            i = skip_ws(i + 1)
            if text[i] == "]":
                return i + 1
            k = 0
            while True:
                i = parse_value(i, path + (k,))
                k += 1
                i = skip_ws(i)
                if text[i] == ",":
                    i += 1
                    continue
                assert text[i] == "]"
                return i + 1
        if c == '"':
            j, val, end = parse_string(i)
            out.append((path, "value", val, i + 1, text[i + 1:end - 1]))
            return end
        # number/true/false/null
        j = i
        while j < n and text[j] not in ",]} \t\r\n":
            j += 1
        return j

    end = parse_value(0, ())
    assert skip_ws(end) == n
    return out


def pointer(path):
    return "/" + "/".join(str(x) for x in path)


def template(path):
    parts = []
    for seg in path[1:]:
        if isinstance(seg, int):
            if parts:
                parts[-1] = parts[-1] + "[]"
            else:
                parts.append("[]")
        else:
            parts.append(str(seg))
    return ".".join(parts)


def leaves_with_raw(obj):
    """(pointer_path, value, raw_leaf_literal_hash?) - structural walk only."""
    out = []
    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, p + (k,))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, p + (i,))
        else:
            out.append((p, o))
    walk(obj, ())
    return out


def string_leaves(obj):
    out = []
    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, p + (k,))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, p + (i,))
        elif isinstance(o, str):
            out.append((p, o))
    walk(obj, ())
    return out


def main():
    raw_bytes = open(RAW_P, "rb").read()
    raw = raw_bytes.decode("utf-8")
    prof = json.loads(open(PROF_P, "rb").read())
    vals = prof[PNAME]["values"]
    inst = json.load(open("/tmp/r29_fpp.json"))
    ip = inst["profiles"][PNAME]

    text = raw
    for n in ORDER:
        text = text.replace(TOK[n], vals[n])
    data = json.loads(text)
    raw_obj = json.loads(raw)

    problems = []

    # 1) scalar metrics
    checks = {
        "projected_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "string_leaf_count": len(string_leaves(data)),
        "parsed_task_count": len(data),
        "changed_leaf_count": sum(1 for (pa, va), (pb, vb)
                                  in zip(string_leaves(raw_obj), string_leaves(data)) if va != vb),
    }
    for k, mine in checks.items():
        theirs = ip[k]
        print(("OK  " if mine == theirs else "MISMATCH ") + k, "mine=", mine, "inst=", theirs)
        if mine != theirs:
            problems.append((k, mine, theirs))

    # 2) values/label/purpose consistency with profiles.json
    print("OK   values_equal" if ip["values"] == vals else "MISMATCH values")
    if ip["values"] != vals:
        problems.append(("values", vals, ip["values"]))
    print("inst stimulus_class:", ip["stimulus_class"])
    print("all six values endswith /prefix:", all(v.endswith("/prefix") for v in vals.values()),
          "| any scheme:", all(v.startswith("http://") for v in vals.values()),
          "| hosts end .invalid:", all(v.split("/")[2].split(":")[0].endswith(".invalid") for v in vals.values()))
    print("inst stimulus_observations:", ip["stimulus_observations"])

    # junction independently
    jt = 0
    for n in ORDER:
        tok = TOK[n]
        start = 0
        while True:
            i = raw.find(tok, start)
            if i < 0:
                break
            if vals[n].endswith("/") and i + len(tok) < len(raw) and raw[i + len(tok)] == "/":
                jt += 1
            start = i + len(tok)
    print(("OK  " if ip["stimulus_observations"]["value_slash_then_raw_slash_junctions"] == jt else "MISMATCH ") +
          "junctions mine=%d inst=%d" % (jt, ip["stimulus_observations"]["value_slash_then_raw_slash_junctions"]))
    if jt != ip["stimulus_observations"]["value_slash_then_raw_slash_junctions"]:
        problems.append(("junctions", jt, ip["stimulus_observations"]))

    # 3) per-task projected objects, changed leaves, file hashes
    inst_tasks = ip["tasks"]
    if len(inst_tasks) != len(data):
        problems.append(("task_count", len(data), len(inst_tasks)))
    raw_leaves = leaves_with_raw(raw_obj)
    proj_leaves = leaves_with_raw(data)
    assert [p for p, _ in raw_leaves] == [p for p, _ in proj_leaves]

    task_problems = 0
    changed_mismatch = 0
    hash_mismatch = 0
    for idx, it in enumerate(data):
        rec = inst_tasks[idx]
        if rec["projected_task"] != it:
            task_problems += 1
            if task_problems <= 3:
                problems.append(("projected_task[%d]" % idx, "diff", ""))
        exp_hash = hashlib.sha256(json.dumps(it, indent=2).encode("utf-8")).hexdigest()
        if rec["would_be_file_sha256"] != exp_hash:
            hash_mismatch += 1
            if hash_mismatch <= 3:
                problems.append(("would_be_file_sha256[%d]" % idx, exp_hash, rec["would_be_file_sha256"]))
        # my changed leaves for this task
        mine = []
        for (p, va), (_, vb) in zip(raw_leaves, proj_leaves):
            if p[0] != idx:
                continue
            if va != vb:
                mine.append((pointer(p), va, vb, template(p)))
        theirs = rec["changed_leaves"]
        if len(mine) != len(theirs):
            changed_mismatch += 1
            if changed_mismatch <= 3:
                problems.append(("changed_len[%d]" % idx, len(mine), len(theirs)))
            continue
        for (ptr, va, vb, tmpl), c in zip(mine, theirs):
            if (c["json_pointer"], c["original"], c["projected"], c["path_template"]) != (ptr, va, vb, tmpl):
                changed_mismatch += 1
                if changed_mismatch <= 3:
                    problems.append(("changed_leaf[%d]" % idx,
                                     (ptr, va, vb, tmpl),
                                     (c["json_pointer"], c["original"], c["projected"], c["path_template"])))
                break
        # index mapping
        if rec["output_index"] != idx or rec["task_id"] != it["task_id"]:
            problems.append(("index[%d]" % idx, idx, (rec["output_index"], rec["task_id"])))
    print("per-task projected_task diffs:", task_problems)
    print("per-task would_be_file_sha256 diffs:", hash_mismatch)
    print("per-task changed_leaves diffs:", changed_mismatch)

    # 4) occurrence provenance vs my raw scanner
    spans = json_string_spans(raw)
    my_occ = []
    for path, role, val, rstart, rawlit in spans:
        if role != "value":
            continue
        for n in ORDER:
            tok = TOK[n]
            pos = 0
            while True:
                k = rawlit.find(tok, pos)
                if k < 0:
                    break
                my_occ.append({
                    "original_input_codepoint_offset": rstart + k,
                    "token": tok,
                    "task_index": path[0],
                    "json_pointer": pointer(path),
                    "path_template": template(path),
                    "string_role": "value",
                })
                pos = k + len(tok)
    my_occ.sort(key=lambda r: r["original_input_codepoint_offset"])
    theirs_occ = inst["occurrence_provenance"]
    print("occurrence counts mine=%d inst=%d" % (len(my_occ), len(theirs_occ)))
    if len(my_occ) != len(theirs_occ):
        problems.append(("occ_count", len(my_occ), len(theirs_occ)))
    occ_bad = 0
    for a, b in zip(my_occ, theirs_occ):
        if a["original_input_codepoint_offset"] != b["original_input_codepoint_offset"] or \
           a["token"] != b["token"] or a["task_index"] != b["task_index"] or \
           a["json_pointer"] != b["json_pointer"] or a["path_template"] != b["path_template"] or \
           a["string_role"] != b["string_role"]:
            occ_bad += 1
            if occ_bad <= 5:
                problems.append(("occ", a, b))
    print("occurrence mismatches:", occ_bad)

    # 5) population / other markers / tokens followed by slash
    pop = inst["population"]
    raw_slash = 0
    for n in ORDER:
        tok = TOK[n]
        start = 0
        while True:
            i = raw.find(tok, start)
            if i < 0:
                break
            if i + len(tok) < len(raw) and raw[i + len(tok)] == "/":
                raw_slash += 1
            start = i + len(tok)
    print("population tokens_followed_by_slash inst=", pop["tokens_followed_by_slash"], "mine=", raw_slash)
    if pop["tokens_followed_by_slash"] != raw_slash:
        problems.append(("tokens_followed_by_slash", raw_slash, pop["tokens_followed_by_slash"]))
    print("other markers __last_url__", raw.count("__last_url__"), "__page__", raw.count("__page__"),
          "| inst", pop["other_double_underscore_markers"])

    # 6) changed-leaf category consistency with the instrument's own template buckets
    URL_TEMPLATES = {"start_url", "eval.reference_url", "eval.program_html[].url"}
    cat_bad = 0
    for t in inst_tasks:
        for c in t["changed_leaves"]:
            want = "url_field" if c["path_template"] in URL_TEMPLATES else "non_url_field"
            if c["category"] != want:
                cat_bad += 1
    print("category-vs-template inconsistencies:", cat_bad)

    # 7) findings / exit surfaces
    print("findings:", inst["findings"])

    print("\nPROBLEMS:", len(problems))
    for p in problems[:20]:
        print(p)
    json.dump({"problems": problems[:50], "n_problems": len(problems)},
              open(SCR + "/compare.json", "w"), indent=1)


if __name__ == "__main__":
    main()

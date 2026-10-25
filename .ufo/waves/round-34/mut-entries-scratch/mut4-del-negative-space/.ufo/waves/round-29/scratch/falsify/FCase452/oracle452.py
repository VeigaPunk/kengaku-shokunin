#!/usr/bin/env python3
"""FCase452 independent oracle for raw task_id 452.

Derived only from the prereg TEXT (plans/round-29-claims.md), the pinned
generator bytes (plans/fixtures/r29/generate_test_data.py), the pinned raw file
and the pinned profiles.  Never imports or reads plans/config_projection.py.

Usage: python3 oracle452.py <instrument-json-capture> <lane-root>
"""
import hashlib
import json
import re
import sys

ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOKENS = ["__%s__" % k for k in ORDER]
REQUIRED_PER_TASK = (
    "output_index",
    "output_filename",
    "task_id",
    "index_equals_task_id",
    "projected_task",
    "changed_leaves",
    "would_be_file_sha256",
)


def leaves(obj, ptr):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, ptr + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, ptr + "/" + str(i))
    else:
        yield ptr, obj


def top_level_spans(text):
    """Character spans of the elements of the top-level JSON array."""
    spans, depth, start = [], 0, None
    i = text.index("[") + 1
    for j in range(i, len(text)):
        c = text[j]
        if c == "{":
            if depth == 0:
                start = j
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                spans.append((start, j + 1))
    return spans


def main():
    inst_path, root = sys.argv[1], sys.argv[2]
    raw_bytes = open(root + "/plans/fixtures/r28/webarena/config_files/test.raw.json", "rb").read()
    text = raw_bytes.decode("utf-8")
    profiles = json.load(open(root + "/plans/fixtures/r29/profiles.json"))
    inst = json.load(open(inst_path))
    raw = json.loads(text)
    idx = 452

    print("raw_bytes", len(raw_bytes), "sha256", hashlib.sha256(raw_bytes).hexdigest())
    print("raw_codepoints", len(text),
          "non_ascii_bytes", sum(1 for b in raw_bytes if b > 127))
    print("raw_index==task_id_all", all(i == t["task_id"] for i, t in enumerate(raw)))
    print("raw_task452_task_id", raw[idx]["task_id"])

    spans = top_level_spans(text)
    s, e = spans[idx]
    seg = text[s:e]
    print("task452_text_span", s, e, "chars", e - s)
    for tok in TOKENS + ["__last_url__", "__page__"]:
        offs = [s + m.start() for m in re.finditer(tok, seg)]
        print("  span_token", tok, "count", len(offs), "offsets", offs)

    raw_flat = dict(leaves(raw[idx], "/%d" % idx))
    print("raw_task452_string_leaves", sum(1 for v in raw_flat.values() if isinstance(v, str)),
          "all_leaves", len(raw_flat))

    for name in ("distinct_origins", "path_prefix", "trailing_slash_sensitivity"):
        vals = profiles[name]["values"]
        projected_text = text
        for k in ORDER:
            projected_text = projected_text.replace("__%s__" % k, vals[k])
        obj = json.loads(projected_text)[idx]
        dump = json.dumps(obj, indent=2).encode("utf-8")
        proj_flat = dict(leaves(obj, "/%d" % idx))
        assert set(raw_flat) == set(proj_flat), "leaf set changed"
        mine = {p: (raw_flat[p], proj_flat[p]) for p in raw_flat if raw_flat[p] != proj_flat[p]}
        rec = inst["profiles"][name]["tasks"][idx]
        theirs = {l["json_pointer"]: (l["original"], l["projected"])
                  for l in rec["changed_leaves"]}
        cats = {l["json_pointer"]: (l["path_template"], l["category"], tuple(l["tokens"]))
                for l in rec["changed_leaves"]}

        print("=" * 20, name)
        print("projected_text_sha256", hashlib.sha256(projected_text.encode("utf-8")).hexdigest(),
              "instrument", inst["profiles"][name]["projected_text_sha256"])
        print("would_be_file_bytes", len(dump), "sha256", hashlib.sha256(dump).hexdigest(),
              "instrument", rec["would_be_file_sha256"])
        print("sorted_keys_sha256", hashlib.sha256(
            json.dumps(obj, indent=2, sort_keys=True).encode()).hexdigest())
        print("output_index", rec["output_index"], "task_id", rec["task_id"],
              "filename", rec["output_filename"], "index_equals_task_id", rec["index_equals_task_id"])
        print("record_keys_complete", sorted(rec) == sorted(REQUIRED_PER_TASK), sorted(rec))
        print("projected_task_deep_equal", rec["projected_task"] == obj)
        print("changed_leaf_sets_equal", mine == theirs, "mine_n", len(mine), "theirs_n", len(theirs))
        if mine != theirs:
            for p in sorted(set(mine) | set(theirs)):
                if mine.get(p) != theirs.get(p):
                    print("  MISMATCH", p, "mine", mine.get(p), "theirs", theirs.get(p))
        print("changed_leaves")
        for l in rec["changed_leaves"]:
            print("  ptr", l["json_pointer"], "| tpl", l["path_template"], "| cat", l["category"],
                  "| tokens", l["tokens"], "| original", repr(l["original"]),
                  "| projected", repr(l["projected"]))
        print("start_url", repr(obj["start_url"]))
        print("program_html0_url", repr(obj["eval"]["program_html"][0]["url"]))
        print("unchanged_required_contents", repr(
            obj["eval"]["program_html"][0]["required_contents"]))
        print("unchanged_intent", repr(obj["intent"]))
        print("unchanged_storage_state", repr(obj["storage_state"]))
        print("non_url_field_leaves", [p for p in cats if cats[p][1] == "non_url_field"])
        print("multi_occurrence_leaves", [
            (p, sum(mine[p][0].count(tok) for tok in TOKENS), list(v[2]))
            for p, v in cats.items()
            if sum(mine[p][0].count(tok) for tok in TOKENS) > 1 or len(v[2]) > 1])
        # cross-check the instrument's projection digest is the text upstream writes to test.json
        print("projtext_dump_len", len(projected_text))


if __name__ == "__main__":
    main()

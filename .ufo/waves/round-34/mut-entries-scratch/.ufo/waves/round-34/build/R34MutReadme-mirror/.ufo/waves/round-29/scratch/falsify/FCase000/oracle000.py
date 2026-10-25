"""Independent oracle for raw task_id 0, round-29 projection.

Derived only from: prereg TEXT (round-29-claims.md), the pinned generator bytes,
pinned profiles.json, pinned manifest.json, pinned raw test.raw.json.
Imports nothing from plans/config_projection.py.
"""
import hashlib
import json
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = LANE + "/plans/fixtures/r29/profiles.json"
MANIFEST = LANE + "/plans/fixtures/r29/manifest.json"
GEN = LANE + "/plans/fixtures/r29/generate_test_data.py"

raw_bytes = open(RAW, "rb").read()
raw_text = raw_bytes.decode("utf-8")
profiles = json.load(open(PROFILES))
manifest = json.load(open(MANIFEST))
order = manifest["replacement_order"]
tokens = {name: "__" + name + "__" for name in order}


def leaves(obj, path=""):
    """Yield (json_pointer, value) for every scalar/container-free leaf, incl. '' entries.

    Arrays use /index pointers. Strings, numbers, booleans, null are leaves.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, path + "/" + k.replace("~", "~0").replace("/", "~1"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, path + "/" + str(i))
    else:
        yield path, obj


def string_leaves(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from string_leaves(v, path + "/" + k.replace("~", "~0").replace("/", "~1"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from string_leaves(v, path + "/" + str(i))
    elif isinstance(obj, str):
        yield path, obj


original = json.loads(raw_text)
orig0 = original[0]

report = {}
for name in profiles:
    values = profiles[name]["values"]
    text = raw_text
    applied = {}
    for tokname in order:
        tok = tokens[tokname]
        if tokname not in values:
            raise SystemExit("profile missing key " + tokname)
        applied[tokname] = text.count(tok)
        text = text.replace(tok, values[tokname])
    projected = json.loads(text)
    proj0 = projected[0]

    # changed string leaves for task 0, walking both parsed objects
    orig_leaves = dict(string_leaves(orig0))
    proj_leaves = dict(string_leaves(proj0))
    changed = []
    for ptr in orig_leaves:
        if orig_leaves[ptr] != proj_leaves.get(ptr):
            changed.append({"pointer": ptr,
                            "original": orig_leaves[ptr],
                            "projected": proj_leaves[ptr]})

    # would-be per-item file exactly as upstream json.dump(item, f, indent=2)
    would_be = json.dumps(proj0, indent=2)
    blob = would_be.encode("utf-8")  # ensure_ascii default True

    # token occurrence codepoint offsets inside the whole original text
    occ = []
    for tokname in order:
        tok = tokens[tokname]
        start = 0
        while True:
            i = raw_text.find(tok, start)
            if i < 0:
                break
            occ.append((tokname, i))
            start = i + 1
    in_item0 = [(t, i) for t, i in occ if 4 <= i < 803]

    report[name] = {
        "applied": applied,
        "projected_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "parsed_task_count": len(projected),
        "index0_changed": changed,
        "index0_pointer_in_document": "/0/start_url",
        "would_be_file_sha256": hashlib.sha256(blob).hexdigest(),
        "would_be_text_len": len(blob),
        "would_be_first_line": would_be.split("\n")[0],
        "would_be_last_char": repr(would_be[-1]),
        "task0_occurrences_codepoint_offsets": in_item0,
        "proj0": proj0,
    }

json.dump(report, open(sys.argv[1], "w"), indent=2, ensure_ascii=False)
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "proj0"} for k, v in report.items()},
                 indent=2, ensure_ascii=False))

"""Independent __GITLAB__ token census over the pinned raw r28 test.raw.json.

Reads a file ONCE into bytes, authenticates sha256, decodes utf-8, then uses a
self-contained JSON scanner over that retained text so that every string token
carries its exact codepoint span in the ORIGINAL serialized text plus its
decoded value. No upstream code is imported or executed.
"""

import hashlib
import json
import sys

PATH = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
TOKEN = "__GITLAB__"
EXPECTED_SHA = "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"
PROFILES = {
    "distinct_origins": "http://gitlab.invalid:10101",
    "path_prefix": "http://gitlab.invalid:10201/prefix",
    "trailing_slash_sensitivity": "http://gitlab.invalid:10301/",
}

bytes_read = open(PATH, "rb").read()
sha = hashlib.sha256(bytes_read).hexdigest()
if sha != EXPECTED_SHA:
    print("FATAL snapshot_tampered", sha)
    sys.exit(2)
text = bytes_read.decode("utf-8")

records = []  # (path, role, raw_start, raw_end, decoded, kind)
WS = " \t\r\n"


def decode_string(i):
    """Decode JSON string starting at text[i]=='"' (i points at the quote).

    Returns (value, end_index_after_closing_quote). Handles \\uXXXX including
    surrogate pairs and the standard two-character escapes represented in the
    serialized text. Records raw span separately by the caller.
    """
    assert text[i] == '"'
    i += 1
    out = []
    while True:
        c = text[i]
        if c == '"':
            return "".join(out), i + 1
        if c == "\\":
            e = text[i + 1]
            if e == "u":
                cp = int(text[i + 2:i + 6], 16)
                i += 6
                if 0xD800 <= cp <= 0xDBFF and text[i:i + 2] == "\\u":
                    lo = int(text[i + 2:i + 6], 16)
                    if 0xDC00 <= lo <= 0xDFFF:
                        cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00)
                        i += 6
                out.append(chr(cp))
                continue
            simple = {'"': '"', "\\": "\\", "/": "/", "b": "\b",
                      "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
            if e not in simple:
                raise ValueError("bad escape at %d" % i)
            out.append(simple[e])
            i += 2
            continue
        out.append(c)
        i += 1


def skip_ws(i):
    while i < len(text) and text[i] in WS:
        i += 1
    return i


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
            raw_start = i
            key, i = decode_string(i)
            records.append((path + [("K", key)], "key", raw_start, i, key, "key"))
            i = skip_ws(i)
            assert text[i] == ":"
            i = parse_value(i + 1, path + [("K", key)])
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
        n = 0
        while True:
            i = parse_value(i, path + [("I", n)])
            n += 1
            i = skip_ws(i)
            if text[i] == ",":
                i += 1
                continue
            assert text[i] == "]"
            return i + 1
    if c == '"':
        start = i
        val, i = decode_string(i)
        records.append((path, "value", start, i, val, "string"))
        return i
    for lit in ("true", "false", "null"):
        if text.startswith(lit, i):
            return i + len(lit)
    j = i
    while j < len(text) and text[j] in "-+.eE0123456789":
        j += 1
    if j == i:
        raise ValueError("bad value at %d: %r" % (i, text[i:i + 20]))
    return j


end = parse_value(0, [])
assert skip_ws(end) == len(text), ("trailing bytes", end, len(text))

# Independent literal count straight from retained text.
literal_total = text.count(TOKEN)

# Walk the scanner records: classify occurrences.
occ = []           # literal occurrences inside the raw serialized slice of a string
decoded_occ = []   # occurrences inside the decoded value
key_hits = []
escaped_only = []  # decoded occurrences not present literally in the raw slice
for path, role, rs, re_, val, kind in records:
    raw_slice = text[rs:re_]
    raw_n = raw_slice.count(TOKEN)
    dec_n = val.count(TOKEN)
    if raw_n:
        idx = 0
        while True:
            p = raw_slice.find(TOKEN, idx)
            if p < 0:
                break
            occ.append({"path": path, "role": role, "span": [rs + p, rs + p + len(TOKEN)],
                        "decoded_span": None})
            idx = p + 1
    if dec_n:
        dstart = 0
        while True:
            p = val.find(TOKEN, dstart)
            if p < 0:
                break
            decoded_occ.append({"path": path, "role": role, "decoded_span": [p, p + len(TOKEN)]})
            dstart = p + 1
    if raw_n != dec_n:
        escaped_only.append({"path": path, "raw_n": raw_n, "decoded_n": dec_n})
    if role == "key" and TOKEN in val:
        key_hits.append(path)

# Attach decoded span to raw occurrences only when multiplicities line up and
# the raw slice literally contains the token in the same order; otherwise mark
# unmapped rather than guessing.
by_slice = {}
for o in occ:
    by_slice.setdefault((tuple(map(str, o["path"])), o["role"]), []).append(o)
for rec in records:
    key = (tuple(map(str, rec[0])), rec[1])
    if key in by_slice and text[rec[2]:rec[3]].count(TOKEN) == rec[4].count(TOKEN):
        for o in by_slice[key]:
            off = o["span"][0] - (rec[2] + 1)
            o["decoded_span"] = [off, off + len(TOKEN)]


def pointer(path):
    out = ""
    for kind, v in path:
        out += "/" + (str(v) if kind == "K" else str(v))
    return out or ""


def task_of(path):
    # path starts with I(task_index)
    if path and path[0][0] == "I":
        return path[0][1]
    return None


data = json.loads(text)

# Scanner fidelity: every decoded string value from the hand scanner must equal
# the corresponding value from json.loads at the same logical pointer, in order.
scanner_values = [(pointer(p), v) for p, role, rs, re_, v, kind in records if role == "value"]
json_values = []


def walk_values(o, ptr):
    if isinstance(o, dict):
        for k, v in o.items():
            walk_values(v, ptr + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk_values(v, ptr + "/" + str(i))
    elif isinstance(o, str):
        json_values.append((ptr or "", o))


walk_values(data, "")
fidelity_ok = scanner_values == json_values

summary = {
    "sha256": sha,
    "bytes": len(bytes_read),
    "codepoints": len(text),
    "pure_single_byte_utf8": len(bytes_read) == len(text),
    "tasks": len(data),
    "distinct_task_ids": len({d["task_id"] for d in data}),
    "literal_total": literal_total,
    "scanner_string_slice_occurrences": len(occ),
    "decoded_leaf_occurrences": len(decoded_occ),
    "key_occurrences": len(key_hits),
    "escaped_only_leaves": escaped_only,
    "scanner_fidelity_vs_json_loads": fidelity_ok,
    "scanner_value_count": len(scanner_values),
    "json_string_leaf_count": len(json_values),
}

# Per occurrence provenance rows.
rows = []
for o in occ:
    ti = task_of(o["path"])
    rows.append({
        "task_index": ti,
        "task_id": data[ti]["task_id"] if ti is not None else None,
        "pointer": pointer(o["path"]),
        "field": ".".join(str(v) for k, v in o["path"] if k == "K"),
        "span": o["span"],
        "decoded_offset_in_value": o["decoded_span"],
    })
rows.sort(key=lambda r: r["span"][0])

print(json.dumps(summary, indent=1))
print("DUPLICATE_SPANS", len(rows) != len({tuple(r["span"]) for r in rows}))
print("FIRST5")
for r in rows[:5]:
    print(json.dumps(r, ensure_ascii=False))
print("LAST5")
for r in rows[-5:]:
    print(json.dumps(r, ensure_ascii=False))
print("TASKS_WITH_TOKEN", len({r["task_index"] for r in rows}))
print("TASK_ID_EQ_INDEX_ALL_ROWS", all(r["task_index"] == r["task_id"] for r in rows))
print("FIELD_COUNTS", json.dumps({k: sum(1 for r in rows if r["field"] == k)
                                  for k in sorted({r["field"] for r in rows})}))
print("POINTER_COUNTS")
import collections
for k, v in sorted(collections.Counter(r["pointer"] for r in rows).items()):
    print(" ", k, v)
print("OCCURRENCES_PER_TASK_HIST")
hist = collections.Counter(collections.Counter(r["task_index"] for r in rows).values())
print(" ", {n: sum(1 for t, c in collections.Counter(r["task_index"] for r in rows).items() if c == n)
            for n in sorted(hist)})
print("TOTAL_CODEPOINT_DELTAS", {n: len(v) - len(TOKEN) for n, v in PROFILES.items()})
for n, v in PROFILES.items():
    d = len(v) - len(TOKEN)
    print("PROFILE", n, "replacement_len", len(v), "delta", d,
          "projected_codepoints", len(text) + d * len(rows),
          "first_new_span", [rows[0]["span"][0], rows[0]["span"][0] + len(v)],
          "last_new_span_start", rows[-1]["span"][0] + d * (len(rows) - 1))
print("PROFILE_VALUES_CONTAIN_KNOWN_TOKEN",
      any(TOKEN in v or any(t in v for t in
          ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
           "__WIKIPEDIA__", "__MAP__"]) for v in PROFILES.values()))
print("TOKEN_SUBSTRING_OF_OTHER_TOKEN",
      any(TOKEN in t and t != TOKEN for t in
          ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
           "__WIKIPEDIA__", "__MAP__"]))

with open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/"
          "KengakuR28.R29TokenGitlab-2/occurrences.json", "w") as f:
    json.dump(rows, f, indent=1, ensure_ascii=False)
print("WROTE occurrences.json rows", len(rows))

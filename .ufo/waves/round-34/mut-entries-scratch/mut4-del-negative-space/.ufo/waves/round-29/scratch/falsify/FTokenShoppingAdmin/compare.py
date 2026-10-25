#!/usr/bin/env python3
"""Independent provenance table from raw bytes; compare with instrument --json output.

No production instrument source is read or imported.
"""
import bisect
import json
import sys

BASE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures"
RAW = BASE + "/r28/webarena/config_files/test.raw.json"
INST = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FTokenShoppingAdmin/instrument.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
          "__WIKIPEDIA__", "__MAP__"]

t = open(RAW, "rb").read().decode("utf-8")
n = len(t)


class P:
    def __init__(self):
        self.i = 0

    def ws(self):
        while self.i < n and t[self.i] in " \t\r\n":
            self.i += 1

    def string(self):
        # t[self.i] == '"'
        assert t[self.i] == '"', ("quote", self.i, t[self.i:self.i + 20])
        start = self.i
        self.i += 1
        cs = self.i
        while True:
            c = t[self.i]
            if c == "\\":
                self.i += 2
            elif c == '"':
                break
            else:
                self.i += 1
        ce = self.i
        self.i += 1
        return cs, ce, json.loads(t[start:self.i])

    def value(self, path, spans, keys):
        self.ws()
        c = t[self.i]
        if c == '"':
            cs, ce, val = self.string()
            spans.append((cs, ce, path, val))
            return
        if c == "{":
            self.i += 1
            self.ws()
            if t[self.i] == "}":
                self.i += 1
                return
            while True:
                self.ws()
                kcs, kce, key = self.string()
                keys.append((kcs, kce, key))
                self.ws()
                assert t[self.i] == ":"
                self.i += 1
                self.value(path + [str(key)], spans, keys)
                self.ws()
                if t[self.i] == ",":
                    self.i += 1
                    continue
                assert t[self.i] == "}"
                self.i += 1
                return
        if c == "[":
            self.i += 1
            self.ws()
            if t[self.i] == "]":
                self.i += 1
                return
            idx = 0
            while True:
                self.value(path + [str(idx)], spans, keys)
                idx += 1
                self.ws()
                if t[self.i] == ",":
                    self.i += 1
                    continue
                assert t[self.i] == "]"
                self.i += 1
                return
        # scalar
        while self.i < n and t[self.i] not in ",]} \t\r\n":
            self.i += 1


p = P()
spans = []
keys = []
p.ws()
p.value([], spans, keys)
p.ws()
print("parser_consumed", p.i, "of", n, "ok", p.i == n)
print("string_value_spans", len(spans), "key_spans", len(keys))

# token occurrences from raw text, attributed to containing value span
starts = [s[0] for s in spans]
occ = []
for tok in TOKENS:
    pos = t.find(tok)
    while pos != -1:
        k = bisect.bisect_right(starts, pos) - 1
        cs, ce, path, val = spans[k]
        assert cs <= pos and pos + len(tok) <= ce, (tok, pos, cs, ce)
        # is the token literally inside the decoded value? token is ASCII, value
        # may contain escapes before pos; locate within val by raw containment
        assert tok in val, (tok, pos, path)
        ptr = "/" + "/".join(path)
        segs = []
        for x in path[1:]:
            if x.isdigit():
                segs[-1] = segs[-1] + "[]"
            else:
                segs.append(x)
        occ.append({
            "token": tok,
            "offset": pos,
            "json_pointer": ptr,
            "task_index": int(path[0]),
            "path_template": ".".join(segs),
        })
        pos = t.find(tok, pos + len(tok))
occ.sort(key=lambda o: (o["offset"], o["token"]))
print("value occurrence total", len(occ))
from collections import Counter
print("value occurrences by token", json.dumps(dict(sorted(Counter(o["token"] for o in occ).items()))))
print("token occurrences inside keys", sum(1 for pos in
      [t.find(tok) for tok in TOKENS] if False))
# explicit key check
keyhits = [(cs, ce, k) for cs, ce, k in keys if any(tok in k for tok in TOKENS)]
print("keys carrying tokens", len(keyhits), keyhits[:3])

# compare with instrument provenance
d = json.load(open(INST))
ins = d["occurrence_provenance"]
print("\ninstrument occurrence entries", len(ins))
mine = {}
for o in occ:
    mine.setdefault(o["token"], []).append(o)
inst_by_tok = {}
for o in ins:
    inst_by_tok.setdefault(o["token"], []).append(o)

bad = 0
for tok in TOKENS:
    a = mine.get(tok, [])
    b = inst_by_tok.get(tok, [])
    ma = [(o["offset"], o["json_pointer"], o["task_index"], o["path_template"]) for o in a]
    mb = [(o["original_input_codepoint_offset"], o["json_pointer"], o["task_index"],
           o["path_template"]) for o in b]
    extra = [x for x in ma if x not in set(mb)]
    missing = [x for x in mb if x not in set(ma)]
    print("TOKEN", tok, "mine", len(ma), "instrument", len(mb),
          "extra_in_mine", len(extra), "missing_in_mine", len(missing),
          "roles", sorted({o["string_role"] for o in b}))
    if extra:
        print("  EXTRA", extra[:5])
        bad += 1
    if missing:
        print("  MISSING", missing[:5])
        bad += 1

# SHOPPING_ADMIN specific: offsets sorted, per pointer, per template
sa = inst_by_tok["__SHOPPING_ADMIN__"]
print("\nSHOPPING_ADMIN instrument count", len(sa))
print("  templates", json.dumps(dict(sorted(Counter(o["path_template"] for o in sa).items()))))
print("  distinct tasks", len({o["task_index"] for o in sa}))
print("  offset monotonic", all(sa[i]["original_input_codepoint_offset"] < sa[i + 1]["original_input_codepoint_offset"] for i in range(len(sa) - 1)))
print("  first", sa[0])
print("  last", sa[-1])

# per-profile task-level comparison of changed leaves carrying SHOPPING_ADMIN
print("\n== per-profile SHOPPING_ADMIN task-level leaf comparison ==")
for pname, prof in d["profiles"].items():
    mine_leaves = Counter()
    mine_tasks = set()
    mine_by_ptr = Counter()
    mine_token_sets = Counter()
    badrows = []
    for idx, task in enumerate(prof["tasks"]):
        for leaf in task["changed_leaves"]:
            toks = leaf["tokens"]
            mine_token_sets[tuple(sorted(toks))] += 1
            if "__SHOPPING_ADMIN__" in toks:
                mine_leaves[leaf["json_pointer"]] += 1
                mine_tasks.add(idx)
                mine_by_ptr[leaf["path_template"]] += 1
                # verify projected value equals profile value
                if leaf["projected"] != prof["values"]["SHOPPING_ADMIN"] and \
                   leaf["original"] == "__SHOPPING_ADMIN__":
                    badrows.append((idx, leaf["json_pointer"], leaf["original"], leaf["projected"]))
    print(pname,
          "instrument_changed_leaves_with_SA", len(mine_leaves),
          "distinct_tasks", len(mine_tasks),
          "by_template", json.dumps(dict(sorted(mine_by_ptr.items()))),
          "token_set_shapes", json.dumps({"+".join(k): v for k, v in sorted(mine_token_sets.items())}),
          "bad_projection_rows", len(badrows))
    if badrows:
        print("  BAD", badrows[:5])
print("\nTOTAL mismatched fields above:", bad)

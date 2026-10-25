"""Independent read-only census of exactly one token: __SHOPPING__.

Scope: one pinned raw serialized file, one literal token, three frozen synthetic
profiles. No imports of lane production code; no writes outside this scratch dir.
All offsets are Unicode codepoints (file is verified ASCII, cp == byte here).
"""
import hashlib
import json
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = LANE + "/plans/fixtures/r29/profiles.json"
TOKEN = "__SHOPPING__"
TOKENS6 = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


class SpanParser:
    """JSON parser that records raw char spans of every string literal and its path."""

    def __init__(self, s):
        self.s = s
        self.n = len(s)
        self.pos = 0
        self.literals = []   # dict: path, role, key, start, end, decoded
        self.top = []        # (start, end) of each top-level array element
        self.keys = []
        self.err = None

    def ws(self):
        s, n = self.s, self.n
        while self.pos < n and s[self.pos] in " \t\r\n":
            self.pos += 1

    def fail(self, msg):
        if self.err is None:
            self.err = "%s at %d" % (msg, self.pos)
        raise ValueError(self.err)

    def parse(self):
        self.ws()
        if self.pos >= self.n or self.s[self.pos] != "[":
            self.fail("top-level is not array")
        self.pos += 1
        self.ws()
        idx = 0
        if self.pos < self.n and self.s[self.pos] == "]":
            self.pos += 1
        else:
            while True:
                start = self.pos
                self.value("[%d]" % idx, "[%d]" % idx, None, top_index=idx)
                end = self.pos
                self.top.append((start, end, idx))
                idx += 1
                self.ws()
                if self.pos >= self.n:
                    self.fail("eof in array")
                c = self.s[self.pos]
                if c == ",":
                    self.pos += 1
                    self.ws()
                    continue
                if c == "]":
                    self.pos += 1
                    break
                self.fail("bad array separator")
        self.ws()
        if self.pos != self.n:
            self.fail("trailing garbage")
        return self

    def value(self, path, keypath, key, top_index=None):
        self.ws()
        s = self.s
        if self.pos >= self.n:
            self.fail("eof in value")
        c = s[self.pos]
        if c == "{":
            self.pos += 1
            self.ws()
            if self.pos < self.n and s[self.pos] == "}":
                self.pos += 1
                return
            while True:
                self.ws()
                if self.pos >= self.n or s[self.pos] != '"':
                    self.fail("expected key")
                kstart = self.pos + 1
                kvalue, kend = self.string_literal()
                self.literals.append(dict(path=keypath, role="key", key=kvalue,
                                          start=kstart, end=kend, decoded=kvalue,
                                          top=top_index))
                self.keys.append((keypath, kvalue))
                self.ws()
                if self.pos >= self.n or s[self.pos] != ":":
                    self.fail("expected colon")
                self.pos += 1
                child = path + "." + kvalue
                self.value(child, child, kvalue, top_index=top_index)
                self.ws()
                if self.pos >= self.n:
                    self.fail("eof in object")
                c = s[self.pos]
                if c == ",":
                    self.pos += 1
                    continue
                if c == "}":
                    self.pos += 1
                    return
                self.fail("bad object separator")
        elif c == "[":
            self.pos += 1
            self.ws()
            i = 0
            if self.pos < self.n and s[self.pos] == "]":
                self.pos += 1
                return
            while True:
                self.value("%s[%d]" % (path, i), "%s[%d]" % (path, i), None,
                           top_index=top_index)
                i += 1
                self.ws()
                if self.pos >= self.n:
                    self.fail("eof in list")
                c = s[self.pos]
                if c == ",":
                    self.pos += 1
                    continue
                if c == "]":
                    self.pos += 1
                    return
                self.fail("bad list separator")
        elif c == '"':
            start = self.pos + 1
            decoded, end = self.string_literal()
            self.literals.append(dict(path=path, role="value", key=key,
                                      start=start, end=end, decoded=decoded,
                                      top=top_index))
        else:
            m = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null")
            mm = m.match(s, self.pos)
            if not mm:
                self.fail("bad scalar")
            self.pos = mm.end()

    def string_literal(self):
        """At opening quote; return (decoded_value, content_end_exclusive)."""
        s, n = self.s, self.n
        i = self.pos + 1
        while i < n:
            ch = s[i]
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                raw = s[self.pos:i + 1]
                decoded = json.loads(raw)
                self.pos = i + 1
                return decoded, i
            i += 1
        self.fail("unterminated string")


def raw_offsets(text, token):
    out = []
    i = text.find(token)
    while i != -1:
        out.append(i)
        i = text.find(token, i + 1)
    return out


def decoded_map(raw_content):
    """Map decoded codepoints to raw indices for one string literal content.

    Returns (decoded_string, list raw_index_per_decoded_char, list raw_span_end)
    """
    out = []
    rmap = []
    rend = []
    i = 0
    n = len(raw_content)
    while i < n:
        c = raw_content[i]
        if c == "\\":
            esc = raw_content[i + 1]
            if esc == "u":
                cp = int(raw_content[i + 2:i + 6], 16)
                if 0xD800 <= cp <= 0xDBFF:
                    lo = int(raw_content[i + 8:i + 12], 16)
                    ch = chr(0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00))
                    out.append(ch)
                    rmap.append(i)
                    rend.append(i + 12)
                    i += 12
                    continue
                ch = chr(cp)
                out.append(ch)
                rmap.append(i)
                rend.append(i + 6)
                i += 6
                continue
            mapping = {'"': '"', "\\": "\\", "/": "/", "b": "\b",
                       "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
            if esc not in mapping:
                raise ValueError("bad escape %r" % esc)
            out.append(mapping[esc])
            rmap.append(i)
            rend.append(i + 2)
            i += 2
            continue
        out.append(c)
        rmap.append(i)
        rend.append(i + 1)
        i += 1
    return "".join(out), rmap, rend


def main():
    rb = open(RAW, "rb").read()
    text = rb.decode("utf-8")
    print("== input ==")
    print("raw_bytes", len(rb))
    print("raw_sha256", sha(rb))
    print("raw_codepoints", len(text))
    print("pure_ascii", all(ord(c) < 128 for c in text))
    print("utf8_bom", rb[:3] == b"\xef\xbb\xbf")

    raw_occ = raw_offsets(text, TOKEN)
    admin_occ = raw_offsets(text, "__SHOPPING_ADMIN__")
    print("raw_occurrences_exact_token", len(raw_occ))
    print("raw_occurrences_shopping_admin", len(admin_occ))
    print("raw_occurrences_SHOPPING_upper_any",
          len(raw_offsets(text, "SHOPPING")))
    print("raw_occurrences_shopping_lower_any",
          len(raw_offsets(text, "shopping")))

    parser = SpanParser(text).parse()
    print("parse_error", parser.err)
    print("top_level_elements", len(parser.top))
    print("string_literals_total", len(parser.literals))
    print("key_literals", sum(1 for l in parser.literals if l["role"] == "key"))

    data = json.loads(text)
    print("decoded_items", len(data))
    ids = [d["task_id"] for d in data]
    print("distinct_ids", len(set(ids)))
    print("index_equals_task_id_all", all(i == v for i, v in enumerate(ids)))

    # Membership checks: every raw occurrence lies inside exactly one literal.
    occ_in_literal = [0] * len(raw_occ)
    lit_stats = []
    for li, lit in enumerate(parser.literals):
        content = text[lit["start"]:lit["end"]]
        nraw = content.count(TOKEN)
        ndec = lit["decoded"].count(TOKEN)
        if nraw or ndec:
            has_escape = "\\" in content
            lit_stats.append((li, lit["path"], lit["role"], lit["key"],
                              nraw, ndec, has_escape,
                              lit["decoded"] == content, lit["top"]))
        if nraw:
            base = lit["start"]
            i = content.find(TOKEN)
            while i != -1:
                abs_off = base + i
                j = raw_occ.index(abs_off) if abs_off in raw_occ else -1
                if j >= 0:
                    occ_in_literal[j] += 1
                i = content.find(TOKEN, i + 1)
    print("occurrences_matched_inside_literals", sum(occ_in_literal))
    print("occurrences_outside_literals", len(raw_occ) - sum(occ_in_literal))
    print("literals_containing_token", len(lit_stats))
    print("literals_with_escapes_containing_token",
          sum(1 for r in lit_stats if r[6]))
    print("literals_raw_equals_decoded_containing_token",
          sum(1 for r in lit_stats if r[7]))

    # Per-occurrence provenance (decoded offsets via escape map).
    occ = []
    for li, path, role, key, nraw, ndec, has_esc, raweq, top in lit_stats:
        lit = parser.literals[li]
        content = text[lit["start"]:lit["end"]]
        dec, rmap, rend = decoded_map(content) if has_esc else (
            lit["decoded"], list(range(len(content))), [i + 1 for i in range(len(content))])
        if dec != lit["decoded"]:
            raise SystemExit("decode mapping mismatch at literal %d" % li)
        pos = dec.find(TOKEN)
        n = 0
        while pos != -1:
            n += 1
            raw_start = lit["start"] + rmap[pos]
            value = lit["decoded"]
            cls = "url_start" if re.match(r"^https?://", value) else (
                "token_only" if value == TOKEN else "embedded_text")
            occ.append(dict(path=path, role=role, key=key, top=top,
                            raw_off=raw_start,
                            decoded_off_in_value=pos,
                            occurrence_in_value=n,
                            value_class=cls,
                            value_len=len(value),
                            value_prefix=value[max(0, pos - 30):pos],
                            value_suffix=value[pos + len(TOKEN):pos + len(TOKEN) + 40],
                            has_escape=has_esc, raw_equals_decoded=raweq))
            pos = dec.find(TOKEN, pos + 1)
    print("provenance_occurrences", len(occ))

    # Raw offsets consistency: occurrence order matches decoded walk order.
    print("provenance_raw_offsets_sorted",
          [o["raw_off"] for o in occ] == sorted(o["raw_off"] for o in occ))
    raw_set = set(raw_occ)
    prov_set = {o["raw_off"] for o in occ}
    print("raw_vs_provenance_offset_diff", len(raw_set ^ prov_set))
    print("provenance_duplicate_offsets",
          len(occ) - len(prov_set))

    # Units.
    affected_tasks = sorted({o["top"] for o in occ})
    affected_paths = sorted({o["path"] for o in occ})
    print("units_raw_occurrences", len(occ))
    print("units_string_literals_containing", len(lit_stats))
    print("units_distinct_paths", len(affected_paths))
    print("units_tasks_affected", len(affected_tasks))
    print("units_decoded_values_with_2plus",
          sum(1 for li, path, role, key, nraw, ndec, he, re_, top in lit_stats if ndec > 1))

    # Aggregates by path (path -> occurrences, literals, value classes).
    agg = {}
    for o in occ:
        a = agg.setdefault(o["path"], dict(occ=0, vals=set(), classes={}, tasks=set(),
                                           keys=set(), role=o["role"], esc=0))
        a["occ"] += 1
        a["vals"].add(o["value_class"])
        a["classes"][o["value_class"]] = a["classes"].get(o["value_class"], 0) + 1
        a["tasks"].add(o["top"])
        a["keys"].add(o["key"])
        a["esc"] += 1 if o["has_escape"] else 0
    print("\n== path aggregates ==")
    for p in sorted(agg):
        a = agg[p]
        print("PATH", p, "occ", a["occ"], "tasks", len(a["tasks"]),
              "classes", json.dumps(a["classes"], sort_keys=True),
              "keys", sorted(a["keys"]), "escaped_occ", a["esc"])
    print("\n== class totals (occurrence units) ==")
    ct = {}
    for o in occ:
        ct[o["value_class"]] = ct.get(o["value_class"], 0) + 1
    print(json.dumps(ct, sort_keys=True))

    print("\n== affected tasks: index/task_id/occurrences/leaf-count/span ==")
    per_task = {}
    for o in occ:
        per_task.setdefault(o["top"], []).append(o)
    for t in affected_tasks:
        row = per_task[t]
        leaves = {o["path"] for o in row}
        start, end, _ = parser.top[t]
        print("TASK", t, "task_id", ids[t], "occ", len(row),
              "leaves", len(leaves), "raw_span", start, end)

    # tasks whose index != task_id inside the affected set (guard, not global claim)
    print("affected_index_ne_taskid",
          [(t, ids[t]) for t in affected_tasks if t != ids[t]])

    # example leaf values (public fixture data), first occurrence per class
    print("\n== examples ==")
    seen = set()
    for o in occ:
        k = (o["path"], o["value_class"])
        if k in seen:
            continue
        seen.add(k)
        print("EX", o["path"], "|class", o["value_class"],
              "|value_len", o["value_len"],
              "|pre", json.dumps(o["value_prefix"]),
              "|post", json.dumps(o["value_suffix"]),
              "|cp", o["raw_off"])

    # Non-token same-word occurrences (case-insensitive word), to separate metadata.
    word_re = re.compile(r"(?<![A-Za-z_])shopping(?![A-Za-z_])")
    wcount = 0
    ls = text.lower()
    for m in word_re.finditer(ls):
        wcount += 1
    print("\nlowercase_word_shopping_occurrences", wcount)
    print("literal_token_inside_lowercase_word", TOKEN.lower() in "shopping")

    # Profiles.
    prof_bytes = open(PROFILES, "rb").read()
    profiles = json.loads(prof_bytes.decode("utf-8"))
    print("\n== profiles ==")
    print("profiles_sha256", sha(prof_bytes))
    print("profile_names", list(profiles))
    print("profile_duplicate_value_sets",
          len({tuple(sorted(p["values"].items())) for p in profiles.values()}))

    dec_leaves = [l for l in parser.literals if l["role"] == "value"]
    for pname in profiles:
        p = profiles[pname]
        vals = p["values"]
        missing = [t for t in TOKENS6 if t not in vals]
        print("PROFILE", pname, "missing_keys", missing,
              "value_types", sorted({type(v).__name__ for v in vals.values()}))
        v = vals["SHOPPING"]
        delta = len(v) - len(TOKEN)
        print("  value", json.dumps(v), "value_cp", len(v),
              "delta_per_occurrence", delta)
        # cascade guard: values must not introduce any of the six tokens
        print("  value_contains_any_token",
              [t for t in TOKENS6 if "__%s__" % t in v])
        # applying prior-order replacements must not change this token count
        pre = text
        for t in ("GITLAB", "REDDIT"):
            pre = pre.replace("__%s__" % t, vals[t])
        print("  token_count_after_prior_GITLAB_REDDIT", pre.count(TOKEN),
              "prior_values_introduce_token",
              any(TOKEN in vals[t] for t in ("GITLAB", "REDDIT")))

        # single-token substitution only (NOT the canonical six-token projection)
        projected = text.replace(TOKEN, v)
        print("  projected_cp", len(projected),
              "delta_total", len(projected) - len(text),
              "occ_after", projected.count(TOKEN))
        pd = json.loads(projected)
        print("  projected_items", len(pd),
              "ids_equal", [d["task_id"] for d in pd] == ids)
        pbad = [i for i, d in enumerate(pd) if d["task_id"] != ids[i]]
        print("  projected_id_mismatches", pbad)

        # per-task span shifts and leaf equivalence
        starts = [s for s, e, i in parser.top]
        ends = [e for s, e, i in parser.top]
        exp_starts = []
        running = 0
        occ_before = {}
        for o in occ:
            occ_before[o["top"]] = occ_before.get(o["top"], 0) + 1
        shift = 0
        span_ok = True
        for t in range(len(starts)):
            exp_starts.append(starts[t] + shift)
            shift += occ_before.get(t, 0) * delta
        psp = SpanParser(projected).parse()
        pstarts = [s for s, e, i in psp.top]
        print("  projected_task_spans_forward_formula_match",
              pstarts == exp_starts,
              "task_count", len(pstarts))
        print("  projected_last_offset", pstarts[-1],
              "base_last_offset", starts[-1])
        # task-local leaf equivalence: each leaf decoded.replace(token, v)
        mism = 0
        leaf_checks = 0
        for i, li, lj in zip(range(len(data)), [l for l in parser.literals if l["role"] == "value"],
                             [l for l in psp.literals if l["role"] == "value"]):
            pass
        # explicit per-task equivalence by re-parsing each projected top element
        for t, (s, e, idx) in enumerate(parser.top):
            base_obj = data[t]
            proj_obj = pd[t]
            base_flat = []
            def flat(x, path=""):
                if isinstance(x, dict):
                    for k in x:
                        flat(x[k], path + "." + k)
                elif isinstance(x, list):
                    for j, y in enumerate(x):
                        flat(y, path + "[%d]" % j)
                else:
                    base_flat.append((path, x))
            flat(base_obj)
            proj_flat = []
            def flat2(x, path=""):
                if isinstance(x, dict):
                    for k in x:
                        flat2(x[k], path + "." + k)
                elif isinstance(x, list):
                    for j, y in enumerate(x):
                        flat2(y, path + "[%d]" % j)
                else:
                    proj_flat.append((path, x))
            flat2(proj_obj)
            if len(base_flat) != len(proj_flat):
                mism += 1
                continue
            for (bp, bv), (pp, pv) in zip(base_flat, proj_flat):
                if bp != pp:
                    mism += 1
                    continue
                if isinstance(bv, str):
                    expect = bv.replace(TOKEN, v)
                else:
                    expect = bv
                if expect != pv:
                    mism += 1
            leaf_checks += 1
        print("  per_task_leaf_equivalence_mismatch_tasks", mism,
              "tasks_checked", leaf_checks)
        # changed leaf counts per task/profile
        ch_leaves = 0
        ch_tasks = 0
        for t, (s, e, idx) in enumerate(parser.top):
            n = sum(1 for l in parser.literals
                    if l["role"] == "value" and l["top"] == t
                    and TOKEN in l["decoded"])
            if n:
                ch_tasks += 1
                ch_leaves += n
        print("  changed_leaves", ch_leaves, "changed_tasks", ch_tasks)
        # projected occurrences of the other five tokens (must be unchanged)
        print("  other_token_counts_after",
              {t: projected.count("__%s__" % t) for t in TOKENS6 if t != "SHOPPING"})

    print("\n== duplicate token occurrences within one leaf ==")
    for li, path, role, key, nraw, ndec, has_esc, raweq, top in lit_stats:
        if ndec > 1:
            print("MULTI", path, "task", top, "occ", ndec,
                  "value_len", len(parser.literals[li]["decoded"]))
    print("\n== done ==")


if __name__ == "__main__":
    main()

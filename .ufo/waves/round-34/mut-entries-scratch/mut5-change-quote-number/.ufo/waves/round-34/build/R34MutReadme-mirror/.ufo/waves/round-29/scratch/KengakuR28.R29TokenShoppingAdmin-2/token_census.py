#!/usr/bin/env python3
"""Independent, read-only census of one literal token in a raw JSON text.

No production imports. Recursive-descent parser records the raw codepoint span
and exact JSON path of every string literal, then cross-checks each decoded
literal against a separate json.loads() walk of the same text.
"""
import json
import re
import sys
from collections import Counter

TOKEN = "__SHOPPING_ADMIN__"


class Parser:
    def __init__(self, text):
        self.t = text
        self.i = 0
        self.n = len(text)
        self.strings = []   # (path, is_key, start, end, literal, decoded)
        self.fail = None

    def ws(self):
        t, n = self.t, self.n
        while self.i < n and t[self.i] in " \t\r\n":
            self.i += 1

    def string(self):
        start = self.i
        assert self.t[self.i] == '"'
        self.i += 1
        while self.i < self.n:
            ch = self.t[self.i]
            if ch == "\\":
                self.i += 2
                continue
            if ch == '"':
                self.i += 1
                lit = self.t[start:self.i]
                return start, self.i, lit, json.loads(lit)
            self.i += 1
        raise ValueError("unterminated string")

    def value(self, path):
        self.ws()
        c = self.t[self.i]
        if c == '"':
            start, end, lit, dec = self.string()
            self.strings.append((tuple(path), False, start, end, lit, dec))
            return dec
        if c == "{":
            self.i += 1
            obj = {}
            while True:
                self.ws()
                if self.t[self.i] == "}":
                    self.i += 1
                    return obj
                kstart, kend, klit, kdec = self.string()
                self.strings.append((tuple(path) + (kdec,), True, kstart, kend, klit, kdec))
                self.ws()
                assert self.t[self.i] == ":"
                self.i += 1
                obj[kdec] = self.value(tuple(path) + (kdec,))
                self.ws()
                if self.t[self.i] == ",":
                    self.i += 1
                    continue
                assert self.t[self.i] == "}"
                self.i += 1
                return obj
        if c == "[":
            self.i += 1
            arr = []
            while True:
                self.ws()
                if self.t[self.i] == "]":
                    self.i += 1
                    return arr
                arr.append(self.value(tuple(path) + (len(arr),)))
                self.ws()
                if self.t[self.i] == ",":
                    self.i += 1
                    continue
                assert self.t[self.i] == "]"
                self.i += 1
                return arr
        j = self.i
        while j < self.n and self.t[j] not in ',]} \t\r\n':
            j += 1
        lit = self.t[self.i:j]
        self.i = j
        return json.loads(lit)

    def parse(self):
        return self.value(())


def lookup(root, path):
    cur = root
    for p in path:
        cur = cur[p]
    return cur


def main():
    raw_path = sys.argv[1]
    b = open(raw_path, "rb").read()
    text = b.decode("utf-8")
    data = json.loads(text)
    assert isinstance(data, list)

    p = Parser(text)
    parsed = p.parse()
    assert parsed == data, "recursive parser disagrees with json.loads"

    mismatch = 0
    value_strings = 0
    for path, is_key, s, e, lit, dec in p.strings:
        if is_key:
            continue
        value_strings += 1
        try:
            ref = lookup(data, path)
        except Exception:
            mismatch += 1
            continue
        if ref != dec:
            mismatch += 1

    raw_occs = []
    key_hits = []
    for path, is_key, s, e, lit, dec in p.strings:
        if TOKEN not in dec:
            continue
        rec = {
            "path": list(path),
            "path_str": "/" + "/".join(str(x) for x in path),
            "is_key": is_key,
            "raw_start": s,
            "raw_end": e,
            "decoded_len": len(dec),
            "count": dec.count(TOKEN),
            "positions_in_decoded": [m.start() for m in re.finditer(re.escape(TOKEN), dec)],
            "decoded_value": dec,
        }
        if is_key:
            key_hits.append(rec)
        else:
            raw_occs.append(rec)

    decoded_total = sum(o["count"] for o in raw_occs)
    raw_total = text.count(TOKEN)

    per_task = {}
    for o in raw_occs:
        t = o["path"][0]
        per_task.setdefault(t, {"occurrences": 0, "leaves": 0, "paths": []})
        per_task[t]["occurrences"] += o["count"]
        per_task[t]["leaves"] += 1
        per_task[t]["paths"].append(o["path_str"])

    top_field = Counter()
    shape = Counter()
    for o in raw_occs:
        path = o["path"]
        if len(path) >= 2:
            top_field[path[1]] += o["count"]
        s = []
        for x in path[1:]:
            s.append("*" if isinstance(x, int) else str(x))
        shape["/" + "/".join(s)] += o["count"]

    url_re = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")
    kinds = Counter()
    leaf_class = Counter()
    for o in raw_occs:
        v = o["decoded_value"]
        per = []
        for pos in o["positions_in_decoded"]:
            m = re.search(r"[^\s\"'<>]*$", v[:pos])
            prefix = m.group(0) if m else ""
            kind = "url" if url_re.match(prefix) else "non_url"
            per.append(kind)
            kinds[kind] += 1
        o["occurrence_kinds"] = per
        leaf_class["all_url" if set(per) == {"url"} else ("all_non_url" if set(per) == {"non_url"} else "mixed")] += 1

    for o in raw_occs:
        o["task_id"] = data[o["path"][0]].get("task_id")
        # raw literal contains token literally; record delta under each profile
        o["own_occurrence_span_codepoints"] = {"token_len": len(TOKEN)}

    out = {
        "raw_path": raw_path,
        "bytes": len(b),
        "codepoints": len(text),
        "non_ascii_codepoints": sum(1 for ch in text if ord(ch) > 127),
        "token": TOKEN,
        "token_codepoints": len(TOKEN),
        "parser_vs_jsonloads_mismatches": mismatch,
        "value_string_literals_checked": value_strings,
        "raw_literal_occurrences": raw_total,
        "decoded_value_occurrences": decoded_total,
        "raw_equals_decoded_values": raw_total == decoded_total,
        "string_value_leaves_with_token": len(raw_occs),
        "key_literal_hits": key_hits,
        "scheme_shape_kinds": dict(kinds),
        "leaf_class_by_scheme_shape": dict(leaf_class),
        "url_typed_field_occurrences": sum(
            o["count"] for o in raw_occs
            if o["path"][-1] in ("start_url", "reference_url", "url")
        ),
        "non_url_typed_field_occurrences": sum(
            o["count"] for o in raw_occs
            if o["path"][-1] not in ("start_url", "reference_url", "url")
        ),
        "top_field_occurrences": dict(top_field),
        "path_shape_occurrences": dict(shape),
        "tasks_with_token": len(per_task),
        "per_task": {str(k): v for k, v in sorted(per_task.items())},
        "occurrences": raw_occs,
        "json_valid_after_own_token_replacement": None,
    }
    proj = text.replace(TOKEN, "http://shopping-admin.invalid:10104")
    try:
        d2 = json.loads(proj)
        out["json_valid_after_own_token_replacement"] = {
            "valid": True, "tasks": len(d2), "token_remaining": proj.count(TOKEN),
        }
    except Exception as exc:  # noqa: BLE001
        out["json_valid_after_own_token_replacement"] = {"valid": False, "error": repr(exc)}

    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()

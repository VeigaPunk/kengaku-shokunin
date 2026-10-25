"""R29Task356 occurrence provenance v2: recursive-descent over the serialized
raw JSON text. Attributes every environment-token occurrence to its JSON pointer
and reports offsets in Unicode codepoints (not bytes). Read-only, stdlib only.
"""
import collections
import hashlib
import json
import os

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(ROOT, "plans/fixtures/r28/webarena/config_files/test.raw.json")
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {k: "__%s__" % k for k in ORDER}
WS = " \t\r\n"


class Scanner:
    def __init__(self, text):
        self.t = text
        self.n = len(text)
        self.strings = []      # (pointer, decoded_value, start_codepoint)

    def ws(self, i):
        while i < self.n and self.t[i] in WS:
            i += 1
        return i

    def string(self, i):
        assert self.t[i] == '"'
        j = i + 1
        while j < self.n:
            if self.t[j] == "\\":
                j += 2
                continue
            if self.t[j] == '"':
                break
            j += 1
        return json.loads(self.t[i:j + 1]), i + 1, j + 1

    def value(self, i, ptr):
        i = self.ws(i)
        c = self.t[i]
        if c == "{":
            i = self.ws(i + 1)
            if self.t[i] == "}":
                return i + 1
            while True:
                key, _, i = self.string(i)
                i = self.ws(i)
                assert self.t[i] == ":"
                i = self.value(self.ws(i + 1), ptr + "/" + key)
                i = self.ws(i)
                if self.t[i] == ",":
                    i = self.ws(i + 1)
                    continue
                assert self.t[i] == "}"
                return i + 1
        if c == "[":
            i = self.ws(i + 1)
            if self.t[i] == "]":
                return i + 1
            idx = 0
            while True:
                i = self.value(i, ptr + "/" + str(idx))
                idx += 1
                i = self.ws(i)
                if self.t[i] == ",":
                    i = self.ws(i + 1)
                    continue
                assert self.t[i] == "]"
                return i + 1
        if c == '"':
            val, start, end = self.string(i)
            self.strings.append((ptr, val, start))
            return end
        j = i
        while j < self.n and self.t[j] not in ",]}":
            j += 1
        return j


def role_of(ptr):
    parts = [p for p in ptr.split("/") if p]
    if len(parts) < 2:
        return "top"
    f = parts[1]
    if f == "start_url":
        return "start_url"
    if f == "eval":
        sub = parts[2] if len(parts) > 2 else "eval"
        if sub == "program_html":
            for tail in ("must_include", "locator", "url"):
                if tail in parts:
                    return "eval.program_html." + tail
            return "eval.program_html"
        return "eval." + sub
    return f


def main():
    with open(RAW, "rb") as f:
        b = f.read()
    text = b.decode("utf-8")
    sc = Scanner(text)
    sc.value(0, "")
    occ = []
    for ptr, val, start in sc.strings:
        for k in ORDER:
            p = val.find(TOK[k])
            while p >= 0:
                occ.append({"json_pointer": ptr, "token": k,
                            "offset_in_value_cp": p,
                            "document_cp": start + p})
                p = val.find(TOK[k], p + len(TOK[k]))
    occ.sort(key=lambda o: o["document_cp"])
    by_role = collections.Counter(role_of(o["json_pointer"]) for o in occ)
    by_token_role = collections.Counter((o["token"], role_of(o["json_pointer"]))
                                        for o in occ)
    nonzero_val = [o for o in occ if o["offset_in_value_cp"] > 0]
    out = {
        "raw_sha256": hashlib.sha256(b).hexdigest(),
        "raw_is_ascii": text.isascii(),
        "bytes": len(b), "codepoints": len(text),
        "parsed_string_leaves": len(sc.strings),
        "occurrence_count": len(occ),
        "occurrences_by_role": dict(by_role),
        "occurrences_by_token_role": {"%s|%s" % k: v for k, v in sorted(by_token_role.items())},
        "distinct_leaf_paths_with_occurrence": len({o["json_pointer"] for o in occ}),
        "occurrences_mid_value": len(nonzero_val),
        "mid_value_examples": nonzero_val[:4],
        "first_two": occ[:2], "last_two": occ[-2:],
        "offsets_strictly_increasing": all(
            occ[i]["document_cp"] < occ[i + 1]["document_cp"] for i in range(len(occ) - 1)),
        "max_document_cp": occ[-1]["document_cp"],
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

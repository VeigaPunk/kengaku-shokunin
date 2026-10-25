"""R29Task356 occurrence provenance: map every environment-token occurrence in
the serialized raw text to (JSON pointer, offset in value codepoints, offset in
document codepoints). Read-only; stdlib only; no upstream import/exec.
"""
import collections
import hashlib
import json
import os

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(ROOT, "plans/fixtures/r28/webarena/config_files/test.raw.json")
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {k: "__%s__" % k for k in ORDER}


def scan(text):
    """Return list of (pointer, value, value_start_codepoint) for strings.

    Minimal JSON scanner specialized to this document's grammar; it tracks
    object keys and array indices, ignoring numbers/bools/null structure.
    """
    out = []
    i, n = 0, len(text)
    stack = []          # entries: ["obj", current_key] or ["arr", next_index]
    pending_key = None
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            buf = []
            while j < n:
                ch = text[j]
                if ch == "\\":
                    buf.append(text[j:j + 2])
                    j += 2
                    continue
                if ch == '"':
                    break
                buf.append(ch)
                j += 1
            raw_val = "".join(buf)
            val = json.loads('"' + raw_val + '"')
            if pending_key is not None:
                ptr = "/".join([e[1] if e[0] == "arr" else str(e[1]) for e in stack]
                               + [pending_key])
                out.append((ptr, val, i + 1))
                pending_key = None
            else:
                ptr = "/".join([str(e[1]) for e in stack])
                out.append((ptr, val, i + 1))
            i = j + 1
            continue
        if c == "{":
            stack.append(["obj", None])
            i += 1
            continue
        if c == "}":
            stack.pop()
            i += 1
            continue
        if c == "[":
            stack.append(["arr", 0])
            i += 1
            continue
        if c == "]":
            stack.pop()
            i += 1
            continue
        if c == ",":
            if stack and stack[-1][0] == "arr":
                stack[-1][1] += 1
            i += 1
            continue
        if c == ":":
            i += 1
            continue
        if c in " \t\r\n":
            i += 1
            continue
        # number / true / false / null
        j = i
        while j < n and text[j] not in ",]}" :
            j += 1
        i = j
        continue
    return out


def main():
    with open(RAW, "rb") as f:
        b = f.read()
    text = b.decode("utf-8")
    spans = scan(text)
    occurrences = []
    for ptr, val, start in spans:
        if not isinstance(val, str):
            continue
        for k in ORDER:
            tok = TOK[k]
            pos = val.find(tok)
            while pos >= 0:
                occurrences.append({"json_pointer": ptr, "token": k,
                                    "offset_in_value_codepoints": pos,
                                    "document_codepoint": start + pos})
                pos = val.find(tok, pos + len(tok))
    by_role = collections.Counter()
    for o in occurrences:
        parts = o["json_pointer"].split("/")
        field = parts[1] if len(parts) > 1 else "TOP"
        if field == "start_url":
            role = "start_url"
        elif field == "eval":
            sub = parts[2] if len(parts) > 2 else "eval"
            role = "eval." + sub
        else:
            role = field
        by_role[role] += 1
    out = {
        "raw_sha256": hashlib.sha256(b).hexdigest(),
        "raw_is_ascii": text.isascii(),
        "bytes": len(b), "codepoints": len(text),
        "string_leaf_count": sum(1 for _, v, _ in spans if isinstance(v, str)),
        "occurrence_count": len(occurrences),
        "occurrences_by_role": dict(by_role),
        "occurrences_by_token": dict(collections.Counter(o["token"] for o in occurrences)),
        "distinct_leaf_paths_with_occurrence": len({o["json_pointer"] for o in occurrences}),
        "first_three": occurrences[:3],
        "last_three": occurrences[-3:],
        "monotone_document_offsets": all(
            occurrences[i]["document_codepoint"] < occurrences[i + 1]["document_codepoint"]
            for i in range(len(occurrences) - 1)),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

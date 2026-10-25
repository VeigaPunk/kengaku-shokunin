"""Independent path-aware oracle for string occurrence provenance.

Uses ONLY a regex tokenizer for literals + json.loads for structure, never the production
recursive scanner. Emits, per literal: (start, end, role, json_pointer, path_template, task_index)
where path_template mirrors the documented convention (task index dropped, list indices
rendered as '[]' suffix on the preceding component).
"""
import json
import re

STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"', re.S)
TOKEN_RE = re.compile(r"__[A-Z][A-Z_]*__")


def esc(part):
    return str(part).replace("~", "~0").replace("/", "~1")


def pointer(path):
    return "/" + "/".join(esc(p) for p in path)


def template(path):
    parts = []
    for part in path[1:]:
        if isinstance(part, int):
            parts[-1] = parts[-1] + "[]" if parts else "[]"
        else:
            parts.append(part)
    return ".".join(parts)


def literal_spans(text):
    """[(start, end, decoded, is_key)]"""
    out = []
    for m in STRING_RE.finditer(text):
        try:
            dec = json.loads(m.group(0))
        except Exception:
            continue
        j = m.end()
        while j < len(text) and text[j] in " \t\n\r":
            j += 1
        out.append((m.start(), m.end(), dec, j < len(text) and text[j] == ":"))
    return out


def occurrences(text, tokens):
    """{token: [(offset, role, pointer, template, task_index)]}"""
    lits = literal_spans(text)
    res = {t: [] for t in tokens}
    for tok in tokens:
        at = text.find(tok)
        while at != -1:
            hit = None
            for (s, e, dec, is_key) in lits:
                if s < at and at + len(tok) <= e:
                    hit = (s, e, is_key)
                    break
            if hit is None:
                res[tok].append((at, "outside", None, None, None))
            else:
                res[tok].append((at, "key" if hit[2] else "value", None, None, None))
            at = text.find(tok, at + len(tok))
    return res

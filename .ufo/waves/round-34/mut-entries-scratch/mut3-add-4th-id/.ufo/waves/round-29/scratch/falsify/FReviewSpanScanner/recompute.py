"""Independent recomputation of the pinned run's provenance/population numbers.

Reads ONLY the pinned raw file + profiles.json and plain json/text operations.
Does NOT import or read plans/config_projection.py.
"""
import json
import re
import hashlib

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json"
ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")
TOKENS = ["__%s__" % n for n in ORDER]
URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url"})
MARKER_RE = re.compile(r"__[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*__")


def esc(p):
    return str(p).replace("~", "~0").replace("/", "~1")


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


def leaves(node, keys=False):
    if isinstance(node, dict):
        for k, v in node.items():
            if keys:
                yield k
            yield from leaves(v, keys)
    elif isinstance(node, list):
        for v in node:
            yield from leaves(v, keys)
    elif isinstance(node, str):
        yield node


def main():
    text = open(RAW, encoding="utf-8").read()
    doc = json.loads(text)
    profiles = json.loads(open(PROFILES, encoding="utf-8").read())

    lit_re = re.compile(r'"(?:[^"\\]|\\.)*"', re.S)
    lits = []
    for m in lit_re.finditer(text):
        j = m.end()
        while j < len(text) and text[j] in " \t\n\r":
            j += 1
        lits.append((m.start(), m.end(), j < len(text) and text[j] == ":"))

    def containing(at, toklen):
        for (s, e, is_key) in lits:
            if s < at and at + toklen <= e:
                return "key" if is_key else "value"
        return "outside"

    occ = []
    for tok in TOKENS:
        at = text.find(tok)
        while at != -1:
            occ.append((tok, at, containing(at, len(tok))))
            at = text.find(tok, at + len(tok))
    roles = {}
    for _, _, r in occ:
        roles[r] = roles.get(r, 0) + 1
    markers = {}
    for m in MARKER_RE.finditer(text):
        if m.group() not in TOKENS:
            markers[m.group()] = markers.get(m.group(), 0) + 1
    out = {
        "input_task_count": len(doc),
        "distinct_task_ids": len({t.get("task_id") for t in doc}),
        "original_occurrences_by_token": {t: text.count(t) for t in TOKENS},
        "occurrence_roles": roles,
        "tokens_followed_by_slash": sum(text.startswith("/", a + len(tk)) for tk, a, _ in occ),
        "other_double_underscore_markers": dict(sorted(markers.items())),
    }

    for name, prof in profiles.items():
        t = text
        for n in ORDER:
            t = t.replace("__%s__" % n, prof["values"][n])
        pj = json.loads(t)
        changed = []
        problems = []

        def diff(a, b, path):
            if type(a) is not type(b):
                problems.append(pointer(path))
            elif isinstance(a, dict):
                if list(a) != list(b):
                    problems.append(pointer(path))
                else:
                    for k in a:
                        diff(a[k], b[k], path + (k,))
            elif isinstance(a, list):
                if len(a) != len(b):
                    problems.append(pointer(path))
                else:
                    for i, x in enumerate(a):
                        diff(x, b[i], path + (i,))
            elif isinstance(a, str):
                if a != b:
                    changed.append((path, a, b))
            elif a != b:
                problems.append(pointer(path))

        diff(doc, pj, ())
        cat, tmpl, bytok = {}, {}, {t: 0 for t in TOKENS}
        for path, before, after in changed:
            c = "url_field" if template(path) in URL_FIELD_TEMPLATES else "non_url_field"
            cat[c] = cat.get(c, 0) + 1
            tmpl[template(path)] = tmpl.get(template(path), 0) + 1
            for tok in TOKENS:
                if tok in before:
                    bytok[tok] += 1
        out[name] = {
            "parsed_task_count": len(pj),
            "string_leaf_count": sum(1 for _ in leaves(pj)),
            "changed_leaf_count": len(changed),
            "changed_task_count": len({p[0] for p, _, _ in changed}),
            "changed_leaves_by_category": dict(sorted(cat.items())),
            "changed_leaves_by_path_template": dict(sorted(tmpl.items())),
            "changed_leaves_by_token": bytok,
            "remaining_known_tokens_text": {tok: t.count(tok) for tok in TOKENS},
            "remaining_known_tokens_decoded": {t: sum(s.count(t) for s in leaves(pj, True)) for t in TOKENS},
            "problems": problems[:20],
            "projected_text_sha256": hashlib.sha256(t.encode("utf-8")).hexdigest(),
        }
    print(json.dumps(out, indent=1, sort_keys=True))


main()

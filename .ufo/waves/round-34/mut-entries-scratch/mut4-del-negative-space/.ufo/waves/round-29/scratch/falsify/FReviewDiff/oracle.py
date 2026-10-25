#!/usr/bin/env python3
"""Independent leaf-walk / census cross-check for the round-29 projection instrument.

Written by KengakuR29-2.FReviewDiff-2 from the PREREG TEXT + pinned generator bytes +
pinned raw data only. It does NOT import or read plans/config_projection.py.
It compares against the instrument's --json OUTPUT only.
"""
import json
import sys
import hashlib

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = ROOT + "/plans/fixtures/r29/profiles.json"
ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")
TOKENS = ["__%s__" % n for n in ORDER]
URL_FIELD_TEMPLATES = {"start_url", "eval.reference_url", "eval.program_html[].url"}


def ptr(path):
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in path)


def tmpl(path):
    """Independent re-implementation of the path-template rule (path[1:] onwards)."""
    parts = []
    for part in path[1:]:
        if isinstance(part, int):
            if parts:
                parts[-1] = parts[-1] + "[]"
            else:
                parts.append("[]")
        else:
            parts.append(part)
    return ".".join(parts)


def walk(original, projected, path, changed, problems):
    if type(original) is not type(projected):
        problems.append(ptr(path))
    elif isinstance(original, dict):
        if list(original) != list(projected):
            problems.append(ptr(path))
        else:
            for key in original:
                walk(original[key], projected[key], path + (key,), changed, problems)
    elif isinstance(original, list):
        if len(original) != len(projected):
            problems.append(ptr(path))
        else:
            for i, item in enumerate(original):
                walk(item, projected[i], path + (i,), changed, problems)
    elif isinstance(original, str):
        if original != projected:
            changed.append((path, original, projected))
    elif original != projected:
        problems.append(ptr(path))


def string_leaves(node, keys=False):
    if isinstance(node, dict):
        for k, v in node.items():
            if keys:
                yield k
            yield from string_leaves(v, keys)
    elif isinstance(node, list):
        for v in node:
            yield from string_leaves(v, keys)
    elif isinstance(node, str):
        yield node


def main():
    raw_text = open(RAW, encoding="utf-8").read()
    profiles = json.load(open(PROFILES, encoding="utf-8"))
    original = json.loads(raw_text)
    out = {}
    for name, profile in profiles.items():
        text = raw_text
        applied = {}
        for tok_name in ORDER:
            tok = "__%s__" % tok_name
            applied[tok_name] = text.count(tok)
            text = text.replace(tok, profile["values"][tok_name])
        projected = json.loads(text)
        changed, problems = [], []
        walk(original, projected, (), changed, problems)
        carriers = sum(1 for t in string_leaves(original) if any(tok in t for tok in TOKENS))
        unexplained = sum(1 for _, before, _ in changed if not [tok for tok in TOKENS if tok in before])
        by_template = {}
        by_category = {}
        by_token = {t: 0 for t in TOKENS}
        multi = 0
        per_task = {}
        for path, before, after in changed:
            t = tmpl(path)
            by_template[t] = by_template.get(t, 0) + 1
            cat = "url_field" if t in URL_FIELD_TEMPLATES else "non_url_field"
            by_category[cat] = by_category.get(cat, 0) + 1
            carried = [tok for tok in TOKENS if tok in before]
            for tok in carried:
                by_token[tok] += 1
            if sum(before.count(tok) for tok in TOKENS) > 1:
                multi += 1
            per_task.setdefault(path[0], []).append(ptr(path))
        out[name] = {
            "parsed_task_count": len(projected),
            "string_leaf_count": sum(1 for _ in string_leaves(projected)),
            "changed_leaf_count": len(changed),
            "changed_task_count": len(per_task),
            "carriers": carriers,
            "unexplained": unexplained,
            "problems": problems[:20],
            "problem_count": len(problems),
            "changed_leaves_by_path_template": dict(sorted(by_template.items())),
            "changed_leaves_by_category": dict(sorted(by_category.items())),
            "changed_leaves_by_token": by_token,
            "changed_leaves_with_multiple_occurrences": multi,
            "remaining_known_tokens_text": {t: text.count(t) for t in TOKENS},
            "remaining_known_tokens_decoded": {t: sum(s.count(t) for s in string_leaves(projected, True)) for t in TOKENS},
            "projected_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "per_task_changed_leaves": {str(k): v for k, v in sorted(per_task.items())},
        }
    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    print()


main()

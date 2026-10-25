"""Provenance-level differential fuzz.

Compares production provenance(raw_text, spans) against an independent oracle that
derives each token occurrence's role / json_pointer / path_template / task_index from
(a) a regex literal tokenizer over the raw text and (b) a json.loads-derived ordered
structure walk (object_pairs_hook keeps duplicates and order).
"""
import importlib.util
import json
import random
import re
import sys

sys.path.insert(0, "/tmp/r29span")

PROD = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py"
spec = importlib.util.spec_from_file_location("cp_prod", PROD)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"', re.S)


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


def ordered_structure(text):
    """[(path, role, decoded)] in document order, duplicates preserved."""
    out = []

    def hook(pairs):
        return ("OBJ", pairs)

    def walk(node, path):
        if isinstance(node, tuple) and node and node[0] == "OBJ":
            for k, v in node[1]:
                out.append((path, "key", k))
                walk(v, path + (k,))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + (i,))
        elif isinstance(node, str):
            out.append((path, "value", node))

    walk(json.loads(text, object_pairs_hook=hook), ())
    return out


def literal_list(text):
    out = []
    for m in STRING_RE.finditer(text):
        j = m.end()
        while j < len(text) and text[j] in " \t\n\r":
            j += 1
        out.append((m.start(), m.end(), j < len(text) and text[j] == ":"))
    return out


ALPHA = list('abcXY09 _/\\"\t\n') + ['\\"', "\\\\", "\\u00e9", "\\/", "\\n", "\\t"]


def rstr(rng, n=None):
    n = rng.randint(0, 10) if n is None else n
    return "".join(rng.choice(ALPHA) for _ in range(n))


TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__MAP__"]


def build(rng, depth=0):
    r = rng.random()
    if depth > 2 or r < 0.5:
        c = rng.random()
        if c < 0.45:
            s = rstr(rng)
            if rng.random() < 0.5:
                s += rng.choice(TOKENS) + rstr(rng, 3)
            return s
        return rng.choice([1, -2, 0, 3.5, True, False, None, 1e5])
    if r < 0.75:
        return [build(rng, depth + 1) for _ in range(rng.randint(0, 3))]
    d = {}
    for _ in range(rng.randint(0, 3)):
        k = rstr(rng, rng.randint(1, 4))
        if rng.random() < 0.4:
            k += rng.choice(TOKENS)
        d[k] = build(rng, depth + 1)
    return d


def run(trials=3000, seed=4242):
    rng = random.Random(seed)
    bad = []
    prod_exc = []
    for t in range(trials):
        doc = build(rng)
        text = json.dumps(doc, indent=rng.choice([None, 0, 2]))
        # inject whitespace
        text = text.replace(":", " : ") if rng.random() < 0.3 else text
        # oracle
        lits = literal_list(text)
        struct = ordered_structure(text)
        # pair literals with structure entries by order (keys+values in doc order)
        if len(lits) != len(struct):
            continue
        # map literal -> (role, path)
        meta = []
        for (s, e, is_key), (path, role, dec) in zip(lits, struct):
            meta.append((s, e, role, path))
        try:
            spans = cp.string_spans(text)
            prov = cp.provenance(text, spans)
        except Exception as exc:
            prod_exc.append((text[:200], repr(exc)))
            continue
        # expected records
        exp = []
        for tok in cp.ORDER:
            t = "__%s__" % tok
            at = text.find(t)
            while at != -1:
                hit = None
                for (s, e, role, path) in meta:
                    if s < at and at + len(t) <= e:
                        hit = (s, e, role, path)
                        break
                if hit is None:
                    exp.append({"token": t, "off": at, "role": "outside", "ptr": None, "tpl": None, "ti": None})
                else:
                    s, e, role, path = hit
                    p = path + ((hit_path_key,) if False else ())
                    exp.append({"token": t, "off": at, "role": role, "ptr": pointer(path),
                                "tpl": template(path), "ti": path[0] if path else None})
                at = text.find(t, at + len(t))
        got = [{"token": r["token"], "off": r["original_input_codepoint_offset"], "role": r["string_role"],
                "ptr": r["json_pointer"], "tpl": r["path_template"], "ti": r["task_index"]} for r in prov]
        if got != exp:
            bad.append((text, got, exp))
    print("trials", trials, "prod exceptions", len(prod_exc), "mismatches", len(bad))
    for text, got, exp in bad[:4]:
        print("=== TEXT", repr(text[:300]))
        for g, e in zip(got, exp):
            if g != e:
                print("  GOT", g)
                print("  EXP", e)
        if len(got) != len(exp):
            print("  len", len(got), len(exp))
    for text, e in prod_exc[:4]:
        print("=== PROD EXC", repr(text[:200]), e)
    return bad, prod_exc


if __name__ == "__main__":
    run()

"""Differential fuzz: production config_projection.string_spans vs independent reference
and vs json.loads-derived ground truth. Read-only w.r.t. production."""
import importlib.util
import json
import random
import sys
import traceback

sys.path.insert(0, "/tmp/r29span")
from ref import ref_spans  # noqa: E402

PROD = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py"
spec = importlib.util.spec_from_file_location("cp_prod", PROD)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)


def truth_from_loads(doc):
    """(path, role, decoded) census derived from json.loads (last-dup-key semantics)."""
    out = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                out.append((path, "key", k))
                walk(v, path + (k,))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + (i,))
        elif isinstance(node, str):
            out.append((path, "value", node))

    walk(doc, ())
    return out


ALPHABET = list('abcXYZ019 /\\"\t\n:_-.') + ['\\"', "\\\\", "\\u00e9", "\\uD83D\\uDE00", "\\/", "\\b", "\\f", "\\n", "\\r", "\\t"]


def rand_string(rng, n=None):
    n = n if n is not None else rng.randint(0, 12)
    return "".join(rng.choice(ALPHABET) for _ in range(n))


def rand_scalar(rng):
    r = rng.random()
    if r < 0.4:
        return rand_string(rng)
    if r < 0.55:
        return rng.randint(-10**6, 10**6)
    if r < 0.65:
        return rng.choice([0, -0.0, 1.5, -2.25, 1e10, 1e-10, 3.0, 123456789012345678901234567890.5])
    if r < 0.75:
        return rng.choice([True, False])
    if r < 0.85:
        return None
    return rand_string(rng)


def rand_doc(rng, depth=0):
    r = rng.random()
    if depth > 3 or r < 0.45:
        return rand_scalar(rng)
    if r < 0.72:
        return [rand_doc(rng, depth + 1) for _ in range(rng.randint(0, 4))]
    return {rand_string(rng, rng.randint(1, 5)): rand_doc(rng, depth + 1) for _ in range(rng.randint(0, 4))}


WS_CHOICES = ["", " ", "\n", "\t", "\r", "  ", "\n\t "]


def dumps_ws(obj, rng):
    """json.dumps then sprinkle whitespace between tokens (still valid JSON)."""
    s = json.dumps(obj)
    out = []
    i = 0
    in_str = False
    esc = False
    while i < len(s):
        c = s[i]
        if in_str:
            out.append(c)
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c in "{}[],:":
            out.append(c)
            out.append(rng.choice(WS_CHOICES))
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def run(trials=4000, seed=20261021):
    rng = random.Random(seed)
    mism_ref = []
    mism_truth = []
    prod_errors = []
    ref_errors = []
    for t in range(trials):
        obj = rand_doc(rng)
        try:
            text = dumps_ws(obj, rng)
        except Exception:
            continue
        # production
        try:
            p = cp.string_spans(text)
            p_err = None
        except Exception as e:
            p, p_err = None, repr(e)
        # reference
        try:
            r = ref_spans(text)
            r_err = None
        except Exception as e:
            r, r_err = None, repr(e)
        if p_err and not r_err:
            prod_errors.append((text, p_err))
        if r_err and not p_err:
            ref_errors.append((text, r_err))
        if p_err or r_err:
            continue
        if p != r:
            mism_ref.append((text, p, r))
        # ground truth
        try:
            g = truth_from_loads(json.loads(text))
        except Exception:
            continue
        pv = sorted((x[2], x[3], x[4]) for x in p if x[3] == "value")
        gv = sorted((x[0], x[1], x[2]) for x in g if x[1] == "value")
        pv2 = sorted((x[2], x[4]) for x in p if x[3] == "value")
        gv2 = sorted((x[0], x[2]) for x in g if x[1] == "value")
        if pv2 != gv2:
            mism_truth.append((text, pv2, gv2))
    print("trials", trials)
    print("prod_only_errors", len(prod_errors), "ref_only_errors", len(ref_errors))
    print("mismatch_vs_reference", len(mism_ref))
    print("mismatch_vs_loads_truth", len(mism_truth))
    for i, (text, p, r) in enumerate(mism_ref[:5]):
        print("--- REF MISMATCH", i, repr(text[:400]))
        for a, b in zip(p, r):
            if a != b:
                print("   prod", a, "ref", b)
                break
        if len(p) != len(r):
            print("   len", len(p), len(r))
    for i, (text, pv2, gv2) in enumerate(mism_truth[:5]):
        print("--- TRUTH MISMATCH", i, repr(text[:400]))
        print("   prod-only", [x for x in pv2 if x not in gv2][:3])
        print("   truth-only", [x for x in gv2 if x not in pv2][:3])
    for text, e in prod_errors[:5]:
        print("--- PROD ERROR", repr(text[:300]), e)
    return mism_ref, mism_truth, prod_errors, ref_errors


if __name__ == "__main__":
    run()

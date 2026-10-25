#!/usr/bin/env python3
"""Targeted check of the new duplicate_json_key finding: true duplicates vs same-name keys in different objects."""
import importlib.util
import json
import random

spec = importlib.util.spec_from_file_location("cp2", "/tmp/fr29d2/cp2.py")
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)
V = {n: "http://%s.invalid:1" % n.lower().replace("_", "-") for n in cp.ORDER}


def findings(raw):
    _, f = cp.audit_text(raw, {"p": {"purpose": "probe", "values": V}})
    return [x for x in f if x["id"] == "duplicate_json_key"]


def true_dups(raw):
    """Independent count of keys that occur twice inside the SAME object."""
    import collections
    counts = collections.Counter()

    def hook(pairs):
        c = collections.Counter(k for k, _ in pairs)
        for k, n in c.items():
            if n > 1:
                counts[k] += 1
        return dict(pairs)
    json.loads(raw, object_pairs_hook=hook)
    return sum(counts.values())


cases = [
    ('[{"a": 1, "a": 2}]', 1),
    ('[{"a": 1}, {"a": 2}]', 0),                      # same key name, different objects
    ('[{"x": {"a": 1, "a": 2}}]', 1),
    ('[{"x": [{"a": 1, "a": 2}]}]', 1),
    ('[{"a": 1, "a": 2, "a": 3}]', 1),                # one key, three times -> one pointer
    ('[{"a": 1, "a": 2}, {"b": 3, "b": 4}]', 2),
    ('[{"a\\u0062": 1, "ab": 2}]', 1),               # distinct RAW names, same DECODED name -> real collision
    ('[{"a": 1, "a": 2, "b": 3, "b": 4}]', 2),
]
bad = []
for raw, expect in cases:
    got = findings(raw)
    count = got[0]["count"] if got else 0
    ok = (count == expect) and (true_dups(raw) == expect)
    print("%-46s expect=%d got=%d pointers=%s true_dups=%d %s" %
          (raw, expect, count, json.dumps(got[0]["pointers"] if got else []), true_dups(raw), "OK" if ok else "MISMATCH"))
    if not ok:
        bad.append(raw)

# randomised: same key name repeated in distinct objects must never be reported
rng = random.Random(7)
for _ in range(400):
    raw = json.dumps([{rng.choice(["a", "b", "c"]): rng.randint(0, 9)} for _ in range(rng.randint(2, 4))])
    if findings(raw):
        bad.append(("false positive", raw))
print("mismatches/false positives:", bad if bad else "NONE")

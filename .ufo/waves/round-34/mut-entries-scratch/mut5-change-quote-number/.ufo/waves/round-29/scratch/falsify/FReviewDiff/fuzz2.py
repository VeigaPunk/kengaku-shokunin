#!/usr/bin/env python3
"""Text-level differential fuzz: JSON escapes, duplicate keys, tokens in key position.

Checks the decoded remaining-token census (keys included), the serialized-text census, the
occurrence-provenance census, and the known_token_remaining finding against independent
recomputation from the same raw text.
"""
import importlib.util
import json
import random

spec = importlib.util.spec_from_file_location("cp", "/tmp/fr29d/cp.py")
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

ORDER = cp.ORDER
TOKENS = ["__%s__" % n for n in ORDER]
VALUES = {n: "http://%s.invalid:1" % n.lower().replace("_", "-") for n in ORDER}
ESC = "\\u005f"  # literal backslash-u escape text that decodes to "_"


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
    rng = random.Random(4242)
    stats = {"cases": 0, "text_census_mismatch": 0, "decoded_census_mismatch": 0,
             "known_token_remaining_missing": 0, "known_token_remaining_spurious": 0,
             "occ_vs_decoded_disagree": 0, "exceptions": 0}
    examples = []
    for case in range(3000):
        task = {"task_id": 0, "a": rng.choice(TOKENS), "b": "x", "c": {"d": rng.choice(TOKENS)}}
        raw = json.dumps([task], indent=rng.choice([None, 2]))
        kind = rng.choice(["none", "escape", "escape", "dupkey", "keytoken", "escape_key"])
        if kind == "escape":
            tok = rng.choice(TOKENS)
            pos = raw.find(tok)
            if pos >= 0:
                raw = raw[:pos] + ESC * 2 + tok[2:] + raw[pos + len(tok):]
        elif kind == "escape_key":
            tok = rng.choice(TOKENS)
            raw = raw.replace('"a":', '"%s":' % tok, 1)
            pos = raw.find(tok)
            if pos >= 0:
                raw = raw[:pos] + ESC * 2 + tok[2:] + raw[pos + len(tok):]
        elif kind == "dupkey":
            raw = raw.replace('"b": "x"', '"b": "x", "b": "y"', 1)
        elif kind == "keytoken":
            raw = raw.replace('"a":', '"%s":' % rng.choice(TOKENS), 1)
        try:
            original = json.loads(raw)
        except ValueError:
            continue
        try:
            result, findings = cp.audit_text(raw, {"distinct_origins": {"purpose": "fuzz", "values": VALUES}})
        except Exception as error:
            stats["exceptions"] += 1
            if len(examples) < 10:
                examples.append(("EXC", kind, raw, type(error).__name__, str(error)))
            continue
        stats["cases"] += 1
        rec = result["profiles"]["distinct_origins"]
        text = raw
        for name in ORDER:
            text = text.replace("__%s__" % name, VALUES[name])
        try:
            projected = json.loads(text)
        except ValueError:
            continue
        # independent serialized-text census on the projected text
        mine_text = {t: text.count(t) for t in TOKENS}
        if mine_text != rec["remaining_known_tokens_text"]:
            stats["text_census_mismatch"] += 1
            if len(examples) < 10:
                examples.append(("TEXT", kind, raw, mine_text, rec["remaining_known_tokens_text"]))
        # independent decoded census (values + keys)
        mine_dec = {t: sum(s.count(t) for s in leaves(projected, True)) for t in TOKENS}
        if mine_dec != rec["remaining_known_tokens_decoded"]:
            stats["decoded_census_mismatch"] += 1
            if len(examples) < 10:
                examples.append(("DEC", kind, raw, mine_dec, rec["remaining_known_tokens_decoded"]))
        # known_token_remaining finding must match "any census non-zero"
        expect = any(mine_text.values()) or any(mine_dec.values())
        got = any(f["id"] == "known_token_remaining" for f in findings)
        if expect and not got:
            stats["known_token_remaining_missing"] += 1
            if len(examples) < 10:
                examples.append(("MISS", kind, raw, mine_text, mine_dec))
        if got and not expect:
            stats["known_token_remaining_spurious"] += 1
            if len(examples) < 10:
                examples.append(("SPUR", kind, raw, mine_text, mine_dec))
        # occurrence provenance (text-level) vs decoded census: a token that survives decoding
        # but never appears literally in the raw text is invisible to the provenance census
        prov_counts = {t: sum(1 for r in result["occurrence_provenance"] if r["token"] == t) for t in TOKENS}
        surviving = {t for t in TOKENS if mine_dec.get(t)}
        literal_in_raw = {t for t in TOKENS if raw.count(t)}
        if surviving - literal_in_raw:
            stats["occ_vs_decoded_disagree"] += 1
            if len(examples) < 10:
                examples.append(("OCC", kind, raw, sorted(surviving - literal_in_raw), prov_counts))
    print(json.dumps(stats, indent=1))
    for e in examples:
        print(e)


main()

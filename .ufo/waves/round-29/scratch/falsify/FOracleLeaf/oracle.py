#!/usr/bin/env python3
"""FOracleLeaf-2 decoded-leaf oracle — Kengaku round 29 falsify wave.

INDEPENDENCE: this file never reads or imports plans/config_projection.py
(production source). It is derived only from:
  - the prereg TEXT (plans/round-29-claims.md): six global ordered text
    replacements __GITLAB__ __REDDIT__ __SHOPPING__ __SHOPPING_ADMIN__
    __WIKIPEDIA__ __MAP__ over the raw serialized text, then json parse,
    then positional enumerate for output filenames;
  - the pinned generator bytes (plans/fixtures/r29/generate_test_data.py);
  - the pinned data (manifest.json, profiles.json, test.raw.json).
It MAY read the instrument's --json OUTPUT (a file) for comparison, which the
contract explicitly allows ("compare against the instrument's --json/--summary
OUTPUT only").

Modes:
  (default)      frozen-input audit: census + leaf-vs-text-vs-instrument
                 comparison over all 812x3 = 2436 projections.
  --hands        adversarial hand inputs where decoded-leaf substitution and
                 text substitution provably differ (quote-in-value,
                 backslash/escape, later-token cascade, trailing backslash).
  --json-path F  path to captured instrument --json output (default: sibling
                 instr_json.out in this script's directory).

Stdlib only. Read-only with respect to the lane root.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
RAW = LANE / "plans/fixtures/r28/webarena/config_files/test.raw.json"
GENERATOR = LANE / "plans/fixtures/r29/generate_test_data.py"
MANIFEST = LANE / "plans/fixtures/r29/profiles.json".replace(
    "profiles.json", "manifest.json"
)
PROFILES = LANE / "plans/fixtures/r29/profiles.json"

TOKEN_NAMES = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOKENS = [f"__{n}__" for n in TOKEN_NAMES]
# Longest-first alternation makes overlap at a shared start position impossible.
_LEAF_RE = re.compile("|".join(re.escape(t) for t in sorted(TOKENS, key=len, reverse=True)))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_pinned_inputs():
    raw_bytes = RAW.read_bytes()
    gen_bytes = GENERATOR.read_bytes()
    man_bytes = MANIFEST.read_bytes()
    prof_bytes = PROFILES.read_bytes()
    man = json.loads(man_bytes.decode("utf-8"))
    pins = {
        str(RAW.relative_to(LANE)): sha256_bytes(raw_bytes),
        str(GENERATOR.relative_to(LANE)): sha256_bytes(gen_bytes),
        str(PROFILES.relative_to(LANE)): sha256_bytes(prof_bytes),
    }
    pin_findings = []
    for rel, got in pins.items():
        want = man["files"].get(rel, {}).get("sha256")
        if want != got:
            pin_findings.append({"pin_mismatch": rel, "manifest_sha256": want, "observed": got})
    return raw_bytes, man, pins, pin_findings


# ---------------------------------------------------------------- leaf oracle

def leaf_sub(s: str, values: dict[str, str]) -> tuple[str, list[str]]:
    """Single-pass token substitution over one DECODED string.

    Each decoded string is scanned exactly once; replacement text is never
    rescanned (no cascade). keys and values are both treated as strings.
    """
    hits: list[str] = []

    def repl(m: re.Match) -> str:
        tok = m.group(0)
        hits.append(tok)
        return values[tok[2:-2]]

    return _LEAF_RE.sub(repl, s), hits


def leaf_project(doc, values, key_collisions: list | None = None):
    """Walk the decoded structure in document order, substituting tokens in
    every decoded string (dict keys AND values). Returns the new structure."""
    if isinstance(doc, dict):
        out = {}
        for k, v in doc.items():
            nk, _ = leaf_sub(k, values) if isinstance(k, str) else (k, [])
            nv = leaf_project(v, values, key_collisions)
            if key_collisions is not None and nk in out and nk != k:
                key_collisions.append({"original_key": k, "projected_key": nk})
            out[nk] = nv
        return out
    if isinstance(doc, list):
        return [leaf_project(v, values, key_collisions) for v in doc]
    if isinstance(doc, str):
        s, _ = leaf_sub(doc, values)
        return s
    return doc


# ---------------------------------------------------------------- text oracle

def text_project(raw: str, values: dict[str, str]):
    """Own re-derivation of the upstream TEXT contract from the prereg text and
    pinned generator bytes: six sequential str.replace calls over the raw
    serialized text, then json parse. Raises json.JSONDecodeError on bad text."""
    s = raw
    for name in TOKEN_NAMES:
        s = s.replace(f"__{name}__", values[name])
    return s, json.loads(s)


# ------------------------------------------------------------------- census

def census(doc, raw_text):
    c = {
        "raw_token_counts": {t: raw_text.count(t) for t in TOKENS},
        "decoded_value_occurrences": {t: 0 for t in TOKENS},
        "decoded_key_occurrences": {t: 0 for t in TOKENS},
        "string_value_leaves": 0,
        "string_key_leaves": 0,
        "tasks": len(doc),
        "task_ids": [item.get("task_id") for item in doc],
    }
    for _, s, is_key in walk_strings_decoded(doc):
        for t in TOKENS:
            n = s.count(t)
            if n:
                if is_key:
                    c["decoded_key_occurrences"][t] += n
                else:
                    c["decoded_value_occurrences"][t] += n
        if is_key:
            c["string_key_leaves"] += 1
        else:
            c["string_value_leaves"] += 1
    return c


def walk_strings_decoded(doc, pointer=""):
    """Yield (json_pointer, string, is_key) in document order, keys first."""
    if isinstance(doc, dict):
        for k, v in doc.items():
            if isinstance(k, str):
                yield pointer, k, True
            yield from walk_strings_decoded(v, pointer + "/" + esc(k))
    elif isinstance(doc, list):
        for i, v in enumerate(doc):
            yield from walk_strings_decoded(v, f"{pointer}/{i}")
    elif isinstance(doc, str):
        yield pointer, doc, False


def esc(seg: str) -> str:
    return seg.replace("~", "~0").replace("/", "~1")


def diff_leaves(orig, proj):
    """Deep diff of two JSON trees; yields (pointer, original, projected) for
    every leaf where they differ (including type changes)."""
    out = []

    def rec(a, b, p):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in a:
                if k in b:
                    rec(a[k], b[k], p + "/" + esc(k))
                else:
                    out.append((p + "/" + esc(k), a[k], "<key-removed>"))
            for k in b:
                if k not in a:
                    out.append((p + "/" + esc(k), "<key-added>", b[k]))
        elif isinstance(a, list) and isinstance(b, list):
            for i, (x, y) in enumerate(zip(a, b)):
                rec(x, y, f"{p}/{i}")
            if len(a) != len(b):
                out.append((p + "/len", len(a), len(b)))
        elif a != b:
            out.append((p, a, b))

    rec(orig, proj, "")
    return out


def tokens_in_leaf_diff(orig, proj, values):
    """Token hits attributable to one changed leaf (from the ORIGINAL value)."""
    if isinstance(orig, str):
        _, hits = leaf_sub(orig, values)
        return sorted(set(hits))
    return []


# ----------------------------------------------------------- frozen comparison

def run_frozen(instr_json_path: Path | None) -> dict:
    raw_bytes, man, pins, pin_findings = load_pinned_inputs()
    raw_text = raw_bytes.decode("utf-8")
    profiles = json.loads(PROFILES.read_bytes().decode("utf-8"))
    orig_doc = json.loads(raw_text)

    cens = census(orig_doc, raw_text)
    findings = list(pin_findings)

    # Domain preconditions D1..D5 (see report for definitions)
    domain = {"D1_escape_safe_per_token": {}, "D2_json_verbatim_values": {}, "D3_no_token_in_values": {}, "D4_tokens_pairwise_nonoverlapping": None, "D5_key_occurrences": cens["decoded_key_occurrences"]}
    for t in TOKENS:
        domain["D1_escape_safe_per_token"][t] = (
            cens["raw_token_counts"][t]
            == cens["decoded_value_occurrences"][t] + cens["decoded_key_occurrences"][t]
        )
    for pname, p in profiles.items():
        vals = p["values"]
        ok = True
        detail = {}
        for name, v in vals.items():
            verbatim = json.dumps(v) == f'"{v}"' and not any(ch in v for ch in ('"', "\\"))
            verbatim = verbatim and not any(ord(ch) < 0x20 for ch in v)
            detail[name] = verbatim
            ok = ok and verbatim
        domain["D2_json_verbatim_values"][pname] = {"all": ok, "per_token": detail}
        has_tok = {name: any(t in v for t in TOKENS) for name, v in vals.items()}
        domain["D3_no_token_in_values"][pname] = has_tok
    domain["D4_tokens_pairwise_nonoverlapping"] = {
        f"{a} in {b}": (a in b) for i, a in enumerate(TOKENS) for b in TOKENS if a != b and a in b
    }

    instr = None
    if instr_json_path is not None and instr_json_path.exists():
        instr = json.loads(instr_json_path.read_text())

    results = {}
    totals = {"objects_compared": 0, "leaf_eq_text": 0, "leaf_eq_instr": 0, "text_eq_instr": 0, "mismatches": []}
    prov_multi = []
    for pname, p in profiles.items():
        vals = p["values"]
        ptext, pdoc = text_project(raw_text, vals)
        leaf_doc = leaf_project(orig_doc, vals)
        prof_res = {
            "projected_text_sha256_mine": sha256_bytes(ptext.encode("utf-8")),
            "parsed_task_count_mine": len(pdoc),
            "objects": 0,
            "leaf_vs_text_equal": 0,
            "leaf_vs_instr_equal": 0,
            "text_vs_instr_equal": 0,
            "changed_leaves_mine": 0,
            "changed_leaves_instr": None,
            "file_sha_mismatches": 0,
            "mismatches": [],
        }
        for i, (o_item, l_item, t_item) in enumerate(zip(orig_doc, leaf_doc, pdoc)):
            eq_lt = o_item is not None and l_item == t_item
            prof_res["objects"] += 1
            totals["objects_compared"] += 1
            if eq_lt:
                prof_res["leaf_vs_text_equal"] += 1
                totals["leaf_eq_text"] += 1
            else:
                prof_res["mismatches"].append({"index": i, "kind": "leaf_vs_text"})
            if instr is not None:
                it = instr["profiles"][pname]["tasks"][i]
                if l_item == it["projected_task"]:
                    prof_res["leaf_vs_instr_equal"] += 1
                    totals["leaf_eq_instr"] += 1
                else:
                    prof_res["mismatches"].append({"index": i, "kind": "leaf_vs_instr"})
                if t_item == it["projected_task"]:
                    prof_res["text_vs_instr_equal"] += 1
                    totals["text_eq_instr"] += 1
                else:
                    prof_res["mismatches"].append({"index": i, "kind": "text_vs_instr"})
                # changed-leaf agreement per task
                mine = diff_leaves(o_item, l_item)
                theirs = it["changed_leaves"]
                mset = sorted(
                    (
                        f"/{i}{ptr}",
                        json.dumps(o, sort_keys=True, ensure_ascii=False),
                        json.dumps(pr_, sort_keys=True, ensure_ascii=False),
                    )
                    for ptr, o, pr_ in mine
                )
                tset = sorted(
                    (cl["json_pointer"], json.dumps(cl["original"], sort_keys=True, ensure_ascii=False), json.dumps(cl["projected"], sort_keys=True, ensure_ascii=False))
                    for cl in theirs
                )
                if mset != tset:
                    prof_res["mismatches"].append({"index": i, "kind": "changed_leaves_diff"})
                prof_res["changed_leaves_mine"] += len(mine)
                # would_be_file_sha256 = sha256 of upstream json.dump(item, indent=2)
                wob = sha256_bytes(json.dumps(l_item, indent=2).encode("utf-8"))
                if wob != it["would_be_file_sha256"]:
                    prof_res["file_sha_mismatches"] += 1
        if instr is not None:
            ip = instr["profiles"][pname]
            prof_res["changed_leaves_instr"] = ip["changed_leaf_count"]
            prof_res["projected_text_sha256_instr"] = ip["projected_text_sha256"]
            prof_res["text_sha_match"] = prof_res["projected_text_sha256_mine"] == ip["projected_text_sha256"]
        results[pname] = prof_res

    # independent provenance reconstruction: (token, codepoint offset, pointer)
    prov_mine = provenance_from_raw(orig_doc, raw_text, TOKENS)
    prov_cmp = None
    if instr is not None:
        theirs = instr["occurrence_provenance"]
        mine_set = {(r["token"], r["original_input_codepoint_offset"], r["json_pointer"], r["string_role"]) for r in prov_mine}
        their_set = {(r["token"], r["original_input_codepoint_offset"], r["json_pointer"], r["string_role"]) for r in theirs}
        prov_cmp = {
            "mine": len(mine_set),
            "instr": len(their_set),
            "equal_multiset": mine_set == their_set,
            "missing_from_instr": sorted(mine_set - their_set)[:10],
            "extra_in_instr": sorted(their_set - mine_set)[:10],
        }

    out = {
        "pins": pins,
        "pin_findings": findings,
        "census": cens,
        "domain": domain,
        "profiles": results,
        "totals": totals,
        "provenance": prov_cmp,
        "provenance_mine_first3": prov_mine[:3],
        "index_mapping_mine": {
            "positions": len(orig_doc),
            "distinct_task_ids": len(set(cens["task_ids"])),
            "index_equals_task_id": sum(1 for i, t in enumerate(cens["task_ids"]) if t == i),
            "violations": [i for i, t in enumerate(cens["task_ids"]) if t != i],
        },
    }
    return out


def provenance_from_raw(doc, raw_text, tokens):
    """Reconstruct token occurrences from the RAW TEXT in codepoint offsets and
    attach the decoded json pointer of the containing string by locating each
    occurrence's leaf through a raw-text scan of the decoded document."""
    # Build list of decoded strings with their pointers (document order).
    strings = [(ptr, s, is_key) for ptr, s, is_key in walk_strings_decoded(doc)]
    # For each token, find all raw offsets, then attribute each to a decoded
    # string by matching the leaf's token count in document order.
    out = []
    per_leaf = []
    for ptr, s, is_key in strings:
        occ = []
        start = 0
        while True:
            j = s.find("__", start)
            if j < 0:
                break
            m = _LEAF_RE.match(s, j)
            if m:
                occ.append(m.group(0))
                start = m.end()
            else:
                start = j + 2
        per_leaf.append((ptr, s, is_key, occ))
    # Raw offsets: find each token occurrence in raw text (in order), and
    # attribute to leaves by consuming each leaf's occurrence queue in order.
    raw_occ = []
    for t in tokens:
        start = 0
        while True:
            j = raw_text.find(t, start)
            if j < 0:
                break
            raw_occ.append((j, t))
            start = j + len(t)
    raw_occ.sort()
    queues = [list(o) for _, _, _, o in per_leaf]
    total_dec = sum(len(q) for q in queues)
    if total_dec != len(raw_occ):
        # Domain D1 violated; report counts, attribution best-effort skipped.
        return [{"d1_violation": True, "raw_occurrences": len(raw_occ), "decoded_occurrences": total_dec}]
    qi = 0
    ki = 0
    used = [0] * len(per_leaf)
    # Walk decoded strings in document order; for each, its occurrences must
    # match the next raw offsets in order (this is exactly D1 alignment).
    # To map offsets we re-find each leaf's tokens inside the raw text by
    # advancing a cursor — valid only when raw and decoded orders agree,
    # which D1 guarantees on the frozen input.
    # Strategy: serialize positions via a custom scan.
    # Simpler robust approach: re-derive (offset, pointer) by scanning the raw
    # text with a pointer-tracking mini-parser is overkill here; instead we use
    # the fact that on D1 inputs, the k-th decoded occurrence (document order)
    # equals the k-th raw occurrence (offset order).
    flat = []
    for (ptr, s, is_key, occ) in per_leaf:
        for t in occ:
            flat.append((ptr, is_key, t))
    result = []
    for (j, t), (ptr, is_key, t2) in zip(raw_occ, flat):
        assert t == t2, (t, t2, ptr)
        role = "key" if is_key else "value"
        result.append(
            {
                "json_pointer": ptr,
                "original_input_codepoint_offset": j,
                "string_role": role,
                "token": t,
            }
        )
    return result


# ----------------------------------------------------------------- hand cases

def run_hands() -> dict:
    cases = {}

    def run_case(name, raw_text, values, note):
        rec = {"note": note, "values": values, "raw": raw_text}
        # leaf oracle
        try:
            leaf_doc = leaf_project(json.loads(raw_text), values)
            rec["leaf"] = {"ok": True, "doc": leaf_doc}
        except json.JSONDecodeError as e:
            rec["leaf"] = {"ok": False, "error": f"JSONDecodeError: {e}"}
        # text oracle (upstream semantics)
        try:
            ptext, tdoc = text_project(raw_text, values)
            rec["text"] = {"ok": True, "doc": tdoc, "text_sha256": sha256_bytes(ptext.encode())}
        except json.JSONDecodeError as e:
            rec["text"] = {"ok": False, "error": str(e).split("(")[0].strip(), "position": e.pos, "line": e.lineno, "col": e.colno}
        # exact first difference
        if rec["leaf"]["ok"] and rec["text"]["ok"]:
            d = diff_leaves(rec["leaf"]["doc"], rec["text"]["doc"])
            rec["first_differences_leaf_vs_text"] = [
                {"pointer": p, "leaf": a, "text": b, "leaf_codepoints": [hex(ord(c)) for c in str(a)][:8] if isinstance(a, str) else None,
                 "text_codepoints": [hex(ord(c)) for c in str(b)][:8] if isinstance(b, str) else None}
                for p, a, b in d[:4]
            ]
        elif rec["leaf"]["ok"] and not rec["text"]["ok"]:
            rec["asymmetry"] = "leaf projection parses; text projection raises JSONDecodeError (no output file at all upstream)"
        cases[name] = rec
        return rec

    RAWA = '{"task_id": 0, "start_url": "__GITLAB__", "eval": {"reference_url": ""}}'
    # H1: double quote inside the profile value
    run_case(
        "H1_quote_in_value",
        RAWA,
        {"GITLAB": 'http://gitlab.invalid:10101/"q"', "REDDIT": "http://reddit.invalid:10102",
         "SHOPPING": "http://shopping.invalid:10103", "SHOPPING_ADMIN": "http://shopping-admin.invalid:10104",
         "WIKIPEDIA": "http://wikipedia.invalid:10105", "MAP": "http://map.invalid:10106"},
        "value contains U+0022; text injection terminates the JSON string early",
    )

    RAWB = '{"task_id": 1, "start_url": "__REDDIT__"}'
    # H2: backslash-n sequence inside the profile value (two chars: \ then n)
    run_case(
        "H2_backslash_n_escape",
        RAWB,
        {"GITLAB": "http://gitlab.invalid:10101", "REDDIT": "http://reddit.invalid:10102\\nfast",
         "SHOPPING": "http://shopping.invalid:10103", "SHOPPING_ADMIN": "http://shopping-admin.invalid:10104",
         "WIKIPEDIA": "http://wikipedia.invalid:10105", "MAP": "http://map.invalid:10106"},
        "value contains backslash+n; JSON text layer consumes it as U+000A, leaf layer keeps two chars",
    )

    RAWC = '{"task_id": 2, "start_url": "__MAP__"}'
    # H2b: value ending in a single backslash, injected directly before the closing quote
    run_case(
        "H2b_trailing_backslash",
        RAWC,
        {"GITLAB": "http://gitlab.invalid:10101", "REDDIT": "http://reddit.invalid:10102",
         "SHOPPING": "http://shopping.invalid:10103", "SHOPPING_ADMIN": "http://shopping-admin.invalid:10104",
         "WIKIPEDIA": "http://wikipedia.invalid:10105", "MAP": "http://map.invalid:10306/\\"},
        "value ends with U+005C; text injection escapes the closing quote, string never terminates",
    )

    RAWD = '{"task_id": 3, "start_url": "__GITLAB__", "alt": "__MAP__"}'
    # H3: GITLAB value contains __MAP__ — a token replaced LATER in the order
    run_case(
        "H3_later_token_cascade",
        RAWD,
        {"GITLAB": "http://gitlab.invalid:10101/__MAP__", "REDDIT": "http://reddit.invalid:10102",
         "SHOPPING": "http://shopping.invalid:10103", "SHOPPING_ADMIN": "http://shopping-admin.invalid:10104",
         "WIKIPEDIA": "http://wikipedia.invalid:10105", "MAP": "http://map.invalid:10306"},
        "later-token cascade: text step 1 injects __MAP__, step 6 substitutes it; single-pass leaf never rescans",
    )

    RAWE = '{"task_id": 4, "start_url": "__MAP__"}'
    # H4 (control): MAP value contains __GITLAB__ — an EARLIER token; both leave it literal
    run_case(
        "H4_earlier_token_control",
        RAWE,
        {"GITLAB": "http://gitlab.invalid:10101", "REDDIT": "http://reddit.invalid:10102",
         "SHOPPING": "http://shopping.invalid:10103", "SHOPPING_ADMIN": "http://shopping-admin.invalid:10104",
         "WIKIPEDIA": "http://wikipedia.invalid:10105", "MAP": "http://map.invalid:10306/__GITLAB__"},
        "control: value containing an EARLIER token — both methods leave it literal (order asymmetry)",
    )

    RAWF = '{"task_id": 5, "intent": "top __WIKIPEDIA__ \\u2122 item", "start_url": "__WIKIPEDIA__"}'
    # H5: escaped source text around a token (\u2122 adjacent) — D1 family probe
    run_case(
        "H5_escaped_text_adjacent",
        RAWF,
        {"GITLAB": "http://gitlab.invalid:10101", "REDDIT": "http://reddit.invalid:10102",
         "SHOPPING": "http://shopping.invalid:10103", "SHOPPING_ADMIN": "http://shopping-admin.invalid:10104",
         "WIKIPEDIA": "http://wikipedia.invalid:10105", "MAP": "http://map.invalid:10106"},
        "escaped source text (\\u2122) adjacent to tokens; probes D1 escape-straddle direction that DOES match",
    )
    return cases


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hands", action="store_true")
    ap.add_argument("--json-path", type=Path, default=Path(__file__).resolve().parent / "instr_json.out")
    args = ap.parse_args()
    if args.hands:
        print(json.dumps(run_hands(), indent=1, ensure_ascii=False))
        return 0
    out = run_frozen(args.json_path if args.json_path.exists() else None)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    rc = 1 if (out["pin_findings"] or out["totals"]["mismatches"]) else 0
    return rc


if __name__ == "__main__":
    sys.exit(main())

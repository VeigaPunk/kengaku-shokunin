#!/usr/bin/env python3
"""Read-only stdlib census for R29ReverseDeadField247 (task 247 reference_url).

Pinned bytes are read once into memory and verified by sha256. The raw fixture is
parsed with json only. evaluators.py and helper_functions.py are parsed with ast.parse
only: never imported, compiled for execution, or executed. profiles.json values are
synthetic *.invalid fixture strings used only for in-memory str.replace. Writes only
census.json into this seat's scratch directory.
"""
import ast
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRATCH = LANE / ".ufo/waves/round-29/scratch/KengakuR28.R29ReverseDeadField247-2"
PIN = {
    "raw": ("plans/fixtures/r28/webarena/config_files/test.raw.json",
            "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652", 880776),
    "evaluators": ("plans/fixtures/r28/webarena/evaluation_harness/evaluators.py",
                   "e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22", 13264),
    "helpers": ("plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py",
                "ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275", 7565),
    "profiles": ("plans/fixtures/r29/profiles.json",
                 "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018", None),
}
# plans/fixtures/r29/manifest.json replacement_order (frozen)
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {t: "__" + t + "__" for t in ORDER}
MARKERS = ["__last_url__", "__page__"]
URL_LIKE = re.compile(r"^(https?://|__[A-Z_]+__)")
PROFILE_NAMES = ["distinct_origins", "path_prefix", "trailing_slash_sensitivity"]
KEYS_EVAL = {
    "reference_url", "url_match", "string_match", "eval_types", "reference_answers",
    "fuzzy_match", "exact_match", "must_include", "string_note", "intent", "program_html",
    "url_note", "reference_answer_raw_annotation", "start_url", "task_id", "sites", "eval",
    "required_contents", "url", "locator", "__last_url__", "__page__",
}
CALLS = {"URLEvaluator", "StringEvaluator", "HTMLContentEvaluator", "EvaluatorComb",
         "evaluator_router", "eval", "exec"}
NONSTR_KINDS = ("null", "empty", "non-string")


def pinned(name):
    rel, sha, size = PIN[name]
    data = (LANE / rel).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != sha or (size is not None and len(data) != size):
        raise SystemExit(f"PIN MISMATCH {name}: sha256={digest} bytes={len(data)}")
    return data


def toks(s):
    return {t: s.count(v) for t, v in TOK.items() if s.count(v)}


def markers(s):
    return {m: s.count(m) for m in MARKERS if s.count(m)}


def kind_of(ref):
    if ref is None:
        return "null"
    if not isinstance(ref, str):
        return "non-string"
    if ref == "":
        return "empty"
    return "url-like" if URL_LIKE.match(ref) else "prose/other"


def project(text, vals, order=ORDER):
    counts = {}
    for t in order:
        counts[t] = text.count(TOK[t])
        text = text.replace(TOK[t], vals[t])
    return text, counts


def leaf_project(v, vals):
    return project(v, vals)[0] if isinstance(v, str) else v


def leaf_tokens(node, acc):
    if isinstance(node, dict):
        for k, v in node.items():
            for t, c in toks(k).items():
                acc[t] += c
            leaf_tokens(v, acc)
    elif isinstance(node, list):
        for v in node:
            leaf_tokens(v, acc)
    elif isinstance(node, str):
        for t, c in toks(node).items():
            acc[t] += c
    return acc


def ast_rows(name):
    rel = PIN[name][0]
    tree = ast.parse(pinned(name).decode("utf-8"), filename=rel)
    rows, stack = [], []

    class V(ast.NodeVisitor):
        def _scope(self, node):
            stack.append(node.name)
            self.generic_visit(node)
            stack.pop()

        visit_ClassDef = _scope
        visit_FunctionDef = _scope
        visit_AsyncFunctionDef = _scope

        def visit_Constant(self, node):
            if isinstance(node.value, str) and node.value in KEYS_EVAL:
                rows.append(["const", node.lineno, node.value, ".".join(stack) or "<module>"])

        def visit_Call(self, node):
            f = node.func
            nm = f.id if isinstance(f, ast.Name) else getattr(f, "attr", None)
            if nm in CALLS:
                rows.append(["call", node.lineno, nm, ".".join(stack) or "<module>"])
            self.generic_visit(node)

    V().visit(tree)
    return rows


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    raw_bytes = pinned("raw")
    text = raw_bytes.decode("utf-8")
    assert text.isascii(), "non-ASCII raw: codepoint offsets would differ from bytes"

    # Enumerate top-level array elements with codepoint spans (json only, no repair).
    dec = json.JSONDecoder()
    assert text[0] == "["
    spans, i = [], 1
    while True:
        while text[i] in " \t\r\n,":
            i += 1
        if text[i] == "]":
            break
        obj, j = dec.raw_decode(text, i)
        spans.append((i, j, obj))
        i = j
    assert text[i + 1:].strip() == "", "trailing data after top-level array"
    parsed = json.loads(text)
    assert parsed == [o for _, _, o in spans]
    n = len(spans)

    records = []
    for k, (s, e, obj) in enumerate(spans):
        span = text[s:e]
        key = '"reference_url"'
        assert span.count(key) == 1, ("reference_url occurrences", k)
        ev = obj["eval"]
        ref, et = ev["reference_url"], ev["eval_types"]
        # Locate the raw value by skipping the colon and whitespace, then decode one JSON value.
        p = span.index(key) + len(key)
        while span[p] in " \t\r\n:":
            p += 1
        val, vend = dec.raw_decode(span, p)
        assert val == ref
        rs, re_ = s + p, s + vend
        ann = ev.get("reference_answer_raw_annotation")
        note = ev.get("string_note")
        ref_s = ref if isinstance(ref, str) else ""
        records.append({
            "index": k,
            "line": text.count("\n", 0, s) + 1,
            "reference_url_line": text.count("\n", 0, rs) + 1,
            "task_id": obj.get("task_id"),
            "sites": obj.get("sites"),
            "start_url": obj.get("start_url"),
            "start_url_tokens": toks(obj.get("start_url") or ""),
            "eval_keys": sorted(ev.keys()),
            "eval_types": et,
            "scorer_reads_reference_url": "url_match" in et,
            "reference_url": ref,
            "reference_url_raw_cp": [rs, re_],
            "reference_url_kind": kind_of(ref),
            "reference_url_tokens": toks(ref_s),
            "reference_url_markers": markers(ref_s),
            "annotation_type": type(ann).__name__,
            "annotation_tokens": toks(ann if isinstance(ann, str) else ""),
            "string_note_type": type(note).__name__,
            "string_note_tokens": toks(note if isinstance(note, str) else ""),
        })

    by_id = {}
    for r in records:
        by_id.setdefault(r["task_id"], []).append(r["index"])
    assert len(by_id[247]) == 1
    k247 = by_id[247][0]
    r247 = records[k247]

    def cls(r):
        if r["reference_url_kind"] in NONSTR_KINDS:
            return r["reference_url_kind"]
        return "tokens" if r["reference_url_tokens"] else "tokenfree"

    cells = Counter(("url_match" if r["scorer_reads_reference_url"] else "no_url_match", cls(r))
                    for r in records)
    unread_ne = [r for r in records
                 if not r["scorer_reads_reference_url"] and r["reference_url_kind"] not in NONSTR_KINDS]
    read_ne = [r for r in records
               if r["scorer_reads_reference_url"] and r["reference_url_kind"] not in NONSTR_KINDS]
    dec_counts = leaf_tokens(parsed, Counter())
    summary = {
        "raw_bytes": len(raw_bytes),
        "raw_codepoints": len(text),
        "tasks": n,
        "distinct_task_ids": len(by_id),
        "index_equals_task_id": sum(r["index"] == r["task_id"] for r in records),
        "first_index_task_id_mismatch": next(
            ((r["index"], r["task_id"]) for r in records if r["index"] != r["task_id"]), None),
        "task_247_indices": by_id[247],
        "eval_types_combos": [[list(c), v] for c, v in Counter(
            tuple(r["eval_types"]) for r in records).most_common()],
        "reference_url_kind_all": dict(Counter(r["reference_url_kind"] for r in records)),
        "reference_url_2x2": {f"{a}/{b}": v for (a, b), v in sorted(cells.items())},
        "scorer_read_but_null_or_nonstring_or_empty": sum(
            1 for r in records if r["scorer_reads_reference_url"]
            and r["reference_url_kind"] in NONSTR_KINDS),
        "unread_nonempty_count": len(unread_ne),
        "unread_nonempty_kinds": dict(Counter(r["reference_url_kind"] for r in unread_ne)),
        "unread_nonempty_token_bearing": sum(1 for r in unread_ne if r["reference_url_tokens"]),
        "read_nonempty_count": len(read_ne),
        "read_nonempty_kinds": dict(Counter(r["reference_url_kind"] for r in read_ne)),
        "read_nonempty_token_bearing": sum(1 for r in read_ne if r["reference_url_tokens"]),
        "annotation_types": dict(Counter(r["annotation_type"] for r in records)),
        "annotation_token_bearing_tasks": sum(1 for r in records if r["annotation_tokens"]),
        "annotation_token_bearing_unread_tasks": sum(
            1 for r in records if r["annotation_tokens"]),
        "string_note_types": dict(Counter(r["string_note_type"] for r in records)),
        "string_note_token_bearing_tasks": sum(1 for r in records if r["string_note_tokens"]),
        "start_url_token_bearing_tasks": sum(1 for r in records if r["start_url_tokens"]),
        "reference_url_marker_tasks": sum(1 for r in records if r["reference_url_markers"]),
        "raw_vs_decoded_token_counts": {
            t: {"raw_text": text.count(TOK[t]), "decoded_leaves": dec_counts.get(t, 0)}
            for t in ORDER},
        "runtime_marker_raw_counts": {m: text.count(m) for m in MARKERS},
    }

    profiles = json.loads(pinned("profiles"))
    proj = {}
    for name in PROFILE_NAMES:
        vals = profiles[name]["values"]
        assert set(vals) == set(ORDER)
        p_text, counts = project(text, vals)
        p = json.loads(p_text)
        assert len(p) == n
        ref_changed = [k for k in range(n)
                       if p[k]["eval"]["reference_url"] != parsed[k]["eval"]["reference_url"]]
        start_changed = [k for k in range(n) if p[k]["start_url"] != parsed[k]["start_url"]]
        leaf_ok = all(leaf_project(parsed[k]["eval"]["reference_url"], vals)
                      == p[k]["eval"]["reference_url"] for k in range(n))
        fwd, _ = project(text, vals, ORDER)
        rev, _ = project(text, vals, list(reversed(ORDER)))
        proj[name] = {
            "raw_replacements_in_order": counts,
            "parsed_tasks": len(p),
            "reference_url_changed_tasks": len(ref_changed),
            "reference_url_changed_scorer_read": sum(records[k]["scorer_reads_reference_url"]
                                                     for k in ref_changed),
            "reference_url_changed_unread": sum(not records[k]["scorer_reads_reference_url"]
                                                for k in ref_changed),
            "start_url_changed_tasks": len(start_changed),
            "leaf_oracle_agrees_on_reference_url": leaf_ok,
            "forward_equals_reversed_order_full_text": fwd == rev,
            "profile_values_contain_double_underscore": any("__" in v for v in vals.values()),
            "task_247": {
                "index": k247,
                "reference_url_before": r247["reference_url"],
                "reference_url_after": p[k247]["eval"]["reference_url"],
                "reference_url_identical": p[k247]["eval"]["reference_url"] == r247["reference_url"],
                "start_url_before": parsed[k247]["start_url"],
                "start_url_after": p[k247]["start_url"],
            },
        }
    summary["projection"] = proj

    hv = profiles["distinct_origins"]["values"]
    hand = [
        ("Valorie doesn't have a email in the system",
         "Valorie doesn't have a email in the system"),
        ("__SHOPPING_ADMIN__/x", "http://shopping-admin.invalid:10104/x"),
        ("__SHOPPING__ and __SHOPPING_ADMIN__",
         "http://shopping.invalid:10103 and http://shopping-admin.invalid:10104"),
        ("__MAP____WIKIPEDIA__", "http://map.invalid:10106http://wikipedia.invalid:10105"),
    ]
    hw = []
    for inp, exp in hand:
        got, _ = project(inp, hv)
        hw.append({"input": inp, "hand_expected": exp, "actual": got, "match": got == exp})
    # Semantics-only witness with a NON-frozen synthetic map: later-token cascade.
    cascade_vals = {"GITLAB": "G", "REDDIT": "R", "SHOPPING": "__SHOPPING_ADMIN__",
                    "SHOPPING_ADMIN": "X", "WIKIPEDIA": "W", "MAP": "M"}
    fwd_c, _ = project("__SHOPPING__", cascade_vals, ORDER)
    rev_c, _ = project("__SHOPPING__", cascade_vals, list(reversed(ORDER)))
    hw.append({"input": "__SHOPPING__ (non-frozen cascade map)",
               "hand_expected_forward": "X", "hand_expected_reversed": "__SHOPPING_ADMIN__",
               "actual_forward": fwd_c, "actual_reversed": rev_c,
               "match": fwd_c == "X" and rev_c == "__SHOPPING_ADMIN__"})
    summary["hand_witnesses"] = hw

    ev_rows = ast_rows("evaluators")
    help_rows = ast_rows("helpers")
    out = {"summary": summary, "task_247": r247, "records": records,
           "ast_evaluators": ev_rows, "ast_helpers": help_rows}
    (SCRATCH / "census.json").write_text(json.dumps(out, indent=1, ensure_ascii=True) + "\n",
                                         encoding="ascii")

    print(json.dumps(summary, indent=1, ensure_ascii=True))
    print("TASK_247_RECORD", json.dumps(r247, ensure_ascii=True))
    print("AST_EVALUATORS_ROWS", len(ev_rows))
    for row in ev_rows:
        print("AST_EV", row)
    print("AST_HELPERS_ROWS", len(help_rows))
    for row in help_rows:
        print("AST_HELP", row)


if __name__ == "__main__":
    main()

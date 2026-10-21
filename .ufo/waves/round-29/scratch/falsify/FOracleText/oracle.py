#!/usr/bin/env python3
"""Independent oracle for round-29 claim C1 (seat KengakuR29-2.FOracleText-2).

Re-derives the WebArena generated-config projection from the prereg TEXT, the
pinned generator BYTES and the pinned raw/profile inputs. It NEVER reads or
imports plans/config_projection.py; it only diffs its own result against the
instrument's --json OUTPUT (via --diff).

Domain boundary (explicit): offline textual substitution of the six generator
tokens over the frozen synthetic *.invalid profiles; upstream code is parsed
as inert text, never executed or imported; no env values, auth state or
network access. The decoded-leaf view is used only as a cross-check of the
text-level replacement inside this frozen benign domain; quote/backslash or
later-token-cascade hand cases are outside this oracle's equivalence claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
PATHS = {
    "manifest": f"{ROOT}/plans/fixtures/r29/manifest.json",
    "generator": f"{ROOT}/plans/fixtures/r29/generate_test_data.py",
    "profiles": f"{ROOT}/plans/fixtures/r29/profiles.json",
    "raw": f"{ROOT}/plans/fixtures/r28/webarena/config_files/test.raw.json",
}
# Persisted independently in the prereg text (round-29-claims.md).
MANIFEST_SELF_SHA256 = "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87"
URL_FIELD_LAST_SEGMENTS = {"start_url", "url", "reference_url"}
WS = " \t\r\n"


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def esc_pointer_seg(s) -> str:
    s = str(s)
    return s.replace("~", "~0").replace("/", "~1")


def pointer_of(segs) -> str:
    return "/" + "/".join(esc_pointer_seg(s) for s in segs)


def path_template_of(segs) -> str:
    parts = []
    for s in segs[1:]:  # segment 0 is the task index in the outer list
        if isinstance(s, int):
            if parts:
                parts[-1] += "[]"
            else:
                parts.append("[]")
        else:
            parts.append(s)
    return ".".join(parts) if parts else ""


def last_string_segment(segs):
    for s in reversed(segs[1:]):
        if isinstance(s, str):
            return s
    return None


# ---------------------------------------------------------------- raw scanner
def _prev_nonspace(raw: str, i: int) -> str:
    j = i - 1
    while j >= 0 and raw[j] in WS:
        j -= 1
    return raw[j] if j >= 0 else ""


def scan_string_literals(raw: str):
    """Yield (content_start, content_end, segs, is_key) per JSON string literal.

    segs are the logical JSON-pointer segments (tuple, task index included);
    content spans exclude the quotes and are codepoint offsets in `raw`.
    """
    n = len(raw)
    i = 0
    frames: list[dict] = []  # {"kind","segs","key","idx"}
    in_str = False
    esc = False
    start = -1

    def complete_value(frame: dict) -> None:
        if frame["kind"] == "obj":
            frame["key"] = None
        else:
            frame["idx"] += 1

    while i < n:
        c = raw[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
                content = raw[start + 1:i]
                j = i + 1
                while j < n and raw[j] in WS:
                    j += 1
                top = frames[-1]
                is_key = top["kind"] == "obj" and j < n and raw[j] == ":"
                if is_key:
                    segs = top["segs"] + (content,)
                    top["key"] = content
                else:
                    seg = top["key"] if top["kind"] == "obj" else top["idx"]
                    segs = top["segs"] + (seg,)
                    complete_value(top)
                yield (start + 1, i, segs, is_key)
            i += 1
            continue
        if c == '"':
            in_str = True
            esc = False
            start = i
        elif c in "{[":
            kind = "obj" if c == "{" else "arr"
            top = frames[-1] if frames else None
            if top is None:
                child_segs = ()
            elif top["kind"] == "obj":
                child_segs = top["segs"] + (top["key"],)
                top["key"] = None
            else:
                child_segs = top["segs"] + (top["idx"],)
                top["idx"] += 1
            frames.append({"kind": kind, "segs": child_segs, "key": None, "idx": 0})
        elif c in "}]":
            if _prev_nonspace(raw, i).isalnum():
                complete_value(frames[-1])  # trailing scalar before the bracket
            frames.pop()
        elif c == ",":
            if _prev_nonspace(raw, i).isalnum():
                complete_value(frames[-1])  # scalar element/value completed
        i += 1


# ------------------------------------------------------------- leaf scanning
def walk_leaves(orig, proj, structural: list):
    """Lockstep walk of two parsed trees; yields (segs, o, p) leaves."""
    out = []

    def rec(o, p, segs):
        if isinstance(o, str) and isinstance(p, str):
            out.append((segs, o, p))
            return
        if isinstance(o, dict) and isinstance(p, dict):
            if o.keys() != p.keys():
                structural.append({"pointer": pointer_of(segs), "issue": "key_sets_differ"})
            for k in o:
                if k in p:
                    rec(o[k], p[k], segs + (k,))
            return
        if isinstance(o, list) and isinstance(p, list):
            if len(o) != len(p):
                structural.append({"pointer": pointer_of(segs), "issue": "lengths_differ"})
            for idx in range(min(len(o), len(p))):
                rec(o[idx], p[idx], segs + (idx,))
            return
        out.append((segs, o, p))  # scalar or mixed-type leaf

    rec(orig, proj, ())
    return out


def iter_string_leaves(node, segs=()):
    if isinstance(node, str):
        yield segs, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from iter_string_leaves(v, segs + (k,))
    elif isinstance(node, list):
        for idx, v in enumerate(node):
            yield from iter_string_leaves(v, segs + (idx,))


# --------------------------------------------------------- generator contract
def extract_source_contract(src: str) -> dict:
    lines = src.split("\n")
    steps = []
    for lineno, line in enumerate(lines, start=1):
        m = re.search(
            r'raw\s*=\s*raw\.replace\(\s*"(__[A-Z_]+__)"\s*,\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)',
            line,
        )
        if m:
            steps.append({"line": lineno, "token": m.group(1), "name": m.group(2)})
    parse_line = next((i for i, l in enumerate(lines, 1) if re.search(r"json\.loads\(\s*raw\s*\)", l)), None)
    enum_line = next((i for i, l in enumerate(lines, 1) if "enumerate(" in l), None)
    fname_tpl = None
    for l in lines:
        m = re.search(r'f"([^"]*\{idx\}[^"]*)"', l)
        if m:
            fname_tpl = m.group(1)
            break
    return {
        "replace_steps": steps,
        "parse_line": parse_line,
        "enumerate_loop_line": enum_line,
        "per_task_filename_template": fname_tpl,
    }


# ------------------------------------------------------------------- pipeline
def build() -> tuple[dict, list, int]:
    findings: list[dict] = []
    blobs = {k: open(p, "rb").read() for k, p in PATHS.items()}  # each input read ONCE

    manifest = json.loads(blobs["manifest"].decode("utf-8"))
    texts = {k: blobs[k].decode("utf-8") for k in ("generator", "profiles", "raw")}
    raw_ascii = texts["raw"].isascii()

    # --- manifest authentication -------------------------------------------
    if sha256_text(blobs["manifest"].decode("utf-8")) != MANIFEST_SELF_SHA256:
        findings.append({"code": "manifest_tampered"})
    for key, mpath in (
        ("generator", "plans/fixtures/r29/generate_test_data.py"),
        ("raw", "plans/fixtures/r28/webarena/config_files/test.raw.json"),
        ("profiles", "plans/fixtures/r29/profiles.json"),
    ):
        want = manifest["files"][mpath]["sha256"]
        got = sha256_text(texts[key])
        if got != want:
            findings.append({"code": "snapshot_tampered", "path": mpath, "expected": want, "observed": got})

    # --- source contract from generator bytes ------------------------------
    contract = extract_source_contract(texts["generator"])
    steps = contract["replace_steps"]
    if len(steps) != 6:
        findings.append({"code": "source_contract_unrecognized", "replace_steps": len(steps)})
    if [s["name"] for s in steps] != list(manifest.get("replacement_order", [])):
        findings.append({"code": "replacement_order_mismatch"})

    # --- profiles ----------------------------------------------------------
    profiles = json.loads(texts["profiles"])
    if len(profiles) != 3:
        findings.append({"code": "profile_count", "observed": len(profiles)})
    for pname, pdef in profiles.items():
        vals = pdef.get("values")
        if not isinstance(vals, dict) or set(vals.keys()) != {s["name"] for s in steps}:
            findings.append({"code": "profile_missing_key_or_type", "profile": pname})
        elif not all(isinstance(v, str) for v in vals.values()):
            findings.append({"code": "profile_missing_key_or_type", "profile": pname})

    # --- raw population ----------------------------------------------------
    raw_tasks = json.loads(texts["raw"])
    if not isinstance(raw_tasks, list):
        findings.append({"code": "projection_json_invalid", "stage": "raw"})
        raw_tasks = []
    task_ids = [t.get("task_id") for t in raw_tasks if isinstance(t, dict)]
    tokens = [s["token"] for s in steps]
    tok_by_name = {s["name"]: s["token"] for s in steps}

    # original-text token occurrences via own scanner (provenance)
    tree = {}
    for segs, val in iter_string_leaves(raw_tasks):
        tree[pointer_of(segs)] = val

    provenance = []
    tok_followed_by_slash = 0
    for content_start, content_end, segs, is_key in scan_string_literals(texts["raw"]):
        if is_key:
            continue
        content = texts["raw"][content_start:content_end]
        for tok in tokens:
            at = 0
            while True:
                idx = content.find(tok, at)
                if idx < 0:
                    break
                off = content_start + idx
                followed = off + len(tok) < len(texts["raw"]) and texts["raw"][off + len(tok)] == "/"
                tok_followed_by_slash += 1 if followed else 0
                provenance.append({
                    "token": tok,
                    "json_pointer": pointer_of(segs),
                    "path_template": path_template_of(segs),
                    "string_role": "value",
                    "task_index": segs[0] if segs else None,
                    "original_input_codepoint_offset": off,
                    "followed_by_slash": followed,
                })
                at = idx + len(tok)
    # cross-check scanner rows against the parsed tree
    for row in provenance:
        leaf = tree.get(row["json_pointer"])
        if not isinstance(leaf, str) or row["token"] not in leaf:
            findings.append({"code": "scanner_tree_disagreement", "pointer": row["json_pointer"], "token": row["token"]})
            break

    occ_by_token = Counter(p["token"] for p in provenance)
    tasks_with_token = {tok: len({p["task_index"] for p in provenance if p["token"] == tok}) for tok in tokens}
    marker_re = re.compile(r"__[a-z_]+__")
    other_markers = Counter(m for m in marker_re.findall(texts["raw"]) if m not in tokens)

    # --- per-profile projection -------------------------------------------
    profile_blocks = {}
    task_blocks = {}
    for pname, pdef in profiles.items():
        vals = pdef["values"]
        text = texts["raw"]
        steps_out = []
        for s in steps:
            cnt = text.count(s["token"])
            steps_out.append({"name": s["name"], "token": s["token"], "applied_replacements": cnt})
            text = text.replace(s["token"], vals[s["name"]])
        proj_tasks = json.loads(text)
        proj_tree = {pointer_of(segs): v for segs, v in iter_string_leaves(proj_tasks)}

        structural: list = []
        leaves = walk_leaves(raw_tasks, proj_tasks, structural)
        if structural:
            findings.append({"code": "structural_drift", "profile": pname, "detail": structural[:5]})
        string_leaf_count = sum(1 for _, o, p in leaves if isinstance(o, str) and isinstance(p, str))

        changed = []
        for segs, o, p in leaves:
            if isinstance(o, str) and isinstance(p, str) and o != p:
                toks = [t for t in tokens if t in o]
                cat = "url_field" if last_string_segment(segs) in URL_FIELD_LAST_SEGMENTS else "non_url_field"
                changed.append({
                    "json_pointer": pointer_of(segs),
                    "path_template": path_template_of(segs),
                    "category": cat,
                    "original": o,
                    "projected": p,
                    "tokens": toks,
                    "occurrence_total": sum(o.count(t) for t in tokens),
                })
        changed_leaf_count = len(changed)
        changed_task_count = len({c["json_pointer"].split("/")[1] for c in changed})
        multi = sum(1 for c in changed if c["occurrence_total"] > 1)
        by_token = {tok: sum(1 for c in changed if tok in c["tokens"]) for tok in tokens}
        changed_tasks_by_token = {
            tok: len({c["json_pointer"].split("/")[1] for c in changed if tok in c["tokens"]}) for tok in tokens
        }
        by_cat = Counter(c["category"] for c in changed)
        by_tpl = Counter(c["path_template"] for c in changed)
        remaining_text = {tok: text.count(tok) for tok in tokens}
        remaining_dec = {tok: sum(v.count(tok) for v in proj_tree.values() if isinstance(v, str)) for tok in tokens}

        # decoded-leaf equivalence cross-check (benign-domain disclosure)
        equiv = 0
        for c in changed:
            expect = c["original"]
            for s in steps:
                expect = expect.replace(s["token"], vals[s["name"]])
            if expect == c["projected"]:
                equiv += 1

        junctions = tok_followed_by_slash if vals[steps[0]["name"]].endswith("/") else 0
        profile_blocks[pname] = {
            "purpose": pdef.get("purpose"),
            "string_leaf_count": string_leaf_count,
            "parsed_task_count": len(proj_tasks),
            "changed_leaf_count": changed_leaf_count,
            "changed_task_count": changed_task_count,
            "changed_leaves_with_multiple_occurrences": multi,
            "changed_leaves_by_category": dict(by_cat),
            "changed_leaves_by_path_template": dict(by_tpl),
            "changed_leaves_by_token": by_token,
            "changed_tasks_by_token": changed_tasks_by_token,
            "remaining_known_tokens_text": remaining_text,
            "remaining_known_tokens_decoded": remaining_dec,
            "projected_text_sha256": sha256_text(text),
            "steps": steps_out,
            "stimulus_observations": {"value_slash_then_raw_slash_junctions": junctions},
            "decoded_leaf_equivalent_changes": equiv,
        }

        recs = []
        per_task_changed: dict[str, list] = {}
        for c in changed:
            per_task_changed.setdefault(c["json_pointer"].split("/")[1], []).append(
                {k: c[k] for k in ("json_pointer", "original", "projected", "tokens", "path_template", "category")}
            )
        for idx, item in enumerate(proj_tasks):
            tid = item.get("task_id")
            recs.append({
                "output_index": idx,
                "output_filename": contract["per_task_filename_template"].format(idx=idx),
                "task_id": tid,
                "index_equals_task_id": idx == tid,
                "would_be_file_sha256": sha256_text(json.dumps(item, indent=2)),
                "changed_leaves": per_task_changed.get(str(idx), []),
                "projected_task": item,
            })
        task_blocks[pname] = recs

    index_equal = sum(1 for p in task_blocks.values() for r in p if r["index_equals_task_id"])
    violations = [
        {"profile": pn, "output_index": r["output_index"], "task_id": r["task_id"]}
        for pn, rs in task_blocks.items() for r in rs if not r["index_equals_task_id"]
    ]

    result = {
        "manifest_sha256": sha256_text(blobs["manifest"].decode("utf-8")),
        "raw_text_sha256": sha256_text(texts["raw"]),
        "raw_is_ascii": raw_ascii,
        "upstream_revision": manifest.get("upstream_revision"),
        "inputs": {
            "plans/fixtures/r28/webarena/config_files/test.raw.json": sha256_text(texts["raw"]),
            "plans/fixtures/r29/generate_test_data.py": sha256_text(texts["generator"]),
            "plans/fixtures/r29/profiles.json": sha256_text(texts["profiles"]),
        },
        "source_contract": contract,
        "population": {
            "input_task_count": len(raw_tasks),
            "distinct_task_ids": len(set(task_ids)),
            "profile_count": len(profiles),
            "task_profile_projections": len(profiles) * len(raw_tasks),
            "tasks_with_any_token": len({p["task_index"] for p in provenance}),
            "original_occurrences_by_token": {t: occ_by_token.get(t, 0) for t in tokens},
            "tasks_with_token": tasks_with_token,
            "occurrence_roles": {"value": len(provenance)},
            "other_double_underscore_markers": dict(sorted(other_markers.items())),
            "tokens_followed_by_slash": tok_followed_by_slash,
        },
        "index_mapping": {
            "output_index_rule": "enumerate position",
            "index_equals_task_id": index_equal,
            "violations": violations,
        },
        "occurrence_provenance": provenance,
        "profiles": profile_blocks,
        "tasks": task_blocks,
        "findings": findings,
    }
    exit_code = 2 if any(f["code"] in {"manifest_tampered", "snapshot_tampered", "source_contract_unrecognized",
                                       "profile_missing_key_or_type", "projection_json_invalid"} for f in findings) else (1 if findings else 0)
    return result, findings, exit_code


# ------------------------------------------------------------------- diffing
def deep_diff(a, b, loc, out):
    if type(a) is not type(b):
        out.append((loc, a, b))
        return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((f"{loc}.{k}", a.get(k, "<absent>"), b.get(k, "<absent>")))
            else:
                deep_diff(a[k], b[k], f"{loc}.{k}", out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((f"{loc}[len]", len(a), len(b)))
        for i in range(min(len(a), len(b))):
            deep_diff(a[i], b[i], f"{loc}[{i}]", out)
    elif a != b:
        out.append((loc, a, b))


def diff_against_instrument(mine: dict, inst_path: str):
    inst = json.load(open(inst_path))
    dis: list[tuple[str, object, object]] = []
    notes: list[str] = []

    for k in ("manifest_sha256", "raw_text_sha256", "upstream_revision"):
        if mine[k] != inst.get(k):
            dis.append((k, mine[k], inst.get(k)))
    deep_diff(mine["inputs"], inst.get("inputs"), "inputs", dis)
    for k, v in mine["population"].items():
        if inst["population"].get(k) != v:
            dis.append((f"population.{k}", v, inst["population"].get(k)))
    for k, v in mine["index_mapping"].items():
        if k == "output_index_rule":
            if inst["index_mapping"].get(k) != v:
                notes.append(f"wording index_mapping.output_index_rule: oracle={v!r} instrument={inst['index_mapping'].get(k)!r}")
        elif inst["index_mapping"].get(k) != v:
            dis.append((f"index_mapping.{k}", v, inst["index_mapping"].get(k)))
    sc = inst.get("source_contract", {})
    for s in mine["source_contract"]["replace_steps"]:
        want = {"line": s["line"], "name": s["name"], "token": s["token"]}
        if want not in sc.get("replace_steps", []):
            dis.append((f"source_contract.replace_steps[{s['name']}]", want, sc.get("replace_steps")))
    for k in ("parse_line", "enumerate_loop_line", "per_task_filename_template"):
        if mine["source_contract"].get(k) != sc.get(k):
            dis.append((f"source_contract.{k}", mine["source_contract"].get(k), sc.get(k)))

    # provenance: multiset of comparable rows + order check
    def prow(p):
        return (p["token"], p["json_pointer"], p["original_input_codepoint_offset"], p["path_template"],
                p["string_role"], p["task_index"])
    mine_rows = [prow(p) for p in mine["occurrence_provenance"]]
    inst_rows = [prow(p) for p in inst["occurrence_provenance"]]
    if Counter(mine_rows) != Counter(inst_rows):
        only_mine = Counter(mine_rows) - Counter(inst_rows)
        only_inst = Counter(inst_rows) - Counter(mine_rows)
        dis.append(("occurrence_provenance.multiset", dict(only_mine), dict(only_inst)))
    elif mine_rows != inst_rows:
        notes.append(f"occurrence_provenance multiset equal but row order differs (n={len(mine_rows)})")

    if inst.get("findings") != []:
        notes.append(f"instrument findings non-empty: {inst.get('findings')!r}")

    for pname, pb in mine["profiles"].items():
        ip = inst["profiles"].get(pname, {})
        for k, v in pb.items():
            if k in ("purpose",):
                if ip.get(k) != v:
                    dis.append((f"profiles.{pname}.{k}", v, ip.get(k)))
            elif k == "stimulus_observations":
                deep_diff(v, ip.get(k, {}), f"profiles.{pname}.stimulus_observations", dis)
            elif k == "steps":
                for s in v:
                    want = {"applied_replacements": s["applied_replacements"], "name": s["name"], "token": s["token"]}
                    if want not in ip.get("steps", []):
                        dis.append((f"profiles.{pname}.steps[{s['name']}]", want, ip.get("steps")))
            else:
                if k not in ip:
                    notes.append(f"oracle-only diagnostic profiles.{pname}.{k}={v!r} (no instrument counterpart)")
                elif ip.get(k) != v:
                    dis.append((f"profiles.{pname}.{k}", v, ip.get(k)))
        if "stimulus_class" in ip:
            notes.append(f"instrument-only wording profiles.{pname}.stimulus_class: {ip['stimulus_class']!r}")

    # all 2436 task records
    cmp_records = 0
    cmp_leaves = 0
    cmp_proj = 0
    for pname, recs in mine["tasks"].items():
        irecs = inst["profiles"].get(pname, {}).get("tasks", [])
        if len(recs) != len(irecs):
            dis.append((f"tasks.{pname}[len]", len(recs), len(irecs)))
        for i, (m, n) in enumerate(zip(recs, irecs)):
            for k in ("output_index", "output_filename", "task_id", "index_equals_task_id", "would_be_file_sha256"):
                cmp_records += 1
                if m[k] != n.get(k):
                    dis.append((f"tasks.{pname}[{i}].{k}", m[k], n.get(k)))
            cmp_proj += 1
            dd = []
            deep_diff(m["projected_task"], n.get("projected_task"), f"tasks.{pname}[{i}].projected_task", dd)
            dis.extend(dd)
            ml, nl = m["changed_leaves"], n.get("changed_leaves", [])
            cmp_leaves += len(ml)
            if len(ml) != len(nl):
                dis.append((f"tasks.{pname}[{i}].changed_leaves[len]", len(ml), len(nl)))
            for j, (a, b) in enumerate(zip(ml, nl)):
                for k in ("json_pointer", "original", "projected", "path_template", "category"):
                    if a[k] != b.get(k):
                        dis.append((f"tasks.{pname}[{i}].changed_leaves[{j}].{k}", a[k], b.get(k)))
                if Counter(a["tokens"]) != Counter(b.get("tokens", [])):
                    dis.append((f"tasks.{pname}[{i}].changed_leaves[{j}].tokens", a["tokens"], b.get("tokens")))

    return dis, notes, {
        "task_records_compared": sum(len(v) for v in mine["tasks"].values()),
        "record_scalar_field_comparisons": cmp_records,
        "projected_tasks_deep_compared": cmp_proj,
        "changed_leaves_compared": cmp_leaves,
        "provenance_rows_compared": len(mine_rows),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="independent oracle for round-29 C1")
    ap.add_argument("--json", action="store_true", help="print oracle result JSON")
    ap.add_argument("--diff", metavar="INSTRUMENT_JSON", help="diff against instrument --json output")
    args = ap.parse_args()

    result, findings, code = build()
    if args.json:
        print(json.dumps(result, indent=1))
    if args.diff:
        dis, notes, tallies = diff_against_instrument(result, args.diff)
        print(f"DISAGREEMENTS {len(dis)}")
        for loc, a, b in dis[:200]:
            print(f"MISMATCH {loc}\n  oracle    ={json.dumps(a)[:400]}\n  instrument={json.dumps(b)[:400]}")
        if len(dis) > 200:
            print(f"... {len(dis) - 200} more disagreements (truncated display)")
        print("NOTES (wording/instrument-only fields, not disagreements)")
        for nt in notes:
            print(f"NOTE {nt}")
        print("TALLIES " + json.dumps(tallies))
        print(f"ORACLE_FINDINGS {json.dumps(findings)}")
        return 0 if not dis else 1
    if args.json:
        pass
    else:
        print(json.dumps({"findings": findings, "population": result["population"]}, indent=1))
    return code


if __name__ == "__main__":
    sys.exit(main())

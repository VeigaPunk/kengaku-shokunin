#!/usr/bin/env python3
"""Independent census for round-29 eval.reference_url leaf attack.

Derived only from: prereg TEXT (plans/round-29-claims.md), pinned generator bytes,
pinned raw task file, pinned profiles. Does NOT read plans/config_projection.py.
"""
import hashlib
import json
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = LANE + "/plans/fixtures/r29/profiles.json"
GEN = LANE + "/plans/fixtures/r29/generate_test_data.py"
MAN = LANE + "/plans/fixtures/r29/manifest.json"

TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__",
          "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
URL_TEMPLATES = {"start_url", "eval.reference_url", "eval.program_html[].url"}


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_text(t):
    return sha256_bytes(t.encode("utf-8"))


def project_text(raw_text, values):
    text = raw_text
    applied = {}
    for name in ORDER:
        token = "__" + name + "__"
        applied[token] = text.count(token)
        text = text.replace(token, values[name])
    return text, applied


def template_of(pointer):
    """Map a JSON pointer to the prereg path-template naming."""
    parts = pointer.lstrip("/").split("/")
    # drop task list index
    parts = parts[1:]
    out = []
    for p in parts:
        if p.isdigit():
            if out and out[-1] == "program_html":
                continue  # list element marker handled below
            out.append("[]")
        else:
            out.append(p)
    name = ".".join(out)
    # canonical list forms used by the instrument/claim text
    name = name.replace("program_html.[].required_contents.must_include.[]", "program_html[].required_contents.must_include[]")
    name = name.replace("program_html.[].url", "program_html[].url")
    return name


def walk(obj, pointer="", acc=None):
    if acc is None:
        acc = []
    if isinstance(obj, str):
        acc.append((pointer, obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            walk(v, pointer + "/" + str(k), acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, pointer + "/" + str(i), acc)
    return acc


def main():
    raw_b = open(RAW, "rb").read()
    print("raw_sha256", sha256_text(raw_b.decode("utf-8")), "size", len(raw_b))
    raw_text = raw_b.decode("utf-8")
    raw = json.loads(raw_text)
    prof = json.load(open(PROF))
    manifest = json.load(open(MAN))
    gen = open(GEN, "rb").read().decode("utf-8")
    print("generator_sha256", sha256_bytes(gen.encode("utf-8")))
    print("manifest_sha256", sha256_bytes(open(MAN, "rb").read()))
    # confirm generator replacement contract from its bytes
    gen_tokens = [t for t in TOKENS if ('"' + t + '"') in gen]
    print("generator_tokens_present", gen_tokens)
    print("generator_order_occurrences", [gen.index('"' + t + '"') for t in TOKENS])

    # raw occurrence census at root and at eval.reference_url
    root_occ = {t: raw_text.count(t) for t in TOKENS}
    print("raw_root_occurrences", json.dumps(root_occ, sort_keys=True))

    leaves = walk(raw)
    ref_leaves = [(i, ptr, v) for (ptr, v) in leaves
                  for i in [int(ptr.split("/")[1])]
                  if template_of(ptr) == "eval.reference_url"]
    # simpler explicit pass for reference_url
    ref = []
    for idx, task in enumerate(raw):
        v = task["eval"].get("reference_url")
        ref.append((idx, v))
    str_ref = [(i, v) for i, v in ref if isinstance(v, str)]
    tok_ref = []
    for i, v in str_ref:
        cnt = {t: v.count(t) for t in TOKENS if v.count(t)}
        if cnt:
            tok_ref.append((i, v, cnt))
    print("reference_url_total", len(ref),
          "string", len(str_ref),
          "non_string", len(ref) - len(str_ref),
          "with_token", len(tok_ref),
          "byte_empty", sum(1 for i, v in str_ref if v == ""))
    tok_occ = {t: sum(c.get(t, 0) for _, _, c in tok_ref) for t in TOKENS}
    print("reference_url_token_occurrences", json.dumps(tok_occ, sort_keys=True))

    # per-profile projection and leaf diff
    out = {}
    for pname, pdata in prof.items():
        values = pdata["values"]
        projected_text, applied = project_text(raw_text, values)
        print("PROFILE", pname, "applied", json.dumps(applied, sort_keys=True),
              "projected_sha256", sha256_text(projected_text))
        pt = json.loads(projected_text)
        if len(pt) != len(raw):
            print("TASK COUNT MISMATCH", len(pt), len(raw))
        changed = []          # (idx, pointer, template, original, projected, tokens)
        cat = {"url_field": 0, "non_url_field": 0}
        by_tmpl = {}
        ref_changed = []
        leaf_level_mismatch = []
        for idx, (task_o, task_p) in enumerate(zip(raw, pt)):
            lo = walk(task_o, "/" + str(idx))
            lp = walk(task_p, "/" + str(idx))
            po = {p: v for p, v in lo}
            pp = {p: v for p, v in lp}
            if len(lo) != len(lp):
                print("LEAF COUNT MISMATCH task", idx, len(lo), len(lp))
            for ptr, ov in lo:
                pv = pp.get(ptr)
                if ov != pv:
                    tmpl = template_of(ptr)
                    toks = [t for t in TOKENS if t in ov]
                    category = "url_field" if tmpl in URL_TEMPLATES else "non_url_field"
                    cat[category] += 1
                    by_tmpl[tmpl] = by_tmpl.get(tmpl, 0) + 1
                    changed.append((idx, ptr, tmpl, category, ov, pv, toks))
                    if tmpl == "eval.reference_url":
                        ref_changed.append((idx, ov, pv, toks))
                    # independent leaf-level replacement equivalence
                    lv = ov
                    for name in ORDER:
                        lv = lv.replace("__" + name + "__", values[name])
                    if lv != pv:
                        leaf_level_mismatch.append((idx, ptr, ov, pv, lv))
        print("PROFILE", pname, "changed_leaves", len(changed),
              "by_category", json.dumps(cat, sort_keys=True),
              "by_template", json.dumps(by_tmpl, sort_keys=True),
              "changed_tasks", len({c[0] for c in changed}),
              "ref_changed", len(ref_changed),
              "leaf_level_mismatch", len(leaf_level_mismatch))
        out[pname] = {
            "changed_leaf_count": len(changed),
            "by_category": cat,
            "by_template": by_tmpl,
            "ref_changed": ref_changed,
            "leaf_level_mismatch": leaf_level_mismatch,
        }
        # verify every reference_url leaf with a token is changed, and no other
        changed_ref_idx = {i for i, *_ in ref_changed}
        tok_ref_idx = {i for i, _, _ in tok_ref}
        print("PROFILE", pname, "ref_missing_changed",
              sorted(tok_ref_idx - changed_ref_idx),
              "ref_changed_without_token", sorted(changed_ref_idx - tok_ref_idx))
    json.dump(out, open(sys.argv[1], "w"))


if __name__ == "__main__":
    main()

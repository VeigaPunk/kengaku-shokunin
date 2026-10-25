"""Independent re-derivation of ordered text-replacement + parse + leaf diff.

Derived from the prereg TEXT (round-29-claims.md), the pinned generator bytes
(scripts/generate_test_data.py: six sequential str.replace on the whole file, then
json.loads), and the pinned raw task file.  Does NOT read or import
plans/config_projection.py.
"""
import hashlib
import json
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT + "/plans/fixtures/r29/profiles.json"

ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOKEN = {k: "__%s__" % k for k in ORDER}
URL_TEMPLATES = {"start_url", "eval.reference_url", "eval.program_html[].url"}


def walk(obj, path=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, path + (i,))
    else:
        yield path, obj


def template(path):
    # path[0] is the top-level task index; templates are task-relative
    assert isinstance(path[0], int)
    out = []
    for p in path[1:]:
        if isinstance(p, int):
            out[-1] += "[]"
        else:
            out.append(p)
    return ".".join(out)


def pointer(path):
    def esc(s):
        return s.replace("~", "~0").replace("/", "~1")

    return "".join(
        "/%d" % p if isinstance(p, int) else "/" + esc(p) for p in path
    )


def leaves_by_pointer(obj):
    return {pointer(p): (p, v) for p, v in walk(obj)}


def project(text, values):
    steps = []
    cur = text
    for name in ORDER:
        tok = TOKEN[name]
        n = cur.count(tok)
        cur = cur.replace(tok, values[name])
        steps.append({"name": name, "token": tok, "count": n})
    return cur, steps


def main():
    text = open(RAW, "r", encoding="utf-8", newline="").read()
    profiles = json.load(open(PROF))
    base = json.loads(text)
    base_leaves = leaves_by_pointer(base)
    print("raw sha256", hashlib.sha256(
        open(RAW, "rb").read()).hexdigest())
    print("base tasks", len(base), "base leaves", len(base_leaves),
          "string leaves",
          sum(1 for _, v in base_leaves.values() if isinstance(v, str)))

    report = {}
    for prof_name in ("distinct_origins", "path_prefix",
                      "trailing_slash_sensitivity"):
        values = profiles[prof_name]["values"]
        proj_text, steps = project(text, values)
        proj = json.loads(proj_text)
        proj_leaves = leaves_by_pointer(proj)
        assert set(base_leaves) == set(proj_leaves), "leaf pointer set changed"
        changed = []
        for ptr, (path, ov) in base_leaves.items():
            pv = proj_leaves[ptr][1]
            if ov != pv:
                changed.append({
                    "pointer": ptr,
                    "template": template(path),
                    "original": ov,
                    "projected": pv,
                    "tokens": [TOKEN[n] for n in ORDER
                               if isinstance(ov, str) and TOKEN[n] in ov],
                })
        by_tmpl = {}
        by_cat = {"url_field": 0, "non_url_field": 0}
        for c in changed:
            by_tmpl[c["template"]] = by_tmpl.get(c["template"], 0) + 1
            by_cat["url_field" if c["template"] in URL_TEMPLATES
                   else "non_url_field"] += 1
        multi = 0
        for c in changed:
            occ = sum(c["original"].count(TOKEN[n]) for n in ORDER) \
                if isinstance(c["original"], str) else 0
            if occ > 1:
                multi += 1
        report[prof_name] = {
            "text_sha256": hashlib.sha256(proj_text.encode()).hexdigest(),
            "parsed": len(proj),
            "changed": len(changed),
            "by_template": dict(sorted(by_tmpl.items())),
            "by_category": by_cat,
            "multi_occurrence_leaves": multi,
            "steps": steps,
        }
        # program_html url detail, per task index
        ph = {}
        for c in changed:
            if c["template"] == "eval.program_html[].url":
                task_idx = int(c["pointer"].split("/")[1])
                ph.setdefault(task_idx, []).append(c)
        report[prof_name]["program_html_url_changed"] = len(
            sum(ph.values(), []))
        report[prof_name]["program_html_url_tasks"] = len(ph)
        report[prof_name]["_ph"] = ph
        report[prof_name]["_changed"] = changed

    # census of program_html url leaves in the base
    total = 0
    with_tok = 0
    for p, v in base_leaves.values():
        if template(p) == "eval.program_html[].url":
            total += 1
            if any(TOKEN[n] in v for n in ORDER):
                with_tok += 1
    print("program_html[].url leaves", total, "with token", with_tok)

    for name in report:
        r = report[name]
        print("\nPROFILE", name)
        print("  text_sha256", r["text_sha256"])
        print("  parsed", r["parsed"], "changed", r["changed"])
        print("  by_template", json.dumps(r["by_template"]))
        print("  by_category", json.dumps(r["by_category"]))
        print("  multi_occ_leaves", r["multi_occurrence_leaves"])
        print("  program_html url changed", r["program_html_url_changed"],
              "in tasks", r["program_html_url_tasks"])

    json.dump({k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")}
               for k, v in report.items()},
              open(ROOT + "/.ufo/waves/round-29/scratch/falsify/FPathHtmlUrl/"
                   "oracle_counts.json", "w"), indent=1, sort_keys=True)
    json.dump({k: v["_ph"] for k, v in report.items()},
              open(ROOT + "/.ufo/waves/round-29/scratch/falsify/FPathHtmlUrl/"
                   "oracle_ph.json", "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    sys.exit(main())

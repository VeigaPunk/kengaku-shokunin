"""Independent URL census over pinned raw tasks; stdlib only, no production/oracle import."""
import collections
import json
import re
import sys
import urllib.parse

raw = json.load(open(sys.argv[1]))
out = collections.OrderedDict()
url_tasks = [t for t in raw if "url_match" in t["eval"]["eval_types"]]
out["url_match_tasks"] = len(url_tasks)
out["url_note_explicit"] = collections.Counter(repr(t["eval"]["url_note"]) for t in url_tasks if "url_note" in t["eval"])
out["url_note_absent_ids"] = [t["task_id"] for t in url_tasks if "url_note" not in t["eval"]]
non = [t for t in raw if "url_match" not in t["eval"]["eval_types"]]
out["non_url_tasks"] = len(non)
out["non_url_url_note_values"] = collections.Counter(repr(t["eval"].get("url_note", "<ABSENT>")) for t in non)
out["non_url_reference_url_values"] = collections.Counter("<ABSENT>" if "reference_url" not in t["eval"] else ("<nonempty>" if t["eval"]["reference_url"] else repr(t["eval"]["reference_url"])) for t in non)
orders = collections.Counter(",".join(t["eval"]["eval_types"]) for t in url_tasks)
out["url_eval_orders"] = orders
# scorer-mirrored vacuity: clean_url then netloc+path
vac, delim, alt_counts, query_only = [], [], collections.Counter(), []
for t in url_tasks:
    ref = t["eval"]["reference_url"]
    alts = [a.rstrip("/") for a in ref.split(" |OR| ")]
    alt_counts[len(alts)] += 1
    for a in alts:
        p = urllib.parse.urlparse(a)
        if not (p.netloc + p.path):
            vac.append(t["task_id"])
        if not (p.netloc + p.path) and p.query:
            query_only.append(t["task_id"])
    if re.search(r"\|\s*OR\s*\|", ref) and len(re.findall(r"\|\s*OR\s*\|", ref)) != ref.count(" |OR| "):
        delim.append(t["task_id"])
    if "OR" in ref and "|OR|" not in ref:
        delim.append(t["task_id"])
out["alternative_count_histogram"] = alt_counts
out["vacuous_base_alt_task_ids"] = vac
out["query_only_alt_task_ids"] = query_only
out["malformed_or_delimiter_task_ids"] = delim
# raw-template base: scheme-less placeholders land in path, not netloc
out["refs_with_scheme"] = sum(1 for t in url_tasks if re.match(r"^[a-z]+://", t["eval"]["reference_url"]))
out["refs_starting_placeholder"] = sum(1 for t in url_tasks if all(re.match(r"^__[A-Z_]+__", a) for a in t["eval"]["reference_url"].split(" |OR| ")))
# combo tasks with non-last html targets (navigation would mutate page.url if order reversed)
combo = [t for t in url_tasks if "program_html" in t["eval"]["eval_types"]]
out["combo_tasks"] = len(combo)
out["combo_tasks_with_navigating_target"] = sum(1 for t in combo if any(x["url"] != "last" for x in t["eval"]["program_html"]))
out["combo_url_first"] = sum(1 for t in combo if t["eval"]["eval_types"].index("url_match") < t["eval"]["eval_types"].index("program_html"))
# any OR-like delimiter variants anywhere in raw bytes
text = open(sys.argv[1]).read()
out["raw_or_variants"] = collections.Counter(m.group(0) for m in re.finditer(r".?\|\s*OR\s*\|.?", text))
print(json.dumps(out, indent=1, default=lambda o: dict(o)))

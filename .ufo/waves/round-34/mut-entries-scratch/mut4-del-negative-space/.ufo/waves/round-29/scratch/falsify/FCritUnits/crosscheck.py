"""Compare instrument --json OUTPUT (path argv[1]) against independent census; also unit-label probes."""
import collections, hashlib, json, pathlib, re, sys

ROOT = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
RAW = (ROOT / "plans/fixtures/r28/webarena/config_files/test.raw.json").read_bytes().decode("utf-8")
PROFILES = json.loads((ROOT / "plans/fixtures/r29/profiles.json").read_text("utf-8"))
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
J = json.load(open(sys.argv[1]))
data = json.loads(RAW)
r = {}

prov = J["occurrence_provenance"]
r["prov_len"] = len(prov)
r["prov_distinct_pointers"] = len({p["json_pointer"] for p in prov})
r["prov_distinct_tasks"] = len({p["task_index"] for p in prov})
mult = collections.Counter(p["json_pointer"] for p in prov)
r["prov_pointers_gt1"] = sum(1 for v in mult.values() if v > 1)
r["prov_surplus"] = sum(v - 1 for v in mult.values())
tt = collections.defaultdict(set)
for p in prov:
    tt[p["token"]].add(p["task_index"])
r["prov_tasks_by_token"] = {k: len(v) for k, v in sorted(tt.items())}
r["prov_tasks_by_token_sum"] = sum(len(v) for v in tt.values())
tok_per_task = collections.defaultdict(set)
for p in prov:
    tok_per_task[p["task_index"]].add(p["token"])
two = sorted(i for i, s in tok_per_task.items() if len(s) > 1)
r["two_token_tasks"] = len(two)
r["two_token_task_pairs"] = dict(collections.Counter("+".join(sorted(tok_per_task[i])) for i in two))
r["two_token_task_ids_first10"] = two[:10]
offs_ok = all(RAW[p["original_input_codepoint_offset"]:p["original_input_codepoint_offset"] + len(p["token"])] == p["token"] for p in prov)
r["prov_offsets_codepoint_exact"] = offs_ok

for name, P in J["profiles"].items():
    tasks = P["tasks"]
    cl = sum(len(t["changed_leaves"]) for t in tasks)
    ct = sum(1 for t in tasks if t["changed_leaves"])
    # projected text / would-be file digests
    txt = RAW
    for n in ORDER:
        txt = txt.replace(f"__{n}__", PROFILES[name]["values"][n])
    pdata = json.loads(txt)
    text_sha = hashlib.sha256(txt.encode("utf-8")).hexdigest()
    file_ok = sum(1 for i, t in enumerate(tasks)
                  if hashlib.sha256(json.dumps(pdata[i], indent=2).encode("utf-8")).hexdigest() == t["would_be_file_sha256"])
    obj_ok = sum(1 for i, t in enumerate(tasks) if t["projected_task"] == pdata[i])
    distinct_files = len({t["output_filename"] for t in tasks})
    r[name] = {"tasks_len": len(tasks), "changed_leaves_sum": cl, "changed_tasks": ct,
               "projected_text_sha_matches_utf8_text": text_sha == P["projected_text_sha256"],
               "would_be_file_sha_matches": file_ok, "projected_object_matches": obj_ok,
               "distinct_output_filenames": distinct_files,
               "test_json_digest_field_present_in_tasks": any("test.json" in json.dumps(t.get("output_filename")) for t in tasks),
               "sample_changed_leaf_keys": sorted(tasks[0]["changed_leaves"][0].keys()) if tasks[0]["changed_leaves"] else None}

for m in ["__last_url__", "__page__"]:
    occ = RAW.count(m)
    lv = tk = 0
    def walk(n):
        global lv
        if isinstance(n, str):
            if m in n:
                lv += 1
        elif isinstance(n, dict):
            [walk(v) for v in n.values()]
        elif isinstance(n, list):
            [walk(v) for v in n]
    for t in data:
        before = lv
        walk(t)
        tk += lv > before
    r[m] = {"text_occurrences": occ, "leaves": lv, "tasks": tk}

# '//' junction unit probe (trailing_slash): occurrences followed by '/', and their leaves/tasks
fol = [p for p in prov if RAW[p["original_input_codepoint_offset"] + len(p["token"]):][:1] == "/"]
r["followed_by_slash"] = {"occurrences": len(fol), "leaves": len({p["json_pointer"] for p in fol}),
                          "tasks": len({p["task_index"] for p in fol})}
non_url = [p for p in prov if p["path_template"] in ("eval.program_html[].required_contents.must_include[]", "eval.reference_answer_raw_annotation")]
r["non_url"] = {"occurrences": len(non_url), "leaves": len({p["json_pointer"] for p in non_url}),
                "tasks": len({p["task_index"] for p in non_url})}
json.dump(r, sys.stdout, indent=1)
print()

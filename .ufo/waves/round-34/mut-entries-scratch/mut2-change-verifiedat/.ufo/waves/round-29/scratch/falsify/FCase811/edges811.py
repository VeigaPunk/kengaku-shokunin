#!/usr/bin/env python3
"""Supplementary attacks around the task-811 record: category rule, occurrence
offsets, multi-occurrence token-list shape, digest identity, leftover markers."""
import hashlib
import json
import re
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = ROOT + "/plans/fixtures/r29/profiles.json"
INST = "/tmp/r29_fcase811_json.json"
ORDER = [("GITLAB", "__GITLAB__"), ("REDDIT", "__REDDIT__"),
         ("SHOPPING", "__SHOPPING__"), ("SHOPPING_ADMIN", "__SHOPPING_ADMIN__"),
         ("WIKIPEDIA", "__WIKIPEDIA__"), ("MAP", "__MAP__")]
sha = lambda b: hashlib.sha256(b).hexdigest()

text = open(RAW, "rb").read().decode("utf-8")
profiles = json.load(open(PROFILES))
inst = json.load(open(INST))
orig = json.loads(text)


def project(t, values):
    for name, tok in ORDER:
        t = t.replace(tok, values[name])
    return t


def leaves(a, b, path="", acc=None):
    acc = [] if acc is None else acc
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            leaves(a[k], b[k], path + "/" + k, acc)
    elif isinstance(a, list) and isinstance(b, list):
        for i, (x, y) in enumerate(zip(a, b)):
            leaves(x, y, path + "/" + str(i), acc)
    elif a != b:
        acc.append((path, a, b))
    return acc


def cat(orig_v):
    v = orig_v
    for _, tok in ORDER:
        v = v.replace(tok, "http://H.invalid")
    return "url_field" if re.match(r"^https?://[^/\s]+(?:[/?#]|$)", v) else "non_url_field"


# 1. global category agreement with instrument per profile
for pname in profiles:
    proj = json.loads(project(text, profiles[pname]["values"]))
    counts = {}
    for ti, item in enumerate(orig):
        for p, a, b in leaves(item, proj[ti]):
            c = cat(a)
            counts[c] = counts.get(c, 0) + 1
    print("category_mine[%s]=%s instrument=%s agree=%s"
          % (pname, counts, inst["profiles"][pname]["changed_leaves_by_category"],
             counts == inst["profiles"][pname]["changed_leaves_by_category"]))

# 2. multi-occurrence leaves: what does the instrument's record look like?
print("\n-- multi-occurrence leaf records (instrument) --")
for (ti, ptr) in [(66, "/eval/reference_answer_raw_annotation"), (431, "/start_url"),
                  (682, "/eval/reference_url")]:
    rec = inst["profiles"]["distinct_origins"]["tasks"][ti]
    for lf in rec["changed_leaves"]:
        if lf["path_template"].startswith(ptr.strip("/").replace("/", ".")) or \
           lf["json_pointer"] == "/%d%s" % (ti, ptr):
            print("task=%d ptr=%s tokens=%s original=%r projected=%r"
                  % (ti, lf["json_pointer"], lf["tokens"], lf["original"], lf["projected"]))
            if lf["original"].count("__REDDIT__") or lf["original"].count("__SHOPPING__"):
                print("   occurrence_repeat_in_tokens_list=%s"
                      % (lf["tokens"] != sorted(set(lf["tokens"]))))

# 3. occurrence offsets: global multiset equality for all 1435 occurrences
claimed = [(o["original_input_codepoint_offset"], o["token"])
           for o in inst["occurrence_provenance"]]
actual = []
for name, tok in ORDER:
    for m in re.finditer(re.escape(tok), text):
        actual.append((m.start(), tok))
print("\noccurrence_offsets: claimed=%d actual=%d multiset_equal=%s"
      % (len(claimed), len(actual), sorted(claimed) == sorted(actual)))
dup = len(claimed) - len(set(claimed))
print("duplicate_claimed_offsets=%d" % dup)
# task 811 both offsets are exactly the two real token starts inside its slice
starts = [i for i in range(len(text)) if text.startswith("__GITLAB__", i)]
t811 = [o for o in inst["occurrence_provenance"] if o["task_index"] == 811]
print("t811_offsets=%s all_are_gitlab_starts=%s ordered=%s"
      % ([o["original_input_codepoint_offset"] for o in t811],
         all(o["original_input_codepoint_offset"] in starts for o in t811),
         [o["original_input_codepoint_offset"] for o in t811]
         == sorted(o["original_input_codepoint_offset"] for o in t811)))

# 4. digest identity of would_be_file_sha256 for 811
item = orig[811]
rec = inst["profiles"]["distinct_origins"]["tasks"][811]
cands = {
    "json_dumps_indent2": sha(json.dumps(item, indent=2).encode()),
    "raw_item_compact": sha(json.dumps(item).encode()),
    "raw_item_sorted": sha(json.dumps(item, indent=2, sort_keys=True).encode()),
    "filename": sha(b"config_files/811.json"),
}
print("\nwould_be_digest_candidates_match_instrument=%s"
      % {k: v == rec["would_be_file_sha256"] for k, v in cands.items()})

# 5. per-profile exact projected values for the two changed leaves of 811
print("\n-- projected values at 811 per profile --")
for pname in profiles:
    proj = json.loads(project(text, profiles[pname]["values"]))
    it = proj[811]
    print("%-26s start_url=%r" % (pname, it["start_url"]))
    print("%-26s program_html[0].url=%r"
          % ("", it["eval"]["program_html"][0]["url"]))
    print("%-26s would_be_sha_mine=%s instrument=%s"
          % ("", sha(json.dumps(it, indent=2).encode()),
             inst["profiles"][pname]["tasks"][811]["would_be_file_sha256"]))

# 6. leftover markers inside task 811
seg_start = text.find('"task_id": 811')
seg = text[seg_start:]
print("\ntask811_slice_has__last_url__=%d __page__=%d other_double_underscore=%s"
      % (seg.count("__last_url__"), seg.count("__page__"),
         sorted(set(re.findall(r"__[A-Za-z0-9_]+__", seg)))[:12]))

# 7. population cross-checks
tasks_with_token = sum(1 for i, x in enumerate(orig)
                       if any(tok in json.dumps(x) for _, tok in ORDER))
print("tasks_with_any_token mine=%d instrument=%s"
      % (tasks_with_token, inst["population"]["tasks_with_any_token"]))
per_tok_tasks = {}
for name, tok in ORDER:
    per_tok_tasks[tok] = sum(1 for x in orig if tok in json.dumps(x))
print("tasks_with_token mine=%s instrument=%s agree=%s"
      % (per_tok_tasks, inst["population"]["tasks_with_token"],
         per_tok_tasks == inst["population"]["tasks_with_token"]))
print("string_leaf_count_orig=%d instrument=%s"
      % (sum(1 for x in orig for _ in [0]), None))

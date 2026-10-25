#!/usr/bin/env python3
"""Independent __REDDIT__ census for round 29.

Reads ONLY: pinned fixture bytes, the prereg-implied replacement order
(plans/fixtures/r29/manifest.json), profiles.json, and the PRODUCTION
INSTRUMENT'S STDOUT (subprocess). Does not read or import
plans/config_projection.py source.
"""
import json
import os
import re
import subprocess
import sys
import hashlib
import collections
import bisect

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(LANE, "plans/fixtures/r28/webarena/config_files/test.raw.json")
GEN = os.path.join(LANE, "plans/fixtures/r29/generate_test_data.py")
PROF = os.path.join(LANE, "plans/fixtures/r29/profiles.json")
MAN = os.path.join(LANE, "plans/fixtures/r29/manifest.json")
INST = os.path.join(LANE, "plans/config_projection.py")
SCRATCH = os.path.join(LANE, ".ufo/waves/round-29/scratch/falsify/FTokenReddit")

fails = []
def check(name, cond, detail=""):
    print(("OK   " if cond else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not cond:
        fails.append((name, detail))

sha = lambda b: hashlib.sha256(b).hexdigest()
raw_bytes = open(RAW, "rb").read()
text = raw_bytes.decode("utf-8")
man = json.load(open(MAN))
prof = json.load(open(PROF))
order = man["replacement_order"]
toks = {t: "__%s__" % t for t in order}
orig = json.loads(text)

print("== pinned bytes (sha256, bytes) ==")
for path in (GEN, RAW, PROF, MAN):
    b = open(path, "rb").read()
    print("%s %8d %s" % (sha(b), len(b), os.path.relpath(path, LANE)))
check("raw sha matches prereg", sha(raw_bytes) == "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652")
check("raw is ASCII, no CR", all(b < 128 for b in raw_bytes) and b"\r" not in raw_bytes)

print("\n== A. literal __REDDIT__ in raw text ==")
reddit = toks["REDDIT"]
nonover = text.count(reddit)
scan = sum(1 for m in range(len(text)) if text.startswith(reddit, m))
look = len(re.findall("(?=%s)" % re.escape(reddit), text))
print("str.count=%d overlap-scan=%d lookahead=%d" % (nonover, scan, look))
check("literal occurrences 336", nonover == 336 and scan == 336 and look == 336)
print("near-miss triple underscores ___REDDIT =", len(re.findall(r"___REDDIT", text)),
      "REDDIT___ =", len(re.findall(r"REDDIT___", text)))
check("no near-miss continuation", len(re.findall(r"__REDDIT__\w", text)) == 0)

print("\n== B. decoded census (independent leaf walk) ==")
def walk(o, ptr, acc):
    if isinstance(o, str):
        acc.append((ptr, o))
    elif isinstance(o, dict):
        for k, v in o.items():
            walk(v, ptr + "/" + k, acc)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, ptr + "/" + str(i), acc)

def tmpl(ptr):
    s = ""
    for q in ptr.split("/")[2:]:
        if q.isdigit():
            s += "[]"
        else:
            s += ("." if s else "") + q
    return s

leaves = []
for i, item in enumerate(orig):
    acc = []
    walk(item, "/" + str(i), acc)
    leaves.append(acc)
all_leaves = [s for lv in leaves for _, s in lv]
print("tasks=%d string_leaves=%d" % (len(orig), len(all_leaves)))
check("812 tasks", len(orig) == 812)
check("10869 string leaves", len(all_leaves) == 10869)

leaf_ct = sum(1 for lv in leaves for _, s in lv if reddit in s)
occ_ct = sum(s.count(reddit) for s in all_leaves)
task_ct = sum(1 for lv in leaves if any(reddit in s for _, s in lv))
multi = [(i, p, s.count(reddit)) for i, lv in enumerate(leaves) for p, s in lv if s.count(reddit) > 1]
multi_occ = sum(c for _, _, c in multi)
print("decoded leaves=%d occurrences=%d tasks=%d" % (leaf_ct, occ_ct, task_ct))
print("leaves with >1 __REDDIT__: %d (counts=%s, occurrences=%d, excess=%d)"
      % (len(multi), [c for _, _, c in multi], multi_occ, multi_occ - len(multi)))
check("decoded leaves 323", leaf_ct == 323)
check("decoded occurrences 336", occ_ct == 336)
check("tasks 128", task_ct == 128)
check("multi leaves 8, excess 13", len(multi) == 8 and multi_occ - len(multi) == 13)
by_path = collections.Counter(tmpl(p) for lv in leaves for p, s in lv if reddit in s)
occ_path = collections.Counter()
for lv in leaves:
    for p, s in lv:
        if reddit in s:
            occ_path[tmpl(p)] += s.count(reddit)
print("leaves by path:", dict(by_path))
print("occurrences by path:", dict(occ_path))
check("path leaf sum 323", sum(by_path.values()) == 323)
check("path occurrence sum 336", sum(occ_path.values()) == 336)

# distinct-token overlap
multi_tok = []
for i, lv in enumerate(leaves):
    for p, s in lv:
        present = [t for t in toks.values() if t in s]
        if len(present) > 1:
            multi_tok.append((i, p, present))
check("no leaf carries two distinct tokens", len(multi_tok) == 0, str(multi_tok[:3]))

# keys
key_hits = []
def keyscan(o, ptr):
    if isinstance(o, dict):
        for k, v in o.items():
            if any(t in k for t in toks.values()):
                key_hits.append(ptr + "/" + k)
            keyscan(v, ptr + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            keyscan(v, ptr + "/" + str(i))
keyscan(orig, "")
check("no token in any key", len(key_hits) == 0)

print("\n== C. substring / overlap logic ==")
pairs = [(a, b) for a in toks.values() for b in toks.values() if a != b and a in b]
check("no token is substring of another", len(pairs) == 0, str(pairs))
print("__SHOPPING__ count=%d  __SHOPPING_ADMIN__ count=%d  prefix __SHOPPING=%d"
      % (text.count("__SHOPPING__"), text.count("__SHOPPING_ADMIN__"), text.count("__SHOPPING")))
check("__SHOPPING prefix exactly = __SHOPPING__ + __SHOPPING_ADMIN__",
      text.count("__SHOPPING") == text.count("__SHOPPING__") + text.count("__SHOPPING_ADMIN__"))
check("profile values contain no token delimiter", all("__" not in v for p in prof.values() for v in p["values"].values()))

print("\n== D. independent per-profile projection ==")
instrument_summary = subprocess.run(
    [sys.executable, INST, "--summary"], cwd=LANE, capture_output=True, text=True)
check("instrument --summary exit 0", instrument_summary.returncode == 0, "stderr=" + instrument_summary.stderr[:200])
instrument_json = subprocess.run(
    [sys.executable, INST, "--json"], cwd=LANE, capture_output=True, text=True)
check("instrument --json exit 0", instrument_json.returncode == 0, "stderr=" + instrument_json.stderr[:200])
D = json.loads(instrument_json.stdout)
S = {}
for line in instrument_summary.stdout.splitlines():
    m = re.match(r"ORIGINAL_OCCURRENCES_BY_TOKEN (.*)$", line)
    if m: S["occ"] = json.loads(m.group(1))
    m = re.match(r"TASKS_WITH_TOKEN (.*)$", line)
    if m: S["tasks"] = json.loads(m.group(1))
    m = re.match(r"PROFILE (\S+) applied_replacements=(.*)$", line)
    if m: S.setdefault(m.group(1), {})["applied"] = json.loads(m.group(2))
    m = re.match(r"PROFILE (\S+) changed_leaves_by_token=(.*)$", line)
    if m: S.setdefault(m.group(1), {})["leaves"] = json.loads(m.group(2))
    m = re.match(r"PROFILE (\S+) changed_tasks_by_token=(.*)$", line)
    if m: S.setdefault(m.group(1), {})["tasks"] = json.loads(m.group(2))

check("summary __REDDIT__ occurrences", S["occ"]["__REDDIT__"] == 336, str(S["occ"]["__REDDIT__"]))
check("summary __REDDIT__ tasks", S["tasks"]["__REDDIT__"] == 128, str(S["tasks"]["__REDDIT__"]))
check("json population occ == summary", D["population"]["original_occurrences_by_token"] == S["occ"])
check("json population tasks == summary", D["population"]["tasks_with_token"] == S["tasks"])

for pname, pobj in prof.items():
    t = text
    applied = {}
    for name in order:
        tok = toks[name]
        applied[name] = t.count(tok)
        t = t.replace(tok, pobj["values"][name])
    proj = json.loads(t)
    digest = sha(t.encode())
    inst = D["profiles"][pname]
    steps = {s["name"]: s["applied_replacements"] for s in inst["steps"]}
    print("%s applied=%s digest=%s parsed=%d" % (pname, applied, digest, len(proj)))
    check("%s REDDIT applied 336" % pname, applied["REDDIT"] == 336, str(applied["REDDIT"]))
    check("%s instrument applied == own" % pname, steps == applied)
    check("%s instrument applied == summary" % pname, S[pname]["applied"] == steps)
    check("%s digest matches instrument" % pname, digest == inst["projected_text_sha256"], inst["projected_text_sha256"])
    check("%s parsed 812" % pname, len(proj) == 812)
    check("%s remaining REDDIT text 0" % pname, t.count(reddit) == 0)
    rem = []
    for item in proj:
        acc = []
        walk(item, "", acc)
        rem.extend(s for _, s in acc)
    check("%s remaining REDDIT decoded 0" % pname, not any(reddit in s for s in rem))

    bad_obj = bad_sha = bad_leaf = bad_idx = 0
    for i, item in enumerate(proj):
        rec = inst["tasks"][i]
        if rec["projected_task"] != item: bad_obj += 1
        if sha(json.dumps(item, indent=2).encode()) != rec["would_be_file_sha256"]: bad_sha += 1
        if rec["output_index"] != i or rec["output_filename"] != "config_files/%d.json" % i or rec["task_id"] != item["task_id"]: bad_idx += 1
        acc = []
        walk(item, "/" + str(i), acc)
        got = []
        for (ptr, ov), (ptr2, nv) in zip(leaves[i], acc):
            if ov != nv:
                got.append({"json_pointer": ptr, "original": ov, "projected": nv,
                            "tokens": [toks[x] for x in order if toks[x] in ov],
                            "path_template": tmpl(ptr)})
        want = [{k: c[k] for k in ("json_pointer", "original", "projected", "tokens", "path_template")}
                for c in rec["changed_leaves"]]
        if got != want: bad_leaf += 1
    check("%s 812 projected task objects equal" % pname, bad_obj == 0, str(bad_obj))
    check("%s 812 would_be_file_sha256 equal (ensure_ascii=True)" % pname, bad_sha == 0, str(bad_sha))
    check("%s 812 changed-leaf lists equal" % pname, bad_leaf == 0, str(bad_leaf))
    check("%s output index/filename/task_id equal" % pname, bad_idx == 0, str(bad_idx))
    own_leaf = collections.Counter()
    own_task = collections.Counter()
    for i, lv in enumerate(leaves):
        ts = set()
        for _, s in lv:
            for name in order:
                if toks[name] in s:
                    ts.add(toks[name])
        for name in order:
            if any(toks[name] in s for _, s in lv):
                pass
        for tt in ts: own_task[tt] += 1
    # per-leaf attribution against instrument
    for i, lv in enumerate(leaves):
        for _, s in lv:
            for name in order:
                if toks[name] in s:
                    own_leaf[toks[name]] += 1
    own_leaf = {k: own_leaf.get(k, 0) for k in toks.values()}
    own_task = {k: own_task.get(k, 0) for k in toks.values()}
    check("%s changed_leaves_by_token equal (REDDIT 323)" % pname,
          own_leaf == inst["changed_leaves_by_token"] and own_leaf[reddit] == 323,
          "own REDDIT=%d" % own_leaf[reddit])
    check("%s changed_tasks_by_token equal (REDDIT 128)" % pname,
          own_task == inst["changed_tasks_by_token"] and own_task[reddit] == 128,
          "own REDDIT=%d" % own_task[reddit])
    check("%s summary leaves == json leaves" % pname, S[pname]["leaves"] == inst["changed_leaves_by_token"])
    check("%s summary tasks == json tasks" % pname, S[pname]["tasks"] == inst["changed_tasks_by_token"])

print("\n== E. occurrence provenance (span-tracked raw parser) ==")
def parse_with_spans(s):
    spans = []
    pos = 0
    n = len(s)
    def ws():
        nonlocal pos
        while pos < n and s[pos] in " \t\r\n":
            pos += 1
    def parse(ptr):
        nonlocal pos
        ws()
        ch = s[pos]
        if ch == "{":
            pos += 1
            obj = {}
            first = True
            while True:
                ws()
                if s[pos] == "}":
                    pos += 1
                    return obj
                if not first:
                    assert s[pos] == ","
                    pos += 1
                    ws()
                first = False
                assert s[pos] == '"'
                k0 = pos
                pos += 1
                while s[pos] != '"':
                    pos += 2 if s[pos] == "\\" else 1
                k1 = pos
                pos += 1
                key = json.loads(s[k0:k1 + 1])
                ws()
                assert s[pos] == ":"
                pos += 1
                obj[key] = parse(ptr + "/" + key)
        elif ch == "[":
            pos += 1
            arr = []
            first = True
            idx = 0
            while True:
                ws()
                if s[pos] == "]":
                    pos += 1
                    return arr
                if not first:
                    assert s[pos] == ","
                    pos += 1
                    ws()
                first = False
                arr.append(parse(ptr + "/" + str(idx)))
                idx += 1
        elif ch == '"':
            st = pos
            pos += 1
            while s[pos] != '"':
                pos += 2 if s[pos] == "\\" else 1
            en = pos
            pos += 1
            val = json.loads(s[st:en + 1])
            spans.append((ptr, st + 1, en, val))
            return val
        else:
            st = pos
            while pos < n and s[pos] not in " \t\r\n,]}":
                pos += 1
            return json.loads(s[st:pos])
    val = parse("")
    ws()
    assert pos == n
    return val, spans

parsed, spans = parse_with_spans(text)
check("span parse reproduces decoded doc", parsed == orig)
check("span count == decoded leaf count", len(spans) == 10869)
starts = [sp[1] for sp in spans]
def span_of(off):
    j = bisect.bisect_right(starts, off) - 1
    if j < 0:
        return None
    ptr, s, e, v = spans[j]
    return (ptr, s, e, v) if s <= off < e else None

P = [p for p in D["occurrence_provenance"] if p["token"] == reddit]
P.sort(key=lambda p: p["original_input_codepoint_offset"])
own_offs = [m for m in range(len(text)) if text.startswith(reddit, m)]
print("provenance entries=%d own offsets=%d" % (len(P), len(own_offs)))
check("336 provenance entries, 336 own occurrences", len(P) == 336 and len(own_offs) == 336)
check("provenance offsets exactly own offsets", [p["original_input_codepoint_offset"] for p in P] == own_offs)
check("all offsets slice to token", all(text[p["original_input_codepoint_offset"]:p["original_input_codepoint_offset"] + len(reddit)] == reddit for p in P))
bad_ptr = bad_ti = bad_role = 0
for p in P:
    sp = span_of(p["original_input_codepoint_offset"])
    if sp is None or sp[0] != p["json_pointer"]:
        bad_ptr += 1
        continue
    if int(sp[0].split("/")[1]) != p["task_index"]:
        bad_ti += 1
    if p["string_role"] != "value":
        bad_role += 1
check("pointer from span equals provenance json_pointer", bad_ptr == 0, str(bad_ptr))
check("task_index equals pointer head", bad_ti == 0, str(bad_ti))
check("all roles value", bad_role == 0)
ptrs = set(p["json_pointer"] for p in P)
print("distinct pointers=%d distinct tasks=%d" % (len(ptrs), len(set(p["task_index"] for p in P))))
check("323 distinct leaf pointers", len(ptrs) == 323)
check("128 distinct tasks", len(set(p["task_index"] for p in P)) == 128)
path_ct = collections.Counter(p["path_template"] for p in P)
print("provenance path counts:", dict(path_ct))
check("provenance path counts sum 336", sum(path_ct.values()) == 336)
check("provenance path counts == decoded occurrence counts", path_ct == occ_path)
check("all occurrences inside one of the 5 paths",
      set(path_ct) == {"start_url", "eval.program_html[].url", "eval.reference_url",
                       "eval.program_html[].required_contents.must_include[]",
                       "eval.reference_answer_raw_annotation"})

print("\n== F. determinism vs build receipt ==")
receipt = open(os.path.join(LANE, "corpus/evidence/round29-calibration/build-summary.txt")).read().splitlines()
cur = instrument_summary.stdout.splitlines()
check("summary byte-lines equal receipt (receipt adds trailing exit=0)",
      cur == [l for l in receipt if l != "exit=0"], "%d vs %d lines" % (len(cur), len(receipt)))
json_sha = sha(instrument_json.stdout.encode())
print("current --json sha256 =", json_sha)
check("json digest equals receipt build-json-sha256",
      json_sha in open(os.path.join(LANE, "corpus/evidence/round29-calibration/build-json-sha256.txt")).read())

print("\n== G. runtime unit checks ==")
check("2436 task/profile projections", sum(len(D["profiles"][p]["tasks"]) for p in D["profiles"]) == 2436)
check("index_equals_task_id 812 own", all(it["task_id"] == i for i, it in enumerate(orig)))
check("task ids distinct", len(set(it["task_id"] for it in orig)) == 812)

print("\nFAILS:", len(fails))
for f in fails:
    print(" -", f)
print("VERDICT:", "PASS" if not fails else "FAIL")

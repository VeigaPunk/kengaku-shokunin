"""Independent F1-F5 census. Reads generator bytes, raw812, profiles, and the instrument's --json OUTPUT only.
Never reads/imports plans/config_projection.py."""
import json, re, sys, hashlib, urllib.parse, random
from collections import Counter, defaultdict

L = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
RAW = L + "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = L + "plans/fixtures/r29/profiles.json"
GEN = L + "plans/fixtures/r29/generate_test_data.py"
OUT = L + ".ufo/waves/round-29/scratch/falsify/FCritForecasts/out.json"

gen = open(GEN, encoding="utf-8").read()
steps = re.findall(r'raw = raw\.replace\("(__[A-Z_]+__)", ([A-Z_]+)\)', gen)
print("GEN_STEPS", steps)
TOKENS = [t for t, _ in steps]

rawb = open(RAW, "rb").read()
raw = rawb.decode("utf-8")
print("RAW sha256", hashlib.sha256(rawb).hexdigest(), "ascii", all(b < 128 for b in rawb), "CR", b"\r" in rawb)
data = json.loads(raw)
profiles = json.load(open(PROF))

def leaves(o, path="$", tmpl=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{path}.{k}", f"{tmpl}.{k}" if tmpl else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{path}[{i}]", f"{tmpl}[]")
    elif isinstance(o, str):
        yield path, re.sub(r"^\[\]\.", "", tmpl), o

def keys(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k
            yield from keys(v)
    elif isinstance(o, list):
        for v in o:
            yield from keys(v)

# --- F1 preconditions: profile alphabet cannot break JSON string literals
for pn, p in profiles.items():
    bad = {k: v for k, v in p["values"].items() if any(c in v for c in '"\\') or any(ord(c) < 0x20 for c in v)}
    print("F1_ALPHABET", pn, "json-breaking chars:", bad or "none")
print("TOKENS_IN_KEYS", sum(1 for k in keys(data) for t in TOKENS if t in k))

# --- per-profile projection (upstream semantics: sequential str.replace over serialized text)
proj = {}
for pn, p in profiles.items():
    txt = raw
    for tok, var in steps:
        txt = txt.replace(tok, p["values"][var])
    d2 = json.loads(txt)
    proj[pn] = d2
    rem_text = {t: txt.count(t) for t in TOKENS}
    rem_dec = {t: sum(v.count(t) for _, _, v in leaves(d2)) for t in TOKENS}
    # F2 cascade possibility: could a profile value create/contain any token?
    cascade = [t for t in TOKENS for v in p["values"].values() if t in v or v.startswith("__") or v.endswith("__")]
    print("F1", pn, "parsed", len(d2), "| F2 text", sum(rem_text.values()), "decoded", sum(rem_dec.values()), "| value-side token risk", cascade or "none")

# --- F4
idx_eq = sum(1 for i, t in enumerate(data) if t.get("task_id") == i)
print("F4 index==task_id", idx_eq, "of", len(data), "| ids distinct", len({t['task_id'] for t in data}))
hf = json.load(open(L + "plans/fixtures/r29/hand/index-shuffled-ids.fixture.json"))
print("F4 hand fixture keys", list(hf)[:12] if isinstance(hf, dict) else type(hf).__name__)

# --- F3: changed-leaf classification under competing readings
URL_ROLE_TMPL = {"start_url", "eval.reference_url", "eval.program_html[].url"}
ref = proj["distinct_origins"]
orig_leaves = {p: (tm, v) for p, tm, v in leaves(data)}
new_leaves = {p: v for p, _, v in leaves(ref)}
changed = [(p, tm, v, new_leaves[p]) for p, (tm, v) in orig_leaves.items() if new_leaves[p] != v]
print("F3 changed leaves", len(changed))

def single_url(s):
    if any(c.isspace() for c in s) or "," in s or "|" in s:
        return False
    u = urllib.parse.urlsplit(s)
    return bool(u.scheme in ("http", "https") and u.netloc)

def contains_url(s):
    return bool(re.search(r"https?://[^\s,|]+", s))

reading = Counter()
nonrole = []
for p, tm, v, nv in changed:
    role_url = tm in URL_ROLE_TMPL
    reading["A_key_role_nonurl"] += (not role_url)
    reading["B_value_not_single_url"] += (not single_url(nv))
    reading["C_value_contains_no_url"] += (not contains_url(nv))
    reading["D_value_not_starting_with_token_or_scheme"] += (not (v.startswith("__") ))
    if not role_url or not single_url(nv):
        nonrole.append((p, tm, v, nv, single_url(nv), contains_url(nv)))
print("F3 READINGS (count of changed leaves satisfying 'non-URL-valued field' under each reading):", dict(reading))
tm_c = Counter(tm for p, tm, v, nv in changed)
print("F3 changed by template", dict(tm_c))
print("F3 non-role-or-non-single-url leaves:", len(nonrole))
bytm = defaultdict(list)
for r in nonrole:
    bytm[(r[1], r[4], r[5])].append(r)
for k, rs in sorted(bytm.items()):
    print("  ", k, "n=", len(rs), "example:", rs[0][0], repr(rs[0][2])[:140], "->", repr(rs[0][3])[:160])

# role-URL leaves whose projected value is NOT a single URL (value-shape reading flips the other way)
weird_role = [(p, v, nv) for p, tm, v, nv in changed if tm in URL_ROLE_TMPL and not single_url(nv)]
print("F3 URL-role leaves whose projected value is not a single absolute URL:", len(weird_role))
for p, v, nv in weird_role[:6]:
    print("   ", p, repr(nv)[:180])

# --- compare with instrument --json OUTPUT
inst = json.load(open(OUT))
for pn in profiles:
    ip = inst["profiles"][pn]
    pl = {q: w for q, _, w in leaves(proj[pn])}
    mine_cat = Counter(("url_field" if tm in URL_ROLE_TMPL else "non_url_field")
                       for p, (tm, v) in orig_leaves.items() if pl[p] != v)
    print("CMP", pn, "parsed", ip["parsed_task_count"], len(proj[pn]),
          "| cat inst", ip["changed_leaves_by_category"], "mine", dict(mine_cat),
          "| rem_text inst", sum(ip["remaining_known_tokens_text"].values()),
          "| rem_dec inst", sum(ip["remaining_known_tokens_decoded"].values()))
print("CMP index inst", inst["index_mapping"]["index_equals_task_id"], "violations", len(inst["index_mapping"]["violations"]))
t0 = inst["profiles"]["distinct_origins"]["tasks"][66]
print("CMP inst task[66] keys", list(t0))
for k, v in t0.items():
    if k != "projected_task":
        print("   ", k, json.dumps(v)[:700])
cats = Counter()
for t in inst["profiles"]["distinct_origins"]["tasks"]:
    for leaf in t.get("changed_leaves", []):
        if isinstance(leaf, dict):
            cats[(leaf.get("category"), leaf.get("path_template", leaf.get("template")))] += 1
print("CMP inst per-leaf (category, template) census", dict(cats))
print("CMP 'category' rule text anywhere in output:", [m for m in ("URL_ROLE", "url_field_paths", "category_rule", "category_definition") if m in json.dumps(inst)])
multi = [p for p, tm, v, nv in changed if sum(v.count(t) for t in TOKENS) > 1]
print("F3 multi-occurrence changed leaves", len(multi), "equal to not-single-url set:",
      set(multi) == {p for p, tm, v, nv in changed if not single_url(nv)})
s = json.dumps({k: v for k, v in inst.items() if k != "profiles" and k != "occurrence_provenance"})
print("CMP inst top-level text mentions 'category' def?", "url_field" in s, "| limitations:", inst["limitations"])

"""Fifth pass: replacement-site leaf counts, eval field census, consumption categories."""
import json
from collections import Counter
from functools import reduce
from urllib.parse import urlsplit

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {k: "__%s__" % k for k in ORDER}
raw = open(RAW, "rb").read().decode("utf-8")
profiles = json.loads(open(PROFILES, "rb").read())
orig = json.loads(raw)


def project(values):
    return reduce(lambda s, k: s.replace(TOK[k], values[k]), ORDER, raw)


def walk(a, b, path=()):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            yield from walk(a[k], b[k], path + (k,))
    elif isinstance(a, list) and isinstance(b, list):
        for i, (x, y) in enumerate(zip(a, b)):
            yield from walk(x, y, path + (i,))
    elif a != b:
        yield path, a, b


proj0 = json.loads(project(profiles["distinct_origins"]["values"]))
projT = json.loads(project(profiles["trailing_slash_sensitivity"]["values"]))
diffs = [(ti, path, old, new) for ti, d in enumerate(orig) for path, old, new in walk(d, proj0[ti])]

# replacement sites followed by '/' -> leaves containing at least one
sites_followed = 0
leaves_followed = 0
for ti, path, old, new in diffs:
    n = 0
    for k in ORDER:
        i = old.find(TOK[k])
        while i >= 0:
            j = i + len(TOK[k])
            if j < len(old) and old[j] == "/":
                n += 1
            i = old.find(TOK[k], j)
    if n:
        sites_followed += n
        leaves_followed += 1
print("SITES_FOLLOWED_BY_SLASH", sites_followed, "LEAVES", leaves_followed)
print("SITES_AT_VALUE_END", sum(1 for _t, _p, old, _n in diffs for k in ORDER
                                 for _ in range(old.count(TOK[k]) - old.count(TOK[k] + "/") * 0)))
# exact at-end count
at_end = 0
for ti, path, old, new in diffs:
    for k in ORDER:
        i = old.find(TOK[k])
        while i >= 0:
            j = i + len(TOK[k])
            if j == len(old):
                at_end += 1
            i = old.find(TOK[k], j)
print("SITES_AT_VALUE_END_EXACT", at_end)

# trailing-slash newly double-slashed leaves: compare per-leaf, count leaves where
# projT value contains '//' at a site where proj0 has single '/'
dbl_leaves = 0
dbl_sites = 0
for ti, path, old, new in diffs:
    nother = projT[ti]
    # walk parallel path
    node = nother
    for p in path:
        node = node[p]
    # count occurrences of value+"/" where old had token followed by '/'
    c = 0
    for k in ORDER:
        v = profiles["trailing_slash_sensitivity"]["values"][k]
        i = old.find(TOK[k])
        while i >= 0:
            j = i + len(TOK[k])
            if j < len(old) and old[j] == "/":
                c += 1
            i = old.find(TOK[k], j)
    if c:
        dbl_leaves += 1
        dbl_sites += c
print("TRAILING_NEW_DOUBLE_SLASH_LEAVES", dbl_leaves, "SITES", dbl_sites)

# path_prefix: sites where value appended at end, and where '/prefix/' inserted
print("PREFIX_SITES_TOTAL", sum(old.count(TOK[k]) for _t, _p, old, _n in diffs for k in ORDER))

# eval field census
ru_empty = ru_nonempty = 0
ph_entries = 0
ph_url_empty = 0
ph_url_token = 0
mi_strings = 0
mi_token = 0
loc_nonempty = 0
loc_token = 0
storage_prefix = Counter()
storage_null = 0
string_note_vals = {}
refans_kinds = Counter()
for d in orig:
    ev = d["eval"]
    for k in ("reference_url",):
        pass
    ru = ev.get("reference_url", "")
    if ru == "":
        ru_empty += 1
    else:
        ru_nonempty += 1
    refans_kinds[type(ev.get("reference_answers")).__name__] += 1
    for ph in ev.get("program_html", []):
        ph_entries += 1
        if ph.get("url", "") == "":
            ph_url_empty += 1
        if any(TOK[k] in ph.get("url", "") for k in ORDER):
            ph_url_token += 1
        if ph.get("locator", ""):
            loc_nonempty += 1
        if any(TOK[k] in ph.get("locator", "") for k in ORDER):
            loc_token += 1
        for s in ph.get("required_contents", {}).get("must_include", []) or []:
            mi_strings += 1
            if any(TOK[k] in s for k in ORDER):
                mi_token += 1
    ss = d["storage_state"]
    if ss is None:
        storage_null += 1
    else:
        storage_prefix[ss.split("/")[0] + "/" + (ss.split("/")[1] if "/" in ss else "")] += 1
    if "string_note" in ev:
        string_note_vals[d["task_id"]] = ev["string_note"]
print("\nEVAL_CENSUS reference_url_empty", ru_empty, "nonempty", ru_nonempty,
      "program_html_entries", ph_entries, "url_empty", ph_url_empty, "url_token", ph_url_token,
      "locator_nonempty", loc_nonempty, "locator_token", loc_token,
      "must_include_strings", mi_strings, "must_include_token", mi_token)
print("REFERENCE_ANSWERS_KINDS", dict(refans_kinds))
print("STORAGE_STATE prefixes", dict(storage_prefix), "null", storage_null)
print("STRING_NOTE", string_note_vals)

# sanity: no tokens anywhere in serialized original other than leaves already counted
alltxt = json.dumps(orig, ensure_ascii=True)
print("\nTOKENS_IN_RESERIALIZED_ORIG", {k: alltxt.count(TOK[k]) for k in ORDER})

# check eval.reference_answers nested strings for tokens explicitly
rawans = json.dumps([d["eval"].get("reference_answers") for d in orig])
print("TOKENS_IN_REFERENCE_ANSWERS", {k: rawans.count(TOK[k]) for k in ORDER})

"""In-memory bounded counterexamples; nothing written except stdout. Raw/profile files only read."""
import json, re, collections

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
raw = open(ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json", "rb").read().decode()
prof = json.load(open(ROOT + "plans/fixtures/r29/profiles.json"))
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
IDENT = re.compile(r"__([A-Za-z0-9]+(?:_[A-Za-z0-9]+)*)__")
ALLOW = {"__last_url__": 65, "__page__": 12}

def project(text, values):
    for k in ORDER:
        text = text.replace(f"__{k}__", values[k])
    return text

def six_only_check(projected):
    return {k: projected.count(f"__{k}__") for k in ORDER}

def closed_residual_check(raw_text, projected):
    after = collections.Counter(m.group(0) for m in IDENT.finditer(projected))
    findings = []
    for name, n in after.items():
        if name.strip("_") in ORDER:
            findings.append(("known_token_remaining", name, n))
        elif name not in ALLOW:
            findings.append(("unclassified_residual_marker", name, n))
        elif n != raw_text.count(name):
            findings.append(("residual_marker_count_changed", name, raw_text.count(name), n))
    for name in ALLOW:
        if after.get(name, 0) != ALLOW[name]:
            findings.append(("residual_marker_expected_count", name, ALLOW[name], after.get(name, 0)))
    return findings

base = prof["distinct_origins"]["values"]

print("CONTROL frozen raw, distinct_origins")
p = project(raw, base)
print("  six_only", six_only_check(p), "closed", closed_residual_check(raw, p))

print("M1 seventh-token mutant: first start_url '__MAP__' -> '__HOMEPAGE__'")
needle = '"start_url": "__MAP__"'
assert needle in raw
m1 = raw.replace(needle, '"start_url": "__HOMEPAGE__"', 1)
p = project(m1, base)
print("  six_only", six_only_check(p), "closed", closed_residual_check(m1, p))

print("M2 marker-collision profile: SHOPPING value carries '__page__'")
v2 = dict(base, SHOPPING="http://shopping.invalid:10103/__page__")
p = project(raw, v2)
print("  six_only", six_only_check(p), "closed", closed_residual_check(raw, p))

print("M3 marker-deletion projector bug: also strips '__last_url__'")
p = project(raw, base).replace("__last_url__", "")
print("  six_only", six_only_check(p), "closed", closed_residual_check(raw, p))

print("M4 detector regex choice on frozen projection (distinct_origins)")
p = project(raw, base)
for rg in [r"__[A-Z_]+__", r"__\w+__", r"__.+?__"]:
    print("  ", rg, collections.Counter(m.group(0) for m in re.finditer(rg, p)).most_common(4))

print("M5 codepoint vs byte offsets: raw non-ASCII codepoints =", sum(ord(c) > 127 for c in raw),
      "; projected (all profiles) non-ASCII =",
      [sum(ord(c) > 127 for c in project(raw, v["values"])) for v in prof.values()])

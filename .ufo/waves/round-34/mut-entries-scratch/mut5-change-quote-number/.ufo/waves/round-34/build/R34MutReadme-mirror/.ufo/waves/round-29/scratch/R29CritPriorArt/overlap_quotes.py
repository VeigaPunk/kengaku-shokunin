"""Read-only: r28-overlap cross-check and programmatic quote verification. DATA reads only."""
import hashlib
import json
import re

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
with open(RAW, "rb") as f:
    raw_b = f.read()
assert hashlib.sha256(raw_b).hexdigest() == "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"
data = json.loads(raw_b.decode("utf-8"))
TOK = re.compile(r"__(GITLAB|REDDIT|SHOPPING_ADMIN|SHOPPING|WIKIPEDIA|MAP)__")

nav = last = helper = other = 0
nav_tok = nav_tok_occ = nontarget_tok = 0
ref_tasks = ref_tok_tasks = 0
start_prefix = 0
for t in data:
    if TOK.match(t.get("start_url", "")):
        start_prefix += 1
    ev = t.get("eval") or {}
    if isinstance(ev.get("reference_url"), str) and ev["reference_url"]:
        ref_tasks += 1
        if TOK.search(ev["reference_url"]):
            ref_tok_tasks += 1
    for tgt in ev.get("program_html") or []:
        u = tgt.get("url")
        if u == "last":
            last += 1
            c = "last"
        elif isinstance(u, str) and u.startswith("func:"):
            helper += 1
            c = "helper"
        else:
            nav += 1
            c = "nav"
        n = len(TOK.findall(u)) if isinstance(u, str) else 0
        if c == "nav" and n:
            nav_tok += 1
            nav_tok_occ += n
        elif n:
            nontarget_tok += 1
print("R28_TARGET_CLASSES last", last, "nav", nav, "helper", helper, "total", last + nav + helper)
print("NAV_TARGETS_WITH_TOKEN", nav_tok, "occ", nav_tok_occ, "NONNAV_TARGETS_WITH_TOKEN", nontarget_tok)
print("REFERENCE_URL_TASKS", ref_tasks, "WITH_TOKEN", ref_tok_tasks)
print("START_URL_TOKEN_PREFIXED_TASKS", start_prefix)

QUOTES = [
    (LANE + "/plans/round-29-claims.md", "0 dedicated generated-config audits at base"),
    (LANE + "/plans/round-29-claims.md", "No new scientific method, actual deployment config, task validity,"),
    (LANE + "/plans/round-29-claims.md", "Decoded-leaf rewriting is an independently implemented oracle only within the frozen benign profile domain;"),
    (LANE + "/plans/round-29-claims.md", "F5 no method-novelty score increase, p=.95."),
    (LANE + "/plans/round-29-claims.md", "own-work profiles.json: distinct origins, path-prefix sensitivity, trailing-slash sensitivity."),
    (LANE + "/plans/round-29-claims.md", "P2/P3 sensitivity profiles are not deployment recommendations or model errors."),
    (LANE + "/SCORECARD.md", "a phenomenon already published (keep as replication, not contribution)"),
    (LANE + "/SCORECARD.md", "observable improved, no method novelty (xFinder and public harness prior art)"),
    (LANE + "/corpus/knowledge/webarena-task-spec-audit.md", "target URL classes |last238, navigation338, helper75|"),
    (LANE + "/corpus/knowledge/webarena-task-spec-audit.md", "effective URL rules / provenance |205 GOLD in PRED;"),
    (LANE + "/plans/fixtures/r29/generate_test_data.py", 'raw = raw.replace("__GITLAB__", GITLAB)'),
    (LANE + "/plans/fixtures/r29/generate_test_data.py", "for idx, item in enumerate(data):"),
]
for path, q in QUOTES:
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    hits = [i + 1 for i, line in enumerate(lines) if q in line]
    if not hits:
        norm = " ".join(" ".join(lines).split())
        span = "multiline" if " ".join(q.split()) in norm else "ABSENT"
    else:
        span = ",".join(map(str, hits))
    print("QUOTE words=%d lines=%s file=%s :: %s" % (len(q.split()), span, path.rsplit("/", 1)[1], q))

#!/usr/bin/env python3
"""FRevHistory upstream-history probe: static fetch + hash only, no upstream execution."""
import hashlib, json, re, ssl, urllib.request, sys

UA = {"User-Agent": "r29-falsify-history"}
API = "https://api.github.com/repos/web-arena-x/webarena"
RAW = "https://raw.githubusercontent.com/web-arena-x/webarena/"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
PIN_GEN_SHA = "45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd"
PIN_RAW_SHA = "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"
PIN_REV = "dce04686a56253aefba7b18a4fa0937cf1dc987b"

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def h(b): return hashlib.sha256(b).hexdigest()

gen_commits = json.load(open("/tmp/r29fh/gen_commits.json"))
raw_commits = json.load(open("/tmp/r29fh/raw_commits.json"))
head = json.load(open("/tmp/r29fh/head.json"))

print("== HEAD ==")
print("head_sha", head["sha"])
print("head_date", head["commit"]["committer"]["date"])
print("pinned==head:", head["sha"] == PIN_REV)

release = gen_commits[0]["sha"]
print("\n== generator history (commits?path=) ==")
for c in gen_commits:
    print("GEN", c["sha"], c["commit"]["committer"]["date"], c["commit"]["message"].splitlines()[0])
print("\n== raw.json history (commits?path=) ==")
for c in raw_commits:
    print("RAW", c["sha"], c["commit"]["committer"]["date"], c["commit"]["message"].splitlines()[0])

print("\n== release-commit parents check ==")
try:
    rel = json.loads(get(f"{API}/commits/{release}").decode())
    print("release_sha", rel["sha"], "parents", [p["sha"] for p in rel["parents"]])
except Exception as e:
    print("parents check failed:", e)

print("\n== generator bytes: pinned vs head vs release ==")
gen_pin = open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py","rb").read()
gen_head = get(RAW + f"{PIN_REV}/scripts/generate_test_data.py")
gen_rel = get(RAW + f"{release}/scripts/generate_test_data.py")
print("pinned gen sha256", h(gen_pin))
print("head   gen sha256", h(gen_head), "pinned==head:", h(gen_head)==PIN_GEN_SHA)
print("release gen sha256", h(gen_rel), "release==pinned:", h(gen_rel)==PIN_GEN_SHA)

print("\n== raw.json per-commit census (oldest first) ==")
rows = []
for c in reversed(raw_commits):
    sha = c["sha"]
    data = get(RAW + f"{sha}/config_files/test.raw.json")
    dsha = h(data)
    counts = {t: data.count(t.encode()) for t in TOKENS}
    try:
        tasks = json.loads(data)
        n = len(tasks)
        ids = [t.get("task_id") for t in tasks]
        id_ok = ids == [str(i) for i in range(n)]
    except Exception as ex:
        n, ids, id_ok = f"PARSE_FAIL:{ex}", [], False
    # first-occurrence order of tokens in the raw text
    pos = sorted((data.find(t.encode()), t) for t in TOKENS if counts[t] > 0)
    order = [t for _, t in pos]
    rows.append((sha, c["commit"]["committer"]["date"], dsha, n, counts, order, id_ok))
    print(sha[:12], c["commit"]["committer"]["date"][:10], dsha[:12], "tasks=", n,
          "tokens=", sum(counts.values()), "counts=", counts)
    print("   file-first-occurrence order:", order, "index==task_id:", id_ok)

head_row = [r for r in rows if r[0] == PIN_REV]
print("\n== raw.json pinned vs head ==")
print("pinned raw sha256 (manifest):", PIN_RAW_SHA)
print("head raw sha256:", head_row[0][2] if head_row else "n/a", "== pinned:", bool(head_row) and head_row[0][2] == PIN_RAW_SHA)
print("latest commit touching raw.json:", raw_commits[0]["sha"], raw_commits[0]["commit"]["committer"]["date"])

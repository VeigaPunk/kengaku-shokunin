#!/usr/bin/env python3
"""FRevHistory verification pass 2: head-revision bytes, task_id typing, HTML cross-check."""
import hashlib, json, re, urllib.request

UA = {"User-Agent": "r29-falsify-history"}
API = "https://api.github.com/repos/web-arena-x/webarena"
RAW = "https://raw.githubusercontent.com/web-arena-x/webarena/"
PIN_REV = "dce04686a56253aefba7b18a4fa0937cf1dc987b"
PIN_RAW_SHA = "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"
LOCAL_RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def h(b): return hashlib.sha256(b).hexdigest()

print("== default branch ==")
repo = json.loads(get(API).decode())
print("default_branch:", repo["default_branch"], "pushed_at:", repo["pushed_at"])

print("\n== raw.json fetched AT the pinned/head revision (not last-touch) ==")
raw_head = get(RAW + f"{PIN_REV}/config_files/test.raw.json")
print("head-revision raw sha256:", h(raw_head), "== pinned:", h(raw_head) == PIN_RAW_SHA)

print("\n== local pinned raw: task_id typing and index==task_id ==")
loc = open(LOCAL_RAW, "rb").read()
print("local pinned raw sha256:", h(loc), "== pinned manifest:", h(loc) == PIN_RAW_SHA)
tasks = json.loads(loc)
ids = [t.get("task_id") for t in tasks]
print("n tasks:", len(tasks), "id types:", sorted({type(i).__name__ for i in ids}))
as_int = [int(i) for i in ids]
print("index==task_id (int-normalized):", as_int == list(range(len(tasks))))
print("distinct ids:", len(set(ids)), "first/last:", ids[0], ids[-1])
print("token counts in pinned local raw:", {t: loc.count(t.encode()) for t in TOKENS})

print("\n== release-commit raw.json task_id typing ==")
rel_raw = get(RAW + "b454f2dcfdc62af07beebb832b04bf8991ca409f/config_files/test.raw.json")
rt = json.loads(rel_raw)
rid = [t.get("task_id") for t in rt]
print("release n:", len(rt), "index==task_id:", [int(i) for i in rid] == list(range(len(rt))))

print("\n== HTML history cross-check (commits pages) ==")
for label, path in [("generator", "scripts/generate_test_data.py"), ("raw", "config_files/test.raw.json")]:
    page = get(f"https://github.com/web-arena-x/webarena/commits/HEAD/{path}").decode("utf-8", "replace")
    shas = re.findall(r'href="/web-arena-x/webarena/commit/([0-9a-f]{40})"', page)
    uniq = sorted(set(shas))
    print(label, "unique commit links on page:", len(uniq))
    for s in uniq:
        print("  ", s)
    print("   branch shown:", re.findall(r'"refName":"([^"]+)"', page)[:3])

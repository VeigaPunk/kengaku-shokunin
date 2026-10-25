"""Second read-only census: non-dunder residual markers, literal hosts, wikipedia coverage, detector regexes."""
import json, re, collections

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
RAW = ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT + "plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
text = open(RAW, "rb").read().decode("utf-8")
data = json.loads(text)

def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, path + ("[]",))
    elif isinstance(o, str):
        yield path, o

# sites containing wikipedia vs __WIKIPEDIA__ usage
wiki_sites = [d["task_id"] for d in data if "wikipedia" in d.get("sites", [])]
print("tasks with 'wikipedia' in sites:", len(wiki_sites), "first:", wiki_sites[:12])
lw = collections.Counter()
for d in data:
    for p, s in walk(d, ()):
        if "wikipedia" in s.lower():
            lw[".".join(p)] += 1
print("leaves containing 'wikipedia' (case-insens) by path:", dict(lw))
for d in data:
    if d["task_id"] in wiki_sites[:3]:
        print("  task", d["task_id"], "start_url", repr(d["start_url"]), "sites", d["sites"])

# non-dunder markers
mk = collections.Counter(); mk_tasks = collections.defaultdict(set); ex = {}
for d in data:
    for p, s in walk(d, ()):
        pj = ".".join(p)
        checks = {
            "url==last": pj.endswith("program_html.[].url") and s == "last",
            "startswith func:": s.startswith("func:"),
            "contains |AND|": "|AND|" in s,
            "contains |OR|": "|OR|" in s,
            "contains literal http(s)://": bool(re.search(r"https?://", s)),
        }
        for name, hit in checks.items():
            if hit:
                key = (name, pj)
                mk[key] += 1; mk_tasks[key].add(d["task_id"]); ex.setdefault(key, (d["task_id"], s))
print("\n[non-dunder residual markers by path] leaf-occ / tasks / example")
for k in sorted(mk):
    print(f"  {k}: {mk[k]} / {len(mk_tasks[k])}  e.g. {ex[k][0]}: {ex[k][1][:120]!r}")

# func: leaves that also contain env tokens (projection rewrites eval-able code text)
fe = collections.Counter(); fex = {}
for d in data:
    for p, s in walk(d, ()):
        if s.startswith("func:"):
            toks = tuple(t for t in ORDER if f"__{t}__" in s)
            runs = tuple(r for r in ("__last_url__", "__page__") if r in s)
            fe[(".".join(p), toks, runs)] += 1
            fex.setdefault((".".join(p), toks, runs), (d["task_id"], s))
print("\n[func: leaves by path / env tokens inside / runtime markers inside]")
for k, v in sorted(fe.items()):
    print(f"  {k}: {v}  e.g. {fex[k][0]}: {fex[k][1][:120]!r}")

# literal hosts
hosts = collections.Counter(m.group(1) for m in re.finditer(r"https?://([^/\s\"'\\]+)", text))
print("\n[literal http(s) hosts in raw text]")
for h, n in hosts.most_common():
    print(f"  {h}: {n}")

# naive residual-detector regexes: false positives on post-projection text
prof = json.load(open(PROF))
t = text
for tok in ORDER:
    t = t.replace(f"__{tok}__", prof["distinct_origins"]["values"][tok])
regs = {
    r"__[A-Z_]+__": r"__[A-Z_]+__",
    r"__[A-Za-z_]+__": r"__[A-Za-z_]+__",
    r"__\w+__": r"__\w+__",
    r"__\w+?__": r"__\w+?__",
    r"__.+?__": r"__.+?__",
}
print("\n[post-projection matches by candidate residual regex, distinct_origins]")
for name, rg in regs.items():
    c = collections.Counter(m.group(0) for m in re.finditer(rg, t))
    print(f"  {name}: total={sum(c.values())} distinct={len(c)} top={c.most_common(6)}")

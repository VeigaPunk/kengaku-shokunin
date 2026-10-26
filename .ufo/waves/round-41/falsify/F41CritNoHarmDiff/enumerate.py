import subprocess, re, os, collections
os.chdir("/fast/scratch/hyaku/kengaku-r41/F41CritNoHarmDiff/lane")
OLD = "e50c134556b4ba48e29dc7ff364e90d6ef07a3f3"
NEW = "3d0058fbde484c9d6c23fd997d9ee09a0663bcdb"
DOCS = {"SKILL.md": 1, "corpus/README.md": 1, "corpus/SOURCES.md": 1}
def blob(rev, p):
    return subprocess.run(["git", "show", f"{rev}:{p}"], capture_output=True).stdout.decode("utf-8", "replace").split("\n")
old = {p: blob(OLD, p) for p in DOCS}
new = {p: blob(NEW, p) for p in DOCS}
PAT = re.compile(r"(SKILL|SOURCES|README)\.md:([0-9]+)")
hdr = re.compile(r"^([0-9a-f]{40}):(.+?):([0-9]+):(.*)$", re.S)
out = subprocess.run(["git", "grep", "-nE", PAT.pattern, OLD, "--", ":!.ufo"], capture_output=True).stdout.decode("utf-8", "replace")
SIBLING = set()
rows = []
for line in out.splitlines():
    m = hdr.match(line)
    if not m: continue
    path, ln, text = m.group(2), int(m.group(3)), m.group(4)
    for mm in PAT.finditer(text):
        base, n = mm.group(1), int(mm.group(2))
        doc = {"SKILL": "SKILL.md", "SOURCES": "corpus/SOURCES.md", "README": "corpus/README.md"}[base]
        if n >= min(len(old[doc]), len(new[doc])):
            rows.append((path, ln, mm.group(0), doc, n, "OUT-OF-RANGE-no-lane-target"))
            continue
        if old[doc][n-1].strip() == new[doc][n-1].strip():
            continue
        if path.startswith(("corpus/evidence/", "plans/fixtures/")): cls = "frozen-receipt/fixture"
        elif path == "PROVINCE.md" or "README.md:" in text and re.search(r"[A-Za-z0-9_-]+/README\.md:", text): cls = "sibling/third-party"
        else: cls = "live-lane-prose"
        rows.append((path, ln, mm.group(0), doc, n, cls))
rows.sort(key=lambda r: (r[5], r[0], r[1]))
c = collections.Counter(r[5] for r in rows)
print("AFFECTED-BY-CLASS", dict(c), "TOTAL", len(rows))
for r in rows:
    print(f"{r[5]:24s} {r[0]}:{r[1]}  {r[2]}")

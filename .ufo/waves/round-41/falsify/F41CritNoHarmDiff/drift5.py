import subprocess, re, collections, os
os.chdir("/fast/scratch/hyaku/kengaku-r41/F41CritNoHarmDiff/lane")
OLD = "e50c134556b4ba48e29dc7ff364e90d6ef07a3f3"
NEW = "3d0058fbde484c9d6c23fd997d9ee09a0663bcdb"
DOCS = {
    "SKILL.md": [(594, 4), (644, 23), (1030, 83)],
    "corpus/README.md": [(73, 1), (267, 1), (340, 17)],
    "corpus/SOURCES.md": [(136, 3)],
}

def blob(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True).stdout.decode("utf-8", "replace").split("\n")

old = {p: blob(OLD, p) for p in DOCS}
new = {p: blob(NEW, p) for p in DOCS}

def mapf(p, n):
    return n + sum(sz for pos, sz in DOCS[p] if n > pos)

PAT = re.compile(r"([A-Za-z0-9_./-]*)(SKILL|SOURCES|README)\.md:(\d+)")
out = subprocess.run(["git", "grep", "-nE", PAT.pattern, OLD, "--", ":!.ufo"], capture_output=True).stdout.decode("utf-8", "replace")
tot = intodocs = sibling = 0
zone = []
hdr = re.compile(r"^([0-9a-f]{40}):(.+?):(\d+):(.*)$", re.S)
for line in out.splitlines():
    m = hdr.match(line)
    if not m:
        continue
    path, ln, text = m.group(2), int(m.group(3)), m.group(4)
    for mm in PAT.finditer(text):
        pre, base, n = mm.group(1), mm.group(2), int(mm.group(3))
        tot += 1
        if base == "SKILL":
            doc = "SKILL.md" if pre == "" else pre + "SKILL.md"
        elif base == "SOURCES":
            doc = "corpus/SOURCES.md" if pre == "" else pre + "SOURCES.md"
        else:
            doc = "corpus/README.md" if pre == "" else pre + "README.md"
        if doc not in DOCS:
            if pre:
                sibling += 1
            continue
        intodocs += 1
        if n > len(old[doc]):
            zone.append(("OUT-OF-RANGE", path, ln, mm.group(0), doc, n, None))
            continue
        nn = mapf(doc, n)
        o = old[doc][n - 1].strip()
        nw = new[doc][nn - 1].strip()
        if o != nw:
            zone.append(("CHANGED", path, ln, mm.group(0), doc, n, (o[:110], nw[:110])))
print(f"total_citations={tot} into_modified_docs={intodocs} other_path={sibling}")
print(f"zone_entries={len(zone)}")
for z in zone:
    if z[6]:
        print(f"  {z[0]} {z[1]}:{z[2]} cite={z[3]} {z[4]} {z[5]}->{mapf(z[4], z[5])}")
        print("     old:", z[6][0])
        print("     new:", z[6][1])
    else:
        print(f"  {z[0]} {z[1]}:{z[2]} cite={z[3]} {z[4]}:{z[5]}")

import subprocess, re, collections, os
os.chdir("/fast/scratch/hyaku/kengaku-r41/F41CritNoHarmDiff/lane")
OLD = "e50c134556b4ba48e29dc7ff364e90d6ef07a3f3"
NEW = "3d0058fbde484c9d6c23fd997d9ee09a0663bcdb"
# insertion points in OLD numbering: (after_old_line, lines_inserted)
DOCS = {
    "SKILL.md": [(594, 4), (644, 23), (1030, 83)],
    "corpus/README.md": [(73, 1), (267, 1), (340, 17)],
    "corpus/SOURCES.md": [(136, 3)],
}
ROOT_README = "README.md"

def blob(rev, path):
    p = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True)
    return p.stdout.decode("utf-8", "replace").split("\n") if p.returncode == 0 else None

old = {p: blob(OLD, p) for p in DOCS}
new = {p: blob(NEW, p) for p in DOCS}
root_old = blob(OLD, ROOT_README)
root_new = blob(NEW, ROOT_README)
print("root README.md exists:", root_old is not None, "| identical across range:", root_old == root_new)

def mapf(p, n):
    return n + sum(sz for pos, sz in DOCS[p] if n > pos)

PAT = re.compile(r"([A-Za-z0-9_./-]*)(SKILL|SOURCES|README)\.md:([0-9]+)")
out = subprocess.run(["git", "grep", "-nE", PAT.pattern, OLD, "--", ":!.ufo"],
                     capture_output=True).stdout.decode("utf-8", "replace")
tot = intodocs = other = 0
zone = []
amb = 0
hdr = re.compile(r"^([0-9a-f]{40}):(.+?):([0-9]+):(.*)$", re.S)
for line in out.splitlines():
    m = hdr.match(line)
    if not m:
        continue
    path, ln, text = m.group(2), int(m.group(3)), m.group(4)
    for mm in PAT.finditer(text):
        pre, base, n = mm.group(1), mm.group(2), int(mm.group(3))
        tot += 1
        if base == "SKILL":
            cands = ["SKILL.md"] if pre == "" else [pre + "SKILL.md"]
        elif base == "SOURCES":
            cands = ["corpus/SOURCES.md"] if pre == "" else [pre + "SOURCES.md"]
        else:
            if pre == "":
                cands = ["corpus/README.md", ROOT_README]
            else:
                cands = [pre + "README.md"]
        cands = [c for c in cands if c in DOCS]
        if not cands:
            other += 1
            continue
        doc = cands[0]
        if len(cands) > 1:
            amb += 1
        intodocs += 1
        if n > len(old[doc]) - 1:
            zone.append(("OUT-OF-RANGE", path, ln, mm.group(0), doc, n, None))
            continue
        nn = mapf(doc, n)
        o = old[doc][n - 1].strip()
        nw = new[doc][nn - 1].strip()
        if o != nw:
            zone.append(("CHANGED", path, ln, mm.group(0), doc, n, (o[:120], nw[:120])))
print(f"total_citations={tot} into_modified_docs={intodocs} ambiguous_readme={amb} other_path={other}")
print(f"zone_entries={len(zone)}")
for z in zone:
    if z[6]:
        print(f"  {z[0]} {z[1]}:{z[2]} cite={z[3]} {z[4]} {z[5]}->{mapf(z[4], z[5])}")
        print("     old:", z[6][0])
        print("     new:", z[6][1])
    else:
        print(f"  {z[0]} {z[1]}:{z[2]} cite={z[3]} {z[4]}:{z[5]}")

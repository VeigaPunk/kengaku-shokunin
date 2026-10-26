import subprocess, re, os
os.chdir("/fast/scratch/hyaku/kengaku-r41/F41CritNoHarmDiff/lane")
OLD = "e50c134556b4ba48e29dc7ff364e90d6ef07a3f3"
NEW = "3d0058fbde484c9d6c23fd997d9ee09a0663bcdb"
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

PAT = re.compile(r"(SKILL|SOURCES|README)\.md:([0-9]+)")
hdr = re.compile(r"^([0-9a-f]{40}):(.+?):([0-9]+):(.*)$", re.S)

def scan(rev):
    out = subprocess.run(["git", "grep", "-nE", PAT.pattern, rev, "--", ":!.ufo"],
                         capture_output=True).stdout.decode("utf-8", "replace")
    rows = []
    for line in out.splitlines():
        m = hdr.match(line)
        if not m:
            continue
        path, ln, text = m.group(2), int(m.group(3)), m.group(4)
        for mm in PAT.finditer(text):
            base, n = mm.group(1), int(mm.group(2))
            # path-qualified sibling citations are skipped by requiring the citing file's dir
            doc = {"SKILL": "SKILL.md", "SOURCES": "corpus/SOURCES.md", "README": "corpus/README.md"}[base]
            pre = text[max(0, mm.start() - 24):mm.start()]
            if re.search(r"[A-Za-z0-9_-]+/[A-Za-z0-9_-]*$", pre) and base != "README":
                continue
            rows.append((path, ln, mm.group(0), doc, n))
    return rows

old_rows = scan(OLD)
new_rows = scan(NEW)
oldset = {(p, l, c) for p, l, c, _, _ in old_rows}
print(f"old-tree citation occurrences={len(old_rows)}  new-tree={len(new_rows)}")
broken = 0
for path, ln, cite, doc, n in old_rows:
    if n > len(old[doc]) - 1 or n > len(new[doc]) - 1:
        print(f"OUT-OF-RANGE {path}:{ln} {cite}")
        continue
    o, nw = old[doc][n - 1].strip(), new[doc][n - 1].strip()
    if o != nw:
        broken += 1
        print(f"BROKEN {path}:{ln} cite={cite}")
        print(f"   old_line[{n}]: {o[:130]}")
        print(f"   new_line[{n}]: {nw[:130]}")
print(f"pre-existing citations broken by literal shift: {broken} of {len(old_rows)}")

# new-only citations (added text) that point past EOF or land on a blank line
newonly = [r for r in new_rows if (r[0], r[1], r[2]) not in oldset]
print(f"citations added in this round={len(newonly)}")
bad = 0
for path, ln, cite, doc, n in newonly:
    if n > len(new[doc]) - 1:
        print(f"  ADDED-OUT-OF-RANGE {path}:{ln} {cite} (doc has {len(new[doc])-1} lines)")
        bad += 1
print(f"added citations out of range: {bad}")

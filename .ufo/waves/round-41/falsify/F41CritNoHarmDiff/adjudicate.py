import subprocess, re, os
os.chdir("/fast/scratch/hyaku/kengaku-r41/F41CritNoHarmDiff/lane")
OLD = "e50c134556b4ba48e29dc7ff364e90d6ef07a3f3"
NEW = "3d0058fbde484c9d6c23fd997d9ee09a0663bcdb"
DOCS = {"SKILL.md": 1, "corpus/README.md": 1, "corpus/SOURCES.md": 1}
def blob(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True).stdout.decode("utf-8", "replace").split("\n")
old = {p: blob(OLD, p) for p in DOCS}
new = {p: blob(NEW, p) for p in DOCS}
PAT = re.compile(r"(SKILL|SOURCES|README)\.md:([0-9]+)")
hdr = re.compile(r"^([0-9a-f]{40}):(.+?):([0-9]+):(.*)$", re.S)
out = subprocess.run(["git", "grep", "-nE", PAT.pattern, OLD, "--", ":!.ufo"], capture_output=True).stdout.decode("utf-8", "replace")

def phrases(text):
    out = []
    for m in re.finditer(r"[`\"\u201c]([^`\"\u201d]{12,120})[`\"\u201d]", text):
        out.append(m.group(1).strip())
    return out

correct_before = broken_now = stale_before = unknown = 0
rows = []
for line in out.splitlines():
    m = hdr.match(line)
    if not m:
        continue
    path, ln, text = m.group(2), int(m.group(3)), m.group(4)
    for mm in PAT.finditer(text):
        base, n = mm.group(1), int(mm.group(2))
        pre = text[max(0, mm.start()-24):mm.start()]
        if re.search(r"[A-Za-z0-9_-]+/[A-Za-z0-9_-]*$", pre) and base != "README":
            continue
        doc = {"SKILL": "SKILL.md", "SOURCES": "corpus/SOURCES.md", "README": "corpus/README.md"}[base]
        if n >= min(len(old[doc]), len(new[doc])):
            rows.append(("OUT", path, ln, mm.group(0), None))
            continue
        if old[doc][n-1].strip() == new[doc][n-1].strip():
            continue  # not affected
        # did the citation resolve correctly at OLD? look for a quoted phrase of the citing line on line n
        ok_old = any(p in old[doc][n-1] for p in phrases(text))
        ok_new = any(p in new[doc][n-1] for p in phrases(text))
        where = [i+1 for i, s in enumerate(old[doc]) if any(p in s for p in phrases(text))] if not ok_old else []
        rows.append(("AFFECTED", path, ln, mm.group(0), (ok_old, ok_new, where[:3])))
        if ok_old and not ok_new:
            correct_before += 1
        elif not ok_old:
            if where:
                stale_before += 1
            else:
                unknown += 1
print(f"AFFECTED citations (old content != new content at literal line): {sum(1 for r in rows if r[0]=='AFFECTED')}")
print(f"  was correct at e50c134, wrong at 3d0058fb (NEW HARM): {correct_before}")
print(f"  already stale at e50c134 (the quoted phrase lived elsewhere): {stale_before}")
print(f"  no quoted phrase to adjudicate: {unknown}")
print(f"  out of range: {sum(1 for r in rows if r[0]=='OUT')}")
for r in rows:
    if r[0] == 'AFFECTED' and r[4][0] and not r[4][1]:
        print("  HARM", r[1]+":"+str(r[2]), r[3], r[4])
for r in rows:
    if r[0] == 'AFFECTED' and not r[4][0]:
        print(f"  stale {r[1]}:{r[2]} {r[3]} phrase-now-at={r[4][2]}")

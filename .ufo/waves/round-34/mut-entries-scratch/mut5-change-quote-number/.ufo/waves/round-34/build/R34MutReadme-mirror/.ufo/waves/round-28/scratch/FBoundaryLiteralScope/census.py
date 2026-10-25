import json, re, subprocess, sys
BASE = "b9b24796277020d1b9b01923b45313d6a565e664"
IDS = ["S038"] + [f"S0{n}" for n in range(49, 61)]
pop = json.load(open("plans/fixtures/r28/registry/population.json"))
def text(rev, path):
    if rev is None:
        return open(path, encoding="utf-8").read()
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
def rows(src):
    out, on = {}, False
    for ln in src.splitlines():
        if ln.startswith("## "): on = ln.strip() == "## Registry"
        if on and ln.startswith("| S"):
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            out[c[0]] = c
    return out
for label, rev in (("baseline", BASE), ("current", None)):
    r = rows(text(rev, "corpus/SOURCES.md"))
    links, bad, variants = 0, [], []
    for sid in IDS:
        cites = sorted(p for p in pop["knowledge_paths"] if re.search(r"(?<![A-Za-z0-9_])" + sid + r"(?![0-9A-Za-z_])", text(rev, p)))
        links += len(cites)
        c = r[sid]; used = [u.strip() for u in re.split(r"[,;]", c[10]) if u.strip() not in ("", "—")]
        miss = [p for p in cites if p not in used]
        if cites and c[7] != "mined": bad.append((sid, "status", c[7]))
        for p in miss: bad.append((sid, "missing", p))
    for p in pop["knowledge_paths"]:
        for m in re.finditer(r"(?i)\bS[\s\-_]?0?(38|49|5\d|60)\b|S0?4[89]\s*[–-]\s*S?0?(5\d|60)|\bsources?\s+(38|49|5\d|60)\b", text(rev, p)):
            if not re.fullmatch(r"S0(38|49|5\d|60)", m.group(0)): variants.append((p, m.group(0)))
    print(label, "links", links, "findings", bad, "variants", variants)

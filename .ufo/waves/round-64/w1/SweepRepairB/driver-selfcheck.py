import pathlib, re, subprocess, datetime

SEAT = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/SweepRepairB")
CLONE = pathlib.Path("/fast/scratch/hyaku/kengaku-r64/SweepRepairB/clone")
TRIO_KEYS = ("source", "verified-at", "recheck")
KEY_RE = re.compile(r"^(source|verified-at|recheck):")

def trio_missing(text):
    seen = []
    for line in text.splitlines()[:12]:
        if line.startswith("## "):
            break
        m = KEY_RE.match(line)
        if m:
            seen.append(m.group(1))
    first = {}
    for i, k in enumerate(seen):
        first.setdefault(k, i)
    missing, last = [], -1
    for k in TRIO_KEYS:
        i = first.get(k)
        if i is None or i <= last:
            missing.append(k)
        else:
            last = i
    return missing

def addendum_rule(text):
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.rstrip() == "## Freshness addendum (round 64)"), None)
    if start is None:
        return False
    block = []
    for l in lines[start + 1:]:
        if l.startswith("## "):
            break
        block.append(l)
    return (any(l.startswith("verified-at: 2026-11-03") for l in block)
            and any(l.startswith("recheck:") for l in block))

head = subprocess.run(["git", "-C", str(CLONE), "rev-parse", "HEAD"],
                      capture_output=True, text=True, check=True).stdout.strip()
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
print(f"# R64-C3 SweepRepairB self-check — {now}")
print(f"# clone HEAD {head}; network: none; lane files untouched")
print("# columns: entry | trio missing at base | addendum rule | class after append | append-only | re-run stable")
out = []
for a in sorted(SEAT.glob("*.addendum.txt")):
    base = a.name[:-len(".addendum.txt")]
    entry = CLONE / "corpus/knowledge" / base
    orig = entry.read_text()
    block = a.read_text()
    combined = orig + block if orig.endswith("\n") else orig + "\n" + block
    append_only = combined[:len(orig)] == orig
    before = trio_missing(orig)
    add = addendum_rule(combined)
    class_after = "ADDENDUM" if add else ("OPEN" if not trio_missing(combined) else "RED")
    cmd = next(l for l in block.splitlines() if l.startswith("recheck: "))[len("recheck: "):]
    proc = subprocess.run(["/bin/bash", "-c", cmd], cwd=CLONE, capture_output=True, text=True)
    rec = (SEAT / f"{base}.reverify.txt").read_text()
    recorded = rec.split("$ " + cmd + "\n", 1)[1].rsplit("\n[exit=", 1)[0]
    stable = recorded.strip() == proc.stdout.strip()
    out.append((base, ",".join(before), add, class_after, append_only, stable, proc.returncode))
    print(f"{base} | {','.join(before)} | {add} | {class_after} | {append_only} | {stable} rc={proc.returncode}")

print(f"SUMMARY entries={len(out)} addendum_rule_all={all(o[2] for o in out)} "
      f"append_only_all={all(o[4] for o in out)} rerun_stable_all={all(o[5] for o in out)} "
      f"repaired={sum(1 for o in out if o[2] and o[3]=='ADDENDUM')} unrepaired={sum(1 for o in out if not (o[2] and o[3]=='ADDENDUM'))}")

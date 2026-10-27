#!/usr/bin/env python3
"""Check an entry's `## Located quotes` table the way plans/pkg_gate.py resolves captures:
capture_dir / <name exactly as written>. No candidate search. Also reports the source: ranges
against physical line counts."""
import re, sys, pathlib
entry = pathlib.Path(sys.argv[1])
cap = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round45/tb2-password-recovery")
print(f"# entry {entry} sha256_pending")
lines = entry.read_text().splitlines()
sec = None; rows = 0; bad = 0
for ln in lines:
    if ln.startswith("## "): sec = ln[3:].strip()
    if sec != "Located quotes": continue
    if not ln.startswith("| ") or ln.count("|") < 4: continue
    parts = [p.strip() for p in ln.strip().strip("|").split("|")]
    if len(parts) < 3: continue
    quote, loc = parts[1], parts[2].strip("`")
    m = re.match(r"(.+):(\d+)$", loc)
    if not m: continue
    rows += 1
    name, n = m.group(1), int(m.group(2))
    p = cap / name
    if not p.exists():
        print(f"UNREADABLE {loc} (capture_dir/{name} absent)"); bad += 1; continue
    body = p.read_text().splitlines()
    q = quote.strip().strip("“”").strip()
    if n <= len(body) and q in body[n-1]:
        print(f"ok {loc}")
    else:
        near = [k+1 for k, L in enumerate(body) if q in L]
        print(f"MISMATCH {loc} found_on={near} physical={len(body) if body[-1].strip() else len(body)}"); bad += 1
print(f"rows={rows} bad={bad}")

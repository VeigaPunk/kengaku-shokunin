import re, pathlib, sys
entry = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/tb2-password-recovery-grader.md")
base = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round45/tb2-password-recovery")
text = entry.read_text().splitlines()
sec = None
rows = []
for i, ln in enumerate(text, 1):
    if ln.startswith("## "):
        sec = ln[3:].strip()
    if sec == "Located quotes" and ln.startswith("| ") and "`" in ln and ":" in ln:
        parts = [p.strip() for p in ln.strip().strip("|").split("|")]
        if len(parts) < 3: continue
        claim, quote, loc = parts[0], parts[1], parts[2]
        loc = loc.strip("`")
        m = re.match(r"([A-Za-z0-9_./-]+):(\d+)$", loc)
        if not m: continue
        f, n = m.group(1), int(m.group(2))
        # capture path resolution
        cand = [base / f, base / "tests" / f, base / "environment" / f, base / "solution" / f]
        path = next((c for c in cand if c.exists()), None)
        q = quote.strip().strip("“”").strip()
        if path is None:
            print(f"NOFILE {loc}"); continue
        lines = path.read_text().splitlines()
        hit = n <= len(lines) and q in lines[n-1]
        if not hit:
            near = [k+1 for k, L in enumerate(lines) if q in L]
            print(f"MISMATCH {loc} quote={q[:60]!r} found_on={near} nlines={len(lines)}")
        else:
            print(f"ok {loc}")

import pathlib, re, json
lane = pathlib.Path('/fast/scratch/hyaku/kengaku-r39/F39XMut/lane')
spec = json.loads((lane / 'plans/pkg-spec-r35.json').read_text())
cap = lane / spec['d5_capture_dir'] / spec['d5']['capture_name']
raw = cap.read_bytes().decode('utf-8')
lines = raw.splitlines()
q = spec['d5']['quote']
print("quote occurrences in RAW:", raw.count(q))
flat_ref = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", raw))
print("quote in flat_ref:", q in flat_ref)
hits = [no for no, l in enumerate(lines, 1) if q in l]
print("quote on raw line(s):", hits)
for no in hits:
    l = lines[no - 1]
    i = l.index(q)
    before, after = l[:i], l[i + len(q):]
    print(f"line {no}: {len(l)} chars")
    print("  tags before quote on the line:", re.findall(r'<[^>]+>', before))
    print("  tags after quote on the line :", re.findall(r'<[^>]+>', after))
# XD5b flat (letter-led tags only)
flat_mut = re.sub(r"\s+", "", re.sub(r"</?[a-zA-Z][^>]*>", "", raw))
print("quote in flat_XD5b:", q in flat_mut)
# XD5c flat (greedy <.*>, dot not crossing newline)
flat_greedy = re.sub(r"\s+", "", re.sub(r"<.*>", "", raw))
print("quote in flat_XD5c(greedy):", q in flat_greedy)

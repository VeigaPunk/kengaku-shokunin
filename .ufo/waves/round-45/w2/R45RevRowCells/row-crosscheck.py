#!/usr/bin/env python3
"""R45RevRowCells — mechanical cross-check of SOURCES rows S149-S156.
Checks per row: sha256(row anchor) == sha256(capture) == sha256(pkg-spec pin) ==
sha256(refetch); quote substring on the cited line; wc -w of the quote vs the
row's "(N words)"; file line count vs the row's "1-N" range; used-by cell.
Read-only. Prints one line per row."""
import hashlib, json, re, pathlib
lane = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
cap = lane / "corpus/evidence/round45/tb2-password-recovery"
src = (lane / "corpus/SOURCES.md").read_text()
rows = {}
for line in src.splitlines():
    m = re.match(r'\| (S1(4[9]|5[0-6])) \|', line)
    if m:
        rows[m.group(1)] = [c.strip() for c in line.strip().strip('|').split('|')]
spec = json.loads((lane / "plans/pkg-spec-r45.json").read_text())
refetch = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45RevRowCells/refetch")
quotes = {
    'S149': ('test_outputs.py', 18, 'assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses', 4, 19),
    'S150': ('instruction.md', 9, 'Write each matching password you find, one per line', 8, 9),
    'S151': ('setup.sh', 30, 'split_point=$((offset + 20))', 4, 45),
    'S152': ('Dockerfile', 15, 'RUN bash /app/setup.sh', 4, 16),
    'S153': ('test.sh', 28, 'echo 1 > /logs/verifier/reward.txt', 6, 31),
    'S154': ('README.md', 44, 'is among the recovered passwords', 5, 46),
    'S155': ('solve.sh', 63, 'echo "$combined" >> "$OUTPUT_FILE"', 3, 70),
    'S156': ('task.toml', 34, 'allow_internet = true', 3, 41),
}
ok = lambda b: 'OK' if b else 'BAD'
for rid, cells in sorted(rows.items()):
    anchor, usedby = cells[5], cells[10]
    sha_row = re.search(r'sha256 ([0-9a-f]{64})', anchor).group(1)
    fname, cited, quote, claimed_words, claimed_hi = quotes[rid]
    data = (cap / fname).read_bytes()
    sha_cap = hashlib.sha256(data).hexdigest()
    sha_spec = spec["rows"][rid]["sha256"]
    sha_ref = hashlib.sha256((refetch / fname).read_bytes()).hexdigest()
    text = data.decode()
    nlines = text.count('\n') + (0 if text.endswith('\n') else 1)
    lines = text.split('\n')
    actual_lines = [i + 1 for i, l in enumerate(lines) if quote in l]
    words = len(quote.split())
    print(f"{rid} sha row==cap:{ok(sha_row==sha_cap)} ==spec:{ok(sha_row==sha_spec)} "
          f"==refetch:{ok(sha_row==sha_ref)} | quote cited:{cited} "
          f"on-cited:{ok(cited in actual_lines)} actual:{actual_lines} | "
          f"words claimed:{claimed_words} actual:{words} {ok(claimed_words==words)} | "
          f"range 1-{claimed_hi} vs 1-{nlines} {ok(claimed_hi==nlines)} | usedby:{usedby}")

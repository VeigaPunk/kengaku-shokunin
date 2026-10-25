#!/usr/bin/env bash
# F35ReopenS106S107 — reproducible re-open of S106 (tests/test.sh) and S107 (instruction.md)
# Read-only against the lane and against raw.githubusercontent.com. Writes only into this dir.
#
#   bash .ufo/waves/round-35/falsify/F35ReopenS106S107/repro.sh
#
# Exit 0 = no defect found; exit 1 = at least one defect.
set -u
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
PIN=2fd12b88aafdd04a52c298e3940bcb189f9766d6
BASE="https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/$PIN/protein-assembly"
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=$(mktemp -d /tmp/k35f-reopen-repro-XXXX)
trap 'rm -rf "$WORK"' EXIT
rc=0

say() { printf '\n=== %s ===\n' "$1"; }

say "1. FETCH the pinned URLs (HTTP status + bytes)"
for spec in "tests/test.sh:test.sh" "instruction.md:instruction.md" "tests/test_outputs.py:test_outputs.py"; do
  p=${spec%%:*}; out=${spec##*:}
  code=$(curl -sSL -o "$WORK/$out" -w '%{http_code}' "$BASE/$p")
  printf '%-22s http=%s bytes=%s sha256=%s\n' "$p" "$code" \
    "$(wc -c <"$WORK/$out" | tr -d ' ')" "$(sha256sum "$WORK/$out" | cut -d' ' -f1)"
done

say "2. MANIFEST sha256sum -c (all six capture files)"
( cd "$LANE/corpus/evidence/round35/tb2-eval" && sha256sum -c SHA256SUMS )

say "3. ROW ANCHORS: quoted span present verbatim on the cited line?"
python3 - "$LANE" "$WORK" <<'PY'
import pathlib, re, sys
lane, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
src = {p.name: p.read_text().splitlines() for p in work.iterdir()}
text = (lane / "corpus/SOURCES.md").read_text()
want = {"S106": "test.sh", "S107": "instruction.md"}
bad = 0
for line in text.splitlines():
    m = re.match(r"^\|\s*(S10[67])\s*\|", line)
    if not m:
        continue
    rid = m.group(1)
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    anchor = cells[5]
    for lm in re.finditer(r"(tests/test\.sh|instruction\.md):(\d+)\s*\"([^\"]+)\"", anchor):
        path, ln, quote = lm.group(1), int(lm.group(2)), lm.group(3)
        f = work / ("test.sh" if path.endswith("test.sh") else "instruction.md")
        lines = f.read_text().splitlines()
        ok = 1 <= ln <= len(lines) and quote in lines[ln - 1]
        print(f"  {rid} {path}:{ln} verbatim={ok}  {quote[:62]!r}")
        if not ok:
            bad += 1
    for qm in re.finditer(r':(\d+)\s+"([^"]+)"', anchor):
        pass
    # the ":21" continuation form for S106
    for lm in re.finditer(r'and :(\d+)\s+"([^"]+)"', anchor):
        ln, quote = int(lm.group(1)), lm.group(2)
        lines = (work / "test.sh").read_text().splitlines()
        ok = 1 <= ln <= len(lines) and quote in lines[ln - 1]
        print(f"  {rid} test.sh:{ln} (continuation form) verbatim={ok}  {quote!r}")
        if not ok:
            bad += 1
sys.exit(1 if bad else 0)
PY
[ $? -ne 0 ] && rc=1

say "4. PARENTHETICAL WORD COUNTS vs the lane's canonical counter (len(text.split()))"
python3 - "$LANE" <<'PY'
import pathlib, re, sys
text = pathlib.Path(sys.argv[1], "corpus/SOURCES.md").read_text()
pat = re.compile(r'"([^"]+)"\s*\((\d+) words?\)')
bad = 0
for line in text.splitlines():
    if not re.match(r"^\|\s*S\d+\s*\|", line):
        continue
    rid = re.match(r"^\|\s*(S\d+)", line).group(1)
    for q, n in pat.findall(line):
        actual = len(q.split())
        flag = "OK " if actual == int(n) else "MISMATCH"
        if actual != int(n):
            bad += 1
        print(f"  {flag} {rid}: claimed={n} canonical(len split)={actual}  {q[:58]!r}")
print(f"  mismatching parentheticals in the whole registry: {bad}")
sys.exit(1 if bad else 0)
PY
[ $? -ne 0 ] && rc=1

say "5. S107 teaches cell: 'fifteen requirement bullets' vs the file"
python3 - "$WORK" <<'PY'
import pathlib, sys
L = pathlib.Path(sys.argv[1], "instruction.md").read_text().splitlines()
b = [(i + 1, l) for i, l in enumerate(L) if l.startswith(" * ")]
print(f"  bullets in instruction.md = {len(b)}  (row claims fifteen)")
for i, l in b:
    print(f"    {i:>2}: {l.strip()[:80]}")
sys.exit(0 if len(b) == 15 else 1)
PY
[ $? -ne 0 ] && rc=1

say "6. ENTRY Located quotes: every quote verbatim on the cited line of the FRESH fetch?"
python3 - "$LANE" "$WORK" <<'PY'
import pathlib, re, sys
lane, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
up = {p.name: p.read_text().splitlines() for p in work.iterdir()}
alias = {"test.sh": "test.sh", "instruction.md": "instruction.md",
         "test_outputs.py": "test_outputs.py"}
text = (lane / "corpus/knowledge/tb2-protein-assembly-grader.md").read_text()
sec = re.search(r"^## Located quotes\n(.*?)(?=^## |\Z)", text, re.S | re.M).group(1)
n = bad = 0
for line in sec.splitlines():
    m = re.match(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$", line)
    if not m:
        continue
    q, f, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
    n += 1
    if f not in up:
        print(f"  SKIP (not re-fetched here) {f}:{a}  {q[:50]!r}")
        continue
    span = "\n".join(up[f][a - 1:b])
    if q not in span:
        bad += 1
        print(f"  BAD {f}:{a}-{b}  {q[:60]!r}")
print(f"  quoted rows checked against fresh bytes: {n}, not-verbatim: {bad}")
sys.exit(1 if bad else 0)
PY
[ $? -ne 0 ] && rc=1

say "7. FRESHNESS: pinned bytes vs upstream main (drift check)"
for spec in "tests/test.sh:test.sh" "instruction.md:instruction.md"; do
  p=${spec%%:*}; out=${spec##*:}
  curl -sSL -o "$WORK/main_$out" "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/main/protein-assembly/$p"
  if cmp -s "$WORK/$out" "$WORK/main_$out"; then
    printf '  %-18s main == pinned (no upstream drift)\n' "$p"
  else
    printf '  %-18s DRIFT: main differs from the pinned commit\n' "$p"; rc=1
  fi
done

say "8. FROZEN COUNTERS (read-only in the lane)"
( cd "$LANE" && python3 plans/round35_c1_verify.py --lane . | tail -3 )
( cd "$LANE" && python3 plans/defect_ledger.py --lane . | tail -3 )

say "RESULT"
if [ "$rc" -eq 0 ]; then echo "no defect"; else echo "DEFECT FOUND (see MISMATCH lines above)"; fi
exit "$rc"

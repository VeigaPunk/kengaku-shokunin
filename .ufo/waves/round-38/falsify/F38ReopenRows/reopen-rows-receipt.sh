#!/bin/bash
# F38ReopenRows (kengaku round 38, wave 2 falsify) — re-open rows S115/S116 live at
# terminal-bench-2 2fd12b88, test whether anything checks a SOURCES row's quote, and test the
# entry's documented recheck command. Read-only against the lane; mutations run in a clone.
set -u
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
PIN=2fd12b88aafdd04a52c298e3940bcb189f9766d6
S=$(mktemp -d /fast/scratch/hyaku/kengaku-r38/F38ReopenRows/rcpt.XXXXXX)
export TMPDIR="$S"
trap 'rm -rf -- "$S"' EXIT
RAW=https://raw.githubusercontent.com/harbor-framework

echo "## A. live fetch at the pin: sha256 vs the rows' anchors"
for p in build-pmars/tests/test_outputs.py build-pmars/instruction.md \
         build-pmars/tests/test.sh build-pmars/task.toml \
         build-pmars/solution/solve.sh build-pmars/environment/Dockerfile; do
  out="$S/$(basename "$p")"
  code=$(curl -sS -o "$out" -w '%{http_code}' "$RAW/terminal-bench-2/$PIN/$p")
  echo "$code $(sha256sum "$out" | cut -d' ' -f1) $p"
done
echo "row anchors: S115 d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85"
echo "row anchors: S116 1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82"

echo "## B. capture manifest (run inside its own dir, the only form that works)"
( cd "$LANE/corpus/evidence/round38/tb2-build-pmars" && sha256sum -c SHA256SUMS )

echo "## C. live bytes == committed captures"
for f in test_outputs.py instruction.md test.sh task.toml; do
  cmp "$S/$f" "$LANE/corpus/evidence/round38/tb2-build-pmars/$f" && echo "$f byte-identical"
done
cmp "$S/solve.sh" "$LANE/corpus/evidence/round38/tb2-build-pmars/solve.sh" && echo "solve.sh byte-identical"

echo "## D. row parse: cells, anchor tokens, cited line, quote == that line"
python3 - "$LANE" <<'PY'
import re, sys
lane = sys.argv[1]
txt = open(lane + "/corpus/SOURCES.md").read().splitlines()
SR = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
for line in txt:
    m = SR.match(line)
    if not (m and m.group(1) in ("S115", "S116")):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    a = cells[5]
    q = re.search(r"\u201c(.+)\u201d\s*\(\d+ words\)", a).group(1)
    cited = int(re.search(r":(\d+) \u201c", a).group(1))
    fname = "test_outputs.py" if m.group(1) == "S115" else "instruction.md"
    src = open(lane + "/corpus/evidence/round38/tb2-build-pmars/" + fname).read().splitlines()
    print(f"{m.group(1)} cells={len(cells)} anchor_tokens={re.findall(r'sha256\s+([0-9a-f]{64})', a)} "
          f"cited={fname}:{cited} words={len(q.split())} quote==line.strip()={src[cited-1].strip()==q}")

PY
echo "-- the two cited lines as sed prints them:"
sed -n '46p' "$LANE/corpus/evidence/round38/tb2-build-pmars/test_outputs.py"
sed -n '9p'  "$LANE/corpus/evidence/round38/tb2-build-pmars/instruction.md"

echo "## E. upstream main and TB2.1 (grader drift)"
curl -sS https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/main \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print("terminal-bench-2 HEAD", d["sha"], d["commit"]["committer"]["date"])'
T21=7131e4375048a0e408a8fb404b5f499d726b695b
for p in tests/test_outputs.py instruction.md solution/solve.sh tests/test.sh task.toml environment/Dockerfile; do
  out="$S/t21_$(echo "$p" | tr / _)"
  code=$(curl -sS -o "$out" -w '%{http_code}' "$RAW/terminal-bench-2-1/$T21/tasks/build-pmars/$p")
  same=$(cmp -s "$out" "$S/$(basename "$p")" && echo SAME-AS-PIN || echo DIFFERS)
  echo "$code $(sha256sum "$out" | cut -d' ' -f1) tb2-1@$T21 $p $same"
done
echo "-- instruction.md diff (pin -> tb2-1):"
diff "$S/instruction.md" "$S/t21_instruction.md"
echo "-- solve.sh diff (pin -> tb2-1):"
diff "$S/solve.sh" "$S/t21_solution_solve.sh"

echo "## F. does any clause read a SOURCES row's quote?"
git clone -q --no-local "$LANE" "$S/lane" && git -C "$S/lane" checkout -q 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
echo "clone toplevel=$(git -C "$S/lane" rev-parse --show-toplevel)"
echo "-- V3 (round38_c2_verify.py) before any mutation:"
python3 -c "
import sys; sys.path.insert(0,'$S/lane/plans'); import round38_c2_verify as m
from pathlib import Path; print(m.v3(Path('$S/lane')))"
python3 - "$S/lane" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "corpus/SOURCES.md"
t = p.read_text()
old = ':46 \u201cassert re.match(r"Results: \\d+ \\d+ \\d+", battle_result), (\u201d (7 words)'
new = ':46 \u201cFORGED QUOTE THAT IS NOT IN THE FILE AT ALL AND NEVER WILL BE (7 words)\u201d (7 words)'
assert t.count(old) == 1, t.count(old)
p.write_text(t.replace(old, new))
print("-- S115 anchor quote replaced, digest token untouched")
PY
echo "-- V3 after forging the S115 row quote:"
python3 -c "
import sys; sys.path.insert(0,'$S/lane/plans'); import round38_c2_verify as m
from pathlib import Path; print(m.v3(Path('$S/lane')))"
echo "-- package gate on the forged-row tree (no --rerun, so P2 cannot run a probe):"
( cd "$S/lane" && python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r38.json 2>&1 | grep -E '^P[0-9]' )
git -C "$S/lane" show HEAD:corpus/SOURCES.md > "$S/lane/corpus/SOURCES.md"
echo "-- same gate with the ENTRY's copy of the same quote forged instead (re.match -> re.fullmatch):"
python3 - "$S/lane" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "corpus/knowledge/tb2-build-pmars-grader.md"
t = p.read_text()
old = '\u201cassert re.match(r"Results: \\d+ \\d+ \\d+", battle_result), (\u201d'
new = '\u201cassert re.fullmatch(r"Results: \\d+ \\d+ \\d+", battle_result), (\u201d'
assert t.count(old) == 1
p.write_text(t.replace(old, new)); print("-- entry located-quote for test_outputs.py:46 forged")
PY
( cd "$S/lane" && python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r38.json 2>&1 | grep -E '^P[0-9]' )
git -C "$S/lane" show HEAD:corpus/knowledge/tb2-build-pmars-grader.md > "$S/lane/corpus/knowledge/tb2-build-pmars-grader.md"
echo "-- clone status after restore: [$(git -C "$S/lane" status --short | tr '\n' ' ')]"

echo "## G. the entry's documented recheck command, run from the lane root"
sha256sum -c corpus/evidence/round38/tb2-build-pmars/SHA256SUMS >/dev/null 2>&1
echo "round38 exit=$?"
sha256sum -c corpus/evidence/round37/tb2-git-webserver/SHA256SUMS >/dev/null 2>&1
echo "round37 exit=$?"

echo "## H. the upstream items the entry cites"
for u in terminal-bench-2/issues/59 terminal-bench-2/pulls/38 terminal-bench/issues/631; do
  curl -sS "https://api.github.com/repos/harbor-framework/$u" \
    | python3 -c '
import json,sys
d=json.load(sys.stdin)
print("'"$u"'", d.get("state"), d.get("created_at"), repr(d.get("title")))'
done
curl -sS https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53/files \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print("PR53 build-pmars files:", [f["filename"] for f in d if "pmars" in f["filename"]])'
curl -sS https://api.github.com/repos/harbor-framework/terminal-bench/issues/631 \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); b=(d.get("body") or "").splitlines(); print("issue631 line19:", b[18])'

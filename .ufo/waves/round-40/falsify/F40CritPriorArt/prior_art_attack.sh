#!/usr/bin/env bash
# F40CritPriorArt — wave-2 attack on the entry's §Prior art
#   (corpus/knowledge/tb2-db-wal-recovery-grader.md:294-319), lane tip ec1005a2.
# Read-only: HTTP GETs + local hashes. Writes only under $TMPDIR.
# Run: bash prior_art_attack.sh   (inside the mandated bwrap wrapper)
set -u
T=${TMPDIR:-/tmp}
P=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round40/tb2-db-wal-recovery
SHA_TEST=88dc5c2a3abba75bca0e0f9136223ae5bb585d5984b8d9eba51a7829c1d2ba49
SHA_INST=5a20375162921b8911c67035d1905df7fd335d1bed03044271e608b2c3c93b26
SHA_DOCK=63a260531c62f4ae72060db17f295c0aa03cfc6321f8162c324b7aa6b3f81302
say(){ printf 'CHECK %-4s %-4s %s\n' "$1" "$2" "$3"; }
h(){ sha256sum | cut -d' ' -f1; }

# ---- A: TB2.1 main carries the same three task bytes -----------------------
for spec in "tests/test_outputs.py:$SHA_TEST" "instruction.md:$SHA_INST" "environment/Dockerfile:$SHA_DOCK"; do
  f=${spec%%:*}; want=${spec##*:}
  got=$(curl -sSL -m 60 "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2-1/main/tasks/db-wal-recovery/$f" | h)
  [ "$got" = "$want" ] && say A PASS "$f == pinned $want" || say A FAIL "$f live=$got pinned=$want"
done
# ---- A2: the other six files TB2.1 ships ---------------------------------
for f in solution/solve.sh tests/test.sh task.toml environment/main.db environment/main.db-wal.encrypted README.md; do
  a=$(curl -sSL -m 60 "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2-1/main/tasks/db-wal-recovery/$f" | h)
  b=$(curl -sSL -m 60 "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/$f" | h)
  [ "$a" = "$b" ] && say A2 PASS "$f tb2.1==tb2 $a" || say A2 FAIL "$f tb2.1=$a tb2=$b"
done
# ---- B: TB2 main (unpinned) no drift -------------------------------------
for spec in "tests/test_outputs.py:$SHA_TEST" "instruction.md:$SHA_INST" "environment/Dockerfile:$SHA_DOCK"; do
  f=${spec%%:*}; want=${spec##*:}
  got=$(curl -sSL -m 60 "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/main/db-wal-recovery/$f" | h)
  [ "$got" = "$want" ] && say B PASS "tb2 main $f == pinned" || say B FAIL "tb2 main $f=$got"
done
# ---- C: zai-org verified fork (the copy agents downloaded, harbor #3607) --
got=$(curl -sSL -m 60 "https://huggingface.co/datasets/zai-org/terminal-bench-2-verified/resolve/main/db-wal-recovery/tests/test_outputs.py" | h)
[ "$got" = "$SHA_TEST" ] && say C PASS "zai-org fork test_outputs.py == pinned" || say C FAIL "zai-org fork=$got"
# ---- D: the four pinned objects of the entry's other bullets -------------
curl -sSL -m 60 -o "$T/wal.html" https://www.sqlite.org/wal.html
HERE=$(cd "$(dirname "$0")" && pwd)
python3 "$HERE/check_wal_section.py" "$T/wal.html"
curl -sSL -m 60 https://www.sqlite.org/fileformat2.html | grep -q '0x377f0682 or 0x377f0683' \
  && say D PASS "fileformat2 §4.1 carries both magics" || say D FAIL "magics absent"
[ "$(head -c4 "$P/main.db-wal.encrypted" | od -An -tx1 | tr -d ' \n')" = 753d44c0 ] \
  && say D PASS "encrypted WAL starts 753d44c0" || say D FAIL "encrypted prefix differs"
# ---- E: GitHub objects the entry dates/quotes ----------------------------
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  st=$(gh api repos/harbor-framework/terminal-bench-2-1/pulls/3 --jq '.state+" merged="+(.merged|tostring)+" created="+.created_at+" files="+(.changed_files|tostring)')
  say E INFO "pr3 $st"
  gh api repos/harbor-framework/terminal-bench-2-1/pulls/3 --jq '.body' \
    | grep -q "Opening the database with a normal read-write SQLite connection can truncate or remove that file before the agent has inspected it" \
    && say E PASS "pr3 §Reasoning quote verbatim (21 words)" || say E FAIL "pr3 quote absent"
  gh api repos/harbor-framework/terminal-bench-2-1/pulls/3/files --jq '.[].filename' | tr '\n' ' ' | sed 's/^/CHECK E    INFO pr3 changed: /'
  c=$(gh api repos/harbor-framework/terminal-bench/issues/comments/6131410584 --jq '.created_at')
  say E INFO "tb#2218 comment created $c"
  gh api repos/harbor-framework/harbor/issues/3607 --jq '.created_at' | sed 's/^/CHECK E    INFO harbor#3607 created /'
  # ---- F: the cited audit — locator and body -----------------------------
  code=$(curl -sSL -m 60 -o "$T/jg_root.txt" -w '%{http_code}' "https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/35f11039/audit.txt")
  [ "$code" = 200 ] && say F PASS "root audit.txt resolvable at 35f11039" || say F FAIL "cited path audit.txt @35f11039 -> HTTP $code"
  curl -sSL -m 90 -o "$T/jg.txt" "https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/35f11039/audit_results/20260120_125158/audit.txt"
  sed -n '753p;782,784p;796p' "$T/jg.txt" | sed 's/^/CHECK F    INFO audit /'
  # ---- G: second public audit naming this task ---------------------------
  gh api repos/kimjune01/terminal-bench-audit/contents/results/verdicts-2.1.jsonl --jq '.download_url' 2>/dev/null \
    | xargs -r curl -sSL -m 60 -o "$T/kj.jsonl"
  grep -c '"task":"db-wal-recovery"' "$T/kj.jsonl" 2>/dev/null | sed 's/^/CHECK G    INFO kimjune01 db-wal-recovery verdict rows: /'
  grep '"task":"db-wal-recovery"' "$T/kj.jsonl" 2>/dev/null | grep FRAME_BLIND | sed 's/^/CHECK G    INFO /'
  # ---- H: public executed fabrication report -----------------------------
  gh api repos/dzhioev/bro/issues/659 --jq '.created_at+" | "+(.body|split("\n")[7])' 2>/dev/null | sed 's/^/CHECK H    INFO bro#659 /'
  gh api repos/dzhioev/bro/issues/659 --jq '.body' 2>/dev/null \
    | grep -q "The verifier caught it only because the two updates in the lost WAL were unguessable" \
    && say H PASS "bro#659 states the grader's discrimination rests on the two pinned values" || say H FAIL "sentence absent"
  # ---- I: re-search for a public 22/33 report ----------------------------
  for r in harbor-framework/terminal-bench harbor-framework/terminal-bench-2 harbor-framework/terminal-bench-2-1 harbor-framework/harbor; do
    n=$(gh search issues "recovered.json" --repo "$r" --limit 30 --json number 2>/dev/null | grep -o '"number"' | wc -l)
    say I INFO "issues/PRs in $r matching recovered.json: $n"
  done
  say I INFO "no public hit states a count of pinned cells (searches logged in report §4)"
else
  say E SKIP "gh unavailable in this namespace (auth/keyring); gh-based checks run outside bwrap, logged in report"
fi

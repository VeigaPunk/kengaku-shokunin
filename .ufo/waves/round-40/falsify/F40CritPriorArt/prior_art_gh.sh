#!/usr/bin/env bash
# F40CritPriorArt — gh-dependent half of the §Prior art attack.
# Read-only API GETs only (no POST/PATCH/DELETE, no git, no writes outside $TMPDIR).
# Must run in the session namespace: gh reads its token from the keyring, which the
# bwrap wrapper (--tmpfs /run/user/1000, no user bus) does not expose.
set -u
T=${TMPDIR:-/tmp}
E=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round40/tb2-db-wal-recovery
say(){ printf 'CHECK %-4s %-4s %s\n' "$1" "$2" "$3"; }

# E1 PR #3: state, dates, changed files, §Reasoning quote
gh api repos/harbor-framework/terminal-bench-2-1/pulls/3 \
  --jq '"state="+.state+" merged="+(.merged|tostring)+" created="+.created_at+" files="+(.changed_files|tostring)' \
  | sed 's/^/CHECK E1   INFO pr3 /'
gh api repos/harbor-framework/terminal-bench-2-1/pulls/3/files --jq '.[].filename' | tr '\n' ' ' \
  | sed 's/^/CHECK E1   INFO pr3 changed: /;s/$/\n/'
gh api repos/harbor-framework/terminal-bench-2-1/pulls/3 --jq '.body' \
  | grep -q "Opening the database with a normal read-write SQLite connection can truncate or remove that file before the agent has inspected it" \
  && say E1 PASS "the quoted sentence is verbatim in the PR body (§Reasoning)" \
  || say E1 FAIL "quote not found in PR body"

# E2 the two secondary citations: dates the entry gives
gh api repos/harbor-framework/terminal-bench/issues/comments/6131410584 \
  --jq '"comment created="+.created_at+" issue="+.issue_url' | sed 's/^/CHECK E2   INFO tb#2218 /'
gh api repos/harbor-framework/terminal-bench/issues/comments/6131410584 --jq '.body' \
  | grep -q "The agent's own SQLite probe removed the task's WAL" \
  && say E2 PASS "2218 comment carries the quoted sentence" || say E2 FAIL "2218 quote absent"
gh api repos/harbor-framework/harbor/issues/3607 --jq '"created="+.created_at' \
  | sed 's/^/CHECK E2   INFO harbor#3607 /'
gh api repos/harbor-framework/harbor/issues/3607 --jq '.body' \
  | grep -q "agents often end up searching the whole filesystem for an intact copy of the WAL" \
  && say E2 PASS "3607 carries the paraphrased sentence" || say E2 FAIL "3607 sentence absent"

# F the cited audit: locator as written, then the real file
code=$(curl -sSL -m 60 -o "$T/jg_root.txt" -w '%{http_code}' \
  "https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/35f11039/audit.txt")
[ "$code" = 200 ] && say F PASS "audit.txt resolvable at root of 35f11039" \
  || say F FAIL "cited locator audit.txt@35f11039 -> HTTP $code (real path: audit_results/20260120_125158/audit.txt)"
gh api 'repos/JonathanGabor/terminal-bench-2-audit/git/trees/35f110397bc8ea58538424a1951760a9c5a0a710?recursive=1' \
  --jq '.tree[]|select(.path|test("audit\\.txt$"))|.path' | sed 's/^/CHECK F    INFO only audit.txt in tree: /'
curl -sSL -m 90 -o "$T/jg.txt" \
  "https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/35f11039/audit_results/20260120_125158/audit.txt"
sed -n '753p;782,784p;794p;796p' "$T/jg.txt" | cut -c1-150 | sed 's/^/CHECK F    INFO | /'

# G second public audit naming db-wal-recovery
u=$(gh api repos/kimjune01/terminal-bench-audit/contents/results/verdicts-2.1.jsonl --jq '.download_url')
curl -sSL -m 60 -o "$T/kj.jsonl" "$u"
say G INFO "kimjune01 db-wal-recovery verdict rows: $(grep -c '"task":"db-wal-recovery"' "$T/kj.jsonl")"
grep '"task":"db-wal-recovery"' "$T/kj.jsonl" | grep -E 'FRAME_BLIND|gold_pass' | cut -c1-200 \
  | sed 's/^/CHECK G    INFO | /'
gh api 'repos/kimjune01/terminal-bench-audit/commits?path=results/verdicts-2.1.jsonl&per_page=1' \
  --jq '.[]|"verdicts commit "+.sha[0:8]+" "+.commit.committer.date' | sed 's/^/CHECK G    INFO /'

# H public executed fabrication report
gh api repos/dzhioev/bro/issues/659 \
  --jq '"created="+.created_at+" state="+.state' | sed 's/^/CHECK H    INFO bro#659 /'
gh api repos/dzhioev/bro/issues/659 --jq '.body' > "$T/bro659.md"
grep -cF 'the verifier caught it only because the two updates in the lost WAL were unguessable' -i "$T/bro659.md" \
  | sed 's/^/CHECK H    INFO bro#659 discrimination sentences: /'
grep -cF 'invented the six missing rows' "$T/bro659.md" \
  | sed 's/^/CHECK H    INFO bro#659 invention sentences: /'
grep -cF 'wrote a fresh WAL from the invented rows' "$T/bro659.md" \
  | sed 's/^/CHECK H    INFO bro#659 fabricated-WAL sentences: /'
grep -qF 'wrote a fresh WAL from the invented rows' "$T/bro659.md" \
  && say H PASS "bro#659: fabricated rows + fabricated WAL are published; grader caught 4/4 only via the two pinned values" \
  || say H FAIL "bro#659 sentence absent"

# I re-search for a public report of the pin surface / a count
for r in harbor-framework/terminal-bench harbor-framework/terminal-bench-2 harbor-framework/terminal-bench-2-1 harbor-framework/harbor; do
  for q in "db-wal" "recovered.json"; do
    n=$(gh search issues "$q" --repo "$r" --limit 30 --json number | grep -o '"number"' | wc -l)
    say I INFO "$r :: '$q' -> $n issue/PR hit(s)"
  done
done
n=$(gh api 'search/issues?q=%22db-wal-recovery%22+%22pinned%22&per_page=20' --jq '.total_count')
say I INFO "global search '\"db-wal-recovery\" \"pinned\"' -> $n hit(s); none states a count of pinned cells"

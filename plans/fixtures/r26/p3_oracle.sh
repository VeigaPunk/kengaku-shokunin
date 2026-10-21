#!/bin/sh
# p3_oracle.sh — independent oracle for the round-26 C2 population P3a / P3b / P3e
# (plans/round-26-claims.md §C2). POSIX sh + grep + awk; no python, no git, no network
# (--selftest also uses mkdir/cp/mv/rm on a scratch copy). Written without reading plans/state_check.py.
#
# Population, enumerated by this oracle's author at base f11bffbf:
#   P3a  SCORECARD capability rows `interval-reverdict` (:558) and `state-assertion-check` (:559): every
#        digit-bearing token of the row against the round-25 v2 receipts in corpus/evidence/round25-calibration/;
#        a coverage guard proves no digit-bearing token of either row is left unchecked or unclassified.
#   P3b  PROVINCE §Province map rows :112 (Public-literature registry), :116, :117 and the :119 round-25 correction,
#        against the SOURCES census at the measured tree (grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md)
#        and the round-25 receipts.
#   P3e  corpus/README index rows and corpus entries (knowledge/*.md, lessons/*.md, evidence/<dir>/) present at
#        f11bffbf and absent at 6180e4f (`git diff --name-status 6180e4f f11bffbf -- corpus/`), both directions:
#        row -> target exists, entry -> index row exists.
#   X.*  oracle-only extension (numeric tokens inside the P3e rows); printed, excluded from totals and exit code.
# Supersession (R25-E rule, widened): a stale assertion is SUPERSEDED only by a later line of the same file that
# matches R2[5-9]-E[0-9], names the assertion's subject and carries the re-derived value.
#
# Usage: sh p3_oracle.sh [ROOT]              ROOT defaults to the lane root three levels above this file
#        sh p3_oracle.sh --selftest [ROOT]   mutation red/green checks on a scratch copy of ROOT (base f11bffbf
#                                            or a descendant whose only P3 drift is R26-E1..E3 + the P3e row)
# Output: "<STATUS>: <id>:<line> — <detail>" per assertion, STATUS in MATCH|MISMATCH|SUPERSEDED|UNVERIFIED
#         (UNVERIFIED = no committed receipt exhibits the claimed token; not a contradiction); "SKIP:" lines list
#         digit-bearing tokens that are labels, names, dates or commit ids; then TOTAL and VERDICT lines.
# Exit: 0 = no registered MISMATCH; 1 = >=1 registered MISMATCH or a selftest failure; 2 = usage / not a lane root.
set -u
LC_ALL=C
export LC_ALL

usage() { echo "usage: sh p3_oracle.sh [--selftest] [ROOT]" >&2; exit 2; }

SELF=$0
MODE=run
case ${1-} in
  --selftest) MODE=selftest; shift ;;
  -*) usage ;;
esac
[ $# -le 1 ] || usage
if [ $# -eq 1 ]; then
  R=$1
else
  case $SELF in */*) d=${SELF%/*} ;; *) d=. ;; esac
  R=$(cd "$d/../../.." && pwd) || exit 2
fi
for f in SCORECARD.md PROVINCE.md corpus/README.md corpus/SOURCES.md; do
  [ -f "$R/$f" ] || { echo "p3_oracle: $R is not a lane root (missing $f)" >&2; exit 2; }
done

RC=corpus/evidence/round25-calibration
SUM=$RC/attrib-calibration-summary-v2.txt
SLF=$RC/attrib-calibration-selftest-v2.txt
SCA=$RC/state-check-after-v2.txt
SCS=$RC/state-check-selftest-v2.txt
CB=$RC/round25-census-before-6180e4f.txt
CA=$RC/round25-census-after.txt
P3E_ROWS='knowledge/attribution-interval-calibration.md lessons/round-24-verifier-spotcheck.md lessons/round-25.md evidence/round25-sources/ evidence/round25-calibration/'
P3E_FILES='evidence/round25-calibration/ evidence/round25-sources/ knowledge/attribution-interval-calibration.md lessons/round-25-verifier-spotcheck.md lessons/round-25.md'

# ---------- helpers ----------
N=0 NM=0 NX=0 NS=0 NU=0 NK=0 XM=0 XX=0
emit() {  # STATUS ID LINE DETAIL...
  _st=$1 _id=$2 _ln=$3; shift 3
  case $_id in
    X.*) case $_st in MATCH) XM=$((XM+1)) ;; *) XX=$((XX+1)) ;; esac ;;
    *) N=$((N+1))
       case $_st in MATCH) NM=$((NM+1)) ;; MISMATCH) NX=$((NX+1)) ;; SUPERSEDED) NS=$((NS+1)) ;; UNVERIFIED) NU=$((NU+1)) ;; esac ;;
  esac
  printf '%s: %s:%s — %s\n' "$_st" "$_id" "$_ln" "$*"
}
skip() { NK=$((NK+1)); printf 'SKIP: %s:%s — %s\n' "$1" "$2" "$3"; }
lineno() {  # FILE ERE -> line number when exactly one line matches, else empty
  grep -nE -- "$2" "$R/$1" 2>/dev/null | awk -F: 'NR==1{l=$1} END{if (NR==1) print l}'
}
textat() { awk -v n="$2" 'NR==n{print; exit}' "$R/$1"; }
grab() {  # TEXT ERE -> first match
  printf '%s\n' "$1" | awk -v re="$2" '{ if (match($0, re)) { print substr($0, RSTART, RLENGTH); exit } }'
}
nums() {  # TEXT -> digit runs, space separated
  printf '%s\n' "$1" | awk '{ s=$0; o=""; while (match(s, /[0-9]+/)) { o = o (o=="" ? "" : " ") substr(s, RSTART, RLENGTH); s = substr(s, RSTART+RLENGTH) } print o }'
}
nth() { printf '%s\n' "$1" | awk -v n="$2" '{print $n}'; }
cell() {  # TEXT N -> N-th |-separated table cell, trimmed
  printf '%s\n' "$1" | awk -F'|' -v n="$2" '{ c=$(n+1); sub(/^ +/, "", c); sub(/ +$/, "", c); print c }'
}
field() {  # FILE KEY -> value of the first whitespace token KEY=value
  awk -v k="$2" '{ for (i=1; i<=NF; i++) if (index($i, k "=") == 1) { print substr($i, length(k)+2); exit } }' "$R/$1" 2>/dev/null
}
trans() {  # TRANSITIONS KEY -> count
  printf '%s\n' "$1" | awk -v k="$2" '{ n=split($0, a, ","); for (i=1; i<=n; i++) { split(a[i], b, ":"); if (b[1] == k) print b[2] } }'
}
word2num() {
  printf '%s\n' "$1" | awk '{ w=tolower($0); split("one two three four five six seven eight nine ten eleven twelve", a, " "); for (i=1; i<=12; i++) if (a[i] == w) print i }'
}
superseded_at() {  # FILE AFTER_LINE SUBJECT_ERE VALUE_ERE -> first later R2[5-9]-E line carrying both
  awk -v a="$2" -v s="$3" -v v="$4" 'NR > a+0 && /R2[5-9]-E[0-9]/ && $0 ~ s && $0 ~ v { print NR; exit }' "$R/$1"
}
verdict() {  # ID LINE CLAIMED OBSERVED FILE SUBJECT_ERE VALUE_ERE DETAIL...
  _i=$1 _l=$2 _c=$3 _o=$4 _f=$5 _s=$6 _v=$7; shift 7
  if [ -n "$_c" ] && [ "$_c" = "$_o" ]; then emit MATCH "$_i" "$_l" "claimed=$_c observed=$_o $*"; return; fi
  if [ -n "$_s" ] && [ -n "$_o" ]; then
    _at=$(superseded_at "$_f" "$_l" "$_s" "$_v")
    if [ -n "$_at" ]; then emit SUPERSEDED "$_i" "$_l" "claimed=$_c observed=$_o correction=$_f:$_at $*"; return; fi
  fi
  emit MISMATCH "$_i" "$_l" "claimed=${_c:-<none>} observed=${_o:-<none>} $*"
}
numval() { printf '(^|[^0-9])%s([^0-9]|$)' "$1"; }
coverage() {  # ID LINE TEXT RULE... : each rule consumes one occurrence; residual digit-bearing tokens = unchecked
  _ci=$1 _cl=$2 _ct=$3; shift 3
  _rules=''
  for _r in "$@"; do _rules="$_rules$_r"'@@'; done
  _res=$(printf '%s\n' "$_ct" | awk -v rs="$_rules" '{
      n = split(rs, r, "@@"); miss = ""
      for (i = 1; i < n; i++) if (!sub(r[i], "#")) miss = miss " " r[i]
      m = split($0, t, /[ `|]+/); left = ""
      for (j = 1; j <= m; j++) if (t[j] ~ /[0-9]/) left = left " " t[j]
      printf "unchecked=[%s ] unmatched-rules=[%s ]", left, miss }')
  case $_res in
    'unchecked=[ ] unmatched-rules=[ ]') emit MATCH "$_ci" "$_cl" "every digit-bearing token is checked or classified ($# rules)" ;;
    *) emit MISMATCH "$_ci" "$_cl" "$_res" ;;
  esac
}
round_of() {  # CAPID ROWLINE -> N of the first "#.. Round N" section mentioning CAPID outside the capability row
  awk -v id="$1" -v row="$2" '
    /^#+ / { cur = ""; if (match($0, /^#+ Round [0-9]+/)) { h = substr($0, RSTART, RLENGTH); sub(/^#+ Round /, "", h); cur = h } }
    NR != row+0 && index($0, id) && cur != "" { print cur; exit }' "$R/SCORECARD.md"
}
exists_tok() { if [ -e "$R/$1" ]; then printf '%s' "$1"; fi; }

CENSUS=$(grep -cE '^\| *S[0-9]{3,} *\|' "$R/corpus/SOURCES.md")
printf '# p3_oracle root=%s sources_census=%s\n' "$R" "$CENSUS"

# ---------- P3a: capability rows vs v2 receipts ----------
SC=SCORECARD.md
L=$(lineno "$SC" '^[|] interval-reverdict [|]')
if [ -z "$L" ]; then emit MISMATCH P3a.interval-reverdict.row - "row absent or not unique in $SC"; else
  id=P3a.interval-reverdict; T=$(textat "$SC" "$L"); E=$(cell "$T" 3); D=$(cell "$T" 2)
  subj='interval-reverdict'
  o=$(field "$SUM" unique_samples); verdict $id.unique_samples "$L" "$(nums "$(grab "$E" 'unique_samples=[0-9]+')")" "$o" "$SC" "$subj" "unique_samples=$o([^0-9]|\$)" "receipt=$SUM"
  o=$(field "$SUM" scored_trials); verdict $id.scored_trials "$L" "$(nums "$(grab "$E" 'scored_trials=[0-9]+')")" "$o" "$SC" "$subj" "scored_trials=$o([^0-9]|\$)" "receipt=$SUM"
  o=$(field "$SUM" correct); verdict $id.correct "$L" "$(nums "$(grab "$E" ' correct=[0-9]+')")" "$o" "$SC" "$subj" " correct=$o([^0-9]|\$)" "receipt=$SUM"
  o=$(field "$SUM" transitions); c=$(grab "$E" 'transitions=[A-Z>:0-9,]+'); c=${c#transitions=}
  verdict $id.transitions "$L" "$c" "$o" "$SC" "$subj" "transitions=$o" "receipt=$SUM"
  o=$(field "$SUM" mismatches); verdict $id.mismatches "$L" "$(nums "$(grab "$E" 'mismatches=[0-9]+')")" "$o" "$SC" "$subj" "mismatches=$o([^0-9]|\$)" "receipt=$SUM"
  o=$(field "$SUM" exit); verdict $id.summary-exit "$L" "$(nums "$(grab "$E" 'exit [0-9]+')")" "$o" "$SC" "$subj" "exit $o([^0-9]|\$)" "receipt=$SUM"
  o=$(awk '/^selftest: [0-9]+ checks, [0-9]+ failed/{print $2; exit}' "$R/$SLF" 2>/dev/null)
  verdict $id.selftest-checks "$L" "$(nums "$(grab "$E" '[0-9]+ checks')")" "$o" "$SC" "$subj" "(^|[^0-9])$o checks" "receipt=$SLF"
  o=$(awk '/^selftest: [0-9]+ checks, [0-9]+ failed/{print $4; exit}' "$R/$SLF" 2>/dev/null)
  verdict $id.selftest-failed "$L" "$(nums "$(grab "$E" '[0-9]+ failed')")" "$o" "$SC" "$subj" "(^|[^0-9])$o failed" "receipt=$SLF"
  rr=$(nums "$(grab "$E" 'R[0-9]+–R[0-9]+')"); a=$(nth "$rr" 1); b=$(nth "$rr" 2); miss=''
  if [ -n "$a" ] && [ -n "$b" ]; then
    k=$a; while [ "$k" -le "$b" ]; do grep -qE "^selftest ok +R$k:" "$R/$SLF" 2>/dev/null || miss="$miss R$k"; k=$((k+1)); done
    c="R$a..R$b"; if [ -z "$miss" ]; then o=$c; else o="missing:$miss"; fi
  else c=''; o=''; fi
  verdict $id.red-runs "$L" "$c" "$o" "$SC" '' '' "receipt=$SLF (each label has a 'selftest ok' line)"
  c=$(grab "$E" 'corpus/evidence/round[0-9]+-calibration/'); verdict $id.receipts-dir "$L" "$c" "$(exists_tok "$c")" "$SC" '' '' "test -d"
  o=$(round_of interval-reverdict "$L"); verdict $id.round "$L" "$(cell "$T" 4)" "$o" "$SC" '' '' "first '## Round N' section of $SC naming the capability outside the row"
  if [ -n "$(grab "$D" 'CP95')" ] && grep -q 'cp95=\[' "$R/$SUM" 2>/dev/null; then o=CP95; else o=''; fi
  verdict $id.cp95 "$L" "$(grab "$D" 'CP95')" "$o" "$SC" '' '' "receipt=$SUM carries cp95=[lo,hi] intervals"
  if grep -qE '^selftest ok .*sha256 [0-9a-f]+ != frozen' "$R/$SLF" 2>/dev/null; then o=sha256-pinned; else o=''; fi
  verdict $id.sha256-pinned "$L" "$(grab "$D" 'sha256-pinned')" "$o" "$SC" '' '' "receipt=$SLF has a red run on a frozen sha256 pin"
  skip $id.python3 "$L" "interpreter name in the command"
  coverage $id.token-coverage "$L" "$T" 'CP95' 'sha256-pinned' 'python3' 'unique_samples=[0-9]+' 'scored_trials=[0-9]+' \
    ' correct=[0-9]+' 'transitions=[A-Z>:0-9,]+' 'mismatches=[0-9]+' 'exit [0-9]+' '[0-9]+ checks' '[0-9]+ failed' \
    'R[0-9]+–R[0-9]+' 'round[0-9]+-calibration' '[|] *[0-9]+ *[|] *$'
fi

L=$(lineno "$SC" '^[|] state-assertion-check [|]')
if [ -z "$L" ]; then emit MISMATCH P3a.state-assertion-check.row - "row absent or not unique in $SC"; else
  id=P3a.state-assertion-check; T=$(textat "$SC" "$L"); E=$(cell "$T" 3); D=$(cell "$T" 2)
  subj='state-assertion-check'
  S1=$(printf '%s\n' "$E" | awk -F';' '{print $1}'); S2=$(printf '%s\n' "$E" | awk -F';' '{print $2}'); S3=$(printf '%s\n' "$E" | awk -F';' '{print $3}')
  h=$(grab "$S1" 'base `[0-9a-f]+`'); h=${h#base \`}; h=${h%\`}
  SCB=$RC/state-check-before-$h-v2.txt
  if [ -n "$h" ] && [ -f "$R/$SCB" ]; then o=$h; else o=''; fi
  verdict $id.base-commit "$L" "$h" "$o" "$SC" '' '' "receipt=$SCB exists"
  o=$(field "$SCB" mismatch); verdict $id.base-mismatch "$L" "$(nums "$(grab "$S1" 'mismatch=[0-9]+')")" "$o" "$SC" "$subj" "mismatch=$o([^0-9]|\$)|(^|[^0-9])$o mismatch" "receipt=$SCB"
  o=$(field "$SCB" exit); verdict $id.base-exit "$L" "$(nums "$(grab "$S1" 'exit [0-9]+')")" "$o" "$SC" "$subj" "exit $o([^0-9]|\$)" "receipt=$SCB"
  o=$(field "$SCA" mismatch); verdict $id.landed-mismatch "$L" "$(nums "$(grab "$S2" 'mismatch=[0-9]+')")" "$o" "$SC" "$subj" "mismatch=$o([^0-9]|\$)" "receipt=$SCA"
  o=$(field "$SCA" superseded); verdict $id.landed-superseded "$L" "$(nums "$(grab "$S2" 'superseded=[0-9]+')")" "$o" "$SC" "$subj" "superseded=$o([^0-9]|\$)" "receipt=$SCA"
  o=$(field "$SCA" exit); verdict $id.landed-exit "$L" "$(nums "$(grab "$S2" 'exit [0-9]+')")" "$o" "$SC" "$subj" "exit $o([^0-9]|\$)" "receipt=$SCA"
  if grep -q 'ALL PASS' "$R/$SCS" 2>/dev/null && grep -qx 'exit=0' "$R/$SCS"; then o='ALL PASS'; else o=''; fi
  verdict $id.selftest "$L" "$(grab "$S3" 'ALL PASS')" "$o" "$SC" "$subj" 'ALL PASS' "receipt=$SCS (ALL PASS, exit=0)"
  for code in $(nums "$(grab "$D" 'exit [0-9]/[0-9]/[0-9]')"); do
    hit=''
    for rf in "$R/$RC"/state-check-*-v2.txt; do [ -f "$rf" ] && grep -qx "exit=$code" "$rf" && hit=${rf##*/} && break; done
    if [ -n "$hit" ]; then emit MATCH $id.exit-contract-$code "$L" "claimed exit $code exhibited by $RC/$hit"
    else emit UNVERIFIED $id.exit-contract-$code "$L" "claimed exit $code; no $RC/state-check-*-v2.txt receipt exhibits exit=$code"; fi
  done
  o=$(round_of state-assertion-check "$L"); verdict $id.round "$L" "$(cell "$T" 4)" "$o" "$SC" '' '' "first '## Round N' section of $SC naming the capability outside the row"
  skip $id.python3 "$L" "interpreter name in the command"
  coverage $id.token-coverage "$L" "$T" 'exit [0-9]/[0-9]/[0-9]' 'python3' 'base `[0-9a-f]+`' 'mismatch=[0-9]+' 'exit [0-9]+' \
    'mismatch=[0-9]+' 'superseded=[0-9]+' 'exit [0-9]+' '[|] *[0-9]+ *[|] *$'
fi

# ---------- P3b: PROVINCE §Province map rows vs SOURCES census + receipts ----------
PV=PROVINCE.md
L112=$(lineno "$PV" '^[|] Public-literature registry [|]')
C112=''
if [ -z "$L112" ]; then emit MISMATCH P3b.registry-row.row - "row absent or not unique in $PV"; else
  id=P3b.registry-row; T=$(textat "$PV" "$L112"); E=$(cell "$T" 3)
  C112=$(nums "$(grab "$E" '[0-9]+ rows')")
  rcpt=$(awk '/^rows: [0-9]+/{print $2; exit}' "$R/corpus/evidence/round24-census/after.txt" 2>/dev/null)
  verdict $id.rows "$L112" "$C112" "$CENSUS" "$PV" 'registry|SOURCES' "$(numval "$CENSUS")" "observed=SOURCES census at measured tree; cited receipt round24-census/after.txt rows=${rcpt:-<absent>}"
  c=$(grab "$E" 'corpus/evidence/round24-census/after[.]txt'); verdict $id.census-receipt "$L112" "$c" "$(exists_tok "$c")" "$PV" '' '' "test -e"
  c=$(grab "$E" 'corpus/evidence/round24-sources/gate[.]md'); verdict $id.gate-receipt "$L112" "$c" "$(exists_tok "$c")" "$PV" '' '' "test -e"
  skip $id.contract-v1 "$L112" "contract version label"
  coverage $id.token-coverage "$L112" "$T" '[0-9]+ rows' 'contract-v1' 'round24-census/after' 'round24-sources/gate'
fi

L=$(lineno "$PV" '^[|] Interval re-verdict instrument [(]round 25[)] [|]')
if [ -z "$L" ]; then emit MISMATCH P3b.interval-row.row - "row absent or not unique in $PV"; else
  id=P3b.interval-row; T=$(textat "$PV" "$L"); E=$(cell "$T" 3)
  subj='Interval re-verdict|interval-reverdict|attrib_calibration'
  ee=$(nums "$(grab "$E" 'exit [0-9]+ / exit [0-9]+')")
  o=$(field "$SUM" exit); verdict $id.summary-exit "$L" "$(nth "$ee" 1)" "$o" "$PV" "$subj" "exit $o" "receipt=$SUM"
  o=$(field "$SLF" exit); verdict $id.selftest-exit "$L" "$(nth "$ee" 2)" "$o" "$PV" "$subj" "exit $o" "receipt=$SLF"
  o=$(field "$SUM" unique_samples); verdict $id.unique-samples "$L" "$(nums "$(grab "$E" '[0-9]+ unique samples')")" "$o" "$PV" "$subj" "$(numval "$o") unique" "receipt=$SUM"
  cc=$(nums "$(grab "$E" '[0-9]+/[0-9]+ correct')"); o="$(field "$SUM" correct)/$(field "$SUM" scored_trials)"
  verdict $id.correct "$L" "$(nth "$cc" 1)/$(nth "$cc" 2)" "$o" "$PV" "$subj" "$o" "receipt=$SUM correct/scored_trials"
  tt=$(field "$SUM" transitions)
  o=$(trans "$tt" 'FAIL>UNTESTED'); verdict $id.fail-untested "$L" "$(nums "$(grab "$E" 'FAIL>UNTESTED [0-9]+')")" "$o" "$PV" "$subj" "FAIL>UNTESTED:? $o" "receipt=$SUM transitions"
  o=$(trans "$tt" 'PASS>INDETERMINATE'); verdict $id.pass-indeterminate "$L" "$(nums "$(grab "$E" 'PASS>INDETERMINATE [0-9]+')")" "$o" "$PV" "$subj" "PASS>INDETERMINATE:? $o" "receipt=$SUM transitions"
  if grep -qE '^selftest ok .*sha256 [0-9a-f]+ != frozen' "$R/$SLF" 2>/dev/null; then o=sha256-pinned; else o=''; fi
  verdict $id.sha256-pinned "$L" "$(grab "$E" 'sha256-pinned')" "$o" "$PV" '' '' "receipt=$SLF has a red run on a frozen sha256 pin"
  o=$(round_of interval-reverdict 0); verdict $id.round "$L" "$(nums "$(grab "$T" '[(]round [0-9]+[)]')")" "$o" "$PV" '' '' "first '## Round N' section of SCORECARD.md naming interval-reverdict"
  skip $id.P1 "$L" "population label"; skip $id.python3 "$L" "interpreter name in the command"
  coverage $id.token-coverage "$L" "$T" '[(]round [0-9]+[)]' 'python3' 'exit [0-9]+ / exit [0-9]+' 'P1' 'sha256-pinned' \
    '[0-9]+ unique samples' '[0-9]+/[0-9]+ correct' 'FAIL>UNTESTED [0-9]+' 'PASS>INDETERMINATE [0-9]+'
fi

L=$(lineno "$PV" '^[|] State-assertion check [(]round 25[)] [|]')
if [ -z "$L" ]; then emit MISMATCH P3b.state-check-row.row - "row absent or not unique in $PV"; else
  id=P3b.state-check-row; T=$(textat "$PV" "$L"); E=$(cell "$T" 3)
  subj='State-assertion|state-assertion-check|state_check'
  ee=$(nums "$(grab "$E" 'exit [0-9]+ / exit [0-9]+')")
  o=$(field "$SCA" exit); verdict $id.landed-summary-exit "$L" "$(nth "$ee" 1)" "$o" "$PV" "$subj" "exit $o" "receipt=$SCA"
  o=$(field "$SCS" exit); verdict $id.selftest-exit "$L" "$(nth "$ee" 2)" "$o" "$PV" "$subj" "exit $o" "receipt=$SCS"
  h=$(grab "$E" 'base `[0-9a-f]+`'); h=${h#base \`}; h=${h%\`}; B=$RC/state-check-before-$h-v2.txt
  if [ -n "$h" ] && [ -f "$R/$B" ]; then o=$h; else o=''; fi
  verdict $id.base-commit "$L" "$h" "$o" "$PV" '' '' "receipt=$B exists"
  bb=$(nums "$(grab "$E" 'exit [0-9]+, [0-9]+ mismatches')")
  o=$(field "$B" exit); verdict $id.base-exit "$L" "$(nth "$bb" 1)" "$o" "$PV" "$subj" "exit $o" "receipt=$B"
  o=$(field "$B" mismatch); verdict $id.base-mismatch "$L" "$(nth "$bb" 2)" "$o" "$PV" "$subj" "$(numval "$o") mismatch|mismatch=$o([^0-9]|\$)" "receipt=$B"
  o=$(round_of state-assertion-check 0); verdict $id.round "$L" "$(nums "$(grab "$T" '[(]round [0-9]+[)]')")" "$o" "$PV" '' '' "first '## Round N' section of SCORECARD.md naming state-assertion-check"
  skip $id.python3 "$L" "interpreter name in the command"
  coverage $id.token-coverage "$L" "$T" '[(]round [0-9]+[)]' 'python3' 'exit [0-9]+ / exit [0-9]+' 'base `[0-9a-f]+`' 'exit [0-9]+, [0-9]+ mismatches'
fi

L=$(lineno "$PV" '^[*]Round-25 correction [(]appended')
if [ -z "$L" ]; then emit MISMATCH P3b.round25-correction.row - "line absent or not unique in $PV"; else
  id=P3b.round25-correction; T=$(textat "$PV" "$L")
  verdict $id.quoted-rows "$L" "$(nums "$(grab "$T" 'says [0-9]+ rows')")" "$C112" "$PV" '' '' "observed=the registry row's own rows token (:${L112:-?})"
  o=$(field "$CB" sources_rows); hb=$(nums "$(grab "$T" 'held [0-9]+ at base')")
  verdict $id.base-rows "$L" "$hb" "$o" "$PV" 'registry|SOURCES' "$(numval "$o")" "receipt=$CB sources_rows"
  o=$(grep -oE '^\| *S[0-9]{3,} *\|' "$R/corpus/SOURCES.md" | awk -v k="${o:-0}" 'NR == k+0 { gsub(/[| ]/, ""); print; exit }')
  c=$(grab "$T" '[(]S[0-9]+,'); c=${c#(}; c=${c%,}
  verdict $id.base-last-id "$L" "$c" "$o" "$PV" '' '' "observed=id of SOURCES row number <receipt base rows> at measured tree"
  ra=$(field "$CA" sources_rows)
  verdict $id.after-r25-rows "$L" "$(nums "$(grab "$T" 'holds [0-9]+ after round')")" "$CENSUS" "$PV" 'registry|SOURCES' "$(numval "$CENSUS")" "observed=SOURCES census at measured tree; receipt $CA sources_rows=${ra:-<absent>}"
  w=$(grab "$T" '[A-Za-z]+ `## Surfaces` rows'); w=${w%% *}
  o=$(awk '/^## /{ins = ($0 ~ /^## Surfaces/)} ins && /^[|]/ && /ABSENT [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/ {c++} END{print c+0}' "$R/$PV")
  verdict $id.absent-markers "$L" "$(word2num "$w")" "$o" "$PV" 'ABSENT' "$(numval "$o")" "claimed word '$w'; observed=## Surfaces table rows carrying 'ABSENT YYYY-MM-DD'"
  q=$(grab "$T" 'QUALITY R[0-9]+'); q=${q#QUALITY }
  if [ -n "$q" ] && grep -qE "^- [*][*]$q — " "$R/corpus/QUALITY.md" 2>/dev/null; then o=$q; else o=''; fi
  verdict $id.quality-criterion "$L" "$q" "$o" "$PV" '' '' "corpus/QUALITY.md defines criterion $q"
  skip $id.label "$L" "'Round-25' label"; skip $id.date "$L" "append date (tree-only oracle: no commit dates)"
  skip $id.commit "$L" "commit id $(grab "$T" '`[0-9a-f]+`') (tree-only oracle: no object store)"
  skip $id.round-label "$L" "'after round 25' label"; skip $id.command "$L" "census command text (it is the oracle's own observable)"
  coverage $id.token-coverage "$L" "$T" 'Round-25' '[0-9]+-[0-9]+-[0-9]+' 'says [0-9]+ rows' 'held [0-9]+ at base' '[(]S[0-9]+,' \
    '`[0-9a-f]+`' 'holds [0-9]+ after round [0-9]+' 'grep -cE [^`]*' 'QUALITY R[0-9]+'
fi

# ---------- P3e: out-of-population README rows and entries, both directions ----------
RM=corpus/README.md
rowline() { awk -v p="$1" 'index($0, "| `" p "` |") == 1 { print NR; exit }' "$R/$RM"; }
for p in $P3E_ROWS; do
  l=$(rowline "$p")
  if [ -z "$l" ]; then emit MISMATCH "P3e.row.$p" - "index row absent from $RM"
  elif [ -e "$R/corpus/$p" ]; then emit MATCH "P3e.row.$p" "$l" "row -> corpus/$p exists"
  else emit MISMATCH "P3e.row.$p" "$l" "row -> corpus/$p missing"; fi
done
for p in $P3E_FILES; do
  l=$(rowline "$p")
  if [ ! -e "$R/corpus/$p" ]; then emit MISMATCH "P3e.file.$p" - "corpus/$p absent"
  elif [ -n "$l" ]; then emit MATCH "P3e.file.$p" "$l" "corpus/$p -> index row $RM:$l"
  else emit MISMATCH "P3e.file.$p" - "corpus/$p exists, no $RM index row"; fi
done

# ---------- X: oracle-only extension — numeric tokens inside the P3e rows (not in totals / exit) ----------
l=$(rowline evidence/round25-sources/)
if [ -n "$l" ]; then
  T=$(textat "$RM" "$l"); sr=$(nums "$(grab "$T" 'S[0-9]+–S[0-9]+')"); lo=$(nth "$sr" 1); hi=$(nth "$sr" 2)
  mx=$(grep -oE '^[|] *S[0-9]+ *[|]' "$R/corpus/evidence/round25-sources/gate.md" 2>/dev/null | awk '{ gsub(/[^0-9]/, ""); n = $0 + 0; if (n > m) m = n } END { printf "%03d", m }')
  verdict X.readme.round25-sources.s-range "$l" "S$lo-S$hi" "S$lo-S$mx" "$RM" '' '' "observed=highest row-key S id in corpus/evidence/round25-sources/gate.md"
fi
l=$(rowline lessons/round-25.md)
if [ -n "$l" ]; then
  T=$(textat "$RM" "$l")
  for k in M F; do
    cr=$(nums "$(grab "$T" "$k[0-9]+–$k[0-9]+")")
    if [ $k = M ]; then pat='^[|] *M[0-9]+ *[|]'; else pat='^[|] F[0-9]+ '; fi
    o=$(grep -oE "$pat" "$R/corpus/lessons/round-25.md" 2>/dev/null | awk -v k=$k '{ gsub(/[^0-9]/, ""); n = $0 + 0; if (mn == "" || n < mn) mn = n; if (n > mx) mx = n } END { if (mn != "") print k mn "-" k mx }')
    verdict X.readme.round25-lesson.$k-range "$l" "$k$(nth "$cr" 1)-$k$(nth "$cr" 2)" "$o" "$RM" '' '' "observed=min-max $k table ids in corpus/lessons/round-25.md"
  done
fi
l=$(rowline knowledge/attribution-interval-calibration.md)
if [ -n "$l" ]; then
  T=$(textat "$RM" "$l"); id=X.readme.attribution-entry
  verdict $id.unique-samples "$l" "$(nums "$(grab "$T" 'on [0-9]+ unique samples')")" "$(field "$SUM" unique_samples)" "$RM" '' '' "receipt=$SUM"
  cc=$(nums "$(grab "$T" '[(][0-9]+/[0-9]+[)]')")
  verdict $id.correct "$l" "$(nth "$cc" 1)/$(nth "$cc" 2)" "$(field "$SUM" correct)/$(field "$SUM" scored_trials)" "$RM" '' '' "receipt=$SUM"
  c=$(grab "$T" 'TARGET hyper [0-9]+/[0-9]+ PASS → INDETERMINATE'); c=${c#TARGET hyper }; c=$(printf '%s' "$c" | awk '{print $1 " " $2 ">" $4}')
  o=$(awk '/ target:hyper / { for (i = 1; i <= NF; i++) { if ($i ~ /^[0-9]+\/[0-9]+$/) f = $i; if ($i ~ /^stored=/) s = substr($i, 8); if ($i ~ /^interval=/) v = substr($i, 10) } print f " " s ">" v; exit }' "$R/$SUM" 2>/dev/null)
  verdict $id.target-hyper "$l" "$c" "$o" "$RM" '' '' "receipt=$SUM target:hyper line"
  w=$(grab "$T" '[a-z]+ 0/0 FAILs'); w=${w%% *}
  o=$(grep -cE ' 0/0 .*stored=FAIL interval=UNTESTED' "$R/$SUM" 2>/dev/null)
  verdict $id.fail-untested "$l" "$(word2num "$w")" "$o" "$RM" '' '' "claimed word '$w'; receipt=$SUM 0/0 stored=FAIL interval=UNTESTED lines"
fi
l=$(rowline evidence/round25-calibration/)
if [ -n "$l" ]; then
  T=$(textat "$RM" "$l"); pats=$(printf '%s\n' "$T" | awk '{ s = $0; while (match(s, /`[^`]*[.]txt`/)) { t = substr(s, RSTART+1, RLENGTH-2); if (t ~ /^-/) t = "*" t; print t; s = substr(s, RSTART+RLENGTH) } }')
  dead=''; uncov=''
  set -f
  for pt in $pats; do
    m=0; set +f
    for f in "$R/$RC"/*; do b=${f##*/}; case $b in $pt) m=1 ;; esac; done
    set -f; [ $m = 1 ] || dead="$dead $pt"
  done
  set +f
  for f in "$R/$RC"/*; do
    b=${f##*/}; m=0; set -f
    for pt in $pats; do case $b in $pt) m=1 ;; esac; done
    set +f; [ $m = 1 ] || uncov="$uncov $b"
  done
  if [ -z "$dead$uncov" ]; then emit MATCH X.readme.round25-calibration.contents "$l" "every named file/glob resolves and every file in $RC is named"
  else emit MISMATCH X.readme.round25-calibration.contents "$l" "unresolved=[$dead ] unnamed=[$uncov ]"; fi
fi

printf 'TOTAL assertions=%s match=%s mismatch=%s superseded=%s unverified=%s skipped_tokens=%s extension_match=%s extension_mismatch=%s\n' \
  "$N" "$NM" "$NX" "$NS" "$NU" "$NK" "$XM" "$XX"
if [ "$MODE" = run ]; then
  if [ "$NX" -eq 0 ]; then echo "VERDICT: PASS — no registered P3a/P3b/P3e assertion mismatches"; exit 0; fi
  echo "VERDICT: FAIL — $NX registered P3a/P3b/P3e assertion(s) mismatch"; exit 1
fi

# ---------- --selftest: mutation red/green checks on scratch copies ----------
echo "# selftest on scratch copies of $R"
TMPROOT=${TMPDIR:-/tmp}/p3_oracle_selftest.$$
rm -rf "$TMPROOT"; mkdir -p "$TMPROOT/tpl" || exit 2
trap 'rm -rf "$TMPROOT"' EXIT
for f in SCORECARD.md PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/QUALITY.md \
  corpus/evidence/round24-census/after.txt corpus/evidence/round24-sources/gate.md corpus/evidence/round25-sources/gate.md \
  corpus/knowledge/attribution-interval-calibration.md corpus/lessons/round-24-verifier-spotcheck.md \
  corpus/lessons/round-25.md corpus/lessons/round-25-verifier-spotcheck.md; do
  [ -e "$R/$f" ] || continue
  case $f in */*) mkdir -p "$TMPROOT/tpl/${f%/*}" ;; esac
  cp "$R/$f" "$TMPROOT/tpl/$f"
done
mkdir -p "$TMPROOT/tpl/$RC"; cp "$R/$RC"/* "$TMPROOT/tpl/$RC/"
ck=$(awk '/^selftest: [0-9]+ checks/{print $2; exit}' "$R/$SLF"); bm=$(field "$RC/state-check-before-6180e4f-v2.txt" mismatch)
green() {  # DIR: append R26-E corrections carrying re-derived values + the missing P3e index row
  printf '%s\n' "- **R26-E1 (selftest)** supersedes \`interval-reverdict\` — now \`--selftest\` $ck checks 0 failed" \
    "- **R26-E2 (selftest)** supersedes \`state-assertion-check\` — now base \`mismatch=$bm\` exit 1" >> "$1/SCORECARD.md"
  printf '%s\n' "*R26-E3 (selftest): the Public-literature registry holds $CENSUS rows.*" >> "$1/PROVINCE.md"
  grep -q '^| `lessons/round-25-verifier-spotcheck.md` |' "$1/corpus/README.md" || \
    printf '%s\n' '| `lessons/round-25-verifier-spotcheck.md` | selftest row | - |' >> "$1/corpus/README.md"
}
mut() { awk "$2" "$1" > "$1.tmp" && mv "$1.tmp" "$1"; }
ST=0 SF=0
expect() {  # NAME DIR WANT_EXIT STATUS:ID...
  _n=$1 _d=$2 _w=$3; shift 3
  _out=$(sh "$SELF" "$_d" 2>&1); _e=$?; _bad=''
  [ "$_e" = "$_w" ] || _bad="exit=$_e want $_w"
  for _x in "$@"; do
    _s=${_x%%:*}; _k=${_x#*:}
    printf '%s\n' "$_out" | awk -v s="$_s" -v k="$_k" 'index($0, s ": " k ":") == 1 { f = 1 } END { exit !f }' || _bad="$_bad; no $_s for $_k"
  done
  ST=$((ST+1))
  if [ -z "$_bad" ]; then echo "selftest ok   $_n"; else SF=$((SF+1)); echo "selftest FAIL $_n — $_bad"; fi
}
fresh() { rm -rf "$TMPROOT/$1"; cp -R "$TMPROOT/tpl" "$TMPROOT/$1"; printf '%s' "$TMPROOT/$1"; }

d=$(fresh g1); green "$d"
expect G1-green-after-corrections "$d" 0 SUPERSEDED:P3a.interval-reverdict.selftest-checks SUPERSEDED:P3a.state-assertion-check.base-mismatch \
  SUPERSEDED:P3b.registry-row.rows SUPERSEDED:P3b.round25-correction.after-r25-rows MATCH:P3e.file.lessons/round-25-verifier-spotcheck.md
d=$(fresh r1); green "$d"; mut "$d/$SLF" '/^selftest: [0-9]+ checks/{ $2 = $2 + 1 } { print }'
expect R1-selftest-count-drift "$d" 1 MISMATCH:P3a.interval-reverdict.selftest-checks
d=$(fresh r2); green "$d"; mut "$d/$SCA" '{ sub(/superseded=1 /, "superseded=2 "); print }'
expect R2-landed-superseded-drift "$d" 1 MISMATCH:P3a.state-assertion-check.landed-superseded
d=$(fresh r3); green "$d"; printf '| S999 | selftest | - |\n' >> "$d/corpus/SOURCES.md"
expect R3-registry-grows "$d" 1 MISMATCH:P3b.registry-row.rows MISMATCH:P3b.round25-correction.after-r25-rows
d=$(fresh r4); green "$d"; mut "$d/PROVINCE.md" '!done && /^[|]/ && /ABSENT 2026-10-20/ { sub(/ABSENT 2026-10-20/, "absent"); done = 1 } { print }'
expect R4-absent-marker-dropped "$d" 1 MISMATCH:P3b.round25-correction.absent-markers
d=$(fresh r5); green "$d"; mut "$d/$RC/state-check-before-6180e4f-v2.txt" '{ sub(/ mismatch=10 /, " mismatch=9 "); print }'
expect R5-base-receipt-drift "$d" 1 MISMATCH:P3b.state-check-row.base-mismatch MISMATCH:P3a.state-assertion-check.base-mismatch
d=$(fresh r6); green "$d"; rm -f "$d/corpus/knowledge/attribution-interval-calibration.md"
expect R6-row-to-missing-entry "$d" 1 MISMATCH:P3e.row.knowledge/attribution-interval-calibration.md MISMATCH:P3e.file.knowledge/attribution-interval-calibration.md
d=$(fresh r7); green "$d"; mut "$d/corpus/README.md" 'index($0, "| `lessons/round-25.md` |") != 1 { print }'
expect R7-entry-without-row "$d" 1 MISMATCH:P3e.file.lessons/round-25.md MISMATCH:P3e.row.lessons/round-25.md
d=$(fresh r8)
awk -v l="- **R26-E1 (selftest)** supersedes \`interval-reverdict\` — now \`--selftest\` $ck checks 0 failed" 'NR == 1 { print l } { print }' \
  "$d/SCORECARD.md" > "$d/x" && mv "$d/x" "$d/SCORECARD.md"
expect R8-correction-above-not-appended "$d" 1 MISMATCH:P3a.interval-reverdict.selftest-checks
d=$(fresh r9); printf '%s\n' '- **R26-E1 (selftest)** supersedes `interval-reverdict` — `--selftest` 14 checks' >> "$d/SCORECARD.md"
expect R9-correction-with-stale-value "$d" 1 MISMATCH:P3a.interval-reverdict.selftest-checks
d=$(fresh r10); printf '%s\n' "- **R24-E9 (selftest)** supersedes \`interval-reverdict\` — now \`--selftest\` $ck checks" >> "$d/SCORECARD.md"
expect R10-id-outside-R25-to-R29 "$d" 1 MISMATCH:P3a.interval-reverdict.selftest-checks
d=$(fresh r11); green "$d"; mut "$d/SCORECARD.md" '/^[|] interval-reverdict [|]/ { sub(/ 0 failed/, " 0 failed, 7 widgets") } { print }'
expect R11-unchecked-token "$d" 1 MISMATCH:P3a.interval-reverdict.token-coverage
d=$(fresh r12); green "$d"; printf '%s\n' 'unindexed' > "$d/$RC/extra-unnamed.txt"
expect R12-extension-red-registered-green "$d" 0 MISMATCH:X.readme.round25-calibration.contents
echo "selftest: $ST checks, $SF failed"
[ "$SF" -eq 0 ] || exit 1
exit 0

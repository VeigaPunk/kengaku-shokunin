#!/bin/sh
# kengaku round-25 census — run from the lane root: sh plans/round25_census.sh
# Read-only: reads the working tree, prints one key=value line per key and writes
# nothing (python runs with PYTHONDONTWRITEBYTECODE=1). Base keys: run it in a
# checkout of 3f371d2, or export the base and run it there (head prints n/a):
#   mkdir -p /tmp/k25base && git archive 3f371d2 | tar -x -C /tmp/k25base
#   (cd /tmp/k25base && sh /path/to/plans/round25_census.sh)
# Exit 0 = census printed; 2 = usage (any argument, or cwd lacks SKILL.md/corpus/).
# A key prints `absent` when its input file is missing.
#
#   head                           short HEAD when cwd is a git toplevel, else n/a
#   sources_rows, sources_malformed, sources_tier_histogram, sources_status_histogram
#                                  CORPUS.md SOURCES contract-v1 census commands, verbatim;
#                                  histogram tokens are sorted (C locale) for a stable line
#   sources_new_rows_r25           well-formed (NF==13) rows whose `opened` cell is 2026-10-20
#   knowledge_files                regular files matching corpus/knowledge/*.md
#   lesson_mistake_rows_r25        `^\| M` lines inside the `^## Mistakes$` section (up to
#                                  the next `^## `) of corpus/lessons/round-25.md
#   shonen_evidence_lines_per_box  one count per `- [?]` box in SHONEN.md, comma-joined:
#                                  non-blank indented lines before the next box or
#                                  unindented line (`none` = no boxes)
#   skill_frontmatter_triggers     quoted strings in the SKILL.md frontmatter `description`
#                                  value after YAML unquoting (rules at the awk below)
#   calib_summary, calib_exit      the TOTAL line and exit status of
#                                  python3 plans/attrib_calibration.py --summary
#   state_check_summary, state_check_exit
#                                  the assertions= line and exit status of python3 plans/state_check.py --summary
#   Limits (round-25 falsify RevCensusScript): shonen_evidence_lines_per_box counts lines, not
#   pointer-only form (state_check P2c checks the form); skill_frontmatter_triggers counts quoted
#   strings even when the frontmatter is not valid YAML (parse it separately to show validity).
set -u

if [ "$#" -ne 0 ]; then
  echo "usage: sh plans/round25_census.sh   (no arguments; run from the lane root)" >&2
  exit 2
fi
if [ ! -f SKILL.md ] || [ ! -d corpus ]; then
  echo "round25_census: cwd is not a lane root (needs SKILL.md and corpus/)" >&2
  exit 2
fi

R25_OPENED=2026-10-20
SRC=corpus/SOURCES.md
L25=corpus/lessons/round-25.md

kv() { printf '%s=%s\n' "$1" "$2"; }
sorted() { tr ' ' '\n' | sed '/^$/d' | LC_ALL=C sort | paste -s -d ' ' -; }

# --- provenance: never report an enclosing repository's HEAD ------------------
top=$(git rev-parse --show-toplevel 2>/dev/null) || top=
if [ -n "$top" ] && [ "$(cd "$top" && pwd -P)" = "$(pwd -P)" ]; then
  kv head "$(git rev-parse --short HEAD 2>/dev/null || echo n/a)"
else
  kv head n/a
fi

# --- SOURCES registry (CORPUS.md §Census, contract v1) ------------------------
if [ -f "$SRC" ]; then
  kv sources_rows "$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$SRC")"
  kv sources_malformed "$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' "$SRC")"
  kv sources_tier_histogram "$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' "$SRC" | sorted)"
  kv sources_status_histogram "$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' "$SRC" | sorted)"
  # `opened` is $10; NF==13 keeps a shifted (malformed) row from being read at the wrong column
  kv sources_new_rows_r25 "$(awk -F'|' -v d="$R25_OPENED" '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {o=$10; gsub(/[[:space:]]/,"",o); if (o==d) n++} END{print n+0}' "$SRC")"
else
  for k in sources_rows sources_malformed sources_tier_histogram sources_status_histogram sources_new_rows_r25; do
    kv "$k" absent
  done
fi

# --- corpus files ---------------------------------------------------------------
if [ -d corpus/knowledge ]; then
  n=0
  for f in corpus/knowledge/*.md; do [ -f "$f" ] && n=$((n + 1)); done
  kv knowledge_files "$n"
else
  kv knowledge_files absent
fi
if [ -f "$L25" ]; then
  # heading anchored with $ (round-24 M20: a prefix match is not a count)
  kv lesson_mistake_rows_r25 "$(awk '/^## Mistakes$/{f=1;next} /^## /{f=0} f&&/^\| M/{c++} END{print c+0}' "$L25")"
else
  kv lesson_mistake_rows_r25 absent
fi

# --- SHONEN.md: evidence lines under each box (canonical form: exactly 1) --------
if [ -f SHONEN.md ]; then
  kv shonen_evidence_lines_per_box "$(awk '
    /^- \[[^]]*\]/ { n++; c[n] = 0; box = 1; next }
    box && /^[ \t]*$/ { next }
    box && /^[ \t]/ { c[n]++; next }
    { box = 0 }
    END {
      if (!n) { print "none"; exit }
      s = c[1]; for (i = 2; i <= n; i++) s = s "," c[i]; print s
    }' SHONEN.md)"
else
  kv shonen_evidence_lines_per_box absent
fi

# --- SKILL.md frontmatter description: quoted trigger strings --------------------
# The value is read from the line-1 `---` frontmatter: the text after `description:`
# plus its indented continuation lines, joined by single spaces. YAML scalar style
# is undone first, so the quotes of a quoted scalar are never counted:
#   `>`/`|` block: continuation lines only; "...": up to the closing unescaped
#   quote, \x keeps x; '...': up to the closing quote, '' keeps one quote;
#   plain: cut at the first blank-then-# comment.
# Counted in the value: "..." pairs, curly double and single pairs (normalized to
# ASCII first), and '...' pairs whose opening quote follows a non-word character
# and whose closing quote precedes one (word = ASCII letter, digit, underscore),
# so apostrophes never pair. Prints `absent` when no description key exists.
if [ -f SKILL.md ]; then
  ldq=$(printf '\342\200\234'); rdq=$(printf '\342\200\235')
  lsq=$(printf '\342\200\230'); rsq=$(printf '\342\200\231')
  kv skill_frontmatter_triggers "$(LC_ALL=C awk -v dq='"' -v sq="'" \
      -v ldq="$ldq" -v rdq="$rdq" -v lsq="$lsq" -v rsq="$rsq" '
    function word(ch) { return ch ~ /^[A-Za-z0-9_]$/ }
    function unquote(v, r,    c, s, n, i, ch, out) {
      c = substr(v, 1, 1)
      if (c == ">" || c == "|") return r
      if (c == dq || c == sq) {
        s = substr(v, 2) (r == "" ? "" : " " r); n = length(s); out = ""
        for (i = 1; i <= n; i++) {
          ch = substr(s, i, 1)
          if (c == dq && ch == "\\") { i++; out = out substr(s, i, 1); continue }
          if (ch == c) {
            if (c == sq && substr(s, i + 1, 1) == sq) { out = out sq; i++; continue }
            break
          }
          out = out ch
        }
        return out
      }
      s = v (r == "" ? "" : " " r)
      if (match(s, /[ \t]#/)) s = substr(s, 1, RSTART - 1)
      return s
    }
    function count_quoted(s,    n, i, j, ch, cnt) {
      if (ldq != "") { gsub(ldq, dq, s); gsub(rdq, dq, s); gsub(lsq, sq, s); gsub(rsq, sq, s) }
      n = length(s); cnt = 0
      for (i = 1; i <= n; i++) {
        ch = substr(s, i, 1)
        if (ch == dq) {
          j = index(substr(s, i + 1), dq)
          if (j) { cnt++; i += j }
          continue
        }
        if (ch == sq && (i == 1 || !word(substr(s, i - 1, 1)))) {
          for (j = i + 1; j <= n; j++)
            if (substr(s, j, 1) == sq && (j == n || !word(substr(s, j + 1, 1)))) break
          if (j <= n) { cnt++; i = j }
        }
      }
      return cnt
    }
    NR == 1 { if ($0 != "---") exit; next }
    $0 == "---" || $0 == "..." { exit }
    desc && /^[ \t]*$/ { next }
    desc && /^[ \t]/ {
      line = $0; sub(/^[ \t]+/, "", line); sub(/[ \t]+$/, "", line)
      rest = (rest == "" ? line : rest " " line); next
    }
    { desc = 0 }
    /^description:/ {
      found = 1; desc = 1
      first = substr($0, 13); sub(/^[ \t]+/, "", first); sub(/[ \t]+$/, "", first)
    }
    END {
      if (!found) { print "absent"; exit }
      if (first == "") { first = rest; rest = "" }
      print count_quoted(unquote(first, rest))
    }' SKILL.md)"
else
  kv skill_frontmatter_triggers absent
fi

# --- round-25 instruments (offline; exit status is part of their verdict) -------
summary() { # $1 = key prefix, $2 = script path
  if [ -f "$2" ]; then
    out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$2" --summary); rc=$?
    # the line carrying the counts: TOTAL (attrib_calibration) or assertions= (state_check)
    kv "${1}_summary" "$(printf '%s\n' "$out" | awk '/^(TOTAL |assertions=)/{l=$0} END{print l}')"
    kv "${1}_exit" "$rc"
  else
    kv "${1}_summary" absent
    kv "${1}_exit" absent
  fi
}
summary calib plans/attrib_calibration.py
summary state_check plans/state_check.py
exit 0

#!/bin/sh
# kengaku round-25 L0 filing check — run from the lane root:
#   sh plans/l0_filed_check.sh <report.md> <l0-questions.md>
# Extracts every `kengaku | round-<N> | <question>` entry from the report's `## L0 questions`
# section(s) and checks that each one is present in the fleet L0 queue file.
# Key: the first 60 characters of the question text after the round tag, taken after undoing the
# report's line wrapping (continuation lines joined, whitespace runs -> one space, trailing space
# dropped). Filed: `kengaku | round-<N> | <key>` occurs in the queue after the same normalisation
# (queue lines are joined too, so a wrapped or annotated queue line still matches). Lane and round
# are part of the identity (PROTOCOL.md L0 side channel: "Cite a question by lane + round + its
# opening words"); opening words found only without that anchor are shown, never counted as filed.
# Output: one FILED/UNFILED line per question with report:<line> (queue:<line> where found), then
# `l0_filed_check: sections=<s> questions=<n> filed=<f> unfiled=<u>`.
# Exit: 0 every question filed (a section that lists none counts); 1 at least one unfiled;
# 2 usage, unreadable file, or no `## L0 questions` section (nothing to evaluate).
# Offline: reads only the two named files; writes nothing.
usage() { echo "usage: sh plans/l0_filed_check.sh <report.md> <l0-questions.md>" >&2; exit 2; }
[ "$#" -eq 2 ] || usage
for f in "$1" "$2"; do
  [ -r "$f" ] && [ ! -d "$f" ] || { echo "l0_filed_check: not a readable file: $f" >&2; exit 2; }
done
# Paths go through the environment (awk -v would rewrite backslashes); C.UTF-8 makes the 60-character
# cut count characters. Without that locale awk counts bytes, which still matches byte-identically.
L0_REPORT=$1 L0_QUEUE=$2 LC_ALL=C.UTF-8 awk '
function norm(s) { gsub(/[[:space:]]+/, " ", s); sub(/^ /, "", s); sub(/ $/, "", s); return s }
function pipes(s) { gsub(/ ?[|] ?/, " | ", s); return s }
function anchorable(k) { k = pipes(k); sub(/ $/, "", k); return k }
function qline(p,   i) { for (i = nq; i > 1 && qoff[i] > p; i--) ; return i }
# first occurrence of a in s that starts a queue row: only an optional list marker or backtick may
# precede it on its line (round-25 falsify RevL0Check: a prose mention inside a line must not count)
function anchored(s, a,   p, q, li, pre) {
  for (q = 0; (p = index(substr(s, q + 1), a)) > 0; ) {
    q += p
    li = qline(q); pre = substr(s, qoff[li], q - qoff[li])
    if (pre ~ /^((([-*+]|[0-9]+[.)]) )?`?)$/) return q
  }
  return 0
}
function close_entry(   t, k) {
  if (!cur) return
  t = norm(buf); if (bt) sub(/`$/, "", t)
  k = substr(t, 1, KEYLEN); sub(/ $/, "", k)
  n++; eln[n] = cur; etag[n] = tag; ekey[n] = k
  cur = 0
}
BEGIN {
  KEYLEN = 60
  ENTRY = "^[ \t]*(([-*+]|[0-9]+[.)])[ \t]+)?`?kengaku[ \t]*[|][ \t]*round-[0-9]+[ \t]*[|]"
  rp = ENVIRON["L0_REPORT"]; qp = ENVIRON["L0_QUEUE"]

  # Queue: one normalised stream; qoff[i] is where queue line i starts in it. A blank line leaves a
  # double space, so no match can span two blank-separated blocks.
  S = ""; off = 1
  while ((rc = (getline l < qp)) > 0) {
    l = pipes(norm(l)); nq++; qoff[nq] = off
    S = S l " "; off += length(l) + 1
  }
  if (rc < 0) { print "l0_filed_check: cannot read " qp > "/dev/stderr"; exit 2 }
  close(qp)

  # Report: entries start with an optional list marker or backtick, then the kengaku round tag;
  # indented or lazy continuation lines join the entry; a blank line, heading, code fence or the
  # next list item closes it. An h1/h2 heading ends the section.
  while ((rc = (getline l < rp)) > 0) {
    ln++; sub(/\r$/, "", l)
    if (l ~ /^##?[ \t]/) {
      close_entry()
      insec = (tolower(l) ~ /^##[ \t].*l0[ \t]+questions/)
      nsec += insec
      continue
    }
    if (l ~ ENTRY) {
      if (!insec) { outside = outside (nout++ ? "," : "") ln; continue }
      close_entry()
      cur = ln; bt = (l ~ /^[ \t]*(([-*+]|[0-9]+[.)])[ \t]+)?`/)
      match(l, /round-[0-9]+/); tag = substr(l, RSTART, RLENGTH)
      buf = substr(l, RSTART + RLENGTH); sub(/^[ \t]*[|]/, "", buf)
      continue
    }
    if (!insec) continue
    if (l ~ /^[ \t]*$/ || l ~ /^#/ || l ~ /^[ \t]*(```|~~~)/ || l ~ /^ ?([-*+]|[0-9]+[.)])[ \t]/) {
      close_entry(); continue
    }
    if (cur) buf = buf " " l
  }
  if (rc < 0) { print "l0_filed_check: cannot read " rp > "/dev/stderr"; exit 2 }
  close_entry()
  if (!nsec) {
    print "l0_filed_check: no \"## L0 questions\" section in " rp "; nothing to evaluate" > "/dev/stderr"
    exit 2
  }

  for (i = 1; i <= n; i++) {
    shown = "kengaku | " etag[i] " | " ekey[i]
    if (ekey[i] == "") { print "UNFILED report:" eln[i] " " shown "[empty question text]"; continue }
    p = anchored(S, "kengaku | " etag[i] " | " anchorable(ekey[i]))
    if (p) { filed++; print "FILED   report:" eln[i] " queue:" qline(p) " " shown; continue }
    p = index(S, anchorable(ekey[i]))
    print "UNFILED report:" eln[i] " " shown \
      (p ? "  [opening words at queue:" qline(p) " without this lane/round anchor; not counted]" : "")
  }
  if (nout)
    print "l0_filed_check: note: kengaku round-tag line(s) outside the L0 section, not checked: report:" outside > "/dev/stderr"
  printf "l0_filed_check: sections=%d questions=%d filed=%d unfiled=%d\n", nsec, n, filed, n - filed
  exit (filed < n)
}'

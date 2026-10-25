#!/bin/sh
# attrib_oracle.sh — kengaku round 25, C1 cross-check oracle (POSIX sh + awk; no python).
#
# Independent second parser for plans/attrib_calibration.py. For every
# corpus/evidence/attrib-r2[123]-*.log under the lane root (or each FILE given)
# it takes the LAST "## GT + scoring at close" block — the receipts' own
# AUTHORITATIVE SCORING SECTION rule (corpus/evidence/attrib-r21-impl-ds-trials.log:316),
# frozen as population P1 in plans/round-25-claims.md — and prints one line per file:
#   scored n, correct, per-GT-leg correct/n, per-predicted-leg counts,
#   table_md5 and key_md5 (duplicate detection), the block's journal window,
#   and checks=<pass>/<total>: every stored count/verdict line of the block
#   (GT counts, ACCURACY, TARGET, BODY, STREAM TARGET, score_summary JSON)
#   re-derived from the block's own rows; each failure prints a MISMATCH line.
# --intervals adds, per file: exact two-sided 95% Clopper-Pearson intervals
# (binomial pmf recurrence summed directly, then 100-step bisection; + - * / only,
# a different numerical method from the python instrument), Wilson 95%
# (sensitivity column only), the interval verdict
# (PASS iff lower >= bar; FAIL iff upper < bar; INDETERMINATE otherwise;
# UNTESTED iff n = 0) for overall accuracy, every stored point verdict, per-leg
# recall and specificity, and the Rogan-Gladen leg-share bound
# min/max (q + sp - 1)/(se + sp - 1) over se in [se_L,1], sp in [sp_L,1]
# (box corners; [0,1] when se_L + sp_L <= 1), clipped to [0,1].
#
# Definitions:
#   row         a block line starting "| T<digit>"; cells split on "|", trimmed.
#   scored      rows whose GT cell does not start with "EXCLUDED:".
#   correct     scored rows with prediction == GT (the stored correct cell must agree).
#   table_md5   md5 of every block line starting with "|" (header, separator,
#               rows), bytes as stored, newline-terminated.
#   key_md5     md5 of the LC_ALL=C-sorted lines "trial<TAB>prediction<TAB>GT<TAB>chain":
#               the frozen dedup key (same trial ids, predictions, GT, chains).
#   DUP         last blocks sharing key_md5 are one sample under the frozen rule;
#               keep = earliest journal --since. journal_windows and
#               ablations_equal say whether the merged blocks are in fact one run.
#   prior       each earlier GT block of the file: same|diff table_md5 as the last block.
#   trials      "=== [T..." trial records anywhere in the file (all runs, scored or not).
#   extra_req   journal request-lines in the block's GT window minus table rows.
#   read_lag_s  block scoring stamp minus the journal --until bound (negative =
#               the journal was read before the GT window closed).
#   summary_verdict  the score_summary JSON verdict and the stored line it equals
#               (accuracy | stream-target).
#   legs (--intervals) keys of the trials' scores={...} dicts in the file (src s)
#               plus every GT (g) and prediction (p) value of the scored rows;
#               share q = predicted count / scored.
#
# Usage: sh plans/fixtures/r25/attrib_oracle.sh [--root DIR] [--intervals] [FILE...]
#        sh plans/fixtures/r25/attrib_oracle.sh --cp-table N   (k n lo hi, 0 <= k <= n <= N)
# Exit:  0 every stored line re-derives from its rows; 1 a mismatch or parse
#        anomaly (or a failed CP self-check); 2 usage. Reads receipt bytes only.

set -u
LC_ALL=C
export LC_ALL

usage() {
  echo "usage: sh plans/fixtures/r25/attrib_oracle.sh [--root DIR] [--intervals] [FILE...] | --cp-table N" >&2
  exit 2
}

root=
intervals=0
cptable=
while [ $# -gt 0 ]; do
  case $1 in
    --root) [ $# -ge 2 ] || usage; root=$2; shift 2 ;;
    --root=*) root=${1#--root=}; shift ;;
    --intervals) intervals=1; shift ;;
    --cp-table)
      [ $# -eq 2 ] || usage
      case $2 in '' | *[!0-9]*) usage ;; esac
      cptable=$2; shift 2 ;;
    --) shift; break ;;
    -*) usage ;;
    *) break ;;
  esac
done

if [ -n "$cptable" ]; then
  :
elif [ $# -eq 0 ]; then
  if [ -z "$root" ]; then
    root=$(CDPATH= cd -- "$(dirname "$0")/../../.." && pwd) || usage
  fi
  [ -d "$root/corpus/evidence" ] || { echo "attrib_oracle: no corpus/evidence under $root" >&2; exit 2; }
  set -- "$root"/corpus/evidence/attrib-r2[123]-*.log
  [ -e "$1" ] || { echo "attrib_oracle: no attrib-r2[123]-*.log under $root/corpus/evidence" >&2; exit 2; }
else
  [ -z "$root" ] || usage
  for f in "$@"; do [ -f "$f" ] || { echo "attrib_oracle: not a file: $f" >&2; exit 2; }; done
fi

if command -v md5sum >/dev/null 2>&1; then MD5=md5sum
elif command -v md5 >/dev/null 2>&1; then MD5='md5 -q'
elif command -v openssl >/dev/null 2>&1; then MD5='openssl md5 -r'
else echo "attrib_oracle: no md5 tool (md5sum, md5 or openssl)" >&2; exit 2
fi
md5_stdin() { $MD5 | awk '{ print $1 }'; }

# Shared awk library: parsing helpers, exact binomial CP, Wilson, verdicts, RG bound.
LIB=$(cat <<'AWK'
BEGIN { ALPHA = 0.05; Z = 1.959963984540054 }
function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
function after(s, k,   i) { i = index(s, k); return i ? substr(s, i + length(k)) : "" }
function upto(s, k,   i) { i = index(s, k); return i ? substr(s, 1, i - 1) : s }
function num(s) { return match(s, /^[0-9]+(\.[0-9]+)?/) ? substr(s, 1, RLENGTH) : "" }
function word(s) { return match(s, /^[A-Za-z0-9_.:-]+/) ? substr(s, 1, RLENGTH) : "" }
function get(a, k) { return (k in a) ? a[k] + 0 : 0 }
function absv(x) { return x < 0 ? -x : x }
function sortkeys(a, out,   k, m, t, x) {
  m = 0
  for (k in a) {
    out[++m] = k
    for (t = m; t > 1 && (out[t - 1] "") > (out[t] ""); t--) { x = out[t]; out[t] = out[t - 1]; out[t - 1] = x }
  }
  return m
}
function pw(x, n,   r, i) { r = 1; for (i = 0; i < n; i++) r *= x; return r }
function sqroot(a,   x, i) { if (a <= 0) return 0; x = (a > 1) ? a : 1; for (i = 0; i < 100; i++) x = (x + a / x) / 2; return x }
# P(lo_i <= X <= hi_i), X ~ Binomial(n, p): the pmf by the multiplicative recurrence
# t(i+1) = t(i) (n - i)/(i + 1) p/(1 - p) from t(0) = (1 - p)^n, reflected to p <= 0.5
# so t(0) >= 2^-n. Arithmetic only: no exp/log/lgamma (runs on math-less awks too).
function binsum(lo_i, hi_i, n, p,   i, t, s, x) {
  if (p <= 0) return (lo_i <= 0) ? 1 : 0
  if (p >= 1) return (hi_i >= n) ? 1 : 0
  if (p > 0.5) { x = lo_i; lo_i = n - hi_i; hi_i = n - x; p = 1 - p }
  t = pw(1 - p, n); s = 0
  for (i = 0; i <= n; i++) {
    if (i >= lo_i && i <= hi_i) s += t
    if (i < n) t = t * (n - i) / (i + 1) * p / (1 - p)
  }
  return s
}
# Clopper-Pearson: lower solves P(X >= k | p) = alpha/2, upper solves P(X <= k | p) = alpha/2.
function cp_lo(k, n,   a, b, m, it) {
  if (n <= 0 || k <= 0) return 0
  a = 0; b = 1
  for (it = 0; it < 100; it++) { m = (a + b) / 2; if (binsum(k, n, n, m) < ALPHA / 2) a = m; else b = m }
  return (a + b) / 2
}
function cp_hi(k, n,   a, b, m, it) {
  if (n <= 0 || k >= n) return 1
  a = 0; b = 1
  for (it = 0; it < 100; it++) { m = (a + b) / 2; if (binsum(0, k, n, m) > ALPHA / 2) a = m; else b = m }
  return (a + b) / 2
}
function wilson(k, n,   p, z2, d, c, h) {
  if (n <= 0) { WLO = 0; WHI = 1; return }
  p = k / n; z2 = Z * Z; d = 1 + z2 / n; c = p + z2 / (2 * n)
  h = Z * sqroot(p * (1 - p) / n + z2 / (4 * n * n))
  WLO = (c - h) / d; WHI = (c + h) / d
  if (WLO < 0) WLO = 0
  if (WHI > 1) WHI = 1
}
function iv(k, n, bar) {
  if (n <= 0) return "UNTESTED"
  if (cp_lo(k, n) >= bar) return "PASS"
  if (cp_hi(k, n) < bar) return "FAIL"
  return "INDETERMINATE"
}
function ivs(k, n, bar) {
  if (n <= 0) return (k + 0) "/" (n + 0) " -> UNTESTED"
  wilson(k, n)
  return sprintf("%d/%d cp=[%.4f,%.4f] wilson=[%.4f,%.4f] -> %s", k, n, cp_lo(k, n), cp_hi(k, n), WLO, WHI, iv(k, n, bar))
}
function rg(q, sel, spl,   i, se, sp, v) {
  if (sel + spl <= 1) { RGLO = 0; RGHI = 1; return }
  RGLO = 2; RGHI = -1
  for (i = 0; i < 4; i++) {
    se = (i < 2) ? sel : 1; sp = (i % 2 == 0) ? spl : 1
    v = (q + sp - 1) / (se + sp - 1)
    if (v < RGLO) RGLO = v
    if (v > RGHI) RGHI = v
  }
  if (RGLO < 0) RGLO = 0
  if (RGHI > 1) RGHI = 1
  if (RGLO > 1) RGLO = 1
  if (RGHI < 0) RGHI = 0
}
AWK
)

# --cp-table N: k n lo hi (12 decimals) for 0 <= k <= n <= N, for diffing against any
# other CP implementation (e.g. a reference table or the python instrument).
if [ -n "$cptable" ]; then
  awk -v N="$cptable" "$LIB"'
  BEGIN { print "k\tn\tlo\thi"; for (n = 0; n <= N; n++) for (k = 0; k <= n; k++) printf "%d\t%d\t%.12f\t%.12f\n", k, n, cp_lo(k, n), cp_hi(k, n) }'
  exit $?
fi

# Per-file analysis. Inputs: REL S E NB PRIOR TMD5 KMD5 INTERVALS SQ (S = E = 0: trial-only).
ANALYZE=$(cat <<'AWK'
function canon_arr(a,   ks, m, i, s) {
  m = sortkeys(a, ks); s = ""
  for (i = 1; i <= m; i++) s = s (i > 1 ? "," : "") ks[i] "=" (a[ks[i]] + 0)
  return s
}
function canon_str(d,   n, i, j, parts, tmp) {
  split("", tmp)
  gsub(/[{} "]/, "", d); gsub(SQ, "", d)
  n = split(d, parts, ",")
  for (i = 1; i <= n; i++) {
    if (parts[i] == "") continue
    j = index(parts[i], ":")
    if (!j) return "UNPARSED(" d ")"
    tmp[substr(parts[i], 1, j - 1)] = substr(parts[i], j + 1)
  }
  return canon_arr(tmp)
}
function class_dist(cls,   k, p, tmp) {
  split("", tmp)
  for (k in cg) { split(k, p, SUBSEP); if (p[1] == cls) tmp[p[2]] = cg[k] }
  return canon_arr(tmp)
}
function point(k, n, bar, mn,   a) { a = (n > 0) ? k / n : 0; return (n >= mn + 0 && a >= bar + 0) ? "PASS" : "FAIL" }
function chk(name, good, detail) { nchk++; if (good) npass++; else { bad++; mm = mm "  MISMATCH " name ": " detail "\n" } }
function tally(kind, v) { TAL = TAL "@tally\t" REL "\t" kind "\t" v "\n" }
function iso2epoch(s,   y, mo, d, yy, era, yoe, mp, doe) {
  y = substr(s, 1, 4) + 0; mo = substr(s, 6, 2) + 0; d = substr(s, 9, 2) + 0
  yy = y - (mo <= 2); era = int(yy / 400); yoe = yy - era * 400; mp = (mo + 9) % 12
  doe = yoe * 365 + int(yoe / 4) - int(yoe / 100) + int((153 * mp + 2) / 5) + d - 1
  return (era * 146097 + doe - 719468) * 86400 + substr(s, 12, 2) * 3600 + substr(s, 15, 2) * 60 + substr(s, 18, 2)
}
BEGIN { split("", skey); split("", gtn); split("", predn); split("", tp); split("", cg); split("", cgok); split("", clsn); split("", uni) }
/^    prediction=/ && index($0, " scores={") {
  d = upto(after($0, " scores={"), "}"); n = split(d, parts, ",")
  for (i = 1; i <= n; i++) { k = upto(parts[i], ":"); gsub(/[" ]/, "", k); if (k != "") skey[k] = 1 }
}
/^=== \[T[0-9]/ { trials++ }
NR < S + 0 || NR > E + 0 { next }
NR == S + 0 {
  if (match($0, /[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z/)) at = substr($0, RSTART, RLENGTH)
  next
}
/^# journal command:/ { unit = word(after($0, " -u ")); since = num(after($0, "--since @")); untl = num(after($0, "--until @")); next }
/^# journal stdout/ { jreq = num(after($0, "request-lines=")); next }
/^[|] trial [|]/ { thead++; next }
/^[|] T[0-9]/ {
  rows++
  if (split($0, c, "[|]") != 9) { malformed++; next }
  t = trim(c[2]); cl = trim(c[3]); pr = trim(c[4]); g = trim(c[5]); co = trim(c[8])
  if (t in seen) duptrial++
  seen[t] = 1
  predall[pr]++
  if (index(g, "EXCLUDED:") == 1) { excl++; if (co == "YES" || co == "NO") malformed++; next }
  scored++; gtn[g]++; predn[pr]++
  hit = (pr == g)
  if (hit) { ok++; tp[g]++ }
  if (co != "YES" && co != "NO") malformed++
  else if (hit != (co == "YES")) colmis++
  clsn[cl]++; cg[cl SUBSEP g]++
  if (hit) cgok[cl SUBSEP g]++
  next
}
/^GT counts: / { has_gt = 1; st_gt = after($0, "GT counts: "); next }
/^ACCURACY: / {
  has_acc = 1; r = after($0, "ACCURACY: ")
  acc_k = num(r); acc_n = num(after(r, "/")); acc_bar = num(after($0, "(bar "))
  acc_min = num(after($0, "min scored n ")); acc_v = word(after($0, "-> ")); next
}
/^TARGET / {
  nt++; tl[nt] = upto(after($0, "TARGET "), ":")
  tn[nt] = num(after($0, "on-target GT n=")); tk[nt] = num(after($0, "correct "))
  tbar[nt] = num(after($0, "(bar ")); tmin[nt] = num(after($0, "min on-target n "))
  tv[nt] = word(after($0, "-> ")); td[nt] = after($0, "class GT dist "); next
}
/^BODY / {
  nbd++; bname[nbd] = upto(after($0, "BODY "), ":")
  bs[nbd] = num(after($0, "scored n=")); btg[nbd] = upto(after($0, "on-target("), ")")
  bn[nbd] = num(after($0, ") n=")); bk[nbd] = num(after($0, "correct ")); bd[nbd] = after($0, "GT dist "); next
}
/^STREAM TARGET / {
  has_st = 1; st_t = upto(after($0, "STREAM TARGET "), ":")
  st_n = num(after($0, "on-target GT n=")); st_k = num(after($0, "correct "))
  st_bar = num(after($0, "(bar ")); st_min = num(after($0, "min on-target n ")); st_v = word(after($0, "-> ")); next
}
/^  (loo|mimicry):/ { abl = abl $1 "=" $2 ";"; next }
/^[{]"kind": "score_summary"/ {
  has_js = 1
  js_n = num(after($0, "\"scored\": ")); js_k = num(after($0, "\"correct\": "))
  js_v = upto(after($0, "\"verdict\": \""), "\""); js_gt = upto(after($0, "\"gt_counts\": "), "}")
  x = upto(after($0, "\"excluded\": "), ", \"ablations\""); js_ex = gsub(/\[/, "[", x) - 1; next
}
END {
  if (S + 0 == 0) { printf "%s blocks=0 trial-only trials=%d scored=0 correct=0\n", REL, trials; exit 0 }
  # a block must carry exactly one trial-table header; zero rows under it is a
  # legitimate n = 0 (UNTESTED), not a parse anomaly
  chk("rows", thead == 1 && !malformed && !colmis && !duptrial, "table_headers=" (thead + 0) " rows=" (rows + 0) " malformed=" (malformed + 0) " correct_cell_vs_pred_eq_gt=" (colmis + 0) " dup_trial_ids=" (duptrial + 0))
  if (has_gt) chk("GT_counts", canon_str(st_gt) == canon_arr(gtn), "stored{" canon_str(st_gt) "} rows{" canon_arr(gtn) "}")
  if (has_acc) {
    pv = point(ok, scored, acc_bar, acc_min)
    chk("ACCURACY", acc_k + 0 == ok && acc_n + 0 == scored && acc_v == pv, "stored " acc_k "/" acc_n " -> " acc_v "; rows " (ok + 0) "/" (scored + 0) " -> " pv)
  }
  for (i = 1; i <= nt; i++) {
    cls = "force-" tl[i]; n = get(cg, cls SUBSEP tl[i]); k = get(cgok, cls SUBSEP tl[i]); v = point(k, n, tbar[i], tmin[i])
    chk("TARGET:" tl[i], tn[i] + 0 == n && tk[i] + 0 == k && tv[i] == v && canon_str(td[i]) == class_dist(cls), "stored n=" tn[i] " correct=" tk[i] " -> " tv[i] " dist{" canon_str(td[i]) "}; rows n=" n " correct=" k " -> " v " dist{" class_dist(cls) "}")
  }
  for (i = 1; i <= nbd; i++) {
    cls = "stream-" bname[i]; s2 = get(clsn, cls); n = get(cg, cls SUBSEP btg[i]); k = get(cgok, cls SUBSEP btg[i])
    chk("BODY:" bname[i], bs[i] + 0 == s2 && bn[i] + 0 == n && bk[i] + 0 == k && canon_str(bd[i]) == class_dist(cls), "stored scored=" bs[i] " on-target=" bn[i] " correct=" bk[i] " dist{" canon_str(bd[i]) "}; rows " s2 "/" n "/" k " dist{" class_dist(cls) "}")
  }
  if (has_st) {
    stn = get(gtn, st_t); stk = get(tp, st_t); spv = point(stk, stn, st_bar, st_min)
    chk("STREAM_TARGET:" st_t, st_n + 0 == stn && st_k + 0 == stk && st_v == spv, "stored n=" st_n " correct=" st_k " -> " st_v "; rows n=" stn " correct=" stk " -> " spv)
  }
  if (has_js) {
    src = (has_acc && js_v == pv) ? "accuracy" : ((has_st && js_v == spv) ? "stream-target" : "none")
    chk("score_summary", js_n + 0 == scored && js_k + 0 == ok && js_ex == excl + 0 && canon_str(js_gt) == canon_arr(gtn) && src != "none", "stored scored=" js_n " correct=" js_k " excluded=" js_ex " gt{" canon_str(js_gt) "} verdict=" js_v "; rows " (scored + 0) "/" (ok + 0) " excluded=" (excl + 0) " gt{" canon_arr(gtn) "} verdict_src=" src)
  }
  m = sortkeys(gtn, ks); gs = ""
  for (i = 1; i <= m; i++) gs = gs (i > 1 ? "," : "") ks[i] "=" get(tp, ks[i]) "/" gtn[ks[i]]
  m = sortkeys(predn, ks); ps = ""
  for (i = 1; i <= m; i++) ps = ps (i > 1 ? "," : "") ks[i] "=" predn[ks[i]]
  hw = (since != "" && untl != ""); if (unit == "") unit = "NA"
  lag = (at != "" && untl != "") ? iso2epoch(at) - untl : "NA"
  line = REL " blocks=" NB
  if (PRIOR != "") line = line " prior=" PRIOR
  line = line " last=" S "-" E " trials=" (trials + 0) " rows=" (rows + 0) " excl=" (excl + 0) " scored=" (scored + 0) " correct=" (ok + 0) " gt[" gs "] pred[" ps "]"
  if (excl > 0) line = line " pred_all[" canon_arr(predall) "]"
  line = line " table_md5=" TMD5 " key_md5=" KMD5 " unit=" unit " win=" (hw ? since "-" untl : "NA")
  line = line " win_req=" (jreq == "" ? "NA" : jreq) " extra_req=" (jreq == "" ? "NA" : jreq - rows) " read_lag_s=" lag
  if (has_js) line = line " summary_verdict=" js_v "(" src ")"
  print line " checks=" (npass + 0) "/" nchk
  printf "%s", mm
  if (INTERVALS + 0) {
    bar = has_acc ? acc_bar + 0 : 0.8
    print "  acc " ivs(ok, scored, bar) " | stored ACCURACY point=" (has_acc ? acc_v : "absent")
    tally("acc", iv(ok, scored, bar))
    if (has_acc) tally("stored", iv(ok, scored, bar))
    for (i = 1; i <= nt; i++) {
      cls = "force-" tl[i]; n = get(cg, cls SUBSEP tl[i]); k = get(cgok, cls SUBSEP tl[i])
      print "  reverdict TARGET:" tl[i] " " ivs(k, n, tbar[i] + 0) " | stored point=" tv[i]
      tally("stored", iv(k, n, tbar[i] + 0))
    }
    if (has_st) {
      print "  reverdict STREAM_TARGET:" st_t " " ivs(stk, stn, st_bar + 0) " | stored point=" st_v
      tally("stored", iv(stk, stn, st_bar + 0))
    }
    for (k in skey) uni[k] = 1
    for (k in gtn) uni[k] = 1
    for (k in predn) uni[k] = 1
    m = sortkeys(uni, ks)
    for (i = 1; i <= m; i++) {
      L = ks[i]; n = get(gtn, L); k = get(tp, L); neg = scored - n; tneg = neg - (get(predn, L) - k)
      rg(scored ? get(predn, L) / scored : 0, cp_lo(k, n), cp_lo(tneg, neg))
      print "  leg " L " src=" ((L in gtn) ? "g" : "") ((L in predn) ? "p" : "") ((L in skey) ? "s" : "") " recall " ivs(k, n, bar) " | spec " ivs(tneg, neg, bar) " | share q=" get(predn, L) "/" (scored + 0) " rg=[" sprintf("%.4f,%.4f", RGLO, RGHI) "]"
      tally("recall", iv(k, n, bar)); tally("spec", iv(tneg, neg, bar))
    }
  }
  print "@rec\t" REL "\t" KMD5 "\t" TMD5 "\t" unit "\t" (hw ? since : "-") "\t" (hw ? untl : "-") "\t" (scored + 0) "\t" (ok + 0) "\t" (abl == "" ? "-" : abl)
  printf "%s", TAL
  if (bad) exit 1
  exit 0
}
AWK
)

# Cross-file: duplicate samples, shared GT windows, totals, deduplicated verdict tallies.
FOOTER=$(cat <<'AWK'
$1 == "@rec" { n++; rel[n] = $2; key[n] = $3; tmd[n] = $4; unit[n] = $5; hw[n] = ($6 != "-"); since[n] = $6 + 0; untl[n] = $7 + 0; sc[n] = $8 + 0; okc[n] = $9 + 0; abl[n] = $10; next }
$1 == "@tally" { nt++; tr[nt] = $2; tkind[nt] = $3; tv[nt] = $4; next }
END {
  for (i = 1; i <= n; i++) { cnt[key[i]]++; mem[key[i]] = mem[key[i]] " " i }
  m = sortkeys(cnt, ks)
  for (j = 1; j <= m; j++) {
    K = ks[j]
    if (cnt[K] < 2) continue
    split(substr(mem[K], 2), ids, " ")
    # keep: the earliest journal --since among blocks that record a window; ties and
    # window-less blocks fall back to the smallest path.
    keep = ids[1]
    for (q = 2; q <= cnt[K]; q++) {
      i = ids[q]
      if (hw[i] != hw[keep]) { if (hw[i]) keep = i; continue }
      if ((hw[i] && since[i] < since[keep]) || ((!hw[i] || since[i] == since[keep]) && rel[i] < rel[keep])) keep = i
    }
    dl = ""; wl = ""; teq = "yes"; aeq = "yes"
    for (q = 1; q <= cnt[K]; q++) {
      i = ids[q]
      if (tmd[i] != tmd[keep]) teq = "no"
      if (abl[i] != abl[keep]) aeq = "no"
      if (i == keep) continue
      duprel[rel[i]] = 1; ndup++; dl = dl (dl == "" ? "" : ",") rel[i]
      if (!hw[i] || !hw[keep]) w = "unknown"
      else if (since[i] == since[keep] && untl[i] == untl[keep]) w = "identical"
      else w = (since[i] <= untl[keep] && since[keep] <= untl[i]) ? "overlap" : "disjoint"
      wl = wl (wl == "" ? "" : ",") w
    }
    print "DUP key_md5=" K " keep=" rel[keep] " dup=" dl " table_md5_equal=" teq " journal_windows=" wl " ablations_equal=" aeq
  }
  if (!ndup) print "DUP none"
  for (i = 1; i <= n; i++) for (j = i + 1; j <= n; j++)
    if (hw[i] && hw[j] && unit[i] == unit[j] && since[i] <= untl[j] && since[j] <= untl[i]) {
      no++
      print "OVERLAP " rel[i] " " rel[j] " unit=" unit[i] " shared_s=" ((untl[i] < untl[j] ? untl[i] : untl[j]) - (since[i] > since[j] ? since[i] : since[j]))
    }
  if (!no) print "OVERLAP none (no two last blocks share a unit and a journal window)"
  for (i = 1; i <= n; i++) { s1 += sc[i]; k1 += okc[i]; if (!(rel[i] in duprel)) { nu++; s2 += sc[i]; k2 += okc[i] } }
  print "TOTAL files=" F " with_block=" (n + 0) " trial_only=" (F - n) " scored=" (s1 + 0) " correct=" (k1 + 0) " unique_samples=" (nu + 0) " dedup_scored=" (s2 + 0) " dedup_correct=" (k2 + 0) " files_with_mismatch=" BADF
  if (nt) {
    for (i = 1; i <= nt; i++) if (!(tr[i] in duprel)) vc[tkind[i] SUBSEP tv[i]]++
    split("acc stored recall spec", kinds, " ")
    for (j = 1; j <= 4; j++)
      print "VERDICTS(dedup) " kinds[j] ": PASS=" get(vc, kinds[j] SUBSEP "PASS") " FAIL=" get(vc, kinds[j] SUBSEP "FAIL") " INDETERMINATE=" get(vc, kinds[j] SUBSEP "INDETERMINATE") " UNTESTED=" get(vc, kinds[j] SUBSEP "UNTESTED")
  }
}
AWK
)

status=0
if [ "$intervals" -eq 1 ]; then
  # CP defining equations with closed forms (k = n, k = 0, k = 1, k = n - 1),
  # tail symmetry, and Wilson at k = n (lower = n / (n + z^2)); powers only.
  awk "$LIB"'
  BEGIN {
    e1 = absv(pw(cp_lo(17, 17), 17) - ALPHA / 2); e2 = absv(pw(cp_lo(16, 16), 16) - ALPHA / 2)
    e3 = absv(pw(1 - cp_hi(0, 16), 16) - ALPHA / 2); e4 = absv(1 - pw(1 - cp_lo(1, 10), 10) - ALPHA / 2)
    e5 = absv(1 - pw(cp_hi(9, 10), 10) - ALPHA / 2); e6 = absv(cp_lo(9, 10) - (1 - cp_hi(1, 10)))
    wilson(20, 20); e7 = absv(WLO - 20 / (20 + Z * Z))
    e = e1; if (e2 > e) e = e2; if (e3 > e) e = e3; if (e4 > e) e = e4; if (e5 > e) e = e5; if (e6 > e) e = e6; if (e7 > e) e = e7
    printf "# cp_selfcheck=%s max_abs_err=%.1e lo(16/16)=%.6f lo(17/17)=%.6f\n", ((e < 1e-12) ? "ok" : "FAILED"), e, cp_lo(16, 16), cp_lo(17, 17)
    if (e < 1e-12) exit 0
    exit 1
  }' || status=1
fi

echo "# attrib_oracle files=$# block=LAST '## GT + scoring at close' md5=${MD5%% *} root=${root:-argv}"
recs=
bad_files=0
for f in "$@"; do
  if [ -n "$root" ]; then rel=${f#"$root"/}; else rel=$f; fi
  ranges=$(awk '
    /^## GT [+] scoring at close/ { if (n && !e[n]) e[n] = NR - 1; n++; s[n] = NR; next }
    /^## / { if (n && !e[n]) e[n] = NR - 1 }
    END { if (n && !e[n]) e[n] = NR; for (i = 1; i <= n; i++) print s[i], e[i] }' "$f")
  nb=0 s=0 e=0 prior= tmd5=- kmd5=-
  if [ -n "$ranges" ]; then
    nb=$(printf '%s\n' "$ranges" | awk 'END { print NR }')
    last=$(printf '%s\n' "$ranges" | awk 'END { print }')
    s=${last% *} e=${last#* }
    tmd5=$(awk -v s="$s" -v e="$e" 'NR >= s + 0 && NR <= e + 0 && /^[|]/' "$f" | md5_stdin)
    kmd5=$(awk -v s="$s" -v e="$e" -F'[|]' 'NR >= s + 0 && NR <= e + 0 && /^[|] T[0-9]/ {
        for (i = 2; i <= 7; i++) { sub(/^[ \t]+/, "", $i); sub(/[ \t]+$/, "", $i) }
        print $2 "\t" $4 "\t" $5 "\t" $7 }' "$f" | sort | md5_stdin)
    if [ "$nb" -gt 1 ]; then
      prior=$(printf '%s\n' "$ranges" | sed '$d' | while read -r ps pe; do
        pm=$(awk -v s="$ps" -v e="$pe" 'NR >= s + 0 && NR <= e + 0 && /^[|]/' "$f" | md5_stdin)
        if [ "$pm" = "$tmd5" ]; then printf '%s:same,' "$ps"; else printf '%s:diff,' "$ps"; fi
      done)
      prior=${prior%,}
    fi
  fi
  out=$(awk -v REL="$rel" -v S="$s" -v E="$e" -v NB="$nb" -v PRIOR="$prior" -v TMD5="$tmd5" \
    -v KMD5="$kmd5" -v INTERVALS="$intervals" -v SQ="'" "$LIB
$ANALYZE" "$f")
  rc=$?
  printf '%s\n' "$out" | awk '!/^@/'
  recs="$recs$(printf '%s\n' "$out" | awk '/^@/')
"
  [ "$rc" -eq 0 ] || { status=1; bad_files=$((bad_files + 1)); }
done
printf '%s' "$recs" | awk -F '\t' -v F="$#" -v BADF="$bad_files" "$LIB
$FOOTER"
exit "$status"

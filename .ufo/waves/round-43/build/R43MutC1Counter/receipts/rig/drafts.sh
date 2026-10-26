#!/usr/bin/env bash
# R43MutC1Counter: draft controls for surviving guards + gap probes. Each draft runs the named control
# against the PRISTINE counter and (where relevant) the mutant counter, into $S/drafts-out/<draft>/.
# usage: drafts.sh <draft ...>   (d02 d03 d04 d08 d09 d12 d13 d14 d15 h7)
set -u
S=/fast/scratch/hyaku/kengaku-r43/R43MutC1Counter
L=$S/lane
LC=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims
P=$S/lane/plans/round43_c1_verify.py   # pristine
W=$S/dw; rm -rf "$W"; mkdir -p "$W" "$S/drafts-out"
env43() { "$LC/envelope.sh" "$W" "$@"; }
mirror() { M=$W/m-$1; mkdir -p "$M/plans"; cp "$2" "$M/plans/round43_c1_verify.py"; cp "$L"/plans/anchor_digest_check.py "$L"/plans/order_check.py "$L"/plans/round42_c1_verify.py "$M/plans/"; }
patched() { python3 - "$M/plans/round43_c1_verify.py" "$1" "$2" <<'PY'
import sys
p, old, new = sys.argv[1], sys.argv[2].encode().decode("unicode_escape"), sys.argv[3].encode().decode("unicode_escape")
s = open(p).read(); assert s.count(old) == 1, ("patch anchor not unique", old); open(p, "w").write(s.replace(old, new))
PY
}
SEL=" ${*:-all} "
has() { case "$SEL" in *" $1 "*|*" all "*) return 0 ;; esac; return 1; }

# d02: control-c1-value (SITE_EQUAL->True) re-run against the M02 counter: dropped first reference trace
# turns the forced-equal cases into FALSE KILLS.
if has d02; then
  mirror d02 "$S/mut/M02-ref-trace1-dropped.py"; mkdir -p "$M/plans/battery43"; cp "$LC/witness/w_near.py" "$M/plans/battery43/"
  { patched '    return tuple(mut_sites) == tuple(ref_sites)' '    return True'
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$W/d02"; } > "$S/drafts-out/d02.txt" 2>&1
  echo "d02 rc=$? (expect killed=9 here; pristine value control gives unattributed=9)"
fi
# d03: PYTHONHASHSEED dropped ("" = randomized) -> set-repr order varies -> site records unstable?
if has d03; then
  mirror d03p "$P"
  { patched '"PYTHONHASHSEED": "0"' '"PYTHONHASHSEED": ""'
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$LC/witness" --work "$W/d03p"; } > "$S/drafts-out/d03-pristine.txt" 2>&1
  echo "d03 pristine rc=$? (look for site-record-unstable)"
  mirror d03m "$S/mut/M03-ref-trace2-reused.py"
  { patched '"PYTHONHASHSEED": "0"' '"PYTHONHASHSEED": ""'
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$LC/witness" --work "$W/d03m"; } > "$S/drafts-out/d03-mutant.txt" 2>&1
  echo "d03 mutant rc=$?"
fi
# d04: extra mutant row XNL1 with a TWO-line new for a ONE-line old -> newline-count validity must refuse it.
if has d04; then
  mirror d04p "$P"
  { python3 - "$M/plans/round43_c1_verify.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read(); i = s.index("MUTANTS = ["); j = s.index("\n]\n", i)
row = ("    ('XNL1', 'anchor', 'row-malformed', 'silence', 'direct',\n"
       "     \"draft XNL1: a two-line new for a one-line old (newline-count validity check)\",\n"
       "     \"draft\",\n"
       "     '        if len(r[\"cells\"]) != NCELLS:',\n"
       "     '        if len(r[\"cells\"]) < NCELLS:\\n            pass'),\n")
open(p, "w").write(s[:j] + row + s[j:])
PY
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$LC/witness" --work "$W/d04p"; } > "$S/drafts-out/d04-pristine.txt" 2>&1
  echo "d04 pristine rc=$? (expect MUTANT XNL1 ... invalid)"
  mirror d04m "$S/mut/M04-newline-check-off.py"
  { python3 - "$M/plans/round43_c1_verify.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read(); i = s.index("MUTANTS = ["); j = s.index("\n]\n", i)
row = ("    ('XNL1', 'anchor', 'row-malformed', 'silence', 'direct',\n"
       "     \"draft XNL1: a two-line new for a one-line old (newline-count validity check)\",\n"
       "     \"draft\",\n"
       "     '        if len(r[\"cells\"]) != NCELLS:',\n"
       "     '        if len(r[\"cells\"]) < NCELLS:\\n            pass'),\n")
open(p, "w").write(s[:j] + row + s[j:])
PY
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$LC/witness" --work "$W/d04m"; } > "$S/drafts-out/d04-mutant.txt" 2>&1
  echo "d04 mutant rc=$? (expect MUTANT XNL1 ... killed)"
fi
# d08: hostile h8bare-wt — the core.worktree-branch-only state.
if has d08; then
  for cnt in "$P:pristine" "$S/mut/M08-repo-worktree-off.py:mutant"; do
    c=${cnt%%:*}; who=${cnt##*:}
    mirror d08 "$c"; d=$W/hb-h8; mkdir -p "$d"; cp "$S/drafts/h8bare-wt.py" "$d/"
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$d" --only NO5 --work "$W/d08-$who" > "$S/drafts-out/d08-$who.txt" 2>&1
    echo "d08 $who rc=$?"
  done
fi
# d09: hostile wrongdecl — the defects-declaration conjunct of exhibits.
if has d09; then
  for cnt in "$P:pristine" "$S/mut/M09-exhibits-defects-dropped.py:mutant"; do
    c=${cnt%%:*}; who=${cnt##*:}
    mirror d09 "$c"; d=$W/hb-wd; mkdir -p "$d"; cp "$S/drafts/wrongdecl.py" "$d/"
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$d" --only NA1 --work "$W/d09-$who" > "$S/drafts-out/d09-$who.txt" 2>&1
    echo "d09 $who rc=$?"
  done
fi
# d12: tamper probe — a content-only rewrite of a fixture file between the two fingerprints.
if has d12; then
  for cnt in "$P:pristine" "$S/mut/M12-fingerprint-content-dropped.py:mutant"; do
    c=${cnt%%:*}; who=${cnt##*:}
    mirror d12 "$c"
    { patched 'prints = [fingerprint(fx["dir"]) for fx in fixtures]' \
        'prints = [fingerprint(fx["dir"]) for fx in fixtures]; _tp = pathlib.Path(fixtures[0]["argv"][1]) / "corpus/SOURCES.md"; _td = _tp.read_bytes(); _tp.write_bytes(_td[::-1])'
      env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$LC/witness" --work "$W/d12-$who"; } > "$S/drafts-out/d12-$who.txt" 2>&1
    echo "d12 $who rc=$?"
  done
fi
# d13: hostile sctoken — the token scan must fire on a comment-only mention.
if has d13; then
  for cnt in "$P:pristine" "$S/mut/M13-sidechannel-scan-off.py:mutant"; do
    c=${cnt%%:*}; who=${cnt##*:}
    mirror d13 "$c"; d=$W/hb-sc; mkdir -p "$d"; cp "$S/drafts/sctoken.py" "$d/"
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$d" --only NO5 --work "$W/d13-$who" > "$S/drafts-out/d13-$who.txt" 2>&1
    echo "d13 $who rc=$?"
  done
fi
# d10: FLOORS inconsistent with TOTAL (sum 10 != 9) — the sum term cannot be isolated: the per_tool
# floors term fails too, so pristine and M10 counters both print PREDICATE C1 fail (redundancy demo).
if has d10; then
  for cnt in "$P:pristine" "$S/mut/M10-floors-sum-dropped.py:mutant"; do
    c=${cnt%%:*}; who=${cnt##*:}
    mirror d10 "$c"; mkdir -p "$M/plans/battery43"; cp "$LC/witness/w_near.py" "$M/plans/battery43/"
    { patched 'FLOORS = {"anchor": 6, "order": 3}' 'FLOORS = {"anchor": 6, "order": 4}'
      env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --work "$W/d10-$who"; } > "$S/drafts-out/d10-$who.txt" 2>&1
    echo "d10 $who rc=$? (both expected rc=1: the per_tool term also fails)"
  done
fi
# d14: PINS-AFTER — the tool file is edited MID-RUN (between the two pin hashes).
if has d14; then
  for cnt in "$P:pristine" "$S/mut/M14-pins-after-dropped.py:mutant"; do
    c=${cnt%%:*}; who=${cnt##*:}
    mirror d14 "$c"
    env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$LC/witness" --work "$W/d14-$who" > "$S/drafts-out/d14-$who.txt" 2>&1 &
    dpid=$!; sleep 2; echo "# midrun edit" >> "$M/plans/anchor_digest_check.py"; wait $dpid
    echo "d14 $who rc=$? (racy: the edit must land between the two pin hashes)"
  done
fi
# d15: null detection — the null copy is made behaviourally different (NA1-shaped) by a one-line patch.
if has d15; then
  for cnt in "$P:pristine" "$S/mut/M15-null-run-off.py:mutant"; do
    c=${cnt%%:*}; who=${cnt##*:}
    mirror d15 "$c"
    { patched 'nv.write_text(srcs[tool])' "nv.write_text(srcs[tool].replace('len(r[\"cells\"]) != NCELLS', 'len(r[\"cells\"]) < NCELLS', 1))"
      env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$LC/witness" --work "$W/d15-$who"; } > "$S/drafts-out/d15-$who.txt" 2>&1
    echo "d15 $who rc=$?"
  done
fi
# h7: hostile h7gitfile — GAP PROBE against the PRISTINE counter (expect: NO refusal = acceptance).
if has h7; then
  mirror h7 "$P"; d=$W/hb-h7; mkdir -p "$d"; cp "$S/drafts/h7gitfile.py" "$d/"
  env43 python3 "$M/plans/round43_c1_verify.py" --lane "$M" --battery-dir "$d" --only NO5 --work "$W/h7" > "$S/drafts-out/h7-pristine.txt" 2>&1
  echo "h7 pristine rc=$? (refusal expected if the guard were complete; acceptance = gap)"
fi
echo "drafts done"

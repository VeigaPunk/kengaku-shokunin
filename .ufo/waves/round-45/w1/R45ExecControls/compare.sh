#!/usr/bin/env bash
# R45ExecControls: byte/field comparison of reproduced controls against the committed receipts.
# usage: compare.sh <receipts dir copied into this dir> <frozen claims dir>
set -u
W=${1:-$(dirname "$0")}
CL=${2:-/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims}
fail=0
echo "## C1: the four frozen predicate lines, byte-compared"
for pair in "nothing:control-c1-nothing.txt" "r44:control-c1-fence-r44.txt" \
            "admit:control-c1-fence-admit_all.txt" "refuse:control-c1-fence-refuse_all.txt" \
            "static:control-c1-fence-static_only.txt"; do
  n=${pair%%:*}; c=${pair##*:}
  grep -E '^(REFUSALS|HONEST|CALIBRATION|PREDICATE)' "$W/out-c1-$n.txt" > "/tmp/s-$n.$$"
  grep -E '^(REFUSALS|HONEST|CALIBRATION|PREDICATE)' "$CL/$c" > "/tmp/sc-$n.$$"
  if cmp -s "/tmp/s-$n.$$" "/tmp/sc-$n.$$"; then
    echo "CONTROL c1-$n vs $c : 4 summary lines BYTE-IDENTICAL"
  else
    echo "CONTROL c1-$n vs $c : DIFF"; diff "/tmp/sc-$n.$$" "/tmp/s-$n.$$"; fail=1
  fi
  rm -f "/tmp/s-$n.$$" "/tmp/sc-$n.$$"
done
echo
echo "## C1: per-fixture verdict + outside-open counts (FENCE-RUN fields 1-5, REFUSAL rows, summary lines)"
for pair in "nothing:control-c1-nothing.txt" "r44:control-c1-fence-r44.txt" \
            "admit:control-c1-fence-admit_all.txt" "refuse:control-c1-fence-refuse_all.txt" \
            "static:control-c1-fence-static_only.txt"; do
  n=${pair%%:*}; c=${pair##*:}
  awk '/^FENCE-RUN/{print $1,$2,$3,$4,$5} /^REFUSAL /{print $0} /^(PINS|FENCE |REFUSALS|HONEST|CALIBRATION|PREDICATE)/{print}' \
      "$W/out-c1-$n.txt" > "/tmp/f-$n.$$"
  awk '/^FENCE-RUN/{print $1,$2,$3,$4,$5} /^REFUSAL /{print $0} /^(PINS|FENCE |REFUSALS|HONEST|CALIBRATION|PREDICATE)/{print}' \
      "$CL/$c" > "/tmp/fc-$n.$$"
  if cmp -s "/tmp/f-$n.$$" "/tmp/fc-$n.$$"; then
    echo "CONTROL c1-$n vs $c : $(grep -c '^FENCE-RUN' "/tmp/f-$n.$$") fixture verdicts + all REFUSAL rows IDENTICAL"
  else
    echo "CONTROL c1-$n vs $c : DIFF"; diff "/tmp/fc-$n.$$" "/tmp/f-$n.$$" | head -20; fail=1
  fi
  rm -f "/tmp/f-$n.$$" "/tmp/fc-$n.$$"
done
echo
echo "## C2 nothing control (HEAD-era committed receipt, 8-row spec, 6 untracked at capture)"
grep -vE '^ENVELOPE' "$W/out-c2-untracked.txt" > "/tmp/c2h.$$"
if cmp -s "$CL/control-c2-nothing.txt" "/tmp/c2h.$$"; then echo "BYTE-IDENTICAL"; else diff "$CL/control-c2-nothing.txt" "/tmp/c2h.$$"; fail=1; fi
echo
echo "## C2 nothing control (freeze-era committed receipt, 9-row spec, 151 untracked at capture)"
grep -vE '^ENVELOPE' "$W/out-c2-freeze-u151.txt" > "/tmp/c2f.$$"
if cmp -s "$W/c2-committed-freeze.txt" "/tmp/c2f.$$"; then echo "BYTE-IDENTICAL"; else diff "$W/c2-committed-freeze.txt" "/tmp/c2f.$$"; fail=1; fi
echo
echo "## C2 nothing control on a clean clone (P9 clean-tree clause reads untracked=0)"
grep -E '^    gate: P9|^    gate: defects' "$W/out-c2-head.txt" "$W/out-c2-freeze.txt"
echo
echo "## C2 predictor control (V11 red-as-required), freeze-era committed receipt"
grep -vE '^ENVELOPE' "$W/out-predictor-freeze.txt" > "/tmp/p.$$"
grep -vE '^2026-' "$CL/control-c2-predictor.txt" > "/tmp/pc.$$"
if cmp -s "/tmp/pc.$$" "/tmp/p.$$"; then echo "BYTE-IDENTICAL (committed file's trailing timestamp line excluded)"; else diff "/tmp/pc.$$" "/tmp/p.$$"; fail=1; fi
rm -f "/tmp/c2h.$$" "/tmp/c2f.$$" "/tmp/p.$$" "/tmp/pc.$$"
echo
echo "RESULT controls mismatched=$fail"
exit $fail

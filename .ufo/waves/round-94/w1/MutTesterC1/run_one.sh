#!/usr/bin/env bash
# run_one.sh LABEL MUTANT_PY LANE REV WORKDIR
set -u
label="$1"; mut="$2"; lane="$3"; rev="$4"; work="$5"
S=/fast/scratch/hyaku/kengaku-r94/MutTesterC1
out="$S/out/$label.txt"
mkdir -p "$S/out" "$(dirname "$work")"
sha=$(sha256sum "$mut" | cut -d' ' -f1)
{
  echo "# cmd: python3 ${mut#$S/} --lane $lane --rev $rev --work ${work#$S/}"
  echo "# counter bytes: $sha; host $(date -Is)"
  python3 "$mut" --lane "$lane" --rev "$rev" --work "$work"
  echo "rc=$?"
} > "$out" 2>&1
echo "$label rc=$(tail -1 "$out")"

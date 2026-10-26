#!/usr/bin/env bash
# R42MutC1Counter runner: one enveloped counter run per (variant, setup), diff vs committed control block.
set -u
S=/fast/scratch/hyaku/kengaku-r42/R42MutC1Counter
EW=(/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)
declare -A MIRROR=( [N]="$S/lane" [W]="$S/mW" [A]="$S/mW" [M]="$S/mW" [T]="$S/mT" [H]="$S/mH" [D]="$S/mW" )
declare -A CBASE=( [N]=pristine [W]=pristine [A]=attr [M]=nomut [T]=pristine [H]=pristine [D]=dir )
ORDER="N H M T W D A"

run_one() { # $1=setup $2=variant-file $3=tag -> echoes MATCH/DIFF + rc; writes $S/res/$3.$1.out
  local setup=$1 vf=$2 tag=$3 out rc
  out=$( cd "${MIRROR[$setup]}" && "${EW[@]}" /usr/bin/python3 "$vf" --lane . --work "$S/w/$tag" 2>&1 ); rc=$?
  printf '%s\n' "$out" > "$S/res/$tag.$setup.out"
  echo "$rc" > "$S/res/$tag.$setup.rc"
  if diff -q "$S/res/$tag.$setup.out" "$S/base/$setup.block" >/dev/null 2>&1; then
    echo "$tag $setup MATCH rc=$rc"
  else
    echo "$tag $setup DIFF rc=$rc"
    diff "$S/res/$tag.$setup.out" "$S/base/$setup.block"
  fi
}

mode=$1
if [ "$mode" = pristine ]; then
  for st in $ORDER; do run_one "$st" "$S/c/${CBASE[$st]}.py" "PRISTINE"; done
else
  mid=$1
  : > "$S/res/$mid.txt"
  for st in $ORDER; do
    line=$(run_one "$st" "$S/v/${mid}_${st}.py" "$mid")
    echo "$line" >> "$S/res/$mid.txt"
    case "$line" in DIFF*) echo "CAUGHT-BY $st" >> "$S/res/$mid.txt"; break;; esac
  done
  cat "$S/res/$mid.txt"
fi

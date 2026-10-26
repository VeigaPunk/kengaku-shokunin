#!/usr/bin/env bash
# R42MutC1Counter draft controls: intact counter vs guard-mutant counter on a drafted setup.
set -u
S=/fast/scratch/hyaku/kengaku-r42/R42MutC1Counter
EW=(/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)
runv() { # $1=variant-file $2=tag $3...=extra args ; cwd from DRAFT_CWD (default $S/lane)
  local vf=$1 tag=$2; shift 2
  ( cd "${DRAFT_CWD:-$S/lane}" && "${EW[@]}" /usr/bin/python3 "$vf" --lane . "$@" ) > "$S/res/$tag.out" 2>&1
  echo "rc=$?" >> "$S/res/$tag.out"
}
show() { echo "--- $1 (intact vs mutant)"; diff "$S/res/$1.intact.out" "$S/res/$1.mut.out" || true; }

case "${1:-all}" in
d1) runv "$S/v2/d1_intact.py" d1.intact --only XO5 --battery-dir "$S/draft/b1" --work "$S/w/d1i"
    runv "$S/v2/d1_mut.py"    d1.mut    --only XO5 --battery-dir "$S/draft/b1" --work "$S/w/d1m"
    show d1 ;;
d2) runv "$S/v2/d2_intact.py" d2.intact --only XO1 --battery-dir "$S/draft/b2" --work "$S/w/d2i"
    runv "$S/v2/d2_mut.py"    d2.mut    --only XO1 --battery-dir "$S/draft/b2" --work "$S/w/d2m"
    show d2 ;;
d3) runv "$S/v2/d3_intact.py" d3.intact --only XO6 --battery-dir "$S/draft/b3" --work "$S/w/d3i"
    runv "$S/v2/d3_mut.py"    d3.mut    --only XO6 --battery-dir "$S/draft/b3" --work "$S/w/d3m"
    show d3 ;;
d4) runv "$S/v2/d4_intact.py" d4.intact --only ERR1 --battery-dir "$S/draft/b4" --work "$S/w/d4i"
    runv "$S/v2/d4_mut.py"    d4.mut    --only ERR1 --battery-dir "$S/draft/b4" --work "$S/w/d4m"
    show d4 ;;
d5) runv "$S/v2/d5_intact.py" d5.intact --only X7 --battery-dir "$S/draft/b5" --work "$S/w/d5i"
    runv "$S/v2/d5_mut.py"    d5.mut    --only X7 --battery-dir "$S/draft/b5" --work "$S/w/d5m"
    show d5 ;;
d6) runv "$S/v2/d6_intact.py" d6.intact --battery-dir "$S/draft/b6" --work "$S/w/d6i"
    runv "$S/v2/d6_mut.py"    d6.mut    --battery-dir "$S/draft/b6" --work "$S/w/d6m"
    show d6 ;;
d8) DRAFT_CWD="$S/mW" runv "$S/v2/d8_intact.py" d8.intact --work "$S/w/d8i"
    DRAFT_CWD="$S/mW" runv "$S/v2/d8_mut.py"    d8.mut    --work "$S/w/d8m"
    show d8 ;;
d11) runv "$S/v2/d11_intact.py" d11.intact --only TR1 --battery-dir "$S/draft/b11" --work "$S/w/d11i"
     runv "$S/v2/d11_mut.py"    d11.mut    --only TR1 --battery-dir "$S/draft/b11" --work "$S/w/d11m"
     show d11 ;;
d14) runv "$S/v2/d14_intact.py" d14.intact --battery-dir "$S/draft/b14" --work "$S/w/d14i"
     runv "$S/v2/d14_mut.py"    d14.mut    --battery-dir "$S/draft/b14" --work "$S/w/d14m"
     show d14 ;;
d15) runv "$S/v2/d15_intact.py" d15.intact --battery-dir "$S/draft/b15" --work "$S/w/d15i"
     runv "$S/v2/d15_mut.py"    d15.mut    --battery-dir "$S/draft/b15" --work "$S/w/d15m"
     show d15 ;;
d20) runv "$S/c/pristine.py"  d20.intact --only X1 --battery-dir "$S/draft/wdir" --work "$S/w/d20i"
     runv "$S/v/CM20_W.py"    d20.mut    --only X1 --battery-dir "$S/draft/wdir" --work "$S/w/d20m"
     show d20 ;;
d9)
  rm -rf "$S/mP"; mkdir -p "$S/mP"; cp -a "$S/mW/." "$S/mP/"
  ( sleep 2; printf '# midrun edit (draft control D9)\n' >> "$S/mP/plans/anchor_digest_check.py" ) & EP=$!
  DRAFT_CWD="$S/mP" runv "$S/c/pristine.py" d9.intact --work "$S/w/d9i" --jobs 1
  wait "$EP" 2>/dev/null || true
  cp -f "$S/mW/plans/anchor_digest_check.py" "$S/mP/plans/anchor_digest_check.py"
  ( sleep 2; printf '# midrun edit (draft control D9)\n' >> "$S/mP/plans/anchor_digest_check.py" ) & EP=$!
  DRAFT_CWD="$S/mP" runv "$S/v/CM18_W.py" d9.mut --work "$S/w/d9m" --jobs 1
  wait "$EP" 2>/dev/null || true
  show d9 ;;
*) for d in d1 d2 d3 d4 d5 d6 d8 d11 d14 d15 d20; do bash "$0" "$d"; done ;;
esac

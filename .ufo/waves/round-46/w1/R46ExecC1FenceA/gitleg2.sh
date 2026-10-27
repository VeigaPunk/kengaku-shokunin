set -u
R="$1"
export HOME=/nonexistent GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
cd "$R" || exit 9
for leg in "rev-parse --show-toplevel" "rev-parse --git-common-dir"; do
  out=$(strace -f -qq -y -e trace=%file -o /tmp/gl2.$$ git $leg 2>&1)
  rc=$?
  anc=$(grep -o "\"/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceA/layout[^\"]*\"" /tmp/gl2.$$ | sort -u | tr '\n' ' ')
  echo "CDLEG [$leg] rc=$rc out=${out:-<none>} anc_stats=${anc:-none}"
done

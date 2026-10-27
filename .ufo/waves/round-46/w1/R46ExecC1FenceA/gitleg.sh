set -u
R="$1"
export HOME=/nonexistent GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
for leg in "rev-parse --show-toplevel" "rev-parse --absolute-git-dir" "rev-parse --git-common-dir" "cat-file -t HEAD:plans/x.md"; do
  out=$(strace -f -qq -y -e trace=%file -o /tmp/gl.$$ git -C "$R" $leg 2>/tmp/gl.err)
  rc=$?
  n=$(grep -c "R46ExecC1FenceA/layout\|R46ExecC1FenceA/layout/repo>" /tmp/gl.$$ || true)
  anc=$(grep -o "\"/fast/scratch/hyaku/kengaku-r46/R46ExecC1FenceA/layout[^\"]*\"" /tmp/gl.$$ | sort -u | tr '\n' ' ')
  echo "LEG [$leg] rc=$rc out=${out:-<none>} anc_stats=${anc:-none}"
done

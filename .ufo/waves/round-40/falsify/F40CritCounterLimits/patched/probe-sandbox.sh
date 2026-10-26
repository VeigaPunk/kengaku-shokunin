#!/bin/bash
# Measures the patched sandbox()'s write surface from the patched counter's own argv, inside the round-40
# HOST-SAFETY wrapper. Prints the argv it used and one line per attempted write.
set -u
S=/fast/scratch/hyaku/kengaku-r40/F40CritCounterLimits
ROOT="$S/probe-root"; mkdir -p "$ROOT"
ARGV=$(cd "$S/lane/plans" && python3 -c '
import importlib.util, sys, pathlib
spec = importlib.util.spec_from_file_location("c1", "c1_patched.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print("\n".join(m.sandbox(write_root=pathlib.Path(sys.argv[1]))))' "$ROOT")
mapfile -t AV <<< "$ARGV"
echo "# argv: ${AV[*]}"
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
      bash -c 'exec "$@"' _ "${AV[@]}" bash -c '
for p in "$HOME/.local/bin/zz" /usr/zz /etc/zz "$HOME/.ssh/zz" /fast/scratch/hyaku/kengaku-r40/F40CritCounterLimits/zz; do
  if ( echo x > "$p" ) 2>/dev/null; then echo "WRITE ok   $p"; rm -f "$p"; else echo "WRITE denied $p"; fi
done
( echo x > "'"$ROOT"'/zz" ) 2>/dev/null && echo "WRITE ok   <run root>/zz" || echo "WRITE denied <run root>/zz"
python3 -c "import socket;s=socket.create_connection((\"1.1.1.1\",443),2)" 2>&1 | tail -1'
echo "EXIT=$?"

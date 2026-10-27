set -u
echo "== scratch_guard unreadable sentinel"
d=$(mktemp -d -p "$TMPDIR" gXXXX); : > "$d/.ROUND-ROOT-SENTINEL"; chmod 000 "$d/.ROUND-ROOT-SENTINEL"
python3 "$LANE/plans/scratch_guard.py" check "$d" 2>&1 | tail -1; echo "rc=$?"
python3 "$LANE/plans/scratch_guard.py" check "$d" >/dev/null 2>&1; echo "rc_direct=$?"
chmod 644 "$d/.ROUND-ROOT-SENTINEL"; rm -rf -- "$d"
echo "== selftest tail"
python3 "$LANE/plans/scratch_guard.py" --selftest 2>&1 | tail -2
echo "== git_leak_probe absent --work"
d2=$(mktemp -d -p "$TMPDIR" hXXXX)
python3 "$LANE/plans/git_leak_probe.py" --lane "$LANE" --work "$d2/absent" >"$TMPDIR/glp.out" 2>&1; echo "rc=$?"; tail -2 "$TMPDIR/glp.out"
rm -rf -- "$d2"

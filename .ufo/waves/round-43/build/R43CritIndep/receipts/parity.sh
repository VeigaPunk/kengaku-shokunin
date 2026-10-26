#!/usr/bin/env bash
# R43CritIndep: real-pytest parity for the tb2 feal grader's exit-status mapping.
# Runs the captured grader under pytest==8.4.1 with /app and /tests bound into a bwrap sandbox
# (same sandbox shape as plans/feal_probe.py: /usr and /etc read-only, private /tmp, cwd /app).
set -u
S=/fast/scratch/hyaku/kengaku-r43/R43CritIndep
CAP=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round43/tb2-feal-differential-cryptanalysis
P="$S/parity"
rm -rf "$P"
mkdir -p "$P/app" "$P/tests"
cp "$CAP/feal.py" "$P/app/feal.py"
for f in test_outputs.py setup.py feal_module.c feal.c feal.h; do cp "$CAP/$f" "$P/tests/$f"; done

run_case() {
  local name=$1 atk=$2
  rm -f "$P/app/attack.py"
  if [ "$atk" != "-" ]; then cp "$S/atk/$atk" "$P/app/attack.py"; fi
  env -i PATH=/venv/bin:/usr/bin:/bin HOME=/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUTF8=1 \
    /usr/bin/bwrap --unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session \
      --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/bin /sbin \
      --symlink usr/lib /lib --symlink usr/lib /lib64 \
      --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp \
      --bind "$P/app" /app --bind "$P/tests" /tests --ro-bind "$S/venv" /venv \
      --chdir /app /venv/bin/python -m pytest /tests/test_outputs.py -v -rA \
      >"$S/parity-$name.log" 2>&1
  local rc=$?
  echo "PARITY case=$name pytest_rc=$rc reward=$([ "$rc" -eq 0 ] && echo 1 || echo 0)"
  grep -E 'PASSED|FAILED|passed|failed|SystemExit|Error' "$S/parity-$name.log" | tail -4
}

run_case cheat-always-equal a_always_equal.py
run_case wrong-key a_wrong_key.py
run_case cheat-exit-zero a_exit_zero.py
run_case x-system-exit a_system_exit.py
run_case x-rekey-then-get a_rekey.py

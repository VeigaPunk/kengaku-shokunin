#!/usr/bin/env bash
# R43CritIndep: instrumented path-order probe (not one of the three scored extra cases).
# (a) dump sys.path as the grader sees it just before test_outputs.py:25 imports feal_in_c;
# (b) run the path-precedence shadow shape (/app/feal_in_c.py before /tests' real extension) under pytest.
set -u
S=/fast/scratch/hyaku/kengaku-r43/R43CritIndep
CAP=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round43/tb2-feal-differential-cryptanalysis
P="$S/parity"
rm -rf "$P"
mkdir -p "$P/app" "$P/tests"
cp "$CAP/feal.py" "$P/app/feal.py"
for f in test_outputs.py setup.py feal_module.c feal.c feal.h; do cp "$CAP/$f" "$P/tests/$f"; done

SB=(/usr/bin/bwrap --unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session
    --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/bin /sbin
    --symlink usr/lib /lib --symlink usr/lib /lib64
    --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp
    --bind "$P/app" /app --bind "$P/tests" /tests --ro-bind "$S/venv" /venv --chdir /app)

pytest_run() {
  local name=$1
  env -i PATH=/venv/bin:/usr/bin:/bin HOME=/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUTF8=1 \
    "${SB[@]}" /venv/bin/python -m pytest /tests/test_outputs.py -v -rA >"$S/parity3-$name.log" 2>&1
  local rc=$?
  echo "PATHORDER case=$name pytest_rc=$rc reward=$([ "$rc" -eq 0 ] && echo 1 || echo 0)"
  grep -E 'PASSED|FAILED|passed in|failed in' "$S/parity3-$name.log" | tail -2
}

rm -f "$P/app/attack.py" "$P/app/feal_in_c.py" "$P/app/syspath.txt"
cp "$S/atk/dump_syspath.py" "$P/app/attack.py"
pytest_run syspath-dump
echo "SYSPATH-AT-IMPORT"
cat -n "$P/app/syspath.txt"

rm -f "$P/app/attack.py" "$P/app/feal_in_c.py"
cp "$S/atk/fake_module_attack.py" "$P/app/attack.py"
cp "$S/atk/feal_in_c.py" "$P/app/feal_in_c.py"
pytest_run app-module-shadow
grep -E 'test_outputs.py:[0-9]+' "$S/parity3-app-module-shadow.log" | tail -3

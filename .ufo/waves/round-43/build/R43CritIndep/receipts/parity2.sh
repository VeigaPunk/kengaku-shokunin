#!/usr/bin/env bash
# R43CritIndep: real-pytest parity over the 12 frozen C2 cases (minus the shapes already run in parity.sh).
# Same sandbox shape as plans/feal_probe.py; the recipe runs in its own bwrap pass with cwd /app.
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
    --bind "$P/app" /app --bind "$P/tests" /tests --ro-bind "$S/venv" /venv
    --ro-bind "$CAP/solve.sh" /cap/solve.sh
    --ro-bind "$S/recipe.sh" /recipe.sh --chdir /app)

pytest_run() {
  local name=$1
  env -i PATH=/venv/bin:/usr/bin:/bin HOME=/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUTF8=1 \
    "${SB[@]}" /venv/bin/python -m pytest /tests/test_outputs.py -v -rA >"$S/parity2-$name.log" 2>&1
  local rc=$?
  echo "PARITY case=$name pytest_rc=$rc reward=$([ "$rc" -eq 0 ] && echo 1 || echo 0)"
  grep -E 'PASSED|FAILED|passed in|failed in|SystemExit' "$S/parity2-$name.log" | tail -3
}

recipe_run() {  # name, recipe body file
  local name=$1 body=$2
  cp "$body" "$S/recipe.sh"
  rm -f "$P/app/attack.py"
  env -i PATH=/venv/bin:/usr/bin:/bin HOME=/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUTF8=1 \
    "${SB[@]}" /usr/bin/bash -euo pipefail /recipe.sh >"$S/recipe2-$name.log" 2>&1
  echo "RECIPE case=$name rc=$?"
  pytest_run "$name"
}

attack_run() {  # name, attack file or -
  local name=$1 atk=$2
  rm -f "$P/app/attack.py"
  if [ "$atk" != "-" ]; then cp "$S/atk/$atk" "$P/app/attack.py"; fi
  pytest_run "$name"
}

attack_run nop -
recipe_run oracle-solve-sh "$S/rec/solve_only.sh"
recipe_run oracle-off-by-one "$S/rec/off_by_one.sh"
recipe_run return-str "$S/rec/return_str.sh"
attack_run cheat-import-get_keys import_get_keys.py
attack_run cheat-sysmodules-shadow sysmodules_shadow.py
attack_run cheat-patch-get_keys patch_get_keys.py
attack_run cheat-clock-seed clock_seed.py
recipe_run slow-oracle-45s "$S/rec/slow.sh"

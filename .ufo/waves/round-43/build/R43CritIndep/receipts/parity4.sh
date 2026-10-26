#!/usr/bin/env bash
# R43CritIndep: instrumented divergence probe (not a scored case).
# The SAME end state that failed under pytest (/app/feal_in_c.py + attack() returning 6) is graded by the frozen
# probe's own harness body (extracted byte-identically from plans/feal_probe.py via the scratch copy's HARNESS_PY),
# to see whether the probe's harness maps it to the grader's verdict.
set -u
S=/fast/scratch/hyaku/kengaku-r43/R43CritIndep
CAP=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round43/tb2-feal-differential-cryptanalysis
P="$S/parity"
rm -rf "$P"
mkdir -p "$P/app" "$P/tests"
cp "$CAP/feal.py" "$P/app/feal.py"
for f in test_outputs.py setup.py feal_module.c feal.c feal.h; do cp "$CAP/$f" "$P/tests/$f"; done
cp "$S/atk/fake_module_attack.py" "$P/app/attack.py"
cp "$S/atk/feal_in_c.py" "$P/app/feal_in_c.py"
/usr/bin/python3 -c "import sys; sys.path.insert(0, '$S'); import feal_probe_copy as p; open('$S/harness2.py', 'w').write(p.HARNESS_PY)"
sha256sum "$S/harness2.py"

env -i PATH=/venv/bin:/usr/bin:/bin HOME=/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUTF8=1 \
  /usr/bin/bwrap --unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session \
    --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/bin /sbin \
    --symlink usr/lib /lib --symlink usr/lib /lib64 \
    --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp \
    --bind "$P/app" /app --bind "$P/tests" /tests --ro-bind "$S/venv" /venv \
    --ro-bind "$S/harness2.py" /harness2.py --chdir /app \
    /venv/bin/python /harness2.py grade
echo "PROBEHARNESS case=app-module-shadow rc=$? -> P iff rc=0 (test_outputs.py:25 resolves feal_in_c)"

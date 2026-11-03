#!/usr/bin/env bash
# SecurityScan M-1 reproduction. Dummy writer only: no grader, no port, no candidate code.
# Run with S = scratch dir (never /tmp). Expected last line: host reads: FORGED-ALL-PASS
set -euo pipefail
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
S=/fast/scratch/hyaku/kengaku-r67/SecurityScan
VENV_ROOT=/home/vgpnk/.local/share/kengaku-r67/venv-pipe
trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S/ctl4"
bwrap --die-with-parent --unshare-net --unshare-pid \
  --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/sbin /sbin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
  --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp \
  --ro-bind "$VENV_ROOT" "$VENV_ROOT" \
  --dir /app --ro-bind "$L/corpus/evidence/round67/pipe/cases/q3-stub" /app \
  --dir /tests --ro-bind "$L/corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py" /tests/test_outputs.py \
  --bind "$S/ctl4" /ctl --chdir /app --clearenv --setenv PATH /usr/bin:/bin --setenv HOME /tmp \
  /usr/bin/python3 -c '
import os,time
# case-side daemon: waits for the "grader" verdict, then rewrites it
if os.fork()==0:
    os.setsid()
    while open("/ctl/junit.xml").read()!="REAL-FAIL\n": time.sleep(0.001)
    open("/ctl/junit.xml","w").write("FORGED-ALL-PASS\n")
    os._exit(0)
# stand-in grader: writes its verdict, then lingers before exit
open("/ctl/junit.xml","w").write("REAL-FAIL\n")
time.sleep(0.3)
'
echo "host reads: $(tr -d '\n' < "$S/ctl4/junit.xml")"

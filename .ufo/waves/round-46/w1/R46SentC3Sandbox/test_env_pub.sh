#!/usr/bin/bash
# Adversarial checks for the recommended C3 invocation:
#  (a) what the payload's environment actually is under --clearenv/--setenv (HOME, PATH, count);
#  (b) is /pub (a --dir on the root tmpfs) writable after --remount-ro / ?
#  (c) is /tests (a --ro-bind) writable after --remount-ro / ?
set -u
B=/usr/bin/bwrap
W=$1
argv=("$B" --unshare-all --die-with-parent --new-session --hostname k46sent --ro-bind /usr /usr)
for l in /bin /sbin /lib /lib64; do [ -L "$l" ] && argv+=(--symlink "$(readlink "$l")" "$l"); done
argv+=(--ro-bind /etc /etc --proc /proc --dev /dev --size 8388608 --tmpfs /tmp --size 8388608 --tmpfs /app
       --ro-bind "$W/tests" /tests --dir /pub --ro-bind "$W/tests/f.txt" /pub/f.txt
       --clearenv
       --setenv PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
       --setenv HOME /tmp --setenv TMPDIR /tmp --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
       --setenv PYTHONUTF8 1 --setenv PYTHONDONTWRITEBYTECODE 1
       --remount-ro / --chdir /app /usr/bin/python3 -c '
import os
print("ENV HOME=%r TMPDIR=%r PATH_head=%r n=%d" % (os.environ.get("HOME"), os.environ.get("TMPDIR"),
      os.environ.get("PATH", "").split(":")[0], len(os.environ)))
for p in ("/pub/planted.txt", "/pub/f.txt", "/tests/planted.txt", "/tests/f.txt", "/tmp/ok.txt"):
    try:
        os.close(os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)); print("WOK", p)
    except OSError as e:
        print("WNO", p, e.errno, e.strerror)
')
prlimit --nproc=48 --cpu=20 --fsize=1048576 --core=0 --as=536870912 --nofile=512 -- "${argv[@]}"
echo "RC $?"

#!/usr/bin/bash
# Two bwrap-invocation questions for the C3 probe, measured in one run:
#  (1) does `--size N --tmpfs DEST` cap DEST (write 16 MiB into an 8 MiB tmpfs)?
#  (2) does `--remount-ro /` close the writable root tmpfs while leaving /tmp and /app writable?
set -u
BWRAP=/usr/bin/bwrap
BASE=("$BWRAP" --unshare-net --unshare-pid --unshare-ipc --unshare-uts --hostname k46sent
      --die-with-parent --new-session --ro-bind /usr /usr)
for link in /bin /sbin /lib /lib64; do
  [ -L "$link" ] && BASE+=(--symlink "$(readlink "$link")" "$link")
done
BASE+=(--ro-bind /etc /etc --proc /proc --dev /dev --size 8388608 --tmpfs /tmp
       --size 8388608 --tmpfs /app)

probe='
import errno, os
def w(path, n):
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    except OSError as e:
        print("W", path, "open-fail", e.errno, e.strerror); return
    written = 0
    try:
        while written < n:
            written += os.write(fd, b"x" * 65536)
    except OSError as e:
        print("W", path, "stop", e.errno, e.strerror, "written", written)
    else:
        print("W", path, "ok", written)
    finally:
        os.close(fd)
w("/ESCAPE-root.txt", 2048)
w("/tmp/fill.bin", 16 << 20)
w("/app/fill.bin", 16 << 20)
'

for mode in no-remount remount-ro-root; do
  argv=("${BASE[@]}")
  if [ "$mode" = remount-ro-root ]; then argv+=(--remount-ro /); fi
  argv+=(--chdir /app /usr/bin/python3 -c "$probe")
  echo "== MODE $mode"
  /usr/bin/prlimit --nproc=48 --cpu=20 --fsize=67108864 --core=0 --as=1073741824 -- "${argv[@]}" 2>&1
  echo "== RC $?"
done

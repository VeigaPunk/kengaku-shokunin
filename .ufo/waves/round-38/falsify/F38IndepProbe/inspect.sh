set -eu
R="$1"; C="$2"; CMD="$3"
mount --bind /usr "$R/usr"; mount --bind /etc "$R/etc"; mount --bind /dev "$R/dev"
mount -t proc proc "$R/proc"
mount --bind "$C/app" "$R/app"; mount --bind "$C/ulb" "$R/usr/local/bin"; mount --bind "$C/ulsb" "$R/usr/local/sbin"
mount --bind "$C/test_outputs.py" "$R/tests/test_outputs.py"
exec chroot "$R" /usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/tmp /bin/sh -c "cd /app && $CMD"

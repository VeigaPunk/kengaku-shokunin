# trace-full.log analysis (strace -f -v -s 8000, 6119718 bytes)

## bwrap / process
bwrap execve count: 23
sandboxed /usr/bin/bash execve count: 9
python3 execve count (driver + sandboxed): 17
execve lines containing SENTINEL_CANARY_R95: 107

## socket families observed in whole tree (driver + sandbox)
AF_NETLINK: 23
AF_UNIX: 23
socketpair calls: 0

## unshare calls

## write-mode openat: unique sandbox-view paths (NOT under scratch S)
./sed0VxQM5  x1  last=4
./sed1S4cEM  x1  last=4
./sed6FiYls  x1  last=4
./sed7bEplI  x1  last=4
./sedBVsmK3  x1  last=4
./sedDRj4Oh  x1  last=4
./sedKGKj7i  x1  last=4
./sedVsD2mr  x1  last=4
./sedZUFrLu  x1  last=4
./sedZe9YM2  x1  last=4
./seddyFEgj  x1  last=4
./sedgHyZGO  x1  last=4
./sedmNJ35l  x1  last=4
./sedqAXPMB  x1  last=4
./sedrrsiYq  x1  last=4
./seduLJVrc  x1  last=4
/app/report.jsonl  x8  last=3
/dev/null  x1  last=3
/dev/tty  x9  last=-1 ENXIO (No such device or address)
full  x23  last=5
gid_map  x46  last=6
harness.py  x15  last=5
null  x23  last=5
random  x23  last=5
setgroups  x23  last=6
solve.sh  x8  last=5
tty  x23  last=5
uid_map  x46  last=6
urandom  x23  last=5
zero  x23  last=5

## write-mode openat: unique driver-view paths under S (aggregated by top dirs)
/fast/scratch/hyaku/kengaku-r95/SentinelProbe/work  x52

write-mode openat total: 362
EROFS results on write opens: 0

## lines mentioning /home/vgpnk/Projects (fleet tree): 7
4048942 newfstatat(AT_FDCWD, "/home/vgpnk/Projects", {st_dev=makedev(0, 0x38), st_ino=27238, st_mode=S_IFDIR|0755, st_nlink=1, st_uid=1000, st_gid=1000, st_blksize=4096, st_blocks=0, st_size=1244, st_
4048942 newfstatat(AT_FDCWD, "/home/vgpnk/Projects/shokunin", {st_dev=makedev(0, 0x38), st_ino=9655549, st_mode=S_IFDIR|0755, st_nlink=1, st_uid=1000, st_gid=1000, st_blksize=4096, st_blocks=0, st_siz
4048942 newfstatat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/kengaku-shokunin", {st_dev=makedev(0, 0x38), st_ino=9823272, st_mode=S_IFDIR|0755, st_nlink=1, st_uid=1000, st_gid=1000, st_blksize=4096, st
4048942 newfstatat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.git", {st_dev=makedev(0, 0x38), st_ino=9823273, st_mode=S_IFDIR|0755, st_nlink=1, st_uid=1000, st_gid=1000, st_blksize=409
4048942 newfstatat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.git/objects", {st_dev=makedev(0, 0x38), st_ino=9823298, st_mode=S_IFDIR|0755, st_nlink=1, st_uid=1000, st_gid=1000, st_blk
4048942 newfstatat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.git/objects", {st_dev=makedev(0, 0x38), st_ino=9823298, st_mode=S_IFDIR|0755, st_nlink=1, st_uid=1000, st_gid=1000, st_blk
4048942 openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.git/objects/info/alternates", O_RDONLY) = -1 ENOENT (No such file or directory)


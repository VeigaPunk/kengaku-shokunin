#!/usr/bin/env bash
# R45LabratGitAPIs probe round 13: which filesystem operations count as an "open" under the counter's rule?
# (reproduced into the receipt directory after the scratch tree was removed; run under claims/envelope.sh)
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe13
rm -rf "$P"; mkdir -p "$P"; cd "$P" || exit 1
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null HOME=/nonexistent
hr() { printf '\n===== %s =====\n' "$*"; }
trace() { local l=$1; shift; printf -- '--- %s\n' "$l"
  local log="$P/s.$$.$RANDOM.log"
  strace -f -qq -y -e trace=open,openat,openat2,creat,newfstatat,statx,readlink,readlinkat,getdents64 -o "$log" "$@" >/dev/null 2>&1
  printf '[rc=%s]\n' "$?"
  sed 's/^/    /' "$log"
  rm -f "$log"; }
mkdir -p "$P/d"; printf 'x\n' > "$P/d/file.txt"; printf 'y\n' > "$P/outside.txt"

hr "A1  os.stat on a path OUTSIDE d"
trace "a1 python os.stat(outside.txt) + os.stat(outside/.git)" \
  python3 -c "import os,sys; print(os.path.exists(sys.argv[1]), os.path.isdir(sys.argv[2]))" "$P/outside.txt" "$P/nosuch"

hr "A2  pathlib.Path.read_text on a path OUTSIDE d"
trace "a2 python read_text(outside.txt)" python3 -c "import pathlib,sys; print(len(pathlib.Path(sys.argv[1]).read_text()))" "$P/outside.txt"

hr "A3  os.listdir / os.scandir on a directory OUTSIDE d"
trace "a3 python os.listdir(outside dir)" python3 -c "import os,sys; print(os.listdir(sys.argv[1]))" "$P"

hr "A4  os.walk over d (inside d) -- which dirs get opened?"
trace "a4 python os.walk(d)" python3 -c "
import os,sys
for top,dirs,files in os.walk(sys.argv[1]): pass
print('walked')" "$P/d"

hr "A5  Path.resolve() on a path outside d (symlink resolution)"
trace "a5 python Path.resolve(outside)" python3 -c "import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve())" "$P/outside.txt"

hr "A6  os.path.islink on a symlink pointing outside d"
ln -sfn "$P/outside.txt" "$P/d/link-out"
trace "a6 python islink(d/link-out) + resolve()" python3 -c "
import os,pathlib,sys
p=sys.argv[1]
print(os.path.islink(p), pathlib.Path(p).resolve())" "$P/d/link-out"

hr "DONE"

#!/usr/bin/env bash
# R45LabratGitAPIs probe round 9: symlinked .git, relative core.worktree base, config.worktree without the extension.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe9
rm -rf "$P"; mkdir -p "$P"; cd "$P" || exit 1
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null HOME=/nonexistent
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@example.invalid
export GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@example.invalid
export GIT_CONFIG_COUNT=4 GIT_CONFIG_KEY_0=core.fsmonitor GIT_CONFIG_VALUE_0=false \
       GIT_CONFIG_KEY_1=core.hooksPath GIT_CONFIG_VALUE_1=/dev/null \
       GIT_CONFIG_KEY_2=gpg.program GIT_CONFIG_VALUE_2=/bin/true \
       GIT_CONFIG_KEY_3=log.showSignature GIT_CONFIG_VALUE_3=false
hr() { printf '\n===== %s =====\n' "$*"; }
run() { local l=$1; shift; printf -- '--- %s\n' "$l"; "$@" 2>&1; printf '[rc=%s]\n' "$?"; }
fired() { local l=$1 n=$2; shift 2; printf -- '--- %s\n' "$l"
  local log="$P/s.$$.$RANDOM.log"
  strace -f -qq -y -e trace=open,openat,openat2,creat -o "$log" "$@" >/dev/null 2>&1
  if grep -F -- "$n" "$log" >/dev/null; then printf '  OPENED the outside path\n'; else printf '  not opened\n'; fi
  rm -f "$log"; }
mkrepo() { mkdir -p "$1"; git -C "$1" init -q -b master . >/dev/null 2>&1
  printf 'x\n' > "$1/file.txt"; git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm one >/dev/null 2>&1; }

hr "W1  .git is a SYMLINK to an outside git dir"
W1=$P/w1; mkdir -p "$W1"; mkrepo "$W1/store"
mkdir -p "$W1/d"; ln -s "$W1/store/.git" "$W1/d/.git"
run "w1 ls -ld .git" ls -ld "$W1/d/.git"
run "w1 rev-parse --absolute-git-dir" git -C "$W1/d" rev-parse --absolute-git-dir
run "w1 rev-parse --show-toplevel" git -C "$W1/d" rev-parse --show-toplevel
fired "w1 does a git probe open the outside store config?" "$W1/store/.git/config" git -C "$W1/d" rev-parse --show-toplevel
run "w1 python: os.path.isdir(.git) is True, os.path.islink(.git) is True" python3 -c \
  "import os,sys; p=sys.argv[1]; print('isdir', os.path.isdir(p), 'islink', os.path.islink(p))" "$W1/d/.git"

hr "W2  relative core.worktree : resolved against the GIT DIR or the WORK TREE?"
W2=$P/w2; mkdir -p "$W2"; mkrepo "$W2/d"
mkdir -p "$W2/d/wt"; mkdir -p "$W2/wt"
git -C "$W2/d" config core.worktree "wt"
run "w2 --show-toplevel" git -C "$W2/d" rev-parse --show-toplevel
run "w2 --absolute-git-dir" git -C "$W2/d" rev-parse --absolute-git-dir
run "w2 config --local --no-includes --get core.worktree" git -C "$W2/d" config --local --no-includes --get core.worktree
W2B=$P/w2b; mkdir -p "$W2B"; mkrepo "$W2B/d"; mkdir -p "$W2B/d/wt"; mkdir -p "$W2B/wt"
git -C "$W2B/d" config core.worktree "../wt"
run "w2b --show-toplevel (../wt)" git -C "$W2B/d" rev-parse --show-toplevel
run "w2b --absolute-git-dir" git -C "$W2B/d" rev-parse --absolute-git-dir

hr "W3  .git/config.worktree present but extensions.worktreeConfig NOT set"
W3=$P/w3; mkdir -p "$W3"; mkrepo "$W3/d"
printf '[include]\n\tpath = %s\n' "$W3/out.cfg" > "$W3/d/.git/config.worktree"
printf '[user]\n\temail = OUTSIDE-W3@invalid\n' > "$W3/out.cfg"
run "w3 config --list --show-origin" git -C "$W3/d" config --list --show-origin
fired "w3 does a git probe open the worktree-config target?" "$W3/out.cfg" git -C "$W3/d" rev-parse --show-toplevel
run "w3 config --worktree --get-regexp include (without the extension)" git -C "$W3/d" config --worktree --get-regexp '^include(if)?\.'
W3B=$P/w3b; mkdir -p "$W3B"; mkrepo "$W3B/d"
git -C "$W3B/d" config extensions.worktreeConfig true
run "w3b extension set, NO config.worktree file: config --list --show-origin" git -C "$W3B/d" config --list --show-origin
fired "w3b does a probe open a nonexistent worktree config?" "$W3B/d/.git/config.worktree" git -C "$W3B/d" rev-parse --show-toplevel

hr "W4  text scan vs git: does a pure read of .git/config* ever open an outside file?"
W4=$P/w4; mkdir -p "$W4"; mkrepo "$W4/d"
printf '[include]\n\tpath = %s\n' "$W4/out.cfg" >> "$W4/d/.git/config"
printf '[user]\n\temail = OUTSIDE-W4@invalid\n' > "$W4/out.cfg"
fired "w4 python text scan of .git/config" "$W4/out.cfg" python3 -c \
  "import sys,pathlib; t=pathlib.Path(sys.argv[1]).read_text(); print('include' in t)" "$W4/d/.git/config"

hr "W5  is a repo's own .git/config read by any git call? (i.e. is the repo's config inside d?)"
W5=$P/w5; mkdir -p "$W5"; mkrepo "$W5/d"
fired "w5 rev-parse opens the repo's own .git/config (inside d)" "$W5/d/.git/config" git -C "$W5/d" rev-parse --show-toplevel

hr "DONE"

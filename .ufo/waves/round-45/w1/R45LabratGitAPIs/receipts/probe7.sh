#!/usr/bin/env bash
# R45LabratGitAPIs probe round 7: pin the relative includeIf gitdir base; confirm the f9 detection rule; ceiling forms.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe7
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
  if grep -F -- "$n" "$log" >/dev/null; then printf '  FIRED (target opened)\n'; else printf '  not fired\n'; fi
  rm -f "$log"; }
mkrepo() { mkdir -p "$1"; git -C "$1" init -q -b master . >/dev/null 2>&1
  printf 'x\n' > "$1/file.txt"; git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm one >/dev/null 2>&1; }

hr "U1  relative includeIf gitdir base : --separate-git-dir breaks the worktree/gitdir coincidence"
U1=$P/u1; mkdir -p "$U1"
# work tree at U1/wt/work, git dir at U1/gd/gitdir  (different parents on purpose)
mkdir -p "$U1/wt"; git init -q -b master --separate-git-dir "$U1/gd/gitdir" "$U1/wt/work" >/dev/null 2>&1
printf 'x\n' > "$U1/wt/work/f.txt"; git -C "$U1/wt/work" add -A >/dev/null 2>&1
git -C "$U1/wt/work" commit -qm one >/dev/null 2>&1
run "u1 .git file" cat "$U1/wt/work/.git"
run "u1 --absolute-git-dir" git -C "$U1/wt/work" rev-parse --absolute-git-dir
run "u1 --show-toplevel" git -C "$U1/wt/work" rev-parse --show-toplevel
printf '[user]\n\temail = OUTSIDE-U1@invalid\n' > "$U1/out.cfg"
tryU1() { printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$1" "$U1/out.cfg" >> "$U1/gd/gitdir/config"
  printf -- '--- pattern "%s"\n' "$1"
  fired "u1 probe" "$U1/out.cfg" git -C "$U1/wt/work" rev-parse --show-toplevel; }
tryU1 "wt/work/.git"          # relative to U1 (parent of the work tree's parent?)
tryU1 "work/.git"             # relative to U1/wt (parent of the work tree)
tryU1 "gd/gitdir"             # relative to U1 (parent of the git dir)
tryU1 "gitdir"                # relative to U1/gd (parent of the git dir)

hr "U2  f9 detection rule : bare repo vs empty .git dir (both 'git cannot describe')"
U2=$P/u2; mkdir -p "$U2"; mkrepo "$U2/bare"; git -C "$U2/bare" config core.bare true
mkdir -p "$U2/empty/.git"
for t in bare empty; do
  printf -- '--- %s\n' "$t"
  run "u2 $t --absolute-git-dir" git -C "$U2/$t" rev-parse --absolute-git-dir
  run "u2 $t --show-toplevel" git -C "$U2/$t" rev-parse --show-toplevel
  run "u2 $t --git-common-dir" git -C "$U2/$t" rev-parse --git-common-dir
  run "u2 $t --is-inside-work-tree" git -C "$U2/$t" rev-parse --is-inside-work-tree
  run "u2 $t config --local --no-includes --get-regexp include" git -C "$U2/$t" config --local --no-includes --get-regexp '^include(if)?\.'
done

hr "U3  ceiling must be ABSOLUTE"
U3=$P/u3; mkdir -p "$U3"; mkrepo "$U3/P"; mkdir -p "$U3/P/sub/d"
printf '[run] relative ceiling "P" from cwd U3/P/sub/d\n'
( cd "$U3/P/sub/d" && GIT_CEILING_DIRECTORIES="P" git rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?" )
printf '[run] absolute ceiling U3/P/sub (d.parent)\n'
GIT_CEILING_DIRECTORIES="$U3/P/sub" git -C "$U3/P/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] absolute ceiling U3/P (the repo root)\n'
GIT_CEILING_DIRECTORIES="$U3/P" git -C "$U3/P/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"

hr "U4  --local --no-includes : what it LISTS vs what it OPENS (a worktree-scoped include)"
U4=$P/u4; mkdir -p "$U4"; mkrepo "$U4/d"
printf '[include]\n\tpath = %s\n' "$U4/out.cfg" > "$U4/d/.git/config.worktree"
printf '[user]\n\temail = OUTSIDE-U4@invalid\n' > "$U4/out.cfg"
git -C "$U4/d" config extensions.worktreeConfig true
run "u4 --local --no-includes --get-regexp include" git -C "$U4/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "u4 --worktree --no-includes --get-regexp include" git -C "$U4/d" config --worktree --no-includes --get-regexp '^include(if)?\.'
run "u4 --list --show-origin (which config files are read?)" git -C "$U4/d" config --list --show-origin

hr "DONE"

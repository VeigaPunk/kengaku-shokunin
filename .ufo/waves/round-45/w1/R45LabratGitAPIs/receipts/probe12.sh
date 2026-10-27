#!/usr/bin/env bash
# R45LabratGitAPIs probe round 12: linked-worktree commondir layout; does the fence's own cwd matter.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe12
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
mkrepo() { mkdir -p "$1"; git -C "$1" init -q -b master . >/dev/null 2>&1
  printf 'x\n' > "$1/file.txt"; git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm one >/dev/null 2>&1; }

hr "Z1  a LINKED WORKTREE : where does the 'commondir' file live?"
Z1=$P/z1; mkdir -p "$Z1"; mkrepo "$Z1/main"
git -C "$Z1/main" worktree add -q "$Z1/wt" -b side 2>&1 | head -2
run "z1 wt/.git (a FILE)" cat "$Z1/wt/.git"
run "z1 find: every file named commondir under main/.git" find "$Z1/main/.git" -name commondir
run "z1 main/.git/commondir exists?" ls -l "$Z1/main/.git/commondir" 2>&1
run "z1 the worktree's commondir content" cat "$Z1/main/.git/worktrees/wt/commondir" 2>&1
run "z1 wt --git-common-dir" git -C "$Z1/wt" rev-parse --git-common-dir
run "z1 wt --absolute-git-dir" git -C "$Z1/wt" rev-parse --absolute-git-dir

hr "Z2  the fence runs with cwd=d : does a git probe from cwd=d read the LANE repo's config?"
Z2=$P/z2; mkdir -p "$Z2"; mkrepo "$Z2/d/lane"
printf '[include]\n\tpath = %s\n' "$Z2/out.cfg" >> "$Z2/d/lane/.git/config"
printf '[user]\n\temail = OUT@invalid\n' > "$Z2/out.cfg"
run "z2 cwd=d, git -C d/lane rev-parse" git -C "$Z2/d/lane" rev-parse --show-toplevel
run "z2 cwd=d, git -C d rev-parse (d is not a repo)" git -C "$Z2/d" rev-parse --show-toplevel

hr "Z3  does 'git config --local --no-includes' LIST an [includeIf] section in .git/config ?"
Z3=$P/z3; mkdir -p "$Z3"; mkrepo "$Z3/d"
printf '[includeIf "gitdir:%s/d/.git"]\n\tpath = %s\n' "$Z3" "$Z3/out.cfg" >> "$Z3/d/.git/config"
run "z3 --local --no-includes --get-regexp '^include(if)?\\.'" git -C "$Z3/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "z3 --local --no-includes --get-regexp '^includeif\\.'" git -C "$Z3/d" config --local --no-includes --get-regexp '^includeif\.'
run "z3 --local --no-includes --list" git -C "$Z3/d" config --local --no-includes --list

hr "Z4  what does --no-includes do to the VALUES of the include? (does it still merge them?)"
Z4=$P/z4; mkdir -p "$Z4"; mkrepo "$Z4/d"
printf '[include]\n\tpath = %s\n' "$Z4/out.cfg" >> "$Z4/d/.git/config"
printf '[user]\n\temail = OUTSIDE-Z4@invalid\n' > "$Z4/out.cfg"
run "z4 --local --no-includes --get user.email" git -C "$Z4/d" config --local --no-includes --get user.email
run "z4 --local --get user.email (includes on)" git -C "$Z4/d" config --local --get user.email
run "z4 --get user.email (no scope)" git -C "$Z4/d" config --get user.email

hr "DONE"

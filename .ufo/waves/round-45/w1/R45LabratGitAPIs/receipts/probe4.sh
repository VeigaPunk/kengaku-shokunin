#!/usr/bin/env bash
# R45LabratGitAPIs probe round 4: mechanism probes for the leg design.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe4
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
strun() { local l=$1 n=$2; shift 2; printf -- '--- %s\n' "$l"
  local log="$P/s.$$.$RANDOM.log"
  strace -f -qq -y -e trace=open,openat,openat2,creat -o "$log" "$@" >/dev/null 2>&1
  printf '[rc=%s]\n' "$?"
  if grep -F -- "$n" "$log" >/dev/null 2>&1; then printf 'OPENED %s : YES\n' "$n"
    grep -F -- "$n" "$log" | sed 's/^/    /'; else printf 'OPENED %s : NO\n' "$n"; fi
  rm -f "$log"; }
mkrepo() { mkdir -p "$1"; git -C "$1" init -q -b master . >/dev/null 2>&1
  printf 'x\n' > "$1/file.txt"; git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm one >/dev/null 2>&1; }

hr "R8  f1 shape (.git is a FILE, gitdir: outside) : does a git probe open the OUTSIDE store?"
R8=$P/r8; mkdir -p "$R8"
mkrepo "$R8/store"; mkdir -p "$R8/d"
printf 'gitdir: %s\n' "$R8/store/.git" > "$R8/d/.git"
strun "r8 rev-parse --absolute-git-dir on the redirect repo" "$R8/store/.git/config" git -C "$R8/d" rev-parse --absolute-git-dir
strun "r8 rev-parse --show-toplevel" "$R8/store/.git/config" git -C "$R8/d" rev-parse --show-toplevel
strun "r8 config --local --no-includes --get-regexp include" "$R8/store/.git/config" \
    git -C "$R8/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "r8 rev-parse --git-common-dir" git -C "$R8/d" rev-parse --git-common-dir
run "r8 rev-parse --path-format=absolute --git-common-dir" git -C "$R8/d" rev-parse --path-format=absolute --git-common-dir

hr "R9  f7 shape (.git/commondir -> outside store) : does a git probe open the OUTSIDE store config?"
R9=$P/r9; mkdir -p "$R9"
mkrepo "$R9/store"; mkdir -p "$R9/d/lane/.git"
printf 'ref: refs/heads/master\n' > "$R9/d/lane/.git/HEAD"
printf '%s\n' "$R9/store/.git" > "$R9/d/lane/.git/commondir"
strun "r9 rev-parse --absolute-git-dir" "$R9/store/.git/config" git -C "$R9/d/lane" rev-parse --absolute-git-dir
strun "r9 rev-parse --show-toplevel" "$R9/store/.git/config" git -C "$R9/d/lane" rev-parse --show-toplevel
strun "r9 rev-parse --git-common-dir" "$R9/store/.git/config" git -C "$R9/d/lane" rev-parse --git-common-dir
strun "r9 config --local --no-includes --get-regexp include" "$R9/store/.git/config" \
    git -C "$R9/d/lane" config --local --no-includes --get-regexp '^include(if)?\.'
run "r9 config --local --list --show-origin (whose config?)" git -C "$R9/d/lane" config --local --list --show-origin

hr "R10 relative commondir that ESCAPES d"
R10=$P/r10; mkdir -p "$R10"
mkdir -p "$R10/outside"; git init -q -b master --bare "$R10/outside/store.git" >/dev/null 2>&1
mkdir -p "$R10/d/lane/.git"; printf 'ref: refs/heads/master\n' > "$R10/d/lane/.git/HEAD"
printf '../../outside/store.git\n' > "$R10/d/lane/.git/commondir"
run "r10 commondir" cat "$R10/d/lane/.git/commondir"
run "r10 --git-common-dir" git -C "$R10/d/lane" rev-parse --git-common-dir
run "r10 --absolute-git-dir" git -C "$R10/d/lane" rev-parse --absolute-git-dir
run "r10 --show-toplevel" git -C "$R10/d/lane" rev-parse --show-toplevel
strun "r10 does a probe open the outside store config?" "$R10/outside/store.git/config" \
    git -C "$R10/d/lane" rev-parse --show-toplevel

hr "R11 includeIf gitdir: RELATIVE pattern base (which directory is the base?)"
R11=$P/r11; mkdir -p "$R11"
mkcase() { local nm=$1 pat=$2
  mkdir -p "$R11/$nm"; mkrepo "$R11/$nm/lane"
  printf '[user]\n\temail = OUTSIDE-%s@invalid\n' "$nm" > "$R11/$nm/out.cfg"
  printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$pat" "$R11/$nm/out.cfg" >> "$R11/$nm/lane/.git/config"
  printf -- '--- case %s pattern=%s\n' "$nm" "$pat"
  strun "r11/$nm rev-parse" "$R11/$nm/out.cfg" git -C "$R11/$nm/lane" rev-parse --show-toplevel
}
mkcase p_lane_dotgit "lane/.git"
mkcase p_dot_slash_lane "./lane/.git"
mkcase p_lane "lane"
mkcase p_dotdot_lane "../lane/.git"
mkcase p_lane_slash "lane/"

hr "R12 worktree-scoped include : which git scope SEES it?"
R12=$P/r12; mkdir -p "$R12"; mkrepo "$R12/d"
printf '[include]\n\tpath = %s\n' "$R12/out.cfg" > "$R12/d/.git/config.worktree"
printf '[user]\n\temail = OUTSIDE-R12@invalid\n' > "$R12/out.cfg"
git -C "$R12/d" config extensions.worktreeConfig true
run "r12 --local --no-includes --get-regexp include" git -C "$R12/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "r12 --worktree --no-includes --get-regexp include" git -C "$R12/d" config --worktree --no-includes --get-regexp '^include(if)?\.'
run "r12 --get-regexp include (no scope)" git -C "$R12/d" config --get-regexp '^include(if)?\.'
run "r12 --get-regexp include.path (any scope, includes on)" git -C "$R12/d" config --get-regexp '^include\.path'
run "r12 --list --show-origin" git -C "$R12/d" config --list --show-origin
run "r12 --show-origin --get include.path" git -C "$R12/d" config --show-origin --get include.path

hr "R13 core.worktree : reading it via git can FAIL (relative) ; text scan is reliable"
R13=$P/r13; mkdir -p "$R13"; mkrepo "$R13/d"
git -C "$R13/d" config core.worktree "$R13/outside"
run "r13 --show-toplevel (absolute outside worktree)" git -C "$R13/d" rev-parse --show-toplevel
run "r13 --local --no-includes --get core.worktree" git -C "$R13/d" config --local --no-includes --get core.worktree
run "r13 --absolute-git-dir" git -C "$R13/d" rev-parse --absolute-git-dir
R13B=$P/r13b; mkdir -p "$R13B"; mkrepo "$R13B/d"
git -C "$R13B/d" config core.worktree "../wt"
run "r13b --show-toplevel (relative worktree, missing)" git -C "$R13B/d" rev-parse --show-toplevel
run "r13b --local --no-includes --get core.worktree" git -C "$R13B/d" config --local --no-includes --get core.worktree
run "r13b --absolute-git-dir" git -C "$R13B/d" rev-parse --absolute-git-dir

hr "R14 does the fence-visible repo need a HEAD? (empty .git dir = not a repo)"
R14=$P/r14; mkdir -p "$R14/d/.git" "$R14/d2/.git"
run "r14 empty .git: rev-parse --absolute-git-dir" git -C "$R14/d" rev-parse --absolute-git-dir
run "r14 empty .git: rev-parse --show-toplevel" git -C "$R14/d" rev-parse --show-toplevel
run "r14 empty .git: rev-parse --git-common-dir" git -C "$R14/d" rev-parse --git-common-dir
run "r14 empty .git: config --local --no-includes --get-regexp include" \
    git -C "$R14/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "r14 d2 empty .git: rev-parse --show-toplevel" git -C "$R14/d2" rev-parse --show-toplevel

hr "R15 what does a repo dir with .git/config carrying an include do to a PROBE THAT ONLY READS .git/config text?"
R15=$P/r15; mkdir -p "$R15"; mkrepo "$R15/d"
printf '[include]\n\tpath = %s\n' "$R15/out.cfg" > "$R15/d/.git/config"
printf '[user]\n\temail = OUTSIDE-R15@invalid\n' > "$R15/out.cfg"
run "r15 the text of .git/config (a pure-python read sees the include)" cat "$R15/d/.git/config"
strun "r15 rev-parse (git still follows it)" "$R15/out.cfg" git -C "$R15/d" rev-parse --show-toplevel

hr "DONE"

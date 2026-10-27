#!/usr/bin/env bash
# R45LabratGitAPIs probe round 5: remaining ambiguities.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe5
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

hr "S1 base of a RELATIVE [includeIf \"gitdir:...\"] pattern : cwd? git-dir parent? work-tree root?"
S1=$P/s1; mkdir -p "$S1"; mkrepo "$S1/base/lane"
printf '[user]\n\temail = OUTSIDE-S1@invalid\n' > "$S1/out.cfg"
printf '[includeIf "gitdir:lane/.git"]\n\tpath = %s\n' "$S1/out.cfg" >> "$S1/base/lane/.git/config"
printf -- '--- git -C lane (cwd becomes the work tree) : pattern "lane/.git"\n'
strun "s1 -C lane" "$S1/out.cfg" git -C "$S1/base/lane" rev-parse --show-toplevel
printf -- '--- GIT_DIR absolute, cwd = the work tree (lane) : pattern "lane/.git"\n'
strun "s1 GIT_DIR abs, cwd=lane" "$S1/out.cfg" \
    env GIT_DIR="$S1/base/lane/.git" GIT_WORK_TREE="$S1/base/lane" git -C "$S1/base/lane" rev-parse --show-toplevel
printf -- '--- GIT_DIR absolute, cwd = S1 (grandparent) : pattern "lane/.git"\n'
strun "s1 GIT_DIR abs, cwd=S1" "$S1/out.cfg" \
    env GIT_DIR="$S1/base/lane/.git" GIT_WORK_TREE="$S1/base/lane" git -C "$S1" rev-parse --show-toplevel
printf -- '--- GIT_DIR absolute, cwd = S1/base : pattern "lane/.git"\n'
strun "s1 GIT_DIR abs, cwd=S1/base" "$S1/out.cfg" \
    env GIT_DIR="$S1/base/lane/.git" GIT_WORK_TREE="$S1/base/lane" git -C "$S1/base" rev-parse --show-toplevel
printf -- '--- GIT_DIR absolute, cwd = S1/base/lane : pattern "lane/.git"  (candidate base = git-dir parent S1/base)\n'
strun "s1 GIT_DIR abs, cwd=S1/base/lane" "$S1/out.cfg" \
    env GIT_DIR="$S1/base/lane/.git" GIT_WORK_TREE="$S1/base/lane" git -C "$S1/base/lane" rev-parse --show-toplevel

hr "S2 [includeIf \"onbranch:\"] : can it open an outside file too?"
S2=$P/s2; mkdir -p "$S2"; mkrepo "$S2/d"
printf '[user]\n\temail = OUTSIDE-S2@invalid\n' > "$S2/out.cfg"
printf '[includeIf "onbranch:master"]\n\tpath = %s\n' "$S2/out.cfg" >> "$S2/d/.git/config"
strun "s2 rev-parse (branch master)" "$S2/out.cfg" git -C "$S2/d" rev-parse --show-toplevel
strun "s2 status" "$S2/out.cfg" git -C "$S2/d" status --porcelain
run "s2 config --local --no-includes --get-regexp include" git -C "$S2/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "s2 --show-origin --get-regexp include" git -C "$S2/d" config --show-origin --get-regexp '^include(if)?\.'
run "s2 current branch" git -C "$S2/d" rev-parse --abbrev-ref HEAD

hr "S3 an EXPLICIT GIT_DIR still triggers the setup read of the repo config (and its include)"
S3=$P/s3; mkdir -p "$S3"; mkrepo "$S3/d"
printf '[include]\n\tpath = %s\n' "$S3/out.cfg" > "$S3/d/.git/config"
printf '[user]\n\temail = OUTSIDE-S3@invalid\n' > "$S3/out.cfg"
mkdir -p "$S3/elsewhere"
strun "s3 GIT_DIR explicit, cwd outside the repo" "$S3/out.cfg" \
    env GIT_DIR="$S3/d/.git" GIT_WORK_TREE="$S3/d" git -C "$S3/elsewhere" rev-parse --show-toplevel
strun "s3 --git-dir explicit, cwd outside the repo" "$S3/out.cfg" \
    git --git-dir="$S3/d/.git" --work-tree="$S3/d" -C "$S3/elsewhere" rev-parse --show-toplevel

hr "S4 [include] inside .git/config with a RELATIVE path : resolved against what?"
S4=$P/s4; mkdir -p "$S4"; mkrepo "$S4/d"
mkdir -p "$S4/d/sub"; printf '[user]\n\temail = OUTSIDE-S4@invalid\n' > "$S4/d/sub/rel.cfg"
printf '[include]\n\tpath = sub/rel.cfg\n' >> "$S4/d/.git/config"
run "s4 config --list --show-origin (which file is read?)" git -C "$S4/d" config --list --show-origin
strun "s4 does the relative include resolve inside d?" "$S4/d/sub/rel.cfg" git -C "$S4/d" rev-parse --show-toplevel
printf -- '--- S4b: a relative include that escapes d\n'
S4B=$P/s4b; mkdir -p "$S4B"; mkrepo "$S4B/d"
printf '[user]\n\temail = OUTSIDE-S4B@invalid\n' > "$S4B/outside.cfg"
printf '[include]\n\tpath = ../outside.cfg\n' >> "$S4B/d/.git/config"
run "s4b config --list --show-origin" git -C "$S4B/d" config --list --show-origin
strun "s4b does the escaping relative include get opened?" "$S4B/outside.cfg" git -C "$S4B/d" rev-parse --show-toplevel

hr "S5 --git-common-dir for a repo whose commondir points INSIDE d (honest shape) and the plain vs absolute form"
S5=$P/s5; mkdir -p "$S5"
mkrepo "$S5/main"; git -C "$S5/main" worktree add -q "$S5/wt" -b side 2>&1 | head -2
run "s5 wt --git-common-dir (plain)" git -C "$S5/wt" rev-parse --git-common-dir
run "s5 wt --path-format=absolute --git-common-dir" git -C "$S5/wt" rev-parse --path-format=absolute --git-common-dir
run "s5 wt --git-dir (plain)" git -C "$S5/wt" rev-parse --git-dir
run "s5 wt --absolute-git-dir" git -C "$S5/wt" rev-parse --absolute-git-dir

hr "DONE"

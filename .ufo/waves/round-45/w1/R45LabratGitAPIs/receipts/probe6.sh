#!/usr/bin/env bash
# R45LabratGitAPIs probe round 6: the base of a RELATIVE include.path and a RELATIVE includeIf gitdir pattern;
# does --no-includes still open an includeIf target inside .git/config?
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe6
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
# trace every open whose path ends with a suffix
traceall() { local l=$1 sfx=$2; shift 2; printf -- '--- %s\n' "$l"
  local log="$P/s.$$.$RANDOM.log"
  strace -f -qq -y -e trace=open,openat,openat2,creat -o "$log" "$@" >/dev/null 2>&1
  printf '[rc=%s]\n' "$?"
  grep -F -- "$sfx" "$log" | sed 's/^/    /' || printf '    (no open ending in %s)\n' "$sfx"
  rm -f "$log"; }
mkrepo() { mkdir -p "$1"; git -C "$1" init -q -b master . >/dev/null 2>&1
  printf 'x\n' > "$1/file.txt"; git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm one >/dev/null 2>&1; }

hr "T1  relative include.path : which directory is the base? (markers everywhere)"
T1=$P/t1; mkdir -p "$T1/base"
mkrepo "$T1/base/d"
printf '[include]\n\tpath = rel.cfg\n' >> "$T1/base/d/.git/config"
printf '[user]\n\temail = MARK-REL@invalid\n' > "$T1/base/d/.git/rel.cfg"
printf '[user]\n\temail = MARK-REL@invalid\n' > "$T1/base/d/rel.cfg"
printf '[user]\n\temail = MARK-REL@invalid\n' > "$T1/base/rel.cfg"
printf '[user]\n\temail = MARK-REL@invalid\n' > "$T1/rel.cfg"
traceall "t1 rev-parse : every open of rel.cfg" "rel.cfg" git -C "$T1/base/d" rev-parse --show-toplevel
run "t1 config --list --show-origin" git -C "$T1/base/d" config --list --show-origin

hr "T2  relative include.path ESCAPING d (../outside.cfg) : which file is read?"
T2=$P/t2; mkdir -p "$T2/base"
mkrepo "$T2/base/d"
printf '[include]\n\tpath = ../outside.cfg\n' >> "$T2/base/d/.git/config"
printf '[user]\n\temail = MARK-ESC@invalid\n' > "$T2/base/d/.git/../outside.cfg"
printf '[user]\n\temail = MARK-ESC@invalid\n' > "$T2/base/d/../outside.cfg"
printf '[user]\n\temail = MARK-ESC@invalid\n' > "$T2/base/outside.cfg"
traceall "t2 rev-parse : every open of outside.cfg" "outside.cfg" git -C "$T2/base/d" rev-parse --show-toplevel

hr "T3  does 'git config --local --no-includes' open an includeIf target inside .git/config?"
T3=$P/t3; mkdir -p "$T3"; mkrepo "$T3/d"
printf '[user]\n\temail = OUTSIDE-T3@invalid\n' > "$T3/out.cfg"
printf '[includeIf "gitdir:%s/d/.git"]\n\tpath = %s\n' "$T3" "$T3/out.cfg" >> "$T3/d/.git/config"
traceall "t3 config --local --no-includes --get-regexp include (opens out.cfg?)" "out.cfg" \
    git -C "$T3/d" config --local --no-includes --get-regexp '^include(if)?\.'
traceall "t3 rev-parse (opens out.cfg?)" "out.cfg" git -C "$T3/d" rev-parse --show-toplevel

hr "T4  relative includeIf gitdir pattern : which base? (try several patterns, one repo)"
T4=$P/t4; mkdir -p "$T4/base"; mkrepo "$T4/base/lane"
printf '[user]\n\temail = OUTSIDE-T4@invalid\n' > "$T4/out.cfg"
try() { local pat=$1
  printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$pat" "$T4/out.cfg" >> "$T4/base/lane/.git/config"
  printf -- '--- pattern "%s" (cwd=%s)\n' "$pat" "$1"
  local log="$P/t4.$$.$RANDOM.log"
  strace -f -qq -y -e trace=open,openat,openat2,creat -o "$log" git -C "$T4/base/lane" rev-parse --show-toplevel >/dev/null 2>&1
  if grep -F -- "$T4/out.cfg" "$log" >/dev/null; then printf '    FIRED\n'; else printf '    not fired\n'; fi
  rm -f "$log"; }
try "lane/.git"
try "base/lane/.git"
try "t4/base/lane/.git"
try "./lane/.git"

hr "T5  can a hostile module make git hang the fence via include.path = a FIFO inside d's PARENT?"
T5=$P/t5; mkdir -p "$T5"; mkrepo "$T5/d"
mkfifo "$T5/fifo.cfg"
git -C "$T5/d" config --add include.path "$T5/fifo.cfg"
printf -- '--- timeout 5 git rev-parse (repo cwd)\n'
timeout 5 git -C "$T5/d" rev-parse --show-toplevel; printf '[rc=%s] (124=blocked on the FIFO)\n' "$?"
printf -- '--- timeout 5 git rev-parse with GIT_CEILING_DIRECTORIES=d.parent\n'
GIT_CEILING_DIRECTORIES="$T5" timeout 5 git -C "$T5/d" rev-parse --show-toplevel; printf '[rc=%s]\n' "$?"

hr "T6  does the fence have to worry about 'git -C <repo>' vs cwd? (probe inside d vs at d)"
T6=$P/t6; mkdir -p "$T6"; mkrepo "$T6/d/lane"
printf '[include]\n\tpath = %s\n' "$T6/out.cfg" >> "$T6/d/lane/.git/config"
printf '[user]\n\temail = OUTSIDE-T6@invalid\n' > "$T6/out.cfg"
traceall "t6 probe with cwd = the repo (lane)" "out.cfg" git -C "$T6/d/lane" rev-parse --show-toplevel
traceall "t6 probe with cwd = d (parent of lane)" "out.cfg" git -C "$T6/d" rev-parse --show-toplevel
traceall "t6 probe with cwd = d and --git-dir=lane/.git" "out.cfg" \
    git -C "$T6/d" --git-dir=lane/.git rev-parse --show-toplevel

hr "DONE"

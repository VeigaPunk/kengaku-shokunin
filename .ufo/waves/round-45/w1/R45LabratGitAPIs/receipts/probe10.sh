#!/usr/bin/env bash
# R45LabratGitAPIs probe round 10: --file include behaviour, ceiling vs include, relative gitdir: base (isolated).
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe10
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
opened() { local l=$1 n=$2; shift 2; printf -- '--- %s\n' "$l"
  local log="$P/s.$$.$RANDOM.log"
  strace -f -qq -y -e trace=open,openat,openat2,creat -o "$log" "$@" >/dev/null 2>&1
  if grep -F -- "$n" "$log" >/dev/null; then printf '  OPENED\n'; else printf '  not opened\n'; fi
  rm -f "$log"; }
mkrepo() { mkdir -p "$1"; git -C "$1" init -q -b master . >/dev/null 2>&1
  printf 'x\n' > "$1/file.txt"; git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm one >/dev/null 2>&1; }

hr "X1  does 'git config --file <f>' FOLLOW include.path ?"
X1=$P/x1; mkdir -p "$X1"; mkrepo "$X1/d"
printf '[include]\n\tpath = %s\n' "$X1/out.cfg" > "$X1/standalone.cfg"
printf '[user]\n\temail = OUTSIDE-X1@invalid\n' > "$X1/out.cfg"
run "x1 config --file standalone --list  (does the included VALUE appear?)" \
    git -C "$X1" config --file "$X1/standalone.cfg" --list
run "x1 config --file standalone --get user.email" \
    git -C "$X1" config --file "$X1/standalone.cfg" --get user.email
opened "x1 does --file --list OPEN the include target?" "$X1/out.cfg" \
    git -C "$X1" config --file "$X1/standalone.cfg" --list
run "x1 same file via --file, with --includes" \
    git -C "$X1" config --file "$X1/standalone.cfg" --includes --list
opened "x1 --includes: opened?" "$X1/out.cfg" git -C "$X1" config --file "$X1/standalone.cfg" --includes --list

hr "X2  a ceiling does NOT stop the repo's own config (include) from being read"
X2=$P/x2; mkdir -p "$X2"; mkrepo "$X2/d"
printf '[include]\n\tpath = %s\n' "$X2/out.cfg" >> "$X2/d/.git/config"
printf '[user]\n\temail = OUTSIDE-X2@invalid\n' > "$X2/out.cfg"
opened "x2 rev-parse with ceiling=d.parent" "$X2/out.cfg" \
    env GIT_CEILING_DIRECTORIES="$X2" git -C "$X2/d" rev-parse --show-toplevel
opened "x2 config --local --no-includes with ceiling=d.parent" "$X2/out.cfg" \
    env GIT_CEILING_DIRECTORIES="$X2" git -C "$X2/d" config --local --no-includes --get-regexp '^include(if)?\.'
printf -- '--- and with --no-includes + GIT_CONFIG_NOSYSTEM etc, is the include still opened?\n'
opened "x2 config --local --no-includes --list" "$X2/out.cfg" git -C "$X2/d" config --local --no-includes --list

hr "X3  relative includeIf gitdir base : ISOLATED, one pattern per repo, cwd varied"
X3=$P/x3; mkdir -p "$X3"
one() { # one <name> <pattern> <cwd-rel-to-X3>
  local nm=$1 pat=$2 cw=$3
  mkdir -p "$X3/$nm"; mkrepo "$X3/$nm/lane"
  printf '[user]\n\temail = OUTSIDE@invalid\n' > "$X3/$nm/out.cfg"
  printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$pat" "$X3/$nm/out.cfg" >> "$X3/$nm/lane/.git/config"
  printf -- '--- case %s pattern=%s cwd=%s\n' "$nm" "$pat" "$cw"
  opened "   probe" "$X3/$nm/out.cfg" git -C "$X3/$cw" rev-parse --show-toplevel
}
one c1 "lane/.git"    ""            # cwd = X3/c1, gitdir = X3/c1/lane/.git
one c2 "lane/.git"    "c2/lane"     # cwd = X3/c2/lane (the work tree)
one c3 "c3/lane/.git" "c3"          # cwd = X3/c3, pattern includes the case dir
one c4 "../c4/lane/.git" "c4/lane"  # cwd = X3/c4/lane, pattern escapes upward
one c5 "x3/c5/lane/.git" "x3"       # cwd = X3/x3, pattern from X3's parent

hr "X4  what does 'git rev-parse --git-common-dir' print for a repo with NO commondir? (relative!)"
X4=$P/x4; mkdir -p "$X4"; mkrepo "$X4/d"
run "x4 --git-common-dir" git -C "$X4/d" rev-parse --git-common-dir
run "x4 --path-format=absolute --git-common-dir" git -C "$X4/d" rev-parse --path-format=absolute --git-common-dir
run "x4 --git-dir" git -C "$X4/d" rev-parse --git-dir
run "x4 --path-format=absolute --git-dir" git -C "$X4/d" rev-parse --path-format=absolute --git-dir
run "x4 --show-toplevel" git -C "$X4/d" rev-parse --show-toplevel
run "x4 --show-toplevel from a SUBDIR of the repo" sh -c "cd '$X4/d' && git rev-parse --show-toplevel"

hr "X5  a repo whose HEAD points at a missing ref : what do the probes answer?"
X5=$P/x5; mkdir -p "$X5"; mkrepo "$X5/d"
printf 'ref: refs/heads/nope\n' > "$X5/d/.git/HEAD"
run "x5 --absolute-git-dir" git -C "$X5/d" rev-parse --absolute-git-dir
run "x5 --show-toplevel" git -C "$X5/d" rev-parse --show-toplevel
run "x5 --git-common-dir" git -C "$X5/d" rev-parse --git-common-dir
run "x5 cat-file -t HEAD:nope" git -C "$X5/d" cat-file -t HEAD:nope

hr "DONE"

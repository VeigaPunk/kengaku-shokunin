#!/usr/bin/env bash
# R45LabratGitAPIs probe script: measure git's ACTUAL behaviour for the legs the round-45 fence needs.
# Runs entirely under /fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe (never the lane).
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe
rm -rf "$P"; mkdir -p "$P"
cd "$P" || exit 1

# Match the counter's pin env (plans/round44_c1_verify.py GIT_PINS / PIN_CHECK_ENV).
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export HOME=/nonexistent
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@example.invalid
export GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@example.invalid
export GIT_CONFIG_COUNT=4 GIT_CONFIG_KEY_0=core.fsmonitor GIT_CONFIG_VALUE_0=false \
       GIT_CONFIG_KEY_1=core.hooksPath GIT_CONFIG_VALUE_1=/dev/null \
       GIT_CONFIG_KEY_2=gpg.program GIT_CONFIG_VALUE_2=/bin/true \
       GIT_CONFIG_KEY_3=log.showSignature GIT_CONFIG_VALUE_3=false

hr() { printf '\n===== %s =====\n' "$*"; }

# run <label> <cmd...>   : run a command, print rc and stdout/stderr
run() { local lbl=$1; shift; printf -- '--- %s\n' "$lbl"; "$@" 2>&1; printf '[rc=%s]\n' "$?"; }

# strun <label> <needle> <cmd...> : run under strace, report whether <needle> was opened
strun() {
  local lbl=$1 needle=$2; shift 2
  printf -- '--- %s\n' "$lbl"
  local log="$P/strace.$$.$RANDOM.log"
  strace -f -qq -y -e trace=open,openat,openat2,creat -o "$log" "$@" >/dev/null 2>&1
  local rc=$?
  printf '[rc=%s]\n' "$rc"
  if grep -F -- "$needle" "$log" >/dev/null 2>&1; then
    printf 'OPENED %s : YES\n' "$needle"
    grep -F -- "$needle" "$log" | sed 's/^/    /'
  else
    printf 'OPENED %s : NO\n' "$needle"
  fi
  rm -f "$log"
}

mkrepo() { # mkrepo <dir> -> initialised repo with one commit
  mkdir -p "$1"; git -C "$1" init -q -b master . >/dev/null 2>&1
  printf 'x\n' > "$1/file.txt"; git -C "$1" add -A >/dev/null 2>&1
  git -C "$1" commit -qm one >/dev/null 2>&1
}

##############################################################################
hr "P1  [include] in .git/config : does rev-parse follow it? does --no-includes skip it?"
D1=$P/p1; mkdir -p "$D1"; mkrepo "$D1/d"
printf '[user]\n\temail = OUTSIDE-P1@invalid\n' > "$D1/out1.cfg"
git -C "$D1/d" config --add include.path "$D1/out1.cfg"
run "p1 .git/config contents" cat "$D1/d/.git/config"
run "p1 config --local --no-includes --get-regexp ^include(if)?\\." \
    git -C "$D1/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "p1 config --local --get-regexp ^include(if)?\\.  (includes ON)" \
    git -C "$D1/d" config --local --get-regexp '^include(if)?\.'
run "p1 config --local --get user.email  (value from the include?)" \
    git -C "$D1/d" config --local --get user.email
strun "p1 rev-parse --show-toplevel" "$D1/out1.cfg" git -C "$D1/d" rev-parse --show-toplevel
strun "p1 status --porcelain"          "$D1/out1.cfg" git -C "$D1/d" status --porcelain
strun "p1 config --local --no-includes --get-regexp" "$D1/out1.cfg" \
    git -C "$D1/d" config --local --no-includes --get-regexp '^include(if)?\.'
strun "p1 config --local --get-regexp (includes ON)" "$D1/out1.cfg" \
    git -C "$D1/d" config --local --get-regexp '^include(if)?\.'
strun "p1 rev-parse --absolute-git-dir" "$D1/out1.cfg" git -C "$D1/d" rev-parse --absolute-git-dir

##############################################################################
hr "P2  extensions.worktreeConfig + .git/config.worktree"
D2=$P/p2; mkdir -p "$D2"; mkrepo "$D2/d"
printf '[include]\n\tpath = %s\n' "$D2/out2.cfg" > "$D2/d/.git/config.worktree"
printf '[user]\n\temail = OUTSIDE-P2@invalid\n' > "$D2/out2.cfg"
git -C "$D2/d" config extensions.worktreeConfig true
run "p2 .git/config" cat "$D2/d/.git/config"
run "p2 .git/config.worktree" cat "$D2/d/.git/config.worktree"
run "p2 config --local --no-includes --get-regexp include" \
    git -C "$D2/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "p2 config --worktree --get-regexp include" \
    git -C "$D2/d" config --worktree --get-regexp '^include(if)?\.'
run "p2 config --list --show-origin (which files?)" \
    git -C "$D2/d" config --list --show-origin
strun "p2 rev-parse --show-toplevel" "$D2/out2.cfg" git -C "$D2/d" rev-parse --show-toplevel
strun "p2 status --porcelain" "$D2/out2.cfg" git -C "$D2/d" status --porcelain
strun "p2 status --porcelain (config.worktree itself?)" "$D2/d/.git/config.worktree" \
    git -C "$D2/d" status --porcelain

##############################################################################
hr "P3  relative commondir : resolved against the git dir?"
D3=$P/p3; mkdir -p "$D3"
mkdir -p "$D3/d/.git"; printf 'ref: refs/heads/master\n' > "$D3/d/.git/HEAD"
printf '../storeA\n' > "$D3/d/.git/commondir"
mkdir -p "$D3/d/storeA"; git -C "$D3/d/storeA" init -q -b master . >/dev/null 2>&1
run "p3 commondir file" cat "$D3/d/.git/commondir"
run "p3 rev-parse --git-common-dir" git -C "$D3/d" rev-parse --git-common-dir
run "p3 rev-parse --absolute-git-dir" git -C "$D3/d" rev-parse --absolute-git-dir
run "p3 rev-parse --show-toplevel" git -C "$D3/d" rev-parse --show-toplevel
run "p3 rev-parse --git-dir" git -C "$D3/d" rev-parse --git-dir
# decoy: a same-named dir relative to CWD (the probe dir) but not under the git dir
mkdir -p "$P/storeA"; git -C "$P/storeA" init -q -b master . >/dev/null 2>&1
printf 'MARKER-IN-GITDIR-STORE\n' > "$D3/d/storeA/MARKER"; printf 'MARKER-IN-CWD-STORE\n' > "$P/storeA/MARKER"
run "p3 which storeA is the common dir (marker content)?" cat "$D3/d/storeA/MARKER"
run "p3 cwd-relative storeA marker" cat "$P/storeA/MARKER"

##############################################################################
hr "P4  GIT_CEILING_DIRECTORIES : does it stop discovery above a repo-parent?"
D4=$P/p4; mkdir -p "$D4"
mkrepo "$D4/P"; mkdir -p "$D4/P/sub/d"          # d is inside repo P
run "p4 no ceiling: rev-parse --show-toplevel from D4/P/sub/d" git -C "$D4/P/sub/d" rev-parse --show-toplevel
printf '[run] ceiling=P (the repo root itself)\n'
GIT_CEILING_DIRECTORIES="$D4/P" git -C "$D4/P/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] ceiling=P/sub (below the repo root)\n'
GIT_CEILING_DIRECTORIES="$D4/P/sub" git -C "$D4/P/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] ceiling=P/sub/d (the fixture dir itself)\n'
GIT_CEILING_DIRECTORIES="$D4/P/sub/d" git -C "$D4/P/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] ceiling=D4 (parent of the repo root)\n'
GIT_CEILING_DIRECTORIES="$D4" git -C "$D4/P/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] ceiling=/ (nothing above is visible)\n'
GIT_CEILING_DIRECTORIES="/" git -C "$D4/P/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] ceiling=P as a RELATIVE path from the cwd P/sub/d\n'
( cd "$D4/P/sub/d" && GIT_CEILING_DIRECTORIES="P" git rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?" )
printf '[run] multi-entry ceiling "A:B"\n'
D4B=$P/p4b; mkdir -p "$D4B"; mkrepo "$D4B/Q"; mkdir -p "$D4B/Q/sub"
GIT_CEILING_DIRECTORIES="$D4B/nowhere:$D4B/Q" git -C "$D4B/Q/sub" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] ceiling with a trailing slash on the repo root\n'
GIT_CEILING_DIRECTORIES="$D4/P/" git -C "$D4/P/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"

##############################################################################
hr "P5  [includeIf \"gitdir:...\"] : does it fire for a fixture path?"
D5=$P/p5; mkdir -p "$D5"; mkrepo "$D5/lane"
printf '[user]\n\temail = OUTSIDE-P5@invalid\n' > "$D5/out5.cfg"
printf '[includeIf "gitdir:%s/.git/"]\n\tpath = %s\n' "$D5/lane" "$D5/out5.cfg" >> "$D5/lane/.git/config"
run "p5 .git/config" cat "$D5/lane/.git/config"
run "p5 config --local --no-includes --get-regexp include" \
    git -C "$D5/lane" config --local --no-includes --get-regexp '^include(if)?\.'
run "p5 config --local --get-regexp include (includes ON)" \
    git -C "$D5/lane" config --local --get-regexp '^include(if)?\.'
run "p5 config --local --get user.email" git -C "$D5/lane" config --local --get user.email
strun "p5 rev-parse --show-toplevel" "$D5/out5.cfg" git -C "$D5/lane" rev-parse --show-toplevel
strun "p5 status --porcelain" "$D5/out5.cfg" git -C "$D5/lane" status --porcelain
strun "p5 config --local --get-regexp (includes ON)" "$D5/out5.cfg" \
    git -C "$D5/lane" config --local --get-regexp '^include(if)?\.'
# non-matching gitdir pattern
D5B=$P/p5b; mkdir -p "$D5B"; mkrepo "$D5B/lane"
printf '[includeIf "gitdir:%s/other/.git/"]\n\tpath = %s\n' "$D5B/lane" "$D5B/out5b.cfg" >> "$D5B/lane/.git/config"
printf '[user]\n\temail = OUTSIDE-P5B@invalid\n' > "$D5B/out5b.cfg"
strun "p5b NON-matching gitdir includeIf : rev-parse" "$D5B/out5b.cfg" git -C "$D5B/lane" rev-parse --show-toplevel

##############################################################################
hr "P6  rev-parse --git-common-dir with an ABSOLUTE commondir (f7 shape)"
D6=$P/p6; mkdir -p "$D6"
mkrepo "$D6/store"
mkdir -p "$D6/d/lane/.git"; printf 'ref: refs/heads/master\n' > "$D6/d/lane/.git/HEAD"
printf '%s\n' "$D6/store/.git" > "$D6/d/lane/.git/commondir"
run "p6 commondir" cat "$D6/d/lane/.git/commondir"
run "p6 rev-parse --git-common-dir" git -C "$D6/d/lane" rev-parse --git-common-dir
run "p6 rev-parse --absolute-git-dir" git -C "$D6/d/lane" rev-parse --absolute-git-dir
run "p6 rev-parse --show-toplevel" git -C "$D6/d/lane" rev-parse --show-toplevel
run "p6 rev-parse --git-dir" git -C "$D6/d/lane" rev-parse --git-dir
run "p6 rev-parse --is-inside-work-tree" git -C "$D6/d/lane" rev-parse --is-inside-work-tree

##############################################################################
hr "P7  core.bare=true : what do the git probes answer? (f9 shape)"
D7=$P/p7; mkdir -p "$D7"; mkrepo "$D7/d"
git -C "$D7/d" config core.bare true
run "p7 rev-parse --show-toplevel" git -C "$D7/d" rev-parse --show-toplevel
run "p7 rev-parse --absolute-git-dir" git -C "$D7/d" rev-parse --absolute-git-dir
run "p7 rev-parse --git-common-dir" git -C "$D7/d" rev-parse --git-common-dir
run "p7 rev-parse --is-inside-work-tree" git -C "$D7/d" rev-parse --is-inside-work-tree
run "p7 config --local --no-includes --get-regexp include" \
    git -C "$D7/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "p7 status --porcelain" git -C "$D7/d" status --porcelain

##############################################################################
hr "P8  core.worktree pointing outside d : what does rev-parse answer?"
D8=$P/p8; mkdir -p "$D8"; mkrepo "$D8/d"
git -C "$D8/d" config core.worktree "$D8/outside"
run "p8 rev-parse --show-toplevel" git -C "$D8/d" rev-parse --show-toplevel
run "p8 rev-parse --absolute-git-dir" git -C "$D8/d" rev-parse --absolute-git-dir
run "p8 config --local --no-includes --get core.worktree" git -C "$D8/d" config --local --no-includes --get core.worktree

##############################################################################
hr "P9  .git as a FILE with gitdir: redirect (f1 shape) : rev-parse answers?"
D9=$P/p9; mkdir -p "$D9"; mkrepo "$D9/store"
mkdir -p "$D9/d"; printf 'gitdir: %s\n' "$D9/store/.git" > "$D9/d/.git"
run "p9 rev-parse --absolute-git-dir" git -C "$D9/d" rev-parse --absolute-git-dir
run "p9 rev-parse --show-toplevel" git -C "$D9/d" rev-parse --show-toplevel
run "p9 rev-parse --git-common-dir" git -C "$D9/d" rev-parse --git-common-dir

##############################################################################
hr "P10 objects/info/alternates : does a probe git call read it?"
D10=$P/p10; mkdir -p "$D10"; mkrepo "$D10/d"
mkdir -p "$D10/other.git"; git -C "$D10/other.git" init -q -b master . >/dev/null 2>&1
printf '%s\n' "$D10/other.git/.git/objects" > "$D10/d/.git/objects/info/alternates"
strun "p10 rev-parse --show-toplevel" "$D10/other.git/.git/objects" git -C "$D10/d" rev-parse --show-toplevel
strun "p10 status --porcelain" "$D10/other.git/.git/objects" git -C "$D10/d" status --porcelain

##############################################################################
hr "P11 how the ceiling interacts with a .git FILE above d (discovery shape)"
D11=$P/p11; mkdir -p "$D11"; mkrepo "$D11/outer"
mkdir -p "$D11/outer/deep/d"
run "p11 no ceiling from D11/outer/deep/d" git -C "$D11/outer/deep/d" rev-parse --show-toplevel
printf '[run] ceiling = D11/outer/deep (parent of d, inside the repo)\n'
GIT_CEILING_DIRECTORIES="$D11/outer/deep" git -C "$D11/outer/deep/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] ceiling = D11/outer (the repo root itself)\n'
GIT_CEILING_DIRECTORIES="$D11/outer" git -C "$D11/outer/deep/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] ceiling = D11 (above the repo root)\n'
GIT_CEILING_DIRECTORIES="$D11" git -C "$D11/outer/deep/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"

hr "DONE"

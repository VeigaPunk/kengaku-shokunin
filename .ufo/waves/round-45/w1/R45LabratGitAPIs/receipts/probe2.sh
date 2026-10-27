#!/usr/bin/env bash
# R45LabratGitAPIs probe round 2: disambiguate the round-1 findings.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe2
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

hr "Q1  relative commondir : base of resolution (git dir vs cwd), with a BARE common dir"
Q1=$P/q1; mkdir -p "$Q1"
mkdir -p "$Q1/d/.git"; printf 'ref: refs/heads/master\n' > "$Q1/d/.git/HEAD"
printf '../storeA\n' > "$Q1/d/.git/commondir"
git init -q -b master --bare "$Q1/d/storeA" >/dev/null 2>&1      # git dir relative to d/.git
git init -q -b master --bare "$P/storeA" >/dev/null 2>&1          # git dir relative to cwd
printf 'IN-GITDIR-STORE\n' > "$Q1/d/storeA/MARKER"; printf 'IN-CWD-STORE\n' > "$P/storeA/MARKER"
run "q1 commondir" cat "$Q1/d/.git/commondir"
run "q1 rev-parse --git-common-dir" git -C "$Q1/d" rev-parse --git-common-dir
run "q1 rev-parse --path-format=absolute --git-common-dir" git -C "$Q1/d" rev-parse --path-format=absolute --git-common-dir
run "q1 rev-parse --absolute-git-dir" git -C "$Q1/d" rev-parse --absolute-git-dir
run "q1 rev-parse --show-toplevel" git -C "$Q1/d" rev-parse --show-toplevel
run "q1 git-dir storeA marker (git-dir base)" cat "$Q1/d/storeA/MARKER"
run "q1 cwd storeA marker (cwd base)" cat "$P/storeA/MARKER"
run "q1 config --local --list --show-origin" git -C "$Q1/d" config --local --list --show-origin

hr "Q2  includeIf gitdir: WHICH pattern forms actually fire?"
Q2=$P/q2; mkdir -p "$Q2"
mkcase() { # mkcase <name> <pattern>
  local nm=$1 pat=$2
  mkdir -p "$Q2/$nm"; mkrepo "$Q2/$nm/lane"
  printf '[user]\n\temail = OUTSIDE-%s@invalid\n' "$nm" > "$Q2/$nm/out.cfg"
  printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$pat" "$Q2/$nm/out.cfg" >> "$Q2/$nm/lane/.git/config"
  printf -- '--- case %s pattern=%s\n' "$nm" "$pat"
  strun "q2/$nm rev-parse --show-toplevel" "$Q2/$nm/out.cfg" git -C "$Q2/$nm/lane" rev-parse --show-toplevel
  strun "q2/$nm config --list" "$Q2/$nm/out.cfg" git -C "$Q2/$nm/lane" config --list
  run "q2/$nm config --local --get-regexp include" git -C "$Q2/$nm/lane" config --local --get-regexp '^include(if)?\.'
}
mkcase abs_no_slash "$Q2/abs_no_slash/lane/.git"
mkcase abs_slash   "$Q2/abs_slash/lane/.git/"
mkcase abs_star    "$Q2/abs_star/lane/.git/**"
mkcase rel_dotgit  "lane/.git"
mkcase rel_dotgit_slash "lane/.git/"

hr "Q3  does --no-includes really skip the include? which command opens it?"
Q3=$P/q3; mkdir -p "$Q3"; mkrepo "$Q3/d"
printf '[user]\n\temail = OUTSIDE-Q3@invalid\n' > "$Q3/out.cfg"
git -C "$Q3/d" config --add include.path "$Q3/out.cfg"
run "q3 config --list --show-origin (includes ON, all scopes)" git -C "$Q3/d" config --list --show-origin
run "q3 config --local --list --show-origin" git -C "$Q3/d" config --local --list --show-origin
run "q3 config --local --no-includes --list --show-origin" git -C "$Q3/d" config --local --no-includes --list --show-origin
run "q3 config --file .git/config --no-includes --list (explicit file, no repo discovery?)" \
    git -C "$Q3/d" config --file "$Q3/d/.git/config" --no-includes --list
run "q3 config --file .git/config --list (explicit file, includes ON)" \
    git -C "$Q3/d" config --file "$Q3/d/.git/config" --list
strun "q3 config --file .git/config --no-includes --list" "$Q3/out.cfg" \
    git -C "$Q3/d" config --file "$Q3/d/.git/config" --no-includes --list
strun "q3 config --file .git/config --list" "$Q3/out.cfg" \
    git -C "$Q3/d" config --file "$Q3/d/.git/config" --list
strun "q3 rev-parse --show-toplevel" "$Q3/out.cfg" git -C "$Q3/d" rev-parse --show-toplevel
strun "q3 rev-parse --git-dir" "$Q3/out.cfg" git -C "$Q3/d" rev-parse --git-dir
strun "q3 --version (no repo context)" "$Q3/out.cfg" git --version

hr "Q4  alternates with an EXISTING alternate object store : successful outside open?"
Q4=$P/q4; mkdir -p "$Q4"; mkrepo "$Q4/d"
git init -q -b master --bare "$Q4/other.git" >/dev/null 2>&1
printf '%s\n' "$Q4/other.git/objects" > "$Q4/d/.git/objects/info/alternates"
run "q4 alternates file" cat "$Q4/d/.git/objects/info/alternates"
strun "q4 rev-parse --show-toplevel" "$Q4/other.git/objects" git -C "$Q4/d" rev-parse --show-toplevel
strun "q4 status --porcelain" "$Q4/other.git/objects" git -C "$Q4/d" status --porcelain
strun "q4 rev-parse --show-toplevel (the alternates FILE itself)" "$Q4/d/.git/objects/info/alternates" \
    git -C "$Q4/d" rev-parse --show-toplevel

hr "Q5  ceiling + ancestor repo : can any git probe SEE a repo above d?"
Q5=$P/q5; mkdir -p "$Q5"; mkrepo "$Q5/P"; mkdir -p "$Q5/P/sub/d"
printf '[user]\n\temail = OUTSIDE-ANCESTOR@invalid\n' > "$Q5/P/.git/config"
run "q5 no ceiling toplevel" git -C "$Q5/P/sub/d" rev-parse --show-toplevel
printf '[run] ceiling = Q5/P/sub (the round-44 shape: ceiling=d.parent)\n'
GIT_CEILING_DIRECTORIES="$Q5/P/sub" git -C "$Q5/P/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
strun "q5 NO ceiling: rev-parse --show-toplevel" "$Q5/P/.git/config" git -C "$Q5/P/sub/d" rev-parse --show-toplevel
strun "q5 ceiling=P/sub: rev-parse --show-toplevel" "$Q5/P/.git/config" \
    env GIT_CEILING_DIRECTORIES="$Q5/P/sub" git -C "$Q5/P/sub/d" rev-parse --show-toplevel
strun "q5 NO ceiling: config --local --get user.email" "$Q5/P/.git/config" git -C "$Q5/P/sub/d" config --local --get user.email
run "q5 filesystem: does Q5/P/sub/d have .git?" ls -a "$Q5/P/sub/d"

hr "Q6  core.worktree RELATIVE : base of resolution"
Q6=$P/q6; mkdir -p "$Q6"; mkrepo "$Q6/d"
git -C "$Q6/d" config core.worktree "../wt"
run "q6 rev-parse --show-toplevel (relative core.worktree)" git -C "$Q6/d" rev-parse --show-toplevel
run "q6 config --local --no-includes --get core.worktree" git -C "$Q6/d" config --local --no-includes --get core.worktree
Q6B=$P/q6b; mkdir -p "$Q6B"; mkrepo "$Q6B/d"
git -C "$Q6B/d" config core.worktree "wt"
run "q6b rev-parse --show-toplevel (relative core.worktree 'wt')" git -C "$Q6B/d" rev-parse --show-toplevel

hr "Q7  .git/config.worktree : which git calls read it, and does --no-includes see its include?"
Q7=$P/q7; mkdir -p "$Q7"; mkrepo "$Q7/d"
printf '[include]\n\tpath = %s\n' "$Q7/out.cfg" > "$Q7/d/.git/config.worktree"
printf '[user]\n\temail = OUTSIDE-Q7@invalid\n' > "$Q7/out.cfg"
git -C "$Q7/d" config extensions.worktreeConfig true
run "q7 config --local --no-includes --get-regexp include" git -C "$Q7/d" config --local --no-includes --get-regexp '^include(if)?\.'
run "q7 config --worktree --no-includes --get-regexp include" git -C "$Q7/d" config --worktree --no-includes --get-regexp '^include(if)?\.'
run "q7 config --local --get-regexp include (no --no-includes)" git -C "$Q7/d" config --local --get-regexp '^include(if)?\.'
run "q7 config --list --show-origin" git -C "$Q7/d" config --list --show-origin
strun "q7 rev-parse --show-toplevel" "$Q7/out.cfg" git -C "$Q7/d" rev-parse --show-toplevel
strun "q7 config --local --no-includes --get-regexp include" "$Q7/out.cfg" \
    git -C "$Q7/d" config --local --no-includes --get-regexp '^include(if)?\.'
strun "q7 config --worktree --no-includes --get-regexp include" "$Q7/out.cfg" \
    git -C "$Q7/d" config --worktree --no-includes --get-regexp '^include(if)?\.'
strun "q7 rev-parse --show-toplevel (config.worktree itself)" "$Q7/d/.git/config.worktree" \
    git -C "$Q7/d" rev-parse --show-toplevel

hr "Q8  .git/commondir ABSOLUTE : --git-common-dir path-format + inside/outside check"
Q8=$P/q8; mkdir -p "$Q8"; mkrepo "$Q8/store"
mkdir -p "$Q8/d/lane/.git"; printf 'ref: refs/heads/master\n' > "$Q8/d/lane/.git/HEAD"
printf '%s\n' "$Q8/store/.git" > "$Q8/d/lane/.git/commondir"
run "q8 --git-common-dir" git -C "$Q8/d/lane" rev-parse --git-common-dir
run "q8 --path-format=absolute --git-common-dir" git -C "$Q8/d/lane" rev-parse --path-format=absolute --git-common-dir
run "q8 --absolute-git-dir" git -C "$Q8/d/lane" rev-parse --absolute-git-dir
run "q8 --show-toplevel" git -C "$Q8/d/lane" rev-parse --show-toplevel
run "q8 --git-dir" git -C "$Q8/d/lane" rev-parse --git-dir
run "q8 status --porcelain" git -C "$Q8/d/lane" status --porcelain
run "q8 config --local --list --show-origin" git -C "$Q8/d/lane" config --local --list --show-origin

hr "Q9  rc!=0 semantics: bare repo, non-repo dir, and a repo whose HEAD is broken"
Q9=$P/q9; mkdir -p "$Q9"; mkrepo "$Q9/d"
git -C "$Q9/d" config core.bare true
run "q9 bare: rev-parse --show-toplevel" git -C "$Q9/d" rev-parse --show-toplevel
run "q9 bare: rev-parse --absolute-git-dir" git -C "$Q9/d" rev-parse --absolute-git-dir
run "q9 bare: rev-parse --git-common-dir" git -C "$Q9/d" rev-parse --git-common-dir
run "q9 bare: rev-parse --is-inside-work-tree" git -C "$Q9/d" rev-parse --is-inside-work-tree
mkdir -p "$Q9/plain"
run "q9 plain dir (no repo): rev-parse --show-toplevel" git -C "$Q9/plain" rev-parse --show-toplevel
run "q9 plain dir (no repo): rev-parse --absolute-git-dir" git -C "$Q9/plain" rev-parse --absolute-git-dir
run "q9 plain dir (no repo): rev-parse --git-common-dir" git -C "$Q9/plain" rev-parse --git-common-dir
run "q9 plain dir (no repo): config --local --no-includes --get-regexp include" \
    git -C "$Q9/plain" config --local --no-includes --get-regexp '^include(if)?\.'
mkdir -p "$Q9/broken"; printf 'ref: refs/heads/nope\n' > "$Q9/broken/.git/HEAD" 2>/dev/null || true

hr "Q10 what does a bare-dir (.git as bare repo) look like: does rev-parse answer?"
Q10=$P/q10; mkdir -p "$Q10"
git init -q -b master --bare "$Q10/store.git" >/dev/null 2>&1
run "q10 bare repo: rev-parse --absolute-git-dir" git -C "$Q10/store.git" rev-parse --absolute-git-dir
run "q10 bare repo: rev-parse --show-toplevel" git -C "$Q10/store.git" rev-parse --show-toplevel
run "q10 bare repo: rev-parse --git-common-dir" git -C "$Q10/store.git" rev-parse --git-common-dir
run "q10 bare repo: rev-parse --is-bare-repository" git -C "$Q10/store.git" rev-parse --is-bare-repository

hr "DONE"

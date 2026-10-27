#!/usr/bin/env bash
# R45LabratGitAPIs probe round 3: mechanism probes (why an include target is opened), FIFO blocking,
# ceiling vs an ancestor repo that sits AT d.parent, and path formats.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe3
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

hr "R1  WHO opens an include target?  repo-setup read vs the explicit --no-includes read"
R1=$P/r1; mkdir -p "$R1"
mkrepo "$R1/d"; printf '[user]\n\temail = OUTSIDE-R1@invalid\n' > "$R1/out.cfg"
git -C "$R1/d" config --add include.path "$R1/out.cfg"
# copy the config OUT of the repo and read it with --file from a NON-repo cwd
cp "$R1/d/.git/config" "$R1/copy-config"
mkdir -p "$R1/norepo"
strun "r1 (A) NON-repo cwd + --file copy --no-includes --list" "$R1/out.cfg" \
    git -C "$R1/norepo" config --file "$R1/copy-config" --no-includes --list
strun "r1 (B) NON-repo cwd + --file copy --list (includes on)" "$R1/out.cfg" \
    git -C "$R1/norepo" config --file "$R1/copy-config" --list
strun "r1 (C) repo cwd + --file copy --no-includes --list" "$R1/out.cfg" \
    git -C "$R1/d" config --file "$R1/copy-config" --no-includes --list
strun "r1 (D) repo cwd + --local --no-includes --list" "$R1/out.cfg" \
    git -C "$R1/d" config --local --no-includes --list
strun "r1 (E) NON-repo cwd + --file copy --no-includes --get include.path" "$R1/out.cfg" \
    git -C "$R1/norepo" config --file "$R1/copy-config" --no-includes --get include.path
strun "r1 (F) NON-repo cwd + --file copy --get include.path (includes on)" "$R1/out.cfg" \
    git -C "$R1/norepo" config --file "$R1/copy-config" --get include.path

hr "R2  FIFO include : does every git call BLOCK? (f4 shape)"
R2=$P/r2; mkdir -p "$R2"; mkrepo "$R2/d"
mkfifo "$R2/fifo.cfg"
git -C "$R2/d" config --add include.path "$R2/fifo.cfg"
printf '[user]\n\temail = FIFO@invalid\n' > "$R2/norepo.cfg"
cp "$R2/d/.git/config" "$R2/copy-config"
mkdir -p "$R2/norepo"
run "r2 repo cwd: timeout 5 git config --local --no-includes --get-regexp include" \
    timeout 5 git -C "$R2/d" config --local --no-includes --get-regexp '^include(if)?\.'
printf '[rc=%s] (124 = timeout/blocked)\n' "$?"
run "r2 repo cwd: timeout 5 git rev-parse --show-toplevel" timeout 5 git -C "$R2/d" rev-parse --show-toplevel
printf '[rc=%s] (124 = timeout/blocked)\n' "$?"
run "r2 repo cwd: timeout 5 git config --local --get-regexp include (includes ON)" \
    timeout 5 git -C "$R2/d" config --local --get-regexp '^include(if)?\.'
printf '[rc=%s] (124 = timeout/blocked)\n' "$?"
run "r2 NON-repo cwd: timeout 5 git config --file copy --no-includes --list" \
    timeout 5 git -C "$R2/norepo" config --file "$R2/copy-config" --no-includes --list
printf '[rc=%s] (124 = timeout/blocked)\n' "$?"
run "r2 NON-repo cwd: timeout 5 git config --file copy --list (includes ON)" \
    timeout 5 git -C "$R2/norepo" config --file "$R2/copy-config" --list
printf '[rc=%s] (124 = timeout/blocked)\n' "$?"

hr "R3  ancestor repo that sits AT d.parent (f6 shape): does a ceilinged probe read it?"
R3=$P/r3; mkdir -p "$R3"
mkrepo "$R3/d.parent"; mkdir -p "$R3/d.parent/sub/d"
printf '[user]\n\temail = ANCESTOR-R3@invalid\n' >> "$R3/d.parent/.git/config"
printf '[run] no ceiling, from d.parent/sub/d\n'
git -C "$R3/d.parent/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
printf '[run] ceiling = d.parent (the round-44 shape)\n'
GIT_CEILING_DIRECTORIES="$R3/d.parent" git -C "$R3/d.parent/sub/d" rev-parse --show-toplevel 2>&1; printf '[rc=%s]\n' "$?"
strun "r3 NO ceiling: does it open d.parent/.git/config ?" "$R3/d.parent/.git/config" \
    git -C "$R3/d.parent/sub/d" rev-parse --show-toplevel
strun "r3 ceiling=d.parent: does it open d.parent/.git/config ?" "$R3/d.parent/.git/config" \
    env GIT_CEILING_DIRECTORIES="$R3/d.parent" git -C "$R3/d.parent/sub/d" rev-parse --show-toplevel
strun "r3 ceiling=d.parent: git cat-file -t HEAD:x on the ancestor repo" "$R3/d.parent/.git/config" \
    env GIT_CEILING_DIRECTORIES="$R3/d.parent" git -C "$R3/d.parent" cat-file -t HEAD:x

hr "R4  path formats of the git-dir probes (a normal repo)"
R4=$P/r4; mkdir -p "$R4"; mkrepo "$R4/d"
run "r4 --git-dir (relative)" git -C "$R4/d" rev-parse --git-dir
run "r4 --path-format=absolute --git-dir" git -C "$R4/d" rev-parse --path-format=absolute --git-dir
run "r4 --git-common-dir" git -C "$R4/d" rev-parse --git-common-dir
run "r4 --path-format=absolute --git-common-dir" git -C "$R4/d" rev-parse --path-format=absolute --git-common-dir
run "r4 --absolute-git-dir" git -C "$R4/d" rev-parse --absolute-git-dir
run "r4 --show-toplevel" git -C "$R4/d" rev-parse --show-toplevel
run "r4 --show-superproject-working-tree" git -C "$R4/d" rev-parse --show-superproject-working-tree
run "r4 --show-prefix (from a subdir)" sh -c "cd '$R4/d' && git rev-parse --show-prefix"

hr "R5  relative commondir, revisited: base = the git dir (not the cwd)"
R5=$P/r5; mkdir -p "$R5"
mkdir -p "$R5/d/.git"; printf 'ref: refs/heads/master\n' > "$R5/d/.git/HEAD"
printf 'storeA\n' > "$R5/d/.git/commondir"     # relative, one level under the git dir
git init -q -b master --bare "$R5/d/.git/storeA" >/dev/null 2>&1
git init -q -b master --bare "$R5/storeA" >/dev/null 2>&1
run "r5 --git-common-dir (relative 'storeA')" git -C "$R5/d" rev-parse --git-common-dir
run "r5 --absolute-git-dir" git -C "$R5/d" rev-parse --absolute-git-dir
run "r5 --show-toplevel" git -C "$R5/d" rev-parse --show-toplevel
run "r5 config --local --list --show-origin (whose config is used?)" git -C "$R5/d" config --local --list --show-origin

hr "R6  includeIf gitdir: pattern forms (repeat, cleaner) + does --no-includes list it?"
R6=$P/r6; mkdir -p "$R6"
mkcase() { local nm=$1 pat=$2
  mkdir -p "$R6/$nm"; mkrepo "$R6/$nm/lane"
  printf '[user]\n\temail = OUTSIDE-%s@invalid\n' "$nm" > "$R6/$nm/out.cfg"
  printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$pat" "$R6/$nm/out.cfg" >> "$R6/$nm/lane/.git/config"
  printf -- '--- case %s pattern=%s\n' "$nm" "$pat"
  strun "r6/$nm rev-parse" "$R6/$nm/out.cfg" git -C "$R6/$nm/lane" rev-parse --show-toplevel
  run "r6/$nm config --local --no-includes --get-regexp include" \
      git -C "$R6/$nm/lane" config --local --no-includes --get-regexp '^include(if)?\.'
}
mkcase exact_abs "$R6/exact_abs/lane/.git"
mkcase exact_abs_slash "$R6/exact_abs_slash/lane/.git/"
mkcase rel_gitdir "lane/.git"
mkcase rel_gitdir_slash "lane/.git/"
mkcase abs_glob "$R6/exact_abs/lane/.git*"

hr "R7  [includeIf \"onbranch:\"] and [includeIf \"gitdir:~\"] do not matter; check a plain include inside a repo with a worktree"
R7=$P/r7; mkdir -p "$R7"; mkrepo "$R7/d"
git -C "$R7/d" worktree add -q "$R7/wt" -b side 2>&1 | head -3
run "r7 worktree .git file" cat "$R7/wt/.git"
run "r7 worktree: --git-common-dir" git -C "$R7/wt" rev-parse --git-common-dir
run "r7 worktree: --git-dir" git -C "$R7/wt" rev-parse --git-dir
run "r7 worktree: --absolute-git-dir" git -C "$R7/wt" rev-parse --absolute-git-dir
run "r7 worktree: --show-toplevel" git -C "$R7/wt" rev-parse --show-toplevel

hr "DONE"

#!/usr/bin/env bash
# prior-art experiments; run under envelope.sh; all paths under $S
set -u
S=$1; cd "$S"; export TMPDIR="$S"
export HOME="$S/home"; mkdir -p "$HOME"
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
OUT="$S/outside"; mkdir -p "$OUT"
printf '[user]\n\tname = LEAKED\n' > "$OUT/inc.cfg"
tr() { # tr <label> <cwd> cmd... ; prints whether $OUT paths were opened (any openat, ok or ENOENT counted separately)
  label=$1; cwd=$2; shift 2
  ( cd "$cwd" && strace -f -y -e trace=openat,open,openat2,stat,newfstatat,statx,access,readlink,readlinkat,getcwd -o "$S/st.$$" "$@" >"$S/o.$$" 2>&1; rc=$? 
    ok=$(grep -c "$OUT" "$S/st.$$" | tr -d ' ' 2>/dev/null || true)
    succ=$(grep "$OUT" "$S/st.$$" | grep -v ENOENT | grep -c 'open' || true)
    echo "$label rc=$rc outside_refs=$ok outside_successful_open=$succ out=$(head -c 80 "$S/o.$$" | tr '\n' '|')" )
}
unset -f tr 2>/dev/null
run() { label=$1; cwd=$2; shift 2
  ( cd "$cwd" && strace -f -y -e trace=openat,open,openat2,newfstatat,statx,access,readlink,readlinkat -o "$S/st.log" "$@" >"$S/o.log" 2>&1; rc=$?
    refs=$(grep -c "$OUT" "$S/st.log"); succ=$(grep "$OUT" "$S/st.log" | grep -E 'open(at2?)?\(' | grep -vc ENOENT)
    echo "$label rc=$rc outside_refs=$refs outside_successful_open=$succ stdout=$(head -c 60 "$S/o.log" | tr '\n' '|')" ); }
git --version
echo "== E1 include in .git/config (env isolated: NOSYSTEM + GLOBAL=/dev/null + HOME scratch)"
D=$S/e1; mkdir -p $D; git -C $D init -q; git -C $D config include.path "$OUT/inc.cfg"
run "E1a git rev-parse HEAD"              $D git rev-parse --git-dir
run "E1b git status"                      $D git status --short
run "E1c git -c include.path=/dev/null status" $D git -c include.path=/dev/null status --short
run "E1d git config user.name (default)"  $D git config user.name
run "E1e git config --no-includes user.name" $D git config --no-includes user.name
run "E1f git config --local --no-includes --get-regexp ^include" $D git config --local --no-includes --get-regexp '^include'
run "E1g git config --file .git/config (default no includes)" $D git config --file .git/config --get-regexp '^include'
run "E1h git config --file .git/config --includes user.name" $D git config --file .git/config --includes user.name
run "E1i GIT_CONFIG_COUNT override" $D env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=include.path GIT_CONFIG_VALUE_0=/dev/null git status --short
run "E1j git --no-replace-objects? (no includes flag exists?) git --config-env" $D git status --short
echo "== E1k: git has global switch for includes?"; git --help 2>&1 | grep -ci 'no-includes' || true
echo "== E2 config.worktree include, main worktree"
D=$S/e2; mkdir -p $D; git -C $D init -q; printf '[include]\n\tpath = %s\n' "$OUT/inc.cfg" > $D/.git/config.worktree
run "E2a worktree file present, extension OFF: git config user.name" $D git config user.name
run "E2b same, git status" $D git status --short
git -C $D config extensions.worktreeConfig true
run "E2c extension ON: git config user.name" $D git config user.name
run "E2d extension ON: git config --local user.name" $D git config --local user.name
run "E2e extension ON: git config --worktree --no-includes --get-regexp ^include" $D git config --worktree --no-includes --get-regexp '^include'
run "E2f extension ON: git rev-parse --git-dir (plain discovery)" $D git rev-parse --git-dir
run "E2g extension ON: git status" $D git status --short
echo "== E3 commondir delegation"
C=$S/e3common; mkdir -p $C; git -C $C init -q --bare; git -C $C config include.path "$OUT/inc.cfg"
D=$S/e3; mkdir -p $D/.git; echo 'ref: refs/heads/master' > $D/.git/HEAD; echo "$C" > $D/.git/commondir
printf '[core]\n\trepositoryformatversion = 0\n' > $D/.git/config   # innocuous local config inside d
run "E3a d/.git has only HEAD+commondir(abs outside): git config user.name" $D git config user.name
run "E3b same: git rev-parse --git-dir --git-common-dir --show-toplevel" $D git rev-parse --git-dir --git-common-dir --show-toplevel
run "E3c same: git status" $D git status --short
# relative commondir
echo "../../e3common" > $D/.git/commondir
run "E3d relative commondir ../../e3common: git config user.name" $D git config user.name
echo "== E3x: is commondir honoured w/o objects/ refs/ in gitdir?"; (cd $D; git rev-parse --git-common-dir 2>&1)
echo "== E4 repo above d + GIT_CEILING_DIRECTORIES"
X=$S/e4; mkdir -p $X/d; git -C $X init -q; git -C $X config include.path "$OUT/inc.cfg"
run "E4a no ceiling, cwd=d: git rev-parse --show-toplevel" $X/d git rev-parse --show-toplevel
run "E4b ceiling=X (parent of repo-root X is not listed; X itself listed)" $X/d env GIT_CEILING_DIRECTORIES=$X git rev-parse --show-toplevel
run "E4c ceiling=X/d (d itself)" $X/d env GIT_CEILING_DIRECTORIES=$X/d git rev-parse --show-toplevel
run "E4d ceiling=dirname(d)=X ... plus config read: git status" $X/d env GIT_CEILING_DIRECTORIES=$X git status
run "E4e ceiling=X/d, d contains its own .git (init)" $X/d bash -c 'git init -q . ; GIT_CEILING_DIRECTORIES='$X/d' git rev-parse --show-toplevel'
echo "== E5 alternates (object db) lazy read"
D=$S/e5; mkdir -p $D; git -C $D init -q; echo "$S/e5altobjs" > $D/.git/objects/info/alternates; mkdir -p $S/e5altobjs
run "E5a git rev-parse --git-dir (alternates opened?)" $D git rev-parse --git-dir
run "E5b git rev-parse HEAD (unborn)" $D git rev-parse HEAD
run "E5c git cat-file -t deadbeefdeadbeefdeadbeefdeadbeefdeadbeef" $D git cat-file -t deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
run "E5d git status" $D git status --short

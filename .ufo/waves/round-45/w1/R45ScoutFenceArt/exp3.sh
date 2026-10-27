#!/usr/bin/env bash
set -u
S=$1; cd "$S"; export TMPDIR="$S" HOME="$S/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
run() { label=$1; cwd=$2; pat=$3; shift 3
  ( cd "$cwd" && strace -f -y -e trace=openat,open,openat2,newfstatat,statx,access,readlink,readlinkat -o "$S/st.log" "$@" >"$S/o.log" 2>&1; rc=$?
    refs=$(grep -c "$pat" "$S/st.log"); succ=$(grep "$pat" "$S/st.log" | grep -E 'open(at2?)?\(' | grep -vc ENOENT)
    echo "$label rc=$rc refs=$refs successful_open=$succ stdout=$(head -c 70 "$S/o.log" | tr '\n' '|')" ); }
# E17 populated alternate: real repo as alternate store, local missing object lookup
A=$S/e17alt; rm -rf $A; mkdir -p $A; git -C $A init -q; git -C $A -c user.name=a -c user.email=a@b commit -q --allow-empty -m x; git -C $A gc -q 2>/dev/null
D=$S/e17; rm -rf $D; mkdir -p $D; git -C $D init -q; echo "$A/.git/objects" > $D/.git/objects/info/alternates
SHA=$(git -C $A rev-parse HEAD)
run "E17a rev-parse --git-dir (alternate store populated)" $D "e17alt" git rev-parse --git-dir
run "E17b status" $D "e17alt" git status --short
run "E17c cat-file -t <sha only in alternate>" $D "e17alt" git cat-file -t $SHA
run "E17d cat-file -t <missing sha>" $D "e17alt" git cat-file -t deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
# E18 untrusted? gitfile -> gitdir with commondir -> config in common used, config.worktree in gitdir used only if ext on in COMMON config
C=$S/e18c; rm -rf $C; mkdir -p $C; git -C $C init -q --bare; git -C $C config extensions.worktreeConfig true; git -C $C config core.repositoryformatversion 1
G=$S/e18g; rm -rf $G; mkdir -p $G/d; cp -r $C/. $G/d/ 2>/dev/null; rm -rf $G/d/config; printf '[include]\n\tpath = %s/outside/inc.cfg\n' "$S" > $G/d/config.worktree; echo "$C" > $G/d/commondir
mkdir -p $S/e18w; echo "gitdir: $G/d" > $S/e18w/.git
run "E18a gitfile->gitdir(config.worktree include) + commondir(ext ON in common cfg)" $S/e18w "$S/outside" git rev-parse --git-dir
printf '[core]\n\trepositoryformatversion = 0\n' > $C/config
run "E18b same but ext OFF in common cfg (config.worktree ignored)" $S/e18w "$S/outside" git rev-parse --git-dir

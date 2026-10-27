#!/usr/bin/env bash
set -u
S=$1; cd "$S"; export TMPDIR="$S" HOME="$S/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
run() { label=$1; cwd=$2; pat=$3; shift 3
  ( cd "$cwd" && strace -f -y -e trace=openat,open,openat2,newfstatat,statx,access,readlink,readlinkat -o "$S/st.log" "$@" >"$S/o.log" 2>&1; rc=$?
    refs=$(grep -c "$pat" "$S/st.log"); succ=$(grep "$pat" "$S/st.log" | grep -E 'open(at2?)?\(' | grep -vc ENOENT)
    echo "$label rc=$rc refs=$refs successful_open=$succ stdout=$(head -c 80 "$S/o.log" | tr '\n' '|')" ); }
B=$S/e9
run "E19a bare above d, -c safe.bareRepository=explicit" $B/d "$S/outside" git -c safe.bareRepository=explicit rev-parse --git-dir
run "E19b same via GIT_CONFIG_GLOBAL file" $B/d "$S/outside" env GIT_CONFIG_GLOBAL=$S/safe.cfg git rev-parse --git-dir
printf '[safe]\n\tbareRepository = explicit\n' > $S/safe.cfg
run "E19c (after writing safe.cfg) GIT_CONFIG_GLOBAL=safe.cfg" $B/d "$S/outside" env GIT_CONFIG_GLOBAL=$S/safe.cfg git rev-parse --git-dir
# E20: --no-pager + --file + --no-includes on d/.git/config* for every file: the cheapest git-based include lister
D=$S/e2
run "E20a git --no-pager config --file config.worktree --get-regexp ^include (cwd d, no discovery side-effects?)" $D "$S/outside" git --no-pager config --file .git/config.worktree --get-regexp '^include'
run "E20b same but with GIT_DIR=/nonexistent GIT_CEILING_DIRECTORIES=parent" $D "$S/outside" env GIT_CEILING_DIRECTORIES=$S git --no-pager config --file .git/config.worktree --get-regexp '^include'

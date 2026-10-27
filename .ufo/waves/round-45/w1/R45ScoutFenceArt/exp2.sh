#!/usr/bin/env bash
set -u
S=$1; cd "$S"; export TMPDIR="$S" HOME="$S/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
OUT="$S/outside"; mkdir -p "$OUT" "$S/e5altobjs"
printf '[user]\n\tname = LEAKED\n' > "$OUT/inc.cfg"
run() { label=$1; cwd=$2; pat=$3; shift 3
  ( cd "$cwd" && strace -f -y -e trace=openat,open,openat2,newfstatat,statx,access,readlink,readlinkat -o "$S/st.log" "$@" >"$S/o.log" 2>&1; rc=$?
    refs=$(grep -c "$pat" "$S/st.log"); succ=$(grep "$pat" "$S/st.log" | grep -E 'open(at2?)?\(' | grep -vc ENOENT)
    echo "$label rc=$rc outside_refs=$refs outside_successful_open=$succ stdout=$(head -c 70 "$S/o.log" | tr '\n' '|')" ); }
git --version
D=$S/e1
echo "== E8 pager hypothesis: which git invocations can read a config WITHOUT parsing the include target?"
run "E8a git config --local --no-includes --get-regexp (pager path)" $D "$OUT" git config --local --no-includes --get-regexp '^include'
run "E8b git --no-pager config --local --no-includes --get-regexp" $D "$OUT" git --no-pager config --local --no-includes --get-regexp '^include'
run "E8c git --no-pager config --file .git/config --get-regexp" $D "$OUT" git --no-pager config --file .git/config --get-regexp '^include'
run "E8d git config --file .git/config --get-regexp, GIT_PAGER_IN_USE-free: PAGER=cat GIT_PAGER=cat" $D "$OUT" env GIT_PAGER=cat git config --file .git/config --get-regexp '^include'
run "E8e git --no-pager config --file <path outside any repo>" $S "$OUT" git --no-pager config --file $D/.git/config --get-regexp '^include'
run "E8f same, but cwd inside repo that itself has the include" $D "$OUT" git --no-pager config --file $S/e1/.git/config --no-includes --list
run "E8g git config --blob/--stdin? git config --file - < cfg (stdin)" $S "$OUT" sh -c 'git --no-pager config --file - --no-includes --list < '$D'/.git/config'
echo "== E9 bare repo layout ABOVE d (no .git entry) : does discovery find it?"
B=$S/e9; mkdir -p $B/d; git init -q --bare $B; git -C $B config include.path "$OUT/inc.cfg"
run "E9a cwd=d no ceiling: rev-parse --git-dir" $B/d "$OUT" git rev-parse --git-dir
run "E9b same with GIT_CEILING_DIRECTORIES=B (parent of d)" $B/d "$OUT" env GIT_CEILING_DIRECTORIES=$B git rev-parse --git-dir
echo "== E10 invalid/empty d/.git dir does NOT stop discovery"
X=$S/e10; mkdir -p $X/d/.git; git -C $X init -q; git -C $X config include.path "$OUT/inc.cfg"
run "E10a cwd=d (d/.git empty dir), no ceiling" $X/d "$OUT" git rev-parse --show-toplevel
echo "== E11 relative include path and chains"
D=$S/e11; mkdir -p $D $S/e11-out; git -C $D init -q; printf '[user]\n\tname = CHAINED\n' > $S/e11-out/b.cfg; printf '[include]\n\tpath = b.cfg\n' > $S/e11-out/a.cfg
printf '[include]\n\tpath = ../../e11-out/a.cfg\n' > $D/.git/config.extra; printf '[include]\n\tpath = ../../e11-out/a.cfg\n' >> $D/.git/config
run "E11a relative include in .git/config -> ../../e11-out/a.cfg (chain to b.cfg)" $D "$S/e11-out" git config user.name
echo "== E12 includeIf (condition not matching) still read? gitdir:/nonmatching/"
D=$S/e12; mkdir -p $D; git -C $D init -q; printf '[includeIf "gitdir:/nonmatching/"]\n\tpath = %s\n' "$OUT/inc.cfg" >> $D/.git/config
run "E12a includeIf non-matching gitdir (file opened?)" $D "$OUT" git config user.name
printf '[includeIf "onbranch:nonexistent"]\n\tpath = %s\n' "$OUT/inc.cfg" > $D/.git/config.tmp; cat $D/.git/config.tmp >> $D/.git/config
run "E12b + onbranch non-matching" $D "$OUT" git config user.name
echo "== E13 alternates (real target)"
D=$S/e5; run "E13a rev-parse --git-dir" $D "e5altobjs" git rev-parse --git-dir
run "E13b status" $D "e5altobjs" git status --short
run "E13c cat-file -t <missing sha>" $D "e5altobjs" git cat-file -t deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
run "E13d rev-parse HEAD (unborn)" $D "e5altobjs" git rev-parse HEAD
git -C $D -c user.name=a -c user.email=a@b commit -q --allow-empty -m x
run "E13e rev-parse HEAD (born)" $D "e5altobjs" git rev-parse HEAD
run "E13f cat-file -t HEAD (found locally)" $D "e5altobjs" git cat-file -t HEAD
echo "== E14 gitfile to outside: git reads target"
D=$S/e14; mkdir -p $D; echo "gitdir: $S/e1/.git" > $D/.git
run "E14a gitfile -> other repo with include" $D "$OUT" git rev-parse --git-dir
echo "== E15 tilde include expands HOME; GIT_CONFIG_GLOBAL=/dev/null does not stop repo include"
D=$S/e15; mkdir -p $D; git -C $D init -q; printf '[user]\n\tname = HOMELEAK\n' > $HOME/h.cfg; printf '[include]\n\tpath = ~/h.cfg\n' >> $D/.git/config
run "E15a ~ include" $D "$HOME/h.cfg" git config user.name
echo "== E16 core.worktree / core.bare / safe.directory: ownership check not applied to scratch (same uid)"
D=$S/e16; mkdir -p $D $S/e16-wt; git -C $D init -q; git -C $D config core.worktree $S/e16-wt
run "E16a core.worktree outside: git rev-parse --show-toplevel" $D "e16-wt" git rev-parse --show-toplevel

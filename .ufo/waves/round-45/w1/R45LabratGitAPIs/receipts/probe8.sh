#!/usr/bin/env bash
# R45LabratGitAPIs probe round 8: the base of a relative includeIf gitdir pattern (separate git dir),
# and confirm that ANY git probe of a repo reads that repo's config (setup read) regardless of flags.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe8
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
fired() { local l=$1 n=$2; shift 2; printf -- '--- %s\n' "$l"
  local log="$P/s.$$.$RANDOM.log"
  strace -f -qq -y -e trace=open,openat,openat2,creat -o "$log" "$@" >/dev/null 2>&1
  if grep -F -- "$n" "$log" >/dev/null; then printf '  FIRED (target opened)\n'; else printf '  not fired\n'; fi
  rm -f "$log"; }
mkrepo() { mkdir -p "$1"; git -C "$1" init -q -b master . >/dev/null 2>&1
  printf 'x\n' > "$1/file.txt"; git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm one >/dev/null 2>&1; }

hr "V1  relative includeIf gitdir : base = cwd? git dir? work tree? (separate git dir, absolute path)"
V1=$P/v1; mkdir -p "$V1/gd" "$V1/wt"
git init -q -b master --separate-git-dir "$V1/gd/gitdir" "$V1/wt/work" >/dev/null 2>&1
run "v1 .git file" cat "$V1/wt/work/.git"
run "v1 --absolute-git-dir" git -C "$V1/wt/work" rev-parse --absolute-git-dir
run "v1 --show-toplevel" git -C "$V1/wt/work" rev-parse --show-toplevel
printf '[user]\n\temail = OUTSIDE-V1@invalid\n' > "$V1/out.cfg"
for pat in "wt/work/.git" "work/.git" "gd/gitdir" "gitdir" "wt/work" "work"; do
  printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$pat" "$V1/out.cfg" >> "$V1/gd/gitdir/config"
  printf -- '--- pattern "%s"  (cwd=V1)\n' "$pat"
  fired "v1 probe (cwd=V1)" "$V1/out.cfg" git -C "$V1" rev-parse --show-toplevel
done

hr "V2  relative includeIf gitdir : base tested with a plain repo (no separate git dir)"
V2=$P/v2; mkdir -p "$V2"; mkrepo "$V2/lane"
printf '[user]\n\temail = OUTSIDE-V2@invalid\n' > "$V2/out.cfg"
for pat in "lane/.git" "v2/lane/.git" "lane" "lane/"; do
  printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$pat" "$V2/out.cfg" >> "$V2/lane/.git/config"
  printf -- '--- pattern "%s"  (cwd=V2)\n' "$pat"
  fired "v2 probe (cwd=V2)" "$V2/out.cfg" git -C "$V2" rev-parse --show-toplevel
  fired "v2 probe (cwd=V2/lane)" "$V2/out.cfg" git -C "$V2/lane" rev-parse --show-toplevel
done

hr "V3  does EVERY git probe of a repo read its config? (include target opened even with --no-includes)"
V3=$P/v3; mkdir -p "$V3"; mkrepo "$V3/d"
printf '[include]\n\tpath = %s\n' "$V3/out.cfg" >> "$V3/d/.git/config"
printf '[user]\n\temail = OUTSIDE-V3@invalid\n' > "$V3/out.cfg"
mkdir -p "$V3/elsewhere"
for c in "rev-parse --show-toplevel" "rev-parse --absolute-git-dir" "rev-parse --git-common-dir" \
         "config --local --no-includes --get-regexp ^include(if)?\\." "status --porcelain" \
         "cat-file -t HEAD" "log --oneline -1"; do
  printf -- '--- git %s   (cwd = the repo)\n' "$c"
  fired "v3" "$V3/out.cfg" git -C "$V3/d" $c
done
printf -- '--- git rev-parse --show-toplevel   (cwd = elsewhere, GIT_DIR explicit)\n'
fired "v3 GIT_DIR" "$V3/out.cfg" env GIT_DIR="$V3/d/.git" GIT_WORK_TREE="$V3/d" git -C "$V3/elsewhere" rev-parse --show-toplevel

hr "V4  core.worktree RELATIVE : which git calls fail?"
V4=$P/v4; mkdir -p "$V4"; mkrepo "$V4/d"
git -C "$V4/d" config core.worktree "../wt"
for c in "rev-parse --show-toplevel" "rev-parse --absolute-git-dir" "rev-parse --git-common-dir" \
         "config --local --no-includes --get core.worktree" "config --local --no-includes --get-regexp ^include(if)?\\."; do
  printf -- '--- git %s\n' "$c"
  git -C "$V4/d" $c 2>&1 | sed 's/^/    /'; printf '    [rc=%s]\n' "${PIPESTATUS[0]}"
done
printf -- '--- text of .git/config (a pure read never fails)\n'
cat "$V4/d/.git/config" | sed 's/^/    /'

hr "DONE"

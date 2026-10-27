#!/usr/bin/env bash
# R45LabratGitAPIs probe round 11: isolate the relative [includeIf "gitdir:"] base; confirm path-format needs.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe11
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
  if grep -F -- "$n" "$log" >/dev/null; then printf '  OPENED (fired)\n'; else printf '  not opened\n'; fi
  rm -f "$log"; }
mkrepo() { mkdir -p "$1"; git -C "$1" init -q -b master . >/dev/null 2>&1
  printf 'x\n' > "$1/file.txt"; git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm one >/dev/null 2>&1; }

hr "Y1  relative gitdir: base = cwd? toplevel-parent? gitdir-parent? (one pattern per repo, isolated)"
Y1=$P/y1; mkdir -p "$Y1"
# layout per case:  <case>/repo/.git   (toplevel = <case>/repo, gitdir = <case>/repo/.git)
#   cwd candidates:   <case>            (toplevel's parent)
#                     <case>/repo       (toplevel == gitdir's parent)
#                     <case>/repo/sub   (deeper inside the work tree)
probe() { # probe <case> <pattern> <cwd>
  local nm=$1 pat=$2 cw=$3
  mkdir -p "$Y1/$nm"; mkrepo "$Y1/$nm/repo"; mkdir -p "$Y1/$nm/repo/sub"
  printf '[user]\n\temail = OUT@invalid\n' > "$Y1/$nm/out.cfg"
  printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$pat" "$Y1/$nm/out.cfg" >> "$Y1/$nm/repo/.git/config"
  printf -- '--- case %s pattern=%s cwd=%s\n' "$nm" "$pat" "$cw"
  opened "   probe" "$Y1/$nm/out.cfg" git -C "$Y1/$cw" rev-parse --show-toplevel
}
probe b_cwd     "repo/.git"        "b_cwd"          # base = cwd (= toplevel's parent)
probe b_tp      "../repo/.git"     "b_tp/repo/sub"  # base = cwd (deeper): ../repo/.git from <case>/repo/sub = <case>/repo/repo/.git (no)
probe b_tp2     "../../repo/.git"  "b_tp2/repo/sub" # base = cwd(deeper): ../../repo/.git = <case>/repo/.git  <- MATCHES if base=cwd
probe b_gd      ".git"             "b_gd/repo"      # base = gitdir's parent (== toplevel): .git
probe b_gd2     "repo/.git"        "b_gd2/repo"     # base = toplevel (== gitdir parent): repo/.git -> <case>/repo/repo/.git (no)

hr "Y2  the ABSOLUTE gitdir: pattern : exact match on the git dir path"
Y2=$P/y2; mkdir -p "$Y2"; mkrepo "$Y2/repo"
printf '[user]\n\temail = OUT@invalid\n' > "$Y2/out.cfg"
printf '[includeIf "gitdir:%s"]\n\tpath = %s\n' "$Y2/repo/.git" "$Y2/out.cfg" >> "$Y2/repo/.git/config"
opened "y2 absolute exact gitdir (cwd=Y2)" "$Y2/out.cfg" git -C "$Y2" rev-parse --show-toplevel
opened "y2 absolute exact gitdir (cwd=Y2/repo)" "$Y2/out.cfg" git -C "$Y2/repo" rev-parse --show-toplevel

hr "Y3  git rev-parse --git-common-dir : RELATIVE output when no commondir (path-format needed)"
Y3=$P/y3; mkdir -p "$Y3"; mkrepo "$Y3/d"
run "y3 --git-common-dir (plain)" git -C "$Y3/d" rev-parse --git-common-dir
run "y3 --path-format=absolute --git-common-dir" git -C "$Y3/d" rev-parse --path-format=absolute --git-common-dir

hr "Y4  relative include.path base : the .git directory (not the work tree)"
Y4=$P/y4; mkdir -p "$Y4"; mkrepo "$Y4/d"
mkdir -p "$Y4/d/.git"; printf '[user]\n\temail = OUT@invalid\n' > "$Y4/d/.git/rel.cfg"
printf '[user]\n\temail = OUT@invalid\n' > "$Y4/d/rel.cfg"
printf '[include]\n\tpath = rel.cfg\n' >> "$Y4/d/.git/config"
opened "y4 which rel.cfg is opened? (.git/rel.cfg)" "$Y4/d/.git/rel.cfg" git -C "$Y4/d" rev-parse --show-toplevel
run "y4 config --list --show-origin" git -C "$Y4/d" config --list --show-origin

hr "Y5  relative commondir base : the git dir (not the work tree)"
Y5=$P/y5; mkdir -p "$Y5"
mkdir -p "$Y5/d/.git"; printf 'ref: refs/heads/master\n' > "$Y5/d/.git/HEAD"
printf 'storeA\n' > "$Y5/d/.git/commondir"
git init -q -b master --bare "$Y5/d/.git/storeA" >/dev/null 2>&1
run "y5 --git-common-dir" git -C "$Y5/d" rev-parse --git-common-dir
run "y5 --path-format=absolute --git-common-dir" git -C "$Y5/d" rev-parse --path-format=absolute --git-common-dir

hr "DONE"

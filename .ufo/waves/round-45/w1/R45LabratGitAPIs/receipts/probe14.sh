#!/usr/bin/env bash
# R45LabratGitAPIs probe round 14: simulate the round-45 counter's OWN outside-open counting rule
# (plans/round45_c1_verify.py run_fence: OPEN_RE / DONE_RE / UNFINISHED_RE / scratch=(root/fx, root/btmp))
# against candidate fence detection strategies, on a realistic fx/ layout.
set -u
P=/fast/scratch/hyaku/kengaku-r45/R45LabratGitAPIs/probe14
rm -rf "$P"; mkdir -p "$P"; cd "$P" || exit 1
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null HOME=/nonexistent
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@example.invalid
export GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@example.invalid
hr() { printf '\n===== %s =====\n' "$*"; }

# lay out the counter's scratch shape: root/fx/<module>/f000 = d ; root/btmp/<module>
ROOT=$P/root
mkdir -p "$ROOT/fx/mod/f000/d/lane" "$ROOT/btmp/mod" "$ROOT/fx/mod/outside"
D="$ROOT/fx/mod/f000/d"
# an ANCESTOR repo at d.parent (the f6 shape): d.parent = .../f000
git init -q -b master "$ROOT/fx/mod/f000" >/dev/null 2>&1
# a hostile include target OUTSIDE d but under the scratch (the f10 shape)
printf '[user]\n\temail = OUTSIDE@invalid\n' > "$ROOT/fx/mod/f000/inc.cfg"

cat > "$P/count.py" <<'PYEOF'
import pathlib, re, sys
OPEN_RE = re.compile(r"\bopen(?:at|at2)?\(|creat\(")
DONE_RE = re.compile(r"=\s+(-?\d+|E[A-Z]+)(?:<(.+)>)?\s*$")
UNFINISHED_RE = re.compile(r"(<unfinished \.\.\.>|=\s*\?)\s*$")
RESUMED_RE = re.compile(r"^\s*(\d+)\s*<\.\.\.\s+\w+\s+resumed>")
root, d = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
scratch = (root / "fx", root / "btmp")
opens, first = 0, ""
pending = {}
for line in pathlib.Path(sys.argv[3]).read_text(errors="replace").splitlines():
    pidm = re.match(r"^\s*(\d+)", line)
    pid = pidm.group(1) if pidm else "-"
    if RESUMED_RE.search(line):
        pending.pop(pid, None)
    if not OPEN_RE.search(line):
        continue
    if UNFINISHED_RE.search(line):
        pending[pid] = line
        continue
    done = DONE_RE.search(line)
    if not done or done.group(1).startswith("E") or done.group(1).startswith("-"):
        continue
    p = pathlib.Path(done.group(2) or "")
    if any(p == s or p.is_relative_to(s) for s in scratch) and not (p == d or p.is_relative_to(d)):
        opens += 1
        first = first or str(p)
for line in pending.values():
    for m in re.finditer(r'"(/[^"]+)"', line):
        p = pathlib.Path(m.group(1))
        if any(p == s or p.is_relative_to(s) for s in scratch) and not (p == d or p.is_relative_to(d)):
            opens += 1
            first = first or str(p)
            break
print(f"outside_opens={opens} first={first or '-'}")
PYEOF

count() { # count <label> <cmd...>
  local lbl=$1; shift
  local log="$P/t.$$.$RANDOM.log"
  strace -f -qq -y -e trace=open,openat,openat2,creat -o "$log" "$@" >/dev/null 2>&1
  printf -- '--- %s\n' "$lbl"
  python3 "$P/count.py" "$ROOT" "$D" "$log"
  rm -f "$log"; }

hr "S1  candidate A : STAT-ONLY ancestor detection (no listing of the ancestor dir)"
cat > "$P/statonly.py" <<'PYEOF'
import pathlib, sys
d = pathlib.Path(sys.argv[1]).resolve()
anc = d.parent
hits = []
while anc != anc.parent:
    if (anc / ".git").exists():          # stat only
        hits.append(str(anc / ".git"))
    anc = anc.parent
print("ancestor_git=" + ",".join(hits))
PYEOF
count "S1 stat-only ancestor walk" python3 "$P/statonly.py" "$D"

hr "S2  candidate B : LISTDIR-based ancestor detection (lists each ancestor dir)"
cat > "$P/listdir.py" <<'PYEOF'
import os, pathlib, sys
d = pathlib.Path(sys.argv[1]).resolve()
anc = d.parent
while anc != anc.parent:
    if ".git" in os.listdir(anc):        # opens the ancestor DIRECTORY
        print("hit", anc)
    anc = anc.parent
PYEOF
count "S2 listdir ancestor walk" python3 "$P/listdir.py" "$D"

hr "S3  candidate C : a git probe with ceiling=d.parent (the ancestor repo at d.parent)"
count "S3 git -C d rev-parse --show-toplevel, ceiling=d.parent" \
  env GIT_CEILING_DIRECTORIES="$D/.." git -C "$D" rev-parse --show-toplevel
count "S3b git -C d rev-parse --show-toplevel, NO ceiling" \
  git -C "$D" rev-parse --show-toplevel
count "S3c git -C d/lane rev-parse --show-toplevel, NO ceiling" \
  git -C "$D/lane" rev-parse --show-toplevel

hr "S4  candidate D : TEXT SCAN of .git/config for an include (pure read, inside d)"
cat > "$P/scan.py" <<'PYEOF'
import pathlib, sys
d = pathlib.Path(sys.argv[1])
for p in sorted(d.rglob(".git/config*")):
    t = p.read_text(errors="replace")
    if "[include" in t or "[includeif" in t.lower():
        print("include-section", p)
PYEOF
count "S4 text scan of .git/config*" python3 "$P/scan.py" "$D"

hr "S5  candidate E : git config --local --no-includes on a repo whose config has an include"
git init -q -b master "$D/lane" >/dev/null 2>&1
printf '[include]\n\tpath = %s\n' "$ROOT/fx/mod/f000/inc.cfg" >> "$D/lane/.git/config"
count "S5 git config --local --no-includes --get-regexp include" \
  git -C "$D/lane" config --local --no-includes --get-regexp '^include(if)?\.'
count "S5b git rev-parse --show-toplevel in the same repo" git -C "$D/lane" rev-parse --show-toplevel

hr "S6  candidate F : git --git-dir probe (bypasses discovery)"
count "S6 git --git-dir=d/lane/.git --work-tree=d/lane rev-parse --show-toplevel" \
  git --git-dir="$D/lane/.git" --work-tree="$D/lane" rev-parse --show-toplevel

hr "DONE"

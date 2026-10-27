#!/usr/bin/env bash
# Envelope v3 red/green driver (seat R44EnvelopeV3). Everything under $S; ~/.local/bin is only ever READ.
#   usage: driver.sh <scratch S> <draft envelope> <old envelope copy with remapped target>
set -u
S=$1; DRAFT=$2; OLD=$3
W=$S/work
rm -rf "$W"; mkdir -p "$W"

mkfixture() {  # $1 = dir; rich fixture incl. the shapes that must not false-fire
  local d=$1
  mkdir -p "$d/sub"
  printf 'alpha-content\n' > "$d/real-tool"; chmod 755 "$d/real-tool"
  printf 'beta-content\n'  > "$d/plain";     chmod 644 "$d/plain"
  printf 'gamma-secret\n'  > "$d/secret";    chmod 000 "$d/secret"
  ln -s real-tool "$d/link-tool"
  printf 'inner\n' > "$d/sub/inner"
  ln -s /nonexistent-target "$d/broken"
  ln -s loop "$d/loop"
  ln -s sub "$d/dirlink"
  mkfifo "$d/fifo"
}

case_run() {  # $1=id $2=envelope $3=mutation shell command ("" = no-op)
  local id=$1 env=$2 mut=$3 dir=$W/$1/target scr=$W/$1/scr
  mkdir -p "$W/$1" "$scr"
  mkfixture "$dir"
  if [ -z "$mut" ]; then
    ENVELOPE_BINDIR="$dir" "$env" "$scr" /bin/true > "$W/$1/out.txt" 2>&1
  else
    ENVELOPE_BINDIR="$dir" "$env" "$scr" /bin/sh -c "cd '$dir' && $mut" > "$W/$1/out.txt" 2>&1
  fi
  echo "RC=$?" >> "$W/$1/out.txt"
}

M1='printf "evil-backdoor\n" > real-tool'                                   # content rewrite
M2='printf "planted\n" > planted-tool'                                     # new file
M3='ln -sfn other-target link-tool'                                        # symlink retarget
M4='chmod 700 plain'                                                       # mode-only (644 -> 700)
M5='chmod 600 secret; printf "stolen-secret\n" > secret; chmod 000 secret'  # rewrite of a mode-000 entry, mode restored
M6='setfattr -n user.tag -v evil real-tool'                                # xattr
N0=''                                                                      # negative control: no mutation

for pair in "M1:$M1" "M2:$M2" "M3:$M3" "M4:$M4" "M5:$M5" "M6:$M6" "N0:$N0"; do
  id=${pair%%:*}; mut=${pair#*:}
  case_run "new-$id" "$DRAFT" "$mut"
  case_run "old-$id" "$OLD" "$mut"
done

# v3-specific negative controls, same rich fixture
mkdir -p "$W/nc-a" "$W/nc-a/scr"; mkfixture "$W/nc-a/target"
ENVELOPE_BINDIR="$W/nc-a/target" "$DRAFT" "$W/nc-a/scr" /bin/true > "$W/nc-repeat.txt" 2>&1; echo "RC=$?" >> "$W/nc-repeat.txt"
ENVELOPE_BINDIR="$W/nc-a/target" "$DRAFT" "$W/nc-b/scr" /bin/false > "$W/nc-exit.txt" 2>&1; echo "RC=$?" >> "$W/nc-exit.txt"
mkdir -p "$W/nc-b/scr"
mkdir -p "$W/nc-absent/scr"
ENVELOPE_BINDIR="$W/no-such-dir" "$DRAFT" "$W/nc-absent/scr" /bin/true > "$W/nc-absent.txt" 2>&1; echo "RC=$?" >> "$W/nc-absent.txt"
mkdir -p "$W/nc-link/scr"; ln -sfn "$W/nc-a/target" "$W/nc-linkdir"
ENVELOPE_BINDIR="$W/nc-linkdir" "$DRAFT" "$W/nc-link/scr" /bin/true > "$W/nc-link.txt" 2>&1; echo "RC=$?" >> "$W/nc-link.txt"

# real watched dir (read-only; default target), timed
mkdir -p "$W/real-scr"
t0=$(date +%s%N)
"$DRAFT" "$W/real-scr" /bin/true > "$W/real.txt" 2>&1; rc=$?
t1=$(date +%s%N)
printf 'RC=%s\nREAL_WALL_MS=%s\n' "$rc" "$(( (t1 - t0) / 1000000 ))" >> "$W/real.txt"

# watched path is a regular file (loud INVALID expected)
printf 'not-a-dir\n' > "$W/plainfile"
mkdir -p "$W/nc-file/scr"
ENVELOPE_BINDIR="$W/plainfile" "$DRAFT" "$W/nc-file/scr" /bin/true > "$W/nc-file.txt" 2>&1; echo "RC=$?" >> "$W/nc-file.txt"

# watched path is a symlink to a directory: link field recorded, digest over the resolved tree
mkdir -p "$W/nc-sym/scr"; mkfixture "$W/nc-symA"
ln -sfn "$W/nc-symA" "$W/nc-symB"
ENVELOPE_BINDIR="$W/nc-symB" "$DRAFT" "$W/nc-sym/scr" /bin/true > "$W/nc-symlinkroot.txt" 2>&1; echo "RC=$?" >> "$W/nc-symlinkroot.txt"

# retarget the watched symlink at an identical tree: the header link/ino must change the digest
mkdir -p "$W/m7/scr" "$W/m7/targetA" "$W/m7/targetB"; mkfixture "$W/m7/targetA"; mkfixture "$W/m7/targetB"
ln -sfn "$W/m7/targetA" "$W/m7/watched"
ENVELOPE_BINDIR="$W/m7/watched" "$DRAFT" "$W/m7/scr" /bin/sh -c "ln -sfn '$W/m7/targetB' '$W/m7/watched'" > "$W/m7/out.txt" 2>&1; echo "RC=$?" >> "$W/m7/out.txt"

# old envelope on the real watched dir (parity timing, read-only)
mkdir -p "$W/oldreal-scr"
t0=$(date +%s%N); "$OLD" "$W/oldreal-scr" /bin/true > "$W/oldreal.txt" 2>&1; rc=$?; t1=$(date +%s%N)
printf 'RC=%s\nREAL_WALL_MS=%s\n' "$rc" "$(( (t1 - t0) / 1000000 ))" >> "$W/oldreal.txt"

# extras: nested change under an existing subdir, and a mode-only flip of the watched dir itself
case_run "new-M8" "$DRAFT" 'printf "injected\n" > sub/injected'
case_run "old-M8" "$OLD"   'printf "injected\n" > sub/injected'
case_run "new-M9" "$DRAFT" 'chmod 750 .'
case_run "old-M9" "$OLD"   'chmod 750 .'

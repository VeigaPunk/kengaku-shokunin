#!/usr/bin/env bash
# Reproduce the three fixture measurements cited by F39EntryQuotes.md.
set -u
R=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-39/falsify/F39EntryQuotes
S=/fast/scratch/hyaku/kengaku-r39/F39EntryQuotes
export TMPDIR=$S

###
{ git --version
  D=$(mktemp -d -p "$S")
  echo "D=$D (fresh repo, challenge-setup.sh recipe)"
  git -C "$D" init -q
  git -C "$D" config user.name TB
  git -C "$D" config user.email tb@example.com
  (
    cd "$D" || exit 1
    echo "demo project" > README.md
    git add README.md
    git commit -q -m "chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc"
    echo "secret[lost_and_found_in_git]" > secret.txt
    git add secret.txt
    git commit -q -m "feat: add scratch notes"
    git reset -q --hard HEAD~1
    echo "some changes" >> README.md
    git add README.md
    git commit -q -m "chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc"
  )
  echo "--- state A: reflog alive (the task's initial state)"
  echo '$ git fsck';                 git -C "$D" fsck;              echo "rc=$?"
  echo '$ git fsck --lost-found';    git -C "$D" fsck --lost-found; echo "rc=$?"
  echo '$ git fsck --unreachable';   git -C "$D" fsck --unreachable; echo "rc=$?"
  echo '$ git fsck --no-reflogs --unreachable'; git -C "$D" fsck --no-reflogs --unreachable; echo "rc=$?"
  echo '$ git fsck --lost-found --unreachable'; git -C "$D" fsck --lost-found --unreachable; echo "rc=$?"
  C=$(git -C "$D" fsck --lost-found | sed -n 's/^dangling commit //p')
  echo "dangling commit = $C"
  echo "\$ git cat-file -p $C"
  git -C "$D" cat-file -p "$C"
  echo "\$ git cat-file -p $C | grep -c 'secret['"
  git -C "$D" cat-file -p "$C" | grep -c 'secret\[' || true
  echo "\$ git show $C | grep -o 'secret[^]]*]'"
  git -C "$D" show "$C" | grep -o 'secret\[[^]]*\]'
  echo "--- state B: after git reflog expire --expire=now --all"
  git -C "$D" reflog expire --expire=now --all
  echo '$ git fsck --lost-found';  git -C "$D" fsck --lost-found
  echo '$ git fsck --unreachable'; git -C "$D" fsck --unreachable
  rm -rf "$D"
} > "$R/fsck-fixture.txt" 2>&1

###
{ D=$(mktemp -d -p "$S")
  echo "D=$D (stash fixture)"
  git -C "$D" init -q
  git -C "$D" config user.name TB
  git -C "$D" config user.email tb@example.com
  (
    cd "$D" || exit 1
    printf 'demo project\n' > README.md
    git add README.md
    git commit -q -m "chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc"
    echo "some changes" >> README.md
    git add README.md
    git commit -q -m "chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc"
    printf 'demo project\nsome changes\nsecret[lost_and_found_in_git]\n' > README.md
    git stash -q
  )
  echo '$ git log --oneline --all'
  git -C "$D" log --oneline --all
  echo '$ git log --all --grep "secret\[" --regexp-ignore-case'
  git -C "$D" log --all --grep 'secret\[' --regexp-ignore-case; echo "rc=$?"
  echo '$ git log --all -p -S "secret["'
  git -C "$D" log --all -p -S 'secret['; echo "rc=$?"
  echo '$ git rev-parse refs/stash'; git -C "$D" rev-parse refs/stash
  echo '$ git cat-file -p refs/stash'; git -C "$D" cat-file -p refs/stash
  rm -rf "$D"
} > "$R/stash-logall.txt" 2>&1

###
{ D=$(mktemp -d -p "$S")
  echo "D=$D (checksum-sensitivity fixture; the grader's own sh -c, path substituted)"
  git -C "$D" init -q
  ( cd "$D" || exit 1; echo "demo project" > README.md )
  CMD() { sh -c "find $D -type f -not -path '*/\.*' -exec sha256sum {} + | sort | sha256sum"; }
  echo "baseline            $(CMD)"
  mkdir -p "$D/newdir/subdir";      echo "after empty dir     $(CMD)"
  ln -s README.md "$D/link";        echo "after symlink       $(CMD)"
  chmod 600 "$D/README.md";         echo "after chmod 600     $(CMD)"
  mkfifo "$D/fifo1";                echo "after fifo          $(CMD)"
  echo note > "$D/NEWFILE.md";      echo "after new reg. file $(CMD)"
  echo "--- /app/secret.txt is outside the find root by construction: find is scoped to /app/repo only (test_outputs.py:101)"
  rm -rf "$D"
} > "$R/checksum-sensitivity.txt" 2>&1
echo done

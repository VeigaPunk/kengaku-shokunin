#!/usr/bin/env bash
# CriticClaims fixture attacks on the R94-C2 gate v2 (tabled bytes at T 90c7677f). Fixtures only.
S=/fast/scratch/hyaku/kengaku-r94/CriticClaims
GATE="$S/lane/plans/round94_freeze_integrity.py"
ID=(-c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false)
newrepo() { rm -rf "$1"; mkdir -p "$1"; git -C "$1" init -q -b main; top=$(git -C "$1" rev-parse --show-toplevel); [ "$top" = "$1" ] || { echo "TOPLEVEL MISMATCH $top"; exit 1; }; }
commit() { git -C "$1" add -A && git -C "$1" "${ID[@]}" commit -q -m "$2" && git -C "$1" rev-parse HEAD; }
gate() { python3 "$GATE" --lane "$1" --freeze "$2" --rev "$3" --claims "$4" --work "$5" | grep -E "INSTRUMENT|FREEZE-INTEGRITY|PREDICATE"; echo "rc=${PIPESTATUS[0]}"; }

echo "## A. edit then revert, plus refs/replace graft of the edit commit"
D="$S/fx-a"; newrepo "$D"; printf 'def count():\n    return 3\n' > "$D/probe.py"
H=$(sha256sum "$D/probe.py" | cut -c1-64); printf '# claims\n\n```frozen-instruments\n%s  probe.py\n```\n' "$H" > "$D/claims.md"
F=$(commit "$D" freeze); printf 'def count():\n    return 4\n' > "$D/probe.py"; E=$(commit "$D" edit)
printf 'def count():\n    return 3\n' > "$D/probe.py"; T1=$(commit "$D" revert)
echo "A0 honest history (no replace refs):"; gate "$D" "$F" "$T1" claims.md "$S/w-a0"
E2=$(git -C "$D" "${ID[@]}" commit-tree "$(git -C "$D" rev-parse "$F^{tree}")" -p "$F" -m "edit (replaced, empty diff)")
git -C "$D" replace "$E" "$E2"; echo "A1 replace refs present: $(git -C "$D" for-each-ref refs/replace | wc -l)"
echo "A1 gate, default (replace honored):"; gate "$D" "$F" "$T1" claims.md "$S/w-a1"
echo "A2 control, GIT_NO_REPLACE_OBJECTS=1:"; GIT_NO_REPLACE_OBJECTS=1 gate "$D" "$F" "$T1" claims.md "$S/w-a2"

echo "## B. spelled duplicate row (./probe.py next to probe.py), after an edit"
D="$S/fx-b"; newrepo "$D"; printf 'def count():\n    return 3\n' > "$D/probe.py"
H=$(sha256sum "$D/probe.py" | cut -c1-64); printf '# claims\n\n```frozen-instruments\n%s  probe.py\n%s  ./probe.py\n```\n' "$H" "$H" > "$D/claims.md"
F=$(commit "$D" freeze); printf 'def count():\n    return 4\n' > "$D/probe.py"; T1=$(commit "$D" edit)
gate "$D" "$F" "$T1" claims.md "$S/w-b"

echo "## C. second table block with four-backtick and tilde fences naming notes.md (edited after freeze)"
D="$S/fx-c"; newrepo "$D"; printf 'def count():\n    return 3\n' > "$D/probe.py"; printf 'notes\n' > "$D/notes.md"
H=$(sha256sum "$D/probe.py" | cut -c1-64); HN=$(sha256sum "$D/notes.md" | cut -c1-64)
printf '# claims\n\n```frozen-instruments\n%s  probe.py\n```\n\n````frozen-instruments\n%s  notes.md\n````\n' "$H" "$HN" > "$D/claims-four.md"
printf '# claims\n\n```frozen-instruments\n%s  probe.py\n```\n\n~~~frozen-instruments\n%s  notes.md\n~~~\n' "$H" "$HN" > "$D/claims-tilde.md"
git -C "$D" add -A && git -C "$D" "${ID[@]}" commit -q -m freeze && F=$(git -C "$D" rev-parse HEAD)
printf 'notes changed\n' > "$D/notes.md"; T1=$(commit "$D" edit-notes)
echo "C1 four-backtick second block:"; gate "$D" "$F" "$T1" claims-four.md "$S/w-c1"
echo "C2 tilde second block:"; gate "$D" "$F" "$T1" claims-tilde.md "$S/w-c2"
echo "C3 control, notes.md in the one honored block (committed at freeze), same edit:"; D3="$S/fx-c3"; newrepo "$D3"; printf 'def count():\n    return 3\n' > "$D3/probe.py"; printf 'notes\n' > "$D3/notes.md"
H3=$(sha256sum "$D3/probe.py" | cut -c1-64); HN3=$(sha256sum "$D3/notes.md" | cut -c1-64)
printf '# claims\n\n```frozen-instruments\n%s  probe.py\n%s  notes.md\n```\n' "$H3" "$HN3" > "$D3/claims.md"
F3=$(commit "$D3" freeze); printf 'notes changed\n' > "$D3/notes.md"; T3=$(commit "$D3" edit-notes)
gate "$D3" "$F3" "$T3" claims.md "$S/w-c3"

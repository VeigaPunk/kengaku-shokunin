#!/bin/sh
# §10 id-collision check — scratch receipt for kengaku round 36 (seat R36IdGuard).
#
# Usage:
#   id-collision-check.sh            real run: lane registry vs held staged package
#   id-collision-check.sh --selftest fixture proof (indented S002 row must collide)
#
# Contract anchor (0-3 leading ASCII spaces, the census parser's own allowance):
#   ^ {0,3}\|[[:space:]]*S[0-9]{3,}
# Exit: 0 clean, 3 collisions present, 2 input absent/empty/anchor-silent.
# The bare shell pipeline false-greens on a missing registry (grep -> empty list,
# comm -> 0 rows, status 0). This wrapper refuses instead.
set -eu
ANCH='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kengaku-shokunin}
A=${A:-$LANE/.ufo/waves/round-36/assimilation}
REG=${REG:-$LANE/corpus/SOURCES.md}
STAGED=${STAGED:-/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md}

ids_of() { # $1 file, $2 out
  [ -f "$1" ] || { echo "REFUSED: input absent: $1" >&2; exit 2; }
  grep -oE "$ANCH" "$1" | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > "$2" || true
  [ -s "$2" ] || { echo "REFUSED: anchor matched no row in $1" >&2; exit 2; }
}

if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d /tmp/k36-guard-XXXXXX); trap 'rm -rf "$T"' EXIT
  printf '  | S002 | indented collision bait | code |\n| S900 | control | code |\n' > "$T/reg.md"
  printf '| S002 | staged twin | code |\n| S901 | no twin | code |\n' > "$T/staged.md"
  printf '    | S003 | four-space code row | code |\n   | S004 | three-space row | code |\n' > "$T/indent.md"
  ids_of "$T/reg.md" "$T/reg"; ids_of "$T/staged.md" "$T/staged"; ids_of "$T/indent.md" "$T/indent"
  LC_ALL=C comm -12 "$T/reg" "$T/staged" > "$T/coll"
  grep -oE '^[|][[:space:]]*S[0-9]{3,}' "$T/reg.md" | grep -oE 'S[0-9]{3,}' | LC_ALL=C sort -u > "$T/reg-bad"
  LC_ALL=C comm -12 "$T/reg-bad" "$T/staged" > "$T/coll-bad"
  printf 'SELFTEST reg=[%s] staged=[%s] indent=[%s] collisions=[%s] bad-anchor-collisions=%s\n' \
    "$(tr '\n' ' ' < "$T/reg")" "$(tr '\n' ' ' < "$T/staged")" \
    "$(tr '\n' ' ' < "$T/indent")" "$(tr '\n' ' ' < "$T/coll")" "$(wc -l < "$T/coll-bad")"
  [ -s "$T/coll" ] || { echo "SELFTEST FAIL: indented collision missed"; exit 1; }
  [ ! -s "$T/coll-bad" ] || { echo "SELFTEST FAIL: bad anchor should miss it"; exit 1; }
  grep -qx S004 "$T/indent" || { echo "SELFTEST FAIL: 3-space row must parse"; exit 1; }
  grep -qx S003 "$T/indent" && { echo "SELFTEST FAIL: 4-space row must not parse"; exit 1; }
  echo "SELFTEST guard-ok"; exit 0
fi

ids_of "$REG" "$A/reg-ids"
ids_of "$STAGED" "$A/staged-ids"
LC_ALL=C comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
n=$(wc -l < "$A/collisions")
echo "reg-ids=$(wc -l < "$A/reg-ids") staged-ids=$(wc -l < "$A/staged-ids") collisions=$n"
[ "$n" -eq 0 ] || exit 3

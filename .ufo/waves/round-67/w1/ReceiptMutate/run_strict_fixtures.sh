#!/bin/sh
# run_strict_fixtures.sh -- R67-C2 strict-gate mutation corpus runner.
#
# Usage: sh run_strict_fixtures.sh <path-to-strict-capable-checker>
#
# For every row of fixtures/expected.tsv (tab-separated columns: file, clause,
# expected_rc) the runner executes
#
#     python3 <checker> --check-receipt <fixture> --strict
#
# and compares the observed exit status with expected_rc.  A row is PASS only
# when the exit status matches AND (for a non-zero expectation) the output
# carries a `CHECK defect` line: an uncaught Python traceback also exits 1 and
# must never be recorded as a gate verdict.
#
# Exit 0: every row matched.  Exit 1: at least one mismatch.  Exit 2: the
# runner itself could not be set up (arguments, table, fixture, interpreter).
#
# The runner writes no files -- checker output is captured in shell variables,
# never under /tmp -- and it never touches the lane tree.
#
# Run it only against a checker whose --strict mode already exists.

set -u

usage() {
    printf 'usage: %s <path-to-strict-capable-checker>\n' "$0" >&2
    exit 2
}

[ "$#" -eq 1 ] || usage
checker=$1
[ -f "$checker" ] || { printf 'SETUP checker-missing %s\n' "$checker" >&2; exit 2; }

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd) || exit 2
fixtures_dir=$script_dir/fixtures
table=$fixtures_dir/expected.tsv
[ -f "$table" ] || { printf 'SETUP table-missing %s\n' "$table" >&2; exit 2; }

PY=${PYTHON:-python3}
command -v "$PY" >/dev/null 2>&1 || { printf 'SETUP python-missing %s\n' "$PY" >&2; exit 2; }

tab=$(printf '\t')
total=0
mismatches=0

while IFS=$tab read -r file clause expected_rc rest; do
    case ${file:-} in
        ''|'#'*|file) continue ;;
    esac

    total=$((total + 1))
    fixture=$fixtures_dir/$file
    if [ ! -f "$fixture" ]; then
        printf 'FIXTURE %s clause=%s expected_rc=%s observed_rc=missing FAIL\n' \
            "$file" "$clause" "$expected_rc"
        mismatches=$((mismatches + 1))
        continue
    fi

    out=$("$PY" "$checker" --check-receipt "$fixture" --strict 2>&1)
    observed_rc=$?

    verdict=PASS
    if [ "$observed_rc" != "$expected_rc" ]; then
        verdict=FAIL
    elif [ "$expected_rc" != 0 ]; then
        case $out in
            *'CHECK defect'*) ;;
            *) verdict=FAIL ;;
        esac
    fi

    printf 'FIXTURE %s clause=%s expected_rc=%s observed_rc=%s %s\n' \
        "$file" "$clause" "$expected_rc" "$observed_rc" "$verdict"
    if [ "$verdict" != PASS ]; then
        mismatches=$((mismatches + 1))
    fi
    if [ -n "$out" ]; then
        printf '%s\n' "$out" | sed 's/^/    | /'
    fi
done < "$table"

printf 'RESULT fixtures=%d mismatches=%d\n' "$total" "$mismatches"

[ "$total" -gt 0 ] || { printf 'SETUP table-empty %s\n' "$table" >&2; exit 2; }
[ "$mismatches" -eq 0 ] || exit 1
exit 0

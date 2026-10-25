#!/bin/sh
set -eu

fixtures=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
sandbox=/tmp/kengaku-r26-ExecGateTimingFixtures-sbx
marker=.r26-gate-timing-sandbox

if [ -e "$sandbox" ]; then
    if [ ! -f "$sandbox/$marker" ]; then
        printf 'refusing to replace unmarked path: %s\n' "$sandbox" >&2
        exit 2
    fi
    rm -rf -- "$sandbox"
fi
mkdir -p "$sandbox"
printf 'round-26 gate-timing disposable fixture repository\n' > "$sandbox/$marker"
git -C "$sandbox" init -q
git -C "$sandbox" config user.name 'R26 Gate Timing Fixture'
git -C "$sandbox" config user.email 'r26-gate-timing@example.invalid'

commit() {
    message=$1
    date=$2
    shift 2
    git -C "$sandbox" add -- "$@"
    GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" \
        git -C "$sandbox" commit -q --date="$date" -m "$message"
    git -C "$sandbox" rev-parse HEAD
}

# All cases share registered reader identities; report presence is the changed variable.
mkdir -p "$sandbox/.ufo/waves/round-26/falsify"
printf '%s\n' '{"members":{"SecondSeatA":{"role":"reviewer"},"SecondSeatC":{"role":"reviewer"},"SameSeatD":{"role":"reviewer"}}}' \
    > "$sandbox/.ufo/waves/round-26/falsify/swarm-registry.json"
base=$(commit base 2026-10-21T00:00:00Z "$marker" \
    .ufo/waves/round-26/falsify/swarm-registry.json)

# (a) The lesson and candidate land first; its cited second-seat report is
# introduced only by the next commit on this branch.
git -C "$sandbox" switch -q -c fixture-a-late-report
mkdir -p "$sandbox/corpus/lessons" "$sandbox/knowledge"
cp "$fixtures/late-report.md" "$sandbox/corpus/lessons/late-report.md"
printf '# Candidate A\nwriter: ClaimWriterA\n' > "$sandbox/knowledge/case-a.md"
a_landing=$(commit case-a-landing 2026-10-21T00:00:01Z \
    corpus/lessons/late-report.md knowledge/case-a.md)
mkdir -p "$sandbox/.ufo/waves/round-26/falsify"
printf '# Second-seat report\nseat: SecondSeatA\nReviewed knowledge/case-a.md.\nVERDICT: PASS\n' \
    > "$sandbox/.ufo/waves/round-26/falsify/SecondSeatA.md"
a_report=$(commit case-a-report-later 2026-10-21T00:00:02Z \
    .ufo/waves/round-26/falsify/SecondSeatA.md)

# Each remaining case branches from the empty baseline so unrelated reports
# cannot accidentally support a row that does not cite them.
git -C "$sandbox" switch -q --detach "$base"
git -C "$sandbox" switch -q -c fixture-b-generic-only
mkdir -p "$sandbox/corpus/lessons" "$sandbox/knowledge"
cp "$fixtures/generic-wave-2.md" "$sandbox/corpus/lessons/generic-wave-2.md"
printf '# Candidate B\nwriter: ClaimWriterB\n' > "$sandbox/knowledge/case-b.md"
b_generic=$(commit case-b-generic-only 2026-10-21T00:00:03Z \
    corpus/lessons/generic-wave-2.md knowledge/case-b.md)

git -C "$sandbox" switch -q --detach "$base"
git -C "$sandbox" switch -q -c fixture-c-same-commit
mkdir -p "$sandbox/corpus/lessons" "$sandbox/knowledge" \
    "$sandbox/.ufo/waves/round-26/falsify"
cp "$fixtures/same-commit-report.md" "$sandbox/corpus/lessons/same-commit-report.md"
printf '# Candidate C\nwriter: ClaimWriterC\n' > "$sandbox/knowledge/case-c.md"
printf '# Second-seat report\nseat: SecondSeatC\nReviewed knowledge/case-c.md.\nVERDICT: PASS\n' \
    > "$sandbox/.ufo/waves/round-26/falsify/SecondSeatC.md"
c_same=$(commit case-c-same-commit 2026-10-21T00:00:04Z \
    corpus/lessons/same-commit-report.md knowledge/case-c.md \
    .ufo/waves/round-26/falsify/SecondSeatC.md)

git -C "$sandbox" switch -q --detach "$base"
git -C "$sandbox" switch -q -c fixture-d-same-writer
mkdir -p "$sandbox/corpus/lessons" "$sandbox/knowledge" \
    "$sandbox/.ufo/waves/round-26/falsify"
cp "$fixtures/same-writer-report.md" "$sandbox/corpus/lessons/same-writer-report.md"
printf '# Candidate D\nwriter: SameSeatD\n' > "$sandbox/knowledge/case-d.md"
printf '# Report by the candidate writer\nauthor: SameSeatD\nseat: SameSeatD\nReviewed knowledge/case-d.md.\nVERDICT: PASS\n' \
    > "$sandbox/.ufo/waves/round-26/falsify/SameSeatD.md"
d_same=$(commit case-d-same-writer 2026-10-21T00:00:05Z \
    corpus/lessons/same-writer-report.md knowledge/case-d.md \
    .ufo/waves/round-26/falsify/SameSeatD.md)

printf 'sandbox=%s\n' "$sandbox"
printf 'base=%s\n' "$base"
printf 'case_a_landing=%s\ncase_a_report_later=%s\n' "$a_landing" "$a_report"
printf 'case_b_generic_only=%s\n' "$b_generic"
printf 'case_c_same_commit=%s\n' "$c_same"
printf 'case_d_same_writer=%s\n' "$d_same"
printf 'expected=FAIL,FAIL,PASS,FAIL\n'

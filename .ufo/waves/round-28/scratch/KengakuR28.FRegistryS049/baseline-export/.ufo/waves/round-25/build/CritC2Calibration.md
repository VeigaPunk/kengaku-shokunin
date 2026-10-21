# CritC2Calibration — adversarial review of C2 (round-25-claims.md:68-96); read-only.
Axes: novelty, calibration. Base `3f371d2a2ce5` (declared `6180e4f`, :3).

## F1 — P2d asserts the superseded table, not current state
`round-25-claims.md:82` fixes P2d as "`PROVINCE.md` `## Surfaces` rows (9)", but
`PROVINCE.md:97-100` declares that table retained verbatim as *historical* record —
superseded by `## Province map` `### Core`/`### Historical` (`:102-160`). `test -e`
today → ABSENT for the first paths of `PROVINCE.md:12,13,15,16,17` (`~/Projects/
webzites/…`, `~/archive/bench-arena/`, `~/Projects/bounties/…`, `~/.bailian/*`), no
`ABSENT` token on most rows → forced mismatches against a deliberately frozen table,
"closable" (`claims:90`) only by correcting what the supersession forbids. Sub-defects:
row `:14` is URL-first → `offline_unverifiable`, immunizing embedded local pins
(`/proc/1299/cmdline` absent today) — censorship-by-classification; row `:17` needs
brace expansion "tilde expanded" doesn't specify. Failure-capable against the wrong
slice — F9 mechanized (`kaika-w3/kengaku-review.md:140`).

## F2 — one genuine undisclosed defect exists at base (the checker can fire)
`corpus/lessons/round-24-verifier-spotcheck.md` exists; `grep -n verifier-spotcheck
corpus/README.md` → rc=1. P2e's file→row direction (`claims:85-86`) catches it:
mismatch=1 at base. Round 24's census exempted this class (`lessons_unindexed_
excl_round24`, `kengaku-review.md:32`), so the new check is strictly stronger than the
presence census (`plans/round24_census.sh:65-73`). Falsifiable: if `--summary` at
`git archive 6180e4f` reports mismatch=0, the instrument is blind as F9 predicted.

## F3 — P2a "expected token" extraction is unfrozen
`claims:76-77` pins no grammar; `SCORECARD.md:557`'s evidence cell mixes command output
with file facts ("receipts `corpus/evidence/round24-sources/gate.md`") → the assertion
set is authored at build time, not frozen at base. Same hole in P2b (`claims:79`):
`SCORECARD.md:610-616` name no executable commands. Exit-code semantics unpinned — today
`sources-census.sh validate --root … kengaku` → `kengaku ok`, exit 0 (pin it before the
tool drifts again, cf. F13 in the same review).

## F4 — frozen-P2 blind spot + environment coupling
"after = 0 mismatches on P2" (`claims:91`) never asserts rows added this round (`:75`),
so a false new assertion rides in unchecked; `unasserted=<n>` closes it. And P2c diffs
SHONEN's seed against `PROTOCOL.md:439-448` — a fleet file outside `--root`, absent
under `git archive`; the "before" run (`claims:89`) can't run P2c unless the seed is
frozen into `plans/fixtures/r25/`. SHONEN commit pointers (`SHONEN.md:10`) likewise fail
under an archive unless resolution degrades to "text present" — the presence-check again.

## Axis verdict
Re-running authored assertions is operability-grade until it fires on an *undeclared*
defect (AXES.md:15). F2 proves it can fire; F1 floods it with disclosed ones and F3 lets
the builder choose what counts — round-24 C2's bookkeeping verdict (`kengaku-review.md
:52,149`) in mechanical dress. The plan's "score held" (`claims:92-93`) is correctly
conservative — keep it.

## Smallest safe correction
Rescope P2d to `## Province map` `### Core`+`### Historical` (Core resolves; Historical
fails-and-carries-ABSENT); freeze the P2a/P2b token grammar; freeze the SHONEN seed into
`plans/fixtures/r25/`; add `unasserted=<n>` to `--summary`. Spec tightenings only.

## Falsifiable condition
C2 counts as calibration iff `state_check.py` at base `6180e4f` reports ≥1 mismatch not
already disclosed by `PROVINCE.md:97-100`/§Historical/errata (F2 predicts exactly one).
Zero undisclosed mismatches → bookkeeping closure, `verdict-only` row again.

Installs: none (stdlib + ss + git; registered census run once, exit 0).
VERDICT: C2 is failure-capable but mis-scoped — wrong-table population (F1) + unfrozen
extraction (F3) must be amended before landing, else "0 mismatches on P2" certifies a
stale table while the current one stays unchecked.

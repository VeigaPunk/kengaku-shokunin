# ScribeQuality — round 94, wave 1

Seat ScribeQuality (scribe). Three drafted texts for the L1 to integrate, plus a source-verification
pass over the round's new SOURCES rows and a review of the L1's own uncommitted registry row.
Full report and receipts: `.ufo/waves/round-94/w1/ScribeQuality/`.

Drafts: `.ufo/waves/round-94/w1/ScribeQuality/quality-criterion.md` (new QUALITY criterion Q75),
`.ufo/waves/round-94/w1/ScribeQuality/lesson-gate.md` (round-94 lesson `## Gate` for S297–S302),
`.ufo/waves/round-94/w1/ScribeQuality/skill-registry-row.md` (SKILL.md gate-registry row for
freeze-integrity v2, v1 named superseded).

Verified: gate v2 at T `90c7677f` → `SELFTEST cases=15 ok=15`, `instruments=11 intact=11
broken=0`, rc 0; the round-94 C2 counter at T → `TARGET legs_passed=5 of 5`, `PREDICATE R94-C2
pass`, rc 0, `W5 null ok fixtures_ok=12 of 12`, `W5 pass mutants=7 killed=7`; all five known
false gates at T → each `PREDICATE R94-C2 fail` rc 1, each RED at its own designated fixture;
all six new SOURCES rows vs the lane capture (sha256, bytes, line, word count, quote substring);
all twelve rc-2 paths of gate v2.

FINDING SQ-1 major S299's `(9 words)` cell is wrong (the quote has 10 whitespace tokens): `plans/anchor_line_check.py --lane .` is red at the tip (`ROW S299 state=live defects=words:1`, `live=1 cells=1`, rc 1) where at BASE it was `live=0` rc 0, and `plans/round91_f1_counter.py` flips `PREDICATE R91-F1 pass` rc 0 → `PREDICATE R91-F1 fail` rc 1; the defect entered with commit `90c7677f` (C). Effect on a verdict: neither R94-C1 nor R94-C2 is flipped (no round-94 counter reads corpus/SOURCES.md, the defect is in no tabled instrument, the fleet census exits 0, both counters re-run green at T) — it is a red standing lane gate at the tip. Repair per CORPUS rule 2 / Q34 is a new superseding row, verified in scratch to give `ROW S299 state=repaired by=S303`, `live=0 cells=0`, rc 0; the L1 decides, this seat does not repair.
FINDING SQ-2 minor sibling overlap: the lane working tree already carries an uncommitted `freeze-integrity` row at SKILL.md:698 and an uncommitted `freeze-integrity gate` SCORECARD row (written 19:04:37, right after the w1 dispatch commit d04e6664) — my third deliverable is a review of that row, not a competing draft; measured differences: "printed on every run" is not literally true (two rc-2 paths print no SELFTEST line) and the rc-2 cause list omits five causes the code raises. No verdict change; I did not touch SKILL.md or SCORECARD.md.
FINDING SQ-3 minor latent: gate v2 does not refuse a `--work` inside the lane (unlike round38-c1 / round42-c1, whose registry rows say "refused inside the lane") — `--work ./inlane` runs green and leaves an empty directory behind; `git status` stays clean, so no tracked byte changes.
FINDING SQ-4 info: `corpus/lessons/round-94.md` does not exist at the tip; the lesson `## Gate` draft has no home until the L1 creates it.

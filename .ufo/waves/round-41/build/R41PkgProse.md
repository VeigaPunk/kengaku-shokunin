# R41PkgProse — C2 prose drafts (kengaku round 41, wave 1)

Seat: scribe. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (tip `fc79f2a`).
Scratch: `/fast/scratch/hyaku/kengaku-r41/R41PkgProse` (created empty, removed at exit — no
fixture, no clone, no counter run was needed for this seat).
Drafts: `.ufo/waves/round-41/build/R41PkgProse/`.

## Behaviour

Four prose blocks drafted, no lane file edited. Block (a) is two rows in `corpus/README.md`
(the knowledge index row and one coverage-map bullet), (b) one §Frontier TB2 sub-bullet narrowed
to "7 of 89 read", (c) one `PROVINCE.md` round-41 paragraph with its surface and routing clause,
(d) one `SKILL.md` decision-table section "Scheduling-constraint TB2 grader — round 41". Every
number in every block is the receipt's; every case cite is `receipt:<line>` of
`corpus/evidence/round41/constraints-probe.txt`; every code quote is `<file>:<line>`.

Not started, not needed: `plans/battery41` (C1), the entry itself, the C1/C2 counters, the probe,
the gate, the spec, the dry table, the captures. Nothing frozen was read in a way that could
change it, and nothing outside `.ufo/waves/round-41/build/` was written.

## Gates (what the L1 must satisfy when applying)

| block | gate |
|---|---|
| (a1) index row | one physical line; mirrors the round-40 row's three-cell shape; entry path + what-grader-is + what-passes + summary numbers + sources cell |
| (a2) coverage bullet | one line; mirrors rounds 35-40: bold class label with ordinal, "covered at … depth and executed offline (round 41, 2026-10-26)", entry; sources; probe, receipt; bound; unanswered surfaces; three refusals |
| (b) frontier | appends one sub-bullet inside the existing "Agentic benchmark task-spec audits" bullet; changes no previous round's count text; says "7 of 89 read" |
| (c) PROVINCE | new `##` section + adjacency/routing paragraph after the round-40 pair; narrows only the previous rounds' "remaining TB2 tasks" clause; names the surface; states the routing clause |
| (d) SKILL | new `##` section with `### Decision table — what the grader reads, and what passes it`, "what a green means here", the V7-derived requirement labels, limits, closing property line |

Two constraints on the entry author (not mine, but the prose must not contradict them): V7
(`plans/round41_c2_verify.py:232-272`, `MAP_ROW` at `:85`) requires exactly one `|
\`instruction.md:<L>\` | \`<tag>\` | <label> | <cases> |` row per frozen tag with the derived
label and ≥1 backticked violating case id; V4 (`:179-221`) fails unless both `match=NO` ids
(`later-valid-wed-1105`, `seconds-30`) appear in the entry in backticks. Both are recorded in
`d-skill-scheduling-section.md` §"Open item for L1".

## Touched surfaces

- Written: `.ufo/waves/round-41/build/R41PkgProse/{a,b,c,d}-*.md`, `paste-blocks.md`, and this
  report — all inside the wave build dir.
- Read only: `plans/round-41-claims.md`; `corpus/evidence/round41/constraints-probe.txt`;
  `corpus/evidence/round41/constraints-dry-cases-freeze.txt`; the ten captures under
  `corpus/evidence/round41/tb2-constraints-scheduling/`; `plans/constraints_probe.py`;
  `plans/round41_c2_verify.py`; `plans/pkg-spec-r41.json`; `corpus/README.md`, `PROVINCE.md`,
  `SKILL.md`, `corpus/SOURCES.md`; two sibling PROVINCE files (routing check).
- No tool installed or upgraded (nothing needed). No pacman, no `uv`, no network fetch.

Lane tree untouched:
```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain
?? .ufo/waves/round-41/build.ready
?? .ufo/waves/round-41/build.ready.dispatched
?? .ufo/waves/round-41/build/
?? .ufo/waves/round-41/integrate/
```
No modification under `corpus/`, `plans/`, or any tracked file. HEAD `fc79f2a`.

## Numbers, each with the command that produced it

1. Five target files measured before drafting:
   `wc -l plans/round-41-claims.md corpus/evidence/round41/constraints-probe.txt corpus/README.md PROVINCE.md SKILL.md`
   → `129`, `33`, `499`, `468`, `1030`. Insert anchors used: README 73/267/340, PROVINCE 468,
   SKILL 1030.
2. Receipt facts: `cat -n corpus/evidence/round41/constraints-probe.txt` →
   `:32 regrade cases=25 differ=0`, `:33 cases=25 observed_pass=6 observed_fail=19 mismatches=2`;
   CASE lines are `:7`-`:31`, so all `receipt:<n>` cites in the drafts index that file directly.
3. Requirement labels (the SKILL paragraph), derived from the receipt by the V7 rule:
   script printed at 15:41:45 in `d-skill-scheduling-section.md` §"Derivation", output:
   `window instruction.md:1 enforced 1 0` / `output-file :10 enforced 1 0` / `meeting-title :10
   enforced 1 0` / `attendees :10 enforced 1 0` / `one-hour :10 enforced 1 0` /
   `hard-constraints :12 partly 5 1` / `no-conflict :12 enforced 5 0` / `inputs-readonly :15
   partly 3 1` / `version-prodid :23 enforced 1 0` / `utc-format :25 enforced 1 0` /
   `earliest :27 partly 10 1`. Of the 11 tags: 7 are `enforced` on a single witness, 1 is
   `enforced` on five (`no-conflict`), 3 are `partly` (5, 3 and 10 witnesses) — see finding F4.
4. Capture sizes: `wc -l` on the captures → `test_outputs.py` 209, `README.md` 40,
   `instruction.md` 30, `alice_calendar.ics` 79, `bob_calendar.ics` 61, `carol_calendar.ics` 61.
   All ten files listed in `SHA256SUMS` with the digests the receipt header repeats (`:2-6`).
5. Routing check for block (c), 2026-10-26 15:41:
   `grep -rln "RFC 5545\|iCalendar\|calendar scheduling\|ICS file" --include=PROVINCE.md
   --include=SKILL.md --include=*.md /home/vgpnk/Projects/shokunin` → no lane but this one;
   `grep -rln "cron\|scheduling\|calendar" --include=PROVINCE.md .` → only
   `kaidoku-shokunin/PROVINCE.md:259` ("shared calendar date", supersession dating) and
   `lore-shokunin/PROVINCE.md:28` (routes invented calendar/era design to kotodama, recorded dates
   to lore). Hence "unowned" for meeting scheduling and RFC 5545 conformance, with kotodama's
   fictional-calendar ownership named so the claim is not overbroad.
6. Registry state: `grep -n "S122\|S123\|S124" corpus/SOURCES.md` → no match, exit 1 (the last
   row is `S121`, `corpus/SOURCES.md:136`). See finding F1.

## Findings

**F1 — the source rows the drafts cite do not exist yet.** `corpus/SOURCES.md` ends at S121
(`:136`); S122/S123 (the two captures) and S124 (TB2.1 PR #245) are assigned to wave 1 by
`plans/round-41-claims.md` §C2 but are not committed. The index row and coverage bullet cite
`S122, S123`, and every prior round's rows do the same, so the wording is right; the rows must
land or the citations dangle. For S124 the drafts deliberately do **not** cite the id:
"(prior art, to open as S124)" in (a1) and "published: TB2.1 PR #245" in (a1)/(b)/(d). Replace
that parenthetical once the row exists.

**F2 — "second run byte-equal" has no committed artifact for round 41.** The assignment describes
the receipt as including a byte-equal second run; the committed receipt has no such line and the
only second-reading evidence is `regrade cases=25 differ=0` (`:32`), a same-process regrading of
each un-rebuilt end state (`plans/constraints_probe.py:23-25`). Command:
`grep -rn "byte-equal\|byte_equal\|rerun\|second run" plans/round41_c2_verify.py
plans/constraints_probe.py plans/round-41-claims.md` → only V5's `--dry` byte-equality with the
dry table (`:29`, `:215`), the gate's `--rerun` (`:141`), and the claims' description of it. So
the drafts say "a same-process second grading … not a second run" (PROVINCE) and "a determinism
read of the probe, not re-run stability" (SKILL) — matching the round-40 wording precedent. If a
second full run exists on the host, it is not in `corpus/evidence/round41/`; the L1 should either
commit it or keep the narrower sentence.

**F3 — the sharpest unpriced surface is the input-integrity hole.** `input-crlf-rewrite` passes
3/3 (`receipt:31`) although `instruction.md:17-18` says "Any modification will cause the tests to
fail", because the check compares decoded text and hashes that text
(`test_outputs.py:88-96`). The decoy surface (tests 2-3 read the file's first `DTSTART`) is
published as TB2.1 PR #245, so the round claims no novelty; the CRLF/integrity surface has **no
prior-art check in this wave's artifacts** and the drafts therefore present it as an observation
of the probe, never as a discovery. If wave 2 wants to price it, it needs its own fetch.

**F4 — seven of the eleven requirement tags rest on a single witness.** Derived list above:
`output-file`, `meeting-title`, `attendees`, `one-hour`, `version-prodid`, `utc-format`, `window`
each have exactly one violating case. Recorded in the SKILL section so `enforced` cannot be read
as a general guarantee, and consistent with the round-40 precedent that said the same about
`sorted-by-id`.

**F5 — no registry row for the probe.** `SKILL.md`'s tool-registry table has rows for
`git-leak-probe` (`:587`), `order-check` (`:590`) and `db-wal-probe` (`:594`) but nothing for
`plans/constraints_probe.py`, so the section's first instruction ("run
`python3 plans/constraints_probe.py --lane .`") points at a tool the registry does not list.
Left undrafted because the assignment names four blocks; the exact row shape is written out in
`d-skill-scheduling-section.md` so it can be routed or added by the L1.

**F6 — two labels are `partly` for reasons worth stating in the entry.** `hard-constraints` and
`earliest` are both `partly` on the same case (`decoy-first-vevent`, `receipt:14`):
its Friday 15:00 meeting is outside Alice's 14:00 limit and later than both valid slots, yet the
file passes 3/3 because tests 2-3 read the decoy's `DTSTART`. `inputs-readonly` is `partly` on
`input-crlf-rewrite` (`receipt:31`). The SKILL paragraph names each pass by id so the label cannot
be read as "enforced with an exception".

**F7 — the `earliest` test's shape is not "validity", and two cases prove it.** `PFP` on
`bob-start-0900-wed` (`receipt:13`) and `wed-1059-overlaps-alice` (`receipt:23`): the scan asserts
the absence of a valid *earlier* slot, so an invalid chosen slot is passed by test 3 whenever the
first valid slot is later. Recorded as the `earliest` table row with the "compare equality
instead" reviewer check.

**F8 — dead-code branch found while reading the model (no case covers it).** `_hard_ok`'s Bob
Tue/Thu 4:30 clause (`test_outputs.py:65-68`) cannot fire once the Alice-end check (`:61`) has
passed, because every surviving start ends ≤14:00. Commented in the table's reviewer column; no
frozen case exercises it, so it is a reading of the capture, not a probe result.

## Out-of-scope items (named, not done)

- The entry `corpus/knowledge/tb2-constraints-scheduling-grader.md` (absent at draft time:
  `ls corpus/knowledge/tb2-constraints-scheduling-grader.md` → `No such file or directory`), its
  `## Requirement map`, and its Findings/Regrade sections.
- `corpus/SOURCES.md` rows S122, S123, S124 (F1).
- The round-41 `### Round-41 evidence` subsection in `corpus/README.md` — every prior round has
  one, but the assignment's block (a) names only the index row and the coverage bullet; the
  content is ready (three bullets: captures, receipt+dry table, and — if it lands — the C1
  `battery41` line).
- The `constraints-probe` registry row (F5).
- `plans/battery41/*` and anything the C1 counter reads.
- `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `corpus/lessons/round-41.md` — L1-owned.

## Artifact paths

- `.ufo/waves/round-41/build/R41PkgProse.md` — this report.
- `.ufo/waves/round-41/build/R41PkgProse/a-readme-index-and-coverage.md` — block (a), two fences
  with anchors.
- `.ufo/waves/round-41/build/R41PkgProse/b-frontier-tb2-subbullet.md` — block (b).
- `.ufo/waves/round-41/build/R41PkgProse/c-province-round41.md` — block (c) + routing clause.
- `.ufo/waves/round-41/build/R41PkgProse/d-skill-scheduling-section.md` — block (d) +
  derivation script/output + V7/V4 handoff notes.
- `.ufo/waves/round-41/build/R41PkgProse/paste-blocks.md` — application order and anchors.

No file was written outside `.ufo/waves/round-41/build/` and the scratch dir; timestamps of the
writes are the mtimes in that directory (15:40-15:43), and no other path needed a timestamp.

VERDICT: prose-drafted-4-blocks

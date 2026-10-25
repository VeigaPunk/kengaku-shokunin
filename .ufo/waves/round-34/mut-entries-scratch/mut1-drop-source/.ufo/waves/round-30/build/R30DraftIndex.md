author: L1Kengaku30.R30DraftIndex (leaf scribe seat, round 30 wave 1)
round: kengaku 30 (hyaku run 6), 2026-10-25
scope: read-only drafting of `corpus/README.md` rows for the C1 admission; no production byte created,
edited or deleted. Scratch is `/tmp/r30-R30DraftIndex/`.

# R30 — README rows the contamination-transparency amendment needs

Inputs read (all read-only): `plans/round-30-claims.md` (frozen C1–C3);
`corpus/README.md` (whole file, index table / coverage map / `## Frontier`);
`corpus/SOURCES.md` (whole registry); `corpus/QUALITY.md` Q4–Q8 skim;
`corpus/lessons/round-29.md` §Rejected candidates (the flip condition's own words);
`corpus/lessons/round-29-verifier-spotcheck.md` §5 (D1–D5);
`plans/adoption_check.py`; staged package
`/home/vgpnk/Projects/shokuknow/merge/kengaku/{SOURCES.append.md,knowledge/corpus/knowledge/contamination-transparency-card.md}`.

One command was run for evidence, on synthetic bytes only: `plans/adoption_check.py` against a
`/tmp` copy of the two corpus files plus the staged card and the six staged rows (§Verification).

## Block (a) — index table row

Anchor: **`corpus/README.md:64`** — the row ``| `knowledge/benchmark-task-validity-checklist.md` | Ten-axis…``.
Insert as a new line immediately after it, i.e. as new line 65, directly before
`corpus/README.md:65` — the row ``| `lessons/round-1.md` | Path-correction…``. This is the last `knowledge/`
row of the top `## What's here` table, so the new row stays inside the knowledge block.

```
| `knowledge/contamination-transparency-card.md` | Amendment to the round-24 contamination entry (knowledge/contamination-detection-and-transparency.md), not a fourth rival card design: release-side fields R1-R5 (strata, elicitation budget, contamination type tested, regeneration status, instrument currency) and score-side fields S1-S2 (acquired contamination, card integrity) answering a Q1-Q8 gate; each detector's blind spot is stated beside its result | S081–S086 (`corpus/SOURCES.md` rows, opened 2026-10-25); `plans/round-30-claims.md` §C1; round-30 Gate |
```

Shape check (measured): 4 `|` separators → 3 cells, matching `| Entry | Covers | Primary source |`
(`corpus/README.md:26-27`); row begins at column 0 with `` | `knowledge/ `` so the counter's
``^\| `knowledge/<name>` \|`` regex (`plans/adoption_check.py:85`) anchors on it; 61 words, 564 bytes,
no tab; the Covers cell names the entry it extends (QUALITY Q6) and states the negative space
(QUALITY Q4).

## Block (b) — coverage-map amendment line

Anchor: **`corpus/README.md:240`** (`- **Contamination detection and transparency**: covered at
source-digest depth (round 24) …`). Insert immediately after it, before
`corpus/README.md:241` (`- **Judge calibration**: covered at source-digest depth (round 24) …`), so the
amendment sits beside the row it amends. This row is not optional prose: QUALITY Q7 makes the
entry file, its index row and its coverage-map row a same-commit landing condition.

```
- **Contamination transparency card format**: covered at source-digest depth (round 30, 2026-10-25) — knowledge/contamination-transparency-card.md; S081–S086. Lands as an amendment to the round-24 *Contamination detection and transparency* row, not a fourth rival card design: it adds the release-side R1-R5 and score-side S1-S2 fields and the Q1-Q8 gate on top of that entry's tier/access vocabulary. Not a contamination measurement of any benchmark, not a runtime judge, not a card any benchmark has adopted.
```

Shape check (measured): 71 words, 510 bytes, plain `- ` bullet in the top-level coverage-map list,
same `**Bold ground**: covered at … depth (round N, date) — knowledge/…; S…` voice as
`corpus/README.md:242-244`, and ends on explicit negative space like `:249`.

Alternative placement, if the admission seat prefers the round-section pattern
(`corpus/README.md:343-373`, "Coverage-map ground" tables): a second row there would still satisfy
the counter (its `re.search` is boolean) but it cannot substitute for this bullet, because the
`## Coverage map` list is what `corpus/README.md:249` treats as the canonical coverage statement.
Recommendation: land this bullet only, once.

## Block (c) — frontier discharge line

Anchor: **`corpus/README.md:272`** — the bullet ``- **Contamination transparency cards**: why — `knowledge/
contamination-detection-and-transparency.md` establishes the tier/access vocabulary …``. Insert as a
nested sub-bullet immediately after it, before `corpus/README.md:273`
(`- **Judge calibration applied inward**: why — …`). The sub-bullet is 2-space indented like
`corpus/README.md:271,274-277`.

```
  - *Partly discharged round 30 (2026-10-25):* `knowledge/contamination-transparency-card.md` supplies the card format and the Q1–Q8 gate as an amendment to `knowledge/contamination-detection-and-transparency.md`, re-grounded on S081–S086 opened this round — the tabulated card designs now carry a record of detector access, tier tested and what a negative cannot rule out. This supersedes the `draft a card template and gate a knowledge entry on Q1–Q8` instruction and, for the card format only, the `unopened lead` phrase. Still frontier: benchmark-maintainer releases on hidden-test governance (no private-split or hidden-test-governance release was opened this round), a runtime judge as the scoring artefact, and adoption of the card by any benchmark.
```

Shape check (measured): 103 words, 756 bytes, `  - *Partly discharged round N (date):*` marker with
the three-part shape every existing discharge line uses (what landed → which clause it supersedes →
what remains): `corpus/README.md:271` (round 29 attempt 2), `:274-277` (rounds 25/26/27).

## What stays frontier — one line

Hidden-test governance releases (no private-split or hidden-test-governance release opened this
round), a runtime judge as the scoring artefact, and adoption of the card by any benchmark.

## Verification actually performed

1. Anchor bytes: `sed -n '64p;65p;240p;241p;272p;273p' corpus/README.md` — quoted in each anchor above.
2. Counter dry run, **on a `/tmp` synthetic tree, not the lane**: `/tmp/r30-R30DraftIndex/lane/corpus/`
   = verbatim copies of `corpus/{SOURCES.md,README.md}` + the six staged `S081`–`S086` rows appended
   verbatim + the staged card with only `verified-at:` patched to `2026-10-25`; block (a) inserted
   verbatim after the `benchmark-task-validity-checklist` row:
   `python3 plans/adoption_check.py --lane /tmp/r30-R30DraftIndex/lane --expect /tmp/r30-R30DraftIndex/adoption-expect.json`
   → `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=skipped`, exit 1.
   Exit 1 is the census clause alone: `ok` requires `args.census and census_code == 0`
   (`plans/adoption_check.py:129-133`), and no `--census` was passed in a tree that is not a lane repo.
   Every printed counter that a README row can move hit the frozen C1 values.
3. Cell/word/byte counts of all three blocks, measured in the same kernel
   (`row` 4 pipes/3 cells; no tabs; no trailing whitespace).
4. `verified-at` gating is real but unprinted (`plans/adoption_check.py:87,130`), so the staged
   `2026-10-23` value is a hard blocker for C1 even though the printed line never shows it (finding F1).

Not run, therefore not passed: no gate, selftest, census or validator was executed on the lane tree;
no `python3 plans/sources_adopt.py` run; `README.md` was not modified anywhere but `/tmp`.

## Findings handed to the admission seat (in order of how they can void C1)

- **F1 — the staged card is not re-grounded yet.** Its frontmatter reads `verified-at: 2026-10-23` and
  `recheck: 180d — re-run the Gate commands for S081–S086 (ran 2026-10-23)`. The frozen C1 predicate
  requires `verified-at: 2026-10-25`; `adoption_check.py:87` gates on it silently. Both fields must be
  rewritten by the seat that re-opens the sources, not left to the index edit.
- **F2 — the staged card still argues against its own admission.** Its closing `ground:` paragraph
  says "the *admission* of the card against the lane's existing
  `knowledge/contamination-detection-and-transparency.md` vocabulary is the lane's call, not this
  entry's". Under an admitted amendment that sentence is false of the landed bytes; it must be
  replaced by the amendment relation (which is what block (a) and block (b) assert).
- **F3 — registry rows must carry `opened=2026-10-25`.** Every staged `S081`–`S086` row has
  `opened = 2026-10-23` and a prose `recheck` cell (`2026-10-23 — re-verify at the next upstream
  release (Gate S081)`). Block (a) states "opened 2026-10-25", so an append that keeps the staged
  dates makes the index row overclaim. Round 29's normalizer precedent projects a prose `recheck` to
  `180d` with `opened` set to the round's access date.
- **F4 — dangling `used-by` pointers on the staged rows.** `S081` also names
  `corpus/knowledge/judge-calibration-thresholds.md`, and `S084`/`S085`/`S086` also name
  `corpus/knowledge/cjk-eval-venue-access.md`. Neither file exists in this lane, and the first was a
  round-29 *rejected* candidate. `usedby_ok` still passes (`all(...)` over the cited ids,
  `adoption_check.py:107-115`), so the counter will not catch this; the append should drop those
  paths. This is D5's shape in the opposite direction.
- **F5 — do not add `S077` as a `source:` line.** The card's Q2 row cites S077's canary in prose. The
  frozen C1 line is `cited_rows=6`; `SOURCE_LINE_RE` counts every `source: S###` line
  (`adoption_check.py:29,88-89`), so a seventh line prints `cited_rows=7` and fails the claim while
  the entry would be *more* honest. Keep S077 prose-only.
- **F6 — the counter cannot see a duplicate index row.** `indexed` is a boolean `re.search`
  (`adoption_check.py:85-86`), so two rows for one entry still print `indexed=1`; and
  `plans/sources_adopt.py` never reads `README.md`. Landing block (a) exactly once, in the top table,
  is therefore an unguarded manual condition — worth a line in the Gate.
- **F7 — pre-existing malformation at the insertion boundary.** `corpus/README.md:249` (the round-29
  coverage bullet) is followed by `## Open gaps` at `:250` with no blank line. Anchors (b) and (c) are
  chosen away from `:249`/`:250`; a seat that appends the new coverage bullet at the end of the list
  instead will edit that boundary and should not also "fix" it silently in an admission commit.

## Out of scope, untouched

`corpus/README.md` itself; `corpus/SOURCES.md` (the six-row append and its date/`used-by` projection);
`corpus/knowledge/contamination-transparency-card.md` (entry body, frontmatter, `ground:` rewrite);
`plans/sources_adopt.py` and its selftest (C3); `plans/round30_defects.py` and D1–D5 (C2); the
`## Round-30 supporting artifacts` section such a round would add (not asked for by this seat, and the
frozen C1 predicate asks only for one index row); `SCORECARD.md`, `LOG.md`, `.ufo/state`,
`MANIFEST.json`, `watchdog.log`; `/home/vgpnk/Projects/shokuknow` (read-only, no campaign tool run);
sibling lane repos.

## Tooling

Nothing installed or upgraded. Pacman transactions stay paused host-wide; no `uv`/`npx`/binary
channel was needed — the only execution was the lane's own stdlib `plans/adoption_check.py` under
`python3` on `/tmp` bytes.

## Handoff

The three blocks are copy-ready but not landed by design. The seat that lands C1 should run, on the
lane tree after its own append and entry edits:
`python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census`
and require the exact frozen line with `census=ok` and exit 0; if `indexed` is the only counter
short, block (a)'s anchor is the cause; if it is still 1 after a second row, see F6.

# R30DraftScore — SCORECARD/LOG round-30 draft (scribe seat)

Draft artifact: `/tmp/r30-DraftScore/score.md` (scratch, per round-30 leaf bounds; copy it before /tmp
is cleared). This report is the only lane file this seat wrote.

## Behavior

Read: `plans/round-30-claims.md` (all three frozen predicates, controls, kill rules),
`SCORECARD.md:986-1010` (round-29 attempt-2 section, its capability table and its axis-hold paragraph),
`LOG.md:631-778` (round-29 attempt-2 entry, correction batches 1–5),
`corpus/QUALITY.md:157-194` (R1–R15, Q18, Q19), `corpus/lessons/round-29-verifier-spotcheck.md:93-160`
(§5 D1–D5 verbatim), the three committed controls in `.ufo/waves/round-30/claims/`,
`.ufo/waves/round-30/{build-dispatch.json,adoption-expect.json,assimilation/*}`,
`.ufo/waves/yield.tsv` (41 lines), `plans/round30_defects.py --help`, `plans/sources_adopt.py --help`,
and `corpus/evidence/round29-attempt2/control-nothing.txt`.

Produced, in the target files' own formats:

- **(a) SCORECARD section** headed `## Round 30 — assimilation round 2, routed-defect closure, quote
  validation (hyaku run 6, 2026-10-25)`: baseline, the lowest-axis + tie-break sentence R8 greps for,
  a three-row claim table (C1 **coverage**, C2 **calibration**, C3 **operability**) with
  before → after cells and score/verdict cells, the other-axes-held paragraph, and one capabilities-table
  row (`quote-validating adoption gate`, first working round 30).
- **(b) LOG entry** with numbered correction items 1–5 mapped to D1–D5, a measured paragraph, a
  re-verification (freshness) paragraph naming what this round re-ran, waves, L0, safety, and the Q19
  seat-yield paragraph.
- **(c) `yield.tsv` row shape**: header byte-exact, the six columns with their value domains taken from
  the 40 landed round-29 rows, and a worked row for this seat.

Cell provenance is tagged inline: **(M)** measured by me with the command printed, **(C)** committed
freeze control, **(T)** frozen predicate text NOT observed, **(D)** labelled arithmetic. No score is
raised anywhere: C1 7→7 held (round-25 L0 cap open), C2 8→8 held, C3 8→8 held with a capability row.

## Gates (measured this seat, read-only, no production writes)

| command | bytes | exit |
|---|---|---|
| `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census` | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` | 1 |
| `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | `82` | 0 |
| `ls corpus/knowledge/*.md \| wc -l` | `38` | 0 |
| `grep -cE '^\| \`knowledge/' corpus/README.md` | `38` | 0 |
| `grep -nE '^\s*\|\s*S08[1-6]' corpus/SOURCES.md` | no output — the six cited ids are absent | 1 |
| `python3 plans/round30_defects.py --lane .` | D1/D2/D3/D5 `repaired`, D4 `DEFECT … uncommitted: M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md`, `defects=1` | 1 |
| `python3 plans/sources_adopt.py --selftest` | `SELFTEST cases=10 failed=0` | 0 |
| `python3 plans/sources_adopt.py --quote-file /tmp/x --artifact /tmp/y` | `error: unrecognized arguments: --quote-file /tmp/x --artifact /tmp/y` | 2 |
| `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census` | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok` | 0 |
| `awk -F'\t' '{print NF}' .ufo/waves/yield.tsv \| sort -u` | `6` (41 lines = header + 40 rows; 27 `yes` / 13 `no`; 0 round-30 rows) | 0 |

State at draft: **C1 not landed** (no card, registry 82 / knowledge 38 / index 38), **C2 at 1 open
defect** (D4, a commit item), **C3 not landed** (10 selftest cases, no quote mode). The draft therefore
keeps `(T)` tags on the three after-cells rather than copying the predicate's target lines as measured.

## Touched surfaces

- Written: `.ufo/waves/round-30/build/R30DraftScore.md` (this report); `/tmp/r30-DraftScore/score.md`.
- Not written: `SCORECARD.md`, `LOG.md`, `.ufo/waves/yield.tsv`, `corpus/**`, `plans/**`,
  `/home/vgpnk/Projects/shokuknow/**`, fleet root, sibling lanes, `.ufo/state`, `watchdog.log`,
  `MANIFEST.json`. `git status --porcelain` was read, never modified. No pacman transaction (host
  paused), no tool install, no subagent, no `agent://all`.

## Findings

1. **C2 is one commit from its target, and that commit is not mine to make.** `defects=1` with D4 as the
   sole item; the check reads git state, so `defects=0` follows the wave-evidence commit, not an edit.
   C2's row must not be scored met on a re-run that still prints `defects=1`.
2. **The two C1 control receipts are different invocations and the row must quote one of them.** The
   freeze control `.ufo/waves/round-30/claims/control-nothing.txt` prints `… usedby_ok=0 census=ok` /
   `exit=1`; the D1 receipt now committed at `corpus/evidence/round29-attempt2/control-nothing.txt`
   prints `… usedby_ok=0 verified_at=0 census=skipped` / `exit=1`, because the no-`--census` invocation
   cannot print `census=ok` (round-29 correction item 8). Both are honest; quoting a mixture is not.
   The SCORECARD draft uses the freeze control and says so.
3. **R13 exposure in C3.** If either new quote selftest case reads C1's card, reverting C1 moves C3's
   `--selftest` case count and the round fails one-artifact-one-claim. The two new cases need inline
   synthetic fixtures, which is also the only way they can fail on the unmodified validator body — the
   frozen kill rule.
4. **The staged card is not re-grounded bytes.** Its frontmatter reads `verified-at: 2026-10-23` with
   locators instead of quotes; C1's predicate requires `verified-at: 2026-10-25` and six rows opened
   today. Its body does use all six ids (S085 at line 81, CAICT 2024), so no `source:` line can be
   pruned for tidiness.
5. **R8 compliance is in the body, not the heading.** The prescribed heading carries no axis word, so
   the lowest-axis/tie-break/waiver sentence is the first paragraph of the draft section — that is what
   `grep -nE 'lowest axis|tie-break|waiver'` hits inside `## Round 30`.
6. **Q19 row shape is fixed by 40 landed rows**: `round\tseat\trole_family\treport\tcaused_change\tcommit`,
   six columns, `caused_change` ∈ {yes,no}, non-empty commit in every row (a `no` seat names the round's
   landing commit). Round 30 owes 36 build rows plus wave-2 falsify rows; the file currently has zero
   round-30 rows.

## Out of scope (not done, by bound)

No production edit (SCORECARD/LOG/yield.tsv/corpus/plans), no commit, no push. I did not run the
freshness suite — `grader.py` (16 `open(…, "w")` sites by `grep -c 'open(.*"w"' grader.py`, so a run
writes), plus `plans/round28_census.py`, `plans/config_projection.py` (0 writer sites) and the fleet
`scripts/sources-census.sh` — they are named in the LOG draft as close-time re-verification commands
with their values left to the census seat, whose assignment they are. No model routing, no subagent
dispatch.

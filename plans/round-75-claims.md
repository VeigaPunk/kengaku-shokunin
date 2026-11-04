# Round 75 — kengaku — frozen claims (R75-C1, R75-C2)

Frozen before data: `2026-11-04T04:20:00Z` (L1 `KengakuR75`), base tip
`4c4249a26a01aeb081915755076f74a7d6c88923` (round-74 verifier spot-check). This file names
each claim's sentence, counting command, target, control and kill rule. Nothing below changes
after a seat scores it.

Round shape: one v1 wave, 13 seats (see `.ufo/waves/round-75/w1-dispatch.json`). The L1 holds
the canonical planner seat; the bounded planning data-walk rides the `scout` item
(`SourcesHostR75`). Axis assignment: R75-C1 works **coverage** (the lane's lowest non-retired
axis, held at its L0 cap of 7); R75-C2 works **calibration** (held at ceiling 10, exercised).

Both claims discharge routed defects of the round-74 outside closure: R75-C1 prices
`AXES.md`'s coverage sentence (which no instrument priced, and which had drifted to 58
unindexed surfaces); R75-C2 prices R74-D4 (any-defect mutant counting, literal tallies, no
null arm), R74-D1 (receipts with no measured revision), and R74-D5 (no claim evidence cites a
`S###` row) by resting its flag leg on S251's `git rev-parse --verify` semantics and S250's
reject-flip.

## R75-C1 — coverage (lowest non-retired axis, L0-capped at 7)

**Claim.** The lane gains a corpus index-parity gate that enumerates three universes from disk —
`corpus/knowledge/*.md`, `corpus/lessons/*.md`, `corpus/evidence/*/` — and prices both directions
of `AXES.md`'s coverage sentence (every described surface indexed; every index row on disk), then
the drifted index is repaired so the gate passes on the landing tree: 3 unindexed knowledge
entries, 35 unindexed lesson files and 20 unindexed evidence directories become 0.

**Frozen sentence (the predicate, in one sentence).**

    python3 plans/round75_c1_index_parity.py --lane .

prints

    UNIVERSE knowledge files=74 indexed=74 missing=0 orphan=0
    UNIVERSE lessons files=123 indexed=123 missing=0 orphan=0
    UNIVERSE evidence dirs=66 indexed=66 missing=0 orphan=0
    PREDICATE R75-C1 pass

and exits 0, with `LANE_TIP <40-hex>` naming the measured revision and `WORKTREE clean` on its
first two lines; `--selftest --work DIR` prints `SELFTEST cases=8 red=7 failures=0 ok=True`
(amended by A4 and A5: five arms at freeze, seven after the two seat counterexamples, eight after
the mutation-tester's printed-verdict survivor — a battery that grew, never a target that narrowed).

**Counting command (both states).**

    python3 plans/round75_c1_index_parity.py --lane . ; echo "rc=$?"

**Before** (measured at the freeze revision by `corpus/evidence/round75/c1-before.txt`):
`UNIVERSE knowledge files=74 indexed=71 missing=3 orphan=0`, `UNIVERSE lessons files=123
indexed=87 missing=36 orphan=0`, `UNIVERSE evidence dirs=66 indexed=46 missing=20 orphan=0`,
`PREDICATE R75-C1 fail`, rc 1 — 59 unindexed surfaces, each printed by name. (The lesson file
added in the freeze commit is itself one of the 36; the repair indexes it too.)

**After (target).** The four lines above, rc 0.

**Control (cheapest skip; committed at freeze).** `--control-rowshuffle --work DIR` builds a
README whose index-row *count* equals the surface count (6 = 6) while every row names one file:
a counter that counts rows scores it complete, the frozen gate still prints four `MISSING*`
defects and `PREDICATE R75-C1-control pass` (rc 0) — receipt
`corpus/evidence/round75/c1-control-rowshuffle.txt`.

**Kill rule.** The claim fails if any `MISSING`/`ORPHAN`/`MISSING-EVIDENCE`/`ORPHAN-EVIDENCE`
line is printed at the landing tip, if the printed universe counts differ from the target lines,
or if the selftest regresses below `cases=5 red=4 failures=0`.

## R75-C2 — calibration (held at ceiling 10, exercised)

**Claim.** The registry audit's self-evidence becomes derived and attributed: every mutant kill is
priced against its declared expected finding id (a kill by a different defect is a `wrong_id`
kill, and an off-target fixture therefore fails), a measured null arm must survive, every tally is
computed, each receipt carries a `LANE_TIP` that `--check-stamps` resolves and proves an ancestor
of the measured branch tip, and the entry-flag leg follows S250's reject-flip — when a script
declares its CLI through `add_argument`, a flag counts only if `add_argument` declares it.

**Frozen sentence (the predicate, in one sentence).**

    python3 plans/round75_c2_registry_audit.py --lane . --mutants --check-stamps corpus/evidence/round75

prints `MISMATCH 0`, `DEFECTS n=0`, `FLAGS ok n=0`,
`MUTANTS real=10 expected_matched=10 wrong_id=0 survived=0 null_arms=1 null_survived=1 total=11`
(amended by A4: nine mutants at freeze, ten after the seat's help-text counterexample),
`STAMPS files=K stamped=K unstamped=0 unresolved=0 not_ancestor=0` with `K > 0`, and
`PREDICATE R75-C2 pass`; exit 0. `--selftest --work DIR` prints `SELFTEST arms=5 failures=0 ok=True` (amended by A5: a fifth arm
reads the printed tally, after the mutation-tester survived a literal `wrong_id=0`).

**Counting command (both states).**

    python3 plans/round75_c2_registry_audit.py --lane . --mutants --check-stamps corpus/evidence/round75 ; echo "rc=$?"

**Before** (measured at the freeze revision, two receipts):
1. `corpus/evidence/round75/c2-stamp-red-before.txt` — the same stamp leg on
   `corpus/evidence/round74`: `STAMPS files=11 stamped=0 unstamped=11 unresolved=0
   not_ancestor=0` (one `DEFECT UNSTAMPED` line per file), `PREDICATE R75-C2 fail`, rc 1 — the
   R74-D1 class: receipts with no measured revision.
2. `corpus/evidence/round75/c2-control-attribute.txt` — the off-target control:
   `R74-METRIC killed=10/10 (any-defect counting)`, `R75-METRIC expected_matched=9/10
   wrong_id=1`, `OFF-TARGET X-off-target expected=:entry:unbacked-flag: defects=1 matched=False`,
   `NULL-ARM defects=0`, `PREDICATE R75-C2-control pass` (rc 0) — on the *same* fixture bytes
   round 74's metric reports a kill and the attributed metric reports a wrong-id kill.

**After (target).** The frozen sentence above at the landing tip, rc 0.

**Kill rule.** The claim fails if any audit defect is printed, if `expected_matched < real`, if
`wrong_id` or `survived` is nonzero, if the null arm is killed, if any stamp is unstamped,
unresolvable or not an ancestor, or if any selftest arm fails.

## Frontier step (not a claim)

- `corpus/SOURCES.md` gains S251 (Git `git-rev-parse` documentation, tier A) opened this round by
  a live fetch with capture, sha256 and a located ≤25-word quote; it grounds R75-C2's stamp leg
  (`git rev-parse --verify <rev>^{commit}`) and is cited in the claim's evidence.
- `corpus/lessons/round-75.md` carries `## Gate` (≥1 admit and ≥1 reject from the opened set) and
  `## Mistakes`; the mining target is the R74-D1 receipt-provenance miss.
- Census before → after with
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
- Assimilation: none (no staged row admitted this round; open L0 `kengaku | round-54` carried).

## Amendment A1 — every receipt mode stamps; the stamp-count before value (appended 2026-11-04T04:52Z, before any seat returned)

Two corrections landed before any seat scored anything; predicate, target, control and kill rule
are unchanged.

1. **Every receipt mode prints `LANE_TIP`/`WORKTREE`.** The first freeze printed the stamp only on
   the verdict path, so `--selftest` and `--control-*` receipts would have been `UNSTAMPED` by the
   claim's own `--check-stamps` leg. Both instruments now print the pair before dispatch and the
   verdict path writes it into the `--receipt` bytes. All round-75 receipts are regenerated from a
   clean clone at this amendment's revision.
2. **`STAMPS files=` before value corrected 13 → 11** — `corpus/evidence/round74/*.txt` holds 11
   receipts, not 13 (counted: `ls corpus/evidence/round74/*.txt | wc -l` → 11). Same defect class
   as R74-D1: a number asserted rather than counted.
3. **R75-C1 Before lessons count 35 → 36 and total 58 → 59** — the freeze commit adds
   `corpus/lessons/round-75.md`, which is itself unindexed until the repair lands.

## Amendment A2 — the stamp leg enforces its own sentence; the null arm is cosmetic (appended 2026-11-04T05:10Z, after seat `C2MutantReplayR75` scored but before integration)

Seat `C2MutantReplayR75` found that `--check-stamps` printed `PREDICATE R75-C2 pass` with
`LANE_TIP unknown` and `STAMPS files=0` on a clone whose `--rev` did not resolve and whose evidence
dir held no receipts. The frozen sentence already requires `LANE_TIP <40-hex>` and `files=K
stamped=K` with `K > 0`; the counter simply did not enforce its own words. This amendment makes the
counter implement the existing sentence; the sentence, target, controls and kill rules are
unchanged.

1. `check_stamps` emits `DEFECT TIPTAG:unresolved` when `--rev` does not resolve to a commit, and
   `DEFECT STAMPS:empty-dir` when the evidence dir holds no `*.txt`. Red-before:
   `--check-stamps <empty dir>` → `STAMPS files=0 stamped=0 …`, `PREDICATE R75-C2 fail`, rc 1.
2. The null arm is now a whitespace-only delta on the existing `tool-b` row (the first version
   renamed `tool-b`→`tool-n`, which was a substantive edit and therefore not a null arm). The arm's
   purpose — a benign edit must survive — is unchanged; the mutant count is unchanged.

Recorded as M75-9 in `corpus/lessons/round-75.md`.

## Amendment A3 — the counters recognise only rendered index rows and only declared options (appended 2026-11-04T05:35Z, after seats scored, before integration)

Two seat counterexamples showed the counters under-enforcing the frozen sentences. Both fixes make
the counter implement the sentence it already had; predicate, target, controls and kill rules are
unchanged.

1. **R75-C1** (seats `ClaimsCriticR75` and `C1GateAuditR75`): a README whose *only* match was an HTML
   comment listing every filename token satisfied all three universes (rc 0), and a `.md`-named
   directory counted as a knowledge file. `AXES.md`'s sentence is about an index, i.e. rendered rows.
   The counter now strips HTML comments and fenced code blocks before scanning, splits rows on
   unescaped pipes, requires the first cell to be exactly `` `kind/file` `` and every later cell to be
   non-empty, and enumerates regular files only. Rejection proof: the comment-only and fenced-row
   fixtures both print `PREDICATE R75-C1 fail`; the critic's counterexample is now a reject case.
2. **R75-C2** (seat `ClaimsCriticR75`): `add_argument('--lane', help='--strict')` made a *rejected*
   option look declared, because keyword values were collected as declarations. Only positional
   string arguments register an option; `help=`/`metavar=`/`dest=` never do. Rejection proof: that
   fixture now prints `DEFECT tool-doc:entry:flag-not-declared:--strict`, `PREDICATE R75-C2 fail`.
3. **R75-C1 kill-rule omission** (seat `ClaimsCriticR75`): the kill rule's enumeration does not name
   the `WORKTREE clean` line that the frozen sentence requires as one of the first two lines. The
   sentence governs; the omission is recorded as a defect in the round report rather than repaired
   by widening the rule after scoring.

Recorded as M75-10 and M75-11 in `corpus/lessons/round-75.md`.

## Amendment A4 — the batteries absorbed the seat counterexamples (appended 2026-11-04T05:48Z, before integration)

Two seat counterexamples were not only fixed but turned into permanent reject arms, and the
frozen sentences' printed tallies moved with them. Nothing the claim *targets* narrowed: the
battery grew by two C1 arms and one C2 mutant.

- R75-C1 battery: `cases=5 red=4` → `cases=7 red=6`; the added arms are `comment-only` (an HTML
  comment listing every filename must fail) and `fenced-rows` (rows inside a code fence must fail).
- R75-C2 matrix: `real=9 total=10` → `real=10 total=11`; the added mutant is
  `M10-flag-in-help-text` (`add_argument('--lane', help='--strict')` must produce
  `:entry:flag-not-declared:`). The selftest battery is unchanged at 4 arms.
- Disclosed rather than folded away: the round report's "Before → after measurements" names both
  tallies as amended, and the lesson carries the two seats' counterexamples (M75-10, M75-11).

## Amendment A5 — a printed-verdict arm and a printed-tally arm (appended 2026-11-04T06:05Z, after WAVE-DONE, before the report)

Seat `MutantBatteryR75` mutation-tested both instruments: C1 `SURVIVORS n=4` of 9, C2 `SURVIVORS n=8`
of 11, every survivor in the *reporting* surface (a mutant printing `PREDICATE R75-C1 pass` over 59
defects, or `wrong_id=0` as a literal, was not killed because every arm read state, never the printed
verdict). Two arms close the highest-value part of that gap and the sentences' tallies move with
them:

- R75-C1 battery: `cases=7 red=6` → `cases=8 red=7`; the `printed-verdict` arm asserts the printed
  `PREDICATE R75-C1 fail` token on a red fixture (kills the token and exit-code mutants).
- R75-C2 battery: `arms=4` → `arms=5`; the `tally` arm reads the printed
  `expected_matched=/wrong_id=` numbers on the clean matrix (kills the literal-tally mutants).

The remaining survivors are reported, not claimed away: see M75-12 and the round report's wave
findings.

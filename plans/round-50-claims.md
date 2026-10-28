# Round 50 — declared claims (frozen before data)

Lane: `kengaku-shokunin` · round 50 · attempt 1 · hyaku run 11 · L1 `KengakuR50`.
Base lane tip at freeze: `71f5f5f77591d8c3d19297ee9785436da45209e4`.
Instrument digests frozen with this file (stage 1): `plans/round50_c1_verify.py`
`f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76`; `plans/round50_c2_audit.py` (C2 command);
`plans/honest50/population.txt` `b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69` (126 fixtures);
`plans/honest50/build_honest_population.py` `35e3de6059e4676133291c615fdac7b04342e7c43827ec1e70ac09f83267a70b`;
`plans/fixture_fence.py` (the fence under test, still the base fence)
`05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.

Two claims, two distinct axes, causally separable (C1 touches `plans/fixture_fence.py`, `plans/honest50/`,
`plans/mutants50/`, `plans/sealed50/`, `plans/round50_c1_verify.py`; C2 touches `SCORECARD.md` corrections only).
Lowest non-retired axes at round start: coverage 7 (capped by the open L0 `kengaku | round-33` decision) and
novelty 7. C1 works **novelty**. Coverage is not claimed this round (its cap is operator-blocked and the r25
question is unanswered); the round records that in `SCORECARD.md` and harms no axis.

## C1 — novelty (7 → 8): an honest-geometry instrument for the fixture fence, and the fence repaired under it

**What the lane could not observe before.** The standing fence counters (`plans/round45_c1_verify.py`,
`plans/round46_c1_verify.py`) measure a fence's *under*-refusal (does a hostile module get admitted / read
outside `d`?) and only a 104-fixture honest leg drawn from the batteries. Round 48 measured, for the first time,
that the landed fence also *over*-refuses: `HONEST fixtures=120 admitted=112 refused=8`. Round 49 built the
population to 124 and a counter contract but never landed a repair or a scored run (honest stop, no counter at
landing — `SCORECARD.md` r49 row). The lane had no committed tool that answers "which documented git states does
this fence refuse?" with a frozen denominator.

**Instrument (this round, committed).** `plans/round50_c1_verify.py` — one command, four legs, one predicate:
`POPULATION` (126 honest fixtures rebuilt and identity-compared to the pinned `tree_sha256` rows),
`HONEST` (each must be admitted), `REFUSALS` (the 20 frozen modules of `plans/refusals46/` must be refused),
`SEALED` (the 12 frozen modules of `plans/sealed46/` plus the blind `plans/sealed50/` modules authored this round
must be refused), `MUTANTS` (each frozen mutation of the fence must change the verdict vector; floor 12).

Honest population = 126: the 104 battery fixtures of `plans/battery42|43|44`, the 9 r46 novel classes, the 7 r48
classes, the 4 r49 classes (`n17` replace refs, `n18` shallow boundary, `n19` template-less init, `n20` linked
worktree) and two r50 classes (`n21` separate gitdir inside `d`, `n22` alternates inside `d`). Population
composition and every fixture's identity are in the pinned file; `CHECKS all-ok` at build.

Why exactly two new classes and not three: the r49 critic documented three in-`d` indirection shapes — separate
gitdir, alternates, `commondir`. A `commondir` file is written by git only for a linked worktree (already `n20`),
so a hand-forged standalone `commondir` adds no state git itself produces; it is recorded as a decided exclusion,
not an unknown. The population is frozen at 126 before any fence measurement in this round.

**Before.** Base fence `05d5fe03…` on the frozen population: `HONEST fixtures=126 admitted=113 refused=13`
(control receipt below). No committed counter existed that could produce that number.

**After (claim).** At the landing tip, on a clean clone:
`python3 plans/round50_c1_verify.py --lane .` prints, in this order,

    POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
    HONEST fixtures=126 admitted=126 refused=0 error=0
    REFUSALS total=20 clean=20 leaked=0 build_errors=0
    SEALED total=<S> clean=<S> leaked=0 build_errors=0
    MUTANTS total=<M> caught=<k> broken=0 floor=12 verdict=met
    PREDICATE R50-C1 pass

and exits 0. `<S>` ≥ 18 (12 frozen + ≥6 blind) and `<M>` ≥ 12 with `<k>` ≥ 12 are literals in the counter
(`SEALED50_MIN`, `MUTANT_MIN`), not values the counter can satisfy from the files it reads.

**Kill rule (frozen).** C1 is NOT admitted if any of: `HONEST admitted < 126`; any refusal or sealed module not
refused; `mismatched > 0`; `PREDICATE` line absent or `fail`; exit code ≠ 0; the predicate runs on a dirty tree;
or any control below reaches the predicate.

**Controls (must fail; cheapest first).** All four are committed fences under `plans/controls50/`, run through the
same counter with `--allow-dirty` on the stage-1 tree, receipts in `.ufo/waves/round-50/claims/`:

| control | skips | expected |
|---|---|---|
| `plans/fixture_fence.py` @ stage 1 (do-nothing) | all claimed work | `PREDICATE fail` on `HONEST admitted=113` |
| `plans/controls50/admit_all.py` | refusal reasoning | `PREDICATE fail` on REFUSALS/SEALED leaks |
| `plans/controls50/refuse_all.py` | admission reasoning | `PREDICATE fail` on `HONEST refused=126` |
| `plans/controls50/keyed_names.py` (Q39 shape keys) | boundary reasoning | `PREDICATE fail` on the in-`d` honest classes it refuses |

A control that reaches `PREDICATE R50-C1 pass` before the round's data invalidates the counter and the target and
the round is re-designed before any scoring (run-6 lesson; the do-nothing control was run at stage 1 and fails).

**Open window (instrument repairs, before the stage-3 scored run).** The counter, the population builder and the
mutant battery may be repaired between the stage-1 commit and the stage-3 scored run only, and only for: a
measured defect (a leg that cannot run, a false clean, an unreproducible fixture), filling `<S>`/`<M>` pins, and
re-deriving mutant rows whose kill direction was not witnessed on the candidate fence (QUALITY Q38: a frozen
mutant's kill direction is witnessed, not assumed). Every repair records old→new digest in this file and in the
stage-2 commit: the predicate sentence, the four leg names, the literals `126`, `20`, `12`, `SEALED50_MIN` and the
population pin never change. A repair after the first scored run is not this claim's instrument.

**Stages (all three commits must exist for the claim to be judgeable).**
- **S1 (this commit):** claims, counter, C2 command, control fences, the 126-fixture population with its builder,
  receipts and pins, the carried r49 mutant battery (candidate only).
- **S2 (open window closed):** the repaired `plans/fixture_fence.py`; the re-derived `plans/mutants50/` with a
  witnessed kill for every frozen row; `plans/sealed50/` (blind hostile modules); the control receipts re-run on
  the S2 tree. No scored counter run before this commit exists.
- **S3 (receipt):** the scored run of the frozen predicate on a clean clone of S2/S3, committed as
  `corpus/evidence/round50/c1-receipt.txt` with `REV`, the exact command and its full output.

**Named limits.** The counter measures admission decisions only. The outside-`d` read property stays with
`plans/round46_c1_verify.py`, unchanged and not re-scored here; the repaired fence starts no git child at all, and
that counter is run as supplementary evidence (not part of this predicate). io_uring and host paths outside the
scratch root are not observed. The population is host-sensitive where git output is (`hooks/*.sample`,
`info/exclude`, `git worktree --relative-paths` ≥ 2.48, git 2.56.0 here); identity pins make that visible rather
than silent. Fixture semantics are "states git itself writes", not "all states a third-party tool may write".

**Sourced basis.** C1's knowledge entry cites the rows opened this round for the documented git store shapes the
two new honest classes use — `git-init(1)` `--separate-git-dir` and `gitrepository-layout(5)`
`objects/info/alternates`, `refs/replace`, `.git/shallow`, `FETCH_HEAD` (`corpus/SOURCES.md`, rows added this
round; ids in the round lesson).

## C2 — calibration (8 → 9): every artifact pointer the self-assessment files carry resolves

**Claim.** At the landing tip, `python3 plans/round50_c2_audit.py --lane .` prints
`POINTERS total=… unresolved=0` and exits 0, over a frozen surface: every `plans/…`/`corpus/…` artifact path in
`SCORECARD.md`, `SHONEN.md` and `PROVINCE.md`, plus every 40-hex hash in them (must exist and be an ancestor of
the branch tip). This is the calibration rubric's own condition (c): "this file exists and every row's pointer
re-runs".

**Before** (measured at `71f5f5f`, 2026-10-28, receipt `.ufo/waves/round-50/claims/c2-before.txt`):
`POINTERS total=271 paths=213 hashes=58 resolved=259 … unresolved=12`, of which six pointers name counters the
lane's last three rounds promised in a row's "counting command" cell and never committed
(`plans/round48_c1_verify.py`, `plans/round48_c2_verify.py`, `plans/round49_c1_verify.py`, `plans/round49_c2_verify.py`,
`plans/round34_c1_verify.py`, `plans/round34_defects.py`, `plans/round34_mutate.py`, and four corpus paths).

**After.** Every unresolved pointer is resolved by an append-only correction row in the `## Round 50 — C2
corrections` block of `SCORECARD.md`:

    SUPERSEDED <pointer> -> <target>          # target exists at the tip
    SUPERSEDED <pointer> -> never-landed      # only when `git log --all --oneline -- <pointer>` is empty

and the audit exits 0. **Kill rule:** any unresolved pointer or hash; a correction row whose target does not
exist; a `never-landed` row for a path that is in history; a correction that rewrites earlier SCORECARD text
instead of appending. `--selftest` must show a bogus pointer added to a scratch copy is the only new unresolved
row (it does: `.ufo/waves/round-50/claims/c2-selftest.txt`).

**Non-reachability.** The do-nothing control is the same command at `71f5f5f`: `unresolved=12`, exit 1.

## Frontier step (§2b) and assimilation (§10)

- `corpus/SOURCES.md` curated this round: rows opened for the git-surface documentation C1 rests on, plus the
  census before→after (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`).
- One mistake mined into `corpus/lessons/round-50.md` `## Mistakes`.
- At least one sourced claim: C1 (above).
- Assimilation: one `considerthese/` proposal if it fits the claims; otherwise the report says
  `Assimilation: none` with the reason. `merge/kengaku/` package: not adopted this round (the round's claims are
  internal instruments; the report records the choice).

## Round shape

One v2 build-and-attack wave (policy v2, band 64–128) inside the 64–128 seat band; the L1 holds the canonical
planner seat; ≥25 % attack roles; the wave's `reportDir` is `.ufo/waves/round-50/w1`. Seats never edit production
files, never commit, and write only their own report plus scratch under `/fast/scratch/hyaku/kengaku-r50/<seat>/`.

## Open-window instrument repairs (recorded before the first scored run)

| when | instrument | old digest | new digest | measured defect | effect on the predicate |
|---|---|---|---|---|---|
| 2026-10-28, before any scored run | `plans/round50_c1_verify.py` | `f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76` | `d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2` | module attribution keyed on `path.name`, so the same filename in `plans/battery42` and `plans/battery43` (e.g. `a_class.py`) made the hostile/honest leg attribution ambiguous; a leg could read another module's verdicts | none: predicate sentence, the four leg names, the literals `126`, `20`, `12`, `SEALED50_MIN` and the population pin are unchanged; re-measured do-nothing control still prints `HONEST fixtures=126 admitted=113 refused=13` and `PREDICATE R50-C1 fail` |

## Open-window repair 2 (recorded after the first scored run; see the round report erratum)

| when | instrument | old digest | new digest | measured defect | effect on the predicate |
|---|---|---|---|---|---|
| 2026-10-28, after the first receipt | `plans/round50_c1_verify.py` | `d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2` | `850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999` | `R50C1CritPredicate` measured that the in-process fence call lets a hostile fence rewrite the counter's globals and forge `caught`, and that fixture parent names carried the leg ("refusals46"/"sealed46") so a name-keyed fence passed `--skip-mutants` | none: predicate sentence, four leg names, literals `126`, `20`, `12`, `SEALED50_MIN` and the population pin unchanged. Deviation from "a repair after the first scored run is not this claim's instrument" is recorded, and the round's scored receipt is the post-repair re-run, not the earlier one |

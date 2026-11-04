# ScribeCorrectionsR77 — scoped report

Date: 2026-11-04. Axes: coverage and calibration. Deliverable: correction proposals for R77-C2 legs V3/V4/V6; no claim of executed discharge.

## Behavior and touched surfaces

Wrote only:

- `.ufo/waves/round-77/w1/proposals/corrections.md`: three dated, single-physical-line V3 correction blocks; one V4 LOG block; two V6 append-only clarification blocks and a two-site occurrence inventory.
- `.ufo/waves/round-77/w1/ScribeCorrectionsR77.md`: this report.

No production file, counter, ledger, git state, PATH directory, other lane or fleet tracked file was written by this seat. No install, new runtime, subagent, fixture, commit, push or gate execution occurred. No scratch directory was created. `functions.glob` for `/fast/scratch/hyaku/kengaku-r77/ScribeCorrectionsR77` returned `Skipped missing paths`; there is no seat-created scratch to delete.

## Provenance and exact observations

The full frozen claims file was read before any shell command. `skill://godspeed` was read; the assigned axes are coverage/calibration. Required lesson passages and counter V3/V4/V6 implementation were read. `functions.read`/`functions.grep` outputs are observations, not process exit-code receipts.

Shell commands actually executed:

1. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format=%H -- plans/round-77-claims.md` — rc 0; printed `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`.
2. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb -- PROVINCE.md LOG.md SCORECARD.md corpus/lessons/round-76.md` — rc 0; showed existing integration additions for V3/V4 and the PROVINCE capability-name replacement. Those changes were not made by this seat.

Target searches actually executed with `functions.grep` (literal path prefix below is `/home/vgpnk/Projects/shokunin/kengaku-shokunin/`; patterns are tool regexes, not claimed shell executions):

- Pattern `R76-V[346]|^##|Second-reviewer|agree=9|agree=8|wrong=12|wrong=13|Census|instrument` over `corpus/lessons/round-76-verifier-spotcheck.md`, `corpus/lessons/round-76.md`, `LOG.md`, `SCORECARD.md`: initial multi-file results capped; subsequently narrowed reads/searches located all required sections.
- Pattern `Round 76|round-76|Second-reviewer|agree=9 disagree=2|wrong=12|wrong=13` in `LOG.md`: original before reading at 2873; appended V4 heading at 2910; concurrently added V3 correction at 2923 onward.
- Pattern `Round 76|Round-76|agree=9 disagree=2|wrong=12|wrong=13|declared-surface-resolver|province-surface-resolver-table-anchored` in `SCORECARD.md`: main rows 3454–3455 retain superseded values; final C2 reading at 3549; existing correction at 3554 onward.
- Pattern `declared-surface-resolver|province-surface-resolver-table-anchored` in `PROVINCE.md`, `SCORECARD.md`: exactly two returned sites, PROVINCE.md:999 and SCORECARD.md:3509, both current canonical name; no legacy-name site returned.
- Pattern `AGREE|SELFTEST|MUTANTS|SCOPE|cases=|expected_matched|survived` in six `corpus/evidence/round76/` files (`c1-before.txt`, `c2-before.txt`, `c1-selftest.txt`, `c1-mutants.txt`, `c2-selftest.txt`, `c2-mutants.txt`): printed `AGREE agree=8 disagree=3`; `SCOPE ids=7 registered=0 closed=0 open=7 discharged=0 legs_passed=0 legs_pending=2 wrong=13`; `SELFTEST cases=12 red=11 failures=0 ok=True`; C1 `MUTANTS total=9 killed=9 expected_matched=9 wrong_id=0 survived=0`; `SELFTEST cases=14 red=13 failures=0 ok=True`; C2 `MUTANTS total=12 killed=12 expected_matched=12 wrong_id=0 survived=0`. Stored receipt text only; none rerun.
- Pattern `correction_pairs|agree=9 disagree=2|wrong=12|Second-reviewer classes|declared-surface-resolver|province-surface-resolver-table-anchored|dated =` in `plans/round77_c2_defect_discharge.py`: lines 222–224 define the three V3 literal pairs; 237 requires a date on the matching physical line; 248 checks V4 heading text; 270–276 require canonical names and reject the legacy PROVINCE token.

## Findings

1. **V3 proposal covers both requested value pairs and all three files.** Each proposed correction line includes `2026-11-04`, `superseded`, `agree=9 disagree=2` → `agree=8 disagree=3`, and `wrong=12` → `wrong=13`. It also corrects the lesson's actual `wrong=14` and the stale LOG battery counts. This avoids attributing SCORECARD's original `wrong=12` to the LOG or lesson. Sources: lesson Census lines 58–61; closure V3 lines 196–203; receipt search above.
2. **Existing integration corrections moved during observation.** Early tool output split both agreement literals across physical lines in LOG and lesson; later reads/diff showed joined, dated lines. The proposal keeps each complete correction on one physical line, as required by counter lines 234–239. No gate result is inferred from these reads.
3. **V4 block is a present-day erratum, not historical evidence at commit R.** Closure lines 204–207 name `d31feec9` and the missing `Second-reviewer classes` entry. Lesson lines 120–123 supply the three A9 classes and the limits. Proposal explicitly says appending now does not make the block exist at commit R. Current LOG already has an added block at 2910–2921; do not blindly duplicate it. The proposed version preserves the lesson's caveat about fence stripping rather than asserting universal fence stripping.
4. **V6 occurrence census:** frozen PROVINCE.md:999 used `declared-surface-resolver`; current PROVINCE.md:999 and SCORECARD.md:3509 use `province-surface-resolver-table-anchored`. Historical/current difference is directly printed by the read-only git diff; the literal search returns only these two sites in the two requested files.
5. **V6 contract conflict, verbatim:** item: "Every draft must be copy-pasteable markdown and must not reflow the filed lines (append-only)." Frozen counter: `hits = [ln for ln in province.splitlines() if "declared-surface-resolver" in ln]`; `if hits: return "fail", f"PROVINCE.md still names declared-surface-resolver ({len(hits)} lines)"`. An append alone cannot remove the visible legacy token at the freeze. The observed integration already replaced that token in place. This seat reports the conflict without changing contract, target or implementation, and provides append-only clarification text rather than editing production. Canonical judgment remains external to this report.

## Gates and known limits

Executed gates: **0**. No R77-C1/R77-C2 pass, leg-pass, ledger discharge, receipt honesty or final landing-tip result is asserted. Grepped receipt totals are transcription evidence only. The V4 draft records filed A9 content; it does not independently execute or rederive A9. Concurrent production changes mean line numbers describe observed snapshots, not a promised final tree.

Main-agent integration checks to run, not run by this seat:

- From the lane: `python3 plans/round77_c2_defect_discharge.py --lane .`; acceptance remains exactly the frozen scope/predicate/rc target.
- Confirm appended corrections and the V4 block at the actual evidence-carrying commit before closing ledger rows; no report text substitutes for evidence-at-close ancestry/literals.

Out of scope: V1/V2/V5/V7 repairs, canonical C1 table integration, production edits, ledger rows, receipt minting, commits, judgment, promotion and cross-lane work.

## Self-evaluation

Accuracy 4/5: direct source/receipt transcriptions; no final gate execution claimed. Completeness 4/5: all three requested legs and two capability sites covered; V6's frozen append-only conflict remains an integration/judgment constraint, not silently resolved. Clarity 4/5: destinations and historical/current state separated; report includes detailed evidence rather than a short summary. Actionability 4/5: copy-paste blocks supplied, but existing concurrent additions require avoiding duplicates. Conciseness 4/5: source-to-value details are retained for auditability. Mean 4.0/5. Highest-impact improvements are final-tip gate evidence and evidence-at-close binding, both intentionally owned by integration. User-agreement self-check: the proposal is complete as a proposal, not an executed discharge.

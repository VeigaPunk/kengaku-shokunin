# ScribeR91 — round-91 scribe report (leaf seat, drafts only)

Scope: the LOG.md Round 91 entry, the SCORECARD Round 91 section (before→after table per claim, prediction ledger) and the report's Sources & frontier section, drafted from measurements at BASE `59764383d4dd33d58faa50daad4c06d0cde410aa` and the measured tip `a8de3e6933a220ad12e3fb3523ce4627a44c8cf0`. The lane was not written; nothing was committed, pushed or staged. The drafts sit under `.ufo/waves/round-91/w1/ScribeR91/`.

## Files written

- `.ufo/waves/round-91/w1/ScribeR91/log-entry.md` — LOG.md Round 91 entry.
- `.ufo/waves/round-91/w1/ScribeR91/scorecard-r91.md` — SCORECARD Round 91 section: claim table, prediction ledger, controls, capability, planned.
- `.ufo/waves/round-91/w1/ScribeR91/sources-section.md` — report Sources & frontier section.
- `.ufo/waves/round-91/w1/ScribeR91.md` — this report.

## Verdicts (measured; the frozen predicates decide)

| claim | verdict | evidence (command, exit code) |
|---|---|---|
| R91-C1 coverage | **not met** at tip | `python3 plans/round91_c1_replay.py --lane . --rev a8de3e69… --work DIR` → `TARGET … executed=0 cases=10 legs=20 mismatches=10 defects=10`, ten `DEFECT L5 receipt names unknown case ?`, `PREDICATE R91-C1 fail`, **rc 1**. At BASE `59764383…`: `executed_rows=34 … defects=9`, `PREDICATE R91-C1 fail`, **rc 1**. |
| R91-C2 calibration | **met** at tip (ceiling held) | `python3 plans/round91_counter_pin.py --lane . --rev a8de3e69… --work DIR` → sixteen `PIN-OK`, `PINS checked=16 matched=16 mismatched=0`, `SELFTEST cases=8 red-green-ok=8`, `PREDICATE R91-C2 pass`, **rc 0**. At BASE: `DEFECT SETUP unreadable plans/counter-pins-r91.json`, `PREDICATE R91-C2 could-not-evaluate`, **rc 2**. |
| R91-C3 operability | **not met** at tip (BASE and tip identical) | `python3 plans/round91_burndown.py --lane . --rev a8de3e69… --work DIR --freeze-round 92` → `freeze=refused oldest_pending_round=82 pending=30 parked=7 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=34 checks_run=114 overrides=3`, `PREDICATE R91-C3 fail`, **rc 1**. Same at BASE with the tip script, **rc 1**. `--selftest` → `cases=13 red-green-ok=13`, **rc 0**. |
| F1 companion (R82-F1) | met at tip; BASE not reproduced | `python3 plans/round91_f1_counter.py --lane . --work DIR` at tip → `PARSED S260=1,S261=2,S265=1,S266=2`, `ANCHORLINE rows=274 cited=84 captured=71 uncaptured=13 defective=10 repaired=10 live=0`, `PREDICATE R91-F1 pass`, **rc 0**. At BASE (tip counter, BASE checker) → `AttributeError: … no attribute 'anchor_quotes'`, **rc 1**. |
| Census | ok | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, **rc 0**. |

Round outcome: one of three claims met (C2). The companion F1 counter passes at tip. Coverage and operability do not move.

## Findings (ordered by weight)

1. **C1 fails at the measured tip because the frozen counter cannot read the probe's receipt.** `parse_receipt` (`plans/round91_c1_replay.py:69–86`) takes the case id from an `id=` token; the probe writes `CASE <id> predicted=… observed=…` (`plans/round91_modernize_probe.py:165`), so every id parses as `?` and L5 fails ten times. The probe's own receipt has ten `ok=True` lines. The gate worked as designed (`executed=0`). The ledger row still flipped to executed (34 → 35 of 88), so the ledger and the claim verdict disagree at the tip. Routed to round 92 as a new frozen amendment; the frozen counter must not be edited in place.
2. **C3 has no round-91 triage at the measured tip.** `corpus/routed-findings.jsonl` is byte-identical at BASE and at `a8de3e69` (blob `830c0dae…`), and the frozen Move says the triage lands in the measured tip. The gate's output is identical at both revisions; the "before→after" for C3 is therefore nil. The freeze cannot be admitted at this tip.
3. **The R82-V8 repair named in the frozen C3 Move did not land.** `plans/round83_c2_checks.py` has no change since `ddb903a8` (round 83). `v8()` derives the fleet root from `origin.parent` (`:167–168`). From a clone with default origin the check fails (`CHECK v8 fail`, rc 1); with `R83_ORIGIN_REPO` and `R83_FLEET_REPO` set it passes (`CHECK v8 ok`, rc 0). This matches lesson M6 and is still live.
4. **The C2 kill rule and the frozen tip rule are contradicted by B2.** `git diff --stat 386184a6 a8de3e69 -- <pinned set>` prints `plans/counter-pins-r91.json` and `plans/round91_counter_pin.py` (105 insertions, 112 deletions). The frozen text voids C2 on any edit after commit B and says the same diff must print nothing. B2 is disclosed (M3) as made before scoring; but the selftest measured 4 of 8 at B before that correction, so "before any scoring" holds only for the tip. The operator must rule on this; the scribe did not reclassify C2.
5. **The gate's owner clause is too weak.** `R51-R3-R90` is `status blocked`, `owner "unowned:integrator"`. The non-empty-string check passes it; the frozen text requires the lane or seat that holds the fix. The four R51 blocked rows are not yet named to real owners.
6. **The gate prints more DEFECT lines than the L1's excerpt.** In a scratch clone the gate printed four lines: `override-unjustified R42-R2`, `override-unjustified R42-R3-33`, `override-unjustified R42-R3-37` (rows carry `override_reason` null) and `check-failed R82-V8`. The L1 excerpt names one line (`R42-R3-37`). The scribe did not run the gate in the lane (it would write into the lane tree) [INFERENCE: the lane-root run produces the same three override lines, since the row data is identical; the R82-V8 line is path-dependent].
7. **F1 BASE figure not reproduced.** The string `PARSE-ABSENT` is absent from both checker revisions; the tip counter against the BASE checker crashes. The L1's BASE figures for S260/S261/S265/S266 need a harness that runs at BASE, or a retraction.
8. **Wave shape disagrees with the frozen text.** The frozen round-shape says 12 seats with 5 executors; `.ufo/waves/round-91/w1/swarm-registry.json` has 11 members (executor 4, scout 1, connector 1, scribe 1, reviewer 1, critic 1, mutation-tester 1, sentinel 1). The task brief also says 11. Attack seats are 4 of 11 (36 %), connector 1. Only the registry is present in `w1/` at measurement time; seat reports are not in the lane.
9. **Prediction misses (recorded, not repaired):** C2 selftest 6 predicted, 8 measured; C3 selftest 9 predicted, 13 measured; C3 BASE malformed-unresolved predicted ≥1, measured 0 (1 invalid row); C3 BASE DEFECT class predicted as unresolved-invalid rows, measured as override and check defects; C3 after freeze predicted admitted, measured refused.
10. **Lane working tree is dirty.** At measurement: ` M SCORECARD.md`, ` M corpus/QUALITY.md`, `?? .ufo/waves/round-91/`. None were touched by this seat. The integrator must reconcile the working-tree `SCORECARD.md` with the drafted section.

## Discrepancies with the L1 measurement set

- ANCHORLINE `rows`: the L1 wrote 272; the counter prints `rows=274` at the tip (census also 274). Recorded as 274.
- Ledger counts, the C1 BASE figures (`executed_rows=34`, `defects=9`), the C2 BASE and tip figures, the C3 BASE/tip gate line (`freeze=refused … pending=30 parked=7 … seeds_83_91=46 resolutions=34 checks_run=114 overrides=3`), the C3 selftest 13/13, and the census exit 0 all matched my re-runs.
- C1 tip: the L1 figures (`executed_rows=35 … cases=10 legs=20 mismatches=10 defects=10`, `PREDICATE R91-C1 fail`) matched.

## Procedure and hygiene

- Scratch: `$HYAKU_SCRATCH/kengaku-r91/ScribeR91/` (`HYAKU_SCRATCH=/fast/scratch/hyaku`): one `git clone --shared` of the lane at `clone/` (detached checkouts of BASE and tip, read-only in effect), copies of the tip counters under `tip-tools/`, work dirs for each counter run. Every clone command ran against `git -C … rev-parse --show-toplevel`. No git mutation was made in the lane; the only lane-side commands were `git show`, `git diff --stat`, `git log`, `git rev-parse`, `git status` and `git cat-file`.
- Scratch is deleted on exit (`rm -rf -- "$S"` as the last command of this seat).
- Tools installed or upgraded by this seat: none. No pacman, no sysctl change, no `~/.omp` or `mcp.json` change, no write to the fleet root.
- The counters were run from scratch copies; the BASE gate runs used the tip scripts copied into scratch, because the BASE tree does not contain them (their rc 2 "no such file" run was discarded and re-run).

## Not done

- The frozen controls named in the C1 and C2 Move (ledger-only, forged-tip, forged-stamp, decorative-stamp, executed-gating; one-byte mutation, absent path, tampered pin) were not re-run by this seat. Their figures are the L1's and are not restated.
- No lane-root run of the gate (to avoid writing into the lane); the lane-root behaviour of finding 6 is an inference.

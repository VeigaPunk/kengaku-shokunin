# Round 34 — honest stop: evaluator coverage and counter calibration (2026-10-25, hyaku run 7)

Baseline `5022357cc69334e83b5a2f76c34daea440077a57`; frozen claims `plans/round-34-claims.md` (freeze `adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae`). One v2 wave: 64 seats; 64/64 spawned; no residual call. Results: `.ufo/waves/round-34/build-results.json`.

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| C1 Terminal-Bench `protein-assembly` evaluator | **Not admitted** | The pinned evaluator and environment captures exist; however C1's frozen counter review finds V3/V4/V5/V6/V7/V8 false greens and V7 red on the truthful freeze receipt (`.ufo/waves/round-34/build/R34ReviewCounterC1.md`). The entry also overstates expected-artifact grounding and Harbor context (`R34CriticEntryTB2.md`). Flip only after the frozen predicate's exact source-row, README-section, truthful control, and evaluator-manifest checks pass on committed bytes and independent source review agrees. |
| C2 defect counter + mutation harness | **Not admitted** | Frozen predicate unsatisfied: initial clean harness output is red on N3/N4/N7; mutants M4/M7/M8 map to checks/surfaces they do not affect; width/newline receipt did not run the mutated sandbox probes (`R34ReviewClaimsFile.md`, `R34CriticC2.md`, `R34MutC2Harness.md`). Flip only with a clean-tree green run and eight class-aligned mutants producing expected named defects, with receipts. |
| Quarantine S091 → S108 | **Refused** | This round's NEC capture is Access Denied (418 bytes) and does not contain the staged quote (`assimilation/quarantine-verdicts.txt`); flip when a capture at the source locator yields a located ≤25-word quote. |
| Quarantine S105 → S109 | **Not appended** | METI archive quote is located, but no admitted entry cites it; CORPUS rule 4 forbids adding an uncited row. Flip when a later admitted entry cites a re-grounded S109 row. |
| Package candidates | **0 admitted; 6 refused/held as staged** | Package screen lists missing live rows, Q1/Q2/Q3 failures, or no new ground; see `.ufo/waves/round-34/build/R34ReconPackage.md`. |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| control/predicate drift | `plans/round-34-claims.md` C1 control text vs `claims/control-c1.txt`; V7's required `label = value` strings are not present in the frozen receipt (`build/R34ReviewCounterC1.md:57-64`) | frozen control binding and independent counter review | bind the checker to the exact committed receipt bytes/digest and freeze a control whose content can satisfy the declared check; demonstrate a changed receipt fails before counting. |
| mutation mapping/surface mismatch | `.ufo/waves/round-34/build/R34MutateDraft/round34_mutate.py`; C2 mapping F2/M4/M6/M7/M8 does not exercise the named check surfaces (`build/R34ReviewClaimsFile.md:43-59`) | frozen C2 mapping + reviewer | each mutant must edit the exact file read by its expected N-check; run against a clean clone and preserve both clean and red outputs. |
| quarantined source inaccessible | `.ufo/waves/round-34/assimilation/captures/nec-s091.html` (418-byte denial page; quote absent) | CORPUS SOURCES rule 1 / quarantine hand-check | refuse S091 now; reopen from an accessible source copy and locate the quote before adoption. |

## Assimilation record

Read-only package screen: six entries screened, zero admitted; refusal/open reasons in `build/R34ReconPackage.md`. Considerthese proposal 2 was mined into a Q23 draft (`build/R34Considerthese/q23.md`) but not added to QUALITY.md because C2 failed. Quarantine slice derived from the source register contains S091 and S105 (`build/R34ReconQuarantine.md`). S091 refused; S105 source quote found, but no row appended because no admitted entry cites it.

## Census

Before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` — 15 W04, `kengaku ok`, exit 0 (`corpus/evidence/round34/census-before.txt`). After: same command — output in `corpus/evidence/round34/census-after.txt`, exit 0. SOURCES remains 97 rows; additions by tier A/B/C = 0/0/0; rows touched 0→0; frontier rows advanced 0.

## Seat ledger

One v2 wave: 64 seats. Mix: executor 17, scribe 10, scout 9, reviewer 9, mutation-tester 8, critic 6, connector 3, sentinel 2. m_flash roles (executor/scribe/critic/sentinel) = 35/64 (54.7%); attack roles reviewer/critic/mutation-tester = 23/64 (35.9%). Planner held by L1. Results `../.ufo/waves/round-34/build-results.json`; dead-seat count/statuses are in that results file.

## Gate timing and source notes

No knowledge entry or registry row was admitted. The two quarantine captures are `assimilation/captures/{nec-s091-reopen.html,geniac-s105-reopen.html}` and their `captures/quarantine-SHA256SUMS`; the opened NEC response was unavailable, while the METI archive paragraph was located.

## Frontier clarification

The round-31 frontier sentence that says the Terminal-Bench 2.0 "axis-E cell is filled" describes verifier-execution context only; it did not read task-level scoring assertions. Round-34 opened `protein-assembly/tests/test_outputs.py` but the C1 counter/admission failed, so this task-level scoring-code ground remains unadmitted and the frontier stays open. Evidence: `corpus/README.md` round-31 bullet (clarified in round 34); `R34ReviewCounterC1.md`; `R34CriticFrontier.md`.

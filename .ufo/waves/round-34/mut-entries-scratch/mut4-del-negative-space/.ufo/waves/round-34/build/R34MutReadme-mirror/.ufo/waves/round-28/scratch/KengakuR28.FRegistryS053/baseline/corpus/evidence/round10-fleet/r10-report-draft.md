# kengaku-shokunin — round 10 report

Lane: `kengaku` (child repo `kengaku-shokunin/`, axes **novelty + calibration**; domain: LLM eval/research). Report model: `{{MODEL}}`.
Axis-move: **operability 4 → {{OPERABILITY_AFTER}}** — a hermetic in-repo grader (`grader.py`, repo root) that replays the committed probe evidence offline and exits 0/1/2.
Pre-round HEAD `1bd17ec`; child-repo round-10 commit `{{CHILD_COMMIT}}`; main-repo report commit `{{MAIN_REPORT_COMMIT}}`.

## The move — `grader.py`, a hermetic replay gate

`python3 grader.py [--selftest] [--r8-jsonl P] [--r8-runlog P] [--r9-jsonl P] --r9-md P` — stdlib only, no network, deterministic across runs (`PYTHONHASHSEED`-independent: never iterate sets for ordering-sensitive results). Defaults resolve relative to the script's own directory (repo root): `corpus/evidence/round8-horizon/{results.jsonl,run.log}` and `corpus/evidence/round9-replication/{results-r9.jsonl,replication.md}` (268 / 284 records). Exit 0 = every recomputed value matches the stored one; 1 = at least one mismatch, each printed `MISMATCH <check-id>: stored=<x> recomputed=<y>`; 2 = missing/unreadable input. `--selftest` corrupts temp copies internally (flip one stored `ok`; edit one `run.log` SUMMARY number; flip one byte inside a `raw` string) and passes (exit 0) only when all three corruptions are detected (grader exit 1 on each).

Falsifiable target, quoted from `SCORECARD.md` §Planned (`:79` section, target sentence `:86-90`):

> Falsifiable target: `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' | wc -l` ≥ 12 **and** the grader exits 0 on the committed files while exiting 1 on a deliberately corrupted copy (one flipped `ok` field), with both runs recorded in `LOG.md`.

Measured base: the count half is **already 12 before this round's file lands** (§Calibration errata), so the binding halves of the target are the exit-0/exit-1 pair plus the recorded runs; post-move count re-run in Results.

## L2 fleet (10 agents, one batched call)

Task lines transcribed from each L2's own dispatch brief (`history://<Id>:1-22`, read 2026-09-28 19:0x). No L2 wrote into the repo (single integration owner: L1).

| Agent (role) | Task | Artifact |
|---|---|---|
| ScoutEndpoint (scout) | `:34113` served-model surface: `/v1/models`, `/health`, llama-server pid + full cmdline — closes `PROVINCE.md`'s "documented from behaviour" ceiling | `local://r10-scout-endpoint.md` |
| ScoutWiki (scout) | llm-wiki digest queue vs disk: each queued source exists? already cited? + freshness sweep against `LOG.md` mtime | `local://r10-scout-wiki.md` |
| ScoutBench (scout) | `~/bench-arena` inventory + 3 load-bearing corpus claims re-derived (REPRODUCES / DRIFTED / UNVERIFIABLE) | `local://r10-scout-bench.md` |
| CriticScorecard (critic) | adversarial re-run of every round-9 post-move SCORECARD pointer, incl. the 11-vs-12 operand; count falsified claims | `local://r10-critic.md` |
| ReviewerCites (reviewer) | citation resolution ≥90%: SKILL.md cited sources, knowledge source lines, prior-art URLs (status codes) | `local://r10-review-cites.md` |
| ConnectorSiblings (connector) | sibling gate conventions (`kagi-shokunin/corpus/drift-pins.sh` reference) + adoption recommendations for `grader.py` + overlap rulings | `local://r10-connector.md` |
| LabratSchema (labrat) | schema invariants of both probe files (cell/key-set census, duplicates, truth alignment) so `grader.py` assumes nothing false | `local://r10-labrat-schema.md` |
| MutationHarness (mutation-tester) | M0–M3 mutation battery `/tmp/kengaku-r10/mutate_test.sh` (M0 control, M1 `ok` flip, M2 SUMMARY edit, M3 `raw` corruption) | `local://r10-mutation-sh.md` |
| ExecutorDocs (executor) | draft `SKILL.md` §"Hermetic grader", README evidence row, `LOG.md` round-10 entry | `local://r10-drafts.md` |
| ScribeReport (scribe) | this report skeleton (draft-only; L1 lands it — no repo writes) | `local://r10-report-draft.md` |

## Results

- Grader checks: **{{GRADER_CHECK_COUNT}}** (r8 side: all 11 `run.log` SUMMARY lines + per-record re-parse/re-grade; r9 side: 4-cell pass/`nwrong` table, record counts, ack-compliance); check inventory: {{CHECKS_PTR}}.
- Exit-0 run on committed bytes: {{EXIT0_RUN}} — output head `{{EXIT0_HEAD}}`.
- Mutation battery on copies: M0 → {{M0_RESULT}}; M1 → {{M1_RESULT}}; M2 → {{M2_RESULT}}; M3 → {{M3_RESULT}}.
- `--selftest`: {{SELFTEST_RESULT}} (expected: exit 0, 3/3 corruptions detected).
- Post-move runnable count: `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' | wc -l` → **{{RUNNABLE_COUNT_AFTER}}**.
- SCORECARD deltas: operability 4 → **{{OPERABILITY_AFTER}}**; {{OTHER_AXIS_DELTAS}} (candidates this round: coverage via the fleet-artifact index, freshness via the endpoint/bench re-verifications; any row whose ceiling line changed must be recorded here).
- Both grader runs recorded in `LOG.md`: {{LOG_REF}}.

## Calibration errata — runnable-file count 11 vs 12

- L1 measured `git ls-tree -r 2575be6 --name-only | grep -cE '\.(py|sh)$'` → **12**, while `SCORECARD.md:58` records "Runnable files in-repo went 0 → 11" under `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' | wc -l` → 11. Re-measured at filing time: the same find command → **12**; the 12 entries are `corpus/evidence/round9-fleet/*.py` (9) + `round8-horizon/horizon.py` + `round9-replication/{replicate.py,run_r9.py}`, with no `.sh` in the listing. Before-side re-check: `git ls-tree -r f147a27 --name-only | grep -cE '\.(py|sh)$'` → **0**.
- Cause: the 11 was accurate when written and was overtaken by a script landed later in the same round; which file landed last is unrecorded ({{WHICH_FILE_WAS_12TH}}). `LOG.md:16` reconciled two other figures from the same row-set (19 fleet files; 11/11 lessons rows) and did not touch this one.
- Consequence for this round: the ≥12 half of the §Planned target is already satisfied pre-move; the report states {{RUNNABLE_COUNT_AFTER}} and rests the falsification on the exit-code pair.
- Second spec drift found while measuring: `SCORECARD.md:83` names the grader source as `corpus/evidence/analyze.py`, which does not exist (`test -e corpus/evidence/analyze.py` → exit 1); the analyzer on disk is `corpus/evidence/round9-fleet/analyze.py`, and the pinned CLI spec lands the gate at repo-root `grader.py`. SCORECARD update covering both drifts: {{SCORECARD_UPDATE_REF}}.

## Next planned move

{{NEXT_MOVE}} — read from `SCORECARD.md` §Planned after the round-10 update; candidate ceilings it may quote: {{NEXT_MOVE_CANDIDATES}}.

## Commit hashes

- Child repo (`kengaku-shokunin`): `{{CHILD_COMMIT}}` (round-10; pre-round HEAD `1bd17ec`), `LOG.md` line {{LOG_LINE}}.
- Main-repo report commit: `{{MAIN_REPORT_COMMIT}}` for `.ufo/reports/round-10/kengaku.md`.
- Push evidence: `{{PUSH_EVIDENCE}}`.

## Template sections to complete (round-9 report parity)

- Changes landed ↔ `LOG.md`: {{CHANGES_TABLE_ROWS}} (LOG line → content → files).
- Cross-domain evidence — reported, not absorbed: {{ROUTED_ROWS}} (item | owner lane | disposition); `ConnectorSiblings`'s artifact is the input.
- SHONEN four boxes re-marked: {{SHONEN_MARKS}} with the verifying command per box — no `[x]` for lane-dispatched verification (`../PROTOCOL.md:39-46`: a subagent the lane dispatched is still the lane).
- Mission-age actuator: {{ACTUATOR_ROWS}} (fleet lanes + verdicts at filing time).

_Fill rule: every `{{...}}` is unfilled by design — copy values from L1's own run output, never from an L2 artifact second-hand; delete a placeholder only if its line is deleted whole._

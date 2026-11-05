author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 92 — non-author verifier spot-check

Reviewed lane tip: `1df7653633bd4c5a5f373d139f9f1ed02e0f9c07` (BASE `4ba56182307ccda1ec436bfe3d61cb3d92e56608`; freeze A `96f249e0`). Report: `.ufo/reports/round-92/kengaku.md` (fleet commit `ea96f154898ae0d5e16db911df62d6f8456a452e`, author `kengaku-shokunin <kengaku@shokunin.local>`). Driver digest (`.ufo/watchdog.log`, copied 2026-11-05): `2026-11-05T09:43:34-03:00 launch kengaku round=92 pgid=2856414 driver=hyaku-inline attempt=1`; `2026-11-05T12:11:56-03:00 lane-dead-no-report kengaku round=92; retry same round (hyaku-inline attempt=1 …)`; `2026-11-05T12:11:58-03:00 launch kengaku round=92 pgid=3370906 driver=hyaku-inline attempt=2`; `2026-11-05T12:48:46-03:00 complete kengaku round=92; hyaku-inline attempt=2`.

Method. Plain measurements over committed bytes (`git show`, `git diff --stat`, `git grep`, `git merge-base --is-ancestor`, `sha256sum`, `jq`-equivalent Python reads, census CLI). Lane counters, gates and selftests were **not executed** by this integrator (PROTOCOL §Gate standard, "Closure consequence"); their committed receipts under `.ufo/waves/round-92/` were read and graded evidence-verified. Live re-fetches were run for S283 and S286 only; the three own-work capture pins were re-hashed from the tracked bytes.

## 1. Step-1 conformance

| check | command (observed) | result |
|---|---|---|
| report commit attribution | `git log --format='%an %H' -- .ufo/reports/round-92/kengaku.md` → `kengaku-shokunin \| ea96f154898ae0d5e16db911df62d6f8456a452e` | lane identity ✓ |
| `## SHONEN` heading | report carries `## SHONEN` with four `[~]` lines matching the four SHONEN.md boxes; no `[x]` anywhere (`grep -n '\[x\]' SHONEN.md` → none) | ✓ one line per box, author-asserted |
| cited commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> refs/heads/master` for `96f249e0 4f6b3c52 f0018773 42bd5104 d1ccf56d b62ea270 6a51ff0e 1d5634e3 801b8157 5b6c00b8 a0c7438a b72c83e9 dd48027f 288511d8 bb29a660 1df76536` | all 16 ancestor ✓ (`2fd12b88` is the upstream terminal-bench-2 revision in the S283–S286 URLs, not a lane commit — correctly outside ancestry) |
| lane pushed, no leftovers | `jj-lane.sh state …` → `branch=master local=1df76536… remote=1df76536… ahead=0 behind=0`; `git status --porcelain` empty | ✓ |
| dispatch evidence | watchdog digest above; attempt-1 relaunch and attempt-2 completion match the report's stale-lane section | ✓ dispatched, terminated, re-dispatched same round |
| wave shape | `.ufo/waves/round-92/w1-results.json`: 12 seats, notes all null (no dead seats); executor 4, scout 1, connector 1, scribe 1, reviewer 2, critic 1, mutation-tester 1, sentinel 1; planner held by L1 | attack 5/12 = 42% (≥25%) ✓; connectors 1 (≤2) ✓; L2 floor ✓ |
| prompt template contract | `.ufo/prompts/kengaku-round-92.md`: zero `{{…}}` placeholders left; §1 MISSION/AXES binding, §3 ≥8 L2 in one batched call, §5 commit-then-push + push scope + L0 channel, §4 report path `…round-92/kengaku.md`, SHONEN heading duty (incl. the pre-commit `grep -c '^## SHONEN'` check), commit-hash citation, write scope `…/kengaku-shokunin` (lines 1, 82, 101, 118, 131–138, 448, 516–522) | ✓ all round-level and five child-lane items embedded |
| report sections | `## Work performed`, `## Landed changes`, `## Before → after measurements`, `## Sources & frontier`, `## Trend verdicts`, `## SHONEN`, Stale-lane, Honest limits, Admission | ✓ |
| L0 durability | three `kengaku \| round-92` lines at `.ufo/l0-questions.md:364-366`; fleet `git status --porcelain -- .ufo/l0-questions.md` empty (committed) | ✓ |
| misroot sweep | `cases_A.json` absent at fleet root; landed in lane at `bb29a660` | ✓ (M12 resolved as reported) |

Conformance defects (status-neutral, carried to round notes): none new. The report itself carries the round-91 erratum debt ("14 controls" wording, still unrepaired), the inherited `w1.ready` naming the attempt-1 L1, and the attempt-1 `w1-dispatch.json` rewrite — all disclosed; none bars admission.

## 2. Claims — re-derivation at `1df76536`

**R92-C1 — coverage (held at its L0 cap 7) — MET on its frozen predicate; re-measured.**
- Re-measured: `git show 1df76536:plans/grader-population-ledger.json` → members with `status=="executed"`: **36 of 88**; member `llm-inference-batching-scheduler` `status=executed`, round 92. At BASE `4ba56182`: **35 of 88**. The ledger flip 35→36 is real.
- Re-measured: the C1 counter is byte-unchanged after B2 — `git diff --stat f0018773 1df76536 -- plans/round92_c1_replay.py` → empty. Its green measurement is untainted by post-freeze edits.
- Evidence-verified (committed receipts, not re-run): `L1/c1-base.txt` (`executed_rows=35 … defects=9`, `PREDICATE R92-C1 fail`, rc 1); `L1/c1-tip-d.txt` at `b62ea270` and `L1a2/c1-head.txt` at HEAD (both `executed_rows=36 … mismatches=0 defects=0`, `PREDICATE R92-C1 pass`, rc 0) — quotes match the report verbatim.
- Residual (disclosed): the `sandbox-red` control is unmet (expected rc 2, observed 0; `/usr/bin/bwrap` present; host mutation forbidden) and the slot-budget mutant survives. Neither is a frozen-predicate leg.
- **Axis verdict: coverage improved** (claim verifies; ledger advanced; score held at cap per precedent — no number move).

**R92-C2 — calibration (held at 10) — NOT admitted under the frozen rule; evidence-verified + edit history re-measured.**
- Re-measured: the instrument was edited after freeze A and after its first scored run — `git diff --stat 96f249e0 1df76536 -- plans/` lists exactly the 10 files the report names, including `round91_counter_pin.py` (114 ±), `round92_burndown.py`, `round92_c2_conformance.py`; `git log` shows E `6a51ff0e` … E7 `dd48027f` after the first scored tips. The freeze-breach is real.
- Re-measured: at HEAD the M9 literal is gone — `git grep -n 'skip-selftest' 1df76536 -- plans/round91_counter_pin.py` → no match (`c2-head.txt`: `M9-SELFTEST-ESCAPE pass … tip-flag-absent=True`).
- Evidence-verified: `L1/c2-tip-final3.txt` (M7/M12/M9 pass) and `L1a2/c2-head.txt` (`PREDICATE R92-C2 pass`, rc 0) match the report. The amended instrument passes; the frozen-rule verdict (not admitted) is the honest reading, and the SCORECARD erratum (commit `bb29a660`) states it.
- **Axis verdict: calibration unchanged** (no verifiable move; no harm; score held at 10).

**R92-C3 — operability (held at 10) + capability `routed-findings freeze gate v3` — NOT admitted; evidence-verified + absence sweeps re-measured.**
- Re-measured absence: at HEAD the gate's override branch (`plans/round92_burndown.py:306-329`) never calls `vacuous_check` — it checks `override-unjustified`/`override-unanchored` and runs both commands, while only the non-override `else` branch applies `vacuous_check`. Critic G4 / sentinel H1 / M9(lesson) / M10(b)(frozen rule) confirmed against the bytes.
- Re-measured absence: `plans/counter-pins-r91.json` at HEAD names only `plans/round92_bs_probe.py` among round-92 files — the three counters are unpinned (sentinel H4 / M11).
- Evidence-verified: `L1/c3-base.txt` (`freeze=refused`, `DEFECT check-failed R82-V8`, `PREDICATE R92-C3 fail`), `L1/c3-tip.txt` and `L1a2/c3-head.txt` (`freeze=admitted oldest_pending_round=- pending=0 parked=24 … checks_run=124`, `PREDICATE R92-C3 pass`, rc 0); the selftest battery reports `cases=10 red-green-ok=10` in the committed receipts (evidence-verified, not re-run).
- The capability row did **not** enter SCORECARD this round (correct per AXES.md — the demonstration is not admitted), so nothing is minted here.
- **Axis verdict: operability unchanged** (repairs landed post-score; two open defects at HEAD; no harm).

**R92-F2 — companion (no claim slot) — verified; re-measured.**
- Re-measured: the three capture pins match the tracked bytes — `sha256sum` over `corpus/evidence/round81/log-summary-date-ranges-probe.txt` → `7c8d3f56…f81e78`, `corpus/evidence/round92/instructions/log-summary-date-ranges-instruction.md` → `c1d4516a…3484`, `corpus/evidence/round92/instructions/vulnerable-secret-instruction.md` → `d43c72e6…7a2f`; all equal the S287/S288/S289 `anchor` pins, and the quoted lines at `:1`, `:9`, `:1` carry the quotes verbatim.
- Evidence-verified: `L1/f2-base.txt` (`rows=274 captured=71`, three `PARSE-MISSING` DEFECTs, `PREDICATE R92-F2 fail`, rc 1); `L1/f2-tip.txt` (`CAPTURE-PINNED S287=1,S288=1,S289=1`, `ANCHORLINE rows=281 cited=91 captured=78 … live=0`, `PREDICATE R92-F2 pass`) — captured=78 confirms the critic's F-1 correction of the claim text's "71 + 3 = 74".

**Census — re-run by this integrator:** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, exit 0, 281 rows (W04 duplicate-url warnings are pre-existing warnings, not errors). `L1a2/census-end.txt` at `1df76536` matches. Registry 274 → 281 as reported.

**SCORECARD harm sweep:** `git diff 4ba56182 1df76536 -- SCORECARD.md` touches no axis-score row; all seven scores held (novelty 8, calibration 10, depth 10, operability 10, freshness 10, adjacency 9, coverage 7). No owned axis harmed.

## 3. Per-axis verdicts (this closure)

| axis | verdict | basis |
|---|---|---|
| coverage | **improved** | C1 verifies on its frozen predicate; executed ledger 35→36 of 88 (re-measured); score held at L0 cap 7 |
| calibration | **unchanged** | C2 not admitted under the frozen rule (post-freeze instrument edits, re-measured); no harm |
| operability | **unchanged** | C3 not admitted (post-first-run repairs; override-vacuity and marker-skip open at HEAD, re-measured); no harm |
| depth | **unchanged** | no knowledge entry added or re-verified this round |
| freshness | **unchanged** | S283/S284/S286 re-fetched by the lane's scout at `2fd12b88` (evidence-verified); no freshness move claimed |
| adjacency | **unchanged** | connector absorbed nothing (report-only); no cross-domain bleed observed |
| novelty | **unchanged** | no novelty claim this round |

## 4. Discernment spot-check (LEARNING.md — from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S283 `tests/test_outputs.py` @ `2fd12b88` | admit (tier A) | fetched `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/llm-inference-batching-scheduler/tests/test_outputs.py` → HTTP 200, sha256 `80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa`, 14194 B — identical to the row | **agree** | sha and size match; `:91` is `def test_output_files_exist() -> None:`; `EXPECTED_INPUT_HASHES` at `:25`; six `def test_` functions — the teaches-cell is grounded; member-replay scope is honestly bounded |
| S286 `tests/test.sh` @ `2fd12b88` | reject | fetched same base `tests/test.sh` → HTTP 200, sha256 `005f980332355e2fe143d4ff4aac11828adf070594bbe7055399c238f06953ca` | **agree** | `:5` is `# Install curl`; lines 6–7 `apt-get … install -y curl`, line 10 `curl … uv install.sh \| sh`, line 20 `uvx` — a network wrapper, correctly refused by the offline-replay scope; kept as a rejection row with a flip |
| S287 supersedes S265 | admit (tier A, own-work) | `sha256sum corpus/evidence/round81/log-summary-date-ranges-probe.txt` → `7c8d3f5656edc2affbd594cc4c33c796e01dc51852d5b00100fc1a8455f81e78`; `:1` quote verbatim | **agree** | pin matches the row; 7-word quote corrects the round-91 word-count defect at `d1ccf56d`; supersede form follows CORPUS rule 2 |
| S288 / S289 supersedes | admit (tier A, own-work) | sha256 over both instruction captures; quotes at `:9` and `:1` verbatim (12 and 13 words) | **agree** | one capture per row is respected (the S285 scribe finding is correctly honored); pins byte-verified |
| census | — | re-run CLI (above) | **agree** | exit 0, 281 rows at HEAD |

All four sampled decisions reproduce; no disagreement. The gate's rejects (S286) and admits (S283, S287–S289) match an outside re-open.

## 5. Trend verdicts (this closure)

- **expansion: improved** — executed ledger 35→36 of 88 (re-measured from the committed ledger); six admitted registry rows (S283–S285 member/dataset, S287–S289 own-work supersede pins), one rejection kept (S286); census exit 0 at both ends (274→281). No knowledge entry added — the expansion rides the member-ledger ground the coverage map already tracks, consistent with the round-88 precedent.
- **quality: unchanged** — no admitted entry added, re-verified or superseded. The counter repairs landed, but three instrument gaps are open at HEAD (override vacuity, planted-marker battery skip, unpinned counters — each re-measured above), so no quality credit is taken.
- **discernment: harmed** — attempt 1 filed C2 and C3 as "met as frozen" while their instruments had been edited after freeze A and after the first scored run (edit history re-measured above). The lane's own non-author wave contradicted both verdicts (critic P1/G4, reviewer F-1/F-5, sentinel H1/H3/H4), and the lane corrected them by SCORECARD erratum (`bb29a660`) with lessons M8–M13. The correction is real but the filed verdicts were wrong: harmed, scoped to this round, operator may rule otherwise (L0 `kengaku | round-92`).

## 6. Routed defects the lane must fix next round (round 93)

1. **Freeze-hash check with a red-before witness (M8):** no gate compares the counter bytes to freeze A's table; route with a fixture that must go red.
2. **Override-branch vacuity (frozen M10(b); critic G4; sentinel H1):** `plans/round92_burndown.py:306-329` never applies `vacuous_check` to an override command.
3. **Planted-marker battery skip (M10; sentinel H3; mutation-tester):** `.predicate-selftest-child` marker skips the battery (`:445`, `:558`).
4. **Pin the three round-92 counters (M11; sentinel H4):** `plans/counter-pins-r91.json` carries only `round92_bs_probe.py`.
5. **`sandbox-red` control must be injectable (M13):** absolute `/usr/bin/bwrap` path cannot go red on this host.
6. **Unguarded sibling `cost_model_for_tests.py` (ScoutS283 F1):** executed by the grader, gated by no instrument; comment/semantic mutations stay green.
7. **WAVE-DONE addressing after a relaunch (L0 line 365):** operator ruling; until then keep forwarding (as done here).

Honest limits carried: the C1 replay grades captured grader bytes on this host's toolchain (not the TB2 harness or a real submission); the H5 in-tree-pin residual stays open under L0 `kengaku | round-91`. Driver completion is not admission; the operator rules on L0 `kengaku | round-92`.

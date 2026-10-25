# r13-scribe — SHONEN assessment, report-contract and claim-boundary record

Advisory lane artifact. Author: `R13Scribe` (scribe seat, lane-dispatched L2).
Round label: 13 (re-dispatch, steered 2026-10-15). Baseline commit
`3f31e54c6e7aeddef13db11985b3c7a9dad9e0cf` (`git rev-parse HEAD` in the lane
repo returns the same value; the working tree is not clean — see §5).

**Scope of this file.** Assessment and bookkeeping only. It writes no final
report, no checklist row, no `SHONEN.md`/`SCORECARD.md`/`LOG.md` edit and no
commit. Every figure below is either an inherited measured artifact (cited) or
a read-only file fact produced in this session (`git ls-tree`, `git status`,
`grep`, `wc`, `sha256sum`). **No build, lint, test, formatter, gate run, or
endpoint probe was executed by this seat.** In particular the `grader.py`
733-check / S0–S7 result is quoted from inherited artifacts
(`corpus/lessons/round-16-recensus.md:8-10` verdict, `:19` "the admissible
baseline is the parent-run receipt above"; `SHONEN.md:10`), not re-run here.

## 1. Four SHONEN assessment lines (one per box, evidence-pinned)

Box lines are `SHONEN.md:5`, `:7`, `:9`, `:11` (continuation text `:6`, `:8`,
`:10`, `:12`); file is 12 lines, sha256-identical to the baseline blob
`git rev-parse 3f31e54:SHONEN.md` → `bd0ba20c8a7285f43c940928cb0edbdb1e4cafb3`.
Statuses below are the assessment this seat would file; **this seat issues no
`[x]`** — per `PROTOCOL.md:63-71` a lane's own assessment is `[~]` and only a
non-author may write `[x]`.

1. `[~]` **SKILL.md decision tables / error patterns / checklists / cited
   sources** — author-asserted counts (`SHONEN.md:6`: 2 decision tables, 19
   anti-patterns, 13 measurement rules, 9-step checklist, 23 cited-source
   bullets, SKILL.md 578 lines) with the round-14 citation re-fetch named
   (`r14-review-priorart.md`; 14 URLs). Asserted-by-author, not re-counted or
   re-fetched by this seat; no non-author re-count exists in this batch.
2. `[~]` **At least one end-to-end domain task executed and logged in LOG.md** —
   `SHONEN.md:8` names the rounds 4–14 chain and the r12/r13 late-landing
   breach. The r13-and-earlier rounds it rests on are logged
   (`LOG.md:20` round 13 "evidence committed in round 14", `LOG.md:21` round 14
   landing). Evidence pointer resolvable; the assertion itself is author-side.
3. `[x]` **Instructions executable by an agent without oral context** — the
   current `[x]` names a **non-author** verifier: `SHONEN.md:10` →
   "the aggregator's non-author cold run
   (`corpus/lessons/round-8-aggregator-box3-coldrun.md`, commits `06cdc98` +
   `d8f2898`)". That artifact declares its own provenance at
   `round-8-aggregator-box3-coldrun.md:1-2`: "verifier: aggregator-lane round-8
   L2 `labrat` seat Box3Kengaku — **non-author**; author lane: kengaku;
   dispatched by `.ufo/reports/round-8/aggregator.md`". Re-execution at the
   later landed revision is recorded in
   `corpus/lessons/round-9-aggregator-corpus-verdict.md` (`CHECKS n=280
   mismatches=0`, S0–S6, "Firm, not broken"). **Inherited, not renewed:** the
   `SHONEN.md:10` addendum "the hermetic gate now replays four trees
   (`python3 grader.py` → 733 checks)" is a parent/lane-run measurement
   (`round-16-recensus.md:8-10`); an author-side or lane-dispatched run cannot
   support or renew `[x]`, so box 3 stands only on the round-8/round-9
   aggregator artifacts. Caveat to the canonical reviewer, reported not
   resolved: `round-9-aggregator-corpus-verdict.md:5` itself says "the
   aggregator-dispatched reviewer is still lane-authored, not non-author
   evidence" — whether that qualifier reaches the round-8 `labrat` cold run is
   a judgment for the promotion gate, not for this seat.
4. `[~]` **No cross-domain bleed (PROVINCE.md still accurate)** — `SHONEN.md:12`
   asserts round-14 re-verification and lists the benchmark tree as "relocated
   intact to `~/archive/bench-arena`". That present-tense claim is already named
   as stale/unmarked debt by the round-16 audit
   (`round-16-recensus.md:34` counts `SHONEN.md:12` among 61 live citations to
   deleted paths; `:38` names `PROVINCE.md:13-14`). §5 of this file records the
   conflict verbatim. `[~]`, not `[x]`.

## 2. Prior non-author verifier vs this batch's lane-dispatched agents

- **Non-author, admissible role:** the aggregator/integrator lane. Box 3's `[x]`
  rests on it (round-8 `labrat` cold run; round-9 aggregator verdict). Under
  `PROTOCOL.md:63-65` a promotion box is checked "by a reviewer who did not
  author the round's changes — a fresh lane or integrator review, never
  self-attestation; **a subagent the lane dispatched is still the lane**."
- **Lane-dispatched, NOT outside review:** all nine seats of this batch —
  `R13Planner`, `R13Connector`, `R13LivingSources`, `R13KnowledgeSources`,
  `R13CoverageCensus`, `R13Scribe`, `R13SurfaceScout`, `R13Reviewer`,
  `R13Critic` (roster in `dispatch.json:7-17`, `routing_authority` at `:18`).
  `dispatch.json:20` states it directly: "All seats are lane-dispatched advisory
  L2s, not an outside non-author learning/promotion verifier. Spawn success is
  not evidence of completed work."
- **Consequence:** no box moves to `[x]` on this batch's evidence, no existing
  `[x]` is renewed by it, and no learning/coverage trend may be scored
  `improved` on it. This matches the inherited lesson
  `corpus/lessons/round-13-coverage.md` ("Spot-check: no outside non-author
  learning-gate review was performed in this continuation … they are advisory
  lane evidence, not an external admit/reject spot-check or a promotion
  authority").

## 3. Report append-only check and the required final report sections

**The filed fleet report is the old plan and must be answered, not rewritten.**
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-13/kengaku.md` — 25 lines,
4220 bytes, `sha256
a0f01968278c61ade8640f37278dec6e6f96b283fec4bf51f6d752c320331ab4`, committed
and clean under `git status --porcelain .ufo/reports/round-13/` (last commit
touching it: `17c1fad` "fleet relaunch … repo moved to ~/Projects/shokunin").
Its only structure is `:1` title, `:3-4` axis block, `:6` "Data walk", `:15`
"WWKD plan", `:25` "Out of scope" — it is the **ack-state plan**, filed as a
report, with no landed work.

Required sections (prompt `.ufo/prompts/kengaku-round-13.md` §4, mirroring the
report gate at `PROTOCOL.md:176-190` and the report contract at `:220`):
**Work performed → Landed changes → Before → after
measurements → SHONEN**, in that order, each work item carrying an evidence
pointer and a checkable commit hash.

Contract status of the filed report, plainly:

- all four required sections **absent** (`grep -n '^#'` on the file returns only
  the title/Data walk/WWKD headings);
- zero commit-hash citations: `grep -nE '\b[0-9a-f]{7,40}\b'` on the file
  returns **no** output;
- therefore it is at minimum an `ok`-plus-minimum-content-defect candidate, and
  per `PROTOCOL.md:188-190` a contract violation inside a real report is a
  **status-neutral defect recorded by the integrator**; per `PROTOCOL.md:150-151`
  "the assessment (reports are filed once; the assessment is not) must be
  re-filed under the heading in the next round's report."

**Append-only rule (checked, not violated by this seat).** Precedent
`corpus/evidence/round12-fleet/r12-doc-deltas-final.md:227` and
`SCORECARD.md:221`: a stale figure in a committed report is answered by an
appended erratum that *names* the report site; "append-only discipline forbids
rewriting a committed report". Direction for the parent, not performed here:
the round-13 continuation erratum must be appended to the filed file (or to the
next report) and must **not** modify the 4220 bytes above; the historical
ack-audit outcome already lives in `LOG.md:20` and `LOG.md:21` and in
`corpus/lessons/round-13.md`, so the plan-only file can keep its bytes intact.

Parent's landing plan, as relayed by peer `R13Critic` (**peer-reported, not
independently verified by this seat**): a two-commit split (baseline artifacts
first, after-result second) so measurement citations are not circular; the
after-result and the final report remain parent-owned. This seat neither
executed nor checked it.

## 4. Round-number mismatch against the later-16 records (reported, not resolved)

- Steered label is **round 13** (`.ufo/prompts/kengaku-round-13.md`; §4 names the
  path `.ufo/reports/round-13/kengaku.md`). The file's content is unchanged
  versus `HEAD` (`git status --porcelain` on the prompt is clean), i.e. the
  re-dispatch reuses the existing round-13 prompt rather than minting a new
  round number.
- The artifacts of this continuation **postdate round-14, round-15 and
  round-16 records**: `surface-receipt.json:2,5` carry `"round": 13` and
  `observed_at 2026-10-15T04:49:50.049812+00:00`; `MANIFEST.json`'s latest closure row
  records kengaku at `lane_rounds: {kengaku: 16}` with `closed_at
  2026-10-15T00:23:52.103882+00:00`; the round-16 records are dated 2026-10-14
  (`LOG.md` §16, `.ufo/reports/round-16/kengaku.md`, mtime 2026-10-14 21:21).
  So a round-13-labeled tree lands after round-16 files.
- `PROTOCOL.md:86` ("Round numbers are monotonic; a lane must not claim a
  round other than the steered one … several entries for one steered round are
  allowed") makes the steer legal; the mismatch is chronological, not a
  counterfeit round. The inherited lesson says the same in its own words
  (`corpus/lessons/round-13-coverage.md`: "This continuation does not renumber
  or replace the earlier round-13 ack-state work or the later round-14–16
  records."). Recorded so the integrator's closure entry can name the
  lane-round it describes (`PROTOCOL.md:283`, `lane_rounds` map).
- Secondary bookkeeping drift: `.ufo/waves/round-13/` still holds only the
  *older* wave's files (`round13-entries.json`, `scribe-measurements.md`, …);
  this continuation's batch roster lives in the lane repo at
  `corpus/evidence/round13-coverage/dispatch.json`, not in
  `.ufo/waves/round-13/`. Nothing was moved; reported only.

## 5. Claim / data boundaries (what the inherited evidence does and does not say)

- **Retained digest ≠ original source bytes.** `surface-receipt.json:74-78`:
  "Path existence is not original-byte recovery, model identity, or
  capability"; "Public URLs were not re-fetched"; "Historical model/host
  observations remain historical; no service was restored." Any corpus
  annotation may therefore cite a historical path, never a restored source.
- **Population is the twelve fixed candidates, not the round-16 sweep.**
  `baseline-initial.json:9-11` fixes `source_candidates: 12`, `unmarked: 12`
  over `corpus/knowledge/*` at `3f31e54`; its `limits` field states this is "not
  a remeasurement of the round-16 audit's broader 61-live-citation population"
  (`round-16-recensus.md:34`: 61 live / 14 labelled / 294 marked-historical / 0
  unclassified, 369 token-hits). 12 ≠ 61 ≠ 17 knowledge source lines — the three
  counts are different instruments and must not be summed or set-equal'd.
- **Index census is bounded and two-sided.** `surface-receipt.json:60-73`
  baseline: knowledge 23 files / 23 indexed; lessons 18 files / 17 indexed with
  `corpus/lessons/round-16-recensus.md` unindexed. Verified independently as a
  file fact: `git ls-tree -r --name-only 3f31e54 -- corpus/knowledge | wc -l` →
  `23`; the same over `corpus/lessons` → `18` (including
  `round-16-recensus.md`). **Mine is a working-tree count, not a committed
  one:** `M corpus/README.md` + `?? corpus/evidence/round13-coverage/` +
  `?? corpus/lessons/round-13-coverage.md` (parent-owned README and lesson,
  uncommitted) give 23 knowledge rows/23 files, 19 lesson rows/19 files, 11
  evidence rows/11 dirs, and no unindexed lesson file. The baseline/after
  pair is only meaningful once the parent commits; label the revision with
  every number.
- **Cap holds.** Coverage is the falsifiable tie choice at legacy anchor 7 with
  the declared-but-unresolvable-surface cap firing (`SCORECARD.md:144`,
  `:161`, rubric row `:243`; route telemetry absent per `PROVINCE.md:15` and
  the endpoint absent per `surface-receipt.json:41-44`). Nothing in this batch
  restores a source or lifts the cap; no score increase is claimed or earned.
- **Conflict reported verbatim (not adjudicated here).** `SCORECARD.md:217-219`
  (round-15 host sweep, capture time 2026-10-14) reads "`~/archive/bench-arena` —
  resolves; `~/Projects/webzites/repos/llm-wiki` — resolves". `round-16-recensus.md:23-25`
  reads "`~/Projects/webzites/repos/llm-wiki` (SSOT) absent; `~/archive/
  bench-arena` and `~/bench-arena` absent"; `surface-receipt.json:7-40` records
  both paths `exists: false` on 2026-10-15. **Scope of the disagreement, stated
  precisely:** the 2026-10-15 receipt is a *present-tense* negative measurement;
  it does **not** by itself prove the round-15 capture-time sentence was false —
  `round-16-recensus.md:29-30` already rules the round-15 "resolves" sentences
  transcript-less with "historical accuracy unresolved, current truth negative.
  Do not re-pin." So the record is: **capture-time accuracy unresolved, current
  truth negative.** The round-16 audit also flags `SCORECARD.md:217-219` and
  `PROVINCE.md:13-14` as unmarked present-tense claims
  (`round-16-recensus.md:38`), and `SHONEN.md:12` carries the same
  archive-relocation phrasing. Direction for the parent: preserve
  `SCORECARD.md:217-219` as historical text and append a **clearly scoped
  current-availability erratum** (do not silently rewrite the line, do not
  renumber the round). Per this seat's role the disagreement is relayed as-is
  for the canonical judge; no rerun was performed.

## 6. Outside-reviewer prerequisites (what this lane cannot self-supply)

1. **Promotion gate** (`PROTOCOL.md:63-71`): every `SHONEN.md` box marked `[x]`
   needs a named verifier who did not author the round's changes; a
   lane-dispatched subagent is still the lane, so this batch can never satisfy
   it, and box 3's existing `[x]` can only be *renewed* by a fresh lane or the
   integrator/operator. Minimum bar: box 1 needs one `SKILL.md` decision table,
   an error-pattern list and a checklist each citing a resolvable source; box 2
   an end-to-end task executed and logged; box 3 executable-without-oral-context
   instructions with resolvable pointers; box 4 no cross-domain bleed with an
   accurate `PROVINCE.md`.
2. **Discernment spot-check** (`LEARNING.md` §"Discernment is checked from
   outside"): a non-author — fresh reviewer or the operator, never a subagent
   the lane dispatched — samples at least one admit and one reject from this
   round's gate decisions and records `agree`/`disagree` with a reason in the
   round's lesson. Absent as of this seat's run.
3. **Integrator step-1 verification** (`PROTOCOL.md:214-222`): cited child-repo
   commits exist and are ancestors of lane `HEAD`; no uncommitted round work
   left; the report carries the `SHONEN` heading; the dispatcher prompt carried
   the full embedded contract. The round's report-contract violations in §3 are
   the integrator's to record.
4. **Not performed and not claimable here:** source restoration, fresh URL
   verification, model/service health, promotion, or any score movement.

## 7. Hand-off pointers

- Filed report to preserve byte-for-byte: `.ufo/reports/round-13/kengaku.md`
  (`sha256 a0f01968…31ab4`) — append erratum, never rewrite.
- Inherited measured inputs: `surface-receipt.json` (`c3372d80…680f`),
  `baseline-initial.json` (`13f2b1ae…3f3b`), `dispatch.json`
  (`655d44e2…1818`), `corpus/lessons/round-13-coverage.md` (`29f46b62…82b0`).
- Lane artifacts cited: `SHONEN.md` (baseline blob `bd0ba20c…`), `SCORECARD.md`
  (`2e6f610e…`), `LOG.md` (`8bf51633…`), `corpus/README.md` (baseline
  `16512924…`, working tree modified — parent-owned).
- Verifier-facing conclusions: three `[~]` boxes plus one inherited `[x]`
  (box 3, non-author-sourced, unchanged by this batch); report-contract defect
  on the filed plan; round-label chronology mismatch; 12-candidate census ≠
  61-live-citation audit ≠ 17 knowledge source lines; one path-availability
  conflict (capture-time unresolved, currently negative); no score, promotion,
  restoration or outside-review claim.
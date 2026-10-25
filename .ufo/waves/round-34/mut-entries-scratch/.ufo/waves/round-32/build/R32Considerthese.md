# R32 Considerthese — read of the lane's considerthese inputs (2026-10-25)

Scout `L1Kengaku32.R32Considerthese`. Read all 7 files in
`considerthese/` (2026-10-19 … 2026-10-25), the frozen claims
(`plans/round-32-claims.md`), `corpus/QUALITY.md` (Q1–Q21, R1–R15), `SKILL.md`
(§Gate/probe registry), `corpus/README.md`, lessons round-29/30/31, and probed
for the proposal footprints (files, greps, presence checks). No sources were
opened; no edits made outside this report.

VERDICT: considerthese-read

## (a) Which proposal round 32's C3 grounds

C3 grounds **proposal 2 of `considerthese/2026-10-24.md`, second half** (the
catalog refresh). The claims file states it directly (round-32-claims.md line
92): "This is the second half of `considerthese/2026-10-24.md` proposal 2
("a first cheap refresh of the two public catalogs with a schema diff against
the 09-28 description"); Q21 already landed the cheap half in round 31."

Exact proposal text, `considerthese/2026-10-24.md` (date 2026-10-24, lines
27–35):

> 2. **Put an as-of date and a live/dead status on every knowledge entry, then re-probe the live ones.** `corpus/README.md`
>    lists most primary sources as "Historical-unavailable" (wiki, Bailian, bench-arena, ledger), and the one entry
>    built on live public APIs, `knowledge/open-model-catalogs.md` (HF `api/models`, OpenRouter `api/v1/models`), was
>    probed 2026-09-28, 26 days ago. Nothing in `corpus/knowledge/` (37 entries) says when a claim was last true or when
>    it should be rechecked. For a model-evaluation lane, catalog fields, model lists and benchmark versions drift on a
>    weekly scale. Proposal: front-matter `as_of`, `source_status` (live/historical/dead) and `revalidate_by` per entry,
>    a check that fails when a live-source entry passes its date, and a first cheap refresh of the two public catalogs
>    with a schema diff against the 09-28 description. That is a freshness and coverage gain that doesn't need any
>    decision from João.

The second-half clause C3 grounds is the final one: **"a first cheap refresh
of the two public catalogs with a schema diff against the 09-28 description."**
Consistency check: Q21 (round 31) is documented as the *cheap half* only —
its Limits paragraph says it "does not add an `as_of` field, does not classify
a source live/historical/dead, and cannot tell whether a *live* source's claim
is still true" (`corpus/QUALITY.md` Q21), which is exactly the gap C3's
re-probe + schema-delta receipt fills. Registry rows S101/S102 (C3's citations)
do not exist yet in `corpus/SOURCES.md` (grep for S101/S102: 0 hits) — they are
to be opened by C3 this round.

## (b) Status of the other proposals (one line each)

Proposals are listed by file date; status is grounded in current repo state.

**2026-10-19**
1. Bidirectional index gate in `grader.py` (corpus/README.md ↔ disk) — **open**: no `check_corpus_index`/index check in `grader.py` (grep 0); index parity is only enforced by per-round census scripts and `state_check.py` (R12), not a standing grader gate.
2. TTL + quarantine rule for unadmitted WIP (`wip/` prefix, grader refusal to cite it, N-session expiry) — **partial**: a quarantine mechanic exists at assimilation level (per-round `.ufo/waves/round-{30,31}/assimilation/quarantine-slice`, absent-defect-register, CORPUS rule 4 "no row appended that no admitted entry cites"), but the `wip/`-prefix rule, the TTL and the grader-citation refusal are not in QUALITY/SKILL (grep `wip/`|`unadmitted`: 0).
3. SCORECARD self-consistency pass — **grounded**: R12 (`state_check.py --summary` re-derives SCORECARD capabilities/axis basis/SHONEN/PROVINCE/index) mechanizes it; the stale "Planned" section problem has not recurred since r24.
4. Per-trial ground-truth predicate field (`gt_predicate: header_only|header_and_body`) — **open**: no `gt_predicate` field in the attribution receipts (grep 0); the r23 lesson records the predicate distinction but the receipts never carried it as a field.

**2026-10-20**
1. Make R1–R10 executable + mutation-test the census — **partial**: Q20 (out-of-band gate run on gate-touching landings) and per-round defect counters (`round30/31/32_defects.py`) execute subsets, but no standing `close_check.py` runs R1–R10 verbatim (glob 0).
2. Mechanize Q3/Q10 with archived source text + quote locator — **partial**: superseded in effect by Q10/Q13/Q14 second-seat rules and `sources_adopt.py` quote mode (rounds 29–31, ≤25-word located byte-substring spans); the proposed `quote_locate.py` tool itself is absent (glob 0).
3. Stop-loss on opencode-go + coverage-cap petition — **partial**: R9 pre-flight landed (and opencode-go was effectively stopped after r23 FAIL), but no formal `unreachable-via-current-routes` record/flip condition exists; the L0 cap petition is still open (see 10-25 #3).
4. Self-verdict vs outside-verdict agreement ledger (`verdict-agreement.tsv`) — **open**: file absent; non-author spot-checks run (r25 `f11bffbf`, r29–r31) but there is no running agreement metric with an interval.

**2026-10-21**
1. Re-score history under a hardened extractor — **grounded**: r27 `plans/parser_policy_compare.py` (15712 paired verdicts, 1089 events) + `knowledge/extraction-policy-comparison.md`; only the "stored historical flips written back into past rounds" tail remains undone (r27 lesson).
2. Prior-art preflight as a pre-registration gate — **open**: no `plans/round-*-claims.md` contains a preflight block (grep `preflight` in plans: 0); no Q-row; R9 is coverage target-leg preflight, a different thing.
3. Seat-yield ledger and wave budget — **grounded**: Q19 landed (proposal cited in Q19 text), `.ufo/waves/yield.tsv` exists with round-30 rows, zero-yield families merge/cut.
4. Blind forecasters — **open**: forecasts remain "source-informed, not calibration trials, no calibration credit" (10-25 reflection; r29 F1–F5, F3 unscorable); no hash-pinned forecaster seat artifact.

**2026-10-22**
1. Scratch as untracked content-addressed cache + carrier-aware pre-landing scan — **open as written**: `.gitignore` does not exclude scratch (only `interactive-sessions/` and `__pycache__/`); no archive-opening scan script/fixtures. The r29 credential event produced only the lesson `round-29-source-copy-containment.md`; wave context now caps scratch at 60 MB.
2. WebArena evaluator-error measurement (false-pass/false-fail per stratum, CP95) — **open**: only static audits exist (`benchmark_spec_audit.py` r28, `config_projection.py` r29), both explicitly "not task validity, model ability"; no evaluator-logic reimplementation measurement.
3. Resumable waves (seat journal + `resume_wave`) — **open**: no journal/resume tool; dead seats are recorded but never redispatched under a budget (r27 19+21 unreplaced; r29 23/64; r31 "dead seats: none" but no resume mechanism).

**2026-10-23**
1. Cap non-author closure debt (block pre-registration while >1 round lacks non-author verdict; `closure lag (rounds)` field) — **partial**: practice caught up — non-author verifier spot-checks exist for r29/r30/r31 (r31's is still pending per the r31 lesson), but the blocking rule and the SCORECARD closure-lag field are absent (grep `closure lag`: 0).
2. Audit gate yield (replay every Q-gate against each round's landing commit, red/green table) — **open**: no replay table/tool; Q19/Q20 record seat yield and gate-run receipts, not per-gate red/green across rounds.
3. Machine-readable root `STATUS.json` — **open**: file absent.

**2026-10-24**
1. Run the gates on every push (.github Actions workflow) — **partial**: landed as criterion Q20 (mechanical out-of-band gate-run receipt on gate-touching landings), but the GitHub Actions workflow itself is unimplemented (`.github/` absent; Q20 records the proposal and the absence check).
2. as_of/source_status/revalidate_by front-matter + live re-probe — **partial**: Q21 landed the cheap half (pinned `recheck:` naming) in r31; the front-matter schema and the staleness check have not landed; the second half is exactly what C3 grounds this round (see (a)).
3. Measure whether the corpus answers the questions it exists for (demand-side) — **open**: all coverage numbers remain supply-side; no frozen 30–40-question set or per-question grading exists.

**2026-10-25**
1. Model-diverse verification — **open**: all 18 role routes still go to `@m_flash`; no second-model discernment run on a fixed seeded sample.
2. One persistent routed-defect ledger (`corpus/defects.jsonl`) — **open**: file absent; rounds keep adding new `roundNN_defects.py` counters (r30/r31/r32), exactly the pattern the proposal argues against.
3. Decision packet for the round-25 L0 coverage cap — **open**: the L0 question is still open (claims cite SCORECARD ~line 782; 10-25 reflection records three rounds of "7 → 7 held" while the cap question is unanswered).

## (c) Proposals that could be reflected in QUALITY.md or SKILL.md but are not yet

1. **2026-10-24 #2, leftover half — `as_of` / `source_status` / `revalidate_by` front-matter plus a failing staleness check for live sources.** This is a quality bar for every knowledge entry and belongs in the QUALITY Q-block. Q21 explicitly carves it out ("does not add an `as_of` field, does not classify a source live/historical/dead, and cannot tell whether a *live* source's claim is still true"). Reason it has not landed: Q21 was deliberately scoped to the pin-naming half, and the schema would touch all 40 entries and require deciding which sources are live — the classification input that C3's catalog refresh (this round) is only now producing.
2. **2026-10-21 #2 — prior-art preflight as a Q-row.** The proposal itself says "A Q-row would make a missing or post-freeze preflight a closure failure"; no such Q-row exists (R9 covers a different, target-leg forcing preflight). Reason: rounds 25–31 consistently spent the lowest axis on coverage/calibration, so no round converted this novelty-axis mechanic into a closure criterion; it also needs a dated, committed search log before the freeze, a sequencing only a round-level change can set.
3. **2026-10-22 #1 — carrier-aware pre-landing scan (fail-closed, red/green fixtures).** A hygiene gate with fixture-driven failure belongs next to Q20 in QUALITY or as a row in the SKILL.md §Gate/probe registry; it is in neither. Reason: the r29 credential near-miss ended at "bounded current-tree removal without historical purge" (an operator hold; lesson `round-29-source-copy-containment.md`), and no later landing touched a hygiene surface again, so no incident drove a rule into the bar.
4. **2026-10-25 #2 — persistent routed-defect ledger.** A single persistent checker (re-running closed defects at tip, recurrence blocking, tip-receipt validator) fits the SKILL.md §Gate/probe registry and would replace the per-round counters; it is absent, and round 32's C2 freeze re-uses a new `round32_defects.py`. Reason: it is a cross-round meta-process needing a committed schema and a tip-receipt validator, while rounds have continued to freeze individual counters; D2's recurrence (r30 → r31) has not yet forced the consolidation.

## Evidence notes

- Sources read: `considerthese/2026-10-{19..25}.md` (all 7), `plans/round-32-claims.md`, `corpus/QUALITY.md`, `SKILL.md`, `corpus/README.md`, `corpus/lessons/round-31.md`, `corpus/lessons/round-30.md`, `corpus/lessons/round-29-source-copy-containment.md` (indexed), `.gitignore`.
- Presence probes: `grader.py` (no index-gate fn), `plans/quote_locate.py` (absent), `plans/*preflight*` (absent), `plans/*resume*`/`plans/*evaluator*` (absent), `corpus/defects.jsonl` (absent), `corpus/evidence/verdict-agreement.tsv` (absent), root `STATUS.json` (absent), `.ufo/waves/yield.tsv` (present), `plans/catalog_probe.py` (present, C3 counter), `SCORECARD.md` (no "closure lag"), `corpus/SOURCES.md` (no S101/S102 yet), `corpus/evidence/attrib-r23-stream-trials.log` (no `gt_predicate`).
- No tool installs/updates were needed; nothing was changed outside this report.

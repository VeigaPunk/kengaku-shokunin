# Round-14 revenger — reconstructing round-13 completion state

Scope: map the round-13 report's WWKD plan to what exists on disk, independently
re-derive the stored claims of the two committed scripts under
`corpus/evidence/round13-ack-state/`, draft the lessons entry, and list every
promised-but-unlanded deliverable so the scorecard can score honestly.

Everything below was re-run on 2026-09-29 inside
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. No network, no endpoint
traffic, no repo writes besides this file. The independent re-derivation used a
fresh stdlib script (own `extract_json_block`, own schedule math); it did not
import either round-13 script.

Inputs hashed (all four numbers quoted in the artifact body are re-observed
values, not copied):

```bash
$ sha256sum corpus/evidence/round9-replication/results-r9.jsonl \
            corpus/evidence/round11-power/results-r11.jsonl
c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb  results-r9.jsonl
918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad  results-r11.jsonl
```

`918bf7aa…` equals `EXPECTED_SHA256` hard-pinned in `analyze_ack_state.py:20`;
the analyzer refuses stale input itself. `c20158bd…` matches the digest column
printed by `audit_ack_schedule.py` for both r9 rows.

## 1. Completion map — WWKD plan step → artifact → landed?

Report under audit: `.ufo/reports/round-13/kengaku.md` (25 lines; **ends at
"Out of scope" — the report carries no results section**). Plan steps numbered
as in the report.

| Plan step (verbatim gist) | Artifact produced | Landed? | Evidence |
|---|---|---|---|
| 1. Skeleton: stdlib analyzer over `results-r11.jsonl`, join to `meta.truth`, schedule split {2,3,4,5,6,9} vs {1,8} | `corpus/evidence/round13-ack-state/analyze_ack_state.py` (md5 `9cbdc4665fb1fd760ccb2e2a3f31dded`) + `audit_ack_schedule.py` (md5 `494928b959a4b9c3cbbcf7dc5d7a1df5`) | **LANDED-uncommitted** (untracked in git: `git status --porcelain` → `?? corpus/evidence/round13-ack-state/`) | selftest + main exit 0, output below |
| 2. Overfit one real instance (pid 203 turn 8 negative control) | No standalone artifact; the exclusion is structural in `analyze_ack_state.py` (`intent_for_turn(8)` → control) | PARTIAL — logic landed, no per-instance note | my re-run: pid203 t8 raw parses and equals `truth[7]` (see claim 8) |
| 3. Measure: 384 = 64×6 ack-only rows, 4 categories + controls | Script stdout only; a structured run exists as `/tmp/kengaku-round13-final.json` (38,373 B; keys `cell_row_counts/checkpoints/controls/pids/primary_ack_only/schedule_derivation/witnesses`) | **ABSENT from repo** — no committed `analysis_r13.md`/JSON; the only durable copy is this re-run | re-run table below reproduces every number |
| 4. Price + boundary: prior-art scout; connector sibling check; route prompt-craft to kotoba | Scout wrote `/tmp/kengaku-round13-priorart.md` (13,208 B), `/tmp/kengaku-round13-prior-art-ack-fidelity.md` (11,606 B), `/tmp/…-venues.md` (4,412 B), fetched source `/tmp/r13-stageif.html` (725,653 B), raw arXiv API `/tmp/ack2.xml` (17,316 B; `ack1.xml` 0 B — empty response recorded). No connector artifact found anywhere. No kotoba route (`grep -i ack round-13/kotoba.md round-14/kotoba.md` → no kengaku referral) | **ABSENT** — prior-art verdict exists only in `/tmp`; connector produced **no file at all**; kotoba routing unevidenced | `find /tmp` + `ls corpus/evidence/` + sibling-report grep |
| 5. Verification gate: selftest + on-bytes asserts + novelty bump only if prior art supports | Selftests exist **inside** both scripts (`--selftest` flags, 4/4 and 8/8 PASS); on-bytes asserts at `analyze_ack_state.py:99-124,171` (64 meta, 512 rows, unique keys, category total = 384) all fire on every run. Scorecard never got an r13 row | PARTIAL — gate code landed and passes; the novelty-bump clause is moot because the prior-art verdict never landed and SCORECARD.md has no r13 row | `grep -n 'round-13\|round 13' SCORECARD.md` → 0 hits |
| Out-of-scope compliance | — | HONORED: zero repo writes outside `round13-ack-state/`; zero endpoint traffic (both scripts stdlib-only, offline) | file census + script source |

**R13 fleet leftovers in `/tmp` (context, not repo evidence — may not survive
reboot):** beyond the scout files, `/tmp/kengaku-round13-method.py` (20,810 B,
executor prototype, md5 `58bcefa8…` — a *different* implementation than the
committed analyzer), `/tmp/kengaku-round13-recompute.py` (20,461 B, independent
recompute), `-method.md`, `-recompute-report.md`, `run{,A,B,2}.json`
(278,391 B each), `summary.json`/`final.json` (38,373 B). So round 13 actually
ran a fuller fleet (executor + recompute + scout) whose outputs stayed in
scratch; only the two consolidated scripts reached the repo. Related
`/tmp/r13-{census,newrows}.tsv`, `r13-table.json` are protocol-lane obligation
scans, not kengaku [INFERENCE: content is PROTOCOL.md obligation grep rows;
mtime same window].

## 2. Independent re-derivations (≥6)

Reproduce everything below:

```bash
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 corpus/evidence/round13-ack-state/audit_ack_schedule.py --selftest   # SELFTEST: 4/4 PASS
python3 corpus/evidence/round13-ack-state/audit_ack_schedule.py              # exit 0
python3 corpus/evidence/round13-ack-state/analyze_ack_state.py --selftest    # SELFTEST: 8/8 PASS
python3 corpus/evidence/round13-ack-state/analyze_ack_state.py               # exit 0
```

Fresh-code re-derivation (my own parser + schedule math, full source kept in
the revenger transcript; rejects on any mismatch):

1. **Prompt schedule → `-ack` is a storage label, not prompt intent.**
   Command: read `run_r9.py:16,26-28` and `run_r11.py:61,76-80`. Observed
   (`run_r11.py:77-79`): the prompt for turn t is `"Reply 'ok'."` iff
   `t-1 ∉ checkpoints ∧ t ∉ checkpoints`; `"Output the FULL state…"` if
   `t-1` was a checkpoint (spillover); `"CHECKPOINT — output the FULL state
   now."` if `t` is a checkpoint. `run_r9.py:26-27` is the same code plus a
   dead `name=='A-INC'` clause (A-INC checkpoints every turn ⇒ the branch never
   logs `-ack`; census confirms `A-INC-ack` count = 0). Derived sets:
   CKPT4710 ⇒ true-ack {2,3,6,9}, controls {1,5,8}, logged {1,2,3,5,6,8,9};
   CKPT710 ⇒ true-ack {2,3,4,5,6,9}, controls {1,8}, logged {1,2,3,4,5,6,8,9}.
   Both equal `true_ack_turns()` and the script selftest expectations.
   **VERDICT: REPRODUCE.**

2. **Row census + denominators.** Command: `Counter(r['cell'] for r in rows)`.
   Observed r9: `A-CKPT4710-ack` 56, `A-CKPT710-ack` 64, meta 8 (pids 101–108),
   each meta with 10 ops + 10 truth. Observed r11: `A-CKPT4710-ack` 448,
   `A-CKPT710-ack` 512, meta 64 (pids 201–264), `descriptors` 1, `filler` 128,
   graded cells 192+128, total 1473 — matching `probe_plan_r11.md:59-64`.
   True-ack subsets: r9 32/56 and 48/64 (8 pids × 4 / 6 turns); r11 256/448
   and **384/512 = 64×6**. **VERDICT: REPRODUCE** (all four assignment
   denominators exact).

3. **80-char capture clip.** `run_r9.py:24` / `run_r11.py:74` store
   `r['content'][:80]`; `probe_plan_r11.md:32-35` documents it and
   `probe_plan_r11.md:60` declares `raw ≤80 chars` in the schema. Empirical:
   max stored raw length = 80 in all four cells; at-cap rows r9 15/56 +
   10/64, r11 124/448 + 101/512. (Scratch scout file cites `run_r11.py:78`
   for the clip — actual clip line is `:74`; `:76-80` is the ask block. Minor
   stale pointer in an unlanded artifact, noted, no repo impact.)
   **VERDICT: REPRODUCE.**

4. **Bare-ok headline: 84.4% on true ack-only turns (r11).**
   `sum(raw.strip().lower() == 'ok')` over true-ack rows: CKPT710 **324/384 =
   84.375% → 84.4%**; CKPT4710 coincidentally identical 216/256 = 84.375%.
   Prefix `startswith('ok')`: 330/384 and 220/256 (85.9%). Label-wide prefix
   (the historical proxy): 330/512 = 64.5% and 220/448 = 49.1% — the r11
   analysis/report denominators reproduced (`analysis_r11.md:30` claim,
   `.ufo/reports/round-11/kengaku.md:48` "220/448 = 49.1%"). r9 is 100% bare
   on all true-ack rows (32/32, 48/48). **VERDICT: REPRODUCE.**

5. **Exact-state emissions bounded [0.047, 0.125].** Fresh parse of each of
   the 384 r11 CKPT710 true-ack raws through a re-implemented
   fenced-then-brace-fallback extractor, compared `==` to `meta[pid]
   ['truth'][turn-1]`: **exact 18, nonexact 6, bare-ok 324, unresolved-cap 30,
   unresolved-other 6** (sum 384). Incidence bound: 18/384 = 0.0469 → 0.047,
   (18+30)/384 = 0.125. Brace-bearing raws 54/384 across 9/64 pids, and all
   9 brace-pids carry a brace on all six turns; parseable-exact share among
   brace raws [18/54, (18+30)/54] = [0.333, 0.889]; pids with ≥1 exact = 5/64.
   Every figure matches the analyzer's printed table verbatim.
   **VERDICT: REPRODUCE.**

6. **Label-wide startswith reproduction.** 330/512 (=64.5%) across all
   `-ack` rows including state-ask controls — the "old denominator" figure in
   `analyze_ack_state.py:198` prints identically under my scan.
   **VERDICT: REPRODUCE.**

7. **Schedule-label controls behave as controls.** Turn 1 (initial-state
   ask): 38/64 exact vs `truth[0]`, 23 unresolved-cap, 0 bare-ok. Turn 8
   (post-checkpoint spillover ask): 14/64 exact vs `truth[7]`, 23 nonexact,
   27 unresolved-cap, 0 bare-ok. Both rows are dominated by state-shaped
   replies — exactly the dissociation the audit claims between label and
   intent. **VERDICT: REPRODUCE.**

8. **Negative control pid 203 turn 8.** Stored raw =
   `` ```json\n{"nails": 6, "bolts": 27, "screws": 14, "hinges": 0,
   "brackets": 8}\n``` ``; parsed dict `== meta[203]['truth'][7]` (state
   after operation 8 = the post-`{7}` spillover state), `len(raw)=79 < 80`.
   The report's claim ("JSON matches truth after operation 8 … must be
   excluded from the ack-only denominator") checks out, and the analyzer does
   exclude it (intent `post-checkpoint-full-state`, not ack-only).
   **VERDICT: REPRODUCE.**

9. **Selftest coverage vs plan step 5.** Plan demanded selftests for plain
   ok, exact JSON, wrong/partial JSON, truncated raw, turn-8 exclusion, plus
   on-bytes asserts (unique join keys, 64 meta, 384 ack-only, category total
   = 384). Observed: `analyze` selftest covers all five classes (8/8 PASS),
   `audit` selftest covers the schedule derivation for both checkpoint sets
   (4/4 PASS), and runtime asserts at `analyze_ack_state.py:99-124,171-172`
   (census, key uniqueness, raw ≤80, 384 denominator) + `audit_ack_schedule.py
   :51-55,69-78` (meta census, 10 ops/10 truth, key set exact, raw ≤80) fire
   on every normal run — both mains exit 0 on committed bytes.
   **VERDICT: REPRODUCE / gate as specified exists.**

## 3. Draft — `corpus/lessons/round-13.md`

```markdown
# Lessons — round 13 (ack-label prompt-intent audit)

Source: `.ufo/reports/round-13/kengaku.md` (plan only); committed instrument
`corpus/evidence/round13-ack-state/{audit_ack_schedule.py,analyze_ack_state.py}`;
reconstruction + independent re-derivation `corpus/evidence/round14-fleet/
r14-revenger-r13.md`.

1. **A logged cell suffix is a storage label, not prompt intent.** `-ack` rows
   exist wherever the runner's logging `else` branch fires (every
   non-checkpoint turn), but two of those turns — the initial state (turn 1)
   and the post-checkpoint spillover (turn 8 for CKPT710; 5 and 8 for
   CKPT4710) — were *asked for* full states. Turn intent must be re-derived
   from the runner's ask-construction code (`run_r11.py:76-80`,
   `run_r9.py:26-28`), never from the cell name; r11's naive label-wide
   `startswith('ok')` counted 330/512 while the intent-aware denominator
   makes it 330/384 prefix / 324/384 bare.
2. **Denominators fall out of the schedule, not the file.** For checkpoint
   set C the true ack-only turns are `t ≥ 2, t ∉ C, t−1 ∉ C`; everything else
   logged under `-ack` is a schedule-label control. That is 384 = 64×6 for
   r11 CKPT710 and 256 = 64×4 for CKPT4710; controls {1,8} / {1,5,8}. Encode
   the schedule once (`true_ack_turns`) and assert the key census rather than
   re-listing turns.
3. **Cap-aware verdicts.** Ack raws are clipped at 80 chars (`run_r11.py:74`);
   an unparseable raw at the cap is UNRESOLVED, not a model error. Report
   bounded estimates — exact ack-only state emissions are [18,48]/384 =
   [0.047,0.125] — and keep a separate category for cap-hits (30/384) instead
   of folding them into either side.
4. **The model occasionally ignores the `ok` contract with a *correct*
   state.** 18/384 true-ack replies were unsolicited state snapshots exactly
   equal to simulator truth (54/384 brace-bearing, 9 pids, all of them
   brace-on-all-six-turns — a per-pid behavior, not sporadic); 6/384 were
   uncapped prose that resolved to neither `ok` nor JSON. An exact state is
   state-faithful but contract-violating: score fidelity and compliance as
   separate axes.
5. **Meta-lesson: a measurement that lands no durable analysis scores
   nothing.** Round 13's instruments ran and verified, but no analysis file,
   lesson, knowledge entry, LOG/SCORECARD row, or report results section was
   ever written — the measured numbers lived only in stdout and /tmp JSON.
   Any future "instrument-only" round must land its output table in-repo at
   minimum (this artifact is that landing, one round late).
```

## 4. Landing-gap list — promised but ABSENT

For scorecard honesty; "absent" = not in the repo and not reproducible from
committed bytes as of 2026-09-29.

| # | Promised (report §WWKD / §Out-of-scope) | Status | Where it survives |
|---|---|---|---|
| G1 | Prior-art pricing (step 4) | **ABSENT from repo** — `corpus/evidence/` holds no r13 prior-art file | `/tmp/kengaku-round13-priorart.md` + `-ack-fidelity.md` + `-venues.md` (scout verdict: NON-DUPLICATE at instrument level, medium confidence; needs re-commit or re-fetch) |
| G2 | Connector sibling-ownership check (step 4) | **ABSENT entirely** — no file in repo or `/tmp` | nowhere; must be re-run |
| G3 | Route prompt-craft implications to kotoba (step 4) | **UNEVIDENCED** — no `ack` referral in `round-13/kotoba.md` or `round-14/kotoba.md` | nowhere |
| G4 | `corpus/lessons/round-13.md` (round convention) | **ABSENT** — lessons jump round-11 → nothing; drafted §3 above | this file, §3 |
| G5 | Durable measurement output (step 3's numbers) | **ABSENT** — no `analysis_r13.md`/results file; report itself is plan-only (25 lines, ends at §Out-of-scope) | `/tmp/kengaku-round13-final.json`; reproducible by rerunning §2 commands |
| G6 | LOG.md / SCORECARD.md / corpus README r13 rows | **ABSENT** — `grep 'round-13\|round 13'` hits 0 in all three; SCORECARD still shows r11 post-move state (novelty 6) | n/a |
| G7 | Knowledge entry | **Not promised** by the report and absent — no gap to score | n/a |
| G8 | `round13-ack-state/` scripts themselves | **LANDED but uncommitted** (`??` in `git status`) — must ride the r14 commit | this round's commit |
| G9 | Selftest (step 5) | **LANDED** — inside both scripts, passes (4/4, 8/8); runtime census asserts fire on committed bytes | in-repo |
| G10 | Scratch-artifact citation defect | stale pointer: `/tmp/kengaku-round13-prior-art-ack-fidelity.md:8` cites `run_r11.py:78` for the 80-char clip; clip is `:74` | noted; fix if G1 is re-landed |

## Final assessment

Round 13's two committed scripts are correct and self-verifying: every stored
claim I re-derived from committed bytes (schedule mapping, all four
denominators, the 80-char cap, 84.4% bare-ok, [0.047,0.125] incidence bound,
the pid-203 control) reproduced exactly, and no falsification surfaced. The
round's failure is purely a landing failure — of five plan steps, only the
instrument code and its selftests reached the repo; the measured output, the
prior-art pricing, the connector check, the kotoba route, and every durable
ledger row are absent. Net round-13 state for the scorecard: **instrument
verified, axis-move claim unpriced and unrecorded.**

REVENGER VERDICT: **SCRIPTS REPRODUCE CLEAN; LANDING INCOMPLETE (G1–G6).**

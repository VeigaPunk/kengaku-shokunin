<!-- r12 doc-deltas DRAFT — authored by L2 scribe `ScribeDrafts` (role: scribe, wave 1).
     Task restated: the exact text blocks L1 pastes into corpus/README.md, PROVINCE.md,
     SHONEN.md and SCORECARD.md for round 12.
     L1: fill every `{{TOKEN}}` from YOUR OWN run output / the landed `analysis_r12.md` /
     the gate run, then paste block-by-block. Placeholder names are canonical and shared
     with `r12-report-draft.md` (§Placeholder registry = every resolution command) and
     `r12-log-draft.md`. Blocks are paste-ready markdown: nothing here is a measured value
     unless it is written without braces; a block marked **OPTIONAL** is L1's call.
     All four target files are L1-owned; this file is a proposal, never an edit. -->

# Round-12 doc deltas — four paste-ready blocks + one closing rationale

Scribe: `ScribeDrafts` (L2, wave 1). Target files, all L1-owned: `corpus/README.md`, `PROVINCE.md`, `SHONEN.md`, `SCORECARD.md` — plus two **OPTIONAL** blocks (`LOG.md` errata line, `SCORECARD.md` errata section) that record a defect this scribe found while drafting rather than silently repeating it.

Pre-round committed state measured 2026-09-28 at HEAD `f09ff1f` (real, no braces — re-derive with the commands shown if L1 wants a second reading):

| Quantity | Pre-round value | Command |
|---|---|---|
| knowledge rows / files | 22 / 22 | `grep -c '^\| \`knowledge/' corpus/README.md` = `ls corpus/knowledge \| wc -l` |
| lessons rows / files | 13 / 13 | `grep -c '^\| \`lessons/' corpus/README.md` = `ls corpus/lessons \| wc -l` |
| evidence dirs committed / indexed rows | 6 / 6 (`round12-ladder/` is untracked at draft time) | `git ls-tree -r f09ff1f --name-only -- corpus/evidence/ \| cut -d/ -f3 \| sort -u \| wc -l` = `grep -c '^\| \`evidence/' corpus/README.md` |
| `SKILL.md` | 518 lines, 15 anti-patterns, 23 cited-source bullets, 2 decision tables, 9-step checklist | `wc -l < SKILL.md`; `awk '/^## Benchmark anti-patterns/,/^## Research-note structure/' SKILL.md \| grep -cE '^[0-9]+\. '`; `awk '/^## Cited local sources/,0' SKILL.md \| grep -cE '^- '` |
| `PROVINCE.md` surface rows | 9 | `awk '/^## Surfaces/,/^## Refusals/' PROVINCE.md \| grep -c '^\|'` − 2 header lines |
| `grader.py` | 1711 lines, `CHECKS n=280 mismatches=0 errata_pinned=1`, exit 0, selftest S0–S6 (7 scenarios) `ALL PASS` exit 0 | `wc -l < grader.py`; `python3 grader.py`; `python3 grader.py --selftest` (all re-run 2026-09-28) |
| `LOG.md` | 18 lines; round-11 entry is line 18 | `wc -l < LOG.md` |

---

## 1. `corpus/README.md`

### 1a. `### \`evidence/\`` table — two new rows (append after the existing six)

```markdown
| `evidence/round12-ladder/` | preregistration bundle (`probe_plan_r12.md`, `power_analysis_r12.md`, `predictions-r12.md`, `prereg-bundle.sha256`, `ordering.log`, `prereg-precheck.log`), probe machinery + runners (`probe_r12.py`, `run_r12.py`, `predict_r12.py`), mock server + mock/smoke logs, run bytes (`results-r12.jsonl` md5 `{{RESULTS_MD5}}`, `run.log` md5 `{{RUNLOG_MD5}}`), generated `analysis_r12.md` (md5 `{{ANALYSIS_MD5}}`; census `{{CENSUS}}`), promoted `recompute_r12.py` |
| `evidence/round12-fleet/` | wave-1 L2 artifacts (design critic, 3 scouts, connector, reviewer-baseline, labrat mock, 2 executor drafts, the three scribe drafts), wave-2 artifacts (mutation battery, landed-number critic, landing reviewer), `INTEGRATOR-NOTES.md` — `{{FLEET_FILES}}` files; artifact filenames follow the round-11 convention (`r12-*.md`), roll-call in `INTEGRATOR-NOTES.md` |
```

(Count check after pasting: `grep -c '^\| \`evidence/' corpus/README.md` must equal `ls -d corpus/evidence/*/ | wc -l` → `{{EV_ROWS_AFTER}}` = `{{EV_ROWS_AFTER}}`.)

### 1b. Main table — new knowledge and lessons rows (append to the table, before the `evidence/` section)

```markdown
| `knowledge/bench-arena-round12-ladder.md` | Four-point emission-granularity ladder (Page ordered-trend) + batching dissociation + transport to a second task family + per-problem probabilistic forecasts: verdicts `{{VERDICT_R1}}` / `{{VERDICT_R2}}` / `{{VERDICT_R3}}` / `{{VERDICT_R4}}` / `{{VERDICT_R5}}`; Brier `{{E6_BRIER_POOLED}}` (N `{{E6_N}}`), BSS `{{E6_BSS}}`, calibration slope `{{E6_SLOPE}}`; E2 `{{E2_DIFF}}` vs r11's +0.352 | `corpus/evidence/round12-ladder/` (`{{RECORDS}}` records, bundle `prereg-bundle.sha256`, verdicts in `analysis_r12.md`), run 2026-09-28 |
| `lessons/round-12.md` | `{{LESSON_BULLETS}}` | LOG.md round 12, `corpus/evidence/round12-{ladder,fleet}/` |
```

`{{LESSON_BULLETS}}` is L1's to write from the round's own record. Candidate lessons the class of round-12 design makes *possible* (keep only those the run actually supports; a candidate that the run contradicts must be cut, not softened — round-9 lesson "pre-registered rules have three outcomes"):

- an ordered ladder claim needs an **ordered-trend statistic** on within-block ranks, not three separate adjacent contrasts (the contrasts cannot reject the ordering as a whole);
- a transport claim needs a **scale-invariance argument or a ratio-only report** — two task families graded on different severity metrics cannot be pooled;
- a **persistence predictor is not a cold forecast**: the C5 skill number is bounded by the fact that the predictor is fitted on the same problems, so BSS > 0 buys calibration evidence, not forecasting evidence;
- a dissociation contrast (`A-MONO − A-CKPT10`) that differs on two axes decomposes a confound but cannot itself name the mechanism;
- an underpowered branch must be reported as filed — `UNDERPOWERED-INDETERMINATE` is an outcome, not a failure to try harder.

### 1c. Coverage-map lines — replace the two stale bullets

```markdown
- **Multi-turn state tracking / planning horizon**: instrument built (r8, 3 probes), replicated on fresh seeds (r9), severity dose ESTABLISHED at preregistered power (r11, paired diff +0.352), then extended to a **four-point density ladder** at r12 — `{{VERDICT_R1}}` (E1 Page trend `{{E1_PAGE}}`), within-run replication `{{VERDICT_R2}}` (E2 `{{E2_DIFF}}`), batching dissociation r8's MONO collapse `{{VERDICT_R3}}` (E4 `{{E4_DIFF}}`), transport to a token-sequence family `{{VERDICT_R4}}` (E5 `{{E5_DIFF}}` on n `{{E5_N}}`), per-problem forecast skill `{{VERDICT_R5}}` (Brier `{{E6_BRIER_POOLED}}` over `{{E6_N}}` pass events, BSS `{{E6_BSS}}`) — `knowledge/bench-arena-round12-ladder.md`. Still open: probe B with a binding manipulation, probe C at n≥12, the r8 arithmetic covariate, and any second **served unit** (the ladder is single-stack by construction).
- **Novelty pricing**: r9 4/4 findings priced; r11 C1–C4 + M1–M3 priced with fetched URLs; r12 prices C1–C6 + method items — `{{C1_C6_VERDICTS}}`, `{{METHOD_ITEMS}}` (`evidence/round12-fleet/`; `knowledge/eval-prior-art-calibration.md`).
```

### 1d. Open-gaps lines — replace the three superseded entries

```markdown
- **Probabilistic forecasts**: CLOSED round 11 at the event level (3 predictions, Brier 0.153) and **CLOSED round 12 at the per-problem level** — `{{E6_N}}` pass events scored, pooled Brier `{{E6_BRIER_POOLED}}`, BSS vs arm climatology `{{E6_BSS}}`, calibration slope `{{E6_SLOPE}}` (the lane's own "prefer per-problem probabilities" preference is now satisfied; §`Planned` of round 11 clause (b)).
- **No in-repo gate**: CLOSED round 10; extended in-round at r11 (280 checks, three trees) and again at r12 (`{{GRADER_CHECKS}}` checks, four trees, selftest S0–S7) — `grader.py` replays all four committed probe trees offline, exit 0/1/2.
- **Prior-art digest queue**: STILL OPEN — Laban et al. ICLR 2026 (`arxiv.org/abs/2505.06120`), Lanham et al. (`2307.13702`), llama.cpp #7052 named in `knowledge/eval-prior-art-calibration.md` and still unread; carried unchanged and named as a coverage candidate in `SCORECARD.md` §Planned.
```

---

## 2. `PROVINCE.md`

### 2a. §Surfaces header line (replace the existing heading)

```markdown
## Surfaces (re-verified round 12, 2026-09-28; every row re-checked this round — route telemetry `{{LEDGER_STATUS}}`, `~/wikillm/llm-wiki` `{{WIKI_STATUS}}`; evidence in `corpus/evidence/round12-fleet/` and the round-12 report)
```

### 2b. §Surfaces row replacements (three rows change; paste each row whole)

```markdown
| Served local model | `http://127.0.0.1:34113` — `/v1/models`, `/health`, `/v1/chat/completions` (Qwen3-Coder-30B-A3B-Instruct **UD-IQ2_XXS**, `owned_by=llamacpp`, `n_ctx=16384`). Round-12 re-verification: read-only scout `GET /v1/models` + `/health` → `{{ENDPOINT_SCOUT}}`; process-level pin re-read (pid `{{SERVER_PID}}`, argv `{{ARGV_TOKENS}}` tokens: `--parallel 2`, `--cont-batching`, `--ctx-size 16384`, `--kv-unified`, `--cache-type-k/v q4_0` — 4-bit KV, unstated premise of every r8/r9/r11/r12 number, `--flash-attn on`, `--no-context-shift`, `--n-gpu-layers 999`, `--jinja --chat-template-file ~/.config/llama/qwen-coder-godspeed.jinja`) | the r12 run re-pins the stack **in-band** in its own `descriptors` record (`corpus/evidence/round12-ladder/results-r12.jsonl`, record 0) and re-reads it at run end (`cell:"descriptors_end"`); a mismatch is a recorded deviation and the run is re-executed, not analyzed (`probe_plan_r12.md:343-348`). |
| Route telemetry | `~/Projects/bounties/ledger/telemetry.jsonl` — `{{LEDGER_STATUS}}`; absent since round 11 (last resolving 23:32Z, live count 7,226 lines; no relocation found) | model×lane and reroute-chain **inference about model service** only; derived counts stay cited as historical until a dated re-check resolves it |
| Own probe artifacts | `corpus/evidence/round8-horizon/`, `corpus/evidence/round9-replication/`, `corpus/evidence/round9-fleet/`, `corpus/evidence/round10-fleet/`, `corpus/evidence/round11-power/`, `corpus/evidence/round11-fleet/`, **`corpus/evidence/round12-ladder/`** (`{{LADDER_FILES}}` files: bundle + machinery + run bytes + generated analysis), **`corpus/evidence/round12-fleet/`** (`{{FLEET_FILES}}` files: L2 artifacts + `INTEGRATOR-NOTES.md`) | durable run bytes + analyses + L2 fleet artifacts; nothing cited from `/tmp` or session `local://` alone |
| In-repo gate | `grader.py` (repo root; `python3 grader.py` → exit 0/1/2, `--selftest` S0–S7) | hermetic offline replay of **four** probe trees (r8/r9/r11/r12): recomputes every stored SUMMARY/analysis number from committed bytes, md5-pins the evidence files, pins the adjudicated erratum pairs, re-verifies every ordering proof (r9 + r11 + **r12 prereg bundle hash chain**); **`{{GRADER_CHECKS}}`** checks after the round-12 extension (from 280; `grader.py` `{{GRADER_LINES}}` lines) |
```

### 2c. Round-12 report-outs (append after the round-11 block, same shape)

```markdown
Round-12 report-outs (evidence sent, not absorbed): (1) **protocol** — the
preregistration standard referral from r11 stands (hashed predictions + filed
power analysis + probabilistic scoring + ordering proof + hermetic replay gate;
no sibling owner, `{{W1_ARTIFACT_CONNECTOR}}` re-checked at current sibling
HEADs). (2) **kotoba** — the 6-cell ack-compliance table under checkpoint
schedules `{{ACK_COMPLIANCE}}` (the model emits unrequested full states on ack
turns; the r9-verbatim post-checkpoint spillover ask inflates this by design):
prompt-craft evidence for benchmark authors who treat `Reply 'ok'` turns as
free. (3) **integrator / unowned serving plane** — the r12 `descriptors` record
re-pins the same stack (pid `{{SERVER_PID}}`, `{{ARGV_TOKENS}}`-token argv,
q4_0 KV, `--kv-unified`); flag-change authority stays unowned, and the
KV-quantization level remains material to ANY cross-model number from :34113.
(4) **kasegi** — ledger-tree status re-checked this round: `{{LEDGER_STATUS}}`
(command in the round-12 LOG entry); no change to the r11 marking unless the
dated re-check resolves it.
```

---

## 3. `SHONEN.md` — the four checklist lines, round-12 counts (paste over lines 5–12, keeping the `- [..]` glyphs L1 rules on)

```markdown
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  2 decision tables, `{{ANTIPATTERN_AFTER}}` anti-patterns, 9-step checklist, `{{BULLETS_AFTER}}` cited-source bullets, SKILL.md `{{SKILL_LINES_AFTER}}` lines (from 518); citation resolution `{{CITATION_RES}}` under the round-10 convention (the ≥90% rubric floor must be re-measured after the round-12 edits, not assumed)
- [~] At least one end-to-end domain task executed and logged in LOG.md
  round-4 4-task slice, round-5 33-task battery, round-8 78-job horizon probe, round-9 pre-registered replication (284 records), round-11 powered preregistered rerun (n=64, 1473 records, severity dose ESTABLISHED), **round-12 ladder + transport run (n=64 family 1 + n=48 family 2, `{{RECORDS}}` records, five mechanical verdicts `{{VERDICT_R1}}`/`{{VERDICT_R2}}`/`{{VERDICT_R3}}`/`{{VERDICT_R4}}`/`{{VERDICT_R5}}`) — `corpus/evidence/round12-ladder/results-r12.jsonl`**; LOG.md rounds 4–12
- [x] Instructions executable by an agent without oral context
  tested 2026-09-28T23:31–23:33Z at HEAD `0c51208` by the aggregator's non-author cold run (`corpus/lessons/round-8-aggregator-box3-coldrun.md`, aggregator-committed `06cdc98` + amendment `d8f2898`): 20/20 read-only commands reproduced from SKILL.md text alone; the hermetic gate ran cold, exit 0 with the exact claimed outputs (then-current n=149 + selftest 4/4). Round-12 state: the gate is `{{GRADER_CHECKS}}` checks / S0–S7 and re-runs cold at the r12 HEAD (round-12 reviewer baseline `{{REVIEW_BASELINE_VERDICT}}`); box stays `[x]` unless a re-run breaks a cited command
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  `PROVINCE.md` §Surfaces re-verified round 12 — `{{PROVINCE_DRIFT}}` drift recorded, not hidden; knowledge entries cite llm-wiki notes, bench-arena/bailian surfaces, model-catalog APIs, own `corpus/evidence/`, or fetched public literature; round-9/10/11/12 report-outs on file (round 12: protocol preregistration-standard referral, kotoba ack-compliance craft evidence, integrator KV-quantization materiality, kasegi ledger status)
```

---

## 4. `SCORECARD.md`

### 4a. New section — paste after the round-11 post-move table (i.e. before `## Scoring rubric`, line 148)

```markdown
## Round 12 — post-move (novelty axis-move landed)

| Axis | Before → After | What moved | Evidence |
|---|---|---|---|
| **novelty** *(owned)* | 6 → **`{{AXIS_NOVELTY_AFTER}}`** | `{{NOVELTY_MOVE}}` | `{{NOVELTY_PTR}}` |
| **calibration** *(owned)* | 8 → **`{{AXIS_CALIBRATION_AFTER}}`** | `{{CALIBRATION_MOVE}}` | `{{CALIBRATION_PTR}}` |
| depth | 9 → **`{{AXIS_DEPTH_AFTER}}`** | `{{DEPTH_MOVE}}` | `{{DEPTH_PTR}}` |
| coverage | 7 → **`{{AXIS_COVERAGE_AFTER}}`** | `{{COVERAGE_MOVE}}` | `{{COVERAGE_PTR}}` |
| operability | 7 → **`{{AXIS_OPERABILITY_AFTER}}`** | `{{OPERABILITY_MOVE}}` | `{{OPERABILITY_PTR}}` |
| freshness | 7 → **`{{AXIS_FRESHNESS_AFTER}}`** | `{{FRESHNESS_MOVE}}` | `{{FRESHNESS_PTR}}` |
| adjacency | 8 → **`{{AXIS_ADJACENCY_AFTER}}`** | `{{ADJACENCY_MOVE}}` | `{{ADJACENCY_PTR}}` |

Pre-move anchors (round-11 §Round-11 post-move): novelty 6, calibration 8, depth 9, coverage 7, operability 7, freshness 7, adjacency 8.
```

Scribe drafting notes for the cells L1 writes by hand (not paste text — reasoning to speed the scoring, each one quoted against the rubric at `SCORECARD.md:148-161`):

- **novelty** — the +1 leg needs all three: a construct the lane could not previously observe (the four-point ordered ladder + the transport family + per-problem forecast skill — none observable before r12), an instrument inspectable in-repo (`probe_r12.py`/`run_r12.py`/`recompute_r12.py`/`predict_r12.py` + the hashed bundle), and a prior-art verdict with a fetched URL per claim (`{{C1_C6_VERDICTS}}`). Caps that may apply: one served unit, one phenomenon family; an INCREMENTAL pricing on the ladder/transport claims does not block the +1 (r11 scored 5→6 with C1 INCREMENTAL-low) but it *is* the pointer's ceiling clause.
- **calibration** — +1 only if all five clauses hold: predictions filed pre-request and scored (clause (a)/(b)); every row's pointer re-runs (clause (c) — the `{{REVIEW_BASELINE_VERDICT}}` sweep plus the r11 criticisms); analyzed + indexed + logged in-round (clause (d) — the two new README rows and the LOG entry); landed bytes match the run (clause (e) — md5 at copy). The rubric's cap "point forecasts where probabilities are feasible" is now *closed* (448 per-problem events scored), so this is the round where 8→9 is arguable.
- **depth** — the anti-double-count ruling from rounds 10–11 applies: SKILL/README bytes that merely document *this round's* artifact do not earn depth. Bump only for new sourced claims beyond the probe bytes (e.g. the ordered-trend statistic or the persistence-vs-cold-forecast distinction if written as a decision rule with a citation).
- **coverage** — the cap that fired in r11 was "declared-but-unresolvable surfaces": `{{LEDGER_STATUS}}` this round. Index both directions must be equal after the new rows (`{{KN_ROWS_AFTER}}`/`{{LS_ROWS_AFTER}}`/`{{EV_ROWS_AFTER}}`); if the ledger surface is still absent, coverage cannot reach 10, and whether it earns +1 turns on whether "PROVINCE enumerates surfaces that resolve" holds with one marked-absent surface.
- **operability** — the round's +1 rests on the gate extension landing **in the same round as the bytes** (round-11 §Planned clause (d)): `{{GRADER_CHECKS}}` checks / four trees / S0–S7 / `{{MUTATION_BATTERY}}`. Ceiling unchanged: new data still needs the live endpoint.
- **freshness** — +1 requires a re-verification line per touched claim in the LOG entry (drafted in `r12-log-draft.md` §(i)) plus resolving host-path/endpoint citations (`{{ENDPOINT_SCOUT}}`, `{{LEDGER_STATUS}}`, `{{WIKI_STATUS}}`).
- **adjacency** — held unless the connector surfaces a **new** arbitration; re-verifying the r10/r11 rulings is not a bump.

### 4b. Rewritten `## Planned (next axis-move)` — replace lines 163–184

```markdown
## Planned (next axis-move)

Lowest post-move axis is **coverage (`{{AXIS_COVERAGE_AFTER}}`)** — reasoned,
not guessed, from the round-12 table above and the rubric that scores it:

1. An axis-move is ±1, and a round picks the **lowest** post-move axis.
2. Round 12 spends the owned novelty move: its three +1 legs (new construct,
   in-repo instrument, fetched-URL pricing) are satisfied by the ladder +
   transport + per-problem-forecast instrument — so novelty leaves the floor
   unless a pricing lock (`{{C1_C6_VERDICTS}}`) demotes every claim to a
   re-run of a published phenomenon.
3. The axes the round does **not** earn are exactly the ones whose +1 clauses
   it fails: **depth** (anti-double-count — its bytes document this round's own
   artifact; only new *sourced* claims beyond the probe bytes count),
   **adjacency** (no new integrator arbitration; the connector re-verifies
   standing rulings), and **coverage** (the round adds bytes, not surfaces).
4. Therefore the projected floor is a tie between **coverage (`{{AXIS_COVERAGE_AFTER}}`)**
   and **novelty (`{{AXIS_NOVELTY_AFTER}}`)** whenever novelty gains exactly
   one point. Tie-break used here: prefer the axis whose +1 leg is (i) satisfiable
   inside this lane without the operator and (ii) *not* named on the rubric's
   cap list. Coverage's cap names "declared-but-unresolvable surfaces" — it
   prevents 10 while `~/Projects/bounties/ledger/` is missing, but the +1 leg
   is still landable on the surfaces this corpus *describes and can reach*.

The move: a **surface-completeness move** — close the two coverage items the
corpus itself names and never resolves. (a) Sweep the named open surface
(non-karpathy `wiki/ai/` topics beyond eval scope) and **either** digest each
into `corpus/knowledge/` with a first-line source **or** record an explicit
out-of-scope ruling with its reason in `corpus/README.md` §Coverage map —
`../AXES.md`'s coverage signal is "none unexplored without reason". (b) Clear
the **prior-art digest queue** (`arxiv.org/abs/2505.06120`,
`arxiv.org/abs/2307.13702`, llama.cpp #7052) either as digests or as scoped
rulings — it has been carried as "named but unread" since round 9. (c) Re-check
`~/Projects/bounties/ledger/` with a dated command and, whether it resolves or
not, replace the undated marking with a dated one so the cap is at least
*measured* rather than assumed. (d) Index both directions at round close
(rows = files for knowledge/lessons/evidence, commands in the round-12 LOG
entry). Anti-double-count ruling recorded in advance: any new *sourced claims*
produced by (a) may bump **depth** or **coverage** in this round, never both.
Contingency (if L1's post-move table puts **novelty** at the floor instead, or
if coverage's +1 is refused because a marked-absent surface means "PROVINCE
does not enumerate only resolving surfaces"): the fallback move is a novelty
move on the forecast axis — a **cold-forecast** design in which the predictor
is fitted on r11's bytes and scored on **unseen** problems/arms, pre-registering
the persistence baseline as the comparator, at a filed MDE. That needs a new
problem sample and a new bundle, not a new model.

Falsifiable target: the named `wiki/ai/` surface is either digested (new
`corpus/knowledge/` entry with a first-line source) or ruled out of scope with
a stated reason in `corpus/README.md`; the three queued prior-art sources are
digested or explicitly ruled; the ledger surface carries a dated re-check line;
index both directions equal at round close (commands pasted in `LOG.md`);
`python3 grader.py` exits 0 with selftest S0–S7 passing on the r13 tree.
```

### 4c. **OPTIONAL** — round-12 errata block (paste after 4a, before `## Scoring rubric`, if L1 rules the defect as one)

Evidence, all re-runnable at HEAD `f09ff1f` (see the round-12 report draft §Errata & deviations for the full statement):

```markdown
## Round 12 — erratum to a round-11 row (measured at `HEAD` `f09ff1f`)

- **F-R12-1 — round-11 operability cell, gate line count.** The round-11 row
  (`## Round 11 — post-move`), `LOG.md:18` and the round-11 report all publish
  `grader.py` as growing "936 → **1709** lines". The committed artifact is
  **1711** lines: `git show f09ff1f:grader.py | wc -l` → `1711`;
  `wc -l < grader.py` → `1711`; `grep -c -v '^$' grader.py` → `1527`;
  `grep -c '^$' grader.py` → `184` — no counting convention yields 1709. The
  *before* half is exact (`git show 0c51208:grader.py | wc -l` → `936`) and the
  check count is exact (`python3 grader.py` → `CHECKS n=280 mismatches=0
  errata_pinned=1`, exit 0, re-run 2026-09-28). [INFERENCE] the 1709 was most
  likely measured before the two-line in-code comment recording the
  file-order-primacy ordering-check fix (`round11-fleet/INTEGRATOR-NOTES.md`
  §Integration deltas 2) landed in the same commit; that provenance is
  conjectural and is not claimed. Consequence: any round-12 self-description
  must use the measured `{{GRADER_LINES}}` *after* the extension, and the
  round-11 sentence is corrected here, never patched in place (round-10 F1/F2/F3
  precedent).
```

### 4d. **OPTIONAL** — append a movement line to `## Retired` (the section already carries the round-11 movement sentence)

```markdown
Round-12 movement: novelty 6→`{{AXIS_NOVELTY_AFTER}}` (the axis-move landed),
calibration 8→`{{AXIS_CALIBRATION_AFTER}}`, operability 7→`{{AXIS_OPERABILITY_AFTER}}`,
freshness 7→`{{AXIS_FRESHNESS_AFTER}}`; depth, coverage and adjacency held
`{{AXIS_DEPTH_AFTER}}` / `{{AXIS_COVERAGE_AFTER}}` / `{{AXIS_ADJACENCY_AFTER}}`
with the no-bump rulings recorded in the round-12 table above.
```

---

## 5. **OPTIONAL** — `LOG.md` errata line (append-only; one physical line)

If L1 files F-R12-1, the round-12 LOG entry may be followed by a second single-line bullet in the round-9 style ("corrections … supersedes two figures inside the round-9 entry above"):

```markdown
- 2026-09-28 — round 12 (erratum; supersedes one figure inside the round-11 entry above): the round-11 gate line count "936→1709 lines" is corrected to **936 → 1711** — `git show f09ff1f:grader.py | wc -l` → 1711 at the round-11 commit, while `git show 0c51208:grader.py | wc -l` → 936 confirms the before-half; the check count (280) and the selftest claim (7 scenarios S0–S6) are unaffected. Recorded at three sites so the correction is findable from each: `LOG.md:18`, `SCORECARD.md:142`, and the round-11 report — the report site is named in the errata rather than edited (append-only discipline forbids rewriting a committed report; the naming makes the stale figure traceable from the correction); no committed byte is edited in place (round-6 audit rule 9).
```

---

## 6. Closing — round-11 sentences deliberately NOT carried over (and why)

Rationale for omissions from the round-11 texts (`LOG.md:18`, `.ufo/reports/round-11/kengaku.md`, the round-11 rows of `SCORECARD.md`, `SHONEN.md` lines 5–12, `PROVINCE.md` §§Surfaces/report-outs). Each omission is deliberate; a carried-forward number is stale or now wrong, not merely old.

1. **`grader.py` "936 → 1709 lines"** — stale/wrong: the committed artifact is 1711 lines (commands in §4c). Carried only as the erratum, never as a live claim.
2. **`LOG.md:18`'s "1409 requests / 1473 records in 259.1 s"** and the round-11 census `1/64/320/960/128/0` — r11 run bytes. r12's gate-pinned totals are 4 114 records / 4 002 calls, and the observed values are `{{RECORDS}}` / `{{REQUESTS}}` / `{{WALL_S}}` / `{{CENSUS}}`.
3. **The r11 result numbers as if they were the round's** (+0.352, t=+3.431, p=0.0011, CI [+0.147,+0.556], sign 26W/7L/31T, McNemar b=13 c=5 p=0.0963, 29/64 & 21/64, Brier 0.153, ack 49.1%/64.5%) — they now appear **only** where explicitly labelled `r11 comparator` (E2, E6) or as the E2 point-match anchor. Reusing them unlabelled is the stale-count defect class the round-10 critic filed (F1).
4. **"`python3 grader.py --selftest` → S0–S6 ALL PASS"** as the current state — superseded by S0–S7 (`{{SELFTEST}}`); the r11 sentence is quoted only inside historical context.
5. **"novelty 5 → 6" / "calibration 7 → 8" / "operability 6 → 7" / "depth 8 → 9" / "freshness 6 → 7"** as live before→after pairs — those are round-11 movements; round 12's before-column is exactly those after-values (6/8/9/7/7/7/8) and the new cells are `{{AXIS_*_AFTER}}`.
6. **The r11 L2 roster and every per-agent task sentence** (CriticDesign's r11 brief, ScoutGranularity, ScoutPrereg, ExecutorGrader/ExecutorRecompute as *r11 extension* drafts, ScribeReport, LabratMock's `import json` catch, CriticLanded's 10/10, MutationGrader's 11/11, ReviewerIndex's 4 defects) — replaced wholesale by the r12 roll-call. The only reused text is the MISSION route-bucket sentence and the "no L2 wrote a shared file; single integration owner: L1" convention.
7. **r11's prior-art verdict table** (C1 INCREMENTAL-low with StageIF `2609.08589` / `2605.30233`; C2 KNOWN/INCREMENTAL; C3 NOVEL-instrument; C4 INCREMENTAL with `2606.11217` / `2603.10044`) — that was round 11's pricing of round-11 claims. C1–C6 must be priced afresh against a new search set; r11 URLs may return only as explicitly-labelled method context (the r11 report's own wording-finding discipline: negatives scoped to the search set, prior-art-context framing stated).
8. **"Ack compliance: A-CKPT4710 220/448 = 49.1%, A-CKPT710 330/512 = 64.5%"** — wrong denominators for r12 (six ack cells, `{{ACK_COMPLIANCE}}`).
9. **"route-telemetry surface … ABSENT … resolved 23:32Z … 7,226 live lines"** and the SHONEN box-3 flip narrative ("20/20 read-only reproductions … flipped the box") — round-11 events now permanent repo state. The carried element is only the *re-check* (`{{LEDGER_STATUS}}`) and the box's own re-verified line.
10. **"41 committed pointers → BASELINE GREEN"**, **"ReviewerBaseline … grader n=149 control"** — r11 counts; r12's own sweep is `{{REVIEW_BASELINE_VERDICT}}`, whose control value is now 280 checks pre-extension (real, re-run 2026-09-28).
11. **"Brier 0.153" as the lane's probabilistic-forecast state** — true for r11 (3 events), but the round-11 §Planned clause (b) is now fulfilled at the per-problem level; the README/SHONEN text says so with `{{E6_*}}` instead of restating 0.153 as current.
12. **The r11 §Planned target sentence as the round-12 target** — it is quoted once, in the falsifiable-target checklist, as the target r12 *closes* (verbatim, `SCORECARD.md:181-184`); §4b replaces the section itself.

_Fill rule: L1 resolves every `{{TOKEN}}` with the command in `r12-report-draft.md` §Placeholder registry — the same names, nothing renamed. Blocks 4c/4d/5 are optional but mutually consistent: filing the errata in SCORECARD without the LOG line is a half-correction, and `PROVINCE.md`/`SHONEN.md` must not cite 1709 anywhere after this round._
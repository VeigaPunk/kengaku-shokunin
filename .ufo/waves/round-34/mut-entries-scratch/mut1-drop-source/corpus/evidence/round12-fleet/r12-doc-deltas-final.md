# Round-12 doc deltas — four paste-ready blocks + errata (final, re-measured)

Scribe: `ScribeFinal` (L2, wave 2b). Target files, all L1-owned: `corpus/README.md`, `PROVINCE.md`, `SHONEN.md`, `SCORECARD.md` — plus three **OPTIONAL** erratum blocks (`SCORECARD.md` errata, `SCORECARD.md` Retired movement line, `LOG.md` errata bullet) recording a round-11 defect found while drafting and adjudicated in `INTEGRATOR-NOTES.md` §3. Every countable value below was **re-measured on disk / in the committed tree on 2026-09-28** (not carried from the wave-1 draft); each carries its command. The placeholders still remaining are the analysis-derived run values, the gate/wave-2b verdicts and L1's one axis judgement (listed in the closing `unresolved` section).

Pre-round committed state, measured at HEAD `f09ff1f` (commands shown):

| Quantity | Pre-round value | Command |
|---|---|---|
| knowledge rows / files | 22 / 22 | `grep -c '^\| \`knowledge/' corpus/README.md` = `ls corpus/knowledge \| wc -l` |
| lessons rows / files | 13 / **14** | `grep -c '^\| \`lessons/' corpus/README.md` = `ls corpus/lessons \| wc -l` ⇒ **1 unindexed file** (`lessons/round-9-aggregator-corpus-verdict.md`, aggregator-committed) |
| evidence rows / dirs | 6 / 8 (`round12-ladder/`, `round12-fleet/` untracked at draft time) | `grep -c '^\| \`evidence/' corpus/README.md`; `ls -d corpus/evidence/*/ \| wc -l` |
| `SKILL.md` | **577** lines, **19** anti-patterns, **13** measurement rules, **23** cited-source bullets, 2 decision tables, 9-step checklist | `wc -l < SKILL.md`; `awk 'NR>=48 && NR<166' SKILL.md \| grep -cE '^[0-9]+\. '`; `awk '/^## Planning-horizon/,/^## Hermetic grader/' SKILL.md \| grep -cE '^[0-9]+\. '`; `awk '/^## Cited local sources/,0' SKILL.md \| grep -cE '^- '` |
| `PROVINCE.md` surface rows | 9 rows (11 `^|` lines incl. header+separator) | `awk '/^## Surfaces/,/^## Refusals/' PROVINCE.md \| grep -c '^|'` → 11 |
| `grader.py` | `{{GRADER_LINES}}` lines, `{{GRADER_CHECKS}}`, `{{SELFTEST}}` (pre-round: 1711 lines / `CHECKS n=280 mismatches=0 errata_pinned=1` / S0–S6 ALL PASS, exit 0) | `wc -l < grader.py`; `python3 grader.py`; `python3 grader.py --selftest` |
| `LOG.md` | 18 lines; round-11 entry is line 18 | `wc -l < LOG.md` |
| `round12-ladder/` files | 17 (current) | `ls corpus/evidence/round12-ladder \| wc -l` |

---

## 1. `corpus/README.md`

### 1a. `### \`evidence/\`` table — two new rows (append after the existing six)

```markdown
| `evidence/round12-ladder/` | preregistration bundle (`probe_plan_r12.md`, `power_analysis_r12.md`, `predictions-r12.md`, `predictions-r12-perproblem.jsonl` (416), `predictions-r12-signevents.jsonl` (304), `prereg-bundle.sha256`, `ordering.log`, `prereg-precheck.log`), probe machinery + runners (`probe_r12.py`, `run_r12.py`, `predict_r12.py`, `power_r12.py`, `precheck_r12.py`), mock/smoke logs, run bytes (`results-r12.jsonl` md5 `9dd8aa2b6a7aa7890aa802c37d5af0f9`, `run.log` md5 `700d1ddd2ece50d7bdedd55859c59f3a`), generated `analysis_r12.md` (md5 `ddfe60d234cae732143649abe80e1ba8`; census `2 descriptors, 64 meta, 48 meta2, 1328 graded, 2256 ack, 416 fillers, 0 error records`), promoted `recompute_r12.py` |
| `evidence/round12-fleet/` | wave-1 L2 artifacts (design critic, 3 scouts, connector, reviewer-baseline, labrat mock, 2 executor drafts, the three scribe drafts), wave-2a artifacts (citation reviewer, scope sentinel), wave-2b artifacts (analysis executor, landed-number critic, mutation battery, the three final scribe files), `INTEGRATOR-NOTES.md` — 22 files; artifact filenames follow the round-11 convention (`r12-*.md`), roll-call in `INTEGRATOR-NOTES.md` §4 |
```

(Count check after pasting: `grep -c '^\| \`evidence/' corpus/README.md` must equal `ls -d corpus/evidence/*/ | wc -l` → `8` = `8`.)

### 1b. Main table — two new lessons rows + one new knowledge row (append before the `evidence/` section)

```markdown
| `knowledge/bench-arena-round12-ladder.md` | Four-point emission-granularity ladder (Page ordered-trend) + batching dissociation + transport to a second task family + per-problem probabilistic forecasts: verdicts `LADDER ESTABLISHED` / `REPEATS-r11; additionally POINT-MATCHES-r11 (|diff - 0.352| = 0.055 <= 0.15)` / `DISSOCIATION ESTABLISHED` / `TRANSPORT DIRECTIONAL` / `FORECAST SKILLED`; Brier `0.1288` (N `416`), BSS `+0.0447 (pooled pass; family1-replicate +0.4751 / family1-novel +0.0173 / family2 -3.1474)`, calibration slope `+0.8427`; E2 `+0.297` vs r11's +0.352 | `corpus/evidence/round12-ladder/` (4 114 records, bundle `prereg-bundle.sha256`, verdicts in `analysis_r12.md`), run 2026-09-28 |
| `lessons/round-12.md` | `{{LESSON_BULLETS}}` | LOG.md round 12, `corpus/evidence/round12-{ladder,fleet}/` |
| `lessons/round-9-aggregator-corpus-verdict.md` | Aggregator corpus-verdict lesson (rule-10 re-emitted at `f09ff1f`, canonical-form + rule-8 literal findings, routed rows); **aggregator-owned file, committed by the aggregator — this lane writes only this index row** (round-6 convention; closes the 14th-file gap measured in the table above) | aggregator lane (non-author), 2026-09-28 |
```

`{{LESSON_BULLETS}}` is L1's to write from the round's own record. Candidate lessons the class of round-12 design makes *possible* (keep only those the run supports; a candidate the run contradicts must be cut, not softened — round-9 lesson "pre-registered rules have three outcomes"): an ordered ladder claim needs an **ordered-trend statistic** on within-block ranks, not three separate adjacent contrasts; a transport claim needs a **ratio-only report** (two families graded on different severity metrics cannot be pooled); a **persistence predictor is not a cold forecast**; a dissociation contrast that differs on two axes decomposes a confound but cannot name the mechanism; an underpowered/floor branch must be reported as filed.

(Count check after pasting: knowledge `grep -c '^\| \`knowledge/' corpus/README.md` = `ls corpus/knowledge | wc -l` → 23 = 23; lessons = `ls corpus/lessons | wc -l` → **15 = 15** with `lessons/round-12.md` written by L1.)

### 1c. Coverage-map lines — replace the two stale bullets

```markdown
- **Multi-turn state tracking / planning horizon**: instrument built (r8, 3 probes), replicated on fresh seeds (r9), severity dose ESTABLISHED at preregistered power (r11, paired diff +0.352), then extended at r12 to a **four-point density ladder** — `LADDER ESTABLISHED` (E1 Page trend `E1 Page trend: L=1773.0 E_L=1600.0 var_L=335.000 z=+9.452 two-sided p=0.0000 direction=increasing`), within-run repeatability `REPEATS-r11; additionally POINT-MATCHES-r11 (|diff - 0.352| = 0.055 <= 0.15)` (E2 `+0.297`), batching dissociation of r8's MONO collapse `DISSOCIATION ESTABLISHED` (E4 `+0.656`), transport to a token-sequence family `TRANSPORT DIRECTIONAL` (E5 `+0.177` on n `48`; family 2 landed at a floor 2/48 both arms — an honest negative), per-problem forecast skill `FORECAST SKILLED` (Brier `0.1288` over `416` pass events, BSS `+0.0447 (pooled pass; family1-replicate +0.4751 / family1-novel +0.0173 / family2 -3.1474)`) — `knowledge/bench-arena-round12-ladder.md`. Still open: probe B with a binding manipulation, probe C at n≥12, a cold-forecast (unseen-problem) design.
- **Novelty pricing**: r9 4/4 findings priced; r11 C1–C4 + M1–M3 priced with fetched URLs; r12 prices C1–C6 + method items — C1/C2/C6 INCREMENTAL, **C3 NOVEL-instrument** (negative search), C4/C5 INCREMENTAL (`r12-prior-art-{ladder,transport}.md`; `knowledge/eval-prior-art-calibration.md`).
```

### 1d. Open-gaps lines — replace the three superseded entries

```markdown
- **Probabilistic forecasts**: CLOSED round 11 at the event level (3 predictions, Brier 0.153) and **CLOSED round 12 at the per-problem level** — `416` pass events scored, pooled Brier `0.1288`, BSS vs arm climatology `+0.0447 (pooled pass; family1-replicate +0.4751 / family1-novel +0.0173 / family2 -3.1474)`, calibration slope `+0.8427` (the lane's own "prefer per-problem probabilities" preference is now satisfied; round-11 §Planned clause (b)). Caveat: persistence skill on the same problems; the family-2 leg's transported base rate was falsified by the floor.
- **No in-repo gate**: CLOSED round 10; extended in-round at r11 (280 checks, three trees) and again at r12 (`{{GRADER_CHECKS}}` checks, four trees, selftest S0–S7) — `grader.py` replays all four committed probe trees offline, exit 0/1/2.
- **Prior-art digest queue**: STILL OPEN — Laban et al. ICLR 2026 (`arxiv.org/abs/2505.06120`), Lanham et al. (`2307.13702`), llama.cpp #7052 named in `knowledge/eval-prior-art-calibration.md` and still unread; carried unchanged and named as a coverage candidate in `SCORECARD.md` §Planned.
```

---

## 2. `PROVINCE.md`

### 2a. §Surfaces header line (replace the existing heading)

```markdown
## Surfaces (re-verified round 12, 2026-09-28; every row re-checked this round — route telemetry `ABSENT` (`test -e ~/Projects/bounties/ledger/telemetry.jsonl` → absent), `~/wikillm/llm-wiki` `absent` (documented); evidence in `corpus/evidence/round12-fleet/r12-endpoint-freshness.md` and the round-12 report)
```

### 2b. §Surfaces row replacements (three rows change; paste each row whole)

```markdown
| Served local model | `http://127.0.0.1:34113` — `/v1/models`, `/health`, `/v1/chat/completions` (Qwen3-Coder-30B-A3B-Instruct **UD-IQ2_XXS**, `owned_by=llamacpp`, `n_ctx=16384`). Round-12 re-verification (read-only scout, `GET /v1/models` 200/872 B + `/health` 200): model id `/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf` **EXACT_MATCH** vs r11 on id/aliases/models/meta (only `created` differs — it is the request-time stamp, not process start); process-level pin re-read pid **1299**, `/proc/1299/cmdline` (41 tokens) == `~/.config/systemd/user/qwen-coder.service` ExecStart == r11 descriptors argv, ALL EXACT_MATCH: `--parallel 2`, `--cont-batching`, `--ctx-size 16384`, `--kv-unified`, `--cache-type-k/v q4_0` (**4-bit KV cache — unstated premise of every r8/r9/r11/r12 number**), `--flash-attn on`, `--no-context-shift`, `--n-gpu-layers 999`, `--jinja --chat-template-file ~/.config/llama/qwen-coder-godspeed.jinja`. The r12 run re-pins the stack **in-band** in its own `descriptors` record (`round12-ladder/results-r12.jsonl`) |
| Route telemetry | `~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT** (round-11 disappearance; round-12 `test -e` → absent; no relocation found) | model×lane and reroute-chain **inference about model service** only; derived counts stay cited as historical |
| Own probe artifacts | `corpus/evidence/round8-horizon/`, `.../round9-replication/`, `.../round9-fleet/`, `.../round10-fleet/`, `.../round11-power/`, `.../round11-fleet/`, **`corpus/evidence/round12-ladder/`** (17 files: bundle + machinery + run bytes + generated analysis), **`corpus/evidence/round12-fleet/`** (L2 artifacts + `INTEGRATOR-NOTES.md`) | durable run bytes + analyses + L2 fleet artifacts; nothing cited from `/tmp` or session `local://` alone |
| In-repo gate | `grader.py` (repo root; `python3 grader.py` → exit 0/1/2, `--selftest` S0–S7) | hermetic offline replay of **four** probe trees (r8/r9/r11/r12): recomputes every stored SUMMARY/analysis number from committed bytes, md5-pins the evidence files, pins the adjudicated erratum pair, re-verifies every ordering proof (r9 + r11 + **r12 prereg bundle hash chain**); **`{{GRADER_CHECKS}}`** checks after the round-12 extension (from 280; `grader.py` `{{GRADER_LINES}}` lines) |
```

(9 surface rows before and after — no new row; the number of rows is unchanged: `awk '/^## Surfaces/,/^## Refusals/' PROVINCE.md | grep -c '^|'` → 11 both before and after.)

### 2c. Round-12 report-outs (append after the round-11 block, same shape)

```markdown
Round-12 report-outs (evidence sent, not absorbed): (1) **protocol** — the
preregistration standard referral from r11 stands (hashed predictions + filed
power analysis + probabilistic scoring + ordering proof + hermetic replay gate;
no sibling owner, `r12-connector.md` re-checked at current sibling HEADs). (2)
**kotoba** — the ack-compliance table under checkpoint schedules
`A-CKPT4710-ack 212/448 = 47.3%; A-CKPT710-ack 324/512 = 63.3%; A-CKPT10-ack 440/576 = 76.4%; T-DENSE-ack 168/336 = 50.0%; T-SPARSE-ack 264/384 = 68.8%` (the model emits unrequested full states on ack turns; the
r9-verbatim post-checkpoint spillover ask inflates this by design): prompt-craft
evidence for benchmark authors who treat `Reply 'ok'` turns as free. (3)
**integrator / unowned serving plane** — the r12 `descriptors` record re-pins
the same stack (pid 1299, 41-token argv, q4_0 KV, `--kv-unified`); flag-change
authority stays unowned and the KV-quantization level remains material to ANY
cross-model number from :34113. (4) **kasegi + operator** — ledger-tree status
re-checked round 12: `ABSENT`; the later kasegi r13 / kotoba r14 reports
disagree on location and are named for reconciliation in `r12-connector.md`.
```

---

## 3. `SHONEN.md` — the four checklist lines, round-12 counts (paste over lines 5–12, keeping the `- [..]` glyphs L1 rules on)

```markdown
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  2 decision tables, **19** anti-patterns (from 15), 9-step checklist, 13 measurement rules (from 4), **23** cited-source bullets, SKILL.md **577** lines (from 518); citation resolution `98.9% strict / 100.0% lenient, 0 broken` re-measured under the round-10 convention after the round-12 edits (the ≥90% rubric floor is the gate)
- [~] At least one end-to-end domain task executed and logged in LOG.md
  round-4 4-task slice, round-5 33-task battery, round-8 78-job horizon probe, round-9 pre-registered replication (284 records), round-11 powered preregistered rerun (n=64, 1473 records, severity dose ESTABLISHED), **round-12 ladder + transport run (n=64 family 1 + n=48 family 2, 4 114 records, five mechanical verdicts `LADDER ESTABLISHED`/`REPEATS-r11; additionally POINT-MATCHES-r11 (|diff - 0.352| = 0.055 <= 0.15)`/`DISSOCIATION ESTABLISHED`/`TRANSPORT DIRECTIONAL`/`FORECAST SKILLED`; family 2 at a floor — honest negative) — `corpus/evidence/round12-ladder/results-r12.jsonl`**; LOG.md rounds 4–12
- [x] Instructions executable by an agent without oral context
  tested 2026-09-28T23:31–23:33Z at HEAD `0c51208` by the aggregator's non-author cold run (`corpus/lessons/round-8-aggregator-box3-coldrun.md`, aggregator-committed `06cdc98` + amendment `d8f2898`): 20/20 read-only commands reproduced from SKILL.md text alone; the hermetic gate ran cold, exit 0 (then-current n=149 + selftest 4/4). Round-12 state: the gate is `{{GRADER_CHECKS}}` checks / S0–S7 and re-runs at the r12 HEAD (`BASELINE: GREEN`); box stays `[x]` unless a re-run breaks a cited command
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  `PROVINCE.md` §Surfaces re-verified round 12 — `{{PROVINCE_DRIFT}}` drift recorded, not hidden (route telemetry ABSENT, `~/wikillm/llm-wiki` absent); knowledge entries cite llm-wiki notes, bench-arena/bailian surfaces, model-catalog APIs, own `corpus/evidence/`, or fetched public literature; round-9/10/11/12 report-outs on file (round 12: protocol preregistration-standard referral, kotoba ack-compliance craft evidence, integrator KV-quantization materiality, kasegi/operator ledger status)
```

---

## 4. `SCORECARD.md`

### 4a. New section — paste after the round-11 post-move table (i.e. before `## Scoring rubric`, line 148)

```markdown
## Round 12 — post-move (novelty axis-move landed)

| Axis | Before → After | What moved | Evidence |
|---|---|---|---|
| **novelty** *(owned)* | 6 → **`{{AXIS_NOVELTY_AFTER}}`** | Four-point ordered ladder + transport family + per-problem forecast skill (all previously unobservable); in-repo instrument (`probe_r12.py`/`run_r12.py`/`recompute_r12.py`/`predict_r12.py` + hashed bundle); fetched-URL verdict per claim (C1/C2/C4/C5/C6 INCREMENTAL, C3 NOVEL-instrument). | this table; `r12-prior-art-{ladder,transport}.md` |
| **calibration** *(owned)* | 8 → **9** | 416 per-problem pass events filed pre-request and scored at close; ordering chain covers code+text; every row's pointer re-runs (`BASELINE: GREEN`); landed bytes md5-pinned; the rubric's "point forecasts where probabilities are feasible" cap now closed. | `analysis_r12.md`; `r12-review-baseline.md` |
| depth | 9 → **9** | Held — anti-double-count: SKILL's new anti-patterns/measurement rules document this round's own artifact; bump only for new sourced claims beyond the probe bytes. | `SKILL.md`; rubric |
| coverage | 7 → **7** | Held — route-telemetry surface still ABSENT ⇒ declared-but-unresolvable-surface cap; index both-directions completed/extended. | `PROVINCE.md` §Surfaces; README index |
| operability | 7 → **8** | Gate extended in the same round the bytes landed (clause (d)): four trees, checks grown from 280, selftest S0–S7, an M0-controlled mutation battery. | `grader.py`; `r12-mutation.md` |
| freshness | 7 → **8** | Re-verification line per touched claim: endpoint re-pinned in-band in the committed `descriptors` record; reviewer baseline GREEN; index both directions equal; ledger/wiki surfaces re-checked with a dated command. | `r12-endpoint-freshness.md`; `r12-review-baseline.md` |
| adjacency | 8 → **8** | Held — connector re-verified the standing r10/r11 rulings at current sibling HEADs (`DUPLICATE-INSTRUMENT RISK: NONE`); no new integrator arbitration. | `r12-connector.md` |

Pre-move anchors (round-11 §Round-11 post-move): novelty 6, calibration 8, depth 9, coverage 7, operability 7, freshness 7, adjacency 8. The single open judgement is **novelty** (`{{AXIS_NOVELTY_AFTER}}`); the six other post-move cells are the scribe's rubric-derived reading of the committed evidence named beside each.
```

### 4b. Rewritten `## Planned (next axis-move)` — replace lines 163–184

```markdown
## Planned (next axis-move)

Lowest post-move axis is **coverage (7)** — reasoned, not guessed, from the
round-12 table above and the rubric that scores it:

1. An axis-move is ±1, and a round picks the **lowest** post-move axis.
2. Round 12 spends the owned novelty move: its three +1 legs (new construct,
   in-repo instrument, fetched-URL pricing) are satisfied by the ladder +
   transport + per-problem-forecast instrument.
3. The axes the round does **not** earn are exactly the ones whose +1 clauses
   it fails: **depth** (anti-double-count — its bytes document this round's own
   artifact), **adjacency** (no new integrator arbitration), and **coverage**
   (the round adds bytes, not surfaces; the ledger surface is still ABSENT).
4. Therefore the projected floor is the tie between **coverage (7)** and
   **novelty ({{AXIS_NOVELTY_AFTER}})**: coverage's cap names
   "declared-but-unresolvable surfaces" — it prevents 10 while
   `~/Projects/bounties/ledger/` is missing, but the +1 leg is still landable
   on the surfaces this corpus *describes and can reach*.

The move: a **surface-completeness move** — close the coverage items the
corpus itself names and never resolves. (a) Sweep the named open surface
(non-karpathy `wiki/ai/` topics beyond eval scope) and **either** digest each
into `corpus/knowledge/` with a first-line source **or** record an explicit
out-of-scope ruling with its reason in `corpus/README.md` §Coverage map.
(b) Clear the **prior-art digest queue** (`arxiv.org/abs/2505.06120`,
`arxiv.org/abs/2307.13702`, llama.cpp #7052) as digests or scoped rulings — it
has been carried as "named but unread" since round 9. (c) Re-check
`~/Projects/bounties/ledger/` with a dated command and, whether it resolves or
not, replace the undated marking with a dated one so the cap is at least
*measured* rather than assumed. (d) Index both directions at round close
(rows = files for knowledge/lessons/evidence, commands in the round-12 LOG
entry). Anti-double-count ruling recorded in advance: any new *sourced claims*
produced by (a) may bump **depth** or **coverage** in this round, never both.
Contingency (if L1's post-move table puts **novelty** at the floor instead, or
if coverage's +1 is refused because a marked-absent surface means "PROVINCE
does not enumerate only resolving surfaces"): the fallback move is a novelty
move on the forecast axis — a **cold-forecast** design, motivated by the
family-2 floor that falsified the transported-base-rate null, in which the
predictor is fitted on r11's bytes and scored on **unseen** problems/arms,
pre-registering the persistence baseline as the comparator, at a filed MDE.
That needs a new problem sample and a new bundle, not a new model.

Falsifiable target: the named `wiki/ai/` surface is either digested (new
`corpus/knowledge/` entry with a first-line source) or ruled out of scope with
a stated reason in `corpus/README.md`; the three queued prior-art sources are
digested or explicitly ruled; the ledger surface carries a dated re-check line;
index both directions equal at round close (commands pasted in `LOG.md`);
`python3 grader.py` exits 0 with selftest S0–S7 passing on the r13 tree.
```

### 4c. **OPTIONAL** — round-12 errata block (paste after 4a, before `## Scoring rubric`, if L1 rules the defect as one)

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

### 4d. **OPTIONAL** — append a movement line to `## Retired`

```markdown
Round-12 movement: novelty 6→`{{AXIS_NOVELTY_AFTER}}` (the axis-move landed),
calibration 8→9, operability 7→8, freshness 7→8; depth, coverage and adjacency
held `9` / `7` / `8` with the no-bump rulings recorded in the round-12 table
above.
```

---

## 5. **OPTIONAL** — `LOG.md` errata line (append-only; one physical line)

If L1 files F-R12-1, the round-12 LOG entry may be followed by a second single-line bullet in the round-9 style ("corrections … supersedes two figures inside the round-9 entry above"):

```markdown
- 2026-09-28 — round 12 (erratum; supersedes one figure inside the round-11 entry above): the round-11 gate line count "936→1709 lines" is corrected to **936 → 1711** — `git show f09ff1f:grader.py | wc -l` → 1711 at the round-11 commit, while `git show 0c51208:grader.py | wc -l` → 936 confirms the before-half; the check count (280) and the selftest claim (7 scenarios S0–S6) are unaffected. Recorded at three sites so the correction is findable from each: `LOG.md:18`, `SCORECARD.md:142`, and the round-11 report — the report site is named in the errata rather than edited (append-only discipline forbids rewriting a committed report); no committed byte is edited in place (round-6 audit rule 9).
```

---

## 6. Closing — round-11 sentences deliberately NOT carried over (and why)

1. **`grader.py` "936 → 1709 lines"** — stale/wrong (the committed artifact is 1711 lines; §4c). Carried only as the erratum.
2. **`LOG.md:18`'s "1409 requests / 1473 records in 259.1 s"** and the round-11 census — r11 run bytes. r12's gate-pinned totals are 4 114 records / 4 002 calls; observed 4 114 / 4 002 / 701.6 s.
3. **The r11 result numbers as if they were the round's** (+0.352, t=+3.431, p=0.0011, CI [+0.147,+0.556], sign 26W/7L/31T, McNemar b=13 c=5 p=0.0963, 29/64 & 21/64, Brier 0.153, ack 49.1%/64.5%) — they now appear **only** where explicitly labelled `r11 comparator` or as the E2 point-match anchor. Reusing them unlabelled is the stale-count defect class the round-10 critic filed (F1).
4. **"`python3 grader.py --selftest` → S0–S6 ALL PASS"** as the current state — superseded by S0–S7 (`{{SELFTEST}}`); the r11 sentence is quoted only inside historical context.
5. **"novelty 5 → 6" / "calibration 7 → 8" / …** as live before→after pairs — those are round-11 movements; round 12's before-column is exactly those after-values (6/8/9/7/7/7/8) and the new cells are as in §4a.
6. **The r11 L2 roster and every per-agent task sentence** — replaced wholesale by the r12 roll-call (16 agents). The only reused text is the MISSION route-bucket sentence and the "no L2 wrote a shared file; single integration owner: L1" convention.
7. **r11's prior-art verdict table** — that was round 11's pricing of round-11 claims (C1 StageIF `2609.08589`, etc.). C1–C6 must be priced afresh; r11 URLs may return only as explicitly-labelled method context (Miller `2411.00640`; `2503.01747`; PR #21038).
8. **"Ack compliance: A-CKPT4710 220/448 = 49.1%, A-CKPT710 330/512 = 64.5%"** — wrong denominators for r12 (five ack cells, `A-CKPT4710-ack 212/448 = 47.3%; A-CKPT710-ack 324/512 = 63.3%; A-CKPT10-ack 440/576 = 76.4%; T-DENSE-ack 168/336 = 50.0%; T-SPARSE-ack 264/384 = 68.8%`).
9. **"route-telemetry surface … ABSENT … resolved 23:32Z … 7,226 live lines"** and the SHONEN box-3 flip narrative — round-11 events now permanent repo state. The carried element is only the *re-check* (ABSENT) and the box's own re-verified line.
10. **"41 committed pointers → BASELINE GREEN"** — r11's reviewer sweep; r12's is `BASELINE: GREEN` with its own pointer count (46 rows).
11. **"Brier 0.153" as the lane's probabilistic-forecast state** — true for r11 (3 events), but round-11 §Planned clause (b) is now fulfilled at the per-problem level; the README/SHONEN text says so with `{{E6_*}}` instead of restating 0.153 as current.
12. **The r11 §Planned target sentence as the round-12 target** — quoted once, as the target r12 *closes* (verbatim, `SCORECARD.md:181-184`); §4b replaces the section itself.



## unresolved

Every remaining placeholder is listed with its resolving command and why it is not yet resolvable. All run values (E1–E6, the five verdicts, census, arm table, ack table, finish audit, point scores) are already filled in §1b/§2c/§3/§4a above and **re-pinned verbatim to the landed `analysis_r12.md`** (md5 `ddfe60d234cae732143649abe80e1ba8`).

- `{{GRADER_LINES}}`, `{{GRADER_CHECKS}}`, `{{SELFTEST}}` — `wc -l < grader.py; python3 grader.py; python3 grader.py --selftest`. Reason: ExecutorGrader's `main` glue is mid-flight: the r12 layer is committed and *runs* (it replays four trees and emits `r12.*` checks — `CHECKS n=693 mismatches=28` at 2026-09-28 22:55, `VERDICT: FAIL`; selftest S0–S7 present, S0 control still red), so the final counts are not yet stable.
- `{{LESSON_BULLETS}}`, `{{PROVINCE_DRIFT}}` — L1's prose: `{{LESSON_BULLETS}}` from the round's own record; `{{PROVINCE_DRIFT}}` is the drift found by the §Surfaces re-verification (`test -e` + the endpoint scout capture — currently: route telemetry ABSENT, `~/wikillm/llm-wiki` absent).
- `{{AXIS_NOVELTY_AFTER}}` — L1's own scoring, `sed -n '/^## Round 12/,/^## /p' SCORECARD.md` after L1 lands the post-move table. Reason: the sole open axis judgement.
# r14 scribe drafts — bookkeeping deltas for the round-14 debt-landing

Author: `ScribeDrafts` (L2, round 14). **This file writes nothing.** Every block below
is a paste-ready delta for an **L1-owned** file (`LOG.md`, `SCORECARD.md`,
`corpus/README.md`); no L1-owned file was modified by this task.

Measured on host `linux 7.1.8-arch1-3` at cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(`git rev-parse HEAD` → `e171cdf`), 2026-09-29. Working tree at draft time:
` M SKILL.md`, ` M grader.py`, `?? corpus/evidence/round12-fleet/`, `?? corpus/evidence/round12-ladder/`,
`?? corpus/evidence/round13-ack-state/`, `?? corpus/evidence/round14-fleet/` (`git status --porcelain`).

Sources adapted: `corpus/evidence/round12-fleet/r12-log-final.md` and
`corpus/evidence/round12-fleet/r12-doc-deltas-final.md` (round 12's own drafts, which never landed).
Every value carried into those drafts as a `{{PLACEHOLDER}}` is now resolved below and re-measured;
every value that could not be re-measured is flagged in §5/§6 rather than filled.

---

## 0. Pre-landing state (all values measured, 2026-09-29)

| Quantity | Value now | Command |
|---|---:|---|
| `LOG.md` lines (round-11 entry is line 18) | 18 | `wc -l < LOG.md` |
| `grader.py` lines / checks / selftest | 5734 / **732** / S0–S7 `ALL PASS` | `wc -l < grader.py`; `python3 grader.py`; `python3 grader.py --selftest` |
| `SKILL.md` lines / anti-patterns / measurement rules / cited-source bullets | 577 / 19 / 13 / 23 | `wc -l < SKILL.md`; `awk 'NR>=48 && NR<166' SKILL.md \| grep -cE '^[0-9]+\. '`; `awk '/^## Planning-horizon/,/^## Hermetic grader/' SKILL.md \| grep -cE '^[0-9]+\. '`; `awk '/^## Cited local sources/,0' SKILL.md \| grep -cE '^- '` |
| knowledge rows / files | 22 / 22 | `grep -c '^\| `knowledge/' corpus/README.md` = `ls corpus/knowledge \| wc -l` |
| lessons rows / files | **13 / 14** ⇒ 1 unindexed (`lessons/round-9-aggregator-corpus-verdict.md`) | `grep -c '^\| `lessons/' corpus/README.md`; `ls corpus/lessons \| wc -l` |
| evidence rows / dirs | **6 / 10** | `grep -c '^\| `evidence/' corpus/README.md`; `ls -d corpus/evidence/*/ \| wc -l` |
| `round12-ladder/` files | **18** (not 17) | `ls corpus/evidence/round12-ladder \| wc -l` |
| `round12-fleet/` files | **22** (not 21) | `ls corpus/evidence/round12-fleet \| wc -l` |
| `round13-ack-state/` files | 2 | `ls corpus/evidence/round13-ack-state \| wc -l` |
| `round14-fleet/` files | created this round (`drafts/`) | `ls -d corpus/evidence/round14-fleet/` |

Post-landing targets used in the count checks below: knowledge **23 = 23**, lessons **17 = 17**,
evidence **10 = 10**.

---

## 1. `LOG.md` entries

Each block is **ONE physical line** (`awk 'NR==19' LOG.md | wc -l` → 1, and likewise 20/21), matching
`LOG.md:17-18`. Append in order after line 18.

### 1a. Round 12 — append as `LOG.md:19`

```markdown
- 2026-09-28 — round 12 (evidence committed in round 14): **novelty axis-move** — powered, preregistered, prior-art-priced **four-point emission-granularity ladder** + **batching dissociation** + **second task family (transport)** + **per-problem probabilistic forecasts**; closes the round-11 §Planned target (`SCORECARD.md:163-184`). Evidence: **(a) design hashed BEFORE any request** — bundle `corpus/evidence/round12-ladder/prereg-bundle.sha256` (9 files; probe_plan_r12 `0efa130a…`, power_analysis_r12 `15cd40e8…`, predictions-r12 `d76dfe12…`) at `ordering.log` pre/post-hash **`2026-09-29T01:16:08Z` / `2026-09-29T01:16:08Z`**; run scripts hashed post-fix **`2026-09-29T01:16:08Z`** (probe_r12.py `1871697f…`, run_r12.py `3beb91ea…`); first `request_ts` **`2026-09-29T01:19:59Z`**, last `request_ts` `01:31:41Z`, landing `01:32:44Z`. **(b) run bytes** — `results-r12.jsonl` (md5 `9dd8aa2b6a7aa7890aa802c37d5af0f9`, 4 114 records: `2 descriptors, 64 meta, 48 meta2, 1328 graded, 2256 ack, 416 fillers, 0 error records`), `run.log` (md5 `700d1ddd2ece50d7bdedd55859c59f3a`, `wall_total_s: 701.6`, seven cell lines `A-INC: 48/64 … T-SPARSE: 2/48`), 4 002 HTTP calls (4 000 `chat/completions` + 2 `/v1/models`). **(c) five mechanical verdicts** (`analysis_r12.md`, produced by `recompute_r12.py`, whose own selftest is 165/165 PASS): `LADDER ESTABLISHED` (E1 `E1 Page trend: L=1773.0 E_L=1600.0 var_L=335.000 z=+9.452 two-sided p=0.0000 direction=increasing`), `REPEATS-r11; additionally POINT-MATCHES-r11 (|diff - 0.352| = 0.055 <= 0.15)` (E2 `+0.297` sd 0.754 n=64 t=+3.148 p=0.0025 CI [0.108, 0.485] sign 24/7/33 p=0.0033; r11 comparator +0.352 p=0.0011), `DISSOCIATION ESTABLISHED` (E4 `+0.656` sd 1.158 t=+4.535 p=0.0000 W/L/T=34/8/22), `TRANSPORT DIRECTIONAL` (E5 `+0.177` sd 1.069 n=48 t=+1.147 p=0.2571 — family 2 landed at a floor `2/48` both arms, an honest negative), `FORECAST SKILLED` (E6 `pass=416 sign=304 runlevel=7 total=727`; pooled Brier `0.1288` N=416, BSS `+0.0447` [persistence + arm-rate transport; family1-replicate +0.4751 / family1-novel +0.0173 / family2 -3.1474], calibration slope `+0.8427` intercept `-0.7511`). **(d) per-arm** A-INC 48/64, A-CKPT4710 28/64, A-CKPT710 21/64, A-CKPT10 10/64, A-MONO 2/64, T-DENSE 2/48, T-SPARSE 2/48; ack labels `A-CKPT4710-ack 212/448 = 47.3%; A-CKPT710-ack 324/512 = 63.3%; A-CKPT10-ack 440/576 = 76.4%; T-DENSE-ack 168/336 = 50.0%; T-SPARSE-ack 264/384 = 68.8%` — **label-wide** counts, not ack-only (round 13 shows the denominator mixes prompt intents); finish audit `finish=length 0/1328, parse fail 0/1328`; `Excluded pids: family1 none family2 none` (floors 44/44 never fired). **(e) prior art priced with fetched URLs** — C1/C2/C6 INCREMENTAL, **C3 NOVEL-instrument** (required negative-search log), C4/C5 INCREMENTAL (`r12-prior-art-ladder.md`: 56 URLs fetched, 53×200, 3 failures; `r12-prior-art-transport.md`: 45 works / 52 URL rows, all 200) — phenomenon-new 0 / instrument-new 1. **(f) gate extended in the same round the bytes landed** — `grader.py` 280 → **732** checks (452 in the r12 layer), four trees (r8/r9/r11/r12), `--selftest` S0–S7 ALL PASS, exit 0 (re-measured 2026-09-29); mutation battery 18/18 KILLED, 0 survivors, M0 instrument control KILLED (`r12-mutation.md`); reviewer `BASELINE: GREEN` (41 committed pointers, `r12-review-baseline.md`); connector `DUPLICATE-INSTRUMENT RISK: NONE` (`r12-connector.md`); endpoint scout `GO`, 6× `NO-DRIFT` (`r12-endpoint-freshness.md`). **(g) 16 L2 agents**, every artifact committed verbatim under `corpus/evidence/round12-fleet/` (22 files); `SCOPE VERDICT: VIOLATION (1)` — the endpoint scout self-documented two bounded read-only metadata `GET`s to `:34113` (`r12-scope-audit.md`); the design critic landed `DO-NOT-RUN` (1 FATAL / 5 MAJOR / 4 MINOR) **before any bundle hash existed**, so all defects were absorbed as hashed v1 and there is no v2 chain. **Not delivered**: `r12-critic-landed.md` — the promised fresh-implementation re-derivation of the landed numbers was never filed (`test -e corpus/evidence/round12-fleet/r12-critic-landed.md` → absent; the r12 report's `{{CRITIC_LANDED_VERDICT}}` placeholder is therefore permanently open). Confidence for the landed numbers rides on the promoted engine (165/165 selftest), the 732-check gate replay, and the round-14 independent re-measurement — not on a fresh implementation.
```

### 1b. Round 13 — append as `LOG.md:20`

```markdown
- 2026-09-28 — round 13: **ack-state measurement audit (hermetic — no endpoint, no probe)** — two stdlib scripts landed under `corpus/evidence/round13-ack-state/` re-derive the prompt-intent denominators behind the r9/r11/r12 `-ack` metrics from committed bytes alone. Evidence: **(a)** `audit_ack_schedule.py` (`--selftest` 4/4 PASS, exit 0) derives true ack-only turns from each runner's checkpoint schedule (`run_r9.py:16,26-28`; `run_r11.py:61,76-80`) and reports, per round: r9 `A-CKPT4710-ack` 32/32 = 100.0% prefix `ok` and 32/32 = 100.0% bare vs 32/56 = 57.1% label-wide, r9 `A-CKPT710-ack` 48/48 = 100.0% / 48/48 = 100.0% vs 48/64 = 75.0%; r11 `A-CKPT4710-ack` 220/256 = 85.9% prefix / 216/256 = 84.4% bare vs 220/448 = 49.1% label-wide, r11 `A-CKPT710-ack` 330/384 = 85.9% / 324/384 = 84.4% vs 330/512 = 64.5%; inputs pinned by sha256 (r9 `c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb`, r11 `918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad`). **(b)** `analyze_ack_state.py` (`--selftest` 8/8 PASS, exit 0) scores r11 `A-CKPT710-ack` against simulator truth: 512 label rows = 384 true ack-only (turns 2–6, 9) + 128 full-state-ask controls (turns 1, 8) logged under the same label; 330/384 raw replies start with `ok`, 324/384 are exactly bare `ok`, 18/384 carry a parseable state equal to that turn's truth, 54/384 raws contain `{` across 9/64 pids and 5/64 pids have ≥1 exact ack-only snapshot. **(c) finding (falsifies the label's reading, not the bytes)**: the `-ack` label is a storage label, not prompt intent — the published label-wide prefix figure understates true ack-only compliance by ~7× on r11 (64.5% label vs 85.9% true ack-only). The r12 ack table has the same denominator class and must be read as label-wide. **(d) bounded, not laundered**: exact-state emissions are bounded [0.047, 0.125] across all 384 ack-only prompts because 30/54 brace-bearing raws hit the runner's 80-char raw clip (`run_r11.py:74`) and 6 uncapped non-bare raws stay unparsed — capped/unparseable is `unresolved`, never counted as a model failure. No endpoint traffic; both scripts read only committed bytes.
```

### 1c. Round 14 — append as `LOG.md:21`

```markdown
- 2026-09-29 — round 14: **debt-landing + independent-verification round** — the round-12 ladder/fleet and round-13 ack-state evidence, found by the aggregator sitting untracked for a full round (an r8-style landing debt), is committed, indexed, logged and independently re-measured so the r12 novelty claim is durable in-repo. Evidence: **(a) gate** — `python3 grader.py` → `CHECKS n=732 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline`, exit 0; `python3 grader.py --selftest` → S0–S7 `ALL PASS`, exit 0 (re-measured 2026-09-29; the r12 report's own falsifiable-target clause 3, "NOT MET as of writing", is now MET). **(b) independent re-derivation** — `recompute_r12.py --selftest` → `SELFTEST 165/165 PASS` (supersedes `r12-mutation.md`'s "promoted engine fails its own selftest" on the pre-repair draft); `audit_ack_schedule.py --selftest` 4/4 and `analyze_ack_state.py --selftest` 8/8; the landed run bytes re-pin at md5 `9dd8aa2b…` / `700d1ddd…`. **(c) landed & indexed** — `corpus/evidence/round12-ladder/` (18 files), `round12-fleet/` (22), `round13-ack-state/` (2), `round14-fleet/` (this round's L2 artifacts); corpus/README.md index both directions equal after landing — evidence rows 6 → 10 = 10 dirs, knowledge 23 = 23, lessons 17 = 17 (the standing 14th-file gap, `lessons/round-9-aggregator-corpus-verdict.md`, committed `e171cdf` without a row, is closed with an index row per the round-6 convention: this lane writes only the row); `SKILL.md` (+59 lines: anti-patterns **16–19**, measurement rules **11–12**) and the 4 027-line `grader.py` extension are now tracked. **(d) errata filed, not patched in place** — (1) the `analysis_r12.md` md5 stored in three round-12 artifacts (`ddfe60d2…`) does not match the landed bytes (**`029c3bcdcf11209d575734742bf239f6`**, sha256 `1ceebd75…`), and the gate pins only `r12_jsonl`/`r12_runlog`, never `analysis_r12.md`, so nothing caught it; (2) `r12-critic-landed.md` was never delivered; (3) round 11's published `grader.py` "936 → 1709 lines" is **936 → 1711** (`git show f09ff1f:grader.py \| wc -l` → 1711); (4) regeneration of `analysis_r12.md` in-repo is **not** byte-identical (a lone `Generator source:` path line is directory-dependent — the landed bytes embed `/home/vgpnk/projects/…`, a path that does not exist on this host). **(e) axes** — novelty **6 → 7** (all three rubric legs: constructs unobservable before r12 are now measured — full four-arm ordered ladder direction, batching/emission dissociation, second-family transport; instrument inspectable in-repo — `probe_r12.py`/`run_r12.py`/`recompute_r12.py`/`predict_r12.py` plus 452 gate checks; every claim priced with fetched URLs); calibration **holds at 8 with the breach recorded** — the bytes sat uncommitted a full round, so rubric (d) ("every probe analyzed, indexed and logged in the round it ran") was violated and is **not** laundered back by landing late; operability 7 → 8 (the r12 gate extension is verified green); coverage, freshness, depth and adjacency held (rulings in `SCORECARD.md` §Round 12-13).
```

---

## 2. `SCORECARD.md` deltas

### 2a. New section — paste after the round-11 post-move table (before `## Scoring rubric`, `SCORECARD.md:148`)

Column style copied from `## Round 11 — post-move` (`SCORECARD.md:136-147`): `| Axis | Before → After | What moved | Evidence |`.
Before-column = the round-11 post-move anchors (novelty 6, calibration 8, depth 9, coverage 7, operability 7, freshness 7, adjacency 8).

```markdown
## Round 12-13 — landed in round 14 (debt-landing)

The round-12 ladder/fleet and round-13 ack-state evidence was produced, analyzed and
self-verified but **never committed**; round 14 lands it, re-measures every headline number
from the committed bytes, and indexes it. The table records the movement those rounds earned
as it becomes durable in-repo; the before-column is the round-11 post-move anchor set.

| Axis | Before → After | What moved | Evidence |
|---|---|---|---|
| **novelty** *(owned)* | 6 → **7** | All three rubric legs fire. (i) *New constructs measured*: a full four-arm ordered emission-density ladder (Page's test on within-block ranks, one confirmatory p), a batching/emission **dissociation** that decomposes r8's `A-MONO 0/10`, and the same contrast **transported** to a second task family (positional token-sequence editing) — none of the three was observable before r12. (ii) *Instrument inspectable in-repo*: `probe_r12.py` (sha256 `1871697f…`), `run_r12.py` (`3beb91ea…`), `recompute_r12.py` (selftest 165/165), `predict_r12.py`, a 9-file hashed bundle, and 452 new gate checks replaying the tree offline. (iii) *Prior-art verdict with a fetched URL per claim*: C1/C2/C6 INCREMENTAL, C4/C5 INCREMENTAL, **C3 NOVEL-instrument** with its required negative search. **Ceiling**: one served sub-3-bit unit (descriptors-pinned, no cross-model claim); the family-2 leg landed at a floor (`2/48` both arms) and `TRANSPORT DIRECTIONAL` is read as a floor, not as positive transport; phenomenon-new 0 / instrument-new 1. | `analysis_r12.md` (R1–R5); `r12-prior-art-{ladder,transport}.md` |
| **calibration** *(owned)* | 8 → **8 (held — breach recorded)** | The loop ran correctly *inside* r12 (predictions filed pre-request and scored at close: 416 per-problem pass events, Brier `0.1288`, BSS `+0.0447`, slope `+0.8427`; C2's point prediction `+0.3520 → +0.297`, abs err `0.055`) — but rubric clause (d) is "every probe analyzed, indexed and logged **in the round it ran**", and these artifacts sat untracked in the working tree for a full round. The cap is named honestly rather than paid off by landing late: **no +1**. Round-13's audit additionally found that the published r12 ack table is a storage-label figure (see below), a second reason the round's self-description is not scored as clean. | this file; `r12-log-final.md` (drafted, unlanded); `r14-scribe-drafts.md` §5 F-1/F-2 |
| **operability** | 7 → **8** | The gate was extended **in the same round the bytes landed** (round-11 §Planned clause (d)) and is verified green at landing: `grader.py` 280 → **732** checks, 4 trees (r8/r9/r11/r12), `--selftest` S0–S7 `ALL PASS`, exit 0; 18/18 mutation-battery scenarios KILLED with the M0 instrument control also KILLED. | `grader.py`; `r12-mutation.md` |
| **coverage** | 7 → **7 (held at draft time; +1 earned by the index landing)** | Held pending the README index, which this landing writes: evidence rows 6 → 10 = 10 dirs, knowledge 23 = 23, lessons 17 = 17 (closing the standing 14th-file gap with a row, not a commit). The cap still applies — the route-telemetry surface is **ABSENT** (`test -e ~/Projects/bounties/ledger/telemetry.jsonl` → absent), so the **declared-but-unresolvable-surface** clause blocks 10 but not this +1. Flip condition: `grep -c '^\| \`lessons/' corpus/README.md` = `ls corpus/lessons \| wc -l` = 17 **and** `grep -c '^\| \`evidence/' corpus/README.md` = `ls -d corpus/evidence/*/ \| wc -l` = 10. | `corpus/README.md` index; `PROVINCE.md` §Surfaces |
| **freshness** | 7 → **7 (held)** | Every claim the landed set touches already carried an in-band re-verification from its own round (r12 `descriptors` re-pin of pid 1299 + 41-token argv + q4_0 KV; endpoint scout `GO` with 6× `NO-DRIFT`; reviewer `BASELINE: GREEN`, strict citation resolution 9/10 = 90% on a fixed 10-bullet sample). No **new** re-verification line is authored by the landing itself, so no bump. | `r12-endpoint-freshness.md`; `r12-review-baseline.md` |
| **adjacency** | 8 → **8 (held)** | The connector re-verified the standing r10/r11 no-duplicate rulings at current sibling HEADs (`DUPLICATE-INSTRUMENT RISK: NONE`; five sibling repos, exact greps, nothing operating a hashed preregistration / per-problem Brier scoring / evidence-replay gate). Report-outs were filed, not absorbed (protocol, kotoba, integrator/serving plane, kasegi). No new integrator arbitration — which is the adjacency cap. | `r12-connector.md`; `PROVINCE.md` tail |
| depth | 9 → **9 (held — anti-double-count)** | `SKILL.md` grew 518 → **577** lines (anti-patterns 15 → **19**, measurement rules 10 → **13**), but those bytes document *this* round's own artifact; counting them under depth too would reward one landing twice. Bump only for new sourced claims beyond the probe bytes. | `SKILL.md`; rubric anti-double-count ruling |

Pre-move anchors (round-11 §Round-11 post-move): novelty 6, calibration 8, depth 9, coverage 7,
operability 7, freshness 7, adjacency 8. All cells above the pre-move line are the scribe's
rubric-derived reading of the committed evidence named beside each; the **novelty** cell is the
axis-move judgement and remains L1's to confirm or overturn.
```

### 2b. New section — paste immediately after 2a (still before `## Scoring rubric`)

```markdown
## Round 14 — landing round

| Axis | Before → After | What moved | Evidence |
|---|---|---|---|
| **novelty** *(owned)* | 7 → **7 (held)** | The round commits and re-measures; it measures no new construct. Landing is durability, not novelty. | this table; `r14-scribe-drafts.md` §0 |
| **calibration** *(owned)* | 8 → **8 (held)** | The debt is paid, but paying it late does not restore rubric (d) for rounds 12–13, and the landing found four open instrument defects (stale `analysis_r12.md` md5, missing `r12-critic-landed.md`, directory-dependent regeneration, unpinned analysis file). A +1 here would launder exactly the behaviour the rubric exists to penalise. **Ceiling:** until the analysis-file pin is added to the gate, the corpus cannot detect a silent analysis regeneration. | §Round 12-13 above; `r14-scribe-drafts.md` §5 |
| **operability** | 8 → **8 (held)** | No gate change this round; the extension verified here (732 checks, S0–S7, exit 0) was earned in round 12. | `python3 grader.py`; `python3 grader.py --selftest` |
| **coverage** | 7 → **8 (CONDITIONAL — hold unless the index is landed and audited)** | The +1 leg is the index landing: rows = files in all three namespaces after this commit (evidence 10 = 10, knowledge 23 = 23, lessons 17 = 17), plus a `lessons/` row for the aggregator-committed 14th file and an evidence section covering all four newly-landed dirs. **Default per the round-14 gate ruling is HOLD** — the uncommitted evidence alone earns nothing; credit only once the README/index parity is actually present in the landing commit. **Capped below 10** by the declared-but-unresolvable route-telemetry surface. Flip condition (verify at land time): `grep -c '^\| \`evidence/' corpus/README.md` = `ls -d corpus/evidence/*/ \| wc -l` = 10 **and** knowledge 23 = 23 **and** lessons 17 = 17. | `corpus/README.md` §What's here / §`evidence/`; `PROVINCE.md` §Surfaces |
| **freshness** | 7 → **8 (CONDITIONAL — hold unless the LOG re-verification entry is committed)** | The +1 clause is "each round's `LOG.md` entry carries a re-verification result for the claims it touched"; §1a–1c above supply exactly that (commands, md5/sha256 pins, re-measured gate/selftest outputs) and §5 records the four open defects instead of smoothing them. **Default per the round-14 gate ruling is HOLD** — the entry must be *committed*, not merely drafted, before the cell moves. | `LOG.md` round 14; `r14-scribe-drafts.md` §5 |
| **adjacency** | 8 → **8 (held)** | No cross-domain evidence changed hands this round; the standing report-out owners are unchanged and the r12 `SCOPE VERDICT: VIOLATION (1)` (two read-only metadata `GET`s by an L2 endpoint scout) is disclosed in the round-12 entry instead of absorbed. | `r12-scope-audit.md`; `LOG.md` round 12 |
| depth | 9 → **9 (held)** | No sourced content beyond the landed artifacts. | `SKILL.md`; rubric |

Projected floor after this round is **coverage-driven**: with coverage at 8 and novelty at 7,
the lowest axis is **novelty (7)** — the round-12 §Planned surface-completeness move is still
available, and the anti-double-count ruling there (new sourced claims may bump depth **or**
coverage, never both) still holds.

**Round-14 gate ruling carried verbatim (cross-check, not our judgement).** `LandingGate`
(`corpus/evidence/round14-fleet/r14-landing-gate.md`): *"There is no existing r14 plan doc/§Planned
to cite; the only current planned section is round-11's stale r12 target. … For an r14 scorecard,
this gate adjudicates only novelty 6→7. Do not credit freshness or coverage from the uncommitted
evidence alone: freshness requires the round's LOG re-verification entry; coverage requires
README/index parity after landing. Hold other axes unless those required landing artifacts are
actually present and audited."* Accord: §2a/§2b hold calibration, depth and adjacency unconditionally;
coverage and freshness are held by **default** in §2b and move only on the named verification
commands passing against the landing commit; novelty 6 → 7 is the one cell this gate adjudicates.
```

### 2c. OPTIONAL — append one movement line to `## Retired` (`SCORECARD.md:186-194`)

```markdown
Round 12-13 movement (landed round 14): novelty 6→7, operability 7→8; calibration held at 8
with the uncommitted-round breach recorded, coverage held pending the index then 7→8 at landing,
freshness held at 7 then 7→8 for the landing's own re-verification line; depth, coverage (in
r12-13) and adjacency held with the no-bump rulings above.
```

---

## 3. `corpus/README.md` deltas

### 3a. `### \`evidence/\`` table — four new rows (append after the existing six rows, `corpus/README.md:48-62`)

```markdown
| `evidence/round12-ladder/` | preregistration bundle (`probe_plan_r12.md` sha256 `0efa130a…`, `power_analysis_r12.md` `15cd40e8…`, `predictions-r12.md` `d76dfe12…`, `predictions-r12-perproblem.jsonl` (416), `predictions-r12-signevents.jsonl` (304), `prereg-bundle.sha256`, `ordering.log`, `prereg-precheck.log` (23 `[PASS]`)), probe machinery + runners (`probe_r12.py` `1871697f…`, `run_r12.py` `3beb91ea…`, `predict_r12.py`, `power_r12.py`, `precheck_r12.py`), run bytes (`results-r12.jsonl` md5 `9dd8aa2b6a7aa7890aa802c37d5af0f9`, 4 114 records; `run.log` md5 `700d1ddd2ece50d7bdedd55859c59f3a`, `wall_total_s: 701.6`), generated `analysis_r12.md` (md5 `029c3bcdcf11209d575734742bf239f6`; census `2 descriptors, 64 meta, 48 meta2, 1328 graded, 2256 ack, 416 fillers, 0 error records`; verdicts R1–R5) + `recompute-run.log`, promoted `recompute_r12.py` (selftest 165/165) — 18 files | `corpus/evidence/round12-ladder/`, run 2026-09-29T01:19:59Z–01:31:41Z (landed 01:32:44Z) |
| `evidence/round12-fleet/` | 16-agent L2 fleet, artifacts committed verbatim: `r12-critic-design.md` (`DO-NOT-RUN`, 1 FATAL / 5 MAJOR / 4 MINOR; absorbed pre-hash), `r12-prior-art-ladder.md` / `r12-prior-art-transport.md` (pricing C1–C6 with fetched URLs), `r12-endpoint-freshness.md` (`GO`, 6× `NO-DRIFT`; closes the r10 gguf-size open item with residual 0), `r12-connector.md` (`DUPLICATE-INSTRUMENT RISK: NONE`), `r12-review-baseline.md` (`BASELINE: GREEN`, 41 pointers), `r12-review-citations.md` (`CITATION RESOLUTION: 98.9% strict / 100.0% lenient, 0 broken`), `r12-scope-audit.md` (`SCOPE VERDICT: VIOLATION (1)`), `r12-mutation.md` (18/18 KILLED, M0 control KILLED), `r12-mock-smoke.md` + `mock_server_r12.py`, `r12-recompute-notes.md`, `r12-grader-notes.md` + `grader_r12_draft.py`, `recompute_r12_draft.py`, wave drafts (`r12-report-draft.md`, `r12-log-draft.md`, `r12-doc-deltas.md`, finals), `INTEGRATOR-NOTES.md` (20 binding adjudications, L1 self-found defects incl. the 448→416 E6 denominator, the carried r11 1709→1711 erratum) — 22 files. **Not present**: `r12-critic-landed.md` (never delivered). | `corpus/evidence/round12-fleet/`, round 12 |
| `evidence/round13-ack-state/` | two hermetic ack-state audit scripts, no run bytes: `audit_ack_schedule.py` (selftest 4/4 PASS) derives true ack-only turns per round from the runners' checkpoint schedules and contrasts label-wide vs ack-only prefix/bare counts; `analyze_ack_state.py` (selftest 8/8 PASS) scores r11 `A-CKPT710-ack` against simulator truth (384 true ack-only rows; 330/384 prefix `ok`, 324/384 bare, 18/384 exact-state) — 2 files, read-only over committed bytes | `corpus/evidence/round13-ack-state/`, round 13 |
| `evidence/round14-fleet/` | round-14 landing/verification L2 artifacts (bookkeeping drafts + independent re-derivations); filenames follow the `r14-*` convention | `corpus/evidence/round14-fleet/`, round 14 |
```

(Count check after pasting: `grep -c '^\| \`evidence/' corpus/README.md` must equal `ls -d corpus/evidence/*/ | wc -l` → **10 = 10**.)

### 3b. Main table — one new knowledge row (append at the end of the knowledge block, after `knowledge/bench-arena-round11-power.md`)

The knowledge entry itself (`corpus/knowledge/bench-arena-round12-ladder.md`) must be written by L1; this is only its index row.

```markdown
| `knowledge/bench-arena-round12-ladder.md` | Four-point emission-granularity ladder + batching dissociation + transport to a second task family + per-problem probabilistic forecasts: verdicts `LADDER ESTABLISHED` (E1 `E1 Page trend: L=1773.0 E_L=1600.0 var_L=335.000 z=+9.452 two-sided p=0.0000 direction=increasing`) / `REPEATS-r11; additionally POINT-MATCHES-r11 (\|diff - 0.352\| = 0.055 <= 0.15)` (E2 `+0.297`) / `DISSOCIATION ESTABLISHED` (E4 `+0.656`) / `TRANSPORT DIRECTIONAL` (E5 `+0.177`, n=48; family 2 at a floor `2/48` both arms — honest negative) / `FORECAST SKILLED` (E6 `pass=416`, Brier `0.1288`, BSS `+0.0447`, slope `+0.8427`); prior art C1/C2/C4/C5/C6 INCREMENTAL, C3 NOVEL-instrument | `corpus/evidence/round12-ladder/` (4 114 records, bundle `prereg-bundle.sha256`, verdicts in `analysis_r12.md`), run 2026-09-29 |
```

(Count check after pasting: knowledge `grep -c '^\| \`knowledge/' corpus/README.md` = `ls corpus/knowledge | wc -l` → **23 = 23**.)

### 3c. Main table — four new lessons rows (append at the end of the lessons block, before `### \`evidence/\``)

The three `lessons/round-1{2,3,4}.md` files must be written by L1; these are only the index rows. The fourth row closes a **standing gap** and writes no file (aggregator-owned, round-6 convention).

```markdown
| `lessons/round-12.md` | Legs of a ladder claim: an ordered alternative needs an ordered test, and the four-arm spread is only the ladder if the *direction* is signed — a Page test on within-block ranks, not three adjacent contrasts. A within-run re-measurement on identical problems/seeds is **repeatability**, never replication — the label is part of the claim. An arm that differs from its comparator on two axes decomposes a confound but cannot name a mechanism. A transported contrast across two severity scales is a **ratio-only** report, never pooled. A floor is reported as filed — the family-2 arm landed 2/48 both ways and the transported-base-rate null was falsified, which *damaged* the BSS and must be said so. A promoter that regenerates a derived artifact must be re-run and re-pinned after the last edit (see `lessons/round-14.md`). | LOG.md round 12, `corpus/evidence/round12-{ladder,fleet}/` |
| `lessons/round-13.md` | A storage label is not a prompt intent: `-ack` rows mixed ack-only turns with full-state-ask turns, and the published label-wide prefix figure understated true ack-only compliance ~7× on r11 (64.5% label vs 85.9% true). Any compliance metric must name its denominator's *intent*, not its storage bucket. A capped capture bounds the answer instead of answering it — report the bound and count `unresolved` separately from failure. | LOG.md round 13, `corpus/evidence/round13-ack-state/` |
| `lessons/round-14.md` | Uncommitted is unlanded: evidence that is analyzed and self-verified but never committed, indexed or logged spends a full round as a claim no gate can see — and the rubric's in-round clause is violated by lateness, not excused by it. A derived artifact's md5 must be pinned by the gate or it will drift silently (three different md5s were recorded for `analysis_r12.md` across one round's paper trail). A generator that embeds its own path is not byte-reproducible outside the directory that produced it. A promised verification artifact that is never filed leaves a permanent hole in the confidence chain — name it, do not let the placeholder resolve itself. | LOG.md round 14, `corpus/evidence/round14-fleet/` |
| `lessons/round-9-aggregator-corpus-verdict.md` | Aggregator corpus-verdict lesson (rule-10 re-emitted at `f09ff1f`, canonical-form + rule-8 literal findings, routed rows); **aggregator-owned file, committed by the aggregator in `e171cdf` — this lane writes only this index row**, closing the standing 14th-file gap (round-6 convention) | aggregator lane (non-author), committed `e171cdf` |
```

(Count check after pasting: `grep -c '^\| \`lessons/' corpus/README.md` = `ls corpus/lessons | wc -l` → **17 = 17**.)

### 3d. Coverage map — replace the `Multi-turn state tracking` bullet (`corpus/README.md:91`)

```markdown
- **Multi-turn state tracking / planning horizon**: instrument built (r8, 3 probes), replicated on fresh seeds (r9), severity dose ESTABLISHED at preregistered power (r11, paired diff +0.352, p=0.0011), then extended at r12 to a **four-point density ladder** — `LADDER ESTABLISHED` (E1 `E1 Page trend: L=1773.0 E_L=1600.0 var_L=335.000 z=+9.452 two-sided p=0.0000 direction=increasing`), within-run repeatability `REPEATS-r11; additionally POINT-MATCHES-r11 (|diff - 0.352| = 0.055 <= 0.15)` (E2 `+0.297`), batching dissociation of r8's MONO collapse `DISSOCIATION ESTABLISHED` (E4 `+0.656`), transport to a token-sequence family `TRANSPORT DIRECTIONAL` (E5 `+0.177` on n `48`; family 2 landed at a floor `2/48` both arms — an honest negative), per-problem forecast skill `FORECAST SKILLED` (416 pass events, Brier `0.1288`, BSS `+0.0447`, calibration slope `+0.8427`) — `knowledge/bench-arena-round12-ladder.md`. Still open: probe B with a binding manipulation, probe C at n≥12, the r8 arithmetic covariate.
```

Also replace the `Novelty pricing` bullet (`corpus/README.md:92`) with:

```markdown
- **Novelty pricing**: r9 4/4 findings priced; r11 C1–C4 + M1–M3 priced with fetched URLs; r12 prices C1–C6 + method items — C1/C2/C4/C5/C6 INCREMENTAL, **C3 NOVEL-instrument** (negative search required and filed), phenomenon-new 0 / instrument-new 1 (`evidence/round12-fleet/r12-prior-art-{ladder,transport}.md`; `knowledge/eval-prior-art-calibration.md`).
```

### 3e. Open gaps — replace/add lines (`corpus/README.md:95-105`)

Replace the `Probabilistic forecasts` and `No in-repo gate` bullets, keep the rest, and append three new lines:

```markdown
- **Probabilistic forecasts**: CLOSED round 11 at the event level (3 predictions, Brier 0.153) and **CLOSED round 12 at the per-problem level** — `416` pass events filed before the first request and scored at close, pooled Brier `0.1288`, BSS vs arm climatology `+0.0447` (family1-replicate `+0.4751` / family1-novel `+0.0173` / family2 `-3.1474`), calibration slope `+0.8427`; caveat: this is *persistence* skill on the same problems, and the family-2 transported base rate was falsified by the floor. See `knowledge/bench-arena-round12-ladder.md`.
- **No in-repo gate**: CLOSED round 10 (`grader.py`, exit 0/1/2); extended in-round at r11 (280 checks, three trees, S0–S6) and again at r12 (**732** checks, four trees r8/r9/r11/r12, `--selftest` S0–S7 `ALL PASS`, exit 0; plus an 18/18-KILLED mutation battery with its M0 instrument control). The gate does **not** pin `analysis_r12.md` — see the line below.
- **Derived-artifact pinning** (new, round 14): `analysis_r12.md` is unpinned by the gate while three round-12 artifacts store md5 `ddfe60d2…` against landed bytes `029c3bcd…`; regenerating it in-repo also changes one `Generator source:` path line, so the file is not byte-reproducible outside the directory that produced it. Open until the pin is added (recorded, not patched).
- **r12 adversarial re-derivation** (new, round 14): `r12-critic-landed.md` was never delivered, so the round-12 confidence chain rests on the promoted engine (selftest 165/165), the 732-check gate and the round-14 re-measurement rather than on a fresh independent implementation. Recorded as a permanent hole, not silently resolved.
- **Ack metric denominators** (new, round 13/14): every `-ack` figure published so far (r9/r11/r12) is label-wide and mixes ack-only with full-state-ask turns; the true ack-only rate is ~85.9% prefix / 84.4% bare on r11 (`corpus/evidence/round13-ack-state/`). Any future ack number must state its denominator's intent.
- **Prior-art digest queue**: STILL OPEN — Laban et al. ICLR 2026 (`arxiv.org/abs/2505.06120`), Lanham et al. (`arxiv.org/abs/2307.13702`), llama.cpp #7052 named in `knowledge/eval-prior-art-calibration.md` and still unread as digests; carried unchanged as the named coverage candidate.
```

---

## 4. Verbatim quote register (every number above, against its stored line)

All rows below were produced by `python3 -c` substring tests against the named committed file
(`analysis_r12.md` for E-lines/verdicts/census/ack, `run.log` for the SUMMARY, the two round-13
scripts' own stdout for their tables). This register is the quote-check for §1–§3: no number in the
drafts above is rendered differently from its source.

**`corpus/evidence/round12-ladder/analysis_r12.md`** (md5 `029c3bcdcf11209d575734742bf239f6`):

```text
results-r12.jsonl contains 2 descriptors, 64 meta, 48 meta2, 1328 graded, 2256 ack, 416 fillers, 0 error records
E1 Page trend: L=1773.0 E_L=1600.0 var_L=335.000 z=+9.452 two-sided p=0.0000 direction=increasing
E2 paired diff (710 - 4710, {7,10}): +0.297 sd 0.754 n=64
E2 paired t: t=+3.148, df=63, two-sided p=0.0025
E2 95% CI: [0.108, 0.485]
E2 exact sign: wins=24 losses=7 ties=33 two-sided p=0.0033 direction=+1
E2 McNemar final passes: b=12 c=5 two-sided p=0.1435
E3 adjacent gaps: 4710-INC {4,7,10} +0.438 p=0.0000; 710-4710 {7,10} +0.297 p=0.0025; 10-710 {10} +0.547 p=0.0000
E4 batching diff (MONO - CKPT10, final): +0.656 sd 1.158 n=64 t=+4.535 p=0.0000 sign W/L/T=34/8/22
E5 transport diff (SPARSE - DENSE, {7,10}): +0.177 sd 1.069 n=48 t=+1.147 p=0.2571 sign W/L/T=22/16/10
E6 events: pass=416 sign=304 runlevel=7 total=727 (excluded pids dropped from score and climatology)
E6 Brier pass: pooled=0.1288 (N=416); per-arm A-INC=0.1959 A-CKPT4710=0.1294 A-CKPT710=0.1155 A-CKPT10=0.0743 A-MONO=0.0734 T-DENSE=0.2092 T-SPARSE=0.1220
E6 BSS pass vs arm climatology: pooled=+0.0447 [persistence + arm-rate transport]; family1-replicate=+0.4751 (N=128); family1-novel=+0.0173 (N=192); family2=-3.1474 (N=96)
E6 calibration (pass events): slope=+0.8427 intercept=-0.7511 (damped Newton on logit(p) clipped to [1e-06, 0.999999], 416 events)
Finish audit at graded turns: finish=length 0/1328, parse fail 0/1328
Ack compliance (raw lowercased startswith ok): A-CKPT4710-ack 212/448 = 47.3%
Ack compliance (raw lowercased startswith ok): A-CKPT710-ack 324/512 = 63.3%
Ack compliance (raw lowercased startswith ok): A-CKPT10-ack 440/576 = 76.4%
Ack compliance (raw lowercased startswith ok): T-DENSE-ack 168/336 = 50.0%
Ack compliance (raw lowercased startswith ok): T-SPARSE-ack 264/384 = 68.8%
Excluded pids: family1 none family2 none
VERDICT R1 ladder: LADDER ESTABLISHED
VERDICT R2 repeat: REPEATS-r11; additionally POINT-MATCHES-r11 (|diff - 0.352| = 0.055 <= 0.15)
VERDICT R3 batching: DISSOCIATION ESTABLISHED
VERDICT R4 transport: TRANSPORT DIRECTIONAL
VERDICT R5 forecast: FORECAST SKILLED
```

**`corpus/evidence/round12-ladder/run.log`** (md5 `700d1ddd2ece50d7bdedd55859c59f3a`):

```text
=== SUMMARY ===
A-INC: 48/64
A-CKPT4710: 28/64
A-CKPT710: 21/64
A-CKPT10: 10/64
A-MONO: 2/64
T-DENSE: 2/48
T-SPARSE: 2/48
wall_total_s: 701.6
EXIT=0
```

**`corpus/evidence/round13-ack-state/audit_ack_schedule.py`** (stdout, `--selftest` → `SELFTEST: 4/4 PASS`):
`220/256 (85.9%)`, `216/256 (84.4%)`, `220/448 (49.1%)`, `330/384 (85.9%)`, `324/384 (84.4%)`,
`330/512 (64.5%)`, `32/32 (100.0%)`, `32/56 (57.1%)`, `48/48 (100.0%)`, `48/64 (75.0%)`,
`c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb`,
`918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad`.

**`corpus/evidence/round13-ack-state/analyze_ack_state.py`** (stdout, `--selftest` → `SELFTEST: 8/8 PASS`):
`64 meta; 512 rows logged as A-CKPT710-ack; 6 true ack-only turns × 64 pids = 384`,
`330/384 raw replies start with ok`, `324/384 are exactly bare ok`, `18/384 contain a parseable state`,
`54/384 across 9/64 pids`, `5/64`, `[0.333, 0.889]`, `[0.047, 0.125]`, `input SHA-256 918bf7aa…`.

**Gate / engines** (stdout, 2026-09-29): `CHECKS n=732 mismatches=0 errata_pinned=1` +
`VERDICT: PASS — stored evidence fully re-derives offline`; `SELFTEST 165/165 PASS`;
`[selftest] ALL PASS`.

Any rendering above that differs from a stored line (e.g. `330/384 = 85.9%` in §1b prose for the
audit's `330/384 (85.9%)`) is a prose joiner only; the counts and percentages are transcribed
character-for-character from the register.

---

## 5. Findings (each cited; falsifications first)

- **F-1 — FALSIFIED: the `analysis_r12.md` md5 stored by three landed round-12 artifacts does not match the bytes on disk.** `md5sum corpus/evidence/round12-ladder/analysis_r12.md` → `029c3bcdcf11209d575734742bf239f6` (sha256 `1ceebd7568aab4ecba694b983d7f3312c957402c7841b7597d6ed4506b6453e3`, 9882 B). Stored as `ddfe60d234cae732143649abe80e1ba8` at `r12-report-final.md:96`, `:238`, `r12-log-final.md:5`, `:11`, `r12-doc-deltas-final.md:25`, `:251`; a **third** value `fd3ca422…` is recorded at `r12-review-citations.md` §6 O6 for the same path the same round. The gate pins only `r12_jsonl`/`r12_runlog` (`grader.py:1533-1535`) — `R12_PINS` has no `r12_md` key although the comment directly above it says "`analysis_r12.md` is pinned in the same dict once the promoted engine has generated it" (`grader.py:1530-1532`) — so nothing caught the drift and `python3 grader.py` still reports `CHECKS n=732 mismatches=0`. **Consequence for the landing: do not paste `ddfe60d2…` into LOG/README/SCORECARD; use `029c3bcd…` or pin it in `R12_PINS` first.**
- **F-2 — FALSIFIED: `analysis_r12.md` is not byte-reproducible on this host.** `cd corpus/evidence/round12-ladder && python3 recompute_r12.py` → exit 0, rewrites the file, and the result differs from the landed bytes in exactly one line: `66c66 < Generator source: /home/vgpnk/projects/shokunin/kengaku-shokunin/corpus/evidence/round12-ladder/probe_r12.py …` vs `> … /home/vgpnk/Projects/shokunin/…`. The path comes from `HERE = os.path.dirname(os.path.abspath(__file__))` (`recompute_r12.py:115`) + `PROBE_R12 = os.path.join(LADDER_DIR, "probe_r12.py")` (`:132`) and is printed at `:2003`. `/home/vgpnk/projects` does not exist on this host (`ls -la /home/vgpnk | grep -i project` → only `Projects`), and the committed `recompute-run.log` carries the same lowercase path. So the landed analysis was generated in a tree spelled `/home/vgpnk/projects/…`; [INFERENCE] the landing tree and this host differ only in that spelling, and the engine is otherwise deterministic (a copy at `/tmp/r14regen/ladder` reproduced byte-identically *within its own directory* and differed from the landed file only on that line). The r12 report's claim "regeneration from committed bytes must be byte-identical at round close" (`r12-report-final.md:96`) is false as stated. **Preserved**: the repo file was restored byte-identical after this test (`md5sum` back to `029c3bcd…`).
- **F-3 — MISSING ARTIFACT (not a falsified number): `r12-critic-landed.md` was never delivered.** `test -e corpus/evidence/round12-fleet/r12-critic-landed.md` → absent; the directory holds 22 files (`ls … | wc -l` → 22) and none is the promised fresh-implementation re-derivation. `r12-report-final.md` carries it as `{{CRITIC_LANDED_VERDICT}}` in two places and in the confidence line ("high *after* independent recomputation: … and `CriticLanded`'s fresh implementation") — so the confidence claim is unsupported by any committed artifact. The round-14 landing must record the hole rather than resolve the placeholder.
- **F-4 — STALE, now superseded: the round-12 mutation report's blocker claim is no longer true.** `r12-mutation.md` §Scope/"Survivors" states the promoted engine is "not executable on the committed tree: `--selftest` exits 1 with `AssertionError: no line with prefix 'VERDICT R2 replication'`" and that "no clean `analysis_r12.md` exists in the committed tree". Both are false now: `python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest` → `SELFTEST 165/165 PASS`, exit 0, and `analysis_r12.md` exists (9882 B, md5 `029c3bcd…`). The battery's own results stand as reported (18/18 KILLED, 0 survivors, M0 control KILLED) but its real-byte phase is *now* runnable — the landing should either run it or record the artifact's timestamped scope.
- **F-5 — CONFIRMED, refined: the `-ack` denominators published at r9/r11/r12 are storage-label counts, not ack-only counts.** `python3 corpus/evidence/round13-ack-state/audit_ack_schedule.py` → 4/4 selftest PASS and, for r11 `A-CKPT710-ack`: label rows 512, true ack rows 384, prefix `ok` 330/384 = 85.9%, bare `ok` 324/384 = 84.4%, label-wide prefix 330/512 = 64.5%; r11 `A-CKPT4710-ack`: 220/256 = 85.9% / 216/256 = 84.4% / 220/448 = 49.1%; r9 both cells 100.0% ack-only. `analyze_ack_state.py` → 8/8 selftest PASS, `330/384` prefix `ok`, `324/384` exactly bare, `18/384` exact-state, `54/384` raws contain `{` across `9/64` pids, `5/64` pids with ≥1 exact snapshot, exact-state share bounded `[0.333, 0.889]` because 30 hit the 80-char clip (`run_r11.py:74`). The r12 table (`A-CKPT4710-ack 212/448 = 47.3% … T-SPARSE-ack 264/384 = 68.8%`, `analysis_r12.md` §Ack compliance) is the same label-wide class.
- **F-6 — GATE VERIFIED GREEN at the landing state.** `python3 grader.py` → `CHECKS n=732 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline`, exit 0; `python3 grader.py --selftest` → S0–S7 each `PASS` then `[selftest] ALL PASS`, exit 0. Round 11's 280 → **+452 in the r12 layer**; the `r12.` check-id namespace carries 191 distinct ids (`grep -oE '"r12\.[a-z0-9_.]+"' grader.py | sort -u | wc -l` → 191). This resolves `r12-report-final.md`'s falsifiable-target clause 3 ("NOT MET as of writing — the extended gate exits 1 with 28 r12-layer mismatches") and the mid-review state recorded at `r12-review-citations.md` O6 (`CHECKS n=693 mismatches=28 VERDICT: FAIL`).
- **F-7 — DISCLOSED SCOPE VIOLATION carried by r12.** `r12-scope-audit.md` §Verdict table S5 → `VIOLATION (1)`, `SCOPE VERDICT: VIOLATION (1)`: the L2 endpoint scout self-documented two read-only metadata `GET`s to `127.0.0.1:34113` against a brief that reserved endpoint traffic to L1. Bounded and recoverable (disclose in the report; run evidence unchanged). The round-12 LOG entry above discloses it.
- **F-8 — COUNT CORRECTIONS vs the round-12 drafts.** `ls corpus/evidence/round12-ladder | wc -l` → **18**, not the 17 in `r12-doc-deltas-final.md` §pre-round table (the 18th is `recompute-run.log`, mtime 23:01, written after that table's 23:00 measurement). `ls corpus/evidence/round12-fleet | wc -l` → **22**, not the 21 assumed in this round's brief. Evidence dirs on disk = **10** (six indexed) — including this round's `round14-fleet/`.
- **F-9 — r11 `grader.py` line count erratum carried forward (already adjudicated, restated for the landing).** Committed artifact at `f09ff1f` is **1711** lines (`git show f09ff1f:grader.py | wc -l` → 1711; non-blank 1527 + blank 184), not the `936 → 1709` published at `LOG.md:18`, `SCORECARD.md:142` and the r11 report (`INTEGRATOR-NOTES.md` §3). Recorded in `SCORECARD.md`/`LOG.md` as an erratum, never patched in place. Note `SCORECARD.md` §Confidence (round-10 F1–F3 precedent) allows the erratum; the drafts above do **not** restate 1709 anywhere.
- **F-10 — prior-art counts as measured.** `grep -oE 'https?://[^ )|]+' corpus/evidence/round12-fleet/r12-prior-art-ladder.md | sort -u | wc -l` → **38** unique URL strings, while the artifact's own §0 census states **56 distinct URLs fetched, 53×200, 3 failures** and **22 cited sources**; transport: **64** unique strings vs its §5 "**45 distinct works / 52 URL rows**, all 200" and "6 fetch failures". Quote the artifact's own census (fetch-count/row-count convention), not the `grep` — and note `r12-prior-art-transport.md:25` still prints the pre-amendment **"448 binary pass events"** for C5 where the amended plan and the landed analysis use **416** (`INTEGRATOR-NOTES.md` §2 L1-E6).
- **F-11 — independent audits that passed.** `r12-review-baseline.md` → `BASELINE: GREEN` (41 pointers re-run; strict citation resolution 9/10 = 90% on a fixed 10-bullet sample; the single miss is the documented-absent ledger path). `r12-review-citations.md` → `CITATION RESOLUTION: 98.9% strict / 100.0% lenient, 0 broken`. `r12-connector.md` → `DUPLICATE-INSTRUMENT RISK: NONE` (five sibling HEADs, exact greps). `r12-endpoint-freshness.md` → run verdict `GO` with 6× `NO-DRIFT`, and the r10 open item closed: the on-disk gguf `10 333 691 040 B` = `data_offset 5 973 152` + Σ tensors `10 327 717 888` (= `meta.size`), residual 0, `NE` sum `30 532 122 624`.
- **F-12 — SKILL.md delta as measured.** `git diff --stat SKILL.md` → `59 +`; `wc -l < SKILL.md` → 577 (r11 recorded 518); anti-patterns **19**, measurement rules in the planning-horizon section **13**, cited-source bullets **23**. The landed `SKILL.md` is therefore past the round-11 self-description at every count; any text carrying "15 anti-patterns"/"518 lines" is superseded (note `r12-review-citations.md` O3 already flags the 15-vs-19 section-scoping discrepancy in the r12 drafts).

---

## 6. Gaps / open items for L1 (not resolved here)

1. **`analysis_r12.md` pin decision** — the landing must either add `"r12_md": ("md5", "029c3bcdcf11209d575734742bf239f6")` to `R12_PINS` (fixing the false comment above it) or record in `SCORECARD.md` why the derived analysis stays unpinned. Until then F-1 is live and a silent regeneration is undetectable.
2. **Regeneration reproducibility** — either accept F-2 as a recorded limit (generator path is directory-dependent) or have `recompute_r12.py` emit a path-independent `Generator source` line and re-land the analysis + pin once. Re-landing changes `analysis_r12.md` bytes, so it must be a single recorded act, not a side effect.
3. **`r12-critic-landed.md`** — either commission the fresh re-derivation now (narrow: re-derive R1–R5 and the §5 lines from `results-r12.jsonl` with an independent implementation) or record the placeholder as permanently open in `SCORECARD.md` §Confidence. The round-12 report cannot be edited in place.
4. **Mutation-battery real-byte phase** — with the promoted engine now green (165/165), the real-byte mutations the battery declared UNVERIFIED are runnable; decide whether to run them in-round or timestamp the artifact's scope.
5. **Round-13 knowledge row** — the drafts above put the ack-denominator correction in `LOG.md` round 13, `lessons/round-13.md` and the open-gaps list. If L1 wants it durable in `corpus/knowledge/` too, the OPTIONAL row is `| knowledge/bench-arena-ack-denominators.md | … | corpus/evidence/round13-ack-state/, round 13 |` — then knowledge rows must be **24 = 24** and the coverage flip condition in §2b changes accordingly.
6. **Round-14 scorecard semantics** — §2b is the scribe's rubric-derived reading, held to `LandingGate`'s
   ruling: **only novelty 6 → 7 is adjudicated**; coverage and freshness move only if their named
   verification commands pass against the landing commit (both are written as CONDITIONAL/hold-by-default
   so the conservative variant can be pasted unchanged). Whether the landing round earns any other move
   remains L1's judgement.
7. **Dates** — the round-12 entry is dated `2026-09-28` (the local date of its `01:16Z`–`01:32Z` work) to match `LOG.md:17-18`'s convention; round 14 is dated `2026-09-29`. If the landing commits after local midnight, L1 may prefer both at the commit's date — the UTC anchors are in the entries either way.
8. **Out of scope here (not drafted)**: `PROVINCE.md` §Surfaces row updates (round 12's drafts had three replacement rows — the served-model row, the route-telemetry row and the In-repo-gate row with the new check count) and `SHONEN.md`'s four checklist lines. Both were drafted in `r12-doc-deltas-final.md` §2/§3 and still need the now-resolved values (`{{GRADER_CHECKS}}` → 732, `{{SELFTEST}}` → S0–S7 ALL PASS, `{{AXIS_NOVELTY_AFTER}}` → 7). Flagging, not writing, per this task's target.

---

## 7. Verify this file's numbers

```bash
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
md5sum corpus/evidence/round12-ladder/analysis_r12.md corpus/evidence/round12-ladder/results-r12.jsonl corpus/evidence/round12-ladder/run.log
python3 grader.py; echo "exit=$?"; python3 grader.py --selftest; echo "exit=$?"
python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest; echo "exit=$?"
(cd corpus/evidence/round13-ack-state && python3 audit_ack_schedule.py --selftest && python3 analyze_ack_state.py --selftest)
grep -nE '^(E1|E2|E3|E4|E5|E6) |^VERDICT' corpus/evidence/round12-ladder/analysis_r12.md
ls corpus/evidence/round12-ladder | wc -l; ls corpus/evidence/round12-fleet | wc -l
grep -c '^| `knowledge/' corpus/README.md; ls corpus/knowledge | wc -l
grep -c '^| `lessons/' corpus/README.md; ls corpus/lessons | wc -l
grep -c '^| `evidence/' corpus/README.md; ls -d corpus/evidence/*/ | wc -l
```

> **Caution for the landing operator**: `python3 corpus/evidence/round12-ladder/recompute_r12.py`
> (without `--selftest`) **rewrites `corpus/evidence/round12-ladder/analysis_r12.md` in place**
> (`recompute_r12.py` `--out` defaults to that path). Running it changes the md5 from the landed
> `029c3bcd…` to a directory-dependent value (F-2). `--selftest` is safe — it only writes into
> `tempfile.TemporaryDirectory()` (verified: the md5 was unchanged after the selftest run above).
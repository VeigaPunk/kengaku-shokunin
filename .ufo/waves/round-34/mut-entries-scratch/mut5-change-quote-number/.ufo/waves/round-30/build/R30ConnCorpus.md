# R30ConnCorpus — lane-internal duplication scan of the contamination-transparency card

Seat: connector (`L1Kengaku30.R30ConnCorpus`), leaf. Round 30, kengaku, hyaku run 6, 2026-10-25.
Scope: lane-internal duplication only — which **already-landed kengaku bytes** state each card field and
each Q1–Q8 question, what NEW statements an admission would actually add, and whether the entry should be
an errata-style amendment. Read-only; no production edits; no subagents. Written permission: this file only.

**Honesty bounds.** I did **not** open S081–S086. No line below is a re-grounding verdict and no quote is
offered as a fetch receipt. Every quoted byte is read from the lane repo (`/home/vgpnk/Projects/shokunin/
kengaku-shokunin`) or from the staged package (`/home/vgpnk/Projects/shokuknow/merge/kengaku/`, read-only);
each is labelled by path and line. Every count below is a command I ran and can be re-run. No tool was
installed or upgraded (nothing was needed). `pacman` was not invoked.

**The tree moved under this scan, and the report says which state each section answers.** When this seat
started, `corpus/knowledge/` held 38 entries and `plans/sources_adopt.py` had no quote logic. While it ran,
peers landed: the entry itself (`corpus/knowledge/contamination-transparency-card.md`, untracked, 163 lines,
mtime 04:31, `writer: KengakuR30`), six registry rows S081–S086 in `corpus/SOURCES.md`, the C3 quote
validation (`--quote-file`/`--artifact`, `quote_check`, `EXIT_QUOTE_*`), README index/coverage/frontier rows,
`plans/round30_defects.py`, and `corpus/evidence/round30/`. Therefore: **§1–§6 answer the question as frozen**
— duplication against the 38 entries that existed when the claim was set, with the card as an object, not a
neighbour — and **§13 audits the landed 39th entry against that matrix**, which is now the live question.
Where §7/§10 predicted a tool behaviour, §10 now carries the landed code's actual behaviour and the prediction
is marked as borne out rather than assumed.

Second-seat relation to the sibling report: `.ufo/waves/round-30/build/R30Overlap.md` already publishes a
field-by-field table. This report is an **independent re-read of its matrix** (QUALITY Q10's second-seat
discipline applied to a build artifact, not an admission) — §2c lists six places where my grep disagrees with
it, and §7 adds landing mechanics it did not derive. Where I agree I say so and add the pointer.

## 0. Verdict in one line

**Amendment, not a rival design** — and smaller than it looks: the card's 15 disclosure cells collapse to
**12 distinct statements**, of which **1 is fully held** (`Q4`), **7 are partially grounded** in lane bytes
with different vocabulary or scope, and **4 are wholly absent** (`R1`, `R2≡Q6`, `R4`, `S1`); the smallest
honest new content is **7 statements plus 1 design rule**, all of which fit in an amendment file that names
`corpus/knowledge/contamination-detection-and-transparency.md:9-14,70` as the entry it extends.

---

## 1. Vocabulary scan — with the false friends that make a keyword search lie

Commands are exact; run from the lane root. `knowledge` = `corpus/knowledge/*.md` — **38 entries at scan
start, which is the population this table scores; 39 now that the card itself has landed** (§13). The count
command returns 38 then and 39 now, and `grep -c '^| \`knowledge/' corpus/README.md` matches it at both times
(38 → 39), so the index and the tree agree in both states.

| Card term | Pattern | Hits | What the hits actually are | Verdict |
|---|---|---|---|---|
| contamination type | `grep -rn -i 'contamination type'` | **0** | — | absent |
| contamination tier | `grep -rn -i 'contamination tier'` | 4 | `contamination-detection-and-transparency.md` (CDT) `:11`, `:19`, `:70`; `README.md:56` | slot exists, never defined |
| T1–T4 | `grep -rn 'T1–T4'` (**en dash**) | 1 | CDT`:70` "contamination tier tested (T1–T4)" | token used |
| T1-T4 | `grep -rn 'T1-T4'` (**ASCII hyphen**) | 1 | `corpus/SOURCES.md:23` (S001 row) "four-tier contamination taxonomy (T1-T4)" | **count stated in the registry, enumeration nowhere** |
| tier (bare) | `grep -rni 'tier'` | 41 | mostly SOURCES tier A/B/C, "frontier tier", "spec-ability tiers" (`eval-design-digest-2.md`), `bench-arena-…` arms | **false friend** — a fourth sense |
| T-numbered labels | `grep -rn 'T[0-9]'` | many | `SKILL.md:72` and `godspeed-eval-findings.md:19` "**T2 review** gradient"; `attrib-r21.md` timestamps; `bench-arena-round12-ladder.md` `A-CKPT10` | **false friend** — a *third* T-vocabulary already in the lane |
| canary | `grep -rni 'canary'` | 4 files | `benchmark-task-validity-checklist.md` (BTVC) `:1`, `:5`, `:40`, `:51`, `:119-127`; **but** `bench-arena-round5-battery.md:76` "Canary update" and `round6-stability.md:72` "Canary refresh" are probe names, not contamination markers; sibling lane has a third sense (`chousa-shokunin/corpus/knowledge/engine-swap-canary-r36.md`, a tool tripwire) | **false friend ×2 inside the lane** |
| hold-out | `grep -rni 'hold-out\|holdout'` | **0** | only the hyphenated adjective: CDT`:50`, `agent-time-horizon-and-task-validity.md:45`, both inside falsifier sentences | absent as a concept |
| elicitation budget | `grep -rni 'elicitation'` | **0** in `knowledge/` + `SKILL.md`; 1 repo-wide, `corpus/evidence/round12-fleet/r12-prior-art-transport.md:96` (an unrelated search string in a prior-art receipt) | — | absent |
| strata / stratification | `grep -rni 'stratif'` | 5 | `grader-perturbation-audit.md:84`, `:106`; `webarena-task-spec-audit.md:66`, `:115`; `SKILL.md:481` — all the lane's **own** analyses | absent as a disclosure requirement |
| per-stratum | `grep -rn 'per-stratum'` | **0** | — | absent |
| regeneration | `grep -rni 'regeneration'` | 4 | `bench-arena-round11-power.md:98`; `round12-ladder.md:203`, `:211`, `:264` — **artifact** regeneration / byte-identical replay | **false friend** for R4 (instrument regeneration status) |
| disclosure card | `grep -rni 'disclosure card'` | **0** | — | absent |
| "card" (any) | `grep -rni 'card'` in `knowledge/`+`SKILL.md` | 3 relevant | CDT`:73` (a preference for suites with a card); `open-model-catalogs.md:17` (HF model card); `SCORECARD` prose elsewhere | **the lane has zero card-*schema* bytes**; the word appears once in an apply row and is never defined |
| hidden test | `grep -rni 'hidden.test'` | 1 | BTVC`:38` "hidden-test paths are restored or removed before the test patch applies" | held, adjacent |
| hidden/private split | `grep -rni 'private split\|hidden split'` | 3 | CDT`:73` (Don't); `benchmark-saturation-and-lifecycle.md:74` (Don't), `:83` (flip) | held as a *warning* |
| unknown-is-valid | `grep -rni 'unknown'` | 3 relevant | `local-model-index.md:28` tri-state "missing = unknown, `null` = not applicable, populated = known"; `webarena-task-spec-audit.md:49` "Unknown/missing runtime conditions are not silently reclassified as task failures here"; `QUALITY.md:36-42` (Q4) | principle held, application absent |
| web index / crawl (as detector access) | `grep -rni 'web index\|crawl'` | **0** | — | absent |
| Q1–Q8 | `grep -rn 'Q1[–-]Q8'` | ≥2 senses | `QUALITY.md:15`…`:61` admission bar; `README.md:115` indexes it as "Admission bar for knowledge entries (Q1–Q8)"; the card's gate at `:45`,`:47`,`:69`,`:90` | **live label collision** — see §4 |

Consequence for any future mechanical duplication scan: a single pattern per term under-counts. `T1–T4`
(en dash) and `T1-T4` (ASCII) hit **different files**; `canary`, `tier`, `regeneration` and `card` each have
at least one in-lane homonym.

---

## 2. Field → existing-entry matrix (the deliverable)

Legend — **HELD**: the lane states the same requirement; **PARTIAL**: the slot or the principle exists but
the values, scope or attachment differ; **ABSENT**: no lane bytes state it. Card line numbers are the staged
file's (`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md`).

### Release-side fields

| Cell | Card | Verdict | Lane pointer(s) and the bytes that decide it |
|---|---|---|---|
| **R1 Strata** — per-stratum scores for a named stratification | `:32` | **ABSENT** | Nearest *practice*, not requirement: `paired-eval-uncertainty-reporting.md:14` "When questions are drawn in related groups, computing clustered standard errors"; `:9` "report uncertainty and resolution under the actual item-family clustering"; `:34` names the lane's own r8/r11/r12 within-problem designs. `grader-perturbation-audit.md:84` "Its format strata are FJ1 639/639…" is a lane analysis. No entry requires a *third party* to publish per-stratum scores. |
| **R2 Elicitation budget** — identified harness + ≥2 of {version, budget, attempts, attempt resolution} | `:33` | **ABSENT** | Zero `elicitation` bytes. Nearest are rules about the **lane's own** freeze, not a disclosed third-party budget: `SKILL.md:80-81` "Freeze godspeed text, judge schema, and telemetry capture before scored runs"; `telemetry-run-design.md:36` "**Phase 0 freeze** before scored runs"; `bench-arena-round11-power.md:25` "Experimental-unit descriptors pinned at run time"; `attrib-r21.md:37` "weights pre-registered, sha-frozen". Nothing in the lane mentions *attempts* or *attempt resolution* as disclosure values (`grep -rn 'attempts' corpus/knowledge/*.md` → `probe-battery-r19.md:264` only, a fallback-leg narrative). |
| **R3 Contamination type tested** — direct / derivative / temporal / distributional + observed code | `:34` | **PARTIAL (slot only)** | `CDT:70` "contamination tier tested (T1–T4)" — the slot, with an **undefined token**; `SOURCES.md:23` "four-tier contamination taxonomy (T1-T4)" — the *count* is a lane byte, the four labels are not; `grep -rl 'derivative' corpus/knowledge/*.md` → 0. So the lane states that a four-part taxonomy exists and never lists it. |
| **R4 Regeneration status** — of the instrument used, whether or not the reporter built it | `:35` | **ABSENT** | Only word-collision: `bench-arena-round12-ladder.md:203` "regeneration from committed bytes must be byte-identical"; `bench-arena-round11-power.md:98` "offline (meta regeneration…)". Both are the lane reproducing *its own* artifacts. |
| **R5 Instrument currency** — date of the benchmark's last substantive update | `:36` | **PARTIAL** | The *rule that a date must accompany a benchmark claim* is landed, the *field* is not: `benchmark-saturation-and-lifecycle.md:14` "any retirement call must name the model set, leaderboard snapshot, and uncertainty assumptions"; `:73` "State top-k set, dated leaderboard snapshot, SE assumptions"; BTVC`:43` "the release gate is dated and states its hardware and check set" (S078 gate `2026-09-22`); `SKILL.md:62-65` "a benchmark's reputation outlives its signal. Re-check contamination status before citing." |

### Score-side fields

| Cell | Card | Verdict | Lane pointer(s) |
|---|---|---|---|
| **S1 Acquired contamination** — network access, env sanitisation, transcript review, boundary monitoring, with elements in `notes` | `:42` | **ABSENT** | `CDT:13-14` requires "keep a transparency record rather than report \"clean\"" — a record with no field set and no attachment point. Nearest run-side sentences: BTVC`:38` "the verifier does not run inside the agent's sandbox"; BTVC`:39` "S078 sanitised-history clause" (`grep -rni 'sanitis'` → this one hit). Neither covers network access, environment sanitisation, transcript review or boundary monitoring **at run time**. |
| **S2 Card integrity** — `controlled` / `not_controlled` / `unknown`; `unknown` valid | `:43` | **PARTIAL (principle)** | `local-model-index.md:28` "Tri-state: missing = unknown, `null` = not applicable …, populated = known" — the lane already has a tri-state-with-unknown convention; `webarena-task-spec-audit.md:49` "Unknown/missing runtime conditions are not silently reclassified as task failures"; `QUALITY.md:36-42` (Q4) "An indeterminate or detector-negative result is reported as such, never laundered into a positive". The principle is held **three times**; a *card-integrity* triple is new. |

### The Q1–Q8 gate

| Cell | Card | Verdict | Lane pointer(s) |
|---|---|---|---|
| **Q1** Which contamination type is claimed/tested | `:53` | **PARTIAL** | ≡ R3 — `CDT:70` slot, no labels. (The card duplicates itself here; see §3.) |
| **Q2** What detector access the reporter had — parameters only / training corpus / public web index / **canary** | `:54` | **PARTIAL (field held, enum partly new)** | `CDT:70` "model access (weights/logits/black-box)" + `CDT:9-11` "bounds only what that detector could see at its access level"; canary is held in a **different role**: BTVC`:40` "a per-task canary is embedded in the task files and checked mechanically" and BTVC`:119-121` "a canary's absence is not evidence of contamination, and a canary's presence is detectability, never proof of training-corpus exclusion". Missing: training-corpus access and public-web-index access as named options (`grep -rni 'web index\|crawl'` → 0). |
| **Q3** Which tier and which datasets/subsets were tested, and the coverage limit | `:55` | **PARTIAL** | `CDT:9-11` states the coverage-limit *principle* ("bounds only what that detector could see at its access level and contamination tier"); no lane byte carries a *dataset/subset*-level scope for a detector. `BTVC:57-63` bounds that entry's own counts (1 of 89 task dirs), which is a different denominator. |
| **Q4** What a negative does **not** rule out | `:56` | **HELD** | `CDT:70` Do-cell "…and what a negative cannot rule out"; `CDT:9-11`; `CDT:41-50` (§What this does not establish, incl. the falsifier at `:49-50`); `README.md:56` "detector-negative ≠ uncontaminated". Only the two *source-specific* blind spots (S084 "no widely accepted solution", S086 false-positive regime) are new material — on a held rule. |
| **Q5** Is this artefact release-side or score-side | `:57` | **PARTIAL** | The lane has a **run-side artifact convention** but no split rule: `telemetry-run-design.md:15-32` "10 telemetry fields per run" + "Artifact set per run dir … `response.md` + `telemetry.json` + `judge.json` adjacent". What is absent is the rule that contamination *acquired during a run* must be recorded with the score and not with the release. `CDT:71` ("require transparency records of training stages") is a stage requirement, not an attachment side. |
| **Q6** Was the elicitation budget stated | `:58` | **ABSENT** | ≡ R2. |
| **Q7** Is the item set protected, and is there a refresh protocol | `:59` | **PARTIAL** | Protection half held, as a **warning against** reading protection as cleanliness: `CDT:73` Don't "Treat a private/hidden split as proof of cleanliness"; `benchmark-saturation-and-lifecycle.md:74` Don't "keep on a \"private split\" claim"; the evidence behind it at `:25-27` "Hiding test data does not prevent it. S007, §4.1: \"Hiding test data does not appear to prevent saturation once benchmarks are widely adopted\"" and `:44` "too weak to assume it protects"; canary practice at BTVC`:40`; hidden-test hygiene at BTVC`:38`. Refresh/retirement **protocol as a disclosable artefact**: absent. |
| **Q8** When was the instrument last regenerated / the benchmark last substantively updated | `:60` | **PARTIAL** | Both components are adjacent, neither is a field: BTVC`:43` (dated release gate) and `benchmark-saturation-and-lifecycle.md:14`,`:73` (dated snapshot). No lane byte asks a reporter to publish either date. |

### The card's two design rules and its precedent section

| Cell | Card | Verdict | Lane pointer(s) |
|---|---|---|---|
| **D1** A card must be procedural, not item-revealing (S082) | `:64-69` | **ABSENT** | `CDT:73` presumes "a documented transparency card" exists; `SKILL.md:88-90` (anti-pattern 8) is about memorised-data benchmarks *understating* gains, not about disclosure form. `grep -rni 'procedural'` → 0 in `knowledge/`. |
| **D2** A negative must be stated as a negative | `:71-77` | **HELD** | `CDT:9-14` + `CDT:70` + `QUALITY.md:36-42` (Q4). The mechanism (per-detector blind-spot disclosure) is new source material on a held principle. |
| **P** S085 "方升" dynamic test bank | `:79-88` | **ABSENT as content, but it meets a landed negative-space line** | `grep -rl '方升\|OpenCompass\|CAICT\|C-Eval' corpus/knowledge/*.md` → 0 files. `CDT:37-38` holds S004's construction-side remedy and `CDT:47-48` "S004 proposes a direction; it supplies no working contamination-resistant benchmark today." See contradiction X4. |

**Counts, stated once and exactly.** The card has 15 disclosure cells (R1–R5, S1–S2, Q1–Q8). De-duplicating
the card's own repeats (§3) leaves **12 distinct requirements**:

- **HELD — 1:** Q4 (and design rule D2 held as a principle).
- **PARTIAL — 7:** R3≡Q1, R5, S2, Q2, Q3, Q5, Q7.
- **ABSENT — 4:** R1, R2≡Q6, R4, S1.

Q8 is not a thirteenth requirement: it is the union of R4's status and R5's date and is scored through them
(absent + partial). D1 is a separate design rule, ABSENT; P is a section, ABSENT. This is why §5 lists **7 new
statements plus 1 design rule** rather than 12.

### 2c. Six corrections to `R30Overlap.md`'s matrix (independent re-read)

| # | R30Overlap says | I read | Consequence |
|---|---|---|---|
| a | R5 "**NEW** (adjacent)" | **PARTIAL** — `benchmark-saturation-and-lifecycle.md:14` *requires* a dated snapshot in any retirement call, and `:73` repeats it as a Do-cell | The rule is landed; only the card *field* is new. Calling it NEW overstates the delta and would let the amendment re-teach a held rule. |
| b | Q5 "**NEW**" | **PARTIAL** — `telemetry-run-design.md:15-32` is a run-side record convention (per-run `telemetry.json`+`judge.json`) | New content is the **split rule**, not "where does a run record live". |
| c | S2 "**NEW**" | **PARTIAL (principle)** — `local-model-index.md:28` states a tri-state with `unknown` already; `webarena-task-spec-audit.md:49` states "not silently reclassified" | R30Overlap cited `QUALITY.md:36-42` (Q4). Both support it, but the *tri-state* pointer is the closer and the one that stops the amendment re-inventing a convention. |
| d | "`grep -rn 'T1–T4' corpus/ SKILL.md` → one hit … the four labels are never spelled out anywhere in the lane" | True for the labels; but the **ASCII spelling** hits `corpus/SOURCES.md:23`, in the very row whose `used-by` names CDT | The lane *does* state "four-tier contamination taxonomy (T1-T4)". The defect is a **count without a listing** (Q3-shaped), not an entirely undefined token. |
| e | R3 "Card values are therefore new vocabulary **resolving** an existing undefined token" | No byte establishes that S001's T1–T4 and S081's t1–t4 are the same four. `CDT:9-11` pairs "**access level** and contamination tier", i.e. tier reads as a detector-access/stage dimension, while the card's t1–t4 are contamination *types* | These may be orthogonal axes. The amendment must **not** silently redefine a landed line; state the identity as open (X3). |
| f | (A1) implies the source header needs rework | The staged card already has **six separate `source:` lines** (`:2-7`), one id each | `SOURCE_LINE_RE` will find six; C1's `cited_rows=6` is satisfiable without reformatting. Do not "fix" a non-defect. |

---

## 3. The card duplicates itself: 15 cells → 12 distinct statements

| Duplicate | Card lines | Why it matters |
|---|---|---|
| R3 ≡ Q1 | `:34`, `:53` | Q1's "Answerable from" column just restates R3's values. |
| R2 ≡ Q6 | `:33`, `:58` | Q6 adds no value beyond R2. |
| Q8 ⊃ R4 + R5 | `:60` vs `:35-36` | Q8 asks both dates; R4 asks one of them, R5 the other. |
| Q5 ≡ the score-side table header | `:57` vs `:38` | `:38` already says "recorded with each reported score, not with the dataset" — the split rule *is* Q5. |

So the entry should publish **one** table, not a fields table plus a gate table that re-asks four of its
cells. Under QUALITY Q6 ("extends, never duplicates") re-tabling the same cell twice is self-duplication.

---

## 4. `Q1–Q8` is a live label collision — with a mechanical reason to rename

- The lane's admission bar is already called Q1–Q8: `QUALITY.md:15` (Q1) … `:61` (Q8), and
  `corpus/README.md:115` indexes it as "Admission bar for knowledge entries (**Q1–Q8**)".
- The card names its gate "The Q1–Q8 gate" (`:45`) and uses it at `:47`, `:69`, `:90`.
- Round 29's own flip string is `corpus/lessons/round-29.md:180`: "open S081–S086 in a later round as its own
  theme and **pass QUALITY Q1–Q8** then".
- After admission, `grep -rn 'Q1–Q8'` matches two different gates, and a Gate receipt that says "Q1–Q8 pass"
  cannot be read back. Rename at admission — the landed draft chose **`CG1–CG8`** (§13), and any prefix
  distinct from the admission bar's works; the requirement is that `grep -rn 'Q1–Q8'` resolves to one gate.
  Keeping the numerals with a mandatory "card gate" qualifier in the heading and every citation would also
  clear it. Confirms `R30Overlap.md` A2 and adds the round-29 line that makes the ambiguity load-bearing.

---

## 5. The smallest set of NEW statements (what the admission actually adds)

Seven statements plus one design rule. Each entry names its anchor, **why the lane does not already hold it**,
and where it should land. These are the only claims an amendment needs; everything else in the card is a
restatement that must be *marked*, not reprinted.

| # | Statement | Anchor | Why not already held | Lands as |
|---|---|---|---|---|
| **N1** | A reported score must be accompanied by per-stratum values for a **named** stratification; a pooled number hides the stratification the result depends on. | S081 F1 (card `:32`) | `paired-eval-uncertainty-reporting.md:14` tells *this lane* to cluster; no lane byte requires a third party to publish stratified scores. | release-side cell |
| **N2** | A score's **elicitation budget** must be identified: named harness pinned to a public version or fully specified as a scaffold, plus ≥2 of {version, budget, attempts, attempt resolution}. | S081 F2 (`:33`, `:58`) | `SKILL.md:80-81`, `telemetry-run-design.md:36`, `bench-arena-round11-power.md:25`, `attrib-r21.md:37` freeze the lane's *own* harness; no "attempts"/"attempt resolution" bytes exist anywhere in the lane. | release-side cell (absorbing Q6) |
| **N3** | The contamination **type** tested is one of four named types, each recorded with the code observed — **and** the lane's existing `T1–T4` token is *not* thereby defined (identity to S001's taxonomy unproven). | S081 F3 t1–t4 (`:34`) | `CDT:70` uses `T1–T4`; `SOURCES.md:23` says four tiers exist; neither lists them, and no byte equates the two taxonomies. | release-side cell + a dated erratum appended to CDT (R1/R5 — never in-place) |
| **N4** | Contamination **acquired during evaluation** is a property of one run and is recorded with the reported score, not with the benchmark release. | S081 (`:38`, `:57`) | `telemetry-run-design.md:15-32` is a run-artifact set, not an attachment rule; `CDT:13-14` requires a record with no attachment point. | the split itself; Q5 reduces to this one sentence |
| **N5** | A detector's **dataset coverage limit** is a required field: which datasets/subsets the method supports, stated by the detector's own documentation. | S084's two "仅支持" clauses (`:55`) | `CDT:9-11` bounds a negative by *access level and tier*; no lane byte carries a dataset-scoped limit. | release-side cell (Q3) |
| **N6** | A **refresh/retirement protocol** for the item bank is a disclosable artefact — written beside the lane's opposite-direction evidence that protection is not cleanliness. | S083 (`:59`) | BTVC`:38`, `:40` hold hidden-test hygiene and canary practice; `CDT:73` and `benchmark-saturation-and-lifecycle.md:25-27,44,74` hold the *warning*. No lane byte asks for a published refresh path. | gate cell **plus** the warning pointers (X1) |
| **N7** | **Card integrity** is a tri-state `controlled` / `not_controlled` / `unknown`, and `unknown` is a valid entry; a `controlled` claim without boundary monitoring is an assumption. | S081 (`:43`) | The principle is held three times (`local-model-index.md:28` tri-state; `webarena-task-spec-audit.md:49`; `QUALITY Q4`), but never as a card field with those three values. | score-side cell, citing `local-model-index.md:28` so the convention is inherited, not re-invented |
| **D1** | A card's fields must be **procedural, not item-revealing** — publishing live items to prove contamination-freedom increases contamination. | S082 (`:64-69`) | `CDT:73` presumes a card exists; no lane byte states the disclosure boundary. | one design-rule paragraph |
| — | (Held; mark as restatement) Q4 negative-space rule; D2 negative-as-negative; Q2's `weights/logits/black-box` field; Q7's "protection is not cleanliness" Don't. | — | `CDT:9-14`, `:41-50`, `:70`, `:73`; `QUALITY.md:36-42`; BTVC`:119-121` | one pointer row each, no re-teaching |

Not in the list on purpose: the S085 dynamic-bank precedent is **not** a card field and **not** an upgrade of
`CDT:47-48` — see X4.

**What the landed draft does with this list.** It goes the other way and reclassifies N2/N3/N5/N6 as columns
the three published card designs already carry, leaving only S1, S2 and R1's value set as a delta (§13). That
is the stronger Q6 answer **if** the table it maps into is inspectable from the lane — and it is not, which is
§13's D-a. If D-a is repaired by landing/citing the table, this N-list shrinks to three items; if it is not,
the N-list is the honest delta and needs nothing outside the lane. The list is therefore not optional
either way: it is the fallback that survives D-a, and its seven statements are the seven content claims an
admitted entry must be able to defend from the six rows' own quotes.

---

## 6. Verdict: entry vs amendment

**Amendment — expressed as the file C1's predicate requires.** Four independent reasons:

1. **The recorded flip demands it.** `corpus/lessons/round-29.md:242`: "…to the tabulated designs rather than
   a new design"; the rejection reason at `:223-224` is QUALITY **Q6** — "it offers a fourth card design where
   the campaign's own round 6 tabulated three published designs". A standalone entry that reprints 13 cells
   of which 1 is fully held and 7 partly grounded *is* the fourth design.
2. **QUALITY Q6's test is satisfiable only by naming.** `QUALITY.md:50-53`: "The entry names the existing
   entry or coverage row it extends; a weaker entry is superseded by a new entry that names it." CDT is not
   weaker on Q4 (it *owns* the negative-space rule), so nothing is superseded — the new bytes must declare
   extension. The card as staged **refuses** this: its `ground:` line (`:90`) says "the *admission* of the
   card against the lane's existing … vocabulary is the lane's call, **not this entry's**". That sentence is
   the Q6 defect and must be replaced by an `## Extends` heading naming
   `contamination-detection-and-transparency.md:9-14,70` (primary) and
   `benchmark-task-validity-checklist.md:19-21,40,43` + `benchmark-saturation-and-lifecycle.md:14,74`
   (adjacent holders, explicitly not absorbed — the BTVC precedent is `:19-21` "extends … and supersedes
   neither").
3. **C1's frozen predicate constrains the path, not the content.** It requires
   `corpus/knowledge/contamination-transparency-card.md` to exist with six `source:` lines, `verified-at:
   2026-10-25`, and one index row. "Amend CDT in place" cannot satisfy that, and R1 (`QUALITY.md:48-49`
   "numbers are corrected by appended errata, never in-place edits") forbids in-place editing anyway. An
   **amendment file** satisfies the predicate and Q6 simultaneously. This is not predicate-gaming: the
   predicate says nothing about the file's internal claims, and the amendment is the *stricter* reading of
   the round-29 flip.
4. **The delta is smaller than the restatement.** 7 new statements + 1 design rule against 13 cells of
   table; a schema that re-lists held bytes would make the entry mostly duplication by line count. The
   amendment's table must therefore be a **delta table**: every row carries either `new` (N-number) or
   `held at <path>:<line>` + the row's own words.

Not errata-**only**, though: `grep -rni 'card'` over `knowledge/` returns exactly one relevant line
(`CDT:73`), so the lane genuinely has **no card schema** — the schema is real new content. The amendment is
a schema whose cells declare their own provenance.

Mandatory sections the staged file lacks and an admitted amendment must carry (else it fails the admission
bar it is being admitted under): `## Extends` (Q6), §What this does not establish **with a falsifier** (Q4),
an attribution/labelling paragraph (Q5 — S081/S082 are tier-B preprints, S083/S086 tier-A peer-reviewed,
S084 tier-A documentation, S085 a tier-B report with no document number: `SOURCES.append.md` rows 11-16),
and a `§Rejected` recording the rival-design framing with the round-29 flip as its condition (Q8).

---

## 7. Landing mechanics the counter actually enforces (derived from the two tools, not from prose)

Read from `plans/adoption_check.py` and `plans/sources_adopt.py` today:

| Requirement | Source | Consequence for this admission |
|---|---|---|
| Registry cells are index-addressed: `cells[7]`=status, `cells[8]`=opened, `cells[9]`=recheck, `cells[10]`=used-by; 11 columns (`COLUMNS = 11`, `sources_adopt.py:38`) | `adoption_check.py` `rows_mined`/`usedby_ok`; `sources_adopt.py:38` | the six rows must be appended as 11-cell rows; a 12-cell row is refused (`columns=` defect) |
| `usedby_ok` is **per-entry all-of** and a **membership** test (`rel in [part.strip() for part in registry[row_id][10].split(",")]`) | `adoption_check.py` | a used-by cell containing *extra* paths still passes — so a hand-written block that carries the staged rows' `corpus/knowledge/judge-calibration-thresholds.md` and `corpus/knowledge/cjk-eval-venue-access.md` (both **absent from the lane**: `ls` → No such file) would pass the counter while leaving pointers to non-existent files. `sources_adopt.py` rewrites `cells[10]` to exactly the admitted entries (`build_block`), so **the gate must be the channel** |
| `verified-at` is matched by `^verified-at: 2026-10-25\b` | `adoption_check.py` | the staged `:8` (`2026-10-23`) must be rewritten |
| Index row regex `^\| \`knowledge/<name>\` \|` | `adoption_check.py` | the README row must begin with the backticked path, at line start |
| `--census` shells out to `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <parent> <lane>` and needs exit 0 | `adoption_check.py` | the census, not this seat, decides |
| `build_block` refuses a row whose `opened` ≠ access date unless `attest_opened`; its own comment: "silently stamping it would launder a stale row" | `sources_adopt.py:155-159` | the staged rows carry `opened = 2026-10-23`. C1's `opened=2026-10-25` therefore needs either a real re-fetch today or the attestation flag — and **the counter cannot tell which**. Honesty of C1 rests on the source seats, not on the gate |
| `ISO_DATE_RE = ^\d{4}-\d{2}-\d{2}$`, `CADENCE_RE = ^\d+d$`, `SYMBOLIC_CADENCE = {on-release, on-request, on-commit, never}` | `sources_adopt.py:34-36` | the staged recheck cell ("2026-10-23 — re-verify at the next upstream release (Gate S081)") does **not** match ISO_DATE_RE (anchored `$`), so it is treated as prose and coerced to `recheck_default = 180d`, with the prose reported. For arXiv preprints the honest cell written by hand is `on-release` (precedent: S005/S006) — otherwise the append silently converts an event trigger into a 180-day clock |

---

## 8. The D5 asymmetry class recurs at S077 (new finding; complements `R30Overlap.md` A1)

- The card's Q2 row cites **S077** in its body (`:54`, "S077 (canary, per task)") while `:2-7` list S081–S086.
- S077 is `mined`; its `used-by` cell is exactly `corpus/knowledge/benchmark-task-validity-checklist.md`
  (`corpus/SOURCES.md`, S077 row, last cell).
- `adoption_check.py` builds `cited` from `SOURCE_LINE_RE` (`^source:` lines) and computes `usedby_ok` over
  the **expect file's** six ids. A seventh body citation is invisible: the counter prints
  `cited_rows=6 … usedby_ok=1` while the entry cites a row whose `used-by` does not name it.
- That is, **byte for byte, the D5 asymmetry round 30 is closing for S091** — and
  `.ufo/waves/round-30/adoption-expect.json` already carries a `usedby_notes.S091` paragraph for it. C1 would
  open the same class at S077 in the round that closes it.

Options, in predicate order: (i) add S077 to the entry's `source:` header — **excluded**, it breaks C1's
"exactly the six ids … (six distinct)"; (ii) keep the body citation and add the entry path to S077's
`used-by`, recording the asymmetry in the expect file's notes exactly as S091 is recorded; (iii) drop the
S077 clause and source Q2's canary option from S084/S086 alone. Recommendation: (iii) if Q2 can stand without
it; otherwise (ii) — the mechanism already exists, so it costs one cell and one note.

---

## 9. Contradictions to record, not smooth

**X1 — Q7 vs the lane's landed evidence.** Q7 asks "is the item set protected…". The lane holds the opposite
direction twice: `benchmark-saturation-and-lifecycle.md:25-27` (S007: "Hiding test data does not appear to
prevent saturation once benchmarks are widely adopted"), `:44` ("too weak to assume it protects"), `:74`
(Don't), and `CDT:73` (Don't "Treat a private/hidden split as proof of cleanliness"). If the amendment asks
about protection without writing the warning beside it, the entry contradicts two landed entries. Phrase Q7
as *protection **and** a retirement path*, with "protection is not evidence of cleanliness" in the same cell.

**X2 — R1/R2 are not properties of the published card.** The staged registry states, at row **S131**
(`SOURCES.append.md`, Appendix E row): the preprint "states that the CTC covers neither elicitation budget nor
stratification". So N1 and N2 are the lane's synthesis via S081's four-field protocol, **not** fields of the
Contamination Transparency Card. An entry that presents them as CTC fields asserts a property the same
package's own row refutes. Attribute them to S081 F1/F2 and say the published CTC lacks them.

**X3 — `T1–T4` cannot be "resolved" by assertion.** `CDT:70`'s token is en-dashed; `SOURCES.md:23`'s is
hyphenated; the entry that uses it pairs it with *access level* ("its access level and contamination tier",
`CDT:9-11`), while S081's t1–t4 are contamination *types*. No byte I read equates the two taxonomies. An
erratum that defines `:70`'s token as S081's four types would be an in-place semantic change by another
route (R1/R5). The erratum must instead say: the lane's `T1–T4` is **not** defined here; the card states a
distinct four-type set; identity is an open question with a named test (S001's table vs S081's Table
`tab:instrument`).

**X4 — S085 vs `CDT:47-48`.** CDT holds "S004 proposes a direction; it supplies no working
contamination-resistant benchmark today" (`:47-48`) after `:37-38` ("benchmark datasets should be
'contamination-resistant, i.e., unlearnable, but support inference'"). S085 documents a **deployed dynamic
test bank**, which removes the stable target instead of making data unlearnable — a different property. So
S085 neither supersedes nor confirms `:47-48`; the amendment must note the adjacency and must not claim an
upgrade. (`R30Overlap.md` records this as "NEW"; the sharper point is the *tension* with a landed
negative-space line, which is where a careless entry would over-claim.)

---

## 10. Cross-claim interaction C1 × C3 — the CJK cap cannot fail for three of the six rows (now verified in code)

**The prediction, then the check.** Before C3 landed, the concern was that a ≤25-word rule counted by
whitespace would be vacuous for the card's three CJK sources. C3 has since landed, so this is no longer a
prediction. Verified in the landed bytes today:

- `plans/sources_adopt.py:272-273` — `def words(text: str) -> int: return len(text.split())`.
- `:265` `QUOTE_WORDS = 25`; `:49-50` `EXIT_QUOTE_TOO_LONG = 6`, `EXIT_QUOTE_ABSENT = 7`; `:40-47` the
  exit-code ladder.
- Run through the module's own functions against the **landed** registry (`sa.parse_rows` +
  `sa.quoted_spans` + `sa.words`):

| Row | spans found | words per span | cap reachable? |
|---|---|---|---|
| S081 | 3 | 22, 6, 18 | yes (all < 25) |
| S082 | 2 | 11, 17 | yes |
| S083 | 2 | 14, 19 | yes |
| S084 | 3 | **3, 7, 1** | no span can exceed 25 |
| S085 | **0 — reason `no-quote`** | — | structural refusal (exit 4) |
| S086 | 1 | **1** (+ printed-title span 3) | no span can exceed 25 |

So: three of the six cited rows carry CJK spans that are **1–7 whitespace tokens** no matter how long the
sentence is (S084's third span is 24 codepoints in one token; S086's is 30). The ≤25-word refusal cannot fire
for them, and the selftest exercises only the whitespace path: `grep -nP '[\x{4e00}-\x{9fff}\x{3040}-\x{30ff}]'
plans/sources_adopt.py` → **0 hits**, i.e. none of the 14 landed cases contains a CJK fixture. The registry
now holds the lane's first three CJK rows (`grep -cP … corpus/SOURCES.md` → **3**; before today: 0), so the
first customers of the new cap are exactly the rows the cap cannot measure.

**Two defects this surfaces in the landed registry rows, both recoverable without a fetch.** The anchor cells
annotate their own spans in prose, and the gate never reads those annotations (it recounts spans itself), so a
green `--quote-file` run can coexist with wrong annotations:

| Row | annotated | actual `sa.words()` | verdict |
|---|---|---|---|
| S081 span 3 "Two variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type introduced here" | "21 words" | **18** | does not reproduce |
| S084 span 2 "目前该方案仅支持 C-Eval, MMLU, HellaSwag 和 ARC 数据集" | "13 whitespace tokens" | **7** | does not reproduce |
| S084 span 3 "但如今开源社区往往只会公开模型参数而非训练数据集" | "3 whitespace tokens" | **1** | does not reproduce |
| S086 span 1 "一致したものを一律に混入とみなして除去することには疑問が残る" | "23 CJK characters" | 30 codepoints (11 Han + 19 kana) | does not reproduce |
| S084 span 1 / S085 spans 1-2 / S086 title span | 3 / 3, (1 token, 23 CJK) | 3 / 3, (1 token, 23 Han) | reproduce |

Three of six rows carry at least one count that does not reproduce; every one is well under the cap, so
nothing is unsafe — but this is precisely the class QUALITY Q10 ("locations and numbers are re-read by a
second seat") exists for, and the cap's own receipts will not catch it. Repair is one of: delete the
parenthetical counts (the gate prints its own), or re-derive them from `sa.words()`/codepoint counts in the
same run that writes the row — not by eye.

**Compatible synthesis, now one line of code plus one case.** Either make the cap script-aware
(`words()` counts a Han/Kana run as ceil(codepoints/2), or add `cap_cjk = 50` codepoints and refuse on
`max(words, codepoints/2)`), and add one CJK fixture beside case 11 (`quote-overlong-refused`, `:600-615`);
or — if whitespace tokens are the deliberate contract — say so in the gate docstring and in the entry's
`recheck:` line, so no future receipt claims length validation for S084–S086 that did not happen. The first
option costs one case; the second costs one sentence. Either is cheap; leaving it unstated is the only
expensive choice, because C1's kill rule ("a cited source whose located quote cannot be found in this round's
own fetch is refused") is then the *only* real check behind three of the six rows.

Related observation, stated as observation: `grep -n '…' corpus/SOURCES.md` → 2 rows (S027, S036), and both
`…` sit in abbreviated sha/numeric values inside non-quote cells, not inside a quoted sentence. So the
byte-substring rule does not retro-fail those two rows *on that count* — a reading of two rows, not a test of
the rule. One landing caution the same reading produces: `quoted_spans` pairs **ASCII** double quotes only,
so an anchor cell written with curly `“ ”` reports `no-quote`. S085's landed anchor cell is written that way
(see §13 D-b) and is the one row that currently refuses structurally.

---

## 11. Risks

1. **Pointer rot in the delta table.** `CDT`'s own `## Corrections` section (`:85-100`) already appends; a
   future append shifts nothing above it but will shift anything appended below. Cite the **row text**
   ("CDT §How kengaku applies it, 'Reporting a contamination check'") with the line number as convenience,
   and apply R5's erratum discipline to the amendment itself.
2. **Label collision** (Q1–Q8) — two gates under one name, with round-29's flip string already using the
   admission-bar sense.
3. **Attestation laundering** — `opened=2026-10-25` is only honest if the six sources were re-opened today;
   `--attest-opened` records a claim, not a fetch, and the code says so.
4. **Counter blindness** to body citations (S077) — a green C1 can coexist with a D5-class registry
   asymmetry.
5. **Misattribution of R1/R2 to the published CTC** (X2).
6. **Q7 phrased naively** would contradict `benchmark-saturation-and-lifecycle.md:25-27` and `CDT:73` (X1).
7. **Later staging collision.** The same package stages `benchmark-card-field-schema-2026-10-23.md`,
   `maintainer-contamination-disclosure.md`, `per-benchmark-contamination-verdicts-2026-10-23.md` and
   `contamination-mitigation-comparative-evidence-2026-10-23.md` (`MERGE-REPORT.md:20,36,38,61`), two of
   which the staged rows name in `used-by`. None is in the lane, none may be cited today (QUALITY Q7 forbids
   resting on an unlanded working copy), but if any lands later this amendment becomes a partial duplicate —
   decide the naming then, and keep this entry's extension target lane-internal only.

---

## 12. Proposed move (one, bounded) and verification

**Move.** Admit the card as a **self-citing delta amendment**: keep C1's predicate path
`corpus/knowledge/contamination-transparency-card.md`; write **one** table, not two, whose every row carries
either `new (N1…N7/D1)` or `held at <path>:<line>` plus the held row's own words; publish the gate as
**CT1–CT8** (the landed draft used **CG1–CG8**, which is the same fix; §13); carry only N1–N7 + D1 as new content; append a dated erratum to CDT for the `T1–T4` count-without-
listing that leaves `:70` byte-identical and states the identity question as open; keep six `source:` lines
with `verified-at: 2026-10-25`; write each `recheck` cell deliberately (`on-release` for the preprints) so
`sources_adopt.py` does not coerce prose prose to `180d`; append through `sources_adopt.py` so `used-by` is
rewritten to exactly the entry, and use `--attest-opened` only if the six were actually fetched today.

**Why it does not harm the other axes.** Coverage: +6 registry rows, +1 indexed entry, and the frontier bullet
at `README.md:272` moves from *unopened lead* to *core* — a real registry delta. Calibration: the amendment
asserts nothing beyond the six rows' own cells, leaves X3 open rather than resolving it, and cannot pass
without the Q4/Q5 sections the staged file lacks. Operability: it hands C3 a concrete six-row, three-CJK
fixture set and forces the CJK counting decision into the open instead of letting it pass vacuously.

**Update, after the tree moved.** The move above was written before the entry landed; §13 reports what landed
and what it costs. In short: the landed draft already implements the rename (as **CG1–CG8**), the one-table
discipline, the six `source:` lines, `verified-at: 2026-10-25`, and the Q4/Q5/Q6/Q8 sections — so the remaining
delta is **D-a** (the union table's provenance, which is the only structural liability), plus the five
mechanical repairs **D-b…D-f** in §13. Verification items 3–5 below become: no `held at` count is required in
the landed shape (it uses a Status column instead, which is equivalent); `grep -rn 'Q1–Q8'` should show the
admission-bar sense only, with the README row's parenthetical (already present at `:274`) naming the
distinction; and item 6 gains one: run `--quote-file` against the six rows and expect **exit 4 / `S085:no-quote`**
until D-b is repaired.

**Verification (none of it run by me — main agent's step).**
1. `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census` →
   `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, exit 0.
2. `grep -c '^source: S08[1-6]' corpus/knowledge/contamination-transparency-card.md` → `6`.
3. `grep -c 'held at' corpus/knowledge/contamination-transparency-card.md` → one per held cell (expected 8:
   R3/Q1, R5/Q8, S2, Q2, Q3, Q4, Q5, Q7).
4. `grep -rn 'Q1–Q8' corpus/README.md corpus/QUALITY.md corpus/knowledge/*.md` → after the rename, only the
   admission-bar sense remains.
5. `grep -n 'T1' corpus/knowledge/contamination-detection-and-transparency.md` → `:70` unchanged byte-for-
   byte (R1), with the erratum present as an appended section.
6. `python3 plans/sources_adopt.py --selftest` → still the C3 target line; if C3 lands, confirm its CJK case
   exists before C1's rows are cited as validated.

## 13. The landed 39th entry (mtime 04:31, untracked) — audited against §2's matrix

The entry appeared while this scan ran, so it is not in §2's population (it is the object under test, not a
neighbour). Reading `corpus/knowledge/contamination-transparency-card.md` (163 lines,
`writer: KengakuR30`) plus its index row `corpus/README.md:65`, coverage row `:242` and frontier discharge
`:274-275`, and the six registry rows in `corpus/SOURCES.md`:

**What it does better than the staged card, measured against my own list.** (i) It renamed the gate
**CG1–CG8** — the §4 collision is fixed, and the README row says why. (ii) It has `## Extends`,
`## What this does not establish` with a falsifier, `## Attribution`, `## Rejected` and `## Corrections` —
Q4, Q5, Q6, Q8 are all satisfiable from its own bytes, which the staged file could not do. (iii) It **drops
S077**, so my §8 D5-class finding does not reach the landed text (it still applies to the staged file). (iv) It
deletes the staged `T1–T4` claim entirely and uses S081's five types. (v) It states the CJK token counts in the
`source:` lines and the anchor cells instead of silently relying on them — §10's vacuity is now visible in
prose. (vi) Its `## Extends` names `CDT` and quotes the apply row ("prefers 'suites with a documented
transparency card'"), which is the exact extension my §2 Q2-cell and §6 pointed at.

**And it goes further than my N-list, in a direction that needs a decision.** Its field-mapping table
reclassifies N2/N3/N5/N6 from "new statements" to "columns the three published designs already carry", leaving
**only S1 and S2 new as fields and R1 new as a value set** (the entry's own words: "exactly two fields are new
as *fields* … one is new as a *value set*"). That is a defensible and stronger Q6 answer than mine — *if* the
union table it maps into is inspectable by a lane reader. It is not: the entry's own text says the table lives
in `benchmark-card-field-schema-2026-10-23.md` under the merge package, "**not** in this lane's
`corpus/knowledge/`, and its three source rows are not in this lane's registry". So the entry's central claim
rests on an unlanded working copy.

**Defects, each with the byte that shows it** (all fixable inside the entry or its rows; none requires a fetch):

| # | Defect | Evidence | Repair |
|---|---|---|---|
| **D-a** | **Q7 risk.** The amendment's headline ("exactly two fields are new as fields") rests on a staged file outside `corpus/knowledge/` whose rows are not in the registry. `QUALITY.md:56-58`: "no support rests on `/tmp`, `local://` or an unlanded working copy." | entry `:37-47` (the union table) and `:34-40` (the package path and the admission that its rows are not in this registry) | one of: cite the staged file's sha256 beside the path and label the table "this entry's reading of a package file, not a re-derivation"; or land the union table's three columns with their own registry delta; or fall back to §5's N-list, which needs no staged bytes at all |
| **D-b** | **S085's anchor cell cannot be quote-checked at all.** It is written with curly `“ ”`, and `quoted_spans` pairs ASCII `"` only, so the row returns `no-quote` → exit 4 (structural), not the exit 6/7 the entry's `recheck:` implies. Verified by running the landed module: `S085 reason='no-quote' spans=[]`. | `corpus/SOURCES.md`, S085 row anchor cell; `plans/sources_adopt.py:281-293` | replace the curly quotes with ASCII `"` in the S085 anchor cell and the entry's S085 `source:` line; re-run `--quote-file` |
| **D-c** | **Three prose counts do not reproduce** (§10's table): S081 "21 words"→18, S084 "13 whitespace tokens"→7 and "3"→1, S086 "23 CJK characters"→30. The gate recounts spans itself, so a green run coexists with wrong annotations; QUALITY Q10 is the rule that should have caught them. | entry `:1-6` and the same annotations in all six registry anchor cells | delete the parentheses (the gate prints counts) or re-derive them from `sa.words()`/codepoints in the writing run |
| **D-d** | **The `T1–T4` seam is now unmapped in both directions.** The entry uses S081's **five** types; `CDT:70` still says "contamination tier tested (T1–T4)" and `SOURCES.md:23` still says "four-tier … (T1-T4)". Nothing states they are different sets, and a reader can map T1–T4 onto the first four of the five and miss that the fifth (`acquired`) is the run-side type — the exact split the entry exists to make. | entry `:19-23` vs `CDT:70` vs `SOURCES.md:23` | one delta row in the union table: "the lane's `T1–T4` token (CDT:70) is **not** mapped here; S081's set is four release-side types plus `acquired`" — no edit to CDT, so R1/R5 hold |
| **D-e** | **CG2 asks about "a canary" with no source and no lane pointer**, while the lane's only canary bytes are `BTVC:40` and its caveat `BTVC:119-121` ("a canary's presence is detectability, never proof of training-corpus exclusion"). As written, the question re-introduces a term the lane already defines elsewhere and leaves the reader to find it. | entry `:105` (CG2 row) | point CG2's canary option at `benchmark-task-validity-checklist.md:40,119-121`; costs one clause, prevents two vocabularies |
| **D-f** | **Eight union-table cells assert positive facts about three published designs** ("already a column", "already a column in two of three", "narrower") whose tables are not in this lane. Same class as D-a at cell granularity: a reader cannot check any of them from lane bytes. | entry `:41-48` | soften to "the staged table's column set", or land the table (D-a) |

None of D-a…D-f touches the six-source predicate, so C1's counter can be green while all six stand — which is
why they are worth recording in the Gate row rather than only here.

**Verdict on the landed draft.** As an amendment it is structurally correct and answers round 29's flip in the
form the flip asked for (names the extended entry; keeps the designs tabulated rather than replaced). Its one
structural liability is D-a: it converts a content question ("is this a fourth design?") into a **provenance**
question ("can a lane reader see the table you are amending?"). Two admissible shapes follow, and the
discriminator is D-a, not taste: (1) if the union table can be cited verifiably — path + sha256 + explicit
"unlanded" label, or landed with its own registry delta — keep the landed shape, which is the stronger Q6
answer; (2) if it cannot, withdraw the table to a pointer and carry §5's seven statements instead, which are
all anchored in the six rows' own quotes and need nothing outside the lane.

## 14. What I did not do

- Did not fetch or open S081–S086; no quote above is a fetch receipt, and no line is a survival verdict under
  C1's kill rule. Every "does not reproduce" in §10/§13 is a statement about the **strings the lane wrote**, not
  about the sources' bytes.
- Did not run `adoption_check.py`, `sources_adopt.py --selftest`, `sources_adopt.py --quote-file`, or the
  census. What I did run was narrower and says so: I imported `plans/sources_adopt.py` as a module and called
  its pure functions (`parse_rows`, `cell`, `quoted_spans`, `words`) on the landed registry. That produces the
  span/word/`no-quote` facts in §10 and §13; it produces **no exit code** and is not a gate receipt.
- Did not re-write or re-derive any registry row, entry, or README line — read-only throughout; this report is
  the only file I created under the lane.
- Did not adjudicate whether S001's `T1–T4` and S081's `t1–t4` are the same taxonomy — I state it as open (X3).
- Did not read the staged sibling entries' bodies beyond the merge-report index rows and the S131 row, so no
  claim is made about what they contain. `MERGE-REPORT.md`'s adopt-checklist item 5 (quoted in
  `R30Overlap.md`) is the only byte I read about how the package is meant to land.
- Did not verify the landed entry's README rows for wording beyond quoting them, and did not run
  `gate_timing_check.py` — Q13/Q14 need a qualifying reviewer seat, and a connector is explicitly not one
  (`QUALITY.md` Q14's role list).
- Installed or upgraded no tool; `pacman` was not invoked (host-wide pause).

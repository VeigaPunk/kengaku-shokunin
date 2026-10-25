# R30FxEntryQ4Q6 — QUALITY Q4/Q5/Q6 audit of the landed card entry

Seat: `L1Kengaku30.R30FxEntryQ4Q6-3` (reviewer, leaf). Access date for every source opened here:
**2026-10-25**. No model was passed; no lane byte was edited; no subagent was dispatched.

Candidate under audit: `corpus/knowledge/contamination-transparency-card.md`

VERDICT: FAIL

| bar row | verdict | one-line reason |
|---|---|---|
| Q4 negative space | **FAIL** | the only falsifier is aimed at the wrong bullet, is stated over a field pair the entry's own mapping contradicts, and its target sentence converts S081's *reliability* result into a *prevalence* result |
| Q5 source labelling | **FAIL** | S086 is labelled "a peer-reviewed 言語処理学会 paper"; the publisher of that series states its annual-meeting papers are published **without peer review**, and this lane's own registry row claims no review |
| Q6 extends, never duplicates | **FAIL** | the naming half holds; the field mapping calls three published CTC-v1.1 constructs new (R1 strata, S1 acquired, S2 integrity) — the pinned form at the commit the tabulation cites carries all three |

## 0. Bytes audited, and the drift I watched

The entry was being rewritten while I audited it (three distinct hashes in eight minutes). Every
finding below is stated against the **latest** bytes at write time, and I re-located each quoted
sentence in those bytes:

- `sha256 f01b7cd20cf4ebcaf3ee9f7af8b109ace8b86e69002ae53a213c2dc80ad1e6cd`,
  mtime `2026-10-25 04:45:17 -0300` (07:45 UTC), 177 lines.
- Earlier observed states: `0f2e1614…` at 04:43:05 (no sha256 pin, no "field mapping is not
  lane-sourced" bullet, mapping said "**delta**" for S1/S2 and "exactly two fields are new as
  *fields* (S1, S2)"); `df0b6d41…` at 04:44:02 (pin added, `grader integrity` row added, S1
  restated as "**delta in placement, not in field**", "one new field / one new placement / one new
  value set"). The last change (`df0b6d41 → f01b7cd2`) touched only the S085 `source:` cell
  ("three typeset lines, not byte-contiguous") and no sentence I cite.
- Consequence for the Gate: `corpus/lessons/round-30.md:17` scores Q4/Q5/Q6 **pass** against a
  moving target. The bytes I graded are the ones present when this report was written; a later
  edit does not retroactively make the Gate cell true, and it does not make it false either — the
  Gate cell needs re-taking against the admitted commit, not against the working copy.

Admission-side note (not mine to score, recorded for the Q13 seat): the entry is **untracked**
(`git status --porcelain` → `?? corpus/knowledge/contamination-transparency-card.md`).

## 1. Q4 — negative space is written down — **FAIL**

### 1.1 What the section actually says (quoted, latest bytes)

`corpus/knowledge/contamination-transparency-card.md:102-107`:

> - **The layer the card adds is the layer its own source could not validate.** S081's arXiv abstract
>   reports of its own protocol (the compiled paper states the same audit outcome in different words
>   and does not print this sentence): "Two variables fall below the prevalence-robust threshold registered in advance:
>   strata reporting and the acquired type introduced here" — that is R1 (strata) and S1/S2
>   (acquired / integrity) in this entry's own naming. The two fields this entry adds are therefore
>   the two its source measured as rare in practice. A complete card is not a common card.

`:126-129`:

> - **Falsifier:** a benchmark release that publishes a card answering all eight CG questions while
>   its own contamination audit shows the strata and acquired fields are *populated* (not "unknown")
>   and non-trivial would show the two delta fields are not rare in practice, **narrowing the third
>   bullet above.**

### 1.2 Defect A — the falsifier points at the wrong bullet

The section's bullets in order are: 1 *"The card is a format, not a finding"* (`:100`), 2 *"The layer
the card adds…"* (`:102`), 3 *"Agreement is not established"* (`:112`), 4 *"S085 cannot be used as
evidence about anyone else"* (`:116`), 5 *"S082 is a working paper"* (`:121`), 6 *"The field mapping
is not lane-sourced"* (`:124`). **The third bullet is the inter-coder-agreement bullet.** The
falsifier's content ("the two delta fields are not rare in practice") belongs to bullet 2 and has
no bearing on agreement at all. As landed, the entry attaches its one falsifier to a claim about
coder agreement that the falsifier cannot touch, and leaves the rarity sentence it visibly
continues without a falsifier.

*Reproduce:* `sed -n '98,129p' corpus/knowledge/contamination-transparency-card.md` and count the
`- **` bullets before `- **Falsifier:`.

*Repair:* name the bullet by its lead ("narrowing the rarity sentence in the second bullet"), or
delete the pointer.

### 1.3 Defect B — "the two delta fields" denotes two different pairs in adjacent sections

The mapping section (`:69-71`) now states the delta as three parts:

> **one new field** (S2's tri-state integrity flag), **one new placement** (S1 — contamination
> acquired during the run belongs with the reported score…), and **one new value set** (R1's
> strata…)

But the falsifier says "the two delta fields" and names **strata and acquired** (= R1 and S1), while
the mapping says the field this entry adds is **S2**. The rarity bullet (`:105`) repeats the error
on its own axis: "The two fields this entry adds" cannot be the two S081 measured — S081's
below-threshold pair is *strata reporting* and *the acquired type*, so under this entry's naming the
pair is {R1, S1}; S2 appears nowhere in S081's measurement. The entry therefore uses the same
phrase, "the two fields this entry adds / the two delta fields", to denote **{S1, S2} in the
mapping and {R1, S1} in the negative space and in the falsifier**. A reader cannot tell which pair
the falsifier would refute, and the S2 field is conceded to be new while being reported as
source-measured.

### 1.4 Defect C — the target sentence launders a reliability outcome into a prevalence claim

Q4: "An indeterminate or detector-negative result is reported as such, never laundered into a
positive." The entry reports S081's below-threshold pair honestly in the quote and then reads it as
prevalence. The same abstract, fetched today at `https://arxiv.org/abs/2608.29463` (blockquote
`abstract`, 278 whitespace tokens), says in the sentence order it prints:

> Per-variable linear-weighted $\kappa$ runs from 0.00 to 0.35 (median 0.21) over 29 main-pass
> documents … Two variables fall below the prevalence-robust threshold registered in advance: strata
> reporting and the acquired type introduced here. **Disagreement concentrates on when a variable
> applies rather than on what a document states.**

"Prevalence-robust threshold" is an *agreement* threshold robust to prevalence, and the source
locates its own failure in coders disagreeing about *applicability*. The entry's rendering —
"the two its source measured as rare in practice" (`:106`) — turns that into a statement about how
often the fields are populated. The entry's own bullet 3 then restates the same instrument as
"modest and skew-sensitive", i.e. the entry knows the result is a reliability result and still
uses it as a prevalence result two sentences earlier. `[INFERENCE]` on the term's meaning; the
supporting evidence is the source's own next sentence, quoted above.

*Repair:* say what S081 measured ("two variables did not clear its pre-registered agreement floor,
with disagreement concentrated on applicability"), and drop "measured as rare in practice".

### 1.5 Defect D — the falsifier is not decidable, and no falsifier reaches the Claim

Three separate gaps:

1. **No population, no n.** The rarity sentence inherits "in practice" from a 41-document audit
   (29 main-pass) that the entry never states; its own source prints both numbers. QUALITY Q10's
   standard for numbers ("exact cells or a stated range, never an approximation") is not met by an
   unquantified "rare in practice".
2. **No decision rule.** "populated (not 'unknown') and non-trivial" defines neither *non-trivial*
   nor how many releases, how many strata, or what n would break the claim. Compare the round-29
   standard the lane already enforces (Q18: name the measured unit, population and category rule
   before seeing output) — as written, two auditors can score the same release differently.
3. **The Claim has no falsifier.** The Claim (`:13-26`) is the split rule: "that record has two
   halves **that cannot be merged**". Nothing in §What this does not establish names an observation
   that would refute *that*. The one named falsifier is confined to the delta-field rarity. Q4 says
   "the observation that would falsify **the claim**"; the entry supplies one for a supporting
   observation only. (A candidate the entry could have used: a benchmark whose run-side exposure was
   reconstructed from release-side artefacts alone — that would undercut "cannot be merged". Note
   also that S081 states *placement* ("must be recorded with the reported score rather than with
   the benchmark release"), not an impossibility of one document carrying both halves — yet this
   entry's own card is exactly such a document, so "cannot be merged" is stronger than its quote
   and narrower than its design. `[INFERENCE]` on the reading of "merged".)

### 1.6 What Q4 does carry

For the record, the negative-space half is otherwise real and I am not scoring it as missing: six
bullets, four of them genuine limits (S085's self-report, S082's working-paper status, S083's
single-benchmark design, S081's agreement), and the below-threshold pair is **not** hidden — it is
quoted. The failure is entirely in the falsifier and in the one sentence that repurposes the
negative.

## 2. Q5 — every source is labelled for what it is — **FAIL**

### 2.1 The three legs the task names, verified

| leg | entry text | what I found | verdict |
|---|---|---|---|
| CAICT on its own programme | `:136` "S085 is a self-report by the China Academy of Information and Communications Technology about its own benchmark programme" + `:116-118` "the sponsoring body's own 2024 description of its own programme: no document number, no measurements, no data release" | re-fetched `P020240711534708580017.pdf` (1 949 572 bytes): cover carries 中国信息通信研究院 / 人工智能关键技术和应用评测工业和信息化部重点实验室; 图 2 自适应动态测试方法原理图 is captioned 来源：中国信息通信研究院; p.35 (printed 30) reads 信通院于 2024 年初启动"方升"首轮试评测. The programme is the publisher's own | **holds** |
| OpenCompass docs on its own procedures | `:134-135` "S084 is vendor documentation for OpenCompass 0.4.0 (a self-description of two procedures, not an evaluation of any model)" | re-fetched the doc page: it describes two 数据污染评估 methods and their dataset limits; the page footer prints `0.4.0 documentation`, matching the version label on a `/latest/` URL | **holds** (note: OpenCompass is an open-source project, so "vendor" is loose; the substance — self-description, not evaluation — is right) |
| preprint vs peer-reviewed split | `:133-137`: S081/S082 "arXiv preprints (a taxonomy paper and a working paper)"; S083 "a peer-reviewed Findings of EACL 2026 paper"; S086 "a peer-reviewed 言語処理学会 paper" | S081 abs page carries no venue, only "18 pages, 3 figures, 6 tables" → preprint ✓. S082 full text self-labels "**Working Paper \| May 2026**" (`arXiv:2607.01254v2 [cs.CY] 13 Jul 2026`) ✓. S083 is ACL Anthology Findings ✓ | **split labelled, one side wrong** — see 2.2 |

### 2.2 Defect — S086 is labelled peer-reviewed; the publisher says otherwise

`:136-137`: "S086 is a peer-reviewed 言語処理学会 paper on code-corpus contamination." The Gate
repeats it (`corpus/lessons/round-30.md:17`: "S081/S082 preprints vs S083/S086 peer-reviewed").

Evidence against:

1. **The society's own published policy for its annual meeting.** `https://www.anlp.jp/nlp2026/submit.html`
   (fetched today) states that submitted manuscripts are published CC BY 4.0 with the stamp:
   > This work is published without peer review and is licensed by the author(s) under CC BY 4.0
   The 発表論文集 at issue (第31回年次大会, `https://www.anlp.jp/proceedings/annual_meeting/2025/`) is the
   same series.
2. **Nowhere on the 2025 material.** `submit.html`, `summary.html` and the proceedings index for
   NLP2025 contain **0** occurrences of 査読; the society's 査読 apparatus (査読要領, 論文査読倫理綱領,
   `https://www.anlp.jp/guide/`) belongs to the journal 自然言語処理, a different publication.
3. **This lane's own row does not claim it.** `corpus/SOURCES.md:112` (S086) records kind `paper`,
   tier `A`, scope "the paper's own contamination-detection method and its false-positive caveat",
   and no review status. The label exists only in the entry's Attribution.
4. S086's own PDF (re-fetched, 371 155 bytes) carries the conference header
   `言語処理学会 第31回年次大会 発表論文集（2025年3月）` and no review statement.

`[INFERENCE]` the 2025 proceedings follow the same no-review regime as the 2026 call, for which
there is a printed statement. The finding does not need the inference to stand: Q5 requires a label
that says what the source **is**, and the entry asserts a review status that neither the source, its
publisher's current statement, nor the lane's registry establishes — while the nearest published
statement of the same series' policy says the opposite. A tier-A conference paper is a perfectly
good source without the "peer-reviewed" badge, so the cost of removing it is zero and the cost of
keeping it is a false provenance claim in the one section whose job is provenance.

*Repair:* "S086 is a 言語処理学会 第31回年次大会 発表論文集 paper (conference proceedings, not
peer-reviewed — the society publishes annual-meeting manuscripts without peer review)"; make the
same correction in the Gate cell.

### 2.3 A second labelling residue (minor)

`:19` attributes the CG gate's provenance as `corpus/QUALITY.md` Q1–Q8 in the same breath as the
frontier's "gate a knowledge entry on Q1–Q8", and the gate is renamed CG1–CG8 to avoid the collision
— that part is correct and I verified the labels do not collide in the landed bytes
(`grep -c 'CG[1-8]'` on the entry runs; `QUALITY.md` has no CG ids). No finding.

## 3. Q6 — extends, never duplicates or overwrites — **FAIL**

### 3.1 The naming half holds (verified, not asserted)

`corpus/knowledge/contamination-transparency-card.md:142-147` names both objects:

> `corpus/knowledge/contamination-detection-and-transparency.md` (tier/access vocabulary, and its
> "How kengaku applies it" row that prefers "suites with a documented transparency card" — the card
> was named there and is defined here), and the union table of the campaign's round-6 staging file
> `benchmark-card-field-schema-2026-10-23.md` (continued, not re-derived; its rows are staged, not in
> this lane's registry). Coverage map: `corpus/README.md` row *Contamination transparency card
> format*. New: `Contamination transparency card format`.

Checks I ran:

- `corpus/knowledge/contamination-detection-and-transparency.md:14` — "keep a transparency record
  rather than report \"clean\""; `:73` — "Prefer suites with a documented transparency card or
  auditable construction". Both phrases exist; neither is defined in that entry (no definition of
  "card" anywhere in its 100 lines). The entry's description of what it extends is accurate.
- `corpus/README.md:65` (index row, anchored `| \`knowledge/contamination-transparency-card.md\` |`)
  and `:242` (coverage row "*Contamination transparency card format*") both exist.
- The staged tabulation's pin is real: `:39` prints
  `sha256 66651007989a7fb5df4671f5f86e69ab1436517025a821afe8c451641a3533b9`; `sha256sum` of
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md`
  returns exactly that hash. The `grader integrity` row that a sibling seat found dropped
  (`R30FxPriorArt.md:51`) is now carried and justified (`:63`), so that omission is closed.

### 3.2 The mapping overclaims: all three "new" items are in the published CTC v1.1 form

The entry's delta sentence (`:69-73`):

> **one new field** (S2's tri-state integrity flag), **one new placement** (S1 — contamination
> acquired during the run belongs with the reported score; the CTC form carries it as a per-type
> value inside a release-side artefact, not as a score-side record), and **one new value set**
> (R1's strata, **which no design tabulates** and whose own source records this lane's first failure
> with it)

The tabulation's CTC column points at `templates/disclosure.yaml`, commit `4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6`
(`benchmark-card-field-schema-2026-10-23.md:2`). I fetched that exact blob
(`raw.githubusercontent.com/Jangulo7/contamination-disclosure-paper/4dba1ed…/templates/disclosure.yaml`,
2 181 bytes, head `# Contamination Disclosure v1.1`, `disclosure_version: "1.1"`). Findings, field
by field:

| entry field | entry status | published CTC v1.1 bytes | verdict |
|---|---|---|---|
| **R1 strata** | "**delta**"; CTC cell `(absent)`; prose "no design tabulates" | `:16-22` — a full block: `strata_reported:` / `reported: true` ("false is an answer; make it visible") / `strata: []` ("e.g. [\"disease_category_A\", \"...\"]") / `aggregate_only: false` / `definition:` ("what defines a stratum") / `pre_registered: false` / `scores: {}` ("{stratum_name: {n: 0, score: 0.0, ci95: [0.0, 0.0]}}") | **mislabelled.** A published design does tabulate strata, with definition, pre-registration, aggregate-only marker and per-stratum CIs — a *value set*, exactly what the prose says no design carries. The `(absent)` cell is false, not merely unverified |
| **S1 acquired** | "delta in placement" | `:40-47` — `# Type 5 is evaluation-time: a property of THIS run, not of the benchmark.` / `# No benchmark author can answer this for you.` / `acquired: "unknown"` / `network_access_during_eval` / `environment_sanitised` / `transcripts_reviewed` / `boundary_integrity_monitored` / `notes` | **mislabelled.** The prose's parenthetical — "inside a release-side artefact, not as a score-side record" — is contradicted by the form's own comment: the form is keyed per run (`benchmark.name/version/doi`, `:9-13`; `system_under_test`, `evaluation_date`, `:13-14`) and its Type-5 block is explicitly the run-side half. The staged S1's value list ("network access, environment sanitisation, transcript review or boundary monitoring — with the elements actually stated recorded in `notes`", staged `:42`) is a 5-of-5 restatement of those keys |
| **S2 integrity** | "one new field — a state for the card itself" | `:38` declares the per-type value set `# controlled \| not_controlled \| unknown \| n/a`; `acquired: "unknown"` (`:42`) is the tri-state on the acquired claim; `boundary_integrity_monitored: ""` (`:46`) is the monitoring record the staged S2's rationale names | **mislabelled.** The published form already carries a tri-state on the Type-5 claim plus the monitoring field; what S2 adds is a *relabel*, and the entry's own CTC cell ("`unknown` / `not_controlled` are valid values") says so |

Net: against the pinned form the honest delta is **zero new fields**; against the round-6
tabulation alone (which never had R1/S2/R4 rows) the honest statement is "not in the recorded
table", not "no design tabulates". Either way the sentence "That is what an amendment looks like; a
design would have claimed all eight" (`:73`) rests on a delta that does not exist.

### 3.3 Two cell errors in the same table (under-claiming, and resolvable to wrong fields)

- **R4 regeneration status** maps CTC → `evaluation_date` (`:66`). The form has a dedicated
  `regeneration:` block (`:49-53`: `procedure_published`, `procedure_url`, `artifact_only`,
  `notes`) — the actual published home of R4. The GEM cell "Reproducibility" is also wrong: GEM's
  Table 3 Reproducibility is "Exact prompt templates; few-shot example ordering and count; scoring
  procedure; multi-run variance; generation parameters" (re-fetched `acm.org`/`aclanthology`
  `2026.gem-main.50.pdf`, Table 3) — no regeneration requirement. So "already a column, narrower"
  is wrong in both directions: R4 is a *full* published CTC column, and not a GEM column.
- **R5 instrument currency** ("the date of the benchmark's last substantive update", staged `:36`)
  maps CTC → `evaluation_date`, which the form defines as the **evaluation's** date for a
  `system_under_test`. The form has no benchmark-update date (only `benchmark.version`). R5's real
  home is the AI Alliance template's "Release date"/"Change log".
- Consequence for the "already a column in two of three" counts: R2 stands (CTC `elicitation_budget`,
  GEM Reproducibility); R5's CTC leg is a conflation and R4's GEM leg does not exist, so the table's
  "in two of three" labels are not safe as *counts* even where the individual rows are defensible.

### 3.4 "Continued, not re-derived" vs what the table does

`:45` says "The union table is continued, not re-derived", while `:41-43` says "What the mapping
below records is this entry's reading of a staged document". Both cannot describe the same table:
four of its rows (R4, S2, R1 — and the S1 placement claim) carry design cells that the round-6
table never tabulated (`benchmark-card-field-schema-2026-10-23.md:73-78` has six rows: detector
access, negative space, release-vs-score, elicitation budget, instrument currency, grader). Those
cells are this entry's own reading of the three designs — which is legitimate, and is exactly the
sense in which the table is *re-derived* for those rows. Three of the four new cells are then wrong
(§3.2/§3.3), so the wording matters: "continued" implies the cells were inherited; they were not,
and nothing in the entry discloses where the new cells came from.

### 3.5 What would turn Q6 green

1. Delete the delta claim, or restate it against the pinned form: R1/S1/S2 are carried by CTC v1.1
   (`strata_reported:`, the Type-5 block, `boundary_integrity_monitored:`); the honest novelty is
   the *gate* (CG1–CG8), which is an instrument over the fields, not a field.
2. Correct the R4 and R5 cells (`regeneration:` block; AI Alliance "Release date"/"Change log").
3. Replace "continued, not re-derived" with what is true: rows 1–2, R2, R5 and grader inherit the
   round-6 cells; R1, R4 and S2 are cells this entry read out of the three designs, with the URL
   and key names given per row.

## 4. Adjacency (out of my scope, consequential for the round)

- **The Gate's Q4/Q5/Q6 cells are all "pass"** (`corpus/lessons/round-30.md:17`), and the Q6 cell
  says "the delta is stated as **one field**, one placement, one value set" — which is neither the
  entry's earlier "two fields" nor a statement about *which* field, so the Gate cannot be read as
  endorsing or rejecting §3.2 either way. The cells need re-taking against the admitted commit.
- **Gate citations point at reports that do not exist yet.** `corpus/lessons/round-30.md:15-21`
  cites `falsify/R30FxEntryCompleteSet.md`, `R30FxRowsCensus.md`, `R30FxSrcS085.md` and
  `falsify/swarm-registry.json`; `ls .ufo/waves/round-30/falsify/` today shows none of those four
  (it shows `R30FxSrcS08{1,2,3,4,6}.md`, `R30FxQuotes.md`, `R30FxPriorArt.md`, …). Q13/Q14 is the
  seat for that; I record it because this report is one of the paths the lesson cites, and a
  citation to this file is not an endorsement of any cell.
- **`build/R30RevEntryQ1Q6.md:165,188,208` already scored Q4/Q5/Q6 FAIL** — against the 92-line
  staged text, before this entry existed. Several of its findings are now discharged (the sections
  exist; the Attribution exists; Extends names both objects). My verdicts above are new defects in
  the landed bytes, not restatements of that review.
- **The S086 label propagates.** The Gate repeats "S083/S086 peer-reviewed", and `SOURCES.md:112`
  (S086's `teaches` cell) is silent on review status. Fixing the entry alone leaves the Gate
  asserting it.

## 5. Residual risk and verification gaps

- I did not edit, stage or run any lane gate; I did not touch `.ufo/state`, `MANIFEST.json` or any
  sibling lane. No tool was installed or upgraded (used the pre-existing `curl` and poppler
  `pdftotext`; nothing recorded to report).
- **GEM leg is read, not exhaustively scanned.** I extracted Table 3 (`Training Data /
  Decontamination / Evidence Provided / IFT Stage / Reproducibility`) and their required
  disclosures from the PDF; I did not search the whole 819 KB document for the word "strata" outside
  Table 3 §7 (the review uses "stratified evidence" about its own synthesis at `:131`, `:387`, which
  is not a card field). If a GEM field outside Table 3 carries per-stratum disclosure, §3.2's R1
  finding is unaffected (CTC already carries it) but the R3/negative-space GEM cells would deserve
  a second look.
- **AI Alliance template is grep-level, not full-read.** I searched the rendered page for
  `strata|stratif|breakdown|subset` (0 hits) and confirmed the two fields the entry cites
  ("Contamination controls", "Checks performed, their coverage, and known gaps", "Release date",
  "Change log", both at `:50-56` and `:80-81` of the rendered text). I did not enumerate every
  template field, so §3.2's claim is "CTC carries R1", not "no template field could".
- **The 2025-vs-2026 review regime is an inference** (§2.2), flagged inline. If someone produces a
  2025 call for papers that says otherwise, the S086 label becomes merely unsupported rather than
  contradicted — the Q5 verdict stands either way, because the entry offers no evidence for it.
- **The entry moved under me.** The hash in §0 is the state I graded; if it moves again, §1.1's
  quotes and §3.2's table should be re-located before this report is cited at closure.

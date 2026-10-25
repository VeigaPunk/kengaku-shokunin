# R30FxEntryQ4Q6 — QUALITY Q4/Q5/Q6 audit of the landed card entry

Seat: `L1Kengaku30.R30FxEntryQ4Q6-3` (reviewer, leaf). Access date for every source opened here:
**2026-10-25**. No model was passed; no lane byte was edited; no subagent was dispatched.

Candidate under audit: `corpus/knowledge/contamination-transparency-card.md`

VERDICT: FAIL

| bar row | verdict | one-line reason |
|---|---|---|
| Q4 negative space | **FAIL** | the one falsifier is aimed at the wrong bullet, is stated over a "delta" field pair the entry's own mapping no longer has, sets no measurement or decision rule, and no falsifier reaches the Claim |
| Q5 source labelling | **FAIL** | S086 is labelled "a peer-reviewed 言語処理学会 paper"; the publisher of that series stamps its annual-meeting papers "published without peer review", and this lane's own registry row claims no review |
| Q6 extends, never duplicates | **FAIL** on the admitted tree | the naming half holds; the field mapping called three published CTC-v1.1 constructs new (R1 strata, S1 acquired, S2 integrity), and the pinned form carries all three |
| Q6 (live worktree) | **FAIL, narrowed** | R1 and R4 cells have been repaired in the uncommitted worktree; **S2's "only new field" claim survives, and it is falsified by the same form** |

## 0. Bytes audited, and the drift I watched

The entry was rewritten under me while I audited it — five distinct hashes recorded, a commit in the
middle of it, and further uncommitted edits after. Two objects matter, and I grade both:

| object | bytes | state |
|---|---|---|
| **admitted tree** — commit `623c1fc` ("round-30: assimilation round 2 …") | entry `sha256 f01b7cd20cf4ebcaf3ee9f7af8b109ace8b86e69002ae53a213c2dc80ad1e6cd`, 177 lines, blob `43001f5` | the tree the Gate's admission record points at; **this is what my verdicts are stated against** |
| **live worktree** | entry `sha256 ba0465d1cbcbb0b62529343a7c4fe5c4c26e37db6fd462ac93a8e9d95f106d82`, `git status` → `M` | supersedes the committed entry with repairs made after the admit; not yet committed |

Hashes observed on the way: `0f2e1614…` (04:43:05Z−3, no sha256 pin, mapping said "exactly two
fields are new as *fields* (S1, S2)"), `df0b6d41…` (04:44:02, pin + `grader integrity` row + "one new
field / one new placement / one new value set"), `f01b7cd2…` (04:45:17, **committed** at `623c1fc`),
`211e5bcd…`, `b29eac97…`, `ba0465d1…` (worktree repairs: R1/R4/S1 cells, rarity bullet, Extends caveat; checked at `ba0465d1`).

Consequence for the Gate, stated plainly: `corpus/lessons/round-30.md:64-66` scores Q4/Q5/Q6 **pass**
("Q4 pass (§What this does not establish, six bullets including the **two-delta-field** concession and
a named falsifier) … Q6 pass (§Extends names both objects; the delta is stated as one field, one
placement, one value set)") against a tree that has since been replaced twice — and the two Gate
phrases disagree with each other about the same entry, one counting two delta *fields* and the other
one field plus a placement plus a value set. The lesson itself is uncommitted
(`M corpus/lessons/round-30.md`). §4 records, finding by finding, which of my defects the later edits
have repaired and which are still live in the worktree; a gate cell re-taken at `623c1fc` is what the
round's own Q13/Q15/Q16 machinery grades.

Sibling seats converged on parts of the Q6 finding independently — `falsify/R30FxCoverageAxis.md:12`
and `:237`, `falsify/R30FxEntryQ1Q3.md:199` and `:206-211` read the same CTC form and reached the same
R1/S1/R4 repairs. I cite them rather than claim those two findings as mine; what remains mine and
still unfalsified by anyone is Q4 (all four defects), the S086 label, and S2.

## 1. Q4 — negative space is written down — **FAIL**

### 1.1 What the section says (admitted tree, quoted)

`corpus/knowledge/contamination-transparency-card.md` at `623c1fc`, `:108-113`:

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

Bullet order in that tree: 1 *card is a format…* (`:106`), 2 *layer the card adds…* (`:108`),
3 *Agreement is not established* (`:114`), 4 *S085 cannot be used…* (`:118`), 5 *S082 is a working
paper* (`:121`), 6 *field mapping is not lane-sourced* (`:123`), then the falsifier.

### 1.2 Defect A — the falsifier points at the wrong bullet (live)

**The third bullet is the inter-coder-agreement bullet.** The falsifier's content — "the two delta
fields are not rare in practice" — belongs to bullet 2 and says nothing about agreement. As landed,
the entry attaches its only falsifier to a claim it cannot touch, leaving the rarity sentence it
visibly continues unfalsified.

*Reproduce:* `git show 623c1fc:corpus/knowledge/contamination-transparency-card.md | sed -n '98,130p'`
and count the `- **` bullets before `- **Falsifier:`.

*Live:* unchanged in the worktree — the pointer still reads "narrowing the third bullet above"
(`sha ba0465d1…`, `:135-136`), and the third bullet there is still the agreement bullet.

### 1.3 Defect B — "the two delta fields" is stale in both trees (live)

- Admitted tree: the mapping says the delta is **three parts** — "one new field (S2's tri-state
  integrity flag), one new placement (S1 …), and one new value set (R1's strata…)" (`:70-74`) — while
  the falsifier counts "**the two** delta fields" and names **strata and acquired** (R1+S1).
- Live worktree: the mapping now says "**S2's tri-state integrity flag is the only new field**", and
  the rarity bullet sets S081's pair against it ("the two fields S081 measured as rare are the two
  this entry marks as already-columned"). The falsifier has not been updated: it still counts two
  delta fields, and the pair it names (strata, acquired) is now by the entry's own text *not* the
  delta.

So in the admitted tree the falsifier and the mapping disagree about how many new fields exist
(two vs three parts, and the pair {R1,S1} vs {S1,S2}); in the live tree they disagree about whether
the named pair is a delta at all (one vs two). Either way the falsifier cannot be evaluated against
the claim it is filed under.

### 1.4 Defect C — the rarity sentence converted a reliability result into a prevalence result (repaired live)

In the admitted tree, `:112-113` reads "The two fields this entry adds are therefore the two its
source measured as **rare in practice**." The source says, in its own order (re-fetched today,
`https://arxiv.org/abs/2608.29463`, `blockquote.abstract`, 278 whitespace tokens):

> Per-variable linear-weighted $\kappa$ runs from 0.00 to 0.35 (median 0.21) over 29 main-pass
> documents … Two variables fall below the prevalence-robust threshold registered in advance: strata
> reporting and the acquired type introduced here. **Disagreement concentrates on when a variable
> applies rather than on what a document states.**

A "prevalence-robust threshold" is an *agreement* threshold that survives prevalence change, and the
source locates its failure in coders disagreeing about applicability. Rendering that as "measured as
rare in practice" reports a reliability outcome as a prevalence finding — Q4's "an indeterminate or
detector-negative result is reported as such, never laundered into a positive", one step removed
(the negative is quoted and then repurposed).

*Live:* repaired. The worktree bullet now states the population ("over a 41-document, five-variable
population in which three variables clear it") and drops "rare in practice" from the S081 restatement
while keeping "A complete card is not a common card". I record the repair and do not count it again.
The population numbers are consistent with the abstract I fetched (41 documents, 29 main-pass,
five variables).

### 1.5 Defect D — the falsifier is not decidable, and none reaches the Claim (live)

1. **No decision rule.** "populated (not 'unknown') and non-trivial" defines neither *non-trivial*
   nor how many releases, strata or items would count. The lane's own standing standard for exactly
   this failure is Q18 ("name the measured unit, population and category rule … If the frozen wording
   admits incompatible outcomes, record the forecast UNSCORABLE"): as written two auditors can score
   the same release differently, so no observation can settle the claim.
2. **No denominator in the admitted tree.** "in practice" inherited an unstated 41-document audit;
   the worktree fix supplies it for the *rarity* bullet but not for the falsifier, which still names
   no population.
3. **The Claim has no falsifier.** The Claim (`:13-27`) is the split rule — "that record has two
   halves **that cannot be merged**". Nothing under §What this does not establish names an
   observation that would refute *that*; the single falsifier is confined to delta-field prevalence.
   Q4 asks for "the observation that would falsify **the claim**". A candidate the entry could have
   used: a benchmark whose run-side exposure was reconstructed from release-side artefacts alone.
   Related: S081 states *placement* ("must be recorded with the reported score rather than with the
   benchmark release"), not that one document cannot carry both halves — yet this entry's card is
   exactly such a document, so "cannot be merged" is stronger than its quote and inconsistent with
   its own design. `[INFERENCE]` on the reading of "merged"; the quotes are exact.

### 1.6 A live presentation defect in the same section (Q4's own surface)

In the worktree (`sha ba0465d1…`, `:120`) the agreement bullet is emitted as:

```
- **- **Agreement is not established.** S081's own abstract reports a test–retest ceiling "collapsing under
```

A doubled bullet marker: the edit that replaced the bullet's text left the old marker behind. It
renders as literal `- **Agreement is not established.**` inside a bold run. If this lands, the
section reads as malformed markdown in the very section Q4 grades. (Not present at `623c1fc`.)

### 1.7 What Q4 carries, for the record

The negative-space half is real and I am **not** scoring it as missing: six bullets, four of them
genuine limits (S085's self-report, S082's working-paper status, S083's single-benchmark design,
S081's agreement), and the below-threshold pair is quoted rather than hidden. The failure is located
entirely in the falsifier and (in the admitted tree) in the one sentence that repurposed the
negative.

## 2. Q5 — every source is labelled for what it is — **FAIL**

### 2.1 The three legs the task names, verified

| leg | entry text | what I re-opened | verdict |
|---|---|---|---|
| CAICT on its own programme | `:136` "S085 is a self-report by the China Academy of Information and Communications Technology about its own benchmark programme"; `:116-118` "the sponsoring body's own 2024 description of its own programme: no document number, no measurements, no data release" | re-fetched `P020240711534708580017.pdf` (1 949 572 bytes): cover carries 中国信息通信研究院 / 人工智能关键技术和应用评测工业和信息化部重点实验室; 图 2 自适应动态测试方法原理图 captioned 来源：中国信息通信研究院; p.35 (printed 30) reads 信通院于 2024 年初启动"方升"首轮试评测. The programme is the publisher's own | **holds** |
| OpenCompass docs on its own procedures | `:134-135` "S084 is vendor documentation for OpenCompass 0.4.0 (a self-description of two procedures, not an evaluation of any model)" | re-fetched the doc page: two 数据污染评估 methods with their dataset limits; footer prints `0.4.0 documentation`, matching the version label on a `/latest/` URL; all three quoted spans present | **holds** (OpenCompass is an open-source project, so "vendor" is loose; the substance — self-description, not evaluation — is right) |
| preprint vs peer-reviewed split | `:133-137`: S081/S082 "arXiv preprints (a taxonomy paper and a working paper)"; S083 "a peer-reviewed Findings of EACL 2026 paper"; S086 "a peer-reviewed 言語処理学会 paper" | S081 abs page carries no venue, only "18 pages, 3 figures, 6 tables" → preprint ✓; S082's full text self-labels "**Working Paper \| May 2026**" (`arXiv:2607.01254v2 [cs.CY] 13 Jul 2026`) ✓; S083 = ACL Anthology Findings ✓ | **split labelled; one side wrong** — §2.2 |

### 2.2 Defect — S086 is labelled peer-reviewed; the publisher says otherwise (live in both trees)

Admitted tree `:136-137` (identical in the worktree, `:144`): "S086 is a peer-reviewed 言語処理学会
paper on code-corpus contamination." The Gate repeats it (`corpus/lessons/round-30.md:65`: "S081/S082
preprints vs S083/S086 peer-reviewed"), and a sibling second-seat report repeats it again
(`falsify/R30FxRowsCensus.md:167`: "S086 | A | peer-reviewed proceedings paper for its own method and
caveat") — so the label is now carried by three round-30 artefacts.

Evidence against:

1. **The society's published policy for its annual meeting.** `https://www.anlp.jp/nlp2026/submit.html`
   (fetched today) prints the stamp it applies to accepted manuscripts:
   > This work is published without peer review and is licensed by the author(s) under CC BY 4.0
   The 発表論文集 at issue (`https://www.anlp.jp/proceedings/annual_meeting/2025/`, 第31回年次大会) is the
   same series; nothing on the 2025 site distinguishes its review regime.
2. **Nowhere on the 2025 material.** `submit.html`, `summary.html` and the NLP2025 proceedings index
   contain **0** occurrences of 査読. The society's 査読 apparatus (査読要領, 論文査読倫理綱領,
   `https://www.anlp.jp/guide/`) governs the journal 自然言語処理, a different publication.
3. **This lane's own row does not claim it.** `corpus/SOURCES.md:112` (S086) records kind `paper`,
   tier `A`, scope "the paper's own contamination-detection method and its false-positive caveat" —
   no review status. The label exists only in the entry, the Gate and the census report.
4. **S086's own PDF** (re-fetched, 371 155 bytes) carries `言語処理学会 第31回年次大会 発表論文集（2025年3月）`
   and no review statement.

`[INFERENCE]` that the 2025 proceedings follow the same no-review regime, on the strength of the
2026 call. The finding does not depend on it: Q5 requires a label that says what the source **is**,
and "peer-reviewed" is a provenance claim no artefact in this round supports, contradicted by the
nearest published statement of the series' policy. A tier-A conference paper stands on its own
evidence; the badge buys nothing and risks the one section whose job is provenance.

*Repair:* "S086 is a 言語処理学会 第31回年次大会 発表論文集 paper (conference proceedings; the society
publishes annual-meeting manuscripts without peer review)"; correct the Gate cell and
`R30FxRowsCensus.md:167` in the same pass.

### 2.3 A labelling detail that does hold, and one that is loose

- The gate rename is correct and I verified it: the entry's gate is CG1–CG8 throughout, and
  `corpus/QUALITY.md` has no CG ids, so the two Q1–Q8 label sets no longer collide.
- "sponsoring body" (S085) and "vendor" (S084) are loose words for, respectively, *publisher/operator*
  and *open-source project*. Neither overclaims independence; no finding.

## 3. Q6 — extends, never duplicates or overwrites — **FAIL (admitted tree)**

### 3.1 The naming half holds (verified, not accepted)

Admitted tree `:142-147`:

> `corpus/knowledge/contamination-detection-and-transparency.md` (tier/access vocabulary, and its
> "How kengaku applies it" row that prefers "suites with a documented transparency card" — the card
> was named there and is defined here), and the union table of the campaign's round-6 staging file
> `benchmark-card-field-schema-2026-10-23.md` (continued, not re-derived; its rows are staged, not in
> this lane's registry). Coverage map: `corpus/README.md` row *Contamination transparency card
> format*. New: `Contamination transparency card format`.

Checks run:

- `corpus/knowledge/contamination-detection-and-transparency.md:14` — "keep a transparency record
  rather than report \"clean\""; `:73` — "Prefer suites with a documented transparency card or
  auditable construction". Both phrases exist and neither is defined in that entry, so the entry's
  account of what it extends is accurate.
- `corpus/README.md:65` (anchored index row) and `:242` (coverage row) both exist.
- The tabulation's pin is real: `:39` prints `sha256 66651007989a7fb5df4671f5f86e69ab1436517025a821afe8c451641a3533b9`,
  and `sha256sum` of `…/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md`
  returns exactly that hash. The `grader integrity` row a sibling found dropped
  (`falsify/R30FxPriorArt.md:51`) is now carried with a reason (`:61`).

### 3.2 The mapping overclaims: the published CTC v1.1 form carries the "new" fields

The tabulation's CTC column points at `templates/disclosure.yaml`, commit
`4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6` (`benchmark-card-field-schema-2026-10-23.md:2`). I fetched
that blob (`raw.githubusercontent.com/Jangulo7/contamination-disclosure-paper/4dba1ed…/templates/disclosure.yaml`,
2 181 bytes, head `# Contamination Disclosure v1.1`, `disclosure_version: "1.1"`).

| entry field | admitted-tree status | published CTC v1.1 bytes | verdict |
|---|---|---|---|
| **R1 strata** | cell `(absent)` in all three designs; prose "which **no design tabulates**" (`:73-74`) | `:16-22` — `strata_reported:` / `reported: true` ("false is an answer; make it visible") / `strata: []` / `aggregate_only: false` / `definition:` ("what defines a stratum") / `pre_registered: false` / `scores: {}` ("{stratum_name: {n: 0, score: 0.0, ci95: [0.0, 0.0]}}") | **mislabelled in the admitted tree.** A published design does tabulate strata *as a value set* — definition, pre-registration, aggregate-only flag, per-stratum CIs. Repaired in the worktree (CTC cell now `` `strata_reported` ``) |
| **S1 acquired** | "**delta** — the run-side half" | `:40-47` — `# Type 5 is evaluation-time: a property of THIS run, not of the benchmark.` / `# No benchmark author can answer this for you.` / `acquired: "unknown"` / `network_access_during_eval` / `environment_sanitised` / `transcripts_reviewed` / `boundary_integrity_monitored` / `notes`; the form itself is per-run (`benchmark.name/version/doi` `:9-13`, `system_under_test`, `evaluation_date` `:13-14`) | **mislabelled in the admitted tree.** The staged S1's value list — "network access, environment sanitisation, transcript review or boundary monitoring — with the elements actually stated recorded in `notes`" (staged `:42`) — is a 5-of-5 restatement of those keys, and the form's own comment puts the block on the run side, not the release side. Repaired in the worktree (row now reads "**not a delta** — the CTC form already…", cell `contamination_controls.acquired` plus the run-side keys) |
| **S2 integrity** | "**delta in field** — a state for the card itself"; cell "`unknown` / `not_controlled` are valid values" | `:38` declares the per-type value set `# controlled \| not_controlled \| unknown \| n/a`; `acquired: "unknown"` (`:42`) is the tri-state on the acquired claim; `boundary_integrity_monitored: ""` (`:46`) is the monitoring record the staged S2's rationale names ("a `controlled` claim for Type 5 without boundary monitoring is an assumption rather than a control", staged `:43`) | **still mislabelled, in the worktree too.** The worktree now says "**S2's tri-state integrity flag is the only new field**" — but the published form already declares that tri-state and the monitoring key. What S2 adds is a *name*, and the entry's own CTC cell names the published values |

Net for the admitted tree: against the pinned form the honest delta is **zero new fields** — R1, S1
and S2 are all carried. Against the round-6 tabulation alone (which never had R1/R4/S2 rows) the
honest wording is "not in the recorded table", not "no design tabulates": the cells added to those
rows are this entry's reading of the three designs, so the tabulation is *extended by re-derivation*
on those rows and the reader is never told.

### 3.3 Two cell errors in the same table (both repaired live; recorded because they were in the admitted tree)

- **R4 regeneration status** mapped CTC → `evaluation_date` and GEM → "Reproducibility". The form has
  a dedicated `regeneration:` block (`:49-53`: `procedure_published`, `procedure_url`,
  `artifact_only`, `notes`) — R4's real home; and GEM's Table 3 Reproducibility ("Exact prompt
  templates; few-shot example ordering and count; scoring procedure; multi-run variance; generation
  parameters", re-extracted from `2026.gem-main.50.pdf`) says nothing about regeneration. Both cells
  are now corrected in the worktree (`regeneration:` block; GEM `(absent — …)`).
- **R5 instrument currency** ("the date of the benchmark's last substantive update") mapped CTC →
  `evaluation_date`, which the form defines as the evaluation's date for a `system_under_test`; the
  form has no benchmark-update field (only `benchmark.version`). R5's real home is the AI Alliance
  "Release date"/"Change log". Unchanged in the worktree.

Both were independently found by `falsify/R30FxEntryQ1Q3.md:206-211`; I record them as corroboration
and as evidence that the admitted table's "already a column in two of three" counts were not safe.

### 3.4 "Continued, not re-derived" against what the table does

`:45` (admitted) says "The union table is continued, not re-derived", while `:42` says "What the
mapping below records is this entry's reading of a staged document". Both cannot describe one table:
four rows (R4, R1, S2, and the S1 placement claim) carry design cells the round-6 table never
tabulated — `benchmark-card-field-schema-2026-10-23.md:73-78` has six rows (detector access, negative
space, release-vs-score, elicitation budget, instrument currency, grader). Those cells are this
entry's own reading of the three designs, which is legitimate — and is exactly the sense in which the
table is re-derived on those rows. Three of the four were wrong (§3.2, §3.3), which is why the
wording matters: "continued" tells the reader the cells were inherited and need no check.

### 3.5 What would turn Q6 green

1. Land the worktree repairs **in a commit the Gate cites** (§3.2 R1/S1, §3.3 R4), and re-take the
   Gate's Q6 cell against that commit.
2. Delete the S2 novelty claim, or state what S2 has that `contamination_controls.acquired` +
   `boundary_integrity_monitored` + `notes` do not.
3. Replace "continued, not re-derived" with what is true: rows 1–2, R2, R5, grader inherit the
   round-6 cells; R1, R4 and S2 are cells this entry read out of the three designs, with key names
   cited per row.

## 4. Live-state table (what the post-commit edits repaired, what is still live)

Against worktree `sha256 ba0465d1…` (uncommitted, `M`; the live defects below were re-located at this hash after two further edits):

| finding | admitted tree `623c1fc` | worktree `ba0465d1…` |
|---|---|---|
| Q4-A falsifier points at the third bullet | present | **live** (`:135-136`) |
| Q4-B "two delta fields" vs the mapping's field count | present | **live** (mapping says one field; falsifier still says two and names the pair it now calls non-delta) |
| Q4-C reliability→prevalence laundering | present | repaired (population stated, "rare in practice" removed from the S081 restatement) |
| Q4-D falsifier undecidable / no Claim falsifier | present | **live** |
| Q4-E malformed bullet `- **- **Agreement…` | absent | **live** (`:120`, re-verified at `ba0465d1`) |
| Q5 S086 "peer-reviewed" | present | **live** (`:144`, re-verified at `ba0465d1`); also Gate `:65` and `R30FxRowsCensus.md:167` |
| Q6 R1 cell `(absent)` / "no design tabulates" | present | repaired in the table; the prose's new distinction ("absent from all three *tabulated* designs but present in S081's own four-field protocol") still separates S081's protocol from the released form of that protocol, which is the CTC v1.1 form — so the design still carries it |
| Q6 S1 "delta…the run-side half" | present | repaired ("not a delta", with `contamination_controls.acquired` and the run-side keys named) — and the neighbouring sentence still says the lane "cannot settle it without reading that form, which it has not admitted", which is now inconsistent with a cell that names the form's keys |
| Q6 S2 "only new field" | present | **live** (`:70-71`, re-verified at `ba0465d1`) |
| Q6 R4/R5 cells | both wrong | R4 repaired; R5 unchanged |

## 5. Residual risk and verification gaps

- No lane byte was edited; nothing was staged; no gate was run by me; no tool installed or upgraded
  (pre-existing `curl`, poppler `pdftotext`). Scratch: `/tmp/r30fx-entry/` (fetched sources + two
  entry snapshots).
- **The entry is a moving target.** §0's hashes are exact; if it moves again, §1.1's quotes and
  §3.2's cells must be re-located before this report is cited at closure. The defects that survived
  two independent edits (Q4-A/B/D, Q5, Q6-S2) are the ones I would defend at the final tip.
- **GEM leg is targeted, not exhaustive.** I extracted §7 Table 3 and its required disclosures from
  the PDF; I did not scan the whole 819 KB document for strata language outside Table 3 (the review
  uses "stratified evidence" about its own synthesis at `:131`, `:387`, which is not a card field).
  §3.2's R1 finding does not depend on GEM: CTC already carries it.
- **AI Alliance template is grep-level.** I searched the rendered page for
  `strata|stratif|breakdown|subset` (0 hits) and confirmed the fields the entry cites
  ("Contamination controls", "Checks performed, their coverage, and known gaps", "Release date",
  "Change log"). I did not enumerate every field, so §3.2 says "CTC carries R1", not "no template
  field could".
- **The 2025-vs-2026 review regime is an inference** (§2.2), flagged inline. If a 2025 call for
  papers is produced that says otherwise, the S086 label becomes unsupported rather than
  contradicted — the Q5 verdict stands on either footing, because the round offers no evidence for
  it and the series' nearest published statement denies it.
- **Not my rows:** Q1/Q2/Q3 (Q1Q3 seat), Q7–Q9, Q10 quote re-reads (`R30FxQuotes.md`, per-source
  seats), Q13 timing. I did not score them and cite their results only where a finding of mine
  touches theirs.

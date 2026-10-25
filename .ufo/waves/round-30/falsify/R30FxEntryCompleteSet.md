# R30 falsify — complete-set Q10 second-seat re-read of the contamination transparency card

Seat: `L1Kengaku30.R30FxEntryCompleteSet-3` (leaf; no subagents, no `ask`, no background watch, no model calls).
Candidate under review: `corpus/knowledge/contamination-transparency-card.md`.

**Bytes reviewed (pinned).** Committed blob at `623c1fc` —
`git show 623c1fc:corpus/knowledge/contamination-transparency-card.md`, sha256
`f01b7cd20cf4ebcaf3ee9f7af8b109ace8b86e69002ae53a213c2dc80ad1e6cd`, 13,395 B. This is the admission
candidate (Q10/Q13 measure the admitting commit's tree), so every line number `:N` below indexes that blob.

**The lane is moving under this seat.** While I was capturing sources the working copy changed: at
2026-10-25T04:48Z `corpus/knowledge/contamination-transparency-card.md` hashes
`31b72304365bf471cd0353d591ead5f85cef5e5afffb4de7edef084acf5622bb` and `git status` reports it `M`
against `623c1fc`. §Drift below re-reads that blob separately. Findings H1–H5 / M1–M5 / L1–L5 are
statements about `f01b7cd2…`, not about `31b7230…`; the verdict line names both.

Tooling used: `curl` (all fetches), poppler `pdftotext`/`pdftoppm`/`pdfinfo`, ImageMagick `magick`
(folio crops), Python 3.14 stdlib (counts), and **PyMuPDF 2.0 installed with `pip` into a scratch venv
at `/tmp/r30fx-entrycomplete/venv`** (reason: poppler reports one footer glyph per page; I needed an
independent text-layer extraction to settle the S085 folio). No pacman transaction of any kind; no
tool outside `/tmp` was installed or upgraded.

---

## 1. Capture set (my own fetches, 2026-10-25)

| Row | Locator | Capture | Bytes | sha256 (prefix) |
|---|---|---|---|---|
| S081 | `https://arxiv.org/abs/2608.29463` | HTML abs page, 620 lines | 44,646 | `4c81bd3c18…` |
| S081 | `https://arxiv.org/pdf/2608.29463` | compiled PDF, 18 pp (used only to test the entry's compiled-paper parenthetical) | 342,646 | `a14f8cdcf2…` |
| S082 | `https://arxiv.org/html/2607.01254v2` | full-text HTML, 1,319 lines | 212,631 | `82a5c5c6e9…` |
| S082 | `https://arxiv.org/abs/2607.01254v2` | abs page HTML, 602 lines | 42,993 | `ed049b139e…` |
| S083 | `https://aclanthology.org/2026.findings-eacl.353.pdf` | PDF, 15 pp | 2,697,379 | `662c223568…` |
| S084 | `https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html` | HTML, 562 lines | 32,762 | `c4447d93c6…` |
| S085 | `https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf` | PDF, 52 pp (AES, copy:no — extractable) | 1,949,572 | `e551e2e095…` |
| S086 | `https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf` | PDF, 6 pp (poppler emits one Marked-Content warning on p.1) | 371,155 | `c3706aca80…` |

Cross-checks fetched from the campaign's own pinned locators (used in §4 only):
CTC v1.1 form at commit `4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6` (`templates/disclosure.yaml`, 2,181 B,
sha256 `05131be9f72b333a479046a0df4510d48fd5389192d40c595869e718b5c90d0f`), AI Alliance template page
(25,177 B, `5ff8fe9d69…`), GEM 2026 review PDF (819,775 B, `177341b8de…`). Campaign staging file
`benchmark-card-field-schema-2026-10-23.md` = `66651007…` — **matches the sha256 the entry states at `:38`.**

## 2. Per-source re-read — one row per source

| Row | Entry's locator | Span located in my capture? | Count recomputed | Entry's count | Agree? |
|---|---|---|---|---|---|
| S081 | abs page, **line 124** | **All three spans verbatim in line 124** (`<span class="descriptor">Abstract:</span>` line). Q1 "because it is a property of one run…" contiguous; Q2 "-- direct, derivative, temporal, distributional, and acquired --" contiguous; Q3 "Two variables fall below…" contiguous | 22 / 6 / 18 words | 22 / 6 / 18 | **yes** |
| S081 | "the printed title" | Document title = "Benchmark Contamination: A Taxonomy Organized by Defeated Mitigation" (`<title>`, `citation_title`, PDF metadata) | — | no count | yes (used for identity only; no quote rests on it) |
| S082 | full text **§7.3 line 855** | **Located**: line 855 sits inside §7.3 (heading at :746, §7.4 at :865); the quoted sentence is the paragraph's 2nd sentence, verbatim | 11 words | 11 | **yes** |
| S082 | full text **§8.2 line 901** | **Located**: line 901 sits inside §8.2 (heading at :895, §8.3 at :905); the quoted span is the paragraph's final clause (starts mid-sentence after "…distinction formalized above:") | 17 words | 17 | **yes** |
| S082 | "the abs page carries neither phrase" | **None of either phrase, and not the word `transparency` at all**: abs page hits = 0 for `transparency`, `Item-level`, `live item pools`, `procedures, governance`, `validity testing` | 0 / 0 | 0 / 0 | **yes** (stronger than stated) |
| S083 | **p.1, printed page 6710** | **Both located on page 1**, in the Abstract (raw-extraction lines 25–28 and 33–35). p.1 carries the folio `6710` and "Findings … EACL 2026, pages 6710–6724" | 14 / 19 words (14 requires resolving three break joins) | 14 / 19 | **yes** |
| S084 | **html lines 344 and 397** | **All three located**: Q1 at line 344, Q2 at line 397, Q3 at **line 315** — line 315 is **not** named in the entry (see M4). Page title = `数据污染评估 — OpenCompass 0.4.0 documentation` | 3 / 7 / 1 whitespace tokens | 3 / 7 / 1 | **yes** on counts, **no** on completeness of locations |
| S085 | **p.32 (printed 27), p.34 (printed 29)** | **Both located**: Q1 on PDF p.32 (page-concatenated extraction lines 65–67 ⇒ "three typeset lines" is right), Q2 on PDF p.34 (inside the "2. 动态更新，测试题库实时化" item) | Q1 3 tokens; Q2 1 token, **24 characters** (23 ideographs + U+FF0C fullwidth comma) | 3 tokens, not contiguous / 1 token, 24 characters incl. comma | **yes**, with the folio caveat below |
| S086 | **p.1, printed page 797** | **Both located**: title on p.1 only, one text-layer line, identical to PDF `Title` metadata ⇒ "one contiguous run" correct; caveat sentence present, **quoted span spans text-layer lines 80–81** ("一致したものを一律に" ends line 80, "混入とみなして…残る。" is line 81) | title 3 tokens; caveat 1 token, **30 CJK characters** (kana+kanji; 11 kanji alone, 19 kana alone) | 3 tokens / 1 token, 30 CJK, lines 80–81 | **yes** for the entry; **disagrees with `corpus/SOURCES.md:112`, which still says lines 78–81** |

**S085 folio caveat (the one location a reader cannot confirm by eye).** PDF page *N* carries printed
folio *N−5*: PDF 6–14 print 1–9 exactly, and every two-digit folio renders **only its tens digit**
(PDF 15–24 print "1", 25–34 print "2", 35–44 "3", 45–52 "4" — verified with PyMuPDF `get_text("dict")`:
one 9 pt TimesNewRomanPSMT span per page, x≈295 pt, plus a page render at 200 dpi showing a lone "2"
on PDF 32 and PDF 34). So "printed 27" / "printed 29" are correct **by the +5 offset**, but the artefact
literally prints "2" on both pages. The entry asserts the label without the method; a rechecker who
trusts the visible folio cannot reproduce it. Not a falsification — a calibration gap (recorded, not scored as a defect).

## 3. Per-number re-read — one row per stated number

| # | Number as stated | Where | Recomputed from my captures | Verdict |
|---|---|---|---|---|
| 1 | 22 words (S081 Q1) | `:1` | 22 | match |
| 2 | 6 words (S081 Q2) | `:1` | 6 | match |
| 3 | 18 words (S081 Q3) | `:1` | 18 | match |
| 4 | 11 words (S082 Q1) | `:2` | 11 | match |
| 5 | 17 words (S082 Q2) | `:2` | 17 | match |
| 6 | 14 words (S083 Q1) | `:3` | 14 | match |
| 7 | 19 words (S083 Q2) | `:3` | 19 | match |
| 8 | 3 / 7 / 1 whitespace tokens (S084) | `:4` | 3 / 7 / 1 | match |
| 9 | html lines 344, 397 (S084) | `:4` | 344 ✓, 397 ✓, **315 unnamed** | partial (M4) |
| 10 | 3 whitespace tokens, S085 Q1 | `:5` | 3 | match |
| 11 | 24 characters incl. fullwidth comma, S085 Q2 | `:5` | len = 24, ideographs 23, comma U+FF0C | match |
| 12 | p.32 = printed 27, p.34 = printed 29 | `:5` | offset +5 ✓; visible folio = "2" on both | match by offset only (caveat) |
| 13 | 3 whitespace tokens, S086 title | `:6` | 3 (`Code`/`LLM`/`事前学習時の評価データ混入への対策`) | match |
| 14 | 1 whitespace token, 30 CJK chars, lines 80–81, S086 caveat | `:6` | 1 token, 30 CJK, lines 80–81 | match |
| 15 | "the two fields this entry adds" | `:112` | the table at `:63`–`:68` and the paragraph at `:70`–`:75` both report **three** delta-status rows (S2 new field, S1 new placement, R1 new value set) | **disagree: 2 vs 3** (M1) |
| 16 | "the two delta fields" (falsifier) | `:128` | same table: three delta-status rows; the two named here are the two *already-columned* ones, the only genuinely new field (S2) is excluded | **disagree: 2 vs 3** (M1) |
| 17 | "one new value set (R1's strata, which no design tabulates)" | `:72`–`:74` | the pinned CTC v1.1 form carries a top-level `strata_reported:` block (6 sub-keys, per-stratum `scores`) ⇒ **a design tabulates strata** | **disagree: absent vs present** (H1) |
| 18 | R1 row cells "(absent) / (absent) / (absent)" | `:68` | AI Alliance: absent ✓; **CTC: `strata_reported` present**; GEM Table 3: absent ✓ | **disagree on one of three cells** (H1) |
| 19 | R4 CTC cell `evaluation_date` | `:65` | the CTC's regeneration carrier is a dedicated `regeneration:` block (`procedure_published`, `procedure_url`, `artifact_only`, `notes`); `evaluation_date` is its own separate key | **disagree: wrong cell** (M2) |
| 20 | "the CTC form carries it as a per-type value inside a **release-side** artefact" | `:72` | form's top-level keys are `benchmark`, `system_under_test`, `evaluation_date`, and its own comment: "Type 5 is evaluation-time: a property of THIS run, not of the benchmark" ⇒ per-run record | **disagree: run-side, not release-side** (H2) |
| 21 | "its three source rows are not in this lane's registry" | `:41` | the GEM 2026 review (campaign S124 = `2026.gem-main.50.pdf`) **is** `corpus/SOURCES.md:23` row S001, tier A, `mined`, teach cell names "the Contamination Transparency Card" | **disagree: 3 absent vs 2 absent** (H3) |
| 22 | "no measurements" (S085) | `:119`, `:170` | S085 PDF p.38 (printed 33) prints scores: "Qwen-7B在本次评测中仅为25.8分，但Qwen1.5-7B的分数却显著提升至51.8分"; p.37 (printed 32) prints rankings; p.36–37 print 203万 items, 40/40/20% dimension split, 2月19日–2月29日 | **disagree: none vs present** (H4) |
| 23 | "no document number" (S085) | `:119` | 0 hits for 编号 / `No.` / 报告编号 across all 52 pages | match |
| 24 | "no data release" (S085) | `:119` | report's own sentence (p.34): "这些数据在一定时间内不会进行公开，后续会根据产业需求进行开放" | match |
| 25 | "no two sittings share items" (S085 gloss) | `:99` | the quoted sentence says "保证每次参与测试题目的都不相同"; the **next** sentence bounds it: "…从而保证每次测试时有一定占比的题目从未用于大模型测试" | **disagree: absolute vs bounded share** (H5) |
| 26 | "all eight" (a design would claim all eight) | `:75` | table rows at `:60`–`:68` = 9 data rows (R3, grader integrity, negative, R2, R5, R4, S1, S2, R1) | **disagree: eight vs nine** (M6) |
| 27 | CG1–CG8 (eight questions) | `:78`–`:90` | 8 numbered rows | match |
| 28 | `recheck: 180d` ⇒ "next due 2027-04-23" | `:8` | 2026-10-25 + 180 d = 2027-04-23 | match |
| 29 | staging-file sha256 `66651007…` | `:38` | `66651007989a7fb5df4671f5f86e69ab1436517025a821afe8c451641a3533b9` | match |
| 30 | `corpus/SOURCES.md` "88 rows total" | registry | 88 rows matching `^\| S[0-9]`, 88 distinct ids, max S091 | match |
| 31 | registry teach cell "CJK quotes count **1-13** whitespace tokens" | `SOURCES.md:110` | over the six rows' CJK spans the counts are 3, 7, 1, 3, 1, 3 ⇒ **max 7**; registry-wide CJK-quoted spans also max at 7. **13 is reachable only by counting the unquoted line-397 paragraph** (computed: 13 tokens) | **disagree: 1–13 vs 1–7** |
| 32 | registry "the caveat sentence … spans extraction lines **78-81**" | `SOURCES.md:112` | the caveat *sentence* starts at line 78 ("しかし、表 1 のように、極めて短い"); the quoted *span* is lines 80–81 | **disagree with the entry's 80–81** (both internally consistent, mutually inconsistent) |

**Prompt-state numbers that no longer exist in the admitted bytes** (named for honesty, with both values):
the assignment lists word counts `22/6/21/11/17/14/19`, "13 whitespace tokens" and "23 CJK characters".
In `f01b7cd2…` those three are `18`, `7`, and `30`. My own recomputation gives **18 / 7 / 30**, i.e. the
committed bytes are right and the prompt's figures are the pre-commit values; the only "21" anywhere in
the entry is S081's κ *median* 0.21, and the only "23" is S085's ideograph count.

## 4. Non-quote claims: the field mapping

### 4a. Against the campaign table (the narrow test the assignment names)

Every cell of the entry's nine-row table is cell-for-cell consistent with
`benchmark-card-field-schema-2026-10-23.md` **except** the three items below, which are places where the
entry *departs* from its source table:

| Entry row | Campaign table | Departure |
|---|---|---|
| R4 regeneration status → AI Alliance "Change log", CTC `evaluation_date`, GEM "Reproducibility" | campaign has no regeneration row; its instrument-currency row carries the same two cells and gives GEM "—" | the entry's R4 reuses R5's cells and adds a GEM cell the campaign marks absent (M2) |
| grader integrity → "already a column … dropped from this entry" | campaign row 6, presented as one of the lane's first-class fields | disclosed drop, but then "continued, not re-derived" (`:48`) overstates: a 6→9 row continuation that omits a campaign row is a re-derivation (M6) |
| S1 → "delta in placement" | campaign row 3 ("release-side vs score-side") already lists it as a lane field with the CTC mapping | the entry re-describes a campaign row as a delta (M7) |

### 4b. Against the pinned primaries (the test that actually decides the ledger)

The entry's ledger ("one new field / one new placement / one new value set", `:70`–`:75`) is checkable
only against the three designs' own bytes, because the campaign table is itself a reading of them. I
fetched all three at the campaign's pinned revisions:

- **CTC form** (`disclosure.yaml` @ `4dba1ed`): top-level blocks = `disclosure_version`, `benchmark`,
  `system_under_test`, `evaluation_date`, **`strata_reported`** (`reported`, `strata`, `aggregate_only`,
  `definition`, `pre_registered`, `scores`), `elicitation_budget`, `contamination_controls`
  (`direct`/`derivative`/`temporal`/`distributional`/`acquired` + `network_access_during_eval`/
  `environment_sanitised`/`transcripts_reviewed`/`boundary_integrity_monitored`/`notes`), **`regeneration`**.
  ⇒ strata **is** tabulated; regeneration **is** tabulated; the form is a per-evaluation record.
- **AI Alliance template**: `Contamination controls` ("Checks performed, their coverage, and known gaps"),
  `Release date`, `Change log`, `Grader evidence` present; no `elicitation`, no `strata`, no `budget` ⇒ the
  entry's four AI Alliance cells and two "(absent)" cells all hold.
- **GEM 2026 §7 / Table 3**: five dimensions = Training Data, Decontamination, Evidence Provided,
  IFT Stage, Reproducibility; Reproducibility = "Exact prompt templates; few-shot example ordering and
  count; scoring procedure; multi-run variance; generation parameters" ⇒ no strata, no regeneration
  (confirms the entry's GEM cells for R1 and R4).

Net: of the three limbs, **S2 stands** (`unknown`/`not_controlled` are per-type *values*, and no design
carries a card-integrity state), **S1's "placement" limb does not** (the CTC form is the run-side record),
and **R1's "value set" limb does not** (strata is a CTC column). The ledger should read: one new field (S2),
one inherited column the campaign table under-reported (R1 strata), and one rename (S1).

## 5. Findings, by severity

**H1 (HIGH). R1's absence claim is false against the artefact its own column names.** `:68` marks the CTC
cell `(absent)` and `:72`–`:74` asserts "no design tabulates" strata and sells R1 as "one new value set".
The pinned CTC v1.1 form carries a top-level `strata_reported:` block with a per-stratum `scores` map.
Evidence: `ctc-disclosure.yaml:16-22` (sha256 `05131be9…`, commit `4dba1ed`). Root cause is inherited —
`benchmark-card-field-schema-2026-10-23.md` lists only four CTC fields — but the entry asserts the
absence as its own conclusion and never opened the form it maps into.

**H2 (HIGH). S1's "new placement" limb rests on a characterisation the form contradicts.** `:72` says the
CTC form carries the acquired type "inside a release-side artefact, not as a score-side record". The form's
top-level keys are `benchmark` / `system_under_test` (model id + version) / `evaluation_date`, and its own
comment reads "Type 5 is evaluation-time: a property of THIS run, not of the benchmark"
(`ctc-disclosure.yaml:9-14,34-46`). A per-run form cannot be the evidence that placement is new.

**H3 (HIGH). "its three source rows are not in this lane's registry" is false for the GEM row.** `:40`–`:41`
asserts all three campaign source rows are unregistered and concludes "no load-bearing claim here rests on
it". `corpus/SOURCES.md:23` (S001, tier A, `mined`, teach cell names "the Contamination Transparency Card")
is the same GEM 2026 paper the campaign cites as S124 (`2026.gem-main.50`). The entry contradicts itself
six lines earlier, at `:52`–`:53`: "the review this lane already registers at tier A". So the GEM column of
the mapping *can* be lane-sourced today, and the "open work" framing at `:45`–`:47` understates what the
lane already holds.

**H4 (HIGH). "no measurements" about S085 is false.** `:119` and `:170` both say the report carries no
measurements. It prints measured scores and rankings for its own first-round trial — "Qwen-7B在本次评测中
仅为25.8分，但Qwen1.5-7B的分数却显著提升至51.8分" (PDF p.38 = printed 33), "从排名来看，Qwen-72B-Chat、
Yi-34B-Chat、…" (p.37 = printed 32) — plus construction measurements (203万-item database, 40/40/20%
dimension split, test window 2月19日–2月29日). The claim that survives is narrower: **no contamination
measurement and no released dataset**. As written, the sentence is a false negative-space claim in the
section whose job is negative space (Q4).

**H5 (HIGH). The CG7 gloss widens the quote past the page.** `:99` renders S085 as an item bank "rebuilt
so that no two sittings share items". The quoted sentence says "保证每次参与测试题目的都不相同"; the very
next sentence on the same page bounds it: "…从而保证每次测试时有一定占比的题目从未用于大模型测试" (only a
share of each sitting's items is fresh). Q3 forbids widening; this is the entry's load-bearing CG7 claim.

**M1 (MEDIUM). "The two fields this entry adds" contradicts the entry's own ledger.** `:112` and the
falsifier at `:128` say "two", while `:70`–`:75` reports three delta-status rows (one new field, one new
placement, one new value set) — and `:75` explicitly says the "two new fields" reading is superseded.
The stale "two" also excludes S2, the only field the paragraph calls new.

**M2 (MEDIUM). R4's CTC cell is the wrong key.** `:65` maps regeneration onto `evaluation_date`; the form's
regeneration carrier is the dedicated `regeneration:` block (`ctc-disclosure.yaml:49-53`). "Narrower" is
defensible; the cell that is supposed to show it is not.

**M3 (MEDIUM). "CTC v1.1 form" names the wrong artefact.** `:58` labels the second column "CTC v1.1 form"
for S123's `templates/disclosure.yaml`, whose own header is "# Contamination Disclosure v1.1". "CTC"
(Contamination Transparency Card) is **GEM's** name for a different design — S124 `Table 3: Proposed
Contamination Transparency Card (CTC)`, and S001's teach cell already registers that card. Two designs now
share one acronym in a table whose whole job is to keep designs apart.

**M4 (MEDIUM). S084's third quote has no location in the entry.** `:4` locates the row as "the two
documented methods (html lines 344 and 397)" but carries three quotes; the third (the access quote used
again at CG2) is at line 315. The registry row has the line; the entry does not. Q10 asks for every quote
location in the entry itself.

**M5 (MEDIUM). "whose own source records this lane's first failure with it".** `:73`–`:74`. S081 reports
*its own* two-coder instrument's poor agreement on strata reporting ("Two variables fall below the
prevalence-robust threshold registered in advance…", abs line 124; compiled PDF p.1 and §"Sample and
inference" restate it). Nothing in S081 records a failure of this lane. The same paragraph's later bullet
states the relation correctly, so this is a wording defect that contradicts its own file.

**M6 (MEDIUM). "all eight" and "continued, not re-derived" no longer describe the table.** `:75` says a
design "would have claimed all eight"; the table at `:60`–`:68` now has **nine** rows. `:48` and `:151`
say the union table is "continued, not re-derived", while the continuation drops the campaign's grader
evidence row (`:61`) — disclosed, but a drop is a re-derivation.

**L1 (LOW). "S082 is a working paper" has no on-source support.** `:119`, `:135`, `:137`, `:163`. Neither
the v2 HTML nor the abs page designates it a working paper; the only "working paper" string in the HTML is
a bibliography entry for a different paper (`:1000`). "Preprint, not peer-reviewed" is supportable and
carries the same weight.

**L2 (LOW). "S086 is a peer-reviewed 言語処理学会 paper".** `:163`. The capture states the venue
(第31回年次大会 発表論文集, CC BY 4.0) and nothing about review status; the label is not verifiable from the
capture. Everything else in `## Attribution` checks out (S083's Findings status, S084's vendor-doc status,
S085's self-report status).

**L3 (LOW). "supplies the reason the release-side half may be published at all".** `:20`–`:21`. The quote
supports "procedural transparency improves validity … without necessarily exposing live items"
(full text `:855`); it does not license publication. A deontic step beyond the quote, in the Claim paragraph.

**L4 (LOW). S083's hyphen-blind note names one of three break joins.** `:3`. The rule "drop `-` before the
line break in the artefact, drop `-` in the quote" does reproduce Q1 — I verified it (`contaminationresistant`
matches) — but it works only because it also silently resolves `re-|leased` and `imple-|mentations`. A
rechecker applying the join the entry names, and nothing else, fails; my first two attempts did.

**L5 (LOW, registry). The S082 row's title cell is wrong.** `corpus/SOURCES.md:108` titles S082 "The
Benchmark Ceiling: Human Judgment, Evaluation Economics and Benchmark Governance". v2's title is "The
Benchmark Ceiling: Human Judgment, Evaluation Scarcity, and the Political Economy of AI Capability
Measurement"; "Evaluation Economics" is §8.3's subsection title, and "Benchmark Governance" occurs **0**
times in the v2 HTML and 0 times on the abs page — the very string the entry's `## Corrections` (:184)
declares absent from v2.

## 6. Drift — the uncommitted working copy (`31b7230…`)

Not the admission candidate; recorded because it lands in the same tree and Q13 wants the Gate to name
bytes that exist. Read at 2026-10-25T04:48Z, diffed against `623c1fc`:

- **Fixed since commit**: R1's CTC cell now reads `strata_reported` (`:68`); R4's CTC cell is now "a
  dedicated `regeneration:` block" — both match my capture; the S085 CG7 paragraph now carries the
  adjacent bound ("only a share of each sitting's items is fresh") — fixes **H5**; the delta paragraph is
  rewritten to "the delta is one field" — fixes **M1** for that paragraph.
- **D1 (MEDIUM). New self-contradiction**: `:68` says CTC has `strata_reported`, `:74` of the same file
  still says "R1's strata are absent from all three *tabulated* designs". Both cannot be true; my capture
  says `:68` is right.
- **D2 (MEDIUM). Malformed bullet**: `:120` reads `- **- **Agreement is not established.**` — two bullet
  markers, unclosed bold. A scribe-facing file should not land in that state.
- **D3 (LOW). New number in flight**: `:115` adds "over a 41-document, five-variable population in which
  three variables clear it". 41 documents ✓ (abs line 124); "five variables" is **not** in the abstract the
  sentence attributes it to — it is in the compiled PDF ("five variables"), and "three clear it" is 5−2
  arithmetic, not a printed result. Cite the PDF or drop "five".
- **D4 (LOW).** The S1 status in the working copy is "delta in placement, not in field" while its own new
  paragraph (`:118`–`:119`) says "the two fields S081 measured as rare are the two this entry marks as
  already-columned" — S1's cell is a delta, so "already-columned" is wrong for it.

## 7. Residual risk and verification gaps

- **V1 — S085's printed labels** are recoverable only by the +5 offset; the two-digit folios on the
  artefact print their tens digit only. If a later seat treats the visible "2" as the label, it will
  read p.32 as printed 2 and call the row wrong. The row is right; the method is unstated.
- **V2 — S085's AES copy:no flag**: extraction and rendering both worked, but the file is not
  byte-redistributable; a recheck must re-fetch the same URL, and no stable hash for it is published
  anywhere in the lane.
- **V3 — S081's "printed title"** is asserted in the row and used for nothing; the row would be stronger
  citing the abs-page `<title>` line rather than a phrase with no anchor.
- **V4 — H1/H2 depend on S123's pinned commit.** I read `4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6`;
  the campaign row pins the same commit. If that repository force-pushes, the finding needs a re-fetch;
  the 2,181 B `05131be9…` blob is the identity anchor to re-check.
- **V5 — no LSP server exists for prose markdown in this lane**, so caller/definition/diagnostics checks
  were not run at all: every quotation check above is byte-level (`grep`/Python/`pdftotext`/PyMuPDF), and
  no semantic cross-reference engine was available. Recorded as a method limit, not as evidence.
- **V6 — the six sibling source reports** were not consulted before my captures; after them I did not
  fold their findings in except where a peer message named a claim I then re-derived myself (the CTC form).
  Anything they caught and I did not is unrepresented here.

## 8. What passes

Contamination of the report by wishful counting is the failure this seat exists to catch, so, plainly:
all seven Latin word counts (22/6/18/11/17/14/19), all five CJK token counts (3/7/1/3/1), S085's 24-character
span, S086's 30 CJK characters and 80–81 line span, S086's "one contiguous run", S082's two line locators
and its abs-page absence claim, S083's page and printed label, S084's three line numbers, the staging-file
hash, the 180-day date arithmetic, "no document number", "no data release", and the "compiled paper states
the same audit outcome in different words and does not print this sentence" parenthetical (PDF
`:36`–`:37`, `:1108`) **all reproduce on my own captures**. The failures are in the ledger the entry draws
*from* those quotes, not in the quotes' arithmetic.

VERDICT: FAIL — corpus/knowledge/contamination-transparency-card.md (committed admission candidate `623c1fc`, blob sha256 `f01b7cd20cf4ebcaf3ee9f7af8b109ace8b86e69002ae53a213c2dc80ad1e6cd`): H1, H2, H3, H4 and H5 are unrepaired in those bytes; the uncommitted working copy `31b7230…` repairs H5 and M1 and M2's cell but still carries D1 and D2, so the verdict must be re-taken on the repaired blob before admission.

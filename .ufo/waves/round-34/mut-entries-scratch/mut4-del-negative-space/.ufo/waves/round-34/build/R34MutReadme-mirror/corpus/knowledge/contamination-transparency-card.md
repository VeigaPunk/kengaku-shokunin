source: S081 — https://arxiv.org/abs/2608.29463 — Abstract (HTML abs page, line 124) and the printed title — "because it is a property of one run, it must be recorded with the reported score rather than with the benchmark release" (22 words); "direct, derivative, temporal, distributional, and acquired" (6 words); "Two variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type introduced here" (18 words) — arXiv 2608.29463 v1, accessed 2026-10-25
source: S082 — https://arxiv.org/html/2607.01254v2 — §7.3 (line 855) and §8.2 (line 901) of the full text; the abs page carries neither phrase — "Item-level transparency and procedural transparency have opposite effects on benchmark validity." (11 words); "transparency should attach primarily to procedures, governance, credentials, and validity testing, not necessarily to live item pools" (17 words) — arXiv 2607.01254v2 working paper, accessed 2026-10-25
source: S083 — https://aclanthology.org/2026.findings-eacl.353.pdf — p.1, printed page 6710 — "a contamination-resistant design by separating the publicly released game engine from hidden card implementations" (14 words, hyphen-blind compare: the extractor joins `contamination-|resistant`); "We also formalize a practical threat model and refresh protocol that preserves evaluation integrity even if specific cards leak." (19 words, byte substring after whitespace collapse) — Findings of EACL 2026, accessed 2026-10-25
source: S084 — https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html — 数据污染评估, the two documented methods and their access note (html lines 344, 315 and 397) — "目前该方案仅支持 GSM8K 数据集" (3 whitespace tokens); "目前该方案仅支持 C-Eval, MMLU, HellaSwag 和 ARC 数据集" (7 whitespace tokens); "但如今开源社区往往只会公开模型参数而非训练数据集" (1 whitespace token) — OpenCompass 0.4.0 documentation, accessed 2026-10-25
source: S085 — https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf — p.32 (printed 27) and p.34 (printed 29) — “方升”测试体系提出自适应动态测试（Adaptive Dynamic Testing，ADT）方法对大模型进行评测 (3 whitespace tokens, three typeset lines, not byte-contiguous); 采用动态方式构建，保证每次参与测试题目的都不相同 (1 whitespace token, 24 characters incl. the fullwidth comma) — 大模型基准测试体系研究报告（2024年）, CAICT, accessed 2026-10-25
source: S086 — https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf — p.1, printed page 797 — "Code LLM 事前学習時の評価データ混入への対策" (3 whitespace tokens, printed title, one contiguous run); the caveat 一致したものを一律に混入とみなして除去することには疑問が残る (1 whitespace token, 30 CJK characters, text-layer lines 80-81, located only on newline-unwrapped extraction) — 言語処理学会 第31回年次大会 発表論文集, accessed 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-fetch S081–S086 at their pinned locators, re-locate each quoted span in fresh captures (S081/S082/S084/S085 raw HTML or extracted text; S083 whitespace-collapsed default `pdftotext` plus a hyphen-blind compare; S086 newline-unwrapped extraction) and re-run `python3 plans/sources_adopt.py --quote-file <admission rows> --artifact <capture>` against the matching form, noting that S083's 14-word span needs a hyphen-blind compare the gate cannot perform, so that one span is human-verified (next due 2027-04-23)
writer: KengakuR30

# Contamination transparency card — an amendment to the tabulated card designs

## Claim

A benchmark's contamination claim is only as good as the record beside it, and that record
has two halves that cannot be merged: what the **release** discloses about its own exposure
(procedures, coverage, dates) and what the **run** must disclose because it was acquired during
that evaluation. S081 supplies the rule that forces the split — contamination acquired during an
evaluation "is a property of one run, it must be recorded with the reported score rather than
with the benchmark release" — and names the five types the record has to distinguish:
"direct, derivative, temporal, distributional, and acquired". S082 supplies the reason the
release-side half may be published at all: "Item-level transparency and procedural transparency
have opposite effects on benchmark validity", so "transparency should attach primarily to
procedures, governance, credentials, and validity testing, not necessarily to live item pools".
A card that omits either half converts a bounded disclosure practice into a claim about the
items themselves.

## It is an amendment, not a fourth design

This entry is an **amendment** to two things and a rival to neither:

- `corpus/knowledge/contamination-detection-and-transparency.md` (round 24) fixes the tier/access
  vocabulary and the rule that a detector negative bounds only what that detector could see. It
  names a "transparency record" and a "documented transparency card" without ever defining either.
  This entry defines them.
- The three published card designs tabulated in the campaign's round-6 staging file
  `benchmark-card-field-schema-2026-10-23.md` — package path
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md`,
  sha256 `66651007989a7fb5df4671f5f86e69ab1436517025a821afe8c451641a3533b9`, read 2026-10-25.
  That file is **staged, not lane-admitted**: it is not in this lane's `corpus/knowledge/`, and two
  of its three source rows are not in this lane's registry (the GEM 2026 review it tabulates is the
  registered one: this lane carries that review at tier A as S001), so no load-bearing claim here
  rests on it
  (QUALITY Q2). What the mapping below records is this entry's reading of a staged document;
  adopting those two rows as registry entries is what would make the mapping lane-sourced — that
  is open work, stated under §What this does not establish, never a claim of this entry. The union
  table is continued, not re-derived.

Round 29 refused the staged version of this entry exactly because it presented the field list as
*the* card format. The refusal's flip condition — "land it as an amendment to the tabulated
designs rather than a new design" — is what the two sections below discharge.

### Field mapping into the union table

Columns are the round-6 table's own: the AI Alliance maintainer template, the released CTC v1.1
form, and the GEM 2026 § 7 five-dimension proposal (the review this lane already registers at tier A;
it is named here by document, not by row id, because this entry's citation set is exactly S081–S086). Every row of this entry's field list is either
a column that already exists or an explicit delta.

| This entry's field | AI Alliance template | CTC v1.1 form | GEM § 7 Table 3 | Status |
|---|---|---|---|---|
| R3 contamination type tested | "Contamination controls" | per-type `controlled` / `not_controlled` / `unknown` / `n/a` | Decontamination | **already a column**; S081's five types give it values |
| grader integrity | "Grader evidence" | (absent) | (absent) | **already a column**, and dropped from this entry: this lane's grader work is `corpus/knowledge/grader-perturbation-audit.md`, not a card field |
| "what a negative cannot rule out" | "their coverage, and known gaps" | `unknown` and `not_controlled` are valid entries | Evidence Provided | **already a column** |
| R2 elicitation budget | (absent) | `elicitation_budget` | Reproducibility | **already a column** in two of three |
| R5 instrument currency | "Release date", "Change log" | `evaluation_date` | (absent) | **already a column** in two of three |
| R4 regeneration status | "Change log" | a dedicated `regeneration:` block | (absent — GEM's Reproducibility column lists prompt templates, few-shot, scoring and multi-run variance, not regeneration) | **already a column** in one of three |
| S1 acquired contamination | (absent) | `contamination_controls.acquired` plus the run-side keys | (absent) | **not a delta** — the CTC form already carries the run-side fact; it is a rename, not a relocation |
| S2 card integrity flag | (absent) | `unknown` / `not_controlled` are valid values | (absent) | **delta in field** — a state for the card itself |
| R1 strata | (absent) | `strata_reported` | (absent) | **already a column in one of three** — see §What this does not establish for what the entry's own source measured about it |

So the delta is one field, and the rest is not a delta at all. **The only field this entry adds to the
union table is S2, and what it adds is the field — a state recorded for the card itself rather than for a
contamination type. Its values are not new: the CTC v1.1 form already publishes `controlled` /
`not_controlled` / `unknown` / `n/a` per type, and `unknown` / `not_controlled` as valid entries.**
S1 is not a new field: the CTC v1.1 column beside it reads `type 5 recorded per run`,
so the run-side fact is carried; whether that makes the record score-side is a question about *where*
it is filed, and this lane cannot settle it without reading that form, which it has not admitted. R1's
strata are carried by the CTC v1.1 form (`strata_reported`) and are absent from the other two tabulated
designs, while also being present in S081's own four-field protocol (F1, strata) — so strata is a value
set this entry inherits from two cited-or-tabulated sources, not a discovery, and the mapping row above
is the authoritative status. Two earlier readings of this paragraph ("two new fields", then "one field, one
placement, one value set") overclaimed; this is the corrected one, and it is why the amendment is a
mapping rather than a design.

## The card gate — CG1–CG8

The frontier's instruction was to "gate a knowledge entry on Q1–Q8". The eight questions are
labelled **CG1–CG8** here so they cannot be confused with `QUALITY.md` Q1–Q8, which are this
lane's *admission* criteria. Each CG question is answerable from a published artefact, and each
names the case in which it is not answerable.

| # | Question | Answerable from | Not answerable when |
|---|---|---|---|
| CG1 | Which contamination type is claimed or tested? | the detector's own documentation — S084 names its two methods; S086 names its code-corpus method | a type is claimed with no detector behind it |
| CG2 | What access did the reporter have — parameters only, the training corpus, a public index, a canary? | S084 states the usual case: "但如今开源社区往往只会公开模型参数而非训练数据集"; S086 works from a code corpus; a task-file canary is the fourth channel (`corpus/knowledge/benchmark-task-validity-checklist.md`) | access is unstated |
| CG3 | Which datasets were tested, and what is the coverage limit? | S084 states both limits in its own words (GSM8K; C-Eval, MMLU, HellaSwag, ARC) | a benchmark-wide result is claimed from a single-dataset method |
| CG4 | What does a negative **not** rule out? | S084's stated access limit; S086's false-positive caveat: "一致したものを一律に混入とみなして除去することには疑問が残る" | "no contamination found" is read as "no contamination" |
| CG5 | Is this artefact release-side or score-side? | S081's one-run rule | a run-level claim is filed against the dataset |
| CG6 | Was the elicitation budget stated? | the union table's `elicitation_budget` column | a score has no budget behind it |
| CG7 | Is the item set protected, and is there a refresh path? | S083's separated engine and hidden implementations plus its "practical threat model and refresh protocol"; S085's dynamic bank, built "采用动态方式构建，保证每次参与测试题目的都不相同" | items are public with no retirement path |
| CG8 | When was the instrument last regenerated, and when was the benchmark last substantively updated? | the union table's `evaluation_date` / "Release date" columns; S085's 2024 programme description | dates are absent |

CG7 is where the two Eastern sources meet the Western ones from the opposite direction: S085's
report describes the 方升 system's adaptive dynamic testing method — “方升”测试体系提出自适应动态测试
（Adaptive Dynamic Testing，ADT）方法对大模型进行评测 — whose item bank is built dynamically, with
"采用动态方式构建，保证每次参与测试题目的都不相同". Read alone that sentence sounds absolute, and the
next sentence on the same page bounds it: only a share of each sitting's items is fresh, the rest is
shared. That bound is the point for a card: CG7's answer is "dynamic bank, *and* the share", never
"dynamic bank" as a cleanliness claim. A dynamic bank reduces farmability; a card makes a fixed bank
honest about its exposure. They answer the same threat from opposite directions, and a benchmark that
answers CG7 must say which of the two it does and with what qualifier.

## What this does not establish

- **The card is a format, not a finding.** Nothing here measures contamination in any benchmark.
  Every CG answer is a statement about a *published artefact*, never about a model.
- **The card's fields are fields its own source measured as rare.** S081's arXiv abstract reports of
  its own protocol (the compiled paper states the same audit outcome in different words and does not
  print this sentence): "Two variables fall below the prevalence-robust threshold registered in advance:
  strata reporting and the acquired type introduced here" over a 41-document, five-variable population
  in which three variables clear it. Strata reporting is this entry's R1 and the acquired type is S1 —
  both of which the mapping above shows a published design already carries in some form. So the entry's
  one genuinely new field (S2) is *not* one its source validated, and the two fields S081 measured as
  rare are the two this entry marks as already-columned. A complete card is not a common card.
- **Agreement is not established.** S081's own abstract reports a test–retest ceiling "collapsing under
  the class skew the registration anticipated", with pooling raising it "through chance correction rather
  than better agreement" (arXiv abs page, abstract). Two coders filling this card need not agree; the
  card records what each stated, not a reconciled truth.
- **S085 cannot be used as evidence about anyone else.** It is the sponsoring body's own 2024
  description of its own programme: it carries programme numbers and score tables (p.38 prints its own
  figures), but no document number, no contamination measurement and no data release. It
  supports "this is how one programme builds its item bank", nothing about contamination rates.
- **S082 is a working paper**, not a peer-reviewed result: its item/procedure transparency claim is
  an argument plus a wage-premium dataset, not a measured disclosure effect.
- **The field mapping is not lane-sourced.** The union table it maps into comes from a staged
  campaign document (sha256 above) whose two non-GEM source rows this lane has not admitted; the mapping
  is this entry's reading of that document. The entry's own load-bearing claims rest on S081–S086.
- **Falsifier:** a benchmark release that publishes a card answering all eight CG questions while
  its own contamination audit shows the strata and acquired fields are *populated* (not "unknown")
  would show that the fields this entry's sources measured as rare
  (R1 strata, S1's acquired type) are common — a decision rule the card design cannot supply on its own,
  which is why this bullet names the unit (one benchmark release), the population (its published card)
  and the observation (both fields populated and non-trivial) rather than a trend
  bullet above.

## Attribution

S081 and S082 are arXiv preprints (a taxonomy paper and a working paper); S083 is a peer-reviewed
Findings of EACL 2026 paper; S084 is vendor documentation for OpenCompass 0.4.0 (a self-description
of two procedures, not an evaluation of any model); S085 is a self-report by the China Academy of
Information and Communications Technology about its own benchmark programme: it carries programme
numbers and score tables, but no contamination measurement, no document number and no data release; S086 is a 言語処理学会 2025 paper that the society publishes **without peer review** (its own stamp on
`anlp.jp/nlp2026/submit.html` says so and the 2025 pages carry no 査読), so it is labelled a
non-peer-reviewed proceedings paper, not a peer-reviewed result. Where a source describes its own artefact, this
entry labels it a self-report and takes no independent-replication weight from it.

## Extends

`corpus/knowledge/contamination-detection-and-transparency.md` (tier/access vocabulary, and its
"How kengaku applies it" row that prefers "suites with a documented transparency card" — the card
was named there and is defined here), and the union table of the campaign's round-6 staging file
`benchmark-card-field-schema-2026-10-23.md` (continued, not re-derived; two of its three source rows are staged and not in this
lane's registry, while the GEM 2026 review it tabulates is already registered here at tier A, so that
one column is lane-checkable). Coverage map: `corpus/README.md` row *Contamination transparency card
format*. New: `Contamination transparency card format`.

## How kengaku applies it

| Situation | Do | Don't |
|---|---|---|
| Citing a benchmark as "decontaminated" | Ask for the card's CG1–CG4 answers and quote the coverage limit beside the claim | Read a detector negative as a property of the dataset |
| Reporting a score on a possibly contaminated benchmark | Record the run-side half (S1 acquired contamination, S2 integrity state) with the score | File a run-level claim against the release |
| Designing a disclosure for a benchmark you own | Answer CG1–CG8 procedurally; leave `unknown` where unknown | Publish items to prove cleanliness |
| Comparing two benchmarks' transparency | Compare the CG answers field by field | Compare the number of fields filled |
| Evaluating a claim that "the card exists" | Name which of the three published designs it is, and which fields it lacks | Treat the union as one design |

## Rejected

- **The staged text as the card design (round 30).** `contamination-transparency-card.md` in the
  merge package presents R1–R5/S1–S2 as *the* card format and never names the three published
  designs; its `ground:` line explicitly declines the amendment relation the flip required. Kept
  only as the field vocabulary this entry maps. Flip: none needed — this entry is the flip.
- **A canary as a CG4 answer (round 30).** A canary string present in task files proves a
  contamination-*detection* channel exists for that task family; it is not an answer to "what does
  a negative not rule out". Flip: a study showing canary absence/presence predicting measured
  contamination at the task level.
- **S085 as cross-benchmark comparative evidence (round 30).** Rejected as comparative evidence: a
  programme's self-description: it carries its own programme figures but no contamination measurement.
  Flip: an S085-adjacent artefact reporting
  per-benchmark dynamic-bank adoption with numbers.

## Corrections

- The staged version's S082 anchor named a `# Benchmark Governance` section that does not
  exist in v2; the locators above are the ones re-located in this round's captures, and the abs page
  carries neither phrase (the full-text HTML does).

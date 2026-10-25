# R30RevEntryQ1Q6 — the C1 amendment entry against QUALITY Q1–Q6

Seat: `L1Kengaku30.R30RevEntryQ1Q6` (reviewer, leaf). Access date for every source opened here: **2026-10-25**.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (no production byte written; this report is my only file).
Scope: Q1–Q6 only. Q7–Q9 are `R30RevEntryQ7Q9.md`; I did not re-score them and cite their results only where
my own bytes force a different conclusion.

## Object under test

| # | path | sha256 | lines | state |
|---|---|---|---|---|
| 1 | `/tmp/r30-DraftEntry/entry.md` | — | — | **ABSENT**: `read` → `Path '/tmp/r30-DraftEntry/entry.md' not found` |
| 2 | `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md` (read-only fallback the ticket names) | `9dee0e0306b9f38a1739b16a0a318e9c76bd3203f2c6656fceeba3f90eaa4dfc` | 92 | the round-1 campaign text; **not** an amendment draft — its own `ground:` line says so |

Every verdict below is against object 2 at that hash. **Scope warning for the integrator:** there is no drafted
amendment. The text I graded is the same candidate round 29 refused (`corpus/lessons/round-29.md:223-227`), unchanged
in substance and still carrying `verified-at: 2026-10-23`. A repaired amendment is a different object and must be
re-read by a second seat (Q10) before admission; this report does not transfer.

## Method disclosure

- **No `lsp` device is mounted** in this session: `read xd://lsp` → `No such tool: xd://lsp. Mounted devices:
  ast_edit, debug, mcp__aseprite_*, mcp__blender_*, mcp__godot_*, mcp__tripo_*, mcp__unity_cli_status.`
  No `references`/`definition`/`diagnostics` were available, so every locator below is a literal read, a hash, or a
  grep whose command and output appear in this report. Nothing here is presented as semantic proof.
- No tool was installed or upgraded; no pacman transaction attempted (host guard respected).
- Quotes are checked as whitespace-normalised byte substrings of artifacts **I fetched today**, hashed below, so a
  re-runner can re-fetch the same URL and compare. `pdftotext` line-wraps CJK, so a strict byte test on PDF text
  needs whitespace removal; the matrix shows exactly which spans need more than that.

## 1. Source re-open — all six rows

| id | URL I fetched | HTTP / bytes | sha256 (first 16) | the entry's quote located at | C1 kill rule |
|---|---|---|---|---|---|
| S081 | `https://arxiv.org/abs/2608.29463` + `/html/2608.29463v1` + `/e-print/2608.29463v1` | 200 / 44646, 305243, 38326 | `4c81bd3c18073631` / `7e5838c5ee2fdf55` | Abstract (abs page); `\label{tab:instrument}` at `preprint.tex:682` = Table 3, rows `F1 Strata` … `F4 Regeneration`; the "assumption rather than a control" sentence is in the **Figure 2 caption** (`preprint.tex:433`, `\label{fig:form}`) | **survives** |
| S082 | `https://arxiv.org/abs/2607.01254`, `/html/2607.01254v1`, `/html/2607.01254v2` | 200 / 43552, 212629, (v2) | `6ef2093990f95ec7` / `cf086cfc4fba9d8e` | **not on the abstract page** (see §2); full text §7.3 "Governance Design: Protected Items and Procedural Transparency" and §8.2 "Mandatory Transparency in Benchmark Design and Deployment", v1 **and** v2 | **survives on the full text only** |
| S083 | `https://aclanthology.org/2026.findings-eacl.353.pdf` | 200 / 2697379 | `662c2235680e475c` | Abstract, `pdftotext` lines 15 and 18; venue line "Findings of the Association for Computational Linguistics: EACL 2026, pages 6710–6724" | **survives** |
| S084 | `https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html` | 200 / 32762 | `c4447d93c6945d2c` | §数据污染评估 preamble char 750 ("这些问题还没有被广泛接受的解决方案", preceded by "只会公开模型参数而非训练数据集"); char 2131 in 基于自建同分布数据的污染数据标注; char 4664 in 基于经典预训练集的污染数据标注 | **survives** |
| S085 | `https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf` | 200 / 1949572 | `e551e2e0956c3145` | §（二）"方升"自适应动态测试方法 (heading at `pdftotext` line 1002), quotes at lines 1013 and 1049 | **survives** |
| S086 | `https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf` | 200 / 371155 | `c3706aca80aa8aee` | 概要 line 11; はじめに line 27, quote at line 80, printed p.797 | **survives** |

**Row survival is 6/6.** That is the one positive result C1's kill rule asks for: no cited row is refused for a quote
that cannot be found in this round's fetch. S082 survives *only* because the quotes live in the full-text HTML — the
`/abs/` URL the entry cites cannot carry them (§2). The staged registry row's `S082` title is also wrong: the paper is
"The Benchmark Ceiling: Human Judgment, Evaluation Scarcity, and the Political Economy of AI Capability Measurement"
(`citation_title` on the abs page), not "…Evaluation Economics and Benchmark Governance". That is a row defect, not an
entry defect, but the row must be corrected before adoption or the registry carries a false title.

## 2. Quote matrix — 11 spans, word and byte checks

Word counts are `len(span.split())` on the entry's own string; `ws` = found as a substring of the fetch after removing
all whitespace; `+q` = needs quote-character normalisation as well; `+backtick` = the entry's span is **not** a
substring because the entry inserted characters.

| entry line | source | words | chars | exact-byte (ws only) | verdict |
|---|---|---|---|---|---|
| 43 | S081 "a \`controlled\` claim for Type 5 …" | 16 | 98 | **no** | backticks inserted inside the quote; the source reads "a controlled claim for Type 5 …" verbatim |
| 32–35, 42 field text R1–R4, S1 | S081 `tab:instrument` | 6–20 each | — | yes | copied from Table 3 rows `F1 Strata`, `F2 Elicitation`, `F3 t1–t4`, `F3 t5 Acquired`, `F4 Regeneration` — correct rows, unquoted (narrowing, not widening) |
| 55 | S084 "目前该方案仅支持 GSM8K 数据集" | 3 | 18 | yes | ok |
| 55 | S084 "目前该方案仅支持 C-Eval, MMLU, HellaSwag 和 ARC 数据集" | 7 | 42 | yes | ok (narrows at the comma; the source continues "…，Contamination_Detector 中还包含了 CSQA 和 WinoGrande，但目前还没有在 OpenCompass 中实现。") |
| 56 | S084 "no widely accepted solution exists when only parameters are public" | unquoted | — | paraphrase | faithful translation of the char-750 sentence, but written without quote marks and with **no location** |
| 56 | S086 "一致したものを一律に混入とみなして除去することには疑問が残る" | 1 (CJK) | 30 | yes | ok |
| 59 | S083 "separating the publicly released game engine from hidden card implementations" | 10 | 77 | yes | ok (Abstract) |
| 59 | S083 "a practical threat model and refresh protocol that preserves evaluation integrity even if specific cards leak" | 16 | 109 | yes | ok (Abstract) |
| 64 | S082 "Item-level transparency and procedural transparency have opposite effects on benchmark validity" | 11 | 95 | yes (full text §7.3) | **location in the entry is wrong** |
| 66 | S082 "transparency should attach primarily to procedures, governance, credentials, and validity testing, not necessarily to live item pools." | 17 | 134 | yes (full text §8.2 — a *different* section) | **location in the entry is wrong** |
| 84 | S085 "测试数据标签化管理、动态测试数据库和高质量测试数据抽样算法" | 1 (CJK) | 29 | yes | ok (§（二）, line 1013) |
| 86 | S085 "为了防止大模型测试的"刷榜"问题，…都不相同" | 1 (CJK) | 57 | **no — needs `+q`** | source bytes use U+201C/U+201D (“刷榜”), the entry uses ASCII `"`; `entry in raw` → `False` |

Absence measurements on the cited URLs, run against my own fetches:

```
S082 /abs page: 'procedural transparency' → 0, 'Item-level' → 0, 'should attach' → 0,
                'validity testing' → 0, 'Benchmark Governance' → 0
S082 full-text headings (v1 and v2): no 'Benchmark Governance'; the nearest are
  '7 Governance Implications: Who Controls the Benchmark Controls the Narrative',
  '7.3 Governance Design: Protected Items and Procedural Transparency',
  '8.2 Mandatory Transparency in Benchmark Design and Deployment'
S081 LaTeX: \label{tab:instrument} at preprint.tex:682 (Table 3); no table carries the
  sentence 'assumption rather than a control' — that is \caption{…} at preprint.tex:433
S083 PDF: '10.18653/v1/2026.findings-eacl.353' → 0 in the text layer; the DOI is on the
  Anthology landing page (fetched, 1 occurrence), not in the cited PDF
```

## 3. Verdicts

### Q1 — the triad opens the entry — **FAIL**

Deciding cell: **line 8, `verified-at: 2026-10-23`.**

`QUALITY.md:15` requires "ISO date the source was opened **for this entry**". Round 29 refused this candidate
precisely on that cell — `corpus/lessons/round-29.md:227`: "all six sources carry the campaign's `2026-10-23` opened
date and none was re-opened this round" — and C1's frozen predicate demands `verified-at: 2026-10-25` plus six rows
with `opened=2026-10-25`. As it stands the amendment re-imports the exact property it was supposed to discharge, and
any admission on this text would be an admission on a 2026-10-23 opening that this round did not perform.

Secondary cells (each named so the repair is mechanical):

1. **line 1 is blank** — the file opens with an empty line, so the triad does not open the entry. The lane's own
   admitted precedent opens at line 1 with `source:` (`corpus/knowledge/benchmark-task-validity-checklist.md:1`).
2. **line 3 anchor `# Benchmark Governance` does not exist** in arXiv 2607.01254, v1 or v2 (§2). An anchor that
   names a non-section is not "the exact anchor".
3. **line 7 anchor `# 1 はじめに`** — the opened PDF's heading text is `はじめに` (line 27); the section number is
   not in the text layer. Cite the heading as it appears, or `p.797`.
4. **line 4 DOI** — `10.18653/v1/2026.findings-eacl.353` is not in the cited PDF; it is on the Anthology landing
   page. Either cite both URLs or drop the DOI from the anchor cell.

PASS half, stated so it is not re-litigated: the **multi-`source:`-line shape is correct in this lane** — Q1's
"`S###` row id(s)" and the admitted round-29 entry (`benchmark-task-validity-checklist.md:1-5`, then `verified-at:`
then `recheck:`) settle it; I do not read "the first three lines" as forbidding six source lines. Lines 2, 5, 6
anchors are exact (`# Abstract` + `tab:instrument`; `# 数据污染评估`; `# （二）"方升"自适应动态测试方法`), and line 9
carries cadence **and** action as Q1 requires.

### Q2 — tier floor, per claim — **PASS**

Every load-bearing claim has ≥1 A/B row scoped to that claim; there is no tier-C and no `community` row anywhere in
the entry.

| claim | entry line(s) | row | tier | in that row's scope? |
|---|---|---|---|---|
| acquired-during-evaluation contamination belongs with the score | 20, 57 | S081 | B | yes ("for the preprint's own text") |
| the four release-side fields R1–R4 and the score-side values S1–S2 | 42–43 (R rows above) | S081 | B | yes (`tab:instrument`) |
| disclosure must be procedural, not item-revealing | 64–69 | S082 | B | yes |
| protection + threat model + refresh protocol | 59 | S083 | A | yes ("for the paper's own design claim") |
| detector coverage limits and the parameters-only case | 53, 55, 56, 73 | S084 | A | yes |
| string overlap over-reports; blind spot must be stated | 56, 74 | S086 | A | yes |
| dynamic bank as the opposite-direction answer | 81–88 | S085 | B | yes |

Two caveats that are **not** floor breaches but must not be read as endorsement:

- line 54 cites **S077** ("canary, per task") — an eighth id, outside the six-row triad, tier A in
  `corpus/SOURCES.md`, opened 2026-10-19, **not re-opened this round**. Tier is fine; the undeclared, unanchored
  citation is a Q1/Q3 defect (see Q3).
- line 49 "Each is answerable from a published artefact" is the entry's own synthesis, not a source claim. Q2 does
  not cover it; do not cite this PASS as evidence the card works.

### Q3 — claim stays inside its quote — **FAIL**

Deciding cell: **lines 64–67 with line 3** — the entry's only governance quote is anchored to a section that does not
exist and to a URL that contains neither of its two spans.

`QUALITY.md:31` requires each load-bearing sentence to map to "an anchored quote (≤25 words, with location)". Measured:
`/abs/2607.01254` returns 0 occurrences for `'procedural transparency'`, `'Item-level'`, `'should attach'`,
`'validity testing'`; the spans are in **§7.3** and **§8.2** of the full-text HTML, in v1 and v2. As cited, the claim
has no checkable location. (Independently reached by `R30SrcS082.md` §5 and `R30RevEntryQ7Q9.md`; I record it from my
own two fetches, not from those reports.)

Three further cells:

1. **line 43** — the quoted string is not a substring of S081: the entry writes "a \`controlled\` claim …". The source
   text at `preprint.tex:433` is "a `controlled` claim for Type 5 without boundary monitoring is an assumption rather
   than a control" with the markup removed, i.e. "a controlled claim …". Inserted characters inside quotation marks
   are exactly what C3's byte-substring case is meant to refuse.
2. **line 86** — `entry in raw` → `False`: the entry uses ASCII quotes where the report uses “ ”. It passes only after
   quote normalisation. Undeclared transcription drift in a quote.
3. **lines 67–68 widening** — the entry writes "Publishing the live items to prove contamination-freedom **would
   increase contamination**"; S082 §7.3 reads "Revealing live benchmark items **may** improve reproducibility, but it
   also increases **exposure to contamination and strategic optimization**." A hedged exposure claim became a
   categorical contamination claim, and the conceded benefit was dropped. Q3's "may narrow, never widen" fails here.

All word counts are ≤25 by whitespace tokens (max 17). The CJK loophole is a C3 problem, not a Q3 pass: lines 84 and
86 are 29 and 57 characters but **1 whitespace word** each, so a naive `len(split())` gate admits any length of Chinese
or Japanese. `SOURCES` contract v1 defines no CJK word rule; the gate needs one before it can be called honest.

### Q4 — negative space is written down — **FAIL**

Deciding cell: **there is no such text.** `grep -n 'does not establish\|Falsif\|falsif\|not establish\|What this'`
over the 92 lines → **no match**. The entry never states what its six sources do not establish and never names an
observation that would falsify the card. Line 90 disclaims only *admission authority* ("is the lane's call, not this
entry's"), which is not negative space. The lane's admitted form for this is a closing "What this does not establish"
section ending in a bolded `Falsifier.` (`corpus/knowledge/benchmark-task-validity-checklist.md:84-97`).

Worse than the absence: the entry **launders a negative from its own primary source.** S081's abstract (fetched bytes,
`arxiv.org/abs/2608.29463`):

> "Per-variable linear-weighted $κ$ runs from 0.00 to 0.35 (median 0.21) over 29 main-pass documents against a
> single-coder test-retest ceiling of 0.84, collapsing under the class skew the registration anticipated" … "Two
> variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type
> introduced here."

Those two variables are **R1 (F1 Strata, line 32)** and **S1/S2 (acquired, t5; lines 42–43)** in the entry's own
tables. The entry prescribes both as required fields with no reliability caveat, in a card whose purpose
is to make a disclosure trustworthy. Q4's rule — "an indeterminate or detector-negative result is reported as such,
never laundered into a positive" — is broken on the entry's central instrument. This is the single most consequential
substantive finding in this review: the amendment states the protocol as settled while its only formal source reports
that two of its eight variables did not clear the pre-registered agreement floor.

### Q5 — every source is labelled for what it is — **FAIL**

Deciding cell: **lines 81–88** (the "Eastern precedent" paragraph) with **line 18**.

```
grep -c 'self-report'  → 0
grep -c 'independent'  → 0
```

Line 81–88 presents S085 — the China Academy of Information and Communications Technology's report on **its own**
"方升" system — as "answer[ing] the same threat from the opposite direction", closing "They are complements, and both
are recorded here." That is the operator describing its own system, offered as corroboration, with no self-report
label. Line 18 does the same for S083: "one maintainer-engineering example of contamination **resistance**" turns the
authors' offered design ("TCG-Bench offers … a contamination-resistant design", Abstract line 15) into an example of
resistance achieved — a Q5 label defect that doubles as a Q3 widening.

The only near-label is line 53 ("the detector's own documentation"), and it covers S084/S086 only; S083 and S085 carry
nothing. This is the same test the lane applied to the round-29 entry — `R29a2RevQuality.md` Table 2 marks Q5 **FAIL**
on `grep 'self-report' → no match` — so the verdict is the lane's own standard, not mine.

### Q6 — extends, never duplicates or overwrites — **FAIL**

Deciding cell: **line 90**:

> "The card format and the Q1–Q8 gate are supplied here; the *admission* of the card against the lane's existing
> `knowledge/contamination-detection-and-transparency.md` vocabulary **is the lane's call, not this entry's**."

```
grep -c 'extends' → 0   grep -c 'extend' → 0   grep -c 'amend' → 0
```

`QUALITY.md:50` requires the entry to name the existing entry or coverage row it extends. The entry names the path in
prose (line 13) and then explicitly declines to state the relation the refusal turned on. Round 29's reason
(`corpus/lessons/round-29.md:223-227`) was that this file "offers a fourth card design where the campaign's own round 6
tabulated three published designs and ruled this file an amendment, not a rival"; the flip it recorded was to "land it
as an amendment to the tabulated designs rather than a new design". The text I graded is that rival, unamended.

Compounding fact: the tabulation it would amend is **not in the lane corpus**. `ls corpus/knowledge/` → 38 entries,
none of `benchmark-card-field-schema-2026-10-23.md`, `card-design-arbitration.md`, `card-authorship-and-attachment.md`,
`card-publication-contracts.md`; those are staged paths under `/home/vgpnk/Projects/shokuknow/merge/kengaku/`, which
Q7 forbids as support. So an amendment cannot name what it amends until either (a) the tabulation rows land, or (b) the
amendment names `knowledge/contamination-detection-and-transparency.md` as the entry it extends and the frontier bullet
(`corpus/README.md:272`) as the gap it closes — with an `extends` sentence, in the admitted form of
`benchmark-task-validity-checklist.md:14-17`.

## 4. Overall recommendation

**REFUSE admission of this text as the C1 amendment.** Blocking reason: it is not an amendment (Q6 — line 90 declines
the relation, `extends`/`amend` = 0 hits) and it re-imports the `2026-10-23` unopened date that round 29 refused on
(Q1 — line 8), while its central governance claim points at a section that does not exist and a URL that cannot carry
the quote (Q3 — lines 3 and 64–67).

The card itself is not refused: **all six cited rows survive today's fetch (6/6 on C1's kill rule)**, every span is
within the 25-word cap, and Q2 clears. What fails is the packaging — a dated, anchored, labelled, extending
amendment — plus one substantive silence the entry cannot leave (the S081 κ result bearing on R1 and S1/S2).

## 5. Minimal repair list, in order (for the amendment's writer, not executed here)

1. `line 8` → `verified-at: 2026-10-25`; the six rows' `opened` → `2026-10-25`; only after the re-open is on record —
   the re-open exists now (§1) and can be cited, not asserted.
2. `line 3` → URL `https://arxiv.org/html/2607.01254v2`, anchors `§7.3` and `§8.2`; fix the staged S082 title.
3. `line 43` → remove the backticks from inside the quote.
4. `line 86` → transcribe “刷榜”/“方升” with the report's own quote characters, or declare the normalisation.
5. `lines 67-68` → restore S082's hedge and its conceded benefit, or drop the sentence.
6. Add an `extends` sentence naming `knowledge/contamination-detection-and-transparency.md` and the frontier bullet;
   if it amends the round-6 tabulation, that tabulation must be in-lane first.
7. Add a Q5 label block (all six are self-reports about their own artefact; none is an independent replication) and a
   "What this does not establish / Falsifier" section that includes S081's two below-threshold variables.
8. `line 54` → declare S077 in the triad with an anchor, or drop the canary example.

## 6. Residual risk and verification gaps

- **Title defect travels into the registry.** C1's frozen predicate checks ids/status/`opened`/`used-by`, not titles,
  so a false S082 title passes the counter. Nothing in the counter will catch it after adoption.
- **CJK word counting is undefined in SOURCES contract v1.** Until C3 defines it, a 57-character Japanese/Chinese
  quote counts as one word and passes "≤25 words". `sources_adopt.py` needs the rule and a selftest case for it, else
  C3 proves quote *presence* only.
- **Artifact choice changes the answer.** S082's spans pass on the HTML full text and fail on `/abs/`; S083/S085/S086
  pass only after whitespace removal from `pdftotext`; S085's long span needs quote normalisation. The gate must state
  which artifact it is given and which normalisations it applies, or the same row will be green and red by turn.
- **I did not verify S090/S091 or any row outside the six** — out of scope.
- **Not re-scored:** Q7–Q19, C2's D1–D5, C3's selftest. `R30RevEntryQ7Q9.md` reports Q7 FAIL (nothing landed) and Q10
  incomplete; my §1 does not disturb those conclusions, and my Q6 finding is independent of them.

## 7. Tooling

Nothing installed, nothing upgraded, no pacman transaction (host guard). `pdftotext`, `curl`, `python3` were already
present and are the only tools used.

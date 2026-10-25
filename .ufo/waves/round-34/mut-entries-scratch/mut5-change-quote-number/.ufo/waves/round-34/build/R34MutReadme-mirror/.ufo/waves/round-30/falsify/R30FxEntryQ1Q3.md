# R30 falsify — entry audit Q1/Q2/Q3 (contamination transparency card)

Seat `L1Kengaku30.R30FxEntryQ1Q3-3` (reviewer). Leaf: no dispatch. 2026-10-25.
Candidate: `corpus/knowledge/contamination-transparency-card.md` (writer `KengakuR30`, not this seat).

VERDICT: FAIL — Q3 fails: two load-bearing sentences widen their quote, one of them contradicting
the entry's own restated delta arithmetic nine lines above it, and two union-table cells are false
against the artefacts they cite; Q2 fails on the same sentence's scope plus one misstated registry
fact; Q1 passes.

**Bytes reviewed / churn.** The candidate changed while this seat was reading it:
`04:37` (unhashed read) → `0f2e1614…` at `04:42:01` → `df0b6d41…` at `04:44` → **current
`f01b7cd20cf4ebcaf3ee9f7af8b109ace8b86e69002ae53a213c2dc80ad1e6cd`, 177 lines**. Every line
number and quoted string below was re-read and byte-verified against `f01b7cd2`; `df0b6d41` and
`f01b7cd2` are line-identical at every cited line, so the findings stand on either tree. Repaired
live between the first reads and the current one: the S085/S086 count cells ("24 characters incl.
the fullwidth comma", "30 CJK characters, text-layer lines 80-81"), the per-source extraction
disclosures (lines 3, 5, 6, 8), the restored grader-integrity row (line 61), and the delta
restatement (lines 70-77). The two blocking sentences (lines 97-102, 108-113) are byte-identical
across all four reads.

Nothing below rests on a build report. No model was passed; no `agent://all`; no install, no
package operation (pacman paused host-wide, nothing needed). Scratch: `/tmp/r30fx-EntryQ1Q3/`.
Lane write: this report.

## Fresh captures (all fetched by this seat)

| id | locator | HTTP | bytes | capture |
|---|---|---|---|---|
| S081 | `arxiv.org/abs/2608.29463` | 200 | 44 646 | abs HTML (quote at line 124) |
| S081 full | `arxiv.org/pdf/2608.29463v1`, `/html/…v1` | 200/200 | 342 646 / 305 243 | `pdftotext -layout` (85 060 B), HTML v1 |
| S082 | `arxiv.org/html/2607.01254v2` + `/abs/2607.01254` | 200/200 | 212 631 / 43 552 | full text; abs page |
| S083 | `aclanthology.org/2026.findings-eacl.353.pdf`, `/2026.findings-eacl.353/` | 200/200 | 2 697 379 / 45 139 | `-layout`, `-raw`, landing page |
| S084 | `doc.opencompass.org.cn/…/contamination_eval.html` | 200 | 32 762 | HTML (lines 315/344/397) |
| S085 | `caict.ac.cn/…/P020240711534708580017.pdf` | 200 | 1 949 572 | `pdftotext -layout` (84 820 B) |
| S086 | `anlp.jp/…/Q2-11.pdf` | 200 | 371 155 | `pdftotext` plain and `-layout` |
| **S001 = staging S124** | `aclanthology.org/2026.gem-main.50.pdf` | 200 | 819 775 | GEM 2026 review, §7 Table 3 |
| **staging S123** | `raw.githubusercontent.com/Jangulo7/contamination-disclosure-paper/4dba1ed…/templates/disclosure.yaml` | 200 | 2 181 | CTC v1.1 template |
| **staging S122** | `the-ai-alliance.github.io/trust-safety-evals/evaluations/benchmark-card-template/` | 200 | 25 177 | AI Alliance template |

---

## Q1 — the triad opens the entry: **PASS** (one low defect)

Deciding evidence, lines 1-9:

- six `source:` lines (1-6) — one per id, each with id, URL, anchor, quoted span and a per-span
  measure (words for English, whitespace tokens/characters for CJK) — and each now carrying its own
  extraction caveat: line 3 "hyphen-blind compare: the extractor joins `contamination-|resistant`",
  line 5 "three typeset lines, not byte-contiguous", line 6 "located only on newline-unwrapped
  extraction";
- line 7 `verified-at: 2026-10-25` — ISO, equals the `opened` cell of all six rows;
- line 8 `recheck: 180d — re-fetch … re-locate each quoted span in fresh captures (…) and re-run
  python3 plans/sources_adopt.py --quote-file … --artifact … against the matching form (next due
  2027-04-23)` — cadence **and** action **and** resolved date; 2026-10-25 + 180 d = 2027-04-23
  (6+30+31+31+28+31+23 = 180), re-derived, not copied;
- line 9 `writer: KengakuR30` — present, in the lane's `KengakuR<round>` form.

Both failure modes Q1 names are absent (no undated recheck; no locator claimed current without one).

I executed the recheck myself with the lane's own locator (`plans/sources_adopt.py:328 locates()` —
byte substring of newline-folded text; `normalize_text` folds `\r\n`/`\r` only, `sources_adopt.py:276`):

| span | default capture | after newline-unwrap |
|---|---|---|
| S081 a/b/c | ✔✔✔ | ✔ |
| S082 a/b | ✔✔ | ✔ |
| **S083 a (14 w) / b (19 w)** | **✘✘** | **✘** |
| S084 a/b/c | ✔✔✔ | ✔ |
| S085 a | **✘** | ✔ |
| S085 b | ✔ | ✔ |
| S086 title / caveat | ✔ / ✘ | ✔ / ✔ |

So 11 of 14 spans locate in a default capture and 13 of 14 after unwrapping; **S083 locates in no
PDF capture** (both modes) because the printed abstract hyphenates and interleaves columns
(`contamination-`/`resistant`, `publicly re-`/`leased`, `imple-`/`mentations`, `eval-`/`uation`) and
no single de-hyphenation rule recovers both spans (one hyphen is real, the other is a break). The
line 3/8 disclosures are accurate and now say so. Both spans *are* byte-contiguous on the anthology
landing page (`locates()` → true for both, raw), which is the capture the recheck should name — the
in-lane pattern is S082's row ("the abs page carries neither phrase").

Residual Q1 defects:

- **Q1-1 (low).** Line 4 names a location for two of its three S084 spans only; the third
  ("但如今开源社区往往只会公开模型参数而非训练数据集") is html **line 315** (re-verified: 315, 344, 397).
- **Q1-2 (low, cross-cutting, not the entry's own bytes).** The extraction caveats at lines 3/5/6 are
  not mirrored in the registry rows: `corpus/SOURCES.md:109` (S083) and `:111` (S085) record the same
  spans with no non-contiguity note, so the recheck's gate step will refuse those two rows on a
  default capture (my matrix: S083 a/b ✘, S085 a ✘). The entry is consistent; the rows are the gap.

Strict-letter note (does not move the verdict): Q1 says "the first three lines are `source:`,
`verified-at:` and `recheck:`". With six sources, `verified-at` is line 7. The letter is unachievable
for any multi-source entry and is already violated by the admitted
`benchmark-task-validity-checklist.md` (five source lines, `verified-at` on line 6). Q1's own
definition ("the `S###` row id(s)") is what matters; the wording should be amended to "the header
block comprises source line(s), then `verified-at:`, then `recheck:`".

All count cells in the current bytes re-derived and correct: 22/6/18 words (S081), 11/17 (S082),
14/19 (S083), 3/7/1 whitespace tokens (S084), 3/1 tokens + 24 characters incl. `，` (S085), 3 tokens
+ 30 characters (11 kanji, 19 kana) at plain-extraction lines 80-81 (S086).

---

## Q2 — tier floor: **FAIL** (floor passes; scope and a registry fact do not)

Tiers from `corpus/SOURCES.md`, all six with `status=mined`, `opened=2026-10-25`,
`used-by corpus/knowledge/contamination-transparency-card.md` (verified row by row):

| row | kind | **tier** | scope (verbatim head) | in scope for the entry's claim? |
|---|---|---|---|---|
| S081 | paper | **B** | "the four-field contamination disclosure protocol … the rule that evaluation-time acquired contamination is reported with the score … — for the preprint's own argument" | ✔ split rule, five types, prevalence, reliability |
| S082 | paper | **B** | "the distinction between item-level and procedural transparency … where disclosure should attach — for the working paper's own argument, not peer reviewed" | ✔ |
| S083 | paper | **A** | "a peer-reviewed benchmark paper's own contamination-resistant design … for the paper's own design claim" | ✔ |
| S084 | docs | **A** | "its own two documented contamination-evaluation procedures and their stated coverage limits …" | ✔ CG1/3/4; partial CG2 |
| S085 | docs | **B** | "the report's own account of the 方升 benchmark system's adaptive dynamic testing method and its dynamically built item bank; … self-description with no document number, measurements or data release" | ✔ the bank fact; **✘ "complements"** |
| S086 | paper | **A** | "the paper's own contamination-detection method and its false-positive caveat for code benchmarks" | ✔ |

No tier-C row stands alone, no `community` row is used, and both B rows are labelled inside the entry
(line 1 "preprint", line 121 "S082 is a working paper"). The floor holds; the scope does not.

**Q2-A (blocking; same sentence as Q3-A).** Line 101 "They are complements". S085's declared scope is
the report's own account of ADT and its dynamically built bank — not any relation to a disclosure
card, which the report never mentions. The relation exists in-lane only in the row's own `teaches`
cell ("a card and a dynamic bank are complements"), i.e. the entry cites the lane's synthesis as if it
were the source's. Custody: the sentence is verbatim from the untouched staging entry
(`…/corpus/knowledge/contamination-transparency-card.md:87-88`), so no round has ever anchored it.

**Q2-B (medium).** Line 40-41: "its **three** source rows are not in this lane's registry". False for
one of the three. The GEM 2026 §7 column is `aclanthology.org/2026.gem-main.50` — the same paper as
lane row **S001** ("Are LLM Benchmarks Already Contaminated? A Systematic Review of Contamination
Detection Methods", tier **A**, mined 2026-10-19, `used-by contamination-detection-and-transparency.md`);
I fetched the PDF and read its §7 Table 3 under that URL. Only S122 (AI Alliance) and S123 (CTC v1.1)
are genuinely unregistered. The entry half-admits this at 53-55 ("the review this lane already
registers at tier A; it is named here by document, not by row id, because this entry's citation set
is exactly S081–S086") — so 40-41 and 53-55 contradict each other, and the self-imposed "exactly
S081–S086" rule discards a tier-A row for a column the amendment's central count depends on. Q6 also
wants the existing row named.

**Q2-C (low).** S084's scope cell names the two procedures and their coverage limits; the CG2 sentence
is a community-access statement carried in the row's anchor cell but not its scope cell. Append it.

---

## Q3 — claim stays inside its quote: **FAIL** (blocking)

### Q3-A (blocking) — CG7 paragraph, lines 97-102

> "S085's report describes the 方升 system's adaptive dynamic testing method … whose item bank is
> **rebuilt so that no two sittings share items**. A dynamic bank makes **leaderboard farming
> unfarmable**; a card makes a fixed bank honest about its exposure. **They are complements** …"

Anchored span, S085 pdf p.34 (printed 29), verbatim: `“方升”测试体系的底层测试数据库采用动态方式构建，
保证每次参与测试题目的都不相同`. Four widenings, one of them falsified inside the same page:

1. **"no two sittings share items"** — the next sentence on that page reads "…从而保证**每次测试时都有
   一定占比**的题目从未用于大模型测试": a *certain share* is fresh; the remainder is by construction
   shared. The entry's absolute states the opposite of the qualifier one line below its own quote.
2. **"rebuilt"** — the source heads the section `2.动态更新，测试题库实时化` and says items are
   "**定期进行扩充**" (periodically expanded), not rebuilt.
3. **"unfarmable"** — the source states its aim ("为了**解决** … 测试'刷榜'等问题") and then weakens it on
   the same page: generated items "质量很难保证，需要人工 … 核验", and "这些数据在一定时间内不会进行公开，
   后续会根据产业需求进行开放".
4. **"They are complements" / "a card makes a fixed bank honest"** — no S085 bytes concern cards
   (see Q2-A).

This is the round-9 defect ("direction replicating is not magnitude replicating") in a new place: the
source establishes *a rotating bank on a fixed programme*; the entry reports *unfarmability plus a
complementary design relation*.

### Q3-B (blocking) — the prevalence sentence, lines 108-113, now contradicts the entry's own table

> "…that is **R1 (strata) and S1/S2 (acquired / integrity)** in this entry's own naming. **The two
> fields this entry adds are therefore the two its source measured as rare in practice.**"

Nine lines above, the entry restated its own delta as: "**one new field** (S2's tri-state integrity
flag), **one new placement** (S1 …), and **one new value set** (R1's strata …)" (lines 70-74), adding
"the earlier 'two new fields' reading counted a placement as a field" (76-77). The negative-space
bullet was **not updated** and still uses the retired "two fields" reading — inside the same document.
And the pairing itself does not close: the quote names two variables (strata reporting, the acquired
type); under the current table only S2 is a new *field*, and S2 (card integrity) corresponds to
neither variable — its values come from the CTC form (line 67). Read as R1+S1 the sentence contradicts
lines 70-77; read as S1+S2 it invents a source variable. Either way the sentence is false.

Population, never stated: the evidence is "Two coders external to the design team applied a
pre-registered instrument to **41 documents**" (29 main-pass; κ 0.00-0.35), and the compiled paper
bounds it further — verified in the v1 PDF: "**Of the five variables where no single code dominates,
three clear** the prevalence-robust threshold registered in advance; the two that fall below it are
strata reporting and the acquired type introduced here". "Rare in practice" generalises a 41-document,
five-variable pool, and drops that 3 of 5 cleared.

Credit: the parenthetical at 109-110 ("the compiled paper … does not print this sentence") is TRUE —
"Two variables fall below" occurs in neither the v1 PDF text nor the v1 HTML, while the "three clear"
wording occurs in both.

### Q3-C (blocking-strength) — two union-table cells are false against the artefacts they cite

I re-read the two non-lane artefacts at the pinned commit/page (S123, S122) and the same-paper lane
row (S001), rather than trusting the round-6 staging table this entry "continues".

1. **Line 68 `R1 strata | (absent) | (absent) | (absent)` and lines 73-74 "R1's strata, which no
   design tabulates".** CTC v1.1 `templates/disclosure.yaml` at `4dba1ed` carries a full block:
   `strata_reported: {reported, strata[], aggregate_only, definition, pre_registered, scores{}}`
   (lines 19-26 of the template). The design tabulates strata. The staged round-6 table omitted the
   block; continuing it without re-reading the cited artefact is what produced the false cell — and
   R1 is the row Q3-B leans on.
2. **Line 65 `R4 regeneration status | "Change log" | evaluation_date | Reproducibility`.** CTC has a
   dedicated `regeneration: {procedure_published, procedure_url, artifact_only, notes}` block, which
   the row does not name; and GEM's "Reproducibility" cell is "Exact prompt templates; few-shot
   example ordering and count; scoring procedure; multi-run variance; generation parameters"
   (S001 §7 Table 3) — nothing about regeneration or instrument dates. So R4 currently cites the same
   CTC cell as R5 and the same GEM cell as R2, and its "already a column, narrower" rests, wrongly,
   on GEM.
   Correct cells that I verified and that the table gets right: AI Alliance "Contamination controls:
   Checks performed, their coverage, and known gaps", "Release date", "Change log: Describe
   score-affecting changes and compatibility with prior versions", "Grader evidence"; CTC
   `contamination_controls` per-type `controlled|not_controlled|unknown|n/a`, `elicitation_budget`,
   `evaluation_date`, the header note "unknown is a valid entry. So is not_controlled."; GEM
   Decontamination / Evidence Provided / Reproducibility as dimensions; AI Alliance has **no** strata
   field and GEM Table 3 has **no** strata dimension (both verified) — which is why the CTC block is
   the decisive one.

Related, smaller: **S2 (line 67) re-uses the CTC value pair already assigned to the blind-spot row
(line 62)** — the values exist in `contamination_controls`, so S2 is new as a *name for the card's own
state*, not as a new value domain; and S1's "delta in placement" is right about placement (CTC puts
type 5 on the release-side form) but its `network_access_during_eval` / `environment_sanitised` /
`transcripts_reviewed` / `boundary_integrity_monitored` value set is the same one.

### Q3-D (major) — the reliability sentence, lines 114-117, has no anchored quote anywhere

> "S081's own reliability is modest and skew-sensitive (its test–retest ceiling collapses under class
> skew, and pooling raises it through chance correction rather than better agreement)."

Faithful to the abstract (κ 0.00-0.35, median 0.21, 29 main-pass, single-coder ceiling 0.84, pooled
0.46 "through chance correction rather than better agreement") — but the S081 row's anchor cell
carries none of it and the entry quotes none of it. It is a load-bearing honesty sentence (it grounds
"Two coders filling this card need not agree") with no location, no re-readable target for the 180 d
recheck, and no target for Q10's second seat.

### Q3-E (major) — "no measurements", lines 118-120

`no document number` holds (no 编号/ISBN/No./报告号/版次 in the text layer). `no measurements` is false
about the document: 35 `%` tokens, a dataset count ("达到 209 个"), and decimal score tables
(51.8, 64.1, 58.3 …) at pdf pp.13/14/36/37 = printed 8/9/31/32. The operative claim ("nothing about
contamination rates"; no measurement of its own programme's effect) is true — narrow the clause. The
same three words sit in S085's scope cell (`corpus/SOURCES.md:111`), so the correction must be
appended there too (R1: append, never rewrite).

### Q3-F (minor) — Rejected bullet misstates the staged ground line, lines 161-164

> "its `ground:` line **explicitly declines the amendment relation** the flip required."

The staged card's ground line declines **admission**, not amendment: "The card format and the Q1–Q8
gate are supplied here; the *admission* of the card against the lane's existing
`knowledge/contamination-detection-and-transparency.md` vocabulary is the lane's call, not this
entry's." Neither "amendment" nor "relation" occurs in it; the staging *schema* file's ground line
asserts the relation ("so the lane's card becomes an amendment to published designs rather than a new
invention"). The bullet gives no quote and no location, which is how "explicitly" survived. Its first
half is correct (the staged card does present R1–R5/S1–S2 as "that format" and names none of the three
designs — verified across its 96 lines).

### Q3-G (minor) — round-29 refusal narrowed to one limb, lines 47-49

The lesson's reason is a two-limb Q6 rejection — "it offers a fourth card design where the campaign's
own round 6 tabulated three published designs and ruled this file an amendment, not a rival
(`lanes/kengaku/round6/DOMAIN.md:43-46`; `benchmark-card-field-schema-2026-10-23.md:71`). Secondary: all
six sources carry the campaign's 2026-10-23 opened date and none was re-opened this round"
(`corpus/lessons/round-29.md:223-226`). "exactly because" keeps one limb and drops the other, and the
flip quote silently drops its "for the card," qualifier.

### Q3-H (minor) — the frontier quote carries no location, line 81

The string is real (`corpus/README.md:274`, present since round-24 `94da19e`), but the entry names no
path where the sibling checklist entry writes (`corpus/README.md` §Frontier). Observation for the
Q6/Q7 seats, not a Q3 defect: the same frontier line was **edited this round** to add "(the entry's
own answerability questions, labelled **CG1–CG8** in the landed entry …)" — the index row now echoes
the entry's own label.

---

## Recommendation

**FAIL — do not admit these bytes.** Blocking reason: Q3. (i) The CG7 sentence widens its quote in
three places and states the opposite of the qualifier in the source's next sentence; (ii) the
prevalence sentence still uses a delta reading the entry itself retired nine lines above, and pairs
S2 with a source variable that does not exist; (iii) two union-table cells (R1 strata, R4
regeneration) are false against CTC v1.1 at its pinned commit. Q2 fails on the same CG7 sentence's
scope and on the misstated "three source rows are not in this lane's registry". Q1 passes
(header triad, cadence+action+date, writer; 13 of 14 spans re-locate on fresh captures).

Repair set, in priority order (append-only for registry cells, per R1):

1. **CG7 (97-102):** cut to the source — a dynamically built bank, periodically expanded, with a
   stated share of never-used items per sitting; delete "rebuilt", "no two sittings share items",
   "unfarmable"; mark "complements" as this entry's inference or drop it.
2. **Prevalence (108-113):** align with 70-77 (one field = S2, one placement = S1, one value set =
   R1); drop S2 from any source-measured claim; state the population (41 documents / 29 main-pass /
   5 variables, 3 cleared).
3. **Table cells:** R1's CTC cell → `strata_reported` (reported, strata[], aggregate_only, definition,
   pre_registered, scores); R4's CTC cell → `regeneration`, and drop GEM from R4 (no regeneration
   dimension) or mark the row "this entry's reading"; re-read the three artefacts instead of
   continuing round 6's table.
4. **Q2-B:** name S001 for the GEM column (tier A, already in the registry) and fix 40-41 to "two of
   its three source rows are not in this lane's registry".
5. **Reliability (114-117):** append the κ/ceiling span to S081's anchor cell and quote it here.
6. **"no measurements" (119):** narrow to "no measurement of its own programme"; append the same
   correction to S085's scope cell.
7. **Rejected bullet (161-164):** quote the staged ground line verbatim; strike "explicitly declines
   the amendment relation".
8. **S084 line 315** and **frontier location** as above; **round-29 "exactly because"** back to the
   lesson's two limbs.

## Residual risk and verification gaps

- **The file is live.** Two edits landed during this review; findings are pinned to `df0b6d41`. If
  more land, re-diff 97-102, 108-113, 65 and 68 first — they are the ones that decide the verdict.
  (Both blocker sentences were unchanged from 04:37 to 04:44.)
- **S085 "no document number"** rests on the PDF text layer; an image stamp or cover code would not
  appear there (the extracted cover has title, institute, "2024年6月" only).
- **S085 printed pages** could not be read as two digits here: the footer extracts as "2" on pdf
  pp.31-34 and "3" on p.35, so "printed 27/29" is confirmed by the constant pdf−5 offset, not by
  reading the digits.
- **S083** has no HTML full text; the anthology landing page is the only byte-contiguous capture I
  found. **S122/S123** were read at their pinned page/commit but I did **not** admit them as rows —
  that is admission work, not review.
- **Not tested (other seats' claims):** C1's `adoption_check.py --expect … --census`, C2's
  `round30_defects.py`, C3's gate selftest. I ran `sources_adopt.py`'s `locates`/`normalize_text`
  read-only on `/tmp` captures to execute the entry's own recheck.
- **Q13/Q14 note for the gate:** candidate `corpus/knowledge/contamination-transparency-card.md` is
  named; writer `KengakuR30` ≠ this seat; verdict below is a recommendation, not an admission.

# R30 falsify — entry audit Q1/Q2/Q3 (contamination transparency card)

Seat: `L1Kengaku30.R30FxEntryQ1Q3-3` (reviewer, round-30 falsify wave, 2026-10-25). Leaf: no dispatch.
Candidate: `corpus/knowledge/contamination-transparency-card.md`

VERDICT: FAIL — Q3 fails on two widening sentences (one of them contradicted by the adjacent
sentence of its own source) and Q2 fails on the same sentence's scope; Q1 passes.

Bytes reviewed: `sha256 0f2e16148cf170e7d30f29a7f25ad5f625e20540a70e3cc005c5d479d2af7880`, 171 lines,
mtime `2026-10-25 04:42:01 -0300`. **The file changed under this seat mid-review**: at 04:37 the
S085/S086 source lines still read "23 CJK characters" and "text-layer lines 78-81"; at 04:42 they
read "24 characters incl. the fullwidth comma" and "30 CJK characters, text-layer lines 80-81".
Every finding below is against the 0f2e hash; the two blocking sentences (lines 91-96, 102-107) are
byte-identical across both reads.

Every source was re-opened by this seat in a fresh capture; nothing below rests on a build report.
No tool installed, no package touched (pacman paused host-wide).

| id | locator | fetch | bytes | capture used |
|---|---|---|---|---|
| S081 | `https://arxiv.org/abs/2608.29463` | 200 | 44 646 | abs page HTML |
| S081 full | `https://arxiv.org/pdf/2608.29463v1` | 200 | 342 646 | `pdftotext -layout` (85 060 B) + HTML v1 |
| S082 | `https://arxiv.org/html/2607.01254v2` (+`/abs/`) | 200 / 200 | 212 631 / 43 552 | full-text HTML; abs page |
| S083 | `https://aclanthology.org/2026.findings-eacl.353.pdf` | 200 | 2 697 379 | `pdftotext -layout` / `-raw`; landing page HTML 45 139 B |
| S084 | `https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html` | 200 | 32 762 | HTML |
| S085 | `https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf` | 200 | 1 949 572 | `pdftotext -layout` (84 820 B) |
| S086 | `https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf` | 200 | 371 155 | `pdftotext` plain and `-layout` |

Scratch: `/tmp/r30fx-EntryQ1Q3/`. Lane write: this report only.

---

## Q1 — the triad opens the entry: PASS (two recorded defects, neither blocks)

Deciding evidence — header block, lines 1-9 of the candidate:

- six `source:` lines (1-6), one per id, each carrying the id, URL, anchor and quoted span;
- `verified-at: 2026-10-25` (line 7) — ISO date, equals the `opened` cell of all six rows;
- `recheck: 180d — re-fetch S081–S086 at their pinned locators, re-locate each quoted span in
  fresh captures and re-run python3 plans/sources_adopt.py --quote-file … --artifact … (next due
  2027-04-23)` (line 8) — cadence **and** action **and** a resolved date; the arithmetic re-derives:
  2026-10-25 + 180 d = 2027-04-23 (Oct 6 + Nov 30 + Dec 31 + Jan 31 + Feb 28 + Mar 31 + Apr 23);
- `writer: KengakuR30` (line 9) — present, and consistent with the in-lane `KengakuR<round>` form
  (`KengakuR26-2`, `KengakuR27`, `KengakuR28`, `KengakuR29-2`).

Both defects Q1 was written to prevent are absent: the recheck has a date and an action, and the
locators are the ones this round re-located (I re-located them independently, table above).

Strict-letter note (does not change the verdict). Q1 says "the first three lines are `source:`,
`verified-at:` and `recheck:`". With six sources, `verified-at` is line 7. The letter is
unachievable for a multi-source entry and is already violated by an admitted one —
`corpus/knowledge/benchmark-task-validity-checklist.md` has five `source:` lines and its
`verified-at` on line 6. Q1's own definition of the `source:` line says "the `S###` row id(s)",
plural, so the criterion is satisfiable in spirit but not in letter here. That is a QUALITY.md
wording debt (the criterion should read "the header block comprises source line(s), then
`verified-at:`, then `recheck:`"), not this entry's block.

**Defect Q1-1 (low).** The S084 line names a location for two of its three spans only: "the two
documented methods (html lines 344 and 397)" — but it also quotes
"但如今开源社区往往只会公开模型参数而非训练数据集", whose location is html line 315 (re-verified:
315, 344, 397 all present in the fresh page). The registry row carries 315; the entry does not.

**Defect Q1-2 (medium — the recheck is not executable as written).** Line 8's action is "re-locate
each quoted span in fresh captures and re-run `sources_adopt.py --quote-file … --artifact …`". I
ran that action against fresh captures using the lane's own locator (`plans/sources_adopt.py:328
locates()` — byte substring of newline-normalised text):

| span | capture | direct | after newline-unwrap |
|---|---|---|---|
| S081 a/b/c | abs HTML | ✔ ✔ ✔ | ✔ |
| S082 a/b | full-text HTML | ✔ ✔ | ✔ |
| **S083 a (14 w)** | PDF `-layout` **and** `-raw` | **✘** | **✘** |
| **S083 b (19 w)** | PDF `-layout` **and** `-raw` | **✘** | **✘** |
| S084 a/b/c | HTML | ✔ ✔ ✔ | ✔ |
| S085 a | PDF `-layout` | ✘ | ✔ |
| S085 b | PDF `-layout` | ✔ | ✔ |
| S086 title | PDF plain | ✔ | ✔ |
| S086 caveat | PDF plain | ✘ | ✔ (disclosed at line 6) |

S083 fails because the printed abstract hyphenates and column-interleaves: `pdftotext -raw` reads
`(1) a contamination-`/`resistant design by separating the publicly re-`/`leased game engine from
hidden card imple-`/`mentations` and `preserves eval-`/`uation integrity even if specific cards
leak`. No single de-hyphenation rule recovers both spans (`contamination-` keeps its hyphen,
`eval-/uation` drops it), so the S083 row is **not** byte-locatable in any PDF capture, while the
S086 row is. The row does not disclose this; the S086 row and the S082 row both do
("the abs page carries neither phrase", "located only on newline-unwrapped extraction"). Both S083
spans *are* byte-contiguous on the anthology landing page
(`https://aclanthology.org/2026.findings-eacl.353/`, `locates()` → true for both raw), which is the
locator the entry should carry — S082's row is the in-lane pattern.

Counts re-derived, all correct in the current bytes: 22 / 6 / 18 words (S081), 11 / 17 (S082),
14 / 19 (S083), 3 / 7 / 1 whitespace tokens (S084), 3 / 1 tokens with 24 characters incl. the
fullwidth comma (S085; I count 24 incl. `，`), 3 tokens for the S086 title and 30 characters for
the caveat (11 kanji + 19 kana; the caveat locates in the plain extraction at lines 80-81 exactly
as the entry now states).

---

## Q2 — tier floor: **FAIL**, on one claim's scope (the tier floor itself passes)

Tier of every cited row, read from `corpus/SOURCES.md` (all six: `status=mined`, `opened=2026-10-25`,
`used-by corpus/knowledge/contamination-transparency-card.md` — verified per row):

| row | kind | **tier** | declared scope (verbatim head) | in-scope for the entry's claims? |
|---|---|---|---|---|
| S081 | paper | **B** | "the four-field contamination disclosure protocol … its JSON schema and validator, and the rule that evaluation-time acquired contamination is reported with the score rather than with the benchmark release — for the preprint's own argument" | ✔ split rule, five types, prevalence sentence |
| S082 | paper | **B** | "the distinction between item-level and procedural transparency … where disclosure should attach — for the working paper's own argument, not peer reviewed" | ✔ |
| S083 | paper | **A** | "a peer-reviewed benchmark paper's own contamination-resistant design … for the paper's own design claim" | ✔ |
| S084 | docs | **A** | "its own two documented contamination-evaluation procedures and their stated coverage limits … not a claim about contamination in any particular model" | ✔ CG1/CG3/CG4; **partial** CG2 |
| S085 | docs | **B** | "the report's own account of the 方升 benchmark system's adaptive dynamic testing method and its dynamically built item bank; a sponsoring body's self-description with no document number, measurements or data release" | ✔ the bank fact; **✘ the "complements" relation** |
| S086 | paper | **A** | "the paper's own contamination-detection method and its false-positive caveat for code benchmarks" | ✔ |

Tier floor: no tier-C row stands alone, no `community` row is used, and the two B rows are labelled
for what they are inside the entry (line 1 "preprint", line 115 "S082 is a working paper"), so Q5's
labelling holds too. **The failure is scope, not tier.**

**Q2-A (blocking, same sentence as Q3-A).** Line 95: "They are complements". S085's declared scope
is the report's *own account* of ADT and its dynamically built bank — not a relation between that
bank and a disclosure card, which the report never mentions. The only place that relation exists
in-lane is the row's own `teaches` cell ("a card and a dynamic bank are complements") — a
self-citation: the entry's sentence and the row's synthesis are the same claim, and neither is
anchored in S085. The sentence is also inherited verbatim from the untouched staging entry
(`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md:87-88`:
"A dynamic bank makes leaderboard farming unfarmable; a transparency card makes a fixed bank honest
about its exposure. They are complements"), so it has never had a source behind it in any round.

**Q2-B (medium, disclosed but unresolved).** Lines 68-71: "So exactly two fields are new as
*fields* (S1, S2) … and the rest are this entry's names for columns those designs already carry."
Those five "already a column" cells and the two deltas rest on S122/S123/S124 — I verified those ids
are **absent** from `corpus/SOURCES.md` (`grep -n 'S12[234]' → no rows`). The entry discloses this
at lines 40-45 ("staged, not lane-admitted … so no load-bearing claim here rests on it (QUALITY
Q2)") and again under §What this does not establish. The disclosure is honest, but it collides
with line 68: if the delta is the amendment's substance — the very thing that makes this an
amendment rather than a design — then a load-bearing claim *does* rest on the staged file, and
line 41's "no load-bearing claim here rests on it" is false. Two clean exits: admit S122–S124 as
rows (then the mapping is lane-sourced), or restate line 68 as this entry's reading rather than a
fact. Separately, **S2's "delta" is a re-used cell**: its CTC entry (`unknown` / `not_controlled`)
is the identical cell already consumed by the blind-spot row two lines above (line 60), so S2 is
new as a *name*, not as a column.

**Q2-C (low).** S084's scope cell names the two procedures and their coverage limits; the CG2
sentence ("但如今开源社区往往只会公开模型参数而非训练数据集") is a general statement about the
open-source community, carried in the row's *anchor* cell but not in its *scope* cell. Extend the
scope cell by append (R1) rather than relying on the anchor alone.

---

## Q3 — claim stays inside its quote: **FAIL** (blocking)

### Q3-A (blocking) — the CG7 sentence, lines 91-96

> "S085's report describes the 方升 system's adaptive dynamic testing method — “方升”测试体系提出自适应
> 动态测试（Adaptive Dynamic Testing，ADT）方法对大模型进行评测 — whose item bank is **rebuilt so
> that no two sittings share items**. A dynamic bank makes **leaderboard farming unfarmable**; a
> card makes a fixed bank honest about its exposure. **They are complements** …"

Anchored quote, S085 pdf p.34 (printed 29), verified verbatim: `“方升”测试体系的底层测试数据库采用动
态方式构建，保证每次参与测试题目的都不相同`. Four widenings:

1. **"no two sittings share items" is contradicted by the next sentence of the same page**:
   "…从而保证**每次测试时都有一定占比**的题目从未用于大模型测试" — a *certain proportion* of items
   is fresh; the rest are necessarily shared. The entry's absolute states the opposite of the
   source's qualifier, which sits one line below its own quote.
2. **"rebuilt"** is stronger than the source's own heading and body: `2.动态更新，测试题库实时化`
   and "题目会通过人工补充、题目自生成和智能算法生成三种方式**定期进行扩充**" — dynamically updated
   and periodically *expanded*, not rebuilt.
3. **"unfarmable"** converts the source's aim ("为了解决 … 测试'刷榜'等问题") into an absolute the
   page itself weakens: 智能算法生成 items "质量很难保证，需要人工 … 核验", and 这些数据在一定时间内
   不会进行公开，后续会根据产业需求进行开放.
4. **"They are complements" / "a card makes a fixed bank honest"** — S085 contains no bytes about
   cards; the relation is the lane's, presented here as the source's ("S085's report describes …
   They are complements"). See Q2-A for its custody chain.

This is exactly the defect Q3 exists to stop (round-9: "Direction replicating is not magnitude
replicating"): the source establishes *a dynamic bank with a rotating share of fresh items*; the
entry reports *unfarmability plus a complementary relation*.

### Q3-B (blocking) — the prevalence sentence, lines 102-107

> "S081's arXiv abstract reports of its own protocol …: "Two variables fall below the prevalence-robust
> threshold registered in advance: strata reporting and the acquired type introduced here" — that is
> **R1 (strata) and S1/S2 (acquired / integrity)** in this entry's own naming. **The two fields this
> entry adds are therefore the two its source measured as rare in practice.**"

The quote names **two** variables: strata reporting, acquired type. The entry's own table (lines 62-71)
names the two new *fields* as **S1 and S2** and calls R1 a new *value set*, not a field. So the
mapping the sentence performs is:

- S1 (acquired contamination) ↔ "the acquired type" — ✔;
- S2 (card integrity flag) ↔ **nothing** — the abstract's below-threshold variables are strata and
  acquired; card integrity is not one of them, and S2's own provenance is the CTC form's
  `unknown`/`not_controlled` (line 65), not S081;
- R1 (strata) ↔ "strata reporting" — ✔, but R1 is the row the entry explicitly excludes from
  "fields".

Under either reading the sentence is false: read "fields" as S1+S2 and S2 has no source variable;
read it as R1+S1 and the entry contradicts its own delta count. Widening, plus a population that is
never stated: the abstract's evidence is "Two coders external to the design team applied a
pre-registered instrument to **41 documents**" (29 main-pass, per-variable κ 0.00-0.35), and the
compiled paper bounds it further — verified in the v1 PDF: "**Of the five variables where no single
code dominates, three clear** the prevalence-robust threshold registered in advance; the two that
fall below it are strata reporting and the acquired type introduced here". "rare in practice"
generalises a 41-document, five-variable pool to practice and drops that 3 of 5 cleared.

Credit where due: the parenthetical "the compiled paper states the same audit outcome in different
words and **does not print this sentence**" is TRUE — "Two variables fall below" appears in neither
the v1 PDF text nor the v1 HTML full text, while the "three clear …" wording does.

### Q3-C (major) — the reliability sentence, lines 108-111, has no anchored quote anywhere

> "S081's own reliability is modest and skew-sensitive (its test–retest ceiling collapses under class
> skew, and pooling raises it through chance correction rather than better agreement)."

The paraphrase is faithful to the abstract ("Per-variable linear-weighted κ runs from 0.00 to 0.35
(median 0.21) over 29 main-pass documents against a single-coder test-retest ceiling of 0.84,
collapsing under the class skew the registration anticipated; pooling raises it to 0.46 through
chance correction rather than better agreement") — but the S081 row's anchor cell carries none of
it, and the entry quotes none of it. A load-bearing honesty sentence (it grounds "Two coders filling
this card need not agree") with no quote, no location and no re-readable target for the 180 d
recheck, and no Q10 second-seat target either.

### Q3-D (major) — "no measurements", lines 112-114

> "It is the sponsoring body's own 2024 description of its own programme: no document number, no
> measurements, no data release."

`no document number` holds (no 编号/ISBN/No./报告号/版次 in the text layer). `no measurements` is
false as written about the document: the report carries **35 `%` tokens**, a dataset count
("达到 209 个"), and score tables with decimals (51.8, 64.1, 58.3 …) at pdf pp.13/14/36/37 (printed
8/9/31/32). What is true — and is the operative claim — is that the report has no measurement of
its *own programme's effect* and "nothing about contamination rates". Narrow the clause. Note the
same three-word clause is copied in S085's scope cell, so the correction has to be appended there
too (R1: append, never rewrite).

### Q3-E (minor) — the Rejected bullet mischaracterises the staged ground line, lines 155-158

> "its `ground:` line explicitly declines the amendment relation the flip required."

The staged card's ground line (read this session) declines **admission**, not amendment: "The card
format and the Q1–Q8 gate are supplied here; the *admission* of the card against the lane's existing
`knowledge/contamination-detection-and-transparency.md` vocabulary is the lane's call, not this
entry's." Neither "amendment" nor "relation" occurs in it. The staging *schema* file's ground line
does the opposite — it asserts the relation ("so the lane's card becomes an amendment to published
designs rather than a new invention"). "explicitly" is the false word; the bullet gives no quote and
no location, which is what let the error through. The bullet's first half is correct: that file
does present R1–R5/S1–S2 as *the* format ("The card below is that format") and never names the three
designs (verified: no AI Alliance / CTC / GEM / amendment mention in 96 lines).

### Q3-F (minor) — round-29 refusal restated more narrowly than the lesson, lines 47-49

> "Round 29 refused the staged version of this entry exactly because it presented the field list as
> *the* card format."

The lesson's reason is a Q6 scope rejection with a second limb the entry drops:
"reject on scope (QUALITY Q6): it offers a fourth card design where the campaign's own round 6
tabulated three published designs and ruled this file an amendment, not a rival
(`lanes/kengaku/round6/DOMAIN.md:43-46`; `benchmark-card-field-schema-2026-10-23.md:71`). Secondary:
all six sources carry the campaign's 2026-10-23 opened date and none was re-opened this round."
(`corpus/lessons/round-29.md:223-226`). "exactly because" converts a two-limb reason into one, and the
flip quote silently drops its "for the card," qualifier.

### Q3-G (minor) — the frontier quote carries no location, line 75

> The frontier's instruction was to "gate a knowledge entry on Q1–Q8".

The string is real: `corpus/README.md:274` (present since round-24 commit `94da19e`), but the entry
names no path or section, where the sibling checklist entry writes (`corpus/README.md` §Frontier).
Observation for the Q6/Q7 seats: the same frontier line was **edited this round** to add "(the
entry's own answerability questions, labelled **CG1–CG8** in the landed entry …)" — the index row
now echoes the entry's label. The quoted base fragment pre-existed, so Q3 is not violated by the
edit; but the round wrote its own label back into the row it cites.

### Q3-H (minor) — S084's third span has no location (see Q1-1).

---

## Recommendation

**FAIL — do not admit as landed.** Blocking reason: Q3. Two load-bearing sentences widen their
quotes, and one of them (Q3-A) states the opposite of the qualifier in the sentence that follows its
own quote, while the other (Q3-B) is internally inconsistent with the entry's delta table; the same
Q3-A sentence is also the Q2 scope miss. Q1 passes; Q2's tier floor passes (B, B, A, A, B, A).

Minimal repair set (no other seat's files touched, registry edits append-only per R1):

1. **CG7 (lines 91-96):** reduce to what S085 states — a dynamically built bank, periodically
   expanded, with a stated share of never-used items each sitting; delete "unfarmable", "rebuilt"
   and "no two sittings share items"; mark "complements" as this entry's inference (or delete it).
2. **Prevalence sentence (lines 104-107):** pair R1↔strata and S1↔acquired, drop S2 from the
   source-measured claim, and state the population (41 documents, 29 main-pass, the five-variable
   pool, 3 cleared / 2 below).
3. **Reliability sentence (108-111):** append the κ/ceiling span to the S081 row's anchor cell and
   quote it in the entry, so the 180 d recheck and Q10 have a target.
4. **"no measurements" (113):** narrow to "no measurement of its own programme"; append the same
   correction to S085's scope cell.
5. **S083 locator:** add `https://aclanthology.org/2026.findings-eacl.353/` as the byte-contiguous
   capture and disclose the PDF hyphenation, as S082's and S086's rows already do.
6. **S084 line 315:** add the location to the entry's source line and to the row's scope cell.
7. **Rejected bullet (155-158):** quote the staged ground line verbatim and strike "explicitly
   declines the amendment relation".
8. **Frontier quote (75):** add (`corpus/README.md` §Frontier).
9. **Delta claim (68-71) vs line 41:** either admit S122–S124 as rows or restate the delta as this
   entry's reading.

## Residual risk and verification gaps

- **The file is live.** It changed at 04:42:01 during this review (two source-line cells). Findings
  are pinned to `0f2e1614…`; if more corrections land, Q3-A and Q3-B must be re-checked against the
  new hash — they were unchanged across the two reads I made.
- **S085 "no document number"** rests on the PDF text layer only; an image stamp or cover code would
  not appear there (the CAICT cover page I extracted has title, institute and "2024年6月" only).
- **S085 printed page numbers** could not be read as two digits on this host: `pdftotext` renders the
  footer as "2" on pdf pp.31-34 and "3" on p.35, so "printed 27 / 29" is confirmed by the constant
  pdf−5 offset, not by reading "27"/"29" directly.
- **S083** has no HTML full text; the anthology landing-page abstract is the only byte-contiguous
  capture I found (both spans, raw `locates()` → true). The PDF is the locator the entry names.
- **Not tested here:** C1's frozen predicate (`plans/adoption_check.py --expect … --census`), C2's
  counter, C3's gate selftest — other seats' scope. I did run `plans/sources_adopt.py`'s
  `locates()`/`normalize_text()` read-only on `/tmp` captures to execute the entry's own recheck.
- **S122/S123/S124 were not tiered** — I verified the union-table cells against the staging file's
  bytes (the same object the entry cites), which is not the same as admitting those rows.

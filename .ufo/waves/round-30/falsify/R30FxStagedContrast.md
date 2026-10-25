# R30FxStagedContrast — the staged card versus the landed card, claim by claim

- Seat: `L1Kengaku30.R30FxStagedContrast-3` (leaf, no dispatch, no lane edits outside this file).
- Round 30, hyaku run 6, 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
- Candidate path under review: `corpus/knowledge/contamination-transparency-card.md`.
- Staged side (read-only): `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md`
  (92 lines, sha256 `9dee0e0306b9f38a1739b16a0a318e9c76bd3203f2c6656fceeba3f90eaa4dfc`) plus the
  package registry rows it depends on, `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`
  (sha256 `a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b`).
- Landed side at scoring time: sha256 `ba0465d1cbcbb0b62529343a7c4fe5c4c26e37db6fd462ac93a8e9d95f106d82`,
  186 lines, 18520 B, mtime 2026-10-25 04:49:45 -0300 (unchanged at 04:52 when this report was written).

VERDICT: FAIL — the amendment relation, the S081 cut, the S082 re-location and the S085 mark repair are all sound and now largely verified, but the landed text still asserts in two places that the round-6 file's "three source rows are not in this lane's registry" (the GEM review *is* this lane's S001) while its own §Extends says two are staged, carries a stale falsifier that names delta fields the current mapping no longer has, ships a broken bullet with a doubled marker and a duplicated sentence, leaves CG2's canary option with no citation at all, and points its recheck at a gate invocation that turns red on two of its six rows.

## 1. Snapshot identity (the entry moved four times under this seat)

| time (-0300) | sha256 of the candidate | bytes / lines | note |
|---|---|---|---|
| ~04:41 (first read) | not hashed | 168 lines | "two new fields (S1, S2)" reading; no grader-integrity row |
| 04:44:02 | `df0b6d41…251a4` | 17074 | grader row added; "one new field / one placement / one value set" |
| 04:45:17 | `f01b7cd2…d1e6cd` | 17116 | S083/S085/S086 provenance notes; per-source recheck form |
| 04:48:02 | `b29eac97…cc1385` | 18493 | transient: R4/R1/S1 re-mapped onto CTC keys, rarity bullet rewritten, CG7 bound added, Agreement bullet broken |
| 04:49:45 | `ba0465d1…f106d82` | 18520 / 186 | settled; identical wording to the previous row, two bytes-level fixes; the version every row below is scored against |

**Every row below is scored against `ba0465d1…`** (snapshot: `/tmp/r30fx-stagedcontrast/snap/card-final2.md`,
byte-identical to `snap/card-final.md`). A sibling seat was editing the entry throughout this seat's
window; findings name the sentence they apply to, so re-grep before acting if a five-line block changes
again. Line counts are `wc -l`; the 168-line first read predates the delta-table rewrite.

## 2. Evidence base (all re-derived, nothing taken from a build report)

Captures this seat made 2026-10-25 into `/tmp/r30fx-stagedcontrast/`:

| id | fetched URL | bytes | sha256 / note |
|---|---|---|---|
| S081 | `https://arxiv.org/abs/2608.29463` | 44646 | `4c81bd3c180736318ed03e31968fa4d109b94025ec596203dbc4e963b396908a` |
| S081 full | `https://arxiv.org/html/2608.29463v1` | 305243 | — |
| S082 | `https://arxiv.org/html/2607.01254v2` | 212631 | `82a5c5c6e9de647ee3fa7fb4c13c6d7b6decbaef5ed717b59c18d457d1371ed5` |
| S082 abs | `https://arxiv.org/abs/2607.01254` | 43552 | — |
| S083 | `https://aclanthology.org/2026.findings-eacl.353.pdf` | 2697379 | — |
| S084 | `https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html` | 32762 | — |
| S085 | `https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf` | 1949572 | HTTP 200 first try; the round-29 HTTP 000 did not recur |
| S086 | `https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf` | 371155 | — |
| CTC v1.1 | `https://raw.githubusercontent.com/Jangulo7/contamination-disclosure-paper/4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6/templates/disclosure.yaml` | 2181 | HTTP 200; read-only check of the mapping's claims |
| round-6 table | `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md` | — | read-only; six union rows |

Extractions: `pdftotext` 26.08.0, default, `-raw` and `-layout`. Gate:
`python3 plans/sources_adopt.py --quote-file <row> --artifact <capture>` with the live registry rows
copied verbatim to `/tmp/r30fx-stagedcontrast/row-S08N.md`.

## 3. The table

Status key: **kept** = same claim survives; **corrected** = same subject, changed content;
**dropped** = absent from the landed text; **added** = no staged counterpart.

### A. Frontmatter triads and registry anchors

| # | Staged claim | Landed | Why |
|---|---|---|---|
| A1 | S081 anchor is "`# Abstract` and Table `tab:instrument`" | **corrected** | Landed anchors abs line 124 plus the printed title; `tab:instrument` is dropped although the R1–R5/S1–S2 field names come from that table (`\label{tab:instrument}` = Table 3, rows F1 Strata … F4 Regeneration), and the HTML does not carry the label. |
| A2 | S081's first quote is the 30-word abstract sentence "We operationalize … in which unknown is a valid entry …" | **corrected** | Cut to 22/6/18-word spans; re-running the gate on the staged row against my own capture reproduces `EXIT 6 … REFUSED S081 overlong words=30 cap=25`, and the 30-word string is not a byte substring because the page writes `&#34;unknown&#34;`. |
| A3 | S081's table rows are quoted as `"F3 t5 Acquired"` and `"F4 Regeneration"` | **dropped** | Those are row labels, not spans: the gate returns `absent` for both, and no landed line quotes table text. |
| A4 | S082 anchor is the section "`# Benchmark Governance`" | **corrected** | On my v2 fetch `grep -c 'Benchmark Governance'` = 0, and both quotes sit at line 855 (§7.3) and 901 (§8.2); the staged row was gate-green on the full text, so only re-location could refute the anchor. |
| A5 | S083 is "one maintainer-engineering example of contamination resistance" | **corrected** | It is a peer-reviewed Findings of EACL 2026 benchmark paper (p.1 = printed 6710); the triad now also admits that its quote needs a hyphen-blind/whitespace-collapsed compare, which the gate does not implement. |
| A6 | S084 and S086 are "two detector implementations that state their own limits" | **corrected** | S084 is vendor documentation of two OpenCompass procedures, S086 a peer-reviewed method paper; Attribution says exactly that and drops the "implementations" label. |
| A7 | S085 anchor is "`# （二）"方升"自适应动态测试方法`" with ASCII marks | **corrected** | The report prints fullwidth marks: my extraction holds `“方升”自适应动态测试方法` twice and the ASCII form zero times, so the staged anchor was not a byte substring; the landed line keeps the report's own marks. |
| A8 | S085 body quote is one 45-character sentence with nested ASCII marks around 刷榜/方升 | **corrected** | Replaced by two quotable runs (ADT sentence; 采用动态方式构建… 24 characters incl. the fullwidth comma); the marks were never the gate's problem — it strips them, so bare `方升`/`污染` locate as one-word spans while the long span failed on line wrap. |
| A9 | S085's method "has three parts — 测试数据标签化管理、动态测试数据库和高质量测试数据抽样算法" | **dropped** | Grounded in the PDF (whitespace-collapsed match, p.32 = printed 27) and dropped without replacement; the landed CG7 paragraph describes the method's bound but not its three components. |
| A10 | S086 anchors the printed title and the caveat | **kept** | Title locates under default, `-raw` and `-layout` (gate green, 3 tokens); the caveat's count (30 characters) and lines 80–81 reproduce, and it is now marked as locating only on an unwrapped extraction. |
| A11 | `verified-at: 2026-10-23` | **corrected** | Now `2026-10-25`, C1's frozen predicate date and the date of my own captures. |
| A12 | `recheck: 180d — re-run the Gate commands for S081–S086 (ran 2026-10-23)` | **corrected** | Now names the invocation, a per-source capture form, and `2027-04-23`; run as written it still exits 7 on S083 and S085 — §6. |
| A13 | (no `writer:` line) | **added** | `writer: KengakuR30`, required by QUALITY Q13/Q14. |
| A14 | S084 anchor names only lines 344 and 397 (the two methods) | **corrected** | Now "the two documented methods and their access note (html lines 344, 315 and 397)"; lines 344/315/397 and token counts 3/1/7 reproduce exactly on my fetch. |

### B. Framing claims

| # | Staged claim | Landed | Why |
|---|---|---|---|
| B1 | "The card below is that format" — the entry supplies the card format | **corrected** | Reframed as an amendment to the round-24 entry and the round-6 tabulated designs; round 29's flip ("land it as an amendment to the tabulated designs rather than a new design") is quoted verbatim in `corpus/lessons/round-29.md`. |
| B2 | presents the field list as the card design (round 29 calls that "a fourth card design") | **corrected** | The heading "It is an amendment, not a fourth design" answers round-29's phrase; the staged file never uses it and simply claims to be the format. |
| B3 | S081 is "one formal protocol" | **dropped** | No protocol claim survives; S081 is cited for the one-run rule, the five types and the audit outcome. |
| B4 | Rule 1: "A card must be procedural, not item-revealing" | **kept** | Carried into the Claim with both S082 quotes intact (verified at 855/901). |
| B5 | Rule 2: "A negative must be stated as a negative" | **corrected** | Survives as CG4 plus the Claim's closing sentence; "a card that omits the blind spot is worse than no card" is gone. |
| B6 | "Every detector with a real access level has a blind spot" and the "worse than no card" consequence | **dropped** | Unsourced generalisation; only the sourced half survives (CG4's caveat). |
| B7 | "An Eastern precedent worth noting" as its own section | **corrected** | Folded into CG7 and Attribution; the "complements" sentence survives, the "remove the stable target" framing does not. |
| B8 | `ground:` line: "The card format and the Q1–Q8 gate are supplied here; the admission … is the lane's call, not this entry's." | **corrected** | Replaced by §Extends plus the README frontier quote; the deferral of the admission call is not carried (see E5). |

### C. Field table (R1–R5, S1–S2)

| # | Staged claim | Landed | Why |
|---|---|---|---|
| C1 | R1 = "per-stratum scores for a named stratification", why: a pooled number hides the stratification | **dropped** | Only "R1 strata" survives; the definition and its reason are absent, though the CTC form the mapping now cites carries `strata_reported` with `definition`/`pre_registered`/per-stratum `scores` — i.e. the dropped content is recoverable from the column the entry maps into. |
| C2 | R2 = "identified harness (named, pinned … or fully specified as a scaffold) plus at least two of version, budget, attempts, attempt resolution" | **dropped** | The name and CG6's question survive; the acceptance tests are gone, although they are literally the CTC `elicitation_budget` subfields (`harness`, `token_budget`, `attempts_allowed`, `attempt_resolution`, `scaffold_notes`) the entry now maps into. |
| C3 | R3 = "one of direct / derivative / temporal / distributional, each with the code observed" | **corrected** | The mapping says "S081's five types give it values", folding the acquired type into R3 while S1 is the acquired field; "code observed" is dropped, so the card never states R3's admissible values. |
| C4 | R4 = "the regeneration status of the instrument used, whether or not the reporter built it" | **dropped** | Only the name survives; the new row maps to the CTC `regeneration:` block (verified) but the "whether or not the reporter built it" distinction is gone. |
| C5 | R5 = "the date of the benchmark's last substantive update" | **kept** | Carried into CG8's second clause. |
| C6 | S1 values = network access, environment sanitisation, transcript review, boundary monitoring, with elements in `notes` | **dropped** | All four and `notes` are absent from the landed text — and they are exactly the CTC keys (`network_access_during_eval`, `environment_sanitised`, `transcripts_reviewed`, `boundary_integrity_monitored`, `notes`) the entry now cites to argue S1 is not a delta. Dropping the list removed the evidence for the entry's own newest argument. |
| C7 | S2 values = `controlled` / `not_controlled` / `unknown`, with `unknown` explicitly valid | **corrected** | Narrowed to `unknown` / `not_controlled`; `controlled` is removed although the CTC controls take all four values. |
| C8 | S2's justification: "a `controlled` claim for Type 5 without boundary monitoring is an assumption rather than a control" | **dropped** | The sentence exists only in the full text's Figure 2 caption (`figcaption` id `S4.F2.8`), not on the abs page the triad anchors; it is the strongest support for S2's "state for the card itself", and the entry already uses a full-text locator for S082, so the same pattern could have carried it. |
| C9 | the F1–F4 / t1–t5 numbering tying each field to a table row | **dropped** | No F or t identifier remains, yet the new delta paragraph says strata is "present in S081's own four-field protocol (F1, strata), which this entry cites" — F1 has no locator anywhere in the entry (see E18). |
| C10 | "R1–R5/S1–S2" is the card's field list | **corrected** | Demoted to "the field vocabulary this entry maps" — the right relation, but the vocabulary is left undefined in this lane (C1/C2/C4/C6/C8). |

### D. The eight questions

| # | Staged claim | Landed | Why |
|---|---|---|---|
| D1 | The gate is "Q1–Q8" | **corrected** | Relabelled CG1–CG8 for a real collision: `corpus/QUALITY.md` uses Q1 (triad) through Q8 (rejections); README:274 records the relabel. |
| D2 | Q2 access options include "a public web index" and "a canary", sourced to S084, S086 and "S077 (canary, per task)" | **corrected** | S077 is dropped (correct: C1's predicate is exactly six ids) but the canary option survives with no citation at all — no row in S081–S086 supports it. |
| D3 | Q2's answer includes S084's "no widely accepted solution exists when only parameters are public" | **corrected** | Moved to CG4 as "S084's stated access limit"; the phrase itself is no longer quoted, though the page prints it at line 315. |
| D4 | Q3 asks "which tier and which datasets/subsets were tested" | **corrected** | "Tier" is dropped; no CG row records a tier, yet README:275 says the designs now carry "tier tested". |
| D5 | Q4: string-match overlap over-reports; removal on match alone is doubtful | **kept** | CG4 keeps the Japanese caveat verbatim (verified lines 80–81); the staged `return x+y` example (5 occurrences in the PDF) is dropped. |
| D6 | Q5: release-side versus score-side | **kept** | CG5 unchanged in substance. |
| D7 | Q6 answerable from "S081 F2" | **corrected** | Re-pointed at the union table's `elicitation_budget` column, i.e. at the staged round-6 document (whose form does have the field, verified), not at a locator in this lane's registry. |
| D8 | Q7 answerable from S083's engine/implementation split and refresh protocol | **corrected** | S083 kept, S085's dynamic bank added as a second ground (verified, pages 32/34). |
| D9 | Q8 answerable from "S081 F4 and S082" | **corrected** | Both dropped in favour of the union table's `evaluation_date` / "Release date" columns and S085. |
| D10 | "Each is answerable from a published artefact" | **kept** | Retained as the gate's premise. |

### E. Claims with no staged counterpart

| # | Landed claim | Status | Why |
|---|---|---|---|
| E1 | In the amendment bullet: the round-6 file's "three source rows are not in this lane's registry, so no load-bearing claim here rests on it (QUALITY Q2)" | **added** | False for one of the three and self-contradicted: the GEM review is this lane's S001 (`aclanthology.org/2026.gem-main.50`, tier A, `mined`, opened 2026-10-19, teaches "the Contamination Transparency Card"), and §Extends now says "two of its three source rows are staged … so that one column is lane-checkable". |
| E2 | Delta arithmetic: "the delta is one field … S2's tri-state integrity flag is the only new field" | **added** | The two re-mappings beneath it are true against the pinned CTC form (`strata_reported`, `contamination_controls.acquired`, `regeneration:`), so the count is now defensible; residual: S2's row prints `unknown`/`not_controlled` in the CTC column, which are the *controls'* value vocabulary, not a card-state column, so the table cannot display its one delta — the prose has to. |
| E3 | R3 mapped to the round-6 row labelled "detector access / tier tested" | **added** | The cells (`Contamination controls`, per-type tri-state, GEM "Decontamination") do support a type row, so the relabel is defensible; what remains is that CG2's access question and "tier tested" have no union column at all. |
| E4 | "Round 29 refused the staged version of this entry exactly because it presented the field list as *the* card format" | **added** | Round 29's Gate row records a second frontier theme plus un-reopened sources; the design/rival objection is its amendment-set verdict — "exactly" overstates the record. |
| E5 | The staged "`ground:` line explicitly declines the amendment relation the flip required" | **added** | The staged ground line declines the *admission call* ("the lane's call, not this entry's"); it says nothing about amendment, so the stated reason is not in the bytes it cites. |
| E6 | Rejected: "A canary as a CG4 answer (round 30)" | **added** | The staged file never offers canary as a Q4 answer; its canary is an access option in Q2, which the landed CG2 keeps — a rejection of a claim that was not made. |
| E7 | S081 reliability: test–retest ceiling "collapsing under the class skew the registration anticipated", pooling "through chance correction rather than better agreement" | **added** | Both quoted fragments are in the abs page I fetched; the bullet is grounded (and now quotes rather than paraphrases). |
| E8 | "The card's fields are fields its own source measured as rare … S2 is *not* one its source validated, and the two fields S081 measured as rare are the two this entry marks as already-columned" | **added** | Rewritten during this seat and now correct: the source names "strata reporting and the acquired type", the table marks both as already-columned, and S2 is excluded — this repairs the earlier over-read. |
| E9 | Falsifier: "… would show the two delta fields are not rare in practice, narrowing the third bullet above" | **added** | Stale in three ways against the same file: there is now one delta field, not two; the fields it names (strata, acquired) are exactly the ones the mapping calls already-columned; and "the third bullet" is "Agreement is not established" — the target is the second bullet, "The card's fields are fields its own source measured as rare". |
| E10 | S082 is "a working paper", not a peer-reviewed result | **added** | The full text calls itself a working paper (3 occurrences); the abs page does not, which is why the full-text locator was needed. |
| E11 | "The field mapping is not lane-sourced" bullet: "a staged campaign document … whose three source rows this lane has not admitted" | **added** | Carries the same false "three" as E1 (S001 is admitted at tier A); a third statement of the count, and the only correct one is §Extends' "two". |
| E12 | "S085 cannot be used as evidence about anyone else" | **added** | Fair and supported (self-description, no document number, no data release); small tension with the new Attribution sentence, which says it "carries programme numbers and score tables" while this bullet says "no measurements". |
| E13 | §Corrections | **added** | "None yet. The staged version's S082 anchor named … does not exist" — a corrections section that opens by denying it has corrections. |
| E14 | The Agreement bullet's markup and text | **added** | The bullet opens `- **- **Agreement is not established.**` (doubled marker, unbalanced emphasis) and repeats its closing sentence twice ("Two coders filling this card need not agree; the card records what each stated, not a reconciled truth." appears at both the start of the wrap and the end). |
| E15 | CG7: "the next sentence on the same page bounds it: only a share of each sitting's items is fresh, the rest is shared" | **added** | Verified: the sentence after the quoted one reads "…都不相同，以解决存在题目封闭、考题过时、模型作弊等问题。动态测试数据库中的题目会通过…三种方式定期进行扩充，从而保证每次测试时都有一定占比的题目从未用于大模型测试". "The rest is shared" is a fair reading of a periodically expanded bank. |
| E16 | Attribution: S085 "carries programme numbers and score tables, but no contamination measurement" | **added** | Supported: the PDF has 表 1/表 2 captions, 分数 ×3 and 35 `%` occurrences, and no contamination measurement. |
| E17 | R4 → CTC "a dedicated `regeneration:` block"; R1 → `strata_reported`; S1 → `contamination_controls.acquired` plus run-side keys | **added** | All three verified against the pinned `disclosure.yaml` (2181 B): `regeneration:` exists with `procedure_published`/`artifact_only`; `strata_reported` with `pre_registered`/`scores`; `contamination_controls` with the four types plus `acquired`, `network_access_during_eval`, `environment_sanitised`, `transcripts_reviewed`, `boundary_integrity_monitored`, `notes`. |
| E18 | R1's strata are "present in S081's own four-field protocol (F1, strata), which this entry cites" | **added** | The F1 label is in Table 3 (`tab:instrument`), which this entry no longer anchors and whose label the arXiv HTML does not carry; the abstract I verified says "Strata and elicitation budget are prerequisites", which supports strata but not F1. |

## 4. Counts

| status | count | rows |
|---|---|---|
| kept | **6** | A10, B4, C5, D5, D6, D10 |
| corrected | **25** | A1, A2, A4, A5, A6, A7, A8, A11, A12, A14, B1, B2, B5, B7, B8, C3, C7, C10, D1, D2, D3, D4, D7, D8, D9 |
| dropped | **10** | A3, A9, B3, B6, C1, C2, C4, C6, C8, C9 |
| added | **19** | A13, E1–E18 |
| **total** | **60** | |

By section: A 14 (10 corrected, 2 dropped, 1 kept, 1 added); B 8 (5 corrected, 2 dropped, 1 kept);
C 10 (3 corrected, 6 dropped, 1 kept); D 10 (7 corrected, 3 kept); E 18 added.

The shape is what an amendment should look like: the design claim is gone, the vocabulary is demoted,
and correction dominates. The dropped block is dominated by value sets (C1, C2, C4, C6, C8) — and two
of those drops are self-harming, because the CTC form the entry now maps into carries exactly the
subfields the staged definitions described (C2's `elicitation_budget` children, C6's four run-side
keys). The landing argues from the form while deleting the list that the form proves.

## 5. What the landing kept that a re-grounding should have refused

Ranked by what a reader would be misled about.

1. **The "three source rows are not in this lane's registry" claim (E1, E11).** It is in two bullets
   and contradicted by the third mention in the same file (§Extends: "two of its three source rows
   are staged … one column is lane-checkable"). The GEM review is S001, tier A, `mined`, and its
   `teaches` cell already names the Contamination Transparency Card. The sentence is load-bearing:
   it is the QUALITY Q2 justification for the mapping.
2. **The recheck instruction as a runnable check (A12).** Run as written with poppler captures it
   returns `exit 7` for S083 (two spans `absent` on default, `-raw` and `-layout`) and for S085 (the
   ADT span `absent` on all three). The triad now discloses the needed preprocessing, but the command
   it hands the next round does not perform it, and R30RevGate recorded that S083's historic green
   came from matching `verify.py`, the seat's own script, not the PDF.
3. **The falsifier bullet (E9).** It names "the two delta fields" against a file that now claims one,
   names strata and acquired as deltas against a table that now calls both already-columned, and
   points at the wrong bullet. A falsifier that cannot be tested against its own entry is not a
   falsifier.
4. **CG2's canary option (D2).** The only staged citation (S077) was correctly dropped for C1's
   six-id predicate; the option stayed, so a gate question names an access level no row in this
   entry's set supports. `R30ConnCorpus` §D-e raised exactly this and it was not repaired.
5. **README:275's "tier tested" (D4, E3).** No CG row and no union row carries a tier for this entry,
   yet the README bullet says the tabulated designs now carry it.
6. **The two Rejected bullets against the staged file (E5, E6).** A Rejected section is evidence; a
   ground-line characterization the staged bytes do not support and a canary claim staged never made
   cost more than leaving them out.
7. **The broken Agreement bullet (E14).** Mechanical, but it is in a landed entry: a literal `- **- **`
   marker and a duplicated sentence.

## 6. Gate runs, reproduced (commands and observed lines)

Rows are the live `corpus/SOURCES.md` S081–S086 lines copied verbatim.

| invocation | observed |
|---|---|
| staged S081 vs `s081.html` | `REFUSED S081 overlong words=30 cap=25`; `absent=2` (`"F3 t5 Acquired"`, `"F4 Regeneration"`); `exit=6` |
| staged S082 vs `s082.html` | `spans=2 located=2`; `exit=0` — the gate cannot see that the anchor names a nonexistent section |
| staged S082 vs `s082abs.html` | `absent=2`; `exit=7` |
| staged S085 vs `s085.txt` | 5 spans; `located=4 absent=1`; ASCII-quoted `方升` and `污染` locate as one-word spans, the 45-character sentence is absent; `exit=7` |
| staged S086 vs `s086.txt` | `absent=2`; `exit=7` |
| landed S081 vs `s081.html` | `spans=3 located=3` words `[22, 6, 18]`; `exit=0` |
| landed S082 vs `s082.html` | `spans=2 located=2`; `exit=0` |
| landed S084 vs `s084.html` | `spans=3 located=3` words `[3, 7, 1]`; `exit=0` |
| landed S083 vs `s083.txt` (default), `s083-raw.txt`, `s083-layout.txt` | `absent=2`; `exit=7` on all three |
| landed S085 vs `s085.txt`, `s085-raw.txt`, `s085-layout.txt` | `REFUSED S085 absent words=3` for the ADT span on all three; the second span locates; `exit=7` |
| landed S086 vs `s086.txt`, `s086-raw.txt`, `s086-layout.txt` | `spans=1 located=1 words=3`; `exit=0` (the caveat is not ASCII-quoted in the row, so the gate never checks it) |

Root cause (observed, not inferred): `locates()` is an exact byte substring of newline-style-normalised
text — `plans/sources_adopt.py:276-278` folds `\r\n`/`\r` only, and `:328-336` says "never a fuzzy or
whitespace-insensitive match". Both spans cross typeset line breaks (S083 splits after "own"/"engine";
S085 splits at `（Adaptive Dynamic Testing，ADT）方` / `法对大模型进行评测`). The S083 row's "hyphen-blind
compare" and "byte substring after whitespace collapse" describe comparisons made outside the gate.

## 7. Adjacency defects in the landing's own supporting bytes

- `corpus/lessons/round-30.md` §Sources contradicts the registry rows the gate validates: S081's
  two-variables span is priced **21** (registry, entry and my count: 18); S084 is priced **13** for the
  ARC span and **3** for the 但如今… span (registry, entry and the gate: 7 and 1).
- `corpus/SOURCES.md` S085 gives no non-contiguity warning while the entry now says "three typeset
  lines, not byte-contiguous"; registry S086 says "text-layer lines 78-81", the entry says 80–81, my
  extraction says 80–81.
- `corpus/SOURCES.md` S085 prices the dynamic-bank span at "23 CJK characters"; the entry says "24
  characters incl. the fullwidth comma" (both defensible, stated differently in two artefacts read
  together; S086's "30 CJK characters" is the character count, of which 11 are kanji).
- `corpus/README.md:275` says the designs "now carry a record of detector access, tier tested and what
  a negative cannot rule out"; there is no tier field in CG1–CG8.
- `.ufo/waves/round-30/build/R30RevGate.md` §3 records S085 as `exit 4 … malformed=1 (curly-quoted
  anchor)`, but the live row is ASCII-quoted and returns `exit 7 absent=1`; the same table records
  S083's green as matching `verify.py:6`.
- The entry's Attribution ("carries programme numbers and score tables") and the S085 bullet ("no
  measurements") sit two sections apart and read as a contradiction unless the reader supplies
  "contamination measurements" for the second.

## 8. What the landing got right (so the FAIL is scoped)

- S082: the nonexistent section is refuted on the page (0 occurrences) and both quotes re-located at
  855/901.
- S081: the 30-word span is refused for length *and* absent as bytes (`&#34;unknown&#34;`); the three
  replacements are gate-green, and the entry's claim that the compiled paper words the outcome
  differently is true — the exact sentence is absent from the full HTML while its paraphrase is present.
- S085: marks preserved (ASCII 0, fullwidth 2); the ADT span's non-contiguity disclosed; CG7's new
  bound sentence verified in the PDF; the "no two sittings share items" overstatement replaced.
- S084: lines 344/315/397 and token counts 3/1/7 reproduce.
- S086: caveat count 30 and lines 80–81 reproduce; the title is gate-green on every extraction tried.
- The CTC re-mappings (E17) are true against the pinned form, which is the first time the union table's
  CTC column is checkable rather than copied; the rarity bullet (E8) was rewritten to match the table.
- Q1–Q8 → CG1–CG8: the collision is real (`QUALITY.md` Q1 = triad, Q8 = rejections) and documented.

## 9. Repairs this seat would require before admission

1. E1/E11: change both "three source rows are not in this lane's registry" statements to §Extends'
   "two are staged, the GEM column rests on S001" — the current sentences are false and self-contradicted.
2. A12/§6: either add wrapping-insensitive and hyphen-insensitive matching to `sources_adopt.py`, or
   restate the recheck as "unwrap the capture and record the recipe", and drop "hyphen-blind compare"
   from the S083 anchor until the tool can do it.
3. E9: rewrite the falsifier for one delta field (S2), name the second bullet as its target, and drop
   strata/acquired from it (both are already-columned now).
4. D2: cite the lane's canary bytes (`benchmark-task-validity-checklist.md:40,119-121`) in CG2 or
   delete "a canary" from the option list.
5. E14: restore one bullet marker and delete the duplicated sentence.
6. E13: make §Corrections either empty or a list; E5/E6: rewrite or drop the two staged-file rejections.
7. Either restore R2's and S1's value sets as mappings onto the CTC subfields they already name, or
   accept that the card's central argument is no longer reproducible from the entry alone (C2, C6).
8. C9/E18: re-anchor F1 (`tab:instrument`/Table 3, full HTML or PDF) or stop citing F1; D4/README:275:
   either add a tier field or correct the README sentence.

## 10. Remaining unknowns

- Whether the concurrent edit continues: the registry sentence (E1) survived three snapshots, the
  falsifier (E9) was written before the delta arithmetic changed, and both are one-line fixes a sibling
  may already have made by the time this is read — re-grep first.
- [INFERENCE] "The rest is shared" (E15) is my reading of a periodically expanded bank, not a quoted
  clause; the report states a share of fresh items, not the disposition of the others.
- Whether any extractor other than poppler's three modes yields byte-contiguous S083/S085 spans is
  unknown to this seat; the entry's own recheck names the preprocessing, which implies the seats know
  the raw captures fail.
- The staged S077 `used-by` asymmetry is a staged-file property; nothing here re-opens it.

## 11. Tools installed or upgraded

None. No package, tool or binary was installed or upgraded for this seat; no pacman transaction was
run (pacman is paused host-wide). Scratch: `/tmp/r30fx-stagedcontrast/`.

Report: .ufo/waves/round-30/falsify/R30FxStagedContrast.md

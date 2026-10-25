# FSourceS066 — Q10 reread: S066 Reiczigel known-vs-estimated row, Gate quote/anchor, candidate use and append-only correction

Identity: **KengakuR28.FSourceS066** (scout), leaf seat. Author-side, read-only; no production file,
registry cell, fixture, candidate or instrument was edited. No subagent dispatch. No outside/non-author
closure is claimed. Paths relative to lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Pins and access

- Candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, writer `KengakuR28`,
  12405 bytes / 146 lines, sha256
  `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (matches
  `.ufo/waves/round-28/candidate-freeze.json:candidate_sha256`).
- Proposed canonical path `corpus/knowledge/webarena-task-spec-audit.md` is absent
  (`test -e` exit 1), consistent with deferred admission.
- S066 row: `corpus/SOURCES.md:88`. Gate row: `corpus/lessons/round-28.md:45`. Old-knowledge
  correction: `corpus/knowledge/attribution-interval-calibration.md:191–205`.
- Source: Reiczigel, Földi & Ózsvári, “Exact confidence limits for prevalence of a disease with an
  imperfect diagnostic test”, *Epidemiol. Infect.* 138 (2010) 1674–1678,
  doi:10.1017/S0950268810000385. The row URL is the DOI.
- Access: **no live publisher call by this seat.** I copied the archived publisher PDF already
  retained by OpenS038 (`.ufo/waves/round-28/scratch/OpenS038/wb20261004.pdf`) into my own scratch
  (`.ufo/waves/round-28/scratch/KengakuR28.FSourceS066/`). sha256
  `fc935f40a6f58cb7fea9407490a768fd63078eaf46ccd3b40b260d109de82e8c`, 108614 bytes, 5 pages.
  `pdfinfo`: Title/Subject/Author/Creator metadata and `CreationDate 2010-08-18` match the publisher
  version; base32 SHA-1 `GWYEXRXGLWELYZ5D4M3HDN4ZA4K6VJJS` equals the Wayback CDX digest recorded in
  `build/OpenS038.md`; page footer reads “Downloaded … on 04 Oct 2026 at 19:02:46” and header reads
  “Epidemiol. Infect. (2010), 138, 1674–1678 … doi:10.1017/S0950268810000385”.
- My `pdftotext -layout` output sha256 `edd31ec7cad1d313e4a563f29a8c6b0e59c2f51e0fee30c0b6e8712f4ce6fd0b`
  is byte-identical to OpenS038’s `wb.txt` (`diff -q` exit 0); `pdftotext -raw` independently contains
  the sentence after ligature/hyphen normalisation.
- Access limitations (from `build/OpenS038.md`, attempts 1–7): DOI and Cambridge PDF/article HTML
  returned HTTP 429; Wayback raw capture returned HTTP 200; live HTML via WebFetch was corroborating
  and possibly cached. I did not re-call any of these routes.

## Gate quote and actual location

Gate row (`corpus/lessons/round-28.md:45`): “the proposed methods assume that sensitivity and
specificity are known exactly” — Discussion p.1677, archived publisher PDF reopened by OpenS038;
supersedes S038’s unqualified fix scope.

- Verbatim in the archived PDF: “It should be noted that the proposed methods assume that sensitivity
  and specificity are known exactly.” (`wb.txt` layout lines 243–245, right column; raw mode joins
  “known ex-\nactly”).
- Word count: **11** whitespace tokens, therefore ≤25. I did not rely on any seat’s claimed count.
- Section: `DISCUSSION` header at `wb.txt:227`, `CONCLUSION` at `:256`; the quote lines 243–245 lie
  between them → Discussion, not Conclusion.
- Page: the quoted fragment’s `assume…` token starts at raw offset 25657 (the preceding “the
  proposed methods” is on layout line 243); p.1677 header offset 21965; next p.1678 header offset
  29611 → p.1677 (PDF page 4 of 5). The Introduction coverage sentence is raw offset 6713 between
  p.1675 (offset 5845) and p.1676 (offset 14492).
- No ellipsis is needed: the quoted words are contiguous; the fragment begins mid-sentence with
  lowercase “the”, and the paper continues “These values are used in the procedure as fixed numbers
  known without any uncertainty.” The Gate quote does not include that continuation.

## Row tier / scope / teaches

`corpus/SOURCES.md:88`: kind `paper`, tier `A`, status `mined`, opened `2026-10-21`, recheck `180d`,
used-by `corpus/lessons/round-28.md, corpus/knowledge/attribution-interval-calibration.md`.

- Tier A is correct as scoped: the row is the original publisher paper, not a secondary account.
  Tier is scoped to the row’s own coverage-warning/exact-inversion scope, per SOURCES contract v1.
- Scope (“this paper’s coverage warning and exact-test-inversion scope, not an estimated-sensitivity
  interval port”) is supported: Introduction p.1675 (naive adjusted interval can cover 60% at nominal
  95%); Methods p.1675 (“Both Blaker’s and Sterne’s CIs are derived by inverting the corresponding
  tests”); Discussion p.1677 (assumption and estimated-case gap); Conclusion p.1677 (known Se/Sp easy
  adjustment).
- Teaches (“supersedes S038’s unqualified fix clause — the exact Blaker/Sterne construction discussed
  assumes known sensitivity/specificity; estimated properties remain a distinct uncertainty problem,
  so the lane’s bound is not this paper’s exact method”) is supported by the Discussion passage and
  the Conclusion. S038’s `teaches` cell (`corpus/SOURCES.md:60`) is indeed unqualified:
  “test-inversion (Blaker, Sterne) limits on the adjusted scale fix it”. The base-vs-current cell diff
  shows S038’s id/source/kind/tier/scope/anchor/teaches unchanged (only status and used-by changed),
  so a superseding row is the correct mechanism rather than an edit.
- Same-publication scoped rows are the registry’s established pattern: S064 shares S054’s CommonMark
  0.31.2 URL, and S065 shares S052’s Python `json` documentation page with a different anchor; S066
  shares S038’s DOI. `corpus/SOURCES.md:111` calls S064–S066 “scope/anchor extensions, not3 new
  publications”. No duplicate-ID issue; S066 is not in the frozen C2 population
  (`plans/fixtures/r28/registry/population.json` lists S038 and S049–S060), so its used-by cells do
  not enter the C2 verdict. Structure: `plans/registry_check.py:54` initializes `refs` only from
  `population["source_ids"]`, and the per-path scan intersects matches with `refs.keys()` (line 63),
  so non-frozen IDs such as S066 are ignored; I did not run the checker.

## Final draft source use

- Draft front matter (`draft:1`) cites S061–S063 only. A grep for `S066|S038|Reiczigel|attribution`
  in the draft returns no match. `draft:136–141` explicitly says the new audit does not count the
  round28 source-reference diagnostic and keeps the claims partitioned.
- S066 is therefore **not** used by the frozen candidate. Its used-by cell listing only the round-28
  lesson and `corpus/knowledge/attribution-interval-calibration.md` is complete: a full-lane S066
  census finds exactly those two production paths (plus the registry row itself and the round-28
  search note). No canonical citing path is missing.
- Candidate sha256 `77e19d5b...`; canonical path absent. No candidate S066 claim exists to verify.

## Old-knowledge append-only correction

`corpus/knowledge/attribution-interval-calibration.md:191–205` appends
“## Round28 source-scope clarification (2026-10-21)”.

- Append-only: `git diff b9b24796277020d1b9b01923b45313d6a565e664 -- corpus/knowledge/attribution-interval-calibration.md`
  shows 16 insertions after EOF and 0 deletions/modifications; pre-existing lines 1–189 are unchanged and lines 190–205 are the appended block (including the blank separator).
- Claims verified: (i) S038’s coverage warning remains supported by Introduction p.1675 (left column
  lines 82–86); (ii) its old registry row is indexed `mined` because this file already cited it
  (`corpus/knowledge/attribution-interval-calibration.md:144`, S038 status/used-by at
  `corpus/SOURCES.md:60`); (iii) S066 supersedes S038’s unqualified fix clause; (iv) the exact
  Blaker/Sterne test-inversion construction assumes Se/Sp known exactly (Discussion p.1677);
  (v) estimated Se/Sp is not developed for exact intervals — the paper says “but currently it has not
  been developed for exact intervals”; (vi) no interval method was ported this round; (vii) the
  historical “conservative” characterisation remains superseded by the round25 correction above (the
  file’s round25 text at :139–145).
- No new frozen13 edge: S038 was already cited in this file at :144, and S066 is not in the frozen13.
  The appended block adds no new row-file link among the frozen13 under the file-level counter; the
  frozen population is unchanged. I did not run `registry_check.py` (not assigned).
- Label: Amendment 1 item 5 says calibration corrections are “append-only, explicitly marked as errata
  and separate from C1”. The block is append-only, explicit, separate from C1 and adds no frozen13
  edge, but it is headed “source-scope clarification” and calls itself “a source-scope clarification”,
  not “errata”/“erratum”. See F2.

## Mutable-cell delta vs base

Cell-level parse of `git show b9b2479:corpus/SOURCES.md` vs current:

| row | cell | base → current |
|---|---|---|
| S038 | status | queued → mined |
| S038 | used-by | — → corpus/knowledge/attribution-interval-calibration.md |
| S050 | used-by | corpus/lessons/round-27.md → corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |
| S066 | all | new row (11 cells), status mined, opened 2026-10-21, recheck 180d |

No other S038/S050 cell changed; immutable cells (id/source/kind/tier/scope/anchor/teaches) are
unchanged. S066 is absent at base. This matches `corpus/lessons/round-28.md:62–68` and the statement
that existing recheck/opened cells are unchanged.

## Findings

**F1 (Low; registry anchor metadata; actionable because the row is explicitly an anchor extension).**
`corpus/SOURCES.md:88` anchor says “2010,
Introduction/Methods p.1675 and Conclusion p.1677”. The quote the Gate row attributes to S066
(`corpus/lessons/round-28.md:45`) is in **Discussion p.1677**, not Conclusion; the Gate and the
knowledge block (`:197`) both say Discussion.
Page 1677 is correct, and the Conclusion p.1677 does contain a related sentence — “In case of known
sensitivity and specificity CIs are easy to adjust by applying the Rogan & Gladen transformation to
the CI endpoints.” (23 words; raw offset 27728) — so the anchor is not a false location. But the
round’s anchors point at the quoted evidence (S061 task0:18–21; S062 EvaluatorComb:336–352 containing
351; S063 146–173 containing 169; S064 §4.5 paragraph; S065 named paragraph), and S066 is explicitly
an “anchor extension” (`corpus/SOURCES.md:111`). The anchor therefore omits the section of its own
superseding sentence and names a different section instead. Resolution (L1): add “Discussion p.1677”,
or state that Conclusion is an intentional second anchor and add Discussion. No number, quote, tier,
scope or teaches claim is falsified.

**F2 (Low; label conformance).** The knowledge correction is a “source-scope clarification”, not
literally marked “errata”/“erratum”; Amendment 1 item 5 says “explicitly marked as errata”. The
substance (append-only, separate from C1, no new frozen13 edge) passes. L1 may accept the label as an
explicit named correction or rename it.

**F3 (Low; wording).** Gate row `:45` says “supersedes S038’s unqualified fix **scope**”; the registry
row says “fix **clause**”. The unqualified cell is S038’s `teaches` clause (`corpus/SOURCES.md:60`),
not its `scope` cell, so “clause” is the precise word. No factual impact.

**No finding:** URL/DOI `https://doi.org/10.1017/S0950268810000385` matches the PDF header DOI and
the S038 row; publication 2010, 138:1674–1678; archive capture date 2026-10-04 and digest
`fc935f40…`/base32 `GWYEX…` reproduce; 5 pages and publisher metadata; quote verbatim, 11 words,
Discussion p.1677 right column; tier A / kind paper, narrow scope, teaches accuracy; candidate
non-use and used-by completeness; append-only knowledge correction; S038/S050 cell deltas match the
lesson.

## Remaining unknowns

- I did not re-query the Wayback CDX or the live publisher (no network); the archive’s “authenticated”
  status is accepted from OpenS038’s recorded CDX digest match. I independently verified the PDF’s
  base32 SHA-1 equals that recorded digest and that the PDF metadata/text are the publisher’s.
- I did not run `plans/benchmark_spec_audit.py` or `plans/registry_check.py` (not assigned); C2
  counters are not re-measured here.
- Page/column placement comes from `pdftotext -layout`/`-raw`; page boundaries are byte-offset
  unambiguous, while right-column placement comes from the two-column layout text split, consistent
  with OpenS038’s stated limitation.
- Whether L1 reads the registry anchor as a quote-location or a relevant-passage list is a resolution
  decision.

Installs: none. Tools used: `sha256sum`, `sha1`/base32 via `python3`, `pdfinfo`, `pdftotext`,
`git show/diff` (read-only), `grep`/`awk`. No pacman/uv/npx, no network, no browser; no LSP server
applies to a PDF source (the quote/anchor checks are direct byte/line reads, not grep-as-semantic-
proof).

**Canonical proposed path:** `corpus/knowledge/webarena-task-spec-audit.md` (not admitted; candidate
sha256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`).

VERDICT: PARTIAL (scoped) — the S066 quote, 11-word count, Discussion p.1677 location, DOI/2010
date, archive digest, tier A/paper, scope, teaches, candidate non-use, used-by completeness,
append-only knowledge correction and S038/S050 cell deltas all pass; the actionable item is F1, the
registry anchor cell naming Conclusion p.1677 instead of the quoted Discussion p.1677, with F2/F3 as
low-severity notes. No substantive source claim or number is falsified. This is not an admission or
an outside closure.

## v2 — post-falsification S067 chain (appended 2026-10-21; v1 above preserved)

L1 reports S066 committed with its immutable anchor preserved, S067 added to supersede the location,
a post-falsification lesson Gate with the exact 11-word quote, and an appended anchor erratum in the old
attribution entry. I re-read all current fields against the unchanged archived bytes; no live publisher
call was made.

### Current chain and fields

- `corpus/SOURCES.md:89` S067: `paper`, tier `A`, `mined`, opened `2026-10-21`, recheck `180d`,
  used-by `corpus/lessons/round-28.md, corpus/knowledge/attribution-interval-calibration.md`.
  - scope: “exact location of the known-sensitivity/specificity caveat, not estimated-property
    interval validity”.
  - anchor: “2010 Discussion p.1677 right column, archived publisher PDF text243–245 under
    Discussion227; Conclusion begins256”.
  - teaches: “supersedes S066's anchor — the quoted known-exactly caveat is in Discussion p.1677,
    not the listed Conclusion; the scientific scope correction to S038 is unchanged”.
- `corpus/SOURCES.md:88` S066 is the same 11-cell row as v1: anchor still names Conclusion p.1677,
  teaches/scope/status/used-by unchanged. The v1 F1 anchor defect is resolved by the superseding S067
  row, not by a silent edit of S066.
- Lesson M77 (`corpus/lessons/round-28.md:168`): “FSourceS066/FBoundaryNoAxisHarm: caveat in Discussion,
  not listed Conclusion; Q10 | NewS067 supersedes S066 anchor after its build commit; old cells
  preserved. Scientific scope unchanged.” The post-falsification Gate row (`:207`) carries the same
  quote/location; `:215–217` states S066's source scope remains right and that the Gate and older-entry
  clarification named Discussion from the start.
- Knowledge erratum (`corpus/knowledge/attribution-interval-calibration.md:207–210`): “Round28 anchor
  erratum: **S067 supersedes S066's registry location** for the known-exactly caveat: it is in
  Discussion p.1677 (archived text243–245), not the listed Conclusion. The scientific
  known-versus-estimated distinction above is unchanged. The Gate and this entry already named
  Discussion; the old row is preserved rather than silently repaired after its build commit.”

### Anchor and quote re-verification (unchanged archived bytes)

- Archived PDF sha256 `fc935f40a6f58cb7fea9407490a768fd63078eaf46ccd3b40b260d109de82e8c` and my
  `wb.txt` sha256 `edd31ec7cad1d313e4a563f29a8c6b0e59c2f51e0fee30c0b6e8712f4ce6fd0b` are identical to
  v1; no live/cached publisher route was called.
- `wb.txt:227` is the `DISCUSSION` header; right-column lines 243–245 read “It should be noted that
  the proposed methods / assume that sensitivity and speciﬁcity are known ex- / actly.”; `:256` is the
  `CONCLUSION` header. The quote lies between the p.1677 header (offset 21965) and the p.1678 header
  (offset 29611). S067's “Discussion p.1677 right column … text243–245 under Discussion227; Conclusion
  begins256” is therefore exact.
- Quote: “the proposed methods assume that sensitivity and specificity are known exactly” — 11
  whitespace tokens, exact in layout and raw extraction. The post-falsification Gate (`:207`) and
  `corpus/evidence/round28-calibration/source-correction-quotes.json` both record the same URL,
  accessed date, location and 11-word count; no live publisher-success claim is made.

### Append-only and population checks

- Knowledge diff vs base `b9b2479` is now 21 insertions, 0 deletions: the v1 block (current lines
  191–205) is unchanged, and the anchor erratum (207–210 plus the blank separator) is appended.
- S067 is not in the frozen13 population (`plans/fixtures/r28/registry/population.json`), so it adds no
  C2 row-file edge; both used-by paths contain S067 literally. S066's used-by is unchanged. The lesson
  `:190–192` partitions S064–S067 to calibration and excludes new rows from the frozen13 C2 verdict;
  `:202–203` calls S067–S069 metadata/scope corrections, not new publications.
- S067 shares the DOI with S038/S066; this is the round's established same-publication scoped-row
  pattern (S064/S054, S065/S052), with S066's old cells retained.

### Current candidate and freeze state (observation, outside the S067 chain)

- The current draft `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` is sha256
  `3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182`, 14419 bytes / 163 lines. It
  cites S061/S068, S062/S069, S063 and S005/S006; a `S066|S067|Reiczigel` grep returns no match, and
  its calibration section (`:153–158`) still says the audit does not count the source-reference
  diagnostic. S066/S067 are therefore unused by the draft, and the S067 used-by cell is complete.
- `.ufo/waves/round-28/candidate-freeze.json` still pins `77e19d5b…`, and the lesson (`:149–157`) calls
  frozen draft `77e19d5b` and its 21-case/12-case instruments historical. No new freeze for
  `3eb2afe5…` is observed. This is an admission-boundary observation for L1, not an S067 defect; I did
  not edit the draft or the freeze file.

### Findings carried/updated

- v1 F1 (anchor cell named Conclusion) — **resolved by S067** (`corpus/SOURCES.md:89`), recorded by M77
  and the knowledge anchor erratum; S066's old cells are preserved and the scientific content is
  unchanged.
- v1 F2 (errata label) — the location correction is literally labeled “anchor erratum” (`:207`); the
  earlier scientific-scope block remains a historical “clarification” and is not rewritten. Low-severity
  historical note only.
- v1 F3 (Gate “fix scope” vs row “fix clause”) — unchanged wording drift; no factual impact.
- New observation: S067's evidence record (`source-correction-quotes.json`) records URL/location/quote/
  accessed/11 words but does not repeat the archived PDF or extracted-text digest; it inherits capture
  identity from S066's anchor, the lesson's S038 paragraph (`fc935f40…`), and `build/OpenS038.md`
  (`wb.txt` `edd31ec7…`). If full self-containment is required, L1 can add the digest; the line numbers
  are stable for the unchanged bytes. Not a defect in the location correction.

**Canonical proposed path:** `corpus/knowledge/webarena-task-spec-audit.md` (still absent; not admitted).

VERDICT (v2, scoped to S066→S067): PASS — S067's row fields, Discussion p.1677 right-column
text243–245 anchor, 11-word Gate quote, M77, and append-only anchor erratum all verify against the
unchanged archived bytes; S066's immutable cells are preserved and the scientific scope correction is
unchanged. v1 remains above as the historical PARTIAL. This is not a whole-round admission or an outside
closure.

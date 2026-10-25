# R33FArxivScope — S104 source anchor and survey scope falsification (arXiv 2412.05579v2)

Seat: KengakuR33.R33FArxivScope (leaf, no subagent dispatch). Date: 2026-10-25.
Lane bounds: read-only; no edits, commits, or tool installs. Only file written: this report.
Scratch: none used. Commands below are `grep`/`awk`/`wc`/`sha256sum` reads over the pinned
capture; **no live fetch was re-run** (R33SurveyScope's live-API claims are reported as
unverified-by-me, not re-executed).

## 1. Evidence base (all anchored, read-only)

- Capture: `.ufo/waves/round-33/assimilation/captures/arxiv-2412.05579v2-abs.html`
  — 43,661 bytes, 618 lines (617 `\n`), sha256 `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660` matches the committed `SHA256SUMS.txt` (`sha256sum -c ...` → OK).
- Landed S104 row: `corpus/SOURCES.md:119` (11-col registry row).
- Entry citing it: `corpus/knowledge/benchmark-grader-semantics.md` (`:3`, `:5`, `:25`, `:28`, `:38`, `:107-124`).
- Build reports under test: `R33CaptureArxiv.md`, `R33SurveyScope.md`, `R33RowDrafts.md`, `R33EntryPatch.md`, `R33C1KillRule.md`, `R33GateMutants.md`.

## 2. Behavior

Task: read current arXiv capture lines 41, 116, 124, 131; compare the S104 row's
version/date/title/abstract/comments and spelling claims against them; report only anchored
facts and any scope overreach. All reads done; findings below.

## 3. Verified anchored facts (capture bytes vs S104 row)

### 3.1 Title — `:116` (the capture report's `:117` tag is off by one)
- `:116` holds the one `Title:` `<h1 class="title mathjax">` (byte 11299 = `<h1 class="title mathjax"`; line starts at byte 11295):
  `LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods` (8 words).
- The same exact string occurs 11×: `:4`, `:21`, `:23`, `:33`, `:41` (citation_title), `:98`, `:116`, `:117`, `:177`, `:243`, `:248` — matching R33CaptureArxiv §3's count/list.
- **R33CaptureArxiv §3 is wrong on the line tag**: it says "Line 117, the `Title:` line (offset 11299)". The byte offset 11299 is correct but belongs to **line 116**; `:117` is the Authors div, whose only title occurrence is inside the "View a PDF of the paper titled …" sentence (byte 12414), not a Title: line. (R33SurveyScope's `:4`/`:116` mapping is correct.)
- S104 row anchor cites `:41` for the title: `:41` does carry `citation_title` (byte 5367) with the same string → **resolves**, and the entry explicitly labels it "title as served in the capture's `citation_title` meta tag" (correctly scoped). The visible h1 line is `:116`.

### 3.2 Version / date — row matches capture exactly
- `:115` dateline: `[Submitted on 7 Dec 2024 (v1), last revised 10 Dec 2024 (this version, v2)]`.
- `:41` meta: `citation_date` = `2024/12/07`, `citation_online_date` = `2024/12/10`.
- `:164-167` submission history: `[v1] Sat, 7 Dec 2024 08:07:24 UTC (4,814 KB)`; `[v2] Tue, 10 Dec 2024 05:49:12 UTC (4,809 KB)`.
- S104 anchor: `arXiv 2412.05579v2 (v1 Sat, 7 Dec 2024; v2 Tue, 10 Dec 2024)` — **matches** :115/:165/:167 byte-for-byte in content. `:109` confirms the served id `arXiv:2412.05579v2`; `:115` says "this version, v2" (no silent redirect).
- **Provenance gap (unfixed from R33CaptureArxiv §7 #3):** the row's source cell and entry `:3` cite the **unpinned** URL `https://arxiv.org/abs/2412.05579` while the anchor/entry claim v2 and the recheck line names the pin `arXiv 2412.05579v2`. `R33C1KillRule.md:19` records the same unpinned mapping. Recommend the `/v2` URL (the bytes this quote resolves against); as of the capture this is the same document (v2 is the only version), so it is a pin-hygiene defect, not a content falsification.

### 3.3 Abstract — quoted sentence resolves byte-exact at `:124`; 20 words
- The blockquote spans `:123` (`<blockquote class="abstract mathjax">`)–`:125` (`</blockquote>`); body is `:124`.
- The quoted sentence resolves byte-exact at `:124` (index 532 in the line) and also at `:30` (og:description) and `:41` (citation_abstract):
  `This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.` — **20 words** ✓, contiguous, entity-free.
- Five perspective names all appear in that order in `:124` ✓ (row scope cell "Functionality, Methodology, Applications, Meta-evaluation, Limitations" ✓).

### 3.4 Comments — `:131` ✓ (R33CaptureArxiv's `:130` is the label cell)
- `:130` = label `Comments:`; `:131` = value `<td class="tablecell comments mathjax">60 pages, comprehensive and continuously updated</td>` — **6 words** ✓, byte-identical to the row's quote. R33CaptureArxiv §6 wrote "line 130" (that line is the label; the value is 131) — minor off-by-one.

### 3.5 Tier B evidence (preprint)
- `grep -ci 'journal'` = 0, `grep -ci 'doi:'` = 0, `grep -c 'journal-ref'` = 0 over the whole capture → no journal reference / DOI at open time ✓. Scope cell "for the preprint's own text; tier B because it is a preprint at the time of opening" is grounded.

## 4. Spelling claims — falsified as stated (the one substantive content defect)

Capture-wide case-sensitive counts:

| string | hits | where |
|---|---|---|
| `LLMs-as-Judges` (cap J) | 17 | title 11× (4/21/23/33/41/98/116/117/177/243/248) + `:30` og 2 + `:41` citation meta 2 + `:124` abstract body 2 |
| `LLMs-as-judges` (low j) | 9 | `:30` 3, `:41` 3, `:124` 3 |

Inside the **abstract body `:124`** (bytes 12721–14367), the two cap-J hits are:
- `@13517` — prose: `…providing a systematic definition of LLMs-as-Judges and introduce their functionality…` (sentence: "We begin by providing a systematic definition of LLMs-as-Judges and introduce their functionality …");
- `@14261` — inside the resource-list link `href="https://github.com/CSHaitao/Awesome-LLMs-as-Judges"` (rendered link text is "this https URL", so not visible prose).

The three low-j hits are the quoted-label `'LLMs-as-judges'` (@13057), the quoted 20-word sentence (@13340), and the closing "development and application of LLMs-as-judges" (@14111).

Therefore:
- **S104 row teaches cell** — "the survey uses its own spelling, `LLMs-as-Judges` in the title and `LLMs-as-judges` in the abstract" — is **over-broad/false as stated**: the abstract body does *not* uniformly use the lowercase form; it writes `LLMs-as-Judges` (cap J) once in visible prose ("definition of LLMs-as-Judges") and once in the URL. "The survey uses its own spelling" (singular per location) implies a clean two-location split the source does not have.
- **Entry `:116-117`** — "the title capitalises `Judges` (`LLMs-as-Judges`, `…-abs.html:41`), while the abstract body writes `LLMs-as-judges` lowercase (`:124`)" — same overreach. The claimed dichotomy is not exclusive. The statement "The capitalisation differs between the two source locations and neither form is a transcription error" is right that both forms exist in the source; wrong in asserting the abstract is lowercase-only.
- R33EntryPatch §5.2 item 8 records the same incomplete claim ("the abstract body has `LLMs-as-judges` (lowercase)").

Note the **visible** abstract is mixed but nearly lowercase: exactly one visible prose cap-J occurrence plus one non-rendered URL string; the title is exclusively cap-J. Smallest truthful repair: "the abstract body is (almost) all lowercase `LLMs-as-judges`, with one cap-J prose occurrence (`definition of LLMs-as-Judges`) and a cap-J URL".

## 5. Scope overreach / wording drift

- Row scope cell "…five-part structure for **LLM-as-a-judge** evaluation…": the source never writes `LLM-as-a-judge` (0 hits in capture; the source uses `LLMs-as-judges` / `LLMs-as-Judges`). This is a lane-side generic renaming, not a source quote — minor, but it sits next to the row's own spelling claim and should use the source's form.
- "five-part structure" for the source's "five key perspectives" is an acceptable paraphrase (the five names follow the colon); not a widening of content. The row correctly scopes with "for the preprint's own text".
- Entry `:109` still reads "**The field's own survey** is …" — the field-canonical overclaim R33SurveyScope attacked persists in the **entry** (its table showed it in the landed teaches cell; the current row `:119` teaches cell does **not** contain "the field's own" — it reads "the survey uses its own spelling…"). So R33SurveyScope's "landed teaches still overclaims" row is stale vs current bytes; the issue lives only in the entry at `:109`.

## 6. Gate boundaries / out-of-scope

- No git/jj/index inspection (off-limits); no live network re-fetch (R33SurveyScope's "no v3 exists, latest=v2 at 2026-10-25T17:27Z" claims are **not re-verified** here — reported as [INFERENCE] from that report, supported by the pinned capture showing v2 as the served version).
- Not checked (other seats): `plans/adoption_check.py`, `plans/round33_c1_verify.py`, `plans/sources_adopt.py`; census/index rows; S103/Toolathlon row; SWE-bench capture manifest (flagged by R33CaptureArxiv §8.7).
- No tool installs; no edits beyond this report.

## 7. Findings

| # | finding | verdict |
|---|---|---|
| 1 | S104 row's version/date claims (v1 7 Dec 2024, v2 10 Dec 2024) byte-match capture `:115`/`:164-167`/`:41` | **verified** |
| 2 | S104 row's title claim (`LLMs-as-Judges: …`, 8 words) resolves at `:116` (h1) and `:41` (citation_title) | **verified** (pointer `:41` resolves, `:116` canonical) |
| 3 | S104 row's abstract quote resolves byte-exact at `:124`, 20 words; five perspectives in order | **verified** |
| 4 | Comments quote `60 pages, comprehensive and continuously updated` at `:131`, 6 words | **verified** |
| 5 | Tier B (preprint, no journal/DOI in capture) | **verified** |
| 6 | **Spelling claim** "title LLP-J, abstract lowercase" is over-broad: abstract body `:124` contains cap-J prose `definition of LLMs-as-Judges` + cap-J URL; `LLMs-as-judges` lowercase is dominant but not exclusive | **caught (claim falsified as stated)** |
| 7 | Row teaches "the survey uses its own spelling, … in the abstract" — same non-exclusivity problem | **caught (over-broad)** |
| 8 | Source cell cites unpinned `…/abs/2412.05579` while claiming v2 (R33CaptureArxiv §7 #3 recommendation not adopted) | **unfixed pin-hygiene defect** |
| 9 | R33CaptureArxiv §3 "Line 117, the Title: line (offset 11299)" — line tag off by one (offset 11299 = `:116`); §6 comments "line 130" is the label cell (value `:131`); history lines cited as 166–168 (actual 164–167) | **report line-pointer errors** |
| 10 | R33SurveyScope's "landed teaches still says 'the field's own'" is stale vs current row `:119`; the overclaim persists only in entry `:109` | **discrepancy noted** |

## 8. Artifact paths

- Report (this file): `.ufo/waves/round-33/falsify/R33FArxivScope.md`
- Capture: `.ufo/waves/round-33/assimilation/captures/arxiv-2412.05579v2-abs.html` (digest verified)
- Landed row: `corpus/SOURCES.md:119`
- Entry: `corpus/knowledge/benchmark-grader-semantics.md:107-124` (`:3`, `:5`, `:25`, `:28`, `:38`)

**VERDICT: row-repairs** — version/date/title/abstract/comments claims all verify against the capture; the spelling claim (and its entry echo) overstates exclusivity; the URL pin recommendation remains unadopted; build-report line pointers have off-by-one tags.

## L1 integration correction

The S104 source URL, entry `source:` line, `url-map.json`, `append-rows.md`, and landed registry row now use the version-pinned `/abs/2412.05579v2` URL. A direct fetch from that exact URL was byte-identical to the committed HTML capture (sha256 `44195c5f…`). The entry/row spelling statements were narrowed: the title uses `LLMs-as-Judges`, the quoted abstract phrase uses `LLMs-as-judges`, and the abstract also contains a title-case occurrence; no exclusivity is claimed. The version-pin and capitalization findings above describe the pre-correction snapshot.

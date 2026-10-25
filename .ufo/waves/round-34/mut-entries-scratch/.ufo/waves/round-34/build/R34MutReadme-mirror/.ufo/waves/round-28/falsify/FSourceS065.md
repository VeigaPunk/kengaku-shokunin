# FSourceS065 — source-row falsification: Python JSON non-finite docs (S065); adjacent S066 access check

Seat: `KengakuR28.FSourceS065` (scout; calibration axis; author-side falsifier, not outside closure).
Date: 2026-10-21. Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Read-only over production. My only writes are this report and scratch under
`.ufo/waves/round-28/scratch/KengakuR28.FSourceS065/`. No upstream code execution/import/eval, no
benchmark-site contact, no DOI/Wayback request; one `docs.python.org` GET for S065 (see below).
No installs or updates. No subagent dispatch.

Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (matches the pinned value).
Canonical candidate: `corpus/knowledge/webarena-task-spec-audit.md` — **not admitted** (file absent;
the round-28 Gate defers it). I claim no candidate admission and no candidate PASS. Candidate writer is
`KengakuR28`, not this seat.

## Axes

- **Calibration (primary):** exact source metadata for S065 — canonical URL, access date, page version,
  located quote, anchor, word count, tier/scope/teaches, used-by, and the append-only knowledge correction.
- **Coverage/constructs (secondary, no score claim):** S065 supplies the Python-side authority for the
  extraction-policy E4 statement; it does not extend the C1 WebArena candidate.

## Row as recorded

Gate row `corpus/lessons/round-28.md:44` records URL
`https://docs.python.org/3/library/json.html#infinite-and-nan-number-values`, accessed `2026-10-21`,
and the quote “this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON
number literal values” (18 words) — Python3.15.1, Infinite and NaN Number Values; “supplies Python-side
authority, not RFC content. OpenS059 and L1 reopened docs.”

Registry row `corpus/SOURCES.md:87` (same URL; scope “documented default Python acceptance of NaN and
infinities, not the RFC rule”; anchor “Python3.15.1, Infinite and NaN Number Values paragraph and examples;
opened2026-10-21”; teaches “default Python JSON accepts and emits NaN and infinities; … distinct from
S059's RFC-side restriction”; `mined`, `on-release`, used-by lesson + `extraction-policy-comparison.md`).

The lesson's second mention, `corpus/lessons/round-28.md:59`: “S065 supplies explicit Python-side
authority.” The knowledge mention, `corpus/knowledge/extraction-policy-comparison.md:130`, is inside the
appended errata section.

## Independent re-open (S065)

Command (scratch only):

`curl -sS -L --max-time 30 -D headers.txt -o pyjson-live.html https://docs.python.org/3/library/json.html`

Observed 2026-10-21T14:31:33Z (-03 local 11:31):

| item | observed |
|---|---|
| HTTP | `HTTP/2 200`, `content-type: text/html`, `content-length: 115104` |
| `last-modified` | Wed, 21 Oct 2026 13:04:29 GMT |
| body sha256 | `7197009d47b8a44ce5a8c22b8c70ab5f754fd479cb30268284b0da84a9d1f8fb` |
| comparison | byte-identical to `scratch/OpenS059/pyjson.html` (captured 2026-10-21 10:57:27 -03 = 13:57Z), same sha256 |
| `<title>` | `json — JSON encoder and decoder — Python 3.15.1 documentation` |
| `<link rel="canonical">` | `https://docs.python.org/3/library/json.html` |
| section | `id="infinite-and-nan-number-values"`; `<h3>Infinite and NaN Number Values` at html:877; paragraph 878–880 |

This confirms the row's **canonical URL** (page canonical + section fragment), **access date**
2026-10-21, and **version** Python 3.15.1. The `/3/` URL is a moving alias, but the recorded access date
and version make the snapshot identity explicit; today's live page is the same bytes as the recorded
capture, not a later drift.

Located paragraph (rendered text; html:878–880). The preceding sentence (14 words):
“The RFC does not permit the representation of infinite or NaN number values.” The quoted sentence
(22 words): “Despite that, by default, this module accepts and outputs Infinity, -Infinity, and NaN as if
they were valid JSON number literal values.”

Gate quote: `this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON
number literal values` — contiguous rendered text, **18 words** (≤25). It is a mid-sentence fragment:
the source sentence begins `Despite that, by default,` and the full sentence is **22 words** (still ≤25).

## Narrow tier/scope/teaches check

- **Tier/kind:** `docs`/A. Python's official docs are tier A for the module's documented behavior; the row
  does not use them for the RFC's rule. Correct.
- **Scope:** “documented default Python acceptance of NaN and infinities, not the RFC rule.” The page's
  paragraph says the RFC does not permit these values and that *by default* this module accepts/outputs
  them. The row narrows to the Python-side behavior. Accurate and narrow.
- **Teaches:** “default Python JSON accepts and emits NaN and infinities; … distinct from S059's RFC-side
  restriction.” The source examples show both directions (`json.dumps(float('-inf'))` → `'-Infinity'`;
  `json.loads('NaN')` → `nan`). “emits” = “outputs”; accurate. S059's row is the RFC-side prohibition.
- **Used-by:** `corpus/lessons/round-28.md` and `corpus/knowledge/extraction-policy-comparison.md` both
  contain literal S065 mentions (lesson:44,59; knowledge:130). Status `mined`, recheck `on-release` are
  consistent. S065 is outside the frozen13 C2 population, so it adds no C2 reference edge.
- **Final draft use:** the candidate source header (`draft:1`) cites S061/S062/S063 only. The draft
  contains no S065/S066 mention and no NaN/Infinity/non-finite claim (a case-insensitive grep hit is the
  substring “nan” inside “provenance”, not a source term). The row's use is the calibration knowledge and
  the lesson, exactly as its used-by lists; there is no missing draft citation.
- **Old-knowledge correction:** `corpus/knowledge/extraction-policy-comparison.md` changed by **+24 lines,
  0 deletions**; the original E4 sentence at :52–53 (“Python also accepts NaN/Infinity by default, unlike
  RFC8259 §6 (S059)”) is unchanged. The appended errata (:116–138) adds S065 as the Python-side authority
  and explicitly keeps S059 to the RFC-side prohibition. Append-only, marked as errata, and accurate. It
  adds no new reference edge to a frozen13 ID (S065 is outside the frozen13; S059 was already cited).

## Findings

### F1 — second-seat evidence: word count and html range are wrong (minor, calibration; not a row-truth failure)

`build/OpenS059.md` quotes the **full 22-word** sentence but reports “(19 words)”. It also gives
`html:876–879`; the quoted sentence starts on line 879 and ends on line 880, so the range misses its last
line (the paragraph spans 878–880; the section heading is at 877; the Gate fragment spans 879–880). The Gate's own quote is 18 words, so
the ≤25 rule is met either way, and the row's quote/anchor are exact. This is a Q10 number/location erratum
in the source-opening record, not a false claim in S065. Recommended: correct `build/OpenS059.md` to
22 words and html:879–880 for the quoted sentence (878–880 for the paragraph); no production source-row
change is forced by this alone.

### F2 — Gate fragment drops the qualifier the teaches relies on (minor, optional)

The Gate quote begins after `Despite that, by default,`; the row's teaches says “default”. The quote is
verbatim and the anchor paragraph contains the qualifier, so this is not a widening (the paraphrase is
narrower than the source sentence). Still, the full 22-word sentence is within the ≤25-word cap and would
make the quote self-contained: `Despite that, by default, this module accepts and outputs Infinity,
-Infinity, and NaN as if they were valid JSON number literal values`. Optional presentation fix; no truth
change.

### F3 — same-page disclosure for S052 (minor, optional)

S065's URL is the same base page as S052's (`docs.python.org/3/library/json.html`, different section
anchors). `corpus/SOURCES.md:111` calls S064–S066 “scope/anchor extensions, not3 new publications”, which
declares this at cohort level; the S065 row/Gate does not name S052. A one-line “extends S052's page
anchor” note would match the lane's duplicate-URL census convention. No C2 effect (S065 is outside the
frozen13).

### F4 — adjacent S066 check (not my primary scope; FSourceS066 owns the full audit)

No live DOI/Wayback call was made. The local archived PDF
`scratch/OpenS038/wb20261004.pdf` has sha256
`fc935f40a6f58cb7fea9407490a768fd63078eaf46ccd3b40b260d109de82e8c`, matching the lesson; its SHA-1
base32 is `GWYEXRXGLWELYZ5D4M3HDN4ZA4K6VJJS`, matching the capture digest claimed in
`build/OpenS038.md`; `pdfinfo` gives 5 pages, the expected title/DOI and ModDate
`Sun Oct 4 16:02:46 2026 -03` (the capture is `20261004190246Z`). The access limits are explicit:
DOI/publisher curl and headless Chromium returned 429; the opened artifact is a 2026-10-04 Internet
Archive capture, and the live WebFetch read is disclosed as possibly cached.

The S066 **Gate** row is exact: quote “the proposed methods assume that sensitivity and specificity are
known exactly” = **11 words** (≤25), located in the Discussion at p.1677 (wb.txt page header 1677 at :217,
DISCUSSION at :227, sentence at :243–245, CONCLUSION at :256). The PDF text layer renders `speciﬁcity`
with the fi ligature and `ex-\nactly` across the line break; the quoted words are the rendered words.

One adjacent registry defect: `corpus/SOURCES.md:88` gives the anchor as “Introduction/Methods p.1675 and
Conclusion p.1677” but omits **Discussion p.1677**, the section of the quoted sentence. The lesson Gate
row (`round-28.md:45`) and the attribution-knowledge errata
(`corpus/knowledge/attribution-interval-calibration.md:195`) both correctly say Discussion p.1677.
Recommended: add Discussion p.1677 to the registry anchor before this new row is admitted; this is
metadata exactness, not a change to S066's truth or scope. FSourceS066 owns the complete S066 audit.

## Remaining unknowns / limits

- The 2026-10-04 Wayback CDX record itself is not stored locally; the local PDF's SHA-1 base32 matches the
  report's claimed digest, but I did not query the archive (per the instruction not to call the cached
  copy live). The PDF header/footer and ModDate corroborate the capture date.
- The docs page is a moving `/3/` alias; a future Python release can change it. The row's `on-release`
  recheck is the right control. Today's page is byte-identical to the recorded capture.
- I did not execute Python's `json` module or import upstream code; the S065 check is documentation text
  only. No browser actions, no benchmark sites, no credentials.

## Verdict

**VERDICT: PARTIAL (scoped, calibration).**

The S065 Gate/registry rows' substantive cells are source-exact: canonical URL, access date 2026-10-21,
Python 3.15.1, section `Infinite and NaN Number Values`, the 18-word quote (≤25), tier/scope/teaches,
used-by, and the append-only extraction-policy errata all check out; the frozen candidate does not use
S065 and need not. The partial is for the source-opening record and quote self-containment: the
second-seat report's word count is wrong (22, not 19) and its html range misses line 880, and the Gate's
18-word fragment omits the `by default` qualifier that the row's teaches depends on (the full 22-word
sentence is still within the cap). Adjacent S066's Gate row is exact and its access limitations are
explicit; its registry anchor omits Discussion p.1677 and is flagged for L1/FSourceS066. None of these
findings reverses a truth, scope, or admission boundary; L1 resolves them.

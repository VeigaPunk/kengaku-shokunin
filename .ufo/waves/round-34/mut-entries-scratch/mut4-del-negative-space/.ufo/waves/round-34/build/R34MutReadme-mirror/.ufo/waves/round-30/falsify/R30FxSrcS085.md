# R30FxSrcS085 — S085 re-opened independently (falsify wave, round 30 / hyaku run 6)

- **Seat:** L1Kengaku30.R30FxSrcS085-3 (leaf; no dispatch; this file is the only lane write)
- **Candidate under test:** `corpus/knowledge/contamination-transparency-card.md` — its `source: S085` line,
  against `corpus/SOURCES.md` row `| S085 |` (registry line 111) and `corpus/lessons/round-30.md` line 52.
- **Access date:** 2026-10-25. **Scratch:** `/tmp/r30fx-S085-3/` (nothing else in the lane touched).
- **Question:** are the two Chinese spans on p.32 (printed 27) and p.34 (printed 29) really there, verbatim,
  with the counts the row prints — and are those printed labels derivable from the footer?

**Answer in one line:** both spans are located verbatim at the claimed pages with the claimed counts; the
printed labels are **not** derivable from the footer (it is genuinely broken) but are derivable from the
document by two other routes; and the entry's own prescribed recheck command fails today on span A for a
reason that is the entry's, not the source's (§6, R-1).

## 1. Capture identity (my own fetch, before reading any build report)

| field | value |
|---|---|
| URL | `https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711534708580017.pdf` |
| fetch | `curl -sSL` → `http_code=200 size=1949572 ctype=application/pdf`, first attempt, no UA spoof |
| **sha256** | **`e551e2e0956c314507ab240b3ca19ce47aed88640a98e6c316bd4efc6bbc131c`** |
| **bytes** | **`1949572`** |
| refetch | second independent `curl` → same 1949572 B, sha256 identical ⇒ representation stable within the day |
| served headers | `ETag: "1dbf84-61cf4aaac5a9e"`, `Last-Modified: Thu, 11 Jul 2024 08:37:01 GMT` |
| `pdfinfo` | PDF 1.6, **52 pages**, A4 595.32×841.92 pt, `Acrobat PDFMaker 17` / `Adobe PDF Library 17.11.238`, `CreationDate: 2024-07-10 22:03:23 -03`, `Encrypted: yes (print:yes copy:no …)` |
| cover (pdf 1) | `大模型基准测试体系研究报告` / `(2024 年)` / `中国信息通信研究院人工智能研究所` / `2024年6月` — no document number on the cover |
| text layer | `pdftotext -enc UTF-8` whole file → `74975` bytes, `2604` lines, sha256 `bc6a20d6216b453075cac294281754513c8c536aa1e356a0c328925cfcce1ae4` |
| span-search form | newlines deleted (`str.replace("\n","")`) → `31898` chars, sha256 `d377d909c02256e7e581c6903e8a8988a36d16b73d5002c2cafaaf97596c0b90` |

No text layer exists in the raw `.pdf` bytes (FlateDecode page streams), so every quote test below is
against the extraction text — same conclusion the source seat reached, reached here independently.

## 2. Span A — `“方升”测试体系提出自适应动态测试（Adaptive Dynamic Testing，ADT）方法对大模型进行评测`

| property | measured |
|---|---|
| **verbatim** | `“方升”测试体系提出自适应动态测试（Adaptive Dynamic Testing，ADT）方法对大模型进行评测` |
| **location** | PDF page **32** = printed **27**; extraction lines **1011–1012**, the span starting at the end of line **1010** (`…“刷榜”等问题，“方升”` \| `测试体系提出…（Adaptive Dynamic Testing，ADT）方` \| `法对大模型进行评测，以保证…`) |
| **whitespace tokens** | **3** — `“方升”测试体系提出自适应动态测试（Adaptive` / `Dynamic` / `Testing，ADT）方法对大模型进行评测` |
| **CJK ideographs** | **25** (incl. `方升`); 57 characters total; sha1 of the span `720c5b91031bd17b79134a4d08383a476ec0a2c4` |
| **occurrences in the 52-page document** | exactly **1** (whole-document sweep) |
| **quotation marks** | U+201C … U+201D, drawn by the report itself: page content stream emits `(\223)Tj` … `(\224)Tj` (WinAnsi 0x93/0x94) around the glyph run `方升`. Not added by the lane. |
| **byte-contiguous?** | **No.** The run crosses three typeset lines; it is a byte substring only after newline deletion (offset `19654` in the de-wrapped text, 1 occurrence). |
| **locatedness** | **LOCATED** |

Boundary check on the de-wrapped text (proves nothing was omitted inside the span):
`…“刷榜”等问题，` ▸ *span* ◂ `，以保证大模型基准测试能高质、高准、高效的完成。如图 12 所示，…`

Match against the row as written: the registry row's quoted bytes are an **exact character-run substring**
of the document after newline deletion, not a paraphrase — proven with the round's own gate (§6), which is a
literal `in` test with no fuzzy or whitespace-insensitive matching.

## 3. Span B — `采用动态方式构建，保证每次参与测试题目的都不相同`

| property | measured |
|---|---|
| **verbatim** | `采用动态方式构建，保证每次参与测试题目的都不相同` |
| **location** | PDF page **34** = printed **29**; extraction **line 1050**, whole span on one line, §`2.动态更新，测试题库实时化`, inside `…底层测试数据库采用动态方式构建，保证每次参与测试题目的都不相同，以解决存在题目封闭、考题过时、模型作弊等问题。` |
| **whitespace tokens** | **1** |
| **CJK ideographs** | **23**; 24 characters total (the 24th is `，`); sha1 `93fd7d25661dd83fbe0d749cd8daa042cba1e28e` |
| **occurrences** | exactly **1** in the 52-page document |
| **byte-contiguous?** | **Yes** — byte substring of a single extraction line (offset `20462` de-wrapped, and it also locates in the raw newline-containing extraction: gate `ok` on both artifacts) |
| **locatedness** | **LOCATED** |

Both counts in the landed row are right: `3 whitespace tokens` (A) and `1 whitespace token, 23 CJK characters`
(B). The row does not understate or overstate either span, and neither spans a page break.

## 4. Printed page labels — the footer is broken; the labels are still derivable

**Verdict on the assigned question: the printed labels are NOT derivable from the footer.**

The footer is a `/Subtype /Footer` pagination artifact with per-character clipped text runs. On pdf page 32:

```
/Artifact <</Attached [/Bottom ]/BBox [290.328 53.757 523.734 66.12 ]/Subtype /Footer /Type /Pagination >>BDC
BT /TT0 1 Tf 9 0 0 9 505.32 56.76 Tm ( )Tj ET
q 295.44 49.32 4.559 15.6 re W n
BT 9 0 0 9 295.44 56.52 Tm (2)Tj ET          <- the only digit drawn
Q
q 295.44 49.32 4.559 15.6 re W n
BT 9 0 0 9 304.44 56.52 Tm ( )Tj ET          <- placed at x=304.44, i.e. OUTSIDE its own 4.559 pt clip
Q
EMC
```

Glyph trace of the page's bottom band (`y>760`, top-down coordinates): exactly three glyphs —
`' '` at x=505.32, **`'2'`** at x=295.44 (9 pt TimesNewRomanPSMT), `' '` at x=304.44. A 900 dpi raster of
the strip `x 275–325, y 772–800` shows one glyph: `2`. So the units digit is not a space that renders
blank in one mode and not the other — **it is absent from the content stream and absent from the render.**

Across all 52 pages (`/Subtype /Footer` run dump, per page):

| printed range | pdf pages | footer digits present |
|---|---|---|
| 1–9 | 6–14 | **complete** (`1`…`9`) — the whole label |
| 10–19 | 15–24 | `1` only |
| 20–29 | 25–34 | `2` only |
| 30–39 | 35–44 | `3` only |
| 40–47 | 45–52 | `4` only |

There is **no `/PageLabels`** entry in the PDF catalog (`xref_get_key(catalog,"PageLabels") → null`,
`doc.get_page_labels() → []`), so the file carries no machine-readable printed-page mapping either.

**How the labels are then derivable (two independent routes, both measured):**

1. **Complete footers on printed 1–9.** pdf 6 carries `一、大模型基准测试发展概述` (TOC: page 1) and its footer
   reads `1`; pdf 14's footer reads `9` (TOC: 一（三） at 9). Nine complete labels pin
   `printed = pdf_page − 5`. Under that rule pdf 32 → 27 and pdf 34 → 29, and the surviving tens digit
   on each (`2`) is consistent with it.
2. **TOC titles + body cross-references** (footers not used at all): TOC `（二）“方升”自适应动态测试方法 … 27`
   and `图 12 自适应动态测试方法原理图 … 27` — pdf 32 carries **both** that heading and a caption whose
   title is `自适应动态测试方法原理图`. For printed 29: TOC `图 13 大模型基准测试标签体系 … 28` (pdf 33 carries
   that caption) and TOC `（三）“方升”大模型测试体系实践 … 30` (pdf 35 carries that heading); pdf 34 is the
   only page strictly between printed 28 and 30 under consecutive pagination, and `34 − 5 = 29`.

**A second defect found while doing this, and one the row should know about.** Figure-caption numerals
`图 11`–`图 14` are themselves corrupted in the same way and **collide with `图 1`–`图 4`**: pdf 29 prints
`图 1 “方升”大模型基准测试体系` (TOC: 图 11, p.24), pdf 32 prints `图 2 自适应动态测试方法原理图` (图 12),
pdf 33 prints `图 3 …标签体系` (图 13), pdf 36 prints `图 4 “方升”大模型首轮试评测模式` (图 14). Glyph evidence
on pdf 32's caption: the numeral run is `U+0020`, `'2'`, `U+0020` at 6 pt pitch — the leading `1` slot holds a
space glyph. By contrast `图15` (pdf 38) is complete, and the **body** cross-references are intact
(`完成。如图 12 所示，…` survives `pdftotext -raw`). Consequence for the lane: a citation must anchor on the
caption *title* or the TOC, never on the caption numeral, for 图 11–14.

## 5. What the landed bytes assert vs. what the artifact says

| assertion (entry line 5 / SOURCES line 111 / lessons line 52) | measured | verdict |
|---|---|---|
| span A verbatim, p.32 (printed 27) | located, unique, page correct | **holds** |
| span A = 3 whitespace tokens; fullwidth quotes are the report's own | 3 tokens; U+201C/U+201D present in the report's own run | **holds** |
| span B verbatim, p.34 (printed 29) | located, unique, byte-contiguous, page correct | **holds** |
| span B = 1 token / 23 CJK characters | 1 token / 23 ideographs (24 chars with `，`) | **holds** |
| fetch identity `1949572 B sha256 e551e2e0…` | identical, twice | **holds** |
| rationale: “no document number” | cover carries no number | **holds** |

Two precision notes, neither of which changes a count:

- `“fullwidth quotes”` is a typographic description: U+201C/U+201D have East_Asian_Width **Ambiguous**, not
  `F`. The substantive half of the clause (the report wrote them, the lane did not) is verified.
- The registry title cell writes `（2024年）`; the cover and running header print `（2024 年）` (with a space).
  It is a title cell, not a quoted span, so it is not a quote defect — recorded only so a future reader does
  not treat the cell as verbatim.

## 6. R-1 — the entry's own recheck recipe fails on span A today (the sharpest finding)

The entry's `recheck:` line (and lessons line 38) prescribes: re-fetch, re-locate each span in fresh
captures, and **re-run `python3 plans/sources_adopt.py --quote-file <admission rows> --artifact <capture>`**.
Running exactly that, with the real registry row and my own capture, **read-only**:

```
$ python3 plans/sources_adopt.py --quote-file s085row.txt --artifact mine_default.txt     # pdftotext output
QUOTE rows=1 spans=2 located=1 found=1 overlong=0 absent=1 malformed=0 cap=25 artifacts=mine_default.txt
  REFUSED S085 absent words=3 quote="“方升”测试体系提出自适应动态测试（Adaptive Dynamic Testing，ADT）方法对大模型进行评测"
  ok S085 words=1 at mine_default.txt quote="采用动态方式构建，保证每次参与测试题目的都不相同"
exit=7
```

Same row, same gate, artifact with newlines deleted:

```
$ python3 plans/sources_adopt.py --quote-file s085row.txt --artifact mine_dewrapped.txt
QUOTE rows=1 spans=2 located=2 found=2 overlong=0 absent=0 malformed=0 cap=25 artifacts=mine_dewrapped.txt
  ok S085 words=3 at mine_dewrapped.txt quote="“方升”测试体系提出自适应动态测试（Adaptive Dynamic Testing，ADT）方法对大模型进行评测"
  ok S085 words=1 at mine_dewrapped.txt quote="采用动态方式构建，保证每次参与测试题目的都不相同"
exit=0
```

Mechanism, read off the gate: `normalize_text()` maps CRLF/CR to LF only, and `locates()` is a literal
substring test on that normalized text — so a span cut across a **CJK hard wrap** can never locate against a
plain poppler capture. The source seat's own declared canonical form for this PDF was “delete `\n`, collapse
whitespace runs to one space” (`R30SrcS085.md` §2.2); the gate implements CRLF normalization, not that form.
Exit 7 is a *refusal*, not an error, so a rechecker following the entry literally will record S085 as
`absent` in 2027-04 while the bytes are present. Nothing in C1's or C3's frozen predicate is violated by this
(the predicate never runs the gate over the admitted rows) — but the entry's own `recheck:` action, as
written, cannot pass, and the fix is either a de-wrapped capture pinned in the recipe or CRLF→unwrap
normalization in the gate. **R-1: recheck recipe vs gate normalizer mismatch, reproducible, exit 7 vs 0.**

**R-2 (disclosure asymmetry, minor).** S086's row explicitly discloses that its caveat spans extraction
lines 78–81 and is “reported as located but not byte-contiguous”. S085 span A has exactly the same property
(three lines, 1010–1012) and the row does not say so; the only place it is stated is the source seat's
report. This is the same gap R-1 turns into a refusal, so the two should be repaired together.

## 7. Comparison with the source seat's report (`build/R30SrcS085.md`) — after my capture

Captured first, compared second. Agreement: sha256 `e551e2e0…131c`, 1949572 B, ETag/Last-Modified, 52 pages,
the `/tmp` extraction byte-identical to mine (`cmp` clean, sha256 `bc6a20d6…`), both spans' page attributions,
`(a1)` = 3 tokens / 25 CJK, span B = 1 token / 23 CJK, “each quote occurs exactly once”, and “the footer is a
broken field — do not trust the footer”.

Named disagreements / corrections:

- **D1 — mechanism of the Latin spaces (§2.3 of that report).** It says “poppler pads Latin runs in CJK text”
  and cites both `如图 12 所示` and `（Adaptive Dynamic Testing，ADT）` as poppler artefacts. Measured: the two
  spaces in `Adaptive Dynamic Testing` are **real U+0020 glyphs in the page content stream** (glyph trace:
  `(' ',3,337.32)` and `(' ',3,391.32)` at 14 pt; stream contains `( )-17 (Dyn)`), while poppler **`-raw`**
  *drops* them (`（AdaptiveDynamicTesting，ADT）`), and `如图 12 所示` survives `-raw` unchanged. So nothing is
  padded. This matters in the lane's favour: span A's `3 whitespace tokens` is a property of the document,
  not of the extractor — but the report's stated reason for it is wrong, and its parenthetical example is
  half wrong.
- **D2 — footer description.** “the remaining glyphs being absent from both the text layer and the render” is
  correct; I add the precision that the *trailing* `( )Tj` run sits at x=304.44 **outside its own
  `295.44 … 4.559` clip**, so the footer field draws exactly one digit and one clipped space, and that
  `/PageLabels` is absent, and that footers on printed 1–9 are complete (which is what actually pins the −5
  offset; the report's “body start” route is right but states it as a single anchor when there are nine).
- **D3 — page count.** 52 pages (`pdfinfo`, pymupdf). The sibling falsify report `falsify/R30FxC3CLI.md:202`
  writes “PDF page 32 of **53**”. 53 is wrong by one; 32 is still the right page.
- **D4 — “four dimensions” §5 anchor page.** Not my span, so not adjudicated here; recorded only because it
  is the same document and a later reader may pair it with my capture.

Also observed, outside my span, consistent with `falsify/R30FxC3CLI.md` (not a finding of mine): the entry's
S086 source line says `23 CJK characters` and `lines 78-81`, while `lessons/round-30.md` row S086 says
`30 CJK chars` and `lines 80-81`. One of those two lane artefacts is wrong; S085's own `23` is correct
(measured, §3), so the “23 copied from S085” suspicion in the sibling report is plausible but not mine to rule on.

## 8. Remaining unknowns

- Whether CAICT will serve different bytes after today is unverified; this report pins the 2026-10-25
  representation (sha256 + ETag).
- The cause of the digit loss (PDFMaker/Word field composition vs font subsetting) is not established; only
  the observable is (one digit drawn, units digit absent, captions 11–14 colliding with 1–4).
- Whether the other five rows' spans would also be refused by the gate on plain captures (R-1's blast radius)
  was not measured here — one `--quote-file` run per source, per its own seat, would settle it.

## 9. Tooling

- Nothing installed into the host; `pacman` untouched (host-wide pause respected). Used host `curl`,
  `pdftotext`/`pdfinfo`, `python3`.
- One scratch-only install for glyph-level forensics: `uv venv /tmp/r30fx-S085-3/.venv` +
  `uv pip install pymupdf` → **PyMuPDF 1.28.5** (via `fitz`). Reason: read the footer/caption content-stream
  operators, per-glyph unicode and clip rects, which `pdftotext` cannot show. Disposable, `/tmp` only.
- Commands that produced every number in this report are in `/tmp/r30fx-S085-3/` (`mine_default.txt`,
  `mine_dewrapped.txt`, `s085row.txt`, `footer_p32.png`); they regenerate from the pinned sha256.

## 10. Verdict

Both of S085's quoted spans exist, verbatim and uniquely, on the pages the entry names, with the word/CJK
counts the entry prints and the printed-page labels the entry prints; the footer cannot be the source of
those labels, and the entry never claims it is.

VERDICT: PASS — corpus/knowledge/contamination-transparency-card.md, for its `source: S085` line (spans located on pdf p.32 = printed 27 and pdf p.34 = printed 29, 3 tokens / 1 token 23 CJK as written); scope note: R-1 (the row's recheck command returns exit 7 against a plain capture) and R-2 (missing non-contiguity note) are recorded as defects of the entry's recheck recipe and disclosure, not of the quoted bytes.

# R30FxSrcS086 — independent re-read of source S086 (round 30 falsify, hyaku run 6)

- **Seat:** L1Kengaku30.R30FxSrcS086-3 (leaf; no subagents, no lane writes outside this file; scratch `/tmp/r30fx-s086/`)
- **Access date:** 2026-10-25
- **Target under test:** the `source: S086` line of `corpus/knowledge/contamination-transparency-card.md` (line 6)
  and the `S086` row of `corpus/SOURCES.md` (line 112) — two asserted spans: the printed title and the Japanese caveat.
- **Method note:** capture, extraction and hashing were completed **before** any build-seat report was opened.
  The comparison against `.ufo/waves/round-30/build/R30SrcS086.md` is §6.
- **Candidate path:** `corpus/knowledge/contamination-transparency-card.md`

## 1. Capture identity (my own fetch, 2026-10-25 07:37–07:41 GMT)

| field | value |
|---|---|
| URL | `https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf` |
| local path | `/tmp/r30fx-s086/Q2-11.pdf` (scratch, outside the lane) |
| sha256 | `c3706aca80aa8aeee7fa39d3a5988f238a138c508c0ca5fe5c107c50d7feb303` |
| byte count | **371155** (`content-length: 371155`, on-disk `371155`) |
| pages | 6 (`file`: `PDF document, version 1.5, 6 page(s)`; `pdfinfo` Pages: 6) |
| `last-modified` | `Thu, 27 Feb 2025 16:49:21 GMT` |
| `etag` | `"5a9d3-62f2278c2cb47"` |
| PDF `/Title` | `Code LLM 事前学習時の評価データ混入への対策` |
| PDF `/Author` | 金山 博, 大湖 卓也, 村岡 雅康, 吉田 一星 |
| HTTP | `200`, `server: nginx`, `content-type: application/pdf`, no redirect |
| byte-identity cross-check | `cmp /tmp/r30-R30SrcS086/Q2-11.pdf /tmp/r30fx-s086/Q2-11.pdf` → **IDENTICAL** (the build seat's surviving scratch copy and my fresh fetch are the same bytes, not merely the same hash) |

Printed page labels (footers, all six pages): `― 797 ―` … `― 802 ―`, 1:1 with PDF pages 1–6, glyph U+2015.
**PDF page 1 = printed 797** — the entry's page assertion holds.

## 2. Extraction identities

| extract | command | bytes | sha256 |
|---|---|---|---|
| `p1.raw.txt` | `pdftotext -f 1 -l 1 Q2-11.pdf` | 4008 | `ef8e808646154dc5d86a5255c90ae9640fecd55d7575ff333972c9031bb85f04` |
| `p1.layout.txt` | `pdftotext -layout -f 1 -l 1 Q2-11.pdf` | 4687 | `655f834e10c06496cdf1e01c8c02b71e55f2f2d90617c3018d872382c0a9e68f` |
| `all.raw.txt` | `pdftotext -f 1 -l 6 Q2-11.pdf` | 30100 | `88b4201d81b2d867c7de66390b2bbeee120bc6779f83df10956362391160fc1f` |
| `p1.unwrapped.txt` | page 1, `"".join(l.rstrip() …)` | 3920 | `7af6144a8ac9b8fa3d347fb9785e2e9364d0b16a82fc4a340097b65af3581bde` |
| unwrapped (6 pp) | same join over `all.raw.txt` | 29076 | `887adab868aff11b4392f55bd3aed0eda642e55f7065cf26d40e890a632b8a9c` |
| `p1.fitz.txt` | PyMuPDF `page.get_text()` | 3979 | `611ca0382037bfda20fa612b0c7b2e1199e32423fd3d1b989045b9416f7ba1c6` |

Extractors: **poppler `pdftotext` 26.08.0** (host package) and **PyMuPDF 2.0** (ephemeral, `uv run --with pymupdf`; see §9).
Poppler emits one non-fatal warning per run — `Syntax Error (366527): insufficient arguments for Marked Content` — identical to the one the source seat recorded; no text dropped (6/6 pages, title/author/caveat/footer all present).

## 3. Span 1 — printed title

> `Code LLM 事前学習時の評価データ混入への対策`

| property | measured |
|---|---|
| chars | **26** (4 + space + 3 + space + 17 CJK) |
| whitespace tokens | **3** — `Code` / `LLM` / `事前学習時の評価データ混入への対策` |
| both separators | ASCII `U+0020`, present in the source bytes |
| location | PDF page 1 = printed **797**; `p1.raw.txt` line **3**; `p1.layout.txt` line **6**; unwrapped byte offset **72** (raw-file byte offset 74) |
| byte-substring status | **contiguous — no unwrapping needed.** 1 occurrence in `p1.raw.txt`, 1 in `p1.layout.txt`, 1 in `p1.unwrapped.txt`, 1 in `p1.fitz.txt` |
| metadata | identical to the PDF `/Title` value |
| **verdict** | **LOCATED**, and the entry's annotation "3 whitespace tokens, printed title, one contiguous run" is **true in all four extracts** |

The English subtitle carried in the registry's `source` cell (`Countermeasures against evaluation-data contamination in Code LLM pretraining`) is **not** in the PDF (`grep -c Countermeasures p1.raw.txt` → 0); it is a translation, and the registry row does not present it as printed text.

## 4. Span 2 — the Japanese caveat

> `一致したものを一律に混入とみなして除去することには疑問が残る`

| property | measured |
|---|---|
| chars | **30** (all CJK; no `。`, the quote is a clause of the sentence, not the sentence) |
| whitespace tokens | **1** after unwrapping; **2** on the raw text layer, because a line break falls inside the span |
| location | PDF page 1 = printed **797**; `p1.raw.txt` lines **80–81**; start at line 80 **col 13**, end at line 81 **col 21**; page-1 char offset 1498 (byte 3794); 6-page unwrapped byte offset **3715** |
| extraction split point | exactly one `\n` sits between `一律に` and `混入`, with **no other whitespace inserted**: the raw bytes are `…を一律に\n混入とみなして…` |
| source context | §2 関連研究, closing sentence of the Riddell-et-al. paragraph; lines 78–81 carry the full sentence `しかし、表 1 のように、…疑問が残る。` (85 chars, 3 tokens) |
| **verdict** | **LOCATED** — but **only after unwrapping** |

### 4.1 Substring status per artifact (this is the item's explicit question)

| artifact | `quote in text` | note |
|---|---|---|
| `p1.raw.txt` (poppler, default) | **False** | internal `\n` after `一律に` |
| `p1.layout.txt` (poppler, `-layout`) | **False** | same break, plus two-column padding spaces around the fragments |
| `p1.unwrapped.txt` (line breaks removed) | **True**, 1 occurrence | |
| `p1.fitz.txt` (PyMuPDF) | **False** raw; **True** after `text.replace("\n","")` | second engine, same geometry — the break is in the content stream, not a poppler layout heuristic |

**Answer to the item:** my extraction makes the caveat **need unwrapping**, not a byte substring. The title is a byte run. Two independent extractors agree.

### 4.2 Consequence under the lane's own gate (`plans/sources_adopt.py`)

The gate's `normalize_text` only normalises line-end *style* (`\r\n`, `\r` → `\n`); it does not remove `\n`, so `locates()` is a strict `needle in text`. Fed a 1-row / 2-span S086 quote file:

```
--artifact p1.raw.txt       -> QUOTE rows=1 spans=2 located=1 found=1 absent=1  REFUSED S086 absent (caveat)   exit=7
--artifact p1.layout.txt    -> QUOTE rows=1 spans=2 located=1 found=1 absent=1  REFUSED S086 absent (caveat)   exit=7
--artifact p1.unwrapped.txt -> QUOTE rows=1 spans=2 located=2 found=2 absent=0                                  exit=0
```

Both outcomes are the *correct* behaviour of a byte-substring gate on a line-wrapped quote; the refusal is a property of the artifact choice, and the entry discloses it ("located but not byte-contiguous"). No C1 kill-rule hit: the quote exists.

## 5. Defects in the landed bytes

Measured: **30** CJK characters. Landed statements:

| file (bytes I read) | statement | measured | status |
|---|---|---|---|
| `corpus/knowledge/contamination-transparency-card.md` line 6 (file sha256 `9dd5ff1b…680c`, line sha256 `0d31e797…37b5`) | "the caveat … (1 whitespace token, **23 CJK characters**, text-layer lines 78-81)" | 30 | **wrong count** |
| `corpus/SOURCES.md` line 112 | "the caveat sentence … (1 whitespace token, **30 CJK characters**) spans extraction lines 78-81" | 30 | count correct |
| `corpus/lessons/round-30.md` line 56 | "一致したもの…残る (1 token / **23 CJK chars**, p.1 = printed 797)" | 30 | **wrong count** |
| `.ufo/waves/round-30/build/R30RowSchema.md` §6 | "The **23-character** caveat spans a line break …" | 30 | **wrong count** |

- **D-a (count).** The entry's `source:` line states 23 CJK characters for a span that has 30, and it contradicts the registry row it points at, which states 30. The same round's own source seat measured 30 in its staged-quote audit (`R30SrcS086.md`: "card Q4; 30 chars, no trailing 。"). So the number was corrupted between the seat's capture and the entry line, and the error then propagated into the lessons receipt and the row-schema review. 23 has no referent in these bytes: 30 total, 25 distinct, 10 kanji, and the contiguous no-unwrap suffix `混入とみなして除去することには疑問が残る。` is 20. [INFERENCE] provenance: the adjacent `source: S085` line carries the identical `<n> CJK characters` phrasing with 23, and 23 is exactly the comma-stripped length of S085's second quote — a copy-down from the line above is the most economical explanation, not an independent miscount.
- **D-b (line range).** "text-layer lines 78-81" bounds the *enclosing sentence* (`しかし、表 1 のように、…`), not the quoted bytes: the 30-char caveat itself sits at lines **80–81**. A reader who seeks the quoted text at line 78 finds `似的に示した。しかし、表 1 のように、極めて短い`. The registry's own label ("the caveat *sentence* … spans extraction lines 78-81") is defensible; the card applies the sentence's range to a clause.
- **D-c (word counter, minor, disclosed).** "1 whitespace token" is the post-unwrap count; on the raw text layer the span is 2 tokens. The entry discloses non-contiguity, so this is a precision note, not a contradiction.
- The registry row's count (30), its `status=mined`, `opened=2026-10-25`, `recheck=180d` and `used-by=corpus/knowledge/contamination-transparency-card.md` are all as claimed.

## 6. Comparison with the build seat's capture (opened only after §1–§5)

Agreement, verified against my own files — not taken on report:

| item | build seat (`R30SrcS086.md`) | mine |
|---|---|---|
| PDF sha256 / bytes | `c3706aca…b303` / 371155 | same, and `cmp` **IDENTICAL** to their saved copy |
| raw extract | `88b4201d…fc1f` / 30100 | same |
| unwrapped extract | `887adab8…b8a9c` / 29076 | same |
| layout extract | `3d8ecf8c…852a` / 41898 | same bytes (`all.layout`-equivalent; page-1 slice 4687) |
| printed labels | 797–802, U+2015 | same |
| title | 3 tokens, 26 chars, contiguous, = `/Title` | same |
| caveat | not a byte run in raw/layout; exact in unwrapped | same, and PyMuPDF independently agrees |
| caveat position | unwrapped byte offset 3715 | **3715** (char offset 1419; their number is a byte offset, which is why it looks different from a char count) |
| sentence position | offset 3559, 85 chars, 3 tokens, raw lines 78–81 | **3559**, 85, 3, 78–81 |
| byte-exact fallback run | `混入とみなして除去することには疑問が残る。` needs no unwrapping | confirmed, 1 occurrence in raw and layout |

**No factual disagreement with the source seat.** The disagreement is with what was *written into the entry*: their audit already says 30 and already scopes 78–81 to the sentence; the card line says 23 and applies 78–81 to the clause. `R30RowSchema.md` §6 reproduces the same 23 error while quoting the split correctly.

## 7. Does the quote support the use the entry makes of it?

- The caveat is in the **authors' voice**, not a quotation of prior work: it closes the §2 関連研究 paragraph on Riddell et al. [24] and refers to **表 1**, which is this paper's own table — `p1.raw.txt` … `all.raw.txt` line 88: `表 1 Riddell らの手法により、評価データの正解（左）と…`. So "S086's false-positive caveat" (card CG4) is a fair description.
- The paper's own method corroborates the motive rather than contradicting it: 概要 lines 19–21 propose `評価データと学習データの間の文字列の一致の検出に加えて、由来となるレポジトリの情報を用いる手法`, and §4 contains a step titled `短い文字列の無視` (all.raw line 474) plus `般的な文字列は混入検出の対象から除外するこ…` (line 336). The caveat is the stated reason for that exclusion, so filing it against CG4 ("what a negative does not rule out") is supported by the source, not merely by the quote.

## 8. What this check does and does not establish

- Established: both asserted spans are verbatim and located on PDF page 1 = printed 797; the title needs no unwrapping, the caveat needs unwrapping and is present in two independent extractors; the capture is byte-identical to the one the round used.
- Not established here: the paper's numeric results (the seat's numerals are out of scope for this item), and whether any *other* S086 sentence quoted elsewhere in the corpus is verbatim — I checked only the two spans named in the entry's `source:` line.
- Nothing was run to "confirm" a claim from a build report; every number above came from the files named in §1–§2.

## 9. Tooling

- **No installs and no upgrades.** `pacman` untouched (host-wide pause respected). No binary placed in `~/.local/bin`.
- One ephemeral addition: `uv run --with pymupdf` (PyMuPDF reports version `2.0`) to get a second, independent extractor. It lives only in the uv cache for the duration of the run; nothing was added to `PATH`.
- Host tools used read-only: `curl`, `file`, `pdfinfo`/`pdftotext` (poppler 26.08.0), `sha256sum`, `cmp`, `python3`.
- Lane writes: this file only.

VERDICT: FAIL — `corpus/knowledge/contamination-transparency-card.md` line 6 misstates its own S086 evidence (caveat measured at 30 CJK characters, stated as 23; the quoted clause sits at text-layer lines 80–81, not 78–81), and it contradicts the `S086` row of `corpus/SOURCES.md`, which states 30. Both quoted spans are themselves verbatim and located on p.1 / printed 797 (title contiguous, caveat after line unwrapping), so the repair is a number and a line range, not a quote: C1's kill rule is not triggered for S086.

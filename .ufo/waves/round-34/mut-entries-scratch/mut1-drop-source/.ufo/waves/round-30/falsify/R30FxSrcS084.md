# R30FxSrcS084 — independent re-open of S084, span-level falsification

- **Seat:** L1Kengaku30.R30FxSrcS084-3 (leaf; independent capture; no lane edits outside this file)
- **Round / wave:** round 30, hyaku run 6 — FALSIFY wave
- **Candidate under test:** `corpus/knowledge/contamination-transparency-card.md`
- **Assertion under test:** the entry's `source: S084` line (card `:4`) and the registry row it backs
  (`corpus/SOURCES.md:110`) — three Chinese spans with line numbers and whitespace-token counts
- **Access date:** 2026-10-25
- **Independence:** I fetched the page myself, measured the bytes myself, and only then opened
  `.ufo/waves/round-30/build/R30SrcS084.md`. No install, upgrade, or package transaction of any kind
  was performed (no `pacman`, no `uv tool`, no `npx`); `curl`, `python3`, `cmp`, `sha256sum` from the host
  were sufficient.

Bottom line: all three spans the entry and registry row assert are single-occurrence byte substrings of my
own capture, at exactly the lines stated, with exactly the stated whitespace-token counts; the card and the
registry anchor cell reproduce. Two *other* landed numbers that carry the same 3/13/3 shape do not reproduce
— see D3 below; they are not on the card's `source: S084` line. The single machine-read verdict is the last
line of this report.

## 1. My capture

| field | value |
|---|---|
| URL | `https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html` |
| fetch 1 | `curl -sSL -A "Mozilla/5.0 (X11; Linux x86_64) kengaku-r30-falsify"` → `http=200`, `size_download=32762`, final URL unchanged |
| sha256 | `c4447d93c6945d2c68dbffac8274b3adc4aa2b6e510120c33eea1de966b7ec23` |
| bytes | `32762` |
| lines | 562 newlines, **563** logical lines (file does **not** end with a newline, so `wc -l` prints `562`, not `563`) |
| fetch 2 (refetch) | `http=200`, `size_download=32762`, `cmp` against fetch 1 → clean, same sha256 → stable within the round |
| `content-length` | `32762` (server-declared length equals my on-disk bytes) |
| `last-modified` | `Fri, 14 Feb 2025 07:00:08 GMT` |
| `etag` | `"67aee9f8-7ffa"` |
| `server` / `date` | `istio-envoy` / `Sun, 25 Oct 2026 07:39:22 GMT` |
| scratch (outside the lane) | `/tmp/r30fx-S084/s084.html`, `/tmp/r30fx-S084/s084.b.html` |

Version identity, read from my own bytes: line **16** is
`<title>数据污染评估 &mdash; OpenCompass 0.4.0 documentation</title>` and line **312** is the `<h1>`
`数据污染评估`. No other `x.y.z` third-party version string occurs in the document except KaTeX
`0.10.0` (8× in `<link>` font URLs, lines 77-84) and one `0.18.1` asset reference — so the `0.4.0` the
entry attributes is the page's own title, and it is the only version evidence the page carries.

**Measurement conventions used below.** *Whitespace tokens* = `len(span.split())` (the same counter
`plans/sources_adopt.py:272` uses and the one the registry annotates). *CJK characters* = code points in
U+4E00–U+9FFF (Han); for these three spans that equals the count of non-ASCII code points, because none of
the spans contains full-width punctuation. *Byte offset* = length of the UTF-8 prefix before the span in my
capture. *Locatedness* = `span in capture`, a plain substring test, 1 occurrence each.

## 2. The three spans, verbatim, measured

### Span a — first method's dataset coverage (card `:4`, registry `:110`)

Verbatim: `目前该方案仅支持 GSM8K 数据集`

| measure | value |
|---|---|
| line | **344** (entry and registry both say 344) |
| byte offset / byte length | 17813 / 40 bytes |
| **whitespace tokens** | **3** — `目前该方案仅支持` / `GSM8K` / `数据集` (card says 3 ✔) |
| **CJK characters** | **11** Han (8 + 3), 18 code points total |
| occurrences | 1 |
| verdict | **located** |

Raw line 344 is `<p>目前该方案仅支持 GSM8K 数据集，我们欢迎社区贡献更多的数据集。</p>`; the span stops before
the full-width comma `，`, so it is a prefix of the sentence, contiguous in the bytes. Section trace: line 344
lies inside `<section id="id2">` (opened line 316, closed 362), under `<h2>` line 317
`基于自建同分布数据的污染数据标注` — the first of the two methods, as the entry says.

### Span b — second method's dataset coverage (card `:4`, registry `:110`)

Verbatim: `目前该方案仅支持 C-Eval, MMLU, HellaSwag 和 ARC 数据集`

| measure | value |
|---|---|
| line | **397** (entry and registry both say 397) |
| byte offset / byte length | 25836 / 66 bytes |
| **whitespace tokens** | **7** — `目前该方案仅支持` / `C-Eval,` / `MMLU,` / `HellaSwag` / `和` / `ARC` / `数据集` (card says 7 ✔) |
| **CJK characters** | **12** Han (8 + 1 + 3), 42 code points total |
| occurrences | 1 |
| verdict | **located** |

Raw line 397 continues `<p>…数据集，<a class="reference external" href="https://github.com/liyucheng09/Contamination_Detector">Contamination_Detector</a>
中还包含了 CSQA 和 WinoGrande，但目前还没有在 OpenCompass 中实现。我们欢迎社区贡献更多的数据集。</p>`. The
span ends before the `，` that precedes the inline `<a>`, so it does not straddle markup. I confirmed the
contiguity hazard is real for the *whole* sentence: the tag-stripped sentence
`目前该方案仅支持 C-Eval, MMLU, HellaSwag 和 ARC 数据集，Contamination_Detector 中还包含了 CSQA 和 WinoGrande，但目前还没有在 OpenCompass 中实现。我们欢迎社区贡献更多的数据集。`
has **0** occurrences in the raw bytes — the entry's shorter form is the only form that passes a
byte-substring gate on this artifact. Section trace: line 397 lies inside `<section id="id3">` (363-415),
`<h2>` line 364 `基于经典预训练集的污染数据标注` — the second method.

### Span c — access limitation (card `:4`, card CG2 `:79`, registry `:110`)

Verbatim: `但如今开源社区往往只会公开模型参数而非训练数据集`

| measure | value |
|---|---|
| line | **315** (entry and registry both say 315) |
| byte offset / byte length | 13608 / 72 bytes |
| **whitespace tokens** | **1** — the run is unspaced (card says 1 ✔) |
| **CJK characters** | **24** Han, 24 code points total |
| occurrences | 1 |
| verdict | **located** |

Raw line 315 is `<p>但如今开源社区往往只会公开模型参数而非训练数据集，在此种情况下 如何判断是否存在数据污染问题或污染程度如何，这些问题还没有被广泛接受的解决方案。OpenCompass 提供了两种可能的解决方案。</p>`.
Line 315 sits in `<section id="id1">` (311-415) — the intro paragraph *before* the first `<h2>`, i.e. the
access statement that motivates the two methods, not part of either. Note the single ASCII space in
`在此种情况下 如何判断`: it is in the source bytes and lies outside the quoted span, so it does not affect
the count of 1, but a longer quote that crossed it would count 2.

### The "two documented methods" claim

Exactly **two** `<h2>` elements exist in the file (line 317, line 364), and no `<h3>` at all; the two
`<section>` children of `id1` are `id2` and `id3`. Line 344 ∈ `id2`, line 397 ∈ `id3`. The entry's
"the two documented methods (html lines 344 and 397)" is therefore accurate as a structural claim, not a
reading of ordering.

## 3. Gate re-run on my capture (not on anyone's report)

I rebuilt two quote files in `/tmp` from the *landed bytes themselves* and ran the landed gate against my
capture:

- From the card's `source: S084` line (`corpus/knowledge/contamination-transparency-card.md:4`), wrapped as
  an 11-cell row:

```
QUOTE rows=1 spans=3 located=3 found=3 overlong=0 absent=0 malformed=0 cap=25 artifacts=s084.html
  ok S084 words=3 at s084.html quote="目前该方案仅支持 GSM8K 数据集"
  ok S084 words=7 at s084.html quote="目前该方案仅支持 C-Eval, MMLU, HellaSwag 和 ARC 数据集"
  ok S084 words=1 at s084.html quote="但如今开源社区往往只会公开模型参数而非训练数据集"
EXIT=0
```

- From the landed registry row (`corpus/SOURCES.md:110`, copied verbatim with the table header): identical
  `rows=1 spans=3 located=3 found=3 overlong=0 absent=0 malformed=0`, `EXIT=0`.

So the gate's own counter agrees with my hand measurement on all three spans (3 / 7 / 1), and the counts the
card and the registry anchor cell print are the counts the gate prints. That is the property QUALITY Q10
asks for and it holds here.

## 4. Comparison with the build seat's report (`build/R30SrcS084.md`), opened after my capture

Agreements (byte-level, checked against my own artifact, not taken on trust): sha256
`c4447d93…b7ec23`; 32762 bytes; refetch byte-identical; `last-modified 2025-02-14`, `etag "67aee9f8-7ffa"`,
`content-length 32762`; title on line 16; `<h1>` on line 312; all three line numbers; single occurrence each;
span-b's whole-sentence contiguity hazard (0 raw occurrences, `<a>` inside the sentence); span-a offset
17813; span-b offset 25836.

Disagreements, each with the byte that shows it:

**D1 — the line count is attributed to the wrong command.** Report `:15` says "`563` lines (`wc -l`)".
`wc -l` on this artifact prints `562`, because the file's last byte is not `\n`
(`t.endswith("\n") == False`, `t.count("\n") == 562`, `len(t.splitlines()) == 563`). The number 563 is the
logical line count; it is not what `wc -l` prints. Low severity (no gate reads it), but it is the same
class as the round-29 "prints green while measuring the wrong thing" mistake: a number annotated with a
method it did not come from.

**D2 — span-c's byte offset is wrong, and is reused for a second, later run.** Report `:57` gives
`byte offset 13768` for the run that begins `但如今…`; that run starts at offset **13608** in my capture
(and 13608 is forced: the file is byte-identical to the seat's, same sha256). Offset 13768 is the start of
the *later* run `这些问题还没有被广泛接受的解决方案。`, which report `:64` also labels 13768 — correctly. Two
different runs cannot share an offset, and the start of a later run cannot precede the start of the run that
contains it; `s084.html[13768:13820]` decodes to `这些问题还没有被广泛接受的解决方案。OpenCompass 提供了两种…`,
confirming which of the two labels is the wrong one. The card and registry cite *lines*, not offsets, so
no landed claim breaks — but `build/R30RevEntryQ7Q9.md:201-202` repeats the triple
"17813 … 25836, 13768" as independently verified, so the bad offset propagated into a reviewer's evidence
without being recomputed.

**D3 — the seat's counts are paragraph counts, and that frame leaked into two landed numbers.** The seat is
internally explicit: it counts the **full tag-stripped paragraph** (3 for line 344's paragraph, 13 for line
397's, 3 for line 315's), and separately states that the card's form of line 397 is "7 tokens" and that the
narrower line-315 run is "1 token". I reproduced both frames exactly — full-paragraph tokens of line 397 =
**13**, of line 315 = **3**; quoted-span tokens = **7** and **1** — so the seat did not misquote anything.
What inherited the paragraph frame is elsewhere:

| landed byte | says | measures | status |
|---|---|---|---|
| `corpus/knowledge/contamination-transparency-card.md:4` | 3 / 7 / 1 whitespace tokens | 3 / 7 / 1 | **reproduces** |
| `corpus/SOURCES.md:110` anchor cell | 3 / 7 / 1 whitespace tokens | 3 / 7 / 1 | **reproduces** |
| `corpus/SOURCES.md:110` teaches cell | "CJK quotes count **1-13** whitespace tokens" | the row's own three spans span **1-7** | **does not reproduce**; 13 is reachable only by counting line 397's whole paragraph, which the row does not quote |
| `corpus/lessons/round-30.md:51` | `…HELLA…ARC 数据集 (13, line 397)`; `…训练数据集 (3, line 315)` | 7 and 1 | **does not reproduce** — and the lesson's own sentence two lines above says "Word counts are whitespace tokens, the counter the gate prints" |

So the disagreement is not with the seat's evidence but with the transposition of it: the lesson table's
column is headed *located quotes (words / location)*, yet two of its three S084 cells carry the containing
paragraph's token count. The lesson therefore contradicts its own stated counter, and `1-13` in the registry
teaches cell is the same paragraph count surviving as a range. A reader who trusts the lesson would conclude
the card's C-Eval span is annotated 13 when the card says 7 — and would "repair" the card in the wrong
direction. Nothing in the lane's checkers reads these numbers: `plans/round30_defects.py` has no round-30
lesson check at all (its `D2`/`D3` regexes are bound to `corpus/lessons/round-29.md` and to the round-29
quote), and `gate_timing_check.py` reads only `VERDICT:`/report/writer lines. That is why the mismatch
survives a green gate.

A sibling seat reached the same numbers for the spans independently — `build/R30ConnCorpus.md:349` re-derives
S084 span 2 as **7** and span 3 as **1** ("does not reproduce"), and `:473` records it as defect D-c. Its
D-c additionally lists the *registry anchor cell* as carrying "13 whitespace tokens"; the landed anchor cell
now reads 7 and 1, so either the row was repaired after that report or the connector read a pre-repair
working copy (`git status` shows `M corpus/SOURCES.md` uncommitted, so the two readings may simply be
different revisions of an uncommitted file). What survived all repairs is the teaches cell's `1-13` and the
lesson row's 13/3.

## 5. One recheck hazard worth pinning (not a defect in the landed bytes)

The registry locator is the `latest` alias; the only evidence that these are the 0.4.0 docs is the served
`<title>`. On this host, `does_not_exist_r30fx.html` under `/latest/` returns a real `404` (153 B,
`<title>404 Not Found</title>`), so a 200 does mean something — but
`/zh_CN/v0.4.0/advanced_guides/contamination_eval.html` returns **HTTP 200** with 27091 bytes whose title is
`Welcome to the OpenCompass Documentation &mdash; OpenCompass 0.5.4 documentation`, i.e. the docs root of a
*different* version, and it contains **none** of the three spans. A 180-day recheck that "pins the version
path" would get a 200 and the wrong page; the recheck must keep using the `/latest/` URL the row names and
assert the spans, not the status code. This also means the entry's "0.4.0" is a title reading, not a
version-path fetch, and it cannot be independently corroborated from the site's versioned URLs today.

## 6. Residual unknowns

- Whether upstream republishes `latest` before the 180-day recheck; `last-modified 2025-02-14` is the only
  freshness signal, so `verified-at` records the access, not a page revision.
- Whether `Contamination_Detector` (the external repo the page links) really carries CSQA/WinoGrande: the page
  says only that they are *not implemented in OpenCompass*. Nothing in the entry's S084 use depends on it.
- Whether the two non-reproducing numbers (D3) are repaired in a later revision of an uncommitted file; my
  reading is of the bytes present at report time.

## 7. Confidence

- **High** on capture identity (two fetches, `cmp` clean, size and sha256, server-declared length),
  on locatedness (1 occurrence each, exact offsets), on token/CJK counts (recomputed three ways: hand split,
  my script, and the landed gate), and on the section trace.
- **High** on D1/D2/D3 as contradictions between two measurable numbers, not as readings.
- **Medium-high** on the claim that the lesson's 13 and 3 are the *paragraph* counts rather than an unrelated
  error: both reproduce exactly under that frame (13, 3) and neither reproduces under the span frame, and the
  build seat that produced them reports precisely those paragraph counts.

VERDICT: PASS

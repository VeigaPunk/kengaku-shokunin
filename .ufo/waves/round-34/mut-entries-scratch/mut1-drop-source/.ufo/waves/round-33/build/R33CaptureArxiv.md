# R33CaptureArxiv — S104 re-grounding capture (arXiv 2412.05579v2)

Seat: capture leaf. Scope: open the pinned v2 abstract page, commit bounded bytes + digest,
report the printed title, locate the frozen abstract sentence, and supply a ≤25-word located
quote for the S104 anchor cell. Access date **2026-10-25** for every source opened below.

**VERDICT: `captured`**

---

## 1. Capture identity

Command (exact, single fetch, no retries):

```
mkdir -p .../.ufo/waves/round-33/assimilation/captures
curl -fsSL 'https://arxiv.org/abs/2412.05579v2' \
  -o .../.ufo/waves/round-33/assimilation/captures/arxiv-2412.05579v2-abs.html
# exit 0
```

| field | value |
|---|---|
| absolute path | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-33/assimilation/captures/arxiv-2412.05579v2-abs.html` |
| lane-relative path (the committed path) | `.ufo/waves/round-33/assimilation/captures/arxiv-2412.05579v2-abs.html` |
| bytes | **43661** (`stat -c '%s'`; `file`: `HTML document, ASCII text, with very long lines (2528)`) |
| sha256 | **`44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660`** |

Server-side corroboration (separate `curl -fsSI`, headers only, same URL):

```
HTTP/2 200
last-modified: Mon, 24 Aug 2026 21:41:04 GMT
content-type: text/html; charset=utf-8
date: Sun, 25 Oct 2026 17:23:05 GMT
content-length: 43661
```

`content-length` equals the captured byte count exactly.

Digest manifest: `.ufo/waves/round-33/assimilation/captures/SHA256SUMS.txt` already carried this
exact digest line for this path (manifest mtime 14:18, my fetch 14:22 — the pre-existing line and
my independent fetch agree byte-for-byte). Verification from the lane root:

```
$ sha256sum -c .ufo/waves/round-33/assimilation/captures/SHA256SUMS.txt
.ufo/waves/round-33/assimilation/captures/arxiv-2412.05579v2-abs.html: OK
.ufo/waves/round-33/assimilation/captures/toolathlon-ab-testing-evaluation-main.py: OK
.ufo/waves/round-33/assimilation/captures/toolathlon-utils-evaluation-retry.py: OK
exit 0
```

No manifest edit was needed from this seat (the line is already correct).

---

## 2. v2 revision metadata — PRESENT

Four independent markers, all in the captured bytes:

| line | evidence (verbatim) |
|---|---|
| 109 | `<strong>arXiv:2412.05579v2</strong> (cs)` |
| 115 | `[Submitted on 7 Dec 2024 (<a href="https://arxiv.org/abs/2412.05579v1">v1</a>), last revised 10 Dec 2024 (this version, v2)]</div>` |
| 166–168 | submission history: `[v2]` … `Tue, 10 Dec 2024 05:49:12 UTC (4,809 KB)` |
| 41 | `<meta name="citation_date" content="2024/12/07" />` … `<meta name="citation_online_date" content="2024/12/10" />` |

So the page served at the `v2` URL is the v2 revision (`this version, v2`), revised 10 Dec 2024,
and not a silent redirect to a later version. `[v1]` appears only as a submission-history entry
(`Sat, 7 Dec 2024 08:07:24 UTC (4,814 KB)`).

---

## 3. Title exactly as printed

Line 117, the `Title:` line (offset 11299):

```html
<h1 class="title mathjax"><span class="descriptor">Title:</span>LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods</h1>
```

**Exact title text:**

```
LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods
```

The same string appears 11× in the capture (lines 4, 21, 23, 33, 41, 98, 116, 117, 177, 243, 248),
including the `citation_title` meta at line 41 — i.e. no title variant exists anywhere in the page.

**Correction to the task's premise:** the staged row does *not* spell the title `LLMs-as-judges`.
Staged `SOURCES.append.md:27` (row S097) spells it

```
LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods
```

which is byte-identical to the capture's `Title:` line — capital `Judges`. The lowercase-`j`
`LLMs-as-judges` string appears in the staged row only *inside its abstract quote*, and that quote
carries the real defect reported in §4/§7.

---

## 4. The abstract sentence — located, with one transcription defect in the staged string

The sentence **as supplied in the task and in the staged row** (single `L`):

```
This paper presents a comprehensive survey of the LMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.
```

resolves **0 times** in the capture (`grep -c` → `0`, exit 1). At sentence scope it is absent.
(Raw substring `grep -o 'LMs-as-judges'` returns 9 hits, but every one is the tail of a longer
`LLMs-as-judges`; that is a substring confound, not a match.)

The sentence **as printed** (double `LL`):

```
This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.
```

resolves **3 times**, all of them inside the page's three copies of the abstract:

| line | byte offset | location |
|---|---|---|
| 30 | 2979 | `<meta property="og:description" content="…">` social-card description |
| 41 | 6613 | `<meta name="citation_abstract" …>` Highwire metadata |
| 124 | 13290 | **the visible abstract body**, `<blockquote class="abstract mathjax">` opening at byte 12721 |

Located context in the abstract body (line 124): the sentence sits immediately after
“…interpretability in the form of natural language.” and immediately before
“We begin by providing a systematic definition of LLMs-as-Judges…” — it is the fourth of the
abstract's ten sentences, closing the framing passage before the roadmap sentences (“We begin…”,
“Then…”, “Additionally…”, “Finally…”).

Properties that matter for quote matching: the matched string is **contiguous** (no inline tags
inside it) and **entity-free** (no `&#39;`/`&amp;`), so it matches the capture's stored bytes
literally. The surrounding abstract *does* contain entities — `referred to as &#39;&#39;LLMs-as-judges&#39;&#39;`
— and two verbatim defects: `we aim aims to provide insights` and `maintain the relevant resource
list at this https URL`. Do not anchor on the abstract tail.

---

## 5. Anchor cell — proposed quote (20 words, ≤25)

Quote (20 words, verbatim, line 124):

> This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.

Proposed `anchor` cell (provenance prefix + the 20-word located quote):

```
arXiv 2412.05579v2 (submitted 7 Dec 2024; last revised 10 Dec 2024), abstract, <blockquote class="abstract mathjax"> sentence 4 of 10: "This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations." (20 words)
```

---

## 6. Draft registry row for S104 (adoption bytes for the L1 — do not integrate from here)

Schema copied from live `corpus/SOURCES.md` (11 columns, header line 21); conventions sampled
from live rows: `recheck` = `180d` (as used by S081/S082/S083/S090/S093/S100), `opened` = round
access date, `used-by` = the entry path.

```
| S104 | LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods — https://arxiv.org/abs/2412.05579v2 | paper | B | the survey's own five-perspective decomposition of LLM-judge evaluation — functionality, methodology, applications, meta-evaluation, limitations — for the preprint's own text at the pinned v2 revision; tier B under row 10 because the abs page shows no journal reference and no DOI at the time of opening | arXiv 2412.05579v2 (submitted 7 Dec 2024; last revised 10 Dec 2024, "this version, v2"), abstract: "This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations." (20 words) | the field's own survey separates *meta-evaluation* — how a judge is itself evaluated — from methodology and applications, which is the separation a calibration protocol needs; the limitations section is where a lane looks for the known failure modes of judge-based scoring | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-grader-semantics.md |
```

Tier evidence for the `B` claim, checked in the capture, not inherited: `grep -c` for
`Journal reference`, `DOI:`, `journal-ref` → **0 / 0 / 0**. The metatable carries only
`Comments: 60 pages, comprehensive and continuously updated` (line 130) and
`Subjects:` (line 134, cs.CL; cs.IR). Preprint at 2026-10-25 → tier B, matching the staged row's
row-10 rationale.

For the entry's `source:` line, cite the **pinned** URL `https://arxiv.org/abs/2412.05579v2`
(not the bare `abs/2412.05579`), since the row's quote is a v2-revision quote.

---

## 7. Cross-check against staged row S097 (`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md:27`)

| # | staged field | captured truth | judgement |
|---|---|---|---|
| 1 | title `LLMs-as-Judges: …` | identical byte-for-byte (line 117) | **matches — no defect** (task premise "staged spells LLMs-as-judges" is wrong, see §3) |
| 2 | abstract quote `…survey of the LMs-as-judges paradigm…` | printed text has `LLMs-as-judges`; single-`L` sentence resolves 0 times | **DEFECT — must be corrected before adoption**; under C1's kill rule an unfindable located quote refuses the row (S104 would be refused, dropping the entry to 1 surviving new row and forcing the honest-stop path) |
| 3 | source URL `https://arxiv.org/abs/2412.05579` (unpinned) with the quote labelled `arXiv 2412.05579v2` | page at `/abs/2412.05579v2` is v2 | **DEFECT (pin hygiene)** — cite the `/v2` URL the capture was taken from |
| 4 | `opened 2026-10-23`, recheck `2026-10-23 — re-verify at the next revision` | this round's access date is 2026-10-25 | must be re-dated `opened 2026-10-25`, `recheck 180d` for the lane row |
| 5 | `Comments: "60 pages, comprehensive and continuously updated"` | line 130 text identical | matches |
| 6 | staged S103 = the survey's full-text PDF row | lane S103 is frozen to Toolathlon `evaluation/main.py` @ `9be8d8fe…` | boundary note: the full-text row is **not** carried by the renumber and must not take id S103; the C1 entry cites only S093/S103/S104 |

Related finding for C1's predicate, checked live: **S093's `used-by` already reads**
`corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md`
— the entry is already named there (from the round-32 draft), so no append is required for S093;
a counter that expects a fresh diff on that cell will mis-score.

---

## 8. Falsifiers handed to the L1

1. Adopting the staged S097 quote unchanged guarantees a verbatim-resolution failure (0 matches);
   the correction is one character (`LMs` → `LLMs`) and is proven above.
2. The staged title is already correct — no title erratum is owed, and writing one would be a
   false record.
3. The row must carry the pinned `/v2` URL; the staged URL is unpinned.
4. S093 already satisfies `used-by`; S103/S104 are the only rows needing `used-by`.
5. Tier stays B: no journal reference, no DOI in the capture at 2026-10-25.
6. Do not quote the abstract tail: it contains `we aim aims to` and the literal `this https URL`.
7. Unrelated shared-dir observation: `captures/swebench-pro-tests-test.sh` (7864 B, mtime 14:22)
   has **no** line in `SHA256SUMS.txt`. Not my file and not my item — flagged so whoever owns the
   SWE-bench capture item can manifest it; `--verify`-style checks over this directory will not
   see it.

---

## 9. Writes, reads, tools

- Files written by this seat: the capture in §1 and this report. Nothing else.
- Scratch: `/tmp/r33-R33CaptureArxiv/` created, empty.
- Read-only reads outside my write scope: `plans/round-33-claims.md`, `corpus/SOURCES.md`,
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` (read-only tree, no writes).
- No build, lint, test, formatter, counter, or git mutation was run; the parent owns the gate.
- **Tool installs/updates: none.** No pacman transaction attempted (host pause respected);
  `curl`, `sha256sum`, `grep`, `awk`, `sed`, `python3` were already present and sufficient.

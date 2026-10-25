# R30FxSrcS083 — independent re-open of source S083 (falsify wave, round 30)

- **Seat:** `L1Kengaku30.R30FxSrcS083-3` (leaf; no dispatch, no lane edits except this file)
- **Access date:** 2026-10-25
- **Target:** https://aclanthology.org/2026.findings-eacl.353.pdf
- **Candidate:** `corpus/knowledge/contamination-transparency-card.md`
- **Question assigned:** the entry's `source: S083` line quotes two spans from p.1 (printed 6710). Are they byte substrings of the raw extraction, or only of a normalised form?
- **Short answer:** **neither span is a byte substring of any raw extraction I produced.** Span 2 is a substring of a whitespace-collapsed capture. **Span 1 is a substring of no capture under any whitespace-only or wrap-join normalisation** — it needs a hyphen-blind compare, because poppler's default mode deletes the hyphen the paper prints.

Scratch: `/tmp/r30fx-s083/`. The build seat's report was opened only after every measurement in §1–§6 below was taken.

---

## 1. My capture (fetched independently of the build seat)

| field | value |
|---|---|
| fetch 1 | `curl -sSL` → `http=200 size=2697379 type=application/pdf` |
| fetch 2 | `http=200 size=2697379`; `cmp` clean against fetch 1 → **CMP-CLEAN** |
| sha256 | `662c2235680e475c1880b1a4486a8e001eb746c6d992384e1400d01287b3dfe4` |
| bytes | `2697379` (equals served `Content-Length`) |
| `ETag` | `"2928a3-64cefe4654240"` |
| `Last-Modified` | `Fri, 13 Mar 2026 23:04:33 GMT` |
| `pdfinfo` | `Pages: 15`, A4 `595.276 x 841.89 pts`, `Producer: pdfTeX-1.40.27` |
| `file(1)` | `PDF document, version 1.7, 6 page(s)` — **wrong**; per-page extraction succeeds for 1–15 |

**One distinction that matters and is easy to blur.** No quote is a byte substring of the PDF *file*: `grep -c -a "contamination" s083.pdf` = **0**, and `qpdf --qdf --object-streams=disable` then `grep -a` = **15**. The text layer is Flate-compressed. Every "raw" claim below therefore means **raw text extraction**, never the file's own bytes.

## 2. Extraction tools and versions (stated as required)

| tool | version | use |
|---|---|---|
| poppler `pdftotext` | **26.08.0** | primary: `-raw` per page, `-layout`, default, and `-remove-hyphens none\|soft\|all` |
| `pypdf` | **6.21.2** | second, independent text-layer reader (`uv run --with pypdf`) |
| `qpdf` | **12.4.2** | stream decompression (§1 only) |
| `python3` | **3.14.8** | substring / occurrence / line-number measurement |
| `uv` | 0.13.0 | ephemeral env for pypdf |

No system packages installed, no global tool installed, `pacman` untouched.

## 3. Page label — the landed locator is correct

Page 1's extracted tail carries folio `6710`; its running header reads `Findings of the Association for Computational Linguistics: EACL 2026, pages 6710–6724`. The rule *pdfpage N → folio 6709+N* holds on **all 15 pages** (I tested each page for its expected folio; zero failures — page 12's folio `6721` sits mid-page beside a wide table, not in the trailing lines, so a tail-only read misses it).

Both spans are on pdfpage 1 = printed page 6710, as the entry and the registry row say. **This part of the claim is verified.**

## 4. Span 1 — the 14-word span

> `a contamination-resistant design by separating the publicly released game engine from hidden card implementations`

- **Word count:** 14 (my count, and the gate's own `words()` counter both print 14).
- **Location:** pdfpage 1 / printed 6710; abstract, innovation (1); `pdftotext -f 1 -l 1 -raw` lines **25–28**. It is a numbered-list clause, not a standalone sentence — the enclosing sentence is 51 words (measured) and over the gate's 25-word cap.
- **Verdict: LOCATED (content faithful), NOT a byte substring of the raw extraction, and not recoverable by whitespace normalisation.**

The divergence is **one character**, and it is a *deleted* one. In the default (dehyphenating) capture the region reads:

```
a contaminationresistant design by separating the publicly released game engine from hidden card implementations
```

`difflib.SequenceMatcher` over the two strings yields exactly one non-equal opcode: `delete '-'`. Re-inserting that single hyphen makes the span a byte substring of the default capture (`True`). poppler's default mode deletes **every** wrap hyphen on this page — `re-|leased`, `imple-|mentations`, `eval-|uation` are correctly rejoined, and `contamination-|resistant` is wrongly rejoined, because this hyphen is a genuine compound hyphen that happens to land at the wrap.

In the `-raw` and pypdf captures the hyphen is present, but the span then contains **three** wrap hyphens the quote lacks:

```
a contamination-
resistant design by separating the publicly re-
leased game engine from hidden card imple-
mentations
```

So the quote keeps one hyphen and drops two. **No single mechanical rule — collapse, wrap-join-with-hyphen, or wrap-join-without-hyphen — produces this span.** A `-layout` capture interleaves the two columns and does not carry the span contiguously at all.

## 5. Span 2 — the 19-word span

> `We also formalize a practical threat model and refresh protocol that preserves evaluation integrity even if specific cards leak.`

- **Word count:** 19 (mine and the gate's counter: 19). Complete sentence. Faithful: it ends at `leak.` — the paper continues `Our analysis across 17 models…`.
- **Location:** pdfpage 1 / printed 6710; abstract sentence 3; `-raw` lines **33–35**.
- **Verdict: LOCATED; substring only of a normalised form.**

Not a byte substring of any capture, because the capture breaks after `threat`:

```
do so. We also formalize a practical threat
model and refresh protocol that preserves eval-
uation integrity even if specific cards leak. Our
```

The gap here is *only* a line break plus, in the `-raw`/pypdf captures, the `eval-|uation` wrap hyphen. **A plain whitespace collapse (N2) already locates this span in the default capture**, exactly once; `-raw` and pypdf additionally need the wrap-join.

## 6. Normalisation matrix (same normalisation applied to quote *and* capture)

| normalisation | pdftotext default | `-raw` | `-layout` | pypdf 6.21.2 |
|---|---|---|---|---|
| **N0** raw bytes | S1 ✗ S2 ✗ | S1 ✗ S2 ✗ | S1 ✗ S2 ✗ | S1 ✗ S2 ✗ |
| **N1** CRLF→LF only (**this is the landed gate**) | S1 ✗ S2 ✗ | S1 ✗ S2 ✗ | S1 ✗ S2 ✗ | S1 ✗ S2 ✗ |
| **N2** + collapse whitespace runs | S1 ✗ **S2 ✓** | ✗ ✗ | ✗ ✗ | ✗ ✗ |
| **N3** + wrap-hyphen join, hyphen removed | S1 ✗ **S2 ✓** | S1 ✗ **S2 ✓** | ✗ ✗ | S1 ✗ **S2 ✓** |
| **N4** + hyphen-blind (every `-` deleted) | **S1 ✓ S2 ✓** | **S1 ✓ S2 ✓** | ✗ ✗ | **S1 ✓ S2 ✓** |

Occurrence counts at N4 over the whole 15-page document: **S1 = 1, S2 = 1** — so each occurs only where the row says.

Two readings worth carrying forward:

1. A **`-layout` capture admits neither span at any level up to N4.** A gate handed a human-style layout dump refuses every paper row, whatever hyphen policy it declares.
2. Span 1 needs N4 (a *character*-deleting compare), not merely N3. That is strictly stronger than the "line break" caveat the entry already writes for S086.

## 7. The decisive operability test — the landed row is unprovable by the landed gate

`plans/sources_adopt.py` normalises both sides with `normalize_text()` = CRLF→LF **only**, and `locates()`'s own docstring says the test is "a byte substring of the normalised text, never a fuzzy or whitespace-insensitive match". `grep` for `pdf|PDF|canonical|hyphen` in the whole file: **no hits**. I ran the landed S083 row (line 109 of `corpus/SOURCES.md`, unchanged, extracted verbatim) through `--quote-file … --artifact …`:

| artifact handed to the gate | gate output | exit |
|---|---|---|
| my raw `pdftotext` capture | `located=0 found=0 absent=2` | **7** |
| whitespace-collapsed capture | `located=1 absent=1` (S1) | **7** |
| **the build seat's own canonical, hyphen-blind capture** | `located=1 absent=1` (S1) | **7** |
| hyphen-blind capture **+ the hyphen deleted from the quote** | `located=2 found=2 absent=0` | **0** |

The third row is the finding: **canonicalising the artifact exactly as the build seat prescribes still fails**, because the gate normalises only the artifact and never the needle. Exit 0 is reachable **only by editing the quote's bytes** — deleting a hyphen the paper actually prints. The row and the gate, as both are landed, are mutually unsatisfiable; since the row's bytes are the truthful ones, the repair belongs on the gate side (a declared, two-sided PDF canonical form), which is what the build seat recommended and which C3's landed predicate does not require.

## 8. Comparison with the build seat (`build/R30SrcS083.md`) — read after §1–§7

### Independent agreements

Every measured claim of substance reproduces on my own fetch:

- sha256 `662c2235…`, 2697379 bytes, 15 pages, `file`'s bogus 6, the `6709+N` page map, the title/author line.
- "none of the three quotes is a byte substring of the raw extraction" — confirmed at N0 for spans 1 and 2 in all four captures.
- The two-sided hyphenation argument is correct, and I confirm it by a stronger route than the report's own: N3 (join, drop hyphen) admits S2 and refuses S1 in three of four captures; the keep-hyphen variant (`-\n`→`-`) also refuses S1, because `re-|leased` and `imple-|mentations` then stay hyphenated. Neither policy alone admits both.
- Their canonical form (my N4) admits span 1 and span 2 exactly once each, document-wide.
- All secondary counts verify: (a2) = 24 words, tail = 18, enclosing sentence = 51, spans = 14 and 19.
- The (a2) observation that the "Our approach." sentence says **private** where the abstract clause says **hidden** is true in my bytes.

### Disagreements

**D1 — every line-number citation in the report is wrong (5 of 5), measured under the exact command the report names (`pdftotext -f N -l N -raw`, poppler 26.08.0).**

| report says | my measurement | offset |
|---|---|---|
| (a) `p1.txt` lines 29–33 | `p1.txt` lines **25–28** | −4 |
| (b) `p1.txt` lines 38–41 | `p1.txt` lines **33–35** | −5 |
| (a2) `p1.txt` lines 50–53 | `p1.txt` lines **83–86** | +33 |
| (iv) `p2.txt` lines 43–46 | `p2.txt` lines **51–54** | +8 |
| §3.2 `p3.txt` lines 50–52 | `p3.txt` lines **47–50** | −3 |
| §3.2 `p4.txt` line 34 | `p4.txt` line **23** | −11 |

The quoted *text* at each locus is real and matches the artifact; the *pointers* are not reproducible, and the offsets are not a single mode shift (I tested default mode too: (a) moves to 15, (b) to 18, (iv) to 76, p3 to 31, p4 to 30 — none reproduce 29/38/43/50/34). A location pointer that a later round cannot re-find is the one thing a registry row exists to carry. **The lander was right to drop them**: the landed row cites `p.1 (printed 6710)`, which I verified.

**D2 — the `-remove-hyphens` table is one measurement printed three times.** In `-raw` mode all three values produce **byte-identical** output: `4332` bytes, sha256 `f2e7a842f0afdcf5e5e54608bbcd288a91365a8e516f075b73cb1d4379da5a6c` for `none`, `soft` **and** `all`. The flag is inert in `-raw`. It discriminates only outside `-raw`: in default mode, `none`/`soft` → `5b2b33a6…` (wrap hyphens kept), `all` → `00a2dd06…` (`contaminationresistant`). Their *conclusion* survives — I confirmed refusal at N0 in default/none, default/soft and default/all — but the three-row table does not support the wording "under any poppler hyphen mode" as evidence.

**D3 — `build/R30BuildAppend.md`'s note is mode-dependent and, as a general statement about "PDF text extraction", false.** It says "S083's `contamination-resistant` is dehyphenated to `contaminationresistant` by PDF text extraction." That is true only of poppler's **default** mode; `-raw`, `-layout` and pypdf 6.21.2 all keep the hyphen (`contamination-\nresistant`). The precise statement, which changes what the gate has to do: *default mode deletes every wrap hyphen, so the compound's hyphen vanishes; the raw and pypdf modes keep all wrap hyphens, so the span then carries three the quote lacks.*

**D4 — two small overstatements by omission.** (i) Span 2 does not need the full canonical form: whitespace collapse alone locates it in the default capture. (ii) The `-layout` case was never tested and is the worst: it refuses both spans at every level up to N4.

## 9. Defects in the landed bytes

1. **Undisclosed normalisation, on the row and in the entry.** `grep -i "hyphen\|byte\|normalis\|normaliz\|dehyphen"` over `corpus/knowledge/contamination-transparency-card.md` → **0 hits**. The S083 `source:` line asserts both spans under `p.1, printed page 6710` with `(14 words)` / `(19 words)` and says nothing about how they were located. The registry row (`SOURCES.md:109`, anchor cell 5) is the same.
2. **Asymmetry inside one file.** The S086 line in the *same entry* explicitly writes "spans extraction lines 78-81, so it is reported as located but not byte-contiguous". That is a *line break*, recoverable by a whitespace collapse. S083's span 1 is worse — a **deleted character**, recoverable by nothing short of a hyphen-blind compare — and carries no note at all. The milder case is disclosed; the stronger one is silent.
3. **The entry's `recheck:` instruction cannot pass for this row.** It says to "re-locate each quoted span in fresh captures and re-run `python3 plans/sources_adopt.py --quote-file <admission rows> --artifact <capture>`". Measured for S083: exit **7**. As written, that procedure is unexecutable for a row the entry itself admits.
4. **Severity is disclosure, not fabrication.** C1's kill rule fires on "a cited source whose located quote cannot be found in this round's own fetch". Both spans **were** found: wording exact, order exact, page label exact, word counts exact, each occurring once in the document. The row is not killed. What fails is the entry's implied claim that the landed gate can re-prove it.

## 10. Not tested here (outside this assignment)

- The other five rows (S081, S082, S084, S085, S086) against their own captures — other seats own them. The exit-7 result above is evidence about S083 only; it is *not* extended to them.
- Whether the Anthology will serve identical bytes on a later date; my sha256 pins the 2026-10-25 representation.
- The paper's own contamination figures and its 17-model analysis: out of scope, and outside what this artifact independently establishes.

## Receipt

```
2697379  s083.pdf           sha256 662c2235680e475c1880b1a4486a8e001eb746c6d992384e1400d01287b3dfe4
2697379  s083-refetch.pdf   same sha256; cmp clean
 46589  p1-default.txt      sha256 1c2292a8c37045bc0954752deaf037cfbc45e1305d11e633d9c8dbf2eb71ddb6
 46579  p1-raw.txt          sha256 d965610682f099b063c03fb34f7282746a24a4cf5193ce739312abcd5a50ea38
 76312  p1-layout.txt       sha256 71e10e2626e15fbeb50f125f6d3737b9397048ee32f16c1dcbbb682086f99b5a
  4332  p1-pypdf.txt        sha256 6609588fb3adbda29604dee22cc1d27bf56e5de2a5c71ef1f14263c6d41cd3b9
  4332  hyph-{none,soft,all}.txt  all three identical: f2e7a842f0afdcf5e5e54608bbcd288a91365a8e516f075b73cb1d4379da5a6c
  4278  dflt-all.txt        00a2dd06d230e85495d56ec277f4af04663c0e9a26966492a29b8a63ef2b5ba8
  4340  dflt-{none,soft}.txt  identical: 5b2b33a6cca1ab9faf2a5bfbd8a412cc27f08b73bdb30aabdf2ff48da9dd21e0
46039  p1-hyphblind.txt     sha256 5ac87af0a0858071d401b7b63f2ad1bd9f05db5ca2aa043fea00f7dd3b674027
  919  s083-row.txt          SOURCES.md line 109, byte-extracted verbatim
 1060  s083-quotefile.md     header + that row, fed to --quote-file
```

`plans/sources_adopt.py` was run from the lane read-only; no lane byte was written except this report.

VERDICT: PASS — corpus/knowledge/contamination-transparency-card.md — both S083 spans verified version-located on pdfpage 1 / printed 6710 with exact wording and exact word counts (14, 19) in my own independent fetch (sha256 662c2235…, 2697379 B, 15 pages), each occurring once document-wide, so C1's kill rule does not fire; neither span is a byte substring of the raw extraction — span 2 needs only a whitespace collapse, span 1 needs a hyphen-blind compare because poppler's default mode deletes the compound hyphen — and since the entry discloses that caveat for S086 but not for S083 and its own `recheck:` command exits 7 here, that silence plus the build report's five wrong line pointers are recorded defects to repair, not falsified quotes.

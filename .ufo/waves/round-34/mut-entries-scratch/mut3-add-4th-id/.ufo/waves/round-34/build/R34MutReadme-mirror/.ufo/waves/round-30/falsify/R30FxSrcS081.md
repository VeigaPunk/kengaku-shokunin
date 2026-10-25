# R30FxSrcS081 — independent re-read of S081 (arXiv 2608.29463)

Seat `R30FxSrcS081` (role: scout, leaf). Wave `kengaku-r30-falsify`, 2026-10-25.
Candidate under test: `corpus/knowledge/contamination-transparency-card.md` (its `source: S081` line)
and the S081 row at `corpus/SOURCES.md:107`.

**Order of operations, stated because it is the point of the seat:** I fetched and hashed my own
captures, located all three spans, and ran the gate before opening
`.ufo/waves/round-30/build/R30SrcS081.md`. Every number in §1–§5 is from my own bytes. The
comparison in §7 is post-hoc.

Bounds respected: no lane writes except this file; all work in `/tmp/r30fx-srcs081/`; no package
manager, no installs, no subagents, no background jobs; `/home/vgpnk/Projects/shokuknow` read only.

---

## 0. Summary

| assertion | verdict |
|---|---|
| span A, "one run" rule, claimed 22 words | **located**, 22 words, abs page line 124 |
| span B, five types, claimed 6 words | **located**, 6 words, abs page line 124 |
| span C, prevalence-robust, claimed 18 words | **located**, 18 words, abs page line 124 |
| stated location "abs page (HTML) line 124" | **accurate** in my capture (all three spans on that line) |
| the task text's "21-word prevalence-robust sentence" | **does not reproduce** — the sentence is 18 words; 21 appears in `corpus/lessons/round-30.md:51`, not in the entry or the registry row |

Two real defects surfaced, neither of them in the entry's quotes (details §6): the landed lesson
carries a word count that does not reproduce on my bytes, and the registry row's `scope` cell names a
protocol field the artifact its `anchor` cites does not contain.

---

## 1. My capture identity

Fetched 2026-10-25 with `curl -sS -L` for each URL; every response `200`.

| artifact | URL | bytes | sha256 |
|---|---|---|---|
| abs page | `https://arxiv.org/abs/2608.29463` | 44646 | `4c81bd3c180736318ed03e31968fa4d109b94025ec596203dbc4e963b396908a` |
| abs page `...v1` | `https://arxiv.org/abs/2608.29463v1` | 44660 | `f19d597a3906e083459d70fbaa2042a03b4a363d2873b5d6f8b24826746c85c3` |
| full text `...v1` | `https://arxiv.org/html/2608.29463v1` | 305243 | `7e5838c5ee2fdf5556f5e840378075a11780d8f47016d54fb965ce426759d7af` |

Served-state evidence (from the abs page response headers): `last-modified: Tue, 01 Sep 2026
00:48:48 GMT`, `age: 229542` (~63.8 h behind origin), `date: Sun, 25 Oct 2026 07:39:26 GMT`. The abs
page has not changed at origin since 1 Sep 2026, which is consistent with §5 below (v1-only, metadata
never regenerated from the compiled paper).

Version state, checked in my bytes: submission history at `abs.html:164-165` lists **[v1] only**
(`Sat, 29 Aug 2026 23:04:09 UTC (37 KB)`, from Johanna Angulo); `citation_arxiv_id` = `2608.29463`;
`citation_date` = `2026/08/29`; **0** occurrences of `withdrawn`/`retracted` in the page. Title
`Benchmark Contamination: A Taxonomy Organized by Defeated Mitigation` (8 words) occurs 11 times,
including the visible `<h1 class="title mathjax">` at `abs.html:116`.

## 2. The three asserted spans, measured

Word counts are whitespace tokens (`str.split()`), the counter the registry's own cells and the gate
use. Byte offsets are into my `abs.html`.

| span | verbatim span (mine to transcribe; each is a byte substring) | words | claimed | located |
|---|---|---|---|---|
| A | `because it is a property of one run, it must be recorded with the reported score rather than with the benchmark release` | **22** | 22 (entry line 1; `SOURCES.md:107`) | **yes** — `abs.html:124`, offset **13650**; also `:30` @3233, `:41` @7088 |
| B | `direct, derivative, temporal, distributional, and acquired` | **6** | 6 (both) | **yes** — `abs.html:124`, offset **13429**; also `:30` @3012, `:41` @6867 |
| C | `Two variables fall below the prevalence-robust threshold registered in advance: strata reporting and the acquired type introduced here` | **18** | 18 (both) | **yes** — `abs.html:124`, offset **14343**; also `:30` @3922, `:41` @7781 |

Each span occurs exactly **3** times in the abs page and **0** times altered; no span exceeds the
25-word cap. The entry's Claim section also quotes the tail
`is a property of one run, it must be recorded with the reported score rather than with the benchmark release`
(20 words) — also a byte substring (3 occurrences). The "What this does not establish" bullet repeats
span C verbatim. Every S081-attributed quotation in the entry is byte-present in my capture.

Location statement checked as written. The entry says "Abstract (HTML abs page, line 124)"; in my
capture line 124 is the abstract's text node (1974 chars; the `Abstract:` descriptor plus 278 words of
abstract), inside `<blockquote class="abstract mathjax">` opened at `:123` and closed at `:125`. So
"line 124" resolves to the visible abstract, not to a metadata carrier.

## 3. How strong the "line 124" locator actually is

The same abstract is carried three times in `abs.html`: `:30` (`<meta property="og:description">`),
`:41` (`citation_abstract` meta), `:124` (the rendered blockquote). Consequences I verified, not
assumed:

- A whole-file `grep -F` for any span passes even if the rendered abstract were removed, because the
  metas still carry it. The `line 124` claim is therefore only ever verified by a seat that looks at
  line numbers; nothing mechanical checks it.
- The gate cannot check it either: `quote_check()` calls `locates(quote, loaded)` on whole artifact
  text (`plans/sources_adopt.py:340-400`) and never inspects line or offset. `ANCHOR_COLUMN = 5` and
  `QUOTE_SPAN_RE = '"([^"]+)"'` are the only structural facts it reads.
- The locator is nevertheless **true** in my capture. No defect here — a strength-of-evidence note.

## 4. Independent gate run (not the lane's receipt)

I extracted the live row (`sed -n '107p' corpus/SOURCES.md`, 1137 bytes) and ran the lane's gate
myself against my own captures:

```
$ python3 plans/sources_adopt.py --quote-file row107.txt --artifact s081-abs.html
QUOTE rows=1 spans=3 located=3 found=3 overlong=0 absent=0 malformed=0 cap=25 artifacts=s081-abs.html
  ok S081 words=22 at s081-abs.html quote="because it is a property of one run, ..."
  ok S081 words=6  at s081-abs.html quote="direct, derivative, temporal, distributional, and acquired"
  ok S081 words=18 at s081-abs.html quote="Two variables fall below the prevalence-robust threshold ..."
EXIT=0
```

Against my `.../abs/2608.29463v1` capture: identical, `EXIT=0`. Against my **full-text** capture:

```
QUOTE rows=1 spans=3 located=2 found=2 overlong=0 absent=1 malformed=0 cap=25 artifacts=full.html
  ok S081 words=22 at full.html ...
  ok S081 words=6  at full.html ...
  REFUSED S081 absent words=18 quote="Two variables fall below the prevalence-robust threshold ..."
EXIT=7
```

So the row is green on the artifact its anchor names and **red on S081's own compiled text**. That is
the finding of §5, demonstrated rather than asserted.

## 5. The divergence that matters: the abs-page abstract is not the paper's abstract

From my `full.html` (`id="abstract1.1"`, rendered abstract at line 245), the compiled v1 abstract
prints the prevalence-robust outcome as **32 words**, and never prints span C:

> Of the five variables where no single code dominates, three clear the prevalence-robust threshold
> registered in advance; the two that fall below it are strata reporting and the acquired type
> introduced here

Other divergences I re-verified in my own bytes between `abs.html:124` and `full.html:245`:
`Leaderboards typically publish` / `capability and leakage remain` / `for automated detection; they do
not answer the question` / `closes the first of these alone` / `acquired during evaluation` /
`We operationalize the taxonomy as` / `unknown is a valid entry` (no quotes, inside a typewriter span) /
`test–retest` (U+2013) / `defeats—direct` (U+2014). Spans A and B survive this divergence as byte
substrings of `full.html` (line 245, 1 occurrence each); span C does not (0 occurrences).

**Why this does not fail the quote assertion.** The entry's locator says "Abstract (HTML abs page, line
124)" and the quote is exactly what that locator carries. The failure mode is narrower and worth
fixing: the entry's third bullet writes "S081 reports of its own protocol:" and then gives the
metadata wording, which the printed paper does not contain. A reader who opens the PDF to check the
lane's most load-bearing negative claim ("the two fields this entry adds are the two its source
measured as rare") finds a different sentence. The paper's sentence still supports the same two
variables, so the argument survives; the attribution wording does not.

Minimal repair, one clause: say "the abs-page abstract reports" (or cite `full.html:245` alongside
`abs.html:124` and quote the paper's 32-word form as the primary, noting the 18-word metadata form).
Second half of the same repair: the entry's `recheck:` line says "re-fetch S081–S086 at their pinned
locators … `--artifact <capture>`" — for S081 the pinned locator must be the **abs URL**, and the
recheck must say so, because an otherwise identical capture of the paper refuses the row (exit 7
above). NBSP hazard is real but not the driver here: `abs.html` has **0** U+00A0; `full.html` has
**241** across **173** lines.

## 6. Disagreements, named

### D1 — landed lesson prices span C at 21 words; my bytes give 18 (real, unrepaired)

- `corpus/lessons/round-30.md:51` (Sources table, S081 row): span C annotated **"(21)"**.
- `corpus/SOURCES.md:107` anchor: **"(18 words)"**. `corpus/knowledge/contamination-transparency-card.md:1`:
  **"(18 words)"**. Both are correct against my capture.
- No tokenization I tested yields 21: whitespace split **18**; hyphen-split (counting
  `prevalence-robust` twice) **19**; span C plus the following abstract sentence **33**; the paper's
  32-word form **32**. The figure 21 has no origin in these bytes.
- The same defect class was already reported by the connector seat
  (`.ufo/waves/round-30/build/R30ConnCorpus.md:348`, and `:473` as item "D-c"), and the lesson still
  says 21 on my read — the repair did not land.
- Nothing catches it. `plans/round30_defects.py` has **no S081 check at all** (`grep -n S081` → 0
  hits); D3 (`check_d3`, `:124-139`) prices only S078's line-75 quote. C2's `defects=0` therefore
  coexists with a wrong count in a landed source table. Any future re-read should treat the lesson's
  count column as unverified.
- Note for the record: the task text I was given repeats the lesson's "21-word" figure, which is where
  I found the discrepancy — the entry was right, the ticket and the lesson were wrong.

### D2 — the registry `scope` cell names a field the cited artifact does not carry

`SOURCES.md:107` scope: "the four-field contamination disclosure protocol (strata, elicitation budget,
five types, **regeneration**), its JSON schema and validator, …". Against my captures:

| token | in `abs.html` (the cited artifact) | in `full.html` |
|---|---|---|
| `regenerat` | **0** | 15 |
| four-field *enumeration* | `0` — the page has only the phrase "a four-field disclosure protocol" | `full.html:245` "elicitation and regeneration each stay under 25% in every stratum" |
| `strata` | 1 (inside span C) | present |
| `elicitation budget` | 2 | present |
| `JSON Schema`, `validator` | 1 each | present |

So the four-field list, and specifically `regeneration`, are supportable only from the full text or
PDF, while the row's `anchor` cites only "abs page (HTML) line 124". This is an anchor/scope mismatch,
not a quote defect: the gate reads the anchor cell only, so it cannot see it. Repair is either to add
the full-text locator to the anchor cell or to drop `regeneration` from the `scope` cell. The entry
itself does not repeat the four-field enumeration — it only claims "the four-field contamination
disclosure protocol" via the row — so the entry needs no edit for this item.

### Precision notes (no verdict weight)

- **P1** The entry's `source:` line cites "and the printed title" but carries no title span for the
  gate to validate. The title is verifiable (8 words, `abs.html:116` visible, `:4`, `:41`) — the
  citation is checkable in principle, unquoted in fact.
- **P2** The build report places `<blockquote class="abstract mathjax">` at line 124; the tag is at
  `:123` and its text at `:124`. Immaterial, recorded because the locator is what gets re-used.
- **P3** All three spans live on three lines, not one (§3). A recheck that only greps cannot
  distinguish "line 124" from "anywhere in the file".

## 7. Comparison with the build seat's report (read after my capture)

Agreements — every one of these is my own re-derivation, not their assertion accepted:

| claim | my result |
|---|---|
| abs page 44646 B, sha256 `4c81bd3c…` | identical |
| abs `...v1` 44660 B, `f19d597a…`; full text 305243 B, `7e5838c5…` | identical |
| span A at `:124` offset 13650; span B at `:124` offset 13429 | identical |
| spans A/B at `:30` and `:41` (offsets 3233/3012 and 7088/6867) | identical |
| word counts 22 (A), 6 (B), 8 (title) | identical |
| the full "fifth is acquired…" sentence is 30 words, over the 25 cap | identical (3 occurrences in abs) |
| abs page encodes em dashes as ASCII `--`, 0 U+2014; full text uses U+2014 | identical |
| abs-page abstract ≠ compiled abstract, with the divergences of §5 | **reproduced independently** |
| v1-only, 29 Aug 2026, `Preprint.` | identical |
| 0 U+00A0 in `abs.html` | identical |

Disagreements with the build report:

1. Its §6 says "`full.html` contains **173** U+00A0 non-breaking spaces". 173 is the number of **lines**
   containing one; the character count is **241**. Same bytes (sha256 identical), so this is an
   arithmetic/label error, not a capture difference. No impact on the entry — the direction of the
   claim (full text is NBSP-laden, abs page is clean) holds.
2. The build report never states a word count for span C anywhere (its §6 table quotes the fragment
   `Two variables fall below the prevalence-robust threshold registered in advance:` without a count,
   and §5 is about the title). So the 21 in the lesson did not come from the build report: it was
   introduced downstream, when the lesson's Sources table was written. The build report cannot be
   blamed for D1, and its own quote work is correct.

## 8. What would flip this verdict

- If arXiv regenerates the abs metadata abstract from the compiled paper (the normal event on a v2),
  span C disappears from the abs page and the entry's own third bullet becomes an unlocatable quote
  whose only support is the paper's rewording. The gate run in §4 shows exactly this outcome, exit 7,
  on today's bytes. The 180-day recheck (due 2027-04-23) will hit it if v2 lands first.
- If a rechecker uses the PDF or `full.html` as `--artifact`, S081 refuses today. The locator pinned in
  the entry must be the abs URL, explicitly.
- Nothing I tested would flip spans A or B: both are stable across abs page, `abs_v1`, and compiled
  full text.

## 9. Tooling

No tool installed or upgraded. `curl` (system) and `python3` (system) sufficed; pacman was not
invoked, consistent with the host-wide pause. Scratch: `/tmp/r30fx-srcs081/`
(`s081-abs.html`, `abs_v1.html`, `full.html`, `row107.txt`, `abs_plain.txt`, `full_abs2.txt`).

## Verdict

All three S081 spans the entry and the registry row assert are byte substrings of my independently
fetched capture, with the counts the entry states (22 / 6 / 18 words — not 21) and at the location the
entry states (abs page line 124, offsets 13650 / 13429 / 14343), and the lane's own gate returns exit 0
on that row against my capture. The defects I found are adjacent, not in the quotes: the landed lesson
mis-prices span C at 21 (D1), and the registry `scope` cell names `regeneration` while citing an
artifact that lacks it (D2); plus the forward risk that span C is metadata-only and will vanish if the
abs abstract is ever regenerated.

VERDICT: PASS corpus/knowledge/contamination-transparency-card.md — the entry's S081 quotes are verbatim in my capture at the stated counts and stated location; the 21-word figure is the lesson's, not the entry's.

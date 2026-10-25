# R30 FALSIFY — source S082 (`arXiv:2607.01254v2`), quote re-open

Seat: `L1Kengaku30.R30FxSrcS082-3` (leaf scout, falsify wave). Lane: `kengaku-shokunin`.
Date (UTC): **2026-10-25T07:39Z**. Scratch: `/tmp/r30fx-S082/`. Lane writes: this file only.
Installed/upgraded: **nothing** (`curl 8.23.0`, `python3 3.14.8`, `pdftotext`/`poppler` already on PATH).

Candidate under test: `corpus/knowledge/contamination-transparency-card.md` (its `source: S082` line, line 2)
plus the registry row it lands: `corpus/SOURCES.md:108`.

Method: I fetched, hashed and searched the source **before** opening any wave-1 build report. §6 is the
comparison, written afterwards.

---

## 1. Capture identity (mine, independent of the build seat)

| artifact | URL | HTTP | bytes | sha256 |
|---|---|---|---|---|
| full text v2 (the cited URL) | `https://arxiv.org/html/2607.01254v2` | 200 | 212631 | `82a5c5c6e9de647ee3fa7fb4c13c6d7b6decbaef5ed717b59c18d457d1371ed5` |
| abstract page | `https://arxiv.org/abs/2607.01254` | 200 | 43552 | `6ef2093990f95ec7297a0e29656a825a2730b5a6ab24d477ab4f56a37206571c` |
| abstract page, version-suffixed | `https://arxiv.org/abs/2607.01254v2` | 200 | 42993 | `ed049b139e3bc4d6ce2b790f9af0d62b397eb7e711bd008247f2b85c24bf2d94` |
| full text v1 (control, not cited) | `https://arxiv.org/html/2607.01254v1` | 200 | 212629 | `cf086cfc4fba9d8e22f218afdbeb5ce9c6910a715e9572ae500167aec2c4cfc6` |
| PDF v2 | `https://arxiv.org/pdf/2607.01254v2` | 200 | 257833 | `45986bd76db778016ce602c8f0f2f72055bbc8507934816846271366d81cba71` |

Line numbers below are 1-based lines of `html_2607.01254v2.html` (the artifact whose hash is above), reproducible
with `grep -n -F`. All five fetches returned 200 with `curl -sS -L`.

Source self-identity, read off my own captures: title on the abs page (`citation_title`) and on PDF p.1 is
**"The Benchmark Ceiling: Human Judgment, Evaluation Scarcity, and the Political Economy of AI Capability
Measurement"**; `citation_author` = Esposito, Mark; Zhang, Liu; version history `[v1] Thu, 4 Jun 2026`,
`[v2] Mon, 13 Jul 2026`; PDF header line `Working Paper | May 2026`.

---

## 2. Span A — the 11-word span

Verbatim, exactly as it sits in the fetched bytes:

> Item-level transparency and procedural transparency have opposite effects on benchmark validity.

- Words: **11** (`len(text.split())`, and independently `words=11` from the landed gate, §5).
- HTML: **line 855**, `<p id="S7.SS3.p4.1">`; second sentence of the paragraph. Section anchor `S7.SS3`
  opens at **line 746** with the heading **"7.3 Governance Design: Protected Items and Procedural Transparency"**.
  Enclosing §7 heading is "7 Governance Implications: Who Controls the Benchmark Controls the Narrative".
- PDF: **page 20** (located after stripping all whitespace — the PDF text layer line-wraps this sentence).
- Inline markup inside the span: none (the exact byte substring occurs on one line).
- **Verdict: LOCATED** — §7.3, line 855, word count 11, all three as the entry claims.

Variant that also exists (same clause, not the quoted sentence): a **23-word** abstract-form sentence at
**line 260**, `<p id="abstract1.2">`:

> Benchmark control creates epistemic power over the narrative of AI progress, while item-level transparency and procedural transparency have opposite effects on benchmark validity.

This is why a case-insensitive search returns 2 hits for the clause and 1 for the quoted standalone sentence —
the second hit is the abstract, **not** a second body occurrence.

---

## 3. Span B — the 17-word span

Verbatim:

> transparency should attach primarily to procedures, governance, credentials, and validity testing, not necessarily to live item pools

- Words: **17** (`words=17` from the gate too).
- HTML: **line 901**, `<p id="S8.SS2.p2.1">`, the post-colon clause of the paragraph's last sentence.
  Section anchor `S8.SS2` opens at **line 895** with heading **"8.2 Mandatory Transparency in Benchmark Design
  and Deployment"**.
- PDF: **page 23** (whitespace-stripped; line-wrapped in the text layer).
- Source punctuation: the sentence ends `…live item pools.` — the quoted span drops the terminal period and
  nothing else; the 17-word count is unaffected.
- Enclosing sentence is 27 words ("The key design principle, however, is the distinction formalized above: …"),
  i.e. over the gate's 25-word cap, so quoting the 17-word sub-clause is the correct move, not a silent trim.
- **Verdict: LOCATED** — §8.2, line 901, word count 17, all three as the entry claims.

Version stability: both spans are present in **v1 as well** (v1/v2 normalised text differs only in arXiv
site chrome — 6 diff lines, none in the body). The quote is not a v2-only artefact, so a v2 pin is safe
rather than load-bearing.

---

## 4. The staged absence claim — "the abs page carries neither phrase"

| search (whole page, HTML-stripped, case-insensitive) | `abs/2607.01254` | `abs/2607.01254v2` | `html/2607.01254v2` |
|---|---|---|---|
| span A exact | 0 | 0 | **1** |
| span B exact | 0 | 0 | **1** |
| `transparency` (any case) | **0** | **0** | 25 |
| `item-level` | 0 | 0 | 11 |
| `procedural transparency` | 0 | 0 | 11 |

- **Verdict: ABSENT** on both abstract-page forms — the entry's and the row's assertion is true for my capture,
  and still true for the version-suffixed abs URL (a form the build seat did not test).

**Why it is absent — this is the falsifiable edge of the claim.** The absence is not evidence that the phrases
are body-only. The abstract arXiv *registers* is **shorter** than the LaTeX abstract in the paper:

- abs page abstract (`citation_abstract` meta == the rendered `<blockquote>`, 1711/1721 chars, **238 words**) ends:
  `… Third, we develop the political economy and governance implications.`
- the LaTeX/HTML abstract (`abstract1.*`, **2159 chars**) continues past that cut:
  `Benchmark control creates epistemic power over the narrative of AI progress, while item-level transparency and procedural transparency have opposite effects on benchmark validity. The policy implication is not a choice between fully public and fully private …`

So span A's *clause* is an advertised, abstract-level claim of the paper; it is missing from the abs page only
because the registered abstract truncates one sentence before it. The claim as written ("the abs page carries
neither phrase") survives; an inference from it ("the quotes live only deep in the body") would be false.
Both the card (`## Corrections`, "the abs page carries neither phrase (the full-text HTML does)") and the
row's anchor stay on the safe side of that line; neither states the stronger inference.

Related card claim, also checked: the `## Corrections` note that the staged anchor pointed at a
`# Benchmark Governance` section "that does not exist in v2" is **accurate** — no heading in v2 contains that
string (0 `ltx_title` matches); the words "benchmark governance" appear only as lowercase body prose
(lines 749 and 911).

---

## 5. Independent machine checks (not read off any report)

I ran the **landed** gate against **my** captures, on a `/tmp` copy of the row (lane untouched):
`plans/sources_adopt.py --quote-file row082.md --artifact <my capture>`.

- vs `html_2607.01254v2.html` (mine): `QUOTE rows=1 spans=2 located=2 found=2 overlong=0 absent=0 malformed=0 cap=25`
  — `ok S082 words=11`, `ok S082 words=17`, **exit 0**.
- vs `abs_2607.01254.html` (mine): `located=0 absent=2`, **exit 7** (`REFUSED S082 absent` for both spans).

So the row's two quotes are valid inputs to the gate's own validator, and the abs page is refused by it —
the cited-locator choice (HTML full text, not `/abs/`) is the one that carries.

---

## 6. Comparison with the build seat (`build/R30SrcS082.md`), read after my capture

| item | my capture | build seat | agree? |
|---|---|---|---|
| v2 HTML sha256 / bytes | `82a5c5c6…71ed5` / 212631 | same | **yes, byte-identical** |
| abs page sha256 / bytes | `6ef2093990…6571c` / 43552 | same | **yes** |
| PDF sha256 / bytes | `45986bd7…cba71` / 257833 | same | **yes** |
| span A line / para id / words | 855 / `S7.SS3.p4.1` / 11 | same | **yes** |
| span A §7.3 heading line | 746 | 746 | **yes** |
| span B line / para id / words | 901 / `S8.SS2.p2.1` / 17 | same | **yes** |
| span B §8.2 heading line | 895 | 895 | **yes** |
| PDF pages | 20 and 23 (ws-stripped) | 20 and 23 | **yes** |
| abs page carries neither | absent both, 238-word abstract, ends "…governance implications." | same finding | **yes** |
| 23-word abstract variant | line 260, 23 words | line 260, 23 words | **yes** |
| title | Scarcity / Political Economy / AI Capability Measurement | same (report table line 12) | **yes** |

Independent fetches hours apart, run without coordination, produced identical bytes — the locators are
reproducible today.

**Disagreements: none on the quote, its location, its word counts, or the abs-page absence.** Where the seat's
report and the *landed bytes* diverge, and where my capture adds findings the seat did not reach:

### D-1 (landed defect, outside the quote predicate) — the registry row carries a false title

`corpus/SOURCES.md:108` reads:

> `| S082 | The Benchmark Ceiling: Human Judgment, Evaluation Economics and Benchmark Governance — https://arxiv.org/html/2607.01254v2 | …`

I checked the title against four of my own captures: abs `citation_title`, the v2 `<title>`/`h1`, the v1 `h1`
and PDF p.1 — all read **"…Evaluation Scarcity, and the Political Economy of AI Capability Measurement"**.
"Evaluation Economics and Benchmark Governance" is not a truncation or a variant — it is a different subtitle
attested nowhere in the source bytes.

Provenance is visible in the wave tree, so this is a landing regression rather than a sourcing error:

- `build/R30SrcS082.md:12` records the **correct** title (verified against `citation_title`).
- `build/R30RowSchema.md:24` — the row template — already carried the wrong title (and an `/abs/` URL).
- the landed row copied the template's title and the scout's URL.
- `build/R30RevEntryQ1Q6.md:45–46` **found it and wrote the remedy**: "… not '…Evaluation Economics and
  Benchmark Governance'. That is a row defect, not an entry defect, but the row must be corrected before
  adoption or the registry carries a false title."

It landed uncorrected. Every landed check still greens it: the frozen C1 predicate inspects ids, `status`,
`opened`, `used-by` and row presence — not titles — and `plans/sources_adopt.py` never reads the title cell or
fetches the URL (its only `https` string is a selftest fixture). I demonstrated the consequence directly: the
row's quote validation exits **0** while its identity cell is false. That is an admission-bar gap, not a C1
predicate failure: C1 can be satisfied by a row that misnames its source.

### D-2 (confirmations the seat's report did not include)

- the version-suffixed abs URL `abs/2607.01254v2` also carries neither phrase (seat tested only the bare `/abs/`);
- v1 carries both spans unchanged, so the pin to v2 is not what makes the quote exist;
- the seat's "no inline markup inside the span" claim for span A is confirmed by the byte-substring test;
- the seat recorded the PDF line-wrap honestly, and my whitespace-stripped search confirms the 27-word enclosing
  sentence at line 901, i.e. the 17-word split is required by the gate's 25-word cap.

### Minor, not defects

- The card's `## Claim` prose quotes span A without the source's terminal period (appends a comma) and quotes
  span B without its period. 11 and 17 words respectively, both verbatim substrings — integration punctuation
  only.
- Line-number locators are only as stable as the artifact; they are anchored to the recorded sha256, which is
  the right discipline, and the hash reproduces today.

---

## 7. Remaining unknowns

- Whether arXiv will keep serving this exact v2 HTML byte-string for the `recheck: 180d` window — the abs page
  metadata abstract and the LaTeX abstract already diverge, and a re-render would move lines 855/901 while
  leaving both spans findable. The quote survives a re-render; the *line numbers* do not.
- Whether the campaign's staged anchor (the `# Benchmark Governance` one) came from the same wrong title — I did
  not open the staging file; the coincidence is consistent but unverified.
- Whether the wrong title is the only row-level identity defect in the 88-row registry — outside my slice
  (I checked S082 only).

---

## 8. Verdict

Both spans are verbatim in my own fetch of the cited URL, at the claimed locations and word counts; the abs page
carries neither, as claimed (and the reason is registered-abstract truncation, not body-only sourcing). The
card's S082 line is true in every clause.

Line for `plans/gate_timing_check.py`:

VERDICT: PASS — corpus/knowledge/contamination-transparency-card.md (S082 line: both spans located at §7.3 line 855 / §8.2 line 901, 11 and 17 words, abs page carries neither)

Separate, row-level, for routing (not part of the verdict above and not in C1's predicate):
`corpus/SOURCES.md:108` lands a **false title** that a round-30 reviewer already required be fixed before
adoption (`build/R30RevEntryQ1Q6.md:45–46`); the quote gate cannot see it.

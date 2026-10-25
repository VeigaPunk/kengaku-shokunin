# R33SurveyScope — attack on the arXiv 2412.05579v2 row (S104)

Seat: R33SurveyScope (critic, leaf). Date: 2026-10-25. No production writes; this
report is my only lane-repo write. Scratch: `/tmp/r33-surveyscope/` (2 fetched files,
< 90 KB). Tooling: no installs (curl + sha256sum only).

## Evidence base

- Capture: `.ufo/waves/round-33/assimilation/captures/arxiv-2412.05579v2-abs.html`
  (618 lines). Digest verified this round:
  `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660` —
  `sha256sum -c .ufo/waves/round-33/assimilation/captures/SHA256SUMS.txt` → `OK`
  for all three captures (run 2026-10-25).
- Staged row: `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md:27`
  (staged id S097, read-only).
- Landed row under attack: `corpus/SOURCES.md:119` (lane id S104, renumbered from
  staged S097). Entry citing it: `corpus/knowledge/benchmark-grader-semantics.md:3,62-72`.
- Live re-fetch (my own, 2026-10-25): `https://arxiv.org/abs/2412.05579`
  (unversioned → 43,647 bytes) and arXiv API `id_list=2412.05579`
  (query `<updated>2026-10-25T17:27:47Z</updated>`).

## The five-perspectives quote — located, and the staged row dropped an L

Exact bytes in the capture, three independent carries, all identical:

- `:30` (og:description) and `:124` (abstract blockquote, the canonical location):
  `This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.`
- `:41` (citation meta) carries the same sentence.

**The abstract says `LLMs-as-judges` (two L).** Grep for single-L occurrences not
preceded by another L (`[^L]LMs-as-judges`) over the whole capture: **0 hits** —
`LMs-as-judges` does not exist anywhere in the captured bytes. The staged row's
anchor quote reads "a comprehensive survey of the **LMs-as-judges** paradigm" —
a quote that cannot be located in this round's captured bytes at the pinned
revision, i.e. exactly the C1 kill-rule shape ("located quote cannot be found …
is refused for that row"). As staged, the row would have been refused.

The landed `corpus/SOURCES.md:119` row carries the corrected string
`LLMs-as-judges`, byte-exact against `:124` including the closing period before
` We begin`, capitals F/M/A/M/L, and the hyphenated `Meta-evaluation`.
Word count 20 (≤ 25 ✓; I counted). The `Comments` quote `60 pages, comprehensive
and continuously updated` sits at `:131` (`<td class="tablecell comments
mathjax">`), 6 words ✓.

## v2 vs latest — v2 is both the pin and the current version

Live unversioned abs page fetched today carries the dateline
`[Submitted on 7 Dec 2024 (v1), last revised 10 Dec 2024 (this version, v2)]`
(same as capture `:115`). The arXiv API lists the latest version as
`arxiv.org/abs/2412.05579v2`, `<updated>2024-12-10T05:49:12Z</updated>` — no v3
exists. So the v2 pin and "latest" coincide as of 2026-10-25T17:27Z; pinning v2
(the immutable, addressable `…v2` object) rather than the mutable "latest" is the
correct choice under Q21, and the versioned URL stays re-fetchable even after a
future v3. The entry's `recheck:` line names the pin
(`benchmark-grader-semantics.md:5` — "re-fetch the three pinned revisions (…
arXiv 2412.05579v2)") ✓.

## Tier B — defensible

SOURCES contract v1 (restated `corpus/SOURCES.md:11-17`): B = "strong secondary
(expert write-up with reproducible detail, **survey**, textbook)"; "Tier is scoped
to `scope`, never global". The row's scope is the survey's own five-part structure,
and the record supports the preprint rationale today: the live abs page's metatable
carries Comments / Subjects / Cite-as / arXiv DOI only — `grep -ciE 'journal'`
over the whole page → **0**; no journal-ref, no venue. Lane practice is consistent:
peer-reviewed survey → A (S001, GEM 2026), preprint survey → B (landed S081, S098;
staged S121/S126 use the same rule). Tier B is correct, not a downgrade to repair.

Note: the staged rationale "tier B **under row 10**" cited `tier-rules.md` row 10
— a shokuknow-package file (confirmed: staged
`knowledge/corpus/knowledge/judge-meta-evaluation-2026-10-23.md:64` "tier B under
`tier-rules.md` row 10") that does not resolve in this lane. The landed row's
self-contained "tier B because it is a preprint" is the right repair; the tense
is present ("is") and verified true today. Optional hardening (not required):
"because it was a preprint at the time of opening (2026-10-25)", matching the
staged tense and Q21's pinned-historical-object reading.

## Scope cell — stays inside the quote

All five perspective names in the scope cell (Functionality, Methodology,
Applications, Meta-evaluation, Limitations) appear in the abstract sentence in that
order. The teaches gloss "how a judge itself is scored" is grounded in the abstract
itself: `:124` `…(How to evaluate LLM judges?)`. "Five-part structure" is a fair
narrowing of "five key perspectives". No widening except the one phrase below.

## "the field's own survey" — overclaiming (the one open repair)

Landed teaches cell: "the field's own survey separates meta-evaluation …". Echo at
`benchmark-grader-semantics.md:64`: "The field's own LLM-as-judge survey names the
paradigm's parts:". No byte in the capture asserts field-canonical or
field-representative status: the abstract self-describes as "a comprehensive
survey" by eight named authors (`:117`), unreviewed, whose maintenance commitment
is the authors' own ("We will continue to maintain the relevant resource list at
github.com/CSHaitao/Awesome-LLMs-as-Judges", `:124`). Under Q3 (a paraphrase may
narrow, never widen) and Q5 (label a source for what it is), "the field's own"
imports an unverified consensus claim into the row — while the same row's scope
cell correctly says "for the preprint's own text" and the entry's Source labels
(`:24-25`) correctly call it "an arXiv preprint … not an independent measurement".
Precedent cuts both ways (`benchmark-verifier-execution-model.md:27` uses "the
field's own documentation" and passed round-31 gates), so I flag severity
honestly: this is a wording overclaim, not a kill-rule breach — but it is exactly
the failure shape Q5's lesson names (mislabelling status), and the fix is one
phrase. Smallest safe correction:

- teaches cell → "the survey separates meta-evaluation — how a judge itself is
  scored — from methodology, so judge-based scoring owns a distinct validation
  protocol" (drop "the field's own"; optionally "a comprehensive survey separates…").
- entry `:64` → "The survey's abstract names the paradigm's parts:".

## Anchor — `Abstract` is acceptable; a section is not required

The row's claims (five-part structure, meta-evaluation as its own part, "How to
evaluate LLM judges?") are all asserted in the abstract; body sections matter only
for the staged-but-not-adopted full-text row (staged S103, § 6 META-EVALUATION),
which this round did not adopt. Precedent: abstract-only anchors are established
for arXiv rows (S004 "Published 2026-05-19, Abstract"; S008; S020; S022). The
anchor's dateline matches `:115` byte-for-byte in content. Strengthening available
(not refusal-level): S081's landed form names the capture line ("abs page (HTML)
line 124"), and the round-33 assimilation draft `.ufo/waves/round-33/assimilation/
append-rows.md` already carries it — `:41` title (8 words; "the survey's own
spelling, three Ls"), `:124` sentence (20 words), `:131` comments (6 words).
Recommend the L1 add the `:124`/`:131` line pointers (or record them in the Gate
row) so the Q10 second-seat location is cell-exact; this report supplies that
re-read for S104.

## Cell-correction table (staged S097 → landed S104)

| Cell | Staged S097 (`SOURCES.append.md:27`) | Landed S104 (`corpus/SOURCES.md:119`) | Correction still needed |
|---|---|---|---|
| source | same title/URL | same; title byte-matches capture `:4`/`:116` | none |
| kind | paper | paper | none |
| tier | B ("under row 10", unresolvable in lane) | B ("because it is a preprint" — verified live: no journal ref) | none (optional: "at the time of opening" tense) |
| scope | five-part structure, "row 10" rationale | same, self-contained rationale; all five names match abstract | none |
| anchor | quote **`LMs-as-judges` — not in capture** (kill-rule breach as staged); no word counts | **`LLMs-as-judges` byte-exact at `:124`**, "(20 words)"; Comments at `:131` "(6 words)" — repaired in landed bytes | add capture line pointers `:124`/`:131` per S081 precedent (strengthening) |
| teaches | "the field's own survey separates *meta-evaluation* …" | "the field's own survey separates meta-evaluation …" — **still overclaims** | **repair: drop "the field's own" → "the survey separates…"**; same echo at entry `:64` |
| status | mined | mined | none |
| opened | 2026-10-23 | 2026-10-25 (re-grounded this round; capture digest committed) | none |
| recheck | "re-verify at the next revision (Gate S097 below)" — pointed at the refused-id gate | 180d; entry recheck names the v2 pin (Q21 ✓) | none (optional: add "if a v3 appears, re-locate quotes") |
| used-by | benchmark-grader-semantics.md | benchmark-grader-semantics.md (new row, entry cites S104 at `:3`) | none |

## Checks actually run (honesty)

- `sha256sum -c` on the three committed captures → OK (2026-10-25).
- Read-only greps of the capture (`[^L]LMs-as-judges` → 0; sentence located at
  :30/:41/:124; Comments at :131; dateline at :115; authors at :117).
- Live fetches today: unversioned abs page (dateline v2-latest; `journal` 0 hits)
  and arXiv API (latest = v2, updated 2024-12-10; no `<arxiv:journal_ref>`).
- Not run (out of my scope, named for the L1): `plans/adoption_check.py`,
  `plans/round33_c1_verify.py`, `plans/sources_adopt.py` quote-mode — my quote
  re-read above is the Q10 input, not a substitute for those counters.

VERDICT: row-repair

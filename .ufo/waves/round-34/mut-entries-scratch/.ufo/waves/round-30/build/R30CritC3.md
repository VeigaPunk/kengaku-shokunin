# R30CritC3 — falsification of C3 (quote validation in the adoption gate)

critic: leaf seat, no dispatch, no production edit
round: kengaku 30 (hyaku run 6, 2026-10-25), access date 2026-10-25
attacked claim: `plans/round-30-claims.md` §C3 (frozen predicate quoted below)
tested artifacts: `plans/sources_adopt.py` @ `363a4eb` (478 lines, 10 selftest cases),
`.ufo/waves/round-30/claims/gate-before.txt`, `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`
rows S081–S086, and three artifacts staged by C1 seats in `/tmp` (opened read-only, not re-fetched)

**Verdict in one line.** C3's *predicate* survives the caller-supplied critique only because its second
clause says "the supplied artifact bytes" and therefore claims no provenance; the claim's *surface
sentence* ("validates … the thing that makes a row evidence: its quote") does not survive, and the
predicate is **satisfiable by a validator that refuses every quote** — so as frozen it does not
establish even the discrimination it does claim.

`/tmp/r30-GateQuote/sources_adopt.py` was **absent** (the directory existed and was empty at 04:21), so
no executor artifact was under test. Everything below is measured against the live gate, the staged
rows, and the three artifacts, by the probes recorded in `/tmp/r30-R30CritC3/`.

## 1. Named attacks

| # | attack | probe result | verdict |
|---|---|---|---|
| A1 | **vacuity** — an always-refuse validator satisfies the frozen predicate | `/tmp/r30-R30CritC3/always_refuse.py` prints exactly `SELFTEST cases=14 failed=0`, exit 0, with both named cases PASS and codes 6≠7 | **lands.** The predicate text cannot exclude a wrong artifact |
| A2 | **case arithmetic** — 10 existing + 2 named = 12 ≠ 14 | `grep -c '^        case(' plans/sources_adopt.py` → 10; `gate-before.txt` → `SELFTEST cases=10 failed=0` | **lands.** "including two new … cases" leaves two cases unspecified, and A1 fills them with filler |
| A3 | **caller-supplied artifact proves nothing** | S082's two anchor quotes (`ws_tokens=11`, `ws_tokens=17`) are **absent** from the fetched `s082-abs.html` (43552 B, direct=absent, whitespace-normalized=absent); that file contains `0` occurrences of `Benchmark Governance` — it is the abstract page, the quotes are from § Benchmark Governance | **lands as an identity limit, not a predicate limit.** The gate cannot separate (a) fabricated quote, (b) wrong document, (c) wrong portion of the right document |
| A4 | **byte-substring refuses real PDF quotes** | S083 PDF (2697379 B, sha256 `662c2235680e475c…`): raw bytes contain `0` plaintext `contamination` (compressed streams). `pdftotext` output contains S083's second quote verbatim (`We also formalize a practical threat model and refresh protocol …`) while the raw-byte test fails on it | **lands.** "absent from artifact ⇒ refuse" is a byte-layout test, not a fabrication test — and 3 of C1's 6 sources are PDFs (S083, S085, S086) |
| A5 | **text-layer hyphen loss** | S083's first quote is written `a contamination-resistant design …`; the text layer renders `(1) a contaminationresistant design by separating the publicly released game engine from hidden card implementations` (`contaminationresistant` count = 1, no hyphen glyph at all) | **lands.** Fails raw bytes and fails naive text comparison; the gate needs a declared rejoin rule or it refuses a correct quote |
| A6 | **CJK has no whitespace words** | S086's 53-wide-char quote → `ws_tokens=1`; S085's 48-wide-char quote → `1`; S084's quotes → `3` and `1`; a 212-wide-char Japanese quote → **`1` token, passes `<=25`** | **lands, and it is live in this round's set.** The cap is unenforced for S084/S085/S086 |
| A7 | **opt-in bypass** | `main()` requires `--access-date`/`--entries` only when `--admit-ids` is given; a `--quote-file` in the same style would be checked only when supplied, so the append path can still run quote-free | **lands.** No predicate case forbids omitting the flags |
| A8 | **no standing quote surface / no caller** | the repo convention is `corpus/evidence/roundNN-sources/gate.md`, 5 columns `id \| URL \| location/version \| located quote \| opening evidence` (r26, r27 present); `corpus/evidence/round29-attempt2/` has **none**; `corpus/evidence/round30/` holds only `census-before.txt`; S081–S086 quotes live **inside the `anchor` cell**, mixed with locator text | **lands.** `--quote-file` invents a schema with zero callers this round, and the surface it validates is not the row |
| A9 | **duplicate word authority** | `plans/round30_defects.py:38` already defines `def words(text): return len(text.split())` and D3 asserts a quote against it; a second counter in `sources_adopt.py` is a rival authority for the same contract rule. Convention wobble is real: `"731 -> 642 tasks: 89 dropped after review."` = **8** whitespace tokens, the lesson priced it **9** | **lands (mild).** Two gates, one rule, no shared definition |
| A10 | **non-isolating refusal cases** | if the 26-word fixture's quote is *also* absent from its artifact, either code can be produced by the other condition and the "absent" case is never exercised alone | **lands (test design).** Each named case must isolate one condition |

Measured S081 fact, needed for A6/A10: the first quoted span of S081's `anchor` cell is

```
We operationalize the taxonomy as a four-field disclosure protocol in which unknown is a valid entry, released under CC BY 4.0 with a JSON Schema, a validator, and worked examples.
```
= **30 whitespace tokens, 180 chars** — already over the 25-word cap, in the package C1 is admitting.
C3 does not wire the new check into C1's run, so that row is never tested and the over-length goes
unobserved while the receipt says the gate validates quotes.

## 2. Exactly what the gate proves, and what it does not

Proves, for one caller-supplied pair and a declared normalization:

1. the quote string occurs in the bytes the caller named as the artifact (or, added, the text extracted
   from them by a named tool at a named version);
2. the quote's token count is ≤ the declared budget under a declared tokenization;
3. the append block was built from rows the gate itself parsed (existing capabilities 1–3, unchanged).

Does **not** prove, and must not be read as proving:

- that the artifact is the cited source, or the cited portion of it (A3);
- that the source was opened on the access date — `opened=2026-10-25` still rests on `--attest-opened`,
  the caller's assertion (existing, unchanged);
- that the quote is the row's located quote, since no row cell holds one (A8);
- that a CJK or wide-character quote is length-bounded (A6);
- that any quote was checked at all on a normal `--admit-ids` run (A7);
- anything about a row's *evidence* status: the same caller authors the row, the quote, the artifact and
  the receipt. The only party who can break that tautology is a non-author holding the original bytes —
  which is what round 29's spot-check did by hand (`corpus/lessons/round-29-verifier-spotcheck.md` §3).

## 3. Wording the SCORECARD row must use

Capability name: `quote-consistency-check` — **not** `quote-validation`, **not** `evidence-gate`.

Row text (use verbatim, or stronger in the direction of less):

> `quote-consistency-check` — `plans/sources_adopt.py` now refuses a supplied quote that exceeds the
> declared word budget and a quote that is absent from the supplied artifact bytes under the declared
> normalization. Caller-consistent only: it does not verify that the artifact is the cited source or that
> the source was opened, the word budget is whitespace-tokenized and therefore unbounded for CJK text,
> and the check is exercised by its selftest, not yet wired into the adoption run.

Forbidden phrasings, each of which overstates what the gate proves: "validates quotes", "makes a row
evidence", "quote verified against the source", "closes the quote gap", "evidence-grade gate", and any
`failed=0` receipt quoted without the selftest's own accept-path cases named.

## 4. Smallest safe corrections, ranked

1. **Mutation pairs, not single refusals.** Four named cases: `quote-25-words-accepted` (exit 0, row
   emitted) / `quote-26-words-refused` (same quote + one word); `quote-present-accepted` /
   `quote-absent-refused` (≤25 tokens). This discharges the frozen `cases=14` as 10+4 **and** kills A1,
   A2 and A10 together. Without the two accept cases the claim must be reported partial.
2. **Bind to the standing surface.** `--quote-file` should name the existing
   `corpus/evidence/roundNN-sources/gate.md` shape (`id | URL | location/version | located quote |
   opening evidence`) and look up by row id, so the check is bound to a row rather than to a free-floating
   string. Optionally recompute sha256 and compare against the receipt's recorded hash — that blocks
   post-hoc edits, not fabrication; say so in the docstring.
3. **Make it mandatory on the append path.** When `--admit-ids` is given, require `--quote-file` and
   `--artifact` exactly as `--access-date` and `--entries` are required today (`parser.error`), plus a
   `missing-quote-file-refused` case. Otherwise A7 keeps the capability decorative.
4. **Declare the normalizations and print them.** NFC, whitespace collapse, `artifact-kind=pdf|html|text`,
   `extract=pdftotext-<version>` when text is extracted, hyphen rejoin for joined compounds (A5), and
   `quote-unmeasured` as an explicit verdict when a comparison cannot be made — never silently `absent`.
5. **Declare the token rule and refuse to certify wide text.** Tokenization = whitespace; for any quote
   containing East-Asian wide characters, print `wide_chars=N` and return `quote-budget-unmeasured`
   instead of a silent pass (A6).
6. **One `words()`.** Import the counter from a single place (D3's in `plans/round30_defects.py`) rather
   than defining a second one (A9).

## 5. Axis impact

- **operability:** as frozen, C3 adds a flag with zero callers and no mandatory path — a capability
  exercised only by its own selftest. Corrections 1–3 make it a real operability delta, because the
  append path then cannot run quote-free; without them the honest row is "capability added, not wired".
- **calibration:** A1, A2 and A7 are the calibration exposures. A receipt reading
  `SELFTEST cases=14 failed=0` produced by an always-refuse body is precisely the false-green class
  round 29's closure routed to this lane, and A2's two unspecified cases are the opening that lets it
  through while the frozen literal is still satisfied.

## 6. Limits of this review

- No executor artifact existed (`/tmp/r30-GateQuote` empty) — this attacks the frozen predicate and the
  live gate, not a candidate implementation.
- The three artifacts (S082 abstract HTML, S083 PDF, S084 docs HTML) were found already in C1 seats'
  scratch and opened read-only; I did not re-fetch them. S083's directory entry read 278528 B at my first
  listing and 2697379 B (`sha256 662c2235680e475c…`) moments later — the fetching seat was still writing
  it — so A4's measurements are pinned to the hash, not the byte count, and a re-run must match that hash.
  S081, S085, S086 quotes were **not** tested
  against artifacts — the CJK measurements are of row bytes only, and S085/S086 PDFs were not fetched
  into my scratch.
- I ran no production gate and its selftest (sibling-gate rule: evidence-verified, not executed). The
  case count was established statically (`grep -c '^        case('` → 10) and from the committed
  `gate-before.txt`, which shows `SELFTEST cases=10 failed=0` and `quote_mode_exit=2`.
- No tool installs or upgrades were needed; no pacman/uv transactions were attempted.

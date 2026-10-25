# R29 S071 — Python json serialization/escaping contract (source proposal)

seat: KengakuR28.R29SourceJsonDocs-2
actual writer: KengakuR28.R29SourceJsonDocs-2 (leaf; this report is the only file written)
verified-at: 2026-10-21
scope: propose one source row, S071, for the documented default escaping and rejection
behavior of stdlib json in Python 3.15.1. No `corpus/SOURCES.md` edit, no projection output,
no generator read, no runtime or deployment claim.

## Opened primary source

- URL: https://docs.python.org/3/library/json.html
- access date: 2026-10-21 (reader fetch of the URL; the reader reported method native).
- served identity: page title at rendered line 17 reads `json — JSON encoder and decoder —
  Python 3.15.1 documentation`; footer at line 761 reads `Last updated on Oct 21, 2026
  (13:02 UTC)`.
- chosen anchor: `#character-encodings`, heading at rendered line 576, inside
  `#standard-compliance-and-interoperability` at line 557. Anchored form:
  https://docs.python.org/3/library/json.html#character-encodings
- anchor rationale: the escaped-output sentence is located in Character Encodings. S065 on
  the same URL owns `#infinite-and-nan-number-values`; S052 owns
  `#json.JSONDecoder.raw_decode`. S071 is a distinct contract, not a substitute for either.

Line numbers below are rendered-document lines from the reader/grep fetch of this page. They
are document-layout positions, not byte offsets and not CPython source lines.

## Located quote (the only source quotation in this report)

> thus escaping the output so that the resulting strings only contain printable ASCII characters.

- location: under Character Encodings (heading line 576), rendered lines 581-582. The
  sentence begins at line 581 with its earlier clause naming `ensure_ascii=True`; the retained
  fragment is the part that wraps onto line 582.
- programmatic word count: 14 (Python `str.split()` on whitespace).
- retained bytes: 95 UTF-8 bytes, ASCII-only; sha256
  `ccdb630107e51b18d696d3f821a02c4ae84be5d497582cde5ae66515769f9d8e` over the quote text
  (UTF-8, no trailing newline).
- page bytes were not retained (instruction: safe quoted metadata only), so no page-level
  digest is claimed. Only this sentence fragment is stored.
- transcription check: the fragment deliberately excludes the inline `ensure_ascii=True` span,
  so it carries no emphasis markers and no backslash escaping. The S068/M78 wrapping and
  escaping erratum class therefore does not arise here.

## Observed documentation facts (source, not runtime)

| fact | rendered lines | observation |
|---|---|---|
| `json.dumps` default parameter | 254 | signature lists `ensure_ascii=True` |
| default output escaping | 581-582 | serializer escapes non-ASCII/non-printable by default |
| `ensure_ascii=False` escape set | 198-200, 452-454 | only quotation mark, reverse solidus, U+0000-U+001F are escaped |
| serializer BOM behavior | 588-589 | no BOM is added to output |
| deserializer BOM behavior | 590-591 | initial BOM raises `ValueError` |
| `json.loads` input domain | 337-345 | accepts `str`, `bytes`, `bytearray`; encoding UTF-8, UTF-16 or UTF-32; `encoding` keyword removed in 3.9 |
| strict decoding default | 398-400 | `strict` defaults to True; raw control characters 0-31 are allowed in strings only when it is false |
| invalid document | 402 | `JSONDecodeError` is raised; no repair is documented |
| exception class | 533 | `JSONDecodeError` subclasses `ValueError` |
| repeated object names | 620-625 | no exception; only the last name-value pair is used by default |
| order preservation | 168-169 | encoders and decoders preserve input and output order by default |
| implementation limits | 647-660 | no limits beyond Python datatypes/interpreter |

## Proposed S071 row (for L1; not written to SOURCES)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S071 | Python json module — JSON encoder and decoder — https://docs.python.org/3/library/json.html | docs | A | documented default serialization escaping and deserialization rejection of stdlib json 3.15.1; not generated config values, deployment, or runtime | Python3.15.1, Character Encodings §576-591, escaped-output sentence581-582; dumps default254; invalid-document402; BOM591; duplicate last-wins624-625; opened2026-10-21 | default `dump`/`dumps` escapes non-ASCII so output is printable ASCII; `ensure_ascii=False` escapes only quote, reverse solidus and U+0000-U+001F; `loads` accepts `str`/`bytes`/`bytearray` in UTF-8/16/32 and raises `ValueError`/`JSONDecodeError` instead of repairing an invalid document or initial BOM; duplicate names keep the last value; order is preserved | mined (proposed; L1 decides) | 2026-10-21 | on-release | — (pending; do not preclaim; distinct from S065 NaN/Infinity scope) |

Proposed status and used-by are deliberately not asserted as final. The row is not an index
row, coverage row, or admission.

## What this contract does and does not license for the round-29 projection

All items in this section are [INFERENCE] from the documented facts above, not measurements.

1. A re-serialization with default `json.dumps` is not a byte-identity function: it emits
   printable ASCII and its own separator/indent formatting. A digest of re-serialized output
   cannot stand in for the retained input bytes.
2. Text-level token replacement inserts profile characters literally. A value containing a
   quotation mark or reverse solidus can make the document invalid, and line 402 documents a
   raise, not a repair. `strict=True` also rejects raw control characters.
3. An initial BOM or non-UTF-8/16/32 byte stream is a parse-boundary rejection (591, 345).
   The projection must report it; stripping or normalizing it would be a repair the docs do
   not describe.
4. Duplicate object names collapse to the last value (620-625), so a plain parse cannot
   recover duplicate pairs. Any duplicate census needs `object_pairs_hook`, which is outside
   the default projection path.
5. Array order is preserved (168-169), so parsing does not disturb enumerate order. Whether
   output ordinal equals `task_id` remains a property of the frozen data, unmeasured here.
6. These docs describe CPython 3.15.1 stdlib behavior. They do not establish the lane's
   interpreter version, the upstream generator's own dump call, or any benchmark runtime.

## Unknowns preserved

- The lane's actual Python version/implementation used by the projection is unmeasured in
  this seat; the page is Python 3.15.1 documentation only.
- BOM presence, duplicate names, and non-ASCII escapes in `test.raw.json` are unmeasured here;
  this seat opened only the docs URL.
- The upstream generator's serialization call detail belongs to S070 and was not re-read.
- Whether any frozen profile value breaks JSON syntax is unmeasured; fixtures were not opened.
- No browser, config output, judge, model, or deployment behavior was observed.

## Commands, units, and outputs

- `read` of the URL at ranges 1-300, 301-560 and 564-768; the reader reported 768 rendered
  lines total for the fetched page.
- `grep` calls on the same URL, literal patterns and returned rendered lines:

```text
serializer sets <span class="pre">ensure_ascii=True</span> by default   -> no matches (grep reads rendered text, not raw HTML)
not a valid JSON document                                                -> 313, 402
escaping the output so that                                              -> 581-582
^### Character Encodings|^## Standard Compliance                         -> 557, 576
raises a \[`ValueError`\]|initial BOM                                   -> 590-591
^### Repeated Names|ignores all but|^json\.dumps|^json\.loads            -> 254, 337, 620, 624
quotation mark, reverse solidus|serializer does not add a BOM|preserve input and output order -> 168-169, 199, 453, 589
If \*strict\* is false|Subclass of \[`ValueError`\]                      -> 398, 533
^### Implementation Limitations|does not impose any such limits          -> 647, 659
Python 3\.15\.1 documentation|Last updated on                            -> 17, 761
```

  The first, raw-HTML-shaped pattern returned no matches: the fetched text is the rendered
  document, so all later patterns use rendered wording. This is a method limit, not evidence
  of absence.
- `python3` stdlib check on the retained quote: printed `ccdb6301...f9d8e 14` (sha256 prefix,
  whitespace word count); byte length 95; non-ASCII code points 0.
- `ls` of `.ufo/waves/round-29/build` and `.../drafts`; `os.path.exists` for this report path
  returned False before this write.
- No packages installed or updated. No production file, fleet state, sibling lane, Git index
  or jj state touched. No `corpus/SOURCES.md` edit.

## Limits

The docs URL is version-floating (`/3/`); the served 3.15.1 identity and last-updated stamp
above bound this read. On release, L1 must reopen the anchor and confirm the escaped-output
sentence, BOM, invalid-document, and duplicate-name lines before relying on the row.

VERDICT: PASS

Scoped to the S071 source-row proposal and its cited locations. This is not an admission, not
a projection measurement, and not a round verdict.

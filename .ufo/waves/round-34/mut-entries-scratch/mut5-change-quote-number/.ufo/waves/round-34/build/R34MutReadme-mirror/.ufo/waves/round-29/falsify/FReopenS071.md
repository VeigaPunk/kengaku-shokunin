writer: KengakuR29-2.FReopenS071-2

# FReopenS071 — live re-open of S071 (Python json docs): every cell holds, quote is exact, coverage notes only

Seat: `KengakuR29-2.FReopenS071-2` (leaf; actual writer same). Lane root
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Date: 2026-10-21. Item: re-open S071
(`https://docs.python.org/3/library/json.html`) live, record access date/HTTP status/byte size/sha256,
audit `scope`, `anchor`, `teaches` and the remaining cells against the live bytes, and re-locate/count the
build seat's quote.

Read-only leaf: no production, fixture, corpus, SOURCES, SCORECARD or candidate edit; no lane git
mutation; no subagents; no installs or updates. Writes: this report plus scratch under
`/tmp/freopens071` (page body and quote file). No credentials, cookies, auth state, env values or private
URLs were read or recorded.

Independence: I did **not** read or import `plans/config_projection.py`. The only touch was a literal
`grep -rn "S071" plans/config_projection.py`, which returned no lines. Inputs used: the row text at
`corpus/SOURCES.md:93`, the build report `.ufo/waves/round-29/build/R29SourceJsonDocs.md`, the candidate
draft's two S071 mentions, live docs bytes, and the earlier same-page capture at
`.ufo/waves/round-28/scratch/OpenS059/pyjson.html`.

## Target and revision

- Row: `corpus/SOURCES.md:93`, 832 bytes. The registry has 73 unique S-numbered rows; `S071` occurs once.
  Lane HEAD `56fd949a6478342531e61f4feecb4a685d831640`; the SOURCES blob at HEAD and in the worktree is
  `a295b7c2ea018c418b4a9a4eb68221d3c28c652eec3b8a8f4a9a9fce06b89b95`. The row landed in `b98dcf3`,
  an ancestor of HEAD.
- Build proposal: `R29SourceJsonDocs.md`. The `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`,
  `opened` and `recheck` cells are byte-identical to the integrated row. Only `status`
  (`mined (proposed; L1 decides)` → `queued`) and `used-by` (`— (pending; ...)` → `—`) differ; these are
  the stated L1 decisions, not source changes.
- Candidate draft: `.ufo/waves/round-29/drafts/webarena-config-projection.md` cites S071 at draft line 1
  (`Character Encodings and loads`) and line 30 (invalid-document rejection). `used-by: —` is consistent
  with the unadmitted draft; `corpus/knowledge/webarena-config-projection.md` is absent.

## Live fetch (observed)

Command (scratch only):

```text
curl -sS -L -o /tmp/freopens071/json.html -w 'HTTP_STATUS=%{http_code}\nSIZE=%{size_download}\nTYPE=%{content_type}\n' \
  --max-time 60 https://docs.python.org/3/library/json.html
HTTP_STATUS=200
SIZE=115104
TYPE=text/html
sha256sum /tmp/freopens071/json.html
7197009d47b8a44ce5a8c22b8c70ab5f754fd479cb30268284b0da84a9d1f8fb  json.html
stat -c '%s bytes' /tmp/freopens071/json.html
115104 bytes
date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-21T16:47:23Z
```

HEAD at `2026-10-21T16:49:23Z`: `HTTP/2 200`, `content-type: text/html`,
`content-length: 115104`, `last-modified: Wed, 21 Oct 2026 13:04:29 GMT`, ETag `"6ad8b85d-1c1a0"`,
cache `HIT, HIT`.

| item | observed |
|---|---|
| URL / effective URL | `https://docs.python.org/3/library/json.html` |
| access date | 2026-10-21 (body fetch 16:47:23Z; HEAD 16:49:23Z) |
| HTTP status | 200 (`HTTP/2`, text/html) |
| byte size | 115104 bytes (body and `content-length` agree) |
| sha256 | `7197009d47b8a44ce5a8c22b8c70ab5f754fd479cb30268284b0da84a9d1f8fb` |
| title | `json — JSON encoder and decoder — Python 3.15.1 documentation` (rendered line 17) |
| canonical link | `https://docs.python.org/3/library/json.html` |
| footer | `Last updated on Oct 21, 2026 (13:02 UTC).` (rendered line 761) |

The prior same-page capture `.ufo/waves/round-28/scratch/OpenS059/pyjson.html` is 115104 bytes with the
same sha256 `7197009d…f8fb`; today's bytes are byte-identical to it. That is a same-day stability
observation, not an independent mirror.

Line-number basis: the row's numbers are the harness rendered-text positions (768 rendered lines), as the
build report states. Raw HTML is 1212 lines; the quoted sentence is raw lines 859-860 and the
`id="character-encodings"` section starts raw line 854. I reproduced the rendered numbers with the
harness `read`/`grep` on the URL; I did not use a raw-line claim for any row cell.

## Cell audit

### source, kind, tier, id

- `source`: URL live 200; rendered title and canonical URL match. Supported.
- `kind: docs`, `tier: A`: official Python documentation is tier A for the module's documented behavior,
  which the row's `scope` narrows to. Supported. The page is the same base URL as S052 and S065 with
  different section anchors; the build report names that overlap (see N6).
- `id`: S071 appears once in the registry; no duplicate row.

### scope

Row bytes (18 words):

`documented default serialization escaping and deserialization rejection of stdlib json 3.15.1; not generated config values, deployment, or runtime`

Live: the page is Python 3.15.1; it documents the default serializer escaping (rendered 581-582, 173,
254, 197-200), the invalid-document raise (402), and the initial-BOM raise (591). It documents no
generated config value, deployment setting or runtime behavior. The scope's positive statement is true
and its exclusions are correct. Coverage note N1: the scope does not name three clauses the `teaches`
cell also asserts.

### anchor

Row bytes (13 words):

`Python3.15.1, Character Encodings §576-591, escaped-output sentence581-582; dumps default254; invalid-document402; BOM591; duplicate last-wins624-625; opened2026-10-21`

Every stated locator reproduces exactly on today's rendered page:

| stated | live observation |
|---|---|
| `Python3.15.1` | title line 17; footer line 761; version is 3.15.1 |
| `Character Encodings §576-591` | heading `### Character Encodings` at 576; the cited escaped-output/BOM facts are within 581-591; section body actually continues to 596 (N3) |
| `escaped-output sentence581-582` | line 581 ends `…by default, thus escaping the output so that the resulting`; line 582 is `strings only contain printable ASCII characters.` |
| `dumps default254` | `json.dumps(…, ensure_ascii=True, …)` signature at 254 |
| `invalid-document402` | `If the data being deserialized is not a valid JSON document, a JSONDecodeError will be raised.` at 402 |
| `BOM591` | `This module’s deserializer raises a ValueError when an initial BOM is present.` at 591 |
| `duplicate last-wins624-625` | `…it ignores all but / the last name-value pair for a given name:` at 624-625 |
| `opened2026-10-21` | live fetch today, 2026-10-21 |

No stated anchor number is wrong. Coverage note N2: the anchor does not list the locations of three
taught clauses.

### teaches

The cell has six clauses; each is live-supported:

1. **Default `dump`/`dumps` escaping.** `json.dump` signature at 173 and `json.dumps` at 254 both show
   `ensure_ascii=True`; the parameter prose at 197-200 says the output is guaranteed to have incoming
   non-ASCII and non-printable characters escaped; 581-582 says the resulting strings only contain
   printable ASCII characters. Supported.
2. **`ensure_ascii=False` escape set.** Live 198-200 and 452-454: the characters that must be escaped are
   the quotation mark, reverse solidus, and the control characters `U+0000` through `U+001F`. The row's
   "escapes only" matches. Supported.
3. **`loads` input domain.** Live 337 (signature), 339-340 (`str`, `bytes` or `bytearray`), 342-345
   (versionchanged: input encoding should be UTF-8, UTF-16 or UTF-32; `encoding` removed in 3.9).
   Supported.
4. **Raises instead of repairing.** Live 402 (`JSONDecodeError` for an invalid document), 591
   (`ValueError` for an initial BOM), and 533 (`JSONDecodeError` subclasses `ValueError`). Supported.
5. **Duplicate names keep the last value.** Live 620-625: no exception; ignores all but the last
   name-value pair. Supported.
6. **Order is preserved.** Live 168-169: encoders and decoders preserve input and output order by default;
   order is lost only if the underlying containers are unordered. Supported as a default-behavior
   summary (N5).

No teaches clause widens the live text. The flat `order is preserved` omits the 169 caveat, and
`accepts … in UTF-8/16/32` compresses the page's `should be` guidance; both remain true as default
summaries (N5).

### status, opened, recheck, used-by

- `status: queued`, `opened: 2026-10-21`, `recheck: on-release`: consistent with the S070-S073 convention
  and the version-floating `/3/` URL; today's page is the 3.15.1 identity the row names.
- `used-by: —`: no `corpus/knowledge/` citation exists; the draft's S071 mention is pre-admission. The
  `corpus/SOURCES.md` convention in the wave context is `used-by` none until admission. Consistent.

## Build-seat quote (re-located and counted)

Quote as landed:

> thus escaping the output so that the resulting strings only contain printable ASCII characters.

- **Location:** rendered lines 581-582 (harness `read`/`grep`); raw HTML lines 859-860. It occurs once in
  the whitespace-normalized raw page.
- **Word count:** 14 by Python `str.split()` and 14 by `wc -w`; ≤25.
- **Bytes/hash:** 95 UTF-8 bytes, ASCII-only; sha256
  `ccdb630107e51b18d696d3f821a02c4ae84be5d497582cde5ae66515769f9d8e` over the quote text with no trailing
  newline. Both match the build report.
- **Line split:** 8 words (`thus escaping the output so that the resulting`) are on rendered line 581;
  6 words (`strings only contain printable ASCII characters.`) are on line 582.

The build report's 14-word count, 95-byte length, sha256, and 581-582 location are all exact. Its
sentence `the retained fragment is the part that wraps onto line 582` is accurate only as "the fragment
continues onto line 582": a line-582-only reading would be wrong because 8 of the 14 words are on line
581. The build report discloses that the fragment excludes the earlier clause naming `ensure_ascii=True`;
the located sentence includes that qualifier (N4).

## Coverage notes (not cell errors)

**N1 — scope does not name three taught clauses (medium, curation).** `scope` names serialization
escaping and deserialization rejection; `teaches` also asserts the `loads` input domain, duplicate
last-wins, and order preservation. All three are documented defaults on the same page (337-345, 624-625,
168-169) and the scope's exclusion list does not exclude them. [INFERENCE] A strict Q2 reading would
broaden the scope to "documented default serialization and deserialization behavior" at admission; this
is a coverage wording note, not a false cell. The candidate's load-bearing use (invalid-document
rejection) is inside the scope and anchored at 402/591.

**N2 — anchor selects, but does not locate, three taught clauses (low-medium, curation).** The anchor
lists 576-591, 581-582, 254, 402, 591, 624-625. It does not list 198-200/452-454 (`ensure_ascii=False`),
337-345 (`loads` input domain), 168-169 (order), or 533 (`JSONDecodeError` subclass). Every stated
number is exact and the missing lines are on the same page. [INFERENCE] This is a locator-selection gap,
not a false anchor; add those lines if the row is cited for those clauses.

**N3 — `Character Encodings §576-591` is the cited span, not the section extent (low, ambiguity).** The
live section runs 576-596 (surrogate paragraph 593-596; blank 597; next heading 598). Read as the whole
section, 576-591 is short by five lines; read as the escaped-output/BOM span, it is exact. [INFERENCE]
Clarify the anchor wording at admission.

**N4 — quote fragment is a mid-sentence tail (low, presentation).** The 14-word fragment starts at the
tail of line 581 (`thus escaping…`) and ends on 582; it omits the earlier clause naming
`ensure_ascii=True`. The build report discloses this and the located sentence includes the qualifier.
[INFERENCE] A 21-word clause including the qualifier would be self-contained and still ≤25.

**N5 — two compressions in `teaches` (low).** `order is preserved` omits the live 169 caveat
`Order is only lost if the underlying containers are unordered`; `loads` `in UTF-8/16/32` compresses the
live `The input encoding should be UTF-8, UTF-16 or UTF-32` (342-345). Both are default-behavior
summaries, not false claims.

**N6 — same-page rows not named in S071 (observation).** S052 and S065 use the same base URL with
different section fragments; the build report names them, the registry row does not. [INFERENCE] An
optional cohort note at admission, not a cell error.

**N7 — line basis is rendered text (observation).** The row's 576/581-582/591 etc. are harness
rendered-text lines (768 total), not raw HTML lines (1212 total; quote raw 859-860). The build report
states the rendered basis; the row does not. [INFERENCE] A raw-byte checker must use the rendered reader
or the `#character-encodings` fragment; not a false cell under the stated method.

**N8 — version boundary (observation/limit).** The page is Python 3.15.1; the host `python3 --version` is
3.14.8. The row scopes itself to the documented 3.15.1 behavior and does not claim the lane's runtime;
the build report preserves the projection's interpreter as unmeasured. [INFERENCE] The candidate's
rejection use is a documented-rule rationale inside the row's scope; whether the projection's interpreter
matches 3.15.1 is not established by this row and was not measured here.

## Limits and unknowns

- One endpoint, two GETs (body and HEAD); no mirror or independent timestamp. The `/3/` alias can drift;
  the row's `on-release` recheck is the control. Today's bytes match the earlier same-day round-28
  capture, but that is not a long-term pin.
- I did not execute `json`, the generator, or `plans/config_projection.py`; no runtime or deployment
  claim is made. The quote, cells and version identity are documentation observations only.
- The candidate's draft line 30 is a design rationale; I did not test profile-value JSON invalidity or
  the projection's output. That belongs to the projection/candidate seats.
- The build report's access date (2026-10-21) cannot be re-observed independently; my 2026-10-21 fetch is
  the live access record here.

## Verdict

All 11 row cells are supported against today's live page; every stated anchor line number is exact; the
build quote is 14 words, 95 bytes, sha256 `ccdb6301…f9d8e`, and located at rendered 581-582. I found no
wrong cell and no unsupported cell. N1-N8 are scope/anchor coverage, wording, line-basis and version
observations for L1, not contradictions with the live bytes. The row's candidate use (invalid-document
rejection) is inside its scope and anchored. This is a scoped source-row verdict, not a round admission.

VERDICT: PASS

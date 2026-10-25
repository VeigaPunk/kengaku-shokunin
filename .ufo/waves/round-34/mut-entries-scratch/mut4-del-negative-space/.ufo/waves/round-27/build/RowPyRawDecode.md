# RowPyRawDecode — round 27 (read-only seat; no lane writes)

Base read: lane HEAD 11a7fc8 (pre-registration `plans/round-27-claims.md`). Seat did not clone; no product or corpus file touched.

## Source opened (2026-10-21)
- URL: https://docs.python.org/3/library/json.html — page title "json — JSON encoder and decoder — Python 3.15.0 documentation".
- Saved bytes: /tmp/kengaku-r27-RowPyRawDecode/json-3.html, 115104 bytes, sha256 `390c826f16e9d7350d09f87d06bec2d5d2adff8b09fd09c949611054eadfc383` (curl, UA Mozilla/5.0).
- Location: method `json.JSONDecoder.raw_decode(s)` at json-3.html:650; prose at :652-656.
- Local check (not doc evidence; Python 3.14.8, PYTHONDONTWRITEBYTECODE=1): `raw_decode('{"a":1} trailing text')` returned `({'a': 1}, 7)`; `raw_decode(' {"a":1}')` raised JSONDecodeError "Expecting value … char 0". The doc says "beginning with"; it does not state the leading-whitespace case.

## (1) SOURCES.md contract-v1 row (draft; id left as S0xx)

Cells split by `|` give 13 pieces including empty edges, matching existing rows (S001 at corpus/SOURCES.md:23 has 11 real columns).

| S0xx | Python json — JSONDecoder.raw_decode(s) — https://docs.python.org/3/library/json.html | docs | A | what Python's json docs say raw_decode(s) returns and tolerates, not answer-extraction policy in general | json.JSONDecoder → raw_decode(s), anchor json.JSONDecoder.raw_decode (saved html :650-656); Python 3.15.0 docs, opened 2026-10-21 | raw_decode decodes one JSON document starting at the string's beginning and returns (object, end index); extraneous data after the document is allowed; the page says nothing about scan start positions or candidate choice | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |

## (2) gate.md lines (URL · access date · version · location · quote)
- `S0xx | https://docs.python.org/3/library/json.html | accessed 2026-10-21 | Python 3.15.0 docs | JSONDecoder.raw_decode, html :653-654 (method def html :650) | "return a 2-tuple of the Python representation and the index in s where the document ended." (16 words)`
- `S0xx | https://docs.python.org/3/library/json.html | accessed 2026-10-21 | Python 3.15.0 docs | JSONDecoder.raw_decode, html :655-656 | "This can be used to decode a JSON document from a string that may have extraneous data at the end." (20 words)`
- Supporting, for E7 unbounded nesting (module Warning admonition): `S0xx | https://docs.python.org/3/library/json.html | accessed 2026-10-21 | Python 3.15.0 docs | module Warning, html :248 | "A malicious JSON string may cause the decoder to consume considerable CPU and memory resources." (16 words)`

Saved-bytes line numbers were checked by reading /tmp/kengaku-r27-RowPyRawDecode/json-3.html:649-660 after the first draft.

## (3) Policy grounding
- Grounds **E7** (decode-first) and **E8** (decode-last): the doc licenses calling raw_decode on a string with trailing text and getting the end index back.
- Does NOT ground: the left→right `{`/`[` scan, first-vs-last selection, E8's skip-contained-spans rule, or any nesting limit. Those are lane design; E7/E8 rows should cite the lane's own `plans/parser_policy_compare.py` once it exists, not this row.
- Other policies E0–E6: none.

## Notes for the integrator
- Next id: corpus/SOURCES.md's last row is S048 (line 70), so S049 is free; the seat left the id as S0xx per assignment.
- The scope cell is narrow on purpose: "tolerates trailing data" is documented; "first-match vs last-match policy" is not.
- The Warning quote is a safety note about untrusted input. It supports only the observation that unbounded nesting in E7/E8 is a CPU/memory concern.

## Installs / tool changes
- None. Used system curl and the local python3 3.14.8 (stdlib only) for the one-off check.

## Files written
- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/build/RowPyRawDecode.md (this report; rewritten once after a mis-targeted edit corrupted the first draft).
- /tmp/kengaku-r27-RowPyRawDecode/json-3.html (scratch, sha256 above).

VERDICT: Opened json docs (Python 3.15.0); raw_decode documents trailing-data tolerance, which grounds E7/E8 only. Output: one S0xx row, two gate quotes, one supporting quote; no lane writes, no installs.

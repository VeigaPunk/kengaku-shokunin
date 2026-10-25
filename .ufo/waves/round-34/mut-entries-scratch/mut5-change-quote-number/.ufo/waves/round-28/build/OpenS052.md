# OpenS052 — round 28 source re-open (author-side, read-only seat)

Writer/seat: `KengakuR28.OpenS052-2` (scout, read-only). Scope: S052 only. Author-side advice, not outside
non-author closure. No registry, knowledge or production edits; scratch evidence only under
`.ufo/waves/round-28/scratch/OpenS052/`. No installs or updates. No REA MCP. No benchmark-site contact.

S038 and S056 instructions in the shared assignment template belong to their own seats (`OpenS038-2`,
`OpenS056-2`); they were not opened here and nothing is claimed about them.

## Registry row under review (unchanged, `corpus/SOURCES.md:74`)

Identical at baseline `b9b24796…` (`git show b9b2479:corpus/SOURCES.md`, line 74) and at the current tree.
Immutable cells: source/kind `docs`/tier `A`/scope "decoder return value and trailing-data tolerance, not
candidate selection"/anchor "Python 3.15.0 documentation, JSONDecoder.raw_decode"/teaches. Mutable cells:
status `mined`, opened `2026-10-21`, recheck `on-release`, used-by
`corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`.

## Source opening

- URL: https://docs.python.org/3/library/json.html#json.JSONDecoder.raw_decode — accessed 2026-10-21, HTTP 200,
  115104 bytes, sha256 `7197009d47b8a44ce5a8c22b8c70ab5f754fd479cb30268284b0da84a9d1f8fb`
  (`scratch/OpenS052/json.html`). Page title: "json — JSON encoder and decoder — Python 3.15.1 documentation".
- Located quote 1 (return value, 24 words), `raw_decode(s)` entry:
  “Decode a JSON document from s (a str beginning with a JSON document) and return a 2-tuple of the Python
  representation and the index in s where the document ended.”
- Located quote 2 (trailing-data tolerance, 20 words), same entry:
  “This can be used to decode a JSON document from a string that may have extraneous data at the end.”
- Version cross-check: CPython `Doc/library/json.rst` fetched at tags `v3.15.0` and `v3.15.1`
  (raw.githubusercontent.com/python/cpython/<tag>/Doc/library/json.rst, 2026-10-21, HTTP 200 each).
  The two files are byte-identical (sha256 `64429e9269df70c75e66d3588f22d59412fe1b93019c4bcf70075a91bbdc7622`).
  The `.. method:: raw_decode(s)` text sits at lines 469–476 in both.

## Teaches/anchor confirmation

- Observed: the official docs state that the method returns a pair: the decoded object and the end index. They
  also say it tolerates extraneous trailing data. This matches the row's teaches and scope exactly.
- Observed: the docs say nothing about brace/bracket scanning, choosing the first or last candidate, or skipping
  starts that fall inside an already-decoded span. The row's statement that these are the lane's own design
  is therefore correct and properly narrow.
- Observed nuance (no change required): the docs require `s` to *begin* with a JSON document. So the
  primitive does not tolerate leading data. That is consistent with E7/E8 scanning brace positions first,
  and it is already covered by "lane-defined scan".
- Anchor drift: the live page now serves 3.15.1, while the anchor says 3.15.0. The `on-release` recheck was
  therefore triggered. The raw_decode text, and the whole `json.rst`, are unchanged between the two releases,
  so the anchor stays accurate for its claim. Anchor is an immutable cell, so no edit is suggested.
- Tier A is justified: this is official language documentation for its own API, within the stated scope.

## Literal citations in the frozen 35-file population

Method: `plans/fixtures/r28/registry/population.json` `reference_pattern`
`(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`, matched exactly against `S052` across all 35 `knowledge_paths`
(stdlib Python read-only scan).

| path | line | context |
|---|---|---|
| `corpus/knowledge/extraction-policy-comparison.md` | 1 | `source:` line: "S052 https://docs.python.org/3/library/json.html#json.JSONDecoder.raw_decode" |
| `corpus/knowledge/extraction-policy-comparison.md` | 49 | "E7/E8 use Python's decoder primitive (S052), but their scan and selection rules are lane-defined." |

No other frozen file mentions S052. Set of citing frozen paths = {`corpus/knowledge/extraction-policy-comparison.md`}.
Outside the population (allowed extra used-by path): `corpus/lessons/round-27.md` lines 45, 57 and 201. Line 201
records the round-27 used-by change old→new; status and recheck were left unchanged.

Usage check: line 49 attributes only "decoder primitive" to S052 and gives the scan/selection rules to the lane.
That is consistent with the row's scope. This is structural/literal evidence, not a semantic endorsement.

## Comparison against existing mutable cells

- status `mined`: S052 is cited by a frozen path, so it must be `mined`, and it is. OK.
- used-by: lists every citing frozen path (`extraction-policy-comparison.md`) plus the lesson. OK, no missing path.
- opened `2026-10-21`: matches today's re-open. OK.
- recheck `on-release`: still the right cadence for versioned docs. The 3.15.1 release triggered it, and this
  re-open has now performed it with no content change. OK.

Suggested allowed mutable-cell changes: **none**. S052 has no cited-but-queued or missing-used-by drift. The
C2 checker should report S052 as clean on both the baseline and the final tree. [INFERENCE: this follows from
the frozen contract in `plans/round-28-claims.md:9,25`; the delivered `registry_check.py` was not run.]
If L1 wants the re-open recorded, the round-28 lesson could note "S052 reopened 2026-10-21 against 3.15.1;
text identical to 3.15.0; cells unchanged". That would be a lesson note, not a registry delta.

## Commands observed

`rg`/`sed`/`git show b9b2479:corpus/SOURCES.md`; a stdlib Python population scan; `curl` of the docs page and of
the two CPython tag `json.rst` files; `sha256sum`; `diff` (output: RAW_DECODE_IDENTICAL).

## Limitations

- Only the page and the CPython doc source were opened. CPython's `json/decoder.py` implementation was not
  inspected (its undocumented `idx` parameter is out of scope).
- Literal coverage on the frozen population only. This is not semantic citation support for the
  extraction-policy entry as a whole.
- `registry_check.py` was not run (no checks mid-flight).

## Verdict

**PASS (scoped to S052):** the source was reopened at its primary URL; the narrow teaches/scope/anchor were
confirmed, and the 3.15.0→3.15.1 drift was verified to leave the content unchanged; the frozen literal citations
(one file, two mentions) are fully covered by `mined` status and used-by. No mutable-cell change is warranted.
This is not a round-level PASS.

# OpenS059 — reopening S059 (RFC 8259 §6 Numbers)

Writer/seat: `KengakuR28.OpenS059-2` (read-only scout, author-side advice; not outside non-author closure).
Scope: re-open existing row S059 only; C2 literal-reference check for S059 within the frozen 35-path population.
The S056 and S038 instructions in the brief refer to other rows/seats. I did not open those rows and make no claim about them.
Lane HEAD at reading: `f0ba09be0f3066daba2134b943d973ad1588f34a`. `git diff --stat b9b24796… -- corpus/SOURCES.md corpus/knowledge/extraction-policy-comparison.md corpus/lessons/round-27.md` returned empty, so those files match the baseline.

## Row under audit (corpus/SOURCES.md:81, unchanged)

`| S059 | RFC 8259 numeric grammar (extends S053 anchor) — https://www.rfc-editor.org/rfc/rfc8259 | spec | A | RFC JSON numeric restrictions versus Python decoder extensions | §6 Numbers, txt:377–378; independent reread FSourceS053 | extends S053's §2 grammar/whitespace scope: NaN and Infinity are not permitted JSON numbers, although Python decoder accepts them by default; E4 is Python-whole, not RFC-strict | mined | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |`

## Opening (2026-10-21)

Commands I ran (scratch: `.ufo/waves/round-28/scratch/OpenS059/`):
- `curl -sS -L https://www.rfc-editor.org/rfc/rfc8259.txt`: HTTP 200, 899 lines, sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`. This is **identical** to the hash recorded in `corpus/evidence/round27-sources/gate.md:46`.
- `curl -sS -L https://www.rfc-editor.org/rfc/rfc8259` (the exact row URL): HTTP 200 after a redirect to `https://www.rfc-editor.org/info/rfc8259/`. The page title is "RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format", with `citation_doi` 10.17487/RFC8259 and publication date 2017/12/13. The rendered body contains the same §6 sentence (html line 495). sha256 `c813c1125b9b…f57`. This is a dynamic page, so its hash is not stable evidence; the .txt hash is the stable one.
- Header (txt:8–9): "Request for Comments: 8259 … Obsoletes: 7159 … December 2017"; Standards Track.

Located quote, URL https://www.rfc-editor.org/rfc/rfc8259 (.txt rendering), §6 Numbers, txt:377–378, accessed 2026-10-21:
> "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted."

That is 18 words. The anchor `§6 Numbers, txt:377–378` is **exact**: line 377 is "Numeric values … (such", and line 378 is "as Infinity and NaN) are not permitted.". The grammar `number = [ minus ] int [ frac ] [ exp ]` follows at txt:380. The quote matches round-27 lesson line 52 and gate.md:44–46 verbatim.

## Teaches/scope check (narrow)

The teaches cell makes three claims, and RFC 8259 supports only one of them:
1. **"NaN and Infinity are not permitted JSON numbers"**: directly supported by the RFC (quote above). Tier A spec within this scope is appropriate.
2. **"although Python decoder accepts them by default"**: RFC 8259 does not say this. I checked a separate source: https://docs.python.org/3/library/json.html, HTTP 200, accessed 2026-10-21, sha256 `7197009d…f8fb`. In section `#infinite-and-nan-number-values` (html:876–879) it says: "Despite that, by default, this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values" (19 words). The claim is therefore true, but its authority is the Python documentation page (the same page as S052's URL). S059's anchor and S052's `raw_decode` anchor both miss it.
3. **"E4 is Python-whole, not RFC-strict"**: this is a lane-internal inference from claims 1 and 2 together with the policy definition. It is not RFC content.

So the row's scope ("RFC JSON numeric restrictions versus Python decoder extensions") is a comparison, and only the RFC half has an opened anchor in the row. [INFERENCE] This is a calibration nuance, not an error: the comparison is correct, and the Python half was verified today.
- Scope, anchor and teaches are not mutable cells under the round-28 contract, so I propose **no edit** to them.
- Optional and not requested: L1 could record this note in the round-28 lesson. If a separate anchor is ever wanted, it would belong to a new row or an S052 correction, which needs its own opening. Seats may not add rows.

The kind/tier "spec/A" is correct for the RFC half. Round-27 census W04 ("S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes", `corpus/evidence/round27-calibration/sources-census-final.txt:6`) remains a known, intended duplicate. S053 (§2) and S059 (§6) are distinct anchors of one RFC.

## C2 literal-reference check for S059

I applied the frozen `reference_pattern` from `plans/fixtures/r28/registry/population.json` to all 35 `knowledge_paths`. I used an inline stdlib regex scan; this is not `registry_check.py`, which is not used or read here.
- `corpus/knowledge/extraction-policy-comparison.md:1`: provenance header "S053/S059 https://www.rfc-editor.org/rfc/rfc8259 §2/§6".
- `corpus/knowledge/extraction-policy-comparison.md:53`: "unlike RFC8259 §6 (S059): “strict-whole” means whole-output Python decoding, not RFC-strict syntax."
- Total: 2 mentions in 1 frozen file; 0 in the other 34.

Other S059 mentions exist outside the frozen population and do not count for C2: `corpus/README.md:63,233` (range "S049,S051–S059"), `corpus/lessons/round-27.md`, `corpus/evidence/round27-*`.

Comparison with the row:

| check | observed |
|---|---|
| citing frozen files | `corpus/knowledge/extraction-policy-comparison.md` |
| used-by | `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md` |
| missing_used_by | none |
| status | `mined` (as required for a cited row) |
| recheck | 2027-01-19 (not yet due) |

The extra lesson path is allowed by the contract. The used-by provenance is the lesson round-27.md:201–202 (old `corpus/lessons/round-27.md` changed to the current two-path value; status/recheck unchanged).

**Suggested mutable-cell changes: none.** The status, recheck and used-by cells are already consistent with today's opening and the frozen citations. Because the source was reopened today with an unchanged hash, an `opened`/`recheck` refresh is possible only if L1's convention counts reopenings. The contract does not require it, and I do not recommend it as a C2 repair because there is no mismatch to repair.

Semantic side note, outside C2's literal contract: at knowledge line 52–53, "Python also accepts NaN/Infinity by default" is attributed only by proximity to S059/RFC. The supporting Python documentation is not cited in that sentence; the nearest S052 citation is at line 49. This is not a literal-coverage finding and calls for no registry change.

## Limitations

- RFC errata were not checked. The .txt reflects the published RFC; for this sentence I found no errata claim either way.
- HTML hashes are volatile. I made no use of Python behavior beyond the documentation text: no Python decoding experiment was run.
- I made no installs or updates, did not edit the registry, and did not touch any production file.

## Verdict

**PASS (scoped)** for: the S059 reopening (URL live, .txt hash identical to round-27, anchor txt:377–378 exact, quote located), the RFC half of teaches, and C2 literal coverage for S059 (1 citing frozen file, covered, `mined`, no mutable-cell change needed).
**PARTIAL** on the teaches cell's Python-default clause: it is true per the Python documentation (opened today), but it is not supported by S059's own source or anchor. I recommend disclosure only, with no cell change.
This is not a round, C2-wide, or semantic-citation PASS.

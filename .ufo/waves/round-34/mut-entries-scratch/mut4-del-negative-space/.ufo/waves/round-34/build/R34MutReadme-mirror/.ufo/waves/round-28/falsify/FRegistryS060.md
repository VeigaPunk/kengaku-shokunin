# FRegistryS060 — author-side falsification of row S060 under the frozen13/35 literal contract

- Seat: `KengakuR28.FRegistryS060` (leaf revenger, calibration axis). Date: 2026-10-21.
- Scope: row **S060 only**, under `plans/fixtures/r28/registry/population.json` (sha256 `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014`, base_revision `b9b24796277020d1b9b01923b45313d6a565e664`). This is a frozen literal-reference finding, **not** a whole-registry truth claim and **not** a whole-current-tree claim.
- Anchors: lane HEAD `18b192266389e8d6c74d0e1f1f2db337739e63dd` (round-28 build, landed); current-tree `corpus/SOURCES.md` sha256 `014175dd88f679a23b0f70f88ef10332007b554c88684ba4d0e1532812c619a1`.

## Method (independent; no production import in derivation)

1. Own parser + own regex (`(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`; S060-specific `(?<![A-Za-z0-9_])S060(?![A-Za-z0-9_])`) re-derived from `plans/registry_check.py` source text and `population.json`; registry rows, 35 frozen knowledge paths, and the used-by target parsed directly from the working tree and from `git show b9b24796…:<path>` (read-only). Baseline knowledge paths all present at base (0 missing).
2. Lane checker probe (explicitly permitted): `python3 -B plans/registry_check.py --json` (bytecode disabled, read-only, exit 0). Delivered output saved at scratch `checker-current.json`.
3. Scratch mutation probe (explicitly permitted): falsifier tree under own scratch, checker run with `--root` pointing there. Production untouched.

An early census pass of mine double-counted (counted any `S\d{3,}` token instead of per-ID); it was discarded and redone per-ID. Only the corrected artifacts are retained in scratch.

## Row identity (S060)

`corpus/SOURCES.md:82`, inside `## Registry`, 11 cells, read 2026-10-21:

`| S060 | json-repair 0.64.1 — https://pypi.org/project/json-repair/ | tool | B | the community package's documented/probed repair semantics as an excluded round-27 policy candidate, not independent validation | PyPI summary and README; wheel SHA2561e1022f8…b9e0a | REJECTED for this frozen stdlib-only E0–E8 comparison: repairs add semantics and an unfrozen dependency; flip: separately preregister a pinned repair policy, its truth-sensitive controls and an independent oracle without rewriting this round's eight-policy denominator | rejected | 2026-10-21 | 90d | corpus/lessons/round-27.md |`

- Row line bytes (sed 82p) sha256: current `ed2f59def07205dcb5dc6cefc75b31f8a29ed59bd156314871c4cadf0f4baf34` == baseline `ed2f59def07205dcb5dc6cefc75b31f8a29ed59bd156314871c4cadf0f4baf34` → **byte-identical baseline↔current**.
- Used-by target `corpus/lessons/round-27.md` sha256 `a15cf0b98f99ba7c978fc178cb8a5f541ab34820a340f179cc82d28b0022c254` at both current and baseline → **identical**; it cites S060 at lines 36, 53, 188, 203 in both revisions (verified).

## Expected-before (b9b2479) / current-after (18b1922) — S060

| facet | expected-before | current-after | delta |
|---|---|---|---|
| row bytes @SOURCES.md:82 | sha `ed2f59de…` | same | none |
| status / tier / kind | rejected / B / tool | same | none |
| citing set in 35 frozen paths | ∅ (0 standalone S060 hits) | ∅ (0 hits) | none |
| used_by | `corpus/lessons/round-27.md` (exists, safe path) | same | none |
| missing_used_by | ∅ | ∅ | none |
| findings | **∅** | **∅** | none |

Missing/corrective/code-reference check: zero standalone `S060` tokens anywhere in the 35 frozen knowledge paths, current and baseline — hence no missing link, no corrective-mention edge, and no code-fence edge (literal contract counts fences; there is simply nothing to count). Boundary stress: no longer `S060`-prefixed tokens (e.g. `S0600`), no case-variant standalone tokens; `anomalous_files` = {} (scratch `census-s060-v2.json`).

**Exact effective denominator for S060:** 1 of 13 frozen source rows; 35 file×row literal link opportunities → **0 formed citing links** (population-wide links are 12, none owned by S060); plus 4 structural checks per row, all pass: 11-cell parse, enum check (tool∈KINDS, B∈{A,B,C}, rejected∈{queued,mined,rejected}; community-A rule n/a), used-by path safety+existence (1 path, exists), subset used-by coverage (citing ∅ ⊆ used_by; subset, not equality — the lesson-only used-by path is an explicitly permitted additional lesson path per population note and claims:25). `cited_not_mined` is vacuous because the citing set is empty; an uncited rejected row is not an error.

## Delivered vs derived (checker comparison)

Lane checker (exit 0, finding_count 0, reference_links 12, mismatch_sources 0) per-row S060 output:

```json
{"source":"S060","status":"rejected","citing_files":[],"used_by":["corpus/lessons/round-27.md"],"missing_used_by":[]}
```

Byte-for-byte equal to my independently derived map. Full 13-row map (my derivation, baseline→current findings):

| row | expected-before findings (b9b2479) | current-after findings (18b1922) |
|---|---|---|
| S038 | cited_not_mined; missing_used_by:attribution-interval-calibration | ∅ |
| S049 | ∅ | ∅ |
| S050 | missing_used_by:extraction-policy-comparison | ∅ |
| S051–S059 | ∅ (each cites extraction-policy-comparison, listed in used_by) | ∅ |
| **S060** | **∅** | **∅** |

Baseline reproduces exactly 2 mismatch rows (S038, S050) → final 0; total links 12 at both revisions (S038×attribution-interval-calibration + S049–S059×extraction-policy-comparison). Context match: C2 frozen13 / 35 paths / 12 literal row-file links, baseline2→final0.

## Boundary notes (disclosed context, not my discovery, not support)

- S038 queued/cited drift and its status/used-by repair delta are **already-disclosed drift**; my map only reproduces them as expected-before vs current-after. Not claimed as a finding.
- S050's corrective-index reversal is disclosed; S058 controls the no-hit-reason correction. The S050 delta in my table is the disclosed used-by repair. It is **NOT** support for any superseded-reason claim, and nothing here re-opens S050. S060's rejection reason stands on its own row text and `corpus/lessons/round-27.md:36` (reject: frozen eight-policy denominator, stdlib constraint, repair-vs-span-selection semantics).
- Out-of-population S060 mentions (not contract inputs, noted only): `corpus/SOURCES.md:82` (the row itself), `corpus/lessons/round-27.md:36,53,188,203` (the permitted used-by target), `corpus/evidence/round27-sources/gate.md:53` and `corpus/README.md:306` ("S049–S060"). None are among the 35 frozen knowledge paths.
- Source quote provenance: the PyPI summary “A package to repair broken json strings” is recorded at `corpus/lessons/round-27.md:53` and `corpus/evidence/round27-sources/gate.md:54` (URL https://pypi.org/project/json-repair/, accessed 2026-10-21, version 0.64.1). This seat did not re-open PyPI; the opening is OpenS060's, and this seat's scope is the registry/source-file contract, which those files satisfy.

## Row-specific falsifier (executed)

**Falsifier:** if any one of the 35 frozen knowledge paths contained a single standalone `S060` token, S060 — status `rejected`, used_by lacking that path — must flip from clean to exactly two findings: `cited_not_mined` and `missing_used_by:<that path>`. **Executed** in scratch (`falsifier-tree2`): control copy → 0 findings, 12 links; append one probe line citing `S060` to `corpus/knowledge/extraction-policy-comparison.md` → exactly `{cited_not_mined(S060), missing_used_by(S060, extraction-policy-comparison.md)}`, links 12→13. The check is therefore discriminating for S060, not vacuous. No such token exists in the real tree (current or baseline), so the falsification attempt **fails to break** the delivered S060 state.

## Tooling record

No tool installed or updated (none needed). Checker and probes ran `python3 -B`; `git show`/`rev-parse` read-only. All writes confined to this report and `.ufo/waves/round-28/scratch/FRegistryS060/` (retained: `census-s060-v2.json`, `checker-current.json`, `checker-current.err`, `SOURCES.current.md`, `SOURCES.baseline.md`, `falsifier-probe-clean.json`, `falsifier-tree2/`). Superseded buggy first-pass artifacts deleted. No production file, registry cell, fixture, or candidate byte touched.

## Finding

Row S060 is contract-clean under the frozen13/35 literal diagnostic at both revisions: uncited by all 35 frozen knowledge paths (expected-before ∅ → current-after ∅, zero row-specific delta), `rejected` status correctly non-triggering, lesson-only used-by target present and identical at base and HEAD, and the delivered checker per-row output exactly equals the independently derived map.

VERDICT: PASS

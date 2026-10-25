# FRegistryS054 — S054 frozen literal-reference check

## Scope and evidence

This is a row-only reading of the frozen C2 contract: the checker instrument at `plans/registry_check.py` and the pinned population at `plans/fixtures/r28/registry/population.json` (base `b9b24796277020d1b9b01923b45313d6a565e664`; 13 IDs, 35 knowledge paths). The reference regex is `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`. The checker deduplicates matches within each file and checks literal file coverage, row status/enums, and used-by path liveness; it is expressly not a citation-truth or whole-tree verifier.

I derived the S054 map from baseline `git show b9b24796277020d1b9b01923b45313d6a565e664:corpus/SOURCES.md` and the baseline frozen knowledge file, then directly read final `corpus/SOURCES.md`, `corpus/knowledge/extraction-policy-comparison.md`, and `corpus/lessons/round-27.md`. Only after that independent derivation, I ran `PYTHONDONTWRITEBYTECODE=1 python3 plans/registry_check.py --json` read-only as a comparison. Its current per-row S054 record agrees with the independent map.

## S054 result: expected before / observed after

| | Baseline b9b2479 | Current tree |
|---|---|---|
| Registry row | `S054`, kind `spec`, tier `A`, status `mined` | Same |
| `used_by` | `corpus/lessons/round-27.md`; `corpus/knowledge/extraction-policy-comparison.md` | Same |
| Frozen `citing_files` | `corpus/knowledge/extraction-policy-comparison.md` | Same |
| `missing_used_by` / row finding | empty / none | empty / none |

The current checker output gives S054 status `mined`, that single frozen citing file, both listed `used_by` paths, and an empty `missing_used_by`. The baseline source row has the same status and paths. The round-27 lesson path is a valid listed use, but is not a member of the frozen 35 knowledge-path population and therefore adds no C2 citing link.

The S054 token occurs three times in the frozen extraction-policy entry (provenance header, E6 limitation, and the later S064 correction). Under the checker contract these are **one** S054-to-file link, not three. The baseline row already lists that file; no S054 used-by repair is needed.

## Denominator and neighboring findings

Effective population: **13 source rows × 35 frozen knowledge paths**; **12 distinct source-ID/file links** across **2 citing files** (attribution calibration and extraction-policy comparison). Thus 33 frozen paths have no link; S060 is the one uncited frozen source row. These are source/file pairs after per-file ID-set deduplication, not token-occurrence counts or a 13-row citation denominator. S054 contributes exactly one of the 12 links.

The recorded baseline whole-check output has three findings, none for S054: S038 `cited_not_mined` plus `missing_used_by`, and S050 `missing_used_by`. The current output has zero findings. S038's baseline drift was already disclosed and is not a new discovery here. The S050 used-by addition indexes its corrective mention in the frozen extraction-policy file; it is **not** support for S050's superseded blanket no-match reason—S058 remains controlling. These neighboring rows do not alter the S054 result.

## One row-specific falsifier, bounded separately from C2

The S054 `teaches` wording says closing fences “must match opening type/length.” Round-28's reopened-source correction S064 states the precise rule: same fence character type and closing length **at least** the opening length, not necessarily equal; round-28 lesson M68 explicitly says S064 supersedes S054's ambiguous shorthand. This falsifies an exact-equal-length reading of S054's shorthand. It is a source-content correction already disclosed in the tree, **not** a frozen literal-reference finding: the S054 citation remains present and indexed correctly, and the literal checker cannot certify semantic support.

## Boundaries and confidence

No whole-registry truth, whole-current-tree, or source-support claim follows. The canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` is not admitted; the frozen draft is `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` (context-pinned SHA-256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a`). This report does not evaluate Q10 candidate completeness or admission.

Confidence: **high** for the S054 literal status/reference/used-by result and the row-file denominator (direct baseline/final files plus matching read-only checker output); **high** that the S064 correction is recorded as the specific shorthand correction, based on the opened round-28 source/lesson entries. No tools were installed or updated.

**VERDICT: PASS — S054 only, under the frozen13/35 literal-reference contract.**
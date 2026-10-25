# FRegistryS055 — bounded literal row falsification

**Axis:** calibration. **Scope:** S055 only, under the frozen13/35 literal contract. This is not citation-truth validation or a whole-registry/current-tree verdict.

## Contract and evidence

- Read `plans/registry_check.py` and `plans/fixtures/r28/registry/population.json` directly. The pinned population is base revision `b9b24796277020d1b9b01923b45313d6a565e664`, 13 IDs including S055, 35 explicit knowledge paths, population SHA-256 `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014`.
- Independently parsed `corpus/SOURCES.md` and each frozen file at baseline using `git show <revision>:<path>`, then the current files; did not import the production checker for this derivation. Baseline and current `SOURCES.md` SHA-256: `b1a74eb5f1cdbefa8e055cfee79dda7894a4b00a611788c3798140596258c62e` and `014175dd88f679a23b0f70f88ef10332007b554c88684ba4d0e1532812c619a1` respectively. Exact S055 row cells are unchanged.
- Checker semantics relevant here: source-row parsing is restricted to `## Registry` and 11-cell rows; it scans all text of each frozen knowledge file with the declared standalone-ID regex and deduplicates per source/file. It does not suppress inline/code/fenced mentions in those knowledge files. Cited rows must be `mined`; each `used-by` path must be safe and exist.
- No LSP device/server was exposed in the available session tools. Literal searches below establish occurrence locations only, not semantic source support.

## S055 expected-before / current-after

| State | Row/status and used-by | Frozen S055 citing set | S055-specific findings |
|---|---|---|---|
| Baseline `b9b2479…`, row 77 | `kind=code`, `tier=A`, `status=mined`; used-by = `corpus/lessons/round-27.md`, `corpus/knowledge/extraction-policy-comparison.md` | `corpus/knowledge/extraction-policy-comparison.md` | None: cited path is indexed; both used-by paths exist. |
| Current, row 77 | Same 11 cells and same `status=mined` / used-by values | Same one path | None: `missing_used_by=[]`; checker’s S055 finding projection is empty. |

Independent literal locations in `corpus/knowledge/extraction-policy-comparison.md` are identical at baseline and current: line 1 has one S055 source-list mention; line 20 has one `(S055 math_eval.py:53–54)` mention. Both are outside fenced blocks. Each counts literally; together they are **two token occurrences but one source-row/file link**. The line-20 mention is the frozen path’s substantive S055 reference. No S055 token occurs in the other 34 frozen paths.

The additional used-by path `corpus/lessons/round-27.md` is outside the frozen population and therefore does not enlarge the denominator. It exists at baseline and current (same SHA-256 `a15cf0b98f99ba7c978fc178cb8a5f541ab34820a340f179cc82d28b0022c254`); literal S055 mentions include lines 48, 56, and 201. It is an allowed additional used-by entry, not a frozen citation link.

**Effective denominator:** for this one frozen row, 35 eligible knowledge paths were scanned; one distinct path cites S055 (1/35), 34 do not. The checker’s row/file-link count for S055 is 1, not 2; the two literal mentions are within that one path. Its two used-by entries comprise one frozen citing path and one permitted out-of-population lesson path.

The lane checker `--json` cross-check agrees with this independent map for S055 at baseline replay and current: `status=mined`, `citing_files=[corpus/knowledge/extraction-policy-comparison.md]`, `missing_used_by=[]`, and no S055-specific findings. Baseline replay’s source row and frozen inputs were reconstructed from the pinned revision in my scratch tree. A first incomplete scratch clone omitted the row’s additional lesson target and spuriously emitted `used_by_missing`; I corrected the clone by including that baseline lesson (which exists at the pinned revision) and use only the corrected replay above. Scratch evidence: `.ufo/waves/round-28/scratch/FRegistryS055/independent-map.json` and `checker-comparison.json`.

## Row-specific falsifier

Counterfactual scratch mutation only: remove `corpus/knowledge/extraction-policy-comparison.md` from S055’s `used-by`, leaving the lesson entry and all frozen inputs intact. The checker then returns exactly a S055 `missing_used_by` finding for `corpus/knowledge/extraction-policy-comparison.md`; line 20 remains the triggering frozen mention. This is a concrete falsifier for S055’s coverage if that one used-by link were absent, not a defect in the current row.

S050’s corrective-index reversal is separate and is not evidence for S055 or endorsement of S050’s superseded reason. S038’s already-disclosed drift is not a discovery here. No semantic citation truth, whole-registry correctness, or whole-current-tree consistency is claimed.

**Confidence:** high for the S055 row identity, baseline/current equality, literal frozen-path map, status, and subset used-by accounting; none asserted for semantic truth of the cited code source.

**VERDICT: PASS** — S055 passes this bounded frozen literal-reference check.
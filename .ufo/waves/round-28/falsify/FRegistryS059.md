# FRegistryS059 — bounded row falsification

## Verdict: PASS

**Scope:** S059 only, under the frozen 13-row / 35-knowledge-path literal-reference contract. This is not a semantic citation-support finding, a whole-registry truth judgment, or a whole-current-tree census.

## Evidence and method

- Read `plans/registry_check.py`, the frozen `plans/fixtures/r28/registry/population.json`, the S059 registry row, and the relevant knowledge/lesson files. The population SHA-256 is `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014`; its `base_revision` is `b9b24796277020d1b9b01923b45313d6a565e664`.
- The population manifest itself is not present at that baseline commit. I therefore used the pinned manifest's 35 paths, then directly read `corpus/SOURCES.md` and those paths from `git archive b9b2479…`, and read their current worktree counterparts. The baseline archive contained `SOURCES.md` plus all 35 requested paths. No production module was imported in this independent derivation.
- Independently parsed the Registry table row and applied the manifest's standalone-reference expression to every raw file. The delivered checker was separately run read-only on the final tree with bytecode disabled (`PYTHONDONTWRITEBYTECODE=1`, `python3 -B`, `--json`). Its S059 record agrees with the independent map.

## S059 expected-before / current-after

| State | Row status | Frozen paths with literal S059 | Literal occurrences in that path | Used-by | Missing frozen used-by | S059 row finding |
|---|---|---|---:|---|---|---|
| Baseline `b9b2479…` | `mined` | `corpus/knowledge/extraction-policy-comparison.md` | 2 (lines 1, 53) | `corpus/lessons/round-27.md`; `corpus/knowledge/extraction-policy-comparison.md` | none | none |
| Final worktree | `mined` | `corpus/knowledge/extraction-policy-comparison.md` | 3 (lines 1, 53, 132) | `corpus/lessons/round-27.md`; `corpus/knowledge/extraction-policy-comparison.md` | none | none |

The S059 registry row's status and used-by cells are unchanged from baseline. Both listed used-by paths exist in the respective state. The frozen citing set is a subset of used-by: the lesson is an allowed additional used-by path and is not part of the 35-path denominator. S059 is a `spec` row, not a `code` row.

The added current occurrence at line 132 is the explicit authority boundary: “the RFC S059 supplies only the RFC-side prohibition”; S065 supplies the Python-side documentation. It is a literal reference and is counted, not evidence that S059 supports the Python-side claim. The S050 corrective-index reversal is separate and is not treated as support for S050's superseded no-match reason. S038's previously disclosed drift is not a new S059 finding.

## Denominator and literal behavior

- Effective population: **13 source IDs × 35 frozen files**; no frozen file was missing in either state.
- Total effective denominator: **12 distinct source–file links** in both baseline and final, across **2** cited files; the remaining **33** paths are zero-reference controls. S060 is uncited, so the denominator is not 13.
- S059 contributes **1 of those 12 links**, not 2 or 3: repeated occurrences within one file collapse to one row–file edge. Its used-by contains that one frozen path.
- The checker scans raw file text using the literal regex; it does not interpret Markdown quotes or code fences. Its source includes a `valid_literal_fence` self-test fixture with S049 inside a fenced block and expects that literal to count. The independently observed S059 occurrences themselves are all outside fenced blocks; none was excluded or assigned special Markdown meaning.

The final `--json` output reports 13 checked rows, 35 expected files, 12 links and zero scoped findings; its S059 entry has the single citing file above, status `mined`, and an empty `missing_used_by`. This bounded checker output is not a claim of citation truth. The captured baseline checker output is red for S038 and S050; that does not produce an S059 mismatch and is not being recast as a whole-registry baseline pass.

## Row-specific falsifier

**F-S059:** A standalone S059 reference in any frozen path that is absent from S059's used-by, or a non-`mined` status while S059 is cited, would falsify this row's clean result (`missing_used_by` or `cited_not_mined`). The observed frozen citing set is exactly `{corpus/knowledge/extraction-policy-comparison.md}`, it is listed in used-by, and status is `mined`; this falsifier did not trigger.

**Confidence:** High for the limited literal S059 coverage/status result (direct baseline and final derivations agree with the delivered final checker); no conclusion is drawn about whether the underlying source semantically supports every statement.

VERDICT: PASS
# FRegistryS056 — frozen literal-contract finding

**Scope:** S056 only, against the pinned frozen13/35 population. This is not a whole-registry truth or whole-current-tree review.

## Independent derivation

I read `plans/registry_check.py`, `plans/fixtures/r28/registry/population.json`, and parsed the baseline `b9b24796277020d1b9b01923b45313d6a565e664` files directly with `git show`; I independently read the current working-tree files. The independent derivation did not import the checker or another oracle. The population digest is `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014`; it fixes 13 source IDs and 35 knowledge paths, with `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` as the literal matcher.

Effective denominator for this assignment: **one row (S056) scanned against all 35 frozen knowledge paths**. All 35 files existed in both baseline and current snapshots. There is exactly one standalone S056 occurrence in each snapshot, in `corpus/knowledge/extraction-policy-comparison.md:1`; the other 34 paths contain none.

## Expected-before / current-after, S056 only

| Observation | Baseline b9b2479 | Current tree |
|---|---|---|
| Registry row | `corpus/SOURCES.md:78`, S056 | `corpus/SOURCES.md:78`, same row cells |
| Status | `mined` | `mined` |
| Frozen citing files | `corpus/knowledge/extraction-policy-comparison.md` | same |
| Declared `used_by` | `corpus/lessons/round-27.md`; `corpus/knowledge/extraction-policy-comparison.md` | same |
| `used_by` paths absent from row’s frozen citations | none | none |
| Row-specific literal-contract findings | none | none |

The knowledge file is the sole counted S056 link and is included in `used_by`. The round-27 lesson is an additional, live `used_by` path outside the frozen knowledge population; it is permitted and is not an extra frozen link. `plans/parser_policy_compare.py`, the row’s code locator, exists in both snapshots and has the same SHA-256 (`c4296935ed40f4d12a5d3ad238a2d5b9c7ca98712e61a2caf206476f9b025a27`, 22,089 bytes). Its `render()` code includes the `POLICY` and `TOTAL` output anchors named in the row (lines 329–350). I did not run that code or validate its recorded metrics.

## Corrective and code-reference boundaries

The one frozen S056 occurrence is the knowledge-file header’s code reference to `plans/parser_policy_compare.py`. The same knowledge file separately has the S050 corrective mention at lines 18–20 and 123–126. That mention is an S050 literal-index correction, not evidence for S056 and not support for S050’s superseded blanket no-hit reason; the text leaves S058 controlling. S038’s already-disclosed drift is likewise not an S056 finding.

The contract checked here establishes literal coverage, row status/enums, and `used_by` path coverage/liveness. It does not establish source-truth, semantic endorsement, or correctness of the code’s reported counts.

## Cross-check and row-specific falsifier

After completing the independent derivation, I ran the permitted read-only command with bytecode disabled: `PYTHONDONTWRITEBYTECODE=1 python3 plans/registry_check.py --json`. Its S056 object agrees exactly: status `mined`, one citing file (`corpus/knowledge/extraction-policy-comparison.md`), the two `used_by` paths above, and `missing_used_by: []`. The bounded CLI output reports 13 rows / 35 files / 12 links / 0 findings; I do not independently adjudicate its other twelve rows or infer whole-tree consistency from it.

**Row-specific falsifier tested:** the exact `S056 own-work plans/parser_policy_compare.py` mention at `corpus/knowledge/extraction-policy-comparison.md:1` falsifies the possible claim that S056 has no frozen literal reference (or only a lesson reference). It is the one in-population link that must remain in the row’s `used_by`; it is present in both baseline and current rows. Thus this discriminator exposes no S056 defect in either snapshot.

## Verdict and confidence

**VERDICT: PASS** — S056 alone satisfies the frozen13/35 literal-reference contract in baseline and current snapshots; no expected-before/current-after S056 finding or row-cell divergence was observed. Confidence is high for the bounded literal-reference/status/used-by result, and intentionally makes no claim about source truth, code-output metrics, other rows, or the current tree as a whole.

Tool installs/updates: none.

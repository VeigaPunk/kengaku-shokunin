# MutPopulationDesign — literal boundaries and frozen-population loss

Writer/seat: `KengakuR28.MutPopulationDesign-2` · author-side mutation-design seat · 2026-10-21.

**Axes:** novelty (legacy) mapped to canonical coverage/constructs, held at 7; calibration, held at 8. This assignment supplies C2 boundary witnesses and a single planned mutation, not C1 evidence, score repricing, outside review, or round admission.

**Scoped verdict: PASS — the requested preimplementation design deliverable is complete. Mutation-probe verdict: INCONCLUSIVE / NOT RUN.** No instrument was inspected or executed, so there is no killed/survived mutant and no demonstrated C2 capability improvement.

## Evidence and authority actually opened

All lane-relative paths below resolve under `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

| Input / location | URL and access date | Located quotation (at most 25 words) | Scope |
|---|---|---|---|
| `plans/round-28-claims.md:9,23–27` | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-28-claims.md`, accessed 2026-10-21 | Line 25: “A missing frozen knowledge file/source row is failure, never silently excluded.” | C2 completeness, literal mentions, actual Registry section, 11 columns, exit classes and per-source outputs. |
| `plans/fixtures/r28/registry/population.json:2–55` | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/registry/population.json`, accessed 2026-10-21 | Line 55: `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` | Exact lexical boundary and persisted source/path identity; not a semantic Markdown or citation-support rule. |
| `.ufo/waves/round-28/build-spec.json`, `.items[name=ExecRegistry].prompt` | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/build-spec.json`, accessed 2026-10-21 | “stable findings queued_cited, missing_used_by, duplicate_source_id, source_missing, knowledge_missing, invalid_used_by etc.” | Shared writer interface names, not observed instrument output. |
| Canonical `CORPUS.md:86–108` | `file:///home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`, accessed 2026-10-21 | Line 89: “No `\|` inside any cell.” | Eleven-column registry shape and status/used-by schema used to author synthetic rows. |
| Canonical `PROTOCOL.md:398–402` | `file:///home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md`, accessed 2026-10-21 | Lines 399–400: “asserting both the exit code and a stable expected finding-id” | Reason to pin an exit plus the named failure, rather than accept any red result. |

The preregistration identifies baseline `b9b24796277020d1b9b01923b45313d6a565e664`; tasking identifies preregistration `f0ba09be0f3066daba2134b943d973ad1588f34a`. Neither history statement was independently checked with Git. Production `SOURCES.md`, knowledge bodies, implementation files and sibling worktrees were not opened for this design. Mandated Godspeed/Shokunin operational instructions were also read. No external source was reopened or admitted.

## Exact witness artifact

Created only:

- `.ufo/waves/round-28/scratch/MutPopulationDesign-2/witness-fixtures.json`
- This assigned report: `.ufo/waves/round-28/build/MutPopulationDesign.md`

The JSON artifact is a **hand-authored fixture description**, not a runnable harness or an observed test log. Its `materialization` member defines exact UTF-8/LF bytes, population JSON serialization, registry line rendering and independent case application. `base_population` contains the complete persisted 35 path names and the exact 13 source IDs:

`S038, S049, S050, S051, S052, S053, S054, S055, S056, S057, S058, S059, S060`.

The synthetic base creates every frozen knowledge path. All 13 IDs appear once in `corpus/knowledge/agent-time-horizon-and-task-validity.md`; each synthetic mined registry row lists that path. Every other frozen file contains only `# Frozen non-reference witness\n`. Thus the designed clean baseline does not inherit the disclosed real-tree S038 queued drift. Synthetic rows and `S999` controls are **not source admissions**.

Every case starts from this complete base, not from the previous case. The JSON's expected structures are semantic projections: they are not an assertion of the uninspected implementation's JSON key spelling. Unmodified sources retain `base_expected`; missing rows cannot inherit its mined status or used-by values.

## Hand-expected boundary and loss witnesses — not executed

Interface IDs already named by the writer assignment are marked **specified**. New error names are marked **proposed**; their exact spellings do not become preregistered requirements merely by appearing here.

| Stable fixture ID | Exact change / distinguishing witness | Expected result by design |
|---|---|---|
| `MPD-000-clean` | Complete synthetic base, unchanged. | Exit 0; no findings; requested source set exactly the 13 IDs above; 35 frozen files read. |
| `MPD-001-embedded-identifiers` | Replace `attrib-prior-art-r21.md` with `xS038 S038x _S038 S038_ foo_S038 S038_bar S038x9 0S038 XS038Y s038 S03 S0380 S03801 S0380_\n`. | Exit 0. Raw lexical matches are exactly `S0380`, `S03801`; neither is a prefix citation of S038, neither enters C2. S038's citing_files remains only the base file. |
| `MPD-002-literal-wrappers` | Six exact file texts in JSON: fenced-only `S038`; quoted-only `S049`; inline-code `S050`; historical `S051 -> S052`; accented-neighbor `éS053 S053é`; punctuation/hyphen `S054`. | Exit 1; **specified** `missing_used_by` for exactly S038, S049, S050, S051, S052, S053, S054, each paired with its exact changed file. Repeated mentions still add one citing_files member per file. |
| `MPD-003-queued-cited` | Change only S038 status `mined` → `queued`; retain correct used-by. | Exit 1; **specified** `queued_cited:S038`; no missing_used_by. |
| `MPD-004-missing-frozen-source-primary-witness` | Delete S038's row from Registry; keep the population and its literal citation. | Exit 1; **specified** `source_missing:S038`. Thirteen sources remain requested; twelve registry rows are present. Do not claim twelve is the whole frozen population. |
| `MPD-005-duplicate-source` | Duplicate S038's identical row inside Registry. | Exit 1; **specified** `duplicate_source_id:S038`. Identical duplicates must not disappear into last-wins dictionary construction. |
| `MPD-006-malformed-ten-cell-row` | Exact S038 row has ten cells: omit recheck, leaving used-by as the last cell. | Proposed exit 1 and **proposed** `registry_row_malformed:S038`; source_missing may additionally describe an unavailable parsed row. Mandatory semantic guard: non-clean, no silent drop/coercion. |
| `MPD-007-malformed-twelve-cell-row` | Exact S038 row has twelve cells due to `synthetic \| only` split across two cells. | Proposed exit 1 and **proposed** `registry_row_malformed:S038`; source_missing may additionally describe an unavailable parsed row. Never truncate the surplus cell. |
| `MPD-008-outside-registry-cannot-rescue-missing` | Delete actual S038 row; prepend an otherwise valid S038 table under `## Example`, outside Registry. | Exit 1; **specified** `source_missing:S038`. An example cannot rescue an absent Registry row. |
| `MPD-009-new-source-and-file-excluded` | Add valid queued synthetic S999 row plus unlisted `corpus/knowledge/r28-outside-population.md` containing `S038 S999`. | Exit 0; no new source/file enters C2; S038 citing_files unchanged. This is the positive exclusion control, not a whole-registry audit. |
| `MPD-010-missing-frozen-nonreference-file` | Delete `corpus/knowledge/telemetry-run-design.md`, which contains no IDs in the base. | **Specified** `knowledge_missing` at that exact path; proposed exit 2 for unavailable input. Frozen denominator stays 35, readable files 34; never 34-of-34 clean. The preregistration requires failure but does not explicitly fix this case's 1/2 split. |
| `MPD-011-population-omits-frozen-source` | Remove S038 from population source_ids, without changing base_revision or Registry. | Proposed exit 2, **proposed** `population_mismatch`, missing ID S038. A 12-source edited manifest must not silently redefine C2. |
| `MPD-012-population-same-count-unknown-source` | Replace population S038 with S999: list still has 13 entries. | Proposed exit 2, **proposed** `population_mismatch`, missing S038/unexpected S999. At minimum, an evaluator that reaches S999 must report **specified** source_missing rather than intersecting it away. |
| `MPD-013-population-duplicate-source` | Replace population S038 with a second S049: length 13, distinct IDs 12. | Proposed exit 2, **proposed** `population_mismatch`; distinguish population duplication from duplicate Registry rows. |
| `MPD-014-population-same-count-path-substitution` | Replace the telemetry path with an existing new-file control: length remains 35; both files exist. | Proposed exit 2, **proposed** `population_mismatch`, naming the missing baseline path and unexpected replacement. Counts and file existence alone do not pin membership. |
| `MPD-015-population-wrong-type` | Set source_ids to the exact space-separated string supplied in JSON, not an array. | Proposed exit 2, **proposed** `population_invalid`; no character iteration or silent coercion. |
| `MPD-016-invalid-status-enum` | Change only S038 status to `mine`. | Proposed exit 1, **proposed** `invalid_source_enum:S038`, column status/value mine. No default-to-mined repair. |
| `MPD-017-unsafe-used-by` | Keep S038's correct used-by and append `../outside.md`. | Exit 1; **specified** `invalid_used_by:S038`; no missing_used_by. No outside-root file should be created or read. |

### Boundary distinctions these fixtures preserve

1. **Literal is not Markdown-semantic.** The fenced-only file must count. Keeping fenced, inline and quote witnesses in separate files prevents prose/quote detection from accidentally masking code-fence suppression.
2. **The boundary is explicitly ASCII.** The persisted lookarounds count `éS053` and `S053é`; a Unicode `\bS[0-9]{3,}\b` replacement is not equivalent. Longer digit strings are whole tokens, not three-digit prefixes.
3. **Known baseline drift is not the mutant.** Any red result on the real baseline would be insufficient. The clean synthetic control and exact named missing-row witness separate detector sensitivity from unrelated queued findings.
4. **Missing input is not absence of references.** Removing a reference-free frozen file must still fail. Returning fewer readable inputs with no typed finding is silent loss.
5. **Population loss differs from registry loss.** An omitted Registry row needs `source_missing`. Editing the frozen source/path manifest attacks the denominator itself; same-cardinality substitutions show why counts alone cannot establish identity. A persisted `base_revision` string alone does not authenticate membership.

The preregistration fixes membership but does not assign a C2 population-tamper finding name or expressly prescribe an authentication mechanism. The population-mismatch taxonomy above is therefore a concrete design proposal, not an observed implementation defect or a new claim about shipped protections. Expected membership must be taken from the preregistered frozen set, not regenerated from the corrupted test input.

## Single planned mutation and bounded detector

**Mutant `MPD-M1-frozen-source-intersection`:** at the future `plans/registry_check.py` frozen-source iteration point, change only the iterator/filter so it visits `frozen_source_ids ∩ parsed_registry_ids` instead of every frozen source ID with an explicit missing-row branch. No implementation line number is asserted: production code was not read. Do not change parser, regex, output, fixtures or expected data at the same time.

**Expected detector:** materialize `MPD-000-clean` and `MPD-004-missing-frozen-source-primary-witness` as independent roots under the assigned scratch directory. Invoke the same isolated instrument for each, with a finite per-call deadline, for example:

```text
python3 <own-scratch>/instrument/plans/registry_check.py --root <own-scratch>/roots/MPD-000-clean --json
python3 <own-scratch>/instrument/plans/registry_check.py --root <own-scratch>/roots/MPD-004-missing-frozen-source-primary-witness --json
```

These commands are **proposed, not run**. A suitable bound is ten seconds per CLI call. The wrapper detector passes only if the clean case is exit 0 with no findings and the missing-row case is exit 1 with the exact `source_missing:S038` finding, retaining the requested 13-source scope. Check exact per-source identity, not merely nonzero exit or a reported total. The witness's expected CLI exit 1 is a passing detector assertion, not a pristine detector failure.

On one assigned isolated scratch copy, the later experiment should save exact instrument bytes and SHA-256, run this identical bounded detector on pristine bytes, apply M1 only, run it again, restore original bytes in a `finally` path, verify the restored hash equals the original, and run the same detector after restoration. Record stdout, stderr, every CLI exit and wrapper assertion result in all three phases. Baseline or restored detector failure is **inconclusive**, never a killed mutant. A surviving mutant is a coverage finding, not permission to narrow C2.

Predicted discriminator, explicitly **not observed**: the mutant may leave the clean control unchanged while losing `source_missing:S038` or reducing output to twelve sources for the witness. Either discrepancy must fail the detector even if another unrelated finding keeps an overall run red.

## Actual outputs, hashes and restoration evidence

No detector run, mutation, restoration, build, test, linter, formatter, browser action, benchmark request, Git/index/jj operation, upstream import/eval, REA MCP call, tool install or host-service change was performed. No tool version/channel install entry is applicable.

Actual tool activity was reading/searching preregistration and interface/instruction documents, writing this report and the owned fixture description, and this single hash command:

```text
sha256sum plans/round-28-claims.md plans/fixtures/r28/registry/population.json .ufo/waves/round-28/build-spec.json .ufo/waves/round-28/scratch/MutPopulationDesign-2/witness-fixtures.json
```

Observed command output:

```text
d406d22270cc7639032ad519f64d24493463e6621a1c0a31bca139083a9e9afb  plans/round-28-claims.md
1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014  plans/fixtures/r28/registry/population.json
2a9a2e0932c6e12638cfb27bd28c07ee3fe6b46331185ba98b77d402c48af204  .ufo/waves/round-28/build-spec.json
6736251bc8a94c8ba14e3a328a2cc5e241e7394445f95e38bf46ea4ac45ba552  .ufo/waves/round-28/scratch/MutPopulationDesign-2/witness-fixtures.json
```

These identify the opened design inputs and produced fixture artifact; they are **not** a pristine/mutated/restored hash triplet. Instrument before/after/restored hashes and runtime outputs are unavailable because this assignment explicitly stops at design. No instrument bytes were touched, so no restoration was necessary or claimed.

## Limitations and final scope

This is complete design work within the assigned leaf-seat write scope, not execution evidence. Fixture descriptions were not materialized or checked against an implementation; proposed error names and unspecified exit splits need an explicit writer-interface decision before becoming exact-name assertions. The six specified names above come from the writer contract, not observed behavior. The report claims no real source-row repair, semantic citation support, whole-tree census, endpoint restoration, outside-non-author closure or C1 result. Prior two P4 offline groups and one superseded P4 ID remain outside this work and unchanged.

**Final scoped verdict: PASS for the requested mutation plan and exact hand-expected witness fixtures; INCONCLUSIVE / NOT RUN for mutant efficacy and C2 behavioral validation. Scores held.**

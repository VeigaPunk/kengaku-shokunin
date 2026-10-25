# C1 pinned-snapshot mutation-control design

Writer/seat: **KengakuR28.MutPinDesign-2**. Date: **2026-10-21**. Author-side advice only.

**Axes:** legacy novelty → canonical coverage/constructs (7 held); calibration (8 held). This seat improves the specificity of integrity controls without converting a design into empirical evidence or repricing either axis.

**Scoped verdict: PASS — requested design and hand-expected witnesses delivered. Mutation efficacy: NOT RUN / unassessed.** This is not a C1, C2, whole-round, source-endorsement, or outside-closure PASS.

## Authority and exact reading scope

Only preregistration and interfaces were read. No production audit implementation, independent oracle implementation, raw task body, evaluator/helper source body, or external benchmark endpoint was opened or executed.

| Reference opened locally | Located quote (≤25 words) | Scope |
|---|---|---|
| [Preregistration](file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-28-claims.md), accessed 2026-10-21, line 15 | “Verify snapshot sha256 values against persisted manifest before calculating anything” | C1 integrity gate; same line fixes exit 0/1/2 and `snapshot_tampered` / `input_missing`. |
| Same preregistration, accessed 2026-10-21, line 21 | “Mutation tests run on scratch copies; no changes to immutable input snapshots.” | Isolation and restoration boundary; hand expectations must precede output comparison. |
| [Build interface](file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/build-spec.json), accessed 2026-10-21, `items[name=ExecBenchmark].prompt`, line 17 | “Include source mutation controls (manifest digests independently persisted).” | Independent original identity is required; the changed manifest cannot be its own expectation oracle. |
| [Manifest](file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/manifest.json), accessed 2026-10-21, line 2; file records lines 5–23 | `"upstream_revision": "dce04686a56253aefba7b18a4fa0937cf1dc987b"` | Original WebArena revision and four declared source-file pins; not WebArena-Verified. |
| [Frozen selection](file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/selected-task-ids.json), accessed 2026-10-21, line 1 | `[389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]` | Fixed ordered selection; matches preregistration line 19. |

C1 claim location is preregistration line 8; full population and static-only interface are lines 15–21. Baseline commit supplied by the assignment: `b9b24796277020d1b9b01923b45313d6a565e664`; preregistration commit: `f0ba09be0f3066daba2134b943d973ad1588f34a`. No Git operation was used to independently verify those commit labels.

Manifest URLs identify pinned raw GitHub paths under `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/`. They were read as manifest metadata only, not reopened upstream. This report does not supply independent upstream source-opening evidence.

## Fixed expectations delivered before comparisons

Hand-authored, non-executable witness file:

`.ufo/waves/round-28/scratch/KengakuR28.MutPinDesign-2/c1-pin-witnesses.json`

Observed SHA-256 of that artifact: `5ee7d00e82078a2b75e1213b5418ce0959a4920591cbd13e61a27cfadba36829`.

The file fixes the original revision, complete four-file map, manifest identity, ordered selection, expected exit/finding predicates, construction recipes, and restoration ledger. Its expected results are not copied from any audit output. Keep this expectation file outside every mutated witness root. Preserve its hash and the eventual runner hash before running comparisons; never regenerate expectations from the changed manifest or audit output.

### Interface hashes actually measured

| Lane-relative interface | Observed SHA-256 |
|---|---|
| `plans/round-28-claims.md` | `8b2e237a05b15dc2f10a62a19947ab8b15120af3c16ae9cf245da1945c485a5f` |
| `plans/fixtures/r28/webarena/manifest.json` | `c78b1478c5cb18dd7621723023e7ff15342401c72fc04a939a8d4d290323a6dd` |
| `plans/fixtures/r28/webarena/selected-task-ids.json` | `5f7eea2e6868553dbda4d7a4be491b3cbaaeb532f1c44dfb9fb40006ff3ed17a` |

### Source pins copied literally from the manifest, not independently rehashed

Paths below are relative to `plans/fixtures/r28/webarena/`.

| Path; manifest location | Declared bytes | Declared SHA-256 |
|---|---:|---|
| `config_files/test.raw.json`; lines 5–8 | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| `evaluation_harness/evaluators.py`; lines 10–13 | 13264 | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` |
| `evaluation_harness/helper_functions.py`; lines 15–18 | 7565 | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` |
| `LICENSE`; lines 20–23 | 11357 | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |

The selection file is not in the manifest's four-file map. Its measured hash and ordered list are baseline identity witnesses here, not an invented new `snapshot_tampered` contract for changes to that file. Other aggregate counts, including informed forecasts, are deliberately not manufactured as observed oracle results.

## One plausible defect under challenge

**M1: mutable-manifest trust.** The audit accepts the supplied manifest as the sole authority, rather than checking it or the complete original file map against independently persisted original pins. A coherent source-and-manifest rewrite can then pass ordinary file-to-manifest hashing.

The proposed smallest future code mutation disables only the independent original-pin rejection decision while retaining ordinary per-manifest hashing and missing-file detection. No implementation was inspected, so no actual filename/line for that decision, syntactic edit, or mutated runner hash is claimed. Binding the semantic defect to a real single behavior-bearing point belongs to a separately assigned probe after implementation exists. Do not remove multiple independent defenses merely to manufacture a kill.

**Key distinction:** raw-byte corruption, a missing file, and a deliberately wrong manifest digest can all be rejected by a verifier that still has M1. They are necessary controls but do not alone establish independent original pinning. The coherent-rebind witness is the discriminating case.

## Concrete isolated witness matrix

All cases use a complete copied lane-shaped C1 fixture root, never the lane snapshot or a sibling worktree. Each starts from exact originals. Four-file parameterizations are four separate cases, not simultaneous corruption. `exit 2` is a could-not-evaluate integrity result, not an assertion that WebArena tasks are invalid.

| Witness | Isolated mutation | Fixed hand-expected result |
|---|---|---|
| **P0 pristine** | None. Complete four-file snapshot, original manifest and selection file. | Exit **0**; valid population **812**; selected count **16** and exact ordered IDs above; no `snapshot_tampered` or `input_missing`. |
| **T1 byte change ×4** | Append exactly one LF byte to each pinned file separately; leave manifest unchanged. | Exit **2**, `snapshot_tampered`; no success-class task/scorer inventory. The JSON/Python trailing newline preserves parsing semantics, so this tests byte identity rather than intentional schema breakage. |
| **I1 missing file ×4** | Make each pinned file absent separately; leave its original manifest entry present. | Exit **2**, `input_missing`; no success-class inventory. Include the helper and LICENSE, not just raw tasks/scorer. |
| **C1 manifest digest change** | Only replace the raw-task digest's leading `7` with `0`; all source bytes and byte counts unchanged. | Exit **2**, `snapshot_tampered`. Wrong digest is `0b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`. This alone does **not** distinguish M1. |
| **C2 coherent rebind** | Append one LF to raw tasks. Change only that manifest record to the new actual digest and bytes **880777**. Other records, revision and URLs stay fixed. | Exit **2**, `snapshot_tampered`, even though the changed manifest is internally consistent. This is the principal M1 discriminator. |
| **C3 manifest record omission** | Remove only the helper-function record from valid manifest JSON; leave the actual helper and all other source files unchanged. | Exit **2**, `snapshot_tampered`. This is changed authority, not a physically missing source file. Do not let the altered manifest shrink the required population. |
| **I2 missing manifest** | Make only the manifest absent. | Exit **2**, `input_missing`; source files remaining intact cannot justify proceeding without the persisted manifest. |

C2 may compute a digest solely to construct its changed manifest payload. That computed value must never replace the independently fixed original digest or the expected failure. The original task JSON meaning and task selection are unchanged by the extra trailing newline; thus matching aggregate outputs cannot excuse accepting changed pinned bytes.

The stable finding codes for these designs are frozen above. Production JSON member names are not specified by preregistration; the witness file therefore defines predicates, not fictitious production schema keys. An eventual adapter may map actual fields to those predicates without changing expected outcomes. A traceback, timeout, malformed output, or exit 1 is not an acceptable substitute for the designed exit-2 finding. Integrity failure must not publish a success-class inventory; pin diagnostics and explicitly unevaluated counters remain permissible. Output alone cannot prove that no calculation occurred internally, so code-order review remains distinct from these behavioral controls.

## Same bounded detector and restoration protocol — proposed, not executed

Suggested future CLI invocation, identical across phases except the isolated root substitution:

```text
timeout 30s python3 <fixed-runner>/plans/benchmark_spec_audit.py --root <isolated-witness-root> --summary --json
```

The bounded detector **D** compares all 13 CLI instances in the matrix against the frozen witness predicates. For an eventual code mutation, run the same D on **pristine runner bytes → M1-mutated runner bytes → exact restored runner bytes** (at most 39 CLI invocations, each bounded to 30 seconds). Freeze the runner and expectation hashes before the first comparison. The detector never imports/executes the upstream Python files, invokes a browser, or contacts benchmark sites.

For each instance preserve stdout/stderr bytes, exit status, command, case ID, runner/expectation hashes, and before/mutant/restored hashes for every touched file; an absent file is recorded as `MISSING`, never assigned a fake hash. Restore exact preserved bytes in a finally-equivalent cleanup even after detector failure or timeout. Do not recreate originals by JSON serialization or recomputing a manifest. Restored hashes must equal both the recorded before hashes and the independent original pins. If a code mutation is assigned later, the runner itself receives the same exact-byte restoration evidence.

**Future verdict rule:** baseline detector failure is **INCONCLUSIVE**, never killed. Baseline D PASS, mutant D failure on the required integrity predicate, restored D PASS, and exact restored bytes can support a **killed** verdict. A completed mutant D PASS is **survived**, a coverage finding rather than permission to relax the contract. Missing restoration evidence prevents a completed kill claim. Redundant independent guards may make a particular single-guard mutation survive; do not silently weaken additional guards or overstate which defect was introduced.

## Actual commands, outputs and restoration evidence

Only checksum fact commands were executed; there were **zero detector runs**:

```text
sha256sum plans/round-28-claims.md plans/fixtures/r28/webarena/manifest.json plans/fixtures/r28/webarena/selected-task-ids.json
8b2e237a05b15dc2f10a62a19947ab8b15120af3c16ae9cf245da1945c485a5f  plans/round-28-claims.md
c78b1478c5cb18dd7621723023e7ff15342401c72fc04a939a8d4d290323a6dd  plans/fixtures/r28/webarena/manifest.json
5f7eea2e6868553dbda4d7a4be491b3cbaaeb532f1c44dfb9fb40006ff3ed17a  plans/fixtures/r28/webarena/selected-task-ids.json

sha256sum .ufo/waves/round-28/scratch/KengakuR28.MutPinDesign-2/c1-pin-witnesses.json
5ee7d00e82078a2b75e1213b5418ce0959a4920591cbd13e61a27cfadba36829  .ufo/waves/round-28/scratch/KengakuR28.MutPinDesign-2/c1-pin-witnesses.json
```

Both commands ran from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Reads, listings and targeted searches accessed only the interfaces identified above and their directory names. No builds, tests, linters, formatters, selftests, production checks, external source fetches, REA tools, model runtimes, Git writes, jj writes, or package/service operations were run. No tools were installed or updated.

**Actual mutant:** none applied; M1 is a design target. **Actual detector stdout/stderr/status:** absent, because no detector ran. **Killed/survived/inconclusive:** no empirical classification is claimed; `NOT_RUN_DESIGN_ONLY` is the recorded state. This is not an inconclusive *baseline failure*, since no baseline experiment occurred.

**Restoration:** no source or instrument bytes were changed, so there is no mutation/restoration event or before/after mutation hash pair to claim. The observed hashes above pin interfaces and the delivered witness artifact only. The only writes were this assigned report and this seat's own scratch expectation JSON; neither is executable probe scaffolding. A later probe must obtain real before/mutant/restored hashes rather than relabeling these design pins as restoration evidence.

## Limits and final scoped disposition

This report completes the assigned **design-only** task without waiting for integration or inspecting production code. It does not demonstrate an implemented gate, a killed mutant, an actual pristine audit PASS, or an independent rehash of the four source bodies. No C2 source-reference repair, source admission, score change, endpoint restoration, whole-tree census, or admission-timing endorsement is asserted. Round27's two offline P4 groups and one superseded P4 ID remain disclosed and unaffected. All advice here is author-side; Q13 structural evidence is not source endorsement or outside closure.

**Final scoped verdict: PASS for the pinned-control design and fixed hand-expected witness deliverables; empirical mutation resistance remains NOT RUN.**

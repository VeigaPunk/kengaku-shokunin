# MutRegistryDesign — C2 same-command repair and mutation design

Writer/seat: `KengakuR28.MutRegistryDesign-2` (author-side mutation-design seat). Date: 2026-10-21.

**Axes:** novelty (legacy → canonical coverage/constructs, held 7) and calibration (held 8). This assignment supports the bounded C2 diagnostic, not a new method-novelty claim or repricing.

**Final scoped verdict: PASS — requested design delivered.** Empirical mutant verdict: **INCONCLUSIVE / NOT RUN (explicit design-only assignment)**. No mutant was applied, killed, or shown to survive. No C2 repair, round admission, outside closure, or blanket round PASS is asserted.

## Scope and exact authority

Read preregistration/interfaces only; did not read `registry_check.py`, the actual `corpus/SOURCES.md` rows, or the 35 knowledge-file bodies. No upstream code was executed/imported/evaluated, no benchmark endpoint was contacted, and no REA MCP was used. No production check, build, test, linter, or formatter ran. No tool was installed or updated.

Baseline supplied by the preregistration: `b9b24796277020d1b9b01923b45313d6a565e664`. Dispatch supplies preregistration revision `f0ba09be0f3066daba2134b943d973ad1588f34a`; this seat did not run Git to re-verify that commit. The opened population declares exactly S038 and S049–S060, 13 IDs, and 35 explicit knowledge paths. The actual S038 citation set and old registry cells remain **unobserved by this seat**.

The following are local contract openings, not openings or endorsements of the original S038 source. Each access date is 2026-10-21; each located quote is at most 25 words.

| Located URL | Located quote | Scope |
|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-28-claims.md#L9` | “Repair only after reopening its original source; source-row immutable cells remain unchanged.” | C2 repair/admission gate; literal completeness, not source truth. |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-28-claims.md#L25` | “A missing frozen knowledge file/source row is failure, never silently excluded.” | Frozen-input negative control. |
| Same URL, `#L25` | “Cited rows must be `mined` and list every citing frozen path.” | Status and used-by are separate obligations. |
| Same URL, `#L27` | “Selftest must be CLI-level with hand-authored fixture expectations” | Expected values must precede detector execution. |
| Same URL, `#L33` | “passes with allowed-cell repair as the only delta.” | Same-command baseline/repair causal contrast. |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/registry/population.json#L55` | `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` | Exact frozen literal-reference matching rule; lines 3–17 give the IDs and 18–54 the paths. |
| `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/build-spec.json#L34` | “stable findings queued_cited, missing_used_by, duplicate_source_id, source_missing, knowledge_missing, invalid_used_by etc.” | Writer interface naming, not observed implementation output. |
| `file:///home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md#L86` | `id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by` | Eleven registry content columns, quoted as column names in order. |
| Same URL, `#L116` | “Only `status`, `recheck` and `used-by` change in place” | Allowed-cell boundary; each actual change requires lesson old→new logging. |

Preregistration lines 11 and 25 exclude new sources/new round28 knowledge from C2. Lines 40–41 describe baseline mismatch and S038-only sufficiency as informed forecasts; F5 is only p=.55. **A green live result must be measured, not assumed from this design.**

## Deliverable: hand-expected witnesses

Own scratch artifact:

`.ufo/waves/round-28/scratch/KengakuR28.MutRegistryDesign-2/registry-witnesses.design.json`

SHA-256: `f9ac6db7ed1a7a1e5ab02867b136d1ff2f9d2b682c5db275079818e6c2c60fbf`.

This is a complete **declarative fixture recipe and expectation set**, not an executable runner, an actual baseline export, or detector output. It specifies the eleven-column Registry table, all 13 row IDs, unchanged committed population bytes, default contents for all 35 files, individual overrides, and each case's full expected findings and S038 projection. Synthetic rows are expressly not source admissions. Main can render the recipe inside an isolated root after receiving the instrument; this seat neither waits for nor reads that implementation.

Notation:

- `A = corpus/knowledge/agent-time-horizon-and-task-validity.md` (population line 19).
- `B = corpus/knowledge/attrib-prior-art-r21.md` (population line 20).
- `NEW = corpus/knowledge/round28-outside-frozen-registry-witness.md` (not in the frozen list).
- Every synthetic selected row starts valid, present once, queued, and uncited, with `used-by = —`. All 35 files exist and contain no source token except A, whose exact initial contents are `S038\n`.
- In every case, unmentioned selected rows remain queued/uncited with empty citing/used-by/missing sets and no findings. Denominators remain 13 configured IDs and 35 configured paths.

| Case | Isolated delta | Hand-expected CLI result | Required S038/path witness |
|---|---|---|---|
| `BASE_QUEUED_CITED` | Initial synthetic state. | exit1; exactly `queued_cited`, `missing_used_by`. | `status=queued`, `citing_files=[A]`, `used_by=[]`, `missing_used_by=[A]`. |
| `GREEN_ALLOWED_CELL_REPAIR` | From base: S038 status `queued→mined`, used-by `—→A`; recheck unchanged. | exit0; no findings. | `status=mined`, `citing_files=[A]`, `used_by=[A]`, `missing_used_by=[]`. |
| `STATUS_ONLY_OMITS_USED_BY` | From base: status `queued→mined` only. | exit1; exactly `missing_used_by`; no `queued_cited`. | `status=mined`, `citing_files=[A]`, `used_by=[]`, `missing_used_by=[A]`. |
| `MISSING_FROZEN_NONCITING_FILE` | From green: remove B, not A. | exit1; `knowledge_missing` at B. | 35 configured paths, only 34 readable; S038's green projection unchanged. Choosing nonciting B avoids confounding this with a removed used-by target. |
| `DUPLICATE_SOURCE_ROW` | From green: repeat the exact valid S038 row inside Registry before `## Paths`. | exit1; `duplicate_source_id` for S038. | Two S038 row occurrences; 14 selected row occurrences but still 13 distinct selected IDs. A last-wins dictionary is not acceptable duplicate detection. |
| `NEW_FILE_EXCLUDED` | From green: create NEW containing `S038\n`; do not modify the population or registry. | exit0; no findings, same frozen source projection as green. | 36 physical knowledge files, **35** frozen readable files; NEW absent from `citing_files` and `missing_used_by`. |
| `PARTIAL_USED_BY_IS_NOT_COMPLETE` | From green: replace B's no-token body with `S038\n`; leave used-by=A. | exit1; exactly `missing_used_by`. | `citing_files=[A,B]`, `used_by=[A]`, `missing_used_by=[B]`; nonempty used-by is insufficient. |
| `QUOTED_LITERAL_COUNTS` | From green: A becomes `> S038\n`. | exit0; no findings. | `citing_files=[A]`, not empty. |
| `FENCED_LITERAL_COUNTS` | From green: A contains a text fence with only S038. | exit0; no findings. | `citing_files=[A]`, not empty. Literal code mentions are not endorsement. |

Compare exact exit, finding-ID set, source/path attribution, configured populations, and the preregistered per-source `citing_files`, `used_by`, `missing_used_by`, and `status`. The JSON top-level schema is not fully declared; the artifact uses a **semantic projection**, not invented production key names. Normalize path/finding ordering, not content. In particular, exit-only checking would miss quote/fence stripping because extra used-by entries do not by themselves require a citation.

## Same-command live red/green contrast — main only, NOT RUN

Use the **delivered, digest-pinned checker outside the replay root**. Keep the same instrument, cwd, environment, root path, population bytes, and argument vectors for all replays. Example constant commands from the lane root:

```sh
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/registry_check.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/scratch/KengakuR28.MutRegistryDesign-2/replay/root --summary
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/registry_check.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/scratch/KengakuR28.MutRegistryDesign-2/replay/root --json
```

These are two separate fixed command vectors, not an assumption that `--summary --json` is a supported combination. `replay/root` has not been created by this seat. The first command is the preregistered counting command with explicit frozen root; the second retains the per-source witness.

1. **Prepare the red state.** Main exports the baseline registry and exactly the 35 baseline knowledge bodies from `b9b247...`, then installs the preregistered population at its expected path as an explicitly disclosed, common detector-input overlay. The population is instrumentation, not a claimed baseline file or repair. Its SHA-256 must be `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014` in both states. Do not obtain the checker from the historical export, where it was absent.
2. **Record actual red output.** Preserve stdout/stderr and exit for both fixed commands. Preregistration expects at least one mismatch including S038's cited-but-queued drift. This seat predicts no exact real-tree finding total or actual missing path. An absent script, malformed setup, or exit2 is not the disclosed red drift and cannot establish the claimed repair.
3. **Enforce reopening before a real repair.** Main needs the original S038 source reopening and the actual frozen citing-file map. Neither is supplied by these synthetic witnesses. Do not infer source support from a Q13 structural result or a checker success.
4. **Apply only S038 mutable cells.** Set cited S038 to `mined`; make used-by the union of its existing valid entries and **every actually citing frozen path**, not merely one path. Recheck may change only as supported by reopening/policy; no gratuitous change is needed for this detector. Preserve all eight immutable S038 cells (`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`), every other row, all 35 bodies, and the frozen population. Record exact old→new status/recheck/used-by in the lesson; distinguish unchanged cells. Keep that lesson outside the red/green checker-input delta.
5. **Replay unchanged commands.** Green means actual exit0 with no C2 findings over the same 13/35 scope. If any other finding remains, report it and F5's outcome; do not change other rows, suppress a finding, remove a path, add NEW to the population, or substitute the synthetic green result. S038-only sufficiency is a falsifiable forecast, not authorization to widen the repair.
6. **Restore and replay.** Restore the exact red registry bytes in this isolated replay root and require the original red outputs again under the same commands. Record registry and frozen-input hashes before/after each state and a cell-allowlist diff certificate. The external checker and population hashes must stay constant. This gives a red→green→red contrast without touching the lane Git index or production bytes.

A full final-tree check can additionally be reported by main, but cannot replace this S038-only causal contrast. C1 and historical P2–P4 have not been tested by this design; two disclosed P4 offline groups and one superseded P4 ID remain limitations, not repaired endpoints or a current-tree census.

## Four prospective one-point checker mutants

These are independent designs requested by the assignment, never combined, and have no asserted implementation line number because the implementation was not opened.

| Mutant | Smallest prospective behavior-point defect | Expected detector/witness | [INFERENCE] plausible mutant symptom |
|---|---|---|---|
| M1: mined-as-complete | At missing-used-by validation, let `mined` bypass the citing-file inclusion check. | `STATUS_ONLY_OMITS_USED_BY`; also the nonempty partial-used-by variant. | Drops `missing_used_by` or misreports its set, possibly false exit0 after status-only repair. |
| M2: missing-path filter | Before traversing frozen paths, discard members that do not exist instead of reporting them. | `MISSING_FROZEN_NONCITING_FILE`. | No `knowledge_missing`, reduced denominator, or false exit0 for a 34/35 readable population. |
| M3: last-wins source map | At duplicate-ID handling, overwrite the earlier registry row without recording duplication. | `DUPLICATE_SOURCE_ROW`. | Clean per-source values hide the duplicate; `duplicate_source_id` disappears. |
| M4: current-tree discovery | At candidate-file enumeration, replace the explicit frozen list with recursive current knowledge discovery. | `NEW_FILE_EXCLUDED`, whose correct result remains green and unchanged. | False `missing_used_by` for NEW or a widened 36-file denominator. Do not “repair” the fixture by adding NEW to used-by. |

**Bounded detector definition for later execution:** compare the CLI's actual exit/findings/per-source projection to the hand-expected case. All chosen cases must satisfy their expectations with the pristine instrument before any mutant is scored. A deliberately red fixture (expected CLI exit1) is a passing behavioral control only when its expected finding and path are present; a raw nonzero alone is never kill evidence. Thus live baseline drift is not confused with a broken pristine mutation-test control.

For each prospective source-code mutant, main should use one isolated scratch copy and the **same bounded case detector** for pristine → mutated → exact-byte restored bytes. Pin checker/input hashes and retain every command/output. Only a pristine-matching, mutant-mismatching, restored-matching triplet supports **killed**. An unchanged mutant outcome is **survived**, a coverage finding, not permission to revise C2. A failed pristine control, failed restoration, timeout/setup failure, or missing output is **inconclusive**. A red nonzero without the expected semantic witness is also inconclusive.

## Actual commands, outputs, and restoration evidence

Only two shell commands ran, both read-only SHA-256 provenance measurements. File reads/searches opened the local preregistration, population, assignment interface, and applicable skill/protocol interfaces. No detector was invoked.

Command 1, cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`:

```sh
sha256sum plans/round-28-claims.md plans/fixtures/r28/registry/population.json .ufo/waves/round-28/build-spec.json /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md
```

Command 2 used the same arguments plus:

```text
.ufo/waves/round-28/scratch/KengakuR28.MutRegistryDesign-2/registry-witnesses.design.json
```

Both completed exit0. Actual output hashes for each read-only input were identical before and after writing the scratch design:

| Input | Before SHA-256 | After SHA-256 |
|---|---|---|
| `plans/round-28-claims.md` | `8b2e237a05b15dc2f10a62a19947ab8b15120af3c16ae9cf245da1945c485a5f` | Same |
| `plans/fixtures/r28/registry/population.json` | `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014` | Same |
| `.ufo/waves/round-28/build-spec.json` | `2a9a2e0932c6e12638cfb27bd28c07ee3fe6b46331185ba98b77d402c48af204` | Same |
| Canonical `protocol/CORPUS.md` | `b6ed4476b0d1a5a3176ce728e4eb44997bddfa6dfb9fdb2f1a15e81d3f0821bf` | Same |

The only writes were this unique report and the named own-scratch JSON artifact. **No mutated/restored checker hashes or empirical detector output exist.** Restoration of a mutation is not applicable because none was applied. Matching interface-input hashes establish only that those four inputs stayed unchanged, not a whole-tree or production-registry restoration claim. The fixture hash above is artifact provenance, not mutation evidence.

## Limitations and final disposition

- Actual S038 old cells, frozen citations, original-source opening, complete baseline findings, final repair success, and concrete implementation mutation locations remain unmeasured by this deliberately interface-only seat.
- All fixture exits/findings are **hand-expected**, not observed. They neither kill a mutant nor prove the delivered selftest covers these cases.
- This design does not cover all other preregistered C2 controls, execute two-way C1/C2 separation checks, revise source rows, admit knowledge, add a QUALITY criterion, change scores, or supply non-author closure.
- There is no missing prerequisite to the assigned design deliverable. Empirical acceptance belongs to main's later isolated runs, not to this report.

**Scoped final verdict: PASS for the mutation-design assignment only; empirical mutation and C2 repair status INCONCLUSIVE / NOT RUN.**

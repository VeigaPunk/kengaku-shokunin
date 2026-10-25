writer: KengakuR29-2.FMutSourceContract-2

# FMutSourceContract: round-29 falsify of the source-contract extractor

Scope: mutation-test the instrument's own tests (`--selftest`) and audit outputs (`--summary`, `--json`) against a source-contract extractor that accepts (O) swapped replacement order, (L) a literal RHS, or (E) an extra replace step. Lane master 56fd949a6478342531e61f4feecb4a685d831640. Lane never edited.

Provenance and independence:
- Production source READ: `plans/config_projection.py` and `plans/fixtures/r29/generate_test_data.py`. This item targets that source, so it is not an independent-oracle item.
- The re-derivations in section 6 read pinned bytes only and did not import the production module.
- Labrat: not dispatched. This seat is a leaf (ROLE: never spawn or delegate) and the contract forbids subagents; the lane-bounds clause naming one labrat is superseded.
- Tooling: no installs or upgrades. Used python3 3.14.8 (already present) and coreutils. No pacman.
- Working copies: `/tmp/r29-mut/{pristine,control,mutO,mutL,mutL1,mutE,authorO,authorI,probeO,probeOm,probeL,probeLm,probeE,probeEm,probeL1m,unpinned}/plans` (`cp -a` of the lane tree). Probe copies `probe*m`, `probeL1m` retain their mutant lines by design (they are the re-pin evidence). All four sandboxes and both author-row copies were reverted and hash-verified.

## 1. Controls (reproduction of the reference)

Pinned hashes, observed by `sha256sum` on the lane:
- `plans/config_projection.py` 5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3 (matches mutation-witness.txt line 1)
- `plans/fixtures/r29/manifest.json` f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87 (= MANIFEST_SHA256, line 24)
- `plans/fixtures/r29/generate_test_data.py` 45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd
- `plans/fixtures/r29/profiles.json` 90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018
- `plans/fixtures/r28/webarena/config_files/test.raw.json` 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652

Control copy (unmodified, sha 5673405e...), Python 3.14.8:
- `--selftest` exit 0; stdout `SELFTEST clean cases=20 ...`. The 20 names equal build-selftest.txt line 1.
- `--summary` exit 0; last line `TOTAL findings=0 exit=0`; stdout sha256 5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f.
- `--json | sha256sum` = c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630, equal to build-json-sha256.txt.
- Lane instrument, read-only: `--summary` exit 0; `--json` sha c8da0c5a... (same).

Receipt defect (mismatch 1): mutation-witness.txt line 2 is cut mid-name (`...units_n`). The full list is in build-selftest.txt line 1.

Commands (each mutant and probe): `python3 <root>/plans/config_projection.py --root <root> --selftest`, then `--summary` and `--json`, where `<root>` is the copy directory.

## 2. Mutants (one minimal edit each; copy-only)

Edits are in the extractor only. Line numbers are the lane's.

| Mutant | Exact edit in copy | `--selftest` | `--summary` | `--json` |
|---|---|---|---|---|
| O: accepts swapped order | L84 `if [...] != [...]:` becomes `if sorted((s["token"], s["name"]) for s in steps) != sorted(("__%s__" % name, name) for name in ORDER):` | exit 1; `AssertionError: order_swap` raised at selftest line 473 -> KILLED | exit 0; sha 5ce5cb0f = control -> SURVIVED | exit 0; sha c8da0c5a = control -> SURVIVED |
| L: accepts literal RHS | L75 `isinstance(call.args[1], ast.Name)` becomes `isinstance(call.args[1], (ast.Name, ast.Constant))`; L79 `call.args[1].id` becomes `getattr(call.args[1], "id", call.args[0].value[2:-2])` | exit 1; `AssertionError: literal_rhs` at line 473 -> KILLED | exit 0; = control -> SURVIVED | exit 0; = control -> SURVIVED |
| E: accepts extra step | L84 becomes `if [(s["token"], s["name"]) for s in steps][:len(ORDER)] != [...]:` | exit 1; `AssertionError: extra_step` at line 473 -> KILLED | exit 0; = control -> SURVIVED | exit 0; = control -> SURVIVED |
| L1: variant of L (L75 only; `.id` unguarded) | L75 as in L | exit 1; uncaught `AttributeError: 'Constant' object has no attribute 'id'` at L79, reached via L468; no designed assertion reached -> KILLED by accident | exit 0; = control -> SURVIVED | exit 0; = control -> SURVIVED |

Unrelated-to-kill note: the selftest's `except Unevaluable` (L469) is the only handler inside selftest, so an assertion and a crash both exit 1.

Answer to "can frozen real data alone detect it?": NO, for O, L, E and L1. Observed reasons:
- The pinned generator is conforming. The mutants accept exactly what the pinned extractor accepts, so the real-data run never takes a different branch.
- Generator bytes are pinned. Changing them without re-pinning stops the audit at `read_pinned` (lines 100-114) with `snapshot_tampered` before the extractor runs (section 5).
- Even when accepted, the extracted contract does not drive output. `project()` iterates the module constant ORDER (lines 143-146) and the profile values. For the three frozen profiles, forward, swapped and reversed orders give identical text (section 6), so a wrong order cannot change the summary.

## 3. Re-pinned end-to-end probes (pin refreshed to a non-conforming generator)

Each probe copy has its generator edited, its manifest generator sha re-pinned (`write`), and MANIFEST_SHA256 at line 24 re-pinned. The control extractor and the mutant extractor run on identical bytes.

| Probe | Generator edit (copy) | Extractor | Exit | `--summary` sha / finding | `--json` recorded contract |
|---|---|---|---|---|---|
| probeO | L11/L12 swapped (REDDIT first) | pristine | 2 | cf2f93d6...; `source_contract_unrecognized`, detail "replacement tokens/order/names differ"; observed starts `__REDDIT__` | - |
| probeOm | same | O | 0 | 5ce5cb0f = control; 0 findings | replace_steps begins `["__REDDIT__","REDDIT",11]` |
| probeL | L16 RHS literal `"http://map.invalid:19999"` | pristine | 2 | d76a5fef...; `non-literal replace step`, line 16 | - |
| probeLm | same | L | 0 | 5ce5cb0f = control; 0 findings | `["__MAP__","MAP",16]` (literal RHS recorded as name MAP) |
| probeE | `raw = raw.replace("__page__", PAGE)` after L16 | pristine | 2 | 9a3a0d26...; "replacement tokens/order/names differ", 7 observed steps | - |
| probeEm | same | E | 0 | 5ce5cb0f = control; 0 findings | `["__page__","PAGE",17]` accepted |
| probeL1m | literal (as probeL) | L1 | 1 (both modes) | stdout empty (sha e3b0c442, zero bytes); uncaught AttributeError at L79 | - |

Findings:
- The pristine extractor exits 2 on all three non-conforming re-pins with the designed finding id. Each mutant exits 0 with a `--summary` byte-identical to the clean control. Under the exit contract this is a certifying survivor.
- Only `--json` records the non-conforming contract (`source_contract.replace_steps`). Under L the literal RHS appears as name MAP.
- [INFERENCE, not executed with env values] Upstream semantics: with the literal probe, upstream would replace the 133 `__MAP__` occurrences (summary `ORIGINAL_OCCURRENCES_BY_TOKEN`) with the literal, while the instrument uses profile MAP values. With the extra-step probe, upstream would replace the 12 `__page__` occurrences (summary `OTHER_MARKERS_NOT_ENV_TOKENS`), which the instrument leaves in place. Neither divergence produces a finding.

## 4. Selftest on re-pinned mutant copies (what kills them after a refresh)

- probeOm: exit 1; `AssertionError` at line 461 (`assert [s["name"] ...] == list(ORDER)`, the real-data names check).
- probeLm: exit 1; `AssertionError: literal_rhs` at line 466 (`assert mutated != source, name`). The synthetic text no longer matches the re-pinned generator, so this kill is a harness text-match failure, not extractor behavior. The line-461 names check passes because L derives names from the token.
- probeEm: exit 1; `AssertionError` at line 461 (7 names, not ORDER).

So after a refresh, real data kills O and E only through the line-461 names check, and L only through a text-match artifact.

## 5. Unpinned generator change (control)

Generator bytes changed, pins untouched (`/tmp/r29-mut/unpinned`): `--summary` exit 2, `TOTAL findings=1 exit=2`; `--json` exit 2 with finding `{"id":"snapshot_tampered","path":"plans/fixtures/r29/generate_test_data.py"}`. The extractor is not reached.

## 6. Re-derivation from pinned bytes (no production import)

For distinct_origins, path_prefix and trailing_slash_sensitivity: forward == swapped == reversed order (true for all three); no profile value contains `__`; full sha256 of the forward projection equals the receipt's projected_text_sha256: 2aec098e..., 54cf9833..., 49bbee2e....

Hand cascade fixture (R29_ORDER_CASCADE_01): forward text equals expected_projected_text; reversed text does not equal it and does equal predicted_mapping_order_mutant_text.

## 7. Reference rows (mutation-witness.txt)

- control: reproduced exactly (section 1).
- wrong_order_reversed: the receipt does not record its edit. Natural reading, `for name in reversed(ORDER):` at line 143: selftest exit 1 with `AssertionError` at line 416 (`escaped_token_not_replaced`), so the cascade assertion at line 438 is never reached. Summary exit 0, `TOTAL findings=0 exit=0`, stdout sha 65eeef25 (bytes differ only in applied_replacements key order). The kill comes from an earlier, unrelated case; the cascade fixture would also reject the reversed text (section 6).
- index_by_task_id: natural reading, `"output_index": task.get("task_id")` at line 330: selftest exit 1, `AssertionError` at line 456 (`hand_index`); summary exit 0, `TOTAL findings=0 exit=0`, sha = control.
- url_only_substitution: NOT reproduced. The receipt has no edit text. The build-seat specs (`scratch/R29MutUrlOnly-2/mutant-spec.json`, `scratch/R29MutOrder-2/mutant-spec.json`) are design-only (`observed_experiment_status`: NOT RUN / INCONCLUSIVE) and specify no production edit. The reproduced rows use natural readings, so they confirm outcomes, not the author's exact edits.

## 8. Mismatches (exact location and value)

1. mutation-witness.txt line 2: truncated at `...units_n` (receipt defect; full list in build-selftest.txt line 1).
2. Exit taxonomy: an uncaught `AttributeError` (probeL1m) exits 1 with empty stdout. The documented taxonomy reserves 1 for a projection or invariant finding and 2 for could-not-evaluate. `main()` catches a fixed tuple at line 538 (`OSError, ValueError, KeyError, TypeError, AssertionError, IndexError`) that omits AttributeError.
3. Kill quality: selftest exit 1 does not separate an assertion from a crash (L1 kill, section 2).
4. Mutant L after a refresh is killed by the line-466 text-match check, not by extractor behavior, and the real-data names check (line 461) is blind to a literal RHS (section 4).
5. Byte-level summary drift without findings: the reversed-order reading changes the summary bytes (sha 65eeef25 vs 5ce5cb0f) while findings stay 0. Not a finding; the summary is not order-invariant byte-wise.

## 9. Evidence

- Summary texts for each run: `.ufo/waves/round-29/scratch/falsify/FMutSourceContract/` (control, mutO, mutL, mutL1, mutE, probeO, probeOm, probeL, probeLm, probeE, probeEm `.summary.txt`).
- Hashes and exits are as reported above. JSON outputs were hashed, not saved, because they are large.

## 10. Verdict and handoff

- Killed by selftest on the pinned tree: 3 of 3 (L1 by accident).
- Survived real-data `--summary` and `--json`: 3 of 3. Frozen real data alone cannot detect them.
- Survived a refreshed-pin end-to-end audit (exit 0, byte-identical summary): 3 of 3 (the pristine extractor exits 2 on each).
- No checks are requested from the main agent: this item is read-only against the lane, and its artifacts are in the copies and the scratch directory listed above.

VERDICT: PARTIAL

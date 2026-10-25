# Kengaku R26 FxFamilyG1 — family G1 only

## Finding — P2: token fallback can be an equal-token no-op

- `plans/grader_perturb.py:359-387` writes the fixed `__perturbed_token__` for the first list string without checking it differs. `apply_family` (`:450-457`) accepts the result whenever serialization changes; `family_stats` (`:519-541`) counts every accepted transform in `n`. Amendment 1 (`plans/round-26-claims.md:186-187`) requires a distinct, actually graded value.
- Reproduction against the production G1 path, with a baseline-PASS state whose answer is an indented `{"x":["__perturbed_token__"]}`:
  `python3 /tmp/fx_family_g1_edge.py` — exit 0
  ```
  applies=True
  raw_changed=True
  answer_changed=False
  regraded_pass=True
  mutation_success=False
  ```
  Therefore this case enters the MC denominator despite no meaning-changing mutation. `plans/fixtures/r26/perturb_oracle.py:241-265` uses a token distinct from the selected string. This is a real generic-input edge, not a pinned-population failure.

## Frozen-raw result — independently recomputed

- Independent script reads all four raw JSONL files, checks each SHA-256 pin, regenerates non-C wants from `meta`/`meta2`, replays the baseline grader, mutates and regrades each G1 candidate. Command: `python3 /tmp/fx_family_g1_recompute.py` — exit 0.
  ```
  PIN_SHA256 matches=4/4
  POPULATION raw_ok_candidates=1964 baseline_pass=1021 baseline_fail=943 baseline_mismatches=0 meta_want_mismatches=0
  G1 exclusions={"baseline_fail": 943}
  G1 n=1021 k=1021 rate=1.000000 CP95=[0.996394,1.000000]
  G1 format_strata={"FJ1": 710, "FJM": 268, "MULTI": 17, "DANGLE": 17, "BARE": 9}
  G1 pid_composite n=143 k=143 rate=1.000000 CP95=[0.974534,1.000000]
  G1 mutations={'integer': 996, 'list-token': 25} semantic_noops=0
  ```
  All 943 baseline FAIL records are excluded by MC precondition; every baseline PASS has an answer, mutatable value and answer span. All 1,021 changed parsed values are actually rejected by the applicable state/sequence/C grader. No sentinel collision occurs in these frozen raws; thus the current finite-population G1 result is valid. CP95 is nominal/descriptive, not an iid generalization claim.
- Exact instrument command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/grader_perturb.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --summary` — exit 0. Relevant output:
  ```
  FAMILY G1 kind=MC n=1021 k=1021 rate=1.000000 cp95_nominal=[0.996394,1.000000] verdict=PASS composite=143/143@1.000000 cp95_nominal=[0.974534,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
  CLASSES G1 FJ1=710/710@1.000[710/710;0/0]cp95_nominal=[0.995,1.000] FJM=268/268@1.000[268/268;0/0]cp95_nominal=[0.986,1.000] MULTI=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] DANGLE=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] BARE=9/9@1.000[9/9;0/0]cp95_nominal=[0.664,1.000]
  ```
- Independent-oracle command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r26/perturb_oracle.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin` — exit 0; `G1 kind=MC n=1021 k=1021`. Aggregate agrees; oracle does not report G1 strata or pid composites. Instrument `--selftest` also returned `SELFTEST G1 PASS` and `SELFTEST TOTAL families=10 failed=0` (exit 0).

## D1 separation and draft review

- Amendment 1 (`round-26-claims.md:188-191`) says D1 is PC, baseline-PASS, turn>1 ordinary state/sequence operations, previous truth different from want; k is appended-block capture, not correctness invariance. Code matches: `FAMILY_KIND` marks PC; `apply_family` (`grader_perturb.py:438-449`) enforces those conditions and excludes A-MONO/B/C; `_metric_success` (`:490-493`) checks extracted output equals previous truth. Output is `D1 kind=PC n=909 k=909 capture_rate=1.000000 ... verdict=NOT_SCORED`; D1 is not mixed into G1/MP.
- Draft `grader-perturbation-audit.md:48-52,69-71,81-85` describes G1’s pinned result and D1’s PC interpretation correctly. However, its general G1 statement that the mutation changes a graded value is not guaranteed by the implementation: qualify/fix the token collision before relying on the entry beyond these pinned records. The 1021/1021 frozen result itself does not need correction.

## Verification gaps / residual risk

- No LSP device is mounted (`read xd://lsp` returned “No such tool”); therefore no LSP status, references, definition or diagnostics were available. Source review used direct reads; grep was used only to locate `GRADED_CELLS`, not as semantic proof. No tools installed; no production files changed.

VERDICT: G1 frozen-population result passes and matches oracle; P2 distinct-token applicability defect survives for generic inputs. Report: .ufo/waves/round-26/falsify/FxFamilyG1.md

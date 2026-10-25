writer: KengakuR29-2.FCritOracleIndependence-2

# FCritOracleIndependence — authorship and discrimination attack

Scope: round 29 C1, not round admission. All relative locations below are rooted at `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Axes

Judged axis: novelty, specifically evidence for acquired offline generated-config projection capability. Supporting attack axes: independent authorship, non-circular derivation, discriminating coverage, exact provenance and bounded interpretation. Calibration/model/deployment claims are outside scope.

**Production source disclosure: YES.** This critic read production lines 425–470 in the earlier portion of this review (recorded in `scratch/falsify/FCritOracleIndependence/strict_audit_v3.txt:11–12`). Consequently NONE of my scripts or comparisons qualifies as the prereg's no-production-read independent oracle. Their headers' claim of derivation from text/data is not an assertion of compliant author independence. They are adversarial diagnostics only. No production edits, integration or admission performed.

## 1. Dead executor does not transfer authorship — fixable evidentiary defect if credited

Observed: `build-dead-seats.json:16–23` records R29ExecOracle, agent KengakuR28.R29ExecOracle-2, `report=null`, `final_output_bytes=0`. Lines 7–14 and 25–32 record the same absence for core/case executors. The integrated instrument's author is KengakuR29-2 under the canonical assignment. A dispatch or dead-seat identity is not a delivered oracle.

Prerequisite: `plans/round-29-claims.md:79–82` requires a separately authored oracle, no production read/import, its own census/leaf walk, explicit domain limits, and comparison of every required metric and object. It does NOT require that author to be the originally dispatched build executor, or require oracle delivery before the crash.

**Smallest safe correction:** retain dead-seat attribution as dead, name the actual returning falsify author and exact script/output digest, and credit that replay only. A coordinator-authored alternate implementation cannot inherit the dead executor's independence. A fresh seat in this wave CAN satisfy the stated authorship condition; rejecting it merely because the coordinator wrote production would add an unregistered rule.

## 2. Strong counterexample: complete population agreement does not establish source semantics

Observed experiment: `scratch/falsify/FCritOracleIndependence/discrimination.py:68–75` defines the seven variants; `:111–137` compares exact projected objects, filenames, upstream-format digests and changed-leaf pointer/original/projected triples. It authenticates raw/profile pins (`:22–31`). Command exercised earlier:

`python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FCritOracleIndependence/discrimination.py /tmp/fcoi_prod.json`

Retained stdout: `scratch/falsify/FCritOracleIndependence/discrimination.out:1–16`; exit 0. Instrument capture was 3,881,050 bytes, SHA256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` (earlier command output), matching the frozen JSON receipt.

| Variant | Exact agreement on all four compared classes, task/profile records |
|---|---:|
| faithful serialized sequential source order | 2436/2436 |
| reversed serialized replacement order | 2436/2436 |
| simultaneous single-pass serialized replacement | 2436/2436 |
| sequential decoded keys/values | 2436/2436 |
| reversed-order decoded keys/values | 2436/2436 |
| filename from task_id instead of enumeration | 2436/2436 |
| URL-fields-only decoded substitution | 2382/2436 |

The URL-only first mismatch is distinct_origins, output_index 66/task_id 66, in projected_task, would_be_file_sha256 and changed_leaves (`discrimination.out:8`). `positive_control.out:3` records 18 mismatching tasks per profile and 183 omitted non-URL leaf changes across the three profiles: raw annotation 3, must_include 180. These are deliberately wrong comparator outputs, NOT production defects.

Discriminating hand cases reject reverse/simultaneous replacement and ID-based filenames (`discrimination.out:11–15`). Exact cascade mismatch: `plans/fixtures/r29/hand/cascade-order.case.json:25–26` expects `/0/start_url=https://map.invalid/order/probe`; lines 33–34 predict `/0/start_url=__REDDIT__/probe` for wrong mapping-order/simultaneous semantics. Sequential decoded rewriting still passes this cascade, so a cascade alone does not distinguish text from sequential decoded replacement. Quote/backslash cases are necessary for that boundary (`discrimination.out:10,13`).

Comparator sensitivity control: corruption at path_prefix, output_index 452, `/452/start_url` drops object agreement from 2436 to 2435 and locates that record (`positive_control.out:1–2`). This is diagnostic sensitivity, not comprehensive mutant coverage.

**Classification:** intrinsic frozen-domain tradeoff, not a production defect. [INFERENCE] A claim that these 2436 agreements prove replacement order, generalized text/leaf equivalence or ordinal semantics must be rejected; additional author identities do not create distinguishing inputs. Smallest correction: preserve frozen-population agreement as bounded evidence and separately pair it with exact hand expectations/mutant outcomes. Do not change the frozen population or inflate independent sample counts.

## 3. Returned fresh evidence is meaningful, but not completely blind

Observed returned reports:

- `falsify/FOracleText.md:7–12,21–32`: actual writer FOracleText-2 declares no production read/import; compares 2436 records, 4248 changed leaves and 1435 provenance records. One reporting-unit disagreement is explicitly retained: `index_mapping.index_equals_task_id`, oracle 2436 task/profile records versus instrument 812 input tasks. Smallest correction: normalize both to input-task units in the comparison while retaining both raw values; not a failed projection.
- `falsify/FOracleProvenance.md:8–10,21–32`: actual writer FOracleProvenance-2 declares no production read/import; own scanner matches all 1435 records. Its initial path-template spelling `eval.program_html.[].url` differed from instrument `eval.program_html[].url`; 398 membership/field mismatches were resolved by formatting normalization. Treat that as convention alignment, not independent discovery of the instrument's exact serialization convention. Preserve raw paths and compare semantic identity before rendering adaptation.
- `falsify/FOracleIndex.md:38–64`: independent source-order serialization matches all 2436 claimed file digests. Re-dumping the emitted, key-sorted projected_task does not: distinct_origins index 0 claimed `9533088e31781047e4c4f3b9cafe02f734aaaa3fb9c47ebc29176bd8d6a6e5e6`, emitted-object re-dump `823a9a7fd4ca2b16ae5d6e0c7966f22584691845bdb675832ad56983085aebcd`. Smallest correction: state digest serialization uses original generator key order; hashing only emitted objects cannot be the independent digest oracle.

My historical tool-call snapshot (`strict_audit_v3.txt:1–16`) found no detected source reads for the named oracle seats, but it is a heuristic snapshot, not proof of everything they ever saw. FOracleText consumed production output at 16:48:31.025Z before a script write was recorded in that snapshot; the case-000 oracle write at 16:47:52.078Z likewise followed production execution at 16:47:25.136Z. This does not violate prereg: output comparison is expressly allowed. [INFERENCE] It permits output-conditioned conventions, hence weaker blindness than a precommitted oracle. Do not call it blind or independently model-calibrated. Smallest safe evidence package: actual writer, no-source disclosure, frozen oracle bytes, authenticated inputs, independently derived expected values, separate comparator, complete diff and recorded oracle corrections. Freezing expected outputs before viewing production would strengthen evidence, but is not an added prereg requirement.

## 4. Concrete returned-oracle mismatches requiring correction

**Fixable method mismatch:** `falsify/FOracleLeaf.md:24–29` describes SINGLE-PASS combined-regex decoded substitution with no rescanning. The canonical FOracleLeaf assignment (falsify-spec.json item FOracleLeaf, also supplied in this review's earlier command output) specifies decoded keys/values substituted in source order. These are different algorithms outside the benign domain. At report `:96–99`, H3 reports a difference for a later token introduced by GITLAB; sequential decoded rewriting cascades just like sequential text rewriting and does not differ there (my diagnostic `discrimination.py:62–65`, `discrimination.out:10,13`). Smallest correction: implement/report sequential decoded substitution for the assigned oracle, retaining single-pass rewriting only as a separately named negative control; use quote/backslash/escaped-marker cases to demonstrate actual text-versus-decoded differences. Benign 2436-object agreement remains useful, but does not repair this method substitution.

**Fixable false provenance:** `falsify/FOracleLeaf.md:84–87` says upstream would produce no test.json after quote-induced JSON failure. Pinned generator `plans/fixtures/r29/generate_test_data.py:17–20` writes test.json BEFORE parsing. Exact correction: malformed test.json is already written; no per-index output is reached in a clean directory. This is source-order evidence, not a deployment claim.

**Fixable overstatement:** `falsify/FOracleLeaf.md:61–69,133–135` calls D1–D5 an iff/exact equivalence boundary. Its own `:100–103` gives agreeing cases outside the no-cascade restriction. These are useful sufficient benign-domain conditions, not demonstrated necessary conditions. Smallest correction: label them sufficient checked preconditions, retain outside-domain agreeing controls, remove iff/exact/general necessity language.

## Evidence hygiene and scope of my experiments

No installs/upgrades; Python 3.14.8 observed in earlier command output. No REA, network, host service or package transactions performed.

Earlier in this review, `gen_witness.py` executed copied upstream generator bytes in `/tmp/fcoi_gen` with synthetic stub values. This went beyond the assigned critic's no-other-runtime posture; it is NOT eligible independent-oracle evidence and is not needed for the source-order objection above. Further, `gen_witness.out:17` is stale: it predates a fix to dictionary-based filename comparison at `gen_witness.py:105–107` and incorrectly shows ID-based naming agreeing on the shuffled case. Do not credit that row or treat the existing output as a run of current script bytes. The separate `discrimination.out:15` correctly rejects ID naming on the shuffled fixture. No generator execution was repeated after resumption.

No direct prose source quotations are used here; identifiers, paths, values and command/result tables are technical evidence, not quoted passages. My diagnostic comparison is explicitly source-exposed, not a replacement for the fresh oracles. No production finding was demonstrated by my faithful comparator; the retained objections are evidence qualification, returned-oracle method mismatch and boundedness errors.

## Scoped conclusion

Fresh post-crash authorship is allowed by the prereg and returned separately named oracles supply substantive agreement evidence; the dead build seat does not supply any. Unqualified independence/blindness and complete semantic certification are unsupported. Correct the leaf oracle's algorithm/claims and the listed provenance/serialization/unit disclosures before describing the whole package as satisfying every prereg oracle requirement. This is an evidentiary correction request, not a novelty-score decision or round admission.

VERDICT: PARTIAL

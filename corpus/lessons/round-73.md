# Round 73 — kengaku (2026-11-03/04 UTC)

Base `d96c3e62fd01771718368688c2685dceeef5b83e`; freeze `255c261db2119906c70195291a2b6f9f46f82a72`;
row landing and amendments `ea41880fa755816d2c21a7ee53e14bf95d95e340`.
R73-C1 targets coverage: include plans documents in the advertised instrument universe and register the missing instruments.
R73-C2 targets calibration: compare registry declarations to source/schema observations.
**Both original claims are not admitted.** Engineering-green amendments do not replace frozen verdicts.

## Gate

- **S249 admitted for its narrow API scope**, not as proof of registry correctness. URL opened by
  L1 and SourcesAstR73 this round: https://docs.python.org/3/library/ast.html#ast.parse,
  access date 2026-11-04 UTC, page title Python 3.15.2. Capture:
  `corpus/evidence/round73/sources/ast-docs.html`, HTTP 200. Located quote, capture line 2680:
  **“Parse the source into an AST node.”** Seven whitespace-delimited words —
  `python3 -c "print(len('Parse the source into an AST node.'.split()))"` → 7.
  `wc -c corpus/evidence/round73/sources/ast-docs.html` → 362493;
  `sha256sum corpus/evidence/round73/sources/ast-docs.html` →
  `94bead0ac6482efc08bbc790acb1cff809ca4b8a9829a1def2245451a42fe809`.
  Fetch details and independently located anchors:
  `.ufo/waves/round-73/w1/SourcesAstR73.md` and
  `corpus/evidence/round73/sources/ast-anchor.md`. Kind docs, tier A only for Python's AST API.
  Registry change: absent → S249 mined, recheck on-release, used-by this lesson and the held
  `corpus/knowledge/instrument-registry-derivation.md`. No pre-existing row status/recheck/used-by changed.
- **Reject the stronger candidate inference “AST parse proves executable validity.”** Same source,
  capture lines 2708–2715 explicitly warns successful AST parsing does not guarantee executable code
  and omits scoping checks. Flip: controlled execution of the exact declared command plus independent
  exit/output comparison. S249 is not a runtime-certification source; no extra row duplicates the URL.
- **Held knowledge candidate** `corpus/knowledge/instrument-registry-derivation.md` (writer's draft:
  KnowledgeEntryR73; L1 integration). Provenance trio first, source S249. It documents structural
  checks and explicitly records missing semantic/runtime coverage. Admission remains hold pending a
  qualifying complete Q10/Q13/Q14 reread; source admission is not entry admission.
- **Earlier HF candidates remain held.** `corpus/knowledge/tb2-hf-model-inference-offline.md` and
  `corpus/knowledge/tb2-hf-model-inference-provenance.md` are not newly admitted here. See
  `.ufo/waves/round-73/w1/EntryFalsifyR73.md` and `corpus/evidence/round73/w1/entry-hold-review.md`.
  A qualifying source/number reread, not merely the name of a second wave, is the missing evidence.
- **Assimilation: none.** No staged shokuknow row appended. The latest operator reflection,
  `considerthese/2026-10-26.md:44-49`, proposes a standing TB2 admission counter with a filler control.
  It is considered but not implemented: this round freezes registry-universe/structural checks, not
  grader-package admission. The operator reflection is a pointer, not support for either claim.
  Package mass-id-drift question `kengaku | round-54` remains open; no source-repo writes occurred.

## Mistakes

| id / class | evidence pointer | captured-by | fix / disposition |
|---|---|---|---|
| M73-1 vacuous — landing predicate contradicts registration | `corpus/evidence/round73/a1-red-green.txt`; C1CriticR73 deterministic registered fixture | Q46/Q48 should have required the projected registered tree | Same tree: frozen counter exits 1 because plans_only=0, amended counter exits 0 using plans_seen. This proves the repair can fail, not admission of A1. Original claim stays not admitted. Q54 added. |
| M73-2 number-drift — exact denominator changes under the other claim | `c2-red-before.txt` total106 versus `c2-after.txt` total114; C2CriticR73 | AXES causal-separability rule; no projected-tree freeze check | Record original106 as missed, amended114 separately. No numeric axis increment. Q54 prohibits a fixed denominator changed by planned work. |
| M73-3 attribution — “no result returned” mistaken for “no scoring happened” | `plans/round-73-claims.md` A1/A2 and E-R73-1; RegistryReviewerR73 read the original before amendments | protocol freeze-before-data rule | E-R73-1 withdraws the timing inference; no re-scored admission. |
| M73-4 reference-drift — future-looking amendment heading times | A1/A2 say 02:54/02:56Z but `git show -s --format='%H %cI' ea41880f` is 02:48:24Z | Evidence standard; Q50 | Append E-R73-1 with actual committer timestamp. Earlier bytes preserved. |
| M73-5 survivor — structural audit read as semantic truth | `c2-blindspots.md`, `c2-critic.md` | Q3/Q4; frozen eight-field description too broad | Record accepted malformed rows, nonexistent pins, false flags and contradictory errata. Do not tighten a scored rule. Held entry states parse-survivor universe and substring checks. |
| M73-6 reference-drift — newly written row names nonexistent r69 receipt | C1RowAuditR73, exact entry returns 2 receipt-missing | Gate standard registry; new audit checks script existence only | Correct entry to existing receipt-v2.txt; its legitimate historical predicate remains red (seen_f=6/8), not falsely green. |
| M73-7 scope — new row scopes omit host locks/output paths | C1RowAuditR73 rows r66/r69/r70; draft JSON | Gate standard Scope | Integrate independent row draft: optional receipt/evidence writes, home locks, shared-loopback services and cleanup responsibility disclosed. |
| M73-8 number-drift — old five-cell tensor row silently skipped | C2CriticR73 denominator reconstruction; old SKILL.md:688 | no malformed-line leg in audit | Remove obsolete malformed tensor row after adding its complete eight-cell replacement; original source remains in history. Frozen parser unchanged and its hole recorded. |
| M72-V1 reference-drift — dead report hash | `corpus/lessons/round-72-verifier-spotcheck.md:136-140` | Q50 | Correct citation in this round's report errata to 08df910ab461620741d433def3df38a8406efe9f; no historical report rewrite. |
| M72-V2 attribution — census revision label | `corpus/evidence/round72/census-after.txt:2-3` | Evidence standard measured revision | Its b6336136 label is not the final rerun. File first ships with 08df910ab; db78d059 reruns three other receipts only. Record the boundary, not an invented exact historical worktree. |
| M72-V3 vacuous — negative rejection sweep not reproducible | round72 verifier §6 item3, lesson ground(iii) | CORPUS negative-sweep rule/Q9 | Withdraw ground(iii)'s no-hits premise; sweep returns unrelated battery lines. Earlier refusal remains on triad/source-id provenance grounds alone. |
| R71-R2 attribution — report counter revision | `corpus/evidence/round71/final-c2-gate.txt:1` | Q50 | Correct report attribution edaea66e to receipt REV c80fcdb3761035a711aaa7f1edfabaaa5da01eb3; filed bytes stay unchanged. |

## Measurements and controls

All commands below are lane-root-relative; receipts retain UTC run timestamps.

- C1 before: `python3 plans/round52_c2_registry.py --lane .` on base bytes:
  ADVERTISED110, MISSING5, rc1 (`c1-before.txt`). Widening first exposed two additional existing
  plans-only instruments, round32_c1_verify and round32_defects. Registration subsequently
  advertises these through SKILL.md too: final ADVERTISED113, MISSING0, plans_only0.
  `a1-red-green.txt` demonstrates original R73-C1 fail/rc1 versus A1 pass/rc0 on identical bytes.
- C2 before: frozen audit over base tree: total106, MISMATCH2, rc1 (`c2-red-before.txt`).
  Current engineering run: total114, MISMATCH0, rc0 (`c2-after.txt`). Original exact106 target misses.
- `--selftest`: C1 cases4 failures0; C2 arms4 red3 ok=True. C2 `--mutants`:
  total7 killed7 survived0 invalid0 null_detected1 (`c2-after.txt`); this proves only those sampled
  textual arms. C2BlindSpotR73's different adversarial battery accepts thirteen of sixteen cases,
  not a contradiction of the seven selected mutants: they measure different surfaces.
- Cheapest controls: `c1-control-legacy.txt`; `c2-control-frozen-tuple.txt` — old counter accepts
  fifth defective registry row, new audit prices its kind/owner and exits1.

## Census

Command at both ends:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before `corpus/evidence/round73/census-before.txt`: rc0, 25 W04 warnings. Registry row count240
at base, before S249 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`).
After expected row count241 after S249; actual end command/output is retained in
`corpus/evidence/round73/census-after.txt`, not inferred from row addition.

## Outside spot-check

Pending non-author closure. Dispatched wave seats are lane-authored evidence, never the outside
reviewer required by LEARNING.md. No SHONEN box is promoted to [x].

## Verdicts and next boundary

Both original claims not admitted; A1/A2 green runs are engineering repair evidence only.
No new capability or scientific novelty asserted. Coverage7 and calibration10 stay held.
Next freeze must evaluate projected registration before scoring, reject malformed registry rows,
and separate structural declarations from exact-command execution and semantic revision binding.
Source/entry truth must not be inferred from ast.parse or a green inventory token.

## Settled-wave integration and security repair

WAVE-DONE received from orchestrator: one v1 wave, sixteen settled outputs, no non-null result
notes (`w1-results.json` has seats16 and results length16). Role mix from spec: executor4,
reviewer3, critic2, scout2, scribe2, mutation-tester1, connector1, sentinel1. Attack share6/16;
one connector. L1 holds planner; RoundStateScoutR73 supplies its bounded data-walk.

- **M73-9 scope/data-loss defect, fixed outside the claim predicates.** CredentialSentinelR73
  proved both audit fixture modes delete caller-owned canaries because finally removed the entire
  supplied work directory. The repair allocates an owned tempfile child beneath existing --work
  and removes only that child. `cleanup-after.txt` replays both modes: rc0, caller canary survives
  and no child fixtures remain. Red-before is the sentinel's retained receipt, not an assertion.
  Registry write scope corrected; selected fixture semantics and original non-admission unchanged.
- Independent row draft/audit integrated, including r32 argparse exit2, actual r69 receipt-v2.txt,
  home locks/shared-loopback writes and selftest cleanup. The sources-adopt row no longer
  advertises unsupported --lane. Historical red entry verdicts are recorded, not “fixed” by
  lowering their bars. The obsolete five-cell tensor row is removed after its complete replacement.
- RegistryReviewerR73 confirms the original C1 contradiction and C2 denominator miss.
  Its other findings remain limitations: helper tests do not assert CLI finding ids;
  duplicate selftest arm is masked by another defect; no digest-pinned snapshot; token co-occurrence
  does not prove semantic erratum attribution; filesystem reads alone are not revision binding.
- Earlier claim prose “two instruments enter through plans” describes the pre-registration
  discovery only. After rows are added, legacy and full both advertise113 because SKILL.md itself
  advertises those entries. A1 is pad-able; no widening-contribution or exact112 landing claim is
  admitted. This supersedes A1's “unchanged target” explanation.
- Q13/Q14 qualifying source/number reread remains incomplete for the held candidates. A wave name
  alone neither grants nor forbids admission; EntryFalsifyR73 performed bounded spot-checks and
  explicitly did not do the complete reread. No new entry admitted.
- Self-evaluation: accuracy3 (original freezes invalid, now marked); completeness4 (all work and
  received falsifications retained, predicates miss); clarity4 (original/amended outcomes separate);
  actionability4 (counterexamples and cleanup repair run); conciseness3 (evidence large).
  Mean3.6, not a learning-trend score. Highest-impact improvement is Q54's projected-tree freeze.

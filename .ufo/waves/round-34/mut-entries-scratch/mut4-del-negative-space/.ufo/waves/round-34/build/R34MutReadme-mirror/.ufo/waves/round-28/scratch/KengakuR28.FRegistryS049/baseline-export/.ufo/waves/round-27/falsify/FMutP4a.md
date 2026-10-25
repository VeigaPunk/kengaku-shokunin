# FMutP4a — bounded P4a mutation probe
Axes: novelty→coverage/constructs (no score claim); calibration/detector sensitivity, full-token integrity, exact restoration.
Identity: KengakuR27.FMutP4a, not candidate writer KengakuR27; lane-dispatched advisory, not outside non-author closure.
Read the whole draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md`, proposed canonical `corpus/knowledge/extraction-policy-comparison.md`, and `plans/round-27-claims.md` including Amendment1. This is P4a evidence, not a Q1–Q15 entry-admission verdict.
Clone command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutP4a && git -C /tmp/kengaku-r27-FMutP4a switch -c r27-FMutP4a b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutP4a rev-parse HEAD` → exit0, observed HEAD exactly b5f62e5e637b34a1549e3475fc58b4227ed87e5a.

## Detector and retained evidence
Let S=/tmp/kengaku-r27-FMutP4a and C=$S/plans/state_check.py. All commands below ran with cwd=$S.
D(phase): `env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/kengaku-r27-FMutP4a python3 /tmp/kengaku-r27-FMutP4a/probe_p4a.py PHASE` (PHASE is the literal table row below).
D runs `/usr/bin/python3 C --root S --selftest`, then `/usr/bin/python3 C --root ROOT --json` on the clone and a b5719440e5eee46c1886fddbdf7bdc1624829454 export before/after/restoring the P4a recipe.
`env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FMutP4a/plans/fixtures/r27/p4_mutate.py --help` → exit0; no class CLI exists, so D reuses only its `export_base`, `load_recipes` P4a row, `apply_recipe`, `run_checker`, and `judge` APIs (plans/fixtures/r27/p4_mutate.py:80–155); no other class recipe runs.
The recipe is SCORECARD.md:790 `278 assertions`→`279 assertions` (plans/fixtures/r27/p4_mutants/P4a.json:2–8); all generated fixtures restore in finally. Detector commands are bounded at1200s; none timed out.
Raw stdout/stderr, exact argv/exits, JSON assertions and byte snapshots are retained in `$S/p4a-evidence/<phase>/`; each `record.json` records inventory, judgments, hashes and fixture restoration.
Every JSON run has9 P4a assertions and `P4.population.assertion-inventory=MATCH` (production inventory plans/state_check.py:3312–3325). No missing-id vacuity, setup exit2, or failing pristine baseline was used as a kill.

## Actual outputs / exits
All rows have327 assertions,3 offline-unverifiable; clone out_of_population=24, exported-base out_of_population=20. Counts below are clone match/mismatch/superseded. “fixture” is the exported source-token mutation under that checker.
| D phase | selftest exit | clone exit / P4a.scorecard.final.c2 | counts | fixture exit / new P4a MISMATCH | D exit |
|---|---:|---|---|---|---:|
| pristine | 0 | 0 / MATCH | 318/0/6 | 1 / final.c2 | 0 |
| source-token | 0 | 1 / MISMATCH | 317/1/6 | 1 / final.c2 | 1 |
| correction-full | 0 | 0 / SUPERSEDED | 317/0/7 | 1 / final.c2 | 0 |
| correction-partial | 0 | 1 / MISMATCH | 317/1/6 | 1 / final.c2 | 1 |
| correction-wrong | 0 | 1 / MISMATCH | 317/1/6 | 1 / final.c2 | 1 |
| source-restored | 0 | 0 / MATCH | 318/0/6 | 1 / final.c2 | 0 |
| comparison-removed | 0 | 0 / MATCH | 318/0/6 | 0 / none | 1 |
| comparison-restored | 0 | 0 / MATCH | 318/0/6 | 1 / final.c2 | 0 |

## M1 — asserted source token: KILLED by production comparison
Single clone edit SCORECARD.md:790:278→279. Expected: class-specific MISMATCH for final.c2, not merely a nonzero exit.
Actual D(source-token): JSON `P4a.scorecard.final.c2` MISMATCH, source_line789, claimed=[5,0,5,279,3] versus final receipt assertions278 (corpus/evidence/round26-calibration/state-check-final.txt:2); exit1. D(source-restored) returns MATCH/exit0.
Stock selftest stays0 because its P4a red fixture mutates claim.c1, not final.c2 (plans/state_check.py:3639–3648). The scoped production detector kills M1; selftest alone is not the measurement.

## P4a correction acceptance / refusal
With M1 still present, appended at SCORECARD.md:841: `- **R27-E901 (2026-10-21)** supersedes ` followed by code-span P4a.scorecard.final.c2, ` — now ` and these six ordered code spans:
`base_mismatch=5` `final_mismatch=0` `superseded=5` `assertions=278` `offline_unverifiable=3` `calibration_score=8`.
D(correction-full) → SUPERSEDED, correction_line841, exact derived/correction arrays equal, exit0. D(correction-partial), omitting calibration_score=8, → named MISMATCH/exit1. D(correction-wrong), restoring all six but assertions=279, → named MISMATCH/exit1. This exercises plans/state_check.py:2001–2012 on P4a, not only the built-in P4b correction case.
All correction lines were removed and the source restored before M2. No correction entered the live lane.

## M2 — remove production comparison: SURVIVED selftest; KILLED by scoped target harness
Single edit plans/state_check.py:2299: remove `c2_claim_values == c2_expected and `, leaving only `c2_score_value == c2_score_value_expected,`.
Expected: selftest or the P4a target harness rejects a checker that accepts the recipe's wrong assertion count.
Actual D(comparison-removed): stock `--selftest` exits0 and still prints `selftest ok P4a: mutation red (P4a.scorecard.claim.c1)` and `[selftest] ALL PASS`; clean-clone JSON remains byte-identical to pristine/exit0.
But the exported279-assertion fixture now exits0 with final.c2 MATCH while its JSON still shows claimed=[5,0,5,279,3] and receipt assertions278. Harness output is `HARNESS P4a red=False new=[] named=0`; D exits1 because the required new class-specific MISMATCH disappeared. Pristine/restored harness output is red=True, new=['P4a.scorecard.final.c2'], named=1; D exits0.
Coverage finding: green built-in selftest and green current-tree measurement do not protect this P4a final-C2 comparison. The separately run P4a fixture does detect its removal; this is not an existing pristine-data mismatch or a reason to change the frozen contract.

## Hashes / restoration
SHA256 clone SCORECARD: pristine/restored Hs=f015519478dce27960a2052f5ab71fa3d54769592e8a4831d4f177044e523936; M1=eb1413f867b6255ae86f37e2560101a76e62957e9b1aeaf2afcc1af4cd60ccf1; sequence Hs→M1→Hs.
Correction-control SCORECARD SHA256: full=e9ef308d6bdd6f3c16532c044108f67994635afb0b2879ff9c2b0bc081531a76; partial=cac2ab83e6a128c32a60122182000a2e42562655197e408ac4cda10fc168baa3; wrong=2fc1e4d7612e99f98cc4357927c8298524fefa0fabea667e3539f42a16bf8684; final restored Hs.
SHA256 checker: pristine/restored Hc=29c5d716a53e77bf4a82d2155775dda3e94385e058b4700af54cb3a23d031f32; M2=4256b49cd1d86585c52f0bd13434635cacf680e41ea34214472dc8a9ce024a1f; sequence Hc→M2→Hc.
Every exported fixture SCORECARD: before/restored=5030b75dcba57ca34eccb3120f439e9bccff2d0fd36eb1741f89f42eea67ee84; mutant=5ff220022c6e9f14d980b199341a82b91bc8d48cad41dbdf9dcb24d6a22ad8f2. All8 phases record exact=True and pristine/restored stdout/stderr equality=True.
Pristine/source-restored/comparison-restored clone JSON stdout SHA256=33fdfb2bcfda94dc9b6872a756281466174f3d09cc50f72cfa7a328304820d2d; M2's clean-clone stdout has that same hash.
Pristine/M2/restored selftest stdout SHA256=7fb4b3f930b229507cae7e449d6d3ffb72ecdab8a1e0057cc9743ec26e0a4973; selftest stderr empty. JSON source_line is789; private runner's display-only `:None` uses the wrong field name, while full retained JSON preserves source_line.
Live writes: only this report. No Git/jj/index mutations outside clone, no delegation/background jobs, no unrelated checks or runtime/model requests. Installs/updates: none.
VERDICT: P4a source-count mutant killed; complete true correction accepted and partial/false correction refused; comparison-removal mutant survives built-in selftest/current-tree replay but is killed by the scoped P4a target harness. Exact source, checker and generated-fixture bytes restored. Scoped evidence only; no admission judgment.

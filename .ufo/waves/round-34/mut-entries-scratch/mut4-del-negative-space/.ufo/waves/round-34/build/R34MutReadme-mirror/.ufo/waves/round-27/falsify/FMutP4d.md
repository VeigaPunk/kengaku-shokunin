# FMutP4d — frozen P4d mutation probe

- Identity: KengakuR27.FMutP4d, mutation-tester; not candidate writer KengakuR27. Advisory lane-dispatched evidence, not outside closure or a qualifying Q10 source/number reread.
- Axes: calibration (assertion sensitivity and full-token corrections); legacy novelty → canonical coverage/constructs is context only, with no score/admission judgment.
- Read the whole draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (including its full source line), pre-registration including Amendment 1, QUALITY Q1–Q15, and build ExecStateCheckV4/ExecP4RedFixtures/ExecP4Inventory. Proposed canonical entry: `corpus/knowledge/extraction-policy-comparison.md`; no canonical admission is asserted here.
- Isolation: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutP4d && git -C /tmp/kengaku-r27-FMutP4d switch -c r27-FMutP4d b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutP4d rev-parse HEAD` exited 0; observed HEAD `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.

## Detector and retained commands

- Below, R = `/tmp/kengaku-r27-FMutP4d`, E = R`/probe`; all execution/mutations were confined to this clone or its exports. All Python calls used `PYTHONDONTWRITEBYTECODE=1` and `-B`.
- S: `env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B /tmp/kengaku-r27-FMutP4d/plans/state_check.py --selftest`.
- J: `env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B /tmp/kengaku-r27-FMutP4d/plans/state_check.py --root /tmp/kengaku-r27-FMutP4d --json`.
- Recorder command: `env PYTHONDONTWRITEBYTECODE=1 python3 -B /tmp/kengaku-r27-FMutP4d/probe/p4d_probe.py --label LABEL FLAGS`; each invocation exited 0 as a recorder, not as a detector verdict. Exact child argv/cwd/exits are in E`/LABEL/record.json`; complete stdout/stderr and both byte snapshots are alongside it.
- T: recorder `--target` loads the real `plans/fixtures/r27/p4_mutate.py`, exports frozen P4 base `b5719440e5eee46c1886fddbdf7bdc1624829454`, selects only recipe P4d, uses its `apply_recipe` and `judge`, and captures checker `--root EXPORT --json` before/mutated/restored. `--help` was read first (exit 0); the five-class CLI was intentionally not run.
- T's existing source-token control is `corpus/knowledge/grader-perturbation-audit.md:34`, state count 1708→1709 (`plans/fixtures/r27/p4_mutants/P4d.json:4-7`). A red requires exit 1 and a new `P4d.` MISMATCH, not just nonzero or an inventory mismatch.

## Same-detector pristine / mutant / restored results

| LABEL | FLAGS | S exit/output | J exit; F1 verdict | T output |
|---|---|---|---|---|
| pristine | --selftest --json --target | 0; ALL PASS | 0; MATCH | control 0, mutant 1, restored 0; new=P4d.population.graders, red=true |
| source-mutant | --selftest --json | 1; pristine control did not MATCH (P4d.family.F1) | 1; MISMATCH | not run |
| source-restored | --selftest --json | 0; ALL PASS | 0; MATCH | not run |
| comparison-mutant | --selftest --json --target | 0; ALL PASS | 0; MATCH | control 0, mutant 1, restored 0; new=P4d.population.graders, red=true |
| comparison-impact | --json | not run | 0; MATCH despite source n=1820 | not run |
| restored | --selftest --json --target | 0; ALL PASS | 0; MATCH | control 0, mutant 1, restored 0; new=P4d.population.graders, red=true |

- Every J run emitted all **14 P4d ids** and `P4.population.assertion-inventory` MATCH; baseline and restored summary: assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3 out_of_population=24. These are not empty-inventory exits.
- Source mutant: only the F1 denominator at `corpus/knowledge/grader-perturbation-audit.md:64`, `1802/1819`→`1802/1820`. Expected J: exit 1 with `P4d.family.F1` MISMATCH. Actual: exactly that, claim n=1820 versus grader/oracle n=1819; summary mismatch=1. **KILLED**. Evidence E`/source-mutant/p4d-projection.json:160-186`, E`/source-mutant/selftest.stdout:12`; restored evidence E`/source-restored/p4d-projection.json:160-190`.

## Full-token correction acceptance is defective in the frozen checker

- With only the source mutant active, appended at audit line 130 (after frozen floor 128): `- **R27-E9001 (2026-10-21)** supersedes \`P4d.family.F1\` — now \`family=F1\` \`kind=MP\` \`k/n=1802/1819\`.` The full values equal the pristine checker's own derived tokens.
- Ran recorder labels `correction-full`, `correction-partial`, `correction-wrong`, `correction-r29`, each with `--json` (hence exact J above). Every child exited **1**, `P4d.family.F1` MISMATCH, `derived_tokens:null`, `correction_line:null`, and the inventory MATCH.
- Full expected: SUPERSEDED / exit 0; actual full remains MISMATCH / exit 1. Evidence E`/correction-full/grader-perturbation-audit.md.bytes:130`, E`/correction-full/p4d-projection.json:160-186`; pristine expected tokens E`/pristine/p4d-projection.json:180-189`.
- Refusal controls: partial omits `k/n`; wrong uses `k/n=1802/1820`; R29 uses all correct tokens but `R29-E9001`. Each remained MISMATCH as required; evidence respective E`/correction-{partial,wrong,r29}/p4d-projection.json:160-186` and byte snapshot line 130. Refusal does not establish selective acceptance: the correct full correction also fails.
- Cause: `plans/state_check.py:3245-3247` supplies derived family tokens only `if family_ok`; on a stale family claim it supplies None. `:2003-2006` only attempts correction when the failed assertion has non-None derived tokens. Thus this observed, independently rederived F1 discrepancy cannot close through its correct appended tokens (pre-registration `:122-124`). No production fix made.

## Removed production comparison survives the registered controls

- Mutant: delete only `plans/state_check.py:3237`, `and claim_values["n"] == command_values["n"] == oracle_values["n"]`; retain ids, kind/k comparisons, and all other code. Expected detector: S or existing target T should fail if they protect family denominators.
- Actual S: exit 0, `selftest ok P4d: mutation red (P4d.family.F1)` and ALL PASS (E`/comparison-mutant/selftest.stdout:12,17`). Existing T remains red on its unrelated graders count and its computed harness exit stays 0 (E`/comparison-mutant/record.json:50-58`). **SURVIVED S + existing P4d T**.
- Independent impact: reapply the exact already-killed denominator token with this one-line checker deletion. J now exits **0**, emits MATCH for `P4d.family.F1` although claim n=1820 and both recomputations n=1819, with all 14 ids retained (E`/comparison-impact/p4d-projection.json:160-190`). This is a sensitivity gap, not a contract change or evidence that the pristine comparator missed the token.
- Explanation: S's P4d fixture changes the F1 numerator 1802→1801 (`plans/state_check.py:3676-3677`), while T changes state-grader count (`P4d.json:4-7`); neither needs the removed denominator comparison.

## Hashes and exact restoration

| File/variant | SHA-256 |
|---|---|
| checker before = restored | 29c5d716a53e77bf4a82d2155775dda3e94385e058b4700af54cb3a23d031f32 |
| checker comparison mutant | 62e32affdb780fac5d98b923015081327d254c540d748721e35c4a72ae1a0916 |
| audit before = restored | 0ca1fdbce1544bf4ea4042d342ad30eb88e38398c45222190b78a327e7ea37ab |
| audit denominator mutant | fe0b8b3c893c0e0fbc7bf180ea2d05370327fa4a7fb9480a49e87ad5750ab5b7 |
| T's audit state-count mutant | 3b377988719cdb7e5e3c9df81d74d16fa07a49b47ad0c4cbc29149d7ee613b25 |

- Exact restoration command: `cmp -s /tmp/kengaku-r27-FMutP4d/probe/pristine/state_check.py.bytes /tmp/kengaku-r27-FMutP4d/plans/state_check.py && cmp -s /tmp/kengaku-r27-FMutP4d/probe/pristine/grader-perturbation-audit.md.bytes /tmp/kengaku-r27-FMutP4d/corpus/knowledge/grader-perturbation-audit.md` exited **0**; subsequent sha256sum printed the two original hashes above. Both mutations and every temporary correction were removed. Original/mutant/restored snapshots remain private under E; T also restores its exported mutants in finally and records before/restored identical hashes (`E/restored/record.json:33,101`).
- Restored S/J/T were rerun, not inferred: outputs are in the table and E`/restored/record.json`. No builds, lint, formatters, models/endpoints, services, live production edits, target Git/index writes, integration or admission were performed.
- Installs/updates: none.

VERDICT: Scoped P4d source mutant KILLED; production denominator-comparison mutant SURVIVED the frozen selftest and existing P4d target harness; full correct R27-E family correction was wrongly refused. Exact checker/audit bytes restored. These are calibration coverage/correction findings only, not a round or knowledge-admission verdict.

## Same-seat corrective probe — 2026-10-21

- At KengakuR27's followup request, imported only the corrected checker into the same private sandbox; observed/copy-pinned SHA-256 **5db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c**. The original frozen findings above remain historical; this addendum tests these new bytes, not an inferred commit.
- Reused exact S/J/T and the recorder command from lines 11–14. Labels/flags: `corrected-pristine`, `corrected-comparison-mutant`, `corrected-restored` each `--selftest --json --target`; `corrected-source-mutant` `--selftest --json`; `corrected-comparison-impact` and `corrected-correction-{full,partial,wrong,r29}` each `--json`. Every recorder exit was 0; child exits below are the detector results.
- Corrected pristine: S exit 0/ALL PASS; J exit 0, assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5 out_of_population=24. T control/mutant/restored exits 0/1/0 and new `P4d.population.graders` MISMATCH (harness exit 0). Evidence E`/corrected-pristine/record.json`, `selftest.stdout:18-26`.
- Repeated the prior denominator-deletion behavior at corrected `plans/state_check.py:3433`: the revised whole-dictionary equality was expanded to explicit non-null/kind/k comparisons, omitting only n; authority derivation remained untouched. Expected S: exit 1 naming the denominator fixture. Mutant checker SHA **f4bfa7caaf196f8bb17996e70d95b367961025abe7c242a95746b2f876e69a1d**.
- Actual corrected mutant: S **exit 1**, `selftest FAIL P4d denominator: red mutation survived (P4d.family.F1)` (E`/corrected-comparison-mutant/selftest.stdout:19`). The same detector was green before and after restoration; this is a **KILLED** production-comparison mutant, not a baseline failure. T still passes its state-count control and is not independently sensitive to family denominators.
- Confirmed the same production effect before restoring the comparator: exact prior source token `1802/1819`→`1802/1820` at audit `:64` gives J exit 0/F1 MATCH under the mutant (E`/corrected-comparison-impact/p4d-projection.json:181`). Restoring only the corrected comparator gives J **exit 1/F1 MISMATCH**, claim n=1820 versus both authorities n=1819 (E`/corrected-source-mutant/p4d-projection.json:181`).
- Retested the exact positive correction at audit `:130`: R27-E9001 with `family=F1`, `kind=MP`, `k/n=1802/1819`. Corrected J **exit 0/F1 SUPERSEDED**, correction_line=130, all derived/correction tokens equal; superseded=7/mismatch=0 (E`/corrected-correction-full/p4d-projection.json:181-215`). The prior acceptance defect is resolved on this case.
- Negative controls remained discriminating: partial omits k/n; wrong has `k/n=1802/1820`; R29 has correct tokens under R29-E9001. Corrected J **exit 1/F1 MISMATCH** for each (E`/corrected-correction-{partial,wrong,r29}/p4d-projection.json:181`). These are the original controls, not replacement easier inputs.
- All corrected J runs emitted **15 P4d ids** with the assertion inventory MATCH. `P4d.unmapped-numerics` is explicitly OFFLINE_UNVERIFIABLE/status UNVERIFIABLE, not a silent MATCH (E`/corrected-restored/p4d-projection.json:511`). No extra raw-count mutation or general inventory-completeness claim is made here.
- Corrected restored S **exit 0/ALL PASS**, including `selftest ok P4d denominator: mutation red (P4d.family.F1)` and full/partial/wrong/R29 controls (E`/corrected-restored/selftest.stdout:19-26`); restored J exit 0 with the pristine 329/318/0/6/5 summary above; restored T control/mutant/restored 0/1/0, new class-specific graders MISMATCH.
- Restoration command: `cmp -s /tmp/kengaku-r27-FMutP4d/probe/corrected-pristine/state_check.py.bytes /tmp/kengaku-r27-FMutP4d/plans/state_check.py && cmp -s /tmp/kengaku-r27-FMutP4d/probe/corrected-pristine/grader-perturbation-audit.md.bytes /tmp/kengaku-r27-FMutP4d/corpus/knowledge/grader-perturbation-audit.md` exited **0** after the restored detector run.
- Before/restored checker SHA is **5db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c**; before/restored audit SHA remains **0ca1fdbce1544bf4ea4042d342ad30eb88e38398c45222190b78a327e7ea37ab**; denominator source mutant remains **fe0b8b3c893c0e0fbc7bf180ea2d05370327fa4a7fb9480a49e87ad5750ab5b7**. New snapshots/outputs retained under E`/corrected-*`; original frozen snapshots preserved.
- Installs/updates: none. No lane source/Git/index edit or integration; only this append-only report changed outside the sandbox.

VERDICT: Original production-comparison mutant SURVIVED → corrected checker KILLED it via the targeted denominator selftest; exact full-token R27-E correction now SUPERSEDED, with original partial/wrong/R29 controls refused. Corrected pristine/restored checks green, class-specific MISMATCH demonstrated, and exact corrected bytes restored. Scoped corrective probe only; not admission or outside non-author closure.

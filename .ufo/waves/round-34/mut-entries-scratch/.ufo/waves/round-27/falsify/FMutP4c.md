# FMutP4c — bounded P4c mutation probe

Identity: **KengakuR27.FMutP4c**, not candidate writer KengakuR27. Advisory mutation evidence only; no admission/closure authority.
Axes: calibration (P4c detection and supersession); novelty unchanged/unscored by this probe.
Read `plans/round-27-claims.md` including Amendment 1 and the WHOLE 110-line draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` (including its untruncated source header). Proposed canonical path: `corpus/knowledge/extraction-policy-comparison.md`; this is not a qualifying whole-entry/source admission judgment.

## Isolation and detector

Created with `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutP4c && git -C /tmp/kengaku-r27-FMutP4c switch -c r27-FMutP4c b5f62e5e637b34a1549e3475fc58b4227ed87e5a` (exit 0).
`git -C /tmp/kengaku-r27-FMutP4c rev-parse HEAD` returned **b5f62e5e637b34a1549e3475fc58b4227ed87e5a** (exit 0).
Below, `R=/tmp/kengaku-r27-FMutP4c`, `E=/tmp/kengaku-r27-FMutP4c/probe-evidence`; all tests/mutations/exports stayed under R.
Exact child command S: `/usr/bin/python3 /tmp/kengaku-r27-FMutP4c/plans/state_check.py --selftest`.
Exact child command D: `/usr/bin/python3 /tmp/kengaku-r27-FMutP4c/plans/state_check.py --root /tmp/kengaku-r27-FMutP4c --json`.
Private recorder `R/p4c_probe.py` captures command, actual child exit, stdout/stderr and both file hashes; timeout 180s/child, `PYTHONDONTWRITEBYTECODE=1`, temporary files under `R/probe-temp`.
Recorder commands were `env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FMutP4c/p4c_probe.py LABEL --selftest`, LABEL = pristine, source-mutant, source-restored, comparison-mutant, comparison-restored. Recorder exits were 0; child exits below are not recorder exits.

## M1 — asserted source token: killed by production checker

At `corpus/lessons/round-26.md:87`, changed only `22 scout` → `23 scout` (spec remains scout=22).
Expected D: exit 1 with **P4c.build.role-mix MISMATCH**, not merely another class/inventory failure.

| Bytes | S exit | D exit | D output |
|---|---:|---:|---|
| pristine | 0 | 0 | assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3 |
| source-mutant | 0 | 1 | assertions=327 match=317 mismatch=1 superseded=6 offline_unverifiable=3; sole mismatch P4c.build.role-mix |
| source-restored | 0 | 0 | assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3 |

Evidence: `E/source-mutant-state.stdout:5135-5189` records lesson scout=23, expected/spec scout=22, class-specific MISMATCH. All 11 P4c IDs remain present. Verdict: **KILLED by D**, not inconclusive; pristine/restored controls pass. S alone does not validate this source token.

## M2 — one production comparison deletion survives selftest

At original `plans/state_check.py:2770-2771`, removed only `and build_claim_roles == expected_build_roles`, leaving the spec comparison and emitted assertion intact. Exact patch retained in `E/mutations.patch`.
Expected regression detector S: nonzero on losing the lesson-vs-expected build-role comparison. Actual pristine/mutated/restored S exits: **0 / 0 / 0**.
Mutant output remains `selftest ok P4c: mutation red (P4c.falsify.dead-seats)` and `[selftest] ALL PASS` (`E/comparison-mutant-selftest.stdout:11,17`). The P4c selftest mutates only dead seats (`plans/state_check.py:3663-3670`), not this build-role branch.
D on the unmodified lesson also stays exit 0. Its mutant run emits all **11 P4c IDs**, and `P4.population.assertion-inventory` is **MATCH**, expected=actual=48 P4 content IDs. This is a missing behavioral branch control, not a vacuous missing-inventory exit.
Used the existing P4c target harness after reading `p4_mutate.py --help` (exit 0): its `export_base`, `load_recipes`, `apply_recipe`, `run_checker`, `judge` functions, restricted to P4c, with original/restored bytes controls. No unrelated class mutants were run.
Exact wrapper: `env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/kengaku-r27-FMutP4c/probe-temp python3 /tmp/kengaku-r27-FMutP4c/p4c_probe.py LABEL --target-harness`, LABEL = pristine, comparison-mutant, comparison-restored (each wrapper exit 0).
Harness child command is `/usr/bin/python3 /tmp/kengaku-r27-FMutP4c/plans/state_check.py --root /tmp/kengaku-r27-FMutP4c/probe-evidence/LABEL-harness/target --json`, run before/after/restoring the recipe against exported base b5719440e5eee46c1886fddbdf7bdc1624829454.

| Checker bytes | Target pristine/mutated/restored child exits | P4c recipe attribution |
|---|---|---|
| pristine | 0 / 1 / 0 | named=1, new=[P4c.build.role-mix], red=true |
| comparison-mutant | 0 / 0 / 0 | named=0, new=[], red=false |
| comparison-restored | 0 / 1 / 0 | named=1, new=[P4c.build.role-mix], red=true |

`E/comparison-mutant-harness.json:16-66` retains the actual results and exact target-byte restoration. Thus the external targeted recipe exposes the regression, but **M2 SURVIVED S**. Finding: selftest coverage gap; current production comparison is present/correct, not a discovered current population mismatch. No contract change or production fix attempted.

## P4c full-token correction acceptance/refusal

With M1 active and pristine checker, appended at lesson line 199: `- **R27-E9001 (2026-10-21)** supersedes ` followed by backticked `P4c.build.role-mix`, ` — now ` and these ordered backticked tokens: `scout=22` `executor=14` `reviewer=12` `connector=6` `critic=6` `scribe=6` `revenger=4` `sentinel=1` `simplifier=1` plus final period.
Each row ran D through `env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FMutP4c/p4c_probe.py LABEL` (wrapper exit 0); exact commands, hashes and outputs retained in `E/LABEL-state.json` and `.stdout`.

| LABEL / correction | D exit | P4c.build.role-mix | Raw evidence |
|---|---:|---|---|
| correction-full / all nine correct tokens | 0 | SUPERSEDED; superseded=7, mismatch=0 | E/correction-full-state.stdout:5135-5199 |
| correction-partial / omit simplifier=1 | 1 | MISMATCH; superseded=6, mismatch=1 | E/correction-partial-state.stdout:5135-5198 |
| correction-wrong / full nine, scout=23 | 1 | MISMATCH; superseded=6, mismatch=1 | E/correction-wrong-state.stdout:5135-5199 |
| correction-r29 / correct nine, R29-E9001 | 1 | MISMATCH; superseded=6, mismatch=1 | E/correction-r29-state.stdout:5135-5189 |

Scoped **PASS** for these P4c supersession controls (`p4_record` exact list equality, `plans/state_check.py:1991-2012`). No claim about untested P4c branches or all correction syntax.

## Exact restoration and retained evidence

Lesson SHA-256 original → M1 → restored: `31c530da3a4d6adb5284dedfbbe11cf814eb5def730bd8deb5bbd211801081c8` → `7016b042a82e720003e83694f88a4b2432b50ac5f4bd0fbc6eee28f2506273f2` → original.
Checker SHA-256 original → M2 → restored: `29c5d716a53e77bf4a82d2155775dda3e94385e058b4700af54cb3a23d031f32` → `ea47500dccc24ebf9554449f74733e0e7a1ee57c954241f0a7c5dd76f760aeb1` → original.
`sha256sum` after restoration returned both original hashes and unchanged harness hash `627d592b6bd6bacc83a614e7593325632cb5c5c36d8db105acbf2316e224d0ba` (exit 0). All correction rows removed; restored S/D and target-harness results are above.
Retained exact checker-mutant/restored bytes in `E/comparison-mutant.tar` / `E/restored.tar`; SHA-256 respectively `5cc2b4420c3b5275500844d12f0dbfcfde06333b55d01835ac7c16434a37bd4f` / `80cf5f2f8403e7782a04b3bd0d5e4bd335b5c115fd4840d5978889e7f66fe46f`. M1 patch, all phase hashes, full stdout/stderr and harness JSON remain private under E.
Installs/updates: **none**. Existing Python 3.14.8; no build/lint/formatter, endpoint/model, service, integration, or admission commands run. Lane writes: this report only.

VERDICT: M1 KILLED by class-specific production MISMATCH; M2 SURVIVED state_check --selftest and is exposed by the targeted P4c harness; full-token correction controls PASS within scope; exact original bytes restored. Calibration selftest coverage finding, not an admission verdict.

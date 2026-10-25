# FMutP4b — frozen P4b mutation probe
Identity: KengakuR27.FMutP4b; not candidate writer KengakuR27. Advisory lane-dispatched evidence, not outside admission or Q15 closure.
Read the entire 110-line draft, including its full source header, for proposed canonical `corpus/knowledge/extraction-policy-comparison.md`; read `plans/round-27-claims.md` including Amendment 1.
Axes: calibration/detector sensitivity, full-token correction integrity, assertion-population visibility, exact-byte isolation. No C1 parser/novelty score or global admission verdict is tested here.

## Isolation and detector
Clone command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-FMutP4b && git -C /tmp/kengaku-r27-FMutP4b switch -c r27-FMutP4b b5f62e5e637b34a1549e3475fc58b4227ed87e5a && git -C /tmp/kengaku-r27-FMutP4b rev-parse HEAD` → exit 0; observed HEAD `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
Notation: C=`/tmp/kengaku-r27-FMutP4b`, E=`/tmp/kengaku-r27-FMutP4b/p4b-evidence`, T=`P4b.readme.covers.round26-sources`.
D(flag): `env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/kengaku-r27-FMutP4b/p4b-evidence /usr/bin/python3 /tmp/kengaku-r27-FMutP4b/plans/state_check.py --root /tmp/kengaku-r27-FMutP4b <flag>`.
Recorded driver command: `env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-FMutP4b/p4b_probe.py <stage> [--json-only]`; each invocation exited 0 (collector success, not checker verdict).
The driver runs D(--json) and D(--selftest) concurrently, each bounded to 180 seconds; correction variants run only D(--json). No background job, delegation, build/lint/formatter, endpoint request, or other runtime.
Read `p4_mutate.py --help` → exit 0. Its CLI runs all five classes and has no class selector; used its actual `judge('P4b', control, trial)` function with the same normalized (id, observed) mismatch pairs instead. This is a P4b-only target-oracle invocation, not a claimed full five-class harness run (`plans/fixtures/r27/p4_mutate.py:145-155`).
A class kill requires checker exit 1 plus a NEW `P4b.*` MISMATCH, not an unrelated nonzero exit. Initial control must pass; an existing SUPERSEDED result is not a mismatch.

## Pristine and restored controls
Stages `pristine`, `source-token-restored`, `production-call-restored`: D(--json) exit 0, `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3 out_of_population=24`.
Each has exactly eight P4b IDs, T=SUPERSEDED, and `P4.population.assertion-inventory`=MATCH. Frozen external ID list: `plans/fixtures/r27/p4_assertion_ids.txt:10-17`.
Each D(--selftest) exits 0, ends `[selftest] ALL PASS (...)`, stderr empty; stdout SHA256 `7fb4b3f930b229507cae7e449d6d3ffb72ecdab8a1e0057cc9743ec26e0a4973`.
Full commands, exits, stdout/stderr and snapshots: E/<stage>/manifest.json, json.stdout, json.stderr, selftest.stdout, selftest.stderr, checker.snapshot, readme.snapshot.

## M1 — asserted source-range token: KILLED
Only edit: `corpus/README.md:269`, the round-26 Covers cell, `S043–S047` → `S043–S046`; leave its existing S043–S048 erratum and registry untouched.
Expected detector: production T must MISMATCH because the shortened source range no longer qualifies for the exact historical erratum exception (`plans/state_check.py:2557-2606`).
Command: driver `source-token-mutant` (both D flags).
Actual D(--json): exit 1; `327/318/1/5/3` assertions/match/mismatch/superseded/offline, out_of_population=24; exactly eight P4b IDs; ONLY mismatch T, source_line=269.
Observed claim `[043,046]`; registry `[43,44,45,46,47,48]`; derived range S043–S048; `base_erratum_exact=false` despite retained erratum at line 284.
Actual target harness: `{"named":1,"new":["P4b.readme.covers.round26-sources"],"red":true}`.
Actual D(--selftest): exit 1, stdout contains `selftest FAIL P4 supersession: exact base anchor was not superseded`; stderr empty. Its fixtures are copied from the checker tree, so this is a mutated-fixture-control failure; the production class-specific MISMATCH is the substantive kill.
Evidence: E/source-token-mutant/manifest.json and both stdout files. Restore stage returns both detectors to the pristine outputs; no baseline failure was counted as a kill.

## P4b correction acceptance/refusal controls
Keep M1 in place; append at `corpus/README.md:301` one unique correction with prefix `- **R27-E900 (2026-10-21)** supersedes ` followed by backticked T, ` — now `, and backticked tokens below. No original assertion is rewritten by the correction.
Full required tokens, in order: `sources=S043–S048`, `source_count=6`, `source_ids=S043,S044,S045,S046,S047,S048` (`plans/state_check.py:1991-2012,2569-2572`).
Driver `correction-partial --json-only`: omit source_ids; exit 1, T=MISMATCH; correction_line=301 and exactly the two supplied tokens are observed; class oracle red=true.
Driver `correction-full --json-only`: supply all three; exit 0, T=SUPERSEDED, mismatch=0; observed correction tokens exactly equal derived tokens. Oracle red=false is expected acceptance, not a surviving defect.
Driver `correction-wrong-count --json-only`: supply all three but source_count=5; exit 1, T=MISMATCH; class oracle red=true.
All three retain eight P4b IDs and inventory MATCH; manifests, actual output and source snapshots are retained in E/<stage>/. All correction bytes were then removed and README restored before M2.
Scoped result: complete correct R27-E tokens accepted; incomplete and incorrect complete tokens refused for this class. Existing erratum recognition is not a new discovery or repair.

## M2 — remove production comparison dispatch: selftest SURVIVED; inventory KILLED
Only edit: delete `check_p4b(root, out)` at frozen `plans/state_check.py:3315`, leaving its implementation, expected ID registry, and direct selftest calls intact.
Expected detector: end-to-end selftest should notice missing production P4b comparisons; production inventory should refuse a shrunken population (`plans/state_check.py:3312-3325`).
Command: driver `production-call-mutant` (both D flags).
Actual D(--selftest): exit 0, byte-identical to pristine, still says `selftest ok P4b: mutation red (P4b.readme.artifact-row.evidence/round26-calibration/)` and `[selftest] ALL PASS (...)`.
Actual D(--json): exit 1; `assertions=319 match=310 mismatch=1 superseded=5 offline_unverifiable=3 out_of_population=24`; P4b IDs=0; T absent; ONLY mismatch `P4.population.assertion-inventory` (expected 48 grouped IDs, actual 40).
Actual class-specific harness: `{"named":0,"new":[],"red":false}`. The inventory exit is NOT evidence of a P4b-specific mismatch.
Finding: the helper-level P4 selftest does not cover its production dispatch (`plans/state_check.py:3657-3660,3707-3754` call check_p4b directly). This is a surviving selftest coverage defect, NOT an end-to-end CLI escape: the separate inventory correctly kills the omission.
Evidence: E/production-call-mutant/manifest.json, json.stdout and selftest.stdout. Restoring the dispatch returns all eight P4b IDs and both pristine detector outputs.

## Hashes and exact restoration
README original/final SHA256 R=`6f65de1bdd231edc989df36aabd5db256dbb1d46a14ea29a9afe1a83643bed80`.
M1 README before R; mutant `f9c79b829793e4d9096e30426fae44b06083365fdfcb5d4cdf17bdd3edf542a4`; restored R.
Correction README snapshots: partial `943c6e0b4e50fbc93185b9162b13bd48d535f85aebe693d2bde5688732144405`; full `481340e4ac14dcce6ddb4a8147677b792feac4a27a42fef3097cdf5496c01270`; wrong-count `f5bc22a907b33dc64805ad617929727851cc9b1c6eba76937d0d440a7ddcaa9e`; restored R.
Checker original/final SHA256 H=`29c5d716a53e77bf4a82d2155775dda3e94385e058b4700af54cb3a23d031f32`.
M2 checker before H; mutant `58000d4f4cf5f973464c5cd35cd5bb2f92a4ad913a21ac828c0784ec5696d36a`; restored H. README remains R throughout M2; checker remains H throughout M1/corrections.
Restoration command: seven chained `cmp` calls compare pristine to restored README/checker snapshots and each restored json.stdout/selftest.stdout; exit 0, output `RESTORATION: seven exact byte comparisons PASS`. Exact file pairs are pristine/readme vs source-token-restored/readme; pristine/checker vs production-call-restored/checker; pristine/readme vs production-call-restored/readme; pristine/json.stdout vs each restored/json.stdout; pristine/selftest.stdout vs each restored/selftest.stdout (all under E; snapshot suffixes as listed above).
Only live-lane write is this report. Private driver, actual outputs, mutant snapshots and restored snapshots remain under C; no integration or candidate edits performed.
Installs/updates: none. Existing Python observed: 3.14.8, GCC 16.2.1 build; no package transaction.
VERDICT: M1 KILLED by a new P4b-specific MISMATCH; correct full-token correction accepted and partial/wrong tokens refused. M2 SURVIVED --selftest but was KILLED by the production assertion inventory, without a P4b-specific mismatch. Both mutated source files and pristine detector outputs were restored byte-for-byte; this scoped result is not admission authority.

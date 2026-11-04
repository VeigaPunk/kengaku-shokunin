# C1RowAuditR73 independent row audit

Axes: coverage and calibration. Independent derivation below was persisted before opening any c1-rows-draft.md. This is a moving-worktree measurement, not a landing-tip certification. LSP unavailable: `read xd://lsp` returned “No such tool”; source inspection is a literal fallback, not semantic reference proof. No tools installed.

## Independently derived eight fields

Commands below are lane-relative; execution used absolute script/input paths and scratch cwd. `DIR` is an existing seat-owned scratch directory. All seven scripts implement a failure verdict, so `gate` is the honest kind despite filenames containing probe.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| round32-c1 | gate | `python3 plans/round32_c1_verify.py --lane .` | 0 clean (`checks=6 defects=0`); 1 failed (V0 absent expect or V1–V6 defect, including raising checks); 2 could-not-evaluate (argparse usage); uncaught malformed expect JSON also exits 1 with traceback | `python3 plans/round32_c1_verify.py --selftest`; seven named CASE lines, summary checks=6 failed=0 | script ENTRY/EXPECT/CONTROL/PINS constants; `.ufo/waves/round-32/claims/adoption-expect.json`, control-nothing.txt; revisions 66f92766, 9be8d8fe and literal 2412.05579; 40 lines/3000 bytes/20-character title | entry read-only; selftest TemporaryDirectory under TMPDIR, removed | kengaku |
| round32-defects | gate | `python3 plans/round32_defects.py --lane .` | 0 clean checks=7 defects=0; 1 failed R1–R7 or frozen-list defect; 2 could-not-evaluate argparse usage | `python3 plans/round32_defects.py --selftest`; isolated synthetic reports plus empty-tree checks, checks=7 failed=0 | script CHECKS/FROZEN and constants, fleet `.ufo/reports/round-31/kengaku.md` and round-32/kengaku.md, a44b5a8/ae95fe0, lesson/receipt anchors | entry reads lane plus absolute fleet reports and git master; selftest TMPDIR temporary report fixtures, removed; no report edits | kengaku |
| round66-c1-tensor-probe | gate | `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt` | 0 clean R66-C1 pass; 1 failed receipt mismatch (unhandled I/O can also exit 1); 2 could-not-evaluate usage/setup; bare CLI requires a mode | `python3 plans/round66_c1_tensor_probe.py --selftest --work DIR`; good acceptance and vector/no-CASE/malformed refusals | script GRADER_SHA256/FROZEN_TABLE; corpus/evidence/round66/tensor/cases, receipt.txt and receipt.junit/*.xml; grader capture under round52 | check read-only; selftest writes/removes child of --work; --run writes --work, --receipt (default committed receipt) and sibling receipt-stem.junit; also ~/.local/share/kengaku-r66/port-12355.lock; sandbox private /tmp | kengaku |
| round69-c1-nginx-probe | gate | `python3 plans/round69_c1_nginx_probe.py --check-receipt corpus/evidence/round69/nginx/receipt-v2.txt` | 0 clean matching full-coverage predicate; 1 failed including honest R69 frozen-table seen_f=6/8; 2 could-not-evaluate usage/setup/missing receipt | `python3 plans/round69_c1_nginx_probe.py --selftest --work DIR`; five refused receipts and synthetic acceptance; optional --green-receipt | script GRADER_SHA256/TB2_PIN/CASES/LEGS; plans/round-69-claims.md; corpus/evidence/round69/nginx/receipt-v2.txt | check read-only; selftest leaves fixtures under --work; battery replaces case directories under --work, writes optional --receipt/--evidence-dir, host ~/.local/share/kengaku-r69/port-8080.lock and shared-loopback HTTP service on 8080; private sandbox /tmp | kengaku |
| round69-c2-routed-defects | gate | `python3 plans/round69_c2_routed_defects.py --root .` | 0 clean DEFECTS n=0; 1 failed E1–E7 (or uncaught input exception); 2 could-not-evaluate argparse or missing work directory | `python3 plans/round69_c2_routed_defects.py --selftest --work DIR`; fake-lane all-seven red plus stale E7 receipt refusal; not run here because it internally git-adds/commits | script TREE=27f649f8/LANDING=1ec2e60a, four ROUND68_INSTRUMENTS, STRICT_ROLES; corpus/evidence/round69/c2-receipts/provenance-erratum.txt and gates/{depth-gate,trio}.txt | entry read-only including git show and subprocess checks; selftest deletes/recreates --work/fake-lane, creates/configures/commits git repo there and rewrites synthetic files; fixtures remain for caller cleanup | kengaku |
| round70-c1-nginx-probe | gate | `python3 plans/round70_c1_nginx_probe.py --check-receipt corpus/evidence/round70/nginx/receipt.txt` | 0 clean full seven-case/eight-leg predicate; 1 failed mismatch, coverage or digest finding; 2 could-not-evaluate usage/setup/missing receipt | `python3 plans/round70_c1_nginx_probe.py --selftest --work DIR`; seven refusals, synthetic acceptance, path-independent and staged-state arms | script GRADER_SHA256/TB2_PIN/CASES/CASE_SHA; committed probe git blob; plans/round-70-claims.md and corpus/evidence/round70/nginx/receipt.txt | check read-only git/grader reads; selftest/stage-sha write case trees under explicit work; battery writes optional receipt/evidence, host ~/.local/share/kengaku-r70/port-8080.lock and shared-loopback HTTP 8080; private sandbox /tmp | kengaku |
| round70-c2-routed-defects | gate | `python3 plans/round70_c2_routed_defects.py --root .` | 0 clean DEFECTS n=0; 1 failed E1–E8 including caught exceptions; 2 could-not-evaluate argparse or missing work | `python3 plans/round70_c2_routed_defects.py --selftest --work DIR`; eight red fake checks plus E2 byte flip; --mutants also exists | script CHECKS, R69_LANDING_REV=4038bb11, INSTRUCTION_SHA/ANCHOR; corpus/evidence/round70/c2/depth-gate-provenance.txt; gates/trio-nginx.txt and r69-c2-landing.txt; .ufo/waves/round-70/w1-validate.* | entry read-only subprocess trio; selftest/mutants remove/recreate --work/fake-lane and write fixtures/generated mutants under --work, left for caller cleanup | kengaku |

## Gate standard findings

1. **Medium — selftest conformance is narrower than a real spelling.** PROTOCOL.md:385–389 requires isolated self-invocation asserting exit code and stable finding-id. round32_c1_verify.py:149–164 calls check functions directly and accepts any exception as a successful red; round32_defects.py:207–240 similarly uses helper return truthiness. They are real --selftest spellings and isolated, but do not satisfy the strict CLI/finding-id requirement. round66_c1_tensor_probe.py:334–369 checks booleans rather than asserting the named finding per mutation. The nginx selftests assert checker rc but accept any refusal reason (r69:629–638; r70:776–786). Do not describe these as full PROTOCOL conformance merely because a flag exists.
2. **Medium — preserve host-write disclosure.** round66_c1_tensor_probe.py:222–225 writes a home-directory lock; nginx r69:267–270 and r70:352–355 also create host lock files. Any row claiming all modes write only --work/receipt is false. Battery shared-loopback services are an additional externally observable effect. My check-receipt entry choices avoid those writes; full replay was not executed.
3. **Low — current red instruments must remain red, not be called landing passes.** The measured entry results below expose real historical predicates/inputs rather than invalid argv.
4. **Low — frozen pins are legacy/non-digest baselines in several rows.** r32 expect/control and r69/r70 C2 mutable fleet/lane surfaces are named inputs, not comprehensive digest-pinned snapshots. PROTOCOL.md:390–397 is not established by registry inventory checks. r32 defects FROZEN is computed directly from CHECKS (:204), so that equality is not an independent frozen-list oracle.

All declared 0/1/2 codes are explicitly classified in my rows. No installed tool or alternate runtime used; no admission recommendation follows from a tally.

## Independent sweep (first sample)

SWEEP command_forms=596 distinct_script_spellings=128 existing_lane_scripts=117 gate_ADVERTISED=113 existing_not_advertised=4.

Scope: all plans/*.md plus SCORECARD.md, SKILL.md, LOG.md, corpus/README.md. Broad extraction `\bpython3\s+([^\s`<>|;()]+\.py)\b`; compared existing lane-relative paths with gate.collect(lane)'s actual advertised keys. Gate additionally scans corpus/knowledge/*.md; thus totals are not identical universes of text. Literal command occurrences include repeated forms, not 596 independent instruments. The gate sample reported MISSING [] and REGISTERED 113; this is already different from frozen target 112, and is not certified as a landing measurement.

Existing paths omitted by CMD (round52_c2_registry.py:36):
- SCORECARD.md:74 — corpus/evidence/round9-fleet/test_harness.py. Hyphen in directory excluded by `[A-Za-z0-9_]+`.
- SKILL.md:592 — corpus/evidence/round13-coverage/coverage_census.py. Same hyphen gap. corpus/README.md:18 also names it as evidence/round13-coverage/coverage_census.py (document-relative spelling).
- SKILL.md:599 — plans/fixtures/r29/mutation_witness.py. Additional depth excluded by plans' single-component regex. Gate docstring deliberately excludes fixture helpers, so report as a bounded-universe exclusion, not automatically a missing independent instrument.
- LOG.md:521 — plans/fixtures/r28/acceptance.py. Same deliberate fixture-depth exclusion.

`uv run ... python3 plans/tb2_grader_probe.py` is present and the embedded python3 command is recognized; uv wrapper is NOT an observed blind spot. Searches for python -m and dotted path forms will be enumerated with the execution evidence below; no invented example is counted.

## Draft comparison

Read `corpus/evidence/round73/w1/c1-rows-draft.md` only after persisting my independent rows above. Seven-row comparison: entry argv, gate kind, self-test spelling, owner, pin sources and write boundaries substantively agree. Differences:
- My first name `round32-c1` versus draft `round32-c1-verify`: naming preference only; use the draft's script-identifying name.
- Draft r32-C1, r66-C1 and r69-C2 verdict cells assign exit 1 both “failed” and “could-not-evaluate” for uncaught exceptions. This conflicts with PROTOCOL's fleet-wide 1=failed outer mapping. Preserve the exception caveat but give a single outer class; fixing scripts is outside this seat's scope.
- My rows explicitly disclose shared-loopback HTTP service/port effects, private sandbox /tmp and caller cleanup of retained work trees. Draft captures host lock and output writes correctly but omits the shared-loopback effects.
- Draft includes an eighth r73 audit row; outside the seven-script derivation requested here, so not independently certified.
- No other substantive seven-row disagreement. Draft does NOT inherit the erroneous live r69 entry path.

## Actual diff findings, severity ordered

**High: live appended r69 row has a dead entry.** `SKILL.md:702` names `corpus/evidence/round69/nginx/receipt.txt`, which is absent. Executing that exact check-receipt entry returned 2, `SETUP receipt-missing .../receipt.txt`, stderr empty. Existing receipt-v2.txt returned 1 for the legitimate historical coverage miss, not setup. The draft correctly names v2; the live row does not. Gate structural success cannot establish entry executability.

**Medium: live write scopes underdeclare effects.** `SKILL.md:701,702,704` state scratch-under-work while their explicitly advertised battery modes also write optional receipt/evidence paths and home-directory locks (source anchors above). `SKILL.md:699–700` describe read-only but omit temporary selftest writes; r32-defects also reads absolute fleet reports rather than just repo bytes. r69-C2 and r70-C2 correctly bound fixture writes, though r69's fixture internally commits.

**Medium: live r32 verdict maps omit argparse exit 2.** `SKILL.md:699–700` list only 0 and 1; both CLIs use argparse (source r32 verifier:168–171; defects:244–247). Declare usage as could-not-evaluate. Their isolated helper tests still do not establish strict PROTOCOL self-invocation/finding-id conformance.

**Low: live r32-defects pins description is factually overbroad.** `SKILL.md:700` says the CLI receipt is what “every R check re-reads”; only R3 reads it (round32_defects.py:101–113), while other checks read reports/lessons/SKILL. Draft corrects this with explicit literals and input identities.

**Coverage residual: two real hyphenated evidence instruments are outside CMD.** The four exclusions in SWEEP include two deliberately excluded fixture helpers, but `coverage_census.py` documents a real read-only census at :1–19 and `test_harness.py` documents an offline adversarial battery at :1–19. Therefore saturation must be qualified to the regex-defined universe, not every existing advertised Python instrument.

**Frozen-contract drift, not resolved by this seat:** actual gate execution printed `ADVERTISED total=113`, `REGISTERED total=113 rows=115`, `MISSING 0`, all other inventory legs 0, `PREDICATE R73-C1 pass`, rc 0. This is not the assignment's exact target 112. During review the predicate changed from the initially read `len(plans_only)>=1` to `len(plans_seen)>=1`; reread source `round52_c2_registry.py:133–161` explicitly labels Amendment A1. Initial in-memory gate collection and later subprocess therefore differ in predicate bytes. Do not treat this as an unchanged frozen-rule success or certify a landing tip. Whether any amendment is admissible is for the canonical assignment owner; I edited no rule.

## Verification boundaries

Seven --help invocations returned 0, stderr empty. Entry/check results in script order: r32-C1=1 (`S094 registry row cites no URL`); r32-defects=1 (historical round32 report does not cite current master); r66-C1=0; r69-C1 v2=1 (seen_f=6/8); r69-C2=1 (E7 depth receipt differs); r70-C1=0; r70-C2=0. All stderr empty. Six authorized selftests returned 0; r69-C2 selftest was deliberately not executed because it internally git-adds/commits, prohibited by this seat's assignment. None of these observations changes a predicate, target or historical claim.

Sweep supplement: three uv-wrapped python3 occurrences (SCORECARD.md:564, SKILL.md:665, LOG.md:1000) are recognized by the embedded python3 regex. Two python -m occurrences (plans/round-63-claims.md:34; round-68-claims.md:64) are `pip install`, not lane-owned scripts, so not counted as missing instruments. No existing lane script with an extra-dot filename was found among the broad python3 forms; this is not proof that such forms could never be missed. A document-relative evidence spelling at corpus/README.md:18 resolves to the already-counted coverage census, not a fifth unique omission.

## Exact commands and captured outputs

Environment: cwd=/fast/scratch/hyaku/kengaku-r73/C1RowAuditR73; PYTHONDONTWRITEBYTECODE=1; TMPDIR=/fast/scratch/hyaku/kengaku-r73/C1RowAuditR73. Runtime python3 only.

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round32_c1_verify.py --help

rc=0

```text
usage: round32_c1_verify.py [-h] [--lane LANE] [--selftest]

Second receipt for round 32's C1: the literals `adoption_check.py` does not
read.

options:
  -h, --help   show this help message and exit
  --lane LANE
  --selftest
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round32_defects.py --help

rc=0

```text
usage: round32_defects.py [-h] [--lane LANE] [--selftest]

Re-derive the seven defect items round 31's non-author closure routed to this
lane.

options:
  -h, --help   show this help message and exit
  --lane LANE
  --selftest
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round66_c1_tensor_probe.py --help

rc=0

```text
usage: round66_c1_tensor_probe.py [-h] (--run |
                                  --check-receipt CHECK_RECEIPT | --selftest)
                                  [--receipt RECEIPT] [--work WORK]

options:
  -h, --help            show this help message and exit
  --run
  --check-receipt CHECK_RECEIPT
  --selftest
  --receipt RECEIPT
  --work WORK
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c1_nginx_probe.py --help

rc=0

```text
usage: round69_c1_nginx_probe.py [-h] [--lane LANE] [--work WORK]
                                 [--receipt RECEIPT]
                                 [--evidence-dir EVIDENCE_DIR]
                                 [--check-receipt CHECK_RECEIPT] [--selftest]
                                 [--green-receipt GREEN_RECEIPT]
                                 [--render-table]

Round 69, C1: the `nginx-request-logging` Terminal-Bench 2.0 grader replayed
offline.

options:
  -h, --help            show this help message and exit
  --lane LANE
  --work WORK
  --receipt RECEIPT
  --evidence-dir EVIDENCE_DIR
  --check-receipt CHECK_RECEIPT
  --selftest
  --green-receipt GREEN_RECEIPT
  --render-table
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c2_routed_defects.py --help

rc=0

```text
usage: round69_c2_routed_defects.py [-h] [--root ROOT] [--selftest]
                                    [--work WORK]

Round 69, C2: the routed-defect gate for the round-68 non-author closure's
seven items.

options:
  -h, --help   show this help message and exit
  --root ROOT
  --selftest
  --work WORK
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round70_c1_nginx_probe.py --help

rc=0

```text
usage: round70_c1_nginx_probe.py [-h] [--lane LANE] [--work WORK]
                                 [--receipt RECEIPT]
                                 [--evidence-dir EVIDENCE_DIR]
                                 [--check-receipt CHECK_RECEIPT] [--selftest]
                                 [--green-receipt GREEN_RECEIPT]
                                 [--render-table] [--stage-sha STAGE_SHA]

Round 70, C1: the `nginx-request-logging` Terminal-Bench 2.0 grader replayed
offline,

options:
  -h, --help            show this help message and exit
  --lane LANE
  --work WORK
  --receipt RECEIPT
  --evidence-dir EVIDENCE_DIR
  --check-receipt CHECK_RECEIPT
  --selftest
  --green-receipt GREEN_RECEIPT
  --render-table
  --stage-sha STAGE_SHA
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round70_c2_routed_defects.py --help

rc=0

```text
usage: round70_c2_routed_defects.py [-h] [--root ROOT] [--selftest]
                                    [--mutants] [--work WORK]

Round 70, C2: the routed-defect gate for the round-69 non-author closure's
eight items.

options:
  -h, --help   show this help message and exit
  --root ROOT
  --selftest
  --mutants
  --work WORK
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round32_c1_verify.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin

rc=1

```text
DEFECT V2 cited-row-identity: the S094 registry row cites no URL
checks=6 defects=1
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round32_defects.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin

rc=1

```text
DEFECT R2 round32-report-order-tip: the round-32 report does not cite the final lane tip ea41880fa7
checks=7 defects=1
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round66_c1_tensor_probe.py --check-receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round66/tensor/receipt.txt

rc=0

```text
CHECK ok cases=5
PREDICATE R66-C1 pass
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c1_nginx_probe.py --check-receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round69/nginx/receipt-v2.txt

rc=1

```text
CHECK ok cases=5 legs=8 seen_p=8 seen_f=6
DEFECT leg-coverage test_nginx_running p=5 f=0
DEFECT leg-coverage test_custom_404_page p=5 f=0
DEFECT stored-predicate PREDICATE R69-C1 fail
CHECK stored-predicate=fail derived=fail
PREDICATE R69-C1 fail
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c2_routed_defects.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin

rc=1

```text
E1 ok rows=4/4 missing=[] thin=[]
E2 ok headings=1 q50=True round68-lesson=True spotcheck=True
E3 ok inputs=6 differs=['SKILL.md'] problems=[]
E4 ok verified-at-lines=2 last-names-landing=True
E5 ok strict-lines=1
E6 ok rerecord-lines=1
E7 defect problems=['corpus/evidence/round69/gates/depth-gate.txt:differ']
DEFECTS n=1
PREDICATE R69-C2 fail
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round70_c1_nginx_probe.py --check-receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round70/nginx/receipt.txt

rc=0

```text
CHECK ok cases=7 legs=8 seen_p=8 seen_f=8
CHECK stored-predicate=pass derived=pass
PREDICATE R70-C1 pass
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round70_c2_routed_defects.py --root /home/vgpnk/Projects/shokunin/kengaku-shokunin

rc=0

```text
E1 ok depth-gate-identity line-changes=1 problems=[]
E2 ok trio-receipt trio bytes=64
E3 ok instruction-row problems=[]
E4 ok s241-correction problems=[]
E5 ok corpus-index problems=[]
E6 ok r69-landing-receipt problems=[]
E7 ok gate-reject problems=[]
E8 ok wave-validation problems=[]
DEFECTS n=0
PREDICATE R70-C2 pass
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round32_c1_verify.py --selftest

rc=0

```text
CASE registry-complete PASS
CASE V1-red-on-empty PASS
CASE V2-red-on-empty PASS
CASE V3-red-on-empty PASS
CASE V4-red-on-empty PASS
CASE V5-red-on-empty PASS
CASE V6-red-on-empty PASS
SELFTEST checks=6 failed=0
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round32_defects.py --selftest

rc=0

```text
CASE registry-complete PASS
CASE R1-red-without-erratum PASS
CASE R1-green-with-erratum PASS
CASE R2-red-missing-report PASS
CASE R3-red-on-empty PASS
CASE R4-red-on-empty PASS
CASE R5-red-on-empty PASS
CASE R6-red-on-empty PASS
CASE R7-red-on-empty PASS
SELFTEST checks=7 failed=0
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round66_c1_tensor_probe.py --selftest --work /fast/scratch/hyaku/kengaku-r73/C1RowAuditR73/round66_c1_tensor_probe

rc=0

```text
SELFTEST {'good_accepted': True, 'mutated_refused': True, 'nocase_refused': True, 'malformed_refused': True}
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c1_nginx_probe.py --selftest --work /fast/scratch/hyaku/kengaku-r73/C1RowAuditR73/round69_c1_nginx_probe

rc=0

```text
RED r1-all-p rc=1 refused=True
RED r2-probe-sha rc=1 refused=True
RED r3-leg-vector rc=1 refused=True
RED r4-missing-leg rc=1 refused=True
RED r5-grader-sha rc=1 refused=True
ACCEPT synthetic rc=0 accepted=True
SELFTEST red_refused=5/5 green_ok=0 accept_ok=1 ok=True
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round70_c1_nginx_probe.py --selftest --work /fast/scratch/hyaku/kengaku-r73/C1RowAuditR73/round70_c1_nginx_probe

rc=0

```text
RED r1-all-p rc=1 refused=True
RED r2-probe-sha rc=1 refused=True
RED r3-leg-vector rc=1 refused=True
RED r4-missing-leg rc=1 refused=True
RED r5-grader-sha rc=1 refused=True
RED r6-case-sha rc=1 refused=True
RED r7-probe-blob rc=1 refused=True
ACCEPT synthetic rc=0 accepted=True
PATH-INDEPENDENT sha_equal=True
STAGED-STATE changes_on_byte=True
SELFTEST red_refused=7/7 green_ok=0 accept_ok=1 ok=True
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round70_c2_routed_defects.py --selftest --work /fast/scratch/hyaku/kengaku-r73/C1RowAuditR73/round70_c2_routed_defects

rc=0

```text
E1 defect depth-gate-identity problems=['corpus/evidence/round70/c2/depth-gate-provenance.txt:missing']
E2 defect trio-receipt corpus/evidence/round70/gates/trio-nginx.txt:missing
E3 defect instruction-row problems=['anchor', 'no-S242-cite', 'S242-absent']
E4 defect s241-correction S243-absent
E5 defect corpus-index problems=['no-round-69-lesson-row', 'no-round-69-block']
E6 defect r69-landing-receipt corpus/evidence/round70/gates/r69-c2-landing.txt:missing
E7 defect gate-reject problems=['corpus/lessons/round-70.md:missing', 'no-rejected-package-row']
E8 defect wave-validation problems=['.ufo/waves/round-70/w1-validate.rc:missing', '.ufo/waves/round-70/w1-validate.out:missing', '.ufo/waves/round-70/w1-validate.stderr:missing']
DEFECTS n=8
PREDICATE R70-C2 fail
SELFTEST defects-in-fake=8 want=8 all-fail=True
SELFTEST e2-byte-flip-red=True
SELFTEST ok=True
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c1_nginx_probe.py --check-receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round69/nginx/receipt.txt

rc=2

```text
SETUP receipt-missing /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round69/nginx/receipt.txt
```

stderr:
```text
```

### python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin

rc=0

```text
UNIVERSE mode=full files=133 plans_seen=82 plans_only=0
ADVERTISED total=113
REGISTERED total=113 rows=115
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 pass
PREDICATE R73-C1 pass
```

stderr:
```text
```

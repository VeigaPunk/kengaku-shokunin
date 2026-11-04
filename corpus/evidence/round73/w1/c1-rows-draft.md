# C1RowDraftR73 — independently derived registry rows

Axes: coverage and calibration. These are drafts only; no lane implementation file was edited. Names follow current registry naming; kind follows returned 0-clean/1-failed verdicts, not filenames containing “probe”. All eight instruments judge and are gates.

## Eight-row splice block

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `round32-c1-verify` | gate | `python3 plans/round32_c1_verify.py --lane .` | `0` clean: six checks hold or self-test passes; `1` failed: V0 absent expect, V1–V6 defects or self-test failure (uncaught input errors also exit 1, could-not-evaluate); `2` could-not-evaluate: argparse usage | `python3 plans/round32_c1_verify.py --selftest` | ENTRY benchmark-grader-semantics.md; PINS `66f92766`, `9be8d8fe`, `2412.05579`; V6 binds `.ufo/waves/round-32/claims/adoption-expect.json` sha256 and `exit=1` in control-nothing.txt | read-only lane and expect/control bytes; self-test creates and removes a TemporaryDirectory | kengaku |
| `round32-defects` | gate | `python3 plans/round32_defects.py --lane .` | `0` clean: seven checks hold or self-test passes; `1` failed: any R1–R7 defect, frozen-list mismatch or self-test failure; `2` could-not-evaluate: argparse usage | `python3 plans/round32_defects.py --selftest` | no fixed digest — literals `a44b5a8` superseded by `ae95fe0`, CLI receipt exit tokens and corrected path, lesson locators and S086 erratum; absolute fleet round-31/32 reports; R2 reads master tip | read-only lane, absolute fleet reports and git plumbing; self-test writes/removes temporary report fixtures | kengaku |
| `round66-c1-tensor-probe` | gate | `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt` | `0` clean: frozen five-case vectors match or self-test passes; `1` failed: receipt/vector or self-test defect (missing receipt raises FileNotFoundError and exits 1, could-not-evaluate); `2` could-not-evaluate: SETUP run prerequisites, missing work or argparse usage | `python3 plans/round66_c1_tensor_probe.py --selftest --work DIR` | grader sha256 `4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290`; five-case FROZEN_TABLE; re-derived probe/case/junit hashes; round66/tensor/receipt.txt and receipt.junit/; TORCH `2.15.0+cpu` | check is read-only; run writes --work, --receipt and sibling <stem>.junit/, plus ~/.local/share/kengaku-r66/port-12355.lock; self-test writes/removes a child of --work; no venv installation by this script | kengaku |
| `round69-c1-nginx-probe` | gate | `python3 plans/round69_c1_nginx_probe.py --check-receipt corpus/evidence/round69/nginx/receipt-v2.txt` | `0` clean: predicate/self-test holds, or help/table reporting completed (table is not a verdict); `1` failed: clause/vector/coverage or self-test defect; `2` could-not-evaluate: SETUP prerequisites/missing receipt or argparse usage | `python3 plans/round69_c1_nginx_probe.py --selftest --work DIR` (optional `--green-receipt PATH`) | grader sha256 `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0`; TB2_PIN `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; frozen CASES/LEGS; own-probe digest; receipt-v2.txt (not absent receipt.txt) | check/table read-only; battery writes --work, optional --receipt/--evidence-dir and ~/.local/share/kengaku-r69/port-8080.lock; self-test writes under --work | kengaku |
| `round69-c2-routed-defects` | gate | `python3 plans/round69_c2_routed_defects.py --root .` | `0` clean: DEFECTS n=0 or self-test passes; `1` failed: any E1–E7 defect or self-test failure (uncaught evaluation errors also exit 1, could-not-evaluate); `2` could-not-evaluate: missing/non-directory --work or argparse usage | `python3 plans/round69_c2_routed_defects.py --selftest --work DIR` | TREE `27f649f8`, LANDING `1ec2e60a`; provenance-erratum.txt input digests re-derived at both revisions; round69/gates/depth-gate.txt and trio.txt compared to fresh commands; seven correction checks | read-only check including git show and fresh depth/trio commands; self-test writes fake-lane and creates/commits a git fixture under --work (not executed by this seat) | kengaku |
| `round70-c1-nginx-probe` | gate | `python3 plans/round70_c1_nginx_probe.py --check-receipt corpus/evidence/round70/nginx/receipt.txt` | `0` clean: predicate/self-test holds, or help/table reporting completed (table is not a verdict); `1` failed: clause/vector/coverage/digest or self-test defect; `2` could-not-evaluate: SETUP prerequisites/missing receipt or argparse usage | `python3 plans/round70_c1_nginx_probe.py --selftest --work DIR` (optional `--green-receipt PATH`) | grader sha256 `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0`; TB2_PIN `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; seven CASE_SHA pins and STAGED_INPUTS; frozen CASES/LEGS; own-probe and git blob digests; round70/nginx/receipt.txt | check read-only; battery writes --work, optional --receipt/--evidence-dir and ~/.local/share/kengaku-r70/port-8080.lock; self-test under --work; --render-table --stage-sha DIR stages cases in DIR | kengaku |
| `round70-c2-routed-defects` | gate | `python3 plans/round70_c2_routed_defects.py --root .` | `0` clean: eight checks hold, self-test passes or all eight mutants killed; `1` failed: E1–E8 defect, self-test failure or mutant not killed; `2` could-not-evaluate: missing/non-directory --work or argparse usage | `python3 plans/round70_c2_routed_defects.py --selftest --work DIR`; `--mutants --work DIR` | INSTRUCTION_SHA `26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99`; anchor instruction.md:6-11,15-18; R69_LANDING_REV `4038bb11`; round69 depth copies, round70 depth provenance/trio/r69-c2-landing receipts and round70 wave validation files | read-only check and fresh trio command; self-test/mutants create fake-lane and mutant scripts under --work | kengaku |
| `round73-c2-registry-audit` | gate | `python3 plans/round73_c2_registry_audit.py --lane .` | `0` clean: MISMATCH 0 / PREDICATE R73-C2 pass, self-test passes or mutant criterion holds; `1` failed: any D1–D4 defect, self-test failure or mutant criterion failure; `2` could-not-evaluate: no SKILL.md, absent --work or non-directory fixture work, or argparse usage | `--selftest --work DIR`; `--mutants --work DIR` | SKILL.md registry and every row entry script; round-72 erratum in claims input `plans/round-71-claims.md`, ERRATUM_ITEMS labels bound to `c80fcdb3` and `d8a77d3f`; round-73 contract `plans/round-73-claims.md` documents the audit but is not read by the audit; no input digest pins | lane audit read-only; fixture/mutant modes write under --work and remove the entire supplied work tree in finally | kengaku |

## Source traceability

All name cells identify the named script; owner is the assigned lane `kengaku`. Each remaining cell is grounded below; hashes identify the bytes opened and help-tested. `--help` establishes accepted spelling, not execution success.

- `plans/round32_c1_verify.py`: lines 32–38 constants; 121–133 V6; 146–195 self-test/main. SHA256 `b348dc967a815e21734122dc968a64dcc93e74ea711382a9f04dd3242dfc225f`.
- `plans/round32_defects.py`: lines 43–51 inputs; 76–108 revision/report checks; 205–269 self-test/main. SHA256 `064289153d4b49431e135a2f8275affab2e845e25cde91ae45365f98ebdcdf06`.
- `plans/round66_c1_tensor_probe.py`: lines 16–41 contract; 56–100 pins/table; 153–252 run/write/exit; 255–402 check/self-test/main. SHA256 `7640a639bbfeeb5276763fe05f63d25e14d2544d5ffc98faa0fabff1e172106e`.
- `plans/round69_c1_nginx_probe.py`: lines 45–119 pins/table; 265–282 lock; 408–484 battery; 487–584 receipt check; 587–729 self-test/main. SHA256 `0f491333743222c04bf3fe10d05faaf955c03b71307f50cff24364ee5879d6d7`.
- `plans/round69_c2_routed_defects.py`: lines 41–64 inputs/pins; 133–271 checks/verdict; 274–405 fixture/main. SHA256 `ea28b006d528a99befdc193c5463ef552b0a15d0b71b03a091ec011fae115485`.
- `plans/round70_c1_nginx_probe.py`: lines 51–168 pins/table; 304–348 digest; 350–367 lock; 501–578 run; 581–727 check; 730–915 self-test/table/main. SHA256 `9c9effeb004a4207b6811e8b9aa84907214ffe9d74631456e6b55846dbb43c4b`.
- `plans/round70_c2_routed_defects.py`: lines 49–73 inputs/pins; 122–351 checks/verdict; 354–468 fixtures/mutants/main. SHA256 `367ce58e41799a75b9fd3a9df5ad032c1fe30acc89b7fb4bba32ffb7c35a36fb`.
- `plans/round73_c2_registry_audit.py`: lines 43–58 columns/kinds/owner/errata; 124–157 row pricing; 205–234 verdict; 288–425 fixtures/mutants/main. SHA256 `9ec8f4d2ba2233751f3ef54c31fe169dfd89b39249dcc459b6b9e75756345828`.

## Exact help receipts

### plans/round32_c1_verify.py

Command: `python3 plans/round32_c1_verify.py --help` (absolute script path; cwd seat scratch). Exit `0`. First usage line:

```text
usage: round32_c1_verify.py [-h] [--lane LANE] [--selftest]
```

Full stdout:

```text
usage: round32_c1_verify.py [-h] [--lane LANE] [--selftest]

Second receipt for round 32's C1: the literals `adoption_check.py` does not
read.

options:
  -h, --help   show this help message and exit
  --lane LANE
  --selftest
```

Stderr: empty.

### plans/round32_defects.py

Command: `python3 plans/round32_defects.py --help` (absolute script path; cwd seat scratch). Exit `0`. First usage line:

```text
usage: round32_defects.py [-h] [--lane LANE] [--selftest]
```

Full stdout:

```text
usage: round32_defects.py [-h] [--lane LANE] [--selftest]

Re-derive the seven defect items round 31's non-author closure routed to this
lane.

options:
  -h, --help   show this help message and exit
  --lane LANE
  --selftest
```

Stderr: empty.

### plans/round66_c1_tensor_probe.py

Command: `python3 plans/round66_c1_tensor_probe.py --help` (absolute script path; cwd seat scratch). Exit `0`. First usage line:

```text
usage: round66_c1_tensor_probe.py [-h] (--run |
```

Full stdout:

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

Stderr: empty.

### plans/round69_c1_nginx_probe.py

Command: `python3 plans/round69_c1_nginx_probe.py --help` (absolute script path; cwd seat scratch). Exit `0`. First usage line:

```text
usage: round69_c1_nginx_probe.py [-h] [--lane LANE] [--work WORK]
```

Full stdout:

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

Stderr: empty.

### plans/round69_c2_routed_defects.py

Command: `python3 plans/round69_c2_routed_defects.py --help` (absolute script path; cwd seat scratch). Exit `0`. First usage line:

```text
usage: round69_c2_routed_defects.py [-h] [--root ROOT] [--selftest]
```

Full stdout:

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

Stderr: empty.

### plans/round70_c1_nginx_probe.py

Command: `python3 plans/round70_c1_nginx_probe.py --help` (absolute script path; cwd seat scratch). Exit `0`. First usage line:

```text
usage: round70_c1_nginx_probe.py [-h] [--lane LANE] [--work WORK]
```

Full stdout:

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

Stderr: empty.

### plans/round70_c2_routed_defects.py

Command: `python3 plans/round70_c2_routed_defects.py --help` (absolute script path; cwd seat scratch). Exit `0`. First usage line:

```text
usage: round70_c2_routed_defects.py [-h] [--root ROOT] [--selftest]
```

Full stdout:

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

Stderr: empty.

### plans/round73_c2_registry_audit.py

Command: `python3 plans/round73_c2_registry_audit.py --help` (absolute script path; cwd seat scratch). Exit `0`. First usage line:

```text
usage: round73_c2_registry_audit.py [-h] [--lane LANE] [--selftest]
```

Full stdout:

```text
usage: round73_c2_registry_audit.py [-h] [--lane LANE] [--selftest]
                                    [--mutants] [--work WORK]

options:
  -h, --help   show this help message and exit
  --lane LANE
  --selftest
  --mutants
  --work WORK
```

Stderr: empty.

## Known entry correction

The live appended round69 nginx row names `corpus/evidence/round69/nginx/receipt.txt`, which is absent (observed `SETUP receipt-missing`, exit 2). File discovery locates `receipt-v2.txt` and `receipt-v1-checker-broken.txt`; this draft selects v2, rather than publishing a known dead entry. A fixture audit only prices row structure and cannot establish historical predicate truth.

## Fixture proof — all transcripts

The requested copy list omits root `grader.py`, although an existing registry row requires it. The literal-copy attempt below therefore yields two existing-row defects both before and after the splice. The corrected fixture additionally copies the discovered root `grader.py` unchanged; no registry declaration or predicate is relaxed. Existing eight named rows are removed for baseline and replaced with this draft. The pre-existing five-cell `round66_c1_tensor_probe` orphan is preserved (both parsers skip it); no pre-existing defect is silently repaired.

### literal-copy baseline

Cwd: `/fast/scratch/hyaku/kengaku-r73/C1RowDraftR73/fixture`

```sh
python3 plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C1RowDraftR73/fixture
```

Exit `1`; stdout:

```text
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=1
D1 defect n=1
  DEFECT SCRIPT-MISSING grader.py
D2 defect n=1
  DEFECT `hermetic-grader`:entry:script-absent:grader.py
D3 ok n=0
D4 ok n=0
MISMATCH 2
DEFECTS n=2
PREDICATE R73-C2 fail
```

Stderr: empty.

### literal-copy draft splice

Cwd: `/fast/scratch/hyaku/kengaku-r73/C1RowDraftR73/fixture`

```sh
python3 plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C1RowDraftR73/fixture
```

Exit `1`; stdout:

```text
INSTRUMENTS total=114 derived=registry rows=114
PARSED scripts=114 failed=1
D1 defect n=1
  DEFECT SCRIPT-MISSING grader.py
D2 defect n=1
  DEFECT `hermetic-grader`:entry:script-absent:grader.py
D3 ok n=0
D4 ok n=0
MISMATCH 2
DEFECTS n=2
PREDICATE R73-C2 fail
```

Stderr: empty.

### corrected round69 entry check

Cwd: `/fast/scratch/hyaku/kengaku-r73/C1RowDraftR73`

```sh
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round69_c1_nginx_probe.py --check-receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round69/nginx/receipt-v2.txt
```

Exit `1`; stdout:

```text
CHECK ok cases=5 legs=8 seen_p=8 seen_f=6
DEFECT leg-coverage test_nginx_running p=5 f=0
DEFECT leg-coverage test_custom_404_page p=5 f=0
DEFECT stored-predicate PREDICATE R69-C1 fail
CHECK stored-predicate=fail derived=fail
PREDICATE R69-C1 fail
```

Stderr: empty.

### baseline

Cwd: `/fast/scratch/hyaku/kengaku-r73/C1RowDraftR73/fixture`

```sh
python3 plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C1RowDraftR73/fixture
```

Exit `0`; stdout:

```text
INSTRUMENTS total=106 derived=registry rows=106
PARSED scripts=106 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
```

Stderr: empty.

### draft-splice

Cwd: `/fast/scratch/hyaku/kengaku-r73/C1RowDraftR73/fixture`

```sh
python3 plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C1RowDraftR73/fixture
```

Exit `0`; stdout:

```text
INSTRUMENTS total=114 derived=registry rows=114
PARSED scripts=114 failed=0
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MISMATCH 0
DEFECTS n=0
PREDICATE R73-C2 pass
```

Stderr: empty.

The corrected baseline and draft splice both print `MISMATCH 0`, exit 0; the eight additions introduce no defect. The row count changes 106 → 114, independently exposing the frozen claim’s literal 106-row target conflict. The round69 v2 entry is runnable but intentionally red (six of eight legs have F witnesses); a runnable entry is not a green historical predicate. No bytecode/import caches were written by these retained runs.

Cleanup: fixture receipts were persisted here before the corrected fixture tree was removed in `finally`. The initial literal-copy attempt was removed before its in-memory transcript was persisted; this ordering lapse is recorded, not represented as meeting the copy-before-delete discipline.

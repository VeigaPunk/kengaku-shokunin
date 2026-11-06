# MutC1 — mutation test of the R99-C1 counter and probe (round 99)

Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` · seat `MutC1` · 2026-11-06
Measured `T f72a8bc710b12473b5c768004e2581f980d924f4` · `BASE 2233a66195e3d3d85856248fb8f66c1d8127cede` ·
freeze `F 24a5a5554130065917d55618ae10309403abf60d` · receipts commit `23d58036` (not measured; the clone is at `T`).

Frozen instruments under test (values from the frozen-instruments table at `F`, confirmed on the working tree at `T`):

| file | sha256 |
|---|---|
| `plans/round99_c1_replay.py` (counter) | `3619199e709dfd542e39ac1d6f020ca84110731dcdf6122e524436c88bb8ff23` |
| `plans/round99_bnfit_probe.py` (probe) | `afacbf81fcc84fd9b5216b6a3e66072cddc565291617bfaaf62e515c6d5563eb` |
| `plans/round99-cases.json` (table) | `ee76e2b5ae7477849fd74e66e969ae687bfb883a8affdae54091bea2d2839e73` |
| `plans/anchor_digest_check.py` (gate) | `11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2` |
| `corpus/evidence/round99/tb2-bn-fit-modify/test_outputs.py` | `364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b` |
| `corpus/evidence/round99/bn-fit-modify-solution/final_bn_sample.csv` | `982a7441d4469c4b09eb0c9a27d5ca62f7fb38bdee6542b56a767e0c4b26ab66` |

No lane file was edited; every write is under `.ufo/waves/round-99/w1/` (this report and its `MutC1/`
evidence directory) or the private scratch.

## Method

* One `git clone --shared` of the lane, detached at `T`, under `/fast/scratch/hyaku/kengaku-r99/MutC1/clone`
  (`git rev-parse --show-toplevel` asserted equal to the clone before every fixture write).
* 40 mutants, each **one commit on parent `T`** built with `git commit-tree` from a temporary index
  (`git read-tree T` → `git update-index --cacheinfo` → `git write-tree` → `git commit-tree -p T`), plus a
  local `refs/heads/mut-<id>`. The working tree is never checked out at a mutant and is never modified;
  the pristine bytes are the same bytes before and after the matrix.
* Detector: the frozen counter, unmodified, run from the clone root:
  `python3 plans/round99_c1_replay.py --lane . --rev <mutant commit> --work <per-mutant dir> --grader-venv G`.
  Every run re-executes the full 13-case probe through `L6` (real pytest in bubblewrap), so the matrix is
  behavioural, not static.
* Seven builder mutants (`M19`–`M25`) were additionally run as the **mutated probe itself** from a
  `git archive` of the mutant commit (`--lane <extract>`), to isolate the observation comparison that `L6`
  performs from the `TOOL_SHA` stamp that also trips on any probe byte change.
* One pair (`M37`) was executed twice: by the pristine counter (from the clone) and by the **weakened
  counter itself** from a second `--shared` clone checked out at the mutant commit.
* Grader venv `G`: `uv venv -p 3.13` → CPython 3.13.16; `pytest==8.4.1 pandas==2.3.2 scipy==1.16.1`,
  resolving `numpy 2.5.4` — exactly the probe's `GRADER_WANT` / `BUILDER_WANT`. The counter and the probe
  driver run under the host `python3` (3.14.8), as the frozen command specifies; the sandboxed build and
  pytest steps run under `G/bin/python` 3.13.16.

Baseline (pristine `T`, before the matrix), rc 0, 18.2 s:

```
REV f72a8bc710b12473b5c768004e2581f980d924f4
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass L10=pass L11=pass
TARGET executed_rows=43 member=bn-fit-modify cells=file-artifact:34 set_equals_base_plus_member=1 located=1 executed=1 cases=13 legs=130 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0
PREDICATE R99-C1 pass
```

Restored run at `T` after the matrix, rc 0, 11.6 s: `diff -u base.out restored.out` is empty. No run was
inconclusive in the baseline sense; `M15`/`M16` are refusals (rc 2), not leg failures.

## Kill matrix (40 mutants: 30 killed, 10 survived)

`killed` = `PREDICATE R99-C1 fail` (rc 1) or refusal (rc 2); `SURVIVED` = `PREDICATE R99-C1 pass` (rc 0).

| # | mutant | edit (one commit on T) | expected detector | failing legs | rc | verdict |
|---|---|---|---|---|---|---|
| 1 | `M01` | receipt CASE C01 observed flipped P->F | L5/L6 | L5, L6 | 1 | killed |
| 2 | `M01b` | receipt drops case C13 (CASE+DETAIL) | L5/L6 | L5, L6 | 1 | killed |
| 3 | `M02` | receipt CASE C12 predicted+observed flipped to pass | L5/L6 | L5, L6 | 1 | killed |
| 4 | `M03` | receipt DETAIL C03 final digest edited | L6 | L6 | 1 | killed |
| 5 | `M04a` | receipt LANE_TIP -> descendant 23d58036 | L3 | L3 | 1 | killed |
| 6 | `M04b` | receipt LANE_TIP -> ancestor BASE 2233a661 | L3 | — | 0 | **SURVIVED** |
| 7 | `M05` | case table C11 predicted flipped | L4/L5 | L4, L5, L6, L9 | 1 | killed |
| 8 | `M06` | ledger member classes += numeric-band | L7 | L7 | 1 | killed |
| 9 | `M07` | ledger member round 99->98 | L7 | L7 | 1 | killed |
| 10 | `M08` | ledger member receipt path edited | L7 | L7 | 1 | killed |
| 11 | `M09` | ledger member subject tb2-header->tb2-body | L7 | L7 | 1 | killed |
| 12 | `M10` | second executed member build-pmars -> located | L7 | L7 | 1 | killed |
| 13 | `M11` | other executed member loses file-artifact class | L7/cells | — | 0 | **SURVIVED** |
| 14 | `M12` | SOURCES S342 added, unbound digest | L10 | L10 | 1 | killed |
| 15 | `M13` | SOURCES S342 added, correctly bound | L10/new_rows | — | 0 | **SURVIVED** |
| 16 | `M14` | SOURCES S341 removed | L10/new_rows | — | 0 | **SURVIVED** |
| 17 | `M15` | capture test_outputs.py byte appended | L2 | — | 2 | killed (rc 2) |
| 18 | `M16` | fixture final_bn_sample.csv byte appended | L2 | — | 2 | killed (rc 2) |
| 19 | `M17` | probe comment inserted | L6/L8/L9 | L6, L8, L9 | 1 | killed |
| 20 | `M18` | counter comment inserted | L11 | L11 | 1 | killed |
| 21 | `M19` | builder C03 draws U instead of D | L6/L8 | L6, L8, L9 | 1 | killed |
| 22 | `M20` | builder C03 seed 3->5 | L6(DETAIL)/L8 | L6, L8, L9 | 1 | killed |
| 23 | `M21` | builder C11 shift 0.045->0.060 | L6/L8 | L6, L8, L9 | 1 | killed |
| 24 | `M22` | builder C12 shift 0.050->0.040 | L6/L8 | L6, L8, L9 | 1 | killed |
| 25 | `M23` | builder C13 quantile grid -> seeded random | L6(DETAIL)/L8 | L6, L8, L9 | 1 | killed |
| 26 | `M24` | builder comment only | L6/L8 | L6, L8, L9 | 1 | killed |
| 27 | `M25` | probe mismatch check disabled (ok=True) | L6/L8 | L6, L8, L9 | 1 | killed |
| 28 | `M26` | receipt LEG_ORDER first two legs swapped | none | — | 0 | **SURVIVED** |
| 29 | `M27` | receipt HOST_BASH edited | L9 | L9 | 1 | killed |
| 30 | `M28` | receipt SUBJECT_SHA edited | L2 | L2 | 1 | killed |
| 31 | `M29` | receipt DATASET_SHA edited | L2 | L2 | 1 | killed |
| 32 | `M30` | ledger member status executed->located | L7 | L7 | 1 | killed |
| 33 | `M31` | extra file plans/round99_extra.txt added | none | — | 0 | **SURVIVED** |
| 34 | `M32` | SKILL file-artifact cell 34->35 | none | — | 0 | **SURVIVED** |
| 35 | `M33` | claims candidate-bytes SOURCES sha edited | none | — | 0 | **SURVIVED** |
| 36 | `M34` | receipt mismatches 0->1 | none | — | 0 | **SURVIVED** |
| 37 | `M35` | receipt GRADER_SIDE stamp 8.4.1->8.4.0 | L6 | L6 | 1 | killed |
| 38 | `M37` | weakened counter L10 + unbound SOURCES row (pair) | L11 | L10, L11 | 1 | killed |
| 39 | `M38` | frozen gate anchor_digest_check.py edited at rev | none | — | 0 | **SURVIVED** |
| 40 | `M39` | receipt file deleted | L1 | L1, L2, L3, L5, L6, L9 | 1 | killed |

Representative actual outputs (full text in `MutC1/results/<id>.out`):

```
M03  DEFECT L6 rerun rc=0 obs=26 want=26 equal=False stamps_equal=True
M04a DEFECT L3 LANE_TIP 23d580366db2a3462c9bbfc3b0ff71bce5837374 not an ancestor of f7a4048758c6
M05  DEFECT L4 case table 0f3766075a08 vs frozen ee76e2b5ae74
     DEFECT L5 case C11 predicted=P,P,P,P,P,P,P,P,P,1 observed=P,P,P,P,P,P,P,P,P,1 frozen=P,P,P,P,P,P,P,P,F,0
     DEFECT L6 rerun rc=1 obs=26 want=26 equal=False stamps_equal=False
     DEFECT L9 stamps tool=afacbf81fcc8 table=ee76e2b5ae74 bash=GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)
M10  DEFECT L7 ledger member=executed round=99 executed_total=42 cells={'file-artifact': 33} legacy_fields=True set_added=['bn-fit-modify'] set_removed=['build-pmars']
M12  DEFECT L10 new SOURCES rows=9 gate-flagged=S342
M15  DEFECT SETUP probe-rerun DEFECT SETUP capture sha mismatch tb2-bn-fit-modify/test_outputs.py
     PREDICATE R99-C1 could-not-evaluate
M18  DEFECT L11 counter 62da16ce070b vs frozen 3619199e709d
M24  DEFECT L6 rerun rc=0 obs=26 want=26 equal=True stamps_equal=False
     DEFECT L8 probe 4fb7ad6b766e vs frozen afacbf81fcc8
M27  DEFECT L9 stamps tool=afacbf81fcc8 table=ee76e2b5ae74 bash=GNU bash, version 5.2.0(1)-release (x86_64-pc-linux-gnu)
M39  DEFECT L1 receipt absent at revision: corpus/evidence/round99/bnfit-probe.txt
```

## Which leg is load-bearing

* **L1** receipt presence — `M39` only (the other failures in that run cascade from the absent receipt).
* **L2** capture/fixture pins and receipt subject/test.sh/solve/dataset/fixture stamps — `M28`
  (`SUBJECT_SHA`) and `M29` (`DATASET_SHA`) alone. `M15`/`M16` never reach a printed leg: the probe's own
  pin check aborts the rerun and the counter returns `could-not-evaluate` before printing `LEGS`; the L2
  condition is false but its defect line is swallowed by the early return.
* **L3** `LANE_TIP` ancestry — `M04a` only. `M04b` shows it is ancestry, not equality (survivor S4).
* **L4** frozen table sha — `M05` (with L5/L6/L9). No single-mutant run makes L4 the sole killer, because
  the receipt's `CASE_TABLE_SHA` stamp (L9) and the rerun (L6) also move; L4 is the only leg that still
  knows the frozen value when the receipt stamp is coordinated (round-98 `d3`).
* **L5** receipt vector equality — `M01`, `M01b`, `M02`, `M05`. It never reads the probe, so it cannot
  catch any builder mutation (all of `M19`–`M25` show `L5=pass`).
* **L6** rerun reproduction — `M03` (observation block only, `stamps_equal=True`), `M35`
  (`GRADER_SIDE` stamp only), plus `M01`/`M02`/`M05` and every probe mutation `M17`–`M25`.
* **L7** ledger — `M06` (classes), `M07` (round), `M08` (receipt), `M09` (subject), `M10` (second member
  flipped: `set_removed=['build-pmars']`), `M30` (status). Set equality is load-bearing in both
  directions; the per-class census is computed but not asserted (survivor S1).
* **L8** frozen probe sha — `M17`–`M25` (never sole killer among single mutants; the receipt `TOOL_SHA`
  stamp and L6's stamp check also move).
* **L9** receipt stamps — `M27` (`HOST_BASH`) alone; plus `M05`, `M17`–`M25`, `M39`.
* **L10** new SOURCES rows — `M12` alone; `M37` with L11. `M13` (a correctly bound ninth row) passes, so
  L10 is specific to *bad* anchors, not to novelty — but the row count is not asserted (survivor S2).
* **L11** counter's own bytes — `M18` alone; `M37` with L10.

**Round-98 routed defect 2 (counter self-integrity) is closed in the shape that mattered.** `M37` is the
round-98 `d1` pair — the counter's L10 weakened to `bool(added)` plus the unbound SOURCES row it should
reject. Run by the pristine counter it fails L10 and L11. Run by the **weakened counter itself** from a
checkout at the mutant commit, L10 passes (the honest `new_rows_flagged=1` is printed and ignored) and
L11 alone kills it:

```
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass L10=pass L11=fail
TARGET executed_rows=43 member=bn-fit-modify cells=file-artifact:34 set_equals_base_plus_member=1 located=1 executed=0 cases=13 legs=130 mismatches=0 new_rows=9 new_rows_flagged=1 defects=1
DEFECT L11 counter 81aea75baf39 vs frozen 3619199e709d
PREDICATE R99-C1 fail
```

## Probe-builder mutants: what L5 and L6 actually catch

`L5` compares the receipt's CASE vectors to the frozen table; it never reads the probe, so it catches
none of `M19`–`M25` (`L5=pass` in every run). `L6` compares the rerun's OBSERVATIONS block to the
receipt's and then four stamps (`TOOL_SHA`, `CASE_TABLE_SHA`, `GRADER_SIDE`, `BUILDER_SIDE`). The direct
mutated-probe runs isolate the observation comparison:

| mutant | builder edit | probe rc | observation block vs receipt |
|---|---|---|---|
| `M19` | C03 draws `U` instead of `D` | 1 | `CASE C03 … observed=…F,0`; `DETAIL C03 final=a9ad7f5f…` → `de8e735a…` |
| `M20` | C03 seed 3 → 5 | 0 | verdicts unchanged; `DETAIL C03 final=` `a9ad7f5f…` → `daec10f5…` |
| `M21` | C11 shift 0.045 → 0.060 | 1 | `CASE C11 … observed=…F,0`; `DETAIL C11 final=` `8fc148c6…` → `5b4f5c39…` |
| `M22` | C12 shift 0.050 → 0.040 | 1 | `CASE C12 … observed=…P,1`; `DETAIL C12 final=` `311bbd9f…` → `ae678248…` |
| `M23` | C13 quantile grid → seeded random | 0 | verdicts unchanged; `DETAIL C13 final=` `390259ae…` → `c1f7e334…` |
| `M24` | builder comment only | 0 | **identical** |
| `M25` | probe mismatch check disabled (`ok = True`) | 0 | **identical** |

So the behavioural comparison catches every builder mutation that changes the built artifact bytes —
including `M20`/`M23`, where no verdict flips and only the `DETAIL` digest moves. It does **not** catch a
probe change that leaves the observation block byte-identical (`M24`, `M25`); those are killed only by the
`TOOL_SHA` stamp (`L6` `stamps_equal=False`), `L8` and `L9`. In the full counter every probe mutation is
therefore killed, but the observation comparison alone is blind to a probe that is weakened without
changing what it prints on pristine inputs. `L5` contributes nothing to any probe mutation.

## Survivors with reasons

### S1 (`M11`) — the TARGET `cells` count is printed, not asserted (high)

Edit: ledger `build-pmars.classes` `["file-artifact","subprocess-exec"]` → `["subprocess-exec"]`.
Actual: `TARGET … cells=file-artifact:33 … defects=0`, `PREDICATE R99-C1 pass`, rc 0.
The frozen predicate requires `cells=file-artifact:34`. L7 checks only the measured member's own
`classes` (`member.get("classes") == MEMBER_CLASSES`) and set equality of executed names; the per-class
census over all 88 members is computed for the TARGET line and never compared to 34. This is the claim's
headline cell count and part of the frozen TARGET text, yet a ledger edit that changes another executed
member's class list passes. Reason: the predicate is `all(legs)`, and no leg reads `cells`.

### S2 (`M14`) — the TARGET `new_rows` count is printed, not asserted (high)

Edit: remove the S341 line from `corpus/SOURCES.md`.
Actual: `TARGET … new_rows=7 … defects=0`, `PREDICATE R99-C1 pass`, rc 0. The frozen predicate requires
`new_rows=8`, and the claim names exactly S334–S341. L10 is `bool(added) and not flagged`: it requires at
least one row added after BASE and none gate-flagged, not the eight named rows. Removing one of eight
leaves seven and passes (removing all eight would fail `bool(added)`). A new SOURCES row can therefore be
dropped after C without the counter noticing; the census would catch it, the counter does not.

`M13` (a correctly bound ninth row) also passes with `new_rows=9` — the same unasserted-count shape. It is
a control by design (round-98 `s2`: L10 is specific to bad anchors), but it confirms that `new_rows` is
descriptive only.

### S3 (`M38`) — the frozen gate is not bound at the measured revision (medium-high)

Edit: append a comment to `plans/anchor_digest_check.py` at the mutant revision.
Actual: all eleven legs pass, rc 0, TARGET identical to baseline. L10 runs `blob(lane, BASE, GATE)` — the
BASE bytes — on a checkout of `--rev`; no leg hashes the gate at `--rev`, although the
frozen-instruments table lists it (`11bb2cad…`). The kill rule "a frozen file changes after F" is
therefore not enforced by the counter for this row. Today BASE = T = frozen value, so the measurement at
T is unaffected; the finding is that a post-F edit to the gate is invisible to the predicate.

### S4 (`M04b`) — `LANE_TIP` is ancestry-only (low-medium)

Edit: receipt `LANE_TIP 24a5a555…` → `2233a661…` (BASE, an ancestor). All legs pass, rc 0. L3 is
`git merge-base --is-ancestor tip rev`; any ancestor (BASE, P0, P1, P2, F) is accepted. `LANE_TIP` is not
in `RERUN_STAMPS`, and the L6 rerun's probe runs against a plain `git archive` extract and prints
`LANE_TIP absent`, so nothing cross-checks the receipt's tip against the measured tree. `M04a` (a
descendant, `23d58036`) is killed by L3, so the leg does catch non-ancestors.

### S5 (`M26`) — the receipt's `LEG_ORDER` is unread (medium)

Edit: swap `bn_exists,ldag_exists` in the receipt's `LEG_ORDER`. All legs pass, rc 0. `parse_receipt`
stores header fields, but no leg compares `LEG_ORDER` to the frozen table's `leg_order`; L6 compares only
the OBSERVATIONS block and four stamps. The CASE vectors are positional, so a forged leg order misreads
which test each verdict belongs to while the receipt remains "verified". This is the round-98 S-B class,
still open.

### S6 (`M31`) — the C diff / candidate-bytes table is unbound (medium)

Edit: add `plans/round99_extra.txt` at the mutant revision. All legs pass, rc 0. No leg compares the
BASE..rev diff to the candidate-bytes table in `plans/round-99-claims.md`; the table is read only at the
freeze commit, and only for the frozen-instruments rows (L4/L8/L11), not for the candidate rows. The kill
rule "C lands exactly the candidate-bytes files plus the receipt" is not enforced. `M32` and `M33` are the
same class.

### S7 (`M32`) — `SKILL.md` is unread (low; declared)

Edit: `SKILL.md` file-artifact cell `executed 34 of 76` → `executed 35 of 76`. All legs pass, rc 0. The
claims declare "no counter reads SKILL.md"; the ledger is the count's source of truth, but see S1 — the
ledger's count is not asserted either.

### S8 (`M33`) — the claims file at the measured revision is unread (low)

Edit: change the candidate-bytes sha for `corpus/SOURCES.md` in `plans/round-99-claims.md` at the mutant
revision. All legs pass, rc 0. `frozen_table` reads the commit that *added* the claims file (F), so the
frozen values are safe by construction; the contract text at the measured revision can drift without
detection. This is the correct side of the freeze for the frozen values, but it means the claims file at
rev is not part of the measured surface.

### S9 (`M34`) — the receipt's `mismatches` line is unread (low; known round-98 S-B)

Edit: `mismatches 0` → `mismatches 1`. All legs pass, rc 0; the counter recomputes `mismatches` from the
CASE lines for its TARGET. Informational only.

### S10 (`M13`) — a correctly bound ninth SOURCES row passes (control)

Edit: append S342 as a duplicate of S334 with its true URL and digest. All legs pass, `new_rows=9`,
`new_rows_flagged=0`. By design (L10 is specific to bad anchors), but it is the same unasserted-count
shape as S2.

## Diagnostics (detection correct, messages weak)

* `L9`'s defect line prints the receipt's stamps, not the measured values: for `M05` it prints
  `table=ee76e2b5ae74` (the receipt's stamp) while the measured table is `0f3766075a08`, so the failing
  comparison is not visible in the line.
* `L2`'s defect line prints `cap` vs `SUBJECT_SHA` only. `M29` edits `DATASET_SHA` and fails L2, but the
  line reads `cap=364069f893e3 receipt=364069f893e3` — two equal 12-char prefixes; the failing field is
  not named.
* `M15`/`M16` are refused by the probe's pin check (rc 2) before `LEGS` is printed, so the L2 failure is
  computed and then swallowed by the early return. The refusal is honest (not a pass), but the counter
  cannot distinguish a tampered capture from a broken environment in its output.

## Restoration evidence

* The clone's `HEAD` is `T` and `git status --porcelain` is empty after the matrix; the working-tree
  sha256 of the six files above equals the frozen values (`restoration.txt`).
* Every mutant is a commit object on parent `T` under `refs/heads/mut-*` in the fixture only; the main
  clone's working tree was never checked out at a mutant, so no restore was needed. The second clone used
  for the `M37` weakened-counter run was checked out at that mutant commit and removed with the scratch;
  the scratch clone and venv are removed before yield per the seat contract.
* Baseline (`base.out`) and restored (`restored.out`) are byte-identical; both `PREDICATE R99-C1 pass`,
  rc 0.

## Verdict

**30 of 40 mutants killed; 10 survived.** Every assigned input class is killed by the leg the claim names:
receipt CASE/DETAIL edits (L5/L6), `LANE_TIP` non-ancestor (L3), case-table edit (L4/L5/L6/L9), ledger
class/round/receipt/subject/status and second-member flip (L7), a gate-flagged new SOURCES row (L10),
capture and fixture byte edits (refused, rc 2), probe byte edit (L6/L8/L9), counter byte edit (L11), and
all five builder mutations of C03/C11/C12/C13 (L6/L8/L9). The round-98 counter self-integrity survivor is
closed by L11 even when the weakened counter is the one running (`M37`).

The two survivors that matter are **S1 (`cells`)** and **S2 (`new_rows`)**: both are fields of the frozen
predicate's TARGET line that the counter computes and prints but never asserts, so a ledger class edit or
a removed SOURCES row makes the counter print a TARGET line that differs from the frozen predicate while
`PREDICATE R99-C1 pass` and rc 0. **S3** (frozen gate unbound at rev) is a frozen-instrument coverage gap;
**S5**/**S6** (receipt `LEG_ORDER`, candidate-bytes table / C diff) and **S4** (`LANE_TIP` ancestry-only)
are provenance-scope gaps; **S7**–**S10** are declared or known informational-field classes. No repair was
attempted in round: findings are routed to round 100.

## Evidence index (`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-99/w1/MutC1/`)

| file | content |
|---|---|
| `../MutC1.md` | this report (sibling of this directory) |
| `base.out` | pristine `T` run (LEGS/TARGET/PREDICATE, rc 0) |
| `restored.out` | restored `T` run after the matrix (byte-identical to `base.out`) |
| `results/<id>.out`, `results/<id>.rc` | one counter run per mutant |
| `results/<id>.probe.out`, `.probe.rc` | direct mutated-probe runs for `M19`–`M25` |
| `results/M37.weakened-counter.out` | the weakened counter executed from its own checkout |
| `matrix.json`, `matrix.txt`, `kill_matrix.md` | kill matrix (machine-readable and markdown) |
| `summary.json`, `manifest.json` | per-mutant results, commits, before/after hashes |
| `hashes.md` | per-mutant before/after sha256 and commit |
| `restoration.txt` | pristine HEAD, clean status, pins, baseline=restored, mutant refs |
| `mutate.py`, `analyse.py` | fixture builder/runner and summariser |

## Tooling record

| tool | version | channel | reason |
|---|---|---|---|
| CPython (grader venv) | 3.13.16 | `uv venv -p 3.13` | `test.sh`'s `-p 3.13` pin |
| pytest | 8.4.1 | `uv pip install` | `test.sh`'s `-w pytest==8.4.1` pin |
| pandas | 2.3.2 | `uv pip install` | `test.sh`'s `-w pandas==2.3.2` pin |
| scipy | 1.16.1 | `uv pip install` | `test.sh`'s `-w scipy==1.16.1` pin |
| numpy | 2.5.4 | resolved by the above | the probe's `BUILDER_WANT` pin |

No pacman transaction was run (host-wide pause). No tool outside the grader pins was installed.

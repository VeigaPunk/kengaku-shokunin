# MutTesterC1 — round 95 mutation test of `plans/round95_c1_replay.py` (R95-C1 counter)

Seat: MutTesterC1 (kengaku round 95, wave 1, leaf; no subagents). Lane `kengaku-shokunin`, measured tip
T `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`. Pristine counter sha256
`c7e13dc9146ebc1fc3fcd07b404f985ce842e33fdea38c9a4cc21b3b3a7ff3e2` (lane file read-only; never written).
Host bwrap `/usr/bin/bwrap` 0.13.1. Tools installed or upgraded: none.

Full write-up and all raw receipts: `MutTesterC1/report.md`, `MutTesterC1/receipts/`, mutant generator
`MutTesterC1/tools/gen_mutants.py`, harness hook `MutTesterC1/tools/drv_mutant_hook.py`, forgery builder
`MutTesterC1/tools/build_fixtures.py`, mutant bytes `MutTesterC1/mutants/files/`, matrix
`MutTesterC1/receipts/mutant-matrix.tsv`.

## Scope

1. 32 mutants of the pristine counter (`plans/round95_c1_replay.py` at T; 31 single-point, one two-point m03+m04), every
   anchor asserted to occur exactly once: the round-94 survivor analogues m01–m13 (+ m03a, m03b, m03+m04),
   and new n01–n16 on this round's additions (L6 `stamps_equal`, L7 `legacy_ok`, L2 `UPSTREAM_BOTTLE_SHA`,
   the `--work`-inside-lane guard, L4 pin, L9 host stamps, `parse_receipt` CASE lines, `--bwrap` injection).
2. Each mutant run through the committed round-95 driver `.ufo/waves/round-95/L1/controls/c1_controls.py`
   (unmodified; only the counter path is redirected by `drv_mutant_hook.py`). The driver rebuilds the nine
   receipt-side controls (pos, D4–D8, ledger-only, member-swap, sandbox-red) in its own scratch clone.
   Each mutant's signature (rc, LEGS, PREDICATE, TARGET, DEFECT leg codes) is compared with the committed
   `c1-*.txt`, plus the do-nothing controls at BASE and P1 (committed `c1-base.txt`, `c1-at-P1.txt`).
3. Each mutant run against T itself (rc 0 pristine; "T" column below).
4. Held-out forgeries (not in the committed set): 14 fixtures on scratch clones of T built by
   `tools/build_fixtures.py`, plus three special invocations (unresolved revision, `--work` inside a clone,
   a broken-but-present `--bwrap`). Every mutant × every fixture: 33 counters (pristine + 32 mutants) × 17 inputs = 561 counter runs; all receipts
   under `receipts/matrix/`.

## Harness fidelity (pristine)

- Pristine at T: `LEGS L1=pass … L9=pass`, `TARGET executed_rows=39 … cases=15 legs=105 … defects=0`,
  `PREDICATE R95-C1 pass`, rc 0 (`receipts/runs/pristine/T.txt`).
- Pristine driver run: 9/9 controls OK; each control's signature equals the committed `c1-*.txt`
  (`receipts/runs/pristine/controls/`). Pristine at BASE and P1 equals committed `c1-base`/`c1-at-P1`.

## Round-94 survivors re-measured on the round-95 control set

| R94 id | R94 status (committed set then) | R95 committed controls | R95 held-out | R95 status |
|---|---|---|---|---|
| m01 L7 member-set dropped | KILLED by member-swap | **NOT killed** — R95 member-swap also breaks `cells` (serialization-schema 7), so L7 fails on cells regardless of the set check | C-swap rc 1→0, D-squash rc 1→0 | **REGRESSION**: R94 kill lost |
| m02 L7 BASE-absent fail-open | SURVIVES | survives | D-squash rc 1→0 | survives, flipped |
| m03 L5 coverage dropped | KILLED (ledger-only L5 leg) | KILLED **designated** by D6 (also ledger-only, at-P1) | — | killed (stronger) |
| m04 L6 counts-not-lines | SURVIVES (F1) | survives alone | none alone; flipped only with m03 (A-dup) | survives alone |
| m05 L4 table read at --rev | SURVIVES (F4) | survives | B2 rc 1→0 | survives, flipped |
| m06 L9 stamps skipped | KILLED (L9 leg) | KILLED leg-level (D4, ledger-only, base, at-P1) | I/J/K rc 1→0 | killed |
| m07 L2 grader pin only | SURVIVES (F7) | survives | L-solve: rc 2 both | survives, equivalent |
| m08 sandbox rc2→1 | KILLED (sandbox-red) | KILLED (sandbox-red, verdict) | — | killed |
| m09 L1 absent accepted | KILLED (ledger-only L1 leg) | KILLED (ledger-only L1, designated) | — | killed |
| m10 L3 dropped | SURVIVES (F3) | **KILLED designated** by D5-foreign-lane-tip | — | **newly killed** |
| m11 L8 pin dropped | SURVIVES (F2) | **KILLED designated** by D4-probe-swap | — | **newly killed** |
| m12 exit collapse | KILLED | KILLED (verdict, 9 controls) | all | killed |
| m13 handler rc2→1 | SURVIVES (F5) | survives | UNRESOLVED rc 2→1; WORK-INSIDE-LANE rc 2→1 | survives, flipped |
| m03+m04 interaction | SURVIVES as a D6 forgery (demo only) | KILLED designated by D6 **only because dropping 3 lines changes the count** | A-dup (count-preserving duplicate) rc 1→0 | killed by coincidence; forgery still passes |

Kills the round-95 controls add over round 94 on the R94 set: m10, m11, m03 (designated), m03+m04 (by
count coincidence). Lost: m01. New mutants killed: n01 (D7), n02 (D8), n08 and n14 (also rc flip at T),
n16 (D4 leg-level).

## Full mutant table

Committed = against the nine receipt-side controls and base/at-P1. Held-out = fixtures or special invocations
where the mutant's rc differs from pristine (m12 excluded: exit-collapse flips everything).

| id | mutation | committed | held-out flips | status |
|---|---|---|---|---|
| m01 | L7 set check dropped | — | C-swap, D-squash | SURVIVES committed, flipped |
| m02 | L7 BASE absent → pass | — | D-squash | SURVIVES committed, flipped |
| m03 | L5 both coverage clauses | D6 designated; ledger-only, at-P1 (leg) | — | KILLED |
| m03a | L5 seen-set dropped | — | none (A-dup, M-extra rc 1 via L6) | survives, redundant with L6 |
| m03b | L5 count dropped | — | none (M-extra rc 1 via L6) | survives, redundant with L6 |
| m04 | L6 counts not lines | — | none alone | survives alone |
| m05 | L4 table read at --rev | — | B2 | SURVIVES committed, flipped |
| m06 | L9 stamps skipped | D4, ledger-only, base, at-P1 (leg) | I, J, K | KILLED leg-level |
| m07 | L2 grader pin only | — | L-solve (rc 2 both) | survives, equivalent |
| m08 | sandbox could-not-evaluate → fail | sandbox-red (verdict) | — | KILLED |
| m09 | L1 receipt-absent accepted | ledger-only (designated) | — | KILLED |
| m10 | L3 ancestor dropped | D5 (verdict, designated) | — | KILLED |
| m11 | L8 probe pin dropped | D4 (designated) | — | KILLED |
| m12 | exit collapse | 9 controls (verdict) | all | KILLED |
| m13 | handler could-not-evaluate → fail | — | UNRESOLVED, WORK-INSIDE-LANE | SURVIVES committed, flipped |
| m03+m04 | interaction | D6 designated (count) | A-dup | KILLED by coincidence; forgery passes |
| n01 | L6 stamps_equal dropped | D7 designated; D4 leg | — | KILLED |
| n02 | L7 legacy fields dropped | D8 designated | — | KILLED |
| n03 | L2 UPSTREAM pin dropped | — | E-upstream | SURVIVES committed, flipped |
| n04 | `--work`-inside-lane guard dropped | — | WORK-INSIDE-LANE (rc 2→0) | SURVIVES committed, flipped |
| n05 | L5 frozen-vector compare dropped | — | none (H rc 1 via L6) | survives, redundant with L6 |
| n06 | L7 member classes dropped | — | G-member-classes | SURVIVES committed, flipped |
| n07 | L7 executed total / class cells dropped | — | F-classes-other | SURVIVES committed, flipped |
| n08 | L3 merge-base args reversed | pos (verdict), D6–D8, member-swap (leg) | T rc 0→1 | KILLED |
| n09 | L4 pin dropped | — | B1, B2 | SURVIVES committed, flipped |
| n10 | L9 HOST_SED dropped | — | K-host-sed | SURVIVES committed, flipped |
| n11 | L9 HOST_BASH dropped | — | J-host-bash | SURVIVES committed, flipped |
| n12 | L9 HOST_PYTHON dropped | — | I-host-python | SURVIVES committed, flipped |
| n13 | rerun ignores injected `--bwrap` | — | BROKEN-SANDBOX (rc 1→0) | SURVIVES committed, flipped |
| n14 | CASE lines dropped in parse | pos (verdict), others (leg) | T rc 0→1 | KILLED |
| n15 | probe rerun rc check dropped | — | none | survives, equivalent under L8 (argued, not demonstrated) |
| n16 | stamp presence check dropped | D4 (leg) | — | KILLED leg-level |

Tally: 13 survivors of committed controls flipped by a held-out fixture or special invocation; 6 survivors with no
flip (m03a, m03b, m04, m07, n05, n15); 11 killed by a committed designated or verdict change; 2 killed at leg level only
(m06, n16). m09's kill is designated (ledger-only, L1) and counted above.

## Findings (routed to round 96; no instrument touched — FROZEN RULE respected)

Severity words: blocker/major/minor/info. A flip means: pristine rc differs from the mutant's rc on a held-out
input; the pristine verdict on that input is correct in every case except the sandbox case in P-1.

- **F1 major — member-set kill lost (m01).** Round-94's m01 kill came from its member-swap fixture, whose cells
  matched the set. The round-95 member-swap control has `cells={'file-artifact': 30, 'serialization-schema': 7}`
  so L7 fails on cells and m01 is no longer detected by any committed control. Verdict flip, exact command:
  `python3 <scratch>/mutants/m01.py --lane <scratch>/fx/C-swap --rev HEAD --work <w>` → `PREDICATE R95-C1 pass`,
  rc 0. Pristine on the same fixture (`receipts/matrix/C-swap/pristine.txt`): `LEGS … L7=fail`,
  `DEFECT L7 ledger member=executed round=95 executed_total=39 cells={'file-artifact': 30, 'serialization-schema': 6}
  legacy_fields=True set_added=['fix-code-vulnerability', 'mailman'] set_removed=['configure-git-webserver']`, rc 1.
  The forgery is a same-class swap (`configure-git-webserver` unflipped, `mailman` flipped; neither carries the two
  cell classes). Missing control: a same-cells / different-set ledger.

- **F2 major — L4 pin is uncontrolled in its non-absent direction (m05, n09).** No committed control edits the case
  table or the frozen claims row; L4 is only exercised as `absent` (c1-base, c1-at-P1). Pristine rejects both
  forgeries: B1 (table forged, claims untouched) → `DEFECT L4 case table d02b1fad3960 vs frozen ff361d141561`, rc 1;
  n09 (no pin) → rc 0. B2 (table forged + claims row rewritten at the forged rev) → pristine rc 1, m05 (reads claims
  at --rev) → rc 0. This is the exact freeze bypass the claims exist to stop; the counter catches it only because
  the frozen row is read at the adding commit. Missing control: a post-F table edit plus claims-row rewrite judged rc 1.

- **F3 major — the D6 kill of m03+m04 is an accident of the control shape.** D6 drops three CASE lines, so the
  count changes and L6's count-compare still fails. A count-preserving forgery (C02's line replaced by a copy of the
  C01 line; `receipts/matrix/A-dup/`) gives: pristine rc 1 (`DEFECT L5 case coverage 15 of 15`, seen-set fails;
  `DEFECT L6 … equal=False`), m03+m04 rc 0 (`PREDICATE R95-C1 pass`). Missing control: a committed count-preserving
  receipt forgery judged rc 1.

- **F4 minor — no committed control forges a host stamp (n10–n12).** L9's HOST_PYTHON/BASH/SED legs are only ever
  exercised as present-and-correct (pos) or absent (D4, D7 and friends). Pristine correctly rejects forged values
  (`DEFECT L9 stamps … python=Python 3.13.0`, rc 1; `receipts/matrix/I-host-python/`), but dropping any single host
  leg passes all committed controls and flips the three fixtures. Missing control: one forged host stamp per leg.

- **F5 minor — L2 is the sole anchor for the UPSTREAM receipt field (n03).** L6 compares observations and three
  stamps (VULNERABLE_BOTTLE_SHA, TOOL_SHA, CASE_TABLE_SHA), not UPSTREAM_BOTTLE_SHA. Pristine catches a forged
  header (`DEFECT L2 capture/receipt sha mismatch`, rc 1); n03 rc 0. Missing control: a forged UPSTREAM header.

- **F6 minor — other members' class lists and the member's own class list are not pinned (n06, n07).** Pristine:
  F-classes-other (chess-best-move classes emptied) → `DEFECT L7 … cells={'file-artifact': 29, …}`, rc 1; n07 rc 0.
  G-member-classes (fix row gains `stdout-inspection`, cells unchanged) → pristine rc 1 on classes, n06 rc 0.
  Missing control: one tampered class list each for another member and for the member itself.

- **F7 minor — fail-open when BASE is absent (m02, D-squash).** A squashed single-commit repo with no BASE history:
  pristine `DEFECT L7 ledger member=executed … set_added=[…all members…]`, rc 1 (fails closed, correct); m02 rc 0.
  Round 94 called this unreachable; it is reachable by any squashed or shallow clone of the lane. Missing control:
  the squashed fixture, judged rc 1.

- **F8 minor — handler exit code uncontrolled (m13).** `--rev deadbeefdeadbeef…` pristine:
  `DEFECT SETUP unresolved-revision deadbeef…`, `PREDICATE R95-C1 could-not-evaluate`, rc 2. m13: `PREDICATE R95-C1 fail`,
  rc 1. The same flip happens on `--work` inside the clone (WORK-INSIDE-LANE). Missing control: an unresolved-rev receipt.

- **F9 minor — `--work`-inside-lane guard uncontrolled (n04).** Pristine on `--lane <clone> --work <clone>/w-…`:
  `DEFECT SETUP --work inside the lane …`, rc 2. n04 runs to completion, rc 0, writing extraction output into the
  clone. Missing control: a work-inside-lane invocation judged rc 2.

- **F10 minor — `--bwrap` injection not honoured by the probe rerun (n13).** With an injected executable that exits 3
  on every call (`--bwrap <scratch>/fake/bwrap-broken`), pristine: `DEFECT L6 rerun rc=1 obs=0 want=15 …`,
  `PREDICATE R95-C1 fail`, rc 1. n13 rc 0, `PREDICATE R95-C1 pass` (the rerun silently used `/usr/bin/bwrap`).
  Missing control: a broken-but-present injected sandbox.

- **P-1 minor (pristine, verdict class: rc 2 → rc 1, no false pass).** A sandbox that exists and is executable but
  fails every call is reported as an **outage-free fail**, not `could-not-evaluate`. The guard only covers the missing
  binary path (`sandbox-red`). Exact command: `python3 plans/round95_c1_replay.py --lane <lane> --rev afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239
  --work <w> --bwrap <exe that exits 3>` → `DEFECT L6 rerun rc=1 obs=0 want=15 equal=False`, `PREDICATE R95-C1 fail`,
  rc 1 (`receipts/matrix/BROKEN-SANDBOX/pristine.txt`). The wave's own docstring says "an unusable sandbox is
  could-not-evaluate (rc 2), never a pass"; this fail is fail-closed, so no false pass, but the classification is
  wrong for an infrastructure outage. Route to R96 as a calibration fix.

- **Info — equivalences (m03a, m03b, m04 alone, m07, n05, n15).** Each is redundant with another leg on the
  forgeries tried: m03a and m03b are caught by L6 line equality (A-dup, M-extra rc 1); n05 is caught by L6 (H rc 1);
  m04 alone is caught by L5 seen-set (A-dup rc 1); m07 is equivalent with the probe's own pin check (L-solve rc 2
  both); n15's rc check is covered by L8 for the honest probe (argued, not demonstrated).

- **Info — operational.** Each counter run extracts the full `git archive` (about 690 MB) into `--work/extract` and
  never removes it. My ~560 counter runs drove the scratch to ~390 GB and `/fast` to 100% (80 MB free) at one point;
  I deleted my own extraction dirs (my scratch now ~12 GB) and `/fast` is at 50%. The C2 census (15 counters) and
  other seats share `/fast`; route to the orchestrator for a `--work` cleanup or a `--keep` flag in R96.

## Equivalence / restoration

- Lane `plans/round95_c1_replay.py` never modified; mutants and fixtures run from scratch only; the lane was used
  read-only (`clone --shared`, `git archive` by the counter from the clone). No `git add/commit/stash/checkout` in the
  lane; fixture repos asserted `git rev-parse --show-toplevel == fixture dir` before every commit with identity
  `fixture <fixture@invalid>`.
- No sysctl touched; no tool installed or upgraded; no fleet-root file written.
- Scratch `/fast/scratch/hyaku/kengaku-r95/MutTesterC1` removed at seat end after receipts were copied.

## Commands to reproduce (scratch paths are not citable; receipts are under `receipts/`)

- Pristine T: `python3 -I -B <clone>/plans/round95_c1_replay.py --lane <clone> --rev afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239 --work <w>`.
- Driver with a mutant: `MUT_COUNTER=<mutant.py> python3 -I -B tools/drv_mutant_hook.py --lane <clone> --base-rev 16dcfed7ef4c9e2ac7d28568d855905a8457b20d --scratch <s> --out <o>`.
- Fixtures: `python3 tools/build_fixtures.py <clone> afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239 <fxdir>`.
- Mutants: `python3 tools/gen_mutants.py <pristine counter> <outdir>` (asserts each anchor occurs exactly once).

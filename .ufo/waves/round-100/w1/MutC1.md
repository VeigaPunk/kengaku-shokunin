# MutC1 — mutation battery of the R100-C1 counter at T

Seat MutC1 (leaf, wave 1, round 100). Lane `kengaku-shokunin`, BASE `7846037`, candidate T
`dbe0cefa607cf57f7f58346fce64bcc127144ca0`. Scope: falsify `plans/round100_c1_replay.py` (the C1
counter) and the T tree it measures, one single-point mutant at a time, in isolated
`git clone --shared` fixtures. No production edit, no task call, no lane write outside this report
and `./MutC1/`.

## Method — fixture construction

Each mutant is built in its own clone under `/fast/scratch/hyaku/kengaku-r100/MutC1/fx/<name>`:

1. `git clone --shared` at **P2 `5220b71d`**, the last commit before F. A fixture built on T would
   carry the lane's own freeze commit, `freeze_commit()` would find two commits that add
   `plans/round-100-claims.md`, return `None`, and L3 would die on a fixture artefact rather than on
   the mutant.
2. Apply the instrument mutation (counter / probe / case table) to the working tree.
3. Write a fixture-only `plans/round-100-claims.md` whose `frozen-instruments` and
   `candidate-bytes` blocks are computed from the bytes the mutant tree will carry — the
   `run_controls.sh` discipline, so L11/L4/L8 and L12's `own_bad` do not trivially kill a counter
   mutant. For the three instrument mutants that target L4/L8/L11 the frozen row instead holds T's
   sha, so the leg under test is the only thing that can catch the byte change.
4. Commit `fixture freeze` → **F**.
5. `git read-tree -u --reset T` (tree = T, HEAD still F), restore the fixture claims file, re-apply
   the instrument mutation, write the mutated candidate/receipt bytes, commit `mutant` → **rev**.
6. Run `python3 plans/round100_c1_replay.py --lane . --rev HEAD --work … --grader-venv G` from the
   fixture root (the counter refuses any other cwd).

Two fixture adaptations, both outside the predicate's subject:

- the fixture receipt carries `LANE_TIP <fixture F>`; the lane's receipt names the lane's F
  (`54df15ca`), which no fixture can reproduce. L6 compares the observation block and
  TOOL_SHA/CASE_TABLE_SHA/GRADER_SIDE only, so the rewrite is invisible to every leg except L3 —
  the leg that exists to bind the receipt to F.
- the fixture claims file is the same two-block table `run_controls.sh` writes; the lane's claims
  file is never read.

Every run records `defect_present`: the sha of each touched instrument at rev vs at T, plus the
F..rev path set against the baseline set. All 47 mutants show `defect_present = yes`; the baseline
shows `no`. Every fixture is detached at T with `git rev-parse --show-toplevel` asserted equal to
the fixture directory before any write.

## Baseline (the only admissible positive)

`P00_positive` (no mutation) prints

```
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass L10=pass L11=pass L12=pass L13=pass
TARGET executed_rows=44 member=financial-document-processor cells=crypto-credential:5,file-artifact:35 set_equals_base_plus_member=1 located=1 executed=1 cases=15 legs=120 mismatches=0 new_rows=8 new_rows_flagged=0 new_rows_line_live=0 changed_outside_table=0 defects=0
PREDICATE R100-C1 pass
```

byte-for-byte the frozen TARGET line of `plans/round-100-claims.md`, rc 0. A baseline failure would
make every kill inconclusive; there is none.

## Results

47 single-point mutants (25 counter, 22 tree) plus the baseline: **27 killed, 19 survived,
1 inconclusive**. The battery ran twice; the 47 specs common to both runs agree on
LEGS/TARGET/PREDICATE except two specs that were changed between runs (see
`MutC1/run1-vs-run2.txt`). Every tree-only forgery (T01–T21) is killed, most by exactly the leg the
claim names as its guard.

| mutant | mutation | verdict | failing legs |
|---|---|---|---|
| M01_L1_true | L1 `receipt_bytes is not None` -> `True`; receipt deleted | KILLED | 2,3,5,6,9 |
| M02_L2_true | L2 `l2 = (all(sha(...PINS...` -> `l2 = True or (...)`; receipt SUBJECT_SHA=0 | SURVIVED | — |
| M03_L3_true | L3 `tip == fcommit` -> `True`; receipt LANE_TIP=BASE | SURVIVED | — |
| M04_L3_weak | L3 `tip == fcommit` -> `bool(tip)`; receipt LANE_TIP=BASE | SURVIVED | — |
| M05_L4_true | L4 `sha(table) == frozen[TABLE]` -> `True`; case table + stray key (receipt not re-stamped) | KILLED | 6,9 |
| M05b_L4_true_stamped | same L4 mutant; table + stray key; receipt CASE_TABLE_SHA re-stamped | SURVIVED | — |
| M06_L5_drop_frozen | L5 `obs != pred or pred != predicted[cid]` -> `obs != pred`; receipt C01 predicted+observed flipped together | KILLED | 6 |
| M07_L6_obs_true | L6 `rerun_obs == receipt['obs']` dropped; receipt DETAIL C03 summary forged | SURVIVED | — |
| M08_L6_stamps_true | L6 `stamps_equal` -> `True`; receipt TOOL_SHA=0 | KILLED | 9 |
| M09_L7_set_weak | L7 set equality (rev_set vs base_set + member) dropped; extra executed member | SURVIVED | — |
| M10_L7_legacy_true | L7 `legacy_ok` -> `True`; member `receipt` field changed | SURVIVED | — |
| M11_L7_classes_true | L7 `classes == MEMBER_CLASSES` -> `True`; classes drop file-artifact | SURVIVED | — |
| M12_L7_round_true | L7 `round == 100` -> `True`; member round=99 | SURVIVED | — |
| M13_L8_true | L8 -> `True`; probe + comment; receipt TOOL_SHA re-stamped | SURVIVED | — |
| M14_L9_hostbash_true | L9 HOST_BASH conjunct -> `True`; receipt HOST_BASH forged | SURVIVED | — |
| M15_L10_ge | L10 `== NEW_ROWS` -> `>= NEW_ROWS`; S350 duplicate of S348 | SURVIVED | — |
| M15b_L10_ge_noflag | L10 `== NEW_ROWS and not flagged` -> `>= NEW_ROWS`; S350 duplicate | SURVIVED | — |
| M16_L10_flag_dropped | L10 `and not flagged` dropped; S342 URL basename edited | SURVIVED | — |
| M17_L11_true | L11 -> `True`; counter + comment (frozen table holds T's counter sha) | SURVIVED | — |
| M18_L12_outside_dropped | L12 `not outside_table` dropped; extra file corpus/knowledge/zz-extra.md | SURVIVED | — |
| M19_L12_own_dropped | L12 `not own_bad` dropped; SKILL cell 35->36 (frozen table holds T's SKILL sha) | SURVIVED | — |
| M20_L13_true | L13 -> `True`; S343 `(2 words)` -> `(3 words)` | SURVIVED | — |
| M21_TARGET_exec_total | TARGET `exec_total` drops the status filter (counts all 88 members) | SURVIVED | — |
| M22_parser_obs_eq_pred | parser `observed` -> `predicted`; receipt C01 observed flipped | KILLED | 6 |
| M23_parser_fields_lower | parser `fields[key] = value.strip()` -> `.lower()` | KILLED | 9 |
| T01_receipt_lanetip | receipt LANE_TIP=BASE | KILLED | 3 |
| T02_receipt_detail | receipt DETAIL C03 summary forged | KILLED | 6 |
| T03_receipt_toolsha | receipt TOOL_SHA=0 | KILLED | 6,9 |
| T04_receipt_hostbash | receipt HOST_BASH forged | KILLED | 9 |
| T05_receipt_tablesha | receipt CASE_TABLE_SHA=0 | KILLED | 6,9 |
| T06_receipt_drop_case | receipt C15 CASE+DETAIL deleted | KILLED | 5,6 |
| T07_receipt_flip_case | receipt C01 observed flipped | KILLED | 5,6 |
| T08_receipt_absent | receipt deleted | KILLED | 1,2,3,5,6,9 |
| T09_ledger_extra_member | ledger: winning-avg-corewars -> executed | KILLED | 7 |
| T10_ledger_status | ledger: member status=pending | KILLED | 7 |
| T11_ledger_classes | ledger: member classes drop file-artifact | KILLED | 7 |
| T12_ledger_legacy | ledger: member verdict=reward | KILLED | 7 |
| T13_sources_extra_row | SOURCES: S348 duplicated as S350 | KILLED | 10 |
| T14_sources_typed_words | SOURCES: S343 (2 words) -> (3 words) | KILLED | 13 |
| T15_sources_drop_row | SOURCES: S349 deleted | KILLED | 10 |
| T16_sources_url_edit | SOURCES: S342 URL basename edited | KILLED | 10 |
| T17_skill_cell | SKILL: executed 35 of 76 -> 36 (frozen table holds T's SKILL sha) | KILLED | 12 |
| T18_extra_file | extra file corpus/knowledge/zz-extra.md | KILLED | 12 |
| T19_probe_comment | probe + comment (frozen table holds T's probe sha); receipt TOOL_SHA re-stamped | KILLED | 8 |
| T20_table_stray_key | case table + stray key (frozen table holds T's table sha) | KILLED | 4,6,9 |
| T21_counter_comment | counter + comment (frozen table holds T's counter sha) | KILLED | 11 |
| T22_capture_edit | capture test.sh + comment | INCONCLUSIVE | — |

## Survivors and one-line repairs

A survivor means: with the named leg weakened, the paired defect passes **every other leg**. It is
a statement about single-guarding, not a claim that the production counter is wrong — the production
legs are intact. Repairs are what would make the defect doubly guarded.

- **M02** (L2 receipt-digest conjuncts dropped; receipt `SUBJECT_SHA=0`) — restore the five
  receipt-field conjuncts; the probe rerun never reads the receipt, so nothing else binds
  CAPTURE/FIXTURE/SUBJECT/SOLVE/TEST_SH digests.
- **M03 / M04** (L3 true / weakened; receipt `LANE_TIP=BASE`) — L3 is the only leg that reads
  LANE_TIP; add LANE_TIP to a second leg (L12 can compare it to `fcommit`) or accept single-guarding.
- **M05b** (L4 true; case table + stray key; receipt re-stamped) — L4 is the only leg that reads the
  frozen case-table sha; a regenerated receipt re-stamps L6/L9, so keep L4.
- **M07** (L6 obs equality dropped; forged `DETAIL C03 … summary=0000…`) — L6 is the only guard for
  DETAIL lines (L5 parses CASE only); extend L5's parse to DETAIL, or keep L6.
- **M09** (L7 set equality dropped; extra executed member) — L7's set equality is the only guard;
  the TARGET line moves to `executed_rows=45`, `cells=…:6,…:36` and is not asserted (F1).
- **M10** (L7 `legacy_ok` true; member `receipt` field changed) — `legacy_ok` is the sole guard for
  receipt/subject/verdict.
- **M11** (L7 classes check true; classes drop file-artifact) — the classes check is the sole guard;
  TARGET prints `file-artifact:34` and is not asserted (F1).
- **M12** (L7 round check true; round=99) — the round check is the sole guard.
- **M13** (L8 true; probe + comment; receipt re-stamped) — L8 is the sole guard for probe bytes once
  the receipt is regenerated.
- **M14** (L9 HOST_BASH conjunct true; forged HOST_BASH) — HOST_BASH is not in `RERUN_STAMPS`; add it
  there (the probe stamps it from the same host, so the rerun would catch it).
- **M15 / M15b** (L10 count `>=`; S350 duplicate row) — the exact count is the sole guard; the gate
  prints no DEFECT for a duplicated row (`gate-flagged=-`).
- **M16** (L10 `not flagged` dropped; S342 URL edited) — the flag clause is the sole guard; the line
  gate does not see a URL edit (`new_rows_line_live=0`).
- **M17** (L11 true; counter + comment) — L11 is the sole guard for the counter's own bytes.
- **M18** (L12 `not outside_table` dropped; extra file) — the outside-table clause is the sole guard
  for an extra file (`changed_outside_table=1`, predicate pass).
- **M19** (L12 `not own_bad` dropped; SKILL cell 35→36) — the own-bytes clause is the sole guard for
  a candidate file drifting from the table.
- **M20** (L13 true; S343 `(2 words)`→`(3 words)`) — L13 is the sole guard for the line gate on new
  rows (`new_rows_line_live=1`).
- **M21** (TARGET `exec_total` counts all 88 members) — TARGET is printed, never asserted: the
  counter prints `executed_rows=88` and `PREDICATE pass`.

## Findings (routed to round 101; nothing repaired in round)

**F1 — the TARGET line is printed, never asserted.** M21 prints `executed_rows=88`; M09 prints
`executed_rows=45 cells=…:6,…:36`; M11 prints `cells=…:34` — all with `PREDICATE R100-C1 pass`,
rc 0. The counter's exit status is insensitive to every field of its own TARGET line. The claim's
frozen predicate names the TARGET line, so the claim is falsifiable only at the text level: a
verifier that checks `rc`/`PREDICATE` alone accepts a wrong count or cell. Repair: assert the TARGET
fields in the counter, or make the verifier diff the printed line.

**F2 — L3 is the sole binding of the receipt to F.** M03/M04 survive: `RERUN_STAMPS` is
`TOOL_SHA, CASE_TABLE_SHA, GRADER_SIDE`, so L6 never compares LANE_TIP and no other leg reads it.

**F3 — L2's receipt half is a sole guard and its capture half has no isolating falsifier.** M02
survives with a forged `SUBJECT_SHA`. T22 is inconclusive: editing a capture byte makes the probe
rerun exit 2 (`DEFECT SETUP capture sha mismatch …/test.sh`), so the counter returns
could-not-evaluate before L2 can be exercised in isolation. The capture-pin conjuncts are therefore
only ever observed true at T; a capture edit is reported as could-not-evaluate, never as a leg
failure (could-not-evaluate is not a pass, so the claim is not falsely confirmed).

**F4 — L6's observation equality is the only guard for DETAIL lines.** M07 survives a forged
`DETAIL C03 … summary=0000000000000000` when the comparison is dropped; L5 parses CASE lines only,
and the other legs never read DETAIL.

**F5 — L7's four conjuncts are each sole guards.** M09 (set equality), M10 (legacy fields), M11
(classes), M12 (round). None has a backstop; the class cells and the executed count surface only in
TARGET (F1).

**F6 — L10's count and flag clauses are sole guards; the digest gate does not flag a duplicated
row.** M15/M15b survive with 9 rows under `>=`; T13 shows `gate-flagged=-` for a duplicated S350, so
the exact count is what catches a duplicate. M16 survives with `new_rows_flagged=1` when the flag
clause is dropped; T16 shows the gate does flag an edited URL (S342) and T14 shows the line gate
catches typed words (S343) but not a URL edit.

**F7 — L4/L8/L11 are sole guards for instrument bytes once the receipt is regenerated; L12's two
clauses are sole guards for the file set.** M05b (table + re-stamped receipt), M13 (probe +
re-stamped receipt), M17 (counter), M18 (extra file), M19 (SKILL drift). The receipt stamp (L6/L9)
catches a stale receipt, not a regenerated one.

**F8 — L13 is the sole guard for the line gate on new rows.** M20 survives with
`new_rows_line_live=1`.

**F9 — L9's HOST_BASH conjunct is outside `RERUN_STAMPS`.** M14 survives a forged HOST_BASH; L6
cannot see it because the stamp list omits it.

**F10 — the counter is sensitive to its own parser formatting.** M23 (lowercase field values) is
killed by L9 on `HOST_BASH` case alone: a receipt whose field values are case-normalised would fail
the predicate even though no measured quantity changed.

## Killed — leg attribution

Every tree-only forgery is killed, and by the leg the claim names: T01 L3; T02 L6; T03 L6+L9; T04
L9; T05 L6+L9; T06 L5+L6; T07 L5+L6; T08 L1+L2+L3+L5+L6+L9; T09–T12 L7; T13 L10; T14 L13; T15 L10;
T16 L10; T17 L12; T18 L12; T19 L8; T20 L4+L6+L9; T21 L11. Counter mutants killed: M01 by L2/L3/L5/L6/L9
(L1 is redundant), M05 by L6+L9 (the stale receipt stamp, not L4), M06 by L6, M08 by L9, M22 by L6,
M23 by L9.

## Receipts

`MutC1/` holds one `<mutant>.txt` per run (freeze commit, rev, F..rev tree diff, instrument sha
proof, `defect_present`, expected leg, rc, and the counter's full stdout), `summary.tsv` (the table
above), `run1-vs-run2.txt` (determinism check) and `mut.py` (the driver; 47 specs, one clone each).

## Reproduction

```
mkdir -p /fast/scratch/hyaku/kengaku-r100/MutC1 && cd /fast/scratch/hyaku/kengaku-r100/MutC1
uv venv -p 3.13 G && uv pip install --python G/bin/python pytest==8.4.1 pandas==2.3.2 pytest-json-ctrf==0.3.5
python3 mut.py --jobs 6 --out results.json          # ~4 min, 48 fixtures
```

Tooling: no install or upgrade was needed; the venv is python 3.13.16 / pytest 8.4.1 / pandas 2.3.2
/ pytest-json-ctrf 0.3.5 (numpy 2.5.4), the sandbox is the host `/usr/bin/bwrap`, and the probe
runs with no network.

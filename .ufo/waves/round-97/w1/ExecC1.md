# ExecC1 — independent C1 replay + C2 calibration exercise (round 97, wave 1)

Seat: ExecC1 (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Revisions: BASE `4992cd0e32b8db23ca20310deb7de12d485f8bcc`, P0 `5b41c1c3`, P1 `b2352135`,
P2 `e40fd0c2`, freeze F `8d9d271306c4e7e2d586e51cd546652249d286cb`, measured T
`f1083da60e7ff6b88f7420aae7424f7762d14700` (lane HEAD at start and end of this seat; working
tree clean apart from the wave's own untracked `.ufo/waves/round-97/` files).

No production edits, no commits/pushes/jj writes in the lane, no `task` calls, no host sysctl or
service mutation, no pacman transaction. All writes are this report, this evidence directory, and
scratch `/fast/scratch/hyaku/kengaku-r97/ExecC1` (removed after copying receipts).

Every measurement ran in an isolated `git clone --shared` detached at T (clean tree), never in the
lane working tree. At the end of the seat the lane working tree showed sibling-seat edits
(`LOG.md`, `corpus/QUALITY.md`, `corpus/README.md` modified; `corpus/knowledge/tb2-sparql-university-grader.md`,
`corpus/lessons/round-97.md` new). None are mine and none affect the numbers below; HEAD was still
T throughout.

## Verdict

| Claim | Verdict | Basis |
|---|---|---|
| R97-C1 coverage | **pass as measured** | replay at T prints the frozen `LEGS`/`TARGET`/`PREDICATE` lines verbatim, rc 0; fails at BASE (rc 1) and on two independent forgeries |
| R97-C2 calibration | **pass as measured** | census at T prints the frozen lines, rc 0; at BASE 44 mismatches rc 1; only 44 `kind` cells differ, all 44 entry scripts byte-identical, 84/84 gate rows carry a self-test spelling |

I found no defect in either frozen instrument and no unmet clause I could measure. Everything below
is my own execution of the frozen bytes at T and BASE, plus structural checks with my own parser.

## Environment (measured)

- Driver: `python3` 3.14.8 (`/usr/bin/python3`), `uv` 0.13.0, `bubblewrap` 0.13.1 (`/usr/bin/bwrap`),
  host `bash` 5.3.20(1)-release, `max_user_namespaces` > 0 (count 122865).
- Grader venv `G` staged exactly as the claims prescribe:
  `uv venv -p 3.13 G && uv pip install --python G/bin/python rdflib==7.1.4 pytest==8.4.1`
  → CPython 3.13.16, rdflib 7.1.4, pytest 8.4.1, pyparsing 3.3.3 (unpinned, resolved).
- Tool installs: **none**. No pacman/uv-tool/release-binary install or upgrade was needed; the venv
  packages above are fixture dependencies inside my scratch, not host tooling.

## 1. Frozen instruments and candidate bytes at T

All 10 rows of the `frozen-instruments` table and all 3 rows of the `candidate-bytes` table hash
exactly as the claims file states at T (sha256 of the whole file, `git show T:<path>` and the
working tree agree). No frozen file changed after F.

## 2. R97-C1 — replay at T

Command (from the clone root, cwd asserted by the counter):

```
cd /fast/scratch/hyaku/kengaku-r97/ExecC1/lane-T   # --shared clone, detached at T
TMPDIR=/fast/scratch/hyaku/kengaku-r97/ExecC1/tmp \
python3 plans/round97_c1_replay.py --lane . --rev f1083da60e7ff6b88f7420aae7424f7762d14700 \
  --work /fast/scratch/hyaku/kengaku-r97/ExecC1/rerun-T \
  --grader-venv /fast/scratch/hyaku/kengaku-r97/ExecC1/G
```

Output, rc 0, wall 22 s (`replay-T.txt`, `replay-T.time.txt`):

```
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass
TARGET executed_rows=41 member=sparql-university cells=file-artifact:32 set_contains_base=1 located=1 executed=1 cases=18 legs=72 mismatches=0 defects=0
PREDICATE R97-C1 pass
```

Line-for-line the frozen predicate. L6 re-ran the probe from a `git archive` of T and reproduced
the committed receipt's 36-line observation block with equal `TOOL_SHA` / `CASE_TABLE_SHA` /
`GRADER_SIDE` stamps.

## 3. R97-C1 — replay at BASE (negative)

Same command with `--rev 4992cd0e…` (`replay-BASE.txt`), rc 1:

```
LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=fail L8=fail L9=fail
TARGET executed_rows=40 member=sparql-university cells=file-artifact:31 set_contains_base=0 located=0 executed=0 cases=0 legs=0 mismatches=0 defects=9
DEFECT L1 receipt absent at revision: corpus/evidence/round97/sparql-probe.txt
DEFECT L2 capture/receipt sha mismatch (cap=absent receipt=absent)
DEFECT L3 LANE_TIP absent not an ancestor of 4992cd0e32b8
DEFECT L4 case table absent vs frozen absent
DEFECT L5 case coverage 0 of 0
DEFECT L6 probe absent at revision: plans/round97_sparql_probe.py
DEFECT L7 ledger member=unexecuted round=None executed_total=40 cells={'file-artifact': 31} legacy_fields=False set_added=[] set_removed=[]
DEFECT L8 probe absent vs frozen absent
DEFECT L9 stamps tool=absent table=absent bash=None
PREDICATE R97-C1 fail
```

The counter is not trivially green: at BASE every leg fails and the executed totals read 40 / 31.

**Wrong-cwd guard** (`wrongcwd.txt`): run from a non-lane cwd → rc 2,
`DEFECT SETUP cwd … is not the lane root …`, `PREDICATE R97-C1 could-not-evaluate`. The refusal
works and does not print `pass`.

## 4. Captured probe run twice — determinism and stamps

Two direct runs of the captured probe at T, separate work dirs (`probe-run1.txt`, `probe-run2.txt`):

- Full outputs are **byte-identical** (both sha256 `b320e50b…`), not merely observation-equal.
- Observation blocks identical to each other and to the committed receipt
  `corpus/evidence/round97/sparql-probe.txt`.
- Pinned stamps identical across run 1, run 2 and the receipt:
  `SUBJECT_SHA ecf15840…`, `TEST_SH_SHA 45902b57…`, `TEST_GRAPH_SHA 368ce01d…`,
  `SOLVE_SHA d17995a8…`, `TOOL_SHA 13a4564d…`, `CASE_TABLE_SHA 7b846270…`,
  `GRADER_SIDE python,rdflib,pytest 3.13 7.1.4 8.4.1`.
- Only expected difference from the receipt: `LANE_TIP` is T in my runs and F in the receipt
  (the receipt was generated at F). L3 checks ancestry, not equality, and passes; `LANE_TIP` is
  deliberately outside the replay's `RERUN_STAMPS`.
- `GRADER_UNPINNED python,pyparsing 3.13.16 3.3.3` also reproduced, though L6 does not compare it
  by design (round-96 W-2).

## 5. Reward leg is real pytest, not a derived bit

The harness in the frozen probe runs
`python -I -B -m pytest -q -p no:cacheprovider /tests/test_outputs.py` and takes reward 1 iff that
subprocess exits 0. I measured pytest's own exit code for **all 18 cases** in my own bwrap staging
(`indep_reward18.py`, `indep-reward18.txt`): `pytest_rc` 0 ⇔ receipt reward 1, non-zero ⇔ 0,
`reward_mismatches=0`. Sample with pytest's own summary line (`indep-reward.txt`):

| case | pytest rc | summary | reward |
|---|---|---|---|
| C01 solve | 0 | `3 passed` | 1 |
| C07 no-graduation-filter | 1 | `1 failed, 2 passed` | 0 |
| C11 duplicate-rows | 0 | `3 passed` | 1 |
| C12 extra-column | 0 | `3 passed` | 1 |
| C13 semicolon-separator | 1 | `1 failed, 2 passed` | 0 |

pytest collects and executes the three captured test functions in every case, so the reward leg is
a real pytest verdict over the captured `test_outputs.py`.

## 6. C11 / C12 shapes (the located grading gaps)

- **C11 duplicate-rows**: `rows=8 distinct=4`, names the four reference professors, reward 1.
  Independently re-derived with my own rdflib query (`indep-reward.txt` `SHAPE C11
  vars=professorName+countries rows=8 distinct=4`). The grader's `test_sparql_query_results`
  compares `set(...)`, so duplicate rows collapse and pass.
- **C12 extra-column**: `vars=professorName+countries+n`, `rows=4 distinct=4`, reward 1.
  Independently re-derived (`SHAPE C12 vars=professorName+countries+n rows=4 distinct=4`). The
  grader reads `row.professorName` / `row.countries` by attribute, so an extra projected `?n`
  column is ignored.
- The hidden-graph claim is confirmed by the captured bytes: `DATA_PATH =
  Path("/tests/university_graph_test.ttl")`, never the agent's `/app/university_graph.ttl`.
  C17 (`agent-graph-literal`) fails with names `Aristotle_Tympas|Orfeas_Menis|Pepe_Attanasio`,
  which differ from the reference set.

## 7. Ledger flip (independent count)

Own parse of `plans/grader-population-ledger.json` at BASE and T (`indep-structure.txt`):

```
BASE members=88 executed=40 file-artifact=31
T    members=88 executed=41 file-artifact=32
set_added=['sparql-university'] set_removed=[]
```

The member at T carries `status=executed`, `round=97`, `classes=["file-artifact"]`,
`receipt=corpus/evidence/round97/sparql-probe.txt`, `subject=tb2-header`, `verdict=cases`. The
SKILL class cell reads `executed 32 of 76 (round 97 adds sparql-university; …)` at T vs
`executed 31 of 76` at BASE.

## 8. C landing surface (F → T)

`git diff --name-status F T` is exactly four paths, matching the kill rule:

```
M  SKILL.md
M  corpus/SOURCES.md
A  corpus/evidence/round97/sparql-probe.txt
M  plans/grader-population-ledger.json
```

i.e. the three candidate-bytes files plus the one named receipt path, nothing else. No file was
deleted anywhere in BASE→T, and under `plans/` only five files were added (claims, cases, replay,
census, probe) — no pre-existing script was modified.

SOURCES S317–S325 are present: S317–S322 tier A admitted, S323–S325 `rejected` with flips.

## 9. R97-C2 — census at T and BASE

At T (`census-T.txt`), rc 0:

```
ROWS base=168 rev=171 removed=0 duplicate=0 cells_changed=0
GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0 scripts_changed=0
MISMATCH_TOTAL n=0
PREDICATE R97-C2 pass
```

At BASE (`census-BASE.txt`), rc 1: `GATES total=127 with_selftest=83 without=44`,
`MISMATCH_TOTAL n=44`, 44 `MISMATCH` lines, `PREDICATE R97-C2 fail`. The 44-name list is
**set-identical** to the L1 BEFORE receipt `.ufo/waves/round-97/L1/c2-base.txt`
(`m-base.txt` and `m-l1.txt` are the same file, sha256 `cecc313d…`).

**Gate self-test** of the new census row (`census-selftest.txt`): `SELFTEST cases=8 failed=0`, rc 0
(base-red, retype-green, row-removed, demoted, cell-changed, script-forged, prose-only, duplicate).

## 10. C2 calibration is exact (own parser, `indep-structure.txt`)

- Registry rows: base 168 → rev 171, removed 0, added exactly the three round-97 rows
  (`round97-c1-replay` probe, `round97-sparql-probe` probe, `round97-gate-selftest-census` gate).
- `kind_changes=44`, `other_cell_changes=0`; every transition is `gate → probe`; histogram
  gate 127→84, probe 41→87.
- The 44 re-typed rows' entry scripts are **byte-identical at BASE and T** (`identical=44
  differ=[] unresolved=[]`) — "no old script" holds.
- The set of rows demoted at T equals the set of BASE mismatches exactly (no over-correction, no
  under-correction).
- All 84 gate rows at T have an existing entry script that mentions a self-test spelling
  (`gate_rows=84 script_absent=[] no_self_test_mention=[]`, coarse independent detector; the exact
  detector remains the frozen instrument).

## 11. Falsification (my own fixtures, `git -C` with toplevel asserted)

| Forgery | Fixture HEAD | Result |
|---|---|---|
| receipt: C11 `observed=P,P,P,1` → `P,P,P,0` | `999562d7…` | rc 1, `L5=fail L6=fail`, `DEFECT L5 case C11 …`, `DEFECT L6 rerun … equal=False` (`fx-receipt.txt`) |
| ledger: `sparql-university` → `unexecuted` | `50cec174…` | rc 1, `L7=fail`, `DEFECT L7 ledger member=unexecuted … executed_total=40` (`fx-ledger.txt`) |
| registry: all 84 gate rows re-typed `probe` | `2368186b…` | rc 1, `GATES total=0 … demoted_with_selftest=83`, 83 `DEMOTED` lines, `PREDICATE R97-C2 fail` (`fx-blanket.txt`) |

The 83 (not 84) in the blanket control is correct: the 84th gate row is new at T and has no BASE
row to compare against, so it cannot be "demoted".

## 12. Risks / notes (not defects)

1. **L6 is host-dependent**: it needs `bwrap` and user namespaces. Both were present; a host
   without them yields `could-not-evaluate` (rc 2), not a pass. Measured, not inferred.
2. **`GRADER_UNPINNED` is not compared** by L6 (round-96 W-2). My venv happened to resolve the
   same CPython micro and pyparsing (3.13.16 / 3.3.3) as the receipt, so this is a non-issue here,
   but the leg genuinely does not test it.
3. **Receipt `LANE_TIP` is F, not T.** L3 tests ancestry only; a reader expecting equality would
   misread it. The claims describe L3 as ancestry, so this is consistent.
4. **C11/C12 passing is a property of the captured grader**, not a lane defect: the claims report
   them as located grading gaps, and the probe correctly records them as passes.
5. **Independent detector strength**: my gate scan in §10 is coarse (any `self-test` mention). The
   authoritative detector is the frozen census; my check only corroborates that no gate row points
   at a script with no self-test mention at all.
6. The replay's L6 re-runs the probe with the *replay's* interpreter (`sys.executable`), so the
   driver python (3.14.8 here) must be able to run the stdlib-only probe. It can; the grader side
   always runs under the injected venv.

## 13. Exact commands and exit codes

All from `/fast/scratch/hyaku/kengaku-r97/ExecC1` unless noted; `TMPDIR` set explicitly to
`/fast/scratch/hyaku/kengaku-r97/ExecC1/tmp` for every run.

| # | command | rc |
|---|---|---|
| 1 | `uv venv -p 3.13 G` | 0 |
| 2 | `uv pip install --python G/bin/python rdflib==7.1.4 pytest==8.4.1` | 0 |
| 3 | `cd lane-T && python3 plans/round97_c1_replay.py --lane . --rev f1083da6… --work …/rerun-T --grader-venv …/G` | 0 |
| 4 | `cd lane-T && python3 plans/round97_c1_replay.py --lane . --rev 4992cd0e… --work …/rerun-BASE --grader-venv …/G` | 1 |
| 5 | `cd lane-T && python3 plans/round97_sparql_probe.py --lane . --work …/probe-run1 --grader-venv …/G` | 0 |
| 6 | `cd lane-T && python3 plans/round97_sparql_probe.py --lane . --work …/probe-run2 --grader-venv …/G` | 0 |
| 7 | `cd lane-T && python3 plans/round97_gate_selftest_census.py --lane . --rev f1083da6…` | 0 |
| 8 | `cd lane-T && python3 plans/round97_gate_selftest_census.py --lane . --rev 4992cd0e…` | 1 |
| 9 | `cd lane-T && python3 plans/round97_gate_selftest_census.py --selftest --work …/census-selftest` | 0 |
| 10 | `python3 indep/indep_structure.py lane-T` | 0 |
| 11 | `python3 indep/indep_reward.py lane-T G indep/work` | 0 |
| 12 | `python3 indep/indep_reward18.py lane-T G indep/work18` | 0 |
| 13 | `cd fx-receipt && python3 plans/round97_c1_replay.py --lane . --rev 999562d7… --work … --grader-venv …/G` | 1 |
| 14 | `cd fx-ledger && python3 plans/round97_c1_replay.py --lane . --rev 50cec174… --work … --grader-venv …/G` | 1 |
| 15 | `cd fx-blanket && python3 plans/round97_gate_selftest_census.py --lane . --rev 2368186b…` | 1 |
| 16 | `cd wrongcwd && python3 …/lane-T/plans/round97_c1_replay.py --lane …/lane-T --rev f1083da6… --work … --grader-venv …/G` | 2 |

## Evidence

`.ufo/waves/round-97/w1/ExecC1/` — `SHA256SUMS` plus:
`tabled-hashes.txt` (all 13 tabled rows re-hashed at T from the claims file itself),
`replay-T.txt`, `replay-T.time.txt`, `replay-BASE.txt`, `wrongcwd.txt`,
`probe-run1.txt`, `probe-run2.txt`, `census-T.txt`, `census-BASE.txt`, `census-selftest.txt`,
`m-base.txt`, `m-l1.txt`, `fx-receipt.txt`, `fx-ledger.txt`, `fx-blanket.txt`,
`indep-structure.txt`, `indep-reward.txt`, `indep-reward18.txt`,
and the three check scripts `indep_structure.py`, `indep_reward.py`, `indep_reward18.py`.

Scratch `/fast/scratch/hyaku/kengaku-r97/ExecC1` removed after the copy.

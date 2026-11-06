# ExecHarm — round 97 independent harm and scope check

Seat: ExecHarm (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
BASE `4992cd0e32b8db23ca20310deb7de12d485f8bcc`; F `8d9d271306c4e7e2d586e51cd546652249d286cb`;
T `f1083da60e7ff6b88f7420aae7424f7762d14700`. Scratch root `/fast/scratch/hyaku/kengaku-r97/ExecHarm`
(two `--shared` clones: `laneT` detached at T, `laneB` detached at BASE; venv `G` = CPython 3.13.16,
rdflib 7.1.4, pytest 8.4.1). No production edit, no git/jj mutation in lane/fleet/siblings; every
fixture write used explicit `git -C <fixture>`; `rev-parse --show-toplevel` was checked before
writing on f1–f5 and after the fact on f6–f8 — all eight resolve to their own fixture directory.
During the wave another seat modified three tracked lane files in the working tree (`LOG.md`,
`corpus/QUALITY.md`, `corpus/README.md`); I did not write them, and every check below reads committed
revisions through `git show`/`git archive`, so they do not affect any result. Lane HEAD stayed T.

**Verdict: both frozen predicates pass at T exactly as claimed, C's scope is exactly the four declared
paths, every frozen file is intact, and no pre-existing gate's verdict or defect line moved. One
counter-coverage gap (three receipt lines), one detector limitation, one wording note and one scope
observation are recorded below for routing; none makes a round-97 claim not met.**

---

## 1. Scope — what C landed, and nothing else

`git diff --name-status F T` returns exactly four paths:

```
M  SKILL.md
M  corpus/SOURCES.md
A  corpus/evidence/round97/sparql-probe.txt
M  plans/grader-population-ledger.json
```

That is the three candidate-bytes files plus the one named receipt. `git diff --name-status BASE T`
shows those three as the **only** modifications in the whole round; every other path is an addition
(round-97 instruments, captures, claims, controls, evidence). No closed-round script or document is
modified anywhere in BASE..T.

Candidate bytes at T hash to the F table exactly:

```
739fb58bdfedc000fe8d2cf237e5603f87b621cdf2da6e01bd773d4c1a7b3df6  SKILL.md
567a26bbe05bee1710eee235ae97a885433104aa0dec8e9ebb6a68e13e6919db  plans/grader-population-ledger.json
c54a0ecea33fb1fc31314bc928077e0860502548be8544d216e6108511d0ce04  corpus/SOURCES.md
```

All ten frozen instruments hash to the frozen table **at F** (computed with `git show F:<path>`), so
nothing changed between F and T either:

```
13a4564d…  plans/round97_sparql_probe.py            7b846270…  plans/round97-cases.json
f736b04b…  plans/round97_c1_replay.py               a255e830…  plans/round97_gate_selftest_census.py
ecf15840…  …/tests/test_outputs.py                  45902b57…  …/tests/test.sh
368ce01d…  …/tests/university_graph_test.ttl        d17995a8…  …/solution/solve.sh
dd0abcd6…  …/environment/Dockerfile                 0b0b1f2c…  …/environment/university_graph.ttl
```

Commit shape: `T.parent = F`, `F.parent = P2 e40fd0c2`. Evidence: `ExecHarm/shas.txt`,
`ExecHarm/scope.txt`.

---

## 2. R97-C1 — fifteenth grader replay, independently exercised

**Command (exact):** from `laneT` root,
`python3 plans/round97_c1_replay.py --lane . --rev f1083da6… --work …/rerun --grader-venv …/G`.

**Result rc 0:**

```
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass
TARGET executed_rows=41 member=sparql-university cells=file-artifact:32 set_contains_base=1 located=1 executed=1 cases=18 legs=72 mismatches=0 defects=0
PREDICATE R97-C1 pass
```

This is byte-identical to the lane's untracked `.ufo/waves/round-97/L1/c1-tip.txt`.

**BEFORE control (BASE, rc 1):** all nine legs fail with 9 DEFECT lines (receipt, capture, tip, table,
cases, probe, ledger, probe-hash, stamps all absent at BASE). The predicate is therefore not a
tautology on this tree.

**Independent checks of the claim's content (not just the counter's rc):**

| Claim element | Independent observation |
|---|---|
| 18 cases × 4 legs = 72 | receipt has 18 `CASE` lines; `LEG_ORDER exists,runs,results,reward`; `18*4=72` |
| reward leg is real pytest, not a derived bit | probe harness runs `sys.executable -m pytest -q -p no:cacheprovider /tests/test_outputs.py` and appends `1` iff rc 0 (`round97_sparql_probe.py:160`); `test.sh` writes reward from pytest's exit code |
| grader reads its **own** hidden graph | `test_outputs.py:12 DATA_PATH = Path("/tests/university_graph_test.ttl")`, parsed at :40 and :59; the probe stages the captured test graph at `/tests` and the agent graph at `/app` |
| solve.sh runs unmodified | probe copies `solution/solve.sh`, `--ro-bind`s it, runs `/usr/bin/bash /solve.sh`; all six captures are sha-verified against PINS before the run, mismatch exits 2 |
| 18/18 predictions held | P0 `predictions-mechanism.txt` (blob identical at P0 and T) predicted vectors == frozen case table == receipt `predicted=` == receipt `observed=` for all 18 ids |
| ledger flip | executed member set BASE 40 → T 41, added exactly `sparql-university`, removed none; record `{status:executed, round:97, receipt:corpus/evidence/round97/sparql-probe.txt, subject:tb2-header, verdict:cases, reason:replayed}`; class `file-artifact` 31→32 of 76 |

**Falsifications (each a one-commit fixture clone of T; receipts in `ExecHarm/harm/`):**

| Fixture | Mutation | Counter result |
|---|---|---|
| f1 | receipt `CASE C05 observed P,P,P,1` → `P,P,P,0` | **fail** rc 1: `L5=fail L6=fail`, `DEFECT L5 case C05 …`, `DEFECT L6 rerun … equal=False` |
| f2 | ledger reverted to BASE (no flip) | **fail** rc 1: `L7=fail`, `DEFECT L7 ledger member=unexecuted … executed_total=40` |
| f6 | receipt `mismatches 0` → `mismatches 9` | **pass** rc 0 — line not compared |
| f7 | receipt `SANDBOX clearenv=1 unshare-all=1 etc-bound=0` → inverted | **pass** rc 0 — line not compared |
| f8 | receipt `LANE_TIP` F → P1 (still an ancestor) | **pass** rc 0 — L3 checks ancestry only |

So the measured evidence block cannot be forged (f1), the ledger flip is load-bearing (f2), but
**three receipt lines are outside the counter's comparison**: the `mismatches` summary, `SANDBOX`,
and `LANE_TIP` beyond ancestry. `MEMBER`, `LEG_ORDER`, `GRADER_UNPINNED`, `HOST_USERNS` are likewise
never read (`grep 'fields.get("…")'` finds only SUBJECT/SOLVE/TEST_GRAPH/TEST_SH/LANE_TIP/TOOL_SHA/
CASE_TABLE_SHA/HOST_BASH). The committed receipt's values are truthful (L6 re-derives the block; the
stamps match), so this is a counter-coverage gap for round 98, not a false claim.

**Wording note:** `test.sh` pins four packages (`pytest==8.4.1`, `rdflib==7.1.4`,
`pytest-json-ctrf==0.3.5`). The receipt's `GRADER_SIDE python,rdflib,pytest 3.13 7.1.4 8.4.1` and the
claim's parenthetical carry three; the ctrf plugin is reporting-only (`--ctrf` is not passed in the
reward leg), so reward semantics are unaffected. Low severity, wording only.

---

## 3. R97-C2 — gate-kind calibration, independently exercised

**Command (exact):** from `laneT` root,
`python3 plans/round97_gate_selftest_census.py --lane . --rev f1083da6…`.

**Result rc 0:**

```
ROWS base=168 rev=171 removed=0 duplicate=0 cells_changed=0
GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0 scripts_changed=0
MISMATCH_TOTAL n=0
PREDICATE R97-C2 pass
```

Byte-identical to the lane's untracked `.ufo/waves/round-97/L1/c2-tip.txt`.

**BEFORE control (BASE, rc 1):** `GATES total=127 with_selftest=83 without=44`,
`MISMATCH_TOTAL n=44`, `PREDICATE R97-C2 fail`, and the 44-row list matches the claims' BEFORE
receipt (`c2-base.txt`) exactly (my run differs only by the harness-appended `rc=1` line).

**Independent registry parse (own parser, not the census):** 168 data rows at BASE, 171 at T;
3 rows added (`round97-sparql-probe` probe, `round97-c1-replay` probe,
`round97-gate-selftest-census` gate), 0 removed, **exactly 44 kind changes, all `gate`→`probe`, zero
other cells changed in any surviving row**. Kind census 127 gate / 41 probe → 84 gate / 87 probe
(127−44+1 = 84; 41+44+2 = 87). The 44 changed names are set-equal to the census's 44 MISMATCH names
(no census-only, no changed-only).

**Independent script check:** for each of the 44, the BASE entry script was read at BASE and T: no
script differs BASE→T; none contains a code-level self-test spelling. Seven contain the word
`selftest` only in prose/strings (`round36-c1-battery`, `round41-c1-mutants`, `defect-ledger`,
`round35-hardening`, `round46-c2`, `freeze-integrity`, `round95-c2-counter`) — I confirmed by
argparse inspection that none of those scripts accepts `--selftest`/`--self-test`. On the T side, a
token-level classifier over all 84 `gate` rows finds a **code-level** (not comment/docstring)
spelling in every one — `with_selftest=84` is not a prose artefact.

**Census self-test:** `python3 plans/round97_gate_selftest_census.py --selftest --work …` →
`SELFTEST cases=8 failed=0` (base-red, retype-green, row-removed, demoted, cell-changed,
script-forged, prose-only, duplicate). The new `gate` row is backed.

**Falsifications (fixture clones of T; receipts in `ExecHarm/harm/`):**

| Fixture | Mutation | Counter result |
|---|---|---|
| f3 | blanket: all 84 gate rows retyped `probe` | **fail** rc 1: `GATES total=0 … demoted_with_selftest=83`, 83 `DEMOTED` lines |
| f4 | delete `package-gate` row | **fail** rc 1: `removed=1`, `ROW-REMOVED package-gate` |
| f5 | append `if "--selftest" in sys.argv: pass` to `plans/round36_c1_verify.py` | **fail** rc 1: `scripts_changed=1`, `SCRIPT-CHANGED round36-c1-battery` + `DEMOTED` |

These corroborate the lane's own P2 controls (`c2-blanket`, `c2-delete`, `c2-scriptforge`,
`c2-cellforge`, `c2-do-nothing`, `c2-positive`), whose receipts I read and which show the same
finding ids.

**Residual limitation (routed, not a defect):** the census is a *spelling* proxy, not a
substance check of PROTOCOL §Gate standard (isolated fixtures, exit code + stable finding-id,
committed expected values). Ten of the 44 demoted rows carry fixture selectors
(`--battery`/`--battery-dir`: round37/38/39/40/41/42/43/44-c1, round39-c1-audit; `--skip-mutants`:
round50-c1). I read each row's own self-test cell: they describe external controls, not a
self-invocation mode, and `round39-c1-audit` / `round50-c1` explicitly state no `--selftest` exists
(measured argparse exit 2). The demotions are therefore defensible; the blind spot is that a
differently-spelled real self-test would be demoted and `DEMOTED` would not fire.

---

## 4. Harm — exact findings at BASE vs T (not just rc)

All six instruments are byte-identical at BASE and T (they are not in BASE..T). Same clone layout,
same `--work` isolation; full outputs in `ExecHarm/harm/`.

| Instrument | BASE | T | Diff |
|---|---|---|---|
| `grader.py` | rc 0, `CHECKS n=733 mismatches=0 errata_pinned=1`, `VERDICT: PASS` | identical | **none** |
| `round68_capability_table.py --lane .` | rc 0, `T1..T4 ok n=0`, `MISMATCH n=0`, `PREDICATE R68-A3 pass` | identical | **none** |
| `round73_c2_registry_audit.py --lane .` | rc 0, `INSTRUMENTS total=167 … PARSED 167 failed=0`, D1–D4 ok, `MISMATCH 0`, `DEFECTS n=0`, `PREDICATE R73-C2 pass` | `INSTRUMENTS total=170 … PARSED 170`, D1–D4 ok, `MISMATCH 0`, `DEFECTS n=0`, pass | only the two count lines (+3 rows) |
| `round74_c1_registry.py --lane .` | rc 1, `files=161 plans_seen=132`, `ADVERTISED 172`, `REGISTERED 167 rows=167`, `MISSING 18`, `PREDICATE R52-C2 fail` + `R74-C1 fail` | rc 1, `files=162 plans_seen=134`, `ADVERTISED 174`, `REGISTERED 170 rows=170`, **same 18 MISSING**, same two fail lines | counts only; the 18-name MISSING list is identical. `files/plans_seen/ADVERTISED` move because F adds `plans/round-97-claims.md`, which advertises `round97_c1_replay.py` and `round97_gate_selftest_census.py` (both registered, so no new MISSING) |
| `round74_c2_registry_audit.py --lane .` | rc 1, `INSTRUMENTS 167`, D1–D4 ok, `MALFORMED defect n=1` (`round88-fixgit-probe`, columns=7), `MISMATCH 1`, `DEFECTS n=1`, fail | `INSTRUMENTS 170`, **same MALFORMED line**, `MISMATCH 1`, `DEFECTS n=1`, fail | counts only; the defect line is byte-identical |
| `round79_c1_population_ledger.py --lane . --rev worktree` | rc 1, `LEDGER rows=88 executed=40 unlocated=0 unexecuted=48`, member unexecuted, `CLASS file-artifact k=31`, `COVERAGE replayed=40`, `DEFECT SUBJECT-MISMATCH mteb-retrieve ledger=tb2-result-file receipt=tb2-header`, `DEFECTS n=1`, `TARGET replayed=40`, fail | rc 1, `executed=41 unexecuted=47`, member executed, `k=32`, `COVERAGE replayed=41`, **same SUBJECT-MISMATCH**, `DEFECTS n=1`, `TARGET replayed=41`, fail | only the five ledger-flip lines; the defect line is byte-identical |

Cross-check: my T outputs for grader/r68/r73/r74c2/r79 are line-identical to the lane's committed
pre-freeze candidate-fixture receipts (`controls/harm-pre-freeze/b82b4c75/*`), and my BASE outputs are
line-identical to the P1 receipts (`b2352135/*`) apart from the harness `rc=` line. The only
P1→candidate diffs in those receipts are the row counts and the `file-artifact` k, exactly as the
claims state.

---

## 5. Inherited history harm (not cured, unchanged by this round)

- `round74_c1_registry.py`: **MISSING 18** — round87/90/91/92/93/94/95 instruments with no registry row. Identical at BASE and T; exit 1 both.
- `round74_c2_registry_audit.py`: **MALFORMED-ROW `round88-fixgit-probe` (columns=7)**. Identical at BASE and T; exit 1 both.
- `round79_c1_population_ledger.py`: **SUBJECT-MISMATCH `mteb-retrieve`** (`ledger=tb2-result-file receipt=tb2-header`). Identical at BASE and T; exit 1 both.
- `round74_c1_registry.py` also prints `PREDICATE R52-C2 fail` at both revs.

None of these is introduced or worsened by round 97; none is repaired by it.

---

## 6. Findings and risks (routed, not repaired — instruments are frozen)

1. **R97-C1 counter coverage gap (medium-low).** The receipt's `mismatches` summary, `SANDBOX`,
   `MEMBER`, `LEG_ORDER`, `GRADER_UNPINNED`, `HOST_USERNS` lines are never compared, and `LANE_TIP`
   is checked for ancestry only. Fixtures f6/f7/f8 pass with those lines forged. The measured
   observation block itself is unforgeable (f1 fails). Route to round 98: compare the whole receipt
   except the explicitly exempt `GRADER_UNPINNED`, or pin the receipt sha.
2. **R97-C1 wording (low).** `test.sh` pins `pytest-json-ctrf==0.3.5`; `GRADER_SIDE` and the claim's
   parenthetical carry three pins. Reporting-only plugin; reward semantics unaffected.
3. **R97-C2 detector is a spelling proxy (low).** `with_selftest` means "the script contains one of
   the lane's spellings in code", not "the self-test conforms to the standard". Ten demoted rows have
   `--battery`/`--battery-dir`/`--skip-mutants` selectors that are not self-tests; each row's own
   self-test cell confirms no self-test flag exists. No over-correction observed in fact.
4. **Scope observation (informational).** The pre-freeze harm check compared P1 with the candidate
   fixture, which does not contain F's `plans/round-97-claims.md`. At T that file adds two advertised
   plans targets, so `round74_c1_registry.py`'s `files/plans_seen/ADVERTISED` counts move as well as
   `REGISTERED`. Verdict and defect lines are unchanged, so this is not harm; a future harm receipt
   measured at T should expect those three counts.

**Blockers: none.** Every frozen predicate was independently reproduced; every falsification I ran
was caught except the three receipt-line gaps above, which do not affect either claim's predicate.

---

## 7. Evidence inventory (all under `.ufo/waves/round-97/w1/ExecHarm/`)

```
c1-t.log c1-base.log c2-t.log c2-base.log        exact counter outputs at T and BASE
harm/grader-{B,T}.txt                            grader.py, both revs
harm/r68-{B,T}.txt r73-{B,T}.txt                 capability table, r73 audit
harm/r74c1-{B,T}.txt r74c2-{B,T}.txt r79-{B,T}.txt
harm/f1..f8.txt                                  falsification receipts
harm/c2-selftest.txt                             census --selftest (8 cases, 0 failed)
harm/skill.diff                                  SKILL.md BASE..T diff
an/registry_diff.py an/regdiff.json              independent registry parse (44 kind cells, 3 rows)
an/scripts_check.py an/scripts_check.json        independent 44-script / 84-gate spelling check
an/spelling_classify.py an/spelling_classify.json  token-level code-vs-prose classification
scope.txt shas.txt commands.txt identity.txt   scope diffs, hashes, exact commands, targeted identity checks
```

No tool was installed or upgraded for this seat. Scratch root removed after these receipts were
copied.

REPORT: .ufo/waves/round-97/w1/ExecHarm.md

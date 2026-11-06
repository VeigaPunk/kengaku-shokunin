# CriticClaims — round 97 w1: closure critique of R97-C1 and R97-C2

Seat: CriticClaims (leaf; no subagents, no `task`). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
BASE `4992cd0e32b8db23ca20310deb7de12d485f8bcc`; P0 `5b41c1c3`; P1 `b2352135`; P2 `e40fd0c2`;
freeze F `8d9d271306c4e7e2d586e51cd546652249d286cb`; measured T
`f1083da60e7ff6b88f7420aae7424f7762d14700`. Scratch `/fast/scratch/hyaku/kengaku-r97/CriticClaims`
(removed before yield; receipts copied to `.ufo/waves/round-97/w1/CriticClaims/`). All commands ran
from the root of a `git clone --shared` detached at T; the three adversarial fixtures were separate
`--shared` clones, each asserted `git rev-parse --show-toplevel` equal to its own root before the
first commit, and every fixture write named that root with `git -C`. No lane mutation, no production
edit, no commit, no `task`. Venv staged in scratch with `uv venv -p 3.13` +
`uv pip install rdflib==7.1.4 pytest==8.4.1` (python 3.13.16, rdflib 7.1.4, pytest 8.4.1,
pyparsing 3.3.3); no host tool install.

## Verdicts

| claim | verdict | one line |
|---|---|---|
| **R97-C1 coverage** | **met** | Independent replay at T prints the exact frozen target (9/9 legs, `executed_rows=41`, `file-artifact:32`, `cases=18 legs=72 mismatches=0 defects=0`); the 18 P0 prediction vectors equal the frozen table; the capture, probe and case table match live upstream bytes and the frozen table at F and T; a forged receipt and a removed ledger member each fail the counter. Two claim-text imprecisions (see F1/F3) do not touch the predicate. |
| **R97-C2 calibration** | **met** | Independent census at T prints `ROWS base=168 rev=171 …`, `GATES total=84 with_selftest=84 without=0 …`, `MISMATCH_TOTAL n=0`, pass rc 0; at BASE it prints `GATES total=127 with_selftest=83 without=44`, `MISMATCH_TOTAL n=44`, fail rc 1; the registry diff is exactly 44 `gate→probe` cells, 0 other cells, 3 added rows; all 84 gates carry a code-level self-test entry point and all 44 demoted scripts carry none. The predicate does not pin the new kind to `probe` (F4) and one harm-check sentence is literally false (F5); the landed bytes are correct. |

## R97-C1 — what I measured

### 1. The replay is real and reproduces the frozen target at T

`python3 plans/round97_c1_replay.py --lane . --rev f1083da6… --work … --grader-venv G` from the
clone root (`c1-replay-at-T.txt`):

```
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass
TARGET executed_rows=41 member=sparql-university cells=file-artifact:32 set_contains_base=1 located=1 executed=1 cases=18 legs=72 mismatches=0 defects=0
PREDICATE R97-C1 pass
rc=0
```

L6 re-ran the frozen probe from a `git archive` of T and compared the whole observation block
(36 lines: 18 `CASE` + 18 `DETAIL`) plus `TOOL_SHA`/`CASE_TABLE_SHA`/`GRADER_SIDE`; the probe runs
the captured `test_outputs.py`'s three functions by import and then real pytest 8.4.1 for the reward
bit, in a `--unshare-all --clearenv` bwrap namespace with the captured test graph at `/tests` and
the agent graph at `/app`. The DETAIL lines independently show each transform's effect (C07 rows=5
with `Marie_Dubois`; C08 rows=5 with `Athanasios_Voulodimos`; C11 rows=8 distinct=4; C12
`vars=professorName+countries+n`; C17 agent-graph names `Orfeas_Menis|Pepe_Attanasio|Aristotle_Tympas`).

### 2. Predictions were filed before the run and were not back-fitted

`git show 5b41c1c3:.ufo/waves/round-97/L1/predictions-mechanism.txt` (P0) parsed against
`git show b2352135:plans/round97-cases.json` (P1): 18/18 `(app, predicted)` pairs equal, 0 mismatches
(`p0-predictions-vs-table.txt`). The P0 file states the only pre-filing input was the solve query on
the **agent** graph; the test-graph mechanism was read, not run. Dry-run 2 is 18/18
(`L1/dryrun/probe-dryrun-2.txt`); dry runs 0/1 failed on probe defects, and the P0 vectors were not
edited afterwards.

### 3. Exact counting values

`ledger-counts.txt` (plain `json` over `git show REV:plans/grader-population-ledger.json`):
BASE 88 members, executed **40**, `file-artifact` executed **31 of 76**; T 88 members, executed
**41**, `file-artifact` **32 of 76**; the member row at T is `status=executed`, `round=97`,
`receipt=corpus/evidence/round97/sparql-probe.txt`, `subject=tb2-header`, `verdict=cases`, and
`sparql-university` is `unexecuted` at BASE. The claim's 40→41 of 88 and 31→32 of 76 are exact.

### 4. Frozen bytes, candidate bytes and C scope

`frozen-and-candidate-hashes.txt`: all 10 `frozen-instruments` rows hash equal at F and at T; the
three candidate bytes hash equal to the `candidate-bytes` table at T
(`739fb58b… SKILL.md`, `567a26bb… ledger`, `c54a0ece… SOURCES.md`); `git diff --name-status F..T`
is exactly `M SKILL.md`, `M corpus/SOURCES.md`, `A corpus/evidence/round97/sparql-probe.txt`,
`M plans/grader-population-ledger.json` — the candidate bytes plus the one receipt, nothing else.
The two instruments' own hashes cannot be self-verified by their predicates; I checked them
externally against the frozen table (both match at T).

### 5. Source grounding

Live fetch of all nine `sparql-university` files at pin `2fd12b88…` (`sources-fetch.txt`): HTTP 200
and sha256 equal to the SOURCES rows for S317–S325 (2399/10680/1600/629/1268/10481/235/1007/1697 B),
and each quoted line sits on its cited line (test_outputs.py:79, test graph:157, solve.sh:46,
test.sh:21, instruction.md:7, Dockerfile:7, task.toml:29, README.md:24). S317–S322 are tier A
admitted, S323–S325 rejected with stated flips; the rows are in C. Source-blind work: none found.

### 6. No-work, forgery and separability

- Committed controls: do-nothing all legs fail rc 1; positive 9/9 pass rc 0; `c1-only` pass rc 0;
  `c2-only` fail rc 1; wrong cwd rc 2; forged receipt (no DETAIL) L6 fail rc 1. Read, not re-run.
- My forged receipt (fixture `fx-forge`, C01 `observed=P,P,P,1 → P,P,P,0`, DETAIL untouched):
  `L5=fail L6=fail`, `DEFECT L5 case C01 …`, `DEFECT L6 rerun … equal=False`, rc 1
  (`c1-forged-receipt.txt`).
- My ledger removal (fixture `fx-ledger`, `build-pmars executed → unexecuted`): `L7=fail`,
  `set_removed=['build-pmars']`, `executed_rows=40`, rc 1 (`c1-ledger-removal.txt`). The target is
  not reachable without the C1 work, and the member-set check bites.

### 7. C1 findings (none changes the predicate)

- **F1 (minor, claim text).** "the verifier side is a venv with `tests/test.sh`'s uvx pins (python
  3.13, rdflib 7.1.4, pytest 8.4.1)" is not an exhaustive list: `tests/test.sh` also pins
  `pytest-json-ctrf==0.3.5` and invokes pytest with `--ctrf /logs/verifier/ctrf.json … -rA`. The
  probe's venv omits the plugin and its pytest command omits those flags. The reward rule is
  `pytest rc 0`, and the plugin is a reporting plugin, so all 18 reward bits are unchanged; the
  claim's substance holds. Smallest correction: say "the three grading pins" (or add the ctrf pin
  and the flags to the claim and to `GRADER_SIDE`).
- **F2 (minor, presentational).** In the TARGET line `executed=1` is `1 if ok else 0` (the predicate
  bit, not the ledger count), `located=1` is "capture file present", and `legs=72` is
  `len(receipt cases) × len(leg_order)` (18×4), not a parsed observation count. The real evidence is
  L6 plus the 18 four-value vectors; the fields are not independent measurements. No correction
  required; a reader should not cite `executed=1` as a count.
- **F3 (minor, evidence independence).** The reward leg is real pytest, but for this grader
  (`test_outputs.py` contains exactly the three test functions) its value is necessarily the
  conjunction of the three: all 18 vectors satisfy `reward=1 ⇔ all three P`. The claim's "not a
  derived bit" is true of the implementation, not of the information content; the effective
  independent observation count is 54, not 72. Smallest correction: state "54 independent leg
  observations + 18 reward conjunctions" if the count is cited as evidence breadth.

## R97-C2 — what I measured

### 1. The census at T passes and at BASE fails with the claimed counts

`python3 plans/round97_gate_selftest_census.py --lane . --rev REV` from the clone root
(`c2-census-at-T.txt`, `c2-census-at-BASE.txt`):

```
T:    ROWS base=168 rev=171 removed=0 duplicate=0 cells_changed=0
      GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0 scripts_changed=0
      MISMATCH_TOTAL n=0
      PREDICATE R97-C2 pass   rc=0
BASE: ROWS base=168 rev=168 removed=0 duplicate=0 cells_changed=0
      GATES total=127 with_selftest=83 without=44 demoted_with_selftest=0 scripts_changed=0
      MISMATCH_TOTAL n=44
      PREDICATE R97-C2 fail   rc=1
```

The BASE run lists exactly the 44 rows in `L1/c2-base.txt`, including `round96-c1-replay` and
`round96-standing-battery`, the two rows the round-96 spot-check routed (defects 3 and 4,
`corpus/lessons/round-96-verifier-spotcheck.md`). The instrument's own `--selftest` is 8/8 green
(`c2-selftest.txt`).

### 2. The correction shape is exact in the landed bytes

Independent parse of the registry at BASE and T (`registry-diff.txt`): 168 → 171 rows; 3 added
(`round97-sparql-probe` probe, `round97-c1-replay` probe, `round97-gate-selftest-census` gate), 0
removed; **44 kind changes, all `gate→probe`**; **0 other cell changes**. The C diff contains no
script file. The SKILL `file-artifact` class cell moved 31→32 of 76 with the round-97 add
(`SKILL.md` diff), and the "Round-97 registry correction" paragraph is present.

### 3. The demotions are truthful at the script-byte level

`gate-spelling-analysis.txt`: all 84 remaining `gate` rows have a code-level self-test entry point
(`add_argument("--selftest")` plus a dispatch/`run_selftest`/subparser; 0 with only prose). All 44
demoted scripts have no self-invocation entry point: their `selftest` tokens are docstrings, expected
strings, or an invocation of **another** script's `--selftest` (`round46-c2` runs
`plans/anchor_line_check.py --selftest`); none exposes a self-test for itself. The two round-96 rows
are among the 44. So the 44→0 is a truthful self-assessment correction, not a spelling trick.

### 4. No-work, forgery and separability

- Committed controls: do-nothing 44 mismatches fail rc 1; blanket retyping `DEMOTED 83` fail rc 1;
  deletion `ROW-REMOVED 44` fail rc 1; self-test-cell rewrite `CELL-CHANGED 44` + `MISMATCH 44` fail
  rc 1; appended script spelling `SCRIPT-CHANGED` + `DEMOTED` fail rc 1; positive pass rc 0;
  `c2-only` pass rc 0; `c1-only` fail 44 rc 1. Read, not re-run.
- My scope fixture (`fx-check`, the 44 rows retyped `check` instead of `probe`): the census still
  prints `GATES total=84 with_selftest=84 without=0`, `MISMATCH_TOTAL n=0`, **pass rc 0**
  (`c2-check-kind-loophole.txt`). The predicate certifies "no `gate` row lacks a spelling", not "the
  44 rows are `probe`". The landed bytes are `probe`, so the claim is true; the predicate is weaker
  than the claim's sentence.

### 5. Harm check

`harm-diff.txt` compares the P1 `b2352135` and candidate+receipt `b82b4c75` receipts for the twelve
standing checks. Eleven are signature-identical (DEFECT lines, rc, PREDICATE). `r78c1` differs in
exactly two lines: `CLASS file-artifact k=31 → 32` and the `DEFECT COUNT-DRIFT file-artifact class
row k=31 → k=32` line. No new defect, no rc change (`PREDICATE R78-C1 fail`, rc 1 at both); the
`r79c1` ledger line moves executed 40→41 and `file-artifact` 31→32 with unchanged DEFECT lines.
The claim's "differ only in row counts and the file-artifact k" is accurate; its "every exit code
and every DEFECT line unchanged" is literally false for the one COUNT-DRIFT line whose k moved.

### 6. C2 findings (none changes the predicate)

- **F4 (minor, kill-rule scope).** The census passes when the 44 rows are retyped to any non-`gate`
  kind (`check` fixture above). The claim's "re-types exactly those 44 rows `probe`" is true of the
  landed bytes but is not enforced by the predicate. Smallest correction: add a leg that every BASE
  `gate` row whose script lacks a spelling is `probe` at REV (or that every kind cell is in
  `gate|probe`), and print the 44 names.
- **F5 (minor, claim text).** "every exit code and every DEFECT line unchanged" is contradicted by
  the r78-c1 `COUNT-DRIFT … k=31 → k=32` line in the claim's own harm receipts. The substantive
  harm check holds (same defect, same ledger executed=4, same rc). Smallest correction: "every
  DEFECT line unchanged except the file-artifact k embedded in r78-c1's COUNT-DRIFT line".
- **F6 (observation, axis fit).** Calibration is held at ceiling 10 (the lane's convention after the
  round-96 harm: score line not edited), and the claim's countable before→after is 44→0 mismatches.
  That fits the calibration axis ("self-assessment matches observed repo state"); it does not move
  the score, and the claim does not say it does.

## Scope observation (round-level, not a claim failure)

The round-97 claims discharge only round-96 routed defects 3 and 4 (the two registry rows) and do
not touch defects 1, 2, 5, 6, 7, 8 (freeze-integrity history harm, standing reds, the R96-C1 finding
set, the C byte-scope check, wave losses, carried items). The SCORECARD's "Planned (round 97)" items
(successor C1 counters for the absolute-L7 class, a deterministic battery, the merger replay's three
wrong-pass states) are also not the frozen claims. The claims are honest about their own scope and
their kill rules do not require the rest; the lane's routed-defect queue remains open and should be
recorded as carried in the round report/SCORECARD rather than read as discharged by the 44-row
correction (the `freeze-integrity` row is among the 44, but demoting its registry kind does not
repair the r93/r94/r95 verdicts).

## Impacted axes

| axis | effect of the landed bytes | evidence |
|---|---|---|
| coverage | improved as claimed: executed 40→41 of 88, `file-artifact` 31→32 of 76, member set = BASE ∪ {sparql-university}; score held at the L0 cap 7 | `ledger-counts.txt`, `c1-replay-at-T.txt` |
| calibration | improved as claimed on the registry self-assessment: 44 spelling mismatches → 0, 44 truthful `gate→probe` retypes, no script change; score held at ceiling 10 | `c2-census-at-T.txt`, `registry-diff.txt`, `gate-spelling-analysis.txt` |
| other axes | no claim; no harm found in the twelve standing checks beyond the disclosed file-artifact k line | `harm-diff.txt` |

## Smallest safe corrections (routed, not applied)

1. C1 claim/S320: say "the three grading pins" or add `pytest-json-ctrf==0.3.5` and the
   `--ctrf`/`-rA` flags to the modelled verifier side (F1).
2. C2 census: pin the corrected rows' new kind to `probe` (or validate `gate|probe`) and print the
   44 names (F4).
3. C2 claim harm sentence: except the r78-c1 `COUNT-DRIFT` k value (F5).
4. Round report/SCORECARD: record round-96 routed defects 1, 2, 5, 6, 7, 8 as carried (scope
   observation).

## Evidence

`.ufo/waves/round-97/w1/CriticClaims/`: `c1-replay-at-T.txt`, `c1-forged-receipt.txt`,
`c1-ledger-removal.txt`, `c2-census-at-T.txt`, `c2-census-at-BASE.txt`, `c2-selftest.txt`,
`c2-check-kind-loophole.txt`, `registry-diff.txt`, `gate-spelling-analysis.txt`,
`ledger-counts.txt`, `p0-predictions-vs-table.txt`, `frozen-and-candidate-hashes.txt`,
`sources-fetch.txt`, `harm-diff.txt`.

report: .ufo/waves/round-97/w1/CriticClaims.md

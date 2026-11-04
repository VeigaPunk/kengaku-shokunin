author: hyaku closure (non-author integrator, @m_zfl)
lane: kengaku · round: 71 · date: 2026-11-03
report: `.ufo/reports/round-71/kengaku.md` (fleet commit `916cd7d4`, lane identity)
lane base `1cb49cac` → lane tip `edaea66e` (remote `refs/heads/master` = `edaea66e`)

# Round 71 — kengaku verifier spot-check (non-author)

I did not author this round. Everything below is re-derived from committed bytes at the lane tip
unless it says *evidence-verified*: lane-owned gates and selftests were checked by their committed
receipts, never executed (PROTOCOL §Gate standard, Closure consequence).

## 1. Step-1 conformance

| item | check | observed |
|---|---|---|
| report landed by the lane | `git log --format='%an %H' -- .ufo/reports/round-71/kengaku.md` | `kengaku-shokunin <kengaku@shokunin.local> 916cd7d4`; ancestor of fleet `origin/master` (`8ccfd01e`) |
| SHONEN heading | `grep -c '^## SHONEN' report`; `[~]` lines vs `SHONEN.md` boxes | 1 heading; 4 `[~]` lines = 4 boxes, each with a resolvable pointer |
| cited commits | `git cat-file -t` + `merge-base --is-ancestor <h> master` for `1cb49cac`/`d8a77d3f`/`c80fcdb3`/`edaea66e` | all four commits; all four ancestors of `master` |
| lane clean / pushed | `jj-lane.sh state`; `git status --porcelain` | `local=edaea66e remote=edaea66e ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty |
| prompt fidelity | rendered `templates/round-prompt.md` (§1–5, substitutions only) vs `.ufo/prompts/kengaku-round-71.md` §1–5 | `diff` empty → IDENTICAL; §6 addendum present |
| L2 route map | prompt net map vs `~/.omp/agent/config.yml` `agentModelOverrides` | prompt "only reviewer `@m_zfl`" = config (`reviewer: @m_zfl`, all 17 other roles `@m_flash`); `MISSION.md` bucket is role-class advisory, no alias conflict |
| wave shape | `w1-validate.rc`/`.out`, `w1-results.json` | rc 0; `counts={"spawn":14,"resume":0,"total":14}`; 14 seats = executor 4, reviewer 3, mutation-tester 2, scribe 2, critic 1, scout 1, connector 1; attack 6/14 = 43 % ≥ 25 %; 1 connector ≤ 2; 14/14 seat reports on disk; `CounterMutate71.md` embeds the seat output byte-exact (4634 B, equal) |
| report sections | order and presence | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN, Addendum — all present |

**Conformance defects (status-neutral; routed below).** (a) The report says the three closing
counters were "measured at `edaea66e`" (lines 133/141/149), but the committed receipts' `REV`
line reads `c80fcdb3`; `edaea66e` only adds the receipt files (`git log -- corpus/evidence/round71/final-c1-check.txt`
→ `edaea66e`). (b) The round prompt §2 planner-seat ruling requires the L1 to record the
planner mapping in the report; `grep -i planner` over the report → 0 hits. (c) Neither round-71
instrument has a row in the lane's `SKILL.md` `## Gate/probe registry` (§Gate standard,
Registry/Delivery), so neither is gradeable conformant yet. (d) The frozen claims doc's
"Do-nothing control (committed at freeze)" is false of `d8a77d3f` (the control landed at
`c80fcdb3`); "Red-before (committed at freeze)" is a red-data run with the freeze instrument
because the gate did not exist at base. The lane captured (c)-(d)'s substance as its own
`## Mistakes` rows; they stay named here because they outlive the round.

## 2. Claim re-checks

### R71-C1 — coverage (lowest non-retired axis, L0-capped at 7)

| measurement | command | base `1cb49cac` | tip `edaea66e` |
|---|---|---|---|
| receipt absent → present | `git cat-file -e 1cb49cac:corpus/evidence/round71/hf/receipt.txt` | rc 128 | 2940 B, 36 lines |
| class row moves | `grep -c 'executed 3 of 8' SKILL.md` → `grep -c 'executed 4 of 8' SKILL.md` | 1 / 0 | 0 / 1 (`SKILL.md:78`) |
| new registry rows | `grep -cE '^\|[[:space:]]*S24[56][[:space:]]*\|' corpus/SOURCES.md` | 0 | 2 (rows 238 total vs 236) |
| frozen vectors | `grep -c 'agree=True' receipt.txt`; probe `VECTORS` vs claims table | — | 8; K1–K8 = PPPP/PPFP/PPFP/PPPF/PFPP/PFFF/FPPP/FPPP, identical in both files |
| leg coverage | awk over the eight `LEGS` lines | — | each of the four legs has `P=1` and `F=1` (`legs_with_both=4`) |
| grader digest | `sha256sum corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` | — | `61a686d6…87857` = receipt `GRADER`, `SHA256SUMS:76`, and a live fetch (HTTP 200, 4239 B) |
| instruction digest | `sha256sum corpus/evidence/round71/hf/instruction.md` | — | `29151c5b…d1cc1` = receipt and live fetch (HTTP 200, 1264 B) |
| model tree | `tree_digest` recipe over the five committed fixture files | — | `c5c25767…8944` = receipt `MODEL` |
| probe blob | `git show d8a77d3f:plans/round71_c1_hf_probe.py | sha256sum`; `sha256sum` at tip | — | `d5ce2fa5…a82e` at both revisions = `PROBE`/`PROBE_BLOB` |
| case digests | re-staged all eight cases from the committed model + grader with the probe's own `stage_case`/`tree_digest` | — | all eight equal the receipt's `case_sha256` (K1 `e96b30e1` … K8 `82c99ab8`) |
| replicate | `diff receipt.txt receipt-replicate.txt` | — | empty (36 lines each) |
| do-nothing control | `.ufo/waves/round-71/c1-control.txt` | — | 8 × `derived=FFFF`, `LEG-COVERAGE legs=4 seen_p=0 seen_f=4`, `PREDICATE R71-C1 fail` |
| checker | `corpus/evidence/round71/final-c1-check.txt` (+ `hf/check.txt`) | — | `DEFECTS n=0`, `PREDICATE R71-C1 pass`, `RC=0` |

*Re-measured:* every digest, the eight case digests, the vectors/coverage re-parsed from the
`LEGS` lines, the before-state greps, the control's vectors, the replicate identity.
*Evidence-verified, not executed:* the battery itself and `--check-receipt`/`--selftest`; the
receipts are internally consistent and their bound inputs re-derive. The claim's own named
limitations (outcome-not-provenance witness, leg-not-assert unit, `--check-receipt` as
consistency check) are recorded by the lane and are not defects of this claim.

### R71-C2 — calibration (held at ceiling 10, exercised)

| measurement | base `1cb49cac` | tip `edaea66e` |
|---|---|---|
| round-70 `## Mistakes` rows | 8 data rows (10 `|` lines = header+separator+8) | 8, same eight class keys |
| `LOG.md` "five rows" | present in the round-70 block | superseded text kept as written + dated appended correction at `LOG.md:2650` naming R70-D1, quoting "five rows", stating eight |
| `corpus/README.md` supporting block | "six Mistakes rows" (`:799`) | eight, all eight classes named (`:802`) |
| `corpus/README.md` index row | "eight Mistakes rows" naming six (`:565`) | eight, all eight classes named (`:567`) |
| nginx entry | body sentence cites `instruction.md:6-11` for the bodies (`:15`), no erratum | `## Errata` E-D2 + E-D2a appended; superseded sentence kept verbatim; corrected range `instruction.md:6-11,15-18` |
| append-only shape | — | diff base→tip: nginx +11/−0, lesson `round-70.md` +8/−0, `LOG.md` +49/−0, `README.md` +16/−2 (two old→new lines); repo total 3 deletions (README ×2, SKILL class row) |
| gate red → green | `.ufo/waves/round-71/c2-red-before.txt`: `E1b`, `E1c`×3, `E2a`×2 → `DEFECTS n=6`, `PREDICATE R71-C2 fail`, rc 1 | `final-c2-gate.txt`: `E1a ok` … `E2a ok`, `DEFECTS n=0`, `PREDICATE R71-C2 pass`, `RC=0` |
| controls | — | `c2-controls.txt`: `defects-in-fake=4 want=4 all-fail=True append-only-arm=True`; `MUTANTS total=4 killed=4 survived=0` |

*Re-measured:* all six base defect sites and their corrections, the eight rows, the append-only
diff shape. *Evidence-verified:* the selftest and mutant tallies. The gate was not executed. The
lane's own reported weakness — `--mutants` 4/4 is invariant under a semantic matrix (2/6 killed),
`parse_count` false-reds a digit `8` and a backticked `` `eight` `` — is recorded and routed, and
does not change the frozen predicate's verdict.

### No axis harmed

`git diff --stat 1cb49cac edaea66e -- SCORECARD.md` → 88 insertions, 0 deletions (pure append;
every prior axis row untouched). `SKILL.md` diff → 1 insertion, 1 deletion (the class row only).
`PROVINCE.md` diff → empty. Depth gate receipt `gates/final-depth.txt` (evidence-verified):
`REV c80fcdb3`, `ROWS n=16 class_match=True count_mismatch=0 paths total=36 resolved=36
share=1.00`, `PREDICATE R63-C2 pass`; the decision table's 16 data rows re-counted.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | improved | class row `executed 3 of 8` → `4 of 8` on a passing frozen predicate; score still held at 7 by the open L0 cap `kengaku | round-25/33/51` |
| calibration | improved | the round-70 closure's two routed defects closed by a re-deriving gate `n=6` → `n=0` with selftest 4/4 and mutants 4/4; score held at ceiling 10, exercised |
| depth | unchanged | one new sourced entry + two tier-A rows; depth gate green; score 10 held |
| operability | unchanged | two instruments run; no new gate registered (see R71-R1); score 10 held |
| freshness | unchanged | both pinned sources re-fetched live with sha256 + `cmp`; score 10 held |
| adjacency | unchanged | `SiblingOverlap71` 13/13 term-level, 0 surface-level; nothing routed; score 9 held |
| novelty | unchanged | no new instrument-level construct claimed; score 8 held |

## 4. Discernment spot-check (non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S245 — TB2 `hf-model-inference` instruction at pin `2fd12b88` | admit, tier A | live `curl` of the pinned URL (HTTP 200, 1264 B, sha256 `29151c5b…d1cc1`) and `corpus/evidence/round71/hf/instruction.md` | agree | sha matches the row and the committed capture; the 16-word `:3` quote is present verbatim; the file states the request/response schema (`:11-24`) and not the six graded texts, as the row claims |
| S246 — the grader at the same pin | admit, tier A | live `curl` (HTTP 200, 4239 B, sha256 `61a686d6…87857`), the committed capture and `SHA256SUMS:76` | agree | sha triple-matches; the `:29-30` liveness quote is present; the 400 assert is the unquoted `assert response.status_code == 400,` at `:103` |
| `merge/kengaku` entry `grader-predicate-input-types.md` | reject (reason + flip) | `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/grader-predicate-input-types.md` (3300 B) and this lane's registry | agree | line 1 blank, `source:` at `:2-3`, `recheck:` at `:5`; its cited S143/S144 resolve here to the `feal-linear-cryptanalysis` README/`solve.sh` (`corpus/SOURCES.md:160-161`); `git ls-files | grep -c 'lanes/kengaku'` → 0, so the "16 of 16 separate the two" (`:23`) has no held artefact; the flip condition is stated |

Both new `SOURCES.md` rows carry ≤25-word located quotes (16 and 4 words) and their `mined`
status/`used-by` point at the new entry. Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin kengaku` → rc 0, 238 rows, 25 pre-existing `W04`.

## 5. Trend verdicts

- **expansion: improved** — the `network-service` class row moves `executed 3 of 8` → `4 of 8`
  (measured), S245/S246 are new mined tier-A rows cited by the landed entry (census 236 → 238),
  and the README frontier bullet gains "Partly discharged round 71" (`:459`). Caveat, recorded:
  the knowledge entry itself lands `admission: hold` (Q13/Q14 second-seat re-read absent), so the
  "net new admitted entries" leg is not exercised; the verdict rests on the executed-member /
  class-row / frontier / registry evidence.
- **quality: improved** — the two routed defects from the round-70 closure are corrected
  append-only and their six base defect sites no longer exist; Q53 enters with the round's
  leg-vs-assert lesson; the depth gate is green and no admitted entry failed its re-check.
- **discernment: improved** — the three gate decisions above re-open agree; the wave's attack
  seats wrote the round's defects down (the verbatim-quote gap produced `E-D2a`; the leg/assert
  gap produced Q53); the entry is held rather than self-admitted, and the do-nothing control
  refuses the claim.

## 6. Routed defects the lane must fix next round

1. **R71-R1 — instrument registry rows absent.** Neither `plans/round71_c1_hf_probe.py` nor
   `plans/round71_c2_routed_defects.py` appears in `SKILL.md` `## Gate/probe registry`
   (`grep -c 'round71_' SKILL.md` → 0). §Gate standard Registry/Delivery: a gate is not gradeable
   conformant until its row exists. Add rows (kind, entry command, verdict map with declared
   nonzero codes, self-test spelling, pinned values, write scope, owner) for both.
2. **R71-R2 — report revision attribution.** Report lines 133/141/149 say the counters were
   measured at `edaea66e`; the receipts' `REV` line is `c80fcdb3` and `edaea66e` only adds the
   receipt files. Correct in round 72's report (filed reports are records — append, never rewrite).
3. **R71-R3 — planner mapping not recorded.** Round prompt §2 requires the report to record that
   the L1 holds the planner seat (the validator rejects the role); the report has no mention.
4. **R71-R4 — C1 `--selftest` two defective arms** (lane-routed): `case_digest` runs without
   `--work` (`refused=False`) and the `PATH-INDEPENDENT` arm crashes (`grader copy missing`) —
   `corpus/evidence/round71/c1-selftest.txt`.
5. **R71-R5 — C2 mutation metric and `parse_count`** (lane-routed): `--mutants` 4/4 is invariant
   under a semantic matrix (`GateMutate71`: 2/6 killed, 4/6 survived; M1/M2 pass on defective
   bytes); `parse_count` false-reds a digit `8` and a backticked `` `eight` ``.
6. **R71-R6 — sandbox environment inheritance** (lane-routed): `bwrap` without `--clearenv` lets a
   `PYTHONPATH` stub reproduce 8/8 vectors and a byte-identical receipt; the model-load witness is
   an outcome check. Fix in the round-72 successor instrument.
7. **R71-R7 — freeze-doc overclaims** (lane self-captured): the control and red-before labels do
   not match the freeze commit's contents; reword in round 72 and keep the receipts labelled.

## 7. Notes for the operator

All four `SHONEN.md` boxes carry `[~]` with pointers that resolve for a non-author (SKILL decision
table + depth gate; the R71-C1 LOG entry → receipt; the entry's `recheck:`; `SiblingOverlap71`).
No `[x]` was written — promotion is operator-owned. The entry `corpus/knowledge/tb2-hf-model-inference-offline.md`
stays at `admission: hold` until the round-72 falsify wave; `plans/gate_timing_check.py` prints
`no admit rows … failed=1` at this tip by design.

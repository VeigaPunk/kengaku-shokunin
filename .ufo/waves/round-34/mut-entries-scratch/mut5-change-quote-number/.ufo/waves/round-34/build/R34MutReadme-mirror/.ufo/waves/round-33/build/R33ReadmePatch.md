# R33ReadmePatch — corpus/README.md patch blocks for the admitted grader-semantics entry

Seat: `R33ReadmePatch` (leaf; no subagent dispatch, no background jobs, no model pinning).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Access date for every source touched: **2026-10-25**.
Report path: `.ufo/waves/round-33/build/R33ReadmePatch.md`.
Production writes by this seat: **none**. This file is the only lane path written.

## 1. Baseline and observed tree state

- `HEAD` = `7895588` — `round-33: C2 routed-defect repairs (N2 scorecard section, N5/N6 lesson errata), Q22, defects-after receipt`.
  Behind it: `c227e48` (round-32 wave inheritance, defect N1), `f0b20ae` (frozen claims/counters/controls).
- `git status --porcelain` at read time:
  `M corpus/README.md`, `M corpus/SOURCES.md`, `M corpus/knowledge/benchmark-grader-semantics.md`,
  `M plans/round33_c1_verify.py`, plus untracked `.ufo/waves/round-33/` (`assimilation/`, `build/`,
  `build-dispatch.json`, `build-spec.json`, `build-validate-err.txt`, `build.ready`, `build.ready.dispatched`).
- **`corpus/README.md` already carries an in-flight after-state in the working tree** (3 insertions / 3
  deletions vs `HEAD`, exactly lines 67 / 255 / 279, `388` lines at both ends). This seat did not write it.
  The blocks below are keyed to `HEAD` so they are idempotent against that in-flight state; the only delta
  between the in-flight text and the recommended after-text is the `, S103` insertion on line 279 (§4).
- Anchors verified by numbering: index row `:67` (single row for the entry), coverage bullet `:255`,
  frontier sub-bullet `:279`. No `S094` / `S097` token survives anywhere in the README (`awk` scan, zero hits).

## 2. (a) Index row — `corpus/README.md:67`

Requirement: citation cell names S103/S104 in place of S094/S097, row shape kept, exactly one row for the
entry. The after-block additionally carries the C1-mandated credential correction in the description cell
(see §6, Finding F2).

BEFORE (`HEAD:corpus/README.md:67`):

```
| `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; a log-bucket check fails open) and the LLM-as-judge survey frame: meta-evaluation is its own part | S094 (Toolathlon @ 9be8d8fe), S097 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry |
```

AFTER:

```
| `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; its log-bucket check mixes fail-open exceptions with fail-closed credential absence) and the LLM-as-judge survey frame: meta-evaluation is its own part | S103 (Toolathlon @ 9be8d8fe), S104 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry |
```

Span-level delta (character opcodes, `difflib`): description cell `a log-bucket check fails open` →
`its log-bucket check mixes fail-open exceptions with fail-closed credential absence`; citation cell
`S094`→`S103`, `S097`→`S104`. Cell count `3` before and after; leading cell still
`` `knowledge/benchmark-grader-semantics.md` ``; `S093 restated from the verifier-execution entry` retained.

## 3. (b) Coverage bullet — `corpus/README.md:255`

Requirement: `round 32` attribution → `round 33 (admitted under renumbered ids)`, same claim text.

BEFORE (`HEAD:corpus/README.md:255`):

```
- **Benchmark grader semantics**: covered at source-code depth (round 32, 2026-10-25) — knowledge/benchmark-grader-semantics.md; S093, S094, S097. Discharges the round-31 frontier clause "and for Toolathlon" for the one task whose evaluation script is read (Toolathlon `ab-testing/evaluation/main.py` @ `9be8d8fe`): the grader is a deterministic state comparison — `record.csv` vs `expected_ratio.csv` within the executed 0.05% tolerance — preceded by two side-effect checks, one of which fails open; the S097 survey separates Meta-evaluation from methodology, so judge-based scoring owns its validation part. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
```

AFTER:

```
- **Benchmark grader semantics**: covered at source-code depth (round 33, 2026-10-25, admitted under renumbered ids) — knowledge/benchmark-grader-semantics.md; S093, S103, S104. Discharges the round-31 frontier clause "and for Toolathlon" for the one task whose evaluation script is read (Toolathlon `ab-testing/evaluation/main.py` @ `9be8d8fe`): the grader is a deterministic state comparison — `record.csv` vs `expected_ratio.csv` within the executed 0.05% tolerance — preceded by two side-effect checks, the log-bucket one mixing fail-open exceptions with fail-closed credential absence; the S104 survey separates Meta-evaluation from methodology, so judge-based scoring owns its validation part. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
```

Span-level delta: `round 32`→`round 33`; `, admitted under renumbered ids` inserted inside the existing
parenthesis; `S094`→`S103`, `S097`→`S104` (two id sites); `one of which fails open` → `the log-bucket one
mixing fail-open exceptions with fail-closed credential absence`. Sentence structure, the 0.05% clause, the
`PROVINCE` refusal and the three "Not …" disclaimers are byte-identical to `HEAD`.

Selection note (b1): the phrase is rendered as `(round 33, 2026-10-25, admitted under renumbered ids)`
— the house form used by `:254` and `:253` — rather than nested parentheses
`(round 33 (admitted under renumbered ids), 2026-10-25)`. Both contain `round 33` and
`admitted under renumbered ids`; if a literal byte-match for the latter is required, moving the clause
before the date is the only change (`(round 33, admitted under renumbered ids, 2026-10-25)`).

## 4. (c) Frontier bullet — `corpus/README.md:279`

Requirement: record the `"and for Toolathlon"` clause discharged for the ab-testing task **under S103**.
The in-flight working-tree text names the path/commit and S104 but **never names S103**; the block below is
therefore the in-flight text plus exactly one insertion, `, S103`.

BEFORE (`HEAD:corpus/README.md:279`; 574 chars):

```
  - *Partly discharged round 32 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey frame (S097). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

AFTER (recommended; = in-flight text + `, S103`):

```
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads the one Toolathlon task whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`, S103) and the LLM-as-judge survey frame (S104). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

Span-level delta vs `HEAD`: `round 32`→`round 33`; `9be8d8fe`)`→`9be8d8fe`, S103)`; `S097`→`S104`.
Nothing else moves: the scope limitation (**for that one task's scoring code only**), the two open clauses,
and the `PROVINCE.md` refusal stay byte-identical.

## 5. (d) Nothing else changes — checks actually run

Read-only checks against the tree (script `/tmp/r33-R33ReadmePatch/check_readme.py`, exit 0):

| Check | HEAD | after (working tree, +`, S103` on :279) |
|---|---|---|
| README line count | 388 | 388 |
| `^\| \`knowledge/…\` \|` rows | 41 | 41 |
| rows for `benchmark-grader-semantics.md` | 1 | 1 |
| row cell count / non-empty cells 2,3 | 3 / yes | 3 / yes |
| row citation ids | S093,S094,S097 | S093,S103,S104 |
| refused ids in row | S094,S097 present | absent |
| `S094`/`S097` anywhere in README | 0 hits (post-patch scan) | 0 hits |
| coverage bullet: `round 33` + `admitted under renumbered ids` | no | yes |
| frontier :279: `round 33`, clause discharged, S104, `ab-testing/evaluation/main.py` | no/no/S097/yes | yes/yes/yes/yes |

- The three changed lines are adjacent-history-free: no other README line is touched (git diff = 3 hunks,
  `3 insertions(+), 3 deletions(-)`), so no history/attribution row is rewritten and no new index row appears.
- The row's cited ids resolve to live registry rows `S093` (`corpus/SOURCES.md:112`, `mined`),
  `S103` (`:118`), `S104` (`:119`) — so the README does not cite a non-existent source.
- `plans/adoption_check.py` (read at `:60-140`) only requires, for the README, exactly one anchored row
  matching `^\| \`knowledge/<name>\` \|` with non-empty cells 2 and 3. The after-text satisfies that
  (`rows==1`, 3 cells). This seat did **not** run the full adoption counter/census (owned by the C1 scorer);
  the README-only predicate was exercised directly, not inferred.

## 6. Findings

- **F1 (must fix before integration): `S103` is absent from frontier `:279`.** The in-flight line records
  the discharged clause and the pinned path/commit but attributes no id; item (c) requires the discharge
  *under S103*. §4 inserts `, S103` and changes nothing else.
- **F2 (deliberate deviation, needs explicit acceptance): "same claim text".** Item (b) says keep the claim
  text, but the README's HEAD text asserts `one of which fails open`, and the round-33 lane facts require the
  corrected reading (credential failures fall through to implicit `None` and **fail closed**). Leaving the
  old clause would make the coverage map contradict the entry it indexes. §2/§3 therefore carry the corrected
  credential clause. If the integrator demands byte-minimal edits instead, the only subtraction is that
  clause (returning to `one of which fails open` / `a log-bucket check fails open`), which I do not recommend.
- **F3 (out of this seat's surface, reported only):** the entry `corpus/knowledge/benchmark-grader-semantics.md`
  cites `corpus/README.md:276` for the clause `"and for Toolathlon"`. `:276` is the *bullet header*; the
  literal clause sits on `:278` (`… and for Toolathlon;`). The anchor points at the right bullet but not the
  right line. No README block here depends on it; the entry owner should decide `:276` vs `:278`.
- **F4:** the C1-mandated tolerance correction (`0.1` signature default vs executed `0.05`) does **not** touch
  the README — `HEAD:67` and `HEAD:255` already say "executed 0.05% tolerance". Only the credential
  misstatement is present in this surface, which narrows F2 to one clause.

## 7. Commands run (all read-only; no lane writes, no git mutation)

- `git -C <lane> status --porcelain`; `git -C <lane> log --oneline -3` — tree state, tip `7895588`.
- `git -C <lane> diff -- corpus/README.md` — 3 hunks, 3+/3-.
- `git show HEAD:corpus/README.md | sed -n '67p;255p;279p'`; `sed -n` on the working tree — before/after bytes.
- `awk` line-number scans for anchors and for `S094|S097` (zero hits post-patch).
- `awk` scan of `corpus/SOURCES.md` for rows S093/S103/S104 — rows present at `:112/:118/:119`.
- `python3 /tmp/r33-R33ReadmePatch/check_readme.py` — opcode-level diff of the three lines, row counts, cell
  shape, cited-id extraction, predicate checks. Exit 0.
- Scratch: `/tmp/r33-R33ReadmePatch/` (script + two README copies, < 100 KiB). No tooling installed or
  upgraded this seat; `/home/vgpnk/Projects/shokuknow` untouched; no campaign tool run.

## 8. Out of scope / not claimed

- Not run by this seat: `plans/adoption_check.py --expect … --census`, `plans/round33_c1_verify.py`,
  `plans/round33_defects.py`, `plans/catalog_probe.py --verify`. Their receipts belong to the C1/C2/C3 scorers.
- Not claimed: registry (`corpus/SOURCES.md`) correctness, entry prose correctness, admission, SCORECARD,
  lessons, fleet-report errata. This report drafts README bytes only.
- The in-flight working tree is a peer's/L1's state; this seat neither authored nor reverted it.

VERDICT: readme-patched

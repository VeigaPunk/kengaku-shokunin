# ScribeLesson — round 97 lesson draft

Seat: ScribeLesson (leaf, no subagents). Date: 2026-11-06. Lane `kengaku-shokunin`, round 97.
Measured tip T `f1083da60e7ff6b88f7420aae7424f7762d14700`; BASE `4992cd0e32b8db23ca20310deb7de12d485f8bcc`;
F `8d9d271306c4e7e2d586e51cd546652249d286cb`. Frozen plan: `plans/round-97-claims.md`.

This is a **draft only**: it is written in the wave dir for the L1 to integrate. No corpus file was
edited, no production byte was changed, no instrument was run against the lane's writable state.
The existing L1 draft `corpus/lessons/round-97.md` (untracked, 50 lines) was read as a cross-check;
where this draft differs, the difference is called out (F1, F5).

Method: read the frozen claims, the r96 spot-check §6, the r96 lesson, the r97 receipts and the two
instruments; re-derived the S317–S325 rows from the captured bytes at T with
`verify_gate_rows.py` (sha256, byte size, cited line, quote, `len(quote.split())`); reconstructed the
dry-run-1 staging dispatch from the frozen `VARIANTS` map and case table; ran the C2 census's own
`--selftest` over isolated fixtures. The C1 replay and the full C2 census were **not** re-run here;
their official receipts are cited. Live source re-open is the ScoutSources seat's surface; this
draft verifies the captured bytes, not a fresh HTTP fetch.

## 1. Gate table — S317–S325 (draft for `corpus/lessons/round-97.md` §Gate)

Candidates opened this round (CORPUS rule 1). Capture: `L1/capture-sha.txt` — fetched
2026-11-06T01:01:20-03:00 from `raw.githubusercontent.com/harbor-framework/terminal-bench-2`
at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, all HTTP 200; nine files, nine sha256 stamps.
The quotes below were checked against the captured bytes at T and the word counts recomputed
with `len(quote.split())`, not copied from the rows. Six admitted as primary replay inputs/contracts, three rejected as unnecessary or derivative.

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S317 `sparql-university/tests/test_outputs.py` | **admit** (tier A, member replay only) | 2026-11-06, 2399 B, sha256 `ecf15840…` | `tests/test_outputs.py:79` “assert result_set == reference_set, (” (5 words) | the three functions the fifteenth replay grades: the results test compares SETS of (name, sorted countries), so duplicate rows (C11), an extra projected column (C12) and a literal VALUES answer (C10) pass; a renamed variable raises AttributeError (C16) | — |
| S318 `tests/university_graph_test.ttl` | **admit** (tier A) | 2026-11-06, 10680 B, sha256 `368ce01d…` | `tests/university_graph_test.ttl:157` “uni:worksIn uni:Engineering_Berkeley, uni:Robotics_UPM , uni:Physics_ETH .” (6 words) | the hidden graph the grader reads: every professor the EU criterion would exclude is excluded by the >10 rule too (C05 passes without it); no professor separates per-department from aggregate counting (C09); graduations end 2026-06-12, so a NOW()-dated query passes (C06) | — |
| S319 `solution/solve.sh` | **admit** (tier A) | 2026-11-06, 1600 B, sha256 `d17995a8…` | `solution/solve.sh:46` “HAVING(COUNT(DISTINCT ?student) > 10)” (4 words) | the positive control, run unmodified (C01); it counts distinct students across ALL of a professor's departments, not per department as the instruction states, and the test graph cannot tell the two apart (C09) | — |
| S320 `tests/test.sh` | **admit** (tier A, grader-side pins) | 2026-11-06, 629 B, sha256 `45902b57…` | `tests/test.sh:21` “-w rdflib==7.1.4 \” (3 words) | `uvx -p 3.13` with pytest 8.4.1 and rdflib 7.1.4 runs only `tests/test_outputs.py`; reward 1 iff pytest exits 0; the replay's reward leg runs that pytest for real (no derived bit) | — |
| S321 `instruction.md` | **admit** (tier A, agent-facing contract) | 2026-11-06, 1268 B, sha256 `22eeab47…` | `instruction.md:7` “3. Among all departments they work in, at least one has more than 10 students currently enrolled in any classes taught in that department.” (24 words) | the stated contract is stricter than the graded one: an EU-agnostic query (C05), a NOW()-dated query (C06), duplicate rows (C11), an extra column (C12) and a hardcoded answer (C10) all pass | — |
| S322 `environment/university_graph.ttl` | **admit** (tier A) | 2026-11-06, 10481 B, sha256 `0b0b1f2c…` | `environment/university_graph.ttl:113` “uni:hasName "Orfeas Menis" ;” (4 words) | the graph the agent can query; it names two professors the test graph replaces (Orfeas Menis, Pepe Attanasio), so a query hardcoding the agent-graph answer fails (C17) while one hardcoding the test answer passes (C10) | — |
| S323 `environment/Dockerfile` | **reject** (tier A) | 2026-11-06, 235 B, sha256 `dd0abcd6…` | `environment/Dockerfile:7` “COPY university_graph.ttl /app/” (3 words) | REJECTED as an input: `ubuntu:24.04` plus the agent graph, no package pins; the replay stages the same `/app` bytes and never runs agent-side code beyond `solve.sh`'s heredoc | flip: a case whose verdict depends on an agent-side tool |
| S324 `task.toml` | **reject** (tier A) | 2026-11-06, 1007 B, sha256 `47a6f6dd…` | `task.toml:29` “docker_image = "alexgshaw/sparql-university:20251031"” (3 words) | REJECTED as an input: the harness runs a prebuilt image the replay never pulls; the grader side is modelled by a pinned venv | flip: the image pulled and its `/app` and verifier versions compared to `GRADER_SIDE` |
| S325 `README.md` | **reject** (tier B) | 2026-11-06, 1697 B, sha256 `947086de…` | `README.md:24` “3. The query returns the correct set of professors and countries, matching reference results (4 professors expected)” (17 words) | REJECTED: restates the instruction (S321) and carries no byte the grader or the replay reads | flip: a claim about the README's own statements |

Verification (receipt `ScribeLesson/gate-rows.txt`): all 9 rows — captured sha256 equals the row
stamp, captured byte size equals the row's HTTP size, the quote occurs on the cited line, and the
word count equals `len(quote.split())`; `ROWS 9 defects 0`, rc 0. Longest quote 24 words (S321),
under the 25-word cap. Registry old→new: no existing row changed; S317–S325 added (8 tier A, 1
tier B; 6 mined, 3 rejected); rows 308→317 (`L1/census-start.txt`, `L1/census-end.txt`); anchor gate
`live=0 cells=0` (`L1/anchor-tip.txt`).

**Gate criterion red case** (`ScribeLesson/gate-rows-mutated.txt`): a scratch copy of SOURCES with
S317's cited line moved 79→80, S321's word count 24→23, and S323's sha first nibble changed returns
`ROWS 9 defects 3`, rc 1 — the line check prints the actual line 79, the word check prints
`24/23`, the sha check prints `MISMATCH`. The criterion is falsifiable, not a rubber stamp.

## 2. Round-96 routed defects — disposition (draft for `corpus/lessons/round-97.md`)

Source: `corpus/lessons/round-96-verifier-spotcheck.md:115-124` (eight items). Dispositions are what
the r97 bytes and receipts show, not what the claims promise.

| # | routed defect (r96 spot-check §6) | round-97 disposition | evidence |
|---|---|---|---|
| 1 | r93/r94/r95 freeze-integrity gates read `broken:touched-after-freeze` permanently; land successor counters with new freeze tables (Q79) or a dated waiver; never byte-edit closed tables | **carried, not claimed.** The `freeze-integrity` row (`plans/round94_freeze_integrity.py`) is one of the 44 re-typed `gate`→`probe`, which changes the registry's self-assessment, not the broken readings. No successor counter and no dated waiver landed; the claims repeat Q79 (no closed instrument edited), and the L1 draft's #1 says “Successors deferred”. | `c2-base.txt:41` `MISMATCH freeze-integrity plans/round94_freeze_integrity.py`; `c2-tip.txt` `MISMATCH_TOTAL n=0`; grep for `waiver`/`successor counter` over `plans/round-97-claims.md` and `.ufo/waves/round-97/` returns nothing |
| 2 | seven standing reds: r79 `SUBJECT-MISMATCH mteb-retrieve` and r90–r95 absolute L7 pins; successor counters, not edits | **carried, not claimed.** r79 is still red at the candidate: `DEFECT SUBJECT-MISMATCH mteb-retrieve ledger=tb2-result-file receipt=tb2-header`, `PREDICATE R79-C1 fail`, rc 1. The r97 C1 growth 40→41 is in the direction that keeps an absolute pin red; the r90–r95 counters are not in the r97 harm-check population, so their state is not re-measured here [INFERENCE: they remain red, because their L7 pins are absolute totals below 41]. The new r97 C1 counter's L7 is member-set keyed (never an absolute total), so the new instrument avoids the class; the old reds remain. | `L1/controls/harm-pre-freeze/b82b4c75/r79c1.txt` (executed=41, `DEFECTS n=1`, rc 1); `b2352135/r79c1.txt` (executed=40, same defect); `L1/controls/README.md:8` “The existing r79 subject mismatch and r78 legacy-ledger drift remain open”; `plans/round97_c1_replay.py:22-23` |
| 3 | `round96-standing-battery` non-deterministic; make it deterministic or keep failing-run output and require two agreeing runs; **until then register it `probe`, not `gate`** | **interim requirement done; determinism not cured.** The row is `probe` at T (one of the 44). No new battery, no two-run rule, no retained failing output. | `SKILL.md` at `f1083da6`, line 702: the `round96-standing-battery` kind cell is `probe`; `c2-base.txt:44` `MISMATCH`; `c2-tip.txt` n=0 |
| 4 | both r96 rows record self-test `none`; add a self-invocation mode over isolated fixtures with committed expected exit code and finding-id | **classification corrected; capability not invented.** Both rows are `probe` at T; their self-test cells still say `none`. No self-invocation mode was added. The C2 paragraph says a row returns to `gate` only when a successor file with a self-invocation mode is registered. | `SKILL.md` at `f1083da6`, lines 701-702 (`probe`, self-test cell `none`); `SKILL.md:773` correction paragraph |
| 5 | R96-C1 finding set: add the three missing wrong-pass states (over-report, wrong name winner, partial `values`); narrow L6 to the pinned triples (unpinned numpy; W-2) | **partial.** The L6 narrowing is applied to the new r97 instrument: L6 compares `TOOL_SHA`, `CASE_TABLE_SHA`, `GRADER_SIDE` and the observation block, and `GRADER_UNPINNED` is not compared. The three merger wrong-pass states are **not** added: the r97 member is `sparql-university`, and the merger member is not re-claimed. | `plans/round97_c1_replay.py:17` (“GRADER_UNPINNED … not compared”), `:69` `RERUN_STAMPS = ("TOOL_SHA", "CASE_TABLE_SHA", "GRADER_SIDE")`; `plans/round97-cases.json` has no over-report / wrong-name-winner / partial-`values` case |
| 6 | the C commit landed bytes outside the frozen candidate-bytes table; add a pre-push byte-scope check against the F table | **carried, not claimed.** No r97 instrument or registry row implements a pre-push byte-scope check. The C1 replay's L4/L8 hash the case table and probe (instrument scope); the C2 census checks kind cells, row presence and closed scripts; neither hashes the candidate bytes (`SKILL.md`, `plans/grader-population-ledger.json`, `corpus/SOURCES.md`) against the F table. The claims' kill rule remains prose. | `plans/round97_c1_replay.py` L1–L9 docstring; grep for `candidate-bytes`/`byte-scope` over `plans/round97*` returns nothing; `plans/round-97-claims.md` kill rule |
| 7 | wave losses: MutTesterC2 and ScribeLesson were never re-run; if C2 is re-claimed, run a C2 mutation seat | **done (dispatch).** w1 dispatches `MutC2` (mutation-tester) and `ScribeLesson` (scribe); this report is the ScribeLesson output. MutC2's output is not yet in this seat's evidence. | `.ufo/waves/round-97/w1-spec.json` items `MutC2`, `ScribeLesson` (11 seats); the live roster names both |
| 8 | carried items: R95-C1 at reward scope, R95-C2 held-out false gates, round-92 items, W-4 | **carried, not claimed.** The r97 C1 reward leg is real pytest for `sparql-university` — a new instance of the method, not a disposition of the r95 member's reward-scope item. None of the four is named in the r97 claims. | `plans/round-97-claims.md` (no mention); `corpus/lessons/round-96.md` disposition table items 3/4/7 |

Notes. #3 and #4 are the two rows the r97 C2 claim says the r96 spot-check routed; the r97
correction satisfies #3's *interim* wording (“register it as a `probe`”) and corrects #4's
classification, but does not add the self-test capability #4 asks for. #5's L6 half is a new
instrument, not a repair of the reverted r96 counter; the merger finding-set half is untouched.
#1's `freeze-integrity` re-typing is a classification change, not the successor/waiver #1 asks for.

## 3. Mistakes — two mined entries

Format follows `corpus/lessons/round-96.md` §Mistakes: class · evidence · captured-by · fix. IDs
match the L1 draft's M1/M2 so integration is mechanical; the red cases are in §3.1.

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | **attribution** — a registry row's `kind` cell says `gate` while its own self-test cell says `none` and the entry script exposes no self-invocation mode | `SKILL.md` at `4992cd0e`, lines 701-702: both `round96-c1-replay` and `round96-standing-battery` are `gate`, self-test cell `none` (the battery's cell also says “**not deterministic**”). The r96 spot-check §1(c) (`round-96-verifier-spotcheck.md:32`) names both rows and the unmet PROTOCOL §Gate standard self-test clause. The r97 C2 BASE census lists both as `MISMATCH` (`c2-base.txt:43-44`, `MISMATCH_TOTAL n=44`); at T both are `probe` and `MISMATCH_TOTAL n=0` (`c2-tip.txt`). | the r96 non-author spot-check §1(c); the r97 C2 census's `MISMATCH` leg (BASE receipt) | correct only the `kind` cells (`gate`→`probe`), never the scripts (`scripts_changed=0`); the rule is “kind is a claim about the script's bytes; a gate without a self-invocation mode is a probe”; a row returns to `gate` only with a successor file that has a self-invocation mode. No claim to add self-test capability to the 44. |
| M2 | **vacuous** — a string sentinel is dispatched by type, so the sentinel itself is written as the data | `L1/dryrun/README.md:5-8`: dry run 1 used `isinstance(source, str)`; the sentinel `"solve"` is a str, so every solve-based case wrote the literal text `solve` as the query; fixed by `source != "solve"` (`plans/round97_sparql_probe.py:270`). The README re-describes the run as “12 of 18 cases `observed=P,F,E:ParseException,0`”; the failing output was overwritten by dry run 2 and the buggy bytes were never committed. | **none** — self-disclosed re-description; the failing stdout is unrecoverable, and the L1 discloses that rather than reconstructing it. The frozen dry-run-2 receipt (`probe-dryrun-2.txt`) is the only committed output. | dispatch on a non-string sentinel (e.g. `source is SOLVE` with `SOLVE = object()`), or compare the sentinel explicitly before the literal branch; keep each dry run's stdout in its own file. The current fix (`source != "solve"`) removes this collision but leaves the sentinel a string, so a future literal query equal to `"solve"` would collide again. |

### 3.1 Red cases — evidence the criteria can fail

**M2 (sentinel).** `ScribeLesson/sentinel-redgreen.txt` reconstructs the two dispatch predicates
over the **frozen** `VARIANTS` map and the **frozen** 18-case table (dispatch level, not a probe
run). Under the old `isinstance(source, str)` predicate, 13 cases stage the literal `solve`:
C01, C04–C08, C11–C16, C18 — `OLD_LEAKS n=13`. Under the fixed `source != "solve"` predicate,
`NEW_LEAKS n=0`. The criterion “no solve-based case stages the literal sentinel” is `fail` under
the old predicate and `pass` under the fixed one. The 13-case list is reproducible from the frozen
bytes; the README's “12” is not (F1).

**M1 (r96 self-test classification).** The criterion is the census's `MISMATCH` leg: a `gate` row
whose entry script has no self-invocation spelling. It fails on the real BASE population —
`MISMATCH_TOTAL n=44`, with both r96 rows named (`c2-base.txt:43-44`), `PREDICATE R97-C2 fail`,
rc 1. It fails on the P2 cell-forgery control (`CELL-CHANGED` + `MISMATCH`, rc 1,
`L1/controls/c2-cellforge.txt`) and on the census's own `base-red` fixture (`rc=1 ids=MISMATCH`).
It passes on the re-typed population (`MISMATCH_TOTAL n=0`, `PREDICATE R97-C2 pass`; the P2
positive control records `rc=0`) and on the `retype-green` fixture (`rc=0`). Independent rerun of the census `--selftest`:
`SELFTEST cases=8 failed=0`, rc 0 (`ScribeLesson/c2-selftest-rerun.txt`), including `base-red`,
`retype-green`, `row-removed`, `demoted`, `cell-changed`, `script-forged`, `prose-only`,
`duplicate`.

## 4. Findings and limits

- **F1 (minor, provenance).** The dry-run README says dry run 1 had “12 of 18 cases
  `observed=P,F,E:ParseException,0`”. The frozen case table has **13** cases whose `app` maps to
  `source == "solve"` (C01, C04–C08, C11–C16, C18), and the reconstructed old predicate leaks in
  all 13. The dry-run-1 table and stdout are not committed (the README says the output was
  overwritten by run 2), so the difference cannot be attributed to a table change; the
  re-described count does not reproduce from the frozen bytes. This does not flip R97-C1 (the
  frozen dry-run-2 receipt is 18/18 `ok=True`), but the lesson should record “12 per the L1
  re-description; 13 against the frozen table” rather than a single number, and should keep each
  dry run's output. The L1 draft's M2 currently says “12 cases failed dry run” — recommend
  qualifying it.
- **F2 (info, detector scope).** The C2 census measures a **lexical** self-invocation spelling,
  not semantic self-test quality or branch reachability (the L1 draft's M4 says the same). An
  independent case-insensitive scan of the 44 BASE scripts found 7 with a `self[-_]?test`
  substring (`ScribeLesson/c2-alt-spellings.txt`): `round36-c1-battery` (fixture string),
  `round41-c1-mutants` (usage string), `defect-ledger` (docstring/regex), `round35-hardening`
  (regex), `round46-c2` (docstring + a subprocess call to another tool's `--selftest`),
  `freeze-integrity` (a printed `SELFTEST` line), `round95-c2-counter` (`SELFTEST` constants and
  regex). None is a self-invocation mode; the other 37 contain no such substring. So the 44 is
  not a regex artifact **for these bytes**, but the detector remains a spelling proxy: a comment
  such as `# "--selftest" in sys.argv` would satisfy it, and a new script with such a comment
  would be counted as a gate. The P2 `script-forged` control shows the `SCRIPT-CHANGED` leg
  catches a change to a closed script, not a comment in a new one. The semantic check is the
  ExecC2 seat's surface; the C2 claim is correctly restricted to the frozen code-spelling
  population.
- **F3 (info).** At T the two r96 rows are `probe` but their self-test cells still say `none`;
  only the `kind` cell changed (`c2-tip.txt` `cells_changed=0` is the census's BASE-vs-REV
  non-kind check; the 44 kind changes are the correction). This is consistent with R97-C2's
  “only the 44 `kind` cells change” and with the spot-check's #4 “capability not invented”.
- **F4 (info).** Defect 6's pre-push byte-scope check is not acquired. The C1 replay's L4/L8
  hash the case table and probe; the C2 census checks kind cells, row presence and closed
  scripts. The candidate bytes are guarded by the claims' prose kill rule and the non-author
  seats, not by a gate. Carried.
- **F5 (info, coordination).** The L1's existing `corpus/lessons/round-97.md` M2 says “12 cases
  failed dry run”; see F1. The L1's disposition list matches this draft on #1–#8. The wording differs but the
  substance agrees: the L1's #5 already separates the deferred merger cases from the applied
  unpinned-stamp lesson (this draft's **partial**), and its #3 already says the nondeterminism
  is not cured (this draft's **interim only**).
- **F6 (info).** The r97 harm check confirms the r79 standing red at the candidate
  (`DEFECT SUBJECT-MISMATCH mteb-retrieve`, `PREDICATE R79-C1 fail`, rc 1) while the ledger grows
  40→41; the r90–r95 absolute pins are not in the r97 harm population. This is the evidence for
  #2's “carried” disposition, not a new finding.
- **F7 (info, receipt completeness).** The official `L1/c2-tip.txt` ends at
  `PREDICATE R97-C2 pass` and does not record the process exit code, although the claims' frozen
  predicate includes “exit 0”; `L1/c1-tip.txt` has the same shape. The exit is not in doubt — the
  P2 positive control records `rc=0` (`L1/controls/c2-positive.txt`) and the census `--selftest`
  returns rc 0 — but the official receipts are one line short of self-contained. The r96 lesson's
  M4 made the same point about rc stamps; the fix is to write `cmd; echo rc=$?` on its own line.

**Verdict (this seat's scope).** The Gate table is integration-ready: 9/9 rows verify against the
captured bytes, and the criterion has a red case. The eight r96 routed defects are dispositioned
from observed r97 bytes: #1, #2, #6, #8 carried; #3 interim only; #4 classification corrected,
capability not invented; #5 partial (L6 narrowing applied to the new instrument, merger
finding-set not added); #7 dispatched. Both mined mistakes have red cases. No finding here flips
R97-C1 or R97-C2; F1 is a minor provenance gap in the lesson's own dry-run-1 count (12 vs 13),
not a claim defect.

## 5. Provenance and receipts

- `ScribeLesson/verify_gate_rows.py` — the row verifier (sha256, size, cited line, quote, word
  count); `gate-rows.txt` (real rows, 0 defects, rc 0); `gate-rows-mutated.txt` (scratch mutated
  copy, 3 defects, rc 1); `gate-rows-cells.txt` (full 11-cell rows).
- `ScribeLesson/sentinel_redgreen.py` — dispatch-level reconstruction; `sentinel-redgreen.txt`
  (13 old leaks, 0 new).
- `ScribeLesson/c2-selftest-rerun.txt` — independent `--selftest` run, 8/8 cases, rc 0.
- `ScribeLesson/c2-alt-spellings.txt` — case-insensitive `self[-_]?test` scan of the 44 BASE
  scripts (7 hits, all prose/fixture/regex/other-tool).
- `ScribeLesson/commands.txt`, `ScribeLesson/sha256sums.txt` — exact commands and receipt hashes.
- Cited lane receipts (not copied): `L1/c2-base.txt`, `L1/c2-tip.txt`, `L1/c1-tip.txt`,
  `L1/dryrun/README.md`, `L1/dryrun/probe-dryrun-2.txt`, `L1/controls/README.md`,
  `L1/controls/c2-*.txt`, `L1/controls/harm-pre-freeze/b82b4c75/r79c1.txt`,
  `L1/capture-sha.txt`, `L1/anchor-tip.txt`, `L1/census-start.txt`, `L1/census-end.txt`,
  `corpus/evidence/round97/sparql-probe.txt`, `plans/round97_c1_replay.py`,
  `plans/round97_sparql_probe.py`, `plans/round97_gate_selftest_census.py`,
  `plans/round-97-claims.md`, `corpus/lessons/round-96-verifier-spotcheck.md`,
  `corpus/lessons/round-96.md`.

## 6. Out of scope / not claimed

- No production edits, no commits, no corpus edits, no task calls; only this report and the
  receipts under `.ufo/waves/round-97/w1/ScribeLesson/`.
- The C1 replay and the full C2 census were not re-run; their official receipts are cited. The
  only executions here are the row verifier (read-only over captured bytes), the dispatch-level
  sentinel reconstruction (imports the frozen `VARIANTS`; no probe run), the census `--selftest`
  (isolated fixtures under scratch), and a read-only `git show` substring scan of the 44 BASE
  scripts.
- Live HTTP re-open of S317–S325 is the ScoutSources seat's surface; this draft verifies the
  captured bytes at T. The capture's own provenance is `L1/capture-sha.txt` (all HTTP 200 at
  2026-11-06T01:01:20-03:00).
- The eight r96 routed defects are dispositioned as observed; none was repaired. M1's fix is the
  R97-C2 kind-cell correction; M2's fix is the r97 probe's predicate change. No new instrument
  was written.

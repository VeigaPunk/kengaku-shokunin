# Round-38 wave-2 → round-39 dispositions

Seat `R39R38Integrate` (scribe), kengaku round 39 wave 1, 2026-10-26. Read-only: no lane file, index, jj state
or fleet-root file was written; this file lives only under `.ufo/waves/round-39/build/R39R38Integrate/`.

Basis: every report under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/falsify/*.md`,
the closure's routed items (`corpus/lessons/round-38-verifier-spotcheck.md` §5, R1–R7), and the round-39 wave-1
item roster (`.ufo/waves/round-39/build-spec.json`, 36 seats). No instrument was re-run for this map; each row
rests on the report's own text plus the file/line it cites.

## 0. Coverage, method, counting convention

| check | command | observed |
|---|---|---|
| reports present | `find . -maxdepth 1 -type f -name '*.md' \| wc -l` in the falsify dir | `34` |
| seat dirs present | `find . -maxdepth 1 -mindepth 1 -type d \| wc -l` | `34` |
| seat dirs with no `.md` | `for d in $(find . -maxdepth 1 -mindepth 1 -type d -printf '%f\n'); do [ -f "$d.md" ] \|\| echo NO-MD: $d; done` | empty output — **0** |
| R1 commit half | `git ls-files .ufo/waves/round-38/falsify \| wc -l`; `git log -1 --format='%h %cI %s' -- .ufo/waves/round-38/falsify/` | `428` files; `ef2fba0 2026-10-26T03:37:53-03:00 round-38: wave-2 reports and results (34/34), outcome appended to lesson` |
| `falsify.ready.dispatched` | `git ls-files .ufo/waves/round-38/falsify.ready.dispatched` | tracked (`.ufo/waves/round-38/falsify.ready.dispatched`) |
| reports tracked | `git ls-tree -r --name-only HEAD .ufo/waves/round-38/falsify \| grep -c '\.md$'` | `37` (34 reports + `F38CritSkipControls/filler-entry-tb2-build-pmars-grader.md`, `F38EntryQuotes/receipts.md`, `F38RevLesson/receipts.md`) |
| uncommitted r38 wave-2 output | `git status --porcelain -- .ufo/waves/round-38` | empty |
| reports the closure read | closure §header (`.ufo/waves/round-38/falsify` snapshot at 2026-10-26T06:21Z = 03:21 -03) | 14 named seats — the other **20** landed between that snapshot and `ef2fba0` |
| r38 scratch (R6 clause) | `du -sh /fast/scratch/hyaku/kengaku-r38`; `ls -A /fast/scratch/hyaku/kengaku-r38 \| wc -l` | `0`, `0` — the directory survives empty; the 22 seat dirs the scout owed are gone |

**Counting convention (stated so the numbers are auditable).** *Finding* = an item a report itself places under
`Findings` / `Defects` / `Residual(s)` / `Observations` / `Disputes` / `Survivors` / `Limit reported` and that
requires a decision (fix, route, limit, or a recorded no-action). Items presented only as confirmations
("held", "no defect", "no counterexample", "agrees") are *not* counted; where a report numbers a confirmation
among its findings, it is listed in the per-report inventory as a confirmation instead:
`F38C1RerunPy313` F5, `F38ConnClaims` #1, `F38CritN21` C1/C2, `F38MutDirection` #1, `F38MutC2Counter` #1/#4,
`F38XMutRerunMain` #1/#5, `F38C2Rerun` #5, `F38XCrit*`-style "attacked and cleared" sections. Reports that
found nothing are kept as rows with `0` so the map is exhaustive.

**Disposition codes.** `R39:<ITEM>` = decided this round by a round-39 wave-1 seat (the item drafts or measures;
the L1 integrates — no lane file is written by these seats). `R40` = routed to round 40, no round-39 item owns it.
`LIMIT` = record only; the property is a limit of a frozen instrument or an append-only document. `NONE` = no
action, reason given. `DONE` = already satisfied.

## 1. Counts

| quantity | value |
|---|---|
| reports mapped | 34 |
| seat dirs without a `.md` | 0 |
| findings | 97 |
| — `R39:<ITEM>` (decided by a wave-1 item) | 21 |
| — `R40` (routed to round 40) | 58 |
| — `LIMIT` (record only) | 9 |
| — `NONE` (no action, reason) | 9 |
| findings from the 14 reports the closure read | 36 |
| findings from the 20 reports that landed after the closure snapshot | 61 |

By routed group: R1 1 meta-row (DONE, 0 findings) · R2 30 · R3 3 · R4 4 · R5 8 · R6 17 · R8 35.
R8 is an explicit extension: the closure derived R1–R7 from 14 reports, so 35 findings from the 20 late reports
had no routed item. They are grouped by report there rather than forced into R2–R6.

Round-39 items that carry dispositions: `R39BatP1`, `R39BatP3`, `R39BatP7`, `R39BatD5`, `R39CritC1Counter`,
`R39CritC1Equiv`, `R39AdvErrata`, `R39DirCheckLeg`, `R39LessonErrata`, `R39OrderGate`, `R39RecheckFix`,
`R39AnchorUnion`, `R39LedgerProvenance`, `R39RevCounters`, `R39RevFreeze`, `R39CritSkipC2`, `R39CritProbe`,
`R39SentinelProbe`, `R39MutC2Counter`.

## 2. R1 — wave-2 outputs uncommitted and unintegrated

| report | finding | disposition | owner / reason |
|---|---|---|---|
| (all 34) | wave-2 tree uncommitted; findings unintegrated | **DONE** | committed `ef2fba0` (34/34 + `falsify.ready.dispatched`, 428 files); integration = this map (`R39R38Integrate`) |

Residual of R1, not a finding: 20 of the 34 reports postdate the closure's read snapshot, so the closure's R2–R6
were written without them. Their 61 findings are dispositioned below (R2/R6 where the theme matches, R8 otherwise).

## 3. R2 — C1 re-freeze (N21 as mirror, extra survivors, out-of-process batteries, `adv`/direction wording)

| report | finding | disposition | owner / reason |
|---|---|---|---|
| F38XMutP | X01 — P1 checks only the first pinned instrument | `R39:R39BatP1` | battery39 module for M02 |
| F38XMutP | X05 — P3 accepts a quote one word above the range | `R39:R39BatP3` | battery39 module for M03 |
| F38XMutP | X15 — P7 tolerates a second `source:` line for one sid | `R39:R39BatP7` | battery39 module for M04 |
| F38XMutP | X06 withdrawn — observationally equivalent, reported as a limit | `LIMIT` | round-38 discipline: shown equivalent, kept out of the list |
| F38CritBatE | D1 — N11 `adv` ("a recheck line must carry a value") overstates the gate | `R39:R39AdvErrata` | erratum line; reword is round-40 re-freeze |
| F38CritBatE | D2 — N09 `adv` credits "distinct" words the gate does not enforce | `R39:R39AdvErrata` | same |
| F38MutDirection | #2 — the mislabel signal is a single path; m1, m2 survive | `R39:R39DirCheckLeg` | redundant leg drafted this round |
| F38MutDirection | #3 — UNWITNESSED class untested; m3 equivalent on the landed input | `R40` | needs a fixture family, not a wording fix |
| F38MutDirection | #4 — a crashed run exits 1, the same code as a detection | `R40` | exit-code contract; minor |
| F38CritN21 | D1 — "makes D5 stricter on every input" is false (66% identical) | `R40` | lesson/`QUALITY.md` Q29 wording; no wave-1 item owns it |
| F38CritN21 | D2 — Q29's check cannot run at freeze; freeze list held the polarity contrast | `R39:R39CritC1Equiv` | pre-integration Q29 re-run is this round's check |
| F38C1Rerun | instrument margin — MAIN attribution ignores the direction cell; direction check vacuous for N17/N18 | `R40` | frozen MUTANT list; wording/rule at next freeze |
| F38CritBatF | D1 — `PINS total=14` does not bind `plans/battery38/*.py` (green over an edited fixture) | `R40` | pin completeness needs a new freeze |
| F38CritBatF | D2 — "every input that exists at the freeze" false; 3 unpinned lane data files; a moved source line is a traceback, not `SETUP` | `R40` | same, plus a builder-level `SETUP` line |
| F38CritBatD | §5 — N03's "every quote" half undemonstrated (X1/X4 survive); new fixture would reopen C1 | `LIMIT` | breadth limit; priced, not applied |
| F38RevBatA | residual 1 — the token scan cannot see `sys.argv` (dev flags reachable token-free) | `R40` | harness token pair, false-positive cost |
| F38RevBatA | residual 2 — a fixture mutating `ctx.spec` in place poisons later fixtures | `R39:R39RevCounters` | verify the child-process contract isolates it |
| F38RevBatB | residual 1 — the silence rule does not require the mutant rc to flip to 0 | `R40` | counter rule; frozen |
| F38RevBatB | residual 2 — battery bytes are not pinned | `R40` | duplicate root of `F38CritBatF` D1 |
| F38RevBatC | obs 1 — `p3m` sits on both floors at once (also kills the Y3 class) | `LIMIT` | attribution by name is correct; no change |
| F38RevBatC | obs 2 — the 7-row counterpart is impossible by the module guard; battery37 pins that side | `NONE` | coverage is held elsewhere |
| F38RevBatC | obs 3 — N07's second branch is demonstrated only on the first row | `R40` | fixture coverage |
| F38XMutRerunMain | #2 — the ATTRIBUTED rule has an exit-code blind spot (X07, X10 survive) | `R40` | counter rule; `R39CritC1Counter` probes the rc legs this round |
| F38XMutRerunMain | #3 — X04 confirms the freeze's B4 exclusion (P10 rerun arm unreachable) | `LIMIT` | documented limit, not a gap |
| F38XMutRerunMain | #4 — X15: D5's tag-strip half is demonstrated by no fixture | `R39:R39BatD5` | battery39 module for M07 (markup inside the quote span) |
| F38XMutRerunMain | #6 — `declared := observed` makes the declared half vacuous for round-36 modules | `R40` | rule tightening |
| F38C1RerunPy313 | F1 — the landing receipt is one commit behind the tip it is cited for | `NONE` | closure §1 verified the measurement transfers; numbers re-measured byte-equal |
| F38C1RerunPy313 | F2 — N13/N14/N15 never test the counter's interpreter (P10 runs a uv child) | `LIMIT` | scope of that report; constancy expected, not evidence |
| F38C1RerunPy313 | F3 — both artifacts assume a UTF-8 default; `LC_ALL=C PYTHONUTF8=0` fails closed | `R40` | `encoding=` on the next touch |
| F38C1RerunPy313 | F4 — `killed=21` needs `uv` on PATH (18 without); fails closed | `R40` | host dependency; fix = pin the probe interpreter |

## 4. R3 — order-of-operations recurrence

| report | finding | disposition | owner / reason |
|---|---|---|---|
| F38RevLesson | Defect 1 — lesson row 2 quotes only half of the round-37 fix (drops the rule-forward) | `R39:R39LessonErrata` | appended `## Errata (round 39)` drafted |
| F38RevLesson | Defect 2 — `census-before.txt` (exit 0) listed inside "all red" | `R39:R39LessonErrata` | same |
| F38C2Rerun | #4 — order-of-operations is not falsifiable from the tree | `R39:R39OrderGate` | the history-reading gate is this round's check (`R39QualityQ30` drafts the criterion) |

## 5. R4 — recheck command reds as written

| report | finding | disposition | owner / reason |
|---|---|---|---|
| F38ReopenRows | F38R-2 — `sha256sum -c …/SHA256SUMS` reds from the lane root (bare basenames); template sits in the r35–r38 entries | `R39:R39RecheckFix` | corrected line + errata drafted |
| F38ReopenRows | F38R-3 — the TB2.1 comparison is unpinned | `R39:R39RecheckFix` | pin the ref and digests |
| F38ReopenRows | F38R-1 — nothing checks a SOURCES row's quote (a forged row quote stays green) | `R40` | needs a V3 extension or a gate clause; folding into P3 would move admitted counts |
| F38ReopenRows | F38R-4 — the `pmars-dir-elsewhere` contest is a TB2.0-text artifact | `R40` | one clause in the entry |

## 6. R5 — D3/D4 residuals

| report | finding | disposition | owner / reason |
|---|---|---|---|
| F38AnchorFix | F1 — the anchor binding unions digests over every locator a row names | `R39:R39AnchorUnion` | fixed copy + red-before drafted |
| F38AnchorFix | F2 — removing a digest claim silences the check (verifier of claims, not of presence) | `LIMIT` | tool scope |
| F38AnchorFix | F3 — `QUALITY.md` Q26 still advertises the hole the tool closed | `R40` | Q26 amendment; append-only, no wave-1 item owns Q26 |
| F38LedgerTip | F1 — `--lane` reads an existing stale `refs/heads/master` with no provenance line | `R39:R39LedgerProvenance` | refuse + line printed |
| F38LedgerTip | F2 — a refusal raised mid-ledger prints ledger statements incl. a false `agree=NO` | `R39:R39LedgerProvenance` | refusal ordering in the same draft |
| F38CritNoHarmDiff | R1 — the stale round-37 map row (`enforced`) survives; only prose corrects it | `LIMIT` | append-only norm; read the erratum, not the row |
| F38CritNoHarmDiff | R2 — "no-harm at the landing tip" was measured three commits before it | `NONE` | closure §1 verified the input set is untouched across those commits |
| F38CritNoHarmDiff | R3 — the C1 source arithmetic (`13+1+6≠22`) is not restated in SCORECARD | `R40` | SCORECARD errata line |

## 7. R6 — carried (C2 filler, `R36CritScope` wording, scratch) and the operability family

| report | finding | disposition | owner / reason |
|---|---|---|---|
| F38CritSkipControls | control (a) — an informed filler entry prints the identical C2 receipt (`checks=7 defects=0`) | `R40` | entry-derivation check (a V8) needed; `R39CritSkipC2` re-tests the same shape on the round-39 counter |
| F38CritSkipControls | control (b′) — a module patching `attributed` in-process reaches `PREDICATE C1 pass` with no kill | `R39:R39CritC1Counter` | round-39 loads/builds fixtures out of process; the attack seat tests it |
| F38SentinelBattery | F1 (HIGH) — both predicates need network or a warm `~/.cache/uv`; undeclared host dependency | `R40` | pin the probe interpreter in the spec |
| F38SentinelBattery | F2 (HIGH) — the kills are carried by unpinned `plans/battery38/*.py` | `R40` | pin the fixtures |
| F38SentinelBattery | F3 (HIGH) — fixtures are arbitrary in-process code; both guards one-line bypassable | `R39:R39CritC1Counter` | out-of-process child build is the round-39 mitigation; verify it |
| F38SentinelBattery | F4 (MED) — probe execution escapes the seat's scratch and outlives the gate | `R40` | probe honours `--work`/`TMPDIR`; `R39SentinelProbe` reviews the new probe |
| F38SentinelBattery | F5 (MED) — C2's V6 executes unpinned host state at a hardcoded absolute path | `R40` | pin or vendor the census script |
| F38SentinelBattery | F6 (LOW) — `uv` and `git` are PATH-resolved inside the verified path | `R40` | second leg of F1 |
| F38SentinelBattery | F7 (LOW) — a missing `--work` parent dies with an uncaught traceback | `R40` | refuse with a diagnostic (family of 5 below) |
| F38C1Rerun | §8 — `--work DIR` crashes when `DIR` does not exist | `R40` | same family; create-or-refuse |
| F38C2Rerun | #3 — the probe's `--work` parent must already exist | `R40` | same family |
| F38NoHarmSweep | O-3 — an absent `--work` path exits 1, not 2 (carried from round-37 N2) | `R40` | same family; against SKILL's `2` = usage/refusal |
| F38NoHarmSweep | O-1 — the shipped spec has `receipt_sha256: null`, so the documented gate entry is red at P2 | `R39:R39RevFreeze` | **recurrence checked this round**: `plans/pkg-spec-r39.json` also ships `null` (see report) |
| F38NoHarmSweep | O-2 — the `round38-c1-mutants` registry row maps `0` to a state unreachable at the tip and stays silent | `R40` | SKILL registry errata (precedent: the anchor-check addendum) |
| F38NoHarmSweep | O-4 — `gate_timing_check.py --selftest` is not byte-stable across commits | `LIMIT` | verdicts stable; no receipt byte-compares it |
| F38NoHarmSweep | O-5 — the fixed `anchor_digest_check.py` has no pin at its new digest | `R40` | pin it when `R39AnchorUnion`'s copy lands |
| F38ScoutMisroot | 22 r38 scratch dirs (20 G) owed at the sweep | `NONE` | now empty (`du -sh` = 0; 0 entries); round-39 seats use `kengaku-r39` with `trap rm -rf` |

## 8. R8 — extension: findings from the 20 reports the closure snapshot did not contain

### 8.1 C1/C2 counters and probes

| report | finding | disposition | owner / reason |
|---|---|---|---|
| F38C2Rerun | #1 — V6 depends on an unpinned file outside the clone (absolute fleet-root path) | `R40` | carried property (same constant in the r37 counter); `R39RevCounters` records it |
| F38C2Rerun | #2 — V4's mismatch-naming branch is vacuous at the tip (`0/0`) | `LIMIT` | real branch (tamper G fires), unexercised by the landing datum |
| F38C2Rerun | #5 — P10 closes the hand-typed-receipt gap in practice, not by inspection | `NONE` | confirmation of the design statement |
| F38MutC2Counter | #2 — M4 (drop `--rerun`) is killable only by a fixture that did not exist at freeze | `R40` | `R39MutC2Counter` tests the round-39 counter's own mutants |
| F38MutC2Counter | #3 — M2 and M5 are genuine survivors (shielded by P10 / P5+P9) | `R40` | defense-in-depth clauses, untestable at predicate level |
| F38MutC2Counter | #5 — V3's own-row pin is the sole catcher of a cross-bound anchor | `R40` | cheap fixtures the freeze did not include |

### 8.2 Entry prose, prose apparatus and coverage counts

| report | finding | disposition | owner / reason |
|---|---|---|---|
| F38CritOverclaim | O1 (HIGH) — "a fabricated non-ELF artefact cannot pass" is false; a PATH-planted `ldd` passes | `R40` | entry sentence + SKILL row; no wave-1 item edits the r38 entry |
| F38CritOverclaim | O2 — the seven "derived" labels are four statistics; one "not vacuous" reading contradicted | `R40` | add a fail-side witness column |
| F38CritOverclaim | O3 — the SKILL decision table mis-states 3 of its 13 mechanisms | `R40` | SKILL errata |
| F38CritOverclaim | O4 — "first probed instance" drops TB2.1 PR #118 (reward-hacking verdict) | `R40` | novelty clause qualification |
| F38CritOverclaim | O5 — "89 carry `tests/test.sh`" has no in-repo count | `R40` | PROVINCE wording ("89 task directories at the pin") |
| F38CritOverclaim | O6 — two count/wording defects in the README index row and summary prose | `R40` | README errata |
| F38CritOverclaim | O7 — "gate behaviours attributed 21/22" precedes the review it says it needs | `R39:R39AdvErrata` | erratum line for the round-38 SCORECARD title |
| F38EntryQuotes | F1 — "fixes four of the seven labels" contradicts the doc's own all-cases rule | `R40` | entry errata |
| F38EntryQuotes | F2 — "ignores its `argv`" is wrong: the canned program branches on argv, not warrior args | `R40` | entry errata |
| F38CritTags | the frozen `violates=` tags are self-referential under V7; strongest alternative priced at 2 rows / 3 labels | `R40` | tagging statement + alternative disclosure; `R39CritProbe` attacks the round-39 tags |
| F38CritSeparability | A — the `## Separability` read-set sentence is false (fixtures copy `corpus/**`; P8 couples them) | `R40` | claims errata (adversarial only, no laundering path) |
| F38CritSeparability | B — C2's V2/P9 depends on any untracked file, including C1's artifacts | `R40` | C2 limits sentence |
| F38RevQuality | #1 — §A.3 misattributes `trailing-newlines` to `:122-124` | `R40` | erratum apparatus |
| F38RevQuality | #2 — §B F8's anchor `:222-224` misses its clause by one line (`:225`) | `R40` | same class the erratum itself fixed for F5 |
| F38ConnClaims | #2 — the frozen §C1 prose arithmetic sums to 20 ≠ 22 | `NONE` | disclosed and mined in the round-38 lesson; frozen file correctly left frozen |
| F38ConnClaims | #3 — docs cite `d93b7d68` for a measurement the wave was dispatched at `8c7422d` | `NONE` | closure §1 verified the transfer; `measure-tip2.txt` re-confirms |
| F38ConnFrontier | obs a — the round-35 §Frontier bullet still reads "executes `test.sh`" | `NONE` | dated history sub-bullet; convention keeps it |
| F38ConnFrontier | obs b — no TB2 entry names a sibling lane | `NONE` | adjacency is registered in `PROVINCE.md` |

### 8.3 Self-report calibration

| report | finding | disposition | owner / reason |
|---|---|---|---|
| F38RevScorecard | dispute 1 — the C2 "fourth grader class" framing is unresolved in-lane | `R40` | lesson note; SCORECARD/README/PROVINCE are mutually consistent |
| F38RevScorecard | dispute 2 — V6's absolute census path contradicts "measured on a clean clone" | `R40` | carried property (identical constant in r37); duplicate of C2Rerun #1 |
| F38RevScorecard | dispute 3 — the claims' "V2's P10 … makes such a receipt red" is imprecise | `R40` | prereg wording |

### 8.4 `plans/tip_receipts.py` (registered capability)

| report | finding | disposition | owner / reason |
|---|---|---|---|
| F38TipReceipts | F1 — a new runnable probe receipt is labelled `no-committed-re-run-command`, gate green | `R40` | population/label rule |
| F38TipReceipts | F2 — 176 of 200 committed `corpus/evidence/**` receipts are outside the population | `R40` | scope rule must be stated |
| F38TipReceipts | F3 — an absent dependency turns a receipt into an unverified skip counted as `compared` | `R40` | skip must not be `compared` |
| F38TipReceipts | F4 — a mistyped filter is a green gate that checked nothing | `R40` | empty population must be red |
| F38TipReceipts | F5 — the verdict depends on the filter, not on the tip | `R40` | same root as F4 |
| F38TipReceipts | F6 — an uncommitted edit of a receipt is invisible (`git show HEAD:`) | `R40` | state the blob-of-record limit |
| F38TipReceipts | F7 — the "clean clone" is a `--shared` clone | `R40` | state or use `--no-hardlinks` |
| F38TipReceipts | F8 — `doc=` provenance is a cross-file substring join | `R40` | tighten the join |

## 9. Per-report inventory

Role/axes from `.ufo/waves/round-38/falsify/swarm-registry.json`; verdict token is the report's own terminal
line; digest is the first 16 hex of `sha256sum <report>`.

| # | report | role | axes | verdict | findings | groups |
|---|---|---|---|---|---|---|
| 1 | F38AnchorFix | executor | calibration, operability | `anchor-cross-row-caught` | 3 | R5 |
| 2 | F38C1Rerun | executor | calibration | `c1-rerun-fail-killed-21/22` | 2 | R2 |
| 3 | F38C1RerunPy313 | executor | calibration, operability | `c1-interpreters-same` | 4 | R2 |
| 4 | F38C2Rerun | executor | coverage | `c2-rerun-pass-probe-byte-equal-yes` | 5 | R3, R6, R8 |
| 5 | F38ConnClaims | connector | calibration | `cross-doc-drift-0 …` | 2 | R8 |
| 6 | F38ConnFrontier | connector | coverage, adjacency | `frontier-ok` | 2 | R8 |
| 7 | F38CritBatD | critic | calibration | `battery-p4a-p4b-attack-0-defects` | 1 | R2 |
| 8 | F38CritBatE | critic | calibration | `battery-p6m-p7m-attack-2-defects` | 2 | R2 |
| 9 | F38CritBatF | critic | calibration | `battery-d4m-d5m-attack-2-defects` | 2 | R2 |
| 10 | F38CritN21 | critic | calibration | `n21-silence-unreachable` | 2 | R2 |
| 11 | F38CritNoHarmDiff | critic | calibration | `no-harm-removed-lines-0` | 3 | R5 |
| 12 | F38CritOverclaim | critic | calibration, coverage | `overclaims-7` | 7 | R8 (1 → R39) |
| 13 | F38CritSeparability | critic | calibration | `separable-yes` | 2 | R8 |
| 14 | F38CritSkipControls | critic | calibration | `skip-controls-c1-red-c2-green` | 2 | R6 |
| 15 | F38CritTags | critic | coverage, calibration | `tags-contestable-24-labels-change-2` | 1 | R8 |
| 16 | F38EntryQuotes | reviewer | depth, coverage | `entry-quotes-28/28-claims-unsupported-2` | 2 | R8 |
| 17 | F38IndepProbe | critic | coverage | `indep-probe-agree-8/8` | 0 | — |
| 18 | F38LedgerTip | executor | operability | `ledger-tip-detached-ok` | 2 | R5 |
| 19 | F38MapV7Control | mutation-tester | calibration, quality | `v7-controls-5/5` | 0 | — |
| 20 | F38MutC2Counter | mutation-tester | calibration | `c2-counter-mutants-3/5` | 3 | R8 |
| 21 | F38MutDirection | mutation-tester | calibration | `direction-check-mutants-1/3` | 3 | R2 |
| 22 | F38NoHarmSweep | executor | operability, freshness | `no-harm-31/31-new-red-0` | 5 | R6 |
| 23 | F38ReopenRows | critic | freshness, coverage | `rows-2/2-quotes-2/2` | 4 | R4 |
| 24 | F38RevBatA | reviewer | calibration | `battery-b1run-mainx-attack-0-defects` | 2 | R2 |
| 25 | F38RevBatB | reviewer | calibration | `battery-p10a-p10b-attack-0-defects` | 2 | R2 |
| 26 | F38RevBatC | reviewer | calibration | `battery-p3m-p5m-attack-0-defects` | 3 | R2 |
| 27 | F38RevLesson | reviewer | calibration | `lesson-2-defects` | 2 | R3 |
| 28 | F38RevQuality | reviewer | calibration, quality | `quality-2-defects` | 2 | R8 |
| 29 | F38RevScorecard | reviewer | calibration | `self-report-mismatches-0` | 3 | R8 |
| 30 | F38ScoutMisroot | scout | adjacency | `misroot-0-scratch-leftovers-22` | 1 | R6 |
| 31 | F38SentinelBattery | sentinel | operability | `sentinel-7-findings` | 7 | R6 |
| 32 | F38TipReceipts | executor | operability, freshness | `tip-receipts-4/24-tamper-caught` | 8 | R8 |
| 33 | F38XMutP | mutation-tester | calibration | `xmut-p-killed-17/20` | 4 | R2 |
| 34 | F38XMutRerunMain | mutation-tester | calibration | `xmut-rest-killed-12/16` | 4 | R2 |

## 10. Limits of this map

- No instrument was executed for this document. Every disposition rests on report text plus the cited
  file:line; where a report's own claim is contested by another report (e.g. `F38CritBatF` D1 vs
  `F38RevBatB` residual 2) the two rows are kept separate and both routed, not merged into one verdict.
- `R39:<ITEM>` means the round-39 wave-1 item addresses the finding *as a draft or a measurement*; these seats
  write only under `.ufo/waves/round-39/build/`. Whether the L1 lands the draft is outside this map.
- The 97 count is a coding of each report's own itemisation under the convention in §0. Counting every numbered
  item including the confirmations named there yields a larger number; the difference is exactly those named
  confirmations, listed report by report in §0.
- Scope excluded by the task: round-38 wave-1 build reports (`.ufo/waves/round-38/build/*.md`) and the closure
  document's own findings (§1–§4), except where a routed item cites them.

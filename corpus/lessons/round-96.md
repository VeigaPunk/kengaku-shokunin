Author: kengaku (L1 KengakuR96, attempt 1, through C and the receipts at T; L1 KengakuR96a2, attempt 2, integration)

# Kengaku round 96 — lesson

Lane `kengaku-shokunin`, branch `master`. Base `45740a61` (round 95 closed, lane tip at round
start); P0 mechanism predictions, capture, census start, standing-counter BASE receipts `ff6765a6`;
instruments P1 `cea469bd`; battery grow leg P1b `e8a80c0e`; pre-freeze controls P2 `a3b57321`;
frozen claims F `be3ff962` (`plans/round-96-claims.md`, 11-row `frozen-instruments` table, 7-row
`candidate-bytes` table); official receipt, ledger flip, mteb-retrieve subject re-pin, R96-C2
counter repairs, SKILL class cells and SOURCES C `09717e49` = measured tip T; receipts at T
`7b7a17d3` (C1) and `599c1fa1` (C2); R96-C2 repair bytes reverted after T `3f300cbd`. Wave
evidence: `.ufo/waves/round-96/w1/` (13 seats, 6 delivered) and the residual call
`.ufo/waves/round-96/r1/` (4 seats). Attempt 1's L1 died after dispatching w1
(`.ufo/watchdog.log`: `lane-dead-no-report kengaku round=96`); attempt 2 inherited every committed
byte above and the untracked w1 seat outputs, re-verified them against the seat receipts, and
discarded nothing.

## Round-95 spot-check routed defects — disposition

| # | routed defect (round-95 spot-check §6) | round-96 disposition |
|---|---|---|
| 1 | round-79 vs round-87 gate disagreement on `mteb-retrieve` `subject` | **claimed inside R96-C2** (r87 re-pin to `tb2-header` + ledger cell); reverted after T (M1): the re-pinned r87 counter fails at r87's own measured tip `10de494d` (CriticClaimsR F2). At the landing tip the disagreement is back to the BASE state (`L1a2/r79-landing.txt` `DEFECTS n=1`, `L1a2/r87-landing.txt` pass at T and at `10de494d`). Still routed |
| 2 | C1 counters' L7 pin an absolute executed total | **claimed as R96-C2** (L7 keyed to each round's BASE executed set); predicate failed at T (`GROWS 6/5`) and the bytes were reverted after T (M1). Routed to round 97 as an additive successor, never a byte-replace |
| 3 | R95-C1 at reward scope | not claimed; carried |
| 4 | R95-C2 held-out false gates | not claimed; carried |
| 5 | SP1 probe sandbox inherits host env; credential receipt | done for the round-96 probe: `--clearenv` (SentinelProbe SP-1: 4 env names inside, canary absent); wave context forbids raw env values; no seat receipt holds values (sentinel receipts print names/counts only) |
| 6 | wrong-cwd recurrence: counters refuse when cwd ≠ lane root | done for round-96 instruments: `controls/c1-wrong-cwd.txt` rc 2 `could-not-evaluate` |
| 7 | carried items (W-4, round-92, docker image) | not claimed; still open |

The round-95 spot-check §3 recorded 5/5 agree, so no discernment criterion is owed from it.

## Gate

Candidates opened this round (CORPUS rule 1). Every fetch HTTP 200 on 2026-11-05 (22:30 -03) from
raw.githubusercontent.com at terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6`
(`.ufo/waves/round-96/L1/capture-sha.txt`). Quotes and word counts were computed by the script that
wrote the rows (`len(quote.split())`). Re-opened live by the non-author ScoutSources seat: 7/7 HTTP
200, size and sha256 equal to the row, quote on the cited line, word count equal
(`.ufo/waves/round-96/w1/ScoutSources.md` §1).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S310 `multi-source-data-merger/tests/test_outputs.py` | **admit** (tier A, member replay only) | 2026-11-05, 1889 B, sha256 `a0708889…08ca5` | line 53: `if email_conflicts:` (2 words) | the three functions the fourteenth replay grades; the only value check of the conflict report is guarded (C04 under-report passes), rows 102/103 never content-checked (C06), `user_id` only compared by set (float64 passes, C07). CriticClaimsR adds three more wrong-pass states (over-report, wrong name winner, partial `values`), all `P,P,P,1` (`r1/CriticClaims/newstate2.txt`) | — |
| S311 `solution/solve.sh` | **admit** (tier A) | 2026-11-05, 4315 B, sha256 `1b3d0d50…537e1e` | line 103: `merged = all_data.sort_values('_priority').groupby('user_id').first().reset_index()` (3 words) | the positive control, run unmodified (C01); ExecImage ran it inside the real image: outputs byte-identical to the venv run | — |
| S312 `environment/Dockerfile` | **admit** (tier A, agent-side pins) | 2026-11-05, 427 B, sha256 `c95a40d3…5e4f` | line 11: `RUN pip install pandas==2.2.3 pyarrow==17.0.0` (5 words) | the agent-side venv pins; ExecImage: the image runs python 3.11.14 / pandas 2.2.3 / pyarrow 17.0.0 / numpy 2.3.4 (venv numpy 2.4.6, unpinned both sides, outputs identical) | — |
| S313 `tests/test.sh` | **admit** (tier A, grader-side pins) | 2026-11-05, 652 B, sha256 `d5a00e64…a336d1` | line 21: `-w pandas==2.3.3 \` (3 words) | runs only `test_outputs.py`; reward 1 iff pytest rc 0. ReviewerC1: real pytest 8.4.1 reward equals the harness reward bit on 17/17; the exact stack with pytest-json-ctrf 0.3.5 changes no verdict | — |
| S314 `instruction.md` | **admit** (tier A, agent-facing contract) | 2026-11-05, 1912 B, sha256 `d1d28bb6…aab944` | line 61: `- Data types are correct (user_id as integer)` (8 words) | the stated contract is stricter than the graded one (C04, C06, C07) | — |
| S315 `task.toml` | **reject** | 2026-11-05, 1107 B, sha256 `ee3964c0…31c694` | line 30: `docker_image = "alexgshaw/multi-source-data-merger:20251031"` (3 words) | REJECTED as an input: the harness runs a prebuilt image the replay never pulls. The flip was exercised by the non-author ExecImage seat (digest `sha256:8b327820…e666e`): `/data` bytes equal the capture, solve.sh outputs byte-identical, grader `P,P,P,1`. The row stays rejected as an input; the finding (venv models the image for C01) moves to knowledge | flip met; reason now: the image is a confirmation, the replay does not need it |
| S316 `README.md` | **reject** (tier B) | 2026-11-05, 2567 B, sha256 `9bf37162…4c69d6` | line 20: `- **Pre-installed tools**: pandas (2.2.3), pyarrow (17.0.0), tmux, asciinema` (9 words) | derivative summary of S312/S314 | a claim about the README's own statements |

Rows touched old → new: none (registry rows of earlier rounds unchanged; the S315 flip outcome is
recorded here, not in the row). Round-start census: `kengaku ok`, 301 rows
(`.ufo/waves/round-96/L1/census-start.txt`); round-end census: `kengaku ok`, exit 0, 308 rows
(`.ufo/waves/round-96/L1a2/census-end.txt`). Anchor gate at the landing tip `live=0 cells=0`
(`L1a2/lane-gates-landing.txt`). Assimilation: none (`merge/kengaku/` held by L0 `kengaku | round-54`).
considerthese: none taken (latest file `considerthese/2026-11-05.md`; its residual is not
implemented this round).

## Mistakes

Class · evidence pointer · captured-by · fix.

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | **a repair byte-replaced frozen instruments of closed rounds** | C `09717e49` rewrote `plans/round87_c1_replay.py` and `plans/round90..95_c1_replay.py`. Non-author seats: gate v2 at T reports r93/r94/r95 freezes broken (each round's own C1 counter; pass at BASE), `round95_c2_counter.py` W4 fail (`w1/ExecHarm.md` §3); the re-pinned r87 counter fails at r87's own measured tip `10de494d` while the old bytes pass (`r1/CriticClaims/r87-at-r87T.txt`, `r87-old-at-r87T.txt`). Revert `3f300cbd` restores the bytes (`rev=table` hashes) and r87 history, but gate v2 still reports `broken:touched-after-freeze=2` for all three (`L1a2/freeze-landing.txt`): the history touch is permanent | Q78 covers ledger rows only, not instrument paths; the claims file reclassified the seven files as "claimed work, not instruments" — a second authority the gate ignores (CriticClaimsR F4, ConnectorOverlapR CO-4) | **Q79** (below); successor counters land as new files beside the frozen ones, never as byte-replacements. Shown able to fail: `L1a2/freeze-landing.txt` rc 1 ×3 at the landing tip |
| M2 | **frozen predicate not deterministic** | official battery at T: `GROWS checked=6 tolerant=5`, `PREDICATE R96-C2 fail` (`L1/c2-tip.txt`); CriticClaimsR's run of the same bytes at the same rev: `GROWS 6/6`, `PREDICATE R96-C2 pass`, rc 0 (`r1/CriticClaims/battery-t.txt`); r91 grow passes alone and 6× parallel (`L1/diag-r91-grow/`), ConnectorOverlapR 6/6 (`r1/ConnectorOverlap/receipts/c-grow-r9*.txt`); the battery keeps no per-run output, so the failing run cannot be attributed | none: P2 ran each control once | **Q80** (below). Shown able to fail: the two committed battery receipts at T differ in their PREDICATE line |
| M3 | **a variable assigned inside a backgrounded chain used outside it** | the first C2 run at T ran with `--rev` empty: argparse `expected one argument`, rc 2 (`L1/mistakes/M3-c2-tip-empty-rev.txt`); a ledger count ran on a partial set (`L1/mistakes/M3-ledger-count-partial.txt`) | the counter's rc 2 | re-run with the assignment in the same foreground shell; the wave context carried the rule to every seat |
| M4 | **an rc stamp that records the wrong status** | every P2 `controls/c2-*.txt` ends `rc=` from `echo "fixture_rev=$(cat …) rc=$?"`: `$?` is the command substitution's status, not the battery's (`L1/controls/README.md` "Known receipt defects") | none; disclosed by the L1 before F | the PREDICATE line is the verdict; receipts must write `cmd; echo rc=$?` on their own line (the round-96 end receipts do) |
| M5 | **the candidate-bytes table omitted a repair byte** | C landed the ledger `mteb-retrieve` `subject` cell change as part of C2's repair, outside the seven-file `candidate-bytes` table (CriticClaimsR F3, `r1/CriticClaims/git-scope.txt`) | the claims file's own kill rule ("C lands bytes other than the candidate-bytes table") — read only by the non-author critic | R96-C2 is not met on that clause independently of the predicate; a candidate table lists every repair byte, cells of shared files included |
| M6 | **growth drift counted as self-assessment mismatch** | five of the "six mismatches" (r90–r94) pass at the revisions their SCORECARD rows name (`r1/CriticClaims/hist-r90.txt`, `hist-r91.txt`, `hist-r92.txt`); only r79 (the standing population gate) was a genuine standing mismatch (CriticClaimsR F5) | prompt §9 calibration rule — not applied at claim choice | a calibration population row names the revision its SCORECARD row records and is a mismatch only if the counter fails there or the row says "standing" |
| M7 | **seat scratch inside the lane / fleet root** | SentinelProbe SP-11: one probe run used `--work` inside the lane's untracked `w1/` (removed by the seat); ConnectorOverlapR CO-5: fleet-root `.pytest_cache` naming the round-96 grader tests (moved byte-exact to `.ufo/waves/round-96/L1a2/misroot/pytest_cache`, fleet copy removed, `L1a2/misroot-sweep.txt`) | the probe's lane guard scopes to the *passed* `--lane`; nothing guards pytest's rootdir | seats run pytest with `--rootdir "$S"` and `-p no:cacheprovider`; `--work` always under `$S` |
| M8 | **seats lost with the coordinating session** | 7 of 13 w1 seats left no report when the orchestrator session crashed (`w1-results.json` notes); residual call r1 re-ran 4 of them | the orchestrator note | the lost items not re-run (ExecC2Rerun, MutTesterC2, ScribeLesson) are named in the report; their partial files stay as evidence and are not counted |

## Quality criteria added

- Q79 and Q80 in `corpus/QUALITY.md` (grounded in M1 and M2).

## Wave findings (w1 delivered seats + residual r1)

| id | seat | severity | finding | route |
|---|---|---|---|---|
| W-1 | ExecC1Rerun | — | R96-C1 re-measured with fresh venvs: pass at T rc 0, fail at BASE and F rc 1; probe 3× identical; alt numpy identical | — |
| W-2 | ReviewerC1 F1 / CriticClaimsR C1-F2 | minor | L6 compares full ENV/GRADER stamps incl. unpinned numpy and CPython micro: future resolution change fails L6 with no behaviour change | round 97 |
| W-3 | ReviewerC1 | — | real pytest 8.4.1 reward = harness reward 17/17; exact test.sh stack on C01/C12 changes nothing | — |
| W-4 | ExecImage | — | real image `sha256:8b327820…`: solve.sh outputs byte-identical to the venv run, grader `P,P,P,1` | S315 flip recorded |
| W-5 | CriticClaimsR C1-F1 | major | finding set incomplete: over-report, wrong name winner, partial `values` all pass; the report is checked at one value point | round 97 (add cases) |
| W-6 | CriticClaimsR | — | C1 separable: seven counters reverted → C1 still passes (`c1-noc2.txt`); ledger flip reverted → L7 fails (`c1-noc1.txt`) | — |
| W-7 | CriticClaimsR C2-F1 / ConnectorOverlapR CO-7 | blocker (instrument) | battery nondeterministic; failed bite output discarded | M2, Q80, round 97 |
| W-8 | ExecHarm / CriticClaimsR C2-F4 / CO-4 | major | freeze-integrity r93/r94/r95 PASS → FAIL; permanent after revert | M1, Q79 |
| W-9 | CriticClaimsR C2-F2 | major | re-pinned r87 counter red at r87's own tip | M1; reverted `3f300cbd` |
| W-10 | CriticClaimsR C2-F3 | major | candidate-bytes table omits ledger subject cell | M5 |
| W-11 | CriticClaimsR C2-F5 | major | 1 genuine + 5 drift, not 6 mismatches | M6 |
| W-12 | ConnectorOverlapR CO-2 | minor | 12 bites / 6 grows use 8 distinct forgery inputs | round 97 |
| W-13 | ConnectorOverlapR CO-3 | minor | set-keyed L7 accepts any superset; r79 catches the ledger-only grow forgery but the battery never composes them | round 97 (proposed leg) |
| W-14 | ConnectorOverlapR CO-6 | major | r80/r81 still pin absolute totals 24/26 behind worktree-only legs | round 97 |
| W-15 | SentinelProbe SP-7 / SP-9 / SP-10 | minor / info | whole uv interpreter store bound; host hostname visible; tmpfs root writable inside the namespace | round 97 |
| W-16 | ScoutSources | — | 7/7 rows re-open; upstream `main` identical to the pin | — |
| W-17 | ExecHarm | — | grader.py, anchor line, R68-C1, R91-F1 PASS → PASS BASE → T; census rc 0 | — |
| W-18 | ConnectorOverlapR CO-1 | — | no sibling replays TB2 graders; PROVINCE holds | — |
| W-19 | ReviewerC2R C2-1 | blocker (instrument) | second independent battery run at T passes 6/6 (`r1/ReviewerC2/battery-T-at-T.txt`); hand grow fixture `defects=0`; 12/12 concurrent r91 grow runs pass (`load-12x-r91-grow.txt`): the official fail is not reproduced | M2, Q80 |
| W-20 | ReviewerC2R C2-5 | major | battery GREEN rule satisfiable by a non-evaluating stub in the 8 bite-free counters (r79, r83–r89): a stub `round83_c1_replay.py` passes the whole predicate (`forgery-F2-fake-r83.txt`) | round 97 |
| W-21 | ReviewerC2R C2-6 / C2-8 | minor | a two-member L7 passes all three bites (`forgery-F3-two-member-r90.txt`); r90 keeps `MEMBERS_TOTAL=88`, so one new ledger row turns it red | round 97 |
| W-22 | MutTesterC1R | minor | `plans/round96_c1_replay.py`: 43 mutants, 28 killed, 15 survive, all redundant with another leg (L5 subsumed by L4+L6; TARGET line not predicate-bearing; tampered capture gives rc 2, not 1; probe timeout under load gives L6 fail) — no verdict-flipping defect (`r1/MutTesterC1.md`) | round 97 |

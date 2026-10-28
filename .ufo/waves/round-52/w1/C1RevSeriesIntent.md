# C1RevSeriesIntent — reverse-engineering the round-35..46 TB2 hand-reading series (kengaku r52, wave 1, 2026-10-28)

Seat: revenger, leaf member (no subagent dispatch). Read-only over the lane; no lane file was
modified; no git/jj mutation anywhere; no tool installed or upgraded (pacman guard respected —
nothing was needed). Base tip context `30801b47`; frozen claims `plans/round-52-claims.md` read in
full, **including the appended Amendment A1** (classification unit moved from grader file to test
functions, disclosed as written after the L1 saw population marker statistics). Lane bounds:
`ls corpus/knowledge/tb2-*-grader.md | wc -l` → **12**, matching the claims' corroborating count.

## 1. What the series is

Rounds 35–46 of this lane each captured, statically read, and **executed** one Terminal-Bench 2.0
task grader at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, producing one knowledge entry
(`corpus/knowledge/tb2-*-grader.md`), one frozen probe (`plans/*_probe.py`), one receipt
(`corpus/evidence/round*/…-probe.txt`), one §Frontier sub-bullet, and one falsifier block. Round →
task, with the receipt line I extracted today:

| round | task | receipt | receipt line (today, lane tree) |
|---|---|---|---|
| 35 | protein-assembly | `corpus/evidence/round35/tb2-grader-probe.txt` | `cases=18 observed_pass=5 observed_fail=13 mismatches=0` |
| 36 | regex-log | `corpus/evidence/round36/regex-log-probe.txt` | `cases=24 observed_pass=8 observed_fail=16 mismatches=0` |
| 37 | configure-git-webserver | `corpus/evidence/round37/git-webserver-probe.txt` | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` |
| 38 | build-pmars | `corpus/evidence/round38/build-pmars-probe.txt` | `cases=22 observed_pass=7 observed_fail=15 mismatches=0` |
| 39 | git-leak-recovery | `corpus/evidence/round39/git-leak-probe.txt` | `cases=25 observed_pass=13 observed_fail=12 mismatches=0` |
| 40 | db-wal-recovery | `corpus/evidence/round40/db-wal-probe.txt` | `cases=28 observed_pass=8 observed_fail=20 mismatches=0`, `regrade cases=28 differ=0` |
| 41 | constraints-scheduling | `corpus/evidence/round41/constraints-probe.txt` | `cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `regrade cases=25 differ=0` |
| 42 | circuit-fibsqrt | `corpus/evidence/round42/fibsqrt-probe.txt` | `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0` |
| 43 | feal-differential-cryptanalysis | `corpus/evidence/round43/feal-probe.txt` | `cases=12 observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0` |
| 44 | feal-linear-cryptanalysis | `corpus/evidence/round44/feal-linear-probe.txt` | `cases=14 observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0` |
| 45 | password-recovery | `corpus/evidence/round45/password-recovery-probe.txt` | `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0` |
| 46 | polyglot-c-py | `corpus/evidence/round46/polyglot-c-py-probe.txt` | `cases=18 observed_pass=7 observed_fail=11 mismatches=0`, `regrade cases=18 differ=7` |

Totals: **240 frozen end states, 91 observed passes, 149 observed fails.** Each round's entry
explicitly names the graded-state class new to the lane's executed sample ("the graded state is a
class the lane had not executed before": built binary+source tree r38, git object store r39,
binary-pair-derived JSON export r40, computed scheduling model over an ICS file r41, data format
executed by a grader-compiled simulator r42, imported-and-called Python module r43, substring-swept
text file r44, membership-checked guesses file r45, dual-runtime-executed source file r46) — the
series deliberately walked the space of grader *mechanisms* one executed exemplar at a time.

## 2. The series' question (reconstructed)

Per task: **what does the grader's reward bit actually decide, stated-requirement by stated
requirement — and what does a reward-1 end state actually prove?** Each entry builds an
instruction-line → assertion map, derives `enforced / unenforced / partly` labels from executed end
states (the counter-derived V7 rule: `enforced` iff every violating case fails, `unenforced` iff
every violating case passes, `partly` otherwise), and bounds what a trajectory analysis may read
into a 1. The entries say this in so many words (r36: "A trajectory or submission analysis that
reads a 1 as 'the agent implemented the stated date rule' is therefore reading more than this
grader decides").

Method invariants repeated in all twelve (these are part of the series' intent — the triage inherits
them): capture at the pin with `SHA256SUMS`; predictions written from static reading and **frozen
before the first recorded run** (dry-case freeze); executed probe over frozen end states including a
`nop` and the task's own oracle; `mismatches=0` prediction discipline (the only exception, r41,
carries its 2 mismatches as named pilot errors); a falsifier block that makes the entry
re-executable; ≤25-word located byte-exact quotes; append-only errata after falsify waves.

## 3. The series' running conclusion

**Every one of the twelve graders under-decides its instruction, and none of them is
presence-only.** Of the 91 passing end states, **≥56 are documented passing violators** — end
states that violate at least one stated instruction requirement and are nevertheless observed
`pass` — counted per entry: r35 ≥1 (G-only linkers), r36 6/8 ("Six of the eight passing cases …
violate a stated or structural requirement"), r37 7/9 (5 named + `catch-all-200` + `slow-server-3s`),
r38 7/7 (canned 21-line C program, empty `debian/`, zero-byte `src/dummy.c`, `dlopen`-invisible,
`Results:` prefix, exit-status-blind, PATH split, `debian`-as-file, `*.c`-as-dir), r39 8/13
(echo-only, reflog-expire, gc-only, blob-ref, tag-message, stash, dotfile, config), r40 1/8
(hand-typed JSON that never opens the database scores 7/7; 22 of 33 cells pinned), r41 ≥3/6
(decoy-first-VEVENT, CRLF input rewrite ×2), r42 6/7 (lookup-28 family incl. plus-examples,
padding, comments, reversed lines, CRLF), r43 7/8 (five never-cryptanalysed cheats + untimed 45 s),
r44 7/8 (public keys, public generator replay, copied constants, concatenated/reversed/zero-padded/
decoys), r45 3/5 (public-test-file constant ± CRLF, 1000 decoys), r46 0 documented (its defect is
non-idempotence: `regrade differ=7`). The cross-task conclusion the series converged on:

- the decisive mechanism in every grader is a **fixed, finite, in-file witness set** (literals,
  a 25-line log, a 28-input table, 100 constants, one constant, 22/33 cells, three N points, the
  first `DTSTART`), so *satisfaction-of-witnesses ≠ satisfaction-of-requirement*;
- the reward is one pytest exit bit, so per-requirement partial compliance is invisible;
- grader-marker coverage (content reads, subprocess execution, value comparisons) **never**
  implies requirement coverage — the most marker-rich graders in the sample (r38, r39, r40) carry
  the headline permissiveness findings.

## 4. Per-task weakness classes the series found

Taxonomy over the twelve entries (class → exemplar tasks):

1. **Finite in-file witness set / literal answer** — r35 (PDB/FPbase/FLAG literals), r36 (9 dates +
   fixed 25-line log; hardcoded alternation passes), r40 (22/33 pinned cells), r42 (28 graded
   inputs; `lookup-28` passes while the instruction's own examples print 0), r44 (100 constants as
   substrings), r45 (one constant as a split-line member), r46 (3 fixed points).
2. **Proxy checks, no provenance** — r38 (`ldd` scan, directory shape, stdout prefix, exit status
   unread — nothing ties the binary to a build), r37 (git-step exit status never read), r43
   (nothing times the call; 45 s passes a "under 30 s" request), r46 (exact directory listing taken
   *before* the grader's own gcc build mutates the directory; `regrade differ=7`).
3. **Graded channel narrower than the work** — r40 (only `/app/recovered.json` is read; the repair
   step is unobservable), r44 (substring containment anywhere in the file), r45 (membership in
   `split("\n")`), r37 (stdout token `TEST PASSED` in helper output, incl. an echoed body).
4. **In-process authority granted to the artefact** — r36 (agent regex compiled and run inside the
   scoring process), r43 (agent module imported into the grader; `get_keys()[5]` public answer,
   `__eq__`-always-true, `sys.modules` shadow, `os._exit(0)` before the assert, clock-seeded 16-bit
   keys replayable via libc `srand`/`rand`).
5. **State space not swept** — r39 (reflog, gc'd-but-present objects, dangling blobs/commits,
   annotated-tag messages, stash, dot files, `.git/config` all outside the four checks), r41
   (first-`DTSTART` binding, decoy VEVENT, `read_text()` input-integrity hole under CRLF/CR), r35
   (G-only linkers, order-message misattribution via `find`→−1, cap never decides).
6. **Presence-only head test** — existence tests that pass for a directory or an empty artefact
   (`r42 gates-is-directory` `PFF`, r40 `test_recovered_json_exists`, r45
   `test_recovery_file_exists`; measured `P1` under A1, below), and untouched/nop states that pass a
   majority of tests (r39 `untouched` 4/5, r42 `nop` 2/3, r40 `[]` 4/7).
7. **Unbounded time / hung service tolerated** — r43 (45 s oracle passes), r37 (no `curl`
   `--max-time`; 3 s answer counts).
8. **Non-idempotent grading** — r46 (the grader's own compile changes the graded directory;
   same tree grades differently on a second pass).

## 5. What a whole-benchmark triage must not lose — the named property

**No-clear one-sidedness across the mechanism→witness gap.** The triage's marker vocabulary
(presence/content/behaviour, per-file V-classes or per-test P-classes) measures *mechanism
presence*; the series' conclusions live one level higher, at *requirement decisions over finite
in-file witness sets*. The property a triage must preserve is that its output is **one-sided**: a
class may only lower a task into the candidate queue; **absence from the queue must never be
readable as "grader sound" or "requirement covered."** If any V2/V3/V0/P2/P3 label could be read as
clearance, the triage would contradict **all twelve** entries at once, because every one of them
documents passing violators inside marker-rich graders.

Measured check (run today, with the frozen counter's own code —
`plans/round52_c1_grader_audit.py` imported and its `classify`/`classify_tests` applied to the 12
captured `tests/test_outputs.py`; script and raw output in my report dir, `series12-classes.txt`):

| round | task | file class | in V1/V4 queue? | A1 per-test classes |
|---|---|---|---|---|
| 35 | protein-assembly | V3 | no | [P3] |
| 36 | regex-log | V3 | no | [P3] |
| 37 | configure-git-webserver | V2 | no | [P2] |
| 38 | build-pmars | V2 | no | [P3,P3,P3,P3] |
| 39 | git-leak-recovery | V2 | no | [P3,P2,P2,P2,P2] |
| 40 | db-wal-recovery | V3 | no | [**P1**,P3,P3,P3,P3,P3,P3] |
| 41 | constraints-scheduling | V3 | no | [P3,P3,P3] |
| 42 | circuit-fibsqrt | V2 | no | [P3,P3,P2] |
| 43 | feal-differential-cryptanalysis | V2 | no | [P2] |
| 44 | feal-linear-cryptanalysis | V3 | no | [P3] |
| 45 | password-recovery | V3 | no | [**P1**,P3] |
| 46 | polyglot-c-py | V2 | no | [P2] |

- **File-level queue (V1/V4): 0 of 12** — and 12 of 12 carry documented unenforced requirements.
  The file-level unit has, on the only tasks with ground truth, zero recall of the series' findings
  and no false-clearance risk *only if* read one-sidedly.
- **A1 per-test queue (≥1 P1): 2 of 12** — `db-wal-recovery::test_recovered_json_exists` and
  `password-recovery::test_recovery_file_exists`. A1 recovers weakness class 6 only.
- **The A1 amendment's own motivating example is invisible to A1.** The claims' Amendment A1 cites
  round 38 ("build-pmars … a canned 21-line C program passing on presence-level checks") — yet all
  four of build-pmars's test blocks classify P3 because each carries a value token (`in`/`==`/`len`)
  over under-checked inputs. A1's unit change does not recover classes 1–5, 7–8; this is a measured
  divergence the wave-2 critic seats should weigh.
- The file-level `V4` leg ("no marker class applies and ≤2 tests") is nearly unreachable for pytest
  graders: any `assert x in y` matches the content marker, so a 2-test grader with one membership
  assert is V3. On the 12, V4 never fires. The population queue is therefore effectively the A1 P1
  pool (disclosed by the L1 as 54 presence-only tests across 42 tasks — the L1's observation, not
  this seat's measurement).

Three subordinate preserves follow from the same evidence (a triage keeps the series true only with
all four):

- **(P2) Pin-byte identity.** `CAPTURES expected=184 present=184 mismatched=0` at
  `corpus/evidence/round52/graders/SHA256SUMS` keeps every one of the 240 end-state conclusions and
  every entry's falsifier re-executable at `2fd12b88`; a triage over re-fetched drifting bytes
  would sever the series' recheck lines (`recheck: 180d …`).
- **(P3) Per-requirement attachment via located verbatim quotes.** The series' admission bar is a
  ≤25-word byte-exact quote at `file:line`; A1's hardened `CONFIRMED` leg (verbatim quote in the
  captured grader bytes) is the triage-side encoding of the same bar and must not be relaxed.
- **(P4) Population continuity.** `CONFIRMED new` must exclude the 12 series tasks (new = 89 − 12):
  the triage cannot claim as "new" findings the entries already own; at most it may re-flag their
  `P1` head tests as known-class instances.

## 6. Divergences and risks worth wave 2's attention

1. **Unit change is an amendment, not the frozen §C1 text.** The claims' main C1 section freezes
   file-level rules; Amendment A1 (2026-10-28, disclosed, before the scored after-run) moves the
   unit to test functions and hardens `CONFIRMED`. My reconstruction judges both units; the frozen
   after-predicate is the amended one.
2. **P1 (A1) can over-flag relative to the series' meaning of vacuity**: a `P1` presence-only test
   never awards the reward by itself (pytest exit requires all functions), so a P1 flag is a
   per-assertion weakness, not a task-level "presence satisfies the grader". The series' own
   task-level vacuity instances (e.g. r38's canned program) are *not* P1. Expect P1-heavy counts to
   need per-finding wording at this grain.
3. **`mismatches=2` (r41) is the only receipt where prediction discipline broke**; it is carried as
   named pilot errors with errata W1. A triage has no prediction freeze at all — its analogue is the
   blind labelling leg (`labels.json`), which the claims keep as evidence-only.
4. The series' `partly` labels (e.g. r42's `output-function` enforced at exactly 28 points) are the
   finest-grained conclusions; no marker class can represent "enforced at N points". The triage must
   not emit coverage-shaped labels.

## 7. What I did (commands), artifacts, cleanup

- Read in full: `plans/round-52-claims.md` (incl. Amendment A1); heads/tails of all 12
  `corpus/knowledge/tb2-*-grader.md`; `corpus/README.md` §Frontier (lines 324–513); lesson heads
  `corpus/lessons/round-{35,41,44,46}.md`; `plans/round52_c1_grader_audit.py:1-123` (marker rules
  + Amendment A1 code); `plans/round52-tasks.json:1-43`.
- Ran: `grep -m2 -hE '^(cases=|regrade )'` over the 12 receipts (table above, verbatim strings);
  `grep -n '^def test_'` over the r38/r40/r45 captures (P1 test names);
  `python3 series12_classes.py` (imports the frozen counter; classifies the 12 captures) — raw
  output receipt `series12-classes.txt` in this report dir, script copy `series12_classes.py`
  alongside.
- Scratch discipline: all work under `/fast/scratch/hyaku/kengaku-r52/C1RevSeriesIntent/` (527 GB
  free at start, `df -h /fast`); the scratch dir is removed immediately before yielding; receipts
  kept are copied into this report dir.
- Nothing was written outside my scratch and this report dir; no installs; no subprocesses left
  running.

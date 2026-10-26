# R38ScorecardDraft — paste-ready `## Round 38` SCORECARD section, capability candidates, and the LOG entry

Seat `R38ScorecardDraft` (scribe), kengaku round 38 wave 1. I drafted text only: no lane file was edited, no
clone or fixture was built (so no scratch dir was created), no tool was installed, and no mutating git command
was run. Everything below was read from the lane at tip `2c5f4e0` (read-only `git log`/`git show`/`git
ls-tree`), from the freeze tree `e0a37853`, and from the captured artefacts.

**Placeholder convention.** Every landing number is written `<L1 fills>`; §5 maps each placeholder to the
receipt that owns it. Freeze-side numbers are real and carry their command/output in §1. Two score cells are
drafted as *held* by the round-37 precedent — see the draft note under the table.

---

## §1 Numbers this draft rests on (with the command that produced each)

| # | fact | value | command / source |
|---|---|---|---|
| 1 | baseline lane tip (round-37 non-author spot-check) | `fc1174f52b150999bef91f2e81da78732ca0eb9f` | `plans/round-38-claims.md:3`; `git log --oneline -12` shows `fc1174f` beneath `e0a3785` |
| 2 | freeze commit | `e0a378539a45cc9388c66cfba22f44275131de23` | `git show --stat --oneline e0a3785` → 18 files, 1588 insertions (claims, both counters, probe, spec template, dry table, five captures + `SHA256SUMS`, four controls + `census-before.txt` + `frozen-digests.txt`) |
| 3 | first recorded probe run | `e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b` | `git show --stat --oneline e95cf55` → one file, `corpus/evidence/round38/build-pmars-probe.txt` (+26); commit subject carries `cases=22 observed_pass=7 observed_fail=15 mismatches=0; second run byte-equal` |
| 4 | wave-1 build spec / dispatch | `2c5f4e0`, 40 items | `git log --oneline -1`; `.ufo/waves/round-38/build-spec.json` → `python3 -c "…len(d['items'])"` → `items 40` |
| 5 | C1 do-nothing control | `PINS total=14 mismatched=0`; `BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0`; `MUTANTS total=22 killed=0 survived=22 invalid=0 null_detected=0`; `PREDICATE C1 fail`; `exit=1` | `.ufo/waves/round-38/claims/control-c1-nothing.txt` (95 lines; `real 0m48.467s`) |
| 6 | C1 gate-edited control (pin is failure-capable) | `PINS total=14 mismatched=1 first=plans/pkg_gate.py`; all 22 mutants `invalid`; `MUTANTS total=22 killed=0 survived=0 invalid=22 null_detected=0`; `PREDICATE C1 fail`; `exit=1` | `.ufo/waves/round-38/claims/control-c1-gate-edited.txt` (91 lines) |
| 7 | C2 do-nothing control | `checks=7 defects=4`; `V2 DEFECT`, `V3 DEFECT`, `V4 DEFECT`, `V7 DEFECT`; `PREDICATE C2 fail`; `exit=1` | `.ufo/waves/round-38/claims/control-c2-nothing.txt` (gate inside: `defects=8`, `P9 DEFECT untracked=11`) |
| 8 | C2 skip-control (hand-typed receipt copied from `--dry`) | `checks=7 defects=2`; `V2 DEFECT` (gate `P10 DEFECT fresh probe output is not byte-equal to the receipt`), `V6 DEFECT census_exit=1`; `V7 ok rows=7 tags=7`; `exit=1` | `.ufo/waves/round-38/claims/control-c2-skip.txt` |
| 9 | frozen digests | 8 entries: gate `ea638822…`, both r38 counters, probe `32f0771c…`, `pkg-spec-r38.json` `bd9bfe71…`, dry table `93b4b60c…`, r37 counters | `.ufo/waves/round-38/claims/frozen-digests.txt` |
| 10 | C1 mutant split | direction cells: 19 silence, 3 mirror (N02, N08, N15); clause families: P1 (N01), P3 (N02), P4 (N03–N06), P5 (N07–N08), P6 (N09–N10), P7 (N11–N12), P10 (N13–N15), RUN handler (N16), MAIN exits (N17–N18), D4 (N19–N20), D5 (N21–N22) | `plans/round38_c1_verify.py:93-137` `MUTANTS` table (cells `(id, clause, direction, adv, old, new)`); `plans/round-38-claims.md:32` ("Mirror mutants (N02, N08, N15) test the false-red direction") |
| 11 | C1 counter pins | 14 inputs = gate + r37 counter + r36 counter + r35 spec + nine battery37 modules + r37 attribution audit | `plans/round38_c1_verify.py:1-70` docstring ("Pins (`PINS total=14`)") |
| 12 | probe receipt | `cases=22 observed_pass=7 observed_fail=15 mismatches=0`; predictions `predicted_pass=7 predicted_fail=15` | `corpus/evidence/round38/build-pmars-probe.txt:26`; `corpus/evidence/round38/build-pmars-dry-cases-freeze.txt` (`CASE` lines carry `predicted=`) |
| 13 | dry-table requirement tags | 7 tags: `from-source` (instruction.md:1), `no-x11` (:3), `debian-source` (:3), `extract-to-app` (:3), `install-path` (:3), `results-format` (:7), `debugger-works` (:9) | `grep -n '^TAG' corpus/evidence/round38/build-pmars-dry-cases-freeze.txt` |
| 14 | census before | `exit=0` (16 `W04 duplicate url … across scopes` findings + `ok` line) | `.ufo/waves/round-38/claims/census-before.txt` |
| 15 | registry / index before | SOURCES 107 rows; knowledge files 44; README knowledge index rows 44 | `grep -cE '^\| *S[0-9]{3}' corpus/SOURCES.md` → 107; `ls corpus/knowledge/*.md \| wc -l` → 44; `grep -cE '^\| *`knowledge/' corpus/README.md` → 44 |
| 16 | capability table size before | 13 rows (`offline-replay-gate` … `service-grader-probe`) | `SCORECARD.md:555-567` |
| 17 | upstream drift at the pin | `terminal-bench-2` `main` = `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (2026-04-30); five captures `cmp`-equal, blob shas equal | `.ufo/waves/round-38/build/R38ScoutUpstream.md` §1 (12 commits total for `build-pmars`; no newer) |
| 18 | `terminal-bench-2-1` divergence | `tasks/build-pmars/` path move (5fc7d3b9); `instruction.md` line 3 differs (adds `/pmars-<version>/`, "Leave the source tree in place"), `solution/solve.sh` differs; `test_outputs.py`/`test.sh`/`task.toml` identical | `R38ScoutUpstream.md` §2 |
| 19 | routed D1 state | round-37 `falsify/` is committed at the tip: 37 report `.md` on disk, `git ls-tree -r --name-only HEAD -- .ufo/waves/round-37/falsify \| wc -l` → 380 | commands in the row; commit `21e6251` |
| 20 | routed D4 state at the freeze | still hard-codes the branch ref: `plans/defect_ledger.py:29` and `plans/round36_c1_verify.py:38` both `BRANCH = "refs/heads/master"` | `grep -n 'refs/heads/master' plans/defect_ledger.py plans/round36_c1_verify.py` |

---

## §2 Paste-ready SCORECARD section

> Paste after line 1332 of `SCORECARD.md` (after the round-37 `### Wave 2 outcome` block). One draft note
> follows the table; it is L1-facing and should be deleted before pasting.

## Round 38 (hyaku run 8, 2026-10-26): gate mutants killed only by attribution, a build-provenance TB2 grader executed

Baseline `fc1174f52b150999bef91f2e81da78732ca0eb9f` (the round-37 non-author spot-check); frozen prereg
`plans/round-38-claims.md` (freeze `e0a378539a45cc9388c66cfba22f44275131de23`; first recorded probe run
`e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b`; wave-1 build spec and validated dispatch `2c5f4e0`, 40 items). Axis
state carried: calibration 8, coverage 7, novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Lowest
non-retired axis: coverage 7, tied with novelty 7; coverage chosen by the frozen tie-break (a pinned local source
and an offline sandbox exist; the round-37 planning seat priced every novelty candidate as published,
`.ufo/waves/round-37/build/R37PlanNext.md` §4). Coverage stays capped at 7 by the open L0 question
(`.ufo/l0-questions.md`, `kengaku | round-33`), so C2 is judged on its counter, not on a score move. No stagnation
waiver.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 gate behaviours the round-37 battery does not demonstrate, killed only by an ATTRIBUTED kill: 22 frozen one-behaviour mutants N01–N22 of `plans/pkg_gate.py` (freeze digest `ea638822…`, unedited; 19 silence-direction, 3 mirror-direction, over the clause families P1–P10, D4/D5, the RUN handler and MAIN's exits) over the round-36 battery, `plans/battery37/*.py` and `plans/battery38/*.py` | **calibration** — the number of frozen mutants no fixture kills under the attributed rule (silence: the reference prints the mutant's clause `DEFECT`, the fixture declares it, the mutant does not; mirror: reference `ok`, mutant `DEFECT`; RUN: a declared `DEFECT` clause stops being `DEFECT`; MAIN: reference exit 2, mutant exit 0/1), i.e. the mismatch between what the gate docstring, `corpus/QUALITY.md` Q24/Q27 and the `package-gate` / `gate-mutation-harness` capability rows advertise and what the lane's tests show. The 3 mirror mutants add the false-red direction the round-37 list lacked | `python3 plans/round38_c1_verify.py --lane .` on a clean clone: before `PINS total=14 mismatched=0`, `BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=0 survived=22 invalid=0 null_detected=0`, `PREDICATE C1 fail`, exit 1 (`.ufo/waves/round-38/claims/control-c1-nothing.txt`; the gate-edited control prints `PINS total=14 mismatched=1 first=plans/pkg_gate.py` and refuses to judge, `invalid=22`, `claims/control-c1-gate-edited.txt`) → after `PINS total=14 mismatched=0`, `BATTERY fixtures=<L1 fills> wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=<L1 fills> survived=<L1 fills> invalid=<L1 fills> null_detected=<L1 fills>` (predicate: `killed=22 survived=0 invalid=0 null_detected=0`), `PREDICATE C1 <L1 fills>`, exit `<L1 fills>` (`.ufo/waves/round-38/integrate/measure-final.txt`); no-harm: `python3 plans/round37_c1_verify.py --lane .` at the landing tip `<L1 fills>` | **8 → 8 held**; frozen predicate `<L1 fills: met / not met>`; mismatch count 22 → `<L1 fills>` on the frozen list, every kill attributed to the mutant's own clause and direction. No score raise: the denominator is the lane's own mutant list (a branch nobody mutated is invisible), a kill records a result difference and not a reason, and the side-channel scan that guards the battery is a token heuristic |
| C2 pinned TB2 `build-pmars` grader admitted with an executed 22-case offline probe of a fourth grader class: the graded state is a built artefact plus a source tree, checked by presence, an `ldd` string scan, directory shape and a regex over the program's output (S115 `tests/test_outputs.py`, S116 `instruction.md`, terminal-bench-2 @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, opened 2026-10-26; upstream `main` byte-equal for all five captures) | **coverage** (lowest, tied) — `coverage/surfaces`: SOURCES 107 → 109 rows (`<L1 fills>` tier split), knowledge files / index rows 44/44 → 45/45, one README coverage bullet, one PROVINCE paragraph, one §Frontier TB2 sub-bullet narrowed by one task; `coverage/constructs`: unchanged (the executed-sample class sentence is a property of this capture's evidence, not a construct claim) | `python3 plans/round38_c2_verify.py --lane .`: before `checks=7 defects=4` (V2, V3, V4, V7), exit 1 (`.ufo/waves/round-38/claims/control-c2-nothing.txt`); skip-control `checks=7 defects=2` (V2 via `P10 DEFECT fresh probe output is not byte-equal to the receipt`, V6), exit 1, with `V7 ok rows=7 tags=7` — the derived-label check alone cannot be satisfied by a receipt copied from `--dry` (`claims/control-c2-skip.txt`) → after `checks=7 defects=<L1 fills>` (predicate `defects=0`), `PREDICATE C2 <L1 fills>`, exit `<L1 fills>` (`.ufo/waves/round-38/integrate/measure-final.txt`); probe `cases=22 observed_pass=7 observed_fail=15 mismatches=0`, second run byte-equal (`corpus/evidence/round38/build-pmars-probe.txt`) | **7 → 7 held** (L0 cap); frozen predicate `<L1 fills: met / not met>`; the counter now pins every input it reads (spec template, gate, probe, dry table, five captures — round-37 closure D7) and derives each requirement-map label from all receipt cases violating its tag (D2), so a one-witness label is a red counter rather than a prose risk |

Draft note (do not paste): both score cells are drafted *held* on the round-37 precedent (demonstration is
observational; the denominators are the lane's own lists). The L1 may reprice C1 to 9 if it treats the attributed
kill rule — a rule the round-37 attack showed the previous "any result differs" rule to be gameable — as a
claim-strength increase rather than an instrument repair; the round-30/31 precedent (capability added, score held)
argues for held.

Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Capabilities entered (table above,
first-working round 38): `<L1 fills: the candidate row(s) that passed their landing-tip predicate, or "none">`;
candidates were `build-artifact-grader-probe` (the C2 probe) and `attributed-gate-mutation-harness` (the C1 counter),
each of which enters only with `PREDICATE C1 pass` / `PREDICATE C2 pass` at the landing tip, and a refused candidate
is logged as a refusal, not dropped. Registry 107 → 109 rows (`<L1 fills>` tier split); knowledge files /
index rows 44/44 → 45/45; census exit 0 before (`claims/census-before.txt`) and `<L1 fills>` after. Assimilation:
`considerthese/2026-10-25.md` proposal 2(c) (tip-receipt validator) `<L1 fills>`; `merge/kengaku/` re-screened
`<L1 fills>` (`.ufo/waves/round-38/build/R38MergeRescreen.md`). Frontier mistake: `<L1 fills>`
(`.ufo/waves/round-38/build/R38LessonDraft.md`). Routed-item closure: D1 (round-37 wave-2 outputs) is committed at
the baseline — 37 reports, 380 tracked paths under `.ufo/waves/round-37/falsify/`; D3 and D7 are the frozen V3 and
V2 pins above; D4 is still open at the freeze (`plans/defect_ledger.py:29`, `plans/round36_c1_verify.py:38` both
`refs/heads/master`) → `<L1 fills>`; D6 `<L1 fills>` (`.ufo/waves/round-38/build/R38SiblingCite.md`).

### Limits named at freeze, and found in wave 1

- C1: the attribution rule ties a kill to the mutant's own clause and direction, not to the fixture's intent; the
  side-channel scan is a token heuristic (`/proc`, `ppid`, `cmdline`, `psutil`, `environ`), so a non-author review
  of `plans/battery38/*.py` remains part of admission; a mutant later shown equivalent is reported as a limit and
  never removed from the frozen list; a battery38 fixture may own its spec (shapes B1/B6/B8 need it), and the
  counter only checks that the spec path is inside the fixture directory.
- C2: the probe runs the grader, never the task image or the oracle; host bash stands in for Debian dash, host
  glibc `ldd`, and the canned artefacts are compiled on the host. The finding class — the unenforced half of the
  instruction passes — is published (`.ufo/waves/round-37/build/R37ScoutPriorArt.md`); the entry claims a probed
  instance only. Prior upstream report TB2 issue #59 (`build-pmars` oracle pins fail) concerns the oracle, not the
  grader: `<L1 fills>` (re-opened and rowed or refused).
- Freshness: `terminal-bench-2` `main` equals the pin for all five captures (5/5 `cmp`-equal, blob shas equal,
  `.ufo/waves/round-38/build/R38ScoutUpstream.md` §1). Not a drift, but a limit of the anchor: `terminal-bench-2-1`
  carries `build-pmars` under `tasks/` and its `instruction.md` line 3 is different prose (same line numbering), so
  every `instruction.md:<L>` row in the entry is an anchor into the 2.0 document only, and the 2.1 instruction adds
  "Leave the source tree in place" while the identical grader checks nothing about it (`R38ScoutUpstream.md` §2).
- Wave-1 additions: `<L1 fills>` (critics `R38CritC1Counter`, `R38CritC2Counter`, `R38CritProbe`,
  `R38CritPytest`, `R38CritIndep`, `R38CritClaims`, `R38RevCounters`, `R38RevFreeze`; mutation-tester greps
  `R38MutC2Counter`, `R38MutProbe`; connectors `R38ConnSibling`, `R38ConnPattern`; `R38SentinelProbe`).

### Planned (round 39)

- `<L1 fills>` — drafted against `.ufo/waves/round-38/build/R38PlanNext.md` (planning seat), the wave-1 critic
  reports above, and the wave-2 outcome.

### Wave 2 outcome (appended after WAVE-DONE falsify; `<L1 fills>` seats, `<L1 fills>` reports, `.ufo/waves/round-38/falsify-results.json`)

- `<L1 fills>`

---

## §3 Capability-row candidates (only if demonstrated this round — all `pending demonstration`)

Both candidates are drafted in the table's cell style. Neither may enter on wave-1 development runs: the counter
prints `PREDICATE C1 n/a` / `C2 n/a` in development mode, so only the landing-tip measure counts.

### 3.1 `build-artifact-grader-probe` — **pending demonstration**

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| build-artifact-grader-probe | Execute a captured grader whose graded state is a built artefact plus its source tree — binary presence, an `ldd` string scan for disallowed libraries, directory-shape checks, a glob over `src/*.c`, and a regex over the program's stdout — offline against lane-built states, with the predictions frozen in a dry table written before any recorded run (`--dry` runs no grader), and print predicted vs observed with the first failing assertion. Not task certification, not runtime inside the task image, not a claim that the grader is a good grader. | `python3 plans/build_pmars_probe.py --lane .` → `cases=22 observed_pass=7 observed_fail=15 mismatches=0`; receipt `corpus/evidence/round38/build-pmars-probe.txt`, re-run byte-equal by `plans/round38_c2_verify.py` V2 (`P10`)/V5 | 38 — **pending demonstration: requires `PREDICATE C2 pass` (`checks=7 defects=0`) at the landing tip**, `.ufo/waves/round-38/integrate/measure-final.txt` |

Ceiling to paste with the row: host bash for Debian dash, host glibc `ldd`, host-compiled canned artefacts; the
grader's own weaknesses (the seven `CASE` observations in §4) are observations of the capture, not a validity claim.

### 3.2 `attributed-gate-mutation-harness` — **pending demonstration**

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| attributed-gate-mutation-harness | Decide which advertised clauses of a gate a fixture battery demonstrates, counting a mutant killed only when the run changes **its own clause in its own direction** (silence, mirror, RUN-handler, MAIN-exit), with the counter's own 14 inputs digest-pinned (an edited gate gives `PINS mismatched=1` and `invalid=22` rather than a verdict) and a source token scan against fixtures that inspect the running gate. Survivors are advertised-but-undemonstrated behaviours; mirror mutants cover the false-red direction. Not proof that a check is the right check. | `python3 plans/round38_c1_verify.py --lane .` on a clean clone → `PINS total=14 mismatched=0`, `BATTERY fixtures=<L1 fills> wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0`; freeze control `killed=0 survived=22` (`.ufo/waves/round-38/claims/control-c1-nothing.txt`) | 38 — **pending demonstration: requires `PREDICATE C1 pass` at the landing tip** |

**Supersession option for the L1.** If a second C1 row is judged duplicative, the alternative is a correction line
that supersedes only the *evidence cell* of `gate-mutation-harness` (`SCORECARD.md:566`), because that cell's
definition — "killed iff the gate's observable result … changes on some fixture" — is the rule round 37 showed to
be gameable (`.ufo/waves/round-37/build/R37CritC1Battery.md`: a hostile battery reaches the same kill line). The
round-38 counter's attributed rule and its pins are the repair. Either form needs the same landing evidence; the
row must not enter on the freeze control.

---

## §4 Paste-ready LOG entry

> Append to `LOG.md` after the round-37 entry. `<L1 fills>` where the value is a landing or wave-2 measurement.

## Round 38 — 2026-10-26 (hyaku run 8)

Declared C1 calibration (8): kill, only under an attributed rule, the gate behaviours the round-37 battery leaves
undemonstrated — 22 frozen one-behaviour mutants of `plans/pkg_gate.py` (19 silence-direction, 3 mirror-direction,
over the clause families P1–P10, D4/D5, the RUN handler and MAIN's exits; `plans/round38_c1_verify.py`, 14 inputs
pinned by digest) over the round-36 battery plus `plans/battery37/` and `plans/battery38/`. Declared C2 coverage (lowest, tied 7, L0 cap `kengaku | round-33`): admit the pinned
Terminal-Bench 2.0 `build-pmars` grader (S115 `tests/test_outputs.py`, S116 `instruction.md` @ `2fd12b88`) with an
executed 22-case offline probe of a build-provenance grader — a class new to the lane. Baseline `fc1174f5`; freeze
`e0a37853` (claims, both counters, the probe, the spec template, the dry table, five captures, four controls);
first recorded probe run `e95cf550` (second run byte-equal); wave-1 build spec and dispatch `2c5f4e0` (40 items
across battery, entry, scout, critic, reviewer, mutation-tester, connector and sentinel seats; `<L1 fills>` dead).

- C1: freeze `PINS total=14 mismatched=0`, `BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0`,
  `MUTANTS total=22 killed=0 survived=22 invalid=0 null_detected=0`, `PREDICATE C1 fail` — the round-36+37 battery
  demonstrates none of the 22. The gate-edited control is red on the pin, not on a verdict
  (`PINS total=14 mismatched=1 first=plans/pkg_gate.py`, `invalid=22`). Twelve battery seats were dispatched
  (`R38BatP1Run`, `P3`, `P4a`, `P4b`, `P5`, `P6`, `P7`, `P10a`, `P10b`, `Main`, `D4`, `D5`); `<L1 fills>` of them
  produced `plans/battery38/` modules (battery commit `<L1 fills>`, `<L1 fills>` modules / `<L1 fills>` fixtures);
  landing `BATTERY fixtures=<L1 fills> wrong=0
  renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=<L1 fills> survived=<L1 fills> invalid=<L1 fills>
  null_detected=<L1 fills>`, `PREDICATE C1 <L1 fills>` on a clean clone; no-harm `plans/round37_c1_verify.py`
  `<L1 fills>` at the landing tip.
- C2: probe `cases=22 observed_pass=7 observed_fail=15 mismatches=0`, predictions `7/15` frozen in the dry table
  before any recorded run (`--dry` runs no grader; the one control-time execution was discarded unread,
  `plans/round-38-claims.md:8-15`) — `corpus/evidence/round38/build-pmars-dry-cases-freeze.txt`; entry
  `corpus/knowledge/tb2-build-pmars-grader.md`
  with S115/S116, a seven-row requirement map (tags `from-source`, `no-x11`, `debian-source`, `extract-to-app`,
  `install-path`, `results-format`, `debugger-works`) whose labels V7 derives from every violating case
  (`<L1 fills>` labels). Before `checks=7 defects=4` (V2, V3, V4, V7) → landing `checks=7 defects=<L1 fills>`,
  `PREDICATE C2 <L1 fills>`; skip-control red at `checks=7 defects=2` with `V7 ok` — a hand-typed receipt that
  copies the predictions still dies on `P10`/V2 (`claims/control-c2-skip.txt`).
- Observations on the pinned capture (receipt `corpus/evidence/round38/build-pmars-probe.txt`, case ids as filed):
  `canned-shape` (`:5`) passes all four tests with a canned C program, an empty `debian/` directory and a
  zero-byte `src/dummy.c`; `debian-is-file` (`:21`) passes with `debian` as a zero-byte regular file
  (`test_outputs.py:70` uses `Path.exists()`); `c-is-dir` (`:23`) passes with `src/sim.c` a directory
  (`test_outputs.py:84` globs `*.c`); `canned-x11-dlopen` (`:9`) passes while `dlopen()`ing `libX11.so.6`, because
  the scan reads `ldd` text (`test_outputs.py:53-57`) and the library is never a `DT_NEEDED` entry;
  `results-trailing-text` (`:11`) passes a forged battle line, `test_outputs.py:46` anchors the start only;
  `canned-exit-nonzero` (`:16`) passes with the program exiting 3, `test_outputs.py:14-15` returns non-empty output
  from a `CalledProcessError`; `path-split` (`:19`) passes when a canned script earlier on `PATH` answers the
  behaviour checks while `ldd` reads the silent installed binary.
- Freshness: `terminal-bench-2` `main` is the pin (`2fd12b88`, 2026-04-30) and the five captures are `cmp`-equal
  with equal blob shas (`.ufo/waves/round-38/build/R38ScoutUpstream.md` §1). `terminal-bench-2-1` moved
  `build-pmars` under `tasks/` and differs at `instruction.md` line 3 (adds `/pmars-<version>/`, "Leave the source
  tree in place") and in `solution/solve.sh`; the grader is byte-identical, and the 2.1 instruction adds a sentence
  no test checks — recorded as an anchor limit, not a drift.
- Frontier: every input the C2 counter reads is now digest-pinned (D7) and each requirement-map label is derived
  from all violating cases (D2), with V3 binding every anchor token to its own row's capture (D3). Mined mistake
  for the lesson: `<L1 fills>` (`.ufo/waves/round-38/build/R38LessonDraft.md`) — the freeze disclosure repeats
  round 37's order-of-operations mistake (`plans/round-38-claims.md:8-15`).
- Routed items: D1 closed at the baseline (round-37 wave-2 outputs committed: 37 reports, 380 tracked paths under
  `.ufo/waves/round-37/falsify/`, commit `21e6251`); D4 still open at the freeze — `plans/defect_ledger.py:29` and
  `plans/round36_c1_verify.py:38` hard-code `refs/heads/master` → `<L1 fills>`; D6 `<L1 fills>`.
- Assimilation: `considerthese/2026-10-25.md` proposal 2(c) (tip-receipt validator) `<L1 fills>`; `merge/kengaku/`
  re-screened `<L1 fills>` (`.ufo/waves/round-38/build/R38MergeRescreen.md`).
- Re-verification at the landing tip: both frozen predicates `<L1 fills>`; round-37 counter no-harm `<L1 fills>`;
  census `<L1 fills>`; anchor check `<L1 fills>`; render/state checks `<L1 fills>`
  (`.ufo/waves/round-38/build/R38TipReceipts.md`).
- Tool use: none installed by this seat; the host's pacman transactions are paused, so any wave-1 install would
  have gone through `uv tool`/`npx`/an official binary into `~/.local/bin` — `<L1 fills: tool, version, channel,
  reason>` for the seats that did.

---

## §5 Fill map — each `<L1 fills>` and the receipt that must own it

| placeholder | appears in | owning receipt / command |
|---|---|---|
| landing tip sha | §2 header if the L1 records the measure clone's revision | the measure clone's `git rev-parse HEAD`; the round-37 precedent (`measure-final.txt`) |
| C1 `BATTERY fixtures=<n>` | §2 C1 after-cell, §3.2, §4 C1 | `python3 plans/round38_c1_verify.py --lane .` on a clean clone of the landing tip (expect `64 +` count of battery38 fixtures) |
| C1 `killed/survived/invalid/null_detected`, `PREDICATE`, exit | §2 C1 after-cell, §3.2, §4 C1 | same run; frozen predicate is `killed=22 survived=0 invalid=0 null_detected=0` |
| round-37 counter no-harm line | §2 C1 after-cell, §4 | `python3 plans/round37_c1_verify.py --lane .` at the landing tip (must still print `PREDICATE C1 pass`) |
| battery commit / fixture count / module count | §4 C1 | the L1's `plans/battery38/` integration commit (`git show --stat`) |
| C2 `defects=<n>`, `PREDICATE C2`, exit | §2 C2 after-cell, §3.1, §4 C2 | `python3 plans/round38_c2_verify.py --lane .` on the landing clone |
| C2 requirement-map labels | §4 C2 | `corpus/knowledge/tb2-build-pmars-grader.md` `## Requirement map`, re-derived by V7 |
| SOURCES tier split (S115/S116) | §2 C2 axis cell, other-axes paragraph | `corpus/SOURCES.md` rows S115/S116 tier cells |
| census after | §2 other-axes paragraph | `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md`, exit + findings |
| capability rows entered | §2 other-axes paragraph | the landing measure plus the L1's admission decision on §3.1/§3.2 |
| assimilation outcomes | §2 other-axes paragraph, §4 | `.ufo/waves/round-38/build/R38MergeRescreen.md`; `.ufo/waves/round-38/assimilation/` |
| frontier mistake / lesson | §2 other-axes paragraph, §4 | `.ufo/waves/round-38/build/R38LessonDraft.md` |
| D4 / D6 closure lines | §2 other-axes paragraph, §4 | `.ufo/waves/round-38/build/R38LedgerTip.md`, `R38SiblingCite.md`; re-check `grep -n 'refs/heads/master' plans/defect_ledger.py plans/round36_c1_verify.py` |
| wave-1 additions to Limits | §2 Limits | the critic / reviewer / mutation-tester / connector / sentinel reports listed there |
| wave-2 outcome block | §2 tail, §4 | `.ufo/waves/round-38/falsify-results.json` after WAVE-DONE |
| round-39 plan | §2 `### Planned (round 39)` | `.ufo/waves/round-38/build/R38PlanNext.md` |
| C2 probe exit / oracle-pin item (issue #59) | §2 Limits, §4 | the wave-1 seat that re-opens TB2 issue #59; `R38SentinelProbe.md` |
| wave-2 seat/report counts | §2 wave-2 heading | `falsify-results.json` |

## §6 What this draft does not do

- It does not measure the landing. Both frozen predicates are unmeasured here; every after-cell is a placeholder
  form. Wave-1 battery development runs print `PREDICATE C1 n/a` (development mode), and no `plans/battery38/`
  module is in the lane at drafting time (`ls -d plans/battery38` → `No such file or directory`; `git status
  --porcelain` lists only the untracked `.ufo/waves/round-38/` dirs) — the aggregate run is the L1's.
- It does not re-run any frozen counter, probe, gate or census: the freeze controls and the committed probe receipt
  are quoted as filed, not re-derived.
- It does not judge the C2 entry's prose or labels. V7 derives them; the entry seat
  (`R38PkgEntry`/`R38PkgProse`) and the critics own the text, and a label disagreement is theirs to fix before the
  landing measure.
- It does not decide the score. The table drafts *held* on the round-37 precedent and flags the one place a
  repricing is arguable (§2 draft note, §3.2 supersession option).
- It does not touch any lane file, any `plans/` or `corpus/` tree, the lane's git index, or sibling lanes.

VERDICT: scorecard-log-drafted

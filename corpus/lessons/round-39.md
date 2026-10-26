# Round 39 — undemonstrated gate behaviours with witnessed directions; a fifth TB2 grader (repository history) executed (2026-10-26, hyaku run 8)

Baseline as read at round start: `b2bdd425fbc042d3075994dae60fe88a51e277ab` (the round-38 non-author spot-check). Frozen
claims `plans/round-39-claims.md`, freeze `088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8`; first recorded probe run
`6a1eb5e1da4a435940b821e28530c31f3411549c` (`cases=25 observed_pass=13 observed_fail=12 mismatches=0`, second run byte-equal,
`.ufo/waves/round-39/first-run/first-run.txt`).

Controls at the freeze (`.ufo/waves/round-39/claims/`): `control-c1-nothing.txt` (`PINS total=26 mismatched=0`, `BATTERY
fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=3 survived=4`, exit 1 — red),
`control-c1-gate-edited.txt` (`mismatched=1`, `invalid=7` — red), `control-c1-hostile-inproc.txt` (the round-38 in-process
`run_gate` patch as a battery39 module: `killed=3 survived=4`, unchanged — the patch reaches only its child process),
`control-c2-nothing.txt` (`checks=7 defects=4`, V2 V3 V4 V7, exit 1 — red), `census-before.txt` (exit 0, 15 W04 — a
baseline, not a control). Order of operations: no committed control executed the probe before `6a1eb5e1` (the C2 control's
P10 stops at `receipt unreadable`); `--stage-check` built the case states without importing the grader.

Baseline drift (disclosed): the round-38 L1 landed `ef2fba062069de4f29aea45cb2a03d29a131054b` (round-38 wave-2 reports and
results, 34/34, outcome appended to `corpus/lessons/round-38.md`) at 03:37:53, after this round's baseline read and before
its freeze, so the freeze `088f7c36` is a child of `ef2fba0`, not of `b2bdd425`. `git diff --stat b2bdd425 ef2fba0 -- plans
corpus/knowledge corpus/SOURCES.md corpus/README.md` is empty: no frozen input moved. That commit also closes round-38
closure item R1 (wave-2 outputs committed: `git ls-files .ufo/waves/round-38/falsify | wc -l` → 428); wave-1 seat
`R39R38Integrate` mapped its 34 reports / 97 findings to dispositions (`build/R39R38Integrate/dispositions.md`: this round 21,
round 40 58, limit 9, none 9).

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `knowledge/tb2-git-leak-recovery-grader.md` (C2) | **Admitted** | Drafted by wave-1 scribe `R39PkgEntry` (its clone `checks=7 defects=0`), integrated by the L1: prior-art section rewritten from `R39ScoutPriorArt` (sources opened, not snippets), finding 9 rewritten from `R39CritFsckReflog` (git `--lost-found` clears `include_reflogs`, `builtin/fsck.c:905-908` at v2.56.0, `:950-953` at v2.43.0), contestable tags and case-text corrections from `R39CritProbe` D1–D5 (frozen table not edited). Rests on the 25-case receipt (predictions frozen before the first recorded run, second run byte-equal) and the frozen C2 counter at the landing tip. Independent agreement: real pytest 8.4.1 25/25 (`R39CritPytest`), independent re-derivation 25/25 (`R39CritIndep`), probe mutants 7/7 change the receipt (`R39MutProbe`), counter mutants 11/11 caught (`R39MutC2Counter`). Flip: a fresh probe run differs from the receipt, or a capture leaves its pin. |
| S117 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined)** | Opened by the L1 2026-10-26 03:27 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/git-leak-recovery/tests/test_outputs.py`; quote, line 16: “assert text == "secret[lost_and_found_in_git]", f"Flag value is incorrect: {text}"”; sha256 `dc7b01c1b9dbb0c123def54b146dc1dd399a600edee5970d043a5db5eac4c775`; byte-identical in TB2.1 `main` (`R39ScoutUpstream`, `R39ScoutPriorArt`). Flip: the capture's digest leaves the pin. |
| S118 `instruction.md` @ `2fd12b88` | **Admitted (mined)** | Opened by the L1 2026-10-26 03:27 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/git-leak-recovery/instruction.md`; quote, line 4: “clean up the secret in that repo to make sure it cannot be found anywhere in that repo.”; sha256 `54ac693fd26a4c003f610d62c4b2671f1d1d04ac5b1286f780605e385a9a5861`. Flip: the capture's digest leaves the pin. |
| `challenge-setup.sh`, `solve.sh`, `test.sh`, `task.toml`, `Dockerfile` @ `2fd12b88` (captured) | **Captured, not rows** | `challenge-setup.sh` builds the graded state and `solve.sh` runs as one probe case; `test.sh` is the pytest → reward mechanism the registry holds as S109; `task.toml` and `Dockerfile` are read for declared limits. Flip: an entry statement that needs one of them as its source. |
| `harbor-framework/terminal-bench` `docs/TASK_REVIEW_AUTOMATION.md:244` (nop validation contract) | **Refused as a row; cited in the entry** | Opened by `R39ScoutPriorArt`: "Nop Validation confirms doing nothing fails tests (task is non-trivial)." — a task-level contract consistent with the receipt (`untouched` reward 0), not a report of this grader's per-test behaviour; no entry statement rests on it. Flip: a claim about TB's validation process. |
| JonathanGabor/terminal-bench-2-audit `audit.txt:1485` @ `35f11039` | **Refused as a row; cited as nearest prior statement** | LLM prose, no executed case; names the reflog gap and dismisses it ("fsck should catch objects…"), contradicted by `echo-gc-only`/`echo-reflog-expire`. Tier C at best. Flip: a claim resting on what the audit asserts. |
| R38PlanNext §2.5 snippets ("must score exactly 0.0"; third-party "1 of 5 passing" at no-op) | **Refused — not found when opened** | `R39ScoutPriorArt` §1.4/§3.F: neither statement appears in any opened page; they were search-engine snippets carried unopened in round 38. Flip: a located primary source. |
| Assimilation: `merge/kengaku/` re-screen (`R39MergeRescreen`) | **Nothing adopted** | Package unchanged since round 38; id check (0–3-space pattern, guard proven on an indented `  | S002 |` fixture) `reg-ids=109 staged-ids=175 collisions=33` (S077–S086, S090–S094, S097, S100–S116), receipts `build/R39MergeRescreen/{reg-ids,staged-ids,collisions}`; verdicts admit-candidate 2 (card family, deferred again: no frozen claim names it), hold 42, refuse 21 (per-entry reasons in the report). Flip: a round that freezes an assimilation claim on the card family. |
| Assimilation: `considerthese/2026-10-25.md` proposal 2(b) (read 2026-10-26) | **Mined; landed as `plans/order_check.py` + QUALITY Q30** | "blocks pre-registration when a class recurs twice": the order-of-operations class recurred (round 37, round 38); the gate reads committed history and is red on both and green on round 39 (Mistakes row 1). It detects rather than blocks; Q30 says so. |
| SOURCES curation: four due rows re-opened (`R39SourcesRecheck`) | **No status/recheck change** | Each opened live 2026-10-26 with a located quote; every `status`/`recheck` stays as it was (old→new identical, logged in the report); the 15 W04 census warnings are by design (scoped tiers, superseding-row idiom). |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **order-of-operations — recurrence closed by a gate** (round 37 lesson row 3, round 38 lesson row 2) | `.ufo/waves/round-37/claims/control-c2-skip.txt:12` and `.ufo/waves/round-38/claims/control-c2-skip.txt:11` each carry a gate `P10` line from a control committed in the freeze, before the first receipt commit | the round-38 closure R3 (no gate existed: round 37's rule forward was prose) | `plans/order_check.py` (wave-1 executor `R39OrderGate`) + QUALITY Q30: round 38 → `ORDER HIT …control-c2-skip.txt@e0a378539a45:11`, `ORDER RESULT FAIL`, exit 1; round 37 → FAIL, exit 1; round 39 → `ORDER RESULT PASS`, exit 0 (`build/R39OrderGate.md`, re-run in `integrate/measure-final.txt`) — shown able to fail on both earlier rounds. Not written: a `recurrence=2` row in `corpus/defects.jsonl` (the frozen claims' frontier sentence says it would be) — its checker is the round-35 frozen counter `plans/defect_ledger.py`, which has no check for this class and would report an unknown check as a failure; routed to round 40 (a separately frozen checker extension). |
| **load-bearing fixture bytes edited — the L1 appended an erratum to the round-35 genuine package entry** (new this round) | the R4 errata from `R39RecheckFix` appended to `corpus/knowledge/tb2-protein-assembly-grader.md` added four `recheck:` strings; the next C1 run printed `SETUP module battery38/p7m.py failed to build (rc=1) … expected exactly one 'recheck:', found 5` (that entry is the genuine package every round-36..39 battery copies) | the C1 counter's own SETUP refusal (exit 2) on the working tree, before any commit | reverted from the branch (`git show master:… >`), never committed; the R4 correction for that entry is recorded here instead: its recheck command is `(cd corpus/evidence/round35/tb2-eval && sha256sum -c SHA256SUMS)` (6/6 `OK`, exit 0; `build/R39RecheckFix.md` §4a). Forward rule: the round-35 entry and every file `plans/round36_c1_verify.py:copy_package` copies are fixture bytes — an erratum to them goes to a lesson, not the file. |
| **counter docstring overclaims its own isolation** (new this round) | `plans/round39_c1_verify.py:40-42` "A module therefore cannot patch this counter's `run_gate`": true for battery38/39 (built in children), false for an added `plans/battery37/*.py` file, which the round-37 loader imports in-process and no pin covers (`R39CritC1Counter` A3: `killed=7`, `PREDICATE C1 pass` with a forged in-process battery). Same report: A1 a daemon flips a fixture's spec between the reference and mutant phases (`killed=7` from four dishonest fixtures), A4 pins hashed once before the children run, A5 the child's reported `dir` trusted | `R39CritC1Counter` (wave-1 critic); none at freeze — the hostile control tested only the vector already closed | the frozen counter is not edited (its predicate judges C1). Post-hoc `plans/round39_c1_audit.py` (L1, not the frozen rule) re-checks each kill with a reference re-run, closes the battery37/38 name sets, re-hashes pins after the run and uses the parent's own fixture dirs: A3 replay → `PINS … mismatched=1 first=plans/battery37/zz_inproc.py`, refusal, exit 2 (`integrate/audit-a3-replay.txt`; the frozen counter on the same tree prints `PREDICATE C1 pass`); A1 replay → `AUDIT nondeterministic_kills=4 first=M02:a1b-p1-second-instrument`, `AUDIT C1 dirty` (`integrate/audit-a1-replay.txt`; the audit's verdict is that line — its exit code follows the frozen predicate); landed battery → `AUDIT nondeterministic_kills=0`, `PINS final … mismatched=0`, `AUDIT C1 clean` (`integrate/measure-final.txt`). Round 40: re-freeze with the four repairs in the counter itself. |
| **calibration count overstated by its own `adv` cells** | the claims mark 3 of 7 `adv` cells indirect; `R39CritClaims` §1 and `R39AdvErrata` find M01, M04, M07 cite no sentence that reaches their behaviour (M01's cited genuine package has its capture on manifest row 1, so `[:1]` is a no-op there) | wave-1 critics; the round-38 closure had already flagged the same shape (3 of 22) | the advertised-behaviour count is reported as 4 (M02, M03, M05, M06): before 2 undemonstrated (M02, M03) → after 0; the frozen 7-mutant predicate is reported unchanged beside it. Forward: an `adv` cell must quote its sentence with file:line at freeze. |
| **separability sentence true only at clean tips** | `plans/round-39-claims.md` §Separability; `R39CritClaims` §4: a knowledge file without its index row reds C1 (`wrong=51`, every genuine-package fixture copies the live corpus), and an untracked battery39 file reds C2 (P9) | `R39CritClaims` | both predicates are measured on a clean clone of the landing tip, where the C2 package and battery39 landed in one commit (`34158b0`), so neither predicate moved; the sentence is corrected here: each claim passes with the other's work product wholly absent, not partly present. |

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): exit 0, `kengaku ok`, 15 W04 (`claims/census-before.txt`). After: exit 0 (`integrate/census-after.txt`).
Registry rows 109 → 111 (S117, S118; tier A; `mined`), knowledge files 45 → 46, README index rows 45 → 46. Rows touched
old→new: none.

## Spot-check

Pending — the non-author closure follows the report. Cheapest failing checks first:

1. `python3 plans/round39_c1_verify.py --lane .` on a clean clone of the landing tip → `MUTANTS total=7 killed=7
   survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`; then `python3 plans/round39_c1_audit.py --lane .` → `AUDIT C1 clean`.
2. Remove `plans/battery39/p7m39.py` in a scratch clone → `M04 … SURVIVED`.
3. `python3 plans/round39_c2_verify.py --lane .` → `checks=7 defects=0`, `PREDICATE C2 pass`; probe re-run byte-equal.
4. Relabel the entry's `secret-gone` row to `enforced` in a scratch clone → V7 red.
5. Re-open S117/S118 live (digest + quote line).
6. `python3 plans/order_check.py --lane . --claims plans/round-38-claims.md --receipt corpus/evidence/round38/build-pmars-probe.txt` → exit 1; round 39 → exit 0.
7. `python3 plans/round37_c1_verify.py --lane .` → `killed=55` (no harm); `round38_c1_verify.py` → `killed=21 survived=1` as landed.

## Errata (round 39, wave 2)

Appended after the falsify wave (`.ufo/waves/round-39/falsify/F39RevLesson.md` D1–D3, `F39CritC1Count.md`); the rows above
stand as written.

- Mistakes row 2's refusal line was not committed when written; it is now reproduced by a non-author seat:
  `F39RevErrata.md` §F4 appended the same errata to `tb2-protein-assembly-grader.md` in a clone and the round-38 counter
  aborted with `RuntimeError: expected exactly one 'recheck:', found 5` (claim confirmed).
- Gate row "four due rows re-opened": none was due (`sources-census.sh overdue` printed no line); the seat opened the four
  rows with the highest drift risk. Flip for that row: a later re-open whose bytes or quote differ from the row.
- Gate row for `considerthese` proposal 2(b): flip — a round in which `plans/order_check.py` is red on its own round or
  green on round 37/38, or in which the class recurs while the gate passes.
- Mistakes row 4's advertised-behaviour count: `F39CritC1Count` recounts against the four declared surfaces as C 2 (M05,
  M06), K 3 (M01, M02, M03 — a class sentence covers them), N 2 (M04, M07): the denominator is **5**, not 4, and the
  attribution to `R39CritClaims` §1 for M01 is wrong (that report tiers it as uncited, the recount as K). Before/after is
  unchanged: of the five, M02 and M03 survived the freeze (M01 was killed by the round-38 battery), so 2 → 0.
- Post-hoc audit limit found by `F39SentinelAudit`: a battery module whose daemon reads the process table can serve the
  reference and replay one spec and every mutant run another (`aa_sa_phasekey.py`, `AUDIT C1 clean`, `killed=7` with the
  honest modules moved aside). The audit's kill re-check catches only flips still in place at replay. The landed battery
  holds no such code: four non-author reviewers found each module honest (`F39RevBatP1/P3/P7/D5`), and fixture-level mutants
  are caught 12/12 (`F39MutBattery`). Round 40's counter needs immutable fixture snapshots and sandboxed build children.

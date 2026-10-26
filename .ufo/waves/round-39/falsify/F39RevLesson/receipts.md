# F39RevLesson receipts — round-39 lesson review (wave 2 falsify)

Fixture: `S=/fast/scratch/hyaku/kengaku-r39/F39RevLesson`; `git clone -q --no-local <lane> "$S/lane" && git -C "$S/lane" checkout -q a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`; `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`; `status --porcelain` = 0 lines. Lesson copy at tip vs workspace: md5 `86968fa1f33b352f7b308a57378a418a` both. Scratch removed after receipts were copied.

All paths below are relative to the lane root; `L=$S/lane`.

## 1. Header drift (lesson lines 3, 12-16)

- `git -C "$L" show -s --format='%H | %ci | %s' <rev>`:
  - `b2bdd425…` → `2026-10-26 03:22:34 -0300 | round-38 verifier spot-check (integrator, hyaku): non-author admit/reject`
  - `ef2fba0…` → `2026-10-26 03:37:53 -0300 | round-38: wave-2 reports and results (34/34), outcome appended to lesson`
  - `088f7c36…` → `2026-10-26 03:40:24 -0300 | round-39: freeze claims, C1/C2 counters, git-leak probe, dry table, captures, controls`
  - `6a1eb5e1…` → `2026-10-26 03:40:45 -0300 | round-39: first recorded git-leak probe run (25 cases, mismatches=0, byte-equal second run)`
  - `34158b0…` → `2026-10-26 04:25:25 -0300 | round-39: battery39 (4 modules), C2 package …, post-hoc C1 audit, wave-1 reports`
  - `a6832f5…` → `2026-10-26 04:37:51 -0300 | round-39: lesson, SCORECARD and LOG …`
- Parentage: `rev-parse 088f7c36^` = `ef2fba0…`; `rev-parse ef2fba0^` = `b2bdd425…`; `merge-base --is-ancestor` chains b2bdd425→ef2fba0→088f7c36→6a1eb5e1→a6832f5 all true.
- `git diff --stat b2bdd425 ef2fba0 -- plans corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l` → `0`.
- `git ls-tree -r --name-only ef2fba0 -- .ufo/waves/round-38/falsify | wc -l` → `428`; top-level `.md` → `34`.
- `git diff-tree --name-only -r ef2fba0` corpus hits → `corpus/lessons/round-38.md` only.
- Freeze commit 088f7c36 adds `.ufo/waves/round-39/claims/{census-before,control-c1-gate-edited,control-c1-hostile-inproc,control-c1-hostile-inproc-module.py,control-c1-nothing,control-c2-nothing,frozen-digests}` + `plans/round-39-claims.md`. Commit 6a1eb5e1 adds `first-run/first-run.txt` + `corpus/evidence/round39/git-leak-probe.txt`.

## 2. Controls at the freeze (lesson lines 6-11)

- `control-c1-nothing.txt`: `PINS total=26 mismatched=0`; `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`; `MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0`; `PREDICATE C1 fail`; `exit=1`.
- `control-c1-gate-edited.txt`: `PINS total=26 mismatched=1 first=plans/pkg_gate.py`; `MUTANTS total=7 killed=0 survived=0 invalid=7 …`; `exit=1`.
- `control-c1-hostile-inproc.txt`: `BATTERY fixtures=88 …`; `MUTANTS total=7 killed=3 survived=4 …`; `exit=1` (unchanged vs nothing-control).
- `control-c2-nothing.txt:11` `gate: P10 DEFECT receipt unreadable`; V2/V3/V4/V7 DEFECT; `checks=7 defects=4`; `exit=1`.
- `census-before.txt`: 15 W04 lines; line 17 `exit=0`.
- `first-run.txt`: `rc1=0 rc2=0; cmp run1 run2 -> byte-equal`; date `2026-10-26T03:40:45-03:00`.
- `corpus/evidence/round39/git-leak-probe.txt:30` `cases=25 observed_pass=13 observed_fail=12 mismatches=0`.

## 3. Census section (lesson lines 57-59)

- Registry S-rows: `git show <rev>:corpus/SOURCES.md | awk 'match($0,/\| *S[0-9][0-9][0-9] *\|/){n++} END{print n+0}'` → b2bdd425 `109`, tip `111`.
- Knowledge files: `ls-tree -r --name-only <rev> -- corpus/knowledge | wc -l` → `45` / `46`.
- README index rows `^\| \`knowledge/` → `45` / `46`. Counter's own P8 at measure-final: `index_rows=46 knowledge_files=46 bad=0`.
- `diff <(awk NF claims/census-before.txt) <(awk NF integrate/census-after.txt)` → identical; census-after `exit=0`, 15 W04.
- `scripts/sources-census.sh` exists (fleet root, 35466 bytes).
- S117/S118 rows: tier `A`, status `mined`, opened `2026-10-26`, 180d, used-by the new entry.

## 4. Gate rows

- Entry receipt `R39PkgEntry/c2-counter-output.txt`: `checks=7 defects=0`, `PREDICATE C2 pass`.
- `R39CritPytest.md`: "real pytest 8.4.1", result "25/25 per-test vectors agree", totals 13/12.
- `R39CritIndep.md:68` "Agreement: 25/25"; VERDICT `indep-agree-25/25-extra-2/3`.
- `R39MutProbe.md`: "Counter-level catch: 7/7"; VERDICT `probe-mutants-7/7`.
- `R39MutC2Counter.md`: 11 mutants M01–M11 table; VERDICT `c2-mutants-11/11`; M01 = `secret-gone` `partly`→`enforced` → V7 DEFECT.
- S117 capture `sha256sum` = `dc7b01c1…c775` = lesson digest = SHA256SUMS line; quote at capture line 16 exact. S118 capture sha256 = `54ac693f…861`; quote at line 4 exact.
- `R39ScoutUpstream.md`: "Raw-fetched 2.1 files … `2.1-IDENTICAL-TO-CAPTURES`"; "vs TB 2.1: 0 files differ"; `R39ScoutPriorArt.md:58` grader unchanged in TB2.1 `main`.
- `R39ScoutPriorArt.md:20` quote, line 244 "Nop Validation confirms doing nothing fails tests (task is non-trivial)."; entry cites it at `tb2-git-leak-recovery-grader.md:296`.
- `R39ScoutPriorArt.md:64-65` audit repo @ `35f11039…`, quote `audit.txt:1485`; §1.4/§3.F both snippets not found.
- `R39CritFsckReflog.md:15` "`builtin/fsck.c`, v2.56.0:905-908 / v2.43.0:950-953".
- Receipt CASE ids `echo-reflog-expire` (line 9) and `echo-gc-only` (line 10) exist, both `violates=secret-gone`.
- `R39MergeRescreen/`: `reg-ids` 109 lines; `staged-ids` 175 lines; `collisions` 33 lines = S077–S086, S090–S094, S097, S100–S116; `entry-verdicts.tsv` → ADMIT-candidate 2 (benchmark-card-adoption.md, benchmark-card-field-schema-2026-10-23.md), HOLD 42, REFUSE 21. Report: package unchanged since round 38; 0–3-space anchor with indented `  | S002 |` guard fixture.
- `considerthese/2026-10-25.md` tracked in lane; lines 42-44 "(b) blocks pre-registration when a class recurs twice".
- `R39SourcesRecheck.md`: "0 `overdue` lines"; "Because nothing is due, I opened the 4 rows with the highest drift risk"; change rows "none"/"No edit recommended"; §3 W04 "by design", superseding-row idiom.

## 5. Mistakes rows

- Round-37 lesson data rows: 1 reference-drift (l.40), 2 vacuous 5/55 (l.41), **3 order-of-operations (l.42)**. Round-38 lesson: 1 freeze-defect N21, **2 order-of-operations (l.36)**. Both lesson pointers correct.
- `.ufo/waves/round-37/claims/control-c2-skip.txt` line 12 and `.ufo/waves/round-38/…` line 11: `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt` (blobs at freezes ca790460 / e0a378539a45).
- `round-38-verifier-spotcheck.md:162` "3. **R3 — order-of-operations recurrence.**".
- ORDER gate: `R39OrderGate.md` r38 RED exit 1 (HIT `control-c2-skip.txt@e0a378539a45:11`), r37 RED exit 1, r39 GREEN exit 0; re-run at landing `integrate/measure-final.txt:235-247` same verdicts.
- `corpus/defects.jsonl`: 0 lines matching "order"; no `corpus/defects-round39.jsonl` in 34158b0; `plans/defect_ledger.py:124` `ok, note = False, f"unknown check {r.get('check')!r}"`.
- `plans/round39_c1_verify.py:40` exact docstring sentence; `plans/round36_c1_verify.py:55` `def copy_package`; `corpus/QUALITY.md:522` Q30.
- Row 2: `plans/battery38/p7m.py:36-38` `_only_once` → `expected exactly one {needle!r}, found {text.count(needle)}`; counter SETUP wrapper `plans/round39_c1_verify.py:204` + `:289`. Tip protein entry: exactly 1 `^recheck:` line. `R39RecheckFix.md:214` "`(cd corpus/evidence/round35/tb2-eval && sha256sum -c SHA256SUMS)` → 6/6 `OK`, exit 0" (§4a); `recheck-green.txt` OK lines + `exit=0`; `recheck-red-verbatim.txt` lane-root legs exit=1. grep "found 5|failed to build" over `.ufo/waves/round-39/` + `plans/`: only code hits, no receipt.
- Row 3: `integrate/audit-a3-replay.txt:16-18` `PINS total=26 mismatched=1 first=plans/battery37/zz_inproc.py`, refusal, `exit=2` (frozen counter above it: `PREDICATE C1 pass`, `exit=0`); `audit-a1-replay.txt:27-29` `AUDIT nondeterministic_kills=4 first=M02:a1b-p1-second-instrument`, `AUDIT C1 dirty`, `exit=0`; `measure-final.txt:229-231` `nondeterministic_kills=0`, `PINS final … mismatched=0`, `AUDIT C1 clean`. `R39CritC1Counter.md` §1 table A1/A3/A4/A5 as the lesson states.
- Row 4: `R39CritClaims.md:12` "3 of the 7 `adv` cells cite no sentence that reaches their behaviour (M01, M04, M07…)"; `R39AdvErrata.md:103` M01 no-op row-1 / `:121` `[:1]`; round-38 lesson:38 "3 of the 22 `adv` cells".
- Row 5: `R39CritClaims.md:117` `BATTERY fixtures=86 wrong=51`; `:122-124` untracked battery39 → `P9 DEFECT` (receipt-c2-untracked-coupling.txt); 34158b0 touches `corpus/knowledge/tb2-git-leak-recovery-grader.md` + `plans/battery39/{p1m,p3m39,p7m39,d5m39}.py` in one commit.
- Spot-check backing: measure-final lines 95/103/104 (C1 pass), 126 (C2 pass), 337-361 (r38 counter killed=21 survived=1), 451-508 (r37 counter killed=55), 235-247 (ORDER), 602 (REF AUDIT rev=34158b0).
- `--stage-check`: `plans/git_leak_probe.py:231,260-268` builds case states, returns before any grader import; also `plans/round-39-claims.md:8`.

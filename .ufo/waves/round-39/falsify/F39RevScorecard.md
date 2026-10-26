# F39RevScorecard — calibration count of the round-39 self-report (wave 2, falsify)

Scope: every factual statement in `SCORECARD.md` §Round 39 (lines 1375–1420, incl. "Planned (round 40)"), the
`LOG.md` Round-39 entry (lines 1150–1177), and `SHONEN.md`, checked against repo state at
`a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`. Method: clean `--no-local` clone at the tip in
`/fast/scratch/hyaku/kengaku-r39/F39RevScorecard` (removed; receipts copied here first), frozen instruments re-run,
receipts and wave-1 reports opened line-by-line. Re-run log: `rerun-transcript.txt`; full C1 counter log:
`c1-rerun-a6832f5.txt`.

## Result: 1 mismatch found

**M1 (minor, wording overstates diligence).** `LOG.md:1175` "four **due** SOURCES rows re-opened with no status change
(`R39SourcesRecheck`)" — the cited report says the opposite: `.ufo/waves/round-39/build/R39SourcesRecheck.md:10-14`
"`--today 2026-10-26` → 0 `overdue` lines" and "Because nothing is due, I opened the 4 rows with the highest drift
risk". The four re-opens (S027, S014, S041, S045), the no-status-change outcome, and the "15 W04 by design" note are
all real; only "due" is wrong (they were proactive re-opens, not scheduled). The lesson repeats the same "four due
rows" wording (out of this seat's scope, noted for the ledger).

## Verified inventory (statement → command → result), all confirmed

Commit graph: `git show --no-patch --format='%H %P' 088f7c36… b2bdd425… ef2fba0 6a1eb5e1` → 088f7c3's parent is
ef2fba0; baseline b2bdd425 and first probe run 6a1eb5e1 exist with matching subjects. Lesson header discloses the
drift: `corpus/lessons/round-39.md:16-19` "the freeze `088f7c36` is a child of `ef2fba0` … `git diff --stat …` is
empty: no frozen input moved" — scorecard's "— lesson header" attribution is accurate.

C1 (scorecard row + LOG): pkg_gate digest `sha256sum plans/pkg_gate.py` → `ea63882240e6…`, `git diff --stat
b2bdd425 HEAD -- plans/pkg_gate.py …` empty; 7 mutants M01–M07 with N21 as mirror, wave-2 survivors, pre-freeze
witnesses (`plans/battery38/d5m.py:77`, `F38XMutP/witness-run.txt`, `F38XMutRerunMain/survivor-probes.txt`,
`survivor-probeB.txt` all present), two rc legs and out-of-process builds (`round39_c1_verify.py:199,214`
subprocess). Before-control `.ufo/waves/round-39/claims/control-c1-nothing.txt` → `fixtures=86`, `killed=3
survived=4`, `C1 fail`, `exit=1`. Landing: my re-run at the tip → `PINS total=26 mismatched=0`, `BATTERY fixtures=90
wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`,
`PREDICATE C1 pass`, exit 0 — identical to `integrate/measure-final.txt`. Gameability A1/A3/A4/A5 as claimed in
`build/R39CritC1Counter.md` (§2/§3/§4/§5 = kill re-check, closed name sets, re-hashed pins, parent-owned dirs);
`integrate/audit-a3-replay.txt` → "AUDIT unpinned battery module present; refusing to import it", exit 2 (A3
refused); `audit-a1-replay.txt` → "AUDIT nondeterministic_kills=4 … AUDIT C1 dirty" (A1 caught); landed battery →
"AUDIT C1 clean" (re-run confirms). Advertised-only recount 2 → 0 (M02/M03/M05/M06 reach; M01/M04/M07 do not) matches
`build/R39CritClaims.md:12,45` and lesson Mistakes row 4.

C2: S117/S118 rows at `corpus/SOURCES.md:132-133`, tier A, pin `2fd12b88aafdd…`; SOURCES rows 109→111
(`git show ef2fba0:corpus/SOURCES.md | grep -c '^| S'` = 109; tip = 111); knowledge/index 45/45 → 46/46
(control-c2 `P8 … 45/45` vs landing `P8 … 46/46`); registry 109→111 (`R39MergeRescreen.md:33` reg-ids=109;
measure-final `registry_rows=111`); probe `cases=25 observed_pass=13 observed_fail=12 mismatches=0`, P10
`probe_rerun=byte-equal bytes=5867`, first-run `first-run.txt:4` "rc1=0 rc2=0; cmp run1 run2 -> byte-equal";
dry table has 25 `violates=` tags; before-control `checks=7 defects=4 (V2,V3,V4,V7)` exit 1; my re-run →
`checks=7 defects=0`, `PREDICATE C2 pass`. LOG's per-case observations all match the frozen table (untouched FPPPP =
flag test only, test 1 = `test_flag_file_exists_and_correct`; dangling blob/commit PPPFP = test 4
`test_no_secrets_in_unreachable_objects`); `builtin/fsck.c:905-908` at v2.56.0 per `R39CritFsckReflog.md:15`;
pytest 8.4.1 25/25 (`R39CritPytest.md:48,79`), independent 25/25 (`R39CritIndep.md:68`); prior art verified
(`tb2-git-leak-recovery-grader.md:297` "two third-party validation runs record it", `:305` "No upstream issue or
PR"; lesson:32-33 nop contract + LLM audit dismissing the reflog gap).

No-harm set, re-run by me at a6832f53: round-38 C1 `killed=21 survived=1` (fail by design), round-37 C1
`killed=55` pass, round-38/37 C2 `checks=7 defects=0`, round-36 C2 `checks=6 defects=0`, anchor `rows=111 tokens=19
defects=0`, ledger-tip `rows=9 closed=9 mismatches=0`, census exit 0, `sha256sum -c frozen-digests.txt` 9/9 OK,
order_check round-38 exit 1 / round-39 exit 0 (exact commands and outputs as advertised), and — new evidence —
order_check round-37 exit 1, confirming LOG's "red on rounds 37 and 38, green on 39".

Routed work: `## Errata (round 39…)` at `corpus/lessons/round-38.md:94` and in exactly three TB2 entries
(build-pmars:344, git-webserver:448, regex-log:320); round-35 entry's correction lives in the round-39 lesson
(fixture bytes, lesson row 2); `R39DirCheckLeg.md:85` "Count: 3/3 caught"; `R39AnchorUnion.md` §2-§5 digest-to-own-
locator fix; `R39LedgerProvenance.md` REFUSE stale master (receipted; REF AUDIT in measure-final); R1 closed in
ef2fba0 (commit subject "wave-2 reports and results (34/34)"); Q24/Q27/Q30 present (`corpus/QUALITY.md:299,409,522`);
PROVINCE deferral paragraph (`PROVINCE.md:413-414`, `R39ConnSibling.md` defer + §5 kasegi cite); considerthese
`2026-10-25.md:43` "(b) blocks pre-registration when a class recurs twice"; merge/kengaku unchanged with collisions
33 / admit-candidate 2 deferred (`R39MergeRescreen.md:23-24,33`, package at `/home/vgpnk/Projects/shokuknow/merge/kengaku/`);
defects.jsonl still rows=5 with no order-class row — consistent with scorecard's "Carried" wording, not contradicted.

Planned (round 40) pricing verified in `R39PlanNext.md`: 17 mutants (anchor 10 :145, ledger-tip 7 :146) unkilled
(:18-19); order_check 4/13 (:23,129); db-wal 7/7 offline / nop 7/7 / byte-equal (:24-25); openssl fallback with
OpenSSL 3.6.5 limit (:25-27); polyglot-c-py second-grading failure (:28-29).

Tool use: no pacman transaction on 2026-10-26 (`/var/log/pacman.log` grep); pytest 8.4.1 in `uv venv -p 3.13`
(`R39CritPytest.md:38,45`); docker `ubuntu:24.04` → apt git 2.43.0 (`R39CritFsckReflog.md:116-119`); biopython 1.85
via the gate's `uv run --with` fallback (`plans/pkg_gate.py:272-276`, `R39AdvErrata.md:70`).

SHONEN.md: all four pointers resolve — SKILL.md has decision tables (9+ hits) and probe exit tables (:587);
`LOG.md:7` is the round-4 "executed first authored eval (closes SHONEN …)" line;
`corpus/lessons/round-8-aggregator-box3-coldrun.md:48` is the Box-3 cold-execution verdict;
`PROVINCE.md:129` opens "### Adjacent" (owner-lane routing table).

## Residual notes (not counted as mismatches)

- `plans/mutant_direction_check.py` exits 1 at the tip (`N21 … MISLABELLED`, `mislabelled=1`): by construction after
  the R2 relabel (round-38 claims still declare `silence`). No self-report text claims it green; the frozen no-harm
  set (claims Kill rule) names only the r37/r38 counters. Flagged so round 40 doesn't mistake it for a regression.
- `measure-final.txt` header says `TIP 34158b0…` (measurement necessarily predates the report commit a6832f5);
  `git diff --stat 34158b0 a6832f5` touches only LOG/SCORECARD/lesson/integrate receipts/falsify-spec generator, and
  my re-runs reproduce every advertised number at a6832f5, so "no-harm at the landing tip" is true.
- Non-author review of `plans/battery39/` is cited as a wave-2 admission leg — this wave, in flight; no wave-2
  receipt exists yet at the tip (prospective statement, not a false one).

## Verification gaps

- The 25-case bubblewrap probe was not re-executed in a sandbox by this seat (docker/bwrap run cost); accepted via
  the committed receipt, the counter's byte-equal P10 re-run, and R39CritPytest's independent 25/25.
- Upstream/TB2.1 byte-equality (R39ScoutUpstream) and the "no upstream issue" search are taken from the wave-1
  scout's receipts, not re-fetched here.
- Host-state claims ("no host install", pacman) checked against `/var/log/pacman.log` only.

Receipts: `rerun-transcript.txt`, `c1-rerun-a6832f5.txt` (this dir). Scratch `/fast/scratch/hyaku/kengaku-r39/F39RevScorecard`
removed; no processes left running.

VERDICT: self-report-mismatches-1

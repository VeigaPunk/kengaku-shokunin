# ExecLegacyHarm — harm and conformance check at T afe9c229

Seat: ExecLegacyHarm (leaf, executor). Lane clones: `--shared` at T and BASE, detached, under scratch (removed before yield). No lane mutation, no git write, no tool install (none needed; no tool installed or updated).

Revisions: BASE 4524072dfae9c5e8210592b7c1da26959aa29dae; T afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239. Raw receipts: `receipts/` in this directory (every file names its exact command at its top; rc line at its end).

## 1. Legacy gate (round79 population ledger)

Command: `python3 plans/round79_c1_population_ledger.py --lane <clone> --rev <rev>` (clone = lane clone at T; `--rev` reads git objects).

| rev | DEFECTS n | TARGET | PREDICATE | rc | receipt |
|---|---|---|---|---|---|
| BASE 4524072d | **14** | classes=16 members=88 pairs=230 replayed=38 located=38 unexecuted=50 covered=15 | fail | 1 | `receipts/legacy-at-BASE-rev-lane-clone.txt` |
| T afe9c229 | **0** | classes=16 members=88 pairs=230 replayed=39 located=39 unexecuted=49 covered=15 | pass | 0 | `receipts/legacy-at-T-rev-lane-clone.txt` |

Worktree mode (`--lane .` in each clone) reproduces the same: `legacy-worktree-base.txt` (14, fail), `legacy-worktree-T.txt` (0, pass).

The 14 BASE defect lines are identical to the BASE block of `.ufo/waves/round-95/L1/legacy-r79-gate.txt` (checked by diff). The T block matches the L1 T block (`DEFECTS n=0`, `PREDICATE R79-C1 pass`).

Mapping of each BASE defect to the C commit's edit (the C commit moved all 14 and nothing else):

| BASE defect | C-commit edit that clears it | backed by |
|---|---|---|
| RECEIPT-UNTRACKED llm-inference-batching-scheduler | ledger row gains `receipt` | `corpus/evidence/round92/bs-probe.txt` (tracked) |
| RECEIPT-UNTRACKED schemelike-metacircular-eval | ledger row gains `receipt` | `corpus/evidence/round93/scheme-probe.txt` (tracked) |
| RECEIPT-UNTRACKED write-compressor | ledger row gains `receipt` | `corpus/evidence/round94/compressor-probe.txt` (tracked) |
| SUBJECT-MISMATCH mteb-retrieve (ledger tb2-result-file, receipt tb2-header) | subject -> tb2-header | see §1a |
| CLASS-K-MISMATCH x10 (subprocess-exec 10->15, shell-exec 1->2, file-artifact 24->29 (+1 for fix-code-vulnerability's flip to 30 at T), stdout-inspection 8->13, numeric-band 3->4, crypto-credential 3->4, timing-wall 3->4, filesystem-metadata 2->4, git-plumbing 1->2, serialization-schema 3->5) | SKILL.md class cells | ledger-derived counts |

Note on the class cells: file-artifact and serialization-schema end at 30 and 6 at T because the C commit also flips fix-code-vulnerability (classes file-artifact, serialization-schema) to executed. The cells match the ledger at T; the gate passes.

Ledger T executed = 39 (BASE 38). Members whose ledger rows changed between BASE and T: exactly `fix-code-vulnerability`, `llm-inference-batching-scheduler`, `mteb-retrieve`, `schemelike-metacircular-eval`, `write-compressor` (`receipts/ledger-BASE.json`, `receipts/ledger-T.json`).

### 1a. Is each C-commit ledger edit supported by its receipt bytes?

Receipt first lines (`git show T:<receipt>`), the subject shape the round79 gate matches (`^# tb2 <member> grader probe`), and the verdict rule (`^PREDICATE R<n>-C<m> pass` -> predicate; else `^VECTOR ` -> vectors; else `^CASE `/`^case=` -> cases):

- round87 `corpus/evidence/round87/mteb-retrieve-probe.txt`: `# tb2 mteb-retrieve grader probe` -> subject tb2-header, verdict cases. Supported.
- round92 `bs-probe.txt`: `# tb2 llm-inference-batching-scheduler grader probe`; 10 CASE lines; no VECTOR; its only PREDICATE line is `PREDICATE R92-PROBE pass` (line 29), which does not match the frozen `R<n>-C<m>` shape -> verdict cases. Supported under the frozen rule (see info I2).
- round93 `scheme-probe.txt`: `# tb2 schemelike-metacircular-eval grader probe (round 93)`; CASE lines; no PREDICATE/VECTOR -> cases. Supported.
- round94 `compressor-probe.txt`: `# tb2 write-compressor grader probe (round 94)`; CASE lines -> cases. Supported.
- round95 `vuln-probe.txt`: `# tb2 fix-code-vulnerability grader probe (round 95)`; 15 CASE lines; no PREDICATE/VECTOR -> cases; `SUBJECT_SHA c006a5de95b69bd7...` matches the ledger evidence `sha256=c006a5de95b69bd7`. Supported.

The C-commit ledger edits are correct against the bytes. No subject or verdict is unsupported.

### 1b. The mteb-retrieve old subject

- `tb2-result-file` is not one of the five frozen subject shapes in `plans/round79_c1_population_ledger.py` (tb2-header, receipt-header, grader-path, task-under-test, capture-tree). It has been an invalid value since its ledger row landed in commit `10de494d` (round 87); the round-87 counter's frozen `LEDGER_SUBJECT` (`plans/round87_c1_replay.py:48`) carries the same string from its own creation in `21da383b`.
- `git log -S tb2-result-file` lists `afe9c229`, `bb29a660`, `e2c73b68`, `c3f81f72`, `10de494d`, `21da383b`. Occurrences in committed plan code: only `plans/round87_c1_replay.py` (lines 48, 251). Wave snapshots under `.ufo/waves/round-89,90,92` also carry the old value; they are not gates.
- The rounds 88/89/90 replay counters all pin `LEDGER_SUBJECT = "tb2-header"`, the same shape the C commit now writes. So the round-87 counter is the only standing gate that expects the non-shape value.

## 2. Standing lane gates, BASE and T (both green at both revs)

Run in the lane clone at each rev (`receipts/<name>-base.txt` / `-T.txt`).

| gate | BASE | T | flip |
|---|---|---|---|
| `python3 grader.py` | `CHECKS n=733 mismatches=0 errata_pinned=1`, VERDICT PASS, rc 0 | identical, rc 0 | none |
| `python3 plans/state_check.py --summary` | `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`, VERDICT PASS, rc 0 | identical counts, VERDICT PASS, rc 0 | none |
| `python3 plans/round68_capability_table.py --lane .` | `MISMATCH n=0`, `PREDICATE R68-A3 pass`, rc 0 | identical | none |
| `python3 plans/round91_f1_counter.py --lane . --work <scratch>` | `ANCHORLINE rows=294 cited=104 captured=91 uncaptured=13 defective=10 repaired=10 live=0`, `WRONG-LINE-CAUGHT True`, `PREDICATE R91-F1 pass`, rc 0 | `rows=301 cited=111 captured=98 uncaptured=13 defective=10 repaired=10 live=0`, pass, rc 0 | none (rows +7 = S303-S309) |
| `python3 plans/anchor_line_check.py --lane .` | `ANCHORLINE rows=294 ... live=0 cells=0`, rc 0 | `rows=301 ... live=0 cells=0`, rc 0 | none |
| `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | rc 0, `kengaku ok` + W04 list (10 duplicate-URL warnings S222...S270) | see below | n/a |

Sources census detail:
- The `--root` form as specified reads the fleet-root worktree `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, not T. That worktree's HEAD is `ea19299d` (T is an ancestor of it; the worktree has 15 dirty entries). Its output is `ok` with the same W04 list; it does not measure T or BASE. `receipts/sources-census-fleet-lane.txt`.
- Explicit lane-dir form on the clones: `validate $S/base` -> rc 0, `base ok`, W04 list; `validate $S/lane` -> rc 0, `lane ok`, identical W04 list (`receipts/sources-census-explicit-base.txt`, `-T.txt`). The C commit adds 7 SOURCES rows (S303-S309) with no new E-code and no new W04 duplicate. No flip.

No standing gate in this list is green at BASE and red at T.

## 3. Additional green->red checks (replay counters that read the ledger)

I ran the round-92/93/94 C1 replays and the round-87 C2 wording counter at both revs, because the C commit changed their member rows. Also round-87 C1 (its member row changed).

| counter | BASE | T | flip | receipt |
|---|---|---|---|---|
| `round87_c1_replay.py --rev` | `TARGET ... defects=0`, `PREDICATE R87-C1 pass`, rc 0 | `DEFECT L7-ledger row {... "subject": "tb2-header" ...}`, `TARGET executed_rows=39 ... defects=1`, `PREDICATE R87-C1 fail`, rc 1 | **PASS -> FAIL** (H1) | `receipts/round87-BASE.txt`, `round87-T.txt` |
| `round94_c1_replay.py --rev` | `LEGS ... L7=pass`, `TARGET executed_rows=38 ... defects=0`, `PREDICATE R94-C1 pass`, rc 0 | `DEFECT L7 ledger member=executed round=94 executed_total=39 cells={'file-artifact': 30, 'stdout-inspection': 13, 'subprocess-exec': 15} set_added=['fix-code-vulnerability', 'write-compressor']`, `PREDICATE R94-C1 fail`, rc 1 | **PASS -> FAIL** (H2) | `receipts/round94-c1-BASE.txt`, `round94-c1-T.txt` |
| `round93_c1_replay.py --rev` | `DEFECT L7 ... executed_total=38`, `PREDICATE R93-C1 fail`, rc 1 | `DEFECT L7 ... executed_total=39`, `PREDICATE R93-C1 fail`, rc 1 | fail -> fail (pre-existing) | `round93-c1-BASE.txt`, `-T.txt` |
| `round92_c1_replay.py --rev` | `DEFECT L7 ledger member=executed round=92 executed_total=38 cells_ok=False`, `PREDICATE R92-C1 fail`, rc 1 | `... executed_total=39 cells_ok=False`, fail, rc 1 | fail -> fail (pre-existing) | `round92-c1-BASE.txt`, `-T.txt` |
| `round87_c2_wording.py --rev` | `TARGET mismatches=0 defects=0 total=8 schema=6 control=2`, `PREDICATE R87-C2 pass`, rc 0 | identical, pass | none | `round87-c2-wording-*.txt` |

Process note: the 92/93 replays ran for minutes; two of my first background batches hit the 300 s cap and left partial receipts. The reruns used `timeout 0`. One rerun reused a work dir that a failed `rm -rf` had left half-populated and produced a tar-extraction traceback; it was rerun in a fresh work dir and its receipt was overwritten by that run. The receipts listed above are the complete runs.

### H1 (major): round-87 counter flips PASS -> FAIL at T

Verdict-level: `plans/round87_c1_replay.py --rev afe9c229` prints `PREDICATE R87-C1 fail`, rc 1, with `DEFECT L7-ledger row {"classes": ["file-artifact"], ..., "subject": "tb2-header", "verdict": "cases"}`. At BASE the same command prints `PREDICATE R87-C1 pass`, rc 0.

Cause: the C commit's correct subject correction (tb2-result-file -> tb2-header, §1a, and the only shape the round-79 gate accepts). The round-87 counter's frozen `LEDGER_SUBJECT` expects the stale value. At T the two standing counters cannot both be green: round-79 needs tb2-header, round-87 needs tb2-result-file. The round-87 counter is not in the round-95 frozen table, but per the FROZEN RULE I did not and cannot repair it in round. Routed to round 96: re-pin `LEDGER_SUBJECT` to tb2-header (or re-derive it from the shape list), and re-run it at T.

H1 touches only the round-87 counter and the ledger row it reads; the round-95 claims are not evaluated by that counter, so this flip does not change any round-95 predicate.

### H2 (minor, by cause): round-94 counter flips PASS -> FAIL at T by ledger growth

`round94_c1_replay.py` L7 pins `EXECUTED_AFTER = 38` (its own round's tip) and requires the executed set to equal the 0cbb9279 set plus write-compressor. At T the executed set is that set plus write-compressor plus fix-code-vulnerability (`set_added=['fix-code-vulnerability', 'write-compressor']` is relative to the 0cbb9279 base; the write-compressor entry is expected, the fix-code-vulnerability entry is the round-95 flip). Its L7 is a snapshot check and red at any later tip with one more executed member.

Same pattern is already present at BASE: counters 90 (EXECUTED_AFTER=34), 91 (35), 92 (36), 93 (37) are red at BASE against the BASE total 38 (round 92 and 93 measured above; 90 and 91 read from their constants, not re-run [INFERENCE]). So this is not a new harm class from the C commit, but it is a standing counter going green->red at T, so it is reported. Routed to round 96: snapshot-pinned L7 totals are unstable under any ledger growth; re-pin or key them to the member set.

## 4. Info / minor (no verdict flips)

- I1 (minor, doc): SKILL.md class cells updated by the C commit change only the numeric `executed k of n` text. Their parenthetical round attributions were not extended to round 95 for fix-code-vulnerability (the file-artifact cell lists rounds 81-88; the serialization-schema cell lists rounds 85-86). Verified: the non-count text of SKILL.md at T is identical to BASE (the diff after normalising `executed N of M` is empty; `receipts/C-commit-SKILL-ledger.diff`, 20 changed SKILL lines, all count cells).
- I2 (info): round92 receipt carries `PREDICATE R92-PROBE pass`, which the frozen predicate shape `^PREDICATE R<n>-C<m> pass` does not match. The ledger verdict `cases` is what the frozen rule yields; the verdict is correct under the rule, the receipt's naming is outside it.
- I3 (info): the round-79 gate's ledger subject checks compare against receipt header shapes, but it has no check that a standing counter's frozen expectation agrees with the ledger. That is the gap behind H1.

## 5. Overlap

Only the round-79 ledger/SKILL cells (C commit) and the round-87/92/93/94 counters that read ledger rows were checked. No overlap with the R95-C1 replay or the R95-C2 census beyond the ledger rows they read. The round-95 C1 counter (`plans/round95_c1_replay.py`) and census were not run by this seat (other seats).

## Findings

FINDING H1 major round-87 counter flips PASS->FAIL at T (`DEFECT L7-ledger row ... "subject": "tb2-header"`, `PREDICATE R87-C1 fail`, rc 1); C's correct subject fix conflicts with the frozen LEDGER_SUBJECT; route R96
FINDING H2 minor round-94 counter flips PASS->FAIL at T (`executed_total=39`, EXECUTED_AFTER=38); ledger growth, pre-existing pattern for 90-93; route R96
FINDING I1 info SKILL.md class cells lack round-95 attribution text (count cells correct; non-count text unchanged)
FINDING I2 info round92 receipt PREDICATE line uses R92-PROBE shape; verdict cases is correct under the frozen rule
FINDING none for legacy gate (14 -> 0 exactly mapped to C-commit ledger/SKILL edits), grader, state_check, round68, round91, anchor_line_check, sources-census (explicit dirs at BASE and T)

## Files
- `.ufo/waves/round-95/w1/ExecLegacyHarm/report.md` (this file)
- `.ufo/waves/round-95/w1/ExecLegacyHarm/receipts/*.txt` (raw gate and counter output, rc-terminated)
- `.ufo/waves/round-95/w1/ExecLegacyHarm/receipts/ledger-BASE.json`, `ledger-T.json`, `C-commit-SKILL-ledger.diff`
- `.ufo/waves/round-95/w1/ExecLegacyHarm.md` (scoped findings copy)

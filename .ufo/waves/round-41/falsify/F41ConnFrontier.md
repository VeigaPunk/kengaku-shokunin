# F41ConnFrontier — connector falsify report (round 41 wave 2)

Seat: F41ConnFrontier (connector, leaf). Lane: kengaku-shokunin @ tip
`74513c0625df7886357b866074104a0cf4bf9cc1`. Scope: after landing, do any
self-assessment lines in SCORECARD.md, SHONEN.md, corpus/README.md (coverage
map, §Frontier, open gaps) or PROVINCE.md mismatch the repo state? And is
"7 of 89" / "class new to the lane" wording right against the six earlier
TB2 entries?

Axes (godspeed): A1 count-truth (every number in the four files traceable to
repo bytes), A2 denominator-truth ("89", "7", "82" against the pinned TB2
tree), A3 class-truth ("embedded-scheduling-model class" vs the six earlier
graders), A4 cross-file consistency (progression 3→4→5→6→7 read).

## 1. Denominator truth: "89" and "7" — verified against the pinned tree

Clone of upstream at the pin (scratch, read-only usage):

```
$ git init -q tb2 && git -C tb2 remote add origin https://github.com/harbor-framework/terminal-bench-2
$ git -C tb2 fetch -q --depth 1 origin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
$ git -C tb2 checkout -q FETCH_HEAD
$ git -C tb2 rev-parse HEAD
2fd12b88aafdd04a52c298e3940bcb189f9766d6
$ find . -maxdepth 2 -name task.toml | wc -l
89
$ find . -maxdepth 3 -path '*/tests/test.sh' | wc -l
89
$ for d in */; do [ -f "$d/task.toml" ] && [ ! -f "$d/tests/test.sh" ] && echo "$d"; done
(empty)
```

- 89 task directories at the pin, each carrying `task.toml` **and**
  `tests/test.sh` (plus LICENSE, README.md, hidden .gitignore → 91 visible
  root entries, matching S100's "92 top-level entries" count where
  .gitignore is included).
- The seven read graders map 1:1 to tasks at the pin: protein-assembly,
  regex-log, configure-git-webserver, build-pmars, git-leak-recovery,
  db-wal-recovery, constraints-scheduling (S105–S123). So **"7 of the 89
  TB2 task graders"** (corpus/README.md:269), **"(7 of 89 read)"** (§Frontier
  round-41 sub-bullet, corpus/README.md:356) and **"remaining 82 TB2 task
  graders (89 carry `tests/test.sh`; 7 are read)"** (PROVINCE.md:507) are all
  correct: 89 − 7 = 82. The progression is internally consistent
  (PROVINCE.md:276 3/86, :303 4/85, :397 5/84, :445 6/83, :507 7/82).

## 2. Capture identity: the entry's pins equal the upstream bytes

Re-fetched the pinned raw files and compared to the lane's captures:

```
$ curl -sS https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88.../constraints-scheduling/tests/test_outputs.py ...
$ sha256sum -c <capture SHA256SUMS>   # for the 5 re-fetched paths
MATCH test_outputs.py (1422b345…)  MATCH instruction.md (342def78…)
MATCH test.sh  MATCH task.toml  MATCH Dockerfile  MATCH solve.sh
MATCH alice/bob/carol_calendar.ics
```

(correct upstream paths: `environment/Dockerfile`, `environment/inputs/*.ics`,
`solution/solve.sh`; my first fetch used wrong paths → "404: Not Found" 14-byte
bodies — those DIFFER lines in my log are fetch-path artifacts, not capture
mismatches.) S122/S123/S124 rows describe the pinned files as captured, and the
entry's falsifier clause (a) stands.

## 3. Class truth: "embedded-scheduling-model class" vs the six earlier entries

Read the captured constraints grader (`test_outputs.py`): `_overlap` (:46-55),
`_hard_ok` (:58-83), minute-granularity earliest-slot scan (:158-167) over the
three sha256-pinned calendars — the *verdict is computed from input data*, not
compared to a literal. Contrast with the closest prior grader (db-wal-recovery,
captured): seven pytest functions are literal/structural assertions over the
parsed JSON (`json.load`, field types, sortedness, eleven ids with pinned values
— test_outputs.py:7-107); no input data feeds a decision model. The other five
earlier graders are likewise artefact-vs-literal/pattern assertions (substring,
regex scan, git-state checks). So "the verdict is no longer an assertion over a
fixed artefact but a computation" (corpus/README.md:269), "a grader class new to
this lane" (corpus/knowledge/tb2-constraints-scheduling-grader.md:47-51) and
"The graded state is a class new to this lane: … whose verdict is *computed* by
a scheduling model embedded in the test file" (PROVINCE.md:477-479) are right:
the class is new within the executed sample, and it does not collide with the
earlier class labels (R37 "one new executed edge class"; R38 "build-provenance";
R39 "repository-history"; R40 "binary database file pair"). The entry's own
scoping — "not a new verdict channel … not a new reading" — matches.

## 4. Every round-41 number in the four files traces to repo bytes

| File:line claim | Verification |
|---|---|
| SCORECARD.md:1539 C1 before `BATTERY fixtures=0 … PREDICATE C1 fail` | `claims/control-c1-nothing.txt` prints exactly that; baseline `measure-baseline.txt` agrees |
| SCORECARD.md:1539/1563 C1 after `fixtures=48 wrong=0 tampered=0 sidechannel=0`, `total=23 killed=23 survived=0 invalid=0 null_detected=0`, `receipts=13/13 sources=10/10`, `ADVERTISED direct=21 indirect=2 none=0`, `PINS total=2 mismatched=0`, `PREDICATE C1 pass` | `measure-final.txt` lines 4,76-82 |
| SCORECARD.md:1540 C2 "knowledge files/index rows 47→48, SOURCES 114→117; S124 … closed unmerged" | `measure-final.txt:800` `registry_rows=117 knowledge_files=48 index_rows=48`; `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 117; `ls corpus/knowledge/ | grep -c '\.md$'` → 48; SOURCES S122/S123 tier A + S124 tier B (rows 137-139) → +2 A/+1 B; S124 state=closed merged=false |
| SCORECARD.md:1564 capability `embedded-model-grader-probe` `cases=25 observed_pass=6 observed_fail=19 mismatches=2`; "byte-equal re-run (measure-final.txt `constraints_probe exit=0 byte_equal=yes`)" | receipt tail `cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `regrade cases=25 differ=0`; measure-final.txt:768 `constraints_probe exit=0 byte_equal=yes`; R41CritPytest.md `VERDICT: pytest-parity-25/25` |
| SCORECARD.md:1565 `routed-findings-burndown` `ROWS total=10 open=4 blocked=1 closed=5 refused=0`, `routed_open=5 oldest_round=39`, `SELFTEST 12/12` | live run reproduced identical output; `--selftest` → `SELFTEST 12/12`, exit 0 |
| SCORECARD.md:1552-1557 no-harm block | `measure-final.txt`: anchor `rows=117 tokens=24 defects=0` (:625), frozen digests rounds 39/40/41 all OK (:645-671), ledger-tip `mismatches=0` (:690), tip receipts `receipts=27 byte_equal=7 differ=0 skipped=20` (:729), census `exit=0 warnings=15` (:797), `order_check` rounds 39/40/41 PASS, round 38 FAIL as before |
| SCORECARD.md:1549 "L1 checked … `corpus/README.md` §Frontier '7 of 89 read'" | §Frontier round-41 sub-bullet (corpus/README.md:343-359) reads "(7 of 89 read)" — matches |
| corpus/README.md:269 coverage bullet "(7 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict)" | verified §1; wording matches the frozen claim "7 of 89" (plans/round-41-claims.md:84) |
| corpus/README.md:74 index row, §Frontier bullet, PROVINCE.md §Round41 partial frontier admission | all present, all quote the same `cases=25 observed_pass=6 observed_fail=19 mismatches=2` and same class wording |
| PROVINCE.md:470-529 Round41 paragraph | "remaining 82 … (89 carry `tests/test.sh`; 7 are read)" verified §1; `regrade cases=25 differ=0` matches receipt; `stagecheck cases=25 failed=0` matches `claims/c2-stage-check.txt`; "16 of the 25 cases are the round-40 planning seat's pilot" matches claims file :12-16 |
| QUALITY.md Q31/Q32 (referenced by SCORECARD.md:1572) | both criteria present at the end of QUALITY.md (Q31 :571-622, Q32 :624-675); lesson `corpus/lessons/round-41.md` now exists (was "does not exist at this draft" in Q31's dated note — historical, not a current-state claim) |

## 5. SHONEN.md

Four-pointer checklist; no round-41 content. The `PROVINCE.md:129` pointer
resolves to the `### Adjacent` section header (the cross-domain-routing
section), so "No cross-domain bleed (PROVINCE.md still accurate)" still lands on
the relevant area. No mismatch.

## 6. Result

- Mismatches found between round-41 self-assessment lines and repo state:
  **0**.
- "7 of 89": right — 89 task graders exist at the pin, 89 carry
  `tests/test.sh`, and exactly 7 have been read (all seven mapped to tasks at
  the pin).
- "class new to the lane": right — the constraints-scheduling grader is the
  first in the executed sample whose verdict is computed by a model embedded in
  the test file over pinned input calendars (code cites §3); the phrase's
  repetition across R38-R41 refers to distinct classes, so it does not
  contradict the six earlier entries.
- Observations (not counted as mismatches): (a) QUALITY Q31's note "lessons/
  round-41.md does not exist at this draft" is a dated freeze-time note and is
  now superseded by the lesson's existence; (b) SCORECARD C2's "before"
  (`checks=8 defects=5`, V2/V3/V4/V7/V8) cites the freeze control
  (`claims/control-c2-nothing.txt`, which prints exactly that), while the
  measured baseline at `fc79f2a4` shows `defects=4` because there V8 passed —
  the scorecard cites the control, so this is not a mismatch.

All commands above ran read-only against the lane (or in scratch); no lane file
was modified. Scratch `/fast/scratch/hyaku/kengaku-r41/F41ConnFrontier` deleted
at close.

VERDICT: mismatches-0

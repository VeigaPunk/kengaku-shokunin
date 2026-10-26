# F41ConnClaims — connector: cross-document drift check (round 41, wave 2, falsify)

Seat: F41ConnClaims (connector, leaf). Scope: every number and hash in the task list across
`plans/round-41-claims.md` (freeze `8ef8b4f`), the counters' docstrings
(`plans/round41_c1_verify.py`, `plans/round41_c2_verify.py`), `.ufo/waves/round-41/claims/*`,
`.ufo/waves/round-41/integrate/measure-final.txt` and `measure-baseline.txt`, SCORECARD round-41 /
LOG round-41 text, `corpus/lessons/round-41.md`, the entry `corpus/knowledge/tb2-constraints-scheduling-grader.md`,
and the README (corpus/README.md index row, coverage bullet, §Frontier sub-bullet) + SOURCES rows S122–S124.
All commands were read-only against the lane (no git/jj mutation, no writes outside report/scratch).

## Method

Ground truth taken from `integrate/measure-final.txt` (landing measurement, clean clone) and the committed
freeze controls; every doc number was compared against it with the command shown.

## Target numbers — verdict per item

| target | commandments | result |
|---|---|---|
| 23 mutants / 13 receipts / 10 sources | `sed -n '128,233p' plans/round41_c1_verify.py | grep -c '^\s*("T\|^\s*("S'` → 23; claims:35; scorecard:1539; LOG:1240; lesson:7; C1 docstring `TOTAL=23`/`FLOORS={receipts:13,sources:10}` (round41_c1_verify.py:123-124); measure-final `MUTANTS total=23 killed=23`, `MUTANTS-BY-TOOL receipts=13/13 sources=10/10` | all agree |
| 21/2 adv kinds | `sed -n '128,233p' ... | grep -o '"direct"' | wc -l` → 21; `"indirect"` → 2 (T06, S11); `"none"` → 0; matches claims:37, control-c1-nothing:28, measure-final:79, SKILL addendum:650-651 | all agree |
| 48 fixtures | battery41 modules: r_ctl=4, r_map=10, r_run=4, r_setup=8, s_exit=6, s_modes=8, s_usage=8 = 48 (read `plans/battery41/{s_exit,s_modes,s_usage}.py` FIXTURES lists; r_* dicts literal) — matches `BATTERY fixtures=48` (measure-final:76), landing commit subject `74513c0` ("7 modules, 48 fixtures"), LOG:1239-1240, lesson:6, scorecard:1539; 48 FIXTURE lines counted in measure-final C1 section | all agree |
| probe 25/6/19/2 | receipt:33 `cases=25 observed_pass=6 observed_fail=19 mismatches=2`; dry table tail `cases=25 predicted_pass=6 predicted_fail=19`; V4 `cases=25 mismatches_named=2/2` (measure-final:98); pass cases counted by hand = 6; `match=NO` rows = later-valid-wed-1105, seconds-30 (receipt:10,18); stage-check `stagecheck cases=25 failed=0` | claims:10,89-90; lesson:8-9; scorecard:1540,1553; LOG:1242; PROVINCE:475; entry:29; SKILL:597,1069 | all agree |
| 114→117 | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 117; `git show 8ef8b4f:corpus/SOURCES.md` → 114 ; measure-final tail `registry_rows=117`; lesson:106; scorecard:1540,1573 | all agree |
| 47→48 | `git ls-tree -r --name-only HEAD corpus/knowledge/ | grep -c '\.md$'` → 48; at `8ef8b4f` → 47; `grep -c '^| `knowledge/' corpus/README.md` → 48 (47 at freeze); measure-final `knowledge_files=48 index_rows=48`; control-c2-nothing P8 `index_rows=47 knowledge_files=47`; lesson:106 | all agree |
| freeze/first/landing hashes | `git log --format='%h %s' -1 8ef8b4fc7c6302c527db90244d69aa18f53e83bf` → "round-41: freeze — claims, C1/C2 counters …"; `f774a87ad071122acd39ba02a9901b5b56d9910a` → "first recorded constraints-scheduling probe run (25 cases, mismatches=2 …)"; `74513c0625df7886357b866074104a0cf4bf9cc1` → "land battery41 (7 modules, 48 fixtures), C2 …"; all three ancestors of HEAD (`git merge-base --is-ancestor`). Docs: claims:3-4 (baseline `e50c1345`), lesson:3-4 (`8ef8b4fc`/`f774a87a`/`fc79f2a4`/`74513c06`), scorecard:1531-1532, LOG:1233-1236, measure-final TIP `74513c06…`, measure-baseline TIP `fc79f2a4…`, order gate outputs `freeze=8ef8b4f… receipt_commit=f774a87a…` (measure-final:107-108,196-199) | all agree |
| C1 before/after controls | control-c1-nothing: `fixtures=0`, `total=23 killed=0 survived=23`, `receipts=0/13 sources=0/10`, fail, exit 1; control-c1-no-mutants: `fixtures=22`, `total=0`, fail, exit 1; control-c1-witness-as-battery: `fixtures=22`, `killed=23/23`, pass, exit 0; witness-run: `fixtures=22`, `killed=23/23`, `ADVERTISED direct=21 indirect=2 none=0`, dev-mode `n/a`, exit 0; control-c1-tool-edited: `PINS mismatched=1`, T01–T13 `invalid`; control-c1-hostile: `sidechannel=1`, `build_write=OSError.lane_read=FileNotFoundError`, no markers | claims:43,53-67; lesson:15-17 | all agree |
| C2 before/after | control-c2-nothing: `checks=8 defects=5` (V2,V3,V4,V7,V8), fail, exit 1; baseline measure: `defects=4` (V8 ok), lesson:43-47 documents both; final `checks=8 defects=0` pass exit 0 | claims:97-100; scorecard:1540-1541 | all agree |

## Hash/pin cross-check

`claims/frozen-digests.txt` pins match the constants inside the counters (tip_receipts `e4f49714…`,
sources_adopt `38492bf1…`, probe `8c471fbd…`, dry table `a656ce9b…`, spec `8e96421d…`, gate `ea638822…`)
and `round41_c2_verify.py` `CAPTURES` equal `SHA256SUMS` entries (10 files + SHA256SUMS = 11 entries; V1 `listed=10`).
`plans/round-41-claims.md` sha256 `3b239b50…` matches `ROUND-CLOSE claims=… sha256=3b239b50…` (measure-final tail).

## Surrounding facts checked

- `git rev-parse --short HEAD` = `d7c7789` (wave-2 falsify dispatch); tip `3d0058f` (wave-1 reports) is an
  ancestor and exists with matching subject.
- Pilot provenance: `.ufo/waves/round-40/build/R40PlanNext/cs/run1.txt` tail `cases=16 observed_pass=3
  observed_fail=13 mismatches=2`; dry-table first 16 cases are `(pilot)` (grep lines 12-27; line 33 decoy-second
  is new); claims:12-16 carries it verbatim.
- `main()` killed 2 of 32 claim (claims:31) traces to `build/R40PlanNext.md:19,324`; SKILL.md:573 `sources-adopt`
  row lists the eight error codes (0 plus 2-9) used as directions.
- routed-findings rider: `corpus/routed-findings.jsonl` 10 rows, open=4 blocked=1 closed=5 → `routed_open=5
  oldest_round=39` (scorecard capability row `ROWS total=10 open=4 blocked=1 closed=5 refused=0`; LOG:1256).
- Census: `warnings=15` W04 unchanged before/after (claims/census-before.txt, measure-final tail); merge re-screen
  collisions 38 → 41-on-landing consistent.

## Disagreements found

None in the listed number set. Two non-numeric prose notes, both already disclosed in-lane (not new drift):

1. Claims:27,34-35 "no committed fixture demonstrates" vs the freeze commit's own witness modules killing 23/23 —
   recorded as erratum in SCORECARD:1543-1545 and lesson:20-21 (claims file frozen, unchanged).
2. Claims:105 "published (TB2.1 PR #245)" vs the PR's live state closed-unmerged — recorded as a mistake in
   lesson:17 and the Gate row S124; SOURCES S124 now carries "closed unmerged at access".

## Proposed move

None required: all target numbers and hashes agree across the seven surfaces. No axis harmed; calibration/coverage
narrative stays as landed. (L1 may optionally drop the `write=denied` phrase in claims:67 alongside the existing
erratum note, since the recorded hostile control shows the marker absence and `OSError`/`sidechannel=1` but does not
echo the stub's stdout; this is wording, not a number.)

## Verification

Re-run commands (all read-only): the `grep`/`sed`/`git show`/`git ls-tree` commands above; `git merge-base
--is-ancestor {8ef8b4f,f774a87a,74513c0,3d0058f} HEAD`; `sha256sum` of the claims file vs the `ROUND-CLOSE`
line; read of the three s_* battery FIXTURES lists; tail of run1.txt and dry table.

VERDICT: drift-0

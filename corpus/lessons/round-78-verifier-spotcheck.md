# Round 78 — verifier spot-check (kengaku)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04 (UTC)
lane: `kengaku-shokunin`
base `3ae0ab540c35fe40da048198f3e5d4042766b2b7` (round-77 verifier spot-check)
lane tip `148801a67aebe7bf062932556083131fe96a2d39` (remote verified: `git -C kengaku-shokunin ls-remote origin refs/heads/master` → the same hash)
report `.ufo/reports/round-78/kengaku.md` @ `12a4fec14ef0e0aa0f1791a9966ff476fdf39c52`
dispatch/complete digest (mutable `.ufo/watchdog.log`, copied):
`2026-11-04T02:55:33-03:00 launch kengaku round=78 pgid=48359 driver=hyaku-inline attempt=1`;
`2026-11-04T03:18:55-03:00 complete kengaku round=78; hyaku-inline attempt=1`.

This file is integrator work, not lane work: I did not author the round and changed no lane-authored
file. Every number below was re-derived by me over committed bytes with plain `git`/`grep`/`awk`/`jq`
reads. The lane's counters were **not executed**: the Gate standard's Closure consequence binds the
integrator to verify a gate's committed evidence (self-test tally, frozen-run verdict, revision
measured), never to run a sibling's gate. My ad-hoc re-derivation script lived under `/tmp` and is
not citable; the commands below are the re-runnable form.

## 1. Step-1 conformance

| item | result |
|---|---|
| report identity | `git log --format='%h author=%an <%ae> committer=%cn <%ce>' -- .ufo/reports/round-78/kengaku.md` → `12a4fec1 author=kengaku-shokunin <kengaku@shokunin.local> committer=kengaku-shokunin <kengaku@shokunin.local>`; committer time 2026-11-04T03:18:17-03, seven seconds after the cited lane tip commit 03:18:10 — the report lands last. The earlier draft `fc8da0e0` cited `49d4f0e1`, which existed then; the final bytes cite `148801a6` |
| SHONEN heading | `grep -c '^## SHONEN'` → 1; four `[~]` lines with pointers against the four boxes in `SHONEN.md`; no `[x]` |
| cited commits | 15/15 exist and are ancestors of `master`: the 14 round commits `2f9eeafb cd2e25bb f20a2f6f bbf4f36c a0e86c10 e4c661ab 3cc5cecb 749c2a40 2aa6c4e4 b47dbea8 04fdd644 49d4f0e1 63fb46ba 148801a6` plus the cited base `3ae0ab54`; `git merge-base --is-ancestor <hash> master` returned 0 for each |
| lane state | `jj-lane.sh state` → `branch=master local=148801a67aebe7bf062932556083131fe96a2d39 remote=148801a67aebe7bf062932556083131fe96a2d39 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty — no uncommitted round work |
| prompt fidelity | `.ufo/prompts/kengaku-round-78.md` lines 1–140 diff against `templates/round-prompt.md` with only the five placeholder substitutions (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`, `<kengaku-repo>`); report path, commit-before-report ordering, `SHONEN` heading, commit-hash citation rule and lane write scope are present (grep hits at §4/§5 and addendum item 3); the L2 floor is `8` (`## 3`), matching `MISSION.md` §L2 concurrency (`at least 8`); the run-15 addendum `## 6` and scratch `## 7` follow |
| wave | one v1 wave, 11 spawn / 11 results (`w1-dispatch.json` `counts.spawn=11`; `w1-results.json` 11 non-empty outputs, 0 dead), band 8–16; roles executor 3, scribe 2, scout 1, critic 1, reviewer 1, mutation-tester 1, sentinel 1, connector 1; attack seats (reviewer, critic, mutation-tester) 3/11 = 27 % ≥ 25 %; connector 1 ≤ 2 |
| marker vs report | not a marker: 184 lines, both claims with named counting commands, evidence pointers per work item, all eight required sections present |
| report sections | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN, Stale-lane, Tool installs — in the contract's order |

No step-1 defect bars admission. Evidence-standard defects are routed in §6.

## 2. Claims — re-derived, not evidence-read

### R78-C1 / coverage — 12-member ledger

Re-checked from committed bytes at the tip:

```
$ git -C kengaku-shokunin cat-file -e 3ae0ab54:plans/grader-selected-members.json; echo rc=$?
rc=1                                   # the ledger does not exist at base
$ jq '.members|length'            kengaku-shokunin/plans/grader-selected-members.json
12
$ jq '[.members[]|select(.status=="executed")]|length'   … → 7
$ jq '[.members[]|select(.status=="unexecuted")]|length' … → 5
$ grep -c 'ledger=plans/grader-selected-members.json' kengaku-shokunin/SKILL.md
3
```

- **Universe, derived.** `SKILL.md` §Decision table carries exactly the three partial rows
  `network-service 4 of 8`, `process-environment 2 of 3`, `db-state 1 of 2` (awk over the table,
  fenced blocks skipped); the round-62 census's `CLASS … members=` lines yield 12 distinct members
  over 13 member-class pairs — 12 members, 13 pairs (awk, `2026-11-04`). The ledger's key set equals
  the census universe exactly (12 vs 12; `jq` key sort) and the per-class executed counts are 4/2/1,
  matching each row's `k`.
- **Executed rows (7).** Each receipt exists, is tracked (`git ls-files --error-unmatch`), prints
  `PREDICATE R<n>-C1 pass` — for `torch-pipeline-parallelism` the `vectors` form, six
  `VECTOR … frozen=match` lines and no `frozen=mismatch` — and names its task (`TASK-UNDER-TEST
  <member>` or the member string in the header).
- **Unexecuted rows (5).** Every reason is in the frozen enum (`browser-required`, `vm-required`,
  `network-install-required`, `external-db-required`, `candidate-library-required`) and its frozen
  regex fires over the stored grader bytes `corpus/evidence/round52/graders/<member>/tests/{test_outputs.py,test.sh}`.
- **Committed before/after.** `c1-before.txt` → `DEFECTS n=21`, `unaccounted=12`, rc 1;
  `c1-after.txt` → `DEFECTS n=0`, `TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0
  unbacked=0`, rc 0. Both match the report.
- **Batteries (evidence-read, not re-run).** `c1-selftest.txt` `cases=8 red=7 failures=0`;
  `c1-mutants.txt` `real=6 killed=6 survived=0`; `c1-control-prose.txt`
  `members_named=0 receipts_resolved=0 reasons_backed=0 target_reached=False`.

Verdict: **verified (re-measured)**.

### R78-C2 / calibration — receipt stamp location

Rule re-derived: the **last** `LANE_TIP` block governs; a receipt is located iff its tip resolves and
is an ancestor of `master`; `TOOL` + a full 64-hex `TOOL_SHA` recomputed with
`git show <tip>:<tool> | sha256sum` (or `TOOL-SUPPLIED` + `WORKTREE dirty` with the named path
present in the audit tree); `COMMAND` present; no conflicting tip without a re-stamp marker.

- **Before @ `3ae0ab54`.** 16 verdict-bearing receipts; **2 located / 14 unlocated** under that rule.
  Matches `c2-before.txt` (`UNIVERSE dirs=2 receipts=16`, `TARGET receipts=16 located=2 unlocated=14`).
- **After @ `148801a6`.** 26 verdict-bearing receipts; **26/26 tips resolve and are ancestors**;
  **26/26 tool digests recompute at their own stamped revision** (12 re-minted at `cd2e25bb`, three
  reruns again at `bbf4f36c`, six round-78 receipts, four appended re-stamps with `TOOL-SUPPLIED` +
  `WORKTREE dirty` for `c1-before`, `c2-before`, `exec-attrib-calibration`, `exec-state-check`);
  `COMMAND` present on all; no `SUPPLIED-BUT-CLEAN`; no unlabelled `STAMP-CONFLICT`. Matches
  `c2-after.txt` (`DEFECTS n=0`, `TARGET receipts=26 located=26 unlocated=0`).
- **Batteries (evidence-read).** `cases=7 red=6`, mutants `6/6`, control
  `receipts=6 stamped=6 located=6 real_defects=4 target_reached=False`.

Verdict: **verified (re-measured)** — the frozen predicate holds. The claim's prose clause that the
round-77 stamp-prose and at-tip rerun-block items are "corrected" is only partly true; the
documentation defects are routed as R78-D2/R78-D3 and do not move the predicate.

## 3. Discernment spot-check (`corpus/lessons/round-78.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S254 Git `git-status` documentation | admit (tier A, `mined`) | live `https://git-scm.com/docs/git-status` (HTTP 200, 100 062 B, sha256 `22ff28ff…b0180`, byte-identical to the committed capture `corpus/evidence/round78/sources/git-status.html`); quote at capture 2322 + 2326 | **agree** | the quote is present in the rendered text and grounds untracked-file semantics — the exact rule behind `WORKTREE clean`; tier A is right for official docs. Citation metadata is off: the quote is 15 words (not 17) and spans capture lines 2322 and 2326, not 2322–2324 |
| S255 lane round-62 class census (`own-work`) | admit (tier A, `mined`) | path `corpus/evidence/round62/class-survey.txt`; sha256 `ee30c698…d45613` matches the row; quote `EXECUTED-COVERAGE …` at line 21 | **agree** | a lane-produced, re-runnable instrument's output is legitimate tier A `own-work`; the quote exists. The row anchor says "lines 1–9", but the quoted `EXECUTED-COVERAGE` line is line 21 — anchor text defect |
| "a class count in a prose table is evidence of class membership" | reject | `SKILL.md` §Decision table row `network-service` + census line 11 | **agree** | the `executed 4 of 8` cell names four of eight members; membership exists only in the census member list. The flip (name every member, resolve one receipt per execution) is what the ledger now does |
| "a `LANE_TIP` line locates a receipt" | reject | `corpus/evidence/round78/c2-control-stamp-only.txt` + base `corpus/evidence/round77/c1-before.txt` | **agree** | the stamp-only control reaches `located=6` while `real_defects=4`; the base `c1-before` carries tips but no tool pair/command in its last block. Digests + command are what locate a receipt |

Census gate: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
→ rc 0, `ok …/corpus/SOURCES.md`, 25 `W04` duplicate-URL warnings (count from the same run's output, 2026-11-04).

## 4. Trend verdicts

- **expansion: improved.** Three capability rows enter `SCORECARD.md` with a demonstrated command and
  a committed receipt (`grader-class-member-ledger`, `receipt-stamp-location-gate`,
  `receipt-restamp-append-only` — `corpus/evidence/round78/c1-after.txt`, `c2-after.txt`,
  `plans/round78-restamp.json` + `f20a2f6f`), and the registry gains two opened, tiered, cited rows
  (S254 live-verified, S255 hash-verified). No new `corpus/knowledge/` entry — declared, not hidden.
- **quality: improved.** 16 round-77 receipts were superseded by located ones (before 2/16 located,
  after 26/26 — the counts above), the inherited missing index row was repaired (base
  `git show 3ae0ab54:corpus/README.md | grep -c round-77-verifier-spotcheck` → 0), and the inherited
  `EMPTY-SCOPE` was closed by the R76-C2 amendment. Caveat routed as R78-D5: `R51-C1` and `R77-C1`
  were **green at base** (base `rerun-r51-c1.txt` `PREDICATE R51-C1 pass`; base round-77 `c1-after.txt`
  `SURFACE 19 … rows=245 pin=245`, `DEFECTS n=0`, pass), so the "eight gates that were red or
  unmeasured at base" sentence overstates both the count (six are named) and the redness; the pin move
  245 → 247 is maintenance that kept them green, and is still a real freshness action.
- **discernment: improved.** The outside spot-check agrees on both admits and both rejects; the wave's
  attack seats changed committed bytes (Amendment A1's nine defect-only legs are present in both
  counters: `TOOL-PIN-SHORT`, `SUPPLIED-UNRECOVERABLE`, `STAMP-CONFLICT`, `TASK-MISMATCH`,
  duplicate-JSON-key hook, fenced-table skip, ≥2-vector rule, `RECEIPT-SYMLINK`,
  `MEMBER-NAME-ESCAPE`). Caveat: the three annotation defects R78-D1…R78-D3 were not caught by any
  criterion; the next round must mine them into a lesson row and either add a grounded `QUALITY.md`
  criterion (numbers must match the receipt they cite) or record why not.

## 5. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | **improved** | 12 members accounted (12 → 0 unaccounted), 3 class rows linked, 0 unbacked; score held at its L0 cap 7 |
| calibration | **improved** | 26/26 receipts locate at their own stamp (2/16 before); score held at ceiling 10, exercised |
| depth | unchanged | no new knowledge entry; S254/S255 + five Mistakes rows |
| operability | unchanged | two new gates and one repair driver are registered and evidenced; axis held at 10 (saturated) |
| freshness | unchanged | S254 re-fetched live and byte-identical; declared surfaces untouched; axis held at 10 |
| adjacency | unchanged | connector matrix 20 lanes, 0 duplicates, 22 adjacent, all routed not absorbed |
| novelty | unchanged | two instruments, no new construct claimed |

No axis harmed: `git diff 3ae0ab54 148801a6 -- SCORECARD.md` adds the round-78 section and changes no
score downward; the lane diff is additive except the three class-row pointers, the SF14 pin, and the
re-minted receipts the claim itself prices.

## 6. Routed defects (lane fixes next round)

- **R78-D1 (high) — the C2 before-defect breakdown is not derivable from its own receipt.** Report
  line 97, `SCORECARD.md:3615` and `corpus/lessons/round-78.md:53` print
  `11 TOOL-UNNAMED, 10 COMMAND-ABSENT, 4 PASS-UNLOCATED, 2 WORKTREE-ABSENT, 2 TOOL-UNPINNED` (sum 29);
  the committed `c2-before.txt` contains `11 TOOL-UNNAMED, 11 COMMAND-ABSENT, 5 PASS-UNLOCATED,
  2 WORKTREE-ABSENT` (sum 29) — `TOOL-UNPINNED` never fired in any committed c2-before version
  (`git log --all -- <path>` × `grep -c 'DEFECT TOOL-UNPINNED'` → 0 at every revision). The 10/4 split
  is the earlier 27-defect reading; the 2 `TOOL-UNPINNED` rows are invented to reach 29. Fix: append a
  dated correction naming the superseded split (append-only LOG/lesson) and correct the SCORECARD row
  with the per-class counting commands.
- **R78-D2 (medium) — the round-77 stamp-prose item is not actually corrected.** The report and
  `SCORECARD.md` say the stale `d181e16b` stamp prose was corrected, but `SCORECARD.md:3564` and
  `:3565` still print "stamped `d181e16b`, clean" for the two round-77 after receipts, whose committed
  stamps are `cd2e25bb` (both `c1-after.txt` and `c2-after.txt`). A correction note in the round-78
  section does not sweep the surviving mention (Evidence standard: corrections sweep every mention).
  Fix: dated in-place correction of the two round-77 rows plus `grep -rn d181e16b` proven empty (or
  every hit named as historical).
- **R78-D3 (medium) — the at-tip rerun block contradicts its own receipt.** `LOG.md:2963` and `:3017`
  print `routed_open.py` → `ROWS total=93 open=31 blocked=1 closed=59 refused=2`, while the cited
  `corpus/evidence/round77/rerun-routed-open.txt` prints `ROWS total=98 open=31 blocked=1 closed=64
  refused=2` and stamps `LANE_TIP bbf4f36c`, not the final tip. The block titled "at the tip" is
  therefore stale by five routed rows and one commit. Fix: append a correction entry and land a
  routed_open receipt at the tip.
- **R78-D4 (low) — S254/S255 citation metadata.** The S254 quote is 15 words, not "17 words", and its
  two sentences sit at capture lines 2322 and 2326, not 2322–2324 (report line 120, lesson line 18).
  The S255 row anchor says "lines 1–9" while its quoted `EXECUTED-COVERAGE` line is line 21. Fix:
  correct the lesson text and, because `anchor` is not in SOURCES v1's mutable set, add the superseding
  row or a dated correction naming the row it re-anchors.
- **R78-D5 (low) — quality-trend evidence overstates base redness.** "Eight gates that were red or
  unmeasured at base" names six, and two of them (`R51-C1`, `R77-C1`) were green at base: the base
  `rerun-r51-c1.txt` prints `PREDICATE R51-C1 pass` (`DRIFT 0`, `NUMBER-DRIFT 0`) at pin 245/count
  245, and the base round-77 `c1-after.txt` prints `SURFACE 19 … rows=245 pin=245`, `DEFECTS n=0`,
  `PREDICATE R77-C1 pass`. The C1 row also labels its after measurement `@04fdd644` while
  `c1-after.txt` stamps `LANE_TIP b47dbea8` (04fdd644 is the commit that carries the receipt). Fix:
  restate the quality paragraph with the two genuinely red gates (R75-C1, R76-C2) plus the two new
  unmeasured gates, and the real pin-maintenance sentence.
- **R78-D6 (low) — "clean tree" contradicted by the evidence file.** Report and commit message
  `148801a6` say the gate block was "re-run from the clean tree at `63fb46ba`", but the committed
  `.ufo/waves/round-78/gates-tip.txt` line 2 says `WORKTREE dirty`. Fix: either re-run the block in a
  clean clone and commit that receipt, or correct the prose. (Gate standard: a run over a moving
  worktree is not comparable to one over the cited commit.)
- **R78-D7 (low) — closure-artifact debt the lane must discharge.** This file
  (`corpus/lessons/round-78-verifier-spotcheck.md`) is unindexed in `corpus/README.md`, so R75-C1 will
  report `MISSING` at the next tip until the lane adds its row (the same debt round 78 discharged for
  the round-77 spot-check). Because this file is now the newest `round-*-verifier-spotcheck.md`,
  R76-C2 will derive ids `R78-D1 … R78-D7` and report `MISSING-ROW` until the lane registers them in
  `corpus/routed-findings.jsonl` (amendment A1's bare-id rule is what makes this queue visible).
  Expected routed-queue behaviour, not a regression: register each id with its close evidence when
  fixed.

## 7. Promotion note (operator-owned)

All four `SHONEN.md` boxes now carry `[~]` with a pointer, and every pointer resolves for a non-author
(the SKILL decision tables and registry rows, LOG round 78 with end-to-end runs, the executable
claim/counter bytes, and the PROVINCE/connector no-bleed evidence). The boxes look fully checkable by a
non-author from those pointers; promotion remains operator-owned and this closure does not mark them.

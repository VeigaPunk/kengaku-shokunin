# Round 79 — verifier spot-check (kengaku)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04 (UTC)
lane: `kengaku-shokunin`
base `660ec0b905957100b4122f655dda08f56c5b8b21` (round-78 verifier spot-check)
lane tip `f10a2678342efed6292864e8f273fb26f6297d11` (`git -C kengaku-shokunin ls-remote origin refs/heads/master` → the same hash)
report `.ufo/reports/round-79/kengaku.md` @ `1f8d67662d1ab02281d3959903f7eda21572e1fb`
dispatch/complete digest (mutable `.ufo/watchdog.log`, copied):
`2026-11-04T03:32:03-03:00 launch kengaku round=79 pgid=1259174 driver=hyaku-inline attempt=1`;
`2026-11-04T04:01:14-03:00 complete kengaku round=79; hyaku-inline attempt=1`.

This file is integrator work, not lane work: I did not author the round and changed no lane-authored
file. Every number below was re-derived by me over committed bytes with plain `git`/`grep`/`awk`/`jq`
reads. The lane's counters were **not executed**: the Gate standard's Closure consequence binds the
integrator to verify a gate's committed evidence (self-test tally, frozen-run verdict, revision
measured), never to run a sibling's gate. The commands below are the re-runnable form.

## 1. Step-1 conformance

| item | result |
|---|---|
| report identity | `git log --format='%an <%ae> %H %s' -- .ufo/reports/round-79/kengaku.md` → `kengaku-shokunin <kengaku@shokunin.local> 1f8d6766 round-79: kengaku report`. Committer time `2026-11-04T04:00:17-03:00`, 56 s after the cited lane tip `f10a2678` (`2026-11-04T03:59:21-03:00`): the report lands last |
| SHONEN heading | `grep -c '^## SHONEN'` → 1; four `[~]` lines, one per `SHONEN.md` box, each with a path pointer; no `[x]` |
| cited commits | 7/7 exist and are ancestors of `master`: `5d684313 42d9d60a e2d418ca dd302f48 e560695c 5302b92a f10a2678`; `git merge-base --is-ancestor <hash> master` returned 0 for each (`f10a2678` is the tip itself) |
| lane state | `jj-lane.sh state` → `branch=master local=f10a2678342efed6292864e8f273fb26f6297d11 remote=f10a2678342efed6292864e8f273fb26f6297d11 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty — no uncommitted round work |
| prompt fidelity | `.ufo/prompts/kengaku-round-79.md` lines 1–140 (`## 6. Campaign addendum` excluded) diff against `templates/round-prompt.md` with only the placeholder substitutions (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`, `<kengaku-repo>`); the five child-lane items are present (§4 report path `…/round-79/kengaku.md`, §5 commit-then-push, §4 `SHONEN`, commit-hash citation rule, lane write scope/push scope); the L2 floor is `8` (`## 3`), matching `MISSION.md` §L2 concurrency; the run-15 addendum routes roles through the host table and the report's 14-seat wave respects the 8–16 band |
| wave | one v1 wave: `w1-dispatch.json` 14 items, `w1-results.json` `seats=14` / 14 non-empty outputs / 0 dead. Roles: executor 5, scribe 3, critic 1, reviewer 1, mutation-tester 1, sentinel 1, connector 1, scout 1. Attack seats (critic, reviewer, mutation-tester, sentinel) 4/14 = 29 % ≥ 25 %; connector 1 ≤ 2; 14 seat reports on disk |
| report sections | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN — in the contract's order (then Round shape and seats, L0 questions) |
| marker vs report | not a marker: 199 lines, two claims each with a counting command and receipt, evidence pointers per work item, all six sections present |

No step-1 defect bars admission. The evidence-standard defects found are routed in §6.

## 2. Claims — re-derived, not evidence-read

### R79-C1 / coverage — 88-member population ledger

```
$ git -C kengaku-shokunin cat-file -e 660ec0b9:plans/grader-population-ledger.json; echo rc=$?
rc=1                                   # no ledger at base
$ jq '.members|length'  plans/grader-population-ledger.json            → 88
$ jq -r '.members|to_entries|group_by(.value.status)[]|"\(.[0].value.status) \(length)"' …
executed 18 · executed-unlocated 6 · unexecuted 64
$ jq '[.members[].classes[]]|length' … → 230        # member-class pairs
$ jq '[.members[].classes[]]|unique|length' … → 15  # container-image is empty
$ jq -r '.members|to_entries|map(select(.value.status=="unexecuted"))|group_by(.value.reason)[]|…'
browser-required 2 · candidate-library-required 3 · external-db-required 1 · unattempted 57 · vm-required 1
```

- **Universe, derived.** `corpus/evidence/round62/class-survey.txt` (sha256
  `ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613`, matching the S257 row) yields
  88 distinct real members over 230 pairs and 16 classes (`container-image` `members=-`); the ledger
  key set equals the census member set exactly (`comm -23`/`comm -13` both empty; the only census
  token outside the ledger is the empty-class `-`).
- **Statuses and blockers** reproduce the report exactly: 18/6/64, and 7 detector-backed blockers
  over four codes plus 57 `unattempted` (2 browser, 1 vm, 1 external-db, 3 candidate-library).
- **Executed rows (18).** Every `receipt` is tracked at the tip and names its member; subject shapes
  are the five frozen ones (`tb2-header` 10, `receipt-header` 3, `grader-path` 2, `task-under-test`
  2, `capture-tree` 1):
  `for each row: git cat-file -e f10a2678:<receipt> && git show … | grep -c <member>` → all 18
  present, mentions ≥ 1, e.g. `circuit-fibsqrt corpus/evidence/round42/fibsqrt-probe.txt` (6
  `CASE … observed=…` lines) and `nginx-request-logging corpus/evidence/round70/nginx/receipt.txt`
  (`TEST K1 test_nginx_installed P`).
- **Unlocated rows (6).** Each `instrument` is tracked, each `receipt` exists, and none of the three
  sampled receipts carries a `subject` stamp (0 hits) — the `no-subject-stamp` debt is real, not
  invented.
- **Class cells are derived, not quoted.** All 16 `SKILL.md` rows carry `executed k of n`
  (`grep -cE 'executed [0-9]+ of [0-9]+'` → 16; base: `3`, with 12 bare `executed` + 1
  `recipe-unexecuted`). Each `k` equals the ledger's replayed pair count for that class, and each
  `n` the class count:
  `signal 1/1, subprocess 10/45, shell 1/6, candidate-import 3/6, file-artifact 16/76,
  stdout 8/29, numeric 2/10, crypto 2/12, network-service 4/8, timing 3/9, fs-metadata 2/10,
  process-env 2/3, git-plumbing 1/3, db-state 1/2, serialization 1/10, container-image 0/0`
  — 16/16 agreement; `Σ n = 230`, `Σ k = 57` pairs over 24 replayed members.
- **Coverage numbers reproduce.** `COVERAGE replayed=24 covered=15 covered_located=13
  uncovered=container-image census_covered=12`: distinct classes among non-unexecuted members = 15,
  among `executed` = 13 (both re-derived by `jq … |unique|length`), census covered 12 matches the
  S255 quote's `classes-covered=12`.
- **Before receipt** (`c1-before.txt`) is internally consistent: `DEFECT` lines 105 =
  88 `MEMBER-UNACCOUNTED` + 13 `CLASS-ROW-UNQUANTIFIED` + 1 `LINK-ABSENT` + 3 `CLASS-K-MISMATCH`;
  after receipt prints `DEFECTS n=0` / `PREDICATE R79-C1 pass`.
- **Controls** (`c1-control-*.txt`): all three `target_reached=False`; name-grep `executed=88
  defects=102`, default-reason `defects=71 codes=EVIDENCE-SHA-MISMATCH,REASON-UNDERSTATED`,
  all-blocked `defects=62 codes=REASON-UNBACKED`. Verified as committed bytes; not executed.

### R79-C2 / calibration — seven closure defects discharged

```
$ git show 660ec0b9:corpus/routed-findings.jsonl | wc -l      → 98
$ wc -l < corpus/routed-findings.jsonl                        → 105
$ jq -r 'select(.id|test("^R78-D"))|[.id,.status,.verified_at,(.close_commit[0:8]),.evidence_path]…'
R78-D1…D7: status=closed, verified_at=2026-11-04, close_commit 42d9d60a or e2d418ca
```

- **Each row's evidence resolves at its close commit** (`git cat-file -e <cc>:<path>` +
  `git show <cc>:<path> | grep -cF <literal>`): D1 `11 TOOL-UNNAMED, 11 COMMAND-ABSENT, 5
  PASS-UNLOCATED, 2 WORKTREE-ABSENT` ×1; D2 `stamped \`cd2e25bb\`, clean` ×2; D3 `ROWS total=105`
  ×1; D4 `15 words` ×2; D5 `R78-D5` ×1 (window also names `R51-C1` and `R75-C1`); D6 `WORKTREE
  clean` ×1; D7 `round-78-verifier-spotcheck` ×1. All seven `close_commit`s are ancestors of the
  tip.
- **The base-failing leg is real for all seven**, checked by reading base bytes: D1's corrected
  split string is absent at base (0 hits) and `R78-D1` is absent; D2 has 0 `cd2e25bb` at base; D3
  has no `## Round 79` section at base; D4's `corpus/lessons/round-79.md` is absent at base; D5's
  `R78-D5` is absent at base; D6's `corpus/evidence/round79/gates-clean.txt` is absent at base and
  `R78-D6` is absent from LOG.md; D7's README row is absent at base (0 hits).
- **D1's re-derived split is the receipt's own**: `grep -oE '^DEFECT [A-Z-]+' corpus/evidence/round78/c2-before.txt | sort | uniq -c` → `11 COMMAND-ABSENT, 5 PASS-UNLOCATED, 11 TOOL-UNNAMED, 2 WORKTREE-ABSENT`, `TOOL-UNPINNED` 0 — the report's `11/11/5/2` is correct.
- **D4's word count is correct** (S254 quote = 15 words), but its anchor statement is imprecise —
  see routed defect V4.
- **After receipt** (`c2-after.txt`): `DEBT-TOTAL ids=7 registered=7 closed=7 checks_passed=7`,
  `INDEX … indexed=yes`, `DEFECTS n=0`, `PREDICATE R79-C2 pass`. `corpus/README.md` carries the
  spot-check row (1 hit). Counts re-derived by `jq` over the JSONL: status histogram
  `71 closed, 31 open, 1 blocked, 2 refused` = 105, matching `routed-open.txt`'s
  `ROWS total=105 open=31 blocked=1 closed=71 refused=2`.
- **Batteries** are evidence-verified only: C2 selftest `cases=9 red=8 failures=0`, mutants
  `real=4 killed=4 survived=0`, control `target_reached=False`.
- **Gate block**: `gates-clean.txt` is stamped `LANE_TIP e560695c…`, `WORKTREE clean`, and 12 live
  gates print `EXIT 0` (13 `EXIT` lines total); `grader.py` prints `CHECKS n=733 mismatches=0`.
  Its last block is the **retired** gate, which exits 1 (`SETUP unresolved revision 'worktree'`) —
  see routed defect V1 for the report's overclaim about it.

## 3. Discernment spot-check (LEARNING.md — `## Gate` of `corpus/lessons/round-79.md`)

| item | decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S256 · Terminal-Bench 2.0 harness README | admit, tier A, scope narrowed to the containerized-run premise | live `curl` of the pinned URL `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/README.md` | **agree** | HTTP 200, 4 574 bytes, sha256 `7dfa9992…d972364` — byte-identical to the committed capture; line 24 carries the quoted sentence, 21 words ≤ 25. The row's scope is the containerized-execution premise, not the four detector codes; the `SourcesScribeR79` narrowing is visible in the row text |
| S257 · population ledger + round-62 census | admit, `own-work`, tier A | repo paths `plans/grader-population-ledger.json`, `corpus/evidence/round62/class-survey.txt` | **agree** | census sha256 `ee30c698…d45613` matches the row and the committed file; ledger has 88 rows; both instruments are re-runnable in-repo. Quote is the census `EXECUTED-COVERAGE` line, at line 21 as the lesson's D4 correction says |
| Reject · "the four named blockers price the unexecuted population" | reject | ledger ledger histogram + base `SCORECARD.md` §Planned (round 79) | **agree** | measured: 7 members over four codes, 57 `unattempted`; `ssh+nginx` is not a code; the base text names no member |
| Reject · "`DEFECTS n=0` means the ledger is knowledge" | reject | `c1-after.txt` + ledger | **agree** | 57 of 64 unexecuted members are the `unattempted` absence, and `covered_located=13` < `covered=15`; a priced absence is not coverage |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc 0
(before receipt rc 0, 245-row registry; after rc 0, 249 rows). The W04 count moved 25 → 26 because
S256 registers a duplicate URL (V5); the report says "unchanged in both" (V2).

## 4. Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | ledger 0 → 88 rows over the 16-class universe; 12 → 88 priced members; all 16 `SKILL.md` cells derived and matching the ledger 16/16; score held 7 at the L0 cap by declaration |
| calibration | **improved** | 7/7 routed ids registered, closed, evidence resolving at their close commits, and base-failing (re-derived above); score held 10, exercised |
| depth | unchanged | two tier-A rows (S256 live-verified, S257 hash-verified) and three `## Mistakes` rows; score held 10 |
| freshness | unchanged | S256 re-fetched live this round with capture + digest; no declared surface drift; score held 10 |
| operability | unchanged | two new gates with selftest/mutant/control receipts (evidence-verified, not executed); score held 10 |
| adjacency | unchanged | `ConnectorR79` sibling matrix; no cross-domain artifact absorbed; score held 9 |
| novelty | unchanged | two instruments, no new domain construct claimed; score held 8 |

No axis harmed: the `SCORECARD.md` diff between base and tip removes only the two round-77 stamp
lines it corrects (`d181e16b` → `cd2e25bb`) and adds the round-79 section; every score line at the
base is unchanged in value.

## 5. Trend verdicts

- **expansion: improved.** Two capability rows enter `SCORECARD.md` with a demonstrated command and
  a committed receipt (`grader-population-member-ledger`, `closure-debt-discharge`); the priced
  population grows 12 → 88 members; the registry gains two tier-A rows (S256 live, S257 own-work)
  with the census before→after recorded. No new `knowledge/` entry — declared, not hidden.
- **quality: improved.** A weaker gate is superseded by a stronger one (`round78-c1` retired,
  population ledger in its place), 12 live gates re-run green in a clean tree, two evidence defect
  classes added after the attacks, and both after receipts re-measured post-amendment. The residual
  limit (a presence gate cannot prove a semantic repair) is stated, not papered over.
- **discernment: improved.** The spot-check agrees on both admits and both rejects; four attack
  seats changed committed bytes (six C1 defect classes, the C2 sensitivity leg, `covered_located`),
  and two disagreements are recorded as honest limits rather than repaired. The report's own
  evidence-prose slips (V1–V3) are calibration blemishes routed below, not unlearned gate
  disagreements.

## 6. Routed defects (the lane must correct next round)

- **V1 · report overclaims a re-verification.** `.ufo/reports/round-79/kengaku.md` says the retired
  `round78-c1` gate's "round-78 verdict stands at `148801a6`, re-verified in `gates-clean.txt`".
  That receipt's retired-gate block prints `SETUP unresolved revision 'worktree'` / `EXIT 1`; no
  passing re-run at `148801a6` is committed. Either drop the clause or run
  `plans/round78_c1_class_member_ledger.py --lane . --rev 148801a6` and commit its pass. (The
  historical verdict itself is supported: `corpus/evidence/round78/c1-after.txt:28` prints
  `PREDICATE R78-C1 pass`.)
- **V2 · census W04 count is wrong in the report.** Sources & frontier says "25 `W04` … unchanged in
  both"; receipts are 25 before and 26 after (`diff` adds S256's duplicate-URL line). rc stays 0.
- **V3 · "13 rows said a bare `executed`" is off by one.** Base has 12 bare `executed` cells plus
  one `recipe-unexecuted` (`container-image`), i.e. 13 *unquantified* rows; the sentence should say
  unquantified, not 13 bare-executed.
- **V4 · R78-D4's S254 anchor is imprecise.** The quoted 15-word sentence spans capture lines 2322
  (`Show untracked files.`) and 2326 (`The mode parameter …`), not "capture line 2322 (one
  sentence)". Re-anchor in the next dated correction.
- **V5 · S256 adds a duplicate-URL W04.** The row is contract-legal (same URL, different scope) but
  the new warning should be stated in the lesson's census reading and either kept with a reason or
  scoped out.
- **V6 · the standalone after receipts carry no revision stamp.** `c1-after.txt` and `c2-after.txt`
  print no `LANE_TIP`; the report's "measured at `5302b92a`" is not re-derivable from the receipt
  itself (the `gates-clean.txt` block is stamped). Stamp the revision in the receipt next round.

No defect above changes the claim measurements; all six are evidence-standard / prose corrections
for the lane's next round. SHONEN boxes 1–4 each carry a checkable pointer, so a non-author review
could check all four; promotion remains operator-owned.

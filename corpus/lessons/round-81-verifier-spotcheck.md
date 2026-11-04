# Round 81 verifier spot-check — kengaku (hyaku closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `kengaku-shokunin`, lane round 81, hyaku run 15 attempt 1. Base
`4e833e9fee8022d24559535178c6fe32b2cd62f1` (round-80 verifier spot-check); lane tip
`ae03c4f6fe1cd805f7808670f053e5bd1b66857a`; fleet report
`.ufo/reports/round-81/kengaku.md` @ `9335e8e632316b778ef20b34de98b974892378ee`. Closed 2026-11-04.

I did not author this round. Nothing below edits lane-authored bytes; every number is a command I
ran myself over committed bytes or committed gate evidence I read. No lane gate was executed. The
two round-81 probes were replayed because they are instruments (they cannot fail a claim), not
verdict scripts; the gate tallies are read from the committed receipts.

## 1. Conformance (step 1)

| Check | Result | Evidence |
|---|---|---|
| Report at the contract path, committed by the lane identity | pass | `git log --format='%an %H' -- .ufo/reports/round-81/kengaku.md` → `kengaku-shokunin 9335e8e6…` (author `kengaku@shokunin.local`, committer same; commit touches only that path, 245 insertions) |
| `SHONEN` heading, one line per box | pass | `kengaku.md:213`; four `[~]` lines, one per `SHONEN.md` box, each with a pointer (`SKILL.md`, `LOG.md:3123`, the two counters + `gates-clean.txt`, `PROVINCE.md` + `ConnectorR81.md`) |
| Every cited lane commit exists and is an ancestor of the branch ref | pass | 31 hashes tested (base `4e833e9f` + the 30 commits in the report's table); `git cat-file -e` and `git merge-base --is-ancestor <h> refs/heads/master` rc 0 for all 31 |
| Lane repo clean and pushed | pass | `jj-lane.sh state` → `branch=master local=ae03c4f6… remote=ae03c4f6… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` prints nothing; `git ls-remote origin refs/heads/master` → `ae03c4f6fe1cd805f7808670f053e5bd1b66857a` |
| Report is a real report, not a completion marker | pass | work performed, 13 evidence-pointed items, 30 commits tied to `LOG.md` §Round 81 (`LOG.md:3123`), checkable hashes, wave tally with the two empty seats named |
| Prompt carries the template contract | pass | `diff` of `.ufo/prompts/kengaku-round-81.md:1-140` against `templates/round-prompt.md` after `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitution: only substituted lines differ; §6 hyaku addendum at `:141`, §7 scratch discipline at `:674`; prompt committed by the lane at `d01af747` (pathspec-limited, 704 insertions) |
| Quoted L2 route map vs `MISSION.md` | pass | `MISSION.md` pins no alias (role buckets only); the prompt's §3 defers to the host route table and §6 carries the 2026-11-03 amendment (only reviewer `@m_zfl`, every other role `@m_flash`) |
| Report filed after its cited work | pass | report committer `2026-11-04 06:07:28 -0300`; lane tip committer `06:06:44 -0300`; wave settle `70707d9d` committer `06:06:10` — the report landed last |

Conformance defects, status-neutral (none changes the ledger status):

- **C-D1 — the C2 after receipt is a dirty-worktree run.** `corpus/evidence/round81/c2-after.txt:3`
  stamps `WORKTREE dirty (1 paths)`, while commit `f70fe5fa`'s message and the report's Landed
  changes row say both after receipts were "re-minted … in a clean clone". The comparable clean
  run exists (`gates-clean.txt` at `39bbe9a4`, `WORKTREE clean`, `PREDICATE R81-C2 pass`), so the
  claim's substance is not carried by the dirty receipt — but the round's own M81-2/Q58 rule
  (a receipt minted over a moving worktree is not a measurement of a tree) was applied to C1 only.
  Routed (V1).
- **C-D2 — the wave has no planner seat** (`templates/round-prompt.md` §3 minimum split) and
  counts the sentinel as its fourth attack seat (4/14 = 29 %); without it the share is 3/14 = 21 %.
  `w1-results.json` roles: executor 6, scribe 2, reviewer 1, critic 1, mutation-tester 1,
  sentinel 1, connector 1, scout 1. Routed (V6).
- **C-D3 — two seats died with empty output** (`LessonScribeR81`, `MutationGateR81`;
  `w1-results.json` `output` length 0). The report names both and says the round has no
  independent mutation-tester pass. Routed (V6).
- **C-D4 — `corpus/knowledge/tb2-file-artifact-replay-classes.md` lacks the provenance trio.**
  `grep -nE '^(source|verified-at|recheck):'` prints nothing; CORPUS.md requires a new knowledge
  entry to open with `source:`, `verified-at:`, `recheck:`. Routed (V3).
- **C-D5 — the lane committed its own dispatch prompt** (`d01af747`) rather than the integrator
  doing it with the round's integration commit. Fleet hyaku-inline convention; no other lane's
  bytes touched; recorded, not routed.
- **C-D6 — stray empty `--lane/` directory** in the lane repo root (mtime 2026-11-04 01:58,
  untracked, empty, not reported by `git status`). A mistyped command's residue; routed (V5).

## 2. Claims (step 2)

Both claims re-derived at the tip with plain measurements (no gate executed). Where a claim rests
on a lane-owned gate, the committed evidence (self-test tally, control, frozen run, revision) was
verified, not re-run — marked *evidence-verified*.

### R81-C1 — coverage: two `unattempted` members become located, reproducible `executed`

Re-measured (mine). Universe, from committed bytes at the base revision:

```sh
python3 - <<'PY'   # ast/grep over `git show 4e833e9f:corpus/evidence/round52/graders/<m>/tests/test_outputs.py`
# eligible = unexecuted + reason=unattempted + classes ⊆ {file-artifact, serialization-schema} → 16
# stdlib-only imports → 11 ; max ^\s*assert\b = 5
# 5: log-summary-date-ranges, vulnerable-secret ; then 3,3,3,2,2,2,2,1,1
PY
```

The 11-member candidate table and the max=5 pair match `c1-before.txt:1-2` exactly. Ledger
(base → tip), `plans/grader-population-ledger.json`:

```sh
git show <rev>:plans/grader-population-ledger.json > /tmp/led-<rev>.json
python3 - <<'PY'   # len(members), status counts, class membership
# base 4e833e9f: members=88 executed=24 unexecuted=64 file-artifact 16/76
# tip  ae03c4f6: members=88 executed=26 unexecuted=62 file-artifact 18/76
# both named rows: base status=unexecuted reason=unattempted → tip status=executed
#                  subject=tb2-header verdict=predicate round=81
PY
```

Receipts (tip): `corpus/evidence/round81/log-summary-date-ranges-probe.txt` and
`vulnerable-secret-probe.txt` are absent at `4e833e9f` and present at `ae03c4f6`; stamp block
lines 2–14; `SUBJECT_SHA` and `TOOL_SHA` recomputed from committed bytes match
(`2fc06a6c…`/`a983909a…` and `f2b65f63…`/`209b28bc…`); `LANE_TIP 4ac8471b` is an ancestor of
`master`; `WORKTREE clean`. Replay at the tip reproduces both observation blocks line-for-line:

```sh
/usr/bin/python3 plans/round81_log_summary_probe.py --lane . --work /tmp/r81verify/ls
# 12 CASE lines, cases=12 observed_pass=4 observed_fail=8 mismatches=0, PREDICATE R81-C1 pass, rc=0
/usr/bin/python3 plans/round81_vulnerable_secret_probe.py --lane . --work /tmp/r81verify/vs
# 12 CASE lines, cases=12 observed_pass=4 observed_fail=8 mismatches=0, PREDICATE R81-C1 pass, rc=0
```

Two consecutive runs of each instrument hash identically (`4ca4c612…` and `5fb7aa35…`), so the
determinism claim holds. `SKILL.md:74` moves `executed 16 of 76` → `executed 18 of 76 (round 81:
log-summary-date-ranges, vulnerable-secret)`.

Evidence-verified (read, not executed): `c1-before.txt` (`DEFECTS n=2`, `TARGET … located=0
reproduced=0 ledger_flipped=0`, `PREDICATE … fail`, `EXIT 1`); `c1-after.txt` (`TARGET members=2
located=2 reproduced=2 ledger_flipped=2 defects=0`, `LEDGER-GATE rc=0 LEDGER rows=88 executed=26
unlocated=0 unexecuted=62`, `EXIT 0`; `LANE_TIP 604be350` ancestor); `gates-clean.txt` at
`39bbe9a4` (`R79-C1 pass`, `R81-C1 pass`, every block `EXIT 0`); `c1-selftest.txt`
(`cases=11 red=10 failures=0`); `c1-mutants.txt` (`real=10 killed=10 survived=0`); the three C1
controls all `target_reached=False`.

**Verdict: improved.** No harm: the previous 24 executed rows and their receipt bytes are
unchanged; the lane diff deletes only the two ledger rows' old state and three index/cell lines.

### R81-C2 — calibration: the round-80 spot-check's U1–U6 discharged as closed rows

Re-measured (mine), `corpus/routed-findings.jsonl` base → tip:

```sh
git show 4e833e9f:corpus/routed-findings.jsonl | grep -c '"id": "R80-U'   # 0
git show ae03c4f6:corpus/routed-findings.jsonl | grep -c '"id": "R80-U'   # 6
# all six status=closed; each evidence_path exists at the tip and contains its evidence_literal
# (6/6: `supersedes S258`, `e985e56a`, `rows=249`, `ModuleNotFoundError: No module named 'Bio'`,
#  `round80-c1-located-replay`, `R80-U6`)
# source lines 157/167/173/178/187/193 of the round-80 spot-check carry U1…U6
# corpus/README.md:929 indexes the spot-check (absent at base)
```

Frozen row counts re-derive exactly: 249 at `dce7c275`, 250 at `507d249b`, 250 at `4e833e9f`,
253 at `ae03c4f6` (`git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`).

Evidence-verified (read, not executed): `c2-before.txt` (six `DEBT-UNREGISTERED`, `INDEX …
indexed=no`, `DEFECTS n=7`, `EXIT 1`); `c2-after.txt` (`TARGET ids=6 closed=6 checks_passed=6
indexed=yes`, `DEFECTS n=0`, `PREDICATE R81-C2 pass`, `EXIT 0`; **`WORKTREE dirty (1 paths)`** —
C-D1); `c2-selftest.txt` (`cases=9 red=8 failures=0`); `c2-mutants.txt` (`real=4 killed=4
survived=0`); `c2-checks-selftest.txt` (`cases=12 red=6 failures=0`); `gates-clean.txt` at
`39bbe9a4` (`R81-C2 pass`, `OK u1`…`OK u6`, `EXIT 0`, clean tree). The sensitivity leg
("checks fail when the repair is reverted to `4e833e9f`") is gate-internal and was verified only
as committed evidence (no `CHECK-NOT-REPAIR-SENSITIVE` line in `c2-after.txt`); I did not execute
the gate, per the closure rule.

**Verdict: improved.** The claim's substance rests on the six rows and the clean `gates-clean`
run, not on the dirty `c2-after` receipt; the receipt defect is routed (V1).

### Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| coverage | **improved** | 24 → 26 executed of 88; `file-artifact` 16 → 18 of 76; the two members' receipts and ledger rows verified |
| calibration | **improved** | six outside findings closed as rows whose evidence literals and sources resolve; clean gate run passes |
| depth | unchanged | held at 10; S259–S261 and the knowledge entry land, no score change |
| operability | unchanged | held at 10; two new gates + a repair-check battery land without a claimed axis move |
| freshness | unchanged | held at 10; census rc 0 before/after, PROVINCE count corrected 249 → 253 |
| adjacency | unchanged | held at 9; connector's sibling scan is the wave's evidence, nothing absorbed |
| novelty | unchanged | held at 8; two new instruments, no new construct claimed |

**No axis harmed.** The SCORECARD diff `4e833e9f..ae03c4f6` is additive (a dated erratum + the
round-81 section); no earlier score line changed or was deleted.

## 3. Discernment spot-check (step 3, LEARNING.md)

`corpus/lessons/round-81.md` `## Gate` records three admits (S259, S260, S261) and one reject
(the `tasks/<member>/task.yaml` spine). Sample: two admits, the reject, and one newly written
`SOURCES.md` row's quote.

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S261 — pinned TB2 task documents | admit | `raw.githubusercontent.com/.../2fd12b88/{log-summary-date-ranges/instruction.md,task.toml, vulnerable-secret/instruction.md}` — HTTP 200 each | **agree** (annotation defect) | all three quotes verbatim at the cited lines (`instruction.md:9`, `vulnerable-secret/instruction.md:1`, `task.toml:6`) and ≤25 words; the recorded counts "14 words" and "17 words" are wrong (actual 12 and 13); 19 is correct |
| S259 — round-80 receipts re-anchored | admit | six `corpus/evidence/round80/<member>-probe.txt` at `ae03c4f6` via `sha256sum` | **agree** | the six prefixes match (`11a53bf3`, `1a3d4e1b`, `afef9380`, `f60bc00b`, `b7e66f4c`, `778565cd`); anchor `lines 2-12` (MEMBER → MINTED_BY_SHA) verified on protein-assembly; S258's bytes are untouched (`corpus/SOURCES.md` diff is 3 insertions) |
| S260 — round-81 instrument set | admit | `corpus/evidence/round81/log-summary-date-ranges-probe.txt:1` + receipt layout | **agree** (annotation defect) | quote `# tb2 log-summary-date-ranges grader probe (round 81)` is verbatim at line 1 and 7 words; the row's cell says "9 words" and "stamp 2-16, observations from 17" — actual stamp 2-14, `OBSERVATIONS_BEGIN` 15, first observation 16 |
| Reject — `tasks/<member>/task.yaml` spine | reject | GitHub tree API at `2fd12b88`, `truncated=false`, 1446 entries | **agree** | 0 entries end `task.yaml`; 89 end `task.toml`; both members are top-level dirs each with `task.toml` + `instruction.md` — a wrong-locator class, not a source |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` → exit 0, final line `kengaku ok …/corpus/SOURCES.md`;
26 `W04` warnings, no `E..` finding. Both committed census receipts are 28 lines with 26 `W04`
each and `EXIT 0`.

## 4. Trend verdicts

- **expansion: improved.** Two population members move `unattempted → executed` (24 → 26 of 88),
  the `file-artifact` class cell moves 16 → 18 of 76, three tier-A rows land (S259–S261,
  `corpus/SOURCES.md` 250 → 253), a knowledge entry enters the index, and `host-pinned-first-receipt`
  enters the capabilities table with a demonstrated command. Evidence: `/tmp/led-*` census above,
  `ledger-census.txt`, `c1-after.txt`, `SCORECARD.md` §Round-81 capabilities.
- **quality: improved.** The replay predicate gains the `HOST_PYTHON`/`HOST_OPENSSL` pin (successor
  rule; round-80 bytes untouched), the mint driver refuses a dirty worktree before and after the
  probes, the repair checks carry a self-test that drops each repair's evidence in turn, and two
  new gates land with 10/10 and 4/4 mutant batteries and a real-tree control. One receipt-accuracy
  blemish (V1) is named and routed, not left unmarked.
- **discernment: improved.** Six outside findings (R80-U1…U6) are closed with checks that fail at
  base rather than restated; the stale `PROVINCE.md` count was found by the round's own gate and
  corrected (249 → 253 with the producing command); the reviewer's F1 is discharged in-round with
  its commit order; the round names what it cannot close (F2/F3/F4/S1/S2 and the critic's (a)–(e)).
  My spot-check agrees on all sampled decisions; the annotation miscounts are routed (V2).

## 5. Routed defects (the lane must fix next round)

- **V1 · the C2 after receipt is a dirty-worktree run.** `c2-after.txt:3` stamps `WORKTREE dirty
  (1 paths)`; `f70fe5fa`'s message and the report say "re-minted … in a clean clone". Fix: re-mint
  `c2-after.txt` from a clean checkout, or make the C2 paragraph cite `gates-clean.txt` @
  `39bbe9a4` as its comparable measurement (the way the round-80 erratum did for `c1-after.txt`),
  and extend the M81-2 rule to the C2 receipt.
- **V2 · annotation miscounts in two files.** `corpus/lessons/round-81.md` records "14 words"
  (actual 12), "17 words" (13) and "9 words" (7); `corpus/SOURCES.md` S260 says "9 words" and
  "stamp 2-16, observations from 17" (actual 7 words; stamp 2-14, observations from 16), and
  S261 repeats 14/17. Every quote is ≤25 words and verbatim, so no admit changes; fix the numbers
  and the anchor range (or state the counting rule).
- **V3 · the new knowledge entry has no provenance trio.** `corpus/knowledge/tb2-file-artifact-replay-classes.md`
  does not open with `source:`, `verified-at:`, `recheck:`; CORPUS.md requires it. Fix: add the
  trio (source S260/S261, `verified-at` the tip, `recheck` the counter command).
- **V4 · a counter docstring contradicts its battery.** `plans/round81_c2_spotcheck_debt.py:384`
  says "Six attributed data mutations"; `c2-mutants.txt` prints `real=4`. Fix the docstring (or
  add the two missing mutants in round 82).
- **V5 · stray empty `--lane/` directory** in the lane repo root (mtime 2026-11-04 01:58,
  untracked, empty). Remove it; it is a mistyped-argument residue, not round work.
- **V6 · wave composition and the dead mutation seat.** The wave has no planner seat and counts
  the sentinel as its fourth attack seat (4/14 = 29 %; 3/14 = 21 % if the campaign list
  reviewer/critic/mutation-tester/labrat is exhaustive). `MutationGateR81` died with empty output,
  so there is no independent mutation-tester pass. Fix: seat a planner and a live mutation-tester
  next round, or record the operator's ruling that the sentinel counts as attack.
- **V7 · `determinism.txt` carries no producing command.** It records two identical hashes per
  instrument but no command or revision, and its hashes are not re-derivable by a plain replay
  (my two runs hash `4ca4c612…` and `5fb7aa35…` and are identical, so the claim holds). Fix:
  paste the command and the revision into the receipt.

## 6. Operator notes (SHONEN)

Every `SHONEN.md` box carries a checkable pointer and all four are `[~]` (author-asserted):
`SKILL.md` (decision tables, error patterns, checklists, cited sources), `LOG.md:3123` (two
graders replayed, six repairs discharged), `plans/round81_c1_new_members.py` +
`plans/round81_c2_spotcheck_debt.py` (self-contained docstrings, run from a clean clone), and
`PROVINCE.md` + `ConnectorR81.md` (no surface absorbed; every sibling overlap adjacent-but-different).
A non-author could check all four from committed bytes; writing `[x]` and promotion are
operator-owned and neither was done here.

Verdict: **admitted** — both claims verified, no axis harmed, seven routed defects.

# Round 80 verifier spot-check — kengaku (hyaku closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `kengaku-shokunin`, lane round 80, hyaku run 15 attempt 1. Base
`dce7c275381c669e6489f1b795b1505d0824c262` (round-79 verifier spot-check); lane tip
`507d249b32eb90863cd0dc78a5672f777ce9d658`; fleet report
`.ufo/reports/round-80/kengaku.md` @ `e560ed5ab646a0eab132f867c4c6b22444a5e69f`. Closed 2026-11-04.

I did not author this round. Nothing below edits lane-authored bytes; every number is a command I
ran myself over committed bytes or committed gate evidence I read (no lane gate was executed).

## 1. Conformance (step 1)

| Check | Result | Evidence |
|---|---|---|
| Report at the contract path, committed by the lane identity | pass | `git log --format='%an %H' -- .ufo/reports/round-80/kengaku.md` → `kengaku-shokunin e560ed5a…` (author and committer identity `kengaku@shokunin.local`) |
| `SHONEN` heading, one line per box | pass | `kengaku.md:169`; four `[~]` lines, one per box of `SHONEN.md`; each carries a pointer |
| Every cited lane commit exists and is an ancestor of the branch ref | pass | 13 round commits (`af51132d`, `6250e94b`, `5b11bc5f`, `bb3d6555`, `446b157f`, `6669fe72`, `14cfe3d0`, `84a89e4e`, `0cb34bf2`, `e985e56a`, `28f8e4c8`, `2763c581`, `507d249b`) plus the historical V1 revision `148801a6`; `git merge-base --is-ancestor <h> master` rc 0 for all 15 tested hashes |
| Lane repo clean and pushed | pass | `jj-lane.sh state` → `branch=master local=507d249b… remote=507d249b… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` prints nothing; `git ls-remote origin refs/heads/master` → `507d249b…` |
| Report is a real report, not a completion marker | pass | work performed, 13 evidence-pointed items, 13 commits tied to `LOG.md` §Round 80 (`kengaku-shokunin/LOG.md:3068`), checkable hashes |
| Prompt carries the template contract verbatim | pass | `diff` of `.ufo/prompts/kengaku-round-80.md` first 140 lines against `templates/round-prompt.md` after `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitution: empty; §6 hyaku addendum (`:141`) and §7 scratch discipline (`:674`) present; prompt committed by the lane at `26823a2` |
| Quoted L2 route map vs `MISSION.md` | pass | `MISSION.md` pins no alias and leaves routing to the operator's host table; the prompt carries the 2026-11-03 amendment ("ONLY reviewer uses `@m_zfl`; every other role `@m_flash`") that supersedes its own run-15 alias line |
| Report filed after its cited work | pass | report change authored 05:00:31 and exported 05:02:09 (jj export — author date is the change's first record); lane tip authored 05:01:11; the final bytes cite `507d249b` and the commit is an ancestor |

Conformance defects, status-neutral (none changes the ledger status):

- **C-D1 — wave has no planner seat.** `templates/round-prompt.md` §3 minimum role split requires
  1× planner; the wave (`w1-spec.json` items, `w1-results.json` roles) has none, and the report's
  "per the orchestrator ruling" has no committed ruling artifact. Named for the operator; the lane
  followed a claimed external ruling.
- **C-D2 — the lane's report commit sweeps the integrator-owned L0 path.** `e560ed5a` carries
  `.ufo/l0-questions.md` (+1 line) beside the report; the protocol gives that path's durability to
  the integrator. Same pattern as kumitate round 78 `88ccf5b2`; the swept line is the lane's own
  `kengaku | round-80` question and nothing else. Recorded, not routed.
- **C-D3 — the lane committed its own dispatch prompt** (`26823a2`) instead of the integrator doing
  it with the round's integration commit. Fleet hyaku-inline convention; harmless (no other lane's
  bytes), recorded for the integrator.

## 2. Claims (step 2)

Both claims were re-derived at the tip with plain measurements (no gate executed). Where a claim
rests on a lane-owned gate, the committed evidence (self-test tally, control, frozen run, revision)
was verified, not re-run — marked *evidence-verified*.

### R80-C1 — coverage: the six `executed-unlocated` members become located, reproducible `executed`

Re-measured (mine):

```sh
jq '.members|length,([.[]|.status]|group_by(.)|map("\(.[0])=\(length)"))'  # base via git show, tip from worktree
# base: members=88 executed=18 executed-unlocated=6 unexecuted=64
# tip : members=88 executed=24 unexecuted=64
jq -n --slurpfile a base.json --slurpfile b tip.json '<diff of .members>'
# changed=6 ; cancel-async-tasks, chess-best-move, distribution-search, largest-eigenval,
#             openssl-selfsigned-cert, protein-assembly : executed-unlocated -> executed
# class-diffs=0 (every classes list identical)
# tip rows: status=executed subject=tb2-header round=80 verdict=predicate x5 / cases x1
for f in corpus/evidence/round80/*-probe.txt; do sha256sum "$(grep -m1 '^SOURCE_RECEIPT ' $f|awk '{print $2}')"; ...; done
# 6/6 SOURCE_SHA MATCH, 6/6 TOOL_SHA MATCH (recomputed against the committed historical receipts
# and the instruments as committed at the tip); every receipt ends `PREDICATE R<n>-C<m> pass`
grep -l HISTORICAL-DIVERGENCE corpus/evidence/round80/*-probe.txt
# openssl-selfsigned-cert (8), protein-assembly (2) — the two `diverged` the report names
```

Evidence-verified (committed receipts, not executed here): `c1-before.txt`
(`DEFECTS n=6`, `located=0 reproduced=0 ledger_flipped=0 defects=6`, `PREDICATE R80-C1 fail`);
`c1-after.txt` (`TARGET members=6 located=6 reproduced=6 ledger_flipped=6 diverged=2 defects=0`,
`LEDGER-GATE rc=0 executed=24 unlocated=0 defects=0`, `PREDICATE R80-C1 pass`, `EXIT 0`);
`c1-selftest.txt` (`SELFTEST cases=19 red=15 failures=0`); `c1-mutants.txt`
(`MUTANTS real=10 killed=10 survived=0`; 6 mutants at the freeze `af51132d` → 10 at the tip);
three controls each `target_reached=False`; `gates-clean.txt` at `e985e56a` (`WORKTREE clean`,
`grader.py` `CHECKS n=733 mismatches=0`, R79-C1 `DEFECTS n=0`, `routed_open` `ROWS total=111
open=31 blocked=1 closed=77 refused=2`, R80-C2 and R80-C1 pass, every block `EXIT 0`).

Verdict: **verified**. The after receipt itself records `WORKTREE dirty` (see U2); the clean
measurement is the `e985e56a` block, and it carries the same four `EXIT 0` verdicts.

### R80-C2 — calibration: the round-79 spot-check's V1–V6 are discharged

Re-measured (mine):

```sh
wc -l corpus/routed-findings.jsonl                  # 111
jq -r .status corpus/routed-findings.jsonl|sort|uniq -c   # 31 open, 1 blocked, 77 closed, 2 refused
jq -r 'select(.id|test("^R79-V"))|[.id,.status,.disposition,has("evidence_path"),has("evidence_literal"),has("verified_at")]|@tsv'
# R79-V1..V6 all closed fixed-verified true true true
jq -r 'select(.id|test("^R79-V"))|.check' | while read -r c; do eval "$c"; done   # 6/6 check=exit0
sed -n '168p;175p;177p;180p;183p;186p' corpus/lessons/round-79-verifier-spotcheck.md
# V1..V6 bullets at exactly the cited lines
grep -c W04 corpus/evidence/round79/census-before.txt corpus/evidence/round79/census-after.txt  # 25 / 26
git show 660ec0b9:SKILL.md | grep -cE '\|[[:space:]]*executed[[:space:]]*\|'   # 13 incl. the header cell => 12 data rows
git show 660ec0b9:SKILL.md | grep -c 'container-image.*recipe-unexecuted'       # 1 => 12 + 1 = 13 unquantified
sed -n '2322p;2326p' corpus/evidence/round78/sources/git-status.html
# "<p>Show untracked files.</p>" / "<p>The mode parameter is used to specify the handling of untracked files."
grep -c 'README.md' on S256/S180 rows                        # same URL, distinct scope (harness model vs grader bytes)
grep -nE '^(LANE_TIP|EXIT)' corpus/evidence/round80/r79-c1-after.txt r79-c2-after.txt   # LANE_TIP 446b157f, EXIT 0 both
```

Evidence-verified: `c2-before.txt` (`DEFECTS n=7`, `indexed=no`), `c2-after.txt`
(`TARGET ids=6 closed=6 checks_passed=6 indexed=yes`, `DEFECTS n=0`, `PREDICATE R80-C2 pass`,
`WORKTREE clean` at `0cb34bf2`), `c2-selftest.txt` (9 cases, 8 red, 0 failures), `c2-mutants.txt`
(4/4 killed), `c2-control-presence.txt` (`CHECK-TRIVIAL`,`CLOSE-NOT-REPAIR`,`SOURCE-LINE`,
`target_reached=False`).

Verdict: **verified**. All six per-id checks re-derive from the tip and all six repair artifacts
exist; V2 (25/26), V3 (12 bare + 1 `recipe-unexecuted`), V4 (lines 2322/2326), V5 (S256 kept), V6
(both stamps) were checked against their own sources, not against the lane's prose.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| coverage | improved | 18 → 24 `executed`, 6 → 0 `executed-unlocated` (my jq); score held at its L0 cap 7 |
| calibration | improved | V1–V6 closed with re-deriving checks (my re-run of all six); score held at ceiling 10 |
| depth | unchanged | S258 + M80-1/M80-2 landed; score held 10 |
| operability | unchanged | two new gate batteries landed (evidence-verified, not executed); score held 10 |
| freshness | unchanged | census rc 0, six replays at the tip, six V1/V6 re-stamps; score held 10 |
| adjacency | unchanged | connector matrix, no absorption; score held 9 |
| novelty | unchanged | two instruments, no new construct; score held 8 |

No axis harmed: `git diff dce7c275 507d249b -- SCORECARD.md` is append-only (no existing score line
changes value), no `knowledge/` entry is superseded, no declared surface is removed, and the one
stale artifact (U1) is routed below rather than an admitted basis.

## 3. Discernment spot-check (step 3, LEARNING.md)

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc 0, 26 `W04`
lines and `kengaku ok`; the registry carries 250 rows
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; 249 at `dce7c275`).

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S258 own-work located-replay instrument set (`round-80.md:12`) | admit | all six `corpus/evidence/round80/*-probe.txt`, `plans/round80_probes.json`, `plans/round80_c1_located_replay.py` | agree (decision), disagree (anchor) | The instrument set is real, in-repo, and re-runnable, so `own-work` tier A fits; the ≤25-word quote is `cancel-async-tasks-probe.txt:1` ("# tb2 cancel-async-tasks grader probe (round 80 re-mint)", 8 words) and matches. Disagree on the anchor's six sha256 prefixes and line range — they pin the pre-A3 bytes (U1) |
| "a located replay is a container run" (`round-80.md:22`) | reject | S256 row + `corpus/evidence/round79/sources/tb2-readme.md:24`; `PROVINCE.md:705,741` (refuses the image, the harness, real submissions, runtime validity) | agree | The capture says TB2 tasks run in containerized environments; the receipts are in-process offline replays of stored grader bytes. The flip (a container receipt naming task and image digest) is testable and would change the verdict |
| "the re-minted numbers are the historical numbers" (`round-80.md:26`) | reject | `corpus/evidence/round57/eigen-probe.txt:23` (`eig-bare-speed-s10 predicted=U observed=P`) vs the tip receipt (`observed=F`); `corpus/evidence/round59/openssl-probe.txt:3-6,16` (two `MISMATCH`, `PREDICATE R59-C1 fail`) vs the tip block (`mismatches=0`, pass) | agree | Both divergences are real and the tip receipts state them (`HISTORICAL-DIVERGENCE 8`, `2`), so the identity claim is false and the reject is right; the flip (block equal to the historical observation lines, `historical=same`) is precise |

## 4. Trend verdicts

- **expansion: improved.** `executed` 18 → 24 members; S258 mined (`own-work`, tier A); registry
  249 → 250 rows, census rc 0; capability `located-replay-mint` entered with a demonstrated command
  (`SCORECARD.md` §Round-80 capabilities). No new `knowledge/` entry — declared in the report, not
  hidden; the expansion observable "a capability admitted to `SCORECARD.md`" carries it.
- **quality: improved.** Two attack-forced hardenings landed with evidence (A2 projection: six
  alternating full-block hashes, one projection hash; A3 mint provenance: `HEAD` + `MINTED_BY_SHA`
  + pre-write cleanliness; both re-derived from the receipts at the tip), mutants 6 → 10 with
  10/10 killed, every control loses, clean-tree block green. One stale pin was found and is routed
  (U1); it does not falsify an admitted entry's substance.
- **discernment: improved.** The spot-check agrees on the one admit and both rejects; the lane
  recorded the reviewer's two P1s as limits, named the undelivered `CriticC1R80` as undelivered
  (its output stops mid-sentence), and raised the amendment question to L0 `kengaku | round-80`
  instead of arguing it away. Learning-path omission: M80-1's `captured-by none` required a
  `QUALITY.md` criterion that did not land (U4).

## 5. Routed defects (the lane must fix next round)

- **U1 · S258's anchor pins the pre-A3 receipt bytes.** `corpus/SOURCES.md` S258 names six sha256
  prefixes `7923b6dc…, b32f4b37…, fd337d12…, 9179d62d…, 08c10b0d…, 82b910af…` and "lines 1-10
  (subject at line 1, stamp at 3-10)". Those are the `bb3d6555` blobs; the committed receipts
  (`446b157f` → tip) hash `11a53bf3…, 1a3d4e1b…, afef9380…, f60bc00b…, b7e66f4c…, 778565cd…`, and
  the A3 stamp block now runs to line 12 (`MINTED_BY`, `MINTED_BY_SHA`). The same stale list is in
  `corpus/lessons/round-80.md:18-20` and is repeated in the report's Sources & frontier. Fix:
  a superseding row (contract v1: `teaches` opens `supersedes S258 —`) or an in-place correction
  limited to the contract's allowed fields plus a lesson correction naming the superseded text;
  state the receipt sha256s with their command
  (`sha256sum corpus/evidence/round80/*-probe.txt`) and the stamp range 3–12.
- **U2 · R80-C1's after receipt is a dirty-worktree run.** `c1-after.txt` prints `WORKTREE dirty`
  and `MINTED_BY plans/round78_restamp.py`; its `LANE_TIP 446b157f` is a HEAD assertion, not a
  measured tree (PROTOCOL §Gate standard: a run over a moving worktree is not comparable to the
  cited commit). The comparable measurement is `gates-clean.txt` at `e985e56a`. Fix: cite the clean
  block as C1's after measurement (or re-mint `c1-after.txt` from a clean checkout) and name
  `e985e56a` in the scorecard row.
- **U3 · the census row counts have no producing command.** The report and lesson state 249 → 250
  registry rows citing `census-before.txt`/`census-after.txt`, but `sources-census.sh validate`
  prints only warning lines and `ok` — no row count (both receipts are 27 lines). Fix: cite the
  frozen census command (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`,
  249 → 250 reproduced) or add a `rows=` line to the census receipt.
- **U4 · M80-1's fix is asserted, not shown able to fail, and its criterion is missing.** The
  lesson says removing the probe table's `prefix` makes the protein leg die with
  `ModuleNotFoundError: No module named 'Bio'` and the gate report `REPRODUCTION-EXIT`, but no
  committed receipt carries that failure (the string appears nowhere in the repo; the C1 selftest
  has 19 cases, none for the interpreter prefix), and the `ModuleNotFoundError` observation itself
  (04:11) is uncommitted. `captured-by none` also requires a `QUALITY.md` criterion citing the
  lesson; `corpus/QUALITY.md` is unchanged this round. Fix: commit the red-before output (prefix
  removed → protein leg non-clean) or a selftest case exercising `REPRODUCTION-EXIT`, and add the
  criterion.
- **U5 · the two new gates have no registry row.** `plans/round80_c1_located_replay.py` and
  `plans/round80_c2_spotcheck_debt.py` are absent from `SKILL.md` (grep prints nothing; round 79's
  counters were registered at `e2d418ca`). PROTOCOL §Gate standard Delivery: "closure grades no
  gate conformant until its registry row exists at the lane's registry home". Fix: add both rows
  (name, `gate`, entry command, verdict map including the declared nonzero codes, self-test command
  and spelling, pinned-value path, write scope, owner).
- **U6 · two smaller evidence-prose slips.** (a) The report's "`REMINT minted=6 failed=0`" is a
  quoted driver stdout with no committed receipt (grep finds it nowhere); the six receipts are the
  durable evidence — cite them or commit the driver log. (b) `corpus/README.md`'s round-80 lesson
  row says "M80-1" while the lesson carries M80-1 and M80-2; an index row is a claim.

## 6. Operator notes (SHONEN)

Every `SHONEN.md` box carries a checkable pointer and all four are `[~]` (author-asserted): the
`SKILL.md` decision table, `LOG.md` §Round 80 (six replays), `plans/round-80-claims.md` (predicate,
universe, controls, kill rule), and `PROVINCE.md` (unchanged, no absorption). A non-author could
check all four from committed bytes; writing `[x]` and promotion are operator-owned and neither was
done here. C-D1 (no planner seat) is the one prompt-contract deviation the operator should rule on.

Verdict: **admitted** — both claims verified, no axis harmed, six routed defects.

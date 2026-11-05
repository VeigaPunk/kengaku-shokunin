author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 86 — verifier spot-check

Reviewed 2026-11-05. Lane before `88651a72ef112ed9f5361e1c8c197babec691f96` (BASE), delivered
`239f8699a3cc336257f4c5659b2c2961582df900` (AFTER), branch `refs/heads/master`. Fleet report
`.ufo/reports/round-86/kengaku.md` is committed in three lane-identity commits (`8aa0a895`,
`135df29b`, `da610129`; all `kengaku-shokunin <kengaku@shokunin.local>`). All lane-relative paths
below resolve in `kengaku-shokunin/`; `L1/` abbreviates `.ufo/waves/round-86/L1/`, `W1/`
abbreviates `.ufo/waves/round-86/w1/`.

## Closure

**status=ok; admitted=true; verdict=admitted.** Both declared claims re-derive from committed
bytes at AFTER and fail at BASE; the two axes they move are `improved` and no owned axis is harmed.
The report is a real lane-attributed report, not a completion marker. The conformance defects in
this review (an in-place rewrite of filed report bytes, stale seat-count sentences, one dead
evidence path, and a Q20-roster revision/wording imprecision) are status-neutral under PROTOCOL
§Round-robin step 1 and are routed below; none touches a declared claim or an axis.

Dispatch/completion digest copied from the mutable `.ufo/watchdog.log`:

```text
2026-11-04T23:51:41-03:00 launch kengaku round=86 pgid=3149765 driver=hyaku-inline attempt=1
2026-11-05T00:33:18-03:00 complete kengaku round=86; hyaku-inline attempt=1
```

Three earlier launches of the same round died without a landed report
(`22:20:16`, `22:30:19`, `22:31:29`, each followed by `lane-dead-no-report`); they are lane history,
not a fourth wave of this round.

## Step-1 conformance

- **Attribution.** `git log --format='%an %H' -- .ufo/reports/round-86/kengaku.md` gives only
  `kengaku-shokunin` commits: `8aa0a895` (00:31:44), `135df29b` (00:31:56), `da610129` (00:32:55),
  all `-0300`. Author and committer are the lane identity.
- **Report contract.** One `## SHONEN` heading (`grep -c '^## SHONEN'` → 1) with four `[~]` lines,
  one per canonical box, each carrying a resolvable pointer (`SKILL.md`, `LOG.md:7`,
  `corpus/lessons/round-8-aggregator-box3-coldrun.md:48`, `PROVINCE.md:151`). Required sections
  occur in order: Work performed (`:9`), Landed changes (`:111`), Before → after measurements
  (`:130`), Sources & frontier (`:167`), Trend verdicts (`:196`), SHONEN (`:212`).
- **Cited lane commits.** All eighteen report-cited hashes exist and satisfy
  `git merge-base --is-ancestor <hash> refs/heads/master`: `61b0e074`, `877f6512`, `316811fa`,
  `48a1ffbd`, `d5e67d9c`, `f357e4c1`, `981d6f19`, `ab9da0d4`, `4d2a0ee8`, `a571044c`, `e23bec07`,
  `276abd46`, `25f68ca0`, `239f8699`, `0481a6d3`, `c939e6b5`, `bfda0472`, `b8f05bef`. Ancestry was
  tested against the branch ref, never `@{u}` (HEAD is detached).
- **Lane state.** `scripts/hyaku/jj-lane.sh state` before this review's write:
  `branch=master local=239f8699 remote=239f8699 ahead=0 behind=0 head=detached tracked=0
  untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` prints
  `239f8699`. No uncommitted round work, no unpushed commit.
- **Prompt fidelity.** `.ufo/prompts/kengaku-round-86.md` is tracked and committed (`39fb4191`).
  Its sections 1–5 are the rendered `templates/round-prompt.md`: 138 lines each, differing only by
  the `{{FLEET_ROOT}}`/`{{ROUND}}`/`{{LANE}}`/`{{AXES}}` substitutions. The round-level items
  (mission/axes binding, 1–3 claims, L2 floor, commit-then-push, push scope, L0 channel) and the
  five child-lane items (report path/filename, commit-before-report, SHONEN heading, hash citation,
  lane write scope) are present; `## 6. Campaign addendum` follows.
- **Wave.** One v1 wave: `w1-dispatch.json` counts `spawn=12 resume=0 total=12`; roles are executor
  3, scribe 2, reviewer 2, scout/critic/mutation-tester/sentinel/connector 1 each — the report's
  seat list exactly. Attack share 4/12 = 33 % ≥ the 25 % floor; 12 sits inside the operative
  policy-`v1` band 8–16 (`scripts/hyaku/ufo-wave-policy.json`, `waveMinLanes` 8 / `waveMaxLanes`
  16; spec `maxLanes` 12). No `w1-results.json` exists; the report discloses the missing envelope
  instead of inventing one.
- **Conformance defects (status-neutral, routed).**
  1. The report's filed bytes were rewritten in place: the Round-shape paragraph
     (`8aa0a895`: "Dead or incomplete seats: **two** … Lane tip at close: `25f68ca0…`") was replaced
     at `135df29b` with the one-seat/`239f8699` text, and the appended `## Correction` section does
     not name the sentences it supersedes. PROTOCOL requires an erratum appended after the filed
     bytes that names the superseded text, never a rewrite of filed bytes.
  2. The correction sweep left two stale sentences: report line 7 still says "zero dead seats" and
     line 242 still says "naming the two incomplete seats above", while line 230 says one incomplete
     seat (`ReviewerC286`). §Evidence standard: corrections sweep every mention.
  3. `135df29b` (00:31:56) cited lane hash `239f8699` thirty-six seconds before that commit existed
     (00:32:32). The final report commit `da610129` (00:32:55) lands after the lane tip, so the filed
     final revision is consistent; the premature intermediate citation is recorded, not charged to
     the final bytes.
  4. Dead evidence path: report line 59 and `LOG.md:3317` cite
     `.ufo/waves/round-86/L1/outside-gates.txt` for the Q20 roster. That path exists in no ref
     (`git log --all --` → empty; no tree in `rev-list --all` carries it). The roster itself is
     committed at `W1/ExecGatesR86/gate-receipt.txt` and verifies (see below).
  5. The Q20 roster is described as "from a shared clone at the tip"; the committed receipt records
     a `git archive` **extraction** at tips `f357e4c1` (pass A) and `ab9da0d4` (pass B) — both
     before instrument v2 `e23bec07` and before the final tip `239f8699` — with `--lane/--repo`
     overrides where the counters need git history (first attempts exit 2 `unresolved-revision
     master`, then remedied). Substance holds; the revision and method wording do not.

## Claim rechecks

Plain committed-byte measurements were the evidence of record; the two frozen counters were
additionally re-run read-only at BASE and AFTER with `--work` under `/tmp` (disclosed in
*Review limitations*). No lane file was written by this review.

### R86-C1 / coverage — re-derived, verifies

Independent ledger measurement, `git show REV:plans/grader-population-ledger.json` parsed with
plain `json` (88 members; counters over each row's `classes` list and `status`):

| fact | BASE `88651a72` | AFTER `239f8699` |
|---|---|---|
| executed members | 29 | 30 |
| `raman-fitting` row | `unexecuted` | `executed`, round 86, receipt `corpus/evidence/round86/raman-fitting-probe.txt`, subject `tb2-header`, verdict `cases` |
| `file-artifact` | 21 of 76 | 22 of 76 |
| `serialization-schema` | 2 of 10 | 3 of 10 |
| `numeric-band` | 2 of 10 | 3 of 10 |

Only the `raman-fitting` row changes; the three class cells match the report's before→after
exactly. Frozen-counter transcripts at both revisions, re-run by this review:

```text
$ python3 plans/round86_c1_replay.py --lane . --rev 88651a72… --work /tmp/cl86/base
DEFECT L1-receipt missing corpus/evidence/round86/raman-fitting-probe.txt
DEFECT L2-stamp
DEFECT L3-tip
DEFECT L4-table missing plans/round86-cases.json@rev 88651a72ef11
DEFECT L5-vectors
DEFECT L6-reproduce no tool plans/round86_raman_probe.py@rev 88651a72ef11
DEFECT L7-ledger status=unexecuted,round=None,receipt=None,subject=None,verdict=None
TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=7
PREDICATE R86-C1 fail   (rc=1)

$ python3 plans/round86_c1_replay.py --lane . --rev 239f8699… --work /tmp/cl86/tip
TARGET members=1 cases=8 legs=24 mismatches=0 located=1 executed=1 defects=0
PREDICATE R86-C1 pass   (rc=0)
```

Receipt at AFTER (`git show 239f8699:corpus/evidence/round86/raman-fitting-probe.txt`): eight
`CASE` lines, `cases=8 legs=24 mismatches=0`, `PREDICATE R86-PROBE pass`, `LANE_TIP b8f05bef…`
(an ancestor of AFTER), `WORKTREE clean`, `EXIT 0`. Its `TOOL_SHA 09731b3e…` and
`CASE_TABLE_SHA f8aa21f3…` equal `sha256sum` of `plans/round86_raman_probe.py` and
`plans/round86-cases.json` at AFTER; `SUBJECT_SHA 171fae77…` equals the round-52 capture
(`corpus/evidence/round52/graders/raman-fitting/tests/test_outputs.py`, 2029 B) and the live URL.
Two of the eight `CASE` lines are the receipt's own controls, not schema cases — the disclosed
R86-V3 wording defect; the numeral the claim is measured on (8 cases, 24 legs, 0 mismatches)
holds.

### R86-C2 / calibration — re-derived, verifies

Plain measurement over committed bytes: `SHONEN.md` box 4 is `PROVINCE.md:151` at AFTER and
`PROVINCE.md:129` at BASE; `grep -n '^### Adjacent' PROVINCE.md` gives `151` at both revisions
(line 129 is a table rule `|---|---|---|` at BASE). `plans/state_check.py --summary` run over a
`git archive` extraction of BASE and over the AFTER worktree:

```text
BASE  (--root /tmp/cl86/basetree): assertions=329 match=317 mismatch=1 superseded=6 offline_unverifiable=5
      MISMATCH: P3c.box.4.pointer.1  pointer=PROVINCE.md:129 target_line=151 token_hits=1
      VERDICT: FAIL
AFTER (worktree):                  assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5
      VERDICT: PASS — all comparable frozen assertions match
```

Frozen-counter transcripts:

```text
$ python3 plans/round86_c2_repin.py --lane . --rev 88651a72… --work /tmp/cl86/c2base
DEFECT P2-shonen pointer=PROVINCE.md:129 derived=PROVINCE.md:151
DEFECT P3-pin line=129 derived=151
DEFECT P4-state mismatches=1
TARGET derived_line=151 shonen_pointer=PROVINCE.md:129 pin_line=129 state_mismatches=1 selftest=pass defects=3
PREDICATE R86-C2 fail   (rc=1)

$ python3 plans/round86_c2_repin.py --lane . --rev 239f8699… --work /tmp/cl86/c2tip
TARGET derived_line=151 shonen_pointer=PROVINCE.md:151 pin_line=151 state_mismatches=0 selftest=pass defects=0
PREDICATE R86-C2 pass   (rc=0)
```

The claimed single repaired assertion is the one my BASE run prints (`P3c.box.4.pointer.1`), and
the pointer now names the derived token line. The claim "re-derived, not hand-edited" is verifiable
only as the observable (pointer == derived line, recomputed by `P1-derive` on every run) plus the
lesson's provenance note; the historical value 129 is retained as `STALE_LINE`, not erased.

### Separation and gate evidence — verified, not executed

- `bash L1/separation.sh /tmp/cl86/sep` at AFTER: reverting C1's receipt and ledger row leaves
  `R86-C2` at `defects=0`; reverting C2's two-line repair leaves `R86-C1` at `defects=0`. Both
  `PREDICATE … pass`, rc 0. The claims are causally separable as declared.
- `L1/freeze-battery-v2.txt`: C1 `SELFTEST cases=10 red=10 failures=0`,
  `MUTANTS real=6 necessary=5 redundant=1 declared_redundant=1`, four controls each
  `target_reached=False`; C2 `SELFTEST cases=4 red=4 failures=0`,
  `MUTANTS real=3 necessary=1 redundant=2 declared_redundant=2` with `caught_by` named per
  redundant mutant, four controls each `target_reached=False`.
- `L1/base-runs-v2.txt` carries the BASE transcripts quoted above; `L1/c1-c2-tip.txt` carries the
  tip runs at `276abd46` plus the R79 gate (`DEFECTS n=0`, `replayed=30`); `W1/ExecGatesR86/
  gate-receipt.txt` records `CHECKS n=733 mismatches=0`, `sources_adopt SELFTEST cases=17
  failed=0`, R75 parity PASS, R79 `DEFECTS n=0`, R82 `DEFECTS n=0`, `defect_ledger mismatches=0`,
  `state_check --selftest` exit 0 and C1 `SELFTEST cases=10 red=10 failures=0` with
  `FINDINGS: 0 count differences`. Batteries and the roster were not re-executed by this review.

## Axis verdicts

| axis | verdict | basis |
|---|---|---|
| **coverage** | **improved** | executed population 29 → 30 and three class cells move, re-derived above; predicate passes at AFTER, fails at BASE |
| **calibration** | **improved** | self-assessment mismatch 1 → 0 with the named assertion re-derived from `PROVINCE.md` bytes; `VERDICT: PASS` |
| novelty | unchanged | 8 held; no new construct, no prior-art verdict this round (SCORECARD §Round 86 "Other axis scores") |
| depth | unchanged | 10 held; no score-row movement in `git diff 9972c87c 239f8699 -- SCORECARD.md` |
| operability | unchanged | 10 held; three new instruments with batteries extend the rounds 83–85 replay method, no capability row claimed |
| freshness | unchanged | 10 held; the stale canonical surface row (`253` → `266`) is repaired, no new drift mechanism |
| adjacency | unchanged | 9 held; connector scan report-only, nothing absorbed |

No owned axis is harmed: the `SCORECARD.md` diff between `9972c87c` and AFTER appends one round-86
section and changes no score row; `corpus/SOURCES.md` gains S274 with zero deletions
(`git diff --stat`: `1 insertion(+)`).

## Discernment spot-check (LEARNING §"Discernment is checked from outside")

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S274 `raman-fitting/tests/test_outputs.py`, tier A, member replay only | admit | live `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/raman-fitting/tests/test_outputs.py` (HTTP 200, 2029 B, `sha256 171fae77…`) and the committed round-52 capture (`cmp` silent) | **agree** | the pinned bytes are the acceptance rule the claim replays; the row's quote is `:36`, `assert x0_correct and gamma_correct and A_correct and offset_correct,` — 8 whitespace-split words ≤ 25, present verbatim at line 36 (trailing ` (` correctly excluded); scope is stated and narrower than a solved-task claim |
| new `corpus/knowledge/` entry for `raman-fitting` | not created (reject) | `plans/gate_timing_check.py:241-243` (`is_second_wave` accepts only `falsify` or `wave2`), `.ufo/l0-questions.md:297` (`kengaku \| round-84`), policy `maxLanes`/`waveMinLanes` (a residual falsify wave under 8 seats is refused) | **agree** | a one-wave round cannot supply the Q13 second-seat citation the admit table requires; writing an unconfirmable entry is what round 84 refused, and the correct move is to stay held and route the shape question |
| `merge/kengaku/` package | none (reject) | `.ufo/l0-questions.md:213` (`kengaku \| round-54`, mass id drift) | **agree** | the id-collision ruling is still open and no package bytes were read; adopting anything would launder a known collision |
| `considerthese/2026-10-26.md` §2 standing TB2 counter | none new (reject) | `considerthese/2026-10-26.md` §Self-improvement suggestions 2 and `corpus/QUALITY.md:1320` (Q61) | **agree** | the proposal is already Q61's per-entry form; the round adds no counter, so naming it as the open half is accurate, not an evasion |

`corpus/SOURCES.md` new row: one insertion, no deletions; registry 265 → 266 rows
(`grep -cE '^\| S[0-9]{3}'` at both revisions); `sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` exits 0 with 30 `W04` lines and
`kengaku ok …/corpus/SOURCES.md` — matching the report's after-state.

## Trend verdicts

- **expansion — `unchanged`.** No new `corpus/knowledge/` entry on uncovered ground, no new kind of
  source, no capability row: S274 is the same pinned-grader class rounds 83–85 used, and the
  frontier advanced by one member of the same method. The coverage axis moved on counts, but
  `LEARNING.md`'s expansion observable is admitted entries/frontier entry, neither of which occurs.
- **quality — `improved`.** A weaker held claim was superseded by a stronger one in place of a
  rewrite (`Q62`'s dead evidence pointer corrected by `Q63`, `corpus/QUALITY.md:1332-1335`), three
  grounded criteria Q63–Q65 cite this round's own mined mistakes, the stale canonical surface row
  was re-counted (`PROVINCE.md:1041`, `rows=253` → `266`), and no admitted entry fails its
  re-check (`state_check` PASS; census exit 0).
- **discernment — `improved`.** The outside spot-check agrees on the round's one admit and all
  three rejects above, and the attacks changed the record instead of being argued away: R86-V3
  (case-set mislabel) and R86-V4 (`members=1` literal) are in the lesson and *Planned*, and the
  battery mistakes are captured as criteria. The stale-sweep and dead-pointer defects below are
  report-craft defects routed to the lane, not gate-decision disagreements.

## Routed defects the lane must fix or answer next round

1. **Dead evidence pointer (evidence standard).** `.ufo/waves/round-86/L1/outside-gates.txt` is cited
   at report line 59 and `LOG.md:3317` and exists in no ref. Append a correction naming
   `W1/ExecGatesR86/gate-receipt.txt`, and correct the "shared clone" wording: the receipt records a
   `git archive` extraction at `f357e4c1`/`ab9da0d4`, before instrument v2 `e23bec07`, with
   `--lane/--repo` overrides. If a tip-level roster is wanted, run it at `239f8699` and commit it
   under `L1/`.
2. **Correction sweep (report record).** Append an erratum naming the superseded sentences and the
   rewritten paragraph: report line 7 ("zero dead seats"), line 242 ("naming the two incomplete
   seats above"), and the `8aa0a895` Round-shape text it replaced. Do not rewrite filed bytes
   again.
3. **Stale case-set wording in live docs.** `LOG.md:3300` and `corpus/README.md:941` still say
   "eight frozen schema-drift cases"; the corrected fact is "eight case shapes, six schema-drift and
   two controls" (R86-V3). LOG takes an appended correction; the README index row is editable.
4. **R86-V4 `members=1` literal.** Keep the frozen predicate as-is for this round's record, but the
   successor C1 instrument must count executed rows (or delete the clause); do not re-freeze the
   literal.
5. **CriticR86 counter precision defects.** A malformed ledger exits 1 with a traceback instead of a
   named `DEFECT`; `--freeze` can make L4 compare a table with itself; fixture mode (`--lane`
   without `--rev`) measures the dirty worktree. Each needs a named leg or a refusal in the
   successor instrument.
6. **SentinelR86 residuals.** F2 (ancestor-tip acceptance), F3 (one stdout channel shared with the
   graded capture) and F5 (sandbox ro-binds host `/etc`/`/usr`, no rlimits) remain recorded
   limitations of the harness; carry their remediation into the successor instrument's honest-limit
   block.

## Review limitations

- The two registered claim counters were re-run read-only with `--work` under `/tmp` and reproduced
  the committed `TARGET` lines verbatim. PROTOCOL §Gate standard assigns the integrator
  evidence-verification, not execution; the verdicts above rest on the plain committed-byte
  measurements and the committed transcripts, not on this execution, and no lane file was touched.
- Battery tallies, mutant splits, control results, the Q20 roster and the frozen-run transcripts were
  evidence-verified from committed bytes; no self-test, mutant battery, grader or sandbox was
  executed. A first C1 BASE attempt during this review returned `DEFECT SETUP unresolved-revision`
  (rc 2) while a concurrent git object repack was in flight; the retry reproduced the committed
  line. Not charged to the lane.

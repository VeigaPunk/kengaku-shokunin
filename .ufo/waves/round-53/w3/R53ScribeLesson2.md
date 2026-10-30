# R53ScribeLesson2 — round-53 lesson draft (scribe, wave 3)

Seat: `R53ScribeLesson2` (scribe, leaf — no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Axis: **calibration**. Assignment: draft `corpus/lessons/round-53.md` in the shape of
`corpus/lessons/round-52.md` (sections `## Gate`, `## Mistakes`, `## Limits`, plus `## Assimilation`: none), write it
into my own seat directory, and leave the landing to the L1.

**Nothing outside my seat directory and my scratch was written.** No lane file was edited, staged or committed; no
`git commit/add/push/stash/checkout/reset/pull` and no mutating `jj` command ran in the lane or the fleet repo; no
fixture repository was created. The lane's own `corpus/lessons/round-53.md` was **not** created — the L1 owns the
landing (and `corpus/lessons/round-53.md` is still absent at `9ead4476`).

## Lane tip I ran at

| what | hash |
|---|---|
| tip named in the assignment | `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe` |
| lane HEAD when my clone was made | `9ead4476bf55b1ea6490d0204b668195db4a4d1d` (`round-53: confirmations integrated (20 tasks, five wave-2 readers), wave-3 spec+dispatch evidence`) |

`git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/R53ScribeLesson2/lane`
then `git -C … rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r53/R53ScribeLesson2/lane` (the required
path). `git diff --stat b1f79a54 9ead4476 -- plans/ SKILL.md` → only `corpus/evidence/round53/confirmations.json`
changed, so every counter measurement below holds at both hashes. The L1 reconciles.

## What I did

1. Read the frozen claims in full (A1–A3), `.ufo/waves/round-53/facts.md` (raw, including the truncated line 52),
   `corpus/lessons/round-52.md` and `corpus/lessons/round-52-verifier-spotcheck.md` (the latter for the Gate/spot-check
   shape), the five wave-1 attack reports named in the assignment (`C1CritCounterReach`, `C1MutCounter`,
   `C1SentinelScreen`, `C2CritLedgerReach`, `C2MutCounter`), `claims/c2-run1.txt`, `claims/c1-selftest.txt`,
   `claims/c2-selftest.txt`, `claims/c2-a3-redbefore.txt`, `claims/c1-after-oracle.txt`, `claims/c1-candidates.txt`.
2. Read every wave-3 report that existed while I wrote (`C1RelabelRev1-4`, `C1TouchExecA`, `C1ScoutLitSrc`,
   `C1ScribeSources2A`, `C1PriceScoutC`, `C1PriceScoutD`, `C1MutClassifier`, `C2MeasureExecA`, `C2MeasureExecB`,
   `C2RevLedgerPlan`, `R53ConnSiblings2`, `R53RevengerCarried`, `R53ScoutSurfaces`, `R53ScribeScoreLog2`) and the two
   wave-1 reviewer reports that define the ledger's remaining defects (`C1RevCounter`, `C2RevCounter`).
3. Made my own measurements at the lane's current HEAD (all in the scratch clone, receipts copied into my seat dir).
4. Wrote the lesson draft.

## My own measurements (exact commands, all at `9ead4476`)

### C1 counter, full run in the clean clone

```
S=/fast/scratch/hyaku/kengaku-r53/R53ScribeLesson2
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane
git -C $S/lane rev-parse --show-toplevel        # -> $S/lane
cd $S/lane && TMPDIR=$S/tmp python3 plans/round53_c1_triage.py --lane .
```

Output (`w3/R53ScribeLesson2/c1-at-head.txt`, exit 1):

```
PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok r52_audit_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184
FREEZE clean=yes classifier_and_freeze_one_commit=yes classifier_sha=ok label_files_pinned=ok shards_pinned=ok labels_after_freeze_and_untouched=yes authors=4
ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52 unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)
ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes
CONFIRM candidates_never_read=28 new_confirmed=20 rejected=0 target>=3
PRIOR-ART rows=0 tasks_covered=0/20 known=0 new=0 urls=0 rejected=0 target: urls>=3 new>=1
PREDICATE R53-C1 fail
```

### C2 counter, static legs and the one disagreeing row

```
cd $S/lane && TMPDIR=$S/tmp python3 plans/round53_c2_tipstate.py --lane . --dry
  -> ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok
     ARGV entry=74 selftest=4 help=0 help_limit=7.8 ; DRY static legs only: no predicate   (exit 0)

cd $S/lane && TMPDIR=$S/tmp python3 plans/round53_c2_tipstate.py --lane . --source . --work $S/work2 --only round53-c1 --jobs 1
  -> SOURCE rev=9ead4476bf55b1ea6490d0204b668195db4a4d1d clean=yes lane_rev_equal=yes
     MISMATCH round53-c1 declared exit=0 observed exit=1 sec=2.4
     RUN executed=1 timeout=0 mismatched=1 evidence_missing=0
     PREDICATE R53-C2 fail   (exit 1)
```
Receipt: `w3/R53ScribeLesson2/c2-only-round53-c1.txt`. This reproduces, on the single disagreeing row, the
full-run result the two independent measurement seats recorded (`C2MeasureExecA`, `C2MeasureExecB`: `executed=78
timeout=0 mismatched=1 evidence_missing=0`, `declared_green=66 declared_red=12 observed_green=65 observed_red=13`,
`PREDICATE R53-C2 fail`, exit 1, at `b1f79a54`). **The `round53-c1` ledger cell is still false at the tip**: the
ledger declares `exit 0 / green`, the counter observes `exit 1`.

### The `rule-unit-leak` repair, re-measured at the tip

```
python3 -  (importlib load plans/round52_c1_grader_audit.py, call classify_tests on
            corpus/evidence/round52/graders/<task>/tests/test_outputs.py)
  pytorch-model-recovery    -> test_model_file_exists      class P3
  torch-tensor-parallelism  -> test_parallel_linear_exists  class P2
python3 -  (importlib load plans/round53_c1_classify.py, call classify_source on the same bytes)
  pytorch-model-recovery    -> test_model_file_exists      P1
  torch-tensor-parallelism  -> test_parallel_linear_exists  P1
```
The round-52 lexical splitter still leaks at `9ead4476`; the frozen AST classifier does not. The same P3/P2 values
are committed in the round-52 receipt `.ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json`. The classifier's
own digest is `sha256sum plans/round53_c1_classify.py` → `935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6`.

### The wave-3 blind re-label cross-check (my own; the oracle leg's third opinion)

I merged the eight wave-1 label files and compared the four wave-3 re-label sets against both the merged oracle and
the frozen classifier (`w3/R53ScribeLesson2/relabel-crosscheck.txt`, `relabel-composition.txt`):

```
oracle label files: 8  ids: 305  labels per id: Counter({2: 305})
v2 ids: 305
wave-3 relabel ids (union): 80   pairwise shard overlap: 0 / 0 / 0 / 0 / 0 / 0
agree with oracle: 80 of 80   disagree: 0
agree with v2 classifier: 80 of 80   disagree: 0
oracle label pairs over the 80 relabel ids: Counter({('Y','Y'): 52, ('N','N'): 28})
oracle-Y ids: 52 ; relabel covers all 52 oracle-Y: True ; oracle-N ids: 253 ; relabel covers 28 of them (11.1 %)
```

So the four wave-3 reviewers reproduce the frozen classifier on every id they were given — but the shards were
L1-chosen and cover **every** oracle-`Y` id and only 28 of the 253 `N` ids, so this corroborates the positives and
leaves 225 `N` ids unconstrained. The lesson says exactly that.

### "never-read" is not "never-examined" — measured

```
python3 -  (compare the 28 candidate ids in claims/c1-candidates.txt and the 20 confirmed tasks in
            corpus/evidence/round53/confirmations.json against the round-52 receipt
            .ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json)
round-52 live_tests.json: tasks 89  per-test records 305
candidates 28   in receipt 28   per-test records over them 112
confirmed  20   in receipt 20   per-test records over them 78
```
Receipt: `w3/R53ScribeLesson2/never-read-overlap.txt`. Every candidate and every confirmed task already carries a
per-test class record in the round-52 critic's receipt; the counter's blocklist covers only base-tip lane texts
(`plans/round53_c1_triage.py:280-300`), so it cannot see them.

### Census

```
cd /home/vgpnk/Projects/shokunin && scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
  -> 15 x W04 ; last line "kengaku ok /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md" ; EXIT=0
grep -c '^| S[0-9]' corpus/SOURCES.md   -> 186
```
Same as the round-start figures (15 `W04`, 186 rows, exit 0). No row from this round is landed: the last registry id
is still `S193`.

## What the lesson contains

`w3/R53ScribeLesson2/lesson.md` (28 KB), in the round-52 shape:

- **Header** — L1, frozen claims and the three amendments, the three wave shapes, and the two verdicts *as the counter
  prints them at the tip*, explicitly deferring the verdict to the L1's landing receipt.
- **`## Gate`** — the SOURCES candidates in three groups with placeholder ids and located quotes: group A
  (`C1ScribeSources2A`, 18 rows `T01`–`T18`, 10 queued / 8 rejected, each re-opened live on 2026-10-30 with HTTP
  status, bytes, sha256 and rendered/raw line spans); group B (`C1ScoutLitSrc`, 15 rows `L01`–`L15`, all HTTP 200 with
  recorded sha256 and `SOURCE-URL:` headers, cited by the knowledge entry rather than offered as registry rows); the
  wave-1 fallback drafts (`C1RevSources2`, 46 rows) recorded as **history, not rows**, with the reviewer's defect
  list and the warning that their `S901…`/`S941…` placeholder ids collide across the four groups. Admits/rejects are
  `[pending]`: the L1 has landed nothing and assigns ids from `S194`. Prior-art pricing is marked `[pending]` with the
  measured reason (the `PRIOR-ART` leg holds no rows because no `prior-art.json` and no `fetched/` directory exist).
  Spot-check set `[pending: non-author spot-check]`, with the proposed set named.
- **`## Mistakes`** — thirteen rows in the round-52 columns (class · evidence pointer · captured-by · fix), each fix citing
  a receipt that shows the repaired instrument failing on the defect. The four required classes are there
  (`counter-reachable-without-the-work` second occurrence, repaired by A1 and independently re-attacked in wave 3;
  `rule-unit-leak`, repaired by the AST classifier; `false-registry-cell`, partly repaired — one cell still false;
  `operator-interruption-partial-wave`, repaired by the re-dispatch), plus nine classes the wave-3 reports name with
  resolvable pointers (`ledger-reason-overstates-cause`, `vacuous-selftest`, `host-surface-retired-under-the-round`,
  `number-drift` recurrence, `mechanical-verification-blocked`, `never-read-is-not-never-examined`,
  `oracle-leg-tolerates-a-class-change`, `frozen-suite-is-not-a-safety-net`,
  `counter-selftest-blind-to-the-dangerous-direction`).
- **`## Limits`** — thirteen bounded statements, each with its own number or command.
- **`## Assimilation`** — none.

Two honest statements I put in the draft and will repeat here:

1. **C1 is not admitted as of this tip.** The classifier, oracle, control and confirmation legs hold
  (`disagree=0`, `per_label_agree=1.000`, `new_confirmed=20`), but `PRIOR-ART rows=0 tasks_covered=0/20` fails the
   frozen score rule, so the counter prints `PREDICATE R53-C1 fail` (exit 1). The prior-art pricing seats
   (`C1PriceScoutC` 4 rows, `C1PriceScoutD` 4 rows) have produced seat-local `prior-art-part.json` files that are
   **not integrated** into `corpus/evidence/round53/prior-art.json` and whose archives are not under the lane's
   `fetched/` prefix, so the leg is still empty.
2. **C2 is not admitted either, and the one failure is the ledger's, not the counter's.** `mismatched=1`, and the
   mismatch is `round53-c1 declared exit=0 observed exit=1` — the ledger cell is false because the C1 counter exits 1
   at the tip. The counter is doing its job; the cell needs the L1 (re-declare it red with its evidence, or land the
   prior-art rows that make C1 exit 0).

## Findings worth the L1's attention

- **`round53-c1` is a live false registry cell.** Two independent wave-3 measurement seats and my own single-row
  re-run agree on it. It is the only mismatch, so it is also the only thing between the C2 counter and a pass.
- **The wave-3 blind re-label is not an independent sample.** It covers all 52 oracle-`Y` ids and 28 of 253 `N` ids.
  The 80/80 agreement is real but bounds the positives only; the 225 untested `N` ids are unconstrained.
- **"never-read" is narrow.** All 28 candidates and all 20 confirmed tasks already carry per-test class records in
  the round-52 critic's receipt (112 and 78 records). A1 names this "not changed"; the lesson records it as a limit
  and as an open mistake class, with the wave-3 re-attack seat `C1CritNeverRead` still pending.
- **The touch-run leg produced nothing.** All 13 invocations are `blocked` (no pytest fetchable without network, and
  the bwrap sandbox could not create `/app`), so no receipt shows an empty artefact passing a confirmed test. The
  wave-2 readers substituted a direct function call without pytest; that is a protocol, not the mechanical check the
  seat spec asked for.
- **Two wave-3 attack seats are named in the assignment but not in the wave.** `C2MutLedger2` is not a wave-3 seat:
  `w3-spec.json` (32 items) has `C2CritPredicate2` and `C1MutCounter2`; wave 2's list had `C2MutCounter2`. The lesson
  leaves it `[pending]` rather than inventing a seat. `C1CritOracle2` (the ORACLE leg's 305/305 agreement) is
  dispatched but has written nothing yet.
- **The ORACLE leg is budgeted, not verified.** The wave-3 mutation seat `C1MutClassifier` measured against the
  counter's own `leg_oracle()`: the budget is `0.03 × 305 = 9.2` disagreements, so a classifier that moves up to 9
  ids' classes keeps the leg at `pass` (`M20` moves 1 id, `M26` moves 2, leg `pass` for both). The tip's
  `disagree=0` is a stronger reading than the leg requires — but the leg would not have said so, and the frozen
  predicate has no class-level leg. The lesson records this as a mistake class and a limit.
- **The classifier's frozen suites are not a safety net.** 22 of 42 single-edit mutants survive both the 83-case
  selftest and the 90-case adversarial set; 20 have a one-to-five-line witness, 12 of which move the *class*. The
  wave-3 seat also re-attacked wave 1's joint classifier+digest edit and confirmed A1 closed it (all three variants
  now fail FREEZE). Both directions are in the lesson.
- **`C2RevLedgerPlan`'s medium finding is a live cell defect**: `plans/round53-tipstate.json:723` says the
  `round46-c3` map "lacks the frozen tags both-print and toolchain", but both tags occur at
  `corpus/knowledge/tb2-polyglot-c-py-grader.md:86,89` (marked *not exercised*). The exit and the evidence are
  right; the prose cause is not.

## Files produced (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeLesson2/lesson.md` — the lesson draft.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeLesson2/c1-at-head.txt` — C1 counter output at `9ead4476`.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeLesson2/c2-only-round53-c1.txt` — C2 counter on the one disagreeing row.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeLesson2/relabel-crosscheck.txt` — the 80-id re-label cross-check.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeLesson2/relabel-composition.txt` — the re-label set's composition against the oracle classes.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeLesson2/never-read-overlap.txt` — the candidate/confirmed vs round-52-receipt overlap.
- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeLesson2.md`.

Scratch (`/fast/scratch/hyaku/kengaku-r53/R53ScribeLesson2/`) was removed before this report was written.

## Tooling

Nothing installed, upgraded or removed. No pacman transaction (pacman is paused host-wide by the 2026-10-20
orchestrator ruling). Only `git` (clone + read-only queries), `python3` (3.14, stdlib), `grep`, `awk`, `sed`, `df` and
the lane's own `scripts/sources-census.sh` were used. Disk guard: `/fast/scratch/hyaku` 44 % used, 450.4 G free before
the pass; no ENOSPC.

tool: `_bash` returned an empty body (exit 1) for a command whose last statement was a non-zero exit, even though the
earlier statements in the same line had produced output that was redirected to a file; the file had to be re-read with
`read`. Same behaviour reported by the wave-1 seat `C2MutCounter`.

## Out of scope / not done

- `corpus/lessons/round-53.md` was **not** created — the L1 lands it. This seat's deliverable is the draft in its own
  directory, as the assignment specifies.
- No SOURCES row was written and no id assigned; the Gate carries placeholder ids only.
- The wave-3 attack reports named in the assignment that have not yet been written (`C1CritOracle2`,
  `C1CritNeverRead`, `C2CritPredicate2`, `C1MutCounter2`) are `[pending]` in the lesson, with the seat named for
  each; their mistake classes are not claimed. `C1MutClassifier` landed while I was writing and is incorporated.
- I did not re-run the full 78-row C2 counter myself (the two measurement seats did, and I re-ran the one disagreeing
  row plus the static legs); I did not re-run the C1 selftests beyond reading the committed receipts; I did not
  re-fetch any source URL (the source scribes fetched live on 2026-10-30 and I quote their located rows).
- Blindness: this seat read the label files, the classifier and the counter — a lesson scribe must, to state the
  oracle's numbers and the ledger's cells. It is not a labelling seat and wrote no label.

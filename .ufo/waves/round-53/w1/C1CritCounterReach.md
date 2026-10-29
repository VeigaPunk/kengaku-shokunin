# C1CritCounterReach — critic on the frozen C1 counter (round 53, wave 1)

Target: `plans/round53_c1_triage.py` (frozen; not edited, not committed, not run on the lane tree).
Scope: find inputs that make `PREDICATE R53-C1 pass` without the claimed work. Round-52 routes were not re-tested.
Only scratch clones were used: `/fast/scratch/hyaku/kengaku-r53/C1CritCounterReach/` (removed at exit; the scripts and receipts are kept below).

## Bottom line

1. **The frozen counter passes its own predicate with no classifier and no labelling.** A fixture whose "classifier" marks every test `P1` (classifies nothing), whose labels are that classifier's own output, whose author list is self-declared, and whose confirmations and prior-art are forged, gets `PREDICATE R53-C1 pass` (`results/composite-fixture.txt`). Every one of the five legs prints a passing line.
2. **The planned real-tree control "labels copied from the classifier's own output (order leg)" will not fail under the frozen counter.** The order leg only checks commit order of two files; a copy committed after the classifier satisfies it. In the composite the ORACLE leg prints `disagree=0 ... control_ok=yes`. Under the claims' kill rule this is a frozen-rule defect, not a fixture artefact; the decision (amend by dated entry, or admit/reject as frozen) belongs to the L1. I have not changed anything.
3. **Freeze check is not bound to history.** The classifier and the freeze JSON are read from the working tree; `first_add` checks only the freeze JSON's add-time. Two routes pass FREEZE (R1, R2). The frozen selftest's `classifier-edited-after-freeze` case misses R2 because it does not re-hash the freeze file.
4. **Contested tests are excluded from the disagreement count.** 45 contested tests (the allowed 15 %) plus 0 disagreements on the 260 decided tests pass ORACLE with an all-`P1` classifier (R4).
5. **Confirmation and prior-art legs accept forged or unrelated evidence:** a report outside `.ufo/waves/round-53/`, a reader who is a labeller, an archive reached through `..` that is a grader, a sweep consisting of one file listed twice, and "known" rows whose archive is a bare list of task ids (R5–R9).
6. **"Never-read" is not never-examined.** All 63 counter-candidates have per-test records in the round-52 receipt `.ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json` (208 records for those 63 tasks), which the blocklist does not cover (R10).

Smallest fixes are listed per route below. None was implemented; the counter stays as frozen.

## What I ran (exact commands; all paths absolute or scratch-relative)

```
S=/fast/scratch/hyaku/kengaku-r53/C1CritCounterReach
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane     # rev-parse --show-toplevel asserted = clone dir (lane base 1373b6c)
cd $S/lane && TMPDIR=$S/tmp python3 plans/round53_c1_triage.py --lane .           # baseline at 1373b6c
TMPDIR=$S/tmp python3 plans/round53_c1_triage.py --selftest                       # cases=22 failures=0 (results: selftest-base.txt)
TMPDIR=$S/tmp python3 plans/round53_c1_triage.py --lane . --candidates            # CANDIDATES never_read_tasks=63 (cand.txt)
python3 attacks.py ; python3 attacks2.py ; python3 attacks3.py ; python3 attacks4.py   # fixture drivers, all in .ufo/waves/round-53/w1/C1CritCounterReach/
```

Every fixture commit was made with `git -C <clone> -c user.email=c1crit@fixture.invalid -c user.name=C1CritCounterReach ...` in a clone. The only reads of the real lane were `git clone --shared`, `git show/log/ls-tree` (read-only) and reading pinned inputs. Real pins held: `population_sha=ok pin_tree_sha=ok tests_index_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184`.

**Blindness.** I did not read the real classifier (it does not exist at 1373b6c; I wrote my own stand-in `plans/round53_c1_classify.py` in the scratch clone and labelled it as such), any `C1Label*` directory or output, any `.ufo/waves/round-53/w1/C1Exec*` path, or `.ufo/waves/round-53/labels/`. I did read round-52 wave files (including round-52 `C1Exec*` files) only to test name matches for the never-read definition; those are not round-53 label or classifier seats. No label or classifier output of this round exists in the lane yet. No violation to report.

**Installs.** None. No tool was installed or upgraded; no pacman, no `~/.local/bin` change.

**Scratch.** Free space on `/fast` was 459 GB before the run (no ENOSPC).

## Fixtures used (all forged; stated so the numbers are not read as evidence about the real classifier)

- `ALLP1` classifier: `classify_source` returns `P1` for every `test_*` function. Freeze JSON: `classifier_sha256` of that file, `author_seats: ["C1ExecClassifier"]`.
- Labels: all 305 tests `labelers: [C1LabelA, C1LabelB]`, `labels: [Y, Y]` (copied from the stand-in's output).
- Confirmations: three never-read tasks from `--candidates`, reader `ReaderZ`, report at `.ufo/waves/round-53/w2/ReaderZ/report.md` (path-compliant, content is a forgery), quotes copied from each test's own span.
- Prior-art: three `phenomenon-new` rows, three invented `https://fixture-{a,b,c}.invalid/...` URLs (fixture-only, not real sources) over one archive, two unrelated sweep files.

## Measured numbers

| run | FREEZE | ORACLE (decided / contested / disagree / limit) | ORACLE-CONTROL | CONFIRM | PRIOR-ART | predicate |
|---|---|---|---|---|---|---|
| baseline 1373b6c | absent | not evaluable | — | 0 | 0 | fail |
| composite (all-P1 + copied labels + forged evidence) | ok, freeze-before-labels | 305 / 0 / 0 / 9.2 | r52 disagree 272, yes | 3 | 3 rows, 3 URLs, new=3 | **pass** |
| T1 classifier committed after labels | ok, freeze-before-labels | 305/0/0 | yes | — | — | (FREEZE+ORACLE pass) |
| T2 classifier v2 + re-hashed freeze after labels | ok, freeze-before-labels | 305/0/0 | yes | — | — | (FREEZE+ORACLE pass) |
| T3 labels committed all-Y, uncommitted edit to 45 contested | ok | 260 / 45 / 0 / 7.8 (working tree) | yes | — | — | (HEAD has 0 contested) |
| T4 45 contested + all-P1 | ok | 260 / 45 / 0 / 7.8 | yes | — | — | ORACLE holds |
| T7 all labels U | ok | 0 / 305 / 0 | NO (vacuous) | — | — | fail (negative, works) |

Names in parentheses are the legs that hold in that run; the other legs were not made to pass there.

## Routes

Each row: construction → counter output → whether the leg holds → smallest fix. "exercised" = run on a scratch clone; "by reading" = code path only.

**R1 — classifier committed after the labels (FREEZE, exercised, holds).** Commit A: freeze JSON with the sha of a classifier that exists only in the working tree. Commit B: labels. Commit C: `plans/round53_c1_classify.py`. Output: `FREEZE classifier_sha=ok order=freeze-before-labels authors=1`. `first_add` is only ever applied to the freeze JSON and the labels, never to the classifier, so the claim's own parenthetical ("labels read only after the classifier was committed") is not checked. Fix: `first_add(classify)` must exist and be a strict ancestor of `c_lab`; the classifier blob at `c_fz` must equal HEAD's blob. Result: `results/T1.txt`, commit `b37e986 classifier added last`.

**R2 — classifier edited and freeze re-hashed after the labels (FREEZE + ORACLE, exercised, holds).** Commit A: freeze + classifier v1. Commit B: labels copied from v1. Commit C: classifier v2 (one comment line) and freeze JSON re-hashed. Output: `FREEZE classifier_sha=ok order=freeze-before-labels`; ORACLE unchanged. The freeze file was not re-added, so `first_add` still points to A. Fix: read the freeze JSON and the classifier from git at `c_fz` (`git show c_fz:...`), require no commit to either path after `c_fz` (`git log c_fz..HEAD -- <both>` empty), and require a clean tree. Also add this case to `selftest()`; the current `classifier-edited-after-freeze` case does not re-hash the JSON, so it cannot catch R2. Result: `results/T2.txt` (commit `447c653`).

**R3 — the counter reads the working tree, not the committed labels (ORACLE, exercised, holds).** HEAD labels: 0 contested. Uncommitted `oracle-labels.json` with 45 split labels: the counter prints `contested=45` and the ORACLE leg passes against the uncommitted file. No `git status` check exists anywhere in the counter. Fix: refuse a dirty tree for `plans/`, `corpus/evidence/round53/`, `.ufo/`, or read each input with `git show HEAD:<path>`. Result: `results/T3-working-tree.txt`; `git status --porcelain` showed `M corpus/evidence/round53/oracle-labels.json`.

**R4 — labels copied from the classifier's own output; contested budget (ORACLE, exercised, holds).** Two sub-routes, both pass:
- (a) Composite: all-`P1` stand-in, labels = its output: `disagree=0`, `control_ok=yes` (r52 disagreement 272). The control passes because the copied labels are all `Y`; the r52 mapping disagrees on any `P0` output. The control therefore measures "labels differ from r52", not classifier quality.
- (b) Contested budget (T4): 45 tests labelled `[Y,N]`, the rest `[Y,Y]`, all-`P1` classifier. `contested=45 <= 45.75`, `disagree=0 <= 7.8`. Contested tests are excluded from `dis`, so a classifier wrong on all 45 is scored as perfect.
Fix (partial; the counter cannot prove independence): (i) a contested test counts as a disagreement unless the classifier's class equals both labels; (ii) decided labels must contain both `Y` and `N` in a floor of tests (an all-`Y` copy fails); (iii) independence is a protocol property: each labeller's shard is a committed file whose git author is in a seat registry, the classifier's committed author set is derived from `git log`, and the copy-vs-independent question is answered by the labelers' transcripts, not by the counter. The frozen control "labels copied from the classifier's own output (order leg)" cannot fail under the frozen counter (see bottom line 2).

**R5 — report path outside `.ufo/waves/round-53/` (CONFIRM, exercised, holds).** `report: corpus/evidence/round53/ReaderZ-notes.md` (content identical, sha256 matching, path contains the reader name). Output: `new_confirmed=3 rejected=0`. The counter never checks the prefix the claim requires. Also by reading: `lane / str(report)` with an absolute `report` yields the absolute path (pathlib), and `..` components are not normalised, so the report may live anywhere on disk. Fix: `rep = (lane / r["report"]).resolve()`; require `rep.is_relative_to(lane / ".ufo/waves/round-53")`; reject absolute paths and `..`. Result: `results/T5b-report-outside-prefix.txt`.

**R6 — the reader is a labeller (CONFIRM, exercised, holds).** `reader: C1LabelA` (also a labeller in the label file) with a report whose path contains `C1LabelA`: `new_confirmed=3`. The only exclusion is `r["reader"] in info["authors"]`, where `authors` is the freeze JSON's `author_seats` (classifier authors). Blindness of labellers versus readers is not enforced. Fix: reader must not be in the labeller set derived from `oracle-labels.json` nor in `author_seats`; compare case-folded. Result: `results/T5c-reader-is-labeler.txt`.

**R7 — archive reached through `..` (PRIOR-ART, exercised, holds).** `fetched: corpus/evidence/round53/fetched/../../round52/graders/<task>/tests/test_outputs.py` with the grader's own sentence (9 words, a grader comment) as the quote, and `fetched_sha256` of that file. `fetched()` checks only the string prefix `corpus/evidence/round53/fetched/` and then resolves the path, so the "archive" is a grader. Output: `PRIOR-ART ... new=3 ... PREDICATE R53-C1 pass`. Fix: `(lane / r[key]).resolve()` must be under `lane / RUN_DIR / "fetched"`; reject symlinks (`is_symlink`). Result: `results/T6a-archive-traversal.txt`.

**R8 — sweep of one file listed twice (PRIOR-ART, exercised, holds).** `sweep: [fx-s1, fx-s1]` (same unrelated page twice). Passes `len(sw) >= 2`. A "negative claim carries its sweep" is not checked for coverage at all. Fix: sweep entries distinct and resolved, each with a recorded query and result count; or drop "sweep" as the proof of a negative. Result: `results/T6b-sweep-duplicate.txt`.

**R9 — "known" rows accept a bare list of task ids; URL not bound to archive (PRIOR-ART, exercised).** Archive: one line `fixture link list of task names: <three task ids>`; three `phenomenon-known` rows quoting that line: `known=3` accepted. The check is `task not in text` (substring) with no test-name requirement, so a page naming the task id once is "known prior art". The predicate then fails only on `new>=1` (T6c). Mixed run: two `known` rows from the link list plus one `new` row with a 2-file sweep gives `PREDICATE R53-C1 pass` (T6d). URLs are shape-checked only: the composite used three invented URLs over one archive and `URL_MIN=3` passed. Fix: a known row's quote must contain a test name as a whole token (or the task id as a whole token and a sentence about the phenomenon); the archive must contain its row's URL (archive header bound to the URL). Results: `results/T6c-known-link-list.txt`, `results/T6d-mixed-known-new.txt`.

**R10 — a `phenomenon-new` row may cite an archive that names the task (PRIOR-ART, exercised, holds).** In the composite, row 1's archive is a page naming `break-filter-js-from-html`; the new-row branch checks only the quote and the sweep, never the main archive. Fix: a new row's fetched archive must not name the task or its test names (same test as the sweep).

**R11 — "never-read" is not never-examined (CONFIRM candidate set, exercised).** The blocklist covers 59 base-tip texts (corpus/knowledge, SCORECARD, LOG, SKILL, README). Measured on base 536925b:
- 18 of 88 tasks are named in the blocklist (case-sensitive and case-insensitive counts are equal: 18/18; spaced-form-only mentions: 0 — the case/spacing route is closed in practice).
- The `candidates` set is 63 tasks (the counter's own `--candidates`, with the all-P1 stand-in).
- All 63 appear in `.ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json`, a round-52 receipt with per-test class records (`P0`–`P3` style) for every task: 208 per-test records for the 63 candidates. The blocklist does not cover `.ufo/waves/`.
- 4 candidates (`fix-code-vulnerability`, `hf-model-inference`, `pytorch-model-recovery`, `torch-tensor-parallelism`) are named in the round-52 triage entry, which the counter excludes from the blocklist by name.
- The composite's `break-filter-js-from-html` is one of the 63.
Fix: define never-read against every prior receipt (`.ufo/waves/round-52/**`, `corpus/evidence/round52/**` excluding the captures), or rename the claim to "not confirmed in round 52 and not named in base-tip knowledge" and say so in the report. Neither is done.
Negative: `seen_before` boundary handling is correct for the one prefix pair in the population (`path-tracing` / `path-tracing-reverse`).

**R12 — the confirmation quote and span arithmetic (negative).** Checked the pinned `tests-index.json`: `src[lineno-1]` begins with `def <name>` for 305 of 305 tests; the boundary after `end_lineno` is blank/outdented for 302 of 305, and the other three are whitespace-only lines. Span arithmetic is correct; the 20-character quote check is not a route on its own.

**R13 — the control module is unpinned (by reading, plus a warning seen during the run).** `r52_classes` executes `plans/round52_c1_grader_audit.py` from the working tree with no digest. A tampered r52 module changes `dis52` and therefore the control. Not exercised as a tamper. `tool:` the counter loads `plans/round52_c1_grader_audit.py`, which emits `SyntaxWarning: "\." is an invalid escape sequence` at its line 101; it is a warning only and did not change any verdict observed here.

**R14 — classifier reads the labels file (by reading, not exercised).** `load_mod` executes the classifier in the counter's process with full filesystem access; the freeze hashes only the one `.py` file. A classifier that reads `corpus/evidence/round53/oracle-labels.json` at call time agrees with any labels. R4 already shows the same end state without this route. Fix: run the classifier in a child process with `-I`, a copy of the tree that holds only the captures, and no labels file; pin every module it imports.

**R15 — `author_seats` is self-declared (by reading, not exercised).** The counter never reads git authorship; an empty list fails only via `bool(authors)`; a list that omits the real classifier author passes (the disjointness test only excludes names that are listed). Fix: derive authors from `git log --format=%an -- plans/round53_c1_classify.py` and the labels' first-add author.

## Composite result (headline evidence)

`results/composite-fixture.txt`:
```
PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184
FREEZE classifier_sha=ok order=freeze-before-labels authors=1
ORACLE tests=305 labelled_ok=305 bad_label_rows=0 decided=305 contested=0 oracle_Y=305 v2_P1=305 unclassified=0 disagree=0 limit=9.2
ORACLE-CONTROL r52_classifier_disagree=272 all_P0_disagree=305 control_ok=yes
CONFIRM candidates_never_read=63 new_confirmed=3 rejected=0 target>=3
PRIOR-ART rows=3 tasks_covered=3/3 known=0 new=3 urls=3 rejected=0 target: urls>=3 new>=1
PREDICATE R53-C1 pass
```
Nothing in this run requires a classifier that classifies, a labeller who labelled, or a reader who read.

## Routes checked and found closed (negatives)

- Pins (PINS leg): the population, pin-tree and tests-index sha256 values and the 183 blob matches are not re-pinnable by a forged capture (`blob_bad=1` in the selftest; real tree unchanged).
- `first_add` for the freeze JSON and labels: the same-commit case returns `UNPROVEN` (verified by running T2's first variant: `order=UNPROVEN`).
- All-`U` labels: `decided=0 contested=305 control_ok=NO(leg vacuous)`, `PREDICATE fail` (T7).
- Quote-in-span (CONFIRM): span arithmetic correct for all 305 tests (R12).
- `never_read_blocklist`: no case or spacing variant of any task id appears in base texts beyond the 18 exact matches (R11).

## Files

- Scripts (fixture drivers, all in scratch clones): `.ufo/waves/round-53/w1/C1CritCounterReach/attacks.py`, `attacks2.py`, `attacks3.py`, `attacks4.py`.
- Receipts: `.ufo/waves/round-53/w1/C1CritCounterReach/results/` (T1, T2, T3-working-tree, T4, T5a/b/c, T6a/b/c/d, T7, `composite-fixture.txt`, attack logs); `.ufo/waves/round-53/w1/C1CritCounterReach/selftest-base.txt` (`cases=22 failures=0`); `.ufo/waves/round-53/w1/C1CritCounterReach/cand.txt` (63 candidates under the stand-in; `count-dataset-tokens` appears in it, so a grep for credential-shaped strings matches a task name, not a credential).
- Absolute paths of the scratch material (removed at exit): `/fast/scratch/hyaku/kengaku-r53/C1CritCounterReach/`.

## Not done

- The real classifier, labels, confirmations and prior-art of this wave do not exist in the lane yet; no route was tested against them. All numbers above are for fixtures I built.
- No fix was implemented; the counter was not edited (per the assignment).
- R13–R15 are by reading only.

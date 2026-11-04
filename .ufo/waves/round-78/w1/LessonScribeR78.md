# LessonScribeR78 — lesson draft and evidence

Axes: coverage; calibration. Draft destination for the integrator: `corpus/lessons/round-78.md`. Only this report was written in the lane; the lesson destination was not modified.

## Full lesson text

# Round 78 — kengaku (2026-11-04 UTC)

Base `3ae0ab54` (`3ae0ab540c35fe40da048198f3e5d4042766b2b7`); freeze `2f9eeafb` (`2f9eeafb35f3d4c0df2259ec8dc73c48009c96c8`).

R78-C1 / coverage (L0-capped at 7): account exactly once for the 12 distinct members across 13 member-class pairs of the three partially executed classes, binding executions to tracked passing receipts and non-executions to detector-backed typed reasons, with SKILL ledger pointers.

R78-C2 / calibration (ceiling 10, exercised): make verdict-bearing round77/round78 receipts self-locating through an ancestral LANE_TIP, WORKTREE, TOOL plus revision-recomputable TOOL_SHA (or honest supplied-tool disclosure), and COMMAND; repair the routed round-77 evidence defects.

## Gate

These are draft registry rows in the sources seat's specified eleven-cell order. S254's capture was not fetched by this seat; its capture-derived fields remain `<unmeasured>`, not an assertion of completed admission. S255's committed object was read directly. These rows are proposals, not a claim that registry changes landed.

| id | source title + URL/path | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S254 | Git git-status reference https://git-scm.com/docs/git-status | docs | A | semantics of untracked-file reporting in git status | --untracked-files option; capture date 2026-11-04 proposed; HTTP, bytes, sha256, exact capture line and located quote <unmeasured> | distinguish tracked-file cleanliness from inclusion of untracked files | queued | 2026-11-04 | on-release | corpus/lessons/round-78.md, plans/round-78-claims.md |
| S255 | Lane grader-class census corpus/evidence/round62/class-survey.txt | own-work | A | class membership counts of the committed grader population only | object 2f9eeafb:corpus/evidence/round62/class-survey.txt; CLASS lines 11,14,16 and EXECUTED-COVERAGE line 21; sha256 ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613 | derive member identity and overlap rather than trusting prose execution totals | mined | 2026-11-04 | on-release | corpus/lessons/round-78.md, plans/grader-selected-members.json |

- **S254 docs gate — queued capture-dependent admission.** Proposed source URL above; access date, HTTP status, byte count, capture digest, quote and capture line are `<unmeasured>` by this seat. The sources-seat contract calls for the untracked-file option sentence and a quote of at most 25 words. Do not replace those unknowns with an assumed fetch result. This is not executed source-admission evidence.
- **S255 admitted for the narrow own-work fact.** `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 2f9eeafb:corpus/evidence/round62/class-survey.txt` returned rc 0; SHA-256 over the returned bytes is `ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613`. Its selected CLASS rows name network-service count=8, process-environment count=3 and db-state count=2. The sources-seat contract explicitly lists own-work as admissible; this admits the census as evidence of the stored population, not as independent proof that every grader ran or every task is correct.
- **Reject:** “a class count in a prose table is evidence of class membership.” A count does not identify the tasks, resolve overlapping classes, or bind an execution to receipt bytes. Flip: derive members from the committed census, assign each member one ledger row carrying its classes, and check execution receipts or typed reason detectors. At the measured base, the counter finds 12 unaccounted members despite the existing class execution totals.

## Census and instrument readings

The scribe ran the frozen counter programs, not imported modules, in a shared scratch clone checked out at freeze `2f9eeafb`. Both commands below ran with cwd `/fast/scratch/hyaku/kengaku-r78/LessonScribeR78/before-lonppd0c/clone`. The clone top-level was asserted equal to that path before checkout. The clone was deleted after measurement. Results are embedded here; the deleted scratch path is not a durable evidence artifact.

Exact setup commands executed through subprocess argv:

```sh
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r78/LessonScribeR78/before-lonppd0c/clone
git -C /fast/scratch/hyaku/kengaku-r78/LessonScribeR78/before-lonppd0c/clone rev-parse --show-toplevel
git -C /fast/scratch/hyaku/kengaku-r78/LessonScribeR78/before-lonppd0c/clone checkout --detach 2f9eeafb
```

All returned rc 0. The counters were independent concurrent subprocesses over the same read-only clone:

```sh
python3 plans/round78_c1_class_member_ledger.py --lane . --rev 3ae0ab54
```

Observed rc 1:

```text
LANE_TIP 3ae0ab540c35fe40da048198f3e5d4042766b2b7
WORKTREE clean
UNIVERSE classes=3 members=12 pairs=13
CLASS network-service k=4 n=8 census=8 ledger_k=0
CLASS process-environment k=2 n=3 census=3 ledger_k=0
CLASS db-state k=1 n=2 census=2 ledger_k=0
LEDGER rows=0 executed=0 unexecuted=0
COVERAGE recomputed_covered=12 census_covered=12 promoted=- recomputed_uncovered=network-service,process-environment,db-state,container-image
DEFECTS n=21
TARGET classes=3 members=12 executed=0 unexecuted=0 unaccounted=12 unbacked=0
PREDICATE R78-C1 fail
```

The output names 12 MEMBER-UNACCOUNTED defects, three CLASS-ROW-UNLINKED, three COUNT-DRIFT, and three COVERAGE-REGRESSION defects. **Conflict, preserved rather than repaired:** assignment says “Before: no ledger, 12 `MEMBER-UNACCOUNTED`, 19 defects, rc 1.” The frozen program actually prints `DEFECTS n=21` with the command above. No claim, target, control or kill rule was edited.

```sh
python3 plans/round78_c2_stamp_location.py --lane . --rev 3ae0ab54
```

Observed rc 1:

```text
LANE_TIP 3ae0ab540c35fe40da048198f3e5d4042766b2b7
WORKTREE clean
UNIVERSE dirs=2 receipts=16
DEFECTS n=27
TARGET receipts=16 located=3 unlocated=13
PREDICATE R78-C2 fail
```

The three rerun receipts (`rerun-r51-c1.txt`, `rerun-r75-c1.txt`, `rerun-routed-open.txt`) are printed with `legs=ok`; the other receipt rows expose absent commands, unnamed tools, absent worktree stamps, or unlocated passes. This is stamp-location evidence, not independent replay of their predicates.

Source-registry census for round 78: `<unmeasured>` by this seat. After-state counter results: `<unmeasured>` by this seat. No final green or round-wide admission is asserted here.

## Mistakes

All evidence pointers below refer to committed bytes at freeze unless another revision is explicit. Proposed fixes are dispositions, not claims of completed repairs.

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| D1 / stamp does not locate predicate truth | corpus/evidence/round77/rerun-r51-c1.txt stamps 9ebb8ed1 and WORKTREE dirty; round-77-verifier-spotcheck.md §6 D1 records the pass depending on post-8da90eb7 fixes | none in the original receipt gate; closure D1 found it; the frozen C2 before run still prints legs=ok for this receipt | re-mint at a revision where the predicate reproduces; do not equate a matching tool digest with verified run inputs |
| D2 / battery tool digest from a different revision | corpus/evidence/round77/c1-selftest.txt stamps 51ffc14f and TOOL_SHA a4777acf4d5874191f37d59eab8563f5f45b18a0991d805fe6b7dc3283eee571; reading 51ffc14f:plans/round77_c1_declared_surfaces.py yields SHA-256 5a507c086ea8bf7e4a2f604fd37a1173065e89911812d38b8a75422e886b1bd3 | none until closure D2 / R78-C2; frozen C2 catches TOOL-UNNAMED first because this receipt supplies no TOOL path | name the tool and full digest at the revision actually carrying its bytes, then re-mint the battery there |
| D5 / WORKTREE clean untracked-tool blind spot | corpus/evidence/round77/c1-before.txt prints WORKTREE clean at 07c97fcd; git show 07c97fcd:plans/round77_c1_declared_surfaces.py returned rc 128, path absent at that revision; closure D5 records supplied untracked tool | nothing checking untracked supply in the original receipt; frozen C2 prints COMMAND-ABSENT for this file, not SUPPLIED-BUT-CLEAN, because no tool is named | disclose supplied tool and mark WORKTREE dirty, with the exact tool identity and command; a clean tracked diff alone is insufficient |
| receipt identity / TOOL_SHA without TOOL | entire corpus/evidence/round77/c1-selftest.txt was read: TOOL_SHA exists but no TOOL or COMMAND line | R78-C2 before output: TOOL-UNNAMED and COMMAND-ABSENT | record the repository-relative TOOL path alongside its full digest and executable command; a digest alone does not name what to recompute |
| measurement / narrated before total differs from executable result | assignment's C1 before total says 19 defects; frozen counter at 2f9eeafb with --rev 3ae0ab54 prints DEFECTS n=21 | this seat's required before replay, including three COVERAGE-REGRESSION lines | retain observed output and route the discrepancy for adjudication; do not alter the frozen instrument or silently replace the measured total |

## Limits

- C1 does not replay the five unexecuted members. Directly reading `2f9eeafb:plans/grader-selected-members.json` names filter-js-from-html, git-multibranch, headless-terminal, install-windows-3.11 and query-optimize as unexecuted. install-windows-3.11 belongs to two classes, so member-class pairs must not be confused with distinct members.
- **Frozen-text conflict, verbatim:** the claims' out-of-scope bullet says “Simulating the 6 unexecuted members”. The frozen ledger names five distinct unexecuted members, matching this seat's requested limit. This draft reports the difference; it does not amend the frozen claim.
- C1's reason detector establishes a condition in stored grader bytes, not impossibility of executing the task by another setup. Receipt predicate text is evidence checked by the ledger, not fresh replay of that grader by this seat.
- C2 checks stamps, not predicate truth. The observed legs=ok rerun receipts demonstrate why tool-location and predicate re-derivation are separate obligations. C2 also cannot establish the historical truth of a self-reported WORKTREE state merely by parsing it.
- The receipt universe is limited to qualifying round77/round78 files and excludes sources captures; other rounds are not repaired by this claim. SCORECARD prose corrections and completeness of an at-tip rerun block require their own evidence, not an inference from C2's location count.
- Source capture statistics and final after-state measurements remain `<unmeasured>` here. No source fetch, unexecuted-member replay, receipt re-mint, product edit, commit, push, deployment or final claim judgment was performed by this seat.

---

## Audit handoff

- **Behavior/gates exercised:** required C1 and C2 before counter invocations above, both rc 1, at the frozen program revision against base data. No selftests, mutants, controls, after checks or unrelated gate reruns.
- **Additional provenance commands:** `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master`, `rev-parse 3ae0ab54`, `rev-parse 2f9eeafb`, `merge-base 3ae0ab54 2f9eeafb`, and `log -1 --format=%s` for base/freeze returned successfully. Master observed at that instant was cd2e25bb80cf618135cc001193df13966ef1c711; the report does not treat that moving tip as the measured program revision. Receipt heads were read with `git show 2f9eeafb:corpus/evidence/round77/<name>.txt` for rerun-r51-c1, rerun-r75-c1, c1-selftest, c1-before, c1-after and c2-selftest. Entire c1-selftest/c1-before objects were subsequently read in the clone. At-revision tool-object reads and SHA-256 results appear in the Mistakes table. Census and frozen ledger were read with `git show 2f9eeafb:<path>`; ledger SHA-256 was e268972164df734b7f6fc7ed95e86b56cbe0561584a2e44e60f8526149efb606.
- **Exploration failures, not evidence of product defects:** guessed lane-root CORPUS.md did not exist; an attempted JSON extraction using top-level `tasks` failed with KeyError, then the actual SourcesScribeR78 contract was read in full at dispatch line 183. No rule about source admission is claimed independently verified from the absent CORPUS.md file; the lesson identifies its contract provenance.
- **Touched surfaces:** this report only; temporary shared clone under the seat's scratch directory was removed in a finally block after measurements. No commits were made in any repository. No tools were installed or upgraded.
- **Known limits:** the sources seat's completed capture/report was not consumed; its contract was read. The S254 row intentionally preserves unknown capture values. No frozen text was repaired.
- **Artifact:** `.ufo/waves/round-78/w1/LessonScribeR78.md` contains the complete lesson draft and observed readings; no deleted scratch artifact is offered as evidence.
- **Self-evaluation:** accuracy 4 (observed C1 mismatch and unmeasured fields are explicit, but historical D1 truth is attributed to closure rather than independently replayed); completeness 4 (all requested sections and five mistake rows, with source capture deliberately left unmeasured as permitted); clarity 4 (draft and audit notes are separated, though the report is longer than a final lesson); actionability 4 (integrator can copy the full lesson, but S254 capture values remain contract-only); conciseness 4 (exact provenance and caveats add length). Overall 4.0. Main improvement is to integrate the sources seat's observed capture and final measurements without converting this seat's unknowns into execution evidence. The user should agree that these are explicit measurement limits, not silently completed work.

LESSON: drafted 5 rows

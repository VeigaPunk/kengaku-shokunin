# Wave 2 seat W2ConnectIndexBoth — corpus index, both directions (read-only)

Seat: connector, round 52 wave 2 (falsify). Judged on coverage. Lane: `kengaku-shokunin`, HEAD `87301ba`, base `30801b4`.
No lane file, no sibling file and no git state was modified. Only this report and `receipts/` were written under the wave dir.

## Verdict

The corpus index is **not clean in either direction**.

- **Direction B (new files → rows): fails.** 185 of 185 files added this round under `corpus/` have no README row. `corpus/README.md` contains zero occurrences of `round52` / `round-52`. The minimum fix is one directory row for `corpus/evidence/round52/graders/`, which covers the 89 task directories, `SHA256SUMS` and `EXCLUDED.md`.
- **Direction A (rows → files): 8 named lane artefacts are absent, and 5 rows resolve only from the fleet root.** The defects are concentrated in the round-45 evidence bullet and in four `.ufo/...` pointers.

Neither direction touches R52-C1's or R52-C2's frozen predicates. This is an index-hygiene finding, not a score-bearing one.

## What I attacked

The item: check `corpus/README.md` against the tree in both directions, and report missing rows and dangling rows with file:line evidence. I did not attack the grader instrument or the registry rows on this seat.

## Commands run (all read-only)

```
git rev-parse --show-toplevel                                  # lane root confirmed
git diff --name-status 30801b479e3418c11089b8586178b6960216f364 HEAD -- corpus
git diff --name-only --diff-filter=A 30801b47... HEAD -- corpus   # -> 185 paths (receipts/new-corpus-count.txt)
grep -n -i 'round52|round-52|round 52' corpus/README.md          # -> 0 hits
python3 index_census2.py   # scratch script: README token census + new-file coverage (receipts/census2-run.txt)
# inline first-cell check: every table row's first backtick token resolved against corpus/ and lane root,
#   then (for receipt rows at README:180-214) against corpus/evidence/  -> 177 ok at corpus/ or lane;
#   32 resolve only under corpus/evidence/ (heading "Root-level receipt logs"); all 32 present; 0 missing.
ls / find on: corpus/evidence/round45, round45/tb2-password-recovery, round46/tb2-polyglot-c-py,
              plans/refusals45, plans/battery*, .ufo/reports, ../.ufo/reports, ../research, ../MISSION.md, ../AXES.md
```

Census totals (`receipts/census2-run.txt`): 713 path tokens resolved, 127 unresolved by the naive resolver, 50 external or historical. The 127 are dominated by bare filenames whose directory is named in the same paragraph (checked by hand, below), by TB2 upstream-tree-relative names, and by container paths. The naive count is not a defect count; the manual triage below is.

## Direction A — README rows whose named artefact is absent or unresolvable from the lane

### A1. Strict dangling: named lane artefacts that do not exist (8 names)

| README line | Named | Finding |
|---|---|---|
| 643 | `../plans/battery45/` | Absent. `plans/` has `battery37`…`battery44` only; `find` for `battery45` returns nothing. The row also says "the 33 honest fixtures". |
| 643 | `f1_truncated_git.py` | Absent. Actual file: `plans/refusals45/f1_gitfile.py`. |
| 643 | `f4_fifos.py` | Absent. Actual: `plans/refusals45/f4_fifo.py`. |
| 643 | `f6_move.py` | Absent. Actual: `plans/refusals45/f6_above.py`. |
| 643 | `f8_worktree.py` | Absent. Actual: `plans/refusals45/f8_worktreecfg.py`. |
| 643 | `f9_describe.py` | Absent. Actual: `plans/refusals45/f9_nodescribe.py`. |
| 642 | `evidence/round45/frozen-digests.txt` | Absent. `corpus/evidence/round45/` lists `c1-counter-run.txt counter-a-run.txt counter-b-run.txt gate-call.txt password-recovery-dry-cases-freeze.txt password-recovery-probe.txt probe-run-envelope.txt tb2-password-recovery`. The three other names on that line exist. |
| 641 | `envelope.sh` (bare, under `evidence/round45/password-recovery-probe.txt`) | No copy under `corpus/` or `plans/`. It exists only at `.ufo/waves/round-45/claims/envelope.sh`, a wave scratch directory. |

Present and correct on line 643: `f3_abbrev.py`, `f5_alternates.py`, `f7_commondir.py`, `f10_laneinclude.py`.

### A2. Wrong base: the row resolves only from the fleet root `../`, not from the lane

| README line | Named | Where it exists |
|---|---|---|
| 125 | `.ufo/reports/round-29/kengaku.md` | `../.ufo/reports/round-29/kengaku.md` only. Lane `.ufo/reports/` contains `round-17` only. |
| 127 | `.ufo/reports/round-30/kengaku.md` | `../.ufo/reports/round-30/kengaku.md` only. |
| 119 | `.ufo/waves/kaika-w3/kengaku-review.md` | `../.ufo/waves/kaika-w3/kengaku-review.md` only. The row says "fleet", so this is declared, but a reader in the lane cannot resolve it. |
| 245 | `.ufo/l0-questions.md` | `../.ufo/l0-questions.md` only. Named in prose as the file a check reads. |
| 52, 180 | `research/round-18-kimi-model-routing/` | `../research/round-18-kimi-model-routing/` only. The row says "Parent repo". |

### A3. Declared historical or external (not lane artefacts; the row or the path says so)

About 50 tokens, all in the knowledge table (lines 29–45, marked `Historical-unavailable`), in the `~/` and `/tmp/` rows (lines 32–45, 82–85, 164, 251, 283, 321, 443), or container paths from TB2 task images (`/app/...`, `/tests`, `/logs/verifier/reward.txt`; lines 66–78, 298, 300, 304, 355, 371, 386, 403). Also `llm-wiki/...` (29–37), `arxiv.org/abs/2505.06120` (322), and model ids `hyper/qwen3.8-flash` / `opencode-go/deepseek-v4.1-flash` (197, 199). Not counted as dangling.

### A4. Upstream-tree-relative names, captured flat (not dangling for the capture; path convention mismatch)

Lines 296–346 and 574–647 name upstream TB2 paths such as `tests/test_outputs.py`, `environment/setup.sh`, `solution/solve.sh`, `build-pmars/tests/test_outputs.py`. The byte captures in this lane are flat. For example, `corpus/evidence/round45/tb2-password-recovery/` contains `test_outputs.py`, `test.sh`, `setup.sh`, `solve.sh`, `Dockerfile`, and `corpus/evidence/round46/tb2-polyglot-c-py/` contains `test_outputs.py`, `test.sh`, `solve.sh`, `Dockerfile`. Line 640 names `environment/setup.sh` and `environment/Dockerfile`, and line 647 names `environment/Dockerfile`; the flat captures exist under the basename.

### A5. Prose, not rows (no action)

- Line 126: `judge-calibration-thresholds.md` is named as a *refused* candidate. No file is expected.
- Line 91: `MISSION.md`, `AXES.md` exist at fleet root `../`.
- Bare fragments such as `.sha256`, `.py`, `.out` (170–171) and `-selftest.txt` (228) are extension fragments, not files.

### A6. Checked and resolved (false alarms from the naive census)

- All 32 bare receipt rows at lines 104–107 (under `### evidence/round29-attempt2/`) and 187–214 (under `Root-level receipt logs`, which resolve to `corpus/evidence/`) exist.
- Bullet and table rows at lines 170–176, 221, 228, 247, 557, 609, 630 resolve: the named files exist in their directories (`round9-fleet`, `round10-fleet`, `round11-power`, `round11-fleet`, `round12-ladder`, `round24-census`, `round25-calibration`, `plans/fixtures/r25`, `round33/catalogs`, `plans/battery40/43`).
- Every table entry cell (first column) in the knowledge, lessons and evidence tables resolves to an existing file.

## Direction B — new corpus files of round 52 → README rows

| Set | Count | Rows |
|---|---|---|
| `git diff --diff-filter=A 30801b4 HEAD -- corpus` | 185 | 0 |
| `corpus/evidence/round52/graders/*` (89 task directories, `SHA256SUMS`, `EXCLUDED.md`) | 185 files | 0 |
| `README.md` mentions of `round52` / `round-52` | — | 0 |

Notes on the 185:

- The 185 are 183 grader files, `SHA256SUMS` and `EXCLUDED.md`. `SHA256SUMS` has 184 lines because it intentionally lists the excluded `sanitize-git-repo/tests/test_outputs.py` (line 158, per `EXCLUDED.md`). Index-neutral; noted so the row does not overclaim 184 files.
- `git diff` shows `corpus/SOURCES.md` unchanged this round. The round-52 Gate block (`lessons/round-52.md`) and the claimed round-52 artefacts `corpus/evidence/round52/prior-art.md`, `confirmations.json`, `labels.json` are **absent** from the tree (`test -e` false, checked 2026-10-28). They cannot be indexed yet. R52-C1 legs 3–5 depend on them.
- Adjacent, outside `corpus/`: the four round-52 files under `plans/` (`round-52-claims.md`, `round52-tasks.json`, `round52_c1_grader_audit.py`, `round52_c2_registry.py`) have no README row either. The README indexes counters under `plans/` (rows for `round51_surfaces.py` and `round51_routing.py` at lines 672–675), so the same precedent applies. Recorded here, not counted in the 185.

## Minimal fix (for the L1 to decide; this seat did not edit the lane)

1. Add one row for `evidence/round52/graders/` (the 183 captures, `SHA256SUMS`, `EXCLUDED.md`), citing the pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`.
2. Fix line 643: replace the five wrong names with the actual `plans/refusals45/` names, and either add `plans/battery45/` or remove the reference.
3. Fix line 642: `frozen-digests.txt` is absent. Remove it or restore the file from its source.
4. Fix line 641: give `envelope.sh` its real path (`.ufo/waves/round-45/claims/envelope.sh`) or drop it.
5. Lines 119, 125, 127, 245 and 52/180: prefix as fleet-root paths (`../.ufo/...`, `../research/...`) so they are not read as lane paths.
6. Add rows for the four `plans/round-52*` files once the L1 accepts them.

## Receipts (`receipts/`)

- `index_census2.py` — the census script (the scratch copy; read-only; writes nothing in the lane).
- `census2-run.txt` / `census2-run.err` — its output (713 resolved, 127 unresolved, 50 external, 0 round-52 rows; exit 0).
- `new-corpus-count.txt` — `185` (new corpus files since base) and `0` (README round-52 mentions).

Scratch dir `/fast/scratch/hyaku/kengaku-r52/w2-W2ConnectIndexBoth/` removed after copying receipts.

## Tooling

No tool was installed or upgraded on this seat. All checks used the base `python3` and `git` binaries already present.

# R46W2LogAppend — `plans/log_appendonly.py` falsification

## Scope and setup

Tested the pinned lane clone at `42d5043afac952fcb43bf4798757785dd258cf85` (clone top-level verified) and fixture repos under `/fast/scratch/hyaku/kengaku-r46/R46W2LogAppend`. Every counter/fixture run used the required envelope; the recorded envelope lines end `unchanged`, not `INVALID`. Receipts (including full command/output and measured HEADs) are in `R46W2LogAppend/`.

## Counter behavior

- Lane at TIP, `python3 plans/log_appendonly.py --lane <clone> --show-lines`: exit 1, `commits=78 violations=7`. It enumerated seven historical rewrite commits, including `f660ae04a1c5` deleting the two lines at 1374/1388 and `3d9ea54a558b` deleting two different lines at 1407/1408. The report says 78 at the measured TIP; the earlier LOG.md entry records 77 at its measurement point. Receipt: `lane-plain.txt`.
- Lane since baseline `64ba8385ea10af1b78d367dcb242b92d97062af7`: exit 0, `commits=1 violations=0`; `WALK full-history=1 simplified=1`. Receipt: `lane-since-r45tip.txt`.
- Required mutation matrix: edit, delete, reorder, LF→CRLF, CRLF→LF, and whitespace-only change each returned exit 1 with at least one violation (receipts `fx-edit.txt`, `fx-delete.txt`, `fx-reorder.txt`, `fx-crlf.txt`, `fx-crlf-to-lf.txt`, `fx-ws.txt`). The first attempted `fx-crlf2lf.txt` was a no-op fixture (LF base rewritten as identical LF; no new commit); it is not counted as a test or miss. Corrected CRLF→LF test is `fx-crlf-to-lf.txt`.
- Rename: renaming `LOG.md` to `LOG2.md` is detected at the old path as a five-line deletion (exit 1, `fx-rename-old-path.txt`); the subsequent rewrite is detected when checking `--path LOG2.md` (`fx-rename-new-path.txt`).
- Additional checks: whole-file removal and replacement by symlink both flagged; first-parent merge walk found three rewrite commits; a rewrite at the exact `--since` boundary and an unreachable side-branch rewrite are not reported, consistent with the tool's documented limits. The built-in selftest passed. Receipts: `fx-rmfile.txt`, `fx-symlink.txt`, `fx-merge.txt`, `fx-since-boundary.txt`, `fx-abandoned-branch.txt`, `selftest.txt`.

**Mutation misses: 0 / 6.** All six requested mutation types were detected. Rename is detected as deletion of the tracked old path; checking the renamed path separately detects later edits there.

## D1 correction entry

The round-46 LOG.md change is append-only: `git diff 64ba8385ea10af1b78d367dcb242b92d97062af7 42d5043afac952fcb43bf4798757785dd258cf85 -- LOG.md` has one hunk `@@ -1412,3 +1412,69 @@`, no deleted content lines, and 67 additions. The appended correction is at EOF (the clone's LOG.md is 1480 lines; the entry starts at 1416). `d1-range.diff` preserves the measured diff.

The entry's quoted old/current heading and line match `4290d64:LOG.md` and `3d9ea54:LOG.md` at lines 1374 and 1388, respectively; both quoted old strings occur once in TIP's LOG.md. Those byte/content restoration claims are accurate.

**D1 attribution is inaccurate (defect).** The entry states: “commit `3d9ea54` rewrote two lines … that `4290d64` committed.” The counter's per-commit first-parent walk at TIP attributes deletion of those exact old lines (1374, 1388) to the earlier commit `f660ae04a1c5`; it separately attributes two other deletions (1407, 1408) to `3d9ea54a558b`. The endpoint range diff `fbad1c5..3d9ea54` proves the net content changed between those endpoints, not that `3d9ea54` made the 1374/1388 rewrite. The correction entry is appended correctly and restores the text, but its commit-level attribution overstates what that range diff establishes. Evidence: `lane-plain.txt`; `d1-range.diff`; closure D1 at `corpus/lessons/round-45-verifier-spotcheck.md:39-42`.

## Residual risk / verification gaps

The documented scope limits remain: only history reachable from HEAD is walked, `--since` excludes its boundary commit, and a renamed log must be checked under its new path to inspect subsequent edits. No other actionable counter miss was observed in this attack.

VERDICT: log-appendonly-misses-0-d1-entry-defect
# R9 mutation probe

Detector: `python3 plans/round31_defects.py --lane .` (the R9 implementation is `plans/round31_defects.py:265-289`; report set is `:55-61`). Scratch repo: `/tmp/r31fx-c2r9/`, fresh `git clone --shared` detached at `dbb07364` for each isolated attack. Pristine baseline output in `/tmp/r31fx-c2r9/lane`: `checks=10 defects=0`, exit 0.

| Attack | Exact operation/path | Detector output | Result |
|---|---|---|---|
| Revert one report | In `/tmp/r31fx-c2r9/revert`, overwrite `.ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md` with `git show 0883e72:<path>`, commit. Baseline 0883e72 blob is 94 lines; landed dbb07364 blob is 95 lines (commands: `git show 0883e72:<path> \| wc -l`, `git show dbb07364:<path> \| wc -l`). | `checks=10 defects=0`, exit 0 | SURVIVED: revert not detected because old report is not shorter than baseline and committed cleanly. |
| 120-line stub containing Pass 9 | In `/tmp/r31fx-c2r9/stub`, replace `.ufo/waves/round-30/build/R30DraftGate.md` with 120 lines all `Pass 9`, then commit. | `DEFECT R9 ... is shorter than at 0883e72 (120 < 199 lines): a revert is not the repair`; `checks=10 defects=1`, exit 1 | KILLED. It catches this stub only due to the baseline length comparison, not the `Pass 9` check (the stub satisfies that string test). |
| Append one line | In `/tmp/r31fx-c2r9/append`, append `probe append` to `.ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md`, commit. | `checks=10 defects=0`, exit 0 | SURVIVED, expected: exact unchanged bytes are not required by R9. |
| Delete then re-add identical bytes | In `/tmp/r31fx-c2r9/readd`, delete `.ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md` and commit, then restore its saved bytes and commit. `git diff 0883e72 HEAD -- <path>` has no output (zero lines). | `checks=10 defects=0`, exit 0 | SURVIVED: final committed blob is present and identical, as required. |

The comparison `current_lines < baseline_lines` (`plans/round31_defects.py:277-285`) is **not the right invariant** for proving the five reports remain intact: an older report with 94 lines passes against a 93-line baseline (exact commands and counts above), while a fabricated but long-enough blob can satisfy the count. It is useful as a narrow short-stub tripwire. Better invariant for this frozen criterion is per-report committed blob identity against the expected repaired blob(s) at `dbb07364` (or, if only avoiding older revision, assert current blob hash differs from the 0883e72 blob and remains present). The frozen claim explicitly requires bytes intact (`plans/round-31-claims.md:67-69`), so the hash/identity check directly matches it; append-only content could be accepted only if criterion is adjusted to permit it.

Tool installs/updates: none. Scratch clones and generated commits remain only under `/tmp/r31fx-c2r9/`.

VERDICT: R9 catches the 120-line short stub and misses the baseline revert, one-line append, and identical delete/re-add; the shorter-than-baseline test is only a stub heuristic, not the correct invariant for report integrity.

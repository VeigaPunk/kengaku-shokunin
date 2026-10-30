# R5LedgerCorrectionAudit — scoped findings (E4 ledger corrections)

Audit of E4's working-tree corrections to `plans/round54-entrytruth.json` at landing HEAD
`248a42b8` (base `798f5e9`). Bounded wait: file changed at poll step 25 (~25 min), working-tree
only (uncommitted).

## Correction scope (vs base 798f5e9) — verified
- Changed: `round35-c1-coverage` (evidence 57/57→58/58, sec 0.7→0.5, reason rewritten).
- Added: `round54-c1`, `round54-c2`, `round55-c2`, `round55-c2-controls`, `round55-c3`.
- Removed: none. Other rows changed: none (77 byte-identical). Schema unchanged.

## Per-row verdict (measured hermetically in a clean worktree @248a42b8 + landing script overlay)
| Row | Declared | Measured | Evidence verbatim? | Verdict |
|-----|---------:|---------:|--------------------|---------|
| round35-c1-coverage | 1/red | 1/red | YES `files=58 index rows=58 (want 42/42)` | AGREE |
| round54-c1 | 1/red | 1/red | YES `ModuleNotFoundError: No module named 'opentimestamps'` | AGREE |
| round54-c2 | 2/red | 2/red | YES `SETUP --source and --work are required unless --dry` | AGREE |
| round55-c2 | 2/red | 2/red | YES `SETUP --source and --work are required unless --dry` | AGREE |
| round55-c2-controls | 2/red | 2/red | YES `one of the arguments --case --selftest is required` | AGREE |
| round55-c3 | 0/green | 0/green | n/a (green rows carry no evidence by convention) | AGREE |

**Result: 6/6 AGREE.** All declared exits/states match my independent measurements; all declared
red-row evidence fragments are verbatim in my output.

## Calibration caveat (residual risk, not a disagreement)
`round35-c1-coverage`'s fragment is revision-sensitive. It is truthful for a **clean clone of the
committed HEAD `248a42b8`** (tb2 knowledge file still untracked → `files=58`; committed README →
`index rows=58`). It becomes stale once R55-C3's knowledge file/README row are committed
(predicted `files=59 index rows=59`). If the after-run measured-after revision includes the
committed C3 knowledge file, the fragment must be re-derived to `59/59`.

## Cross-checks
- No other row changed (field-level vs base).
- L1 binding spot-check: all 5 new ledger `entry_argv` token-equal the `SKILL.md` registry entries.
- round55-c3 registry verdict-map records exactly my bare-entry measurement
  (`cases=12 observed_pass=5 observed_fail=7 mismatches=0`, exit 0).
- Live lane left unpolluted; all execution in scratch (now removed).

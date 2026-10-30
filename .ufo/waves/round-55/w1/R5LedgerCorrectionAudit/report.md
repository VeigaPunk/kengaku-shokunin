# R5LedgerCorrectionAudit — E4 ledger-correction audit (round 55, w1)

Seat: `R5LedgerCorrectionAudit` (leaf reviewer; calibration). No subagents dispatched. No lane
writes. No installs/upgrades this seat (none needed). Scratch:
`/fast/scratch/hyaku/kengaku-r55/R5LedgerCorrectionAudit/` (deleted on exit).

## What was assigned

Audit E4's corrections to `plans/round54-entrytruth.json` after a bounded wait for the file to
change. Independently re-run `plans/round35_c1_verify.py --lane <clean clone>` (evidence must be
verbatim from my output too); re-measure each of the five new rows' entries hermetically in
scratch (declared exit/state must match my measurement); verify no other row changed vs the
committed base ledger `798f5e9ef30ef39291295565209b65a17343c00e`.

## Bounded wait

Polled the live lane `plans/round54-entrytruth.json` every 60 s (max 25 min). The file changed at
step 25 (~25 min). Landing HEAD at change: `248a42b8c73b6415963f16b13127a9aa6d4c997c`. The
correction is in the **working tree only** (` M plans/round54-entrytruth.json`, uncommitted); HEAD
itself still carries the base bytes. The two commits landed during the wait
(`0d11d9ab`, `248a42b8`) are honest-stop / LOG entries and do not touch the ledger.

## Scope of E4's corrections (working tree vs base 798f5e9)

Field-level diff of every row:

- **Changed (1):** `round35-c1-coverage` — `evidence` 57/57 → 58/58, `sec` 0.7 → 0.5, `reason` rewritten.
- **Added (5):** `round54-c1`, `round54-c2`, `round55-c2`, `round55-c2-controls`, `round55-c3`.
- **Removed (0).** **Other rows changed (0)** — the remaining 77 base rows are byte-identical.
- Top-level structure and `schema` (`r54-entrytruth-v1`) unchanged.

This is exactly the expected correction set (R55-C2 ledger-truth legs a + c).

## Measurement environment

Clean worktree of the landing HEAD `248a42b8` in scratch (functioning `.git`, so the verify
script's `git ls-files` leg works), overlaid with the untracked landing scripts
`plans/round55_c2_entryargv.py`, `plans/round55_c3_chess_probe.py` (`round55_c2_controls.py` is
committed at the freeze). Round-35 verify and all five entries run inside this scratch tree —
never in the live lane. `round54-c1`'s `--work work/anchor-verify-row` writes stayed in scratch.

## Per-row agree/disagree (measured exits)

| Row | Declared exit/state | My measured exit/state | Evidence verbatim from my output? | Verdict |
|-----|--------------------:|-----------------------:|-----------------------------------|---------|
| `round35-c1-coverage` (changed) | 1 / red | **1 / red** | YES — `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)` | **AGREE** |
| `round54-c1` (new) | 1 / red | **1 / red** | YES — `ModuleNotFoundError: No module named 'opentimestamps'` | **AGREE** |
| `round54-c2` (new) | 2 / red | **2 / red** | YES — `SETUP --source and --work are required unless --dry` | **AGREE** |
| `round55-c2` (new) | 2 / red | **2 / red** | YES — `SETUP --source and --work are required unless --dry` | **AGREE** |
| `round55-c2-controls` (new) | 2 / red | **2 / red** | YES — `one of the arguments --case --selftest is required` | **AGREE** |
| `round55-c3` (new) | 0 / green | **0 / green** | n/a — green rows carry no evidence (see note) | **AGREE** |

Raw captured outputs (exit codes above; full text preserved during the run):

- round35 (clean clone @248a42b8): `V1..V3 ok`, `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)`, `V5 V6 ok`, `checks=6 defects=1`, `PREDICATE C1 fail`, exit 1.
- round54-c1: traceback ending `ModuleNotFoundError: No module named 'opentimestamps'`, exit 1.
- round54-c2: `SETUP --source and --work are required unless --dry`, exit 2.
- round55-c2: `SETUP --source and --work are required unless --dry`, exit 2.
- round55-c2-controls: argparse usage error `... error: one of the arguments --case --selftest is required`, exit 2.
- round55-c3: `cases=12 observed_pass=5 observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass`, exit 0.

**All six rows: AGREE.** Every declared exit and state matches my independent measurement; every
declared red-row evidence fragment is verbatim present in my captured output.

## Cross-checks (all pass)

- **No other row changed:** field-level comparison vs base — only `round35-c1-coverage` changed,
  5 added, 0 removed, 77 byte-identical, schema intact.
- **L1 argv binding (spot):** all five new ledger `entry_argv` **token-equal** the corresponding
  `SKILL.md` gate/probe registry entry commands (registry rows added this round; base had 0).
- **round55-c3 registry cell consistency:** the SKILL.md verdict-map records the bare entry as
  `cases=12 observed_pass=5 observed_fail=7 mismatches=0`, exit 0 — exactly my measurement.
- **`round55-c3` sparse row is correct, not a defect:** every green row in the ledger omits
  `evidence` (63/63 green rows have none; evidence is red-row-only, 20/20 red rows have it).
- **`opentimestamps` absent** on this host's `python3`, matching E4's stated reason for `round54-c1`.

## Residual risk / caveats (not disagreements)

1. **round35 fragment is revision-sensitive (calibration caveat).** E4's `files=58 index rows=58`
   reproduces verbatim only in a **clean clone of the committed HEAD `248a42b8`**, where the
   R55-C3 knowledge file `corpus/knowledge/tb2-chess-best-move-grader.md` is still untracked
   (excluded from `git ls-files`) and the committed `corpus/README.md` has 58 knowledge rows.
   Measured across states:
   - clean HEAD clone → `files=58 index rows=58`  ← E4's declared value (matches the assigned
     "run in a clean clone");
   - committed git + working-tree README → `files=58 index rows=59`;
   - **predicted final R55-C3-committed landing → `files=59 index rows=59`** (once the tb2
     knowledge file and README row are committed, both counts become 59).
   So the fragment is truthful for the current landing revision but will go stale the moment the
   C3 knowledge file/README row land in a commit. If the after-run's measured-after revision
   includes the committed C3 knowledge file, the fragment must be re-derived to `59/59`. This is
   a data-staleness risk, not a false declaration at the revision E4 measured.
2. **Uncommitted working-tree state.** The whole correction set is unstaged/uncommitted at
   `248a42b8`; final byte-truth depends on the L1's integration commit.
3. **Registry set (sibling scope).** The live registry (`SKILL.md`) already carries the 5 new rows
   in the working tree; `round53-tipstate.json` is the tip-state snapshot (not the live registry)
   and correctly still lists 78. Ledger-set ═ registry-set closure is R55-C1/L1 integration work,
   out of this seat's scope; not E4's defect.

## Dead ends / environment notes

- A first working-tree-only copy (no `.git`) yielded `files=0 index rows=59` — an artifact:
  V4 counts committed knowledge via `git ls-files` (needs `.git`) and reads the working README
  (59 rows). Resolved by measuring in a clean worktree at `248a42b8` (gives E4's 58/58).
- `/fast` scratch intermittently returned a transient `i/o error` from the `cd` builtin; absolute
  paths and `git -C` worked throughout.

## Installs / upgrades

None (no tools installed or upgraded by this seat).

## Files written (lane outputs)

- `.ufo/waves/round-55/w1/R5LedgerCorrectionAudit/report.md` (this file)
- `.ufo/waves/round-55/w1/R5LedgerCorrectionAudit.md` (scoped findings)

Round 48 seat R48C1HoStore — benign Git metadata counterexamples

Axes: calibration (assigned). No admission judgment or C1/C2 claim made.

Commands and observed evidence:
- Read the full frozen claims at `plans/round-48-claims.md`, the full `corpus/lessons/round-46-verifier-spotcheck.md`, `SCORECARD.md` lines 1980–2097, `plans/fixture_fence.py` relevant sections, refusal fixtures `f7_commondir.py`, `f5_alternates.py`, `f8_worktreecfg.py`, and peer pattern report `R48C1ConnPattern.md`.
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` → `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`.
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse a543d92083557dd9b33ee674e9b99b03411f80af^{tree}` → `e91c8156c64031483529035923ee1182dcfff31d`.
- `git -C ... cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af` → `commit`; `merge-base --is-ancestor ... HEAD` → exit 0. Claims blob from that commit and worktree copy both sha256 `87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672`; commit date `2026-10-27T06:53:29-03:00`.
- No score, counter, probe, fixture, or Git mutation was run. The stage-2 counter/population/control freeze is absent at the frozen revision: `plans/round48_c1_verify.py`, stage-2 literals/pins, and pre-receipt control receipts are not in that committed tree (also recorded by `R48C1ScribeSynth.md` lines 54–59). Accordingly the required prerequisite for scoring is not met. The present HEAD being later does not authorize a score before stage 2.
- Scratch command: `mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C1HoStore && export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1HoStore; printf 'TMPDIR=%s\n' "$TMPDIR"; rmdir /fast/scratch/hyaku/kengaku-r48/R48C1HoStore; test ! -e /fast/scratch/hyaku/kengaku-r48/R48C1HoStore && printf 'scratch_removed=yes\n'` → `TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1HoStore`, `scratch_removed=yes`.

Counterexample and interpretation (static, not measured):
- A legitimate linked worktree fully contained under `d` has a `.git` gitdir-pointer file in the worktree and a worktree gitdir whose `commondir` resolves to the shared repository under `d`. The current fence's `_tree` rejects any `.git` file as “gitdir redirect” (`fixture_fence.py:212–213`); `_store` then permits only plain-init entries and rejects `commondir` (`:453–465`). Thus this ordinary, wholly in-`d` metadata layout is an over-refusal candidate, not evidence of outside access. The required distinction is whether the resolved gitdir/common-dir bytes and actual traced reads remain under `d`, not whether metadata uses Git's worktree indirection.
- A legitimate alternate object store under `d` is likewise a candidate over-refusal: `_store`'s plain-init top-level allowlist and object-tree validation do not model `objects/info/alternates` (`:453–525`). An alternate resolving outside `d` is different: refusal is expected, and an admission is a leak only if tracing observes outside opens/reads.
- An in-`d` `.git/commondir` target deserves the same treatment: an in-tree target alone is not grounds for refusal; an outside target remains hostile. Existing round-46 `f7_commondir.py` is explicitly hostile because its `commondir` points beside `d` (lines 1–4, 11–29); `f5_alternates.py` is explicitly hostile because the alternate object store is beside `d` (lines 1–16). These cases establish the boundary, not that an in-`d` counterpart was measured.
- Round-46's reported 9/9 honest refusals were ordinary repository states, and its frozen rule treated any honest refusal as a C1 kill. The round-48 frozen predicate further specifies that `LEAK` requires traced outside access (`touches>0` or READ) and that zero-touch admissions are separately `BENIGN-ADMIT`; no inference of leakage should be drawn from admission alone.

Smallest safe correction: when stage 2 is committed, add paired frozen honest/hostile fixtures for linked-worktree gitdir+commondir and alternates: resolve both relative and absolute metadata targets against their correct Git base, accept only when every resolved metadata/store path is inside `d`, and have the trace classify outside opens/reads as hostile leakage. Keep the frozen kill rule unchanged; do not treat a refusal of an all-in-`d` Git layout as success. No implementation or counter change was made.

Exact source commands: repository files were read with the `read` tool at the paths/sections above; revision checks used the exact `git -C` commands listed above; `grep` searched the round-48 wave directory for `commondir|alternates|worktree|linked worktree`.

Sources opened (local URLs; access date 2026-10-27), located quotes (each ≤25 words):
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — “a fixture result is `LEAK` only if traced opens/reads outside `d` are observed” (§C1).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — “9/9 novel honest fixtures refused” (Routed defects).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/SCORECARD.md` — “commondir (V1)” (§Planned round 45).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixture_fence.py` — “Anything the parser does not fully classify is refused.” (`_config` docstring).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/refusals46/f7_commondir.py` — “a hand-written `.git/commondir` sends refs, objects and config to a store built BESIDE d.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/refusals46/f5_alternates.py` — “the fixture's object store borrows from a store outside d”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/refusals46/f8_worktreecfg.py` — “its second config file `.git/config.worktree` carries an include that names a file OUTSIDE d.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ConnPattern.md` — “Stage-2 freeze absent.”

Limits: No Git fixture was constructed; no behavior was measured; static analysis cannot establish the future v3 counter's classification. No external sources were opened. Stage-2 is a hard blocker to scoring, not permission to improvise a score. No tool installed or updated.

VERDICT: calibration — identifies an in-`d` linked-worktree/alternate over-refusal counterexample in the current fence by inspection; not empirically scored; stage-2 freeze absent, so no C1 admission verdict.
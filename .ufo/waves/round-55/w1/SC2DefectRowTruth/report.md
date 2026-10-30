# SC2DefectRowTruth — report

Seat `SC2DefectRowTruth`, kengaku round 55, wave 1 (v2, build+attack).
Judged axis: **calibration**. Scope: independent truth for the ledger row
`round35-c1-coverage` (double-run beside E4). Full deliverable:
`.ufo/waves/round-55/w1/SC2DefectRowTruth/round35-truth.md`.

## 1. What I ran

| # | command | cwd | exit | result |
|---|---|---|---|---|
| 1 | `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin clone` | scratch | 0 | HEAD `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`, `git status --porcelain` empty |
| 2 | `python3 plans/round35_c1_verify.py --lane .` | clone | **1** | full stdout captured (below), stderr empty |
| 3 | same, ×3 more (repro/determinism) | clone | 1 each | 4/4 byte-identical output, sha256 `69d71d19…8d337d` |
| 4 | `git clone --shared --no-checkout … oldclone && git checkout -q 6e0a1915 && python3 plans/round35_c1_verify.py --lane .` | scratch | 1 | fragment at the ledger's declaration tip was `…files=57 index rows=57…` |
| 5 | `git ls-tree`/`git diff --name-status` count of `corpus/knowledge/*.md` and `^\| \`knowledge/` rows across `6e0a1915..80afa613` | clone | 0 | 57→58 at `9a0746be` |
| 6 | `git show 9a0746be -- plans/round54-entrytruth.json` | clone | 0 | 3 rows re-derived at that commit; `round35-c1-coverage` **not** among them |
| 7 | `python3 plans/round54_c2_entrytruth.py --lane . --source . --work … --jobs 6` | clone | 1 | **completed** (239 s): `EVIDENCE-MISSING round35-c1-coverage fragment not in output`, `evidence_missing=1` (full output in §5) |
| 8 | substring test of the ledger's declared fragment against the captured stdout | scratch | 0 | `declared in stdout? False` |
| 9 | `python3 plans/round35_c1_verify.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` (live in-flight tree, read-only) | scratch | 1 | `V4 DEFECT knowledge files=58 index rows=59 (want 42/42)`, `V6 DEFECT census exit 1` — dirty-tree transient, see §4 defect 4 |

No mutating git/jj command was executed anywhere (only `clone` and a read-revision
`checkout` inside a scratch clone). No lane-tracked file was written.

## 2. Full captured output (command 2)

stdout, verbatim and complete:

```
V1 ok
V2 ok
V3 ok
V4 DEFECT knowledge files=58 index rows=58 (want 42/42)
V5 ok
V6 ok
checks=6 defects=1
PREDICATE C1 fail
```

stderr: empty (0 bytes). Exit code: `1`.

## 3. Headline finding

- **Truthful fragment NOW (tip `80afa613`):**

  ```
  V4 DEFECT knowledge files=58 index rows=58 (want 42/42)
  ```

- **Declared in `plans/round54-entrytruth.json` row `round35-c1-coverage`:**

  ```
  V4 DEFECT knowledge files=57 index rows=57 (want 42/42)
  ```

- **Delta:** exactly the two integers `57 → 58` (knowledge-file count and README index-row
  count). The `V4 DEFECT` prefix, the field names, the `(want 42/42)` suffix, the exit code
  (1) and the state (red) are unchanged. No other output line changed: V1/V2/V3/V5/V6 still
  print `ok`, `checks=6 defects=1` and `PREDICATE C1 fail` are unchanged.

- **Cause:** commit `9a0746be` ("round-54: retain settled wave findings and honest-stop source
  interpretation") added `corpus/knowledge/external-anchor-freeze.md` and its README index row,
  moving both counts 57→58. That commit re-derived three *other* ledger rows' evidence but
  left `round35-c1-coverage` at its declaration-tip value. The declared fragment was correct
  at `6e0a1915` (re-verified by running the entry there) and went stale at `9a0746be`.

- **Why it matters for R55-C2 (calibration):** the counter matches a red row's declared
  fragment as a **substring** of the entry's stdout
  (`plans/round54_c2_entrytruth.py:338` — `sp.get("evidence") not in r["out"]`). The declared
  57-fragment is *not* a substring of the current stdout (empirically `False`; the 58-fragment
  is `True`). As the ledger stands, this row yields `EVIDENCE-MISSING round35-c1-coverage`,
  which breaks R55-C2's frozen after-predicate `evidence_missing=0`. The fix is the ledger
  correction R55-C2 (a) already mandates, with the fragment re-derived **at the landing
  revision**, not copied from this seat's measurement.

- **Landing-revision rule (important):** the fragment is a function of the tree, not a
  constant. At the landing revision it will be
  `V4 DEFECT knowledge files=<N> index rows=<N> (want 42/42)` with
  `N = git ls-files 'corpus/knowledge/*.md' | wc -l` there (equal to the README
  `^| \`knowledge/` row count if index rows are added in lockstep).
  `[INFERENCE]` R55-C3 adds exactly one knowledge entry plus one README index row → predicted
  `N = 59` → `V4 DEFECT knowledge files=59 index rows=59 (want 42/42)`. Not measured: no
  round-55 corpus entry had landed in the tree I measured. The L1 must re-run the entry at
  the landing revision and commit the observed line.

## 4. Defects found

1. **Stale ledger evidence (the seat's target).** `round35-c1-coverage.evidence` is one
   corpus-entry behind the entry's actual output; it must be corrected to the observed line
   before the R55-C2 after-run. Severity: blocks `evidence_missing=0` if left as-is.
2. **Structural cause of the drift (report, not a fix I may make).** The counter
   `plans/round35_c1_verify.py` hardcodes `want 42/42` for the knowledge-file/index-row
   counts (`v4()`), while the corpus has grown to 58. The row is therefore *permanently red
   by design drift* — the honest declaration is "red, with this exact fragment", not
   "green". Changing the tool's constant would be a rule/frozen-instrument change and is
   out of scope for this seat; the frozen claims only authorise the ledger **data**
   correction.
3. **Latent fragility (same class, adjacent):** the 57→58 move was caught for three other
   rows at `9a0746be` but missed for this one — i.e. ledger evidence fragments are re-derived
   ad hoc, not by a sweep. Any row whose entry output embeds a corpus-count is exposed to the
   same staleness. **Sweep result (observed):** the unchanged r54 counter re-executed all 78
   ledger rows at the tip and reported `evidence_missing=1` — only this row — so no other row
   is stale in the same way today.
4. **Measurement hazard for the correction (observed on the live in-flight lane).** `v4()`
   counts knowledge files with `git ls-files` (**tracked only**) but index rows by reading
   `corpus/README.md` from the **working tree**. A read-only snapshot of the live tree during
   this wave printed `V4 DEFECT knowledge files=58 index rows=59 (want 42/42)` — the
   round-55 README index row for `knowledge/tb2-chess-best-move-grader.md` is already in the
   README while the entry file has not landed. **The L1 must re-derive and commit the
   fragment at a clean, committed landing revision**; a mid-flight or dirty-tree measurement
   bakes an asymmetric `58/59` shape into the ledger and the row stays `EVIDENCE-MISSING`.
   (That snapshot also printed `V6 DEFECT census exit 1` — the live-lane branch of `v6()`
   validating an in-flight `corpus/SOURCES.md`; on a clean clone `V6 ok`. Not this row's
   defect.)

## 5. Corroboration run — OBSERVED

The fleet r54 counter (`plans/round54_c2_entrytruth.py`, unchanged) was run against the tip
clone; it **completed** (exit 1, 239 s wall, `--jobs 6`) and its full output is:

```
ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb clean=yes lane_rev_equal=yes
  EVIDENCE-MISSING round35-c1-coverage fragment not in output
  LAUNDERED round52-c2 declared green, entry exit=1
RUN executed=78 timeout=0 mismatched=0 evidence_missing=1 laundered=1
TIPSTATE entry_declared_green=62 entry_declared_red=16 observed_green=61 observed_red=17
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R54-C2 fail
```

Key readings (mine vs not mine):

- `EVIDENCE-MISSING round35-c1-coverage fragment not in output` — **observed**, and it is the
  **only** `evidence_missing` in the whole 78-row ledger (`evidence_missing=1`). The stale
  fragment is a single-row defect, not a class-wide one.
- The r54 counter's static legs are clean at this tip (`missing=0 extra=0 argv_defect=0
  bad_decl=0 duplicate_names=0`), so the defect is purely the stale evidence *datum*, not a
  declaration-shape problem → the fix is a one-line data correction.
- `LAUNDERED round52-c2 declared green, entry exit=1` and the `declared_red=16 /
  observed_red=17` skew belong to **other rounds' surfaces** (the R55-C1 registry regression
  that R55-C1's repair and R55-C2 clause (b) address), not to my row. I report them for the
  L1 and touch nothing. `laundered=1` is the known r54 soundness gap that R55-C2's new
  binding legs close.

### Dead ends

- The first corroboration attempt was killed at the 300 s default deadline — the counter
  buffers all output until the end, so the partial file was empty (0 bytes). A second attempt
  aborted immediately with `fatal: destination path …/work54/w0/src already exists and is not
  an empty directory` because the killed run left its scratch clone behind: **a re-run needs a
  fresh `--work` directory**. Third attempt with a fresh `--work …/work54b` succeeded.
- `git clone --shared --no-checkout` + `checkout` of a read revision was the clean way to
  re-measure the entry at the ledger's declaration tip `6e0a1915` without touching the lane.
- The counter's own output at the tip does not depend on the live lane: `v6()` detects that
  the lane is not the live lane and validates the clone's own `corpus/SOURCES.md`
  (`--file`), so the run is side-effect-free on the fleet root and on the live lane.

## 6. Files written (only these)

1. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-55/w1/SC2DefectRowTruth/round35-truth.md` — the deliverable (truth, delta, root cause, landing rule).
2. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-55/w1/SC2DefectRowTruth/report.md` — this report.
3. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-55/w1/SC2DefectRowTruth.md` — the `Report:` trailer.

Nothing else in the lane repo was created or modified. Scratch
(`/fast/scratch/hyaku/kengaku-r55/SC2DefectRowTruth/`) was deleted at the end of the seat,
after the outputs above were copied in.

## 7. Tooling

No tools were installed or upgraded (nothing needed beyond the lane's own `python3` and
`git`). No network access was used.

## 8. Boundaries respected

No subagents dispatched (leaf seat). No `git add/commit/push/stash/checkout/reset` in the lane
repo. No writes to `MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`, the fleet root's
`scripts/` or `templates/`, any sibling repo, or `.scratch/`. The frozen claims, predicates,
counters and kill rules were read, not modified.

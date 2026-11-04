# Round 82 — registry completeness, the round-81 bill, and the sweep at one tip

Lane `kengaku-shokunin`, round 82, hyaku run 15, attempt 1, 2026-11-04. L1 `KengakuR82`.
Base `a3a03ac31451e58f1742b9bccb73b72c2d90a95c`; freeze `12f1029a45cf0097a3afd030d757bf93b87f8018`.

Three claims, three surfaces: **R82-C1** (coverage) — every `plans/**/*.py` that exists at the base
revision, outside `plans/fixtures/`, and is referenced as a literal path by `SCORECARD.md`, `LOG.md`
or `corpus/README.md` at that revision now either carries a row in `SKILL.md`'s
`## Gate/probe registry` or sits in a frozen `EXCLUSIONS` table with a reason the counter verifies
from the file's own bytes; **R82-C2** (calibration) — the round-81 verifier spot-check's `V1`…`V7`
are discharged as `R81-V1`…`R81-V7` rows with checks that fail at the base revision; **R82-C3**
(capability acquisition, freshness instrument) — `sweep-at-one-tip` re-runs every executed
population member's own replay instrument at one measured tip and classifies it, with the census as
the deliverable and no divergence smoothed.

## Gate

Sources opened this round (S262–S264). Every row's URL, access date and ≤25-word located quote:

- **S262 — admitted (tier A).** `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/`
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/tests/test.sh`, fetched
  **2026-11-04T09:37:08Z** (HTTP 200, 608 B, sha256 `4770437ea96c…`; byte-identical for
  `sqlite-with-gcov`). Located quote, `:18-22` + `:26`: “uvx -p 3.13 -w pytest==8.4.1
  -w pytest-json-ctrf==0.3.5 pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA”
  (12 words) and “echo 1 > /logs/verifier/reward.txt” (6 words). Why it matters: the graded verdict
  at the pin is the exit status of pytest over the task's own test file, which is exactly the surface
  the lane's replay instruments model — the sweep's premise, not a decoration.
- **S263 — admitted (tier A).** `…/nginx-request-logging/tests/test.sh`, fetched
  **2026-11-04T09:37:08Z** (HTTP 200, 634 B, sha256 `27761195f53c…`). Located quote, `:20` and
  `:22`: “-w requests==2.32.4” (1 word) and “-v -rA” (2 words). Why it matters: per-task entries
  differ only in the pytest working set, so the entry shape is a template and a sweep comparing
  instruments by their own test-function calls is entry-shape agnostic.
- **S264 — rejected.** `…/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pyproject.toml`, fetched
  **2026-11-04T09:37:08Z** → **HTTP 404** (14 B `404: Not Found`); `run-tests.sh` and
  `tests/run-tests.sh` are 404 at the same revision. Reason: no locator, so no anchor and no claim;
  a rejected locator is not evidence that the harness has no packaging. Flip condition: a revision
  that carries the file — re-open then.

All three rows are cited by `corpus/knowledge/tb2-replay-sweep-at-one-tip.md` (S262/S263) and the
round's report; the census at round start and round end is rc 0 (see the report's Sources &
frontier section).

## Mistakes

**M82-1 — a probe is not read-only because it takes `--receipt`.** Two of the L1's own probe runs at
06:33 (`plans/round68_c1_pypi_finish.py --lane . --work … --receipt <scratch>`) wrote
`corpus/evidence/round68/pypi/server-log.txt`, `…/stderr/K1.txt` and `…/stderr/K3.txt` **inside the
lane**: `plans/round68_c1_pypi_finish.py:103` falls back to `lane / EVID_DIR` unless `--evidence-dir`
is passed. The worktree was dirty for every measurement after that until the L1 reverted the three
files from `master`. Captured by: `PlansReconR82` §0.1 (`git status --porcelain`, the diff showing the
scratch path baked into the bytes). Fix, and how it can fail: the sweep runs against a disposable
`git clone --shared` and stamps `WORKTREE`; the counter's `--check` refuses a census without a
`WORKDIR` line and its selftest carries a `no-run` case. A future probe that writes into the lane
still shows up as a dirty worktree at the next `git status` — the stamp is the tripwire, not a promise.

**M82-2 — a registry row with pipes in a cell silently disappears.** The first `round82-c3-sweep` row
spelled its flag list as `--selftest|--mutants|--control-ledger-copy|…`; every `|` split the row into
more than eight cells, so `plans/round52_c2_registry.py` dropped the row and went on reporting
`MISSING plans/round82_c3_sweep.py` **while the row was visibly in the file**. Captured by: the
counter itself (`MISSING 1` with the row present at `SKILL.md:736`). Fix: comma-separated flag lists,
and the eight-cell count is checked on every row (`rows with bad cell counts: 0`). It can fail again:
any new cell containing a literal pipe re-triggers the same `MISSING`.

**M82-3 (earlier round, mined) — a receipt minted over a moving worktree is not a measurement of a
tree.** Round 81's `corpus/evidence/round81/c2-after.txt:3` stamped `WORKTREE dirty (1 paths)` while
the commit message and report said “re-minted … in a clean clone”; the round's own M81-2/Q58 rule
(a dirty receipt is not comparable evidence) had been applied to C1's receipt only. Captured by: the
round-81 verifier spot-check (V1). Fix: the C2 receipt is re-minted from a clean clone this round and
the rule is stated as a receipt rule, not a C1 rule; the check greps `WORKTREE clean` so a dirty
re-mint fails mechanically.

## Corrections (the R81-V discharges, with the literal each check re-derives)

- **R81-V1** — `c2-after.txt` re-minted at a clean clone; literal `WORKTREE clean`.
- **R81-V2** — the round-81 lesson's counts recompute, and the two registry anchors S260/S261 carry
  their corrected counts and line ranges as **supersede rows** (`supersedes S260` / `supersedes S261`),
  because `corpus/QUALITY.md` Q34 and the fleet contract make every S-row cell except
  status/recheck/used-by immutable under its id — an in-place fix would have been the very rule-2
  defect the row records. The frozen rows keep their bytes and a check re-derives that too.
- **R81-V3** — the knowledge entry opens with the provenance trio; literal `recheck: 2026-12-04 (30d)`.
- **R81-V4** — the round-81 debt counter's mutant count states what its battery prints; literal
  `MUTANTS real=`.
- **R81-V5** — the stray `--lane/` directory is gone; literal `--lane/ directory`.
- **R81-V6** — this wave's attack share and the live mutation seat; literal `attack share`.
- **R81-V7** — `determinism.txt` carries its command and revision; literal `COMMAND`.

## Wave record

(see the report's round-shape section for the seat tally; the wave's `.ufo/waves/round-82/w1-results.json`
is the authority and the `R81-V6` check reads it.)

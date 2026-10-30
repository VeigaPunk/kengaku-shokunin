# E10NoharmRuns — round-55 w1 no-harm evidence report

Seat: E10NoharmRuns (leaf, no-harm). Lane: kengaku-shokunin.
Measured rev: **80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb** (lane `master` tip at run time;
freeze + before-receipts commit; base of record 798f5e9ef30ef39291295565209b65a17343c00e).
Clone: `git clone --shared` of the lane into
`/fast/scratch/hyaku/kengaku-r55/E10NoharmRuns/lane`, clean tree, rev verified after clone.
A detached worktree at base 798f5e9e was added inside the same clone for the r51
comparison only. No lane writes; no git/jj mutations in the lane (worktree add/remove
stayed inside my scratch clone). No tool installs this seat (nothing needed; pacman
untouched per operator pause).

## Per-check verdict table (all run from the clean clone at rev 80afa61314fa)

| # | Command | Expectation | Observed | Exit | Verdict |
|---|---------|-------------|----------|------|---------|
| 1 | `python3 grader.py` | CHECKS n=733 mismatches=0, VERDICT PASS | `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline` | 0 | PASS |
| 2 | `python3 grader.py --selftest` | ALL PASS | `[selftest] ALL PASS` (S1–S7 all PASS) | 0 | PASS |
| 3 | `python3 plans/round52_c2_registry.py --selftest` | cases=3 failures=0 | `SELFTEST cases=3 failures=0` (ok incomplete-fixture etc.) | 0 | PASS |
| 4 | `python3 plans/round55_c2_controls.py --selftest` | cases=4 failures=0 | `SELFTEST cases=4 failures=0` (incl. `ok abbreviation-live (--selft exits 0)`) | 0 | PASS |
| 5 | `python3 plans/round51_surfaces.py --lane <clone>` | ANCHORS 20/20 + PREDICATE R51-C1 pass | ANCHORS total=20 dup=0 missing=0, but `PREDICATE R51-C1 fail` | **1** | **FINDING (non-green, pre-existing at base — see below)** |
| 6 | `python3 plans/defect_ledger.py --lane <clone>` | record counts | `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass` (open=0; every row status=closed observed=pass agree=yes) | 0 | PASS |
| 7 | `python3 plans/round54_c2_entrytruth.py --selftest` | selftest green | `[selftest] 7/7 PASS` | 0 | PASS |

Outputs saved beside this report: `grader.txt`, `grader-selftest.txt`,
`r52-c2-registry-selftest.txt`, `r55-c2-controls-selftest.txt`, `r51-surfaces.txt`,
`defect-ledger.txt`, `r54-c2-entrytruth-selftest.txt`, plus comparison
`r51-surfaces-base.txt`.

## Finding 1 (only non-green): round51_surfaces R51-C1 predicate fail — pre-existing at base

Full observed output (rev 80afa61314fa):

```
REV 80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb
MANIFEST plans/round51-surfaces.json entries=20 sections=2
ANCHORS total=20 dup=0 missing=0
ROWS section="## Surfaces" rows=10 entries=10 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=20 present=13 absent=7 errors=0
DRIFT 0
STALE 1
  DETAIL STALE SF20 probe=absent state=present (http://127.0.0.1:1234/health -> <urlopen error [Errno 111] Connection refused>)
UNVERDICTED 0
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=193
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT 1
```

Base comparison: the same command at base rev 798f5e9e (clean worktree,
`r51-surfaces-base.txt`) exits 1 with `PREDICATE R51-C1 fail`, `observed_present=13`,
and a byte-identical finding body (same STALE SF20, same NUMBER-DRIFT SF14). Conclusion:
the gate is non-green **before any round-55 bytes**; round-55's landing commit did not
harm it. This is the frozen-before L0 condition `kengaku | round-51` listed as still open
in the round-55 claims file, consistent with that routing `[INFERENCE: the two DETAIL
lines match the unanswered round-51 L0]` — the attribution is my read, the byte equality
is measured.

The two DETAIL lines, exactly:
- `STALE SF20` — probe `http://127.0.0.1:1234/health` refused: it needs a live local
  service that is not running in this environment (environmental, not a repo defect).
- `NUMBER-DRIFT SF14` — the manifest row claims 171 SOURCES rows, the probe counts 193.
  [INFERENCE] the row was written when SOURCES.md had 171 rows; later rounds added rows
  without re-baselining SF14. Not a round-55 change (identical at base).

## Defects found / dead ends

- No defects in round-55 bytes observed by these gates (6/7 green; the 7th is green at
  neither base nor tip).
- Dead end: none. All seven commands ran first try; no retries, no backoff issues.
- No sibling-file defects encountered, so nothing to report upstream.

## Housekeeping

- Scratch `/fast/scratch/hyaku/kengaku-r55/E10NoharmRuns/` deleted after receipts were
  copied out (worktree removed first, then `rm -rf`).
- Installs: none.

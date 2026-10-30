# R11R52Carry — report (kengaku round 55, w1)

**Seat item:** reconstruct the carried r52 repair's two defects — the refused E3
patch's order-check regression and the masked K7 control — as scratch-only
evidence with a runnable recipe. Production counters untouched; no lane writes.

## What I ran

All work under scratch `/fast/scratch/hyaku/kengaku-r55/R11R52Carry/`
(deleted after receipts were copied out). Lane: `git clone --shared` of
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` → `lane/`, verified
`git rev-parse --show-toplevel` = the scratch clone, HEAD `80afa61314fa…` (the
round-55 freeze commit; tree clean), parent = declared base `798f5e9e…`.
Counters: `counters/old_round52_c2_registry.py` (copy of production
`plans/round52_c2_registry.py`, sha256 `9e6f41a4…`),
`counters/patched_round52_c2_registry.py` (copy of
`.ufo/waves/round-54/w1/E3R52RegistryFix/round52_c2_registry.py`, sha256
`83667e8f…`), `counters/mutant_k7_…` (patched + the single controls.json K7
replacement). `PYTHONDONTWRITEBYTECODE=1` on every run.

| Step | Command (cwd = scratch) | Exit | Receipt |
|---|---|---|---|
| A1 old on raw clone | `python3 counters/old_… --lane lane` | 1 | `receipts/A1-old-lane.txt` |
| A1 patched on raw clone | `python3 counters/patched_… --lane lane` | 1 | `receipts/A1-patched-lane.txt` |
| A2 old on registry-closed copy | `python3 counters/old_… --lane lane-closed` | 0 (pass) | `receipts/A2-old-closed.txt` |
| A2 patched on registry-closed copy | `python3 counters/patched_… --lane lane-closed` | 1 (`SELFTEST-UNBACKED \`order-check\``) | `receipts/A2-patched-closed.txt` |
| A3 row isolation | in-process `selftest_unbacked` over all 81 SKILL.md rows, old vs patched | 0 | `receipts/A3-row-isolation.txt` (exactly 1 flip: `` `order-check` `` False→True) |
| A4 old on mixed-negation fixture | `python3 counters/old_… --lane fixtures/negation` | 0 (masking defect reproduced) | `receipts/A4-old-negation.txt` |
| A4 patched on same fixture | `python3 counters/patched_… --lane fixtures/negation` | 1 (`SELFTEST-UNBACKED \`t\``) | `receipts/A4-patched-negation.txt` |
| B1 patched selftest | `python3 counters/patched_… --lane lane --selftest` | 0 (`cases=6 failures=0`; K7 step prints `MISSING 2` + `ENTRY-MISSING 1`) | `receipts/B1-patched-selftest.txt` |
| B2 mutant selftest | `python3 counters/mutant_k7_… --lane lane --selftest` | 0 (`cases=6 failures=0`, incl. `SELFTEST ok K7-entry-missing`) | `receipts/B2-mutant-selftest.txt` |
| B3 confound decomposition | in-process `collect`/`verdict`, both K7 fixture shapes × both modules | 0 | `receipts/B3-k7-confound.txt` |
| B4 old/patched/mutant on corrected K7 fixture | `python3 counters/{old,patched,mutant_k7}_… --lane fixtures/k7-corrected` | 1 / 1 / 0 | `receipts/B4-*.txt` |

Supporting source checks (read-only, in the lane): `sed -n '140,150p'
plans/order_check.py` (accepts `--lane/--claims/--receipt`, required) and
`grep -n add_argument plans/round40_c1_verify.py` (`:443-450`, no
`--receipt`/`--claims`) — the ground truth behind the false red.

## Findings (the two carried defects, both reproduced)

1. **Order-check regression (R4 P1).** The patch touches exactly one
   production check: `selftest_unbacked()` (SELFTEST-UNBACKED leg,
   `plans/round52_c2_registry.py:68-83`). The input that flips is the committed
   `order-check` row's self-test cell (`SKILL.md:590`, col 5): it negates one
   flag locally (`no --selftest`) and its surviving flags `--receipt`/`--claims`
   belong to `plans/order_check.py` (`:143-145`), but the cell's sole `.py`
   mention is the external falsifier `plans/round40_c1_verify.py`, which does
   not accept them. Old logic: blanket negation exempts the cell (green).
   Patched: strips only the negated flag, misattributes the survivors to
   round40_c1_verify.py → false `SELFTEST-UNBACKED \`order-check\``. On a
   registry-closed clone the same tree goes pass→fail solely because of the
   patch (A2). A4 confirms the patch's intended masking-fix is real (old hides
   an unbacked `--check`; patched catches it) — the fix is right for the narrow
   case and wrong for the landed cell.
2. **Masked K7 control (R4 P2).** The implemented K7 selftest overwrites the
   fixture registry with the ghost row only, while `grader.py`/`plans/tool_a.py`
   remain advertised → `MISSING 2` forces the failing verdict independently, so
   the `entry_missing` verdict term is never exercised. The controls.json
   mutation (drop `entry_missing` from the `ok` expression at production
   `:133`) still yields `SELFTEST cases=6 failures=0`, exit 0, including
   `SELFTEST ok K7-entry-missing` (B2). The fixture made invisible is the one
   `fixture-k7.md` itself specifies: the ghost row **inserted into the complete
   table**. With that corrected fixture the same mutation flips the verdict to
   pass (B3/B4) — i.e. the corrected control kills it, the shipped one does
   not.

## Files written (all under the seat output dir)

- `.ufo/waves/round-55/w1/R11R52Carry/recipe.md` — mechanism, exact inputs,
  runnable reproduction of A1–B4, fix directions.
- `.ufo/waves/round-55/w1/R11R52Carry/receipts/` — 13 receipt files listed above.
- `.ufo/waves/round-55/w1/R11R52Carry/report.md` — this report.
- `.ufo/waves/round-55/w1/R11R52Carry.md` — scoped seat findings.

## Dead ends / notes

- The round-55 freeze tip is already red on R52-C2 for the unrelated r54
  surface (`MISSING 2`, the R55-C1 regression), so the cleanest red-before
  demonstration required closing the registry in a scratch copy (A2); the raw
  tip contrast (A1) shows the patched counter's only delta is the order-check
  finding. This matches R4's r54-era receipts, where the lane was still green
  (77/77).
- Seat text pointed at `.ufo/waves/round-52/w2/` for "R4's patch
  demonstration"; the actual R4 refusal review is `.ufo/waves/round-54/w1/
  R4R52Fix.md` (+ `R4R52Fix/review.md`, `evidence.json`). Round-52 lineage is
  real but earlier: w1 `C2RevCounterRule` (B3 masking) and w2 `W2RevRowsB`
  (`a3-fix-probe.py` span-scoped attribution prototype, with the explicit
  warning that naive stripping flags the landed order-check cell).
- `xd://lsp` was not needed (no code-navigation claims made); all behavior
  claims are backed by executed commands.
- No tools installed. No git/jj mutations anywhere (clone + hardlink copy only;
  the one working-tree edit was fixture rows inside the scratch copy
  `lane-closed`). Receipts copied out before scratch deletion; scratch removed
  via `rm -rf` after this report.

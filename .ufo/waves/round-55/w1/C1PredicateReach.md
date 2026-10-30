# C1PredicateReach — scoped findings (R55-C1 predicate-reach attack)

Counter: `plans/round52_c2_registry.py` at freeze `80afa613…`, run against scratch attack trees
(base: `MISSING 2`, exit 1). Full commands, outputs and receipts:
`.ufo/waves/round-55/w1/C1PredicateReach/report.md` + `receipts/`.

**Answer: yes — the frozen after-predicate text can be printed without the repair being real,**
because the counter is advertised-set-relative. Three of the four assigned bypasses pass it:

| # | bypass | result | caught? |
|---|---|---|---|
| A1 | de-advertise both r54 counters (their only ad site is `SCORECARD.md:2346-2347`, not LOG.md) | `MISSING 0`, pass, exit 0, zero rows added | **No** |
| A2 | registry cell padded with ASCII spaces | `INCOMPLETE 1`, fail | Yes |
| A2′ | registry cell = single U+200B ZERO WIDTH SPACE (visually empty, survives `.strip()`, truthy) | `INCOMPLETE 0`, pass, exit 0 | **No** |
| A3 | twin row: unique name, same entry script, absurd verdict map | `DUPLICATE 0`, pass, exit 0 | **No**, but… |
| A3′ | twin rows + withheld row for the other advertised script | `MISSING 1`, fail | Yes — duplicates cannot hide a missing script |
| A4 | rename both scripts hyphenated (dodges the `[A-Za-z0-9_]` class) and re-advertise; or delete both and leave the ads | pass, exit 0 both ways | **No** |
| A4′ | registry entry cell without the `python3 ` prefix | `MISSING 2`, fail | Yes |

**But the claim survives.** (1) No bypass can carry a *false verdict-map cell*: frozen leg 2
executes every round-55-added row's named self-test and matches the cell — a padded, empty, or
absurd cell declares no true verdict and fails the match; the kill rule then holds operability
at 8. (2) A1/A4 contradict the r55 freeze's pinned landing content ("Registry rows added in
round 55: round54-c1, round54-c2, round55-c2, round55-c2-controls, round55-c3"; the advertised
set "includes every script this round's landing adds") — a landing that de-advertised or renamed
would need a dated amendment row, cannot pass silently, and its in-place SCORECARD deletions
are visible in the append-only diff measured by outside closure. Note the r54 spot-check
itself offered the "stop advertising" branch, so the counter passing there is by design; the
r52 universe rule defines the obligation as conditional on advertising.

**Classification for the canonical judge:**
- A2′ (ZWSP) — *fixable defect*, amendment candidate (counter frozen this round): strip
  `[\u200B-\u200D\uFEFF]` in `parse_rows` before the `all()` check. One line.
- A1/A4 — *tradeoff*: inherent to an advertised-set-relative gate; compensated by the freeze
  text + L1 integration diff + outside closure. No counter change required this round.
- A3 — *tradeoff*: DUPLICATE is name-only by frozen Amendment A6; verdict-map truth is leg 2's
  assignment. Optional future duplicate-entry leg.

**Two integration hazards for the L1 (evidenced, not counter defects):**
1. `round54_c1_anchor.py` has **no `--selftest` flag** — the self-test is the `selftest`
   subcommand. A `round54-c1` row whose self-test cell claims `--selftest` (the r54 claims'
   loose "8/8" prose) fires `SELFTEST-UNBACKED` at the after-run (demonstrated). Truthful cell:
   `` `python3 plans/round54_c1_anchor.py selftest` ``.
2. That self-test is **not hermetic to a clean clone**: it imports `opentimestamps`; the r54 OTS
   venv is gone (scratch reclaimed); system python3 → `ModuleNotFoundError` (nonzero). With
   `opentimestamps-client 0.8.0` it is `[selftest] 8/8 PASS`, exit 0 (receipt
   `c1-selftest-venv.txt`). Leg 2's clean-clone execution must provide the dependency or the
   cell must name an interpreter that has it. `round54_c2_entrytruth.py --selftest` is clean
   under system python3: 7/7 PASS, exit 0.

No lane files other than this report path were written; scratch deleted.

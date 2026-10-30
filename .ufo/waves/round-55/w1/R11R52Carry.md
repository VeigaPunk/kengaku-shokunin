# R11R52Carry — scoped findings (round 55, w1)

**Item:** carried r52 repair reconstruction — the refused E3 patch's two
defects, reproduced on scratch copies with a runnable recipe
(`w1/R11R52Carry/recipe.md`, receipts under `w1/R11R52Carry/receipts/`).
Production `plans/round52_c2_registry.py` untouched; no lane writes.

## Defect 1 — order-check regression (no-harm failure; blocks integration)

- **Check touched:** `selftest_unbacked()` — the SELFTEST-UNBACKED leg of
  `plans/round52_c2_registry.py` (`:68-83`). Patch = E3
  `w1/E3R52RegistryFix/delta.diff`: remove the blanket `no … --flag` cell
  exemption; subtract only the locally negated flag.
- **Input that flips:** the committed `order-check` registry row's self-test
  cell (`SKILL.md:590`, col 5). It locally negates `--selftest`; the surviving
  `--receipt`/`--claims` are real controls of `plans/order_check.py`
  (`:143-145` requires both) but the cell's only `.py` mention is the external
  falsifier `plans/round40_c1_verify.py` (`:443-450` does not accept them).
  Old counter: cell exempted, row green. Patched: survivors misattributed to
  the falsifier → `SELFTEST-UNBACKED \`order-check\``, predicate fail.
- **Observed:** on a registry-closed scratch clone, old exits 0
  (`PREDICATE R52-C2 pass`) and patched exits 1 with exactly that finding
  (`receipts/A2-*.txt`); row-level isolation shows exactly 1 of 81 rows flips
  (`receipts/A3-row-isolation.txt`). The patch's narrow target defect is also
  confirmed real and caught (`receipts/A4-*.txt`), so the fix needs the
  span-scoped attribution rule from r52-w2 `W2RevRowsB/a3-fix-probe.py`, not
  naive flag stripping.

## Defect 2 — masked K7 control (the added selftest does not test its claim)

- **Mutation (controls.json):** drop `entry_missing` from the verdict `ok`
  expression (`plans/round52_c2_registry.py:133` region, shared by both
  versions).
- **Fixture made invisible:** `fixture-k7.md` specifies *inserting* the
  `ghost-tool` row into the **complete** registry table; the implemented
  selftest *overwrites* SKILL.md with the ghost row only while the fixture lane
  still advertises `grader.py`/`plans/tool_a.py` → `MISSING 2` masks
  ENTRY-MISSING.
- **Observed:** patched `--selftest` → `cases=6 failures=0` exit 0; the same
  with the mutation applied → still `cases=6 failures=0` exit 0, including
  `SELFTEST ok K7-entry-missing` (`receipts/B1/B2`). With the corrected
  complete-table fixture the same mutation flips the K7 verdict to pass
  (patched fail exit 1 vs mutant pass exit 0; `receipts/B3/B4`) — the corrected
  control kills it, the shipped one cannot.

## For the L1 / future fix seat

Recipe `w1/R11R52Carry/recipe.md` §"Fix directions" gives both repairs with
their red-before evidence already recorded: (1) span-scoped flag attribution
inside `selftest_unbacked`; (2) K7 fixture = insert ghost row into the complete
table. Neither changes any frozen predicate; production counters stay as-is
this round per the claims file.

**Verification gaps:** none for the two reproductions (all commands executed,
exits captured). Not covered: re-deriving E3's full selftest receipts beyond
the K7/span cases; the M4R52FixMutants battery was assigned in r54 but no
published deliverable was found under `round-54/w1/M*` (consistent with
`SC5SpotcheckDebt` noting the gap at r54 mid-wave).

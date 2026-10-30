# SP2RowCells — scoped findings (r55 w1, cell-verbosity pass)

**Deliverable**: `.ufo/waves/round-55/w1/SP2RowCells/trims.diff` — 7 proposed prose trims across 4 of the 5 new registry rows (E1's landed lines 642–646); `round55-c3` intentionally gets no hunk. Net −357 chars. Lane file untouched; L1 applies or rejects.

**Trims, one line each** (full rationale in `SP2RowCells/report.md`):
1. round54-c1 entry: drop "; the bare-host entry measurement is red — see the verdict map" (verdict `1` carries the measured fact; reverse-direction dedup).
2. round54-c1 scope: drop ": anchor assets land only via `stamp`/`upgrade`" (entry cell already states it).
3. round54-c2 entry: drop "— the bare ledger argv exits 2 `SETUP …`, measured 2026-10-30" (verbatim in verdict `2`; date relocated additively into verdict `2`).
4. round55-c2 entry: same as 3 for its row.
5–6. The two verdict-`2` date relocations accompanying 3 and 4 (purely additive, keeps protected cells truthful).
7. round55-c2-controls scope: drop "(the r54 counter passes them)" and "(the r55 binding counter attributes the defect)" (verdict `0`'s measured lines restate both).

**Safety, exercised**: first backtick spans byte-identical in all five rows (the span the R55-C2 L1 leg token-equalizes against the ledger); 8 non-empty cells per trimmed row; `round52_c2_registry.py` output byte-identical on twin HEAD clones differing only in orig vs trimmed SKILL.md; verdict-map/self-test cells otherwise untouched; pinned sha256 cells spot-checked 5/5 against the scripts.

**Defects for other owners**: round54-c1 verdict `1` "`failed=<n>0`" notation ambiguous (R6 truth audit); rows omit house-style "(lane root; …)" prefix (omission, not verbosity — out of a trims-only mandate).

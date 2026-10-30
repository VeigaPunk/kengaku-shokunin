# C5KillRuleScope — scoped findings (R55-C2 kill-rule wording attack)

Frozen rule probed (`plans/round-55-claims.md`, R55-C2 kill rule): calibration held at 9
if any attack seat constructs a runnable fixture with ALL static legs clean that passes
`plans/round55_c2_entryargv.py` at the measured-after revision while the row's
registry-declared entry truly exits otherwise; hand-rewrites of the reviewed SKILL
registry cell are excluded as documentation attacks ("already carried by the r52 row-audit
legs and reviewer cell audits").

Fixtures ran in the seat scratch against a shared clone at `80afa613` with the in-flight
counter copied verbatim; receipts in `C5KillRuleScope/receipts/`, full analysis in
`C5KillRuleScope/analysis.md`.

## Probe 1 — exclusion laundering lane: honest LEDGER, lying REGISTRY cell — UNSOUND

Fixture: entry cell honest, verdict-map cell rewritten `` `0` ok · `1` ok `` (green
declared for a red entry), ledger honest red@1, entry truly exits 1. Result: C2 counter
`PREDICATE R55-C2 pass` (exit 0); r52 counter `PREDICATE R52-C2 pass` (exit 0). No leg
parses the verdict-map cell (only `cells[2]` entry is read). The named carrier does not
exist as described: the r52 legs (MISSING/INCOMPLETE/ENTRY-MISSING/SELFTEST-UNBACKED/
DUPLICATE) are static. Real catchers: R55-C1 frozen leg 2 + C1 kill rule, scoped to the 5
round-55-added rows only; all ~75 pre-existing rows rest on human reviewer cell audits.
Correction path: dated amendment row restating carriers/scope (+ optional full-registry
leg-2 spot). Finding only — no rule edit made.

## Probe 2 — "ALL static legs clean" enumeration + opt-out question — SOUND

Code enumerates 10 fields + 2 preconditions: headings==1, no ledger_err, missing=0,
extra=0, argv_defect=0 (r54 entry_mode_ok + r55 L1 binding), wrapper_defect=0 (L2),
abbrev_defect=0 (L3), bad_decl=0, duplicate_names=0, bad_table_lines=0, n_reg>0. Frozen
text lists 8 (omits bad_table_lines; code stricter — safe direction). Rows with
bad_decl/argv_defect (r54) or +wrapper/abbrev (r55) are skipped from execution
(`round55_c2_entryargv.py:237-241`) — demonstrated: executed=0/1 vs registry=1/2 — but the
opt-out is loud: it dirties a named static leg, fails the counter, and breaks
`executed == n_reg`. No silent opt-out channel; a defect-carrying fixture cannot fire the
kill rule.

## Probe 3 — closure decidability — SOUND firing rule, UNSOUND literal "one command"

Sandbox-gaming fixture (entry exits 0 under the r54 hermetic env, 1 in a plain
environment): closure passes it (`PREDICATE R55-C2 pass`) while the registry-declared
entry truly exits 1 — the kill rule fires on it as worded (soundness break, not a
documentation rewrite; the exclusion does not shield environment-gaming). But the closure
alone cannot establish "truly exits otherwise": minimal decision procedure = closure + one
independent non-hermetic execution of the registry-declared entry (two commands; the
frozen before-receipts already follow this pattern). The universal reading is not
one-command decidable; the closure is a per-fixture checker.

## Impacted axes / hand-off

- Calibration (C2) primary; operability (C1) via the probe-1 scope coupling (C1 leg 2 is
  the only mechanical verdict-map checker).
- Suggested checks for the L1/integration: (1) dated amendment for the probe-1
  parenthetical; (2) receipts here re-runnable via `probe_driver.py` logic (fixtures
  rebuild from scratch; receipts byte-reproducible given the same counter revision).

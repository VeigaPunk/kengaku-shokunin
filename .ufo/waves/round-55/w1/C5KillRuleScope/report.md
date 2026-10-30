# C5KillRuleScope — seat report (kengaku r55 w1)

Seat item: attack the R55-C2 kill-rule wording for holes (frozen text,
`plans/round-55-claims.md` @ `80afa613`). Deliverables: `analysis.md` (3 probes, verdicts)
+ `receipts/`. Scoped findings also at `../C5KillRuleScope.md`.

## What I ran (all under `/fast/scratch/hyaku/kengaku-r55/C5KillRuleScope/`, deleted on exit)

| Command | Exit | Note |
|---|---|---|
| `git clone --shared <lane> lane` | 0 | HEAD `80afa613` (freeze), tree clean |
| `python3 lane/plans/round55_c2_entryargv.py --selftest --work work/selftest` | 0 | 4/4 PASS (instrument sanity before probing) |
| `python3 probe_driver.py` (builds 4 fixtures, runs counter + r52 counter on each) | 0 | per-run counter exits below |

Per-fixture observed exits:
- p1-laundering: r55 counter **0** (`PREDICATE R55-C2 pass`), r52 counter **0**
  (`PREDICATE R52-C2 pass`), true entry exit **1** — probe-1 lane demonstrated.
- p2a-baddecl-optout: r55 counter **1** (`bad_decl=1`, `RUN executed=0` vs `registry=1`).
- p2b-argvdefect-optout: r55 counter **1** (`argv_defect=1`, `RUN executed=1` vs `registry=2`).
- p3-sandbox-gaming: r55 counter **0** (`PREDICATE R55-C2 pass`), true entry exit **1** —
  kill-rule firing fixture; not one-command decidable.

Reads (no mutation): `plans/round-55-claims.md` (frozen claims), `plans/round55_c2_entryargv.py`,
`plans/round54_c2_entrytruth.py`, `plans/round52_c2_registry.py`, `plans/round55_c2_controls.py`,
`SKILL.md` registry block (`:560+`), `plans/round54-entrytruth.json` (78 rows, schema
`r54-entrytruth-v1`), `plans/round-52-claims.md` (C2 kill-rule origin).

## Files written

Lane (this wave dir):
- `.ufo/waves/round-55/w1/C5KillRuleScope/analysis.md` — 3 probes with per-probe verdicts.
- `.ufo/waves/round-55/w1/C5KillRuleScope/report.md` — this file.
- `.ufo/waves/round-55/w1/C5KillRuleScope/receipts/` — 7 receipt files
  (`p1-laundering.r55.txt`, `p1-laundering.r52.txt`, `p1.true-exit.txt`,
  `p2a-baddecl-optout.r55.txt`, `p2b-argvdefect-optout.r55.txt`,
  `p3-sandbox-gaming.r55.txt`, `p3.true-exit.txt`).
- `.ufo/waves/round-55/w1/C5KillRuleScope.md` — scoped findings summary (the seat's
  `Report:` trailer path).

Scratch (deleted): `probe_driver.py`, `lane/` (shared clone), `probes/` (4 fixture repos),
`work/`. The in-flight `plans/round55_c2_entryargv.py` was copied **verbatim** into the
scratch clone as fixture input (it is uncommitted in the lane working tree; owned by
sibling build seats — never edited).

## Defects found (findings; no rule edits — the freeze is not mine to touch)

1. **Probe 1 — UNSOUND (scope/wording).** The exclusion's laundering lane exists: honest
   LEDGER + hand-rewritten registry verdict-map cell (declared green for a red entry)
   passes both the C2 counter and the r52 counter (receipts). The parenthetical's named
   carrier "r52 row-audit legs" is static (MISSING/INCOMPLETE/ENTRY-MISSING/
   SELFTEST-UNBACKED/DUPLICATE) and demonstrably does not carry verdict-map truth; the
   only mechanical checker is R55-C1's leg 2 + kill rule, scoped to round-55-added rows
   (5 rows), leaving ~75 pre-existing rows covered by human reviewer cell audits only.
   Smallest correction: dated amendment row restating the carriers/scope (+ optional L1
   leg-2 extension to the full registry).
2. **Probe 2 — SOUND.** "ALL static legs clean" enumerates 10 fields + 2 preconditions in
   code (frozen text lists 8, omitting `bad_table_lines` — code stricter, safe direction).
   A row CAN opt out of execution by carrying a defect (demonstrated), but only loudly:
   the defect dirties a named static leg, fails the counter, and breaks `executed == n_reg`.
3. **Probe 3 — SOUND as firing rule; UNSOUND literal wording.** A sandbox-gaming entry
   passes the closure while truly exiting otherwise — the kill rule fires on it (not a
   documentation rewrite; exclusion does not shield it). But "truly exits otherwise" is
   not decidable by the closure alone: minimal procedure = closure + one independent
   non-hermetic entry run (the frozen before-receipts already use this two-part pattern).

## Dead ends / adaptations

- The shared clone at `80afa613` does not contain `plans/round55_c2_entryargv.py` — it is
  in-flight and uncommitted in the lane working tree (sibling build seats own it).
  Adapted by copying it verbatim into my scratch clone; selftest 4/4 before probing.
- Fixture git guard: pre-init `git rev-parse --show-toplevel` succeeds inside an existing
  work tree and fails (empty stdout, rc≠0) in a fresh dir — guard split into
  not-inside-a-repo (pre-init) vs equals-root (post-init).
- No installs/upgrades were needed (none performed). No subagents dispatched. No
  mutating git/jj command run anywhere; lane working tree untouched except the wave-dir
  files named above.

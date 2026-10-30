# C6Separability — scoped findings (trailer)

Verdict: **separable under the lane's operative (r52) reading — verification-independence — and
NOT separable under a strict pass-in-isolation reading for C1 and C2 (C3 stands alone).**
Full analysis: `.ufo/waves/round-55/w1/C6Separability/analysis.md`.

## Ruling on the prompt's three checks

1. **Is C2's `round52-c2` dependence non-separable?** No — under the operative reading.
   `AXES.md` freezes "each verifiable without the others having landed"; the lane's canonical
   interpretation (r52 claims §Causal separability) is *predicate-input disjointness + clean
   attribution*, not pass-in-isolation. C2's counter runs standalone and reports the C1
   dependence as a truthful `LAUNDERED round52-c2` verdict; it cannot launder a broken state
   into a pass. The dependence is declared by the freeze ("R55-C1's repair restores its true
   exit 0"), so it is a premise to name, not a defect.
2. **C3 shares no instrument with C1/C2: verified.** `round55_c3_chess_probe.py` imports only
   stdlib + bwrap, never touches SKILL/LOG/ledger/C1-C2 counters; its oracle is the pinned
   in-repo grader capture. One-way edge only: C1 registers/advertises the probe script and C2
   re-executes its ledger entry.
3. **Admission-rule harm vector: partial landings.** The three claims are universal predicates
   over joint state; a lone landing can *create* an axis harm — see defect list.

## Causal coupling map (for the L1's atomic-integration decision)

- C2 → C1: `round52-c2` observed exit needs E1's rows (`LAUNDERED` if absent); `extra=5` if
  E4's ledger rows land without E1's registry rows.
- C1 → C2: `ENTRY-MISSING` on `plans/round55_c2_entryargv.py` (E2's, untracked) via E1's
  `round55-c2` row.
- C1 → C3: `ENTRY-MISSING` on `plans/round55_c3_chess_probe.py` (E5's, untracked).
- C1/C2 → C3 advertisements: C3's README/LOG lines + C2's registry cell enlarge the advertised
  set each C1 row must cover.
- C3: none — passes alone.

## Defects (report-only; owned by L1 / E1 / E4)

- **D1 — C2 after-predicate unreachable as scoped.** `--dry` static legs at HEAD:
  `argv_defect=17 wrapper_defect=1` (receipt `dry-static-legs-wip.txt`). The 17 are pre-existing
  registry cells documenting generic argv vs the ledger's concrete argv (L1 token-equality);
  the 1 is `tb2-grader-probe`'s `uv` argv. No seat is scoped to reconcile them.
- **D2 — `tb2-grader-probe` has no truthful non-wrapper argv.** `uv`-wrapped (L2 defect) and no
  `python3` form exists (`import Bio` fails hermetically). Dropping the row does not help — the
  script stays `ADVERTISED`, so C1 then reports `MISSING`. Needs an L1 decision: re-declare
  `python3 …` red (degrades a working probe) or amend L2 by dated amendment-row.
- **D3 — `round54_c1_anchor.py` self-test trap.** Self-test is subcommand `selftest` (`:568`),
  no `--selftest` flag; an E1 cell claiming `--selftest` trips `SELFTEST-UNBACKED` → C1 fails +
  false cell.
- **D4 — harm requires atomic integration.** A lone C3/C2 landing recreates the advertised-but-
  unregistered r54 regression (operability); lone ledger rows create a registry↔ledger
  divergence (calibration). Land all claim artifacts in one measured-after tip or revert the
  unmatched halves.

Axes: operability (D3/D4 + C1 couplings), calibration (D1/D2 + C2 binding).

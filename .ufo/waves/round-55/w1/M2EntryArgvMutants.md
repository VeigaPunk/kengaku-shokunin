# M2EntryArgvMutants — scoped findings (round-55 w1, mutation probe of R55-C2 instrument)

Target: `plans/round55_c2_entryargv.py` NEW legs, single-leg silence mutants on scratch copies
at base `80afa613` bytes (pristine sha256 `2bf9e66c…6ea74`, unchanged after probe). Detector:
one-row git fixtures × `evaluate(..., jobs=1, timeout=60)`; pristine `--selftest` 4/4 PASS;
truthful baseline passes under all variants; full evidence
`.ufo/waves/round-55/w1/M2EntryArgvMutants/{mutants.md,report.md,receipts/}`.

1. **M1 (L1 removed) KILLED**, **M2 (L2 removed) KILLED**, **M3 (L3 removed) KILLED** — each via
   a leg-isolating fixture the frozen controls don't cover (frozen cases are over-determined by
   2+ legs, so single-leg mutants on them don't flip): F1 positional-decoy argv divergence
   declared truthfully red (only L1 fires), F2 token-equal inline `-cprint(…)` registry entry
   (only L2's inline-`-c` clause fires), F3 registry cell itself declaring `--selft` with a
   truthful green ledger (only L3 fires). Each flip is a clean `PREDICATE R55-C2 fail` →
   `pass` rc 1 → 0. L1, L2(-inline-c), L3 are load-bearing.
2. **M4 (L4 registry-cell ground truth → ledger-argv execution, r54 behavior) SURVIVED as
   vacuous at single-leg granularity** — outputs byte-identical to pristine on all 7 fixtures.
   Structural cause: `evaluate` never executes L1-flagged rows, and L1-clean rows have
   ledger argv ≡ registry argv. **Laundering IS re-introduced by the supplementary M1+M4
   combined probe** (the exact r54 behavior) on F4c (ledger `… --go` declared green vs registry
   bare entry exiting 1): `PREDICATE R55-C2 pass`, exit 0, true entry fails. Defense-in-depth
   is real and ordered: L1 catches argv tampering statically; L4 catches it at runtime when L1
   is gone (`LAUNDERED fixture-gate declared green, entry exit=1` under M1 on F4c); only both
   removed → laundering. The R55-C2 soundness claim is untouched: with all static legs clean,
   ledger argv ≡ registry argv and L4 executes exactly the registry-declared entry, so the
   frozen kill-rule attack remains impossible. Finding is redundancy documentation, not a
   contract defect.
3. **L2's `argv[0]`-interpreter clause is never a sole detector while L1 is intact** (derived):
   any wrapper `argv[0]` breaks token-identity with the registry span and co-fires L1; only the
   inline `-c` clause carries independent weight.
4. Corroboration of the claim surface: fixtures F2/F3/F4c all pass the unchanged r54 counter's
   static legs (`entry_mode_ok` permits `uv` argv[0], non-exact flags and `-cprint(…)` since
   SHELLS holds only bare `-c`) — i.e., the r54 routes generalize beyond the two frozen
   laundering cases, strengthening (not attacking) R55-C2's before-state.

No seat-scoped defects found in the instrument's verdicts (no false pass on honest input, no
inconclusive baseline). Lane files untouched; scratch deleted after receipts were copied out.

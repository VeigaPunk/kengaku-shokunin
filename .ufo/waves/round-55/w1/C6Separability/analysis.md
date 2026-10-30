# C6Separability — causal-separability audit of R55-C1 / R55-C2 / R55-C3

Seat: `C6Separability` (critic). Read-only analysis. Base `798f5e9e`, freeze `80afa613`.
Measured facts are quoted from the committed tree plus a **read-only** `--dry` static-leg run
(receipt: `dry-static-legs-wip.txt`, this dir; the r54/r55 static legs read only SKILL.md +
`plans/round54-entrytruth.json`, both clean at HEAD, so the WIP tree does not perturb them).

## 1. The exact rule and the two readings

`AXES.md` §Working the axes, verbatim:

> "Claims must be **causally separable** — each verifiable without the others having landed —
> and name **distinct axes** … A round is admitted only if every claim verifies **and no axis
> is harmed** — a trade anywhere is not an improvement: report every verdict and let the
> operator rule."

"Verifiable" admits two readings, and the choice decides the whole verdict:

- **(V) verification-independence** — each claim's counter is independently *runnable* on any
  tree and attributes its own verdict. A dependence shows up as a correctly-attributed `fail`,
  never as an uncheckable or a cross-contaminated pass.
- **(P) pass-in-isolation** — each claim could pass even if no sibling had landed.

The lane's operative precedent is (V). Round 52's own frozen defense (`plans/round-52-claims.md`
§Causal separability) argues **predicate-input disjointness**, not isolated pass:

> "C1's predicate reads the grader captures, the classifications, the confirmation receipts and
> the prior-art file; it never reads `SKILL.md`'s registry. C2's predicate reads the
> self-assessment files and the registry table; it never reads the grader captures. Each
> verifies without the other having landed."

(Round 51's claims file says "either can land alone and be scored alone" — a (P)-shaped gloss —
but that described r51's file-disjoint facts; it was not posed as the test and no round was ever
ruled on it. The canonical, reasoned statement is r52's input-disjointness clause.)

## 2. The declared coupling (question 1) — C2 on C1

Confirmed, and **declared by the freeze itself**: R55-C2's ledger-truth clause (b) reads
"`round52-c2` stays declared green — R55-C1's repair restores its true exit 0".

Mechanism, measured:
- Ledger row `round52-c2` (committed `plans/round54-entrytruth.json`) declares
  `entry_argv = ["python3","plans/round52_c2_registry.py","--lane","."]`, `entry_state=green`,
  `entry_exit=0`.
- At base that entry truly exits **1** (`MISSING 2`: `round54_c1_anchor.py`,
  `round54_c2_entrytruth.py` advertised but unregistered — the r54 regression).
- The new counter's L4 re-executes each row via the **registry cell argv**; if C1's five rows
  have not landed, the observed exit is 1 vs declared green → `LAUNDERED round52-c2` →
  `PREDICATE R55-C2 fail`.

**Ruling (question 1):** under (V) this is **separable and safe**. C2's counter runs standalone
and reports the C1-dependence as a truthful `LAUNDERED` verdict; it can never pass on a tree
where `round52-c2` is truly broken. The pass-dependence is one-directional (C2→C1), declared
in the freeze, and costs attribution *nothing* — it cannot launder. Under a strict (P) reading
it would fail, but (P) is not the lane's test and the freeze has already chosen (V). The
dependence must be **stated as a premise in the report**, not papered over.

### The fuller coupling map (stronger than the prompt's one row)

C2's `round52-c2` row is not the only C1-dependence. The causal web at the measured-after tip:

| Edge | Mechanism | Verdict if the tail lands alone |
|---|---|---|
| C2 → C1 | `round52-c2` row: observed exit needs C1's rows (above). | C2 `LAUNDERED` → fail. |
| C2 → C1 | `static` legs: `missing`/`extra` require registry set == ledger set. E4 adds 5 ledger rows; without E1's 5 registry rows `extra=5` → `static_ok` false. | C2 static fail. |
| C1 → C2 | C1's `ENTRY-MISSING` leg: E1's `round55-c2` row registers `plans/round55_c2_entryargv.py`. If that file (E2's, still **untracked**) does not land, `ENTRY-MISSING 1`. | C1 fail. |
| C1 → C3 | E1's `round55-c3` row registers `plans/round55_c3_chess_probe.py` (also **untracked**, E5's). If it does not land, `ENTRY-MISSING 1`. | C1 fail. |
| C1 → (C2,C3) advertisements | the r52 gate's advertised set = `python3 plans/*.py` over SCORECARD/SKILL/LOG/README, filtered to *existing* files. C3's README/LOG and C2's registry/LOG advertisements only enter the set if the scripts exist — and each must then be registered. E1's 5 rows cover exactly this set. | covered only if E1's full set lands. |
| C3 → (none) | C3's predicate reads only its own capture/probe/receipt/entry/index rows. | passes alone. |

So under (V) all three are separable (each verdict self-attributing); under (P) only C3 is.
The three claims are mutually dependent **for pass**, disjoint **for verification**.

## 3. C3 instrument disjointness (question 2) — verified

C3 shares **no instrument code** with C1/C2:

- `plans/round55_c3_chess_probe.py` imports only stdlib + `/usr/bin/bwrap`; it never imports or
  invokes `plans/round52_c2_registry.py`, `plans/round54_c2_entrytruth.py`, or
  `plans/round55_c2_entryargv.py`, and never opens SKILL.md / LOG.md / the ledger (its only
  `open`/`read_text` touches are the sandbox-side `/app/…` artefacts it materializes).
- Its oracle is the already-pinned in-repo capture
  `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` — data, not an
  instrument owned by C1 or C2.
- Its receipt path `corpus/evidence/round55/chess-best-move-probe.txt` and entry
  `corpus/knowledge/tb2-chess-best-move-grader.md` are disjoint from every C1/C2 surface.

Caveat (input-level, not code-level): C3's *script* becomes **input** to C1 (it is advertised→
registered) and to C2 (E4 adds a `round55-c3` ledger row whose entry the new counter re-executes
hermetically). That is a one-way "C1/C2 measure C3" edge — C3 itself never reads or depends on
C1/C2. Disjointness for separability purposes **holds**.

Runtime note for the L1 (not a separability defect): C2's RUN leg will execute `round55-c3`'s
declared entry inside its hermetic worker; that entry runs the real 12-case bwrap battery.
E4's spec anticipates this ("runs the real probe … declare truthfully what you observed"). The
per-row `--timeout` and bwrap availability in the scrubbed env must be honored by E4's declared
`entry_exit`/`timeout_s`, or C2 reports `MISMATCH`/`TIMEOUT` — truthful, but it makes C2's pass
contingent on C3's probe being executable in the hermetic worker.

## 4. The no-harm axis (question 3) — which single landing hurts

The admission rule fires on **partial landings**. Every claim in this round except C3's receipt
is a *universal* predicate over joint state, so a lone landing can actively *create* an axis
harm rather than merely fail:

- **C1 lands with a false verdict-map or self-test cell** → that row is itself a calibration
  harm (a committed self-assessment that does not match observed state), *and* it kills C1's
  claim (operability holds at 8). The trap is already armed: `round54_c1_anchor.py`'s self-test
  is a **subcommand** `selftest` (line 568, *no dashes*), not a `--selftest` flag. If E1 writes
  `--selftest` in that self-test cell, the r52 gate's `selftest_unbacked` leg greps the body,
  finds no `--selftest`, and reports `SELFTEST-UNBACKED 1` → C1 fails *and* a false cell lands.
  Smallest correction: E1's `round54-c1` self-test cell must name `selftest` (subcommand),
  verified against `plans/round54_c1_anchor.py`'s argparse before writing.
- **C3 (or C2) lands its advertisement but C1's rows do not** → `python3 plans/round55_c3_chess_probe.py`
  (and `…_c2_entryargv.py` via its registry cell) is advertised-but-unregistered →
  `MISSING` → the *exact* r54 regression that cost operability 9→8 recurs. A C3/C2 landing
  without C1 is an operability harm, not a neutral partial.
- **C1 lands before E2's `round55_c2_entryargv.py` exists** → its `round55-c2` row is
  `ENTRY-MISSING` → C1 fails and a committed registry row points at a nonexistent entry
  (operability harm).
- **C2's ledger rows land without C1's registry rows** → ledger has rows the registry lacks
  → `extra` → a calibration divergence between two committed self-assessments.
- **The 17-cell L1/L2 reconciliation lands unchecked** → see §5; each rewritten registry entry
  cell is a self-assessment that must be re-measured, else calibration is harmed by unverified
  "corrections".

Smallest safe rule for the L1: **atomicity** — land C1's rows + E2's entryargv + E5's probe +
E4's ledger rows + the entry-cell reconciliations in the same measured-after tip, or revert the
unmatched halves. No single-file landing is axis-safe except C3's receipt/entry *behind* C1's
`round55-c3` row already being present.

## 5. A reachability defect found while auditing (report, do not fix)

The frozen after-predicate requires `argv_defect=0 wrapper_defect=0 abbrev_defect=0`. A `--dry`
static-leg run at HEAD reports **`argv_defect=17 wrapper_defect=1`** (receipt saved). Neither
E1 (appends only the 5 new rows) nor E4 (corrects only `round35-c1-coverage` + adds 5 rows) is
scoped to fix them:

- **17 L1 `ARGV-DEFECT`s** — the registry entry cells document *generic* argv
  (`<expect.json>`, `DIR`, `REV`, `[--rerun]`, `PATH…`, `N`) while the ledger declares the
  *concrete measured* argv. L1 demands token-equality, so all 17 fire. The reconciliation must
  be planned (rewrite the registry first-backtick-span to the concrete invocation, keeping the
  generic form as a later span, *or* re-declare the ledger) — it is currently unassigned.
- **1 L2 `WRAPPER-DEFECT`** — `tb2-grader-probe`: honest argv `['uv','run','--no-project',
  '--with','biopython==1.85','python3',…]`, `argv[0]='uv'`. There is **no truthful `python3`
  argv**: `import Bio` at line 145 fails in the hermetic env (verified: `import Bio` →
  ImportError on this host). Dropping the registry row does not help — the script stays
  `ADVERTISED` (the r52 CMD regex matches `python3 plans/tb2_grader_probe.py` inside the `uv
  run` text) → C1 then reports `MISSING`. The only resolutions are (a) re-declare the row
  `python3 …` red (truthful but *degrades a working probe's declared entry*), or (b) amend
  L2/L1 by dated amendment-row to allow a declared pinned-env wrapper — a freeze change the
  seats cannot make. This is a **fix-now-or-the-after-predicate-cannot-pass** defect; surface
  to the L1 integrator, not to E1/E4 mid-flight.

## 6. Verdict framing the report should use

Recommend the report frame separability as **verification-independence (the r52 standard),
with the pass-dependence declared, not hidden**:

1. **Separability: PASS under the operative reading.** The three counters are independently
   runnable and each attributes its own verdict on any tree; none can pass on a broken sibling
   state. C1 measures the advertised/registered universe; C2 measures the ledger↔registry↔
   observed binding; C3 measures its captured grader — three disjoint verification inputs.
2. **But this round fails pass-in-isolation for C1 and C2 (only C3 stands alone).** State the
   coupling map (§2) explicitly as a *premise*: C1∧C2 must co-land at the measured-after tip.
   This is the freeze's own design ("R55-C1's repair restores its true exit 0"), so it is a
   declared precondition, not a discovered defect — provided the report names it.
3. **Flag the two real defects for the L1:** (i) the unassigned 17-row L1 + 1-row L2
   reconciliation that blocks C2's `argv_defect=0/wrapper_defect=0` regardless of C1; (ii)
   `tb2-grader-probe`'s unresolvable `uv` entry under the frozen L2 wording.
4. **Harm vector to police:** only a *partial* landing harms an axis (advertised-unregistered
   scripts → operability; ledger-registry divergence or a false cell → calibration). Atomic
   integration is the mitigation.

Judged-on axes touched: **operability** (the C1↔C3/C2 advertisement & ENTRY-MISSING couplings)
and **calibration** (the C2 ledger↔registry binding, the 17-cell reconciliation, the tb2 cell).

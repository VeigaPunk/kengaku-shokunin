# M4ControlsMutants — scoped findings (kengaku r55 w1, mutation-tester)

Target: fixture realism of `plans/round55_c2_controls.py` (scratch copy only).
Claim probed: **R55-C2** frozen *before* control — the two laundering fixtures must make the
unchanged r54 counter pass while the registry-declared entry truly exits 1.

**Result: 3/3 mutants killed, 0 survived.** The fixture is not vacuous; the laundering route
really depends on (a) argparse prefix abbreviation and (b) a genuinely failing true entry, and the
r54 counter does not pass a ledger row whose declared entry exit contradicts the observed one.

| mutant | mutation (scratch only) | observed | verdict |
|---|---|---|---|
| baseline | — | `PREDICATE R54-C2 pass`, `ROUTE laundering demonstrated`, exit 0 | live |
| A | `ArgumentParser(allow_abbrev=False)` | `LAUNDERED fixture-gate declared green, entry exit=2`, `PREDICATE R54-C2 fail`, `ROUTE laundering NOT demonstrated`, exit 1; selftest `FAIL abbreviation-live (--selft exits 0)` | killed |
| B | gate true entry `sys.exit(1)`→`sys.exit(0)` | `COUNTER EXIT 0`, `TRUE REGISTRY ENTRY … exit=0`, `ROUTE laundering NOT demonstrated (r54 rc=0, true entry exit=0)`, exit 1 (both frozen cases) | killed |
| C | ledger `entry_exit 0/green`→`1/red` | `BAD-DECL fixture-gate`, `RUN executed=0`, `PREDICATE R54-C2 fail`, exit 1 — not a pass, but detector is `BAD-DECL`, not `MISMATCH` | killed (detector differs) |
| C′ | C + required red `reason`/`evidence` | `MISMATCH fixture-gate declared exit=1 observed exit=0`, `mismatched=1`, `PREDICATE R54-C2 fail`, exit 1 (both frozen cases) | killed (predicted detector) |

Restoration: scratch copy restored to the pristine sha256
`c7591bc6d682c542a595b7fc959f74af61254c53863b8aafd72ecf7c50cbf13d` (== the lane file's hash,
unchanged); post-restore re-run reproduces the baseline (case exit 0, `ROUTE laundering
demonstrated`; `--selftest` exit 0, `cases=4 failures=0`). Scratch dir deleted.

## Defects reported (not fixed — owned by the round-55 instrument seat)

- **DEFECT-1 (fixture writer):** `_fixture()` writes a ledger row valid only in the
  green/exit-0 shape (no `reason`/`evidence`). The r54 counter's `static_legs()` marks a `red`
  row lacking those as `bad_decl` and excludes it from execution, so a ledger state flip in this
  fixture is caught as `BAD-DECL` + `executed=0`, never as the executed-leg `MISMATCH`. If the
  round wants the fixture to assert the MISMATCH detector, `_fixture()` must be able to emit a
  statically valid red row.
- **DEFECT-2 (operability):** `main()` uses
  `tempfile.mkdtemp(prefix="kengaku-r55-controls-", dir="/fast/scratch/hyaku/kengaku-r55")` — a
  hardcoded path, no `--work` argument, no existence check. Where that root is absent the frozen
  command dies with an uncaught `FileNotFoundError` instead of a clean SETUP exit (measured). It
  does not hardcode `/tmp` and leaves no leftovers.

Neither defect changes a frozen predicate, counter, kill rule or claim; both are data/ergonomics
observations for the instrument seat and the L1.

Receipts: `.ufo/waves/round-55/w1/M4ControlsMutants/mutants.md` (full outputs) and
`.ufo/waves/round-55/w1/M4ControlsMutants/report.md` (commands + exit codes).

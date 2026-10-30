# Seat E3ControlsVerify — report (kengaku round 55, wave 1)

**Assignment:** verify the frozen fixture builder `plans/round55_c2_controls.py`
(committed at `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`) by running its selftest and
both frozen laundering cases against the unchanged r54 counter, then diff the outputs
against the committed before-receipts. Lane writes: none (verification seat).

## What I ran

All commands run with cwd = `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (the
fixture builder resolves its lane via `__file__` and writes only under a temp dir in
`/fast/scratch/hyaku/kengaku-r55`, which it removes in a `finally:` block — confirmed
no `kengaku-r55-controls-*` dirs left behind, and `git status` in the lane shows no
new changes attributable to this seat).

Scratch dir created per contract: `/fast/scratch/hyaku/kengaku-r55/E3ControlsVerify/`
(deleted after receipts were copied into the named outputs below).

| # | Command | Exit |
|---|---|---|
| 1 | `python3 plans/round55_c2_controls.py --selftest` | 0 |
| 2 | `python3 plans/round55_c2_controls.py --case abbreviated-selftest --against r54` | 0 |
| 3 | `python3 plans/round55_c2_controls.py --case uv-decoy-script --against r54` | 0 |

Environment: Python 3.14.8, git 2.56.0, uv present at `/home/vgpnk/.local/bin/uv`
(needed by the uv-decoy case, which executes `uv run --no-project --offline python3
-cprint('wrapper green') …`). No tools installed or upgraded by this seat.

## Output 1 — `--selftest` (exit 0)

```
SELFTEST ok r54-passes-abbreviated-selftest
SELFTEST ok r54-passes-uv-decoy-script
SELFTEST ok truthful-fixture-passes-r54
SELFTEST ok abbreviation-live (--selft exits 0)
SELFTEST cases=4 failures=0
```

All four control assertions hold: the r54 counter passes both laundering fixtures,
passes a truthful red-declared fixture, and the gate's argparse genuinely accepts the
`--selft` abbreviation (the attack route is live, not staged).

## Output 2 — `--case abbreviated-selftest --against r54` (exit 0)

```
CASE abbreviated-selftest
ARGV ["python3", "plans/fixture_gate.py", "--selft"]
== r54 counter over the laundering fixture (unchanged module) ==
ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=e84abba186f1bd95531a435257bde48033852594 clean=yes lane_rev_equal=yes
RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0
TIPSTATE entry_declared_green=1 entry_declared_red=0 observed_green=1 observed_red=0
MIGRATION redeclared=0 r53_green_nonentry=0
PREDICATE R54-C2 pass
COUNTER EXIT 0
TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1 out=entry failed: fixture gate is broken on purpose
ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)
```

## Output 3 — `--case uv-decoy-script --against r54` (exit 0)

```
CASE uv-decoy-script
ARGV ["uv", "run", "--no-project", "--offline", "python3", "-cprint('wrapper green')", "python3", "plans/fixture_gate.py"]
== r54 counter over the laundering fixture (unchanged module) ==
ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=1a8428b66048c5229993d9f72736e237f6796cbe clean=yes lane_rev_equal=yes
RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0
TIPSTATE entry_declared_green=1 entry_declared_red=0 observed_green=1 observed_red=0
MIGRATION redeclared=0 r53_green_nonentry=0
PREDICATE R54-C2 pass
COUNTER EXIT 0
TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1 out=entry failed: fixture gate is broken on purpose
ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)
```

## Diff-vs-receipt analysis

Receipts compared (committed before-receipts under `.ufo/waves/round-55/claims/`):

- `c2-before-abbreviated-selftest.txt` vs output 2
- `c2-before-uv-decoy-script.txt` vs output 3

Result of `diff` with only the `SOURCE rev=` fixture-hash line excluded:

- **abbreviated-selftest: byte-identical except the fixture revision hash**
  (receipt `82c5279743766a27f866997d2faaa35ddf58341a` → observed
  `e84abba186f1bd95531a435257bde48033852594`). The hash is the scratch fixture
  repo's own commit id, freshly generated per run — differing is expected and called
  out in the seat spec. Everything else — `ROWS`, `RUN` (`laundered=0`),
  `TIPSTATE`, `MIGRATION`, `PREDICATE R54-C2 pass`, `COUNTER EXIT 0`,
  `TRUE REGISTRY ENTRY … exit=1`, `ROUTE laundering demonstrated (r54 rc=0, true
  entry exit=1)` — matches exactly.
- **uv-decoy-script: byte-identical except the fixture revision hash**
  (receipt `8d00e0a207eda59394318db612481061300e5519` → observed
  `1a8428b66048c5229993d9f72736e237f6796cbe`). All PREDICATE/ROUTE/EXIT lines match
  exactly.
- In both, the remainder of the `SOURCE` line (`clean=yes lane_rev_equal=yes`) also
  matches; only the hash field differs.

## Drift findings

**None.** No drift between the re-run outputs and the committed before-receipts
beyond the expected per-run fixture revision hashes. The frozen red-before state for
R55-C2 is reproduced exactly as committed: the unchanged r54 counter prints
`PREDICATE R54-C2 pass` / exit 0 over both laundering fixtures while the
registry-declared entry truly exits 1, i.e. the before-side of the claim
(`laundered=0` in the r54 counter's own vocabulary, `ROUTE laundering demonstrated`
in the fixture driver's) holds at the frozen revision.

Observations (not defects, no seat action taken):

- The lane tree at run time already carried sibling-seat/orchestrator state
  (` M corpus/SOURCES.md`, untracked `.ufo/waves/round-55/` dispatch files). These
  are outside this seat's files and were not touched; my runs made zero lane writes
  (verified: fixture work is confined to the scratch temp dir the builder deletes).
- `plans/round55_c2_controls.py` `main()` hardcodes its temp parent to
  `/fast/scratch/hyaku/kengaku-r55` (mkdtemp `dir=` argument), not `/tmp`, and
  cleans it in `finally`. It honours the round's scratch-root rule; it lacks a
  `--work` flag, but the file is frozen and this seat was assigned verification
  only, so this is reported as an observation, not changed.
- The `--against r55` mode was not exercised by this seat's frozen command set
  (it requires `plans/round55_c2_entryargv.py`, still under construction by the
  round-55 wave); the builder reports exit 2 / `SETUP` if that counter is absent.

## Files written

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-55/w1/E3ControlsVerify.md`
  (this content, seat findings)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-55/w1/E3ControlsVerify/report.md`
  (this report)

Scratch (`/fast/scratch/hyaku/kengaku-r55/E3ControlsVerify/`, three captured `.out`
files) deleted after the reports were written, per contract. No installs, no
lane-tree writes, no git/jj mutations.

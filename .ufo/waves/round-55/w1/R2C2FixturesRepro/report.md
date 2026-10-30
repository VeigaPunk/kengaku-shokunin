# Seat R2C2FixturesRepro — report (kengaku round 55, w1)

**Assignment:** Independent rebuild of the two R55-C2 laundering fixtures with my own
minimal builder (not reusing `plans/round55_c2_controls.py`) and re-demonstration of the
red-before state, compared against the committed before-receipts.

**Verdict: PASS.** Both frozen laundering fixtures reproduce exactly against the unchanged
r54 counter; both receipts match the committed before-receipts byte-for-byte except the
`SOURCE rev=` line (each scratch fixture is its own git repo, so its commit hash legitimately
differs). The registry-declared entry `python3 plans/fixture_gate.py` exits 1 on both.

## Environment

- Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` @ `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`
  (freeze commit on base `798f5e9ef30ef39291295565209b65a17343c00e`; `git status --porcelain`
  shows no modification to `plans/round54_c2_entrytruth.py`,
  `plans/round55_c2_controls.py`, or `.ufo/waves/round-55/claims/`).
- Tools used: system `git`, `python3 3.14.8`, `uv 0.13.0` (pre-installed; **no installs this seat**).
- No lane writes except my named outputs under `.ufo/waves/round-55/w1/R2C2FixturesRepro/`.
- Scratch: `/fast/scratch/hyaku/kengaku-r55/R2C2FixturesRepro/` (deleted after receipts copied).

## What I ran

1. Read frozen spec: `plans/round-55-claims.md` (R55-C2 Before block), the unchanged r54
   counter `plans/round54_c2_entrytruth.py` (static legs, `entry_mode_ok`, `evaluate`,
   `hermetic_env`), prior r54 evidence `.ufo/waves/round-54/w1/R2C2Counter/laundering-probes.txt`,
   and the two committed before-receipts.
2. Wrote my own builder/driver `build_and_run.py` (copied into this output dir). It builds
   each one-row scratch git fixture directly from the frozen case spec:
   - `SKILL.md` with one `## Gate/probe registry` row:
     `` | `fixture-gate` | gate | `python3 plans/fixture_gate.py` | `0` ok · `1` bad | none | none | none | kengaku | ``
   - `plans/fixture_gate.py`: argparse `--selftest` (abbrev-accepting); bare entry prints
     `entry failed: fixture gate is broken on purpose` and exits 1.
   - `plans/round54-entrytruth.json` (schema `r54-entrytruth-v1`): row `fixture-gate`
     declared green, `entry_exit 0`, `timeout_s 60`, `entry_argv` per case
     (`["python3","plans/fixture_gate.py","--selft"]` /
     `["uv","run","--no-project","--offline","python3","-cprint('wrapper green')","python3","plans/fixture_gate.py"]`).
   - `git init/add/commit` in the fixture root with a `rev-parse --show-toplevel` guard
     asserting the toplevel equals the fixture dir (host-guard parity).
3. Imported the **unchanged** r54 counter by path and ran `evaluate(root, root, work, 1, 60, False)`
   over each fixture; then ran the registry-declared entry directly under the counter's
   `hermetic_env` for ground truth.
4. Oracle cross-check (verification only): imported `plans/round55_c2_controls.py` and
   called its `_fixture` into a scratch dir, byte-diffing the three tree files
   (`SKILL.md`, `plans/fixture_gate.py`, `plans/round54-entrytruth.json`) per case.

## Commands and exit codes

| Command | Exit |
|---|---|
| `python3 build_and_run.py` (in scratch) | **0** |
| `python3 oracle_diff.py` (in scratch) | **0** (`failures=0`, 6/6 files byte-equal) |
| r54 counter inside case abbreviated-selftest | `PREDICATE R54-C2 pass`, counter exit **0** |
| r54 counter inside case uv-decoy-script | `PREDICATE R54-C2 pass`, counter exit **0** |
| true registry entry (both cases) | exit **1**, out `entry failed: fixture gate is broken on purpose` |

`build_and_run.py` exit 0 means: both fixtures laundered (rc=0 while true entry exit=1)
AND both reproductions match the committed receipts modulo the `SOURCE rev=` line.

## Results per case (repro receipts in this dir)

- `repro-abbreviated-selftest.txt`: `ROWS registry=1 ledger=1 missing=0 extra=0
  argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1`;
  `SOURCE rev=36835d6e… clean=yes lane_rev_equal=yes`;
  `RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0`;
  `TIPSTATE entry_declared_green=1 entry_declared_red=0 observed_green=1 observed_red=0`;
  `MIGRATION redeclared=0 r53_green_nonentry=0`; `PREDICATE R54-C2 pass`; `COUNTER EXIT 0`;
  `TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1 out=entry failed: …`.
  → `COMPARE abbreviated-selftest: MATCH committed receipt modulo SOURCE rev line`.
  Committed receipt's rev: `82c52797…` — differs only because it is a different scratch repo's
  commit; all other lines identical.
- `repro-uv-decoy-script.txt`: identical shape; `SOURCE rev=6682f5c3…`;
  committed receipt's rev `8d00e0a2…` — same explanation.
  → `COMPARE uv-decoy-script: MATCH committed receipt modulo SOURCE rev line`.

Mechanism re-verified live: `--selft` is accepted by argparse `allow_abbrev` → gate runs in
selftest mode → exit 0 (the laundered green). The `uv run … python3 -cprint('wrapper green') …`
argv executes only the inline `-c` program (prints `wrapper green`, exit 0) and never reaches
`plans/fixture_gate.py`. The r54 `entry_mode_ok` computes a defect for neither argv
(`--selft` is not a forbidden token; `uv` argv finds `python3` + script), and its result is
unwired — exactly the frozen r54 surface.

## Divergences named

None. Only the `SOURCE rev=` hash differs per fixture, which is expected and non-semantic
(self-contained scratch git repos). No defects found in the frozen receipts, the r54
counter, or the committed controls builder.

## Dead ends / honest notes

- The committed receipts' `ROUTE laundering demonstrated` tail line and my tail line match
  in wording because both report the same demonstrated fact with the same frozen phrase;
  no other path to report it was taken.
- The r55 binding counter `plans/round55_c2_entryargv.py` is under construction by other
  seats this wave; per my seat spec I reproduced the red-before state only and did not
  run the r55 counter (its absence/setup is another seat's surface).
- An unrun check has NOT passed: I did not re-run the committed `round55_c2_controls.py
  --selftest` end-to-end (its r55 leg depends on the not-yet-landed counter); my oracle use
  of that module was limited to its `_fixture` builder for byte-diff verification.

## Files written

Lane outputs (only these):
- `.ufo/waves/round-55/w1/R2C2FixturesRepro/report.md` (this file)
- `.ufo/waves/round-55/w1/R2C2FixturesRepro/repro-abbreviated-selftest.txt`
- `.ufo/waves/round-55/w1/R2C2FixturesRepro/repro-uv-decoy-script.txt`
- `.ufo/waves/round-55/w1/R2C2FixturesRepro/fx-abbreviated-selftest.files.txt`
- `.ufo/waves/round-55/w1/R2C2FixturesRepro/fx-uv-decoy-script.files.txt`
- `.ufo/waves/round-55/w1/R2C2FixturesRepro/build_and_run.py` (my independent builder/driver)
- `.ufo/waves/round-55/w1/R2C2FixturesRepro.md` (scoped findings per seat Report line)

Scratch (deleted): `/fast/scratch/hyaku/kengaku-r55/R2C2FixturesRepro/`.

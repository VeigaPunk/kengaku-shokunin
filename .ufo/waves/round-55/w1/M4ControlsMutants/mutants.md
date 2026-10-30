# M4ControlsMutants — mutation probes of `plans/round55_c2_controls.py` fixture realism

Seat: `M4ControlsMutants` (mutation-tester) · kengaku round 55, wave 1 (v2) · 2026-10-30.
Scope: **fixture realism of `plans/round55_c2_controls.py` only.** No lane file was modified; every
mutation was applied to a scratch copy under `/fast/scratch/hyaku/kengaku-r55/M4ControlsMutants/`
and the bytes were restored between mutants and at the end.

Claim under test: **R55-C2** (calibration 9→10, entry-argv structural binding), specifically its
frozen *before* control: the two laundering fixtures must make the unchanged r54 counter
(`plans/round54_c2_entrytruth.py`) **PASS** (`PREDICATE R54-C2 pass`, exit 0) while the
registry-declared entry truly exits 1 — i.e. the laundering route is live and demonstrable.

Frozen fixtures under probe (from the tool's own docstring, `plans/round55_c2_controls.py:8-22`):
- `abbreviated-selftest` — ledger entry argv `python3 plans/fixture_gate.py --selft`
  (argparse prefix abbreviation of `--selftest`) declared green; registry entry
  `python3 plans/fixture_gate.py` exits 1.
- `uv-decoy-script` — ledger entry argv
  `uv run --no-project --offline python3 -cprint('wrapper green') python3 plans/fixture_gate.py`
  declared green; the wrapper's inline program exits 0 and the true entry is never executed.

## Setup and integrity

Scratch lane (read-only copies of the two plan files the tool loads through `LANE`):

```
S=/fast/scratch/hyaku/kengaku-r55/M4ControlsMutants
mkdir -p $S/lane/plans
cp <lane>/plans/round55_c2_controls.py   $S/lane/plans/
cp <lane>/plans/round54_c2_entrytruth.py  $S/lane/plans/
```

Pristine bytes of the tool under test (unchanged in every mutant cycle):

```
c7591bc6d682c542a595b7fc959f74af61254c53863b8aafd72ecf7c50cbf13d  <lane>/plans/round55_c2_controls.py
c7591bc6d682c542a595b7fc959f74af61254c53863b8aafd72ecf7c50cbf13d  $S/lane/plans/round55_c2_controls.py   (copy, byte-identical)
44c3f412852396451b34fa7d0373b0a5901480189cbf77447b3b050d1cc0da97  <lane>/plans/round54_c2_entrytruth.py
```

All runs were `python3 $S/lane/plans/round55_c2_controls.py …` with cwd `$S`. The tool builds its
own one-row fixture repos under `tempfile.mkdtemp(dir="/fast/scratch/hyaku/kengaku-r55")` and
removes them in its `finally`; every such fixture asserts its own git toplevel
(`_fixture()`'s `fixture root guard`). No mutating git command was issued against the lane repo,
the fleet root, or any sibling repo by this seat.

Detector used (unchanged r54 module, `plans/round54_c2_entrytruth.py`):
`LAUNDERED <name> declared green, entry exit=<rc>` · `MISMATCH <name> declared exit=<X> observed exit=<Y>` ·
`BAD-DECL <name>` · `PREDICATE R54-C2 pass|fail`; and the control's own line
`ROUTE laundering demonstrated|NOT demonstrated (r54 rc=<rc>, true entry exit=<rc>)`.

---

## BASELINE (pristine bytes) — must be green, else every mutant below is inconclusive

`python3 lane/plans/round55_c2_controls.py --case abbreviated-selftest --against r54` → **exit 0**

```
CASE abbreviated-selftest
ARGV ["python3", "plans/fixture_gate.py", "--selft"]
== r54 counter over the laundering fixture (unchanged module) ==
ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=b286ebfe505438010a1957ae594d83e0778e8fe3 clean=yes lane_rev_equal=yes
RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0
TIPSTATE entry_declared_green=1 entry_declared_red=0 observed_green=1 observed_red=0
MIGRATION redeclared=0 r53_green_nonentry=0
PREDICATE R54-C2 pass
COUNTER EXIT 0
TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1 out=entry failed: fixture gate is broken on purpose
ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)
```

`python3 lane/plans/round55_c2_controls.py --case uv-decoy-script --against r54` → **exit 0**
(same shape; `PREDICATE R54-C2 pass`, `COUNTER EXIT 0`, `TRUE REGISTRY ENTRY … exit=1`,
`ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)`). `uv` is present on this host at
`/home/vgpnk/.local/bin/uv`.

`python3 lane/plans/round55_c2_controls.py --selftest` → **exit 0**
(`SELFTEST ok` ×4, `SELFTEST cases=4 failures=0`).

Baseline verdict: **live** — the laundering route is demonstrable and the r54 counter passes the
fixture, exactly as the frozen before-receipt claims.

---

## MUTANT A — `argparse` abbreviation disabled in the fixture gate (`allow_abbrev=False`)

Mutation (one line, in `GATE_SRC` of the scratch copy):
`p = argparse.ArgumentParser()` → `p = argparse.ArgumentParser(allow_abbrev=False)`

Expected detector: the abbreviated-selftest case must FAIL to demonstrate laundering against r54
(the route dies) — proving the fixture's laundering depends on argparse's prefix abbreviation.

Observed — `python3 lane/plans/round55_c2_controls.py --case abbreviated-selftest --against r54`
→ **exit 1** (killed; baseline was exit 0):

```
CASE abbreviated-selftest
ARGV ["python3", "plans/fixture_gate.py", "--selft"]
== r54 counter over the laundering fixture (unchanged module) ==
ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=441baaed9baeabad141702b0bd7468ffa86ecbca clean=yes lane_rev_equal=yes
  LAUNDERED fixture-gate declared green, entry exit=2
RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=1
TIPSTATE entry_declared_green=1 entry_declared_red=0 observed_green=0 observed_red=1
MIGRATION redeclared=0 r53_green_nonentry=0
PREDICATE R54-C2 fail
COUNTER EXIT 1
TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1 out=entry failed: fixture gate is broken on purpose
ROUTE laundering NOT demonstrated (r54 rc=1, true entry exit=1)
```

Observed — same mutant, `python3 lane/plans/round55_c2_controls.py --selftest` → **exit 1**:

```
SELFTEST FAIL r54-passes-abbreviated-selftest
SELFTEST ok r54-passes-uv-decoy-script
SELFTEST ok truthful-fixture-passes-r54
SELFTEST FAIL abbreviation-live (--selft exits 0)
SELFTEST cases=4 failures=2
```

**Verdict A: KILLED.** Both predicted flips observed: the `--selft` token is no longer accepted
(argparse usage error → entry exit 2), the r54 counter flags `LAUNDERED fixture-gate declared
green, entry exit=2` and `PREDICATE R54-C2 fail` (counter exit 1), and the control's ROUTE line
flips to `laundering NOT demonstrated`. The tool's own `abbreviation-live` leg fails as well, which
is the direct proof that the fixture's laundering route rides on argparse prefix abbreviation
rather than on any property of the counter.

---

## MUTANT B — the fixture gate's true entry exit flipped from 1 to 0

Mutation (one line, in `GATE_SRC` of the scratch copy):
`print("entry failed: fixture gate is broken on purpose")` / `sys.exit(1)` → `sys.exit(0)`

Expected detector: the true-entry check must flip the ROUTE line to NOT demonstrated (nothing left
to launder, because the registry-declared entry is genuinely green).

Observed — `python3 lane/plans/round55_c2_controls.py --case abbreviated-selftest --against r54`
→ **exit 1** (killed; baseline was exit 0):

```
CASE abbreviated-selftest
ARGV ["python3", "plans/fixture_gate.py", "--selft"]
== r54 counter over the laundering fixture (unchanged module) ==
ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=280310283cea4d77e986ad484d4682d51be86679 clean=yes lane_rev_equal=yes
RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0
TIPSTATE entry_declared_green=1 entry_declared_red=0 observed_green=1 observed_red=0
MIGRATION redeclared=0 r53_green_nonentry=0
PREDICATE R54-C2 pass
COUNTER EXIT 0
TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=0 out=entry failed: fixture gate is broken on purpose
ROUTE laundering NOT demonstrated (r54 rc=0, true entry exit=0)
```

Observed — same mutant, `--case uv-decoy-script --against r54` → **exit 1**, same flip
(`COUNTER EXIT 0`, `TRUE REGISTRY ENTRY … exit=0`, `ROUTE laundering NOT demonstrated (r54 rc=0,
true entry exit=0)`).

**Verdict B: KILLED.** The r54 counter still passes (rc=0) — the counter is unchanged and blind to
this — but the control's true-entry check now sees exit 0, so the ROUTE line flips to
`laundering NOT demonstrated` and the case exits 1. The ROUTE line therefore genuinely depends on
the registry-declared entry's true exit code, i.e. the "laundering" claim is not vacuous.

---

## MUTANT C — ledger `entry_exit`/`entry_state` flipped to 1/red

### C (literal single-field flip, as specified)

Mutation (in `_fixture()`'s ledger row of the scratch copy):
`"entry_exit": 0, "entry_state": "green"` → `"entry_exit": 1, "entry_state": "red"`

Expected detector: the r54 counter must flag a MISMATCH (not pass).

Observed — `python3 lane/plans/round55_c2_controls.py --case abbreviated-selftest --against r54`
→ **exit 1** (killed; baseline was exit 0):

```
CASE abbreviated-selftest
ARGV ["python3", "plans/fixture_gate.py", "--selft"]
== r54 counter over the laundering fixture (unchanged module) ==
ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=1 duplicate_names=0 bad_table_lines=0 headings=1
  BAD-DECL fixture-gate
SOURCE rev=ebf62540624497e7e1d205ecad5ac692594ac752 clean=yes lane_rev_equal=yes
RUN executed=0 timeout=0 mismatched=0 evidence_missing=0 laundered=0
TIPSTATE entry_declared_green=0 entry_declared_red=0 observed_green=0 observed_red=0
MIGRATION redeclared=0 r53_green_nonentry=0
PREDICATE R54-C2 fail
COUNTER EXIT 1
TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1 out=entry failed: fixture gate is broken on purpose
ROUTE laundering NOT demonstrated (r54 rc=1, true entry exit=1)
```

**Verdict C (literal flip): KILLED — but not by the predicted detector.** The counter refuses to
pass (`PREDICATE R54-C2 fail`, exit 1), which is the substantive requirement ("not pass"), yet it
does **not** print `MISMATCH`. It prints `BAD-DECL fixture-gate` instead: the r54 counter's
`static_legs()` requires a `red` declaration to carry a `reason` (≥ 10 words) and an `evidence`
fragment (≥ 6 chars), and the fixture's ledger row carries neither, so the row is rejected
statically and excluded from execution (`RUN executed=0`). The predicted `MISMATCH` leg is
therefore unreachable through the fixture's own ledger writer as it stands — see DEFECT-1.

### C′ (same flip plus the statically-required red fields, to exercise the executed leg)

Mutation: C's flip **plus** in the same ledger row
`"reason": "the fixture gate's entry mode is broken on purpose for this control fixture"` and
`"evidence": "entry failed: fixture gate is broken on purpose"` (the gate's real entry-mode
output fragment).

Observed — `python3 lane/plans/round55_c2_controls.py --case abbreviated-selftest --against r54`
→ **exit 1** (killed; baseline was exit 0):

```
CASE abbreviated-selftest
ARGV ["python3", "plans/fixture_gate.py", "--selft"]
== r54 counter over the laundering fixture (unchanged module) ==
ROWS registry=1 ledger=1 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
SOURCE rev=5e51319e5869359fb89d275eba9a6f7c851a503e clean=yes lane_rev_equal=yes
  MISMATCH fixture-gate declared exit=1 observed exit=0 sec=0.0
RUN executed=1 timeout=0 mismatched=1 evidence_missing=0 laundered=0
TIPSTATE entry_declared_green=0 entry_declared_red=1 observed_green=1 observed_red=0
MIGRATION redeclared=0 r53_green_nonentry=0
PREDICATE R54-C2 fail
COUNTER EXIT 1
TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1 out=entry failed: fixture gate is broken on purpose
ROUTE laundering NOT demonstrated (r54 rc=1, true entry exit=1)
```

Observed — same mutant, `--case uv-decoy-script --against r54` → **exit 1**, same
`MISMATCH fixture-gate declared exit=1 observed exit=0`, `RUN executed=1 … mismatched=1`,
`PREDICATE R54-C2 fail`.

**Verdict C′: KILLED, with the predicted detector.** The counter flags
`MISMATCH fixture-gate declared exit=1 observed exit=0`, `mismatched=1`,
`PREDICATE R54-C2 fail` (exit 1) — it does not pass a ledger row whose declared entry exit
contradicts the observed one.

---

## DEFECT-1 (found; owned by the round-55 instrument seat, not by this seat)

`plans/round55_c2_controls.py`'s `_fixture()` writes a ledger row that is **only valid in the
green/exit-0 configuration**: it emits `entry_argv`, `entry_exit`, `entry_state`, `timeout_s` and
no `reason`/`evidence`. The r54 counter's `static_legs()` marks any `red` row without a
≥ 10-word `reason` and a ≥ 6-char `evidence` fragment as `bad_decl` and skips executing it. Hence
any state flip of the fixture's ledger row can only be detected as `BAD-DECL` + `executed=0`,
never as the executed-leg `MISMATCH`. If the round wants the fixture to *assert* the MISMATCH
detector (or any other executed-leg detector), `_fixture()` must be able to emit a statically
valid red row. This is a data/ergonomics observation about the fixture writer; no frozen predicate,
counter or kill rule was touched, and no sibling file was modified by this seat.

## DEFECT-2 (found; operability observation)

`plans/round55_c2_controls.py:main()` creates its work dir with
`tempfile.mkdtemp(prefix="kengaku-r55-controls-", dir="/fast/scratch/hyaku/kengaku-r55")` — a
hardcoded path with **no `--work` argument** (the counters take `--work`; this tool does not) and
no existence check. On a host where that round scratch root does not exist, the frozen command
dies with an uncaught `FileNotFoundError` traceback instead of a clean `SETUP` exit. Measured:
`tempfile.mkdtemp(prefix='kengaku-r55-controls-', dir='/fast/scratch/hyaku/kengaku-r55-absent')`
→ `FileNotFoundError [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r55-absent/kengaku-r55-controls-kuylbacs'`.
It does not hardcode `/tmp` (compliant with the lane rule), and it removes its own work dir in a
`finally` (no leftovers observed: `ls -d /fast/scratch/hyaku/kengaku-r55/kengaku-r55-controls-*`
→ no match, exit 2).

## Restoration evidence

After the last mutant the scratch copy was restored from the pristine snapshot and re-verified:

```
RESTORE_EXIT=0
c7591bc6d682c542a595b7fc959f74af61254c53863b8aafd72ecf7c50cbf13d  lane/plans/round55_c2_controls.py
c7591bc6d682c542a595b7fc959f74af61254c53863b8aafd72ecf7c50cbf13d  pristine-round55_c2_controls.py
```

Post-restore re-run (same bytes as baseline):
`--case abbreviated-selftest --against r54` → **exit 0**, `PREDICATE R54-C2 pass`,
`COUNTER EXIT 0`, `ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)`;
`--selftest` → **exit 0**, `SELFTEST cases=4 failures=0`.

Lane integrity: `<lane>/plans/round55_c2_controls.py` sha256
`c7591bc6d682c542a595b7fc959f74af61254c53863b8aafd72ecf7c50cbf13d` (unchanged from the value
recorded before any mutation). `git -C <lane> status --porcelain -- plans/` shows only
`?? plans/round55_c2_entryargv.py` and `?? plans/round55_c3_chess_probe.py` — untracked files
belonging to the round's other seats, untouched by this seat.

## Summary table

| mutant | mutation (scratch copy only) | expected detector | observed | verdict |
|---|---|---|---|---|
| baseline | none | route demonstrable, counter passes | `PREDICATE R54-C2 pass`, `ROUTE laundering demonstrated`, exit 0 | live (green) |
| A | `ArgumentParser(allow_abbrev=False)` | abbrev route dead; case must fail | `LAUNDERED fixture-gate declared green, entry exit=2`, `PREDICATE R54-C2 fail`, `ROUTE laundering NOT demonstrated`, exit 1; selftest `FAIL abbreviation-live` | **killed** |
| B | gate true entry `sys.exit(1)`→`sys.exit(0)` | ROUTE flips to NOT demonstrated | `COUNTER EXIT 0`, `TRUE REGISTRY ENTRY … exit=0`, `ROUTE laundering NOT demonstrated (r54 rc=0, true entry exit=0)`, exit 1 (both frozen cases) | **killed** |
| C | ledger `entry_exit 0/green`→`1/red` | counter flags MISMATCH, not pass | `BAD-DECL fixture-gate`, `RUN executed=0`, `PREDICATE R54-C2 fail`, exit 1 — not pass, but detector is BAD-DECL not MISMATCH | **killed (detector differs — see DEFECT-1)** |
| C′ | C + required red `reason`/`evidence` | counter flags MISMATCH, not pass | `MISMATCH fixture-gate declared exit=1 observed exit=0`, `mismatched=1`, `PREDICATE R54-C2 fail`, exit 1 (both frozen cases) | **killed (predicted detector observed)** |

No mutant survived. No predicate, counter, kill rule or frozen claim text was altered by this seat.

# C2BindingBypass — seat report (kengaku r55 w1)

Attack seat on R55-C2's binding legs. Analysis target: the frozen L1–L4 leg text in
`plans/round-55-claims.md` §R55-C2 plus the unchanged r54 counter
(`plans/round54_c2_entrytruth.py` at 80afa613), which the r55 instrument reuses.

## What I ran

All work in `/fast/scratch/hyaku/kengaku-r55/C2BindingBypass/` (created, deleted on exit
after receipts were copied out). Fixture driver `driver.py` built 9 git fixture repos
(f1, f2, f3, f3-pyc, f4, f5, f6, f7-rowplant, f7-symlink) and ran the frozen r54
counter's `evaluate()` in-process against each; every git mutation asserted
`git rev-parse --show-toplevel` == fixture dir first. No lane writes, no mutating git
in the lane, one process at a time.

Commands (all under the scratch dir; r54 counter loaded read-only from the lane):

- `python3 driver.py` — all fixtures, neutral env →
  `f1=1 f2=0 f3=1 f4=0 f5=1 f6=0 f7=0` (rcs are counter exits per fixture, expected
  profile; details below)
- `KENGAKU_POISON=1 python3 driver.py --only f1-envpoison` → counter exit **0**
  (PREDICATE R54-C2 pass while neutral-truth exit=7)
- `python3 driver.py --only f6-envkill` — 4 counter invocations in one fixture:
  neutral → **1** (LAUNDERED, safe); `PYTHONPATH=…/force0` (`sitecustomize` `os._exit(0)`)
  → **0** (PREDICATE pass — kill shape); `PYTHONPATH=…/tag` → **1** but foreign code ran
  inside the hermetic exec (marker kept in `disagreed-red-gate.txt`);
  `PATH=<shimdir>:$PATH` with `shimdir/python3`=`#!/bin/sh exit 0` → **0**
  (PREDICATE pass — kill shape, executed binary not even Python)
- `python3 -m plans.gate` inside a fixture with only tracked `plans/gate.pyc` → exit 0
  (`sourceless .pyc` executes — unreviewable entry bytes)
- `python3 -c "import Bio"` → ModuleNotFoundError (host system python3 lacks biopython;
  confirms the tb2 row's plain-python3 entry is truly red, per its own verdict map)
- Registry census over `SKILL.md` (78 rows): 0 absolute-interpreter entries, 0 `-m`,
  0 `-c`, 1 `uv` entry (`tb2-grader-probe`), 75/78 multi-backtick-span entry cells.

Also read: `plans/round-55-claims.md`, `plans/round54_c2_entrytruth.py` (full),
`plans/round55_c2_controls.py` (frozen controls builder — confirms my fixtures' shape
matches the freeze), before-receipts `claims/c2-before-*.txt`, ledger
`plans/round54-entrytruth.json` (78 rows, schema r54-entrytruth-v1).

## Files I wrote (named outputs)

- `.ufo/waves/round-55/w1/C2BindingBypass.md` — scoped findings (7 routes analyzed)
- `.ufo/waves/round-55/w1/C2BindingBypass/report.md` — this file
- `.ufo/waves/round-55/w1/C2BindingBypass/driver.py` — fixture builder/replayer
- `.ufo/waves/round-55/w1/C2BindingBypass/receipts/*.txt` — 14 counter transcripts +
  kept disagreement output

## Routes analyzed (≥5 required; 7 delivered) — see C2BindingBypass.md for detail

1. **Env-hygiene (KILL candidate)** — `hermetic_env` inherits caller `PATH`/`PYTHONPATH`
   verbatim; `PATH` shim `python3`→`exit 0` and `PYTHONPATH` `sitecustomize`→`os._exit(0)`
   both turn a truly-red entry (exit 7) into `PREDICATE R54-C2 pass`. The frozen claims
   say the r55 instrument reuses this hermetic execution unchanged → live at r55 unless
   the builder scrubs. Fix: `python3 -I`, `PATH=/usr/bin:/bin`, drop all `PYTHON*` vars.
2. **`-m` module entry** — r54 refuses (`argv shape`); frozen L2 text permits it;
   L3 has no script to introspect; tracked sourceless `.pyc` executes unreviewably
   (observed `python3 -m plans.gate` → exit 0 with only `plans/gate.pyc`).
3. **tb2-grader-probe / frozen-claims inconsistency** — the row's argv[0]=`uv` and its
   own cell documents plain-`python3` entry as exit 1 (`ModuleNotFoundError: Bio`);
   frozen L2 ⇒ WRAPPER-DEFECT ⇒ `wrapper_defect=0` unreachable, unless the builder
   exempts uv-look-through (partial reopening of the r54 decoy class). Needs a dated
   amendment re-declaring the row red, or claims text must bless look-through + `-c` ban.
4. **Two-span entry cell** — parser binds first `python3 …` match; ledger on first span
   passes while the cell advertises the second span's real command; ledger on second
   span is ARGV-DEFECT (false positive vs a truthful seat). Fix: first span = sole
   declared command; interpreter+script patterns outside span 1 are a static defect.
5. **Evidence substring spoof** — two red rows share one declared fragment; a script
   printing another row's fragment passes (`PREDICATE pass`, `evidence_missing=0`).
   Fix: evidence-fragment uniqueness leg.
6. **Absolute interpreter path** — 0/78 real cells use it; r54 refuses. Frozen "resolve
   to a real interpreter binary" is ambiguous; a basename/`which`-based L2 admits
   `/opt/shim/python3` (and under R1, `which` resolves on caller PATH). Fix: exact token
   `{python3, python}`.
7. **Sibling/`__pycache__` swap** — cross-row planting defeated by per-row `git reset
   --hard + clean -ffdx` (observed `LAUNDERED b-consume`); sourceless `.pyc` can't shadow
   a tracked `.py` for script entries; BUT a tracked symlink `plans/row.py`→ absolute
   foreign path passes with foreign bytes executed (mode 120000 in git index). Fix:
   entry file must be a tracked regular file inside the clone.

## Top-3 runnable fixtures (acceptance) — in `receipts/`, replayable via `driver.py`

- `f6-envkill` (`path-shimkill`, `pypath-inject` runs) — **PREDICATE pass while the
  entry truly exits 7**; static legs all clean (`argv_defect=0 bad_decl=0`).
- `f2-twospan` (`firstspan` pass / `secondspan` ARGV-DEFECT) — parser-authority attack.
- `f4-evidspoof` — PREDICATE pass with spoofed evidence binding.
(plus `f3-module`, `f5-absinterp`, `f7-rowplant`/`f7-symlink` covering routes 2/6/7.)

## Defects found in sibling/frozen artifacts (reporting, not fixing)

- `plans/round-55-claims.md` §R55-C2: L2 wrapper ban vs `tb2-grader-probe` (R3) makes
  `wrapper_defect=0` unreachable under a literal reading — needs a dated amendment.
- `plans/round-55-claims.md` §R55-C2: "reusing the unchanged r54 module's hermetic
  execution" inherits the PATH/PYTHONPATH hole (R1) — "hermetic" is currently untrue.

## Dead ends (tried, did not survive)

- `sys.exit(0)` inside `sitecustomize` → "Fatal Python error: init_import_site" →
  exit 1, not the forged green; `os._exit(0)` is the working mechanism (used).
- PYTHONPATH shadowing of same-named sibling imports: `sys.path[0]` (the script's own
  dir) precedes `PYTHONPATH` in Python 3.14 — sibling shadowing can't be beaten that
  way; the injection routes are `sitecustomize`/`PATH`, not module shadowing.
- Cross-row file planting inside a worker clone (R7-1): per-row `reset()` cleans it —
  the clean-clone protection does hold; remaining gap is tracked symlinks.
- Ledger-side duplicate fragments are not checked (R5 finding), but a green row printing
  a red fragment is harmless — the evidence leg only fires on declared-red rows.

## Installs

None. Used system python3 3.14.8, git, uv (already present; only read for census).
Scratch `/fast/scratch/hyaku/kengaku-r55/C2BindingBypass/` deleted after receipts were
copied into the wave dir.

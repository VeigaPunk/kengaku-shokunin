# C2BindingBypass — R55-C2 binding-leg falsification (attack seat)

Scope: routes the frozen L1–L4 of `plans/round55_c2_entryargv.py` (not yet built) can miss,
plus fixtures run against the frozen r54 counter (`plans/round54_c2_entrytruth.py`,
commit 80afa613). Fixtures + receipts: `.ufo/waves/round-55/w1/C2BindingBypass/`
(`driver.py` rebuilds every fixture; receipts under `receipts/`). The L1 replays them
against the new counter at integration.

## Verdict summary

| # | Route | r54 observed | Frozen L1–L4 status | Severity |
|---|-------|--------------|---------------------|----------|
| R1 | env-hygiene: PATH shim / PYTHONPATH `sitecustomize` | **PREDICATE pass while entry truly exits 7** (kill shape) | Inherited unchanged from r54 → live | **HIGH — kill-rule candidate** |
| R2 | `-m` module entry (`python3 -m plans.gate`) | r54 statically refuses (`ARGV-DEFECT argv shape`) | L2 text permits it; L3 under-defined; `.pyc` hole | HIGH if admitted |
| R3 | tb2-grader-probe row vs L2 wrapper ban | r54 passes the uv row | **Frozen claims inconsistency**: after-predicate requires `wrapper_defect=0` but the row's argv[0]=`uv` and plain `python3` entry is red by its own cell | HIGH — frozen-text defect |
| R4 | two-span entry cell (first benign, second real) | first-span pass; second-span `script mismatch` | Parser authority ambiguous for "declared entry" | MEDIUM |
| R5 | evidence-fragment substring spoof | **PREDICATE pass** with shared fragment | L4 evidence leg has no uniqueness/identity | MEDIUM |
| R6 | absolute interpreter path (`/usr/bin/python3`) | r54 refuses (`interpreter not python3/uv`) | L2 text ambiguous ("resolve to"), basename-normalization risk | MEDIUM |
| R7 | cross-row file planting / tracked symlink → foreign file | planting defeated by per-row `reset()`; **symlink passes, foreign bytes run** | L1 binds tokens not content; provenance gap | LOW–MEDIUM |

---

## R1 (seat routes c-env + b-runtime): hermetic_env inherits caller PATH/PYTHONPATH — KILL SHAPE

`hermetic_env()` (r54 counter lines 128–143, per the claims doc *unchanged* in the r55
instrument) scrubs `GIT_*` and secrets but **inherits PATH, PYTHONPATH, and every other
variable**. Row execution (`run_row`) calls `subprocess.run(argv, cwd=w.dir, env=env)` —
argv[0] resolves via `execvp` on the **caller's PATH**, and the interpreter imports
`sitecustomize.py` from the **caller's PYTHONPATH**.

Fixture `f6-envkill` (receipts `f6-envkill.*.txt`): registry cell `python3 plans/red.py`,
ledger declares green; `plans/red.py` truly exits **7** in a neutral env.

- neutral env: `LAUNDERED red-gate declared green, entry exit=7` → `PREDICATE R54-C2 fail`
  (safe direction, counter works).
- `PATH=<shimdir>:$PATH` where `shimdir/python3` is `#!/bin/sh\nexit 0` — **executed
  binary is not Python at all** → `PREDICATE R54-C2 pass`, `observed_green=1`.
  L2's argv[0] check sees a clean token; it binds the token, never the resolved binary.
- `PYTHONPATH=<inject>/force0` whose `sitecustomize.py` runs `os._exit(0)` (plain
  `sys.exit()` inside sitecustomize is a fatal-import error → exit 1, so `os._exit` is
  the forging mechanism) → `PREDICATE R54-C2 pass`.
- `PYTHONPATH=<inject>/tag` (marker sitecustomize): counter still fails safely, but the
  kept output `disagreed-red-gate.txt` shows
  `sitecustomize-marker: foreign code ran under the counter's hermetic env`.

Kill-rule framing: the counter's only environment is the one the counter itself creates.
The claims call the r54 execution "hermetic"; L1–L4 + unchanged `hermetic_env` means
`python3 plans/x.py` is certified under a caller-controlled interpreter path and caller-
controlled import root. A fixture with all static legs clean passes while the declared
entry truly exits otherwise. Whether this fires the frozen kill rule at integration
depends on the caller-env convention for the after-run — but the instrument is
env-dependent, which the frozen "hermetic" descriptor denies.

Smallest safe corrections for the builder: execute rows as `["-I", script]` with argv[0]
resolved to a **real** interpreter (e.g. `shutil.which` against a scrubbed PATH, or pin
`/usr/bin/python3`); inside `hermetic_env` drop `PYTHONPATH`, `PYTHONSTARTUP`,
`PYTHONHOME`, `PYTHONNOUSERSITE`, all `PYTHON*` vars and set `PATH=/usr/bin:/bin`.
Cost: none of the 78 real rows uses those vars.

## R2 (seat route a): `python -m plans.gate` module entries

Observed (receipt `f3-module.neutral.txt`): r54 **refuses** — `row_script` finds no
`.py` token → `entry_mode_ok(argv, None)` → `ARGV-DEFECT mod-gate: argv shape`.

Under the frozen L1–L4 text: ledger `[python3, -m, plans.gate]` token-equals the cell's
first span → L1 pass; argv[0]=python3, no `-c`, no wrapper → L2 pass. So the r55
instrument as *written* admits a class r54 rejected. Consequences:

1. L3 ("flag token that is a strict prefix of a longer flag accepted by **that script's
   own argparse**") has no script token to introspect — either an unhandled defect or a
   silently skipped leg.
2. **Sourceless `.pyc` hole**: `python3 -m plans.gate` with only a tracked
   `plans/gate.pyc` (legacy sourceless layout, no `gate.py`) executes — observed:
   `SOURCELESS-PYC ... exit=0 out='module gate ran'`. The "entry" is then compiled bytes
   invisible to every source-reading audit leg. Nothing in L1–L4 binds executed bytes to
   reviewable source.
3. `-m` resolves via sys.path[0]=cwd — benign in the counter's clone-root cwd, but it is
   exactly the resolution order R1's PYTHONPATH hole manipulates.

Correction: keep r54's refusal — L2 should require a literal `<script>.py` path token
(any `-m` flag → WRAPPER-DEFECT or ARGV-DEFECT). If module entries are wanted, resolve
the module to a tracked `.py` file first and reject `.pyc`/sourceless resolution.

## R3 (seat route b, real-registry cross-check): tb2-grader-probe vs frozen L2 — defect in the frozen data

Registry census (all 78 cells at commit 80afa613): **0 absolute interpreter paths, 0 `-m`
entries, 0 `-c`, exactly one `uv` row** — `tb2-grader-probe`:
`` `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` ``
(ledger `entry_argv[0]` is `uv`, matching). The cell's own verdict map documents:
*"a missing Biopython is a traceback under exit 1 (ModuleNotFoundError: No module named 'Bio')"*
— verified on this host: `python3 -c "import Bio"` → ModuleNotFoundError.

Frozen L2: "uv/pipx/poetry-style wrappers as argv[0] … are WRAPPER-DEFECTs"; the frozen
after-predicate requires `wrapper_defect=0` over the full ledger; the frozen correction
list does **not** re-declare this row. So at measured-after either:
- the builder exempts `uv run … python3 <script>` from L2 → the wrapper class the
  `uv-decoy-script` fixture was built to kill is partially reopened (a
  `uv run --with X python3 -c…` decoy still needs the `-c` check to save it), or
- L2 is implemented as written → the row is a WRAPPER-DEFECT → `wrapper_defect=0` is
  unreachable → after-predicate fails by construction.

Fixable as data before the after-run: dated amendment re-declaring `tb2-grader-probe`'s
registry cell/ledger entry to plain `python3 plans/tb2_grader_probe.py --lane .` with
`entry_exit=1`, `entry_state=red`, evidence `ModuleNotFoundError: No module named 'Bio'`
(the cell already documents this exit). If instead the claims mean L2 to *look through*
`uv run` to an inner `python3 <script>` (as r54's `entry_mode_ok` did), the frozen text
should say so — and L2's `-c` clause must then still fire inside the looked-through argv.

## R4 (seat route e): two-span entry cell — parser binds first, authority ambiguous

Fixture `f2-twospan` (receipts `f2-twospan.*`): cell
`` `python3 plans/benign.py` (real driver `python3 plans/real.py`, do not run directly) ``.

- Ledger argv = first span → `PREDICATE R54-C2 pass`; the cell still advertises
  `plans/real.py` to any prose reader — the registry can point at a command the binding
  legs never check. (Observed.)
- Ledger argv = second span (truthfully matching the cell's second span) →
  `ARGV-DEFECT two-span: script mismatch` — the parser's first-match rule false-positives
  a truthful seat. (Observed.)

75/78 real cells carry extra backtick spans (flag docs) — convention is *first span =
the command*, but nothing enforces it. Frozen L1 says "the SKILL registry row's declared
entry command" without saying which span is declared. Correction, minimal and compatible
with all 78 real cells: L1 binds to the **first backtick span verbatim** and adds a
static leg — any `python3`/`python`/`uv` + `.py` (or `-m`) command pattern appearing
**outside** the first span of the entry cell is a defect (extra spans that are mere flag
names, e.g. `` `--lane` ``, stay legal).

## R5 (seat route d): evidence-fragment substring spoof — passes, no identity

Fixture `f4-evidspoof` (receipt): two red rows share one declared fragment
`BROKEN-BY-DESIGN-B`; `spoof_a.py` prints the other row's fragment and exits 1.
Observed: `PREDICATE R54-C2 pass`, `evidence_missing=0`. L4's check is `fragment in
stdout+stderr` — substring only, no row identity. A red row can print any row's
fragment, or pad output with fragments. Not a soundness kill (the row is truly red) but
a binding-leg weakness: the evidence is supposed to pin the *observed* failure to the
*declared* failure. Correction: add `duplicate evidence` leg (fragments must be unique
across the ledger) — cheap, catches the whole class; row-name tagging optional.

## R6 (seat route b): absolute interpreter path

Observed (`f5-absinterp.neutral.txt`): r54 `ARGV-DEFECT abs-gate: interpreter not
python3/uv`. Census: 0/78 real cells use absolute paths, so **strict-token L2 is free**.
Frozen text "argv[0] must resolve to a real interpreter binary (python3/python)" is
ambiguous: a basename-normalized or `shutil.which`-based check admits
`/opt/shim/python3` and `./python3` — and under R1's inherited PATH, *which* `python3`
`shutil.which` finds is itself caller-controlled. Correction: L2 = exact token,
`argv[0] in {"python3", "python"}` (keep `uv` rejected per R3's amendment), and
resolution-to-binary belongs to the exec path (R1), not the token check.

## R7 (seat route c): sibling swap / `__pycache__` — clean clone protects cross-row; symlink gap remains

- **Cross-row planting — defeated.** Fixture `f7-rowplant`: row `a-plants` writes
  `plans/planted.py` into the worker clone; row `b-consume` imports it. Observed:
  `LAUNDERED b-consume … exit=1` — `Worker.reset()` runs `git reset --hard` +
  `git clean -ffdx` before **every** row, and workers hand fresh `clone --shared` dirs.
  The clean-clone answer is: yes, protected, even under `--jobs` parallelism.
- **Sourceless `__pycache__`/`.pyc` shadowing — cannot shadow a tracked source**
  (CPython checks `row.py` before `row.pyc`), and `-m` is refused per R2. Only live if
  `-m` entries are admitted.
- **Tracked symlink → absolute foreign path — passes.** Fixture `f7-symlink`:
  `plans/row.py` committed as mode 120000 symlink to `/fast/scratch/…/f7-foreign.py`
  outside the clone. `PREDICATE R54-C2 pass` while the executed bytes are outside the
  reviewed tree — content provenance, not argv, is the binding target. Correction:
  static leg — the entry's script path must be a tracked regular file (reject symlinks,
  and resolve `../` escapes so the target stays inside the clone). Cheap; no real cell
  needs it.

## Recommended minimal leg additions (for the builder / L1)

1. Hermetic exec: `python3 -I`, scrubbed `PATH=/usr/bin:/bin`, no `PYTHON*` env vars.
   (Closes R1, hardens R6.)
2. Script-token rule: argv[0] exact ∈ {python3, python}; argv[1] (or the single script
   token) must be `<script>.py`, `-m`/`-c`/absolute-paths all defect. (R2, R6.)
3. Entry-cell rule: first backtick span is the sole declared command; interpreter+script
   command patterns elsewhere in the cell are defects. (R4.)
4. Evidence uniqueness across ledger rows. (R5.)
5. Entry file must be a tracked regular file inside the clone (no symlinks, no
   `..` escapes, no `.pyc`/extensionless). (R2, R7.)
6. Resolve the `tb2-grader-probe` contradiction by dated amendment (R3) before the
   after-run; do not paper over it with a uv look-through exemption.

Replay list at integration (runnable now via `driver.py`, receipts in `receipts/`):
`f6-envkill` under `PATH=<shimdir>:$PATH` and under `PYTHONPATH=<inject>` is the top
kill candidate; `f3-module`, `f2-twospan`, `f4-evidspoof`, `f7-symlink` probe L1–L4
respectively.

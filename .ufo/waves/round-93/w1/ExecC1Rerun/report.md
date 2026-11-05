# ExecC1Rerun — independent re-measurement of R93-C1 (round 93)

Seat: ExecC1Rerun (leaf executor, wave w1). Date: 2026-11-05. Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` (branch master). Scratch:
`/fast/scratch/hyaku/kengaku-r93/ExecC1Rerun` (removed before this report was yielded; all
receipts copied into this dir first).

## Verdict

**R93-C1 reproduces exactly.** In a `--shared` clone detached at the measured tip
T `22972a317185216596b3dfe1c189e98d1eb86787`, the frozen predicate re-ran live and printed the
frozen lines verbatim with exit 0; the L6 leg re-executed the full 8-case probe in a fresh
`git archive` extraction (~5 min wall) and matched the committed receipt observation-for-observation.
Both do-nothing controls behaved as the claims file freezes them (BASE rc 1, F rc 1). A
report-only portability probe driven by uv-managed CPython 3.13.16 also held all 8 vectors.
No instrument defect found; nothing to route except three info-level notes below. No claim flip.

## Environment (no tool installs or updates were made)

- `/usr/bin/python3` = Python 3.14.8 (this interpreter ran the counter, the probe drivers, and —
  inside bwrap — the grader harness and every `python3 interp.py` child).
- `bwrap` = bubblewrap 0.13.1 at `/usr/bin/bwrap`; sandbox smoke-tested ok; `/proc/sys/user/max_user_namespaces` = 122865.
- `uv` 0.13.0 at `~/.local/bin/uv` (pre-existing). For the portability run uv selected its
  **pre-existing managed** `cpython-3.13.16-linux-x86_64-gnu`
  (`~/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu`, symlinked at `~/.local/bin/python3.13`).
  Nothing was downloaded or installed by this seat; pacman untouched.
- Instrument hashes at T (clone HEAD, clean, `git status --porcelain` empty) — all nine match the
  frozen-instruments table byte-for-byte: probe `6fad5d52…`, case table `078b04d2…`,
  c1 counter `89153db6…`, freeze gate `18b01b42…`, c2 counter `ac0e26a5…`, forgeries
  `993ed3cf…`, `5138d354…`, `67d0b757…`, `54bf34a2…`. The frozen rule (no tabled instrument
  changed after F) holds byte-level at T.

## Runs (exact commands, all in `$S/lane` cwd, clone detached at the named rev)

1. **T — the claim itself** (18:16:29→18:21:27, ~298 s; L6 re-ran the probe fully):

   ```
   python3 plans/round93_c1_replay.py --lane $S/lane --rev 22972a317185216596b3dfe1c189e98d1eb86787 --work $S/w
   ```
   stdout+rc → `c1-rerun.txt` (this dir):
   ```
   LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass
   TARGET executed_rows=37 member=schemelike-metacircular-eval located=1 executed=1 cases=8 legs=40 mismatches=0 defects=0
   PREDICATE R93-C1 pass
   rc=0
   ```
   Identical to the frozen predicate string (executed_rows 37, cases 8, legs 40, mismatches 0,
   defects 0). L7 cells at T: timing-wall 4/9, subprocess-exec 14/45, stdout-inspection 12/29,
   file-artifact 28/76 — matches the claims' class-cell deltas.

2. **BASE `28e9f8bf4e8a68b1a34babfa71be9de595b78c4e`** (seconds; probe absent at BASE, so no rerun):

   ```
   python3 plans/round93_c1_replay.py --lane $S/lane --rev 28e9f8bf4e8a68b1a34babfa71be9de595b78c4e --work $S/wbase3
   ```
   → `c1-rerun-base.txt`: all nine legs fail, `TARGET executed_rows=36 … located=0 executed=0 cases=0 legs=0`,
   `PREDICATE R93-C1 fail`, **rc=1**. Matches the claims' do-nothing control (`controls/c1-base.txt`) exactly.

3. **F `d8d0a4b849f3d031a6ad5525e18611a097e08bfe`** (18:23:05→18:27:11, ~245 s):

   ```
   python3 plans/round93_c1_replay.py --lane $S/lane --rev d8d0a4b849f3d031a6ad5525e18611a097e08bfe --work $S/wf
   ```
   → `c1-rerun-f.txt`: `LEGS L1=fail L2=fail L3=fail L4=pass L5=fail L6=fail L7=fail L8=pass L9=fail`,
   `TARGET executed_rows=36 … located=1 executed=0 cases=8 legs=0`, `PREDICATE R93-C1 fail`, **rc=1**.
   L4/L8 pass at F (frozen table matches its own commit, as expected); the receipt is absent
   (L1) because it was committed after F, at T. Extra evidence inside L6: the live re-run at F
   itself returned rc 0 with 8 observations — the instruments' vectors hold even without a receipt.

4. **Portability probe, report-only (never a claim leg)** (18:27:22→18:31:19, ~237 s):

   ```
   uv run --python 3.13 --no-project python plans/round93_scheme_probe.py --lane $S/lane --work $S/w313
   ```
   → `probe-313.txt`: `mismatches 0`, **rc=0**, all eight `CASE … ok=True` lines:
   C01 `P,63,0,63,0`; C02 `F,0,63,63,0`; C03 `F,0,63,63,0`; C04 `F,19,44,63,0`;
   C05 `F,0,63,63,0`; C06 `F,0,1,1,1`; C07 `P,-,-,-,0`; C08 `F,56,7,63,0`.
   **Interpreter roles, stated precisely:** the *driver* (staging, bwrap invocation, receipt
   printing) ran under uv-managed **CPython 3.13.16**; the grader harness and every interpreter
   child (`python3 interp.py …`) ran under host **`/usr/bin/python3` = Python 3.14.8** inside the
   bubblewrap sandbox (receipt `HOST_PYTHON Python 3.14.8`). The 3.13 interpreter never executed
   grader code. The decisive legs C06 (60 s through-eval timeout, timeouts=1) and C07 (grader
   passes with no evaluator and no test programs) hold.

## Routed observations (info; per frozen rule, never repaired in round)

- **R1 — F-control L6 message is misleading.** At F the counter prints
  `DEFECT L6 rerun rc=0 obs=8 want=0 equal=False`; `want=0` is the observation count of an
  *absent* receipt, while the live rerun actually agreed with all eight frozen vectors. Exact
  command/output in run 3 above. Cosmetic; does not affect any verdict (rc 1 either way).
- **R2 — L6 rerun is spent even when it cannot pass.** At F (receipt absent) the counter still
  executes the ~4-minute probe re-run before failing on `bool(receipt["obs"])`. Wasted wall time
  in controls only; the T path needs it and is unaffected.
- **R3 — standalone probe reads the case table from the working tree, not from a rev.**
  `plans/round93_scheme_probe.py` does `(lane / TABLE).read_bytes()`; only the counter's L6 path
  is rev-pinned (`git archive` extraction). On a clean detached checkout (this seat, and the
  official run's `--lane .` form) working-tree bytes equal rev bytes; a dirty tree would decouple
  the probe's predicted vectors from the counter's L4/L8 rev-pinned checks. Informational.

## Discipline notes

- Only the seat's own wave dir and scratch were written; no lane mutation (no add/commit/stash/
  checkout/switch/reset/pull/push in the lane; clone+detach happened in scratch only). No sysctl
  touched. No subagents spawned.
- Scratch incident (ConnectorScope-23 deleted `/fast/scratch/hyaku/kake-r97`): different round
  namespace; this seat's `kengaku-r93` tree unaffected; acknowledged to the connector.
- Harness note for future seats: this session's shell aborts a command chain on the first nonzero
  exit (errexit-like); capture expected-failure rc with `if cmd; then …; else echo rc=$?; fi`.
  This delayed, but did not lose, any receipt: every run above was re-executed cleanly.
- Receipts in this dir: `c1-rerun.txt` (T), `c1-rerun-base.txt` (BASE), `c1-rerun-f.txt` (F),
  `probe-313.txt` (3.13 driver). Scratch removed after copying.

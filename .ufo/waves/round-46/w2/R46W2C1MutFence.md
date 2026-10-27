# R46W2C1MutFence — C1 fixture-fence mutation probe

Axes: calibration (detector sensitivity), evidence integrity (pristine baseline + restoration), contract fidelity (single-edit fence mutants; counter unchanged).

Isolated clone: `/fast/scratch/hyaku/kengaku-r46/R46W2C1MutFence/lane`; `git rev-parse --show-toplevel` = that path and `git rev-parse HEAD` = `42d5043afac952fcb43bf4798757785dd258cf85`. Fence bytes stayed pristine throughout: `sha256sum plans/fixture_fence.py` before and after = `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.

Detector invocation for baseline and each runnable mutant: `envelope.sh "$S/env" python3 plans/round46_c1_verify.py --lane "$S/lane" --work "$S" --jobs 8 [--fence "$S/mutations/mNN.py"]`; the counter's testing `--fence` override exercises an isolated, one-edit byte copy and leaves the pinned counter, fixture modules, and source fence intact. Every observed ENVELOPE end line says `unchanged`; this excludes invalid measurements. Baseline output: `PINS total=65 mismatched=0`, `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, `CALIBRATION advertised=32 contradicted=0`, `PREDICATE C1 pass`; exit 0. Baseline detector was valid.

| # | Single-edit mutant | Detector output / caught-by |
|---:|---|---|
| 1 | Drop `_argv` NUL check (line 164) | `PREDICATE C1 pass`, exit 0 — survived |
| 2 | Drop `_argv` CR/LF check (166) | `PREDICATE C1 pass`, exit 0 — survived |
| 3 | Drop placeholder check (168) | `PREDICATE C1 pass`, exit 0 — survived |
| 4 | Invert `_inside(raw,d)` comparison (171) | `PREDICATE C1 fail`; `REASON honest-not-admitted`; exit 1 — caught by HONEST leg |
| 5 | Change `os.walk(..., followlinks=False)` to true (183) | `PREDICATE C1 pass`, exit 0 — survived |
| 6 | Drop `_tree` directory symlink check (196) | Mutation setup error: source fragment occurred twice; not run, excluded from n |
| 7 | Drop `_tree` special-file refusal (214) | `PREDICATE C1 pass`, exit 0 — survived |
| 8 | Drop `_tree` hard-link refusal (216) | `PREDICATE C1 pass`, exit 0 — survived |
| 9 | Widen `GIT_TOP` with `commondir` (64) | `PREDICATE C1 pass`, exit 0 — survived |
| 10 | Widen `CFG_SECTIONS` with `include` (67) | `PREDICATE C1 pass`, exit 0 — survived |
| 11 | Drop config bare-CR refusal (235) | `PREDICATE C1 pass`, exit 0 — survived |
| 12 | Drop config non-ASCII refusal (237) | `PREDICATE C1 pass`, exit 0 — survived |
| 13 | Drop `_objects` symlink check (333) | Mutation setup error: source fragment occurred five times; not run, excluded from n |
| 14 | Drop `--lane` repo membership check (573) | `PREDICATE C1 fail`; `REASON refusals-not-clean,contradicted=1`; exit 1 — caught by REFUSALS/CALIBRATION |
| 15 | Drop required store-entry check (500) | `PREDICATE C1 pass`, exit 0 — survived |

Results: 13 valid one-edit mutants run; 2 killed, 11 survived. Mutation setups #6 and #13 did not run and are not counted. Thus `VERDICT: fence-mutants-caught-2/13`.

Receipt copy: `w2/R46W2C1MutFence/summary.txt` contains baseline, outputs and hash facts. No tool installed/updated. Scratch cleanup requested via the prescribed scratch guard.

VERDICT: fence-mutants-caught-2/13

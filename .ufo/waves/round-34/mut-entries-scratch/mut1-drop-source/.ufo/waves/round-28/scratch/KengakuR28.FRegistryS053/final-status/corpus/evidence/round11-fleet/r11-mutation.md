# Round-11 grader mutation battery (L2: MutationGrader, wave 2)

Target: repo-root `grader.py` (md5 at battery time
`daadce018b579718da9fec4dcabca86f`), the extended three-tree gate
(`python3 grader.py` → exit 0, `CHECKS n=280`; `--selftest` → S0–S6 ALL PASS).
Method: independent mutation testing — break one stored number at a time, run
the grader, record whether the expected check-id fires (KILLED) or not
(SURVIVED). Only SURVIVED mutants are findings.

Design discipline (all decided BEFORE the first mutation run):

- **No endpoint traffic.** The grader is hermetic/offline (draft header:
  "NEVER issues a request to 127.0.0.1:34113"). The battery only runs
  `python3 grader.py` variants; nothing else touches the network.
- **CLI-override copies.** M0–M8, M11 mutate copies under `/tmp/r11-mut/` and
  pass them via `--r8-jsonl/--r8-runlog/--r9-jsonl/--r9-md/--r11-jsonl/
  --r11-md/--r11-runlog`. Pins skip overridden paths by design
  (`check_pins` compares `abspath` against `DEFAULTS`), which is why the
  pin layer is exercised by M0 only implicitly (M0 copies are byte-identical,
  so pin outcomes are copy-invariant).
- **Guarded in-place swap for fixed-path sidecars.** `ordering.log` and the
  bundle files have NO CLI override (`check_r11_ordering` reads
  `R11_ORDERING`/`R11_SHA`/bundle paths from `REPO_ROOT` constants), so M9/M10
  temporarily swap the committed file: md5 before → backup copy → minimal
  byte edit → run → restore from backup → md5 after, asserted byte-identical.
  This swap protocol is dictated by the round-11 brief; the committed bytes
  end byte-identical (verified below).
- **One mutation per run.** Each M-run isolates one layer: record (M1, M2,
  M7, M8), analysis-markdown (M3, M4, M5), run.log (M6), ordering sidecar
  (M9), bundle sha (M10), cross-tree isolation (M11). Control M0 runs clean
  copies of all 7 CLI-overridable inputs.

## Pre-designed battery (written before execution)

| #  | Layer / file mutated (copy unless noted)                              | Mutation                                                                     | Expected exit | Expected check-id (primary)                          |
|----|-----------------------------------------------------------------------|------------------------------------------------------------------------------|---------------|------------------------------------------------------|
| M0 | none — clean copies of all 7 overridable inputs                        | control                                                                       | 0             | `VERDICT: PASS`, `CHECKS n=280 mismatches=0`          |
| M1 | results-r11.jsonl                                                      | flip stored `ok` true→false in first `A-CKPT710` graded record with ok==true  | 1             | `r11.replay.A-CKPT710.ok`                             |
| M2 | results-r11.jsonl                                                      | stored `nwrong` +1 in first `A-CKPT710` graded record                          | 1             | id containing `r11.replay.A-CKPT710.nwrong`           |
| M3 | analysis_r11.md                                                        | `PREREGISTERED VERDICT: ESTABLISHED` → `DIRECTIONAL`                           | 1             | `r11.analysis.verdict`                                |
| M4 | analysis_r11.md                                                        | paired diff line `+0.352` → `+0.452` (anchor `): +0.352 sd` — unique)          | 1             | `r11.analysis.diff.mean`                              |
| M5 | analysis_r11.md                                                        | Brier `0.153` → `0.154`                                                       | 1             | `r11.analysis.brier`                                  |
| M6 | run.log                                                                | SUMMARY `A-CKPT710: 21/64` → `22/64`                                          | 1             | `r11.summary.A-CKPT710`                               |
| M7 | results-r11.jsonl                                                      | delete one `filler` record (line 66)                                           | 1             | census id (`r11.census.fillers` first)                |
| M8 | results-r11.jsonl                                                      | change one meta `init` value (pid 201 `nails` 19→20)                           | 1             | `r11.meta.regenerate.init`                            |
| M9 | ordering.log (**in-place swap**, backup+md5-verified restore)          | `post-hash 2026-09-28T23:10:20Z` → `2026-09-29T23:00:00Z` (after first request_ts 2026-09-28T23:28:57Z) | 1 | `r11.ordering.hash_precedes_first_request` |
| M10| power_analysis_r11.md (**in-place swap**, backup+md5-verified restore) | append one space (sha256 drift vs `prereg-bundle.sha256`)                      | 1             | `r11.ordering.sha256.power_analysis_r11.md`           |
| M11| results-r9.jsonl (S3-style raw-digit bump, last fenced JSON block, first `A-MONO` raw) | r9-only mutation; r11 inputs clean                            | 1             | ≥1 `r9.*` id fired AND **zero** `r11.*` ids (isolation) |

Plus two whole-grader records:

| #   | Command                                   | Expected                                                        |
|-----|-------------------------------------------|-----------------------------------------------------------------|
| ST  | `python3 grader.py --selftest`             | exit 0, S0–S6 ALL PASS                                          |
| DET | `PYTHONHASHSEED=42 python3 grader.py` vs unset-seed run | exit 0 both; md5(stdout) identical                 |

PASS criterion per row: observed exit == expected AND primary id present
(M11: AND zero `r11.` mismatch ids). Any other outcome = SURVIVED mutant =
blocking issue.

## Executed results

The executor was `./corpus/evidence/round11-fleet/mutate_r11.sh`
(command run; it ran each listed mutation once, with outputs retained under
`/tmp/r11-mut/`). Every verdict below includes the command and observed
stdout result/footer. `fired` lists the mismatch ids observed.

| # | Command / mutation | Observed output | Fired id(s) | Result |
|---|---|---|---|---|
| M0 | `python3 grader.py --r8-jsonl /tmp/r11-mut/r8.jsonl --r8-runlog /tmp/r11-mut/r8.log --r9-jsonl /tmp/r11-mut/r9.jsonl --r9-md /tmp/r11-mut/r9.md --r11-jsonl /tmp/r11-mut/r11.jsonl --r11-md /tmp/r11-mut/r11.md --r11-runlog /tmp/r11-mut/r11.log` | exit 0; `CHECKS n=273 mismatches=0`; `VERDICT: PASS` | none | PASS (copy control; 7 pin checks intentionally skipped) |
| M1 | same command with mutated `--r11-jsonl /tmp/r11-mut/m1.jsonl` | exit 1; `CHECKS n=280 mismatches=1`; `VERDICT: FAIL` | `r11.replay.A-CKPT710.ok` | KILLED |
| M2 | same command with mutated `--r11-jsonl /tmp/r11-mut/m2.jsonl` | exit 1; `CHECKS n=280 mismatches=8`; `VERDICT: FAIL` | `r11.replay.A-CKPT710.nwrong` (plus expected derived-stat ids) | KILLED |
| M3 | same command with mutated `--r11-md /tmp/r11-mut/m3.md` | exit 1; `CHECKS n=280 mismatches=1`; `VERDICT: FAIL` | `r11.analysis.verdict` | KILLED |
| M4 | same command with mutated `--r11-md /tmp/r11-mut/m4.md` | exit 1; `CHECKS n=280 mismatches=1`; `VERDICT: FAIL` | `r11.analysis.diff.mean` | KILLED |
| M5 | same command with mutated `--r11-md /tmp/r11-mut/m5.md` | exit 1; `CHECKS n=280 mismatches=1`; `VERDICT: FAIL` | `r11.analysis.brier` | KILLED |
| M6 | same command with mutated `--r11-runlog /tmp/r11-mut/m6.log` | exit 1; `CHECKS n=280 mismatches=1`; `VERDICT: FAIL` | `r11.summary.A-CKPT710` | KILLED |
| M7 | same command with mutated `--r11-jsonl /tmp/r11-mut/m7.jsonl` | exit 1; `CHECKS n=273 mismatches=7`; `VERDICT: FAIL` | `r11.census.fillers` (plus census/analysis count ids) | KILLED |
| M8 | same command with mutated `--r11-jsonl /tmp/r11-mut/m8.jsonl` | exit 1; `CHECKS n=273 mismatches=12`; `VERDICT: FAIL` | `r11.meta.regenerate.init` (plus truth/replay/analysis cascades) | KILLED |
| M9 | `python3 grader.py` during guarded `ordering.log` timestamp swap | exit 1; `CHECKS n=280 mismatches=1`; `VERDICT: FAIL` | `r11.ordering.hash_precedes_first_request` | KILLED |
| M10 | `python3 grader.py` during guarded one-space `power_analysis_r11.md` swap | exit 1; `CHECKS n=280 mismatches=1`; `VERDICT: FAIL` | `r11.ordering.sha256.power_analysis_r11.md` | KILLED |
| M11 | `python3 grader.py --r9-jsonl /tmp/r11-mut/m11.jsonl` | exit 1; `CHECKS n=280 mismatches=1`; `VERDICT: FAIL` | `r9.replay.A-MONO.got`; **zero `r11.*` ids** | KILLED (isolation) |

M0's clean-copy run reports `n=273`, not the preregistered `n=280`,
because the grader intentionally skips all seven overridden-path pin checks.
The required default-path control was also run as
`python3 grader.py`: observed `exit 0; CHECKS n=280 mismatches=0;
VERDICT: PASS — stored evidence fully re-derives offline`. Thus both the
copy control and the full 280-check control pass; the difference is exactly
the seven documented pin checks, not a failed behavior.

## Kill rate

Mutation score for M1–M11: **11/11 = 100% killed**, 0 surviving mutants.
Including the M0 control row, the executed table has 12 rows; M0 is a
control and is not included in the mutation denominator. No blocking test
gaps were found.

## Determinism + selftest record

- Command `python3 grader.py --selftest`: observed exit 0 and stdout
  `[selftest] ALL PASS`; S0, S1, S2, S3, S4, S5, and S6 each printed PASS
  (S6: all known-value assertions hold).
- Command `python3 grader.py` (unset seed): observed exit 0,
  `CHECKS n=280 mismatches=0`, `VERDICT: PASS`.
- Command `PYTHONHASHSEED=42 python3 grader.py`: observed the same exit/footer.
  stdout md5 for both commands was
  `a98307a2762ec4a5b14bf0693e507106`; determinism PASS.

## End-state cleanliness proof

The script captured `git status --porcelain` before and after. The files were
byte-for-byte identical in both snapshots:
` M PROVINCE.md`, ` M SKILL.md`, ` M corpus/README.md`, ` M grader.py`,
the same untracked `__pycache__/`, `corpus/evidence/round11-fleet/`,
`corpus/evidence/round11-power/`, `corpus/knowledge/bench-arena-round11-power.md`,
and `corpus/lessons/round-11.md`. `diff -u status.before status.after` was
empty. The two guarded swaps restored exact md5s:

- M9 `ordering.log`: before/after
  `5d675d0bacc06039c978f504e4e049bf` / `5d675d0bacc06039c978f504e4e049bf`.
- M10 `power_analysis_r11.md`: before/after
  `8374751d230f172cf185a64bdb01adb0` / `8374751d230f172cf185a64bdb01adb0`.

The complete committed-file md5 manifest (`/tmp/r11-mut/md5.before` versus
`md5.after`) had an empty diff. No pre-existing committed file was left
modified by the battery.

## Known non-gaps observed while designing (not mutations)

- `r11.ordering.pre_le_post` intentionally still passes under M9 (pre
  23:10:20Z ≤ mutated post 2026-09-29T23:00:00Z), so M9 is expected to fire
  exactly the one ordering-time id.
- M8 cascades by construction: `_build_meta` recomputes `truth` from the
  STORED `init` (`states_along(m["init"], …)`), so an init bump also fires
  `r11.meta.regenerate.truth` and pid-201 replay/analysis cascades. The
  battery asserts only the primary id; the full fired set is recorded.
- M2's turn-7 record sits in the shared {7,10} checkpoint set, so the paired
  diff/t/obs-mean ids may co-fire with the primary replay id; recorded.

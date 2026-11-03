# ProbeReview — scoped findings (kengaku r67 w1)

Surgical correctness review of the frozen R67-C1 probe `plans/round67_c1_pipeline_probe.py` (357 lines, sha `32bacf1d…`, HEAD `dcc39ea3`). Read-only; full detail + commands in `w1/ProbeReview/review.md`.

**Predicate verdict: R67-C1 PASSES on committed bytes.** `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt` → `CHECK ok cases=6` / `PREDICATE R67-C1 pass` / rc=0. `py_compile` clean (run on a byte-identical scratch copy + `cfile=` redirect — the literal lane-path command would have written `plans/__pycache__/`; `PYTHONDONTWRITEBYTECODE=1` does not stop py_compile's explicit write).

## Must-fix (lane; frozen file, reported not edited)
- **M1** `check_receipt` accepts a receipt missing a VECTOR line — claims :23 requires six; missing-check :306-308 covers CASE-derived `seen` only. Observed: drop `VECTOR q6-unscaled-loss` → rc=0 `PREDICATE R67-C1 pass`. Fix: require exactly one CASE and one VECTOR per case in `CASES`.
- **M2** junit/case_sha binding skipped when a VECTOR line precedes its CASE line — gated on `if case in seen:` :287 with no else-defect. Observed: reorder `VECTOR q1-ref` before `CASE q1-ref` → rc=0, binding never checked. Fix: two-pass parse or `defect: VECTOR before CASE`.

## Should-fix
- **S1** duplicate CASE line silently overwritten (:275) → rc=0. Flag duplicates.
- **S2** extra unknown CASE line accepted (`CASE q7-fake …` → `CHECK ok cases=7` rc=0; unknown-case check only in VECTOR branch :283). Validate the CASE set equals `CASES`.
- **S3** `run_case` :190 calls `junit_outcomes` unguarded — unexpected testcase name/malformed junit → traceback rc 1, violating the file's own "exit 2, never a verdict" rule (:33-34); `check_receipt` guards the same call (:295-298). Wrap → `{"error": …}`.
- **S4** `receipt.txt` + `receipt.junit/` are **untracked** in git at `dcc39ea3` (`?? ` in `git status --porcelain -- plans/ corpus/evidence/round67/`) — the "committed" receipt of record is absent from any fresh checkout; track both paths.

## Nits
N1 GRADER line substring-matched not fullmatched (:263, extra-field mutant passes). N2 blocking flock no timeout (:206). N3 all six cases run before error inspection — up to 6×900 s under the port lock (:209-211). N4 `frozen=mismatch` with table-equal vec accepted (:277/:285). N5 `probe_sha()` self-referential to executing bytes (:258; equals committed here). N6 `--run --receipt <record>` would overwrite the committed receipt+junit (:213-215,:236).

## Verified clean
bwrap argv :152-177 (unshare-net/pid, die-with-parent, ro-binds /usr /etc venv case grader, /tmp tmpfs, clearenv, offline env; only writable host path is /ctl under `--work` — nothing under host /tmp); flock before port-busy, both inside the lock with all cases (:205-209), self-locking the contract's port-lock path; timeout=900 → SETUP/exit 2 before any receipt mutation (:180-182, :210-211) — never a verdict; junit outcomes re-derived from `receipt.junit/<case>.xml` and compared to VECTOR lines from committed bytes (:249, :295-305); malformed and missing lines yield named `CHECK defect:` findings, never tracebacks (mutants v5, v7 rc=1); FROZEN_TABLE :71-78 ≡ claims table ≡ receipt vectors (PPPP/FFFF/PPFF/PFPP/PPPF/PPFF, all `frozen=match`).

Evidence: 8 mutant receipts + record receipt preserved in `w1/ProbeReview/` (`receipt.observed.txt`, `receipt.junit/`, `mutants/*.receipt.txt`); scratch `/fast/scratch/hyaku/kengaku-r67/ProbeReview` removed. No installs. No edits to L.

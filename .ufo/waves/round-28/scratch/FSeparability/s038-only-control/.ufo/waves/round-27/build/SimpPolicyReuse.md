# SimpPolicyReuse — minimal `parser_policy_compare.py` (advise only)

**Axes:** reuse/novelty, operability (LOC), frozen-output fidelity, calibration (CP import only).

## Must not duplicate

- **Population + pins:** `build_population`, `_LAST` errors — `grader_perturb.py:187-256`, `POPULATION_SHA256 :29-34`.
- **Strata:** `format_class`, `FORMAT_CLASSES`, `FENCED_RE`, `BARE_RE` — `:20,35-36,54-62`.
- **Verdict given parsed JSON:** export **`grade_rec(rec, got)`** from `regrade`'s switch (`:259-276`); `regrade` = extract + `grade_rec`.
- **E0 extract only:** `_GRADER.extract_json_block` — `grader.py:121-134` via perturb `_configure`.
- **CP95:** `clopper_pearson` — `attrib_calibration.py:144-152` (`round-27-claims.md:52-53`).
- **Truth replay / routing:** stays inside `build_population`; instrument never re-walks jsonl.

No second pin table, `_expected_for`, `regrade` copy, or `betai`.

## ~20-line `POLICIES` (E0..E8)

Helpers (~60–80 LOC): `fence_blocks`, `pick_fence(first|last)`, `pick_bare(first|last)`, `fence_then_bare`, `strict_whole`, `decode_spans` (E7 first decode; E8 last top-level skipping contained starts — `claims.md:44-45`). Table = name + one-liner each; E6 regex per `claims.md:43`. E0 may call `extract_json_block` for byte-identical lane reference.

## Loop + output (~180 LOC)

`build_population` → exit 1 on errors; E0 must match every `stored_ok`. Per policy: `got = policy(raw)` (no raise), `ok = grade_rec(rec, got)`; agree/flip_pf/flip_fp/none, pass rates, 9×9 matrix, stratum + `(file,cell)` rates, `delta_pp` vs E0, CP on agree/n. Emit frozen `POLICY`/`STRATUM`/`CELLSHIFT` (max pp + one cell)/`MATRIX`/`TOTAL` (`claims.md:59-62`).

## Selftest (~50–70 LOC)

Micro-strings only (`claims.md:64-66`): E1↔E0 two fences; E2 fence leak; E4 whole JSON; E7 nesting vs wrong depth cap; E8 contained span; one each E3/E5/E6. Mutant must fail. Optional: E0 vs `extract_json_block` on 2 strings.

## Line budget: ~260–330 total (vs grader_perturb 842)

## YAGNI (safe to omit)

Wilson/leg-share; `_dedup_stats`/F-family machinery; per-record logs/CSV/cache/mp; Q1–Q8 in instrument; full cell-shift table (only max frozen); oracle in this file; `extract_json_block` for E1–E8.

**Integrator:** 15-line `grade_rec` refactor in `grader_perturb.py` — single grade authority.

**Installs:** none.

VERDICT: ~280 LOC instrument: import population/strata/CP, thin `POLICIES` over shared helpers, one `grade_rec` export; skip dedup/Wilson/logs/oracle/Q scoring.

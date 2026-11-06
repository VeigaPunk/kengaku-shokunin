# ReviewC2 — R97-C2 calibration review (round 97, wave 1)

Seat ReviewC2 · 2026-11-06 · BASE `4992cd0e` · freeze F `8d9d2713` · measured T `f1083da6`.
Method: isolated `--shared` clone detached at T plus a BASE worktree; the instrument's own parser,
detector and diff logic were **re-derived from scratch** (`.ufo/waves/round-97/w1/ReviewC2/indep_census.py`)
and additionally run against the lane itself via read-only `git show`. No lane mutation, no fixture git
writes outside my scratch.

## Verdict: **R97-C2 met.** Exact, not aesthetic.

Every frozen predicate line reproduced, the 44-row retype is a true calibration in both directions,
the census instrument is itself conforming, and C's file discipline is exact.

## Predicate and BEFORE reproduction

| Run | Command | Result |
|---|---|---|
| T | `python3 plans/round97_gate_selftest_census.py --lane . --rev f1083da6…` (clone at T) | `ROWS base=168 rev=171 removed=0 duplicate=0 cells_changed=0` · `GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0 scripts_changed=0` · `MISMATCH_TOTAL n=0` · `PREDICATE R97-C2 pass`, rc 0 — matches the frozen predicate verbatim |
| BASE | P1 census bytes, `--lane <BASE checkout> --rev 4992cd0e --base 4992cd0e` | `ROWS base=168 rev=168 …` · `GATES total=127 with_selftest=83 without=44 …` · `MISMATCH_TOTAL n=44` + the 44 named rows · `PREDICATE R97-C2 fail`, rc 1 — byte-identical to L1's `.ufo/waves/round-97/L1/c2-base.txt` |
| selftest | `--selftest --work <scratch>` | 8/8 cases ok, rc 0 — identical to `.ufo/waves/round-97/L1/c2-selftest-p1.txt` |

Frozen-instrument integrity: `plans/round97_gate_selftest_census.py` sha256 `a255e830…` matches the
frozen table at T (as do the other four instruments I hashed).

## Misclassification attack — no misclassification either direction

**The 44 (false-negative hunt).** With a deliberately wider net (`self.?test`, case-insensitive, any
context) every non-detector mention in the 44 entry scripts at BASE is one of: (a) checks of *other*
tools' receipt text — `defect-ledger`, `round35-hardening`, `round95-c2-counter`, `round36-c1-battery`,
`round41-c1-mutants` (round-34 SELFTEST receipt lines); (b) invocation of *another* script's
`--selftest` — `round46-c2` leg D runs `plans/anchor_line_check.py --selftest` (line 193), which is a
probe behavior, not a self-invocation mode of its own; (c) `freeze-integrity`'s in-process battery
label. Zero detector false negatives (a script with a real spelling would have matched the detector:
`retyped n=44 detector_false_negatives=[]`).

**`freeze-integrity` — strongest borderline case, correctly typed.** Its argparse
(`--lane/--freeze/--rev/--claims/--paths/--work`) exposes no self-invocation spelling; the module
docstring declares the 15-case battery runs "inside every invocation, in-process (no CLI skip
channel, no marker file, no child re-entry; round-92 M6/M10)". PROTOCOL §Gate standard, Self-test
(fleet-root `PROTOCOL.md`, verified verbatim against the instrument docstring): *"The flag spelling is
the lane's (`--selftest`, `--self-test`, `run_selftest()`) and the registry records it; a helper-only
or model-only self-check does not satisfy this clause."* A default-invocation battery is not a
self-invocation mode → `probe` is the truthful kind. Its own self-test cell says so:
"in-process battery, no flag".

**The 84 retained gates (false-positive hunt).** All 84 have code-level detector hits
(`gates_without_code_hit=[]`). The only hits adjacent to triple-quoted text are fixture-template
strings inside `round54_c2_entrytruth.py` / `round55_c2_entryargv.py` / `round55_c2_controls.py`;
each of those scripts also carries a real argparse `--selftest` + `if args.selftest: return
selftest()` dispatch (round54 :495–498, round55-entryargv :416–419, round55-controls :186–189). No
prose-only inflation of `with_selftest=84`.

**Detector vs PROTOCOL.** The docstring quote is faithful to fleet-root `PROTOCOL.md` §Gate standard;
the registry schema is this section's and the row enum is exactly `gate|probe` — "the registry's only
other kind" is PROTOCOL-defined, not invented. The census's own gate row is exemplary: it exposes
`--selftest --work DIR` and its 8-fixture selftest asserts exit code *and* finding-id per case,
exactly what the clause requires. Anti-gaming legs are real: DEMOTED catches retyping a
spelling-bearing gate, CELL-CHANGED catches cell forgery, SCRIPT-CHANGED catches spelling added to a
closed instrument (all exercised in the 8 selftest cases I re-ran).

## Diff discipline — exact

Independent cell-level diff of the registry (fresh parser): BASE 168 rows (gate 127 / probe 41) →
T 171 rows (gate 84 / probe 87); removed 0; added exactly 3 (`round97-sparql-probe` probe,
`round97-c1-replay` probe, `round97-gate-selftest-census` gate); **kind-only changes = 44, all
gate→probe; any-other-cell diffs = 0**; no probe→gate promotions. File-level BASE..T diff outside
`.ufo/waves/round-97/`: exactly the three candidate bytes + `corpus/evidence/round97/sparql-probe.txt`
+ `plans/round-97-claims.md` + the ten frozen P0/P1 grader/instrument files. **No old script
changed** — none of the 44 entry scripts, none of the 83, nothing else in `plans/` or `corpus/`. The
SKILL.md paragraph (line 773) states the claim accurately (44 rows, kind-only, successor-file rule,
Q79, round-96 rows `round96-c1-replay` / `round96-standing-battery` among the 44 — both present in
my BASE mismatch list).

## Findings

No S1/S2 findings. S3 observations (routed, not repaired):

1. **`--rev T` does not resolve literally.** No ref `T` (or `F`) exists in the lane; a literal
   `--rev T` exits 2 (`could-not-evaluate`). L1's own controls used explicit shas (e.g.
   `controls/c2-positive.txt` runs `--rev f915f4f1…`). Verifiers must substitute the measured sha or
   `HEAD` at master; the sha-stamped output then matches the frozen predicate. Execution note only —
   the claims define T as the sha.
2. **Probe semantics nuance (declared, sound).** PROTOCOL defines probe one-directionally ("A tool
   that cannot fail is a probe"); the 44 *can* fail. The SKILL paragraph declares the operative
   reading ("`probe` records that none carries a conforming self-test, the registry's only other
   kind"). Within the binary enum this is the only non-forging option and it is stated, not hidden.
3. **`round36-c1-battery` wording tension, byte-frozen.** Its self-test cell still reads "the battery
   is the self-test" while kind=probe. CELL-CHANGED discipline (other cells byte-identical) forbids
   touching it; the successor-file rule in the paragraph is the exit. Inherited, unchanged.
4. **Census coverage gap, unexercised.** SCRIPT-CHANGED watches only BASE *no-spelling* gates'
   scripts; a with-spelling gate's script could change without a census finding. Independent file
   diff proves no script changed BASE..T, so no live harm this round.
5. **Pre-existing 7-cell rows.** `round63-c1-pypi-probe`, `round63-gate-checks`,
   `round64-c1-kvstore-probe`, `round64-trio-sweep`, `round88-fixgit-probe` lack the `owner` column;
   identical at BASE and T (outside C2's cell mandate). The two gate rows among them have genuine
   `--selftest` cells and code hits.

## Residual risk and verification gaps

- C1's ledger flip, receipt and replay are out of my seat (ExecC1/ReviewC1 cover them); I only
  verified the C2-owned cells and rows.
- Spellings outside the detector's grammar (e.g. undashed `"selftest" == argv[1]` LHS form) would be
  invisible to the census; my superset sweep over all 44 and all 84 gate scripts found no such form,
  so there is no live false negative at T.
- The census population counts only `| \``-prefixed rows; a differently formatted row would be
  invisible. The registry section has exactly one heading at both revs and all data rows are
  backticked; my independent count matches the instrument (168/171).

## Evidence

`.ufo/waves/round-97/w1/ReviewC2/` — `census-T.txt`, `census-BASE.txt`, `census-selftest.txt`,
`indep-census.txt`, `indep_census.py`, `skill.diff` (full BASE..T SKILL.md diff).

Scratch `/fast/scratch/hyaku/kengaku-r97/ReviewC2` removed after the copy.

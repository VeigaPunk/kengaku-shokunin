# ScribeSkillRule — round 26 build (KengakuR26-2.ScribeSkillRule-4)

Scope: draft text only. No SKILL.md edit (the integration owner, KengakuR26-2, splices). Only this file was written.
Instruments not yet landed in the lane tree at this read: `plans/grader_perturb.py` and `plans/gate_timing_check.py` are absent (`ls plans/`). The rule and rows below follow the shared-interface contract in the assignment and must be checked against the landed `--summary` output before splicing.

## Findings

1. Numbering collision. SKILL.md:136 already holds a `15.` item, but it sits in "Benchmark anti-patterns" (:62–177). The Measurement-rules list is :403–476 (items 1–14). The new text is therefore **Measurement rule 15**, inserted after SKILL.md:476 and before the "Scope limit" paragraph at :478. Rule 14 is at SKILL.md:467–476 in the same style (bold title, "round N; QUALITY Qn" tag, interval gate, `Runnable:` line, provenance parenthetical).
2. Threshold derivation, measured (not recalled). `plans/attrib_calibration.py:clopper_pearson(k,n)` run from stdlib, bar 0.95, k = invariant count, n = applicable count:
   - 0 non-invariant records: PASS first at n = 72 (CP95 lower 0.9501).
   - 1 non-invariant: PASS first at n = 110 (lower 0.9504).
   - 2 non-invariant: PASS first at n = 142 (lower 0.9500).
   - 0 non-invariant: CP95 upper = 1.0 at every n, so FAIL is impossible.
   - 1 non-invariant: upper = 0.975^(1/n) ≥ 0.975 at every n, so FAIL is impossible at any n (bounded search n < 1200 found none; analytic form as stated).
   - 5 non-invariant: FAIL first possible at n = 6 (upper < 0.95). Both checks are bounded (an unbounded loop timed out once; rerun with a cap).
3. Registry anchor. The gate/probe table is SKILL.md:553–558; the last row is `state-assertion-check` at :558. The two new rows go directly after :558, before the paragraph at :560.
4. Lane-tree state read: SKILL.md rules 14 and the registry were read at the base tree. Sibling ScribeRepairRows may also touch SKILL.md; the splice must re-anchor by text, not line number.

## Draft A — insert after SKILL.md:476 (Measurement rule 15)

    15. **A grader's verdict invariance is an interval per perturbation family, never one pooled rate (round 26; QUALITY Q11/Q12).** Run the audit after any change to `grader.py`'s extractor or grade functions, before citing any number that depends on a grader verdict, and at round close. Each family is one edit to the stored `raw`: meaning-preserving (F1–F7, D1) or meaning-changing (G1–G2). Families are never averaged together. Read each `FAMILY <id> kind=<MP|MC> n=<n> k=<k> rate=<r> cp95=[lo,hi] verdict=<v>` line as: for MP, `k` = applicable records whose re-graded `ok` equals baseline; for MC, `k` = baseline-PASS records re-graded FAIL, out of `n` baseline-PASS. PASS = exact CP95 lower bound ≥ 0.95. FAIL = CP95 upper < 0.95. UNTESTED = 0 applicable records. INDETERMINATE = the interval straddles 0.95: the data do not decide the family, so it is reported as neither PASS nor FAIL. At this bar, 0 non-invariant records reach PASS only at n ≥ 72, 1 at n ≥ 110, 2 at n ≥ 142; a family with 0 or 1 non-invariant record can never be FAIL. A FAIL is a finding about the grader and leaves exit 0; exit 1 means only a pin or baseline inconsistency. Runnable: `python3 plans/grader_perturb.py --summary`. (`plans/grader_perturb.py`; predictions P1–P10 in `plans/round-26-claims.md` §C1; the knowledge entry `corpus/knowledge/grader-perturbation-audit.md` lands only under Q13.)

## Draft B — registry rows, insert after SKILL.md:558 (`state-assertion-check`)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `grader-perturb` | gate | `python3 plans/grader_perturb.py [--root DIR]` with `--summary` or `--json` (lane root) | `0` ran; population sha256 pins match and baseline re-grade reproduces stored `ok` on every population record · `1` pin/baseline inconsistency or selftest failure (`MISMATCH …`) · `2` usage. Family `FAIL`/`INDETERMINATE`/`UNTESTED` print as findings and do not change the exit code | `python3 plans/grader_perturb.py --selftest` (exit 1 on failure) | P1 record set from `corpus/evidence/round8-horizon/results.jsonl`, `round9-replication/results-r9.jsonl`, `round11-power/results-r11.jsonl`, `round12-ladder/results-r12.jsonl`, sha256-pinned in the script; oracle `plans/fixtures/r26/`; `clopper_pearson` from `plans/attrib_calibration.py`; `grader.py` extract/grade functions | none — repo bytes only; no network, no endpoint | kengaku |
| `gate-timing` | gate | `python3 plans/gate_timing_check.py --lesson <repo-rel lesson path> --commit <rev> [--repo DIR]` | `0` every `## Gate` admit row cites ≥1 second-seat report path that exists in that commit's tree and no generic seat reference stands as support · `1` a row fails (printed per row/cell) · `2` usage | none declared in the interface; Q13 red-before run `--lesson corpus/lessons/round-25.md --commit 8ea41f9` must exit 1 naming the Q10 cell; fixtures `plans/fixtures/r26/` | read-only git (`show`, `cat-file`, `ls-tree`) at the named commit; no working-tree reads | none — read-only | kengaku |

## Commands run (read-only; no endpoint; no installs)

- `ls plans/`, `ls .ufo/waves/round-26/build/` — instruments absent; build dir holds only `swarm-registry.json`.
- Read `plans/round-26-claims.md`, SKILL.md :403–476, :551–567, `~/.omp/agent/RULES.md`.
- `grep`-free threshold run: `python3 -c` with `sys.path.insert(0,'plans')` and `from attrib_calibration import clopper_pearson` (results in Findings 2).
- One unbounded search timed out (300 s) because a zero-error upper bound never drops below 0.95; replaced with a capped rerun.

## Installs

None. Stdlib `python3` only.

## Files written

- `.ufo/waves/round-26/build/ScribeSkillRule.md` (this file; in the kengaku lane repo).

VERDICT: Draft Measurement rule 15 (grader-perturb interval reading, n-thresholds 72/110/142, FAIL-impossibility facts) and two registry rows (`grader-perturb`, `gate-timing`) are ready for the integration owner to splice after SKILL.md:476 and :558; the two instruments are not yet landed, so the text must be re-checked against their real output before commit.

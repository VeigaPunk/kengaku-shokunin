# Receipt (c) — the cross-axis pattern between R95-C1 and R95-C2

## The pattern: a scalar verdict over inputs the instrument never exercised, and the round's answer — provenance of the verdict

**C1 (coverage).** The captured grader is six pytest functions over `/app/report.jsonl` plus an
import (`corpus/evidence/round95/graders/fix-code-vulnerability/tests/test_outputs.py:13-102`:
test_report_file_exists_example, test_vul_file, test_cwe_id, test_hkey_basic_cases,
test_hkey_error_cases, test_hkey_real_world_examples). Its pass/fail signal is silent about the
vulnerable code path it never calls: the P0 prediction C11 (claims doc, decisive legs) is that
patching only `_hkey` passes the whole file because *no function of the grader calls `_hval`* —
the grader passes a half-fix on an input (the `_hval` path) it never exercised. The probe's
answer is not a better pass/fail; it is verdict provenance: leg L8 observes *which file* the
grader's `from bottle import _hkey` actually resolved to
(`plans/round95_vuln_probe.py:65-66` HKEY_ANCHOR/HVAL_ANCHOR; predictions C15 extends this to
package shadowing), and C13 converts an over-strict fix from silent pass to observed error.

**C2 (calibration).** The round-94 counter passed all 14 false gates 5/5 because its verdict was
pass/fail over a fixture set that never exercised TREESAME merges, octopus side-edits, renames,
duplicate rows, spaced rows, battery concealment… — the exact classes the 14 forgeries exploit
(`plans/round95-false-gates.tsv` rows F1-F7b/X1/M01-M20). The round-95 answer is again
provenance: per-fixture polarity (`W2 <name> ok|RED rc=… want=…`,
`plans/round95_c2_counter.py:333`), PREDICATE-line/rc agreement (`pred_ok`, :124-128), a battery
DRIVEN red by three shared-function mutations (W3 BATTERY_PROBES :96-100), and mutant killing at
*designated* fixtures (W5 MUTANTS :76-87, `designated=` per mutant :414-419). The census then
requires the red to appear at the row's designated leg, not anywhere
(`plans/round95_false_gate_census.py:30-41` DESIGNATED map, `designated_red` :48-52).

**Shared shape, stated once:** both claims measure an instrument whose scalar verdict hides
*which input caused it*; both round-95 instruments add provenance observability — L8
import-resolution for the grader, designated-leg attribution for the census. And the residual
holes are symmetric:

- C1: L8 pins *file resolution*, not code-path exercise — the `_hval` path remains unexercised
  by the grader even under the probe (disclosed as C11; the probe observes it, the grader
  cannot).
- C2: `designated_red` credits *any* red at the designated fixture — see R95-O5.

## R95-O5 analysis — designated-leg theater (routed to round 96, non-flipping at T)

What is verifiably closed: the census scores the counter's own stdout
(`plans/round95_false_gate_census.py:117-122` captures only the counter process); the counter
passes gate stdout through ONLY via the SELFTEST echo — `re.findall(r"^SELFTEST .*$", out_a,
re.M)` then `print("W3 echo " + line)` (`plans/round95_c2_counter.py:360-363`) — so a false
gate cannot inject `^W2 <name> RED` or `^W3 fail ` lines into the census's grep space
(`designated_red`, `plans/round95_false_gate_census.py:48-52`). PREDICATE-line/rc agreement
(`pred_ok`) and the W3 red-line parse (`SELFTEST_LINE` with `ok<15`, :369-376) close the
print-what-the-judge-wants channel for the counter's *verdict*.

What is open: attribution of a red to the *named defect*. The counter emits the reason
(`W2 {name} RED rc={rc} want_rc={want_rc} summary={s} want={want_s} predicate_line_ok={p_ok}`,
:333) but the census greps only the `^{leg} RED ` prefix — the reason field is never parsed. A
held-out forgery that fails its designated fixture by any means — crash (rc ∉ {want, 2}), a
broad breakage, an rc remap on one fixture — earns `designated_red=1` and inflates
`FALSEGATES designated_red=` without exhibiting the defect the leg names (e.g. row
F7-spaced-row-dropped credited for a crash on `w2-spaced-row`, not for dropping the spaced row).
The 14 in-sample rows are unaffected at T (their designated reds are the real polarities per
P2 controls), so the frozen verdict does not flip; but C2's declared scope hands held-out
discrimination to this wave's census, and this class is exactly what a round-96 forgery would
ride.

Candidate census v2 (round 96; FROZEN RULE bars any in-round change): (1) parse the RED detail
and require the row's recorded polarity (`want=` tuple class or `predicate_line_ok=False`
class, both already printed); or (2) a per-row benign-twin negative control — the same gate on
a fixture that differs only in the named defect must stay `ok`, so red-by-any-means stops
crediting. Cost: one extra fixture run per row, inside the existing 8-wide pool. Improves
calibration; touches no C1 artifact.

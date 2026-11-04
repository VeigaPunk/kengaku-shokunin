# Round 83 — a first exact-file replay and the outside record bill

2026-11-04, hyaku run 15, attempt 1. L1 KengakuR83. Base `614f00559c75155ec100e945b3e8257b14fb7496`; freeze `6f076679931367d540c3897a4eafa0eca752e1d4`.
The two frozen claims are R83-C1 (coverage, first code-from-image offline grader replay) and R83-C2 (calibration, eight round-82 record mismatches). All timestamps in this round use UTC unless an explicit offset is supplied. The coverage score stays at its existing L0 cap, 7; calibration stays at 10. The outside review is independent and still owns admission.

## Gate

The L1 opened each source below on 2026-11-04. New rows are S267–S270. S265/S266 are existing rows whose missing round-82 Gate entries are corrected here, not counted as new rows. No frozen SOURCES cell is rewritten.

| id and decision | URL or own-work location | access date | located quote (each under 25 words) | reason / flip |
|---|---|---|---|---|
| S267 admit, A for grader acceptance semantics | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py | 2026-11-04 | :25: `assert output.strip().startswith("bee26a"), (` | The source itself supplies the prefix rule; :28-31 supplies equality. It does not prove model ability. |
| S268 admit, supersedes S262 annotation | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/tests/test.sh | 2026-11-04 | :26: “echo 1 > /logs/verifier/reward.txt” (4 words) | Recomputed whitespace-token count; reward output follows pytest status. |
| S269 admit, supersedes S263 annotation | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test.sh | 2026-11-04 | :20: “-w requests==2.32.4” (2 words) | The request dependency is two tokens, not one. |
| S270 reject, supersedes S264 rejection shape | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pyproject.toml | 2026-11-04 | HTTP response body: `404: Not Found` | Unreachable locator at this pin, not fabrication and not absence of packaging generally; flip: a revision carrying this file is opened and anchored. |
| S265 Gate correction (R82-V6) | corpus/evidence/round81/log-summary-date-ranges-probe.txt | 2026-11-04 | :1: “# tb2 log-summary-date-ranges grader probe (round 81)” (7 words) | Own-work receipt layout; source is the receipt, not an external URL. |
| S266 Gate correction (R82-V6) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/instruction.md | 2026-11-04 | :9: “Write a CSV file /app/summary.csv with the following structure (including the header):” (12 words) | The lane re-opened both documents; second URL below. |

S266's second document, opened 2026-11-04: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/vulnerable-secret/instruction.md . Located quote at :1: “The goal is to extract this secret key” (8 words). The complete line includes a backticked output path; this shorter verbatim substring avoids silently altering those bytes.

Independent spot-check of this round's admit and reject: not supplied by a lane-authored seat. The outside closure must record its own agree/disagree; no self-awarded discernment credit is taken.

SOURCES status/recheck/used-by changes to existing rows: none. New rows' used-by cells point to this lesson (and S267 to the new knowledge entry). Candidate instruction-only support for a solved-task claim is rejected: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/instruction.md, opened 2026-11-04, :1 “Implement the intended logic” — this is the ask, not an observed solution. Flip: an actual solution run against the task's input image, a separate claim not attempted here.

Assimilation: none. `considerthese/2026-10-26.md` proposal 1's burn-down supplies context already implemented in earlier rounds; proposal 2's standing TB2 admission counter is not implemented by another per-member instrument and is not claimed closed. The round-82 planned sweep divergence analysis and anchor-line parser blind spot remain backlog, not covert additions to this freeze.

## Corrections (R82-V1 through R82-V8)

These are dated corrections to round-82 filed bytes. The old report, LOG entry, SCORECARD entry and lesson remain historical records, unchanged.

- **R82-V1** — S268 supersedes S262 and S269 supersedes S263. Correct counts are 4 words for “echo 1 > /logs/verifier/reward.txt” and 2 words for “-w requests==2.32.4”. This supersedes the round-82 Gate/report's 6 and 1 annotations, not the underlying source admit. The repair check extracts and recomputes the new row quotes. Historical S262/S263 remain byte-identical to BASE.

- **R82-V2** — the round-82 report's after-census `26 W04` is superseded by `W04=27` at `a44b2f083ee8b4115aea64598646f4bd9e3c1470`. `corpus/evidence/round83/r82-census-after.txt` is the full historical registry run with COMMAND, REV and EXIT 0, not a present-day census renamed as an old one.

- **R82-V3** — `affected=6`, `unrecovered=2`, `recovered=4`. The six provider-interrupted identities named in the outside spot-check are SweepGateR82, SweepHarvestR82, ReviewerR82, CriticR82, MutationR82 and RegistryCounterR82. Two never recovered (SweepGateR82 and RegistryCounterR82); four later returned substantive results. This supersedes LOG/SCORECARD's “Five seats died”; provider-affected, final failed, empty output and nonterminal transcript are different categories. `corpus/evidence/round83/r82-seat-census.json` derives final output categories from the retained results; it does not invent provider-event counts from missing status fields.

- **R82-V4** — `82fe89d5dd29fa4c1bb8d85399d9e43442d1b862` added both `plans/round82_c2_closure_debt.py` and `plans/round82_c2_checks.py` (not c804dd41). Command: `git log --diff-filter=A --format='%H %s' -- plans/round82_c2_closure_debt.py plans/round82_c2_checks.py`. This supersedes round-82 LOG:3172 and the report's attribution for those two files; other files' attribution is not inferred from the same commit subject.

- **R82-V5** — README indexes `lessons/round-82.md`, `lessons/round-81-verifier-spotcheck.md` and `lessons/round-82-verifier-spotcheck.md` with three cells per rendered row. The prior malformed round-81 spot-check row now has its missing Pointer cell. The old SHONEN box 3's claim that the round-82 lesson was already indexed was incorrect.

- **R82-V6** — this Gate now explicitly enumerates S265 and S266, their opened locations, access dates and located quotes. S270 supersedes S264 with `REJECTED:` and `flip:` in teaches. It corrects the rejection's representation, not its original HTTP result. No S264 immutable cell is edited. “Corrections are new entries” applies to filed lessons too; the earlier in-place round-81 lesson edit was not a model to repeat.

- **R82-V7** — `selftest_declared=7 of 10`, not ten of ten. The three `none declared` exceptions are round37-c1-attribution, round80-c1-remint and round82-c2-checks. The ten added rows are log-appendonly, round37-c1-attribution, round66-registry-check, round80-c1-remint, round81-log-summary-probe, round81-vulnerable-secret-probe, round82-c3-sweep, round82-c1-plans-registry, round82-c2-closure-debt and round82-c2-checks. The check re-reads each row's selftest cell; the correction supersedes the round-82 report's SHONEN box 1, not the registry's truthful exceptions.

- **R82-V8** — the report's `~07:24Z` for RegistryCounterR82 meant `~07:24-03:00`, hence `~10:24Z`, after launch `09:26:48Z`. This is a local-versus-UTC label correction, not a remeasured event time. Round83 timestamps use UTC; no invented precise death timestamp is supplied.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| Repeated source annotation miscount | round-82-verifier-spotcheck.md §6 V1; frozen S262/S263 and round82 lesson :25,30 | Q50 existed but the round82 check's selected S265/S266 universe excluded new Gate annotations | S268/S269 supersede rows plus R83-C2 v1; the same check must fail on BASE, and its fixture mutates the new count. |
| Unretained historical census mistaken for current prose | round-82-verifier-spotcheck.md §6 V2 | Gate standard Two evidences / Q58 | Retain the full run at the actual historical revision; v2 counts W04 lines and rejects a changed count or absent receipt. |
| Conflating provider interruption with terminal output state | round-82-verifier-spotcheck.md §6 V3 | Q50; a five/six sentence disagreement was not checked | Separate affected=6/unrecovered=2/recovered=4 from machine-derived final output categories; v3 fails without the correction and receipt. |
| Commit-subject attribution rather than file history | round-82-verifier-spotcheck.md §6 V4 | Q50 | Derive additions per file with git --diff-filter=A; v4 requires the actual addition commit plus dated correction. |
| Index and Gate assertions preceding their actual rows | round-82-verifier-spotcheck.md §6 V5/V6 | corpus index-row contract / SOURCES rule1 | Add three-cell rendered rows and complete this Gate; v5/v6 fail against BASE. |
| Quantifier and timezone overclaim | round-82-verifier-spotcheck.md §6 V7/V8 | Q50 | Derive selftest cell counts, preserve exceptions, and state UTC conversion rather than transplanting local Z labels; v7/v8 require evidence-specific corrections. |

The runnable red-before/sensitivity receipts in `corpus/evidence/round83/` are the failable-fix evidence; prose alone earns no repair credit. Historical routed finding R82-F1 (`anchor_line_check.py` quote-shape blind spot) stays open and is not called repaired by these count annotations.

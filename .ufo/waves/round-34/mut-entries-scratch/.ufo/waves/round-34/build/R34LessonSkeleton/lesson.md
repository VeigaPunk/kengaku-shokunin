# Round 34 — TB2 evaluator audit, mutant-hardened counter, frontier step (2026-10-25, hyaku run 7)

Baseline `5022357cc69334e83b5a2f76c34daea440077a57`; frozen prereg `plans/round-34-claims.md` (freeze commit `adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae`). Round shape: one v2 wave, 64 seats (build + attack; final participation and role mix: **[fill from landed seat records]**).

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `terminal-bench-task-grader.md` | **[placeholder]** | Expected source rows S105/S106/S107; record landed row ids, located quotes, captured pinned files, final counter output, and index/coverage result. Flip/admission condition: all frozen C1 predicate clauses pass; otherwise record honest stop and exact failed clause. |
| Staged payload-absent row S091 | **[placeholder]** | Hand-check against NEC技報 capture; record exact located anchor or refusal reason. If admitted, renumber under S108 and cite the landed entry. |
| Staged payload-absent row S105 | **[placeholder]** | Hand-check against Internet Archive METI capture; record exact located anchor or refusal reason. If admitted, renumber under S109 and cite the landed entry. |
| `terminal-bench-release-identity.md` (package) | **[placeholder]** | Record PROVINCE scope, QUALITY Q1–Q8/Q21, coverage novelty, cited-row health, and admit/reject reason. |
| `toolathlon-grader-contract-2026-10-23.md` (package) | **[placeholder]** | Record PROVINCE scope, QUALITY Q1–Q8/Q21, coverage novelty, cited-row health, and admit/reject reason. |
| `provider-selfreport-eval-limits.md` | **[placeholder]** | Record whether verified rows S108/S109 are cited and entry clears its admission gates; give rejection/hold reason if not. |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| index-vs-HEAD | Round-33 lesson §Mistakes, `counter-strength`; frozen claim `plans/round-34-claims.md` §C2 | **[round-34 falsify evidence pointer]** | **[N8 / observed fix and outcome]** |
| heading-only | Round-33 lesson §Mistakes, `counter-strength`; frozen claim §C2 | **[round-34 falsify evidence pointer]** | **[N2/N7 / observed fix and outcome]** |
| width/newline | Round-33 lesson §Mistakes, `counter-strength`; frozen claim §C2 | **[round-34 falsify evidence pointer]** | **[N5/N6 / observed fix and outcome]** |
| token-co-occurrence | Round-33 lesson §Mistakes, `counter-strength`; frozen claim §C2 | **[round-34 falsify evidence pointer]** | **[N3/N4 / observed fix and outcome]** |
| class-recurrence | `considerthese/2026-10-25.md` proposal 2; `corpus/QUALITY.md` Q23 | **[round-34 finding and evidence pointer]** | **[record whether the recurrent routed-defect class was pre-registered and counter-guarded]** |
| own-round | **[freeze/landing lesson, evidence pointer]** | **[report or receipt pointer]** | **[observed correction; do not claim unobserved repair]** |

## Seat ledger

Wave shape frozen as one v2 wave, 64 seats, build + attack together, ≥25% attack roles, m_flash majority. Final role counts and reports must come from landed records; do not infer dispatch counts from the plan.

| wave | role mix | flash-majority / attack share | reports / dead |
|---|---|---|---|
| build + attack | **[landed role counts]** | **[observed counts and percentages]** | **[observed reports / dead]** |

Results/registries: **[landed artifact paths]**. Misrooted, missing, or otherwise exceptional reports: **[record exact evidence, or “none observed” only if checked]**.

## Assimilation record (operator directive, §10)

- Theme: **[admitted package theme(s), if any]**. Screen package entries individually against PROVINCE, QUALITY Q1–Q8/Q21, and new coverage-map ground; the Gate records each verdict and reason.
- **Renumber map (by document, never arithmetic):** staged payload-absent S091 → lane **[S108 if verified/admitted]**; staged payload-absent S105 → lane **[S109 if verified/admitted]**. Record collision proof, exact capture locations, located anchors, and final cited entry. Refused rows retain their refusal reason; source repo/register remain read-only.
- C1 rows: record landed S105/S106/S107 source identities and ≤25-word located quotes; `terminal-bench-task-grader.md` admission depends on the frozen predicate and final `plans/round34_c1_verify.py` result.
- `## Gate` records at least one admit and one reject if observed; if either is absent, state that explicitly rather than inventing a verdict.

## Round-34 disclosures

- C1 frozen predicate: `python3 plans/round34_c1_verify.py --lane .` → **[exact output, exit status, receipt/source]**. Pinned evaluator task is `protein-assembly` at `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; captured paths and byte verification: **[evidence]**.
- C2 frozen predicates: `python3 plans/round34_mutate.py` → **[exact `MUTANTS total=8 detected=8` result and exit]**; `python3 plans/round34_defects.py --lane .` → **[exact `checks=8 defects=0` result and exit]**; both selftests → **[observed outcomes]**. Four red-before receipts: **[paths and class-by-class red-before / green-after evidence]**.
- Census before → after: frozen `.ufo/waves/round-34/claims/census-before.txt` records exit 0 and 15 W04; after command **[exact command]**, output **[full or linked receipt]**, exit **[status]**. No numeric census assertion without its command/output.
- Sourced claim: C1’s source rows **[final ids, opened date, quote locations, entry]**. Mistake mining and considerthese proposal 2 / Q23: **[observed disposition and evidence]**; persistent `corpus/defects.jsonl` ledger remains named debt unless actually implemented.
- Tool installations/updates: **[tool, version, channel, reason, or “none” if verified]**. Other limits/deviations from frozen claims: **[evidence-backed disclosure]**.

VERDICT: lesson-skeleton-ready

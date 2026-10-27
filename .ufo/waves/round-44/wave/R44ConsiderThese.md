# R44ConsiderThese — considerthese ledger and the round-44 slot (scout, read-only)

Lane tip read: `5e3d3aa` (2026-10-26 20:27). Files read in full: `considerthese/2026-10-{19,20,21,22,23,24,25,26}.md` (8 files, 49,606 B).
Nothing in the lane was edited. Scratch `/fast/scratch/hyaku/kengaku-r44/R44ConsiderThese` (a `--shared` clone, used only for one read-only observe).

## 1. Every proposal, and whether a later round implemented it

All eight files carry a "proposals only / nothing acted on" heading (10-19, 10-20, 10-21, 10-22, 10-23, 10-24, 10-25, 10-26). 10-23 and 10-24 add "No movement" status blocks and re-list older ones. That makes 27 distinct proposals (4+4+4+3+3+3+3+3).
Status key: LANDED = the proposal's mechanism exists at the tip; PARTIAL = a named half landed or it lapsed; OPEN = no artefact. Evidence is a grep/ls at tip `5e3d3aa` unless a lesson line is cited.

| # | proposal (file:line) | status | evidence |
|---|---|---|---|
| 19-1 | bidirectional README↔disk index gate in `grader.py` (`2026-10-19.md:9`) | PARTIAL | closed by the one-off `plans/round24_census.sh` (`dead_index_rows 0`), not a `grader.py` check: `2026-10-20.md:9` ("a one-off script, not a standing gate"); `grep check_corpus_index grader.py` → 0 hits |
| 19-2 | `wip/` quarantine + TTL for unadmitted bytes (`:20`) | OPEN | no `wip/` prefix or `status: unadmitted` header in the tree; 10-20 `:10` "no TTL on WIP commits" (only QUALITY R3, "logged even on FAIL") |
| 19-3 | SCORECARD self-consistency pass (`:29`) | LANDED | `2026-10-20.md:11` "closed: scorecard_state_defects_open 6/6 → 0/6; D14 errata row" |
| 19-4 | `gt_predicate` field per attribution receipt (`:38`) | OPEN | `grep -ri gt_predicate` over SCORECARD/LOG/SKILL/QUALITY/lessons/plans/grader.py → 0 hits |
| 20-1 | make R1–R10 executable (`2026-10-20.md:16`) | PARTIAL | `plans/round_close.py` (r40) runs two legs only: order gate + sources census (its docstring: "the order gate and the registry census"); `gate_timing_check.py` (Q13/Q14), `gate_flip_check.py` (Q35). R1–R10 as a whole is not executed |
| 20-2 | archived source text + `quote_locate.py` (`:19`) | PARTIAL | located-quote machinery landed as `plans/pkg_gate.py` QUOTE_ROW / `plans/sources_adopt.py` (10-25 `:19-20` "quote-validating → citation-bound"); no committed per-source normalized-text extract tree |
| 20-3 | opencode-go stop-loss rule + cap petition (`:23`) | OPEN | `grep "unreachable-via-current-routes\|stop rule\|stop-loss"` → 0 hits; the cap-petition half became an L0 packet, see 25-3 |
| 20-4 | `verdict-agreement.tsv` (self vs outside) (`:27`) | OPEN | `corpus/evidence/verdict-agreement.tsv` absent (`ls` → no such file); the only hit is an unrelated sentence in `plans/round-27-claims.md:78` |
| 21-1 | re-score history under a hardened extractor (`2026-10-21.md:25`) | PARTIAL | `plans/parser_policy_compare.py` (r27): 15712 comparisons; 10-22 `:12-14` "mostly delivered", write-back into stored round records still missing |
| 21-2 | prior-art preflight block before freeze (`:35`) | OPEN | `grep -i preflight` over QUALITY.md and `plans/round-4*-claims.md` → 0 hits; 10-22 `:16-18` records the pattern repeating |
| 21-3 | seat-yield ledger + wave budget (`:44`) | PARTIAL | QUALITY Q19 (`corpus/QUALITY.md:186-194`) + `.ufo/waves/yield.tsv` exist, but `cut -f1 yield.tsv | sort | uniq -c` → rounds 29 (40 rows) and 30 (69 rows) only; the ledger lapsed after r30 while waves ran r31–r43. Q19's "cut a zero-yield family" rule is unexercised |
| 21-4 | blind forecasters (`:53`) | OPEN | `grep -i "blind forecaster"` → 0 hits |
| 22-1 | scratch untracked + content-addressed manifest + carrier-aware archive scan (`2026-10-22.md:27`) | OPEN | `.gitignore` is 2 lines (`.ufo/interactive-sessions/`, `__pycache__/`); `git ls-files .ufo/waves/*/scratch/` → 6876 tracked paths. `plans/scratch_guard.py` (r42) guards the host scratch root, a different problem |
| 22-2 | WebArena evaluator-error measurement (`:39`) | OPEN | no `false-pass` / evaluator-error tool; one hit in `plans/round-24-claims.md` only |
| 22-3 | resumable waves / `resume_wave` (`:49`) | OPEN | `grep "resume_wave\|resumable"` → 0 hits |
| 23-1 | cap closure debt; `closure lag` field (`2026-10-23.md:16`) | OPEN | `grep "closure lag"` → 0 hits. The debt was paid in practice (r29–r43 each have a `*-verifier-spotcheck.md`), but no rule blocks pre-registration |
| 23-2 | audit gate yield, red/green per gate per round (`:25`) | OPEN | `grep "gate yield"` → 0 hits; r40–r43 mutation-priced individual tools, not a per-gate red/green table |
| 23-3 | root `STATUS.json` (`:32`) | OPEN | `ls STATUS.json` → no such file |
| 24-1 | Actions workflow running the gates on every push (`2026-10-24.md:18`) | PARTIAL | QUALITY Q20 is the cheap half (an out-of-band gate run per landing, `corpus/QUALITY.md:196-233`); `ls .github` → no such directory |
| 24-2 | `as_of` / `revalidate_by` on every knowledge entry (`:27`) | PARTIAL | QUALITY Q21 (`:235-253`) says it is "the cheap half … does not add an `as_of` field" |
| 24-3 | 30–40 frozen demand-side questions (`:37`) | OPEN | `grep "demand-side\|frozen questions"` → 0 hits |
| 25-1 | model-diverse verification (`2026-10-25.md:34`) | OPEN | `corpus/lessons/round-33.md:67` "operator-side and not lane-actionable"; 10-26 `:31` still lists it open |
| 25-2 | one persistent defect ledger (a)(b)(c) (`:39`) | LANDED | (a) `plans/ledger_tip.py` r37, (c) `plans/tip_receipts.py` r38, (b) `plans/order_check.py` + Q30 r39, wired by `plans/round_close.py` r40; `considerthese/2026-10-26.md:24-29` and SCORECARD `:1229,:1362,:1400` |
| 25-3 | L0 decision packet for the coverage cap (`:46`) | LANDED | `corpus/lessons/round-33.md:65-67` "landed as an L0 decision-packet append (fleet `l0-questions.md`, commit `22d28422`)"; the cap itself is still the operator's |
| 26-1 | routed-findings burn-down (`2026-10-26.md:37`) | PARTIAL | see §2 |
| 26-2 | one standing TB2 admission counter + filler control (`:44`) | PARTIAL | filler-control half landed as V9 in `round42_c2_verify.py` (SCORECARD `:1775`, `plans/round-42-claims.md:80,110`); the standing `tb2_grader_admit.py` does not exist and `plans/round{36…44}_c2_verify.py` are nine per-round copies (234 → 554 lines) |
| 26-3 | batch TB2 sweep + stability rider (`:50`) | LANDED | `regrade=` column (r40, `plans/round-40-claims.md:79,106`) and the 89-task class histogram (`.ufo/waves/round-43/build/R43ConsiderThese.md`; LOG `:1331-1332`) |

Tally: **LANDED 4** (19-3, 25-2, 25-3, 26-3) · **PARTIAL 9** (19-1, 20-1, 20-2, 21-1, 21-3, 24-1, 24-2, 26-1, 26-2) · **OPEN 14** (19-2, 19-4, 20-3, 20-4, 21-2, 21-4, 22-1, 22-2, 22-3, 23-1, 23-2, 23-3, 24-3, 25-1). Not fully implemented = 23.
Operator-owned or out of lane reach (not dispatchable by the lane): 25-1, the cap ruling behind 25-3, and the credential rotation / history rewrite in the 10-22/23/24 lessons.

## 2. Proposal 1 of 2026-10-26 (routed burn-down): what is done, what is not

Done (r41–r43): `plans/routed_open.py` (rider, `plans/round-41-claims.md:122-128`), `corpus/routed-findings.jsonl`, `routed_open=<n> oldest_round=<r>` printed in SCORECARD round sections (`SCORECARD.md:1721,1804,1893,1915`).
Measured now (envelope, clean `--shared` clone at `5e3d3aa`; receipt `.ufo/waves/round-44/wave/R44ConsiderThese/routed-observe.txt`):

```
ENVELOPE start 20:36:34 cwd=/fast/scratch/hyaku/kengaku-r44/R44ConsiderThese
OBSERVE rows=60 mismatched=0
ROWS total=60 open=38 blocked=1 closed=21 refused=0
routed_open=39 oldest_round=39
SELFTEST 12/12
ENVELOPE end 20:36:36 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Ledger shape (python over the jsonl): 39 open+blocked rows by `opened_round` = {r39: 3, r40: 2, r42: 34}; **30 of the 39 carry a `check` command**, so a closing pass is machine-observable. No row is opened at r43 although `corpus/lessons/round-43-verifier-spotcheck.md:154-175` routes R1–R5 (R1–R3 are in the r44 claims; R5 "the lane's own routed limits" — V10 readable key, fences, 7/15 and 7/13 survivors, envelope mode-only blind spot — has no row).
Not done, the proposal's enforcement clause (`2026-10-26.md:41-43`): "the freeze refuse a new coverage claim while the oldest open finding is more than two rounds old." `grep -i "more than two rounds\|oldest open"` over QUALITY/SKILL/lessons/`round_close.py`/`routed_open.py` → only the printed line, no threshold, no QUALITY row, no `round_close.py` leg. At the r44 freeze the oldest open row is r39: age 5 rounds, and C2 (S138–S146) is a new coverage claim, so this round would have been refused had the clause existed. The round-44 claims (`plans/round-44-claims.md:122-128`) name no age rule.

## 3. Proposal 1 vs proposal 2 for round 44: verdict

Axes: (a) separability from the frozen C1/C2 (nothing frozen may change); (b) cost and risk; (c) closes a measured, still-open defect; (d) matches the lane's own r39 lesson (`2026-10-26.md:24-29`, "a tool that closes a proposal is not a tripwire until it has been mutation-tested and wired into the round-close path"); (e) the claims file's "at most one considerthese proposal lands" (`round-44-claims.md:122`).

| axis | proposal 1 (routed burn-down, remainder) | proposal 2 (standing TB2 counter) |
|---|---|---|
| frozen-surface collision | none. `routed_open.py`, `round_close.py`, `routed-findings.jsonl` are not in the frozen list; `round44_c1/c2_verify.py` mention `round_close.py` only in prose (`round44_c1_verify.py:102`) | the thing to replace is `round44_c2_verify.py`, frozen (554 lines, digest-pinned spec/gate/probe/dry). A new standing counter cannot touch it, so it adds a tenth parallel copy this round |
| size of the remainder | small: an `--max-age N --round R` check in `routed_open.py` plus one `round_close.py` leg or QUALITY row, red control = the live r39-oldest state, green = a closed/refused ledger; close the 30 check-carrying rows | large: one parametrised counter for 9 admitted graders, each with its own probe/receipt/captures; plus its own mutation pricing, which is exactly what r39 says a new counter needs |
| measured defect | 39 open rows, oldest 5 rounds, grew 5 → 10 → 52 → 39 across r41–r43 | per-round copy drift is real, but the filler hole is already closed by V9 (r42) and V1–V10 re-point cleanly (r44 `diff` vs r43 after renaming ≈ 315 lines, mostly the V11 addition) |
| fits the r44 frozen work | C1 (mutation-attributed tool kills) shows how to price the new check; the r43 §5 routed R5 can be given rows | the C2 admission of `feal-linear` is exactly what a standing counter would re-admit, so building it risks restating C2 rather than adding a result |

**Confirmed: proposal 1 (routed burn-down) is the better fit for round 44**, as the remainder only: the age-gate (refuse a new coverage freeze when `oldest_round` is more than two rounds behind the freeze round, wired into `round_close.py`, with a red control from the current ledger and a mutation pass in the r39 sense), plus a bounded closing pass over rows that already carry a `check`, plus rows for the r43 §5 R5 residues. Proposal 2's remainder is a refactor with a frozen-file collision this round; defer it to a round with no frozen C2 counter (its one cheap, measured part, V9, has already landed).
Caveats (not hidden): (i) the gate cannot be applied retroactively to the already-frozen r44 C2 — it binds the round-45 freeze, and this wave's burn-down is what would make it pass; (ii) any new gate must be mutation-tested before the lane calls the proposal closed (`considerthese/2026-10-26.md:28-29`); (iii) "at most one lands" — if the L1 prefers a no-code landing, the lowest-cost alternate is 21-3 (re-append the missing r31–r43 rows to `yield.tsv`, since Q19 has lapsed).

## 4. Lesson-ready block

> **considerthese ledger audit (r44 scout `R44ConsiderThese`, tip `5e3d3aa`, 2026-10-26).** Of 27 proposals in `considerthese/2026-10-19.md` … `2026-10-26.md`, 4 are landed, 9 partly landed and 14 have no artefact. Two landed halves lapsed or stayed cheap: the seat-yield ledger `.ufo/waves/yield.tsv` holds only rounds 29–30 (Q19, `corpus/QUALITY.md:186`), and Q20/Q21 are named "cheap halves" of the CI and `as_of` proposals (`corpus/QUALITY.md:230-253`). `2026-10-26.md` proposal 1 (routed burn-down) is built — `plans/routed_open.py`, 60 rows, `routed_open=39 oldest_round=39`, `--observe mismatched=0`, `--selftest 12/12` — but its enforcement clause ("refuse a new coverage claim while the oldest open finding is more than two rounds old", `2026-10-26.md:41-43`) has no threshold, no QUALITY row and no `round_close.py` leg; the oldest open row is 5 rounds old at the round-44 freeze. Lesson: a ledger that only counts is not a burn-down until something fails on age. Proposal 2 (standing TB2 counter) is deferred: its filler-control half is V9 (r42) and its remainder collides with the frozen `round44_c2_verify.py`.

## Files
- This report; `.ufo/waves/round-44/wave/R44ConsiderThese/routed-observe.txt` (envelope receipt, < 1 KiB).
- Tooling installed: none.

VERDICT: proposals-open-23-chosen-26P1

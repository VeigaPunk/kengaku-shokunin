# FP4Inventory — frozen P4 scope

Identity: KengakuR27.FP4Inventory; reviewer, **not** candidate writer KengakuR27. Scratch clone HEAD observed at `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`. I read the complete draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md`; the proposed canonical `corpus/knowledge/extraction-policy-comparison.md` is absent at this revision, so this is not an admission reread.

Scope: compare only the P4a–P4e frozen subgroups in `plans/round-27-claims.md:102-124` and Amendment 1 (`:173-186`) with `build/ScoutP4Locations.md` and the committed IDs. No whole-document/current-number coverage is claimed.

## Findings (by severity)

### High — P4a’s eight offline score tokens are reported as MATCH

- P4a promises every numeric token in the listed SCORECARD rows/sections against its receipt or command (`plans/round-27-claims.md:107-110`). Amendment 1 requires unmapped numeric assertions to remain visible as offline-unverifiable (`:184-186`).
- Independent inventory reports eight P4a score/verdict tokens offline-unverifiable: `SCORECARD.md:760` `7`×2, `:761` `8`×2, `:786` `7`, `:789` `8`, `:809` `7`,`8` (`.ufo/waves/round-27/build/ExecP4Inventory.md:4-5`). This is exactly 2+2+1+1+2=8.
- The committed P4a IDs are grouped at `plans/fixtures/r27/p4_assertion_ids.txt:1-9`. `state_check.py:2051-2066` derives `axis_scores` from the same SCORECARD; `:2153-2168`, `:2172-2187`, `:2255-2277`, `:2292-2308`, and `:2356-2379` compare the score tokens to those scores and emit ordinary MATCH/MISMATCH records, not OFFLINE_UNVERIFIABLE. `corpus/lessons/round-27.md:123-125` reports all 48 P4 rows MATCH except the single P4b supersession, so none of these eight is surfaced as offline by the checker.
- The raw inventory does expose the tokens, so they are not absent from that report. The gap is that the frozen checker calls same-document consistency a successful evidence-backed P4 match. Keep these eight explicitly offline (or explicitly exclude score judgments from P4a); do not count them as externally re-derived.

### Medium — the C2 “four numeric repairs” split is omitted

- The frozen P4a target includes every number in the C2 claim row and final measured outcomes (`plans/round-27-claims.md:107-110`). Scout enumerates “four” in the C2 row and again in the final outcome (`.ufo/waves/round-27/build/ScoutP4Locations.md:7,10`; `SCORECARD.md:761,791`).
- `state_check.py:2145-2187` checks only the total `5 P3 mismatches` against the receipt summary; `:2280-2308` checks base/final mismatch totals and other summary counts, but neither extracts or verifies the four-numeric/one-index breakdown. `p4_receipt_summary` parses only the one-line totals (`state_check.py:2032-2041`), despite the base receipt listing five individual mismatches (`corpus/evidence/round26-calibration/state-check-base-f11bffbf.txt:16-20`). Thus the grouped P4a C2 IDs can pass while the promised “four” assertion is wrong.

### Medium — P4c’s 139 total relies on an unsupported hard-coded `+3`

- The preregistration promises the 136/139 totals against the named wave specs, assignments and dead-seat records (`plans/round-27-claims.md:114-116`). Scout finds no recovery-reviewer roster among those sources and flags the 139 statement as overbroad (`.ufo/waves/round-27/build/ScoutP4Locations.md:24-26`).
- `state_check.py:2893-2926` computes `total_139 = total_136 + 3` using a literal constant; it does not derive the three recovery reviewers from a frozen roster/record. `P4c.round.total-139` therefore validates the lesson against its own asserted increment, not the declared evidence. Mark the increment/139 as offline-unverifiable or add an in-scope frozen source; the current MATCH is not independently supported.

## Totals and check performed

- Committed list: P4a9 + P4b8 + P4c11 + P4d14 + P4e6 = 48 P4 checks, plus one inventory-control ID = **49** (`plans/fixtures/r27/p4_assertion_ids.txt:1-49`; `corpus/lessons/round-27.md:121-124`).
- Independent raw inventory arithmetic is exact: 53+65+48+24+127 = **317** candidates and the eight offline tokens above (`.ufo/waves/round-27/build/ExecP4Inventory.md:4-8`). These are raw token/path/citation candidates, not 317 independent P4 IDs.
- Command: `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/state_check.py --summary --root /tmp/kengaku-r27-FP4Inventory` → `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3`; exit 0. Counts balance: 318+0+6+3=327. The command’s zero mismatches does not resolve the P4a/P4c evidence gaps above; round-27 reports P4 as 48 MATCH / 1 SUPERSEDED (`corpus/lessons/round-27.md:123-125`).

## Residual risk and verification gaps

- P4d explicitly freezes the population counts and family n/k pairs, not every adjacent statistic. CP95 bounds and nearby composite/stratum numbers are flagged as ambiguous/outside the named n/k target by `build/ScoutP4Locations.md:28-32`; I do not count them as a proven preregistration omission. Likewise, Scout flags extra timing/refusal/initial-spec values outside the named P4c subgroup (`:26`).
- No `lsp` device is mounted (`read xd://lsp` returned “No such tool”). Grep was used only to locate source blocks; findings above rely on direct reads, and no semantic caller/definition/diagnostics result is claimed. This seat ran the summary only, not `--selftest`.
- No installs or updates.

VERDICT: Advertised totals reconcile, but the frozen P4 result is not a clean coverage PASS: P4a scores are counted MATCH despite the independent offline classification, the C2 four-repair count is unchecked, and P4c’s `+3` has no authority in its declared target evidence.

## Follow-up (same seat, 2026-10-21) — integrated v4.1 reread

Method: copied the integrated `plans/state_check.py` and `plans/fixtures/r27/p4_assertion_ids.txt` from the lane working copy (jj change `mnrqnzpwttmt`, git `38f8d03f84d7`, on top of master `b5f62e5`) into my clone, then reread the code and reran. Gap: the quoted SHA `5db1…c30c` was not found in the lane git object store; the live integration is the uncommitted working-copy change, so I verified those bytes (jj working-copy commit ids churn per touch).

1. Score tokens — RESOLVED. `plans/state_check.py:356` adds `P4a.scorecard.score-tokens-unverifiable`; `:2440-2464` emits it OFFLINE_UNVERIFIABLE with the eight tokens grouped exactly as inventoried (C1 row 7,7; C2 row 8,8; C1 outcome 7; C2 outcome 8; revision 7,8; `token_total=8`), falling to MISMATCH if any group vanishes. Score equality was removed from the MATCH conditions of the c1/c2 rows and outcomes (`:2163-2170`, `:2255-2268`, `:2292-2305`, `:2365` records `unverified_score`/`unverified_score_tokens` only). Presence is guarded; truth is explicitly UNVERIFIABLE, per Amendment 1 (`plans/round-27-claims.md:184-186`).
2. Four-repair split — RESOLVED. `:2159-2181` parses individual `MISMATCH:` ids from `corpus/evidence/round26-calibration/state-check-base-f11bffbf.txt` and requires the numeric set to equal the four P3a/P3b ids (`:359-364`) and the index set the single P3e id (`:365-367`), plus the claim phrase `four routed numeric repairs plus missing spotcheck index` and outcome `Four numeric defects were already routed` (`:2294-2296`). Matches receipt lines 16-20 (4 numeric + 1 index).
3. Recovery 139 — RESOLVED. `:2944-2950` parses `corpus/evidence/round26-calibration/recovery-start.txt:4` (“Three bounded read-only recovery reviews dispatched separately”), `total_139 = total_136 + recovery_count` (`:2960`); missing/unparseable receipt yields OFFLINE_UNVERIFIABLE (`:2972-2978`). Added controls: dead entries carry unique name/agentId matched against falsify assignments (`:2879-2894`) and disjoint unique build/falsify id sets gate `total_136` (`:2951-2959`).

Bonus: `P4d.unmapped-numerics` (`:422`, `:3225-3248`, `:3444-3452`) discloses 48 adjacent audit numerics (family CP95 lowers, flip 17s, strata/interpretation tokens) as OFFLINE_UNVERIFIABLE “disclosed, not silently counted”, closing the residual-risk note in my original report.

Commands run in my clone: summary → `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`, exit 0 (318+0+6+5=329; 51 P4 ids = old 49 + the two new ids, `plans/fixtures/r27/p4_assertion_ids.txt:10,44`); `--json` exit 0 with the records quoted above; `--selftest` exit 0, “[selftest] ALL PASS … P3a–P3e and P4a–P4e red mutations”. No installs or updates; no live edit.

VERDICT (follow-up): All three original findings are resolved in the integrated code and confirmed by runtime output in my clone; totals reconcile. Retain only the verification gap that the quoted `5db1…c30c` is unobservable — the integration lives in the lane working copy (jj `mnrqnzpwttmt` / `38f8d03f84d7`), so L1 must still land it as a commit for SHA-stable evidence.
Follow-up correction: line 35 describes the first-pass review; this follow-up also ran `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/state_check.py --selftest` in the clone → `[selftest] ALL PASS`, exit 0. `--json` reported `P4a.scorecard.score-tokens-unverifiable` OFFLINE_UNVERIFIABLE with `token_total=8`, `P4c.round.total-139` MATCH with receipt count 3 / derived total 139, and `P4d.unmapped-numerics` OFFLINE_UNVERIFIABLE with 48 listed tokens. The result summaries are directly observed in the JSON extraction.
Identity note: observed facts are master `b5f62e5`, jj change `mnrqnzpwttmt`, and the current working-copy commit prefix `38f8d03f84d7`; the quoted `5db1…c30c` did not resolve in the lane object store. “jj working-copy commit ids churn per touch” above is [INFERENCE], not a tested explanation.

VERDICT: In my clone, all three original findings are resolved by the integrated working-copy code; summary, JSON records and selftest match the corrected behavior. Totals balance (329=318+0+6+5; 51 P4 IDs). The only gap is SHA-stable verification of the reported `5db1…c30c` snapshot, which I could not resolve; the reviewed working-copy bytes are the observed jj change `mnrqnzpwttmt`.

## Digest clarification

Correction to the prior SHA note: `5db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c` is a file SHA-256, not a Git revision. In my clone, `sha256sum /tmp/kengaku-r27-FP4Inventory/plans/state_check.py` returned exactly `5db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c`; it matches. No checks were rerun. The worktree-vs-landed caveat remains: this verifies the copied checker bytes, not a jj-helper landing or final committed-tree hash.

VERDICT: All three original findings are resolved and the supplied checker digest matches my clone. Runtime checks remain the previously recorded 329/318/0/6/5 summary and passing selftest. No claim that the integrated working copy is landed; final landing hash remains outstanding.
ATTACKS: round-25 lesson M27 (r24 C1-created `sources-registry` row counted by C2's `capability_rows`) — every pointer, the diagnosis, the class, and whether the named red run goes red.

Pointers resolve at tip 8ea41f9 (`plans/round-24-claims.md` unchanged since 94da19e: `git diff --stat 94da19e..8ea41f9 -- plans/round-24-claims.md` empty):
- `plans/round-24-claims.md:51` C1 "Capability row `sources-registry` enters only if every contract census command"; `:64` C2 "…and enters demonstrated capabilities"; `:73` `| C2.capability_rows | 0 | ≥1 |`. All three exist.
- `RevSeparabilityR24.md` = `.ufo/waves/round-25/build/RevSeparabilityR24.md` (bare name; no copy at fleet root). Its §1 cites the same lines; §2 documents the revert result; §4 proposes the awk check.
- `AXES.md` is fleet-root `/home/vgpnk/Projects/shokunin/AXES.md` (no lane copy): :30-32 "causally separable … distinct axes". Prose only confirmed — RevSeparabilityR24 §3 finds no r24-era QUALITY/SKILL rule.
- `QUALITY R13` landed: `corpus/QUALITY.md:106`, cites "corpus/lessons/round-25.md M27".

Diagnosis CONFIRMED, and the row under-cites: the r24 round report says it outright — `/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/kengaku.md:125` C2 census `capability_rows 0 → 3`, while `:201-202` C1 verdict says "the `sources-registry` capability entered with a clean census".
- Reproduced: base 99cf615 + census script → `C2.capability_rows 0`, `defects_open 6/6`; landed 94da19e → `3`, `0/6`. `git log -S'sources-registry' -- SCORECARD.md` → 94da19e (row created), 8ea41f9 (erratum R25-E1). `round24_census.sh:64` counts `## Capabilities` rows; `:68` closes D11 at ≥1.
- Source's own nuance holds: credit, not count — deleting the SCORECARD row leaves `capability_rows 2`, defects `0/6`. Row says "credited", consistent.

Class: `scope` is defensible only under `kaika-w1/mistakes.md:267` C10 "Write-scope / attribution"; the same vocabulary (:447-449) has `attribution`, and R13 is titled "one artifact, one claim" (attribution). `attribution` is the precise term; the row's class and its fix disagree in vocabulary. Minor, not a break.

Red run DOES NOT go red as written:
- `grep -n capability_rows plans/round-24-claims.md` → `73:` only (C2). The quoted token is not under both claims; C1 names the row (`:51`), C2 names a different string (`capability_rows`, `:73`). Loose `capabilit` matches both sections (r24=2, r25=2); strict `capability_rows|Capability row` gives r24=2, r25=0 — only the strict form is discriminative, and the row quotes neither command.
- No command, exit status, or receipt is named. CORPUS.md:179-184 requires the same command to exit non-clean with observed failure text; the row supplies only a factual observation of an old file.
- The fix's own check is green on the incident. R13 (QUALITY.md:106) checks "each claim's count re-run with the other claim's paths reverted … must not move". On 94da19e with `corpus/SOURCES.md` removed → `C2.capability_rows 3`, defects `0/6`, identical to the landing; even the row-level revert leaves `2`, `0/6`. A repeat of the breach passes R13 by construction (the counted row survives C1's file revert).
- The proposed strict awk check (RevSeparabilityR24 §4) was not landed in R13; R13's Check names paperwork only ("pre-registration names each claim's population and its freeze commit, and the report states the revert test result"). R13 also appears nowhere in `plans/round-25-claims.md` (only R1/R4 cited), so the fix landed post-prereg with no frozen red.

Fix's factual claims verified: `plans/state_check.py` at 8ea41f9:184-185 `SOURCES_BASE_MAX_ID = 26`, `:365` census over S001..S026; live `corpus/SOURCES.md` = 26 rows S001–S026 plus 12 later (S027–S038, excluded); `python3 plans/state_check.py --summary` → `assertions=236 match=232 mismatch=0 superseded=1 offline_unverifiable=3 … VERDICT: PASS`, exit 0; prereg :95-96 freezes C2 at 6180e4f. R13's "report states the revert test result" is untestable at tip: no kengaku round-25 report exists (lane `.ufo/reports/round-25/` absent; fleet holds kotodama.md only); only SCORECARD.md:670-671 + `corpus/evidence/round25-calibration/revert-test.txt`, which reports identical numbers both ways (green).

Caveat: the live tree is mid-mutation by peers (SCORECARD.md, plans/state_check.py, calibration receipts modified; `state-check-before-6180e4f-v2.txt` untracked). Every claim above was read from 8ea41f9 via `git show` or from `git archive` copies under `/tmp/k25w2-LessonM27/`; no lane file was written except this report.

VERDICT: PARTIAL — pointers, diagnosis, class and the freeze/S001–S026 claims hold; the named red run does not reproduce as written and R13's check passes on the incident itself, so the fix is not shown able to fail.
installs: none.

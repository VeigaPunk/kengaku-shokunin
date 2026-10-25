# TallyR03 — read-only hand tally, attrib-r21-impl-ds-trials.log (C1 oracle)

Scope: `corpus/evidence/attrib-r21-impl-ds-trials.log` (353 lines), grep/sed/awk only; no python,
no lane scripts, no network. Frozen-table sha in header `:4` = 9f0244bb…ba33c. File HAS a scored
block, so it is not trial-only.

## GT + scoring blocks (4)
- B1 `:130–174` GT read 2026-10-16T10:25:25Z; B2 `:176–220` 10:25:58Z
- B3 `:222–266` 10:26:11Z; B4 `:268–312` 10:27:01Z
- trailer `:314–353` seat adjudication (no new requests).

## Authoritative block (P1 rule = last)
B4 `:268–312`; the file states the same at `:316–318` ("AUTHORITATIVE SCORING SECTION: the LAST
\"## GT + scoring at close\" block above", PASS 20/20).

| GT leg \ pred | alibaba-token-plan | other | total |
|---|---|---|---|
| alibaba-token-plan | 20 | 0 | 20 |
| other GT legs | 0 | 0 | 0 |

scored n=20, correct=20, excluded=0 (`grep -c EXCLUDED` over `:275–294` = 0; `:312` "excluded": []).
Every row `:275–294` has gt_class=served, chain "1/alibaba-token-plan OK 200", correct YES.
bar=0.80, min scored n=20 (`:297`).

## Stored verdict lines (whole file)
- `:159` ACCURACY: 0/0 = 0.000 (bar 0.80, min scored n 20) -> FAIL
- `:205` ACCURACY: 0/0 = 0.000 (bar 0.80, min scored n 20) -> FAIL
- `:251` ACCURACY: 18/18 = 1.000 (bar 0.80, min scored n 20) -> FAIL   (min-n rule)
- `:297` ACCURACY: 20/20 = 1.000 (bar 0.80, min scored n 20) -> PASS
- score_summary verdicts: `:174` FAIL, `:220` FAIL, `:266` FAIL, `:312` PASS.
- No TARGET / BODY / STREAM TARGET verdict lines: `grep -nE '^(ACCURACY|TARGET|BODY|STREAM)'`
  returns exactly the four ACCURACY lines above.

## Exclusions / duplicates
- B4: none. B3 excludes T06,T10 as `EXCLUDED:AMBIGUOUS(2)` (`:247–248`).
- B1/B2 exclude all 20 as `EXCLUDED:UNMATCHED` (`:137–156`, `:183–202`); tables byte-identical
  (md5 82cee02a637b4e8c6b0d43fa43d4ad12) — duplicate block, outside P1 (last block only).
  B4 = B3 with T06,T10 restored (diff: 2 lines added, 2 removed).
- P1 effect: one sample, n=20, 0 excluded, 20 correct.

## Trial ids + request timestamps (2026-10-16 UTC; `=== [Tn/std]` / t0_utc)
T01 10:21:04.575Z  T02 10:21:08.688Z  T03 10:21:12.543Z  T04 10:21:16.382Z  T05 10:21:20.276Z
T06 10:21:24.141Z  T07 10:21:27.990Z  T08 10:21:31.888Z  T09 10:21:35.934Z  T10 10:21:40.070Z
T11 10:21:43.932Z  T12 10:21:47.844Z  T13 10:21:51.807Z  T14 10:21:55.680Z  T15 10:21:59.850Z
T16 10:22:03.820Z  T17 10:22:07.700Z  T18 10:22:11.685Z  T19 10:22:15.557Z  T20 10:22:19.434Z

Duplication: T01's stamp appears in no other attrib-r2[123] file (`grep -l` → this file only).
Ids restart at T01 in every file, so cross-file dedup must key on timestamps, not ids. Sibling r21
windows: ds 10:23:45–10:24:59 (20), glm 10:21:42–10:23:49 (22), impl-glm 10:22:32–10:24:31 (22).

## Discrepancies (documentation only; do not change n or scoring)
- `:351–352` says "first trial 10:21:00.575Z"; first record is T01 t0_utc 10:21:04.575Z (`:13`);
  grep `10:21:00` hits only `:351`. 4 s typo.
- `:128` last_request_utc=10:22:20Z vs last t0 10:22:19.434Z (`:122`) — completion rounding.
- One GT leg exercised only: recall 20/20, specificity untestable (no other-leg GT), per `:298`.
- C1 eligibility: n=20 ≥ power-ask 17; B3's 18/18 FAIL is min-n, not a wrong answer.

VERDICT: r21-impl-ds authoritative block `:268–312` = 20/20 PASS at bar 0.80/min-n 20, confusion
20×(alibaba-token-plan→alibaba-token-plan), 0 excluded; whole-file verdicts 159/205/251 FAIL,
297 PASS; one 4 s timestamp typo at `:352`. Installs: none.

# TallyR02 — independent hand-tally of `attrib-r21-glm-trials.log`

Method: grep/sed/awk only, no python, no lane scripts, no network. Target sha256
`aa6956065b58ba61a4fdce9c1e47e4bce13b1eeb280cf4c37f29f29e54cc08bb` (27818 B, 153 lines, no CRLF/NUL).

## A. GT blocks — ZERO

- `grep -c '## GT + scoring at close'` → **0**. Also 0 for `^(ACCURACY|TARGET|BODY|STREAM TARGET)` and 0 for
  `AUTHORITATIVE` (case-insensitive). Only `#` comment lines exist (1–6 header, 141–152 addendum).
- Authoritative block under the P1 rule: **none** (plans/round-25-claims.md:28–31: "files with no such block
  contribute 0 scored trials and are reported as trial-only"). No `AUTHORITATIVE SCORING SECTION` note in-file.
- So the requested fields do not exist here: scored n=0, correct=0, excluded=none stored, **no per-leg
  confusion table** (no GT column to key rows on), **no bar/min-n stored**, **0 verdict lines** (no
  ACCURACY/TARGET/BODY/STREAM TARGET). No `score_summary` JSON (count 0).
- Nearest scorable twin `corpus/evidence/attrib-r21-impl-glm-trials.log`: heading at :142, table :149–:170,
  verdicts :172 `GT counts {"devin":9,"zai":13}` / :173 `ACCURACY: 22/22 = 1.000 (bar 0.80, min scored n 20) -> PASS`,
  AUTHORITATIVE note :192 ("the single ... block above"). Not this file.

## B. Trial-only inventory (counted from `{"kind": "record"` lines)

- 22 records, 22 unique `trial_id` (1–22), 0 duplicate ids, std=20 err=2; predictions zai 13 / devin 9;
  exactly one non-200 response (T21, 400 `devin_shim_error`).
- First request `t0_utc` = **2026-10-16T10:21:42.025Z**; last = **2026-10-16T10:23:57.589Z**.
  Line 141 claims `last_request_utc=2026-10-16T10:24:04Z` — that is T22 *completion*
  (10:23:57.589 + wall 6.5394 s = 10:24:04.128), not a request start.
- Per-trial rows (id class t0_utc prediction status id_class):
  T01 std 10:21:42.025Z zai 200 eq-x-log-id      T02 std 10:21:47.092Z zai 200 eq-x-log-id
  T03 std 10:21:52.333Z devin 200 chatcmpl-uuid  T04 std 10:21:56.867Z zai 200 eq-x-log-id
  T05 std 10:22:04.045Z zai 200 eq-x-log-id      T06 std 10:22:08.657Z devin 200 chatcmpl-uuid
  T07 std 10:22:12.915Z devin 200 chatcmpl-uuid  T08 std 10:22:17.242Z zai 200 eq-x-log-id
  T09 std 10:22:27.099Z devin 200 chatcmpl-uuid  T10 std 10:22:31.244Z devin 200 chatcmpl-uuid
  T11 std 10:22:50.048Z devin 200 chatcmpl-uuid  T12 std 10:23:08.834Z devin 200 chatcmpl-uuid
  T13 std 10:23:13.144Z zai 200 eq-x-log-id      T14 std 10:23:17.572Z zai 200 eq-x-log-id
  T15 std 10:23:21.869Z zai 200 eq-x-log-id      T16 std 10:23:26.359Z zai 200 eq-x-log-id
  T17 std 10:23:30.657Z zai 200 eq-x-log-id      T18 std 10:23:40.020Z zai 200 eq-x-log-id
  T19 std 10:23:45.082Z zai 200 eq-x-log-id      T20 std 10:23:49.572Z devin 200 chatcmpl-uuid
  T21 err 10:23:53.735Z devin 400 other          T22 err 10:23:57.589Z zai 200 eq-x-log-id

## C. Duplication across files — must NOT dedup, must NOT cross-score

- Twin `attrib-r21-impl-glm-trials.log` carries the same 22 trial ids but is an **independent run**:
  0 exact `t0_utc` collisions, **0 shared `id_value`** (set intersection = 0), and T01–T04 differ
  (this file zai/zai/devin/zai vs twin devin/devin/devin/devin), i.e. zai was healthy here but 429-limited
  there. Distinct samples, so P1's identical-table dedup does not fire; this file nonetheless contributes 0.
- Provenance defect: line 1 says `# attrib-r21-impl-glm-trials` while the filename is `attrib-r21-glm-trials.log`;
  addendum :142–:152 identifies the writer as `trial-runner-B`. `corpus/knowledge/attrib-r21.md:442–443`
  already records it "Unscored at finalize time"; `:116` and `plans/attrib-r21-frozen.md:244` "PASS" is the
  freeze-order gate only, not an accuracy verdict. `corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md:141–147`
  records the same grep-exit-1 finding.
- Cross-pairing hazard (measured): pairing this file's 22 predictions against the twin's GT table yields
  agree=10, disagree=12 (T01,T02,T04,T06,T07,T08,T11,T12,T16,T17,T20,T21) — transplanting the twin's GT
  would fabricate a wrong verdict. This file's own journal GT was never read (header :5, :150–152).
- Blind-window overlap: the twin's GT sweep `--since @1792146147 --until @1792146311`
  (`attrib-r21-impl-glm-trials.log:143`) = 10:22:27Z–10:25:11Z, which contains this run's T09–T22 legs
  (10:22:27.099–10:23:57.589). Any GT assignment over that slice must pair by rid/chain, never by time window.

VERDICT: trial-only (22 trials, std 20/err 2, 10:21:42.025Z–10:23:57.589Z), zero GT blocks, zero verdicts, zero scored trials — contributes 0 to P1; the twin impl-glm block (n=22) is a separate sample, so no dedup and no GT transplant.
Installs: none.

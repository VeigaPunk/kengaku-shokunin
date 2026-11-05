author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 89 — non-author verifier spot-check and closure

Lane `kengaku-shokunin`, branch `master`. Round 89 (attempt 2, L1 `KengakuR89a2`). Report: `.ufo/reports/round-89/kengaku.md` (fleet repo, commit `5799dda8`, author `kengaku-shokunin <kengaku@shokunin.local>`). Lane HEAD measured: `c3f81f72495476db1f4e36706d2855347077fa36`. Frozen claims commit: `d1c4f1b04bb39d18967075974b5984238b7c97f7`. Base: `192e809d582ecbd544798cbc03da1666a0de23f7`.

Method: the integrator re-measured with plain commands over committed bytes (git, jq, grep, sha256sum, curl for the pinned external source). It did NOT execute the lane's gates (`plans/round89_c1_replay.py`, `plans/round89_claim_figures.py`); for those it verified the committed evidence transcripts only. The grading of the gates is therefore `evidence-verified`, not `re-measured`.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %s' -- .ufo/reports/round-89/kengaku.md` (fleet repo) | `kengaku-shokunin <kengaku@shokunin.local> 5799dda8… round-89: kengaku report` | ok |
| SHONEN heading, one line per box | `grep -n '^## SHONEN' .ufo/reports/round-89/kengaku.md` and read | heading at report line 91; four lines `[~]` with pointers | ok (no `[x]`) |
| Cited hashes are ancestors of the branch | `git -C kengaku-shokunin merge-base --is-ancestor <h> master` for d1c4f1b0, 0e6bb05f, 000b7d1c, 63d61d0f, a9b8a1a0, 07191241, 00462b59, c3f81f72 | all exit 0 | ok |
| Lane pushed, no ahead commits | `scripts/hyaku/jj-lane.sh state …/kengaku-shokunin` | `branch=master local=c3f81f72… remote=c3f81f72… ahead=0 behind=0 head=detached tracked=0 untracked=0` | ok |
| Lane working tree clean | `git -C kengaku-shokunin status --porcelain` | empty | ok |
| Report after the cited tip | report commit `5799dda8` vs tip `c3f81f72` | report commit is a later fleet commit; it cites the tip | ok |
| Prompt committed with template contract items | `git ls-files .ufo/prompts/kengaku-round-89.md`; grep for `Sources & frontier`, `Trend verdicts`, `SHONEN`, commit/push, L0 side channel | tracked; all items present (§4 report contract, §5 commit/push/L0) | ok |
| Dispatch digest (`.ufo/watchdog.log`, mutable) | `grep -n 'kengaku round=89'` | see §5 digest | ok |
| Wave dispatch | report says `w1` dispatched 05:10:10 with 11 seats; `w1-results.json`, `w1-spec.json`, `w1-dispatch.json` present in lane `.ufo/waves/round-89/` | files present (43867, 24906, 33212 B) | ok |
| Frontier census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | `kengaku ok …/corpus/SOURCES.md`, exit 0; only W04 duplicate-URL warnings (allowed) | ok |

Conformance defects (status-neutral, routed in §7): round-88 counter "1 of 3 red" in the report and "1 of 4 red" in SCORECARD and QUALITY Q67 disagree; the fourth control was never run at BASE.

## 2. Per-claim re-check

### R89-C1 — coverage (`polyglot-rust-c`)

Re-measured (plain, over committed bytes):

- Ledger at base and tip: `git show <rev>:plans/grader-population-ledger.json | jq` →
  - base `192e809d`: `members=88 executed=32`; `shell-exec` 1 of 6; `stdout-inspection` 8 of 29; `subprocess-exec` 10 of 45; `polyglot-rust-c` `unexecuted`.
  - tip `c3f81f72`: `members=88 executed=33`; `shell-exec` 2 of 6; `stdout-inspection` 9 of 29; `subprocess-exec` 11 of 45; `polyglot-rust-c` `executed` (receipt `corpus/evidence/round89/polyglot-rust-c-probe.txt`, round 89).
  - The diff against base is one row only (`polyglot-rust-c`, 7 lines). Matches the report.
- Probe bytes pin: `sha256sum plans/round89_polyglot_probe.py` → `03c202f5072e8aa55636592fed9c2fb64b6a7684ec853f8968428e73d50df898`; counter constant `TRUSTED_TOOL_SHA` at `plans/round89_c1_replay.py:46` equals it. Matches receipt `TOOL_SHA`.
- Grader pin: re-fetched `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-rust-c/tests/test_outputs.py` → `200 1638`, sha256 `baed5e4d0cc0e5809ff41a7df1815d18c65c708a3a3f264428e1cda11ce692f9`; receipt `SUBJECT_SHA` equal.
- Frozen table unchanged: `git diff --stat d1c4f1b0 c3f81f72 -- plans/round-89-claims.md plans/round89-cases.json` → empty.

Evidence-verified (gate not executed; committed transcripts read):

- BASE `.ufo/waves/round-89/L1/c1-base.txt` (lane repo): `TARGET executed_rows=32 member=polyglot-rust-c located=0 executed=0 cases=0 legs=0 mismatches=0 defects=4`, `PREDICATE R89-C1 fail`, `RC=1`. Matches the claim.
- Tip `.ufo/waves/round-89/attempt2/c1-tip-attempt2.txt`: `TARGET executed_rows=33 member=polyglot-rust-c located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0`, `PREDICATE R89-C1 pass`, `rc=0`. Matches.
- Failed first attempt-2 run kept verbatim (`…first-run-host-sysctl-0.txt`); environment-dependent (`max_user_namespaces` 0 then 122865). Disclosed by the lane (Mistake 5).

Verdict R89-C1: **verified on its frozen predicate** (evidence-verified for the gate; re-measured for ledger counts, pins and source). Residuals as the lane states: host-sysctl dependence; the counter is pinnable by one commit (the lane's own forgery limit, Sentinel F1). The tip is not such a commit: counter bytes at `00462b59` equal instrument commit `0e6bb05f`'s counter (not re-diffed by me beyond the ledger; treated as lane-stated).

### R89-C2 — calibration (Q66 counter-side, four round-88 attack fixtures)

Re-measured (plain):

- Frozen claims file and case table unchanged after freeze: empty `git diff --stat d1c4f1b0 c3f81f72` (above).
- Frozen Move element (d) "record table pinned to its blob sha at the freeze commit": `git show c3f81f72:plans/round89_claim_figures.py` reads the record table at the measured revision (`git show {rev}:{RECORD_TABLE}`, line 357); no blob-sha or freeze-commit pin exists (`grep -nE 'blob|sha1|sha256|freeze'` returns only the `git show`/`cat-file` plumbing and the `--freeze-records` writer). **Element (d) is not implemented.**
- Control name: frozen text `selftest-removed-from-path` (`plans/round-89-claims.md:50`); implemented as `selftest-in-path` (`plans/round89_claim_figures.py:546`). The control is an injected selftest failure inside the predicate path: a red fixture of the intended kind, with a changed name.
- Round-88 do-nothing on the three fixtures it was run on: `.ufo/waves/round-89/w1/ExecCtrlC2/round88-baseline.txt`: fixture a doctored-claimed `PREDICATE R88-C2 pass`; fixture b deleted-figure `PREDICATE R88-C2 pass`; fixture c doctored-key `PREDICATE R88-C2 fail` (red via `DEFECT F4-unparsed R87-C1:kv:defect`, not via the KNOWN check). The selftest-in-path fixture is not in that file.

Evidence-verified (gate not executed):

- `.ufo/waves/round-89/attempt2/c2-tip-attempt2.txt`: `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`, `DEFECTS n=0`, `PREDICATE R89-C2 pass`.
- `.ufo/waves/round-89/attempt2/c2-controls-attempt2.txt`: `CONTROL doctored-claimed red rc=1 …`, `CONTROL deleted-figure red rc=1 defects=7 …`, `CONTROL doctored-key red rc=1 …`, `CONTROL selftest-in-path red rc=1 …`, `CONTROL tip green rc=0`, `PREDICATE R89-C2-CONTROLS pass red=4 of 4 tip=green`.

Verdict R89-C2: **verified on its frozen predicate** (the predicate sentence in the frozen file, the counter line and the report are identical; the predicate does not include element (d)). The frozen Move overstates: element (d) and the control name are not as written. Both are routed (§7) and do not change the predicate verdict. The after-figure is unchecked by the counter (`ids=8` → `ids=9` at `plans/round-85-claims.md:106`; ReviewerR89b F6 — the lane's own disclosure, not claimed by the round).

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | improved | ledger 32 → 33 of 88 (plain jq, §2 C1); the 0–10 score is held at the L0 cap 7 (SCORECARD round-89 row) — the count moved, the score did not |
| calibration | improved | counter-side: round-88 counter 1 of 3 attack fixtures red → round-89 counter 4 of 4 red, tip green (committed transcripts); the 0–10 score is held at ceiling 10 by rule (SCORECARD) |
| depth | unchanged | `git diff 192e809d c3f81f72 -- SCORECARD.md` is a pure addition (27 lines, 0 deletions); no depth row touched |
| operability | unchanged | as depth; wave instruments attacked, not promoted (SCORECARD states held) |
| freshness | unchanged | as depth; S278 is a new source row, not a freshness re-verification of a knowledge entry |
| adjacency | unchanged | as depth; connector scan report-only |
| novelty | unchanged | as depth |

No axis harmed. No score cell was edited in place (SCORECARD diff is additions only).

## 4. Discernment spot-check (LEARNING.md)

The round's `## Gate` section admits one source (S278) and records no rejection row. Items sampled:

| # | item · decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| 1 | S278 · admit (tier A, member replay only) | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-rust-c/tests/test_outputs.py` (curl 2026-11-05) | agree | HTTP 200, 1638 B, sha256 `baed5e4d…92f9` equal to the row and the round-52 capture; line 19 is `assert polyglot_files == ["main.rs"], (` exactly; lines 24–25 `os.popen(...).read()` (no status check); `check=True` at 34 and 41. The row's characterization holds. |
| 2 | S276 · reject (row says REJECTED: same two-assert shape as S275, adds no class; pre-round row, not in this round's Gate) | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-leaderboard/tests/test_outputs.py` (curl) | agree | 200, 537 B, sha256 `b28f8fc8…3892cf` equal to the row; line 15 `assert lines[0].strip() == expected, "result.txt contains unexpected value"` (quote is 8 whitespace-split words; ≤25). S275 re-opened (200, 559 B, sha `e4e6b21f…`) carries the identical line 15, so the "same shape" reason holds. The rejection is logged with a flip condition. |
| 3 | ScribeR89 knowledge draft (`kengaku-shokunin/.ufo/waves/round-89/w1/ScribeR89/knowledge-draft.md`) · not appended this round | the draft's own cited S278 lines 30, 34, 37, 41, 44 (`subprocess.run` / `check=True` / assert) | agree with the deferral; disagree with the logging | The draft states `Admission state: second-seat re-read pending (R3)`, so the non-admission is a deferral with a stated reason, consistent with the lane's admission rule. The lesson's `## Gate` says only "none" and gives no reason; LEARNING requires each rejection/non-admission logged with its reason in the lesson. Routed (§7). |
| 4 | Lesson `## Gate` · no reject row | read of `corpus/lessons/round-89.md` `## Gate` (committed `c3f81f72`): one admit row (S278), census counts only, no rejection row | disagree | A round with a gate and no logged rejection gives no discernment evidence for rejects. Item 2 above is a pre-round reject, not this round's gate decision. Routed (§7). |

Spot-check for the new SOURCES row (S278): quote is 5 whitespace-split words (≤25) and re-located at line 19 of the re-fetched file: agree.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` exit 0, `kengaku ok`.

## 5. Dispatch and completion digest (`.ufo/watchdog.log`, copied 2026-11-05)

- `2026-11-05T04:29:19-03:00 launch kengaku round=89 pgid=2434151 driver=hyaku-inline attempt=1`
- `2026-11-05T05:21:27-03:00 lane-dead-no-report kengaku round=89; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-89/kengaku.md)`
- `2026-11-05T05:21:29-03:00 launch kengaku round=89 pgid=2313328 driver=hyaku-inline attempt=2`
- `2026-11-05T05:56:36-03:00 complete kengaku round=89; hyaku-inline attempt=2`

Attempt 1 (`KengakuR89`) dispatched wave `w1` and ended without a landed report; attempt 2 (`KengakuR89a2`) re-measured at tip and filed the report. Attempt-1 commits are inside the claim history (`d1c4f1b0` … `07191241`).

## 6. Trend verdicts

- **expansion: unchanged.** No `corpus/knowledge/` entry added (`git diff --stat 192e809d c3f81f72 -- corpus/knowledge` empty). One source row (S278) and one ledger member executed; the member counts as coverage, not expansion (LEARNING: expansion needs admitted entries on uncovered ground).
- **quality: unchanged.** Q67 appended to `corpus/QUALITY.md` (grounded in lesson Mistakes 1–2, a real control-fixture defect caught by the first run). No entry moved, so no quality movement is credited.
- **discernment: unprovable-but-better.** Improvement is real on the instrument side (round-88 counter 1 of 3 red → round-89 counter 4 of 4 red, tip green; Q67 is grounded in a lesson). Not credited as `improved` because (a) this round's own gate logs no reject and the non-admission reason sits only in the wave draft; (b) the counter pins are self-rewritable (Sentinel H1–H3; lane Mistake 9), so the controls are evidence about the counter at the tip, not tamper-resistance; (c) the lane's own before-count is stated two ways (§7).

## 7. Routed defects (for the lane's next round; none bars admission)

1. **Frozen Move element (d) unimplemented** (`plans/round-89-claims.md:43`; `plans/round89_claim_figures.py:357` reads the table at `rev`). Route to round 90 as a counter-side extension: pin the record table to its freeze-commit blob sha. The operator ruling on the frozen text remains open (L0 `kengaku | round-89`, `.ufo/l0-questions.md:319`); this closure does not rule on it.
2. **Control name drift**: frozen `selftest-removed-from-path` vs implemented `selftest-in-path` (`plans/round-89-claims.md:50`, `plans/round89_claim_figures.py:546`). Correct the name in the next round's SCORECARD/LOG note; do not edit the frozen text.
3. **Round-88 before-count stated two ways**: report and `round88-baseline.txt` say 1 of 3 red (the selftest-in-path fixture is not in that file); SCORECARD round-89 row and QUALITY Q67 say 1 of 4 red. Correct to "1 of 3 measured; the fourth not measured at BASE" in a correction entry (append-only), and state that the fixture-c red is a parse failure (`F4-unparsed`), not the KNOWN check.
4. **Lesson `## Gate` has no reject row and no reason for the ScribeR89 non-admission.** Add a rejection/deferral row with its reason (the draft's `second-seat re-read pending (R3)`).
5. **Lesson Mistake 9 has `Captured-by: none`** while L9 (probe pin) is the only defence in the committed tip; the Sentinel forgeries are scratch-only. Keep as routed.
6. **SCORECARD C2 row**: states the record table "pins the claim population at commit B"; the blob-sha pin of element (d) does not exist. Add the limitation to that row.

## 8. Operator note (not a lane decision)

SHONEN boxes: all four are `[~]` with pointers. A non-author could check box 1 (SKILL.md decision tables, cited sources) and box 3 (executable without oral context) from committed bytes; box 2 (end-to-end task logged) has LOG.md:3398 and the replay transcripts; box 4 (PROVINCE.md accurate) was not checked by the integrator. Promotion is operator-owned: no `[x]` written here.

## 9. Integrator verdict

Both claims verify on their frozen predicates; no axis harmed. Admitted, with routed defects §7 and the operator ruling on frozen text still open. The lane's self-hold ("admission held on the operator ruling") is not a protocol rule; the integrator rules admission on the predicate and records the unimplemented element here.

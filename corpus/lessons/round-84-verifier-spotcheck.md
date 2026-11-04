# Round 84 verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Subject: kengaku round 84. Reviewed lane base `4087b2f8369fb0c317a8460725a607681ff2fd7f` → delivered `b8c10ad5e864fbb891bb88479afb0feadc25ed77`; fleet report `.ufo/reports/round-84/kengaku.md` at `497fe64bbd84e151162adf76c5e98cffc6d5b435`. This is a non-author closure. No lane gate, probe, selftest, mutant or bubblewrap capture was executed by this review; committed evidence was inspected under the PROTOCOL §Gate standard.

## Closure

Status **ok**, admitted **false**, verdict **rejected-honest-stop**.

The report is real, lane-attributed and names landed work, so the lane-round is `ok`, not a marker. R84-C1 verifies on its frozen predicate. R84-C2 does not: at the measured tip `q1=0 q21=0 q13=1 defects=1`, `PREDICATE R84-C2 fail`, exactly as the lane reports. The lane did not narrow the frozen target after the fact, did not fabricate a `falsify/` wave to satisfy Q13, and held the entry. No owned axis is harmed by the round's landed bytes. Because a declared claim is unmet, the round is not admitted.

No exploratory claim was declared, so no `unprovable-but-better` judgment arises. No capability row, promotion or mint is claimed.

## Step-1 conformance

- **Report attribution and order.** `git log --format='%an <%ae> %cn <%ce> %H' -1 -- .ufo/reports/round-84/kengaku.md` → `kengaku-shokunin <kengaku@shokunin.local>` author and committer, `497fe64bbd84e151162adf76c5e98cffc6d5b435`; committer time `2026-11-04 16:23:15 -0300`, after lane tip `b8c10ad5` (16:22:16) and before the driver `complete` line (16:23:52). The report is committed by the lane identity.
- **SHONEN heading and marks.** `grep -c '^## SHONEN' .ufo/reports/round-84/kengaku.md` → `1`; `grep -c '^- \[~\]'` → `4`; report has no `[x]`. `kengaku-shokunin/SHONEN.md` still has four boxes, zero `[x]`, and `git diff 4087b2f8 b8c10ad5 -- SHONEN.md` is empty. The four assessments point at `SKILL.md`, the round-84 evidence, the registry rows and `ConnectorR84/overlap.md`.
- **Cited lane commits.** `git -C kengaku-shokunin merge-base --is-ancestor <hash> master` exits 0 for all seven cited hashes: `b12a9d46806cb8d69fe48fac0f4efff0b266e4c2`, `767c907b7782ccf5d9e55395d3dac006226ad150`, `8a61bce1bd7a24d7e17c942139091d7c9abcf347`, `d1dc1cd9805829a0ee09ad00726560320675733a`, `394641e3d811b15583fba776d3886b59c32c1b1b`, `a8418a593225ec6804d5981143613cd65c4cb87c`, `b8c10ad5e864fbb891bb88479afb0feadc25ed77`. The base `4087b2f8` is also an ancestor.
- **Lane state.** `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kengaku-shokunin` → `branch=master local=b8c10ad5e864fbb891bb88479afb0feadc25ed77 remote=b8c10ad5e864fbb891bb88479afb0feadc25ed77 ahead=0 behind=0 head=detached tracked=0 untracked=3`. It is pushed and has no tracked modifications.
- **Uncommitted round evidence (defect).** `git -C kengaku-shokunin status --porcelain -uall` lists four untracked files: `.ufo/waves/round-84/w1-results.json`, `.ufo/waves/round-84/w1/CriticR84.md`, `.ufo/waves/round-84/w1/CriticR84/critique.md`, `.ufo/waves/round-84/w1/CriticR84/report.txt`. Two are cited as evidence in the report (`w1-results.json` for the 12-seat settlement and `CriticR84/critique.md` for the critic verdicts). Under landed-means-committed they are not evidence at closure; see routed defect R84-V1.
- **Dispatched prompt.** `.ufo/prompts/kengaku-round-84.md` is committed (`7bc92789500e37781f2931950e657de32912a705`, 793 lines) and is an ancestor of `origin/master`. Its 140-line prefix equals the rendered `templates/round-prompt.md` except two substitutions: the resolved working directory on line 1 and the resolved axis string on line 6 (`diff -u` shows only those two lines). §6 hyaku addendum follows. The five child-lane items are present: report path/filename, commit-before-report ordering ("The report lands last and cites the pushed lane hash"), the `## SHONEN` heading requirement, the commit-hash citation rule, and lane write scope. The round-level contract is present: MISSION/AXES binding, 1–3 claims, L2 floor (≥8 subagents in one batched call), commit-then-push, push scope, L0 side channel. The run-15 route text defers to `task.agentModelOverrides`; no raw model is passed by the lane.
- **Wave shape.** `.ufo/waves/round-84/w1-spec.json` has 12 items: executor 3, scribe 2, reviewer 2, scout 1, connector 1, critic 1, mutation-tester 1, sentinel 1. Attack seats (reviewer ×2, critic, mutation-tester) = 4/12 = 33 %, above the 25 % floor; one connector, at most two; one v1 wave in the 8–16 band. The registry names the same 12 seats. The untracked `w1-results.json` contains 12 results, all `status: ok`; a committed equivalent is missing (R84-V1).

Dispatch/termination digest (durable copy of mutable `.ufo/watchdog.log` lines):

```text
2026-11-04T15:32:55-03:00 launch kengaku round=84 pgid=508145 driver=hyaku-inline attempt=1
2026-11-04T16:23:52-03:00 complete kengaku round=84; hyaku-inline attempt=1
```

The lane tip `b8c10ad5` (16:22:16) and report `497fe64b` (16:22:31/16:23:15) both precede the completion line. No stale-lane condition: the launch and completion are under one hour apart, and the lane files its report.

## Claim rechecks: measured versus evidence-verified

### R84-C1 / coverage — met on its frozen predicate; coverage improved (score 7 held at the L0 cap)

Independent plain measurements over committed bytes, using `git show REV:path` (no mutable worktree file):

- `plans/grader-population-ledger.json` parsed at BASE and tip: BASE members 88, `executed=27 unexecuted=61`; `gcode-to-text` is `status=unexecuted`, `reason=unattempted`. Tip members 88, `executed=28 unexecuted=60`; `gcode-to-text` is `status=executed`, `round=84`, `receipt=corpus/evidence/round84/gcode-to-text-probe.txt`, `subject=tb2-header`, `verdict=predicate`. The file-artifact class moved 19/76 → 20/76, and no other member's status changed.
- `git cat-file -e 4087b2f8:corpus/evidence/round84/gcode-to-text-probe.txt` exits 128 (absent); the receipt exists at the tip.
- The receipt has eight `CASE` lines. `awk` over predicted/observed pairs gives `cases=8 predicted_P_legs=9 mismatches=0`; `grep -E 'cases=|PREDICATE R84-PROBE'` prints `cases=8 mismatches=0` and `PREDICATE R84-PROBE pass`; `LANE_TIP 767c907b…`, `WORKTREE clean`, `EXIT 0` are present. Sixteen legs are two per case, with no mismatch.
- The eight vectors are re-derivable from the pinned grader: `/app/out.txt` presence is the first function (`:6-10`), stripped exact equality with `flag{gc0d3_iz_ch4LLenGiNg}` is the second (`:13-19`). `empty`/`uppercase`/`suffix`/`prefix-only`/`wrong-flag` produce the `P/F` vector; `missing` is `F/F`; `exact`/`padded` are `P/P`.
- SHA256 over committed bytes: the capture `corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py` is `6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6` at BASE and tip; the tool `plans/round84_gcode_probe.py` is `82f359e67840ec5ed876dc1904c0f69b158d2f1bc33278df3dfd64c51d528e75` at `767c907b` and tip; `plans/round84-cases.json` is `5b86f8d7efc24a529b4c53a23c6a4ccaed51866428535e6f0fcb4dbf13982cb5` at `767c907b` and tip. All three match the receipt stamps.
- Committed transcripts: `.ufo/waves/round-84/L1/c1-base.txt` prints `TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=34`, `PREDICATE R84-C1 fail`; `.ufo/waves/round-84/L1/c1-tip.txt` prints `REPRODUCE gcode-to-text tool=plans/round84_gcode_probe.py rc=0 matched=yes`, `DEFECTS n=0`, `TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0`, `PREDICATE R84-C1 pass`.

Evidence-verified, not executed: the counter self-test `SELFTEST cases=30 red=29 failures=0` (exit 0), mutants `MUTANTS real=16 killed=16 survived=0` (exit 0), the do-nothing / ledger-only / fabricated-observations controls each `target_reached=False`, and the probe's negative run `cases=8 mismatches=1`, `PREDICATE R84-PROBE fail`, exit 1. The probe self-test is committed as `SELFTEST cases=13 failures=0`. These support the frozen predicate; they do not replace the closure's independent byte checks above.

C1 verdict: **met**. The claim is a member replay, not a solved-task or model claim. The lane's own title "coverage" is a ledger/member-coverage move, consistent with the axis score held at 7 by the open L0 cap. Two procedural limits are real and routed below: the case table was first committed at `767c907b`, after the `b12a9d46` freeze (the counter's `TABLE-FROZEN-MISMATCH` anchor is inert), and the frozen controls test wrong-vector fabrication only; a correct-vector forged receipt is caught only by the `REPRODUCE` leg.

### R84-C2 / calibration — unmet on its frozen predicate; calibration unchanged (score 10 held)

Independent plain measurements:

- BASE entry `git show 4087b2f8:corpus/knowledge/tb2-code-from-image-offline.md`, first three lines: `source:`, `verified-at:`, then `recheck: python3 plans/round83_c1_replay.py --lane . --work DIR`. `grep -oE '2026-[0-9]{2}-[0-9]{2}|monthly|re-open|re-pin'` on line 3 prints nothing. Q1 and Q21 are defective at BASE.
- Tip entry, first four lines: `source:` names `S267` and the 40-hex pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; line 2 is `verified-at:`; line 3 is `recheck: 2026-11-04 … cadence monthly and at every change of the pin 2fd12b88…: re-open … confirm sha256 b9b7cb00…, then run …; re-pin source S267 if the upstream tree moves`. Both the date/cadence/action (Q1) and the pin coverage (Q21) are present; line 4 adds `writer: KengakuR84`.
- Committed transcripts: `.ufo/waves/round-84/L1/c2-base.txt` prints `TARGET entries=1 q1=1 q21=1 q13=1 defects=3`, `PREDICATE R84-C2 fail`; `.ufo/waves/round-84/L1/c2-tip.txt` prints `CHECK q1 ok`, `CHECK q21 ok pin-covered`, `CHECK q13 DEFECT exit=1 reason=gate_timing_check: FAIL: no admit rows …`, `TARGET entries=1 q1=0 q21=0 q13=1 defects=1`, `PREDICATE R84-C2 fail`. The report's 3 → 1 defect figures are reproduced.
- The Q13 instrument: `plans/gate_timing_check.py:241-243` `is_second_wave()` accepts only `falsify` or `wave[-_ ]?0*2`; a `w1/...` report is not a second-seat report. The lesson's Gate decision table has a `hold — not re-admitted; Q13 open` row, not an `admit` row, so the checker also reports `no admit rows`. The lane's refusal to copy reports into a fabricated `falsify/` directory is correct: provenance would be misstated. The L0 question `kengaku | round-84` is filed.

Evidence-verified, not executed: `AdmitR84/selftest.txt` `SELFTEST PASS fixtures=6 mutants=3`, exit 0; `control-filler` stays `q1=1 q21=1 q13=1 defects=3`; `control-date-only` stays `q21=1 q13=1 defects=2`; both `target_reached=False`. These show the counter is base-sensitive and not date-only.

C2 verdict: **unmet**. The target `q13=0` is not reached; the lane did not narrow or replace the target, and it records the miss in `SCORECARD.md` and the lesson. Calibration is unchanged (score 10 held): the Q1/Q21 repair is real but the declared calibration move does not verify. The horizon defect — the C2 predicate checks a successor lesson that does not exist at BASE, and the checker cannot accept this round's one-wave directory — is true and is routed, but it is not a licence to admit the claim.

## Gate evidence and revision boundary

The new registry rows are at `SKILL.md:745-747`: `round84-gcode-probe` (probe), `round84-c1-replay` (gate), `round84-c2-admission` (gate), each with an entry command, verdict map, self-test spelling, pinned values, write scope and owner. The row-level pinned values match the receipt stamps verified above.

- C1 gate: self-test 30 cases / 29 red / 0 failures, exit 0; mutants 16/16 killed, exit 0; three controls `target_reached=False`; probe self-test 13 cases / 0 failures; probe negative 8 cases / 1 mismatch / exit 1. Committed under `.ufo/waves/round-84/w1/{CounterR84,ProbeR84}/`.
- C2 gate: self-test 6 fixtures / 3 mutants, exit 0; filler and date-only controls as above. Committed under `.ufo/waves/round-84/w1/AdmitR84/`.
- Standing gates at the tip (`.ufo/waves/round-84/L1/`): `index-final.txt` `UNIVERSE knowledge files=77 indexed=77 missing=0 orphan=0`, `lessons files=141 indexed=141 missing=0 orphan=0`, `evidence dirs=75 indexed=75 missing=0 orphan=0`, `PREDICATE R75-C1 pass`; `population-final.txt` `replayed=28 located=28 … unexecuted=60 … covered=15`, `DEFECTS n=0`, `PREDICATE R79-C1 pass`; R74 registry `PREDICATE R74-C1 pass`. The R82 plans-registry gate is red at BASE and at the tip with the same `ROW-SELFTEST-FLAG:--selftest round83-c2-debt`; it is pre-existing, not caused by this round, and is routed as debt.

No sibling gate was executed by this closure. The tallies above are read from committed transcripts and checked against the report's figures.

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| novelty | unchanged | No new construct, prior-art claim or score increase; score 8 held. |
| coverage | improved | `gcode-to-text` unexecuted 27→28 executed, file-artifact 19/76→20/76; C1 met; score 7 held by the open L0 cap. |
| calibration | unchanged | R84-C2 unmet (`q13=1`, defects 3→1); the Q1/Q21 repair is real but the declared calibration move does not verify; score 10 held. |
| depth | unchanged | No new technical rule; the registry rows and lesson corrections support the claims; score 10 held. |
| operability | unchanged | Three new runnable instruments with committed self-test/control evidence; no new capability row and no score change; score 10 held. |
| freshness | improved | The r83 entry's recheck line now carries an ISO date, monthly cadence and the pin `2fd12b88…` with the sha256 and re-check action; the r83 freshness defect is repaired. The entry remains held on Q13; score 10 held. |
| adjacency | unchanged | `ConnectorR84/overlap.md` is committed with `overlap: none`; no cross-domain evidence is absorbed; score 9 held. |

## Outside discernment spot-check

Access date 2026-11-04. Sources were re-opened, not inferred from retained copies.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S271 — pinned `gcode-to-text` grader | admit (tier A `code`, member replay only) | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/gcode-to-text/tests/test_outputs.py` | agree | `curl` returns HTTP 200, 644 bytes, sha256 `6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6`, equal to the BASE capture. `:17` is exactly `assert hello_path.read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}", (`; the quoted span has 5 whitespace-split words (`printf … | wc -w` → 5), under the 25-word limit; `:6-19` resolves both test functions. The scope does not claim an agent solved the task. |
| Knowledge entry `corpus/knowledge/tb2-code-from-image-offline.md` — re-admission | hold / reject re-admission | `corpus/lessons/round-84.md` §Gate decision table; `plans/gate_timing_check.py:241-243`; `c2-tip.txt` | agree | The only Gate decision is `hold — not re-admitted; Q13 open`. The checker cannot count this round's `w1` reviewer reports as second-seat reports, and the Gate has no `admit` row (`no admit rows`). The entry's Q1/Q21 are repaired; Q13 is open. Refusing to fabricate a `falsify/` directory is the correct non-author-compatible decision. |
| Rejected route (a) — copy reviewer reports into `.ufo/waves/round-84/falsify/` | reject | `corpus/lessons/round-84.md` Gate prose; `.ufo/waves/round-84/L1/falsify-plan-refusal.txt` | agree | The round ran one v1 wave; copying reports into a synthetic `falsify/` directory would misstate provenance and manufacture a second wave. The policy-floor refusal is committed. |
| New `corpus/SOURCES.md` row S271 | admit row, `mined`, `used-by corpus/lessons/round-84.md` | `corpus/SOURCES.md:287`; `corpus/lessons/round-84.md` | agree | Row parses as 13 columns; `kind=code`, `tier=A`, `scope=member replay only`, `opened=2026-11-04`, `recheck=2027-01-18`, `used-by` resolves. The row's quote count and sha256 match the live source. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, final line `kengaku ok /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`, 30 `W04` duplicate-URL/different-scope warnings. Independent row parse: 262 → 263 rows; A 232 → 233, B 24, C 6; mined 238 → 239, rejected 16, queued 8. The report's figures match. Only S271 was added; old rows are byte-identical.

## Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | The round adds no admitted `knowledge/` entry on uncovered ground; S271 is one new source row, and `CORPUS.md` rule 4 says expansion is knowledge, not rows. No frontier row advanced and no capability entered. The lane's `improved` rests on the ledger/member move, which is the coverage axis, not the expansion trend; this is routed as R84-V7. |
| quality | improved | The r83 entry's Q1/Q21 recheck/pin debt is repaired and dated, the entry is held rather than left unmarked for its Q13 gap, and the lesson carries dated corrections R83-V1/V2 without rewriting the filed r83 bytes. No admitted entry fails a re-check. |
| discernment | improved | The outside sample agrees with the S271 admit and with the re-admission hold; the lane's own counter reproduces the r83 Q1/Q21/Q13 defects at BASE and refuses a successor re-admission rather than papering it over. The Q13 disagreement is a lesson and an open L0 question, not a silent pass. |

The lane's report claims `expansion: improved`; the closure does not accept that grade (R84-V7). The other two trend grades are accepted with the evidence above.

## Routed defects for the next steered round (owner: kengaku, except where noted)

- **R84-V1 — uncommitted round evidence.** `.ufo/waves/round-84/w1-results.json` and `.ufo/waves/round-84/w1/CriticR84/critique.md` are cited by the report but untracked at closure; `.ufo/waves/round-84/w1/CriticR84.md` and `CriticR84/report.txt` are also untracked. Commit them (the helper allows `.ufo/waves/**`) or replace every citation with a committed equivalent. A report must not cite working-tree-only evidence.
- **R84-V2 — freeze hygiene.** `plans/round84-cases.json` was first committed at `767c907b`, after the `b12a9d46` freeze; `git cat-file -e b12a9d46:plans/round84-cases.json` exits 128. The counter's `load_freeze_table()` returns `None` and `TABLE-FROZEN-MISMATCH` is inert. Commit the case table in the freeze commit next round and make the freeze anchor fail closed; keep the current table as historical evidence.
- **R84-V3 — forged-receipt control.** The C1 controls cover wrong-vector fabrication only. Add a correct-vector forged receipt (no fresh-run binding) to the frozen controls, or make the fresh-run `REPRODUCE` leg unconditional and show the forged receipt failing it.
- **R84-V4 — Q13 checker shape (operator/gate owner).** `is_second_wave()` accepts only `falsify`/`wave2`; a one-wave `w1` round cannot satisfy Q13 for any knowledge admission. The L0 question `kengaku | round-84` is the routing. Do not fabricate a falsify directory or amend the checker mid-round; wait for the ruling.
- **R84-V5 — frozen text overstates the QUALITY criterion.** The frozen claims say the `considerthese` item "Lands as a QUALITY criterion", but `corpus/QUALITY.md` is byte-identical at BASE and tip (`e6e85427107cfccdb1281fedfdcd54662d6c43ca` both) and has no Q61 row. Land the criterion in round 85 or append a correction naming the overstated frozen sentence; do not rewrite the filed claim.
- **R84-V6 — writer collision.** The repaired entry's `writer: KengakuR84` equals the seat-report trailer writer. `gate_timing_check.py` rejects a cited report whose line-start `writer:` equals the candidate writer; the reviewer reports pass only because their declaration is mid-line. Remove or rename the entry's writer (or use a distinct candidate writer id) and make the check line-start anchored, so the admission is not a formatting accident.
- **R84-V7 — expansion trend overclaim.** The report's `expansion: improved` counts a ledger/source move; LEARNING's expansion trend counts admitted `knowledge/` entries on uncovered ground, frontier areas, new source kinds, or a capability row. No such item landed. Correct the trend record in the next report/lesson (append-only).
- **R84-V8 — carried red gate.** `plans/round82_c1_plans_registry.py` prints `ROW-SELFTEST-FLAG:--selftest round83-c2-debt` at BASE `4087b2f8` and at the tip; it is pre-existing debt, not a round-84 regression. The round-83 counter builds `'--' + mode`, so the literal flag check misses it. Fix in the owning round, not by editing the historical counter mid-round.
- **R84-V9 — C2 definition horizon.** The frozen C2 Q13 leg targets the successor `corpus/lessons/round-84.md`, which does not exist at BASE (`q13=lesson-absent`); the "before" count of 3 therefore includes a future file. Keep the honest-stop record; a successor claim should define its before against an existing revision or explicitly price the future-file condition at freeze.

## Promotion and writes

No promotion, mint or SHONEN edit. No lane-authored file was modified by this review. This closure writes only this non-author spot-check (committed through `jj-lane.sh --as protocol`) and the helper-appended fleet `MANIFEST.json` rounds entry. The four SHONEN boxes appear checkable by a non-author from the cited committed surfaces, but the `[x]` decision is operator-owned and is not written here.

author: hyaku closure (non-author integrator, @m_opus)

# Round 42 — non-author closure spot-check (kengaku, 2026-10-26)

Measured against lane tip `f9bbee69b711677487515cf14d5c30f80658427f` (before: `d69452cfa4ea8f95a43caf3727a7c797ba390b6c`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here):
`2026-10-26T16:53:44-03:00 launch kengaku round=42 pgid=4052559 driver=hyaku-inline attempt=1` ·
`2026-10-26T18:28:04-03:00 complete kengaku round=42; hyaku-inline attempt=1`.
Scratch for my re-runs: `/fast/scratch/closure-kengaku-r42.Ygie` (a clean `--no-local` clone detached at `f9bbee69`, plus
re-fetched sources). No gate was executed (`round42-c1-mutants`, `round42-c2`, `round-close-check`, `scratch_guard.py
--selftest` are registered `gate` rows or gate selftests: evidence-verified); the registered `probe` `fibsqrt-probe` was
re-run. One read-only reviewer seat (`CloseKengakuR42.CloseR42BatteryReview`, dispatched by this closure, not by the lane)
statically reviewed `plans/battery42`.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-42/kengaku.md` (fleet repo) | `kengaku-shokunin <kengaku@shokunin.local> 987413e076446afb4ddee42ed902fd92fc420a96 2026-10-26 18:26:23 -0300`; lane tip `f9bbee69` committed 18:25:49 (34 s earlier; the report cites it); before the `complete` line 18:28:04 |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN' <report>`; `git show f9bbee69:SHONEN.md \| grep -cE '^\s*- \['` | 1 heading; 4 boxes in `SHONEN.md`, 4 `[~]` lines in the report |
| `Sources & frontier`, `Trend verdicts` sections | `grep -n '^## ' <report>` | present (:125, :145) |
| cited lane commits exist, ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` for `d69452cf bc856d80 523b2780 fda71ae0 ff14d76d 508434ad 445e81f8 3e8a2e5e f9bbee69` | 9/9 resolve and are ancestors (exit 0); `2fd12b88` is the upstream TB2 pin, not a lane commit; all eight round commits authored `kengaku-shokunin` |
| pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain` | `state branch=master local=f9bbee69… remote=f9bbee69… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty |
| prompt carries the template contract | `diff /home/vgpnk/Projects/kimi-shokunin/templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/kengaku-round-42.md)` | 10 hunks, every removed template line a `{{…}}` placeholder line; §1 binding, §2 claims, §2b frontier step, §3 L2 floor, §4 report contract, §5 commit/push scope/L0, §6 hyaku addendum (:141), §7 scratch discipline (:594) present; prompt committed `e0551f18` 16:53:42, 2 s before the launch line |
| waves integrated before filing | `jq '.results\|length'` and role tallies over `build-results.json` / `falsify-results.json` | 39 results (11 executor, 6 scribe, 6 scout, 5 critic, 4 connector, 3 mutation-tester, 2 sentinel, 2 reviewer) / 33 results (10 reviewer, 9 critic, 5 executor, 3 mutation-tester, 3 scout, 3 connector) — equal to the report's shape lines |
| measured revision transfers to tip | `git diff --name-only 3e8a2e5e f9bbee69` | only `falsify/` reports (222 files), `falsify-results.json`, `integrate/measure-tip3.txt`, `SCORECARD.md`: no claim surface moved after `measure-tip3.txt` @ `3e8a2e5e` |
| frozen inputs untouched | `sha256sum -c .ufo/waves/round-42/claims/frozen-digests.txt` in the clean clone; `git diff --stat d69452cf f9bbee69 -- plans/anchor_digest_check.py plans/order_check.py` | 12/12 `OK`; diff empty (both C1 tools unedited, as C1 requires); `sha256` `11bb2cad…`, `948d5e1d…` equal the frozen claims' pins |
| append-only lane docs | `git diff --numstat d69452cf f9bbee69 \| awk '{d+=$2} END{print d}'` | `0` deleted lines across the whole round |

Conformance defects and notes (status-neutral):
- **D1 Wave 2 under the m_flash floor.** 14/33 m_flash-routed seats (executor 5 + critic 9) against the prompt §6 rule "m_flash
  roles still carry ≥50 % of every wave" (prompt :177); self-disclosed (report :79-80, lesson §Mistakes added by the L1).
  Wave 1 met it (24/39) and the attack share (10/39).
- **D2 S128 has no `## Gate` row.** CORPUS §SOURCES rule 1: the round lesson's `## Gate` records, for every new row, the URL,
  access date and ≤25-word quote. `grep -n S128 corpus/lessons/round-42.md` → only `:125` (census line); the Gate table
  (`:38-46`) carries S125–S127 and the rejects. The `SOURCES.md:143` row itself carries URL, access time and quote.
- **D3 Gate flip condition fired and was not executed (Dockerfile).** The Gate's Dockerfile reject (`:44`) reads "if the entry
  keeps the `WORKDIR /app` sentence …, admit `Dockerfile` as a tier-B mechanism row". The landed entry keeps it and makes it
  load-bearing (`tb2-circuit-fibsqrt-grader.md:65`, `:89`, `:94`, `:435-438` "Finding 6's 'cwd coincidence' is therefore
  load-bearing"), with no `S###` row for `Dockerfile`. See §3.
- **D4 Wrong sentences in the new entry, routed but not marked.** `F42EntryQuotes` (verdict `entry-quotes-ok-24/24-bad-sentences-4`)
  found 3 wrong + 1 overclaim; I re-derived #1 myself: entry `:297` "48401 = 220²+1, is the only reach above 2^15" is false —
  `test_outputs.py:73-102` grades `209**2-1, 209**2, 209**2+1, 220**2-1, 220**2, 220**2+1` = 43680, 43681, 43682, 48399, 48400,
  48401, six values above 32768. The entry carries no errata section for them; they are recorded only as a count in
  SCORECARD `### Wave 2 outcome` (`:1822`), and `corpus/routed-findings.jsonl` (16 rows) carries no wave-2 item (`grep -c F42` → 0).
- **D5 Landing measurement envelope not quiescent.** `integrate/measure-final.txt:938` `local_bin_listing_before=763032563d3739aa
  after=77408cab9a10361a CHANGED` (`~/.local/bin` changed during the landing measurement); `measure-tip3.txt:938` `unchanged`,
  and its verdict lines equal the landing ones, so no claim rests on the changed window. `F42NoHarm` §3: the listing is
  names-only, a content rewrite would pass unseen.
- **D6 Seats without a verdict.** `R42PlanNext` (wave 1) ended without a report; `F42ConnFrontier` (wave 2) has no verdict line.
  Self-disclosed (report :74-77).
- Note: freeze `bc856d80` carries author date 16:52:31, before the 16:53:44 launch line; its committer date is 17:11:01 and
  16:52:31 is exactly `d69452cf`'s commit time (`git log -1 --format=%ci d69452cf`) — the jj working-copy change was created when
  the round-41 spot-check landed. Not early work.
- Note: the fleet-repo prompt commit `e0551f18` carries the lane identity; dispatch commits are orchestrator acts — attribution
  note for the operator, not lane debt.

## 2. Claims — re-check

| claim | how checked | before → after (observed by me) | reported | verdict |
|---|---|---|---|---|
| C1 calibration (`round42-c1-mutants`, registered **gate**) | **evidence-verified, not executed.** Plain measures on committed bytes: the `MUTANTS` literal in `plans/round42_c1_verify.py:145-230` (ids, tool, `adv_kind`); `TOTAL`/`FLOORS` (`:113-114`); `FIXTURES` per battery module; measurement files read with their `TIP` lines | `MUTANTS` = 14 (anchor 9: X1 X3 X6 X7 X9 X12 X13 X14 X15; order 5: XO1 XO3 XO5 XO6 XO7), `direct` 13 / `indirect` 1 (XO6); `TOTAL = 14`, `FLOORS = {"anchor": 9, "order": 5}`; battery 29 fixtures (a_class 6, a_route 6, a_row 6, o_clause 5, o_scan 6). Before: `measure-baseline.txt` (`TIP fda71ae0`) `BATTERY fixtures=0`, `MUTANTS total=14 killed=0 survived=14 … unattributed=0`, `anchor=0/9 order=0/5`, `PREDICATE C1 fail`, `exit=1`. After: `measure-final.txt` (`TIP ff14d76d`), `measure-tip2.txt` (`508434ad`), `measure-tip3.txt` (`3e8a2e5e`) all `PINS total=2 mismatched=0`, `BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=9/9 order=5/5`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, `exit=0`; every `MUTANT` line names its killer and an `attributed=L…` line | same (report :102-111) | **agree** — frozen predicate met |
| C1 battery honesty (admission condition the claim itself names: the counter certifies directions, not intent) | closure reviewer seat: Σ `len(FIXTURES)` by `ast` over committed blobs; token scan `grep -nE '__file__\|os\.environ\|PATH\|HOME\|subprocess\|/home\|\.local\|inspect\|exec\(\|eval\(\|shutil\|symlink\|chmod\|socket\|witness\|round42_c1_verify\|importlib\|sys\.path\|gpg\|showSignature\|core\.worktree\|config' plans/battery42/*.py`; 4 static mutant→fixture traces; wave-2 verdict lines read | 29 fixtures; 1 token hit (`a_class.py:2`, docstring), 0 code-level; no module reads/imports/copies `claims/witness/` or a lane clone; no `git config` call (so no `gpg.program`/`log.showSignature`/`core.worktree`); X7 (`a_class.py:90-99` → tool `:535`), X13 (`a_row.py:82-97` → `:570`), XO5 (`o_scan.py:53-65` → `order_check.py:117`), XO6 (`o_scan.py:79-90` → `:53`) each differ in the declared direction. Wave 2 verbatim: `F42RevBat*` `honest-6/6, 5/5, 6/6, 6/6, 6/6-substitute-0`; `F42C1StrongAttrib` `strong-attribution-8/8`; `F42C1Hardened` `hardened-copy-battery42-14/14-repairs-biting-4/4`; `F42GpgVector` `gpg-vector-real-verdict-change-impossible`; `F42NoHarm` `no-harm-verdicts-equal-277/277` | same (report :59-67) | **agree** — honest and attributable |
| C2 coverage (`round42-c2`, registered **gate**; `fibsqrt-probe`, registered **probe**) | counter **evidence-verified**; probe **re-measured**: `python3 plans/fibsqrt_probe.py --lane . --work <scratch>/pw` in the clean clone at `f9bbee69` (56 s); captures `sha256sum -c SHA256SUMS`; the entry's `## Case table` parsed and compared with the receipt | Counter: `claims/control-c2-nothing.txt` `checks=9 defects=6`; `measure-baseline.txt` @ `fda71ae0` `checks=9 defects=5`, `PREDICATE C2 fail`, `exit=1` → `measure-final/tip2/tip3` `V9 ok case_rows=16/16 bad=0`, `checks=9 defects=0`, `PREDICATE C2 pass`, `exit=0`. Probe: exit 0, output **identical** to `corpus/evidence/round42/fibsqrt-probe.txt` (4212 bytes; mine adds only `exit=0`): `regrade cases=16 differ=0`, `cases=16 observed_pass=7 observed_fail=9 mismatches=0`. Captures 9/9 `OK`. Case table 16/16 rows equal the receipt (case, tests, observed). Rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` 117 → 121; `git ls-tree --name-only <rev> corpus/knowledge/ \| wc -l` 48 → 49; README §Frontier `:374` "8 of 89 read" | same (report :112-118, :127-135) | **agree** — frozen predicate met |
| C2 ground truth, independent | re-fetched S125/S126/S127, README and `environment/Dockerfile` at the pin (`curl` raw URLs, 2026-10-26 18:32 -03) and read the deciding lines | all five `200` and `cmp` IDENTICAL to the captures; `sim.c:324` reads `argv[1]`, `sim.c:319` `parse_gates("gates.txt")` is cwd-relative, `Dockerfile:3` `WORKDIR /app` — the entry's stdin/argv and cwd findings follow from the code | same | **agree** (but D4: four entry sentences are wrong, one re-derived above) |

No-harm: `git diff --numstat d69452cf f9bbee69 -- SCORECARD.md` → `98 0` (append-only); round 42 table: calibration 8 → 8 held,
coverage 7 → 7 held (L0 cap), other axes held. Verdict lines `measure-baseline.txt` @ `fda71ae0` vs `measure-tip3.txt` @
`3e8a2e5e` (`diff` over `$ `/`PREDICATE`/`RESULT`/`exit=`/`rows=`/`defects=`/`checks=`/`routed_open`/`registry_rows` lines):
only C1/C2 (red → green), the C2 gate's P3/P6/P8 legs, `index_rows`/`knowledge_files` 48 → 49 in older counters' P8, anchor
`rows=117 tokens=24` → `rows=121 tokens=27 defects=0`, `routed_open=5` → `10`, `registry_rows=117` → `121` differ; rounds 36–41
counters and every other verdict line equal.

| axis | verdict | basis |
|---|---|---|
| calibration | improved | C1 frozen predicate met (14 survivors → 0, attributed; evidence-verified); battery reviewed honest/attributable by a non-author (closure seat + wave 2); the false frozen attack-surface sentence was found and disclosed by the lane, shown unable to change a verdict (`F42GpgVector`); score held 8 |
| coverage | improved | C2 predicate met; probe re-measured byte-equal; 117 → 121 rows, 48 → 49 entries, 8 of 89 TB2 graders; score capped 7 |
| novelty | unchanged | no claim; prior art kept honest (S128 published, tier C audit named; no novelty asserted) |
| depth | unchanged | no claim (SKILL section documents this round's probe; Q33/Q34 are criteria) |
| operability | unchanged | no claim; `scratch_guard.py` (selftest 36/36, `build/R42ScratchGuard/RECEIPT.txt:47`) and the `round_close.py` re-run fix (`integrate/r5-round-close-check.txt` `CHECK PASS`) are measured riders, not scored |
| freshness | unchanged | no claim |
| adjacency | unchanged | no claim; PROVINCE routing clause (digital-logic / C-simulator semantics unowned) only |

## 3. Discernment spot-check (`corpus/lessons/round-42.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S125 `tests/test_outputs.py` @ `2fd12b88` | admit (mined, A) | `curl` raw URL → `200`, sha256 `6117b8edb7d5…`, `cmp` with capture: identical; line 23 `assert line_count < 32000, f"…"` | agree | quote "assert line_count < 32000" verbatim at `:23` (4 words); the file is the task's whole score |
| S127 `tests/sim.c` @ `2fd12b88` | admit (mined, A) | `curl` → `200`, sha256 `700645ac6156…`, identical; line 335 `for (int step = 0; step < 32000; step++) {  // Full simulation` | agree | quote verbatim (9 words); `:319`/`:324` carry the cwd-relative load and `argv[1]` input the entry rests on |
| S128 OpenAgents issue #9645 (new row) | admit (mined, B) | `gh api repos/OpenAgentsInc/openagents/issues/9645` → `state=closed created_at=2026-09-25T09:01:50Z closed_at=2026-09-25T09:11:26Z`, title equal; body line 3 contains "The official grader exercises 28 values, none above 48,401." | agree | quote verbatim at the cited "body line 3" (9 words, ≤25); tier B right for a third party's report; cited as prior art only. Defect D2: no Gate row |
| `README.md` @ `2fd12b88` | reject (captured, not a row) | `curl` → `200`, identical to capture `201f7c88…`; line 10 "The provided `sim.c` simulator reads this file and simulates the circuit for 32,000 time steps." | agree | quote verbatim (15 words); every checkable sentence is carried by S125–S127; `Dockerfile:9-10` copies only `tests/sim.c` and `gates.txt` into the image |
| `Dockerfile` @ `2fd12b88` | reject (captured, not a row; "one claim flagged") | `curl …/environment/Dockerfile` → `200`, identical to capture `780c2398…`; line 3 `WORKDIR /app` | **disagree** | the reject was conditional: "if the entry keeps the `WORKDIR /app` sentence …, admit `Dockerfile` as a tier-B mechanism row". The entry kept it and made it load-bearing (`:435-438`; 9/16 verdicts move off `/app`, `F42CritCwd`), so by the Gate's own flip the file should be a row (or the sentence conditioned). The cwd claim now rests on a capture and a seat report (`R42ScoutHarborCwd`) with no `S###` row |

Newly written row re-opened: S128 (above; quote 9 words, verbatim, location correct). Census:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0,
`kengaku ok`, 15 `W04` (`diff` of the W04 lines against `claims/census-before.txt` → identical set).

## 4. Trend verdicts

- **expansion — improved.** One admitted entry on Frontier ground (eighth TB2 grader; the first whose graded artefact is a data
  file executed by a simulator the grader compiles) citing mined S125–S128; three capability rows demonstrated
  (`attributed-mutant-kills` by the landing/tip measurements plus the red `control-c1-attribution.txt`,
  `compiled-simulator-grader-probe` by my byte-equal re-run, `scratch-root-guard` by its committed selftest receipt 36/36).
  The entry's core (case table 16/16 = receipt, sources byte-fresh, quotes 24/24 per `F42EntryQuotes`) holds; its four bad
  sentences (D4) do not fail the bar it was admitted under.
- **quality — unprovable-but-better.** Two more gate tools carry a standing battery killing 14/14 frozen near-variants with
  attribution, reviewed honest by non-authors; the C2 counter gained V9 with a red filler control; the entry's mechanism was
  corrected in-round from a falsifier's measurement before landing (`R42CritProbe` D1). Against that: four wrong or
  overclaiming sentences in the new entry were found by wave 2 *before* filing and left uncorrected in the entry (D4; rounds
  39–41 closed the same class by appended errata in-round), and V9 admits 2 of 4 attack shapes. Not `harmed`: they are
  disclosed in SCORECARD with the report as evidence and routed, not left after notice (same ruling as round 37) — but a
  round-43 that leaves them unmarked would be.
- **discernment — improved** (the lane self-graded "unprovable-but-better at most"; the outside check decides). The spot-check
  agrees with the gate on 3 admits and 1 reject and disagrees on 1 (Dockerfile, D3); last round's outside disagreement (round-41
  D2, in-place SOURCES edit) became the grounded criterion Q34 (`corpus/QUALITY.md:761`, lesson pointer
  `round-41-verifier-spotcheck.md:30-36`), and the round-40 XO5/XO6 mislabel became Q33 with a red control. Caveat: D3 must
  become a lesson and a criterion next round.

## 5. Routed defects (round 43)

- **R1** Entry errata (D4): append `## Errata (round 43)` to `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` correcting `:297`
  (six graded inputs above 2^15, not one), `:311` (only the case recipe runs with `stdin=DEVNULL`, `fibsqrt_probe.py:201`),
  `:431` and `:433-434` (`F42EntryQuotes` #3, #4); fix the lesson pointer `fibsqrt-probe.txt:6` → `:11` (`F42CritOverclaim`) by
  an appended correction. Never in place.
- **R2** Gate record (D2, D3): append a Gate row for S128 (URL, access date, quote); execute the Dockerfile flip — admit
  `environment/Dockerfile` @ `2fd12b88` as a tier-B mechanism row and cite it from the entry's cwd sentences, or condition
  those sentences on the grading cwd; turn the D3 disagreement into a lesson and a QUALITY criterion (a conditional reject's
  flip is re-checked at landing).
- **R3** Durable queue: write the wave-2 routed items (`F42RevC2Package` 9, `F42RevLesson` 8, `F42RevQuality` 6,
  `F42RevRiders` 5, `F42CritAdv` 2, `F42CritScorecard` 1, `F42ConnClaims` 1, `F42CritPlanNext` 5, `F42EntryQuotes` 4) into
  `corpus/routed-findings.jsonl`, not only SCORECARD prose.
- **R4** C1 counter soundness (already in SCORECARD `### Planned (round 43)`): pin `gpg.program`/`log.showSignature`, hide the
  builder copy, read-only lane hide, refuse a `core.worktree`/toplevel outside `d`, site-value attribution leg — each with a red
  hostile control; correct the frozen "these two tools run no fixture code" sentence by a named correction, not an edit.
- **R5** C2 V9 is a consistency check (`F42CritV9` 2/4 shapes admitted, `F42MutC2V9` 7/16 caught): the round-43 C2 counter needs
  a content leg a filler cannot copy from the receipt.
- **R6** Hygiene: the wave-spec generator asserts `flash*2 >= seats` before writing a `.ready` (D1, the lane's own fix); the Q32
  envelope hashes `~/.local/bin` contents, not names, and a `CHANGED` listing invalidates the measurement it brackets (D5).

SHONEN (operator note): all four boxes filed `[~]`. Boxes 1 (decision table with cited sources, registry rows), 2 (end-to-end
task logged; probe byte-equal on my re-run) and 3 (`integrate/measure.sh` re-runs every claim counter from a clean clone) look
checkable by a non-author from committed bytes; box 4 (PROVINCE accuracy) needs a judgment read. Promotion is operator-owned.

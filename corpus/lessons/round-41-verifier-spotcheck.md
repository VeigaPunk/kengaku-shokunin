author: hyaku closure (non-author integrator, @m_opus)

# Round 41 — non-author closure spot-check (kengaku, 2026-10-26)

Measured against lane tip `e61aff6f72c7cc358f854762dd769cd55ef296b7` (before: `e50c134556b4ba48e29dc7ff364e90d6ef07a3f3`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here):
`2026-10-26T15:14:33-03:00 launch kengaku round=41 pgid=749835 driver=hyaku-inline attempt=1` ·
`2026-10-26T16:42:33-03:00 complete kengaku round=41; hyaku-inline attempt=1`.
Scratch for my re-runs: `/fast/scratch/closure-kengaku-r41.phcn` (`git archive e61aff6f` extract plus a clean `--no-local`
clone detached at `e61aff6f`, removed after). No gate was executed (`round41-c1-mutants`, `round41-c2`, `round-close-check`
are registered `gate` rows: evidence-verified); the registered `probe` `constraints-probe` was re-run. One read-only reviewer
seat (`CloseKengakuR41.CloseR41BatteryReview`, dispatched by this closure, not by the lane) statically reviewed `plans/battery41`.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %ad' -- .ufo/reports/round-41/kengaku.md` (fleet repo) | `kengaku-shokunin <kengaku@shokunin.local> 0ff2af1c87b5540b456fd6aca3b8f6b42e4e25ab Mon Oct 26 16:40:23 2026 -0300`; lane tip `e61aff6f` committed 16:40:27 (4 s later; the report cites that hash and `ls-remote` shows it — filed after the tip was known); before the `complete` line 16:42:33 |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN' <report>`; `git show e61aff6f:SHONEN.md \| grep -cE '^\s*- \['` | 1 heading; 4 boxes in `SHONEN.md`, 4 `[~]` lines in the report |
| `Sources & frontier`, `Trend verdicts` sections | `grep -n` on the report | present (:115, :138) |
| cited lane commits exist, ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` for `e50c1345 8ef8b4fc f774a87a fc79f2a4 74513c06 0d574196 3d0058fb d7c77895 53b9e4e5 e61aff6f` | 10/10 resolve and are ancestors; all nine round commits authored `kengaku-shokunin <kengaku@shokunin.local>` |
| pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain \| wc -l`; `git ls-remote origin refs/heads/master` | `state branch=master local=e61aff6f… remote=e61aff6f… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain 0 lines; remote `e61aff6f…` |
| prompt carries the template contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/kengaku-round-41.md)` | 10 hunks, every removed template line a `{{…}}` placeholder line; §1 binding, §2 claims, §2b frontier step, §3 L2 floor, §4 report contract, §5 commit/push scope/L0, §6 hyaku addendum (:141), §7 scratch discipline (:594) present; prompt committed `e25f28e3` 15:14:30, 3 s before the launch line |
| waves integrated before filing | `jq '.seats, (.results\|length)'` over `build-results.json` / `falsify-results.json`; `ls .ufo/waves/round-41/{build,falsify}/*.md \| wc -l` | 38 seats / 38 results / 38 reports; 34 / 34 / 34 |
| measured revision transfers to tip | `git diff --stat 74513c06 53b9e4e5 -- . ':!.ufo/waves'`; `git diff --stat 53b9e4e5 e61aff6f` | landing→`53b9e4e5`: 7 files, 462 insertions, 1 deletion (the S124 anchor cell); `measure-tip2.txt` re-measured at `53b9e4e5`; `53b9e4e5`→tip adds only `integrate/census-final.txt` and `integrate/measure-tip2.txt` |
| frozen inputs untouched | `sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt` on the `e61aff6f` extract; `git diff --stat e50c1345 e61aff6f -- plans/tip_receipts.py plans/sources_adopt.py` | 11/11 `OK`; diff empty (both C1 tools unedited, as C1 requires); `sha256` of both equals the counter's `PINS` (`e4f49714…`, `38492bf1…`) |

Conformance defects and notes (status-neutral):
- **D1 Host-hygiene breach by a wave-1 seat.** `R41CritIndep` ran `rm -rf -- /fast/scratch/hyaku/kengaku-r41` (the shared round
  root) at 15:42:24 -03, deleting running seats' clones and the L1's first baseline run. Disclosed in the report and the lesson
  §Mistakes with the transcript pointer (errata D1); no damage outside the round's scratch. `ls /home/vgpnk/.local/bin/git` at
  closure → no such file (round-40 vector absent). Unguarded by tooling — routed (R2).
- **D2 SOURCES row edited in place outside the three mutable cells.** S124's `anchor` cell changed old→new in `53b9e4e5`
  (`git diff 74513c06 53b9e4e5 -- corpus/SOURCES.md`: 1 −/1 +). CORPUS.md §SOURCES rule 2 lets only `status`, `recheck`,
  `used-by` change in place; a correction is a new row opening `supersedes S124 —`. The change is logged old→new in the lesson
  (`## Gate changes after the falsify wave`) and the row was written this round, so nothing a prior round cited moved; still a
  rule-2 defect — routed (R4).
- **D3 Evidence pointer to a session transcript.** The failed first baseline run is evidenced only in the L1 session file
  (lesson errata D3); `integrate/measure-baseline.txt` holds only the re-run. The lane disclosed it; not a claim input.
- Note: the freeze `8ef8b4fc` carries author date 15:13:37, before the 15:14:33 launch line; its committer date is 15:30:52 and
  15:13:37 is exactly `e50c1345`'s commit time (`git log -1 --format=%ai e50c1345`) — the jj working-copy change was created when
  the round-40 spot-check landed. Not early work.
- Note: the fleet-repo prompt commit `e25f28e3` ("kengaku dispatch evidence (hyaku inline attempt 1)") carries the lane identity;
  dispatch commits are orchestrator acts — attribution note for the operator, not lane debt.

## 2. Claims — re-check

| claim | how checked | before → after (observed by me) | reported | verdict |
|---|---|---|---|---|
| C1 calibration (`round41-c1-mutants`, registered **gate**) | **evidence-verified, not executed.** Plain measures: mutant table parsed from the frozen counter (`ast` + `eval` of the `MUTANTS` literal); each mutant's `old` string counted in its tool; `TOTAL`/`FLOORS` read; controls and measurements read; battery reviewed statically by the closure's reviewer seat | `MUTANTS` = 23 (receipts 13: T01–T13; sources 10: S01–S09, S11), `adv_kind` direct 21 / indirect 2, 23/23 `old` strings occur exactly once; `TOTAL = 23`, `FLOORS = {"receipts": 13, "sources": 10}` (`plans/round41_c1_verify.py:123-124`). Before: `claims/control-c1-nothing.txt` `BATTERY fixtures=0`, `MUTANTS total=23 killed=0 survived=23`, `MUTANTS-BY-TOOL receipts=0/13 sources=0/10`, `PREDICATE C1 fail`, `exit=1`; vacuity control `control-c1-no-mutants.txt` `MUTANTS total=0` → `PREDICATE C1 fail`, `exit=1`. After: `measure-final.txt` (TIP `74513c06`) and `measure-tip2.txt` (TIP `53b9e4e5`) `PINS total=2 mismatched=0`, `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`, `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, `exit=0`; verdict lines of the two files identical (`diff` of `grep -E '^(PINS\|BATTERY\|MUTANTS\|…)'` → empty) | same; score 8 → 8 held | **verified** |
| C1 battery honesty (admission condition the claim names; the counter is forgeable by a hostile stub, `R41CritC1Counter` A1′) | reviewer seat: fixture count by the counter's own enumeration (Σ `len(FIXTURES)`), token scan `grep -nE '__file__\|os\.environ\|PATH\|HOME\|subprocess\|/home\|\.local\|inspect\|exec\(\|eval\(\|shutil\|symlink\|chmod\|socket\|witness\|round41_c1_verify\|importlib\|sys\.path' plans/battery41/*.py`, 4 mutant→fixture traces (T03, T04, S07, S11); wave-2 tallies read | 48 fixtures (r_ctl 4, r_map 10, r_run 4, r_setup 8, s_exit 6, s_modes 8, s_usage 8); 14 token hits, all docstring prose or data strings, 0 code-level; no module reads, imports or copies `claims/witness/`; T03 1→0, T04 0→1, S07 3→0, S11 5→0 traced statically through the mutated lines — agree. `F41C1Attribution.md:69-70,204` `BUILT fixtures=48 sidechannel=0`, `ATTRIBUTABLE 23/23`, negative control `0/1`; `F41C1Hardened.md:244-262,369` frozen and hardened copies both 23/23, repairs biting 5/5; `F41RevBat*` per-module verdicts sum to 47 honest + 1 incidental (`s_usage-03`, exit 5 is `duplicate-request`, S03 still credited via its twin) + 0 dishonest | "attribution 23/23, hardened 23/23, 47/48 honest + 1 incidental" | **agree** (non-author) |
| C2 coverage (`round41-c2`, registered **gate**; `constraints-probe`, registered **probe**) | counter **evidence-verified**; probe **re-measured**: `python3 plans/constraints_probe.py --lane . --work ../pw` and `--dry` in the clean clone at `e61aff6f`; captures `sha256sum -c SHA256SUMS`; plain counts | `control-c2-nothing.txt` `checks=8 defects=5` (V2 V3 V4 V7 V8), `exit=1` → `measure-tip2.txt` `checks=8 defects=0`, `PREDICATE C2 pass`, `exit=0`. Probe: exit 0, first 5775 bytes **byte-equal** to `corpus/evidence/round41/constraints-probe.txt` (my file adds only my `exit=0` line): `regrade cases=25 differ=0`, `cases=25 observed_pass=6 observed_fail=19 mismatches=2`; the two `match=NO` are `later-valid-wed-1105` and `seconds-30`, both named in the entry (:75, :298, :320, :413). `--dry` byte-equal to `constraints-dry-cases-freeze.txt`. Captures 10/10 `OK`. SOURCES rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` 114 → 117; knowledge `.md` 47 → 48; README §Frontier "7 of 89 read" (`corpus/README.md:356`) | same; score 7 → 7 held (L0 cap) | **verified** |
| C2 ground truth, independent | re-read S122 at the pin: integrity check `test_outputs.py:88-96` compares `Path.read_text()` strings; captured calendars' sha256 vs `_EXPECTED_SHA256` (`:27-37`) | `read_text()` translates CRLF → LF, so the `input-crlf-rewrite` case (`PPP`) follows from the code and falsifies `instruction.md:18` as the entry says; the three capture digests equal the grader's pins (`5a5d4580…`, `c97e85db…`, `32a0f868…`) | same | **agree** |
| C2 prose limits (frozen V1–V8 admit a content-free filler, `R41CritClaims` D2) | read the entry's §Errata (wave 2) and the lesson Mistakes row | disclosed by the lane; prose surfaces (PROVINCE paragraph, §Frontier narrowing, S124) were checked by wave-2 reviewers and my source re-opens below, not by the counter | disclosed | limit, routed (R3) |

No-harm: `git diff --numstat e50c1345 e61aff6f -- SCORECARD.md` → `200 0` (append-only, no removed line); whole-round removed
lines in lane-authored docs: 1 (`corpus/SOURCES.md`, D2). Baseline vs tip (`diff` of verdict lines in `measure-baseline.txt` @
`fc79f2a4` vs `measure-tip2.txt` @ `53b9e4e5`): only C1/C2 (red → green), anchor `rows=114 tokens=21` → `rows=117 tokens=24
defects=0`, and `round_close.py --round 41` (`exit=2` → `ORDER RESULT PASS`, `exit=0`) differ; rounds 36–40 counters,
ledger-tip, `tip_receipts` (`receipts=27 byte_equal=7 differ=0 skipped=20`) and r38 `ORDER RESULT FAIL` (pre-existing) unchanged.

| axis | verdict | basis |
|---|---|---|
| calibration | improved | C1 frozen predicate met (23 survivors → 0, evidence-verified); battery reviewed honest/attributable by a non-author; vacuity closed (`TOTAL`/`FLOORS`, shown failing); score held 8 |
| coverage | improved | C2 predicate met; probe re-measured byte-equal; 114 → 117 rows, 47 → 48 entries, 7 of 89 TB2 graders; score capped 7 |
| novelty | unchanged | no claim; prior art kept honest (S124 closed unmerged, no novelty asserted) |
| depth | unchanged | no claim (SKILL constraints section documents this round's probe) |
| operability | unchanged | no claim; `routed_open.py` rider and 4 registry rows are measured riders, not scored |
| freshness | unchanged | no claim; four drift-risk rows re-opened with no change |
| adjacency | unchanged | no claim; PROVINCE routing clause (calendar/RFC 5545 conformance unowned) only |

## 3. Discernment spot-check (`corpus/lessons/round-41.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S122 `tests/test_outputs.py` @ `2fd12b88` | admit (mined, A) | `curl` raw URL at the pin → sha256 `1422b345…90c5d1`; `cmp` with the capture: equal; line 143 `assert not any(_overlap(s, e, cal) for cal in (A, B, C))` | agree | digest = pin, quote verbatim at the cited line (11 words, ≤25); the file is the task's whole score |
| S123 `instruction.md` @ `2fd12b88` | admit (mined, A) | `curl` raw URL → sha256 `342def78…f937b6`; equal to capture; line 18 `… Any modification will cause the tests to fail.` | agree | quote verbatim (8 words); the sentence the probe's `input-crlf-rewrite` case falsifies, which I confirmed from `:88-96` |
| S124 TB2.1 PR #245 | admit (mined, B, closed unmerged) | `gh api repos/harbor-framework/terminal-bench-2-1/pulls/245` → `state=closed merged=false created_at=2026-10-05T02:41:13Z closed_at=2026-10-08T19:02:36Z comments=0`; body line 7 (= capture `pr245-body.md:11`, 4 header lines) carries "the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar"; body line 3 "local draft only; do not submit without owner authorization" | agree | quote verbatim (14 words); tier B right for a closed, unmerged proposal; cited as prior art only |
| PR #245's `tests/test_event_binding_adversarial.py` (55 cases) | reject as row | `gh api …/pulls/245/files` → file `added`, 116 lines; its `CASES` list has 55 entries (`grep -cE '^\+    \("'` over the patch → 55); body line 26 "The patch adds 55 adversarial calendar fixtures …" | agree | the count is real by static reading, but nothing was captured or executed, so the row would rest on an unexecuted claim; the flip condition (capture + executed count) is the right bar |
| `solve.sh`, `test.sh`, `task.toml`, `Dockerfile`, `README.md`, 3 calendars, `SHA256SUMS` | captured, not rows | `sha256sum -c SHA256SUMS` in the capture dir → 10/10 `OK`; calendar digests = grader `_EXPECTED_SHA256`; `curl …/solution/solve.sh \| cmp - <capture>` → equal | agree | they are probe inputs and the oracle, not sources of an entry statement; pinned by digest |

Newly written row re-opened: S124 (quote 14 words, verbatim, at the cited body paragraph; state words "closed", "merged false"
in the anchor match the live API). Census:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0,
`kengaku ok`, 15 `W04` (duplicate urls across scopes; `diff` of the W04 lines against `claims/census-before.txt` → identical set).

## 4. Trend verdicts

- **expansion — improved.** One admitted entry on Frontier ground (seventh TB2 grader; the first whose verdict is computed by an
  embedded scheduling model over sha256-pinned inputs) citing mined S122/S123/S124; three capability rows demonstrated
  (`cli-exit-pair-mutants` by the tip measurement, `embedded-model-grader-probe` by my byte-equal re-run, `routed-findings-burndown`
  by `integrate/routed-observe.txt` `rows=10 mismatched=0`, `routed_open=5 oldest_round=39`).
- **quality — improved.** Two more lane tools carry a standing battery killing 23/23 frozen mutants, each kill attributed to its
  mutated line and reviewed honest by a non-author; the predicate can no longer pass on an empty list; the entry's 12 bad sentences
  and 8 overclaims were corrected in-round by appended errata (none reverses a finding). No admitted entry failed my re-check
  (S122/S123 byte-fresh at the pin, probe byte-equal).
- **discernment — improved** (the lane self-graded "unprovable-but-better at most"; the outside check decides). The spot-check
  agrees with the gate on 3 admits and 2 rejects; S10 was withdrawn on a witness (`ref_rc=5 mut_rc=5`), not an assertion; the
  overstatements ("no committed fixture", S124 "published", mis-pasted plan, C2 overclaims) were caught by the lane's own
  falsify wave and corrected by errata, not relabelled; Q31 cites the round-41 lesson's Mistakes row (`corpus/QUALITY.md:678-679`),
  Q32 the round-40 host-safety breach.

## 5. Routed defects (round 42)

- **R1** C1 counter soundness residuals (`R41SentinelCounter` F1–F4: variant readable inside a tool run, AF_UNIX, SysV IPC, relative
  argv escapes; `R41CritC1Counter` A1′ dead-site credits for T03/T04): the round-42 counter must carry the five `F41C1Hardened`
  repairs frozen, each with a red hostile control. Admission this round rested on attribution 23/23 and the non-author battery
  review above. Also: T08 fixtures depend on `uv` being absent from `/usr/local/bin` on the fixed PATH (`F41RevBatCtl.md:89`) —
  pin that assumption in the counter's PINS or fixture.
- **R2** Scratch hygiene (D1): no seat may delete outside its own `$SCR/<SeatName>`; give the round root a guard the seats cannot
  remove (e.g. a sentinel file the L1 checks before each measurement) and carry the guard sentence into every wave context.
  Q32's forward leg is red on the L1's own seven round-41 receipts (no envelope or timestamp line, `corpus/QUALITY.md:681-687`,
  self-disclosed); it binds L1 counter runs from round 42.
- **R3** C2 filler admission: the frozen V1–V8 pass a content-free package (`R41CritClaims` D2); the round-42 C2 counter needs a
  standing filler control that must stay red, and a check that reads S124-style tier-B PR rows' live state word.
- **R4** SOURCES rule 2 (D2): correct a non-mutable cell by a new row opening `supersedes S0NN —`, never in place.
- **R5** Carried: 14 `round_close.py`/`tip_receipts.py` residuals (`R41RoundCloseMut`), `F39LedgerTip` D1, `F39MutDirection`,
  `F39OrderGateMut` fail-open (no owner this round); `s_usage-03` incidental fixture (`--admit-ids "S131"`); 34 advertised
  behaviour rows of the two tools still unpriced (58 advertised, 24 priced, `F41CritC1Count`).

SHONEN (operator note): all four boxes filed `[~]`. Boxes 1 (decision table with cited sources, registry rows), 2 (end-to-end
task logged; probe byte-equal on my re-run) and 3 (`integrate/measure.sh` re-runs every claim counter from a clean clone) look
checkable by a non-author from committed bytes; box 4 (PROVINCE accuracy) needs a judgment read. Promotion is operator-owned.

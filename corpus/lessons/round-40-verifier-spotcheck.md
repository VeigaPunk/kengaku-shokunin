author: hyaku closure (non-author integrator, @m_opus)

# Round 40 — non-author closure spot-check (kengaku, 2026-10-26)

Measured against lane tip `5b73c5e8a7c605b439ee37caac2b810fed4e1fb8` (before: `d3a6277f188434458e1d2ce04aff59392c6f0dc6`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here):
`2026-10-26T13:00:48-03:00 launch kengaku round=40 pgid=210514 driver=hyaku-inline attempt=1` ·
`2026-10-26T15:07:58-03:00 complete kengaku round=40; hyaku-inline attempt=1`.
Scratch for my re-runs: `/fast/scratch/closure-kengaku-r40.Vahc` (`git archive 5b73c5e8` extract plus a clean `--no-local`
clone detached at `5b73c5e8`, removed after). No gate was executed; the registered probe was re-run (it is a `probe` row).

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-40/kengaku.md` (fleet repo) | `kengaku-shokunin <kengaku@shokunin.local> 58126ecd263362bc4c87ede91f8df3922be868dc 2026-10-26 15:07:21 -0300`; lane tip `5b73c5e8` committed 15:05:43, so the report lands last |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN' <report>`; `git show 5b73c5e8:SHONEN.md \| grep -nE '^\s*- \['` | 1 heading; 4 boxes in `SHONEN.md`, 4 `[~]` lines in the report |
| cited lane commits exist, ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` for `d3a6277f bbb10950 055748f7 3077adbc ec172168 ec1005a2 c9c793ca 7984fd30 5b73c5e8` | 9/9 resolve and are ancestors; all eight round commits authored `kengaku-shokunin` |
| pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain`; `git ls-remote origin refs/heads/master` | `state branch=master local=remote=5b73c5e8… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `5b73c5e8…` |
| prompt carries the template contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/kengaku-round-40.md)` | 10 hunks, every removed template line a `{{…}}` placeholder; §2b frontier step, §3 L2 floor, §4 report path/SHONEN/hash rule, §5 commit/push scope/L0, §6 hyaku addendum present; prompt committed `1be05b85` 13:00:45 |
| waves integrated before filing | `jq length` over `build-results.json` / `falsify-results.json`; top-level `git ls-files '.ufo/waves/round-40/{build,falsify}/*.md'` | 37 results / 37 reports; 35 results / 35 reports |
| measured revision transfers to tip | `git diff --stat ec172168 7984fd30 -- . ':!.ufo/waves'`; same for `7984fd30 5b73c5e8` | `4 files changed, 279 insertions(+)` (LOG, SCORECARD, lesson, entry errata; no deletion); then empty |
| frozen inputs untouched | `sha256sum -c .ufo/waves/round-40/claims/frozen-digests.txt` on the `5b73c5e8` extract; `git diff --stat bbb10950 5b73c5e8 -- <5 frozen files>`; `git diff --stat d3a6277f 5b73c5e8 -- plans/{anchor_digest_check,ledger_tip,order_check,pkg_gate}.py` | 11/11 `OK`; both diffs empty (the three tripwire tools are unedited, as C1 requires) |

Conformance defects (status-neutral):
- **D1 Host-safety breach by a wave-1 seat.** `R40CritC1Counter` wrote a `git` shim into the shared PATH directory
  `/home/vgpnk/.local/bin` (outside every write scope); other lanes' git calls hit it (~14:05–14:07 -03, kasegi r37
  `ExecC1JudgedHeadFail` F4). Disclosed in the report and lesson §Conformance incident; neutralized (`SystemExit` at import,
  SHIM_DIR `/nonexistent`); `ls /home/vgpnk/.local/bin/git` at closure → no such file. The first write is not timestamped.
- **D2 Unregistered gate-shaped tool.** `plans/round_close.py` (exit 0/1 verdict, wired as Q30's gate) and the
  `tip_receipts.py` derived-mapping change are recorded only in the registry addendum, not as rows; PROTOCOL §Gate standard
  (Delivery) grades no gate conformant until its row exists. `F40RoundClose`: 6/14 mutants caught.
- **D3 Census line understated.** The report says census after "exit 0, `kengaku ok`"; my run prints the same 15 `W04`
  duplicate-url warnings as before (`grep -c W04 census-after.txt` → 15). Unchanged, not harm; the line should say so.
- Lane-axis note: the dispatched prompt names lane axes "novelty + calibration"; C2 works coverage as the lowest
  non-retired axis (7, tied with novelty) under the lane's frozen tie-break — conformant with AXES §Working the axes.

## 2. Claims — re-check

| claim | how checked | before → after (observed by me) | reported | verdict |
|---|---|---|---|---|
| C1 calibration (`round40-c1-mutants`, registered **gate**) | **evidence-verified, not executed.** Plain measures: mutant table parsed from the frozen counter; each mutant's `old` string unique in its tool; fixture ids in `plans/battery40`; kill attribution in both receipts; static review of all 7 modules | counter `MUTANTS` = 21 (A 11, L 7, O 3), 21/21 `old` strings occur exactly once in the landed tools; 21 fixtures (3+2+3+3+3+4+3); `control-c1-nothing.txt` `BATTERY fixtures=0`, `MUTANTS total=21 killed=0 survived=21`, `PREDICATE C1 fail`, `exit=1` → `measure-final.txt` (TIP `ec172168`) and `measure-tip2.txt` (TIP `7984fd30`) `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, `exit=0`; the two receipts' C1 sections are line-identical; each mutant killed by the one fixture built for it (A01←a_tok-upper-anchor … O14←o_gate-claims-bak-name) | same | **met** |
| C1 battery honesty (admission condition the claim names) | read all 7 modules (501 lines); `grep -nE '__file__\|os\.environ\|PATH\|subprocess\|/home\|\.local\|inspect\|exec\(\|eval\(\|shutil\|symlink\|chmod' plans/battery40/*.py` | 0 code hits (2 docstring mentions of tool names); every `build()` only writes inside its fixture dir via `ctx.clone`/`ctx.init`/`ctx.git` and returns tool argv; no module reads tool or counter program text, shims a binary, touches PATH/HOME or writes the host fs — none of the wave-1 counterexample vectors (A1 self-reading check body, A2 PATH `git` shim) | "honest 21/21" (lane seats) | **agree** (non-author) |
| C2 coverage (`round40-c2`, registered **gate**; `db-wal-probe`, registered **probe**) | counter **evidence-verified**; probe **re-measured**: `python3 plans/db_wal_probe.py --lane . --work ../pw` and `--dry` in a clean clone at `5b73c5e8`; plain counts | `control-c2-nothing.txt` `checks=7 defects=4` (V2 V3 V4 V7), `exit=1` → `measure-tip2.txt` `checks=7 defects=0`, `PREDICATE C2 pass`, `exit=0`. Probe: exit 0, **byte-equal** to `corpus/evidence/round40/db-wal-probe.txt` (`cases=28 observed_pass=8 observed_fail=20 mismatches=0`, `regrade cases=28 differ=0`; 28 `match=yes`, 0 `match=NO`); `--dry` byte-equal to `db-wal-dry-cases-freeze.txt`. SOURCES rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` 111 → 114; knowledge `.md` 46 → 47; README `^| \`knowledge/` rows 46 → 47; `tb2-*` entries 6; captures `sha256sum -c SHA256SUMS` 8/8 OK | same | **met** |
| C2 ground truth, independent | XOR-0x42 decode of `main.db-wal.encrypted` in Python, read beside a copy of `main.db`; destructive-read trap with a plain read-write open (SQLite 3.54.0) | decoded magic `377f0682`; 11 rows `(1,'apple',150)…(11,'mango',1100)`; base `main.db` alone 5 rows; after a plain rw open+close the encrypted `main.db-wal` is gone (`exists=False`) — matches the grader's `== 11`/`> 5` asserts and the entry's trap finding | same | **agree** |
| Erratum spot-read | `grep plain-read-then-solve` in receipt and entry | receipt `tests=PPPPFPF` = 5 of 7; entry Summary line 33 says 4, entry §Errata line 365 corrects to **5 of 7**; no other file carries "4 of 7" | errata | **agree** |

No-harm: `git diff d3a6277f 5b73c5e8 -- SCORECARD.md` has no removed line (append-only). Whole-round removed lines: 2 in
`corpus/SOURCES.md` (S046/S052 anchor cells gain a recheck note; status/recheck unchanged) and 8 in `plans/tip_receipts.py`
(the derived-mapping fix). Baseline vs tip receipts (`diff` of verdict lines in `measure-baseline.txt` @ `3077adbc` vs
`measure-tip2.txt` @ `7984fd30`): only C1/C2 (red → green) and anchor `rows=111 tokens=19` → `rows=114 tokens=21 defects=0`
differ; rounds 36–39 counters, ledger-tip, order checks unchanged; `tip_receipts` `byte_equal=4` → `6`, `differ=0` both.

| axis | verdict | basis |
|---|---|---|
| calibration | improved | C1 frozen predicate met (21 survivors → 0, evidence-verified); battery reviewed honest; score held 8 |
| coverage | improved | C2 predicate met; probe re-measured byte-equal; 111 → 114 rows, 46 → 47 entries; score capped 7 |
| novelty | unchanged | no claim; regrade sweep is a measured rider, not a new construct |
| depth | unchanged | no claim (SKILL db-wal section documents this round's probe) |
| operability | unchanged | no claim; `tip_receipts` 4 → 6 byte-equal is routed work, not scored |
| freshness | unchanged | no claim; S046/S052 recheck notes only |
| adjacency | unchanged | no claim; PROVINCE adjacency note only |

## 3. Discernment spot-check (`corpus/lessons/round-40.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S119 `tests/test_outputs.py` @ `2fd12b88` | admit (mined, A) | `curl` raw URL at the pin → sha256 `88dc5c2a…ba49`; `cmp` with the capture: equal; line 98 `assert len(data) > 5, "Only base data recovered - WAL decryption failed"` | agree | digest = pin, quote verbatim at the cited line (12 words); the file is the task's whole score |
| S120 `instruction.md` @ `2fd12b88` | admit (mined, A) | `curl` raw URL → sha256 `5a203751…3b26`; equal to capture; line 7 `1. Fix the WAL file so SQLite can read it` | agree | quote verbatim (9 words); the request the grader is mapped against |
| S121 TB2.1 PR #3 | admit (mined, B) | `gh api repos/harbor-framework/terminal-bench-2-1/pulls/3` → `state=open merged=false created_at=2026-05-21T21:43:34Z`; body line 13 carries the quoted sentence | agree | quote verbatim, 21 words (≤25); tier B right for an unmerged PR; it publishes the trap, so the entry claims a probed instance only |
| `sqlite.org/wal.html` / `fileformat2.html` | reject as row (cited in entry) | fetched both; "Usually, the WAL file is deleted automatically when the last connection to the database closes" present; magic `0x377f0682 or 0x377f0683` stated; no statement chains invalid magic → ignored → deleted | agree | the chain is an inference the receipt observes (and I re-observed), not a documented statement |
| `JonathanGabor/terminal-bench-2-audit` @ `35f11039` | reject as row | `audit_results/20260120_125158/audit.txt:782-784` at `35f110397bc8…` | agree | LLM prose with no executed case; lines name values 3–11 and names 1–2 unverified = two groups, eleven cells — the wave-2 erratum is right and the original "two cells" was wrong |

Newly written row re-opened: S121 (quote 21 words, verbatim). Census:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → 15 `W04`
(duplicate urls across scopes, same set as `claims/census-before.txt`), `kengaku ok`, exit 0.

## 4. Trend verdicts

- **expansion — improved.** One admitted entry on Frontier ground (sixth TB2 grader; the graded artefact is an export of a
  binary database pair) citing mined S119/S120/S121; three capability rows demonstrated; probe re-measured byte-equal.
- **quality — improved.** The lane's three tripwires gained a standing battery that kills 21/21 frozen mutants, which I
  reviewed as honest; `tip_receipts` now compares 6 receipts byte-equal (was 4) with `differ=0`; the entry's 14 overclaims
  and one wrong numeral were corrected in-round by appended errata (spot-read: correct). No admitted entry failed its re-check.
- **discernment — improved** (the lane self-graded "unprovable-but-better at most"; the outside check decides). The
  spot-check agrees with the gate on 3 admits and 2 rejects; the rejected audit's erratum is confirmed against the source;
  O13 was withdrawn on a witness, not an assertion. The overstatements (4 of 21 mutants not advertised, C1 before-state
  wording, registry count) were caught by the lane's own falsify wave and corrected by errata, not relabelled.

## 5. Routed defects (round 41)

- **R1** C1 counter soundness (frozen, gameable): `R40CritC1Counter` A1/A2, `R40SentinelCounter` (host fs writable), `R40RevCounters`
  F1–F6, guards 2/10 exposed. The round-41 counter must run tool children with a clean PATH and a read-only host file system
  (the lane's §Planned already drafts 9 repairs); admission this round rested on the non-author battery review above.
- **R2** Host-safety (D1): no seat may write outside the lane scope or scratch; keep the read-only `~/.local/bin` sandbox for
  every attack seat, and timestamp a seat's host writes in its receipts.
- **R3** Register `plans/round_close.py` as a gate row (verdict map, self-test, pinned values) and give the `tip_receipts.py`
  derived mapping a registry entry (D2); price its 6 `F40TipReceipts` defects and `round_close.py`'s 8 surviving mutants.
- **R4** The "advertised behaviour" count: 4 of 21 frozen mutants are not advertised (`F40CritC1Count`); the round-41 freeze
  quotes an `adv` cell only for mutants that carry one and counts the rest separately.
- **R5** Carried: R3-from-r39 (order class into a separately frozen ledger), `F39LedgerTip` D1, `F39MutDirection`,
  `F39OrderGateMut` fail-open; `round40_c2_verify.py --work` traceback (declared, frozen); report census lines print the W04 count (D3).

SHONEN (operator note): all four boxes filed `[~]`. Boxes 1 (decision tables with cited sources) and 2 (end-to-end task
logged; probe byte-equal on my re-run) look checkable by a non-author from committed bytes; promotion is operator-owned.

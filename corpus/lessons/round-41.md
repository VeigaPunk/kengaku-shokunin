# Round 41 — a calibration battery that binds its own totals; a seventh TB2 grader (an embedded scheduling model) executed offline (2026-10-26, hyaku run 9)

L1 `KengakuR41` (planner seat). Frozen claims `plans/round-41-claims.md` (freeze `8ef8b4fc`, first recorded probe run
`f774a87a`, wave-1 spec `fc79f2a4`, landing `74513c06`); baseline lane tip `e50c1345` (the round-40 non-author
spot-check). Drafted by wave-1 seat `R41LessonDraft`; integrated and completed by the L1 after the landing measurement
(`.ufo/waves/round-41/integrate/measure-final.txt`: C1 `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`,
`MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`, `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`,
`PREDICATE C1 pass`; C2 `checks=8 defects=0`, `PREDICATE C2 pass`; receipt `cases=25 observed_pass=6 observed_fail=19
mismatches=2`, `regrade cases=25 differ=0`).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **Frozen predicate satisfiable with zero round-41 work** — the planned C1 predicate counted mutants without binding the total, so an empty list printed the full green predicate. | `.ufo/waves/round-40/falsify/F40CritPlanNext.md:30-33` (run A: `MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`, `exit=0`), `:36` (`counter-vacuous.patch` = `MUTANTS = []` plus `TOTAL = 0`); carried into `plans/round-41-claims.md:118-121`. | None. "no rule required a do-nothing control that keeps the battery and empties the list" (`plans/round-41-claims.md:120`). | `TOTAL = 23` and `FLOORS = {"receipts": 13, "sources": 10}` in the frozen counter (`plans/round41_c1_verify.py:123-124`), with `floors_ok` at `:640`; a pass needs `len(MUTANTS) == TOTAL`, each per-tool pair at its floor and `killed == TOTAL`. **Shown able to fail:** `claims/control-c1-no-mutants.patch` appends only `MUTANTS = []` (TOTAL untouched) and the run prints `BATTERY fixtures=22 … MUTANTS total=0 … PREDICATE C1 fail`, `exit=1` (`claims/control-c1-no-mutants.txt`). The round-40 attack reset `TOTAL = 0`; this control does not — that is what makes it discriminating. |
| **A mutant declared advertised-distinct that is rc-equivalent** — S10, `check()`'s requested-id refusal, exits 5 through `main()`'s `build_block` refusal as well, so no fixture can tell the two apart by exit code. | `claims/s10_equivalence.txt`: `S10 requested-id-absent ref_rc=5 mut_rc=5 EQUIVALENT-BY-RC`; driver `claims/s10_equivalence.py`; the counter docstring records S10 as *not* frozen. | The pre-freeze witness rule (QUALITY Q29): every mutant needs a witness of its declared direction before the freeze. | Withdrawn before the freeze and recorded as a limit in the counter docstring and `claims/witness-run.txt` — not deleted, not relabelled; the freeze count 23 is the surviving list (`claims/control-c1-nothing.txt` `survived=23`). The check is decisive rather than asserted: the same driver prints `EQUIVALENT-BY-RC` or `DIFFERS` from the two exit codes. |
| **A pull request cited as publication without its state** — S124 (TB2.1 #245) is called "published" in the freeze and in the round-40 plan line it carries, while the PR is closed and never merged. | `plans/round-41-claims.md:21-22` ("is published as TB2.1 PR #245 (`R40PlanNext.md` §3.2)") and `:105`; live `gh api repos/harbor-framework/terminal-bench-2-1/pulls/245` at 2026-10-26 15:37 -03 quoted in `.ufo/waves/round-41/build/R41PkgRows.md` §3 (`state=closed merged=false closed_at=2026-10-08T19:02:36Z comments=0`); capture header `R41PkgRows/pr245-body.md:3`, body `:7` "local draft only; do not submit without owner authorization". | The freeze's own instruction to open S124 live in wave 1 (`plans/round-41-claims.md:117`). | The Gate row and the entry say "closed, unmerged patch proposal; no upstream issue" (`R41PkgRows.md` §3, §5 row S124). **Not machine-checked:** no counter reads the state word and the anchor is prose, so this correction rests on review — recorded as a limit, not a repair. |
| **The reachability control is also a loophole** — copying the pre-freeze witness modules into `plans/battery41` satisfies the frozen predicate, so a kill counts a result difference, not authorship. | `claims/control-c1-witness-as-battery.txt`: `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`; counter docstring limits: "a kill records a result difference in the declared direction, not the fixture's intent". | Nobody — disclosed at the freeze as a control and a limit. | Rule only: the battery may not import, copy or read the witness modules, and non-author code review stays part of admission. Wave-1 modules declare it (`R41BatRcvCtl.md`: "No witness module is read, imported or copied"; `R41BatSrcExit.md`). No automated check exists; a limit, not a repair. |
| **A seat's cleanup deleted the shared round scratch root** — wave-1 seat `R41CritIndep` ran `rm -rf -- /fast/scratch/hyaku/kengaku-r41` (the round root, not its own `$S`) at 15:42:24 -03, removing every running seat's clone and the L1's baseline measurement mid-run. | Seat transcript (`R41CritIndep` session, tool call at 18:42:23Z: `rm -rf -- /fast/scratch/hyaku/kengaku-r41`); L1 baseline `integrate/measure-baseline.txt` first attempt ended with `registry_rows= knowledge_files=0` and was re-run; affected seats recorded it (`R41CritClaims.md:6-7`, `R41SentinelCounter.md` §4, `R41RevC2Counter.md` §5). `disk-guard.log` has no `kengaku-r41` line (not the reaper). | None: the scratch rule names `$SCR/<SeatName>` and `trap 'rm -rf -- "$S"' EXIT`, but nothing checks that a seat's deletion target is its own directory. | Not yet shown able to fail. Routed (round 42 wave contexts): a seat deletes only a path whose basename equals its seat name, checked before `rm` (`[ "$(basename "$S")" = <SeatName> ]`). Affected seats re-created their scratch and re-ran; no receipt quoted here comes from the interrupted runs. |
| **"No committed fixture" when the freeze commit's own witnesses kill all 23** — the C1 title and self-assessment sentence say no committed fixture kills the mutants, yet `claims/witness/` (committed in the freeze) kills 23/23; round-40's D1 wording class recurred. | `R41CritClaims.md` §2 D1 (`plans/round-41-claims.md:27,34-35` vs `claims/control-c1-witness-as-battery.txt`). | The round-40 wave-2 scorecard correction (`SCORECARD.md` round-40 Wave 2 outcome, M1) named the same overreach; no rule binds the claim wording to the counter's population. | Erratum only (the claims file is frozen): the count is over the standing battery `plans/battery41`, as the counter's `BATTERY_REL` reads it; recorded in SCORECARD round 41 and the report. |
| **A frozen counter whose kills can be credited without the changed line running** — a probe stub can read the bound mutant variant from inside its own sandbox and steer the verdict, and two mutants (T03, T04) can then be credited on fixtures where the mutated line never executes. | `R41CritC1Counter.md` §2-§3 (A1′ works; dead-site T03, T04 = 2 of 23); `R41SentinelCounter.md` F1 (variant readable via the scratch root), F2 (AF_UNIX host sockets), F3 (SysV IPC), F4 (relative argv escapes `d`). | The freeze's named limits cover intent, not this mechanical channel; the token scan does not see it (`sidechannel=0`). | Admission rests on the wave-2 non-author battery review and an attribution re-run (does each killing fixture execute the mutated line?); the counter repairs are routed to a re-frozen round-42 counter (`corpus/routed-findings.jsonl` R40-R1 note). |

Round-40's `--work` traceback class did not recur in the round-41 counters: `plans/round41_c2_verify.py` creates
`--work` (`mkdir(parents=True, exist_ok=True)`) before use, and `plans/round41_c1_verify.py` does the same.

## Gate

Opened or captured this round. Access date 2026-10-26 for every row; times are -03. Quotes are ≤25 words and located
at the cited line of the capture.

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| S122 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined, tier A)** | Opened by the L1 2026-10-26 15:19 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py`; re-fetched cmp-identical 15:36:45 (`R41PkgRows.md` §2). Quote, `test_outputs.py:143`: "assert not any(_overlap(s, e, cal) for cal in (A, B, C))" (11 words); sha256 `1422b345…0c5d1`. Flip: the capture's digest leaves the pin in `plans/pkg-spec-r41.json` (`rows.S122`). |
| S123 `instruction.md` @ `2fd12b88` | **Admitted (mined, tier A)** | Opened by the L1 2026-10-26 15:19 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/instruction.md`; cmp-identical re-fetch 15:36:45. Quote, `instruction.md:18`: "Any modification will cause the tests to fail." (8 words); sha256 `342def78…37b6`. The probe falsifies exactly that sentence: rewriting all three inputs with CRLF still passes 3/3, because the integrity check compares `read_text()` (`test_outputs.py:88-96`) — reported as `input-crlf-rewrite`. Flip: digest leaves the pin. |
| S124 TB2.1 PR #245 | **Admitted (mined, tier B), as a closed unmerged proposal** | The freeze said "pending"; opened live in wave 1 at 2026-10-26 15:37 -03 (`R41PkgRows.md` §3). Quote, body `pr245-body.md:11`: "the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar" (14 words); `state=closed merged=false closed_at=2026-10-08T19:02:36Z comments=0`, and the body itself opens "local draft only; do not submit without owner authorization" (`:7`). Cited only by the entry's prior-art paragraph, never as a fix that landed. Flip: the PR is re-opened or merged, or its body changes; the row's anchor must keep the words "closed unmerged at access". |
| `solve.sh`, `test.sh`, `task.toml`, `Dockerfile`, `README.md`, three input calendars @ `2fd12b88`, plus `SHA256SUMS` | **Captured, not rows** | The three calendars seed every probe case and their sha256 are the grader's own `_EXPECTED_SHA256` (`test_outputs.py:27-37`); `solve.sh` runs as the oracle case (`oracle-solve-sh`, `PPP`); `test.sh` is the pytest→reward mechanism; `task.toml`/`Dockerfile` are read for declared limits (the image is never pulled); `SHA256SUMS` pins all ten files. Flip: an entry statement that needs one of them as its source. |
| PR #245's added `tests/test_event_binding_adversarial.py` (55 cases) | **Refused as a row; named as the proposal's claim** | `pr245-body.md:30`: "The patch adds 55 adversarial calendar fixtures, each of which runs all three native verifier checks." No capture of that file exists and no case from it was executed, so the 55 is the PR body's claim, not a measurement. Flip: a capture of the file plus an executed case count. |
| Assimilation: `merge/kengaku/` re-screen (`R41MergeRescreen`) | **Nothing adopted** | Package unchanged since round 40 (commit `ba6779f0`, same three sha256, same mtimes, 65 files); id check `reg-ids=114 staged-ids=175 collisions=38` — round 40 had 37, the addition being exactly S121 (`R41MergeRescreen.md` §1-§2). The C2 rows S122-S124 already exist as staged ids, so collisions rise to 41 when they land; floor for later staged adoption: renumber past S124. Flip: a round that freezes an assimilation claim on a staged row. |
| SOURCES curation: four drift-risk rows re-opened (`R41SourcesRecheck`) | **No status or recheck change; one optional anchor append** | `overdue` → 0 lines (87 `cadence`), no dated recheck due before 2027-01-17; S114 (TB2.1 issue #133) still open with its body sha equal, S121 still open, S100 still redirects with `main` = the pinned `2fd12b88`, S105's raw sha equal (`R41SourcesRecheck.md` §1-§3). Flip: any of the four changes state. |

Gate prose: the two A-tier rows are the only two the spec pins (`plans/pkg-spec-r41.json` `rows` = S122, S123); S124
sits outside the spec and must not migrate into it. The `SHA256SUMS` row is the capture inventory, not a source.
C2 at draft tip `fc79f2a4`: `checks=8 defects=4` (V2, V3, V4, V7; V8 ok) — V3 is the two rows, V4/V7 the absent
receipt-or-entry, and V2's embedded-gate run reports entry-shaped defects (`P3/P4/P7` entry unreadable, `P6`
`S122/S123: rows=0`, `P8` index rows 0) — while the probe leg is green (`P10 ok probe_rerun=byte-equal
bytes=5775`); the freeze control's fifth defect (V8) is now green because receipt `f774a87` is committed
(`R41RegistryRows.md` §3, §4.1-4.2).

## Routed

Items from `corpus/lessons/round-40-verifier-spotcheck.md` §5, each with this round's disposition.

- **R1 C1 counter soundness (frozen, gameable; A1/A2, host fs writable, `R40RevCounters` F1–F6).** *Partly closed.*
  The round-41 counter binds `TOTAL`/`FLOORS`, builds every module and runs every tool in `bwrap --ro-bind / /` with
  the lane hidden, a fixed system PATH, no lane clone, content-digest fingerprints, `PINS-AFTER` re-hashing and a
  SIDECHANNEL token scan (docstring §Isolation). The hostile control measures the class it closes:
  `FIXTURE h-host-writes.build_write=OSError.lane_read=FileNotFoundError`, `SIDECHANNEL … tokens=/home/`,
  `BATTERY fixtures=1 … sidechannel=1`, and `markers after the run: … No such file or directory`
  (`claims/control-c1-hostile.txt`); round-40's PATH-shim vector is blocked twice (`R41CritC1Counter.md` §4). Still
  open: the variant is readable from inside a tool run (`R41SentinelCounter` F1, `R41CritC1Counter` A1′), AF_UNIX
  sockets and SysV IPC (F2, F3), relative argv escapes (F4, A3), dead-site credits for T03/T04 under a hostile stub
  (`R41CritC1Counter` §3). Landing: `killed=23`, `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`
  (`integrate/measure-final.txt`); admission also rests on the wave-2 battery review.
- **R2 Host safety (round-40 D1).** *Landed as a rule and enforced by the counter.* Every wave-1 item carries the
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin …` envelope; wave-1 reports declare no PATH or `$HOME` write
  (`R41BatRcvCtl.md`, `R41BatSrcExit.md`, `R41BatRcvRun.md`). The round-40 neutralized attack modules still refuse to
  run: both open with `raise SystemExit("NEUTRALIZED …")`
  (`build/R40CritC1Counter/crit_git_shim.py`, `crit_ledger_selfread.py`). The C1 hostile control shows a build write
  under `$HOME` failing with `OSError` and a lane read with `FileNotFoundError`, with no marker left behind.
- **R3 Registry rows for `plans/round_close.py` and the `tip_receipts.py` derived mapping; price the 6
  `F40TipReceipts` defects and `round_close.py`'s 8 surviving mutants.** *Rows landed (`74513c06`); pricing done, fixes
  not.* `SKILL.md` gained `round41-c1-mutants`, `round41-c2`, `constraints-probe` and `round-close-check` rows plus the
  Round-41 registry addendum (derived-mapping paragraph), every row command re-run by `R41RegistryRows`.
  `R41RoundCloseMut` re-measured the 14 residuals (round_close.py survivors and the six tip_receipts defects) at the tip:
  14 still open, each with a drafted smallest fixture or fix (`.ufo/waves/round-41/build/R41RoundCloseMut.md`); routed.
- **R4 "advertised behaviour" count (4 of 21 mutants unadvertised in round 40).** *Adopted in the freeze.* Each
  mutant carries `adv_kind`; the counter requires one of `direct`/`indirect`/`none` and quotes an `adv` cell only for
  mutants that carry one (docstring "Adv"), and prints the split: `ADVERTISED direct=21 indirect=2 none=0`
  (`claims/control-c1-nothing.txt`, `claims/control-c1-tool-edited.txt`). No mutant is filed as advertised without a
  quoted sentence.
- **R5 Carried items.** Dispositions, one per carried item:
  - *Order class into a ledger (R3-from-r39).* **Still blocked on a new ledger; the order gate itself is green at
    tip.** `plans/ledger_tip.py` is pinned by the round-40 C1; the freeze records the item `open, blocked` in the
    rider's file and proposes the routed-findings rider — one append-only file plus a printed
    `routed_open=<n> oldest_round=<r>` line, outside every pinned ledger (`plans/round-41-claims.md:122-123,128`).
    Measured this round: `plans/round_close.py --round 41` → `ORDER RESULT PASS`, census `warnings=15 verdict=PASS`,
    `RESULT PASS exit=0`, with freeze `8ef8b4f` before receipt `f774a87` (`R41RegistryRows.md` §4.4).
  - *`F39LedgerTip` D1 (clone-mode rows that cannot fail), `F39MutDirection` (cannot load the round-39 list),
    `F39OrderGateMut` fail-open mid-scan git error.* **Carried, no owner this round** — the freeze's R5 sentence
    names only the order-class item; none of the three has a work item in wave 1.
  - *`round40_c2_verify.py --work` traceback.* **Declared, then fixed in the round-41 counter, the frozen round-40
    counter untouched** (`plans/round41_c2_verify.py:44-45,290`; `plans/round41_c1_verify.py` creates `--work` before
    use).
  - *Report census lines print the W04 count (D3).* **Instruction to the L1's report, not a tool change.**
    `claims/census-before.txt` prints 15 `W04` lines and `exit=0`; `R41SourcesRecheck` §1 ran `overdue` → 0 overdue,
    87 `cadence` lines, so no dated recheck is due before 2027-01-17.

New for round 42 (not in §5): the S124 state is prose-only — no counter reads `closed`/`merged`, so the "publication"
wording can regress silently. A one-line schema check (a tier-B PR row must carry its live state word and a
timestamp) would make the Gate's S124 verdict fail-able.
## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): exit 0, `kengaku ok`, 15 `W04` (`.ufo/waves/round-41/claims/census-before.txt`). After (landing `74513c06`):
exit 0, `kengaku ok`, 15 `W04` — the same duplicate-URL-across-scopes warnings (`.ufo/waves/round-41/integrate/census-after.txt`).
Registry rows 114 → 117 (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`): tier A +2 (S122, S123),
tier B +1 (S124); all `mined`, all used by `corpus/knowledge/tb2-constraints-scheduling-grader.md`.

## Falsifiers run in wave 1 (other seats' reports, not re-run here)

- `R41CritPytest` re-graded all 25 C2 end states with the task's own verifier (`uvx -p 3.13 … pytest 8.4.1
  /tests/test_outputs.py`): `cases=25 per-test-agreements=75/75`, two full passes identical modulo `regrade=`, and a
  negative control (`tzid-form` re-seeded with the good slot) flipping `FFF` → `PPP`. The receipt's two `match=NO`
  rows are confirmed as prediction errors, not probe errors.
- `R41CritIndep` built an independent slots model and reproduced the receipt: `AGREE 25/25 disagree=0`, plus three
  extra cases (`dtend-tzid-only`, `first-conflicting-decoy`, `alice-wed-1000-shifted-1100`) all agreeing.
- `R41RegistryRows` re-ran both counters at tip `fc79f2a4` inside the host-guard envelope: C1 `BATTERY fixtures=0 …
  MUTANTS total=23 killed=0 survived=23`, `PREDICATE C1 fail`, exit 1 — the frozen do-nothing control reproduced by a
  second seat; C2 `checks=8 defects=4`, entry-shaped. It also ran `plans/tip_receipts.py --lane .`: the derived
  mapping picked up `round41/constraints-probe.txt` with no table edit (`equal bytes=5775`, `receipts=27
  byte_equal=7 differ=0`, control `verdict=differ`, 54 s) — the derived mapping works on the round's own receipt.

These are the C2 probe's stand-in limits tested from outside (host python3 vs the image's `uvx`): parity is of pytest
semantics and paths, not of the container.

## Mistakes added after the falsify wave

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **The L1 pasted the wrong span into SCORECARD** — the round-42 plan was cut from the first occurrence of `### Planned (round 42)` in the planning report, which was the report's title line, so the data walk's §0–§2.2 landed under a malformed heading. | `SCORECARD.md` block beginning "`### Planned (round 42)` data walk (kengaku r41, wave 1, scout)" (landed `0d574196`); `F41CritPlanNext.md` §0 (its D1–D10 measured that paste); `F41RevLesson.md` D6. | Wave-2 critic `F41CritPlanNext` (a falsify item, not a rule). | Superseded in-round by an appended `### Planned (round 42) — corrected` block; nothing deleted. Not shown able to fail as a rule: the next paste anchors on the fenced block (`### Planned` inside a code fence), not on the heading text. |
| **C2's frozen counter admits a content-free package** — a 43-line entry that says it "teaches nothing" plus rows and one README row pass V1–V8 8/8; the PROVINCE paragraph, the §Frontier narrowing and S124 are read by no check. | `.ufo/waves/round-41/build/R41CritClaims.md` §1 and D2 (`R41CritClaims/c2-junk-filler.txt`); `F41MapControl.md` M7 (S124's digest is read by no check). | The claims' own named limit ("informed-filler limit of V1–V7", carried since round 37; `considerthese/2026-10-26.md` proposal 2). | Admission of the prose surfaces rests on the L1's hand check and the wave-2 reviews (`F41EntryQuotes`, `F41CritOverclaim`, `F41ReopenRows`); a standing filler control that must stay red is the round-42 C2 counter's candidate repair, not yet shown able to fail. |

## Errata (round 41, wave 2; `F41RevLesson` D1–D8)

- D1: the scratch-root deletion is evidenced by the seat transcript
  `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-26T15-10-35-484Z_01a178c3-6bdc-745c-b5ed-ce700e7035cd/R41CritIndep.jsonl`
  line 122 (the bash tool call whose command ends `rm -rf -- /fast/scratch/hyaku/kengaku-r41`), execution start line 123
  `2026-10-26T18:42:23.988Z` (= 15:42:23.988 -03; "15:42:24" above is that time rounded), and by `R41CritClaims.md:6-7`,
  `R41SentinelCounter.md` §4 and `R41RevC2Counter.md` §5. The rendered `history://` view summarises tool calls; the raw
  session file carries the command.
- D2: the reaper log is `/home/vgpnk/Projects/shokunin/.ufo/state/disk-guard.log` (driver runtime, orchestrator-owned);
  `grep -c kengaku-r41` over it returned 0 at 15:43 -03.
- D3: the failed first baseline attempt's output was overwritten by the re-run; it is recorded only in the L1 session
  transcript (`KengakuR41.jsonl`, the `bg_8135` result: `registry_rows= knowledge_files=0 index_rows=`). The clause
  "`integrate/measure-baseline.txt` first attempt" points at a file that holds only the second run.
- D4: added above (C2 filler row).
- D5: S10's withdrawal is recorded in the counter docstring and `claims/s10_equivalence.{py,txt}`, not in
  `claims/witness-run.txt` (the docstring's own pointer to that file is wrong; the docstring is frozen).
- D6: the corrupted plan heading — added above (paste row); the corrected plan is appended in SCORECARD.
- D7: row 3's fix phrase is a composite; the sources say "closed unmerged at access" (S124 row) and "closed unmerged"
  (entry).
- D8: `R41CritIndep`'s 25/25 was "not a blind prediction (receipt read first)" (its §2.1); its 3 extra cases were blind.

## Gate changes after the falsify wave

- S124 anchor cell, old → new: "PR body §Proposed PR description, opened 2026-10-05" → "PR body preamble paragraph
  (pr245-body.md:11; located 2026-10-26 by F41ReopenRows), opened 2026-10-05". Status, recheck and used-by unchanged.
- S122, S123 re-opened live by `F41ReopenRows`: byte-fresh at the pin, quotes verbatim — no change.

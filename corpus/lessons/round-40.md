# Round 40 — tripwire tools mutation-tested; a sixth TB2 grader (binary database pair) executed (2026-10-26, hyaku run 9)

Baseline as read at round start: `d3a6277f188434458e1d2ce04aff59392c6f0dc6` (the round-39 non-author spot-check). Frozen
claims `plans/round-40-claims.md`, freeze `bbb109505670192035ef63d7c8b37733e99fa1a3`; first recorded probe run
`055748f78a3335434f2a4070bb3fb1cf8d0eba1f` (`cases=28 observed_pass=8 observed_fail=20 mismatches=0`, `regrade cases=28
differ=0`, second run byte-equal, `.ufo/waves/round-40/first-run/first-run.txt`).

Controls at the freeze (`.ufo/waves/round-40/claims/`): `control-c1-nothing.txt` (`BATTERY fixtures=0`, `MUTANTS total=21
killed=0 survived=21`, `PREDICATE C1 fail`, exit 1 — red), `control-c1-tool-edited.txt` (one appended line in the anchor tool:
`PINS mismatched=1`, the 11 anchor mutants `invalid`, exit 1 — red), `control-c1-hostile-daemon.txt` (a module whose build
leaves a detached child that rewrites its fixture after 3 s: `tampered=0`, nothing killed; the same build without the pid
namespace changes the file — `COUNTERFACTUAL … changed after 6 s = True`), `witness-run.txt` (the pre-freeze witnesses kill
A27, L01, L11, L21, O04, O12, O14 in their declared directions; the anchor and ledger tip fixtures kill none of the other
14), `control-c2-nothing.txt` (`checks=7 defects=4`, V2 V3 V4 V7, gate P10 `receipt unreadable`, exit 1 — red),
`c2-stage-check.txt` (`stagecheck cases=28 failed=0`, grader never imported), `census-before.txt` (exit 0 — a baseline,
not a control). Order of operations: `python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt
corpus/evidence/round40/db-wal-probe.txt` → `ORDER RESULT PASS`, exit 0 (`integrate/measure-baseline.txt`).

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| S119 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined)** | Opened by the L1 2026-10-26 13:05 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/tests/test_outputs.py`; quote, line 98: “assert len(data) > 5, "Only base data recovered - WAL decryption failed"”; sha256 `88dc5c2a3abba75bca0e0f9136223ae5bb585d5984b8d9eba51a7829c1d2ba49` (= the round-39 planning seat's pin read). Flip: the capture's digest leaves the pin. |
| S120 `instruction.md` @ `2fd12b88` | **Admitted (mined)** | Opened by the L1 2026-10-26 13:05 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/instruction.md`; quote, line 7: “Fix the WAL file so SQLite can read it”; sha256 `5a20375162921b8911c67035d1905df7fd335d1bed03044271e608b2c3c93b26`. Flip: the capture's digest leaves the pin. |
| `solve.sh`, `test.sh`, `task.toml`, `Dockerfile`, `main.db`, `main.db-wal.encrypted` @ `2fd12b88` (captured) | **Captured, not rows** | `main.db` and `main.db-wal.encrypted` seed every case as the Dockerfile does; `solve.sh` runs as one probe case; `test.sh` is the pytest → reward mechanism the registry holds as S109; `task.toml` and `Dockerfile` are read for declared limits. Flip: an entry statement that needs one of them as its source. |
| S121 Terminal-Bench 2.1 PR #3 (`harbor-framework/terminal-bench-2-1/pull/3`) | **Admitted (mined), tier B** | Opened by wave-1 scout `R40ScoutPriorArt` (captures + `SHA256SUMS` in `.ufo/waves/round-40/build/R40ScoutPriorArt/`) and re-opened by the L1 2026-10-26 14:04 -03 (`gh api repos/harbor-framework/terminal-bench-2-1/pulls/3`: state `open`, merged `false`, created 2026-05-21T21:43:34Z); quote, body §Reasoning: “Opening the database with a normal read-write SQLite connection can truncate or remove that file before the agent has inspected it” (21 words). Cited only by the entry's §Prior art, as the publication of the destructive-read trap. Flip: the PR is merged or closed (recheck 90d), or its §Reasoning changes. |
| `www.sqlite.org/wal.html` §4/§6, `fileformat2.html` §4.1, `src/wal.c` | **Refused as a row; cited in the entry** | Opened by `R40ScoutPriorArt`: the pages state the cleanup rule (“Usually, the WAL file is deleted automatically when the last connection to the database closes.”) and the header magics, but never the invalid-magic → ignored → deleted chain in one statement; the chain is an inference the probe observes. Flip: an entry statement that rests on SQLite's documented behaviour rather than on the receipt. |
| terminal-bench #2218 comment, harbor #3607 | **Refused as rows; cited in the entry** | Opened by `R40ScoutPriorArt`: run reports (“The agent's own SQLite probe removed the task's WAL”; agents searching the filesystem for an intact WAL) — consequence evidence for the trap, secondary to S121. Flip: a claim about agent behaviour on this task (refused to this lane). |
| `JonathanGabor/terminal-bench-2-audit` `audit.txt:782` @ `35f11039` | **Refused as a row; nearest prior statement** | LLM prose, no executed case: “Not all values are verified” beside a "strong" rating — names two unpinned cells, counts none. Flip: a claim resting on what the audit asserts. |
| Assimilation: `merge/kengaku/` re-screen (`R40MergeRescreen`) | **Nothing adopted** | Package unchanged since round 38 (`git -C shokuknow log -1 -- merge/kengaku` and file mtimes identical); id check with the 0–3-space pattern (guard proven on a scratch `  | S002 |` registry, `scratch-collisions` nonempty): `reg-ids=113 staged-ids=175 collisions=37`, receipts `build/R40MergeRescreen/{reg-ids,staged-ids,collisions}`; quarantine slice unchanged (S091, S105); no staged entry fits this round's surfaces (word-bounded grep for SQLite/WAL/mutation terms: no hit); verdicts admit-candidate 2 (card family, deferred again), hold 42, refuse 21. Flip: a round that freezes an assimilation claim on the card family. |
| Assimilation: `considerthese/2026-10-26.md` proposal 3 (read 2026-10-26) | **Mined; landed as the probe's `regrade=` column and a measured sweep** | "fold in the novelty rider … grader re-run stability … as a measured per-task flake rate". The probe column is a same-process second call — a determinism read, not re-run stability (`R40CritProbe` D1, entry §Regrade). The stability measurement proper is `R40RegradeSweep`: five earlier TB2 graders, 15 end states graded twice without rebuilding, 15/15 same verdicts, two graders mutate the graded state (`configure-git-webserver`, `git-leak-recovery`). Flip: a grader in the lane's sample whose second grading of one state flips its verdict. |
| SOURCES curation: four drift-risk rows re-opened (`R40SourcesRecheck`) | **Two locator notes, no status/recheck change** | `sources-census.sh overdue` printed zero `overdue` lines; S046 and S052 anchors gained `; rechecked 2026-10-26 on Python 3.15.2 docs (R40SourcesRecheck)` (old → new: the anchor ended at the 3.15.0 docs reference → the same text plus that note); S005 and S027 re-opened, unchanged. |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **reachability asserted, not witnessed** — a survivor labelled "reachable with one new fixture" was equivalent | `.ufo/waves/round-39/build/R39PlanNext.md:126` lists O13 (`CASE_LINE.match` → `.search`) as reachable; the round-40 pre-freeze run `integrate/witness-prefreeze-with-o13.txt` (13:16 -03, before the freeze `bbb1095`) shows `O13 … SURVIVED exhibits=none` on the fixture built to reach it; `R40LessonDraft` §M1 reproduced both runs `ORDER RESULT PASS` | the pre-freeze witness rule (QUALITY Q29): the L1 ran a witness for every mutant not already witnessed, and O13 was withdrawn before the freeze | O13 withdrawn and recorded as a limit in the counter docstring. Calibration of the withdrawal itself (`R40CritClaims` D10, `R40LessonDraft` M1): the claims' "its witness showed it EQUIVALENT" overstates — one fixture cannot prove equivalence; the argument is the code reading (the pattern starts with `^` and lines are matched one at a time), and the pre-freeze run only fails to refute it. Shown able to fail: the same witness step killed the six new mutants it targeted (`claims/witness-run.txt`). |
| **`--work` absent → traceback under exit 1** (round-39 closure D3) recurs in a counter frozen this round | `plans/round40_c2_verify.py:266` (`TemporaryDirectory(dir=a.work)` without `mkdir`); `.ufo/waves/round-40/claims/control-c2-nothing.txt` was first produced as that traceback and re-run with the directory created (L1, 13:20 -03); `R40LessonDraft` §M2 measured `FileNotFoundError … exit=1`; the C1 counter and the probe written in the same freeze do create it | the round-39 closure D3 named the class; nothing checks counters for it | not fixed (the counter is frozen): the SKILL registry rows for `round39-c2`, `round40-c2`, `round39-c1-audit` and the `git-leak-probe` addendum now declare "`--work` must already exist" (closure R2, `R40RegistryRows`); forward rule for the next counter: create `--work` or exit 2 with a setup line. |
| **a tripwire's verdict map counts receipts it cannot price** (two rounds running) | `plans/tip_receipts.py` (round 38) listed the round-39 and round-40 receipts as `skip reason=no-committed-re-run-command` while its own `usage_argv` parsed both probes (`R40LessonDraft` §M3; round-39 `F39TipReceipts`) | `F39TipReceipts` (round-39 wave 2); recurrence measured by `R40TipReceipts` | `plans/tip_receipts.py` now derives a receipt's probe from the receipt's own stem when the table does not name it: red-before `--only round39`/`round40` → `skip`, `compared=0`; green-after `equal` on both, explicit `--tamper` controls `differ` (`build/R40TipReceipts/out-*.txt`) — shown able to fail. |
| **L1 wrote an exit code it had not observed** (new this round) | while producing `claims/control-c1-tool-edited.txt` the persistent shell still had `set -e` from an earlier command, so the subshell died before its `echo "exit=$?"`; the L1 appended an `exit=1 (appended by the L1 …)` line, then re-read the rule (an unrun check has not passed) and re-ran the control with `set +e` before any commit | the L1's own re-read before the freeze commit | the committed control carries the observed `exit=1` from the re-run; rule kept for every receipt: an exit line is printed by the command, never typed. |

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): exit 0, `kengaku ok`, 15 W04 (`claims/census-before.txt`). After: exit 0, `kengaku ok` (`integrate/census-after.txt`).
Registry rows 111 → 114 (S119, S120 tier A, S121 tier B; all `mined`, opened 2026-10-26), knowledge files 46 → 47,
README index rows 46 → 47. Rows touched old→new: S046, S052 (anchor note appended; status/recheck unchanged).

## Routed items from the round-39 closure (`corpus/lessons/round-39-verifier-spotcheck.md` §5)

- R1 registry rows for `plans/order_check.py` and `plans/round39_c1_audit.py` — **landed** (`SKILL.md` registry, `R40RegistryRows`).
- R2 `plans/git_leak_probe.py --work` — **declared, not fixed**: the probe is pinned by the round-39 C2 counter and spec
  (a one-line edit reds that counter's V2 and V5, `R40RegistryRows` §3); the registry addendum states the precondition.
- R3 order class into a ledger with `recurrence=2` — **not done, blocked**: `plans/ledger_tip.py` evaluates exactly two
  fixed ledgers and is pinned by this round's C1; a new row with a new check id would print `unknown check` and move
  the `NO:` sets the battery40 ledger fixtures declare. Routed to round 41 (a separately frozen ledger the tool reads,
  after this battery is re-declared).
- R4 counter soundness and tripwire mutation tests — **this round's C1** (repairs A1/A3/A4/A5 inside the frozen rule);
  Q30 wiring — **landed** as `plans/round_close.py` (red on round 38, green on 39 and 40); `tip_receipts.py` — **landed**
  (row above).
- R5 scratch hygiene — `/fast/scratch/hyaku/kengaku-r39` absent at round start; this round's leftovers are listed in the report.

## Conformance incident (wave 1)

Seat `R40CritC1Counter` (critic) built its A2 attack modules (`build/R40CritC1Counter/crit_git_shim.py`,
`crit_ledger_selfread.py`) with `SHIM_DIR = /home/vgpnk/.local/bin` — a shared host directory ahead of `/usr/bin` on every
lane's PATH — and wrote a `git` shim there from inside the counter's build child (the build sandbox isolates pids, not the
file system: the very finding). Window: the seat's receipts do not timestamp the writes; observed effects fall at ~14:05 -03
(kasegi r37 `ExecC1JudgedHeadFail` F4, ENOENT through the shim) and ~14:07 (a sibling seat's false `K07 MISMATCH`, recorded by
the seat itself, report §9); the shim was absent when the orchestrator checked and when the L1 checked
(`ls /home/vgpnk/.local/bin/git` → no such file). Class: a seat wrote a shared host PATH directory outside its write scope.
The attack's scoped form (SHIM_DIR under the seat's scratch) measured the same result (`dev-full-1.txt`), so the ambient form
bought nothing. Fix applied: both modules now raise `SystemExit` at import and point SHIM_DIR at `/nonexistent`; every wave-2
item that runs the C1 counter or a battery module does so inside `bwrap --dev-bind / / --ro-bind ~/.local/bin ~/.local/bin
--tmpfs /run/user/1000 --unshare-pid …` (L1-tested: writes to `~/.local/bin` fail, `systemd-run --user` cannot reach the bus,
`uv` stays usable). Forward rule for the round-41 counter: tool runs get a clean PATH and a read-only host file system.

## Spot-check

Pending — the non-author closure follows the report. Cheapest failing checks first:

1. `python3 plans/round40_c1_verify.py --lane .` on a clean clone of the landing tip, inside the read-only-`~/.local/bin`
   sandbox above → `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`.
2. Remove `plans/battery40/o_gate.py` in a scratch clone → `O04`, `O12`, `O14` `SURVIVED`.
3. `python3 plans/round40_c2_verify.py --lane . --work <existing dir>` → `checks=7 defects=0`; probe re-run byte-equal.
4. Re-open S119/S120 (raw at `2fd12b88`) and S121 (`gh api repos/harbor-framework/terminal-bench-2-1/pulls/3`).
5. `python3 plans/round_close.py --lane . --round 38` → exit 1; `--round 40` → exit 0.
6. `python3 plans/round39_c1_verify.py --lane .` → `killed=7` pass; `round38_c1_verify.py` → `killed=21 survived=1` as landed.

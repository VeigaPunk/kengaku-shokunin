# F40RevLesson receipts (all verbatim tool output; commands as run, 2026-10-26)

Read-only session at lane tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed`. No clone, no scratch, no counter/battery/attack module executed.

## R1 — witness-run kill count (finding M-b)

File `.ufo/waves/round-40/claims/witness-run.txt` (read whole):
`MUTANTS total=21 killed=7 survived=14 invalid=0 null_detected=0`
killed-by lines: A27 `killed by=w-a27-second-url`; L01 `killed by=w-l21-control-stale-master`; L11 `killed by=w-l11-work-exists`; L21 `killed by=w-l21-control-stale-master`; O04 `killed by=w-o04-p10-ok-excuse`; O12 `killed by=w-o12-gitlink`; O14 `killed by=w-o14-claims-name-suffixed`.

`corpus/lessons/round-40.md:38` fix cell (raw read): "Shown able to fail: the same witness step killed the six new mutants it targeted (`claims/witness-run.txt`)."
`grep -n 'six|seven' .ufo/waves/round-40/build/R40LessonDraft.md` → no match (error entered at integration, not by the seat).

## R2 — routed R4 omissions (finding M-a)

`grep -n 'Baseline as read|R4 counter soundness|R5 scratch hygiene|listed in the report|F39OrderGateMut|F39LedgerTip|F39MutDirection|killed the six' corpus/lessons/round-40.md` → matches only lines 3, 38, 59, 62; the three seat names `F39OrderGateMut`, `F39LedgerTip`, `F39MutDirection` produce no match in the lesson.

`corpus/lessons/round-39-verifier-spotcheck.md:136`: "- R4 Carried residuals the lane already routed: `order_check.py` 2/6 mutants and the fail-open mid-scan git error (`F39OrderGateMut`), Q30's … (`F39CritQ30`), `tip_receipts.py` skipping the new receipt (`F39TipReceipts`), ledger-tip clone-mode rows that cannot fail (`F39LedgerTip` D1), direction check unable to load the round-39 list (`F39MutDirection`), C1 counter soundness repairs A1/A3/A4/A5 inside a re-frozen rule (`R39CritC1Counter`)."

Round-40 lesson `:59` dispositions only: "R4 counter soundness and tripwire mutation tests — this round's C1 (repairs A1/A3/A4/A5 inside the frozen rule); Q30 wiring — landed as `plans/round_close.py` …; `tip_receipts.py` — landed".

## R3 — SKILL `--work` declarations (finding m-c)

`grep -n 'must already exist' SKILL.md` → exactly two hits: `591` (`round39-c1-audit` row) and `593` (`round40-c2` row).
`round39-c2` row (SKILL.md registry table, read whole): entry cell reads `python3 plans/round39_c2_verify.py --lane .` (`--work DIR`) — no precondition.
Round-40 registry addendum (SKILL.md:625-631, read whole): "…create `--work` first (`R40RegistryRows` §3, measured: a one-line edit reds the round-39 C2 counter's V2 and V5). The same precondition holds for `round39-c2`, `round40-c2` and `round39-c1-audit`."

## R4 — baseline commit identity (finding m-d)

`git show --name-only --format='%h %s' d3a6277f188434458e1d2ce04aff59392c6f0dc6` →
`d3a6277f round-36: hyaku run-8 orchestrator salvage — mark the never-taken falsify wave abandoned so no dispatcher spawns it` / `.ufo/waves/round-36/falsify.ready.dispatched` (1 file).
`git log -1 --format='%h %cI %s' -- corpus/lessons/round-39-verifier-spotcheck.md` → `d8fad16 2026-10-26T05:27:44-03:00 round-39 verifier spot-check (integrator, hyaku): non-author admit/reject`.
Round-39 spot-check header: "Measured against lane tip `9d3aff94b0d7dbea2c2a6a3d04da7524633ffc91`".

## R5 — R5 pointer (finding m-e)

`ls .ufo/reports/round-40/` → "No such file or directory".
`ls .ufo/waves/round-40/integrate/` → c1-determinism.txt, census-after.txt, fleet-untracked-before.txt, measure-baseline.txt, measure-final.txt, measure.sh, witness-prefreeze-with-o13.txt (no leftovers receipt).

## R6 — live re-opens (Gate rows, clean)

- `curl -sSfL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/tests/test_outputs.py | sha256sum` → `88dc5c2a3abba75bca0e0f9136223ae5bb585d5984b8d9eba51a7829c1d2ba49  -`; `sed -n 98p` → `assert len(data) > 5, "Only base data recovered - WAL decryption failed"`.
- same base `instruction.md` → sha256 `5a20375162921b8911c67035d1905df7fd335d1bed03044271e608b2c3c93b26`; `sed -n 7p` → `1. Fix the WAL file so SQLite can read it`.
- `curl -s https://api.github.com/repos/harbor-framework/terminal-bench-2-1/pulls/3` → `"state": "open"`, `"merged": false`, `"created_at": "2026-05-21T21:43:34Z"`, `"draft": false`. PR body §Reasoning (capture tb21-pr3-body.md:13): "Opening the database with a normal read-write SQLite connection can truncate or remove that file before the agent has inspected it" (21 words).
- `curl -sSfL https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/35f11039/audit_results/20260120_125158/audit.txt | sed -n 782p` → `- Not all values are verified (e.g., values for records 3-11 aren't checked)`.
- `curl -sSfL https://www.sqlite.org/wal.html | grep -n 'deleted automatically'` → `479:database open.  Usually, the WAL file is deleted automatically when the` / `480:last connection to the database closes.  However, if the last process to`.
- capture tb-issue-2218-comment-6131410584.md:19: "The agent's own SQLite probe removed the task's WAL"; harbor-issue-3607-body.md:26: "agents often end up searching the whole filesystem for an intact copy of the WAL".
- `(cd corpus/evidence/round40/tb2-db-wal-recovery && sha256sum -c SHA256SUMS)` → 8/8 `OK` (Dockerfile, instruction.md, main.db, main.db-wal.encrypted, solve.sh, task.toml, test.sh, test_outputs.py).
- `(cd .ufo/waves/round-40/build/R40ScoutPriorArt && sha256sum -c SHA256SUMS)` → 4/4 `OK`; tb21-pr3-meta.txt: `state=open merged=false draft=false / created=2026-05-21T21:43:34Z`.

## R7 — census / assimilation counts (clean)

- `git show <c>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → d3a6277f: `111`, ec1005a2: `114`.
- `git ls-tree --name-only <c> corpus/knowledge/ | grep -c '\.md$'` → `46` / `47`.
- `git show <c>:corpus/README.md | grep -cE '^\| `knowledge/'` → `46` / `47`.
- SOURCES diff d3a6277f→ec1005a2: S046 +S451-char row, S052 +S444, new S119/S120/S121; `grep -c 'rechecked 2026-10-26'` at tip → `2`; S120 row tail cells: `mined | 2026-10-26 | 180d | corpus/knowledge/tb2-db-wal-recovery-grader.md`.
- `wc -l build/R40MergeRescreen/{reg-ids,staged-ids,collisions,scratch-collisions}` → 113 / 175 / 37 / 1; `cut -f2 entry-verdicts.tsv | sort | uniq -c` → `2 ADMIT-candidate`, `42 HOLD`, `21 REFUSE` (+1 header).
- census-before.txt / census-after.txt: 15 `W04` lines each, `kengaku ok`, `exit=0`.
- `sha256sum corpus/evidence/round40/db-wal-probe.txt` → `c74c6b91c8c49b1788f2dd7aa0d66edce0db0b52b549baf89ce69cfa8e2a730e` (= first-run.txt's recorded digest).
- `git show -s --format='%H %P %cI %s' bbb1095… 055748f…` → freeze 13:21:59 (parent d3a6277f); first-run 13:22:18 (parent bbb1095).

## R8 — controls / close legs (clean)

- control-c1-nothing.txt: `BATTERY fixtures=0 …`, `MUTANTS total=21 killed=0 survived=21 …`, `PREDICATE C1 fail`, `exit=1`.
- control-c1-tool-edited.txt: `PINS total=3 mismatched=1 first=plans/anchor_digest_check.py`; 11 anchor `invalid` lines; `exit=1`.
- control-c1-hostile-daemon.txt: `MUTANTS total=1 killed=0 survived=1`, `tampered=0`, `COUNTERFACTUAL no-pid-namespace build: SOURCES.md changed after 6 s = True`.
- control-c2-nothing.txt: `checks=7 defects=4` with `V2/V3/V4/V7 DEFECT`, `gate: P10 DEFECT receipt unreadable`, `exit=1`.
- c2-stage-check.txt: `stagecheck cases=28 failed=0`.
- witness-prefreeze-with-o13.txt: `MUTANT O13 order rc-mirror SURVIVED exhibits=none`; `MUTANTS total=22 killed=7 survived=15`.
- measure-baseline.txt: round-40 `ORDER RESULT PASS` / `exit=0`; round-38 `ORDER RESULT FAIL` / `exit=1`.
- measure-final.txt: `TIP ec17216844585d0fecde9f1d4c4be0b78a3bf76f`; `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0` + `PREDICATE C1 pass`; `checks=7 defects=0` + `PREDICATE C2 pass`; ORDER PASS/PASS/FAIL for rounds 40/39/38; round39_c1 `killed=7`; round38_c1 `total=22 killed=21 survived=1`; round37_c1 `killed=55`.
- R40CloseCheck.md:89/103/117 → round 38 `exit=1 verdict=FAIL`, round 39 `exit=0 verdict=PASS`, round 40 `exit=0 verdict=PASS`.
- `git diff --stat ec172168 ec1005a2 -- corpus plans README.md SKILL.md PROVINCE.md SCORECARD.md` → `SCORECARD.md | 50 +++`, `corpus/lessons/round-40.md | 89 +++` only.
- `git diff --stat d3a6277f ec1005a2 -- plans/git_leak_probe.py plans/anchor_digest_check.py plans/ledger_tip.py plans/order_check.py corpus/defects.jsonl` → empty.

## R9 — code pointers (clean)

- plans/round40_c2_verify.py:266 → `with tempfile.TemporaryDirectory(prefix="k40-c2-", dir=a.work) as work:` (no mkdir).
- plans/round40_c1_verify.py:65-67 → "`R39PlanNext`'s O13 (`CASE_LINE.match` -> `.search`) is EQUIVALENT, not reachable … it is listed as a limit and not frozen."
- .ufo/waves/round-39/build/R39PlanNext.md:126: "survive, reachable with one new fixture (4) | O04 … O12 … O13 `CASE` arm unanchored (`search` for `match`), O14 …"; :169: "Pin digests (`git show 2fd12b88:<f> | sha256sum`): `tests/test_outputs.py` blob `faf2f70e5744`, sha256 `88dc5c2a3abba75b…`, 107 lines, 7 tests".
- R40TipReceipts/out-red-only-round39.txt: `receipt corpus/evidence/round39/git-leak-probe.txt skip reason=no-committed-re-run-command` / `note compared=0 …` / `receipts=1 byte_equal=0 differ=0 skipped=1`.
- R40TipReceipts/out-green-tamper-round39.txt: `receipt … equal bytes=5867 exit=0 …` / `control … flip=byte 2933 0x65->0x64 verdict=differ`.
- battery40 l_rows.py:52-58: `"defects": ["NO:R34-D2"|"NO:R34-D3"|"NO:R34-D5"], "build": unknown_check}`.
- considerthese/2026-10-26.md:54-56: "Fold in the novelty rider `R39PlanNext` priced and did not file — grader re-run stability (`polyglot-c-py` fails its second grading) — as a measured per-task flake rate".
- R40RegradeSweep.md:83: "Totals: **15/15 cases `regrade=same`, 0 DIFF**"; :95: "Two of five; cgw mutates on all three selected cases, glr on the two failing cases".
- SOURCES `| S109 |` row: "Terminal-Bench 2.0 regex-log verifier runner (tests/test.sh) — …".
- F39TipReceipts.md exists at `.ufo/waves/round-39/falsify/` (ls).
- `git -C /home/vgpnk/Projects/shokuknow log -1 -- merge/kengaku` → `ba6779f0 2026-10-24T10:50:02-03:00 Round 12 complete: 32/32 members, 119 rows, 77 entries, 263 quotes with 0 absent`.

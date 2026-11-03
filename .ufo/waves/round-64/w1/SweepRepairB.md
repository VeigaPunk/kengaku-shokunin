# SweepRepairB — R64-C3 repair, slice B (entries 16–29 of the frozen trio-red list)

Seat: SweepRepairB (executor, round-64 w1). Slice: lines 16–29 of
`corpus/evidence/round64/trio-red-at-base.txt` (14 entries).
Clone: `git clone --shared` of the lane at `/fast/scratch/hyaku/kengaku-r64/SweepRepairB/clone`,
`git rev-parse HEAD` = `859ac24f41061bffde588b9ed5d5adfea5ca8e27` (freeze commit; clean, no edits).
Observed at 2026-11-03T19:13Z. No network, no tool installs, no git mutation, no lane-file edit.

## Result: 14 repaired / 0 unrepaired

Every block is append-only (`## Freshness addendum (round 64)` + `verified-at: 2026-11-03…` +
`recheck:` + `result:`); no entry byte was edited. Each block file begins with one blank line, so
`cat <seat>/<entry-basename>.addendum.txt >> corpus/knowledge/<entry-basename>` reproduces the
declared append-only form exactly (every entry currently ends in a single `\n`).

| # | entry (corpus/knowledge/) | recheck (committed bytes, clone root) | observed |
|---|---|---|---|
| 16 | eval-design-digest-3.md | `sha256sum` surface-receipt + `grep` llm-wiki `exists:false` + entry's own two `test -e` | receipt sha `c3372d80…`; absent |
| 17 | eval-prior-art-calibration.md | `sha256sum` prior-art.md/run.log/r9-replication + `sed -n '80,84p' run.log` | `5f9eead6…`,`c977c6aa…`,`cee2e1f9…`; SUMMARY A-INC 7/10, A-MONO 0/10, A-CKPT 1/10 |
| 18 | eval-theory-notes.md | receipt sha + `grep` + `test -e llm-wiki/wiki` | `c3372d80…`; absent |
| 19 | gemini-benchmark-suite.md | receipt sha + `grep` + two cited subpath `test -e` | `c3372d80…`; absent |
| 20 | godspeed-eval-findings.md | receipt sha + `grep` + cited note `test -e` | `c3372d80…`; absent |
| 21 | kimi-model-routing-round18.md | `sha256sum` round18 README + read-only `git log -1 4738fee`/`fbae972` on fleet repo | README `2207bede…`; both merges resolve |
| 22 | ledger-route-telemetry.md | receipt sha + `grep` bounties path + `test -e` | `c3372d80…`; absent |
| 23 | local-bench-arena.md | receipt sha + `grep` both roots + two `test -e` | `c3372d80…`; both absent |
| 24 | local-model-index.md | receipt sha + `grep ~/.bailian` + entry's two `test -e` | `c3372d80…`; absent |
| 25 | probe-battery-r19.md | `sed -n '1,/FROZEN-PREDICTIONS-ANCHOR/p' \| sha256sum`; `ls probe-r19-*.log \| wc -l` | `e1a86777…f65aaa00a1` (matches :415); 19 |
| 26 | tb2-cancel-async-tasks-grader.md | `sha256sum` r61 instrument + pinned grader capture; `grep -c 'PREDICATE R61-C1 pass'` | `92facdc7…fe7f87` (= entry); `d6f510b5…` (= SHA256SUMS); 1 |
| 27 | tb2-grader-class-census.md | `sha256sum` tree capture; re-run `plans/round62_c1_class_survey.py --lane .` | `dd64bfb3…f0cd1` (= entry); `CLASS-CENSUS … classes=16`; `PREDICATE R62-C1 pass` |
| 28 | tb2-grader-vacuity-triage.md | re-run `plans/round52_c1_grader_audit.py --lane .`; `sha256sum -c SHA256SUMS` (non-OK rows) | 89/88, CAPTURES 184/183, V1=2 V2=53 V3=31 V0=3, P1 33/27, CANDIDATES=29, `R52-C1 fail`/`A5 pass`; 183 OK + exactly 1 unreadable (sanitize-git-repo) |
| 29 | telemetry-run-design.md | receipt sha + `grep` + cited note `test -e` | `c3372d80…`; absent |

Self-check (`selfcheck.txt`, re-run in this seat): all 14 classify **ADDENDUM** (heading +
`verified-at: 2026-11-03` + `recheck:` inside the block), append-only holds byte-for-byte, and
every `recheck:` command re-runs byte-identical to its recorded stdout (rc 0 all 14).
`SUMMARY entries=14 addendum_rule_all=True append_only_all=True rerun_stable_all=True
repaired=14 unrepaired=0`.

## Files in this seat dir

- `<entry-basename>.addendum.txt` ×14 — the block for the L1 to append byte-exact.
- `<entry-basename>.reverify.txt` ×14 — verbatim `$ command`, stdout, `[exit=…]`, plus the
  clone HEAD and the entry's pre-append sha256 (integrity check for the append).
- `selfcheck.txt` — append-only / classifier / re-run-stability receipt above.
- `driver-gen_addenda.py`, `driver-selfcheck.py` — the two drivers that produced the receipts
  (reproducibility aids, not evidence).

Frozen-list cross-check: the 14 blocks cover exactly lines 16–29 of the frozen file, in order;
slice A (lines 1–15) is SweepRepairA's.

## Risks / limitations (named, not hidden)

1. **Shared capture digest for five entries.** Entries 16, 18, 19, 20, 29 cite the same
   historical source root (`~/Projects/webzites/repos/llm-wiki`), and the committed round-13
   availability receipt records only that root (`exists:false`). Their committed-bytes leg is
   therefore identical across the five; per-entry specificity comes from the live `test -e` of
   each entry's exact cited subpath (run this round, all absent).
2. **Host-state leg.** The `test -e` legs re-check today's filesystem, not committed bytes; if the
   closure runs on a host where those roots exist, the addendum's `result:` would not match while
   the committed receipt digest still would. The digest+grep legs are the deterministic core.
3. **Entry 21 reads the fleet repo read-only** (`git log -1 <merge>`); no mutation. Its lane-committed
   leg (round18 evidence README sha256) re-derives without the fleet repo.
4. **Entry 28's tool prints `PREDICATE R52-C1 fail` by design** (the entry's own "not admitted"
   verdict); the recheck re-derives that failure plus the A5 pass, not a pass. Exit is 0 because
   the final pipeline stage is the `sha256sum -c` diagnostic.
5. **No addendum is green-by-prose**: every `result:` token was asserted present in the executed
   stdout before the block was written, and every command was re-run for stability.

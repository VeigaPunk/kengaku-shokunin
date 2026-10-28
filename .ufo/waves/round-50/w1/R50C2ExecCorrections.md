# R50C2ExecCorrections — C2 corrections block (executor, calibration)

Seat: `R50C2ExecCorrections` · wave `.ufo/waves/round-50/w1` · serving **R50-C2** (calibration 8→9).
Axes named: **calibration** (the C2 pointer audit and its append-only correction surface). No other axis is
touched: this seat wrote no production file, no counter, no corpus row.

```
REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1   (lane master at measurement; freeze below is an ancestor)
FREEZE 3b02d573d58cc6d2e0d27ef92ac0815354912252 2026-10-28 14:18:09 -0300
$ git merge-base --is-ancestor 3b02d57… HEAD && echo FREEZE-IS-ANCESTOR
FREEZE-IS-ANCESTOR
```

## 1. What the assignment asked, and what the lane already holds

The item asked for an append-only `## Round 50 — C2 corrections` block: one `SUPERSEDED <pointer> -> <target|
never-landed>` row per unresolved pointer, in the order the audit prints them, each with a one-line reason and
the evidence command, emitted to `.ufo/waves/round-50/w1/C2ExecCorrections/block.md` for verbatim paste.

Measured state at `c3372a9b`: **that block is already in `SCORECARD.md`** (lines 2136-2156, landed in `822f3b7`,
"round-50: C2 corrections (12 pointers resolved append-only)"), and the audit is green. So the deliverable is
not a fresh block: re-pasting the landed rows would duplicate every `SUPERSEDED` row. `block.md` therefore ships
two clearly separated sections and an HTML paste-status header:

- **§1 "append this (delta only)"** — `### Round 50 — C2 corrections — row evidence`: the 12 row-level
  one-line reasons + evidence commands that the landed block carries only as one shared prose paragraph
  (and whose landed prose does not attach an evidence command per row). This is the text the L1 appends.
- **§2 "reference only, do not re-paste"** — the landed heading + 12 `SUPERSEDED` rows verbatim, so the rows
  can be diffed against what is in `SCORECARD.md`.

Both facts were measured, not assumed (see §3, rows D and E): appending §1 leaves the audit green and changes no
count; re-pasting §2 leaves it green but produces 24 `SUPERSEDED` rows.

## 2. The 12 rows, in the order the audit prints them (and the row-level verification)

Order source: the audit iterates `sorted(paths)` and prints `UNRESOLVED <path>`; the pre-correction tree prints
exactly the 12 rows in the same order as the landed block (command A' below). Each row's licence, re-run at
`c3372a9b`:

| # | pointer | row | licence (re-run) |
|---|---|---|---|
| 1 | `corpus/defects.json` | -> `corpus/defects.jsonl` | target EXISTS; `git log --all --oneline -- corpus/defects.json` → 0 rows |
| 2 | `corpus/evidence/analyze.py` | -> never-landed | `git log --all --oneline -- …` → 0 rows; SCORECARD:113 records `test -e` → absent |
| 3 | `corpus/evidence/round9-replication/predictions-r9.sh` | -> `…/predictions-r9.md` | target EXISTS; history 0 rows |
| 4 | `corpus/knowledge/repo-git-state.md` | -> never-landed | history 0 rows; PROVINCE:416 cites Kasegi's entry |
| 5 | `corpus/routed-findings.json` | -> `corpus/routed-findings.jsonl` | target EXISTS (71 rows); history 0 rows |
| 6 | `plans/round34_c1_verify.py` | -> never-landed | history 0 rows; promised at SCORECARD:1168 |
| 7 | `plans/round34_defects.py` | -> never-landed | history 0 rows; promised at SCORECARD:1169 |
| 8 | `plans/round34_mutate.py` | -> never-landed | history 0 rows; promised at SCORECARD:1169 |
| 9 | `plans/round48_c1_verify.py` | -> never-landed | history 0 rows; "Frozen command" at SCORECARD:2104 |
| 10 | `plans/round48_c2_verify.py` | -> never-landed | history 0 rows; SCORECARD:2105 |
| 11 | `plans/round49_c1_verify.py` | -> never-landed | history 0 rows; SCORECARD:2119 says "is not present at landing" |
| 12 | `plans/round49_c2_verify.py` | -> never-landed | history 0 rows; SCORECARD:2120, same wording |

Every row is *consumed* by the audit, so no row is dead: `exists=206`, `superseded=3`, `never-landed=9`, and
`206+3+9 = 218 = paths`. Kill-rule conditions checked: no row's target is missing (3/3 exist), and no
`never-landed` row names a path in history (9/9 empty).

Mechanism worth recording for the lesson file: rows 1 and 5 exist because the audit's extension alternation
(`md|py|json|jsonl|…`) is non-greedy and ordered, so every `corpus/defects.jsonl` / `corpus/routed-findings.jsonl`
mention tokenises as `corpus/defects.json` / `corpus/routed-findings.json`. Measured directly:

```
# the audit's own TOKEN regex, re-run in a throwaway python heredoc (no file written)
corpus/defects.json -> ['corpus/defects.json']
corpus/routed-findings.json -> ['corpus/routed-findings.json']
jsonl tokens: ['corpus/defects.json', 'corpus/routed-findings.json']
```

## 3. Exact commands and observed output (verbatim)

All runs use a `git clone --shared` of the lane in my scratch, plus revision images built with
`git archive <rev> | tar -x` and a `gitdir:` pointer file so the frozen audit script sees that revision's tree
while `git log --all`/`cat-file` read the clone's objects. The live checkout was never the target of a run.

**A — tip (the claim's predicate):**
```
$ cd $S/lane && python3 plans/round50_c2_audit.py --lane .
TIP c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 branch=master
POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3 never-landed=9 unresolved=0
EXIT=0
```

**A' — pre-correction tree (`5c56819`, parent of the landing commit), corrections absent:**
```
TIP c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 branch=master
POINTERS total=275 paths=216 hashes=59 resolved=263 exists=204 superseded=0 never-landed=0 unresolved=12
UNRESOLVED corpus/defects.json
UNRESOLVED corpus/evidence/analyze.py
UNRESOLVED corpus/evidence/round9-replication/predictions-r9.sh
UNRESOLVED corpus/knowledge/repo-git-state.md
UNRESOLVED corpus/routed-findings.json
UNRESOLVED plans/round34_c1_verify.py
UNRESOLVED plans/round34_defects.py
UNRESOLVED plans/round34_mutate.py
UNRESOLVED plans/round48_c1_verify.py
UNRESOLVED plans/round48_c2_verify.py
UNRESOLVED plans/round49_c1_verify.py
UNRESOLVED plans/round49_c2_verify.py
EXIT=1
```
This is the exact sequence §1 follows, and it is the same first twelve `UNRESOLVED` lines as the frozen receipt
`.ufo/waves/round-50/claims/c2-before.txt` (S1 tree `f7281bc`, `total=275 … unresolved=12`, exit 1).

**B — claims' before, reproduced at the base lane tip `71f5f5f` (tip script run against a `71f5f5f` image):**
```
POINTERS total=271 paths=213 hashes=58 resolved=259 exists=201 superseded=0 never-landed=0 unresolved=12
EXIT=1
```
Same 12 rows, same order. (`plans/round50_c2_audit.py` does not exist at `71f5f5f` — it landed at the stage-1
freeze — so the before figure can only be reproduced by pointing the frozen script at the base tree; the frozen
receipt was produced inside the S1 tree and reads `total=275`.)

**C — selftest at tip (does the check go red on a bogus pointer):**
```
$ python3 plans/round50_c2_audit.py --lane . --selftest
… POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3 never-landed=9 unresolved=0
… UNRESOLVED plans/round50_selftest_bogus.py
SELFTEST pristine_rc=0 bogus_rc=1 new_unresolved=['plans/round50_selftest_bogus.py'] verdict=ok
EXIT=0
```

**D — §1 appended to a `c3372a9b` image (the paste the L1 will make):**
```
APPENDED lines: 18
POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3 never-landed=9 unresolved=0
EXIT=0
```
No count moves, so §1 introduces no pointer that does not already resolve.

**E — §2 re-pasted (the mistake §2's label prevents):**
```
SUPERSEDED rows now: 24
POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3 never-landed=9 unresolved=0
EXIT=0
```
Green but duplicated — hence §2 is reference-only.

**F — row licence re-run (12/12 history-empty, 4/4 targets present):**
```
corpus/defects.json                                   log_rows=0
corpus/evidence/analyze.py                            log_rows=0
corpus/evidence/round9-replication/predictions-r9.sh  log_rows=0
corpus/knowledge/repo-git-state.md                    log_rows=0
corpus/routed-findings.json                           log_rows=0
plans/round34_c1_verify.py                            log_rows=0
plans/round34_defects.py                              log_rows=0
plans/round34_mutate.py                               log_rows=0
plans/round48_c1_verify.py                            log_rows=0
plans/round48_c2_verify.py                            log_rows=0
plans/round49_c1_verify.py                            log_rows=0
plans/round49_c2_verify.py                            log_rows=0
corpus/defects.jsonl                                  EXISTS
corpus/evidence/round9-replication/predictions-r9.md  EXISTS
corpus/routed-findings.jsonl                          EXISTS
corpus/evidence/round9-fleet/analyze.py               EXISTS
```

## 4. Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-50/w1/C2ExecCorrections/block.md`
(5906 bytes): paste-status HTML comment, §1 delta (heading + 12 evidence lines), §2 landed rows for diff.

## 5. Limits

- The audit measures pointer *resolution*, not pointer *truth*: a `SUPERSEDED … -> <target>` row is licensed by
  the target's existence, so a semantically wrong but existing target would pass. I checked the four targets by
  content (`corpus/defects.jsonl` = the 5-row round-35 defect ledger with `R34-D*` ids; `predictions-r9.md` =
  the file `predictions-r9.sha256.repo` hashes; `routed-findings.jsonl` = the 71-row routed ledger), which is
  judgement, not a counter.
- Line numbers cited in §1 (`SCORECARD:563…2120`, `PROVINCE:416`) are as of `c3372a9b`; they drift as
  `SCORECARD.md` grows by appending. The landed prose at SCORECARD:2163 says `PROVINCE:415` — that is where the
  citing sentence opens; the pointer string itself is on 416. Not a defect, recorded so a later reader is not
  confused.
- The landed prose at SCORECARD:2162 names `corpus/evidence/round9-fleet/probeA.py` as `analyze.py`'s
  replacement; SCORECARD:113 itself names `corpus/evidence/round9-fleet/analyze.py`. Both files exist, so the
  audit is unaffected; §1 states the SCORECARD:113 successor because that is the row being explained.
- `plans/round-50-claims.md` §C2 prose says "of which six pointers name counters … (`plans/round48_c1_verify.py`,
  `plans/round48_c2_verify.py`, `plans/round49_c1_verify.py`, `plans/round49_c2_verify.py`,
  `plans/round34_c1_verify.py`, `plans/round34_defects.py`, `plans/round34_mutate.py`, and four corpus paths)".
  The measured split is **seven** `plans/` counters and **five** corpus paths (the corpus five include
  `corpus/evidence/analyze.py` and `corpus/knowledge/repo-git-state.md`, which are not ledgers); 7+5=12 is what
  the counter prints. The prose's "six"/"four" is loose; the counter is authoritative. Flagged for the round
  lesson — the claims file is frozen and this seat did not edit it.
- I did not measure `plans/round46_c1_verify.py` or C1's legs; not this seat's item.
- Scratch `/fast/scratch/hyaku/kengaku-r50/R50C2ExecCorrections` was created for this run and is removed before
  yield; no `/tmp` path is cited here.

## 6. Addendum — re-measured at the later tip `d45c5bb` (after the C1 landing)

While this seat was closing, the lane advanced three commits (`6db0279` S3 fence repair, `d6f2fce` mutant
battery, `d45c5bb` scored C1 receipt). C2's predicate is stated at the *landing* tip, so the audit was re-run on
a fresh `git clone --shared` of that tip (clone worktree clean, `git status --porcelain` empty):

```
$ git rev-parse HEAD
d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
$ python3 plans/round50_c2_audit.py --lane .
TIP d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78 branch=master
POINTERS total=279 paths=219 hashes=60 resolved=279 exists=207 superseded=3 never-landed=9 unresolved=0
EXIT=0
$ python3 plans/round50_c2_audit.py --lane . --selftest
… POINTERS total=280 paths=220 hashes=60 resolved=279 … unresolved=1
… UNRESOLVED plans/round50_selftest_bogus.py
SELFTEST pristine_rc=0 bogus_rc=1 new_unresolved=['plans/round50_selftest_bogus.py'] verdict=ok
$ grep -c '^SUPERSEDED ' SCORECARD.md   → 12      ($ grep -n '^## Round 50 — C2 corrections' → 2136)
```

Still green, and the correction block is intact and still the only one (`SCORECARD.md:2136`, 12 rows). The C1
landing added exactly two tokens to the audited surface — both new, both resolving by existence / ancestor:

```
added at d45c5bb: ['corpus/evidence/round50/c1-receipt.txt', 'd6f2fce9889f429162c12f851bae41891bedf5cd']
removed at d45c5bb: []
```

(`d6f2fce…` is a 40-hex hash, so it resolves through `git cat-file -e` + `merge-base --is-ancestor`, not through
path existence.) No further correction row is needed at `d45c5bb`, and `plans/fixture_fence.py` /
`plans/round50_c1_verify.py` edits cannot move this surface unless a later landing adds a new `plans/`/`corpus/`
artifact mention to `SCORECARD.md`, `SHONEN.md` or `PROVINCE.md`.

## 7. Verdict

**VERDICT:** R50-C2 correction surface is complete and green at `REV c3372a9b` —
`POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3 never-landed=9 unresolved=0`, exit 0 —
and still green at the later tip `REV d45c5bb` — `POINTERS total=279 paths=219 hashes=60 resolved=279 exists=207
superseded=3 never-landed=9 unresolved=0`, exit 0;
all 12 `SUPERSEDED` rows are consumed, ordered exactly as the audit prints them, 3/3 targets exist, 9/9
`never-landed` rows have empty history. No new rows are required at either revision; the only text still worth
appending is the row-level evidence delta in `block.md` §1, measured not to change any count. This seat admits
nothing: R50-C2 admission is the L1's call on the landing tip.

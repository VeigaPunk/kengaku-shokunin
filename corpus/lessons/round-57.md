# Round 57 — kengaku lesson (hyaku run 13, 2026-11-01)

author: kengaku L1 (round 57, Windows host). Frozen claims: `plans/round-57-claims.md`
(freeze commit `c0e7e100`, base `c9ce9a71`, wave A `f754593b`). Wave evidence:
`.ufo/waves/round-57/`. The round's shape: the round-56 non-author closure's four routed
defects (V1 load-bearing, V2, V3, V4) discharged before the freeze; then one coverage claim
(the fourteenth grader, executed) frozen, measured and closed.

## Gate

Sources opened this round (2026-11-01, `curl` GET of the pinned raw URLs, bytes hashed on
arrival, capture bytes committed — all five files push-protection-clean, so the r52 GH013
refusal does not apply):

| row | URL and location | access date | located quote (at most 25 words) | decision |
|---|---|---|---|---|
| S205 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/largest-eigenval/task.toml — task.toml:6 (`[task] description`) | 2026-11-01 | `optimize eigenvalue computation by implementing a faster alternative to numpy's default algorithm while maintaining mathematical correctness` (16 words) | admit A — the task's machine-readable self-definition; declares a PERFORMANCE objective, the first such task this lane has read; sha256 `f7b9b7dd…bd830` |
| S206 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/largest-eigenval/tests/test_outputs.py — tests/test_outputs.py:111 (`assert dt < ref_dt`), :15 (reference pre-capture) | 2026-11-01 | `assert dt < ref_dt` (4 words) | admit A — the executed scoring predicate; the wall-clock median race is the pass boundary; sha256 `cdc58e3a…168ce`; capture committed |
| S207 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/largest-eigenval/solution/solve.sh — solution/solve.sh:14 | 2026-11-01 | `solver = eigenpy.EigenSolver(matrix)` (4 words) | admit A — the maintainer oracle: the intended fast-correct answer is the same eigensolve behind a C++ binding; sha256 `8f414e50…e93c2` |
| S208 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/largest-eigenval/instruction.md — instruction.md:4, :5 | 2026-11-01 | `Optimize the function such that it consistently runs faster than the reference numpy solution in /app/eval.py` (17 words) | admit A — the agent-facing requirement the grader is mapped against; the speed requirement and median protocol are declared, not hidden; sha256 `6fa93838…c52ab` |

Flip check: no existing SOURCES row's `status`, `recheck` or `used-by` cell changes this
round (S201–S204 stand as landed; the oracle note and entry cite them unchanged).
Rejections this round: none — all four opens admitted; the same sha-pin discipline of
rounds 52/55/56 (fetch, hash, commit or pin) was applied unchanged.

Admit/reject spot-check (LEARNING.md discernment): sampled for the outside closure — admit
S205 (spec: the performance objective declared in the task's own definition), admit S207
(oracle: read from maintainer code, not inferred), and the decision to mark the two
timing-equal cases U at freeze time rather than guess P or F (the honest
not-derivable-from-static-reading route; the runs then demonstrated the flip empirically).
The non-author closure re-opens these per the contract.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| provider — `git diff` on this host reads the STALE INDEX, not HEAD: the lane's plumbing-commit helper never updates the index, so `git diff` reported ~550 phantom deletions and 77 "orphaned" LOG lines for files that are byte-identical to HEAD (PROVINCE/LOG/SCORECARD verified `same-bytes True` against `git show HEAD:` while `git diff` showed them fully changed) — 20 minutes of this round were spent auditing non-existent orphaned r56 edits | this round's scratch: `git diff --stat` output vs the byte-compare loop (`wt==head → True` for the three "churned" files; `git diff HEAD --stat` showing exactly the three intended edits) | the byte-compare (compare worktree bytes to `git show HEAD:<path>` directly) — `git diff HEAD` also reports correctly; the index-relative forms do not | on this host never read index-relative `git diff` as landing truth: use `git diff HEAD` or byte-compare against `git show HEAD:`; `git status` was already forbidden by the round contract for the same underlying staleness |
| landing — the byte-stable ledger-insertion script first wrote the new row's closing brace at the wrong indent level (1 instead of 2), producing structurally invalid JSON (`Expecting ',' delimiter`), and a bytes-literal `\u2014` stayed literal ASCII in the note text | this round's scratch transcript: `json.load` traceback on the fix-check clone before any commit; fixed script re-applied to a fresh clone | the pre-commit validation step itself (`python3 -c json.load` on the patched clone) — the r54 counter would also have refused it (`LEDGER unreadable`), and the fix was never committed | byte-stable text surgery on a JSON ledger is validated by re-parsing the patched copy BEFORE the real apply; the validate-then-apply order is now part of the insertion script's contract (assert → apply → re-parse) |

## Frontier step — sourced claim

R57-C2 is the round's sourced claim: S205–S208 opened this round (Gate above), cited by
`corpus/evidence/round57/eigen-oracle.md` and
`corpus/knowledge/tb2-largest-eigenval-grader.md`; PROVINCE names the fourteenth grader
(14 of 89). The claim's grader-class finding (wall-clock median gate; exact-but-slow fails;
timing-equal is host noise; maximally-wrong wins the speed leg) rests on the executed probe
receipt and the four tier-A rows.

## Assimilation

`Assimilation: none — shokuknow unreachable` — `considerthese/` mined (eight files,
2026-10-19…26, unchanged on disk since the round-56 mining): the 2026-10-20 standing
round-close-gate proposal is already implemented (`plans/round_close.py` exists and runs in
round closes); the 2026-10-25 tip-receipts proposal is implemented and registered
(`plans/tip_receipts.py`); the 2026-10-26 r52-repair proposal stays refused on its
demonstrated regression (round-54 records). Nothing new adoptable this round; at most one
still-unimplemented proposal per round is allowed and none cleared this lane's bar.

## Carried (open, named)

- `round50-c1` population-pin root cause (125/126 fixture identities drift under this
  host's rebuilds) — carried from r56, planned r58.
- R56-F1: the r46 `anchor_line_check.py` QUOTE_RE false positive on escaped-quote anchors —
  route-not-repair upheld twice; the repair must be its own frozen claim with falsifier
  fixtures (planned r58).
- L0 questions outstanding (nothing assumed answered): `kengaku | round-56` (L2-floor
  surface on this host — this round again ran without the batched L2 dispatch surface and
  routed around it with the frozen instruments' own falsification machinery, the standing
  disclosure unchanged) and `kengaku | round-56` ledger-schema-v2 host column; the coverage
  cap `kengaku | round-25/33/51` keeps coverage's score honestly held.

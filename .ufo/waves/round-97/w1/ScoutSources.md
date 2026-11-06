# ScoutSources — round 97: S317–S325 reopened at T

Seat `ScoutSources`, lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, round 97.
Measured tip **T = `f1083da60e7ff6b88f7420aae7424f7762d14700`**. No production edit, no commit,
no mutating git/jj in the lane; the only clone is a `--shared` detached copy at BASE in scratch
(`/fast/scratch/hyaku/kengaku-r97/ScoutSources/lane-base`, `git rev-parse --show-toplevel`
verified before any command). Receipts: `.ufo/waves/round-97/w1/ScoutSources/`.

Tools (recorded per rules): `uv 0.13.0` (pre-installed, not upgraded) created scratch venv `G`;
`rdflib==7.1.4` and `pytest==8.4.1` installed with `uv pip --python G/bin/python` (channel: uv,
reason: independent semantic check of the graph claims with the grader's own pins). No pacman
transaction, no sysctl/service change.

Method: parse the nine rows from `corpus/SOURCES.md` at T, fetch each row's URL, hash the bytes,
locate the quoted span at the cited line of the cited file as a byte substring, count its words,
then compare against the captured bytes, the frozen-instruments table, the candidate bytes, and
the row's own decision/flip. Scripts and raw output are in the receipt dir (`verify_sources.py`,
`verify.log`, `verify.json`, `live/`, `semantics.py`, `semantics.log`, `semantics.json`).

## 1. Reopen result — 9 of 9 rows pass

All nine URLs are `raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/sparql-university/…`
(pinned commit; content-addressed, so a re-fetch is the same object).

| id | file:line | HTTP | bytes claimed/observed | sha256 claimed = observed | quote at cited line (byte substring) | words claimed/actual | decision |
|---|---|---|---|---|---|---|---|
| S317 | tests/test_outputs.py:79 | 200 | 2399 / 2399 | `ecf15840…7b39` = `ecf15840…7b39` | yes | 5 / 5 | mined (A) |
| S318 | tests/university_graph_test.ttl:157 | 200 | 10680 / 10680 | `368ce01d…92cb` = `368ce01d…92cb` | yes | 6 / 6 | mined (A) |
| S319 | solution/solve.sh:46 | 200 | 1600 / 1600 | `d17995a8…a791` = `d17995a8…a791` | yes | 4 / 4 | mined (A) |
| S320 | tests/test.sh:21 | 200 | 629 / 629 | `45902b57…cc6b` = `45902b57…cc6b` | yes | 3 / 3 | mined (A) |
| S321 | instruction.md:7 | 200 | 1268 / 1268 | `22eeab47…f449` = `22eeab47…f449` | yes | 24 / 24 | mined (A) |
| S322 | environment/university_graph.ttl:113 | 200 | 10481 / 10481 | `0b0b1f2c…9a85` = `0b0b1f2c…9a85` | yes | 4 / 4 | mined (A) |
| S323 | environment/Dockerfile:7 | 200 | 235 / 235 | `dd0abcd6…16a9` = `dd0abcd6…16a9` | yes | 3 / 3 | rejected (A, flip) |
| S324 | task.toml:29 | 200 | 1007 / 1007 | `47a6f6dd…9585` = `47a6f6dd…9585` | yes | 3 / 3 | rejected (A, flip) |
| S325 | README.md:24 | 200 | 1697 / 1697 | `947086de…8d05` = `947086de…8d05` | yes | 17 / 17 | rejected (B, flip) |

Observed: 9/9 HTTP 200, 9/9 exact byte count, 9/9 exact sha256, 9/9 quote present at the exact
cited line as a byte substring (not merely somewhere in the file: each quote occurs exactly once
in its file), 9/9 claimed word count equals the actual count, 9/9 ≤ 25 words (max 24, S321).
The rows' `opened 2026-11-06` / `recheck on-release` cells are consistent with the fetch date and
the pinned-commit URL. Table also at `ScoutSources/sources-table.md`.

## 2. Captured bytes, candidate bytes, registry delta

- **Live == captured, byte for byte.** Each fetched body `cmp`-equals
  `corpus/evidence/round97/graders/sparql-university/<file>` (not just hash-equal). So the row's
  sha is a claim about bytes the lane actually holds, and the held bytes are the upstream bytes.
- **Frozen-instruments table**: the six grader files it lists (`test_outputs.py`, `test.sh`,
  `university_graph_test.ttl`, `solve.sh`, `environment/Dockerfile`,
  `environment/university_graph.ttl`) hash to the table's values at T; the other three
  (`instruction.md`, `task.toml`, `README.md`) are captured and hash to their row values.
- **Candidate bytes**: `corpus/SOURCES.md` at T sha256 `c54a0ece…0ce04`, identical to
  `.ufo/waves/round-97/L1/controls/candidate/corpus/SOURCES.md` — the landed file is the frozen
  candidate, not a post-F edit.
- **Registry delta BASE→T**: `git diff 4992cd0e f1083da6 -- corpus/SOURCES.md` = **9 insertions,
  0 deletions, 0 modifications**; BASE has 308 rows and no `S317…S325` row, T has 317 rows ending
  at S325. No old row's text, decision, tier or anchor changed.
- No duplicate URL among S317–S325 (nine distinct files of one task). The registry does contain
  duplicate URLs from older rounds (e.g. `chess-best-move/tests/test_outputs.py`,
  `configure-git-webserver/*`, `nginx-request-logging/*`); that is pre-existing, not round-97.

## 3. Decisions and flips

- **Admitted S317–S322** are the bytes or documents the replay actually needs: both instruments
  (`plans/round97_sparql_probe.py`, `plans/round97_c1_replay.py`) pin six files, and S321
  (`instruction.md`) is the only admitted row not in the pin set — it is cited for the
  contract-vs-graded gap, which is what its `scope` cell says ("what the agent is told the query
  must satisfy"), and the row is marked "member replay only". Consistent.
- **Rejected S323–S325** each carry a `flip:` clause and each flip is a checkable condition:
  S323 "a case whose verdict depends on an agent-side tool"; S324 "the image pulled and its /app
  and verifier versions compared to GRADER_SIDE"; S325 "a claim about the README's own
  statements". Tier A/A/B respectively; the README stays tier B, which the SOURCES contract allows
  for a derivative summary.
- **One wording tension (S323)**: the row says "REJECTED as a replay input … the replay stages the
  same /app bytes and never runs agent-side code beyond solve.sh's heredoc", yet
  `environment/Dockerfile` **is** in both instruments' `PINS` tables (L2 integrity). The decision
  is coherent — the Dockerfile is not an input to any case verdict — but "rejected as an input"
  can be read as "not read". Note only; no change made.

## 4. Independent check of the admitted rows' `teaches` cells

The grader's own test logic was run over the fetched bytes: a scratch copy of
`tests/test_outputs.py` with only the two absolute paths repointed (`/app/solution.sparql`,
`/tests/university_graph_test.ttl`), pytest 8.4.1 + rdflib 7.1.4, the reference query extracted
from the fetched `solve.sh`, and seven declared variants.

| variant | result | what it confirms |
|---|---|---|
| reference (solve.sh query) | 3 passed | S319 C01: the author's query satisfies all three test functions |
| C05 EU filter removed | 3 passed | S318: every professor the EU criterion would exclude is excluded by the >10 rule |
| C06 `NOW()` for both date literals | 3 passed | S318/S321: a NOW()-dated query passes |
| C09 per-department `HAVING` | 3 passed | S318/S319: per-department and aggregate counting are indistinguishable |
| C10 literal `VALUES` answer | 3 passed | S317/S321: a hardcoded answer with no graph pattern passes |
| C11 duplicate rows (reference UNION itself) | 3 passed, 8 rows / 4 distinct | S317: set comparison discards duplicates |
| C12 extra projected column (`?n`) | 3 passed | S317: an extra column is ignored |
| C17 agent-graph literal | 1 failed, 2 passed | S322: the agent-graph answer fails on the test graph |

Graph facts behind the cells (rdflib over the fetched test graph): reference set = 4 professors;
aggregate counts 12 / 12 / 12 / 11 for those four and 7 (John Smith, US) / 6 (Marie Dubois, FR),
so dropping the EU filter changes nothing; per-department counts are 12 / 12 / 12 / 11, i.e. the
same four, so C09 cannot separate the readings; graduation dates run 2025-06-02 → 2026-06-12,
enrollment dates 2024-01-10 → 2024-01-21, and 16 students carry no graduation date.

**Finding F2 (routed, no repair).** S318's C06 sentence — "graduations end 2026-06-12, so a
NOW()-dated query passes" — was true when written but is now time-stale: at T (2026-11-06) all ten
graduation dates are in the past, so a NOW()-dated query passes because 16 students have **no**
graduation date, not because graduations are still in the future. The conclusion still holds at T
(counts 12/12/11/11 under today's date); the stated mechanism does not. A future round that
changes the no-graduation population could flip C06 without any byte changing.

## 5. `considerthese` latest proposal (2026-11-05) — unimplemented, still relevant

`considerthese/2026-11-05.md` (landed `70eb8cac`, "proposals only, nothing acted on"). All five
proposals are unimplemented at T; none was changed. Evidence per proposal in
`ScoutSources/considerthese-status.md`; summary:

1. Calibration cap conditional on routed-finding age — **unimplemented**: r96 and r97 both say
   "held at ceiling 10"; no cap is emitted by any `plans/round9*` gate (the burndown scripts
   compute `oldest_pending` and print no cap).
2. Root-of-trust manifest / outside verifier — **unimplemented**: no `.github/`, no trust-root
   manifest in `git ls-files`; the trust root is still in-lane pin ledgers.
3. `SKILL.md` byte budget + generated `STATUS` — **unimplemented**: `SKILL.md` is 364,893 B at T
   (356 KB when proposed), no `STATUS.md`, no size check in `plans/*.py`.
4. One round in five on an outward question; separate instrument/domain counts — **unimplemented**:
   no such counts anywhere; round 97 is instrument-only.
5. Operator ruling on the coverage L0 cap — **unimplemented and still live**: `SCORECARD.md:670`
   "coverage is capped at 7 … pending the operator's coverage-cap ruling"; `plans/round-97-claims.md`
   "held at its L0 cap 7"; no ruling in `LOG.md`; the cap has stood since round 25.

## 6. Lane gates that bear on these rows

- `plans/anchor_line_check.py --lane .` at T: **rc 0**, `ANCHORLINE rows=317 cited=125 captured=112
  uncaptured=13 defective=10 repaired=10 live=0 cells=0`. None of S317–S325 appears in the 13
  `UNCAPTURED` rows (they are all old: S093…S266), so the lane's own line gate does resolve the
  round-97 captures and finds every new quote on its cited line.
- `plans/anchor_digest_check.py --lane .` at T: **rc 1**, `rows=317 tokens=201 defects=86`; at BASE
  (clone at `4992cd0e`): **rc 1**, `rows=308 tokens=192 defects=80`. Six of the nine new rows
  (S317, S318, S319, S320, S322, S323) are `class=anchor-unbound
  detail=no-capture-for-upstream-…`; S321, S324 and S325 bind (`bind=url-task` via
  `corpus/evidence/round97/graders/sparql-university/<file>`). Cause (read from the resolution
  code, `anchor_digest_check.py` ~l.330-370): the url-task rule binds `<owner-dir>/<basename>`,
  while the round-97 capture preserves the upstream subdirectories `tests/`, `solution/`,
  `environment/`. Round 96's `multi-source-data-merger` rows S310–S313 show the same class, so the
  red is pre-existing (80 at BASE) and round 97 adds 6 of the same kind (86).
  Neither R97 claim's predicate includes this gate, and C1's own L2 pins the six captures
  directly (verified against live bytes in §1–2), so no claim is false — but the digest gate
  cannot certify 6 of the 9 new rows.

## 7. Verdict

- **S317–S325 reopen: PASS (9/9).** HTTP 200, exact size, exact sha256, quote located at the cited
  line as a byte substring, ≤25 words, claimed word counts exact. Captured bytes equal live bytes;
  the landed `SOURCES.md` is the frozen candidate (`c54a0ece`); BASE→T is +9 rows and nothing else.
- **Decisions and flips: consistent with the bytes.** S317–S322 admitted tier A on files the
  replay reads or the case table cites; S323–S325 rejected with checkable flips. No duplicate URL
  inside the new block.
- **R97-C1 source side: not contradicted.** The probe receipt has 18 `CASE` lines × 4 legs, 18
  `ok=True`, `mismatches 0`, and every `teaches` claim I could test independently reproduced
  (C05, C06, C09, C10, C11, C12 pass; C17 fails; C01 passes).
- **R97-C2 source side: not contradicted.** The registry row `anchor-digest-check` is typed
  `probe` at T, and the script has no `--selftest` (only `--lane`, `--evidence-ref`, `--verbose`),
  so its demotion is corroborated by the bytes.
- **No kill.** Nothing observed falsifies a frozen predicate; the four findings below are routed,
  not repaired.

Routed findings (round 98):
- **F1** `anchor_digest_check.py` is red at T (86 defects) and was red at BASE (80); 6 of 9 new
  rows unbound because the capture preserves upstream subdirectories while the url-task rule binds
  `<owner>/<basename>`. Either flatten the capture or teach the gate nested paths.
- **F2** S318's C06 mechanism sentence is time-stale (graduations all past at T; the pass now rests
  on 16 no-graduation students). Conclusion holds; re-word or re-verify.
- **F3** S323 says "rejected as a replay input" while its bytes are pinned by both instruments;
  wording only.
- **F4** Pre-existing duplicate URLs in the registry (older rounds) — noted, not round-97.

Confidence: **observed** for every HTTP status, byte count, sha256, quote location, word count,
gate exit code and variant result above; **inference** for the digest-gate cause (read from the
resolution code, not mutated) and for the reading of S321 as "cited, not read" (from its absence
in both `PINS` tables).

Remaining unknowns: whether the lane intends `anchor_digest_check` to bind nested capture layouts
(no doc states it); whether the coverage-cap ruling is pending by design; the probe fakes no clock
(no faketime/date shim in `plans/round97_sparql_probe.py`; `NOW()` is the host date), and I did not
re-run the frozen probe — my NOW() check used a scratch copy of the test file with repointed paths.

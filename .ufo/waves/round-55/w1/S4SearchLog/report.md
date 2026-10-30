# S4SearchLog — report (kengaku round 55, wave 1)

Seat: document the 13th-grader selection as a PRISMA-style bounded search; target
`.ufo/waves/round-55/w1/S4SearchLog/search-log.md` (L1 splices it into `corpus/SOURCES.md`
`## Search log`). Leaf member; no subagents; no installs; no scratch clone needed — every
check was a read-only command against the live lane at
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, so no scratch dir was created under
`/fast/scratch/hyaku/kengaku-r55/S4SearchLog/` and none needed cleanup.

## What I ran (commands → observed results, all exit 0)

1. Frozen-claims check: `git -C . show 80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb:plans/round-55-claims.md`
   vs `sha256sum plans/round-55-claims.md` → identical `7f371289…bf88d`; working tree matches
   the freeze, predicates/counters read from the frozen text.
2. Pool size: `find corpus/evidence/round52/graders -mindepth 1 -maxdepth 1 -type d | wc -l`
   → **89** (identified count grounded).
3. Screening line counts: `wc -l` on `corpus/evidence/round52/graders/<task>/tests/test_outputs.py`
   → chess-best-move **25**, cancel-async-tasks **172**, dna-insert **102**, count-dataset-tokens
   **13**, extract-elf **392**; `sanitize-git-repo/tests/test_outputs.py` → MISSING (only dir of
   the 89 without the file).
4. Exclusion grounds: `grep -n oligotm` dna-insert → `tests/test_outputs.py:17,20,92,93` (external
   binary call); `grep "import|sleep|timeout|asyncio"` cancel-async-tasks → `signal`, `subprocess`,
   `time`, `time.sleep(0.5)` ×3, subprocess `timeout=3` comment / `timeout=5` / `timeout=10`;
   read count-dataset-tokens grader bytes → hardcoded `expected_output = "79586"` membership check;
   read chess-best-move grader bytes → sole import `pathlib.Path`, absolute `/app/move.txt` read,
   `assert sorted(move) == sorted(["g2g4", "e2e4"])`.
5. Byte identity: `sha256sum …/chess-best-move/tests/test_outputs.py` →
   `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` — equals the sha256 frozen
   in R55-C3.
6. GH013 exclusion: read `corpus/evidence/round52/graders/EXCLUDED.md` — withheld file sha256
   `57e49041…b59e`, operator decision 2026-10-28; also `corpus/lessons/round-52.md:10,62,65`.
7. Already-read 12: glob `corpus/knowledge/tb2-*.md` → exactly 12 task entries
   (protein-assembly, regex-log, git-webserver, build-pmars, git-leak-recovery, db-wal-recovery,
   constraints-scheduling, circuit-fibsqrt, feal-differential-cryptanalysis, feal-linear-cryptanalysis,
   password-recovery, polyglot-c-py) plus 2 cross-task triage notes not counted;
   `corpus/README.md` Coverage map bullets round 35 (first, protein-assembly) … round 46 (twelfth,
   polyglot-c-py, "12 of the 89 TB2 task graders").
8. Format precedent: read `corpus/SOURCES.md:219-243` (Paths / Search log / Leads); no round-5x
   capture search-log entry exists yet (`grep round-5[0-9] corpus/SOURCES.md` → no hits), so my
   note is the first log entry over this capture set; note written in the established one-bullet
   dated style.
9. Instrument presence: `ls plans/round55_c3_chess_probe.py` → present (10,760 bytes);
   `ls corpus/evidence/round55/` → **absent at read time (2026-10-30)** — the probe receipt dir is
   not landed yet; E6ChessReceipt owns that surface. My note cites the receipt path as the frozen
   After-state does; it does not claim the receipt exists.

## Files I wrote (only these)

- `.ufo/waves/round-55/w1/S4SearchLog/search-log.md` — the splice-ready bounded-search note
  (question / where / screening / included / excluded / stop rationale; counts identified 89,
  excluded 17 = 12 already-read + 1 GH013-blocked + 4 screened-out, included 1, 71 unreached;
  arithmetic 89 = 12 + 1 + 5 + 71 spelled out in the note).
- `.ufo/waves/round-55/w1/S4SearchLog/report.md` — this report.
- `.ufo/waves/round-55/w1/S4SearchLog.md` — scoped-findings trailer required by the seat spec.

## Defects found

None inside my scope. One pre-landing observation, not a defect: `corpus/evidence/round55/` is
absent at my read time because the execution seat had not landed yet; the frozen claims' After
state places the receipt there.

## Dead ends

- First depth probe for grader files (`find … -mindepth 2 -maxdepth 2 -name test_outputs.py`)
  returned 0 — files live at `<task>/tests/test_outputs.py` (depth 3); redone per-dir, which also
  exposed the lone sanitize-git-repo dir without a test file.
- `grep "12 of" PROVINCE.md` matched only an unrelated feal line; the live "12 of 89" statement is
  phrased "12 of the 89 TB2 task graders" in `corpus/README.md` (Coverage map, r46 bullet) —
  cited from there instead of guessing a PROVINCE line.

## Installs / scratch

No tools installed or upgraded. No scratch dir created; nothing to delete.

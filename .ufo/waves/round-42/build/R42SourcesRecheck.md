# R42SourcesRecheck — kengaku sources recheck, 2026-10-26

Envelope: read-only seat; only `curl`/`gh`-style GETs and local reads, no file written outside scratch + this report (no bwrap needed, nothing in the lane or ~/.local/bin was written).
`date +%T` before 17:25:37, after 17:26:41. `ls -A /home/vgpnk/.local/bin | sha256sum` before = after = 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18 (re-measured after: identical).

## 1. Census
- `scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin kengaku` → 90 lines, all `kengaku cadence Sxxx recheck=<90d|180d|on-release> opened=...`; zero `overdue` lines; with `--today 2026-10-26` exit rc=0. **Rows due on or before 2026-10-26: 0** (oldest opened 2026-10-19, shortest cadence 90d → earliest due 2027-01-17, e.g. S014/S024/S025 opened 2026-10-19).
- `census`: rows=117 tier.A=99 tier.B=16 tier.C=2; mined=101 queued=8 rejected=8; invalid=0.
- `validate`: ends `kengaku ok corpus/SOURCES.md`; **W04 warnings = 15** (all "duplicate url … across scopes"): S040 (arxiv.org/abs/2301.09633), S048 (aclanthology.org/2020.acl-main.442), S057 (arxiv.org/abs/2405.11874), S058 (inspect_ai _pattern.py @63e45cc), S059 (rfc8259), S064 (commonmark 0.31.2), S065, S071, S075, S076 (docs.python.org/3/library/json.html), S066, S067 (doi 10.1017/S0950268810000385), S068, S069 (webarena @dce0468 test.raw.json / evaluators.py), S100 (github.com/laude-institute/terminal-bench-2). Census warnings never change exit status. No W code other than W04. S125-S127 are not yet in SOURCES.md (not counted).

## 2. Live opens (no due rows → the 4 highest drift-risk TB2 rows; S124 PR state included). Access 2026-10-26 17:25:51–17:26:00 -03.
Fetch base `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/`; PRs via `https://api.github.com/repos/harbor-framework/terminal-bench-2-1/pulls/<n>` (HTTP 200 each).

| row | live result | quote (≤25 w, located) | sha256 | verdict |
|---|---|---|---|---|
| S120 instruction.md (db-wal-recovery) | HTTP 200, 14 lines | instruction.md:7 “Fix the WAL file so SQLite can read it” | 5a20375162921b8911c67035d1905df7fd335d1bed03044271e608b2c3c93b26 = pinned | holds |
| S121 TB2.1 PR #3 | state=open merged=false draft=false, created 2026-05-21T21:43:34Z, updated 2026-06-11T03:20:48Z, closed_at null, 1 commit, 2 files (environment/Dockerfile, solution/solve.sh), head 6d8dc59c… | PR body line 13 (§Reasoning): “Opening the database with a normal read-write SQLite connection can truncate or remove that file before the agent has inspected it” | n/a (not pinned) | holds: still open/unmerged. One issue comment exists (IsThatYou, 2026-06-11: “5 agent runs before the fix:” + zip) — predates the 10-26 14:04 access; no new activity |
| S122 test_outputs.py (constraints-scheduling) | HTTP 200 | test_outputs.py:143 `assert not any(_overlap(s, e, cal) for cal in (A, B, C))`; :135 `s = _dt(r"DTSTART:(\d{8}T\d{6}Z)", c)` | 1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1 = pinned | holds |
| S123 instruction.md (constraints-scheduling) | HTTP 200 | instruction.md:18 “Any modification will cause the tests to fail.” | 342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6 = pinned | holds |
| S124 TB2.1 PR #245 | state=closed merged=false, created 2026-10-05T02:41:13Z, closed_at=updated_at 2026-10-08T19:02:36Z, comments=0 review_comments=0, 1 commit, 4 files, head ca2256bb… | live body: “the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar” | live body (CR-stripped) sha256 ce3735e8cca9…; capture corpus/evidence/round41/pr245-body.md (sha256 8f3b04c3… = pinned) differs from it only by its 4-line `#` header (diff shows only those 4 lines) | holds, unchanged since the 10-26 15:37 access |
Supplementary: TB2 `main` = 2fd12b88aafdd04a52c298e3940bcb189f9766d6 (committed 2026-04-30T05:53:30Z) — the pin is still HEAD of main; TB2.1 `main` = 7131e4375048a0e408a8fb404b5f499d726b695b (2026-08-11), the base cited by S124. `pulls?state=all` first page lists #245 only among name matches. S119 pinned sha256 88dc5c2a…ba49 reproduces on live fetch of db-wal-recovery/tests/test_outputs.py.

## 3. Drafted row changes (old → new)
None required. Every opened row still matches its pin/state, so status/recheck/used-by stay:
- S120 `mined | 180d` → unchanged; S122, S123, S124 `mined | 180d` → unchanged; S121 `mined | 90d` → unchanged (still open; the 90d cadence is the right one because the PR can merge or close — re-open at 2027-01-24).
- S125-S127 (circuit-fibsqrt) rows are not yet in SOURCES.md; the L1 admits them (not part of this recheck).
- Observation, no edit made: S122's anchor lists `:135, :143` but quotes only the :143 assert; :135 is the first-DTSTART line the teaches cell refers to. Anchor is not an in-place column, so fixing it would need a `supersedes` row; judged not worth one.

VERDICT: sources-rechecked-5-changes-0-w04-15

# F40ReopenRows — wave-2 falsify: live re-open of S119/S120/S121 and the S046/S052 anchor notes

Report: .ufo/waves/round-40/falsify/F40ReopenRows.md

Seat: F40ReopenRows (reviewer, leaf). Date: 2026-10-26. Lane tip under test: `ec1005a2a28bc5cfdde7723374368ed4cc956eed` (master).
Attack target: the C2 admission's three source rows and the round-40 S046/S052 anchor-note edits — every claim re-opened
live today; nothing accepted from wave-1 reports or the L1's own re-open receipts.

Method. Row text was read at the frozen tip, not the working tree:
`git -C <lane> show ec1005a2…:corpus/SOURCES.md | grep -E '^\| S(046|052|119|120|121) \|'` → 5 rows, receipt
`sources-rows-frozen-ec1005a2.txt` (3885 B). Drift check: same grep at lane HEAD `c9c793ca33fab1cdaf1127c06ba31685c7db1325`
→ `diff` exit 0 (`ROWS_IDENTICAL_FROZEN_VS_HEAD`); `git merge-base --is-ancestor ec1005a2 HEAD` → exit 0. Lane HEAD has
moved past the wave tip; the five rows have not. Live fetches: curl (S119/S120 raw files, Python docs) and
`gh api` (gh 2.102.0, authed). No tools installed or updated; pacman untouched; no lane writes; no git mutations;
no subagents, no background jobs.

## Check 1 — S119, `tests/test_outputs.py` (row SOURCES.md:134 @ ec1005a2) — OK

Live: `curl -sS -o live-test_outputs.py -w 'S119HTTP %{http_code}' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/db-wal-recovery/tests/test_outputs.py`
→ `S119HTTP 200`. `sha256sum` → `88dc5c2a3abba75bca0e0f9136223ae5bb585d5984b8d9eba51a7829c1d2ba49` = the row's sha256
cell = the capture's `SHA256SUMS` line; `cmp` vs capture → `S119_BYTES_MATCH_CAPTURE`. All 11 cells:

| # | cell | live evidence | ok |
|---|---|---|---|
| 1 | id `S119` | — | ✓ |
| 2 | name + raw URL | fetched exactly this URL, HTTP 200 | ✓ |
| 3 | kind `code` | Python test file | ✓ |
| 4 | tier `A` | maintainers' own grader code at a pinned commit; primary (entry §Source labels) | ✓ |
| 5 | scope "seven pytest functions over /app/recovered.json" | `grep -n 'def test_\|with open\|assert os\.path\.exists'` on the live bytes: 7 defs at :7, :12, :21, :38, :47, :83, :92; every read is `/app/recovered.json` (exists-check :9; opens :14, :23, :40, :49, :85, :94); no other path opened | ✓ |
| 6 | location `test_outputs.py:1-107`, `:98` quote, sha256 | `wc -l` → 107; line 98 byte-exact: "assert len(data) > 5, \"Only base data recovered - WAL decryption failed\"" (12 words as the cell claims); sha256 match | ✓ |
| 7 | teaches (existence, non-empty list, field types, id order, eleven ids, two pinned values, nine pinned names, unique ids, >5 rows) | live lines: :9; :17-18; :31-35; :44; :53 + :57-58; :64-67; :70-80 (cherry…mango on ids 3-11 = 9 names); :89; :98 | ✓ |
| 8 | status `mined` | cited by the admitted knowledge entry | ✓ |
| 9 | opened `2026-10-26` | lesson round-40.md:23 (L1 opened 13:05 -03) | ✓ |
| 10 | recheck `180d` | = entry frontmatter `recheck: 180d` | ✓ |
| 11 | used-by `corpus/knowledge/tb2-db-wal-recovery-grader.md` | entry cites S119 at :1; matches the same-class precedent (see F1) | ✓ |

## Check 2 — S120, `instruction.md` (row :135) — OK

Live: HTTP 200 at the row's URL; `sha256sum` → `5a20375162921b8911c67035d1905df7fd335d1bed03044271e608b2c3c93b26`
= row cell = capture; `cmp` → `S120_BYTES_MATCH_CAPTURE`. Cells: id/name/URL ✓; kind `docs` ✓; tier `A` ✓;
scope (maintainer's own spec at a pinned commit) ✓; location `instruction.md:1-14` (`wc -l` → 14) with the `:7`
quote "Fix the WAL file so SQLite can read it" (9 words) — live line 7 is `1. Fix the WAL file so SQLite can read it`,
the quoted span is that line minus the list marker ✓; sha256 ✓; teaches (three asks + format) = live :7, :8, :9 and
:11-13 ✓; status `mined` ✓; opened `2026-10-26` ✓; recheck `180d` ✓; used-by the knowledge entry ✓ (entry :2).

## Check 3 — S121, Terminal-Bench 2.1 PR #3 (row :136) — OK

Live: `gh api repos/harbor-framework/terminal-bench-2-1/pulls/3 --jq '{number,state,merged,merged_at,closed_at,created_at,updated_at,title}'`
→ `{"closed_at":null,"created_at":"2026-05-21T21:43:34Z","merged":false,"merged_at":null,"number":3,"state":"open","title":"fix(db-wal-recovery): Move encrypted WAL out of SQLite live sidecar path","updated_at":"2026-06-11T03:20:48Z"}`.
Cells: id/name/URL ✓; kind `docs` ✓; tier `B` ✓ (the benchmark repo reporting its own environment — self-report);
scope "open and unmerged at access" — re-opened live later than the row's 14:04 -03 stamp and still `state=open`,
`merged=false` ✓; location: opened 2026-05-21 ✓ (`created_at`), state/merged ✓, and the §Reasoning quote —
`pr3-body.md:11` is `## Reasoning`; `:13` contains byte-exact "Opening the database with a normal read-write SQLite
connection can truncate or remove that file before the agent has inspected it" (21 words, as the cell claims) ✓;
teaches "two-file fix … leaves the instruction and tests unchanged" — `gh api …/pulls/3/files --jq '.[] | "\(.filename) \(.status) +\(.additions)/-\(.deletions)"'`
→ exactly `tasks/db-wal-recovery/environment/Dockerfile modified +1/-1` and `tasks/db-wal-recovery/solution/solve.sh modified +8/-11`
(`changed_files=2`, head `fix/db-wal-recovery-encrypted-sidecar`, base `main`, 1 commit, not draft) — no `instruction.md`, no `tests/` ✓;
status `mined` ✓; opened `2026-10-26` ✓; recheck `90d` ✓; used-by the knowledge entry ✓ (entry's `source-note:` "cited by
§Prior art only" — the entry cites S121 only at :222, :299-302, :325).

## Check 4 — S046 anchor note (row :68) — OK

The note is the only freeze→tip change: `diff` of the S046/S052 rows at freeze `bbb1095…` vs tip `ec1005a2…` shows
exactly the appended `; rechecked 2026-10-26 on Python 3.15.2 docs (R40SourcesRecheck)` in the location cell; the other
10 cells are byte-identical; S119-S121 count at freeze = 0 (`grep -cE '^\| S1(19|20|21) \|'` → 0), i.e. new rows this round.

Live docs: `curl -sS -o live-re.html 'https://docs.python.org/3.15/library/re.html'` → 200, 257,706 B, sha256
`a99c3e85983a8aba2073827e0e34ee3b0925ddd57b4251584da7a8e9a46877cd` — byte-identical to the wave-1 seat's `/3/` fetch
recorded in `R40SourcesRecheck.md` (same hash, same size), so the rolling `/3/` alias serves the same bytes as `/3.15/`
today and nothing drifted since the wave-1 fetch. Version: the page says "Python 3.15.2 documentation" (`grep -o`, 2 hits);
`endoflife.date/api/python.json` cycle 3.15 → latest `3.15.2` — the note's "3.15.2" is still current. Anchor:
`grep -c 'id="regular-expression-syntax"'` → 1. Claim: live-re.html:803-804 — "Matches Unicode whitespace characters
(as defined by str.isspace()). This includes [ \t\n\r\f\v]" — `\r` present; the row's teaches (CR included) holds.

## Check 5 — S052 anchor note (row :74) — OK

Same diff result: only the note appended; 10 cells unchanged. Live docs: `curl -sS -o live-json.html
'https://docs.python.org/3.15/library/json.html'` → 200, 116,112 B, sha256 `1af0ba1d859bb4134d23b26446bb53735d0b48769a6947d36958ff1937aec8b7`
= the wave-1 seat's recorded hash (byte-identical). Version "Python 3.15.2 documentation" ✓; anchor
`grep -c 'id="json.JSONDecoder.raw_decode"'` → 1 ✓. Text: live-json.html:659-662 — "…return a 2-tuple of the Python
representation and the index in s where the document ended." and "This can be used to decode a JSON document from a
string that may have extraneous data at the end." (20 words) — the row's teaches ("returns an object and end index
while permitting trailing data") holds on the live 3.15.2 wording.

## Findings (receipts, not opinions)

- **F1 — observation, no defect (used-by convention).** S119-S121's used-by cells list only the knowledge entry while
  `corpus/lessons/round-40.md:23-26` also cites them (quote + sha256). This matches the same-class precedent exactly:
  extracted used-by cells at `ec1005a2` — S109 → `corpus/knowledge/tb2-regex-log-grader.md`; S117 →
  `corpus/knowledge/tb2-git-leak-recovery-grader.md`; S118 → same — none lists its admitting lesson. The landed cells
  follow the established pattern; the README.md:103 pointer-vs-backlink ambiguity stays the documented open question
  (round-27 `ScoutP4Locations.md:35-36`), unchanged by this round.
- **F2 — observation (historical ID collision).** `corpus/evidence/round29-attempt2/gate-strict.txt:43-49` prints
  `defect S119: recheck-prose` … `defect S121: recheck-prose`. Those IDs are the round-29/30 staged campaign's colliding
  numbering (round-30 lesson:21 "6 id collisions with this lane's registry"; :19 names staged S120/S121), not the
  round-40 rows. No current-row defect; flagged so a later census does not misread that artifact as a citation.
- **F3 — freshness.** S121 `updated_at 2026-06-11T03:20:48Z`: no upstream movement in >4 months; `state`/`merged` can
  flip at any time; the row's `90d` recheck (opened 2026-10-26 → due ≈2027-01-24) is the right cadence for a live PR.
- **F4 — wording note.** The landed notes read "rechecked 2026-10-26 on Python 3.15.2 docs (R40SourcesRecheck)" while
  the wave-1 report drafted "against Python 3.15.2 docs, same text" (`R40SourcesRecheck.md` §Changes drafted). The L1
  landed its own wording; lesson round-40.md:32 documents the old→new; every claim the landed note makes is verified
  live above. Not a defect.
- No defect found in any of the 55 cells checked (5 rows × 11). The entry's own recheck command also passes as written:
  `(cd corpus/evidence/round40/tb2-db-wal-recovery && sha256sum -c SHA256SUMS)` → all 8 files `OK`, exit 0.

## What this does not establish

- I did not re-run `plans/db_wal_probe.py`, the C1 battery, or any counter — out of this seat's scope (host-safety rule;
  not needed for a source re-open).
- S119/S120 are pinned to commit `2fd12b88`; `terminal-bench-2` `main` may have drifted since (the entry records "no
  drift at main" per wave-1; the pinned-URL re-open is what the rows claim, and it is what I verified).
- The docs pages are rolling live HTML; byte-identity holds as of today's fetch only (the rows pin no hash — the dated
  recheck note is the designed mechanism, and it is what I verified).

## Receipts (all under .ufo/waves/round-40/falsify/F40ReopenRows/)

`sources-rows-frozen-ec1005a2.txt` (the five rows at the wave tip) · `sources-rows-HEAD-c9c793ca.txt` (drift check,
identical) · `sources-rows-freeze-bbb1095.txt` + `sources-rows-tip-s046s052.txt` (freeze→tip diff inputs) ·
`live-test_outputs.py`, `live-instruction.md` (live S119/S120 bytes, sha256-matched to the capture) · `pr3-live.json`,
`pr3-body.md` (live PR #3 metadata + body) · `live-re.html`, `live-json.html` (live Python 3.15.2 docs pages).
Scratch `/fast/scratch/hyaku/kengaku-r40/F40ReopenRows` removed on completion. No lane files edited; no git mutations;
no installs; no processes left running.

VERDICT: rows-reopened-5/5

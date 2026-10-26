# R41SourcesRecheck — kengaku r41 wave 1

Accessed 2026-10-26 15:40–15:45 -03 (`date '+%F %T %z'` → `2026-10-26 15:40:26 -0300`). Read-only; no lane file touched. Scratch files in /fast/scratch (outside lane), not lane scratch tree.

## 1. Rows due on or before 2026-10-26

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin kengaku` (rc=0).
Output: 87 lines, all of the form `kengaku cadence Sxxx recheck=<90d|180d|on-release> opened=<date>`; **0 `overdue` lines**.
Check: `awk '{print $2}' | sort | uniq -c` → `87 cadence`.
Earliest due: oldest NNd rows opened 2026-10-19 with 90d (S014, S024, S025) → due 2027-01-17. Probe: `overdue --today 2027-01-18` → 25 overdue lines (`… | grep -c overdue` → 25), so the first dated recheck wave is Jan 2027.
Registry size: `census` → rows 114, tier A 97 / B 15 / C 2, mined 98 / queued 8 / rejected 8, missing 0 (FLEET totals equal; kengaku is the only target).
**Due rows: none.** So the fallback applied: the 4 highest drift-risk rows among S105-S121 (plus S100, the one unpinned URL).

Drift-risk ranking (mutable upstream state → immutable pin):
1. S114 — open TB2.1 issue (mutable, tier B)
2. S121 — open TB2.1 PR (mutable, tier B)
3. S100 — repo URL that 301-redirects and tracks a moving `main`, but row pins commit tree
4. S105 — representative pinned raw file; checks that the pin + sha still resolve (S105-S113, S115-S120 are all `raw…/2fd12b88…/` immutable-commit URLs, so they share its risk profile)

## 2. Live opens

### S114 — https://github.com/harbor-framework/terminal-bench-2-1/issues/133 (accessed 2026-10-26 15:41 -03)
- `gh`-style API: `curl -sS https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/133` → state `open`, created 2026-07-14T06:32:15Z, updated 2026-09-25T22:54:25Z, comments 2, author alexgshaw.
- Located quote (body line 39): "But the script has no `set -e` / explicit failure check on the clone/push." — row's quote reproduces verbatim.
- sha256: API `body` + one trailing LF = `c217d37253c89a71d6cc4d1c14f588c02ce49039cb1118dd3694150cf4c64193` (`(cat b133.md; echo) | sha256sum`; `cmp` against corpus/evidence/round37/prior-art/tb21-issue-133-body.md → identical). The pinned sha matches; body unchanged since capture. (Raw API body is 3352 bytes; capture is 3353, the extra byte is the LF — note for anyone re-deriving the hash.)
- Timeline: comment 2026-07-16 (shreyshahi, links fix PR #37), cross-reference 2026-07-17, comment 2026-09-25 (202520030411: instruction sentence "I'll setup login with the server to work, you don't have to worry about that." also causes false negatives; quoted from comment, truncated at 900 chars).
- PR #37 "fix(configure-git-webserver): verify the git/SSH pipeline instead of only the final HTTP check": `state open, merged False, merged_at None, updated 2026-07-17T06:26:13Z` (`/pulls/37`).
- Verdict: row claim still true (issue open, body sha equal). Status stays `mined`, recheck stays `90d`.
- Optional new evidence, not required by the row's scope ("as of the captured body"): a later comment reports false negatives, and a fix PR #37 exists, open/unmerged.
- Draft change (optional): anchor, append after "…open at access;": `; rechecked 2026-10-26 15:41 -03: still open, body sha unchanged, fix PR #37 open and unmerged, comments=2 (2026-09-25 adds false-negative report)`. status `mined` → `mined`; recheck `90d` → `90d`.

### S121 — https://github.com/harbor-framework/terminal-bench-2-1/pull/3 (accessed 2026-10-26 15:42 -03)
- `curl -sS …/pulls/3` → state `open`, merged `False`, merged_at None, closed_at None, created 2026-05-21T21:43:34Z, updated 2026-06-11T03:20:48Z, comments 1, author IsThatYou.
- Located quote (body line 13): "Opening the database with a normal read-write SQLite connection can truncate or remove that file before the agent has inspected it" — matches row's 21-word quote.
- Only comment (2026-06-11): "5 agent runs before the fix:" plus attachment pr3-db-wal-recovery.zip; no maintainer response.
- Verdict: no change. Row already records state check at 2026-10-26 14:04 -03; this is 98 minutes later, same state. status `mined`, recheck `90d`, unchanged.

### S100 — https://github.com/laude-institute/terminal-bench-2 (accessed 2026-10-26 15:43 -03)
- `curl -sSI` → `HTTP/2 301`, `location: https://github.com/harbor-framework/terminal-bench-2` — redirect remains as the row says.
- `curl -sS https://api.github.com/repos/harbor-framework/terminal-bench-2/contents/?ref=2fd12b88aafdd04a52c298e3940bcb189f9766d6` → `92 Counter({'dir': 89, 'file': 3})` — equals the row's 92 entries / 89 directories plus 3 files.
- `…/commits/main` → sha `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, committer date 2026-04-30T05:53:30Z, message "Add task metadata to task manifests" — main HEAD equals the pinned commit; no drift.
- Verdict: no change. status `mined`, recheck `180d` unchanged.

### S105 — pinned raw URL, protein-assembly grader (accessed 2026-10-26 15:43 -03)
- `curl -sSL …/2fd12b88…/protein-assembly/tests/test_outputs.py | sha256sum` → `44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` — equals row's pinned sha.
- Line 42: `    assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (` — row quote verbatim.
- Verdict: no change. status `mined`, recheck `180d` unchanged. Because upstream `main` still equals the pin (see S100), S106-S113 and S115-S120 (same commit, raw URLs) cannot have drifted; not individually re-hashed.

## 3. Changes summary (old → new)
| row | field | old | new |
|---|---|---|---|
| S114 | status / recheck | mined / 90d | mined / 90d (no change required) |
| S114 | anchor (optional) | "…open at access; capture … sha256 c217d372…" | append "; rechecked 2026-10-26: open, body sha equal, fix PR #37 open, 2 comments" |
| S121 | status / recheck | mined / 90d | unchanged |
| S100 | status / recheck | mined / 180d | unchanged |
| S105 | status / recheck | mined / 180d | unchanged |

Mandatory changes: **0**; optional anchor addendum: 1 (S114). I count k=0 (the addendum is not required; the row's claims remain true).

Not yet in registry: S122-S124 (C2 admission, pending). S124 (TB2.1 PR #245, tier B) must be opened live by whoever admits it; its `opened` date will not be due before 2027-01-24 at 90d.

## 4. Census W04 warnings now
Command: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (rc=0). `cut -f2 | sort | uniq -c` → `1 ok`, `15 W04`; no E-codes.
**w = 15**, over 14 URL groups (rows named first):
- S040 arxiv.org/abs/2301.09633
- S048 aclanthology.org/2020.acl-main.442
- S057 arxiv.org/abs/2405.11874
- S058 github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc5…/scorer/_pattern.py
- S059 rfc-editor.org/rfc/rfc8259
- S064 spec.commonmark.org/0.31.2
- S065, S071, S075, S076 docs.python.org/3/library/json.html (four rows, each warns, 4 of the 15)
- S066, S067 doi.org/10.1017/S0950268810000385
- S068 raw.githubusercontent.com/web-arena-x/webarena/dce04686…/config_files/test.raw.json
- S069 …/evaluation_harness/evaluators.py
- S100 github.com/laude-institute/terminal-bench-2
These are all pre-existing (earlier rounds' rows re-using a URL under a new scope; warnings do not change exit status). None of S105-S121 emit W04, so the round-40 TB2 admissions added none; planned S122/S123 use new raw URLs (instruction.md / tests/test_outputs.py under constraints-scheduling/ at the same pin) and would not duplicate. S124's PR #245 URL is new too. Predicted W04 after C2 admission: still 15 (assuming S122-S124 URLs are fresh).

VERDICT: sources-rechecked-4-changes-0-w04-15

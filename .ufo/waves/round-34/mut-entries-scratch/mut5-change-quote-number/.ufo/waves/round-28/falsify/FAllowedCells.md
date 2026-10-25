# FAllowedCells — SOURCES mutable-cell audit, b9b2479 → current (18b1922)

Seat: KengakuR28.FAllowedCells (reviewer). Method: read-only `git diff/show`, Python
cell parser (split on `|`, 13 cells/row), mtime evidence, seat-report cross-check.
No checker run, per assignment. Worktree `corpus/SOURCES.md` = HEAD (uncommitted delta: none).

## Findings

### F1 — Only the two allowed mutable-cell deltas were applied. PASS.

Parsed row sets: baseline 60 rows (S001–S060), current 66 (S001–S066); zero removed,
zero reordered. Cell-level diff over all 60 shared rows shows exactly two changed
rows, three changed cells, matching the allowance exactly:

- `S038` (SOURCES.md:60): cell8 `queued`→`mined`; cell11 `—`→`corpus/knowledge/attribution-interval-calibration.md`. All 11 other cells byte-identical.
- `S050` (SOURCES.md:72): cell11 `corpus/lessons/round-27.md`→`corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`. All other cells byte-identical — including the superseded teaches clause ("no hit is invalid_response_format"), correctly left immutable per S058.

No other S001–S060 row changed in any cell. File-level diff is +9/−2 lines total:
two modified rows, six appended rows, one appended changelog bullet; header, tier
contract legend, and all prior changelog bullets byte-identical.

### F2 — Lesson old→new table matches the applied diff exactly. PASS.

`corpus/lessons/round-28.md` "Actual mutable-cell changes after returned openings"
table declares exactly the three transitions in F1 (S038 status, S038 used-by, S050
used-by), and states existing recheck/opened cells unchanged — confirmed by the diff.
Prior-round lessons (round-27.md etc.) are untouched: the S050 used-by change reverses
round-27's lesson-*indexing* decision without mutating the historical lesson text;
`extraction-policy-comparison.md:123-125` records the reversal in-file.

### F3 — Actual reopen evidence precedes the cell changes. PASS.

- `build/OpenS050.md` (worktree mtime 2026-10-21 10:58:26, committed 18b1922) proposes, under "only after this opening": used-by += `corpus/knowledge/extraction-policy-comparison.md`, status stays mined — exactly what was applied. Its reopen fetched the pinned-commit `_pattern.py` (sha256 7974ddb4…) and verified byte-identity to PyPI 0.3.282 wheel members.
- `build/OpenS038.md` (mtime 11:01:16) proposes status `queued`→`mined` and used-by += the citing knowledge path — exactly applied (its optional `+corpus/lessons/round-28.md` was conditionally worded and legitimately omitted; see R1). Documents live-publisher HTTP 429s and an authenticated Wayback capture (2026-10-04, sha256 fc935f40…) of the publisher PDF plus corroborating live HTML — honest non-live disclosure.
- `corpus/SOURCES.md` mtime 11:03:58 postdates both reports; knowledge appends (11:02:51, 11:03:17) also precede it. Commit order caveat: the cell changes were snapshotted in wip `39a66fe` (11:24:13) before the `build/OpenS*.md` evidence files were committed in `18b1922` (11:27:30) — a staging artifact only; worktree authorship order is reopen → proposal → edit.

### F4 — S064/S066 supersede rather than overwrite. PASS.

`S054` and `S038` rows are byte-identical to baseline (parser-verified). S064
("supersedes S054's type/length shorthand — same character type and at least the
opening length, not necessarily equal length") and S066 ("supersedes S038's unqualified
fix clause — Blaker/Sterne construction assumes known sensitivity/specificity") are
new rows, matching the lane's established supersede-by-new-row pattern (S039/S040/S042/
S058/S059). Knowledge files carry append-only clarifications:
`attribution-interval-calibration.md` (+9 lines "Round28 source-scope clarification"),
`extraction-policy-comparison.md` (+13 lines); no deletions of prior content.

### F5 — S061–S066 are distinct opened scoped rows, not six new publications. PASS.

- S061/S062/S063: three distinct previously-unregistered files of pinned snapshot `dce04686` (config_files/test.raw.json; evaluation_harness/evaluators.py; helper_functions.py), each with distinct scope and sha256-pinned anchors; opening evidence `build/OpenTasks.md`/`OpenScorer.md`/`OpenHelpers.md`.
- S064: same URL as S054 (CommonMark §fenced-code-blocks) — a *publication repeat*, not a new publication; distinct narrowed scope (closing-fence type/min-length). Evidence: `build/OpenS054.md` (sha256 c85f56cc… re-verified) + lesson quote (≤25 words).
- S066: same DOI as S038 — same publication, distinct scope (known-vs-estimated Se/Sp caveat). Evidence: `build/OpenS038.md`.
- S065: only genuinely new URL (Python docs `#infinite-and-nan-number-values`, distinct anchor from S052's `#raw_decode`). Evidence: `build/OpenS059.md`.
- Changelog bullet itself states "scope/anchor extensions, not 3 new publications" — consistent with row facts. All six rows: `opened 2026-10-21`, tier A with per-row scope disclaimers, used-by = round-28 lesson + relevant knowledge path.

### F6 — Changelog counts consistent with fixtures. PASS (minor [INFERENCE]).

"4 identified/screened files" matches `plans/fixtures/r28/webarena/` upstream files
(test.raw.json, evaluators.py, helper_functions.py, LICENSE); "LICENSE retained
without separate row" matches its fixture presence and row absence. "Existing13 rows
reopened by OpenS038/OpenS049–OpenS060" — all 13 `build/OpenS0{38,49..60}.md` reports
exist. Population `plans/fixtures/r28/registry/population.json` confirms the frozen13
IDs, 35 knowledge_paths, and the literal-mention contract ("all standalone mentions
count… new round28 knowledge excluded"), which legitimizes the S050 used-by addition
as index-not-endorsement.

## Residual risk / gaps

- R1 (cosmetic, non-finding): `corpus/lessons/round-28.md` itself is absent from S038's and S050's used-by even though new rows list it and the contract permits extra lesson paths. Excluded from C2's frozen-35 math either way; consistent minimal-delta choice, not a defect.
- R2: precedence rests on worktree mtimes plus self-consistent report/commit content; adequate for an author-side audit.
- R3: S050's wheel-vs-commit "agreement" is byte-identity of two files, not a release-tag claim — the seat itself scoped it correctly; row anchor wording unchanged is compatible.
- Did not independently re-open any upstream source or run `registry_check.py` (assignment: no checker); seat-reported red→green expectation remains the instrument's own claim.

VERDICT: PASS

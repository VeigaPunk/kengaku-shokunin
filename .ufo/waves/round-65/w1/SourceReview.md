# SourceReview — round-65 w1 independent source re-open (seat SourceReview)

2026-11-03. Read-only over lane files; git read-only only. Network opens used: raw.githubusercontent.com/harbor-framework/terminal-bench-2 at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 (two files), sqlite.org/2026/sqlite-amalgamation-3540100.zip and sqlite.org/download.html — all named opens, nothing else. No tools installed (curl/unzip/awk/sha256sum/cmp sufficient); pacman untouched. No language server was used: every line-number claim below is verified with grep -n against committed bytes, and the refetched bytes are cmp-identical to the committed bytes, so every quote holds in both. Evidence receipts: .ufo/waves/round-65/w1/SourceReview/receipts/ (copied from scratch; scratch /fast/scratch/hyaku/kengaku-r65/SourceReview removed at close).

## 1. Independent re-opens (curl 2026-11-03, not trusting L1 captures)

| row | fetched sha256 (sha256sum) | bytes | cmp target | cmp rc |
|---|---|---|---|---|
| S232 raw…/2fd12b88…/sqlite-with-gcov/tests/test_outputs.py | b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b | 2166 | corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py | 0 (byte-identical) |
| S233 https://sqlite.org/2026/sqlite-amalgamation-3540100.zip | 0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9 | 2990966 | .ufo/waves/round-65/w1/sqlite-amalgamation-3540100.zip | 0 (byte-identical) |
| S234 raw…/2fd12b88…/kv-store-grpc/tests/test_outputs.py | 115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e | 6076 | corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py | 0 (byte-identical) |

All three shas equal the frozen claims values; S232 = SHA256SUMS line 167, S234/S230 = SHA256SUMS line 80 (grep-verified). S233's companion page open https://sqlite.org/download.html re-fetched: sha256 d0e3fb1a3d9a813560fb525c7124e0088f976a3bd66c330a64963649eb5b2a77 (18299 bytes) — byte-for-byte equal to the page sha recorded in S233's anchor cell.

## 2. Located quotes verbatim at the named lines (grep -n on committed bytes)

- S232 anchor names lines 51 and 25 — both exact:
  - line 25: `    assert sqlite_path is not None, "sqlite3 not found in PATH"`
  - line 51: `        "No .gcda files found, gcov instrumentation may not be enabled"`
  - File carries exactly three test functions in file order: test_sqlite_compiled, test_sqlite_in_path, test_gcov_enabled (claims' leg order confirmed in bytes).
- S233 anchor names the unzip -l four-file layout — verified on the refetched zip: exactly `sqlite-amalgamation-3540100/` (dir) + sqlite3.c (9582521) + shell.c (1270623) + sqlite3.h (695729) + sqlite3ext.h (39547), "5 files". The anchor's roster "sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h" matches 1:1. Minor note, not a defect: the quoted roster is a composite of the listing (each element verbatim in it), disclosed as such by the anchor's "(unzip -l, the four-file amalgamation layout)".
- S234 anchor names grader line 96 — exact and in source f-string form:
  - line 96: `    assert result == 0, f"Port {port} is not listening - no real gRPC server is running"`
  - This is the verbatim source line; S230's defect (quoting the rendered f-string `Port 5328 is not listening - …`) is genuinely corrected.

## 3. Row census (header: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by)

- NF==13 for S230/S232/S233/S234 (awk -F'|'); no `|` inside any cell; 11 content columns match the header.
- teaches = awk field 8; word counts: S230 = 34 (the routed defect, independently reproduced), S232 = 15, S233 = 14, S234 = 22 — all three new rows ≤ 25.
- Enums legal: kind `code` (all three), tier `A`, status ∈ {queued, queued, mined} ⊂ {queued, mined, rejected}; opened 2026-11-03.
- S230 row byte-unchanged from base: extracted `| S230 |…` line from `git show 12a6255170bcc466029bf82037885fd69e20370f:corpus/SOURCES.md` vs working tree → cmp identical, 1083 bytes both (receipts/s230-base.txt, s230-current.txt). Working tree clean for SOURCES.md; HEAD b5032ff8 "round-65: freeze …".
- S234 teaches opens `supersedes S230 — ` as required; `grep -c 'supersedes S230' corpus/SOURCES.md` → 1 (S234 only).
- Observation (no rule broken): S234's recheck cell is 90d while S230's is 180d; no rule fixes a recheck value for superseding rows.

## 4. Verdicts

- **S232 — AGREE.** Tier A code at the pin; independently re-opened, sha+cmp verified; anchors exact at lines 25/51; teaches 15 words. Status queued / used-by `—` is CORPUS-conformant: the citing entry corpus/knowledge/tb2-sqlite-gcov-offline.md does not exist yet (verified absent), and corpus practice is queued = opened-but-not-yet-cited (S020–S022, S038 precedent); the claims schedule the queued→mined flip with logged old→new only after the entry lands. Mining at the freeze would have asserted a citation that does not exist and would survive a C1 miss.
- **S233 — AGREE.** Official SQLite amalgamation, tier A; zip sha, byte count and download-page sha all reproduced by independent re-open; four-file layout verified by unzip -l; teaches 14 words; queued / used-by `—` on the same lifecycle rationale as S232.
- **S234 — AGREE.** Same URL/capture as S230 (re-fetched, cmp-identical to committed kv-store grader, sha = SHA256SUMS line 80); anchor quotes the grader's own f-string verbatim at line 96; teaches 22 words opening `supersedes S230 —`; S230 left byte-identical. Status mined + used-by at landing matches established correction-row practice (S039, S040, S227 all landed mined with used-by set).
- Defect lines: **none.** No row refused.

## 5. Watch item (non-defect, conditional)

At the freeze tip the kv-store knowledge entry does not yet name S234 (`grep -c S234 corpus/knowledge/tb2-kv-store-grpc-offline.md` → 0), and the other C2 counters are likewise still 0 at HEAD (R64-ERRATUM-65 = 0, addendum-classified = 0, Q47 = 0) — consistent with the freeze landing only claims+captures+S232–S234+spec (commit subject). The append-only addendum re-pointing the entry's citation from S230 to S234 is C2 repair 1's second half and must land before close; until then S234's used-by cell states the intended, not the landed, citation. This is the L1's C2 predicate to enforce, flagged here so it cannot pass unnoticed.

## Residual risk

S233's zip and page were re-opened same-day; sqlite.org can replace either at any time — the row's recheck cell (180d) governs future verification. S232/S233's queued state stays honest only while used-by remains `—`; the flip must be logged old→new in the round-65 lesson per the freeze.

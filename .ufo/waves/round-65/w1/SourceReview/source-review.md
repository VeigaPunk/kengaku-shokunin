# source-review.md — seat SourceReview (round-65 w1)

Copy of the seat report; canonical copy at .ufo/waves/round-65/w1/SourceReview.md.

## Per-row verdicts

- **S232 — AGREE**: tier A code at pin 2fd12b88; independent curl re-open sha256 b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b, cmp-identical to corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py (= SHA256SUMS line 167); anchors exact ("sqlite3 not found in PATH" line 25, "No .gcda files found, gcov instrumentation may not be enabled" line 51); teaches 15 words ≤25; queued/used-by `—` conformant — the citing knowledge entry does not exist yet (verified), corpus practice is queued = opened-but-not-yet-cited (S020–S022, S038), flip scheduled after the entry lands with logged old→new.
- **S233 — AGREE**: official amalgamation 3.54.1; refetched zip sha256 0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9 (2990966 bytes), cmp-identical to .ufo/waves/round-65/w1/sqlite-amalgamation-3540100.zip; download page re-open sha256 d0e3fb1a3d9a813560fb525c7124e0088f976a3bd66c330a64963649eb5b2a77 matches the anchor cell byte-for-byte; unzip -l shows exactly the four-file layout (sqlite3.c 9582521, shell.c 1270623, sqlite3.h 695729, sqlite3ext.h 39547); teaches 14 words ≤25; queued conformant as above. Minor note (not a defect): the anchor quote is a composite roster of the unzip -l listing, disclosed as such.
- **S234 — AGREE**: same URL as S230; refetch sha256 115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e (6076 bytes), cmp-identical to corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py (= SHA256SUMS line 80); anchor quotes grader source line 96 verbatim in f-string form (`assert result == 0, f"Port {port} is not listening - no real gRPC server is running"`); teaches 22 words opening `supersedes S230 —`; S230 row byte-identical base 12a62551 ↔ working tree (1083 bytes, cmp); `grep -c 'supersedes S230' corpus/SOURCES.md` → 1; status mined+used-by matches correction-row precedent (S039/S040/S227 all landed mined with used-by set).

## Defect lines

None. No row refused.

## Watch item (non-defect, conditional)

kv entry does not yet name S234 (grep -c S234 in corpus/knowledge/tb2-kv-store-grpc-offline.md → 0) and the other C2 counters are 0 at HEAD — the append-only re-point addendum (C2 repair 1, second half) must land before close or S234's used-by overstates. L1's C2 predicate to enforce.

## Census detail

NF==13 all checked rows; teaches (awk field 8 word counts): S230=34 (routed defect reproduced), S232=15, S233=14, S234=22; kind=code, tier=A legal; status queued/queued/mined legal; S234 recheck 90d vs S230 180d (no rule broken).

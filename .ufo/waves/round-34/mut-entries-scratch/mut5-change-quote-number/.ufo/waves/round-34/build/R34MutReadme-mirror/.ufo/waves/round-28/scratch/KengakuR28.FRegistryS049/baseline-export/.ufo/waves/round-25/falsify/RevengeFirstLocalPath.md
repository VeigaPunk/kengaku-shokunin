ATTACKS: plans/state_check.py first_local_path() (:857-881) + row_map() (:352-361) as used by P2d check_surfaces (:884-937) on the real PROVINCE.md `## Surfaces` rows, tip 8ea41f9ed
Method: pristine `git archive` of 8ea41f9ed and 6180e4f under /tmp/k25w2-RevengeFirstLocalPath/; harnesses trace.py, mut.py, m2clean.py, m9.sh run the tip script (sha256 8be61222…) via `--root <scratch copy> --json`. Lane tree read-only. No network; `ss -ltn` read only the local socket table.

Path tested per row (tip; `python3 trace.py`). The 9 path cells hold 61 backticked spans (~39 local-path-like); 9 are tested, one per row:
- L12 Research notes → `~/Projects/webzites/repos/llm-wiki` (span 1/6); exists=F, ABSENT row → MATCH. Untested: `wiki/…`, `wiki/ai/{…}/`, `Home.md`, `raw/`.
- L13 Benchmark battery → `~/archive/bench-arena/` (1/8); F, ABSENT → MATCH. Untested: `tasks/`, `grade.sh`, `loop.sh`, three csv files.
- L14 Served model → `/proc/1299/cmdline` (span 8/25). The URL is skipped by :863 and `/v1/*` and `/health` by :860-862. F, ABSENT → MATCH, plus `.url` OFFLINE_UNVERIFIABLE. Untested: `~/.config/systemd/user/qwen-coder.service`, `corpus/evidence/round10-fleet/r10-scout-endpoint.md`.
- L15 Route telemetry → `~/Projects/bounties/ledger/telemetry.jsonl`; F, literal **ABSENT** → MATCH.
- L16 Client CLI telemetry → `~/.bailian/telemetry.jsonl` (1/2); F, ABSENT → MATCH. Untested: `~/.bailian/wiki-sync-state.json`.
- L17 Model catalogs → `~/.bailian/skills/bailian-docs-llm-wiki/models`. The `{` truncation at :877-878 tests the parent directory, which the row never names; `index.md` and `models.jsonl` are never tested. F, ABSENT → MATCH, plus `.url`.
- L18 Own probe artifacts → `corpus/evidence/round8-horizon/` (1/10). The 9 bare `roundN-…/` spans fail both regexes at :867-874. T → MATCH.
- L19 In-repo gate → `grader.py` (second-branch bare filename, resolved from the repo root); T → MATCH. L20 Public literature → `corpus/knowledge/eval-prior-art-calibration.md`; T → MATCH, plus `.url`.
These verdicts reproduce the shipped counts: tip exit 0, P2d 9 MATCH/3 OFFLINE_UNVERIFIABLE; base 6180e4f exit 1, P2d MISMATCH on L12/13/14/16/17.

SURVIVES:
- A frozen row that is moved out of `## Surfaces` or renamed gives "row missing" MISMATCH (:903-906). It does not pass silently.
- The marker match is case-sensitive and whole-word (:924), so base L12 "`test -e` → absent" is not counted as a marker.
- In-repo hides are caught elsewhere. Removing `corpus/evidence/round12-ladder` leaves P2d MATCH but exits 1 through P2e row-to-file (README_INDEX_PATHS :121-130) and through P2a/P2b grader replay. Removing `round10-fleet` exits 1 through P2e alone.

BREAKS (hidden absences, all reproduced in scratch copies):
B1 First-path-only plus brace-to-parent (out-of-repo rows have no cross-coverage). `m2clean.py`: tip tree with the round-25 ABSENT tails removed from L12/L13/L16/L17, and HOME set to stubs that hold only each first path (empty dirs, one empty file). Of 10 named artifacts, 0 are present. Result: whole instrument exit 0, `mismatch=0`, the 4 rows MATCH exists=True. The live working-copy script gives the same result.
B2 row_map last-wins (:360). Control: L18 first path → `corpus/evidence/nonexistent-r25-dup/` gives MISMATCH, exit 1. Insert a duplicate row "`` `Own probe artifacts` ``" (backticks stripped at :359) and the result is exit 0 and `mismatch=0`. out_of_population stays 11, and the P2d assertion now cites L20. The earlier row's absent path vanishes without any record. [INFERENCE] The same last-wins applies to P2a (:441) and P2b (:517); not mutated.
B3 The ABSENT match covers the whole row and ignores negation (:924). Control: L19 path → `grader-r25-missing.py` gives MISMATCH. Adding the text "never ABSENT" gives MATCH with ABSENT_marked=true, exit 0. QUALITY.md:97 (R4) asks for `ABSENT <date>`; the code takes any bare token.
B4 A row with no parseable path and no URL is not a mismatch. Writing L18's first span bare like its 9 siblings (`round8-horizon-r25-missing/`) gives `.availability` OFFLINE_UNVERIFIABLE with url_or_endpoint=false, exit 0 (:914-918). The pre-registration (plans/round-25-claims.md:82-84) gives offline-unverifiable only to URL/endpoint rows.
B5 Brace generalisation. A first span `corpus/evidence/{r25-missing-a,r25-missing-b}/` tests `corpus/evidence` and gives MATCH, exit 0 (tip and live).
B6 The L14 verdict is decided by an unrelated PID. In `unshare -r -p -f --mount-proc sh m9.sh`, `sleep 120` was given pid 1299:
- tip → L14 `.path` MISMATCH (exists=true, ABSENT_marked=true), exit 1. This is a false alarm about a surface that did not change.
- tip script on base text → L14 MATCH (exists=true, unmarked). The absent served model hides behind the PID.
- live patch → OFFLINE_UNVERIFIABLE.
Reality check: `ss -ltn 'sport = :34113'` shows no listener. L14's ABSENT is therefore true, but only because of the stale PID.

Divergences in documents and contracts:
- The base "mismatch=11" (PROVINCE.md:117 at tip) counts L14's PID path. The pre-registration (:83-84) says URL rows are offline-unverifiable. The lane's own ProvinceScout.md:15 classed L14 OFFLINE-UNVERIFIABLE. It also tested L17's brace members (:18) and all 10 L18 dirs (:19), so the instrument is weaker than the manual procedure it automates.
- Lesson round-25.md:17 (M26) says "four absent first paths" and then "5 PROVINCE rows"; the fifth is the L14 PID artifact.
- The QUALITY R4 check (QUALITY.md:97) reads `awk -F'|' '… $2 ~ /`/'`, which is the surface-name column. Run verbatim it prints 11 Historical rows (PROVINCE.md:152-162) and 0 `## Surfaces` rows. Its premise of "one path per row" is false: the path cells hold 6/8/25/3/2/3/10/3/1 spans.
- Live drift: the working-copy state_check.py (sha256 b5027b4a…, uncommitted, not at the tip) adds an `endpoint_row` guard. That fixes B6, and the live PROVINCE.md:117 now says "10 mismatches". The live L14 still carries the dated ABSENT marker that cites "first local path fails `test -e`", but the live instrument no longer computes that. B1-B5 still reproduce on the live script.

VERDICT: PARTIAL — Row selection fails closed and in-repo paths have cross-coverage. But first-path-only, brace-to-parent, duplicate-row last-wins, a whole-row ABSENT match that ignores negation, and path-less rows marked OFFLINE_UNVERIFIABLE each let a row hide an absent path with exit 0. L14 also tests a stale round-10 PID: an unrelated pid 1299 flips its verdict on the tip, which is fixed only in the uncommitted live patch.
Installs: none.

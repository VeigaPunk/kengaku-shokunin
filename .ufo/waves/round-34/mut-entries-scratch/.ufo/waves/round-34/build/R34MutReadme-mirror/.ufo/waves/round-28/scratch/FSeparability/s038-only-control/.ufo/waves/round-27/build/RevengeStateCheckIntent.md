# RevengeStateCheckIntent: state_check v3 population/supersession map and P4 invariants (round 27)
Scope: read-only. Subject `plans/state_check.py` sha256 `32a684ffcb3fb222b0360333f83c2e4654c19ec1c3ad6ed47016052401428089` (2553 lines), byte-identical at `11a7fc8c64dc` and base `b5719440` (= v3). Scratch only in /tmp/kengaku-r27-RevengeStateCheckIntent/ (`base/` = git-archive copy, `recur/` = probe copy). No lane writes.

## Baseline (base b5719440, archive copy)
- `--summary`: `assertions=278 match=270 mismatch=0 superseded=5 offline_unverifiable=3`, 20 OUT_OF_POPULATION, VERDICT PASS, exit 0. Matches SCORECARD.md:789-791.
- `--selftest`: `[selftest] ALL PASS` (tail at lines 2487-2491).
- Keyed P2/P3 records: 298 (P2 255, P3 43). sha256 of canonical JSON of those records (`sort_keys`, separators `,:`, `ensure_ascii=False`) = `063981f941ea54f97aad7bddfe375e6bb54c27c6c91f2ef82be3bfbc19272c0d`, identical over 2 runs. This is the v4 byte-identity oracle for base.
- Per verdict: P2a M2 S1 OOP3 | P2b M9 | P2c M13 | P2d M8 OFF3 | P2e M199 OOP17 | P3a M12 S2 | P3b M7 S2 | P3c M7 | P3d M3 | P3e M10.

## 1. Population machinery (frozen; v4 must not edit)
- Tuples: CAPABILITY_IDS 39-42, AXIS_IDS 44-51, SURFACE_IDS 53-62, README_INDEX_PATHS 68-168, README_FILE_PATHS 171-173, AXIS_ANCHOR_CONTENT 195, P3C_PINS 218-227, P3D_TABLES/ANCHORS 228-234, P3E rows/files 235-248.
- Every OOP emitter: 645 (P2a rows), 721 (P2b rows), 1037 (P2c extra box), 1100 (P2d rows), 1229 and 1255 (P2e README rows / on-disk files; scope from actual_index_scope 1193-1206), 1691 and 1696 (P3c pointers), 1772 (P3d anchors).
- OOP is excluded from `assertions` (1830-1831) and never fails exit (2549). Base OOP: SCORECARD:558-560 (round-25/26 capability rows, P2a) and round-26 README rows/files (P2e).
- OFFLINE_UNVERIFIABLE emitters: 664 (P2a row lacking a command; MISMATCH only for COMMAND_CAPABILITIES, line 202), 1122 and 1141 (P2d). Base = PROVINCE.md:14, :17, :20.
- Exit map: 2 for usage/IO/empty population (2509-2539, 2546-2548); 1 iff any MISMATCH (2549).

## 2. Supersession machinery
- SUPERSEDE_RE 197 (`R2[5-9]-E`, already covers R27). Read at 549 (P2 path) and 580 (P3 path).
- P2 path `superseding_tokens` 540-552: SCORECARD only, no floor, lenient spans. Used only by P2a sources-registry (612-622; exact `"; ".join(tokens) == observed`; base SUPERSEDED via SCORECARD:647).
- P3 path `p3_superseding_tokens` 554-593:
  (a) doc not in P3_CORRECTION_FLOORS routes to SCORECARD (559-560); fallback to SCORECARD only when the primary has no matching line;
  (b) texts loaded only for P3_CORRECTION_DOCS (565) = SCORECARD (floor 730), PROVINCE (173), corpus/README.md (257), floors at 252-256;
  (c) correction id must be unique across those three docs (566-572; ID regex 258-259);
  (d) the LAST matching line decides (585). It is poisoned (None, no fallback) if line <= floor (587), not a strict fullmatch of P3_CORRECTION_LINE_RE 260-262 (586), or id/alias mismatch (590).
- `p3_record` 1268-1292: SUPERSEDED only if the check fails and correction tokens equal derived tokens by list equality (1281-1283).
- Base evidence: PROVINCE:180-181 carry trailing text (invalid form) and are shadowed by valid last lines 189-190, so last-match-wins holds. SCORECARD:739-750 are valid only because they sit after line 730.

## 3. Minimal P4 insertion points (append-only)
- I1 constants: after line 332 (P3_SELFTEST_ASSERTION_IDS). New P4 names only. Update the docstring (9-21).
- I2 functions `check_p4a..e` and `check_p4`: after check_p3e (ends 1797), before check_p3 (1800).
- I3 wiring: `check_all` (1807-1820): add `check_p4(root, assertions)` after line 1819. Never before the DUPLICATE_ROWS report (1816-1818).
- I4 selftest: new `write_p4_fixture`. Do not extend write_p3_fixture (1877-1994; it pads SCORECARD to 730 at 1912 and PROVINCE to 173 at 1936). Add a P4 class-id map beside 278-332, plus a loop and MISMATCH-free baseline check mirroring 2149-2166, calling check_p4 directly as P3 does. Place it before the final ALL PASS print (2487-2491).
- I5 untouched: Assertion 349-355, add 358-366, counts 1823-1839, print_summary 1842-1856, main 2494-2549, CommandRunner 433-487, ALLOWED_COMMANDS 182-185 (change only if a P4 instrument is run; never add state_check.py).

## 4. Invariants (P2/P3 keyed records identical)
- V1 Append-only: P2/P3 emitters, tuples, regexes, floors and Assertion fields unchanged. P4 ids must not start with P2/P3. Expected on the landed tree only: new OOP keys for R27 files and rows.
- V2 Verdicts: reuse the five strings (1825-1826). An unknown verdict is counted in `assertions` but never printed and never fails exit.
- V3 No row_map in P4 (493-507): it appends to global DUPLICATE_ROWS (490), and entries appended after 1816 are never reported. Use named_table_row (1258-1265).
- V4 Routing: R27-E corrections placed in SOURCES.md, lessons/ or knowledge/ are invisible to the P3 path (559-565). Put them in SCORECARD.md after line 730. The file ends at 810 and `## Round 26` (752) is its last H2, so EOF appends land inside §Round 26; a next_h2-bounded P4a scan (406-411) would ingest them. Pin P4a by content or base lines. Alternative: extend P3_CORRECTION_FLOORS with each doc's line count, then re-check the digest.
- V5 Form: `- **R27-E<n> (YYYY-MM-DD)** supersedes `<id>` — now `t1` `t2`.` (em dash; no trailing text; no backtick in tokens). Ids unique across the three docs; never reuse R26-E ids.
- V6 Tokens: derived_tokens must equal the correction's code spans verbatim (1281).
- V7 Census consumers: summary line 1 is echoed by round26_census.sh:61-64 and parsed by round25_census.sh:180-190. P4 counts change those numbers, so historical receipts stop reproducing. round26_census.sh counts only `^MISMATCH: P3[a-e]` (66): P4 lines need `MISMATCH: P4x`, and a round-27 census must count them.
- V8 No self-invocation: P4a must not run `state_check.py --summary` (claims :110, :126) or round26_census.sh (line 61 runs state_check). Probe: base copy with that command added to ALLOWED_COMMANDS and a probe in check_all, guarded at depth 3. Result `recur-chain.log` = depth 0,1,2,3, top rc 0. Only my guard stopped it. Neither CommandRunner (433-487) nor main (2494-2549) has a re-entry guard [INFERENCE: unbounded without one]. Read committed receipts instead (corpus/evidence/round26-calibration/state-check-final.txt, state-check-selftest-final.txt, round26-census-after.txt).
- V9 Offline is non-blocking: a required P4 input that cannot be read must be MISMATCH or exit 2, never OFFLINE_UNVERIFIABLE (base: offline_unverifiable=3 with exit 0). `git ls-tree` (claims :116-117, P4c) cannot run on an archive copy (no .git). `.ufo/waves/round-26/` is tracked (144 files) and survives git archive.
- V10 Fleet: find_protocol (800-815) reads root.parent and cwd ancestors; the seed drift check is at 2515-2524. P4 must not read outside the lane root.
- V11 Invisible to v3: SCORECARD:772-776 (`### Round-26 capabilities table additions`). find_line matches only `## Capabilities` (551), so P4a must register these rows explicitly.

## 5. Calibration notes
- Round-26 numbers reproduce on b5719440. SCORECARD:786-787 (`population1964 excluded0 audited verdicts15168 policy checks909`) = grader-perturb-final.txt:25 (`population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9`, exit=0): 5/5 MATCH. SCORECARD:789-791 (278 / 3 / mismatch 0) = this run.
- The pre-registered base-P4-mismatch prediction (p=0.55; claims :129-130) cannot be scored from P2/P3, which show 0 mismatches. [INFERENCE: it depends on P4 rows not yet built.]
- Precedent: corpus/evidence/round26-calibration/p2-preservation.txt compares full keyed projections (247 P2 records at f11bffbf). Reuse that method with the digest above.

VERDICT: v4 can be added by appending only (constants after 332; check_p4 after check_p3e; one call after 1819; its own fixture). Three hazards must be designed out first: self-invocation (V8), correction routing outside SCORECARD (V4), offline-as-pass (V9).
Installs: none (python3 stdlib; read-only `git archive`; sha256sum; tar). No lane writes except this report.

# Round 65 — a db-state grader replayed offline with a lane-built toolchain artifact; the round-64 closure's four defects corrected append-only, and a frozen byte-prefix clause that the freeze itself broke

author: kengaku L1 (round 65, attempt 1), 2026-11-03. Base `12a6255170bcc466029bf82037885fd69e20370f`;
freeze landing `b5032ff8391dcb5939c3be53516b31a50ab340a0` (claims doc `plans/round-65-claims.md`, pre-freeze
controls `corpus/evidence/round65/{g1,g2,g4,g5}-capture.txt`, `grader-import-scan.txt`, `c2-before-counters.txt`,
`census-before.txt`, registry rows S232–S234, validated wave dispatch). Wave `.ufo/waves/round-65/w1`: v1, 12 seats
(scout 1, executor 2, scribe 2, connector 1, reviewer 2, critic 1, mutation-tester 1, sentinel 1, revenger 1).
Claims: R65-C1 (coverage, L0-capped at 7; capability `offline-db-state-grader-probe`) and R65-C2 (calibration,
held at ceiling 10, exercised). Amendment A1 to the claims doc is dated below.

## Gate

**Sources opened this round (2026-11-03).** Each row: URL, access date, located quote ≤25 words with its location.

- **S232** — Terminal-Bench 2.0 `sqlite-with-gcov` grader, `tests/test_outputs.py` at pin
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-with-gcov/tests/test_outputs.py .
  Accessed 2026-11-03 (curl at the pin, HTTP 200). Located quotes: `"No .gcda files found, gcov instrumentation may not be enabled"` (grader line 51) and `"sqlite3 not found in PATH"` (line 25). Tier A code. sha256 `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b` = `corpus/evidence/round52/graders/SHA256SUMS` line 167; fetched bytes `cmp`-identical to the committed capture (GraderRecon and SourceReview seats). Pre-freeze captures corroborate: `sqlite3 not found in PATH` in `corpus/evidence/round65/g2-capture.txt`; `No .gcda files found` in `g5-capture.txt`; `No .gcno files found` (line 60) in `g4-capture.txt`.
- **S233** — SQLite amalgamation 3.54.1, https://sqlite.org/2026/sqlite-amalgamation-3540100.zip (download page https://sqlite.org/download.html). Accessed 2026-11-03 (curl, HTTP 200, **2990966 bytes**). Located quote (zip listing, `unzip -l`): `"sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h"` — the four-file amalgamation layout. Tier A official artifact. Zip sha256 `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9` (observed; re-observed by the GraderRecon seat). Download-page sha256 `d0e3fb1a…2a77` (observed).
- **S234** — Terminal-Bench 2.0 `kv-store-grpc` grader at the same pin (supersedes S230's anchor form), https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py . Accessed 2026-11-03. Located quote, grader line 96 verbatim: `assert result == 0, f"Port {port} is not listening - no real gRPC server is running"`. Tier A code; sha256 `115de2e9…1b0e` = `SHA256SUMS` line 80, byte-identical (SourceReview re-fetch and `cmp`).

**Admitted (this round).** S232 and S233 (both flipped `queued` → `mined`, `used-by` set to
`corpus/knowledge/tb2-sqlite-gcov-offline.md`); S234 (landed `mined`, `used-by`
`corpus/knowledge/tb2-kv-store-grpc-offline.md`). The knowledge entry `corpus/knowledge/tb2-sqlite-gcov-offline.md`
is admitted on the R65-C1 predicate and cites S232 and S233. The four R65-C2 correction artifacts are admitted as dated appends.

**Rejected (this round, with flip conditions).**
- `query-optimize` (the other `db-state` member) — **rejected as a replay candidate this round.** Reason: its
  `test_outputs.py` asserts `solution median ≤ 1.05 × golden median` (line 142) and pins an external
  database by sha256 (`/app/oewn.sqlite`, digest `89eab755…`, line 78); a wall-clock ratio and a sha-pinned
  external input are not freezable offline on this host. Flip: a dated amendment that replaces the timing
  leg with a deterministic plan-equality leg, or an operator ruling that the timing leg is admissible at a
  stated noise bound. Member stays recipe-unexecuted.
- `torch-pipeline-parallelism` / `torch-tensor-parallelism` (`process-environment` class, the next uncovered class) — **not selected this round, not measured**: both need a torch install and read the host environment (`corpus/evidence/round62/class-survey.txt`); no cp314 torch wheel availability was checked on this host, so no availability claim is made. Flip: a dated measurement of wheel availability for this host's python, or an L0 ruling.
- `nginx-request-logging`, `headless-terminal` (network-service, carried from r64): `nginx`/`vim` absent — unchanged.

**Registry state (before → after, `corpus/SOURCES.md`).** Rows 224 → 227 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`). Status histogram, base → end: `mined=203 queued=8 rejected=13` → `mined=206 queued=8 rejected=13`. Tier histogram at end: `A=198 B=24 C=5` (new rows A=3). Malformed rows 0, duplicate ids none. Census exit 0 at round start and end; the E11 `missing used-by` findings for S232/S233 existed between the freeze and the knowledge entry and cleared when it landed; W04 duplicate-URL warnings are pre-existing, plus S234's expected one.

**Registry changes logged old→new.**
- S232: `status queued → mined`; `used-by — → corpus/knowledge/tb2-sqlite-gcov-offline.md`.
- S233: `status queued → mined`; `used-by — → corpus/knowledge/tb2-sqlite-gcov-offline.md`.
- S230: unchanged (byte-identical base → end; its correction is the new row S234, not an in-place edit). Its `used-by` stays `corpus/knowledge/tb2-kv-store-grpc-offline.md`.
- S234: new row at the freeze (`mined`), `supersedes S230 —`.
- S232 anchor line numbers in the freeze text were corrected from 50/24 to 51/25, and S233's size from an unmeasured value to 2990966, before the freeze commit (see `## Mistakes` row 3).

**Spot-check (non-author discernment).** Not yet run by an outside verifier. The seats FreezeReview, SourceReview and ClaimFalsifier are lane-dispatched and are therefore NOT the outside check (LEARNING.md). Their findings are recorded as seat evidence only: SourceReview AGREE on S232, S233, S234 (sha, anchors, word counts); FreezeReview found F1/F2 (Mistakes rows 1–2); ClaimFalsifier killed or survived each attack (Mistakes rows 5–7). The admit/reject pair the non-author closure must spot-check: admit S232 (`corpus/evidence/round65/g1-capture.txt` against grader lines 25 and 51) and reject `query-optimize` (grader line 142 timing leg).

**Considerthese.** `considerthese/2026-10-26.md` is the latest reflection file. Its three "proposals only" items were already implemented before this round: proposal 1 (routed-findings burn-down) → `plans/routed_open.py` (`LOG.md` rounds 40–41); proposal 2 (standing grader-admission counter with a filler control) → the V9 counter (`LOG.md` rounds 44–45; `corpus/QUALITY.md` Q33); proposal 3 (batch TB2 class census) → the round-62 class survey (`corpus/evidence/round62/class-survey.txt`). **No still-unimplemented proposal remains in that file; none mined this round.**

**Assimilation.** `Assimilation: none` — the `merge/kengaku/` package (175 staged rows) remains blocked by id collisions (114 of 175 collide with the lane registry; `.ufo/waves/round-54/assimilation/`); L0 `kengaku | round-54` open. Nothing adopted.

**Quarantine slice.** Not applicable (wave-4 quarantine-first applies to tabi, revenger, chousa and kotodama).

**Operator teachings.** `corpus/lessons/operator-*.md`: none exist in this lane.

## Mistakes

Class · evidence pointer · captured-by (the criterion or rule that should have caught it, or `none`) · fix (and whether the fix was shown able to fail).

1. **Frozen append-only clause made unsatisfiable by the freeze's own landing** · `plans/round-65-claims.md` R65-C2 clause "keep their base bytes as a byte-prefix"; `cmp <(git show 12a62551:corpus/SOURCES.md) corpus/SOURCES.md` → `differ: char 181789, line 248` (FreezeReview F1, `.ufo/waves/round-65/w1/FreezeReview/findings.md`; ClaimFalsifier C2(h), `.ufo/waves/round-65/w1/ClaimFalsifier/falsifier.md`) · captured-by: **none** — the byte-prefix clause was first run after the freeze commit · fix: dated **Amendment A1** (below) restates the clause as zero deleted base lines (`git diff --numstat`) plus a line-deletion diff check. Shown able to fail: `corpus/evidence/round65/a1-prefix-check.txt` — the five touched files report `deleted_base_lines=0`, and a fixture with one base line removed reports `deleted_base_lines=1`. QUALITY Q48 (below) makes the freeze-tip run of every frozen clause a pre-freeze duty.
2. **Dispatch placed a SCORECARD block mid-file against an append-only clause** · `.ufo/waves/round-65/w1-spec.json` item ErrataBuild §3b ("after the round-64 section, before the Planned (round 65) block") against the same claims doc's byte-prefix clause (FreezeReview F2) · captured-by: **none** (the spec was validated for shape, not against the claims doc's clauses) · fix: the block is appended at end of file (`SCORECARD.md` `8 0` in the A1 numstat, zero deleted lines). Honest limit: the numstat check reds a mid-file insertion only if it also deletes a line, so this row's fix rests on A1 §(b)'s placement rule, not on the counter alone.
3. **Unverified location and size numbers entered into registry rows** · the S232 anchor cited grader lines 50 and 24 (true: 51 and 25); the S233 row carried a zip byte count I had not measured (I wrote `2934028` before measuring; `stat -c%s` of the fetched zip is `2990966`) · captured-by: **none** — CORPUS rule 1's located-quote check covers quotes, not byte counts or line numbers, and the census does not check them. It was caught by my own `grep -n` of the committed capture before the freeze commit · fix: rows corrected to the observed values before the commit; the claim's counting commands do not depend on those numbers. Not shown able to fail as a gate: open, routed to round 66 (a registry leg that re-derives anchor line numbers and byte counts from the capture).
4. **Rendered text quoted as source** (carried from the round-64 spot-check §7.1) · `corpus/SOURCES.md` S230 anchor and `corpus/lessons/round-64.md` (Gate bullet, line 20) quote `"Port 5328 is not listening - no real gRPC server is running"`; the source line has `f"Port {port} is not listening - …"` · captured-by: **none** at round 64 (the quote-location rule was satisfied by a rendering) · fix: S234 (verbatim f-string anchor, `supersedes S230 —`) and the appended `## Erratum (round 65)` block (token `R64-ERRATUM-65`) in the round-64 lesson. Shown able to fail: `grep -c 'Port 5328 is not listening' <grader>` → 0 (the rendered form is absent from the source), so a grep-based quote check rejects the old form.
5. **Text-only receipt checker admits a fabricated receipt (C1 limit; SecurityScan M-1, must-fix)** · `ClaimFalsifier/falsifier.md` attack C1(e), reproduced independently by the sentinel (`.ufo/waves/round-65/w1/SecurityScan.md` M-1, `plans/round65_c1_sqlite_probe.py` `receipt_failures` clauses `TOOLCHAIN` / `BUILD` / `RUN` / `FILES` / `NOBIND` check field presence, never value): a hand-written 2540-byte receipt with no compile, sandbox or driver run → `--check-receipt` rc 0, `PREDICATE R65-C1 pass` (`RUN G1 driver="fabricated - nothing ran"`) · captured-by: **the named limitation only** (`plans/round-65-claims.md` "Named limitation"; the probe docstring; the SKILL row; Amendment A1(e)). The frozen predicate names the gcc/gcov version line and does not pin its value; it does not require per-case artifact hashes. · fix: **not landed this round, by decision.** Two parts. (a) Pin the `TOOLCHAIN` values (`gcc`/`gcov` 16.2.1, `bwrap` 0.13.1, python 3.14.8) and bind the receipt to the probe sha256 `f44b7283…4db4eb`: a checker tightening that would be a rule change after the C1 receipts were scored (ProbeBuild, ClaimFalsifier, ProbeMutate), so it is not admissible as this claim's rule; routed to round 66 as the first counter amendment, frozen before its wave. (b) Per-case `.gcda`/`.gcno` hashes: a new counter the frozen predicate does not contain; round 66. Until (a) lands, the C1 verdict is stated as "predicate met on the text fields; live witness `corpus/evidence/round65/battery-run.txt`", never as "the counting command proves the run". Mitigation of record: `battery-run.txt` (per-case BUILD/RUN/FILES lines from the scored battery) and an independent second run `corpus/evidence/round65/replication-run2-receipt.txt` with the same vectors. Open instrument defect, reported as such.
6. **Counting instrument authored after the freeze** · `plans/round-65-claims.md` fixed the predicate and the counting command, but `plans/round65_c1_sqlite_probe.py` did not exist at freeze (FreezeReview F5) · captured-by: **none** · fix: the counter of record is the in-wave file, sha256 `f44b7283…4db4eb` (ClaimFalsifier and ProbeMutate copies match). Its frozen content is the claims doc's table and fragments; ProbeMutate's ten mutants (`.ufo/waves/round-65/w1/ProbeMutate/mutations.md`) show the instrument can fail on vector flips, mask drops, fragment weakening and a bad sha. Open: freeze the instrument's bytes before the wave, next round.
7. **C2 counter 1 is already at its target at the freeze tip** · `grep -c 'supersedes S230' corpus/SOURCES.md` = 1 at the freeze tip (S234 landed with the freeze), so the kill rule "any counter unmoved" is vacuous for it (FreezeReview F7) · captured-by: none · fix: recorded in A1 §(c). Token-stuffing survives the four counters (ClaimFalsifier C2(g)): a content-free EOF line satisfies all four greps, so the repair's substance is judged by the non-author closure, not by the counters. Open (named).

**Quality criteria added this round** (each cites its lesson):
- **Q47** — wave-evidence paths in lane reports are lane-root-based or state the lane-root base once (round-64 spot-check §7.3; this round's report follows it).
- **Q48** — a frozen counting clause that asserts an append-only, byte-prefix or no-deletion property is executed against the freeze tip (base → freeze commit) before the freeze commit, and any clause the freeze itself breaks is restated by a dated amendment before any after-receipt is scored (mistake rows 1–2; shown able to fail: `corpus/evidence/round65/a1-prefix-check.txt`, fixture `deleted_base_lines=1`).

## Stale and open

- L0 carried: `kengaku | round-25/33/51` (coverage cap), `kengaku | round-56`, `kengaku | round-63` (amended K2 detector, unanswered), `kengaku | round-54` (assimilation mass id drift). Nothing assumed answered.
- Open defects: `## Mistakes` rows 3, 5, 6, 7 (named; routed to round 66).
- "At the landing tip" in the claims doc means the round-end tip (FreezeReview F8).

## Amendment A1 (dated 2026-11-03; written after the wave settled and before any C2 after-receipt was scored; appended to `plans/round-65-claims.md`)

- **(a)** The C2 byte-prefix clause is restated: for each touched file, `git diff --numstat 12a62551 -- <file>` reports zero deleted lines, and `diff <(git show 12a62551:<file>) <file> | grep -c '^<'` is 0. The clause's intent (no filed byte is rewritten) is kept; the insertion-based reading that the freeze's own row placement required is recorded.
- **(b)** The SCORECARD correction block is placed at end of file (append), not before `### Planned (round 65)`.
- **(c)** Counter 1 (`supersedes S230`) is an end-of-round target (= 1), not a base-relative "moved" count.
- **Reason:** FreezeReview F1/F2, ClaimFalsifier C2(h). Evidence of the amended check and its red control: `corpus/evidence/round65/a1-prefix-check.txt`.

## SHONEN

Round lesson only; the SHONEN checklist is in `SHONEN.md` and the round report.

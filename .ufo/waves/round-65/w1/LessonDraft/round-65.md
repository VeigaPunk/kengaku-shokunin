# Round 65 — <one-line thesis filled by the L1>

author: kengaku L1 (round 65, attempt 1). Round 65, date 2026-11-03. Base `12a6255170bcc466029bf82037885fd69e20370f`;
freeze `b5032ff8` (claims doc `plans/round-65-claims.md`, pre-freeze control captures
`corpus/evidence/round65/{g1,g2,g4,g5}-capture.txt`, `grader-import-scan.txt`,
`c2-before-counters.txt`, `census-before.txt`, the new registry rows S232/S233/S234, and the
validated wave dispatch) landed BEFORE any scored run. Wave `.ufo/waves/round-65/w1`: v1, 12 seats —
scout `GraderRecon`; executor `ProbeBuild`, `ErrataBuild`; scribe `KnowledgeDraft`, `LessonDraft`;
connector `SiblingOverlap`; reviewer `FreezeReview`, `SourceReview`; critic `ClaimFalsifier`;
mutation-tester `ProbeMutate`; sentinel `SecurityScan`; revenger `ControlOrigin`. Claims: R65-C1
(coverage, lowest non-retired axis, L0-capped at 7 — capability acquisition
`offline-db-state-grader-probe`) and R65-C2 (calibration, held at ceiling 10, exercised — the
round-64 closure's four routed defects land as dated, append-only corrections). Predicates, counting
commands, kill rules, frozen leg vectors and controls are fixed in `plans/round-65-claims.md`; no
seat may change them, and any later change is a dated amendment the L1 writes, never a seat edit.

## Gate

**Sources opened this round (2026-11-03).** Three registry candidates, each with its URL, its access
date, and a ≤25-word located quote whose location is named. Quotes below are verifiable against the
committed pre-freeze captures (`corpus/evidence/round65/`) and the pinned grader captures
(`corpus/evidence/round52/graders/`).

- **S232** — Terminal-Bench 2.0 `sqlite-with-gcov` grader, `tests/test_outputs.py` at pin
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-with-gcov/tests/test_outputs.py .
  Accessed 2026-11-03. Located quotes (≤25 words): `"No .gcda files found, gcov instrumentation may not be enabled"`
  (line 51) and `"sqlite3 not found in PATH"` (line 25). Tier A code. sha256
  `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b` = `corpus/evidence/round52/graders/SHA256SUMS`
  line 167; the committed capture at `corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py`
  hashes to the same value (`sha256sum`, observed at this seat). The two quoted fragments are
  corroborated by the committed pre-freeze captures: `"sqlite3 not found in PATH"` appears in
  `corpus/evidence/round65/g2-capture.txt` (leg 2, `AssertionError`), and
  `"No .gcda files found, gcov instrumentation may not be enabled"` appears in
  `corpus/evidence/round65/g5-capture.txt` (leg 3). The `.gcno` sibling fragment
  `"No .gcno files found, gcov instrumentation may not be enabled"` (line 60) appears in
  `corpus/evidence/round65/g4-capture.txt` (leg 3).
- **S233** — SQLite amalgamation 3.54.1,
  https://sqlite.org/2026/sqlite-amalgamation-3540100.zip (named download page
  https://sqlite.org/download.html). Accessed 2026-11-03. Located quote (≤25 words, from the zip
  file list): `"sqlite3.c, shell.c, sqlite3.h, sqlite3ext.h"` (`unzip -l`, the four-file amalgamation
  layout). Tier A official artifact. Zip sha256
  `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9`, byte-verified at this seat
  (`sha256sum .ufo/waves/round-65/w1/sqlite-amalgamation-3540100.zip`, 2990966 bytes); the same
  `unzip -l` listing shows the four quoted member names under the `sqlite-amalgamation-3540100/`
  directory prefix.
- **S234** — Terminal-Bench 2.0 `kv-store-grpc` grader, `tests/test_outputs.py` at pin `2fd12b88`
  (supersedes S230 form),
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py .
  Accessed 2026-11-03. Located quote (≤25 words, the grader's verbatim source line 96):
  `assert result == 0, f"Port {port} is not listening - no real gRPC server is running"`. Tier A code.
  sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` = `SHA256SUMS` line 80;
  the committed capture at `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py` hashes
  to the same value and its line 96 is byte-identical to the quote (observed at this seat).

**Registry state.** Rows S232, S233 and S234 are written at the freeze: S232 and S233 carry status
`queued` and S234 carries status `mined` with `used-by corpus/knowledge/tb2-kv-store-grpc-offline.md`
(`corpus/SOURCES.md`, rows read at this seat). The L1 flips S232/S233 `queued` → `mined` and sets their
`used-by` ONLY after the round-65 knowledge entry lands, and logs each registry old→new in this
lesson. The registry census at round start was exit 0 with 227 rows and W04 duplicate-URL warnings
only (`corpus/evidence/round65/census-before.txt`); S234's URL duplicates S230's, which the census
already reports as one W04 warning, not a new defect.

**Four R65-C2 correction artifacts (dated, append-only).** Each is an append over the base bytes; the
base bytes are kept as a byte-prefix, verified by `cmp`.

1. **S234 superseding row** — a new registry row whose `teaches` cell opens `supersedes S230 —` and
   whose anchor quotes the grader's own f-string verbatim (line 96). S230's row stays byte-identical.
2. **`corpus/lessons/round-64.md` `## Erratum (round 65)` block** — dated 2026-11-03, marker token
   `R64-ERRATUM-65`, correcting the Gate quote form and citing the spot-check §7.1 and the grader
   source line.
3. **`SCORECARD.md` dated correction block** — appended after the round-64 section, marking the
   round-64 freshness-10 claims `addendum-classified`.
4. **`corpus/QUALITY.md` criterion Q47 —** wave-evidence paths in lane reports are cited lane-root-based
   or state the lane-root base; the round-64 spot-check §7.3 is its lesson.

**Admit / reject decisions (LEARNING.md discernment).**

- ADMIT `corpus/knowledge/tb2-sqlite-gcov-offline.md` (S232/S233 cited) — the first offline replay of
  the `db-state` class member `sqlite-with-gcov`, admitted only if the frozen R65-C1 predicate holds.
- ADMIT the S234 superseding row and the three append-only corrections above, on the R65-C2 predicate.
- REJECT as a candidate: `query-optimize` (the other `db-state` member). It hard-codes a timing
  threshold (`solution median ≤ 1.05 × golden median`) and a 250 MB-class external database
  (`/app/oewn.sqlite`, sha-pinned inside the grader), so its legs are not safely freezable before data
  on this host. It stays recipe-unexecuted, named in the SKILL `db-state` row flip.
- REJECT as a candidate: `torch-pipeline-parallelism` (a `process-environment` member). Its harness
  needs torch wheels, absent for cp314 on this host; the same `process-environment` reasoning that
  blocked r64's `nginx`/`vim` candidates applies (`install-windows-3.11` is blocked for the same
  class reason: Windows installers).
- REJECT as a rewrite: the frozen entries' opening bytes are not edited; every correction is an
  appended dated block (append-only outranks the defect list).

**Spot-check result:** (pending outside verifier) — the non-author spot-check for round 65 is not yet
written; the L1 records the outside verifier's verdict here at landing.

**No-bind observation.** The grader under execution binds no network port: an AST scan of the pinned
capture lists the top-level imports `['os', 'shutil', 'subprocess']` (stdlib only,
`corpus/evidence/round65/grader-import-scan.txt`), and a direct grep of the capture for bind
primitives (`socket`, `.bind(`, `listen(`, `AF_INET`, `SOCK_STREAM`, `http`, `requests`, `urllib`,
`127.0.0.1`, `localhost`, a `:<port>` literal) returns no match (observed at this seat). No seat in
this wave starts a server or binds a port.

**Host facts re-measured at this seat (2026-11-03).** `gcc`/`gcov` 16.2.1 20260810, bubblewrap 0.13.1,
`/usr/bin/python3` 3.14.8, host `/usr/bin/sqlite3` 3.54.0. No venv is needed this round: the grader
imports stdlib only.

## Mistakes

Instruction to the L1 (placeholder — the rows themselves are mined from the wave's outcomes, one row
per defect, in the four-cell shape `class . evidence pointer . captured-by . fix`; mine only what the
wave's seats actually observed, and leave a defect that no seat observed out rather than inventing it):

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| <one-line instruction placeholder for the L1: mine the round-65 wave outcomes into this four-cell row shape; every row must cite a receipt file that exists under `.ufo/waves/round-65/w1/` or `corpus/evidence/round65/`, and a defect with no seat observation is not a row> | <path of the seat receipt or wave file> | <seat name> | <the fix that landed, or the honest refusal> |

## Carried → closed / open

<placeholder for the L1: the round-64 closure's four routed defects, each closed or carried with its
evidence pointer; the L0 questions still open (`kengaku | round-25/33/51` coverage cap,
`kengaku | round-56` L2 surface / ledger host column, `kengaku | round-63` amended K2 detector);
`kengaku | round-54` merge/kengaku mass-id drift; and the lesson-backed limits carried from round 64
(`--check-receipt` cannot prove a live run; the trio gate's red on the frozen openings is named drift
by design).>

## Assimilation

<placeholder for the L1: round 65's own merge/kengaku mass-id drift status.>

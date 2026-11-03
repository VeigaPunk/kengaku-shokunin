# Round 64 — kengaku lesson (2026-11-03)

author: kengaku L1 (round 64, attempt 1). Base `5f517fe7147831f96a9900c9642c07ee71031940`; freeze
`859ac24f41061bffde588b9ed5d5adfea5ca8e27` (claims doc, pre-freeze controls K2/K4, before-state receipts, wave spec,
validated dispatch) landed BEFORE the wave ran. Wave `.ufo/waves/round-64/w1`: v1, 15 seats — 5 executor (ProbeBuild,
GateScopePatch, SweepBuild, SweepRepairA, SweepRepairB), 2 scribe (IndexParity, KnowledgeDraft), 1 scout (GraderRecon),
1 connector (SiblingOverlap), 2 reviewer (FreezeReview, SourceReview), 1 critic (ClaimFalsifier), 1 mutation-tester
(ProbeMutate), 1 revenger (ControlOrigin), 1 sentinel (SecurityScan). Claims: R64-C1 (coverage, `kv-store-grpc`, capability
acquisition), R64-C2 (operability, depth-gate scope repair, routed defect 3), R64-C3 (freshness, provenance-trio sweep and
lesson-index parity, routed defects 1+2). Amendment A1 of `plans/round-64-claims.md` records every post-freeze change.

## Gate

**Sources opened this round (2026-11-03).**

- **S230** — TB2 `kv-store-grpc` grader at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/kv-store-grpc/tests/test_outputs.py .
  Re-fetched by curl in two seats (GraderRecon `s230-test_outputs.py`; SourceReview `s230-test_outputs.py`), HTTP 200, 6076
  bytes; sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` in both = `SHA256SUMS` line 80; `cmp` byte-identical
  to the lane capture. Located quotes (≤25 words): `"Port 5328 is not listening - no real gRPC server is running"` (line 96),
  `"except grpc.RpcError"` (line 128). Tier A code.
- **S231** — gRPC Python API reference, https://grpc.github.io/grpc/python/grpc.html . Fetched by curl in two seats (GraderRecon
  `s231-grpc-python.html`; SourceReview `s231-grpc-python-api.html`), HTTP 200, 250738 bytes, sha256
  `d68676105b4bbf7f701eb3458e95db7efd5fe6129408eba4b574dff23ea083e4`. Located quotes: `"Raised by the gRPC library to indicate
  non-OK-status RPC termination."` (section `exception grpc.RpcError`, anchor `#grpc.RpcError`), `"The service is currently
  unavailable."` (anchor `#grpc.StatusCode.UNAVAILABLE`). Tier A docs. The page is unversioned: recheck is by re-fetch and re-hash (90d).

Both rows are appended to `corpus/SOURCES.md` (222 → 224; `sources-census.sh validate --root … kengaku` exit 0 at round
start and end). Quote verdicts by SourceReview: `VERIFIED` for both.

**Admit / reject decisions (LEARNING.md discernment).**

- ADMIT `corpus/knowledge/tb2-kv-store-grpc-offline.md` — the second network-service TB2 grader replayed offline. Its
  Results section carries the receipt of record and the pre-hardening pair (Amendment A1 item 4).
- ADMIT the R64-C2 gate repair (the frozen patch, byte-identical to the GateScopePatch seat's file) and the R64-C3 sweep
  tool (after the Q46 correction: Amendment A1 item 2).
- REJECT as a candidate: `headless-terminal` and `nginx-request-logging` (the other two network-service members). Their
  harnesses need `vim` and `nginx`; both are ABSENT on this host (`command -v` → absent, recorded in the claims doc host note).
  A scored run would have measured SETUP, not the grader. Flip: a host with both binaries, a captured stdout per the Q45 rule.
- REJECT as a rewrite: the 29 frozen trio-red entries are NOT repaired by editing their opening bytes. The forbidden form is
  pinned by the `sweep-openedit` leg. Each repair is an appended dated addendum.
- REJECT the wave's bullet-form and timestamp-form addenda as they were emitted (format, not content; Mistakes row 5).

**Non-author spot-check (agree/disagree, for the closure).** FreezeReview: **agree** with the C1 and C2 counters against
their frozen sentences; **disagree** with C3's pass path (a Major: the counter did not price clause (a)), reproduced in
`openedit-sim.txt` and fixed before any after-receipt was scored. SourceReview: **agree** with both admits (byte-identical
captures, quotes located). ClaimFalsifier: **agree** with the probe's refusals (forged receipts and port contention) and with
the gate's escape verdicts; it reported no falsification of C1 vectors (independent derivation from the grader source matched
the frozen table cell for cell). SecurityScan: five findings triaged in Amendment A1 (H-1 fixed by canonical addendum shape;
M-2, L-1 fixed; M-1 fixed; L-2 carried r63 M-2; symlink escape named as a limit of the frozen lexical rule). ProbeMutate: three
of six mutants survived on the pre-fix tools; m5 fixed with a selftest leg, m6 covered by the fixed pass path, m4 a named
redundancy survivor.

**Flip checks.** Round-63 lesson `## Gate` refusals: the amended K2 detector (runs 2–3) is still rejected as the verdict;
L0 `kengaku | round-63` is open and routed around. `kengaku | round-25/33/51` (coverage cap) and `kengaku | round-56` (L2
surface; ledger host column) are open. No existing registry row flipped except `network-service` (executed 1 of 8, dated).

**Census.** Round start: exit 0, 222 rows, 22 W04 (`.ufo/waves/round-64/frontier/census-start.txt`). Round end: exit 0,
224 rows, 22 W04 (the same pre-existing duplicate-URL warnings; the two new rows add none). Receipt
`.ufo/waves/round-64/frontier/census-end.txt`.

**Standing gates (round start → end).** `grader.py` `CHECKS n=733 mismatches=0`; `round56_landcheck.py` FAIL (`L-reg`, the
registry closure: `MISSING 2`, the round-63 instruments) → `PASS n=4`; `round52_c2_registry.py` `MISSING 2` → `MISSING 0`,
`PREDICATE R52-C2 pass`; the depth gate `PREDICATE R63-C2 pass` at every stage.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **registration gap carried across a round boundary** — the round-63 close advertised `plans/round63_c1_pypi_probe.py` and `plans/round63_gate_checks.py` without SKILL registry rows or ledger rows; the round-64 landcheck red was the first sign | `.ufo/waves/round-64/frontier/landcheck-start.txt` (`MISSING 2`); `gates-at-start-v2.txt` | the landcheck `L-reg` leg, at round start | registry rows `round63-c1-pypi-probe`, `round63-gate-checks` and ledger rows of the same names; `reg-after-r63rows.txt` (`MISSING 0`); Amendment A1 item 1. Lesson-backed rule: a close lists every advertised instrument's registry row before its receipt is filed |
| **counter narrower than the frozen sentence (the forbidden repair passes)** — the sweep's pass path was `red == 0`; the frozen sentence requires every previously-red entry to carry the dated addendum | `.ufo/waves/round-64/w1/FreezeReview/openedit-sim.txt` (`SWEEP files=29 trio_open=29 addendum=0 red=0`, `PREDICATE R64-C3 pass`, rc 0) | FreezeReview (non-author; reproduced by simulation before any after-data existed) | pass path requires every frozen entry to classify `TRIO-ADDENDUM`; selftest leg `sweep-openedit` (rc 1 `not-addendum=<1>`): `corpus/evidence/round64/sweep-selftest.txt`. QUALITY Q46 |
| **instrument reads a sibling's path outside the lane** — the sweep's `FROZEN_LIST_ABS` fallback resolves the frozen list to a host path when the lane-local copy is missing, the same out-of-root shape R64-C2 forbids the gate to accept | `.ufo/waves/round-64/w1/SecurityScan.md` §M-2 | SecurityScan (sentinel), after the tool landed | fallback removed; no lane-local list is `SETUP frozen-list-unreadable`, rc 2 (`corpus/evidence/round64/sweep-fail-closed.txt`) |
| **frozen list unpinned** — the sweep printed the list's sha256 but compared it to nothing; a substituted list was graded as if it were the frozen one | `SecurityScan.md` §L-1 | SecurityScan | the lane-local list is pinned to `fe0498fb…`; a substituted list is `SETUP frozen-list-substituted`, rc 2 (`sweep-fail-closed.txt`); an explicit `--frozen` override is a caller's choice and is not pinned |
| **addendum emitted in two shapes neither matching the frozen grammar** — slice A wrote markdown bullets (`- verified-at:`), slice B wrote `verified-at: 2026-11-03T…Z`; the bullet form is the L1's own spec template error (the seat followed the spec) | `.ufo/waves/round-64/w1/SecurityScan.md` §H-1; `corpus/evidence/round64/addenda-normalization-diff.txt` (45 bullet strips, 14 timestamp moves) | the sweep's strict grammar, on the first real application (29 RED); SecurityScan H-1 | normalized to the canonical form the tool accepts; byte-prefix check 29/29 (`append-only-prefix-check.txt`); Amendment A1 item 3. The spec template now names the canonical form |
| **install step inherited the ambient environment** — `uv venv`/`uv pip install` (the one network step) ran with the host HOME and pip/uv configuration | `.ufo/waves/round-64/w1/SecurityScan.md` §M-1 | SecurityScan | `_tool_env(work)` (scratch-rooted HOME and caches, `UV_NO_CONFIG`, `PIP_CONFIG_FILE=/dev/null`); the receipt of record re-run under it (`corpus/evidence/round64/kvstore-probe.txt`); the pre-hardening pair kept under `prehardening/` (Amendment A1 item 4) |
| **knowledge entry cited a superseded receipt** — after the hardened re-run, the draft's scored-run section still named the pre-hardening sha and PIDs | `corpus/knowledge/tb2-kv-store-grpc-offline.md` (corrected section; `diff prehardening/… kvstore-probe.txt` = 4 changed lines) | the L1's pre-landing pointer check (every cited path resolved; the stale PIDs were not a path) | section rewritten to the receipt of record, the measured diff stated as measured (only the K1 and K3 `server_pid` differ) |
| **mutation survivor on a predicate-bearing alternative** — the round-63 heading was not a tested negative, so the heading match was unexercised | `.ufo/waves/round-64/w1/ProbeMutate/mutate-report.md` (m5) | ProbeMutate (mutation-tester) | selftest leg `ROUND63-HEADING` → TRIO-RED, shown green. m4 (probe `case-line-missing` guard, redundant with the VECTOR line) survived and is named, not claimed killed |
| **freeze cited a red-before path that did not exist** | `plans/round-64-claims.md` (the cited `corpus/evidence/round64/escape-before.txt`); FreezeReview Minor | FreezeReview | the receipt copied to the cited path (identical bytes); Amendment A1 item 5 |
| **environment: first control attempt used a uv-managed python outside the sandbox** — the venv's `python` symlink resolved to a uv-managed interpreter that `bwrap --ro-bind /usr` cannot exec, so K2 and K4 failed with `execvp … No such file` before any grader ran | `controls/` attempts (bwrap rc 1 ×4) | the bwrap exec error itself | venv built with `uv venv --python /usr/bin/python3` (the probe's own rule); controls then ran (`k2-empty-capture.txt`, `k4-protoonly-capture.txt`) |
| **EOF newline join** — appending a block to an entry whose last line lacked a final newline changes that line's bytes (its terminator) | `git diff --stat` (1 deletion, `corpus/knowledge/bench-arena-round12-ladder.md`) | the `git diff --stat` read after the append | prefix holds (byte-prefix check); named in Amendment A1 item 3 rather than hidden. Rule: the appender writes a terminator first when the file lacks one |

## Carried → closed / open

- Routed defect 1 (provenance trio omission, round 62): the 29 entries that fail the round-63 trio gate now each carry a
  dated round-64 addendum with a re-verification command and observed result (`sweep-after.txt`, `red=0`). The trio gate
  itself still reads the openings as red, by design: CORPUS.md prohibits in-place opening edits. The gate's red on those 29
  is the record of drift; the sweep is the declared freshness form.
- Routed defect 2 (lesson-index parity): rounds 57–62 indexed (`corpus/README.md`); the before-count receipt
  `.ufo/waves/round-64/claims/before-state.txt`.
- Routed defect 3 (depth-gate scope): CLOSED by R64-C2 (red-before `escape-red-before.txt`, green `escape-after.txt`).
- Routed defect 4 (`--check-receipt` cannot prove a live run): carried, named in the registry row and the entry.
- Routed defect 5 (L0 `kengaku | round-63`, the amended K2 detector): OPEN, routed around. R63-C1 stays MISS; run 1 is not re-scored.
- Routed defect 6 (the network-service recipe cell): the kv-store-grpc member flips to executed (dated); the pypi-server cell stays
  recipe-unexecuted.
- Lesson-backed limits carried: the lexical escape rule (symlink traversal not caught; Amendment A1 item 6); the sweep does
  not execute `recheck:` commands (the closure's duty); `executed17.lst` (the round-62 census's executed set) is unchanged,
  so the new kv-store execution is recorded in the SKILL row and the entry, not in the census receipt.
- L0 questions still open: `kengaku | round-25/33/51` (coverage cap), `kengaku | round-56` (L2 surface; ledger host column),
  `kengaku | round-63` (K2 detector). No new L0 question is needed this round.
- Round-63 closure defects: §5.1 (index gap 57–62) closed; §5.2 (verified-at drift on the 29 frozen entries) closed by addenda;
  §5.3 closed; §5.4 carried; §5.5 open; §5.6 closed for kv-store (recipe executed) and carried for pypi-server.
- SiblingOverlap (`.ufo/waves/round-64/w1/SiblingOverlap/sibling-overlap.md`): five contested-scope items routed, not absorbed.
  The gRPC-inside-bwrap pattern is kengaku ground; kama's serving-plane ground is not touched.

## Assimilation

`Assimilation: none — merge/kengaku mass id drift (L0 kengaku | round-54) still open; considerthese 2026-10-26 proposal 3
(batch TB2 grader sweep) is served by the round-62 class census and the round-64 kv-store probe, not re-adopted`.

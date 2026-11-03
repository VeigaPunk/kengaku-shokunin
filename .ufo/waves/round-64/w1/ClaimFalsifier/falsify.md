# ClaimFalsifier — round-64 attack ledger (falsify.md)

Attack seat, Kengaku r64 w1. Scratch: `/fast/scratch/hyaku/kengaku-r64/ClaimFalsifier`
(removed at seat exit; receipts copied into this dir first). Instruments were taken from
sibling clones at the freeze commit, sha256-recorded in `instr/`:
`gate_base.py` 797085c2…, `gate_patched.py` da5f087c… (GateScopePatch clone,
differs from base only by the frozen `_resolves` repair), `trio_sweep.py` 56638ea1…
(SweepBuild clone), `kvstore_probe.py` (ProbeBuild, hashed when taken).
No lane file was edited; no server started; no port bound; no git/jj mutation anywhere.

---

## C1(a) — independent vector derivation from the grader source

Grader: `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py`,
sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` (recomputed,
matches SHA256SUMS line 80 and the freeze). All seven bodies read in full (raw ranges 1–70,
71–140, 140–171). Leg rule (frozen): P iff the function returns normally; F on any exception.

Per-leg deciding asserts:
- L1 `test_proto_file_creation`: `/app/kv-store.proto` exists AND contains
  `service KVStore`, `rpc GetVal`, `rpc SetVal`, `message GetValRequest`,
  `message SetValResponse`.
- L2 `test_grpc_tools_installation`: `import grpc` (ImportError → assert False).
- L3 `test_protobuf_generation`: `/app/kv_store_pb2.py` and `/app/kv_store_pb2_grpc.py`
  exist (existence only; content never imported here).
- L4 `test_server_file_creation`: `/app/server.py` exists AND contains `class Server`.
- L5 `test_real_grpc_server_running`: `connect_ex(("127.0.0.1", 5328)) == 0`;
  failure message is exactly the frozen K2 fragment
  `Port 5328 is not listening - no real gRPC server is running`.
- L6 `test_grpc_protocol_handshake`: imports `grpc`, `kv_store_pb2`, `kv_store_pb2_grpc`
  BEFORE the try (a missing module raises out of the function → F); then
  `stub.SetVal(handshake, 999)`; `response.val == 999` asserted; `except grpc.RpcError`
  prints and RETURNS normally; any other exception → assert False.
- L7 `test_grpc_server_functionality`: imports before try; SetVal(42)→42, GetVal→42,
  SetVal(100)→100, GetVal→100; no except clause, only finally.

My derived table (from source alone):

| case | my derivation | frozen | match |
|---|---|---|---|
| K1 compliant | P P P P P P P | P P P P P P P | ✓ |
| K2 empty | F P F F F F F | F P F F F F F | ✓ |
| K3 wrong-math | P P P P P F F | P P P P P F F | ✓ (conditional, see note) |
| K4 proto-only | P P F F F F F | P P F F F F F | ✓ |
| K5 files-no-server | P P P P F P F | P P P P F P F | ✓ |

Cross-checks against committed control bytes (all recomputed):
- K4 control proto `corpus/evidence/round64/control-k4-kv-store.proto`
  (sha256 `c89bcb1c…` recomputed): contains all five L1 strings (grep count 1 each) →
  K4 L1=P derived independently, not trusted from the capture.
- K2 capture (sha `ae0a78ee…` recomputed): LEGS F P F F F F F; L5 class exactly
  `AssertionError: Port 5328 is not listening - no real gRPC server is running`; L6/L7 class
  `ModuleNotFoundError: No module named 'kv_store_pb2'` — confirms legs continue after a
  failure and that ModuleNotFoundError is NOT swallowed by the L6 RpcError catch.
- K4 capture (sha `b262cfe5…` recomputed): LEGS P P F F F F F, same classes.

Note on K3 (the one derivation-conditional cell): L6=P / L7=F for K3 requires the case's
SetVal handler to return the STORED (+1) value (response.val==1000≠999 → AssertionError →
`except Exception` → F). If the K3 fixture echoed the request value while storing +1, L6
would be P and the vector would MISS. The frozen vector pins the first reading; ProbeBuild's
fixture implementation must match it. [Checked against ProbeBuild's battery receipt in C1(b)
below — the observed vector decides.]

**C1(a) verdict: no cell I would have predicted differently. The frozen 5×7 table is
derivable from the grader source as written.**

## C1(b) — forged/adversarial receipts vs `--check-receipt`

Probe landed at `plans/round64_c1_kvstore_probe.py` (sha256 `9f56d25ddb33e14474c6439c16f25dd5545da99e542a051d342113a88b306843`,
recomputed). Receipt of record `corpus/evidence/round64/kvstore-probe.txt`: GRADER sha+pin
lines, `PORTFREE before-battery True`, per-case CASE/LEG/PORTFREE lines, K2-FRAGMENT line,
VECTOR lines, `SERVERLOG file=…`, `PREDICATE R64-C1 pass`. The checker re-derives the
predicate from three redundant planes (VECTOR lines, CASE observed/expected, per-LEG
verdicts) plus port/pid/fragment clauses, and flags stored-vs-derived disagreement.

Seven forgeries (driver `c1_forged.py`, fixtures `c1/f*.txt`, full outputs
`c1-forged-receipts.txt` in this seat dir):

| forgery | mutation | rc | named failure |
|---|---|---|---|
| f1 | empty file | 1 | 36 failures (grader/vector/case/port/fragment/pid/predicate all missing) |
| f2 | all PORTFREE lines stripped (vectors+fragment intact) | 1 | port-free-at-battery-start + per-case port lines missing; stored `pass` disagrees with derived `fail` |
| f3 | K2-FRAGMENT line removed | 1 | k2-fragment lacks 'Port 5328 is not listening' |
| f4 | fragment kept ONLY in the summary line; K2 leg-5 `frag=` field replaced | 1 | k2 leg-5 fragment does not carry the frozen fragment (leg-level binding holds) |
| f5 | K5 leg-6 flipped in the VECTOR line | 1 | K5 vector != frozen |
| f6 | grader sha256 zeroed | 1 | grader-sha mismatch |
| f7 | K1 `server_pid=none` | 1 | K1 server_pid not recorded |
| control | unmodified real receipt | **0** | `CHECK ok cases=5`, `PREDICATE R64-C1 pass` |

The assigned three attacks are f1 (empty), f3 (missing fragment clause), f2 (vectors but no
port line): all rc 1. The kill-rule scenario (K2 leg-5 answering P through a foreign
listener) is structurally excluded: any K2 leg-5=P forces the K2 vector off the frozen
value, and the battery separately refuses an occupied port before grading.

**C1(b) verdict: SURVIVES — every forgery fails with a named finding; only the unmodified
receipt passes.** The named limitation (text-only re-derivation, no proof of a live run)
stands as frozen and is backed by the server-log sidecar.

**C1(a) conditional resolved:** the live receipt's K3 leg fragments
(`Not a real gRPC server: gRPC server must return the correct value` on leg 6,
`SetVal returned wrong value: 43` on leg 7) confirm the K3 fixture's SetVal returns the
stored (+1) value — my derived K3 reading (and the frozen vector) is the correct one.
Observed vectors in the receipt equal the frozen table for all five cases, and
`--check-receipt` passes rc 0 (control above).

## C2 — attacks on the patched depth gate

Attack harness: `c2_driver.py` (scratch), fixtures under `c2/`; receipts
`c2-attacks.txt`, `c2-predicate-legs.txt` in this seat dir.

| id | input (row-0 pointer unless noted) | base gate | patched gate | verdict for the claim |
|---|---|---|---|---|
| T1a | `` `a/../../etc/hostname` `` (the assigned example) | rc1 `DETAIL row-pointer=cls-00:no-path-token` | identical | token has no counted suffix → never a path token → escape class never sees it; fails only via the pre-existing no-path-token rule. Not an escape-class test. |
| T1b | `` `../../../../etc/` `` (counted, dotdot) | rc1 row-pointer+unresolved (target absent) | rc1 **`DETAIL escape=../../../../etc/`**, share=0.94 shown failing | escape named and failing as frozen |
| T2 | `` `records/` `` directory inside root | rc0 pass | rc0 pass | no over-rejection regression |
| T3 | URL token in section prose | rc0 pass | rc0 pass | URL excluded before escape accounting — patch order preserves the PEP-503 exemption |
| T3b | URL as only pointer-cell content | rc1 no-path-token | rc1 no-path-token | unchanged pre-existing rule |
| T4 | ABSOLUTE path to a file that EXISTS inside root | **rc0 pass** (resolved!) | rc1 **`DETAIL escape=<abs path>`** | sharpest discriminator: "relative-only" holds even for inside-root absolutes |
| T5 | `` `link/secret.md` `` via symlink to outside dir | rc0 pass | **rc0 pass — resolved** | RESIDUAL GAP (see below) |

Committed predicate legs, re-run by me against the GateScopePatch clone AND repeated
against the LANDED gate `plans/round63_gate_checks.py` (sha256
`a98d9c0f75600ea4f99573d2ca291b1ffd97cffc18a53a3a65dce7b7941dfe17`, recomputed; receipts
`c2-attacks-landed.txt`, `c2-predicate-legs-landed.txt`): all verdicts identical — T6b rc 1
with `DETAIL escape=/home/vgpnk/.config/uv/uv-receipt.json`; T7 4/4 `SELFTEST pass` rc 0;
T8 real section `total=24 resolved=24 share=1.00` rc 0; T4 landed rc 1 vs base rc 0; **T5
symlink escape passes the landed gate too (rc 0)** — the residual is in the integrated
repair, not just the clone.

**C2 verdict: SURVIVES.** Every assigned attack input produces the frozen behavior; the two
assigned escape shapes (absolute, `..`) fail with `DETAIL escape=` and rc 1; directory and
URL tokens do not regress. Two recorded residuals (neither falsifies the claim as frozen):
1. **Symlink escape (T5):** `_escape_reason` is lexical (`normpath`), so a token that leaves
   the root through an in-root symlink resolves and the gate PASSES while the pointer reads
   outside-root bytes. The repair closes the lexical escape class named by L-1, not the
   physical one.
2. **Suffix-gated visibility (T1a):** a `..` token without a counted suffix
   (`a/../../etc/hostname`) is invisible to path accounting entirely; it fails only via the
   generic no-path-token rule. A future `..` token shaped like prose (no `/`-suffix) prices
   neither as resolved nor as escape.

## C3 — attacks on the trio sweep

Attack harness: `c3_driver.sh` (scratch). Two instruments tested: the SweepBuild clone sweep
(sha256 `56638ea1…`, receipt `c3-attacks.txt`) and the LANDED sweep
`plans/round64_trio_sweep.py` (sha256 `b559b87cedeeef0a3d9faf9be9ab5cb1ceff4e859d39c04a1e8a427d4586a4f2`,
recomputed; receipt `c3-attacks-landed.txt`). Skeletons built from EXACT freeze-commit bytes
(`git archive 859ac24f… corpus/knowledge` + frozen list, sha256 `fe0498fb…` recomputed).

**Method incident, recorded for provenance:** the first landed-sweep run restored attack
victims from the LIVE lane, which repair seats were concurrently modifying — the lane's
`telemetry-run-design.md` had already gained a real round-64 addendum mid-run, so forgeries
were appended to an already-ADDENDUM file and the red count shifted under me. That run is
superseded; the recorded landed results below use freeze-commit bytes only, re-freshened per
case, with a POST recount proving no bleed.

Landed-sweep results (clone results in parentheses where they differ):

| id | input | observed (landed) | verdict |
|---|---|---|---|
| BASE | pristine freeze-commit skeleton | `SWEEP files=65 trio_open=36 addendum=0 red=29`, `PREDICATE R64-C3 fail`, rc 1; INFO frozen sha `fe0498fb…` entries=29 | equals the frozen red-before |
| C3a | addendum with `verified-at: 2026-11-02` (wrong date) | stays RED (red=29), rc 1, `NOTE addendum-incomplete missing=verified-at: 2026-11-03,result:` | **stays RED as required** |
| C3b | correct date, NO recheck line | stays RED (red=29), rc 1, `NOTE addendum-incomplete missing=recheck:,result:` | **stays RED as required** |
| C3d | correct date + `recheck: echo fabricated…` (no result line) | stays RED (red=29), rc 1, `NOTE addendum-incomplete missing=result:` — the landed sweep is STRICTER than the clone: it also requires a `result:` line before ADDENDUM | forged green blocked at the instrument |
| C3f | fully-shaped forgery: date + recheck + `result: exit 0 (fabricated)` | entry classified ADDENDUM → red=28 → `SETUP frozen-list-mismatch` rc 2 (DETAIL names the entry) | a lone forgery still cannot pass while any base red remains |
| C3c | frozen entry `tb2-grader-vacuity-triage.md` REMOVED from disk | **SETUP frozen-list-mismatch**, rc 2, `DETAIL frozen=<29> observed=<28> missing=<…>` | answer to the assigned question: SETUP, not red, not pass |
| C3e | red=0 lane whose frozen list names an absent entry | **SETUP frozen-entry-missing**, rc 2 (`DETAIL frozen-entries-absent=<1>`) | a deletion can never be the repair |
| POST | fresh freeze-commit copy | red=29 again, rc 1 | no scratch bleed |

**C3 verdict: SURVIVES.** Wrong-date and recheck-less addenda stay RED with named stderr
diagnostics on both instruments; removal is SETUP (exit 2), never a silent pass; the
frozen-list cross-check blocks any single forged repair, and the landed tool additionally
prices the addendum's `result:` line (presence only). Recorded residual: the sweep cannot
price whether a `result:` line is TRUE or whether the `recheck:` command behaves as named —
`recheck: true` with a fabricated result line leaves the red set (C3f). The guard for that
is exactly the frozen kill rule: the closure re-runs every named command; a command that
does not re-derive fails the claim there.

## Verdicts

- **R64-C1: SURVIVES.** (a) My independently derived 5×7 table from the grader source equals
  the frozen table cell-for-cell; the one conditional (K3 leg-6) was resolved in the frozen
  vector's favor by the live receipt's leg fragments. (b) Seven forged receipts all fail
  `--check-receipt` rc 1 with named findings; only the unmodified receipt passes rc 0.
- **R64-C2: SURVIVES.** All assigned attack shapes behave as frozen under both the patch
  clone and the landed gate; selftest 4/4; real section unregulated (24/24 resolved, rc 0).
  Residuals (do not falsify the frozen repair): symlink escapes resolve (lexical-only
  escape detection), and suffix-less `..` tokens are invisible to path accounting.
- **R64-C3: SURVIVES.** Wrong-date and recheck-less addenda stay RED; entry removal is
  SETUP exit 2; the cross-check blocks lone forged greens; the red=0 path still demands
  every frozen entry exist on disk.

**Sharpest finding (cross-claim):** the C2 repair's escape class is lexical only —
`link/secret.md` through an in-root symlink reads outside-root bytes and the LANDED gate
counts it resolved, passing rc 0 (T5, `c2-attacks-landed.txt`). The frozen repair's letter
("relative, no `..`, normpath inside root") is satisfied, so this is a scope bound for the
next routed defect, not a kill: any future gate consumer that trusts `resolved` pointers as
root-confined should `resolve()` physically or refuse symlinked directory components.

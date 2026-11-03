# KnowledgeDraft — round 64, wave 1 (v1), seat `KnowledgeDraft-2`

Scribe seat. Scope: the R64-C1 knowledge entry draft, the SCORECARD capability row text, the
SKILL registry row text, the SKILL decision-table flip text and the dated LOG line. **No
predicate, counter, kill rule, leg vector or control was changed by this seat.** The frozen
file `plans/round-64-claims.md` (freeze commit `859ac24f41061bffde588b9ed5d5adfea5ca8e27`, base
tip `5f517fe7147831f96a9900c9642c07ee71031940`) was read in full and treated as the only rule
source. No lane file outside my seat dir was written; the scratch dir
`/fast/scratch/hyaku/kengaku-r64/KnowledgeDraft/` was removed after the receipts were copied.

## Files written

| path (relative to the lane root) | what |
|---|---|
| `.ufo/waves/round-64/w1/KnowledgeDraft/tb2-kv-store-grpc-offline.md` | the new knowledge entry (mirrors lane path `corpus/knowledge/tb2-kv-store-grpc-offline.md`) |
| `.ufo/waves/round-64/w1/KnowledgeDraft/registry-drafts.md` | the SCORECARD capability row text, the SKILL registry row text (cell-by-cell + as one row), the decision-table flip text, the dated LOG line, and the measured findings |
| `.ufo/waves/round-64/w1/KnowledgeDraft/receipts/verification.txt` | every command output this seat observed, with its command |
| `.ufo/waves/round-64/w1/KnowledgeDraft/receipts/kvstore-probe.txt`, `kvstore-probe-rerun.txt`, `kvstore-probe.txt.server-log`, `selftest.txt`, `determinism.txt`, `check-receipt.txt` | copies of the ProbeBuild seat's receipts that the drafts cite, kept beside the drafts so the cited bytes are present |
| `.ufo/waves/round-64/w1/KnowledgeDraft.md` | this report |

## Verdict: all three deliverables complete; C1 observed PASS

The probe receipt (ProbeBuild seat; wave copy sha256 `a87cd119…`, and the L1 landed the same
bytes at `corpus/evidence/round64/kvstore-probe.txt` — `cmp` rc 0) records, verbatim:

```
VECTOR K1=P/P/P/P/P/P/P
VECTOR K2=F/P/F/F/F/F/F
VECTOR K3=P/P/P/P/P/F/F
VECTOR K4=P/P/F/F/F/F/F
VECTOR K5=P/P/P/P/F/P/F
PREDICATE R64-C1 pass
```

The five observed vectors equal the five frozen vectors in `plans/round-64-claims.md` lines
65-71. The receipt also records `PORTFREE before-battery True` (and `PORTFREE after <case>
True` for every case), the K1 `server_pid=3561122` with `pid_before_legs=True`, and
`K2-FRAGMENT Port 5328 is not listening - no real gRPC server is running` — the frozen
predicate's three clauses, all present. The second battery receipt's `VECTOR`/`PREDICATE`
lines are byte-identical to the first (`cmp` rc 0).

## The trio lines (the entry's opening, exactly as the seat spec words them)

```
source: S230 (TB2 kv-store-grpc grader at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6) — corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py; and S231 (gRPC Python API reference, grpc.RpcError) — https://grpc.github.io/grpc/python/grpc.html#grpc.RpcError
verified-at: 2026-11-03
recheck: sha256sum corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py  # 115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e
```

The drafted entry passes the lane's own trio gate:
`python3 plans/round63_gate_checks.py trio .ufo/waves/round-64/w1/KnowledgeDraft/tb2-kv-store-grpc-offline.md`
→ `TRIO pass`, rc 0.

## Behaviour the entry records

- **The seven legs and their PASS conditions**, read off the pinned grader capture
  (`sha256 115de2e9…` = `SHA256SUMS` line 80), with S230 line numbers for every assert.
- **The five frozen case vectors** (claims doc lines 65-71) with the two **pre-freeze controls'
  committed digests**: `k2-empty-capture.txt` `ae0a78ee…` (vector `F P F F F F F`),
  `k4-protoonly-capture.txt` `b262cfe5…` (vector `P P F F F F F`), K4 input bytes
  `control-k4-kv-store.proto` `c89bcb1c…`.
- **The K5-leg-6 vs K3-leg-6 asymmetry**, grounded in the grader's own `except` structure:
  `except grpc.RpcError:` (S230 :128) exists **only** in the handshake leg, so a transport
  failure (UNAVAILABLE, an `RpcError` per S231) is swallowed and leg 6 returns normally
  (K5 leg 6 = P) while leg 7, which has no such arm (:170-171), fails; a *semantic* failure is
  not an `RpcError`, so the wrong-math case lands in `except Exception` (:131-133) and leg 6
  fails too (K3 leg 6 = F). And `import kv_store_pb2` / `import kv_store_pb2_grpc` sit
  **outside** the `try` (:105-106, :144-145), so a missing module raises
  `ModuleNotFoundError` before any handler sees it (K2/K4 legs 6-7 = F).
- **The named `--check-receipt` limitation** (r63 routed defect 4): text fields only; the live
  evidence is `server_pid` + `server_log`, the sidecar `kvstore-probe.txt.server-log`
  (sha256 `f83e871e…`) carrying `case=K1 pid=3561122` / `SERVER UP 5328` /
  `case=K3 pid=3561190` / `SERVER UP 5328`. Named wherever the checker is cited, including in
  the SKILL registry row draft.
- **The pypi-server R63-C1 MISS of record is explicitly unchanged** — the round-63 entry, its
  receipt and its L0 question stand, and the `network-service` row keeps the round-63 pypi
  pointers.

## Findings for the L1 (reported, not edited)

1. **The flip is only landable after the probe script and the receipt are in the tree** — and
   it now is. The depth gate's pass condition is `resolved == total`
   (`plans/round63_gate_checks.py:333`), not merely `share >= 0.90`. Measured: the flipped row
   against the lane root was **red** at 16:26 (`paths total=26 resolved=24 share=0.92`,
   `DETAIL unresolved=corpus/evidence/round64/kvstore-probe.txt,plans/round64_c1_kvstore_probe.py`,
   `PREDICATE R63-C2 fail`, rc 1) while the two artifacts were absent, and **green** at 16:29
   against both a shadow root and the lane root after the L1 landed them at 16:28:35
   (`paths total=26 resolved=26 share=1.00`, `PREDICATE R63-C2 pass`, rc 0). A flip landing
   ahead of those files would trip C2's own kill rule. Land order for the L1: registry row +
   knowledge entry → decision-table flip.
2. **The census must not be touched.** The flip changes no class name and no count cell
   (`8` stays), so `plans/round63_gate_checks.py`'s `depth` still prices the table against the
   unchanged round-62 receipt `corpus/evidence/round62/class-survey.txt`
   (`EXECUTED-COVERAGE executed=17 … classes-uncovered=network-service,…`, line 21). Adding
   `kv-store-grpc` to `corpus/evidence/round52/graders/executed17.lst` would invalidate that
   committed receipt (sha256 `ee30c698…5613`) and is **not** proposed.
3. **Prose drift needs a dated repair.** `SKILL.md` line 62 says the executed column is
   derived from `executed17.lst`; after the flip that sentence no longer covers the
   `network-service` row (`kv-store-grpc` is not on that list — `grep -c` → 0, rc 1). Two
   prose-only repairs are drafted in `registry-drafts.md` §3c; the append-only dated note (i)
   is recommended. This seat did not edit the sentence.
4. **The two `python3 plans/round64_c1_kvstore_probe.py` mentions are coupled — measured.** The
   registry row and the knowledge entry both advertise that script, so
   `plans/round52_c2_registry.py`'s `MISSING` leg requires both to land together, and
   `ENTRY-MISSING` requires the script to be in the tree (it is — the L1 landed it at 16:28:35,
   sha256 `9f56d25d…`). Measured on a shadow lane root: **with** the drafted row the gate is
   green (`PREDICATE R52-C2 pass`, rc 0; `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`,
   `SELFTEST-UNBACKED 0`, `DUPLICATE 0`); **without** it, the entry alone drives the gate red
   (`MISSING 1`, `MISSING plans/round64_c1_kvstore_probe.py`, `PREDICATE R52-C2 fail`, rc 1).

## Out of scope (not done by this seat)

- The L1's admissions: `corpus/knowledge/tb2-kv-store-grpc-offline.md`, the `corpus/README.md`
  index row (row text drafted in `registry-drafts.md` §"L1 integration checklist"), the
  `corpus/SOURCES.md` rows S230/S231, the `PROVINCE.md` round-64 section, the `LOG.md`
  round-64 section, and the actual splices of the SKILL/SCORECARD texts.
- The predicate, the counter, the kill rules, the frozen vectors and the controls — read as
  frozen, changed by nobody.
- The pypi-server R63-C1 record and the open L0 question `kengaku | round-63`.
- No port was bound by this seat (5328 and 8080 were never listened on here); no git or jj
  mutation was run; no tool was installed (no install was needed for this seat's work, so
  nothing is recorded under the tooling directive).

## Tooling

No install, no upgrade, no network open by this seat. The tooling authorization was read
(`/home/vgpnk/.omp/agent/RULES.md`) and the pacman guard honoured by not running any pacman
transaction; nothing was required beyond the tools already present (`python3` 3.14.8, `grep`,
`sed`, `cmp`, `sha256sum`).

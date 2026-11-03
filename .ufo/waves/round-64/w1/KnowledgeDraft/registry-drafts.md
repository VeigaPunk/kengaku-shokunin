# Registry drafts — R64-C1 (round 64, wave 1, seat KnowledgeDraft)

Admission drafts only. The L1 admits. Nothing here edits a lane file; every draft below is
text to be spliced, with the splice target named. The frozen file
`plans/round-64-claims.md` (freeze commit `859ac24f41061bffde588b9ed5d5adfea5ca8e27`, base tip
`5f517fe7147831f96a9900c9642c07ee71031940`) is the only rule source; no predicate, counter,
kill rule, leg vector or control was changed by this seat.

---

## 1. SCORECARD capability row text

**Capability name (frozen, `plans/round-64-claims.md` lines 119-125):**
`offline-network-service-grader-probe` — the name R63-C1 reserved and never entered because
its predicate missed. It enters here for the first time; the round-63 record of that MISS is
unchanged.

**Primary form** — the house prose form used by rounds 61-63
(`**Capabilities** — new row: …`), for the round-64 SCORECARD section:

> **Capabilities** — new row: `offline-network-service-grader-probe` → runs a TB2 grader
> whose service dependency is a real gRPC server the lane builds (proto + protoc generation +
> server), against a frozen 5-case × 7-leg prediction table inside bwrap →
> `python3 plans/round64_c1_kvstore_probe.py --check-receipt corpus/evidence/round64/kvstore-probe.txt`
> → first working round 64 (the name was reserved by R63-C1 and never entered there because
> its predicate missed; that record of the miss stays unchanged).

**Alternative form** — if the L1 opens a `### Round-64 capabilities (demonstrated this round)`
table in the rounds-38…52 house style, the same content as one row:

> | `offline-network-service-grader-probe` | Execute a pinned TB2 grader whose service dependency is a real gRPC server the lane builds (proto + protoc generation + server), per case in bubblewrap with shared loopback, against a frozen 5-case × 7-leg prediction table | `python3 plans/round64_c1_kvstore_probe.py --check-receipt corpus/evidence/round64/kvstore-probe.txt` → `PREDICATE R64-C1 pass`, rc 0; the five observed vectors equal the five frozen ones | 64 |

**Landing note:** the capability row enters **only if the predicate passes** (claims doc line
119). The count row above it (the round-64 claim/axis table) is the L1's; this seat drafted
the capability row only.

---

## 2. SKILL registry row text

**Splice target:** the `## Gate/probe registry (PROTOCOL §Gate standard)` table in `SKILL.md`
(`plans/round63_gate_checks.py`'s `registry_block` reads exactly that heading), as the **last
row of the table** — the house rule is that registry rows are appended after the last
registry row, not sorted into it.

**Cell-by-cell draft** (8 columns: name | kind | entry | verdict map | self-test | pinned
values | write scope | owner):

| cell | draft text |
|---|---|
| name | `round64-c1-kvstore-probe` |
| kind | `probe` |
| entry | `python3 plans/round64_c1_kvstore_probe.py` (bare; flags implemented: `--lane --work --receipt --check-receipt --selftest --render-table` — the r58 KL-probe form: defaults `--lane .`, no receipt write, the system tempdir as scratch; the receipt of record `corpus/evidence/round64/kvstore-probe.txt` was produced with an explicit `--receipt`; `--check-receipt` re-derives the receipt's text fields and **cannot prove a live run** — the live evidence is `server_pid` + `server_log`, the sidecar written beside the receipt (named limitation, r63 routed defect 4); `--render-table` prints the frozen 5-case × 7-leg prediction table; `--selftest` runs the receipt battery) |
| verdict map | `0` pass (`PREDICATE R64-C1 pass`; the five observed vectors equal the five frozen ones) · `1` fail (`PREDICATE R64-C1 fail`; any observed vector differs from its frozen vector, or a required receipt field is missing — `K2 stderr_mentions_8080`-style text-field detection is text-only) · `2` usage or SETUP (`SETUP port-5328-occupied` — the battery refuses to grade through a foreign listener; `SETUP receipt-missing`; `SETUP lane-required`; `SETUP work-dir-required`) |
| self-test | `python3 plans/round64_c1_kvstore_probe.py --selftest --work <existing dir>` — seven fixtures (render-table, valid-receipt, tampered-vector, no-server-pid, port-not-free, no-k2-fragment, missing-receipt → exit 2); measured `SELFTEST pass`, rc 0 (receipt `.ufo/waves/round-64/w1/ProbeBuild/selftest.txt`, sha256 `de447c764328d20a7cc4fcd44dc973e82258b2f11a43dc48fc40f4b632e271b0e`) |
| pinned values | grader capture `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py` sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` (TB2 pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; `SHA256SUMS` line 80); receipt of record `corpus/evidence/round64/kvstore-probe.txt`; the frozen vectors in `plans/round-64-claims.md` lines 65-71; the two pre-freeze controls `corpus/evidence/round64/k2-empty-capture.txt` (sha256 `ae0a78ee657108a697fae965dc71e7d79f80cd9850d9ec00b2261ba2476f9887`) and `corpus/evidence/round64/k4-protoonly-capture.txt` (sha256 `b262cfe5791cfb93d115a021a8ed392b5a60c07c8f6426dfb8b5b1f9964e4bdb`), plus the K4 input bytes `corpus/evidence/round64/control-k4-kv-store.proto` (sha256 `c89bcb1c3b3da00b437a721d7f9d7b76bd778ca567ca1c077f21339fc8a50e0c`) |
| write scope | reads the lane read-only; writes only its `--work`/TMPDIR tree and the receipt path given; bwrap sandbox (`--ro-bind /usr /usr`, `--ro-bind /etc /etc`, `--proc /proc`, `--dev /dev`, `--tmpfs /tmp`, `/app` bind, `/venv` ro-bind, `/ctl/driver.py` ro-bind); network **shared** (the legs must reach `127.0.0.1:5328`); binds 5328 only while its own server runs and kills only the PIDs it started; the one named network open is PyPI (grpcio/grpcio-tools into the probe-owned venv) |
| owner | kengaku round 64 |

**Drafted as one table row** (for copy-paste; the pipe count must be exactly 8 cells):

```
| `round64-c1-kvstore-probe` | probe | `python3 plans/round64_c1_kvstore_probe.py` (bare; flags implemented: `--lane --work --receipt --check-receipt --selftest --render-table` — the r58 KL-probe form: defaults `--lane .`, no receipt write, the system tempdir as scratch; the receipt of record `corpus/evidence/round64/kvstore-probe.txt` was produced with an explicit `--receipt`; `--check-receipt` re-derives the receipt's text fields and cannot prove a live run — the live evidence is `server_pid` + `server_log`, the sidecar written beside the receipt (named limitation, r63 routed defect 4); `--render-table` prints the frozen 5-case × 7-leg prediction table; `--selftest` runs the receipt battery) | `0` pass (`PREDICATE R64-C1 pass`; the five observed vectors equal the five frozen ones) · `1` fail (`PREDICATE R64-C1 fail`; any observed vector differs from its frozen vector, or a required receipt field is missing) · `2` usage or SETUP (`SETUP port-5328-occupied` — the battery refuses to grade through a foreign listener; `SETUP receipt-missing`; `SETUP lane-required`; `SETUP work-dir-required`) | `python3 plans/round64_c1_kvstore_probe.py --selftest --work <existing dir>` — seven fixtures (render-table, valid-receipt, tampered-vector, no-server-pid, port-not-free, no-k2-fragment, missing-receipt → exit 2); measured `SELFTEST pass`, rc 0 (receipt `.ufo/waves/round-64/w1/ProbeBuild/selftest.txt`, sha256 `de447c764328d20a7cc4fcd44dc973e82258b2f11a43dc48fc40f4b632e271b0e`) | grader capture `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py` sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` (TB2 pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; `SHA256SUMS` line 80); receipt of record `corpus/evidence/round64/kvstore-probe.txt`; the frozen vectors in `plans/round-64-claims.md` lines 65-71; the two pre-freeze controls `corpus/evidence/round64/k2-empty-capture.txt` (sha256 `ae0a78ee657108a697fae965dc71e7d79f80cd9850d9ec00b2261ba2476f9887`) and `corpus/evidence/round64/k4-protoonly-capture.txt` (sha256 `b262cfe5791cfb93d115a021a8ed392b5a60c07c8f6426dfb8b5b1f9964e4bdb`), plus the K4 input bytes `corpus/evidence/round64/control-k4-kv-store.proto` (sha256 `c89bcb1c3b3da00b437a721d7f9d7b76bd778ca567ca1c077f21339fc8a50e0c`) | reads the lane read-only; writes only its `--work`/TMPDIR tree and the receipt path given; bwrap sandbox (`--ro-bind /usr /usr`, `--ro-bind /etc /etc`, `--proc /proc`, `--dev /dev`, `--tmpfs /tmp`, `/app` bind, `/venv` ro-bind, `/ctl/driver.py` ro-bind); network **shared** (the legs must reach `127.0.0.1:5328`); binds 5328 only while its own server runs and kills only the PIDs it started; the one named network open is PyPI (grpcio/grpcio-tools into the probe-owned venv) | kengaku round 64 |
```

**Landing constraints the L1 must honour (measured, see §5):**

1. `plans/round64_c1_kvstore_probe.py` must exist in the tree **before** this row lands —
   `plans/round52_c2_registry.py` prices `ENTRY-MISSING = registry rows whose entry script is
   not in the tree → 0`. **Status at drafting:** the L1 landed the instrument at
   `plans/round64_c1_kvstore_probe.py` (sha256
   `9f56d25ddb33e14474c6439c16f25dd5545da99e542a051d342113a88b306843`, byte-identical to the
   ProbeBuild wave copy — `cmp` rc 0) and the receipt at
   `corpus/evidence/round64/kvstore-probe.txt` (sha256 `a87cd119…`, also `cmp` rc 0) at
   16:28:35, i.e. during this seat's wave. Both prerequisites are therefore already met; this
   row can land now.
2. The row's self-test cell names `--selftest`, which the instrument implements (argparse
   `add_argument("--selftest")`) — `SELFTEST-UNBACKED = 0` holds. Do not rename the flag.
3. The row advertises `python3 plans/round64_c1_kvstore_probe.py`, and so does the new
   knowledge entry; `plans/round52_c2_registry.py`'s `MISSING` leg therefore requires this
   row to land in the same commit as the entry. **Measured** on a shadow lane root: with the
   drafted row, `PREDICATE R52-C2 pass` (rc 0, `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`,
   `SELFTEST-UNBACKED 0`, `DUPLICATE 0`); with the row removed and the entry kept,
   `MISSING 1` / `MISSING plans/round64_c1_kvstore_probe.py`, `PREDICATE R52-C2 fail`, rc 1.

---

## 3. SKILL decision-table flip — the `network-service` row

**Splice target:** `SKILL.md`, the row
`| network-service | 8 | recipe-unexecuted | … | … |` inside the section
`## Decision table — grader class → offline replay recipe` (line 78 at the freeze tip).

**The flip is two cells of one row.** The `recipe-unexecuted` marker lives in the
**executed-status column** (claims doc line 127: "the SKILL decision table's `network-service`
row flips its executed-status cell"), and the same row's **recipe column** still ends with
"so the class is not counted replayed" — a sentence that becomes false at the flip. Both are
flipped together; the count cell stays `8` (claims doc line 127: "counts are untouched") and
the receipt-pointer cell keeps the round-63 pypi-server pointers so that MISS of record stays
cited.

### 3a. The one-line executed-status cell flip

| | cell text |
|---|---|
| before | `recipe-unexecuted` |
| **after** | `executed (kv-store-grpc, r64)` |

One line. The parenthetical names the member and the round so the cell is self-describing
without relying on `executed17.lst` (see the finding in §5, item 3).

### 3b. The row after the flip (whole row, for the L1 to splice)

```
| network-service | 8 | executed (kv-store-grpc, r64) | a lane-built gRPC server (proto + grpcio-tools generation + `server.py` on 127.0.0.1:5328) inside bubblewrap with shared loopback, the server PID and its start log recorded, against a frozen 5-case × 7-leg prediction table; the round-64 probe met its frozen predicate (`PREDICATE R64-C1 pass`), so the class is now counted replayed through this member; the round-63 `pypi-server` replay remains a MISS of record (its frozen stderr clause was missed) and is unchanged. | `corpus/evidence/round64/kvstore-probe.txt`, `plans/round64_c1_kvstore_probe.py`, `corpus/evidence/round63/pypi-probe-run1-literal-detector-fail.txt`, `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` |
```

### 3c. The SKILL prose that describes the executed column

`SKILL.md` line 62 currently reads: *"the executed column is derived from
`corpus/evidence/round52/graders/executed17.lst` (a class is `executed` when at least one of
its members is on that list)"*. After the flip that sentence no longer explains the
`network-service` cell, because `kv-store-grpc` is **not** on `executed17.lst` (that list is a
frozen round-52 census input; `grep -c kv-store-grpc
corpus/evidence/round52/graders/executed17.lst` → 0, rc 1). This seat did **not** edit the
sentence — the executed list and the census receipt are the L1's. Two candidate repairs, for
the L1 to choose (both are prose-only, neither touches the census receipt or the depth
gate):

- **(i) dated note appended to the same paragraph** (append-only; leaves the round-52
  derivation sentence standing as history):
  > Round 64: the executed column also admits a member executed under a **later** frozen
  > predicate — `kv-store-grpc` (round 64, receipt
  > `corpus/evidence/round64/kvstore-probe.txt`); `executed17.lst` remains the round-52
  > census input and is unchanged.
- **(ii) leave line 62 as it is** and rely on the self-describing cell text
  `executed (kv-store-grpc, r64)`. Cheapest, but the derivation sentence then reads as a
  claim that no longer covers the one row that differs.

I recommend **(i)**: it is append-only, dated, and it keeps the prose true without editing a
frozen round-52 input.

---

## 4. The dated LOG line for the flip

**Splice target:** `LOG.md`, inside the round-64 section the L1 opens (LOG.md currently ends
with the round-63 section, line 2480). House form: `## Round 64 (<date>) — …` with `- `
bullets underneath.

**Draft LOG line (one dated bullet):**

```
- 2026-11-03 (round 64, R64-C1): the SKILL decision table's `network-service` row flips its executed-status cell from `recipe-unexecuted` to `executed (kv-store-grpc, r64)` on the R64-C1 predicate's pass — the class's first met frozen predicate (receipt of record `corpus/evidence/round64/kvstore-probe.txt`, `PREDICATE R64-C1 pass`, rc 0; the five observed vectors equal the five frozen ones); the round-63 `pypi-server` replay stays a MISS of record and its pointers stay cited in the same row, unchanged.
```

**Optional second bullet** (only if the L1 wants the prose repair of §3c logged separately):

```
- 2026-11-03 (round 64): `SKILL.md`'s decision-table prose gains a dated note that the executed column also admits a member executed under a later frozen predicate (`kv-store-grpc`, round 64); `executed17.lst` stays the round-52 census input, unchanged, and the round-62 census receipt is not re-derived.
```

---

## 5. What this seat measured (every observed value with its command)

All commands read-only on lane files; the flip was tested on **scratch copies**, never on a
lane file.

| observation | command |
|---|---|
| The drafted knowledge entry passes the trio gate | `python3 plans/round63_gate_checks.py trio .ufo/waves/round-64/w1/KnowledgeDraft/tb2-kv-store-grpc-offline.md` → `TRIO pass`, rc 0 |
| The frozen vectors hold in the wave receipt | `grep -E '^(VECTOR\|PREDICATE)' .ufo/waves/round-64/w1/ProbeBuild/kvstore-probe.txt` → the five `VECTOR` lines above `PREDICATE R64-C1 pass` |
| The two battery receipts agree on vectors and predicate | `grep -E '^(VECTOR\|PREDICATE)'` on `kvstore-probe.txt` and `kvstore-probe-rerun.txt`, then `cmp` → rc 0 (identical) |
| The grader capture is the pinned bytes | `sha256sum corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py` → `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` = `SHA256SUMS` line 80 |
| The control receipts are the committed digests the claims doc names | `sha256sum corpus/evidence/round64/{k2-empty-capture.txt,k4-protoonly-capture.txt,control-k4-kv-store.proto}` → `ae0a78ee…`, `b262cfe5…`, `c89bcb1c…` |
| `kv-store-grpc` is a `network-service` member and was NOT executed at base | `grep -n 'CLASS network-service' corpus/evidence/round62/class-survey.txt` → line 11, `count=8`, member list contains `kv-store-grpc`; `grep -c kv-store-grpc corpus/evidence/round52/graders/executed17.lst` → 0, rc 1 |
| **The flip was depth-gate RED while the two new paths were absent** (measured 16:26, before the L1's 16:28 landing) | `python3 plans/round63_gate_checks.py depth --skill <scratch copy with the flip applied> --receipt corpus/evidence/round62/class-survey.txt --root .` → `ROWS n=16 class_match=True count_mismatch=0 paths total=26 resolved=24 share=0.92`, `DETAIL unresolved=corpus/evidence/round64/kvstore-probe.txt,plans/round64_c1_kvstore_probe.py`, `PREDICATE R63-C2 fail`, rc 1 |
| **The flip is depth-gate GREEN once both artifacts are in the tree** | same command with `--root <shadow root containing corpus/evidence/round64/kvstore-probe.txt and plans/round64_c1_kvstore_probe.py>` → `ROWS n=16 class_match=True count_mismatch=0 paths total=26 resolved=26 share=1.00`, `PREDICATE R63-C2 pass`, rc 0 — and re-measured against the LANE root after the L1's 16:28:35 landing: the same green line, rc 0 |
| The depth gate demands **every** path token in the section to resolve (not merely ≥0.90) | `plans/round63_gate_checks.py` `depth_measure`: the pass condition includes `resolved == total` (line 333) alongside `share >= 0.90`; the share-0.92 case above still failed |
| The L1 landed the instrument + receipt during this wave, byte-identical to the wave copies | `sha256sum plans/round64_c1_kvstore_probe.py corpus/evidence/round64/kvstore-probe.txt` → `9f56d25d…`, `a87cd119…`; `cmp` against `.ufo/waves/round-64/w1/ProbeBuild/` → rc 0 for both |
| **The drafted registry row + the drafted entry pass the lane's registry gate** | `python3 plans/round52_c2_registry.py --lane <shadow lane root: SKILL.md copy with the drafted row spliced, the drafted entry at corpus/knowledge/tb2-kv-store-grpc-offline.md, everything else symlinked>` → `ADVERTISED total=94`, `REGISTERED total=94 rows=96`, `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R52-C2 pass`, rc 0 |
| **Counterfactual: the entry alone (no registry row) makes that gate RED** | same command on the same shadow with the drafted row removed → `MISSING 1`, `MISSING plans/round64_c1_kvstore_probe.py`, `PREDICATE R52-C2 fail`, rc 1 — the entry and the row must land together |

### Findings for the L1 (reported, not edited)

1. **Ordering (now satisfied; recorded because it is a live trap).** The `network-service`
   flip is only landable **after** `corpus/evidence/round64/kvstore-probe.txt` and
   `plans/round64_c1_kvstore_probe.py` are in the tree. The depth gate's pass condition is
   `resolved == total`, so a flip landing ahead of those two files makes the r63 depth gate
   **red** (`PREDICATE R63-C2 fail`, rc 1, `share=0.92`) even though the class/count match is
   untouched — exactly the kill rule the claims doc attaches to C2 ("the real section
   regressing … the repair is defective"). **Measured both ways**: red at 16:26 (paths
   absent), green at 16:29 against the lane root and against a shadow root (paths present,
   `share=1.00`, rc 0). The L1 landed both artifacts at 16:28:35, so the flip is green **now**.
   Remaining land order for the L1: registry row + knowledge entry → decision-table flip (the
   flip may still land last, but it is no longer blocked).
2. **The census is untouched by this flip.** `plans/round63_gate_checks.py`'s `depth` prices
   the decision table against `corpus/evidence/round62/class-survey.txt` (class names and
   counts only). The `network-service` row's count cell stays `8`, the census receipt is not
   re-derived, and `EXECUTED-COVERAGE executed=17 … classes-uncovered=network-service,…`
   (class-survey.txt line 21) still stands as the round-62 record. **Do not** add
   `kv-store-grpc` to `corpus/evidence/round52/graders/executed17.lst`: that is a frozen
   round-52 census input, and editing it would invalidate the round-62 census receipt
   (sha256 `ee30c698…5613`) that the depth gate and the registry both cite.
3. **Prose drift (needs the L1's dated repair).** `SKILL.md` line 62 says the executed column
   is derived from `executed17.lst`; after the flip that sentence does not cover the
   `network-service` row. §3c gives two prose-only repairs; (i) is recommended.
4. **The pypi-server MISS is unaffected.** `corpus/knowledge/tb2-network-service-offline-grader.md`
   and `corpus/evidence/round63/pypi-probe-run1-literal-detector-fail.txt` are untouched by
   every draft here; the L0 question `kengaku | round-63` stays open.

### L1 integration checklist (not part of the three deliverables)

- `corpus/knowledge/tb2-kv-store-grpc-offline.md` — the entry drafted here
  (`.ufo/waves/round-64/w1/KnowledgeDraft/tb2-kv-store-grpc-offline.md`).
- `corpus/README.md` — a knowledge-index row for the new entry (QUALITY Q7: entry file, index
  row and coverage-map row land together). Suggested row text:
  > | `knowledge/tb2-kv-store-grpc-offline.md` | The corpus's second offline replay of a network-service TB2 grader (`kv-store-grpc`, S230; the gRPC Python API reference, S231): `plans/round64_c1_kvstore_probe.py` runs the grader's own seven legs in bwrap against a lane-built gRPC server on 127.0.0.1:5328, over a frozen 5-case × 7-leg prediction table. The five observed vectors equal the five frozen ones (`PREDICATE R64-C1 pass`); the handshake leg's tolerance of `grpc.RpcError` versus its failure on wrong math is read off the grader's own `except` structure. The `--check-receipt` limitation is named (text fields only; live evidence is `server_pid` + `server_log`). The round-63 `pypi-server` MISS of record is unchanged. |
- `PROVINCE.md` — the round-64 section (the L1's).
- `corpus/SOURCES.md` — the S230 and S231 rows (the L1's; the claims doc says the L1 writes
  them only after GraderRecon and SourceReview both opened them live).

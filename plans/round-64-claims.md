# Round 64 — frozen claims (kengaku, 2026-11-03)

Base tip `5f517fe7147831f96a9900c9642c07ee71031940` (`refs/heads/master` == `origin/master` at
round start, per `jj-lane.sh state` local=remote=ahead=0). This document is written and committed
BEFORE any scored run. Predicates, counters, kill rules and controls below are fixed; a seat may
not change them. A rule changed after any scored receipt is not this claim's rule (kumitate r42).
Any later amendment is a new dated section, never an edit.

Round shape: one v1 wave, 14 seats (`.ufo/waves/round-64/w1-spec.json`), build + attack.

Host note (run-15 addendum: host differences are re-measured, never re-declared): this round runs
on the Linux/omp host (Arch, python 3.14.8, bwrap 0.13.1, uv 0.13.0, host `requests` 2.34.2;
`vim` and `nginx` ABSENT — both probed before grader selection, which is why the gRPC candidate
was chosen over headless-terminal/nginx-request-logging). The r56–r63 "canonical WSL environment"
does not exist here; every counter this round declares is re-derived on this host from committed
bytes.

## Declared claims (3), distinct axes

| claim | axis / capability | before → after | score effect |
|---|---|---|---|
| R64-C1 | coverage (lowest non-retired axis, L0-capped at 7) — capability acquisition `offline-network-service-grader-probe` | TB2 class `network-service`: 0 members executed (`CLASS network-service count=8`, executed=0; `grep -c kv-store-grpc corpus/evidence/round52/graders/executed17.lst` → 0, rc 1) → `kv-store-grpc` executed offline under this frozen predicate | score held at 7 (L0 cap `kengaku \| round-25/33/51`, still open — nothing assumed answered) |
| R64-C2 | operability (held at ceiling 10, exercised) — routed defect 3 (`corpus/lessons/round-63-verifier-spotcheck.md` §5.3): the depth gate resolves path tokens outside the lane root | red-before: the committed gate passes a fixture whose receipt-pointer token is an absolute out-of-root path (`escape-before.txt`: share 1.00, `PREDICATE R63-C2 pass`, rc 0, token `/home/vgpnk/.config/uv/uv-receipt.json`, `inside_root=False`) → after: absolute/`..`/escaping tokens are a named finding (`escape=`), fail the gate, and the real SKILL section still passes | operability held at 10 |
| R64-C3 | freshness (held at ceiling 10, exercised) — routed defects 1+2: lesson-index parity and the lane-wide provenance-trio drift | red-before: 29 knowledge entries fail the round-63 trio gate (frozen list `trio-red-at-base.txt`); `lessons/round-{57..62}.md` have 0 README index rows each → after: 0 trio-red (dated round-64 addenda), 1 README row each for round-57..62 | freshness held at 10 |

Causal separation: C1 artifacts = the probe, its receipt, the knowledge entry, the capability row,
S230/S231. C2 artifacts = the `plans/round63_gate_checks.py` `_resolves` patch, the escape
fixtures, and its receipts. C3 artifacts = `plans/round64_trio_sweep.py`, the addenda blocks, and
the README index rows. C2 and C3 share no artifact and no file (the sweep is a new tool, not a
gate edit); C1 shares nothing with either. All three share only this claims doc.

Round-63 routed defects addressed here, by the non-author closure's numbering: 1 → C3(b);
2 → C3(a); 3 → C2; 4 → named limitation below and in the round report; 5 → carried (L0
`kengaku | round-63` still open; R63-C1 stays MISS; run 1 is never re-scored); 6 → the
network-service recipe cell may flip to executed ONLY on a C1 pass, dated, with the pypi-server
record unchanged.

---

## R64-C1 — offline execution of the `kv-store-grpc` grader

**Grader under execution:** `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py`,
sha256 `115de2e964bbe689d07930527113422ef8a9e4be4eb958ad84594e3fcd2b1b0e` (=
`corpus/evidence/round52/graders/SHA256SUMS` line 80). Seven test functions, graded in file order:
proto file creation, grpc tools installation, protobuf generation, server file creation, real
server running (TCP 127.0.0.1:5328), gRPC protocol handshake, server functionality (SetVal/GetVal
echo and overwrite). The candidate is lane-authored: `kv-store.proto` + generated
`kv_store_pb2.py`/`kv_store_pb2_grpc.py` (grpcio-tools in a probe-owned venv) + `server.py`
(`class Server`) + a running server on 5328.

**Probe:** `plans/round64_c1_kvstore_probe.py` (built in the wave). House sandbox shape (r37/r63):
bwrap `--ro-bind /usr /usr` + `--symlink` for `/bin`,`/sbin`,`/lib`,`/lib64` + `--dir` mount
points; network SHARED (no `--unshare-net`: the loopback service must be reachable; r63
precedent), so port 5328 is a host-visible loopback port: the probe checks it is FREE
(`ss -ltn`) before the battery and refuses (exit 2, `SETUP port-5328-occupied`) rather than
grading through a foreign listener; only the probe's seat binds 5328, and it kills only PIDs it
started and recorded. The grader's python is the probe-owned venv (grpcio + grpcio-tools installed
from PyPI — the one named network open of the seat).

**Leg rule:** P iff the test function returns normally; F on any exception. Legs run in file
order in one sandbox process per case.

**Frozen leg vectors (cases × legs 1–7):**

| case | setup | frozen vector |
|---|---|---|
| K1 | compliant: proto + generated pb2 + `server.py` (echo semantics) + server running on 5328 | `P P P P P P P` |
| K2 | do-nothing control (L1-measured pre-freeze): empty `/app`, no server | `F P F F F F F` |
| K3 | wrong-math: server stores `value+1` on SetVal | `P P P P P F F` |
| K4 | proto-only control (L1-measured pre-freeze): only `kv-store.proto` present | `P P F F F F F` |
| K5 | files-complete, server never started | `P P P P F P F` |

Leg-2 (`import grpc`) is P for every case by probe-environment construction (the venv carries
grpcio); that is part of the frozen vector, not an accident. K5 leg-6 is the frozen prediction
that the handshake leg tolerates `grpc.RpcError` (UNAVAILABLE is one) while leg-7 does not —
grounded in the grader's own except structure and the K2/K4 captures, which show the
non-RpcError paths (ModuleNotFoundError) are NOT tolerated.

**Q45 captures (before the freeze).** The predicate names exactly one grader-printed string
fragment; it was captured before this freeze, in the K2 control:
`Port 5328 is not listening - no real gRPC server is running` (leg-5 AssertionError message).
Control receipts (committed this freeze):
- `corpus/evidence/round64/k2-empty-capture.txt` — sha256
  `ae0a78ee657108a697fae965dc71e7d79f80cd9850d9ec00b2261ba2476f9887`; LEGS vector
  `F P F F F F F`; per-leg classes as printed in the file.
- `corpus/evidence/round64/k4-protoonly-capture.txt` — sha256
  `b262cfe5791cfb93d115a021a8ed392b5a60c07c8f6426dfb8b5b1f9964e4bdb`; LEGS vector
  `P P F F F F F`.
- `corpus/evidence/round64/control-k4-kv-store.proto` — sha256
  `c89bcb1c3b3da00b437a721d7f9d7b76bd778ca567ca1c077f21339fc8a50e0c` (the K4 input bytes).

**Predicate R64-C1 (one sentence, the same in this plan, the probe's check and the receipt):**
pass iff, in the receipt of record, the observed 7-leg vector for each case K1–K5 equals the
frozen vector above, AND the K2 receipt records the captured leg-5 failure fragment
`Port 5328 is not listening`, AND the receipt records that port 5328 was free at battery start
and that the K1 server PID was recorded by the probe before the handshake leg ran.

**Counting command (re-derivable from committed bytes):**
`python3 plans/round64_c1_kvstore_probe.py --check-receipt corpus/evidence/round64/kvstore-probe.txt; echo $?`
→ last line `PREDICATE R64-C1 pass`, exit 0.

**Named limitation (r63 routed defect 4, carried):** `--check-receipt` re-derives text fields
only and cannot prove a live run. The live evidence is the server-side log the probe captures
from the process it started (receipt field `server_log` + `server_pid`), copied into the wave
evidence dir beside the receipt. The limitation is named wherever the checker is cited.

**Kill rules:**
- K2 leg-5 returns P (something listening) → the counter or the port discipline is wrong; the
  battery must have refused (exit 2). If it graded through a foreign listener, the claim is dead
  and the round reports it. Not patched, not re-frozen.
- K1 legs 1–4 any F → the candidate or the probe is wrong; the claim is a miss (honest stop).
- Any observed vector differing from the frozen vector → MISS as declared; no re-freeze in this
  round; the miss and its evidence are reported (r59 precedent).

**Do-nothing control status:** K2 and K4 are the controls and were measured BEFORE this freeze
(receipts above). The claim's counter is not already met by a control: K2 is not K1 (its vector
differs in 6 of 7 legs), so a do-nothing run cannot pass the frozen predicate.

**Capability row (enters only if the predicate passes):**
`offline-network-service-grader-probe` → runs a TB2 grader whose service dependency is a real
gRPC server the lane builds (proto + protoc generation + server), against a frozen 5-case × 7-leg
prediction table inside bwrap → `python3 plans/round64_c1_kvstore_probe.py --check-receipt
corpus/evidence/round64/kvstore-probe.txt` → first working round 64. (The name was reserved by
R63-C1 and never entered there because its predicate missed; the record of that miss stays
unchanged.)

**On a pass:** the SKILL decision table's `network-service` row flips its executed-status cell
(dated note in LOG; the r63 depth gate re-run must stay green — counts are untouched); the
knowledge entry `corpus/knowledge/tb2-kv-store-grpc-offline.md` is admitted; the class recipe
cell's `recipe-unexecuted` marker is superseded by the executed pointer for this member, with the
pypi-server R63-C1 MISS of record explicitly unchanged.

---

## R64-C2 — operability: the depth gate resolves path tokens outside the lane root (routed defect 3)

**Defect of record (SecurityScan L-1, `corpus/lessons/round-63-verifier-spotcheck.md` §5.3;
evidence receipt `.ufo/waves/round-63/w1/attack/security.md` §L-1):**
`plans/round63_gate_checks.py:192` computes `(root / token).exists()`; an absolute token
replaces `root`, and `..` segments are not rejected, so a receipt pointer to any host path
counts as resolved and inflates the ≥0.90 share the R63-C2 predicate prices.

**Red-before (measured at the freeze tip, committed):** `corpus/evidence/round64/escape-before.txt`
— a synthetic 16-row fixture (committed driver `wave evidence`) with receipt-pointer token
`/home/vgpnk/.config/uv/uv-receipt.json` (outside the lane root, a real host file):
`ROWS n=16 class_match=True count_mismatch=0 paths total=2 resolved=2 share=1.00`,
`PREDICATE R63-C2 pass`, rc 0. The gate passes an out-of-root pointer today.

**Repair (the only permitted delta):** in `_resolves()`, a token is resolved only if it is
relative, contains no `..` segment, and `os.path.normpath(root/token)` stays inside `root`
(`is_relative_to`). The depth command additionally prints `DETAIL escape=<token list>` (finding
id `ESCAPE`) for absolute/`..`/escaping tokens and FAILS the predicate when the escape set is
nonempty, even if the share clause alone would pass. No other gate behaviour changes.

**Predicate R64-C2:** pass iff (a) the escape fixture under the PATCHED gate fails with
`DETAIL escape=` present and rc 1, (b) the committed selftest exits 0 with FOUR cases — GOOD
(must pass), BAD-COUNT (must fail), NO-SECTION (must fail), BAD-ESCAPE (must fail) — each
asserting its expected verdict and a stable finding id, and (c) the real SKILL decision-table
section still passes unchanged (`ROWS n=16 class_match=True count_mismatch=0`, escape set empty,
rc 0).

**Counting commands:**
- `python3 plans/round63_gate_checks.py --selftest --work <scratch>; echo $?` → exit 0, 4/4 cases.
- `python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .; echo $?` → `PREDICATE R63-C2 pass`, rc 0 (no regression).
- The escape fixture re-run under the patched gate → rc 1 with `DETAIL escape=` (committed receipt).

**Kill rules:** the real section regressing (any of n/class_match/count_mismatch/escape changing)
→ the repair is defective, the claim is dead (honest stop, reverted as a new dated change, never
silently). A selftest case asserting the wrong expectation → fail.

**Verdict rule:** operability held at ceiling 10 either way; the claim admits on the predicate,
it does not move the score (r58-C1/r60-C2 precedent).

---

## R64-C3 — freshness: provenance-trio sweep + lesson-index parity (routed defects 1+2)

**Defect of record:** 29 knowledge entries fail the round-63 trio gate at base (frozen list
`corpus/evidence/round64/trio-red-at-base.txt`, produced by running
`python3 plans/round63_gate_checks.py trio <file>` over every `corpus/knowledge/*.md` at base —
note: the r62 spotcheck's "27/64 lack verified-at" undercounts this gate-based population; two
entries carry `verified-at` but fail the gate's first-12-lines/before-first-heading/order rule).
Six lesson files `lessons/round-{57..62}.md` have no README index row (round-53..56 rows already
exist; the routed defect's "53–62" range was stale on arrival — the before-receipt is the record).

**Instrument:** `plans/round64_trio_sweep.py` (new file; built in the wave). Walks
`corpus/knowledge/*.md` and classifies each entry TRIO-OPEN (opens with `source:`, `verified-at:`,
`recheck:` in order within the first 12 lines before the first `## ` heading — the same rule the
round-63 gate implements) / TRIO-ADDENDUM (opening predates the rule; the file carries a dated
`## Freshness addendum (round 64)` block containing `verified-at: 2026-11-03` and a `recheck:`
line naming the re-verification command) / TRIO-RED (neither). Prints
`SWEEP files=<n> trio_open=<a> addendum=<b> red=<c>` and `PREDICATE R64-C3 pass|fail`. It
cross-checks its red set against the frozen list and exits 2 (SETUP) on any mismatch. Selftest
fixtures: RED, ADDENDUM, OPEN (each must classify as named). The addendum block is APPEND-ONLY
(r10 errata precedent: an appendix-only dated change; no earlier byte is edited) — this is the
freshness sweep's declared form, frozen here so the closure judges the declared rule, not a
post-hoc one.

**Re-verification (the addenda's substance):** for every entry on the frozen list, a
re-verification command is run THIS ROUND against committed bytes — own-work/pinned-capture
entries re-hash their pinned artifact or re-run their pinned tool's `--selftest`/`--summary`;
externally-cited entries re-verify against the committed capture bytes (sha256). The addendum
names the command and the observed one-line result. No bulk network re-fetch is required; an
entry whose source cannot be re-verified from committed bytes keeps its red status (and the
claim fails — honest stop), it is never marked green by prose.

**Predicate R64-C3:** pass iff (a) the sweep's after-receipt at the round tip prints
`red=0` with every previously-red entry carrying a dated round-64 freshness addendum naming its
re-verification command and observed result, (b) the sweep's red set at base equaled the frozen
29-entry list (SETUP cross-check in the red-before receipt), and (c) for N in 57..62,
`grep -c "lessons/round-$N.md" corpus/README.md` → 1 (before: 0 each, receipt
`claims/before-state.txt`).

**Counting commands:**
- `python3 plans/round64_trio_sweep.py --sweep --lane . ; echo $?` → `PREDICATE R64-C3 pass`, exit 0.
- `for n in 57 58 59 60 61 62; do grep -c "lessons/round-$n.md" corpus/README.md; done` → six `1`s.

**Kill rules:** any entry left red, or any addendum whose named command does not re-derive when
the closure runs it → fail, honest stop. An entry "repaired" by editing its opening bytes instead
of appending → the claim is dead (the declared rule is violated).

**Verdict rule:** freshness held at ceiling 10 either way; the claim admits on the predicate.

---

## Frontier step (CORPUS.md rule 1 / §2b) — sources

- **S230** (candidate) — TB2 `kv-store-grpc` grader at pin
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, raw.githubusercontent.com
  `.../kv-store-grpc/tests/test_outputs.py`; tier A (code; scope: the grader's seven-leg
  contract). Opened live by the scout; sha must equal the pinned sha above.
- **S231** (candidate) — gRPC Python API reference on `grpc.RpcError` and status codes
  (grpc.github.io/grpc/python/grpc.html#grpc.RpcError); tier A (docs; scope: the exception type
  the handshake leg tolerates). Opened live by the scout; the row is written only after the
  opening, with a ≤25-word located quote in the round lesson's `## Gate`.

C1 is the round's sourced claim (rests on S230, with S231 grounding the K5 leg-6 prediction).

## Amendment discipline

Anything the wave exposes that this freeze did not anticipate lands as a dated amendment section
here, never as an edit to the sentences above. A rule changed after any seat has scored is not
the claim's rule.

# Round 68 — declared claims (frozen before the receipt of record and before the wave)

Lane: kengaku (novelty + calibration; LLM and model research and evaluation; hyaku run 15, attempt 1).
Lane-root base for every path here and in the round report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Base: `master` tip `d2ed4ca3` at round start (`git rev-parse master` → `d2ed4ca32c9eb8e8a0f8b3c7ced3ff15c53f9821`,
`jj-lane.sh state` → `local=d2ed4ca… remote=d2ed4ca… ahead=0 behind=0`; the tip carries the round-67
non-author spot-check `corpus/lessons/round-67-verifier-spotcheck.md` as its only delta over the round-67
landing `f600c6d3`).

This document is written and committed BEFORE any scored run of round 68. Predicates, counters, kill
rules, the frozen case table and the controls below are fixed; a seat may not change them. A rule
changed after any seat has scored is not this claim's rule (kumitate r42). Any later amendment is a
new dated section, never an edit.

Dev build check, disclosed (not data for any claim): before the freeze, the probe and the gate were
run once each in scratch (`/fast/scratch/hyaku/kengaku-r68/dev`) to catch build defects; their outputs
are discarded, and the scored run below is the receipt of record.

Round shape: ONE v1 wave, 12 seats (`.ufo/waves/round-68/w1-spec.json`), build + attack, validated
under `scripts/hyaku/ufo-wave-policy.json` (band 8–16). Attack seats: reviewer, critic,
mutation-tester, sentinel, revenger, scout (6 of 12 = 50 %). One connector seat. No labrat seat: the
validator rejects the role ("labrat is not a swarm role", L0 `kengaku | round-67` line 281, still
open — nothing assumed answered); the falsifiable-hypothesis work rides the revenger and scout items.

Environment (host state measured at the freeze, no install this round): Python 3.14.8
(`/usr/bin/python3`), bubblewrap 0.13.1 (`/usr/bin/bwrap`), uv 0.13.0 present, port 8080 has no
listener (`ss -ltn | grep -c 8080` → 0). The round-63 probe builds its own venv in the work dir; no
new host package is needed. pacman stays paused (host-recovery L0); nothing to install.

Scratch root (§7): `/fast/scratch/hyaku/kengaku-r68/<seat-name>/`; every work dir, clone and fixture
lives there; `/tmp` only for files under 50 MB; seats delete their scratch before yielding.

---

## Declared claims (2), distinct axes

| claim | axis / capability | before → after | score effect |
|---|---|---|---|
| R68-C1 | coverage (lowest non-retired axis, L0-capped at 7) — capability `offline-network-service-grader-probe` completes its registration | TB2 class `network-service`: `executed 1 of 8` (SKILL.md:78 at base; `pypi-server` stays recipe-unexecuted per the round-63 MISS of record) → `executed 2 of 8` with `pypi-server` counted replayed | score held at 7 (L0 cap `kengaku \| round-25/33/51`, still open) |
| R68-C2 | calibration (held at ceiling 10, exercised) — the round-67 non-author closure's five routed defects land as dated corrections with re-deriving receipts | each defect's counting anchor 0 → 1 (erratum sections, committed selftest tally, registry rows, before-value correction) | score held at 10 |

Causal separation: C1's artifacts are the new probe, its fresh receipt of record, the per-case stderr
captures, the server log, the knowledge-entry addendum, the SKILL class-row flip and S240. C2's
artifacts are the dated errata (`plans/round-67-claims.md`, `corpus/evidence/round67/pipe/a1-mutants.txt`),
the committed round-67 selftest tally, the SKILL registry rows and the correction gate. They share no
artifact except this claims doc.

Why C1 is not the round-63 amendment retro-admitted: L0 `kengaku | round-63` (line 259) asks whether
the round-63 amended K2 detector may be admitted — it is UNANSWERED and stays open. This claim does
not answer it and does not re-score run 1: the round-63 receipt of record
(`corpus/evidence/round63/pypi-probe-run1-literal-detector-fail.txt`, `PREDICATE R63-C1 fail`) stays
the verdict of record for R63-C1. R68-C1 is a NEW frozen predicate (Q25/round-60 re-freeze pattern:
R60-C1 completed the sixteenth grader's admission the same way), frozen before the fresh battery run
below, with its own receipt of record.

---

## R68-C1 — coverage (L0-capped at 7): the corrected stderr re-freeze completes the `pypi-server` offline replay

**Grader under execution (unchanged from round 63):**
`corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py`, sha256
`82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` (= `corpus/evidence/round52/graders/SHA256SUMS`
line 134), pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`. Its `test_api()` calls `install()`, which
runs `python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0`, then imports
`vectorops` and asserts four `dotproduct` values.

**Instrument:** `plans/round68_c1_pypi_finish.py` (built in the wave per this spec; its own sha256 is
the receipt's `PROBE` line). It imports the committed round-63 probe
`plans/round63_c1_pypi_probe.py` (sha256 `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929`,
byte-verified at run time — the `BASE-PROBE` binding) and reuses its machinery (`CASES`, `predict_legs`,
`build_case_index`, `run_leg`, `pip_install_stderr`, `start_server`, `stop_server`, `served_paths`,
`require_port_free`, `materialize_grader`, `ensure_venv`, `make_stub`, `write_hosts`, `uninstall`) —
one implementation of the sandbox/index/leg logic, not a copy. The grader itself is never copied or
rewritten; it is materialized byte-verified and bound read-only at `/tests/test_outputs.py` inside
bwrap, exactly as round 63 ran it.

**Cases (frozen; identical to the round-63 frozen cases, re-frozen here verbatim):**

| case | setup | expected `test_api` leg |
|---|---|---|
| K1 compliant | index on 127.0.0.1:8080 serves `vectorops-0.1.0` with a correct `dotproduct` | **P** |
| K2 do-nothing control | nothing listening on 8080; no index | **F** |
| K3 wrong math | index serves `vectorops-0.1.0` whose `dotproduct` returns `sum(a*b)+1` | **F** (AssertionError) |
| K4 wrong version | index serves only `vectorops-0.2.0` | **F** (`CalledProcessError` from install) |

**Leg rule (frozen):** P iff `test_api()` returns normally; F on any exception. The expected vector is
DERIVED at run time by the round-63 module's `predict_legs()` from the case declarations — never
retyped (the r59 lesson M-1 mechanism).

**The corrected K2 stderr clause (the one clause round 63 missed).** Round 63's frozen clause demanded
the literal `localhost:8080` in K2's captured pip stderr; pip 26.2.1 renders the endpoint as
`HTTPConnection(host='localhost', port=8080)` and the literal appears 0 times
(`corpus/evidence/round63/k2-pip-stderr.txt`: `grep -c 'localhost:8080'` → 0, `grep -c 'port=8080'` → 5).
The corrected clause is grounded in mechanism, not just observation: the rendering is the `repr()` of
an `http.client.HTTPConnection` (S240, opened live this round — `HTTPConnection.__repr__` renders host
and port as separate fields, so the literal `localhost:8080` is not a form this renderer can produce).
**Frozen clause:** K2's captured pip stderr contains BOTH `host='localhost'` AND `port=8080`, AND
pip's own words say the connection was refused (`Errno 111` or `Connection refused`) — the round-63
confound guard, carried over.

**Receipt of record (new format, frozen):** `corpus/evidence/round68/pypi/receipt.txt`, lines:

```
PROBE sha256=<sha256 of plans/round68_c1_pypi_finish.py>
BASE-PROBE sha256=2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929
GRADER sha256=82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6
CASE K1 leg=test_api observed=P expected=P exception=none index_pid=<pid> wheel_sha256=<sha> stderr_sha256=<sha>
CASE K2 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=none wheel_sha256=none stderr_sha256=<sha>
CASE K3 leg=test_api observed=F expected=F exception=AssertionError index_pid=<pid> wheel_sha256=<sha> stderr_sha256=<sha>
CASE K4 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=<pid> wheel_sha256=<sha> stderr_sha256=<sha>
K1 server-log sha256=<sha> served_simple=True served_wheel=True
K2 stderr-names-endpoint=True
CLASS network-service executed=2
PREDICTION-VECTOR P/F/F/F derived=P/F/F/F
PREDICATE R68-C1 pass
CLASS-PROBE-EXIT=0
```

Committed evidence beside it: per-case stderr captures `corpus/evidence/round68/pypi/stderr/<case>.txt`
(K2's is the `pip_install_stderr` bytes; K1/K3/K4's is the leg run's combined output), the K1 server
access log `corpus/evidence/round68/pypi/server-log.txt`, and the live witness
`corpus/evidence/round68/pypi/battery-run.txt` (the in-runner captured exits of the fresh battery and
of `--check-receipt`).

**Predicate R68-C1 (one sentence, the same in the plan, the probe's `check` and the receipt):**
`python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt`
exits 0 and prints `PREDICATE R68-C1 pass`, where the receipt carries exactly one `CASE` line per
frozen case K1–K4 whose observed and expected values both equal the frozen vector P/F/F/F, a `PROBE`
sha equal to the committed probe bytes, a `BASE-PROBE` sha equal to the committed round-63 probe bytes,
a `GRADER` sha/pin equal to the committed capture, per-case `stderr_sha256` values equal to the
committed stderr captures, a K1 `index_pid` that is not `none` with a 64-hex `wheel_sha256`, a K1
server-log sha equal to the committed log which itself contains a `/simple/vectorops` fetch and a
`/packages/vectorops-0.1.0-` wheel fetch, a K2 clause line `K2 stderr-names-endpoint=True` whose
committed stderr capture contains `host='localhost'`, `port=8080` and a connection-refused marker, a
`CLASS network-service executed=2` line, and a `PREDICTION-VECTOR` whose derived vector equals P/F/F/F
re-derived at check time.

**Checker strictness (the A1 lessons, carried):** duplicate or unknown CASE lines are defects; a
missing receipt line is a defect; the stored `PREDICATE` line must agree with the derived verdict; the
receipt's `CLASS-PROBE-EXIT` must equal 0 iff the derived verdict is pass; every sha the receipt names
is re-hashed from committed bytes at check time (PROBE, BASE-PROBE, GRADER, stderr captures, server
log) — a receipt naming a sha the committed bytes do not carry is refused.

**Kill rules:**
- (a) any frozen vector differs from the receipt → the claim is not admitted and the miss is
  reported; the table is not edited after the run.
- (b) `--check-receipt` exits non-zero on the receipt of record for a reason other than a miss in (a)
  → the counter is wrong, the claim is not admitted.
- (c) a case hangs past the 900 s bound → the probe exits 2 (could-not-evaluate), the claim is not
  admitted, and no vector is inferred.
- (d) K2 returns P → the counter or the grader reading is wrong; the claim is dead and the round
  reports it (carried from round 63).
- (e) any seat finds the probe reaching a foreign service on 8080 → predicate fails (carried).

**Do-nothing control (scored before this freeze, committed):** the base state skips the claimed work
entirely — `corpus/evidence/round68/pypi/receipt.txt` does not exist at base
(`git cat-file -e d2ed4ca3:corpus/evidence/round68/pypi/receipt.txt` → absent), and the closest
existing artifact, the round-63 run1 receipt of record, fails the new predicate's necessary conditions
(it carries no `PROBE`, `BASE-PROBE` or `stderr_sha256` fields). Control receipt:
`corpus/evidence/round68/controls/control-old-receipt.txt`. The counter is not already met by the
control; a fabricated-receipt red fixture is additionally required in the counter's `--selftest`
(all-P vector with fabricated shas → refused).

**Named limitations (stated before data):**
- (i) `--check-receipt` re-derives consistency from committed bytes; it cannot by itself prove that
  the run happened. The live-run provenance is the fresh battery's own server access log and the
  in-runner captured exits (`battery-run.txt`). L0 `kengaku | round-67` (line 280, receipt-provenance
  standard) stays open; nothing assumed answered.
- (ii) The corrected clause is grounded in the captured bytes and in S240's mechanism at Python
  3.14.8 / pip 26.2.1; a future pip or CPython that changes the rendering would need a new re-freeze.
  The knowledge entry's `recheck:` cadence records this.
- (iii) The SKILL class row flips to `executed 2 of 8` counting `pypi-server` via THIS round's receipt
  of record; the round-63 receipt of record stays MISS and the L0 `kengaku | round-63` stays open.

**Counting commands:**
- before (base): `git show d2ed4ca3:SKILL.md | grep -c 'executed 1 of 8'` → 1;
  `git cat-file -e d2ed4ca3:corpus/evidence/round68/pypi/receipt.txt` → absent (rc 128).
- after: `python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt; echo $?`
  → `PREDICATE R68-C1 pass`, exit 0; `grep -c 'executed 2 of 8' SKILL.md` → 1;
  `grep -cE '^\|[[:space:]]*S240[[:space:]]*\|' corpus/SOURCES.md` → 1.

**Capability row (enters only if the predicate passes):** `offline-network-service-grader-probe` →
runs a TB2 grader whose `install` step reaches a localhost index, against a lane-built PEP 503 index,
inside bwrap, with the leg vector frozen and the corrected stderr clause byte-bound →
`python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt` →
first working round 68 (the round-63 declaration never demonstrated the capability running clean; the
row enters only now, on this round's pass).

**Sourced:** S228 (the grader at pin, mined round 63) and **S240 — CPython `Lib/http/client.py`
`HTTPConnection.__repr__` at tag `v3.14.8`, opened live this round** (the mechanism that makes the
corrected clause the right clause). S240's row is appended only after the scout's live capture and
located quote are in the wave dir.

---

## R68-C2 — calibration (held at ceiling 10, exercised): the round-67 closure's five routed defects land as dated corrections with re-deriving receipts

Defects (all from `corpus/lessons/round-67-verifier-spotcheck.md` §5, items 1–5; item 6 is
conformance-neutral and is recorded, not corrected):

1. **Wrong instrument sha cited.** The round-67 report (Amendment A1 bullet) and the
   `corpus/evidence/round67/pipe/a1-mutants.txt` header cite `32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836`
   as the amended counter; that is the pre-A1 frozen probe at `dcc39ea3`. The receipt of record and the
   committed probe bind `03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e`.
2. **Mutant count drift.** Report and `LOG.md:2542` say A1 mutants "8 killed, 1 accepted"; the
   committed `a1-mutants.txt` shows 7 refused (rc 1) + 1 accepted by design = 8 mutants.
3. **Self-test tally not committed.** The report/LOG quote `SELFTEST green_rc=0 red_rc=1 ok` for the
   round-67 probe, but no committed file records that tally.
4. **Registry rows stale.** `SKILL.md`'s registry has no row for the `round67_c1_pipeline_probe` gate,
   and the `round65-c1-sqlite-probe` row (SKILL.md:686) was not updated for the new `--strict` flag or
   its verdict codes.
5. **SKILL-row before-value misstated.** The round-67 report's R67-C1 before-state says "process-
   environment executed 1 of 3"; the committed bytes at `4bc29fd8` read `recipe-unexecuted` (round 66
   executed the tensor-parallelism member but never updated the row). The true delta is
   `recipe-unexecuted → executed 2 of 3`.

**Where each correction lands (append-only; nothing rewritten in place):**
- 1, 2, 5 → a dated `## Erratum (round 68)` section appended to `plans/round-67-claims.md`, plus an
  R1-form dated erratum appended to `corpus/evidence/round67/pipe/a1-mutants.txt`, plus a Corrections
  section in the round-68 fleet report (the round-67 report itself is not edited).
- 3 → the tally committed as `corpus/evidence/round68/r67-probe-selftest.txt`, produced by running the
  committed round-67 probe's `--selftest` with the exit captured in-runner and the probe's sha256
  recorded in the file.
- 4 → the registry rows land in `SKILL.md` (drafted by a scribe seat, integrated by the L1).

**Gate:** `plans/round68_c2_correction_gate.py` (built in the wave per this spec). Modes: default =
check the lane tree; `--selftest` = build red fixtures under the scratch root and prove every check
can fail. Five checks, each printing `E<n> ok <detail>` or `E<n> defect <detail>`:

- **E1 erratum-sha:** `plans/round-67-claims.md` contains exactly one `## Erratum (round 68)` heading,
  and the section names both
  `03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e` and
  `32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836`.
- **E2 mutant-count:** the same erratum states `7 refused` and `1 accepted by design` (each substring
  present at least once in the section).
- **E3 selftest-tally:** `corpus/evidence/round68/r67-probe-selftest.txt` exists, contains a
  `PROBE sha256=03793f4f…` line, contains a `SELFTEST` line and an `rc=` capture, and the gate's own
  re-hash of `plans/round67_c1_pipeline_probe.py` equals `03793f4f…`.
- **E4 registry-rows:** `SKILL.md` contains at least one `round67_c1_pipeline_probe` registry row, and
  the `round65-c1-sqlite-probe` row line contains `--strict`.
- **E5 before-value:** the erratum names the true delta — both `recipe-unexecuted` and
  `executed 2 of 3` present in the section.

**Predicate R68-C2 (one sentence, the same in the plan, the gate's code and the receipt):**
`python3 plans/round68_c2_correction_gate.py` exits 0 and prints `PREDICATE R68-C2 pass` with
`DEFECTS n=0`, where every check E1–E5 passes against the landed lane tree, and the gate's
`--selftest` has already shown every check failing on its injected red fixture.

**Counting commands:**
- red-before (measured by the wave, before any correction lands): `python3 plans/round68_c2_correction_gate.py`
  → `DEFECTS n=5`, `PREDICATE R68-C2 fail`, exit 1 (receipt `.ufo/waves/round-68/w1/gate/red-before.txt`).
- after (landed): same command → `DEFECTS n=0`, `PREDICATE R68-C2 pass`, exit 0 (receipt
  `corpus/evidence/round68/c2-green.txt`).
- per-item anchors: `grep -c '^## Erratum (round 68)' plans/round-67-claims.md` → 1;
  `grep -c 'ERRATUM-68' corpus/evidence/round67/pipe/a1-mutants.txt` → 1;
  `test -e corpus/evidence/round68/r67-probe-selftest.txt`;
  `grep -c 'round67_c1_pipeline_probe' SKILL.md` → ≥1;
  `grep -c 'recipe-unexecuted' plans/round-67-claims.md` → ≥1 (in the erratum section).

**Kill rules:** (a) the gate passes the pre-landing tree (false green) → not admitted; (b) the gate
fails the landed tree → the miss is reported, the checks are not narrowed after data; (c) a check that
cannot fail in `--selftest` → the gate is vacuous, not admitted.

**Named limitation (stated before data):** the gate checks the corrections' presence and
self-consistency (re-hashed shas, re-derived counts where the bytes allow); it does not re-verify the
round-67 probe's behavior — that is the round-67 record's own evidence.

**Sourced:** the defects are the round-67 non-author closure's own findings; no `S###` row is cited by
C2 (the sourced-claim duty is carried by C1 via S240).

---

## Frontier step (inside the claim cap; not a claim)

- **F1 — source opened live this round (2026-11-03).** S240: CPython `Lib/http/client.py` at tag
  `v3.14.8`, `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py`, opened by
  the scout seat (curl, sha256 recorded, capture + located ≤25-word quote at `HTTPConnection.__repr__`
  in the wave dir). Tier A (code; scope: the endpoint rendering pip embeds in connection-refused
  stderr). C1 rests on it.
- **F2 — mistakes mined.** `corpus/lessons/round-68.md` `## Mistakes`: the round-67 routed defects
  (wrong-sha citation class: a report quoting a sha from memory instead of re-hashing the committed
  bytes; count-drift class) plus anything this round's own seats catch. Every row: class · evidence
  pointer · captured-by · fix.
- **F3 — census.** Round start (committed at the freeze): `.ufo/waves/round-68/census-before.txt` —
  `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, 24 pre-existing
  W04 warnings, registry ok. Round end: the same command → exit 0 required (S240 appended).
- **F4 — assimilation.** None this round: the round-54 mass id drift (L0 `kengaku | round-54`, lines
  213–214: 175 staged rows vs a 190-row registry, 114 collisions) is unresolved and the operator has
  not ruled on re-staging vs retirement; adopting nothing is the honest state (round-67 precedent).
- **F5 — considerthese.** Scanned by a scribe seat this round; the 2026-10-26 proposal (class
  histogram sweep, pick next graders by uncovered class) is already implemented by rounds 62–67. Any
  still-unimplemented proposal found is reported; adoption only if it fits a claim.

---

## Controls summary

- Do-nothing control (C1): the base state — no round-68 receipt exists, and the round-63 run1 receipt
  fails the new predicate's necessary conditions (`corpus/evidence/round68/controls/control-old-receipt.txt`,
  committed at the freeze).
- Fabricated-receipt red fixture (C1): required in the new counter's `--selftest` (all-P vector with
  fabricated shas → refused).
- Red-before (C2): the correction gate's 5-defect run before any correction lands.
- Host state: no listener on 8080 at the freeze (`ss -ltn | grep -c 8080` → 0); the probe re-checks
  port freedom before every case (round-63 machinery).
- Kill rules: stated per claim; no rule is changed after data.

---

## Amendment A1 (dated 2026-11-03, after the receipt of record and the wave's settled attacks; does not change any predicate, vector, case or kill rule)

1. **S240 re-sourced (mechanism attribution corrected, clause semantics unchanged).** The wave's
   scout and revenger seats established from the opened bytes that CPython's
   `Lib/http/client.py` `HTTPConnection` defines **no** `__repr__`/`__str__` at v3.14.8
   (`S240 opened`, `.ufo/waves/round-68/w1/recon/S240-receipt.md`; `S240-client-py.txt`, sha256
   `016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230`). The renderer of
   `HTTPConnection(host='localhost', port=8080)` is **urllib3's `HTTPConnection.__str__`**
   (`pip/_vendor/urllib3/connection.py:163-164`, byte-identical to upstream urllib3 2.7.0,
   sha256 `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`,
   `.ufo/waves/round-68/w1/RenderingTrace.md` §5 chain). S240's registry row therefore names the
   urllib3 source at tag 2.7.0 (`corpus/SOURCES.md`), and every claim-doc mention of S240's
   attribution reads "urllib3 `HTTPConnection.__str__`" — the frozen clause's semantics
   (`host='localhost'` + `port=8080` + a connection-refused marker; the contiguous literal
   `localhost:8080` absent) are confirmed unchanged (`literal-possible=False`).
2. **Kill rule (c) named limitation, stated as found (not instrumented, not patched).** The
   frozen text names "the 900 s bound"; the instrument's own `LEG_TIMEOUT = 900` is dead code —
   the operative bound is the round-63 module's `LEG_TIMEOUT = 180`, and a timeout maps to a
   leg `F` under the frozen leg rule, not exit-2 (`ForgeScan` M-1, `.ufo/waves/round-68/w1/ForgeScan.md`;
   `ClaimFalsify` kill-rule review agrees). The scored run observed no timeout (K1 P with a
   non-`none` pid; K2/K3/K4 `CalledProcessError`/`AssertionError` within bounds), so the
   verdict stands; a timed-out leg would have scored `F` under the same leg rule — an
   evaluation, not a hang — while a `SETUP`/rc-2 surface is not implemented by the frozen
   instrument.
3. **C2 gate E1 strengthened to its own frozen sentence (counter amendment, R67-A1 pattern).**
   The frozen E1 says "exactly one `## Erratum (round 68)` heading"; the committed gate found
   the first heading only, so a duplicated section passed (`ForgeScan` M-2, fake-root fixture;
   `GateRedRun` clause fixtures agree). A1 makes E1 count the heading lines and require exactly
   one. Evidence: `corpus/evidence/round68/c2-e1-exactly-one.txt` (the duplicate-heading fixture
   refuses with `E1 defect … heading count 2` post-patch). Nothing else in the gate changed;
   its red-before (5 defects against the pre-landing tree) and selftest (5/5 fail-in-fake)
   receipts are recorded against the frozen bytes.
4. **CounterMutate F7 instrument defect recorded (not patched — the probe's `PROBE` line pins
   its bytes):** with the base probe absent or drifted, `run_battery` raises
   `AttributeError`/`FileNotFoundError` instead of the documented `SETUP` + rc 2
   (`CounterMutate` F7, `CounterMutate-evidence/extra-out.txt`). The `--check-receipt` path is
   unaffected (`base-probe-bytes` fires correctly); scored verdict unaffected.

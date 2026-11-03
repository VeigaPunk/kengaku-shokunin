# ReceiptReview — adversarial review of the frozen R68-C1 instrument (round 68, w1)

Seat: ReceiptReview · 2026-11-03 · read-only review of
`plans/round68_c1_pypi_finish.py` (553 lines, read in full) against the frozen predicate in
`plans/round-68-claims.md` (R68-C1, read in full), plus empirical checks of the receipt of
record. Both instruments (`round68_c1_pypi_finish.py`, base `round63_c1_pypi_probe.py`,
787 lines, read in full) were read line-by-line; no rule was edited and nothing in the lane
was written except this file.

Environment: Python 3.14.8 (`/usr/bin/python3`, matches the frozen environment). No tools
installed (nothing to record under the operator authorization). No subagents, no background
jobs, nothing bound on 8080 (`--check-receipt` only imports the base module, whose top level
is constants + defs behind an `if __name__ == "__main__"` guard — verified, base lines
778–787 — so the checker cannot bind the port).

Tree state: lane HEAD `d5b3c309` ("round-68 freeze fix"); the instrument is committed clean
at HEAD and its working-tree bytes hash to the receipt's `PROBE` value; `corpus/evidence/round68/`
is untracked, exactly as the round assignment states (the L1 lands it after the wave). The
freeze commit is `a8883187`, on top of round-start base `d2ed4ca3`.

---

## 1. Clause-by-clause: the frozen predicate sentence vs `check_receipt`

The frozen sentence (claims, "Predicate R68-C1") requires `--check-receipt` to exit 0 and
print `PREDICATE R68-C1 pass` where the receipt carries the eleven items below. Frame: the
exit/print contract is implemented at `round68_c1_pypi_finish.py:395–404` (defect lines →
`CHECK defect`, no defects → `CHECK ok` + `PREDICATE R68-C1 pass` + `return 0`).

| # | clause (frozen sentence) | implementation (function : lines) | as written? |
|---|---|---|---|
| 1 | PROBE sha equal to the committed probe bytes | `check_receipt` :243–254 — receipt value vs `own_sha256()`, which re-hashes the running instrument's file (`:60–62`); invoked as `python3 plans/round68_c1_pypi_finish.py` those are the committed bytes | yes |
| 2 | BASE-PROBE sha equal to the committed round-63 probe bytes | :256–264 — receipt value vs frozen constant AND the committed `plans/round63_c1_pypi_probe.py` re-hashed (`base-probe-bytes`, :263–264); import itself is byte-gated (`load_base_probe` :65–71) | yes (stronger: bytes re-hashed, not just the receipt string) |
| 3 | GRADER sha/pin equal to the committed capture | :266–276 — sha and pin vs frozen constants (:270–274) AND the committed capture `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` re-hashed via `m.GRADER_REL` (`grader-bytes`, :275–276; base probe :94). Pin note → finding O5 | yes for the sha; pin checked against the instrument constant only |
| 4 | exactly one CASE line per frozen case K1–K4, observed==expected==frozen | :278–313 — duplicates flagged (`case-duplicate` :293–294), unknown names flagged (`case-unknown` :295–297), missing flagged (`K<n>-case-missing` :301–302), per-case `expected` and `observed` both compared to `FROZEN_VECTOR` (:305–311), `leg=test_api` enforced (:312–313) | yes (leg field is extra strength beyond the sentence, consistent with the frozen receipt format) |
| 5 | per-case `stderr_sha256` equal to the committed stderr captures | :358–368 — all four captures re-hashed from `corpus/evidence/round68/pypi/stderr/<case>.txt` and compared (:367–368); missing capture → defect (:365–366); K2 additionally bound inside the clause block (:350–351) | yes (the K2 double-binding is redundant-but-harmless strength) |
| 6 | K1 `index_pid` not `none`, 64-hex `wheel_sha256` | :314–319 — pid refused when empty or `none` (:315–316); wheel sha refused unless 64 lowercase-hex (:317–319). A missing pid field also defects, aligned with "a missing receipt line is a defect" | yes |
| 7 | K1 server-log sha equal to the committed log, which itself contains a `/simple/vectorops` fetch and a `/packages/vectorops-0.1.0-` wheel fetch | :321–337 — committed log re-hashed and compared to the receipt line (:325–331); both fetch substrings demanded in the committed log's own bytes (:332–335); `served_simple=True`/`served_wheel=True` flags demanded on the receipt line (:336–337); missing log → defect (:324) | yes |
| 8 | corrected K2 clause: line `K2 stderr-names-endpoint=True`, and the committed K2 capture contains `host='localhost'`, `port=8080`, and a connection-refused marker | :339–356 — exact clause line (:344–345); K2 capture sha vs the K2 CASE line (:350–351); `K2_HOST` and `K2_PORT` containment in the committed bytes (:353–354); refused marker = `Errno 111` OR `Connection refused` (`K2_REFUSED`, :47; check :355–356). Containment is whole-text, no same-line requirement — exactly the frozen wording | yes |
| 9 | `CLASS network-service executed=2` line | :371–372 — exact-line membership; missing → `class-line` defect | yes |
| 10 | `PREDICTION-VECTOR` whose derived vector equals P/F/F/F re-derived at check time | :373–381 — receipt `derived=` suffix vs frozen (:377–379) AND live `m.predict_legs()` (base :163–181) re-derived at check time (`prediction-drift` :380–381). Head nuance → finding O3 | yes for the derived vector; the stored head vector before `derived=` is not compared |
| 11 | stored PREDICATE line agrees with the derived verdict; CLASS-PROBE-EXIT equals 0 iff derived pass | :383–393 — `stored-predicate` defect :392–393; `exit-agreement` defect :390–391 with `want_exit = "0" if derived_pass else "1"` (:387–389), computed after all byte/case/clause checks | yes ("0 iff pass" implemented literally) |

Result: **11/11 clauses implemented as written.** No clause is missing; two are stronger
than the sentence (BASE-PROBE/GRADER bytes re-hashed; `leg` field enforced) and two are
calibrated nuances that match the sentence's literal wording but not the full receipt format
line (O3, O4 below).

### Checker-strictness sentence (the carried A1 lessons), item by item

- "duplicate or unknown CASE lines are defects" — :293–297 ✓
- "a missing receipt line is a defect" — every required line has a missing/absent defect path:
  PROBE :253–254, BASE-PROBE :261–264, GRADER :270–276, CASE :301–302, server log :324/:336–337,
  K2 clause line :344–345, per-case captures :365–366, CLASS :371–372, PREDICTION-VECTOR :375–376,
  PREDICATE :385+392–393, CLASS-PROBE-EXIT :386+390–391 ✓
- "the stored PREDICATE line must agree with the derived verdict" — :392–393 ✓
- "CLASS-PROBE-EXIT must equal 0 iff the derived verdict is pass" — :387–391 ✓
- "every sha the receipt names is re-hashed from committed bytes at check time" — PROBE
  (own file :253), BASE-PROBE (:263), GRADER capture (:275–276), all four stderr captures
  (:365–368), server log (:327–331). The per-case `wheel_sha256` values are deliberately
  outside this list — they name ephemeral scratch bytes, not committed bytes, so no checker
  can re-hash them; the checker format-checks them (64-hex). This matches the sentence's own
  enumeration and named limitation (i). ✓ (see O6)

---

## 2. The frozen check-receipt run (step 3)

Command (from the lane root, exit captured in-runner):

```
$ python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt; echo "exit=$?"
CHECK ok cases=4 vector=P/F/F/F wheel_sha256=6fad8ea86492...
CHECK stored-predicate=pass derived=pass
PREDICATE R68-C1 pass
exit=0
```

Expected output (`PREDICATE R68-C1 pass`, rc 0) reproduced exactly.

## 3. Re-hash of every sha the receipt of record names (step 4)

| receipt field | receipt value | my re-hash of committed bytes | match |
|---|---|---|---|
| PROBE | `4a6fae53…93b3fdfc` | `plans/round68_c1_pypi_finish.py` → `4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc` | ✓ |
| BASE-PROBE | `2ebaf54e…919b929` | `plans/round63_c1_pypi_probe.py` → `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929` | ✓ (also equals the frozen constant in the claims) |
| GRADER sha256 | `82c63517…2650be4c` | `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` → `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` | ✓ |
| GRADER pin | `2fd12b88…9766d6` | TB2 commit pin; committed referent `corpus/SOURCES.md:101` (S079 row) and grader provenance `SHA256SUMS:134` = `82c63517…  ./pypi-server/tests/test_outputs.py` | ✓ present (not re-derived by the checker → O5) |
| K1 stderr_sha256 | `268c02ef…ffecb3` | `stderr/K1.txt` → `268c02efc4bcdefb1d142a0f3e218eccf6429eaefea2f767a6dd664a90ffecb3` | ✓ |
| K2 stderr_sha256 | `dedbc20d…65375d` | `stderr/K2.txt` → `dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d` | ✓ |
| K3 stderr_sha256 | `9c7014b3…2b4a58` | `stderr/K3.txt` → `9c7014b3b55bad773f6b5ac8bf950338e191a40f1ea7e002a25f7a9e1f2b4a58` | ✓ |
| K4 stderr_sha256 | `6a0ccd86…e777ef` | `stderr/K4.txt` → `6a0ccd86a8b5606aa190add39cd8095eb5346b71d2a39eb08200b77e58e777ef` | ✓ |
| K1 server-log sha256 | `574c3a2f…47af28` | `server-log.txt` → `574c3a2f7594d05d45ab06526baa61fc36bcc3ee60ec04cc6716e88f1c47af28` | ✓ |
| CASE wheel_sha256 ×4 | K1 `6fad8ea8…`, K3 `df8d66ab…`, K4 `b97edcfc…` | not re-hashable: the wheels were ephemeral index bytes in the run's scratch dir, never committed (checker format-checks 64-hex only) | n/a by design (O6) |

**All eight re-hashable shas match the committed bytes. No defect.**

## 4. Receipt-of-record internal consistency (step 4, content proofs)

- **K2 capture** (`stderr/K2.txt`, 1526 B): contains `host='localhost'` and `port=8080`
  (five `NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to
  establish a new connection: [Errno 111] Connection refused")` WARNING lines) and both
  refused markers (`[Errno 111]` and `Connection refused`). The corrected clause's byte
  requirement is met with margin; the literal `localhost:8080` appears 0 times, exactly the
  round-63 miss this clause re-freezes. ✓
- **Server log** (`server-log.txt`): two 200 lines — `GET /simple/vectorops/` and
  `GET /packages/vectorops-0.1.0-py3-none-any.whl` — served by the probe's own
  `http.server` on 127.0.0.1:8080. Both fetch proofs present. ✓
- **CASE lines**: exactly 4, one per frozen case, in K1–K4 order; observed and expected both
  P/F/F/F; exceptions `none / CalledProcessError / AssertionError / CalledProcessError` match
  the frozen receipt-format line; K1 `index_pid=1323016` (not none), K1 wheel sha 64-hex;
  K2 `index_pid=none wheel_sha256=none` per the frozen format. ✓
- **Tail lines**: `K1 server-log … served_simple=True served_wheel=True`, `K2
  stderr-names-endpoint=True`, `CLASS network-service executed=2`,
  `PREDICTION-VECTOR P/F/F/F derived=P/F/F/F`, `PREDICATE R68-C1 pass`,
  `CLASS-PROBE-EXIT=0`. All present, exactly once each, no extra lines. ✓
- **Live witness** (`battery-run.txt`): every CASE line matches the receipt verbatim (same
  shas), `K2 ENDPOINT form=urllib3-host-port stderr_bytes=1526` matches the committed K2.txt
  size, `SERVED K1 requests=2` matches the log's two lines, and the final line is
  `PREDICATE R68-C1 pass`. Run-side provenance is consistent with the receipt. ✓
- K1 capture shows the leg ran against the probe's index from the scored work dir
  (`/fast/scratch/hyaku/kengaku-r68/scored/venv/...` in `pip show` output), consistent with
  the scratch-root convention and with no lane-tree writes.

## 5. Red-fixture probes I ran against the checker (scratch-only; no lane writes, no port)

The instrument's own `--selftest` (R1–R5) covers all-P vector, stale PROBE sha, duplicate
CASE line, missing K2 clause line, fabricated stderr sha. I additionally probed two
tolerances its selftest does not cover:

1. **Tampered PREDICTION-VECTOR head** (`PREDICTION-VECTOR X/Y/Z/Z derived=P/F/F/F`, all
   bindings genuine): `PREDICATE R68-C1 pass`, rc 0. The stored head vector before
   `derived=` is never compared (finding O3).
2. **Appended second predicate line** (`PREDICATE R68-C1 fail` after `CLASS-PROBE-EXIT=0`):
   `PREDICATE R68-C1 pass`, rc 0. `next()` takes the first occurrence; duplicates of
   non-CASE lines are not flagged (finding O4).

Both receipts are refused for free in practice — any forged line still has to carry shas the
committed bytes support — but they bound what the checker actually enforces.

## 6. Findings (severity-ordered; seat reports, does not edit)

**O1 — kill rule (c) is not implemented as written (run-side; not triggered in the scored
run).** Frozen: "a case hangs past the 900 s bound → the probe exits 2 (could-not-evaluate)
… no vector is inferred." The finisher defines `LEG_TIMEOUT = 900` (:37) but never uses it —
a dead constant. The operative per-leg timeout is the base module's `LEG_TIMEOUT = 180`
(base :101, consumed in `run_leg` :364–373), and a `subprocess.TimeoutExpired` there is
converted into a leg observation `("F", "TimeoutExpired", "")` (base :372–373). On a hang
the battery would therefore write a receipt whose hung case reads `observed=F
exception=TimeoutExpired` and exit 1 (observed-vector mismatch), i.e. a vector IS inferred
and the exit code is 1, not 2. Fail-closed either way (the claim is not admitted); the
receipt of record was produced without any hang, so the scored verdict is unaffected. A
future re-freeze should either use the constant or restate the rule at 180 s.

**O2 — run-side refusals exit by unhandled traceback, not exit 2 (run-side; not
triggered).** The finisher's `main` does not wrap `run_battery` in
`try/except SetupError → print("SETUP …") → return 2` (the round-63 probe's `main` does,
base :766–773), and the battery's per-case `try` has only `finally` (:186–188). Any refusal
inside the loop — `port-8080-occupied` (`require_port_free`), `server-not-ready-in-5s`,
K1 confound (:162–164), K2 pip-success/confound guards (:176–184) — propagates as an
unhandled exception: rc 1 with a traceback, no `SETUP` line, no receipt. Fail-closed (the
claim cannot be admitted on a confound), but it diverges from the base instrument's
documented 0/1/2 exit map and from kill rule (c)'s exit-2 wording. Note also: per-case
stderr captures for cases completed before a mid-battery abort are already committed to the
evidence dir (each case writes its capture inside the loop, :189–191), so an aborted battery
can leave a partial evidence tree alongside the missing receipt.

**O3 — the stored PREDICTION-VECTOR head is unchecked (checker; as-written).** The sentence
names only the derived vector; the checker compares only the `derived=` suffix (:377–379).
A receipt with head `X/Y/Z/Z` passes (probe 1 above). If the L1 wants the full format line
`PREDICTION-VECTOR P/F/F/F derived=P/F/F/F` pinned byte-for-byte, that is a future
re-freeze, not an edit now.

**O4 — duplicates and unknowns are defects only for CASE lines (checker; as-written).**
The strictness sentence enumerates duplicates/unknowns for CASE lines only, and the checker
implements exactly that (:293–297). Duplicated non-CASE structural lines are ignored (first
occurrence wins, probe 2 above), unknown non-CASE lines are ignored, and a degenerate `CASE`
line with no name token would crash the parser (IndexError → rc 1 — fail-closed, never
false-green). Within the trust model (the receipt is written by the same committed
instrument whose sha is bound), none of these yields a false pass.

**O5 — the pin is checked against the instrument constant, not re-derived from a committed
capture (checker; as-written).** "GRADER sha/pin equal to the committed capture": the sha is
re-hashed from the committed capture (:275–276); the pin is compared to the `TB2_PIN`
constant both instruments carry (:269–274; base :93). The pin's committed referent exists
(`corpus/SOURCES.md:101`, S079 row) but is not consulted. The strictness sentence lists only
shas for re-hashing, so this is as-written; noted for completeness.

**O6 — K1/K3/K4 `wheel_sha256` are format-checked only.** The wheels were served from the
ephemeral scratch index and never committed, so no checker (this one or any future one) can
re-hash them; the strictness sentence's enumeration correctly excludes them. The honest
limit is disclosed by named limitation (i).

**O7 — neutral mechanism note.** The battery prints `K2 ENDPOINT form=…` from the base
module's `stderr_names_endpoint` (base :122–133), whose "url" alternative still matches the
literal `localhost:8080` — but the operative `k2_clause` is the frozen containment form
(:185), and the checker re-checks the committed bytes independently (:353–356). The
diagnostic cannot weaken the clause.

**Positive verifications worth recording:** the battery refuses to write a receipt unless
its own K1 server log carries both fetches (:156–164); the K2 confound guards (pip-success
refusal, refused-words refusal, :176–184) are carried from round 63 as the claims state; the
base probe is byte-verified before import (:65–71) and has no import-time side effects; the
grader capture's `test_api()` matches the claims' description (calls `install()` →
`pip install --index-url http://localhost:8080/simple vectorops==0.1.0` → four `dotproduct`
asserts, read in full); `SHA256SUMS:134` carries the grader sha; the 13-line receipt is
exactly the frozen format.

## 7. Residual risk and verification gaps

- I did not re-run the battery (the receipt of record exists; port 8080 is the L1's; a
  re-run would create a second receipt and confound nothing but prove nothing new).
- The run itself (that pid 1323016's server actually served the leg) is evidenced by the
  access log + `battery-run.txt` witness, which are mutually consistent, but a checker
  cannot distinguish them from a fabricated-but-self-consistent pair; that is exactly the
  claims' named limitation (i), with L0 `kengaku | round-67` (line 280) still open.
- `battery-run.txt` is not sha-bound by the receipt (the frozen format does not bind it);
  its CASE lines match the receipt verbatim today, but nothing re-checks that after any
  future edit.
- Findings O1/O2 are code-path readings of untriggered branches (no hang/confound occurred
  in the scored run); they are traceable to cited lines but not empirically reproduced here
  (reproducing them would require occupying port 8080, which the bounds forbid).

---

**REVIEW clauses=11/11 implemented receipt=consistent verdict=pass**

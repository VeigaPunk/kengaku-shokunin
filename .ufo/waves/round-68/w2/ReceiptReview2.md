# ReceiptReview2 — clause-by-clause adversarial review of the R68-C1 receipt of record

Seat: `ReceiptReview2` (kengaku round 68, attempt 2, wave w2, leaf). Date: 2026-11-03.
Scope: read-only on the lane; this report + scratch only. No predicate, counter, case, kill rule or
target was edited by this seat.

Inputs reviewed in full:
- `plans/round-68-claims.md` (frozen at `a8883187`/`d5b3c309`; A1 + A2 amendments in HEAD `7803bdd4`)
- `plans/round68_c1_pypi_finish.py` (553 lines, `check_receipt` at :235-406)
- `plans/round63_c1_pypi_probe.py` (787 lines — bindings only: `GRADER_REL` :94, `TB2_PIN` :93,
  `CASES` :151-160, `predict_legs` :163-176)
- `corpus/evidence/round68/pypi/receipt.txt` (13 lines, the receipt of record)

Byte provenance: lane tracked tree is clean at HEAD `7803bdd4` (`git status --porcelain` shows only
untracked `.ufo/waves/round-68/w2*` entries); `git diff HEAD --name-only -- corpus/evidence/round68
plans/round68_c1_pypi_finish.py plans/round63_c1_pypi_probe.py corpus/evidence/round52` → empty;
`git diff --name-only 0e52fb5d HEAD` names only `.ufo/waves/round-68/w2*`, `plans/round-68-claims.md`
(A2 section) and `plans/round68_report_contract.py` — **none of the C1 artifacts changed between the
landing `0e52fb5d` and attempt 2**. Every verdict below is therefore on the committed landed bytes.

Environment: Python 3.14.8 (`/usr/bin/python3`) — matches the frozen environment. Tooling
authorization: nothing needed installing; no tool was installed or upgraded.

---

## 1. Clause table (frozen predicate sentence + A1 strictness, implemented as written?)

| # | Clause (frozen source) | Implemented | Evidence (function:line) | Verdict |
|---|---|---|---|---|
| 1 | Command exits 0, prints `PREDICATE R68-C1 pass` | yes | `check_receipt` :235; final print :401-402, `return 0 if ok else 1` :403; `main` :418-419 (`--check-receipt` → `check_receipt`) | ✔ observed rc=0 |
| 2 | exactly one `CASE` line per frozen case K1–K4 | yes | dict keyed by case name + `dup` list :283-291; `case-duplicate` :293-294; `case-unknown` :296-297; missing → `{name}-case-missing` :300-302 | ✔ |
| 3 | observed and expected both equal frozen P/F/F/F (positional) | yes | `zip(CASE_NAMES, FROZEN_VECTOR)` :299; `{name}-expected` :305-306; `{name}-observed` :307-308 | ✔ |
| 4 | `leg=test_api` per case (frozen case table) | yes | :309-311 `{name}-leg` | ✔ (extra strictness beyond the sentence) |
| 5 | `PROBE` sha equal to the committed probe bytes | yes | :251-254 vs `own_sha256()` :62 (this file's bytes) | ✔ |
| 6 | `BASE-PROBE` sha equal to the committed round-63 probe bytes | yes | double check :257-263 — receipt value vs frozen constant AND `sha256_file(base_path)` vs constant (`base-probe-bytes` :262-263) | ✔ |
| 7 | `GRADER` sha/pin equal to the committed capture | yes | :266-274 (sha + pin vs constants); committed capture re-hash at `lane / m.GRADER_REL` :275-277 (`grader-bytes`); `GRADER_REL` = `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` (base probe :94) | ✔ |
| 8 | per-case `stderr_sha256` equal to the committed stderr captures | yes | :359-368, all four cases, `sha256_file(lane/stderr/K<i>.txt)` | ✔ |
| 9 | K1 `index_pid` not `none` | yes | :315-316 (`K1-index-pid`; empty or `none` refused) | ✔ |
| 10 | K1 64-hex `wheel_sha256` | yes | :317-319 (len 64 + lowercase hex charset) | ✔ |
| 11 | K1 server-log sha equal to the committed log | yes | :322-330 (`server-log-sha`) | ✔ |
| 12 | log itself contains a `/simple/vectorops` fetch and a `/packages/vectorops-0.1.0-` wheel fetch | yes | :331-336, substring checks against the committed log bytes (`server-log-simple`, `server-log-wheel`) | ✔ (committed log: 1 and 1 matching lines) |
| 13 | `K2 stderr-names-endpoint=True` clause line | yes | :340-342, exact whole-line equality | ✔ |
| 14 | committed K2 capture contains `host='localhost'` AND `port=8080` | yes | :353-355 vs `K2_HOST`/`K2_PORT` :45-46, checked against `lane/stderr/K2.txt` bytes :345-348 | ✔ (5 and 5 occurrences in the committed capture) |
| 15 | K2 capture carries a connection-refused marker (`Errno 111` / `Connection refused`) | yes | :356-358 vs `K2_REFUSED` :47 | ✔ (5 matching lines) |
| 16 | contiguous literal `localhost:8080` **absent** (A1.1 restated clause semantics; seat envelope) | **NO** | no such check exists in `check_receipt` (:340-358 are the only K2 checks) | ✘ **F1** |
| 17 | `CLASS network-service executed=2` line | yes | :371-372, exact-line membership in the stripped line list | ✔ |
| 18 | `PREDICTION-VECTOR` derived vector equals P/F/F/F **re-derived at check time** | yes | stored `derived=` vs frozen :378-379; live `m.predict_legs()` vs frozen :374 + :380-381 (`prediction-drift`) | ✔ (prefix before `derived=` unchecked — F4) |
| 19 | stored `PREDICATE` line agrees with the derived verdict | yes | :384-385 + :396-398 (`stored-predicate`; derived verdict = `not failures`) | ✔ |
| 20 | `CLASS-PROBE-EXIT` equals 0 iff derived verdict is pass | yes | :386-390 — equality with `"0"` on derived-pass, `"1"` on derived-fail | ✔ (slightly stricter than "≠0 on fail"; matches the battery's own writer :214-215) |
| 21 | strictness: duplicate CASE lines are defects | yes | :285-286 + :293-294 | ✔ (demonstrated by the counter's own r3 fixture) |
| 22 | strictness: unknown CASE lines are defects | yes | :296-297 | ✔ |
| 23 | strictness: a missing receipt line is a defect | yes | absence path for every line type: PROBE :251-254, BASE-PROBE :257-263, GRADER :266-274, CASE :300-302, server-log :322-338, K2 clause :340-343, CLASS :371-372, VECTOR :373-377, PREDICATE :396-398, EXIT :386-390 | ✔ |
| 24 | strictness: every named sha re-hashed from committed bytes at check time | yes | PROBE :251-254, BASE-PROBE :261-263, GRADER :275-277, stderr ×4 :359-368, server log :325-330 | ✔ (K1/K3/K4 `wheel_sha256` + `index_pid` are not re-hashed — no committed bytes exist to hash them against; the frozen sentence does not require it; run-provenance is named limitation (i)) |

Battery-side corroboration (not part of `--check-receipt`, but the receipt's writer):
`require_port_free` before every case (finisher :161/:169-170 via base machinery) implements kill-rule
(e)'s quiet-window discipline; the K1 log is committed only after the live log proves both fetches
(finisher :178-192); K2 refuses on pip success or missing refused words (finisher :198-208).

## 2. Independent re-hash (this seat's own `sha256sum`, not the checker's)

| Artifact | Receipt value | sha256sum (mine) | Match |
|---|---|---|---|
| `plans/round68_c1_pypi_finish.py` (PROBE) | `4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc` | `4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc` | ✔ |
| `plans/round63_c1_pypi_probe.py` (BASE-PROBE) | `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929` | `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929` | ✔ |
| `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` (GRADER) | `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` | `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` | ✔ |
| `corpus/evidence/round68/pypi/stderr/K1.txt` | `268c02efc4bcdefb1d142a0f3e218eccf6429eaefea2f767a6dd664a90ffecb3` | same | ✔ |
| `corpus/evidence/round68/pypi/stderr/K2.txt` | `dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d` | same | ✔ |
| `corpus/evidence/round68/pypi/stderr/K3.txt` | `9c7014b3b55bad773f6b5ac8bf950338e191a40f1ea7e002a25f7a9e1f2b4a58` | same | ✔ |
| `corpus/evidence/round68/pypi/stderr/K4.txt` | `6a0ccd86a8b5606aa190add39cd8095eb5346b71d2a39eb08200b77e58e777ef` | same | ✔ |
| `corpus/evidence/round68/pypi/server-log.txt` | `574c3a2f7594d05d45ab06526baa61fc36bcc3ee60ec04cc6716e88f1c47af28` | same | ✔ |

Corroboration: `corpus/evidence/round52/graders/SHA256SUMS:134` =
`82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c  ./pypi-server/tests/test_outputs.py`
— the frozen "line 134" citation holds; pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` matches the
claims and base probe :93.

Content probes (independent of the checker): K2 capture — `host='localhost'` ×5, `port=8080` ×5,
refused marker ×5, contiguous `localhost:8080` ×**0**; server log — `/simple/vectorops` ×1,
`/packages/vectorops-0.1.0-` ×1.

## 3. Counting command (run once, receipt untouched)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round68_c1_pypi_finish.py \
    --check-receipt corpus/evidence/round68/pypi/receipt.txt
CHECK ok cases=4 vector=P/F/F/F wheel_sha256=6fad8ea86492...
CHECK stored-predicate=pass derived=pass
PREDICATE R68-C1 pass
rc=0
```

Frozen after-anchors re-derived: `grep -c 'executed 2 of 8' SKILL.md` → 1;
`grep -cE '^\|\s*S240\s*\|' corpus/SOURCES.md` → 1; base
`git show d2ed4ca3:SKILL.md | grep -c 'executed 1 of 8'` → 1. All as frozen.

## 4. Falsification probes (scratch copies only; the lane tree was never touched)

Harness: `probe.py` (scratch) copies exactly the nine files `check_receipt` reads into a scratch
lane root per variant, mutates the copy, and runs `--check-receipt` against the copy. Green control
first. All runs on the same committed bytes otherwise.

| Probe | Mutation | Result |
|---|---|---|
| M-0 | none (green control) | rc=0, `PREDICATE R68-C1 pass` (sanity) |
| M-a | stale duplicate `PROBE`/`BASE-PROBE`/`GRADER` lines inserted **after** the true ones | rc=0 **pass** |
| M-b | `exception=CalledProcessError` → `exception=UnicornError` (K2, K4) | rc=0 **pass** |
| M-c | contiguous `localhost:8080` line injected into the K2 capture, receipt `stderr_sha256` rebound to the mutated bytes | rc=0 **pass** |
| M-d | `PREDICTION-VECTOR` prefix `P/F/F/F` → `X/Y/Z` (derived= kept) | rc=0 **pass** |
| M-e | extra unknown line `NOTE forged-provenance line` appended | rc=0 **pass** |

## 5. Findings (severity order)

- **F1 (low-medium, the one substantive gap).** A1.1 restates the corrected K2 clause's semantics as
  "`host='localhost'` + `port=8080` + a connection-refused marker; the contiguous literal
  `localhost:8080` absent", and this wave's seat envelope carries the same wording — but the
  instrument enforces only the three presence checks (finisher :340-358); there is no absence check
  for the contiguous literal. Demonstrated: M-c injects the literal into a copy of the committed K2
  capture with the receipt sha rebound and the checker still prints pass. Mitigations, verified:
  the committed K2 capture carries the literal 0 times (`grep -c 'localhost:8080'` → 0), and per A1.1
  the renderer (urllib3 `HTTPConnection.__str__`) cannot produce that form, so the gap is latent, not
  exploited. Note also that the operative frozen case-table clause ("Frozen clause:" sentence) never
  demanded absence — the instrument is faithful to that sentence; the gap is against A1.1's
  restatement and my envelope. Per the goal, this seat does not edit the rule. Report-only
  recommendation for any future re-freeze: `if "localhost:8080" in k2_text: defect(...)`.
- **F2 (low).** Non-CASE lines are parsed first-match (`next(...)`: PROBE :251, BASE-PROBE :257,
  GRADER :267, server-log :322, K2 clause :340, PREDICTION-VECTOR :373, PREDICATE :384,
  CLASS-PROBE-EXIT :386); duplicates of these lines are unchecked, and within a CASE line a repeated
  token silently keeps the last value (:288-291). M-a demonstrates stale duplicate header lines
  passing. Faithful to the frozen strictness sentence (which scopes duplicate/unknown refusal to CASE
  lines only); strictness boundary, not a defect against the frozen text.
- **F3 (low).** `exception=` fields are parsed but never validated; M-b rewrites K2/K4's exceptions to
  `UnicornError` and the receipt still passes. The frozen predicate sentence does not name exception
  values (they appear only in the frozen receipt FORMAT block and the case table's mechanism notes),
  so this is faithful-as-written; the frozen format's exception values are unenforced documentation.
- **F4 (info).** The `PREDICTION-VECTOR` prefix before `derived=` is unchecked (M-d). The frozen
  sentence binds only the derived vector; the prefix is restated frozen vector, not enforced.
- **F5 (info).** Unknown non-CASE receipt lines are ignored (M-e). Same strictness scope as F2.
- **F6 (info, already recorded).** `LEG_TIMEOUT = 900` (finisher :37) is declared once and never
  referenced — dead code, confirming A1.2's record that the frozen "900 s bound" is not operative
  (the base module's 180 s applies and a timeout maps to leg F). No scored impact: no case timed out
  (K1 P with non-`none` pid; K2/K3/K4 failed with `CalledProcessError`/`AssertionError`).
- **F7 (info).** `served_simple=True`/`served_wheel=True` are checked as substrings of the log line
  (:337-338), not as whole tokens; benign — the battery writes exact tokens (:208-210 region) and the
  fetches are independently re-proven from the committed log bytes (:331-336).

## 6. Verdict

`check_receipt` implements the frozen R68-C1 predicate sentence clause-for-clause as written; no
clause of the frozen sentence is implemented more weakly than written (the absence sub-clause of F1
comes from A1.1's restatement, not the frozen sentence). All eight receipt-bound artifacts re-hash to
exactly the receipt's values; the counting command re-derives `PREDICATE R68-C1 pass`, rc=0, on the
landed bytes at attempt 2. The verdict of record stands. Findings F1–F3 are strictness-boundary
records for the next re-freeze, not grounds to refuse this receipt.

Residual risk / verification gaps: (i) `--check-receipt` cannot prove the run happened — the live
battery, server log and `battery-run.txt` carry that provenance (named limitation (i), unchanged);
(ii) `wheel_sha256`/`index_pid` are bound by the receipt's word only — no committed bytes exist to
re-hash; (iii) F1–F3 mean a *future* receipt could carry cosmetically wrong `exception=` fields or
duplicate header lines without refusal — any such receipt would still need every sha and the full
vector to pass, so the attack surface stays narrow.

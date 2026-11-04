# Round 70 claims — kengaku (hyaku run 15, attempt 1)

Base: `502893ad` (round-69 verifier spot-check tip; the lane tree was clean and the branch
equals its remote). Frozen 2026-11-03 **before** the C1 battery ran and **before** any C2
correction landed. Two claims, distinct axes, causally separable: C1 verifies from the C1
receipt and the SKILL.md class row alone; C2 verifies from the routed-defect gate alone.

## R70-C1 — coverage (lowest owned non-retired axis, L0-capped at 7): the `nginx-request-logging` TB2 grader replayed offline under a re-frozen seven-case table

**Frozen predicate (one sentence).** *Each of the seven frozen cases yields its frozen
eight-leg vector, every one of the eight grader legs is observed `P` in at least one case and
`F` in at least one case, each case line's `case_sha256` equals its frozen staged-input
digest, and the receipt's PROBE, PROBE_BLOB and GRADER sha256 equal the committed bytes; the
counter then prints `PREDICATE R70-C1 pass` and exits 0.*

**Instrument:** `plans/round70_c1_nginx_probe.py` (sha-bound in its own receipt; its
committed blob sha is recorded as `PROBE_BLOB`).
**Grader:** `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`,
sha256 `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0`
(= `corpus/evidence/round52/graders/SHA256SUMS:111`), TB2 pin `2fd12b88`.

**Leg order (the grader's file order).**
1 `test_nginx_installed`, 2 `test_nginx_running`, 3 `test_index_page_content`,
4 `test_custom_404_page`, 5 `test_nginx_config_syntax`, 6 `test_nginx_config_settings`,
7 `test_log_file_creation`, 8 `test_log_file_format`.

**Case table (frozen; `--render-table` must byte-equal it).** K1–K5 are round 69's table
unchanged; K6 and K7 are the two red witnesses round 69 lacked (round-69 Amendment A1 item 3).

| case | staged end state | legs 1..8 |
|---|---|---|
| K1 | all-green: service, bodies, config, shim, access log | `PPPPPPPP` |
| K2 | index body differs by one character (server otherwise green) | `PPFPPPPP` |
| K3 | service answers but writes no access log | `PPPPPPFF` |
| K4 | config lacks the `limit_req_zone` rate clause | `PPPPPFPP` |
| K5 | no `nginx` binary on PATH (shim absent) | `FPPPFPPP` |
| K6 | no HTTP service on 8080 (shim, config, bodies staged) | `PFFFPPFF` |
| K7 | custom-404 body differs by one character | `PPPFPPPP` |

`FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP/PFFFPPFF/PPPFPPPP` (seven
cases × eight legs = 56 observations).

**Freeze-time leg-coverage arithmetic (QUALITY Q51 — computed before data, not asserted).**
`python3 plans/round70_c1_nginx_probe.py --render-table` →
`LEG-COVERAGE-FROZEN legs=8 seen_p=8 seen_f=8`, with per-leg counts
`installed p=6 f=1`, `running p=6 f=1`, `index p=5 f=2`, `custom_404 p=5 f=2`,
`config_syntax p=6 f=1`, `config_settings p=6 f=1`, `log_creation p=5 f=2`,
`log_format p=5 f=2`. Round 69's table carried six reds for eight legs; this one carries
eight by construction, and the count is a printed command, not a sentence in a freeze doc.

**Staged-state digests (frozen).** `case_sha256` digests only the staged candidate inputs —
`etc/nginx/nginx.conf`, `etc/nginx/conf.d/benchmark-site.conf`, `etc/hosts`,
`tests/test_outputs.py`, `tests/runner.py`, `run/server.py`, `run/bodies.json`, the web root
and the shim — and excludes the work path and the server-written access log. The seven frozen
values are the `CASE_SHA` table in the instrument (all seven distinct):
`K1 0cf77ab8…`, `K2 c072ee5f…`, `K3 286db51e…`, `K4 22ee1ff8…`, `K5 5690e1e1…`,
`K6 d4035f6f…`, `K7 07eb2fd3…`. Path independence and byte sensitivity are arms of the
instrument's `--selftest` (`PATH-INDEPENDENT sha_equal=True`,
`STAGED-STATE changes_on_byte=True`).

**Measuring command.**
`python3 plans/round70_c1_nginx_probe.py --lane . --work <scratch> --receipt corpus/evidence/round70/nginx/receipt.txt --evidence-dir corpus/evidence/round70/nginx/sandbox`
then `python3 plans/round70_c1_nginx_probe.py --check-receipt corpus/evidence/round70/nginx/receipt.txt`.

**Kill rule.** Any case whose observed vector differs from its frozen vector; any leg with no
`P` or no `F` witness; any `SETUP` path (`grader-sha-mismatch`, `port-8080-occupied`,
`bwrap-absent`, `receipt-exists`); any `case_sha256` that differs from its frozen value; a
PROBE/PROBE_BLOB/GRADER sha that does not re-derive; or a `--check-receipt` defect list that
is nonempty. A miss is reported, not re-scored.

**Before → after targets (re-derivable).**
- `git cat-file -e 502893ad:corpus/evidence/round70/nginx/receipt.txt` → absent (rc 128) →
  receipt present with `PREDICATE R70-C1 pass`.
- `grep -c 'executed 2 of 8' SKILL.md` → 1 → the class row reads `executed 3 of 8`.
- `grep -cE '^\|[[:space:]]*S242[[:space:]]*\|' corpus/SOURCES.md` → 0 → 1 (the live-reopened
  instruction-file row, cited by the entry's corrected anchor).

**Do-nothing control (committed).** `.ufo/waves/round-70/c1-control.txt`: at base the
measurement command on the receipt path prints `SETUP receipt-missing` and exits 2, and
`grep -c 'executed 3 of 8' SKILL.md` → 0. A round that does nothing cannot reach the target.

**Named limitations (at freeze).** (i) `--check-receipt` re-derives text fields and cannot
prove a live run — the receipt's per-case `server_pid` lines and the committed sandbox
captures are the live witness. (ii) The `nginx` binary is a lane-written shim answering `-t`;
the replay prices the grader's config-file, HTTP-body and log legs, not nginx's own syntax
checker. (iii) K6 stages "no service" as a whole candidate state, so its five red legs are
not independently isolated; only K7 isolates one leg (4) with the service up. (iv) The
`case_sha256` binds staged inputs, not the grader's own behaviour.

**Round-69 findings carried into the instrument.** `case_sha256` is now a staged-input
digest (D-list / A1 item 3); `--check-receipt` re-hashes the lane's grader file and the
committed probe blob instead of trusting constants (round-69 ClaimFalsify M-J/M-K).

## R70-C2 — calibration (held at ceiling 10, exercised): the round-69 non-author closure's eight routed defects

**Frozen predicate (one sentence).** *Each of the eight defects the round-69 non-author
spot-check routed (`corpus/lessons/round-69-verifier-spotcheck.md` §6 D1–D8) is closed by a
dated correction that the gate re-derives as E1–E8, and the gate prints `DEFECTS n=0` and
`PREDICATE R70-C2 pass` with exit 0.*

**Instrument:** `plans/round70_c2_routed_defects.py`.

**Checks (frozen).**
- **E1 depth-gate-identity** (D1) — the two round-69 depth-gate captures are labelled for what
  they are (`TREE-CAPTURE … PRE-CLASS-ROW`, `LANDING-COPY …`), their recorded sha256s
  re-derive, and the two files differ in exactly one line whose only delta is the class-row
  pointer `corpus/knowledge/tb2-nginx-request-logging-offline.md` (paths total 33 → 34). The
  earlier cross-root "byte-identical" claim is superseded in
  `corpus/evidence/round70/c2/depth-gate-provenance.txt`.
- **E2 trio-receipt** (D2) — `corpus/evidence/round70/gates/trio-nginx.txt` equals a fresh run
  of `plans/round63_gate_checks.py trio corpus/knowledge/tb2-nginx-request-logging-offline.md`
  byte for byte.
- **E3 instruction-row** (D3) — the nginx entry's `source:` line names `S242` and the corrected
  anchor `instruction.md:6-11,15-18`; the registry row S242 carries the instruction URL at the
  pin, its sha256 `26a7ac98…9edf99` and the entry in `used-by`.
- **E4 s241-correction** (D4) — a row S243 opens `supersedes S241 —` and states leg 5 as the
  `nginx -t` subprocess, with the entry in `used-by`.
- **E5 corpus-index** (D5) — `corpus/README.md` carries the `lessons/round-69.md` row and a
  `## Round-69 supporting artifacts` block.
- **E6 r69-landing-receipt** (D6) — `corpus/evidence/round70/gates/r69-c2-landing.txt` records
  the round-69 gate's green run at its measured revision `4038bb11`
  (`DEFECTS n=0`, `PREDICATE R69-C2 pass`, `RC 0`).
- **E7 gate-reject** (D7) — the round-70 lesson's `## Gate` carries at least one rejected
  candidate with a stated reason, and the registry keeps the rejected row S244 (the
  `merge/kengaku` package entry refused this round).
- **E8 wave-validation** (D8) — `.ufo/waves/round-70/w1-validate.rc` reads `0` beside the
  stdout/stderr captures of the wave validator run.

**Kill rule.** Any `E<n> defect` line at the landing tip fails the predicate; a correction
that exists only as prose with no re-deriving check is not a closed defect.

**Before → after target.** `python3 plans/round70_c2_routed_defects.py` → `DEFECTS n=8`,
`PREDICATE R70-C2 fail`, rc 1 at base (receipt `.ufo/waves/round-70/c2-red-before.txt`) →
`DEFECTS n=0`, `PREDICATE R70-C2 pass`, rc 0 at the landing.

**Controls (committed).** `--selftest --work <scratch>` builds the pre-correction state from
real files (provenance absent, receipts absent, S242/S243/S244 stripped, anchor reverted,
README block removed, lesson absent, wave receipts absent) and must print
`SELFTEST defects-in-fake=8 want=8 all-fail=True`, then byte-flips the E2 receipt and requires
E2 red. `--mutants --work <scratch>` removes one `CHECKS` entry at a time from a generated copy
of the gate and runs it on that fake lane, requiring exactly 7 defects per mutant
(`MUTANTS total=8 killed=8`). A check that cannot fail refuses the gate.

**Do-nothing control.** The red-before run *is* the do-nothing measurement: the base bytes
satisfy none of E1–E8, so a round that lands nothing scores exactly `n=8`.

## Freeze scope and close

Frozen by this commit: `plans/round70_c1_nginx_probe.py`,
`plans/round70_c2_routed_defects.py`, this document, the wave spec and validated dispatch,
`census-before.txt`, `c2-red-before.txt`, `c1-control.txt`. No predicate, case table, vector,
digest, kill rule or target changes after this commit; an error found after data is an honest
miss or a dated amendment before any after-receipt is scored.

At close, re-derive both predicates from the committed bytes and record: the C1 receipt, the
C1 selftest tally, the C2 green run, the C2 selftest and mutation tallies, the census exit,
the depth and trio receipts, and the class-row count.

# Round 69 claims — kengaku (hyaku run 15)

Base: `a518980e` (round-68 verifier spot-check tip; the lane tree is clean and the branch
equals its remote). Frozen 2026-11-03 **before** the C1 battery ran and **before** any C2
correction landed. Two claims, distinct axes, causally separable: C1 verifies from the C1
receipt and the SKILL.md class row alone; C2 verifies from the routed-defect gate alone.

## R69-C1 — coverage (lowest owned non-retired axis, L0-capped at 7): the `nginx-request-logging` TB2 grader replayed offline

**Frozen predicate (one sentence).** *Each of the five frozen cases yields its frozen
eight-leg vector, every one of the eight grader legs is observed `P` in at least one case and
`F` in at least one case, and the receipt's PROBE and GRADER sha256 equal the committed bytes;
the counter then prints `PREDICATE R69-C1 pass` and exits 0.*

**Instrument:** `plans/round69_c1_nginx_probe.py` (sha-bound in its own receipt).
**Grader:** `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`,
sha256 `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0`
(= `corpus/evidence/round52/graders/SHA256SUMS:111`), TB2 pin `2fd12b88`.

**Leg order (the grader's file order).**
1 `test_nginx_installed`, 2 `test_nginx_running`, 3 `test_index_page_content`,
4 `test_custom_404_page`, 5 `test_nginx_config_syntax`, 6 `test_nginx_config_settings`,
7 `test_log_file_creation`, 8 `test_log_file_format`.

**Case table (frozen; `--render-table` must byte-equal it).**

| case | staged end state | legs 1..8 |
|---|---|---|
| K1 | all-green: service, bodies, config, shim, access log | `PPPPPPPP` |
| K2 | index body differs by one character (server otherwise green) | `PPFPPPPP` |
| K3 | service answers but writes no access log | `PPPPPPFF` |
| K4 | config lacks the `limit_req_zone` rate clause | `PPPPPFPP` |
| K5 | no `nginx` binary on PATH (shim absent) | `FPPPFPPP` |

`FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP` (five cases × eight legs = 40
observations). Each of the eight legs has one red witness and four green witnesses by
construction; a leg the table leaves un-red is a leg the replay does not price.

**Measuring command.**
`python3 plans/round69_c1_nginx_probe.py --lane . --work <scratch> --receipt corpus/evidence/round69/nginx/receipt.txt --evidence-dir corpus/evidence/round69/nginx/sandbox`
then `python3 plans/round69_c1_nginx_probe.py --check-receipt corpus/evidence/round69/nginx/receipt.txt`.

**Kill rule.** Any case whose observed vector differs from its frozen vector; any leg with no
`P` or no `F` witness; a `SETUP` path (`grader-sha-mismatch`, `port-8080-occupied`,
`bwrap-absent`, `receipt-exists`); or a `--check-receipt` defect list that is nonempty. A miss
is reported, not re-scored.

**Before → after targets (re-derivable).**
- `git cat-file -e a518980e:corpus/evidence/round69/nginx/receipt.txt` → absent (rc 128) →
  receipt present with `PREDICATE R69-C1 pass`.
- `grep -c 'executed 2 of 8' SKILL.md` → 1 → the class row reads `executed 3 of 8`.
- `grep -cE '^\|[[:space:]]*S241[[:space:]]*\|' corpus/SOURCES.md` → 0 → 1 (the live-reopened
  grader row, cited by the knowledge entry's nginx section).

**Do-nothing control (committed).** `.ufo/waves/round-69/nginx-control.txt`: at base
`--check-receipt corpus/evidence/round69/nginx/receipt.txt` prints `SETUP receipt-missing` and
exits 2, and `grep -c 'executed 3 of 8' SKILL.md` → 0. A round that does nothing cannot reach
the target.

**Dev build check, disclosed.** Two K1-only smoke runs preceded this freeze, staging only:
run 1 failed the four HTTP legs with `NameResolutionError` (the sandbox had no `/etc/hosts`);
the staging was fixed by binding a lane-written `/etc/hosts`; run 2 gave `K1 PPPPPPPP`. K2–K5
were **not** run before the freeze; their vectors are derived leg by leg from the grader
source.

**Named limitations (at freeze).** (i) `--check-receipt` re-derives text fields and cannot
prove a live run — the receipt's per-case `server_pid` and the committed sandbox captures are
the live witness. (ii) The `nginx` binary is a lane-written shim answering `-t`; the replay
prices the grader's config-file, HTTP-body and log legs, not nginx's own syntax checker.
(iii) `case_sha256` digests the staged tree; the checker records it but cannot re-stage.

## R69-C2 — calibration (held at ceiling 10, exercised): the round-68 closure's seven routed defects

**Frozen predicate (one sentence).** *Each of the seven defects the round-68 non-author
spot-check routed (`corpus/lessons/round-68-verifier-spotcheck.md` §5 items 1–7) is closed by
a dated correction that the gate re-derives as E1–E7, and the gate prints `DEFECTS n=0` and
`PREDICATE R69-C2 pass` with exit 0.*

**Instrument:** `plans/round69_c2_routed_defects.py`.

**Checks (frozen).**
- **E1 registry-rows** — the four round-68 instruments (`round68_c1_pypi_finish`,
  `round68_c2_correction_gate`, `round68_report_contract`, `round68_capability_table`) each
  carry a complete `## Gate/probe registry` row: name, kind, an entry file that exists in the
  lane, a verdict map naming `0` and `1`, a self-test cell, pinned values and write scope.
- **E2 quality-criterion** — `corpus/QUALITY.md` carries exactly one `## Round69 criterion`
  section, labelled `Q50`, citing `corpus/lessons/round-68.md` and
  `corpus/lessons/round-68-verifier-spotcheck.md` (the owed criterion for the `none`
  captured-by rows).
- **E3 receipt-provenance** — `corpus/evidence/round69/c2-receipts/provenance-erratum.txt`
  names `TREE 27f649f8` (the revision the round-68 C2 receipt graded), `LANDING 1ec2e60a`,
  and every bound input's sha256 **at both revisions**; the `DIFFERS` set equals the observed
  differing set (re-derived from `git show`).
- **E4 verified-at** — `corpus/knowledge/tb2-network-service-offline-grader.md` carries a
  second, appended `verified-at:` line naming `1ec2e60a` (the round-68 amendment tip).
- **E5 attack-arithmetic** — `corpus/lessons/round-68.md` carries exactly one line with
  `strict attack share`, `3/12`, and the strict role set (`reviewer`, `critic`,
  `mutation-tester`, `labrat`).
- **E6 results-rerecord** — `corpus/lessons/round-68.md` records that `w1-results.json`
  carries `output: ""` and points at the twelve per-seat reports.
- **E7 gate-receipts** — `corpus/evidence/round69/gates/depth-gate.txt` and
  `corpus/evidence/round69/gates/trio.txt` exist and equal a fresh run of their commands
  (`plans/round63_gate_checks.py depth … --root .` and `… trio <entry>`) byte for byte.

**Kill rule.** Any `E<n> defect` line at the landing tip fails the predicate; a correction
that exists only as prose with no re-deriving check is not a closed defect.

**Before → after target.** `python3 plans/round69_c2_routed_defects.py` → `DEFECTS n=7`,
`PREDICATE R69-C2 fail`, rc 1 at base (receipt `.ufo/waves/round-69/c2-red-before.txt`) →
`DEFECTS n=0`, `PREDICATE R69-C2 pass`, rc 0 at the landing.

**Controls (committed).** `--selftest --work <scratch>` builds the pre-correction state from
the real files by construction (registry rows stripped, criterion absent, no provenance file,
one `verified-at:` line, correction lines removed, no receipts): it must print
`defects-in-fake=7 want=7 all-fail=True`, and a stale-receipt arm must leave E7 red. A check
that cannot fail refuses the gate.

**Do-nothing control.** The red-before run *is* the do-nothing measurement: the base bytes
satisfy none of E1–E7, so a round that lands nothing scores exactly `n=7`.

## Freeze scope and close

Frozen by this commit: `plans/round69_c1_nginx_probe.py`,
`plans/round69_c2_routed_defects.py`, this document, the wave spec and validated dispatch,
`census-before.txt`, `c2-red-before.txt`, `nginx-control.txt`. No predicate, case table,
vector, kill rule or target changes after this commit; an error found after data is an honest
miss or a dated amendment before any after-receipt is scored.

At close, re-derive both predicates from the committed bytes and record: the C1 receipt, the
C1 selftest tally, the C2 green run, the C2 selftest tally, the census exit, the depth and
trio receipts (E7), and the class-row count.

## Amendment A1 (round 69, dated 2026-11-03; no frozen element changed)

1. **R69-C1's verdict is a MISS.** The battery ran at the frozen instrument (`b288e8e0`) and
   produced `LEG-COVERAGE legs=8 seen_p=8 seen_f=6` → `PREDICATE R69-C1 fail` (rc 1), because
   `test_nginx_running` and `test_custom_404_page` are `P` in all five frozen cases. The sentence
   above — "Each of the eight legs has one red witness and four green witnesses by construction"
   — is arithmetically false: the five vectors carry six reds, not eight. The kill rule names
   exactly this, so the miss is reported, not re-scored: the case table, the vectors, the kill
   rule and the target are **not** changed after data. The member is **not** counted in the SKILL
   class row (it stays `executed 2 of 8`, with the replay and the MISS named).

2. **Instrument repair (mechanical, not a rule change).** Three defects the wave's seats found are
   repaired in `plans/round69_c1_nginx_probe.py` (v1 sha `66b5128d…0100ea` → v2 sha
   `0f491333…d6d7`):
   - `check_receipt` required exactly 5 `VECTOR` tokens; the writer emits 6
     (`VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True`), so every genuine receipt was refused
     (ReceiptReview M-A; NginxBattery run 2). It now parses the 6-token form and verifies the
     `expected` field equals the observed vector.
   - `port_free` bound without `SO_REUSEADDR`, so a TIME_WAIT socket from the preceding battery
     refused a free port (`SETUP port-8080-occupied` with no listener; ReceiptReverify result 6).
   - `--selftest` gains an acceptance arm on a synthetic full-coverage table: the five red
     fixtures had all been refused through the parser defect, so `red_refused=5/5` proved nothing
     (ReceiptReview §2).
   No predicate, case table, vector, kill rule or target changes. The v2 battery re-ran the same
   five frozen cases (third independent run) and reproduced every vector; its receipt
   (`corpus/evidence/round69/nginx/receipt-v2.txt`) still prints `PREDICATE R69-C1 fail` on the
   two leg-coverage defects. The v1 receipt is preserved at
   `corpus/evidence/round69/nginx/receipt-v1-checker-broken.txt`.

3. **Frozen-table defects carried to round 70.** The re-freeze needs a `server: False` case field
   (leg 2 red; `run_case` currently aborts at the READY-wait) and a case that mutates the
   `notfound` body (leg 4 red; the field exists). `case_sha256` must digest only the staged inputs,
   not the server-written access log, before it can serve as a staged-state identity.

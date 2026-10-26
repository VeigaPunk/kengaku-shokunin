# R40ConnPattern — cross-claim pattern finding (kengaku round 40, wave 1)

Seat: R40ConnPattern (connector, leaf). Date: 2026-10-26.
Question: do the lane's own instruments carry the shapes the round is falsifying elsewhere —
the db-wal grader checking only a subset of cells (22/33) and never checking the repair step,
and the tripwire survivor classes 'bound loosened by one', 'prefix vs exact', 'one mode never
exercised', 'refusal folded into a verdict'?

Instruments read in full: plans/round40_c1_verify.py, plans/round40_c2_verify.py,
plans/db_wal_probe.py, plans/tip_receipts.py, plans/sources_adopt.py,
plans/anchor_digest_check.py, plans/ledger_tip.py, plans/order_check.py,
plans/round39_c1_verify.py (head+MUTANTS), plans/round39_c2_verify.py (head/V1-V7),
corpus/evidence/round40/db-wal-probe.txt, corpus/evidence/round40/tb2-db-wal-recovery/
(test.sh, task.toml), plans/pkg-spec-r40.json.

Grounding commands (run at the lane tip):
- `grep -c "^CASE " corpus/evidence/round40/db-wal-probe.txt` → 28; `grep -m1 "^cases=" …` →
  `cases=28 observed_pass=8 observed_fail=20 mismatches=0`; `grep -c "match=NO" …` → 0.
- `ls corpus/evidence/round40/tb2-db-wal-recovery/` → 8 files; `db_wal_probe.py:61-66` PINS → 4.
- `python3 -c "import json; …"` on plans/pkg-spec-r40.json → spec rows carry only
  {capture, upstream, sha256} for S119/S120.

Nothing below edits a frozen file. Findings are grouped by shape; each carries file:line and a
one-line fixture that would expose it. Declared/deliberate instances are marked — they are still
the same shape, and the lane's own rule (considerthese 2026-10-26 lesson 3) is that a shape is
worth naming before it bites.

---

## Shape 1 — check only a subset of the cells/artefacts (db-wal 22/33 analogue)

**S1. round40_c2_verify.py V3 checks 1 of 11 registry cells.**
`toks = re.findall(r"sha256\s+([0-9a-fA-F]+)", found[0][5])` (round40_c2_verify.py:149); the
other test is only `len(found[0]) != 11` (:147). Cells 0-4 and 6-10 of the S119/S120 rows are
never compared against anything — the spec rows carry no other field to compare
(pkg-spec-r40.json rows = {capture, upstream, sha256}), and V6 (`census validate`) checks census
shape, not row content. Fixture: in a scratch lane, corrupt the `teaches` cell of the S119 row in
corpus/SOURCES.md → V3 still prints ok.

**S2. tip_receipts.py re-runs only the 5 receipts in its RECEIPTS table.**
RECEIPTS (tip_receipts.py:55-60) names 5 receipts; candidates are matched by
`CANDIDATE_RE = probe.*\.(?:txt|log)$` (:47) and everything else is
`skip reason=no-committed-re-run-command` (:226, :327). This round's own receipt,
corpus/evidence/round40/db-wal-probe.txt, matches the candidate regex but is not in RECEIPTS.
Fixture: `python3 plans/tip_receipts.py --lane <clone>` → observe the db-wal receipt skipped;
the instrument that certifies receipt reproduction never reproduces this round's receipt.

**S3. db_wal_probe.py pins and binds 4 of the 8 captured files.**
PINS (db_wal_probe.py:61-66) = test_outputs.py, solve.sh, main.db, main.db-wal.encrypted; the
sandbox ro-binds only test_outputs.py and solve.sh (:269-270). instruction.md, task.toml,
test.sh, Dockerfile are never read by the probe; the C2 counter's V1 pins all 8
(round40_c2_verify.py CAPTURES), so the package sees a file the probe never opens. Fixture:
flip one byte of captured test.sh in a scratch lane → probe output byte-unchanged.

**S4. sources_adopt.py row_defects checks 3 of 11 cells.**
status (cell 7), recheck (cell 9), source-empty (cell 1) only (sources_adopt.py:112-121);
kind/tier/scope/anchor/teaches/opened/used-by are never defect-checked. Fixture: a staged row
with `tier` = `banana` passes the adoption gate clean.

## Shape 2 — one mode never exercised (db-wal "Fix the WAL file" never checked analogue)

**M1. round40_c2_verify.py never re-observes: V5 runs the probe only `--dry`, V4 reads the
receipt verbatim.** v5 (round40_c2_verify.py:194-200) executes `db_wal_probe.py --lane … --dry`
and byte-compares to the frozen table; v4 (:164-190) parses `observed=(pass|fail)` out of the
receipt text (:155-161) and checks only internal consistency (ids vs frozen table, summary
arithmetic, `match=NO` cases named in the entry). No check re-grades a single case — the
observation mode of the probe is exactly as unexercised as the grader's repair step. (Frozen
this round; named as a limit, see proposal.)

**M2. db_wal_probe.py never runs the grader through the task's declared verifier path.**
The captured test.sh runs `uvx -p 3.13 -w pytest==8.8.1 … pytest /tests/test_outputs.py`
(test.sh:9-13); the probe's HARNESS_PY imports test_outputs.py and calls each test function
directly (db_wal_probe.py:232-246) — the pytest collection/assertion-rewriting layer and
test.sh's reward write are never exercised; `--stage-check` deliberately never imports the
grader (claims doc, C2 stage-check note). Fixture: a grader whose tests pass only under pytest's
assertion rewriting grades differently in-image than in-probe, and the probe cannot see it.

**M3. ledger_tip.py reads exactly two ledgers.** LEDGERS (ledger_tip.py:71-74) =
(defects.jsonl, defects-round35.jsonl); any ledger added later is never read. Fixture: add
corpus/defects-round40.jsonl with a failing `open` row → ledger_tip stays green.

**M4. order_check.py detects only two evidence shapes of "probe executed".** `blob_hits`
(order_check.py:96-110) matches GATE_P10 lines and `CASE … observed=` lines only. A probe
receipt committed under claims/ in any other format (e.g. `TEST x P`, `tests=PPPFPF`,
`RESULT pass`) is invisible to the order gate. Fixture: commit a pre-receipt claims file
containing `TEST test_wal_was_decrypted P` → `ORDER ok`.

## Shape 3 — refusal / setup folded into a verdict

**F1. tip_receipts.py folds probe timeout and missing-interpreter into verdict `differ`.**
run_probe returns `{"exit": "timeout"}` / `{"exit": "missing"}` (tip_receipts.py:177-179); the
verdict loop then does `if run["exit"] != 0: res["verdict"] = "differ"` (:280-282), and the run
exits 1 on any differ (:347). `differ` asserts the committed receipt bytes do not reproduce; a
timeout asserts nothing about bytes. This is the exact 'refusal folded into a verdict' class the
frozen L21/O04 mutants target in the tripwires — present in the lane's own receipt certifier.
Fixture: `python3 plans/tip_receipts.py --lane <clone> --timeout 1` → tb2_grader_probe (uv fetch)
reports `differ`, exit 1, on a perfectly reproducible receipt.

**F2. tip_receipts.py's tamper control silently does not run when nothing graded equal.**
`controls = [min(equal, …)] if equal else []` (tip_receipts.py:306-307) with `control_ok = True`
(:309): the one falsifier the instrument carries (a flipped byte must report differ) is absent on
a fully-red run, and no line records that absence. Fixture: a clone where all 5 receipts differ
→ run ends with zero `control receipt=` lines and control_ok=True.

**F3. ledger_tip.py folds any check crash into observed=fail — declared and mutation-tested.**
`except subprocess.CalledProcessError → refuse` (ledger_tip.py:224-227) vs
`except Exception → ok, note = False, "error …"` (:228-229, comment "a crash is an observed
failure, never a pass"). For a `closed` row a crash prints `observed=fail agree=NO` —
indistinguishable in the agree column from a genuine red check; the error note survives only on
fail or with --keep-notes. Deliberate (frozen mutant L14 kills the laxer direction); listed as
the measured boundary of the fold, not a defect.

**Contrast (clean refusal, same instrument family):** db_wal_probe.py aborts the whole run as
SETUP on the first case that fails to yield 14 verdicts (:361-364, `return 2`) — the safe
direction the lane intends.

## Shape 4 — bound / prefix-vs-exact carve-outs in the instruments themselves

**B1. round40_c1_verify.py classes() skips any ORDER FAIL line containing " hits=".**
`if m and " hits=" not in line` (round40_c1_verify.py:347) — the counter parses the tool's named
fail lines but carves out the summary line by substring. Today's tool prints them on separate
lines so the exclusion is exact (the withdrawn-equivalent O13 was caught pre-freeze by the same
kind of analysis). Fixture: a mutant order_check that appends ` hits=0` to a named-fail line is
scored by the counter against an empty defect set.

**B2. round40_c1_verify.py path_ok validates only absolute tokens.** `if cand.startswith("/")`
(round40_c1_verify.py:328); the contract says "every absolute path in the argv must lie inside
d", so relative tokens pass unvalidated while the tool runs with `cwd=str(fx["dir"])` (:380) —
`../…` from the fixture dir reaches the module dir. The escape is bounded (still under
root/fx/<module>/), so impact is cross-fixture contamination, not lane escape. Fixture: a
fixture whose argv carries `../f000-shared` → path_ok green.

**B3. sources_adopt.py locates() is substring presence, not location.** `needle in text`
(sources_adopt.py:401); the docstring admits "a row that cites a repository root is satisfied by
any capture declared against that root" (:336-341, the round-31 C3 finding restated). A quote
binds wherever it occurs in the artifact, whatever the row's cited line/section. Fixture: a
capture of the wrong section that happens to contain the quoted sentence greens the row.

**B4. tip_receipts.py CANDIDATE_RE is a substring match, not a name shape.**
`probe.*\.(?:txt|log)$` (tip_receipts.py:47) matches any basename containing "probe" — including
`xprobe-notes.txt` or `probes.log`; conversely the RECEIPTS table then decides coverage by exact
rel-path (S2). The candidate set is defined loosely, the covered set strictly. Fixture: rename
a receipt to `aprobe.txt` → it becomes a candidate and is reported `skip` as unmapped, changing
the instrument's printed denominator.

---

## Affected axes

- **Calibration (primary):** F1/B1/B2 sit in the instruments that certify calibration artefacts
  (tip_receipts, the C1 counter's parser); if they misfold, a calibration receipt can be misread
  the same way the db-wal grader misreads the repair step. S1/M1 sit in the C2 counter, which is
  this round's judge for coverage.
- **Coverage:** S2/S3/M2 are coverage-shaped holes in the lane's own evidence chain (receipts
  never reproduced; captures never opened; verifier path never run).
- **Operability:** F1/F2 produce misleading red/green on slow or offline hosts.

## Proposed move (one, bounded — for the L1; nothing frozen changes)

Draft routed lesson for `corpus/lessons/` (round-40 file, L1 integrates): name the four shapes
as a standing checklist for every future counter/probe, with the two cheap repairs that are
admissible after this freeze —
1. tip_receipts (NOT frozen): distinguish setup outcomes (`timeout`/`missing`) from byte
   `differ` in the verdict line, and run the tamper control on the smallest receipt regardless
   of its verdict (F1, F2). Both are output-line changes; the frozen receipts' byte-equality
   verdicts are unaffected.
2. New counters (round 41+; M1 is frozen for r40): either re-observe a sample of receipt cases
   in the counter, or record in the counter docstring that observed values are trusted verbatim
   from the receipt (the same "probed instance only" disclaimer the C2 entry already uses for the
   destructive-read trap).
Risks: (1) changes tip_receipts output lines that round-38/39 receipts quote — needs a
receipt-note in the round-40 lesson, not a re-run; (2) re-observing in-counter costs ~1 min/case
and toolchain parity (the C2 claims doc already names the host-stand-in limit).
Verification for (1): run tip_receipts on a clone with `--timeout 1` and with a flipped-byte
control on a `differ` receipt; both must print a non-differ setup verdict / a control line.

## Notes

- All receipt numbers above were verified against the committed receipt
  (corpus/evidence/round40/db-wal-probe.txt, grep output quoted in Grounding).
- Deliberate instances (F3, M1-frozen, the SETUP abort contrast) are flagged so the L1 can
  route them as documentation, not fixes.
- Peer overlap: R39ConnSibling is triaging sibling lanes for the same instruments; these sites
  are all in this lane's plans/ and need no sibling data.

VERDICT: pattern-14-sites (subset-4: round40_c2_verify.py:149, tip_receipts.py:55-60+47, db_wal_probe.py:61-66+269-270, sources_adopt.py:112-121; skipped-mode-4: round40_c2_verify.py:194-200+164-190, db_wal_probe.py:232-246+test.sh:9-13, ledger_tip.py:71-74, order_check.py:96-110; folded-refusal-2: tip_receipts.py:177-179+280-282, tip_receipts.py:306-309; bound-prefix-4: round40_c1_verify.py:347, round40_c1_verify.py:328+380, sources_adopt.py:401, tip_receipts.py:47)

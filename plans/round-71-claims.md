# Round 71 — kengaku — frozen claims (hyaku run 15, attempt 1)

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`. Base tip at freeze:
`1cb49cac52999475de35f8955d5c01f2ddb66ccf`. Date: 2026-11-03.

Two claims, one axis each, causally separable: **R71-C1 coverage** (the lowest owned non-retired
axis, held at its L0 cap `kengaku | round-25/33/51`) and **R71-C2 calibration** (held at ceiling
10, exercised). Everything below is frozen before any battery runs; a seat that thinks a rule is
wrong reports it and does not edit it.

---

## R71-C1 — coverage: the `hf-model-inference` TB2 grader replayed offline

**Claim sentence (frozen).** The `hf-model-inference` Terminal-Bench 2.0 grader (pin
`2fd12b88`, sha256 `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857`) is replayed
offline under an eight-case frozen table in which **every one of its four legs is witnessed both
`P` and `F`**, every case's derived vector equals its frozen vector, and the receipt's digests
re-derive from committed bytes — moving the `network-service` class row in `SKILL.md` from
`executed 3 of 8` to `executed 4 of 8` (`hf-model-inference` being the fourth executed member).

**Why this is frontier ground.** The census (`corpus/evidence/round62/class-survey.txt:11`) lists
eight `network-service` members; rounds 64/68/70 executed three (`kv-store-grpc`, `pypi-server`,
`nginx-request-logging`). `hf-model-inference` was refused in round 36 as "service + network"
(`.ufo/waves/round-36/build/R36ScoutNextTasks.md:41`) — the service half is discharged by the
lane's shim-on-loopback recipe; the model-load half is priced below.

**Frozen case table** (`plans/round71_c1_hf_probe.py` `CASES`/`VECTORS`; legs in file order
`test_model_downloaded`, `test_flask_api_running`, `test_sentiment_endpoint`,
`test_api_error_handling`):

| case | model stage | service stage | expected | what it prices |
|---|---|---|---|---|
| K1 | `good` | `good` | `PPPP` | all four legs green |
| K2 | `good` | `wrong-label` | `PPFP` | L3 red: the "not bad" text answered negative |
| K3 | `good` | `int-confidence` | `PPFP` | L3 red: confidence scores are ints, not floats |
| K4 | `good` | `no-400` | `PPPF` | L4 red: a body without `text` answered 200 |
| K5 | `good` | `root-drops` | `PFPP` | L2 red: `/` closes the connection, `/sentiment` works |
| K6 | `good` | `none` | `PFFF` | L2/L3/L4 red: no service listens |
| K7 | `absent` | `good` | `FPPP` | L1 red: no model directory |
| K8 | `corrupt` | `good` | `FPPP` | L1 red: `from_pretrained` raises on the staged bytes |

**Frozen predicate (the exact sentence).** `PREDICATE R71-C1 pass` iff the receipt of record
carries, for all eight cases, a `VECTOR` line whose `derived` equals the frozen vector with
`agree=True`; a `LEG-COVERAGE` line with `legs=4 seen_p=4 seen_f=4`; `SUMMARY cases=8 legs=32
mismatches=0 setup=0`; `GRADER`, `INSTRUCTION`, `MODEL`, `PROBE` and `PROBE_BLOB` digests that
re-derive from the committed bytes at the lane tip; and `--check-receipt` exits 0.

**Counting command.** `python3 plans/round71_c1_hf_probe.py --lane . --work <scratch>
--receipt corpus/evidence/round71/hf/receipt.txt --evidence-dir corpus/evidence/round71/hf/sandbox`
then `python3 plans/round71_c1_hf_probe.py --lane . --check-receipt
corpus/evidence/round71/hf/receipt.txt --work <scratch>`; the class-row counters are
`grep -c 'executed 3 of 8' SKILL.md` → 0 and `grep -c 'executed 4 of 8' SKILL.md` → 1 after.

**Kill rule.** One case with `agree=False`, one `setup` failure (port busy, sandbox rc≠0, or a
harness that prints no `LEGS-JSON`), or one leg without both witnesses fails the predicate — no
silent retry, no reselect of cases after data. A `SETUP` case is a failure, never a skip.

**Do-nothing control (committed at freeze).** The same eight case ids staged with **no model and
no service** must derive `FFFF` in every case and the counter must print `PREDICATE R71-C1 fail`.
If the control prints pass, the counter or the target is wrong and no battery is scored.

**Named limitations, declared before data.** (i) The candidate is a lane-written stdlib HTTP
server standing in for the Flask app the task asks for (the class recipe: the probe supplies the
end state, the grader's own `requests` calls decide). (ii) `transformers`/`torch` come from this
host's existing `/fast/ComfyUI/.venv` bound read-only — the task image's own versions are not
reproduced; the receipt records the exact versions and the checker re-derives them. (iii) The six
texts and their expected labels are the grader's own constants, so the replay prices the grader's
logic, not a model's accuracy; the staged model is a tiny random-weight fixture that loads, not
distilbert. (iv) `test_flask_api_running` accepts any HTTP answer from `0.0.0.0:5000` (no status
check) — K5 exercises the only failing mode a live listener can have. (v) `--check-receipt` is a
consistency check over committed bytes, not proof of a live run; the per-case sandbox captures
under `corpus/evidence/round71/hf/sandbox/` are the live witness.

---

## R71-C2 — calibration: the round-70 closure's two routed defects, re-derived

**Claim sentence (frozen).** The round-70 non-author closure's routed defects **R70-D1**
(`Mistakes`-row count drift: `LOG.md` "five rows", `corpus/README.md` "six Mistakes rows" in the
supporting block, and the lesson index row naming six of eight) and **R70-D2** (the nginx entry's
sentence citing `instruction.md:6-11` for the two HTTP bodies, which are at `:15-18`) are closed
by corrections that a re-deriving gate moves from `DEFECTS n≥2` to `DEFECTS n=0`, with the gate
killed 4/4 under single-check deletion.

**Two defects, two fix shapes (append-only corpus norm).**
- D1: an append-only `LOG.md` correction entry (dated, naming R70-D1, quoting the superseded
  "five rows" text and stating eight); both `corpus/README.md` mentions corrected to eight
  `Mistakes rows` naming all eight row classes; an appended `## Errata` block in
  `corpus/lessons/round-70.md` naming the under-sweep.
- D2: an appended `## Errata` block in
  `corpus/knowledge/tb2-nginx-request-logging-offline.md` naming `E-D2`, quoting the superseded
  sentence verbatim and stating the corrected range `instruction.md:6-11,15-18`; the original
  sentence stays as written.

**Frozen predicate (the exact sentence).** `PREDICATE R71-C2 pass` iff
`python3 plans/round71_c2_routed_defects.py --lane .` prints `E1a ok`, `E1b ok`, `E1c ok`,
`E2a ok`, `DEFECTS n=0` and exits 0 at the round tip; `--selftest --work <scratch>` prints
`defects-in-fake=4 want=4 all-fail=True` with the append-only arm true; `--mutants --work
<scratch>` prints `MUTANTS total=4 killed=4 survived=0`.

**Checks (each re-derives from committed bytes, no stored tally).**
- `E1a` the round-70 lesson's `## Mistakes` data-row count is 8 and the eight class keys are
  present;
- `E1b` `LOG.md` carries a dated R70-D1 entry that quotes the superseded "five" and states eight;
- `E1c` every README mention of round-70 Mistakes rows says eight and names all eight classes,
  and no unsuperseded wrong count remains;
- `E2a` the nginx entry keeps the superseded sentence verbatim and carries an `## Errata` block
  naming `E-D2`, `supersedes` and `instruction.md:6-11,15-18`.

**Kill rule.** Any check that prints a defect fails the predicate. A rule changed after a seat has
scored is not the claim's rule. The gate's own selftest must build a fake lane that fails all four
checks and a corrected fake that passes, and the append-only arm must show a rewritten sentence
hides the defect on red bytes (the rule is that the original stays).

**Red-before (committed at freeze).** `.ufo/waves/round-71/c2-red-before.txt` records the gate at
the base tip: `DEFECTS n=6`, `PREDICATE R71-C2 fail`.

---

## Round-level

- **Axes.** C1 → coverage (before 7, held at the L0 cap after: the move is evidence-carried), C2
  → calibration (before 10, held at ceiling, exercised). No other axis is targeted and none may be
  harmed; the round report carries the per-axis check.
- **Sourced claim.** C1 rests on S245 (`hf-model-inference/instruction.md` at the pin) and S246
  (`hf-model-inference/tests/test_outputs.py` at the pin), both opened live this round with access
  date, byte count, sha256 and a located ≤25-word quote; both rows are appended to
  `corpus/SOURCES.md` in `mined` status with `used-by` naming the round-71 entry.
- **Capability.** No new capability row is claimed: the replay re-exercises
  `offline-network-service-grader-probe` (round 68). A capability row enters only if a
  demonstration passes its frozen predicate — that is not this round's target.
- **Out of scope, named before data.** No model behaviour is measured; no live endpoint is
  contacted; no sibling lane is touched; `merge/kengaku` adoption is `Assimilation: none` (one
  entry considered, verdict in the lesson `## Gate`).

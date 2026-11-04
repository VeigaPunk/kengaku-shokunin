# Round 72 — kengaku — frozen claims (hyaku run 15, attempt 1)

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`. Base tip at freeze:
`c63229724893c40b11661194ef1dff2987c177e9` (round-71 verifier spot-check tip). Date: 2026-11-03.

Two claims, one axis each, causally separable: **R72-C1 coverage** (the lowest owned non-retired
axis, held at its L0 cap `kengaku | round-25/33/51`) and **R72-C2 calibration** (held at ceiling
10, exercised). Everything below is frozen before any battery runs; a seat that thinks a rule is
wrong reports it and does not edit it.

---

## R72-C1 — coverage: the `hf-model-inference` replay gains a provenance witness and the ninth case

**Claim sentence (frozen).** The `hf-model-inference` Terminal-Bench 2.0 grader (pin `2fd12b88`,
sha256 `61a686d6…87857`) is replayed offline under a **nine-case** frozen table in which every one
of its four legs is witnessed both `P` and `F`, the ninth case (`K9` `400-no-error-field`,
`PPPF`) prices the `assert "error" in error_data` site at `tests/test_outputs.py:107` that the
round-71 eight-case table could not reach, and the sandbox is proven isolated: it runs under
`bwrap --clearenv` with an explicit nine-variable allowlist and records its **own**
`transformers.__file__`, so the same `transformers` stub that changed the round-71 table on the
parent `PYTHONPATH` is invisible here.

**Why this is frontier ground.** Round 71 admitted R71-C1 at *leg* granularity and named three
carried limits: two defective `--selftest` arms (R71-R4), an inherited sandbox environment that
let a stub reproduce 8/8 vectors (R71-R6, `ClaimFalsify71` §C1-b), and the one reachable assert
gap `CaseTableAudit71` proposed (K9). This round closes all three on the same instrument, so the
`network-service` evidence it produces is the first in this lane whose model-load witness is a
provenance check rather than an outcome check.

**Frozen case table** (`plans/round72_c1_hf_probe.py` `CASES`/`VECTORS`; legs in file order
`test_model_downloaded`, `test_flask_api_running`, `test_sentiment_endpoint`,
`test_api_error_handling`):

| case | model stage | service stage | expected | what it prices |
|---|---|---|---|---|
| K1 | `good` | `good` | `PPPP` | all four legs green |
| K2 | `good` | `wrong-label` | `PPFP` | L3 red: the "not bad" text answered negative |
| K3 | `good` | `int-confidence` | `PPFP` | L3 red: confidence scores are ints, not floats |
| K4 | `good` | `no-400` | `PPPF` | L4 red: a body without `text` answered 200 (`:103`) |
| K5 | `good` | `root-drops` | `PFPP` | L2 red: `/` closes the connection, `/sentiment` works |
| K6 | `good` | `none` | `PFFF` | L2/L3/L4 red: no service listens |
| K7 | `absent` | `good` | `FPPP` | L1 red: no model directory |
| K8 | `corrupt` | `good` | `FPPP` | L1 red: `from_pretrained` raises on the staged bytes |
| K9 | `good` | `400-no-error-field` | `PPPF` | L4 red: 400 with a body lacking `error` (`:107`) |

**Frozen predicate (the exact sentence).** `PREDICATE R72-C1 pass` iff
`python3 plans/round72_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round72/hf/receipt.txt
--work <scratch>` prints `DEFECTS n=0` and `PREDICATE R72-C1 pass` and exits 0 at the round tip;
the receipt of record carries nine `VECTOR` lines with `agree=True`, `LEG-COVERAGE legs=4
seen_p=4 seen_f=4`, `SUMMARY cases=9 legs=36 mismatches=0 setup=0`, and a `PROVENANCE` line with
`env_cleared=True`, `allowlist_seen=9/9`, `distinct=1`, `canary_seen=0` and a `transformers_file`
under `/venv/`; and the `--stub-control` receipt prints `STUB-CONTROL exposed=False
vectors_unchanged=True`.

**Counting commands.**
1. `python3 plans/round72_c1_hf_probe.py --lane . --work <scratch>/battery --receipt
   corpus/evidence/round72/hf/receipt.txt --evidence-dir corpus/evidence/round72/hf/sandbox
   --port-lock <scratch>/port5000.lock`
2. `python3 plans/round72_c1_hf_probe.py --lane . --check-receipt
   corpus/evidence/round72/hf/receipt.txt --work <scratch>/check`
3. `PYTHONPATH=<scratch>/stub python3 plans/round72_c1_hf_probe.py --lane . --work
   <scratch>/stub-battery --receipt corpus/evidence/round72/hf/stub-control.txt --stub-control`

**Kill rule.** One case with `agree=False`, one `setup` failure (port busy, sandbox rc≠0, a
harness that prints no `LEGS-JSON`), a `PROVENANCE` line that is absent/duplicated/outside
`/venv/`, a `canary_seen` count above 0, or a stub control that exposes the stub fails the claim
— no silent retry, no reselect of cases after data. A `SETUP` case is a failure, never a skip.

**Do-nothing control.** The same nine case ids staged with **no model and no service** must
derive `FFFF` in every case and the counter must print `PREDICATE R72-C1 fail`
(`.ufo/waves/round-72/c1-control.txt`). If the control prints pass, the counter or the target is
wrong and no battery is scored.

**Named limitations, declared before data.** (i) The candidate is a lane-written stdlib HTTP
server standing in for the Flask app the task asks for (the class recipe). (ii) `torch` and
`transformers` come from this host's `/fast/ComfyUI/.venv` bound read-only; the task image's
versions are not reproduced, and `LIBRARIES` is measured on the host by design (the sandbox
records only the file it loaded). (iii) The staged model is a five-file synthetic fixture, not
`distilbert-base-uncased-finetuned-sst-2-english` (S248): the replay prices the grader's logic,
not a model's accuracy. (iv) `test_flask_api_running` accepts any HTTP answer (no status check);
K5 prices the only failing mode a live listener can have. (v) `--check-receipt` is a consistency
check over committed bytes: a hand-written receipt with a self-consistent `PROVENANCE` line still
passes it, so the per-case sandbox captures are the live witness. (vi) K9 prices one assert site,
not the leg as a whole; five assert groups remain red-unreachable under the frozen modes.

---

## R72-C2 — calibration: the round-71 closure's routed defects R71-R1 and R71-R7, re-derived

**Claim sentence (frozen).** The round-71 non-author closure's routed defects **R71-R1** (neither
round-71 instrument has a `SKILL.md` `## Gate/probe registry` row) and **R71-R7** (two
`plans/round-71-claims.md` labels claim a freeze-commit content the freeze commit does not hold)
are closed by corrections that a re-deriving gate moves from `DEFECTS n=6` to `DEFECTS n=0`, and
the gate's own mutation metric — the one R71-R5 showed was invariant — is replaced by a fixture
matrix that kills six semantic mutants, reports a deliberate no-op as `null_detected=1`, and
attributes every kill.

**Two defects, two fix shapes (append-only corpus norm).**
- R71-R1: four eight-column rows appended to `SKILL.md` `## Gate/probe registry` — the two
  round-71 instruments and the two round-72 instruments — each naming its entry command, verdict
  map, self-test spelling, pinned values, write scope and owner.
- R71-R7: an appended `## Errata — round 72` block in `plans/round-71-claims.md` that keeps both
  superseded sentences verbatim above it and states the true revisions (`c80fcdb3` for the
  control; `d8a77d3f` for the red-before receipt, produced by the freeze instrument).

**Frozen predicate (the exact sentence).** `PREDICATE R72-C2 pass` iff
`python3 plans/round72_c2_routed_defects.py --lane .` prints `E1a ok`, `E1b ok`, `E1c ok`,
`E2 ok`, `DEFECTS n=0`, `PREDICATE R72-C2 pass` and exits 0 at the round tip;
`--selftest --work <scratch>` prints `SELFTEST defects-in-fake=3 want=3 all-fail=True
append-only-arm=True positional-arm=True parser-arm=True`; and `--mutants --work <scratch>`
prints `MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1` with
`ARM accept-green=ok refuse-red=ok attribution=ok`.

**Checks (each re-derives from committed bytes, no stored tally).**
- `E1a` every instrument in `INSTRUMENTS` has an eight-column `SKILL.md` registry row whose entry
  cell names its script, whose kind is `gate`/`probe`, and whose owner is `kengaku`;
- `E1b` the round-71 claims doc carries an appended erratum quoting both superseded labels
  verbatim and naming both true revisions;
- `E1c` `parse_count` coerces a digit `8`, a plain word, a backticked word and an embedded phrase,
  and returns `None` when there is no count (the R71-R5 false-red class);
- `E2` positional append-only: both superseded sentences still occur **above** the erratum, and
  the erratum is the file's last `##` section.

**Kill rule.** Any check that prints a defect fails the predicate. A rule changed after a seat has
scored is not the claim's rule. The gate's selftest must build a fake lane that fails all three
fixture-driven checks (`E1a`, `E1b`, `E2`) and a corrected fake that passes, plus the append-only,
positional and parser arms; the mutant matrix must kill six semantic mutants and flag the no-op.

**Red-before.** `.ufo/waves/round-72/c2-red-before.txt` records the freeze instrument reading the
base tree: `DEFECTS n=6` (four `row-absent`, `E1b no-errata-section`, `E2 no-errata-section`),
`PREDICATE R72-C2 fail`. This is a red-*data* run with the freeze instrument, labelled as such.

---

## Round-level

- **Axes.** C1 → coverage (before 7, held at the L0 cap after: the move is evidence-carried), C2
  → calibration (before 10, held at ceiling, exercised). No other axis is targeted and none may be
  harmed; the round report carries the per-axis check.
- **Sourced claim.** C1 rests on S245/S246 (round 71, re-opened this round by the wave's source
  seat) and on two rows opened this round: S247 (the `bwrap(1)` manual's `--clearenv` semantics,
  which is the mechanism) and S248 (the model card of the checkpoint the task names, which bounds
  limitation iii). Each new row carries its access date, byte count, sha256 and a located
  ≤25-word quote in `corpus/lessons/round-72.md` `## Gate`.
- **Capability.** No new capability row: the replay re-exercises
  `offline-network-service-grader-probe` (round 68), and `hf-model-inference` is already counted
  as the fourth executed member.
- **Out of scope, named before data.** No model behaviour is measured; no live model endpoint is
  contacted; no sibling lane is touched; `merge/kengaku` adoption is `Assimilation: none` (one
  entry considered and refused, reason and flip in the lesson `## Gate`).

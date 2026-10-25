# R35ConnSibling — Sibling-Overlap Scan, Round 35 Surfaces

**Seat:** R35ConnSibling (connector, leaf)
**Round:** kengaku round 35 (hyaku run 7, 2026-10-25), WAVE 1 of 2
**Axis:** adjacency
**Report target:** `.ufo/waves/round-35/build/R35ConnSibling.md`
**Access date for every sibling file read:** 2026-10-25
**Read-only scan:** no sibling file was edited; no git/jj mutation; no tools installed or upgraded (grep/read/python only).

## 1. Scope and method

Round-35 surfaces scanned for sibling overlap:

- **S1 — benchmark grader code / Terminal-Bench:** pinned Terminal-Bench 2.0 `protein-assembly` grader (`tests/test_outputs.py`, `tests/test.sh`, `instruction.md`) admitted as `corpus/knowledge/tb2-protein-assembly-grader.md` (S105–S107) with an executed offline probe (`plans/tb2_grader_probe.py`, 18 frozen cases; receipt `corpus/evidence/round35/tb2-grader-probe.txt`).
- **S2 — routed-defect ledgers:** persistent routed-defect ledger `corpus/defects.jsonl` + checker `plans/defect_ledger.py` closing D1–D5 (round-34 spot-check).

Sweep: all 21 `*-shokunin` lane repos; read `PROVINCE.md` and `corpus/README.md` for every lane (the files named in the dispatch), plus targeted reads of `SKILL.md`/`corpus/knowledge/` where a hit needed disambiguation.

**Findings summary:** zero sibling lanes claim benchmark-grader code, Terminal-Bench, a persistent routed-defect ledger, or a matching receipt validator for these surfaces. Every lane whose province text touches an eval/verification boundary either refuses model-evaluation claims (routing them to kengaku), or holds a *different* verification craft (mutation-fixture craft; receipt attestation/canonicalization; claim-vs-source research method) that is complementary, not conflicting. Four lanes named in the dispatch (tameshi, kotoba, kumitate, chousa) plus three further lanes with explicit boundary clauses (kama, kasegi, kagi) are **adjacent**; the remaining fourteen lanes have no overlap.

## 2. Freshlane-by-lane evidence (PROVINCE.md / corpus/README.md rows)

### 2.1 Benchmark grader code / Terminal-Bench (S1)

| Lane | Evidence | Ruling |
|---|---|---|
| chousa | `PROVINCE.md:10-11`: "**Refuses:** … model-quality or evaluation claims (→ kengaku)". `corpus/README.md:694`: "phrase match, not a judgment that a record is in model-quality scope." | **Adjacent** — explicitly cedes all model-evaluation/quality claims to kengaku; its `verify-*` gate is a research-record verification method, not a benchmark grader. |
| kasegi | `PROVINCE.md:50`: "kengaku — LLM evaluation and benchmarks" (§Adjacent routing row). No Terminal-Bench/Harbor/grader bytes anywhere in the lane. | **Adjacent** — routes benchmark evaluation to kengaku; no grader code. |
| kama | `PROVINCE.md:40`: "**Refuses:** model quality/eval (kengaku) …". `PROVINCE.md:41-43`: boundary rule — kama answers "is the thing at this baseURL the model this config believes it is, right now", never "is the model good". | **Adjacent** — serving/endpoint health, not evaluation; explicitly refuses model quality. |
| kotoba | `PROVINCE.md:59`: kengaku row of the sibling census — "kengaku keeps measured capability effects of prompt format, kotoba owns the craft rules". No benchmark/grader code. | **Adjacent** — prompt/skill craft; evaluation measured effects stay with kengaku. |
| kumitate | `PROVINCE.md:27`: "Prompt and skill craft → kotoba. Research method → chousa." No grader/benchmark surface. | **Adjacent** — orchestration/tooling; no eval ground. |
| tameshi | `PROVINCE.md:14-17`: "**Refuses:** product domains — every lane's gate remains its own; tameshi owns only the reusable craft". `PROVINCE.md:3-5`: "verification-fixture craft — the reusable method of honest checks: hermetic suites, mutation testing, fail-closed arms, verdict-line discipline …". | **Adjacent** — reusable verification *method*; explicitly refuses product-domain gate code. No benchmark grader. |
| All other 14 lanes (audio, game-dev-2d, game-dev-3d, kaidoku, kake, kagi, kotodama, lore, mado, mori, revenger, souji, tabi, tsukuroi) | Zero mentions of Terminal-Bench, Harbor, `protein-assembly`, or benchmark-grader code in `PROVINCE.md`/`corpus/README.md`. | **None**. |

Fleet-wide negative evidence: `grep` for `terminal-?bench|protein-assembly` across every sibling `PROVINCE.md` → 0 hits (run only inside each lane's own tree). `grep` for `benchmark|grader` across every sibling `PROVINCE.md` → the only hits are kasegi's routing row (`:50`) and kengaku's own rows.

### 2.2 Routed-defect ledgers / receipt validators (S2)

| Lane | Evidence | Ruling |
|---|---|---|
| kagi | `PROVINCE.md:52`: "`corpus/claim-ledger.sh` — calibration gate: verify (91 revision stamps + 65 claim rows) …". This is a **claim ledger for kagi's own scientific claims** (revision stamps + claim rows), not a defect ledger; and it is credential/vault domain. | **Adjacent** — same word "ledger", different object (claim ledger vs defect ledger); calibration-gate pattern. |
| tameshi | `corpus/README.md:49`: "`knowledge/fleet-kill-rate-ledger.md` | standing per-gate view: suite size, kill rate, survivor classes, sweep date, pin; stale successor …". This is a mutation **kill-rate ledger** for the fleet's verification gates, not a routed-defect ledger; it owns the reusable method of "before/after proof" (`PROVINCE.md:3-5`). | **Adjacent** — different ledger object; the reusable verification-fixture craft is the method kengaku's counters use. |
| kumitate | `corpus/README.md:151`: "`knowledge/invocation-attestation.md` | Invocation-receipt attestation design: the M2 prelude-replay class, sidecar-over-whole-file + inner-digest two-layer binding, CLOCK_MONOTONIC spans …". `corpus/README.md:154`: "`knowledge/fail-closed-clock-validation.md` | Fail-closed clock validation for receipt verifiers: the RFC 3339 `date-time` grammar …". `corpus/README.md:156`: "`knowledge/receipt-identity-canonicalization.md` | Receipt identity & the ledger evidence set: a receipt's identity is its canonical-JSON record digest …". Plus `receipt-attest` v2/v3 contract (`knowledge/round-52.md`), `receipt-evidence` capability (`corpus/README.md:174`). | **Adjacent** — this IS a receipt-validator family, but for **orchestration/execution receipts** (invocation attestation, receipt identity, clock validation), not for benchmark-grader probe receipts or defect-ledger receipts. Distinct domain and contract. kengaku should cite kumitate's receipt-identity canonicalization / fail-closed clock-validation design when designing its own tip-receipt validator, rather than re-deriving it. |
| chousa | `corpus/README.md:1056`: "`knowledge/receipt-binding-r38.md` | Round-38 note: receipts bind pre==post gate hashes, counter/expect/receipt digests, verified by a census-tied verifier …". `corpus/README.md:1058`: "`knowledge/receipt-verifier-subject-r39.md` | Round-39 note: receipts bind `verifier_sha256` + `subject_counter_sha256`, re-derived by the verifier …". `corpus/README.md:1059`: "`knowledge/receipt-expectation-digests-r40.md` | Round-40 note: a receipt's `expect_sha256` binds exact expectations-file bytes …". `PROVINCE.md:5-8`: "citation chaining and hop resolution; claim-vs-source verification". | **Adjacent** — research-record receipt verification (claim-vs-source, gate-hash binding). Distinct domain; explicitly refuses evaluation claims. |
| kama | `PROVINCE.md:40-43`: refuses model quality/eval and credential material; owns endpoint health. Its `tests/llamacpp-live/check-receipt.py` (noted in round-34 connector scan) validates service-probe receipts, not benchmark receipts. | **Adjacent** — serving-probe receipt validator, different domain. |
| kotoba | `corpus/README.md:38`: "Independent harness re-derivation (round 37) | `knowledge/harness-independent-round37.md` + `../verifiers/verify_harness_independent.py`". Its verifiers check SKILL.md/frontmatter surfaces, not benchmark grading or defect ledgers. | **Adjacent** — prompt-craft verifier instruments; no overlap with benchmark receipts or defect ledgers. |
| All other 14 lanes | Zero claims of routed-defect ledgers; receipt validators present are domain-specific (kake web-property receipts; souji workspace-hygiene receipts; tabi browser/CDP receipts; kaidoku evidence-ledger discipline; mori census receipts; mado tripwire receipts; tsukuroi system-receipts; kotodama/lore/audio/game-dev worldbuilding/production receipts) — none address benchmark grading or routed defect ledgers. | **None**. |

## 3. Contested scope?

**None.** No sibling lane's `PROVINCE.md` or `corpus/README.md` claims any part of the round-35 C1 (Terminal-Bench 2.0 `protein-assembly` grader / benchmark-grader code) or C2 (persistent routed-defect ledger) surfaces. The only uses of the word "ledger" in sibling lanes refer to different ledger objects (claim ledgers, kill-rate ledgers, orchestration-receipt ledgers). The only "benchmark" mention in a sibling file is kasegi's routing row, which names kengaku as the owner.

## 4. Sibling instruments kengaku should cite rather than duplicate

1. **kumitate — `knowledge/receipt-identity-canonicalization.md`** (`kumitate-shokunin/corpus/README.md:156`): receipt identity = canonical-JSON record digest (RFC 8785), plus `knowledge/invocation-attestation.md` (`:151`) and `knowledge/fail-closed-clock-validation.md` (`:154`). If kengaku builds the tip-receipt validator proposed in `considerthese/2026-10-25.md` proposal 2(c) (every `corpus/evidence/**` receipt re-run and byte-compared), it should model the receipt-identity and attestation layers on kumitate's v2/v3 `receipt-attest` design rather than inventing a new one — while keeping the *replayable-probe* receipt class (like tb2-grader-probe.txt) distinct from historical capture receipts that cannot be re-run.
2. **tameshi — `knowledge/verification-patterns-fleet.md`** (`tameshi-shokunin/corpus/README.md:9`): "the shared verifier shape P1–P10, called general only on ≥2 independent lanes" and the mutation-fixture craft (`PROVINCE.md:3-5`, `tools/mutate-and-run.sh`). kengaku's C1 probe/`round35_c1_verify.py` and C2 `defect_ledger.py` follow this shape; the lane should cite tameshi as the method parent, and tameshi's "before/after proof" rule is what the round-35 controls demonstrate.
3. **chousa — `knowledge/receipt-binding-r38.md` / `receipt-verifier-subject-r39.md` / `receipt-expectation-digests-r40.md`** (`chousa-shokunin/corpus/README.md:1056,1058,1059`): pre==post gate-hash binding and `expect_sha256` digest binding. kengaku's V5 probe-receipt byte-equality check is the same binding class; cite chousa's receipts discipline for the binding semantics (while chousa remains the research-method owner).

## 5. Verification commands (this seat)

- `ls -d /home/vgpnk/Projects/shokunin/*-shokunin/` → 21 lane repos; `*/PROVINCE.md` and `*/corpus/README.md` present in all.
- Python scan over all sibling `PROVINCE.md` + `corpus/README.md` for `terminal-?bench|protein-assembly` → 0 hits outside kengaku.
- Python scan for `benchmark|grader` → only kasegi `PROVINCE.md:50` (routing row) outside kengaku.
- Python scan for `defect` with ledger/routed/jsonl/persist/spotcheck context → lineage of per-round `*-verifier-spotcheck.md` routed defects in every lane (all lanes run the hyaku closure's non-author spot-check pattern); the only *persistent* ledger files found: kengaku's own `corpus/defects.jsonl` (round 35), kagi's `corpus/claim-ledger.sh` (claim ledger), tameshi's `knowledge/fleet-kill-rate-ledger.md` (kill-rate ledger), kumitate's nonce/ledger evidence set in `receipt-identity-canonicalization.md` (receipt ledger).
- Read (targeted): tameshi, kotoba, kumitate, chousa, kama, kasegi, kagi `PROVINCE.md` + `corpus/README.md`; kengaku `plan/round-35-claims.md`, `plans/defect_ledger.py`, `plans/round35_c1_verify.py`, `considerthese/2026-10-25.md`; prior connector reports `round-31/build/R31ConnSibling.md`, `round-32/build/R32ConnSibling.md`, `round-34/build/R34ConnSibling.md`.

Tool installs/upgrades: **none**.

## 6. Counts

- Contested sibling lanes: **0**.
- Adjacent sibling lanes: **7** — chousa, kasegi, kama, kotoba, kumitate, tameshi (all six named/touched by the dispatch's surface list or the lane-set it names) plus kagi (claim-ledger adjacency). All seven have a documented boundary clause in their own `PROVINCE.md`/`corpus/README.md` that either routes evaluation/benchmark ground to kengaku or holds a distinct ledger/receipt object.
- None: the other 14 lanes.

VERDICT: sibling-0-contested-7-adjacent

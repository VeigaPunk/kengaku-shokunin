# R34 Sibling-Overlap Scan & Connector Synthesis

**Seat:** R34ConnSibling (connector, leaf).
**Date:** 2026-10-25.
**Lane repo:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
**Round:** kengaku round 34 (hyaku run 7).
**Report target:** `.ufo/waves/round-34/build/R34ConnSibling.md`.

---

## 1. Sibling Scan across Fleet Lanes

The fleet's 15 sibling lanes (`souji`, `tabi`, `kasegi`, `kaidoku`, `tsukuroi`, `mado`, `kama`, `tameshi`, `mori`, `chousa`, `kake`, `kumitate`, `revenger`, `kotoba`, `kotodama`) were systematically scanned across their `SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `README.md`, `scripts/`, `tools/`, and `plans/` for three declared surfaces:
- **Surface (a):** Anyone reading Terminal-Bench/Harbor scoring code or owning benchmark-grader semantics;
- **Surface (b):** Anyone operating a source-adoption/registry tool like `sources_adopt.py`;
- **Surface (c):** Anyone running defect counters or receipt validators of the same shapes.

### Surface (a): Terminal-Bench / Harbor Scoring Code & Benchmark-Grader Semantics

| Sibling Lane | Findings & Citations | Scope Ruling |
|---|---|---|
| `chousa-shokunin` | `PROVINCE.md:10-11`: `**Refuses:** bounty-program scope and claim packages (→ kasegi); model-quality or evaluation claims (→ kengaku)`. Explicitly cedes model evaluation and quality claims to `kengaku`. | **Adjacent, Ceded.** Chousa disclaims benchmark grading and routes all evaluation claims to kengaku. No edits to chousa. |
| `kasegi-shokunin` | `SKILL.md:76-79,640-641,1031`: Mentions `safe_harbor` strictly in the legal bug-bounty vulnerability disclosure context (SEAL Whitehat / program safe harbor vs routine research). | **Disjoint Domain.** Lexical collision only; completely unrelated to the Harbor benchmark harness or grading code. No overlap. |
| `lore-shokunin` | `corpus/README.md:25`: Mentions "harbor clerk" as an in-world institutional entity / docket filing location. | **Disjoint Domain.** Fictional worldbuilding entity; no overlap with benchmark software. |
| `tabi-shokunin` | `SKILL.md:202,350,402,598`: Uses Chrome DevTools Protocol `Runtime.evaluate` to inspect browser DOM state and accessibility tree nodes. | **Disjoint Domain.** Web browser automation mechanism, not benchmark task evaluation or scoring code. |
| `kama-shokunin` | `SKILL.md:35,200-216` & `PROVINCE.md:17-21`: Inspects local model serving endpoints (`tools/kama-probe.sh check` for llama.cpp / ollama sockets and listeners). | **Disjoint Domain.** Local endpoint infrastructure health, not benchmark execution or task grading semantics. |
| All other siblings (`souji`, `kaidoku`, `tsukuroi`, `mado`, `tameshi`, `mori`, `kake`, `kumitate`, `revenger`, `kotoba`, `kotodama`) | Zero mentions of Terminal-Bench, Harbor framework, or benchmark grading logic. | **Exclusive Ownership.** Kengaku retains sole ownership of benchmark task-spec audits (`Terminal-Bench 2.0`, `SWE-bench Pro`, `Toolathlon`), verifier execution models (`benchmark-verifier-execution-model.md`), and grader semantics (`benchmark-grader-semantics.md`). |

### Surface (b): Source-Adoption & Registry Tooling (`sources_adopt.py`)

| Sibling Lane / Surface | Findings & Citations | Scope Ruling |
|---|---|---|
| `kengaku-shokunin` (Lane) | `plans/sources_adopt.py:1-60` (created r29a2, refined r30/r31; cited `PROVINCE.md:224-227`): Pre-append gate for candidate rows from `shokuknow/merge/kengaku/SOURCES.append.md`. Enforces 0–3 leading spaces ID collision detection against live `corpus/SOURCES.md`, validates 11-column schema, normalizes prose `recheck` to access date, binds URL maps to captured artifacts, and checks $\le 25$-word quote substrings. | **Lane-Local Instrument.** Kengaku is the only lane operating a pre-append adoption gate. |
| `kasegi-shokunin` | `.ufo/waves/round-25/wave1/ConnectorSiblings.md:18`: Evaluated kengaku's `sources_adopt.py` and ruled it: `adjacent, different surface — a SOURCES.md table cell holding a due date, not a knowledge-entry command line.` | **Adjacent, Ceded.** Kasegi confirmed boundary separation; operates no adoption tool. |
| `chousa-shokunin` | `tools/quarantine-check.py:1-30,290-294`: Re-derives absent-defect-register slices from the external campaign tree and inspects quotes against cached captures (`.qcache`). Reports `present`/`absent`/`mixed`/`unverifiable`. Mentions `adoptable later; adoption closed this round`. `tools/quote-reopen.py`: reopens quotes against existing `corpus/SOURCES.md`. | **Adjacent, Non-Conflicting.** Chousa evaluates external campaign quarantine slices read-only; does not generate append blocks, check ID collisions, or gate row adoption into `SOURCES.md`. |
| `kama-shokunin` | `tools/sources-append-only.py:1-50` (KQ22): Enforces Git commit-pair append-only diff invariants on `corpus/SOURCES.md` (`--from A --to B`). | **Adjacent, Complementary.** Kama checks post-commit Git diffs; does not perform pre-append row validation, quote matching, or candidate adoption. |
| `tabi`, `kagi`, `kumitate`, Fleet Root | `tabi/scripts/check-sources.mjs`, `kagi/corpus/sources-census.sh`, `kumitate/scripts/sources-check.mjs`, and fleet `scripts/sources-census.sh`: Validate committed `corpus/SOURCES.md` files against SOURCES-CONTRACT-v1 (NF=13, E01–E12, W01–W04). | **Post-Append Audit.** Fleet census and lane integrity scripts audit the already-committed registry; they do not perform pre-append staging or candidate row normalization. |

### Surface (c): Defect Counters & Receipt Validators of Matching Shapes

| Sibling Lane | Findings & Citations | Scope Ruling |
|---|---|---|
| `kengaku-shokunin` (Lane) | `plans/round34_defects.py` (N1–N8) and `round34_c1_verify.py` output `checks=8 defects=0` (exit 0); `plans/round34_mutate.py` outputs `MUTANTS total=8 detected=8` (exit 0). Prior rounds: `round33_defects.py` (`checks=6 defects=0`), `round30_defects.py` (`defects=5` $\to$ `0`). | **Lane-Local Contract.** Exact predicate and output string format (`checks=N defects=N`, `MUTANTS total=8 detected=8`) is unique to kengaku. |
| `tameshi-shokunin` | `tools/mutate-and-run.sh` (`SKILL.md:162-234,834-853`): Fleet reusable verification-fixture and mutation-testing engine. Emits `MUTATE: DONE (target=... defects=D killed=K survived=S inconclusive=I kill-rate=P%)` and `REGRESSION_CASE <leg>: PASS (band: killed-delta<=0 flips<=0 defects=D)`. `PROVINCE.md:14-17`: `Refuses: product domains — every lane's gate remains its own; tameshi owns only the reusable craft`. | **Methodology Parent, Gate Ceded.** Tameshi provides the reusable mutation craft principles (driver uniqueness check, clean control first, restore verification), but explicitly disclaims owning or editing lane-specific gates. |
| `kaidoku-shokunin` | `tools/routed-defects.py` (r18–r20) and `defect-probes.py`: Checks routed defects from prior rounds (`ROUTED_DEFECTS: 6/6 closed`). Emits bespoke JSON and probe records. | **Parallel Pattern, Disjoint Implementation.** Same architectural concept (re-deriving routed defects from prior spotchecks), but uses kaidoku-specific exit codes and probe runners. |
| `chousa-shokunin` | `tools/research-gate.sh` (`RESEARCH_GATE: CLEAN` / `DRIFT`) and `round48/mutation-check.py` (`MUTANTS_KILLED=5/5`). | **Adjacent Gate.** Distinct research-gate contract and exit codes. |
| `kake-shokunin` | `scripts/receipt_replay.py` (`0 clean receipts; 1 failed receipt criterion; 2 could-not-evaluate`) and `scripts/citing_set.py`. | **Disjoint Domain.** Static site publishing and accessibility receipt replay. |
| `kama-shokunin` | `tests/llamacpp-live/check-receipt.py`: Validates v3 JSON receipts against schema and SHA256 hashes of model, server, probe, and tool. | **Disjoint Domain.** Serving daemon receipt validator. |
| `souji-shokunin` | `tools/souji-axis-check.py`, `souji-receipt-run.py`, and `impl-06.sh` (internal bash counter variable `checks=0`). | **Disjoint Domain.** Workspace hygiene and preservation receipt runner. |
| `kumitate-shokunin` | `scripts/round-gate.mjs`: Checks wave status and reports (`CLEAN, checks=10, no findings`). | **Disjoint Domain.** Fleet orchestration gate. |

### Summary of Overlaps Audited and Ruled

1. **chousa (model evaluation):** Refused by chousa (`PROVINCE.md:11`), routed exclusively to kengaku. Ruled clean.
2. **kasegi (safe_harbor):** Terminology collision on legal safe harbor; no technical overlap. Ruled clean.
3. **lore (harbor clerk):** Fiction setting terminology collision; no technical overlap. Ruled clean.
4. **tabi (Runtime.evaluate):** CDP browser evaluation collision; no technical overlap. Ruled clean.
5. **chousa (quarantine-check):** External campaign cache inspector; does not do row adoption. Ruled clean.
6. **kasegi (sources_adopt review):** Pre-established adjacent surface in r25. Ruled clean.
7. **kama (sources-append-only):** Git diff append-only guard; complementary to pre-append gating. Ruled clean.
8. **tameshi (mutation harness craft):** Reusable mutation craft parent; cedes lane gate ownership to kengaku. Ruled clean.
9. **kaidoku (routed-defects):** Parallel historical routed-defect closing pattern; distinct implementation. Ruled clean.
10. **chousa (mutation-check):** Parallel mutation verification; distinct contract. Ruled clean.
11. **kake / kama / souji / kumitate (receipt validators):** Domain-specific gates; distinct contracts and outputs. Ruled clean.

**Overlaps tally:** 11 potential touchpoints audited across 15 sibling lanes; 0 conflicting collisions; all 11 scope boundaries ruled.

---

## 2. UFO-FSD Connector Synthesis

### Evidence & Contradictions Across Round Proposals

1. **Quarantine & Assimilation Contradiction:**
   - `plans/round-34-claims.md` §10 (lines 125–133) calls for hand-checking staged rows S091 (NEC) and S105 (METI) and adopting verified rows under new IDs S108/S109, cited by `corpus/knowledge/provider-selfreport-eval-limits.md`.
   - Evidence from `R34ReviewRowsQuarantine.md:7-9`, `R34ReviewEntryProvider.md:3-6`, and `R34CriticAssimilation.md:5-7` reveals a fatal defect: the capture for staged S091 (`assimilation/captures/nec-s091.html`, 418 bytes) is an Akamai `Access Denied` HTTP 403 page. No quote was retrieved. Drafting S108 with an unlocated NEC quote would commit a fabrication defect.
   - Conversely, staged S105 (METI / Geniac) in `assimilation/captures/geniac-s105.html:112` successfully captures the non-public hold-out evaluation sentence.
   - Sibling precedent from `chousa-shokunin/tools/quarantine-check.py:28-30` shows the exact honest resolution: unlocated or blocked captures are classified as unverifiable/refused, and must never block verified sibling rows or force synthetic quote attribution.

2. **C2 Calibration & Mutation Testing Tension:**
   - `R34CriticC2.md:3-15` shows that initial drafts of `round34_mutate.py` failed early on clean-tree preflight (`CLEAN exit=1`), and the width/newline red-before receipts lacked execution evidence on the pre-hardened tree.
   - Sibling precedent from `tameshi-shokunin/SKILL.md:162-178` establishes the invariant: driver must assert clean control first (`CONTROL: GREEN`), verify single-edit uniqueness (`count(old) == 1`), and isolate mutations.

3. **Considerthese Q23 Anchor Gap:**
   - `R34ReviewConsiderthese.md:13,19-24` noted that while proposal 2 correctly drafted the recurrence-block rule for Q23, it failed to cite its direct predecessor Q22 (`corpus/QUALITY.md:257-271`), which explicitly named the persistent `corpus/defects.jsonl` ledger as debt.

### Proposed Move

**"Quarantine-Decoupled Single-Row Adoption and Clean-Control-First Calibration Gate"**

1. **Decouple Provider Entry Adoption:**
   - Formally refuse staged row S091 (NEC) in the round Gate and `corpus/lessons/round-34.md` with explicit reason `access-denied/payload-absent` (Akamai 403 stub, 418 bytes; no quote located). Never fabricate an S108 row.
   - Adopt staged row S105 (METI) under the single new ID **S108** using its verified line-112 capture anchor from `geniac-s105.html`.
   - Scope `corpus/knowledge/provider-selfreport-eval-limits.md` to analyze METI's GENIAC hold-out program report as a single verified provider self-report under Q5, avoiding any reliance on the absent NEC text.
2. **Apply Tameshi Control-First Discipline to C2:**
   - Require `plans/round34_mutate.py` to enforce `CONTROL: GREEN` (`checks=8 defects=0`, exit 0) before executing the 8 mutants across the 4 classes.
   - Generate and commit the missing pre-hardening red-before receipt for width/newline (`falsify/red-before/width-newline.txt`) using the pre-hardened baseline.
3. **Anchor Q23 to Q22:**
   - In `corpus/QUALITY.md` Q23, explicitly cite Q22's named debt (`corpus/defects.jsonl`) to preserve the evidence chain from `considerthese/2026-10-25.md`.

### Affected Axes
- **Coverage:** Advances C1 coverage on Terminal-Bench 2.0 scoring code without stalling on quarantined payload-absent rows.
- **Calibration:** Hardens C2 with genuine pre-hardening red-before receipts and clean-control enforcement, preventing ungrounded adoption.
- **Adjacency:** Preserves strict non-interference with chousa and tameshi provinces.

### Second-Order Effects & Risks
- *Second-Order Effect:* Adopting only METI (S108) means the registry grows by 4 rows (S105, S106, S107 for C1 + S108 for METI) instead of 5. This preserves truthfulness while satisfying §10's instruction that only *verified* rows are adopted.
- *Risk:* Downstream reviewers expecting a 2-source provider entry must verify that Q5 allows a single-provider self-report study. This is confirmed by `R34ReviewEntryProvider.md:7-9` and `R34CriticAssimilation.md:7`.

### Verification Commands
1. C1 counter: `python3 plans/round34_c1_verify.py --lane .` $\to$ `checks=8 defects=0`, exit 0.
2. C2 counter: `python3 plans/round34_defects.py --lane .` $\to$ `checks=8 defects=0`, exit 0.
3. C2 mutation harness: `python3 plans/round34_mutate.py` $\to$ `MUTANTS total=8 detected=8`, exit 0.
4. Fleet census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` $\to$ exit 0 (15 W04).

---

VERDICT: conn-sibling (overlaps 11, ruled)

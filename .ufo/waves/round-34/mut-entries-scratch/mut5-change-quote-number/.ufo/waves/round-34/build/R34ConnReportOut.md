# R34ConnReportOut — Candidate Report-Outs & UFO-FSD Connector Synthesis

Round 34 (hyaku run 7, 2026-10-25). Lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Role: UFO-FSD connector (`R34ConnReportOut`).
Report path: `.ufo/waves/round-34/build/R34ConnReportOut.md`.
Baseline freeze commit: `adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae`.

---

## 1. Scope & Sibling Domain Fences

Kengaku owns LLM/model research and evaluation (`kengaku-shokunin/PROVINCE.md:3`). It refuses model serving execution, orchestration runtime, prompt craft, deep-research methodology, and fleet-wide protocol standards (`PROVINCE.md:6, 136-141`).
In round 34, empirical findings from C1 (Terminal-Bench 2.0 `protein-assembly` evaluator audit), C2 (mutant-hardened counter), quarantine verification (S091/S105), and package screening generated facts that touch sibling jurisdictions.
Per `PROVINCE.md:6, 43, 58`, these facts are reported out rather than absorbed into the lane.

---

## 2. Candidate Report-Out Lines (Evidence Sent, Not Absorbed)

The following 11 report-out lines name the owning lane and the exact evidence pointer across the four required categories:

### (a) Serving-Plane & Route-Table Facts (kama / kumitate)

1. **Terminal-Bench / Harbor containerized verifier execution and reward ingestion (kumitate / kama):**
   - **Owning lane:** `kumitate-shokunin` (orchestration runtime) & `kama-shokunin` (serving/runtime inspection).
   - **Evidence pointer:** `.ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh:18-30` & `.ufo/waves/round-34/build/R34CaptureTB2Eval.md:32`.
   - **Fact:** The benchmark task runner `test.sh` invokes pytest in container verifier mode (`pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA`) and writes binary outcome `1` or `0` to `/logs/verifier/reward.txt`. Harness verifier-mode resolution (`shared` vs `isolated`), test-space restoration, and reward file ingestion/aggregation belong to kumitate's orchestration runtime and kama's serving execution boundary; kengaku observes only static AST grading semantics (`test_outputs.py`).

2. **Swarm wave v2 role-table validator discrepancy (kumitate):**
   - **Owning lane:** `kumitate-shokunin` (orchestration & tooling).
   - **Evidence pointer:** `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy-v2.json:256-306`, `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:263-276`, and `.ufo/waves/round-34/build/R34ReconV2Shape.md:7`.
   - **Fact:** Swarm wave v2 policy in `ufo-wave-policy-v2.json` lists `labrat` as a member role, but the executable CLI orchestrator `ufo-swarm-wave.mjs` rejects `labrat` and requires `sentinel` (along with scout, reviewer, critic, connector, executor, mutation-tester, revenger, simplifier, scribe); role-table schema parity between policy JSON and orchestrator CLI belongs to kumitate.

3. **Fleet-root vs lane-relative report path resolution in defect counters (kumitate):**
   - **Owning lane:** `kumitate-shokunin` (tooling & workspace conventions).
   - **Evidence pointer:** `.ufo/waves/round-34/build/R34ReviewClaimsFile.md:87-95`, `.ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py:12-13`, and `plans/round33_defects.py:40-42`.
   - **Fact:** The draft round-34 defect counter attempts to read `.ufo/reports/round-31/kengaku.md` and `round-32/kengaku.md` via lane-relative paths where they do not exist (causing clean-tree exit 1), whereas round 33 correctly anchored them to `FLEET_ROOT` (`/home/vgpnk/Projects/shokunin/.ufo/reports/...`). Standardizing cross-lane report path anchors and working directory assumptions belongs to kumitate tooling.

### (b) Prompt-Craft Implications (kotoba)

4. **Instruction framing vs deterministic literal assertion divergence (kotoba):**
   - **Owning lane:** `kotoba-shokunin` (prompt & skill craft).
   - **Evidence pointer:** `.ufo/waves/round-34/assimilation/captures/tb2-eval/instruction.md:6,14-15,24-26`, `.ufo/waves/round-34/assimilation/captures/tb2-eval/test_outputs.py:25-36`, and `.ufo/waves/round-34/build/R34CriticEntryTB2.md:20-25`.
   - **Fact:** The natural-language prompt in `instruction.md` instructs the agent to query `antibody.fasta` and `/app/pdb_ids.txt` to select proteins and construct an assembled fusion. However, the grader `test_outputs.py` opens neither file; it asserts hardcoded literal amino acid strings (`flag_aa`, `donor_aa`, `dhfr_aa`, `acceptor_aa`, `snap_aa`), strict literal index ordering, and GS linkers. Benchmark prompt engineers auditing agent failures must account for this instruction-vs-assertion divergence: agents generating biologically valid fusions with alternative valid sequences fail due to hidden string literal checks in the prompt harness.

5. **Grader docstring scope inflation vs executable assert coverage (kotoba):**
   - **Owning lane:** `kotoba-shokunin` (prompt & skill craft).
   - **Evidence pointer:** `.ufo/waves/round-34/assimilation/captures/tb2-eval/test_outputs.py:11-12,13-73` and `.ufo/waves/round-34/build/R34CriticEntryTB2.md:20-25`.
   - **Fact:** `test_outputs.py` lines 11–12 claim the test checks that output meets "all the requirements described in task.yaml," whereas lines 13–73 only test single-line representation, alphabet/length, literal subprotein presence/order, GS linkers, and GC windows, omitting API-selection and spectral identity criteria. Auditing prompt-contract fidelity against evaluation harnesses is a prompt-craft discipline belonging to kotoba.

### (c) Research-Method Boundaries (chousa)

6. **Anti-bot CDN edge-blocking on corporate technical journals (chousa):**
   - **Owning lane:** `chousa-shokunin` (deep-research method).
   - **Evidence pointer:** `.ufo/waves/round-34/assimilation/captures/nec-s091.html:1-10`, `.ufo/waves/round-34/build/R34CaptureNec.md:7-15`, and `.ufo/waves/round-34/build/R34ReviewRowsQuarantine.md:7`.
   - **Fact:** Direct HTTP retrieval of NEC 技報 Vol.75 No.2 (`https://jpn.nec.com/techrep/journal/g23/n02/230212.html`) returned a 418-byte Akamai CDN "Access Denied" response (`967e4c244fa...`), blocking quarantine verification and forcing an honest refusal of S091. Reusable research ladders for navigating corporate CDN anti-bot blocks and paywalls belong to chousa's research-method craft.

7. **Dynamic script injection causing archive snapshot digest drift (chousa):**
   - **Owning lane:** `chousa-shokunin` (deep-research method).
   - **Evidence pointer:** `.ufo/waves/round-34/assimilation/captures/geniac-s105.html:1-10`, `.ufo/waves/round-34/build/R34CaptureGeniac.md:4-9`, and `.ufo/waves/round-34/build/R34ReviewEntryProvider.md:5`.
   - **Fact:** Re-fetching the METI GENIAC Internet Archive snapshot (`20251118034714`) yielded byte-length parity (13,030 bytes) with SHA-256 digest drift (`2f46a1...` assigned vs `1bc2c1...` re-fetch) due to dynamic Wayback toolbar/timestamp script injection. Developing canonical content-digest normalization for archived web snapshots belongs to chousa.

8. **Composite constraint conjunctions in prior-art literature (chousa):**
   - **Owning lane:** `chousa-shokunin` (deep-research method).
   - **Evidence pointer:** `.ufo/waves/round-34/build/R34PriorArtTB2.md:5-20`.
   - **Fact:** Prior-art literature search (DNA Chisel, CodonTransformer, arXiv 1508.03428) confirms translation preservation and rolling GC windows are established techniques, but composite conjunction (*translation + strict ordered-subsequence + GS linkers + rolling GC*) in evaluators represents task-specific domain coverage rather than reusable algorithmic novelty. Adjudicating prior-art search breadth and novelty boundaries belongs to chousa.

### (d) Fleet-Process Referrals (protocol / aggregator)

9. **Persistent cross-round defect ledger implementation (protocol / aggregator):**
   - **Owning lane:** `protocol / aggregator` (fleet-wide governance).
   - **Evidence pointer:** `considerthese/2026-10-25.md:39-45`, `plans/round-34-claims.md:119-124`, and `.ufo/waves/round-34/build/R34Considerthese.md:4-8`.
   - **Fact:** Proposal 2 in `considerthese/2026-10-25.md` establishes that recurring defects block pre-registration unless hardened. Kengaku mined the lane-local half as `QUALITY.md` Q23, but the cross-round persistent ledger `corpus/defects.jsonl` and fleet-wide pre-registration enforcement require multi-lane authority and are referred to protocol/aggregator.

10. **Staged package registry ID collision and late-binding namespacing (protocol / aggregator):**
    - **Owning lane:** `protocol / aggregator` (merge pipeline / shokuknow).
    - **Evidence pointer:** `.ufo/waves/round-34/assimilation/collisions`, `.ufo/waves/round-34/build/R34ReconPackage.md:9-14`, and `plans/round-34-claims.md:62-65`.
    - **Fact:** Merge candidates staged from `shokuknow` reuse IDs (S105, S108, S114, S115) that collide with active lane numbering (kengaku baseline S104; round 34 mines S105–S107 for TB2 and adopts S109 for METI), forcing admission refusal on Q1/Q2 gates. Establishing a late-binding namespacing protocol for staged package source IDs belongs to the aggregator.

11. **Fleet census non-canonical URL warning (W04) budget policy (protocol / aggregator):**
    - **Owning lane:** `protocol / aggregator` (fleet registry protocol).
    - **Evidence pointer:** `scripts/sources-census.sh:1-60` and `.ufo/waves/round-34/claims/census-before.txt:1-16`.
    - **Fact:** Running `scripts/sources-census.sh validate` reports 15 `W04` warnings across the fleet. Defining whether W04 warnings must be burned down or tolerated under a fixed budget across rounds belongs to the aggregator.

---

## 3. UFO-FSD Connector Synthesis Proposal

### Title: Decoupled Hermetic Quarantine-Immune Verification Synthesis

### 1. Evidence
1. **Quarantine Refusal Contradiction:** Staged row S091 (NEC 技報) returned an Akamai 418 Access Denied response (`assimilation/captures/nec-s091.html`; SHA-256 `967e4c244fa...`). The quote cannot be located in captured bytes (`build/R34CaptureNec.md:15`, `build/R34RowsQuarantine.md:7`). Adopting S108 would fabricate provenance; honest stop is mandatory (`build/R34ReviewEntryProvider.md:3`).
2. **C1/C2 Coupling via N8:** C2 claims separability from C1 (`plans/round-34-claims.md:102-105`), but `round34_defects.py` check N8 scans `corpus/knowledge/*.md` against `corpus/README.md` index rows. If the draft provider entry (`build/R34EntryProvider/entry.md`) is committed without passing all gates or without a README index row, N8 fails closed.
3. **C2 Clean-Tree Exit 1:** `round34_defects.py` fails on the clean tree (`checks=8 defects=3`, exit 1) because N3/N4 use lane-relative paths for fleet-root reports (`build/R34ReviewClaimsFile.md:87-95`), and N7 looks for a dated correction in `round-33.md` that does not exist.
4. **C1 Counter Format Mismatch:** Draft C1 counter V7 fails against the committed `claims/control-c1.txt` because V7 expects regex `registry rows = 97`, whereas the frozen receipt reads `## registry rows count (expect 97)\n97` (`build/R34ReviewCounterC1.md:57-65`).

### 2. Affected Axes
- **Calibration (C2):** Directly improved from failing (exit 1) to sound (exit 0) by fixing path resolution and coupling invariants.
- **Coverage (C1):** Protected and verified honestly: lands S105–S107 (3 TB2 rows) while maintaining honest refusal of S108 without breaking the registry.
- **Adjacency:** Maintained strictly clean (0 unrouted collisions; 11 verified report-outs).
- **Operability:** Eliminates circular landing locks and ensures clean hermetic verification.

### 3. Proposed Move
Synthesize the round's landing via a three-point bounded move:
1. **Hermetic Quarantine Partitioning:** Enforce that `corpus/knowledge/provider-selfreport-eval-limits.md` is NOT admitted to `corpus/knowledge/` this round because S108 failed capture verification (Akamai 403). Retain METI S109 adoption in the assimilation archive and record honest refusal in `corpus/lessons/round-34.md`. This prevents N8 index-vs-HEAD desynchronization.
2. **Fleet-Root Path Normalization in N3/N4:** In `plans/round34_defects.py`, resolve report paths via `FLEET_ROOT / ".ufo/reports/round-{31,32}/kengaku.md"` (matching `round33_defects.py`) rather than relative lane paths.
3. **Control Receipt Format Reconciliation in V7:** In `plans/round34_c1_verify.py`, adjust the V7 receipt parser to accept multiline number values matching `claims/control-c1.txt` (`expect 97\n97`), ensuring the frozen receipt passes without modification.

### 4. Second-Order Effects & Explicit Contradictions
- **Substrate & Runtime:** Zero network calls or external fetches during verification; no duplicate files created at fleet or lane root.
- **Contract Integrity:** SOURCES v1 format strictly preserved (pipe-wrapped `NF=13`).
- **Contradiction Resolved:** The frozen plan anticipated adopting both S108 and S109, but empirical reality delivered an Akamai 403 on S091. Acknowledging this honest stop resolves the contradiction between frozen optimism and evidentiary rigor without compromising C1's 3-row delivery.

### 5. Risks & Mitigations
- *Risk:* Omission of the provider entry could be seen as reducing planned round scope.
- *Mitigation:* Frozen claims explicitly specify the kill rule: "a cited source whose located quote cannot be found in this round's captured bytes at the pinned revision is refused for that row" (`plans/round-34-claims.md:59-65, 131-133`). Refusing S108 is compliance with the frozen contract, not scope reduction.

### 6. Verification
1. Run `python3 plans/round34_c1_verify.py --lane .` → prints `checks=8 defects=0`, exits 0.
2. Run `python3 plans/round34_defects.py --lane .` → prints `checks=8 defects=0`, exits 0.
3. Run `python3 plans/round34_mutate.py` → prints `MUTANTS total=8 detected=8`, exits 0.

---

VERDICT: conn-reportout (11 lines)

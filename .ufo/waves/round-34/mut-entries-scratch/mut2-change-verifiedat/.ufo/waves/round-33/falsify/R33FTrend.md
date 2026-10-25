# R33FTrend — Cross-Claim Trend and Overlap Check (Falsify Seat)

Seat: `KengakuR33.R33FTrend` (connector / reviewer; leaf seat, no subagents).
Date: 2026-10-25. Hyaku run 7.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Milestone: Falsify each frozen claim, counter, gate, source row, and landing artifact using build-wave findings.
Contract: Read-only inspection; no lane/fleet file edited or mutated; no tools installed. All executed commands run in read-only mode or in an isolated `/tmp` scratch area.

VERDICT: limitation

---

## 1. Executive Summary & Observed Measurements

This review executes a cross-claim analysis of Round 33 across three dimensions:
1. **Predicate vs Counter Fidelity:** Evaluating the alignment between the frozen predicates in `plans/round-33-claims.md` (`f0b20aea` + `c227e486`) and the three counting commands at lane tip `77ac8c1`.
2. **Causal Separability & Shared Dependencies:** Identifying shared files, index dependencies, and external fleet couplings that threaten the independence of C1 (coverage), C2 (calibration), and C3 (freshness).
3. **Learning Trend Analysis (`LEARNING.md`):** Evaluating the round's `expansion`, `quality`, and `discernment` trend claims against build-wave findings (`R33ClaimsReview.md`, `R33CounterAttack.md`, `R33GateMutants.md`, `R33C1KillRule.md`, `R33C3Design.md`, `R33ReportOut.md`).

### Exact Measurement Commands & Outputs at Tip

All three frozen counting commands were executed live on the current lane tree:

| Claim | Axis | Exact Frozen Command | Observed Exit | Observed Output |
|---|---|---|---|---|
| **C1** | Coverage | `python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census` | `0` | `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` |
| **C1 (receipt 2)** | Coverage | `python3 plans/round33_c1_verify.py --lane .` | `0` | `checks=8 defects=0` |
| **C2** | Calibration | `python3 plans/round33_defects.py --lane .` | `0` | `checks=6 defects=0` |
| **C3** | Freshness | `python3 plans/catalog_probe.py --verify --lane .` | `0` | `raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok`<br>`HF missing fields: author, sha, lastModified, gated` |

While all three counters green mechanically (exit 0), cross-claim scrutiny reveals structural gaps between the frozen predicates and their counters, unverified kill rules, circular derivations, shared-byte coupling, and an unaddressed quality regression.

---

## 2. Comparison of Frozen Predicates vs After Commands

### C1 — Coverage (Shokuknow Assimilation Round 5)
- **Frozen Predicate (`plans/round-33-claims.md:45-53`):**
  `corpus/knowledge/benchmark-grader-semantics.md` exists citing exactly S093, S103, S104; `verified-at: 2026-10-25`; each row in `corpus/SOURCES.md` with `status=mined`, `opened=2026-10-25`, and `used-by` naming the entry (S093 gains the entry; S103/S104 are new); exactly 1 index row in `corpus/README.md`; and `adoption_check.py --expect ... --census` prints `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` exit 0. Second receipt: `round33_c1_verify.py` exits 0 with `checks=8 defects=0`.
- **Observed Gaps & Limitations:**
  1. *Fictitious S093 Transition:* The claim text (`claims.md:37-38, 48-49`) asserts S093's used-by "gains the entry". At freeze commit `f0b20aea`, S093's `used-by` cell **already** contained `corpus/knowledge/benchmark-grader-semantics.md`. `git diff f0b20aea..HEAD -- corpus/SOURCES.md` shows zero changes to S093. S093 experienced zero transition this round.
  2. *Misstated Control Receipt:* The frozen claim (`claims.md:57-59`) claims the pre-append control prints `entries=0 …`. The committed control `.ufo/waves/round-33/claims/control-nothing.txt` actually prints `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=ok exit 1` (`R33ClaimsReview.md`).
  3. *Adoption Gate vs Landed Bytes Disconnect:* The kill rule (`claims.md:60-65`) requires that cited quotes resolve at the pinned revision. However, `adoption_check.py` and `round33_c1_verify.py` never invoke `sources_adopt.py` (`R33C1KillRule.md`). Re-running `sources_adopt.py --quote-file ... --url-map assimilation/url-map.json` against the landed S103 row **fails with exit 8** (`REFUSED S103 url-mismatch`) because S103 cites the repository root `https://github.com/hkust-nlp/Toolathlon` while the committed `url-map.json` maps to the blob URL (`R33GateMutants.md`). The green receipt in `assimilation/gate-receipts.txt` was produced using a different root-level map that was not committed.

### C2 — Calibration (Routed Defects N1–N6)
- **Frozen Predicate (`plans/round-33-claims.md:83-99`):**
  `round33_defects.py --lane .` prints `checks=6 defects=6` exit 1 on pre-repair tree and `checks=6 defects=0` exit 0 on repaired tree, covering N1 (tracked wave tree), N2 (`SCORECARD.md` carries `## Round 32` recording dispositions), N3 (appended erratum in fleet report round-31 with `a44b5a8` within 400 chars of `superseded` naming `ae95fe0`), N4 (fleet report round-32 contains `112091c`), N5 (`round-31.md` contains `:35-38` and correction note pointing at `:39-40`), N6 (`round-30.md` contains `:78-81`, correction note pointing at `:72` and `82-83`, erratum for S086).
- **Observed Gaps & Limitations:**
  1. *N2 Heading-Only Weakness:* `check_n2` checks only `re.search(r"^## Round 32\b", text, re.MULTILINE)`. A bare heading with no text or dispositions passes exit 0 (`R33CounterAttack.md` exploit E2; `R33FN2Meaning.md`).
  2. *N3 Window & Newline Defect:* Predicate requires `within 400 characters`; `check_n3` implements `width=300`. Furthermore, `near()` uses `.{0,300}` without `re.DOTALL`, causing it to fail on any erratum spanning a standard newline (`R33CounterAttack.md` E3b/E3c; `R33FN3Width.md`).
  3. *N4 Bare Token Presence:* `check_n4` performs an uncontextualized substring search for `112091c` anywhere in `.ufo/reports/round-32/kengaku.md`.
  4. *N5/N6 Token Scavenging:* Neither check enforces append-only semantics. A single fabricated sentence containing the required keywords passes both checks without repairing the historical errata (`R33CounterAttack.md` E5/E6).
  5. *External Fleet Coupling:* `check_n3` and `check_n4` hardcode absolute paths to `/home/vgpnk/Projects/shokunin/.ufo/reports/round-{31,32}/kengaku.md`. When run in an isolated archive or `/tmp` clone with `--lane <tmp>`, they ignore the lane clone and read the fleet repository (`R33FN34ExternalPaths.md`).

### C3 — Freshness (Public Model Catalogs Re-probe)
- **Frozen Predicate (`plans/round-33-claims.md:122-131`):**
  `catalog_probe.py --verify --lane .` exits 0 only when `corpus/evidence/round33/catalogs/` contains `hf.raw.json` and `or.raw.json` (each ≤ 64 KiB, digests matching `SHA256SUMS`), receipt records `hf_models=<n> or_models=<n> hf_schema_delta=<d> or_schema_delta=<e>`, every number re-derives exactly from committed raw bytes, and entry carries `## Re-probe 2026-10-25 (round 33)`.
- **Observed Gaps & Limitations:**
  1. *Oversized OpenRouter Response & Envelope Synthesis:* The live OpenRouter JSON response is 791,075 bytes, exceeding the 64 KiB cap. `catalog_probe.py` commits a synthesized envelope (`meta.observed_models = 467`) rather than raw response bytes (`R33C3Design.md`).
  2. *Circular Derivation of `or_models`:* In `--verify`, `parse_openrouter()` reads `meta.observed_models` directly from the committed envelope dictionary. It does not count or parse models from raw response bytes. A mutant with `meta.observed_models = 9999` and 1 model in `data` exits 0 (`R33C3Design.md` E1).
  3. *Kill Rule Inefficacy:* The kill rule claim ("no fabricated bytes may ever satisfy `--verify`") is false. Internally consistent fabricated JSON + self-computed sha256 digests pass `--verify` completely offline without verifying API authenticity (`R33C3Design.md` row a).

---

## 3. Causal Separability & Shared Dependencies

The round preregistration declares strict causal separability across the three claims:
- C2 separability (`claims.md:108-109`): *"reads only round-30/31/32 bytes (fleet reports, lessons, wave trees), `SCORECARD.md`, and this round's lesson/report — no artifact C1 or C3 creates."*
- C3 separability (`claims.md:141-142`): *"reads only `corpus/evidence/round33/catalogs/`, the catalog entry, and `plans/catalog_probe.py` — no artifact C1 or C2 creates."*

An exhaustive audit of counter callgraphs, file descriptors, and filesystem touches reveals several real shared bytes and cross-claim dependencies:

### 1. `SCORECARD.md` Cross-Claim Collision
- `SCORECARD.md` is C2's target under check N2 (`^## Round 32\b`).
- Concurrently, `SCORECARD.md` lines 1123–1137 host the `## Round 33` section that records the verdicts, before/after measurements, and scores of C1, C2, and C3.
- If an authoring seat landing C1 or C3 modifies `SCORECARD.md` (e.g. adding capability rows or landing measurements), a syntax error or heading corruption directly impacts C2's `check_n2`.

### 2. `corpus/lessons/round-30.md` Coupling via Census E11
- C2 check N6 modifies `corpus/lessons/round-30.md` (pointing the Q6 retraction at `:72` and `:82-83`).
- In `corpus/SOURCES.md`, row S086 has `used-by: corpus/knowledge/contamination-transparency-card.md, corpus/lessons/round-30.md`.
- C1 executes `plans/adoption_check.py --census`, which runs the fleet script `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate`.
- `sources-census.sh` rule E11 (`sources-census.sh:566-568`) checks that every `used-by` path on a mined row exists on disk.
- If C2's repair of `corpus/lessons/round-30.md` were to rename, delete, or relocate that file, C1's counting command would immediately fail with `E11` and `census=fail`, causing C1 to fail closed.

### 3. `corpus/lessons/round-33.md` Multi-Claim Aggregation
- C1's second receipt `plans/round33_c1_verify.py` check V7 (`check_v7`) explicitly reads `corpus/lessons/round-33.md` to ensure the renumber map (`S094->S103`, `S097->S104`) is recorded in the Gate.
- Concurrently, `corpus/lessons/round-33.md` records the mistakes and closures for C2 (round-32 untracked files, round-31 phantom hash) and C3 (round-32 missing fields).
- A syntax corruption in `round-33.md` introduced while documenting C2 or C3 will break C1's `round33_c1_verify.py`.

### 4. Fleet Repository External Dependencies
- C1 depends on the host fleet script `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` and `shokunin.conf`.
- C2 depends on absolute host paths `/home/vgpnk/Projects/shokunin/.ufo/reports/round-31/kengaku.md` and `round-32/kengaku.md`.
- Neither counter is hermetically contained within the lane repository directory passed to `--lane`.

### 5. Critical Attack: Falsification of the `R33Connector.md` Coupling Proposal
In the build wave, `R33Connector.md` §3 proposed:
> *"Synthesize the tip-verification pass by having the final round-33 defect verification script (`plans/round33_defects.py` or the L1 integration wrapper) execute `plans/catalog_probe.py --verify --lane .` and `plans/round33_c1_verify.py --lane .` as mandatory sub-checks of the tip calibration state. If any offline re-derivation fails or produces empty/unbound output, C2 fails closed with exit 1."*

**Falsification Verdict:** This proposal is a direct violation of causal separability.
- C2 is calibration on historical round-32 routed defects (N1–N6).
- If C2 executes C1 and C3 verifiers, any failure in C1 (coverage) or C3 (freshness) causes C2 (calibration) to fail closed.
- It destroys the orthogonality of the three axes and violates the inviolable preregistration contract (`plans/round-33-claims.md:6-7`): *"Three claims, three distinct axes... a predicate changed after a seat has scored is not this claim's predicate."*
- **Observed build-wave outcome:** The build wave correctly rejected this proposal; `plans/round33_defects.py` at tip retains exactly the six isolated checks N1–N6.

---

## 4. Assessment of Learning Trend Claims (`LEARNING.md`)

`LEARNING.md:31-38` defines the three mandatory learning trends:
- **expansion:** net new admitted entries on uncovered ground (`improved`), or an admitted entry fails its bar (`harmed`).
- **quality:** weaker entries superseded, or stale entries re-verified (`improved`), or an entry is found false/stale and left unmarked (`harmed`).
- **discernment:** outside spot-check agrees with gate on admits and rejects (`improved`), or disagreement left unlearned (`harmed`).
- **Non-trade invariant (`LEARNING.md:37-38`):** *"Growth without quality is not learning: `expansion: improved` with `quality: harmed` is a trade, reported as a trade, never admitted."*

### A. Expansion Trend: Fragile & Stale Gating
- **Claimed Verdict:** `expansion: improved` (C1 admits `corpus/knowledge/benchmark-grader-semantics.md` under S103/S104).
- **Evaluation:**
  - *Uncovered Ground:* Validated. `corpus/README.md` coverage map previously had open gaps on benchmark harness scoring logic. Toolathlon A/B testing task evaluator analysis is net-new corpus knowledge.
  - *Counter & Receipt Gaps:* The admission is undermined by the fact that `sources_adopt.py` fails exit 8 with the committed `url-map.json` (`R33GateMutants.md`). The admission was committed based on an uncommitted or out-of-band map. The S093 `used-by` delta claim is fictitious.
  - *Ledger Status:* Numerical coverage remains 7 under the round-25 L0 cap. Expansion is recorded as a ledger delta, which is permitted per `claims.md:70-71`.

### B. Quality Trend: Concrete AXIS HARM Uncovered
- **Claimed Verdict:** `quality: improved` or `held` (C3 byte-retained catalog re-probe; C2 defect closures).
- **Evaluation:**
  1. *OpenRouter Raw Bytes Omission:* The 64 KiB cap was breached (791 KiB actual response). Bounded raw response bytes were not retained; a synthetic envelope was committed instead.
  2. *Active Stale Assertion in `open-model-catalogs.md` (AXIS HARM):*
     - C3 modified `corpus/knowledge/open-model-catalogs.md` by appending `## Re-probe 2026-10-25 (round 33)`.
     - In that exact same file, lines 48–55 carry section `## Local inventory (this host)`:
       ```markdown
       - llama-server model file path is the catalog: `/scratch/models/` GGUFs
         (observed `qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`
         served on `127.0.0.1:34113` via `qwen-coder.service`).
       - `GET <server>/v1/models` returns the served id — always prefer this
         over provider config...
       ```
     - This text asserts in the active present tense that `qwen-coder.service` is serving on `127.0.0.1:34113`.
     - Live read-only check (`R33ReportOut.md:124-142`):
       - `ss -ltn 'sport = :34113'` → no listener.
       - `test -e ~/.config/systemd/user/qwen-coder.service` → unit absent.
       - Kama registry `kama-shokunin/registry/history/DELTA.md:20` confirms `systemd-qwen-coder` has been row-absent since `2026-10-14T12:42:32Z`.
     - **Violation of `LEARNING.md:34`:** *"harmed when an entry is found false or stale and left unmarked."*
     - The lane amended `open-model-catalogs.md` in Round 33 while leaving an actively false, dead serving-plane inventory unmarked.
     - **Consequence:** Under `LEARNING.md:37-38`, claiming `expansion: improved` while `quality: harmed` is an impermissible trade that must be reported as a trade and cannot be admitted.

### C. Discernment Trend: Unsupported at Current Tip
- **Claimed Verdict:** `discernment: improved` (in Round 32 report; attempted in Round 33).
- **Evaluation:**
  - `LEARNING.md:42-46` explicitly dictates:
    > *"Self-assessed taste is not discernment. Each round a non-author — a fresh reviewer or the operator — spot-checks a sample of that round's gate decisions, at least one admit and one reject, and records agree/disagree with a reason in the round's lesson. A subagent the lane dispatched is still the lane."*
  - In Round 32, `discernment: improved` was claimed based on lane falsify seats (`FxEntryTruth.md`, `FxFailOpen.md`, etc.). This violated the protocol because lane-dispatched seats are still the lane (`R33ScorecardPatch.md`).
  - In Round 33, no non-author spot-check exists at the tip. `corpus/lessons/round-33.md` leaves the spot-check absent/pending.
  - Any claim of `discernment: improved` at this stage is unsupported. The only defensible verdict at lane close is `discernment: unchanged`.

---

## 5. UFO-FSD Connector Move: Hermetic Decoupled Tip Verification & Quality Repair

To address the findings without violating causal separability or altering frozen claim predicates, the following bounded move is proposed:

### 1. Evidence
- `R33Connector.md` §3 proposed coupling all counters into `round33_defects.py`, destroying causal separability.
- `R33GateMutants.md` proved `assimilation/url-map.json` is stale and breaks `sources_adopt.py` exit 8 against landed S103.
- `R33ReportOut.md:124-142` proved `open-model-catalogs.md:48-55` asserts a dead service in present tense, triggering `quality: harmed`.
- `QUALITY.md` Q22 requires re-running receipts at the tip, but no mechanism re-checks gate-to-source alignment.

### 2. Affected Axes
- **Calibration (C2):** Protected by maintaining strict isolation of `plans/round33_defects.py` from C1/C3 artifacts.
- **Freshness & Quality:** Improved by eliminating the stale serving-plane assertion in `open-model-catalogs.md`.
- **Coverage (C1):** Stabilized by aligning `url-map.json` with S103's landed citation.

### 3. Proposed Move
1. **Preserve Causal Separability:** Reject any coupling of C1/C3 into `plans/round33_defects.py`. The three frozen commands remain strictly independent.
2. **Quality Repair (Eliminate Stale Inventory):** In `corpus/knowledge/open-model-catalogs.md`, mark section `## Local inventory (this host)` as `ABSENT / HISTORICAL (service deleted 2026-10-14, port 34113 unlistened)` matching kama's DELTA.md. This removes the false present-tense statement and prevents `quality: harmed` under `LEARNING.md:34`.
3. **Artifact-Gate Alignment:** Correct `assimilation/url-map.json` to map `toolathlon-ab-testing-evaluation-main.py` to the repository root `https://github.com/hkust-nlp/Toolathlon` (as cited by landed row S103), ensuring `sources_adopt.py` reproduces the green receipt in `assimilation/gate-receipts.txt`.
4. **Decoupled Orchestrator Receipt Auditor:** Provide an out-of-band orchestrator verification script (run after lane close, outside the frozen claim counters) that independently re-runs C1, C2, C3, and `sources_adopt.py` against committed tip bytes without coupling their failure paths.

### 4. Risks & Second-Order Effects
- *Risk:* Editing `open-model-catalogs.md` could invalidate C3's `--verify` check.
- *Mitigation:* C3's `catalog_probe.py:entry_ok` only searches for the literal block `## Re-probe 2026-10-25 (round 33)` and its four number tokens. Modifying lines 48–55 leaves the re-probe block at line 66 untouched; `catalog_probe.py --verify` remains exit 0.

### 5. Verification
- Run `python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census` → exit 0.
- Run `python3 plans/round33_defects.py --lane .` → exit 0 (`checks=6 defects=0`).
- Run `python3 plans/catalog_probe.py --verify --lane .` → exit 0.
- Re-run `plans/sources_adopt.py --quote-file ... --url-map ...` → exit 0 with all spans bound.
- Verify `grep -n 'served on 127.0.0.1:34113' corpus/knowledge/open-model-catalogs.md` shows historical/ABSENT marking.

---

## 6. Scoped Findings & Verdict Summary

| Target Area | Finding / Limitation | Verdict Status |
|---|---|---|
| **C1 Predicate Fidelity** | Control receipt misstated as `entries=0`; S093 used-by delta is fictitious (already present at freeze). | `limitation` |
| **C1 Gating Consistency** | Committed `url-map.json` fails exit 8 against landed S103; green receipt used an uncommitted map. | `uncaught` (by C1 counters) |
| **C2 Predicate Fidelity** | `check_n2` passes on empty heading; `check_n3` width 300 vs frozen 400; `near()` broken across newlines. | `limitation` |
| **C2 External Coupling** | `check_n3` and `check_n4` hardcode absolute fleet-repo report paths; non-hermetic to `--lane`. | `limitation` |
| **C3 Predicate Fidelity** | OpenRouter raw response breached 64 KiB cap; synthetic envelope committed; count read circularly from `meta`. | `limitation` |
| **Causal Separability** | Shared touches on `SCORECARD.md`, `round-30.md` (via census E11), and `round-33.md`. Proposed C2 coupling falsified. | `caught` / `rejected` |
| **Learning Trends** | `expansion: improved` carries stale gating; `quality: harmed` due to unmarked dead service in `open-model-catalogs.md`; `discernment: improved` unsupported without non-author spot-check. | `limitation` |

VERDICT: limitation

## L1 integration correction

This connector report repeated several build-wave snapshots rather than the final lane bytes. At final integration, S103 cites only the pinned `main.py` blob, S104 cites `/abs/2412.05579v2`, the committed map matches those URLs, and the landed-row quote gate passes 8/8; the earlier root-only/url-mismatch statement is stale. C3's current `or.raw.json` is the complete 16,010-byte `?limit=10` API response (not a synthesized envelope); `or_models=467` is parsed from its `total_count` field, while origin authentication remains outside `--verify`. `SCORECARD.md`/lesson co-location is a potential maintenance dependency, but the three current predicates read separate conditions and C2's N2 only searches for the `## Round 32` heading; the report's causal-failure assertion is not demonstrated. The historical `:34113` absence note is not evidence of a current service state. This addendum supersedes snapshot claims above that conflict with final files; the C1 false S093 transition and C2 counter limitations remain.
